"""Tests for utils.py: utility helpers."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from socialcrop.utils import collect_images, sanitize_filename


class TestSanitizeFilename:
    def test_basic(self) -> None:
        assert sanitize_filename("Hello World") == "hello-world"

    def test_special_chars_removed(self) -> None:
        assert sanitize_filename("test@#$%123") == "test123"

    def test_hyphens_preserved(self) -> None:
        assert sanitize_filename("my-cool-name") == "my-cool-name"

    def test_underscores_preserved(self) -> None:
        assert sanitize_filename("my_cool_name") == "my_cool_name"


class TestCollectImages:
    def test_collect_from_files(self, tmp_path: Path) -> None:
        jpg = tmp_path / "a.jpg"
        png = tmp_path / "b.png"
        txt = tmp_path / "c.txt"
        Image.new("RGB", (10, 10)).save(jpg, "JPEG")
        Image.new("RGB", (10, 10)).save(png, "PNG")
        txt.write_text("not an image")

        result = collect_images([jpg, png, txt])
        assert len(result) == 2

    def test_collect_from_directory(self, tmp_path: Path) -> None:
        subdir = tmp_path / "images"
        subdir.mkdir()
        for name in ["x.jpg", "y.png", "z.txt"]:
            p = subdir / name
            if name.endswith(".txt"):
                p.write_text("text")
            else:
                Image.new("RGB", (10, 10)).save(p, "JPEG" if name.endswith(".jpg") else "PNG")

        result = collect_images([subdir])
        assert len(result) == 2
