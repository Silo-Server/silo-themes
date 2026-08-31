# Agent guidance

Read [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before making
changes; they define this repository's format, submission workflow, and
validation requirements.

## Repository structure

- `themes/` contains individual v1 theme files. A theme ID is a kebab-case slug
  and must match the `<id>` portion of its filename before `.json` or
  `.silo-theme.json`.
- `catalog.json` is the generated index consumed by Silo. Generate it with
  `python3 scripts/update-catalog.py` and validate it with
  `python3 scripts/update-catalog.py --check`.
- Theme rendering and CSS sanitization belong in `silo-server`, not this
  catalog repository.

## Writing

Before submitting human-facing prose, make a final readability pass. Lead with
the outcome, use concrete plain language and active voice, and cut filler, stock
framing, repetition, and promotional claims. Preserve the original meaning,
evidence, citations, uncertainty, and terminology. Never rewrite exact quotes,
commands, logs, identifiers, API names, or contractual language. Match the
audience and use formatting only when it improves readability.

## Pull requests

- Never create a pull request unless the developer explicitly asks you to do so.
- Use a Conventional Commit title in plain language. Keep one concern per pull
  request; if the description needs “also,” split it.
- Start the body with the problem, then explain the solution. Include the
  repository-specific evidence required by [CONTRIBUTING.md](CONTRIBUTING.md).
- End with the required AI disclosure, including the exact model and
  harness/tooling that did the work.
- UI changes need before-and-after images; motion or timing changes need a short
  video. Upload that evidence to GitHub. Never commit pull-request-only assets
  such as `.github/pr-assets/`.
- When babysitting a pull request, poll checks and comments newer than the last
  push. Verify every bot finding against the source, fix real findings, and
  dismiss false positives with a written reason. Stay quiet when nothing is new
  and stop when the latest commit is green.
