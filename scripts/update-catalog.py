#!/usr/bin/env python3
"""Generate catalog.json from themes/*.json files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
THEMES_DIR = ROOT / "themes"
DEFAULT_REPO = "Silo-Server/silo-themes"
DEFAULT_BRANCH = "main"

THEME_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CATALOG_FIELDS = [
    "id",
    "name",
    "description",
    "author",
    "previewAccent",
    "previewBg",
    "tags",
    "downloadUrl",
    "version",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--themes-dir", type=Path, default=THEMES_DIR)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument(
        "--touch",
        action="store_true",
        help="bump updatedAt even if the catalog entries are unchanged",
    )
    parser.add_argument(
        "--updated-at",
        help="override updatedAt; useful for deterministic tests",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero instead of writing when catalog.json is stale",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")

    return data


def theme_id_from_path(path: Path) -> str:
    name = path.name
    if name.endswith(".silo-theme.json"):
        return name[: -len(".silo-theme.json")]
    return path.stem


def validate_theme(path: Path, theme_id: str, theme: dict[str, Any]) -> None:
    if not THEME_ID_RE.fullmatch(theme_id):
        raise ValueError(
            f"{path}: theme id '{theme_id}' must be a kebab-case slug"
        )

    for key in ["name", "description", "author"]:
        if not isinstance(theme.get(key), str) or not theme[key].strip():
            raise ValueError(f"{path}: missing non-empty string field '{key}'")

    if not isinstance(theme.get("vars"), dict):
        raise ValueError(f"{path}: missing object field 'vars'")


def discover_themes(themes_dir: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    discovered: dict[str, tuple[Path, dict[str, Any]]] = {}

    for path in sorted(themes_dir.glob("*.json")):
        theme_id = theme_id_from_path(path)
        theme = load_json(path)
        validate_theme(path, theme_id, theme)

        if theme_id in discovered:
            first_path = discovered[theme_id][0]
            raise ValueError(
                f"{path}: duplicate theme id '{theme_id}' already defined by {first_path}"
            )

        discovered[theme_id] = (path, theme)

    return discovered


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def first_string(*values: Any, fallback: str) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value
    return fallback


def default_tags(theme: dict[str, Any]) -> list[str]:
    base_theme = theme.get("baseTheme")
    if isinstance(base_theme, str) and "light" in base_theme:
        return ["light"]
    return ["dark"]


def build_entry(
    theme_id: str,
    path: Path,
    theme: dict[str, Any],
    previous: dict[str, Any] | None,
    repo: str,
    branch: str,
) -> dict[str, Any]:
    vars_obj = theme["vars"]
    rel_path = path.relative_to(ROOT).as_posix()

    entry: dict[str, Any] = {
        "id": theme_id,
        "name": first_string(
            previous.get("name") if previous else None,
            theme.get("name"),
            fallback=theme_id,
        ),
        "description": first_string(
            previous.get("description") if previous else None,
            theme.get("description"),
            fallback="",
        ),
        "author": first_string(
            previous.get("author") if previous else None,
            theme.get("author"),
            fallback="",
        ),
        "previewAccent": first_string(
            previous.get("previewAccent") if previous else None,
            vars_obj.get("ambient"),
            vars_obj.get("primary"),
            vars_obj.get("ring"),
            vars_obj.get("sidebar-primary"),
            fallback="#ffffff",
        ),
        "previewBg": first_string(
            previous.get("previewBg") if previous else None,
            vars_obj.get("background"),
            vars_obj.get("card"),
            vars_obj.get("surface"),
            fallback="#000000",
        ),
        "tags": (
            previous["tags"]
            if previous and isinstance(previous.get("tags"), list)
            else default_tags(theme)
        ),
        "downloadUrl": f"https://raw.githubusercontent.com/{repo}/{branch}/{rel_path}",
        "version": first_string(
            previous.get("version") if previous else None,
            fallback="1.0.0",
        ),
    }

    if previous:
        for key, value in previous.items():
            if key not in entry:
                entry[key] = value

    return entry


def build_catalog(
    existing: dict[str, Any],
    discovered: dict[str, tuple[Path, dict[str, Any]]],
    repo: str,
    branch: str,
    touch: bool,
    updated_at: str | None,
) -> dict[str, Any]:
    previous_entries = existing.get("themes", [])
    if not isinstance(previous_entries, list):
        raise ValueError("catalog.json: 'themes' must be an array")

    previous_by_id = {
        entry["id"]: entry
        for entry in previous_entries
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }

    ordered_ids = [
        entry["id"]
        for entry in previous_entries
        if isinstance(entry, dict)
        and isinstance(entry.get("id"), str)
        and entry["id"] in discovered
    ]
    ordered_ids.extend(
        theme_id for theme_id in sorted(discovered) if theme_id not in ordered_ids
    )

    entries = [
        build_entry(
            theme_id,
            discovered[theme_id][0],
            discovered[theme_id][1],
            previous_by_id.get(theme_id),
            repo,
            branch,
        )
        for theme_id in ordered_ids
    ]

    version = existing.get("version", 1)
    existing_compare = {"version": version, "themes": existing.get("themes", [])}
    next_compare = {"version": version, "themes": entries}
    entries_changed = existing_compare != next_compare

    should_update_timestamp = touch or entries_changed or not existing.get("updatedAt")
    next_updated_at = existing.get("updatedAt")
    if should_update_timestamp:
        next_updated_at = updated_at or utc_timestamp()

    return {
        "version": version,
        "updatedAt": next_updated_at,
        "themes": entries,
    }


def json_value(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def format_catalog(catalog: dict[str, Any]) -> str:
    lines = [
        "{",
        f'  "version": {json_value(catalog["version"])},',
        f'  "updatedAt": {json_value(catalog["updatedAt"])},',
        '  "themes": [',
    ]

    themes = catalog["themes"]
    for index, entry in enumerate(themes):
        lines.append("    {")
        fields = [field for field in CATALOG_FIELDS if field in entry]
        fields.extend(sorted(key for key in entry if key not in CATALOG_FIELDS))

        for field_index, field in enumerate(fields):
            comma = "," if field_index < len(fields) - 1 else ""
            lines.append(f'      "{field}": {json_value(entry[field])}{comma}')

        lines.append("    }" + ("," if index < len(themes) - 1 else ""))

    lines.extend(["  ]", "}", ""])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()

    try:
        existing = load_json(args.catalog)
        discovered = discover_themes(args.themes_dir)
        catalog = build_catalog(
            existing,
            discovered,
            args.repo,
            args.branch,
            args.touch,
            args.updated_at,
        )
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    next_text = format_catalog(catalog)
    current_text = args.catalog.read_text(encoding="utf-8")

    if current_text == next_text:
        print("catalog.json is up to date")
        return 0

    if args.check:
        print("catalog.json is stale; run scripts/update-catalog.py", file=sys.stderr)
        return 1

    args.catalog.write_text(next_text, encoding="utf-8")
    print(f"updated catalog.json with {len(catalog['themes'])} themes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
