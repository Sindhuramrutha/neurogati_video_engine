# ADR 0002 — Structured output over free text

## Status

**Proposed.**

## Context

Every LLM call in v1 returns free text that is then parsed, repaired, or trusted:

- `scene_script.py` requests a JSON array and retries up to 3× on parse failure —
  because "long, technical outputs occasionally slip on strict JSON syntax"
- `scene_coder.py` requests raw Python, then runs four repair functions on it:
  `strip_code_fences`, `_last_code_block`, `_last_class_definition`,
  `_clamp_zero_durations`
- `prompt_maker.py` returns prose parsed only by the next prompt

Each repair exists because a real output broke something. The pattern is
consistent: **ask for a format, hope, then repair.**

Modern providers support schema-constrained generation. Combined with Pydantic
validation, malformed structure stops being a failure mode.

This ADR is independent of the architecture choice in
[Q1](../open-questions.md#q1--is-your-content-a-bounded-visual-vocabulary) — it
applies whether the model emits an IR, a component selection, or a plan.

## Decision

**Every LLM call in v2 returns a validated structured object, never free text to
be parsed.**

- Define a Pydantic model for every call's output
- Use provider-native structured output / tool calling to constrain generation
- Validate on receipt; retry with the validation error as feedback
- No regex repair of model output

Free-form natural language remains valid for genuinely textual fields —
narration, a subtopic name. The distinction: text *inside* a validated structure,
not a structure inferred from text.

## Consequences

**Positive**

- Parse failures largely eliminated; `scene_script.py`'s 3× retry becomes unnecessary
- Repair functions in `scene_coder.py` become unnecessary — nothing to repair
- Output shape is documented by a type, not a prompt paragraph
- Schemas are diffable, testable, and versionable
- Prerequisite for a typed IR, should
  [Q1](../open-questions.md#q1--is-your-content-a-bounded-visual-vocabulary) go
  that way

**Negative**

- Requires provider support for constrained generation; a fallback path is needed
  for providers lacking it (validate-and-retry still works, just less strongly)
- Schema design becomes real work, and schema changes become migrations
- Over-constraining can degrade quality — a model forced into an ill-fitting
  schema produces worse content than one given room

**Note on model support**

v1's provider setup found that routers gate models behind different protocols, and
structured-output support varies. Verify support for the specific models you intend
to use before depending on it.

## Revisit if

Schema constraints measurably degrade output quality on a task. The likely fix is
a looser schema for that call rather than abandoning the principle.
