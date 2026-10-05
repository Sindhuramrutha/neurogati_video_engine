"""The finished logo or watermark: sized, rounded, faded and shadowed, once.

ffmpeg could do each of these in its filter graph, and then the page would have
to imitate ffmpeg in CSS and the two would differ by a pixel here and a shade
there. Instead the overlay is drawn once, with Pillow, into a PNG; ffmpeg only
lays that PNG on the frame at a place and a time, and the page shows the very
same PNG. What is previewed is what is rendered.

The PNG is named from everything that decides its pixels, so the same file and
placement always give the same overlay, and a changed slider a new one.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from pipeline.brand_kit import FRAME_HEIGHT_PX, FRAME_WIDTH_PX, BrandFile, Placement

# The shadow needs room around the picture: this much of its shorter side.
SHADOW_ROOM = 0.18
SHADOW_DARKNESS = 0.6


def overlay_directory(project_root: Path) -> Path:
    return project_root / "assets" / "brand" / "prepared"


def _geometry(file: BrandFile, place: Placement) -> tuple[int, int, int]:
    """The picture's width and height on the frame, and the room its shadow needs."""
    width = max(2, round(FRAME_WIDTH_PX * place.width))
    height = max(2, round(width * (file.height or 1) / (file.width or 1)))
    room = round(min(width, height) * SHADOW_ROOM) if place.shadow > 0 else 0
    return width, height, room


def overlay_box(file: BrandFile, place: Placement) -> dict[str, float]:
    """Where the overlay PNG goes on the frame: its top-left corner and size in
    pixels, and the same as shares of the frame for the page."""
    width, height, room = _geometry(file, place)
    left = round(place.x * FRAME_WIDTH_PX - width / 2) - room
    top = round(place.y * FRAME_HEIGHT_PX - height / 2) - room
    full_width, full_height = width + 2 * room, height + 2 * room
    return {
        "left_px": left, "top_px": top, "width_px": full_width, "height_px": full_height,
        "left": left / FRAME_WIDTH_PX, "top": top / FRAME_HEIGHT_PX,
        "width": full_width / FRAME_WIDTH_PX, "height": full_height / FRAME_HEIGHT_PX,
        # The picture itself, without the shadow's room: what the page outlines.
        "inner_width": width / FRAME_WIDTH_PX, "inner_height": height / FRAME_HEIGHT_PX,
    }


def prepare_overlay(project_root: Path, file: BrandFile, place: Placement) -> Path:
    """Draw the overlay, or return the one already drawn for these settings."""
    from PIL import Image, ImageChops, ImageDraw, ImageFilter

    look = [file.path, place.width, place.opacity, place.radius, place.shadow]
    name = hashlib.sha256(json.dumps(look).encode("utf-8")).hexdigest()[:16] + ".png"
    target = overlay_directory(project_root) / name
    if target.exists():
        return target

    width, height, room = _geometry(file, place)
    with Image.open(project_root / file.path) as opened:
        picture = opened.convert("RGBA").resize((width, height), Image.LANCZOS)

    alpha = picture.getchannel("A")
    if place.radius > 0:
        corners = Image.new("L", (width, height), 0)
        ImageDraw.Draw(corners).rounded_rectangle(
            [0, 0, width - 1, height - 1], radius=round(min(width, height) * place.radius),
            fill=255)
        alpha = ImageChops.multiply(alpha, corners)
    if place.opacity < 1:
        alpha = alpha.point(lambda value: round(value * place.opacity))
    picture.putalpha(alpha)

    canvas = Image.new("RGBA", (width + 2 * room, height + 2 * room), (0, 0, 0, 0))
    if room:
        shade = alpha.point(lambda value: round(value * place.shadow * SHADOW_DARKNESS))
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 255), (room, room + room // 4), shade)
        canvas = shadow.filter(ImageFilter.GaussianBlur(room / 3))
    canvas.alpha_composite(picture, (room, room))

    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target)
    return target


def overlay_views(project, kit) -> dict[str, Any]:
    """For the page: each overlay's file name and where it sits on the frame."""
    views: dict[str, Any] = {}
    for slot, place in (("watermark", kit.watermark_place), ("logo", kit.logo_place)):
        file = getattr(kit, slot)
        if file is None:
            continue
        views[slot] = overlay_box(file, place) | {
            "file": prepare_overlay(project.root, file, place).name}
    return views
