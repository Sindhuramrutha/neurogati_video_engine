"""Narration as it is spoken: names said right, and room to breathe between scenes.

- **Pronunciations.** A name the voice says wrong (Loewi, Du Bois-Reymond) is
  respelled for the voice only -- "Loewi" is sent as "Lerver" -- and the word
  timings that come back are given the real spelling again, so subtitles, chapter
  marks and the beats a scene times to its words still read "Loewi".
- **Pauses.** A section is spoken scene by scene and the pieces joined with a
  pause between them. One run of speech left no breath between ideas, and a voice
  service cannot be asked for one; the picture holds the finished scene through it.

Scenes are measured, and the render speaks, through `speak` and `speak_scenes`
here -- one way -- so the timing a scene was made to and the timing it is cut to
cannot differ.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from dataclasses import replace
from pathlib import Path

from pipeline.speech import (
    SpeechFailed,
    SpeechResult,
    WordTiming,
    measure_audio_duration_ms,
    save_word_timings,
    synthesise_narration,
)

SCENE_PAUSE_MS = 700          # between two scenes of a section: one breath, then on
WORD = re.compile(r"\S+")
EDGE = re.compile(r"^\W+|\W+$")


def respell(text: str, sounds: dict[str, str]) -> tuple[str, list[tuple[int, str]]]:
    """The text the voice is given, and for each word it will say, which written
    word it stands for (its place, and how it is written)."""
    lowered = {" ".join(key.lower().split()): value.strip()
               for key, value in sounds.items() if key.strip() and value.strip()}
    longest = max((len(key.split()) for key in lowered), default=1)
    tokens = WORD.findall(text)
    bares = [EDGE.sub("", token) for token in tokens]
    said: list[str] = []
    origin: list[tuple[int, str]] = []
    place = 0
    while place < len(tokens):
        # The longest name that starts here: "Otto Loewi" before "Otto".
        for size in range(min(longest, len(tokens) - place), 0, -1):
            name = bares[place:place + size]
            spoken = lowered.get(" ".join(name).lower()) if all(name) else None
            if spoken:
                break
        else:
            size, spoken = 1, None
        if not spoken:
            said.append(tokens[place])
            origin += [(place, bares[place])] * len(tokens[place].split())
            place += 1
            continue
        first, last = tokens[place], tokens[place + size - 1]
        lead = first[:first.find(name[0])]
        tail = last[last.find(name[-1]) + len(name[-1]):]
        said.append(lead + spoken + tail)
        parts = spoken.split()
        # Word for word when the counts match; otherwise the whole name is one
        # timing that still carries every written word.
        origin += ([(place + index, name[index]) for index in range(size)]
                   if len(parts) == size else [(place, " ".join(name))] * len(parts))
        place += size
    return " ".join(said), origin


def restore(words: tuple[WordTiming, ...],
            origin: list[tuple[int, str]]) -> tuple[WordTiming, ...]:
    """The timings with every word given its written spelling, the parts of a
    respelled name joined into one. Left alone when the voice split the text
    differently from how it was written: a wrong match is worse than none."""
    if not words or len(words) != len(origin):
        return words
    merged: list[WordTiming] = []
    for index, timing in enumerate(words):
        place, written = origin[index]
        if index and origin[index - 1][0] == place:
            last = merged[-1]
            merged[-1] = WordTiming(last.text, last.start_ms, timing.end_ms - last.start_ms)
        else:
            merged.append(WordTiming(written or timing.text, timing.start_ms, timing.duration_ms))
    return tuple(merged)


def speak(text: str, path: Path, provider: str, voice: str,
          sounds: dict[str, str] | None = None) -> SpeechResult:
    """One piece of narration, with its names said as the pronunciation list says."""
    said, origin = respell(text, sounds or {})
    spoken = synthesise_narration(said, path, provider, voice)
    if said == " ".join(WORD.findall(text)):
        return spoken
    words = restore(spoken.words, origin)
    save_word_timings(path, words)
    return replace(spoken, words=words)


def speak_scenes(scenes: list[str], path: Path, provider: str, voice: str,
                 sounds: dict[str, str] | None = None,
                 pause_ms: int = SCENE_PAUSE_MS) -> SpeechResult:
    """A section, scene by scene, joined with a pause after every scene but the
    last; the word timings moved to where each word lands in the joined file."""
    scenes = [scene for scene in scenes if scene.strip()]
    if len(scenes) <= 1:
        return speak(" ".join(scenes), path, provider, voice, sounds)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SpeechFailed("ffmpeg is needed to join the narration of a section's scenes.")
    with tempfile.TemporaryDirectory() as folder:
        pieces = [speak(scene, Path(folder) / f"scene{index:03d}{path.suffix}", provider,
                        voice, sounds) for index, scene in enumerate(scenes)]
        words, offset = [], 0
        for index, piece in enumerate(pieces):
            words += [WordTiming(w.text, w.start_ms + offset, w.duration_ms) for w in piece.words]
            offset += piece.duration_ms + (pause_ms if index < len(pieces) - 1 else 0)
        inputs = [argument for piece in pieces for argument in ("-i", str(piece.audio_path))]
        padded = "".join(
            f"[{index}:a]aformat=sample_rates=24000:channel_layouts=mono"
            + (f",apad=pad_dur={pause_ms / 1000:.3f}" if index < len(pieces) - 1 else "")
            + f"[p{index}];" for index in range(len(pieces)))
        joined = "".join(f"[p{index}]" for index in range(len(pieces)))
        graph = padded + f"{joined}concat=n={len(pieces)}:v=0:a=1[out]"
        done = subprocess.run(
            [ffmpeg, "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]",
             "-ar", "24000", "-ac", "1", str(path)],
            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
        if done.returncode or not path.exists():
            raise SpeechFailed(f"The scenes' narration could not be joined: {done.stderr[-300:]}")
    words_tuple = tuple(words)
    save_word_timings(path, words_tuple)
    return replace(pieces[0], audio_path=path, duration_ms=measure_audio_duration_ms(path),
                   words=words_tuple)
