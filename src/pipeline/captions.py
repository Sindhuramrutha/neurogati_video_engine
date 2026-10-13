"""Subtitles a viewer can read: short cues, timed to the voice word by word.

A cue was a sentence or two -- 150 characters on screen at once, longer than
anyone reads while also watching. Broadcast practice, which this follows:

- at most two lines of 42 characters, split where the phrase breaks;
- a cue ends at a sentence's end, or at a comma once it is long enough, or
  after 6 seconds, whichever comes first;
- each stays up long enough to read at 17 characters a second (but never into
  the next one), and at least one second.

Timed from the voice's own word timings. A voice that reports none (the silent
voice) keeps the older cues, cut from the text (`rendering.section_segments`).
"""

from __future__ import annotations

MOST_LINE_CHARACTERS = 42
MOST_LINES = 2
LONGEST_CUE_MS = 6000
SHORTEST_CUE_MS = 1000
READING_CHARACTERS_PER_SECOND = 17
GAP_MS = 40
SENTENCE_ENDS = (".", "?", "!", ".\"", "?\"", "!\"", "”")
PHRASE_ENDS = (",", ";", ":", "—", "--")


def _timed_words(section) -> list[tuple[str, int, int]]:
    """The narration's words as written -- punctuation kept -- each with when it is
    said, in milliseconds from the start of the video. Empty when the timings
    do not line up with the words."""
    tokens: list[str] = []
    for token in section.narration.split():
        # A dash on its own is not said, so it has no timing: it joins the word before.
        if tokens and not any(character.isalnum() for character in token):
            tokens[-1] += " " + token
        else:
            tokens.append(token)
    start = section.start_ms + section.title_card_ms
    timed, at = [], 0
    for timing in section.words:
        size = max(1, len(timing.text.split()))
        if at + size > len(tokens):
            return []
        timed.append((" ".join(tokens[at:at + size]), start + timing.start_ms,
                      start + timing.end_ms))
        at += size
    return timed if timed and at == len(tokens) else []


def _two_lines(text: str) -> str:
    """One line, or two split at the space nearest the middle."""
    if len(text) <= MOST_LINE_CHARACTERS:
        return text
    middle = len(text) // 2
    spaces = [index for index, character in enumerate(text) if character == " "]
    split = min(spaces, key=lambda index: abs(index - middle), default=None)
    return text if split is None else text[:split] + "\n" + text[split + 1:]


def section_cues(section) -> list[tuple[int, int, str]]:
    """(start ms, end ms, text) for every cue of a section, or [] when the voice
    reported no word timings to cut them by."""
    words = _timed_words(section)
    if not words:
        return []
    cues: list[list] = []
    current: list[tuple[str, int, int]] = []

    def close() -> None:
        if current:
            cues.append([current[0][1], current[-1][2], " ".join(w for w, _, _ in current)])
            current.clear()

    for word in words:
        text = " ".join(w for w, _, _ in current)
        if current and (len(text) + 1 + len(word[0]) > MOST_LINE_CHARACTERS * MOST_LINES
                        or word[2] - current[0][1] > LONGEST_CUE_MS):
            close()
        current.append(word)
        text = " ".join(w for w, _, _ in current)
        if word[0].endswith(SENTENCE_ENDS) and len(text) >= 20:
            close()
        elif word[0].endswith(PHRASE_ENDS) and len(text) >= MOST_LINE_CHARACTERS:
            close()
    close()

    section_end = section.start_ms + section.total_ms
    for index, cue in enumerate(cues):
        readable = cue[0] + max(SHORTEST_CUE_MS,
                                round(len(cue[2]) / READING_CHARACTERS_PER_SECOND * 1000))
        limit = cues[index + 1][0] - GAP_MS if index + 1 < len(cues) else section_end
        cue[1] = max(cue[1], min(readable, limit))
    return [(start, end, _two_lines(text)) for start, end, text in cues]
