"""Planning against the extraction: richer sections, drafting that reads the whole
source, reviewing a draft, and knowing when a plan no longer matches.

The model is stood in for throughout. What is checked is everything around it --
what the agent is shown, what is kept of its answer, and what accepting does --
none of which depends on a real provider.
"""

import json
import re

import pytest

from pipeline import operations, plan_drafting
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    Extraction,
    ExtractionStore,
)
from pipeline.operations import OperationFailed
from pipeline.plan_drafting import DraftOutline, OutlineSection, SectionDetail
from pipeline.planning import (
    LearningObjective,
    Plan,
    PlanDraftStore,
    PlanSection,
    PlanStore,
    SourceReference,
)


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def document(file_name, parts):
    """A document from (heading, text) pairs, each heading at level 1."""
    blocks = []
    for heading, text in parts:
        blocks.append(ContentBlock(kind=BlockKind.HEADING, level=1, text=heading,
                                   heading_path=[heading]))
        blocks.append(ContentBlock(kind=BlockKind.PARAGRAPH, text=text, heading_path=[heading]))
    return ExtractedDocument(file_name=file_name, blocks=blocks)


def project_with_extraction(name, *documents):
    slug = operations.create_project(name)["slug"]
    project = operations.require_project(slug)
    for doc in documents:
        (project.sources_dir / doc.file_name).write_text("source", encoding="utf-8")
    ExtractionStore(project.root).save(Extraction(documents=list(documents)))
    return slug, project


CHAPTER = document("chapter.docx", [
    ("Signals", "Neurons produce tiny electrical signals measured in microvolts."),
    ("Electrodes", "Electrodes detect potentials that are already present."),
    ("Amplifiers", "Amplifiers raise the signal before it is digitised."),
])


# --- extraction: locations and identity ---------------------------------------------


def test_the_outline_counts_the_words_under_each_heading():
    outline = CHAPTER.heading_outline()

    assert [h["heading_path"] for h in outline] == [["Signals"], ["Electrodes"], ["Amplifiers"]]
    assert outline[0]["words"] == 8


def test_text_under_a_heading_is_only_that_part():
    text = CHAPTER.text_under(["Electrodes"])

    assert "Electrodes detect" in text
    assert "Amplifiers" not in text


def test_the_fingerprint_survives_a_rerun_that_changes_nothing():
    """Block ids are new on every run; a plan must not go stale because of that."""
    rerun = Extraction.model_validate(json.loads(Extraction(documents=[CHAPTER]).model_dump_json()))
    for doc in rerun.documents:
        for block in doc.blocks:
            block.id = "regenerated"

    assert rerun.content_fingerprint() == Extraction(documents=[CHAPTER]).content_fingerprint()


def test_the_fingerprint_changes_when_the_text_does():
    edited = document("chapter.docx", [("Signals", "Something else entirely.")])

    assert (Extraction(documents=[edited]).content_fingerprint()
            != Extraction(documents=[CHAPTER]).content_fingerprint())


def test_figures_do_not_change_the_fingerprint():
    with_figure = CHAPTER.model_copy(deep=True)
    with_figure.blocks.append(ContentBlock(kind=BlockKind.FIGURE, text="Figure 1",
                                           heading_path=["Signals"]))

    assert (Extraction(documents=[with_figure]).content_fingerprint()
            == Extraction(documents=[CHAPTER]).content_fingerprint())


# --- the plan's new fields ------------------------------------------------------------


def test_an_older_plan_still_loads():
    old = {"sections": [{"id": "s1", "title": "One", "summary": "", "estimated_seconds": 60}]}
    plan = Plan.model_validate(old)

    assert plan.sections[0].sources == []
    assert plan.sections[0].rendering_approach == ""
    assert plan.extraction_fingerprint == ""


def test_an_unknown_rendering_approach_becomes_not_chosen():
    section = PlanSection(title="x", rendering_approach="hologram")
    assert section.rendering_approach == ""
    assert PlanSection(title="x", rendering_approach="Plot").rendering_approach == "plot"


def test_links_to_a_deleted_objective_are_dropped():
    objective = LearningObjective(text="kept")
    plan = Plan(
        learning_objectives=[objective],
        sections=[PlanSection(title="x", objective_ids=[objective.id, "deleted"])],
    )
    assert plan.sections[0].objective_ids == [objective.id]


def test_an_uncovered_objective_is_reported_once_sections_link_objectives():
    covered, uncovered = LearningObjective(text="a"), LearningObjective(text="b")
    plan = Plan(
        learning_objectives=[covered, uncovered],
        sections=[PlanSection(title="x", objective_ids=[covered.id])],
    )

    assert plan.objective_coverage() == {covered.id: [plan.sections[0].id], uncovered.id: []}
    assert any("1 learning objective(s) are not covered" in w for w in plan.warnings())


def test_objective_coverage_is_not_nagged_before_any_linking():
    plan = Plan(learning_objectives=[LearningObjective(text="a")],
                sections=[PlanSection(title="x")])
    assert not any("not covered" in w for w in plan.warnings())


# --- does the plan still match the extraction? -------------------------------------------


def test_a_hand_made_plan_is_reported_as_not_linked(project_root):
    """The real case: a plan about a chapter the extraction no longer held."""
    slug, _ = project_with_extraction("Unlinked", CHAPTER)
    operations.add_plan_section(slug, title="Something else")

    freshness = operations.read_artifact(slug, "plan")["freshness"]

    assert freshness["is_unlinked"] is True
    assert freshness["is_stale"] is False


def test_confirming_links_the_plan_and_a_changed_extraction_makes_it_stale(project_root):
    slug, project = project_with_extraction("Confirm", CHAPTER)
    operations.add_plan_section(slug, title="Signals")

    confirmed = operations.confirm_plan_matches_extraction(slug)
    assert confirmed["freshness"]["is_linked"] and not confirmed["freshness"]["is_stale"]

    changed = document("chapter.docx", [("Signals", "Rewritten material.")])
    ExtractionStore(project.root).save(Extraction(documents=[changed]))

    plan = operations.read_artifact(slug, "plan")
    assert plan["freshness"]["is_stale"] is True
    assert "the extraction has changed since this plan was drafted" in plan["warnings"]


def test_a_section_whose_source_is_gone_is_flagged(project_root):
    slug, project = project_with_extraction("Missing", CHAPTER)
    store = PlanStore(project.root)
    store.save(Plan(sections=[
        PlanSection(title="Still here",
                    sources=[SourceReference(file_name="chapter.docx", heading_path=["Signals"])]),
        PlanSection(title="Gone",
                    sources=[SourceReference(file_name="chapter.docx", heading_path=["Filters"])]),
    ]))

    missing = operations.read_artifact(slug, "plan")["freshness"]["sections_with_missing_sources"]

    assert [m["title"] for m in missing] == ["Gone"]
    assert missing[0]["missing"] == ["chapter.docx › Filters"]


def test_nothing_to_confirm_without_an_extraction(project_root):
    slug = operations.create_project("Nothing Extracted")["slug"]
    with pytest.raises(OperationFailed, match="Nothing has been extracted"):
        operations.confirm_plan_matches_extraction(slug)


def test_the_planning_chip_counts_sections_not_files(project_root):
    from pipeline.stages import Stage

    slug, project = project_with_extraction("Chip", CHAPTER)
    operations.add_plan_section(slug, title="One", estimated_seconds=90)
    operations.add_plan_section(slug, title="Two", estimated_seconds=90)

    assert project.stage_state(Stage.SCENE_PLAN).detail == "2 sections · ~3 min"


# --- drafting reads everything ------------------------------------------------------------


class FakeModel:
    """Answers the outline pass with a given outline, and each section pass from the
    text it is shown. Records every prompt."""

    def __init__(self, outline, fail_for=()):
        self.outline = outline
        self.fail_for = set(fail_for)
        self.outline_prompts = []
        self.section_prompts = []

    def __call__(self, response_model, system_prompt, user_prompt, **kwargs):
        if response_model is DraftOutline:
            self.outline_prompts.append(user_prompt)
            return self.outline
        self.section_prompts.append(user_prompt)
        title = re.search(r"Section: (.+)", user_prompt).group(1)
        if title in self.fail_for:
            from pipeline.llm import ModelCallFailed
            raise ModelCallFailed("provider timed out")
        return SectionDetail(
            summary=f"Summary of {title}.", rendering_approach="composition",
            rendering_reason="A labelled diagram shows the parts.", estimated_seconds=75,
        )


def outline_of(*sections, objectives=("Explain the chain",), themes=("signals",)):
    return DraftOutline(learning_objectives=list(objectives), key_themes=list(themes),
                        sections=list(sections))


def id_for(doc, heading_path):
    """The outline id a single-document extraction gives this location."""
    _, _, index = plan_drafting.outline_for_agent(Extraction(documents=[doc]))
    return next(key for key, reference in index.items()
                if reference.file_name == doc.file_name
                and reference.heading_path == heading_path)


def source(heading):
    return id_for(CHAPTER, [heading])


def test_the_outline_pass_sees_every_heading_of_a_long_source(project_root, monkeypatch):
    """The old draft was shown the first 40,000 characters. This source is 150,000
    characters; its last heading must still reach the agent, and the section built
    on it must be written from its own text."""
    long_source = document("book.docx", [
        (f"Part {n}", f"Part {n} material. " + "word " * 1000) for n in range(1, 31)
    ])
    assert len(Extraction(documents=[long_source]).as_markdown()) > 140_000

    slug, _ = project_with_extraction("Long Source", long_source)
    fake = FakeModel(outline_of(OutlineSection(
        title="The last part", source_ids=[id_for(long_source, ["Part 30"])],
        objective_numbers=[1],
    )))
    monkeypatch.setattr(plan_drafting, "complete_structured", fake)

    draft = plan_drafting.draft_plan(slug)

    assert "h30 · Part 30 · 1,003 words" in fake.outline_prompts[0]
    assert "Part 30 material." in fake.section_prompts[0]
    assert "Part 1 material." not in fake.section_prompts[0]
    assert draft["headings_read"] == 30


def test_the_outline_names_locations_by_short_id_not_by_copied_path():
    """Copied paths filled a reasoning model's output budget and a real draft was
    cut off mid-answer; one also "tidied" a path until it matched nothing."""
    text, _, index = plan_drafting.outline_for_agent(Extraction(documents=[CHAPTER]))

    assert "=== d1 · chapter.docx" in text
    assert "- h2 · Electrodes · 7 words" in text
    assert index["d1"] == SourceReference(file_name="chapter.docx", heading_path=[])
    assert index["h2"] == SourceReference(file_name="chapter.docx", heading_path=["Electrodes"])


def test_a_draft_records_sources_approach_reason_and_objectives(project_root, monkeypatch):
    slug, project = project_with_extraction("Rich", CHAPTER)
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="What electrodes do", objective_numbers=[1],
                       source_ids=[source("Electrodes")]),
    )))

    draft = plan_drafting.draft_plan(slug)
    section = draft["plan"]["sections"][0]

    assert section["sources"] == [
        # `slide_number` is 0 for a source that is not a deck.
        {"file_name": "chapter.docx", "heading_path": ["Electrodes"], "slide_number": 0},
    ]
    assert section["rendering_approach"] == "composition"
    assert section["rendering_reason"] == "A labelled diagram shows the parts."
    assert section["estimated_seconds"] == 75
    assert section["objective_ids"] == [draft["plan"]["learning_objectives"][0]["id"]]
    assert draft["plan"]["key_themes"] == ["signals"]


def test_drafting_never_touches_the_plan(project_root, monkeypatch):
    slug, project = project_with_extraction("Untouched", CHAPTER)
    operations.add_plan_section(slug, title="Mine")
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="Theirs", source_ids=[source("Signals")]),
    )))

    draft = plan_drafting.draft_plan(slug)

    assert [s.title for s in PlanStore(project.root).load().sections] == ["Mine"]
    assert draft["is_pending"] is True
    fingerprint = ExtractionStore(project.root).load().content_fingerprint()
    assert draft["extraction_fingerprint"] == fingerprint


def test_ids_that_name_nothing_are_ignored_and_named(project_root, monkeypatch):
    slug, _ = project_with_extraction("Invented", CHAPTER)
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="Mixed", source_ids=[source("Electrodes"), "h999", "chapter 7"]),
    )))

    draft = plan_drafting.draft_plan(slug)

    assert len(draft["plan"]["sections"][0]["sources"]) == 1
    note = next(note for note in draft["notes"] if "ignored 2 source id(s)" in note)
    assert "h999" in note and "chapter 7" in note


def test_ids_are_matched_whatever_their_case(project_root, monkeypatch):
    slug, _ = project_with_extraction("Case", CHAPTER)
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="Shouted", source_ids=[source("Signals").upper()]),
    )))

    draft = plan_drafting.draft_plan(slug)

    assert draft["plan"]["sections"][0]["sources"][0]["heading_path"] == ["Signals"]


def test_a_sub_heading_already_covered_by_its_parent_collapses():
    nested = ExtractedDocument(file_name="n.docx", blocks=[
        ContentBlock(kind=BlockKind.HEADING, level=1, text="Parts", heading_path=["Parts"]),
        ContentBlock(kind=BlockKind.HEADING, level=2, text="Amplifier",
                     heading_path=["Parts", "Amplifier"]),
    ])
    _, _, index = plan_drafting.outline_for_agent(Extraction(documents=[nested]))

    kept, _ = plan_drafting.resolve_source_ids(index, ["h1", "h2", "h1"])
    assert [k.heading_path for k in kept] == [["Parts"]]

    whole, _ = plan_drafting.resolve_source_ids(index, ["h2", "d1"])
    assert [k.heading_path for k in whole] == [[]], "a whole document covers its headings"


def test_untitled_slides_are_shown_with_their_opening_words():
    """Shown only "Slide 12", the agent could not tell what a deck was about and
    left the whole deck out of a real plan."""
    deck = document("deck.pptx", [
        ("Slide 12",
         "Hebbian learning strengthens connections between neurons that fire together."),
        ("Why networks learn", "A titled slide needs no preview."),
    ])

    outline, _, _ = plan_drafting.outline_for_agent(Extraction(documents=[deck]))

    assert 'h1 · Slide 12 · 9 words — "Hebbian learning strengthens connections' in outline
    assert "A titled slide" not in outline


def test_one_failed_section_does_not_lose_the_draft(project_root, monkeypatch):
    slug, _ = project_with_extraction("Partial", CHAPTER)
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="Works", source_ids=[source("Signals")]),
        OutlineSection(title="Fails", source_ids=[source("Electrodes")]),
    ), fail_for={"Fails"}))

    draft = plan_drafting.draft_plan(slug)
    by_title = {s["title"]: s for s in draft["plan"]["sections"]}

    assert by_title["Works"]["rendering_approach"] == "composition"
    assert by_title["Fails"]["rendering_approach"] == ""
    assert by_title["Fails"]["sources"], "the outline's sources must be kept"
    assert any('"Fails" could not be detailed' in note for note in draft["notes"])


def test_an_outline_cut_off_by_the_output_limit_says_what_to_do(project_root, monkeypatch):
    """A real draft failed with a library exception about max_tokens."""
    from pipeline.llm import ModelCallFailed

    slug, _ = project_with_extraction("Cut Off", CHAPTER)

    def cut_off(response_model, system_prompt, user_prompt, **kwargs):
        raise ModelCallFailed("IncompleteOutputException: incomplete due to a max_tokens limit")

    monkeypatch.setattr(plan_drafting, "complete_structured", cut_off)

    with pytest.raises(OperationFailed, match="fewer, broader sections"):
        plan_drafting.draft_plan(slug)


def test_parts_no_section_covers_are_listed(project_root, monkeypatch):
    slug, _ = project_with_extraction("Gaps", CHAPTER)
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="Only signals", source_ids=[source("Signals")]),
    )))

    draft = plan_drafting.draft_plan(slug)

    gap_note = next(note for note in draft["notes"] if "not covered by any section" in note)
    assert "chapter.docx › Electrodes" in gap_note and "chapter.docx › Amplifiers" in gap_note


def test_drafting_needs_an_extraction(project_root):
    slug = operations.create_project("Empty")["slug"]
    with pytest.raises(OperationFailed, match="nothing extracted"):
        plan_drafting.draft_plan(slug)


# --- accepting a draft ---------------------------------------------------------------------


def drafted(slug, monkeypatch, *sections, objectives=("Explain the chain", "Name the parts")):
    monkeypatch.setattr(plan_drafting, "complete_structured",
                        FakeModel(outline_of(*sections, objectives=objectives)))
    return plan_drafting.draft_plan(slug)


def test_accepting_all_replaces_the_plan_and_links_it(project_root, monkeypatch):
    slug, project = project_with_extraction("Accept All", CHAPTER)
    operations.add_plan_section(slug, title="Old section")
    plan = PlanStore(project.root).load()
    plan.selected_audience = "Practitioners"
    PlanStore(project.root).save(plan)
    drafted(slug, monkeypatch,
            OutlineSection(title="New one", source_ids=[source("Signals")],
                           objective_numbers=[1]),
            OutlineSection(title="New two", source_ids=[source("Electrodes")],
                           objective_numbers=[2]))

    accepted = operations.accept_plan_draft(slug)

    # A new plan is a lesson: the frame wraps what was drafted.
    assert [s["title"] for s in accepted["sections"]] == [
        "Opening", "New one", "New two", "Recap", "Close"]
    assert [o["text"] for o in accepted["learning_objectives"]] == [
        "Explain the chain", "Name the parts"]
    assert accepted["selected_audience"] == "Practitioners"
    assert accepted["freshness"]["is_linked"] and not accepted["freshness"]["is_stale"]
    assert PlanDraftStore(project.root).load() is None


def test_the_draft_says_how_much_narration_accepting_all_would_detach(project_root, monkeypatch):
    slug, _ = project_with_extraction("Narrated", CHAPTER)
    section_id = operations.add_plan_section(slug, title="Narrated")["sections"][0]["id"]
    operations.write_section_script(slug, section_id, "Words already written.")
    drafted(slug, monkeypatch, OutlineSection(title="New", source_ids=[source("Signals")]))

    assert operations.read_plan_draft(slug)["replaces_narrated_sections"] == 1


def test_accepting_some_sections_appends_them_and_brings_their_objectives(
    project_root, monkeypatch
):
    slug, project = project_with_extraction("Accept Some", CHAPTER)
    plan = operations.add_plan_section(slug, title="Kept")
    PlanStore(project.root).save(Plan.model_validate(plan | {
        "learning_objectives": [{"id": "mine", "text": "Explain the chain"}],
    }))
    draft = drafted(slug, monkeypatch,
                    OutlineSection(title="Take me", source_ids=[source("Signals")],
                                   objective_numbers=[1, 2]),
                    OutlineSection(title="Leave me", source_ids=[source("Electrodes")]))
    take = next(s["id"] for s in draft["plan"]["sections"] if s["title"] == "Take me")

    accepted = operations.accept_plan_draft(slug, [take])

    assert [s["title"] for s in accepted["sections"]] == [
        "Opening", "Kept", "Take me", "Recap", "Close"], "added to the body, inside the frame"
    added = accepted["sections"][2]
    assert added["id"] != take, "an accepted section gets its own identity"
    # The matching objective is reused, the new one added -- never duplicated.
    assert [o["text"] for o in accepted["learning_objectives"]] == [
        "Explain the chain", "Name the parts"]
    assert added["objective_ids"][0] == "mine"
    # Partly accepting is not a claim the plan matches the extraction.
    assert accepted["extraction_fingerprint"] == ""
    remaining = operations.read_plan_draft(slug)
    assert remaining["is_pending"] and remaining["accepted_section_ids"] == [take]


def test_accepting_the_last_remaining_section_clears_the_draft(project_root, monkeypatch):
    slug, project = project_with_extraction("Last One", CHAPTER)
    draft = drafted(slug, monkeypatch, OutlineSection(title="Only", source_ids=[source("Signals")]))

    operations.accept_plan_draft(slug, [draft["plan"]["sections"][0]["id"]])

    assert PlanDraftStore(project.root).load() is None


def test_an_unknown_section_cannot_be_accepted(project_root, monkeypatch):
    slug, _ = project_with_extraction("Unknown Section", CHAPTER)
    drafted(slug, monkeypatch, OutlineSection(title="Only", source_ids=[source("Signals")]))

    with pytest.raises(OperationFailed, match="no section"):
        operations.accept_plan_draft(slug, ["made-up"])


def test_nothing_to_accept_without_a_draft(project_root):
    slug, _ = project_with_extraction("No Draft", CHAPTER)
    with pytest.raises(OperationFailed, match="no drafted plan"):
        operations.accept_plan_draft(slug)


def test_discarding_leaves_the_plan_alone(project_root, monkeypatch):
    slug, project = project_with_extraction("Discard", CHAPTER)
    operations.add_plan_section(slug, title="Mine")
    drafted(slug, monkeypatch, OutlineSection(title="Theirs", source_ids=[source("Signals")]))

    assert operations.discard_plan_draft(slug) == {"discarded": True}
    assert operations.read_plan_draft(slug) == {"is_pending": False}
    assert [s.title for s in PlanStore(project.root).load().sections] == ["Mine"]


# --- clients -----------------------------------------------------------------------------------


@pytest.fixture
def client(project_root):
    from litestar.testing import TestClient

    from pipeline.web import routes_project as routes_project_module
    from pipeline.web.app import create_app

    routes_project_module._service = None
    with TestClient(app=create_app()) as test_client:
        yield test_client
    routes_project_module._service = None


def test_the_plan_route_carries_freshness_and_the_source_outline(project_root, client):
    slug, _ = project_with_extraction("Route", CHAPTER)

    body = client.get(f"/api/projects/{slug}/plan").json()

    assert "freshness" in body and body["has_pending_draft"] is False
    assert body["source_outline"][0]["file_name"] == "chapter.docx"
    assert [h["heading_path"] for h in body["source_outline"][0]["headings"]][0] == ["Signals"]


def test_a_draft_can_be_reviewed_accepted_and_confirmed_over_http(
    project_root, client, monkeypatch
):
    slug, _ = project_with_extraction("Over HTTP", CHAPTER)
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="From HTTP", source_ids=[source("Signals")]))))

    created = client.post(f"/api/projects/{slug}/plan/draft", json={"instruction": ""})
    assert created.status_code == 201, created.text
    assert client.get(f"/api/projects/{slug}/plan/draft").json()["is_pending"] is True

    accepted = client.post(f"/api/projects/{slug}/plan/draft/accept", json={})
    assert accepted.status_code == 201, accepted.text
    assert accepted.json()["sections"][1]["title"] == "From HTTP"

    confirmed = client.post(f"/api/projects/{slug}/plan/confirm-extraction")
    assert confirmed.status_code == 201 and confirmed.json()["freshness"]["is_linked"]


def test_a_draft_can_be_discarded_over_http(project_root, client, monkeypatch):
    slug, _ = project_with_extraction("Discard HTTP", CHAPTER)
    monkeypatch.setattr(plan_drafting, "complete_structured", FakeModel(outline_of(
        OutlineSection(title="Gone soon", source_ids=[source("Signals")]))))
    client.post(f"/api/projects/{slug}/plan/draft", json={})

    response = client.delete(f"/api/projects/{slug}/plan/draft")

    assert response.status_code == 200 and response.json() == {"discarded": True}


async def test_mcp_offers_accepting_and_discarding_a_draft():
    from pipeline.mcp_server import server

    names = {tool.name for tool in await server.list_tools()}
    assert {"draft_plan", "accept_plan_draft", "discard_plan_draft"} <= names
