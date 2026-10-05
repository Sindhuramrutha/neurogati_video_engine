"""Assets & Design: transferring to the next layer, the slide wash, and the
brand assets (watermark, logo, intro and outro).

Its own module so `routes_project.py` does not grow; the work is in
`pipeline.assets_handoff`.
"""

from __future__ import annotations

from typing import Annotated, Any

from litestar import Request, Response, delete, get, post
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException, NotFoundException
from litestar.params import Body, FromPath
from pydantic import BaseModel

from pipeline.assets_handoff import assets_page, confirm_assets, set_slide_wash
from pipeline.brand_kit import (
    brand_file_path,
    remove_brand_file,
    set_brand_options,
    store_brand_file,
)
from pipeline.core import OperationFailed, require_project
from pipeline.project_look import choose_look
from pipeline.web.routes_project import MEDIA_TYPES_BY_SUFFIX, media_response

# An intro or outro may be WebM; the shared table only knew MP4.
MEDIA_TYPES_BY_SUFFIX.setdefault(".webm", "video/webm")
MEDIA_TYPES_BY_SUFFIX.setdefault(".m4v", "video/mp4")
MEDIA_TYPES_BY_SUFFIX.setdefault(".mov", "video/quicktime")


class WashChoice(BaseModel):
    wash: str


def _client_error(call, *args) -> dict[str, Any]:
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/assets/confirm", sync_to_thread=False)
def confirm_asset_library(slug: FromPath[str]) -> dict[str, Any]:
    """Transfer the library as it stands: later stages read this snapshot."""
    return _client_error(confirm_assets, slug)


@post("/api/projects/{slug:str}/assets/look-choice", sync_to_thread=False)
def choose_project_look(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """Which source the look follows, a colour or font role, or the background art."""
    _client_error(choose_look, slug, data)
    return assets_page(slug)


@post("/api/projects/{slug:str}/assets/pictures/{figure_id:str}", sync_to_thread=False)
def change_picture(
    slug: FromPath[str], figure_id: FromPath[str], data: dict[str, Any]
) -> dict[str, Any]:
    """Leave a picture out or put it back; draw its original or its trimmed
    copy; say its crop has been looked at."""
    from pipeline.assets import set_picture

    _client_error(set_picture, slug, figure_id, data)
    return assets_page(slug)


@post("/api/projects/{slug:str}/assets/wash", sync_to_thread=False)
def choose_slide_wash(slug: FromPath[str], data: WashChoice) -> dict[str, Any]:
    """How to read the near-opaque sheet a deck lays over its own background art."""
    return _client_error(set_slide_wash, slug, data.wash)


@post("/api/projects/{slug:str}/assets/brand/{slot:str}")
async def upload_brand_file(
    slug: FromPath[str], slot: FromPath[str],
    data: Annotated[dict[str, Any], Body(media_type=RequestEncodingType.MULTI_PART)],
) -> dict[str, Any]:
    """Put a file in one brand slot: watermark, logo, intro or outro."""
    part = next((value for value in data.values() if hasattr(value, "read")), None)
    if part is None:
        raise ClientException(detail="No file was sent.")
    content = await part.read()
    _client_error(store_brand_file, slug, slot, part.filename or "", content)
    return assets_page(slug)


@delete("/api/projects/{slug:str}/assets/brand/{slot:str}", status_code=200,
        sync_to_thread=False)
def remove_brand_slot(slug: FromPath[str], slot: FromPath[str]) -> dict[str, Any]:
    _client_error(remove_brand_file, slug, slot)
    return assets_page(slug)


@post("/api/projects/{slug:str}/assets/brand-options", sync_to_thread=False)
def choose_brand_options(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    """A logo's or watermark's placement, or an intro's or outro's trims and fade."""
    _client_error(set_brand_options, slug, data)
    return assets_page(slug)


@get("/api/projects/{slug:str}/assets/brand-files/{file_name:str}")
async def read_brand_file(slug: FromPath[str], file_name: FromPath[str],
                          request: Request) -> Response:
    path = brand_file_path(require_project(slug), file_name)
    if path is None:
        raise NotFoundException(detail=f"no such brand file: {file_name}")
    return media_response(path, request, {"x-content-type-options": "nosniff"})


@get("/api/projects/{slug:str}/assets/wash-preview/{wash:str}")
async def read_wash_preview(slug: FromPath[str], wash: FromPath[str],
                            request: Request) -> Response:
    """The deck's first slide drawn with one reading of its sheet."""
    import anyio

    from pipeline.project_look import wash_preview

    try:
        path = await anyio.to_thread.run_sync(wash_preview, slug, wash)
    except Exception as unreadable:     # a slide that cannot be drawn is a missing picture
        raise NotFoundException(
            detail=f"that slide could not be drawn: {unreadable}") from unreadable
    if path is None:
        raise NotFoundException(detail="there is no deck to draw")
    return media_response(path, request, {"x-content-type-options": "nosniff"})


@get("/api/projects/{slug:str}/assets/brand-overlays/{file_name:str}")
async def read_brand_overlay(slug: FromPath[str], file_name: FromPath[str],
                             request: Request) -> Response:
    """A finished logo or watermark, exactly as the render lays it on."""
    from pathlib import Path

    from pipeline.brand_overlay import overlay_directory

    directory = overlay_directory(require_project(slug).root).resolve()
    path = (directory / Path(file_name).name).resolve()
    if not path.is_file() or path.parent != directory:
        raise NotFoundException(detail=f"no such overlay: {file_name}")
    return media_response(path, request, {"x-content-type-options": "nosniff"})


ASSETS_HANDOFF_ROUTES = [confirm_asset_library, choose_slide_wash, choose_project_look,
                         change_picture,
                         upload_brand_file,
                         remove_brand_slot, choose_brand_options, read_brand_file,
                         read_brand_overlay, read_wash_preview]
