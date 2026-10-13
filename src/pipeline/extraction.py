"""Extraction — pull structured content out of the source documents.

The later agents read this text, not file names: an agent asked to plan a video
about a document it cannot read invents a plausible plan about the title.

The output is deliberately **structural, not summarised**. Headings stay
headings, tables stay tables, and nothing is paraphrased on the way in. Summarising
here would put an unreviewable lossy step between the source and every later
stage -- and when a fact went wrong nobody could tell whether the source was
wrong, the extraction dropped it, or the planner invented it. Blocks carry the
file and the heading path they came from, so any claim downstream can be traced
back to a place in a document.

No model is called. This is parsing, and a parser that is wrong is debuggable in
a way that a model that hallucinated a heading is not.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from pipeline.deck_shapes import (
    DRAWING_NAMESPACE,
    _aspect_ratio,
    _caption_near,
    _first_run_style,
    _headline_of,
    _inherited_list_styles,
    _is_bulleted,
    _is_card_title,
    _shape_box,
    _shape_kind,
    _title_element,
)
from pipeline.extraction_assets import (  # re-exported: readers and tests use them
    MAXIMUM_EXTRACTED_ASSET_BYTES,  # noqa: F401
    AssetSink,
)
from pipeline.slide_background import SlideBackground, slide_background  # re-exported
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_BLOCK_LENGTH = 20000
MAXIMUM_BLOCKS_PER_DOCUMENT = 5000

# A slide with more shapes than this is a diagram drawn by hand; its geometry is
# not something a video can reproduce anyway, and keeping all of it would bloat
# the extraction for no gain.
MAXIMUM_SHAPES_PER_SLIDE = 60
MAXIMUM_SHAPE_TEXT_LENGTH = 300

# Word counts are what the Planning stage reasons about when estimating spoken
# duration, so they are computed once here rather than re-derived per stage.
WORDS_PER_MINUTE_OF_NARRATION = 150


class BlockKind:
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"
    FIGURE = "figure"


class ContentBlock(BaseModel):
    """One piece of a source document, kept in document order.

    `heading_path` is what makes a block quotable: "the 400 Hz figure came from
    2.2 Electrodes and Sensors > 2.2.3 Impedance" is a checkable statement, and
    a flat list of paragraphs cannot produce one.
    """

    id: str = Field(default_factory=new_identifier)
    kind: str = BlockKind.PARAGRAPH
    level: int = 0
    text: str = ""
    heading_path: list[str] = Field(default_factory=list)

    # Where the extracted image was written, relative to the project root. Only
    # a FIGURE block has one. Text extraction alone dropped every diagram on the
    # floor: a document could say "as Figure 2.1 shows" and nothing downstream
    # had any figure to show, so Studio narrated a picture that did not exist.
    asset_path: str = ""

    # Where that picture came from: the source document, a person, or a model.
    # A drawn picture is not the author's diagram, and a video that shows one as
    # if it were is making a claim about the source material that is not true.
    asset_origin: str = "source"   # source | uploaded | generated

    # Which slide or page this came from, 1-based, or 0 for a source that has
    # neither. The heading path was the only clue before, and for a deck it is
    # just the slide's title -- so two slides with the same title collapsed into
    # one location, and a video could not be built to follow the deck's order.
    slide_number: int = 0

    # Read off a page image by the vision model rather than parsed from the file.
    transcribed: bool = False

    @field_validator("text")
    @classmethod
    def _cap_text(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_BLOCK_LENGTH]

    @property
    def word_count(self) -> int:
        return len(self.text.split())


class LayoutShape(BaseModel):
    """One shape on a slide, and where it sits.

    Positions are fractions of the slide, not EMUs or pixels: a deck can be 4:3
    or 16:9 and the video is neither, so the only number that survives the
    journey is "38% across, 12% down".
    """

    kind: str = "other"     # title | text | picture | table | chart | other
    left: float = 0.0
    top: float = 0.0
    width: float = 0.0
    height: float = 0.0
    z: int = 0              # back to front, as PowerPoint stacks them
    text: str = ""          # a preview; the words themselves are blocks
    asset_path: str = ""    # a picture's stored copy
    font_size_pt: float = 0.0
    bold: bool = False
    align: str = ""

    @field_validator("text")
    @classmethod
    def _cap_text(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SHAPE_TEXT_LENGTH]


class SlideLayout(BaseModel):
    number: int = 0
    title: str = ""
    layout_name: str = ""
    shapes: list[LayoutShape] = Field(default_factory=list)
    background: SlideBackground | None = None

    @field_validator("shapes")
    @classmethod
    def _cap_shapes(cls, value: list[LayoutShape]) -> list[LayoutShape]:
        return value[:MAXIMUM_SHAPES_PER_SLIDE]


class DocumentDesign(BaseModel):
    """The deck's own styling: its proportions, colours and fonts.

    Kept so a video made from a deck can look like the deck instead of like the
    renderer's defaults.
    """

    aspect_ratio: str = ""          # "16:9"
    slide_width_emu: int = 0
    slide_height_emu: int = 0
    theme_name: str = ""
    colours: dict[str, str] = Field(default_factory=dict)
    major_font: str = ""
    minor_font: str = ""


class ExtractedDocument(BaseModel):
    file_name: str = ""
    blocks: list[ContentBlock] = Field(default_factory=list)
    extraction_note: str = ""

    # Only decks have these, and only when the options are on. Kept out of the
    # markdown an agent reads: a hundred shape boxes would drown the words.
    slides: list[SlideLayout] = Field(default_factory=list)
    design: DocumentDesign | None = None

    # Each file is extracted on its own, so each carries its own run: from a
    # file of what size, and with which options -- what says whether this copy
    # still matches the file and the settings.
    source_bytes: int = 0
    options_used: dict[str, bool] = Field(default_factory=dict)

    @field_validator("blocks")
    @classmethod
    def _cap_blocks(cls, value: list[ContentBlock]) -> list[ContentBlock]:
        return value[:MAXIMUM_BLOCKS_PER_DOCUMENT]

    @property
    def word_count(self) -> int:
        return sum(block.word_count for block in self.blocks)

    def blocks_under(self, heading_path: list[str]) -> list[ContentBlock]:
        """Every block filed under this heading, including the heading itself.

        A heading path is a *location*, and locations are how a plan points at
        content: block ids are generated afresh on every run, so a plan holding
        them would lose every reference the next time extraction ran. An empty
        path means the whole document.
        """
        depth = len(heading_path)
        return [block for block in self.blocks if block.heading_path[:depth] == heading_path]

    def has_location(self, heading_path: list[str]) -> bool:
        return bool(self.blocks_under(heading_path))

    def heading_outline(self) -> list[dict]:
        """Every heading with the number of words filed under it, in order.

        This is what lets a planner see a whole source at once: the headings of a
        long chapter fit easily where its full text would not, and the word count
        says how much material sits behind each one.
        """
        outline = []
        for block in self.blocks:
            if block.kind != BlockKind.HEADING:
                continue
            words = sum(
                under.word_count for under in self.blocks_under(block.heading_path)
                if under.kind != BlockKind.HEADING
            )
            outline.append({
                "heading_path": list(block.heading_path),
                "level": block.level,
                "words": words,
            })
        return outline

    def text_under(self, heading_path: list[str]) -> str:
        """The markdown of one location, in document order."""
        return ExtractedDocument(
            file_name=self.file_name, blocks=self.blocks_under(heading_path)
        ).as_markdown()

    def as_markdown(self) -> str:
        """The document as text a model can read.

        Markdown rather than the JSON: heading levels survive as `##`, which is a
        shape every model already understands, and it costs a fraction of the
        tokens that the block objects would.
        """
        lines: list[str] = []
        for block in self.blocks:
            if block.kind == BlockKind.HEADING:
                lines.append(f"\n{'#' * max(1, min(block.level, 6))} {block.text}")
            elif block.kind == BlockKind.LIST_ITEM:
                lines.append(f"- {block.text}")
            elif block.kind == BlockKind.TABLE:
                lines.append(f"\n{block.text}\n")
            elif block.kind == BlockKind.FIGURE:
                # Marked as a figure so the planner knows a real image exists at
                # this point and can plan to show it, instead of reading the
                # caption as one more sentence of prose.
                lines.append(f"[figure: {block.text}]")
            else:
                lines.append(block.text)
        return "\n".join(lines).strip()


class Extraction(BaseModel):
    documents: list[ExtractedDocument] = Field(default_factory=list)
    extracted_at: str = ""
    # The options this run honoured. Kept so a changed toggle can be reported as
    # "out of date" -- otherwise switching figures off leaves the page saying 70
    # figures were extracted, which is true of a run that no longer matches.
    options_used: dict[str, bool] = Field(default_factory=dict)
    # When this collection was confirmed and handed to later stages. Empty on
    # the collection still being assembled on the Extraction page.
    confirmed_at: str = ""

    @property
    def total_word_count(self) -> int:
        return sum(document.word_count for document in self.documents)

    def document(self, file_name: str) -> ExtractedDocument | None:
        return next((d for d in self.documents if d.file_name == file_name), None)

    def has_location(self, file_name: str, heading_path: list[str]) -> bool:
        document = self.document(file_name)
        return document is not None and document.has_location(heading_path)

    def content_fingerprint(self) -> str:
        """An identity for what this extraction *says*, for knowing when a plan
        built on it is out of date.

        Built from each document's name and its blocks' kind, location and text.
        Block ids are left out because they are regenerated on every run -- a
        fingerprint that included them would call every plan stale after a
        re-extraction that changed nothing. Figures are left out too: switching
        figure extraction off changes what can be shown, not what is taught.
        """
        if not self.documents:
            return ""
        digest = hashlib.sha256()
        for document in sorted(self.documents, key=lambda d: d.file_name):
            digest.update(document.file_name.encode("utf-8") + b"\0")
            for block in document.blocks:
                if block.kind == BlockKind.FIGURE:
                    continue
                digest.update(json.dumps(
                    [block.kind, block.heading_path, block.text], ensure_ascii=False
                ).encode("utf-8") + b"\0")
        return digest.hexdigest()[:16]

    def asset_paths(self) -> set[str]:
        """Every stored picture this extraction points at: figures and backgrounds."""
        return {
            *(b.asset_path for d in self.documents for b in d.blocks if b.asset_path),
            *(s.background.asset_path for d in self.documents for s in d.slides
              if s.background is not None and s.background.asset_path),
            *(shape.asset_path for d in self.documents for s in d.slides
              for shape in s.shapes if shape.asset_path),
        }

    def as_markdown(self) -> str:
        return "\n\n".join(
            f"===== {document.file_name} =====\n{document.as_markdown()}"
            for document in self.documents
        )

    def audit(self) -> dict:
        return {
            "document_count": len(self.documents),
            "block_count": sum(len(d.blocks) for d in self.documents),
            "empty_document_names": [d.file_name for d in self.documents if not d.blocks],
            "heading_count": sum(
                1 for d in self.documents for b in d.blocks if b.kind == BlockKind.HEADING
            ),
            "figure_count": sum(
                1 for d in self.documents for b in d.blocks if b.kind == BlockKind.FIGURE
            ),
            # Stated, because an option that captured nothing looks exactly like
            # one that was never on.
            # Slides with shapes, not slides: a design-only run still records a
            # slide for its background, and counting those would claim layout
            # was captured when it was switched off.
            "slide_layout_count": sum(
                1 for d in self.documents for s in d.slides if s.shapes
            ),
            "slide_background_count": sum(
                1 for d in self.documents for s in d.slides if s.background is not None
            ),
            # Pictures, not colours: a colour behind a slide is styling, while a
            # background image is a picture the video can actually show.
            "background_image_count": sum(
                1 for d in self.documents for s in d.slides
                if s.background is not None and s.background.asset_path
            ),
            "themed_document_names": [
                d.file_name for d in self.documents if d.design and d.design.theme_name
            ],
        }

    def to_dict(self) -> dict:
        audit = self.audit()
        estimated_minutes = round(
            self.total_word_count / WORDS_PER_MINUTE_OF_NARRATION, 1
        )
        return self.model_dump(mode="json") | {
            "total_word_count": self.total_word_count,
            "estimated_narration_minutes": estimated_minutes,
            "audit": audit,
            "warnings": self._warnings(audit),
            "is_empty": not self.documents,
        }

    def _warnings(self, audit: dict) -> list[str]:
        found: list[str] = []
        if audit["empty_document_names"]:
            found.append(
                f"nothing could be read from: {', '.join(audit['empty_document_names'])}"
            )
        if self.documents and not audit["heading_count"]:
            found.append(
                "no headings were found, so the planner has no structure to follow"
            )
        return found


class ExtractionStore(JsonDocumentStore[Extraction]):
    """Persistence for the extracted content."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.EXTRACTION),
            model_type=Extraction,
            build_default=Extraction,
            description="extraction",
        )

    @property
    def extraction_path(self) -> Path:
        return self.document_path


class ExtractionCollectionStore(JsonDocumentStore[Extraction]):
    """The collection being assembled on the Extraction page, one file at a time.

    Not what later stages read: that is `ExtractionStore`, written only when the
    collection is confirmed. A half-built collection -- two decks extracted, a
    third still to go -- must not reach the planner as if it were the source.

    A project from before collections has only the confirmed extraction; it
    becomes the starting collection, so nothing already extracted disappears.
    """

    def __init__(self, project_root: Path) -> None:
        self.confirmed = ExtractionStore(project_root)
        super().__init__(
            document_path=self.confirmed.document_path.with_name("collection.json"),
            model_type=Extraction,
            build_default=Extraction,
            description="extraction collection",
        )

    def load(self) -> Extraction:
        return super().load() if self.document_path.exists() else self.confirmed.load()

    def save(self, document: Extraction) -> Extraction:
        """Stamped on every save, to the microsecond.

        Whether the collection differs from what was confirmed is decided by
        comparing this stamp with the confirmed copy's, so it is set here rather
        than by each writer -- one that forgot would leave a change looking
        already handed on.
        """
        from datetime import UTC, datetime

        return super().save(document.model_copy(update={
            "extracted_at": datetime.now(UTC).isoformat(timespec="microseconds"),
        }))


# --- readers ----------------------------------------------------------------
#
# One per format. Each returns blocks in document order, or raises with a
# message naming the file -- an extraction that silently yields nothing looks
# identical to an empty document, and the two need different fixes.


class SourceUnreadable(Exception):
    """A source file could not be parsed. Names the file and the reason."""


def _heading_level(style_name: str) -> int:
    """Word's heading styles are 'Heading 1'..'Heading 9'."""
    digits = "".join(character for character in style_name if character.isdigit())
    return int(digits) if digits else 1


def _render_table(table) -> str:
    """A table as pipe rows, so its shape survives into the markdown a model reads."""
    rows = [
        " | ".join(cell.text.strip().replace("\n", " ") for cell in row.cells)
        for row in table.rows
    ]
    return "\n".join(row for row in rows if row.replace("|", "").strip())


def _walk_document_body(document):
    """Paragraphs and tables, interleaved, in the order they appear on the page.

    `document.paragraphs` and `document.tables` are two separate sequences, so
    the obvious reading -- all the paragraphs, then all the tables -- puts every
    table at the end of the document under whatever heading happened to come
    last. In a real chapter that meant a comparison table belonging to 2.2.9
    filed under the closing summary, which is not a cosmetic ordering problem:
    `heading_path` is what makes a block quotable, and it was pointing at the
    wrong section.

    The body's own XML children are already in document order, so walking those
    and wrapping each one is the only reading that matches the file.

    Yields `("paragraph" | "table", item)`. The tag is explicit because the two
    wrapper classes share enough of an interface to be mistaken for each other.
    """
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield "paragraph", Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield "table", Table(child, document)


def _paragraph_images(paragraph, document) -> list[tuple[str, bytes]]:
    """Every image anchored in this paragraph, as (extension, bytes).

    Found through the drawing relationships rather than `document.part.image_parts`
    so each image is tied to the paragraph it sits in -- which is what gives a
    figure its position and its caption.
    """
    from docx.oxml.ns import qn

    found = []
    for blip in paragraph._element.findall(f".//{qn('a:blip')}"):
        relationship_id = blip.get(qn("r:embed")) or blip.get(qn("r:link"))
        if not relationship_id:
            continue
        try:
            part = document.part.related_parts[relationship_id]
        except KeyError:
            continue
        blob = getattr(part, "blob", None)
        if not blob:
            continue
        suffix = Path(str(getattr(part, "partname", ".png"))).suffix or ".png"
        found.append((suffix, blob))
    return found


def read_docx(path: Path, assets: AssetSink | None = None) -> list[ContentBlock]:
    import docx

    document = docx.Document(str(path))
    blocks: list[ContentBlock] = []
    heading_path: list[str] = []
    figure_number = 0

    for kind, item in _walk_document_body(document):
        if kind == "table":
            # It takes the heading path current *at this point in the document*,
            # which is the whole reason for walking in order. Tagged rather than
            # sniffed: a python-docx `Table` has a `.style` just as a paragraph
            # does, so telling them apart by attribute silently sends tables
            # down the paragraph branch.
            rendered = _render_table(item)
            if rendered:
                blocks.append(ContentBlock(
                    kind=BlockKind.TABLE, text=rendered, heading_path=list(heading_path),
                ))
            continue

        paragraph = item
        text = paragraph.text.strip()
        style_name = (paragraph.style.name or "").lower()

        # Images first: a figure usually sits in a paragraph of its own, so
        # checking text alone skips it entirely.
        for suffix, blob in _paragraph_images(paragraph, document):
            figure_number += 1
            caption = text or f"Figure {figure_number} from {path.name}"
            stored = assets.store(blob, suffix) if assets else ""
            blocks.append(ContentBlock(
                kind=BlockKind.FIGURE, text=caption,
                heading_path=list(heading_path), asset_path=stored,
            ))

        if not text:
            continue

        if style_name.startswith("heading"):
            level = _heading_level(paragraph.style.name)
            # Keep the path to this heading, dropping any deeper headings it
            # replaces, so every later block knows where in the document it sits.
            heading_path = heading_path[: level - 1] + [text]
            blocks.append(ContentBlock(
                kind=BlockKind.HEADING, level=level, text=text,
                heading_path=list(heading_path),
            ))
        elif style_name.startswith("list"):
            blocks.append(ContentBlock(
                kind=BlockKind.LIST_ITEM, text=text, heading_path=list(heading_path),
            ))
        else:
            blocks.append(ContentBlock(
                kind=BlockKind.PARAGRAPH, text=text, heading_path=list(heading_path),
            ))

    return blocks


def read_pdf(path: Path) -> list[ContentBlock]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    blocks: list[ContentBlock] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue
        blocks.append(ContentBlock(
            kind=BlockKind.HEADING, level=2, text=f"Page {page_number}",
            heading_path=[f"Page {page_number}"],
        ))
        for chunk in (part.strip() for part in text.split("\n\n")):
            if chunk:
                blocks.append(ContentBlock(
                    kind=BlockKind.PARAGRAPH, text=chunk,
                    heading_path=[f"Page {page_number}"],
                ))
    return blocks


def read_plain_text(path: Path) -> list[ContentBlock]:
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks: list[ContentBlock] = []
    heading_path: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title = line.lstrip("#").strip()
            heading_path = heading_path[: level - 1] + [title]
            blocks.append(ContentBlock(
                kind=BlockKind.HEADING, level=level, text=title,
                heading_path=list(heading_path),
            ))
        elif line.startswith(("- ", "* ")):
            blocks.append(ContentBlock(
                kind=BlockKind.LIST_ITEM, text=line[2:].strip(),
                heading_path=list(heading_path),
            ))
        else:
            blocks.append(ContentBlock(
                kind=BlockKind.PARAGRAPH, text=line, heading_path=list(heading_path),
            ))
    return blocks


def read_pptx(path: Path, assets: AssetSink | None = None) -> list[ContentBlock]:
    """One heading per slide, then its text and tables.

    `.pptx` was accepted on upload and advertised on the Inputs page from the
    start, with no reader behind it: a deck uploaded fine and then dead-ended at
    extraction with "no reader for .pptx". Advertising a format the pipeline
    cannot read is worse than refusing it.
    """
    from pptx import Presentation
    from pptx.shapes.picture import Picture

    presentation = Presentation(str(path))
    blocks: list[ContentBlock] = []
    figure_number = 0

    for number, slide in enumerate(presentation.slides, start=1):
        # A slide's own title if it has one, so the heading path means something.
        title = ""
        title_element = _title_element(slide)
        if slide.shapes.title is not None and slide.shapes.title.has_text_frame:
            title = slide.shapes.title.text.strip()
        headline, headline_element = ("", None) if title else _headline_of(slide)
        heading = title or headline or f"Slide {number}"
        heading_path = [heading]

        blocks.append(ContentBlock(
            kind=BlockKind.HEADING, level=2, text=heading, heading_path=list(heading_path),
            slide_number=number,
        ))

        # Lines already used as the heading or a figure caption, by the text box
        # they sit in, so the walk below does not emit them again as paragraphs.
        # Only the line is dropped: the box may carry body text under it. A card's
        # bold title is kept, as a heading, though it also captions its icon.
        consumed: set[tuple[object, str]] = {(headline_element, heading)}
        captions: dict[object, str] = {}
        for shape in slide.shapes:
            if not isinstance(shape, Picture):
                continue
            caption, element = _caption_near(shape, slide)
            if element is not None:
                captions[shape._element] = caption
                if not _is_card_title(element):
                    consumed.add((element, caption))

        for shape in slide.shapes:
            if shape._element is title_element:
                continue
            if shape.has_text_frame:
                list_styles = _inherited_list_styles(shape, slide)
                for paragraph in shape.text_frame.paragraphs:
                    line = "".join(run.text for run in paragraph.runs).strip()
                    if not line or (shape._element, line) in consumed:
                        continue
                    # Bulleted lines stay list items so the structure survives.
                    kind = (BlockKind.HEADING if _is_card_title(shape._element)
                            else BlockKind.LIST_ITEM if _is_bulleted(paragraph, list_styles)
                            else BlockKind.PARAGRAPH)
                    blocks.append(ContentBlock(
                        kind=kind, level=3 if kind == BlockKind.HEADING else 0,
                        text=line, heading_path=list(heading_path),
                        slide_number=number,
                    ))
            elif getattr(shape, "has_table", False):
                rendered = _render_table(shape.table)
                if rendered:
                    blocks.append(ContentBlock(
                        kind=BlockKind.TABLE, text=rendered, heading_path=list(heading_path),
                        slide_number=number,
                    ))
            else:
                # A picture. Slides carry most of their meaning in diagrams, so a
                # text-only reading of a deck loses more than it keeps.
                image = getattr(shape, "image", None)
                if image is None:
                    continue
                figure_number += 1
                caption = captions.get(shape._element) or f"{heading} — figure {figure_number}"
                blocks.append(ContentBlock(
                    kind=BlockKind.FIGURE,
                    text=f"{caption} (slide {number})",
                    heading_path=list(heading_path),
                    asset_path=assets.store(image.blob, f".{image.ext}") if assets else "",
                    slide_number=number,
                ))

        if slide.has_notes_slide:
            notes = (slide.notes_slide.notes_text_frame.text or "").strip()
            if notes:
                blocks.append(ContentBlock(
                    kind=BlockKind.PARAGRAPH, text=f"[speaker notes] {notes}",
                    heading_path=list(heading_path),
                    slide_number=number,
                ))

    return blocks



def _deck_theme(presentation) -> tuple[str, dict[str, str], str, str]:
    """The theme's name, colour scheme and fonts, read from the theme part."""
    from lxml import etree
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT

    try:
        theme_part = presentation.slide_masters[0].part.part_related_by(RT.THEME)
        root = etree.fromstring(theme_part.blob)
    except (KeyError, IndexError, AttributeError, etree.XMLSyntaxError) as unreadable:
        logger.warning("the deck theme could not be read: %s", unreadable)
        return "", {}, "", ""

    namespaces = {"a": DRAWING_NAMESPACE}
    colours: dict[str, str] = {}
    scheme = root.find(".//a:clrScheme", namespaces)
    for entry in scheme if scheme is not None else []:
        name = entry.tag.split("}")[-1]
        value = next(iter(entry), None)
        if value is None:
            continue
        # A system colour (window, windowText) names itself in `val` and states
        # what that resolves to in `lastClr`. Taking `val` first would record
        # the theme's darkest colour as "#WINDOWTEXT".
        is_system = value.tag.endswith("}sysClr")
        hex_value = (value.get("lastClr") if is_system else value.get("val")) or ""
        if hex_value and not hex_value.startswith("#"):
            hex_value = f"#{hex_value.upper()}"
        colours[name] = hex_value

    def typeface(which: str) -> str:
        found = root.find(f".//a:fontScheme/a:{which}Font/a:latin", namespaces)
        return (found.get("typeface") or "") if found is not None else ""

    return root.get("name") or "", colours, typeface("major"), typeface("minor")


def read_pptx_design(
    path: Path,
    assets: AssetSink | None = None,
    *,
    capture_layout: bool = True,
    capture_backgrounds: bool = True,
    capture_styling: bool = True,
    store_pictures: bool = True,
) -> tuple[list[SlideLayout], DocumentDesign | None]:
    """How a deck is put together: where things sit, and how it is styled.

    Separate from `read_pptx` deliberately. The readers all answer the same
    question -- what does this document say -- and every one of them returns
    blocks. This answers a different question, for a different consumer: the
    renderer, which needs to place a picture where the slide placed it rather
    than re-typeset the words.
    """
    from pptx import Presentation

    presentation = Presentation(str(path))
    slide_width = presentation.slide_width or 0
    slide_height = presentation.slide_height or 0

    # The theme is read whenever either option is on: a slide that sets no
    # background of its own has the theme's light colour behind it, so resolving
    # a background needs the colour scheme even when the styling is not kept.
    design = None
    colours: dict[str, str] = {}
    if capture_styling or capture_backgrounds:
        theme_name, colours, major, minor = _deck_theme(presentation)
    if capture_styling:
        design = DocumentDesign(
            aspect_ratio=_aspect_ratio(slide_width, slide_height),
            slide_width_emu=slide_width, slide_height_emu=slide_height,
            theme_name=theme_name, colours=colours,
            major_font=major, minor_font=minor,
        )

    slides: list[SlideLayout] = []
    if not capture_layout and not capture_backgrounds:
        return slides, design
    if not slide_width or not slide_height:
        return slides, design

    for number, slide in enumerate(presentation.slides, start=1):
        shapes: list[LayoutShape] = []
        title_element = _title_element(slide)
        if capture_layout:
            for z, shape in enumerate(slide.shapes):
                left, top, width, height = _shape_box(
                    shape, slide, slide_width, slide_height)
                font_size, bold, align = _first_run_style(shape)
                image = getattr(shape, "image", None)
                shapes.append(LayoutShape(
                    kind=_shape_kind(shape, title_element),
                    left=left, top=top, width=width, height=height, z=z,
                    text=shape.text_frame.text if shape.has_text_frame else "",
                    # Geometry only when figures are switched off: knowing a
                    # picture sits here is layout, copying it out is not.
                    asset_path=(
                        assets.store(image.blob, f".{image.ext}")
                        if image is not None and assets is not None and store_pictures
                        else ""
                    ),
                    font_size_pt=font_size, bold=bold, align=align,
                ))

        title = ""
        if slide.shapes.title is not None and slide.shapes.title.has_text_frame:
            title = slide.shapes.title.text.strip()

        slides.append(SlideLayout(
            number=number, title=title,
            layout_name=getattr(slide.slide_layout, "name", "") or "",
            shapes=shapes,
            background=(
                slide_background(slide, assets, colours, slide_width, slide_height)
                if capture_backgrounds else None
            ),
        ))

    return slides, design


READERS_BY_SUFFIX = {
    ".docx": read_docx,
    ".pptx": read_pptx,
    ".pdf": read_pdf,
    ".md": read_plain_text,
    ".txt": read_plain_text,
}


def extract_document(
    path: Path,
    assets: AssetSink | None = None,
    *,
    keep_tables: bool = True,
    keep_figures: bool = True,
    capture_layout: bool = False,
    capture_backgrounds: bool = False,
    capture_styling: bool = False,
    transcribe_handwriting: bool = False,
) -> ExtractedDocument:
    reader = READERS_BY_SUFFIX.get(path.suffix.lower())
    if reader is None:
        raise SourceUnreadable(
            f"{path.name}: no reader for {path.suffix}. "
            f"Supported: {', '.join(sorted(READERS_BY_SUFFIX))}."
        )

    # Only the readers that can produce figures take a sink; the rest stay
    # single-argument, so adding one later is a signature change rather than a
    # silently ignored keyword.
    takes_assets = reader in (read_docx, read_pptx)

    try:
        # The sink is withheld from the reader when figures are off: passing it
        # would copy every picture out and then drop the blocks that point at
        # them, leaving orphaned files behind. The design pass still gets it,
        # because a slide background is styling rather than a figure.
        reader_assets = assets if keep_figures else None
        blocks = reader(path, reader_assets) if takes_assets else reader(path)
    except SourceUnreadable:
        raise
    except Exception as parse_failure:
        raise SourceUnreadable(
            f"{path.name}: {type(parse_failure).__name__}: {parse_failure}"
        ) from parse_failure

    if not keep_figures:
        blocks = [block for block in blocks if block.kind != BlockKind.FIGURE]
    if not keep_tables:
        # What the option promises when off: the table's words, as ordinary
        # text, rather than rows a model can read as a table.
        blocks = [
            block.model_copy(update={
                "kind": BlockKind.PARAGRAPH,
                "text": " ".join(cell.strip() for cell in block.text.replace("\n", " | ")
                                 .split("|") if cell.strip()),
            }) if block.kind == BlockKind.TABLE else block
            for block in blocks
        ]

    slides: list[SlideLayout] = []
    design: DocumentDesign | None = None
    if reader is read_pptx and (capture_layout or capture_backgrounds or capture_styling):
        try:
            slides, design = read_pptx_design(
                path, assets,
                capture_layout=capture_layout,
                capture_backgrounds=capture_backgrounds,
                capture_styling=capture_styling,
                store_pictures=keep_figures,
            )
        except Exception as design_failure:
            # The words are the point; losing the styling is a degraded result,
            # not a failed extraction.
            logger.warning("%s: layout and design were not captured (%s)",
                           path.name, design_failure)

    ocr_note = ""
    if transcribe_handwriting and reader is read_pdf:
        from pipeline.ocr import transcribe_unread_pages

        blocks, ocr_note = transcribe_unread_pages(path, blocks)

    note = f"{len(blocks)} block(s) read by {reader.__name__}"
    if slides:
        note += f", layout captured for {len(slides)} slide(s)"
    if ocr_note:
        note += f", {ocr_note}"

    return ExtractedDocument(
        file_name=path.name,
        blocks=blocks,
        extraction_note=note,
        slides=slides,
        design=design,
        source_bytes=path.stat().st_size,
    )
