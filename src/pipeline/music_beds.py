"""The built-in music beds, made here in code: free to use, because nobody else made
them. Quiet, slow and unobtrusive by design -- a bed sits under a teacher's voice,
it is never a song.

Each is a loop of four chords, eight seconds each (A minor, F, C, G -- warm and
neither happy nor sad), that ends where it began, so the render can repeat it
under a video of any length without a seam:

- **calm**: a soft pad, every chord swelling in and out;
- **focus**: the pad, quieter, with a gentle arpeggio pulsing over it;
- **warm**: soft, piano-like chords, each struck and left to ring.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

CHORD_SECONDS = 8.0
# MIDI notes: A minor, F major, C major, G major, voiced close and low.
CHORDS = ((57, 60, 64), (53, 57, 60), (48, 52, 55, 60), (55, 59, 62))
BASS = (45, 41, 48, 43)
PEAK = 0.5                     # headroom: the render sets its level under the voice


def _hz(note: float) -> float:
    return 440.0 * 2 ** ((note - 69) / 12)


def _pad(note: float, t: np.ndarray, detune: float) -> np.ndarray:
    """A soft, slightly detuned tone with a few quiet overtones."""
    tone = np.zeros_like(t)
    for harmonic, weight in ((1, 1.0), (2, 0.25), (3, 0.08)):
        for cents in (-detune, detune):
            frequency = _hz(note) * harmonic * 2 ** (cents / 1200)
            tone += weight * np.sin(2 * np.pi * frequency * t)
    return tone


def _swell(length: int, rate: int, attack: float = 2.5, release: float = 2.5) -> np.ndarray:
    envelope = np.ones(length)
    rise, fall = int(attack * rate), int(release * rate)
    envelope[:rise] = np.sin(np.linspace(0, np.pi / 2, rise)) ** 2
    envelope[-fall:] = np.cos(np.linspace(0, np.pi / 2, fall)) ** 2
    return envelope


def _struck(note: float, t: np.ndarray, decay: float) -> np.ndarray:
    """A piano-like note: bright at the strike, mellowing as it rings."""
    tone = np.zeros_like(t)
    for harmonic, weight, fade in ((1, 1.0, 1.0), (2, 0.4, 1.6), (3, 0.18, 2.4), (4, 0.08, 3.2)):
        tone += weight * np.sin(2 * np.pi * _hz(note) * harmonic * t) * np.exp(-t * fade / decay)
    strike = np.minimum(1.0, t / 0.008)
    return tone * strike


def _chord_block(key: str, chord: tuple[int, ...], bass: int, rate: int) -> np.ndarray:
    """One chord's eight seconds, in stereo: (samples, 2)."""
    length = int(CHORD_SECONDS * rate)
    t = np.arange(length) / rate
    left, right = np.zeros(length), np.zeros(length)
    if key in ("calm", "focus"):
        envelope = _swell(length, rate)
        level = 1.0 if key == "calm" else 0.6
        for index, note in enumerate(chord):
            pan = 0.35 + 0.3 * index / max(1, len(chord) - 1)
            tone = _pad(note, t, detune=6 + index) * envelope * level
            left += tone * (1 - pan)
            right += tone * pan
        low = _pad(bass, t, detune=3) * envelope * 0.5 * level
        left, right = left + low, right + low
    if key == "focus":
        step = 0.375                         # an eighth note at 80 beats a minute
        pattern = [*chord, chord[1]]
        for count in range(int(CHORD_SECONDS / step)):
            start = int(count * step * rate)
            note = pattern[count % len(pattern)] + 12
            ring = t[: length - start]
            tone = _struck(note, ring, decay=0.6) * 0.22
            pan = 0.3 if count % 2 else 0.7
            left[start:] += tone * (1 - pan)
            right[start:] += tone * pan
    if key == "warm":
        for strike_at, voicing in ((0.0, chord), (4.0, chord[1:] + (chord[0] + 12,))):
            start = int(strike_at * rate)
            ring = t[: length - start]
            for index, note in enumerate(voicing):
                tone = _struck(note, ring, decay=2.2) * 0.5
                pan = 0.35 + 0.3 * index / max(1, len(voicing) - 1)
                left[start:] += tone * (1 - pan)
                right[start:] += tone * pan
            low = _struck(bass, ring, decay=3.0) * 0.45
            left[start:] += low
            right[start:] += low
    return np.column_stack([left, right])


def _soften(audio: np.ndarray, rate: int, cutoff: float = 2400.0) -> np.ndarray:
    """A gentle low-pass, so nothing in the bed competes with a voice's consonants."""
    alpha = 1 - np.exp(-2 * np.pi * cutoff / rate)
    out = np.empty_like(audio)
    state = audio[0].copy()
    for index in range(len(audio)):
        state += alpha * (audio[index] - state)
        out[index] = state
    return out


def make_bed(key: str, target: Path, rate: int) -> Path:
    """Write the bed `key` to `target` as a seamless stereo WAV loop."""
    import soundfile

    blocks = [_chord_block(key, chord, bass, rate) for chord, bass in zip(CHORDS, BASS,
                                                                           strict=True)]
    audio = np.concatenate(blocks)
    # The tail of the last chord rings into the start of the loop, as it would live.
    tail = int(1.5 * rate)
    ring = _chord_block(key, CHORDS[-1], BASS[-1], rate)[-tail:] if key == "warm" else None
    if ring is not None:
        audio[:tail] += ring * np.linspace(1, 0, tail)[:, None]
    audio = _soften(audio, rate)
    audio *= PEAK / max(1e-9, float(np.abs(audio).max()))
    soundfile.write(str(target), audio.astype(np.float32), rate, subtype="PCM_16")
    return target
