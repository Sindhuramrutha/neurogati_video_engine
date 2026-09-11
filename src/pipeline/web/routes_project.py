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
    ask_stage_agent,
    draft_plan_with_agent,
    draft_section_script_with_agent,
)
from pipeline.agents import AgentRegistry
from pipeline.composition import Composition, CompositionStore
from pipeline.config import REPO_ROOT, get_settings
from pipeline.credentials import describe_credentials, save_credentials
from pipeline.extraction import ExtractionStore
from pipeline.llm import describe_model
from pipeline.operations import (
    OperationFailed,
    list_voice_providers,
    present_artifact,
    render_video,
    run_extraction,
)
from pipeline.planning import Plan, PlanStore
from pipeline.projects import Project, ProjectStore
from pipeline.review import Review, ReviewStore, chapters_from_plan
from pipeline.scripting import Script, ScriptStore
from pipeline.sources import (
    SourceFileRejected,
    reduce_to_bare_file_name,
    validate_uploaded_source_file,
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


class AgentQuestion(BaseModel):
    question: str


class PlanInstruction(BaseModel):
    instruction: str


class SectionScriptInstruction(BaseModel):
    section_id: str
    instruction: str = ""


class RenderRequest(BaseModel):
    voice_provider: str = ""
    voice: str = ""


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


@post("/api/projects/{slug:str}/sources")
async def upload_source(
    slug: FromPath[str],
    projects: NamedDependency[ProjectService],
    data: Annotated[dict[str, Any], Body(media_type=RequestEncodingType.MULTI_PART)],
) -> dict[str, Any]:
    """Accept source documents, one at a time, reporting each outcome separately.

    Partial success is a real outcome and is reported as one: dropping five files
    where one is a 200 MB video should store the four good ones and say precisely
    why the fifth was refused. An all-or-nothing 500 would tell the user nothing
    about which file was the problem.
    """
    project = projects.require(slug)
    project.sources_dir.mkdir(parents=True, exist_ok=True)

    accepted_source_files: list[dict[str, Any]] = []
    rejected_source_files: list[dict[str, str]] = []
    file_parts_seen = 0

    for uploaded_part in data.values():
        original_file_name = getattr(uploaded_part, "filename", "") or ""

        # A multipart body may legitimately carry plain text fields alongside
        # files; those have no filename and must be skipped, not crashed on.
        if not hasattr(uploaded_part, "read"):
            continue
        file_parts_seen += 1

        try:
            file_content = await uploaded_part.read()
            accepted = validate_uploaded_source_file(
                original_file_name=original_file_name,
                file_content=file_content,
                destination_directory=project.sources_dir,
            )
        except SourceFileRejected as rejection:
            logger.info(
                "rejected source upload for project %s: %s", slug, rejection
            )
            rejected_source_files.append(
                {"file_name": rejection.original_file_name, "reason": rejection.reason}
            )
            continue

        try:
            (project.sources_dir / accepted.safe_file_name).write_bytes(file_content)
        except OSError as write_failure:
            # Disk full, permission denied, name still unusable on this platform.
            # The user gets a plain reason; the log keeps the underlying error.
            logger.warning(
                "failed writing source %s for project %s: %s",
                accepted.safe_file_name, slug, write_failure,
            )
            rejected_source_files.append(
                {
                    "file_name": accepted.original_file_name,
                    "reason": "could not be saved to disk",
                }
            )
            continue

        accepted_source_files.append(
            {
                "file_name": accepted.safe_file_name,
                "original_file_name": accepted.original_file_name,
                "was_renamed": accepted.was_renamed,
                "size_in_bytes": accepted.size_in_bytes,
            }
        )

    # A request carrying no usable file part is a client mistake, not a success.
    # Returning 201 with two empty lists is the worst of both: the caller sees no
    # error and no result. Reproduced with `curl -F files=@a -F files=@b`, where
    # the repeated field name collapses to a single entry that is not a file
    # part -- nothing was stored and nothing was reported.
    if not file_parts_seen:
        raise ClientException(
            detail="No file was found in the upload. Send each file under its own "
                   "field name, e.g. file0, file1."
        )

    return {
        "accepted": accepted_source_files,
        "rejected": rejected_source_files,
        "project": project.to_dict(),
    }


@delete("/api/projects/{slug:str}/sources/{file_name:str}", status_code=200)
async def delete_source(
    slug: FromPath[str],
    file_name: FromPath[str],
    projects: NamedDependency[ProjectService],
) -> dict[str, Any]:
    """Remove one source file from a project.

    The filename arrives from the URL and is therefore untrusted, exactly like an
    upload filename. It is reduced to a bare name and the resolved target is
    re-checked against the sources directory, so a crafted request cannot delete
    something outside the project -- the deletion equivalent of the traversal that
    the upload path had.
    """
    project = projects.require(slug)

    bare_file_name = reduce_to_bare_file_name(file_name)
    target_path = (project.sources_dir / bare_file_name).resolve()

    if not target_path.is_relative_to(project.sources_dir.resolve()):
        logger.warning(
            "refused delete outside sources dir for project %s: %r", slug, file_name
        )
        raise ClientException(detail="that filename is not valid")

    if not target_path.is_file():
        raise NotFoundException(detail=f"no such source file: {bare_file_name}")

    try:
        target_path.unlink()
    except OSError as delete_failure:
        logger.warning(
            "failed deleting %s from project %s: %s", bare_file_name, slug, delete_failure
        )
        raise ClientException(detail="could not delete that file") from delete_failure

    return {"deleted": bare_file_name, "project": project.to_dict()}


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
    return PlanStore(project.root).load().to_dict()


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
    project = projects.require(slug)
    return PlanStore(project.root).save(data).to_dict()


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
    project = projects.require(slug)
    return present_artifact(project, "script", ScriptStore(project.root).save(data))


@get("/api/projects/{slug:str}/composition", sync_to_thread=False)
def get_composition(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    project = projects.require(slug)
    return CompositionStore(project.root).load().to_dict()


@post("/api/projects/{slug:str}/composition", sync_to_thread=False)
def put_composition(
    slug: FromPath[str], data: Composition, projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """Replace the whole timeline.

    `data` is a validated `Composition`, so clip durations are clamped above the
    minimum grabbable size and the track/clip counts are capped before anything
    reaches disk. A drag that produced a zero-length clip cannot persist one.
    """
    project = projects.require(slug)
    return CompositionStore(project.root).save(data).to_dict()


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
    project = projects.require(slug)
    return ReviewStore(project.root).save(data).to_dict()


@post("/api/projects/{slug:str}/review/seed-chapters", sync_to_thread=False)
def seed_chapters(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """Replace chapters with ones derived from the plan.

    Explicitly destructive and explicitly invoked: seeding automatically on load
    would silently discard hand-edited chapter titles every time the page opened.
    """
    project = projects.require(slug)
    plan = PlanStore(project.root).load()
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


@get("/api/model", sync_to_thread=False)
def get_model_status() -> dict[str, Any]:
    """Whether a model is reachable, and which one. Never includes the key."""
    return describe_model()


@post("/api/projects/{slug:str}/agent/{stage:str}/ask")
async def ask_agent(
    slug: FromPath[str], stage: FromPath[str], data: AgentQuestion
) -> dict[str, Any]:
    """Ask a stage's agent about this project. Writes nothing.

    Async and off the event loop: the provider call can take the better part of a
    minute under `llm_timeout_seconds`, and blocking the loop would freeze every
    other request in the app while one question was answered.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(
            ask_stage_agent, slug, stage, data.question
        )
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/plan/draft")
async def draft_plan(slug: FromPath[str], data: PlanInstruction) -> dict[str, Any]:
    """Have the Planning agent propose a plan. Returns it; saves nothing.

    Deliberately *not* at `/agent/planning/draft-plan`. A literal `planning`
    segment sitting where `/agent/{stage}/ask` expects a parameter shadowed it
    for that one value: every stage but planning reached `ask`, and planning
    alone 404'd -- the stage this feature exists for. Keeping the artifact routes
    free of literal stage names makes the collision impossible rather than
    merely fixed.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(
            draft_plan_with_agent, slug, data.instruction
        )
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/extraction", sync_to_thread=False)
def get_extraction(
    slug: FromPath[str], projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    """The structured content parsed out of the source documents."""
    project = projects.require(slug)
    return present_artifact(project, "extraction", ExtractionStore(project.root).load())


@post("/api/projects/{slug:str}/extraction/run")
async def run_extraction_route(slug: FromPath[str]) -> dict[str, Any]:
    """Parse every source document into structured content.

    Off the event loop: a large PDF takes real time to parse, and blocking the
    loop would freeze the rest of the app while one project extracted.
    """
    import anyio

    try:
        return await anyio.to_thread.run_sync(run_extraction, slug)
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
            render_video, slug, data.voice_provider, data.voice
        )
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


MEDIA_TYPES_BY_SUFFIX = {
    ".mp4": "video/mp4",
    ".vtt": "text/vtt",
    ".srt": "text/plain",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
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


def resolve_output_file(project: Project, file_name: str) -> Path:
    """The requested file, or a 404 -- never a path outside the output directory.

    The name is reduced to a bare name *and* the resolved path is re-checked
    against the directory: the same belt-and-braces as uploads, because this is
    the identical hole pointing the other way.
    """
    output_directory = (project.root / "reviewing" / "output").resolve()
    candidate = (output_directory / reduce_to_bare_file_name(file_name)).resolve()

    if not candidate.is_file() or output_directory not in candidate.parents:
        raise NotFoundException(detail=f"no such output file: {file_name}")
    return candidate


@get("/api/projects/{slug:str}/output/{file_name:str}")
async def download_output(
    slug: FromPath[str],
    file_name: FromPath[str],
    request: Request,
    projects: NamedDependency[ProjectService],
) -> Response:
    """Serve a rendered file, with Range support so the browser can play it.

    **Range is the whole point.** Returning the bytes as a flat 200 meant no
    `Accept-Ranges` and no 206, so a `<video>` element had no way to seek and
    simply refused to start -- the file was fine and the player showed nothing.

    `content_disposition_type="inline"` is the other half: the default is
    `attachment`, which downloads the file instead of playing it. That is the
    same trap that once made this app download its own index page.
    """
    project = projects.require(slug)
    candidate = resolve_output_file(project, file_name)

    file_size = candidate.stat().st_size
    media_type = MEDIA_TYPES_BY_SUFFIX.get(
        candidate.suffix.lower(), "application/octet-stream"
    )
    common_headers = {
        "accept-ranges": "bytes",
        "content-disposition": f'inline; filename="{candidate.name}"',
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
