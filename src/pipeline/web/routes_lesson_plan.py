"""Scene Plan as a lesson: the frame, reshaping after the target changes, and
AI · write summaries. The work is in `pipeline.lesson_plan` and
`pipeline.plan_summaries`; each route answers with the plan as the page shows it.
"""

from __future__ import annotations

from typing import Any

from litestar import get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath

from pipeline.core import OperationFailed, require_project
from pipeline.lesson_plan import reshape, set_lesson_frame
from pipeline.plan_summaries import accept_summaries, dismiss_summaries, propose_summaries
from pipeline.planning import PlanStore
from pipeline.presentation import present_artifact


def _plan_after(call, slug: str, *args) -> dict[str, Any]:
    try:
        call(slug, *args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure
    project = require_project(slug)
    return present_artifact(project, "plan", PlanStore(project.root).load())


def _ids(data: dict[str, Any]) -> list[str] | None:
    ids = data.get("section_ids")
    return [str(i) for i in ids] if isinstance(ids, list) else None


@post("/api/projects/{slug:str}/plan/lesson-frame", sync_to_thread=False)
def choose_lesson_frame(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """Which of Opening, Recap and Close wrap the body."""
    return _plan_after(set_lesson_frame, slug, list(data.get("parts") or []))


@post("/api/projects/{slug:str}/plan/reshape", sync_to_thread=False)
def reshape_plan(slug: FromPath[str]) -> dict[str, Any]:
    """Share the time out again -- after the target duration changed."""
    return _plan_after(reshape, slug)


@post("/api/projects/{slug:str}/plan/summaries", sync_to_thread=False)
def write_summaries(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """AI: propose a one-line summary for each section that needs one."""
    return _plan_after(propose_summaries, slug, bool(data.get("everything")))


@post("/api/projects/{slug:str}/plan/summaries/accept", sync_to_thread=False)
def accept_summary_proposals(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    return _plan_after(accept_summaries, slug, _ids(data))


@post("/api/projects/{slug:str}/plan/summaries/dismiss", sync_to_thread=False)
def dismiss_summary_proposals(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    return _plan_after(dismiss_summaries, slug, _ids(data))


@post("/api/projects/{slug:str}/plan/build")
async def build_plan_outline(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """Build the outline with a chosen approach: a plan by rule, or a draft by AI."""
    import anyio

    from pipeline.plan_approaches import build_outline

    try:
        return await anyio.to_thread.run_sync(
            build_outline, slug, str(data.get("approach", "")),
            dict(data.get("options") or {}), str(data.get("notes", "")))
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/plan/resync", sync_to_thread=False)
def resync_plan(slug: FromPath[str]) -> dict[str, Any]:
    """Bring a deck-following plan back in step with the deck, keeping its edits."""
    from pipeline.slide_plan import resync_plan_with_deck

    try:
        return resync_plan_with_deck(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/upstream", sync_to_thread=False)
def get_upstream_state(slug: FromPath[str]) -> dict[str, Any]:
    """For each layer: what changed before it since it was handed on."""
    from pipeline.upstream import upstream_state

    return upstream_state(require_project(slug))


LESSON_PLAN_ROUTES = [choose_lesson_frame, reshape_plan, write_summaries,
                      accept_summary_proposals, dismiss_summary_proposals, resync_plan,
                      build_plan_outline,
                      get_upstream_state]
