# v1 Post-mortem

An evidenced account of where the current pipeline breaks down. Every claim here
is traceable to the v1 codebase, its generated output, or the shell history of
real production runs — not impressions.

**Scale it reached:** ~253 scenes across 25 chapters in 4 projects. This is not a
prototype that failed; it is a working system whose costs grew faster than its
output.

---

## The one-sentence diagnosis

**v1 asks a language model to write arbitrary Manim code from a text description,
then has no way to check whether the result looks right.** Everything below is
downstream of that.

---

## What the operator actually did

From PowerShell history of real runs (`errors.txt`, UTF-16 console history):

```
--revise "Keep every visual element fully inside the frame. Nothing should be
          cut off at any edge. Scale down and reposition oversized objects..."
          ← issued for scene 0, then again for scene 1

--revise "The animation is 55.6 seconds but the narration is only 52.3 seconds.
          Shorten the animation runtime by about 3.3 seconds..."
          ← issued for scene 2, then again for scene 1 (60.2s vs 56.5s)

--revise "Fix the Manim code error: Mobject.__init__() got an unexpected
          keyword argument 'gap_length'. Remove gap_length completely..."
```

Three distinct classes of defect, each hit repeatedly, each requiring a human to
notice it, describe it in prose, and pay for a full regeneration.

That is the real cost of v1: **a human is the error detector.**

---

## Failure 1 — The system cannot see its own output

**Evidence:** the repeated "keep every visual element fully inside the frame"
revisions.

`scene_coder.py` receives a text brief and emits Python. It never observes a
rendered frame. Its only information about the frame is a sentence in the system
prompt:

> *the visible frame is about 14 units wide and 8 units tall… stay within roughly
> ±6.5 horizontally and ±3.5 vertically*

So the model must predict, from arithmetic alone, the rendered bounding box of
text at an unknown font, a `VGroup` after `.arrange()`, a `Code` block whose width
depends on its longest line. It cannot. It guesses, and the guess is often wrong.

The prompt has grown a long list of compensating rules — stale `.copy()`
positions, re-zooming already-fitted groups, labels near multi-part structures.
Each was added after a real failure. **Each is a patch for the absence of
feedback.**

> A rule that says "don't go off-frame" is not a substitute for the ability to
> notice that you did.

The vision-critique loop that would have closed this was removed for good reasons
(cost, and a human re-checked it anyway). But nothing replaced it, so the blind
spot remained and the prompt absorbed the pressure.

---

## Failure 2 — Timing is asserted, not constructed

**Evidence:** repeated duration-mismatch revisions (55.6 vs 52.3; 60.2 vs 56.5).

v1's timing contract is that the model performs arithmetic correctly across a
whole scene: sum every `run_time` and `self.wait()`, including inside loops, and
land within ±3s of the narration.

The system prompt spends substantial space teaching this — a Pacing rule, a
dedicated warning that loops are "the single most common way this budget gets
blown", and a worked example of dividing a beat duration by item count.

Post-processing then rewrites the output unconditionally, because the instruction
is not trusted: `_clamp_zero_durations()` wraps every duration in
`max(0.05, …)`, since computed expressions can evaluate negative at render time.

**The architecture makes correct timing possible but not guaranteed.** A design
where beat durations are data — computed by the system, not summed by the model —
makes the failure unrepresentable.

---

## Failure 3 — The lint gate cannot see the API

**Evidence:** `Mobject.__init__() got an unexpected keyword argument 'gap_length'`.

`manim_lint.py` is a regex pass. It catches a fixed list of known-fatal patterns —
`MathTex`, `self.camera.frame` on plain `Scene`, unsized `Code`, unregistered
asset keys — each added after a real crash.

It performs **zero signature validation** (verified: no `inspect`, no `signature`,
no kwarg checking anywhere in the file). An invented keyword argument is invisible
to it and surfaces only as a runtime crash — after a full render has been paid
for.

This matters more now than it used to. `manim_render.py` was changed to render at
`-qh` (1080p), while its own docstring still claims:

> *Renders at low quality (480p15) for fast iteration through the critique loop.*

The docstring is stale, and the staleness hides a real regression: **the retry
loop was designed around cheap renders and now burns expensive ones.** Three
attempts at 1080p is a materially different cost from three at 480p15.

Meanwhile `manim_reference.py` already introspects the live package to build its
API reference. The machinery to validate signatures exists — it just was not
pointed at the generated code.

---

## Failure 4 — Progress is lost on interruption

`run_chapter.py` calls `save_scenes()` **once, after the entire render loop**
(line 277). A 22-scene chapter that fails at scene 20 persists nothing from those
20 scenes.

This is not a hypothetical. v1's own newer code documents it as settled fact —
from `pptx_deck_pipeline.py`:

> *State is saved after every single slide, not once at the end of the whole run —
> a hard lesson from the regular chapter pipeline, where a single end-of-batch save
> meant an interrupted run could lose every already-rendered scene's progress.
> That mistake isn't repeated here.*

The lesson was learned and applied to the new component. The original was never
fixed.

---

## Failure 5 — Fragile transport

`utils/llm.py` constructs `OpenAI()` with no `timeout` and no `max_retries`
(verified: neither appears in the file).

Consequences observed in production: a dropped connection surfaces as
`Connection error.`, and the scene is marked failed with **no code generated** —
`render_attempts=0`, nothing to revise. In one observed run this killed 3 of 4
scenes and cost ~40 minutes.

The per-scene `except` in `run_chapter.py` contains the blast radius, which is
good design. But it converts a transport blip into lost work rather than a retry.

A related trap: because the failure leaves no code, `--revise` cannot help — it
regenerates *from* existing code. The operator must know to use `--stage render`
instead. The CLI does not distinguish these cases.

---

## Failure 6 — Prompt as accumulated scar tissue

`scene_coder.py`'s system prompt is ~36 KB. It is well written and every rule in
it was earned. That is precisely the problem.

The prompt has become the place where all architectural pressure lands:

| The prompt teaches | Because the architecture cannot |
|---|---|
| Frame bounds arithmetic | see the rendered frame |
| Duration summation | compute timing from data |
| "never use MathTex" | express the constraint in types |
| Overlap avoidance rules | model spatial occupancy |
| Loop duration division | represent beats as structured data |
| Colour palette consistency | enforce a design system |

Each rule is individually sensible. Collectively they are a specification being
enforced by persuasion.

**Prompt rules are probabilistic; type systems and layout engines are not.** Every
rule in that list is a candidate for becoming a structural guarantee.

---

## What v1 got right

A rewrite that discards these would be a regression.

- **Audio-first timing.** Synthesising narration before visuals, and deriving both
  animation beats and subtitles from one set of word timings, makes sync
  structural. This is the strongest idea in v1 and should be preserved outright.
- **Per-scene failure isolation.** One scene's error never kills the batch.
- **Resumable staged execution.** Stage-by-stage CLI with on-disk state.
- **The human review checkpoint.** Deciding *not* to automate aesthetic judgment
  was correct. The problem is that humans are also catching mechanical defects
  (clipping, timing) that machines should catch first.
- **Introspected API reference.** `manim_reference.py` refuses to trust
  hand-written docs. Right instinct, under-applied.
- **Closed-set grounding in `highlight_planner.py`.** See below — this is the
  most important thing in the repository.

---

## The pattern v1 already discovered

`agents/highlight_planner.py` — the newest agent — is architecturally different
from everything around it:

> *Split into an LLM "grounding" step and a pure-Python "formatting" step on
> purpose. The LLM's only job is a closed-set choice — which real `shape_id`, from
> the list it's given, matches what the narration is currently saying — never
> inventing a shape or a position. All of the actual geometry (the `manim_bbox`
> each shape already carries) is known in advance, so turning a chosen `shape_id`
> into the literal Manim instruction is deterministic formatting, not something
> worth spending an LLM call to get right or wrong.*

Read against the failures above, this is the thesis of the rewrite:

| | `scene_coder.py` | `highlight_planner.py` |
|---|---|---|
| LLM output | arbitrary Python | one ID from a fixed list |
| Invalid output possible? | yes, unboundedly | no — closed set |
| Geometry | model guesses | computed, known in advance |
| Verification | render and hope | correct by construction |

The same codebase contains both the problem and the demonstrated solution. The
question the new pipeline must answer is **how far that pattern generalises** —
from "point at a slide element" to "build an explanatory animation."

That is not obvious, and it is the central design question. See
[../design/architecture-options.md](../design/architecture-options.md).

---

## Cost summary

| Failure | Detected by | Cost per occurrence |
|---|---|---|
| Off-frame | human eye | full regeneration + review round |
| Duration drift | automated check | retry (now at 1080p) |
| Invented kwarg | runtime crash | wasted render + retry |
| Lost progress | interruption | entire batch re-run |
| Connection drop | scene failure | scene lost, operator confusion |

At 253 scenes, small per-scene costs dominate. The rewrite's target is not better
prose in the prompt — it is **moving each row of this table from "detected late by
a human" to "impossible by construction."**
