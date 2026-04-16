"""Tests for core.py: resize engine."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from socialcrop.core import (
    build_output_path,
    load_image,
    resize_for_platform,
    validate_input,
)
from socialcrop.platforms import PlatformPreset


@pytest.fixture()
def sample_image(tmp_path: Path) -> Path:
    """Create a sample test image."""
    img = Image.new("RGB", (2000, 1500), (100, 150, 200))
    path = tmp_path / "test_image.jpg"
    img.save(path, "JPEG")
    return path


@pytest.fixture()
def sample_png(tmp_path: Path) -> Path:
    """Create a sample PNG with alpha."""
    img = Image.new("RGBA", (1000, 1000), (255, 0, 0, 128))
    path = tmp_path / "test_alpha.png"
    img.save(path, "PNG")
    return path


class TestValidateInput:
    def test_valid_jpg(self, sample_image: Path) -> None:
        result = validate_input(sample_image)
        assert result.exists()

    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            validate_input(tmp_path / "nonexistent.jpg")

    def test_unsupported_format(self, tmp_path: Path) -> None:
        txt = tmp_path / "test.txt"
        txt.write_text("not an image")
        with pytest.raises(ValueError, match="Unsupported format"):
            validate_input(txt)


class TestLoadImage:
    def test_load_rgb(self, sample_image: Path) -> None:
        img = load_image(sample_image)
        assert img.size == (2000, 1500)

    def test_load_rgba(self, sample_png: Path) -> None:
        img = load_image(sample_png)
        assert img.mode == "RGBA"


class TestBuildOutputPath:
    def test_default_output_dir(self) -> None:
        input_path = Path("/tmp/photo.jpg")
        result = build_output_path(input_path, None, "instagram-post", "JPEG")
        assert result == Path("/tmp/photo_instagram-post.jpg")

    def test_custom_output_dir(self, tmp_path: Path) -> None:
        input_path = Path("/tmp/photo.jpg")
        out = tmp_path / "output"
        result = build_output_path(input_path, out, "twitter-post", "JPEG")
        assert result == out / "photo_twitter-post.jpg"

    def test_png_format(self) -> None:
        input_path = Path("/tmp/icon.png")
        result = build_output_path(input_path, None, "discord-emoji", "PNG")
        assert result.suffix == ".png"


class TestResizeForPlatform:
    def test_resize_jpeg(self, sample_image: Path, tmp_path: Path) -> None:
        preset = PlatformPreset("Test", 1080, 1080, "JPEG", "Test preset")
        out = resize_for_platform(sample_image, preset, "test", tmp_path)
        assert out.exists()
        img = Image.open(out)
        assert img.size == (1080, 1080)
        assert out.suffix == ".jpg"

    def test_resize_png(self, sample_png: Path, tmp_path: Path) -> None:
        preset = PlatformPreset("Test Emoji", 128, 128, "PNG", "Test")
        out = resize_for_platform(sample_png, preset, "test-emoji", tmp_path)
        assert out.exists()
        img = Image.open(out)
        assert img.size == (128, 128)

    def test_rgba_to_jpeg_conversion(self, sample_png: Path, tmp_path: Path) -> None:
        preset = PlatformPreset("Test", 500, 500, "JPEG", "Test")
        out = resize_for_platform(sample_png, preset, "test-jpg", tmp_path)
        img = Image.open(out)
        assert img.mode == "RGB"

    def test_output_dir_created(self, sample_image: Path, tmp_path: Path) -> None:
        out_dir = tmp_path / "nested" / "output"
        preset = PlatformPreset("Test", 500, 500, "JPEG", "Test")
        out = resize_for_platform(sample_image, preset, "test", out_dir)
        assert out.exists()
