"""Keeping a drafted section to its slides: checked, and revised by the agent
until nothing is left, for up to three rounds.

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
        description="Each claim in the narration or on screen that is factually wrong "
                    "-- including one that repeats a slide's own error -- or that "
                    "contradicts a slide that is itself right, as 'scene N: the claim -- "
                    "what is right'.")
    slide_wrong: list[str] = Field(
        default_factory=list,
        description="Where a SLIDE itself states something factually wrong, as 'slide "
                    "N: what it says -- what is right'. The video never repeats it: the "
                    "narration says what is right, or leaves the doubtful detail out; if "
                    "it repeats it, list that under `wrong` too.")


class RevisedScene(BaseModel):
    narration: str = Field(description="What is said aloud in this scene.")
    brief: str = Field(description="What is on screen while it is said, in the same shape "
                                   "as before.")


class RevisedSection(BaseModel):
    scenes: list[RevisedScene]
    kept: list[str] = Field(
        default_factory=list,
        description="Each flagged item you deliberately left as it was, as 'the item -- "
                    "why it is right as it is'. Empty when you changed everything flagged.")


def _numbered(scenes: list[ScriptScene]) -> str:
    return "\n\n".join(f"Scene {number}:\nNARRATION: {scene.narration}\nBRIEF: {scene.brief}"
                       for number, scene in enumerate(scenes, start=1))


def _review(source: str, scenes: list[ScriptScene], kept: list[str] | None = None
            ) -> SlideReview:
    from pipeline import llm

    reasons = ("\n\n--- left as they are on purpose by the writer, with why ---\n"
               + "\n".join(f"- {k}" for k in kept)
               + "\nFlag one of these again only if its reason does not hold.") if kept else ""
    return llm.complete_structured(
        SlideReview,
        "You check a lesson's narration against the slides it teaches. The slides are its "
        "direction: the narration should cover every point they make, in substance, and may "
        "explain, define, give context and examples. Judge like a teacher who knows the "
        "subject: list each slide's points and whether they are taught; flag only what "
        "leads away from the slides, and what is wrong. Where a slide itself is wrong, say "
        "so apart (slide_wrong), and if the narration or the screen repeats the slide's "
        "error, that is wrong too: a course never teaches an error because a slide made it.",
        f"--- the slides ---\n{source}\n\n--- the narration ---\n{_numbered(scenes)}{reasons}",
        max_tokens=REVIEW_TOKENS)


def _findings(review: SlideReview, coverage: bool = True) -> tuple[list[str], list[str]]:
    """(what leads away or is wrong, slide points not covered), trimmed."""
    claims = [c.strip() for c in [*review.wrong, *review.leads_away] if c.strip()]
    missing = [f"{p.slide}: {p.point}".strip() for p in review.points
               if not p.covered] if coverage else []
    return claims[:MOST_FINDINGS], missing[:MOST_FINDINGS]


MOST_REVISIONS = 3


class Kept(BaseModel):
    """What keeping a section to its slides ends with, for the script and the page."""
    scenes: list[ScriptScene]
    claims: list[str] = Field(default_factory=list)       # still leading away, or wrong
    missing: list[str] = Field(default_factory=list)      # slide points still not covered
    slide_wrong: list[str] = Field(default_factory=list)  # the slide is wrong: a person decides
    kept: list[str] = Field(default_factory=list)         # left on purpose, with why


def keep_to_slides(system_prompt: str, source: str, scenes: list[ScriptScene],
                    notes: list[str], title: str, own_slides: bool = True,
                    forbidden: list | tuple = ()) -> Kept:
    """The drafted scenes, checked against the slides and revised by the agent until
    nothing is left -- every point covered, nothing leading away or wrong -- for up
    to three rounds. Each round the agent decides what to change and what is right
    as it is, and says why it kept what it kept; the next check reads those reasons.
    A slide that is itself wrong goes to a person. What is still left after the
    rounds is listed for a person to see.

    A section with no slides of its own (an opening, a recap, a close) is written
    from the whole plan, and is checked for what leads away or is wrong, not for
    covering every point."""
    from pipeline import llm

    kept: list[str] = []
    slide_wrong: list[str] = []
    claims: list[str] = []
    missing: list[str] = []
    revisions = 0
    while True:
        try:
            review = _review(source, scenes, kept)
        except ModelCallFailed as failure:
            notes.append(f'"{title}": it could not be checked against its slides ({failure}).')
            break
        slide_wrong = _merged(slide_wrong, review.slide_wrong)
        claims, missing = _findings(review, own_slides)
        # Found by code, not judged: what the fact ledger forbids, said or shown.
        from pipeline.fact_ledger import broken
        claims = list(dict.fromkeys([*broken(scenes, forbidden), *claims]))
        if not claims and not missing:
            if revisions:
                notes.append(f'"{title}": checked against its slides and revised in '
                             f"{revisions} round(s); nothing is left.")
            break
        if revisions == MOST_REVISIONS:
            notes.append(f'"{title}": after {MOST_REVISIONS} rounds of revision, '
                         f"{len(missing)} point(s) and {len(claims)} sentence(s) are left "
                         "for a person.")
            break
        try:
            revised = llm.complete_structured(
                RevisedSection,
                f"{system_prompt}\n\n---\nYou are revising a section you drafted, after a "
                "check against its slides. Cover every point it names in the scene where it "
                "belongs; bring each sentence that leads away back to what the slides are "
                "about, or cut it; correct what is wrong -- where a slide itself is wrong, "
                "say what is right, or leave the doubtful detail out ('around 460 BC'), "
                "never the slide's error, in the narration or on screen. If, on reflection, "
                "a flagged item "
                "is right as it is, keep it -- and say why under `kept`. Keep the same number "
                "of scenes in the same order, change only what needs changing, and keep each "
                "brief in step with its narration (its BEATS quote the narration's words).",
                f"--- the slides ---\n{source}\n\n--- your scenes ---\n{_numbered(scenes)}"
                f"\n\n--- what the check found ---\n{_asked(claims, missing)}",
                max_tokens=REVIEW_TOKENS)
        except ModelCallFailed as failure:
            notes.append(f'"{title}": it could not be revised ({failure}); what the check '
                         "found is listed for a person.")
            break
        rewritten = [scene for scene in revised.scenes if scene.narration.strip()]
        if len(rewritten) != len(scenes):
            notes.append(f'"{title}": a revision came back with {len(rewritten)} scenes for '
                         f"{len(scenes)}; the draft is kept and what the check found is "
                         "listed.")
            break
        scenes = [scene.model_copy(update={"narration": new.narration.strip(),
                                           "brief": new.brief.strip() or scene.brief})
                  for scene, new in zip(scenes, rewritten, strict=True)]
        kept = _merged(kept, revised.kept)
        revisions += 1
    return Kept(scenes=scenes, claims=claims, missing=missing, slide_wrong=slide_wrong,
                kept=kept)


def _merged(known: list[str], new: list[str]) -> list[str]:
    return list(dict.fromkeys([*known, *(item.strip() for item in new if item.strip())]))[
        :MOST_FINDINGS]


def _asked(claims: list[str], missing: list[str]) -> str:
    return "\n".join(
        (["Slide points the narration does not cover yet:"] + [f"- {m}" for m in missing]
         if missing else [])
        + (["Sentences that lead away from the slides, or are wrong:"]
           + [f"- {c}" for c in claims] if claims else []))
