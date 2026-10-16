"""A scene as a folder with a script in it.

    generation/scenes/007-anorexia-defined/
        scene.py       what is on screen and when -- written by the agent, editable by hand
        brief.json     what the script is told: narration, words, length, size, the look
        assets/        files it uses
        sources.json   every outside resource, with its licence and credit
        render.mp4     the clip it drew
        poster.png     a frame of it
        checks.json    what the checks found
        log.txt        what the script printed
        kept/          the last version that passed every check, while it is remade

`scene.py` is free code: it may use Manim, matplotlib, Pillow, anything it
declares at its top (run through `uv`, which installs what it names), and the
resource library (`resources/`). That freedom is the point, and code nobody
checks is unreliable. So the freedom is the script's and the judgement is not:
every run is followed by the same fixed checks (`CHECKS`), and a scene whose
clip fails one is not used.

The script runs as a subprocess in its own folder, with a time limit, and its
whole process tree is killed when the limit passes. It is given only the
environment it needs to run (`SCENE_ENVIRONMENT`) -- never the server's, which
holds the model keys. It is still a program on this machine, with this user's
file permissions: that is stated on the page, and it is not a sandbox.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from pipeline.config import REPO_ROOT
from pipeline.core import OperationFailed, require_project
from pipeline.generation import WORDS_PER_SECOND, VisualPlanStore, _now, brief_fingerprint
from pipeline.plan_handoff import _check
from pipeline.rendering import FRAME_HEIGHT, FRAME_RATE, FRAME_WIDTH
from pipeline.scene_program import (
    _probe,
    entry_of,
    extend_brief,
    make_preview,
    scene_folder,
)

logger = logging.getLogger(__name__)

# Long, because a first run installs what the script declares.
RUN_TIMEOUT_SECONDS = 900
SHORTEST_SCENE_SECONDS = 3.0
LOG_CHARACTERS_KEPT = 6000

PASS, WARN, FAIL = "pass", "warn", "fail"

# Scenes run side by side (scene agents), and each records its result in the one
# visuals.json: every read-change-write of it holds this, and none holds it while
# a scene renders.
PLAN_LOCK = threading.RLock()

INLINE_METADATA = re.compile(r"^# /// script\s*$", re.MULTILINE)

# The only environment variables a scene program inherits: what Python, uv,
# ffmpeg and fonts need to run. Everything else -- API keys above all -- stays out.
SCENE_ENVIRONMENT = {
    "PATH", "PATHEXT", "SYSTEMROOT", "SYSTEMDRIVE", "WINDIR", "COMSPEC", "TEMP", "TMP",
    "TMPDIR", "HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "PROGRAMDATA",
    "PROGRAMFILES", "PROGRAMFILES(X86)", "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE",
    "LANG", "LC_ALL", "FONTCONFIG_PATH", "XDG_CACHE_HOME", "UV_CACHE_DIR",
    "UV_PYTHON_INSTALL_DIR", "UV_INDEX_URL", "UV_DEFAULT_INDEX",
}
BLAS_THREADS = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")


def resources_root() -> Path:
    return REPO_ROOT / "resources"


# --- the brief ---------------------------------------------------------------------------


def _scene_of(project, visual):
    from pipeline.script_handoff import script_for_later_stages

    for entry in script_for_later_stages(project).section_scripts:
        for scene in entry.scenes:
            if scene.id == visual.scene_id:
                return scene
    return None


def _deck_for(project, visual) -> Path | None:
    """The source file a scene's slide came from, if it is still there."""
    from pipeline.plan_handoff import plan_for_later_stages

    section = next((s for s in plan_for_later_stages(project).sections
                    if s.id == visual.section_id), None)
    if section is None:
        return None
    for source in section.sources:
        if source.slide_number and source.file_name:
            candidate = project.root / "sources" / source.file_name
            if candidate.exists():
                return candidate
    return None


def _keep_slide(project, visual, wash: str, target: Path) -> None:
    """The deck's own slide, drawn into the scene's folder for its script to use."""
    from pipeline.slide_frame import compose_slide

    deck = _deck_for(project, visual)
    if deck is None:
        return
    try:
        compose_slide(deck, visual.slide_number, target, wash=wash)
    except Exception as unreadable:   # a slide that cannot be drawn is not a scene that cannot
        logger.warning("slide %s could not be kept: %s", visual.slide_number, unreadable)


def keep_slide(project, visual, library=None) -> Path:
    """The deck's slide, kept in the scene's folder the first time: once the scene
    is scripted its picture is the script's own, and the slide would be lost."""
    from pipeline.plan_pictures import assets_for_later_stages

    slide = scene_folder(project, visual, create=True) / "slide.png"
    if visual.slide_number and not slide.exists():
        library = library or assets_for_later_stages(project).library
        _keep_slide(project, visual, library.look.slide_wash, slide)
    return slide


def write_brief(project, visual) -> dict[str, Any]:
    """What the script is told. Written before every run, so the script always
    draws the scene as it is now."""
    from pipeline import scene_pictures
    from pipeline.assets_handoff import _look_preview
    from pipeline.plan_handoff import plan_for_later_stages
    from pipeline.plan_pictures import assets_for_later_stages
    from pipeline.scene_vetting import notes, offered
    from pipeline.stage_options import video_preferences
    from pipeline.video_setup import platform_needs

    scene = _scene_of(project, visual)
    narration = scene.narration if scene else visual.narration_preview
    on_screen = scene.brief if scene else visual.brief
    plan = plan_for_later_stages(project)
    section = next((s for s in plan.sections if s.id == visual.section_id), None)
    # What the plan carried on from Assets & Design: the section's own pictures
    # and the look.
    library = assets_for_later_stages(project).library
    folder = scene_folder(project, visual, create=True)
    slide = keep_slide(project, visual, library)
    # Every deck picture, nearest first, none withheld: what each is, and whether
    # and how to show it, is the agent's to judge (scene_pictures, scene_vetting).
    tiers = scene_pictures.deck_tiers(project, visual, section, plan, library,
                                      on_screen, narration)
    on_screen, _deck = offered(folder.parent, on_screen,
                               [str(project.root / f.shown_path) for _, f in tiers])
    look = _look_preview(project, library.look)
    paths, catalogue = scene_pictures.catalogue(
        project, tiers, scene_pictures.made_for_scene(folder, on_screen, look),
        notes(folder.parent, [str(project.root / f.shown_path) for _, f in tiers]),
        scene_pictures.shown_pictures(project, skip_visual_id=visual.id),
        slide if slide.exists() else None)

    brief: dict[str, Any] = {
        "scene_id": visual.scene_id,
        "section_title": visual.section_title,
        "how": section.how if section else "",
        # Who it is for, and the smallest text the platforms allow (Video setup).
        "audience": video_preferences(project.root).audience(plan.audience),
        "smallest_text_px": platform_needs(project.root)["smallest_text_px"],
        "scene_number": visual.scene_number,
        "headline": visual.headline or visual.section_title,
        "narration": narration,
        "on_screen": on_screen,
        "seconds": round(max(SHORTEST_SCENE_SECONDS,
                             len(narration.split()) / WORDS_PER_SECOND), 1),
        "width": FRAME_WIDTH, "height": FRAME_HEIGHT, "fps": FRAME_RATE,
        "language": video_preferences(project.root).language,
        "look": {k: v for k, v in look.items() if k != "art"},
        # The pictures the brief names first, then those made for the scene, then
        # the rest of the deck's, nearest first; the catalogue says what each is.
        "pictures": paths,
        "picture_catalogue": catalogue,
        "slide_image": str(slide) if slide.exists() else "",
    }
    # Measured and grounded: the narration's own length and word timings, the
    # section's source text, and where the scene falls in its section.
    brief = extend_brief(project, visual, folder, brief, section)
    (folder / "brief.json").write_text(
        json.dumps(brief, indent=2, ensure_ascii=False), encoding="utf-8")
    return brief


# --- running -----------------------------------------------------------------------------


def _command(folder: Path) -> list[str]:
    arguments = ["scene.py", "--brief", "brief.json", "--out", "render.mp4"]
    code = (folder / "scene.py").read_text(encoding="utf-8")
    uv = shutil.which("uv")
    if uv and INLINE_METADATA.search(code):
        # Its own environment, holding exactly what the script declares.
        return [uv, "run", "--quiet", "--script", *arguments]
    return [sys.executable, *arguments]


def run_script(folder: Path, seconds: int = RUN_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Run `scene.py` in its folder and come back, whatever it does."""
    from pipeline import project_work

    (folder / "render.mp4").unlink(missing_ok=True)
    code_folder = str(resources_root() / "code")
    environment = {name: value for name, value in os.environ.items()
                   if name.upper() in SCENE_ENVIRONMENT} | {
        "PYTHONPATH": os.pathsep.join(filter(None, [code_folder, os.environ.get("PYTHONPATH")])),
        "SCENE_RESOURCES": str(resources_root() / "assets"),
        "PYTHONIOENCODING": "utf-8",
        # NumPy's BLAS keeps a buffer per CPU thread; a render needs none of that
        # speed, and on a machine short of memory it stopped renders with
        # "OpenBLAS error: Memory allocation still failed".
        **{name: "1" for name in BLAS_THREADS},
    }
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    started = subprocess.Popen(
        _command(folder), cwd=folder, env=environment, text=True, encoding="utf-8",
        errors="replace", stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, creationflags=flags,
        start_new_session=sys.platform != "win32")
    timed_out = False
    project_work.register(started)           # deleting the project kills it
    try:
        output, _ = started.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        project_work.kill_tree(started.pid)
        try:
            output, _ = started.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            output = ""
    finally:
        project_work.unregister(started)
    log = (output or "")[-LOG_CHARACTERS_KEPT:]
    if timed_out:
        log += f"\n\nStopped: it did not finish in {seconds} seconds."
    (folder / "log.txt").write_text(log, encoding="utf-8")
    return {"code": started.returncode, "timed_out": timed_out, "log": log}


# --- the checks ----------------------------------------------------------------------------


def check_scene(folder: Path, brief: dict[str, Any], ran: dict[str, Any]) -> list[dict[str, str]]:
    """Every check a scene's clip goes through, in order. Fixed rules: the same
    clip always gets the same results."""
    video = folder / "render.mp4"
    checks = [_check(
        "ran", "The program ran", "It finished without an error, inside the time limit",
        PASS if ran["code"] == 0 and not ran["timed_out"] else FAIL,
        "It finished." if ran["code"] == 0 and not ran["timed_out"]
        else "It ran out of time." if ran["timed_out"]
        else (ran["log"].strip().splitlines() or ["It stopped with an error."])[-1][:300])]

    facts = _probe(video)
    checks.append(_check(
        "video", "It made a video", "render.mp4 exists and has a picture in it",
        PASS if facts else FAIL,
        "render.mp4 is a video." if facts else "There is no readable render.mp4."))
    if not facts:
        return checks

    right_size = (facts["width"], facts["height"]) == (brief["width"], brief["height"])
    checks.append(_check(
        "frame", "The frame is the right size", f"{brief['width']}×{brief['height']}",
        PASS if right_size else FAIL, f"{facts['width']}×{facts['height']}."))

    checks.append(_check(
        "silent", "No sound of its own", "The narration is the only sound",
        WARN if facts["has_sound"] else PASS,
        "The clip has a sound track, which the render ignores." if facts["has_sound"]
        else "Silent."))

    used = [p.name for p in (folder / "assets").glob("*") if p.is_file()]
    record = folder / "sources.json"
    recorded = ({Path(entry.get("file", "")).name for entry in
                 json.loads(record.read_text(encoding="utf-8"))} if record.exists() else set())
    unrecorded = [name for name in used if name not in recorded]
    checks.append(_check(
        "sources", "Outside resources are recorded",
        "Every file in assets/ is in sources.json with its licence and credit",
        WARN if unrecorded else PASS,
        f"Not recorded: {', '.join(unrecorded[:5])}." if unrecorded
        else f"{len(used)} file(s), all recorded." if used else "It uses none."))

    from pipeline.scene_checks import program_checks
    return checks + program_checks(folder, brief, facts["seconds"])


# --- a scene, run and recorded --------------------------------------------------------------


def _relative(project, path: Path) -> str:
    return str(path.relative_to(project.root)).replace("\\", "/")


def _visual(plan, visual_id: str):
    visual = next((v for v in plan.visuals if v.id == visual_id), None)
    if visual is None:
        raise OperationFailed(f"No scene {visual_id!r}.")
    return visual


def run_scene(slug: str, visual_id: str) -> dict[str, Any]:
    """Run the scene's script, check its clip, and -- only if no check fails --
    make the clip what the scene shows."""
    project = require_project(slug)
    store = VisualPlanStore(project.root)
    visual = _visual(store.load(), visual_id)
    folder = scene_folder(project, visual, create=True)
    renderer, entry = entry_of(folder)
    if not (folder / entry).exists():
        raise OperationFailed(f"This scene has no {entry} yet. Write one first.")

    brief = write_brief(project, visual)
    (folder / "layout.json").unlink(missing_ok=True)     # never the last renderer's record
    if renderer in ("web", "revideo"):
        from pipeline.scene_revideo import render_revideo
        from pipeline.scene_web import render_web

        ran = (render_web if renderer == "web" else render_revideo)(
            folder, brief, RUN_TIMEOUT_SECONDS)
        (folder / "log.txt").write_text(ran["log"][-LOG_CHARACTERS_KEPT:], encoding="utf-8")
    else:
        ran = run_script(folder)
    checks = check_scene(folder, brief, ran)
    failing = [c for c in checks if c["status"] == FAIL]
    (folder / "checks.json").write_text(json.dumps(
        {"checked_at": _now(), "checks": checks}, indent=2, ensure_ascii=False), encoding="utf-8")
    if not failing:
        make_preview(folder)
    with PLAN_LOCK:
        plan = store.load()
        visual = _visual(plan, visual_id)
        _record_run(project, visual, folder, failing)
        store.save(plan)
    return read_scene(slug, visual_id)


def _record_run(project, visual, folder: Path, failing: list[dict[str, str]],
                keep_clip: bool = False) -> None:
    """What a run means for the scene: its clip if every check passed, else none --
    unless `keep_clip`, when the clip is the best one made and is kept with its
    failing checks named, for a person to judge."""
    visual.drawn_by = entry_of(folder)[1]
    visual.headline = visual.headline or visual.section_title
    scene = _scene_of(project, visual)
    if scene is not None:
        visual.brief_fingerprint = brief_fingerprint(scene.brief, scene.narration)
    visual.approved_at = ""          # a new run is watched and approved again
    visual.below_bar = ""            # ...and judged again
    if failing and keep_clip and (folder / "render.mp4").exists():
        visual.clip_path = _relative(project, folder / "render.mp4")
        visual.asset_path = _relative(project, folder / "poster.png")
        visual.built_at = _now()
        names = ", ".join(check["name"] for check in failing)
        visual.note = (f"Made, with {len(failing)} check(s) failing: {names}. Watch it, then "
                       "approve it as it is or say what to change.")
    elif failing:
        visual.clip_path, visual.asset_path, visual.built_at = "", "", ""
        # No preview of a failing program: a previous passing one would be shown
        # as if it were this.
        (folder / "preview.mp4").unlink(missing_ok=True)
        visual.note = f"Its script failed a check: {failing[0]['name']} -- {failing[0]['detail']}"
    else:
        visual.clip_path = _relative(project, folder / "render.mp4")
        visual.asset_path = _relative(project, folder / "poster.png")
        visual.built_at = _now()
        visual.note = (f"Drawn by {folder.name}/{entry_of(folder)[1]}. Watch its preview, "
                       "then approve it.")


def save_scene_code(slug: str, visual_id: str, code: str) -> None:
    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    folder = scene_folder(project, visual, create=True)
    (folder / entry_of(folder)[1]).write_text(code, encoding="utf-8")


def read_scene(slug: str, visual_id: str) -> dict[str, Any]:
    """Everything in the scene's folder that the page shows."""
    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    folder = scene_folder(project, visual)

    def text_of(name: str) -> str:
        path = folder / name if folder else None
        return path.read_text(encoding="utf-8", errors="replace") if path and path.exists() else ""

    def json_of(name: str, fallback: Any) -> Any:
        return json.loads(text_of(name)) if text_of(name) else fallback

    return {
        "visual": visual.to_dict(),
        "folder": _relative(project, folder) if folder else "",
        "code": text_of(entry_of(folder)[1]),
        "entry": entry_of(folder)[1],
        "brief": json_of("brief.json", {}),
        "checks": json_of("checks.json", {}).get("checks", []),
        "checked_at": json_of("checks.json", {}).get("checked_at", ""),
        "log": text_of("log.txt"),
        "sources": json_of("sources.json", []),
        "has_clip": bool(folder and (folder / "render.mp4").exists()),
        "has_preview": bool(folder and (folder / "preview.mp4").exists()),
        "spec": json_of("spec.json", {}),
        "author": json_of("author.json", {}),
    }


def scene_file(slug: str, visual_id: str, name: str) -> Path | None:
    """render.mp4, poster.png, or a picture made for it (painted, found, an icon),
    for the page."""
    if name not in ("render.mp4", "poster.png", "preview.mp4") \
            and not re.fullmatch(r"(illustration|found|icon)-[0-9a-f]{12}\.png", name):
        return None
    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    folder = scene_folder(project, visual)
    path = folder / name if folder else None
    return path if path and path.exists() else None
