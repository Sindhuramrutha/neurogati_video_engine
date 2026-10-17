"""The script — narration per plan section, plus variables.

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
import threading
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator

from pipeline.stages import Stage
from pipeline.storage.documents import JsonDocumentStore, new_identifier
from pipeline.storage.layout import artifact_path

logger = logging.getLogger(__name__)

# Spoken-word rate used to estimate duration from a word count. Deliberate and
# named: the number appears in the UI and later drives the narration budget, so it
# must not be an anonymous 150 buried in a formula.
NARRATION_WORDS_PER_MINUTE = 150

# How far a section's narration may run past the plan's estimate before it is
# reported. Estimates are rough and a few words over is not a problem; half as
# long again is a different video from the one that was planned.
OVER_BUDGET_TOLERANCE = 1.25

MAXIMUM_VARIABLE_NAME_LENGTH = 40
MAXIMUM_VARIABLE_VALUE_LENGTH = 200
MAXIMUM_SCRIPT_BODY_LENGTH = 20_000
MAXIMUM_SCENE_NARRATION_LENGTH = 8_000
MAXIMUM_SCENE_BRIEF_LENGTH = 2_000
MAXIMUM_SCENES_PER_SECTION = 40

# Variables are referenced as {{NAME}}. Restricted to a shape that cannot collide
# with markdown or regex syntax when substituted.
VALID_VARIABLE_NAME = re.compile(r"^[A-Z][A-Z0-9_]{0,39}$")
VARIABLE_REFERENCE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


# Scenes are joined with a blank line. The renderer splits on blank lines first,
# so a slide never runs across the boundary between two scenes.
SCENE_SEPARATOR = "\n\n"


def count_words(text: str) -> int:
    return len(text.split())


def estimate_seconds(text: str) -> int:
    return round(count_words(text) / NARRATION_WORDS_PER_MINUTE * 60)


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


class ScriptScene(BaseModel):
    """One scene: what is said, and what is on screen while it is said.

    The brief is the half the script could not hold before. The Scripting agent
    was always told to write one -- "the single most direct cause of bad output
    downstream" in its own instructions -- and the script had nowhere to put it,
    so the only thing a later stage could show was the narration itself.
    """

    id: str = Field(default_factory=new_identifier)
    narration: str = ""
    brief: str = ""

    @field_validator("narration")
    @classmethod
    def _cap_narration(cls, value: str) -> str:
        return value[:MAXIMUM_SCENE_NARRATION_LENGTH]

    @field_validator("brief")
    @classmethod
    def _cap_brief(cls, value: str) -> str:
        return value.strip()[:MAXIMUM_SCENE_BRIEF_LENGTH]

    @property
    def estimated_seconds(self) -> int:
        return estimate_seconds(self.narration)


class SectionScript(BaseModel):
    """Narration for one plan section, keyed by that section's id.

    **The scenes are the narration.** `body` is always rebuilt from them, joined
    scene by scene, so everything that reads a section's text -- the render, word
    counts, the review transcript -- keeps working and cannot disagree with the
    scenes. A section saved before scenes existed has only a body; it becomes a
    single scene when loaded. When a client sends both, the scenes win.
    """

    section_id: str
    body: str = ""
    scenes: list[ScriptScene] = Field(default_factory=list)

    # What this narration was written against: fingerprints of the plan section
    # and of the source content it covers, taken whenever the narration changes.
    # Compared later to say "the plan or the source changed since this was
    # written" -- the gap Planning had with Extraction, one stage further on.
    written_from: dict[str, str] = Field(default_factory=dict)
    # What the check against the slides left standing when it was drafted, after
    # the agent's rounds of revision: claims that lead away from the slides or get
    # them wrong, and slide points the narration does not cover.
    unsupported: list[str] = Field(default_factory=list)
    uncovered: list[str] = Field(default_factory=list)
    # Where a slide itself is wrong (a person decides: the slide or the fact), and
    # what the agent left as it was on purpose, with why.
    slide_wrong: list[str] = Field(default_factory=list)
    kept: list[str] = Field(default_factory=list)

    @field_validator("body")
    @classmethod
    def _cap_body(cls, value: str) -> str:
        return value[:MAXIMUM_SCRIPT_BODY_LENGTH]

    @field_validator("scenes")
    @classmethod
    def _cap_scenes(cls, value: list[ScriptScene]) -> list[ScriptScene]:
        return value[:MAXIMUM_SCENES_PER_SECTION]

    @model_validator(mode="after")
    def _scenes_are_the_narration(self) -> SectionScript:
        if not self.scenes and self.body.strip():
            self.scenes = [ScriptScene(narration=self.body)]
        self.body = SCENE_SEPARATOR.join(
            scene.narration.strip() for scene in self.scenes if scene.narration.strip()
        )[:MAXIMUM_SCRIPT_BODY_LENGTH]
        return self

    @property
    def word_count(self) -> int:
        return count_words(self.body)

    @property
    def estimated_seconds(self) -> int:
        return estimate_seconds(self.body)


class Script(BaseModel):
    section_scripts: list[SectionScript] = Field(default_factory=list)
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

    def in_plan_order(self, plan_section_ids: list[str]) -> Script:
        """The same script with its sections in the order the plan gives them.

        Narration is looked up by section id, so the stored order never changed
        what was rendered -- but it is what anyone reading `script.json` sees,
        agents included. Writing section 2 last left the list as 1, 3, 4, 5, 2,
        and a review agent reported the video as out of order when it was not.

        Sections the plan no longer has keep their place at the end, unchanged:
        orphaned narration is kept on purpose.
        """
        position = {section_id: index for index, section_id in enumerate(plan_section_ids)}
        ordered = sorted(
            self.section_scripts,
            key=lambda s: (s.section_id not in position, position.get(s.section_id, 0)),
        )
        return self.model_copy(update={"section_scripts": ordered})

    def referenced_variable_names(self) -> set[str]:
        """Every {{NAME}} appearing in any body."""
        found: set[str] = set()
        for section_script in self.section_scripts:
            found.update(m.upper() for m in VARIABLE_REFERENCE.findall(section_script.body))
        return found

    def spoken_text(self, section_id: str) -> str:
        """Exactly what is said for this section: its narration, variables filled in.

        The one place that answer comes from. Reading the raw body instead would let
        a reviewer read "Neuroscience 101" while the video says "{{COURSE}}" out loud.
        """
        return self.resolve(self.body_for(section_id))

    def resolve(self, text: str) -> str:
        """Substitute defined variables. Unknown references are left verbatim so
        the gap is visible in a preview rather than silently becoming empty."""
        values = {v.name: v.value for v in self.variables if v.is_valid}
        return VARIABLE_REFERENCE.sub(
            lambda match: values.get(match.group(1).upper(), match.group(0)), text
        )

    def audit(
        self,
        plan_section_ids: list[str],
        plan_budget_seconds: dict[str, int] | None = None,
        plan_titles: dict[str, str] | None = None,
    ) -> dict:
        """Cross-check the script against the plan it belongs to.

        Three things a reviewer needs to know before moving on, none of which is
        visible from either document alone:

        - **orphaned**: narration whose section was deleted from the plan. Kept,
          not dropped -- written words are expensive.
        - **unwritten**: plan sections with no narration yet.
        - **undefined_variables**: {{NAME}} used but never defined, which would
          otherwise reach the final narration as literal braces.
        - **over_budget**: sections whose narration runs well past the plan's
          estimate. Nothing flagged a 90-second section carrying 331 words.
        """
        known = set(plan_section_ids)
        written = {s.section_id for s in self.section_scripts if s.body.strip()}
        defined = {v.name for v in self.variables if v.is_valid}

        budgets = plan_budget_seconds or {}
        over_budget = [
            {
                "section_id": s.section_id,
                "title": (plan_titles or {}).get(s.section_id, s.section_id),
                "planned_seconds": budgets[s.section_id],
                "estimated_seconds": s.estimated_seconds,
            }
            for s in self.in_plan_order(plan_section_ids).section_scripts
            if budgets.get(s.section_id)
            and s.estimated_seconds > budgets[s.section_id] * OVER_BUDGET_TOLERANCE
        ]

        return {
            "orphaned_section_ids": sorted(written - known),
            "unwritten_section_ids": [sid for sid in plan_section_ids if sid not in written],
            "over_budget": over_budget,
            "undefined_variables": sorted(self.referenced_variable_names() - defined),
            "invalid_variables": [v.name for v in self.variables if v.name and not v.is_valid],
        }

    def to_dict(
        self,
        plan_section_ids: list[str] | None = None,
        plan_budget_seconds: dict[str, int] | None = None,
        plan_titles: dict[str, str] | None = None,
    ) -> dict:
        audit = self.audit(plan_section_ids or [], plan_budget_seconds, plan_titles)
        return self.model_dump(mode="json") | {
            "total_word_count": self.total_word_count,
            "total_estimated_seconds": self.total_estimated_seconds,
            "per_section": {
                s.section_id: {
                    "word_count": s.word_count,
                    "estimated_seconds": s.estimated_seconds,
                    "scene_count": len(s.scenes),
                }
                for s in self.section_scripts
            },
            # Narration no plan section points at, shown so it can be reattached
            # or deleted, rather than only counted in a warning.
            "orphaned": [
                {
                    "section_id": s.section_id,
                    "word_count": s.word_count,
                    "scene_count": len(s.scenes),
                    "preview": s.body[:160],
                }
                for s in self.section_scripts
                if s.section_id in set(audit["orphaned_section_ids"])
            ],
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
        for section in audit["over_budget"]:
            found.append(over_budget_warning(section))
        if audit["undefined_variables"]:
            found.append(
                "undefined variable(s): " + ", ".join(audit["undefined_variables"])
            )
        if audit["invalid_variables"]:
            found.append("unusable variable name(s): " + ", ".join(audit["invalid_variables"]))
        return found


def over_budget_warning(section: dict) -> str:
    """One sentence, shared by Scripting and Reviewing so they say the same thing."""
    over = round(100 * section["estimated_seconds"] / section["planned_seconds"]) - 100
    name = section.get("title") or section["section_id"]
    return (
        f"\"{name}\" runs about {section['estimated_seconds']}s against "
        f"{section['planned_seconds']}s planned ({over}% over)"
    )


# Held around every read-change-save of the script: drafting saves each section
# as it lands, and a person's edit landing between a draft's read and its save
# was lost. Re-entrant, so a writer may call another.
SCRIPT_WRITE = threading.RLock()


class ScriptStore(JsonDocumentStore[Script]):
    """Persistence for the script. Durability behaviour lives in
    `JsonDocumentStore`; this only names the path, the model and the default."""

    def __init__(self, project_root: Path) -> None:
        super().__init__(
            document_path=artifact_path(project_root, Stage.SCRIPT_STAGING),
            model_type=Script,
            build_default=Script,
            description="script",
        )

    @property
    def script_path(self) -> Path:
        """Kept as a named alias: tests and callers read better saying
        `store.script_path` than `store.document_path`."""
        return self.document_path

