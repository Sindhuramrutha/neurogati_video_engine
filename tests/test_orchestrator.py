"""The master agent: it belongs to no stage, and it really runs the others.

These tests stand in for the model. What is being checked is the orchestration
-- who gets asked, whether they run together, what happens when one of them
fails -- none of which depends on a real provider, and all of which would be
untestable if it did.
"""

import json
import threading
import time

import pytest

from pipeline import operations, orchestrator
from pipeline.operations import OperationFailed
from pipeline.orchestrator import Consultation, OrchestratorTurn


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


@pytest.fixture
def project(project_root):
    return operations.create_project("Orchestration Check")["slug"]


def scripted(*turns):
    """A model that returns these turns in order. Records what it was asked."""
    calls = []

    def fake(response_model, system_prompt, user_prompt, **kwargs):
        calls.append({"system": system_prompt, "user": user_prompt})
        return turns[min(len(calls) - 1, len(turns) - 1)]

    fake.calls = calls
    return fake


# --- it is not a stage -------------------------------------------------------


def test_the_orchestrator_is_not_one_of_the_pipeline_stages():
    """If it were, it would appear in the stepper and be expected to produce an
    artifact. It stands above the pipeline, not inside it."""
    from pipeline.stages import STAGES

    assert "orchestrator" not in {spec.key.value for spec in STAGES}
    assert "orchestrator" not in operations.ARTIFACTS


def test_the_orchestrator_agent_resolves_without_a_stage(project):
    agent = orchestrator.resolve_orchestrator(operations.require_project(project))

    assert agent.stage is None
    assert agent.name == "Orchestrator"
    assert agent.source == "default"
    # Its tools are declared in the same file the model is prompted with.
    assert "consult_agents" in {tool.name for tool in agent.tools.granted}
    assert agent.tools.unknown == []


def test_a_project_can_override_the_orchestrator(project, project_root):
    override = project_root / project / "agents" / "orchestrator" / "AGENT.md"
    override.parent.mkdir(parents=True)
    override.write_text(
        "---\nname: House Orchestrator\nrole: ours\ntools: [consult_agents]\n---\nBe terse.",
        encoding="utf-8",
    )

    agent = orchestrator.resolve_orchestrator(operations.require_project(project))
    assert agent.name == "House Orchestrator"
    assert agent.source == "project"


# --- it can see the whole pipeline, not one slice ----------------------------


def test_the_snapshot_covers_every_stage(project):
    snapshot = orchestrator.pipeline_snapshot(operations.require_project(project))

    for stage_key in (
        "inputs", "extraction", "scene-plan", "script-staging", "studio", "reviewing",
    ):
        assert stage_key in snapshot
    # And it says which artifacts do not exist yet, so the agent reports an
    # empty project rather than inventing one.
    assert "not produced yet" in snapshot


def test_the_snapshot_notices_an_artifact_appearing(project):
    operations.write_artifact(project, "plan", {"sections": []})
    snapshot = orchestrator.pipeline_snapshot(operations.require_project(project))

    assert "'plan' exists" in snapshot


def test_the_roster_names_every_stage_agent(project):
    roster = orchestrator.agent_roster(operations.require_project(project))

    for name in ("Extraction", "Scene Plan", "Script & Staging", "Studio", "Reviewing"):
        assert name in roster
    # Inputs has no agent, so it cannot be commanded and is not offered.
    assert "inputs" not in roster


# --- it commands the stage agents --------------------------------------------


def test_it_consults_the_agents_it_names_then_answers(project, monkeypatch):
    asked = []

    def fake_ask(slug, stage_key, question):
        asked.append((stage_key, question))
        return {"agent": stage_key.title(), "answer": f"{stage_key} says fine"}

    monkeypatch.setattr(orchestrator, "ask_stage_agent", fake_ask)
    monkeypatch.setattr(orchestrator, "complete_structured", scripted(
        OrchestratorTurn(consult=[
            Consultation(stage="scene-plan", question="how many sections?"),
            Consultation(stage="script-staging", question="any section over budget?"),
        ]),
        OrchestratorTurn(answer="Scene Plan and Script & Staging both report it is fine."),
    ))

    result = orchestrator.ask_the_orchestrator(project, "is this project healthy?")

    assert [stage for stage, _ in asked] == ["scene-plan", "script-staging"]
    assert result["answer"] == "Scene Plan and Script & Staging both report it is fine."
    assert result["agent"] == "Orchestrator"
    assert [c["agent"] for c in result["consulted"]] == ["Scene-Plan", "Script-Staging"]
    # The originals are kept, so a summary can be checked against them.
    assert result["consulted"][0]["answer"] == "scene-plan says fine"


def test_consulted_agents_run_at_the_same_time(project, monkeypatch):
    """Five sequential reasoning-model calls is minutes of waiting; the whole
    reason to let one agent command several is that they overlap."""
    concurrent = []
    live = 0
    guard = threading.Lock()

    def slow_ask(slug, stage_key, question):
        nonlocal live
        with guard:
            live += 1
            concurrent.append(live)
        time.sleep(0.25)
        with guard:
            live -= 1
        return {"agent": stage_key.title(), "answer": "ok"}

    monkeypatch.setattr(orchestrator, "ask_stage_agent", slow_ask)

    started = time.monotonic()
    found = orchestrator.run_consultations(project, [
        Consultation(stage=stage, question="q")
        for stage in ("extraction", "scene-plan", "script-staging", "studio", "reviewing")
    ])
    elapsed = time.monotonic() - started

    assert len(found) == 5
    assert max(concurrent) >= 2, "the agents ran one after another"
    assert elapsed < 1.0, f"five 0.25s agents took {elapsed:.2f}s — they did not overlap"


def test_one_unreachable_agent_does_not_lose_the_others(project, monkeypatch):
    def flaky_ask(slug, stage_key, question):
        if stage_key == "studio":
            raise OperationFailed("the studio agent is unavailable")
        return {"agent": stage_key.title(), "answer": "ok"}

    monkeypatch.setattr(orchestrator, "ask_stage_agent", flaky_ask)

    found = orchestrator.run_consultations(project, [
        Consultation(stage="scene-plan", question="q"),
        Consultation(stage="studio", question="q"),
    ])

    assert [one["ok"] for one in found] == [True, False]
    assert "unavailable" in found[1]["answer"]


def test_it_will_not_run_more_agents_than_there_are(project, monkeypatch):
    """Every consultation is a paid call; a model repeating itself should not
    multiply the bill."""
    monkeypatch.setattr(
        orchestrator, "ask_stage_agent",
        lambda slug, stage_key, question: {"agent": stage_key, "answer": "ok"},
    )

    found = orchestrator.run_consultations(project, [
        Consultation(stage="scene-plan", question=f"q{n}") for n in range(20)
    ])

    assert len(found) == orchestrator.MAXIMUM_CONSULTATIONS_PER_ROUND


# --- it reads artifacts across every stage -----------------------------------


def test_it_reads_any_stage_artifact(project):
    operations.write_artifact(project, "plan", {"sections": [{"id": "s1", "title": "One"}]})

    found = orchestrator.run_reads(project, ["plan", "review"])

    assert found[0]["ok"] and "One" in found[0]["content"]
    # Not yet produced: reported as a finding, so the agent says so rather than
    # inventing a review.
    assert found[1]["ok"] is False


def test_an_unknown_artifact_is_a_finding_not_a_crash(project):
    found = orchestrator.run_reads(project, ["timeline"])

    assert found[0]["ok"] is False
    assert "no such artifact" in found[0]["content"]


def test_a_large_artifact_is_truncated_not_sent_whole(project):
    operations.write_artifact(project, "plan", {
        "sections": [{"id": f"s{n}", "title": "x" * 200} for n in range(200)],
    })

    found = orchestrator.run_reads(project, ["plan"])

    assert len(found[0]["content"]) < orchestrator.MAXIMUM_ARTIFACT_CHARACTERS + 200
    assert "truncated" in found[0]["content"]


# --- the loop is bounded ------------------------------------------------------


def test_it_stops_gathering_and_answers(project, monkeypatch):
    """An agent that can keep asking for more is an agent that can spend an
    unbounded amount of money on one question typed into a chat box."""
    monkeypatch.setattr(
        orchestrator, "ask_stage_agent",
        lambda slug, stage_key, question: {"agent": stage_key, "answer": "ok"},
    )
    never_satisfied = scripted(
        OrchestratorTurn(consult=[Consultation(stage="scene-plan", question="more?")]),
    )
    monkeypatch.setattr(orchestrator, "complete_structured", never_satisfied)

    result = orchestrator.ask_the_orchestrator(project, "tell me everything")

    assert len(never_satisfied.calls) == orchestrator.MAXIMUM_ROUNDS + 1
    assert result["answer"]
    assert result["rounds"] == orchestrator.MAXIMUM_ROUNDS


def test_it_can_answer_without_consulting_anyone(project, monkeypatch):
    monkeypatch.setattr(orchestrator, "complete_structured", scripted(
        OrchestratorTurn(answer="Nothing has been uploaded yet."),
    ))

    result = orchestrator.ask_the_orchestrator(project, "hi")

    assert result["answer"] == "Nothing has been uploaded yet."
    assert result["consulted"] == []
    assert result["rounds"] == 0


def test_a_turn_that_does_nothing_does_not_loop_forever(project, monkeypatch):
    stuck = scripted(OrchestratorTurn())
    monkeypatch.setattr(orchestrator, "complete_structured", stuck)

    result = orchestrator.ask_the_orchestrator(project, "hi")

    assert result["answer"]
    assert len(stuck.calls) <= orchestrator.MAXIMUM_ROUNDS + 1


def test_the_prompt_tells_the_agent_its_tools_actually_run(project, monkeypatch):
    """The stage agents are told the opposite, because for them it is true. If
    the orchestrator inherited that line it would refuse to consult anyone."""
    seen = scripted(OrchestratorTurn(answer="done"))
    monkeypatch.setattr(orchestrator, "complete_structured", seen)

    orchestrator.ask_the_orchestrator(project, "hi")
    system_prompt = seen.calls[0]["system"]

    assert "Your tools do run" in system_prompt
    assert "you cannot call them" not in system_prompt
    # And it knows who it commands.
    assert "Scene Plan" in system_prompt and "Script & Staging" in system_prompt


# --- the web route ------------------------------------------------------------


def test_the_route_is_not_shadowed_by_the_stage_agent_route(project, monkeypatch):
    """`/agent/ask` would put a literal `ask` where `/agent/{stage}` expects a
    parameter -- the exact collision that once left `planning` unable to reach
    its own agent."""
    from litestar.testing import TestClient

    from pipeline.web.app import create_app

    monkeypatch.setattr(
        "pipeline.web.routes_project.ask_the_orchestrator",
        lambda slug, question, conversation_id="": {
            "agent": "Orchestrator", "agent_source": "default", "agent_path": "x",
            "question": question, "answer": "heard you", "rounds": 0,
            "consulted": [], "artifacts_read": [],
        },
    )

    with TestClient(app=create_app()) as client:
        response = client.post(
            f"/api/projects/{project}/orchestrator/ask", json={"question": "hi"}
        )

    assert response.status_code == 201, response.text
    assert response.json()["answer"] == "heard you"


def test_the_route_reports_a_failure_rather_than_a_traceback(project, monkeypatch):
    from litestar.testing import TestClient

    from pipeline.web.app import create_app

    def unhappy(slug, question, conversation_id=""):
        raise OperationFailed("no model is configured")

    monkeypatch.setattr("pipeline.web.routes_project.ask_the_orchestrator", unhappy)

    with TestClient(app=create_app()) as client:
        response = client.post(
            f"/api/projects/{project}/orchestrator/ask", json={"question": "hi"}
        )

    assert response.status_code == 400
    assert "no model is configured" in json.dumps(response.json())


# --- conversations -----------------------------------------------------------


def _answering(text, monkeypatch):
    fake = scripted(OrchestratorTurn(answer=text))
    monkeypatch.setattr(orchestrator, "complete_structured", fake)
    return fake


def test_an_answer_is_kept_so_the_panel_can_be_closed_and_reopened(project, monkeypatch):
    """The exchange is written down, so closing the drawer keeps the thread."""
    _answering("Section 2 runs long.", monkeypatch)

    reply = orchestrator.ask_the_orchestrator(project, "How is the pacing?")

    listed = orchestrator.list_conversations(project)["conversations"]
    assert [c["title"] for c in listed] == ["How is the pacing?"]
    assert listed[0]["turn_count"] == 1

    reopened = orchestrator.read_conversation(project, reply["conversation_id"])
    assert reopened["turns"][0]["question"] == "How is the pacing?"
    assert reopened["turns"][0]["answer"] == "Section 2 runs long."


def test_a_follow_up_is_told_what_was_already_said(project, monkeypatch):
    """A follow-up is told what was said, so "and why is that?" does not refer to
    a conversation only the person can remember."""
    first = _answering("Section 2 runs long.", monkeypatch)
    started = orchestrator.ask_the_orchestrator(project, "How is the pacing?")

    second = _answering("Because it covers three ideas.", monkeypatch)
    orchestrator.ask_the_orchestrator(
        project, "And why is that?", started["conversation_id"])

    asked = second.calls[-1]["user"]
    assert "earlier in this conversation" in asked
    assert "They asked: How is the pacing?" in asked
    assert "You answered: Section 2 runs long." in asked
    assert first.calls[0]["user"].count("earlier in this conversation") == 0


def test_a_new_conversation_starts_clean(project, monkeypatch):
    _answering("First answer.", monkeypatch)
    orchestrator.ask_the_orchestrator(project, "First question?")

    fresh = _answering("Second answer.", monkeypatch)
    second = orchestrator.ask_the_orchestrator(project, "Unrelated question?")

    assert "earlier in this conversation" not in fresh.calls[-1]["user"]
    assert len(orchestrator.list_conversations(project)["conversations"]) == 2
    assert orchestrator.read_conversation(project, second["conversation_id"])["turns"] != []


def test_conversations_are_listed_newest_first(project, monkeypatch):
    _answering("A.", monkeypatch)
    orchestrator.ask_the_orchestrator(project, "Older question?")
    _answering("B.", monkeypatch)
    newer = orchestrator.ask_the_orchestrator(project, "Newer question?")

    listed = orchestrator.list_conversations(project)["conversations"]
    assert listed[0]["id"] == newer["conversation_id"]


def test_a_failed_ask_is_not_recorded_as_something_the_agent_said(project, monkeypatch):
    """A dropped connection is not an answer. Replaying it as one would teach
    the agent to answer that way."""
    from pipeline.llm import ModelCallFailed

    def fails(*_args, **_kwargs):
        raise ModelCallFailed("Could not reach the model provider.")

    monkeypatch.setattr(orchestrator, "complete_structured", fails)

    with pytest.raises(OperationFailed):
        orchestrator.ask_the_orchestrator(project, "Anything?")

    assert orchestrator.list_conversations(project)["conversations"] == []


def test_a_long_thread_replays_its_most_recent_turns_only(project, monkeypatch):
    from pipeline.conversations import MAXIMUM_HISTORY_CHARACTERS

    _answering("x" * 3000, monkeypatch)
    thread = orchestrator.ask_the_orchestrator(project, "First of many?")
    for number in range(4):
        _answering("y" * 3000, monkeypatch)
        orchestrator.ask_the_orchestrator(
            project, f"Question {number}?", thread["conversation_id"])

    latest = _answering("done", monkeypatch)
    orchestrator.ask_the_orchestrator(project, "And finally?", thread["conversation_id"])
    asked = latest.calls[-1]["user"]
    history = asked.split("--- earlier in this conversation ---")[1]

    assert len(history) < MAXIMUM_HISTORY_CHARACTERS + 500
    assert "First of many?" not in history, "the oldest turn should be the one dropped"
    assert "Question 3?" in history


def test_a_conversation_can_be_forgotten(project, monkeypatch):
    _answering("Kept.", monkeypatch)
    kept = orchestrator.ask_the_orchestrator(project, "Keep me?")
    _answering("Gone.", monkeypatch)
    gone = orchestrator.ask_the_orchestrator(project, "Forget me?")

    left = orchestrator.forget_conversation(project, gone["conversation_id"])

    assert [c["id"] for c in left["conversations"]] == [kept["conversation_id"]]
    with pytest.raises(OperationFailed, match="no conversation"):
        orchestrator.read_conversation(project, gone["conversation_id"])


def test_the_consulted_agents_are_kept_with_the_answer(project, monkeypatch):
    """Without them a reopened thread is a claim with no way to check it."""
    monkeypatch.setattr(orchestrator, "complete_structured", scripted(
        OrchestratorTurn(consult=[Consultation(stage="scene-plan", question="Is it long?")]),
        OrchestratorTurn(answer="Yes, section 2."),
    ))
    monkeypatch.setattr(orchestrator, "ask_stage_agent",
                        lambda *_args: {"agent": "Planning", "answer": "It is long."})

    reply = orchestrator.ask_the_orchestrator(project, "Is section 2 long?")
    reopened = orchestrator.read_conversation(project, reply["conversation_id"])

    assert [c["stage"] for c in reopened["turns"][0]["consulted"]] == ["scene-plan"]
