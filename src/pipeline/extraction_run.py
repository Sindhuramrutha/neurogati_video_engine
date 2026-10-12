"""Running extraction: one file at a time, into a collection, then confirmed.

The flow the Extraction page follows, and the only one there is:

1. **Extract one file.** Each source is read on its own and its result goes into
   the *collection* -- replacing that file's previous result if it had one.
   Only one file is extracted at a time per project; a second request while one
   runs is refused rather than queued or raced.
2. **Assemble the collection.** Files are added, re-extracted or removed until
   the collection holds what the video should be made from.
3. **Confirm it.** Confirming copies the collection into the extraction that
   every later stage reads. Until then those stages see the last confirmed
   collection, never one half-assembled.

The options are inputs to a run rather than part of its output, so they live
beside it -- see `stage_options` -- and each extracted file records the options
it was read with, which is how a changed option is reported per file.
"""

from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime
from typing import Any

from pipeline import progress
from pipeline.core import OperationFailed, require_project
from pipeline.extraction import (
    AssetSink,
    Extraction,
    ExtractionCollectionStore,
    ExtractionStore,
    SourceUnreadable,
    extract_document,
)
from pipeline.presentation import present_artifact
from pipeline.projects import Project
from pipeline.stages import Stage

logger = logging.getLogger(__name__)

# One extraction at a time, per project. Two at once would each load the
# collection, add their file, and save -- and whichever saved second would drop
# the other's file without a word.
_running: dict[str, threading.Lock] = {}
_running_guard = threading.Lock()


def _extraction_lock(project: Project) -> threading.Lock:
    with _running_guard:
        return _running.setdefault(str(project.root.resolve()), threading.Lock())


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def extraction_options(project: Project) -> dict[str, bool]:
    """The Extraction options, as saved for this project."""
    from pipeline.stage_options import StageSettingsStore, options_for

    saved = StageSettingsStore(project.root).load(Stage.EXTRACTION).values
    return {
        option.key: bool(saved[option.key])
        for option in options_for(Stage.EXTRACTION)
    }


def extraction_freshness(
    project: Project,
    collection: Extraction | None = None,
    confirmed: Extraction | None = None,
) -> dict[str, Any]:
    """Where the collection stands against the files, the options and the hand-off.

    Per file, because files are extracted one at a time:

    - `added`: on disk but not in the collection -- not extracted yet. A choice,
      not a fault, so it does not make the extraction stale.
    - `removed`: in the collection, but the file is gone.
    - `changed`: in the collection, but the file on disk is a different size --
      it was replaced after it was extracted.
    - `options_changed`: extracted with options that are no longer the current ones.
    - `pending_confirmation`: the collection differs from what later stages read.

    Compared by name and size rather than by timestamp: a file re-uploaded with
    the same content should not force a re-run, and a file swapped for a
    different one of the same name must not pass as unchanged.

    Pass the collection and the confirmed extraction when they are already
    loaded; each is a multi-megabyte parse for a large deck.
    """
    collection = collection or ExtractionCollectionStore(project.root).load()
    confirmed = confirmed or ExtractionStore(project.root).load()
    sizes = {source["name"]: source.get("bytes", 0) for source in project.sources()}
    current = extraction_options(project)

    in_collection = {document.file_name: document for document in collection.documents}
    removed = sorted(name for name in in_collection if name not in sizes)
    changed = sorted(
        name for name, document in in_collection.items()
        if name in sizes and document.source_bytes and document.source_bytes != sizes[name]
    )
    def read_with_other_options(document) -> bool:
        # A file extracted before options were recorded per file falls back to
        # the collection's; one with neither cannot be judged, so is not stale.
        used = document.options_used or collection.options_used
        return any(key in used and used[key] != value for key, value in current.items())

    options_changed = sorted(
        name for name, document in in_collection.items() if read_with_other_options(document))
    pending = (bool(collection.documents or confirmed.documents)
               and collection.extracted_at != confirmed.extracted_at)

    return {
        "has_run": bool(collection.documents),
        "has_confirmed": bool(confirmed.documents),
        "is_stale": bool(removed or changed or options_changed or pending),
        "added": sorted(name for name in sizes if name not in in_collection),
        "removed": removed,
        "changed": changed,
        "options_changed": options_changed,
        "pending_confirmation": pending,
        "extracted_at": collection.extracted_at,
        "confirmed_at": confirmed.confirmed_at,
    }


def freshness_warnings(freshness: dict[str, Any]) -> list[str]:
    """What the freshness means, in sentences, for a page or an agent."""
    return [
        *(f"{name} was extracted but is no longer in the project"
          for name in freshness["removed"]),
        *(f"{name} changed after it was extracted; extract it again"
          for name in freshness["changed"]),
        *(f"{name} was extracted with different options; extract it again"
          for name in freshness["options_changed"]),
        *(["the extracted data has changes that are not transferred yet, so the next layer "
           "still reads what was last transferred"]
          if freshness["pending_confirmation"] else []),
    ]


def extraction_page(
    project: Project,
    collection: Extraction | None = None,
    confirmed: Extraction | None = None,
) -> dict[str, Any]:
    """The collection as the Extraction page shows it, with its freshness."""
    collection = collection or ExtractionCollectionStore(project.root).load()
    presented = present_artifact(project, "extraction", collection)
    freshness = extraction_freshness(project, collection, confirmed)
    presented["freshness"] = freshness
    presented["warnings"] = [*presented["warnings"], *freshness_warnings(freshness)]
    return presented


def _prune_assets(sink: AssetSink, collection: Extraction, confirmed: Extraction) -> None:
    """Drop stored pictures that neither the collection nor the confirmed
    extraction points at. Only after both are saved."""
    sink.prune_unreferenced(collection.asset_paths() | confirmed.asset_paths())


def extraction_asset_sink(project: Project) -> AssetSink:
    # Addressed relative to the project root so a stored path survives the
    # project being moved.
    return AssetSink(project.root / "extraction" / "assets", relative_to=project.root)


def source_file_path(project: Project, file_name: str):
    from pipeline.sources import reduce_to_bare_file_name

    bare_name = reduce_to_bare_file_name(file_name)
    path = (project.sources_dir / bare_name).resolve()
    if not path.is_file() or not path.is_relative_to(project.sources_dir.resolve()):
        raise OperationFailed(f"{project.name} has no source file {file_name!r}.")
    return path


def run_extraction(slug: str, file_name: str = "") -> dict[str, Any]:
    """Extract the project's source file. The result is the whole extraction: a
    project has one file, so a run replaces what was there rather than adding to it.

    Not an agent and not a model call: this is parsing -- except the pages the
    handwriting option sends to the vision model, which are marked as such. A
    parser that is wrong can be debugged against the file it misread.

    An unreadable file fails this call and leaves the collection as it was, so
    a file that extracted fine last time keeps that result.
    """
    project = require_project(slug)
    if not file_name:
        if project.source is None:
            raise OperationFailed(f"{project.name} has no source file. Add one on Inputs.")
        file_name = project.source["name"]
    path = source_file_path(project, file_name)

    lock = _extraction_lock(project)
    if not lock.acquire(blocking=False):
        raise OperationFailed(
            f"Another file is being extracted in {project.name}. "
            f"Wait for it to finish, then extract {path.name}."
        )
    progress.report(slug, "extraction", 0, 0, f"Extracting {path.name}")
    try:
        options = extraction_options(project)
        assets = extraction_asset_sink(project)
        try:
            document = extract_document(
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
                transcribe_handwriting=options["handwriting_ocr"],
            )
        except SourceUnreadable as failure:
            logger.warning("extraction could not read a source: %s", failure)
            raise OperationFailed(str(failure)) from failure

        document = document.model_copy(update={"options_used": options})

        store = ExtractionCollectionStore(project.root)
        collection = store.save(Extraction(documents=[document], options_used=options))

        # Only now that the collection is on disk: pruning first and then failing
        # to save would lose the figures it still points at.
        confirmed = ExtractionStore(project.root).load()
        _prune_assets(assets, collection, confirmed)
    finally:
        progress.finish(slug, "extraction")
        lock.release()

    result = extraction_page(project, collection, confirmed)
    # What this run found, apart from where the collection stands.
    result["extracted"] = {
        "file_name": path.name,
        "block_count": len(document.blocks),
        "word_count": document.word_count,
        "warnings": [
            f"{assets.skipped_for_size} figure(s) were not extracted: this "
            f"project reached the extracted-image limit."
        ] if assets.skipped_for_size else [],
    }
    return result


def confirm_extraction(slug: str) -> dict[str, Any]:
    """Hand the collection to later stages. The one step that changes what they read.

    Refused while any file in it is out of date: confirming a result for a file
    that has since been replaced, or read with options that are no longer set,
    would hand on something that no longer matches what the page shows.
    """
    project = require_project(slug)
    collection = ExtractionCollectionStore(project.root).load()
    if not collection.documents:
        raise OperationFailed(
            f"The extraction collection for {project.name} is empty. "
            f"Extract at least one file first."
        )

    freshness = extraction_freshness(project, collection)
    out_of_date = [*freshness["removed"], *freshness["changed"], *freshness["options_changed"]]
    if out_of_date:
        raise OperationFailed(
            "Extract these again or remove them before "
            f"transferring to the next layer: {', '.join(sorted(set(out_of_date)))}."
        )

    confirmed = ExtractionStore(project.root).save(
        collection.model_copy(update={"confirmed_at": _now()}))
    _prune_assets(extraction_asset_sink(project), collection, confirmed)
    return extraction_page(project, collection, confirmed)


def preview_source(slug: str, file_name: str) -> dict[str, Any]:
    """Where a source file is and how it should be shown. Nothing is parsed.

    **This deliberately does no extraction.** Returning parsed text would put
    Extraction's work behind a chevron on the Inputs page: two places deciding
    what a document says, and the slower one running every time a row was opened.
    Inputs shows the file; Extraction reads it.

    The browser renders every format from the raw bytes, so what is on screen is
    the file on disk rather than a conversion of it.
    """
    project = require_project(slug)
    path = source_file_path(project, file_name)

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


def extracted_content_as_markdown(project: Project, *, collection: bool = False) -> str:
    """The extracted source text, for an agent's context. Empty if not extracted.

    Later stages read the confirmed extraction. The Extraction stage's own agent
    reads the collection, which is what its page is showing.
    """
    store = ExtractionCollectionStore if collection else ExtractionStore
    return store(project.root).load().as_markdown()
