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

import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from pipeline.extraction import BlockKind, Extraction
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_FIGURES = 2_000
MAXIMUM_NOTE_LENGTH = 300

# A picture below this in either direction is decoration: a bullet, a rule, a
# spacer. Kept in the library, but not proposed for use.
SMALLEST_USABLE_PIXELS = 64


class FigureUse:
    """Whether a picture should appear in the video."""

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

    use: str = FigureUse.UNDECIDED
    note: str = ""

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

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump() | {
            "where": self.where,
            "is_decoration": self.is_decoration,
        }


class ProjectLook(BaseModel):
    """How the video should look, taken from the source material."""

    # Off by default: a deck's styling is a decision, not an assumption, and a
    # video that silently adopted a client's brand colours would be worse than
    # one that asked.
    use_source_styling: bool = False

    from_file: str = ""
    aspect_ratio: str = ""
    theme_name: str = ""
    colours: dict[str, str] = Field(default_factory=dict)
    heading_font: str = ""
    body_font: str = ""
    background_colour: str = ""
    background_asset_path: str = ""

    @property
    def is_available(self) -> bool:
        return bool(self.colours or self.heading_font or self.background_asset_path)


class AssetLibrary(BaseModel):
    figures: list[LibraryFigure] = Field(default_factory=list)
    look: ProjectLook = Field(default_factory=ProjectLook)
    refreshed_at: str = ""

    @field_validator("figures")
    @classmethod
    def _cap_figures(cls, value: list[LibraryFigure]) -> list[LibraryFigure]:
        return value[:MAXIMUM_FIGURES]

    def usable(self) -> list[LibraryFigure]:
        """What the video may show: chosen, or undecided and not decoration."""
        return [
            figure for figure in self.figures
            if figure.in_extraction and (
                figure.use == FigureUse.USE
                or (figure.use == FigureUse.UNDECIDED and not figure.is_decoration)
            )
        ]

    def audit(self) -> dict[str, Any]:
        present = [figure for figure in self.figures if figure.in_extraction]
        return {
            "figure_count": len(present),
            "chosen_count": sum(1 for f in present if f.use == FigureUse.USE),
            "skipped_count": sum(1 for f in present if f.use == FigureUse.SKIP),
            "undecided_count": sum(1 for f in present if f.use == FigureUse.UNDECIDED),
            "decoration_count": sum(1 for f in present if f.is_decoration),
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
                f"{audit['gone_count']} picture(s) in this library are no longer in the "
                f"extraction. Their decisions are kept in case they come back."
            )
        if self.look.use_source_styling and not self.look.is_available:
            warnings.append(
                "The look is set to follow the source, but no styling was extracted. "
                "Switch on Extract styling and run extraction again."
            )
        return {
            "figures": [figure.to_dict() for figure in self.figures],
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


def look_from_extraction(extraction: Extraction) -> ProjectLook:
    """The styling of the first source document that has any.

    First rather than merged: two decks with different themes do not average
    into a third, and a video has one look.
    """
    for document in extraction.documents:
        if document.design is None:
            continue
        background = next(
            (slide.background for slide in document.slides if slide.background), None
        )
        return ProjectLook(
            from_file=document.file_name,
            aspect_ratio=document.design.aspect_ratio,
            theme_name=document.design.theme_name,
            colours=dict(document.design.colours),
            heading_font=document.design.major_font,
            body_font=document.design.minor_font,
            background_colour=background.colour if background else "",
            background_asset_path=background.asset_path if background else "",
        )
    return ProjectLook()


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
    from pipeline.extraction_review import _describe_picture

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

            measured = _describe_picture(project_root / block.asset_path)
            previous = decided.get(block.asset_path)
            figures.append(LibraryFigure(
                id=previous.id if previous else new_identifier(),
                asset_path=block.asset_path,
                block_id=block.id,
                file_name=document.file_name,
                heading_path=list(block.heading_path),
                caption=block.text,
                origin=block.asset_origin or "source",
                width=measured.get("width", 0) if measured["readable"] else 0,
                height=measured.get("height", 0) if measured["readable"] else 0,
                use=previous.use if previous else FigureUse.UNDECIDED,
                note=previous.note if previous else "",
                in_extraction=True,
            ))

    # Decisions about pictures the extraction no longer has.
    for asset_path, figure in decided.items():
        if asset_path not in seen:
            figures.append(figure.model_copy(update={"in_extraction": False}))

    look = existing.look
    fresh = look_from_extraction(extraction)
    if fresh.is_available:
        # The styling itself is re-read; whether to use it is the person's
        # choice and is never overwritten by a re-run.
        look = fresh.model_copy(update={"use_source_styling": look.use_source_styling})

    return AssetLibrary(figures=figures, look=look)
