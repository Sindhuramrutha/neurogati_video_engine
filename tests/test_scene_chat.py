"""The scene panel's chat: each ask of a scene and how that making ended."""

from pipeline.scene_agent import conversation


def _event(kind, text, at="2026-10-25T10:00:00"):
    return {"kind": kind, "text": text, "at": at}


def test_each_ask_is_a_turn_with_how_it_ended():
    turns = conversation([
        _event("start", "Started."), _event("round", "Wrote the script."),
        _event("done", "Every check passed."),
        _event("start", "Make the title larger"),
        _event("done", "Every check passed; the reviewer still has remarks."),
    ])
    assert [turn["asked"] for turn in turns] == ["", "Make the title larger"]
    assert turns[1]["status"] == "done" and turns[1]["answer"].startswith("Every check")


def test_a_making_cut_off_by_a_later_one_reads_as_interrupted():
    turns = conversation([_event("start", "Darker background"), _event("start", "Started again.")])
    assert turns[0]["status"] == "stopped" and "Interrupted" in turns[0]["answer"]
    assert turns[1]["status"] == "working" and turns[1]["answer"] == ""


def test_errors_and_stops_before_starting_end_their_turn():
    turns = conversation([
        _event("start", "Add the cortex"), _event("note", "Stopped on an error: no model"),
        _event("stopped", "Stopped before it started."),
    ])
    assert turns[0]["status"] == "failed"
    assert turns[1] == turns[1] | {"asked": "", "status": "stopped"}
