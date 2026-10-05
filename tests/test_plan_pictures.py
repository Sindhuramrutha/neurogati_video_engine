"""The chain is strict: Extraction → Assets & Design → Scene Plan → everything
after. The plan attaches pictures to sections and carries them, the brand kit
and the look on; no later layer reads Assets & Design directly."""
# ruff: noqa: F811

import pytest

from pipeline import operations
from pipeline.assets import set_picture
from pipeline.assets_handoff import confirm_assets
from pipeline.lesson_plan import save_plan
from pipeline.operations import OperationFailed
from pipeline.plan_handoff import FAIL, PASS, TransferredPlanStore, plan_checks, transfer_plan
from pipeline.plan_pictures import assets_for_later_stages, choose_section_pictures
from pipeline.planning import PlanStore
from pipeline.render_run import pictures_for_sections
from pipeline.upstream import upstream_state
from tests.test_assets_and_export import (  # noqa: F401
    project_root,
    project_with_sourced_sections,
)


def stems(paths):
    return [p.stem.split("-")[0] for p in paths]


def with_assets_transferred(name="Chain"):
    slug, project = project_with_sourced_sections(None)
    operations.refresh_asset_library(slug)
    confirm_assets(slug)
    save_plan(project, PlanStore(project.root).load())
    return slug, project


def test_the_plan_cannot_be_transferred_before_assets_and_design(project_root):
    slug, project = project_with_sourced_sections(project_root)

    checks = {c["key"]: c for c in plan_checks(project, PlanStore(project.root).load())}
    assert checks["assets"]["status"] == FAIL
    with pytest.raises(OperationFailed, match="Assets & Design has never been transferred"):
        transfer_plan(slug)

    operations.refresh_asset_library(slug)
    confirm_assets(slug)
    transfer_plan(slug)
    checks = {c["key"]: c for c in plan_checks(project, PlanStore(project.root).load())}
    assert checks["assets"]["status"] == PASS


def test_each_section_gets_the_pictures_from_its_own_place(project_root):
    slug, project = with_assets_transferred()
    sections = {s.id: s for s in PlanStore(project.root).load().sections}

    assert [p.split("/")[-1] for p in sections["s1"].picture_paths] == ["one.png"]
    assert [p.split("/")[-1] for p in sections["s2"].picture_paths] == ["two.png"]
    assert not any("loose" in p for s in sections.values() for p in s.picture_paths), \
        "a picture under a heading no section covers belongs to none"


def test_a_person_attaches_and_detaches_pictures_and_can_hand_back_to_the_rule(project_root):
    slug, project = with_assets_transferred()
    loose = "extraction/assets/loose.png"

    plan = choose_section_pictures(slug, "s1", [loose])
    s1 = next(s for s in plan.sections if s.id == "s1")
    assert s1.picture_paths == [loose] and s1.pictures_chosen

    with pytest.raises(OperationFailed, match="Only a picture that can fill a frame"):
        choose_section_pictures(slug, "s1", ["extraction/assets/never.png"])

    plan = choose_section_pictures(slug, "s1", None)
    s1 = next(s for s in plan.sections if s.id == "s1")
    assert [p.split("/")[-1] for p in s1.picture_paths] == ["one.png"]
    assert not s1.pictures_chosen


def test_later_layers_show_the_pictures_the_plan_attached(project_root):
    slug, project = with_assets_transferred()
    choose_section_pictures(slug, "s2", ["extraction/assets/loose.png"])
    transfer_plan(slug)

    plan = TransferredPlanStore(project.root).load().plan
    chosen = pictures_for_sections(project, plan.model_dump(mode="json"))
    assert stems(chosen["s1"]) == ["one"]
    assert stems(chosen["s2"]) == ["loose"], "exactly the section's pictures, nothing else"


def test_later_layers_read_what_the_plan_carried_not_assets_and_design(project_root):
    slug, project = with_assets_transferred()
    transfer_plan(slug)

    # Assets & Design moves on: a picture is left out, and transferred again.
    library = operations.read_asset_library(slug)
    one = next(f for f in library["figures"] if f["asset_path"].endswith("one.png"))
    set_picture(slug, one["id"], {"left_out": True})
    confirm_assets(slug)

    carried = assets_for_later_stages(project).library
    assert any(f.asset_path.endswith("one.png") for f in carried.usable()), \
        "the plan still carries what was transferred with it"
    state = upstream_state(project)
    assert state["scene-plan"]["flagged"]
    assert state["scene-plan"]["changes"][0]["name"] == "Assets & Design"

    transfer_plan(slug)
    carried = assets_for_later_stages(project).library
    assert not any(f.asset_path.endswith("one.png") for f in carried.usable())
    plan = TransferredPlanStore(project.root).load().plan
    assert next(s for s in plan.sections if s.id == "s1").picture_paths == []
    assert not upstream_state(project)["scene-plan"]["flagged"]


def test_the_script_agent_is_told_each_section_s_pictures(project_root):
    from pipeline.script_drafting import _section_brief, section_pictures

    slug, project = with_assets_transferred()
    plan = PlanStore(project.root).load()
    pictures = section_pictures(project, plan)

    brief = _section_brief(plan, plan.sections[0], 100, pictures["s1"])
    assert "Pictures from the source this section shows" in brief
    assert "Figure 1" in brief
    assert "Figure 2" not in brief


def test_a_source_with_no_pictures_can_still_be_transferred(project_root):
    from pipeline.extraction import ExtractionStore

    slug, project = project_with_sourced_sections(project_root)
    extraction = ExtractionStore(project.root).load()
    for document in extraction.documents:
        document.blocks = [b for b in document.blocks if b.kind != "figure"]
    ExtractionStore(project.root).save(extraction)

    confirm_assets(slug)
    transfer_plan(slug)
    assert TransferredPlanStore(project.root).load().assets is not None


def test_a_picture_gathered_before_slides_were_recorded_finds_its_slide_by_title():
    from pipeline.assets import AssetLibrary, LibraryFigure
    from pipeline.plan_pictures import by_rule
    from pipeline.planning import PlanSection, SourceReference

    old = LibraryFigure(asset_path="extraction/assets/a.png", heading_path=["Feeling"],
                        width=800, height=600, use="use")
    section = PlanSection(sources=[SourceReference(
        file_name="deck.pptx", heading_path=["Feeling"], slide_number=1)])
    assert by_rule(section, AssetLibrary(figures=[old])) == ["extraction/assets/a.png"]
