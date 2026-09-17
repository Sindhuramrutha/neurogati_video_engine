# Academic Explainer Video Pipeline

Turns written academic material (lecture notes, chapters, slide decks) into a
narrated explainer video. Each stage produces one artifact you can read and
edit, and every stage but Inputs is run by an AI agent whose instructions are a
markdown file you can change.

```text
Inputs → Extraction → Assets & Design → Scene Plan → Script & Staging →
Studio → Reviewing → Export
```

The pipeline never hides work inside a model call. Every stage's output is a
JSON file on disk, each response says what is inconsistent, and the video's
timing is measured from the narration audio rather than estimated.

---

## Contents

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
| **Scene Plan** | Sections, learning objectives, audience and key themes. Each section records the extracted content it covers, how it should be shown and why, and which objectives it serves. The Planning agent drafts a plan from the whole extraction; the draft is reviewed next to your plan and accepted whole or section by section. Warns when the extraction has changed since the plan was made. | `planning/plan.json` |
| **Script & Staging** | Each plan section written as **scenes**: what is said, and a brief of what is on screen while it is said. The Scripting agent drafts one section or every unwritten one at once, from that section's own source text. Beside the editor sit the section's plan details, its source text and any review comments. Flags narration written against a plan section or source that has changed since, and narration whose section the plan no longer has. `{{VARIABLES}}` are filled everywhere they are spoken or shown. | `scripting/script.json` |
| **Studio** | A multi-track timeline with playback, seeking and clip properties. Rendering synthesises the narration, measures each section's real audio length, and cuts the picture to fit. | `studio/composition.json` |
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
7. **Render video** from Studio or Reviewing.
8. On **Export**, click **Build export** for the transcript, chapters and
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
- **Options marked "not built yet"** are declared but not read by anything yet,
  so they are disabled. Everything else on this page works.
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

- **Draft plan** has the Scene Plan agent read the whole extraction in two passes:
  every heading of every document first (with a few words of any untitled slide
  or page), then each section from its own full text. Optional guidance steers
  it. Drafting takes a minute or two and is kept as a draft even if you leave.
- **The draft appears next to your plan.** **Accept all** replaces your sections,
  objectives and key themes; **Add to plan** appends one section and brings its
  objectives with it; **Discard** throws the draft away. Your plan never changes
  until you choose. Notes list anything the agent could not match to the
  extraction, and any part of the source no section covers.
- **Each section records** the extracted content it covers, how it should be
  shown (composition, plot, simulation, code or still) with a one-line reason,
  and the learning objectives it serves. All of it is editable in the section
  editor, where sources are picked from the extraction's headings.
- **The bar at the top** says whether the plan matches the current extraction.
  It warns when the extraction has changed since the plan was drafted, flags
  sections whose source content is no longer extracted, and reports a plan that
  is not linked to the extraction at all. **Keep plan as is** records that you
  checked it.
- **Objectives show coverage**: which sections serve each one, or "not covered".

**Assets & Design.**

- **Gather pictures** reads every figure the extraction holds, measures it, and
  says where it came from. A decision — *Use* or *Skip*, with a one-line reason
  — is keyed to the picture itself, so re-running extraction keeps it.
- **Decoration is named rather than hidden.** Anything under 64 pixels a side
  is marked as decoration and left out of "would be shown", but it is still
  listed: a small picture is usually a bullet and occasionally a diagram.
- **The look** is the source deck's own: its colours, heading and body fonts,
  proportions and background. It is off by default — a video that silently
  adopted a client's brand colours would be worse than one that asked.

**Script & Staging.**

- **Scenes, not a wall of text.** Each scene is what is said plus a brief of
  what is on screen while it is said. The video speaks the scenes in order, and
  a slide never runs across two of them.
- **Draft this section** writes one section from its own source text;
  **Draft all unwritten** writes every empty section at once and never touches
  narration that is already written -- including anything typed while it runs.
- **Beside the editor** is everything the section was planned with: its summary,
  target length, how it will be shown and why, the objectives it serves, its
  source text, and any review comment routed back to Script & Staging for it.
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
  `chapters.txt` (`0:00 Title` per line, ready to paste into a video host) and
  `description.md` (audience, objectives and chapters from the plan), then lists
  them beside the rendered video and its subtitles.
- **It says what would make the hand-over wrong** before it says anything else:
  a timeline built from an abandoned script, a section with no narration, a
  video file that is no longer on disk. Open comments are reported as warnings,
  not blockers — whether one stops a hand-over is your judgement.
- **It never refuses.** A project with problems still gets its files, with the
  problems named: withholding the transcript does not make the video better, and
  someone checking what is wrong needs to read it.

**A cut that no longer matches its script is flagged.** Studio and Reviewing
compare the timeline and the chapters against the current plan and say so when
they describe sections it no longer has — the failure that let a project look
finished while its video was built from an abandoned script. Studio offers to
empty the timeline so the next render rebuilds it.

**Renders are versions.** Each render gets its own file name, so choosing an
older version plays that cut. Chapters and the Studio timeline are rebuilt from
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
| `LLM_TIMEOUT_SECONDS` | `600` | Per-request timeout. |
| `LLM_MAX_RETRIES` | `3` | Retries on transient failures. |
| `PROJECTS_DIR` | `./projects` | Where project data is stored. |
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
`draft_unwritten_sections`, `list_voices`, `render_video`, `model_status`.

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
├── studio/composition.json
├── reviewing/
│   ├── review.json             comments, chapters, versions
│   └── output/                 rendered .mp4, .srt, .vtt and narration audio
├── export/
│   ├── manifest.json           what was exported, and what would make it wrong
│   ├── transcript.md           every spoken word, under its section
│   ├── chapters.txt            0:00 Title, per line
│   └── description.md          audience, objectives and chapters
├── drafts/plan.json            a drafted plan waiting to be accepted or discarded
├── settings/                   stage options and which files are extracted
├── agents/conversations.json   threads with the Orchestrator
└── agents/<stage>/AGENT.md     per-project agent overrides, if any
```

Two stages were renamed once their scope was clear: **Planning → Scene Plan**
and **Scripting → Script & Staging**. A project written under the old names is
moved to the new folders the first time it is opened, and the old stage keys
still resolve — so routed comments, saved settings and old bookmarks keep
working.

`projects/` is gitignored: it holds your documents and renders, not code.

---

## Architecture

**One core, three clients.** All behaviour lives behind `pipeline.operations`.
The web app, the command line and the MCP server are thin clients of it, so a
rule enforced in one place (validation, hand-edit protection, audits) applies to
every client.

`operations.py` itself is the *surface*: imports and `__all__`, no logic. It once
held seventeen hundred lines and fifty-eight functions, at which point "one core"
had become "one file everything is in" — the failure it exists to prevent,
reached from the other direction. The verbs now sit in modules beside it, in a
strict dependency order (core → freshness → presentation → the stage verbs), and
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
├── stage_options.py     per-stage options, and whether each is built
├── credentials.py       `.env` editing behind the API keys panel
├── projects.py          project store and stage status
└── storage/             atomic JSON documents and artifact paths
```

**Audio is the clock** ([ADR 0001](docs/decisions/0001-preserve-audio-first-timing.md)).
Narration is synthesised first and measured; one timing function then drives the
picture, the subtitles and the Studio timeline, so the three cannot disagree.

**The browser UI** is plain ES modules with no build step. Viewing documents
uses three vendored libraries under `web/static/vendor/`: pptx-preview 1.0.7
(ISC), [docx-preview](https://github.com/VolodymyrBaydalka/docxjs) (Apache 2.0)
and JSZip 3.10.2 (MIT or GPLv3). They are vendored rather than loaded from a CDN
so the app works offline.

---

## Development

```bash
uv sync                                   # includes the dev group

uv run pytest                             # Python tests
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
| [docs/README.md](docs/README.md) | Design documentation: why v2 exists and how it is organised |
| [docs/fundamentals/](docs/fundamentals/) | What the system is, and the quality model |
| [docs/diagnosis/v1-postmortem.md](docs/diagnosis/v1-postmortem.md) | What went wrong in v1 |
| [docs/design/](docs/design/) | Architecture options, tech stack, interfaces, data layout, agentic stack |
| [docs/decisions/](docs/decisions/) | Architecture decision records |
| [docs/open-questions.md](docs/open-questions.md) | Unresolved questions |

Decision records. Every record is still marked **Proposed** in its own file;
the last column says only what the code shows today.

| ADR | Decision | In the code today |
| --- | --- | --- |
| [0001](docs/decisions/0001-preserve-audio-first-timing.md) | Audio-first timing | Rendering measures the narration, then cuts the picture to it. |
| [0002](docs/decisions/0002-structured-output-over-free-text.md) | Structured output over free text | Drafted plans and narration come back as validated objects. |
| [0003](docs/decisions/0003-durable-incremental-state.md) | Durable, incremental state | — |
| [0004](docs/decisions/0004-mechanical-checks-before-human-review.md) | Mechanical checks before human review | — |
| [0005](docs/decisions/0005-files-as-source-of-truth.md) | Files as the source of truth | No database; every artifact is a JSON file. |
| [0006](docs/decisions/0006-langgraph-as-backbone.md) | LangGraph as the orchestration backbone | Installed as a dependency, not imported anywhere. |
| [0007](docs/decisions/0007-revideo-as-rendering-target.md) | Revideo as the rendering target | Not built; rendering uses Pillow and ffmpeg. |

---

## Status and known limits

This is an early working version. Things to know before relying on it:

- **Videos are plain.** Each section is a title card followed by its narration
  as text slides, which is honest about the content but not yet visual. Figures
  are extracted but not yet placed in the video, and the Studio graphics track
  is empty.
- **Some options are placeholders.** Extraction mode, output format, key-field
  detection, handwriting OCR, and every Scene Plan preference (duration, tone,
  language) are shown as "not built yet" and change nothing.
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
- **A section's rendering approach is recorded but not yet used.** The renderer
  still draws every section as text slides, whatever the plan chooses.
- **Slide layout, backgrounds and styling are captured but not yet drawn.**
  Extraction records where everything sits on a slide, what is behind it, the
  theme colours and the fonts; nothing renders from them yet, and a scene's
  on-screen brief is text the renderer does not read either.
- **The Scene Plan does not target a duration.** The plan's lengths are whatever the
  plan says; Script & Staging and Reviewing warn when narration runs well over them.
- **PDF extraction is text-only.** Figures are extracted from Word and
  PowerPoint files.
- **Not every feature is in every client**, as listed under
  [MCP server](#mcp-server). The web app also has no voice picker.
- **There is no undo** beyond editing an artifact back, and nothing deletes a
  project for you.
