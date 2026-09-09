# System Map — boundaries, contracts, invariants

What crosses which boundary, what each side promises, and what happens when a
promise is broken.

This exists because the failure mode that matters is not "the code is wrong" — it
is "the code is fine but two modules disagreed about who validates what." That
disagreement is only visible when the contracts are written down.

---

## Boundaries

Every failure originates at one of these.

```
   browser ──① HTTP ──► Litestar ──② calls ──► domain modules
      │                                             │
   ①b its own state                          ③ filesystem
                                           (source of truth)
```

### ① Browser → HTTP

**Contract:** `requestJsonFromApi` in
[shared-client.js](../../src/pipeline/web/static/shared-client.js) is the only
sanctioned way for a page to reach the API. It returns parsed JSON (or `null` for
204), or it throws `ApiRequestFailed`. It never returns a partial value.

That "never partial" clause is the point: a caller must not be able to mistake a
failure for data. An earlier page made raw `fetch` calls and checked none of them,
so a failed POST advanced the UI exactly as a successful one did — the write was
lost silently.

| Failure | User sees | Developer sees | Recoverable |
|---|---|---|---|
| Server unreachable | "Could not reach the server. Is it still running?" | `console.error` + `isNetworkFailure: true` | Retry button |
| Offline | "You appear to be offline." | same, `navigator.onLine` checked | Retry button |
| 4xx / 5xx | the API's `detail` field | `statusCode` on the error | Depends on the route |
| 200 with malformed JSON | "The server returned a malformed response." | named explicitly | No — server bug |

**Invariant:** no module may call `fetch` directly. Enforced by
`tests/test_frontend_contracts.js`, not by inspection.

### ①b Browser → its own state

A second boundary inside the browser, promoted to one here because ignoring it
produced the worst defect found so far.

**Contract:** everything scoped to a project lives in
`PROJECT_SCOPED_STATE_DEFAULTS` in
[ui-kit.js](../../src/pipeline/web/static/ui-kit.js), and switching project calls
`clearProjectScopedState()` — which resets *every* field, because it is derived
from that one object rather than written out by hand.

**Why it exists:** selecting a different project used to leave the previous
project's plan, script, composition and review in memory while `projectApiPath`
already resolved to the new slug. Editing anything then wrote one project's
document into another project's file. Silent, immediate, unrecoverable.

**Second guard, belt and braces:** every save captures the project slug before it
starts and discards the response if the slug changed while it was in flight. A
network round-trip is long enough for a user to switch projects.

| Invariant | Enforced by |
|---|---|
| Every project-scoped field is cleared on switch | `test_frontend_contracts.js` |
| Every save verifies the project mid-request | `test_frontend_contracts.js` |
| One optimistic-save implementation, not four | `test_frontend_contracts.js` |
| No in-flight guard silently drops a user action | `test_frontend_contracts.js` |

That last one is a character requirement as much as a correctness one: a button
that does nothing because a previous save is still running teaches the user that
the app is unreliable. It now says *"Still saving the last change — try again in a
moment."*

### ② HTTP → domain

**Contract:** routes are thin. They resolve a project, call one domain function,
and shape the response. No route contains pipeline logic.

Validation happens at this boundary, not deeper, so bad input fails where it
arrives rather than inside an unrelated component later.

| Input | Validated by | On rejection |
|---|---|---|
| Uploaded source file | `validate_uploaded_source_file` | Per-file reason, 201 with a `rejected` list |
| Project name | `create_project` route | 400 with a reason |
| Stage key | `Stage(...)` enum coercion | 404 |
| Stage options | the declaration in `stage_options.py` | Unknown keys dropped; invalid values fall back |
| Plan / script / composition / review | the Pydantic model for that artifact | Clamped or trimmed, never rejected |
| Agent body | none — free text by design | — |

**Partial success is a first-class outcome.** Uploading five files where one is
unsupported stores the four and reports the fifth. An all-or-nothing 500 would
tell the user nothing about which file was the problem.

**Artifacts clamp rather than reject.** A section with a 40-hour duration is
clamped and flagged in `warnings`; it is not a 400. Someone editing a plan should
never lose the rest of their edit because one number was absurd. Warnings are
advisory and never block a save — asserted by
`test_warnings_are_advisory_and_never_block_a_save`.

### ③ Domain → filesystem

**Contract:** files are the source of truth
([ADR 0005](../decisions/0005-files-as-source-of-truth.md)).

Every artifact path is derived in
[storage/layout.py](../../src/pipeline/storage/layout.py) from the `produces`
field each stage declares in [stages.py](../../src/pipeline/stages.py), so the
path shown in the UI and the path written on disk are the same string.

They were not always. Scripting advertised `scripting/scenes.json` while writing
`scripting/script.json`; Reviewing advertised `reviewing/report.json` while
writing `reviewing/review.json`. Nothing failed, because a label is only ever read
by a human. `test_every_store_writes_where_its_stage_says_it_writes` now closes it.

**Invariants:**

- **No write escapes its project directory.** Enforced in
  [sources.py](../../src/pipeline/sources.py) by reducing filenames to a bare name
  under both POSIX and Windows conventions *and* re-checking the resolved
  destination. Both, because sanitisation alone is one refactor away from being
  wrong.
- **All durable writes are atomic** — temp file then rename, in exactly one
  implementation: `write_text_atomically` in
  [storage/documents.py](../../src/pipeline/storage/documents.py). An interrupted
  write must never leave a truncated file that the reader then rejects, because
  the symptom is someone's work silently vanishing.
  `test_no_module_hand_rolls_an_atomic_write` fails the suite if a module
  reimplements it.
- **A corrupt file is never overwritten.** Every store falls back to a default,
  logs at ERROR, and leaves the file on disk for manual recovery. A corrupt
  `script.json` may hold hours of someone's writing; silently replacing it with an
  empty default is the worst possible response.
- **A failed create leaves nothing behind.** A half-built project directory would
  be invisible to `list()` but block `create()` — a wedged slug with no way to
  recover from the UI.

## What is actually on disk

Verified against the code, not aspirational:

```
projects/<slug>/
  project.json                    name, created timestamp
  sources/<uploaded file>         admitted by sources.py, nothing else
  settings/<stage>.json           per-stage option choices
  agents/<stage>/AGENT.md         project override of the shipped default
  inputs/  extraction/            created empty; extraction has no writer yet
  planning/plan.json
  scripting/script.json
  studio/composition.json
  reviewing/review.json
```

The wider layout in [data-layout.md](../design/data-layout.md) — chapters, scene
audio, an IR, render logs — is a **design for stage execution, not a description
of this repository**. That document now says so at the top. It did not before, and
the confusion had a measurable cost: `.gitignore` was written against the
fictional layout, matched nothing, and staged a demo project including an uploaded
PDF for commit.

## Data flow

```
source documents ──► extraction ──► planning ──► scripting ──► studio ──► reviewing
     (you)            content        plan        narration     timeline    comments
                                                      │                        │
                                                word timings              routed to the
                                                      │                   stage that can
                                              the timing authority           fix it
                                              for beats + subtitles
```

Three properties worth stating explicitly:

**Audio is the clock** ([ADR 0001](../decisions/0001-preserve-audio-first-timing.md)).
Word timings from measured narration drive both animation beats and subtitles, so
the two cannot drift apart. *Not built yet* — no narration is synthesised.

**Feedback flows backwards, and targets a stage.** "The pacing is frantic" is a
Scripting defect, not a Studio one, and fixing it in Studio treats the symptom.
This one *is* built: `Comment.routed_to_stage`, and `Review.comments_by_stage()`
gives the count that tells an operator where to go next — six comments routed to
Scripting means the script is the problem, not the timeline.

**Time is integer milliseconds everywhere** — clip starts, durations, comment
anchors, chapter starts. Not float seconds, not frames. Frames tie the data to a
frame rate that can change; floats accumulate error across a timeline until two
components disagree about where a beat is.

---

## Stage state

Derived from disk on every request, never cached. A stage is `ready` when its
directory has content, `empty` otherwise.

The design calls for a third state — `stale`, computed from content hashes so that
editing narration for one section marks only that section's downstream work stale.
**Nothing computes it, and nothing records the hashes.**

A `storage/manifest.py` used to sit here claiming to be that mechanism. It was
deleted in the second review: nothing imported it, it was keyed by `chapter` and
scene id — a shape this pipeline never creates — and it declared a second `Stage`
enum (`SOURCE/SCRIPT/AUDIO/IR/RENDER`) colliding by name with the real six.
`downstream_of` in `stages.py` claimed to "pair with the manifest's content
hashing", which was never possible: the two enums had no member in common. The
design survives in
[data-layout.md](../design/data-layout.md#the-manifest--incremental-rebuild); the
code did not, because it modelled the wrong pipeline.

Recording that here is the point: a reader who sees `stale` in the CSS and not in
the API should find out why from this document rather than from `git log`.

---

## Agents and tools

An `AGENT.md` declares the tools its agent may operate. The declaration **is** the
grant — an agent cannot reach a tool it was not given.

Resolution is project-then-default. Edits always write the project override; the
shipped default is never modified, so tuning one project cannot silently change
another.

**Unknown tool names are reported, never dropped.** A typo would otherwise quietly
remove a capability, and the symptom — an agent that stops doing something it used
to — is very hard to trace back to a misspelling. A test asserts every shipped
agent declares only real tools.

**Every fetch tool must name its resources.** Shipping someone else's copyrighted
image is a real problem and the agent will not be the one to notice; a test
enforces the declaration.

**No agent is connected to a model.** The panel is a surface: it reads, edits and
resets `AGENT.md`, and sends nothing anywhere.

---

## Stage options

Declared once in [stage_options.py](../../src/pipeline/stage_options.py) — key,
label, help text, choices, default — and rendered generically by the UI. Adding an
option is one entry; no template change, no new route.

Unknown keys are dropped rather than persisted, and an invalid stored value falls
back to its default rather than crashing the stage. A settings file hand-edited
into nonsense must not make a tab unreachable.

---

## Configuration

All environment configuration is read in one place,
[config.py](../../src/pipeline/config.py), and nowhere else. Limits with domain
meaning are named constants next to the logic that enforces them —
`MAXIMUM_SOURCE_FILE_SIZE_IN_BYTES` rather than `67108864`.

Explicit LLM `timeout` and `max_retries` are set there deliberately: v1 constructed
its client with neither, so a dropped connection surfaced as a failed scene with no
code generated, losing minutes of work per scene.

---

## Authentication

**There is none.** The app binds to `127.0.0.1` and assumes a single trusted local
operator.

This is a deliberate current-state decision, not an oversight, and it is
load-bearing for several others: no CSRF protection, no per-request authorisation,
no rate limiting, and `ProjectStore.get` trusting its slug argument.

**If this is ever exposed beyond localhost, all four need revisiting**, and the
question of who operates the system
([Q4](../open-questions.md#q4--who-operates-this)) has to be answered first.

---

## Known gaps

Recorded rather than quietly carried:

| Gap | Consequence | Status |
|---|---|---|
| No stage executes | The UI is a surface over artifacts a human fills in | By design; next work |
| No agent reaches a model | The agent panel edits text and sends nothing | Deliberate; surface only |
| Nothing renders | Studio and Reviewing previews say so rather than showing a fake frame | Blocked on [ADR 0007](../decisions/0007-revideo-as-rendering-target.md) |
| `stale` state unused | No content hashes are recorded anywhere | Blocked on stage execution |
| Extraction has no writer | `extraction/content.json` is declared and never written | Next work |
| No auth | Localhost only | Deliberate; see above |
| Uploads read fully into memory | The 64 MB cap bounds one upload; concurrent ones multiply | Streaming to disk is the real fix |
| `slugify` has no length cap | A very long project name makes a very long directory name | Not yet hit; worth a cap |
| A project cannot be deleted | `ProjectStore.delete` exists, guarded and tested, but no route reaches it — projects accumulate and only `rm -rf` removes one | Deliberate for now: irreversible, and it needs a confirmation design |
