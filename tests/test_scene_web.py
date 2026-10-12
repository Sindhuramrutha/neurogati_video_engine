"""A web page as a scene: recorded frame by frame, its text measured from the
page, its motion read from its timelines -- and nothing outside it reachable."""

# ruff: noqa: F811
import json
import shutil
from pathlib import Path

import pytest

from pipeline.generation import VisualPlanStore
from pipeline.scene_lab import run_scene, scene_folder
from pipeline.scene_program import save_spec
from pipeline.scene_web import _answer, is_installed
from tests.test_scene_lab import checks_of, project_root, scripted_project  # noqa: F401

PAGE = """<!doctype html><html><head><meta charset="utf-8"></head><body>
<script src="/lib/gsap.js"></script>
<script src="/kit/webkit.js"></script>
<script>
Kit.load().then(kit => {
  const tl = gsap.timeline();
  const a = kit.label("Touch", { x: 600, y: 400, size: 64 });
  const b = kit.label("Movement", { x: 1300, y: 400, size: 64 });
  const svg = kit.svg();
  const bar = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  bar.setAttribute("x", 300); bar.setAttribute("y", 760); bar.setAttribute("height", 120);
  bar.setAttribute("width", 10); bar.setAttribute("fill", kit.look.accent);
  svg.appendChild(bar);
  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line.setAttribute("x1", 760); line.setAttribute("y1", 400); line.setAttribute("x2", 1080);
  line.setAttribute("y2", 400); line.setAttribute("stroke", kit.look.accent);
  line.setAttribute("stroke-width", 6);
  svg.appendChild(line);
  tl.from(a, { x: -300, duration: 1 }, 0);
  tl.to(bar, { attr: { width: 1300 }, duration: kit.seconds * 0.8 }, 0.5);
  tl.from(b, { y: 200, opacity: 0, duration: 1 }, kit.seconds * 0.4);
  tl.to(a, { scale: 1.3, duration: 1 }, kit.seconds * 0.6);
  kit.timeline(tl);
  kit.ready();
});
</script></body></html>"""


def test_a_page_may_reach_only_its_own_files_the_libraries_and_its_pictures(tmp_path):
    folder = tmp_path / "scene"
    folder.mkdir()
    (folder / "scene.html").write_text("x", encoding="utf-8")
    (tmp_path / "secret.txt").write_text("no", encoding="utf-8")
    brief = {"assets": {"pictures": [str(tmp_path / "offered.png")]}, "slide_image": ""}

    assert _answer(folder, brief, "http://scene.local/scene.html") == folder / "scene.html"
    assert _answer(folder, brief, "http://scene.local/../secret.txt") is None
    assert _answer(folder, brief, "http://scene.local/%2e%2e/secret.txt") is None
    assert _answer(folder, brief, "https://cdn.example.com/gsap.js") is None, "no internet"
    assert _answer(folder, brief, "http://scene.local/kit/webkit.js").name == "webkit.js"
    offered = "http://scene.local/picture?path=" + str(tmp_path / "offered.png")
    assert _answer(folder, brief, offered) == tmp_path / "offered.png"
    other = "http://scene.local/picture?path=" + str(tmp_path / "secret.txt")
    assert _answer(folder, brief, other) is None, "only the pictures the brief offers"


@pytest.mark.skipif(not (is_installed() and shutil.which("ffmpeg")),
                    reason="needs renderers/web/node_modules, Chromium and ffmpeg")
def test_a_web_scene_is_recorded_measured_and_checked(project_root):
    slug, project, visual = scripted_project("Web scene")
    folder = scene_folder(project, visual, create=True)
    (folder / "scene.html").write_text(PAGE, encoding="utf-8")
    save_spec(folder, {"renderer": "web", "entry": "scene.html"})

    result = run_scene(slug, visual.id)

    found = checks_of(result)
    assert found["ran"] == found["renderer"] == found["duration"] == "pass", result["checks"]
    assert found["bounds"] == found["overlap"] == "pass"
    assert found["collide"] == found["fills"] == "pass", "the page's shapes are measured"
    assert found["motion"] == "pass", "moves, grows and scales: it explains by motion"
    layout = json.loads(Path(folder / "layout.json").read_text(encoding="utf-8"))
    said = {t["text"] for s in layout["snapshots"] for t in s["texts"]}
    assert {"Touch", "Movement"} <= said, "the page's text is measured"
    failing = [c["key"] for c in result["checks"] if c["status"] == "fail"]
    assert result["visual"]["clip_path"].endswith("render.mp4"), failing
    assert VisualPlanStore(project.root).load().visuals[1].drawn_by == "scene.html"
