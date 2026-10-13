"""A scene's illustration: a picture painted by the image model, when the script
asks for one.

Drawn from code, a frog's leg came out as two ellipses. Where a scene names a
thing no slide picture shows, the script's brief says so on an `ILLUSTRATE:`
line, and the image model paints it once -- no text in it (the scene puts its
own labels on), on the scene's background, in its colours. Not every scene has
one: the script decides, scene by scene, and a scene the slides already picture
needs none.

Painted before the scene's first round and kept beside its program, named for
what was asked and the look it was painted in, so the rounds after it -- and a
scene made again -- use the same picture instead of paying for another.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

BACKGROUND_TOLERANCE = 14     # per channel: a painted "white" is #fafafa, not #ffffff
ASKED = re.compile(r"^\s*ILLUSTRATE\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
LONGEST_REQUEST = 600


def wanted(on_screen: str) -> str:
    """What the brief asks to have painted, or empty when it asks for nothing."""
    found = ASKED.search(on_screen or "")
    text = found.group(1).strip() if found else ""
    return "" if text.lower() in ("", "none", "-") else text[:LONGEST_REQUEST]


def _path(folder: Path, asked: str, look: dict[str, Any]) -> Path:
    key = hashlib.sha256(f"{asked}|{look.get('background', '')}".encode()).hexdigest()[:12]
    return folder / f"illustration-{key}.png"


def kept(folder: Path, on_screen: str, look: dict[str, Any]) -> Path | None:
    """The scene's illustration, if it has been painted. Never paints."""
    asked = wanted(on_screen)
    path = _path(folder, asked, look) if asked else None
    return path if path and path.exists() else None


def prompt(asked: str, look: dict[str, Any]) -> str:
    accents = ", ".join((look.get("accents") or [look.get("accent", "")])[:3])
    return (
        f"A clean, flat educational illustration for a science explainer video: {asked}. "
        "Accurate to the science; simple shapes, soft shading, one clear subject filling "
        f"most of the picture. Plain solid {look.get('background', '#ffffff')} background, "
        f"so it sits on a video frame of that colour. Accent colours {accents}. "
        "Absolutely no text, letters, numbers, labels or captions anywhere in the picture.")


class Checked(BaseModel):
    matches: bool = Field(description="Does the picture show what was asked, correctly for "
                                      "the science -- the right subject, the right species "
                                      "and parts -- with no text in it?")
    wrong: str = Field("", description="If not: what is wrong, and what it should be, in "
                                       "one sentence (\"human hearts; they must be small "
                                       "frog hearts\").")


def check(path: Path, asked: str, narration: str) -> Checked:
    """One look at the painted picture against what was asked and what is said. A
    painting showed human hearts for "two frog hearts" and nothing noticed."""
    from pipeline.llm import complete_structured_with_images
    from pipeline.scene_review import _jpeg

    return complete_structured_with_images(
        Checked,
        "You check an illustration painted for a science lesson before it is used. Be "
        "strict about the science: the wrong animal, organ, instrument or setup, extra "
        "or missing parts that matter, or any text in the picture, is a no.",
        f"It was asked to show: {asked}\n\nWhat is said while it is on screen:\n"
        f"{narration[:1200]}", [("The illustration", _jpeg(path))], max_tokens=1500)


def blend(path: Path, background: str) -> None:
    """The painted background made the frame's own colour, from each corner inward,
    so the picture has no visible panel edge on the frame."""
    from PIL import Image, ImageDraw

    colour = tuple(int(background.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    with Image.open(path) as opened:
        image = opened.convert("RGB")
    width, height = image.size
    # Filled with a marker first: PIL leaves a region alone when the new colour is
    # already within the tolerance of it -- exactly the case of #fafafa on white.
    marker = (1, 254, 3)
    for corner in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)):
        corner_colour = image.getpixel(corner)
        if corner_colour != marker and sum(
                abs(a - b) for a, b in zip(corner_colour, colour, strict=False)) \
                <= BACKGROUND_TOLERANCE * 3:
            ImageDraw.floodfill(image, corner, marker, thresh=BACKGROUND_TOLERANCE)
    pixels = image.load()
    for x in range(width):
        for y in range(height):
            if pixels[x, y] == marker:
                pixels[x, y] = colour
    image.save(path)


def paint(folder: Path, on_screen: str, look: dict[str, Any],
          state: dict[str, Any], narration: str = "") -> Path | None:
    """Paint the illustration the brief asks for, once: checked, repainted once if
    it is wrong, its background made the frame's. None when it asks for none, or the
    image model could not paint it (the scene is made without it)."""
    import json

    from pipeline.llm import ModelCallFailed, ModelNotConfigured, draw_image
    from pipeline.scene_state import add_event

    asked = wanted(on_screen)
    if not asked:
        return None
    path = _path(folder, asked, look)
    if path.exists():
        return path
    request, verdict = prompt(asked, look), None
    for attempt in (1, 2):
        state["calls"]["image"] = state["calls"].get("image", 0) + 1
        try:
            path.write_bytes(draw_image(request))
        except (ModelCallFailed, ModelNotConfigured, OSError) as failure:
            add_event(state, "note", f"The illustration could not be painted ({failure}); "
                      "the scene is made without it.")
            path.unlink(missing_ok=True)
            return None
        state["calls"]["vision"] += 1
        try:
            verdict = check(path, asked, narration)
        except (ModelCallFailed, ModelNotConfigured):
            break                         # not checked: used as painted, and said so
        if verdict.matches or attempt == 2:
            break
        add_event(state, "note", f"The illustration was wrong ({verdict.wrong}); painted again.")
        request = prompt(asked, look) + f" Correct this from the last attempt: {verdict.wrong}"
    blend(path, look.get("background", "#ffffff"))
    path.with_suffix(".json").write_text(json.dumps({
        "asked": asked, "checked": verdict is not None,
        "matches": verdict.matches if verdict else None,
        "wrong": verdict.wrong if verdict else ""}, ensure_ascii=False), encoding="utf-8")
    add_event(state, "note", f"Painted an illustration: {asked}" + (
        "" if verdict is None or verdict.matches else f" (still not right: {verdict.wrong})"))
    return path
