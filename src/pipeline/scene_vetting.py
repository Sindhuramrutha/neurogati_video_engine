"""Whether a deck's picture teaches, asked once of the vision model and kept.

A deck carries more than its figures: a publisher's "Check for updates" badge,
the book's own cover, a crop of a slide's text. Each came through every measure
of size and tone and was offered to a scene as its picture -- a badge was a
scene's only picture, its parts labelled "brain", "hand" and "blood". The vision
model already knew what it was ("a CrossMark button"); nothing asked it whether
to show it. Now one look says, per picture, cached for the whole project; one
that does not teach is not offered, and a scene left with no picture has one
painted from its brief's DRAW line.
"""

from __future__ import annotations

import json
import logging
import re
import threading
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

VERDICTS = "picture-verdicts.json"
_LOCK = threading.Lock()
DRAWN = re.compile(r"^\s*(DRAW|PICTURE)\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)


class PictureVerdict(BaseModel):
    teaches: bool = Field(description=(
        "True for a picture a lesson would show: a drawing, diagram, photograph, "
        "portrait, apparatus, chart, map or engraving. False for a logo, badge or "
        "button (such as 'Check for updates'), a book or journal cover, a crop of a "
        "slide's text, a screenshot of words, a placeholder or an icon."))
    what: str = Field(description="What it is, in a few words.")


def _ask(path: Path) -> dict[str, Any]:
    from pipeline.llm import VISION_TOKENS, complete_structured_with_images
    from pipeline.scene_review import _jpeg

    verdict = complete_structured_with_images(
        PictureVerdict,
        "You sort the pictures found in a lecture deck: which ones teach, and which "
        "are furniture of the deck or the book it came from.",
        "Does this picture teach something a learner should see?",
        [(path.name, _jpeg(path))], max_tokens=VISION_TOKENS)
    return {"teaches": verdict.teaches, "what": verdict.what[:120]}


def rejected(scenes: Path, pictures: list[str]) -> dict[str, str]:
    """The pictures among these that do not teach, each with what it is. A
    picture the model could not be asked about is kept: not knowing is not a
    reason to take the author's picture away."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured

    path = scenes / VERDICTS
    with _LOCK:
        known = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for picture in pictures:
        if picture in known or Path(picture).name.startswith("illustration-"):
            continue
        try:
            answer = _ask(Path(picture))
        except (ModelCallFailed, ModelNotConfigured, OSError) as failure:
            logger.warning("picture not vetted (%s): %s", picture, failure)
            continue
        with _LOCK:
            known = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            known[picture] = answer
            scenes.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(known, indent=1, ensure_ascii=False), encoding="utf-8")
    return {p: known[p]["what"] for p in pictures if p in known and not known[p]["teaches"]}


def offered(scenes: Path, on_screen: str, pictures: list[str]) -> tuple[str, list[str]]:
    """The brief's on-screen text and the deck pictures worth offering. With
    none left, and no picture asked for, the brief asks for one to be painted:
    what it says to DRAW (or the PICTURE it named)."""
    from pipeline.scene_illustration import wanted

    out = rejected(scenes, pictures)
    kept = [p for p in pictures if p not in out]
    if not kept and not wanted(on_screen):
        found = {m.group(1).upper(): m.group(2) for m in DRAWN.finditer(on_screen or "")}
        asked = found.get("DRAW") or found.get("PICTURE", "")
        if asked and asked.lower() not in ("none", "-"):
            on_screen = f"{on_screen.rstrip()}\nILLUSTRATE: {asked}"
    return on_screen, kept
