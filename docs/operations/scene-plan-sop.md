# SOP: Scene Plan

What this layer decides, in what order, and what it guarantees. The code is
`src/pipeline/planning.py` (the plan), `slide_plan.py` (following the deck),
`plan_drafting.py` (the agent's draft), `lesson_plan.py` (roles, the lesson
frame, time and objective links), `plan_summaries.py` (AI · write summaries) and
`plan_handoff.py` (the checks and the transfer). The page is
`web/static/stage-scene-plan.js`.

## What the layer is for

The shape of the lesson: what is taught, in what order, for how long, and
toward which learning objectives. Script & Staging says it; Generation decides
what is on screen. It also records who the video is for.

A plan is a lesson, not a copy of the deck. Every section has a **role**:

| Role | What it does | Written from |
|---|---|---|
| **Opening** | A hook, then what the viewer will be able to do by the end | The objectives and the plan |
| **Teach** | Teaches its part of the source | Its source |
| **Story** | Tells a story or case first hand, in order, then what it shows | Its source |
| **Recap** | Back through each objective, one short beat each | What the sections actually said |
| **Close** | The one idea to keep, and something to think about next | The plan and the recap |

Opening, Recap and Close are the **lesson frame**. It is on for every new plan,
and each part can be switched off in the Brief. A plan saved before the frame
existed starts with it off.

Every later stage reads the plan: the script, the visuals, the render, the
review and the export.

## Guarantees

1. **Two things here use AI, and both only propose.**
   - *Draft with the agent*: a whole plan, shown beside yours.
   - *AI · write summaries*: one line per section. One model call; the button
     says how many sections before it runs.

   Neither changes the plan until you accept it, all at once or one by one.
   Everything else is rule-based.
2. **Following the deck is a fixed rule.** One section per slide, every slide,
   in the deck's order. The same deck always gives the same plan.
3. **Fixed checks.** The Check tab applies fixed rules. The same plan always
   gets the same results.
4. **The shape is applied on every save.** The frame stays at the edges, and the
   time is shared out again. The same plan, extraction and target always give
   the same lengths.
5. **Later stages read the transferred plan.** After the first transfer, the
   script, visuals, render, review and export read only the transferred plan.
   Editing the outline never shifts a script underneath someone.
6. **Before the first transfer**, later stages read the working plan, as they
   always did. Projects from before this step keep working unchanged. The Final
   tab says which one later stages are reading.
7. **The plan carries Assets & Design.** Each section has pictures, attached
   from what Assets & Design transferred. The transfer copies them, the brand kit
   and the look into the transferred plan; every later layer uses those and
   nothing else (`plan_pictures.py`). The plan cannot be transferred until
   Assets & Design has been.

## The four tabs, in order

### 1. Brief

- The plan is built from the last Extraction transfer of the project's one
  source file, named in the strip under the header. A section's source reads
  "Slide 3" or "§ Heading", never the file's name.
- Set the **target audience** first. Tone and depth are written for one reader.
- Add **learning objectives**: what the viewer should come away knowing.
- **The lesson frame**: switch the Opening, Recap and Close on or off.
- **Key themes** are optional. A draft proposes some.
- **Video preferences** apply to the whole video:
  - *Target duration* decides how the time is shared (see below).
  - *Tone* reaches the narration.
  - *Language* reaches the narration and the voice.

### 2. Outline

Choose **how to build the outline**. The code is `plan_approaches.py`.

| Approach | What decides | Best when |
|---|---|---|
| **Follow the deck** | A fixed rule: one section per slide, in order | The deck is already a good lesson |
| **Group into ideas** | AI: neighbouring slides that make one idea become one section; nothing reordered or skipped | The deck spreads one idea over several slides |
| **Story first** | AI: the story or case first, in order, then what lies behind it | The material has a person, a case or an event |
| **Concept first** | AI: ideas from the simplest up, then the examples | The viewer needs the basics first |
| **Question led** | AI: every section answers one question | The topic is best learnt by asking why and how |
| **By hand** | You | You already know the structure |

- The AI approaches each send a fixed instruction, plus your options and your
  own words, to the Scene Plan agent. The result is a draft beside the plan.
- **Options** for the AI approaches: how many sections, and the longest section.
- **Anything else the plan should do**: your own instructions, in your words.
- **A section covering several slides shows** each slide in turn as its scenes
  go, or only its first. This applies to the plan as it is, and saves at once.

- A draft appears beside your plan. Use **Accept all**, **Add to plan** section
  by section, or **Discard**.
- **The timeline** shows each section's share of the video, coloured by role.
  Under it, the page says how long the material needs and whether the target
  stretches or squeezes it.
- **Time** is shared out by fixed rules:
  - A teaching section needs 0.4 s per word of its source, plus 12 s per
    picture it must explain, and at least 20 s.
  - Opening 25 s; Close 15 s; Recap 8 s plus 10 s per objective (20–90 s).
  - The total is kept inside the target duration. Material that needs less is
    stretched up to the target's start; material that needs more is cut down to
    its end. Past ×1.5 or below ×0.6, the Check tab warns.
  - Typing a section's length **pins** it. The rest share what is left. Click
    **pinned ×** to let it follow the target again.
- **Summaries** say, in one line, what the viewer learns. A deck plan starts
  with the slide's title as a stand-in. A summary that is a stand-in, raw
  source text, or talks about the source ("this chapter explores…") is marked,
  and is not passed to the Scripting agent as a summary.
  - **AI · write N summaries** proposes one for each marked section. Each shows
    under its section with **Use** and **Dismiss**, or use them all at once.
- **Objective links** are suggested by the words a section and an objective
  share, which the chip names. Two shared words suggest a link, and so does one
  when that section is the objective's best match. **Link** one, or link them
  all. The Opening and Recap are linked to every objective by the frame.
- Click a section to edit its title, summary, role (Teach or Story), sources,
  how it is shown, the objectives it serves, and its length. Drag to reorder
  the body; the frame stays at the edges.
- The bar at the top says how the plan relates to the extraction: matches, out
  of date, not linked, or no longer following the deck. **Keep plan as is**
  records that you checked it against the current extraction.

### Pictures, per section

- By rule, a section gets every picture from its own slides (or under its own
  headings) that is large and clear enough to fill a frame. The outline row shows
  them, with **by rule** or **chosen**.
- In the section editor, **Pictures it shows** lists every picture Assets &
  Design handed on. Click one to attach or detach it; the section then keeps
  exactly your choice. **Back to the rule** hands it back. A picture that cannot
  fill a frame says why and cannot be attached.
- When Assets & Design is transferred again, the rule's pictures follow it; a
  chosen set keeps your choice, minus any picture no longer handed on.
- The Script agent is told each section's pictures, and Generation shows only
  these for the section's scenes.

### 3. Check

| Check | Rule | Result if it breaks |
|---|---|---|
| Has sections | At least one section | **Fails**: blocks the transfer |
| Sources exist | Every source a section names is in the extraction | **Fails**: blocks the transfer |
| Lesson frame | An Opening, Recap and Close wrap the body | Warning when switched off |
| Every section has a source | Each teaching section names the content it teaches | Warning |
| Matches the extraction | Drafted or checked against the extraction as it is now | Warning |
| Follows the deck | Every slide covered, in order (only for a plan built slide by slide) | Warning |
| Titles | Every section has a title | Warning |
| Section lengths | Each section between 10 s and 10 min | Warning |
| Total length | Within the target duration set in the Brief | Warning |
| Learning objectives | At least one; each taught by a body section, and each body section teaching one (the frame does not count) | Warning |
| Summaries | Each teaching section says in one line what the viewer learns | Warning |
| Time for the material | The target neither stretches the material past ×1.5 nor squeezes it below ×0.6 | Warning |
| Audience | One audience is chosen | Warning |
| Assets transferred | Assets & Design is transferred; the plan carries its pictures, brand kit and look | **Fails** if never transferred; warning if it has changes not transferred |

The Check tab shows a count badge: red if a check fails, orange if there are
warnings.

### 4. Final & transfer

- The header says where things stand:
  - **Nothing to transfer yet**
  - **N check(s) fail**: fix them first.
  - **Ready to transfer**: never transferred, or changed since the last
    transfer.
  - **Transferred**: the next layer has exactly this.
- **Transfer to the next layer** writes the copy every later stage reads. It is
  refused while a check fails.
- After changing the outline, transfer again. Until you do, later stages keep
  reading the previous transfer.

## Checks before transferring

- [ ] Assets & Design is transferred, and each section shows the pictures it
      should; attach or detach any that are wrong.
- [ ] The audience, objectives and target duration are set.
- [ ] The outline is built by the method that fits the source, and each section
      reads right.
- [ ] The lesson frame is on, unless you have a reason for it not to be.
- [ ] Every teaching section's summary says what the viewer learns.
- [ ] Every objective is taught by a section; the suggested links are looked at.
- [ ] The time note under the timeline does not warn, or you accept why.
- [ ] Check: nothing **fails**. Every warning is either fixed or accepted on
      purpose.
- [ ] Final & transfer says **Transferred**.

## Things to know

- When the extraction is transferred again, this layer is **flagged** (see
  the [change flags SOP](change-flags-sop.md)). **Re-sync the plan** brings a
  deck plan back in step: new slides get sections, removed slides lose theirs,
  and every section you edited is kept.
- Re-extracting and transferring the extraction can make the plan **out of
  date**. Its sources may have changed or disappeared. The Check tab says
  which. Fix the sections, or use **Keep plan as is** if the plan still holds.
- Script sections are tied to plan sections by id. Replacing the whole plan
  (Accept all, Follow the deck) leaves narration written for removed sections
  unattached. It is kept, not deleted.
