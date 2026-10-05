"""Generation hand-off: the shots must match the script and be made, the render
reads the transferred shots, and a transfer freezes the files it points at."""
# ruff: noqa: F811

import pytest

from pipeline import operations
from pipeline.generation import VisualKind, VisualPlanStore
from pipeline.generation_handoff import (
    FAIL,
    generation_checks,
    make_preview,
    read_generation_handoff,
    transfer_generation,
    visuals_for_later_stages,
)
from pipeline.operations import OperationFailed
from pipeline.scripting import ScriptScene, ScriptStore
from tests.test_generation import project_root, scripted_project  # noqa: F401


def made_project(name):
    """Planned and 'made' by hand: a drawn picture on disk for every scene."""
    slug, project = scripted_project(name, figures=0, scenes=2)
    operations.plan_visuals(slug)
    store = VisualPlanStore(project.root)
    plan = store.load()
    (project.root / "generation" / "assets").mkdir(parents=True, exist_ok=True)
    for visual in plan.visuals:
        path = project.root / "generation" / "assets" / f"scene-{visual.id}.png"
        path.write_bytes(b"first picture " + visual.id.encode())
        visual.kind = VisualKind.GENERATED_IMAGE
        visual.asset_path = f"generation/assets/scene-{visual.id}.png"
        visual.headline = "A headline"
    store.save(plan)
    return slug, project


def statuses(project):
    return {c["key"]: c["status"] for c in
            generation_checks(project, VisualPlanStore(project.root).load())}


def test_a_transfer_freezes_the_pictures_the_render_reads(project_root):
    slug, project = made_project("Frozen")
    transfer_generation(slug)
    shot = visuals_for_later_stages(project).visuals[0]
    assert shot.asset_path.startswith("generation/transferred/")
    frozen = (project.root / shot.asset_path).read_bytes()

    # Making the scene again rewrites the working file in place...
    working = VisualPlanStore(project.root).load().visuals[0]
    (project.root / working.asset_path).write_bytes(b"a different picture")

    # ...and the transferred shot still shows exactly what was transferred.
    assert (project.root / visuals_for_later_stages(project).visuals[0].asset_path) \
        .read_bytes() == frozen


def test_an_unmade_shot_blocks_the_transfer(project_root):
    slug, project = scripted_project("Unmade", figures=0, scenes=1)
    operations.plan_visuals(slug)
    assert statuses(project)["made"] == FAIL
    with pytest.raises(OperationFailed, match="Every shot made"):
        transfer_generation(slug)


def test_shots_from_removed_scenes_block_the_transfer(project_root):
    slug, project = made_project("Removed scene")
    script = ScriptStore(project.root).load()
    script.section_scripts[0].scenes = [ScriptScene(narration="Only a new scene now.")]
    ScriptStore(project.root).save(script)

    assert statuses(project)["match"] == FAIL


def test_the_page_says_in_advance_what_make_will_ask_a_model_for(project_root):
    slug, project = scripted_project("Preview", figures=0, scenes=2)
    operations.plan_visuals(slug)
    preview = make_preview(project, VisualPlanStore(project.root).load())
    assert preview["to_make"] == 2 and preview["ai_words"] == 2


def test_drawn_pictures_are_flagged_for_a_look(project_root):
    slug, project = made_project("Drawn")
    handoff = read_generation_handoff(slug)
    drawn = next(c for c in handoff["checks"] if c["key"] == "ai-pictures")
    assert drawn["status"] == "warn" and "image model" in drawn["detail"]


def test_leftover_narration_needs_no_shot(project_root):
    """Narration from sections the plan dropped is never rendered."""
    from pipeline.scripting import SectionScript

    slug, project = made_project("Leftover scenes")
    script = ScriptStore(project.root).load()
    script.section_scripts.append(SectionScript(
        section_id="dropped", scenes=[ScriptScene(narration="From an older plan.")]))
    ScriptStore(project.root).save(script)

    assert statuses(project)["match"] == "pass"
