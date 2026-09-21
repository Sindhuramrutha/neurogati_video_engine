# Tech Stack

The proposed stack for v2, layer by layer, with what it replaces and why.

Every choice here is traceable to a documented v1 failure or an
[open question](../open-questions.md). Where a mainstream option was rejected,
the reason is stated — a rejected alternative is as useful as a chosen one.

---

## The shape

One decision determines the rest: **a Python core and a TypeScript renderer,
separated by a JSON IR.**

```
┌──────────────────── Python 3.12 ────────────────────┐   ┌─── TypeScript ───┐
│                                                     │   │                  │
│  ingestion    LangChain loaders                     │   │   Revideo        │
│  comprehension LLM + structured output              │   │   renderVideo()  │
│  narration    Kokoro TTS + WhisperX alignment       │──►│                  │
│  IR build     Pydantic v2                           │IR │   <Player/>      │
│  orchestration LangGraph (checkpoints, interrupts)  │   │   browser preview│
│  API          Litestar                              │   │                  │
│                                                     │   │                  │
└─────────────────────────────────────────────────────┘   └──────────────────┘
         ▲                                                          │
         └──────── files on disk = source of truth ◄────────────────┘
```

The IR is a **process boundary**, not a convention. Logic cannot leak across it
by accident, which is exactly the separation
[interfaces.md](interfaces.md#the-rule-that-keeps-all-of-this-cheap) argues for —
here it is enforced by the architecture rather than by discipline.

---

## Orchestration — LangGraph, as the backbone

**This is the centre of the system, not a utility.**

v1 already depends on LangGraph and does not use it: `run_chapter.py` bypasses
`workflow.py` entirely. That is the worst of both — paying the dependency, getting
none of the value.

The scene pipeline is genuinely a cyclic graph:

```
build IR ──► validate ──► render ──► check ──✓──► done
    ▲                                   │
    └───────────── feedback ◄───────────✗
```

Committing to LangGraph resolves four open items at once:

| Problem | LangGraph mechanism |
|---|---|
| [ADR 0003](../decisions/0003-durable-incremental-state.md) durable state | **Checkpointer** — persists after every node |
| [Q8](../open-questions.md#q8--where-does-human-judgment-enter) review points | **`interrupt`** — pause, inspect, resume |
| [Q9](../open-questions.md#q9--batch-or-interactive) parallelism | **Fan-out** — scenes as concurrent subgraphs |
| Retry with feedback | **Conditional edges** — first-class, not a `for` loop |
| Opaque runs | **Streaming** — live state to the UI |

Checkpoint history also gives **time-travel debugging**: replay a chapter from any
node with different inputs. v1 cannot do this at all.

**Structure:** a chapter graph that fans out to per-scene subgraphs. Each scene
subgraph owns its own retry cycle, so one scene's loop never blocks another's —
preserving v1's per-scene isolation while adding real concurrency.

## LLM layer — LangChain, selectively

LangChain earns a place in three specific spots:

- **Document loaders** — `.docx/.pdf/.md/.txt` ingestion, replacing v1's
  hand-rolled `utils/references.py`
- **Text splitters** — chapter and section chunking
- **Prompt management** — templates, few-shot examples, versioning

**It does not wrap the LLM call site.** v1's `utils/llm.py` — one module, direct
SDK, provider swap by environment variable — is good design that survived a real
provider migration as a config change. Routing every call through an abstraction
layer adds indirection over something already working, and makes debugging a bad
generation harder.

**Structured output is mandatory** ([ADR 0002](../decisions/0002-structured-output-over-free-text.md)):
Pydantic models + provider-native constrained generation, with **Instructor** as
the retry-on-validation-failure wrapper. This is what makes the IR viable.

---

## Rendering — Revideo

TypeScript, **MIT licensed**, ~4k stars, actively maintained. A fork of Motion
Canvas — which was built specifically for explanatory/educational video — extended
with a rendering API and template system aimed at automated pipelines.

It structurally eliminates v1's four documented failures:

| v1 failure | Revideo |
|---|---|
| "cut off at any edge" | CSS-style layout — a solved problem |
| "55.6s but narration is 52.3s" | Duration **declared**; content is `f(t)`. Unrepresentable. |
| `gap_length` invented | Typed IR consumed by real components; no arbitrary codegen |
| Review takes minutes per look | `<Player/>` renders in-browser — preview without rendering |

It also ships **parallelised rendering across workers**, and frame-accurate audio
sync — which composes directly with
[ADR 0001](../decisions/0001-preserve-audio-first-timing.md).

### Rejected: Remotion

Same model, better known, larger ecosystem. Rejected on licensing: free only for
individuals and companies **up to three people**; beyond that a Company License at
**$0.01/render, $100/month minimum**. Not ruinous, but it is a commercial
dependency at the core of the system where an MIT-licensed equivalent exists.

### Rejected (as default): Manim

Kept as a possible specialist renderer, not the default. Its animation model is
genuinely strong for the ~20% of the corpus that is physical simulation. But
duration is emergent rather than declared, layout is imperative and unmeasurable
before construction, and rendering is slow — the three properties behind v1's
worst failures.

> **This choice is gated on a test, not an argument.** Port one
> `physical-system` scene from the existing corpus to Revideo before committing.
> See [ADR 0007](../decisions/0007-revideo-as-rendering-target.md).

---

## Storage — files, with SQLite where it earns it

**Files are the source of truth. SQLite is a derived index and operational log.**

Full layout and rationale in [data-layout.md](data-layout.md). The short version:

- Pipeline artifacts *are* files — audio, video, code, transcripts. Keeping their
  metadata elsewhere splits truth across two systems for no gain.
- v1's file layout was not the bug. The bug was save **cadence**. Storage medium
  was never the problem.
- Files are inspectable with `cd` and `cat`, diffable, portable by copy, and need
  no migrations.

SQLite handles four things, none of them source of truth:

| Store | Why not a file |
|---|---|
| LLM exchange log | High volume, append-only, needs querying |
| Job / run state | Concurrent workers need transactions |
| Corpus index | Cross-project queries |
| Review annotations | Queryable, aggregatable |

**Invariant:** delete `.index/` entirely and it rebuilds from files.

---

## Backend — Litestar

An upgrade over FastAPI without a conceptual change:

- **Real dependency injection** — matters when wiring LangGraph, storage, and renderers together
- **Channels** — first-class pub/sub for websockets, which is exactly what streaming LangGraph state to the UI needs
- **DTOs and layered structure** — less ad-hoc as the app grows
- **Faster**, with less runtime magic

FastAPI remains a perfectly valid choice and the app I already built uses it; the
migration is mechanical if you prefer to stay.

### Rejected: Django

More powerful in the batteries sense — auth, admin, permissions, migrations. That
becomes the right answer **only if
[Q4](../open-questions.md#q4--who-operates-this) lands on "the Neurovidya content
team uses this"**, where free auth and admin genuinely pay for the weight. Overkill
for a single-operator tool. Revisit when Q4 is answered.

### Rejected: Node/NestJS

Would unify the language with Revideo, but abandons the Python ML stack — Kokoro,
WhisperX, the LLM orchestration. Bad trade.

> The thing that will feel powerful is not the HTTP framework. It is **LangGraph
> streaming live state into the UI** so a running chapter is visible instead of
> opaque. That is an orchestration win, not a web-framework one.

---

## Frontend — React + Vite

React specifically **because Revideo's `<Player/>` is a React component.**
Embedding it gives live scene preview with dynamic inputs, in the review UI, with
no server render — collapsing v1's worst loop.

- **Vite** — dev server and build
- **Tailwind** — styling without a design-system project
- **TanStack Query** — server state, caching, streaming updates

SvelteKit would be a gentler learning curve, but loses the `<Player/>` embed. That
single feature is worth the extra React boilerplate.

---

## Audio

| Component | Choice | Note |
|---|---|---|
| TTS | Kokoro (keep) | Local, free, decent. Evaluate Cartesia / ElevenLabs — narration quality drives perceived production value more than any visual change. |
| Alignment | **WhisperX** | Upgrade from v1's Whisper ASR. Forced alignment against known text, not transcription. These timings drive beats *and* subtitles — load-bearing infrastructure. |
| Assembly | ffmpeg (keep) | Works. Consider **OpenTimelineIO** for the timeline representation rather than inventing one. |

---

## Packaging — uv

**Replaces conda and pip entirely**, and it is not a minor convenience. v1's
onboarding was a documented sequence of failures:

- system Python was 3.14; `kokoro` requires `>=3.10,<3.13` — a hard install error
- a `venv` cannot fix that, because it inherits whatever interpreter created it
- conda was therefore required just to *provision* an interpreter
- winget's Miniconda download failed twice with `0x80072ee7`
- newer conda then demanded Anaconda channel ToS acceptance, carrying commercial
  licensing implications, worked around with `--override-channels --channel conda-forge`

**uv provisions the interpreter itself.** `uv python install 3.12` and
`uv sync` replace that entire sequence — no conda, no channel licensing question,
no venv-inherits-the-wrong-Python trap. Lockfile-based, reproducible, and roughly
10–100× faster than pip.

```bash
uv python install 3.12
uv sync                 # creates .venv, installs from uv.lock
uv run pipeline render  # no activation step
```

The TypeScript side uses **pnpm** for the same reasons — strict, fast, lockfile-driven.

## Other tooling

| Concern | Choice | Replaces |
|---|---|---|
| Config | Pydantic Settings | v1's `config/settings.py` — same pattern, typed |
| Observability | **Langfuse** (self-hosted) | Nothing. v1 persists no exchanges at all. |
| Testing | pytest + golden IR snapshots + property tests | Nothing. v1 has no tests. |

**On observability:** LangSmith has the tightest LangGraph integration and is the
zero-config option. Langfuse is open-source and self-hostable, which keeps cost and
data control in your hands. Either is a large improvement over nothing.

**On testing:** the IR is what makes this possible. Golden snapshots of a
structured document are reviewable; snapshots of generated Python are not. Property
tests ("nothing off-frame", "durations sum correctly") can run against the entire
existing 253-scene corpus.

---

## What is reversible

Everything except the renderer.

The IR is the insurance policy: if Revideo disappoints, write a different IR
consumer and the entire Python side is untouched. That is the whole point of
putting a typed boundary there rather than calling a rendering library directly.

## Honest risks

- **Two languages, two toolchains.** A real cost. Mitigated by the boundary being
  a JSON file you rarely have to think across.
- **Revideo's bus factor.** 4k stars is healthy but smaller than Remotion's. MIT
  means forking is possible; it is still a consideration.
- **The 253-scene Manim corpus stops being directly reusable as code.** It remains
  valuable as reference, eval data, and the evidence base for
  [Q1](../open-questions.md#q1--is-your-content-a-bounded-visual-vocabulary).
- **~20% of scenes are physical simulation**, where Manim is strongest. Motion
  Canvas signals can express this, but the idiom differs from `ValueTracker`. This
  is the category the porting test must cover.

## Related decisions

- [ADR 0005 — Files as source of truth](../decisions/0005-files-as-source-of-truth.md)
- [ADR 0006 — LangGraph as orchestration backbone](../decisions/0006-langgraph-as-backbone.md)
- [ADR 0007 — Revideo as rendering target](../decisions/0007-revideo-as-rendering-target.md)
