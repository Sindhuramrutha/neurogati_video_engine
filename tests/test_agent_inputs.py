"""The stage agents see their own work: asked to review Chapter 1, the Assets,
Generation and Export agents answered that they could not see their inputs."""

import json

from pipeline.agent_runtime import stage_context
from pipeline.scene_lab import scene_folder
from pipeline.stages import Stage
from tests.test_scene_lab import project_root, scripted_project  # noqa: F401


def test_the_generation_and_export_agents_see_each_scene_s_checks(project_root):  # noqa: F811
    slug, project, visual = scripted_project("Seen")
    folder = scene_folder(project, visual, create=True)
    (folder / "checks.json").write_text(json.dumps({"checks": [
        {"name": "No shapes collide", "status": "fail"},
        {"name": "Text is large enough", "status": "pass"}]}), encoding="utf-8")
    (folder / "agent.json").write_text(json.dumps({
        "status": "done", "renders": 5,
        "last_render": {"scores": {"teaches": 2}, "problems": ["Name the heart."]}}),
        encoding="utf-8")

    generation = stage_context(project, Stage.GENERATION)
    assert "status done; rounds 5; FAILING: No shapes collide" in generation
    assert '"teaches": 2' in generation and "still wanted: Name the heart." in generation
    assert "--- scenes ---" in stage_context(project, Stage.REVIEWING)
    assert "Blocks the export:" in stage_context(project, Stage.EXPORT)
