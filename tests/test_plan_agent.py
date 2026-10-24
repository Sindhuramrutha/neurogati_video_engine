"""Planning in a conversation: the agent proposes the shape, code holds the slide
order, the person agrees, and only then are the scenes written. The model is
stood in for throughout; what is checked is everything around it."""
# ruff: noqa: F811

import pytest

from pipeline import operations, plan_agent
from pipeline.operations import OperationFailed
from pipeline.plan_agent import (
    agree,
    discard_proposal,
    read_planning,
    send_message,
    set_setup,
)
from pipeline.plan_answers import (
    DetailedScene,
    LeftOut,
    SceneAnswer,
    ShapeAnswer,
    ShapeSection,
)
from pipeline.plan_handoff import FAIL, plan_checks
from pipeline.plan_order import coverage_problems, order_problems
from pipeline.planning import PlanStore
from tests.test_slide_first import a_deck, a_deck_project, project_root  # noqa: F401

# --- the order, held by code -----------------------------------------------------------


def test_strict_order_wants_unbroken_runs_in_the_deck_s_order():
    assert order_problems([("A", [1, 2]), ("B", [3, 4, 5])], "strict") == []
    assert order_problems([("B", [4, 5]), ("A", [1, 2, 3])], "strict"), \
        "slide 4's topic can never come first"
    assert order_problems([("A", [1, 3]), ("B", [2])], "strict"), "a run has no gaps"
    assert order_problems([("A", [1, 2]), ("B", [2, 3])], "strict"), "no slide twice"


def test_looser_orders_allow_what_they_say():
    assert order_problems([("A", [2, 1]), ("B", [3])], "nearly") == [], \
        "nearly strict: slides may move inside a section"
    assert order_problems([("B", [3]), ("A", [1, 2])], "nearly"), "but sections follow the deck"
    assert order_problems([("B", [3]), ("A", [1, 2])], "loose") == []
    assert order_problems([("A", [1]), ("B", [1])], "free") == []


def test_a_slide_left_out_must_be_said():
    assert coverage_problems([("A", [1, 2])], [1, 2, 3], {}) == [
        "1 slide(s) are not covered and not left out on purpose: 3"]
    assert coverage_problems([("A", [1, 2])], [1, 2, 3], {3: "a thank-you slide"}) == []


# --- the conversation ------------------------------------------------------------------


def shape(*sections, left_out=(), reply="Here is a shape."):
    return ShapeAnswer(
        reply=reply, shortest_minutes=4, longest_minutes=6,
        length_understood="About 5 min.", teaches="How the brain came to be known.",
        sections=[ShapeSection(title=t, how=h, units=u, minutes=m, scenes=n, summary=f"{t}.")
                  for t, h, u, m, n in sections],
        left_out=[LeftOut(unit=u, why=w) for u, w in left_out])


GOOD = shape(("Opening", "Hook", [], 0.5, 1), ("First part", "Plain", [1, 2], 2, 3),
             ("Second part", "Plain", [3], 1.5, 2), ("Recap", "Look back", [], 0.5, 1),
             ("Close", "One idea", [], 0.5, 1))


class FakeModel:
    """Answers shape calls from a queue, and scene calls with as many as asked."""

    def __init__(self, *shapes):
        self.shapes = list(shapes)
        self.shape_prompts, self.scene_prompts = [], []

    def __call__(self, model, system_prompt, user_prompt, **kwargs):
        if model is ShapeAnswer:
            self.shape_prompts.append(user_prompt)
            return self.shapes.pop(0)
        self.scene_prompts.append(user_prompt)
        count = int(user_prompt.split("in exactly ")[1].split(" scenes")[0])
        return SceneAnswer(scenes=[DetailedScene(does=f"Beat {n}", units=[], seconds=10)
                                   for n in range(count)])


def test_a_message_gets_a_proposed_shape_and_changes_nothing(project_root, monkeypatch):
    slug, project = a_deck_project("Talk", slides=3)
    set_setup(slug, {"length_text": "about 5 min, longer is fine", "audience": "Nurses"})
    fake = FakeModel(GOOD)
    monkeypatch.setattr(plan_agent, "complete_structured", fake)

    view = send_message(slug, "Keep the story together.")

    assert [m["role"] for m in view["messages"]] == ["you", "agent"]
    assert view["proposal"]["reply"] == "Here is a shape." and not view["proposal"]["problems"]
    assert "about 5 min, longer is fine" in fake.shape_prompts[0]
    assert "1. Heading number 1" in fake.shape_prompts[0], "the agent sees every slide"
    assert PlanStore(project.root).load().sections == [], "nothing changes until agreed"


def test_a_shape_out_of_order_is_sent_back_once_with_the_problem(project_root, monkeypatch):
    slug, _ = a_deck_project("Order", slides=3)
    backwards = shape(("Second", "Plain", [3], 1, 1), ("First", "Plain", [1, 2], 1, 1))
    fake = FakeModel(backwards, GOOD)
    monkeypatch.setattr(plan_agent, "complete_structured", fake)

    view = send_message(slug, "Plan it.")

    assert len(fake.shape_prompts) == 2
    assert "against the deck's order" in fake.shape_prompts[1]
    assert view["proposal"]["calls"] == 2 and not view["proposal"]["problems"]


def test_a_shape_still_broken_cannot_be_agreed_to(project_root, monkeypatch):
    slug, _ = a_deck_project("Still broken", slides=3)
    backwards = shape(("Second", "Plain", [3], 1, 1), ("First", "Plain", [1, 2], 1, 1))
    monkeypatch.setattr(plan_agent, "complete_structured", FakeModel(backwards, backwards))

    view = send_message(slug, "Plan it.")
    assert view["proposal"]["problems"]
    with pytest.raises(OperationFailed, match="breaks the slide order"):
        agree(slug)


def test_agreeing_makes_the_plan_and_writes_each_section_s_scenes(project_root, monkeypatch):
    slug, project = a_deck_project("Agree", slides=3)
    fake = FakeModel(GOOD)
    monkeypatch.setattr(plan_agent, "complete_structured", fake)
    send_message(slug, "Plan it.")
    assert read_planning(slug)["agree_calls"] == 5, "said before it runs"

    agree(slug)

    plan = PlanStore(project.root).load()
    assert [s.title for s in plan.sections] == [
        "Opening", "First part", "Second part", "Recap", "Close"], "the agent's own sections"
    assert plan.sections[0].sources == [] and plan.sections[0].how == "Hook"
    first = plan.sections[1]
    assert [r.slide_number for r in first.sources] == [1, 2]
    assert len(first.scenes) == 3 and first.estimated_seconds == 120, \
        "its scenes fill the agreed minutes"
    assert plan.length.understood == "About 5 min." and plan.shape_agreed_at
    assert len(fake.scene_prompts) == 5
    view = read_planning(slug)
    assert view["proposal"] is None
    assert "Scenes written for 5 section(s)" in view["messages"][-1]["text"]
    assert view["section_units"][first.id] == [1, 2], "matched on the server, for the page"
    assert view["section_units"][plan.sections[0].id] == [], "about no slide"


def test_a_revision_keeps_the_scenes_of_sections_that_did_not_change(project_root, monkeypatch):
    slug, project = a_deck_project("Revise", slides=3)
    revised = shape(("Opening", "Hook", [], 0.5, 1), ("First part", "Plain", [1, 2], 2, 3),
                    ("Second part, longer", "Plain", [3], 2.5, 4),
                    ("Recap", "Look back", [], 0.5, 1), ("Close", "One idea", [], 0.5, 1))
    fake = FakeModel(GOOD, revised)
    monkeypatch.setattr(plan_agent, "complete_structured", fake)
    send_message(slug, "Plan it.")
    agree(slug)
    kept = PlanStore(project.root).load().sections[1].scenes

    send_message(slug, "More time on the last slide.")
    assert read_planning(slug)["agree_calls"] == 1
    agree(slug)

    plan = PlanStore(project.root).load()
    assert plan.sections[1].scenes == kept, "unchanged slides and count: scenes kept"
    assert len(plan.sections[2].scenes) == 4
    assert len(fake.scene_prompts) == 5 + 1


def test_a_section_told_differently_gets_its_scenes_written_again(project_root, monkeypatch):
    slug, project = a_deck_project("Retold", slides=3)
    retold = shape(("Opening", "Hook", [], 0.5, 1), ("First part", "As a story", [1, 2], 2, 3),
                   ("Second part", "Plain", [3], 1.5, 2), ("Recap", "Look back", [], 0.5, 1),
                   ("Close", "One idea", [], 0.5, 1))
    monkeypatch.setattr(plan_agent, "complete_structured", FakeModel(GOOD, retold))
    send_message(slug, "Plan it.")
    agree(slug)

    send_message(slug, "Tell the first part as a story.")
    assert read_planning(slug)["agree_calls"] == 1, \
        "same slides and count, but a new direction: its scenes are stale"


def test_a_shape_proposed_before_the_source_changed_is_not_applied(project_root, monkeypatch):
    slug, project = a_deck_project("Moved", slides=3)
    monkeypatch.setattr(plan_agent, "complete_structured", FakeModel(GOOD))
    send_message(slug, "Plan it.")
    a_deck(project.root / "sources" / "deck.pptx", slides=4)
    operations.run_extraction(slug, "deck.pptx")
    operations.confirm_extraction(slug)

    with pytest.raises(OperationFailed, match="extracted again"):
        agree(slug)
    assert read_planning(slug)["proposal"], "kept, so the person sees what was proposed"
    assert PlanStore(project.root).load().sections == []


def test_a_proposal_can_be_discarded(project_root, monkeypatch):
    slug, _ = a_deck_project("Discard", slides=3)
    monkeypatch.setattr(plan_agent, "complete_structured", FakeModel(GOOD))
    send_message(slug, "Plan it.")

    view = discard_proposal(slug)
    assert view["proposal"] is None
    assert view["messages"][-1]["text"] == "(Discarded the proposed shape.)"


def test_slides_out_of_order_under_strict_block_the_transfer(project_root, monkeypatch):
    slug, project = a_deck_project("Blocked", slides=3)
    monkeypatch.setattr(plan_agent, "complete_structured", FakeModel(GOOD))
    send_message(slug, "Plan it.")
    agree(slug)
    plan = PlanStore(project.root).load()
    plan.sections[1], plan.sections[2] = plan.sections[2], plan.sections[1]
    PlanStore(project.root).save(plan)

    checks = {c["key"]: c for c in plan_checks(project, PlanStore(project.root).load())}
    assert checks["order"]["status"] == FAIL
    assert checks["scenes"]["status"] != FAIL


def test_the_setup_is_kept_in_the_person_s_words(project_root):
    slug, project = a_deck_project("Setup", slides=2)
    set_setup(slug, {"length_text": "approximately 1 hr but increase if required, not decrease",
                     "slide_order": "nearly", "audience": ""})
    plan = PlanStore(project.root).load()
    assert plan.length_text.startswith("approximately 1 hr")
    assert plan.slide_order == "nearly" and plan.audience == ""
    set_setup(slug, {"slide_order": "sideways"})
    assert PlanStore(project.root).load().slide_order == "strict", "unknown falls back"
