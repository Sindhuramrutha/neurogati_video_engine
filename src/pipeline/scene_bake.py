"""A scene program written from shots, with every value in it.

Before a render the program is written with its pictures named and its moments in
seconds (`written_program`); after it, the places the kit chose for each picture,
title, tag and card (`decisions.json`) are written into it too (`bake`). The
program then renders the same scene, and everything about where and when is in
the file a person opens -- to read, and to change by hand.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipeline.scene_shots import Pictures, is_shots
from pipeline.shot_program import program_for
from pipeline.shot_values import picture_files, timing_of

DECISIONS = "decisions.json"
WRITTEN_FROM_SHOTS = "# Written from the scene's shots"


def pictures_for(brief: dict[str, Any], parts: dict | None, folder: Path | None) -> Pictures:
    """What the shots may use, with each picture's file and what it shows."""
    files, about = picture_files(brief, folder)
    taken = frozenset(entry["index"] for entry in brief.get("picture_catalogue") or []
                      if entry.get("main_of"))
    return Pictures(len(files), parts or {}, taken, files, about)


def written_program(spec: dict, brief: dict[str, Any], parts: dict | None,
                    folder: Path | None) -> str:
    """The program for these shots, its pictures named and its moments in seconds."""
    return program_for(spec, pictures_for(brief, parts, folder), timing_of(brief))


def bake(folder: Path, spec: dict, brief: dict[str, Any], parts: dict | None) -> bool:
    """Write the places the last render chose into the scene's program. Only a
    program written from these shots is rewritten: one written by hand is the
    person's, and is left as it is. True when it was rewritten."""
    entry, decided = folder / "scene.py", folder / DECISIONS
    if not is_shots(spec) or not entry.exists() or not decided.exists():
        return False
    current = entry.read_text(encoding="utf-8")
    if WRITTEN_FROM_SHOTS not in current:
        return False
    try:
        layouts = json.loads(decided.read_text(encoding="utf-8"))
        code = program_for(spec, pictures_for(brief, parts, folder), timing_of(brief), layouts)
        compile(code, str(entry), "exec")
    except (ValueError, SyntaxError, json.JSONDecodeError, KeyError, TypeError):
        return False
    if code != current:
        entry.write_text(code, encoding="utf-8")
    return True
