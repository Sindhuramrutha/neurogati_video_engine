"""Icons for a scene: small symbols beside words or in a diagram, from the Lucide set
bundled in `resources/icons` (ISC) -- nothing is searched for on the web. A brief asks
for them on its own line:

    ICON: microscope, brain, lightning                -- up to three

Each is drawn in the scene's colour (one browser for all of a scene's icons) and kept
in the scene's folder as `icon-<key>.png`, with a `.json` beside it and an entry in
the scene's `sources.json`, which Export lists as credits.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
from pathlib import Path
from typing import Any

from pipeline.config import REPO_ROOT

ICON_LINE = re.compile(r"^\s*ICONS?\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
MOST_ICONS = 3
ICON_PIXELS = 512
LUCIDE = REPO_ROOT / "resources" / "icons" / "lucide"
_SOURCES_LOCK = threading.Lock()


def wanted(on_screen: str) -> list[str]:
    """The icons the brief asks for, by name."""
    found = ICON_LINE.search(on_screen or "")
    names = [n.strip() for n in re.split(r"[,;]| and ", found.group(1))] if found else []
    return [n for n in names if n and n.lower() not in ("none", "-")][:MOST_ICONS]


def _icon_path(folder: Path, name: str) -> Path:
    return folder / f"icon-{hashlib.sha256(name.lower().encode()).hexdigest()[:12]}.png"


def kept(folder: Path, on_screen: str) -> list[tuple[Path, dict[str, Any]]]:
    """The icons drawn for this brief, with what is known about each. Never draws."""
    from pipeline.storage.documents import read_json_object

    found = []
    for path in (_icon_path(folder, name) for name in wanted(on_screen)):
        meta = read_json_object(path.with_suffix(".json"), "icon") if path.exists() else None
        if meta:
            found.append((path, meta))
    return found


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


def find_icons(folder: Path, names: list[str], colour: str,
               state: dict[str, Any]) -> list[Path]:
    """An icon for each name from the bundled set, in the scene's colour, kept with
    its credit; drawn in one browser."""
    from pipeline.scene_state import add_event

    todo = [n for n in names if not (_icon_path(folder, n).exists()
                                     and _icon_path(folder, n).with_suffix(".json").exists())]
    found = {name: _lucide(name) for name in todo}
    for name in todo:
        if found[name] is None:
            add_event(state, "note", f"No icon was found for \"{name}\".")
    ready = [(name, *found[name]) for name in todo if found[name] is not None]
    try:
        drawn = rasterise([svg for _, svg, _ in ready], colour) if ready else []
    except Exception as failure:          # no browser: the scene goes on without them
        add_event(state, "note", f"The icons could not be drawn ({failure}).")
        drawn = []
    for (name, _svg, meta), png in zip(ready, drawn, strict=False):
        _keep(folder, _icon_path(folder, name), png, meta | {"asked": name, "kind": "icon"})
    return [_icon_path(folder, n) for n in names if _icon_path(folder, n).exists()]


def find_icon(folder: Path, name: str, colour: str, state: dict[str, Any]) -> Path | None:
    found = find_icons(folder, [name], colour, state)
    return found[0] if found else None


def _keep(folder: Path, path: Path, data: bytes, meta: dict[str, Any]) -> None:
    """The icon, what is known about it beside it, and its licence and credit in the
    scene's sources.json (read by its checks and by Export's credits). Written whole:
    four scenes are made at once, and Export reads while they write."""
    from pipeline.storage.documents import write_text_atomically

    path.write_bytes(data)
    write_text_atomically(path.with_suffix(".json"),
                          json.dumps(meta, ensure_ascii=False, indent=1))
    record = folder / "sources.json"
    with _SOURCES_LOCK:
        try:
            entries = json.loads(record.read_text(encoding="utf-8")) if record.exists() else []
        except ValueError:
            entries = []
        entries = [e for e in entries if Path(e.get("file", "")).name != path.name]
        entries.append({"file": path.name, "title": meta.get("title", ""),
                        "source": meta.get("source", ""), "licence": meta.get("licence", ""),
                        "licence_url": meta.get("licence_url", ""),
                        "author": meta.get("author", ""), "page": meta.get("page", "")})
        write_text_atomically(record, json.dumps(entries, ensure_ascii=False, indent=1))
