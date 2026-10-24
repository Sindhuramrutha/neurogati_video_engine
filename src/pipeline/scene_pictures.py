"""The pictures a scene is offered, and which of the deck's the video has shown.

A scene used to be offered only its own slide's pictures, after a vision verdict
had taken away every one that did not "teach", and its painted illustration came
first in the list the templates draw from. In Demo 001 that left 32 of 43 scenes
showing a painting and most of the deck's 35 pictures in no scene at all: a
video made from a deck that did not look made from it.

Now a scene is offered the deck's pictures, nearest first, each with where it
comes from, what it is, what was measured about it, and which other scenes show
it -- and the agent decides what to show and how:

1. the deck pictures its brief names (`PICTURE:`), the scene's main subject;
2. the pictures made for this scene (painted by the image model, icons);
3. the rest of its own slide's pictures, and the slide itself as the deck shows it;
4. its section's other pictures;
5. a few more from the slides nearest it.

The first three are the scene's own (`near`). Indexes into this list are what the
program and the shots use (`brief.assets.pictures`); `brief.picture_catalogue`
says what each one is. Only a picture a person left out on Assets & Design is
never offered.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pipeline.storage.documents import read_json_object

# The rest of the deck, nearest slides first. Every picture in the deck, offered to
# every scene, made the prompt long and pulled in pictures that had nothing to do
# with the scene.
MOST_FAR_PICTURES = 8
NAMED, OWN_SLIDE = "named in this scene's brief", "this scene's own slide"
SECTION, ELSEWHERE = "this section", "elsewhere in the deck"
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

    add(NAMED, [f for f in offered if _is_named(f, named_text)])
    add(OWN_SLIDE, sorted(
        (f for f in offered if _figure_slide(f, slide_of) in own_slides), key=nearness))
    add(SECTION, sorted((f for f in offered if f.asset_path in in_section), key=nearness))
    rest = sorted((f for f in offered if f.asset_path not in seen), key=nearness)
    add(ELSEWHERE, rest[:MOST_FAR_PICTURES])
    return tiers


def scene_number(project, visual) -> int:
    """Where the scene comes in the whole video, from 1."""
    from pipeline.generation import VisualPlanStore

    ids = [v.id for v in VisualPlanStore(project.root).load().visuals]
    return ids.index(visual.id) + 1 if visual.id in ids else 0


def _owner(shown: list[str], names_it: bool, this_scene: int) -> int:
    """The scene whose subject a picture is: the earliest that names it on its PICTURE
    line or shows it large -- this scene too, when it names it. 0 for none."""
    claims = [int(s.split(",")[0].split()[1]) for s in shown if not s.endswith(", small")]
    if names_it and this_scene:
        claims.append(this_scene)
    return min(claims, default=0)


def catalogue(project, tiers: list[tuple[str, Any]], made: list[tuple[str, Path, dict]],
              notes: dict[str, dict[str, str]], shown_in: dict[str, list[str]],
              slide_image: Path | None, this_scene: int = 0
              ) -> tuple[list[str], list[dict[str, Any]]]:
    """The scene's pictures as paths (what the program loads) and as a catalogue
    (what the agent reads), index for index: those its brief names, those made for
    it, its own slide's and the slide itself (all `near`), then the rest."""
    from pipeline.assets import FigureUse

    # A fragment cut out of a larger figure -- its words sliced at an edge -- is not
    # offered: on Chapter 1, "...uid sample" and half a pair of tweezers was a scene's
    # picture. One a person chose with "Use" stays.
    tiers = [(where, figure) for where, figure in tiers
             if figure.use == FigureUse.USE
             or not notes.get(str(project.root / figure.shown_path), {}).get("fragment")]

    def deck(where: str, figure) -> tuple:
        path = project.root / figure.shown_path
        note = notes.get(str(path), {})
        prepared = figure.shown_path == figure.prepared_path
        size = ((figure.prepared_width, figure.prepared_height) if prepared
                else (figure.width, figure.height))
        measured = " ".join(part for part in (
            figure.why_not_a_frame,
            "A person chose it on Assets & Design." if figure.use == FigureUse.USE else "",
        ) if part)
        slide = f" (slide {figure.slide_number})" if figure.slide_number else ""
        return (path, where + slide, note.get("what") or figure.caption or figure.name,
                note.get("role", "explains"), measured, size, where in (NAMED, OWN_SLIDE))

    ordered = [deck(w, f) for w, f in tiers if w == NAMED]
    ordered += [(path, where, meta.get("what", ""), meta.get("role", "explains"),
                 meta.get("measured", ""), None, True) for where, path, meta in made]
    ordered += [deck(w, f) for w, f in tiers if w == OWN_SLIDE]
    # The slide itself is not offered: a video's pictures are made for it, and the
    # deck's only as a person chose them (`chosen_pictures`).
    ordered += [deck(w, f) for w, f in tiers if w not in (NAMED, OWN_SLIDE)]

    entries = []
    for index, (path, where, what, role, measured, size, near) in enumerate(ordered):
        width, height = size or _size_of(path)
        shown = shown_in.get(str(path), [])
        owner = _owner(shown, where.startswith(NAMED), this_scene)
        entries.append({"index": index, "file": path.name, "from": where, "what": what,
                        "role": role, "size": f"{width}x{height}" if width else "",
                        "near": near, "shown_in": shown[:4]}
                       | ({"main_of": f"scene {owner}"} if owner and owner != this_scene
                          else {})
                       | ({"measured": measured} if measured else {}))
    return [str(item[0]) for item in ordered], entries


def _size_of(path: Path) -> tuple[int, int]:
    from PIL import Image

    try:
        with Image.open(path) as opened:
            return opened.width, opened.height
    except OSError:
        return 0, 0


# --- which deck pictures the video shows ----------------------------------------------------


MAIN_TEMPLATES = ("hero", "person", "opener", "key_idea")   # one picture, large


def _shown_indexes(folder: Path) -> set[int]:
    """The picture indexes a scene's program shows: from its shots, or read from a
    program written by hand."""
    return set(_shown_as(folder))


def _shown_as(folder: Path) -> dict[int, str]:
    """Each picture index a scene's program shows, and how: "main" (the one large
    picture of a hero, person, opener or key_idea shot) or "small"."""
    spec = read_json_object(folder / "spec.json", "scene spec") or {}
    found: dict[int, str] = {}

    def walk(value: Any, main: bool) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "picture" and isinstance(item, int):
                    if main or item not in found:
                        found[item] = "main" if main else "small"
                else:
                    walk(item, False)
        elif isinstance(value, list):
            for item in value:
                walk(item, main)

    if isinstance(spec.get("shots"), list) and spec["shots"]:
        for shot in spec["shots"]:
            if isinstance(shot, dict):
                walk(shot, shot.get("template") in MAIN_TEMPLATES)
        return found
    for name in ("scene.py", "scene.html", "scene.tsx"):
        program = folder / name
        if program.exists():
            text = program.read_text(encoding="utf-8", errors="replace")
            found.update({int(n): "small" for n in _PICTURE_REFERENCE.findall(text)})
    return found


def shown_pictures(project, skip_visual_id: str = "", planned: bool = True,
                   library=None) -> dict[str, list[str]]:
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

    library = library or (assets_for_later_stages(project).library if planned else None)
    figures = library.handed_on() if planned else []
    shown: dict[str, list[str]] = {}
    for number, visual in enumerate(VisualPlanStore(project.root).load().visuals, start=1):
        if visual.id == skip_visual_id:
            continue
        here: dict[str, str] = {}
        folder = scene_folder(project, visual)
        if folder is not None and (folder / "brief.json").exists():
            brief = read_json_object(folder / "brief.json", "brief") or {}
            pictures = (brief.get("assets") or {}).get("pictures") or brief.get("pictures") or []
            here = {_same_file(project, pictures[index]): how
                    for index, how in _shown_as(folder).items() if 0 <= index < len(pictures)}
        for path, how in here.items():
            shown.setdefault(path, []).append(
                f"scene {number}" + ("" if how == "main" else ", small"))
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


def deck_usage(project, library=None) -> dict[str, Any]:
    """Which of the deck's pictures the video shows, and which it does not."""
    from pipeline.plan_pictures import assets_for_later_stages

    library = library or assets_for_later_stages(project).library
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


# --- what is made for a scene before its first round ------------------------------------


def made_for_scene(folder: Path, on_screen: str, look: dict[str, Any]) -> list[tuple]:
    """The pictures made for this scene alone, as (where from, path, what is known):
    the one painted for its ILLUSTRATE (or PHOTO) line, and its ICONs. Never makes any."""
    from pipeline import icon_pictures, scene_illustration

    made: list[tuple] = []
    painted = scene_illustration.kept(folder, on_screen, look)
    if painted is not None:
        made.append(("painted for this scene", painted,
                     {"what": scene_illustration.wanted(on_screen), "role": "explains",
                      "measured": "Painted and checked: right subject, framed, no words."}))
    for asked in reversed(_asked_paintings(folder)):     # the newest first
        painted = scene_illustration.kept(folder, f"ILLUSTRATE: {asked}", look)
        if painted is not None:
            made.append(("painted for this scene, as its maker asked", painted,
                         {"what": asked, "role": "explains", "measured": "Painted and "
                          "checked: right subject, framed, no words."}))
    for path, meta in icon_pictures.kept(folder, on_screen):
        made.append((f"an icon for this scene: {meta.get('source', '')}", path,
                     {"what": meta.get("title") or meta.get("asked", ""), "role": "icon",
                      "measured": f"Asked for: {meta.get('asked', '')}."}))
    return made


ASKED_PAINTINGS = "paintings-asked.json"
MOST_ASKED = 3                  # pictures a scene's maker may have painted for it
PAINTED = ("A picture was painted for this scene, as you asked: it is in the catalogue now "
           "as this scene's own picture. Answer again, with it as the main picture -- or, "
           "if it is not right, ask for it again, saying what to change.")


def _asked_paintings(folder: Path) -> list[str]:
    try:
        found = json.loads((folder / ASKED_PAINTINGS).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [str(asked) for asked in found] if isinstance(found, list) else []


def paint_asked(project, visual, folder: Path, spec: dict[str, Any], brief: dict[str, Any],
                state: dict[str, Any]) -> dict[str, Any] | None:
    """The scene's maker owns its pictures: it may ask for one painted (its answer's
    "paint") -- one no offered picture shows, or a better version of one it judged
    wrong, saying what to change -- up to MOST_ASKED a scene. Each is painted and
    checked like any other, and the brief written again with it; one the maker no
    longer uses is simply not shown. Scenes about an idea with no picture (dualism)
    failed "It pictures the idea" in every round with nothing to show it with. None
    when nothing new was asked, too many were, or it could not be painted."""
    from pipeline import scene_illustration
    from pipeline.scene_lab import write_brief

    asked = str(spec.get("paint") or "").strip()[:300]
    before = _asked_paintings(folder)
    if not asked or asked in before or len(before) >= MOST_ASKED:
        return None
    (folder / ASKED_PAINTINGS).write_text(json.dumps([*before, asked], ensure_ascii=False),
                                          encoding="utf-8")
    painted = scene_illustration.paint(folder, f"ILLUSTRATE: {asked}", brief["look"], state,
                                       brief["narration"])
    return write_brief(project, visual) if painted is not None else None


def _directed(project, visual, folder: Path, brief: dict[str, Any],
              state: dict[str, Any]) -> dict[str, Any]:
    """The art director's plan made real before the first round: the scene's planned
    background, and its planned picture when the script asked none painted -- so a
    scene never depends on its maker remembering either."""
    from pipeline import art_direction, scene_backgrounds, scene_illustration

    direction = art_direction.ensure(project, visual.id)
    if not direction:
        return brief
    if not scene_backgrounds.read(folder):
        planned = {"kind": direction.get("background_kind"),
                   "describe": direction.get("background", ""),
                   "colours": direction.get("colours") or [],
                   "split": direction.get("split", "none")}
        brief = scene_backgrounds.choose(project, visual, folder, {"background": planned},
                                         brief, state) or brief
    picture = str(direction.get("picture") or "")
    painted = scene_illustration.wanted(brief["on_screen"])
    if picture and not picture.lower().startswith("chosen") and not painted:
        asked = f"{picture} -- in this style: {direction.get('style', '')}"
        brief = paint_asked(project, visual, folder, {"paint": asked}, brief, state) or brief
    return brief


def prepare(project, visual, brief: dict[str, Any], state: dict[str, Any],
            note: str = "") -> dict[str, Any]:
    """Make what the brief asks for that is not made yet -- the painting (from the
    image model, checked before it is used) and the icons (from the bundled set) --
    and return the brief written again with them in it. Each is made once and kept,
    so the rounds after it and a scene made again pay nothing more."""
    from pipeline import icon_pictures, scene_illustration
    from pipeline.scene_lab import write_brief
    from pipeline.scene_program import scene_folder

    folder = scene_folder(project, visual, create=True)
    brief = _directed(project, visual, folder, brief, state)
    on_screen, look, narration = brief["on_screen"], brief["look"], brief["narration"]
    painting, icons = scene_illustration.wanted(on_screen), icon_pictures.wanted(on_screen)
    if not painting and not icons:
        return brief
    if painting:
        scene_illustration.paint(folder, on_screen, look, state, narration, note)
    if icons:
        icon_pictures.find_icons(folder, icons, look.get("accent") or look.get("text")
                                 or "#1a1816", state)
    return write_brief(project, visual)
