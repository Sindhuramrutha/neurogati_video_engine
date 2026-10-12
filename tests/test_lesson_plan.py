"""No fixed kinds of section: every section is the planning agent's, in its own
words, and one about no slide is written from the rest of the plan."""

# ruff: noqa: F811
from pipeline.lesson_plan import plan_source
from pipeline.planning import Plan, PlanSection
from pipeline.scripting import Script, ScriptScene, SectionScript
from tests.test_slide_first import project_root  # noqa: F401


def test_a_plan_with_old_roles_and_a_frame_still_loads():
    older = Plan.model_validate({"lesson_frame": ["opening"], "sections": [
        {"title": "Kept as it was", "role": "story"}]})
    assert older.sections[0].title == "Kept as it was"


def test_a_section_s_length_is_its_scenes():
    section = PlanSection.model_validate({"estimated_seconds": 999, "scenes": [
        {"does": "one", "seconds": 20}, {"does": "two", "seconds": 40}]})
    assert section.estimated_seconds == 60


def test_a_section_about_no_slide_is_written_from_what_the_others_said():
    plan = Plan(sections=[
        PlanSection(id="b", title="Lobes", summary="The four lobes and what each does."),
        PlanSection(id="r", title="Looking back", how="Walk back through each section.")])
    script = Script(section_scripts=[SectionScript(section_id="b", scenes=[
        ScriptScene(narration="The frontal lobe plans.", brief="x")])])

    source = plan_source(plan, script, plan.sections[1])
    assert "Lobes" in source and "The frontal lobe plans." in source
    assert "(this section) Looking back" in source
