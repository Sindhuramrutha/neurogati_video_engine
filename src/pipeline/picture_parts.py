"""Where the parts of a picture are, so a pointer lands on the part it names.

A callout used to be a dot at an (x, y) the scene model guessed from a free-text
description of the picture; on Demystifying the Brain a label meant for the brain
pointed at a statue's clothing. Now each picture's parts are located once by the
vision model as boxes, with whether it can see each one clearly, and kept. A
callout names a part; its dot goes to the middle of that part's box. A part the
model was not sure of, or did not find, gets no callout at all: no pointer is
better than one pointing at the wrong thing.
"""

from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

PARTS_FILE = "picture-parts-v3.json"       # beside the scenes, for the whole project
MOST_PARTS = 12
_LOCK = threading.Lock()


class Part(BaseModel):
    name: str = Field(description="What the part is, in 1 to 4 words, as a label would say it.")
    box: list[float] = Field(description="Its bounding box as [ymin, xmin, ymax, xmax], each "
                                         "from 0 to 1000 of the picture's height or width.")
    sure: bool = Field(description="True only when this part is clearly visible in this "
                                   "picture and the box is tight around it.")


class PictureParts(BaseModel):
    summary: str = Field(description="What the picture shows and teaches, in two sentences.")
    parts: list[Part] = Field(default_factory=list, description=(
        f"Up to {MOST_PARTS} parts a lesson might point to, each where it really is."))


def _ask(path: Path) -> dict[str, Any]:
    from pipeline.llm import VISION_TOKENS, ModelCallFailed, complete_structured_with_images
    from pipeline.resilience import ServiceUnavailable, call
    from pipeline.scene_review import _jpeg

    try:
        found = call("vision", lambda: complete_structured_with_images(
            PictureParts,
            "You locate the parts of a picture for an animator who will point at them on "
            "screen. Give each part's real bounding box; never guess a box for a part you "
            "cannot see.",
            "What does this picture show, and where exactly is each part a lesson might "
            "point to?", [(path.name, _jpeg(path))], max_tokens=VISION_TOKENS),
            attempts=5, base_seconds=5, longest_wait=60, give_up_after=300)
    except ServiceUnavailable as failure:
        raise ModelCallFailed(str(failure)) from failure
    parts = []
    for part in found.parts[:MOST_PARTS]:
        box = _box(part.box)
        if box is not None:
            parts.append({"name": part.name.strip()[:40], "box": box, "sure": part.sure})
    return {"summary": found.summary.strip()[:400], "parts": parts}


def _box(asked: list[float]) -> list[float] | None:
    """[left, top, right, bottom] as fractions, from the model's [ymin, xmin, ymax,
    xmax] out of 1000 (its own convention: read as fractions in the other order, every
    box was clamped to nothing and no picture had a part). None when it is empty."""
    if len(asked) != 4:
        return None
    scale = 1000.0 if max(asked) > 1.5 else 1.0
    top, left, bottom, right = (min(1.0, max(0.0, float(v) / scale)) for v in asked)
    return [left, top, right, bottom] if right > left and bottom > top else None


def parts_of(scenes: Path, path: str, state: dict[str, Any] | None = None) -> dict[str, Any]:
    """The picture's summary and located parts; asked once and kept. Empty when it
    could not be asked about (it is then shown without callouts)."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured
    from pipeline.storage.documents import read_json_object, write_text_atomically

    file = scenes / PARTS_FILE
    known = read_json_object(file, "picture parts") or {}
    if path in known:
        return known[path]
    with _LOCK:
        known = read_json_object(file, "picture parts") or {}
        if path in known:
            return known[path]
        if state is not None:
            state["calls"]["vision"] = state["calls"].get("vision", 0) + 1
        try:
            known[path] = _ask(Path(path))
        except (ModelCallFailed, ModelNotConfigured, OSError):
            return {}
        write_text_atomically(file, json.dumps(known, ensure_ascii=False, indent=1))
        return known[path]


def _words(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def anchor(parts: list[dict[str, Any]], name: str) -> tuple[float, float] | None:
    """The middle of the part `name` names, when the picture has it and the model was
    sure of it; None otherwise (no pointer is drawn)."""
    wanted = _words(name)
    if not wanted:
        return None
    sure = [p for p in parts if p.get("sure")]
    match = next((p for p in sure if _words(p["name"]) == wanted), None) or next(
        (p for p in sure if wanted in _words(p["name"]) or _words(p["name"]) in wanted), None)
    if match is None:
        return None
    left, top, right, bottom = match["box"]
    return (left + right) / 2, (top + bottom) / 2


def described(index: int, file_name: str, found: dict[str, Any]) -> str:
    """One line for the scene model: what the picture is, and the parts it may point to."""
    sure = [p["name"] for p in found.get("parts", []) if p.get("sure")]
    return (f"- pictures[{index}] ({file_name}): {found.get('summary', '')} "
            + (f"Parts you may point to: {', '.join(sure)}." if sure
               else "No part can be pointed to: show it without callouts."))
