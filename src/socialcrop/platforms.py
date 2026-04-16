"""Platform dimension database for social media image presets."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformPreset:
    """A single platform's image specification."""

    name: str
    width: int
    height: int
    format: str  # "JPEG", "PNG", "WEBP"
    description: str


PLATFORMS: dict[str, PlatformPreset] = {
    "instagram-post": PlatformPreset(
        "Instagram Post", 1080, 1080, "JPEG", "Square feed post (1:1)"
    ),
    "instagram-portrait": PlatformPreset(
        "Instagram Portrait", 1080, 1350, "JPEG", "Portrait feed post (4:5)"
    ),
    "instagram-story": PlatformPreset(
        "Instagram Story", 1080, 1920, "JPEG", "Story / Reel cover (9:16)"
    ),
    "instagram-landscape": PlatformPreset(
        "Instagram Landscape", 1080, 566, "JPEG", "Landscape feed post (1.91:1)"
    ),
    "twitter-post": PlatformPreset(
        "Twitter/X Post", 1200, 675, "JPEG", "Timeline image (16:9)"
    ),
    "twitter-header": PlatformPreset(
        "Twitter/X Header", 1500, 500, "JPEG", "Profile header (3:1)"
    ),
    "linkedin-post": PlatformPreset(
        "LinkedIn Post", 1200, 627, "JPEG", "Feed post (1.91:1)"
    ),
    "linkedin-banner": PlatformPreset(
        "LinkedIn Banner", 1584, 396, "JPEG", "Profile banner (4:1)"
    ),
    "youtube-thumbnail": PlatformPreset(
        "YouTube Thumbnail", 1280, 720, "JPEG", "Video thumbnail (16:9)"
    ),
    "youtube-banner": PlatformPreset(
        "YouTube Banner", 2560, 1440, "JPEG", "Channel banner (16:9)"
    ),
    "facebook-post": PlatformPreset(
        "Facebook Post", 1200, 630, "JPEG", "Link / feed post (1.91:1)"
    ),
    "facebook-cover": PlatformPreset(
        "Facebook Cover", 820, 312, "JPEG", "Page cover (2.63:1)"
    ),
    "tiktok": PlatformPreset(
        "TikTok", 1080, 1920, "JPEG", "Video cover / ad (9:16)"
    ),
    "pinterest-pin": PlatformPreset(
        "Pinterest Pin", 1000, 1500, "JPEG", "Standard pin (2:3)"
    ),
    "discord-emoji": PlatformPreset(
        "Discord Emoji", 128, 128, "PNG", "Custom emoji (1:1)"
    ),
    "discord-banner": PlatformPreset(
        "Discord Banner", 960, 540, "JPEG", "Server banner (16:9)"
    ),
    "slack-emoji": PlatformPreset(
        "Slack Emoji", 128, 128, "PNG", "Custom emoji (1:1)"
    ),
    "opengraph": PlatformPreset(
        "OpenGraph", 1200, 630, "JPEG", "og:image meta tag (1.91:1)"
    ),
    "twitter-card": PlatformPreset(
        "Twitter Card", 1200, 628, "JPEG", "twitter:image summary_large_image"
    ),
    "github-social": PlatformPreset(
        "GitHub Social Preview", 1280, 640, "JPEG", "Repo social preview (2:1)"
    ),
    "line-rich": PlatformPreset(
        "LINE Rich Menu", 2500, 1686, "JPEG", "Rich menu image"
    ),
    "whatsapp-status": PlatformPreset(
        "WhatsApp Status", 1080, 1920, "JPEG", "Status image (9:16)"
    ),
    "threads-post": PlatformPreset(
        "Threads Post", 1080, 1080, "JPEG", "Feed post (1:1)"
    ),
}


def get_platform(name: str) -> PlatformPreset | None:
    """Look up a platform preset by key (case-insensitive)."""
    return PLATFORMS.get(name.lower())


def list_platforms() -> list[PlatformPreset]:
    """Return all platform presets sorted by name."""
    return sorted(PLATFORMS.values(), key=lambda p: p.name)


def resolve_platform_names(names: list[str]) -> list[PlatformPreset]:
    """Resolve a list of platform name strings to presets.

    The special name "all" returns every platform.
    Unknown names are silently skipped.
    """
    if "all" in [n.lower() for n in names]:
        return list_platforms()
    result = []
    for name in names:
        preset = get_platform(name)
        if preset is not None:
            result.append(preset)
    return result
