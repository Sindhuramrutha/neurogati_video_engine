"""The video's look, planned before any scene is made: one direction per scene.

Made one by one, each scene's maker chose its own look -- or none: a test of three
Chapter 1 scenes had one with no background, one with a gradient so pale it read
as white, and one that, its deck picture gone, asked for "picture 0" twenty-three
times instead of having a picture painted. A video looks made when its looks are
planned together. Here a director plans each section's scenes -- with the video so
far in view -- and says for each: its style, its background (art to paint, or a
gradient and how it is split), the picture to paint (a subject, a character, a
visual metaphor, or one of the deck pictures a person chose), the layout and the
motion. Then it reviews its own plan against the bar and corrects it: variety from
scene to scene, about seven painted backgrounds in ten, light and pleasant and never
overdone, true to the science, every chosen picture shown.

Kept in `generation/art-direction.json`; each scene's brief carries its direction,
its background and picture are made from it before its first round, and its maker
follows it -- departing from it only for a reason it gives.
"""

from __future__ import annotations

import json
from typing import Any, Literal

from pydantic import BaseModel, Field

DIRECTION_FILE = "art-direction.json"
# The text model thinks before it answers, and that counts: 12000 ran out on six
# scenes. A section that still does not fit is planned in halves.
DIRECTION_TOKENS = 32000
BAR = (
    "The bar is a well-made explainer channel: flat illustrated characters and objects, "
    "a cute character for the brain, a visual metaphor (a seesaw for two forces, a key in "
    "a lock), collage (a halftone brain cut out on paper), a cosy illustrated room, label "
    "pills, a pastel painted scene whose detail sits at its edges round a calm centre, a "
    "clean cream screen with one bold word. Every background fills the whole screen, edge "
    "to edge -- never a picture framed inside it, never a border, mat or margin. Every "
    "frame light and pleasant, colours that suit each other, artistic and "
    "interesting to look at -- never dark or gloomy, never busy, garish or overdone.")


class SceneLook(BaseModel):
    scene: int = Field(description="The scene's number in the video, as listed.")
    style: str = Field(description="Its drawing style, in a phrase: 'flat cartoon, round "
                                   "shapes, warm palette', 'pastel watercolour', 'halftone "
                                   "collage on paper'.")
    picture: str = Field(description="The picture to paint, exactly: its subject alone, "
                                     "what it does, the angle, the kind ('two small frog "
                                     "hearts in beakers'); a character or a visual metaphor "
                                     "where it teaches best -- or 'chosen: <name>' for a "
                                     "deck picture a person chose. True to the science. "
                                     "Only the subject: it is cut out and stood on the "
                                     "background, so its setting -- a room, a landscape, a "
                                     "sky -- belongs to the background, never here.")
    background_kind: Literal["image", "gradient"]
    background: str = Field(description="image: the art to paint behind the scene, filling "
                                        "the whole screen edge to edge (never a frame, "
                                        "border or margin), light, its centre calm. "
                                        "gradient: what it should feel like.")
    colours: list[str] = Field(default_factory=list, description="gradient: 2 or 3 light "
                                                                 "hex colours that suit "
                                                                 "each other.")
    split: Literal["none", "left", "right", "top", "bottom", "diagonal"] = "none"
    layout: str = Field(description="Where things sit in the frame.")
    motion: str = Field(description="What moves, builds or is lit, on which words.")


class SectionLooks(BaseModel):
    scenes: list[SceneLook]
    changes: list[str] = Field(default_factory=list, description="Review only: what you "
                                                                 "changed and why.")


def read(project) -> dict[str, Any]:
    try:
        found = json.loads((project.root / "generation" / DIRECTION_FILE)
                           .read_text(encoding="utf-8"))
        return found if isinstance(found, dict) else {}
    except (OSError, ValueError):
        return {}


def for_scene(project, visual_id: str) -> dict[str, Any] | None:
    return read(project).get("scenes", {}).get(visual_id)


def direct(slug: str, *, again: bool = False) -> dict[str, Any]:
    """Plan the look of every scene not planned yet (all of them, `again`), section by
    section, each plan reviewed and corrected by the director itself."""
    from pipeline.chosen_pictures import chosen
    from pipeline.core import require_project
    from pipeline.generation import VisualPlanStore
    from pipeline.storage.documents import write_text_atomically

    project = require_project(slug)
    visuals = VisualPlanStore(project.root).load().visuals
    narrations = _narrations(project)
    picks = list(chosen(project).values())
    kept = {} if again else read(project).get("scenes", {})
    number = {visual.id: index for index, visual in enumerate(visuals, start=1)}
    sections: dict[str, list] = {}
    for visual in visuals:
        sections.setdefault(visual.section_id, []).append(visual)
    for section_visuals in sections.values():
        if all(v.id in kept for v in section_visuals):
            continue
        so_far = [f"scene {number[vid]}: {look['style']}; background {look['background_kind']}"
                  f" -- {look['background'][:60]}; picture {look['picture'][:60]}"
                  for vid, look in kept.items() if vid in number]
        looks = _plan_section(section_visuals, number, narrations, picks, so_far)
        by_number = {look.scene: look for look in looks}
        for visual in section_visuals:
            look = by_number.get(number[visual.id])
            if look is not None:
                kept[visual.id] = look.model_dump()
        path = project.root / "generation" / DIRECTION_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomically(path, json.dumps({"scenes": kept}, ensure_ascii=False, indent=1))
    return {"scenes": len(kept), "of": len(visuals)}


def _narrations(project) -> dict[str, str]:
    from pipeline.scripting import ScriptStore

    return {scene.id: scene.narration
            for section in ScriptStore(project.root).load().section_scripts
            for scene in section.scenes}


def _plan_section(visuals: list, number: dict[str, int], narrations: dict[str, str],
                  picks: list[str], so_far: list[str]) -> list[SceneLook]:
    """The section's looks, planned then reviewed. An answer cut short is planned again
    in halves; a review that fails keeps the first plan rather than none."""
    from pipeline.llm import ModelCallFailed, complete_structured

    scenes = "\n\n".join(
        f"Scene {number[v.id]}\nSaid: {narrations.get(v.scene_id, v.narration_preview)}\n"
        f"The script's idea for the screen: {v.brief[:700]}" for v in visuals)
    context = "\n".join([
        f"Section: {visuals[0].section_title}",
        "Deck pictures a person chose, each to be shown once in the video: "
        + (", ".join(picks) if picks else "none"),
        "The video so far (vary from it):\n" + ("\n".join(so_far[-24:]) or "nothing yet"),
    ])
    system = (
        "You are the art director of an educational explainer video. You plan how every "
        "scene looks so that the whole video is beautiful, varied and clear, and every "
        "picture teaches. " + BAR + " Plan each scene: one picture to paint that shows what "
        "is said (a subject, a character, a visual metaphor -- concrete, exact and true to "
        "the science), its style (styles may differ from scene to scene, but neighbours "
        "should sit well together), its background -- about seven scenes in ten get painted "
        "art filling the screen edge to edge (from a simple wash to a rich scene whose "
        "detail sits at its edges round a calm centre -- never a frame or border), the "
        "rest a light "
        "gradient, maybe split into a coloured section -- its layout and its motion on the "
        "words. Words on screen are optional. No two scenes look alike.")
    try:
        first = complete_structured(SectionLooks, system, f"{context}\n\n{scenes}",
                                    max_tokens=DIRECTION_TOKENS)
    except ModelCallFailed:
        if len(visuals) < 2:
            raise
        half = len(visuals) // 2
        return [*_plan_section(visuals[:half], number, narrations, picks, so_far),
                *_plan_section(visuals[half:], number, narrations, picks, so_far)]
    review = (
        f"{context}\n\n{scenes}\n\nYour plan for these scenes:\n"
        + json.dumps([look.model_dump() for look in first.scenes], ensure_ascii=False)
        + "\n\nReview it as a demanding director and return it corrected, the same scenes: "
          "is each picture concrete, accurate and the best way to show what is said? Is "
          "any scene dark, dull, busy or overdone? Do neighbouring scenes vary? Are about "
          "seven in ten backgrounds painted? Is any chosen picture left out that belongs "
          "here? Say what you changed.")
    try:
        reviewed = complete_structured(SectionLooks, system, review,
                                       max_tokens=DIRECTION_TOKENS)
    except ModelCallFailed:
        return first.scenes
    return reviewed.scenes or first.scenes


_LOCK = __import__("threading").Lock()


def ensure(project, visual_id: str) -> dict[str, Any] | None:
    """The scene's direction, the video's planned first if this scene has none --
    once: scenes starting together wait for the plan rather than each making one."""
    with _LOCK:
        if for_scene(project, visual_id) is None:
            direct(project.slug)
    return for_scene(project, visual_id)
