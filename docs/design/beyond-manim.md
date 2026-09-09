# Is Manim the Right Target?

v1 uses Manim because 3Blue1Brown does. That is a reason to admire Manim, not
necessarily to generate code for it. Worth resolving early: building a layout
engine or typed IR on top of the wrong target is expensive to undo.

---

## What Manim is actually good at

- Mathematical animation primitives — transforms, morphing, value trackers
- A genuine aesthetic tradition; output looks like serious explanation
- Python, so it composes with the rest of the stack
- Rich vector primitives and a real animation model

## What it costs here

**Rendering is slow.** Now at `-qh` (1080p), each attempt is expensive, and the
retry loop was designed around 480p15 renders. This directly shapes how many
verification iterations are affordable.

**Layout is imperative and unmeasurable ahead of time.** You construct, then
measure. There is no declarative layout pass, which is exactly why v1's generator
cannot know whether something fits.

**API surface is large and version-fragile.** `manim==0.20.1` is pinned because a
minor upgrade renamed an attribute and crashed real scenes. `gap_length` was
hallucinated because the surface is big enough to guess wrong in.

**Verification is awkward.** Checking a rendered frame means running a full render.
Nothing is inspectable between "code" and "video."

**LaTeX is disallowed**, so all mathematics is Unicode `Text` — a real constraint
for a mathematics-heavy course.

---

## Alternatives

### SVG + a timeline

Generate SVG scenes, animate declaratively, rasterise with `cairosvg` (already a
dependency) or headless Chromium.

**For:** layout is measurable *before* rendering — text metrics, bounding boxes,
all computable. Trivial to inspect and diff. Very fast. Web-native, so a browser
preview is nearly free.

**Against:** you build the animation model yourself. Loses Manim's mathematical
primitives and its aesthetic defaults.

**Notable:** this makes Tier 1 checks nearly free — the thing v1 is worst at.

### Web-native (HTML/CSS/Canvas, headless capture)

Compose scenes as web pages; capture frames via Playwright/Puppeteer.

**For:** the most mature layout engine in existence — flexbox and grid solve
fitting properly. Enormous ecosystem (D3 for data, KaTeX for mathematics without a
LaTeX install, Motion/GSAP for animation). Live preview in a browser is free, which
matters a lot for [interfaces](interfaces.md). Text metrics measurable pre-render.

**Against:** frame capture pipeline to build; timing precision needs care. A
different aesthetic tradition — closer to modern explainer than 3B1B.

**Worth weighing seriously.** "Elements must fit" is a solved problem in CSS. v1
spends prompt paragraphs and human review rounds on it.

### Slides as source (PPTX)

Covered as [Option E](architecture-options.md#option-e--deck-first). No layout risk
because a human already laid it out.

### Hybrid: SVG/web for composition, Manim for set pieces

Most scenes are labelled diagrams, comparisons, flows, plots — well served by a
layout engine. A minority genuinely need mathematical animation.

Route by need: cheap, verifiable path for the common case; Manim where its
primitives earn their cost. Mirrors v1's existing manim/matplotlib split, which
already establishes that per-scene renderer routing works.

---

## Rendering as a separate question

Whatever the authoring target, note that **v1's deterministic layer is target-
independent**: TTS, alignment, compose, stitch, subtitles all operate on audio and
video files. That layer is reusable and worth preserving in any rewrite.

The decision here concerns only the scene-authoring surface.

---

## Comparison

| | Manim | SVG | Web | PPTX |
|---|---|---|---|---|
| Layout solved | no | partly | **yes** | **yes** (human) |
| Measurable pre-render | no | **yes** | **yes** | **yes** |
| Render speed | slow | **fast** | **fast** | **fast** |
| Math notation | Unicode only | needs work | **KaTeX** | authored |
| Animation model | **rich** | build it | libraries | limited |
| Preview/iteration | slow | **instant** | **instant** | **instant** |
| Aesthetic fit (3B1B) | **native** | achievable | different | different |
| v1 reuse | **total** | partial | partial | done |

---

## The question to answer

**Is Manim's animation model load-bearing for your content, or is it aesthetic
preference?**

Sample the 253 scenes and count how many genuinely need mathematical animation —
morphing transforms, value trackers, continuous parametric motion — versus static
composition revealed over time.

If most scenes are "arrange labelled things, reveal them in sync with narration,"
a layout-first target removes the failure classes v1 fights hardest, and Manim
becomes a specialist tool for the minority that needs it.

If mathematical animation is central, Manim stays — and the design question
becomes how to make it measurable, which points toward
[Option B](architecture-options.md#option-b--agent-with-measuring-tools) or a
post-construction measurement pass.

Either way this should be settled **before** building layout machinery.
