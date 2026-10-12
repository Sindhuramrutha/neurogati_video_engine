# /// script
# requires-python = ">=3.11"
# dependencies = ["manim>=0.19", "pillow"]
# ///
"""A worked example: a timeline whose stages appear on the words that name them,
each gaining emphasis while it is spoken about, then fading back as the next
arrives. Every label is a few words, recorded by manimkit for the checks.

The stages here come from an imaginary narration; a real scene takes its stages,
words and timings from brief.json."""

from manimkit import *      # every Manim name, and the kit

STAGES = [            # (label on screen, the narration words it lands on)
    ("A promising start", "promising start"),
    ("A turning point", "turning point"),
    ("A long decline", "long decline"),
]


class Timeline(ExplainerScene):
    def construct(self):
        accent, dim = self.look["accent"], self.look["dim"]

        title = self.label("How it changed", size=56, bold=True, at=(0, 2.9))
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.8)

        axis = Line([-5.5, 0, 0], [5.5, 0, 0], color=dim, stroke_width=4)
        self.play(Create(axis), run_time=0.8)

        points = [-4.0, 0.0, 4.0]
        shown = VGroup()
        for (text, words), x in zip(STAGES, points, strict=True):
            self.until(self.when(words))                 # the moment it is said
            dot = Dot([x, 0, 0], radius=0.16, color=accent)
            # Labels alternate above and below the line, so neighbours never overlap.
            name = self.label(text, size=36, at=(x, -1.0 if len(shown) % 2 == 0 else 1.0))
            self.play(FadeIn(dot, scale=0.5), FadeIn(name, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(name, color=accent), run_time=0.6)
            if len(shown):
                self.play(GrowArrow(Arrow(shown[-1].get_center(), dot.get_center(),
                                          buff=0.25, color=accent)), run_time=0.5)
            shown.add(dot)

        self.finish()                                    # exactly brief.seconds


run(Timeline)
