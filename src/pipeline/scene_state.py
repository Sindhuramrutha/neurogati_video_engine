"""What is kept about one scene's making: its status, its steps, what it cost.

`agent.json` in the scene's folder. Small on purpose: the model is not given a
conversation to remember (each round is asked afresh, from the scene's files and
the last result), so there is nothing long to keep.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipeline.generation import _now

STATE = "agent.json"
STOP = "stop-agent"
LONGEST_EVENT = 300


def fresh_state() -> dict[str, Any]:
    return {"status": "idle", "events": [], "summary": "", "remarks": [], "doing": "",
            "renders": 0, "calls": {"agent": 0, "vision": 0},
            "tokens": {"prompt": 0, "completion": 0}, "last_render": None, "error": "",
            "updated_at": ""}


def load_state(folder: Path | None) -> dict[str, Any]:
    path = folder / STATE if folder else None
    if path is None or not path.exists():
        return fresh_state()
    saved = json.loads(path.read_text(encoding="utf-8"))
    # Fields a record may still carry that nothing reads.
    saved.pop("messages", None)
    saved.pop("question", None)
    return fresh_state() | saved


def save_state(folder: Path, state: dict[str, Any]) -> None:
    if not folder.is_dir():
        return                   # its project was deleted: nothing is written back
    state["updated_at"] = _now()
    (folder / STATE).write_text(json.dumps(state, indent=1, ensure_ascii=False),
                                encoding="utf-8")


def add_event(state: dict[str, Any], kind: str, text: str) -> None:
    state["events"].append({"at": _now(), "kind": kind, "text": text[:LONGEST_EVENT]})


def doing(folder: Path, state: dict[str, Any], what: str) -> None:
    """What is happening this moment, saved so the page can say so."""
    state["doing"] = what
    save_state(folder, state)
