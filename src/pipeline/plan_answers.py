"""What the planning agent answers: the video's shape, then each section's scenes.

Its own module so `plan_agent.py`, which asks for them and acts on them, stays within
its length.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ShapeSection(BaseModel):
    title: str = Field(description="What this section is about, as a short title.")
    units: list[int] = Field(
        default_factory=list,
        description="The numbers of the slides (or parts) it covers, in the order taught. "
                    "Empty for a section that is about no slide (an opening, a recap, or "
                    "anything else the video needs).")
    how: str = Field(description="In your own words, how this section should be told from "
                                 "its slides: its approach, voice and purpose in this video. "
                                 "Built on what the slides say -- no story, person or fact "
                                 "they do not point toward.")
    minutes: float = Field(description="How long the section runs.")
    scenes: int = Field(description="How many scenes it is made of.")
    summary: str = Field(description="One sentence: what the viewer gets from it.")
    opens_on: str = Field(
        default="",
        description="How it picks up from the section before -- the thread, question or "
                    "term it takes on ('answers the question the opening posed: where does "
                    "thought live?'). The first section: how the video opens.")
    ends_on: str = Field(
        default="",
        description="What it hands to the next section -- the idea, question or term the "
                    "next one opens on. Never a question the next section asks again; the "
                    "next answers or builds on it. The last section: how the video closes.")
    shows_chosen: list[str] = Field(
        default_factory=list,
        description="Names of the person's chosen pictures this section shows that are NOT "
                    "on its own slides -- e.g. a title slide's cover shown in the opening. "
                    "A chosen picture on a slide the section covers is shown there anyway.")


class LeftOut(BaseModel):
    unit: int
    why: str


class ShapeAnswer(BaseModel):
    reply: str = Field(description="To the person, in a few plain sentences: what you "
                                   "planned and why, and anything you need from them.")
    shortest_minutes: float = Field(description="The shortest length they would accept.")
    longest_minutes: float = Field(description="The longest length they would accept.")
    length_understood: str = Field(
        description="Their length request in one short sentence, as you understood it, "
                    "e.g. 'About 60 min. May run longer, not shorter.'")
    teaches: str = Field(
        default="",
        description="In one or two sentences, to the viewer: what they will come away "
                    "knowing from this video, as part of its course.")
    sections: list[ShapeSection]
    left_out: list[LeftOut] = Field(
        default_factory=list, description="Slides (or parts) deliberately not covered.")


class DetailedScene(BaseModel):
    does: str = Field(description="In one sentence: what this scene says and shows.")
    units: list[int] = Field(default_factory=list,
                             description="The slide numbers (or parts) it is about.")
    seconds: int
    opens_on: str = Field(default="", description="The thread it picks up from the scene "
                                                  "before -- what that scene ended on.")
    ends_on: str = Field(default="", description="What it hands to the next scene: the "
                                                 "idea, question or term that one opens on.")
    pause_after: float = Field(
        default=0.0,
        description="Seconds of quiet after it, 0 to 2, as the moment needs: 0 when the "
                    "thought runs straight on; about 1 at a turn to a new idea; up to 2 "
                    "after a section's last scene, a question left to think about, or a "
                    "reveal that should land.")
    pause_why: str = Field(default="", description="Why that pause, in a few words.")


class SceneAnswer(BaseModel):
    scenes: list[DetailedScene]
