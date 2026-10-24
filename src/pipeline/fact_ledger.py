"""The deck's facts, checked once by two models, decided by a person where a slide is
wrong -- and held to by every stage that says or shows them.

Facts had no home: each stage judged them again with a prompt, and an error any one
model missed went into the video. Chapter 1's v5 script said "Hippocrates, who lived
from 460 to 379 B.C." -- a slide's dates, flagged as wrong, repeated in the narration
and on screen -- and equated negative reinforcement with punishment because a slide
did.

Here every factual claim the deck makes -- a date, a number, a name, a definition, a
scientific statement -- is taken out once, slide by slide, and checked by two
different models. Both say it is right: verified. Both say it is wrong: disputed,
with what is right, and a person decides whether the video follows the slide or the
fact. They disagree, or either is unsure: uncertain, and the video does not state
the precise detail. Until a person decides, the video states neither version. The
checks are kept by the deck's own text, so another video of the same deck checks
nothing again; the decisions are the project's.

Drafting is given each section's rules, and a code gate -- not a model's judgement
-- finds a disputed number, or a misspelt term, if the script says it all the same.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

LEDGER_FILE = "facts.json"
SLIDES_AT_ONCE = 4
CLAIMS_AT_ONCE = 12
FACT_TOKENS = 32000           # the text model reasons before it answers: 8,000 ran out


class FoundClaim(BaseModel):
    slide: int = Field(description="The slide's number.")
    says: str = Field(description="The claim exactly as the slide makes it, in one sentence.")
    kind: Literal["date", "number", "name", "definition", "science", "other"]


class FoundClaims(BaseModel):
    claims: list[FoundClaim] = Field(default_factory=list)


class ClaimVerdict(BaseModel):
    id: str
    verdict: Literal["right", "wrong", "unsure"]
    correct: str = Field("", description="If wrong: what is right, in one sentence.")
    why: str = Field("", description="In a few words.")


class Verdicts(BaseModel):
    verdicts: list[ClaimVerdict] = Field(default_factory=list)


class Claim(BaseModel):
    id: str
    slide: int
    says: str
    kind: str = "other"
    status: Literal["unchecked", "verified", "disputed", "uncertain"] = "unchecked"
    correct: str = ""
    why: str = ""
    checks: dict[str, dict[str, str]] = Field(default_factory=dict)
    decision: Literal["", "slide", "fact"] = ""     # a person's, for disputed/uncertain
    decided_at: str = ""

    @property
    def open(self) -> bool:
        return self.status in ("disputed", "uncertain") and not self.decision

    def rule(self) -> str:
        """What the script must do about this claim; empty when nothing is asked."""
        if self.status == "verified" or self.decision == "slide":
            return ""
        if self.status == "disputed" and self.decision == "fact":
            return f"Slide {self.slide} says: {self.says} -- this is wrong; say: {self.correct}"
        if self.status == "disputed":
            return (f"Slide {self.slide} says: {self.says} -- it may be wrong ({self.correct}) "
                    "and is not decided yet: teach the point without stating this detail "
                    "either way.")
        if self.status == "uncertain":
            return (f"Slide {self.slide} says: {self.says} -- not certain: keep this detail "
                    "general, without the precise figure or name.")
        return ""

    def forbidden(self) -> list[str]:
        """What the script may not say, found by code: the slide's own figure where it
        is disputed or uncertain, and a misspelt term where the right one is known."""
        if not self.rule():
            return []
        said = set(re.findall(r"\d{2,}", self.says))
        right = set(re.findall(r"\d{2,}", self.correct))
        words = [w for w in re.findall(r"[A-Za-z]{6,}", self.says)]
        known = {w.lower() for w in re.findall(r"[A-Za-z]{6,}", self.correct)}
        misspelt = [w for w in words if w.lower() not in known
                    and any(_close(w.lower(), k) for k in known)]
        return sorted(said - right) + misspelt


class Ledger(BaseModel):
    source: str = ""
    built_at: str = ""
    claims: list[Claim] = Field(default_factory=list)


def _close(a: str, b: str) -> bool:
    """One or two letters apart: a misspelling, not another word."""
    if a == b or abs(len(a) - len(b)) > 2:
        return False
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1,
                               previous[j - 1] + (ca != cb)))
        previous = current
    return previous[-1] <= 2


# --- reading and keeping -----------------------------------------------------------------


def load(project) -> Ledger:
    try:
        return Ledger.model_validate_json(
            (project.root / LEDGER_FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return Ledger()


def _save(project, ledger: Ledger) -> None:
    from pipeline.storage.documents import write_text_atomically

    write_text_atomically(project.root / LEDGER_FILE, ledger.model_dump_json(indent=1))


def view(slug: str) -> dict[str, Any]:
    from pipeline.core import require_project

    ledger = load(require_project(slug))
    order = {"disputed": 0, "uncertain": 1, "unchecked": 2, "verified": 3}
    claims = sorted(ledger.claims, key=lambda c: (order[c.status], c.slide))
    return {"built_at": ledger.built_at, "open": sum(c.open for c in ledger.claims),
            "counts": {s: sum(c.status == s for c in ledger.claims) for s in order},
            "claims": [c.model_dump() | {"open": c.open} for c in claims]}


def decide(slug: str, claim_id: str, decision: str) -> dict[str, Any]:
    """A person's decision on a disputed or uncertain claim: follow the slide, or the
    fact; empty takes it back. The sections that teach it are drafted again."""
    from pipeline.core import OperationFailed, require_project

    if decision not in ("slide", "fact", ""):
        raise OperationFailed("Decide 'slide' or 'fact'.")
    project = require_project(slug)
    ledger = load(project)
    claim = next((c for c in ledger.claims if c.id == claim_id), None)
    if claim is None:
        raise OperationFailed("This project has no such fact.")
    claim.decision = decision
    claim.decided_at = datetime.now(UTC).isoformat(timespec="seconds") if decision else ""
    _save(project, ledger)
    return view(slug)


def open_count(project) -> int:
    return sum(c.open for c in load(project).claims)


# --- what a section is held to ---------------------------------------------------------


def _slides_of(section) -> set[int]:
    return {ref.slide_number for ref in getattr(section, "sources", []) or []
            if getattr(ref, "slide_number", 0)}


def rules_for(project, section) -> list[str]:
    slides = _slides_of(section)
    return [c.rule() for c in load(project).claims
            if c.rule() and (not slides or c.slide in slides)]


def forbidden_for(project, section) -> list[tuple[str, str]]:
    """(what may not be said, the rule it breaks) for this section's slides."""
    slides = _slides_of(section)
    return [(token, claim.rule()) for claim in load(project).claims
            if not slides or claim.slide in slides for token in claim.forbidden()]


def broken(scenes: list, forbidden: list[tuple[str, str]]) -> list[str]:
    """Each scene that says or shows what the facts forbid, as a claim to correct."""
    found = []
    for number, scene in enumerate(scenes, start=1):
        text = f"{scene.narration}\n{scene.brief}".lower()
        for token, rule in forbidden:
            if re.search(rf"(?<![a-z0-9]){re.escape(token.lower())}(?![a-z0-9])", text):
                found.append(f"scene {number}: says '{token}' -- {rule}")
    return list(dict.fromkeys(found))


# --- building -------------------------------------------------------------------------


def build(slug: str) -> dict[str, Any]:
    """The deck's claims, checked -- from the cache when this deck was checked before.
    A person's decisions are kept for every claim that is still the same."""
    from pipeline.core import require_project
    from pipeline.extraction import ExtractionStore

    project = require_project(slug)
    extraction = ExtractionStore(project.root).load()
    slides = _slides(extraction)
    source = hashlib.sha256(json.dumps(slides, sort_keys=True).encode()).hexdigest()[:16]
    before = {c.id: c for c in load(project).claims}
    claims = _cached(source)
    if claims is None:
        claims = _verify(_extract(slides))
        _cache(source, claims)
    for claim in claims:
        if claim.id in before:
            claim.decision, claim.decided_at = before[claim.id].decision, \
                before[claim.id].decided_at
    ledger = Ledger(source=source, claims=claims,
                    built_at=datetime.now(UTC).isoformat(timespec="seconds"))
    _save(project, ledger)
    return view(slug)


def _slides(extraction) -> dict[int, str]:
    found: dict[int, list[str]] = {}
    for document in extraction.documents:
        for block in document.blocks:
            if block.slide_number and block.text and block.kind != "figure":
                found.setdefault(block.slide_number, []).append(block.text)
    return {number: "\n".join(lines) for number, lines in sorted(found.items())}


def _cache_path(source: str):
    from pipeline.config import REPO_ROOT

    return REPO_ROOT / ".cache" / "facts" / f"{source}.json"


def _cached(source: str) -> list[Claim] | None:
    try:
        found = json.loads(_cache_path(source).read_text(encoding="utf-8"))
        return [Claim.model_validate(c) for c in found]
    except (OSError, ValueError):
        return None


def _cache(source: str, claims: list[Claim]) -> None:
    from pipeline.storage.documents import write_text_atomically

    path = _cache_path(source)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomically(path, json.dumps(
        [c.model_dump(exclude={"decision", "decided_at"}) for c in claims],
        ensure_ascii=False, indent=1))


def _extract(slides: dict[int, str]) -> list[Claim]:
    from pipeline.llm import complete_structured

    numbers = list(slides)
    claims: dict[str, Claim] = {}
    for start in range(0, len(numbers), SLIDES_AT_ONCE):
        chunk = numbers[start:start + SLIDES_AT_ONCE]
        text = "\n\n".join(f"--- slide {n} ---\n{slides[n]}" for n in chunk)
        found = complete_structured(
            FoundClaims,
            "You list every factual claim a lecture deck makes, slide by slide, so each "
            "can be checked: dates, numbers, who did or said what, definitions, scientific "
            "statements. Copy each as the slide makes it, one sentence each. Leave out "
            "opinions, questions, headings and teaching prose that claims nothing.",
            text, max_tokens=FACT_TOKENS)
        for item in found.claims:
            if item.slide in chunk and item.says.strip():
                key = hashlib.sha256(f"{item.slide}|{item.says.strip()}".encode()) \
                    .hexdigest()[:12]
                claims[key] = Claim(id=key, slide=item.slide, says=item.says.strip(),
                                    kind=item.kind)
    return list(claims.values())


def _verify(claims: list[Claim]) -> list[Claim]:
    """Each claim checked by the text model and, apart, by the vision model; only their
    agreement settles it."""
    from pipeline.llm import complete_structured, complete_structured_with_images

    system = ("You are a careful fact checker for a course. For each claim say whether it "
              "is right, wrong, or that you are unsure, as a specialist would judge it. "
              "'wrong' only when you are confident, with what is right in one sentence. "
              "Approximate dates given as exact, or a common misspelling, count as wrong.")
    asks = {"text": lambda user: complete_structured(Verdicts, system, user,
                                                     max_tokens=FACT_TOKENS),
            "vision": lambda user: complete_structured_with_images(Verdicts, system, user, [],
                                                                    max_tokens=FACT_TOKENS)}
    for start in range(0, len(claims), CLAIMS_AT_ONCE):
        chunk = claims[start:start + CLAIMS_AT_ONCE]
        user = "\n".join(f"{c.id}: (slide {c.slide}) {c.says}" for c in chunk)
        for name, ask in asks.items():
            try:
                verdicts = {v.id: v for v in ask(user).verdicts}
            except Exception as failure:          # one checker down: the other alone is not enough
                verdicts = {c.id: ClaimVerdict(id=c.id, verdict="unsure",
                                               why=f"not checked: {failure}"[:120])
                            for c in chunk}
            for claim in chunk:
                found = verdicts.get(claim.id)
                claim.checks[name] = {"verdict": found.verdict if found else "unsure",
                                      "correct": found.correct if found else "",
                                      "why": found.why if found else ""}
    for claim in claims:
        verdicts = [check["verdict"] for check in claim.checks.values()]
        if verdicts == ["right", "right"]:
            claim.status = "verified"
        elif verdicts == ["wrong", "wrong"]:
            claim.status = "disputed"
            claim.correct = claim.checks["text"]["correct"] or claim.checks["vision"]["correct"]
            claim.why = claim.checks["text"]["why"]
        else:
            claim.status = "uncertain"
            wrong = [c for c in claim.checks.values() if c["verdict"] == "wrong"]
            claim.correct = wrong[0]["correct"] if wrong else ""
            claim.why = "; ".join(f"{name}: {c['verdict']} {c['why']}".strip()
                                  for name, c in claim.checks.items())[:240]
    return claims


# --- after a person decides ------------------------------------------------------------


def sections_touched(project) -> list:
    """The plan's sections that teach a fact a person has decided."""
    from pipeline.plan_handoff import plan_for_later_stages

    decided = {c.slide for c in load(project).claims if c.decision}
    return [section for section in plan_for_later_stages(project).sections
            if _slides_of(section) & decided]


def apply(slug: str) -> dict[str, Any]:
    """Draft again every section that teaches a decided fact, so the narration and
    the screen say what was decided; its scenes are made again from the new script."""
    from pipeline.core import require_project
    from pipeline.script_drafting import draft_section

    project = require_project(slug)
    redrafted = []
    for section in sections_touched(project):
        draft_section(slug, section.id)
        redrafted.append(section.title)
    return view(slug) | {"redrafted": redrafted}


def corrections_markdown(project) -> str:
    """For the course team: what the slides may have wrong, and what the video says --
    so the deck itself can be put right. Empty when nothing was found."""
    claims = [c for c in load(project).claims if c.status in ("disputed", "uncertain")]
    if not claims:
        return ""
    said = {"slide": "as the slide says", "fact": "the checked fact",
            "": "neither, kept general (not decided yet)"}
    lines = [f"# Facts to check in the deck -- {project.name}", "",
             "Each claim below was checked by two models. Where a slide may be wrong, the "
             "video says what was decided.", ""]
    for claim in sorted(claims, key=lambda c: c.slide):
        status = "may be wrong" if claim.status == "disputed" else "uncertain"
        general = claim.status == "uncertain" and claim.decision == "fact"
        says = "it kept general" if general else said[claim.decision]
        lines += [f"## Slide {claim.slide} ({status})", f"- The slide: {claim.says}",
                  *([f"- The checkers: {claim.correct}"] if claim.correct else []),
                  f"- The video says: {says}", ""]
    return "\n".join(lines)


def ensure(slug: str) -> None:
    """The ledger, built before a script is drafted when it is missing or was built
    from another extraction: a section drafted without it is held to nothing."""
    from pipeline.core import require_project
    from pipeline.extraction import ExtractionStore

    project = require_project(slug)
    slides = _slides(ExtractionStore(project.root).load())
    if not slides:
        return
    source = hashlib.sha256(json.dumps(slides, sort_keys=True).encode()).hexdigest()[:16]
    if load(project).source != source:
        build(slug)
