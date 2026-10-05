"""Scene Plan hand-off: fixed checks, a transfer they gate, and later stages
reading only what was transferred once anything was."""
# ruff: noqa: F811

import pytest

from pipeline import operations
from pipeline.operations import OperationFailed
from pipeline.plan_handoff import (
    FAIL,
    PASS,
    WARN,
    plan_checks,
    plan_for_later_stages,
    read_plan_handoff,
    transfer_plan,
)
from pipeline.planning import PlanSection, PlanStore, SourceReference
from tests.test_generation import project_root, scripted_project  # noqa: F401


def statuses(project):
    return {c["key"]: c["status"] for c in plan_checks(project, PlanStore(project.root).load())}


def test_later_stages_read_the_working_plan_until_the_first_transfer(project_root):
    slug, project = scripted_project("Before")
    plan = PlanStore(project.root).load()
    plan.sections[0].title = "Renamed while working"
    PlanStore(project.root).save(plan)

    assert plan_for_later_stages(project).sections[0].title == "Renamed while working"


def test_after_a_transfer_later_stages_read_only_the_transferred_plan(project_root):
    slug, project = scripted_project("After")
    transfer_plan(slug)
    plan = PlanStore(project.root).load()
    plan.sections[0].title = "An edit in progress"
    PlanStore(project.root).save(plan)

    assert plan_for_later_stages(project).sections[0].title == "Signals"
    assert read_plan_handoff(slug)["pending"] is True
    script = operations.read_artifact(slug, "script")
    assert [s["title"] for s in script["plan_sections"]] == ["Signals"], \
        "the script page is written against the transferred plan"

    transfer_plan(slug)
    assert plan_for_later_stages(project).sections[0].title == "An edit in progress"
    assert read_plan_handoff(slug)["pending"] is False


def test_a_section_pointing_at_missing_content_blocks_the_transfer(project_root):
    slug, project = scripted_project("Missing")
    plan = PlanStore(project.root).load()
    plan.sections.append(PlanSection(title="Ghost", sources=[
        SourceReference(file_name="chapter.docx", heading_path=["No such heading"])]))
    PlanStore(project.root).save(plan)

    assert statuses(project)["sources-exist"] == FAIL
    with pytest.raises(OperationFailed, match="Sources exist"):
        transfer_plan(slug)


def test_an_empty_plan_fails_and_warnings_do_not_block(project_root):
    slug, project = scripted_project("Checks")
    assert statuses(project)["sections"] == PASS
    plan = PlanStore(project.root).load()
    plan.sections[0].estimated_seconds = 3            # unusually short: a warning
    PlanStore(project.root).save(plan)
    assert statuses(project)["durations"] == WARN
    transfer_plan(slug)                                # allowed

    PlanStore(project.root).save(plan.model_copy(update={"sections": []}))
    assert statuses(project)["sections"] == FAIL


def test_the_checks_are_the_same_every_time(project_root):
    slug, project = scripted_project("Same")
    assert plan_checks(project, PlanStore(project.root).load()) \
        == plan_checks(project, PlanStore(project.root).load())
