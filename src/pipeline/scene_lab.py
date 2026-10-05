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

`scene.py` is free code: it may use Manim, matplotlib, Pillow, anything it
declares at its top (run through `uv`, which installs what it names), and the
resource library (`resources/`). That freedom is the point, and it is also what
made the first version of this pipeline unreliable -- code nobody checked. So
the freedom is the script's and the judgement is not: every run is followed by
the same fixed checks (`CHECKS`), and a scene whose clip fails one is not used.

The script runs as a subprocess in its own folder, with a time limit, and its
whole process tree is killed when the limit passes. It is a program on this
machine, with this user's permissions: that is stated on the page.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pipeline.config import REPO_ROOT
from pipeline.core import OperationFailed, require_project
from pipeline.generation import VisualPlanStore, brief_fingerprint
from pipeline.rendering import FRAME_HEIGHT, FRAME_RATE, FRAME_WIDTH

logger = logging.getLogger(__name__)

SCRIPTED = "scripted"
SCENES = "generation/scenes"
# Long, because a first run installs what the script declares.
RUN_TIMEOUT_SECONDS = 900
MAXIMUM_SCRIPT_ATTEMPTS = 3   # write, then up to two fixes: one model call each
WORDS_PER_SECOND = 2.5
SHORTEST_SCENE_SECONDS = 3.0
LOG_CHARACTERS_KEPT = 6000

# The clip may be a little short (it holds its last frame) and never long (the
# render cuts it off, and what was cut is what the narration was reaching).
SHORTEST_SHARE, LONGEST_SHARE = 0.6, 1.1
FLATTEST_FRAME = 3.0          # standard deviation of brightness, 0-255
PASS, WARN, FAIL = "pass", "warn", "fail"

INLINE_METADATA = re.compile(r"^# /// script\s*$", re.MULTILINE)


def resources_root() -> Path:
    return REPO_ROOT / "resources"


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


# --- folders ---------------------------------------------------------------------------


def _index_path(project) -> Path:
    return project.root / SCENES / "index.json"


def _index(project) -> dict[str, str]:
    path = _index_path(project)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def scene_folder(project, visual, create: bool = False) -> Path | None:
    """The scene's folder. Named once, from its place and title, and then kept:
    a scene that moves in the script does not lose its script."""
    index = _index(project)
    name = index.get(visual.scene_id)
    if name is None:
        if not create:
            return None
        words = re.sub(r"[^a-z0-9]+", "-", visual.section_title.lower()).strip("-")[:40]
        name = f"{len(index) + 1:03d}-{words or 'scene'}-{visual.scene_number}"
        index[visual.scene_id] = name
        path = _index_path(project)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(index, indent=1), encoding="utf-8")
    folder = project.root / SCENES / name
    if create:
        (folder / "assets").mkdir(parents=True, exist_ok=True)
    return folder


# --- the brief ---------------------------------------------------------------------------


def _scene_of(project, visual):
    from pipeline.script_handoff import script_for_later_stages

    for entry in script_for_later_stages(project).section_scripts:
        for scene in entry.scenes:
            if scene.id == visual.scene_id:
                return scene
    return None


def _keep_slide(project, visual, wash: str, target: Path) -> None:
    """The deck's own slide, drawn into the scene's folder for its script to use."""
    from pipeline.slide_frame import compose_slide
    from pipeline.visual_build import _deck_for

    deck = _deck_for(project, visual)
    if deck is None:
        return
    try:
        compose_slide(deck, visual.slide_number, target, wash=wash)
    except Exception as unreadable:   # a slide that cannot be drawn is not a scene that cannot
        logger.warning("slide %s could not be kept: %s", visual.slide_number, unreadable)


def write_brief(project, visual) -> dict[str, Any]:
    """What the script is told. Written before every run, so the script always
    draws the scene as it is now."""
    from pipeline.assets_handoff import _look_preview
    from pipeline.plan_handoff import plan_for_later_stages
    from pipeline.plan_pictures import assets_for_later_stages, pictures_of
    from pipeline.stage_options import video_preferences

    scene = _scene_of(project, visual)
    narration = scene.narration if scene else visual.narration_preview
    on_screen = scene.brief if scene else visual.brief
    plan = plan_for_later_stages(project)
    section = next((s for s in plan.sections if s.id == visual.section_id), None)
    # What the plan carried on from Assets & Design: the section's own pictures
    # and the look.
    library = assets_for_later_stages(project).library
    folder = scene_folder(project, visual, create=True)
    # The deck's slide, kept in the folder the first time: once the scene is
    # scripted its picture is the script's own, and the slide would be lost.
    slide = folder / "slide.png"
    if visual.slide_number and not slide.exists():
        _keep_slide(project, visual, library.look.slide_wash, slide)

    brief = {
        "scene_id": visual.scene_id,
        "section_title": visual.section_title,
        "role": section.role if section else "teach",
        "scene_number": visual.scene_number,
        "headline": visual.headline or visual.section_title,
        "narration": narration,
        "on_screen": on_screen,
        "seconds": round(max(SHORTEST_SCENE_SECONDS,
                             len(narration.split()) / WORDS_PER_SECOND), 1),
        "width": FRAME_WIDTH, "height": FRAME_HEIGHT, "fps": FRAME_RATE,
        "language": video_preferences(project.root).language,
        "look": {k: v for k, v in _look_preview(project, library.look).items() if k != "art"},
        "pictures": [str(project.root / f.shown_path)
                     for f in (pictures_of(section, plan, library) if section else [])],
        "slide_image": str(slide) if slide.exists() else "",
    }
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
    from pipeline.scene_renderers import _kill_tree

    (folder / "render.mp4").unlink(missing_ok=True)
    code_folder = str(resources_root() / "code")
    environment = os.environ | {
        "PYTHONPATH": os.pathsep.join(filter(None, [code_folder, os.environ.get("PYTHONPATH")])),
        "SCENE_RESOURCES": str(resources_root() / "assets"),
        "PYTHONIOENCODING": "utf-8",
    }
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    started = subprocess.Popen(
        _command(folder), cwd=folder, env=environment, text=True, encoding="utf-8",
        errors="replace", stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, creationflags=flags,
        start_new_session=sys.platform != "win32")
    timed_out = False
    try:
        output, _ = started.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_tree(started.pid)
        try:
            output, _ = started.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            output = ""
    log = (output or "")[-LOG_CHARACTERS_KEPT:]
    if timed_out:
        log += f"\n\nStopped: it did not finish in {seconds} seconds."
    (folder / "log.txt").write_text(log, encoding="utf-8")
    return {"code": started.returncode, "timed_out": timed_out, "log": log}


# --- the checks ----------------------------------------------------------------------------


def _probe(video: Path) -> dict[str, Any]:
    probe = shutil.which("ffprobe")
    if not probe or not video.exists():
        return {}
    try:
        output = subprocess.run(
            [probe, "-v", "error", "-show_entries",
             "format=duration:stream=codec_type,width,height", "-of", "json", str(video)],
            capture_output=True, text=True, timeout=60, check=True).stdout
        facts = json.loads(output)
    except (subprocess.SubprocessError, ValueError):
        return {}
    streams = facts.get("streams", [])
    picture = next((s for s in streams if s.get("codec_type") == "video"), None)
    if picture is None:
        return {}
    return {"width": picture.get("width", 0), "height": picture.get("height", 0),
            "seconds": float(facts.get("format", {}).get("duration") or 0),
            "has_sound": any(s.get("codec_type") == "audio" for s in streams)}


def _sample(video: Path, at_seconds: float, target: Path) -> float | None:
    """One frame saved as a picture, and how much its brightness varies."""
    from PIL import Image, ImageStat

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return None
    subprocess.run([ffmpeg, "-y", "-v", "error", "-ss", f"{at_seconds:.2f}", "-i", str(video),
                    "-frames:v", "1", str(target)], capture_output=True, check=False, timeout=60)
    if not target.exists():
        return None
    with Image.open(target) as image:
        return ImageStat.Stat(image.convert("L")).stddev[0]


def _check(key: str, name: str, rule: str, status: str, detail: str) -> dict[str, str]:
    return {"key": key, "name": name, "rule": rule, "status": status, "detail": detail}


def check_scene(folder: Path, brief: dict[str, Any], ran: dict[str, Any]) -> list[dict[str, str]]:
    """Every check a scene's clip goes through, in order. Fixed rules: the same
    clip always gets the same results."""
    video = folder / "render.mp4"
    checks = [_check(
        "ran", "The script ran", "scene.py finished without an error, inside the time limit",
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

    share = facts["seconds"] / brief["seconds"] if brief["seconds"] else 0
    checks.append(_check(
        "length", "It fits the narration",
        f"Between {SHORTEST_SHARE:.0%} and {LONGEST_SHARE:.0%} of the scene's "
        f"{brief['seconds']} s: shorter holds its last frame, longer is cut off",
        FAIL if share > LONGEST_SHARE else WARN if share < SHORTEST_SHARE else PASS,
        f"{facts['seconds']:.1f} s, for a scene of {brief['seconds']} s."))

    spread = [_sample(video, facts["seconds"] * at, folder / f"sample-{index}.png")
              for index, at in enumerate((0.1, 0.5, 0.9))]
    seen = [value for value in spread if value is not None]
    blank = bool(seen) and max(seen) < FLATTEST_FRAME
    checks.append(_check(
        "shows", "It shows something", "A frame is more than one flat colour",
        FAIL if blank or not seen else PASS,
        "Every sampled frame is one flat colour." if blank
        else "No frame could be read." if not seen else "The frames have a picture in them."))

    first, last = folder / "sample-0.png", folder / "sample-2.png"
    moves = first.exists() and last.exists() and first.read_bytes() != last.read_bytes()
    checks.append(_check(
        "moves", "Something changes", "The start and the end of the clip differ",
        PASS if moves else WARN,
        "The picture changes through the scene." if moves
        else "The start and the end look the same: it is a still."))

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

    if last.exists():
        shutil.copy(last, folder / "poster.png")
    for sample in folder.glob("sample-*.png"):
        sample.unlink()
    return checks


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
    plan = store.load()
    visual = _visual(plan, visual_id)
    folder = scene_folder(project, visual, create=True)
    if not (folder / "scene.py").exists():
        raise OperationFailed("This scene has no scene.py yet. Write one first.")

    brief = write_brief(project, visual)
    ran = run_script(folder)
    checks = check_scene(folder, brief, ran)
    failing = [c for c in checks if c["status"] == FAIL]
    (folder / "checks.json").write_text(json.dumps(
        {"checked_at": _now(), "checks": checks}, indent=2, ensure_ascii=False), encoding="utf-8")

    visual.kind, visual.origin, visual.drawn_by = SCRIPTED, SCRIPTED, "scene.py"
    visual.headline = visual.headline or visual.section_title
    visual.diagram, visual.prompt = None, ""
    scene = _scene_of(project, visual)
    if scene is not None:
        visual.brief_fingerprint = brief_fingerprint(scene.brief, scene.narration)
    if failing:
        visual.clip_path, visual.asset_path, visual.built_at = "", "", ""
        visual.note = f"Its script failed a check: {failing[0]['name']} -- {failing[0]['detail']}"
    else:
        visual.clip_path = _relative(project, folder / "render.mp4")
        visual.asset_path = _relative(project, folder / "poster.png")
        visual.built_at = _now()
        visual.note = f"Drawn by {folder.name}/scene.py."
    store.save(plan)
    return read_scene(slug, visual_id)


def save_scene_code(slug: str, visual_id: str, code: str) -> None:
    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    folder = scene_folder(project, visual, create=True)
    (folder / "scene.py").write_text(code, encoding="utf-8")


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
        "code": text_of("scene.py"),
        "brief": json_of("brief.json", {}),
        "checks": json_of("checks.json", {}).get("checks", []),
        "checked_at": json_of("checks.json", {}).get("checked_at", ""),
        "log": text_of("log.txt"),
        "sources": json_of("sources.json", []),
        "has_clip": bool(folder and (folder / "render.mp4").exists()),
    }


def scene_file(slug: str, visual_id: str, name: str) -> Path | None:
    """render.mp4 or poster.png of a scene, for the page."""
    if name not in ("render.mp4", "poster.png"):
        return None
    project = require_project(slug)
    visual = _visual(VisualPlanStore(project.root).load(), visual_id)
    folder = scene_folder(project, visual)
    path = folder / name if folder else None
    return path if path and path.exists() else None


def keep_scripted(existing: dict, visuals: list) -> list:
    """Deciding again keeps a scripted scene scripted: its script is a person's
    (or the agent's) work, and a rule choosing a slide over it would lose it. A
    scene that was rewritten stays scripted, and unmade until it is run again."""
    for index, visual in enumerate(visuals):
        was = existing.get(visual.scene_id)
        if was is not None and was.kind == SCRIPTED and visual.kind != SCRIPTED:
            visuals[index] = visual.model_copy(update={
                "kind": SCRIPTED, "origin": SCRIPTED, "drawn_by": "scene.py",
                "headline": was.headline, "asset_path": "", "clip_path": "",
                "built_at": "", "note": "Its scene was rewritten: run its script again."})
    return visuals
