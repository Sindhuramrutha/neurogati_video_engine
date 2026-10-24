"""What the script's checks report is what the narration says now."""

from types import SimpleNamespace

from pipeline.narration_voice import reporting_phrases
from pipeline.script_handoff import _still_said


def test_crediting_a_named_writer_is_the_teacher_s_voice():
    """v8 flagged "The writer Lewis Carroll": a person credited, as the narrator is told
    to do. Speaking of the source is still caught."""
    assert reporting_phrases("The writer Lewis Carroll asked a question.") == []
    assert reporting_phrases("Carroll, the author of Alice in Wonderland, wrote it.") == []
    assert reporting_phrases("As the author of the passage says, it is so.")
    assert reporting_phrases("As the writer says, the brain is complex.")
    # Naming the part of the course tells the viewer where they are; describing the
    # chapter as a document does not teach.
    assert reporting_phrases("In this chapter we look at the brain.") == []
    assert reporting_phrases("This chapter explores the brain.")


def test_a_claim_lapses_once_its_sentence_is_rewritten():
    """v8's two corrected sentences were still listed as wrong after the fix."""
    entry = SimpleNamespace(body="", scenes=[SimpleNamespace(
        narration="He timed how fast a signal travels along a nerve.")])
    gone = "scene 5: 'He used the wave reasoning of light' -- it carries the anachronism"
    kept = "scene 5: 'how fast a signal travels' -- check the date"
    assert not _still_said(gone, entry)
    assert _still_said(kept, entry)
    assert _still_said("a claim quoting nothing", entry)
