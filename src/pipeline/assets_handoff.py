"""Assets & Design, handed on: the transferred snapshot later stages read.

The layer works like Extraction. What is being decided -- the library, with a
person's Use and Skip on top of the rules -- is one document; what later stages
read is another, written only by **Transfer to the next layer**. A decision in
progress never leaks into a render, and a render reads exactly the pictures and
the look that were transferred, however long ago.

Everything here is deterministic. Gathering is a function of the transferred
extraction and the stored decisions; every picture is measured against fixed
thresholds (`RULES`, the same numbers the code applies); a picture's outcome is
the person's decision if there is one, the rule's otherwise; and no model is
called anywhere on this layer. The same inputs give the same library, every time.

Stored beside the library, at `assets/library.confirmed.json`.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from pipeline import upstream
from pipeline.assets import (
    SMALLEST_USABLE_PIXELS,
    AssetLibrary,
    AssetLibraryStore,
)
from pipeline.brand_kit import BrandKit, BrandKitStore, brand_fingerprint, brand_view
from pipeline.core import OperationFailed, require_project
from pipeline.extraction import BlockKind, ExtractionStore
from pipeline.figure_prep import (
    EDGE_BAND_FRACTION,
    EDGE_INK_FRACTION,
    FLATTEST_USABLE_RANGE,
    SMALLEST_PREPARED_PIXELS,
    SMALLEST_WORTHWHILE_TRIM,
    WIDEST_USABLE_RATIO,
)
from pipeline.project_look import (
    effective_look,
    look_options,
    readability,
    style_for,
    themes_for,
)
from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore
from pipeline.storage.layout import artifact_path

SLIDE_WASHES = {
    "as_written": "As written: the deck's near-opaque sheet stays over its artwork, "
                  "which gives a pale background and dark, legible text -- what "
                  "PowerPoint shows.",
    "inverted": "Artwork vivid: the sheet is read as see-through, so the background art "
                "shows at full strength -- how some viewers show it; dark text may sit "
                "on dark art.",
    "ignored": "No sheet: the sheet is left off entirely and only the artwork is drawn.",
}

# Every check a picture goes through, in the order the page lists them. The
# numbers are the ones the code uses, imported, so the page cannot drift.
RULES = [
    {"flag": "decoration", "name": "Decoration",
     "test": f"Smaller than {SMALLEST_USABLE_PIXELS} px on either side",
     "outcome": "Won't show"},
    {"flag": "blank", "name": "Blank",
     "test": f"One flat tone throughout (tonal range under {FLATTEST_USABLE_RANGE})",
     "outcome": "Won't show"},
    {"flag": "sliver", "name": "Sliver",
     "test": f"More than {WIDEST_USABLE_RATIO:g} times wider than tall, or taller than wide",
     "outcome": "Won't show"},
    {"flag": "tiny", "name": "Too small",
     "test": f"Under {SMALLEST_PREPARED_PIXELS} px once its border is trimmed",
     "outcome": "Won't show"},
    {"flag": "unreadable", "name": "Unreadable", "test": "The file cannot be opened",
     "outcome": "Won't show"},
    {"flag": "cut_off", "name": "Cut off?", "test": "Ink runs off an edge of the picture",
     "outcome": "Shows -- flagged to check"},
    {"flag": "trimmed", "name": "Trimmed", "test": "A uniform border around the picture",
     "outcome": "Shows the trimmed copy; the original is kept"},
]


class ConfirmedAssets(BaseModel):
    library: AssetLibrary = Field(default_factory=AssetLibrary)
    brand: BrandKit = Field(default_factory=BrandKit)
    confirmed_at: str = ""
    fingerprint: str = ""
    from_transfer: str = ""   # the extraction transfer the library was gathered from


class ConfirmedAssetStore(JsonDocumentStore[ConfirmedAssets]):
    def __init__(self, project_root) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.ASSETS).with_name(
                "library.confirmed.json"),
            model_type=ConfirmedAssets, build_default=ConfirmedAssets,
            description="transferred assets",
        )


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def fingerprint(library: AssetLibrary, brand: BrandKit | None = None) -> str:
    """A digest of everything a later stage reads: which pictures, their
    decisions and measurements, the look, and the brand assets (left out while
    there are none, so a digest from before they existed still matches)."""
    parts = [
        # `use_original` only when chosen, so an earlier digest still matches.
        [f.asset_path, f.use, f.in_extraction, sorted(f.flags), f.prepared_path,
         *(["original"] if f.use_original else [])]
        for f in library.figures
    ]
    extra = [brand_fingerprint(brand)] if brand and not brand.is_empty else []
    look = library.look.model_dump()
    # Left out at their defaults, so a digest from before they existed still matches.
    if not look["choices"]:
        del look["choices"]
    if look["background_art"]:
        del look["background_art"]
    text = json.dumps([parts, look, *extra], sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]


def _transfer_stamp(extraction) -> str:
    return extraction.confirmed_at or extraction.extracted_at


def confirmed_library(project) -> AssetLibrary:
    """What later stages read: the transferred library.

    A project from before transfers existed has a library and no snapshot; it
    is taken as transferred once, as it stands, so what it renders does not
    change underneath it.
    """
    store = ConfirmedAssetStore(project.root)
    confirmed = store.load()
    if confirmed.confirmed_at:
        return confirmed.library
    live = AssetLibraryStore(project.root).load()
    if live.figures:
        store.save(ConfirmedAssets(library=live, confirmed_at=_now(),
                                   fingerprint=fingerprint(live),
                                   from_transfer=live.gathered_from))
    return live


def brand_for_later_stages(project) -> BrandKit:
    """The transferred brand kit; the working one until the first transfer."""
    confirmed = ConfirmedAssetStore(project.root).load()
    return confirmed.brand if confirmed.confirmed_at else BrandKitStore(project.root).load()


# --- what the person does ----------------------------------------------------------


def confirm_assets(slug: str) -> dict[str, Any]:
    """Transfer the library as it stands to the next layer."""
    project = require_project(slug)
    library = AssetLibraryStore(project.root).load()
    brand = BrandKitStore(project.root).load()
    extraction = ExtractionStore(project.root).load()
    # Taking the last brand asset off is a change too, so it can be transferred.
    had_brand = not ConfirmedAssetStore(project.root).load().brand.is_empty
    # A source with no pictures, and no brand assets, is still transferred: the
    # plan needs to know there is nothing, as much as what there is.
    if not extraction.documents and brand.is_empty and not had_brand:
        raise OperationFailed("Nothing is extracted yet, so there is nothing to transfer. "
                              "Transfer the extraction first, or add a brand asset.")
    if library.figures and library.gathered_from != _transfer_stamp(extraction):
        raise OperationFailed(
            "The extraction was transferred again after these pictures were gathered. "
            "Gather again on the Extracted assets tab, check the pictures, then transfer.")
    ConfirmedAssetStore(project.root).save(ConfirmedAssets(
        library=library, brand=brand, confirmed_at=_now(),
        fingerprint=fingerprint(library, brand), from_transfer=library.gathered_from))
    upstream.record(project, "assets")
    return assets_page(slug)


def set_slide_wash(slug: str, wash: str) -> dict[str, Any]:
    if wash not in SLIDE_WASHES:
        raise OperationFailed(f"{wash!r} is not a slide wash. Use one of: "
                              f"{', '.join(SLIDE_WASHES)}.")
    project = require_project(slug)
    store = AssetLibraryStore(project.root)
    library = store.load()
    library.look.slide_wash = wash
    store.save(library)
    return assets_page(slug)


# --- what the page shows -----------------------------------------------------------


def _handed_on(extraction) -> dict[str, Any]:
    """The last layer's transfer: its files and how many pictures each has."""
    files = []
    for document in extraction.documents:
        pictures = {b.asset_path for b in document.blocks
                    if b.kind == BlockKind.FIGURE and b.asset_path}
        files.append({"file_name": document.file_name, "picture_count": len(pictures)})
    return {"transferred_at": _transfer_stamp(extraction), "files": files}


def handoff_state(project, library: AssetLibrary) -> dict[str, Any]:
    extraction = ExtractionStore(project.root).load()
    confirmed = ConfirmedAssetStore(project.root).load()
    brand = BrandKitStore(project.root).load()
    current = fingerprint(library, brand)
    return {
        "has_confirmed": bool(confirmed.confirmed_at),
        "confirmed_at": confirmed.confirmed_at,
        "pending": bool(library.figures or library.look.is_available or not brand.is_empty
                        or not confirmed.brand.is_empty) and (
            # Compared with the transfer as it reads now, not with a digest stored
            # then: a model that has since gained a field reads both the same way.
            current != fingerprint(confirmed.library, confirmed.brand)
            or upstream.is_behind(project, "assets")),
        "in_step": library.gathered_from == _transfer_stamp(extraction),
        "confirmed_usable_count": len(confirmed.library.usable()),
    }


def _look_preview(project, look) -> dict[str, Any]:
    """The colours and fonts the renderer will draw with, from the renderer's own
    style, so the page's preview cannot disagree with the video."""
    from pipeline.rendering import DEFAULT_STYLE

    effective = effective_look(look)
    style = style_for(look, project.root) if look.use_source_styling else DEFAULT_STYLE
    colour = "#{:02x}{:02x}{:02x}".format
    return {
        "background": colour(*style.background_colour), "panel": colour(*style.panel_colour),
        "accent": colour(*style.accent_colour), "text": colour(*style.text_colour),
        "dim": colour(*style.dim_text_colour),
        "heading_font": style.heading_font, "body_font": style.body_font,
        "art": effective["background_asset_path"] if style.background_image else "",
        "readability": readability(style),
        "themes": themes_for(look, project.root) if look.use_source_styling else [],
        # What each colour role is set to now, as a colour.
        "chosen": {"background": colour(*style.background_colour),
                   "panels": colour(*style.panel_colour), "accent": colour(*style.accent_colour)},
    }


def assets_page(slug: str) -> dict[str, Any]:
    """The library, with where it came from, the rules, and the hand-off state."""
    from pipeline.assets import read_asset_library

    project = require_project(slug)
    page = read_asset_library(slug)
    library = AssetLibraryStore(project.root).load()
    return page | {
        "source": _handed_on(ExtractionStore(project.root).load()),
        "rules": RULES,
        # The numbers gathering uses on a picture, so the page can say exactly
        # when it trims and when it flags a crop.
        "picture_rules": {"trim_at": SMALLEST_WORTHWHILE_TRIM, "edge_band": EDGE_BAND_FRACTION,
                          "edge_ink": EDGE_INK_FRACTION},
        "brand": brand_view(project),
        "look_options": look_options(ExtractionStore(project.root).load()),
        "look_preview": _look_preview(project, library.look),
        "slide_washes": SLIDE_WASHES,
        "handoff": handoff_state(project, library),
    }
