"""The video's look is planned before its scenes are made, reviewed by its director,
and made real before each scene's first round."""

import json

import pytest

from pipeline import art_direction
from pipeline.art_direction import SceneLook, SectionLooks
from pipeline.generation import VisualPlanStore
from tests.test_scene_lab import project_root, scripted_project  # noqa: F401


def look(number, kind="image"):
    return SceneLook(scene=number, style="flat cartoon", picture=f"a frog heart {number}",
                     background_kind=kind, background="a pale botanical border",
                     colours=["#fdf6ec", "#efe4ff"], layout="centre", motion="lit on words")


@pytest.mark.real_direction
def test_each_section_is_planned_then_reviewed_and_kept(project_root, monkeypatch):  # noqa: F811
    slug, project, visual = scripted_project("Directed")
    asked = []

    def model(response_model, system, user, max_tokens=0):
        asked.append(user)
        numbers = [index for index, _ in enumerate(
            VisualPlanStore(project.root).load().visuals, start=1)]
        return SectionLooks(scenes=[look(n, "gradient" if len(asked) % 2 else "image")
                                    for n in numbers])

    monkeypatch.setattr("pipeline.llm.complete_structured", model)

    art_direction.direct(slug)

    sections = len({v.section_id for v in VisualPlanStore(project.root).load().visuals})
    assert len(asked) == 2 * sections, "each section planned, then reviewed"
    assert "Review it as a demanding director" in asked[1]
    kept = art_direction.for_scene(project, visual.id)
    assert kept["background_kind"] == "image", "the reviewed plan is the one kept"
    assert json.loads((project.root / "generation" / "art-direction.json")
                      .read_text(encoding="utf-8"))["scenes"]
    art_direction.direct(slug)
    assert len(asked) == 2 * sections, "a planned section is not planned again"


@pytest.mark.real_direction
def test_a_section_too_long_for_one_answer_is_planned_in_halves(project_root,  # noqa: F811
                                                                monkeypatch):
    """v6's prepare stopped: six scenes' looks ran past the answer's length. A plan cut
    short is asked again in halves, and a review that fails keeps the first plan."""
    from pipeline.llm import ModelCallFailed

    visuals = [type("V", (), {"id": f"v{n}", "scene_id": f"s{n}", "brief": "a heart",
                              "narration_preview": "", "section_title": "One"})()
               for n in range(1, 5)]
    number = {v.id: n for n, v in enumerate(visuals, start=1)}

    def model(response_model, system, user, max_tokens=0):
        shown = [n for n in number.values() if f"Scene {n}\n" in user]
        if "Review it" in user or len(shown) > 2:
            raise ModelCallFailed("The output is incomplete due to a max_tokens length limit")
        return SectionLooks(scenes=[look(n) for n in shown])

    monkeypatch.setattr("pipeline.llm.complete_structured", model)

    looks = art_direction._plan_section(visuals, number, {}, [], [])

    assert [look.scene for look in looks] == [1, 2, 3, 4]


@pytest.mark.real_direction
def test_a_chosen_picture_is_planned_once_in_the_whole_video(project_root,  # noqa: F811
                                                             monkeypatch):
    """v6's director put the book cover in scene 1 and again in scene 30."""
    slug, project, _ = scripted_project("Once")
    visuals = VisualPlanStore(project.root).load().visuals
    offered = []

    def plan(section_visuals, number, narrations, picks, so_far):
        offered.append(list(picks))
        # As the director writes it: the name, then how it stands.
        return [look(number[v.id]).model_copy(
                    update={"picture": f"chosen: Cover, upright at a slight angle {v.id}"})
                for v in section_visuals]

    monkeypatch.setattr("pipeline.chosen_pictures.chosen", lambda project: {"c.png": "Cover"})
    monkeypatch.setattr(art_direction, "_plan_section", plan)

    art_direction.direct(slug)

    kept = [art_direction.for_scene(project, v.id)["picture"] for v in visuals]
    assert len(kept) > 1 and kept[0].startswith("chosen: Cover")
    assert sum(p.startswith("chosen") for p in kept) == 1 and kept[1:] == [""] * (len(kept) - 1)
    assert offered[0] == ["Cover"] and all(o == [] for o in offered[1:])


def test_the_director_knows_how_real_people_looked(monkeypatch):
    """Golgi was drawn with a full beard in three videos running."""
    asked = []

    def model(response_model, system, user, max_tokens=0):
        asked.append(system)
        return SectionLooks(scenes=[look(1)])

    monkeypatch.setattr("pipeline.llm.complete_structured", model)
    visual = type("V", (), {"id": "v1", "scene_id": "s1", "brief": "Golgi",
                            "narration_preview": "", "section_title": "One"})()
    art_direction._plan_section([visual], {"v1": 1}, {}, [], [])

    assert "Camillo Golgi" in asked[0] and "no beard" in asked[0]
    assert "never a row or strip" in SceneLook.model_json_schema()["properties"]["picture"][
        "description"]
