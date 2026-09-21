"""Draw one diagram spec as an animated clip, with Manim.

Run as a subprocess, reading the spec as JSON on stdin. Not imported: Manim
configures itself globally -- media directory, quality, logging, ffmpeg -- and
doing that inside the web process would leak those settings into every later
render and every other stage.

The animation is deliberately plain. Nodes appear in the order they are named,
then the arrows between them are drawn. That is the whole point of having an
animation backend at all: the diagram assembles while the narration describes
it, so the viewer's eye is where the words are. Anything more elaborate competes
with the narration.

Nothing here invents content. The nodes are the labels the spec carries, which
came from the source material; a spec with three nodes draws three.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


def build(spec: dict) -> None:
    from manim import (
        DOWN,
        LEFT,
        RIGHT,
        UP,
        Arrow,
        Create,
        FadeIn,
        Rectangle,
        Scene,
        Text,
        VGroup,
        config,
    )

    nodes: list[str] = [str(node) for node in spec["nodes"]][:6]
    seconds = float(spec.get("seconds", 4))
    kind = spec.get("kind", "flow")

    config.pixel_width = int(spec.get("width", 1920))
    config.pixel_height = int(spec.get("height", 1080))
    config.frame_rate = int(spec.get("frame_rate", 30))
    config.background_color = spec.get("background", "#0D0F14")
    config.disable_caching = True
    config.verbosity = "ERROR"

    accent = spec.get("accent", "#E879A8")
    text_colour = spec.get("text", "#E8EAF0")

    # Each beat is one node appearing; the arrows share the last beat, so the
    # whole build lands inside the narration it belongs to.
    beat = max(0.35, min(1.2, seconds / (len(nodes) + 2)))

    class Diagram(Scene):
        def construct(self) -> None:
            caption = None
            if spec.get("caption"):
                caption = Text(str(spec["caption"])[:70], font_size=30, color=text_colour)
                caption.to_edge(UP, buff=0.6)
                self.play(FadeIn(caption), run_time=beat * 0.6)

            boxes = VGroup()
            for label in nodes:
                box = Rectangle(width=3.2, height=1.3, color=accent, stroke_width=3)
                words = Text(label[:28], font_size=24, color=text_colour)
                words.move_to(box.get_center())
                boxes.add(VGroup(box, words))

            if kind == "stack":
                boxes.arrange(DOWN, buff=0.45)
            elif kind == "compare":
                boxes.arrange(RIGHT, buff=1.4)
            else:
                boxes.arrange(RIGHT, buff=0.9)
            boxes.scale(min(1.0, 11.5 / max(1.0, boxes.width)))
            boxes.move_to([0, -0.4 if caption else 0, 0])

            for box in boxes:
                self.play(FadeIn(box, shift=UP * 0.2), run_time=beat)

            if kind in {"flow", "cycle"} and len(boxes) > 1:
                for first, second in zip(boxes[:-1], boxes[1:], strict=False):
                    arrow = Arrow(
                        first.get_right(), second.get_left(),
                        buff=0.1, color=accent, stroke_width=4, max_tip_length_to_length_ratio=0.2,
                    )
                    self.play(Create(arrow), run_time=beat * 0.45)
                if kind == "cycle":
                    back = Arrow(
                        boxes[-1].get_bottom() + DOWN * 0.1,
                        boxes[0].get_bottom() + DOWN * 0.1,
                        buff=0.1, color=accent, stroke_width=3,
                        path_arc=-2.2, max_tip_length_to_length_ratio=0.15,
                    )
                    self.play(Create(back), run_time=beat * 0.8)
            elif kind == "compare" and len(boxes) > 1:
                for first, second in zip(boxes[:-1], boxes[1:], strict=False):
                    line = Arrow(
                        first.get_right(), second.get_left(), buff=0.15,
                        color=text_colour, stroke_width=2, tip_length=0,
                    )
                    self.play(Create(line), run_time=beat * 0.3)

            # Hold on the finished diagram: the narration usually keeps talking
            # about it after the last piece lands.
            self.wait(max(0.3, seconds - self.renderer.time))

    output = Path(spec["output"])
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as working:
        config.media_dir = working
        config.output_file = output.stem
        Diagram().render()
        made = sorted(
            (path for path in Path(working).rglob(f"{output.stem}.mp4")),
            key=lambda path: len(path.parts),
        )
        if not made:
            raise SystemExit("manim wrote no clip")
        output.write_bytes(made[0].read_bytes())


if __name__ == "__main__":
    build(json.loads(sys.stdin.read()))
