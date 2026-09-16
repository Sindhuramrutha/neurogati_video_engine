"""The operations every client shares — web, CLI, and MCP.

Three interfaces now reach this pipeline: a browser, a terminal, and an agent
over MCP. Each one needs "open project X, read its plan, add a section, save".
Writing that three times is how v1 failed: `workflow.py` built a graph that
`run_chapter.py` then bypassed with its own reimplementation, the two drifted,
and only one was ever exercised.

So the verbs live here once. A client's job is to parse its own kind of input --
an HTTP body, an argv list, an MCP tool call -- and then call these. Nothing in
this module knows which of the three it is talking to, and none of the three
contains pipeline logic.

Every function that changes something returns the saved artifact's `to_dict()`,
so a caller always sees the validated, audited result rather than what it hoped
it wrote. Clamping, trimming and warnings happen in the models; a caller cannot
opt out of them by picking a different interface.
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pipeline.composition import Clip, Composition, CompositionStore, Track
from pipeline.config import get_settings
from pipeline.extraction import (
    AssetSink,
    Extraction,
    ExtractionStore,
    SourceUnreadable,
    extract_document,
)
from pipeline.planning import Plan, PlanSection, PlanStore
from pipeline.projects import Project, ProjectStore
from pipeline.rendering import (
    TITLE_CARD_MS,
    RenderedSection,
    RenderFailed,
    RenderResult,
    render_sections,
    write_subtitles,
)
from pipeline.review import Comment, Review, ReviewStore, chapters_from_plan
from pipeline.scripting import Script, ScriptStore, SectionScript
from pipeline.speech import SpeechFailed, describe_voice_providers, synthesise_narration
from pipeline.stages import STAGES, Stage
from pipeline.storage.documents import JsonDocumentStore

logger = logging.getLogger(__name__)


class OperationFailed(Exception):
    """A request that cannot be satisfied, phrased for whoever asked.

    One exception type for all three clients: the web layer turns it into a 404
    or 400, the CLI prints it and exits non-zero, MCP returns it as tool output.
    The message is written for a human or a model to read, never a stack trace.
    """


@dataclass(frozen=True)
class ArtifactBinding:
    """Wires a stage to the store and model that persist its artifact.

    Having this as data rather than a chain of `if stage == ...` is what lets the
    CLI and the MCP server expose all four artifacts through one code path each,
    instead of four near-identical handlers apiece.
    """

    stage: Stage
    store_type: type[JsonDocumentStore]
    model_type: type

    def store(self, project: Project) -> JsonDocumentStore:
        return self.store_type(project.root)


ARTIFACTS: dict[str, ArtifactBinding] = {
    "extraction": ArtifactBinding(Stage.EXTRACTION, ExtractionStore, Extraction),
    "plan": ArtifactBinding(Stage.PLANNING, PlanStore, Plan),
    "script": ArtifactBinding(Stage.SCRIPTING, ScriptStore, Script),
    "composition": ArtifactBinding(Stage.STUDIO, CompositionStore, Composition),
    "review": ArtifactBinding(Stage.REVIEWING, ReviewStore, Review),
}


def projects_root() -> Path:
    return get_settings().projects_dir


def project_store() -> ProjectStore:
    return ProjectStore(projects_root())


def require_project(slug: str) -> Project:
    project = project_store().get(slug)
    if project is None:
        known = ", ".join(p.slug for p in project_store().list()) or "none yet"
        raise OperationFailed(f"No project {slug!r}. Existing projects: {known}.")
    return project


def require_artifact(name: str) -> ArtifactBinding:
    binding = ARTIFACTS.get(name)
    if binding is None:
        raise OperationFailed(
            f"No artifact {name!r}. Choose one of: {', '.join(ARTIFACTS)}."
        )
    return binding


# --- projects ---------------------------------------------------------------


def list_projects() -> list[dict[str, Any]]:
    return [project.to_dict() for project in project_store().list()]


def create_project(name: str) -> dict[str, Any]:
    cleaned = name.strip()
    if not cleaned:
        raise OperationFailed("A project needs a name.")
    return project_store().create(cleaned).to_dict()


def describe_project(slug: str) -> dict[str, Any]:
    return require_project(slug).to_dict()


def describe_stages() -> list[dict[str, Any]]:
    """The pipeline's shape, for a client that has never seen it.

    An agent asking "what can I do here?" gets a real answer from this rather
    than having to infer the stages from endpoint names.
    """
    return [
        {
            "key": spec.key.value,
            "title": spec.title,
            "blurb": spec.blurb,
            "has_agent": spec.has_agent,
            "produces": spec.produces,
        }
        for spec in STAGES
    ]


# --- artifacts: the generic path --------------------------------------------


def present_artifact(project: Project, artifact_name: str, document: Any) -> dict[str, Any]:
    """Serialise an artifact together with the context its audit needs.

    Two of the four artifacts cannot be judged alone. A script's "orphaned" and
    "unwritten" counts are meaningless without the plan's section ids, and the
    review's transcript comes from the script. Assembling that here rather than
    in each client is the whole point of this module: the browser, the CLI and
    MCP get the same audit, because they run the same code to compute it.

    They did not, briefly. The web routes assembled it and `operations` did not,
    so a script saved from the CLI came back reporting every section as orphaned
    -- a warning that was pure noise and would have sent someone hunting a bug in
    their own data.
    """
    if artifact_name == "script":
        plan = PlanStore(project.root).load()
        return document.to_dict([section.id for section in plan.sections]) | {
            "plan_sections": [
                {"id": s.id, "title": s.title, "summary": s.summary,
                 "estimated_seconds": s.estimated_seconds}
                for s in plan.sections
            ],
        }

    if artifact_name == "review":
        plan = PlanStore(project.root).load()
        script = ScriptStore(project.root).load()
        return document.to_dict() | {
            "plan_sections": [
                {"id": s.id, "title": s.title, "estimated_seconds": s.estimated_seconds}
                for s in plan.sections
            ],
            "transcript": [
                {
                    "section_id": section.id,
                    "title": section.title,
                    "body": script.resolve(script.body_for(section.id)),
                    # Measured from the render when there is one. Computing these
                    # in the page from `estimated_seconds` put the last line of an
                    # 8-minute video 109 seconds from where it is actually spoken.
                    "start_ms": start_ms,
                }
                for section, start_ms in zip(
                    plan.sections, section_start_times(project, plan), strict=False
                )
            ],
        }

    return document.to_dict()


def read_artifact(slug: str, artifact_name: str) -> dict[str, Any]:
    """The artifact as the UI sees it: values plus audit plus warnings."""
    project = require_project(slug)
    binding = require_artifact(artifact_name)
    return present_artifact(project, artifact_name, binding.store(project).load())


def write_artifact(slug: str, artifact_name: str, values: dict[str, Any]) -> dict[str, Any]:
    """Replace an artifact wholesale from a plain dict.

    Validation is the model's, not this function's -- the same clamping and
    trimming an edit from the browser goes through. A caller that sends a
    40-hour section gets it clamped and flagged in `warnings`, not rejected,
    because losing the rest of a large edit over one bad number is worse.
    """
    # Resolved here so an unknown project fails before the payload is parsed.
    require_project(slug)
    binding = require_artifact(artifact_name)

    try:
        document = binding.model_type.model_validate(values)
    except Exception as validation_failure:
        raise OperationFailed(
            f"That is not a valid {artifact_name}: {validation_failure}"
        ) from validation_failure

    return save_artifact(slug, artifact_name, document)


def save_artifact(slug: str, artifact_name: str, document: Any) -> dict[str, Any]:
    """Persist an already-validated artifact from a client.

    The single write path for every client, so the rules below cannot be skipped
    by picking a different interface. The web routes used to call the stores
    directly and bypassed exactly this.
    """
    project = require_project(slug)
    binding = require_artifact(artifact_name)
    _mark_as_hand_edited(document)
    return present_artifact(project, artifact_name, binding.store(project).save(document))


def _mark_as_hand_edited(document: Any) -> None:
    """Clear the "a render wrote this" markers on any write from a client.

    Every client sends the whole document back, markers included, so without
    this an edited timeline still claimed to be the renderer's and the next
    render replaced it. The renderer sets the markers again itself, after it
    writes.
    """
    if isinstance(document, Composition):
        document.generated_from_render_at = ""
        document.generated_fingerprint = ""
    elif isinstance(document, Review):
        document.chapters_generated_from_render_at = ""


def extraction_freshness(project: Project) -> dict[str, Any]:
    """Whether the extracted content still matches the files on disk.

    Nothing used to notice this. A source added after the last run simply was not
    in the extraction, the Inputs page happily listed it, and every later stage
    planned around a document the pipeline had never read -- the failure only
    surfaced when an agent was asked directly and said a file "was never
    extracted".

    Compared by name and size rather than by timestamp: a file re-uploaded with
    the same content should not force a re-run, and a file swapped for a
    different one of the same name must not pass as unchanged.
    """
    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        return {"has_run": False, "is_stale": False, "added": [], "removed": []}

    on_disk = {source["name"] for source in project.sources()}
    extracted = {document.file_name for document in extraction.documents}

    added = sorted(on_disk - extracted)
    removed = sorted(extracted - on_disk)
    return {
        "has_run": True,
        "is_stale": bool(added or removed),
        "added": added,
        "removed": removed,
        "extracted_at": extraction.extracted_at,
    }


def run_extraction(slug: str) -> dict[str, Any]:
    """Read every source document and store the structured result.

    Not an agent and not a model call: this is parsing. A parser that is wrong
    can be debugged against the file it misread, which is not true of a model
    that invented a heading.

    One unreadable file does not fail the run. The others are extracted and the
    failure is reported per file -- the same partial-success posture as upload,
    for the same reason: "one of your five documents is a problem" is useful and
    "extraction failed" is not.
    """
    project = require_project(slug)
    sources = project.sources()

    if not sources:
        raise OperationFailed(
            f"{project.name} has no source documents yet. Upload one first."
        )

    documents = []
    unreadable: list[str] = []

    # Figures are written beside the extracted text, addressed relative to the
    # project root so the stored path survives the project being moved.
    assets = AssetSink(
        project.root / "extraction" / "assets", relative_to=project.root
    )

    for source in sources:
        path = project.sources_dir / source["name"]
        try:
            documents.append(extract_document(path, assets))
        except SourceUnreadable as failure:
            logger.warning("extraction skipped a source: %s", failure)
            unreadable.append(str(failure))

    if not documents:
        raise OperationFailed(
            "Nothing could be read from any source. " + " ".join(unreadable)
        )

    store = ExtractionStore(project.root)
    saved = store.save(Extraction(
        documents=documents,
        extracted_at=datetime.now(UTC).isoformat(timespec="seconds"),
    ))

    # Only now that the new extraction is on disk: pruning first and then
    # failing to save would lose the figures the old extraction still points at.
    assets.prune_unreferenced()

    result = present_artifact(project, "extraction", saved)
    if unreadable:
        result["warnings"] = [*result["warnings"], *unreadable]
    if assets.skipped_for_size:
        result["warnings"] = [*result["warnings"], (
            f"{assets.skipped_for_size} figure(s) were not extracted: this "
            f"project reached the extracted-image limit."
        )]
    return result


def preview_source(slug: str, file_name: str) -> dict[str, Any]:
    """Where a source file is and how it should be shown. Nothing is parsed.

    **This deliberately does no extraction.** It used to return the pipeline's
    parsed text, which put Extraction's work behind a chevron on the Inputs page:
    two places deciding what a document says, and the slower one running every
    time a row was opened. Inputs shows the file; Extraction reads it.

    The browser renders every format from the raw bytes, so what is on screen is
    the file on disk rather than a conversion of it.
    """
    from pipeline.sources import reduce_to_bare_file_name

    project = require_project(slug)
    bare_name = reduce_to_bare_file_name(file_name)
    path = (project.sources_dir / bare_name).resolve()

    if not path.is_file() or not path.is_relative_to(project.sources_dir.resolve()):
        raise OperationFailed(f"{project.name} has no source file {file_name!r}.")

    suffix = path.suffix.lower()
    # How the page should draw it. Each of these is the real file: a PDF in the
    # browser's own viewer, a deck and a document rendered from their bytes, and
    # plain text shown as written.
    viewer_by_suffix = {
        ".pdf": "pdf",
        ".pptx": "slides",
        ".docx": "document",
        ".md": "plain",
        ".txt": "plain",
    }

    return {
        "file_name": path.name,
        "suffix": suffix,
        "bytes": path.stat().st_size,
        "viewer": viewer_by_suffix.get(suffix, "unsupported"),
    }


def extracted_content_as_markdown(project: Project) -> str:
    """The extracted source text, for an agent's context. Empty if not extracted."""
    return ExtractionStore(project.root).load().as_markdown()


def list_voice_providers() -> dict[str, Any]:
    """Every text-to-speech option with its live availability."""
    return describe_voice_providers()


def render_video(
    slug: str, voice_provider: str = "", voice: str = ""
) -> dict[str, Any]:
    """Turn the plan and script into an actual video file.

    The order matters and is the point: **narration first, then picture.** Each
    section is synthesised, its real duration measured from the audio file, and
    only then is the picture cut to fit ([ADR 0001]). Deciding the picture from
    the plan's estimated seconds and hoping the voice matches is precisely how
    v1's animation drifted out of sync with its narration.

    Writes into `reviewing/output/`, registers the result as a version on the
    review, and returns where the file landed.
    """
    project = require_project(slug)

    plan = read_artifact(slug, "plan")
    if not plan["sections"]:
        raise OperationFailed(
            f"{project.name} has no plan sections yet, so there is nothing to render."
        )

    script = read_artifact(slug, "script")
    narration_by_section = {
        entry["section_id"]: entry["body"] for entry in script["section_scripts"]
    }

    chosen_provider = voice_provider or describe_voice_providers()["recommended"]

    # Every render gets its own identity. All renders used to write
    # `<slug>.mp4`, and each review version stored that one path -- so a second
    # render overwrote every earlier cut, and picking an old version in the UI
    # played the newest file. A "version" that is not immutable is not a version.
    #
    # Milliseconds, not seconds: at one-second resolution two renders started in
    # the same second shared an id, which put both cuts at the same `.mp4` path
    # and reintroduced exactly the overwrite this id exists to prevent. Short
    # projects on the silent provider render in well under a second.
    render_id = datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f")[:-3]

    output_directory = project.root / "reviewing" / "output"
    audio_directory = output_directory / "audio"
    working_directory = output_directory / "frames" / render_id

    sections: list[RenderedSection] = []
    warnings: list[str] = []
    cursor_ms = 0

    for index, plan_section in enumerate(plan["sections"]):
        narration = (narration_by_section.get(plan_section["id"]) or "").strip()
        section = RenderedSection(
            section_id=plan_section["id"],
            title=plan_section["title"],
            narration=narration,
            start_ms=cursor_ms,
        )

        if not narration:
            # A section with no narration still gets its title card, so the gap
            # is visible in the video rather than silently skipped.
            warnings.append(f"{plan_section['title']!r} has no narration; card only")
            section.audio_duration_ms = 0
        else:
            # Named per render too: an earlier timeline still points at its own
            # narration by file name, and reusing the name would silently swap
            # the audio under it.
            audio_path = audio_directory / f"section-{index:02d}-{render_id}.mp3"
            try:
                spoken = synthesise_narration(
                    narration, audio_path, chosen_provider, voice
                )
                section.audio_path = spoken.audio_path
                section.audio_duration_ms = spoken.duration_ms
            except SpeechFailed as speech_failure:
                raise OperationFailed(str(speech_failure)) from speech_failure

        sections.append(section)
        cursor_ms += section.total_ms

    video_path = output_directory / f"{project.slug}-{render_id}.mp4"
    subtitle_path = output_directory / f"{project.slug}-{render_id}.srt"

    try:
        render_sections(sections, working_directory, video_path)
        write_subtitles(sections, subtitle_path)
    except RenderFailed as render_failure:
        raise OperationFailed(str(render_failure)) from render_failure

    result = RenderResult(
        video_path=video_path,
        subtitle_path=subtitle_path,
        duration_ms=cursor_ms,
        provider_key=chosen_provider,
        voice=voice,
        sections=sections,
        warnings=warnings,
    )

    # The timeline first: the review's chapters are derived from the same
    # measured sections, and registering the version first meant chapters were
    # seeded before any measured data existed -- so they came from the plan's
    # estimates and pointed at 60s in a 15s video.
    timeline_note = _write_timeline_from_render(project, sections, render_id)
    if timeline_note:
        result.warnings.append(timeline_note)

    chapter_note = _register_video_version(project, result, render_id)
    if chapter_note:
        result.warnings.append(chapter_note)

    # The frames are intermediates; only the video, its audio and its subtitles
    # are worth keeping per render.
    shutil.rmtree(working_directory, ignore_errors=True)
    return result.to_dict()


def _write_timeline_from_render(
    project: Project, sections: list[RenderedSection], render_id: str = ""
) -> str:
    """Put the render's structure on the Studio timeline, from the same segments
    the video was cut to -- so what Studio shows is what the file contains.

    Title cards go on the video track, narration slides on the text track, and
    each section's narration audio on the audio track at its real, measured
    offset. Returns a note when it deliberately does nothing.

    **Never over hand-made clips.** It replaces a timeline only when it is empty
    or was written by an earlier render. Anything else is someone's editing, and
    replacing it to display the renderer's output would destroy their work.
    """
    from datetime import UTC, datetime

    from pipeline.composition import ClipKind, TrackKind, default_composition
    from pipeline.rendering import section_segments

    store = CompositionStore(project.root)
    existing = store.load()
    existing_clip_count = sum(len(track.clips) for track in existing.tracks)

    if existing_clip_count:
        was_generated = bool(existing.generated_from_render_at)
        # The fingerprint is what makes this safe. An edit round-trips the whole
        # document through the API, marker included, so the marker alone said
        # "generated" for a timeline the user had just edited by hand.
        is_untouched = existing.generated_fingerprint == existing.fingerprint()

        if was_generated and not existing.generated_fingerprint:
            # Written by a version that recorded no fingerprint, so whether it
            # has since been edited is unknowable. Left alone, and said plainly:
            # telling someone they made edits they did not make is its own bug.
            return (
                "The Studio timeline was built by an earlier version that kept no "
                "record of its contents, so it was left as it is. Delete its clips "
                "to have a render rebuild it."
            )

        if not (was_generated and is_untouched):
            return (
                "The Studio timeline has your own edits, so it was not replaced "
                "with the render's structure. Delete the clips to have a render "
                "rebuild it."
            )

    composition = default_composition()
    tracks_by_kind = {track.kind: track for track in composition.tracks}

    for section in sections:
        for segment in section_segments(section):
            if segment.kind == "title":
                tracks_by_kind[TrackKind.VIDEO].clips.append(Clip(
                    kind=ClipKind.SCENE, label=segment.text[:80], text=segment.text,
                    start_ms=segment.start_ms, duration_ms=segment.duration_ms,
                ))
            else:
                tracks_by_kind[TrackKind.TEXT].clips.append(Clip(
                    kind=ClipKind.TEXT, label=segment.text[:40], text=segment.text,
                    start_ms=segment.start_ms, duration_ms=segment.duration_ms,
                ))

        if section.audio_path and section.audio_duration_ms:
            tracks_by_kind[TrackKind.AUDIO].clips.append(Clip(
                kind=ClipKind.AUDIO,
                label=f"Narration - {section.title[:40]}",
                # The file name only: the studio serves narration from the render's
                # audio directory and never accepts a path.
                asset_id=section.audio_path.name,
                start_ms=section.start_ms + TITLE_CARD_MS,
                duration_ms=section.audio_duration_ms,
            ))

    composition.generated_from_render_at = (
        render_id or datetime.now(UTC).isoformat(timespec="seconds")
    )
    composition.generated_fingerprint = composition.fingerprint()
    store.save(composition)
    return ""


def chapters_from_sections(sections: list[RenderedSection]) -> list:
    """Chapter marks straight from the rendered sections.

    Measured, and independent of anything else having been written yet -- which
    is the point: deriving them from the timeline meant the first render seeded
    chapters before the timeline existed and silently fell back to the plan's
    estimates.
    """
    from pipeline.review import Chapter

    return [
        Chapter(title=section.title, start_ms=section.start_ms) for section in sections
    ]


def _register_video_version(
    project: Project, result: RenderResult, render_id: str = ""
) -> str:
    """Record the render as a version on the review.

    So a comment can always say which cut it was made against -- the reason
    `VideoVersion` existed before anything could produce one.
    """
    from datetime import UTC, datetime

    from pipeline.review import VideoVersion

    store = ReviewStore(project.root)
    review = store.load()
    version = VideoVersion(
        label=f"Render {datetime.now(UTC).strftime('%Y-%m-%d %H:%M')}",
        notes=f"{result.provider_key} voice, {len(result.sections)} section(s)",
        duration_ms=result.duration_ms,
        file_path=str(result.video_path),
    )
    review.versions.append(version)
    review.active_version_id = version.id

    measured = chapters_from_sections(result.sections)
    was_generated = bool(review.chapters_generated_from_render_at)
    note = ""

    if not review.chapters or was_generated:
        # Ours to correct: either there are none, or the last render wrote them
        # and nobody has edited them since (an edit clears the marker).
        review.chapters = measured
        review.chapters_generated_from_render_at = (
            render_id or datetime.now(UTC).isoformat(timespec="seconds")
        )
    elif [c.start_ms for c in review.chapters] != [c.start_ms for c in measured]:
        note = (
            "Your chapter marks do not match this render. Use Rebuild chapters "
            "to move them to the new timings."
        )

    store.save(review)
    return note


# --- artifacts: the ergonomic verbs -----------------------------------------
#
# Whole-document writes are complete but unkind: adding one section should not
# require resending the plan. These cover what a client actually does most.


def add_plan_section(
    slug: str, title: str, summary: str = "", estimated_seconds: int = 60
) -> dict[str, Any]:
    project = require_project(slug)
    store = PlanStore(project.root)

    plan = store.load()
    plan.sections.append(
        PlanSection(title=title, summary=summary, estimated_seconds=estimated_seconds)
    )
    return present_artifact(project, "plan", store.save(plan))


def write_section_script(slug: str, section_id: str, body: str) -> dict[str, Any]:
    """Set the narration for one plan section, creating the entry if needed.

    Rejects a section id the plan does not have. The model would happily store
    it -- orphaned scripts are kept on purpose, so deleting a plan section does
    not destroy its writing -- but an agent inventing an id is a mistake, not an
    edit, and it should hear about it immediately rather than through a warning
    three stages later.
    """
    project = require_project(slug)
    plan = PlanStore(project.root).load()
    known_section_ids = {section.id for section in plan.sections}

    if section_id not in known_section_ids:
        listed = ", ".join(f"{s.id} ({s.title})" for s in plan.sections) or "none"
        raise OperationFailed(
            f"The plan has no section {section_id!r}. Sections: {listed}."
        )

    store = ScriptStore(project.root)
    script = store.load()

    for section_script in script.section_scripts:
        if section_script.section_id == section_id:
            section_script.body = body
            break
    else:
        script.section_scripts.append(SectionScript(section_id=section_id, body=body))

    return present_artifact(project, "script", store.save(script))


def add_clip(
    slug: str,
    track_id: str,
    kind: str = "text",
    label: str = "",
    start_ms: int = 0,
    duration_ms: int = 3000,
    text: str = "",
) -> dict[str, Any]:
    project = require_project(slug)
    store = CompositionStore(project.root)
    composition = store.load()

    track = next((t for t in composition.tracks if t.id == track_id), None)
    if track is None:
        listed = ", ".join(f"{t.id} ({t.kind.value})" for t in composition.tracks) or "none"
        raise OperationFailed(f"No track {track_id!r}. Tracks: {listed}.")

    track.clips.append(
        Clip(kind=kind, label=label, start_ms=start_ms, duration_ms=duration_ms, text=text)
    )
    _mark_as_hand_edited(composition)
    return present_artifact(project, "composition", store.save(composition))


def add_review_comment(
    slug: str,
    body: str,
    author: str = "",
    at_ms: int = 0,
    routed_to_stage: str | None = None,
) -> dict[str, Any]:
    project = require_project(slug)
    store = ReviewStore(project.root)
    review = store.load()

    stage: Stage | None = None
    if routed_to_stage:
        try:
            stage = Stage(routed_to_stage)
        except ValueError as unknown_stage:
            valid = ", ".join(s.key.value for s in STAGES)
            raise OperationFailed(
                f"No stage {routed_to_stage!r} to route to. Stages: {valid}."
            ) from unknown_stage

    review.comments.append(
        Comment(body=body, author=author, at_ms=at_ms, routed_to_stage=stage)
    )
    return present_artifact(project, "review", store.save(review))


def section_start_times(project: Project, plan) -> list[int]:
    """Where each plan section begins in the finished video.

    From the render's title cards when one exists -- those are measured. Before
    a render, the plan's estimates are the only answer available, and they are
    a guess made before a word was spoken.
    """
    from pipeline.composition import ClipKind, TrackKind

    composition = CompositionStore(project.root).load()
    if composition.generated_from_render_at:
        title_cards = sorted(
            (
                clip
                for track in composition.tracks if track.kind is TrackKind.VIDEO
                for clip in track.clips if clip.kind is ClipKind.SCENE
            ),
            key=lambda clip: clip.start_ms,
        )
        if len(title_cards) == len(plan.sections):
            return [clip.start_ms for clip in title_cards]

    starts: list[int] = []
    running_ms = 0
    for section in plan.sections:
        starts.append(running_ms)
        running_ms += section.estimated_seconds * 1000
    return starts


def chapters_for(project: Project) -> list:
    """Chapter marks for this project, preferring the finished video.

    A render writes its title cards onto the timeline at their **measured**
    positions, so those are where the sections actually begin. The plan's
    `estimated_seconds` are a guess made before any narration was spoken, and
    seeding from them was wrong by up to 109 seconds on an 8-minute video --
    chapter 5 pointed at 5:30 for a section that starts at 7:19. Chapters are
    navigation; navigation that lands in the wrong place is worse than none.

    Falls back to the plan's estimates when nothing has been rendered yet, which
    is the best available answer at that point.
    """
    from pipeline.composition import ClipKind, TrackKind
    from pipeline.review import Chapter

    composition = CompositionStore(project.root).load()
    if composition.generated_from_render_at:
        title_cards = [
            clip
            for track in composition.tracks if track.kind is TrackKind.VIDEO
            for clip in track.clips if clip.kind is ClipKind.SCENE
        ]
        if title_cards:
            return [
                Chapter(title=clip.text or clip.label, start_ms=clip.start_ms)
                for clip in sorted(title_cards, key=lambda c: c.start_ms)
            ]

    plan = PlanStore(project.root).load()
    return chapters_from_plan([
        {"title": section.title, "estimated_seconds": section.estimated_seconds}
        for section in plan.sections
    ])


def seed_review_chapters(slug: str) -> dict[str, Any]:
    """Replace chapters with ones matching the rendered video, or the plan if
    nothing is rendered yet.

    Destructive and therefore never automatic on load: seeding every time
    something opened the review would discard hand-edited chapter titles.
    """
    project = require_project(slug)
    store = ReviewStore(project.root)

    review = store.load()
    review.chapters = chapters_for(project)
    return present_artifact(project, "review", store.save(review))


__all__ = [
    "ARTIFACTS",
    "list_voice_providers",
    "render_video",
    "extracted_content_as_markdown",
    "run_extraction",
    "ArtifactBinding",
    "OperationFailed",
    "Track",
    "add_clip",
    "add_plan_section",
    "add_review_comment",
    "create_project",
    "describe_project",
    "describe_stages",
    "list_projects",
    "project_store",
    "projects_root",
    "present_artifact",
    "preview_source",
    "read_artifact",
    "save_artifact",
    "require_artifact",
    "require_project",
    "seed_review_chapters",
    "write_artifact",
    "write_section_script",
]
