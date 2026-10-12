"""Project and stage routes — what the six tabs talk to.

Thin by design. These read and write files; no pipeline logic lives here. When the
graph exists, run endpoints will submit to it and stream progress over the channels
plugin already wired into the app.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, Any

from litestar import Request, Response, delete, get, post
from litestar.di import NamedDependency
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException, NotFoundException
from litestar.params import Body, FromPath
from pydantic import BaseModel

from pipeline.agent_runtime import (
    draft_section_script_with_agent,
)
from pipeline.agents import AgentRegistry
from pipeline.assets_handoff import assets_page
from pipeline.composition import Composition, CompositionStore
from pipeline.config import REPO_ROOT, get_settings
from pipeline.credentials import describe_credentials, save_credentials
from pipeline.deck_edit import delete_pages
from pipeline.extraction_review import (
    acknowledge_finding,
    generate_figure,
    read_extraction_review,
    replace_figure,
    review_extraction,
)
from pipeline.generation import (
    plan_visuals,
    read_visuals,
)
from pipeline.operations import (
    OperationFailed,
    build_export,
    clear_timeline,
    confirm_extraction,
    confirm_section_narration,
    decide_figure,
    extraction_page,
    list_voice_providers,
    present_artifact,
    preview_source,
    read_export,
    refresh_asset_library,
    render_video,
    run_extraction,
    save_artifact,
    set_project_look,
)
from pipeline.orchestrator import (
    ask_the_orchestrator,
    forget_conversation,
    list_conversations,
    read_conversation,
)
from pipeline.planning import Plan, PlanStore
from pipeline.projects import Project, ProjectStore
from pipeline.review import Review, ReviewStore, chapters_from_plan
from pipeline.scripting import Script, ScriptStore
from pipeline.sources import (
    reduce_to_bare_file_name,
)
from pipeline.stage_options import StageSettingsStore
from pipeline.stages import STAGES, Stage, downstream_of

AGENTS_DIR = REPO_ROOT / "agents"

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self) -> None:
        self.store = ProjectStore(get_settings().projects_dir)

    def require(self, slug: str) -> Project:
        p = self.store.get(slug)
        if p is None:
            raise NotFoundException(detail=f"no such project: {slug}")
        return p

    def registry(self, project: Project | None = None) -> AgentRegistry:
        return AgentRegistry(AGENTS_DIR, project.root if project else None)


_service: ProjectService | None = None


async def provide_projects() -> ProjectService:
    global _service
    if _service is None:
        _service = ProjectService()
    return _service


class NewProject(BaseModel):
    name: str


class AgentEdit(BaseModel):
    body: str


class StageSettingsEdit(BaseModel):
    values: dict[str, Any]


class DrawingInstruction(BaseModel):
    # Optional steer, e.g. "show the three stages side by side".
    instruction: str = ""


class FigureDecision(BaseModel):
    # "use", "skip" or "undecided". A string rather than an enum so the same
    # body works from curl and from the page without a schema lookup.
    use: str = "undecided"
    note: str | None = None


class LookChoice(BaseModel):
    use_source_styling: bool = False


class AgentQuestion(BaseModel):
    question: str
    # Empty starts a new thread. The panel sends the id of the conversation it
    # has open, so the Orchestrator is told what was already said.
    conversation_id: str = ""


class ExtractionTarget(BaseModel):
    file_name: str = ""     # the project's source when empty


class PageDeletion(BaseModel):
    pages: list[int]    # 1-based, as the page strip numbers them


class UnwrittenSectionsInstruction(BaseModel):
    instruction: str = ""


class SectionScriptInstruction(BaseModel):
    section_id: str
    instruction: str = ""


class RenderRequest(BaseModel):
    voice_provider: str = ""
    voice: str = ""
    resume: bool = False  # continue the stopped render instead of starting over


class CredentialsEdit(BaseModel):
    """Only the fields being changed. A field left out keeps its stored value,
    which is what lets the panel save without ever having received the secret
    it is not editing."""

    values: dict[str, str]


@get("/api/stages", sync_to_thread=False)
def list_stages() -> list[dict[str, Any]]:
    """The tab definitions. Served rather than duplicated in the frontend so the UI
    cannot show a stage the pipeline does not have."""
    return [
        {
            "key": s.key.value,
            "title": s.title,
            "blurb": s.blurb,
            "has_agent": s.has_agent,
            "color": s.color,
            "produces": s.produces,
        }
        for s in STAGES
    ]


@get("/api/projects", sync_to_thread=False)
def list_projects(projects: NamedDependency[ProjectService]) -> list[dict[str, Any]]:
    return [p.to_dict() for p in projects.store.list()]


@post("/api/projects", sync_to_thread=False)
def create_project(
    data: NewProject, projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    name = data.name.strip()
    if not name:
        raise ClientException(detail="project name is required")
    try:
        return projects.store.create(name).to_dict()
    except ValueError as exc:
        raise ClientException(detail=str(exc)) from exc


@get("/api/projects/{slug:str}", sync_to_thread=False)
def get_project(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    return projects.require(slug).to_dict()


@get("/api/projects/{slug:str}/agent/{stage:str}", sync_to_thread=False)
def get_agent(
    slug: FromPath[str], stage: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    project = projects.require(slug)
    try:
        stage_key = Stage(stage)
    except ValueError as exc:
        raise NotFoundException(detail=f"no such stage: {stage}") from exc

    agent = projects.registry(project).get(stage_key)
    if agent is None:
        raise NotFoundException(detail=f"no agent for stage: {stage}")
    # Editing an agent invalidates every later stage -- surfaced so the UI can
    # warn before an edit silently orphans downstream work.
    return agent.to_dict() | {
        "invalidates": [s.value for s in downstream_of(stage_key)],
    }


@post("/api/projects/{slug:str}/agent/{stage:str}", sync_to_thread=False)
def put_agent(
    slug: FromPath[str],
    stage: FromPath[str],
    data: AgentEdit,
    projects: NamedDependency[ProjectService],
) -> dict[str, Any]:
    project = projects.require(slug)
    try:
        stage_key = Stage(stage)
    except ValueError as exc:
        raise NotFoundException(detail=f"no such stage: {stage}") from exc

    path = projects.registry(project).write_override(stage_key, data.body)
    return {
        "ok": True,
        "path": str(path),
        "source": "project",
        "invalidates": [s.value for s in downstream_of(stage_key)],
    }


def _stage_from_path(stage: str) -> Stage:
    """Coerce a URL segment to a Stage, or 404.

    Shared by every stage-scoped route so an unknown stage fails the same way
    everywhere rather than as a ValueError from whichever handler ran first.
    """
    try:
        return Stage(stage)
    except ValueError as unknown_stage:
        raise NotFoundException(detail=f"no such stage: {stage}") from unknown_stage


@get("/api/projects/{slug:str}/settings/{stage:str}", sync_to_thread=False)
def get_stage_settings(
    slug: FromPath[str], stage: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    project = projects.require(slug)
    stage_key = _stage_from_path(stage)
    return StageSettingsStore(project.root).load(stage_key).to_dict()


@post("/api/projects/{slug:str}/settings/{stage:str}", sync_to_thread=False)
def put_stage_settings(
    slug: FromPath[str],
    stage: FromPath[str],
    data: StageSettingsEdit,
    projects: NamedDependency[ProjectService],
) -> dict[str, Any]:
    project = projects.require(slug)
    stage_key = _stage_from_path(stage)
    return StageSettingsStore(project.root).save(stage_key, data.values).to_dict()


@get("/api/projects/{slug:str}/plan", sync_to_thread=False)
def get_plan(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    project = projects.require(slug)
    return present_artifact(project, "plan", PlanStore(project.root).load())


@post("/api/projects/{slug:str}/plan", sync_to_thread=False)
def put_plan(
    slug: FromPath[str], data: Plan, projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """Replace the whole plan.

    Whole-document rather than per-field patches: the outline is edited as one
    thing (reorder, retitle, delete in one gesture), and a patch API would need a
    conflict story for a document only one operator edits at a time.

    `data` is a validated `Plan`, so titles are trimmed, durations clamped and the
    section count capped before anything reaches disk -- the request cannot store
    a shape the rest of the pipeline would then have to defend against.
    """
    projects.require(slug)  # 404 before anything is written
    return save_artifact(slug, "plan", data)


@get("/api/projects/{slug:str}/script", sync_to_thread=False)
def get_script(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """The script, audited against the plan it belongs to.

    The plan is loaded here rather than by the client so the cross-document
    checks -- orphaned narration, unwritten sections -- are computed in one place
    and cannot disagree between callers.
    """
    project = projects.require(slug)
    return present_artifact(project, "script", ScriptStore(project.root).load())


@post("/api/projects/{slug:str}/script", sync_to_thread=False)
def put_script(
    slug: FromPath[str], data: Script, projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    projects.require(slug)  # 404 before anything is written
    return save_artifact(slug, "script", data)


@get("/api/projects/{slug:str}/composition", sync_to_thread=False)
def get_composition(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    # Through `present_artifact`, like every other artifact: the timeline cannot
    # be judged on its own -- whether it still matches the plan it was built
    # from is the difference between a finished cut and an abandoned one.
    project = projects.require(slug)
    return present_artifact(project, "composition", CompositionStore(project.root).load())


@post("/api/projects/{slug:str}/composition", sync_to_thread=False)
def put_composition(
    slug: FromPath[str], data: Composition, projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """Replace the whole timeline.

    `data` is a validated `Composition`, so clip durations are clamped above the
    minimum grabbable size and the track/clip counts are capped before anything
    reaches disk. A drag that produced a zero-length clip cannot persist one.
    """
    projects.require(slug)  # 404 before anything is written
    return save_artifact(slug, "composition", data)


@get("/api/projects/{slug:str}/review", sync_to_thread=False)
def get_review(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """The review log, plus the material a reviewer needs beside it.

    The plan's sections come along so chapters can be seeded from them, and the
    script's narration so the transcript pane has something to show before any
    audio exists. Assembled here rather than by three client requests, so the
    reviewer never sees a half-populated page.
    """
    project = projects.require(slug)
    return present_artifact(project, "review", ReviewStore(project.root).load())


@post("/api/projects/{slug:str}/review", sync_to_thread=False)
def put_review(
    slug: FromPath[str], data: Review, projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    projects.require(slug)  # 404 before anything is written
    return save_artifact(slug, "review", data)


@post("/api/projects/{slug:str}/review/seed-chapters", sync_to_thread=False)
def seed_chapters(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """Replace chapters with ones derived from the plan.

    Explicitly destructive and explicitly invoked: seeding automatically on load
    would silently discard hand-edited chapter titles every time the page opened.
    """
    from pipeline.plan_handoff import plan_for_later_stages
    project = projects.require(slug)
    plan = plan_for_later_stages(project)
    store = ReviewStore(project.root)

    review = store.load()
    review.chapters = chapters_from_plan([
        {"title": s.title, "estimated_seconds": s.estimated_seconds}
        for s in plan.sections
    ])
    return store.save(review).to_dict()


# --- credentials ------------------------------------------------------------
#
# Not project-scoped: a key belongs to the installation, not to one video. Both
# handlers go through pipeline.credentials, which is the only module allowed to
# touch a secret -- and which returns masks, never values.


@get("/api/credentials", sync_to_thread=False)
def get_credentials() -> dict[str, Any]:
    """Status of every credential field. Secrets come back masked.

    There is deliberately no route that returns a key in the clear. If one is
    ever needed, it is a redesign, not a parameter.
    """
    return describe_credentials()


@post("/api/credentials", sync_to_thread=False)
def put_credentials(data: CredentialsEdit) -> dict[str, Any]:
    """Write submitted values to .env and return the refreshed, masked status."""
    return save_credentials(data.values)


# --- running agents ---------------------------------------------------------


@post("/api/projects/{slug:str}/orchestrator/ask")
async def ask_orchestrator(slug: FromPath[str], data: AgentQuestion) -> dict[str, Any]:
    """Ask the master agent. It decides which stage agents to put to work.

    Deliberately at `/orchestrator/ask` rather than `/agent/ask`: the latter has
    a literal `ask` sitting exactly where `/agent/{stage}` expects a parameter,
    which is the same shadowing that once made `planning` the one stage unable to
    reach its own agent. A separate noun makes the collision impossible instead
    of merely absent.

    Slower than a single stage agent by design -- it may run several of them --
    so it goes off the event loop like the rest of the model calls.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(
            ask_the_orchestrator, slug, data.question, data.conversation_id
        )
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/conversations", sync_to_thread=False)
def list_agent_conversations(slug: FromPath[str]) -> dict[str, Any]:
    """Every thread with the Orchestrator for this project, newest first."""
    try:
        return list_conversations(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/conversations/{conversation_id:str}", sync_to_thread=False)
def get_agent_conversation(
    slug: FromPath[str], conversation_id: FromPath[str]
) -> dict[str, Any]:
    """One thread in full, to reopen and continue."""
    try:
        return read_conversation(slug, conversation_id)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@delete(
    "/api/projects/{slug:str}/conversations/{conversation_id:str}",
    status_code=200, sync_to_thread=False,
)
def delete_agent_conversation(
    slug: FromPath[str], conversation_id: FromPath[str]
) -> dict[str, Any]:
    """Forget one thread. Nothing the project produced is touched."""
    try:
        return forget_conversation(slug, conversation_id)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/extraction", sync_to_thread=True)
def get_extraction(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """The extraction collection, with where it stands against the files and
    against what later stages were last given."""
    return extraction_page(projects.require(slug))


@post("/api/projects/{slug:str}/extraction/run")
async def run_extraction_route(slug: FromPath[str], data: ExtractionTarget) -> dict[str, Any]:
    """Extract the project's source file. The result replaces the last one.

    Off the event loop: a large PDF takes real time to parse, and blocking the
    loop would freeze the rest of the app while one project extracted.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(run_extraction, slug, data.file_name)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/extraction/confirm", sync_to_thread=True)
def confirm_extraction_route(slug: FromPath[str]) -> dict[str, Any]:
    """Hand the collection to later stages -- the only step that changes what they read."""
    try:
        return confirm_extraction(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/script/draft")
async def draft_section_script(
    slug: FromPath[str], data: SectionScriptInstruction
) -> dict[str, Any]:
    """Write narration for one plan section and save it.

    Unlike the plan draft this one writes, because narration is addressed by
    section id: it replaces one section's words and leaves the rest of the script
    untouched.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(
            draft_section_script_with_agent, slug, data.section_id, data.instruction
        )
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/script/draft-unwritten")
async def draft_unwritten_script_sections(
    slug: FromPath[str], data: UnwrittenSectionsInstruction
) -> dict[str, Any]:
    """Draft every section that has no narration yet, at the same time.

    Never replaces narration already written. Off the event loop: it is one model
    call per section.
    """
    import anyio

    from pipeline.script_drafting import draft_unwritten_sections

    try:
        return await anyio.to_thread.run_sync(draft_unwritten_sections, slug, data.instruction)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/script/sections/{section_id:str}/confirm", sync_to_thread=False)
def confirm_section_narration_route(
    slug: FromPath[str], section_id: FromPath[str]
) -> dict[str, Any]:
    """Record that a section's narration still matches its plan section and source."""
    try:
        return confirm_section_narration(slug, section_id)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/extraction/review")
async def review_extraction_route(slug: FromPath[str]) -> dict[str, Any]:
    """Check every extracted picture and figure reference. Off the event loop:
    it opens a few hundred images."""
    import anyio

    try:
        return await anyio.to_thread.run_sync(review_extraction, slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/extraction/review", sync_to_thread=False)
def get_extraction_review(slug: FromPath[str]) -> dict[str, Any]:
    """The last review, with whether it is out of date."""
    try:
        return read_extraction_review(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post(
    "/api/projects/{slug:str}/extraction/findings/{finding_id:str}/acknowledge",
    sync_to_thread=False,
)
def acknowledge_extraction_finding(
    slug: FromPath[str], finding_id: FromPath[str]
) -> dict[str, Any]:
    """Record that a finding has been looked at, so it stops being reported."""
    try:
        return acknowledge_finding(slug, finding_id)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/extraction/figures/{block_id:str}/picture")
async def replace_extracted_figure(
    slug: FromPath[str],
    block_id: FromPath[str],
    data: Annotated[dict[str, Any], Body(media_type=RequestEncodingType.MULTI_PART)],
) -> dict[str, Any]:
    """Put a picture the person supplies where the extracted one should have been."""
    uploaded = next(iter(data.values()), None)
    if uploaded is None:
        raise ClientException(detail="No file was sent.")

    file_name = getattr(uploaded, "filename", "") or "replacement.png"
    content = await uploaded.read()
    try:
        return replace_figure(slug, block_id, content, Path(file_name).suffix or ".png")
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/extraction/figures/{block_id:str}/draw")
async def draw_extracted_figure(
    slug: FromPath[str], block_id: FromPath[str], data: DrawingInstruction
) -> dict[str, Any]:
    """Draw a replacement for a figure that did not extract.

    The result is recorded as generated rather than swapped in quietly:
    everything else in a project comes from the source documents, and a drawn
    picture is the one thing that does not.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(
            generate_figure, slug, block_id, data.instruction
        )
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/composition/clear", sync_to_thread=False)
def clear_studio_timeline(slug: FromPath[str]) -> dict[str, Any]:
    """Empty the timeline so the next render builds it from the current script.

    The hand-edit protection refuses to overwrite a timeline someone has worked
    on, which is right -- but without this the only way out was deleting clips
    one at a time, and a timeline from an abandoned script survived four renders
    that way.
    """
    try:
        return clear_timeline(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/assets", sync_to_thread=False)
def get_asset_library(slug: FromPath[str]) -> dict[str, Any]:
    """Every picture, what was decided about it, the rules, and the hand-off state."""
    try:
        return assets_page(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/assets/refresh", sync_to_thread=False)
def refresh_assets(slug: FromPath[str], clear: bool = False) -> dict[str, Any]:
    """Gather the pictures the transferred extraction has, keeping every decision --
    or, with `clear`, forgetting every picture and decision first."""
    try:
        return refresh_asset_library(slug, clear=clear)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/assets/figures/{figure_id:str}", sync_to_thread=False)
def decide_asset_figure(
    slug: FromPath[str], figure_id: FromPath[str], data: FigureDecision
) -> dict[str, Any]:
    """Say whether a picture should be used, and why."""
    try:
        return decide_figure(slug, figure_id, data.use, data.note)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/assets/look", sync_to_thread=False)
def set_asset_look(slug: FromPath[str], data: LookChoice) -> dict[str, Any]:
    """Whether the video follows the source deck's colours and fonts."""
    try:
        return set_project_look(slug, data.use_source_styling)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/export", sync_to_thread=False)
def get_export(slug: FromPath[str]) -> dict[str, Any]:
    """The last export, with today's blockers rather than the ones it was built with."""
    try:
        return read_export(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/export", sync_to_thread=False)
def build_project_export(slug: FromPath[str]) -> dict[str, Any]:
    """Write the transcript, chapters and description, and list what is ready."""
    try:
        return build_export(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/export/files/{file_name:str}", sync_to_thread=False)
def download_export_file(slug: FromPath[str], file_name: FromPath[str]) -> Response:
    """One exported file, by name.

    The name is reduced to a bare file name before it is joined, so a crafted
    request cannot walk out of the export folder.
    """
    project = ProjectStore(get_settings().projects_dir).get(slug)
    if project is None:
        raise NotFoundException(detail=f"no such project: {slug}")

    path = project.root / "export" / reduce_to_bare_file_name(file_name)
    if not path.is_file():
        raise NotFoundException(detail=f"no exported file named {file_name}")
    return Response(
        content=path.read_bytes(),
        media_type=MEDIA_TYPES_BY_SUFFIX.get(path.suffix.lower(), "text/plain"),
        headers={"Content-Disposition": f'attachment; filename="{path.name}"'},
    )


@get("/api/projects/{slug:str}/visuals", sync_to_thread=False)
def get_scene_visuals(slug: FromPath[str]) -> dict[str, Any]:
    """What each scene shows, and which scenes were rewritten since."""
    try:
        return read_visuals(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/visuals/plan", sync_to_thread=False)
def plan_scene_visuals(slug: FromPath[str]) -> dict[str, Any]:
    """Decide what every scene shows. Calls no model and produces no picture."""
    try:
        return plan_visuals(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/voices", sync_to_thread=False)
def get_voice_providers() -> dict[str, Any]:
    """Every text-to-speech provider, with whether it is usable right now."""
    return list_voice_providers()


@post("/api/projects/{slug:str}/render")
async def render_project_video(
    slug: FromPath[str], data: RenderRequest
) -> dict[str, Any]:
    """Synthesise narration and render the video.

    Long-running and off the event loop: synthesis is a network round trip per
    section and ffmpeg is a subprocess, so this would otherwise block every
    other request for the length of a render.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(
            render_video, slug, data.voice_provider, data.voice, data.resume
        )
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


MEDIA_TYPES_BY_SUFFIX = {
    ".pdf": "application/pdf",
    ".md": "text/plain",
    ".txt": "text/plain",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".mp4": "video/mp4",
    ".vtt": "text/vtt",
    ".srt": "text/plain",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    # Figures pulled out of the source documents.
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".svg": "image/svg+xml",
}

# Big enough that a 9 MB video is a handful of reads, small enough that a seek
# does not pull megabytes nobody watches.
MEDIA_CHUNK_SIZE = 1 << 20


def parse_range_header(range_header: str, file_size: int) -> tuple[int, int] | None:
    """Parse a single `bytes=start-end` range. None if it is absent or unusable.

    Only the single-range form is handled, which is all a media element sends.
    A malformed or unsatisfiable range returns None so the caller falls back to
    a normal 200 -- refusing outright would break playback over a header the
    client can survive without.
    """
    if not range_header or not range_header.strip().lower().startswith("bytes="):
        return None

    specifier = range_header.split("=", 1)[1].split(",")[0].strip()
    start_text, _, end_text = specifier.partition("-")

    try:
        if not start_text:
            # A suffix range: the last N bytes.
            length = int(end_text)
            if length <= 0:
                return None
            return max(0, file_size - length), file_size - 1

        start = int(start_text)
        end = int(end_text) if end_text else file_size - 1
    except ValueError:
        return None

    end = min(end, file_size - 1)
    if start > end or start >= file_size:
        return None
    return start, end


def resolve_output_file(project: Project, file_name: str, subdirectory: str = "") -> Path:
    """The requested file, or a 404 -- never a path outside the output directory.

    The name is reduced to a bare name *and* the resolved path is re-checked
    against the directory: the same belt-and-braces as uploads, because this is
    the identical hole pointing the other way. `subdirectory` is chosen by the
    route, never by the request.
    """
    output_directory = (project.root / "reviewing" / "output" / subdirectory).resolve()
    candidate = (output_directory / reduce_to_bare_file_name(file_name)).resolve()

    if not candidate.is_file() or output_directory not in candidate.parents:
        raise NotFoundException(detail=f"no such output file: {file_name}")
    return candidate


def media_response(
    candidate: Path, request: Request, extra_headers: dict[str, str] | None = None
) -> Response:
    """A file response that answers HTTP Range requests.

    **Range is the whole point.** A flat 200 means no `Accept-Ranges` and no 206,
    so a `<video>` or `<audio>` element cannot seek and refuses to start --
    the file is fine and the player shows nothing.

    `inline` is the other half: `attachment` downloads the file instead of
    playing it, the same trap that once made this app download its own index.
    """
    file_size = candidate.stat().st_size
    media_type = MEDIA_TYPES_BY_SUFFIX.get(
        candidate.suffix.lower(), "application/octet-stream"
    )
    common_headers = {
        "accept-ranges": "bytes",
        "content-disposition": f'inline; filename="{candidate.name}"',
        **(extra_headers or {}),
    }

    requested = parse_range_header(request.headers.get("range", ""), file_size)

    if requested is None:
        return Response(
            content=candidate.read_bytes(),
            media_type=media_type,
            headers={**common_headers, "content-length": str(file_size)},
        )

    start, end = requested
    with candidate.open("rb") as handle:
        handle.seek(start)
        payload = handle.read(end - start + 1)

    return Response(
        content=payload,
        media_type=media_type,
        status_code=206,
        headers={
            **common_headers,
            "content-range": f"bytes {start}-{end}/{file_size}",
            "content-length": str(len(payload)),
        },
    )


@get("/api/projects/{slug:str}/extraction/assets/{file_name:str}")
async def read_extracted_asset(
    slug: FromPath[str],
    file_name: FromPath[str],
    request: Request,
    projects: NamedDependency[ProjectService],
) -> Response:
    """Serve a figure that extraction pulled out of a source document.

    These bytes came out of an uploaded file, so they are someone else's content
    served from this app's own origin. An SVG is a document, not just a picture:
    opened directly it can run script with this origin's authority. The sandbox
    policy makes the browser treat every asset as inert, whatever it contains.
    """
    project = projects.require(slug)
    assets_directory = (project.root / "extraction" / "assets").resolve()
    candidate = (assets_directory / reduce_to_bare_file_name(file_name)).resolve()

    if not candidate.is_file() or assets_directory not in candidate.parents:
        raise NotFoundException(detail=f"no such extracted asset: {file_name}")

    return media_response(candidate, request, {
        "content-security-policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox",
        "x-content-type-options": "nosniff",
    })


@get("/api/projects/{slug:str}/assets/prepared/{file_name:str}")
async def read_prepared_asset(
    slug: FromPath[str],
    file_name: FromPath[str],
    request: Request,
    projects: NamedDependency[ProjectService],
) -> Response:
    """Serve the trimmed copy of a source figure.

    Its own route because it is its own file. The library trims the slide
    background off each figure and keeps the result beside the original, and
    that copy is what the video draws -- so it is also what a thumbnail has to
    show, or the page displays a picture the render will not use.

    Same headers as an extracted asset, for the same reason: these bytes came
    out of somebody's document.
    """
    project = projects.require(slug)
    prepared_directory = (project.root / "assets" / "prepared").resolve()
    candidate = (prepared_directory / reduce_to_bare_file_name(file_name)).resolve()

    if not candidate.is_file() or prepared_directory not in candidate.parents:
        raise NotFoundException(detail=f"no such prepared asset: {file_name}")

    return media_response(candidate, request, {
        "content-security-policy": "default-src 'none'; style-src 'unsafe-inline'; sandbox",
        "x-content-type-options": "nosniff",
    })


@get("/api/projects/{slug:str}/output/{file_name:str}")
async def download_output(
    slug: FromPath[str],
    file_name: FromPath[str],
    request: Request,
    projects: NamedDependency[ProjectService],
) -> Response:
    """Serve a rendered video, caption or subtitle file."""
    project = projects.require(slug)
    return media_response(resolve_output_file(project, file_name), request)


@get("/api/projects/{slug:str}/narration/{file_name:str}")
async def download_narration(
    slug: FromPath[str],
    file_name: FromPath[str],
    request: Request,
    projects: NamedDependency[ProjectService],
) -> Response:
    """Serve one section's narration audio, so Studio can play the timeline.

    A separate route rather than a path parameter on /output: the directory is
    fixed here, so a request can only ever name a file, never a folder.
    """
    project = projects.require(slug)
    return media_response(resolve_output_file(project, file_name, "audio"), request)


# --- reading a source document ----------------------------------------------


@get("/api/projects/{slug:str}/sources/{file_name:str}")
async def read_source_file(
    slug: FromPath[str],
    file_name: FromPath[str],
    request: Request,
    projects: NamedDependency[ProjectService],
) -> Response:
    """Serve an uploaded document so the page can show it.

    Range-capable and `inline`, so a browser can render a PDF in place rather
    than downloading it. The name is reduced to a bare name and the resolved
    path re-checked against the sources directory -- the read counterpart of the
    guard on upload.
    """
    project = projects.require(slug)
    sources_directory = project.sources_dir.resolve()
    candidate = (sources_directory / reduce_to_bare_file_name(file_name)).resolve()

    if not candidate.is_file() or sources_directory not in candidate.parents:
        raise NotFoundException(detail=f"no such source file: {file_name}")

    return media_response(candidate, request)


@get("/api/projects/{slug:str}/sources/{file_name:str}/preview", sync_to_thread=True)
def preview_source_file(
    slug: FromPath[str], file_name: FromPath[str]
) -> dict[str, Any]:
    """What this file contains, without running the Extraction stage.

    `sync_to_thread` because parsing a large document is CPU work, and doing it
    on the event loop would stall every other request for the duration.
    """
    try:
        return preview_source(slug, file_name)
    except OperationFailed as failure:
        raise NotFoundException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/sources/{file_name:str}/pages/delete", sync_to_thread=True)
def delete_source_pages(
    slug: FromPath[str], file_name: FromPath[str], data: PageDeletion
) -> dict[str, Any]:
    """Take slides or pages out of a deck or PDF, in place. Threaded: 100 MB takes seconds."""
    try:
        return delete_pages(slug, file_name, data.pages)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure
