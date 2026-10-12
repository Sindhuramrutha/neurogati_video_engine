"""When a layer is transferred again, every layer after it is flagged, the flag
names what changed, and transferring the layer again clears it."""

# ruff: noqa: F811
from pipeline import operations
from pipeline.assets_handoff import confirm_assets
from pipeline.plan_handoff import read_plan_handoff, transfer_plan
from pipeline.planning import PlanStore
from pipeline.script_handoff import transfer_script
from pipeline.upstream import upstream_state
from tests.test_slide_first import (  # noqa: F401
    a_deck,
    a_deck_project,
    plan_from_slides,
    project_root,
)


def change_the_deck(slug, project, slides):
    a_deck(project.root / "sources" / "deck.pptx", slides=slides)
    operations.run_extraction(slug, "deck.pptx")
    operations.confirm_extraction(slug)


def planned_and_scripted(name, slides=3):
    slug, project = a_deck_project(name, slides=slides)
    operations.refresh_asset_library(slug)
    confirm_assets(slug)
    plan_from_slides(slug)
    transfer_plan(slug)
    for section in PlanStore(project.root).load().sections:
        operations.write_section_script(slug, section.id, f"Narration for {section.title}.")
    transfer_script(slug)
    return slug, project


def test_nothing_is_flagged_while_every_layer_is_in_step(project_root):
    slug, project = planned_and_scripted("In step")
    state = upstream_state(project)
    assert not any(layer["flagged"] for layer in state.values())


def test_a_new_transfer_flags_every_layer_after_it_and_says_what_changed(project_root):
    slug, project = planned_and_scripted("Changed", slides=3)

    change_the_deck(slug, project, slides=4)
    state = upstream_state(project)

    plan = state["scene-plan"]
    assert plan["flagged"]
    change = plan["changes"][0]
    assert change["name"] == "Extraction"
    assert change["added"] == ["slide 4"], "it names the part that is new"
    assert change["counts"] == {"added": 1, "removed": 0, "changed": 0}

    script = state["script-staging"]
    assert script["flagged"], "the script reads the extraction too"
    assert "Scene Plan" in script["behind"], "and what it was built on is now behind"
    assert read_plan_handoff(slug)["pending"], "a flagged layer can be transferred again"


def test_transferring_again_clears_the_flag_and_moves_it_down(project_root):
    slug, project = planned_and_scripted("Cleared", slides=3)
    change_the_deck(slug, project, slides=4)
    assert "Assets & Design" in upstream_state(project)["scene-plan"]["behind"], \
        "the plan is built on Assets & Design too, which is now behind"

    operations.refresh_asset_library(slug)
    confirm_assets(slug)
    plan_from_slides(slug)   # re-planned for the new deck
    transfer_plan(slug)
    state = upstream_state(project)

    assert not state["scene-plan"]["flagged"]
    script = state["script-staging"]
    assert script["flagged"]
    assert {c["name"] for c in script["changes"]} == {"Extraction", "Scene Plan"}
    added = next(c for c in script["changes"] if c["name"] == "Scene Plan")["added"]
    assert added == ["section “Heading number 4”"]


def test_an_older_project_is_taken_as_in_step_once(project_root):
    slug, project = planned_and_scripted("Older")
    (project.root / "handoffs.json").unlink()
    assert not any(layer["flagged"] for layer in upstream_state(project).values())
    assert (project.root / "handoffs.json").exists(), "adopted as it stands"


def test_a_replaced_source_shows_the_slides_that_differ_not_everything(project_root):
    """One source per project, keyed by place: a new file of the same deck says
    which slides differ, and that the source file was replaced."""
    slug, project = planned_and_scripted("Replaced", slides=3)
    (project.sources_dir / "deck.pptx").unlink()
    a_deck(project.sources_dir / "deck-v2.pptx", slides=4)
    operations.run_extraction(slug)
    operations.confirm_extraction(slug)

    change = upstream_state(project)["scene-plan"]["changes"][0]
    assert change["changed"] == ["the source file"]
    assert change["added"] == ["slide 4"] and change["removed"] == []


def test_a_record_from_before_one_source_is_adopted_once(project_root):
    """A record whose parts are keyed by file name is taken as in
    step once, rather than flagging every slide as removed and new."""
    import json

    slug, project = planned_and_scripted("Old keys")
    record = project.root / "handoffs.json"
    stored = json.loads(record.read_text(encoding="utf-8"))
    for snapshots in stored.values():
        if snapshots.get("extraction"):
            parts = snapshots["extraction"]["parts"]
            snapshots["extraction"]["parts"] = {f"deck.pptx#{k}": v for k, v in parts.items()
                                                if k != "~source"}
            snapshots["extraction"]["fingerprint"] = "old"
    record.write_text(json.dumps(stored), encoding="utf-8")

    assert not any(layer["flagged"] for layer in upstream_state(project).values())
    assert "~source" in json.loads(record.read_text(encoding="utf-8"))["scene-plan"][
        "extraction"]["parts"]


def test_the_same_transfer_described_differently_is_not_a_change(project_root):
    """When the app starts recording something new about a transfer, the record
    differs but nothing was handed on again: only a new transfer raises a flag."""
    import json

    slug, project = planned_and_scripted("Same transfer")
    record = project.root / "handoffs.json"
    stored = json.loads(record.read_text(encoding="utf-8"))
    plan_reads = stored["script-staging"]["scene-plan"]
    plan_reads["parts"]["~setup"][1] = "described-the-old-way"
    plan_reads["fingerprint"] = "old"
    record.write_text(json.dumps(stored), encoding="utf-8")

    assert not upstream_state(project)["script-staging"]["flagged"]
    assert json.loads(record.read_text(encoding="utf-8"))["script-staging"]["scene-plan"][
        "fingerprint"] != "old", "the record now describes it as it is"
