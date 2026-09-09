# ADR 0004 — Mechanical checks before human review

## Status

**Proposed.**

## Context

In v1, a human is the primary error detector. Production shell history shows the
operator repeatedly issuing revisions for **mechanical** defects:

```
--revise "Keep every visual element fully inside the frame. Nothing should be
          cut off at any edge..."          ← scene 0, then again scene 1

--revise "The animation is 55.6 seconds but the narration is only 52.3 seconds..."
```

Clipping is bounding-box arithmetic. Duration is subtraction. Neither requires
judgment, yet both consumed human attention and a full regeneration cycle.

v1 correctly decided **not** to automate aesthetic judgment
(v1 ADR 0002, `docs/architecture/decisions/0002-human-review-over-vision-critique.md`
in the v1 repository) —
a vision-critique loop cost several calls per scene to produce a verdict a human
re-checked anyway.

That decision is being misapplied. It argued against automating *taste*. It has
resulted in not automating *measurement* either.

Meanwhile `manim_lint.py` performs zero signature validation (verified: no
`inspect`, no `signature` anywhere), so an invented kwarg like `gap_length` fails
only at runtime — after a full 1080p render.

## Decision

**Mechanical properties are verified by machine before a human sees a scene.
Humans review craft only.**

Minimum check set, all cheap and deterministic:

| Check | Method |
|---|---|
| All elements within frame | Bounding-box measurement post-construction |
| No unintended overlap | Pairwise box intersection |
| Duration matches narration | Computed, or `ffprobe` compare |
| Valid API usage | Signature validation against introspected API |
| Minimum font size after scaling | Arithmetic |
| Contrast ratio | Computed luminance |
| Not blank / near-blank | Frame pixel statistics |
| On-screen strings attested by source | String extraction + source diff |

**No vision model is required for any of these.** They are arithmetic over the
constructed scene, and each is unit-testable.

Two preferences:

**Prefer impossible over detected.** A layout engine that cannot place something
off-frame beats a check that notices afterwards. Where construction can guarantee
a property, prefer that; use checks for what construction cannot predict.

**Reuse existing machinery.** `manim_reference.py` already introspects the live
package to build an API reference. Pointing the same introspection at generated
code gives signature validation nearly free.

The last row — verifying on-screen text against the source — deserves emphasis.
Fabricated data is the most dangerous defect this system can produce: it looks
authoritative and fails silently. v1 addresses it with prompt rules in three
places and no mechanical check. See
[Q10](../open-questions.md#q10--what-is-the-fabrication-guarantee).

## Consequences

**Positive**

- Every defect class in the production history is caught before review
- Human attention moves to craft, where it is irreplaceable
- Checks are deterministic and testable — they can run against all 253 existing
  scenes as a regression suite
- Failures produce precise feedback ("Text at x=7.2 exceeds bound 6.5") rather than
  a human's prose description

**Negative**

- Requires the scene to be inspectable before rendering — a real constraint on
  architecture, and an argument for a typed IR or a measurable target
- Over-strict checks could reject acceptable scenes; tolerances need tuning
- Checks are code, and code needs maintenance

**Not in scope**

Aesthetic judgment stays human. This ADR does not reintroduce vision critique for
quality. Rendered-frame analysis, if used, targets mechanical properties only
(blank frames, legibility) and can be sampled rather than run per scene.

## Revisit if

A defect class emerges that is genuinely mechanical but not cheaply checkable
without a vision model. Then evaluate a VLM for that specific check — sampled, not
per-scene.
