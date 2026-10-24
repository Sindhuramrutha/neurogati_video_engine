"""A script is drafted, and its length checked, at the pace its voice really speaks."""

from pipeline import voice_pace
from pipeline.scripting import estimate_seconds


def test_a_voice_s_own_pace_is_used_once_enough_of_it_is_heard():
    """v9 was drafted at an assumed 150 words a minute and spoken at about 140:
    38 minutes on paper, 41.8 in the video."""
    text = " ".join(["word"] * 140)
    assert estimate_seconds(text) == 56, "150 a minute, assumed, before any is heard"

    voice_pace.record("en-IN-NeerjaNeural", 140, 50_000)        # under a minute heard
    assert voice_pace.words_per_minute("en-IN-NeerjaNeural") == 150

    for _ in range(5):                                           # 5 minutes heard
        voice_pace.record("en-IN-NeerjaNeural", 140, 60_000)
    pace = voice_pace.words_per_minute("en-IN-NeerjaNeural")
    assert abs(pace - 840 / (350 / 60)) < 0.5, "every scene heard, the first included"
    assert estimate_seconds(text) == round(140 / pace * 60), "the voice heard last"
    assert voice_pace.words_per_minute("another-voice") == 150


def test_a_measurement_past_belief_is_not_used():
    for _ in range(4):
        voice_pace.record("broken", 1000, 60_000)                 # 1000 words a minute
    assert voice_pace.words_per_minute("broken") == 150
