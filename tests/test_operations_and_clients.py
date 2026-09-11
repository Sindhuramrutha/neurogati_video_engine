"""The shared core, and the three clients that must not drift from it.

The point of `pipeline.operations` is that the browser, the CLI and MCP produce
identical results. These tests assert that directly rather than testing each
client separately and hoping.
"""

import json

import pytest

from pipeline import operations
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

    assert review["audit"]["by_stage"] == {"scripting": 1}
    assert [entry["body"] for entry in review["transcript"]] == ["Hello and welcome."]


def test_routing_to_an_unknown_stage_lists_the_real_ones(project_root):
    operations.create_project("Routing")
    with pytest.raises(OperationFailed) as failure:
        operations.add_review_comment("routing", body="x", routed_to_stage="nowhere")

    assert "scripting" in str(failure.value)


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
