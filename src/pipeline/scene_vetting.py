"""What each deck picture is, asked once of the vision model and kept -- never a gate.

A deck carries more than its figures: a publisher's "Check for updates" badge,
the book's own cover, a robot hand holding a brain, a floral banner. A vision
verdict once withheld every picture that did not "teach": in Demo 001 it took
ten of the twenty-two pictures out of every scene, the deck's own art among
them, and the video stopped looking like the course it came from.

Now nothing is withheld. Each picture is described once -- what it is, and what
it is good for -- and the scene agent, told that, decides whether and how to
show it: the subject a scene explains, a backdrop while a topic is opened or its
context given, or not at all. A picture the model could not be asked about is
offered all the same. Cached for the whole project beside the scenes.
"""

from __future__ import annotations

import json
import logging
import re
import threading
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

VERDICTS = "picture-verdicts.json"
_LOCK = threading.Lock()
DRAWN = re.compile(r"^\s*(DRAW|PICTURE)\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
ROLES = {
    "explains": "explains something: a scene can be built around it",
    "sets_scene": "the deck's art: a backdrop while a topic is opened or its context given",
    "furniture": "deck furniture (a badge, a cover, a crop of text): rarely worth showing",
}


class PictureNote(BaseModel):
    what: str = Field(description="What it is, in a few words.")
    role: Literal["explains", "sets_scene", "furniture"] = Field(description=(
        "explains: a drawing, diagram, photograph, portrait, apparatus, chart, map or "
        "engraving a lesson could explain. sets_scene: decorative or stock art about the "
        "topic -- a stylised brain, an abstract network, a banner -- that sets the mood "
        "while a topic is opened. furniture: a logo, badge or button, a book or journal "
        "cover, a crop of a slide's text, a placeholder."))


def _ask(path: Path) -> dict[str, Any]:
    from pipeline.llm import VISION_TOKENS, complete_structured_with_images
    from pipeline.resilience import ServiceUnavailable, call
    from pipeline.scene_review import _jpeg

    # Through the gate: a deck's pictures are described one after another, and the
    # provider throttles a burst (429) -- each was lost, undescribed, without it.
    try:
        note = call("vision", lambda: complete_structured_with_images(
            PictureNote,
            "You catalogue the pictures found in a lecture deck for the animator who will "
            "make the course's video from it.",
            "What is this picture, and what could the video use it for?",
            [(path.name, _jpeg(path))], max_tokens=VISION_TOKENS),
            attempts=5, base_seconds=5, longest_wait=60, give_up_after=300)
    except ServiceUnavailable as failure:
        from pipeline.llm import ModelCallFailed
        raise ModelCallFailed(str(failure)) from failure
    return {"what": note.what[:120], "role": note.role}


def _as_note(known: dict[str, Any]) -> dict[str, str]:
    """A cached answer, in today's shape: one kept before roles was a verdict of
    whether it teaches."""
    if "role" in known:
        return {"what": str(known.get("what", "")), "role": str(known["role"])}
    return {"what": str(known.get("what", "")),
            "role": "explains" if known.get("teaches", True) else "sets_scene"}


def notes(scenes: Path, pictures: list[str]) -> dict[str, dict[str, str]]:
    """What each of these deck pictures is and what it is good for, by path. A
    picture not yet described is asked about once; one that could not be asked
    about has no note, and is offered all the same."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured

    path = scenes / VERDICTS
    with _LOCK:
        known = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for picture in pictures:
        if picture in known or _is_made_for_the_scene(picture):
            continue
        try:
            answer = _ask(Path(picture))
        except (ModelCallFailed, ModelNotConfigured, OSError) as failure:
            logger.warning("picture not described (%s): %s", picture, failure)
            continue
        with _LOCK:
            known = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            known[picture] = answer
            scenes.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(known, indent=1, ensure_ascii=False), encoding="utf-8")
    return {p: _as_note(known[p]) for p in pictures if p in known}


def _is_made_for_the_scene(picture: str) -> bool:
    """A picture painted or found for one scene: it is described where it was made."""
    name = Path(picture).name
    return name.startswith(("illustration-", "found-", "icon-"))


def offered(scenes: Path, on_screen: str, pictures: list[str]) -> tuple[str, list[str]]:
    """The brief's on-screen text and every deck picture -- described, none withheld.
    Only a scene with no deck picture at all, and none asked for, has one painted
    from what its brief says to DRAW (or the PICTURE it named)."""
    from pipeline.scene_illustration import wanted

    notes(scenes, pictures)
    if not pictures and not wanted(on_screen):
        found = {m.group(1).upper(): m.group(2) for m in DRAWN.finditer(on_screen or "")}
        asked = found.get("DRAW") or found.get("PICTURE", "")
        if asked and asked.lower() not in ("none", "-"):
            on_screen = f"{on_screen.rstrip()}\nILLUSTRATE: {asked}"
    return on_screen, list(pictures)
