"""Putting the brand kit on a rendered lesson: one ffmpeg pass.

The lesson is drawn and joined as before. Then, only when the transferred kit
has something in it, a single pass:

- lays the watermark and the logo over the lesson -- each already drawn to its
  size, corners, opacity and shadow (`brand_overlay.py`) -- at the place and
  for the time its placement says, fading in and out if asked;
- trims the intro and outro, fits them to the frame (letterboxed, never
  stretched) and the frame rate, gives a silent one silence, and joins them to
  the lesson -- cut to cut, or cross-faded for as long as was chosen;
- levels the whole soundtrack once, so an intro's music is not louder than the
  teacher.

Every number comes from the kit. Nothing here chooses anything, and the command
is built by a pure function so that it can be tested without running ffmpeg.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from pipeline.brand_kit import BrandKit
from pipeline.brand_overlay import overlay_box, prepare_overlay
from pipeline.render_finish import FINAL_VIDEO
from pipeline.rendering import FRAME_HEIGHT, FRAME_RATE, FRAME_WIDTH, _run_ffmpeg

_AUDIO = "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
# Fitted, never stretched: letterboxed to the frame, at the frame rate.
_FIT = (f"scale={FRAME_WIDTH}:{FRAME_HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={FRAME_WIDTH}:{FRAME_HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,"
        f"fps={FRAME_RATE},settb=AVTB")


def brand_arguments(kit: BrandKit, root: Path, lesson: Path, output: Path,
                    lesson_seconds: float, ffmpeg: str = "ffmpeg") -> list[str]:
    """The ffmpeg command that brands `lesson` into `output`. Pure, apart from
    drawing the overlays it points at."""
    inputs: list[str] = ["-i", str(lesson)]
    graph: list[str] = []

    def add(*arguments: str) -> int:
        inputs.extend(arguments)
        return inputs.count("-i") - 1

    graph.append(f"[0:v]{_FIT}[fit]")
    video = "[fit]"
    for slot, place in (("watermark", kit.watermark_place), ("logo", kit.logo_place)):
        file = getattr(kit, slot)
        if file is None:
            continue
        start, end = place.window(lesson_seconds)
        if end <= start:
            continue        # its time lies outside this lesson: nothing to lay on
        box = overlay_box(file, place)
        # Looped for the lesson's length, so it has a timeline to fade along.
        index = add("-loop", "1", "-t", f"{lesson_seconds:.3f}", "-i",
                    str(prepare_overlay(root, file, place)))
        fades = ""
        fade_in, fade_out = (min(f, (end - start) / 2) for f in (place.fade_in, place.fade_out))
        if fade_in > 0:
            fades += f",fade=t=in:st={start:.3f}:d={fade_in:.3f}:alpha=1"
        if fade_out > 0:
            fades += f",fade=t=out:st={end - fade_out:.3f}:d={fade_out:.3f}:alpha=1"
        graph.append(f"[{index}:v]format=rgba{fades}[{slot}]")
        graph.append(f"{video}[{slot}]overlay=x={box['left_px']}:y={box['top_px']}:"
                     f"enable='between(t,{start:.3f},{end:.3f})'[on_{slot}]")
        video = f"[on_{slot}]"
    graph.append(f"{video}format=yuv420p,setsar=1[lesson_v]")
    graph.append(f"[0:a]{_AUDIO}[lesson_a]")

    lengths = {"lesson": lesson_seconds}
    for name, clip, edit in (("intro", kit.intro, kit.intro_edit),
                             ("outro", kit.outro, kit.outro_edit)):
        if not clip:
            continue
        lengths[name] = length = edit.length(clip)
        start = min(max(0.0, edit.trim_start), clip.duration_ms / 1000 - length)
        cut = f"start={start:.3f}:end={start + length:.3f}"
        index = add("-i", str(root / clip.path))
        graph.append(f"[{index}:v]trim={cut},setpts=PTS-STARTPTS,{_FIT},"
                     f"format=yuv420p[{name}_v]")
        if clip.has_audio:
            graph.append(f"[{index}:a]atrim={cut},asetpts=PTS-STARTPTS,{_AUDIO}[{name}_a]")
        else:
            silent = add("-f", "lavfi", "-t", f"{length:.3f}", "-i", "anullsrc=r=24000:cl=mono")
            graph.append(f"[{silent}:a]{_AUDIO}[{name}_a]")

    # Joined left to right: intro + lesson, then + outro. Each join is a cut, or
    # a cross-fade that overlaps the two for as long as was chosen.
    order = [name for name in ("intro", "lesson", "outro") if name in lengths]
    overlaps = {"intro": min(kit.intro_edit.overlap(kit.intro), lesson_seconds / 2),
                "outro": min(kit.outro_edit.overlap(kit.outro), lesson_seconds / 2)}
    video, audio, length = f"[{order[0]}_v]", f"[{order[0]}_a]", lengths[order[0]]
    for step, name in enumerate(order[1:], start=1):
        overlap = overlaps["intro" if name == "lesson" else "outro"]
        if overlap > 0:
            graph.append(f"{video}[{name}_v]xfade=transition=fade:duration={overlap:.3f}:"
                         f"offset={length - overlap:.3f}[v{step}]")
            graph.append(f"{audio}[{name}_a]acrossfade=d={overlap:.3f}[a{step}]")
        else:
            graph.append(f"{video}{audio}[{name}_v][{name}_a]concat=n=2:v=1:a=1"
                         f"[v{step}][a{step}]")
        video, audio, length = f"[v{step}]", f"[a{step}]", length + lengths[name] - overlap
    graph.append(f"{video}format=yuv420p[v]")
    graph.append(f"{audio}loudnorm=I=-16:TP=-1.5:LRA=11[a]")

    return [ffmpeg, "-y", *inputs, "-filter_complex", ";".join(graph),
            "-map", "[v]", "-map", "[a]",
            "-r", str(FRAME_RATE), *FINAL_VIDEO,
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(output)]


def apply_brand(kit: BrandKit, root: Path, video_path: Path, working: Path) -> None:
    """Brand the finished lesson at `video_path`, in place. Nothing to do for an
    empty kit."""
    if kit.is_empty:
        return
    from pipeline.rendering import require_ffmpeg
    from pipeline.speech import measure_audio_duration_ms

    lesson = working / "lesson.mp4"
    shutil.move(str(video_path), lesson)
    seconds = measure_audio_duration_ms(lesson) / 1000
    _run_ffmpeg(brand_arguments(kit, root, lesson, video_path, seconds, require_ffmpeg()),
                "putting on the brand assets")
    lesson.unlink(missing_ok=True)
