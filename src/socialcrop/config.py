"""Configuration loading from ~/.socialcrop/presets.json."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .platforms import PlatformPreset

CONFIG_DIR = Path.home() / ".socialcrop"
CONFIG_FILE = CONFIG_DIR / "presets.json"


@dataclass(frozen=True)
class UserPreset:
    """A user-defined custom platform preset."""

    name: str
    width: int
    height: int
    format: str
    description: str

    def to_platform_preset(self) -> PlatformPreset:
        return PlatformPreset(
            name=self.name,
            width=self.width,
            height=self.height,
            format=self.format,
            description=self.description,
        )


def load_user_presets() -> dict[str, UserPreset]:
    """Load user-defined presets from config file.

    Returns an empty dict if the file does not exist or is invalid.
    """
    if not CONFIG_FILE.exists():
        return {}
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    presets: dict[str, UserPreset] = {}
    for key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        try:
            presets[key.lower()] = UserPreset(
                name=entry.get("name", key),
                width=int(entry["width"]),
                height=int(entry["height"]),
                format=entry.get("format", "JPEG"),
                description=entry.get("description", ""),
            )
        except (KeyError, ValueError, TypeError):
            continue
    return presets


def ensure_config_dir() -> Path:
    """Create config directory if it does not exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def save_user_presets(presets: dict[str, UserPreset]) -> None:
    """Write user presets to the config file."""
    ensure_config_dir()
    data = {}
    for key, preset in presets.items():
        data[key] = {
            "name": preset.name,
            "width": preset.width,
            "height": preset.height,
            "format": preset.format,
            "description": preset.description,
        }
    CONFIG_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
