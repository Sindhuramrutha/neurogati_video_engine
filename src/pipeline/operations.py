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

import hashlib
import json
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
    SourceSelectionStore,
    SourceUnreadable,
    extract_document,
)
from pipeline.planning import (
    LearningObjective,
    Plan,
    PlanDraftStore,
    PlanSection,
    PlanStore,
)
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
from pipeline.scripting import (
    Script,
    ScriptScene,
    ScriptStore,
    SectionScript,
    over_budget_warning,
)
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
    if artifact_name == "plan":
        extraction = ExtractionStore(project.root).load()
        freshness = plan_freshness(document, extraction)
        presented = document.to_dict()
        presented["warnings"] = [*presented["warnings"], *freshness["warnings"]]
        return presented | {
            "freshness": freshness,
            "source_outline": source_outline(extraction),
            "has_pending_draft": PlanDraftStore(project.root).load() is not None,
        }

    if artifact_name == "script":
        plan = PlanStore(project.root).load()
        section_ids = [section.id for section in plan.sections]
        budgets = {section.id: section.estimated_seconds for section in plan.sections}
        titles = {section.id: section.title for section in plan.sections}
        ordered = document.in_plan_order(section_ids)
        presented = ordered.to_dict(section_ids, budgets, titles)

        extraction = ExtractionStore(project.root).load()
        out_of_date = narration_freshness(plan, ordered, extraction)
        if out_of_date:
            presented["warnings"] = [*presented["warnings"], (
                f"{len(out_of_date)} section(s) were written against an earlier version "
                f"of their plan section or source content"
            )]

        return presented | {
            # Everything the writer needs next to the editor. The page used to get
            # a title and a summary, so narration was written without the target
            # length, the objectives or the source it was meant to come from.
            "plan_sections": [
                section.model_dump(mode="json", include={
                    "id", "title", "summary", "estimated_seconds", "sources",
                    "rendering_approach", "rendering_reason", "objective_ids",
                })
                for section in plan.sections
            ],
            "plan_objectives": [
                {"id": o.id, "text": o.text}
                for o in plan.learning_objectives if o.is_included
            ],
            "selected_audience": plan.selected_audience,
            "out_of_date": out_of_date,
            "comments_by_section": _open_comments_by_section(project, plan, Stage.SCRIPTING),
            "measured_seconds": _measured_narration_seconds(project, plan),
        }

    if artifact_name == "review":
        plan = PlanStore(project.root).load()
        script = ScriptStore(project.root).load()
        presented = document.to_dict()
        # Reviewing is the last gate before export, so it repeats what Scripting
        # found about length. A review reading "no warnings" over a section half
        # as long again as planned was how that went unnoticed.
        budget_audit = script.audit(
            [section.id for section in plan.sections],
            {section.id: section.estimated_seconds for section in plan.sections},
            {section.id: section.title for section in plan.sections},
        )
        presented["warnings"] = [
            *presented["warnings"],
            *(over_budget_warning(section) for section in budget_audit["over_budget"]),
        ]
        return presented | {
            "plan_sections": [
                {"id": s.id, "title": s.title, "estimated_seconds": s.estimated_seconds}
                for s in plan.sections
            ],
            "transcript": [
                {
                    "section_id": section.id,
                    "title": section.title,
                    "body": script.spoken_text(section.id),
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
    if artifact_name == "script":
        document = _script_in_plan_order(project, document)
        _stamp_rewritten_narration(project, document)
    return present_artifact(project, artifact_name, binding.store(project).save(document))


def _script_in_plan_order(project: Project, script: Script) -> Script:
    """Stored in plan order, so the file reads the way the video plays."""
    plan = PlanStore(project.root).load()
    return script.in_plan_order([section.id for section in plan.sections])


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


# --- planning against the extraction ----------------------------------------


def source_outline(extraction: Extraction) -> list[dict[str, Any]]:
    """Every extracted document's headings: what a section can point at."""
    return [
        {
            "file_name": document.file_name,
            "words": document.word_count,
            "headings": document.heading_outline(),
        }
        for document in extraction.documents
    ]


def plan_freshness(plan: Plan, extraction: Extraction) -> dict[str, Any]:
    """Whether this plan still matches the extracted content it was made from.

    Three separate questions, because they need different answers:

    - **stale**: the extraction changed since the plan was drafted or confirmed.
      Something may be new, gone or reworded; the plan might still be fine.
    - **missing sources**: a section points at a location that is no longer in
      the extraction. That section is definitely teaching from nothing.
    - **unlinked**: a plan with sections and no record of what they are based
      on. A real plan was in exactly this state -- describing a chapter the
      extraction no longer held -- and nothing could notice.
    """
    current = extraction.content_fingerprint()
    is_linked = bool(plan.extraction_fingerprint)
    is_stale = is_linked and bool(current) and plan.extraction_fingerprint != current

    missing = []
    for section in plan.sections:
        gone = [
            reference.label for reference in section.sources
            if not extraction.has_location(reference.file_name, reference.heading_path)
        ]
        if gone:
            missing.append({"section_id": section.id, "title": section.title, "missing": gone})

    uses_sources = is_linked or any(section.sources for section in plan.sections)
    without_sources = [s.id for s in plan.sections if not s.sources] if uses_sources else []
    is_unlinked = bool(plan.sections) and not uses_sources and bool(extraction.documents)

    warnings = []
    if is_stale:
        warnings.append("the extraction has changed since this plan was drafted")
    if missing:
        warnings.append(
            f"{len(missing)} section(s) point at content that is no longer in the extraction"
        )
    if is_unlinked:
        warnings.append("this plan is not linked to the extracted content")

    return {
        "has_extraction": bool(extraction.documents),
        "extraction_fingerprint": current,
        "is_linked": is_linked,
        "is_stale": is_stale,
        "is_unlinked": is_unlinked,
        "sections_with_missing_sources": missing,
        "sections_without_sources": without_sources,
        "warnings": warnings,
    }


def confirm_plan_matches_extraction(slug: str) -> dict[str, Any]:
    """Record that someone checked this plan against the current extraction.

    The way out of "out of date" without redrafting: the extraction changed, a
    person looked, and the plan still holds. Refused when there is nothing
    extracted to confirm against.
    """
    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        raise OperationFailed("Nothing has been extracted yet, so there is nothing to confirm.")

    store = PlanStore(project.root)
    plan = store.load()
    plan.extraction_fingerprint = extraction.content_fingerprint()
    return present_artifact(project, "plan", store.save(plan))


def read_plan_draft(slug: str) -> dict[str, Any]:
    """The pending drafted plan, with what accepting it would do."""
    project = require_project(slug)
    draft = PlanDraftStore(project.root).load()
    if draft is None:
        return {"is_pending": False}

    current = PlanStore(project.root).load()
    script = ScriptStore(project.root).load()
    narrated = {s.section_id for s in script.section_scripts if s.body.strip()}
    proposed = Plan.model_validate(draft.get("plan", {}))
    extraction = ExtractionStore(project.root).load()

    return draft | {
        "is_pending": True,
        "plan": proposed.to_dict(),
        # Accepting all replaces the sections, and narration is attached to
        # section ids: say how much written narration would be left unattached
        # before anyone clicks, not after.
        "replaces_narrated_sections": sum(1 for s in current.sections if s.id in narrated),
        "is_behind_extraction": (
            draft.get("extraction_fingerprint", "") != extraction.content_fingerprint()
        ),
    }


def accept_plan_draft(slug: str, section_ids: list[str] | None = None) -> dict[str, Any]:
    """Take a drafted plan in whole, or some of its sections.

    **All** replaces the sections, objectives and key themes, keeps the chosen
    audience, and records the extraction the draft was made from.

    **Some** appends just those sections to the current plan. Their learning
    objectives come with them -- matched by wording against the plan's own, so
    the same objective is never added twice -- and the rest of the plan is left
    exactly as it was. Partly accepting a draft is not a claim that the plan
    matches the extraction, so the plan's record of that is not changed.
    """
    project = require_project(slug)
    drafts = PlanDraftStore(project.root)
    draft = drafts.load()
    if draft is None:
        raise OperationFailed("There is no drafted plan to accept.")

    proposed = Plan.model_validate(draft.get("plan", {}))
    store = PlanStore(project.root)
    plan = store.load()

    if section_ids is None:
        plan.sections = proposed.sections
        plan.learning_objectives = proposed.learning_objectives
        plan.key_themes = proposed.key_themes or plan.key_themes
        plan.extraction_fingerprint = draft.get("extraction_fingerprint", "")
        saved = store.save(plan)
        drafts.clear()
        return present_artifact(project, "plan", saved)

    by_id = {section.id: section for section in proposed.sections}
    unknown = [sid for sid in section_ids if sid not in by_id]
    if unknown:
        raise OperationFailed(f"The draft has no section(s) {', '.join(unknown)}.")

    proposed_objectives = {o.id: o for o in proposed.learning_objectives}
    existing_by_wording = {o.text.strip().lower(): o.id for o in plan.learning_objectives}

    for section_id in section_ids:
        section = by_id[section_id].model_copy(deep=True)
        linked = []
        for objective_id in section.objective_ids:
            objective = proposed_objectives.get(objective_id)
            if objective is None:
                continue
            wording = objective.text.strip().lower()
            if wording not in existing_by_wording:
                added = LearningObjective(text=objective.text)
                plan.learning_objectives.append(added)
                existing_by_wording[wording] = added.id
            linked.append(existing_by_wording[wording])
        # A fresh id each time, so adding the same proposed section twice gives
        # two sections rather than two entries sharing one identity.
        section.id = PlanSection().id
        section.objective_ids = linked
        plan.sections.append(section)

    saved = store.save(plan)

    accepted = sorted(set(draft.get("accepted_section_ids", [])) | set(section_ids))
    if set(accepted) >= set(by_id):
        drafts.clear()
    else:
        drafts.save(draft | {"accepted_section_ids": accepted})
    return present_artifact(project, "plan", saved)


def discard_plan_draft(slug: str) -> dict[str, Any]:
    project = require_project(slug)
    return {"discarded": PlanDraftStore(project.root).clear()}


def excluded_sources(project: Project) -> list[str]:
    """Source files left out of extraction by choice, that still exist."""
    on_disk = {source["name"] for source in project.sources()}
    return [name for name in SourceSelectionStore(project.root).load() if name in on_disk]


def set_excluded_sources(slug: str, excluded: list[str]) -> dict[str, Any]:
    """Choose which source files extraction leaves out. Runs nothing.

    Names are checked against the project's files: an unknown name is a typo or
    a stale page, and saving it would exclude a file that does not exist -- and
    then, silently, whatever is uploaded under that name later.
    """
    project = require_project(slug)
    on_disk = {source["name"] for source in project.sources()}
    unknown = sorted(set(excluded) - on_disk)
    if unknown:
        raise OperationFailed(
            f"{project.name} has no source file(s) named {', '.join(unknown)}."
        )

    saved = SourceSelectionStore(project.root).save(list(excluded))
    return {"excluded": saved, "freshness": extraction_freshness(project)}


def forget_excluded_source(project: Project, file_name: str) -> None:
    """Drop a deleted file from the selection, so re-uploading it includes it."""
    store = SourceSelectionStore(project.root)
    current = store.load()
    if file_name in current:
        store.save([name for name in current if name != file_name])


def implemented_extraction_options(project: Project) -> dict[str, bool]:
    """The Extraction options that actually change a run, as saved for this project.

    Only these. The page also shows options that are declared but not built, and
    recording those here would let a toggle that does nothing mark an extraction
    as out of date.
    """
    from pipeline.stage_options import StageSettingsStore, options_for

    saved = StageSettingsStore(project.root).load(Stage.EXTRACTION).values
    return {
        option.key: bool(saved[option.key])
        for option in options_for(Stage.EXTRACTION)
        if option.implemented
    }


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
        return {
            "has_run": False, "is_stale": False,
            "added": [], "removed": [], "options_changed": [],
            "excluded": excluded_sources(project), "newly_excluded": [],
        }

    on_disk = {source["name"] for source in project.sources()}
    extracted = {document.file_name for document in extraction.documents}

    # Left out by choice is not "not extracted". Without this, ticking a box off
    # would have reported that file as missing forever.
    excluded = set(excluded_sources(project))
    added = sorted(on_disk - extracted - excluded)
    removed = sorted(extracted - on_disk)
    # Still in the extraction, but unticked since: the next run drops it, and
    # until then later stages are reading a document someone chose to leave out.
    newly_excluded = sorted(extracted & excluded)

    # An extraction made before options were recorded has none; it cannot be
    # judged against them, so it is not called stale on that basis.
    current_options = implemented_extraction_options(project)
    options_changed = sorted(
        key for key, value in current_options.items()
        if key in extraction.options_used and extraction.options_used[key] != value
    )

    return {
        "has_run": True,
        "is_stale": bool(added or removed or options_changed or newly_excluded),
        "added": added,
        "removed": removed,
        "options_changed": options_changed,
        "excluded": sorted(excluded),
        "newly_excluded": newly_excluded,
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
    all_sources = project.sources()

    if not all_sources:
        raise OperationFailed(
            f"{project.name} has no source documents yet. Upload one first."
        )

    left_out = set(excluded_sources(project))
    sources = [source for source in all_sources if source["name"] not in left_out]
    if not sources:
        raise OperationFailed(
            f"Every source file in {project.name} is left out of extraction. "
            f"Tick at least one to extract it."
        )

    documents = []
    unreadable: list[str] = []
    options = implemented_extraction_options(project)

    # Figures are written beside the extracted text, addressed relative to the
    # project root so the stored path survives the project being moved.
    assets = AssetSink(
        project.root / "extraction" / "assets", relative_to=project.root
    )

    for source in sources:
        path = project.sources_dir / source["name"]
        try:
            documents.append(extract_document(
                path,
                # A deck's backgrounds are pictures too, so the sink is needed
                # for the design pass even when figures themselves are off.
                assets if (options["extract_images"] or options["extract_design"]) else None,
                keep_tables=options["extract_tables"],
                keep_figures=options["extract_images"],
                capture_layout=options["extract_layout"],
                capture_design=options["extract_design"],
            ))
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
        options_used=options,
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

    # The spoken text, variables filled in. The render used to take the raw body,
    # so "{{COURSE}}" reached the voice, the subtitles and the Studio timeline
    # while the review transcript showed the substituted value.
    script_document = ScriptStore(project.root).load()
    undefined_variables = script_document.audit(
        [section["id"] for section in plan["sections"]]
    )["undefined_variables"]

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
    warnings: list[str] = [
        f"{{{{{name}}}}} is not defined, so it is spoken as written"
        for name in undefined_variables
    ]
    cursor_ms = 0

    for index, plan_section in enumerate(plan["sections"]):
        narration = script_document.spoken_text(plan_section["id"]).strip()
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

    # One scene holding the whole body. Assigning `body` alone would be undone
    # on the next load: the scenes are the narration, and they would still hold
    # the old text.
    replacement = SectionScript(section_id=section_id, scenes=[ScriptScene(narration=body)])
    script.section_scripts = [
        s for s in script.section_scripts if s.section_id != section_id
    ] + [replacement]

    ordered = _script_in_plan_order(project, script)
    _stamp_rewritten_narration(project, ordered)
    return present_artifact(project, "script", store.save(ordered))


# --- narration against the plan and the source ---------------------------------


def _fingerprint(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def narration_fingerprints(section: PlanSection, extraction: Extraction) -> dict[str, str]:
    """What a section's narration is written against: the plan section's content
    and the text of the sources it covers.

    Length and presentation are left out on purpose. A new target duration or a
    different rendering approach does not make what was said wrong; a changed
    summary, different sources, or reworded source material might.
    """
    source_text = []
    for reference in section.sources:
        document = extraction.document(reference.file_name)
        source_text.append(document.text_under(reference.heading_path) if document else "")
    return {
        "plan": _fingerprint([
            section.title, section.summary,
            [[r.file_name, r.heading_path] for r in section.sources],
        ]),
        "source": _fingerprint(source_text),
    }


def narration_freshness(
    plan: Plan, script: Script, extraction: Extraction
) -> list[dict[str, Any]]:
    """Sections whose narration was written against something that has changed.

    Narration with no record of what it was written from is not judged: there is
    nothing to compare, and calling all of it out of date would be noise.
    """
    by_id = {s.section_id: s for s in script.section_scripts}
    found = []
    for section in plan.sections:
        written = by_id.get(section.id)
        if written is None or not written.body.strip() or not written.written_from:
            continue
        current = narration_fingerprints(section, extraction)
        reasons = []
        if written.written_from.get("plan") != current["plan"]:
            reasons.append("the plan section changed")
        if written.written_from.get("source") != current["source"]:
            reasons.append("its source content changed")
        if reasons:
            found.append({"section_id": section.id, "title": section.title, "reasons": reasons})
    return found


def _stamp_rewritten_narration(project: Project, script: Script) -> None:
    """Record what each section's narration was written against, when it changes.

    Only sections whose words or briefs actually changed are stamped: saving the
    whole script after editing one section must not declare every other section
    freshly checked against the current plan.
    """
    plan = PlanStore(project.root).load()
    sections = {section.id: section for section in plan.sections}
    extraction = ExtractionStore(project.root).load()
    stored = {s.section_id: s for s in ScriptStore(project.root).load().section_scripts}

    for section_script in script.section_scripts:
        section = sections.get(section_script.section_id)
        if section is None:
            continue
        before = stored.get(section_script.section_id)
        content_now = [(s.narration.strip(), s.brief) for s in section_script.scenes]
        content_before = [(s.narration.strip(), s.brief) for s in before.scenes] if before else []
        if content_now != content_before and section_script.body.strip():
            section_script.written_from = narration_fingerprints(section, extraction)


def confirm_section_narration(slug: str, section_id: str) -> dict[str, Any]:
    """Record that this section's narration was checked against the current plan
    and source, without changing a word of it."""
    project = require_project(slug)
    plan = PlanStore(project.root).load()
    section = next((s for s in plan.sections if s.id == section_id), None)
    if section is None:
        raise OperationFailed(f"The plan has no section {section_id!r}.")

    store = ScriptStore(project.root)
    script = store.load()
    written = next((s for s in script.section_scripts if s.section_id == section_id), None)
    if written is None or not written.body.strip():
        raise OperationFailed("That section has no narration to confirm.")

    written.written_from = narration_fingerprints(section, ExtractionStore(project.root).load())
    return present_artifact(project, "script", store.save(_script_in_plan_order(project, script)))


def section_source_material(slug: str, section_id: str) -> dict[str, Any]:
    """The full text of the content a plan section records, for reading while writing."""
    from pipeline.plan_drafting import MAXIMUM_SECTION_SOURCE_CHARACTERS

    project = require_project(slug)
    plan = PlanStore(project.root).load()
    section = next((s for s in plan.sections if s.id == section_id), None)
    if section is None:
        raise OperationFailed(f"The plan has no section {section_id!r}.")

    extraction = ExtractionStore(project.root).load()
    parts, missing = [], []
    for reference in section.sources:
        document = extraction.document(reference.file_name)
        if document is None or not document.has_location(reference.heading_path):
            missing.append(reference.label)
            continue
        parts.append({"label": reference.label,
                      "text": document.text_under(reference.heading_path)})

    total = sum(len(part["text"]) for part in parts)
    return {
        "section_id": section_id,
        "has_sources": bool(section.sources),
        "parts": parts,
        "missing": missing,
        "characters": total,
        "longer_than_an_agent_reads": total > MAXIMUM_SECTION_SOURCE_CHARACTERS,
    }


def _open_comments_by_section(project: Project, plan: Plan, stage: Stage) -> dict[str, list]:
    """Open review comments routed to a stage, placed on the section they fall in.

    Placed by time: a comment is anchored where it was made in the video, and
    each section starts where its title card does (measured once rendered).
    """
    review = ReviewStore(project.root).load()
    routed = [c for c in review.comments if c.is_open and c.routed_to_stage is stage]
    if not routed or not plan.sections:
        return {}

    starts = section_start_times(project, plan)
    placed: dict[str, list] = {}
    for comment in sorted(routed, key=lambda c: c.at_ms):
        index = max((i for i, start in enumerate(starts) if start <= comment.at_ms), default=0)
        placed.setdefault(plan.sections[index].id, []).append({
            "id": comment.id, "author": comment.author, "body": comment.body,
            "at_ms": comment.at_ms,
        })
    return placed


def _measured_narration_seconds(project: Project, plan: Plan) -> dict[str, float]:
    """How long each section's narration actually ran in the last render.

    Only while the Studio timeline is still the render's own: once someone edits
    it, its clips no longer say how long the render was, and a stale number is
    worse than none.
    """
    from pipeline.composition import TrackKind

    composition = CompositionStore(project.root).load()
    if not composition.generated_from_render_at:
        return {}

    starts = section_start_times(project, plan)
    audio_clips = [
        clip for track in composition.tracks if track.kind is TrackKind.AUDIO
        for clip in track.clips
    ]
    measured = {}
    for section, start in zip(plan.sections, starts, strict=False):
        clip = next((c for c in audio_clips if c.start_ms == start + TITLE_CARD_MS), None)
        if clip is not None:
            measured[section.id] = round(clip.duration_ms / 1000, 1)
    return measured


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
