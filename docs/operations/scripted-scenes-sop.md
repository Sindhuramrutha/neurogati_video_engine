# SOP: Scripted scenes

A scene drawn by its own Python script. The code is `src/pipeline/scene_lab.py`
(folders, running, the checks), `scene_author.py` (the agent that writes the
scripts, and the resource library) and `web/static/scene-lab.js` (the page). The
resource library is the `resources/` folder.

## What it is for

Generation's rules give a scene a slide, a picture, a chart or words. A scripted
scene is the alternative: a script draws exactly this scene, with whatever the
scene needs: an equation that builds up, a diagram that assembles, a chart that
grows, text that arrives as it is said.

Each scripted scene is a folder:

```
generation/scenes/007-anorexia-defined-1/
  scene.py       what is on screen and when
  brief.json     what the script is told
  slide.png      the deck's slide for this scene, when it has one
  assets/        files it uses
  sources.json   every outside resource, with its licence and credit
  render.mp4     the clip it drew
  poster.png     a frame of it
  checks.json    what the checks found
  log.txt        what the script printed
  author.json    how the agent wrote it, attempt by attempt
```

## Guarantees

1. **The script is free; the checks are fixed.** The agent may use any library
   and any open resource. Whether the clip is used is decided by the same eight
   checks every time, not by the agent.
2. **A clip that fails a check is never used.** The scene stays unmade, and the
   Check tab blocks the transfer.
3. **Writing is the only AI.** At most three model calls per scene: write, then
   up to two fixes. The page says the most it can cost before it starts.
   Running and checking use no AI.
4. **Every outside resource is recorded** in `sources.json`, with its licence
   and who to credit.
5. **The render uses the transferred clip.** Transferring Generation copies the
   clip under a name taken from its content, so running a script again does not
   change a video already approved.

## A script is a program

It runs on this computer, with your permissions, in its scene's folder, with a
15-minute limit. It can read and write files and use the internet. Read a script
before trusting it with anything that matters, and only add resources you have
the right to use.

## How to do it

1. **Choose it.** On Generation's Decide tab, set a scene's *Shows* to **A
   scripted scene**, or press **Script every scene**. Nothing is written yet.
2. **Write the scripts.** On the Make tab:
   - **Write the N missing scripts** writes each in turn; or
   - open one scene and press **Write it**, with an instruction in your own
     words if you have one; or
   - paste or type `scene.py` yourself and press **Save and run**.
3. **Watch each one.** Open the scene. The clip is silent on purpose: the
   narration is added by the render. The checks prove the script runs and fits;
   they cannot say whether it shows the right thing.
4. **Change one.** Edit `scene.py` and press **Save and run**, or write what to
   change and press **Rewrite it**.
5. **Transfer** on the Final tab, as for any shot.

## The checks

| Check | Rule | If it breaks |
|---|---|---|
| The script ran | It finished without an error, inside the time limit | **Fails** |
| It made a video | `render.mp4` exists and has a picture in it | **Fails** |
| The frame is the right size | 1920×1080 | **Fails** |
| It fits the narration | 60% to 110% of the scene's length. Shorter holds its last frame; longer is cut off | **Fails** if longer, warning if shorter |
| It shows something | A frame is more than one flat colour | **Fails** |
| Something changes | The start and the end of the clip differ | Warning |
| No sound of its own | The narration is the only sound | Warning |
| Outside resources are recorded | Every file in `assets/` is in `sources.json` | Warning |

The scene's length comes from its narration: 2.5 words a second, and at least
3 seconds.

## What the script is given

- `brief.json`: the narration, the on-screen words, the headline, the length,
  the frame size and rate, the project's colours and fonts, the section's
  pictures, and the deck's slide.
- The resource library, importable by name. `scenekit` reads the brief, draws
  frames, writes the video and fetches outside resources.
- Whatever it declares at its top. The script names the libraries it needs, and
  `uv` builds an environment with exactly those. Manim, matplotlib and the rest
  need no installing by hand. The first run of a new library downloads it.

## The resource library

`resources/` is what the agent is shown every time it writes a scene.

| Folder | What goes in it |
|---|---|
| `code/` | Python the scripts can import. Start each file with a docstring saying what it is for |
| `methods/` | How-to notes and worked examples: a technique, a library's pitfalls, a house style |
| `assets/` | Pictures, icons, fonts and data |

Add to it from Generation's Setup tab, or by hand. To teach the agent a way of
doing something, add a worked example to `methods/`.

## Things to know

- **Deciding again keeps a scripted scene scripted.** If its narration was
  rewritten, it stays scripted and unmade until its script is run again.
- **Changing a scripted scene to another kind** leaves its folder where it is.
  Changing it back finds the script again.
- **LaTeX** is needed for `MathTex` in Manim. The agent is told whether this
  machine has it, and uses plain text when it does not.
