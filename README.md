<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:E67E22,100:E74C3C&height=220&section=header&text=socialcrop&fontSize=70&fontColor=FDF6E3&fontAlignY=42&desc=Social%20Media%20Image%20Resizer%20CLI&descSize=18&descAlignY=62" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/tests-59-brightgreen" alt="Tests" />
  <img src="https://img.shields.io/badge/coverage-92%25-green" alt="Coverage" />
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License" />
  <img src="https://img.shields.io/badge/linter-ruff-purple" alt="Ruff" />
  <img src="https://img.shields.io/badge/API-zero-orange" alt="Zero API" />
</p>

**socialcrop** is a zero-API CLI tool that resizes images to exact dimensions for 15+ social media platforms. Smart crop, batch export, custom presets -- all offline, all local.

## Features

- **15+ platform presets** -- Instagram, Twitter/X, LinkedIn, YouTube, Facebook, TikTok, Pinterest, Discord, Slack, OpenGraph, Twitter Card, GitHub Social Preview, LINE, WhatsApp, Threads
- **Smart crop** -- Center-weighted crop algorithm with configurable anchor points
- **Batch export** -- Generate all sizes from a single image with `--platform all`
- **Custom presets** -- Add your own sizes via `~/.socialcrop/presets.json`
- **Zero API** -- No cloud services, no accounts, no network required
- **Format aware** -- Outputs JPEG/PNG/WEBP per platform specification

## Install

```bash
pip install socialcrop
```

## Quick Start

```bash
# Resize for a single platform
socialcrop resize photo.jpg --platform instagram-post

# Batch export for all platforms
socialcrop batch photo.jpg --platform all --output ./resized/

# List available platforms
socialcrop platforms

# View/set custom presets
socialcrop config
```

## Commands

### `resize` -- Single platform resize

```bash
socialcrop resize <image> --platform <name> [--output <dir>] [--anchor <position>]
```

Options:
- `--platform, -p` -- Platform preset name (required)
- `--output, -o` -- Output directory (default: same as input)
- `--anchor` -- Crop anchor: `center` (default), `top`, `bottom`, `left`, `right`

### `batch` -- Multi-platform export

```bash
socialcrop batch <image> --platform <name> [--platform <name> ...] [--output <dir>]
```

Use `--platform all` to export for every supported platform at once.

### `platforms` -- List presets

```bash
socialcrop platforms
```

Shows a formatted table of all built-in and custom presets.

### `config` -- Manage custom presets

```bash
socialcrop config
```

Custom presets are stored in `~/.socialcrop/presets.json`:

```json
{
  "my-blog-hero": {
    "name": "Blog Hero Image",
    "width": 1600,
    "height": 900,
    "format": "JPEG",
    "description": "Full-width blog hero"
  }
}
```

## Supported Platforms

| Platform | Key | Size | Format |
|----------|-----|------|--------|
| Instagram Post | `instagram-post` | 1080x1080 | JPEG |
| Instagram Portrait | `instagram-portrait` | 1080x1350 | JPEG |
| Instagram Story | `instagram-story` | 1080x1920 | JPEG |
| Instagram Landscape | `instagram-landscape` | 1080x566 | JPEG |
| Twitter/X Post | `twitter-post` | 1200x675 | JPEG |
| Twitter/X Header | `twitter-header` | 1500x500 | JPEG |
| LinkedIn Post | `linkedin-post` | 1200x627 | JPEG |
| LinkedIn Banner | `linkedin-banner` | 1584x396 | JPEG |
| YouTube Thumbnail | `youtube-thumbnail` | 1280x720 | JPEG |
| YouTube Banner | `youtube-banner` | 2560x1440 | JPEG |
| Facebook Post | `facebook-post` | 1200x630 | JPEG |
| Facebook Cover | `facebook-cover` | 820x312 | JPEG |
| TikTok | `tiktok` | 1080x1920 | JPEG |
| Pinterest Pin | `pinterest-pin` | 1000x1500 | JPEG |
| Discord Emoji | `discord-emoji` | 128x128 | PNG |
| Discord Banner | `discord-banner` | 960x540 | JPEG |
| Slack Emoji | `slack-emoji` | 128x128 | PNG |
| OpenGraph | `opengraph` | 1200x630 | JPEG |
| Twitter Card | `twitter-card` | 1200x628 | JPEG |
| GitHub Social Preview | `github-social` | 1280x640 | JPEG |
| LINE Rich Menu | `line-rich` | 2500x1686 | JPEG |
| WhatsApp Status | `whatsapp-status` | 1080x1920 | JPEG |
| Threads Post | `threads-post` | 1080x1080 | JPEG |

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=socialcrop

# Lint
ruff check src/ tests/
```

## License

MIT
