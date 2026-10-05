"""What the Extraction agent looks at: the slide as it is, and its pictures.

The text of a slide says what was extracted; the picture of it says what the
slide actually looks like, which is what a person is looking at when they ask
"what is this diagram?". The whole slide is drawn from the deck itself, then
each figure and the background are added, each labelled with the block it
belongs to, so the agent can say which one it means.
"""

from __future__ import annotations

import hashlib
import io
import logging

from pipeline.extraction import ExtractedDocument
from pipeline.projects import Project

logger = logging.getLogger(__name__)

MAXIMUM_PICTURES_SHOWN = 6
PICTURE_LONGEST_SIDE = 1400


def _as_jpeg(picture: bytes) -> bytes | None:
    """A picture made small enough to send, or None if it cannot be read."""
    from PIL import Image

    try:
        with Image.open(io.BytesIO(picture)) as image:
            image = image.convert("RGB")
            image.thumbnail((PICTURE_LONGEST_SIDE, PICTURE_LONGEST_SIDE))
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=82)
            return buffer.getvalue()
    except Exception as unreadable:  # Pillow raises a wide variety here
        logger.warning("a picture could not be prepared for the agent: %s", unreadable)
        return None


def _slide_picture(project: Project, file_name: str, slide_number: int) -> bytes | None:
    """The whole slide as it looks, drawn from the deck and kept for next time.

    Kept under a name made from the deck's size and time, so a deck with slides
    deleted since is drawn again rather than shown as it was.
    """
    from pipeline.slide_frame import compose_slide

    deck = project.sources_dir / file_name
    if not slide_number or deck.suffix.lower() != ".pptx" or not deck.is_file():
        return None
    stat = deck.stat()
    version = hashlib.sha256(
        f"{deck.name}|{stat.st_size}|{stat.st_mtime_ns}".encode()).hexdigest()[:12]
    stem = hashlib.sha256(deck.name.encode()).hexdigest()[:10]
    folder = project.root / "extraction" / "agent-slides"
    kept = folder / f"{stem}-{version}-{slide_number:03d}.jpg"
    if kept.exists():
        return kept.read_bytes()

    folder.mkdir(parents=True, exist_ok=True)
    for stale in folder.glob(f"{stem}-*.jpg"):
        if version not in stale.name:
            stale.unlink(missing_ok=True)
    drawn = folder / f"{stem}-drawing.png"
    try:
        compose_slide(deck, slide_number, drawn)
        picture = _as_jpeg(drawn.read_bytes())
    except Exception as unreadable:
        logger.warning("slide %s of %s could not be drawn for the agent: %s",
                       slide_number, file_name, unreadable)
        return None
    finally:
        drawn.unlink(missing_ok=True)
    if picture:
        kept.write_bytes(picture)
    return picture


def agent_pictures(
    project: Project, document: ExtractedDocument, slide_number: int,
) -> list[tuple[str, bytes]]:
    """What the agent looks at: the whole slide, then its figures and background.

    For a document without slides, its first figures. Each comes with a label
    naming the block it belongs to.
    """
    pictures: list[tuple[str, bytes]] = []
    slide = _slide_picture(project, document.file_name, slide_number)
    if slide:
        pictures.append((f"Picture 1: the whole of slide {slide_number}, as it looks.", slide))

    shown = [b for b in document.blocks if not slide_number or b.slide_number == slide_number]
    sources = [(f"figure [{b.id}] “{b.text[:80]}”", b.asset_path)
               for b in shown if b.kind == "figure" and b.asset_path]
    layout = next((s for s in document.slides if s.number == slide_number), None)
    if layout and layout.background and layout.background.asset_path:
        sources.append((f"the background of slide {slide_number}", layout.background.asset_path))

    for what, asset_path in sources:
        if len(pictures) >= MAXIMUM_PICTURES_SHOWN:
            break
        path = project.root / asset_path
        picture = _as_jpeg(path.read_bytes()) if path.is_file() else None
        if picture:
            pictures.append((f"Picture {len(pictures) + 1}: {what}.", picture))
    return pictures


def looked_at_summary(pictures: list[tuple[str, bytes]], slide_number: int) -> str:
    whole = any("the whole of slide" in label for label, _ in pictures)
    figures = sum("figure [" in label for label, _ in pictures)
    background = any("the background" in label for label, _ in pictures)
    parts = [f"slide {slide_number}" if whole else "",
             f"{figures} figure{'' if figures == 1 else 's'}" if figures else "",
             "the background" if background else ""]
    return ", ".join(part for part in parts if part)
