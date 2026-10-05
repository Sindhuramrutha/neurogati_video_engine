"""A scene as a folder with a script: the script is free, the checks are fixed,
and a clip that fails one is not used."""

# ruff: noqa: F811
import shutil

import pytest

from pipeline import operations, scene_author
from pipeline.generation import VisualPlanStore
from pipeline.scene_author import add_resource, mark_scripted, resource_index, script_scene
from pipeline.scene_lab import (
    SCRIPTED,
    read_scene,
    resources_root,
    run_scene,
    save_scene_code,
    scene_folder,
)
from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript
from pipeline.slide_plan import plan_from_slides
from tests.test_slide_first import a_deck_project, project_root  # noqa: F401

pytestmark = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")), reason="needs ffmpeg")

# The library's own worked example, without its dependency block, so the test
# runs it with this interpreter instead of asking uv to build an environment.
EXAMPLE = (resources_root() / "methods" / "example_scene.py").read_text(
    encoding="utf-8").split("# ///\n", 1)[1]

CRASHES = "raise RuntimeError('the scene went wrong')\n"
BLANK = '''
from scenekit import VideoWriter, canvas, load_brief
brief = load_brief()
with VideoWriter(brief) as video:
    for _ in range(brief.frames):
        video.write(canvas(brief)[0])
'''
TOO_LONG = EXAMPLE.replace("range(brief.frames)", "range(brief.frames * 2)")


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


def checks_of(result):
    return {c["key"]: c["status"] for c in result["checks"]}


def test_a_scene_that_passes_its_checks_becomes_what_the_scene_shows(project_root):
    slug, project, visual = scripted_project("Good scene")
    save_scene_code(slug, visual.id, EXAMPLE)

    result = run_scene(slug, visual.id)

    assert set(checks_of(result).values()) == {"pass"}, result["checks"]
    made = result["visual"]
    assert made["kind"] == SCRIPTED and made["is_built"]
    assert made["clip_path"].endswith("/render.mp4")
    assert made["asset_path"].endswith("/poster.png")
    folder = scene_folder(project, visual)
    assert {p.name for p in folder.iterdir()} >= {
        "scene.py", "brief.json", "render.mp4", "poster.png", "checks.json", "log.txt"}
    assert result["brief"]["seconds"] == 4.8, "measured from the narration: 12 words"
    assert result["brief"]["slide_image"].endswith("slide.png"), "the deck's slide is kept"


@pytest.mark.parametrize(("code", "failed"), [
    (CRASHES, "ran"), (BLANK, "shows"), (TOO_LONG, "length")])
def test_a_scene_that_fails_a_check_is_not_used(project_root, code, failed):
    slug, project, visual = scripted_project(f"Bad {failed}")
    save_scene_code(slug, visual.id, code)

    result = run_scene(slug, visual.id)

    assert checks_of(result)[failed] == "fail"
    assert result["visual"]["clip_path"] == "" and not result["visual"]["is_built"]
    assert "failed a check" in result["visual"]["note"]
    if failed == "ran":
        assert "the scene went wrong" in result["log"]


class FakeAuthor:
    """Writes a script that crashes, then -- shown the failure -- one that works."""

    def __init__(self):
        self.requests = []

    def __call__(self, model, system_prompt, user_prompt, **_):
        self.requests.append((system_prompt, user_prompt))
        code = CRASHES if len(self.requests) == 1 else EXAMPLE
        return model(approach="A headline and three points.", code=code)


def test_the_agent_writes_runs_and_fixes_until_the_checks_pass(project_root, monkeypatch):
    slug, project, visual = scripted_project("Authored")
    author = FakeAuthor()
    monkeypatch.setattr(scene_author, "complete_structured", author)
    monkeypatch.setattr("pipeline.agent_runtime.build_system_prompt", lambda agent: "AGENT")

    result = script_scene(slug, visual.id)

    assert [a["failed"] for a in result["attempts"]] == [
        ["The script ran", "It made a video"], []]
    assert result["visual"]["is_built"]
    system, first = author.requests[0]
    assert "scene-contract.md" in system and "scenekit.py" in system, "shown the library"
    assert '"on_screen": "Touch. Movement. One picture of the body."' in first
    assert "the scene went wrong" in author.requests[1][1], "the fix is shown the failure"
    assert (scene_folder(project, visual) / "author.json").exists()


def test_deciding_again_keeps_a_scripted_scene_scripted(project_root):
    slug, project, visual = scripted_project("Kept")
    assert mark_scripted(slug, [visual.id]) == 1

    script = ScriptStore(project.root).load()
    script.section_scripts[1].scenes[0].narration = "Rewritten: the body map is learnt."
    ScriptStore(project.root).save(script)
    operations.plan_visuals(slug)

    again = next(v for v in VisualPlanStore(project.root).load().visuals
                 if v.scene_id == visual.scene_id)
    assert again.kind == SCRIPTED and not again.is_built
    assert "run its script again" in again.note


def test_the_library_lists_what_is_in_it_and_takes_more(project_root, monkeypatch, tmp_path):
    shutil.copytree(resources_root(), tmp_path / "resources")
    monkeypatch.setattr("pipeline.scene_lab.REPO_ROOT", tmp_path)

    index = resource_index()
    assert {"name": "scenekit.py",
            "about": "scenekit -- the small toolkit every scene script can import."} \
        in index["code"]
    assert "scene-contract.md" in [entry["name"] for entry in index["methods"]]

    added = add_resource("methods", "house-style.md", b"# Our house style\nUse the accent.")
    assert {"name": "house-style.md", "about": "Our house style"} in added["methods"]
    with pytest.raises(operations.OperationFailed):
        add_resource("code", "notes.exe", b"")


def test_read_scene_of_a_scene_with_no_folder_is_empty_not_an_error(project_root):
    slug, _, visual = scripted_project("Empty")
    scene = read_scene(slug, visual.id)
    assert scene["code"] == "" and scene["checks"] == [] and scene["folder"] == ""


def test_a_scripted_clip_is_frozen_with_the_transfer_and_reaches_the_render(project_root):
    from pipeline.generation_handoff import _freeze

    slug, project, visual = scripted_project("Frozen")
    save_scene_code(slug, visual.id, EXAMPLE)
    made = run_scene(slug, visual.id)["visual"]

    frozen = _freeze(project, made["clip_path"])
    assert frozen.startswith("generation/transferred/") and frozen.endswith(".mp4")
    assert (project.root / frozen).read_bytes() == (project.root / made["clip_path"]).read_bytes()

    # Running the script again rewrites render.mp4; the frozen copy does not move.
    save_scene_code(slug, visual.id, EXAMPLE.replace("88", "96"))
    run_scene(slug, visual.id)
    assert (project.root / frozen).exists()
    assert _freeze(project, made["clip_path"]) != frozen, "a different clip, a different name"
