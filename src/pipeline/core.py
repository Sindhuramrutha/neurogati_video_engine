"""Finding a project and its artifacts — what every operation starts with.

Separate from the operations themselves so that a module holding one stage's
verbs can resolve a project without importing every other stage's verbs. This is
the bottom of the dependency order: it imports the stores and nothing else in
`pipeline` imports it back.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pipeline.composition import Composition, CompositionStore
from pipeline.config import get_settings
from pipeline.extraction import (
    Extraction,
    ExtractionStore,
)
from pipeline.planning import (
    Plan,
    PlanStore,
)
from pipeline.projects import Project, ProjectStore
from pipeline.review import (
    Review,
    ReviewStore,
)
from pipeline.scripting import (
    Script,
    ScriptStore,
)
from pipeline.stages import STAGES, Stage
from pipeline.storage.documents import JsonDocumentStore


class OperationFailed(Exception):
    """A request that cannot be satisfied, phrased for whoever asked.

    One exception type for all three clients: the web layer turns it into a 404
    or 400, the CLI prints it and exits non-zero, MCP returns it as tool output.
    The message is written for a human or a model to read, never a stack trace.
    """

@dataclass(frozen=True)
class ArtifactBinding:
    """Wires a stage to the store and model that persist its artifact.

    Having this as data rather than a chain of `if stage == ...` is what lets the
    CLI and the MCP server expose all four artifacts through one code path each,
    instead of four near-identical handlers apiece.
    """

    stage: Stage
    store_type: type[JsonDocumentStore]
    model_type: type

    def store(self, project: Project) -> JsonDocumentStore:
        return self.store_type(project.root)

ARTIFACTS: dict[str, ArtifactBinding] = {
    "extraction": ArtifactBinding(Stage.EXTRACTION, ExtractionStore, Extraction),
    "plan": ArtifactBinding(Stage.SCENE_PLAN, PlanStore, Plan),
    "script": ArtifactBinding(Stage.SCRIPT_STAGING, ScriptStore, Script),
    "composition": ArtifactBinding(Stage.STUDIO, CompositionStore, Composition),
    "review": ArtifactBinding(Stage.REVIEWING, ReviewStore, Review),
}

def projects_root() -> Path:
    return get_settings().projects_dir

def project_store() -> ProjectStore:
    return ProjectStore(projects_root())

def require_project(slug: str) -> Project:
    project = project_store().get(slug)
    if project is None:
        known = ", ".join(p.slug for p in project_store().list()) or "none yet"
        raise OperationFailed(f"No project {slug!r}. Existing projects: {known}.")
    return project

def require_artifact(name: str) -> ArtifactBinding:
    binding = ARTIFACTS.get(name)
    if binding is None:
        raise OperationFailed(
            f"No artifact {name!r}. Choose one of: {', '.join(ARTIFACTS)}."
        )
    return binding

def list_projects() -> list[dict[str, Any]]:
    return [project.to_dict() for project in project_store().list()]

def create_project(name: str) -> dict[str, Any]:
    cleaned = name.strip()
    if not cleaned:
        raise OperationFailed("A project needs a name.")
    return project_store().create(cleaned).to_dict()

def describe_project(slug: str) -> dict[str, Any]:
    return require_project(slug).to_dict()

def describe_stages() -> list[dict[str, Any]]:
    """The pipeline's shape, for a client that has never seen it.

    An agent asking "what can I do here?" gets a real answer from this rather
    than having to infer the stages from endpoint names.
    """
    return [
        {
            "key": spec.key.value,
            "title": spec.title,
            "blurb": spec.blurb,
            "has_agent": spec.has_agent,
            "produces": spec.produces,
        }
        for spec in STAGES
    ]
