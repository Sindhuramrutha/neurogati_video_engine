# ADR 0007 — Revideo as the rendering target

## Status

**Proposed — gated on a porting test.** See *Validation* below. This is the one
decision in the set that should not be accepted on argument alone.

## Context

v1 renders with Manim, chosen because 3Blue1Brown uses it. That is a reason to
admire Manim, not necessarily to generate code for it.

Three of v1's four documented failures trace to properties of the target itself:

| Failure | Root cause in Manim |
|---|---|
| "cut off at any edge" (repeated by hand) | Layout is imperative and unmeasurable before construction |
| "55.6s but narration is 52.3s" (repeated) | Duration is **emergent** — summed from `run_time`/`wait` |
| `gap_length` invented | Large API surface, validated only at runtime |

A fourth — slow review — follows from render cost, now worse since the switch to
`-qh` (1080p) while `manim_render.py`'s docstring still claims 480p15 "for fast
iteration."

The preliminary corpus classification is relevant: **labelled-diagram 31%,
process-flow 15%, title-or-text 10%** — roughly 56% is composition revealed over
time, which a layout engine handles natively. **physical-system is ~20%**, which is
where Manim's animation model genuinely earns its place.

## Decision

**Adopt Revideo as the default rendering target**, with the IR as the boundary so
the choice stays reversible.

Revideo: TypeScript, **MIT licensed**, ~4k stars, actively maintained. A fork of
Motion Canvas — built specifically for explanatory and educational video —
extended with a rendering API and template system for automated pipelines.

What it changes structurally:

- **Duration is declared** (`durationInFrames`), content is a function of time.
  A clip that overruns its narration is unrepresentable, not merely detected.
- **CSS-style layout** — fitting is a solved problem, not an arithmetic exercise
  performed by a model that cannot measure.
- **`<Player/>` renders in the browser** — preview without rendering, collapsing
  the review loop.
- **Parallelised rendering across workers** — addresses
  [Q9](../open-questions.md#q9--batch-or-interactive) directly.
- **Frame-accurate audio sync** — composes with
  [ADR 0001](0001-preserve-audio-first-timing.md).

### Rejected: Remotion

The better-known equivalent, with a larger ecosystem and the same declared-duration
model. Rejected on licensing: free only for individuals and companies **up to three
people**; beyond that, a Company License at **$0.01/render with a $100/month
minimum**. Not ruinous, but it places a commercial dependency at the core of the
system when an MIT-licensed equivalent exists with the same architectural
properties.

### Manim retained as a specialist option

Not deleted. The ~20% of scenes that are physical simulation are where its model is
strongest, and v1 already demonstrates that per-scene renderer routing works (it
routes between Manim and Matplotlib today). If the porting test shows Revideo
handling simulation poorly, routing is the fallback rather than reversal.

## Validation — required before accepting

**Port one `physical-system` scene from the existing corpus to Revideo.** Pick
from the hardest category, not the easiest.

Assess:

1. Does the animation read as well as the Manim original?
2. How long did it take, versus writing the Manim version?
3. Does `<Player/>` preview meaningfully beat the render-and-watch loop?
4. Does declared duration feel natural, or like fighting the tool?

If simulation is awkward but composition is good, the answer is routing — Revideo
for the ~56%, Manim for the ~20% — not abandoning either.

**This ADR stays Proposed until that test is done.** It is the same standard
applied to [Q1 and Q2](../open-questions.md#suggested-order): decide from evidence,
not argument.

## Consequences

**Positive**

- Three documented failure classes become structurally impossible
- Review latency drops from minutes to instant
- Parallel rendering built in
- MIT licence, no commercial relationship
- Typed IR consumed by real components — no arbitrary code generation

**Negative**

- **A second language and toolchain.** The largest cost. Mitigated by the IR being
  a JSON file, so the boundary is rarely crossed mentally.
- **Smaller ecosystem than Remotion.** 4k stars is healthy; the bus factor is real.
  MIT means forking is possible.
- **The 253-scene Manim corpus stops being directly reusable as code.** It remains
  valuable as reference, eval data, and evidence for
  [Q1](../open-questions.md#q1--is-your-content-a-bounded-visual-vocabulary).
- **Physical simulation idiom differs** from `ValueTracker`/`always_redraw`. This is
  exactly what the porting test must probe.

**The insurance policy**

The IR is why this is reversible. If Revideo disappoints, write a different IR
consumer — Manim, SVG, or something else — and the entire Python side is untouched.
That is the reason for a typed boundary rather than calling a rendering library
directly from pipeline code.

## Revisit if

The porting test goes badly, Revideo's maintenance stalls, or the corpus
classification shifts materially toward simulation-heavy content once
[Q1](../open-questions.md#q1--is-your-content-a-bounded-visual-vocabulary) is
answered properly.
