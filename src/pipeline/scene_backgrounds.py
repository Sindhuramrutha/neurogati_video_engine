"""A scene's background: painted art, or a polished gradient -- never dark.

A scene used to sit on one flat white frame, scene after scene. Now the scene's maker
chooses its background in its answer ("background"): about seven scenes in ten get
art painted for them -- from a simple wash to a rich scene like a pastel botanical
scene, always filling the screen edge to edge -- and the rest a gradient, which may be
split into coloured sections. A
background is light and pleasant, its colours complementary, its centre calm for
what the scene shows; never a dark or gloomy frame, and never busy or overdone.
Darkness is measured, not trusted: a dark painting is painted again, lighter, or
the scene gets a light gradient; a dark gradient colour is lightened.

Kept in the scene's folder (`background.json`, and the painting beside it), with
whether it is on: a person can switch it off and back on from the scene's page, and
the scene is drawn again. The brief carries it to the program, where the kit lays
it under everything, kept across the scene's shots.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

BACKGROUND_FILE = "background.json"
IMAGE_SHARE = 0.7                 # of a video's scenes, roughly: the rest gradients
LIGHTEST_DARK = 150               # mean grey level a background may not fall under
LIGHTEST_CENTRE = 165             # the middle, where words and pictures go
LEAST_GRADIENT_LIGHTNESS = 0.72   # each gradient colour at least this light (0-1)
SPLITS = ("none", "left", "right", "top", "bottom", "diagonal")
FLATTEST_EDGE = 15                # grey levels: an outer edge flatter than this is a frame


def read(folder: Path) -> dict[str, Any]:
    try:
        found = json.loads((folder / BACKGROUND_FILE).read_text(encoding="utf-8"))
        return found if isinstance(found, dict) else {}
    except (OSError, ValueError):
        return {}


def for_brief(folder: Path | None) -> dict[str, Any] | None:
    """What the program draws under the scene: None when there is none, or it is off."""
    if folder is None:
        return None
    found = read(folder)
    if not found.get("on", True) or found.get("kind") not in ("image", "gradient"):
        return None
    if found["kind"] == "image":
        path = folder / str(found.get("file", ""))
        return {"kind": "image", "path": str(path)} if path.is_file() else None
    return {"kind": "gradient", "colours": found.get("colours") or [],
            "split": found.get("split", "none"), "panel": found.get("panel", "")}


def switch(folder: Path, on: bool) -> dict[str, Any]:
    from pipeline.storage.documents import write_text_atomically

    found = read(folder)
    if not found:
        return found
    found["on"] = bool(on)
    write_text_atomically(folder / BACKGROUND_FILE, json.dumps(found, ensure_ascii=False))
    return found


def tally(scenes: Path) -> str:
    """How the video's backgrounds stand so far, for the next scene's maker."""
    kinds = [read(folder).get("kind") for folder in scenes.iterdir() if folder.is_dir()] \
        if scenes.is_dir() else []
    images, gradients = kinds.count("image"), kinds.count("gradient")
    return (f"Backgrounds so far in this video: {images} painted, {gradients} gradients "
            f"(aim for about {round(IMAGE_SHARE * 100)}% painted, the rest gradients).")


def choose(project, visual, folder: Path, spec: dict[str, Any], brief: dict[str, Any],
           state: dict[str, Any]) -> dict[str, Any] | None:
    """Make the background the answer asks for, if it is not made already, and return
    the brief written again with it; None when nothing changed."""
    from pipeline.scene_lab import write_brief
    from pipeline.scene_state import add_event
    from pipeline.storage.documents import write_text_atomically

    asked = spec.get("background")
    if not isinstance(asked, dict) or asked.get("kind") not in ("image", "gradient"):
        return None
    before = read(folder)
    made = _gradient(asked) if asked["kind"] == "gradient" else \
        _painted(folder, str(asked.get("describe") or ""), before, state)
    if made is None or {k: made.get(k) for k in made} == {k: before.get(k) for k in made}:
        return None
    made["on"] = before.get("on", True)
    write_text_atomically(folder / BACKGROUND_FILE, json.dumps(made, ensure_ascii=False))
    add_event(state, "note", "Background: " + (
        f"painted -- {made.get('describe', '')}" if made["kind"] == "image"
        else f"a gradient, {', '.join(made['colours'])}"))
    return write_brief(project, visual)


def _gradient(asked: dict[str, Any]) -> dict[str, Any]:
    colours = [lightened(c) for c in (asked.get("colours") or [])[:3] if _is_colour(c)]
    colours = colours or ["#fdf6ec", "#f3e8ff"]
    split = asked.get("split") if asked.get("split") in SPLITS else "none"
    panel = lightened(asked["panel"]) if _is_colour(asked.get("panel")) else ""
    return {"kind": "gradient", "colours": colours, "split": split, "panel": panel}


def _painted(folder: Path, describe: str, before: dict[str, Any],
             state: dict[str, Any]) -> dict[str, Any] | None:
    """The painted background, made once per description; a dark one painted again,
    lighter, and if it is still dark, a light gradient instead."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured
    from pipeline.scene_state import add_event

    describe = describe.strip()[:400]
    if not describe:
        return None
    name = f"background-{hashlib.sha256(describe.encode()).hexdigest()[:12]}.png"
    if before.get("file") == name and (folder / name).is_file():
        return {"kind": "image", "file": name, "describe": describe}
    request = prompt(describe)
    for _ in range(2):
        state["calls"]["image"] = state["calls"].get("image", 0) + 1
        try:
            (folder / name).write_bytes(draw_background(request))
        except (ModelCallFailed, ModelNotConfigured, OSError) as failure:
            add_event(state, "note", f"The background could not be painted ({failure}); "
                      "a gradient instead.")
            return _gradient({})
        if light_enough(folder / name) and not framed(folder / name):
            return {"kind": "image", "file": name, "describe": describe}
        request = prompt(describe) + (
            " The last one was framed: paint it edge to edge, with no border or margin."
            if framed(folder / name) else
            " The last one was too dark: make it much lighter and brighter, in soft pale "
            "colours.")
    (folder / name).unlink(missing_ok=True)
    add_event(state, "note", "The painted background came out too dark or framed twice; "
              "a light gradient instead.")
    return _gradient({})


def draw_background(request: str) -> bytes:
    """A background, from the cheaper image model: nothing in it must be right."""
    from pipeline.config import get_settings
    from pipeline.llm import ModelCallFailed, _picture_from_chat
    from pipeline.resilience import ServiceUnavailable, call

    try:
        picture = call("images", lambda: _picture_from_chat(
            request, "background", get_settings().background_image_model),
            attempts=4, give_up_after=300)
    except ServiceUnavailable as failure:
        raise ModelCallFailed(str(failure)) from failure
    if not picture:
        raise ModelCallFailed("The image model returned no background.")
    return picture


def prompt(describe: str) -> str:
    return (f"Wide 16:9 background art for a scene of an educational explainer video: "
            f"{describe}. Full-bleed: the art runs to all four edges of the image -- never "
            "a frame, border, mat, margin or vignette round it, never a picture inside a "
            "picture. Light, airy and pleasant -- never dark or gloomy; soft, "
            "complementary colours; artistic and interesting to look at, but subtle: muted, "
            "low in contrast, a quiet ground that words and pictures read on -- never "
            "busy or overdone. Keep the centre open and uncluttered: the scene's own "
            "pictures and words go there. Absolutely no text, letters or numbers.")


def light_enough(path: Path) -> bool:
    from PIL import Image, ImageStat

    with Image.open(path) as opened:
        grey = opened.convert("L")
    width, height = grey.size
    centre = grey.crop((width // 4, height // 4, 3 * width // 4, 3 * height // 4))
    return (ImageStat.Stat(grey).mean[0] >= LIGHTEST_DARK
            and ImageStat.Stat(centre).mean[0] >= LIGHTEST_CENTRE)


def framed(path: Path) -> bool:
    """A picture painted inside a margin: its outermost edge nearly one flat colour all
    round. Measured on Chapter 1's backgrounds: the framed ones varied by 1 to 11 grey
    levels along their outer three pixels, every full-bleed one by 24 or more."""
    from PIL import Image, ImageStat

    with Image.open(path) as opened:
        grey = opened.convert("L")
    width, height = grey.size
    edge = max(2, round(0.004 * min(width, height)))

    def strips(at: int) -> list:
        return [grey.crop((at, at, width - at, at + edge)),
                grey.crop((at, height - at - edge, width - at, height - at)),
                grey.crop((at, at, at + edge, height - at)),
                grey.crop((width - at - edge, at, width - at, height - at))]

    outer = [ImageStat.Stat(strip) for strip in strips(0)]
    if max(stat.stddev[0] for stat in outer) >= FLATTEST_EDGE:
        return False
    # Flat all round. A soft wash is flat all round too, and stays so inward (v7's
    # "soft dawn wash" was thrown away as framed); a mat ends where the picture starts.
    for share in (0.05, 0.10, 0.15):                    # mats come in widths
        inner = [ImageStat.Stat(strip) for strip in strips(round(share * min(width, height)))]
        if sum(abs(o.mean[0] - i.mean[0]) > FLATTEST_EDGE or i.stddev[0] > 2 * FLATTEST_EDGE
               for o, i in zip(outer, inner, strict=True)) >= 3:
            return True
    return False


def lightened(colour: str) -> str:
    """The colour, mixed with white until it is at least LEAST_GRADIENT_LIGHTNESS."""
    red, green, blue = (int(colour.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    lightness = (0.299 * red + 0.587 * green + 0.114 * blue) / 255
    if lightness >= LEAST_GRADIENT_LIGHTNESS:
        return colour.lower()
    mix = (LEAST_GRADIENT_LIGHTNESS - lightness) / (1 - lightness)
    return "#" + "".join(f"{round(c + (255 - c) * mix):02x}" for c in (red, green, blue))


def _is_colour(value: Any) -> bool:
    text = str(value or "")
    return len(text) == 7 and text.startswith("#") and all(
        c in "0123456789abcdefABCDEF" for c in text[1:])


def _folder_of(slug: str, visual_id: str) -> Path | None:
    from pipeline.core import require_project
    from pipeline.generation import VisualPlanStore
    from pipeline.scene_lab import _visual, scene_folder

    project = require_project(slug)
    return scene_folder(project, _visual(VisualPlanStore(project.root).load(), visual_id))


def state_of(slug: str, visual_id: str) -> dict[str, Any]:
    """What the scene's page shows of its background: what it is, and whether it is on."""
    folder = _folder_of(slug, visual_id)
    found = read(folder) if folder else {}
    return {"kind": found.get("kind", ""), "on": found.get("on", True) if found else False,
            "describe": found.get("describe", ""), "colours": found.get("colours", []),
            "file": found.get("file", "")}


def toggle(slug: str, visual_id: str, on: bool) -> dict[str, Any]:
    """Switch the scene's background off or back on, and draw the scene again."""
    from pipeline.core import OperationFailed
    from pipeline.scene_lab import run_scene

    folder = _folder_of(slug, visual_id)
    if folder is None or not read(folder):
        raise OperationFailed("This scene has no background to switch.")
    switch(folder, on)
    return run_scene(slug, visual_id) | {"background": state_of(slug, visual_id)}
