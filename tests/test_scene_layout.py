"""Where things are on screen: the shapes manimkit records for the checks, the
diagrams it lays out, what a failing layout is told, and files a full disk leaves.

The Manim test renders a real scene: the kit's geometry runs inside the scene's
own environment, so only a render can show what it records.
"""

import json
import shutil

import pytest

from pipeline.scene_lab import run_scene, scene_folder
from pipeline.scene_review import Scores, Verdict
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
        title = self.title("The body")
        self.play(self.reveal(title, run_time=0.2))
        steps = self.flow(["Touch", "Movement", "Picture"])
        self.play(*[self.reveal(box, run_time=0.2) for box in steps.boxes])
        self.play(*[self.grow(arrow, run_time=0.2) for arrow in steps.arrows])
        self.play(self.focus(steps.boxes[1], steps.boxes[0], steps.boxes[2], run_time=0.2))
        self.until(end * 0.2)
        self.play(FadeOut(steps), run_time=0.2)
        hub = self.hub("The body", ["Touch", "Movement", "Picture", "Brain"])
        self.play(*[FadeIn(part) for part in hub], run_time=0.2)
        self.until(end * 0.4)
        self.play(FadeOut(hub), run_time=0.2)
        line = self.timeline(["Touch", "Movement", "Picture", "Brain", "Body"])
        self.play(*[FadeIn(part) for part in line], run_time=0.2)
        self.until(end * 0.5)
        self.play(FadeOut(line), run_time=0.2)
        # A label beside the point it names, and -- between two beats -- an arrow
        # drawn through a label and taken away again before the next beat.
        note = self.callout("Nerve", (-2.0, -1.0), side="left")
        self.play(*[FadeIn(part) for part in note], run_time=0.2)
        passing = self.label("Signal", size=40, at=(3.0, -2.5))
        self.play(FadeIn(passing), run_time=0.2)
        stray = Arrow([1.5, -2.5, 0], [4.5, -2.5, 0], buff=0)
        self.play(GrowArrow(stray), run_time=0.2)
        self.play(FadeOut(stray), FadeOut(passing), run_time=0.2)
        self.until(end * 0.6)
        self.play(FadeOut(note), run_time=0.2)
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
    snapshots = json.loads((folder / "layout.json").read_text(encoding="utf-8"))["snapshots"]
    beats = [s for s in snapshots if s["beat"]]
    flow, hub, timeline, callout, broken = beats[0], beats[1], beats[2], beats[3], beats[-1]
    for laid_out in (flow, hub, timeline, callout):
        assert not laid_out["crossings"] and not laid_out["collisions"], laid_out
    assert any(c["text"] == "Signal" for s in snapshots if not s["beat"]
               for c in s["crossings"]), "the arrow between beats was seen"
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
                        lambda slug, visual_id, brief=None:
                        {"checks": [crossing], "log": "", "brief": {}})
    asked = []

    def review(folder, brief, question=""):
        asked.append(question)
        scores = dict.fromkeys(Scores.model_fields, 3) | {"labels": 1, "composition": 2}
        return Verdict(scores=Scores(**scores), teaches=True, motion_explains=True,
                       looks_finished=False,
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
                        lambda slug, visual_id, brief=None:
                        {"checks": [ran], "log": "Traceback", "brief": {}})
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


# --- what a scene is offered to show ----------------------------------------------------


def test_a_scene_paints_its_illustration_once_and_only_when_asked(tmp_path, monkeypatch):
    """Drawn from code, a frog's leg was two ellipses. The script asks for a picture
    when no slide shows the thing; it is painted once, and every later round and a
    scene made again use the same one."""
    import io

    from PIL import Image

    from pipeline import scene_illustration
    from pipeline.llm import ModelCallFailed

    def picture(colour):
        buffer = io.BytesIO()
        Image.new("RGB", (64, 64), colour).save(buffer, format="PNG")
        return buffer.getvalue()

    painted, verdicts = [], [scene_illustration.Checked(
        matches=False, framed=True, clean=True,
        wrong="human hearts; they must be small frog hearts"),
        scene_illustration.Checked(matches=True, framed=True, clean=True)]
    monkeypatch.setattr("pipeline.llm.draw_image",
                        lambda prompt: painted.append(prompt) or picture("#fbfbfa"))
    monkeypatch.setattr(scene_illustration, "check", lambda path, asked, said: verdicts.pop(0))
    look = {"background": "#ffffff", "accents": ["#4472c4", "#ed7d31"]}
    brief = ("PICTURE: none\nDRAW: a frog's leg\nILLUSTRATE: a frog's leg on a bench, two "
             "wires touching its nerve\nLABELS: Galvani")
    state = {"calls": {"agent": 0, "vision": 0}, "events": []}
    scene = tmp_path / "scenes" / "001"
    scene.mkdir(parents=True)

    first = scene_illustration.paint(scene, brief, look, state)
    again = scene_illustration.paint(scene, brief, look, state)

    assert first == again == scene_illustration.kept(scene, brief, look)
    reference = scene.parent / scene_illustration.STYLE_REFERENCE
    assert reference.read_bytes() == first.read_bytes(), "the first painting is the style"
    assert len(painted) == 2 and state["calls"]["image"] == 2, "wrong once, painted again"
    assert "no text" in painted[0].lower() and "#ffffff" in painted[0]
    assert "small frog hearts" in painted[1], "the second asks for the correction"
    assert Image.open(first).getpixel((0, 0)) == (255, 255, 255), "no panel edge"
    assert scene_illustration.paint(scene, "PICTURE: none\nDRAW: a box", look, state) is None
    assert scene_illustration.wanted("ILLUSTRATE: none") == ""

    styled = []
    monkeypatch.setattr(scene_illustration, "_paint_like",
                        lambda request, style: styled.append(style) or picture("#fafafa"))
    verdicts.append(scene_illustration.Checked(matches=True, framed=True, clean=True))
    other = brief.replace("frog's leg on a bench", "voltaic pile")
    assert scene_illustration.paint(scene, other, look, state) is not None
    assert styled == [reference.read_bytes()], "later pictures are painted from the style"

    def down(request, style):
        raise ModelCallFailed("no image model")

    monkeypatch.setattr(scene_illustration, "_paint_like", down)
    third = brief.replace("frog's leg on a bench", "two frog hearts in beakers")
    assert scene_illustration.paint(scene, third, look, state) is None, "made without it"


TEMPLATED = '''# /// script
# requires-python = ">=3.11"
# dependencies = ["manim>=0.19", "pillow"]
# ///
from manimkit import *


class TheScene(ExplainerScene):
    def construct(self):
        end = self.brief.seconds
        self.hero("picture.png", title="The body", callouts=[
            ("Touch", (0.3, 0.3), None, (0.2, 0.2, 0.4, 0.4)),
            ("Movement", (0.7, 0.5), None, (0.6, 0.4, 0.8, 0.6)),
            ("Reach", (0.8, 0.2), None)],
            moves=[([(0.1, 0.5), (0.5, 0.4), (0.9, 0.5)], None)])
        self.until(end * 0.2)
        self.clear()
        self.steps([("Touch", None, None), ("Movement", "picture.png", None),
                    ("Picture", None, None)], title="The body")
        self.until(end * 0.4)
        self.clear()
        self.compare(("Touch", None, ["The body"], None),
                     ("Movement", "picture.png", ["The brain"], None), title="The body")
        self.until(end * 0.6)
        self.clear()
        self.person("picture.png", "The brain", "A picture of the body from touch.")
        self.until(end * 0.75)
        self.clear()
        self.key_idea("The brain builds a picture of the body.", "picture.png")
        self.until(end * 0.85)
        self.clear()
        self.opener("picture.png", "The body", [("Touch", None), ("Movement", None)])
        self.finish()


run(TheScene)
'''


@pytest.mark.skipif(not (shutil.which("uv") and shutil.which("ffmpeg")),
                    reason="needs uv and ffmpeg to render a Manim scene")
@pytest.mark.usefixtures("project_root")
def test_every_shot_template_passes_the_layout_checks_by_construction():
    """The templates are what the scene model fills instead of placing boxes by
    hand: each must come out clean with nothing but its slots filled."""
    from PIL import Image

    slug, project, visual = scripted_project("Templates")
    with_program(slug, project, visual, TEMPLATED, renderer="manim")
    folder = scene_folder(project, visual)
    # A drawing in a wide white margin, as a painted illustration comes: the kit
    # trims the margin, so the picture is shown at the size of what it shows.
    picture = Image.new("RGB", (800, 600), (255, 255, 255))
    picture.paste((90, 140, 200), (200, 150, 600, 450))
    picture.save(folder / "picture.png")

    result = run_scene(slug, visual.id)

    checks = {c["key"]: c for c in result["checks"]}
    for key in ("ran", "bounds", "overlap", "contrast", "legible", "crossing", "collide",
                "fills", "paragraphs"):
        assert checks[key]["status"] == "pass", (key, checks[key]["detail"])
