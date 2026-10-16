# Academic Explainer Video Pipeline

Turns written academic material (lecture notes, chapters, slide decks) into a narrated explainer video.

```text
Inputs → Extraction → Assets & Design → Scene Plan → Script & Staging → Generation → Studio → Reviewing → Export
```

The pipeline never hides work inside a model call. Every stage's output is a
JSON file on disk, each response says what is inconsistent, and the video's
timing is measured from the narration audio rather than estimated.

---

## Contents

- [Academic Explainer Video Pipeline](#academic-explainer-video-pipeline)
  - [Contents](#contents)
  - [What it does today](#what-it-does-today)
  - [Requirements](#requirements)
  - [Quick start](#quick-start)
  - [Using the app](#using-the-app)
  - [Configuration](#configuration)
  - [Narration voices](#narration-voices)
  - [Command line](#command-line)
  - [MCP server](#mcp-server)
  - [Agents](#agents)
  - [Where project data lives](#where-project-data-lives)
  - [Architecture](#architecture)
  - [Development](#development)
  - [Documentation](#documentation)
  - [Status and known limits](#status-and-known-limits)

---

## What it does today

| Stage | What happens | Produces |
| --- | --- | --- |
| **Inputs** | Upload source documents: `.pdf`, `.docx`, `.pptx`, `.md`, `.txt`. Up to 512 MB per file, streamed to disk. Each file can be opened and viewed as itself: decks slide by slide, Word documents with their layout, PDFs in the browser's viewer. | `sources/` |
| **Extraction** | Parses the sources into structured blocks: headings, paragraphs, lists, tables and figures, in document order and filed under the heading they belong to. No model is involved; it is parsing. Embedded images are saved as figures. For decks it can also capture the **slide layout** (where each title, picture and text box sits), the **background images** behind the slides, and the **styling** (theme colours and fonts). Its agent reviews what came out: every picture is opened and measured, and the agent reads the text for what the checks cannot see. | `extraction/content.json`, `extraction/assets/` |
| **Assets & Design** | Every extracted picture, with what it measures and where it came from — the source, a person or a model — and a decision about each: use it or skip it. Decisions are keyed by the picture itself, so re-extracting never loses them. Also holds **the look**: the source deck's colours, fonts and proportions, and whether the video should follow them. | `assets/library.json` |
| **Scene Plan** | The video's shape, agreed in a conversation with the planning agent: its length, its sections (each a run of slides) and the scenes each is made of. You set the length in your own words and how strictly the slides' order is kept; the agent proposes, you agree or say what to change, and only then are the scenes written. The order is held by code. The plan carries each section's pictures, the brand kit and the look on. | `scene-plan/plan.json`, `scene-plan/conversation.json` |
| **Script & Staging** | Each plan section written as **scenes**: what is said, and a brief of what is on screen while it is said. The Scripting agent drafts one section or every unwritten one at once, from that section's own source text. Beside the editor sit the section's plan details, its source text and any review comments. Flags narration written against a plan section or source that has changed since, and narration whose section the plan no longer has. `{{VARIABLES}}` are filled everywhere they are spoken or shown. | `script-staging/script.json` |
| **Generation** | Every scene made by a short loop: one screen, drawn by a program the model writes, renders, has reviewed and fixes until it is good, in time with the narration. Things come onto the screen as the words name them; some stay, some go, and new things keep arriving. The model chooses its renderer — a web page (GSAP, D3, three.js, anime.js), Revideo, Manim or matplotlib — is offered every picture in the deck (its own slide's first) with what each is, fills what the deck does not show with a photo found under an open licence, an icon or a painting, and has its frames reviewed by a vision model. Fixed checks decide whether a clip may be used, then you approve it. | `generation/visuals.json`, `generation/scenes/` |
| **Studio** | A multi-track timeline with playback, seeking and clip properties. Rendering synthesises the narration, measures each section's real audio length, and cuts the picture to fit. Each section is drawn with its own extracted pictures, and — when the project asks for it — the source deck's background, colours and fonts. | `studio/composition.json` |
| **Reviewing** | Plays the rendered video with chapters and subtitles, keeps every render as a separate version, and collects comments routed back to the stage that should fix them. | `reviewing/review.json`, `reviewing/output/` |
| **Export** | The video and everything that travels with it: a transcript, chapter marks a video host can read, a description built from the plan, and the subtitles. Every file is derived, never hand-written. Says plainly what would make the hand-over wrong — a cut built from an abandoned script, a section nobody narrated, a missing video file. | `export/manifest.json`, `export/` |

The **Orchestrator**, the Agent panel in the top bar, sits above every
stage. Ask it anything about the project from any tab: it decides which stage
agents can answer, asks several at once, reads whatever artifacts it needs, and
replies with a list of who it consulted. Click an agent's name to read what that
agent actually said. Conversations are kept per project: **New conversation**
starts a fresh thread, **History** lists the earlier ones, and reopening one
continues it -- the agent is told what was already said. It reads and asks; it
never writes to the project.

---

## Requirements

| | Needed for | Notes |
| --- | --- | --- |
| [uv](https://docs.astral.sh/uv/) | everything | Provisions Python 3.12 itself. Python is pinned `<3.13` because the optional Kokoro voice requires it. |
| An OpenAI-compatible model API key | the agents | Defaults to TokenRouter with `deepseek/deepseek-v4-flash`. Any compatible endpoint works. |
| [ffmpeg](https://ffmpeg.org) on `PATH` | rendering video | Windows: `winget install Gyan.FFmpeg` |
| Node.js | frontend tests only | Not needed to run the app. |

Everything else, including the in-browser document viewers, ships in the
repository and works offline.

---

## Quick start

```bash
git clone https://github.com/shivam-kumar25/acedemic-explainer-video-pipeline.git
cd acedemic-explainer-video-pipeline
uv sync
uv run pipeline serve
```

Open <http://127.0.0.1:8000>, then:

1. Click **API keys** and paste your model key. It is written to `.env`, which
   is gitignored and never sent to the browser.
2. **New project**, then drop your documents on **Inputs**.
3. Go to **Extraction** and click **Extract content**.
4. On **Assets & Design**, click **Gather pictures** to see what the documents
   contain and decide which are worth showing.
5. On **Scene Plan**, click **Draft plan**, review the proposal, and accept it
   (or build the plan by hand).
6. On **Script & Staging**, click **Draft all unwritten** to have the agent
   write every section as scenes, then edit what it wrote.
7. On **Generation**, click **Make the missing**: each scene is written,
   rendered, reviewed and fixed, a few at a time, without stopping to ask.
   Watch the previews, then approve them (**Approve N passed** does it in bulk).
8. **Render video** from Studio or Reviewing.
9. On **Export**, click **Build export** for the transcript, chapters and
   description — and for a straight answer about whether it is ready.

Rendering in the app uses the recommended voice, which out of the box is Edge
TTS and needs a network connection. To render with no narration at all, for
checking structure and timing, use
`uv run pipeline render <project> --voice-provider silent`.

---

## Using the app

**Every stage has its own address.** `/scene-plan/<project>` opens that project on
the Scene Plan, so a URL can be bookmarked, reloaded or sent to someone. The browser's
back and forward buttons move between stages.

**Inputs.** Expand any file row to see the file as it is: a PowerPoint deck is
drawn slide by slide in the browser, a Word document with its own formatting,
markdown and text as written. Nothing is converted on the server; the file you
view is the file that moves on to the next stages.

**Extraction.**

- **Tick or untick files** to choose what gets extracted. The choice is saved
  with the project. A file you leave out is labelled as left out and is never
  reported as missing; a newly uploaded file is included by default.
- **The run bar says when the extraction is out of date**: a file added since
  the last run, a file removed, a file unticked that is still in the extraction,
  or a changed option.
- **Preview** shows the selected file itself; **Extracted text** shows what was
  parsed, with figures drawn as images.
- **Extract slide layout** records, for every slide in a deck, where each
  title, picture and text box sits -- as fractions of the slide, so it survives
  into a video of any shape -- along with font size, weight and stacking order.
- **Extract background images** records what is behind each slide — a picture,
  saved like any other image, or a colour — looked up the way PowerPoint looks
  it up: slide, then layout, then master, then the theme.
- **Extract styling** records the theme's colour scheme, its heading and body
  fonts, and the slide proportions.
- **Extraction review** is the Extraction agent checking its own output. Every
  extracted picture is opened and measured first — missing, corrupt, blank,
  tiny and hairline images are facts, found without a model and identically
  every run. Then, if you leave *Have the agent read it* ticked, the agent reads
  the extracted text for what measuring cannot see: a section that stops
  mid-sentence, a table that lost its shape, a reference to a figure nobody
  extracted.
- **Each finding says where it is** and shows the picture itself. **Upload a
  picture** puts your own image in place of a broken one; **Draw a picture** has
  an image model draw one from the figure's caption and the text around it. Both
  are recorded as what they are — `uploaded` or `generated`, never as the
  author's own figure — and the next extraction run takes the picture from the
  source document again. **It is fine** dismisses a finding for good, and
  re-reviewing does not raise it again.

**Scene Plan.**

- **A conversation with the planning agent.** Say what the video should be. The
  setup beside it is sent with every message:
  - the length in your own words ("about 1 hr, longer if needed, never shorter")
  - how strictly the slides' order is kept: Strict, Nearly strict, Loose or Free
  - an optional audience
  - the language
- **The agent proposes the shape:** the length as it understood it, then each
  section's slides, minutes and scene count. Agree, or reply with what to
  change. Nothing changes until you agree; then each new or changed section is
  broken into its scenes, one call per section, with the count stated first.
- **The slides' order is held by code.** Under Strict, a shape that puts a later
  slide first is sent back with the exact problem, and a saved plan that breaks
  it cannot be transferred.
- **The Plan tab** shows what was agreed. Edit each section's slides, title and
  pictures, and each scene: what it does, its slides and its seconds.
- **The plan owns the scenes.** Script & Staging writes exactly these scenes,
  and Generation draws one per scene.

**Assets & Design.**

- **Gather pictures** reads every figure the extraction holds, measures it, and
  says where it came from. A decision — *Use* or *Skip*, with a one-line reason
  — is keyed to the picture itself, so re-running extraction keeps it.
- **Decoration is named rather than hidden.** Anything under 64 pixels a side
  is marked as decoration and left out of "would be shown", but it is still
  listed: a small picture is usually a bullet and occasionally a diagram.
- **The look** is the source deck's own: its colours, heading and body fonts,
  proportions and background. It is on by default, so the video looks like the
  course it comes from; turn it off on Assets & Design for the renderer's own theme.

**Generation.**

- **Every scene is a program the model makes.** Not a choice of slide, picture or
  chart: one screen, drawn in time with the narration, where things come on as
  the words name them, some stay, some go, and new things arrive into what is
  there.
- **A short loop, not a conversation.** Write the program, render it, run the
  checks, have the frames reviewed by a vision model, then fix a few lines (or
  the whole file) — each round one model call, asked afresh from the brief, the
  file as it is and what the last round found. It is done when the checks pass
  *and* the review says the scene teaches, its motion explains, and it looks
  finished. The slide's pictures are described once, and the last three scenes
  are summarised, so scenes stay consistent.
- **It never stops to ask.** Where the brief is silent it decides and says what
  it assumed. A scene still below the bar after 6 rounds is not given more of
  the same: it starts over with a different shot (4 rounds), then has its
  picture repainted from the reviewer's notes and starts over again (4 more).
  Only then is it made from its best version, with any failing checks and the
  reviewer's remaining remarks shown, and named on Export as *below the quality
  bar*. If no round drew anything, a plain stand-in is drawn, and only when not
  even that makes a clip is it marked *could not be made*. You change a scene by
  saying what to change.
- **It looks made from the deck.** Every scene is offered every picture the
  deck holds -- the ones its brief names, then its own slide's, the slide
  itself, its section's, then the rest -- each with what it is, what it is good
  for and which scenes already show it. Nothing is withheld for being small,
  cropped or decorative: that is said, and the agent decides. A figure is a
  scene's subject; the deck's own art opens a topic behind its title (the
  `opener` shot). Generation and Export say how many of the deck's pictures the
  video shows, and which it does not.
- **What the deck does not show is found, drawn or painted.** The script says,
  scene by scene: `PHOTO:` searches Wikimedia Commons and Openverse, keeping
  only public domain, CC0, CC BY and CC BY-SA pictures, and a vision model picks
  the one that is right (or it is painted instead); `ICON:` takes an icon from
  Iconify's openly licensed sets, or the bundled Lucide set offline;
  `ILLUSTRATE:` paints one. Each is credited in `export/credits.md`.
- **It chooses the renderer.** A web page (GSAP, D3, three.js, anime.js) for rich
  motion, charts and 3D; Revideo for physical, spring motion and typeset maths;
  Manim for diagrams and flows; matplotlib for a chart.
- **Fixed checks decide whether a clip may be used.** Text inside the frame, no
  overlap, contrast, size, no paragraph, only words the narration or source
  supports, no line through words, no box over another, the frame used, the
  section's picture used, the idea
  pictured, motion that explains, no blank frame, the right length. Then you
  approve it; the render refuses what is not approved.
- **The narration is never on screen.** It is being spoken; printing it as well
  is what makes output read as slides with a voice over them.
- **What is happening is on the page.** A status bar across every scene, a card
  per scene with what is happening now and which round it is on, and, on a scene,
  the steps taken, the reviewer's remarks, a box to say what to change, and a
  Stop button; **Stop all** stops everything, deleting nothing.
- **Making is the only AI, and the page asks first.** Setting the scenes up again
  and approving use no model; making and remaking do.
- **The details** are in
  [docs/operations/generation-sop.md](docs/operations/generation-sop.md) and
  [docs/operations/scene-programs-sop.md](docs/operations/scene-programs-sop.md).

**Script & Staging.**

- **Scenes, not a wall of text.** Each scene is what is said plus a brief of
  what is on screen while it is said. The video speaks the scenes in order, and
  a slide never runs across two of them.
- **The slides are the direction.** Narration covers every point on its slides,
  in its own words, and may explain them -- terms, context, examples,
  comparisons -- but not lead away to topics, stories or people they do not
  point toward. Each drafted section is checked against its slides and the
  agent revises it from what the check found (points missed, sentences that lead
  away or are wrong), round after round until nothing is left -- up to three
  rounds. What it keeps on purpose it says why, and the next check reads the
  reason. A slide that is itself wrong is listed apart, for you to decide; only
  what is left after the rounds is listed as a warning.
- **Draft this section** writes one section from its own source text;
  **Draft all unwritten** writes every empty section at once and never touches
  narration that is already written -- including anything typed while it runs.
- **Beside the editor** is everything the section was planned with: its summary,
  target length, how it will be shown and why, its planned scenes, its source
  text, and any review comment routed back to Script & Staging for it.
- **Out of date** marks narration written against a plan section or a source
  that has changed since. **Keep narration as is** records that you checked it.
- **Stranded narration** -- written for a section the plan no longer has -- is
  shown with the text itself, to reattach to a section or delete. It is never
  discarded quietly.
- **Variables** written as `{{NAME}}` are filled wherever the words go: the
  spoken audio, the subtitles, the timeline and the transcript. One that is not
  defined is spoken as written, and said so.

**Script & Staging and Reviewing warnings.** A section whose narration runs more than
25% past its planned length is flagged on both pages. Reviewing shows every
warning, not only open comments, before calling a project ready.

**Export.**

- **Build export** writes `transcript.md` (every spoken word under its section),
  `chapters.txt` (`0:00 Title` per line, ready to paste into a video host),
  `description.md` (audience and chapters from the plan) and, when the video
  uses pictures from outside the deck, `credits.md` (each with its author,
  source and licence), then lists them beside the rendered video and its
  subtitles.
- **It says what would make the hand-over wrong** before it says anything else:
  a timeline built from an abandoned script, a section with no narration, a
  video file that is no longer on disk. Open comments are reported as warnings,
  not blockers — whether one stops a hand-over is your judgement.
- **It never refuses.** A project with problems still gets its files, with the
  problems named: withholding the transcript does not make the video better, and
  someone checking what is wrong needs to read it.

**A cut that no longer matches its script is flagged.** Studio and Reviewing
compare the timeline and the chapters against the current plan and say so when
they describe sections it no longer has, so a project cannot look finished while
its video was built from an abandoned script. Studio offers to
empty the timeline so the next render rebuilds it.

**A job asks first.** A render, and making scenes, start only when the machine is
ready: ffmpeg, ffprobe and uv on PATH, free disk and memory, folders that can be
written. When it is not, the job says what is short and how to fix it, and a queued
render waits and starts by itself once it is. `pipeline doctor` (or
`GET /api/doctor`) runs the same checks on demand; `--deep` (`?deep=true`) also
encodes a second of video, runs Manim, and calls the model, the vision model and
the voice once each.

**Renders are versions.** Each render gets its own file name, so choosing a
past version plays that cut. Chapters and the Studio timeline are rebuilt from
each render unless you have edited them by hand, in which case your edits are
kept.

---

## Configuration

Settings are read from environment variables or `.env` in the repository root.
The **API keys** panel in the app edits the model settings for you; you can also
use `uv run pipeline credentials set LLM_API_KEY`, which reads the value from
stdin.

| Variable | Default | Purpose |
| --- | --- | --- |
| `LLM_API_KEY` | — | Key for the text model, used by every agent. |
| `LLM_BASE_URL` | `https://api.tokenrouter.com/v1` | Any OpenAI-compatible endpoint. |
| `LLM_MODEL` | `deepseek/deepseek-v4-flash` | Model id as the provider spells it. |
| `IR_LLM_API_KEY`, `IR_LLM_BASE_URL`, `IR_LLM_MODEL` | text model's values | A separate provider for structured output (drafted plans and scripts). |
| `IMAGE_MODEL`, `IMAGE_BASE_URL`, `IMAGE_API_KEY` | `google/gemini-2.5-flash-image`, text model's values | The model that draws a replacement for a figure that did not extract. |
| `VISION_MODEL`, `VISION_BASE_URL`, `VISION_API_KEY` | `google/gemini-3.5-flash`, text model's values | The model that looks at pictures: the Extraction agent reading slides, the slide pictures described for Generation, every review of a scene's frames, and handwriting OCR. The text model cannot see. |
| `LLM_TIMEOUT_SECONDS` | `600` | Per-request timeout. |
| `LLM_REQUESTS_PER_MINUTE` | `28` | How many model calls are sent in a minute, across the whole app (TokenRouter allows 30). |
| `SCENE_AGENTS_AT_ONCE` | `4` | Scenes made side by side on Generation. |
| `SCENE_RENDERS_AT_ONCE` | `2` | Scenes rendering at the same moment; rendering is what uses the memory. |
| `LLM_MAX_RETRIES` | `3` | Retries on transient failures. |
| `PROJECTS_DIR` | `./projects` | Where project data is stored. |
| `PIPELINE_TEMP` | `./.cache/tmp` | Where working files go. Kept off the system drive: when that filled up, Windows also ran short of memory. |
| `TTS_API_KEY`, `TTS_BASE_URL`, `TTS_MODEL` | model `tts-1` | For the OpenAI-compatible voice. |
| `HUGGINGFACE_API_KEY` | — | For the Hugging Face Inference API voice. |
| `ELEVENLABS_API_KEY` | — | For the ElevenLabs voice. |

Structured output uses JSON mode rather than forced tool calls, because some
reasoning models reject `tool_choice: required`.

---

## Narration voices

`uv run pipeline voices` lists every provider and whether it is ready on this
machine. The web app renders with the first ready provider other than Silent and
has no voice picker yet; to choose one, render from the command line with
`--voice-provider` (and `--voice` for a specific voice).

| Key | Runs | Setup |
| --- | --- | --- |
| `silent` | nowhere | Nothing. Silence of the estimated length, for checking timing. |
| `edge` | network (Microsoft) | Nothing; installed by default. Free, no account. Sends narration text to Microsoft. |
| `kokoro` | locally | `uv sync --extra audio` (about 1–2 GB; slow without a GPU). |
| `piper` | locally | `uv add piper-tts` |
| `huggingface_local` | locally | `uv add transformers torch` |
| `huggingface_api` | network | `HUGGINGFACE_API_KEY` |
| `openai_compatible` | network | `TTS_API_KEY`, optionally `TTS_BASE_URL` |
| `elevenlabs` | network | `ELEVENLABS_API_KEY`; billed per character |

---

## Command line

Every command prints JSON; add `--pretty` to indent it.

```bash
uv run pipeline serve [--host 127.0.0.1] [--port 8000] [--reload]

uv run pipeline stages
uv run pipeline projects list
uv run pipeline projects create "Neural Signals"
uv run pipeline projects show neural-signals

uv run pipeline show neural-signals plan              # print an artifact
uv run pipeline set neural-signals plan --file plan.json

uv run pipeline plan add-section neural-signals --title "Electrodes" --seconds 90
uv run pipeline plan show-draft neural-signals        # the pending drafted plan
uv run pipeline plan accept-draft neural-signals      # all of it...
uv run pipeline plan accept-draft neural-signals --section <drafted-section-id>   # ...or some
uv run pipeline plan discard-draft neural-signals
uv run pipeline script write neural-signals --section <section-id> --body "..."
uv run pipeline studio add-clip neural-signals --track <track-id> --text "..."
uv run pipeline review comment neural-signals --body "Too fast" --at-ms 42000 --route script-staging
uv run pipeline review seed-chapters neural-signals

uv run pipeline agent ask neural-signals scene-plan --question "What is missing?"
uv run pipeline agent draft-plan neural-signals --instruction "Aim for eight minutes"   # kept as a draft
uv run pipeline agent draft-script neural-signals --section <section-id>
uv run pipeline agent draft-unwritten neural-signals    # every section with no narration

uv run pipeline voices
uv run pipeline render neural-signals --voice-provider edge
uv run pipeline doctor [--deep]                          # is this machine ready for a job?
uv run pipeline model
uv run pipeline credentials show
```

Artifacts are `extraction`, `plan`, `script`, `composition` and `review`.

---

## MCP server

`uv run pipeline mcp` serves the pipeline over MCP (stdio), so an agent client
can operate it directly with typed tools. Add it to a client like this:

```json
{
  "mcpServers": {
    "explainer-pipeline": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/acedemic-explainer-video-pipeline", "pipeline", "mcp"]
    }
  }
}
```

Tools: `describe_stages`, `list_projects`, `describe_project`, `create_project`,
`read_artifact`, `write_artifact`, `add_plan_section`, `write_section_script`,
`add_clip`, `add_review_comment`, `seed_review_chapters`, `ask_stage_agent`,
`draft_plan`, `accept_plan_draft`, `discard_plan_draft`, `draft_section_script`,
`draft_unwritten_sections`, `list_voices`, `render_video`, `check_readiness`, `model_status`.

No tool can read an API key or delete a project. A drafted plan is kept as a
pending draft, so one drafted from MCP or the command line can be reviewed on the
Scene Plan page, and the other way round.

> **Not every feature is in every client yet.**
>
> - **Web app only:** uploading source files, running extraction, choosing which
>   files are extracted, and the Orchestrator with its conversations.
> - **Command line and MCP only:** asking a single stage agent directly.

---

## Agents

Each stage with an agent has a definition at `agents/<stage>/AGENT.md`:

```markdown
---
name: Scene Plan
role: Decide what gets taught, in what order, and which tool renders each part.
tools: [read_extraction, web_search, choose_renderer, estimate_duration]
---

# Scene Plan

Instructions, in markdown...
```

- **The markdown body is the system prompt.** Changing how a stage behaves
  means editing this file, not code. Each stage's **Agent & instructions**
  button edits it from the app.
- **Projects override, never edit, the defaults.** An edit made for one project
  is saved to `projects/<project>/agents/<stage>/AGENT.md` and leaves every other
  project alone.
- **`tools` is a declaration.** Stage agents are told that their tools do not
  execute yet, so they do not claim to have used them. The Orchestrator's tools
  (`consult_agents`, `read_artifact`, `inspect_pipeline`) do run.
- **The Orchestrator** is defined at `agents/orchestrator/AGENT.md`. It gathers
  in at most two rounds, with at most five agent calls per round, and every
  answer lists the agents it consulted.

Agents work from the extracted source text, not from file names. The Scene Plan
agent reads all of it when drafting: every heading first, then each section's
own text. The Script & Staging agent writes a section as scenes from the content that
section records, and is also shown the whole plan in compact form and the
narration on either side of its section, so what it writes joins up with its
neighbours; for a section with no recorded sources, it falls back to the
extracted text, limited to the first 40,000 characters.

---

## Where project data lives

Files are the source of truth. There is no database; delete a file and that
stage is back to empty.

```text
projects/<project>/
├── project.json
├── sources/                    uploaded documents, unchanged
├── extraction/
│   ├── content.json            structured blocks per document
│   ├── review.json             what the checks and the agent found wrong
│   └── assets/                 extracted figures, stored once per image
├── assets/library.json         which pictures to use, and the video's look
├── scene-plan/plan.json
├── script-staging/script.json
├── generation/
│   ├── visuals.json            one entry per scene: its clip, its approval
│   └── scenes/                 one folder per scene: its program, brief, checks,
│                               agent record, clip, preview and frames
├── studio/composition.json
├── reviewing/
│   ├── review.json             comments, chapters, versions
│   └── output/                 rendered .mp4, .srt, .vtt and narration audio
├── export/
│   ├── manifest.json           what was exported, and what would make it wrong
│   ├── transcript.md           every spoken word, under its section
│   ├── chapters.txt            0:00 Title, per line
│   └── description.md          audience and chapters
├── drafts/plan.json            a proposed shape waiting to be agreed to or discarded
├── settings/                   stage options and which files are extracted
├── agents/conversations.json   threads with the Orchestrator
└── agents/<stage>/AGENT.md     per-project agent overrides, if any
```

`projects/` is gitignored: it holds your documents and renders, not code.

---

## Architecture

**One core, three clients.** All behaviour lives behind `pipeline.operations`.
The web app, the command line and the MCP server are thin clients of it, so a
rule enforced in one place (validation, hand-edit protection, audits) applies to
every client.

`operations.py` itself is the *surface*: imports and `__all__`, no logic. The
verbs sit in modules beside it, in a strict dependency order (core → freshness → presentation → the stage verbs), and
tests enforce both that order and that nothing imports the surface back. Clients
still import from `pipeline.operations` and never need to know which module a
verb lives in.

```text
src/pipeline/
├── operations.py        the surface every client imports: re-exports, no logic
│   ├── core.py          finding a project and its artifacts
│   ├── freshness.py     whether an artifact still matches what it was built from
│   ├── presentation.py  how an artifact is handed to a client, with its audit
│   ├── extraction_run.py  running extraction and the settings behind it
│   ├── authoring.py     the verbs that edit an artifact on your behalf
│   └── render_run.py    rendering, and everything measured from the narration
├── web/                 Litestar app, routes, and the browser UI (static/)
├── cli.py               the `pipeline` command
├── mcp_server.py        MCP tools over the same operations
│
├── stages.py            the six stages: order, blurbs, what each produces
├── sources.py           upload validation and streaming
├── extraction.py        document readers (pdf, docx, pptx, md, txt) and figures
├── extraction_review.py checks on what was extracted, and the agent's reading of it
├── planning.py          the Scene Plan's model and store
├── scripting.py         the script: scenes, variables, length checks
├── assets.py            the picture library and the video's look
├── generation.py        one entry per scene of the script; the order and the transfer
├── scene_maker.py       making one scene: write, render, review, edit
├── scene_agent.py       the queue: scenes a few at a time, in order; stop; what the page shows
├── scene_lab.py         a scene's folder: running it, checking it, approving it
├── scene_checks.py      the fixed checks on a scene's clip
├── scene_web.py, scene_revideo.py   the web and Revideo renderers
├── scene_review.py      the vision review of a scene's frames
├── exporting.py         the transcript, chapters and description
├── composition.py       tracks and clips
├── review.py            comments, chapters, versions
├── rendering.py         audio-first rendering with Pillow frames and ffmpeg
├── speech.py            narration voice providers
│
├── agents.py            AGENT.md parsing and project overrides
├── agent_runtime.py     running a stage agent with its project context
├── orchestrator.py      the master agent: parallel consultations, bounded rounds
├── conversations.py     what was asked of the Orchestrator, and what it answered
├── plan_drafting.py     drafting a plan in two passes: every heading, then each section
├── script_drafting.py   writing a section as scenes, from that section's source
├── llm.py               model clients (text and structured output)
├── tools.py             the tool and resource catalogue agents may be granted
├── stage_options.py     per-stage options
├── credentials.py       `.env` editing behind the API keys panel
├── projects.py          project store and stage status
└── storage/             atomic JSON documents and artifact paths
```

**Audio is the clock.** Narration is synthesised first and measured; one timing function then drives the
picture, the subtitles and the Studio timeline, so the three cannot disagree.

**The browser UI** is plain ES modules with no build step. One stylesheet per
page sits in `web/static/styles/`, loaded after the base they share — a request
each, deliberately, because knowing where to change a page's look is worth more
here than the request is. The base keeps any rule a later shared rule overrides,
so splitting the stylesheet did not change a single pixel. Viewing documents
uses three vendored libraries under `web/static/vendor/`: pptx-preview 1.0.7
(ISC), [docx-preview](https://github.com/VolodymyrBaydalka/docxjs) (Apache 2.0)
and JSZip 3.10.2 (MIT or GPLv3). They are vendored rather than loaded from a CDN
so the app works offline.

---

## Development

```bash
uv sync                                   # includes the dev group

uv run pytest                             # Python tests
uv run pytest -m "not slow"               # the fast suite, with the smoke test
git config core.hooksPath tools/hooks     # once: lint + fast suite before each commit
uv run ruff check src tests               # lint (line length 100)
node tests/test_frontend_contracts.js     # invariants across the browser modules
node tests/test_answer_rendering.mjs      # how model answers are rendered, including escaping
```

The frontend contract checks guard things that are easy to break silently
across files: all HTTP goes through one client, HTML escaping has one
implementation, saves check that the project did not change mid-request, and
the stylesheet has no truncated rules.

Tests stand in for the model wherever behaviour does not depend on a real
provider, so the suite passes with no model key set. Rendering tests use the
Silent voice and need ffmpeg.

---

## Documentation

| | |
| --- | --- |
| [docs/README.md](docs/README.md) | Index of the documentation |
| [docs/architecture/system-map.md](docs/architecture/system-map.md) | Layers, boundaries, contracts and the rules that hold them together |
| [docs/operations/](docs/operations) | One procedure per layer: what it does and what it guarantees |
| [WORKFLOW-DIAGRAM.md](WORKFLOW-DIAGRAM.md) | The layers and what each keeps on disk |

---

## Status and known limits

Things to know before relying on it:

- **What a scene agent can use depends on what is installed.** Manim and
  matplotlib come with `uv sync`; the web renderer needs `npm install` in
  `renderers/web` (and Playwright's Chromium); Revideo needs `npm install` in
  `renderers/revideo` and Node. An agent is only offered the renderers this
  machine has.
- **Making scenes is slow and paid.** Every round is a model call (plus a
  review of the frames), and the provider limits requests per minute (TokenRouter: 30). Calls are paced under
  that limit, so a whole video takes tens of minutes; scenes are made four at a
  time (more used up this machine's memory). A render takes seconds (Manim,
  web) to about twenty seconds for a 38-second Revideo scene.
- **A scene program is not sandboxed.** Manim, matplotlib and Pillow programs
  run with your user's permissions and are not given the server's API keys, but
  can read any file you can and use the network. Web and Revideo scenes can only
  reach their own files, the animation libraries and the pictures they were
  offered.
- **Handwriting recognition needs a vision model.** Scanned or handwritten PDF
  pages are read by the model named in `VISION_MODEL`; nothing else in extraction
  calls a model.
- **Stage agents advise and draft; they do not act.** Their declared tools are
  not executable yet. The Scene Plan agent drafts plans (kept as a draft until you
  accept it); the Script & Staging agent writes narration straight into the script,
  one section or every unwritten one, from the page or from a client; the
  Extraction agent reviews what was extracted and can flag it, but the only
  repair it offers is a picture you upload.
- **A drawn picture is not the source's figure.** Drawing one is available
  where a figure failed to extract, and what it draws is marked `generated` so
  no later stage can present it as the author's own diagram. Nothing generates
  pictures on its own.
- **Slide *layout* is captured but not drawn.** The video uses the extracted
  pictures, the background, the theme colours and the fonts; where each shape sat
  on its original slide is recorded for the scene agent to read, not reproduced.
- **A duration target steers, it does not enforce.** The agent is told the
  target and a drafted plan is measured against it, but nothing cuts or pads
  material to fit: a 28-minute chapter asked to be 5 minutes produces an honest
  note, not a shorter plan. Script & Staging and Reviewing warn when narration
  runs well over its section's estimate.
- **PDF extraction is text-only.** Figures are extracted from Word and
  PowerPoint files.
- **Not every feature is in every client**, as listed under
  [MCP server](#mcp-server). The web app also has no voice picker.
- **There is no undo** beyond editing an artifact back, and deleting a project is
  permanent: its folder and everything running in it are erased.
