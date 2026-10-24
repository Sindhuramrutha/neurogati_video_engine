"""One scene leads into the next: joins planned, held to, found wrong by code, and
smoothed where sections meet -- from v8's script, where they did not."""

import pytest

from pipeline import scene_joins
from pipeline.planning import Plan, PlanScene, PlanSection
from pipeline.scene_joins import JoinFix, fit_joins, join_problems
from pipeline.scripting import Script, ScriptScene, SectionScript
from tests.test_project_delete import project_root  # noqa: F401


def test_a_section_s_first_and_last_scenes_take_its_joins_and_it_ends_on_a_breath():
    section = PlanSection(title="Ancient debate", opens_on="answers: where does thought live?",
                          ends_on="hands on: who looked inside the body first")
    scenes = fit_joins(section, [PlanScene(does="Hippocrates"), PlanScene(does="Aristotle")])

    assert scenes[0].opens_on == "answers: where does thought live?"
    assert scenes[-1].ends_on == "hands on: who looked inside the body first"
    assert scenes[-1].pause_after == scene_joins.SECTION_TURN_PAUSE
    assert PlanScene(pause_after=9).pause_after == 2.0, "never more than two seconds"


def written(plan, *sections):
    return Script(section_scripts=[
        SectionScript(section_id=plan.sections[index].id,
                      scenes=[ScriptScene(id=f"{index}-{n}", narration=text)
                              for n, text in enumerate(texts)])
        for index, texts in enumerate(sections)])


def three(course="Demystifying the Brain"):
    return Plan(course=course, this_video="Chapter 1",
                sections=[PlanSection(title=t) for t in ("Opening", "Middle", "Close")])


def test_a_question_asked_again_across_a_join_is_found():
    """v8: scene 2 ended 'Where does thought live?' and scene 3 opened by asking it."""
    plan = three()
    script = written(plan, ["Welcome. Let's start where the argument started. "
                            "Where does thought live?"],
                     ["Now let's begin with a question. Where does thought live? The heart?"],
                     ["That is the story."])

    assert ("1-0", "opens by repeating what the scene before ended on") in \
        join_problems(plan, script)


def test_the_course_named_mid_video_and_a_described_picture_are_found():
    """v8 announced 'Chapter one of Demystifying the Brain' in its third section, and
    said 'This portrait is Galen' instead of teaching."""
    plan = three()
    script = written(plan, ["Welcome to Demystifying the Brain, Chapter 1."],
                     ["We are in Demystifying the Brain again. This portrait is Galen."],
                     ["That was Demystifying the Brain."])
    found = join_problems(plan, script)

    assert ("1-0", "announces the course or part in the middle of the video") in found
    assert ("1-0", "describes the picture instead of teaching") in found
    opening_and_close = [where for where, _ in found if where in ("0-0", "2-0")]
    assert not opening_and_close, "the opening and close may name it"


@pytest.mark.real_joins
def test_a_join_is_smoothed_by_a_small_edit_and_never_rewritten(project_root,  # noqa: F811
                                                                 monkeypatch):
    from pipeline import operations
    from pipeline.planning import PlanStore
    from pipeline.scripting import ScriptStore

    slug = operations.create_project("Joins")["slug"]
    project_dir = project_root / slug
    plan = three()
    PlanStore(project_dir).save(plan)
    ScriptStore(project_dir).save(written(
        plan, ["Galen mapped the parts. Where does thought live, then?"],
        ["Where does thought live, then? The microscope would answer that."],
        ["So the brain is a network."]))
    monkeypatch.setattr("pipeline.fact_ledger.forbidden_for", lambda project, section: [])

    def model(response_model, system, user, **kwargs):
        before = user.split("--- the earlier scene ---\n")[1].split("\n\n")[0]
        after = user.split("--- the later scene ---\n")[1]
        if "microscope" in after:          # a small edit at the join: kept
            return JoinFix(before=before, after=after.replace(
                "Where does thought live, then? ", "To answer that, "))
        return JoinFix(before="Something else entirely, rewritten.", after=after)

    monkeypatch.setattr("pipeline.llm.complete_structured", model)

    notes = scene_joins.smooth_joins(slug)

    scenes = {s.id: s.narration for w in ScriptStore(project_dir).load().section_scripts
              for s in w.scenes}
    assert scenes["1-0"] == "To answer that, The microscope would answer that."
    assert scenes["2-0"] == "So the brain is a network.", "a rewrite is not kept"
    assert scenes["0-0"].startswith("Galen mapped"), "only what changed at the join"
    assert len(notes) == 1
