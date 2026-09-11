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

from litestar import Litestar, get
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.di import Provide
from litestar.response import Response
from litestar.static_files import create_static_files_router

from pipeline.web.routes_project import (
    ask_agent,
    create_project,
    delete_source,
    download_output,
    draft_plan,
    draft_section_script,
    get_agent,
    get_composition,
    get_credentials,
    get_extraction,
    get_model_status,
    get_plan,
    get_project,
    get_review,
    get_script,
    get_stage_settings,
    get_voice_providers,
    list_projects,
    list_stages,
    provide_projects,
    put_agent,
    put_composition,
    put_credentials,
    put_plan,
    put_review,
    put_script,
    put_stage_settings,
    render_project_video,
    run_extraction_route,
    seed_chapters,
    upload_source,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@get("/", sync_to_thread=False)
def index() -> Response[bytes]:
    """Served as a Response rather than litestar's File, which defaults to
    `Content-Disposition: attachment` and makes the browser download the page
    instead of rendering it."""
    return Response(
        content=(STATIC_DIR / "index.html").read_bytes(),
        media_type="text/html",
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
            get_model_status,
            get_extraction,
            run_extraction_route,
            get_voice_providers,
            render_project_video,
            download_output,
            ask_agent,
            draft_plan,
            draft_section_script,
            create_static_files_router(path="/static", directories=[STATIC_DIR]),
        ],
        dependencies={"projects": Provide(provide_projects)},
        # In place now so streaming stage progress later is a route addition
        # rather than a re-architecture. The memory backend is fine
        # single-process; swap for Redis when workers move out of process.
        plugins=[ChannelsPlugin(backend=MemoryChannelsBackend(), channels=["runs"])],
    )


app = create_app()
