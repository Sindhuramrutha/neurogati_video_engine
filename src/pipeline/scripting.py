"""The script — narration per plan section, plus scenarios and variables.

The script does not own its own outline. Sections come from the plan, and script
bodies are keyed by `PlanSection.id`, so renaming or reordering a section in
Planning never orphans its narration.

Deleting one does, though, and that is the interesting case: the body is kept and
reported as orphaned rather than silently dropped. Losing written narration
because someone tidied the outline would be the worst failure this stage can have,
and it would be invisible.

Stored at `projects/<slug>/scripting/script.json`.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

# Spoken-word rate used to estimate duration from a word count. Deliberate and
# named: the number appears in the UI and later drives the narration budget, so it
# must not be an anonymous 150 buried in a formula.
NARRATION_WORDS_PER_MINUTE = 150

MAXIMUM_SCENARIO_NAME_LENGTH = 60
MAXIMUM_SCENARIO_DESCRIPTION_LENGTH = 200
MAXIMUM_VARIABLE_NAME_LENGTH = 40
MAXIMUM_VARIABLE_VALUE_LENGTH = 200
MAXIMUM_SCRIPT_BODY_LENGTH = 20_000

# Variables are referenced as {{NAME}}. Restricted to a shape that cannot collide
# with markdown or regex syntax when substituted.
VALID_VARIABLE_NAME = re.compile(r"^[A-Z][A-Z0-9_]{0,39}$")
VARIABLE_REFERENCE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


def count_words(text: str) -> int:
    return len(text.split())


def estimate_seconds(text: str) -> int:
    return round(count_words(text) / NARRATION_WORDS_PER_MINUTE * 60)


class Scenario(BaseModel):
    """A variant of the same content for a different viewer."""

    id: str = Field(default_factory=new_identifier)
    name: str = ""
    description: str = ""

    @field_validator("name")
    @classmethod
    def _cap_name(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SCENARIO_NAME_LENGTH]

    @field_validator("description")
    @classmethod
    def _cap_description(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SCENARIO_DESCRIPTION_LENGTH]


class ScriptVariable(BaseModel):
    """A named substitution, written as {{NAME}} in a script body."""

    id: str = Field(default_factory=new_identifier)
    name: str = ""
    value: str = ""

    @field_validator("name")
    @classmethod
    def _normalise_name(cls, value: str) -> str:
        # Upper-cased and stripped of anything that would break substitution, so
        # a name typed as "my topic" becomes MY_TOPIC rather than a variable that
        # silently never matches.
        cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip()).strip("_").upper()
        return cleaned[:MAXIMUM_VARIABLE_NAME_LENGTH]

    @field_validator("value")
    @classmethod
    def _cap_value(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_VARIABLE_VALUE_LENGTH]

    @property
    def is_valid(self) -> bool:
        return bool(VALID_VARIABLE_NAME.match(self.name))


class SectionScript(BaseModel):
    """Narration for one plan section, keyed by that section's id."""

    section_id: str
    body: str = ""

    @field_validator("body")
    @classmethod
    def _cap_body(cls, value: str) -> str:
        return value[:MAXIMUM_SCRIPT_BODY_LENGTH]

    @property
    def word_count(self) -> int:
        return count_words(self.body)

    @property
    def estimated_seconds(self) -> int:
        return estimate_seconds(self.body)


class Script(BaseModel):
    section_scripts: list[SectionScript] = Field(default_factory=list)
    scenarios: list[Scenario] = Field(default_factory=list)
    active_scenario_id: str | None = None
    variables: list[ScriptVariable] = Field(default_factory=list)

    def body_for(self, section_id: str) -> str:
        for section_script in self.section_scripts:
            if section_script.section_id == section_id:
                return section_script.body
        return ""

    @property
    def total_word_count(self) -> int:
        return sum(s.word_count for s in self.section_scripts)

    @property
    def total_estimated_seconds(self) -> int:
        return sum(s.estimated_seconds for s in self.section_scripts)

    def referenced_variable_names(self) -> set[str]:
        """Every {{NAME}} appearing in any body."""
        found: set[str] = set()
        for section_script in self.section_scripts:
            found.update(m.upper() for m in VARIABLE_REFERENCE.findall(section_script.body))
        return found

    def resolve(self, text: str) -> str:
        """Substitute defined variables. Unknown references are left verbatim so
        the gap is visible in a preview rather than silently becoming empty."""
        values = {v.name: v.value for v in self.variables if v.is_valid}
        return VARIABLE_REFERENCE.sub(
            lambda match: values.get(match.group(1).upper(), match.group(0)), text
        )

    def audit(self, plan_section_ids: list[str]) -> dict:
        """Cross-check the script against the plan it belongs to.

        Three things a reviewer needs to know before moving on, none of which is
        visible from either document alone:

        - **orphaned**: narration whose section was deleted from the plan. Kept,
          not dropped -- written words are expensive.
        - **unwritten**: plan sections with no narration yet.
        - **undefined_variables**: {{NAME}} used but never defined, which would
          otherwise reach the final narration as literal braces.
        """
        known = set(plan_section_ids)
        written = {s.section_id for s in self.section_scripts if s.body.strip()}
        defined = {v.name for v in self.variables if v.is_valid}

        return {
            "orphaned_section_ids": sorted(written - known),
            "unwritten_section_ids": [sid for sid in plan_section_ids if sid not in written],
            "undefined_variables": sorted(self.referenced_variable_names() - defined),
            "invalid_variables": [v.name for v in self.variables if v.name and not v.is_valid],
        }

    def to_dict(self, plan_section_ids: list[str] | None = None) -> dict:
        audit = self.audit(plan_section_ids or [])
        return self.model_dump(mode="json") | {
            "total_word_count": self.total_word_count,
            "total_estimated_seconds": self.total_estimated_seconds,
            "per_section": {
                s.section_id: {
                    "word_count": s.word_count,
                    "estimated_seconds": s.estimated_seconds,
                }
                for s in self.section_scripts
            },
            "audit": audit,
            "warnings": self._warnings(audit),
        }

    def _warnings(self, audit: dict) -> list[str]:
        found: list[str] = []
        if audit["orphaned_section_ids"]:
            found.append(
                f"{len(audit['orphaned_section_ids'])} script(s) belong to sections "
                f"no longer in the plan — their text is kept but unused"
            )
        if audit["unwritten_section_ids"]:
            found.append(f"{len(audit['unwritten_section_ids'])} section(s) have no narration yet")
        if audit["undefined_variables"]:
            found.append(
                "undefined variable(s): " + ", ".join(audit["undefined_variables"])
            )
        if audit["invalid_variables"]:
            found.append("unusable variable name(s): " + ", ".join(audit["invalid_variables"]))
        return found


def default_script() -> Script:
    """A starting set of scenarios, so the stage is not an empty canvas.

    These are the variants this pipeline was built for; they are ordinary data and
    can be renamed or deleted.
    """
    general = Scenario(
        name="General audience",
        description="Plain language, engaging tone. Suits a broad viewer.",
    )
    return Script(
        scenarios=[
            general,
            Scenario(name="Students",
                     description="More worked examples, more patient pacing."),
            Scenario(name="Practitioners",
                     description="Concise. Assumes background; leads with the point."),
        ],
        active_scenario_id=general.id,
    )


class ScriptStore(JsonDocumentStore[Script]):
    """Persistence for the script. Durability behaviour lives in
    `JsonDocumentStore`; this only names the path, the model and the default."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.SCRIPTING),
            model_type=Script,
            build_default=default_script,
            description="script",
        )

    @property
    def script_path(self) -> Path:
        """Kept as a named alias: tests and callers read better saying
        `store.script_path` than `store.document_path`."""
        return self.document_path

