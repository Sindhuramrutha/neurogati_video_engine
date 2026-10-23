# SOP: Scene programs and their agents

A scene is one screen. Things come onto it as the narration names them; some
stay, some go, and new things keep arriving into what is already there, until
the scene ends. Each scene of the video is drawn by its own **scene program**,
made by a short loop until it is good: write it, render it, review it, fix it.

The code:

| File | What it does |
| --- | --- |
| `scene_maker.py` | Making one scene: the loop (write, render, review, edit), and what the model is told |
| `scene_agent.py` | The queue: a few scenes at a time, in the video's order, on the server; stopping; what the page shows |
| `scene_edit.py` | Reading the model's answer, and applying a few-line edit |
| `scene_round.py` | One round: render, run the checks, review the frames |
| `scene_state.py` | What is kept about a scene's making (`agent.json`) |
| `scene_kept.py` | The version that passed, kept while the scene is changed |
| `scene_review.py` | The vision review of a render's frames, and describing a picture |
| `scene_lab.py` | A scene's folder: the brief, running, the checks, approving, the render guard |
| `scene_program.py` | The narration measured, timing, the spec, the preview, the folder names |
| `scene_checks.py` | The fixed checks |
| `scene_web.py`, `scene_revideo.py` | The web and Revideo renderers |
| `scene_author.py` | The resource library, and marking scenes as programs |
| `llm.py`, `llm_pace.py` | The model calls, and the pace they keep under the provider's limit |
| `web/static/scene-lab.js` | The page |

The resource library is the `resources/` folder.

## A scene's folder

```text
generation/scenes/007-anorexia-defined-1/
  scene.py | scene.html | scene.tsx   the program: Python, a web page, or Revideo
  brief.json     what the agent is told
  spec.json      which renderer it chose, and the beats
  layout.json    what was on screen when (text, shapes, pictures), and the animations
  checks.json    what the checks found
  agent.json     what was done, round by round, and what it cost
  kept/          the last version that passed every check, while it is being changed
  narration.mp3, narration.json   the narration, spoken once and measured
  render.mp4     the clip it drew (silent)
  preview.mp4    the clip with its narration, for watching
  poster.png, frames/   a poster, and the frames the review looked at
  slide.png      the deck's slide for this scene, when it has one
  assets/, sources.json   files it uses, and every outside resource with its licence
  log.txt        what the last run printed
```

## Guarantees

1. **The program is free; the judgement is not.** The model may use any renderer
   and any open resource. Whether its clip is used is decided by the same fixed
   checks every time, then by you.
2. **A scene is done when it is good.** Every check passes *and* a vision review
   of its frames says it teaches, its motion explains, and it looks finished.
   Anything that would only make it nicer is polish and does not block.
3. **It never stops to ask.** Where the brief is silent it decides, and says what
   it assumed. If it runs out of rounds (3), the scene is made from its best
   version, with any failing checks and the reviewer's remaining remarks shown on
   it; if no round drew anything, a plain stand-in is drawn without a model. Only
   when not even that makes a clip is it marked **could not be made**, with which
   checks. You change a
   scene afterwards, by saying what to change.
4. **A clip that fails a check is never used.** And a passing clip is not used
   until a person approves it; running a scene again withdraws its approval.
5. **Every outside resource is recorded** in `sources.json`, with its licence.
6. **The render uses the transferred clip.** Transferring copies the clip under
   a name taken from its content.

## How a scene is made

```text
write the program --> render + fixed checks --> review its frames --> edit it
       ^                                                                 |
       +-----------------------------------------------------------------+
```

Each round is **one model call**, asked afresh: it is given the scene's brief,
the file as it is now, and what the last round found. It is not given a
conversation to remember, so a round costs the same whether it is the first or
the fifth.

1. **Before round 1:** what the brief asks for that the deck does not have is
   made once and kept -- a painting (`ILLUSTRATE:`, checked for its subject,
   framing and finish, and left out if it is never right) and icons (`ICON:`,
   from the bundled set). Every deck picture is described once by the vision
   model (what it is, and whether it explains, sets the scene or is deck
   furniture); the scene's nearest pictures have their parts located as boxes
   (`picture_parts.py`), which callouts are drawn to; and the last three scenes
   of the video are summarised in a line each, so this one stays consistent.
2. **Round 1:** the model writes the whole program, and says which renderer it
   chose and what it assumed.
3. **Render:** the program is run with that renderer and every check is run. If
   a check fails, the failing checks (and what a crash printed) go back. When a
   layout check fails -- words crossed, boxes over boxes, the frame unused --
   a reviewer also looks at the frames and says what causes it and where things
   should go: the model that writes the program reads only text.
4. **Review:** if every check passed, a reviewer looks at six frames beside the
   narration. What *must* change goes back as "must fix"; the rest as "optional
   polish". A pass with only polish left ends the scene: rounds spent on polish
   broke scenes that already worked.
5. **The next round** answers with an `edit` block (lines to find, lines to put
   there) or, for a big change, the whole file. An edit whose lines are not in
   the file exactly once is sent back, not guessed at.
6. **Nothing worse replaces a pass.** Once a version passes every check it is
   kept (`kept/`). A later change that breaks a check is undone: the program,
   clip and checks go back to the version that passed, and the model is told
   what its change broke and asked to make it another way. So the rounds after
   a pass can only improve the scene, and a scene that passed once is never
   marked **could not be made**. When you ask for a change to a scene that
   passes, the scene you had is kept the same way.

Up to 3 rounds. An answer that cannot be used is asked again at once, without
a render, and still carries what the last render found. A call that fails is retried three times, waiting longer each
time, before the scene is marked **could not be made** with the reason. Every
model call waits for a place in the provider's per-minute limit
(`LLM_REQUESTS_PER_MINUTE`, 28 by default).

## The renderers

An agent chooses whichever explains the idea best.

| Renderer | Entry file | For |
| --- | --- | --- |
| `web` | `scene.html` | Rich motion: GSAP (with its MotionPath, MorphSVG, DrawSVG and SplitText plugins), D3, three.js, anime.js. Recorded frame by frame in headless Chromium |
| `revideo` | `scene.tsx` | Polished, physical (spring) motion; maths typeset without TeX; code typed in. Rendered by Revideo / Motion Canvas |
| `manim` | `scene.py` | Diagrams, labels, flows, timelines, transformations |
| `matplotlib`, `pillow` | `scene.py` | Charts; simple composed frames |

- A **web** scene can load only its own folder, the animation libraries
  installed under `renderers/web/node_modules`, `webkit.js`, and the pictures
  its brief offers. Every other request, the internet included, is refused.
- A **Revideo** scene is compiled in a working folder of its own under
  `renderers/revideo/agent/` (removed afterwards) with a `kit.ts` that gives it
  the brief, the font, `when()`, `until()` and `finish()`.
- **Manim** scenes start with `from manimkit import *`, which gives every Manim
  name and the kit. The kit fits anything with words inside the margin, moves
  new words off words, pictures and lines already on screen, and never lets an
  animation or a pause run past the end of the narration. It also turns four
  common Manim mistakes into what was meant: a picture given to `Create` fades
  in, a thing passed to `play()` without an animation is drawn in, a run time
  of zero or less plays for one frame, and `self.now()` works as well as
  `self.now`.

The kits and method notes the model is given are in `resources/code/` and
`resources/methods/`: `manimkit.py`, `scenekit.py`, `webkit.js`, `motion.md`,
`web-scenes.md`, `revideo-scenes.md`, `scene-contract.md`.

## The checks

| Check | Rule | If it breaks |
| --- | --- | --- |
| The program ran | It finished without an error, inside the time limit | **Fails** |
| It made a video | `render.mp4` exists and has a picture in it | **Fails** |
| The frame is the right size | 1920×1080 | **Fails** |
| Renderer is wired | The code uses the renderer the spec names | **Fails** |
| Length matches the narration | Within 5% of the narration's measured length | **Fails** |
| Text inside the frame, no overlap, contrast, size | Inside a 5% margin; no two pieces overlap, and none lies on a picture (it would cover the picture's own labels); contrast at least 4.5:1; lines at least 36 px | **Fails** |
| No paragraph on screen | At most 18 words in a piece, 25 on screen | **Fails** |
| On-screen text is grounded | Words and numbers come from the narration, brief or source | **Fails** |
| No shape runs through words | No visible outline crosses text, followed every 6 px; a filled shape with no outline is a panel | **Fails** |
| No shapes collide | No box, circle or other closed outline runs half through another | **Fails** |
| The frame is used | At its fullest, the scene spans 40% of the height and 50% of the width | **Fails** |
| Uses the slide's pictures | When the section has pictures, at least one is shown | **Fails** |
| It pictures the idea, not only words | At half the beats or more, at least two things on screen are not words | **Fails** |
| Motion explains | At least 3 animations transform, move, grow or draw; things coming on as they are named never count against it | **Fails** |
| No blank frame, nothing cut at an edge, three distinct moments | Sampled from the clip | **Fails** |
| No sound of its own; outside resources recorded | | Warning |

A Revideo scene does not report its text or its animations, so those checks
show a warning for it and the vision review judges them.

When a check fails, its detail says what to change, not only what is wrong: which
beats show only words, and that text measured small was shrunk after it was made
(by `.scale()`, or by fitting too much into a row), so the fix is not to shrink
something else.

## What a program is

A program runs on this computer, in its scene's folder, with a time limit. Manim,
matplotlib and Pillow programs are given only the environment variables they
need to run (never the server's API keys), but they can still read any file
your user can and use the network. It is **not a sandbox.** Web and Revideo
scenes are confined as described above. Read a program before trusting it with
anything that matters, and only add resources you have the right to use.

## How to do it

1. **Transfer** the script and Assets & Design, then open Generation's Make tab.
2. **Make the missing.** The scenes are made in the video's order, four at a
   time. You can leave the page; watch the status bar and each card.
3. **Watch each one.** Open the scene. The preview has the narration. The checks
   prove it runs and fits; the review judged whether it teaches; only you can
   say whether it is right. **Approve** it, or write what to change and press
   **Change it**: the model gets your words and the file as it is.
4. **A scene that could not be made** shows which checks still fail. Change it
   with a sentence, or make it again.
5. **Approve in bulk** with **Approve N passed** when you trust them.
6. **Transfer** on the Final tab.

## Things to know

- **Providers limit requests.** Every model call waits for a place in the
  provider's per-minute limit. A call that fails is retried three times before
  the scene stops.
- **Setting the scenes up again** keeps an unchanged scene's program. A scene
  whose narration was rewritten is unmade until it is made again.
- **LaTeX** is needed for `MathTex` in Manim. The model is told whether this
  machine has it, and uses plain text when it does not.
- **Teaching it something:** add a worked example to
  `resources/methods/`.
