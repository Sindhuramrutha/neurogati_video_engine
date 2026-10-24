"""The program written from a scene's shots, laid out the way a person writes it.

`scene_shots.program_for` writes each statement on one line; `_laid_out` breaks a
call or a list too long for a line into one argument or item per line, keeping
every literal as written (0.60 stays 0.60), so the code a person opens in the
scene's editor reads like code, not a dump.
"""

from __future__ import annotations

from typing import Any

WIDTH = 92          # a line of the written program, at most, where it can be broken


def _one_line(text: str, most: int = 60) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= most else text[:most - 3] + "..."


def _laid_out(line: str, indent: int) -> str:
    """One statement of the program, broken over lines the way a person writes it:
    a call or a list too long for one line gets one argument or item per line,
    nested as deep as needed. Comments, and what does not parse, stay as they are."""
    import ast

    pad = " " * indent
    if line.lstrip().startswith("#") or len(pad + line) <= WIDTH:
        return pad + line
    try:
        tree = ast.parse(line)
    except SyntaxError:
        return pad + line
    if len(tree.body) != 1:
        return pad + line
    statement = tree.body[0]
    if isinstance(statement, ast.Expr):
        return pad + _layout(line, statement.value, indent)
    if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
        target = ast.get_source_segment(line, statement.targets[0]) + " = "
        return pad + target + _layout(line, statement.value, indent, len(target))
    return pad + line


def _layout(source: str, node: Any, indent: int, used: int = 0) -> str:
    """`node` of `source`, in its own words (0.60 stays 0.60), broken if too long."""
    import ast

    flat = ast.get_source_segment(source, node) or ast.unparse(node)
    if indent + used + len(flat) <= WIDTH:
        return flat
    inner = " " * (indent + 4)
    if isinstance(node, ast.Call):
        parts = [_layout(source, arg, indent + 4) for arg in node.args]
        parts += [(f"{kw.arg}=" if kw.arg else "**")
                  + _layout(source, kw.value, indent + 4, len(kw.arg or "") + 1)
                  for kw in node.keywords]
        opening, closing = ast.get_source_segment(source, node.func) + "(", ")"
    elif isinstance(node, (ast.List, ast.Tuple)):
        parts = [_layout(source, item, indent + 4) for item in node.elts]
        opening, closing = ("[", "]") if isinstance(node, ast.List) else ("(", ")")
    elif isinstance(node, ast.Starred):
        return "*" + _layout(source, node.value, indent, used + 1)
    else:
        return flat
    if not parts:
        return flat
    return (opening + "\n" + "".join(f"{inner}{part},\n" for part in parts)
            + " " * indent + closing)
