"""Running extraction, and the settings that decide what it reads.

The options are inputs to the stage rather than part of its output, so they live
beside the run instead of inside the extracted content -- see `stage_options`.
What is left out is recorded per project too: a file someone unticked is left
out of every later run and is never reported as missing.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from pipeline.core import OperationFailed, require_project
from pipeline.extraction import (
    AssetSink,
    Extraction,
    ExtractionStore,
    SourceSelectionStore,
    SourceUnreadable,
    extract_document,
)
from pipeline.presentation import present_artifact
from pipeline.projects import Project
from pipeline.stages import Stage

logger = logging.getLogger(__name__)


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
                # A slide background is a picture too, so the sink is needed for
                # that pass even when figures themselves are switched off.
                assets if (options["extract_images"] or options["extract_backgrounds"])
                else None,
                keep_tables=options["extract_tables"],
                keep_figures=options["extract_images"],
                capture_layout=options["extract_layout"],
                capture_backgrounds=options["extract_backgrounds"],
                capture_styling=options["extract_styling"],
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
