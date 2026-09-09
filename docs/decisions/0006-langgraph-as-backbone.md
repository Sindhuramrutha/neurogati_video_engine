# ADR 0006 — LangGraph as the orchestration backbone

## Status

**Proposed.**

## Context

v1 depends on LangGraph and does not use it. `workflow.py` builds a compiled graph
with a checkpointer and interrupts; `run_chapter.py` — the driver actually used in
production for all 253 scenes — bypasses it entirely and reimplements staging with
plain functions and a JSON file.

That is the worst available state: the dependency is paid for, the capability is
absent, and the reimplementation carries the bugs the framework would have
prevented (batch-level saves, no resume verification, sequential execution).

Meanwhile the scene pipeline is genuinely a cyclic graph, not a linear sequence:

```
build IR ──► validate ──► render ──► check ──✓──► done
    ▲                                   │
    └───────────── feedback ◄───────────✗
```

v1 implements that cycle as a hand-written `for attempt in range(1, MAX+1)` loop
inside `_run_render_loop`, with feedback threaded through local variables.

Four open items independently point at the same set of features:

- [ADR 0003](0003-durable-incremental-state.md) wants persistence after every unit
- [Q8](../open-questions.md#q8--where-does-human-judgment-enter) wants human
  checkpoints at more than one stage
- [Q9](../open-questions.md#q9--batch-or-interactive) wants parallel scene
  execution
- [interfaces.md](../design/interfaces.md#observability) wants live progress
  instead of an opaque wait

## Decision

**Adopt LangGraph as the orchestration backbone, properly — not as a parallel
implementation alongside a hand-rolled driver.**

| Need | Mechanism |
|---|---|
| Durable state | **Checkpointer** — persists after every node |
| Human review points | **`interrupt`** — pause, inspect, resume |
| Parallel scenes | **Fan-out** to per-scene subgraphs |
| Retry with feedback | **Conditional edges** — first-class, not a loop |
| Live progress | **Streaming** state updates to the UI |
| Debugging | **Checkpoint history** — replay from any node |

**Structure:** a chapter-level graph that fans out to per-scene subgraphs. Each
scene subgraph owns its retry cycle, so one scene's failure or retry never blocks
another — preserving v1's per-scene isolation (which was correct) while adding the
concurrency it lacked.

**One driver.** The CLI and the API both invoke the same graph. v1's split between
`workflow.py` and `run_chapter.py` is not repeated.

### LangChain, separately and selectively

LangChain is adopted for three specific things:

- **Document loaders** — `.docx/.pdf/.md/.txt`, replacing v1's `utils/references.py`
- **Text splitters** — chapter and section chunking
- **Prompt management** — templates, few-shot examples, versioning

**It does not wrap the LLM call site.** v1's `utils/llm.py` — one module, direct
SDK, provider swap by environment variable — is good design that survived a real
provider migration as a configuration change. An abstraction layer over that adds
indirection where debugging a bad generation is already hard, and buys nothing the
current shape lacks.

## Consequences

**Positive**

- Checkpointing satisfies ADR 0003 natively rather than by hand
- Interrupts make multi-point human review cheap to add, addressing Q8
- Fan-out addresses Q9 — potentially an order-of-magnitude wall-clock improvement
- Streaming turns opaque runs into visible ones
- The retry cycle becomes declarative and inspectable rather than a nested loop
- Time-travel debugging: replay a chapter from any node with changed inputs

**Negative**

- Real learning curve; the graph model must be understood before it helps
- Framework lock-in at the core of the system. Mitigated by keeping node bodies as
  plain functions with no LangGraph imports — the graph wires them, it does not
  live inside them.
- Debugging a framework-managed loop is harder than a `for` loop when it goes wrong
- Version churn in a fast-moving library

**Mitigation, stated explicitly:** every node is a plain Python function taking
and returning typed state. LangGraph composes them. If the framework is later
abandoned, the node bodies survive and only the wiring is rewritten — the same
insurance the IR provides for the renderer.

## Revisit if

Node-level logic starts being written *for* the framework rather than composed by
it, or graph debugging costs more time than the orchestration saves. The escape is
cheap by construction, given the mitigation above.
