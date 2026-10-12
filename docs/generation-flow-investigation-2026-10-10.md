# Generation flow investigation — 10 October 2026

## Problem reported

The reported problem is that scene generation takes too long, produces weak or empty-looking scenes, needs repeated revisions, and can finish without a usable result despite extensive upstream planning. The supplied Generation screenshot shows the `demo` project with 57 scenes.

This report separates what the screenshot and current source code establish from causes that still require per-scene records. It is a diagnosis, not a claim that the pipeline has been fixed.

## Evidence from the screenshot

- The project has 57 scenes: 6 are counted as passed in the heading; the bar shows 3 passed to watch, 4 being made, 47 queued, and 3 stopped or failed.
- Four scenes are being made concurrently and the rest are queued in order, so this run has a long serial tail.
- The previews vary sharply. Scene 2 shows a headline and three small outlined labels joined by a line. Scene 1 shows “Not made yet”; scene 3 says “could not be made” and its preview is mostly blank.
- Scene 3’s visible diagnostic starts with a text-bounds failure: `Text inside the frame -- “Electricity and ...”`. The screenshot clips the rest of the error.
- “6 passed” and “3 passed, to watch” may count approved and newly passed scenes separately. The screenshot alone does not establish a UI count defect.

The screenshot does not reveal the full event logs, served code revision, model provider, or time spent in each stage.

## What the current working-tree code does

Generation is an open-ended program-authoring loop. For each scene, it prepares a brief and picture notes, asks a model to write or edit renderer code, runs that code, checks the result, and—only if the mechanical checks pass—asks a vision model to review sampled frames. Check failures are sent back to the code-writing model for another attempt.

Relevant source evidence:

- `src/pipeline/scene_maker.py:61` sets `MOST_ROUNDS = 3`; the loop at lines 338–397 can render at most three authored attempts in this checkout.
- `src/pipeline/scene_maker.py:62` permits up to three unusable-answer asks per round. `_ask` at lines 274–291 can make an initial provider call plus three retries after provider failures, waiting 20, 40, and 60 seconds before those retries. Request pacing can add further waits.
- `src/pipeline/scene_round.py` invokes visual review only after every mechanical check passes. Review is another model call. If the review call fails, the result is “could not be reviewed,” not a positive visual verdict.
- `src/pipeline/scene_agent.py:35` defaults to four scene agents at once. `src/pipeline/scene_round.py:22` defaults to two concurrent renders. `src/pipeline/llm_pace.py:9–28` paces all model requests at 28 per minute by default.
- If no authored attempt produced a clip, `scene_maker.py:401–459` renders a plain fallback stand-in. That fallback can still fail checks; it is not a designed scene.
- `src/pipeline/scene_checks.py` applies many independent rules: text bounds, overlap, contrast and size; text grounding; minimum graphics across beats; use of an offered slide picture; frame variation; and explanatory motion. A failed check bypasses visual review for that round.

## Confirmed mismatch: code versus operating instructions

| Source | Maximum rounds stated |
|---|---:|
| Current `scene_maker.py` | 3 |
| `docs/operations/generation-sop.md` | 6 |
| `docs/operations/scene-programs-sop.md` | 6 |

The UI’s `most_renders` value comes from `scene_agent.MOST_RENDERS`, which aliases the code constant. A server running this checkout should expose 3. The screenshot/user report describes six iterations. This indicates either a served-version mismatch or a different meaning of “iteration”; the server revision and scene event history are needed to tell which. The written SOPs are stale relative to this checkout regardless.

## Why the flow can take time and still fail

1. **The expensive checks happen after code generation and rendering.** Each retry is another model-authored program and renderer run, rather than a cheap draft from a known composition that can be rejected before rendering.
2. **A mechanical pass can require more work.** It triggers a vision-review call. If that reviewer identifies a must-fix issue, the scene needs another authoring/render cycle.
3. **A mechanical failure gets narrower feedback.** The visual reviewer does not inspect that render; the code author sees the fixed-check messages and must infer a repair. A recurring layout or renderer-specific failure can consume the attempt budget.
4. **The batch has shared bottlenecks.** Four agents share one provider request limit, while only two renders can run concurrently. A 57-scene workload can therefore take a long time even if each scene needs one authored attempt. Retries, reviews, render duration, and pacing add to it. Exact duration cannot be calculated from the screenshot.
5. **Fallback explains how a clip can exist without a usable visual.** If authoring produces no clip, the pipeline draws a plain stand-in. A saved/rendered artifact is not the same as a successful scene. Scene records are needed to determine whether a blank-looking card is fallback, stale poster, or missing render.
6. **Repeated failure can be terminal.** If no attempt passes and there is no previously passing version to keep, the scene can end as failed. That is consistent with scene 3’s status, but its full log is required to confirm the path.

## Likely quality contributors (not confirmed for each screenshot card)

- The model must satisfy many partly independent constraints at once. That can reward a diagram that technically contains labels, shapes, and motion without ensuring a clear visual hierarchy or a strong teaching moment.
- Visual review runs only after all fixed checks pass, so failed renders do not receive the broader art-direction feedback that could identify the underlying visual problem.
- Renderer instrumentation is uneven. The checks warn when a renderer does not record its text or animations, and `scene-programs-sop.md` documents such limitations for Revideo. The quality gate is therefore not equally measurable across renderers.
- The loop asks a model to invent renderer code for each scene; it does not guarantee a polished composition through a deterministic set of tested layout primitives before spending repeated model/render cycles.

The sparse scene 2 frame is direct visual evidence that “made” can still look weak. The screenshot cannot establish whether it passed because of renderer instrumentation, a reviewer verdict, or a stale/mismatched card state.

## Evidence still needed for a scene-level root cause

The `demo` project has scene folders matching the screenshot, but I could not read their `agent.json`, `checks.json`, `log.txt`, source programs, or sampled frames. Windows returned “There is not enough space on the disk” when the shell stopped launching. No project files were deleted.

To explain the exact failures and time cost, inspect:

- the running server’s revision and effective generation settings;
- `agent.json` for scenes 1–3 and one passed scene, including event, call, render, token, and timing data;
- the affected `checks.json`, `log.txt`, renderer program, and sampled frames;
- the Generation API response and page count logic, to verify the two passed-scene categories.

API keys and unrelated project documents are not needed.

## Findings and next investigation order

The observed pain is consistent with the generation architecture: repeated free-form code generation, execution, rule repair, and conditional visual review. The screenshot confirms at least one text-bounds failure and one visually sparse output. Shared pacing and render limits explain why a large queue can take time, but timings are needed to quantify the delay. The fallback path explains how a scene can end with an artifact that is not useful.

Before changing prompts, thresholds, or concurrency:

1. Reconcile the deployed revision, round limit, and UI status categories.
2. Read the affected scene records and frames; classify failures as model transport/output, program/runtime, mechanical check, visual review, or fallback.
3. Measure time spent waiting for model slots, generating, rendering, checking, and reviewing.
4. Then reduce repeated work at its source: use tested renderer-specific composition primitives, inspect failed renders visually, and define a small set of observable criteria for a usable non-placeholder preview. Reconsider concurrency only after measuring; increasing it may add memory pressure and provider waits without improving scenes per minute.
