"""Where things are on screen: the shapes manimkit records for the checks, the
diagrams it lays out, what a failing layout is told, and files a full disk leaves.

The Manim test renders a real scene: the kit's geometry runs inside the scene's
own environment, so only a render can show what it records.
"""

import json
import shutil

import pytest

from pipeline.scene_lab import run_scene, scene_folder
from pipeline.scene_review import Verdict
from pipeline.scene_round import render_round
from pipeline.storage.documents import TEMPORARY_WRITE_SUFFIX, write_text_atomically
from tests.test_scene_lab import scripted_project, with_program
from tests.test_slide_first import project_root  # noqa: F401

LAID_OUT = '''# /// script
# requires-python = ">=3.11"
# dependencies = ["manim>=0.19", "pillow"]
# ///
from manimkit import *


class TheScene(ExplainerScene):
    def construct(self):
        end = self.brief.seconds
        title = self.label("The body", size=56, at=(0, 3.2))
        self.play(FadeIn(title), run_time=0.2)
        steps = self.flow(["Touch", "Movement", "Picture"])
        self.play(*[FadeIn(part) for part in steps], run_time=0.2)
        self.until(end * 0.2)
        self.play(FadeOut(steps), run_time=0.2)
        hub = self.hub("The body", ["Touch", "Movement", "Picture", "Brain"])
        self.play(*[FadeIn(part) for part in hub], run_time=0.2)
        self.until(end * 0.4)
        self.play(FadeOut(hub), run_time=0.2)
        line = self.timeline(["Touch", "Movement", "Picture", "Brain", "Body"])
        self.play(*[FadeIn(part) for part in line], run_time=0.2)
        self.until(end * 0.6)
        self.play(FadeOut(line), run_time=0.2)
        # A filled shape with no outline behind words is a panel, not a crossing.
        panel = Ellipse(width=4, height=1.6, fill_color=self.look["accent"], fill_opacity=0.3,
                        stroke_width=0).move_to([-3.5, 0, 0])
        words = self.label("Touch", size=40, at=(-3.5, 0))
        self.play(FadeIn(panel), FadeIn(words), run_time=0.2)
        # What went wrong in real scenes: a circle drawn through its own label, and
        # a box laid half over another.
        ring = Circle(radius=0.35, color=self.look["accent"]).move_to(words)
        first = Rectangle(width=3, height=1.5).move_to([2.5, 0.3, 0])
        second = Rectangle(width=3, height=1.5).move_to([4.0, -0.3, 0])
        self.play(Create(ring), Create(first), Create(second), run_time=0.2)
        self.until(end * 0.8)
        self.finish()


run(TheScene)
'''


@pytest.mark.skipif(not (shutil.which("uv") and shutil.which("ffmpeg")),
                    reason="needs uv and ffmpeg to render a Manim scene")
@pytest.mark.usefixtures("project_root")
def test_manimkit_lays_out_diagrams_cleanly_and_records_what_collides():
    slug, project, visual = scripted_project("Laid out")
    with_program(slug, project, visual, LAID_OUT, renderer="manim")

    result = run_scene(slug, visual.id)

    folder = scene_folder(project, visual)
    assert (folder / "layout.json").exists(), (folder / "log.txt").read_text(encoding="utf-8")
    beats = json.loads((folder / "layout.json").read_text(encoding="utf-8"))["snapshots"]
    flow, hub, timeline, broken = beats[0], beats[1], beats[2], beats[-1]
    for laid_out in (flow, hub, timeline):
        assert not laid_out["crossings"] and not laid_out["collisions"], laid_out
    height = result["brief"]["height"]
    assert (hub["extent"][3] - hub["extent"][1]) / height >= 0.4, "it fills the frame"
    assert [c["shape"] for c in broken["crossings"]] == ["Circle"], \
        "the circle crosses its words; the panel with no outline does not"
    assert [(c["a"].split()[0], c["b"].split()[0]) for c in broken["collisions"]] == [
        ("Rectangle", "Rectangle")]
    checks = {c["key"]: c["status"] for c in result["checks"]}
    assert checks["crossing"] == checks["collide"] == "fail"


def test_a_failing_layout_is_looked_at_and_what_is_seen_is_passed_on(tmp_path, monkeypatch):
    """The model that writes the program reads only text. From a check's
    coordinates alone it re-placed the same boxes the same wrong way for rounds."""
    (tmp_path / "frames").mkdir()
    crossing = {"key": "crossing", "name": "No shape runs through words", "status": "fail",
                "rule": "...", "detail": "a Circle through “The brain” at 17.2 s"}
    monkeypatch.setattr("pipeline.scene_lab.run_scene",
                        lambda slug, visual_id: {"checks": [crossing], "log": "", "brief": {}})
    asked = []

    def review(folder, brief, question=""):
        asked.append(question)
        return Verdict(teaches=True, motion_explains=True, looks_finished=False,
                       problems=["The ring is drawn over the label: put the label below it."])

    monkeypatch.setattr("pipeline.scene_review.review_frames", review)
    state = {"renders": 0, "calls": {"agent": 0, "vision": 0}}

    outcome = render_round("s", "v", tmp_path, "manim", {}, state)

    assert not outcome["passed"] and "Circle through" in asked[0]
    assert "What a reviewer sees in the frames:" in outcome["feedback"]
    assert "put the label below it" in outcome["feedback"]
    assert state["calls"]["vision"] == 1


def test_a_crash_is_not_sent_for_a_look(tmp_path, monkeypatch):
    (tmp_path / "frames").mkdir()
    ran = {"key": "ran", "name": "The program ran", "status": "fail", "rule": "...",
           "detail": "It stopped with an error."}
    monkeypatch.setattr("pipeline.scene_lab.run_scene",
                        lambda slug, visual_id: {"checks": [ran], "log": "Traceback", "brief": {}})
    monkeypatch.setattr("pipeline.scene_review.review_frames",
                        lambda *a, **k: pytest.fail("a crash has nothing to look at"))
    state = {"renders": 0, "calls": {"agent": 0, "vision": 0}}

    outcome = render_round("s", "v", tmp_path, "manim", {}, state)

    assert "Traceback" in outcome["feedback"] and state["calls"]["vision"] == 0


def test_a_write_that_fails_part_way_leaves_no_half_file(tmp_path, monkeypatch):
    """A full disk left a 0-byte visuals.json.tmp beside the real visuals.json."""
    target = tmp_path / "visuals.json"
    target.write_text("{}", encoding="utf-8")

    def full(self, *args, **kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr("pathlib.Path.replace", full)
    with pytest.raises(OSError):
        write_text_atomically(target, '{"visuals": []}')

    assert target.read_text(encoding="utf-8") == "{}", "the real file is untouched"
    assert not (tmp_path / ("visuals.json" + TEMPORARY_WRITE_SUFFIX)).exists()
