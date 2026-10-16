"""The storyboard: a card per scene, noted and approved; the first section's
approval opens Making."""
# ruff: noqa: F811

from litestar.testing import TestClient

from pipeline import storyboard
from pipeline.generation import VisualPlanStore
from pipeline.web.app import create_app
from tests.test_scene_lab import project_root, scripted_project  # noqa: F401


def first_section(project) -> str:
    return VisualPlanStore(project.root).load().visuals[0].section_id


def test_scenes_are_not_made_until_the_first_section_s_storyboard_is_approved(project_root):
    slug, project, visual = scripted_project("Gated")

    with TestClient(app=create_app()) as client:
        refused = client.post(f"/api/projects/{slug}/scene-agents", json={"visual_ids": []})
        assert refused.status_code == 400 and "storyboard" in refused.json()["detail"].lower()

        board = storyboard.approve(slug, first_section(project))
        assert board["gate"] == "" and board["sections"][0]["approved"]
        assert board["sections"][0]["required"] and not board["sections"][1]["required"]


def test_a_note_on_a_card_is_kept_for_its_scene_and_can_be_cleared(project_root):
    slug, project, visual = scripted_project("Noted")
    board = storyboard.set_note(slug, visual.id, "Use the Volta portrait")

    assert storyboard.note_for(project, visual.id) == "Use the Volta portrait"
    assert any(card["note"] == "Use the Volta portrait"
               for section in board["sections"] for card in section["cards"])
    storyboard.set_note(slug, visual.id, "")
    assert storyboard.note_for(project, visual.id) == ""


def test_preparing_a_section_makes_each_card_s_pictures(project_root, monkeypatch):
    """Each card's brief is written and what it asks for that the deck does not
    have -- a painting, a photo, icons -- is made, with the card's note."""
    slug, project, visual = scripted_project("Painted")
    section = first_section(project)
    card = next(v for v in VisualPlanStore(project.root).load().visuals
                if v.section_id == section)
    storyboard.set_note(slug, card.id, "show the leg larger")
    prepared = []
    monkeypatch.setattr("pipeline.scene_pictures.prepare",
                        lambda project, visual, brief, state, note="":
                        prepared.append((visual.id, note)) or brief)

    board = storyboard.prepare(slug, section)

    first = board["sections"][0]
    assert len(prepared) == len(first["cards"]), "every scene of the section"
    assert (card.id, "show the leg larger") in prepared, "a card's note goes with it"
    assert all(card["says"] for card in first["cards"])
