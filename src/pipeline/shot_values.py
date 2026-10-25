"""The values a scene program carries in itself: its pictures' files, and its times.

A program written from shots names every picture it shows as a constant at its top
(the file, and what it shows) and waits for seconds, not for words: each cue is
turned into the second it is spoken, from the narration's own word timings, the
same way the kit (`manimkit.when`) would find it. With the places the kit records
(`decisions.json`), nothing about where or when is left outside the file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# A part is never brought on in the last seconds: the kit's own rule (`_at_cue`).
LAST_ENTRY_SECONDS = 3.0
STOP_WORDS = frozenset("a an the of and or in on at to with its their his her for from by "
                       "is are as that this one two".split())


@dataclass(frozen=True)
class Timing:
    """The narration's word timings, its words, and its length."""
    words: tuple[dict, ...]
    narration: str
    seconds: float


def timing_of(brief: dict[str, Any]) -> Timing | None:
    """The brief's timing, or None before its narration is measured."""
    if not brief.get("words") or not brief.get("seconds"):
        return None
    return Timing(tuple(brief["words"]), str(brief.get("narration") or ""),
                  float(brief["seconds"]))


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", str(text).lower())


def second(cue: Any, timing: Timing | None, entry: bool = False) -> float | None:
    """The second `cue` starts being spoken, as the kit would find it: in the timed
    words, else by its place in the written narration. `entry`: a part brought on
    with it, never later than a few seconds before the end. None when it cannot be
    timed here (the kit then finds it by its words)."""
    wanted = _words(cue) if cue else []
    if not wanted or timing is None:
        return None
    flat = [(index, word) for index, timed in enumerate(timing.words)
            for word in _words(timed.get("text", ""))]
    found = None
    for start in range(len(flat) - len(wanted) + 1):
        if [word for _, word in flat[start:start + len(wanted)]] == wanted:
            found = timing.words[flat[start][0]]["start_ms"] / 1000
            break
    if found is None:
        narration = _words(timing.narration)
        for start in range(len(narration) - len(wanted) + 1):
            if narration[start:start + len(wanted)] == wanted:
                found = timing.seconds * start / max(1, len(narration))
                break
    if found is None:
        return None
    if entry:
        found = min(found, timing.seconds - LAST_ENTRY_SECONDS)
    return round(max(0.0, found), 2)


def picture_names(files: tuple[str, ...], about: tuple[str, ...]) -> list[str]:
    """A constant's name for each picture: an icon by what it shows (ICON_MAP), any
    other by its number (PICTURE_1); the comment beside it says what it shows."""
    names: list[str] = []
    for index, file in enumerate(files):
        words = [w for w in re.findall(r"[a-z]+", (about[index] if index < len(about)
                                                    else "").lower()) if w not in STOP_WORDS]
        if Path(file).name.startswith("icon-") and words:
            name = "ICON_" + "_".join(words[:2]).upper()
        else:
            name = f"PICTURE_{index + 1}"
        while name in names:
            name += "_"
        names.append(name)
    return names


def _named(path: Path, folder: Path | None) -> str:
    """A picture's file as the program, run in `folder`, reaches it: relative to it
    when they share a drive (`illustration-1.png`, `../../extraction/assets/a.png`)."""
    import os

    if folder is None:
        return path.as_posix()
    try:
        return Path(os.path.relpath(path, folder)).as_posix()
    except ValueError:                     # another drive: only the full path reaches it
        return path.as_posix()


def picture_files(brief: dict[str, Any], folder: Path | None) -> tuple[tuple[str, ...],
                                                                         tuple[str, ...]]:
    """Each picture the brief offers, as the program names it -- by its file name
    when it is in the scene's folder (where the program runs), else by its full
    path -- and what it shows."""
    paths = [Path(p) for p in (brief.get("assets") or {}).get("pictures") or []]
    catalogue = {entry.get("index"): entry for entry in brief.get("picture_catalogue") or []}
    files = tuple(_named(path, folder) for path in paths)
    about = tuple(" ".join(str(catalogue.get(index, {}).get("what") or "").split())
                  for index in range(len(paths)))
    return files, about
