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
# PHOTO is read as a picture to paint: every picture comes from the image model, and
# a "photograph" of a real person or thing would be a fabrication.
ASKED = re.compile(r"^\s*(?:ILLUSTRATE|PHOTO)\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
PAINTED_AT_MOST = 3
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
    """The scene's illustration, if it has been painted and passed its check. Never
    paints."""
    asked = wanted(on_screen)
    path = _path(folder, asked, look) if asked else None
    return path if path and _passed(path) else None


def _passed(path: Path) -> bool:
    """A picture left by a run stopped while it was painted has no record of passing
    its check, and is never used: it is painted again."""
    from pipeline.storage.documents import read_json_object

    record = path.with_suffix(".json")
    return path.exists() and record.exists() and \
        (read_json_object(record, "illustration") or {}).get("checked") is True


def prompt(asked: str, look: dict[str, Any]) -> str:
    accents = ", ".join((look.get("accents") or [look.get("accent", "")])[:3])
    return (
        f"An illustration for a science explainer video: {asked}. In the style the "
        "description gives -- a flat cartoon, a cute character, a pastel painting, a "
        "collage -- or else a clean, flat educational illustration. Accurate to the "
        "science; one clear subject, whole and centred, filling most of the picture. "
        "Light, pleasant colours that suit each other; never dark or gloomy; appealing, "
        "but never overdone. Never photorealistic: a real person is drawn as a clearly "
        f"illustrated portrait, not a photograph. Plain solid "
        f"{look.get('background', '#ffffff')} background, nothing else behind the "
        f"subject -- it is cut out and laid on the scene's own background. Accent colours "
        f"{accents}. Absolutely no text, letters, numbers, labels or captions anywhere in "
        "the picture. Paint the subject as still, without the glows or changes the scene "
        "animates on top of it.")


class Checked(BaseModel):
    matches: bool = Field(description="Does the picture show the subject asked for, correctly "
                                      "for the science -- the right subject, species and parts "
                                      "that matter -- with no text in it? Small details "
                                      "missing are fine.")
    framed: bool = Field(description="Is the subject whole, centred and large -- not cut off "
                                     "at an edge, not small in an empty picture?")
    clean: bool = Field(description="Is it well drawn -- no deformed anatomy or hands, no "
                                    "garbled parts, no artefacts, not photorealistic?")
    wrong: str = Field("", description="If any is no: what is wrong, and what it should be, "
                                       "in one sentence (\"human hearts; they must be small "
                                       "frog hearts\").")

    @property
    def good(self) -> bool:
        return self.matches and self.framed and self.clean


def check(path: Path, asked: str, narration: str) -> Checked:
    """One look at the painted picture against what was asked and what is said. A
    painting showed human hearts for "two frog hearts" and nothing noticed."""
    from pipeline.llm import VISION_TOKENS, complete_structured_with_images
    from pipeline.scene_review import _jpeg

    return complete_structured_with_images(
        Checked,
        "You check an illustration painted for a science lesson before it is used. Be "
        "strict about the science: the wrong animal, organ, instrument or setup, extra "
        "or missing parts that matter, or any text in the picture, is a no. Do not judge "
        "its background colour or drawing style, which the video sets, nor motion, glows "
        "or changes the description mentions: the scene animates those on top.",
        f"It was asked to show: {asked}\n\nWhat is said while it is on screen:\n"
        f"{narration[:1200]}", [("The illustration", _jpeg(path))], max_tokens=VISION_TOKENS)


def blend(path: Path, background: str) -> None:
    """The painted background cut away, from each corner inward: the subject stands
    on whatever is behind it -- the frame's colour, a gradient, painted art -- with
    no panel round it. (Made the frame's colour, it was a white card on a background.)"""
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
    cut = image.convert("RGBA")
    pixels = cut.load()
    for x in range(width):
        for y in range(height):
            if pixels[x, y][:3] == marker:
                pixels[x, y] = (*colour, 0)
    cut.save(path)


def paint(folder: Path, on_screen: str, look: dict[str, Any],
          state: dict[str, Any], narration: str = "", note: str = "") -> Path | None:
    """Paint the illustration the brief asks for, once: checked, repainted once if
    it is wrong, its background cut away. None when it asks for none, or the image
    model could not paint it (the scene is made without it).

    Each in the style its scene asks for: a video's scenes may differ in style, as
    the explainers it is measured against do -- painted from the first, every
    picture looked drawn by one hand, and alike."""
    from pipeline.llm import draw_image

    asked = wanted(on_screen)
    if not asked:
        return None
    path = _path(folder, asked, look)
    if _passed(path):
        return path
    return _paint_checked(path, asked, look, narration, state, draw_image, note)


def _paint_checked(path: Path, asked: str, look: dict[str, Any], narration: str,
                   state: dict[str, Any], painter, note: str = "") -> Path | None:
    import json

    from pipeline.llm import ModelCallFailed, ModelNotConfigured
    from pipeline.scene_state import add_event

    # A person's note from the storyboard ("show the leg larger") goes with it.
    request = prompt(asked, look) + (f" Also: {note.strip()}" if note.strip() else "")
    # Checked for its subject, its framing and how well it is drawn before it may be
    # used; painted again with what was wrong. One that is never right, or cannot be
    # checked, is not used: a wrong picture misleads more than none.
    verdict = None
    for attempt in range(1, PAINTED_AT_MOST + 1):
        state["calls"]["image"] = state["calls"].get("image", 0) + 1
        try:
            path.write_bytes(painter(request))
        except (ModelCallFailed, ModelNotConfigured, OSError) as failure:
            add_event(state, "note", f"The illustration could not be painted ({failure}); "
                      "the scene is made without it.")
            path.unlink(missing_ok=True)
            return None
        state["calls"]["vision"] += 1
        try:
            verdict = check(path, asked, narration)
        except (ModelCallFailed, ModelNotConfigured) as failure:
            add_event(state, "note", f"The illustration could not be checked ({failure}); "
                      "the scene is made without it.")
            path.unlink(missing_ok=True)
            return None
        if verdict.good:
            break
        if attempt < PAINTED_AT_MOST:
            add_event(state, "note", f"The illustration was not right ({verdict.wrong}); "
                      "painted again.")
            request = prompt(asked, look) + f" Correct this from the last attempt: {verdict.wrong}"
    if not verdict.good:
        add_event(state, "note", f"The illustration for \"{asked}\" was still not right after "
                  f"{PAINTED_AT_MOST} tries ({verdict.wrong}); the scene is made without it.")
        path.unlink(missing_ok=True)
        return None
    blend(path, look.get("background", "#ffffff"))
    path.with_suffix(".json").write_text(json.dumps({"asked": asked, "checked": True},
                                                    ensure_ascii=False), encoding="utf-8")
    add_event(state, "note", f"Painted an illustration: {asked}")
    return path
