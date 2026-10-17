"""The scene drawn when no round drew one: the headline and the section's picture,
timed to the narration, written without a model.

A scene always ends with a clip. When every round crashed, or the model could not
be reached, this is it: plain, true to the source, and plainly a stand-in. The
person sees why it was used and can ask for the scene again.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FALLBACK_NOTE = "A plain stand-in: the headline and the slide's picture."

PROGRAM = '''# /// script
# requires-python = ">=3.11"
# dependencies = ["manim>=0.19", "pillow"]
# ///
"""{note}"""
from manimkit import *

HEADLINE = {headline}
PICTURE = {picture}


class Fallback(ExplainerScene):
    def construct(self):
        title = self.label(HEADLINE, size=52, bold=True, at=(0, 3.1))
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        if PICTURE:
            shown = self.picture(PICTURE, height=5.2, at=(0, -0.5))
            self.play(FadeIn(shown), run_time=0.8)
            self.play(shown.animate.scale(1.08), run_time=max(1.0, BRIEF.seconds - self.now))
        self.finish()


run(Fallback)
'''


def fallback_program(brief: dict[str, Any], folder: Path) -> str:
    pictures = list(brief.get("pictures") or (brief.get("assets") or {}).get("pictures") or [])
    slide = brief.get("slide_image") or (str(folder / "slide.png")
                                         if (folder / "slide.png").exists() else "")
    picture = pictures[0] if pictures else slide
    headline = (brief.get("headline") or brief.get("section_title") or "").strip()[:60]
    return PROGRAM.format(note=FALLBACK_NOTE, headline=json.dumps(headline),
                          picture=json.dumps(picture.replace("\\", "/")))
