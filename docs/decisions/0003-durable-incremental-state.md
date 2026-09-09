# ADR 0003 — Durable incremental state

## Status

**Proposed.**

## Context

`run_chapter.py` calls `save_scenes()` **once, after the entire render loop**
(line 277). A 22-scene chapter failing at scene 20 persists nothing from the 20
scenes already rendered.

This is not inferred. v1's own newer code states it as settled fact —
`pptx_deck_pipeline.py`:

> *State is saved after every single slide, not once at the end of the whole run —
> a hard lesson from the regular chapter pipeline, where a single end-of-batch save
> meant an interrupted run could lose every already-rendered scene's progress. That
> mistake isn't repeated here.*

The lesson was learned and applied to the new component. The original was never
fixed.

A related transport problem compounds it: `utils/llm.py` constructs `OpenAI()`
with no `timeout` and no `max_retries` (verified — neither appears in the file). A
dropped connection surfaces as `Connection error.`, marking the scene failed with
**no code generated** — `render_attempts=0`. In one observed run this killed 3 of 4
scenes.

That failure shape also creates an operator trap: with no code, `--revise` cannot
help (it regenerates *from* existing code). The correct command is `--stage render`.
The CLI does not distinguish the cases, and the error message does not say.

## Decision

**Persist after every atomic unit of work, and configure transport explicitly.**

1. **Save after each scene**, not after each batch. A unit of work that succeeded
   is never lost to a later failure.
2. **Explicit timeout and retries** on every client:
   ```python
   OpenAI(base_url=..., api_key=..., timeout=600.0, max_retries=3)
   ```
   Long enough for a genuine large completion (these legitimately take 1–4
   minutes); retries so a transport blip self-heals instead of destroying work.
3. **Distinguish failure kinds in state.** "Failed before producing output" and
   "produced output that failed validation" need different recovery, and the system
   should say which occurred and what to run next.
4. **Make resume the default.** Re-running should continue, not restart.

## Consequences

**Positive**

- Interruption costs one unit, not a batch
- Transport blips retry instead of failing a scene
- Operators get an actionable next step rather than a misleading one
- Long chapters (22 scenes observed) become safe to run unattended

**Negative**

- More frequent writes — negligible against render cost
- Retries can mask a genuinely degraded endpoint; log retry counts so this is
  visible
- Distinguishing failure kinds requires a richer state model than v1's single
  `render_status`

**Implementation note**

If [LangGraph](../design/agentic-stack.md#orchestration) is adopted properly, its
checkpointer provides this. v1 has LangGraph as a dependency but the CLI drivers
bypass it — so the capability was present and unused. Either commit to it or
implement persistence directly; the current half-adoption is the worst option.

## Revisit if

Execution moves to a distributed or multi-machine model, where a shared durable
store replaces per-chapter JSON files.
