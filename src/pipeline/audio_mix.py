"""Music under a voice, mixed one way everywhere: the sample a person listens to
before choosing is the mix the render makes.

The bed is set to its level (`video_setup.INTENSITIES`, in dB) and then pressed
down further while the voice speaks -- sidechain compression keyed by the voice --
so it fills the pauses and gets out of the way of the words. Both are made
48 kHz stereo first; the voice stays in the middle.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

RATE = 48000
LAYOUT = "aformat=sample_rates=48000:channel_layouts=stereo"
# Pressed down ~10 dB while the voice speaks, back up within half a second after.
DUCKING = "sidechaincompress=threshold=0.015:ratio=8:attack=15:release=450:makeup=1"


def bed_under_voice(voice: str, bed: str, level_db: float, out: str) -> str:
    """An ffmpeg filter: the stream labelled `bed` laid under `voice`, as `out`.
    As long as the voice; the bed must already loop at least that long."""
    return (f"[{bed}]{LAYOUT},volume={level_db:.1f}dB[bedlevel];"
            f"[{voice}]{LAYOUT},asplit=2[voicekey][voicemix];"
            f"[bedlevel][voicekey]{DUCKING}[ducked];"
            f"[voicemix][ducked]amix=inputs=2:duration=first:dropout_transition=0:"
            f"normalize=0[{out}]")


def mix_under_voice(voice_path: Path, bed_path: Path, level_db: float, target: Path,
                    *, seconds: float, lead_in: float = 0.0) -> Path:
    """A sample: the bed alone for `lead_in` seconds, then the voice over it, as
    the render mixes them; `seconds` long, faded at both ends, as MP3."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is needed to mix music under a voice.")
    delay = int(lead_in * 1000)
    graph = (f"[0:a]adelay={delay}|{delay},apad=whole_dur={seconds}[voice];"
             + bed_under_voice("voice", "1:a", level_db, "mixed")
             + f";[mixed]afade=t=in:d=0.8,afade=t=out:st={seconds - 1.5}:d=1.5,"
               f"loudnorm=I=-16:TP=-1.5:LRA=11[final]")
    subprocess.run([ffmpeg, "-y", "-v", "error", "-i", str(voice_path),
                    "-stream_loop", "-1", "-i", str(bed_path), "-filter_complex", graph,
                    "-map", "[final]", "-t", f"{seconds}", "-ar", str(RATE),
                    "-c:a", "libmp3lame", "-b:a", "160k", str(target)],
                   check=True, capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
    return target
