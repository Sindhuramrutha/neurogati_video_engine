"""Project and stage routes — what the six tabs talk to.

Thin by design. These read and write files; no pipeline logic lives here. When the
graph exists, run endpoints will submit to it and stream progress over the channels
plugin already wired into the app.
"""

from __future__ import annotations

import logging
from typing import Annotated, Any

from litestar import delete, get, post
from litestar.di import NamedDependency
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException, NotFoundException
from litestar.params import Body, FromPath
from pydantic import BaseModel

from pipeline.agents import AgentRegistry
from pipeline.composition import Composition, CompositionStore
from pipeline.config import REPO_ROOT, get_settings
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

    for uploaded_part in data.values():
        original_file_name = getattr(uploaded_part, "filename", "") or ""

        # A multipart body may legitimately carry plain text fields alongside
        # files; those have no filename and must be skipped, not crashed on.
        if not hasattr(uploaded_part, "read"):
            continue

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
    plan = PlanStore(project.root).load()
    section_ids = [section.id for section in plan.sections]
    return ScriptStore(project.root).load().to_dict(section_ids) | {
        "plan_sections": [
            {"id": s.id, "title": s.title, "summary": s.summary,
             "estimated_seconds": s.estimated_seconds}
            for s in plan.sections
        ],
    }


@post("/api/projects/{slug:str}/script", sync_to_thread=False)
def put_script(
    slug: FromPath[str], data: Script, projects: NamedDependency[ProjectService]
) -> dict[str, Any]:
    project = projects.require(slug)
    plan = PlanStore(project.root).load()
    saved = ScriptStore(project.root).save(data)
    return saved.to_dict([s.id for s in plan.sections]) | {
        "plan_sections": [
            {"id": s.id, "title": s.title, "summary": s.summary,
             "estimated_seconds": s.estimated_seconds}
            for s in plan.sections
        ],
    }


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
    plan = PlanStore(project.root).load()
    script = ScriptStore(project.root).load()

    return ReviewStore(project.root).load().to_dict() | {
        "plan_sections": [
            {"id": s.id, "title": s.title, "estimated_seconds": s.estimated_seconds}
            for s in plan.sections
        ],
        "transcript": [
            {
                "section_id": section.id,
                "title": section.title,
                "body": script.resolve(script.body_for(section.id)),
            }
            for section in plan.sections
        ],
    }


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
