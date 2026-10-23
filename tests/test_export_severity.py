"""A scene in the video whose own checks still fail is a visible defect: it blocks the
hand-over unless the export is built as a draft on purpose. A scene that passes its
checks but is below the reviewer's bar is worth knowing, counted once.

Demystifying the Brain, Chapter 1 exported with 0 blockers and 53 warnings: 52 scenes
below the bar, one of them with text drawn over text, and the pages called it ready.
"""

# ruff: noqa: F811
import json

from pipeline.exporting import build_export, read_export, scene_problems
from pipeline.generation import VisualPlanStore
from pipeline.presentation import present_artifact
from pipeline.review import ReviewStore
from pipeline.scene_program import scene_folder
from tests.test_scene_lab import scripted_project
from tests.test_slide_first import project_root  # noqa: F401


def with_clips(project, failing: dict[int, list[str]], below: set[int]):
    """Every scene given a clip; some with failing checks, some only below the bar."""
    store = VisualPlanStore(project.root)
    plan = store.load()
    for index, visual in enumerate(plan.visuals):
        folder = scene_folder(project, visual, create=True)
        visual.clip_path = f"generation/scenes/{folder.name}/render.mp4"
        names = failing.get(index, [])
        (folder / "checks.json").write_text(json.dumps({"checks": [
            {"key": "x", "name": name, "status": "fail"} for name in names]
            + [{"key": "ok", "name": "Ran", "status": "pass"}]}), encoding="utf-8")
        visual.below_bar = "the reviewer still wants more" if (names or index in below) else ""
    store.save(plan)
    return plan.visuals


def test_scenes_are_sorted_by_how_bad(project_root):
    slug, project, _ = scripted_project("Severity")
    visuals = with_clips(project, {0: ["No overlapping text"]}, {1})

    problems = scene_problems(project)

    assert [e["visual_id"] for e in problems["failing"]] == [visuals[0].id]
    assert problems["failing"][0]["checks"] == ["No overlapping text"]
    assert [e["visual_id"] for e in problems["below_bar"]] == [visuals[1].id]


def test_a_failing_scene_blocks_the_export_unless_it_is_built_as_a_draft(project_root):
    slug, project, _ = scripted_project("Blocked")
    with_clips(project, {0: ["No overlapping text", "No blank frame"]}, {1})

    built = build_export(slug)
    assert any("still fail their own checks" in b and "No overlapping text" in b
               for b in built["blockers"])
    assert not built["draft"]
    assert sum("below the reviewer's bar" in w for w in built["warnings"]) == 1, \
        "the reviewer-only scenes are one line, not one each"

    drafted = build_export(slug, draft=True)
    assert drafted["draft"]
    assert not any("still fail their own checks" in b for b in drafted["blockers"])
    assert any(w.startswith("Accepted as a draft:") for w in drafted["warnings"])
    assert read_export(slug)["draft"], "the page reads that it was built as a draft"


def test_a_draft_is_not_claimed_when_nothing_fails(project_root):
    slug, project, _ = scripted_project("Nothing fails")
    with_clips(project, {}, set())
    assert not build_export(slug, draft=True)["draft"]


def test_reviewing_is_not_ready_while_a_scene_fails_its_checks(project_root):
    slug, project, _ = scripted_project("Review severity")
    with_clips(project, {0: ["No blank frame"]}, set())

    shown = present_artifact(project, "review", ReviewStore(project.root).load())

    assert shown["is_ready_to_export"] is False
    assert shown["scene_problems"]["failing"][0]["checks"] == ["No blank frame"]
