"""A plan against the extraction: where its sections point, and knowing when it
no longer matches what was extracted."""

import json

import pytest

from pipeline import operations
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    Extraction,
    ExtractionStore,
)
from pipeline.planning import (
    Plan,
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
    assert plan.extraction_fingerprint == ""


def test_a_hand_made_plan_is_reported_as_not_linked(project_root):
    """The real case: a plan about a chapter the extraction no longer held."""
    slug, _ = project_with_extraction("Unlinked", CHAPTER)
    operations.add_plan_section(slug, title="Something else")

    freshness = operations.read_artifact(slug, "plan")["freshness"]

    assert freshness["is_unlinked"] is True
    assert freshness["is_stale"] is False


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


def test_the_planning_chip_counts_sections_not_files(project_root):
    from pipeline.stages import Stage

    slug, project = project_with_extraction("Chip", CHAPTER)
    operations.add_plan_section(slug, title="One", estimated_seconds=90)
    operations.add_plan_section(slug, title="Two", estimated_seconds=90)

    assert project.stage_state(Stage.SCENE_PLAN).detail == "2 sections · ~3 min"


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


async def test_mcp_offers_the_planning_conversation():
    from pipeline.mcp_server import server

    names = {tool.name for tool in await server.list_tools()}
    assert {"plan_say", "plan_agree", "plan_discard"} <= names
    assert not names & {"draft_plan", "accept_plan_draft", "discard_plan_draft"}
