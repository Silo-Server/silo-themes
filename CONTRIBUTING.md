# Contributing Themes

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

- `baseTheme` must be one of the built-in themes: `midnight-cinema`, `cinema-light`, `cobalt-studio`, `oxblood-noir`, `ember-slate`, `evergreen-studio`, `verdant-ink`, `catppuccin`, `gruvbox`, `void-space`, `charcoal-studio`, `graphite-pro`, `obsidian-depth`
- `vars` contains only the CSS tokens you want to override (you don't need all 33)
- `customCss` is optional raw CSS that's sanitized on install (external URLs are stripped)

## Available CSS tokens

These tokens can be set in the `vars` object:

### Surfaces
`background`, `foreground`, `card`, `card-foreground`, `popover`, `popover-foreground`, `surface`, `surface-hover`, `surface-raised`

### Interactive
`primary`, `primary-foreground`, `secondary`, `secondary-foreground`, `muted`, `muted-foreground`, `accent`, `accent-foreground`, `destructive`, `destructive-foreground`, `ambient`

### Sidebar
`sidebar`, `sidebar-foreground`, `sidebar-primary`, `sidebar-primary-foreground`, `sidebar-accent`, `sidebar-accent-foreground`, `sidebar-border`, `sidebar-ring`

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
| `.sidebar-logo-icon` | The logo icon |
| `.sidebar-logo-text` | The server name text |
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
| `.watched-badge` | Completed checkmark badge |
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
- `url(#ref)` — SVG fragment references
- All CSS selectors, properties, animations, transforms, etc.

## Submitting a theme

1. Create your theme file in the `themes/` directory as `<id>.json` or `<id>.silo-theme.json`
2. Open a pull request — catalog automation opens a follow-up PR after merge if `catalog.json` needs changes
3. Optionally edit `catalog.json` in the same pull request if you want custom tags or preview colors
