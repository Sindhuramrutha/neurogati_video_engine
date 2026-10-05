"""The agent that writes a scene's script -- and the resource library it draws on.

Writing is a loop, because code that has not run is a guess:

    write scene.py  ->  run it  ->  check the clip  ->  fix what failed  ->  ...

up to `MAXIMUM_ATTEMPTS` times. Each attempt is one model call, and the page
says how many a job may cost before it starts. The agent is free in *how* it
draws the scene -- any library, any open resource -- and is told the contract
(`resources/methods/scene-contract.md`), every method note, and an index of the
code and assets in the resource library. What decides whether the scene is used
is not the agent's opinion of its own work but the checks in `scene_lab`.

Adding a file to `resources/` is how a person teaches the agent a technique, a
component or a house style: the next scene it writes is shown it.
"""

from __future__ import annotations

import ast
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from pipeline.core import OperationFailed, require_project
from pipeline.generation import VisualPlanStore
from pipeline.llm import ModelCallFailed, ModelNotConfigured, complete_structured
from pipeline.scene_lab import (
    FAIL,
    MAXIMUM_SCRIPT_ATTEMPTS,
    SCRIPTED,
    read_scene,
    resources_root,
    run_scene,
    save_scene_code,
    scene_folder,
    write_brief,
)

MAXIMUM_ATTEMPTS = MAXIMUM_SCRIPT_ATTEMPTS
RESOURCE_KINDS = {"code": {".py"}, "methods": {".md", ".py", ".txt"},
                  "assets": {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ttf", ".otf",
                             ".json", ".csv", ".mp3", ".wav"}}
LONGEST_METHOD_CHARACTERS = 6000
LARGEST_RESOURCE_BYTES = 25 * 1024 * 1024


class WrittenScene(BaseModel):
    approach: str = Field(description="One sentence: what the scene shows, and drawn with what.")
    code: str = Field(description="The complete scene.py, starting with its '# /// script' block.")


# --- the resource library ------------------------------------------------------------------


def _about(path: Path) -> str:
    """One line saying what a resource is for: its docstring, or its first heading."""
    if path.suffix == ".py":
        try:
            docstring = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
        except (SyntaxError, UnicodeDecodeError):
            docstring = ""
        return docstring.strip().splitlines()[0] if docstring.strip() else ""
    if path.suffix in (".md", ".txt"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                return line.strip().lstrip("# ")
    return f"{path.stat().st_size // 1024 or 1} KB"


def resource_index() -> dict[str, list[dict[str, str]]]:
    """Everything in the resource library, by kind, in name order."""
    index: dict[str, list[dict[str, str]]] = {}
    for kind in RESOURCE_KINDS:
        folder = resources_root() / kind
        index[kind] = [{"name": path.name, "about": _about(path)}
                       for path in sorted(folder.glob("*")) if path.is_file()
                       and not path.name.startswith(".")] if folder.exists() else []
    return index


def add_resource(kind: str, file_name: str, content: bytes) -> dict[str, Any]:
    """Put a file in the library. The next scene the agent writes is shown it."""
    if kind not in RESOURCE_KINDS:
        raise OperationFailed(f"{kind!r} is not a kind of resource. One of: code, methods, assets.")
    name = Path(file_name).name
    if Path(name).suffix.lower() not in RESOURCE_KINDS[kind]:
        raise OperationFailed(
            f"{kind} takes {', '.join(sorted(RESOURCE_KINDS[kind]))}; {name} is not one.")
    if len(content) > LARGEST_RESOURCE_BYTES:
        raise OperationFailed(f"{name} is larger than 25 MB.")
    folder = resources_root() / kind
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(content)
    return resource_index()


def remove_resource(kind: str, file_name: str) -> dict[str, Any]:
    if kind not in RESOURCE_KINDS:
        raise OperationFailed(f"{kind!r} is not a kind of resource.")
    (resources_root() / kind / Path(file_name).name).unlink(missing_ok=True)
    return resource_index()


def _library_for_agent() -> str:
    index = resource_index()
    parts = ["## The resource library\n"]
    for note in sorted((resources_root() / "methods").glob("*")):
        if note.is_file():
            text = note.read_text(encoding="utf-8", errors="replace")
            parts.append(f"### methods/{note.name}\n{text[:LONGEST_METHOD_CHARACTERS]}")
    parts.append("### code (importable by name)\n" + ("\n".join(
        f"- {entry['name']}: {entry['about']}" for entry in index["code"]) or "(none)"))
    parts.append("### assets (in the SCENE_RESOURCES folder)\n" + ("\n".join(
        f"- {entry['name']} ({entry['about']})" for entry in index["assets"]) or "(none yet)"))
    return "\n\n".join(parts)


# --- writing a scene -------------------------------------------------------------------------


def _system_prompt(project) -> str:
    from pipeline.agent_runtime import build_system_prompt, resolve_agent
    from pipeline.scene_renderers import has_latex
    from pipeline.stages import Stage

    return (
        f"{build_system_prompt(resolve_agent(project, Stage.GENERATION))}\n\n"
        f"---\nYou are writing ONE scene of an explainer video as a Python script, "
        f"`scene.py`. You choose how to draw it: the library, the technique, an open "
        f"resource from the internet -- whatever shows this scene's idea best. Prefer a "
        f"picture of the idea that moves as it is explained over words on a background. "
        f"Everything on screen must come from the scene's narration and on-screen brief; "
        f"add no fact, number or label that is not in them.\n"
        f"The script is run and its clip is checked. Follow the contract exactly.\n"
        f"LaTeX is {'installed' if has_latex() else 'NOT installed: do not use MathTex or Tex'}"
        f".\n\n{_library_for_agent()}"
    )


def _request(brief: dict[str, Any], instruction: str, code: str) -> str:
    parts = ["## The scene's brief (brief.json)\n"
             + json.dumps(brief, indent=2, ensure_ascii=False)]
    if code.strip():
        parts.append("## The scene.py it has now\n```python\n" + code + "\n```")
    if instruction.strip():
        parts.append("## What the person asked for\n" + instruction.strip())
    parts.append("Write the complete scene.py." if not code.strip()
                 else "Rewrite scene.py as asked. Return the complete file.")
    return "\n\n".join(parts)


def _repair(code: str, checks: list[dict[str, str]], log: str) -> str:
    failed = "\n".join(f"- {c['name']}: {c['detail']} (rule: {c['rule']})"
                       for c in checks if c["status"] == FAIL)
    return ("## This scene.py was run and failed its checks\n```python\n" + code + "\n```\n\n"
            "## The checks that failed\n" + failed + "\n\n## What it printed (the end of it)\n"
            + log[-2500:] + "\n\nFix it. Return the complete corrected scene.py.")


def script_scene(slug: str, visual_id: str, instruction: str = "") -> dict[str, Any]:
    """Have the agent write this scene's script, run it, and fix it until the
    checks pass or the attempts run out. The last attempt is kept either way."""
    project = require_project(slug)
    visual = next((v for v in VisualPlanStore(project.root).load().visuals
                   if v.id == visual_id), None)
    if visual is None:
        raise OperationFailed(f"No scene {visual_id!r}.")

    folder = scene_folder(project, visual, create=True)
    brief = write_brief(project, visual)
    existing = (folder / "scene.py").read_text(encoding="utf-8") \
        if (folder / "scene.py").exists() else ""
    system_prompt = _system_prompt(project)
    request = _request(brief, instruction, existing if instruction.strip() else "")

    attempts, approach, result = [], "", {}
    for attempt in range(1, MAXIMUM_ATTEMPTS + 1):
        try:
            written = complete_structured(WrittenScene, system_prompt, request)
        except (ModelCallFailed, ModelNotConfigured) as failure:
            raise OperationFailed(f"The scene could not be written: {failure}") from failure
        approach = written.approach.strip()
        save_scene_code(slug, visual_id, written.code.strip() + "\n")
        result = run_scene(slug, visual_id)
        failing = [c for c in result["checks"] if c["status"] == FAIL]
        attempts.append({"attempt": attempt, "approach": approach,
                         "failed": [c["name"] for c in failing]})
        if not failing:
            break
        request = _repair(written.code, result["checks"], result["log"])

    (folder / "author.json").write_text(json.dumps({
        "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "instruction": instruction, "approach": approach, "attempts": attempts,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return read_scene(slug, visual_id) | {"attempts": attempts, "approach": approach}


def mark_scripted(slug: str, visual_ids: list[str] | None = None) -> int:
    """Choose "a scripted scene" for these scenes, or for every scene. Nothing is
    written or run: each is simply waiting for its script."""
    project = require_project(slug)
    store = VisualPlanStore(project.root)
    plan = store.load()
    changed = 0
    for visual in plan.visuals:
        if (visual_ids is None or visual.id in visual_ids) and visual.kind != SCRIPTED:
            # The slide is kept for the script to use before the scene stops being one.
            write_brief(project, visual)
            visual.kind, visual.origin, visual.drawn_by = SCRIPTED, SCRIPTED, "scene.py"
            visual.headline = visual.headline or visual.section_title
            visual.asset_path = visual.clip_path = visual.built_at = ""
            visual.note = "Waiting for its script."
            changed += 1
    store.save(plan)
    return changed
