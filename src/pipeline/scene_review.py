"""A scene's clip, looked at: the vision model sees its frames in order, with the
narration, and says whether it teaches the idea and whether its motion explains.

The mechanical checks (`scene_checks.py`) catch what can be measured -- text in
the frame, overlap, contrast, length. They cannot tell a scene that explains from
one that merely shows labels and fades them away. This is the judgement that
can: a scene agent must look before it may finish, and must fix what is said.

Also: a picture (a slide picture, or the slide itself) looked at for a question,
so the agent can see what the author drew before deciding how to explain it.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

from pipeline.llm import complete_structured_with_images

REVIEW_WIDTH = 960          # frames are shrunk to this before they are sent
LONGEST_NARRATION = 1500


class Verdict(BaseModel):
    teaches: bool = Field(description="Would a learner understand the spoken idea from "
                                      "what is on screen, in time with the words?")
    motion_explains: bool = Field(description="Do things transform, move, grow, connect "
                                              "or build up to explain -- rather than labels "
                                              "only appearing and disappearing?")
    looks_finished: bool = Field(description="Would a viewer accept it as finished: "
                                             "readable, nothing cut off or overlapping, the "
                                             "frame used? Polish alone is not a no.")
    problems: list[str] = Field(default_factory=list,
                                description="At most 5 things that MUST be fixed, one short "
                                            "sentence each, most important first.")
    polish: list[str] = Field(default_factory=list,
                              description="Up to 3 optional improvements, one short sentence "
                                          "each. They do not stop the scene being finished.")
    praise: str = Field("", description="What already works, in one sentence.")

    # A longer list is trimmed, not refused: refusing it made the whole answer
    # invalid, and the agent lost turns asking again.
    @field_validator("problems")
    @classmethod
    def _five(cls, value: list[str]) -> list[str]:
        return value[:5]

    @field_validator("polish")
    @classmethod
    def _three(cls, value: list[str]) -> list[str]:
        return value[:3]

    @property
    def good(self) -> bool:
        return self.teaches and self.motion_explains and self.looks_finished


class Seen(BaseModel):
    answer: str


def _jpeg(path: Path) -> bytes:
    from PIL import Image

    with Image.open(path) as image:
        image = image.convert("RGB")
        if image.width > REVIEW_WIDTH:
            image = image.resize((REVIEW_WIDTH, round(image.height * REVIEW_WIDTH / image.width)))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=82)
        return buffer.getvalue()


def review_frames(folder: Path, brief: dict[str, Any], question: str = "") -> Verdict:
    """The latest render's sampled frames, judged against the narration."""
    from pipeline.scene_checks import FRAME_SHARES

    frames = sorted((folder / "frames").glob("frame-*.png"))
    if not frames:
        return Verdict(teaches=False, motion_explains=False, looks_finished=False,
                       problems=["There is no render to look at yet: render first."])
    seconds = float(brief.get("seconds") or 0)
    pictures = [(f"Frame at {seconds * share:.1f} s of {seconds:.1f} s:", _jpeg(path))
                for path, share in zip(frames, FRAME_SHARES, strict=False)]
    system = (
        "You review one scene of an educational explainer video, from frames sampled in "
        "order. Be a demanding art director and teacher. A scene that only shows words and "
        "fades them in and out does NOT explain by motion. Problems are what MUST change "
        "(it misleads, is unreadable, cut off, overlapping, or does not teach the words); "
        "anything that would merely make it nicer is polish. Be concrete and brief.")
    user = "\n\n".join(part for part in [
        "Narration (spoken over the scene):\n"
        + str(brief.get("narration", ""))[:LONGEST_NARRATION],
        f"What the scene should show: {brief.get('on_screen', '')}",
        f"How the section is told: {brief.get('how', '')}",
        f"The agent asks you specifically: {question}" if question.strip() else "",
        "Look at the frames below, in order.",
    ] if part)
    return complete_structured_with_images(Verdict, system, user, pictures, max_tokens=4000)


def look_at_picture(path: Path, question: str) -> str:
    """What the vision model sees in one picture, for the agent's question."""
    answer = complete_structured_with_images(
        Seen,
        "You describe a picture from a lecture slide for an animator who must explain "
        "it on screen. Be specific: parts, labels, arrows, layout, what it teaches.",
        question.strip() or "What does this picture show, part by part?",
        [(path.name, _jpeg(path))], max_tokens=1500)
    return answer.answer
