"""The operations every client shares — web, CLI, and MCP.

Three interfaces reach this pipeline: a browser, a terminal, and an agent over
MCP. Each one needs "open project X, read its plan, add a section, save". Writing
that three times is how v1 failed: `workflow.py` built a graph that
`run_chapter.py` then bypassed with its own reimplementation, the two drifted,
and only one was ever exercised.

So the verbs live behind one name, and this module *is* that name. A client's job
is to parse its own kind of input -- an HTTP body, an argv list, an MCP tool call
-- and then call these. Nothing here knows which of the three it is talking to,
and none of the three contains pipeline logic.

**This file is the surface, not the implementation.** It reached seventeen
hundred lines and fifty-eight functions, at which point "one core" had quietly
become "one file everything is in" -- the failure it was written to prevent,
arrived at from the other direction. The verbs now live in modules beside it, in
a strict order, each importing only from the ones above it:

    core            finding a project and its artifacts
    freshness       whether an artifact is still true of what it was built from
    presentation    how an artifact is handed to a client, with its audit
    extraction_run  running extraction, and the settings that decide what it reads
    authoring       the verbs that edit an artifact on someone's behalf
    render_run      rendering, and everything measured from the narration
    assets          the picture library and the video's look
    exporting       the transcript, chapter marks and description

Nothing below imports this module back, so the order above is the dependency
order and there are no cycles to reason about.

Importing from `pipeline.operations` keeps working and stays the supported way
in: a client should not have to know which module a verb lives in, and moving one
must not break three interfaces. Every name re-exported here *is* the object the
module beside it defines -- nothing is wrapped, so a traceback points at the real
code and a test can patch either name.
"""

from __future__ import annotations

from pipeline.assets import (
    decide_figure,
    read_asset_library,
    refresh_asset_library,
    set_project_look,
)
from pipeline.authoring import (
    accept_plan_draft,
    add_clip,
    add_plan_section,
    add_review_comment,
    chapters_for,
    clear_timeline,
    confirm_plan_matches_extraction,
    confirm_section_narration,
    discard_plan_draft,
    read_plan_draft,
    section_source_material,
    seed_review_chapters,
    write_section_script,
)
from pipeline.core import (
    ARTIFACTS,
    ArtifactBinding,
    OperationFailed,
    create_project,
    describe_project,
    describe_stages,
    list_projects,
    project_store,
    projects_root,
    require_artifact,
    require_project,
)
from pipeline.exporting import build_export, export_readiness, read_export
from pipeline.extraction_run import (
    excluded_sources,
    extracted_content_as_markdown,
    extraction_freshness,
    forget_excluded_source,
    implemented_extraction_options,
    preview_source,
    run_extraction,
    set_excluded_sources,
)
from pipeline.freshness import (
    cut_freshness,
    narration_fingerprints,
    narration_freshness,
    plan_freshness,
    source_outline,
)

# `_script_in_plan_order` is private to the pipeline rather than to one module:
# drafting a plan section and drafting its narration both reorder the script the
# same way, and a second implementation of that is how two orderings appear.
from pipeline.presentation import (
    _script_in_plan_order,
    present_artifact,
    read_artifact,
    save_artifact,
    section_start_times,
    write_artifact,
)
from pipeline.render_run import chapters_from_sections, list_voice_providers, render_video

__all__ = [
    "ARTIFACTS",
    "ArtifactBinding",
    "OperationFailed",
    "_script_in_plan_order",
    "accept_plan_draft",
    "add_clip",
    "add_plan_section",
    "add_review_comment",
    "build_export",
    "chapters_for",
    "chapters_from_sections",
    "clear_timeline",
    "confirm_plan_matches_extraction",
    "confirm_section_narration",
    "create_project",
    "cut_freshness",
    "decide_figure",
    "describe_project",
    "describe_stages",
    "discard_plan_draft",
    "excluded_sources",
    "export_readiness",
    "extracted_content_as_markdown",
    "extraction_freshness",
    "forget_excluded_source",
    "implemented_extraction_options",
    "list_projects",
    "list_voice_providers",
    "narration_fingerprints",
    "narration_freshness",
    "plan_freshness",
    "present_artifact",
    "preview_source",
    "project_store",
    "projects_root",
    "read_artifact",
    "read_asset_library",
    "read_export",
    "read_plan_draft",
    "refresh_asset_library",
    "render_video",
    "require_artifact",
    "require_project",
    "run_extraction",
    "save_artifact",
    "section_source_material",
    "section_start_times",
    "seed_review_chapters",
    "set_excluded_sources",
    "set_project_look",
    "source_outline",
    "write_artifact",
    "write_section_script",
]
