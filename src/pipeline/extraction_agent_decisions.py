"""What the person decides about the Extraction agent's proposals: apply one,
apply all of a conversation's, discard one, or undo the last apply.

The agent only proposes (`extraction_agent.py`); nothing it says changes the
extraction until one of these runs. An apply keeps the file as it was before, so
one Undo puts it back -- for "apply all", every change of the batch at once:
the page applies them one by one (so it can show each landing), and each names
the batch it continues.
"""

from __future__ import annotations

from typing import Any

from pipeline.core import OperationFailed, require_project
from pipeline.extraction_agent import AgentThreads, AgentThreadStore, view
from pipeline.extraction_edits import apply_changes, remember_for_undo, undo_last, undo_point
from pipeline.projects import Project


def _find_turn(threads: AgentThreads, file_name: str, turn_id: str):
    for conversation in threads.for_file(file_name):
        for turn in conversation.turns:
            if turn.id == turn_id:
                return conversation, turn
    return None, None


def _proposal(project: Project, file_name: str, turn_id: str):
    threads = AgentThreadStore(project.root).load()
    conversation, turn = _find_turn(threads, file_name, turn_id)
    if turn is None or turn.status != "proposed":
        raise OperationFailed("That proposal is not open any more.")
    return threads, conversation, turn


def apply_proposal(slug: str, file_name: str, turn_id: str,
                   continues: str = "") -> dict[str, Any]:
    """Apply every change in one proposal, and keep what it replaced for undo.

    `continues` is the batch this apply joins ("apply all"): the ids already
    applied in it, comma-joined, exactly as the last apply recorded them. The
    restore point then stays the file as it was before the batch's first change,
    so one Undo puts the whole batch back."""
    from pipeline.extraction_run import extraction_page

    project = require_project(slug)
    threads, conversation, turn = _proposal(project, file_name, turn_id)
    before, _after = apply_changes(project, file_name, turn.changes)
    point = undo_point(project)
    joining = (continues and point.file_name == file_name and point.turn_id == continues
               and point.document is not None)
    remember_for_undo(project, file_name,
                      f"{continues},{turn.id}" if joining else turn.id,
                      point.document if joining else before)
    turn.status = "applied"
    AgentThreadStore(project.root).save(threads)
    return {
        "thread": view(project, file_name, conversation, threads.for_file(file_name)),
        "extraction": extraction_page(project),
    }


def discard_proposal(slug: str, file_name: str, turn_id: str) -> dict[str, Any]:
    project = require_project(slug)
    threads, conversation, turn = _proposal(project, file_name, turn_id)
    turn.status = "discarded"
    AgentThreadStore(project.root).save(threads)
    return {"thread": view(project, file_name, conversation, threads.for_file(file_name))}


def undo_agent_changes(slug: str, file_name: str) -> dict[str, Any]:
    """Put back the blocks the last applied proposal changed."""
    from pipeline.extraction_run import extraction_page

    project = require_project(slug)
    undone = undo_last(project, file_name)
    store = AgentThreadStore(project.root)
    threads = store.load()
    conversation = None
    # One proposal, or every one an "apply all" applied (their ids, comma-joined).
    for turn_id in undone["turn_id"].split(","):
        found, turn = _find_turn(threads, file_name, turn_id)
        conversation = conversation or found
        if turn is not None:
            turn.status = "undone"
    store.save(threads)
    return {
        "thread": view(project, file_name, conversation, threads.for_file(file_name)),
        "extraction": extraction_page(project),
    }
