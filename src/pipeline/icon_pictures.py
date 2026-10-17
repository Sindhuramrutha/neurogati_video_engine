"""Icons for a scene: small symbols beside words or in a diagram, from Iconify's openly
licensed sets or the Lucide set bundled in `resources/icons` (ISC) when offline --
looked up at once, drawn in the scene's colour in one browser, kept with credit.
"""

from __future__ import annotations

import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from pipeline.config import REPO_ROOT
from pipeline.outside_pictures import _get, _icon_path, _keep

logger = logging.getLogger(__name__)

ICON_PIXELS = 512
LUCIDE = REPO_ROOT / "resources" / "icons" / "lucide"
# Licences that allow use in a commercial video, with credit where they ask for it.
ICON_LICENCES = {"MIT", "Apache-2.0", "ISC", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0",
                 "Unlicense", "CC-BY-3.0", "CC-BY-4.0", "CC-BY-SA-3.0", "CC-BY-SA-4.0"}



def _iconify(name: str) -> tuple[str, dict[str, Any]] | None:
    """The first icon Iconify has for `name` in a set whose licence allows
    commercial use: (its SVG, what to credit)."""
    data = _get("https://api.iconify.design/search", {"query": name, "limit": 48})
    collections = data.get("collections") or {}
    for icon in data.get("icons") or []:
        prefix, _, icon_name = icon.partition(":")
        collection = collections.get(prefix) or {}
        licence = (collection.get("license") or {}).get("spdx", "")
        if licence not in ICON_LICENCES or collection.get("palette"):
            continue
        svg = _get(f"https://api.iconify.design/{prefix}/{icon_name}.svg",
                   {"height": ICON_PIXELS}, as_json=False).decode("utf-8")
        return svg, {"source": f"Iconify: {collection.get('name', prefix)}",
                     "title": icon, "licence": licence,
                     "licence_url": (collection.get("license") or {}).get("url", ""),
                     "author": (collection.get("author") or {}).get("name", "unknown"),
                     "page": f"https://icon-sets.iconify.design/{prefix}/{icon_name}/"}
    return None


def _lucide(name: str) -> tuple[str, dict[str, Any]] | None:
    """The bundled Lucide icon whose name or tags best match `name`."""
    tags_file = LUCIDE / "tags.json"
    if not tags_file.exists():
        return None
    words = set(re.findall(r"[a-z]+", name.lower()))
    tags = json.loads(tags_file.read_text(encoding="utf-8"))

    def score(item) -> int:
        icon, its_tags = item
        named = set(icon.split("-"))
        return 3 * len(words & named) + len(words & {w for t in its_tags for w in t.split()})

    icon, _ = max(tags.items(), key=score, default=("", []))
    if not icon or score((icon, tags[icon])) == 0:
        return None
    svg = (LUCIDE / "icons" / f"{icon}.svg").read_text(encoding="utf-8")
    return svg, {"source": "Lucide (bundled)", "title": icon, "licence": "ISC",
                 "licence_url": "https://lucide.dev/license", "author": "Lucide Contributors",
                 "page": f"https://lucide.dev/icons/{icon}"}


def rasterise(svgs: list[str], colour: str, pixels: int = ICON_PIXELS) -> list[bytes]:
    """SVG icons as transparent PNGs in `colour`, drawn by the browser the web
    renderer already uses (Chromium, through Playwright) -- one browser for all of
    them: one per icon cost seconds and a hundred megabytes each."""
    from playwright.sync_api import sync_playwright

    def page_for(svg: str) -> str:
        svg = re.sub(r"<!--.*?-->", "", svg, flags=re.DOTALL).replace("currentColor", colour)
        svg = re.sub(r'\swidth="[^"]*"', "", svg, count=1)
        svg = re.sub(r'\sheight="[^"]*"', "", svg, count=1)
        svg = svg.replace("<svg", f'<svg width="{pixels}" height="{pixels}"', 1)
        return ("<html><body style='margin:0;background:transparent'>"
                f"<div id='icon' style='width:{pixels}px;height:{pixels}px'>{svg}</div>"
                "</body></html>")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": pixels, "height": pixels})
            drawn = []
            for svg in svgs:
                page.set_content(page_for(svg))
                drawn.append(page.locator("#icon").screenshot(omit_background=True))
            return drawn
        finally:
            browser.close()


def _icon_source(name: str) -> tuple[str, dict[str, Any]] | None:
    try:
        found = _iconify(name)
    except Exception as failure:          # offline: the bundled set
        logger.info("Iconify not reached for %s: %s", name, failure)
        found = None
    return found or _lucide(name)


def find_icons(folder: Path, names: list[str], colour: str,
               state: dict[str, Any]) -> list[Path]:
    """An icon for each name, from Iconify or else the bundled set, in the scene's
    colour, kept with its credit: looked up at once, drawn in one browser."""
    from pipeline.scene_state import add_event

    todo = [n for n in names if not (_icon_path(folder, n).exists()
                                     and _icon_path(folder, n).with_suffix(".json").exists())]
    if todo:
        with ThreadPoolExecutor(max_workers=len(todo)) as pool:
            found = dict(zip(todo, pool.map(_icon_source, todo), strict=True))
        for name in todo:
            if found[name] is None:
                add_event(state, "note", f"No icon was found for \"{name}\".")
        ready = [(name, *found[name]) for name in todo if found[name] is not None]
        try:
            drawn = rasterise([svg for _, svg, _ in ready], colour) if ready else []
        except Exception as failure:      # no browser: the scene goes on without them
            add_event(state, "note", f"The icons could not be drawn ({failure}).")
            drawn = []
        for (name, _svg, meta), png in zip(ready, drawn, strict=False):
            _keep(folder, _icon_path(folder, name), png, meta | {"asked": name, "kind": "icon"})
    return [_icon_path(folder, n) for n in names if _icon_path(folder, n).exists()]


def find_icon(folder: Path, name: str, colour: str, state: dict[str, Any]) -> Path | None:
    found = find_icons(folder, [name], colour, state)
    return found[0] if found else None
