"""Scripted scenes -- a folder and a `scene.py` per scene -- and the resource
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

from pipeline.core import OperationFailed
from pipeline.scene_author import (
    MAXIMUM_ATTEMPTS,
    add_resource,
    mark_scripted,
    remove_resource,
    resource_index,
    script_scene,
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
        return read_scene(slug, visual_id) | {"maximum_attempts": MAXIMUM_ATTEMPTS}
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/scenes/mark")
async def mark_scenes_scripted(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """Choose "a scripted scene" for some scenes, or (no ids) for every scene."""
    ids = data.get("visual_ids")
    changed = await _in_thread(mark_scripted, slug, ids if isinstance(ids, list) else None)
    return {"changed": changed}


@post("/api/projects/{slug:str}/scenes/{visual_id:str}/write")
async def write_scene(
    slug: FromPath[str], visual_id: FromPath[str], data: dict[str, Any]
) -> dict[str, Any]:
    """AI: write this scene's script, run it, and fix it until its checks pass."""
    return await _in_thread(script_scene, slug, visual_id, str(data.get("instruction", "")))


@post("/api/projects/{slug:str}/scenes/{visual_id:str}/run")
async def run_scene_script(
    slug: FromPath[str], visual_id: FromPath[str], data: dict[str, Any]
) -> dict[str, Any]:
    """Run the scene's script -- after saving `code`, when it is sent -- and check it."""
    if isinstance(data.get("code"), str):
        await _in_thread(save_scene_code, slug, visual_id, data["code"])
    return await _in_thread(run_scene, slug, visual_id)


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


SCENE_LAB_ROUTES = [get_scene, mark_scenes_scripted, write_scene, run_scene_script,
                    read_scene_file, get_resources, upload_resource, delete_resource]
