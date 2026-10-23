"""A scene's background: painted art or a gradient, chosen by its maker, never dark,
and switched off and on from its page."""

import io

from PIL import Image

from pipeline import scene_backgrounds


def state():
    return {"calls": {"agent": 0, "vision": 0}, "events": []}


def png(grey: int) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (1376, 768), (grey, grey, grey)).save(buffer, format="PNG")
    return buffer.getvalue()


def test_a_gradient_is_never_dark():
    made = scene_backgrounds._gradient({"colours": ["#1a1a40", "#fdf6ec"], "split": "right",
                                        "panel": "#222222"})
    for colour in made["colours"] + [made["panel"]]:
        red, green, blue = (int(colour[i:i + 2], 16) for i in (1, 3, 5))
        assert (0.299 * red + 0.587 * green + 0.114 * blue) / 255 >= 0.71, colour
    assert made["colours"][1] == "#fdf6ec", "a light colour is left as it is"
    assert scene_backgrounds._gradient({"split": "sideways"})["split"] == "none"


def test_a_dark_painting_is_painted_lighter_then_given_up_for_a_gradient(tmp_path,
                                                                         monkeypatch):
    asked = []
    monkeypatch.setattr(scene_backgrounds, "draw_background",
                        lambda request: asked.append(request) or png(40))
    record = state()

    made = scene_backgrounds._painted(tmp_path, "a starry night sky", {}, record)

    assert made["kind"] == "gradient", "dark twice: a light gradient instead"
    assert "much lighter" in asked[1]
    assert not list(tmp_path.glob("background-*.png")), "the dark one is not kept"


def test_a_painting_is_made_once_and_switched_off_and_on(tmp_path, monkeypatch):
    asked = []
    monkeypatch.setattr(scene_backgrounds, "draw_background",
                        lambda request: asked.append(request) or png(235))
    monkeypatch.setattr("pipeline.scene_lab.write_brief", lambda project, visual: {"new": 1})
    spec = {"background": {"kind": "image", "describe": "a soft pastel botanical border"}}

    assert scene_backgrounds.choose(None, None, tmp_path, spec, {}, state()) == {"new": 1}
    assert scene_backgrounds.choose(None, None, tmp_path, spec, {}, state()) is None, \
        "the same background is not painted again"
    assert len(asked) == 1 and "never dark" in asked[0]
    assert scene_backgrounds.for_brief(tmp_path)["kind"] == "image"

    scene_backgrounds.switch(tmp_path, False)
    assert scene_backgrounds.for_brief(tmp_path) is None, "off: the program draws none"
    scene_backgrounds.switch(tmp_path, True)
    assert scene_backgrounds.for_brief(tmp_path)["kind"] == "image"
