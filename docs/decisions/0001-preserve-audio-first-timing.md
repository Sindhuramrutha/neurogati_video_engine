# ADR 0001 — Preserve audio-first timing

## Status

**Proposed.**

## Context

v1 synthesises narration audio *before* any visual work, extracts word-level
timings, and derives both animation beats and subtitles from that single
measurement.

This is v1's strongest design decision. It makes synchronisation structural rather
than corrected after the fact: because animation timing and subtitle timing come
from the same source, they cannot drift relative to each other.

A rewrite framed as "v1 is mid" risks discarding this along with the parts that
genuinely failed. The [post-mortem](../diagnosis/v1-postmortem.md) locates v1's
failures in scene generation and transport — **not** in the timing model.

## Decision

Preserve audio-first timing in v2, unchanged in principle:

1. Synthesise narration per scene
2. Extract word-level timings
3. Derive animation beats from those timings
4. Derive subtitles from the same timings
5. Length-lock composed output to audio duration

Two improvements, without altering the principle:

**Beat durations become computed data, not model arithmetic.** In v1 the model
sums `run_time` and `self.wait()` values and must land within tolerance — a
recurring failure (55.6s vs 52.3s; 60.2s vs 56.5s in production history). If beats
are structured data with timestamps from the word timings, the system computes
durations and the mismatch becomes unrepresentable.

**Consider true forced alignment.** v1 uses Whisper ASR, which transcribes rather
than aligns, and its own docstring notes domain terms are sometimes mis-transcribed.
Since these timings drive beats *and* subtitles, this is load-bearing. WhisperX or
a comparable aligner would improve reliability. Not required for the principle;
worth evaluating.

## Consequences

**Positive**

- Sync remains structural
- Subtitles remain free
- Timing errors detectable early by comparing computed duration to measured audio
- With beats as data, the most common v1 timing failure disappears

**Negative**

- Audio must complete before visual work; no parallelising across those stages
- TTS and alignment model weights required (~330 MB first run)
- Alignment quality bounds timing quality

**Follow-on**

Because composition length-locks to audio, an over-long animation would be
silently trimmed. v1 correctly checks duration in *both* directions. v2 must
preserve that check, or make overshoot impossible by construction.

## Revisit if

A different narration source appears — human voiceover, or pre-recorded audio.
The principle still holds (audio is the clock), but the synthesis step changes.
