"""The shapes on a slide, read from the deck's own XML.

python-pptx models a deck faithfully but stops where PowerPoint's inheritance
begins: a placeholder that declares no position, a paragraph whose bullet is
defined three levels up on the master. These are the lookups that finish the
job, kept together and away from `extraction`, which is about documents in
general rather than decks in particular.

Nothing here builds a ContentBlock or touches a store. Geometry and styling in,
plain values out -- so each rule is testable on its own and the same helper
serves both the text reader and the layout reader.
"""

from __future__ import annotations

from typing import Any

# A slide heading is large text near the top. Below this it is body copy, and
# past this length it is a paragraph that happens to be set big.
SMALLEST_HEADING_POINTS = 18.0
MAXIMUM_HEADING_LENGTH = 120
MAXIMUM_CARD_TITLE_LENGTH = 60      # a card's bold title: a name or a topic, not a sentence

# Two text sizes this close are one hierarchy level -- a kicker over a title --
# and the longer of them is the title.
NEAR_TIE_RATIO = 0.92

# A caption sits against its picture. One inch away it is still plausibly the
# caption; further than that it is body text about something else, and the
# slide heading is the more honest label. EMU, which is what a deck measures in.
WIDEST_CAPTION_GAP_EMU = 914400  # one inch

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


def _headline_of(slide) -> tuple[str, Any]:
    """The slide's heading when it is not in a title placeholder, and its shape.

    Designed decks routinely set their headings as plain text boxes, so
    `shapes.title` is None and every slide came through as "Slide 7" -- which
    made the heading path useless, gave the plan forty identical section names,
    and lost the one piece of text the author most wanted kept.

    The heading is the largest text in the upper part of the slide. Where two
    sizes are within a hair of each other -- a small kicker above a title, like
    "4.Chapter" over "Networks that Learn" -- the longer line wins, because the
    kicker is a label and the title is the sentence.

    The shape comes back with it so the caller can skip the line it came from:
    a text box is still an ordinary shape, so without that the heading is
    emitted a second time as a paragraph.
    """
    candidates: list[tuple[float, str, Any]] = []
    for shape in slide.shapes:
        if not shape.has_text_frame or shape.top is None or shape.height is None:
            continue
        size, _bold, _align = _first_run_style(shape)
        if size < SMALLEST_HEADING_POINTS:
            continue
        line = _short_first_line(shape)
        if line:
            candidates.append((size, line, shape._element))

    if not candidates:
        return "", None
    largest = max(size for size, _line, _element in candidates)
    close = [(line, element) for size, line, element in candidates
             if size >= largest * NEAR_TIE_RATIO]
    return max(close, key=lambda candidate: len(candidate[0]))


def _caption_near(picture, slide) -> tuple[str, Any]:
    """The text sitting against a picture, which is what a caption is on a slide.

    PowerPoint names every picture "Image 0", "Image 1" and so on, so captioning
    from `shape.name` labelled sixty-three different figures "Image 0" thirty-three
    times over. Everything downstream reads the caption -- the drawing agent
    describes from it, Assets & Design asks Use or Skip on it, and Generation
    matches the author's own figures by it -- so a name from the XML is worse
    than useless there.

    A caption is directly below the picture or directly beside it, and close: any
    further away and the text belongs to something else, so the caller falls back
    to the heading. Pure geometry, no model, identical on every run.

    The shape comes back with the text so the caller can stop it being emitted a
    second time as a paragraph of its own.
    """
    left, top, width, height = picture.left, picture.top, picture.width, picture.height
    if None in (left, top, width, height):
        return "", None
    right, bottom = left + width, top + height

    nearest: tuple[int, str, Any] | None = None
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        if None in (shape.left, shape.top, shape.width, shape.height):
            continue
        line = _short_first_line(shape)
        if not line:
            continue
        if shape.left < right and shape.left + shape.width > left and shape.top >= bottom:
            gap = shape.top - bottom
        elif shape.top < bottom and shape.top + shape.height > top and shape.left >= right:
            gap = shape.left - right
        else:
            continue
        if gap <= WIDEST_CAPTION_GAP_EMU and (nearest is None or gap < nearest[0]):
            nearest = (gap, line, shape._element)

    return nearest[1:] if nearest else ("", None)


def _is_card_title(element) -> bool:
    """Whether a text box is a card's title: one short line, all of it bold.

    Decks lay a topic out as cards -- an icon, a bold title, a line under it --
    and the title sits against the icon, so it was taken as the icon's caption
    and dropped from the text: "Broca's Area" survived only as a figure's name,
    and the extraction agent had to put six slides' titles back by hand. A title
    is kept as a heading (and still captions its icon); a caption in ordinary
    type is still only a caption.
    """
    if element is None:
        return False
    lines = []
    for paragraph in element.iter(f"{{{DRAWING_NAMESPACE}}}p"):
        runs = [run for run in paragraph.iter(f"{{{DRAWING_NAMESPACE}}}r")
                if "".join(run.itertext()).strip()]
        if runs:
            lines.append(runs)
    if len(lines) != 1:
        return False
    text = "".join("".join(run.itertext()) for run in lines[0]).strip()
    bold = all((properties := run.find(f"{{{DRAWING_NAMESPACE}}}rPr")) is not None
               and properties.get("b") in ("1", "true") for run in lines[0])
    # A step's bold number ("1", "2") badges a card; it does not title one.
    return (bold and len(text) <= MAXIMUM_CARD_TITLE_LENGTH and not text.endswith((".", ":"))
            and any(character.isalpha() for character in text))


def _short_first_line(shape) -> str:
    """A text shape's first line, or empty when it is too long to be a label."""
    written = shape.text_frame.text.strip()
    line = written.splitlines()[0].strip() if written else ""
    return line if len(line) <= MAXIMUM_HEADING_LENGTH else ""


def _bullet_of(properties) -> bool | None:
    """Whether a paragraph-properties element turns a bullet on, off, or says nothing."""
    if properties is None:
        return None
    if properties.find(f"{{{DRAWING_NAMESPACE}}}buNone") is not None:
        return False
    for tag in ("buChar", "buAutoNum"):
        if properties.find(f"{{{DRAWING_NAMESPACE}}}{tag}") is not None:
            return True
    return None


def _is_bulleted(paragraph, list_styles: list) -> bool:
    """Whether a slide paragraph carries a bullet.

    Not `paragraph.level`, which is indent depth: a first-level bullet and a
    plain paragraph are both level 0, so reading it meant an ordinarily bulleted
    deck lost every list it had while a merely indented line became a list item.

    The bullet lives in the paragraph's own properties as buChar or buAutoNum,
    or is switched off with buNone. When the paragraph says nothing, the setting
    is inherited from the placeholder's list style on the layout and then the
    master, which is where an untouched deck's bullets actually come from.
    `list_styles` is that chain from `_inherited_list_styles`, resolved once per
    shape by the caller rather than once per paragraph.
    """
    own = _bullet_of(paragraph._pPr)
    if own is not None:
        return own

    level = paragraph.level or 0
    for style in list_styles:
        inherited = _bullet_of(style.find(f"{{{DRAWING_NAMESPACE}}}lvl{level + 1}pPr"))
        if inherited is not None:
            return inherited
    return False


def _own_list_style(element):
    """A shape element's own `lstStyle`, which sits inside its `txBody`."""
    if element is None:
        return None
    body = element.find(f"{{{PRESENTATION_NAMESPACE}}}txBody")
    return body.find(f"{{{DRAWING_NAMESPACE}}}lstStyle") if body is not None else None


def _inherited_list_styles(shape, slide) -> list:
    """Where a shape's bullet setting is looked up, nearest first.

    Its own list style, then the placeholder it follows on the layout and on the
    master, then the master's body style -- the last of which is where a deck
    nobody has restyled actually defines its bullets.
    """
    styles = []
    own = _own_list_style(shape._element)
    if own is not None:
        styles.append(own)

    if not shape.is_placeholder:
        return styles

    index = shape.placeholder_format.idx
    layout = getattr(slide, "slide_layout", None)
    master = getattr(layout, "slide_master", None)
    for source in (layout, master):
        if source is None:
            continue
        try:
            inherited = source.placeholders[index]
        except (KeyError, AttributeError):
            continue
        style = _own_list_style(inherited._element)
        if style is not None:
            styles.append(style)

    if master is not None:
        text_styles = master._element.find(f"{{{PRESENTATION_NAMESPACE}}}txStyles")
        if text_styles is not None:
            for tag in ("bodyStyle", "otherStyle"):
                found = text_styles.find(f"{{{PRESENTATION_NAMESPACE}}}{tag}")
                if found is not None:
                    styles.append(found)

    return styles


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


