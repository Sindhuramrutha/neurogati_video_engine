"""Keeping a drafted section to its slides: checked, and revised once by the agent.

A literal fact-check once flagged 50 claims in one video -- "a dark, silent box", an
everyday comparison -- and changed none: the real drift (a section's narration
3.4 times its slide, about synapses its slide never mentions) sat among the noise,
and a slide's point (the syncytium theory) went unsaid. The slides are the
direction, not a word limit: explaining, defining, giving context and examples is
teaching. What matters is narration that leads away from them, gets them wrong, or
leaves a point out -- and the agent fixes that itself before anyone reads it.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from pipeline.llm import ModelCallFailed
from pipeline.scripting import ScriptScene

# A section's scenes and their briefs, and the model's hidden reasoning, from one
# budget (as drafting).
REVIEW_TOKENS = 65536
SLIDES_ARE_THE_DIRECTION = (
    "The slides are the direction of everything said. Cover every point they make, in "
    "substance and in their order -- explained in your own words, never read out. You "
    "may explain, define, give context, examples and plain comparisons that help a "
    "slide's point land, as long as each is accurate. Do not lead away from the slides: "
    "no new topic, story, person, date or conclusion the slides do not point toward, "
    "however interesting.")
MOST_FINDINGS = 12


class SlidePoint(BaseModel):
    slide: str = Field(description="Which slide (or part) makes it, as the source labels it.")
    point: str = Field(description="The point, in a few words.")
    covered: bool = Field(description="Whether the narration teaches this point in "
                                      "substance -- in any words, not necessarily its own.")


class SlideReview(BaseModel):
    points: list[SlidePoint] = Field(
        default_factory=list, description="Every point the source makes, slide by slide.")
    leads_away: list[str] = Field(
        default_factory=list,
        description="Each sentence that leads away from the slides -- a topic, story, "
                    "person, date or conclusion they do not point toward -- as 'scene N: "
                    "the sentence -- why'. Explanation, definitions, context, examples and "
                    "comparisons that serve a slide's point are NOT this.")
    wrong: list[str] = Field(
        default_factory=list,
        description="Each claim that is factually wrong or contradicts the slides, as "
                    "'scene N: the claim -- what is right'.")


class RevisedScene(BaseModel):
    narration: str = Field(description="What is said aloud in this scene.")
    brief: str = Field(description="What is on screen while it is said, in the same shape "
                                   "as before.")


class RevisedSection(BaseModel):
    scenes: list[RevisedScene]


def _numbered(scenes: list[ScriptScene]) -> str:
    return "\n\n".join(f"Scene {number}:\nNARRATION: {scene.narration}\nBRIEF: {scene.brief}"
                       for number, scene in enumerate(scenes, start=1))


def _review(source: str, scenes: list[ScriptScene]) -> SlideReview:
    from pipeline import llm

    return llm.complete_structured(
        SlideReview,
        "You check a lesson's narration against the slides it teaches. The slides are its "
        "direction: the narration should cover every point they make, in substance, and may "
        "explain, define, give context and examples. Judge like a teacher who knows the "
        "subject: list each slide's points and whether they are taught; flag only what "
        "leads away from the slides, and what is wrong.",
        f"--- the slides ---\n{source}\n\n--- the narration ---\n{_numbered(scenes)}",
        max_tokens=REVIEW_TOKENS)


def _findings(review: SlideReview) -> tuple[list[str], list[str]]:
    """(what leads away or is wrong, slide points not covered), trimmed."""
    claims = [c.strip() for c in [*review.wrong, *review.leads_away] if c.strip()]
    missing = [f"{p.slide}: {p.point}".strip() for p in review.points if not p.covered]
    return claims[:MOST_FINDINGS], missing[:MOST_FINDINGS]


def keep_to_slides(system_prompt: str, source: str, scenes: list[ScriptScene],
                    notes: list[str], title: str
                    ) -> tuple[list[ScriptScene], list[str], list[str]]:
    """The drafted scenes, checked against the slides and -- when they leave a point
    out, lead away from the slides, or get something wrong -- revised once by the
    agent, which decides what to change and what to keep. Returns (the scenes, the
    claims still standing, the points still not covered): the agent's last word,
    for a person to see."""
    try:
        review = _review(source, scenes)
    except ModelCallFailed as failure:
        notes.append(f'"{title}": it could not be checked against its slides ({failure}).')
        return scenes, [], []
    claims, missing = _findings(review)
    if not claims and not missing:
        return scenes, [], []

    from pipeline import llm

    asked = "\n".join(
        (["Slide points the narration does not cover yet:"] + [f"- {m}" for m in missing]
         if missing else [])
        + (["Sentences that lead away from the slides, or are wrong:"]
           + [f"- {c}" for c in claims] if claims else []))
    try:
        revised = llm.complete_structured(
            RevisedSection,
            f"{system_prompt}\n\n---\nYou are revising a section you drafted, after a "
            "check against its slides. Cover every point it names in the scene where it "
            "belongs; bring each sentence that leads away back to what the slides are "
            "about, or cut it; correct what is wrong. If, on reflection, a flagged sentence "
            "does serve a slide's point and is accurate, keep it. Keep the same number of "
            "scenes in the same order, change only what needs changing, and keep each "
            "brief in step with its narration (its BEATS quote the narration's words).",
            f"--- the slides ---\n{source}\n\n--- your scenes ---\n{_numbered(scenes)}"
            f"\n\n--- what the check found ---\n{asked}",
            max_tokens=REVIEW_TOKENS)
    except ModelCallFailed as failure:
        notes.append(f'"{title}": it could not be revised ({failure}); what the check found '
                     "is listed for a person.")
        return scenes, claims, missing
    rewritten = [scene for scene in revised.scenes if scene.narration.strip()]
    if len(rewritten) != len(scenes):
        notes.append(f'"{title}": the revision came back with {len(rewritten)} scenes for '
                     f"{len(scenes)}; the draft is kept and what the check found is listed.")
        return scenes, claims, missing
    scenes = [scene.model_copy(update={"narration": new.narration.strip(),
                                       "brief": new.brief.strip() or scene.brief})
              for scene, new in zip(scenes, rewritten, strict=True)]
    notes.append(f'"{title}": checked against its slides and revised '
                 f"({len(missing)} point(s) to cover, {len(claims)} sentence(s) to bring "
                 "back or correct).")
    try:
        still_claims, still_missing = _findings(_review(source, scenes))
    except ModelCallFailed:
        return scenes, [], []
    return scenes, still_claims, still_missing
