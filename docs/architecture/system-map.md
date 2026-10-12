# System map

What crosses which boundary, what each side promises, and what holds the whole
thing together. The contracts are written down because the failure that matters is
rarely "the code is wrong": it is "two modules disagreed about who validates what".

## The layers

```text
Inputs → Extraction → Assets & Design → Scene Plan → Script & Staging → Generation → Render
                                                                                       │
                                                       Studio · Reviewing · Export ◄───┘
```

Each layer reads only what the one before it **transferred**. A layer's working
copy is its own; a transfer freezes it for the next. When a layer is transferred
again, every layer after it is flagged out of date and says what changed
([change-flags-sop.md](../operations/change-flags-sop.md)). The diagram of what each
layer does, and what it keeps on disk, is [WORKFLOW-DIAGRAM.md](../../WORKFLOW-DIAGRAM.md).

## Boundaries

```text
   browser ──① HTTP ──► Litestar ──② calls ──► domain modules
      │                                             │
   ①b its own state                          ③ filesystem
                                           (source of truth)
```

### ① Browser → HTTP

`requestJsonFromApi` in [shared-client.js](../../src/pipeline/web/static/shared-client.js)
is the only way a page reaches the API. It returns parsed JSON (or `null` for 204)
or throws `ApiRequestFailed`; it never returns a partial value, so a caller cannot
mistake a failure for data.

| Failure | The user sees | Recoverable |
| --- | --- | --- |
| Server unreachable | "Could not reach the server. Is it still running?" | Retry |
| Offline | "You appear to be offline." | Retry |
| 4xx / 5xx | the API's `detail` | Depends on the route |
| 200 with malformed JSON | "The server returned a malformed response." | No: a server bug |

No module calls `fetch` directly. `tests/test_frontend_contracts.js` enforces it.

### ①b Browser → its own state

Everything scoped to a project lives in `PROJECT_SCOPED_STATE_DEFAULTS` in
[ui-kit.js](../../src/pipeline/web/static/ui-kit.js), and switching project calls
`clearProjectScopedState()`, which resets every field because it is derived from
that one object. Every save also captures the project's slug before it starts and
discards its response if the slug changed in flight, so one project's document is
never written into another's file. Both rules are asserted in
`test_frontend_contracts.js`, as is "no in-flight guard silently drops a user
action": a button that does nothing teaches the user the app is unreliable, so it
says "Still saving the last change — try again in a moment."

### ② HTTP → domain

Routes are thin: they resolve a project, call one domain function, and shape the
response. Validation happens here, where bad input arrives.

| Input | Validated by | On rejection |
| --- | --- | --- |
| Uploaded source file | `store_uploaded_source_file` (`sources.py`) | Per-file reason |
| Project name | `create_project` route | 400 with a reason |
| Stage key | `Stage(...)` coercion | 404 |
| Stage options | the declaration in `stage_options.py` | Unknown keys dropped; invalid values fall back |
| Plan / script / composition / review | the Pydantic model of that artifact | Clamped or trimmed, never rejected |

**Partial success is an outcome.** Five files with one unsupported store the four
and report the fifth. **Artifacts clamp rather than reject**: a 40-hour section is
clamped and flagged in `warnings`, never a 400, so one absurd number never loses
the rest of an edit. Warnings never block a save
(`test_warnings_are_advisory_and_never_block_a_save`).

### ③ Domain → filesystem

Files are the source of truth; there is no database. Every artifact path is derived
in [storage/layout.py](../../src/pipeline/storage/layout.py) from the `produces` field
each stage declares in [stages.py](../../src/pipeline/stages.py), so the path shown in
the UI and the path written are the same string
(`test_every_store_writes_where_its_stage_says_it_writes`).

- **No write escapes its project directory.** Filenames are reduced to a bare name
  under POSIX and Windows rules and the resolved destination is re-checked.
- **Durable writes are atomic**: temp file, then rename, in one implementation,
  `write_text_atomically` in [storage/documents.py](../../src/pipeline/storage/documents.py)
  (`test_no_module_hand_rolls_an_atomic_write`).
- **A corrupt file is never overwritten.** A store falls back to its default, logs
  at ERROR, and leaves the file for manual recovery: a corrupt `script.json` may hold
  hours of someone's writing.
- **A failed create leaves nothing behind**, so a slug is never wedged.
- **Deleting a project is permanent, and always works.** Whatever is running in it
  (scenes being made, a render, queued jobs, their ffmpeg, Manim and browser
  processes) is stopped first by `project_work.py`, then the folder is erased: no
  trash, no recovery. A thread stuck in a model call is not waited for more than
  30 seconds; it writes nothing when it returns.

## On disk

```text
projects/<slug>/
  project.json
  sources/                         the uploaded document, unchanged
  extraction/content.json          structured blocks; assets/ holds the figures
  assets/library.json              which pictures to use, and the video's look
  scene-plan/plan.json
  script-staging/script.json
  generation/visuals.json          one entry per scene; scenes/ one folder per scene
  studio/composition.json
  reviewing/review.json            comments, chapters, versions; output/ the renders
  export/                          manifest, transcript, chapters, description
  settings/  agents/  drafts/      stage options, agent overrides, plan proposals
```

## Rules that hold the system together

**One source file per project.** A project is made from one document (a deck, PDF,
Word, Markdown or text file) and it runs through every layer. A second upload
replaces the first only when the request says `replace`. Replacing it leaves later
work in place and flags it out of date, keyed by slide or heading rather than by
file, so a new version of a deck shows the slides that differ.

**One chain.** Assets & Design hands on to the Scene Plan alone: the plan attaches
pictures to sections, and its transfer carries them, the brand kit and the look
(`TransferredPlan.assets`). Every later reader goes through
`plan_pictures.assets_for_later_stages`.

**Every scene is a program that is looked at.** Generation has no shot to choose:
each scene is a program written, rendered, checked and fixed (`scene_maker.py`)
until the fixed checks pass and a vision review of its frames says it teaches.
Each round is one model call asked afresh, answering with a few-line edit or the
whole file. The renderer is the model's choice (a web page, Revideo, Manim,
matplotlib or Pillow). It never stops to ask; the render refuses scenes that are
not approved programs. Scenes are made on the server a few at a time
(`scene_agent.py`) and every model call waits for a place in the provider's
per-minute limit (`llm_pace.py`). See
[scene-programs-sop.md](../operations/scene-programs-sop.md).

**The audio is the clock.** The render synthesises each section's narration,
measures its real length, and cuts the picture to fit; word timings place both
animation beats and subtitles, so they cannot drift apart.

**Structured output over free text.** A model that produces an artifact returns a
validated Pydantic model (`complete_structured`); a malformed answer fails next to
the call that caused it and is re-asked against the schema, never repaired by hand.
Free text is for prose a person reads.

**Mechanical checks come before human review.** Each layer's checks are fixed rules:
the same work always gets the same results. A failing check blocks the transfer.
A person is asked to judge only what a rule cannot.

**State is durable and incremental.** Every layer saves its artifact as it goes, so
an interrupted run loses at most the step it was on, and a restart resumes from
the files.

**Feedback flows backwards to a stage.** "The pacing is frantic" is a Script &
Staging defect, not a Studio one. A review comment carries `routed_to_stage`, and
`Review.comments_by_stage()` says where to go next.

**Time is integer milliseconds** (clip starts, durations, comment anchors, chapters):
frames tie data to a frame rate that can change, and floats accumulate error until
two components disagree about where a beat is.

## Agents and tools

An `AGENT.md` ([agents/](../../agents)) is a stage's instructions and the tools it may
operate; the declaration is the grant. A project can override a stage's agent;
resolution is project, then default, and edits always write the project copy, so
tuning one project never changes another. Unknown tool names are reported, never
dropped (`test_unknown_tool_names_are_reported_not_dropped`), and every fetch tool
must name its licence-clear resources (`test_fetch_tools_declare_licence_clear_resources`).

## Stage options

Declared once in [stage_options.py](../../src/pipeline/stage_options.py) (key, label,
help, choices, default) and rendered generically by the UI: adding an option is one
entry. Unknown keys are dropped and an invalid stored value falls back to its default,
so a hand-edited settings file cannot make a tab unreachable.

## Configuration

All environment configuration is read in [config.py](../../src/pipeline/config.py) and
nowhere else. Limits with domain meaning are named constants beside the logic that
enforces them. Model calls set an explicit `timeout` and `max_retries` there, so a
dropped connection is a reported failure, not a silent loss.

## Authentication

There is none. The app binds to `127.0.0.1` and assumes one trusted local operator.
That is load-bearing for CSRF protection, per-request authorisation, rate limiting
and `ProjectStore.get` trusting its slug. If the app is ever exposed beyond localhost,
all four need to be added first.

## Limits

| Limit | Consequence |
| --- | --- |
| Scene programs in Manim, matplotlib or Pillow are not sandboxed | They run with the user's permissions: they can read the user's files and use the network (they are not given the server's API keys). Web and Revideo scenes are confined to their own files, the animation libraries and the pictures they were offered |
| The provider's per-minute request limit paces every model call | A whole video takes tens of minutes. Raise it with `LLM_REQUESTS_PER_MINUTE` if the plan allows |
