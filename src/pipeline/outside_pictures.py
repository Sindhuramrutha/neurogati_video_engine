"""Pictures from outside the deck: found on the open web, or an icon -- only what may
be used commercially, each kept with its credit.

The deck comes first; these fill what it does not show. A scene's brief asks for
them on lines the script agent writes, scene by scene:

    PHOTO: Ivan Pavlov with a dog in his laboratory   -- a real photograph,
                                                        engraving or diagram to find
    ICON: microscope, brain, lightning                -- up to three simple icons

Where they come from:

- **Wikimedia Commons** and **Openverse** (which also searches Flickr and other
  open collections), keeping only public domain, CC0, CC BY and CC BY-SA -- never a
  licence with NC (non-commercial) or ND (no derivatives).
- **Iconify** (200,000+ open icons), keeping only sets under MIT, Apache 2.0, ISC,
  BSD, CC0, CC BY or CC BY-SA; and the **Lucide** set bundled in `resources/icons`
  (ISC), which needs no network.

A photo is looked at by the vision model before it is used: the best of a few
candidates for what was asked, or none. Asked as written, a brief's line ("Lewis
Carroll, portrait photograph, nineteenth century") found one wrong candidate, so
the search is also tried with the descriptive words taken off ("Lewis Carroll").
A photo that is not found is not painted instead: a painted "photograph" of a
real person, a place or an instrument is a fabrication. The scene goes on with
the deck's pictures, icons and what it draws. Each kept file sits in the scene's folder as
`found-<key>.png` or `icon-<key>.png`, with a `.json` beside it (what was asked,
the source, the licence, the author, the address) and an entry in the scene's
`sources.json`, which the scene's checks read and Export lists as credits.
"""

from __future__ import annotations

import hashlib
import io
import json
import logging
import re
import threading
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from pipeline.config import REPO_ROOT

logger = logging.getLogger(__name__)

PHOTO_LINE = re.compile(r"^\s*PHOTO\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
ICON_LINE = re.compile(r"^\s*ICONS?\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
USER_AGENT = ("explainer-video-pipeline/0.1 "
              "(https://github.com/shivam-kumar25/acedemic-explainer-video-pipeline)")
TIMEOUT_SECONDS = 30
CANDIDATES_LOOKED_AT = 5
MOST_ICONS = 3
SMALLEST_PHOTO_SIDE = 300
LONGEST_SIDE = 1600
ICON_PIXELS = 512
LUCIDE = REPO_ROOT / "resources" / "icons" / "lucide"
_SOURCES_LOCK = threading.Lock()

# Licences that allow use in a commercial video, with credit where they ask for it.
ICON_LICENCES = {"MIT", "Apache-2.0", "ISC", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0",
                 "Unlicense", "CC-BY-3.0", "CC-BY-4.0", "CC-BY-SA-3.0", "CC-BY-SA-4.0"}


def commercial_licence(name: str) -> bool:
    """Whether a picture under this licence may be used in a commercial video:
    public domain, CC0, CC BY or CC BY-SA -- never NC, never ND, never unknown."""
    text = re.sub(r"[\s_]+", "-", (name or "").strip().lower())
    if not text or "nc" in text.split("-") or "nd" in text.split("-") or "-nc" in text \
            or "-nd" in text or "noncommercial" in text or "noderiv" in text:
        return False
    return (text.startswith(("cc0", "pd", "public-domain", "cc-pd", "pdm"))
            or "public-domain" in text
            or bool(re.match(r"^(cc-)?by(-sa)?(-\d(\.\d)?)?$", text))
            or bool(re.match(r"^cc-by(-sa)?(-\d(\.\d)?)?", text)))


def wanted(on_screen: str) -> tuple[str, list[str]]:
    """What the brief asks to find: (a photo's description, icon names)."""
    photo = PHOTO_LINE.search(on_screen or "")
    icons = ICON_LINE.search(on_screen or "")
    asked = photo.group(1).strip() if photo else ""
    names = [n.strip() for n in re.split(r"[,;]| and ", icons.group(1))] if icons else []
    return ("" if asked.lower() in ("none", "-") else asked[:300],
            [n for n in names if n and n.lower() not in ("none", "-")][:MOST_ICONS])


def _key(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:12]


def kept(folder: Path, on_screen: str) -> list[tuple[Path, dict[str, Any]]]:
    """The pictures found for this brief, with what is known about each. Never searches."""
    photo, icons = wanted(on_screen)
    names = ([f"found-{_key(photo)}.png"] if photo else []) + \
        [f"icon-{_key(name.lower())}.png" for name in icons]
    found = []
    for name in names:
        path = folder / name
        meta = path.with_suffix(".json")
        if path.exists() and meta.exists():
            found.append((path, json.loads(meta.read_text(encoding="utf-8"))))
    return found


# --- searching -------------------------------------------------------------------------------


def _get(url: str, params: dict[str, Any] | None = None, as_json: bool = True):
    import httpx

    from pipeline.resilience import call

    def attempt():
        response = httpx.get(url, params=params, timeout=TIMEOUT_SECONDS,
                             headers={"User-Agent": USER_AGENT}, follow_redirects=True)
        response.raise_for_status()
        return response.json() if as_json else response.content

    return call("open-pictures", attempt, attempts=3, base_seconds=2, longest_wait=20,
                give_up_after=90)


def _plain(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()[:160]


def search_commons(query: str, limit: int = 8) -> list[dict[str, Any]]:
    """Wikimedia Commons files for `query` that may be used commercially."""
    data = _get("https://commons.wikimedia.org/w/api.php", {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{query} filetype:bitmap", "gsrlimit": limit, "prop": "imageinfo",
        "iiprop": "url|extmetadata|size|mime", "iiurlwidth": LONGEST_SIDE})
    found = []
    for page in sorted((data.get("query") or {}).get("pages", {}).values(),
                       key=lambda p: p.get("index", 0)):
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        licence = (meta.get("LicenseShortName") or {}).get("value", "")
        if not commercial_licence(licence) or info.get("mime") not in (
                "image/jpeg", "image/png", "image/gif", "image/webp"):
            continue
        if min(info.get("width", 0), info.get("height", 0)) < SMALLEST_PHOTO_SIDE:
            continue
        found.append({
            "source": "Wikimedia Commons", "title": page.get("title", "")[5:],
            "url": info.get("thumburl") or info.get("url", ""),
            "page": info.get("descriptionurl", ""), "licence": licence,
            "licence_url": (meta.get("LicenseUrl") or {}).get("value", ""),
            "author": _plain((meta.get("Artist") or {}).get("value", ""))
            or _plain((meta.get("Credit") or {}).get("value", "")) or "unknown",
        })
    return found


def search_openverse(query: str, limit: int = 8) -> list[dict[str, Any]]:
    """Openverse images for `query` under a licence that allows commercial use."""
    data = _get("https://api.openverse.org/v1/images/", {
        "q": query, "license_type": "commercial", "page_size": limit, "mature": "false"})
    found = []
    for result in data.get("results") or []:
        licence = f"{result.get('license', '')} {result.get('license_version', '')}".strip()
        if not commercial_licence(licence.replace(" ", "-")):
            continue
        if min(result.get("width") or 0, result.get("height") or 0) < SMALLEST_PHOTO_SIDE \
                and result.get("width"):
            continue
        found.append({
            "source": f"Openverse ({result.get('source', '')})",
            "title": (result.get("title") or "")[:120], "url": result.get("url", ""),
            "page": result.get("foreign_landing_url", ""),
            "licence": licence.upper() if licence.startswith(("cc0", "pdm"))
            else f"CC {licence.upper()}",
            "licence_url": result.get("license_url", ""),
            "author": (result.get("creator") or "unknown")[:120],
        })
    return found


def _picture_bytes(url: str) -> bytes | None:
    """A downloaded picture as PNG, its longest side at most LONGEST_SIDE; None if it
    is not a picture."""
    from PIL import Image

    try:
        raw = _get(url, as_json=False)
        with Image.open(io.BytesIO(raw)) as opened:
            image = opened.convert("RGBA") if opened.mode in ("P", "LA", "RGBA") \
                else opened.convert("RGB")
            image.thumbnail((LONGEST_SIDE, LONGEST_SIDE))
            out = io.BytesIO()
            image.save(out, format="PNG")
            return out.getvalue()
    except Exception as failure:          # one bad download is one candidate fewer
        logger.info("picture not downloaded (%s): %s", url, failure)
        return None


class Choice(BaseModel):
    best: int = Field(description="The number of the candidate that shows what was asked "
                                  "best, correctly for the science and the history; 0 when "
                                  "none of them does.")
    why: str = Field("", description="In one sentence, why.")


def _choose(asked: str, narration: str, candidates: list[tuple[dict, bytes]]) -> int:
    """Which candidate shows what was asked (1-based), or 0 for none."""
    from pipeline.llm import VISION_TOKENS, complete_structured_with_images
    from pipeline.scene_review import _jpeg

    pictures = [(f"Candidate {n}: {meta['title']}", _jpeg(io.BytesIO(data)))
                for n, (meta, data) in enumerate(candidates, start=1)]
    from pipeline.resilience import call

    choice = call("vision", lambda: complete_structured_with_images(
        Choice,
        "You pick pictures for a science lesson from open-licence search results. Be "
        "strict: the right person, species, organ, instrument or setup, and nothing "
        "misleading. A picture full of text, a logo, or one that only shares a word with "
        "what was asked is not it.",
        f"The lesson needs: {asked}\n\nWhat is said while it is on screen:\n"
        f"{narration[:1000]}", pictures, max_tokens=VISION_TOKENS),
        attempts=5, base_seconds=5, longest_wait=60, give_up_after=300)
    return choice.best if 0 <= choice.best <= len(candidates) else 0


DESCRIPTIVE = {"photo", "photograph", "photographs", "portrait", "portraits", "picture",
               "image", "engraving", "drawing", "illustration", "diagram", "historical",
               "historic", "century", "nineteenth", "eighteenth", "seventeenth",
               "twentieth", "sixteenth", "black", "white", "old", "a", "an", "the", "of",
               "in", "with", "showing", "early", "original"}


def queries(asked: str) -> list[str]:
    """What to search for, most specific first: as asked, without its descriptive
    words, and its first few words."""
    words = re.findall(r"[A-Za-z0-9'-]+", asked)
    plain = " ".join(words)
    core = [w for w in words if w.lower() not in DESCRIPTIVE and not re.fullmatch(r"\d{4}s?", w)]
    found = [plain, " ".join(core), " ".join(core[:3])]
    return [q for i, q in enumerate(found) if q and q not in found[:i]]


def find_photo(folder: Path, asked: str, narration: str,
               state: dict[str, Any]) -> Path | None:
    """A photograph, engraving or diagram for `asked` from the open web, checked by
    the vision model and kept with its credit; None when nothing found is right."""
    from pipeline.llm import ModelCallFailed, ModelNotConfigured
    from pipeline.resilience import ServiceUnavailable
    from pipeline.scene_state import add_event

    path = folder / f"found-{_key(asked)}.png"
    if path.exists() and path.with_suffix(".json").exists():
        return path
    results: list[dict[str, Any]] = []
    for query in queries(asked):
        try:
            results += search_commons(query) + search_openverse(query)
        except (ServiceUnavailable, Exception) as failure:   # offline: no photo, said
            add_event(state, "note", f"Could not search the open web for \"{query}\" "
                      f"({failure}).")
        if len(results) >= 2 * CANDIDATES_LOOKED_AT:
            break
    seen, candidates = set(), []
    for result in results:
        # Openverse also searches Commons: the same file, found twice.
        same = re.sub(r"^file:|\.(jpe?g|png|gif|webp|tiff?)$", "", result["title"].lower()).strip()
        if result["url"] in seen or same in seen:
            continue
        seen.update({result["url"], same})
        data = _picture_bytes(result["url"])
        if data:
            candidates.append((result, data))
        if len(candidates) >= CANDIDATES_LOOKED_AT:
            break
    if not candidates:
        add_event(state, "note", f"Nothing open-licensed was found for \"{asked}\".")
        return None
    state["calls"]["vision"] = state["calls"].get("vision", 0) + 1
    try:
        best = _choose(asked, narration, candidates)
    except (ModelCallFailed, ModelNotConfigured, ServiceUnavailable) as failure:
        add_event(state, "note", f"The found pictures could not be looked at ({failure}).")
        return None
    if not best:
        add_event(state, "note", f"None of the {len(candidates)} pictures found for "
                  f"\"{asked}\" shows it.")
        return None
    meta, data = candidates[best - 1]
    path.write_bytes(data)
    record = meta | {"asked": asked, "kind": "photo"}
    path.with_suffix(".json").write_text(json.dumps(record, ensure_ascii=False, indent=1),
                                         encoding="utf-8")
    _record_source(folder, path, record)
    add_event(state, "note", f"Found a picture for \"{asked}\": {meta['title']} "
              f"({meta['source']}, {meta['licence']}, by {meta['author']}).")
    return path


# --- icons -----------------------------------------------------------------------------------


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


def rasterise(svg: str, colour: str, pixels: int = ICON_PIXELS) -> bytes:
    """An SVG icon as a transparent PNG in `colour`, drawn by the browser the web
    renderer already uses (Chromium, through Playwright)."""
    from playwright.sync_api import sync_playwright

    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.DOTALL).replace("currentColor", colour)
    svg = re.sub(r'\swidth="[^"]*"', "", svg, count=1)
    svg = re.sub(r'\sheight="[^"]*"', "", svg, count=1)
    svg = svg.replace("<svg", f'<svg width="{pixels}" height="{pixels}"', 1)
    page_html = ("<html><body style='margin:0;background:transparent'>"
                 f"<div id='icon' style='width:{pixels}px;height:{pixels}px'>{svg}</div>"
                 "</body></html>")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": pixels, "height": pixels})
            page.set_content(page_html)
            return page.locator("#icon").screenshot(omit_background=True)
        finally:
            browser.close()


def find_icon(folder: Path, name: str, colour: str, state: dict[str, Any]) -> Path | None:
    """An icon for `name`, from Iconify or else the bundled set, in the scene's
    colour, kept with its credit."""
    from pipeline.scene_state import add_event

    path = folder / f"icon-{_key(name.lower())}.png"
    if path.exists() and path.with_suffix(".json").exists():
        return path
    found = None
    try:
        found = _iconify(name)
    except Exception as failure:          # offline: the bundled set
        logger.info("Iconify not reached for %s: %s", name, failure)
    found = found or _lucide(name)
    if found is None:
        add_event(state, "note", f"No icon was found for \"{name}\".")
        return None
    svg, meta = found
    try:
        path.write_bytes(rasterise(svg, colour))
    except Exception as failure:          # no browser: the scene goes on without it
        add_event(state, "note", f"The icon for \"{name}\" could not be drawn ({failure}).")
        return None
    record = meta | {"asked": name, "kind": "icon"}
    path.with_suffix(".json").write_text(json.dumps(record, ensure_ascii=False, indent=1),
                                         encoding="utf-8")
    _record_source(folder, path, record)
    return path


# --- what the scene keeps --------------------------------------------------------------------


def _record_source(folder: Path, path: Path, meta: dict[str, Any]) -> None:
    """The file's licence and credit in the scene's sources.json (read by its checks
    and by Export's credits)."""
    record = folder / "sources.json"
    with _SOURCES_LOCK:
        entries = json.loads(record.read_text(encoding="utf-8")) if record.exists() else []
        entries = [e for e in entries if Path(e.get("file", "")).name != path.name]
        entries.append({"file": path.name, "title": meta.get("title", ""),
                        "source": meta.get("source", ""), "licence": meta.get("licence", ""),
                        "licence_url": meta.get("licence_url", ""),
                        "author": meta.get("author", ""), "page": meta.get("page", "")})
        record.write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")


def gather(folder: Path, on_screen: str, narration: str, look: dict[str, Any],
           state: dict[str, Any]) -> list[str]:
    """Find what the brief asks for that is not found yet. Returns what could not
    be found (said in the scene's record; never painted in its place)."""
    photo, icons = wanted(on_screen)
    missed = []
    if photo and find_photo(folder, photo, narration, state) is None:
        missed.append(photo)
    colour = look.get("accent") or look.get("text") or "#1a1816"
    for name in icons:
        find_icon(folder, name, colour, state)
    return missed


def credits(project) -> list[dict[str, Any]]:
    """Every outside picture any scene keeps, with its credit, for Export."""
    from pipeline.generation import VisualPlanStore
    from pipeline.scene_program import scene_folder

    found: dict[str, dict[str, Any]] = {}
    for visual in VisualPlanStore(project.root).load().visuals:
        folder = scene_folder(project, visual)
        record = folder / "sources.json" if folder else None
        if record is None or not record.exists():
            continue
        try:
            entries = json.loads(record.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for entry in entries:
            key = entry.get("page") or entry.get("title") or entry.get("file", "")
            found.setdefault(key, entry)
    return list(found.values())
