"""Finishing the video from the app: until this, a person at a terminal remade the
failing scenes, queued the render when they were done, and built the export after."""

import json

from pipeline import finishing
from pipeline.generation import VisualPlanStore
from pipeline.scene_lab import scene_folder
from tests.test_scene_lab import project_root, scripted_project  # noqa: F401


def test_finishing_remakes_failing_scenes_then_renders_then_exports(project_root,  # noqa: F811
                                                                     monkeypatch):
    slug, project, visual = scripted_project("Finish")
    store = VisualPlanStore(project.root)
    plan = store.load()
    plan.visuals[0].clip_path = "clip.mp4"
    store.save(plan)
    folder = scene_folder(project, plan.visuals[0], create=True)
    (folder / "checks.json").write_text(json.dumps({"checks": [
        {"name": "No shapes collide", "status": "fail"}]}), encoding="utf-8")

    started, jobs = [], []
    monkeypatch.setattr(finishing, "POLL_SECONDS", 0)
    monkeypatch.setattr("pipeline.scene_agent.start",
                        lambda slug, ids, fresh=False: started.append((tuple(ids), fresh)))
    monkeypatch.setattr("pipeline.scene_agent.is_working", lambda slug: False)
    monkeypatch.setattr("pipeline.scene_approval.approve_passed", lambda slug: {})
    monkeypatch.setattr("pipeline.render_queue.add_job",
                        lambda slug, provider, voice: jobs.append(
                            {"id": "new", "slug": slug, "status": "done"}))
    monkeypatch.setattr("pipeline.render_queue.queue_view", lambda: {"jobs": list(jobs)})
    monkeypatch.setattr("pipeline.exporting.build_export",
                        lambda slug: {"blockers": [], "warnings": [], "duration_ms": 5})

    finishing._run(slug)

    remade = [ids for ids, fresh in started if fresh]
    assert remade and plan.visuals[0].id in remade[0], "failing scene made again, fresh"
    assert finishing.status(slug)["state"] == "done"
