"""AGENT.md — the agent that runs a stage.

An AGENT.md is not a prompt file. It declares a working agent: its speciality, the
tools it may operate, the external resources those tools reach, and the
instructions it follows.

    ---
    name: Graphics
    role: Realise each scene as a rendered clip.
    tools: [read_plan, write_scenes]
    ---

    # instructions, in markdown

Why this shape:

- **Capability is declared, not implicit.** An agent cannot use a tool it was not
  granted, so "what can this stage actually do?" is answerable by reading one file.
- **It is content, not code.** Anyone who owns the material can change how a
  stage behaves, without a programmer.
- **Projects override, never edit, the defaults.** Tuning one project must not
  silently change another.

Resolution is project-then-default:

    agents/<stage>/AGENT.md                       # shipped default
    projects/<project>/agents/<stage>/AGENT.md    # project override
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from pipeline.stages import Stage
from pipeline.tools import ToolGrant, resolve

FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
LIST_INLINE = re.compile(r"\[(.*?)\]", re.DOTALL)


@dataclass
class Agent:
    # `None` for an agent that does not belong to a stage. The orchestrator is
    # the one such agent: it stands above the pipeline rather than inside it, so
    # forcing it into the `Stage` enum would put it in the stepper, give it an
    # artifact to produce, and make every "for each stage" loop wrong.
    stage: Stage | None
    name: str
    role: str
    body: str
    path: Path
    is_override: bool
    tools: ToolGrant = field(default_factory=ToolGrant)

    @property
    def source(self) -> str:
        return "project" if self.is_override else "default"

    def to_dict(self) -> dict:
        return {
            "stage": self.stage.value if self.stage else None,
            "name": self.name,
            "role": self.role,
            "body": self.body,
            "source": self.source,
            "path": str(self.path),
            "tools": [
                {"name": t.name, "kind": t.kind.value, "summary": t.summary}
                for t in self.tools.granted
            ],
            "resources": [
                {
                    "name": r.name, "kind": r.kind, "summary": r.summary,
                    "licence": r.licence, "requires_key": r.requires_key,
                }
                for r in self.tools.resources
            ],
            "unknown_tools": self.tools.unknown,
        }


def _parse_frontmatter(head: str) -> dict[str, object]:
    """Minimal YAML-ish: scalars and inline lists.

    A real YAML parser is avoidable while the header stays this shape -- name,
    role, and a flat tool list. Anything more structured belongs in the body,
    where a human reads it anyway.
    """
    out: dict[str, object] = {}
    for line in head.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if m := LIST_INLINE.search(value):
            items = [i.strip().strip("\"'") for i in m.group(1).split(",")]
            out[key] = [i for i in items if i]
        else:
            out[key] = value.strip("\"'")
    return out


def parse(text: str, stage: Stage | None, path: Path, is_override: bool) -> Agent:
    name, role, body = (stage.value.title() if stage else path.parent.name.title()), "", text
    tool_names: list[str] = []

    if m := FRONTMATTER.match(text):
        head, body = m.group(1), m.group(2)
        meta = _parse_frontmatter(head)
        name = str(meta.get("name", name))
        role = str(meta.get("role", ""))
        raw_tools = meta.get("tools", [])
        tool_names = raw_tools if isinstance(raw_tools, list) else []

    return Agent(
        stage=stage,
        name=name,
        role=role,
        body=body.strip(),
        path=path,
        is_override=is_override,
        tools=resolve(tool_names),
    )


class AgentRegistry:
    def __init__(self, defaults_dir: Path, project_dir: Path | None = None) -> None:
        self.defaults_dir = defaults_dir
        self.project_dir = project_dir

    def _default_path(self, stage: Stage) -> Path:
        return self.defaults_dir / stage.value / "AGENT.md"

    def _override_path(self, stage: Stage) -> Path | None:
        if self.project_dir is None:
            return None
        return self.project_dir / "agents" / stage.value / "AGENT.md"

    def get(self, stage: Stage) -> Agent | None:
        override = self._override_path(stage)
        if override and override.exists():
            return parse(override.read_text(encoding="utf-8"), stage, override, True)
        default = self._default_path(stage)
        if default.exists():
            return parse(default.read_text(encoding="utf-8"), stage, default, False)
        return None

    def get_standalone(self, folder: str) -> Agent | None:
        """An agent that is not a stage, resolved by folder name.

        Same project-then-default rule as `get`; the only difference is that
        nothing in the pipeline produces its artifact, because it has none.
        """
        if self.project_dir is not None:
            override = self.project_dir / "agents" / folder / "AGENT.md"
            if override.exists():
                return parse(override.read_text(encoding="utf-8"), None, override, True)

        default = self.defaults_dir / folder / "AGENT.md"
        if default.exists():
            return parse(default.read_text(encoding="utf-8"), None, default, False)
        return None

    def write_override(self, stage: Stage, text: str) -> Path:
        if self.project_dir is None:
            raise ValueError("no project selected; cannot write an agent override")
        path = self._override_path(stage)
        assert path is not None
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path
