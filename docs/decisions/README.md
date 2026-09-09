# Decision Records

Decisions for v2. Unlike v1's ADRs — written after the fact — these start as
**Proposed** and are promoted to **Accepted** when committed to.

## Statuses

- **Proposed** — argued for, not yet decided
- **Accepted** — decided; build against this
- **Superseded by ADR-NNNN** — replaced, kept for history
- **Rejected** — considered and declined, with reasons (valuable: stops the
  question being reopened without new information)

## Format

Status / Context / Decision / Consequences / Revisit if.

Never edit an accepted ADR. Write a new one and supersede.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-preserve-audio-first-timing.md) | Preserve audio-first timing | **Proposed** |
| [0002](0002-structured-output-over-free-text.md) | Structured output over free text | **Proposed** |
| [0003](0003-durable-incremental-state.md) | Durable incremental state | **Proposed** |
| [0004](0004-mechanical-checks-before-human-review.md) | Mechanical checks before human review | **Proposed** |
| [0005](0005-files-as-source-of-truth.md) | Files as source of truth, SQLite as derived index | **Proposed** |
| [0006](0006-langgraph-as-backbone.md) | LangGraph as the orchestration backbone | **Proposed** |
| [0007](0007-revideo-as-rendering-target.md) | Revideo as the rendering target | **Proposed — gated on a porting test** |

## Reading order

0001–0004 are independent of the architecture choice; each addresses a documented
v1 failure and holds regardless of direction.

0005–0007 are the stack decisions. They depend on each other:

- **0007** (renderer) is the load-bearing one, and the only one deliberately gated
  on evidence rather than argument
- **0006** (LangGraph) is independent of it
- **0005** (files) is independent of both

## Still to write

Awaiting answers in [../open-questions.md](../open-questions.md):

- Scene authoring architecture (Q1) — the central choice
- Interface strategy (Q4) — determines Litestar vs Django, local vs hosted
- Deck-first path's role (Q6)
- Fabrication guarantee (Q10)
