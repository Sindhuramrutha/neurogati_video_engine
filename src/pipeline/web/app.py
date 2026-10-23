"""Litestar application.

Litestar over FastAPI for three specific reasons: real dependency injection,
first-class channels for streaming stage progress to the UI, and Pydantic-native
DTOs for the artifacts.

The app is deliberately thin. It serves the pipeline surface and its routes; no
pipeline logic lives here. That boundary is the point: the UI is a client, never
the place work happens.
"""

from __future__ import annotations

from pathlib import Path

from litestar import Litestar, Request, get
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.datastructures import CacheControlHeader
from litestar.di import Provide
from litestar.response import Response
from litestar.static_files import create_static_files_router
from litestar.status_codes import HTTP_413_REQUEST_ENTITY_TOO_LARGE

from pipeline.config import use_work_dir
from pipeline.sources import (
    MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES,
    MAXIMUM_UPLOAD_REQUEST_SIZE_IN_BYTES,
)
from pipeline.web.routes_assets_handoff import ASSETS_HANDOFF_ROUTES
from pipeline.web.routes_chosen import CHOSEN_ROUTES
from pipeline.web.routes_doctor import DOCTOR_ROUTES
from pipeline.web.routes_extraction_agent import EXTRACTION_AGENT_ROUTES
from pipeline.web.routes_generation_handoff import GENERATION_HANDOFF_ROUTES
from pipeline.web.routes_lesson_plan import LESSON_PLAN_ROUTES
from pipeline.web.routes_plan_handoff import PLAN_HANDOFF_ROUTES
from pipeline.web.routes_project import (
    acknowledge_extraction_finding,
    ask_orchestrator,
    build_project_export,
    clear_studio_timeline,
    confirm_extraction_route,
    confirm_section_narration_route,
    create_project,
    decide_asset_figure,
    delete_agent_conversation,
    delete_source_pages,
    download_export_file,
    download_narration,
    download_output,
    draft_section_script,
    draft_unwritten_script_sections,
    draw_extracted_figure,
    get_agent,
    get_agent_conversation,
    get_asset_library,
    get_composition,
    get_credentials,
    get_export,
    get_extraction,
    get_extraction_review,
    get_plan,
    get_project,
    get_review,
    get_scene_visuals,
    get_script,
    get_stage_settings,
    get_voice_providers,
    list_agent_conversations,
    list_projects,
    list_stages,
    plan_scene_visuals,
    preview_source_file,
    provide_projects,
    put_agent,
    put_composition,
    put_credentials,
    put_plan,
    put_review,
    put_script,
    put_stage_settings,
    read_extracted_asset,
    read_prepared_asset,
    read_source_file,
    refresh_assets,
    render_project_video,
    replace_extracted_figure,
    review_extraction_route,
    run_extraction_route,
    seed_chapters,
    set_asset_look,
)
from pipeline.web.routes_project_admin import PROJECT_ADMIN_ROUTES
from pipeline.web.routes_render_job import RENDER_JOB_ROUTES
from pipeline.web.routes_scene_lab import SCENE_LAB_ROUTES
from pipeline.web.routes_script_handoff import SCRIPT_HANDOFF_ROUTES
from pipeline.web.routes_source import SOURCE_ROUTES
from pipeline.web.routes_storyboard import STORYBOARD_ROUTES
from pipeline.web.routes_video_setup import VIDEO_SETUP_ROUTES

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
    use_work_dir()
    return Litestar(
        route_handlers=[
            index,
            *EXTRACTION_AGENT_ROUTES,
            *RENDER_JOB_ROUTES,
            *CHOSEN_ROUTES,
            *PROJECT_ADMIN_ROUTES,
            *DOCTOR_ROUTES,
            *ASSETS_HANDOFF_ROUTES,
            *PLAN_HANDOFF_ROUTES,
            *LESSON_PLAN_ROUTES,
            *SCENE_LAB_ROUTES,
            *SCRIPT_HANDOFF_ROUTES,
            *GENERATION_HANDOFF_ROUTES,
            *VIDEO_SETUP_ROUTES,
            *STORYBOARD_ROUTES,
            list_stages,
            list_projects,
            create_project,
            get_project,
            *SOURCE_ROUTES,
            delete_source_pages,
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
            confirm_extraction_route,
            get_extraction,
            run_extraction_route,
            clear_studio_timeline,
            review_extraction_route,
            get_extraction_review,
            acknowledge_extraction_finding,
            replace_extracted_figure,
            draw_extracted_figure,
            get_asset_library,
            refresh_assets,
            decide_asset_figure,
            set_asset_look,
            get_export,
            build_project_export,
            download_export_file,
            get_scene_visuals,
            plan_scene_visuals,
            get_voice_providers,
            render_project_video,
            download_output,
            download_narration,
            read_extracted_asset,
            read_prepared_asset,
            read_source_file,
            preview_source_file,
            ask_orchestrator,
            list_agent_conversations,
            get_agent_conversation,
            delete_agent_conversation,
            draft_section_script,
            draft_unwritten_script_sections,
            confirm_section_narration_route,
            # no-cache: the browser asks every time (a 304 when unchanged). Without
            # it a browser reused an old module after an update and showed an old page.
            create_static_files_router(path="/static", directories=[STATIC_DIR],
                                      cache_control=CacheControlHeader(no_cache=True)),
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
