"""Structured, per-slide extraction from a .pptx: each shape's text (or a
fallback label for non-text shapes) and its position, converted into the
same coordinate space the rasterized slide background will actually occupy
once fitted into Manim's frame.

Rasterization (utils/pptx_rasterize.py) gives a picture of a slide; this
gives the structured data -- what's on it, and where -- that the highlight
planner needs to point at a specific real region rather than a hallucinated
one. The two are deliberately independent passes over the same deck so
either can be tested/debugged without the other.
"""

from pathlib import Path
from typing import Literal, Optional

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pydantic import BaseModel

# Manim Community's default camera frame (16:9, frame_height=8.0).
FRAME_WIDTH = 14.222222
FRAME_HEIGHT = 8.0


class SlideShape(BaseModel):
    shape_id: int
    kind: Literal["text", "picture", "chart", "other"]
    text: Optional[str] = None
    alt_text: Optional[str] = None  # shape.name -- fallback label when there's no text
    manim_bbox: tuple[float, float, float, float]  # x_min, y_min, x_max, y_max


class SlideContent(BaseModel):
    index: int  # 1-based, matches export_slides_to_png's slide_NN.png naming
    slide_width_emu: int
    slide_height_emu: int
    shapes: list[SlideShape]
    notes_text: Optional[str] = None


def emu_to_manim_frame(
    left: int, top: int, width: int, height: int,
    slide_width_emu: int, slide_height_emu: int,
    frame_width: float = FRAME_WIDTH, frame_height: float = FRAME_HEIGHT,
) -> tuple[float, float, float, float]:
    """Converts a shape's bounding box from PowerPoint EMU space (origin
    top-left, y-down) into Manim frame coordinates (origin center, y-up).

    Accounts for letterboxing: the slide background image is *fitted* into
    Manim's frame (scaled to match on whichever axis is tighter), not
    stretched, so a slide whose aspect ratio doesn't exactly match the
    frame's leaves a margin on one axis. Every shape's position must be
    computed relative to the actual displayed image rect, not the raw frame,
    or highlights drift off-target on any non-16:9 deck.
    """
    slide_aspect = slide_width_emu / slide_height_emu
    frame_aspect = frame_width / frame_height

    if slide_aspect >= frame_aspect:
        disp_width = frame_width
        disp_height = frame_width / slide_aspect
    else:
        disp_height = frame_height
        disp_width = frame_height * slide_aspect

    disp_left = -disp_width / 2
    disp_top = disp_height / 2

    fx_min = left / slide_width_emu
    fx_max = (left + width) / slide_width_emu
    fy_min = top / slide_height_emu
    fy_max = (top + height) / slide_height_emu

    x_min = disp_left + fx_min * disp_width
    x_max = disp_left + fx_max * disp_width
    y_max = disp_top - fy_min * disp_height  # smaller y-fraction (higher on slide) -> larger Manim y
    y_min = disp_top - fy_max * disp_height

    return (x_min, y_min, x_max, y_max)


def _shape_kind(shape) -> str:
    if shape.has_text_frame and shape.text_frame.text.strip():
        return "text"
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        return "picture"
    if shape.has_chart:
        return "chart"
    return "other"


def read_deck(pptx_path: Path) -> list[SlideContent]:
    prs = Presentation(str(pptx_path))
    slide_w, slide_h = prs.slide_width, prs.slide_height

    slides = []
    for slide_index, slide in enumerate(prs.slides, start=1):
        shapes = []
        for shape in slide.shapes:
            # Placeholder shapes that were never explicitly repositioned inherit
            # their geometry from the slide layout rather than carrying it
            # themselves -- python-pptx returns None for left/top/width/height in
            # that case. Skipping them (rather than guessing layout geometry) keeps
            # every returned manim_bbox real and precise; the highlight planner
            # only ever points at shapes this module actually measured.
            if None in (shape.left, shape.top, shape.width, shape.height):
                continue
            text = shape.text_frame.text.strip() if shape.has_text_frame else None
            shapes.append(
                SlideShape(
                    shape_id=shape.shape_id,
                    kind=_shape_kind(shape),
                    text=text or None,
                    alt_text=shape.name,
                    manim_bbox=emu_to_manim_frame(
                        shape.left, shape.top, shape.width, shape.height, slide_w, slide_h
                    ),
                )
            )

        notes_text = None
        if slide.has_notes_slide:
            notes_text = slide.notes_slide.notes_text_frame.text.strip() or None

        slides.append(
            SlideContent(
                index=slide_index,
                slide_width_emu=slide_w,
                slide_height_emu=slide_h,
                shapes=shapes,
                notes_text=notes_text,
            )
        )
    return slides
