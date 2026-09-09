# Pipeline — Design Documentation

---

## The short version

v1 works — ~253 scenes across 25 chapters — but its costs grow faster than its
output. The core problem:

> **v1 asks a language model to write arbitrary Manim code from a text
> description, then has no way to check whether the result looks right.**

A human is the error detector. Production history shows the same three defects
handled by hand, repeatedly: elements off-frame, animation duration not matching
narration, and invented Manim API calls. None require judgment. All are
mechanically checkable.

The pattern that fixes this already exists in your codebase.
`agents/highlight_planner.py` constrains the model to a **closed-set choice over
real data** and computes geometry deterministically. `agents/scene_coder.py` does
the opposite. The rewrite's central question is how far the first pattern
generalises.

---

## Map

```
docs/
├── README.md                    ← you are here
│
├── diagnosis/
│   └── v1-postmortem.md         Evidenced failure analysis of v1
│
├── fundamentals/
│   ├── what-this-system-is.md   First principles: what problem is this?
│   └── quality-model.md         What "good" means; how it gets verified
│
├── design/
│   ├── architecture-options.md  Five shapes for v2, with tradeoffs
│   ├── beyond-manim.md          Is Manim the right target?
│   ├── tech-stack.md            ← the proposed stack, layer by layer
│   ├── data-layout.md           ← folder structure; files vs SQLite
│   ├── interfaces.md            Beyond the terminal: review UX, service, observability
│   └── agentic-stack.md         Frameworks and tools worth evaluating
│
├── architecture/
│   └── system-map.md            ← what is BUILT: boundaries, contracts, invariants
│
├── decisions/                   ADRs (Proposed until committed)
│   ├── 0001-preserve-audio-first-timing.md
│   ├── 0002-structured-output-over-free-text.md
│   ├── 0003-durable-incremental-state.md
│   ├── 0004-mechanical-checks-before-human-review.md
│   ├── 0005-files-as-source-of-truth.md
│   ├── 0006-langgraph-as-backbone.md
│   └── 0007-revideo-as-rendering-target.md
│
├── review-2026-09-09.md             Engineering review, first pass
├── review-2026-09-09-second-pass.md Engineering review, second pass
│
└── open-questions.md            Decisions to make, with how to answer them
```

**`design/` is what was proposed; `architecture/system-map.md` is what exists.**
When the two disagree, the system map wins — it is checked against the code and
carries the test names that enforce each claim. The design documents are dated
arguments, and a few describe a pipeline that was never built this way; each one
that does now says so in its own opening.

The stack itself is in **[design/tech-stack.md](design/tech-stack.md)**, with the
storage layout in **[design/data-layout.md](design/data-layout.md)**.

---

## What is already settled

Four decisions are argued as **Proposed** ADRs — independent of the big
architectural choice, each addressing a documented v1 failure:

| ADR | Decision |
|---|---|
| [0001](decisions/0001-preserve-audio-first-timing.md) | Keep audio-first timing. v1's best idea — do not discard it in a rewrite. |
| [0002](decisions/0002-structured-output-over-free-text.md) | Every LLM call returns a validated object, never text to be parsed and repaired. |
| [0003](decisions/0003-durable-incremental-state.md) | Save after every scene; explicit timeout and retries. |
| [0004](decisions/0004-mechanical-checks-before-human-review.md) | Machines check measurable properties; humans review craft only. |

---

## What is not settled

The architecture itself. [Five options](design/architecture-options.md) are laid
out with honest tradeoffs rather than a verdict, because the right answer depends
on [questions you have not yet answered](open-questions.md) — chiefly whether your
content is a bounded visual vocabulary.

**That question is empirically answerable.** You have 253 rendered scenes. Sample
40, classify them by visual form, and read the distribution. It is probably the
highest-value hour available before writing code.

---

## A note on "rewrite"

The [post-mortem](diagnosis/v1-postmortem.md) locates nearly every failure in two
places: scene code generation, and transport configuration. The audio pipeline,
compose layer, subtitle generation, state model, and staged CLI are sound — and
any architecture reuses them.

That is worth weighing against the instinct to start clean. Replacing one component
while keeping proven infrastructure is a much smaller project than rebuilding, and
carries less risk of losing what already works. See
[Q5](open-questions.md#q5--rewrite-or-evolve).

---

## Conventions

- Claims about v1 are traceable to its code, output, or production shell history.
  Where something is inference or opinion, it says so.
- ADRs start **Proposed** and become **Accepted** when committed to. Accepted ADRs
  are never edited — supersede instead.
- Links point to real files **inside this repository**. References to v1 name
  the file in prose instead: v1 lives in a different repository, so a relative
  link to it is dead for anyone who clones this one.

## Related

- v1 documentation — architecture, guides and ADRs for the previous pipeline.
  Outside this repository; alongside the v1 checkout described below.
- v1 source:
  `github-folder/original-pipeline-provided-by-neurovidya-team/neurogati_video_engine/`
