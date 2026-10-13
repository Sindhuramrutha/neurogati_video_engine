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


def paint(folder: Path, on_screen: str, look: dict[str, Any],
          state: dict[str, Any]) -> Path | None:
    """Paint the illustration the brief asks for, once. None when it asks for none,
    or the image model could not paint it (the scene is made without it)."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured, draw_image
    from pipeline.scene_state import add_event

    asked = wanted(on_screen)
    if not asked:
        return None
    path = _path(folder, asked, look)
    if path.exists():
        return path
    state["calls"]["image"] = state["calls"].get("image", 0) + 1
    try:
        path.write_bytes(draw_image(prompt(asked, look)))
    except (ModelCallFailed, ModelNotConfigured, OSError) as failure:
        add_event(state, "note", f"The illustration could not be painted ({failure}); "
                  "the scene is made without it.")
        return None
    add_event(state, "note", f"Painted an illustration: {asked}")
    return path
