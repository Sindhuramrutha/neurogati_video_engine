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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

VERDICTS = "picture-verdicts.json"
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


def _is_described(known: dict[str, Any], picture: str) -> bool:
    """Described with a role. A verdict kept before roles said only whether it
    teaches -- a badge and the deck's art alike were "no" -- so it is asked again
    rather than guessed: guessed, a badge was offered as the deck's art."""
    return isinstance(known.get(picture), dict) and "role" in known[picture]


DESCRIBED_AT_ONCE = 4


def notes(scenes: Path, pictures: list[str]) -> dict[str, dict[str, str]]:
    """What each of these deck pictures is and what it is good for, by path. The
    deck is described once, when its script is drafted (`describe_deck`); here,
    what is already described is read, and any picture still undescribed is asked
    about -- a few at a time, and once: scenes starting together wait for the batch
    being asked, then read its answers. One that could not be asked about has no
    note, and is offered all the same."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured
    from pipeline.storage.documents import read_json_object, write_text_atomically

    path = scenes / VERDICTS

    def read() -> dict[str, Any]:
        return read_json_object(path, "picture notes") or {}

    def undescribed(known: dict[str, Any]) -> list[str]:
        return [p for p in dict.fromkeys(pictures)
                if not _is_described(known, p) and not _is_made_for_the_scene(p)]

    known = read()
    if undescribed(known):
        with _ASKING:
            known = read()
            asking = undescribed(known)

            def ask(picture: str) -> tuple[str, dict[str, Any] | None]:
                try:
                    return picture, _ask(Path(picture))
                except (ModelCallFailed, ModelNotConfigured, OSError) as failure:
                    logger.warning("picture not described (%s): %s", picture, failure)
                    return picture, None

            with ThreadPoolExecutor(max_workers=DESCRIBED_AT_ONCE) as pool:
                answers = dict(pool.map(ask, asking))
            known.update({p: a for p, a in answers.items() if a is not None})
            if any(a is not None for a in answers.values()):
                write_text_atomically(path, json.dumps(known, indent=1, ensure_ascii=False))
    return {p: {"what": str(known[p].get("what", "")), "role": str(known[p]["role"])}
            for p in pictures if _is_described(known, p)}


def describe_deck(project) -> dict[str, dict[str, str]]:
    """Every picture the deck hands on, described once -- at the hand-off to the
    script, so no scene waits on it later."""
    from pipeline.plan_pictures import assets_for_later_stages
    from pipeline.scene_program import SCENES

    library = assets_for_later_stages(project).library
    return notes(project.root / SCENES, [
        str(project.root / f.shown_path) for f in library.handed_on()
        if (project.root / f.shown_path).exists()])


# One batch is asked about at a time across the scenes being made: the others wait
# and then read its answers from the file.
_ASKING = threading.Lock()


def _is_made_for_the_scene(picture: str) -> bool:
    """A picture painted or found for one scene: it is described where it was made."""
    name = Path(picture).name
    return name.startswith(("illustration-", "found-", "icon-"))


def with_painting_asked(on_screen: str, pictures: list[str]) -> str:
    """The brief's on-screen text. Only a scene with no deck picture at all, and
    none asked for, has one painted from what its brief says to DRAW (or the
    PICTURE it named)."""
    from pipeline.scene_illustration import wanted

    if not pictures and not wanted(on_screen):
        found = {m.group(1).upper(): m.group(2) for m in DRAWN.finditer(on_screen or "")}
        asked = found.get("DRAW") or found.get("PICTURE", "")
        if asked and asked.lower() not in ("none", "-"):
            on_screen = f"{on_screen.rstrip()}\nILLUSTRATE: {asked}"
    return on_screen
