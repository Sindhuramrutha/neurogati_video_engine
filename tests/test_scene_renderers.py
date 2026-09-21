"""What can draw a scene, what each kind needs, and what the viewer reads.

The registry's job is to be *honest*: installed is not working, and "can
animate" is not "can animate this". Every test here is about refusing to claim
more than has been proved, because the failure mode it replaced was silent --
a scene composed as a formula on a machine with no way to typeset one came out
as a still of a formula, and nothing said so.
"""

from __future__ import annotations

import json

import pytest

from pipeline.on_screen import (
    KIND_INSTRUCTIONS,
    MAXIMUM_HEADLINE_LENGTH,
    OnScreenPlan,
    fallback_headline,
    spec_from_plan,
)
from pipeline.scene_renderers import (
    NEEDS,
    RENDERERS,
    SCENE_KINDS,
    Capability,
    DiagramSpec,
    drawable_kinds,
    renderer_for_kind,
)

# --- what a kind cannot be drawn without -------------------------------------------


def test_every_kind_declares_what_it_needs_and_who_draws_it():
    """A kind nobody can draw and a kind nothing validates are both dead ends."""
    assert set(NEEDS) == set(SCENE_KINDS), "each kind needs its own requirements"
    claimed = {kind for renderer in RENDERERS for kind in renderer.kinds}
    assert claimed == set(SCENE_KINDS), \
        "a kind in SCENE_KINDS that no renderer claims can never be drawn"
    assert set(KIND_INSTRUCTIONS) | {"figure"} == set(SCENE_KINDS), \
        "the model needs to be told what to fill for every kind it may choose"


@pytest.mark.parametrize(("kind", "raw", "drawable"), [
    ("flow", {"nodes": ["a", "b"]}, True),
    ("flow", {"nodes": ["a"]}, False),
    ("bars", {"values": [1, 2, 3]}, True),
    ("bars", {"nodes": ["a", "b"]}, False),
    ("counter", {"values": [0, 100]}, True),
    ("counter", {"values": [100]}, False),
    ("plot", {"expression": "sin(x)"}, True),
    ("plot", {"nodes": ["a", "b"]}, False),
    ("formula", {"formula": "y = mx + c"}, True),
    ("formula", {"steps": ["y = mx"]}, False),
    ("figure", {"image": "/tmp/a.png"}, True),
    ("figure", {"nodes": ["a", "b"]}, False),
    ("code", {"code": "print(1)"}, True),
    ("table", {"nodes": ["a|1"]}, True),
    ("nonsense", {"nodes": ["a", "b"]}, False),
])
def test_a_spec_is_drawable_only_with_what_its_kind_needs(kind, raw, drawable):
    """Checked here rather than in a subprocess four seconds later."""
    assert (DiagramSpec.from_dict({"kind": kind, **raw}) is not None) is drawable


def test_a_spec_survives_a_round_trip_through_storage():
    """It is stored on the visual as a dict and read back to be drawn."""
    spec = DiagramSpec(
        kind="graph", caption="the chain", nodes=["a", "b", "c"],
        edges=[[0, 1], [1, 2]], labels=["x"], values=[1.5],
        expression="sin(x)", formula="y=x", steps=["y"], code="print(1)",
    )
    again = DiagramSpec.from_dict(json.loads(json.dumps(spec.to_dict())))

    assert again is not None
    assert again.to_dict() == spec.to_dict()


def test_nonsense_in_a_stored_spec_is_dropped_not_drawn():
    """This comes back off disk, where anything could have been written."""
    spec = DiagramSpec.from_dict({
        "kind": "graph",
        "nodes": ["a", "  ", "b", ""],
        "edges": [[0, 1], ["x", 2], [3], None],
        "values": ["4.5", "not a number", 6],
    })

    assert spec is not None
    assert spec.nodes == ["a", "b"], "blank labels would draw empty boxes"
    assert spec.edges == [[0, 1]], "an edge that is not two numbers is not an edge"
    assert spec.values == [4.5, 6.0]


# --- claimed, available, proved ------------------------------------------------------


def test_a_kind_recorded_as_failing_is_not_offered_again(monkeypatch):
    """The whole point of the per-kind record.

    A backend whose formula scenes fail must keep drawing the eleven kinds that
    work, and must not be handed a formula again -- which is a different answer
    from "animation is broken here".
    """
    manim = next(renderer for renderer in RENDERERS if renderer.key == "manim")
    if not manim.is_installed():
        pytest.skip("manim is not installed here")

    monkeypatch.setattr(
        "pipeline.scene_renderers._self_test_results",
        lambda: {
            "manim": {"ok": True, "kinds": {
                "formula": {"ok": False, "detail": "no latex"},
                "flow": {"ok": True, "detail": ""},
            }},
            # Revideo out of the picture, or it would cover the formula that
            # Manim cannot draw -- which is the right behaviour and a different
            # test.
            "revideo": {"ok": False, "detail": "not usable here", "kinds": {}},
        },
    )

    assert manim.can_draw("flow")
    assert not manim.can_draw("formula")
    assert "formula" not in drawable_kinds()
    assert drawable_kinds().get("flow") == "manim"
    assert renderer_for_kind("formula") is None
    assert renderer_for_kind("flow") is manim


def test_a_renderer_recorded_as_broken_draws_nothing(monkeypatch):
    monkeypatch.setattr(
        "pipeline.scene_renderers._self_test_results",
        lambda: {"manim": {"ok": False, "detail": "crashed", "kinds": {}},
                 "revideo": {"ok": False, "detail": "crashed", "kinds": {}}},
    )

    assert drawable_kinds() == {}
    assert renderer_for_kind("flow") is None


def test_the_stills_renderer_is_always_there_and_never_claims_to_animate():
    """A bare checkout still renders a video; it just does not animate one."""
    stills = next(renderer for renderer in RENDERERS if renderer.key == "stills")

    assert stills.is_installed() and stills.is_available()
    assert stills.can(Capability.STILLS)
    assert not stills.can(Capability.ANIMATED_DIAGRAM)
    assert stills.kinds == ()


def test_a_preferred_renderer_is_only_used_for_kinds_it_can_draw(monkeypatch):
    monkeypatch.setattr(
        "pipeline.scene_renderers._self_test_results",
        lambda: {"manim": {"ok": True, "kinds": {}}, "revideo": {"ok": True, "kinds": {}}},
    )
    manim = next(renderer for renderer in RENDERERS if renderer.key == "manim")
    if not manim.is_installed():
        pytest.skip("manim is not installed here")

    # Only Manim draws a plot, whatever is asked for.
    assert renderer_for_kind("plot", preferred="revideo") is manim


def test_the_cheap_renderer_wins_wherever_both_can_draw_the_kind(monkeypatch):
    """Three seconds a scene against forty. On a twenty-scene video that is the
    difference between a minute and a quarter of an hour, and the output is the
    same picture."""
    monkeypatch.setattr(
        "pipeline.scene_renderers._self_test_results",
        lambda: {"manim": {"ok": True, "kinds": {}}, "revideo": {"ok": True, "kinds": {}}},
    )
    manim = next(renderer for renderer in RENDERERS if renderer.key == "manim")
    revideo = next(renderer for renderer in RENDERERS if renderer.key == "revideo")
    if not (manim.is_installed() and revideo.is_installed()):
        pytest.skip("both backends are needed to choose between them")

    # Both draw a flow; only one of them is cheap.
    assert "flow" in manim.kinds and "flow" in revideo.kinds
    assert renderer_for_kind("flow") is manim


def test_the_slow_renderer_wins_the_one_thing_it_does_better(monkeypatch):
    """Revideo typesets with MathJax in the page. Manim's MathTex needs a TeX
    distribution and reads as plain text without one, so on a machine with no
    LaTeX the slower renderer is the only way to get real mathematics."""
    monkeypatch.setattr(
        "pipeline.scene_renderers._self_test_results",
        lambda: {"manim": {"ok": True, "kinds": {}}, "revideo": {"ok": True, "kinds": {}}},
    )
    manim = next(renderer for renderer in RENDERERS if renderer.key == "manim")
    revideo = next(renderer for renderer in RENDERERS if renderer.key == "revideo")
    if not (manim.is_installed() and revideo.is_installed()):
        pytest.skip("both backends are needed to choose between them")

    monkeypatch.setattr("pipeline.scene_renderers.has_latex", lambda: False)
    assert renderer_for_kind("formula") is revideo

    # With a TeX distribution the exception stops applying and cost decides.
    monkeypatch.setattr("pipeline.scene_renderers.has_latex", lambda: True)
    assert renderer_for_kind("formula") is manim


def test_a_hung_renderer_is_killed_rather_than_waited_for():
    """A video is many scenes, and one that hangs must not take all of them.

    `subprocess.run(timeout=...)` was not enough: these processes start others
    -- vite, Chrome, ffmpeg -- and a surviving grandchild holds the pipe open,
    so the call that was meant to time out blocked instead.
    """
    import sys
    import time

    from pipeline.scene_renderers import run_bounded

    started = time.monotonic()
    ran = run_bounded([sys.executable, "-c", "import time; time.sleep(90)"], 2)
    took = time.monotonic() - started

    assert ran.timed_out
    assert took < 20, f"it should have given up in about 2s, not {took:.0f}s"


# --- composing what is on screen ----------------------------------------------------


def test_a_composed_scene_of_an_unavailable_kind_is_not_drawn():
    """The model is only offered what works, but it can still answer with
    anything, and a kind nothing can draw has to be dropped rather than tried."""
    plan = OnScreenPlan(headline="A loop", scene_kind="cycle",
                        nodes=["sense", "decide", "act"])

    assert spec_from_plan(plan, "A loop", {"flow": "steps"}) is None
    assert spec_from_plan(plan, "A loop", {"cycle": "a loop"}) is not None


def test_a_composed_scene_missing_its_own_fields_is_not_drawn():
    """Chose bars, gave no numbers. Nothing can draw that, and inventing the
    numbers is the one thing this pipeline must never do."""
    plan = OnScreenPlan(headline="Three figures", scene_kind="bars",
                        nodes=["one", "two"])

    assert spec_from_plan(plan, "Three figures", {"bars": "quantities"}) is None


def test_a_scene_with_no_shape_stays_words_on_a_frame():
    plan = OnScreenPlan(headline="What a neuron is", points=["threshold"],
                        scene_kind="none")

    assert spec_from_plan(plan, plan.headline, dict(SCENE_KINDS)) is None


def test_the_composed_headline_becomes_the_drawn_caption():
    plan = OnScreenPlan(headline="Where the signal goes", scene_kind="flow",
                        nodes=["electrode", "amplifier"])
    spec = spec_from_plan(plan, plan.headline, {"flow": "steps"})

    assert spec is not None and spec.caption == "Where the signal goes"


def test_on_screen_words_are_capped_where_a_frame_ends():
    plan = OnScreenPlan(
        headline="a headline far longer than any frame could ever hold at this size",
        points=["one", "two", "three", "four", "five", "six"],
    )

    # The plan itself is what the model said; the cap is applied where it is
    # stored, so the words on the frame are the ones that fit.
    from pipeline.generation import SceneVisual

    visual = SceneVisual(headline=plan.headline, points=plan.points)
    assert len(visual.headline) <= MAXIMUM_HEADLINE_LENGTH
    assert len(visual.points) <= 4


def test_the_fallback_headline_is_the_brief_never_the_narration():
    """With no model, a scene still must not print what is being said."""
    brief = "The McCulloch-Pitts neuron: inputs, weights and a threshold"
    narration = "Let us begin by considering the very first model of a neuron."

    assert fallback_headline(brief, narration) == "The McCulloch-Pitts neuron"
    assert fallback_headline("", narration).startswith("Let us begin")
