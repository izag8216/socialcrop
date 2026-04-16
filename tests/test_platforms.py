"""Tests for platforms.py: platform preset database."""

from __future__ import annotations

from socialcrop.platforms import (
    PLATFORMS,
    get_platform,
    list_platforms,
    resolve_platform_names,
)


class TestPlatformDatabase:
    """Tests for the platform dimension database."""

    def test_minimum_15_platforms(self) -> None:
        assert len(PLATFORMS) >= 15

    def test_all_have_required_fields(self) -> None:
        for key, preset in PLATFORMS.items():
            assert preset.name, f"{key} missing name"
            assert preset.width > 0, f"{key} invalid width"
            assert preset.height > 0, f"{key} invalid height"
            assert preset.format in (
                "JPEG",
                "PNG",
                "WEBP",
            ), f"{key} invalid format: {preset.format}"
            assert preset.description, f"{key} missing description"

    def test_get_platform_found(self) -> None:
        result = get_platform("instagram-post")
        assert result is not None
        assert result.width == 1080
        assert result.height == 1080

    def test_get_platform_case_insensitive(self) -> None:
        result = get_platform("Instagram-Post")
        assert result is not None

    def test_get_platform_not_found(self) -> None:
        assert get_platform("nonexistent") is None

    def test_list_platforms_returns_sorted(self) -> None:
        presets = list_platforms()
        names = [p.name for p in presets]
        assert names == sorted(names)

    def test_list_platforms_count(self) -> None:
        assert len(list_platforms()) == len(PLATFORMS)


class TestResolvePlatformNames:
    """Tests for resolving platform name lists."""

    def test_all_returns_everything(self) -> None:
        result = resolve_platform_names(["all"])
        assert len(result) == len(PLATFORMS)

    def test_specific_names(self) -> None:
        result = resolve_platform_names(["instagram-post", "twitter-post"])
        assert len(result) == 2

    def test_unknown_names_skipped(self) -> None:
        result = resolve_platform_names(["instagram-post", "unknown-xyz"])
        assert len(result) == 1

    def test_empty_list(self) -> None:
        assert resolve_platform_names([]) == []

    def test_specific_platform_dimensions(self) -> None:
        """Verify key platform dimensions match spec."""
        ig = get_platform("instagram-post")
        assert ig is not None
        assert ig.width == 1080 and ig.height == 1080

        yt = get_platform("youtube-thumbnail")
        assert yt is not None
        assert yt.width == 1280 and yt.height == 720

        og = get_platform("opengraph")
        assert og is not None
        assert og.width == 1200 and og.height == 630

        gh = get_platform("github-social")
        assert gh is not None
        assert gh.width == 1280 and gh.height == 640
