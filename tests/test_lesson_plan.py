"""The plan as a lesson: a frame around the body, time shared from the target,
objective links suggested by shared words, and summaries that say what the
viewer learns -- all by fixed rules, and the same every time."""

# ruff: noqa: F811
import pytest

from pipeline import operations, plan_summaries
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    Extraction,
    ExtractionStore,
)
from pipeline.lesson_plan import (
    ROLE_GUIDE,
    frame_source,
    objective_suggestions,
    set_lesson_frame,
    summary_problem,
    timing,
)
from pipeline.plan_handoff import plan_checks
from pipeline.planning import LearningObjective, Plan, PlanSection, PlanStore, SourceReference
from pipeline.scripting import Script, ScriptScene, SectionScript
from pipeline.slide_plan import plan_from_slides
from pipeline.stage_options import StageSettingsStore
from pipeline.stages import Stage
from tests.test_slide_first import a_deck_project, project_root  # noqa: F401


def deck(*slides):
    """An extraction of one deck: each slide is (title, words, pictures)."""
    blocks = []
    for number, (title, words, pictures) in enumerate(slides, 1):
        blocks.append(ContentBlock(kind=BlockKind.HEADING, text=title, heading_path=[title],
                                   slide_number=number))
        blocks.append(ContentBlock(kind=BlockKind.PARAGRAPH, text=words, heading_path=[title],
                                   slide_number=number))
        blocks.extend(ContentBlock(kind=BlockKind.FIGURE, text=f"{title} — figure",
                                   heading_path=[title], slide_number=number)
                      for _ in range(pictures))
    return Extraction(documents=[ExtractedDocument(file_name="deck.pptx", blocks=blocks)])


def slide_section(number, title, **extra):
    return PlanSection(id=f"slide-{number}", title=title, sources=[SourceReference(
        file_name="deck.pptx", heading_path=[title], slide_number=number)], **extra)


# --- the frame ------------------------------------------------------------------------


def test_a_plan_from_a_deck_is_a_lesson(project_root):
    slug, project = a_deck_project("Framed", slides=3)
    plan = PlanStore(project.root).load()
    plan.learning_objectives = [LearningObjective(id="o1", text="Know the headings")]
    PlanStore(project.root).save(plan)

    built = plan_from_slides(slug)

    assert [s["role"] for s in built["sections"]] == [
        "opening", "teach", "teach", "teach", "recap", "close"]
    assert built["sections"][0]["id"] == "frame-opening", "a fixed id keeps its narration"
    assert built["sections"][0]["objective_ids"] == ["o1"], "the opening promises each objective"
    assert built["sections"][4]["objective_ids"] == ["o1"], "the recap returns to each"
    assert built["sections"][1]["summary_origin"] == "rule", "a stand-in, and says so"


def test_the_frame_can_be_switched_off_and_on_without_losing_its_narration(project_root):
    slug, project = a_deck_project("Toggle", slides=2)
    plan_from_slides(slug)
    operations.write_section_script(slug, "frame-opening", "Welcome. Here is a question.")

    set_lesson_frame(slug, ["recap"])
    assert [s.role for s in PlanStore(project.root).load().sections] == [
        "teach", "teach", "recap"]
    set_lesson_frame(slug, ["opening", "recap", "close"])
    sections = PlanStore(project.root).load().sections
    assert [s.role for s in sections] == ["opening", "teach", "teach", "recap", "close"]
    assert operations.read_artifact(slug, "script")["section_scripts"][0]["section_id"] \
        == "frame-opening"


def test_reordering_keeps_the_frame_at_the_edges(project_root):
    slug, project = a_deck_project("Edges", slides=2)
    plan = operations.read_artifact(slug, "plan") | {}
    plan = plan_from_slides(slug)
    moved = [plan["sections"][4], *plan["sections"][:4]]     # Close dragged to the top
    saved = operations.save_artifact(slug, "plan", Plan.model_validate(plan | {"sections": moved}))
    assert [s["role"] for s in saved["sections"]] == [
        "opening", "teach", "teach", "recap", "close"]


def test_a_plan_from_before_the_frame_does_not_grow_one():
    older = Plan.model_validate({"sections": [{"title": "Kept as it was"}]})
    assert older.lesson_frame == []
    assert Plan().lesson_frame == ["opening", "recap", "close"], "new plans have it"


# --- time --------------------------------------------------------------------------------


def test_time_follows_the_material_and_stays_inside_the_target():
    extraction = deck(("Dense", " ".join(["word"] * 150), 0), ("Diagram", "few words", 3))
    plan = Plan(lesson_frame=[], sections=[slide_section(1, "Dense"),
                                           slide_section(2, "Diagram")])

    natural = timing(plan, extraction, (0, 10_000))
    assert natural["seconds"] == {"slide-1": 60, "slide-2": 37}, "words, and 12 s a picture"
    assert natural["scale"] == 1.0

    stretched = timing(plan, extraction, (180, 300))
    assert sum(stretched["seconds"].values()) in range(178, 183), "up to the target's start"
    assert stretched["is_stretched"], "97 s of material pushed to 3 min is padding"

    squeezed = timing(plan, extraction, (30, 50))
    assert squeezed["is_squeezed"]
    assert timing(plan, extraction, (180, 300)) == stretched, "the same every time"


def test_a_pinned_length_is_kept_and_the_rest_rebalance():
    extraction = deck(("One", " ".join(["w"] * 100), 0), ("Two", " ".join(["w"] * 100), 0))
    plan = Plan(lesson_frame=[], sections=[
        slide_section(1, "One", pinned=True, estimated_seconds=90), slide_section(2, "Two")])
    shares = timing(plan, extraction, (180, 300))
    assert shares["seconds"]["slide-1"] == 90
    assert shares["seconds"]["slide-2"] == 90, "the rest of the 3 min target"


def test_the_target_reaches_the_saved_plan(project_root):
    slug, project = a_deck_project("Target", slides=2)
    StageSettingsStore(project.root).save(Stage.SCENE_PLAN, {"target_duration": "3-5"})
    plan = plan_from_slides(slug)
    assert 180 <= sum(s["estimated_seconds"] for s in plan["sections"]) <= 300


# --- objectives -----------------------------------------------------------------------------


def test_links_are_suggested_by_the_words_they_share():
    extraction = deck(("Padma's story", "Padma danced Bharatanatyam as a child", 0),
                      ("Anorexia nervosa", "An eating disorder with voluntary weight loss", 0))
    plan = Plan(lesson_frame=[], sections=[slide_section(1, "Padma's story"),
                                           slide_section(2, "Anorexia nervosa")],
                learning_objectives=[
                    LearningObjective(id="story", text="Retell Padma's story as a dancer"),
                    LearningObjective(id="illness", text="Explain what anorexia nervosa is")])

    found = {(s["section_id"], s["objective_id"]): s["words"]
             for s in objective_suggestions(plan, extraction)}
    assert set(found) == {("slide-1", "story"), ("slide-2", "illness")}
    assert found[("slide-2", "illness")] == ["anorexia", "nervosa"], "it says why"

    plan.sections[1].objective_ids = ["illness"]
    assert ("slide-2", "illness") not in {
        (s["section_id"], s["objective_id"]) for s in objective_suggestions(plan, extraction)}


# --- summaries --------------------------------------------------------------------------------


@pytest.mark.parametrize(("summary", "origin", "problem"), [
    ("", "", "no summary"),
    ("Feeling the World", "rule", "a stand-in (the title)"),
    ("Line one\nLine two of the slide", "", "source text, not a summary"),
    ("This chapter explores body image.", "ai", "talks about the source"),
    ("How the brain builds a picture of the body.", "ai", ""),
])
def test_a_summary_says_what_the_viewer_learns(summary, origin, problem):
    section = PlanSection(title="Feeling the World", summary=summary, summary_origin=origin)
    assert summary_problem(section) == problem


class FakeSummaries:
    def __init__(self, ids):
        self.ids = ids

    def __call__(self, model, system_prompt, user_prompt):
        return model(summaries=[{"section_id": i, "summary": f"What {i} teaches."}
                                for i in [*self.ids, "made-up"]])


def test_ai_summaries_are_proposals_until_accepted(project_root, monkeypatch):
    slug, project = a_deck_project("Summaries", slides=2)
    plan_from_slides(slug)
    monkeypatch.setattr(plan_summaries, "complete_structured",
                        FakeSummaries(["slide-001", "slide-002"]))

    view = plan_summaries.propose_summaries(slug)
    assert set(view["proposals"]) == {"slide-001", "slide-002"}, "made-up ids are dropped"
    assert PlanStore(project.root).load().sections[1].summary == "Heading number 1", \
        "nothing in the plan changes until accepted"

    plan_summaries.accept_summaries(slug, ["slide-001"])
    first = PlanStore(project.root).load().sections[1]
    assert (first.summary, first.summary_origin) == ("What slide-001 teaches.", "ai")
    plan_summaries.dismiss_summaries(slug)
    assert operations.read_artifact(slug, "plan")["lesson"]["summaries"]["proposals"] == {}


# --- what the Scripting agent gets -------------------------------------------------------------


def test_the_recap_is_written_from_what_the_body_said():
    plan = Plan(learning_objectives=[LearningObjective(text="Name the lobes")], sections=[
        PlanSection(id="b", title="Lobes", summary="The four lobes and what each does.")])
    script = Script(section_scripts=[SectionScript(section_id="b", scenes=[
        ScriptScene(narration="The frontal lobe plans.", brief="x")])])
    recap = PlanSection(id="frame-recap", role="recap", title="Recap")

    source = frame_source(plan, script, recap)
    assert "1. Name the lobes" in source and "The frontal lobe plans." in source
    assert "one short beat each" in ROLE_GUIDE["recap"]


def test_stand_in_summaries_are_not_passed_on_as_summaries():
    from pipeline.script_drafting import _section_brief

    plan = Plan(sections=[PlanSection(title="Anorexia", summary="Anorexia",
                                      summary_origin="rule")])
    brief = _section_brief(plan, plan.sections[0], 100)
    assert "Summary: (none given)" in brief


# --- the checks --------------------------------------------------------------------------------


def test_the_checks_judge_the_lesson(project_root):
    slug, project = a_deck_project("Checked", slides=2)
    ExtractionStore(project.root).load()
    plan = PlanStore(project.root).load()
    plan.learning_objectives = [LearningObjective(id="o1", text="Something unrelated")]
    PlanStore(project.root).save(plan)
    plan_from_slides(slug)

    checks = {c["key"]: c for c in plan_checks(project, PlanStore(project.root).load())}
    assert checks["frame"]["status"] == "pass"
    assert checks["has-sources"]["status"] == "pass", "the frame needs no source"
    assert checks["objectives"]["status"] == "warn", \
        "the frame serving every objective is not the body teaching one"
    assert checks["summaries"]["status"] == "warn" and "stand-in" in checks["summaries"]["detail"]
