"""The pictures a scene is offered, and which of the deck's the video has shown.

A scene used to be offered only its own slide's pictures, after a vision verdict
had taken away every one that did not "teach", and its painted illustration came
first in the list the templates draw from. In Demo 001 that left 32 of 43 scenes
showing a painting and most of the deck's 35 pictures in no scene at all: a
video made from a deck that did not look made from it.

Now a scene is offered every deck picture, nearest first, each with where it
comes from, what it is, what was measured about it, and whether any scene shows
it yet -- and the agent decides what to show and how:

1. the deck pictures its brief names (`PICTURE:`), the scene's main subject;
2. the pictures made for this scene (painted, found on the open web, icons);
3. the rest of its own slide's pictures, and the slide itself as the deck shows it;
4. its section's other pictures;
5. every other picture in the deck.

Indexes into this list are what the program and the shots use
(`brief.assets.pictures`); `brief.picture_catalogue` says what each one is.
Only a picture a person left out on Assets & Design is never offered.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pipeline.storage.documents import read_json_object

MOST_DECK_PICTURES = 40           # the rest of the deck, nearest slides first
SLIDE_ITSELF = "the slide itself, as the deck shows it"
_PICTURE_REFERENCE = re.compile(r"(?:pictures|\bP)\s*\[\s*(\d+)\s*\]")


def _figure_slide(figure, slide_of: dict[str, int]) -> int:
    return figure.slide_number or slide_of.get(figure.block_id, 0)


def _named(on_screen: str) -> str:
    found = re.search(r"^\s*PICTURES?\s*:\s*(.+)$", on_screen or "", re.MULTILINE | re.IGNORECASE)
    text = found.group(1).strip() if found else ""
    return "" if text.lower() in ("none", "-") else text.lower()


def _is_named(figure, named: str) -> bool:
    """Whether the brief's PICTURE line names this deck picture: by its name
    ("Slide 3 · Heart or Brain"), its caption, or its file."""
    if not named:
        return False
    candidates = [figure.name, figure.caption, Path(figure.asset_path).name]
    return any(c and c.lower() in named for c in candidates if len(c or "") >= 6)


def deck_tiers(project, visual, section, plan, library, on_screen: str,
               narration: str) -> list[tuple[str, Any]]:
    """(where it comes from, figure) for every deck picture a scene is offered, in
    the order above (made-for-the-scene pictures are added by `write_brief`)."""
    from pipeline.extraction import ExtractionStore
    from pipeline.figure_prep import FigureFlag
    from pipeline.plan_pictures import by_rule, pictures_of

    offered = [f for f in library.handed_on()
               if FigureFlag.UNREADABLE not in f.flags
               and (project.root / f.shown_path).exists()]
    if not offered:
        return []
    slide_of = {block.id: block.slide_number
                for document in ExtractionStore(project.root).load().documents
                for block in document.blocks}
    planned = next((s for s in (section.scenes if section else [])
                    if s.id == visual.scene_id), None)
    own_slides = set(planned.slides) if planned and planned.slides else (
        {visual.slide_number} if visual.slide_number else set())
    in_section = [f.asset_path for f in pictures_of(section, plan, library)] if section else []
    # A picture a person detached from this section is not offered back to it.
    detached = (set(by_rule(section, library)) - set(in_section)
                if section and section.pictures_chosen else set())
    said = set(re.findall(r"[a-z]{4,}", (narration or "").lower()))

    def nearness(figure) -> tuple:
        slide = _figure_slide(figure, slide_of)
        distance = min((abs(slide - s) for s in own_slides), default=0) if slide else 99
        overlap = len(said & set(re.findall(r"[a-z]{4,}", figure.caption.lower())))
        return (distance, -overlap)

    named_text = _named(on_screen)
    tiers: list[tuple[str, Any]] = []
    seen: set[str] = set()

    def add(where: str, figures) -> None:
        for figure in figures:
            if figure.asset_path not in seen and figure.asset_path not in detached:
                seen.add(figure.asset_path)
                tiers.append((where, figure))

    add("named in this scene's brief", [f for f in offered if _is_named(f, named_text)])
    add("this scene's own slide", sorted(
        (f for f in offered if _figure_slide(f, slide_of) in own_slides), key=nearness))
    add("this section", sorted(
        (f for f in offered if f.asset_path in in_section), key=nearness))
    rest = sorted((f for f in offered if f.asset_path not in seen), key=nearness)
    add("elsewhere in the deck", rest[:MOST_DECK_PICTURES])
    return tiers


def catalogue(project, tiers: list[tuple[str, Any]], made: list[tuple[str, Path, dict]],
              notes: dict[str, dict[str, str]], shown_in: dict[str, list[str]],
              slide_image: Path | None) -> tuple[list[str], list[dict[str, Any]]]:
    """The scene's pictures as paths (what the program loads) and as a catalogue
    (what the agent reads), index for index."""
    from PIL import Image

    paths: list[str] = []
    entries: list[dict[str, Any]] = []

    def size_of(path: Path) -> str:
        try:
            with Image.open(path) as opened:
                return f"{opened.width}x{opened.height}"
        except OSError:
            return ""

    def entry(path: Path, where: str, what: str, role: str, measured: str = "") -> None:
        key = str(path)
        record = {"index": len(paths), "file": path.name, "from": where,
                  "what": what, "role": role, "size": size_of(path)}
        if measured:
            record["measured"] = measured
        shown = [scene for scene in shown_in.get(key, [])]
        record["shown_in_video"] = (", ".join(shown[:4]) + (" ..." if len(shown) > 4 else "")
                                    if shown else "not yet -- no scene shows it")
        paths.append(key)
        entries.append(record)

    named = [(w, f) for w, f in tiers if w == "named in this scene's brief"]
    others = [(w, f) for w, f in tiers if w != "named in this scene's brief"]

    def deck(where: str, figure) -> None:
        path = project.root / figure.shown_path
        note = notes.get(str(path), {})
        from pipeline.assets import FigureUse
        measured = " ".join(part for part in (
            figure.why_not_a_frame,
            "A person chose it on Assets & Design." if figure.use == FigureUse.USE else "",
        ) if part)
        slide = f"slide {figure.slide_number}" if figure.slide_number else ""
        entry(path, f"{where} ({slide})" if slide else where,
              note.get("what") or figure.caption or figure.name,
              note.get("role", "explains"), measured)

    for where, figure in named:
        deck(where, figure)
    for where, path, meta in made:
        entry(path, where, meta.get("what", ""), meta.get("role", "explains"),
              meta.get("measured", ""))
    own = [(w, f) for w, f in others if w == "this scene's own slide"]
    for where, figure in own:
        deck(where, figure)
    if slide_image is not None and slide_image.exists():
        entry(slide_image, SLIDE_ITSELF,
              "the whole slide: its title, words and pictures as the deck lays them out",
              "slide",
              "Words are in it: show it briefly (opening its topic, or a recap), never "
              "to explain on, and never with labels laid over it.")
    for where, figure in others:
        if where != "this scene's own slide":
            deck(where, figure)
    return paths, entries


# --- which deck pictures the video shows ----------------------------------------------------


def _shown_indexes(folder: Path) -> set[int]:
    """The picture indexes a scene's program shows: from its shots, or read from a
    program written by hand."""
    spec = read_json_object(folder / "spec.json", "scene spec") or {}
    found: set[int] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "picture" and isinstance(item, int):
                    found.add(item)
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    if isinstance(spec.get("shots"), list) and spec["shots"]:
        walk(spec["shots"])
        return found
    for name in ("scene.py", "scene.html", "scene.tsx"):
        program = folder / name
        if program.exists():
            text = program.read_text(encoding="utf-8", errors="replace")
            found |= {int(n) for n in _PICTURE_REFERENCE.findall(text)}
    return found


def shown_pictures(project, skip_visual_id: str = "",
                   planned: bool = True) -> dict[str, list[str]]:
    """Every picture some scene's program shows, by path: the scenes that show it
    ("scene 7"). Read from each scene's own folder -- its brief's pictures and the
    indexes its program uses.

    With `planned`, also the deck pictures each other scene's script names on its
    PICTURE line ("scene 2, planned"): scenes are made four at a time, and three
    scenes of one section, each seeing a picture "not yet shown" by the others,
    all made the same picture their subject."""
    from pipeline.generation import VisualPlanStore
    from pipeline.plan_pictures import assets_for_later_stages
    from pipeline.scene_program import scene_folder

    figures = assets_for_later_stages(project).library.handed_on() if planned else []
    shown: dict[str, list[str]] = {}
    for number, visual in enumerate(VisualPlanStore(project.root).load().visuals, start=1):
        if visual.id == skip_visual_id:
            continue
        here: set[str] = set()
        folder = scene_folder(project, visual)
        if folder is not None and (folder / "brief.json").exists():
            brief = read_json_object(folder / "brief.json", "brief") or {}
            pictures = (brief.get("assets") or {}).get("pictures") or brief.get("pictures") or []
            here |= {_same_file(project, pictures[index]) for index in _shown_indexes(folder)
                     if 0 <= index < len(pictures)}
        for path in here:
            shown.setdefault(path, []).append(f"scene {number}")
        named = _named(visual.brief)
        for figure in figures:
            path = str(project.root / figure.shown_path)
            if path not in here and _is_named(figure, named):
                shown.setdefault(path, []).append(f"scene {number}, planned")
    return shown


def _same_file(project, path: str) -> str:
    """A picture's path as this machine has it: a project moved since a brief was
    written still names its pictures by where they were."""
    marker = "/extraction/assets/" if "/extraction/assets/" in path.replace("\\", "/") \
        else "/assets/prepared/"
    normal = path.replace("\\", "/")
    if marker in normal:
        return str(project.root / normal[normal.index(marker) + 1:])
    return path


def deck_usage(project) -> dict[str, Any]:
    """Which of the deck's pictures the video shows, and which it does not."""
    from pipeline.plan_pictures import assets_for_later_stages

    library = assets_for_later_stages(project).library
    shown = shown_pictures(project, planned=False)
    pictures = []
    for figure in library.handed_on():
        path = str(project.root / figure.shown_path)
        scenes = shown.get(path) or shown.get(str(project.root / figure.asset_path)) or []
        pictures.append({"path": figure.shown_path, "name": figure.name,
                         "slide_number": figure.slide_number, "shown_in": scenes})
    used = [p for p in pictures if p["shown_in"]]
    return {"deck_pictures": len(pictures), "shown": len(used),
            "not_shown": [p for p in pictures if not p["shown_in"]], "pictures": pictures}


def write_usage(project) -> dict[str, Any]:
    """The usage, kept beside the scenes for the page and the report."""
    from pipeline.storage.documents import write_text_atomically

    usage = deck_usage(project)
    write_text_atomically(project.root / "generation" / "deck-pictures.json",
                          json.dumps(usage, indent=1, ensure_ascii=False))
    return usage


# --- what is made for a scene before its first round ------------------------------------


def made_for_scene(folder: Path, on_screen: str, look: dict[str, Any]) -> list[tuple]:
    """The pictures made for this scene alone, as (where from, path, what is known):
    painted for its ILLUSTRATE line, found for its PHOTO line (or painted in its
    place when nothing found was right), and its ICONs. Never makes any."""
    from pipeline import outside_pictures, scene_illustration

    made: list[tuple] = []
    painted = scene_illustration.kept(folder, on_screen, look)
    if painted is not None:
        made.append(("painted for this scene", painted,
                     {"what": scene_illustration.wanted(on_screen), "role": "explains",
                      "measured": "Painted from the brief: no words in it."}))
    for path, meta in outside_pictures.kept(folder, on_screen):
        kind = meta.get("kind")
        made.append((f"{'found' if kind == 'photo' else 'icon'} for this scene: "
                     f"{meta.get('source', '')}, {meta.get('licence', '')}", path,
                     {"what": meta.get("title") or meta.get("asked", ""),
                      "role": "explains" if kind == "photo" else "icon",
                      "measured": f"Asked for: {meta.get('asked', '')}. Credited on Export."}))
    return made


def prepare(project, visual, brief: dict[str, Any], state: dict[str, Any],
            note: str = "") -> dict[str, Any]:
    """Make what the brief asks for that is not made yet -- the painting, the photo
    found on the open web, the icons -- and return the brief written again with
    them in it. A photo that is not found is not painted in its place: a painted
    photograph of a real person or thing is a fabrication. Each is made once and
    kept, so the rounds after it and a scene made again pay nothing more."""
    from pipeline import outside_pictures, scene_illustration
    from pipeline.scene_lab import write_brief
    from pipeline.scene_program import scene_folder

    folder = scene_folder(project, visual, create=True)
    on_screen, look, narration = brief["on_screen"], brief["look"], brief["narration"]
    asked = False
    if scene_illustration.wanted(on_screen):
        asked = True
        scene_illustration.paint(folder, on_screen, look, state, narration, note)
    photo, icons = outside_pictures.wanted(on_screen)
    if photo or icons:
        asked = True
        outside_pictures.gather(folder, on_screen, narration, look, state)
    return write_brief(project, visual) if asked else brief
