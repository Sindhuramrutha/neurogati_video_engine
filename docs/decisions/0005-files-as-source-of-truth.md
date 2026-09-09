# ADR 0005 — Files as source of truth, SQLite as derived index

## Status

**Proposed.**

## Context

v2 needs a place to keep scene state, generated artifacts, review history, and run
metadata. The obvious modern default is a database with artifacts on disk and
metadata in tables.

That default was proposed and rejected on review. Three arguments against it:

**The payload is already files.** Audio, video, generated scene code, transcripts,
subtitles. Putting their metadata in a database while the bytes live on disk splits
truth across two systems that can drift apart — a file deleted, a row orphaned.

**v1's file layout was not the failure.** The failure was save *cadence* — one
write after an entire batch rather than one per scene
([ADR 0003](0003-durable-incremental-state.md)). Storage medium was never
implicated. The layout demonstrably works: the full 253-scene corpus was indexed by
globbing `state.json` files, with no tooling and no schema.

**Inspectability matters disproportionately here.** The system's output is reviewed
by eye, and debugging a bad scene means reading its brief, its IR, its generated
code, and its render log together. `cd` into a chapter and all of it is visible.
A database makes that a query-writing exercise.

Against this, four needs genuinely favour a database: concurrent job state,
cross-project queries, a high-volume append-only exchange log, and aggregatable
review annotations.

## Decision

**Files are the source of truth. SQLite is a derived index and an operational log.**

Layout in [data-layout.md](../design/data-layout.md). Specifically:

1. **All pipeline artifacts and state live as files** under
   `projects/<project>/chapters/<chapter>/`, one directory per stage.
2. **A `manifest.json` records content hashes** per scene per stage, making
   staleness computable rather than guessed — `make` semantics for the pipeline.
3. **SQLite holds four things**, none of them source of truth: job/run state
   (needs transactions), a corpus index (cross-project queries), an LLM exchange
   index (the files remain the record), and review annotations.
4. **The invariant: deleting `.index/` loses nothing.** Everything rebuilds from
   files. This is worth an actual test — build, delete, rebuild, assert
   equivalence.

## Consequences

**Positive**

- One place to look when debugging; no drift between rows and bytes
- Portable by copy; no migrations
- Text layers (IR, config, scripts) are git-diffable — an IR diff is a readable
  answer to "what changed?"
- Content hashing enables incremental rebuild and *verified* resume, neither of
  which v1 can do
- Concurrency and querying still available where they are actually needed

**Negative**

- Cross-project queries require the index to be built and kept current
- No referential integrity; consistency is the code's responsibility
- Many small files per chapter — fine locally, worth revisiting if this ever moves
  to object storage
- Two mechanisms to understand rather than one

**Explicitly not chosen**

Postgres. It would be the right answer for a multi-tenant hosted product, which is
a decision downstream of [Q4](../open-questions.md#q4--who-operates-this). Adopting
it now would pay that cost before the requirement exists.

## Revisit if

[Q4](../open-questions.md#q4--who-operates-this) resolves to a hosted multi-user
service, where concurrent access from multiple operators and per-user permissions
change the calculus. Note that even then, artifacts likely stay in object storage
with the database holding metadata — a variation on this decision rather than a
reversal.
