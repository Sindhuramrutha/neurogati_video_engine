"""Whose voice the narration is in: the teacher's, not a reviewer's.

A finished video said "The chapter opens with a line from Plato", "This chapter
explores...", "The chapter asks...". The narrator was describing a book to the
viewer instead of teaching the viewer. It sounds like a summary read aloud,
because that is what it was: the Scripting agent was told to "rephrase source
content" and nothing said whose voice to say it in, so it reported on the source.

The narrator owns the material. It explains the ideas directly, as a good
teacher and a friendly explainer would, to "you". The source is where the
content came from, not something the video talks about.

Two things use this, so they cannot disagree:

- `VOICE_RULE`, given to the Scripting agent on every draft, whatever the tone;
- `reporting_phrases`, which finds narration that still speaks *about* the
  source as a document, for the check on Script & Staging. Naming the course or
  the part the viewer is watching is not that: it tells them where they are. A
  fixed pattern, so the same narration always gets the same answer.
"""

from __future__ import annotations

import re

VOICE_RULE = (
    "Voice: you are the teacher of this course, speaking directly to the viewer. Own the "
    "material and explain it yourself, the way a professional teacher and a friendly "
    "explainer would: address the viewer as \"you\", and use \"we\" and \"let's\" where it "
    "reads naturally. Let the viewer know where they are -- which course, which part, and "
    "what they will learn -- wherever that helps them. Never talk about the material as a "
    "document: do not say \"the slide\", \"the book\", \"the text\", \"the author\", \"the "
    "writer\", \"the passage\", \"the presentation\" or \"the document\", and never \"the "
    "chapter explores\", \"it opens with\", \"it asks\" or \"according to the ...\". State "
    "the ideas as true, in your own words. When the material quotes someone, credit that "
    "person (\"Plato wrote...\"). When it tells a story or a case, tell it yourself (\"Let "
    "me tell you about Padma.\")."
)

# The material spoken about as a document: "the book", "the author", "according to the
# text". Matched on whole words, case-insensitively. The course's own parts are not
# here: "in this chapter we'll see..." tells the viewer where they are, which they
# should know; "the chapter explores..." describes a document, and is.
_SOURCE_NOUNS = (
    "book|textbook|text|author|authors|writer|passage|reading|"
    "slide|slides|deck|presentation|document|lecture notes|article|paper"
)
# Not before a name or a title: "the writer Lewis Carroll", "the author of Alice in
# Wonderland" credit a person, as the narrator is told to; "the writer says" speaks
# about the source.
REPORTING = re.compile(
    rf"\b(?:the|this|that|our)\s+(?:{_SOURCE_NOUNS})\b(?!\s+(?:of\s+)?(?-i:[A-Z]))"
    rf"|\b(?:the|this)\s+chapters?\s+(?:explores?|opens?|asks?|says?|tells?|describes?|"
    rf"discuss(?:es)?|shows?|covers?|begins?|looks at)\b"
    rf"|\baccording to (?:the|this)\b",
    re.IGNORECASE,
)


def reporting_phrases(text: str) -> list[str]:
    """Each place the narration speaks about the source, with a little context."""
    found = []
    for match in REPORTING.finditer(text):
        start = max(0, match.start() - 25)
        end = min(len(text), match.end() + 35)
        found.append(("…" if start else "") + text[start:end].replace("\n", " ").strip()
                     + ("…" if end < len(text) else ""))
    return found
