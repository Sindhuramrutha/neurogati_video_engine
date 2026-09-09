# Beyond the Terminal

v1 is a CLI with a human review step that happens in a file explorer and a video
player. That shapes the work more than it appears.

---

## What the CLI costs today

Reconstructed from real production sessions:

```
python run_chapter.py --project NPS --input m-2.pdf --stage prepare
  ... wait 15-30 min, no visibility ...
explorer projects\NPS\m-2\rendered_video
  ... open each clip in VLC, watch, remember what was wrong ...
python run_chapter.py --project NPS --input m-2.pdf --scenes 0 --revise "Keep every visual element fully inside the frame. Nothing should be cut off at any edge..."
  ... wait, reopen, re-watch ...
python run_chapter.py --project NPS --input m-2.pdf --scenes 1 --revise "Keep every visual element fully inside the frame..."   ← same text, retyped
```

Observable problems:

- **No progress visibility.** A long run is opaque. Distinguishing "slow" from
  "hung" required inspecting process CPU.
- **Feedback is retyped prose.** The same correction was typed for scene 0 and
  again for scene 1. It is not reusable, not structured, not learned from.
- **Review is manual file management.** Open folder, find clip, open player,
  remember, alt-tab, retype command.
- **Comparison is impossible.** No way to see before/after, or scenes side by side.
- **No history.** Which revisions were tried, what changed, what worked — lost to
  shell history in a UTF-16 console dump.

At 253 scenes these are not annoyances; they are the dominant cost of operating
the system.

---

## What review actually wants to be

The review loop is: *watch → notice → describe → wait → re-watch.* A good
interface collapses it.

**Point instead of describe.** "This label is cut off" should be a click on the
label, not a sentence. The system already knows every element's bounding box —
clicking one identifies it unambiguously, which is exactly the closed-set
grounding `highlight_planner.py` uses.

**Scrub, don't watch.** Reviewing a 55-second clip should not take 55 seconds. A
timeline with beat markers, synced to narration text, lets a reviewer jump to the
moment being discussed.

**See the whole chapter.** A grid of scene thumbnails shows pacing and consistency
problems that watching clips serially hides.

**Compare revisions.** Before/after side by side, with the feedback that produced
the change.

**Reuse corrections.** "Keep everything inside the frame" was typed twice. It
should be a saved action applicable to any scene — and ideally a check that makes
it unnecessary.

---

## Interface options

### 1. Better CLI

Structured progress, per-scene status, `--watch` mode, saved feedback snippets.

**For:** cheap, scriptable, no new stack. **Against:** does not fix review, which
is the actual bottleneck.

### 2. Local review web app

`python -m pipeline.review` opens a browser. Scene grid, inline player, timeline
with beats, click-to-target feedback, revision history.

**For:** solves the real bottleneck. Video and timelines are native to browsers.
Local-only, so no deployment or auth. Can drive the same CLI underneath.

**Against:** a frontend to build and maintain.

**This is likely the highest-value non-pipeline investment.** Every scene passes
through review; a 2× faster review loop is worth more than a 2× faster renderer.

### 3. Notebook-driven

v1 has `main.ipynb` and a LangGraph graph with interrupts already.

**For:** exists; good for experimentation; inline video display works.
**Against:** poor for repeatable production; state in a kernel is fragile.

### 4. Service + queue

Long-running jobs submitted to a worker, artifacts to storage, status via API.

**For:** the honest answer for multi-hour work. Survives disconnection. Enables
parallel scene rendering — currently sequential, and embarrassingly parallel.
**Against:** infrastructure, for a small team.

**Worth noting:** scene rendering is independent per scene. Parallelism could cut
a 22-scene chapter's wall-clock time by most of an order of magnitude. That may
matter more than any single-scene speedup.

### 5. Editor integration

VS Code extension: scenes in a tree, preview on click, feedback inline.

**For:** where the developer already is. **Against:** narrow audience; extension
maintenance.

---

## Who is this for?

The interface question is really an audience question.

**Just you.** CLI plus a local review app is right. No auth, no deployment.

**The Neurovidya content team.** Non-technical authors need to submit content and
review without a terminal. That means a hosted service, upload, review links —
substantially more product.

**Both.** Common core; CLI for development, web for authors. Argues for a clean
separation between pipeline and interface from day one — worth deciding early even
if the web layer is built later.

---

## Observability

Independent of interface, v1 is unobservable. It cannot answer:

- Which stage is running, and how far in?
- How long has this scene been generating?
- What did the model actually return?
- How many tokens did this chapter cost?
- Which check failed, and what was the artifact at that moment?

Minimum worth building:

- **Structured logs** (JSON) per scene per stage — greppable, aggregatable
- **Every LLM exchange persisted** — prompt, response, model, tokens, latency.
  Essential for debugging and for building an evaluation corpus
- **Timing per stage** — where does the wall clock actually go?
- **Cost accounting** per scene and per chapter
- **Artifact snapshots** at each boundary — the IR, the code, the frames

Tracing tools worth considering: **LangSmith**, **Langfuse** (open-source,
self-hostable), **Weights & Biases Weave**, or OpenTelemetry with a generic
backend. See [agentic-stack.md](agentic-stack.md).

The persisted-exchange point deserves emphasis: **without a log of what the model
was asked and what it returned, you cannot improve the prompts, build an eval set,
or diagnose a regression.** v1 kept none of this.

---

## A reasonable sequence

1. **Structured logging and persisted exchanges** — foundational, cheap, enables
   everything else
2. **Local review web app** — attacks the dominant operating cost
3. **Parallel scene execution** — large wall-clock win, no interface work
4. **Service/queue** — only if the team beyond you needs access

Notably, none of this depends on which
[architecture option](architecture-options.md) you choose. It can proceed in
parallel.
