# SOP: Script & Staging

What this layer decides, in what order, and what it guarantees. The code is
`src/pipeline/scripting.py` (the script), `script_drafting.py` (the agent's
drafts) and `script_handoff.py` (the checks and the transfer). The page is
`web/static/stage-script-staging.js`.

## What the layer is for

The words of the video, and what is on screen while each is said. Every
section of the transferred Scene Plan gets narration, written as **scenes**:

- **Said:** the narration, spoken as written. `{{VARIABLES}}` are filled in.
- **On screen:** the brief, which says what is shown. Each scene's agent in
  Generation reads it, with the narration, to make the scene.

Later stages read the script: the scenes, the render, Studio, the review and
the export.

## Guarantees

1. **Written against the transferred plan.** The sections come from the Scene
   Plan's last transfer, so editing the outline never shifts the sections
   under the writing.
2. **AI only where you ask.** *Draft all unwritten* writes empty sections
   only. It never touches narration that is already written. *Draft this
   section* replaces one section, and asks first if it has text. Both are
   marked **AI**.
3. **Fixed checks.** The Check tab applies fixed rules. The same script always
   gets the same results.
4. **Later stages read the transferred script.** After the first transfer, they
   read only the transferred copy. Until then they read the working script, as
   before. The Final tab says which.
5. **Written narration is never dropped silently.** Narration whose section
   left the plan is kept and listed until you attach it or delete it.

## The four tabs, in order

### 1. Setup

- **Handed on by the Scene Plan** lists the sections with their planned length
  and scene count, and the audience if one was given.
- **Script variables**: `{{NAME}}` values filled in wherever they are spoken
  or shown. Names use capitals, digits and `_` only.
- **Narration from earlier plans**: text written for sections the plan no
  longer has. It is not in the video. Attach one piece to a section, delete one,
  or **Delete all**.

### 2. Write

- Pick a section on the left. Write its scenes in the middle. The right shows
  what it was planned with: target length (about 150 words a minute),
  audience, source text, and any open review comments for Scripting.
- **The scenes are the plan's.** Each scene card shows what the plan says that
  scene does, and its planned seconds. The script fills them; it does not add,
  remove or reorder them. That is done on the Scene Plan.
- **Out of date** means the plan section or its source changed since this was
  written. Update the narration, or use **Keep narration as is**.
- Typing saves by itself within a second. Switching sections or tabs saves
  first.

### 3. Check

| Check | Rule | Result if it breaks |
|---|---|---|
| Every section has narration | Each planned section is written | **Fails** (the video would show a silent card) |
| Variables defined | Every `{{NAME}}` used is defined | **Fails** (spoken as literal braces) |
| Variable names | Capitals, digits and `_` only | Warning |
| Section lengths | Each written section between 50% and 125% of its planned length | Warning |
| Total length | Within the length the Scene Plan agreed | Warning |
| Up to date | Written against the plan section and source as they are now | Warning |
| On-screen briefs | Every scene says what is shown | Warning |
| Review comments | No open review comment sent back to Scripting | Warning |
| Unattached narration | No narration from sections the plan dropped | Warning |
| Scene Plan transferred | Written against a transferred plan with no changes waiting | Warning |

### 4. Final & transfer

- The header says where things stand:
  - **Nothing to transfer yet**
  - **N check(s) fail**
  - **Ready to transfer**
  - **Transferred**
- **Transfer to the next layer** writes the copy later stages read. It is
  refused while a check fails.
- After editing, transfer again. Until you do, later stages keep reading the
  previous transfer.

## Checks before transferring

- [ ] The Scene Plan is transferred, and Setup lists the sections you expect.
- [ ] Leftover narration is attached where it belongs, and the rest deleted.
- [ ] Every section is written, and every scene has an on-screen brief.
- [ ] Check: nothing **fails**. Every warning is either fixed or accepted on
      purpose.
- [ ] Final & transfer says **Transferred**.
