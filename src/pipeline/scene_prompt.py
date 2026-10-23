"""What the scene-making model is told: the system prompt, the kits' API, the
answer format, and each round's request (`scene_maker` runs the rounds).

The brief is compacted for it, the scenes just before are summarised in a line
each so it stays consistent with them, and the scene's nearest pictures are
described part by part once by the vision model and kept; every other picture
it is offered is listed in the brief's picture catalogue.
"""

from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path
from typing import Any

from pipeline.generation import VisualPlanStore
from pipeline.scene_lab import scene_folder
from pipeline.scene_program import ENTRY_FILES

EARLIER_SCENES = 3
PICTURES_DESCRIBED = 3
KITS = {
    "manim": "manim -- scene.py starting `from manimkit import *` (every Manim name and the "
             "kit: ExplainerScene, self.label, self.when, self.until, self.finish, "
             "self.picture, self.boxed, self.connect, self.row/column, and the laid-out "
             "diagrams self.flow / self.hub / self.timeline, run). Diagrams, flows, "
             "transformations, camera moves.",
    "matplotlib": "matplotlib -- scene.py with scenekit (load_brief, VideoWriter). Charts "
                  "from numbers that are in the narration or source.",
    "pillow": "pillow -- scene.py with scenekit. Simple frame-by-frame drawing.",
    "web": "web -- scene.html animated with GSAP / D3 / three.js / anime.js through "
           "webkit.js (see web-scenes.md). Rich motion, charts, 3D.",
    "revideo": "revideo -- scene.tsx, a Motion Canvas / Revideo scene (see revideo-scenes.md). "
               "Polished explainer motion in TypeScript.",
}
# Placing boxes by hand coordinates is what failed most: boxes laid over boxes,
# circles drawn through their own labels, a diagram crammed into the top third.
LAYOUT_RULES = (
    "Shots: in Manim, start from a template -- self.hero (a picture and its parts named), "
    "self.steps (an experiment or process, 2-4 steps), self.compare (two sides), "
    "self.person (a portrait, a name, what they did), self.key_idea (one idea to remember), "
    "or self.flow / self.hub / self.timeline. A template lays out, times and moves the "
    "whole scene and passes the checks by construction: fill its slots from the brief and "
    "give each part the narration words it arrives on. Write the layout by hand only when "
    "no template fits, and say why in the json block's \"approach\". "
    "Labels: a label names something, so it sits beside that thing -- on a picture, "
    "self.callout(text, (x, y), side) -- never across the frame from it, and no arrow "
    "ever starts inside a label. "
    "Layout: in Manim, build the diagram with self.flow (steps joined by arrows), "
    "self.hub (one idea and what hangs off it) or self.timeline (things in order) "
    "when one of them fits -- they are laid out so nothing overlaps, crosses words or "
    "leaves the frame, and they fill the frame. Reveal their parts on the words. Place "
    "by hand only what they cannot express, and then: no outline crosses another "
    "outline or any words (a label goes beside a circle, or inside it with room to "
    "spare), and the diagram uses most of the frame, not one strip of it.")


PICTURE_RULES = (
    "Pictures: brief.picture_catalogue lists what you may show, by index -- where each "
    "comes from, what it is, its role (explains, sets_scene, furniture, slide, icon), "
    "what was measured about it, and which other scenes show it (shown_in). Your "
    "instructions say how to use them. A scene with pictures of its own (near: true) "
    "shows one.")


def available_renderers() -> list[str]:
    """The renderers a scene may use: every one wired here whose software this
    machine has (the web libraries; Node and Revideo)."""
    from pipeline import scene_revideo, scene_web
    from pipeline.scene_checks import RENDERERS

    installed = {"web": scene_web.is_installed(), "revideo": scene_revideo.is_installed()}
    return [name for name in RENDERERS if name in ENTRY_FILES and installed.get(name, True)]


def kit_api(renderers: list[str]) -> str:
    """The kits' own API, as it is in the code: what exists, with its signature. A
    model told only that a kit exists guesses at it (`self.assets`, `bold=`) and crashes."""
    from pipeline.scene_lab import resources_root

    code = resources_root() / "code"
    parts = []
    if "manim" in renderers:
        parts.append("### manimkit (Manim)\n" + _python_api(code / "manimkit.py"))
    if {"matplotlib", "pillow"} & set(renderers):
        parts.append("### scenekit (matplotlib / pillow)\n" + _python_api(code / "scenekit.py"))
    if "web" in renderers:
        header = (code / "webkit.js").read_text(encoding="utf-8")
        parts.append("### webkit.js (web)\n" + header[:header.index("(function")].strip())
    parts.append(
        "### Using a picture\n"
        "manim: self.picture(self.brief.assets.pictures[0], height=3.0, at=(x, y)) -- "
        "never a made-up file path. web: kit.picture(kit.pictures[0], {x, y, height}). "
        "revideo: <Img src={pictures[0]} />. The index (0 here) is the picture_catalogue's.\n"
        "A picture named illustration-*.png was painted for this scene and icon-*.png is "
        "an icon: neither has words "
        "in it. Whatever the main picture is, teach on top of it: every label a callout "
        "beside the part it names (manim: self.callout(text, (x, y), side)), a highlight "
        "or zoom on what is being said. Never cover it with boxes; never draw an arrow "
        "out of a label.")
    return "\n\n".join(parts)


def _python_api(path: Path) -> str:
    """A module's docstring and the public signatures in it, one line each."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    lines = [(ast.get_docstring(tree) or "").strip(), ""]

    def signature(node, indent=""):
        arguments = ast.unparse(node.args).replace("self, ", "").replace("self", "")
        note = (ast.get_docstring(node) or "").split("\n")[0]
        return f"{indent}{node.name}({arguments})" + (f" -- {note}" if note else "")

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            lines.append(f"class {node.name}  {(ast.get_docstring(node) or '').split(chr(10))[0]}")
            lines += [signature(item, "  .") for item in node.body
                      if isinstance(item, ast.FunctionDef) and not item.name.startswith("_")]
        elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            lines.append(signature(node))
    return "\n".join(lines)


def has_latex() -> bool:
    """Whether a TeX distribution is on PATH: Manim's `MathTex` needs one and reads as
    plain text without it, while a web page or Revideo typesets in the page."""
    return bool(shutil.which("latex") or shutil.which("xelatex") or shutil.which("pdflatex"))


def system_prompt(project, renderers: list[str]) -> str:
    from pipeline.agent_runtime import resolve_agent
    from pipeline.scene_author import _library_for_agent
    from pipeline.stages import Stage

    return (
        f"{resolve_agent(project, Stage.GENERATION).body.strip()}\n\n---\n"
        "You make ONE scene of an educational explainer video, as a program. You are "
        "asked in rounds: the first time you write the scene; after that you are shown "
        "what was rendered -- the checks that failed, what a reviewer saw in its "
        "frames -- and you fix it. A scene is done when every check passes and the "
        "reviewer says it is good. Never ask a question: where the brief is silent, "
        "decide, and say what you assumed in the json block's \"assumed\" list.\n\n"
        "It must TEACH the spoken idea in beats that land on the words that explain "
        "them (word timings are in the brief). It is NOT a slide: a few words per label, "
        "never the narration or a paragraph on screen. Everything on screen comes from "
        "the narration, the on-screen brief or the source text -- add no fact, number or "
        "label.\n\n" + PICTURE_RULES + "\n\nText is large (36 px lines at 1080p or "
        "more), inside the frame, never overlapping, never crossed by a shape. The clip "
        "lasts exactly brief.seconds. Keep the file short and direct.\n\n"
        + LAYOUT_RULES + "\n\n"
        "Renderers (pick what explains best):\n"
        + "\n".join(f"- {KITS[name]}" for name in renderers if name in KITS)
        + f"\nLaTeX is {'installed' if has_latex() else 'NOT installed: no MathTex or Tex'}."
        + f"\n\n## The kits' API (these are the only helpers that exist)\n{kit_api(renderers)}"
        + f"\n\n{_library_for_agent(renderers)}"
    )


def answer_format(renderers: list[str]) -> str:
    from pipeline.scene_shots import GUIDE

    return (
        "## How to answer\n"
        "Plain text with fenced blocks, nothing else. Answer with SHOTS whenever the idea "
        "fits them -- most scenes do; the program is then written for you and passes the "
        "layout checks by construction:\n"
        "```json\n{\"approach\": \"one sentence\", \"assumed\": [], \"shots\": [{\"template\": "
        "\"hero\", \"title\": \"Galvani's frog\", \"picture\": 0, \"when\": \"a dead frog\", "
        "\"callouts\": [{\"label\": \"Frog's leg\", \"at\": [0.55, 0.40], \"when\": \"leg "
        "kicked\"}]}]}\n```\n" + GUIDE + "\n\n"
        "Only when no shot can show the idea: a ```json block {\"renderer\": \""
        + "|".join(renderers) + "\", \"approach\": \"one sentence, and why no shot fits\", "
        "\"beats\": [{\"when_said\": \"exact narration words\", \"shows\": \"what appears\"}], "
        "\"assumed\": []}, then EITHER the complete file in a fenced block, OR an ```edit "
        "block for a few lines -- each edit is:\n"
        "<<<<<<< SEARCH\nthe lines exactly as they are now\n=======\nthe new lines\n"
        ">>>>>>> REPLACE\n"
        "A SEARCH must match one place in the file exactly (indentation included).")


def compact(brief: dict[str, Any]) -> dict[str, Any]:
    """The brief as the model reads it: word timings as one short line, not a list of
    objects, so the request stays small. The program reads brief.json in full."""
    # `pictures` and `assets.pictures` are paths the program loads; the model
    # reads them as the catalogue, by index.
    shown = {k: v for k, v in brief.items() if k not in ("words", "pictures", "assets")}
    shown["assets"] = {"pictures": f"{len(brief.get('pictures') or [])} pictures, by index: "
                                   "see picture_catalogue"}
    shown["word_starts"] = " ".join(f"{w['text']}@{w['start_ms'] / 1000:.2f}"
                                    for w in brief.get("words", []))
    shown["look"] = {k: v for k, v in brief.get("look", {}).items()
                     if k in ("background", "panel", "accent", "accents", "text", "dim")}
    return shown


def earlier_scenes(project, visual) -> str:
    """One line for each of the last few scenes of the video: what they did."""
    from pipeline.storage.documents import read_json_object

    visuals = VisualPlanStore(project.root).load().visuals
    at = next((i for i, v in enumerate(visuals) if v.id == visual.id), 0)
    lines = []
    for other in visuals[max(0, at - EARLIER_SCENES):at]:
        folder = scene_folder(project, other)
        spec = read_json_object(folder / "spec.json", "scene spec") if folder else None
        if spec and spec.get("approach"):
            lines.append(f"- {other.section_title}, scene {other.scene_number} "
                         f"({spec.get('renderer', '?')}): {spec['approach']}")
    return "\n".join(lines)


def picture_notes(brief: dict[str, Any], cache_folder: Path,
                  state: dict[str, Any]) -> tuple[str, dict[int, list]]:
    """The scene's nearest pictures -- the ones its brief names, the ones made for
    it, its own slide's -- each with what it shows and where its parts are, located
    once by the vision model and kept (picture_parts). Returns the lines the model
    reads and each picture's parts, by index, which its callouts are drawn to. The
    slide itself and icons are not described: they are shown whole, if at all."""
    from pipeline.picture_parts import described, parts_of

    every = brief.get("assets", {}).get("pictures", [])
    roles = {entry.get("index"): entry.get("role")
             for entry in brief.get("picture_catalogue") or []}
    chosen = [(index, path) for index, path in enumerate(every)
              if roles.get(index) not in ("slide", "icon")][:PICTURES_DESCRIBED]
    lines, parts = [], {}
    for index, path in chosen:
        found = parts_of(cache_folder, path, state)
        if found:
            lines.append(described(index, Path(path).name, found))
            parts[index] = found.get("parts", [])
    return "\n".join(lines), parts


def request(brief: dict[str, Any], notes: str, earlier: str, entry: str, code: str,
            feedback: str, instruction: str, renderers: list[str],
            shots: list | None = None) -> str:
    parts = ["## The scene's brief (word_starts are word@seconds)\n"
             + json.dumps(compact(brief), indent=1, ensure_ascii=False)]
    if notes:
        parts.append("## The nearest pictures and the parts you may point to\n" + notes)
    if earlier:
        parts.append("## What the scenes just before this one did (stay consistent)\n" + earlier)
    if instruction.strip():
        parts.append("## What the person asked for\n" + instruction.strip())
    if shots:
        # Written from its shots: they are what to change, not the program.
        parts.append("## The scene's shots as they are now (the program is written from "
                     "them: answer with corrected shots)\n```json\n"
                     + json.dumps({"shots": shots}, indent=1, ensure_ascii=False) + "\n```")
    elif code.strip():
        parts.append(f"## {entry} as it is now\n```\n{code}\n```")
    if feedback:
        parts.append("## What the last round found\n" + feedback)
    task = ("Write the scene." if not code.strip()
            else "Fix what the last round found." if feedback
            else "Change the scene as asked.")
    parts.append(task + "\n\n" + answer_format(renderers))
    return "\n\n".join(parts)
