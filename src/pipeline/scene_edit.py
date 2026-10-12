"""What the model sends back, and how a few-line edit is applied.

A round's answer is plain text with fenced blocks, never code packed inside JSON:

    ```json            optional: {"renderer": ..., "approach": ..., "beats": [...]}
    ```
    ```<language>      the complete file: for the first version, or a big change
    ```
    ```edit            for a few lines: SEARCH / REPLACE pairs
    <<<<<<< SEARCH
    the lines as they are now
    =======
    the lines they become
    >>>>>>> REPLACE
    ```

An edit's SEARCH must find the lines in the current file exactly once (trailing
spaces do not matter, indentation does). Anything else is sent back to the model
to correct rather than guessed at.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

FENCE = re.compile(r"```([A-Za-z0-9_+-]*)[ \t]*\n(.*?)```", re.DOTALL)
EDIT = re.compile(r"<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE", re.DOTALL)


@dataclass
class Answer:
    spec: dict[str, Any] = field(default_factory=dict)
    code: str = ""                       # the whole file, when one was sent
    edits: list[tuple[str, str]] = field(default_factory=list)


def parse_answer(text: str) -> Answer:
    """The spec, the file and the edits in an answer, or a clear reason it is not one."""
    answer = Answer()
    if text.count("```") % 2:
        text += "\n```"                 # the last block was never closed
    for language, body in FENCE.findall(text):
        language = language.lower()
        if language == "json":
            try:
                answer.spec = json.loads(body)
            except ValueError as unreadable:
                raise ValueError(f"the ```json block is not valid JSON: {unreadable}") \
                    from unreadable
        elif language == "edit" or "<<<<<<< SEARCH" in body:
            answer.edits += EDIT.findall(body)
        elif len(body) > len(answer.code):
            answer.code = body
    if not answer.edits and "<<<<<<< SEARCH" in text:
        answer.edits = EDIT.findall(text)            # edit blocks sent without a fence
    if not isinstance(answer.spec, dict):
        raise ValueError("the ```json block must be an object")
    if answer.code.strip():
        answer.code = answer.code.strip("\n") + "\n"
        answer.edits = []
    elif not answer.edits:
        raise ValueError("the answer has neither a complete file nor an ```edit block")
    return answer


def apply_edits(code: str, edits: list[tuple[str, str]]) -> str:
    """The file with each edit made, or a ValueError naming the edit that cannot be."""
    lines = code.split("\n")
    for number, (search, replace) in enumerate(edits, start=1):
        wanted = [line.rstrip() for line in search.split("\n")]
        found = [at for at in range(len(lines) - len(wanted) + 1)
                 if [line.rstrip() for line in lines[at:at + len(wanted)]] == wanted]
        if len(found) != 1:
            raise ValueError(
                f"edit {number}: its SEARCH lines "
                + ("are not in the file as written" if not found
                   else f"are in the file {len(found)} times")
                + ". Copy the lines exactly, with enough of them to be unique -- or send "
                  "the complete file.")
        lines[found[0]:found[0] + len(wanted)] = replace.split("\n")
    return "\n".join(lines)
