# SOP: Assets & Design

What this layer holds, in what order you work through it, and what it
guarantees.

| Part | Code |
|---|---|
| The picture library | `src/pipeline/assets.py`, `figure_prep.py` |
| Brand assets | `brand_kit.py`, `brand_overlay.py`, `render_brand.py` |
| The look | `project_look.py` |
| The transfer | `assets_handoff.py` |
| The page | `web/static/stage-assets.js`, `brand-editor.js`, `look-editor.js` |

## What the layer is for

**The inventory and the look.** It shows what exists and where it came from,
lets you set aside what you don't want, holds your brand assets, and sets how
the video's own frames look.

It does not judge pictures. Whether a picture is large and clear enough to be a
scene's picture is decided in **Generation**, where a picture is chosen for a
scene. Generation's Setup tab lists any handed-on picture it cannot use, and
why.

Generation and Render read what this layer **transferred**, never what is still
being worked on.

## Guarantees

1. **No AI.** Nothing on this layer calls a model.
2. **Same inputs, same result.** Gathering depends only on the transferred
   extraction and your stored choices. A picture's id comes from its content.
3. **Nothing is done to a picture without the page saying so.** Trimming and
   the crop check each say what was done, why, when and how, and each can be
   overruled.
4. **Nothing is hidden.** A picture no longer in the extraction is named. A
   picture you left out is named on the Final tab.
5. **The preview is the render.** The logo and watermark on the page are the
   same image the render lays on, at the same place. The look's preview colours
   come from the renderer's own style.
6. **Every control does something.** A colour, a font, a slider: each changes
   the render.
7. **Only transferred work reaches later stages.**

## The four tabs, in order

### 1. Extracted assets

A project has one source file, named in the strip under the header. This
layer works on the pictures of the last Extraction transfer of it.

**Gather:** the page gathers by itself when it sees a newer transfer. **Gather
again** does it by hand. **Clear everything** empties the library, with your
choices, until you gather again.

**The pictures** are one grid, in the source's order: slide by slide for a
deck.

Each picture's card shows:

- **Where it came from**: "Slide 2 · Padma's Story". For a document that is not
  a deck, the heading it sits under.
- Its own caption, when the source gave it one.
- Its size in pixels.
- One action: **Leave out** (or **Put back**). A left-out picture is not handed
  on. Nothing else is decided here.

A card may also carry one or both of these, each with **See why**:

| Line | What | Why | When | Your say |
|---|---|---|---|---|
| **Its plain border was trimmed** | A trimmed copy was made; the original is untouched | A plain border is wasted screen on a frame | On gathering, when the border is more than 3% of the picture | **Use the trimmed copy** or **Use the original** |
| **Check the crop** | Nothing was changed | The picture touches its own edge, which often means a caption or an axis was cut | On gathering, when more than 10% of the outer 2% of an edge is not background | **It looks right**, or leave it out, or replace the picture on Extraction |

The details show the original beside the trimmed copy, and mark in red the
edges the picture touches. A picture touching all four edges is usually one
that simply fills its frame.

### 2. Brand assets

Four slots, each optional: **Watermark**, **Logo**, **Intro video**, **Outro
video**.

| Slot | Files |
|---|---|
| Watermark, Logo | PNG, JPG, WebP; at least 64 px. Use a transparent PNG |
| Intro, Outro | MP4, MOV, WebM, MKV, M4V; up to 120 s |

**On the lesson frame.** The frame is drawn in the project's look. Drag the
logo or the watermark to place it. The dashed line is the safe margin, 5% in
from every edge.

**Place and style**, for the logo and for the watermark:

| Control | Range |
|---|---|
| Where | Drag, the 3×3 snap grid (just inside the safe margin), or Across / Down in % |
| Size | 2–60% of the frame's width |
| Opacity | 5–100% |
| Rounded corners | 0–50% |
| Shadow | 0–100% |
| When it appears | The whole lesson · the first N s · the last N s · from–to |
| Fade in, fade out | 0–5 s each |

If a file is smaller than it is drawn, the page says it will look soft and how
wide a file it needs.

**Intro and outro:**

- **Cut from the start**, **Cut from the end**: trims, in seconds. A clip is
  never trimmed to less than half a second.
- **Cross-fade** with the lesson: 0–2 s, and never more than half the clip. At
  0 it is a straight cut.
- Fitted to 1920×1080 at 30 fps, letterboxed, never stretched. A silent clip
  gets silence. The whole soundtrack is levelled once.

**The timeline** shows the intro, the lesson and the outro, and when the logo
and the watermark are on screen. It is drawn for a one-minute lesson; the real
length comes from the narration.

The logo and the watermark sit on the lesson only. Subtitles, the Studio
timeline and chapters start where the lesson starts: after the intro, less the
cross-fade.

Every change saves at once. Each file is stored under a name taken from its
content, so replacing one never overwrites a file an earlier transfer uses.

### 3. Look

How the video's **own** frames are coloured and set. A slide of the deck is
always shown as its author made it.

- **Start from:** the source's own styling (when it is a deck that has some),
  or the renderer's own look (dark and neutral).
- **Theme:** ready-made starting points from the chosen deck's own palette:
  Deck's own, Light, Dark, Accent-led. A theme is only offered when the deck
  has its colours and its text reads well.
- **Colours:** Background, Panels, Accent. Click one to pick from the deck's
  colours, or any colour with the picker or a hex value. **Reset** returns it
  to the deck's own.
- **Readability:** the contrast between the text and the panel it sits on. It
  needs 4.5 : 1. Below that, the page says so. The text is dark on a light
  background and light on a dark one; the render picks it.
  - With no panel colour chosen, the panel is made to suit the background.
  - A panel colour you chose is used exactly as chosen.
- **Fonts:** headings and body text, each the deck's heading font, its body
  font, or the renderer's. A font the rendering machine lacks is replaced by
  the nearest it has.
- **Background art** (when the deck has some): a switch to draw it behind the
  frames, and three cards showing slide 1 of the deck really drawn each way:
  - *As PowerPoint shows it*: the deck's pale sheet stays over its art.
  - *Art at full strength*: the sheet is read as see-through.
  - *No sheet*: only the art is drawn.

The preview stays in view and is redrawn on every change.

### 4. Final & transfer

- **The video, as it will look:** Intro → a lesson frame in your look, with the
  logo and watermark as placed → Outro. Each join says whether it is a cut or a
  cross-fade.
- **Pictures handed on**, each with its slide; and **Left out**, by name.
- **The look:** the three colours with their values, the fonts, the text's
  contrast, and the background art.
- **Brand assets:** each in a sentence: its size, opacity, when it is on
  screen, trims and fades.
- **Transfer to the next layer** writes the snapshot later stages read. After
  changing anything, transfer again.

The header says where things stand: Nothing to transfer yet · Gather again
first · Ready to transfer · Transferred.

## Checks before transferring

- [ ] Extracted assets shows the pictures of the source you meant.
- [ ] Every picture you don't want is left out.
- [ ] Every **Check the crop** has been looked at.
- [ ] Brand assets sit where you want on the frame, and nothing is marked soft.
- [ ] The intro and outro play as trimmed.
- [ ] The Look's readability line is green.
- [ ] The Final tab shows the video as you expect it.
- [ ] It says **Transferred**.

## Things to know

- A project from before transfers existed is treated as transferred once, as it
  stood, the first time a later stage reads it.
- A library gathered by an older version is gathered again once when the page
  opens, so its pictures gain their slide. Your choices are kept.
- A brand kit saved with a corner, a size and an opacity keeps its logo on
  exactly the same pixels.
- Re-extracting and transferring a file brings its pictures in again. Your
  choices stay with them, because the same picture has the same id.
