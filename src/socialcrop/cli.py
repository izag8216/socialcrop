"""CLI entry point for socialcrop."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import CONFIG_FILE, load_user_presets
from .core import resize_for_platform
from .crop import CropAnchor
from .platforms import PLATFORMS, list_platforms

console = Console()


def _find_platform_key(name: str) -> str | None:
    """Case-insensitive platform key lookup."""
    lower = name.lower()
    for key in PLATFORMS:
        if key == lower:
            return key
    return None


@click.group()
@click.version_option(version=__version__, prog_name="socialcrop")
def main() -> None:
    """socialcrop - Social media image resizer CLI.

    Resize images to exact dimensions for 15+ social media platforms.
    Smart crop, batch export, zero API.
    """


@main.command()
@click.argument("image", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--platform", "-p", required=True, help="Platform preset name (e.g. instagram-post)"
)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), default=None,
    help="Output directory",
)
@click.option(
    "--anchor",
    type=click.Choice([a.value for a in CropAnchor]),
    default="center",
    help="Crop anchor point",
)
def resize(image: Path, platform: str, output: Path | None, anchor: str) -> None:
    """Resize a single image for a specific platform."""
    # Check built-in platforms first, then user presets
    key = _find_platform_key(platform)
    if key is not None:
        preset = PLATFORMS[key]
    else:
        user_presets = load_user_presets()
        lower = platform.lower()
        if lower not in user_presets:
            console.print(f"[red]Unknown platform:[/red] {platform}")
            console.print(
                "Run [bold]socialcrop platforms[/bold] to see available presets."
            )
            raise SystemExit(1)
        preset = user_presets[lower].to_platform_preset()
        key = lower

    crop_anchor = CropAnchor(anchor)
    out_path = resize_for_platform(image, preset, key, output, crop_anchor)
    console.print(f"[green]Created:[/green] {out_path} ({preset.width}x{preset.height})")


@main.command()
@click.argument("image", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--platform",
    "-p",
    multiple=True,
    help="Platform name(s). Use 'all' for every platform.",
)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), default=None,
    help="Output directory",
)
@click.option(
    "--anchor",
    type=click.Choice([a.value for a in CropAnchor]),
    default="center",
    help="Crop anchor point",
)
def batch(image: Path, platform: tuple[str, ...], output: Path | None, anchor: str) -> None:
    """Batch resize an image for multiple platforms."""
    if not platform:
        console.print(
            "[red]Specify at least one platform with "
            "--platform, or use --platform all[/red]"
        )
        raise SystemExit(1)

    # Merge built-in + user presets
    user_presets = load_user_presets()
    all_keys = list(PLATFORMS.keys()) + list(user_presets.keys())

    if "all" in [p.lower() for p in platform]:
        selected_keys = all_keys
    else:
        selected_keys = [p.lower() for p in platform]

    crop_anchor = CropAnchor(anchor)
    success = 0
    errors = 0

    for key in selected_keys:
        if key in PLATFORMS:
            preset = PLATFORMS[key]
        elif key in user_presets:
            preset = user_presets[key].to_platform_preset()
        else:
            console.print(f"[yellow]Skipping unknown platform:[/yellow] {key}")
            errors += 1
            continue

        try:
            out_path = resize_for_platform(image, preset, key, output, crop_anchor)
            console.print(
                f"  [green]✓[/green] {key}: {out_path} "
                f"({preset.width}x{preset.height})"
            )
            success += 1
        except Exception as exc:
            console.print(f"  [red]✗[/red] {key}: {exc}")
            errors += 1

    console.print(f"\n[bold]Done:[/bold] {success} created, {errors} errors")


@main.command("platforms")
def list_platforms_cmd() -> None:
    """List all available platform presets."""
    table = Table(title="Platform Presets", show_lines=True)
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Size", style="green")
    table.add_column("Format", style="yellow")
    table.add_column("Description", style="dim")

    for preset in list_platforms():
        key = next(k for k, v in PLATFORMS.items() if v == preset)
        dims = f"{preset.width}x{preset.height}"
        table.add_row(key, preset.name, dims, preset.format, preset.description)

    # User presets
    user_presets = load_user_presets()
    for key, up in user_presets.items():
        dims = f"{up.width}x{up.height}"
        table.add_row(key, up.name, dims, up.format, f"{up.description} (custom)")

    console.print(table)
    console.print(f"\n[dim]Config file: {CONFIG_FILE}[/dim]")


@main.command()
def config() -> None:
    """Show configuration path and current custom presets."""
    if CONFIG_FILE.exists():
        console.print(f"[bold]Config file:[/bold] {CONFIG_FILE}")
        console.print(CONFIG_FILE.read_text(encoding="utf-8"))
    else:
        console.print(
            f"[dim]No config file found. "
            f"Create {CONFIG_FILE} to add custom presets.[/dim]"
        )
        console.print("\n[bold]Example presets.json:[/bold]")
        console.print('''{
  "my-custom": {
    "name": "My Custom Size",
    "width": 800,
    "height": 600,
    "format": "JPEG",
    "description": "Custom preset for my blog"
  }
}''')


if __name__ == "__main__":
    main()
