# Motion that explains -- not "things in, things out"

A scene that only fades labels in and out is a slide with a dissolve. Every beat
should *do* something that carries the idea. Pick the moves that fit what the
narration says at that moment:

| The narration says... | Show it by |
| --- | --- |
| A becomes B, one state turns into another | **Transform** A into B (`ReplacementTransform`, `TransformMatchingShapes`; in web: morph positions/sizes/colours with a tween) |
| X causes / leads to Y | **Draw the connection as it is said**: grow the arrow from X to Y (`GrowArrow`, `Create` on a path), then send a pulse or dot along it (`MoveAlongPath`) |
| Several parts make a whole | **Build up**: the diagram stays and grows part by part, each part arriving on its words; never clear the screen between related beats |
| A detail matters | **Zoom or pan** to it and back (Manim `MovingCameraScene` / `self.camera.frame.animate`; web: scale/translate a container), or `Indicate` / `Circumscribe` it |
| Two things differ | **Side by side, then contrast**: move them apart, highlight the difference, swap or overlay them |
| A quantity changes | **Animate the value**: a bar grows, a counter ticks (`ValueTracker` + `always_redraw`; web: tween a number) |
| A sequence or process | **A timeline or flow that advances**: a marker travels, each stage lights up as it is named and dims as the next arrives |
| Sorting, splitting, grouping | **Move the things themselves**: items fly into groups, split apart, merge |
| Back to an earlier idea | **Bring the earlier element back** (continuity with the section's previous scene in `section_scenes`) |

Rules of thumb:

- Bringing each thing on as it is named is right, and never counts against a
  scene. But a scene needs real moves too: the "Motion explains" check fails one
  with fewer than 3 animations that **move, grow, transform or connect**.
- **Never shrink something with words in it** to make motion. Scaling a group
  of labels down makes them too small to read, and "Text is large enough" fails.
  Move it, fade the older things out, or zoom into a part instead.
- Keep a **persistent anchor** (the main diagram, the picture) on screen and
  change it, rather than replacing the whole frame each beat.
- Time each move to land **on the word** that names it (`when("...")` in every kit).
- Ease, don't jerk: smooth rate functions; 0.6-1.2 s for most moves.
- Use the slide's own picture as the anchor when there is one: zoom into its
  parts, label them as they are named, trace its arrows.
