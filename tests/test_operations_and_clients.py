"""The shared core, and the three clients that must not drift from it.

The point of `pipeline.operations` is that the browser, the CLI and MCP produce
identical results. These tests assert that directly rather than testing each
client separately and hoping.
"""

import json
from pathlib import Path

import pytest

from pipeline import operations, render_records
from pipeline.operations import OperationFailed


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    """Point every operation at a temporary projects directory.

    `get_settings` is cached for the process, so clearing it is what actually
    redirects the writes -- without it these tests would edit real projects.
    """
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def test_a_project_round_trips_through_operations(project_root):
    created = operations.create_project("Gradient Descent")
    assert created["slug"] == "gradient-descent"
    assert [p["slug"] for p in operations.list_projects()] == ["gradient-descent"]


def test_an_unknown_project_names_the_ones_that_exist(project_root):
    """An error a model can act on beats an error it can only report."""
    operations.create_project("Real Project")

    with pytest.raises(OperationFailed) as failure:
        operations.read_artifact("imaginary", "plan")

    assert "real-project" in str(failure.value)


def test_an_unknown_artifact_names_the_valid_ones(project_root):
    operations.create_project("P")
    with pytest.raises(OperationFailed) as failure:
        operations.read_artifact("p", "nonsense")

    message = str(failure.value)
    for artifact_name in ("plan", "script", "composition", "review"):
        assert artifact_name in message


def test_script_audit_sees_the_plan(project_root):
    """The bug this fixture of a test exists for.

    `Script.to_dict()` cannot compute "orphaned" without the plan's section ids.
    The web routes passed them and `operations` did not, so a script written from
    the CLI came back claiming every section was orphaned -- noise that would send
    someone hunting a bug in their own data.
    """
    operations.create_project("Audit Check")
    plan = operations.add_plan_section("audit-check", title="Only section")
    section_id = plan["sections"][0]["id"]

    script = operations.write_section_script("audit-check", section_id, "Some narration.")

    assert script["audit"]["orphaned_section_ids"] == []
    assert script["audit"]["unwritten_section_ids"] == []
    assert "plan_sections" in script, "the script must carry the plan it was audited against"


def test_writing_a_script_for_an_unknown_section_is_refused(project_root):
    """An invented section id is a mistake, not an edit.

    The model would happily store it -- orphaned scripts are kept on purpose so
    deleting a plan section does not destroy its writing -- but an agent should
    hear about this immediately rather than through a warning three stages later.
    """
    operations.create_project("Strict")
    operations.add_plan_section("strict", title="Real section")

    with pytest.raises(OperationFailed) as failure:
        operations.write_section_script("strict", "invented-id", "text")

    assert "Real section" in str(failure.value), "the error should list the real sections"


def test_review_presentation_includes_the_transcript(project_root):
    operations.create_project("Review Context")
    plan = operations.add_plan_section("review-context", title="Intro", estimated_seconds=60)
    operations.write_section_script(
        "review-context", plan["sections"][0]["id"], "Hello and welcome."
    )

    review = operations.add_review_comment(
        "review-context", body="Too fast", routed_to_stage="scripting"
    )

    assert review["audit"]["by_stage"] == {"script-staging": 1}
    assert [entry["body"] for entry in review["transcript"]] == ["Hello and welcome."]


def test_routing_to_an_unknown_stage_lists_the_real_ones(project_root):
    operations.create_project("Routing")
    with pytest.raises(OperationFailed) as failure:
        operations.add_review_comment("routing", body="x", routed_to_stage="nowhere")

    assert "script-staging" in str(failure.value)


def test_values_are_clamped_not_rejected(project_root):
    """A caller cannot escape validation by choosing a different interface."""
    operations.create_project("Clamp")
    plan = operations.add_plan_section("clamp", title="Absurd", estimated_seconds=10**9)

    assert plan["sections"][0]["estimated_seconds"] < 10**9
    assert plan["warnings"], "an absurd duration should be flagged, not silently kept"


def test_the_web_and_the_shared_core_return_the_same_document(project_root):
    """The anti-drift test.

    If a route ever reassembles a response itself instead of calling
    `present_artifact`, this fails -- which is exactly how the orphan bug got in.
    """
    from litestar.testing import TestClient

    from pipeline.web.app import create_app

    operations.create_project("Parity")
    plan = operations.add_plan_section("parity", title="Section one")
    operations.write_section_script("parity", plan["sections"][0]["id"], "Narration.")

    with TestClient(app=create_app()) as client:
        for artifact_name in ("plan", "script", "composition", "review"):
            over_http = client.get(f"/api/projects/parity/{artifact_name}").json()
            through_core = operations.read_artifact("parity", artifact_name)
            assert over_http == through_core, (
                f"the {artifact_name} route has drifted from operations.present_artifact"
            )


# --- the MCP server ---------------------------------------------------------


def test_every_mcp_tool_is_a_wrapper_over_operations():
    """MCP must not become a fourth place where pipeline logic lives."""
    import inspect

    from pipeline import mcp_server

    source = inspect.getsource(mcp_server)
    assert "PlanStore" not in source, "MCP is reaching past operations into a store"
    assert "ScriptStore" not in source
    assert "CompositionStore" not in source


def test_no_mcp_tool_can_reach_a_credential():
    """An agent should be able to drive the pipeline without ever being in a
    position to read the provider key."""
    import inspect

    from pipeline import mcp_server

    source = inspect.getsource(mcp_server)
    assert "describe_credentials" not in source
    assert "save_credentials" not in source
    assert "llm_api_key" not in source


async def test_mcp_tools_are_registered():
    from pipeline.mcp_server import server

    tools = await server.list_tools()
    names = {tool.name for tool in tools}

    for expected in ("describe_stages", "list_projects", "read_artifact",
                     "write_artifact", "add_plan_section", "write_section_script",
                     "ask_stage_agent", "draft_plan", "model_status"):
        assert expected in names, f"{expected} is not exposed over MCP"


# --- the CLI ----------------------------------------------------------------


def run_cli(argv, capsys):
    """Invoke the CLI in-process and return (exit_code, parsed stdout)."""
    import sys

    from pipeline.cli import main

    original_argv = sys.argv
    sys.argv = ["pipeline", *argv]
    try:
        code = main()
    finally:
        sys.argv = original_argv

    captured = capsys.readouterr()
    parsed = json.loads(captured.out) if captured.out.strip() else None
    return code, parsed, captured.err


def test_cli_prints_json_and_exits_zero(project_root, capsys):
    code, payload, _ = run_cli(["projects", "create", "From The CLI"], capsys)
    assert code == 0
    assert payload["slug"] == "from-the-cli"


def test_cli_failure_goes_to_stderr_and_exits_nonzero(project_root, capsys):
    """stdout is promised to be JSON. A caller piping into `jq` must not receive
    an error message there."""
    code, payload, errors = run_cli(["show", "ghost", "plan"], capsys)

    assert code == 1
    assert payload is None, "nothing should be written to stdout on failure"
    assert "ghost" in errors


def test_cli_pretty_flag_works_after_the_subcommand(project_root, capsys):
    """argparse only accepts a top-level flag before the subcommand, but everyone
    writes a trailing flag. Both positions must work."""
    run_cli(["projects", "create", "Flags"], capsys)

    _, _, _ = run_cli(["--pretty", "show", "flags", "plan"], capsys)
    leading = capsys.readouterr()

    run_cli(["show", "flags", "plan", "--pretty"], capsys)
    trailing = capsys.readouterr()

    assert leading.out == trailing.out


def test_cli_and_operations_agree(project_root, capsys):
    operations.create_project("Agreement")
    operations.add_plan_section("agreement", title="A section")

    _, from_cli, _ = run_cli(["show", "agreement", "plan"], capsys)
    assert from_cli == operations.read_artifact("agreement", "plan")


def test_default_track_ids_are_stable_across_reads(project_root):
    """The read-then-write an agent always does.

    A default composition is rebuilt on every read until something saves it. With
    generated ids, reading the timeline twice returned two different sets, so
    `read composition -> take a track id -> add a clip to it` failed with "no such
    track". The browser hid it by rendering and posting within one load; an agent
    hits it every time.
    """
    operations.create_project("Stable Ids")

    first = operations.read_artifact("stable-ids", "composition")
    second = operations.read_artifact("stable-ids", "composition")

    assert [t["id"] for t in first["tracks"]] == [t["id"] for t in second["tracks"]]

    # And the id from a read must actually be usable.
    composition = operations.add_clip(
        "stable-ids", track_id=first["tracks"][0]["id"], kind="text",
        label="From an agent", start_ms=0, duration_ms=2000, text="Hello",
    )
    assert composition["clip_count"] == 1


def test_to_dict_is_json_native(project_root):
    """Enums must serialise as strings, or the CLI and MCP hand a model
    `TrackKind.VIDEO` where the web hands it `"video"`."""
    operations.create_project("Json Native")
    composition = operations.read_artifact("json-native", "composition")

    for track in composition["tracks"]:
        assert isinstance(track["kind"], str), f"{track['kind']!r} is not JSON-native"

    json.dumps(composition)  # would raise on a non-serialisable value


def test_every_stage_reaches_the_ask_route(project_root):
    """A literal path segment must never shadow the {stage} parameter.

    `draft_plan` briefly lived at `/agent/planning/draft-plan`. The literal
    `planning` sat exactly where `/agent/{stage}/ask` expects a parameter, so
    Litestar routed `/agent/planning/ask` down the literal branch and returned
    404 -- for the planning stage only. Every other stage worked, which is the
    kind of asymmetry nobody notices until the one broken case is the one they
    need.

    400 is the expected status here: the route is reached and refuses because no
    API key is configured in the test environment. 404 means it was not reached.
    """
    from litestar.testing import TestClient

    from pipeline.web.app import create_app

    operations.create_project("Routing Shadow")

    with TestClient(app=create_app()) as client:
        for stage in ("extraction", "planning", "scripting", "studio", "reviewing"):
            response = client.post(
                f"/api/projects/routing-shadow/agent/{stage}/ask",
                json={"question": "anything"},
            )
            assert response.status_code != 404, (
                f"the {stage} stage does not reach the ask route -- "
                f"a literal path segment is shadowing {{stage}}"
            )


# A structural "no literal segment may shadow a parameter" test was tried here
# and removed. Litestar's own /schema/swagger sits beside /schema/{path:str} and
# works, so the rule condemned correct routing; the mechanism is narrower than it
# looked. `test_every_stage_reaches_the_ask_route` above tests the behaviour that
# actually broke, and a test that keeps flagging correct code is worse than none.


# --- serving rendered media -------------------------------------------------


def test_range_header_parsing():
    """A media element opens with a Range request before it plays anything."""
    from pipeline.web.routes_project import parse_range_header

    assert parse_range_header("bytes=0-1023", 10_000) == (0, 1023)
    assert parse_range_header("bytes=500-", 10_000) == (500, 9_999)
    assert parse_range_header("bytes=-500", 10_000) == (9_500, 9_999)
    # An end past the file is clamped, not refused.
    assert parse_range_header("bytes=9000-99999", 10_000) == (9_000, 9_999)

    # Anything unusable falls back to a normal 200 rather than erroring: the
    # client survives without the header, and refusing would break playback.
    for unusable in ("", "items=0-10", "bytes=abc-def", "bytes=20000-30000", "bytes=-0"):
        assert parse_range_header(unusable, 10_000) is None, unusable


def test_rendered_media_is_served_with_range_support(project_root):
    """The bug that made a finished video refuse to play.

    Returning the bytes as a flat 200 meant no `Accept-Ranges` and no 206, so a
    <video> element had no way to seek and simply showed nothing. The file was
    fine; the response was not.
    """
    from litestar.testing import TestClient

    import pipeline.web.routes_project as routes_project_module
    from pipeline.web.app import create_app

    routes_project_module._service = None
    operations.create_project("Media Serving")

    output_directory = project_root / "media-serving" / "reviewing" / "output"
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / "clip.mp4").write_bytes(b"0123456789" * 100)

    with TestClient(app=create_app()) as client:
        full = client.get("/api/projects/media-serving/output/clip.mp4")
        assert full.status_code == 200
        assert full.headers["accept-ranges"] == "bytes"
        assert full.headers["content-type"].startswith("video/mp4")
        # attachment would download the file instead of playing it.
        assert full.headers["content-disposition"].startswith("inline")

        partial = client.get(
            "/api/projects/media-serving/output/clip.mp4",
            headers={"Range": "bytes=0-9"},
        )
        assert partial.status_code == 206
        assert partial.headers["content-range"] == "bytes 0-9/1000"
        assert partial.content == b"0123456789"

    routes_project_module._service = None


def test_output_route_refuses_to_escape_the_output_directory(project_root):
    """The upload hole pointing the other way."""
    from litestar.testing import TestClient

    import pipeline.web.routes_project as routes_project_module
    from pipeline.web.app import create_app

    routes_project_module._service = None
    operations.create_project("Escape Attempt")
    (project_root / "escape-attempt" / "reviewing" / "output").mkdir(parents=True)

    with TestClient(app=create_app()) as client:
        for payload in ("../../project.json", "..%2F..%2Fproject.json", "....//project.json"):
            response = client.get(f"/api/projects/escape-attempt/output/{payload}")
            assert response.status_code == 404, f"{payload} was not refused"

    routes_project_module._service = None


# --- render timing: one clock for picture, subtitles and timeline -------------


def test_section_segments_are_one_exact_clock():
    """Picture, subtitles and the Studio timeline all read these segments.

    Before this there were three formulas: slides split evenly for the picture
    and by text length for the subtitles, narration muxed under the title card
    while subtitles assumed it started after, and sections overrunning by 2-6s.
    By the end of an 8-minute video the captions were ~20 seconds off.
    """
    from pipeline.rendering import (
        SECTION_TAIL_MS,
        TITLE_CARD_MS,
        RenderedSection,
        section_segments,
    )

    narration = "First point here. A second, noticeably longer sentence follows it. Third. " * 8
    section = RenderedSection("s1", "A title", narration,
                              audio_duration_ms=64_703, start_ms=12_345, is_opening=True)
    segments = section_segments(section)

    assert segments[0].kind == "title"
    assert segments[0].start_ms == 12_345
    assert segments[1].start_ms == 12_345 + TITLE_CARD_MS, "narration must start after the card"
    assert all(a.end_ms == b.start_ms for a, b in zip(segments, segments[1:], strict=False)), \
        "segments must be contiguous"
    assert segments[-1].end_ms == 12_345 + section.total_ms, "must end on the section length"
    assert sum(s.duration_ms for s in segments if s.kind == "slide") \
        == 64_703 + SECTION_TAIL_MS


def test_only_the_opening_section_holds_a_title_card():
    """A card before every section was 2.5 seconds of silence each time -- on a
    ten-section video, most of a minute spent reading names that are already on
    the frames."""
    from pipeline.rendering import RenderedSection, section_segments

    narration = "A sentence of narration. And one more after it."
    later = RenderedSection("s2", "Later", narration,
                            audio_duration_ms=6_000, start_ms=30_000)
    segments = section_segments(later)

    assert "title" not in [s.kind for s in segments], "no card before a later section"
    assert segments[0].start_ms == 30_000, "the voice starts the moment the section does"
    assert later.total_ms < 6_000 + 1_000, "no card, so almost nothing but the narration"


def test_the_cues_break_where_the_voice_says_they_do():
    """A provider that reports word boundaries is telling us exactly where each
    word landed. Splitting by character count instead put the cut up to a
    sentence away from the word it belongs to."""
    from pipeline.rendering import RenderedSection, section_segments
    from pipeline.speech import WordTiming

    # Two sentences, each long enough to need a cue of its own, and the same
    # length so a character-count split would put the break at the halfway mark.
    first = " ".join(["alpha"] * 30) + "."
    second = " ".join(["beta"] * 30) + "."
    narration = f"{first} {second}"
    words = narration.replace(".", "").split()

    # The voice hurried the first sentence and dwelt on the second, so where it
    # really broke is nowhere near the middle of the audio.
    timings = tuple(
        WordTiming(text=word, start_ms=at * 100 if at < 30 else 3_000 + (at - 30) * 300,
                   duration_ms=80)
        for at, word in enumerate(words)
    )
    section = RenderedSection("s1", "Counting", narration,
                              audio_duration_ms=12_000, words=timings)
    cues = [s for s in section_segments(section) if s.kind == "slide"]

    assert len(cues) == 2
    # The second cue starts on its own first word, at three seconds -- not at
    # the share of the characters, which would have put it at six.
    assert cues[1].start_ms == 3_000
    assert cues[0].duration_ms == 3_000


def test_bad_word_timings_fall_back_to_the_text_rather_than_breaking_the_clock():
    """Timings that disagree with the narration would slide every cue along by
    the difference, which is worse than not using them."""
    from pipeline.rendering import RenderedSection, section_segments
    from pipeline.speech import WordTiming

    narration = "One two three. Four five six seven eight nine ten."
    # Half the words, as a provider that split differently would report.
    timings = tuple(WordTiming(text="x", start_ms=at * 500, duration_ms=200)
                    for at in range(5))
    section = RenderedSection("s1", "Counting", narration,
                              audio_duration_ms=14_000, words=timings)
    segments = section_segments(section)

    assert all(s.duration_ms > 0 for s in segments)
    assert segments[-1].end_ms == section.total_ms


def test_one_scene_is_one_shot_however_many_cues_it_needs():
    """The picture changes when the scene changes, not when the text does. Three
    cues of one scene used to be three encodes with the camera restarting on
    each, which is the carousel one level down."""
    from pipeline.rendering import RenderedSection, section_segments, shot_windows

    section = RenderedSection(
        "s1", "Signals",
        narration="A long first scene. " * 20 + "\n\nA second scene.",
        audio_duration_ms=40_000,
    )
    cues = [s for s in section_segments(section) if s.kind == "slide"]
    windows = shot_windows(section)

    assert len([cue for cue in cues if cue.scene_index == 0]) > 1, \
        "the first scene should need more than one cue"
    assert [window.scene_index for window in windows] == [0, 1]
    assert sum(window.duration_ms for window in windows) == section.total_ms
    assert windows[0].duration_ms == sum(
        cue.duration_ms for cue in cues if cue.scene_index == 0)


def test_a_label_appears_on_the_word_that_names_it():
    """The reason for having word timings at all: the label lands as it is said,
    rather than all four arriving at once, which is a slide."""
    from pipeline.rendering import RenderedSection, reveal_times, shot_windows
    from pipeline.speech import WordTiming

    narration = "The amplifier boosts it and the filter removes the noise."
    words = narration.rstrip(".").split()
    timings = tuple(WordTiming(text=word, start_ms=at * 500, duration_ms=400)
                    for at, word in enumerate(words))
    section = RenderedSection("s1", "Chain", narration,
                              audio_duration_ms=len(words) * 500, words=timings)
    window = shot_windows(section)[0]

    at = reveal_times(section, window, ["amplifier", "filter"])

    # "amplifier" is word 1 (500ms) and "filter" is word 6 (3000ms), each less
    # the lead time.
    assert at[0] == 500 - 120
    assert at[1] == 3_000 - 120


def test_labels_never_appear_out_of_order_or_after_the_shot_ends():
    from pipeline.rendering import RenderedSection, reveal_times, shot_windows

    section = RenderedSection("s1", "Chain", "A short scene here.",
                              audio_duration_ms=2_000)
    window = shot_windows(section)[0]

    at = reveal_times(section, window, ["one", "two", "three", "four"])

    assert at == sorted(at), "a label above one already on screen reads as a glitch"
    assert all(when < window.duration_ms for when in at)


def test_a_cross_fade_is_dropped_rather_than_made_a_flicker():
    """Every shot is encoded a fade longer than its slot so the dissolve is paid
    for; a shot too short for that is cut to instead."""
    from pipeline.rendering import CROSS_FADE_MS, _cross_fade_ms

    assert _cross_fade_ms([8_000]) == 0, "one shot has nothing to dissolve into"
    assert _cross_fade_ms([8_000, 6_000]) == CROSS_FADE_MS
    assert _cross_fade_ms([8_000, 600]) == 200, "shortened to fit the shortest shot"
    assert _cross_fade_ms([8_000, 200]) == 0, "too short to be anything but a flicker"


def test_a_section_without_narration_is_just_its_title_card():
    from pipeline.rendering import TITLE_CARD_MS, RenderedSection, section_segments

    segments = section_segments(RenderedSection("s", "Only a title", "", start_ms=0))
    assert [s.kind for s in segments] == ["title"]
    assert segments[0].duration_ms == TITLE_CARD_MS


def _rendered_section(audio_path):
    from pipeline.rendering import RenderedSection

    return RenderedSection(
        "s1", "Section title", "One sentence. Another sentence.",
        audio_path=audio_path, audio_duration_ms=6_000, start_ms=0,
    )


def test_render_writes_its_structure_onto_an_empty_timeline(project_root, tmp_path):
    operations.create_project("Timeline Fill")
    project = operations.require_project("timeline-fill")
    audio = tmp_path / "section-00.mp3"
    audio.write_bytes(b"x")

    note = render_records.write_timeline_from_render(project, [_rendered_section(audio)])
    composition = operations.read_artifact("timeline-fill", "composition")

    assert note == ""
    assert composition["generated_from_render_at"]
    kinds = {t["kind"]: [c["kind"] for c in t["clips"]] for t in composition["tracks"]}
    assert kinds["video"] == ["scene"]
    assert kinds["text"] and set(kinds["text"]) == {"text"}
    assert kinds["audio"] == ["audio"]
    audio_clip = next(t for t in composition["tracks"] if t["kind"] == "audio")["clips"][0]
    assert audio_clip["asset_id"] == "section-00.mp3", "the timeline must name a file, never a path"


def test_render_never_overwrites_hand_made_clips(project_root, tmp_path):
    """Replacing someone's editing to display the renderer's output would destroy
    their work, silently."""
    operations.create_project("Hand Made")
    composition = operations.read_artifact("hand-made", "composition")
    operations.add_clip("hand-made", track_id=composition["tracks"][1]["id"],
                        kind="text", label="Mine", text="I placed this")

    audio = tmp_path / "section-00.mp3"
    audio.write_bytes(b"x")
    project = operations.require_project("hand-made")
    note = render_records.write_timeline_from_render(project, [_rendered_section(audio)])

    after = operations.read_artifact("hand-made", "composition")
    labels = [c["label"] for t in after["tracks"] for c in t["clips"]]
    assert labels == ["Mine"], "the hand-made clip must be the only clip left"
    assert "your own edits" in note


def test_a_render_generated_timeline_is_replaced_by_the_next_render(project_root, tmp_path):
    operations.create_project("Rerender")
    project = operations.require_project("rerender")
    audio = tmp_path / "section-00.mp3"
    audio.write_bytes(b"x")

    render_records.write_timeline_from_render(project, [_rendered_section(audio)])
    first_count = operations.read_artifact("rerender", "composition")["clip_count"]
    note = render_records.write_timeline_from_render(project, [_rendered_section(audio)])

    assert note == ""
    assert operations.read_artifact("rerender", "composition")["clip_count"] == first_count, \
        "a re-render replaces its own timeline rather than stacking a second copy"


def test_narration_route_streams_and_refuses_to_escape(project_root):
    from litestar.testing import TestClient

    import pipeline.web.routes_project as routes_project_module
    from pipeline.web.app import create_app

    routes_project_module._service = None
    operations.create_project("Narration Serving")
    audio_directory = project_root / "narration-serving" / "reviewing" / "output" / "audio"
    audio_directory.mkdir(parents=True)
    (audio_directory / "section-00.mp3").write_bytes(b"ID3" + b"\x00" * 997)

    with TestClient(app=create_app()) as client:
        ranged = client.get("/api/projects/narration-serving/narration/section-00.mp3",
                            headers={"Range": "bytes=0-99"})
        assert ranged.status_code == 206
        assert ranged.headers["content-type"].startswith("audio/mpeg")

        for payload in ("../../project.json", "..%2F..%2F..%2Fproject.json"):
            escaped = client.get(f"/api/projects/narration-serving/narration/{payload}")
            assert escaped.status_code == 404, payload

    routes_project_module._service = None


def test_chapters_follow_the_rendered_video_not_the_plan_estimate(project_root, tmp_path):
    """Chapters are navigation, and these pointed at the wrong places.

    The plan's `estimated_seconds` are a guess made before any narration exists.
    Seeding from them put chapter 5 at 5:30 for a section that really starts at
    7:19 -- 109 seconds out on an 8-minute video. A render knows the measured
    positions, so once one exists the chapters come from it.
    """
    operations.create_project("Chapter Times")
    # The plan guesses 60s per section...
    first = operations.add_plan_section("chapter-times", title="One", estimated_seconds=60)
    operations.add_plan_section("chapter-times", title="Two", estimated_seconds=60)
    for section in operations.read_artifact("chapter-times", "plan")["sections"]:
        operations.write_section_script("chapter-times", section["id"], "Some narration here.")

    project = operations.require_project("chapter-times")
    assert first  # the plan exists

    # ...but the render measured something quite different.
    audio = tmp_path / "section-00.mp3"
    audio.write_bytes(b"x")
    from pipeline.rendering import RenderedSection

    sections = [
        RenderedSection("a", "One", "A sentence.", audio_path=audio,
                        audio_duration_ms=90_000, start_ms=0),
        RenderedSection("b", "Two", "Another sentence.", audio_path=audio,
                        audio_duration_ms=40_000, start_ms=92_500),
    ]
    render_records.write_timeline_from_render(project, sections)

    chapters = operations.chapters_for(project)
    assert [c.start_ms for c in chapters] == [0, 92_500], "chapters must use measured positions"
    assert [c.title for c in chapters] == ["One", "Two"]


def test_chapters_fall_back_to_the_plan_before_anything_is_rendered(project_root):
    operations.create_project("No Render Yet")
    operations.add_plan_section("no-render-yet", title="Only", estimated_seconds=45)

    chapters = operations.chapters_for(operations.require_project("no-render-yet"))
    assert [c.start_ms for c in chapters] == [0]


def test_reviewing_reports_its_renders_not_its_working_files(project_root):
    """A render leaves a PNG per slide and an audio file per section, so counting
    files reported '96 file(s)' for one video -- a number that reads as a fault
    and tells the operator nothing."""
    operations.create_project("Badge")
    output = project_root / "badge" / "reviewing" / "output"
    (output / "frames").mkdir(parents=True)
    for index in range(40):
        (output / "frames" / f"s00_{index:02d}.png").write_bytes(b"x")
    (output / "badge.mp4").write_bytes(b"x")

    project = operations.require_project("badge")
    from pipeline.stages import Stage

    detail = project.stage_state(Stage.REVIEWING).detail
    assert "96" not in detail and "41" not in detail, f"still counting working files: {detail}"
    assert "render" in detail and "badge.mp4" in detail, detail


def test_transcript_times_come_from_the_render(project_root, tmp_path):
    """Clicking a transcript line seeks the video, so its times must be the
    video's -- not the plan's pre-narration guess."""
    from pipeline.rendering import RenderedSection

    operations.create_project("Transcript Times")
    for title in ("One", "Two"):
        operations.add_plan_section("transcript-times", title=title, estimated_seconds=60)
    for section in operations.read_artifact("transcript-times", "plan")["sections"]:
        operations.write_section_script("transcript-times", section["id"], "Narration.")

    before = operations.read_artifact("transcript-times", "review")
    assert [entry["start_ms"] for entry in before["transcript"]] == [0, 60_000], \
        "before a render, the plan's estimate is the only answer available"

    audio = tmp_path / "section-00.mp3"
    audio.write_bytes(b"x")
    render_records.write_timeline_from_render(
        operations.require_project("transcript-times"),
        [
            RenderedSection("a", "One", "Narration.", audio_path=audio,
                            audio_duration_ms=90_000, start_ms=0),
            RenderedSection("b", "Two", "Narration.", audio_path=audio,
                            audio_duration_ms=30_000, start_ms=92_500),
        ],
    )

    after = operations.read_artifact("transcript-times", "review")
    assert [entry["start_ms"] for entry in after["transcript"]] == [0, 92_500]


# --- the three P1s: renders must not destroy work or lie about history -------


def _render_two_short_sections(slug):
    """A real render (silent voice, so no network) of two short sections."""
    operations.create_project(slug.replace("-", " ").title())
    for title in ("First section", "Second section"):
        operations.add_plan_section(slug, title=title, estimated_seconds=60)
    for section in operations.read_artifact(slug, "plan")["sections"]:
        operations.write_section_script(slug, section["id"], "One sentence. Two sentences.")
    return operations.render_video(slug, voice_provider="silent")


def test_an_edited_timeline_survives_a_re_render(project_root):
    """The marker alone was not proof the timeline was still the renderer's.

    Every client sends the whole document back on save, marker included, so an
    edited timeline still claimed to be generated and the next render replaced
    it -- silently destroying the edit.
    """
    _render_two_short_sections("edit-survives")

    composition = operations.read_artifact("edit-survives", "composition")
    for track in composition["tracks"]:
        for clip in track["clips"]:
            clip["text"] = clip["label"] = "MINE"
            break
    operations.write_artifact("edit-survives", "composition", composition)

    saved = operations.read_artifact("edit-survives", "composition")
    assert saved["generated_from_render_at"] == "", "a client write must clear the marker"

    result = operations.render_video("edit-survives", voice_provider="silent")
    after = operations.read_artifact("edit-survives", "composition")
    assert any(clip["text"] == "MINE" for track in after["tracks"] for clip in track["clips"]), \
        "the re-render erased an edit"
    assert any("your own edits" in warning for warning in result["warnings"])


def test_a_forged_marker_does_not_defeat_the_guard(project_root):
    """Defence in depth: a client that writes the marker back by hand still
    cannot get its edits replaced, because the fingerprint will not match."""
    _render_two_short_sections("forged-marker")

    composition = operations.read_artifact("forged-marker", "composition")
    for track in composition["tracks"]:
        for clip in track["clips"]:
            clip["text"] = "MINE"
            break
    composition["generated_from_render_at"] = "2026-01-01T00:00:00"
    composition["generated_fingerprint"] = "not-the-real-one"
    operations.write_artifact("forged-marker", "composition", composition)

    operations.render_video("forged-marker", voice_provider="silent")
    after = operations.read_artifact("forged-marker", "composition")
    assert any(clip["text"] == "MINE" for track in after["tracks"] for clip in track["clips"])


def test_an_untouched_generated_timeline_is_still_rebuilt(project_root):
    """The guard must not be so strict that a re-render stops updating its own
    timeline -- otherwise the timeline drifts from the video."""
    _render_two_short_sections("rebuild-ok")
    first = operations.read_artifact("rebuild-ok", "composition")

    operations.render_video("rebuild-ok", voice_provider="silent")
    second = operations.read_artifact("rebuild-ok", "composition")

    assert second["generated_from_render_at"] != first["generated_from_render_at"]
    assert second["clip_count"] == first["clip_count"]


def test_a_chapter_is_a_section_even_though_a_clip_is_a_scene(project_root):
    """The video track carries one clip per scene. Taking a chapter from each of
    them turned a six-section video into forty-one chapters named after scenes,
    and a chapter list that long is not navigation."""
    _render_two_short_sections("chapters-per-section")

    composition = operations.read_artifact("chapters-per-section", "composition")
    scene_clips = [
        clip for track in composition["tracks"] if track["kind"] == "video"
        for clip in track["clips"]
    ]
    review = operations.read_artifact("chapters-per-section", "review")
    sections = operations.read_artifact("chapters-per-section", "plan")["sections"]

    assert len(scene_clips) > len(sections), "several clips to a section"
    assert [c["title"] for c in review["chapters"]] == [s["title"] for s in sections]


def test_the_first_render_seeds_chapters_from_measured_timing(project_root):
    """Chapters were seeded before the measured timeline existed, so they fell
    back to the plan's estimates -- pointing at 60s in a 15s video."""
    _render_two_short_sections("measured-chapters")

    review = operations.read_artifact("measured-chapters", "review")
    composition = operations.read_artifact("measured-chapters", "composition")

    # A chapter is a section, and the video track carries one clip per scene, so
    # the section starts are where each section's first clip is.
    earliest: dict[str, int] = {}
    for track in composition["tracks"]:
        if track["kind"] != "video":
            continue
        for clip in sorted(track["clips"], key=lambda c: c["start_ms"]):
            earliest.setdefault(clip["section_id"], clip["start_ms"])
    measured = sorted(earliest.values())

    assert [c["start_ms"] for c in review["chapters"]] == measured
    assert review["chapters"][-1]["start_ms"] < review["versions"][-1]["duration_ms"], \
        "a chapter must not point past the end of the video"


def test_edited_chapters_are_not_overwritten_but_are_flagged(project_root):
    _render_two_short_sections("kept-chapters")

    review = operations.read_artifact("kept-chapters", "review")
    review["chapters"] = [{"id": "c1", "title": "Mine", "start_ms": 1234}]
    operations.write_artifact("kept-chapters", "review", review)

    result = operations.render_video("kept-chapters", voice_provider="silent")
    after = operations.read_artifact("kept-chapters", "review")

    assert [c["title"] for c in after["chapters"]] == ["Mine"], "hand-written chapters were lost"
    assert any("do not match this render" in warning for warning in result["warnings"])


def test_every_render_is_kept_as_its_own_file(project_root):
    """A version that can be overwritten is not a version: re-rendering used to
    replace every earlier cut, and selecting an old one played the newest."""
    first = _render_two_short_sections("immutable-versions")
    second = operations.render_video("immutable-versions", voice_provider="silent")

    assert first["video_path"] != second["video_path"]
    from pathlib import Path as _Path
    assert _Path(first["video_path"]).exists(), "the earlier cut was overwritten"
    assert _Path(second["video_path"]).exists()

    versions = operations.read_artifact("immutable-versions", "review")["versions"]
    assert len({v["file_path"] for v in versions}) == len(versions)


def test_render_frames_are_cleaned_up(project_root):
    """Frames are intermediates. Keeping a PNG per slide for every render would
    grow without limit."""
    _render_two_short_sections("tidy-frames")
    frames = project_root / "tidy-frames" / "reviewing" / "output" / "frames"
    leftover = list(frames.rglob("*.png")) if frames.exists() else []
    assert leftover == [], f"{len(leftover)} frame(s) left behind"


def test_two_renders_in_the_same_second_are_still_separate_versions(project_root):
    """A render id is a file path. At one-second resolution two quick renders
    shared one, so the second overwrote the first's video while the review still
    listed both -- picking the older version played the newer file, which is the
    bug the id was introduced to prevent."""
    _render_two_short_sections("same-second")
    operations.render_video("same-second", voice_provider="silent")

    review = operations.read_artifact("same-second", "review")
    paths = [version["file_path"] for version in review["versions"]]

    assert len(paths) == 2
    assert paths[0] != paths[1], "both versions point at the same file"
    for path in paths:
        assert Path(path).exists(), f"{path} was overwritten by the other render"


# --- what a failed model call says ------------------------------------------------------


def _connection_error():
    import httpx
    import openai

    return openai.APIConnectionError(request=httpx.Request("POST", "https://example.invalid"))


def test_a_dropped_connection_is_reported_as_one_not_as_a_bad_answer():
    """The retry wrappers hide the cause, and the message blamed the schema:
    "The model did not return a valid OrchestratorTurn after 2 retries:
    InstructorRetryException: Connection error." blames the model for the
    network and tells the reader nothing they can do."""
    from pipeline.llm import _what_went_wrong

    buried = RuntimeError("InstructorRetryException: Connection error.")
    buried.__cause__ = _connection_error()

    assert "Could not reach the model provider" in _what_went_wrong(buried)


def test_a_rejected_key_names_the_key():
    import httpx
    import openai

    from pipeline.llm import _what_went_wrong

    request = httpx.Request("POST", "https://example.invalid")
    rejected = openai.AuthenticationError(
        "Unauthorized", response=httpx.Response(401, request=request), body=None)

    assert "API key" in _what_went_wrong(rejected)


def test_an_answer_that_does_not_fit_the_schema_keeps_the_schema_message():
    """Only failures that are *not* about the answer are re-explained."""
    from pipeline.llm import _what_went_wrong

    assert _what_went_wrong(ValueError("body.sections.0.title: field required")) == ""


# --- the shape of the core itself ---------------------------------------------------


PIPELINE = Path(__file__).resolve().parents[1] / "src" / "pipeline"

# The order the modules behind `operations` are allowed to depend in. A module may
# import from those above it and never from those below, which is what keeps the
# graph acyclic without anyone having to hold it in their head.
LAYERS = [
    "core",
    "freshness",
    "presentation",
    "render_records",
    "extraction_run",
    "authoring",
    "render_run",
]


def test_the_core_is_a_surface_not_a_file():
    """`operations.py` reached 1,704 lines and 58 functions -- "one core" had
    become "one file everything is in", which is the failure the module exists to
    prevent, arrived at from the other direction. It is now the surface: imports
    and `__all__`, with the verbs in modules beside it."""
    source = (PIPELINE / "operations.py").read_text(encoding="utf-8")

    assert "def " not in source, "operations.py defines a verb again; it is the surface"
    assert len(source.splitlines()) < 300


# Every module that is already too long, with the length it is allowed to keep.
# A ratchet, not a pass: a module in here may shrink and may not grow, and one
# that is not in here may not reach the limit at all.
#
# It exists because the old rule guarded seven modules -- all of which complied
# -- while the twelve that had actually grown were not listed, so nothing
# stopped `routes_project.py` reaching 1,438 lines. Splitting all of them at
# once is not the job; making the debt visible and unable to grow is.
LONGEST_SENSIBLE_MODULE = 450

MODULE_BUDGETS = {
    "web/routes_project.py": 1438,
    "rendering.py": 1283,
    "extraction.py": 1154,
    "scene_renderers.py": 758,
    "slide_frame.py": 677,
    "extraction_review.py": 648,
    "generation.py": 556,
    "speech.py": 551,
    "visual_build.py": 501,
    "plan_drafting.py": 476,
    "orchestrator.py": 465,
    "cli.py": 460,
}


def test_no_module_grows_past_the_length_it_is_allowed():
    """The guard that was pointing at the wrong files.

    It checked seven modules that were all well inside the limit and none of the
    ones that had grown, so the rule read as enforced while the codebase drifted
    past it. Now every module is checked, and the ones already over carry a
    recorded budget they cannot exceed.
    """
    too_long = []
    shrunk = []
    for path in sorted(PIPELINE.rglob("*.py")):
        if "__pycache__" in str(path):
            continue
        name = path.relative_to(PIPELINE).as_posix()
        lines = len(path.read_text(encoding="utf-8").splitlines())
        allowed = MODULE_BUDGETS.get(name, LONGEST_SENSIBLE_MODULE)
        if lines > allowed:
            too_long.append(f"{name}: {lines} lines, allowed {allowed}")
        elif name in MODULE_BUDGETS and lines < allowed - 40:
            shrunk.append(f"{name}: {lines} lines, budget still says {allowed}")

    assert not too_long, "split these before they grow further: " + "; ".join(too_long)
    assert not shrunk, (
        "these shrank -- lower their budget so the ratchet holds: " + "; ".join(shrunk)
    )


def test_every_module_behind_the_core_stays_small_enough_to_read():
    for name in LAYERS:
        lines = (PIPELINE / f"{name}.py").read_text(encoding="utf-8").splitlines()
        assert len(lines) < 450, f"{name}.py is {len(lines)} lines; split it before it grows"


def test_the_modules_behind_the_core_depend_in_one_direction():
    """A cycle here would be invisible until an import failed at a call site far
    away, and the usual fix -- a function-level import -- hides the cycle instead
    of removing it."""
    for position, name in enumerate(LAYERS):
        source = (PIPELINE / f"{name}.py").read_text(encoding="utf-8")
        for below in LAYERS[position + 1:]:
            assert f"from pipeline.{below} import" not in source, (
                f"{name}.py imports {below}.py, which is below it"
            )


def test_nothing_behind_the_core_imports_the_core_back():
    """The surface re-exports the modules; a module importing the surface would
    make the two mutually dependent and the import order load-bearing."""
    for name in [*LAYERS, "assets", "exporting"]:
        source = (PIPELINE / f"{name}.py").read_text(encoding="utf-8")
        assert "from pipeline.operations import" not in source, f"{name}.py imports the surface"
        assert "import pipeline.operations" not in source, f"{name}.py imports the surface"


def test_the_surface_exports_everything_the_clients_import():
    """A verb that moved module but was left out of `__all__` would break one
    client and not the others -- exactly the drift this module prevents."""
    from pipeline import operations

    for client in ("cli.py", "mcp_server.py", "web/routes_project.py"):
        source = (PIPELINE / client).read_text(encoding="utf-8")
        for line in source.splitlines():
            line = line.strip()
            if not line.startswith("from pipeline.operations import "):
                continue
            wanted = line.removeprefix("from pipeline.operations import ").strip("( ")
            for name in (part.strip().strip(",") for part in wanted.split(",")):
                if not name or name == "(":
                    continue
                assert hasattr(operations, name), f"{client} imports {name}, which is not exported"
