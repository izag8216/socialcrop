"""Utility helpers: file I/O, naming, validation."""

from __future__ import annotations

from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename component."""
    keepchars = (" ", "-", "_")
    return (
        "".join(c for c in name if c.isalnum() or c in keepchars)
        .strip()
        .replace(" ", "-")
        .lower()
    )


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def collect_images(paths: list[Path]) -> list[Path]:
    """From a list of paths, collect all valid image files.

    - Files are included as-is (after validation)
    - Directories are scanned for image files
    """
    from .core import SUPPORTED_INPUT_EXTS

    images: list[Path] = []
    for p in paths:
        if p.is_file():
            if p.suffix.lower() in SUPPORTED_INPUT_EXTS:
                images.append(p)
        elif p.is_dir():
            for child in sorted(p.iterdir()):
                if child.is_file() and child.suffix.lower() in SUPPORTED_INPUT_EXTS:
                    images.append(child)
    return images
