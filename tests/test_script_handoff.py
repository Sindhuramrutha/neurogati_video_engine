"""Script & Staging hand-off: fixed checks, a transfer they gate, leftovers
cleared in one step, and later stages reading what was transferred."""
# ruff: noqa: F811

import pytest

from pipeline.operations import OperationFailed
from pipeline.planning import PlanSection, PlanStore
from pipeline.script_handoff import (
    FAIL,
    PASS,
    delete_unattached_narration,
    read_script_handoff,
    script_checks,
    script_for_later_stages,
    transfer_script,
)
from pipeline.scripting import ScriptScene, ScriptStore, SectionScript
from tests.test_generation import project_root, scripted_project  # noqa: F401


def statuses(project):
    return {c["key"]: c["status"] for c in script_checks(project, ScriptStore(project.root).load())}


def narration(project):
    return script_for_later_stages(project).body_for("s1")


def test_after_a_transfer_later_stages_read_only_the_transferred_script(project_root):
    slug, project = scripted_project("Script after")
    assert narration(project).startswith("Scene 1"), "the working script before any transfer"
    transfer_script(slug)

    script = ScriptStore(project.root).load()
    script.section_scripts[0].scenes[0].narration = "A sentence being rewritten"
    ScriptStore(project.root).save(script)

    assert narration(project).startswith("Scene 1"), "the edit has not reached later stages"
    assert read_script_handoff(slug)["pending"] is True
    transfer_script(slug)
    assert narration(project).startswith("A sentence being rewritten")


def test_an_unwritten_section_blocks_the_transfer(project_root):
    slug, project = scripted_project("Unwritten")
    plan = PlanStore(project.root).load()
    plan.sections.append(PlanSection(id="s2", title="Not written yet"))
    PlanStore(project.root).save(plan)

    assert statuses(project)["written"] == FAIL
    with pytest.raises(OperationFailed, match="Every section has narration"):
        transfer_script(slug)


def test_an_undefined_variable_blocks_the_transfer(project_root):
    slug, project = scripted_project("Variable")
    script = ScriptStore(project.root).load()
    script.section_scripts[0].scenes[0].narration = "Welcome to {{COURSE}}."
    ScriptStore(project.root).save(script)

    assert statuses(project)["variables"] == FAIL
    with pytest.raises(OperationFailed, match="Variables defined"):
        transfer_script(slug)


def test_leftover_narration_is_cleared_in_one_step(project_root):
    slug, project = scripted_project("Leftovers")
    script = ScriptStore(project.root).load()
    script.section_scripts += [
        SectionScript(section_id=f"gone-{n}", scenes=[ScriptScene(narration=f"Old {n}")])
        for n in range(3)]
    ScriptStore(project.root).save(script)
    assert statuses(project)["unattached"] != PASS

    result = delete_unattached_narration(slug)

    assert result["removed"] == 3
    kept = [s.section_id for s in ScriptStore(project.root).load().section_scripts]
    assert kept == ["s1"], "the section the plan has is kept"


def test_the_checks_are_the_same_every_time(project_root):
    slug, project = scripted_project("Same script")
    script = ScriptStore(project.root).load()
    assert script_checks(project, script) == script_checks(project, script)


def test_narration_that_reports_on_the_source_is_flagged(project_root):
    slug, project = scripted_project("Reporting")
    script = ScriptStore(project.root).load()
    script.section_scripts[0].scenes[0].narration = "The chapter opens with a line from Plato."
    ScriptStore(project.root).save(script)

    voice = next(c for c in script_checks(project, ScriptStore(project.root).load())
                 if c["key"] == "voice")
    assert voice["status"] == "warn" and "The chapter opens" in voice["detail"]
