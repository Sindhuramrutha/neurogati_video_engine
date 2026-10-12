# SOP: Scene Plan

How the video's shape is decided and agreed: its length, its sections, and the
scenes each section is made of.

**Code:**

- `plan_agent.py`: the conversation and the planning agent
- `plan_order.py`: the slide-order rules
- `plan_units.py`: the source as slides or parts
- `plan_handoff.py`: the checks and the transfer
- `lesson_plan.py`: saving, and what a section about no slide is written from
- `plan_pictures.py`: section pictures

**Page:** `stage-scene-plan.js`

## What the layer is for

You tell the planning agent what the video should be. It proposes the shape. You
agree to it, or say what to change. Once you agree, each section is broken into
its scenes. Every later layer then works scene by scene:

- the script writes each scene's narration
- Generation makes one scene program per scene, each by its own agent
- the render cuts them

## Guarantees

1. **Nothing changes until you agree.** A message gets a proposed shape. The plan
   is untouched until you press **Agree to this shape**.
2. **The slide order is held by code.**
   - The rule you choose (Strict, Nearly strict, Loose, Free) is checked by fixed
     rules, not trusted to the model.
   - Under Strict, a shape whose slides are out of order, overlapping or broken
     into gaps is sent back to the agent once, with the exact problem.
   - If it is still wrong, it cannot be agreed to.
   - A saved plan that breaks Strict fails the check and cannot be transferred.
3. **Every slide is covered, or its being left out is said.** The agent lists any
   slide it leaves out, with why.
4. **AI is said before it runs.**
   - A message costs one call, or two when the first answer breaks the order.
   - Agreeing costs one call per section whose scenes must be written. The button
     says how many.
   - A section whose slides and scene count did not change keeps its scenes, and
     costs nothing.
5. **The plan owns the scenes.** The script fills exactly the planned scenes, by
   their ids. Adding, removing or reordering a scene is done here.
6. **The plan carries Assets & Design.** The plan cannot be transferred until
   Assets & Design has been. The transfer carries each section's pictures, the
   brand kit and the look.

## The three tabs, in order

### 1. Direction

**The setup.** Each part is saved as you change it, and sent with every message.

- **Length, in your words**, for example "about 1 hr, longer if needed, never
  shorter". The agent says back how it understood it, and the checks use that
  reading.
- **Slide order**:
  - **Strict**: unbroken runs, in the deck's order.
  - **Nearly strict**: sections follow the deck; a slide may move within one.
  - **Loose**: no slide twice.
  - **Free**.
- **Audience**: optional, typed by you.
- **Language.**

**The conversation.**

- Write what the video should be: what to stress, what to keep together, what to
  skip.
- The agent answers in words and proposes the shape:
  - the length, as understood
  - each section's title, slides, minutes and scene count, and how it is told,
    in its own words
  - the totals
- Then **Agree to this shape**, **Discard**, or reply with what to change.
- After you agree, keep talking. A reply that changes the shape gives a revised
  one to agree to again.

### 2. Plan

What was agreed, editable by hand:

- **Each section:**
  - its slides, as a run like "4–9" or a list like "4, 6"
  - its time, which is the sum of its scenes
  - its pictures, by rule from its slides; attach or detach any
  - its scenes
- **Each scene:** what it says and shows, its slides, and its seconds. Add,
  remove or move scenes; each change is saved as you make it.
- **Sections:** add one by hand, or delete one in its editor.

### The checks (shown on Final & transfer)

| Check | Rule | Result if it breaks |
|---|---|---|
| Has sections | At least one section | **Fails** |
| Sources exist | Every slide a section names is in the extraction | **Fails** |
| Slide order | The chosen rule | **Fails** under Strict, a warning otherwise |
| Every slide covered | Each slide is in a section, or left out with why | Warning |
| Every section has scenes | Each section is broken into scenes | **Fails** |
| Length | Within the length as understood | Warning |
| Matches the extraction | Planned from the extraction as it is now | Warning |
| Titles | Every section has a title | Warning |
| Assets transferred | Assets & Design is transferred | **Fails** if never transferred; warning if it has untransferred changes |

There is no Check tab. Final & transfer lists only the checks with something to
say: **Blocks** for one that stops the transfer, **Note** for a warning.

### 3. Final & transfer

- **Transfer to the next layer** hands on the plan, its scenes, and the pictures,
  brand kit and look it carries.
- Until the first transfer, later stages read the working plan.

## Checks before transferring

- [ ] The setup says what you want: the length, the slide order, and the audience
      if it matters.
- [ ] You agreed to a shape, and its length as understood is right.
- [ ] Each section covers the slides it should. Under Strict, the order check
      passes.
- [ ] Each section's scenes read right, and their seconds add up to what you want.
- [ ] Each section shows the pictures it should.
- [ ] Final & transfer lists nothing that **blocks**.
- [ ] Final & transfer says **Transferred**.

## Things to know

- **There are no fixed kinds of section** (no Teach, Story, Opening, Recap or
  Close labels). The agent decides what the video needs, names every section, and
  says how each is told. A section about no slide is written from the rest of the
  plan and what the other sections said.

- **When the extraction is transferred again**, this layer is flagged. Tell the
  planning agent what changed. It proposes a revised shape, and unchanged
  sections keep their scenes.
- **A plan from before this layer was rebuilt** has no scenes, so it fails
  "Every section has scenes". Plan it again on the Direction tab, or add scenes
  by hand on the Plan tab.
- **There are no learning objectives, key themes or audience presets.** Your
  direction is the aim, and the audience is optional and in your own words.
