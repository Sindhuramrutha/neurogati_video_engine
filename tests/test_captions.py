"""Subtitles a viewer can read: two lines of 42 characters at most, breaking where
the phrase does, timed to the voice word by word."""

from pipeline.captions import MOST_LINE_CHARACTERS, section_cues
from pipeline.rendering import RenderedSection
from pipeline.speech import WordTiming

NARRATION = ("Let's start with a question that puzzled scientists for a long time. Is life "
             "only chemistry — or is there something electrical in it too? In 1771, Luigi "
             "Galvani noticed something strange: a dead frog's leg kicked when it was "
             "touched by an electric spark.")


def spoken(narration: str, together=("In", "1771,")) -> RenderedSection:
    """Timings as Edge reports them: no timing for a dash, and "In 1771" as one."""
    words, at, tokens = [], 0, narration.split()
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "—":
            index += 1
            continue
        if tuple(tokens[index:index + 2]) == together:
            words.append(WordTiming("In 1771", at, 600))
            index += 2
        else:
            words.append(WordTiming(token.strip(",.?:"), at, 280))
            index += 1
        at += 320
    return RenderedSection(section_id="s", title="t", narration=narration,
                           audio_duration_ms=at, words=tuple(words))


def test_cues_are_short_and_break_where_the_phrase_does():
    cues = section_cues(spoken(NARRATION))

    assert cues and all(len(line) <= MOST_LINE_CHARACTERS
                        for _, _, text in cues for line in text.split("\n"))
    assert all(text.count("\n") <= 1 for _, _, text in cues), "two lines at most"
    assert cues[0][2].replace("\n", " ").endswith("for a long time."), "a sentence ends a cue"
    assert any("—" in text for _, _, text in cues), "the dash is kept, joined to its word"
    assert all(later[0] >= earlier[1] for earlier, later in zip(cues, cues[1:], strict=False))


def test_a_voice_with_no_word_timings_keeps_the_older_cues():
    section = RenderedSection(section_id="s", title="t", narration=NARRATION,
                              audio_duration_ms=20000)
    assert section_cues(section) == []
