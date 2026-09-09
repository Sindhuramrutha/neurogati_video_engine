# Architecture Options

Five viable shapes for v2. None is obviously correct; each buys different
guarantees at a different price. They are presented with tradeoffs rather than a
verdict because the choice depends on answers you have not yet committed to — see
[../open-questions.md](../open-questions.md).

**The axis that separates them:** how much freedom the language model has, and
where correctness is enforced.

```
  more model freedom  ◄──────────────────────────────►  more structure
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  A       │  │  B       │  │  C       │  │  D       │  │  E       │
  │ codegen  │  │ agent +  │  │ typed IR │  │ component│  │ deck-    │
  │ + vision │  │ tools    │  │ + layout │  │ library  │  │ first    │
  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
   v1 + eyes    measure as    compiler       fixed          human made
                you build      model        vocabulary      the visual
```

---

## Option A — Codegen with visual verification

Keep v1's generator; add the eyes it never had. Render, analyse frames, feed
concrete defects back.

```
brief → code → render → frame analysis ──► defects? ──► regenerate with evidence
                             │                              ▲
                             └──────────── clean ───────────┘
```

Analysis can be programmatic (bounding boxes via Manim introspection, pixel
checks, OCR) or a vision model, or both — cheap checks first, VLM only for what
they miss.

**Buys:** closes the exact blind spot behind v1's most-repeated revisions.
Smallest conceptual change; the existing prompt and corpus stay valuable.

**Costs:** a render per iteration, now at 1080p. Retains every other failure mode —
invented APIs, timing arithmetic, unbounded output space. Fixes detection, not
representation.

**Honest framing:** this is v1 plus feedback. If v1's architecture is sound and it
was only blind, this is the efficient answer. If the problem is the architecture,
this is a better patch on the same foundation.

> Note: v1 removed vision critique for cost, and because a human re-checked it
> anyway. Reintroducing it is only different if it targets *mechanical* defects
> (clipping, overlap) rather than aesthetic judgment. That distinction is the
> whole argument — see
> v1 ADR 0002, `docs/architecture/decisions/0002-human-review-over-vision-critique.md`
> in the v1 repository.

---

## Option B — Agent with measuring tools

The model does not emit a file. It calls tools that build the scene incrementally
and return real measurements.

```python
box = place(Text("−70 mV"), at="left-of", target=membrane)
# → {"x": -3.2, "y": 1.1, "w": 2.4, "h": 0.6, "fits": true, "collides": []}
```

Every tool validates arguments and reports actual geometry. The model cannot
invent a kwarg — the tool signature is the API. It cannot place something
off-frame without being told so immediately.

**Buys:** feedback at the granularity of a single action rather than a whole
scene. Invalid API calls impossible. Naturally supports "measure, then decide."

**Costs:** many round-trips per scene (latency, tokens). Requires designing a tool
vocabulary — which is the component-library problem wearing different clothes.
Agent loops are harder to make deterministic and to test.

**Where it shines:** scenes needing genuine spatial reasoning, where the model
benefits from knowing what it just built.

---

## Option C — Typed IR + layout engine

The model emits a validated data structure, never code. A deterministic engine
turns it into a scene.

```json
{"layout": "split-horizontal",
 "left":  {"type": "diagram", "nodes": [...], "edges": [...]},
 "right": {"type": "callout", "value": "−70 mV", "emphasis": "high"},
 "beats": [{"at": 0.0, "action": "reveal", "target": "left"},
           {"at": 4.2, "action": "emphasise", "target": "right"}]}
```

Schema validation rejects malformed output before anything renders. The layout
engine — flexbox-like, or a constraint solver — computes positions and *guarantees*
fitting. Beat timestamps come from word timings; durations are computed, never
summed by the model.

**Buys:** Failures 1, 2 and 3 from the [post-mortem](../diagnosis/v1-postmortem.md)
become unrepresentable. The IR is snapshot-testable and diffable — real regression
testing becomes possible. Retargetable: the same IR could render to Manim, SVG, or
a web player.

**Costs:** you must build the layout engine and design the schema. Expressiveness
is bounded by the schema — anything unanticipated needs a schema change. Risk of
an escape hatch (`{"type": "raw_manim"}`) that quietly becomes the default path.

**The core bet:** that a schema rich enough for your content is designable. This is
the vocabulary question, and the 253-scene corpus can answer it empirically.

---

## Option D — Component library

Sharper form of C: a fixed catalogue of parameterised scene types, each
hand-built, tested, and known-good. The model selects and populates.

```
ConceptIntroduction  ProcessFlow  Comparison  LabelledDiagram
DataPlot             CodeWalkthrough          Timeline
```

**Buys:** the strongest guarantees available. Each component is real code, tested
once, correct forever. Visual consistency by construction. Fastest generation —
selection is a small output. Cheapest to verify.

**Costs:** a hard ceiling. Anything outside the catalogue is impossible until
someone builds it. Risks a homogeneous look. Requires knowing your content shapes
in advance.

**When this is right:** if sampling the corpus shows most scenes are variations on
a dozen forms. **When it is wrong:** if the tail is long and matters — you will
spend the project fighting the ceiling.

---

## Option E — Deck-first

Invert the problem. A human authors the slide; the pipeline adds narration,
timing, highlights, and motion. `pptx_deck_pipeline.py` already does this.

**Buys:** Tier 1 quality is *free* — a human made the layout, so nothing is
off-frame or overlapping. Eliminates the hardest problem entirely. You have 12
Demystifying the Brain decks ready. `highlight_planner.py` demonstrates the
grounding pattern working.

**Costs:** requires authored decks — human effort moves upstream rather than
disappearing. Visuals are static slides plus overlays, not built animation. Does
not solve prose-to-video at all.

**Strategic value:** this is the one option that can ship reliably *now*, and it
is orthogonal to the others. It could be the production path while a more ambitious
generator is developed behind it.

---

## Comparison

| | A: vision | B: agent | C: typed IR | D: components | E: deck |
|---|---|---|---|---|---|
| Off-frame impossible | no (detected) | no (detected fast) | **yes** | **yes** | **yes** |
| Invalid API impossible | no | **yes** | **yes** | **yes** | **yes** |
| Timing structural | no | partly | **yes** | **yes** | **yes** |
| Expressiveness | **high** | **high** | medium | low | low |
| Regression testable | weak | weak | **strong** | **strong** | **strong** |
| Build cost | low | medium | **high** | **high** | done |
| Cost per scene | high | high | **low** | **lowest** | low |
| Reuses v1 work | most | some | little | little | all |

---

## Hybrids worth considering

The options compose, and the strongest designs probably do.

**C with a repair pass (C+A).** Typed IR and layout engine for structure; render
and verify as a safety net for what layout cannot predict (visual density,
legibility). Structure for the predictable, feedback for the emergent.

**D with a C escape hatch.** Components for the common cases; typed IR for the
tail. Only viable with a firm rule about when the escape is permitted — otherwise
it becomes the default and you have built C with extra steps.

**B to discover D.** Build the tool-calling agent first, log every tool sequence,
and let recurring patterns reveal the component vocabulary empirically. Uses the
flexible design as research for the constrained one.

**E as the production track, C as the ambition.** Ship deck-first now; develop the
generator without schedule pressure. The two share TTS, alignment, compose, and
stitch — most of v1's deterministic layer is reusable by both.

---

## Things any option should keep

Independent of the choice, these are settled:

1. **Audio-first timing.** v1's best idea. Word timings drive beats and subtitles.
2. **Per-scene isolation.** One failure never kills a batch.
3. **Save after every unit.** Not end-of-batch — v1's own newer code calls this
   "a hard lesson."
4. **Explicit transport config.** Timeout and retries on every client.
5. **Human review for craft.** Preserve the checkpoint; free it from mechanical
   defects.
6. **Introspected API truth.** Never hand-write what can be derived from the
   installed package.

---

## Deciding

The choice hinges on questions in [../open-questions.md](../open-questions.md),
most importantly:

- **Is your content a bounded vocabulary?** Answerable today by sampling the 253
  existing scenes. This single answer separates {C, D} from {A, B}.
- **What is the quality target?** "Fewer revisions" and "unattended production"
  justify very different investments.
- **What is the time horizon?** A is weeks; C or D is months.
- **Is Manim the right target at all?** See
  [beyond-manim.md](beyond-manim.md) — worth resolving before building a layout
  engine on top of it.
