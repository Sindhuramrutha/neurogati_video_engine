"""Filesystem layout — the one module that knows where a project's files live.

Files are the source of truth (ADR 0005), so "where does this live?" has to have
exactly one answer. Every artifact path is derived from the `produces` field the
stage already declares in `stages.py`, which means the path shown in the UI and
the path written on disk cannot disagree — they are the same string.

They *did* disagree before this module was rewritten. `stages.py` advertised
`scripting/scenes.json` and `reviewing/report.json` while the stores wrote
`scripting/script.json` and `reviewing/review.json`, so the UI named two files
that never existed.

The layout, in full:

    projects/<slug>/
      project.json                    name, created timestamp
      sources/<uploaded file>         admitted by sources.py, nothing else
      settings/<stage>.json           per-stage option choices
      agents/<stage>/AGENT.md         project override of the shipped default
      inputs/                         (the sources themselves; see above)
      extraction/content.json
      planning/plan.json
      scripting/script.json
      studio/composition.json
      reviewing/review.json

An earlier version of this module documented a `chapters/<chapter>/{script,audio,
ir,render}/` tree carried over from v1, along with `ChapterPaths`, `ProjectPaths`
and `scene_stem` to build it. Nothing ever created that tree and nothing imported
those classes. The fiction was not harmless: `.gitignore` was written against it,
so its patterns matched nothing and a demo project — including an uploaded PDF —
was staged for commit. Documenting a layout the code does not create is worse
than documenting nothing.
"""

from __future__ import annotations

import re
from pathlib import Path

from pipeline.stages import BY_KEY, Stage


def slugify(text: str) -> str:
    """Filesystem-safe identifier: lowercase, non-alphanumeric runs collapsed to
    hyphens. Never empty -- a name of only punctuation yields "untitled" rather
    than a directory with no name."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def artifact_path(project_root: Path, stage: Stage) -> Path:
    """Where `stage` writes its artifact inside `project_root`.

    Derived from the stage's own `produces` declaration, so adding a stage or
    renaming its artifact is a one-line change that the stores, the API and the
    UI label all follow automatically.

    Note that `Stage.INPUTS` produces a *directory* (`sources/`) rather than a
    file. Callers that need the distinction should ask the stage, not guess from
    the suffix.
    """
    return project_root / BY_KEY[stage].produces
