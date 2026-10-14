"""The best version of a scene so far, kept while the scene is made.

Every round that draws a clip is ranked: a version that passes every check beats
one that does not, and fewer failing checks beat more. The best is kept in the
scene's own `kept/` folder, and a round that comes out worse is undone back to it.
So the scene on disk is always the best one made, and when the rounds run out it
is what the scene keeps -- a clip with problems is shown with them, never thrown
away for nothing.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from pipeline.core import OperationFailed, require_project
from pipeline.generation import VisualPlanStore, brief_fingerprint
from pipeline.scene_lab import PLAN_LOCK, _record_run, _scene_of, _visual
from pipeline.scene_program import entry_of, make_preview, scene_folder

KEPT = "kept"
KEPT_FILES = ("spec.json", "render.mp4", "preview.mp4", "poster.png", "layout.json",
              "checks.json", "log.txt")


def rank(passed: bool, failing: list[str], good: bool = False, problems: int = 0,
         score: float = 0.0) -> tuple[int, int, float, int, int]:
    """Higher is better: passing first, then what the reviewer said -- good, then
    its rubric score, then fewer things it must fix -- then fewer failing checks.
    Two passing versions used to tie, and the newer one always won: a refinement
    the reviewer liked less replaced one it liked more."""
    return (1 if passed else 0, 1 if good else 0, round(score, 2), -problems, -len(failing))


def has_clip(folder: Path) -> bool:
    return (folder / "render.mp4").exists()


def keep_best(folder: Path) -> None:
    """Put the version on disk aside as the best so far."""
    if not (folder / "preview.mp4").exists():
        make_preview(folder)            # a failing clip is watched too, before deciding
    kept = folder / KEPT
    shutil.rmtree(kept, ignore_errors=True)
    kept.mkdir()
    for name in (*KEPT_FILES, entry_of(folder)[1]):
        if (folder / name).exists():
            shutil.copy2(folder / name, kept / name)
    if (folder / "frames").exists():
        shutil.copytree(folder / "frames", kept / "frames")


def passes_as_written(project, visual) -> bool:
    """The scene has a clip, made for its narration and brief as they are now --
    not one left from before the script was rewritten."""
    scene = _scene_of(project, visual)
    return bool(visual.clip_path) and scene is not None and (
        visual.brief_fingerprint == brief_fingerprint(scene.brief, scene.narration))


def drop_kept(folder: Path) -> None:
    shutil.rmtree(folder / KEPT, ignore_errors=True)


def failing_checks(folder: Path) -> list[dict[str, str]]:
    path = folder / "checks.json"
    if not path.exists():
        return []
    checks = json.loads(path.read_text(encoding="utf-8")).get("checks", [])
    return [c for c in checks if c.get("status") == "fail"]


def adopt(slug: str, visual_id: str) -> None:
    """Make the version on disk the scene's clip, whatever its checks say: it is
    the best one made, and a person decides on it with its problems in view."""
    project = require_project(slug)
    store = VisualPlanStore(project.root)
    folder = scene_folder(project, _visual(store.load(), visual_id))
    if not (folder / "preview.mp4").exists():
        make_preview(folder)
    with PLAN_LOCK:
        plan = store.load()
        _record_run(project, _visual(plan, visual_id), folder, failing_checks(folder),
                    keep_clip=True)
        store.save(plan)


def mark_below_bar(slug: str, visual_id: str, why: str) -> None:
    """Name the scene as used below the bar, so Export and the page can say so."""
    store = VisualPlanStore(require_project(slug).root)
    with PLAN_LOCK:
        plan = store.load()
        visual = _visual(plan, visual_id)
        visual.below_bar = why
        visual.note = f"Below the quality bar: {why} Watch it before approving."
        store.save(plan)


def restore_best(slug: str, visual_id: str) -> str:
    """Put the kept version back -- its program, clip and checks -- as the scene's
    clip, and return its program."""
    project = require_project(slug)
    store = VisualPlanStore(project.root)
    folder = scene_folder(project, _visual(store.load(), visual_id))
    kept = folder / KEPT
    if not kept.exists():
        raise OperationFailed("No version of this scene is kept.")
    for path in kept.iterdir():
        if path.is_file():
            shutil.copy2(path, folder / path.name)
    shutil.rmtree(folder / "frames", ignore_errors=True)
    if (kept / "frames").exists():
        shutil.copytree(kept / "frames", folder / "frames")
    adopt(slug, visual_id)
    return (folder / entry_of(folder)[1]).read_text(encoding="utf-8")
