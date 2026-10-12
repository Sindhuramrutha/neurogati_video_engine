"""Scene Plan: the planning conversation, the setup and the pictures.
The work is in `pipeline.plan_agent`, `pipeline.lesson_plan` and
`pipeline.plan_pictures`.
"""

from __future__ import annotations

from typing import Any

from litestar import delete, get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath

from pipeline.core import OperationFailed, require_project
from pipeline.plan_agent import agree, discard_proposal, read_planning, send_message, set_setup
from pipeline.planning import PlanStore
from pipeline.presentation import present_artifact


def _plan_after(call, slug: str, *args) -> dict[str, Any]:
    try:
        call(slug, *args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure
    project = require_project(slug)
    return present_artifact(project, "plan", PlanStore(project.root).load())


def _guarded(call, *args) -> dict[str, Any]:
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/plan/planning", sync_to_thread=False)
def get_planning(slug: FromPath[str]) -> dict[str, Any]:
    """The conversation with the planning agent, and any proposed shape."""
    return _guarded(read_planning, slug)


@post("/api/projects/{slug:str}/plan/setup", sync_to_thread=False)
def save_setup(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """The length in the person's words, the slide order and the audience."""
    return _plan_after(set_setup, slug, data)


@post("/api/projects/{slug:str}/plan/message")
async def say_to_planner(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """A message to the planning agent. It answers with a proposed shape (AI)."""
    import anyio

    return await anyio.to_thread.run_sync(
        _guarded, send_message, slug, str(data.get("text", "")))


@post("/api/projects/{slug:str}/plan/agree")
async def agree_to_shape(slug: FromPath[str]) -> dict[str, Any]:
    """Make the proposed shape the plan, and write its scenes (AI, one call per section)."""
    import anyio

    return await anyio.to_thread.run_sync(_guarded, agree, slug)


@delete("/api/projects/{slug:str}/plan/proposal", status_code=200, sync_to_thread=False)
def discard_shape(slug: FromPath[str]) -> dict[str, Any]:
    return _guarded(discard_proposal, slug)


@post("/api/projects/{slug:str}/plan/sections/{section_id:str}/pictures", sync_to_thread=False)
def choose_pictures(slug: FromPath[str], section_id: FromPath[str],
                    data: dict[str, Any]) -> dict[str, Any]:
    """Attach exactly these pictures to a section; `paths: null` hands it back to the rule."""
    from pipeline.plan_pictures import choose_section_pictures

    paths = data.get("paths")
    return _plan_after(choose_section_pictures, slug, section_id,
                       [str(p) for p in paths] if isinstance(paths, list) else None)


@get("/api/projects/{slug:str}/upstream", sync_to_thread=False)
def get_upstream_state(slug: FromPath[str]) -> dict[str, Any]:
    """For each layer: what changed before it since it was handed on."""
    from pipeline.upstream import upstream_state

    return upstream_state(require_project(slug))


LESSON_PLAN_ROUTES = [get_planning, save_setup, say_to_planner, agree_to_shape, discard_shape,
                      choose_pictures, get_upstream_state]
