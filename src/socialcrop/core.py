"""Core resize engine: load, process, save images."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from .crop import CropAnchor, smart_crop
from .platforms import PlatformPreset

# Supported input formats (for validation)
SUPPORTED_INPUT_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}

# Format -> Pillow save format string
FORMAT_MAP = {
    "JPEG": "JPEG",
    "PNG": "PNG",
    "WEBP": "WEBP",
}

# Default save quality per format
QUALITY_MAP: dict[str, int] = {
    "JPEG": 92,
    "PNG": 0,  # PNG is lossless; ignored
    "WEBP": 85,
}


def validate_input(path: Path) -> Path:
    """Validate that the input path is a supported image file.

    Returns the resolved absolute path.
    Raises FileNotFoundError or ValueError on invalid input.
    """
    resolved = path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Image not found: {resolved}")
    if resolved.suffix.lower() not in SUPPORTED_INPUT_EXTS:
        supported = ", ".join(sorted(SUPPORTED_INPUT_EXTS))
        raise ValueError(f"Unsupported format: {resolved.suffix}. Supported: {supported}")
    return resolved


def load_image(path: Path) -> Image.Image:
    """Load an image, converting to RGB if needed (for JPEG output)."""
    img = Image.open(path)
    return img


def build_output_path(
    input_path: Path, output_dir: Path | None, platform_key: str, fmt: str
) -> Path:
    """Construct the output file path.

    Pattern: {stem}_{platform_key}.{ext}
    """
    ext = "jpg" if fmt == "JPEG" else ("webp" if fmt == "WEBP" else "png")
    out_name = f"{input_path.stem}_{platform_key}.{ext}"
    dest = output_dir if output_dir else input_path.parent
    return dest / out_name


def resize_for_platform(
    input_path: Path,
    preset: PlatformPreset,
    platform_key: str,
    output_dir: Path | None = None,
    anchor: CropAnchor = CropAnchor.CENTER,
) -> Path:
    """Full pipeline: load -> smart crop -> resize -> save.

    Returns the path to the saved output file.
    """
    resolved = validate_input(input_path)
    img = load_image(resolved)

    # Convert to RGB if saving as JPEG and image has alpha
    if preset.format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")

    result = smart_crop(img, preset.width, preset.height, anchor)

    out_path = build_output_path(resolved, output_dir, platform_key, preset.format)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    save_kwargs: dict = {}
    if preset.format == "JPEG":
        save_kwargs["quality"] = QUALITY_MAP["JPEG"]
        save_kwargs["optimize"] = True
    elif preset.format == "WEBP":
        save_kwargs["quality"] = QUALITY_MAP["WEBP"]

    result.save(out_path, format=FORMAT_MAP[preset.format], **save_kwargs)
    return out_path
