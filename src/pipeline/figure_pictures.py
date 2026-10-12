"""How a figure's picture is changed: the one procedure every path follows.

Four things change a picture -- the agent redrawing, editing or adding one,
and the Review tab's upload and draw buttons. They share this one procedure,
because done separately each had its own failure:

- A drawn picture contained the whole slide. The image model was handed the
  slide's text as context with nothing saying it was context, and a style that
  asked for "large legible labels", so it drew a title bar, the paragraph and a
  quote. The slide already shows its text; a picture that repeats it shows it
  twice.
- The Layout kept the old picture. A figure's picture and the layout shape
  that shows it are the same picture recorded in two places, and only the
  figure was updated.

So, whatever the path (docs/operations/extraction-pictures-sop.md):

1. **Prompt.** `picture_prompt` -- the picture only, no slide text in it, the
   text given as understanding, the slot's shape asked for.
2. **Store.** Content-addressed, like every extracted picture.
3. **Place.** `set_picture` -- the figure and its slot on the slide together.
4. **Mark.** A picture that is not the source's own is `generated`, or
   `uploaded`; later stages say so.
"""

from __future__ import annotations

from pipeline.core import OperationFailed
from pipeline.extraction import BlockKind, ContentBlock, ExtractedDocument, LayoutShape
from pipeline.projects import Project

# What the picture has to be, whatever it is of. An explainer video needs a
# clear picture on a plain background, not an illustration with a style -- and
# not text, which the slide and the narration already carry.
IMAGE_STYLE = (
    "A clear, simple picture for an educational video. Flat vector style, plain "
    "white background, strong contrast, no watermark, no signature, no "
    "photographic texture."
)

NO_SLIDE_TEXT = (
    "Draw the picture only. Do not draw a slide, a title bar, a heading, a "
    "paragraph, a caption, a quote or any sentence from the text above: the "
    "slide already shows its own text. No words in the picture unless the "
    "instruction asks for labels, and then only short labels of one to three "
    "words. Do not invent numbers, data or facts the text does not support."
)

EDIT_KEEPS_THE_REST = (
    "Keep everything else in the picture as it is. Do not add a title, a caption "
    "or any text that is not already in it."
)

MAXIMUM_CONTEXT_CHARACTERS = 1_500


def picture_context(document: ExtractedDocument, block: ContentBlock) -> str:
    """The words a picture has to fit: its slide's text for a deck, the blocks
    around it for a document. Never speaker notes -- what the presenter says is
    not what the slide shows, and it was drawn into a picture once."""
    blocks = document.blocks
    if block.slide_number:
        nearby = [b for b in blocks if b.slide_number == block.slide_number]
    else:
        position = next((i for i, b in enumerate(blocks) if b.id == block.id), 0)
        nearby = blocks[max(0, position - 3):position + 4]
    text = " ".join(
        b.text for b in nearby
        if b.kind in {BlockKind.PARAGRAPH, BlockKind.LIST_ITEM, BlockKind.HEADING}
        and not b.text.startswith("[speaker notes]")
    )
    return text[:MAXIMUM_CONTEXT_CHARACTERS]


def slot_of(document: ExtractedDocument, figure: ContentBlock) -> LayoutShape | None:
    """The layout shape on the figure's slide that shows the figure's picture."""
    if not figure.asset_path or not figure.slide_number:
        return None
    slide = next((s for s in document.slides if s.number == figure.slide_number), None)
    if slide is None:
        return None
    return next((shape for shape in slide.shapes if shape.asset_path == figure.asset_path), None)


def _shape_words(document: ExtractedDocument, slot: LayoutShape | None) -> str:
    """The slot's shape in words, for a model that takes no size parameter."""
    if slot is None or not slot.width or not slot.height:
        return "landscape, about 4:3"
    design = document.design
    deck_ratio = (design.slide_width_emu / design.slide_height_emu
                  if design and design.slide_width_emu and design.slide_height_emu else 16 / 9)
    ratio = slot.width / slot.height * deck_ratio
    if ratio > 1.25:
        return f"landscape, about {ratio:.1f}:1"
    if ratio < 0.8:
        return f"portrait, about 1:{1 / ratio:.1f}"
    return "square"


def picture_prompt(
    document: ExtractedDocument, near: ContentBlock, what: str, instruction: str = "",
) -> str:
    """The prompt for drawing a picture that goes where `near` is."""
    context = picture_context(document, near)
    return "\n".join(part for part in [
        f"Draw one picture: {what}.",
        f"Instruction: {instruction}" if instruction.strip() else "",
        f"For your understanding only, the slide it goes on says: {context}" if context else "",
        f"Shape: {_shape_words(document, slot_of(document, near))}.",
        NO_SLIDE_TEXT,
        f"Unless the instruction asks for another style: {IMAGE_STYLE}",
    ] if part)


def edit_instruction(instruction: str) -> str:
    """What the image model is told when it changes an existing picture."""
    return f"{instruction.strip().rstrip('.')}. {EDIT_KEEPS_THE_REST}"


def store_picture(project: Project, picture: bytes, suffix: str = ".png") -> str:
    from pipeline.extraction_run import extraction_asset_sink

    stored = extraction_asset_sink(project).store(
        picture, suffix if suffix.startswith(".") else f".{suffix}")
    if not stored:
        raise OperationFailed("The new picture could not be stored.")
    return stored


def set_picture(
    document: ExtractedDocument, figure: ContentBlock, stored: str, origin: str,
) -> None:
    """Put a new picture on a figure, and in the slot the old one had on the slide."""
    slot = slot_of(document, figure)
    if slot is not None:
        slot.asset_path = stored
    figure.asset_path = stored
    figure.asset_origin = origin
