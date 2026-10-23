"""Scene programs -- a folder and a program per scene -- and the resource
library the scripts draw on. The work is in `pipeline.scene_lab` and
`pipeline.scene_author`.
"""

from __future__ import annotations

from typing import Annotated, Any

import anyio
from litestar import Request, Response, delete, get, post
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException, NotFoundException
from litestar.params import Body, FromPath

from pipeline import scene_agent
from pipeline.core import OperationFailed
from pipeline.scene_author import (
    add_resource,
    remove_resource,
    resource_index,
)
from pipeline.scene_lab import read_scene, run_scene, save_scene_code, scene_file
from pipeline.web.routes_project import media_response


async def _in_thread(call, *args) -> Any:
    try:
        return await anyio.to_thread.run_sync(call, *args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/scenes/{visual_id:str}", sync_to_thread=False)
def get_scene(slug: FromPath[str], visual_id: FromPath[str]) -> dict[str, Any]:
    """A scene's folder: its script, brief, checks, log and sources."""
    try:
        return read_scene(slug, visual_id) | {
            "agent": scene_agent.agent_view(slug, visual_id)}
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/scene-agents")
async def start_scene_agents(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """AI: make these scenes (`visual_ids`) on the server -- or, with no ids, every
    scene without a clip that passed. With `instruction`, a scene is changed as asked.
    `everything` remakes every scene from nothing; `fresh` remakes the ones named
    from nothing. Not before the first section's storyboard is approved: it sets the
    style every scene follows."""
    from pipeline.operations import require_project as _project
    from pipeline.storyboard import gate

    reason = gate(_project(slug))
    if reason:
        raise ClientException(detail=reason)
    ids = data.get("visual_ids")
    fresh = bool(data.get("everything") or data.get("fresh"))
    if data.get("everything"):
        from pipeline.generation import VisualPlanStore
        from pipeline.operations import require_project

        ids = [v.id for v in VisualPlanStore(require_project(slug).root).load().visuals]
    elif not isinstance(ids, list) or not ids:
        from pipeline.generation import VisualPlanStore
        from pipeline.operations import require_project

        plan = VisualPlanStore(require_project(slug).root).load()
        ids = [v.id for v in plan.visuals if not v.clip_path]
    return await _in_thread(lambda: scene_agent.start(
        slug, [str(i) for i in ids], instruction=str(data.get("instruction", "")),
        fresh=fresh))


@get("/api/projects/{slug:str}/scene-agents", sync_to_thread=False)
def scene_agents(slug: FromPath[str]) -> dict[str, Any]:
    """Every scene's agent at a glance."""
    try:
        return scene_agent.queue_view(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/scene-agents/stop")
async def stop_all_scene_agents(slug: FromPath[str]) -> dict[str, Any]:
    """Stop every scene's agent: the queue is dropped, working ones stop after a step."""
    return await _in_thread(scene_agent.stop_all, slug)


@post("/api/projects/{slug:str}/scenes/{visual_id:str}/agent/stop")
async def stop_scene_agent(slug: FromPath[str], visual_id: FromPath[str]) -> dict[str, Any]:
    """Stop this scene's agent after the step it is on."""
    return await _in_thread(scene_agent.stop, slug, visual_id)


@post("/api/projects/{slug:str}/scenes/{visual_id:str}/run")
async def run_scene_script(
    slug: FromPath[str], visual_id: FromPath[str], data: dict[str, Any]
) -> dict[str, Any]:
    """Run the scene's script -- after saving `code`, when it is sent -- and check it."""
    if isinstance(data.get("code"), str):
        await _in_thread(save_scene_code, slug, visual_id, data["code"])
    return await _in_thread(run_scene, slug, visual_id)


@post("/api/projects/{slug:str}/scenes/{visual_id:str}/approve")
async def approve_scene_program(
    slug: FromPath[str], visual_id: FromPath[str], data: dict[str, Any]
) -> dict[str, Any]:
    """A person watched the preview: approve the scene's program, or take it back."""
    from pipeline.scene_approval import approve_scene

    return await _in_thread(approve_scene, slug, visual_id, bool(data.get("approved", True)))


@post("/api/projects/{slug:str}/scenes/approve-passed")
async def approve_passed_programs(slug: FromPath[str]) -> dict[str, Any]:
    """Approve every scene whose program passed every check, in one go."""
    from pipeline.scene_approval import approve_passed

    return await _in_thread(approve_passed, slug)


@get("/api/projects/{slug:str}/scenes/{visual_id:str}/files/{name:str}")
async def read_scene_file(
    slug: FromPath[str], visual_id: FromPath[str], name: FromPath[str], request: Request
) -> Response:
    try:
        path = scene_file(slug, visual_id, name)
    except OperationFailed:
        path = None
    if path is None:
        raise NotFoundException(detail=f"no such scene file: {name}")
    return media_response(path, request, {"x-content-type-options": "nosniff",
                                          "cache-control": "no-store"})


@get("/api/resources", sync_to_thread=False)
def get_resources() -> dict[str, Any]:
    """The resource library every scene script can draw on."""
    return resource_index()


@post("/api/resources/{kind:str}")
async def upload_resource(
    kind: FromPath[str],
    data: Annotated[dict[str, Any], Body(media_type=RequestEncodingType.MULTI_PART)],
) -> dict[str, Any]:
    part = next((value for value in data.values() if hasattr(value, "read")), None)
    if part is None:
        raise ClientException(detail="No file was sent.")
    try:
        return add_resource(kind, part.filename or "", await part.read())
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@delete("/api/resources/{kind:str}/{file_name:str}", status_code=200, sync_to_thread=False)
def delete_resource(kind: FromPath[str], file_name: FromPath[str]) -> dict[str, Any]:
    try:
        return remove_resource(kind, file_name)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


SCENE_LAB_ROUTES = [get_scene, start_scene_agents, scene_agents,
                    stop_scene_agent, stop_all_scene_agents, run_scene_script,
                    approve_scene_program, approve_passed_programs,
                    read_scene_file, get_resources, upload_resource, delete_resource]
