"""What is behind a slide, looked for where PowerPoint draws it from.

A deck's look is rarely the slide's own background setting. Most slides set
none and inherit the layout's or the master's; and a designed deck usually
puts its artwork on the layout as a full-slide *picture*, above every
background setting and beneath the slide's own shapes. Reading only the
settings reported such a deck -- purple gradient art on every slide -- as
plain white, because the master's setting is the theme's white.

So, in PowerPoint's order:

1. A full-slide picture on the layout, then the master, unless the slide or
   the layout hides background graphics. That picture is what shows.
2. The background setting of the slide, then the layout, then the master: a
   picture, a flat colour or a gradient.
3. The theme's light colour, which is what an unset background is.

A near-opaque sheet the layout lays over its artwork is not applied here: the
art is the background, and how to read that sheet is the Assets stage's
choice (`slide_wash`), because decks and viewers disagree about it.
"""

from __future__ import annotations

import logging
from pathlib import Path

from pydantic import BaseModel, Field

from pipeline.deck_shapes import (
    DRAWING_NAMESPACE,
    PRESENTATION_NAMESPACE,
    RELATIONSHIP_NAMESPACE,
)
from pipeline.extraction_assets import AssetSink

logger = logging.getLogger(__name__)

# How much of the slide a picture must cover to be its background, not a figure.
COVERS_THE_SLIDE = 0.97

# python-pptx names theme colours ("accent_1", "background_1"); the theme's
# colour scheme names them "accent1", "lt1". This joins the two.
THEME_COLOUR_KEYS = {
    "background_1": "lt1", "background_2": "lt2", "text_1": "dk1", "text_2": "dk2",
    "light_1": "lt1", "light_2": "lt2", "dark_1": "dk1", "dark_2": "dk2",
}


class SlideBackground(BaseModel):
    """What is behind everything else on a slide."""

    colour: str = ""        # "#RRGGBB"
    gradient: list[str] = Field(default_factory=list)  # "#RRGGBB" per stop, in order
    asset_path: str = ""    # a picture background, stored like a figure
    inherited_from: str = ""  # slide | layout | master | theme -- where it was set


def _hex(colour, theme_colours: dict[str, str]) -> str:
    """A python-pptx colour as "#RRGGBB", a theme colour resolved through the
    theme; "" when it is neither."""
    try:
        if colour.type is None:
            return ""
        if str(colour.type).startswith("RGB"):
            return f"#{colour.rgb}"
        name = str(colour.theme_color).split(" ")[0].lower()
    except (AttributeError, TypeError, ValueError):
        return ""
    resolved = theme_colours.get(THEME_COLOUR_KEYS.get(name, name.replace("_", "")), "")
    return resolved if resolved.startswith("#") else ""


def _store(part, assets: AssetSink) -> str:
    suffix = Path(str(part.partname)).suffix or ".png"
    return assets.store(part.blob, suffix)


def _setting_picture(holder, assets: AssetSink | None) -> str:
    """A background *setting* that is a picture. Read from the XML because
    python-pptx models solid fills but not the `blipFill` it uses."""
    if assets is None:
        return ""
    background = holder._element.find(f"{{{PRESENTATION_NAMESPACE}}}bg")
    blip = None if background is None else background.find(f".//{{{DRAWING_NAMESPACE}}}blip")
    relationship_id = "" if blip is None else blip.get(f"{{{RELATIONSHIP_NAMESPACE}}}embed")
    if not relationship_id:
        return ""
    try:
        return _store(holder.part.related_part(relationship_id), assets)
    except (KeyError, AttributeError) as unresolved:
        logger.warning("a slide background could not be read: %s", unresolved)
        return ""


def _art_picture(holder, slide_width: int, slide_height: int, assets: AssetSink | None) -> str:
    """The topmost picture on a layout or master that covers the whole slide."""
    if assets is None:
        return ""
    for shape in reversed(list(holder.shapes)):
        image = getattr(shape, "image", None) if not getattr(shape, "is_placeholder", False) \
            else None
        if image is None:
            continue
        if ((shape.left or 0) <= slide_width * (1 - COVERS_THE_SLIDE)
                and (shape.top or 0) <= slide_height * (1 - COVERS_THE_SLIDE)
                and (shape.width or 0) >= slide_width * COVERS_THE_SLIDE
                and (shape.height or 0) >= slide_height * COVERS_THE_SLIDE):
            return assets.store(image.blob, f".{image.ext}")
    return ""


def _shows_art_from(holder) -> bool:
    """False when a slide or layout is set to hide the background graphics
    of what it inherits from."""
    return holder._element.get("showMasterSp") != "0"


def _setting(holder, theme_colours: dict[str, str]) -> SlideBackground | None:
    """A flat colour or a gradient set as the background, or None."""
    from pptx.enum.dml import MSO_FILL

    try:
        fill = holder.background.fill
        if fill.type == MSO_FILL.SOLID:
            colour = _hex(fill.fore_color, theme_colours)
            return SlideBackground(colour=colour) if colour else None
        if fill.type == MSO_FILL.GRADIENT:
            stops = [_hex(stop.color, theme_colours) for stop in fill.gradient_stops]
            stops = [stop for stop in stops if stop]
            return SlideBackground(colour=stops[0], gradient=stops) if stops else None
    except (AttributeError, NotImplementedError, TypeError, ValueError):
        return None
    return None


def slide_background(
    slide, assets: AssetSink | None, theme_colours: dict[str, str],
    slide_width: int = 0, slide_height: int = 0,
) -> SlideBackground | None:
    """What is behind the slide, in the order described at the top."""
    layout = slide.slide_layout
    master = getattr(layout, "slide_master", None)

    if slide_width and slide_height and _shows_art_from(slide):
        art_holders = [("layout", layout)]
        if master is not None and _shows_art_from(layout):
            art_holders.append(("master", master))
        for source, holder in art_holders:
            picture = _art_picture(holder, slide_width, slide_height, assets)
            if picture:
                return SlideBackground(asset_path=picture, inherited_from=source)

    holders = [("slide", slide), ("layout", layout)]
    if master is not None:
        holders.append(("master", master))
    for source, holder in holders:
        picture = _setting_picture(holder, assets)
        if picture:
            return SlideBackground(asset_path=picture, inherited_from=source)
        found = _setting(holder, theme_colours)
        if found:
            return found.model_copy(update={"inherited_from": source})

    fallback = theme_colours.get("lt1", "")
    if fallback.startswith("#"):
        return SlideBackground(colour=fallback, inherited_from="theme")
    return None
