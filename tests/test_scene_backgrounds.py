"""A scene's background: painted art or a gradient, chosen by its maker, never dark,
and switched off and on from its page."""

import io

from PIL import Image

from pipeline import scene_backgrounds


def state():
    return {"calls": {"agent": 0, "vision": 0}, "events": []}


def png(grey: int) -> bytes:
    """Art to its edges: a painted scene varies along every edge (a framed one does not)."""
    import random

    image = Image.new("L", (1376, 768), grey)
    pixels = image.load()
    for x in range(1376):
        for y in range(768):
            pixels[x, y] = max(0, min(255, grey + random.randint(-40, 40)))
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    return buffer.getvalue()


def test_a_painting_inside_a_margin_is_seen_as_framed(tmp_path):
    framed_one = Image.new("RGB", (1376, 768), (250, 246, 238))
    framed_one.paste((120, 160, 120), (60, 60, 1316, 708))
    framed_one.save(tmp_path / "framed.png")
    (tmp_path / "bleed.png").write_bytes(png(220))
    assert scene_backgrounds.framed(tmp_path / "framed.png")
    assert not scene_backgrounds.framed(tmp_path / "bleed.png")


def test_a_wider_mat_is_framed_and_a_soft_wash_is_not(tmp_path):
    """v7's "soft dawn wash" was thrown away as framed: flat all round, as a mat is,
    but it stays smooth inward where a mat ends at the picture."""
    wide_mat = Image.new("RGB", (1376, 768), (250, 246, 238))
    wide_mat.paste((120, 160, 120), (110, 110, 1266, 658))
    wide_mat.save(tmp_path / "wide.png")
    wash = Image.linear_gradient("L").resize((1376, 768)).point(lambda v: 225 + v // 16)
    Image.merge("RGB", (wash, wash.point(lambda v: v + 4), wash)).save(tmp_path / "wash.png")

    assert scene_backgrounds.framed(tmp_path / "wide.png")
    assert not scene_backgrounds.framed(tmp_path / "wash.png")


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
