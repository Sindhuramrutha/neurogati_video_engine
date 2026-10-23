"""One video, start to end: a 2-slide deck from upload to export.

The first render of Demo 001 failed on a path no test had walked (narration
spoken scene by scene, into a folder that did not exist yet). Each layer had its
own tests; nothing ran them in a row. This does: a real deck is extracted,
planned, scripted, made into scenes, approved, rendered with real ffmpeg and
exported. The model and the voice are stand-ins (no network, no cost); the
second scene's model is down, so it is drawn by the real Manim stand-in.

It is in the pre-commit hook (tools/hooks/pre-commit): a commit that breaks the
path from a deck to a video does not go in.
"""
# ruff: noqa: F811

import json
import shutil
import subprocess

import pytest

from pipeline import operations
from pipeline.generation import VisualPlanStore
from pipeline.llm import ModelNotConfigured
from pipeline.scene_approval import approve_scene
from pipeline.scene_lab import scene_folder
from pipeline.scene_maker import make_scene
from pipeline.scene_state import load_state
from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript
from tests.test_scene_agent import GOOD_VERDICT, Model, whole, wired
from tests.test_scene_lab import GOOD
from tests.test_slide_first import a_deck_project, plan_from_slides, project_root  # noqa: F401

pytestmark = [
    pytest.mark.smoke,
    pytest.mark.skipif(not (shutil.which("ffmpeg") and shutil.which("ffprobe")
                            and shutil.which("uv")), reason="needs ffmpeg and uv"),
]

NARRATION = ("The brain builds a picture of the body from touch and movement.",
             "Signals from the skin reach the cortex in an orderly map.")


def seconds_of(video) -> float:
    found = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(video)], capture_output=True, text=True)
    return float(found.stdout.strip() or 0)


def test_a_deck_becomes_a_video_and_its_hand_over(project_root, monkeypatch):
    # Inputs and Extraction: a real .pptx, parsed.
    slug, project = a_deck_project("Smoke", slides=2)
    assert operations.read_artifact(slug, "extraction")["documents"]

    # Scene Plan and Script: one section per slide, one scene each.
    sections = plan_from_slides(slug)["sections"]
    assert len(sections) == 2
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id=section["id"], scenes=[ScriptScene(
            narration=words, brief="Touch. Movement. One picture of the body.")])
        for section, words in zip(sections, NARRATION, strict=True)]))
    operations.plan_visuals(slug)
    visuals = VisualPlanStore(project.root).load().visuals
    assert len(visuals) == 2

    # Generation: the first scene is written by the model; for the second the
    # model cannot be reached, and the plain stand-in is drawn (real Manim).
    wired(monkeypatch, Model(whole(GOOD), *[ModelNotConfigured("no key")] * 20),
          GOOD_VERDICT)
    for visual in visuals:
        make_scene(slug, visual.id)
    for visual in VisualPlanStore(project.root).load().visuals:
        state = load_state(scene_folder(project, visual))
        assert visual.clip_path, f"scene {visual.scene_number} has no clip: {state['events']}"
        approve_scene(slug, visual.id)
    events = [e["text"] for e in load_state(scene_folder(project, visuals[1]))["events"]]
    assert any("plain stand-in" in text for text in events)

    # Studio and Reviewing: rendered with the silent voice and real ffmpeg.
    rendered = operations.render_video(slug, "silent")
    video = project.root / "reviewing" / "output" / rendered["video_file_name"]
    assert video.exists() and seconds_of(video) > 1.0

    # Export: the stand-in scene fails its own checks, so the hand-over is not ready;
    # built as a draft on purpose, it is complete and says it is a draft.
    blocked = operations.build_export(slug)
    assert any("still fail their own checks" in b for b in blocked["blockers"])
    exported = operations.build_export(slug, draft=True)
    manifest = json.loads((project.root / "export" / "manifest.json").read_text("utf-8"))
    assert not manifest.get("blockers"), manifest.get("blockers")
    assert manifest["draft"]
    transcript = (project.root / "export" / "transcript.md").read_text(encoding="utf-8")
    for words in NARRATION:
        assert words in transcript
    assert exported
