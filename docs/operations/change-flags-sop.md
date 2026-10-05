# SOP: Change flags

When a layer is transferred again, every layer after it is flagged. The code is
`src/pipeline/upstream.py`. The page side is in `web/static/ui-kit.js`
(`stageHeader` draws the banner) and `app.js` (what the banner's buttons do).

## What it is for

Each layer is built from the transfer of the layers before it. Transfer the
extraction again with a slide changed, and the plan, the script, the shots and
the render are all about something that is no longer what was extracted. The
flag says so on every one of them, and says what changed.

## Guarantees

1. **Every transfer records what it was built from**: a fingerprint of each
   earlier layer it reads, part by part (each slide, section, scene, picture).
   Stored in `handoffs.json` in the project.
2. **The flag is a comparison of fingerprints.** No AI. The same transfers
   always give the same flags.
3. **The flag names the parts**: what is new, what changed, what is gone.
4. **A layer further down is flagged too**, because what it was built on is now
   behind.
5. **A project from before this existed** is taken as in step, once, as it
   stands. It is not flagged for changes nobody made.

## What each layer reads

| Layer | Flagged when this is transferred again |
|---|---|
| Assets & Design | Extraction |
| Scene Plan | Extraction |
| Script & Staging | Scene Plan, Extraction |
| Generation | Script & Staging, Assets & Design |
| Render | Generation, Script & Staging, Assets & Design |

## What you see

- The layer's button in the sidebar turns red, with a **!**.
- A red **Out of date** banner under the layer's header:
  - which layer was transferred again, and when;
  - the parts that are new, changed or removed (the first eight of each);
  - or, for a layer further down, which earlier layer to bring up to date
    first.

## What to do

Work down the layers in order. On each flagged layer:

1. Press the banner's **redo** button.

   | Layer | Redo | What it does |
   |---|---|---|
   | Assets & Design | Gather again | Gathers from the new extraction. Your Use and Skip are kept |
   | Scene Plan | Re-sync the plan | For a deck plan: adds sections for new slides, removes sections whose slides are gone, keeps every edit. Otherwise, opens the Outline to redo by hand or redraft |
   | Script & Staging | Go to the sections to redraft | Opens the Write tab, where changed sections are marked |
   | Generation | Decide the shots again | Opens the Decide tab. Unchanged scenes keep their shot |
   | Render | Render again | Opens the Render page |

2. Check the layer, then **transfer** it on its Final tab. Transferring clears
   the flag, and the flag moves to the next layer if this one changed.

If the layer still holds as it is, press **Transfer as it stands**. That opens
its Final tab, where it can be transferred again unchanged.

## Things to know

- The flag clears only by transferring the layer again. Redoing the work
  without transferring leaves it flagged.
- Re-syncing a plan re-shares the time, so existing sections can show as
  *changed* to the script even when only their length moved.
