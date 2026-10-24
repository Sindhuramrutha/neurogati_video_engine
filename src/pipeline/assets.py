"""Assets & Design — everything the video can show, and how it should look.

Extraction pulls pictures out of documents and knows nothing about which ones
matter: a deck yields sixty-three images, and a good half are bullets, logos and
divider rules. Planning then has to choose what to show while looking at a list
of file names. Nothing in between decided *which pictures are worth using*, and
nothing carried the deck's own colours and fonts forward, so a video made from a
branded deck came out in the renderer's defaults.

This stage is that decision, kept as an artifact:

- **The library** — one entry per extracted picture, with where it came from,
  what it measures, whether it came from the source, a person or a model, and
  whether it should be used. Decisions survive re-extraction: they are keyed by
  the picture's content, not by a block id that is regenerated every run.
- **The look** — the deck's aspect ratio, background, theme colours and fonts,
  taken from whichever source document has them, and a switch for whether the
  video should use them at all.

Stored at `projects/<slug>/assets/library.json`.
"""

from __future__ import annotations

import hashlib
import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from pipeline.core import OperationFailed, require_project
from pipeline.extraction import BlockKind, Extraction, ExtractionStore
from pipeline.project_look import ProjectLook, look_from_extraction  # noqa: F401 - re-exported
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

_GIVEN_CAPTION = re.compile(r"— figure \d+ \(slide \d+\)$")

MAXIMUM_FIGURES = 2_000
GATHERING_VERSION = 3
MAXIMUM_NOTE_LENGTH = 300

# A picture below this in either direction is decoration: a bullet, a rule, a
# spacer. Kept in the library, but not proposed for use.
SMALLEST_USABLE_PIXELS = 64


class FigureUse:
    """Whether a picture is handed on. `SKIP` is "left out"; anything else is
    included. `USE` is kept for libraries saved when this layer also judged."""

    UNDECIDED = "undecided"
    USE = "use"
    SKIP = "skip"


class LibraryFigure(BaseModel):
    """One extracted picture, and what was decided about it."""

    id: str = Field(default_factory=new_identifier)

    # The stored file is the identity that survives re-extraction. Block ids are
    # regenerated on every run, so keying decisions on them would throw away
    # every choice each time extraction ran.
    asset_path: str = ""
    block_id: str = ""

    file_name: str = ""
    heading_path: list[str] = Field(default_factory=list)
    caption: str = ""
    origin: str = "source"          # source | uploaded | generated
    width: int = 0
    height: int = 0

    # The trimmed copy, and what looking at the pixels found. A figure out of a
    # deck is whatever rectangle the file held -- a diagram with two inches of
    # slide around it, or a screenshot cropped through its own caption -- and
    # until this, nothing opened one to find out.
    prepared_path: str = ""
    prepared_width: int = 0
    prepared_height: int = 0
    trimmed_fraction: float = 0.0
    flags: list[str] = Field(default_factory=list)
    cut_edges: list[str] = Field(default_factory=list)

    # Where it came from, in the words a person uses: slide 2, "Padma's Story".
    slide_number: int = 0
    slide_title: str = ""

    use: str = FigureUse.UNDECIDED
    note: str = ""
    # The person's say over what gathering did to it: draw the file as it was
    # stored rather than the trimmed copy; and "I looked, the crop is right".
    use_original: bool = False
    crop_checked: bool = False

    # False once the extraction no longer contains it -- kept rather than
    # deleted, because a decision about a picture that came back is worth having.
    in_extraction: bool = True

    @field_validator("note")
    @classmethod
    def _cap_note(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_NOTE_LENGTH]

    @property
    def where(self) -> str:
        return " › ".join([self.file_name, *self.heading_path]) or self.file_name

    @property
    def is_decoration(self) -> bool:
        """Small enough that it is almost certainly furniture, not a diagram."""
        return bool(self.width and self.height) and (
            self.width < SMALLEST_USABLE_PIXELS or self.height < SMALLEST_USABLE_PIXELS
        )

    @property
    def is_unfit(self) -> bool:
        """Found to be blank, a sliver, unreadable, or too small once trimmed.

        Not proposed for use -- but still choosable, because this is a
        measurement and somebody looking at the picture knows more than it does.
        """
        from pipeline.figure_prep import DISQUALIFYING

        return bool(DISQUALIFYING.intersection(self.flags))

    @property
    def why_unfit(self) -> str:
        from pipeline.figure_prep import DISQUALIFYING, WHY

        return " ".join(WHY[flag] for flag in self.flags if flag in DISQUALIFYING)

    @property
    def name(self) -> str:
        """What a person would call it: the name they gave it, its slide, or else
        its caption."""
        if self.use == FigureUse.USE and self.note:
            return self.note
        if self.slide_number:
            return f"Slide {self.slide_number} · {self.slide_title}".rstrip(" ·")
        return self.caption or self.slide_title or self.asset_path.split("/")[-1]

    @property
    def is_left_out(self) -> bool:
        return self.use == FigureUse.SKIP

    @property
    def shown_path(self) -> str:
        """The file a frame draws: the trimmed copy, unless the original was chosen."""
        return self.asset_path if self.use_original or not self.prepared_path \
            else self.prepared_path

    @property
    def fills_a_frame(self) -> bool:
        """Large and clear enough to be a scene's picture. A fact about the
        picture, used by Generation where a scene's picture is chosen; this
        layer lists every picture and judges none."""
        return not self.is_decoration and not self.is_unfit

    @property
    def why_not_a_frame(self) -> str:
        if self.is_decoration:
            return f"Smaller than {SMALLEST_USABLE_PIXELS} px on a side."
        return self.why_unfit

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump() | {
            "where": self.where,
            "is_left_out": self.is_left_out,
            "is_chosen": self.use == FigureUse.USE,     # chosen on Extraction: shown
            "shown_path": self.shown_path,
            "fills_a_frame": self.fills_a_frame,
            "why_not_a_frame": self.why_not_a_frame,
            # A caption the source wrote, not the "figure 1 (slide 1)" label
            # extraction gives a picture that has none.
            "own_caption": "" if _GIVEN_CAPTION.search(self.caption) else self.caption,
            "needs_crop_check": "cut_off" in self.flags and not self.crop_checked,
        }


class AssetLibrary(BaseModel):
    figures: list[LibraryFigure] = Field(default_factory=list)
    look: ProjectLook = Field(default_factory=ProjectLook)
    refreshed_at: str = ""
    # Which transfer of the extraction this was gathered from. A newer transfer
    # re-gathers it, so the page always shows what the last layer handed on.
    gathered_from: str = ""
    # The version of gathering that made this. A library gathered by a lower
    # version is gathered again, once, so its pictures gain what is recorded
    # now (the slide each came from, the edges a crop touches). Choices are kept.
    gathered_version: int = 0

    @field_validator("figures")
    @classmethod
    def _cap_figures(cls, value: list[LibraryFigure]) -> list[LibraryFigure]:
        return value[:MAXIMUM_FIGURES]

    def handed_on(self) -> list[LibraryFigure]:
        """The deck pictures the video uses: the two or three a person chose and
        named (`chosen_pictures`). Every other picture is made for the video; the
        deck's own, offered to every scene, made a video look like its slides."""
        return [f for f in self.figures if f.in_extraction and f.use == FigureUse.USE]

    def usable(self) -> list[LibraryFigure]:
        """What a scene may show as its picture: handed on, and large and clear
        enough to fill a frame. (A picture someone chose with "Use" is always
        usable: they looked at it and said so.)"""
        return [f for f in self.handed_on()
                if f.fills_a_frame or f.use == FigureUse.USE]

    def audit(self) -> dict[str, Any]:
        present = [figure for figure in self.figures if figure.in_extraction]
        return {
            "figure_count": len(present),
            "handed_on_count": len(self.handed_on()),
            "left_out_count": sum(1 for f in present if f.is_left_out),
            "decoration_count": sum(1 for f in present if f.is_decoration),
            "unfit_count": sum(1 for f in present if f.is_unfit),
            "trimmed_count": sum(1 for f in present if f.prepared_path),
            "usable_count": len(self.usable()),
            "gone_count": sum(1 for f in self.figures if not f.in_extraction),
            "generated_count": sum(1 for f in present if f.origin == "generated"),
            "uploaded_count": sum(1 for f in present if f.origin == "uploaded"),
        }

    def to_dict(self) -> dict[str, Any]:
        audit = self.audit()
        warnings: list[str] = []
        if audit["gone_count"]:
            warnings.append(
                f"{audit['gone_count']} picture(s) from earlier transfers are not in the "
                f"last one, so they are not handed on. Your choices about them are kept "
                f"in case they come back; Clear everything forgets them."
            )
        if self.look.use_source_styling and not self.look.is_available:
            warnings.append(
                "The look is set to follow the source, but no styling was extracted. "
                "Switch on Extract styling and run extraction again."
            )
        return {
            # Only what the last transfer has. Pictures from earlier ones stay in
            # the file, with their decisions, and are counted, not listed.
            "figures": [figure.to_dict() for figure in self.figures if figure.in_extraction],
            # Named, not counted: what an earlier transfer had and this one does not.
            "gone_figures": [f.name for f in self.figures if not f.in_extraction],
            "look": self.look.model_dump() | {"is_available": self.look.is_available},
            "refreshed_at": self.refreshed_at,
            "audit": audit,
            "warnings": warnings,
            "is_empty": not self.figures,
        }


def default_asset_library() -> AssetLibrary:
    return AssetLibrary()


class AssetLibraryStore(JsonDocumentStore[AssetLibrary]):
    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.ASSETS),
            model_type=AssetLibrary,
            build_default=default_asset_library,
            description="asset library",
        )


def _figure_id(asset_path: str) -> str:
    return hashlib.sha256(asset_path.encode("utf-8")).hexdigest()[:12]


def rebuild_library(
    project_root: Path, extraction: Extraction, existing: AssetLibrary
) -> AssetLibrary:
    """The library as the current extraction sees it, keeping every decision.

    A picture is matched by its stored file, so re-running extraction -- which
    regenerates every block id -- does not lose the choice someone made about
    each one. A picture the extraction no longer has is marked rather than
    dropped: deleting the decision would mean making it again if the file comes
    back.
    """
    from pipeline.figure_prep import prepare_figure

    decided = {figure.asset_path: figure for figure in existing.figures if figure.asset_path}
    figures: list[LibraryFigure] = []
    seen: set[str] = set()

    for document in extraction.documents:
        for block in document.blocks:
            if block.kind != BlockKind.FIGURE or not block.asset_path:
                continue
            if block.asset_path in seen:
                continue
            seen.add(block.asset_path)

            # Opened, trimmed and judged. The measurement is what makes the
            # difference between a library of file names and a library of
            # pictures somebody could actually put on a frame.
            prepared = prepare_figure(project_root, block.asset_path)
            previous = decided.get(block.asset_path)
            figures.append(LibraryFigure(
                # From the picture itself, so the same picture always has the
                # same id -- after a clear, a re-extraction, on any machine.
                id=previous.id if previous else _figure_id(block.asset_path),
                asset_path=block.asset_path,
                block_id=block.id,
                file_name=document.file_name,
                heading_path=list(block.heading_path),
                caption=block.text,
                origin=block.asset_origin or "source",
                width=prepared.width,
                height=prepared.height,
                prepared_path=prepared.prepared_path,
                prepared_width=prepared.prepared_width,
                prepared_height=prepared.prepared_height,
                trimmed_fraction=prepared.trimmed_fraction,
                flags=list(prepared.flags),
                cut_edges=list(prepared.cut_edges),
                slide_number=block.slide_number,
                slide_title=block.heading_path[-1] if block.heading_path else "",
                use=previous.use if previous else FigureUse.UNDECIDED,
                note=previous.note if previous else "",
                use_original=previous.use_original if previous else False,
                crop_checked=previous.crop_checked if previous else False,
                in_extraction=True,
            ))

    # Decisions about pictures the extraction no longer has.
    for asset_path, figure in decided.items():
        if asset_path not in seen:
            figures.append(figure.model_copy(update={"in_extraction": False}))

    look = existing.look
    fresh = look_from_extraction(extraction, prefer=look.from_file)
    if fresh.is_available:
        # The styling itself is re-read; whether to use it, and every choice on
        # top of it, is the person's and is never overwritten by a re-run.
        same = fresh.from_file == look.from_file
        look = fresh.model_copy(update={"use_source_styling": look.use_source_styling,
                                        "slide_wash": look.slide_wash,
                                        "background_art": look.background_art,
                                        "choices": look.choices if same else {}})

    from pipeline.chosen_pictures import mark

    return mark(AssetLibrary(figures=figures, look=look), project_root)


# --- what a client calls -----------------------------------------------------


def read_asset_library(slug: str) -> dict[str, Any]:
    """The library, re-gathered first if the extraction was transferred since.

    Gathering on a press of the button alone would leave the page showing the
    previous transfer's pictures. Decisions are kept either way.
    """
    project = require_project(slug)
    store = AssetLibraryStore(project.root)
    library = store.load()
    extraction = ExtractionStore(project.root).load()
    transferred = extraction.confirmed_at or extraction.extracted_at
    behind = library.gathered_from != transferred or library.gathered_version < GATHERING_VERSION
    if library.figures and transferred and behind:
        return _gather(project, extraction, library, store)
    return library.to_dict()

def refresh_asset_library(slug: str, clear: bool = False) -> dict[str, Any]:
    """Bring the library in step with the transferred extraction, keeping
    decisions -- or, `clear`, empty it: every picture and every decision gone.

    Cleared, it stays empty until someone gathers again: gathering straight
    away would put the same pictures back and look like the button did nothing.
    """
    project = require_project(slug)
    store = AssetLibraryStore(project.root)
    if clear:
        return store.save(AssetLibrary()).to_dict()
    extraction = ExtractionStore(project.root).load()
    if not extraction.documents:
        raise OperationFailed(
            f"{project.name} has nothing extracted yet, so there are "
            f"no pictures to gather. Extract and transfer it first."
        )
    return _gather(project, extraction, store.load(), store)


def _gather(project, extraction: Extraction, existing: AssetLibrary, store) -> dict[str, Any]:
    rebuilt = rebuild_library(project.root, extraction, existing)
    rebuilt.refreshed_at = datetime.now(UTC).isoformat(timespec="seconds")
    rebuilt.gathered_from = extraction.confirmed_at or extraction.extracted_at
    rebuilt.gathered_version = GATHERING_VERSION
    return store.save(rebuilt).to_dict()

def decide_figure(
    slug: str, figure_id: str, use: str, note: str | None = None
) -> dict[str, Any]:
    """Say whether a picture should be used, and why."""
    if use not in {FigureUse.USE, FigureUse.SKIP, FigureUse.UNDECIDED}:
        raise OperationFailed(
            f"{use!r} is not a decision. Use one of: "
            f"{FigureUse.USE}, {FigureUse.SKIP}, {FigureUse.UNDECIDED}."
        )

    project = require_project(slug)
    store = AssetLibraryStore(project.root)
    library = store.load()
    figure = next((f for f in library.figures if f.id == figure_id), None)
    if figure is None:
        raise OperationFailed(f"This library has no picture {figure_id!r}.")

    figure.use = use
    if note is not None:
        figure.note = note
    return store.save(library).to_dict()

def set_picture(slug: str, figure_id: str, changes: dict[str, Any]) -> None:
    """The three things a person can say about a picture: leave it out (or put
    it back), draw the original rather than the trimmed copy, and "the crop is
    right"."""
    project = require_project(slug)
    store = AssetLibraryStore(project.root)
    library = store.load()
    figure = next((f for f in library.figures if f.id == figure_id), None)
    if figure is None:
        raise OperationFailed(f"This library has no picture {figure_id!r}.")
    if "left_out" in changes:
        figure.use = FigureUse.SKIP if changes["left_out"] else FigureUse.UNDECIDED
    if "use_original" in changes:
        figure.use_original = bool(changes["use_original"])
    if "crop_checked" in changes:
        figure.crop_checked = bool(changes["crop_checked"])
    store.save(library)


def set_project_look(slug: str, use_source_styling: bool) -> dict[str, Any]:
    """Whether the video follows the source deck's colours and fonts."""
    project = require_project(slug)
    store = AssetLibraryStore(project.root)
    library = store.load()
    library.look.use_source_styling = bool(use_source_styling)
    return store.save(library).to_dict()
