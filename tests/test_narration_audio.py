"""Narration as it is spoken: names respelled for the voice and given back their
spelling in the timings, and a breath between the scenes of a section."""

import shutil

import pytest

from pipeline.narration_audio import SCENE_PAUSE_MS, respell, restore, speak_scenes
from pipeline.speech import WordTiming


def test_a_name_is_respelled_for_the_voice_and_spelled_right_in_the_timings():
    said, origin = respell("Otto Loewi, in 1921, proved it.", {"loewi": "Ler vee"})
    assert said == "Otto Ler vee, in 1921, proved it."

    heard = tuple(WordTiming(word.strip(",."), index * 300, 250)
                  for index, word in enumerate(said.split()))
    words = restore(heard, origin)

    assert [w.text for w in words] == ["Otto", "Loewi", "in", "1921", "proved", "it"]
    loewi = words[1]
    assert (loewi.start_ms, loewi.end_ms) == (300, 850), "both parts, one word"


def test_a_repeated_word_is_not_merged_and_a_different_split_is_left_alone():
    said, origin = respell("very very old", {})
    heard = tuple(WordTiming(w, i * 200, 150) for i, w in enumerate(said.split()))
    assert [w.text for w in restore(heard, origin)] == ["very", "very", "old"]
    assert restore(heard[:2], origin) == heard[:2], "counts differ: nothing is guessed"


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="needs ffmpeg")
def test_a_section_is_spoken_scene_by_scene_with_a_breath_between(tmp_path):
    from pipeline.speech import measure_audio_duration_ms, synthesise_narration

    one = synthesise_narration("First scene words here.", tmp_path / "a.mp3", "silent")
    two = synthesise_narration("Second scene.", tmp_path / "b.mp3", "silent")

    joined = speak_scenes(["First scene words here.", "Second scene."],
                          tmp_path / "audio" / "section.mp3", "silent", "")  # no folder yet

    expected = one.duration_ms + SCENE_PAUSE_MS + two.duration_ms
    assert abs(measure_audio_duration_ms(joined.audio_path) - expected) < 120


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="needs ffmpeg")
def test_each_scene_is_followed_by_the_pause_the_plan_gave_it(tmp_path):
    """The planner decides the quiet after each scene: none where the thought runs on,
    up to two seconds after a section's last scene -- the quiet before the next."""
    from pipeline.speech import measure_audio_duration_ms, synthesise_narration

    lines = ["First scene words here.", "Second scene.", "Third and last."]
    alone = [synthesise_narration(line, tmp_path / f"{n}.mp3", "silent").duration_ms
             for n, line in enumerate(lines)]

    joined = speak_scenes(lines, tmp_path / "section.mp3", "silent", "",
                          pauses_ms=[1500, 0, 2000])

    assert abs(measure_audio_duration_ms(joined.audio_path)
               - (sum(alone) + 1500 + 2000)) < 150


def test_a_scene_is_cut_to_its_speech_before_the_pause_is_added():
    """The voice's own silence at both ends of each scene doubled v9's pauses: a planned
    second was heard as two. The kept span is the speech and a short edge."""
    from pathlib import Path

    from pipeline.narration_audio import EDGE_AFTER_MS, EDGE_BEFORE_MS, _speech_span
    from pipeline.speech import SpeechResult

    piece = SpeechResult(audio_path=Path("x.mp3"), duration_ms=6_000, provider_key="edge",
                         voice="v", words=(WordTiming("One", 400, 300),
                                           WordTiming("two", 900, 400)))
    assert _speech_span(piece) == (400 - EDGE_BEFORE_MS, 1300 + EDGE_AFTER_MS)
    silent = SpeechResult(audio_path=Path("x.mp3"), duration_ms=6_000, provider_key="silent",
                          voice="")
    assert _speech_span(silent) == (0, 6_000), "no timings: nothing cut"
