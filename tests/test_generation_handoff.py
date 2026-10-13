"""Generation hand-off: the scenes must match the script and be made, the render
reads the transferred scenes, and a transfer freezes the files it points at."""
# ruff: noqa: F811

import pytest

from pipeline import operations
from pipeline.generation import VisualPlanStore
from pipeline.generation_handoff import (
    FAIL,
    generation_checks,
    read_generation_handoff,
    transfer_generation,
)
from pipeline.operations import OperationFailed
from pipeline.scripting import ScriptScene, ScriptStore
from tests.test_generation import project_root, scripted_project  # noqa: F401


def made_project(name):
    """Planned and 'made' by hand: a clip on disk for every scene."""
    slug, project = scripted_project(name, figures=0, scenes=2)
    operations.plan_visuals(slug)
    store = VisualPlanStore(project.root)
    plan = store.load()
    (project.root / "generation" / "scenes").mkdir(parents=True, exist_ok=True)
    for visual in plan.visuals:
        path = project.root / "generation" / "scenes" / f"scene-{visual.id}.mp4"
        path.write_bytes(b"first clip " + visual.id.encode())
        visual.clip_path = f"generation/scenes/scene-{visual.id}.mp4"
        visual.headline = "A headline"
    store.save(plan)
    return slug, project


def statuses(project):
    return {c["key"]: c["status"] for c in
            generation_checks(project, VisualPlanStore(project.root).load())}


def test_an_unmade_scene_blocks_the_transfer(project_root):
    slug, project = scripted_project("Unmade", figures=0, scenes=1)
    operations.plan_visuals(slug)
    assert statuses(project)["made"] == FAIL
    with pytest.raises(OperationFailed, match="Every scene made"):
        transfer_generation(slug)


def test_scenes_of_removed_script_scenes_block_the_transfer(project_root):
    slug, project = made_project("Removed scene")
    script = ScriptStore(project.root).load()
    script.section_scripts[0].scenes = [ScriptScene(narration="Only a new scene now.")]
    ScriptStore(project.root).save(script)

    assert statuses(project)["match"] == FAIL


def test_every_scene_is_flagged_for_a_look(project_root):
    slug, project = made_project("Watched")
    handoff = read_generation_handoff(slug)
    watched = next(c for c in handoff["checks"] if c["key"] == "watched")
    assert watched["status"] == "warn" and "Watch each" in watched["detail"]


def test_leftover_narration_needs_no_scene(project_root):
    """Narration from sections the plan dropped is never rendered."""
    from pipeline.scripting import SectionScript

    slug, project = made_project("Leftover scenes")
    script = ScriptStore(project.root).load()
    script.section_scripts.append(SectionScript(
        section_id="dropped", scenes=[ScriptScene(narration="From an older plan.")]))
    ScriptStore(project.root).save(script)

    assert statuses(project)["match"] == "pass"


def test_with_no_scenes_it_does_not_claim_every_scene_is_approved(project_root):
    """An empty Generation page read "Every scene's program passed and is
    approved." -- true of no scenes, and wrong to tell anyone."""
    slug, project = scripted_project("Nothing yet", figures=0, scenes=1)
    checks = {c["key"]: c for c in
              generation_checks(project, VisualPlanStore(project.root).load())}
    assert checks["programs"]["status"] == "n/a"
    assert checks["programs"]["detail"] == "No scenes are set up yet."
