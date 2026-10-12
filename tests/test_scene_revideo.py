"""A Revideo / Motion Canvas scene an agent wrote: compiled where its packages
resolve, given the kit, rendered at the brief's length -- in seconds, not at its
whole time limit -- and checked."""

# ruff: noqa: F811
import shutil

import pytest

from pipeline.scene_lab import run_scene, scene_folder
from pipeline.scene_program import save_spec
from pipeline.scene_revideo import RENDERER, UNNAMED_SCENE, is_installed
from tests.test_scene_lab import checks_of, project_root, scripted_project  # noqa: F401

# Written the Motion Canvas way (no scene name): the adapter names it.
SCENE = """import {Circle, Line, Txt, makeScene2D} from '@revideo/2d';
import {all, createRef} from '@revideo/core';
import {finish, look, prepare, seconds, until} from './kit';

export default makeScene2D(function* (view) {
  prepare(view);
  const word = createRef<Txt>();
  const dot = createRef<Circle>();
  const line = createRef<Line>();
  view.add(<Txt ref={word} text="Touch" fill={look.text} fontSize={72} y={-200} />);
  view.add(<Line ref={line} points={[[-500, 150], [500, 150]]} stroke={look.accent}
                 lineWidth={10} end={0} />);
  view.add(<Circle ref={dot} size={60} fill={look.accent} x={-500} y={150} />);
  yield* line().end(1, seconds * 0.3);
  yield* all(dot().x(500, seconds * 0.3), word().scale(1.4, seconds * 0.3));
  yield* until(seconds * 0.8);
  yield* word().y(-120, 0.5);
  yield* finish();
});
"""


def test_a_motion_canvas_scene_without_a_name_is_given_one():
    fixed = UNNAMED_SCENE.sub(lambda m: f"makeScene2D('scene', {m.group(1)}",
                              "makeScene2D(function* (view) {})")
    assert fixed == "makeScene2D('scene', function* (view) {})"
    named = "makeScene2D('mine', function* (view) {})"
    assert UNNAMED_SCENE.sub("x", named) == named, "a named scene is left alone"


@pytest.mark.skipif(not (is_installed() and shutil.which("ffmpeg")),
                    reason="needs Node, renderers/revideo/node_modules and ffmpeg")
def test_a_revideo_scene_renders_at_the_narration_s_length(project_root):
    slug, project, visual = scripted_project("Revideo scene")
    folder = scene_folder(project, visual, create=True)
    (folder / "scene.tsx").write_text(SCENE, encoding="utf-8")
    save_spec(folder, {"renderer": "revideo", "entry": "scene.tsx"})

    result = run_scene(slug, visual.id)

    found = checks_of(result)
    assert found["ran"] == found["renderer"] == found["duration"] == "pass", result["log"][-800:]
    assert found["frame"] == "pass"
    assert not list((RENDERER / "agent").glob("*")), "its working folder is cleaned up"
