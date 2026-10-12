"""The resource library every scene agent draws on.

The agent itself is `scene_agent.py`. It is shown the contract
(`resources/methods/scene-contract.md`), every method note (`motion.md` among
them), and an index of the code and assets here.

Adding a file to `resources/` is how a person teaches the agent a technique, a
component or a house style: the next scene it writes is shown it.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from pipeline.core import OperationFailed
from pipeline.scene_lab import resources_root

RESOURCE_KINDS = {"code": {".py"}, "methods": {".md", ".py", ".txt"},
                  "assets": {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ttf", ".otf",
                             ".json", ".csv", ".mp3", ".wav"}}
LONGEST_METHOD_CHARACTERS = 6000
LARGEST_RESOURCE_BYTES = 25 * 1024 * 1024


# --- the resource library ------------------------------------------------------------------


def _about(path: Path) -> str:
    """One line saying what a resource is for: its docstring, or its first heading."""
    if path.suffix == ".py":
        try:
            docstring = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
        except (SyntaxError, UnicodeDecodeError):
            docstring = ""
        return docstring.strip().splitlines()[0] if docstring.strip() else ""
    if path.suffix in (".md", ".txt"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                return line.strip().lstrip("# ")
    return f"{path.stat().st_size // 1024 or 1} KB"


def resource_index() -> dict[str, list[dict[str, str]]]:
    """Everything in the resource library, by kind, in name order."""
    index: dict[str, list[dict[str, str]]] = {}
    for kind in RESOURCE_KINDS:
        folder = resources_root() / kind
        index[kind] = [{"name": path.name, "about": _about(path)}
                       for path in sorted(folder.glob("*")) if path.is_file()
                       and not path.name.startswith(".")] if folder.exists() else []
    return index


def add_resource(kind: str, file_name: str, content: bytes) -> dict[str, Any]:
    """Put a file in the library. The next scene the agent writes is shown it."""
    if kind not in RESOURCE_KINDS:
        raise OperationFailed(f"{kind!r} is not a kind of resource. One of: code, methods, assets.")
    name = Path(file_name).name
    if Path(name).suffix.lower() not in RESOURCE_KINDS[kind]:
        raise OperationFailed(
            f"{kind} takes {', '.join(sorted(RESOURCE_KINDS[kind]))}; {name} is not one.")
    if len(content) > LARGEST_RESOURCE_BYTES:
        raise OperationFailed(f"{name} is larger than 25 MB.")
    folder = resources_root() / kind
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(content)
    return resource_index()


def remove_resource(kind: str, file_name: str) -> dict[str, Any]:
    if kind not in RESOURCE_KINDS:
        raise OperationFailed(f"{kind!r} is not a kind of resource.")
    (resources_root() / kind / Path(file_name).name).unlink(missing_ok=True)
    return resource_index()


def _library_for_agent() -> str:
    index = resource_index()
    parts = ["## The resource library\n"]
    for note in sorted((resources_root() / "methods").glob("*")):
        if note.is_file():
            text = note.read_text(encoding="utf-8", errors="replace")
            parts.append(f"### methods/{note.name}\n{text[:LONGEST_METHOD_CHARACTERS]}")
    parts.append("### code (importable by name)\n" + ("\n".join(
        f"- {entry['name']}: {entry['about']}" for entry in index["code"]) or "(none)"))
    parts.append("### assets (in the SCENE_RESOURCES folder)\n" + ("\n".join(
        f"- {entry['name']} ({entry['about']})" for entry in index["assets"]) or "(none yet)"))
    return "\n\n".join(parts)
