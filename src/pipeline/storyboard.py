"""The storyboard: a still card for every scene of a section, approved before any
scene is animated.

A card is the scene's main picture -- the illustration painted for it in the
project's style, or its slide's own picture -- with what its brief says will be
drawn and labelled, and its first words. That is where most of a scene's
direction is decided (the wrong picture, the wrong subject, the wrong idea),
and a card costs only the painting that making the scene would pay for anyway:
no animation, no rounds.

The first section's storyboard must be approved before scenes are made (Video
quality plan, D): it sets the style every later scene follows. A person can
leave a note on any card -- "use the Volta portrait", "show the leg larger" --
which is the scene's instruction when it is made, and repaint its picture with
the note.

Kept at generation/storyboard.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pipeline.core import OperationFailed, require_project
from pipeline.generation import VisualPlanStore
from pipeline.storage.documents import read_json_object, write_text_atomically

BRIEF_LINES = ("PICTURE", "DRAW", "LABELS", "ILLUSTRATE")


def _path(project) -> Path:
    return project.root / "generation" / "storyboard.json"


def _load(project) -> dict[str, Any]:
    saved = read_json_object(_path(project), "storyboard") or {}
    return {"approved": list(saved.get("approved", [])), "notes": dict(saved.get("notes", {}))}


def _save(project, board: dict[str, Any]) -> None:
    write_text_atomically(_path(project), json.dumps(board, indent=1, ensure_ascii=False))


def _sections(project) -> list[tuple[str, str, list]]:
    """(section id, title, its visuals in order), in the video's order."""
    order: dict[str, tuple[str, list]] = {}
    for visual in VisualPlanStore(project.root).load().visuals:
        order.setdefault(visual.section_id, (visual.section_title, []))[1].append(visual)
    return [(section_id, title, sorted(visuals, key=lambda v: v.scene_number))
            for section_id, (title, visuals) in order.items()]


def note_for(project, visual_id: str) -> str:
    """The person's note on this scene's card: its instruction when it is made."""
    return _load(project)["notes"].get(visual_id, "")


def gate(project) -> str:
    """Why scenes cannot be made yet, or empty when they can."""
    sections = _sections(project)
    if not sections:
        return ""
    first_id, title, _ = sections[0]
    if first_id in _load(project)["approved"]:
        return ""
    return (f"Approve the storyboard of the first section (\"{title}\") before making scenes: "
            "it sets the style every scene follows. It is on the Storyboard tab.")


def _brief_lines(on_screen: str) -> dict[str, str]:
    found = {}
    for name in BRIEF_LINES:
        match = re.search(rf"^\s*{name}\s*:\s*(.+)$", on_screen or "", re.MULTILINE | re.IGNORECASE)
        if match and match.group(1).strip().lower() not in ("none", "-"):
            found[name.lower()] = match.group(1).strip()
    return found


def _picture_of(project, visual) -> tuple[str, str]:
    """(where the card's picture is, as the page asks for it, and what it is)."""
    from pipeline.scene_lab import scene_folder

    folder = scene_folder(project, visual)
    brief = read_json_object(folder / "brief.json", "brief") if folder else None
    pictures = (brief or {}).get("pictures") or []
    if not pictures:
        return "", "none"
    first = Path(pictures[0])
    if first.name.startswith("illustration-"):
        return f"scenes/{visual.id}/files/{first.name}", "painted"
    if "prepared" in first.parts:
        return f"assets/prepared/{first.name}", "slide"
    return f"extraction/assets/{first.name}", "slide"


def read(slug: str) -> dict[str, Any]:
    project = require_project(slug)
    board = _load(project)
    sections = []
    for index, (section_id, title, visuals) in enumerate(_sections(project)):
        cards = []
        for visual in visuals:
            from pipeline.scene_lab import _scene_of

            scene = _scene_of(project, visual)
            on_screen = scene.brief if scene else visual.brief
            narration = scene.narration if scene else visual.narration_preview
            picture, kind = _picture_of(project, visual)
            cards.append({"visual_id": visual.id, "number": visual.scene_number,
                          "says": " ".join(narration.split())[:180],
                          "brief": _brief_lines(on_screen),
                          "picture": picture, "picture_kind": kind,
                          "note": board["notes"].get(visual.id, "")})
        sections.append({"id": section_id, "title": title, "required": index == 0,
                         "approved": section_id in board["approved"],
                         "prepared": any(card["picture"] for card in cards), "cards": cards})
    return {"sections": sections, "gate": gate(project)}


def prepare(slug: str, section_id: str) -> dict[str, Any]:
    """Each scene of the section briefed and its picture painted (AI, one image per
    scene that asks for one; kept, so making the scene later paints nothing)."""
    from pipeline.scene_illustration import paint
    from pipeline.scene_lab import scene_folder, write_brief

    project = require_project(slug)
    visuals = next((v for s, _, v in _sections(project) if s == section_id), None)
    if visuals is None:
        raise OperationFailed("No such section among the scenes.")
    state = {"calls": {"agent": 0, "vision": 0}, "events": []}
    missed = []
    for visual in visuals:
        # One card that cannot be prepared (its narration not spoken, its picture
        # not painted) is named; the others are still prepared.
        try:
            brief = write_brief(project, visual)
            folder = scene_folder(project, visual, create=True)
            if paint(folder, brief["on_screen"], brief["look"], state, brief["narration"],
                     note_for(project, visual.id)):
                write_brief(project, visual)
        except OperationFailed as failure:
            missed.append(f"Scene {visual.scene_number}: {failure}")
    board = read(slug)
    if missed:
        board["missed"] = missed
    return board


def set_note(slug: str, visual_id: str, note: str) -> dict[str, Any]:
    project = require_project(slug)
    board = _load(project)
    if note.strip():
        board["notes"][visual_id] = note.strip()[:600]
    else:
        board["notes"].pop(visual_id, None)
    _save(project, board)
    return read(slug)


def repaint(slug: str, visual_id: str) -> dict[str, Any]:
    """Paint the card's picture again, with its note (AI, one image)."""
    from pipeline.scene_illustration import kept, paint
    from pipeline.scene_lab import _visual, scene_folder, write_brief

    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    brief = write_brief(project, visual)
    folder = scene_folder(project, visual, create=True)
    old = kept(folder, brief["on_screen"], brief["look"])
    if old is None:
        raise OperationFailed("This scene has no painted picture to paint again: its picture "
                              "is the slide's own. Leave a note for the scene instead.")
    old.unlink(missing_ok=True)
    old.with_suffix(".json").unlink(missing_ok=True)
    state = {"calls": {"agent": 0, "vision": 0}, "events": []}
    paint(folder, brief["on_screen"], brief["look"], state, brief["narration"],
          note_for(project, visual.id))
    write_brief(project, visual)
    return read(slug)


def approve(slug: str, section_id: str, approved: bool = True) -> dict[str, Any]:
    project = require_project(slug)
    board = _load(project)
    board["approved"] = [s for s in board["approved"] if s != section_id]
    if approved:
        board["approved"].append(section_id)
    _save(project, board)
    return read(slug)
