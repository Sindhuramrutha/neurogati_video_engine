"""Every scene is a program: a folder with a scene.py that is run, checked by
fixed rules, previewed with its own narration, and approved before the render
may use it."""

# ruff: noqa: F811
import shutil

import pytest

from pipeline import operations
from pipeline.generation import VisualPlanStore
from pipeline.scene_approval import approve_passed, approve_scene
from pipeline.scene_author import add_resource, resource_index
from pipeline.scene_lab import (
    read_scene,
    resources_root,
    run_scene,
    save_scene_code,
    scene_folder,
)
from pipeline.scene_program import save_spec
from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript
from tests.test_slide_first import a_deck_project, plan_from_slides, project_root  # noqa: F401

pytestmark = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")), reason="needs ffmpeg")

CRASHES = "raise RuntimeError('the scene went wrong')\n"
BLANK = '''
from scenekit import VideoWriter, canvas, load_brief
brief = load_brief()
with VideoWriter(brief) as video:
    for _ in range(brief.frames):
        video.write(canvas(brief)[0])
'''
# A program that changes throughout: a bar grows across the frame under a short
# label, so every sampled moment differs.
GOOD = '''
from scenekit import VideoWriter, canvas, font, load_brief
brief = load_brief()
with VideoWriter(brief) as video:
    for n in range(brief.frames):
        t = n / max(1, brief.frames - 1)
        image, draw = canvas(brief)
        draw.text((200, 200), "Touch", font=font(brief, 72), fill=brief.look["text"])
        draw.rectangle([200, 500, 200 + int(1500 * t), 700], fill=brief.look["accent"])
        video.write(image)
'''
TOO_LONG = GOOD.replace("range(brief.frames)", "range(brief.frames * 2)")
STILL = GOOD.replace("t = n / max(1, brief.frames - 1)", "t = 1.0")


def scripted_project(name):
    slug, project = a_deck_project(name, slides=2)
    plan_from_slides(slug)
    sections = operations.read_artifact(slug, "plan")["sections"]
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id=s["id"], scenes=[ScriptScene(
            narration="The brain builds a picture of the body from touch and movement.",
            brief="Touch. Movement. One picture of the body.")])
        for s in sections]))
    operations.plan_visuals(slug)
    visual = VisualPlanStore(project.root).load().visuals[1]
    return slug, project, visual


def with_program(slug, project, visual, code, renderer="pillow"):
    save_scene_code(slug, visual.id, code)
    save_spec(scene_folder(project, visual, create=True),
              {"renderer": renderer, "approach": "test", "beats": []})


def checks_of(result):
    return {c["key"]: c["status"] for c in result["checks"]}


def test_every_scene_is_planned_with_no_clip_until_its_program_is_made(project_root):
    slug, project, _ = scripted_project("Programs")
    scenes = VisualPlanStore(project.root).load().visuals
    assert scenes and not any(v.clip_path or v.approved_at for v in scenes)


def test_a_program_that_passes_every_check_has_a_preview_and_waits_for_approval(project_root):
    slug, project, visual = scripted_project("Good scene")
    with_program(slug, project, visual, GOOD)

    result = run_scene(slug, visual.id)

    failing = {k: v for k, v in checks_of(result).items() if v == "fail"}
    assert not failing, result["checks"]
    assert checks_of(result)["layout"] == "warn", "Pillow does not record its text"
    made = result["visual"]
    assert made["clip_path"].endswith("/render.mp4")
    assert result["has_preview"], "the clip with its own narration"
    assert made["approved_at"] == "", "passing is not approving"
    brief = result["brief"]
    assert brief["narration_measured"] and brief["seconds"] > 0
    assert brief["time_range"]["start"] == 0 and brief["section_scenes"][0]["this_scene"]
    folder = scene_folder(project, visual)
    assert {p.name for p in folder.iterdir()} >= {
        "scene.py", "brief.json", "spec.json", "render.mp4", "preview.mp4", "poster.png",
        "checks.json", "log.txt", "narration.json"}


@pytest.mark.parametrize(("code", "failed"), [
    (CRASHES, "ran"), (BLANK, "not-blank"), (TOO_LONG, "duration"), (STILL, "moments")])
def test_a_program_that_fails_a_check_is_not_used(project_root, code, failed):
    slug, project, visual = scripted_project(f"Bad {failed}")
    with_program(slug, project, visual, code)

    result = run_scene(slug, visual.id)

    if failed == "ran":
        assert checks_of(result)["ran"] == "fail"
        assert "the scene went wrong" in result["log"]
    else:
        assert checks_of(result)[failed] == "fail", result["checks"]
    assert result["visual"]["clip_path"] == ""
    assert "failed a check" in result["visual"]["note"]


def test_a_program_that_does_not_use_the_renderer_it_names_fails(project_root):
    slug, project, visual = scripted_project("Not Manim")
    with_program(slug, project, visual, GOOD, renderer="manim")      # GOOD draws with Pillow
    assert checks_of(run_scene(slug, visual.id))["renderer"] == "fail"


def test_approval_needs_a_passing_program_and_a_new_run_withdraws_it(project_root):
    slug, project, visual = scripted_project("Approve")
    with pytest.raises(operations.OperationFailed, match="passed every check"):
        approve_scene(slug, visual.id)

    with_program(slug, project, visual, GOOD)
    run_scene(slug, visual.id)
    assert approve_scene(slug, visual.id)["visual"]["approved_at"]

    again = run_scene(slug, visual.id)
    assert again["visual"]["approved_at"] == "", "watched and approved again"


def test_every_passed_scene_can_be_approved_at_once(project_root):
    slug, project, visual = scripted_project("Approve all")
    assert approve_passed(slug)["approved"] == 0, "nothing passed, nothing approved"

    with_program(slug, project, visual, GOOD)
    run_scene(slug, visual.id)
    done = approve_passed(slug)
    assert done["approved"] == 1
    assert read_scene(slug, visual.id)["visual"]["approved_at"]
    assert approve_passed(slug)["approved"] == 0, "an approved scene is not approved twice"


def test_a_scene_program_never_sees_the_server_s_secrets(project_root, monkeypatch):
    monkeypatch.setenv("SCENE_TEST_SECRET", "not for scene programs")
    slug, project, visual = scripted_project("Sealed")
    with_program(slug, project, visual,
                 "import os\nassert 'SCENE_TEST_SECRET' not in os.environ\n" + GOOD)
    assert checks_of(run_scene(slug, visual.id))["ran"] == "pass"


def test_the_render_refuses_scenes_that_are_not_approved_programs(project_root):
    from pipeline.scene_approval import render_blockers

    slug, project, visual = scripted_project("Blocked")
    blockers = render_blockers(VisualPlanStore(project.root).load().visuals)
    assert len(blockers) == 2 and all("no program that passed" in b for b in blockers)


def test_the_library_lists_what_is_in_it_and_takes_more(project_root, monkeypatch, tmp_path):
    shutil.copytree(resources_root(), tmp_path / "resources")
    monkeypatch.setattr("pipeline.scene_lab.REPO_ROOT", tmp_path)

    index = resource_index()
    names = [entry["name"] for entry in index["code"]]
    assert "scenekit.py" in names and "manimkit.py" in names
    assert "scene-contract.md" in [entry["name"] for entry in index["methods"]]

    added = add_resource("methods", "house-style.md", b"# Our house style\nUse the accent.")
    assert {"name": "house-style.md", "about": "Our house style"} in added["methods"]
    with pytest.raises(operations.OperationFailed):
        add_resource("code", "notes.exe", b"")


def test_read_scene_of_a_scene_with_no_folder_is_empty_not_an_error(project_root):
    slug, _, visual = scripted_project("Empty")
    scene = read_scene(slug, visual.id)
    assert scene["code"] == "" and scene["checks"] == [] and scene["folder"] == ""


def test_a_program_s_clip_is_frozen_with_the_transfer(project_root):
    from pipeline.generation_handoff import _freeze

    slug, project, visual = scripted_project("Frozen")
    with_program(slug, project, visual, GOOD)
    made = run_scene(slug, visual.id)["visual"]

    frozen = _freeze(project, made["clip_path"])
    assert frozen.startswith("generation/transferred/") and frozen.endswith(".mp4")
    assert (project.root / frozen).read_bytes() == (project.root / made["clip_path"]).read_bytes()
