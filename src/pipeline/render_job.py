"""A render as a job: one at a time, stoppable, and resumable.

A render is minutes of work -- a voice per section, then a picture per
section -- so it must not be all or nothing. A second click must not start a
second render beside the first (three at once slow each other to eight minutes a
section), and a render that stops for any reason must not throw everything away.

So a render keeps a record, `reviewing/output/render-job.json`, updated at
every section:

- **One at a time.** A render is refused while another of the same project
  runs.
- **Halt.** Asked to stop, it stops at the next section boundary and keeps
  what it made. The sections finished so far are joined into a preview.
- **Resume.** Continuing reuses every narration and every section clip already
  made, and starts where it stopped. Refused if the plan, the script, the voice
  or the pictures changed since -- that would mix two versions in one video.
- **Interrupted.** A render whose server stopped (a restart, a crash) is found
  on the next visit as "running" with nothing running it, and offered the same
  way: continue, start over, or discard.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import threading
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from pipeline import progress
from pipeline.core import OperationFailed, require_project
from pipeline.render_finish import _join_and_level
from pipeline.rendering import (
    DEFAULT_STYLE,
    RenderedSection,
    RenderStyle,
    _cross_fade_ms,
    _cut_section,
    _encode_shot,
    require_ffmpeg,
    shot_windows,
)
from pipeline.storage.documents import JsonDocumentStore

JOB = "render"

# Finished, a job leaves nothing behind but its record; unfinished, it keeps
# its working files so it can continue.
UNFINISHED = {"running", "halted", "failed", "interrupted"}


class RenderHalted(Exception):
    """Raised at a section boundary once a halt was asked for. `discard`: the
    person asked to stop and delete, not to pause."""

    def __init__(self, discard: bool = False) -> None:
        super().__init__("halted")
        self.discard = discard


class RenderJob(BaseModel):
    render_id: str = ""
    status: str = ""          # running | halted | failed | done
    started_at: str = ""
    updated_at: str = ""
    fingerprint: str = ""     # what was being rendered; resuming needs it unchanged
    voice_provider: str = ""
    voice: str = ""
    section_count: int = 0
    spoken: int = 0           # sections whose narration is made
    cut: int = 0              # sections whose picture clip is made
    partial_video: str = ""   # the finished sections joined, after a halt
    message: str = ""


class RenderJobStore(JsonDocumentStore[RenderJob]):
    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=project_root / "reviewing" / "output" / "render-job.json",
            model_type=RenderJob, build_default=RenderJob, description="render job",
        )


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def output_directory(project) -> Path:
    return project.root / "reviewing" / "output"


def working_directory(project, render_id: str) -> Path:
    return output_directory(project) / "frames" / render_id


def fingerprint(*parts: Any) -> str:
    """A digest of everything that decides what the video looks and sounds like."""
    text = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]


# --- halting ------------------------------------------------------------------------

_halts: dict[str, bool] = {}   # slug -> also discard what was made
_halts_lock = threading.Lock()


def request_halt(slug: str, discard: bool = False) -> dict[str, Any]:
    """Ask the running render to stop at its next section: to pause, keeping
    what it made, or -- `discard` -- to stop and delete it."""
    if not progress.read(slug, JOB)["active"]:
        raise OperationFailed("No render of this project is running.")
    with _halts_lock:
        _halts[slug] = _halts.get(slug, False) or discard
    progress.report(slug, JOB, 0, 0,
                    "Stopping and deleting after this section" if discard
                    else "Pausing after this section")
    return job_view(slug)


def check_halt(slug: str) -> None:
    with _halts_lock:
        if slug in _halts:
            raise RenderHalted(_halts.pop(slug))


def clear_halt(slug: str) -> None:
    with _halts_lock:
        _halts.pop(slug, None)


# --- the record ---------------------------------------------------------------------


def save(project, job: RenderJob, label: str = "") -> None:
    """Write the record, and tell the progress bar where the job is."""
    job.updated_at = now()
    RenderJobStore(project.root).save(job)
    with _halts_lock:
        stopping = _halts.get(project.slug)
    if stopping is not None:
        # A halt is on its way: say so until it lands, not the next section.
        label = "Stopping and deleting after this section" if stopping \
            else "Pausing after this section"
    if job.status == "running":
        steps = job.section_count * 2
        progress.report(project.slug, JOB, job.spoken + job.cut, steps, label)


def job_view(slug: str) -> dict[str, Any]:
    """The last render's record, as the page shows it."""
    project = require_project(slug)
    job = RenderJobStore(project.root).load()
    status = job.status
    if status == "running" and not progress.read(slug, JOB)["active"]:
        status = "interrupted"   # recorded as running; nothing is running it
    partial = job.partial_video if (
        job.partial_video and (project.root / job.partial_video).exists()) else ""
    return {
        "render_id": job.render_id, "status": status,
        "started_at": job.started_at, "updated_at": job.updated_at,
        "section_count": job.section_count, "spoken": job.spoken, "cut": job.cut,
        "partial_video": Path(partial).name if partial else "",
        "message": job.message,
        "can_resume": status in {"halted", "failed", "interrupted"}
                      and working_directory(project, job.render_id).exists(),
    }


def discard(slug: str) -> dict[str, Any]:
    """Throw an unfinished render away: its working files and its preview."""
    project = require_project(slug)
    if progress.read(slug, JOB)["active"]:
        raise OperationFailed("That render is still running; halt it first.")
    store = RenderJobStore(project.root)
    job = store.load()
    remove_leftovers(project, job)
    store.save(RenderJob())
    return job_view(slug)


def remove_leftovers(project, job: RenderJob) -> None:
    """An unfinished render's files: its working folder, its preview and its
    narration. Only ever called for a render that did not finish -- a finished
    one's narration is what its timeline plays."""
    if job.render_id:
        shutil.rmtree(working_directory(project, job.render_id), ignore_errors=True)
        for narration in (output_directory(project) / "audio").glob(f"*-{job.render_id}.mp3*"):
            narration.unlink(missing_ok=True)
    if job.partial_video:
        (project.root / job.partial_video).unlink(missing_ok=True)


# --- the picture, section by section ------------------------------------------------


def cut_sections(
    sections: list[RenderedSection],
    working: Path,
    *,
    style: RenderStyle = DEFAULT_STYLE,
    reuse: int = 0,
    before: Callable[[int], None] = lambda index: None,
    after: Callable[[int], None] = lambda index: None,
) -> list[Path]:
    """Draw and cut every section, reusing the first `reuse` clips already made.

    `before` runs ahead of each section and may raise `RenderHalted`; `after`
    runs once its clip exists. Returns the clips in order.

    One encode per *scene*, not per sentence: the camera move runs across the
    whole scene and its labels arrive on top as they are spoken. The rest of
    the timing is in `rendering`'s helpers, and each part fixed something:
    only the opening waits for a title card (one per section was seconds of
    silence each); each clip is cut to exactly `total_ms` (`-shortest` let
    sections overrun and drift); shots cross-fade, with the fade paid for out
    of a longer shot; and every clip has an audio stream, or the copy-join
    loses the sound partway through.
    """
    ffmpeg = require_ffmpeg()
    working.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []
    last_section = len(sections) - 1

    for index, section in enumerate(sections):
        clip = working / f"s{index:02d}.mp4"
        if index < reuse and clip.exists():
            clip_paths.append(clip)
            continue
        before(index)
        windows = shot_windows(section)
        if not windows:
            continue
        durations = [window.duration_ms for window in windows]
        fade_ms = _cross_fade_ms(durations)
        shot_paths = [
            _encode_shot(
                ffmpeg, section, window, style, working,
                name=f"s{index:02d}_{at:02d}",
                kicker=f"Section {index + 1}",
                length_ms=window.duration_ms + fade_ms,
                step=f"section {index + 1}, shot {at + 1} of {len(windows)}",
                opens_the_video=index == 0 and at == 0,
                closes_the_video=index == last_section and at == len(windows) - 1,
            )
            for at, window in enumerate(windows)
        ]
        clip_paths.append(_cut_section(
            ffmpeg, section, shot_paths, durations, fade_ms, index, working))
        after(index)
    return clip_paths


def join_clips(clip_paths: list[Path], working: Path, video_path: Path,
               project_root: Path | None = None) -> None:
    """Join the sections into the video, with the music Video setup chose under it."""
    from pipeline.video_setup import music_for

    music = music_for(project_root) if project_root is not None else (None, 0.0)
    _join_and_level(require_ffmpeg(), clip_paths, working, video_path, music)


def join_what_is_done(project, job: RenderJob) -> str:
    """Join the section clips made so far into a preview, and say where it is."""
    working = working_directory(project, job.render_id)
    clips = [working / f"s{index:02d}.mp4" for index in range(job.cut)]
    clips = [clip for clip in clips if clip.exists()]
    if not clips:
        return ""
    preview = output_directory(project) / f"{project.slug}-{job.render_id}-so-far.mp4"
    join_clips(clips, working, preview, project.root)
    return str(preview.relative_to(project.root)).replace("\\", "/")
