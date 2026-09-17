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
      scene-plan/plan.json
      script-staging/script.json
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


# The folders two stages used before they were renamed. Kept as data rather than
# as a one-off `if`, because this is the list a reader needs when they find a
# `planning/` directory in an old project and wonder what reads it.
RENAMED_STAGE_FOLDERS: tuple[tuple[str, str], ...] = (
    ("planning", "scene-plan"),
    ("scripting", "script-staging"),
)


def migrate_stage_folders(project_root: Path) -> list[str]:
    """Move a project's folders to the names its stages now use.

    A rename that left `planning/plan.json` unreadable would be a rename that
    threw away work, so every project is moved the first time it is opened.
    Moved, not copied: two folders holding two versions of the same plan is the
    ambiguity this avoids. If both exist -- which should not happen -- the new
    one wins and the old is left untouched for someone to look at.
    """
    moved: list[str] = []
    for old_name, new_name in RENAMED_STAGE_FOLDERS:
        old_folder = project_root / old_name
        new_folder = project_root / new_name
        if not old_folder.is_dir() or new_folder.exists():
            continue
        old_folder.rename(new_folder)
        moved.append(f"{old_name}/ -> {new_name}/")

    # Settings and agent overrides are named after the stage too.
    for old_name, new_name in RENAMED_STAGE_FOLDERS:
        old_settings = project_root / "settings" / f"{old_name}.json"
        new_settings = project_root / "settings" / f"{new_name}.json"
        if old_settings.is_file() and not new_settings.exists():
            old_settings.rename(new_settings)
            moved.append(f"settings/{old_name}.json -> settings/{new_name}.json")

        old_agent = project_root / "agents" / old_name
        new_agent = project_root / "agents" / new_name
        if old_agent.is_dir() and not new_agent.exists():
            old_agent.rename(new_agent)
            moved.append(f"agents/{old_name}/ -> agents/{new_name}/")

    return moved


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
