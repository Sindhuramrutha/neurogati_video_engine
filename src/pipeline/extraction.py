"""Extraction — pull structured content out of the source documents.

The stage that was declared and never written. Until now the Planning agent saw
only the *names* of the source files, so asking it to plan a video about a
document it could not read was a guarantee of invention: it would produce a
plausible plan about the title.

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

from pipeline.stages import Stage
from pipeline.storage.documents import (
    JsonDocumentStore,
    new_identifier,
    read_json_object,
    write_text_atomically,
)
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

MAXIMUM_BLOCK_LENGTH = 20000
MAXIMUM_BLOCKS_PER_DOCUMENT = 5000

# A slide with more shapes than this is a diagram drawn by hand; its geometry is
# not something a video can reproduce anyway, and keeping all of it would bloat
# the extraction for no gain.
MAXIMUM_SHAPES_PER_SLIDE = 60
MAXIMUM_SHAPE_TEXT_LENGTH = 300

# A slide heading is large text near the top. Below this it is body copy, and
# past this length it is a paragraph that happens to be set big.
SMALLEST_HEADING_POINTS = 18.0
MAXIMUM_HEADING_LENGTH = 120

# Two text sizes this close are one hierarchy level -- a kicker over a title --
# and the longer of them is the title.
NEAR_TIE_RATIO = 0.92

# Extracted figures are a copy of the pictures inside the source files, so a
# picture-heavy deck can approach the size of the deck itself. This is a ceiling
# against the pathological case -- a folder of large decks quietly filling the
# disk -- not a target; normal documents land far below it.
MAXIMUM_EXTRACTED_ASSET_BYTES = 512 * 1024 * 1024

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


class SlideBackground(BaseModel):
    """What is behind everything else on a slide."""

    colour: str = ""        # "#RRGGBB"
    asset_path: str = ""    # a picture background, stored like a figure
    inherited_from: str = ""  # slide | layout | master -- where it was set


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


class SourceSelectionStore:
    """The source files someone has chosen to leave out of extraction.

    **Stored as what is left out, not what is ticked.** A file uploaded later is
    then included without anyone remembering to tick it, and is reported as not
    yet extracted until it is. Storing the ticked set would do the opposite: a
    new upload would be silently excluded, and nothing would ever say so.

    Kept with the stage's settings rather than in the extraction itself, for the
    same reason the options are: it is an input to a run, and it exists before
    any run has happened.
    """

    def __init__(self, project_root: Path) -> None:
        self.path = project_root / "settings" / "extraction-sources.json"

    def load(self) -> list[str]:
        stored = read_json_object(self.path, "extraction source selection") or {}
        names = stored.get("excluded", [])
        return sorted({name for name in names if isinstance(name, str) and name})

    def save(self, excluded: list[str]) -> list[str]:
        cleaned = sorted(set(excluded))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomically(self.path, json.dumps({"excluded": cleaned}, indent=2))
        return cleaned


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


class AssetSink:
    """Somewhere to put the images pulled out of a document.

    Content-addressed by digest, so a logo repeated on forty slides is stored
    once rather than forty times -- which on a real 80 MB deck is the difference
    between a few megabytes of assets and most of the deck copied out again.

    Passed in rather than derived inside the readers so a reader stays a pure
    function of its file when nobody wants the images: `read_docx(path)` with no
    sink extracts text and writes nothing, which is what the tests and the
    preview path want.
    """

    def __init__(self, directory: Path, relative_to: Path | None = None) -> None:
        self.directory = directory
        self.relative_to = relative_to
        self.written: dict[str, str] = {}
        self.bytes_written = 0
        self.skipped_for_size = 0

    def store(self, blob: bytes, suffix: str) -> str:
        digest = hashlib.sha256(blob).hexdigest()[:16]
        if digest in self.written:
            return self.written[digest]

        if self.bytes_written + len(blob) > MAXIMUM_EXTRACTED_ASSET_BYTES:
            # Reported rather than raised: losing the last few figures of a very
            # large deck is a much smaller problem than failing the extraction
            # and keeping none of its text.
            self.skipped_for_size += 1
            return ""

        self.directory.mkdir(parents=True, exist_ok=True)
        destination = self.directory / f"{digest}{suffix.lower()}"
        if not destination.exists():
            destination.write_bytes(blob)

        stored = str(
            destination.relative_to(self.relative_to) if self.relative_to else destination
        ).replace("\\", "/")
        self.written[digest] = stored
        self.bytes_written += len(blob)
        return stored

    def prune_unreferenced(self) -> int:
        """Delete figures this run did not produce. Returns how many went.

        Called only after the new extraction is safely saved. Without it, removing
        a picture-heavy deck from a project left most of its size behind in
        `extraction/assets/` for good, referenced by nothing.
        """
        if not self.directory.exists():
            return 0
        kept = {Path(stored).name for stored in self.written.values()}
        removed = 0
        for candidate in self.directory.iterdir():
            if candidate.is_file() and candidate.name not in kept:
                candidate.unlink()
                removed += 1
        return removed


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

    presentation = Presentation(str(path))
    blocks: list[ContentBlock] = []
    figure_number = 0

    for number, slide in enumerate(presentation.slides, start=1):
        # A slide's own title if it has one, so the heading path means something.
        title = ""
        title_element = _title_element(slide)
        if slide.shapes.title is not None and slide.shapes.title.has_text_frame:
            title = slide.shapes.title.text.strip()
        heading = title or _headline_of(slide) or f"Slide {number}"
        heading_path = [heading]

        blocks.append(ContentBlock(
            kind=BlockKind.HEADING, level=2, text=heading, heading_path=list(heading_path),
            slide_number=number,
        ))

        for shape in slide.shapes:
            if shape._element is title_element:
                continue
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    line = "".join(run.text for run in paragraph.runs).strip()
                    if not line:
                        continue
                    # Bulleted levels stay list items so the structure survives.
                    kind = BlockKind.LIST_ITEM if paragraph.level else BlockKind.PARAGRAPH
                    blocks.append(ContentBlock(
                        kind=kind, text=line, heading_path=list(heading_path),
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
                caption = (getattr(shape, "name", "") or "").strip()
                blocks.append(ContentBlock(
                    kind=BlockKind.FIGURE,
                    text=f"{caption or 'Figure'} (slide {number})",
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


DRAWING_NAMESPACE = "http://schemas.openxmlformats.org/drawingml/2006/main"
PRESENTATION_NAMESPACE = "http://schemas.openxmlformats.org/presentationml/2006/main"
RELATIONSHIP_NAMESPACE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _aspect_ratio(width: int, height: int) -> str:
    """"16:9" rather than 1.777…, because that is what a deck is described as."""
    if not width or not height:
        return ""
    from math import gcd

    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def _shape_box(shape, slide, slide_width: int, slide_height: int) -> tuple[float, ...]:
    """Where a shape sits, as fractions of the slide.

    A placeholder usually declares no position of its own and inherits the one
    on its layout, so an unresolved box is looked up there rather than reported
    as sitting in the top-left corner.
    """
    left, top, width, height = shape.left, shape.top, shape.width, shape.height

    if None in (left, top, width, height) and shape.is_placeholder:
        try:
            inherited = slide.slide_layout.placeholders[shape.placeholder_format.idx]
        except (KeyError, AttributeError):
            inherited = None
        if inherited is not None:
            left = left if left is not None else inherited.left
            top = top if top is not None else inherited.top
            width = width if width is not None else inherited.width
            height = height if height is not None else inherited.height

    return (
        (left or 0) / slide_width,
        (top or 0) / slide_height,
        (width or 0) / slide_width,
        (height or 0) / slide_height,
    )


def _headline_of(slide) -> str:
    """The slide's heading when it is not in a title placeholder.

    Designed decks routinely set their headings as plain text boxes, so
    `shapes.title` is None and every slide came through as "Slide 7" -- which
    made the heading path useless, gave the plan forty identical section names,
    and lost the one piece of text the author most wanted kept.

    The heading is the largest text in the upper part of the slide. Where two
    sizes are within a hair of each other -- a small kicker above a title, like
    "4.Chapter" over "Networks that Learn" -- the longer line wins, because the
    kicker is a label and the title is the sentence.
    """
    candidates: list[tuple[float, str]] = []
    for shape in slide.shapes:
        if not shape.has_text_frame or shape.top is None or shape.height is None:
            continue
        written = shape.text_frame.text.strip()
        line = written.splitlines()[0].strip() if written else ""
        if not line or len(line) > MAXIMUM_HEADING_LENGTH:
            continue
        size, _bold, _align = _first_run_style(shape)
        if size < SMALLEST_HEADING_POINTS:
            continue
        candidates.append((size, line))

    if not candidates:
        return ""
    largest = max(size for size, _line in candidates)
    close = [line for size, line in candidates if size >= largest * NEAR_TIE_RATIO]
    return max(close, key=len)


def _title_element(slide):
    """The XML behind a slide's title, or None.

    Compared by element, never by object: `slide.shapes.title` builds a fresh
    proxy on every access, so `shape is slide.shapes.title` is always False. It
    read as working -- and quietly extracted every slide title twice, once as
    the heading and again as a paragraph of its own.
    """
    title = slide.shapes.title
    return title._element if title is not None else None


def _shape_kind(shape, title_element) -> str:
    if title_element is not None and shape._element is title_element:
        return "title"
    if getattr(shape, "shape_type", None) is not None and shape.shape_type == 13:  # PICTURE
        return "picture"
    if getattr(shape, "has_table", False):
        return "table"
    if getattr(shape, "has_chart", False):
        return "chart"
    if shape.has_text_frame:
        return "text"
    return "other"


def _first_run_style(shape) -> tuple[float, bool, str]:
    """The look of a shape's first line: size, weight, alignment.

    The first line, not an average: what is wanted is "this is a 32pt heading",
    and a shape whose runs disagree is not something a slide-like frame can
    reproduce anyway.
    """
    if not shape.has_text_frame:
        return 0.0, False, ""
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            size = run.font.size.pt if run.font.size is not None else 0.0
            align = paragraph.alignment.__str__().split(" ")[0].lower() \
                if paragraph.alignment is not None else ""
            return float(size), bool(run.font.bold), align
    return 0.0, False, ""


def _colour_of(fill) -> str:
    """A fill's colour as "#RRGGBB", or empty when it is not a plain colour."""
    try:
        colour = fill.fore_color
        if colour.type is not None and str(colour.type).startswith("RGB"):
            return f"#{colour.rgb}"
        # A theme colour resolves against the theme, which is captured
        # separately; the name is more useful than a guessed hex.
        if colour.type is not None:
            return str(colour.theme_color).split(" ")[0].lower()
    except (AttributeError, TypeError, ValueError):
        return ""
    return ""


def _background_picture(holder, assets: AssetSink | None) -> str:
    """A background image, stored like any other extracted picture.

    Read from the XML because python-pptx models solid fills but not the
    `blipFill` a background picture uses.
    """
    if assets is None:
        return ""
    background = holder._element.find(f"{{{PRESENTATION_NAMESPACE}}}bg")
    if background is None:
        return ""
    blip = background.find(f".//{{{DRAWING_NAMESPACE}}}blip")
    if blip is None:
        return ""
    relationship_id = blip.get(f"{{{RELATIONSHIP_NAMESPACE}}}embed")
    if not relationship_id:
        return ""
    try:
        part = holder.part.related_part(relationship_id)
        suffix = Path(str(part.partname)).suffix or ".png"
        return assets.store(part.blob, suffix)
    except (KeyError, AttributeError) as unresolved:
        logger.warning("a slide background could not be read: %s", unresolved)
        return ""


def _slide_background(
    slide, assets: AssetSink | None, theme_colours: dict[str, str]
) -> SlideBackground | None:
    """What is behind the slide, looking where PowerPoint looks.

    A slide usually sets no background of its own and inherits the layout's or
    the master's, so all three are tried in that order -- and when none of them
    sets one, the answer is still not "nothing": it is the theme's light colour.
    Recording that spares every later stage from re-implementing PowerPoint's
    inheritance rules.
    """
    from pptx.enum.dml import MSO_FILL

    holders = [("slide", slide), ("layout", slide.slide_layout)]
    master = getattr(slide.slide_layout, "slide_master", None)
    if master is not None:
        holders.append(("master", master))

    for source, holder in holders:
        picture = _background_picture(holder, assets)
        if picture:
            return SlideBackground(asset_path=picture, inherited_from=source)
        try:
            fill = holder.background.fill
            if fill.type == MSO_FILL.SOLID:
                colour = _colour_of(fill)
                if colour:
                    return SlideBackground(colour=colour, inherited_from=source)
        except (AttributeError, NotImplementedError, ValueError):
            continue

    fallback = theme_colours.get("lt1", "")
    if fallback.startswith("#"):
        return SlideBackground(colour=fallback, inherited_from="theme")
    return None


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
                _slide_background(slide, assets, colours) if capture_backgrounds else None
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

    note = f"{len(blocks)} block(s) read by {reader.__name__}"
    if slides:
        note += f", layout captured for {len(slides)} slide(s)"

    return ExtractedDocument(
        file_name=path.name,
        blocks=blocks,
        extraction_note=note,
        slides=slides,
        design=design,
    )
