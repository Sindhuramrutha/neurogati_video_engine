# What This System Actually Is

Before choosing an architecture, it is worth being precise about the problem.
v1's shape was inherited from "use an LLM to write Manim." That framing decided a
lot before anyone examined it.

---

## Strip it to the core

The system takes **an explanation that exists in text** and produces **the same
explanation delivered as synchronised audio and moving pictures.**

That is a *translation* problem, not a *generation* problem. The ideas, the
ordering, the emphasis — all of it is already in the source. Nothing needs
inventing. v1's own scene-script prompt says this in its strongest terms:

> *Every fact, number, equation, example, and claim in the narration must be
> traceable to the detailed content given to you. Do not invent…*

If the system's job is faithful translation, then **any component with the freedom
to invent is a liability, not a feature.** Arbitrary code generation is maximum
freedom to invent. That is worth sitting with.

---

## Three separable problems

v1 fuses these into one LLM call. They have different natures and deserve
different mechanisms.

### 1. Comprehension — what is being taught?

Reading prose and deciding: these are the concepts, this is their order, this one
depends on that one, this sentence is the crux and that one is an aside.

**Genuinely needs a language model.** This is semantic work with no closed form.
It is also the part v1 does best.

### 2. Depiction — what should be on screen?

Given "the membrane holds a −70 mV potential difference," decide that the viewer
should see a membrane, an inside and outside, a voltage readout.

**Needs a model, but the output space can be bounded.** There is a difference
between "emit Python that draws something" and "choose a *membrane diagram* from a
known vocabulary and populate its labelled slots." Both require judgment; only one
can produce a syntax error, an off-frame element, or an invented API.

### 3. Realisation — where does each pixel go, and when?

Positions, sizes, collision avoidance, frame fitting, beat durations summing to
narration length.

**Needs no model at all.** This is layout and scheduling — a solved class of
problem with decades of prior art (constraint solvers, flexbox, graph layout,
timeline scheduling). Every one of these is deterministic, testable, and
verifiable.

**v1 hands all three to one LLM call.** Failures 1, 2 and 3 in the
[post-mortem](../diagnosis/v1-postmortem.md) are all realisation failures — the
part that needed no model.

---

## The information the model does not have

`scene_coder.py` is asked to guarantee properties it cannot observe:

| Property | Knowable at generation time? |
|---|---|
| Rendered width of a `Text` at font size 36 | No — depends on font metrics |
| Bounding box of a `VGroup` after `.arrange()` | No — depends on children |
| Whether two elements overlap | No — depends on both boxes |
| `Code` block width | No — depends on longest line |
| Total animation runtime | Only by manual arithmetic |

Every one of these is **trivially knowable after construction** — Manim exposes
`.width`, `.height`, `.get_center()`. The information exists; it is simply on the
wrong side of the generation boundary.

This suggests a structural move: **let code that can measure do the positioning.**
Whether that means a layout engine, a post-generation repair pass, or a render-and-
check loop is an open question — see
[architecture-options.md](../design/architecture-options.md). But the diagnosis is
the same in all cases: v1 asks for guarantees at a point where the necessary facts
are unavailable.

---

## Where does correctness actually live?

Worth naming explicitly, because it determines what a rewrite can guarantee.

| Property | Enforceable how? |
|---|---|
| Narration is faithful to source | Prompt + human review. Irreducibly probabilistic. |
| Audio matches narration text | Structural — TTS reads the text. |
| Subtitles match audio | Structural — same word timings. v1 already gets this right. |
| Animation duration matches audio | **Structurally enforceable.** Beats as data, durations computed. |
| Nothing off-frame | **Structurally enforceable.** Layout engine, or measure-and-fix. |
| No overlapping elements | **Structurally enforceable.** Same. |
| Valid API usage | **Structurally enforceable.** Types, or signature validation. |
| Visual is *pedagogically good* | Human judgment. Not automatable, and v1 was right not to try. |

Five of eight rows are currently enforced by asking a model nicely. All five are
mechanically enforceable.

**The rewrite's ambition should be measured by how many rows move from "prompt" to
"structural."**

---

## Framings worth considering

How you name the system shapes what you build. Some alternatives to "LLM writes
Manim":

**A compiler.** Source text → intermediate representation → target (video). The
LLM is the front-end parser; everything after the IR is deterministic. Gives you
a typed IR to validate, optimise, and test independently — and it becomes the
place quality is enforced. Compilers also have a well-understood answer to "how do
I know the output is right": you verify the IR, not the machine code.

**A document renderer.** Like a browser: content, a stylesheet, a layout engine.
The model produces semantic content; the engine handles typography, spacing, and
fitting. Browsers never emit off-screen text because layout is not the author's
job. This framing makes the design-system question primary.

**A scheduler.** The narration is a fixed timeline; visual events are jobs to be
placed on it. Timing correctness becomes a scheduling invariant rather than an
arithmetic exercise.

**A retrieval and assembly problem.** Most explanatory visuals are variations on a
small number of forms — a labelled diagram, a process flow, a comparison, a plot,
a code walkthrough. If the vocabulary is genuinely small, the task is selection and
population, not synthesis. Worth testing empirically against the 253 existing
scenes before assuming either way.

**An agent with tools.** The model is an actor that calls `place()`, `measure()`,
`connect()` — and gets real feedback from each. It cannot produce an invalid state
because tools validate their arguments. See
[agentic-stack.md](../design/agentic-stack.md).

These are not mutually exclusive. A plausible design is a compiler whose IR is a
document tree, laid out by an engine, with beats scheduled on an audio timeline —
authored by an agent with measuring tools.

---

## The question that should be answered first

**How much of explanatory animation is actually a bounded vocabulary?**

If most scenes are variations on a dozen forms, a component library plus layout
engine dominates: it eliminates whole failure classes at the cost of a ceiling on
expressiveness.

If scenes are genuinely bespoke, that ceiling becomes the binding constraint, and
the answer is a feedback loop instead — keep the freedom, add the ability to see.

**This is an empirical question, and you have 253 rendered scenes to answer it
with.** Sampling them and classifying by visual form is probably the
highest-value hour available before committing to an architecture.

Two failure modes to avoid:

- Building a component library that turns out to cover 60% of cases, leaving a
  permanent escape hatch that becomes the default path.
- Building an elaborate feedback loop when a fixed vocabulary would have made most
  of the errors unrepresentable.

See [open-questions.md](../open-questions.md).

---

## The one thing to keep

v1's audio-first timing is genuinely good design and should survive unchanged:
synthesise narration, measure word timings, derive both animation beats and
subtitles from that single source. Sync becomes structural rather than corrected.

Everything else is open.
