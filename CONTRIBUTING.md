# Contributing to Silo Themes

The [Silo contribution guide](https://github.com/Silo-Server/.github/blob/main/CONTRIBUTING.md)
covers project-wide coordination, focused changes, evidence, AI disclosure, and
pull request expectations. Those requirements apply here; this guide adds the
theme-specific format and submission workflow.

Theme additions and narrow corrections can go straight to a pull request. Open
an [issue](https://github.com/Silo-Server/silo-themes/issues) before changing the
theme file format, catalog schema, sanitization assumptions, or stable selector
contract. Product or renderer changes belong in
[`silo-server`](https://github.com/Silo-Server/silo-server).

## Theme file format

Themes use the `SiloThemeFile` v1 format:

```json
{
  "version": 1,
  "name": "My Theme",
  "description": "Short description of the aesthetic",
  "author": "Your Name",
  "baseTheme": "midnight-cinema",
  "vars": {
    "background": "#1a1b26",
    "foreground": "#c0caf5",
    "primary": "#7aa2f7"
  },
  "customCss": "",
  "createdAt": "2026-01-01T00:00:00Z"
}
```

- `baseTheme` must be one of the built-in themes: `midnight-cinema`, `cinema-light`, `cobalt-studio`, `oxblood-noir`, `evergreen-studio`
- `vars` contains only the CSS tokens you want to override; you do not need to include every token
- `customCss` is optional raw CSS that's sanitized on install (external URLs are stripped)

## Available CSS tokens

These tokens can be set in the `vars` object:

### Surfaces
`background`, `foreground`, `card`, `card-foreground`, `popover`, `popover-foreground`, `surface`, `surface-hover`, `surface-raised`

### Interactive
`primary`, `primary-foreground`, `secondary`, `secondary-foreground`, `muted`, `muted-foreground`, `accent`, `accent-foreground`, `destructive`, `destructive-foreground`, `ambient`

### Sidebar
`sidebar`, `sidebar-foreground`, `sidebar-primary`, `sidebar-primary-foreground`, `sidebar-accent`, `sidebar-accent-foreground`, `sidebar-border`, `sidebar-section-divider`, `sidebar-ring`

### Borders & Focus
`border`, `input`, `ring`

### Shape & Font
`radius` (e.g. `"0.5rem"`), `font-body` (e.g. `"\"Outfit\", sans-serif"`)

## Stable CSS selectors

These class names are available for targeting in `customCss`:

### Layout
| Selector | Element |
|----------|---------|
| `aside` | Sidebar container |
| `#main-content` | Main content area |
| `.mobile-header` | Mobile top navigation bar |
| `.sidebar-logo` | Logo + name wrapper |
| `.sidebar-nav` | Main navigation list |
| `.sidebar-libraries` | Libraries section |
| `.sidebar-personal` | "Your Stuff" section (favorites, watchlist, etc.) |
| `.sidebar-footer` | Bottom area (settings, profile) |

### Pages
| Selector | Element |
|----------|---------|
| `.home-hero` | Home page hero banner carousel |
| `.section-row` | Each content carousel row |
| `.item-detail-hero` | Item detail page backdrop/hero section |
| `.page-shell` | Centered page container (max 1400px) |
| `.page-shell-wide` | Wide page container (max 1520px) |
| `.page-title` | Large page heading |
| `.page-subtitle` | Page description text |

### Player
| Selector | Element |
|----------|---------|
| `.player-container` | Fullscreen video player wrapper |
| `.player-controls` | Control bar overlay |
| `.player-seekbar` | Seek/progress bar |

### Cards & Media
| Selector | Element |
|----------|---------|
| `.media-card` | Poster card (hover: lift + brighten) |
| `.media-card-image` | Poster image container |
| `.progress-bar` | Watch progress bar |
| `[data-watched-indicator]` | Completed checkmark indicator |
| `.play-overlay` | Play button overlay on thumbnails |

### Surfaces
| Selector | Element |
|----------|---------|
| `.surface-panel` | Panel with background + border |
| `.surface-panel-subtle` | Lighter panel variant |
| `.glass` | Frosted glass effect |
| `.glass-subtle` | Lighter glass |
| `.glass-dark` | Darker glass |

### Auth Pages
| Selector | Element |
|----------|---------|
| `.auth-shell` | Full-viewport auth page container |
| `.auth-shell::before` | Gradient backdrop (hide with `display: none`) |
| `.auth-card` | Login/signup card |

### Components
| Selector | Element |
|----------|---------|
| `.hero-gradient` | Bottom-to-top fade on hero images |
| `.hero-vignette` | Left + top gradient on heroes |
| `.ambient-glow` | Colored ambient glow effect |
| `.pill` / `.pill-primary` | Rounded button styles |
| `.tab-bar` / `.tab-item` | Tab navigation |
| `.metadata-badge` | Small inline metadata badge |
| `.carousel-dots` / `.dot` | Carousel navigation dots |

## CSS sanitization

Custom CSS is sanitized on save and install. The following are **blocked**:

- `@import url(...)` — external stylesheet loading
- `url(https://...)` / `url(http://...)` — external resource loading
- `url(//...)` — protocol-relative external URLs

The following are **allowed**:
- `url(data:...)` — inline base64 images
- `url(/path)` — local server paths
- `url(relative/path)` — same-origin relative paths
- `url(#ref)` — SVG fragment references
- All CSS selectors, properties, animations, transforms, etc.

## Submitting a theme

1. Create your theme file in the `themes/` directory as `<id>.json` or `<id>.silo-theme.json`.
2. Run `python3 scripts/update-catalog.py`, review the generated `catalog.json`
   diff, and commit it with the theme. Add custom tags or preview colors there
   when needed.
3. Open a pull request with the theme file and current catalog.

## Validate your change

```sh
python3 scripts/update-catalog.py --check
```

The command checks required basic theme fields and fails if `catalog.json` is
stale. It does not validate every v1 field, CSS token, or `customCss` value.
Review new themes in a running Silo web app when possible and include a
screenshot in the pull request.

## Open the pull request

Use a Conventional Commit title, describe the visual intent and supported base
theme, and paste the validation result. Read the
[AI-assisted contribution policy](https://github.com/Silo-Server/silo-server/blob/main/docs/ai-contributions.md)
and include its disclosure block.
