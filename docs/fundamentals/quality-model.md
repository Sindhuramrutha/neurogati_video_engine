# Quality Model

v1 has no definition of "good." It has a human who looks at clips and a duration
check. Everything else is unmeasured.

This matters more than it sounds. **You cannot automate what you have not
defined**, and you cannot tell whether a rewrite improved anything without a
baseline. Before building v2, decide what "correct" means and how each property is
checked.

---

## Three tiers

Not all quality is the same kind of thing. Conflating them is why v1's system
prompt tries to legislate taste.

### Tier 1 — Mechanical correctness

Objectively checkable. No judgment. Should be **impossible to violate**, or failing
that, automatically detected.

| Property | Check |
|---|---|
| All elements within frame bounds | Measure bounding boxes post-construction |
| No unintended overlap | Pairwise box intersection |
| Duration matches narration (±tolerance) | `ffprobe` compare |
| Valid API usage | Signature validation / type system |
| Text legible at output resolution | Min font size after scaling |
| Contrast meets threshold | Computed luminance ratio |
| No element fully occluded | Z-order + box analysis |

**v1 checks two of seven** (duration; a fixed regex list for some API misuse).
Everything else is a prompt rule and a human's eyes.

These are the rows to attack first. Each one moved from "human notices" to
"cannot happen" is a permanent reduction in review cost across every future scene.

### Tier 2 — Pedagogical soundness

Requires understanding the content. Some of it is automatable; most needs judgment.

| Property | Feasible check |
|---|---|
| Every narration claim traceable to source | LLM-as-judge against source text |
| No fabricated numbers/labels | Extract on-screen strings, verify against source |
| Visual matches what narration says *now* | Beat-to-timestamp alignment check |
| Concepts introduced before use | Dependency ordering over the scene graph |
| Visual metaphor is apt | Human |

The second row is worth highlighting: **fabricated on-screen data is the most
dangerous defect this system can produce**, because it is authoritative-looking and
silent. v1 addresses it with prompt rules in three places. A structural check —
extract every string rendered on screen, verify each against the source document —
is mechanical and currently absent.

### Tier 3 — Craft

Rhythm, elegance, whether it feels like one coherent course. Human. Do not
automate; v1 was right about this.

The goal of Tiers 1 and 2 is to **make Tier 3 the only thing a reviewer spends
attention on.** Today a human catches clipped text — a Tier 1 defect — which is
attention stolen from craft.

---

## The verification question

The deep question: **how does the system know a scene is correct before a human
sees it?**

Four postures, not mutually exclusive:

**Correct by construction.** Invalid states unrepresentable. A layout engine
cannot place something off-frame; a typed IR cannot express an invalid API call.
Strongest guarantee, costs expressiveness.

**Verified after construction.** Generate freely, then measure the artifact —
bounding boxes, durations, contrast — and reject or repair. Keeps expressiveness,
needs the artifact to be inspectable.

**Verified after rendering.** Render, then analyse frames — programmatically
(pixel analysis, OCR) or with a vision model. Catches everything including
emergent problems, costs a render per check.

**Verified by human.** The v1 default. Should be reserved for Tier 3.

A plausible target: construction for layout and API validity, post-construction
measurement for timing and occupancy, rendered checks sampled rather than
per-scene, human for craft.

---

## Cheap checks worth having regardless

Independent of architecture, these are inexpensive and would have caught real v1
failures:

- **Frame-bounds assertion** after building a scene — catches every "cut off at
  the edge" revision in the shell history.
- **Signature validation** against the introspected API — catches `gap_length`
  before rendering, using machinery `manim_reference.py` already has.
- **Rendered-string extraction** — collect every `Text`/label string, diff against
  the source document, flag anything unattested. Catches fabricated data.
- **Contrast and min-font-size** — pure arithmetic over the built scene.
- **First/last frame sampling** — a blank or near-blank frame is a strong signal
  something failed silently.

None require a vision model. All are unit-testable.

---

## Regression testing

v1 has no tests. For a system whose output is a video, that seems hard — but most
of what matters is not pixels.

**Golden IR.** If generation produces a structured intermediate representation,
snapshot it. Diffs are readable and reviewable in a way generated Python is not.
This is a strong argument for having an IR at all.

**Property tests.** For any scene: nothing off-frame, durations sum correctly, no
overlap. Assert over generated output rather than fixed expectations — these hold
for *every* scene, so they can run against all 253 existing ones.

**Perceptual diffs.** Render fixed seeds, compare frame hashes. Catches
regressions from dependency upgrades — exactly the class of failure
v1 ADR 0003 (`docs/architecture/decisions/0003-pinned-manim-version.md` in the
v1 repository)
pinned Manim to avoid.

**The 253-scene corpus is an asset.** It is a ready-made regression suite and the
evidence base for the vocabulary question in
[what-this-system-is.md](what-this-system-is.md). Running v2 over the same inputs
and diffing outcomes is the most direct measure of whether the rewrite worked.

---

## Metrics worth tracking

To know whether v2 is better, instrument what v1 never did:

| Metric | Why |
|---|---|
| Scenes needing human revision (%) | The headline number |
| Revisions per scene (mean) | Review burden |
| Failure counts by class | Which defects survive |
| Time to first watchable output | Iteration speed |
| Cost per finished minute | Economics |
| Automated checks caught vs human-caught | Whether verification is working |

The last row is the one that tells you if the rewrite achieved its purpose. In v1
it is effectively 0% — every defect in the shell history was human-caught.

---

## Setting a target

Worth deciding explicitly, because it determines how much machinery is justified:

- **"Most scenes need no revision"** — modest ambition, achievable by fixing Tier 1.
- **"Human reviews for craft only"** — requires Tier 1 fully structural and Tier 2
  largely automated.
- **"Fully unattended for a defined content class"** — requires confident Tier 2
  verification, and is realistic only for narrow, well-specified inputs (a slide
  deck, say — where the visual is already authored).

The third is where the PPTX path is interesting: with a human-made slide as the
visual, Tier 1 is trivially satisfied and the remaining risk is narration and
highlight placement.
