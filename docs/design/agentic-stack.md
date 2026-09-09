# Agentic Stack

A survey of frameworks, libraries, and techniques worth evaluating — with an
opinion about which problems actually need them.

> **Verify before adopting.** Versions and capabilities move fast; treat specific
> claims here as prompts to check current documentation, not settled fact.

---

## First: does this need agents at all?

Worth resisting the pull. Much of v1's pipeline is a **fixed sequence of
transformations** — script, audio, prompts, code, render, compose. There is no
planning, no dynamic tool selection, no open-ended goal. A DAG runs it fine, and
v1 already has one (LangGraph, largely unused).

Agentic patterns earn their cost where there is **genuine iteration against
feedback**:

- Building a scene incrementally while measuring
  ([Option B](architecture-options.md#option-b--agent-with-measuring-tools))
- Diagnosing a failure and choosing a repair strategy
- Deciding whether a rendered result is acceptable

**Default to a pipeline; introduce agency only where feedback loops are real.** An
agent framework wrapped around a linear sequence adds indirection and removes
determinism for nothing.

---

## Orchestration

**LangGraph** — already a dependency. Graph-structured state machines with
checkpointing and interrupts. v1 uses it in `workflow.py` but the CLI drivers
bypass it entirely, so it is effectively dead code today.

*Fit:* strong if you want durable, resumable, human-in-the-loop execution. Its
checkpointer directly addresses v1's "save after every unit" lesson. Worth either
committing to properly or removing — the current half-adoption is the worst state.

**Temporal / Prefect / Dagster** — general durable workflow engines. Retries,
persistence, observability, scheduling as first-class concerns.

*Fit:* well matched to long multi-stage jobs over many chapters. Heavier
operationally. Worth considering if you move to a
[service model](interfaces.md#4-service--queue).

**Plain Python + a state file** — what `run_chapter.py` actually does, and it
works.

*Fit:* do not underrate this. v1's real failure was saving at the wrong cadence,
not lacking a framework. Fixing the cadence is a one-line change; adopting an
engine is a project.

**Recommendation:** fix state persistence first. Adopt an engine only when
parallelism or multi-machine execution forces it.

---

## Structured output

The single highest-leverage category for [Option C](architecture-options.md).

**Pydantic + native structured outputs.** Most providers now support
schema-constrained generation (JSON schema / tool-calling). Combined with Pydantic
models, malformed output stops being a failure mode.

*Directly relevant:* v1's `scene_script.py` retries up to 3 times on JSON parse
failure — a workaround for unconstrained generation. Schema-constrained output
removes the need.

**Instructor** — wraps clients to return validated Pydantic models, with retries on
validation failure. Mature, small, provider-agnostic.

**Outlines / Guidance** — grammar-constrained decoding. Guarantees structural
validity at the token level. Strongest guarantees; typically needs model-side
support.

**Recommendation:** whatever architecture you choose, **make the model's output a
validated schema rather than free text.** This is the cheapest large win
available, and it is the mechanism that makes a typed IR viable.

---

## Tool calling

For [Option B](architecture-options.md#option-b--agent-with-measuring-tools), tools
*are* the API — the model cannot invent `gap_length` if the signature is the
contract.

**Native provider tool calling** — sufficient for most cases; no framework needed.

**MCP (Model Context Protocol)** — standardises tool servers across clients. A
`scene-builder` MCP server exposing `place`, `measure`, `connect` would be usable
from your pipeline, from Claude Code during development, and from any MCP client.

*Interesting property:* the same tools that build scenes in production could let
you author or debug a scene conversationally.

**Recommendation:** design the tool vocabulary carefully — it is the real work.
The transport (native vs MCP) is secondary and swappable.

---

## Vision and verification

For [Option A](architecture-options.md#option-a--codegen-with-visual-verification).

**Cheap programmatic checks first.** Bounding boxes via Manim introspection, pixel
statistics, blank-frame detection, contrast arithmetic, OCR (`tesseract`,
`easyocr`) to verify on-screen text against source. These are fast, deterministic,
and unit-testable — and would catch most of v1's observed defects without a model.

**Vision models** for what those cannot judge: legibility, visual clutter, whether
a diagram reads clearly. Use sparingly — sample scenes rather than checking every
one.

**Recommendation:** exhaust the cheap checks before reaching for a VLM. v1's
repeated "cut off at the edge" revisions are pure bounding-box arithmetic — no
model required.

---

## Evaluation

Currently absent, and the reason "is v2 better?" cannot be answered.

**Promptfoo / DeepEval / Ragas** — prompt and pipeline evaluation harnesses.
**LLM-as-judge** — for Tier 2 properties like source fidelity.
**Golden datasets** — you have 253 scenes. That is a corpus.

**Recommendation:** build a small eval set from real chapters before rewriting.
Without a baseline, the rewrite's success is a matter of opinion. See
[../fundamentals/quality-model.md](../fundamentals/quality-model.md).

---

## Observability

**Langfuse** — open-source, self-hostable LLM tracing. Prompts, responses, tokens,
cost, latency.
**LangSmith** — hosted; tight LangGraph integration.
**W&B Weave** — strong for experiment comparison.
**OpenTelemetry** — vendor-neutral; heavier to set up.

**Recommendation:** adopt something. Persisting every prompt/response pair with
token counts is the foundation for prompt improvement, eval sets, cost control, and
debugging. v1 kept none of it.

---

## Media and rendering

**Manim** — see [beyond-manim.md](beyond-manim.md).
**Playwright / Puppeteer** — headless capture for a web-native target; also useful
for automated visual verification.
**Remotion** — React components as video, with a real preview environment. Worth
a look if the web target appeals; its programmatic-composition model maps closely
to the typed-IR idea.
**Motion Canvas** — TypeScript animation with a live editor; procedural like Manim
but with instant preview.
**cairosvg** — already a dependency; SVG rasterisation.

**Speech:** Kokoro (current, local, free) is decent. Hosted alternatives —
ElevenLabs, OpenAI TTS, Cartesia — offer better prosody at a per-character cost.
Narration quality materially affects perceived production value, so this is worth
an explicit comparison rather than inheriting v1's choice by default.

**Alignment:** v1 uses Whisper ASR, which transcribes rather than aligns. **WhisperX
or a true forced aligner** would give more reliable timings — and since word
timings drive both beats and subtitles, this is load-bearing infrastructure. v1's
own docstring flags the limitation.

---

## Models

Notes rather than recommendations — this moves quickly.

- **Code generation** benefits most from strong reasoning. If you keep codegen,
  this is where quality matters.
- **Structured/IR output** is easier; a smaller fast model may suffice, especially
  with schema constraints.
- **Vision** for verification: check current cost per image before designing a
  loop around it.
- **Routing** (TokenRouter, OpenRouter) gives flexibility, but note the caveat
  found in v1's setup: routers gate models behind different protocols, and only
  `openai`-compatible endpoints work with an OpenAI-SDK client. Anthropic and
  Gemini models were unreachable without an adapter.

**Recommendation:** keep the v1 property of routing every call through one module
with configurable endpoints. It made provider swaps a config change, and it is
worth preserving verbatim.

---

## What to adopt regardless

Independent of architecture:

1. **Schema-constrained structured output** — removes a whole failure class
2. **Persisted LLM exchanges** — foundation for everything else
3. **Explicit transport config** — timeout and retries; v1 has neither
4. **An eval set from the 253-scene corpus** — a baseline to measure against
5. **Cheap programmatic verification** — before any vision model

Each is small, independent of the big architectural decision, and each addresses a
documented v1 failure.
