"""Tests for config.py: user preset configuration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from socialcrop.config import (
    UserPreset,
    load_user_presets,
    save_user_presets,
)


@pytest.fixture(autouse=True)
def _tmp_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Redirect config file to tmp_path for all config tests."""
    import socialcrop.config as cfg

    monkeypatch.setattr(cfg, "CONFIG_DIR", tmp_path / ".socialcrop")
    monkeypatch.setattr(cfg, "CONFIG_FILE", tmp_path / ".socialcrop" / "presets.json")


class TestLoadUserPresets:
    def test_no_config_file(self) -> None:
        result = load_user_presets()
        assert result == {}

    def test_valid_config(self, tmp_path: Path) -> None:
        config = {
            "my-blog": {
                "name": "My Blog",
                "width": 800,
                "height": 600,
                "format": "JPEG",
                "description": "Blog header",
            }
        }
        config_path = tmp_path / ".socialcrop" / "presets.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps(config))

        result = load_user_presets()
        assert "my-blog" in result
        assert result["my-blog"].width == 800

    def test_invalid_json(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".socialcrop" / "presets.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text("not valid json{{{")

        result = load_user_presets()
        assert result == {}

    def test_missing_required_fields_skipped(self, tmp_path: Path) -> None:
        config = {"bad": {"name": "No dimensions"}}
        config_path = tmp_path / ".socialcrop" / "presets.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps(config))

        result = load_user_presets()
        assert "bad" not in result

    def test_defaults_applied(self, tmp_path: Path) -> None:
        config = {
            "minimal": {
                "width": 400,
                "height": 300,
            }
        }
        config_path = tmp_path / ".socialcrop" / "presets.json"
        config_path.parent.mkdir(parents=True)
        config_path.write_text(json.dumps(config))

        result = load_user_presets()
        assert "minimal" in result
        assert result["minimal"].format == "JPEG"
        assert result["minimal"].name == "minimal"


class TestSaveUserPresets:
    def test_save_and_load_roundtrip(self) -> None:
        presets = {
            "test": UserPreset("Test", 640, 480, "JPEG", "A test preset"),
        }
        save_user_presets(presets)
        loaded = load_user_presets()
        assert "test" in loaded
        assert loaded["test"].width == 640

    def test_creates_directory(self, tmp_path: Path) -> None:
        config_dir = tmp_path / ".socialcrop"
        assert not config_dir.exists()
        save_user_presets({})
        assert config_dir.exists()
