# Data Layout

**Files are the source of truth. SQLite is a derived index and an operational log.**

> **This is a design, not a description.** Most of the layout below does not exist
> yet, because no stage executes. What is actually on disk today is the short list
> in [system-map.md](../architecture/system-map.md#what-is-actually-on-disk):
> `project.json`, `sources/`, `settings/`, `agents/`, and one JSON artifact per
> stage.
>
> The distinction is not pedantic. `.gitignore` was once written against the
> chapter tree below, matched nothing because that tree is never created, and
> staged a demo project — including an uploaded PDF — for commit. A layout
> document that reads as current when it is aspirational costs real mistakes, so
> every section here is marked.

---

## Why files

Not nostalgia — three concrete properties a database would cost you.

**The payload is already files.** Audio, video, generated code, transcripts. Storing
their metadata in a database while the bytes sit on disk splits truth across two
systems that can disagree.

**v1's file layout was not the bug.** The failure was save *cadence* — once per
batch instead of once per scene
([ADR 0003](../decisions/0003-durable-incremental-state.md)). Storage medium was
never implicated. And the layout demonstrably works: 253 scenes across 23 chapters
were indexed by globbing `state.json`, with no tooling.

**Inspectability.** `cd` into a chapter and everything about it is visible — the
brief, the audio, the IR, the generated scene, the render log. Debugging a bad
scene means reading files, not writing queries. For a system whose output is
reviewed by eye, this matters more than it sounds.

Plus: portable by copy, diffable in git for the text layers, no migrations.

---

## Layout — proposed

Where stage execution would put its output. Only `project.json`, `sources/` and
the per-stage artifact files exist today.

```
projects/
  <project>/
    project.yaml                    # voice, theme, model defaults
    sources/
      chapter-01.docx               # you author this — the only real input
    chapters/
      <chapter-slug>/
        chapter.yaml                # source ref, target duration, overrides
        manifest.json               # scene index + content hashes
        script/
          scenes.json               # comprehension output (structured)
          scene-00.md               # same content, readable
        audio/
          scene-00.wav
          scene-00.words.json       # word timings — the clock
        ir/
          scene-00.json             # the spine: typed, diffable, reviewable
        render/
          scene-00/
            scene.tsx               # generated Revideo scene
            out.mp4
            checks.json             # bounds / duration / contrast results
        review/
          scene-00.history.json     # every feedback round and what changed
        output/
          chapter.mp4
          chapter.srt
        logs/
          scene-00.render.log
          llm/
            2026-09-08T14-22-01Z.json   # one file per exchange

.index/                             # derived. rebuildable. gitignored.
  runs.db
```

### What is new versus v1

| Directory | Why it exists |
|---|---|
| `ir/` | The typed intermediate representation. Reviewable *before* rendering — see [Q8](../open-questions.md#q8--where-does-human-judgment-enter). |
| `review/` | Feedback history. In v1 this lived in shell scrollback and was lost. |
| `logs/llm/` | Every prompt and response. v1 persisted none, so prompts could not be improved from evidence. |
| `manifest.json` | Content hashes for incremental rebuild. See below. |
| `checks.json` | Mechanical verification results per [ADR 0004](../decisions/0004-mechanical-checks-before-human-review.md). |

---

## The manifest — incremental rebuild

**Proposed. No code implements this.** A `storage/manifest.py` did, briefly, and
was deleted in the second review: nothing imported it, and it was keyed by chapter
and scene id — a shape this pipeline does not create. The idea below is sound; the
implementation modelled v1's pipeline rather than this one, and re-keying it to
the six stages is a small job best done when there is something to hash.

The piece that most justifies files over a database.

```json
{
  "scenes": [
    {
      "id": 0,
      "source_hash":    "sha256:a1b2…",
      "narration_hash": "sha256:c3d4…",
      "audio_hash":     "sha256:e5f6…",
      "ir_hash":        "sha256:0789…",
      "render_hash":    "sha256:ab12…"
    }
  ]
}
```

Each stage records the hash of its inputs. That makes staleness **computable**
rather than guessed:

```
edit narration for scene 3
  → narration_hash changes
  → audio stale → word timings stale → IR beats stale → render stale
  → scenes 0,1,2,4… untouched
```

This is `make` semantics for a video pipeline. v1 has no concept of staleness at
all — after any edit the operator guesses which stage to re-run, and the CLI
offers no help.

It also makes **verified resume** possible: on restart, recompute hashes and know
precisely what is still valid. v1's resume trusts whatever `state.json` last said,
with no way to detect that an input changed underneath it.

---

## Where SQLite would earn its place

None of it exists yet — nothing in the system uses SQLite today, and files are
carrying the whole load. Recorded so the boundary stays deliberate when it does:

**`runs.db` — operational.** Job queue and run history. Concurrent scene workers
need real transactions; concurrent writers to a JSON file need a lock and still
lose updates. This is the one place a database is simply the right tool. It would
also hold LangGraph checkpoints if its SQLite checkpointer is used
([ADR 0006](../decisions/0006-langgraph-as-backbone.md)).

**An LLM exchange index — append-only.** Files under `logs/llm/` stay the durable
record; an index makes them queryable ("all failures last week", "token spend by
chapter"). Write both: the file is the artifact, the row is the index.

Anything added must be **derived or operational**, never source of truth.

---

## The invariant

> **Delete `.index/` and everything rebuilds from files.**

If that ever stops being true, something belongs in SQLite that should not be
there. It is worth an actual test in the suite: build the index, delete it,
rebuild, assert equivalence.

---

## Conventions

**Zero-padded scene ids in filenames** (`scene-00`), plain integers in data. v1
mixed `Scene0` and `scene_00` across directories, which made globbing fiddly.

**Scene ids start at 0**, matching v1. Worth stating explicitly in
operator-facing docs, since it surprises people.

**One exchange per file** in `logs/llm/`, timestamped. Append-only, trivially
greppable, no parsing to inspect one call.

**JSON throughout, for now.** This document originally called for YAML for
human-authored config (`project.yaml`, `chapter.yaml`) and JSON for machine-written
state, on the reasoning that humans get comments and machines get an unambiguous
parse. The code never did it: `project.json` is JSON, there is no `chapter.yaml`,
and no YAML parser is even a dependency. The argument still holds and is worth
revisiting when config grows past two fields — but until then, one format is
simpler than two, and a doc claiming otherwise is just wrong.

**Git: `projects/` is ignored entirely today.** The `.gitignore` in this repo
excludes all of it bar a `.gitkeep`, because a project directory holds someone's
uploaded source documents and nobody's PDF belongs in a shared repository by
default.

The proposal above — track `sources/` and optionally `ir/` — is a *per-project*
choice for a team that wants a reviewable history of one specific course, not a
default for the engine. If it is ever adopted it needs its own `.gitignore` inside
the project directory, and a decision about who owns the material.

That last point is worth emphasising: **the IR is small, textual, and meaningful in
a diff.** Committing it turns "what changed in this chapter?" into a readable
question — something generated Manim code could never support.
