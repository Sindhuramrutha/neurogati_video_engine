# SOP: Generation

What this layer does, in what order, and what it guarantees. The code is
`src/pipeline/generation.py` (one scene per scene of the script),
`scene_agent.py` and its neighbours (the agents that make each scene),
`scene_lab.py` (running, checking and approving a scene) and
`generation_handoff.py` (the checks and the frozen transfer). The page is
`web/static/stage-generation.js` and `scene-lab.js`.

## What the layer is for

Every scene of the script becomes a **scene program**: a small program, written
by a short loop (write, render, review, fix), that draws one screen of the video in time with its narration.
Things come onto the screen as the narration names them; some stay, some go,
and new things arrive into what is already there, until the scene ends. The
render reads the clips these programs make.

The full account of a scene program, how it is made and its checks is in
[scene-programs-sop.md](scene-programs-sop.md). This page is the layer around
them.

## Guarantees

1. **Every scene is a program, made by a short loop.** There is no shot to choose
   (a slide, a picture, a chart, words): every scene is drawn by its own
   program. The deck's slide and the section's pictures are material the
   program may use, never the shot.
2. **Nothing is used until it is approved.** A scene's clip must pass every
   fixed check, and then a person approves it. The render refuses a scene that
   is not an approved program, and never falls back to a still.
3. **Making says what it will cost.** Making is paid model calls, and the page
   asks before starting them. Setting the scenes up again, and
   approving, use no model.
4. **The render reads frozen, transferred clips.** A transfer copies every
   clip it points at under a name taken from its content, so making a scene
   again cannot change a video already approved until you transfer again.
5. **Nothing is hidden.** What was done to a scene, round by round, the checks and their
   results are all on the page.

## The three tabs

### 1. Setup

- **What came in:** whether the script and Assets & Design are transferred.
  Transfer them first, so the scenes are made from fixed inputs.
- **Pictures handed on:** how many of the plan's pictures can be a scene's
  picture (large and clear enough to fill a frame). A scene shows only the
  pictures attached to its own section on Scene Plan.
- **What this machine can draw:** which renderers are installed and working.
- **The resource library:** the code, method notes and assets every agent is
  shown.

### 2. Make

One panel, then the status bar, then one card per scene, in the order of the
video.

- **The panel** says how many scenes passed, how many are still to make, and
  what is happening. Its buttons:
  - **Make the N missing:** makes every scene without a passing clip, in the
    video's order, a few at a time on the server.
  - **Stop all** (while scenes are being made): the ones being made stop after
    their round, and the queue is dropped. Nothing is deleted; **Make the
    missing** resumes them. One scene can be stopped on its own panel.
  - **Approve N passed:** approves every scene whose program passed, after you
    confirm. It does not mean you watched them.
  - **Set up again:** reads the transferred script again and says how many
    scenes are new, rewritten, removed and unchanged. Unchanged scenes keep
    their programs. No model is called.
  - **Remake all:** every scene is made again from nothing. It asks first,
    because every scene, approved ones included, is paid for.
- **The status bar** is one bar across all scenes, coloured by where each is:
  approved, passed (to watch), being made, queued, stopped or failed, not
  started. It refreshes itself while agents work.
- **A card** shows the scene's poster, its brief, and, while it is made,
  what is happening now and which round (of up to 3) it is on. Open a card for
  the scene panel: the steps taken, the reviewer's remarks, a box to say what to
  change, a Stop button, the clip, the checks, and the program.

### 3. Final & transfer

- The header says where things stand: nothing to transfer, N checks fail, ready,
  or transferred.
- **The checks before transfer** are listed at the bottom of this tab:

| Check | Rule | If it breaks |
| --- | --- | --- |
| Shots match the script | One scene per scene of the transferred script | **Fails**: set the scenes up again |
| Every scene is an approved program | Each has a clip that passed every check and was approved | **Fails**: make or approve it |
| Made for the scene as written | No scene rewritten since its clip was made | **Fails**: make it again |
| Script transferred | Made from a transferred script with no changes waiting | Warning |
| Assets carried by the plan | Pictures come from the plan's transferred Assets & Design | Warning |

- **Transfer to the next layer** freezes the clips and hands them to the
  render. It is refused while a check fails.

## What making costs

A scene takes up to **3 rounds**; a round is one model call (a few-line edit
costs little) plus one vision call: a review of the frames when the checks
pass, or a look at them when a layout check fails. A scene that passes stops
there unless the reviewer names something that must change; then one more round
answers it. Every model call
waits for a place in the provider's per-minute limit (TokenRouter allows 30 a
minute, so the pace is set to 28: `LLM_REQUESTS_PER_MINUTE`), so a whole video
takes tens of minutes, not seconds. Scenes are made **four at a time**
(`SCENE_AGENTS_AT_ONCE`): more than that, with Manim and a browser rendering,
used up this machine's memory.

## If the app restarts

Making runs on the server, not in the page, and leaving the page does not stop
it. A restart does: scenes that were being made show as **interrupted**, and
**Make the missing** makes each again from its files as they are.

## Checks before transferring

- [ ] The script and Assets & Design are transferred.
- [ ] Every scene passed, and you watched each one's preview before approving.
- [ ] No scene is marked **could not be made**.
- [ ] Final & transfer lists no failing check, and says **Transferred**. Then
      render from the Render tab.
