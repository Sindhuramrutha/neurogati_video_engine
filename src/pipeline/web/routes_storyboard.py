"""The storyboard: a card per scene, painted, noted and approved before scenes are
made. The work is in `pipeline.storyboard`."""

from __future__ import annotations

from typing import Any

import anyio
from litestar import get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath

from pipeline import storyboard
from pipeline.core import OperationFailed


def _guarded(call, *args):
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/storyboard", sync_to_thread=False)
def read_storyboard(slug: FromPath[str]) -> dict[str, Any]:
    return _guarded(storyboard.read, slug)


@post("/api/projects/{slug:str}/storyboard/prepare")
async def prepare_storyboard(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """Brief every scene of a section and paint its picture (AI, images)."""
    section_id = str(data.get("section_id", ""))
    return await anyio.to_thread.run_sync(lambda: _guarded(storyboard.prepare, slug, section_id))


@post("/api/projects/{slug:str}/storyboard/note", sync_to_thread=False)
def note_on_card(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    return _guarded(storyboard.set_note, slug, str(data.get("visual_id", "")),
                    str(data.get("note", "")))


@post("/api/projects/{slug:str}/storyboard/repaint")
async def repaint_card(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """Paint a card's picture again, with its note (AI, one image)."""
    visual_id = str(data.get("visual_id", ""))
    return await anyio.to_thread.run_sync(lambda: _guarded(storyboard.repaint, slug, visual_id))


@post("/api/projects/{slug:str}/storyboard/approve", sync_to_thread=False)
def approve_storyboard(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    return _guarded(storyboard.approve, slug, str(data.get("section_id", "")),
                    bool(data.get("approved", True)))


STORYBOARD_ROUTES = [read_storyboard, prepare_storyboard, note_on_card, repaint_card,
                     approve_storyboard]
