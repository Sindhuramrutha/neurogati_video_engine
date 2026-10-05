"""Handwriting and scanned-page recognition, for PDF pages with no text layer.

A scanned or handwritten page is a picture of words. `read_pdf` finds nothing
on it and, before this, the page simply vanished from the extraction -- a
chapter of handwritten notes extracted to an empty document.

Such pages are sent, as their own images, to the vision model and its reading
is kept as ordinary blocks **marked `transcribed`**. That mark is the point: a
parser reads what the file contains, a model reports what it sees, and later
stages must be able to tell the two apart.

Pages that do have a text layer are never sent. The option costs a model call
per unread page and nothing at all for a born-digital PDF.
"""

from __future__ import annotations

import io
import logging
from itertools import islice
from pathlib import Path

logger = logging.getLogger(__name__)

# A phone photo of a page is often 4000 pixels tall. Handwriting stays legible
# well below that, and a smaller image is a faster, cheaper call.
LONGEST_IMAGE_SIDE = 2000
MAXIMUM_IMAGES_PER_PAGE = 4

TRANSCRIPTION_INSTRUCTION = (
    "Transcribe every word on this page exactly as written, including "
    "handwriting. Keep the reading order. Separate paragraphs with a blank line. "
    "Do not correct spelling, do not summarise, do not describe pictures, and "
    "add no commentary. Write [illegible] for a word you cannot read. If the "
    "page has no text, reply with nothing."
)


def _as_jpeg(image) -> bytes:
    """A PIL image as a modest JPEG: every vision model accepts one."""
    picture = image.convert("RGB")
    picture.thumbnail((LONGEST_IMAGE_SIDE, LONGEST_IMAGE_SIDE))
    buffer = io.BytesIO()
    picture.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()


def _page_images(page) -> list[bytes]:
    """The pictures a page is made of, largest first."""
    found = []
    for embedded in islice(page.images, MAXIMUM_IMAGES_PER_PAGE):
        try:
            found.append((embedded.image.width * embedded.image.height,
                          _as_jpeg(embedded.image)))
        except Exception as unreadable:  # an image filter Pillow cannot decode
            logger.warning("a page image could not be decoded: %s", unreadable)
    return [data for _area, data in sorted(found, key=lambda item: -item[0])]


def _page_of(block) -> int:
    """The page a PDF block sits on, from its "Page N" heading path."""
    heading = block.heading_path[0] if block.heading_path else ""
    number = heading.removeprefix("Page ").strip()
    return int(number) if number.isdigit() else 0


def _paragraphs(transcription: str) -> list[str]:
    cleaned = transcription.strip().strip("`").strip()
    return [part.strip().lstrip("#").strip()
            for part in cleaned.split("\n\n") if part.strip()]


def transcribe_unread_pages(path: Path, blocks: list) -> tuple[list, str]:
    """`blocks` with every textless page of `path` read by the vision model.

    Returns the merged blocks in page order and a note for the extraction
    summary. Never raises for a model problem: the text layer that was read is
    still a result, and the note says what could not be transcribed and why.
    """
    from pypdf import PdfReader

    from pipeline.extraction import BlockKind, ContentBlock
    from pipeline.llm import ModelCallFailed, ModelNotConfigured, read_image_text

    # PDF blocks carry their page only as the "Page N" heading: `slide_number`
    # means a deck slide to later stages, and a PDF page is not one.
    read_pages = {_page_of(block) for block in blocks}
    reader = PdfReader(str(path))
    transcribed: list = []
    done, failed = 0, 0

    for page_number, page in enumerate(reader.pages, start=1):
        if page_number in read_pages:
            continue
        images = _page_images(page)
        if not images:
            continue

        heading = f"Page {page_number}"
        paragraphs: list[str] = []
        try:
            for image in images:
                paragraphs.extend(_paragraphs(read_image_text(
                    image, "image/jpeg", TRANSCRIPTION_INSTRUCTION)))
        except ModelNotConfigured as not_configured:
            return blocks, f"handwriting recognition skipped: {not_configured}"
        except ModelCallFailed as call_failure:
            logger.warning("%s page %s was not transcribed: %s",
                           path.name, page_number, call_failure)
            failed += 1
            continue

        if not paragraphs:
            continue
        done += 1
        transcribed.append(ContentBlock(
            kind=BlockKind.HEADING, level=2, text=heading, heading_path=[heading],
            transcribed=True,
        ))
        transcribed.extend(ContentBlock(
            kind=BlockKind.PARAGRAPH, text=paragraph, heading_path=[heading],
            transcribed=True,
        ) for paragraph in paragraphs)

    merged = sorted([*blocks, *transcribed], key=_page_of)
    note = f"{done} page(s) transcribed by the vision model"
    if failed:
        note += f", {failed} could not be read"
    return merged, note
