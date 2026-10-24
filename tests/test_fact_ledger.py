"""The deck's facts: checked once by two models, decided by a person where a slide is
wrong, and held to by code."""

from pipeline.fact_ledger import Claim, broken
from pipeline.scripting import ScriptScene


def claim(status, says, correct="", decision=""):
    return Claim(id="x", slide=3, says=says, status=status, correct=correct,
                 decision=decision)


def test_a_disputed_figure_may_not_be_said_until_it_is_decided_for_the_slide():
    """v5's script said 'Hippocrates, who lived from 460 to 379 B.C.': the slide's
    dates, flagged, repeated in the narration and on screen."""
    hippocrates = claim("disputed", "Hippocrates is dated 460-379 B.C.",
                        "Hippocrates is dated c. 460-c. 370 B.C.")
    assert hippocrates.forbidden() == ["379"]
    scene = ScriptScene(narration="He lived from 460 to 379 B.C.", brief="LABELS: 460-379 BC")
    assert broken([scene], [(t, hippocrates.rule()) for t in hippocrates.forbidden()])
    assert "not decided yet" in hippocrates.rule()

    hippocrates.decision = "slide"
    assert hippocrates.rule() == "" and hippocrates.forbidden() == [], \
        "a person chose the slide: it may be said"
    hippocrates.decision = "fact"
    assert "say: Hippocrates is dated c. 460" in hippocrates.rule()


def test_a_misspelt_term_is_found_and_a_verified_claim_asks_nothing():
    term = claim("disputed", "This is the Syncitium theory of the nervous system.",
                 "The term is syncytium theory.")
    assert term.forbidden() == ["Syncitium"]
    assert claim("verified", "Golgi and Cajal shared the Nobel Prize in 1906.").rule() == ""
    assert not claim("verified", "Golgi won in 1906.").open
    assert claim("uncertain", "Pavlov rang a bell.").open


def test_a_decks_decisions_reach_every_version_made_of_it(tmp_path, monkeypatch):
    """v6 was erased and made again: the facts decided on it were decided again. A
    deck's decisions are kept with the deck, and an undo is kept as well."""
    from pipeline import fact_ledger
    from pipeline.fact_ledger import Ledger

    monkeypatch.setattr(fact_ledger, "_cache_path", lambda source: tmp_path / f"{source}.json")
    decided = claim("disputed", "Pavlov was a psychologist.", "a physiologist", "fact")
    decided.decided_at = "2026-10-24T09:00:00+00:00"
    fact_ledger._remember(Ledger(source="deck", claims=[decided]))
    assert fact_ledger._remembered("deck")["x"].decision == "fact"

    decided.decision = ""                                   # taken back, in any version
    fact_ledger._remember(Ledger(source="deck", claims=[decided]))
    assert fact_ledger._remembered("deck") == {}


def test_a_misspelt_name_is_found_however_short():
    """v6 and v7 said 'Anton van Leeuwenhoek': five letters slipped under the check."""
    name = claim("uncertain", "Anton van Leeuwenhoek observed animalcules in 1683.",
                 "The correct name is Antonie van Leeuwenhoek.", decision="fact")
    assert name.forbidden() == ["1683", "Anton"], "the uncertain year, and the name"
    assert broken([ScriptScene(narration="Anton van Leeuwenhoek ground lenses.", brief="")],
                  [(t, name.rule()) for t in name.forbidden()])


def test_a_plural_is_not_a_misspelling():
    """v8 held 'muscles' to be a misspelling of the correction's 'muscle'."""
    volta = claim("disputed", "Volta proved electricity in muscles is ordinary.",
                  "He did not prove muscle electricity was identical.", decision="fact")
    assert "muscles" not in volta.forbidden()
