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
                          tmp_path / "section.mp3", "silent", "")

    expected = one.duration_ms + SCENE_PAUSE_MS + two.duration_ms
    assert abs(measure_audio_duration_ms(joined.audio_path) - expected) < 120
