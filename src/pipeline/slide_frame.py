"""Drawing a deck's own slide as a video frame.

The video used to show the renderer's template with an extracted figure dropped
into it: a section title on the left, a picture on the right, on our background.
A deck that people designed came out looking generated, and the comparison
against the real slide was not close.

This draws the slide instead. The deck's background, its pictures, its heading
and its body text, at its own positions, in its own fonts and colours.

**Read from the .pptx, not from the extraction.** `LayoutShape` records one
size, one weight and one alignment per shape -- taken from the first run of the
first paragraph -- and carries no fill, alpha, line or font family. Extending it
until it could describe a slide would mean re-modelling DrawingML in our own
schema. The source file is kept in `sources/`, so this reads it directly and the
artifact records the *result*: a PNG on disk, which is still a file as the source
of truth (ADR 0005).

**Why hand-built.** There is no pure-Python renderer for PPTX. Drawing a slide
means implementing PowerPoint's layout and fill model, so the honest options are
to drive a real office engine -- LibreOffice or PowerPoint, neither installed --
or to composite it here. What makes the second tractable rather than open-ended
is what real decks actually contain: pictures, rectangles and text runs.

**Three rules that are not obvious.**

- *The design usually lives on the layout, not the slide.* A deck's background
  art is a shape on `slide_layout`, beneath the slide's own shapes. Reading only
  `slide.shapes` -- which is what extraction did -- loses the entire look.
- *Layout placeholders are templates, not content.* "Click to edit Master title
  style" is on the layout and must not be drawn. Non-placeholder layout shapes
  are the design; placeholders are prompts.
- *Text style is inherited.* A run often names no font, size or colour, and the
  answer comes from its placeholder on the layout, then the master, then the
  theme. A resolver that reads only the run draws black Helvetica.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

EMU_PER_INCH = 914400
EMU_PER_POINT = 12700

# PowerPoint's default internal margins on a text frame, in EMU. A frame that
# does not override them still insets its text by this much, and text drawn
# without it sits visibly proud of where the deck put it.
DEFAULT_LEFT_INSET = 91440
DEFAULT_TOP_INSET = 45720

# Metric-compatible substitutes. Arimo has Arial's metrics exactly, so a deck
# set in Arimo lays out identically in Arial -- same line breaks, same widths --
# which is a different and much better outcome than "a sans-serif of some kind".
METRIC_TWINS = {
    "arimo": "arial",
    "tinos": "times new roman",
    "cousine": "courier new",
    "carlito": "calibri",
    "caladea": "cambria",
    "liberation sans": "arial",
    "liberation serif": "times new roman",
}

# Weight words a variable font names its instances with, longest first so
# "extrabold" is not matched as "bold".
WEIGHT_WORDS = (
    "extralight", "extrabold", "semibold", "thin", "light",
    "regular", "medium", "bold", "black",
)


def font_directory() -> Path:
    """Fonts bundled with the repo, for faces a deck names that nobody has.

    A deck can embed its fonts, but PowerPoint embeds them as MicroType-Express
    compressed EOT, which cannot be unpacked here -- so a named face either
    exists on the machine, is bundled, or is substituted.
    """
    from pipeline.config import REPO_ROOT

    return REPO_ROOT / "assets" / "fonts"


@dataclass(frozen=True)
class Placement:
    """How the slide's coordinate space maps onto the frame.

    One scale for both axes plus an offset, so a deck whose shape is not the
    video's shape is letterboxed rather than distorted.
    """

    scale: float
    offset_x: int = 0
    offset_y: int = 0

    def box(self, left: int, top: int, width: int, height: int) -> tuple[int, int, int, int]:
        return (
            self.offset_x + round(left * self.scale),
            self.offset_y + round(top * self.scale),
            round(width * self.scale),
            round(height * self.scale),
        )

    def points_to_pixels(self, size_pt: float) -> float:
        return size_pt * EMU_PER_POINT * self.scale


@dataclass(frozen=True)
class Composed:
    """One drawn slide."""

    path: Path
    slide_number: int
    shapes_drawn: int
    notes: tuple[str, ...] = ()


# How to read a full-bleed wash a deck lays over its own background art.
#
# `as_written` is the spec and what PowerPoint does: `<a:alpha val="95000">` is
# 95% *opaque*, so a near-white sheet at 95% leaves a very pale background with
# a hint of the artwork through it. That is almost certainly the intent here,
# because the deck sets its body text in #2A2742 and only has contrast against a
# pale background.
#
# `inverted` reads the value as transparency instead, which is how some
# authoring tools write it and how some viewers render it: the artwork stays
# vivid. It looks better in isolation and can put dark text on a dark field.
#
# `ignored` drops the wash entirely.
WASH_AS_WRITTEN = "as_written"
WASH_INVERTED = "inverted"
WASH_IGNORED = "ignored"


def compose_slide(
    pptx_path: Path, slide_number: int, output_path: Path, width: int = 0, height: int = 0,
    wash: str = WASH_AS_WRITTEN,
) -> Composed:
    """Draw one slide of a deck as a frame. 1-based, like PowerPoint counts.

    Back to front: the master's decoration, then the layout's, then the slide's
    own -- which is the order PowerPoint composites them and the reason a
    background on the layout appears behind everything.
    """
    from PIL import Image
    from pptx import Presentation

    from pipeline.rendering import FRAME_HEIGHT, FRAME_WIDTH

    width = width or FRAME_WIDTH
    height = height or FRAME_HEIGHT

    presentation = Presentation(str(pptx_path))
    slides = list(presentation.slides)
    if not 1 <= slide_number <= len(slides):
        raise ValueError(
            f"{pptx_path.name} has {len(slides)} slides; there is no slide {slide_number}"
        )
    slide = slides[slide_number - 1]

    slide_width = presentation.slide_width or int(13.333 * EMU_PER_INCH)
    slide_height = presentation.slide_height or int(7.5 * EMU_PER_INCH)

    # Fitted to the frame rather than stretched to its width: a 4:3 deck in a
    # 16:9 video letterboxes, which keeps every shape where the deck put it.
    # Stretching would distort the author's layout to hide a black bar.
    scale = min(width / slide_width, height / slide_height)
    place = Placement(
        scale=scale,
        offset_x=round((width - slide_width * scale) / 2),
        offset_y=round((height - slide_height * scale) / 2),
    )

    frame = Image.new("RGB", (width, height), _slide_background(slide))
    notes: list[str] = []
    drawn = 0

    layout = slide.slide_layout
    master = layout.slide_master
    for holder, is_own in ((master, False), (layout, False), (slide, True)):
        for shape in holder.shapes:
            # A placeholder on the layout or master is a prompt -- "Click to
            # edit Master title style" -- and PowerPoint never renders it. Its
            # non-placeholder shapes are the design.
            if not is_own and getattr(shape, "is_placeholder", False):
                continue
            is_wash = not is_own and _is_obscuring_wash(shape, slide_width, slide_height)
            if is_wash:
                # Only worth saying when it is not the faithful reading. As
                # written is what the file asks for, and repeating that on every
                # one of forty slides is noise.
                if wash == WASH_IGNORED:
                    notes.append("The deck's full-bleed wash was left off this slide.")
                    continue
                if wash == WASH_INVERTED:
                    notes.append(
                        "The deck's full-bleed wash was read as transparency, which "
                        "keeps its background art vivid."
                    )
            try:
                drawn += _draw_shape(
                    frame, shape, slide, place, notes,
                    invert_alpha=is_wash and wash == WASH_INVERTED,
                )
            except Exception as unreadable:      # one bad shape must not lose the slide
                logger.warning("slide %s: a shape could not be drawn: %s",
                               slide_number, unreadable)
                notes.append(f"a {_shape_name(shape)} could not be drawn: {unreadable}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.save(output_path)
    return Composed(output_path, slide_number, drawn, tuple(notes))


def cached_slide_path(directory: Path, pptx_path: Path, slide_number: int) -> Path:
    """Where a composed slide lives, named for the deck it came from."""
    stem = "".join(
        character if character.isalnum() else "-" for character in pptx_path.stem
    ).strip("-").lower()[:40]
    digest = hashlib.sha256(str(pptx_path).encode()).hexdigest()[:8]
    return directory / f"{stem}-{digest}-{slide_number:03d}.png"


# --- one shape ----------------------------------------------------------------------


def _shape_name(shape) -> str:
    return str(getattr(shape, "shape_type", "shape")).split(" ")[0].lower()


def _draw_shape(frame, shape, slide, place: Placement, notes: list[str],
                invert_alpha: bool = False) -> int:
    """Draw one shape, and its children if it is a group. Returns how many."""
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        # Recursed, because everything inside a group is content the deck put on
        # the slide. Extraction drops grouped shapes entirely, which silently
        # loses every word and picture inside them.
        drawn = 0
        for child in shape.shapes:
            drawn += _draw_shape(frame, child, slide, place, notes, invert_alpha)
        return drawn

    box = _box_of(shape, slide, place)
    if box is None:
        return 0

    _draw_fill(frame, shape, box, complement=invert_alpha)
    drawn = _draw_picture(frame, shape, box)
    if shape.has_text_frame and shape.text_frame.text.strip():
        _draw_text(frame, shape, slide, box, place, notes)
        drawn = 1
    return drawn or (1 if _has_fill(shape) else 0)


def _box_of(shape, slide, place: Placement) -> tuple[int, int, int, int] | None:
    """The shape's rectangle in pixels, resolving an inherited position.

    A placeholder often carries no geometry of its own and takes it from the
    matching placeholder on the layout -- the same rule `_shape_box` in
    deck_shapes follows.
    """
    left, top = shape.left, shape.top
    width, height = shape.width, shape.height

    if None in (left, top, width, height) and getattr(shape, "is_placeholder", False):
        try:
            inherited = slide.slide_layout.placeholders[shape.placeholder_format.idx]
            left = left if left is not None else inherited.left
            top = top if top is not None else inherited.top
            width = width if width is not None else inherited.width
            height = height if height is not None else inherited.height
        except (KeyError, AttributeError):
            pass

    if None in (left, top, width, height):
        return None
    return place.box(left, top, width, height)


def _is_obscuring_wash(shape, slide_width: int, slide_height: int) -> bool:
    """Whether this shape is a full-bleed sheet that would hide everything under it.

    Decks carry these: a text-free rectangle covering the whole slide, filled
    near-opaque, sitting on the layout *above* the background artwork. Drawn as
    the file describes it, the deck's own design disappears under a flat wash --
    which is not how the deck looks in any viewer it has been opened in.

    Identifying one is all this does; what to do about it is the caller's
    choice, because the two readings produce very different slides and the file
    does not settle which is meant. See the `WASH_*` constants.

    Deliberately narrow. It never applies to a shape on the slide itself, never
    to one carrying text, and never to one that does not cover the whole slide.

    """
    if getattr(shape, "has_text_frame", False) and shape.text_frame.text.strip():
        return False
    if getattr(shape, "image", None) is not None:
        return False
    left, top = shape.left or 0, shape.top or 0
    width, height = shape.width or 0, shape.height or 0
    covers = (left <= 0 and top <= 0
              and width >= slide_width * 0.99 and height >= slide_height * 0.99)
    return covers and _fill_alpha(shape) >= 0.8 * 255 and _has_fill(shape)


def _has_fill(shape) -> bool:
    try:
        from pptx.enum.dml import MSO_FILL

        return shape.fill.type == MSO_FILL.SOLID
    except Exception:
        return False


def _draw_fill(frame, shape, box: tuple[int, int, int, int], complement: bool = False) -> None:
    """A solid fill, honouring its transparency.

    Alpha matters more than it looks: a deck's background art is often a picture
    with a near-white shape over it at partial opacity, and drawing that shape
    opaque erases the artwork underneath.
    """
    from PIL import Image
    from pptx.enum.dml import MSO_FILL

    try:
        if shape.fill.type != MSO_FILL.SOLID:
            return
        colour = shape.fill.fore_color
        if colour.type is None or not str(colour.type).startswith("RGB"):
            return
        rgb = (colour.rgb[0], colour.rgb[1], colour.rgb[2])
    except Exception:
        return

    left, top, width, height = box
    if width <= 0 or height <= 0:
        return
    alpha = _fill_alpha(shape)
    if complement:
        # The value in the file is transparency, not opacity -- see
        # `_is_obscuring_wash`. A wash stored as 95% is a 5% veil.
        alpha = 255 - alpha
    patch = Image.new("RGBA", (width, height), (*rgb, alpha))
    frame.paste(Image.alpha_composite(
        frame.crop((left, top, left + width, top + height)).convert("RGBA"), patch,
    ).convert("RGB"), (left, top))


def _fill_alpha(shape) -> int:
    """The fill's opacity as 0-255. DrawingML states it in thousandths of a
    percent, so 95000 is 95%."""
    import re

    found = re.search(r"<a:alpha val=\"(\d+)\"", shape._element.xml)
    if not found:
        return 255
    return max(0, min(255, round(int(found.group(1)) / 100000 * 255)))


def _draw_picture(frame, shape, box: tuple[int, int, int, int]) -> int:
    """A picture, stretched to its frame the way PowerPoint stretches it."""
    import io

    from PIL import Image

    image = getattr(shape, "image", None)
    if image is None:
        return 0

    left, top, width, height = box
    if width <= 0 or height <= 0:
        return 0
    try:
        with Image.open(io.BytesIO(image.blob)) as opened:
            picture = opened.convert("RGBA")
    except Exception as unreadable:
        logger.warning("a slide picture could not be read: %s", unreadable)
        return 0

    resized = picture.resize((width, height), Image.LANCZOS)
    frame.paste(resized, (left, top), resized)
    return 1


# --- text ---------------------------------------------------------------------------


def _draw_text(frame, shape, slide, box, place: Placement, notes: list[str]) -> None:
    """The shape's text, run by run, at the deck's sizes and colours."""
    from PIL import ImageDraw
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

    draw = ImageDraw.Draw(frame)
    text_frame = shape.text_frame
    left, top, width, height = box

    inset_left = round((text_frame.margin_left
                        if text_frame.margin_left is not None
                        else DEFAULT_LEFT_INSET) * place.scale)
    inset_right = round((text_frame.margin_right
                         if text_frame.margin_right is not None
                         else DEFAULT_LEFT_INSET) * place.scale)
    inset_top = round((text_frame.margin_top
                       if text_frame.margin_top is not None
                       else DEFAULT_TOP_INSET) * place.scale)
    usable = max(1, width - inset_left - inset_right)
    wraps = text_frame.word_wrap is not False

    inherited = _inherited_style(shape, slide)

    # Laid out first, then drawn, because a vertical anchor cannot be applied
    # until the whole block's height is known.
    lines: list[list[tuple[str, object, tuple[int, int, int]]]] = []
    heights: list[int] = []
    alignments: list[object] = []

    for paragraph in text_frame.paragraphs:
        pieces = [
            (run.text, *_run_style(run, inherited, place))
            for run in paragraph.runs if run.text
        ]
        if not pieces:
            lines.append([])
            heights.append(round(place.points_to_pixels(inherited["size_pt"]) * 1.2))
            alignments.append(paragraph.alignment)
            continue

        for wrapped in _wrap_runs(pieces, usable, wraps):
            lines.append(wrapped)
            tallest = max((piece[1].size for piece in wrapped), default=12)
            heights.append(_line_height(paragraph, tallest, place))
            alignments.append(paragraph.alignment)

    block = sum(heights)
    anchor = text_frame.vertical_anchor
    if anchor == MSO_ANCHOR.MIDDLE:
        y = top + (height - block) // 2
    elif anchor == MSO_ANCHOR.BOTTOM:
        y = top + height - block
    else:
        y = top + inset_top

    for pieces, line_height, alignment in zip(lines, heights, alignments, strict=True):
        if pieces:
            span = sum(piece[1].getlength(piece[0]) for piece in pieces)
            if alignment == PP_ALIGN.CENTER:
                x = left + inset_left + (usable - span) / 2
            elif alignment == PP_ALIGN.RIGHT:
                x = left + inset_left + usable - span
            else:
                x = left + inset_left
            for text, font, colour in pieces:
                draw.text((x, y), text, font=font, fill=colour)
                x += font.getlength(text)
        y += line_height


def _line_height(paragraph, font_size_px: float, place: Placement) -> int:
    """How far down the next line sits.

    `line_spacing` is either a multiple of the line height or an exact length --
    python-pptx returns a float for the first and a `Length` for the second, and
    a deck that sets 48.5pt spacing on a 39pt heading means exactly that.
    """
    spacing = paragraph.line_spacing
    if spacing is None:
        return round(font_size_px * 1.2)
    if isinstance(spacing, float | int) and spacing < 10:
        return round(font_size_px * float(spacing) * 1.2)
    return round(int(spacing) * place.scale)


def _wrap_runs(pieces, usable: int, wraps: bool):
    """Break a paragraph's runs into lines that fit, keeping each run's style.

    Measured with the real font rather than by character count: the whole point
    of matching the deck's fonts is that its line breaks land where its own do.
    """
    if not wraps:
        return [list(pieces)]

    lines: list[list] = []
    current: list = []
    used = 0.0
    for text, font, colour in pieces:
        for word in _words(text):
            span = font.getlength(word)
            if current and used + span > usable and word.strip():
                lines.append(current)
                current, used = [], 0.0
                word = word.lstrip()
                span = font.getlength(word)
            if current and current[-1][1] is font and current[-1][2] == colour:
                current[-1] = (current[-1][0] + word, font, colour)
            else:
                current.append((word, font, colour))
            used += span
    if current:
        lines.append(current)
    return lines or [[]]


def _words(text: str) -> list[str]:
    """Words with their trailing space kept, so widths add up as drawn."""
    out: list[str] = []
    for part in text.split(" "):
        out.append(part + " ")
    if out:
        out[-1] = out[-1][:-1]
    return [part for part in out if part]


def _run_style(run, inherited: dict, place: Placement):
    """This run's font and colour, falling back through what it inherits."""
    size_pt = run.font.size.pt if run.font.size is not None else inherited["size_pt"]
    name = run.font.name or inherited["name"]
    bold = run.font.bold if run.font.bold is not None else inherited["bold"]

    colour = inherited["colour"]
    try:
        if run.font.color.type is not None and str(run.font.color.type).startswith("RGB"):
            rgb = run.font.color.rgb
            colour = (rgb[0], rgb[1], rgb[2])
    except Exception:
        pass

    # Points to pixels through the slide's own scale: a 39pt heading on a 9-inch
    # slide drawn 1080 tall is 65px, and getting this wrong is invisible in code
    # and glaring on the frame.
    return font_for(name, place.points_to_pixels(size_pt), bold), colour


def _inherited_style(shape, slide) -> dict:
    """What a run gets when it names nothing itself.

    Its placeholder on the layout, then the master, then the theme's minor font
    and darkest text colour. Without this, "4.Chapter" -- which names no font,
    no weight and no colour -- draws in the wrong face at the wrong weight.
    """
    style = {"size_pt": 18.0, "name": "", "bold": False, "colour": (0, 0, 0)}

    holders = []
    if getattr(shape, "is_placeholder", False):
        try:
            index = shape.placeholder_format.idx
            holders.append(slide.slide_layout.placeholders[index])
            holders.append(slide.slide_layout.slide_master.placeholders[index])
        except (KeyError, AttributeError):
            pass

    for holder in holders:
        if not getattr(holder, "has_text_frame", False):
            continue
        for paragraph in holder.text_frame.paragraphs:
            for run in paragraph.runs:
                if run.font.size is not None:
                    style["size_pt"] = run.font.size.pt
                if run.font.name:
                    style["name"] = run.font.name
                if run.font.bold is not None:
                    style["bold"] = bool(run.font.bold)
                try:
                    if str(run.font.color.type or "").startswith("RGB"):
                        rgb = run.font.color.rgb
                        style["colour"] = (rgb[0], rgb[1], rgb[2])
                except Exception:
                    pass
                if style["name"]:
                    return style
    if not style["name"]:
        style["name"] = _theme_font(slide)
    return style


def _theme_font(slide) -> str:
    """The theme's body typeface, which is what unstyled text actually uses."""
    from lxml import etree

    DRAWING = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    try:
        master = slide.slide_layout.slide_master
        theme = master.part.part_related_by(
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
        )
        root = etree.fromstring(theme.blob)
        latin = root.find(
            f"{DRAWING}themeElements/{DRAWING}fontScheme/{DRAWING}minorFont/{DRAWING}latin")
        return latin.get("typeface", "") if latin is not None else ""
    except Exception:
        return ""


def _slide_background(slide) -> tuple[int, int, int]:
    """The colour behind everything, before any shape is drawn.

    Only the flat colour: a picture background is a shape and is drawn as one.
    White by default, which is what an unset PowerPoint background is.
    """
    from pptx.enum.dml import MSO_FILL

    for holder in (slide, slide.slide_layout, slide.slide_layout.slide_master):
        try:
            fill = holder.background.fill
            if fill.type == MSO_FILL.SOLID:
                colour = fill.fore_color
                if colour.type is not None and str(colour.type).startswith("RGB"):
                    return (colour.rgb[0], colour.rgb[1], colour.rgb[2])
        except Exception:
            continue
    return (255, 255, 255)


# --- fonts --------------------------------------------------------------------------


def font_for(name: str, size_px: float, bold: bool):
    """A font file for the face a deck names, at this size.

    Three ways, in order: a variable font bundled with the repo, set to the
    weight the name asks for; a metric-compatible substitute already installed,
    which preserves the deck's own line breaks; or whatever the renderer's own
    resolver can find.
    """
    from PIL import ImageFont

    size = max(6, round(size_px))
    wanted = (name or "").strip().lower()

    for candidate in font_directory().glob("*.ttf"):
        family = candidate.stem.split("[")[0].lower()
        if family and wanted.startswith(family):
            try:
                font = ImageFont.truetype(str(candidate), size)
                _set_weight(font, wanted, bold)
                return font
            except OSError:
                continue

    from pipeline.rendering import _load_font

    twin = METRIC_TWINS.get(wanted, wanted)
    return _load_font(size, bold=bool(bold), family=twin)


def _set_weight(font, wanted: str, bold: bool) -> None:
    """Pick a variable font's named instance from the face name.

    "Outfit Extra Bold" is one family with a weight axis, not nine files, so the
    weight has to be read out of the name the deck used.
    """
    try:
        # Kept in the font's own spelling: `set_variation_by_name` matches the
        # instance name exactly, so "extrabold" is rejected where "ExtraBold"
        # is accepted. Matching is done on a lowered copy.
        available = {name.decode().lower(): name.decode()
                     for name in font.get_variation_names()}
    except OSError:
        return

    compact = wanted.replace(" ", "").replace("-", "")
    for word in WEIGHT_WORDS:
        if word in compact and word in available:
            font.set_variation_by_name(available[word])
            return
    if bold and "bold" in available:
        font.set_variation_by_name(available["bold"])
    elif "regular" in available:
        font.set_variation_by_name(available["regular"])
