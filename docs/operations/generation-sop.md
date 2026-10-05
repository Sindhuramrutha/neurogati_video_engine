# SOP: Generation

What this layer decides, in what order, and what it guarantees. The code is
`src/pipeline/generation.py` (deciding), `visual_build.py` (making) and
`generation_handoff.py` (the preview, the checks and the frozen transfer). The
page is `web/static/stage-generation.js`.

## What the layer is for

Every scene of the script gets a **shot**:

- what is on screen: a picture, or words;
- the few words the viewer reads (a headline and a few labels, never the
  narration);
- how the camera moves over it.

The render reads these shots.

## Guarantees

1. **Deciding uses no AI.** Decide applies fixed rules, in a fixed order. The
   same script and pictures always give the same decisions. You can change any
   scene by hand.
2. **Making says in advance what calls a model.** Two things do:
   - the headline and labels, composed from each scene's brief (a text model);
   - pictures drawn for scenes the source has nothing for (the image model).

   Slides, the source's own figures, charts and diagrams are made by local code.
   The Make tab counts each before you press anything.
3. **Fixed checks.** The Check tab applies fixed rules. The same shots always
   get the same results.
4. **The render reads frozen, transferred shots.** A transfer copies every
   picture and clip it points at, under names taken from their content. Making
   a scene again rewrites its working file in place. Without the copy, the
   render would silently change. With it, the render shows exactly what was
   transferred until you transfer again.
5. **Before the first transfer**, the render reads the working shots, as it
   always did. The Final tab says which.

## The five tabs, in order

### 1. Setup

- **What came in**: whether the script and Assets & Design are transferred.
  Transfer them first, so the shots are decided from fixed inputs.
- **Pictures handed on**: how many can be a scene's picture. A picture must be
  at least 64 px on each side, at least 120 px once its border is trimmed, not
  one flat tone, and not a sliver (more than 8 times wider than tall, or the
  reverse). Any that is not is named here with the reason, and no rule picks
  it. Assets & Design lists pictures and judges none; the judgement is made
  here, where a picture is chosen for a scene.
- **How each scene's shot is decided**: the first rule that applies wins.

| # | Shot | When | Made by |
|---|---|---|---|
| — | A scripted scene | You chose it, for this scene or for every scene | **AI** writes a script; fixed checks decide whether its clip is used ([SOP](scripted-scenes-sop.md)) |
| 1 | The deck's slide | The section follows a slide of the deck. A section covering several slides moves through them as its scenes go | Local code |
| 2 | A picture from the source | Assets & Design handed on a picture from the section's own source that is large and clear enough to fill a frame | Local code |
| 3 | A chart | The section is planned as a plot, and its source states enough numbers | Local code |
| 4 | A drawn picture | Nothing above applies, the section teaches or tells a story, and an image model is configured | **AI** (image model) |
| 5 | Words on screen | Nothing above applies; always for the lesson frame (Opening, Recap, Close) | Local code |

- When making finds that a scene describes a sequence or a comparison, a
  **diagram** can replace words or a drawn picture. It is drawn from the
  scene's own terms.
- **What this machine can draw** lists which renderers are installed and
  working, for animated diagrams.

### 2. Decide

- **Decide what to show** applies the rules to every scene. A scene already
  decided keeps its shot, including one you changed by hand, unless its brief
  or narration was rewritten.
- Each row shows the scene, what it shows, why, and the camera move. Change
  either one in place.

### 3. Make

- The bar lists what making will do, marking AI calls with **AI**.
- **Make what is missing** makes unmade scenes, and scenes rewritten since
  they were made.
- **Make everything again** remakes every scene, and asks first.
- The cards show each scene as it will look. Filter by *Not made yet*,
  *Drawn*, and so on.

### 4. Check

| Check | Rule | Result if it breaks |
|---|---|---|
| Shots match the script | One shot per scene of the transferred script | **Fails**: decide again |
| Every shot made | Each shot has its words, and its picture if it needs one | **Fails**: make what is missing |
| Made for the scene as written | No scene rewritten since its shot was made | **Fails**: make again |
| Pictures drawn by AI | Every drawn picture looked at against its brief | Warning while any exist |
| Making went cleanly | No scene reported a problem while being made | Warning |
| Script transferred | Made from a transferred script with no changes waiting | Warning |
| Assets transferred | Pictures chosen from a transferred Assets & Design | Warning |

### 5. Final & transfer

- The header says where things stand:
  - **Nothing to transfer yet**
  - **N check(s) fail**
  - **Ready to transfer**
  - **Transferred**
- **Transfer to the next layer** freezes the shots and hands them to the
  render. It is refused while a check fails.

## Checks before transferring

- [ ] The script and Assets & Design are transferred.
- [ ] Decide has run, and each scene shows what it should.
- [ ] Make has run. Every drawn (AI) picture has been looked at against its
      brief.
- [ ] Check: nothing **fails**.
- [ ] Final & transfer says **Transferred**. Then render from the Render tab.
