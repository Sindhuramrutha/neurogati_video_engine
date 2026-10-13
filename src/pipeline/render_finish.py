"""Finishing: the section clips joined into the video, and its soundtrack made once.

The voice is cleaned (no rumble, softer "s" sounds, an even level), the music bed
Video setup chose is laid under it and ducked while it speaks, and the whole is
levelled for the web in one pass, 48 kHz stereo. The picture is copied: the
sections were encoded at working quality, and the brand pass (`render_brand`)
makes the final encode.
"""

from __future__ import annotations

from pathlib import Path

from pipeline.rendering import _run_ffmpeg

# The finished soundtrack: the voice cleaned, levelled for the web, 48 kHz stereo.
VOICE_CLEANUP = ("highpass=f=70,deesser=i=0.25,"
                 "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=200:makeup=2")
LEVEL_AUDIO = "loudnorm=I=-16:TP=-1.5:LRA=11"
FINAL_AUDIO = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
FINAL_VIDEO = ["-c:v", "libx264", "-preset", "medium", "-crf", "18"]


def _join_and_level(
    ffmpeg: str, clip_paths: list[Path], working_directory: Path, output_video_path: Path,
    music: tuple[Path | None, float] = (None, 0.0),
) -> None:
    """Concatenate the sections, then level the whole soundtrack once.

    One loudness pass over the finished audio, not one per section: levelling
    each section on its own makes every section internally consistent and each
    one a different loudness, which is the thing a viewer actually notices. The
    video is copied, so this costs a pass over the file and no quality.

    `+faststart` moves the moov atom to the front. Without it the index sits at
    the end of the file, so a browser must download all of it before the first
    frame plays -- which looks exactly like a video that does not work.
    """
    joined_list = working_directory / "clips.txt"
    joined_list.write_text(
        "\n".join(f"file '{path.as_posix()}'" for path in clip_paths), encoding="utf-8"
    )

    joined_path = working_directory / "joined.mp4"
    _run_ffmpeg(
        [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(joined_list),
         "-c", "copy", str(joined_path)],
        "joining the sections",
    )

    output_video_path.parent.mkdir(parents=True, exist_ok=True)
    # The voice cleaned (no rumble, softer "s" sounds, an even level), the music
    # bed laid under it when one is chosen, then the whole levelled once; 48 kHz
    # stereo, so a bed keeps its width.
    bed, level_db = music
    inputs = ["-i", str(joined_path)]
    graph = f"[0:a]{VOICE_CLEANUP}[voice];"
    if bed is not None:
        from pipeline.audio_mix import bed_under_voice

        inputs += ["-stream_loop", "-1", "-i", str(bed)]
        graph += bed_under_voice("voice", "1:a", level_db, "mixed") + ";[mixed]"
    else:
        graph += "[voice]"
    graph += f"{LEVEL_AUDIO}[audio]"
    _run_ffmpeg(
        [ffmpeg, "-y", *inputs, "-filter_complex", graph, "-map", "0:v", "-map", "[audio]",
         "-c:v", "copy", *FINAL_AUDIO, "-shortest", "-movflags", "+faststart",
         str(output_video_path)],
        "levelling the audio",
    )
