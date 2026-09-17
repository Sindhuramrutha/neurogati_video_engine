"""Litestar application.

Litestar over FastAPI for three specific reasons (docs/design/tech-stack.md):
real dependency injection, first-class channels for streaming stage progress to
the UI, and Pydantic-native DTOs matching the IR.

The app is deliberately thin. It serves the pipeline surface and its routes; no
pipeline logic lives here. That boundary is the point: the UI is a client, never
the place work happens.
"""

from __future__ import annotations

from pathlib import Path

from litestar import Litestar, Request, get
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.di import Provide
from litestar.response import Response
from litestar.static_files import create_static_files_router
from litestar.status_codes import HTTP_413_REQUEST_ENTITY_TOO_LARGE

from pipeline.sources import (
    MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES,
    MAXIMUM_UPLOAD_REQUEST_SIZE_IN_BYTES,
)
from pipeline.web.routes_project import (
    accept_plan_draft_route,
    acknowledge_extraction_finding,
    ask_agent,
    ask_orchestrator,
    confirm_plan_route,
    confirm_section_narration_route,
    create_project,
    delete_agent_conversation,
    delete_source,
    discard_plan_draft_route,
    download_narration,
    download_output,
    draft_plan,
    draft_section_script,
    draft_unwritten_script_sections,
    get_agent,
    get_agent_conversation,
    get_composition,
    get_credentials,
    get_extraction,
    get_extraction_review,
    get_model_status,
    get_plan,
    get_plan_draft,
    get_project,
    get_review,
    get_script,
    get_section_source,
    get_stage_settings,
    get_voice_providers,
    list_agent_conversations,
    list_projects,
    list_stages,
    preview_source_file,
    provide_projects,
    put_agent,
    put_composition,
    put_credentials,
    put_extraction_sources,
    put_plan,
    put_review,
    put_script,
    put_stage_settings,
    read_extracted_asset,
    read_source_file,
    render_project_video,
    replace_extracted_figure,
    review_extraction_route,
    run_extraction_route,
    seed_chapters,
    upload_source,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@get(["/", "/{stage:str}", "/{stage:str}/{slug:str}"], sync_to_thread=False)
def index() -> Response:
    """The page, at every address a stage can have.

    `/planning/demystifying-the-brain` is a real URL: it can be bookmarked,
    pasted to someone, and reloaded without losing your place. The same document
    is returned for all of them and the page reads the path on boot -- the
    alternative, a single address for six stages, means a reload always lands
    you back on the first one.

    Unknown paths still return the page rather than a 404, because the stage list
    lives in `stages.py` and a router that also knew it would be a second place
    to keep in step.

    The segments are deliberately not parameters: this handler returns the same
    bytes for every address, and the page reads its own path on boot. Declaring
    them would only be a second reader of the same thing.
    """
    return Response(
        content=(STATIC_DIR / "index.html").read_bytes(),
        media_type="text/html",
    )


def _too_large(request: Request, exception: Exception) -> Response:
    """Say what the limit is, rather than "Request Entity Too Large".

    A framework 413 arrives before any handler runs, so the only place this can
    be explained is here. The message names the per-file limit, because that is
    the number a person can act on.
    """
    limit_in_megabytes = MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES // (1024 * 1024)
    return Response(
        status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        content={
            "status_code": HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            "detail": (
                f"That upload is too large for one request. Each file may be up "
                f"to {limit_in_megabytes} MB; try adding fewer files at a time."
            ),
        },
    )


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[
            index,
            list_stages,
            list_projects,
            create_project,
            get_project,
            upload_source,
            delete_source,
            get_agent,
            put_agent,
            get_stage_settings,
            put_stage_settings,
            get_plan,
            put_plan,
            get_script,
            put_script,
            get_composition,
            put_composition,
            get_review,
            put_review,
            seed_chapters,
            get_credentials,
            put_credentials,
            put_extraction_sources,
            get_model_status,
            get_extraction,
            run_extraction_route,
            review_extraction_route,
            get_extraction_review,
            acknowledge_extraction_finding,
            replace_extracted_figure,
            get_voice_providers,
            render_project_video,
            download_output,
            download_narration,
            read_extracted_asset,
            read_source_file,
            preview_source_file,
            accept_plan_draft_route,
            ask_agent,
            confirm_plan_route,
            discard_plan_draft_route,
            get_plan_draft,
            ask_orchestrator,
            list_agent_conversations,
            get_agent_conversation,
            delete_agent_conversation,
            draft_plan,
            draft_section_script,
            draft_unwritten_script_sections,
            get_section_source,
            confirm_section_narration_route,
            create_static_files_router(path="/static", directories=[STATIC_DIR]),
        ],
        # Litestar's own default is 10 MB, which refused a single ordinary
        # 50-slide deck with "Request Entity Too Large" before any of this
        # application's checks could run. Uploads stream to disk, so this bounds
        # the request rather than memory.
        request_max_body_size=MAXIMUM_UPLOAD_REQUEST_SIZE_IN_BYTES,
        exception_handlers={HTTP_413_REQUEST_ENTITY_TOO_LARGE: _too_large},
        dependencies={"projects": Provide(provide_projects)},
        # In place now so streaming stage progress later is a route addition
        # rather than a re-architecture. The memory backend is fine
        # single-process; swap for Redis when workers move out of process.
        plugins=[ChannelsPlugin(backend=MemoryChannelsBackend(), channels=["runs"])],
    )


app = create_app()
