"""Tests for crop.py: smart crop algorithms."""

from __future__ import annotations

from PIL import Image
from PIL.ImageDraw import ImageDraw

from socialcrop.crop import CropAnchor, calculate_crop_box, smart_crop


class TestCalculateCropBox:
    """Tests for the crop box calculation."""

    def test_square_to_square(self) -> None:
        # Same aspect ratio: no crop needed, full source used
        box = calculate_crop_box(1000, 1000, 500, 500)
        assert box == (0, 0, 1000, 1000)

    def test_wide_to_square(self) -> None:
        # 2000x1000 -> 500x500: crop width, center
        box = calculate_crop_box(2000, 1000, 500, 500)
        assert box == (500, 0, 1500, 1000)

    def test_tall_to_square(self) -> None:
        # 1000x2000 -> 500x500: crop height, center
        box = calculate_crop_box(1000, 2000, 500, 500)
        assert box == (0, 500, 1000, 1500)

    def test_same_aspect_ratio(self) -> None:
        # 2000x1000 -> 1000x500: same ratio, no aggressive crop needed
        box = calculate_crop_box(2000, 1000, 1000, 500)
        assert box == (0, 0, 2000, 1000)

    def test_anchor_top(self) -> None:
        box = calculate_crop_box(1000, 2000, 500, 500, CropAnchor.TOP)
        assert box == (0, 0, 1000, 1000)

    def test_anchor_bottom(self) -> None:
        box = calculate_crop_box(1000, 2000, 500, 500, CropAnchor.BOTTOM)
        assert box == (0, 1000, 1000, 2000)

    def test_anchor_left(self) -> None:
        box = calculate_crop_box(2000, 1000, 500, 500, CropAnchor.LEFT)
        assert box == (0, 0, 1000, 1000)

    def test_anchor_right(self) -> None:
        box = calculate_crop_box(2000, 1000, 500, 500, CropAnchor.RIGHT)
        assert box == (1000, 0, 2000, 1000)


class TestSmartCrop:
    """Tests for the full smart crop pipeline."""

    def test_resize_to_exact_size(self) -> None:
        img = Image.new("RGB", (2000, 1000), (255, 0, 0))
        result = smart_crop(img, 500, 500)
        assert result.size == (500, 500)

    def test_same_size_returns_copy(self) -> None:
        img = Image.new("RGB", (500, 500), (0, 255, 0))
        result = smart_crop(img, 500, 500)
        assert result.size == (500, 500)
        assert result is not img  # should be a copy

    def test_wide_to_portrait(self) -> None:
        # 2000x1000 -> 1080x1920 (portrait)
        img = Image.new("RGB", (2000, 1000), (0, 0, 255))
        result = smart_crop(img, 1080, 1920)
        assert result.size == (1080, 1920)

    def test_rgba_preserved(self) -> None:
        img = Image.new("RGBA", (1000, 1000), (255, 0, 0, 128))
        result = smart_crop(img, 500, 500)
        assert result.size == (500, 500)
        assert result.mode == "RGBA"

    def test_anchor_affects_output(self) -> None:
        # Create an image with distinct regions
        img = Image.new("RGB", (2000, 1000), (255, 0, 0))
        draw = ImageDraw(img)
        draw.rectangle([0, 0, 500, 500], fill=(255, 255, 255))

        result_top_left = smart_crop(img, 500, 500, CropAnchor.LEFT)

        # top-left anchor should get the white area
        tl_pixel = result_top_left.getpixel((0, 0))
        assert tl_pixel == (255, 255, 255)
