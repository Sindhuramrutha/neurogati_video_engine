# Open Questions

The decisions that shape everything else. Each is framed with what it depends on, what it implies, and — where possible — how to answer it with evidence rather than argument.

Answered questions graduate to an [ADR](decisions/).

---

## Q1 — Is your content a bounded visual vocabulary?

**Why it matters:** this single answer separates the structured architectures
(typed IR, component library) from the flexible ones (codegen with verification,
tool-calling agent). If most scenes are variations on a dozen forms, structure wins
decisively. If the tail is long and matters, structure becomes a ceiling you fight.

**How to answer it — do this first.** You have **253 rendered scenes**. Sample 40
at random, watch them, and classify by visual form: labelled diagram, process
flow, comparison, plot, code walkthrough, physical simulation, title/text, other.

Then read the distribution:

- Top 10 forms cover **>80%** → component library or typed IR is well justified
- Long tail with no clear modes → a feedback loop is the honest answer
- Bimodal → hybrid: components for the head, escape hatch for the tail (with a
  firm rule about when the escape is allowed)

**This is probably the highest-value hour available before writing any code.**

**Status:** open.

---

## Q2 — Is Manim's animation model load-bearing?

**Why it matters:** determines whether you build on Manim or move to a
layout-first target. Expensive to reverse after building layout machinery.

**How to answer:** in the same sample, count scenes that genuinely need
mathematical animation — morphing transforms, value trackers, continuous
parametric motion — versus static composition revealed over time.

If most are "arrange things, reveal in sync with narration," a target with real
layout (SVG, web) removes v1's hardest failure class outright.

See [design/beyond-manim.md](design/beyond-manim.md).

**Status:** open.

---

## Q3 — What is the quality target?

**Why it matters:** determines how much machinery is justified. These are very
different projects.

| Target | Implies |
|---|---|
| Most scenes need no revision | Fix Tier 1 mechanically. Modest, achievable. |
| Human reviews craft only | Tier 1 structural + Tier 2 largely automated. |
| Unattended for a content class | Confident Tier 2 verification. Realistic only for narrow inputs (e.g. decks). |

See [fundamentals/quality-model.md](fundamentals/quality-model.md).

**Status:** open.

---

## Q4 — Who operates this?

**Why it matters:** decides whether interfaces are a convenience or a product.

- **Just you** → CLI + local review app; no auth, no deployment
- **Neurovidya content team** → hosted service, upload, review links, accounts
- **Both** → clean pipeline/interface separation from day one

Even if the web layer comes later, **the separation decision should be made now** —
retrofitting it is expensive.

See [design/interfaces.md](design/interfaces.md).

**Status:** open.

---

## Q5 — Rewrite, or evolve?

**Why it matters:** the framing of the entire project.

**Evolve** — v1 has ~253 scenes of proven output and a solid deterministic layer
(TTS, alignment, compose, stitch, subtitles) that any design reuses. Its failures
are concentrated in one component: `scene_coder.py`. Replacing that while keeping
everything else is a much smaller project than it feels like.

**Rewrite** — a clean typed core is hard to retrofit; v1's structure assumes
"generate code then check it."

**Worth noting honestly:** the [post-mortem](diagnosis/v1-postmortem.md) locates
almost every failure in scene generation and transport. The audio pipeline, compose
layer, state model, and CLI structure are sound. That is an argument for a targeted
replacement rather than a ground-up rebuild — a rewrite risks discarding working
infrastructure to fix one component.

**Status:** open.

---

## Q6 — What is the deck-first path's role?

**Why it matters:** `pptx_deck_pipeline.py` works today, and you have 12
Demystifying the Brain decks. It could be the production track while a more
ambitious generator is developed without schedule pressure.

Options: primary product; stopgap; parallel track for a different content type; or
abandoned.

**Worth weighing:** it is the only option that ships reliably now, and it shares
most of its infrastructure with any other choice.

**Status:** open.

---

## Q7 — How is the design system expressed?

**Why it matters:** v1 encodes visual consistency as prose in a prompt — palette,
font hierarchy, background colour, entrance variety. It is enforced by persuasion
and cannot be tested.

Alternatives: a token/theme system consumed by renderers; components with
consistency built in; a post-generation normalisation pass.

**Status:** open. Likely follows from Q1.

---

## Q8 — Where does human judgment enter?

**Why it matters:** v1 has exactly one checkpoint — after all scenes render. That
is late: a misread of the source propagates through audio and rendering before
anyone sees it.

Candidate earlier checkpoints: after scene splitting (cheapest place to catch a
structural misread), after narration, after the IR but before rendering.

**Tension:** more checkpoints mean more interruption. But an IR review — reading a
structured description of what will be drawn — is far faster than watching a
rendered clip, and catches the same class of error earlier.

**Status:** open.

---

## Q9 — Batch, or interactive?

**Why it matters:** v1 renders scenes sequentially, and a 22-scene chapter is a
long opaque wait. Scene rendering is **embarrassingly parallel** — nothing depends
on another scene's render.

Parallelism could cut wall-clock time by close to an order of magnitude, and it is
independent of every other decision here. It may be the largest available speedup.

**Status:** open. Low risk, high value.

---

## Q10 — What is the fabrication guarantee?

**Why it matters:** the most dangerous defect this system can produce is
**invented on-screen data** — a number, label, or date that was never in the
source. It looks authoritative and fails silently.

v1 addresses this with prompt rules in three separate places. No mechanical check
exists.

A structural check is feasible: extract every string rendered on screen, verify
each against the source document, flag anything unattested.

**Should this be a hard invariant rather than an instruction?**

**Status:** open. Arguably the most important correctness question here.

---

## Suggested order

1. **Q1 and Q2 together** — one sampling exercise answers both, and they gate the
   architecture choice
2. **Q3** — sets ambition
3. **Q5** — rewrite vs evolve follows from 1–3
4. **Q6** — can proceed in parallel; may be the near-term shipping path
5. **Q4, Q8, Q9** — shape the build once direction is set
6. **Q7, Q10** — design details, though Q10 may deserve promotion

---

## Things that need no decision

Settled by evidence; adopt regardless:

- Audio-first timing (v1's best idea — keep it)
- Save state after every unit, not end-of-batch
- Explicit timeout and retries on every client
- Schema-constrained structured output
- Persisted LLM exchanges
- Per-scene failure isolation
- Human review for craft
