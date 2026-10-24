"""Every scene is a program: what its brief is measured from, what is kept about
it, and when it may be used.

- **The narration, measured.** A scene's narration is spoken once with the
  project's voice and kept in its folder (`narration.mp3`, with the voice's word
  timings). Its measured length is the scene's length, and the word timings are
  how a program puts each visual beat on the words that explain it.
- **The brief, grounded.** Besides the narration and the visual brief, the
  program is given the source text of its section's slides, the approved
  pictures (by path), the deck's slide for reference only, and where the scene
  falls in its section.
- **The specification, kept.** `spec.json`: the renderer, the beats and the
  assets the agent chose, beside the code that does it.
- **A preview with its voice.** `preview.mp4` is the clip with its narration.
- **Its folder.** Named once from its place and title, then kept.

A leaf: it never imports `scene_lab`, which owns a scene's lifecycle -- the brief,
the run, the checks and the approval -- and calls these.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Any

from pipeline.core import OperationFailed
from pipeline.generation import WORDS_PER_SECOND, VisualPlanStore, _now
from pipeline.scene_checks import RENDERERS

NARRATION = "narration.mp3"
NARRATION_FACTS = "narration.json"
LONGEST_SOURCE_TEXT = 4000
SCENES = "generation/scenes"
_INDEX_LOCK = threading.Lock()


# --- its folder ---------------------------------------------------------------------------


def _index_path(project) -> Path:
    return project.root / SCENES / "index.json"


def _index(project) -> dict[str, str]:
    path = _index_path(project)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def scene_folder(project, visual, create: bool = False) -> Path | None:
    """The scene's folder. Named once, from its place and title, and then kept:
    a scene that moves in the script does not lose its script.

    Four scenes are made at once, and each names its folder here. Written in
    place and unlocked, one read the index while another was writing it -- an
    empty file, and eight scenes failed before they began -- and two starting
    together could both take the same number. Locked, and written whole."""
    from pipeline.storage.documents import write_text_atomically

    with _INDEX_LOCK:
        index = _index(project)
        name = index.get(visual.scene_id)
        if name is None:
            if not create:
                return None
            words = re.sub(r"[^a-z0-9]+", "-", visual.section_title.lower()).strip("-")[:40]
            name = f"{len(index) + 1:03d}-{words or 'scene'}-{visual.scene_number}"
            index[visual.scene_id] = name
            write_text_atomically(_index_path(project), json.dumps(index, indent=1))
    folder = project.root / SCENES / name
    if create:
        (folder / "assets").mkdir(parents=True, exist_ok=True)
    return folder


def _voice(project) -> tuple[str, str]:
    from pipeline.stage_options import video_preferences

    return "edge", video_preferences(project.root).voice_for("edge")


def measure_narration(project, folder: Path, narration: str) -> dict[str, Any]:
    """Speak the scene's narration once and measure it. Kept, and spoken again
    only when the words or the voice change."""
    from pipeline.narration_audio import speak
    from pipeline.speech import SpeechFailed
    from pipeline.video_setup import pronunciations

    provider, voice = _voice(project)
    sounds = pronunciations(project.root)
    said = json.dumps(sorted(sounds.items()), ensure_ascii=False)
    key = hashlib.sha256(f"{provider}|{voice}|{said}|{narration}".encode()).hexdigest()[:16]
    facts_path = folder / NARRATION_FACTS
    if facts_path.exists():
        facts = json.loads(facts_path.read_text(encoding="utf-8"))
        if facts.get("key") == key and (folder / NARRATION).exists():
            return facts
    try:
        spoken = speak(narration, folder / NARRATION, provider, voice, sounds)
    except SpeechFailed as failure:
        raise OperationFailed(f"The narration could not be spoken to measure it: {failure}") \
            from failure
    from pipeline import voice_pace
    from pipeline.scripting import count_words

    voice_pace.record(spoken.voice or voice, count_words(narration), spoken.duration_ms)
    facts = {"key": key, "provider": provider, "voice": spoken.voice,
             "seconds": round(spoken.duration_ms / 1000, 2),
             "words": [w.to_dict() for w in spoken.words], "measured_at": _now()}
    facts_path.write_text(json.dumps(facts, indent=1, ensure_ascii=False), encoding="utf-8")
    return facts


def _measured_seconds(folder: Path | None) -> float | None:
    if folder is None or not (folder / NARRATION_FACTS).exists():
        return None
    return json.loads((folder / NARRATION_FACTS).read_text(encoding="utf-8")).get("seconds")


def _section_visuals(project, visual) -> list:
    return sorted(VisualPlanStore(project.root).load().for_section(visual.section_id),
                  key=lambda v: v.scene_number)


def time_range(project, visual, seconds: float, section_visuals: list) -> dict[str, Any]:
    """Where the scene falls in its section: the measured scenes before it, or a
    guess from their words where one is not measured yet (and said so)."""
    start, measured = 0.0, True
    for other in section_visuals:
        if other.scene_number >= visual.scene_number:
            break
        known = _measured_seconds(scene_folder(project, other))
        if known is None:
            measured = False
            known = len(other.narration_preview.split()) / WORDS_PER_SECOND
        start += known
    return {"start": round(start, 2), "end": round(start + seconds, 2),
            "earlier_scenes_measured": measured}


def extend_brief(project, visual, folder: Path, brief: dict[str, Any], section) -> dict:
    """The measured, grounded brief a scene program is written and checked against."""
    from pipeline import art_direction
    from pipeline.extraction import ExtractionStore
    from pipeline.plan_units import section_source_text
    from pipeline.scene_backgrounds import for_brief

    facts = measure_narration(project, folder, brief["narration"])
    source = ""
    if section is not None and section.sources:
        source, _cut = section_source_text(ExtractionStore(project.root).load(), section.sources)
    section_visuals = _section_visuals(project, visual)
    return brief | {
        "seconds": facts["seconds"],
        "narration_measured": True,
        "words": facts["words"],
        "time_range": time_range(project, visual, facts["seconds"], section_visuals),
        "source_text": source[:LONGEST_SOURCE_TEXT],
        "assets": {"pictures": brief.get("pictures", [])},
        "renderers": list(RENDERERS),
        "section_scenes": _section_scenes(visual, section_visuals),
        # What the kit lays under the scene, kept across its shots; None when it
        # has none or a person switched it off (`scene_backgrounds`).
        "background": for_brief(folder),
        # The art director's plan for this scene (`art_direction`): its maker follows it.
        "direction": art_direction.for_scene(project, visual.id),
    }


def _section_scenes(visual, section_visuals: list) -> list[dict[str, Any]]:
    """Every scene of the section, so one scene can be a stage of a picture the
    whole section builds -- a timeline, a growing diagram -- with this one marked."""
    return [{"scene_number": other.scene_number, "this_scene": other.id == visual.id,
             "on_screen": other.brief[:200], "narration_starts": other.narration_preview}
            for other in section_visuals]


# --- what is kept --------------------------------------------------------------------------


ENTRY_FILES = {"manim": "scene.py", "matplotlib": "scene.py", "pillow": "scene.py",
               "web": "scene.html", "revideo": "scene.tsx"}


def entry_of(folder: Path | None) -> tuple[str, str]:
    """The scene's renderer and the file it renders, from its spec (scene.py when
    no renderer is named yet)."""
    spec_path = folder / "spec.json" if folder else None
    spec = json.loads(spec_path.read_text(encoding="utf-8")) \
        if spec_path and spec_path.exists() else {}
    renderer = str(spec.get("renderer", ""))
    return renderer, ENTRY_FILES.get(renderer, "scene.py")


def save_spec(folder: Path, spec: dict[str, Any]) -> None:
    (folder / "spec.json").write_text(json.dumps(spec | {"written_at": _now()}, indent=2,
                                                 ensure_ascii=False), encoding="utf-8")


def make_preview(folder: Path) -> bool:
    """The clip with its own narration, for watching before approving."""
    ffmpeg = shutil.which("ffmpeg")
    clip, voice = folder / "render.mp4", folder / NARRATION
    if not (ffmpeg and clip.exists() and voice.exists()):
        return False
    done = subprocess.run(
        [ffmpeg, "-y", "-v", "error", "-i", str(clip), "-i", str(voice), "-map", "0:v",
         "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest",
         str(folder / "preview.mp4")], capture_output=True, check=False, timeout=300)
    return done.returncode == 0


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


CLIP_LOCK_WAITS = (0.25, 0.5, 1)    # seconds: only a player outside the app holds it now


def _clear_last_clip(clip: Path, waits=CLIP_LOCK_WAITS, sleep=None) -> bool:
    """Remove the last round's clip. On Windows a clip being played -- the page
    showing its preview -- cannot be removed; Demo 003 lost a scene to that, the
    error ending it outright. Waited out a little; False if it stays open."""
    import time

    sleep = sleep or time.sleep
    for pause in (*waits, None):
        try:
            clip.unlink(missing_ok=True)
            return True
        except PermissionError:
            if pause is None:
                return False
            sleep(pause)
    return False


# Releases known to break a scene's environment, held back for every scene program
# whatever it declares: `uv run --with` adds them as requirements. Pillow 13.0.0
# (17 Oct 2026) refuses the image mode Manim 0.22 passes to Image.fromarray, and
# every picture in every Manim scene failed to draw.
HELD_BACK = ("pillow<13",)


PLAYED = "played"            # beside the scene's files: the copies the page plays


def played_copy(clip: Path) -> Path:
    """A copy of `clip` named for this version of it, for the page to play. A page
    playing render.mp4 itself held it open, and on Windows the next round could
    not replace it -- the round waited, then failed. Each round's clip is now a new
    file to the page; copies of earlier versions are removed when nothing holds
    them."""
    stat = clip.stat()
    folder = clip.parent / PLAYED
    copy = folder / f"{clip.stem}-{stat.st_mtime_ns}-{stat.st_size}{clip.suffix}"
    if copy.exists():
        return copy
    folder.mkdir(exist_ok=True)
    partial = copy.with_name(copy.name + ".part")
    shutil.copyfile(clip, partial)
    try:
        partial.replace(copy)
    except PermissionError:             # another request made the same copy first
        partial.unlink(missing_ok=True)
    for older in folder.glob(f"{clip.stem}-*{clip.suffix}"):
        if older != copy:
            try:
                older.unlink()
            except OSError:             # still being played: removed another time
                pass
    return copy
