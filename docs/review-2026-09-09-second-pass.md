# Engineering review — second pass

Follows [review-2026-09-09.md](review-2026-09-09.md), which covered the project and
upload surface. Everything built since — four stage artifacts, six stage modules,
the shared frontend — had not been reviewed.

**Scope note, stated honestly:** this is still a young codebase — 2,800 lines of
Python, 4,400 of browser code and markup, 1,300 of tests, built over a handful of
sessions. It is not production-scale and framing it as such would flatter it. The
standard still applies, and every defect below was reproduced or shown by a failing
test, not asserted.

---

## Summary

| | |
|---|---|
| Defects found | 9 |
| Fixed | 9 |
| Persistence implementations | 6 → 1 |
| Optimistic-save implementations | 4 → 1 |
| Inline id generators | 9 → 1 |
| Wrong-shaped modules removed | `manifest.py`, plus the dead half of `layout.py` |
| Tests before / after | 56 / 102 Python, 0 / 7 frontend |

The most serious finding was **cross-project data corruption**: editing a document
after switching projects wrote one project's work into another project's file.

---

## Findings

### 1. Cross-project write corruption — CRITICAL

Selecting a different project rebuilt the stage surface but left the previous
project's `plan`, `script`, `composition` and `review` in `applicationState`, while
`projectApiPath` already resolved to the *new* slug.

The first edit after a switch therefore POSTed project A's document to project B's
URL. Silent — the save succeeded, the UI showed success, and project B's real work
was gone.

**Two independent fixes, because either alone is one refactor from being wrong:**

1. Every project-scoped field now lives in one `PROJECT_SCOPED_STATE_DEFAULTS`
   object, and `clearProjectScopedState()` resets from it. A new field is cleared
   because it is in the object, not because someone remembered to add a line.
2. Every save captures the slug before the request and discards the response if it
   changed in flight. A round-trip is long enough for a user to switch projects.

**Verified:** `test_frontend_contracts.js` asserts that every key of the defaults
object is reachable from the clear function, and that each stage module's save
compares the slug. Both fail if a future field is added and forgotten.

### 2. Six hand-rolled persistence implementations

`PlanStore`, `ScriptStore`, `CompositionStore`, `ReviewStore`, `SettingsStore` and
`ProjectStore` each had their own temp-file-then-rename, their own corrupt-file
handling and their own id generator. They agreed only because they were written in
one sitting.

The next store added under time pressure would have been the odd one out, and the
divergence would be invisible until someone lost a file.

**Fixed:** [storage/documents.py](../src/pipeline/storage/documents.py) — one
`JsonDocumentStore`, one `write_text_atomically`, one `new_identifier`. Each store
is now a subclass that names a path, a model and a default.

**Verified:** `test_all_document_stores_share_one_durability_implementation`, and
`test_every_document_store_survives_a_corrupt_file_without_destroying_it`
parametrized over all four artifacts.

### 3. The atomic-write guard matched a variable name, not a behaviour

The test written to prevent finding 2 from recurring searched source files for the
literal string `temporary_path.replace`.

That is a variable name. `manifest.py` wrote `tmp.replace(path)` — the same
temp-then-rename dance, a different local — and passed.

**Fixed:** the guard now matches the *shape* (a temp suffix and a rename in the
same module). It failed immediately on `manifest.py`, which is how finding 4 was
confirmed rather than argued.

A test that can only catch the instance it was written for is worse than no test:
it reads as coverage.

### 4. `manifest.py` modelled a pipeline that does not exist — REMOVED

Presented in the docs as "built and tested but unwired." It was worse than unwired:

- **Nothing imported it.** Not one module, in either direction.
- **It was keyed by `chapter` and scene id.** This pipeline has no chapters and no
  scene directories; a project is six stage folders.
- **It declared a second `Stage` enum** — `SOURCE/SCRIPT/AUDIO/IR/RENDER` — sharing
  a name with the real six-member `Stage` in `stages.py` and having no member in
  common with it.
- **`downstream_of` claimed to "pair with the manifest's content hashing."** That
  was never possible. Two enums with no shared member cannot key the same data.

It was v1's manifest, carried across and never re-shaped.

**Removed**, with its 7 tests. The design — content hashes making staleness
computable rather than guessed — is genuinely good and survives in
[data-layout.md](design/data-layout.md#the-manifest--incremental-rebuild), now
marked as proposed. Re-keying it to the six stages is a small job, and the right
time is when there is something to hash.

**Recorded plainly because this is a deletion, not a fix:** the code is gone from
the working tree and was never committed, so it is not recoverable from history.
The reasoning above is the record.

### 5. `storage/layout.py` documented a layout the system never creates

The module docstring described `chapters/<chapter>/{script,audio,ir,render,...}/`,
and `ChapterPaths`, `ProjectPaths`, `scene_stem`, `project()` and `projects()`
existed to build it. **Only `slugify` was ever imported.**

This fiction had already cost something real. `.gitignore` was written against it —
`projects/*/chapters/*/audio/` and similar — so its patterns matched nothing, and a
demo project including an uploaded PDF was staged for the first commit. That was
caught in this pass while checking what would actually be committed.

**Fixed:** the dead classes are gone and the docstring now describes the real
layout. `layout.py` regained a real job (finding 6) rather than being reduced to a
one-function module.

### 6. Stage artifact paths were declared in one place and written in another

`stages.py` declares a `produces` string per stage, shown in the UI under each
stage card. Each store separately hard-coded its own path.

Two had drifted:

| Stage | UI showed | Actually written |
|---|---|---|
| Scripting | `scripting/scenes.json` | `scripting/script.json` |
| Reviewing | `reviewing/report.json` | `reviewing/review.json` |

Nothing failed, because a label is only ever read by a human — which is exactly why
it stayed wrong. Anyone told to "look at `reviewing/report.json`" would find
nothing there.

**Fixed:** `artifact_path(project_root, stage)` in `layout.py` derives the path
from the stage's own declaration, and all four stores use it. The label and the
file are now the same string by construction.

**Verified:** `test_every_store_writes_where_its_stage_says_it_writes`.

### 7. Four optimistic-save implementations, nine inline id generators

Each stage module had written its own save: mutate local state, POST, roll back on
failure. Four copies, subtly different — one rolled back to a stale snapshot, one
did not re-render after rollback, and one still used `crypto.randomUUID` where the
others had moved to a shared generator.

**Fixed:** [document-editing.js](../src/pipeline/web/static/document-editing.js) —
one `editStageDocument`, one `loadStageDocument`, one `newItemIdentifier`.

**Verified:** three separate contract tests. The `crypto.randomUUID` leftover in
`stage-scripting.js` was found by that contract test failing, not by reading.

### 8. Eight guards silently dropped user actions

Every stage carried `if (isSaving) return;`. A user clicking "Add section" while a
previous save was in flight got nothing at all: no message, no queued action, no
disabled state. The app simply ignored them.

This is a character defect as much as a correctness one. Silence teaches a user
that the app is unreliable, and they stop trusting the parts that work.

**Fixed:** the guard now shows *"Still saving the last change — try again in a
moment."* Four `isSaving` flags that nothing read were deleted.

**Verified:** a contract test fails if any guard returns without notifying.

### 9. `stages.py` documented a `SKILL.md` that never existed

The module docstring explained at length that each stage "is governed by a
SKILL.md the operator can edit" and why that mattered. The mechanism is real; the
filename is `AGENT.md` and always was. A test was named
`test_editing_a_skill_invalidates_only_downstream`.

Small, but it is the first file a new reader opens to learn the stage model, and it
sends them looking for a file that is not there.

**Fixed:** docstring and test renamed to the thing that exists.

---

## Documentation defects

Found while checking whether the docs described the system or an intention.

**`system-map.md` claimed "Three, and only three" boundaries** and documented a
`FORMS` validation table for a module deleted two sessions earlier. It mentioned
none of the four stage artifacts. Rewritten against the code, with the enforcing
test named for each claim.

**`data-layout.md` read as a description and was a proposal.** It specified YAML
for human-authored config — the code writes JSON and no YAML parser is even a
dependency — and advised tracking `sources/` in git, which the actual `.gitignore`
correctly refuses to do. Every section is now marked, with a note at the top
explaining that this exact ambiguity is what produced the `.gitignore` failure.

**Four links pointed outside the repository.** `../../../docs/` resolves on the
machine these were written on and nowhere else; once `new-pipeline` is a repository
root, every one is dead for anyone who clones it. Converted to prose citations that
name the file.

---

## Deliberately not fixed

**Uploads are still read fully into memory.** The 64 MB cap bounds one upload, but
concurrent large uploads multiply. Streaming to disk is the real fix and belongs
with a request-size limit at the ASGI layer, not bolted onto the validator.

**`slugify` still has no length cap.** Capping it changes the slug — and therefore
the directory — of any existing long-named project. Not worth a silent migration
for a case not yet hit. It stays in the known-gaps table.

**ADRs were not edited**, including where they describe the manifest as designed.
The repository's own convention says ADRs are dated records and are superseded
rather than rewritten. Only dead links were repaired.

---

## What I verified, and how

| Claim | Evidence |
|---|---|
| Cross-project corruption was real | Traced state through a project switch; the stale document and the new `projectApiPath` are both observable in the code path |
| It is now closed twice over | Two contract tests, each failing when its guard is removed |
| Stores share one durability implementation | `test_all_document_stores_share_one_durability_implementation` |
| No module hand-rolls an atomic write | Hardened guard; it caught `manifest.py` on first run |
| Corrupt artifacts are never overwritten | Parametrized over all four stores; asserts the original bytes survive |
| Store paths match their stage declaration | `test_every_store_writes_where_its_stage_says_it_writes` |
| `manifest.py` was unreachable | `grep` for importers across `src` and `tests`: none |
| `.gitignore` excludes what it should | `git add -An` and `git check-ignore` on `.venv`, `projects/`, the uploaded PDF, the stray clone |
| Full Python suite | **102 passed** |
| Frontend contracts | **7 passed** |
| Lint | `ruff check src tests` → **All checks passed** |

## What I did not verify

Stated plainly rather than implied:

- **No browser testing.** The frontend changes were verified by static contract
  tests and by reading. Rendering, keyboard navigation, focus behaviour and layout
  were not exercised in a real browser this pass.
- **The frontend contract tests are static.** They read source text and assert
  structural properties. They do not execute the modules, so they prove that one
  implementation exists — not that it is correct.
- **No concurrency testing.** The mid-request project check is argued from the code.
- **Stage execution still does not exist**, so nothing about the pipeline's actual
  behaviour was tested — only the surface and the artifacts around it.

---

## Character preserved

The pass did not flatten the UI to make it robust.

- The **five stage colours** still drive heading, card accents, notice borders and
  primary buttons, so each stage reads as its own place.
- Failure now appears **where the user is looking**, in the stage's own colour for
  success and a distinct red for failure — not in an `alert()`.
- A blocked action **says what is blocking it** rather than going inert.
- Empty states say what is missing and why, rather than showing a placeholder that
  implies something rendered. The Studio and Reviewing previews say "rendering is
  not built yet" instead of displaying a plausible frame.

That last one is the review's position on honesty in a UI: a surface that pretends
to have output is the same defect as a doc that describes a layout the code never
creates.
