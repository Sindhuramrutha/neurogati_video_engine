"""The video's look: which source it follows, and a person's choices on top.

Every transferred deck with styling is an option, and so is the renderer's own
look. Within a deck, each part of the frame the renderer colours -- the
background, the panels text and pictures sit on, the accent -- can be set to a
colour of that deck's palette or to any colour a person picks, and the headings
and body text to either of its fonts. Ready-made themes are starting points
built from the deck's own palette. Nothing is guessed: every choice is a value
a person set, and the same choices always draw the same frames.

A choice is never a no-op: `style_for` honours the panel a person picked,
and `readability` says how well the text reads on it.

`effective_look` turns the stored look and choices into what the renderer reads
(`RenderStyle.from_look`), so the renderer does not need to know choices exist.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field

from pipeline.core import OperationFailed, require_project
from pipeline.extraction import Extraction

# role -> (name, the palette colour a deck uses for it when nothing is chosen)
COLOUR_ROLES = {
    "background": ("Background", "lt1"),
    "panels": ("Panels", "lt2"),
    "accent": ("Accent", "accent1"),
}
FONT_ROLES = {"heading_font": "Headings", "body_font": "Body text"}
FONT_CHOICES = {"heading": "The deck's heading font", "body": "The deck's body font",
                "renderer": "The renderer's font"}
HEX = re.compile(r"#[0-9a-fA-F]{6}")
# The least contrast text needs against what it sits on to be read comfortably
# (WCAG AA for normal text).
READABLE_CONTRAST = 4.5

# Starting points, from the deck's own palette. A theme is only offered when the
# deck has every colour it names, and only when its text reads well on its
# panel: a theme that is hard to read is not a starting point.
THEMES = [
    ("deck", "Deck's own", "The colours as the deck's author set them.", {}),
    ("light", "Light", "A light background with dark text.",
     {"background": "lt1", "panels": "lt2", "accent": "accent1"}),
    ("dark", "Dark", "A dark background with light text.",
     {"background": "dk1", "panels": "dk2", "accent": "accent1"}),
    # No panel named: it is made to suit whatever the accent's lightness is.
    ("accent", "Accent-led", "The deck's main colour behind everything.",
     {"background": "accent1", "accent": "accent2"}),
]


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

    # How to read a full-bleed wash a deck lays over its own background art.
    # Decks write these inconsistently and the two readings look very different:
    # "as_written" follows the spec and PowerPoint -- a pale background and
    # legible text -- while "inverted" keeps the artwork vivid, which is how
    # some viewers show it and can put the deck's dark text on a dark field.
    # There is no answer in the file, so it is a choice, and it is here rather
    # than hidden in the compositor.
    slide_wash: str = "as_written"

    # A person's choices on top of the deck: role -> a palette key ("accent2")
    # or, for a font role, one of FONT_CHOICES. Missing means the deck's own.
    choices: dict[str, str] = Field(default_factory=dict)
    # Whether the renderer's own frames draw the deck's background art.
    background_art: bool = True

    @property
    def is_available(self) -> bool:
        return bool(self.colours or self.heading_font or self.background_asset_path)


def looks_in_extraction(extraction: Extraction) -> list[ProjectLook]:
    """Every transferred document with styling, in the order they were transferred."""
    looks = []
    for document in extraction.documents:
        if document.design is None:
            continue
        background = next(
            (slide.background for slide in document.slides if slide.background), None
        )
        looks.append(ProjectLook(
            from_file=document.file_name,
            aspect_ratio=document.design.aspect_ratio,
            theme_name=document.design.theme_name,
            colours=dict(document.design.colours),
            heading_font=document.design.major_font,
            body_font=document.design.minor_font,
            background_colour=background.colour if background else "",
            background_asset_path=background.asset_path if background else "",
        ))
    return [look for look in looks if look.is_available]


def look_from_extraction(extraction: Extraction, prefer: str = "") -> ProjectLook:
    """The styling of the chosen document, or of the first that has any.

    One rather than merged: two decks with different themes do not average
    into a third, and a video has one look.
    """
    looks = looks_in_extraction(extraction)
    chosen = next((look for look in looks if look.from_file == prefer), None)
    return chosen or (looks[0] if looks else ProjectLook())


def _hex(colours: dict[str, str], choice: str) -> str:
    """A choice as a colour: a colour a person picked, or one of the palette's."""
    if HEX.fullmatch(choice or ""):
        return choice.upper()
    value = colours.get(choice, "")
    return value if value.startswith("#") else ""


def effective_look(look: ProjectLook) -> dict[str, Any]:
    """The look with the choices applied, in the shape the renderer reads."""
    result = look.model_dump() | {"is_available": look.is_available}
    colours = dict(look.colours)
    choices = look.choices
    if (value := _hex(colours, choices.get("background", ""))):
        result["background_colour"] = value
    if (value := _hex(colours, choices.get("panels", ""))):
        colours["lt2"] = value
    if (value := _hex(colours, choices.get("accent", ""))):
        colours["accent1"] = value
    fonts = {"heading": look.heading_font, "body": look.body_font, "renderer": ""}
    for role in FONT_ROLES:
        if choices.get(role) in fonts:
            result[role] = fonts[choices[role]]
    if not look.background_art:
        result["background_asset_path"] = ""
    result["colours"] = colours
    return result


def choose_look(slug: str, change: dict[str, Any]) -> None:
    """Apply one change: the source (`from_file`, "" for the renderer's look), a
    role's choice (`role` and `value`, "" for the deck's own), or `background_art`."""
    from pipeline.assets import AssetLibraryStore
    from pipeline.extraction import ExtractionStore

    project = require_project(slug)
    store = AssetLibraryStore(project.root)
    library = store.load()
    look = library.look

    if "from_file" in change:
        wanted = change["from_file"] or ""
        if not wanted:
            look.use_source_styling = False
        else:
            looks = looks_in_extraction(ExtractionStore(project.root).load())
            chosen = next((option for option in looks if option.from_file == wanted), None)
            if chosen is None:
                raise OperationFailed(f"{wanted} has no styling in the last transfer.")
            # A new deck has its own palette, so choices made for another are dropped.
            same = chosen.from_file == look.from_file
            look = chosen.model_copy(update={"use_source_styling": True,
                                             "slide_wash": look.slide_wash,
                                             "background_art": look.background_art,
                                             "choices": look.choices if same else {}})
    if "theme" in change:
        theme = next((t for t in THEMES if t[0] == change["theme"]), None)
        if theme is None or any(not _hex(look.colours, key) for key in theme[3].values()):
            raise OperationFailed(f"This deck has no {change['theme']!r} theme.")
        fonts = {k: v for k, v in look.choices.items() if k in FONT_ROLES}
        look.choices = fonts | theme[3]
    if "role" in change:
        role, value = change["role"], change.get("value") or ""
        if role in COLOUR_ROLES:
            fits = not value or bool(_hex(look.colours, value))
            value = value.upper() if HEX.fullmatch(value) else value
        else:
            fits = role in FONT_ROLES and (not value or value in FONT_CHOICES)
        if not fits:
            raise OperationFailed(f"{role} cannot be {value!r}.")
        look.choices = {k: v for k, v in (look.choices | {role: value}).items() if v}
    if "background_art" in change:
        look.background_art = bool(change["background_art"])

    library.look = look
    store.save(library)


def style_for(look: ProjectLook, project_root):
    """The renderer's style for this look, with the panel it should have.

    One text colour is drawn both straight on the background and on the panel,
    so the two have to be the same kind -- both light, or both dark. A panel a
    person chose is honoured as it is, and `readability` says if text will not
    read on it. With none chosen, the panel is made to suit the background: the
    renderer took a dark background's panel from the deck's "light 2" colour,
    which put light text on a light panel.
    """
    from dataclasses import dataclass, fields

    from pipeline.rendering import RenderStyle, _hex_to_rgb

    base = RenderStyle.from_look(effective_look(look), project_root)
    chosen = _hex(look.colours, look.choices.get("panels", ""))
    if not chosen:
        if contrast(base.text_colour, base.panel_colour) >= READABLE_CONTRAST:
            return base
        chosen = "#{:02X}{:02X}{:02X}".format(
            *_panel_that_reads(base.background_colour, base.text_colour))

    @dataclass
    class ChosenStyle(RenderStyle):
        chosen_panel: tuple[int, int, int] = (255, 255, 255)

        @property
        def panel_colour(self) -> tuple[int, int, int]:
            return self.chosen_panel

    return ChosenStyle(**{f.name: getattr(base, f.name) for f in fields(base)},
                       chosen_panel=_hex_to_rgb(chosen, base.panel_colour))


def _panel_that_reads(
    background: tuple[int, int, int], text: tuple[int, int, int]
) -> tuple[int, int, int]:
    """A panel made from the background that its text reads on.

    First the background lifted a little, which is what a panel usually is. On a
    mid-tone background that is not enough, so the background is then stepped
    away from the text's colour -- darker under light text, lighter under dark
    -- until the text reads. Fixed steps: the same colours, the same panel.
    """
    lifted = tuple(min(255, value + 24) for value in background)
    if contrast(text, lifted) >= READABLE_CONTRAST:
        return lifted
    away = -16 if sum(text) > sum(background) else 16
    panel = background
    for _ in range(16):
        panel = tuple(min(255, max(0, value + away)) for value in panel)
        if contrast(text, panel) >= READABLE_CONTRAST:
            break
    return panel


def _luminance(colour: tuple[int, int, int]) -> float:
    def channel(value: int) -> float:
        share = value / 255
        return share / 12.92 if share <= 0.03928 else ((share + 0.055) / 1.055) ** 2.4
    red, green, blue = (channel(v) for v in colour)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    """The WCAG contrast ratio between two colours: 1 (none) to 21 (black on white)."""
    lighter, darker = sorted((_luminance(first), _luminance(second)), reverse=True)
    return round((lighter + 0.05) / (darker + 0.05), 1)


def readability(style) -> dict[str, Any]:
    """How well the text reads on the panel it sits on, and the accent on the
    background it sits on."""
    text = contrast(style.text_colour, style.panel_colour)
    accent = contrast(style.accent_colour, style.background_colour)
    return {"text_on_panel": text, "text_is_readable": text >= READABLE_CONTRAST,
            "accent_on_background": accent, "accent_is_visible": accent >= 1.5,
            "needed": READABLE_CONTRAST}


def themes_for(look: ProjectLook, project_root) -> list[dict[str, Any]]:
    """The ready-made starting points this deck's palette allows, each with the
    colours it would draw, and which one the current choices match."""
    as_hex = "#{:02x}{:02x}{:02x}".format
    current = {k: v for k, v in look.choices.items() if k in COLOUR_ROLES}
    found = []
    for key, name, about, choices in THEMES:
        if any(not _hex(look.colours, palette_key) for palette_key in choices.values()):
            continue
        style = style_for(look.model_copy(update={"choices": choices}), project_root)
        if not readability(style)["text_is_readable"]:
            continue
        found.append({
            "key": key, "name": name, "about": about, "is_current": current == choices,
            "background": as_hex(*style.background_colour), "panel": as_hex(*style.panel_colour),
            "accent": as_hex(*style.accent_colour), "text": as_hex(*style.text_colour)})
    return found


def wash_preview(slug: str, wash: str):
    """The chosen deck's first slide, drawn with this reading of its sheet: what
    the choice really does, not a description of it. Drawn once and kept."""
    import hashlib

    from pipeline.assets import AssetLibraryStore
    from pipeline.slide_frame import compose_slide

    project = require_project(slug)
    look = AssetLibraryStore(project.root).load().look
    deck = project.root / "sources" / look.from_file
    is_deck = bool(look.from_file) and deck.suffix.lower() == ".pptx" and deck.exists()
    if wash not in ("as_written", "inverted", "ignored") or not is_deck:
        return None
    made_from = f"{look.from_file}:{deck.stat().st_size}:{int(deck.stat().st_mtime)}"
    name = hashlib.sha256(made_from.encode("utf-8")).hexdigest()[:12]
    target = project.root / "assets" / "look-previews" / f"{name}-{wash}.png"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        compose_slide(deck, 1, target, width=640, height=360, wash=wash)
    return target


def look_options(extraction: Extraction) -> dict[str, Any]:
    """What the Look tab offers: every source with styling, and the roles."""
    return {
        "sources": [look.model_dump() for look in looks_in_extraction(extraction)],
        "colour_roles": [{"key": k, "name": name, "deck_default": default}
                         for k, (name, default) in COLOUR_ROLES.items()],
        "font_roles": [{"key": k, "name": name} for k, name in FONT_ROLES.items()],
        "font_choices": FONT_CHOICES,
    }
