# Silo Themes

Community theme catalog for Silo.

Theme files live in `themes/`; `catalog.json` is the generated index consumed by
Silo. Each theme extends a built-in base theme with CSS token overrides and may
include sanitized custom CSS.

## Browse and submit themes

- Browse the source files in [`themes/`](themes/).
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for the v1 file format, supported CSS
  tokens, stable selectors, sanitization rules, and submission workflow.
- Run `python3 scripts/update-catalog.py --check` before opening a pull request.

## License

`silo-themes` is licensed under the MIT License. See [LICENSE](LICENSE).
