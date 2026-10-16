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

from pipeline.llm import VISION_TOKENS, complete_structured_with_images

REVIEW_WIDTH = 960          # frames are shrunk to this before they are sent
LONGEST_NARRATION = 1500


class Scores(BaseModel):
    """The rubric (docs/plans/video-quality-plan.md, section 5), 1 to 5 each. A
    yes/no reviewer passed cluttered frames and never once said "good"; scores say
    how far off a scene is, and which part to fix first."""

    teaches: int = Field(description="1-5. Does the picture show what is being said, at "
                                     "the moment it is said? 5: a learner would get it "
                                     "from the picture alone.")
    accuracy: int = Field(description="1-5. Does every drawn thing, label, name and date "
                                      "match what is said? 1: something is wrong (a human "
                                      "heart for a frog's).")
    illustration: int = Field(description="1-5. Is the subject a real, clear picture of the "
                                          "thing? 1: only words in boxes; 3: crude shapes; "
                                          "5: a clear picture in one style.")
    composition: int = Field(description="1-5. One focal point, balanced, the frame used, "
                                         "nothing overlapping or cut off.")
    labels: int = Field(description="1-5. Few, short, readable labels, each beside what it "
                                    "names; no line through words.")
    motion: int = Field(description="1-5. Things build, move, connect or highlight on the "
                                     "words that say so -- not only fade in and out.")
    finish: int = Field(description="1-5. Would it pass as a finished course video: clean, "
                                    "in colour, nothing crude or unfinished?")

    @field_validator("*")
    @classmethod
    def _one_to_five(cls, value: int) -> int:
        return max(1, min(5, int(value)))

    def ships(self) -> bool:
        """The ship bar: nothing below 3; teaching and accuracy 4 or more."""
        values = self.model_dump()
        return min(values.values()) >= 3 and self.teaches >= 4 and self.accuracy >= 4

    def mean(self) -> float:
        values = list(self.model_dump().values())
        return sum(values) / len(values)

    def weakest(self) -> list[tuple[str, int]]:
        return sorted(self.model_dump().items(), key=lambda item: item[1])


class Verdict(BaseModel):
    scores: Scores = Field(description="The rubric, every line scored 1 to 5.")
    teaches: bool = Field(description="Would a learner understand the spoken idea from "
                                      "what is on screen, in time with the words?")
    motion_explains: bool = Field(description="Do things transform, move, grow, connect "
                                              "or build up to explain -- rather than labels "
                                              "only appearing and disappearing?")
    looks_finished: bool = Field(description="Would a viewer accept it as finished: "
                                             "readable, nothing cut off or overlapping, the "
                                             "frame used, in colour, with the thing named "
                                             "pictured -- not only words in boxes? Polish "
                                             "alone is not a no.")
    problems: list[str] = Field(default_factory=list,
                                description="At most 5 things that MUST be fixed, one short "
                                            "sentence each, most important first: one for "
                                            "every score below 4, naming its line "
                                            "(\"illustration: ...\").")
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
        return (self.teaches and self.motion_explains and self.looks_finished
                and self.scores.ships())


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
        nothing = dict.fromkeys(Scores.model_fields, 1)
        return Verdict(scores=Scores(**nothing), teaches=False, motion_explains=False,
                       looks_finished=False,
                       problems=["There is no render to look at yet: render first."])
    seconds = float(brief.get("seconds") or 0)
    pictures = [(f"Frame at {seconds * share:.1f} s of {seconds:.1f} s:", _jpeg(path))
                for path, share in zip(frames, FRAME_SHARES, strict=False)]
    system = (
        "You review one scene of an educational explainer video, from frames sampled in "
        "order. Be a demanding art director and teacher. A scene that only shows words and "
        "fades them in and out does NOT explain by motion. Problems are what MUST change "
        "(it misleads, is unreadable, cut off, overlapping, or does not teach the words); "
        "anything that would merely make it nicer is polish. Be concrete and brief.\n\n"
        "These are problems, not polish -- they are what made earlier videos look mid:\n"
        "- Only words in boxes joined by lines, when the narration names a thing that can "
        "be shown (a neuron, a frog's leg, a battery, a brain region, an experiment): it "
        "does not teach by picture. Say what to draw or which offered picture to show.\n"
        "- The scene's own pictures (named in its brief, made for it, or from its own "
        "slide) are offered and none is shown, or one is shown so small or so far from "
        "what explains it that it does nothing. The deck's own art used as a backdrop "
        "while a topic is opened is fine: it keeps the video looking like the course.\n"
        "- Lines, arrows or boxes running over each other or over words.\n"
        "- Colourless outline boxes on an empty background, or most of the frame empty: "
        "it looks unfinished.\n"
        "- A painted illustration that is wrong for what is said (the wrong thing drawn, "
        "impossible anatomy or apparatus), or that has text in it.")
    elsewhere = [f"{entry['file']} ({entry.get('what', '')[:50]}): {entry['shown_in_video']}"
                 for entry in brief.get("picture_catalogue") or []
                 if not entry.get("shown_in_video", "not yet").startswith("not yet")]
    user = "\n\n".join(part for part in [
        "Narration (spoken over the scene):\n"
        + str(brief.get("narration", ""))[:LONGEST_NARRATION],
        f"What the scene should show: {brief.get('on_screen', '')}",
        f"How the section is told: {brief.get('how', '')}",
        f"Who it is for: {brief.get('audience', 'not stated')}",
        "The scene's own pictures: " + (", ".join(own_pictures(brief)) or "none"),
        ("Pictures other scenes already show (another scene's picture as this scene's "
         "main picture again is a problem -- the video looks like one scene repeated; a "
         "brief return or a close-up of a different part is fine): " + "; ".join(elsewhere))
        if elsewhere else "",
        f"The agent asks you specifically: {question}" if question.strip() else "",
        "Look at the frames below, in order.",
    ] if part)
    return complete_structured_with_images(Verdict, system, user, pictures,
                                           max_tokens=VISION_TOKENS)


def own_pictures(brief: dict[str, Any]) -> list[str]:
    """The pictures nearest the scene -- named in its brief, made for it, from its own
    slide -- as the reviewer reads them: the rest of the deck is offered too, but a
    scene is not expected to show it."""
    near = ("named", "own slide", "painted", "found", "icon")
    catalogue = brief.get("picture_catalogue")
    if catalogue is None:       # a brief from before the catalogue: all were near
        return [Path(path).name for path in (brief.get("assets") or {}).get("pictures") or []]
    # Deck furniture (a badge, a cover) and the slide itself are offered, but no
    # scene is expected to show them: a check once failed a scene for leaving out
    # its slide's only picture, a "Check for updates" badge.
    return [f"{entry['file']} ({entry.get('what', '')})"[:90] for entry in catalogue
            if any(word in entry.get("from", "") for word in near)
            and entry.get("role") not in ("furniture", "slide")]


def look_at_picture(path: Path, question: str) -> str:
    """What the vision model sees in one picture, for the agent's question."""
    answer = complete_structured_with_images(
        Seen,
        "You describe a picture from a lecture slide for an animator who must explain "
        "it on screen. Be specific: parts, labels, arrows, layout, what it teaches.",
        question.strip() or "What does this picture show, part by part?",
        [(path.name, _jpeg(path))], max_tokens=VISION_TOKENS)
    return answer.answer
