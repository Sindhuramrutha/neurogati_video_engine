"""Planning approaches: a choice, a few options and your own words decide how the
outline is built -- and a section may cover several slides, shown in turn."""

# ruff: noqa: F811
import pytest

from pipeline import operations, plan_drafting
from pipeline.extraction import ExtractionStore
from pipeline.operations import OperationFailed
from pipeline.plan_approaches import build_outline, instruction_for
from pipeline.plan_drafting import OutlineSection
from pipeline.planning import PlanSection, PlanStore, SourceReference
from pipeline.slide_plan import coverage_of, slide_for_scene, slides_in
from tests.test_plan_drafting import FakeModel, outline_of
from tests.test_slide_first import a_deck_project, project_root  # noqa: F401


def test_an_approach_always_sends_the_same_instruction():
    sent = instruction_for("story-first", {"sections": "few", "longest": "90"},
                           "Keep Padma's story together.")
    assert "Lead with the story" in sent
    assert "Use 3 to 5 sections." in sent and "longer than 90 seconds" in sent
    assert sent.endswith("Keep Padma's story together.")
    assert sent == instruction_for("story-first", {"sections": "few", "longest": "90"},
                                   "Keep Padma's story together.")
    assert instruction_for("follow-deck", {}, "ignored") == "", "no AI, so nothing is sent"


def test_following_the_deck_is_an_approach_and_is_remembered(project_root):
    slug, project = a_deck_project("Deck approach", slides=3)
    made = build_outline(slug, "follow-deck", {"merged": "first"}, "")
    plan = PlanStore(project.root).load()
    assert made == {"made": "plan"}
    assert plan.approach == "follow-deck" and plan.approach_options["merged"] == "first"
    assert len([s for s in plan.sections if s.role == "teach"]) == 3


def test_a_choice_that_is_not_offered_is_refused(project_root):
    slug, _ = a_deck_project("Refused", slides=2)
    with pytest.raises(OperationFailed):
        build_outline(slug, "improvise", {}, "")
    with pytest.raises(OperationFailed):
        build_outline(slug, "group-ideas", {"sections": "hundreds"}, "")


def test_an_ai_approach_drafts_with_its_instruction_and_finds_the_slides(
    project_root, monkeypatch
):
    slug, project = a_deck_project("Grouped", slides=4)
    index = plan_drafting.outline_for_agent(ExtractionStore(project.root).load())[2]
    ids = {reference.heading_path[-1]: key for key, reference in index.items()
           if reference.heading_path}
    model = FakeModel(outline_of(
        OutlineSection(title="The first idea", role="story",
                       source_ids=[ids["Heading number 1"], ids["Heading number 2"]]),
        OutlineSection(title="The second idea",
                       source_ids=[ids["Heading number 3"], ids["Heading number 4"]])))
    monkeypatch.setattr(plan_drafting, "complete_structured", model)

    made = build_outline(slug, "group-ideas", {}, "Two ideas only.")

    assert made == {"made": "draft"}
    assert "Group neighbouring parts" in model.outline_prompts[0]
    assert "Two ideas only." in model.outline_prompts[0]
    draft = operations.read_plan_draft(slug)
    sections = draft["plan"]["sections"]
    assert [[s["slide_number"] for s in section["sources"]] for section in sections] == [
        [1, 2], [3, 4]], "each drafted section knows the slides it covers"
    assert sections[0]["role"] == "story"
    assert PlanStore(project.root).load().sections == [], "a draft; the plan is untouched"


def two_slide_section():
    return PlanSection(sources=[
        SourceReference(file_name="deck.pptx", heading_path=["A"], slide_number=2),
        SourceReference(file_name="deck.pptx", heading_path=["B"], slide_number=3)])


def test_a_section_of_several_slides_moves_through_them_as_its_scenes_go():
    section = two_slide_section()
    assert [slide_for_scene(section, i, 4) for i in range(4)] == [2, 2, 3, 3]
    assert [slide_for_scene(section, i, 3) for i in range(3)] == [2, 2, 3]
    assert [slide_for_scene(section, i, 1) for i in range(1)] == [2], "one scene, one slide"
    assert [slide_for_scene(section, i, 4, "first") for i in range(4)] == [2, 2, 2, 2]


def test_a_merged_section_still_covers_every_one_of_its_slides(project_root):
    slug, project = a_deck_project("Merged", slides=3)
    slides = slides_in(ExtractionStore(project.root).load())
    first = PlanSection(sources=[SourceReference(file_name="deck.pptx", slide_number=1)])
    merged = two_slide_section()
    coverage = coverage_of(slides, [first, merged])
    assert coverage["is_complete"], "slides 2 and 3 are both covered by the one section"
