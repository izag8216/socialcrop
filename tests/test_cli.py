"""Tests for cli.py: CLI integration tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner
from PIL import Image

from socialcrop.cli import main


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def sample_image(tmp_path: Path) -> Path:
    img = Image.new("RGB", (2000, 1500), (100, 150, 200))
    path = tmp_path / "sample.jpg"
    img.save(path, "JPEG")
    return path


class TestVersion:
    def test_version_flag(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "socialcrop" in result.output


class TestResize:
    def test_resize_single_platform(
        self, runner: CliRunner, sample_image: Path, tmp_path: Path
    ) -> None:
        out_dir = tmp_path / "output"
        result = runner.invoke(
            main,
            [
                "resize",
                str(sample_image),
                "-p",
                "instagram-post",
                "-o",
                str(out_dir),
            ],
        )
        assert result.exit_code == 0
        assert "Created" in result.output
        assert out_dir.exists()

    def test_resize_unknown_platform(
        self, runner: CliRunner, sample_image: Path
    ) -> None:
        result = runner.invoke(main, ["resize", str(sample_image), "-p", "nonexistent"])
        assert result.exit_code == 1

    def test_resize_with_anchor(
        self, runner: CliRunner, sample_image: Path, tmp_path: Path
    ) -> None:
        out_dir = tmp_path / "output"
        result = runner.invoke(
            main,
            [
                "resize",
                str(sample_image),
                "-p",
                "twitter-post",
                "-o",
                str(out_dir),
                "--anchor",
                "top",
            ],
        )
        assert result.exit_code == 0


class TestBatch:
    def test_batch_all(
        self, runner: CliRunner, sample_image: Path, tmp_path: Path
    ) -> None:
        out_dir = tmp_path / "output"
        result = runner.invoke(
            main, ["batch", str(sample_image), "-p", "all", "-o", str(out_dir)]
        )
        assert result.exit_code == 0
        assert "Done:" in result.output
        # Should have created files for all platforms
        output_files = list(out_dir.iterdir())
        assert len(output_files) >= 15

    def test_batch_specific_platforms(
        self, runner: CliRunner, sample_image: Path, tmp_path: Path
    ) -> None:
        out_dir = tmp_path / "output"
        result = runner.invoke(
            main,
            [
                "batch",
                str(sample_image),
                "-p",
                "instagram-post",
                "-p",
                "twitter-post",
                "-o",
                str(out_dir),
            ],
        )
        assert result.exit_code == 0
        output_files = list(out_dir.iterdir())
        assert len(output_files) == 2

    def test_batch_no_platform(
        self, runner: CliRunner, sample_image: Path
    ) -> None:
        result = runner.invoke(main, ["batch", str(sample_image)])
        assert result.exit_code == 1


class TestPlatformsCommand:
    def test_list_platforms(self, runner: CliRunner) -> None:
        result = runner.invoke(main, ["platforms"])
        assert result.exit_code == 0
        assert "instagram-post" in result.output
        assert "youtube-thumbnail" in result.output


class TestConfigCommand:
    def test_show_config_missing(self, runner: CliRunner, tmp_path: Path) -> None:
        import socialcrop.config as cfg

        # Redirect config path
        cfg.CONFIG_DIR = tmp_path / ".socialcrop"
        cfg.CONFIG_FILE = tmp_path / ".socialcrop" / "presets.json"

        result = runner.invoke(main, ["config"])
        assert result.exit_code == 0
        assert "No config file found" in result.output or "Example" in result.output
