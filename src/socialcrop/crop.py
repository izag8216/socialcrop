"""Smart crop algorithms for intelligent image resizing."""

from __future__ import annotations

from enum import Enum

from PIL import Image


class CropAnchor(Enum):
    """Anchor position for cropping."""

    CENTER = "center"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


def calculate_crop_box(
    src_w: int, src_h: int, dst_w: int, dst_h: int, anchor: CropAnchor = CropAnchor.CENTER
) -> tuple[int, int, int, int]:
    """Calculate the crop box (left, upper, right, lower) for source image.

    Uses center-weighted logic: crop the excess dimension while keeping
    the anchor point as the focal point.
    """
    src_ratio = src_w / src_h
    dst_ratio = dst_w / dst_h

    if src_ratio > dst_ratio:
        # Source is wider: crop width
        crop_w = int(src_h * dst_ratio)
        crop_h = src_h
    else:
        # Source is taller: crop height
        crop_w = src_w
        crop_h = int(src_w / dst_ratio)

    # Clamp crop dimensions to source bounds
    crop_w = min(crop_w, src_w)
    crop_h = min(crop_h, src_h)

    # Position based on anchor
    if anchor == CropAnchor.CENTER:
        left = (src_w - crop_w) // 2
        top = (src_h - crop_h) // 2
    elif anchor == CropAnchor.TOP:
        left = (src_w - crop_w) // 2
        top = 0
    elif anchor == CropAnchor.BOTTOM:
        left = (src_w - crop_w) // 2
        top = src_h - crop_h
    elif anchor == CropAnchor.LEFT:
        left = 0
        top = (src_h - crop_h) // 2
    elif anchor == CropAnchor.RIGHT:
        left = src_w - crop_w
        top = (src_h - crop_h) // 2
    else:
        left = (src_w - crop_w) // 2
        top = (src_h - crop_h) // 2

    return (left, top, left + crop_w, top + crop_h)


def smart_crop(
    img: Image.Image, target_w: int, target_h: int, anchor: CropAnchor = CropAnchor.CENTER
) -> Image.Image:
    """Crop and resize an image to the target dimensions.

    Steps:
    1. Calculate the optimal crop box from the source image
    2. Crop to match the target aspect ratio
    3. Resize to exact target dimensions
    """
    src_w, src_h = img.size

    # If already the correct size, return as-is
    if src_w == target_w and src_h == target_h:
        return img.copy()

    box = calculate_crop_box(src_w, src_h, target_w, target_h, anchor)
    cropped = img.crop(box)
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
