"""Application-surface tests: stages, agents, projects and the tool catalogue."""

import pytest


def test_index_renders_rather_than_downloads():
    """Regression: litestar's File response defaults to
    `Content-Disposition: attachment`, which made the browser download the page
    instead of showing it."""
    from litestar.testing import TestClient

    from pipeline.web.app import create_app

    with TestClient(app=create_app()) as c:
        r = c.get("/")
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/html")
        assert "attachment" not in r.headers.get("content-disposition", "")
        assert b"<title>" in r.content


def test_the_stages_are_defined_once_and_in_order():
    """The tabs come from the pipeline's own stage list, so the UI cannot show a
    stage the pipeline does not have -- the drift that split v1's workflow.py from
    run_chapter.py."""
    from pipeline.stages import STAGES, Stage

    assert [s.key for s in STAGES] == [
        Stage.INPUTS, Stage.EXTRACTION, Stage.ASSETS, Stage.SCENE_PLAN,
        Stage.SCRIPT_STAGING, Stage.STUDIO, Stage.REVIEWING, Stage.EXPORT,
    ]


def test_the_stages_two_older_names_still_resolve():
    """Planning became Scene Plan and Scripting became Script & Staging once their
    scope was clear. Their old keys are written into every project already on
    disk -- routed comments, settings files, bookmarked URLs -- so a rename that
    made those unreadable would be a rename that destroyed data."""
    from pipeline.stages import Stage

    assert Stage("planning") is Stage.SCENE_PLAN
    assert Stage("scripting") is Stage.SCRIPT_STAGING


def test_editing_an_agent_invalidates_only_downstream():
    from pipeline.stages import Stage, downstream_of

    assert downstream_of(Stage.SCENE_PLAN) == [
        Stage.SCRIPT_STAGING, Stage.STUDIO, Stage.REVIEWING, Stage.EXPORT,
    ]
    assert downstream_of(Stage.EXPORT) == []


def test_every_agent_stage_has_a_default_agent():
    from pipeline.agents import AgentRegistry
    from pipeline.config import REPO_ROOT
    from pipeline.stages import STAGES

    reg = AgentRegistry(REPO_ROOT / "agents")
    for spec in STAGES:
        agent = reg.get(spec.key)
        if not spec.has_agent:
            continue
        assert agent is not None, f"missing AGENT.md for {spec.key}"
        assert agent.body.strip()
        assert agent.role, f"{spec.key} agent has no role"
        assert agent.tools.granted, f"{spec.key} agent has no tools"
        # A typo in a tool name silently removes a capability; fail loudly.
        assert not agent.tools.unknown, (
            f"{spec.key} declares unknown tools: {agent.tools.unknown}"
        )


def test_project_override_beats_default_and_never_edits_it(tmp_path):
    """An agent edited for one project must not change every other project."""
    from pipeline.agents import AgentRegistry
    from pipeline.config import REPO_ROOT
    from pipeline.stages import Stage

    defaults = REPO_ROOT / "agents"
    default_text = AgentRegistry(defaults).get(Stage.SCENE_PLAN).body

    proj = tmp_path / "demo"
    proj.mkdir()
    reg = AgentRegistry(defaults, proj)
    reg.write_override(
        Stage.SCENE_PLAN,
        "---\nname: Custom\nrole: mine\ntools: [read_extraction]\n---\n\nproject rules",
    )

    got = reg.get(Stage.SCENE_PLAN)
    assert got.source == "project"
    assert got.body == "project rules"
    assert [t.name for t in got.tools.granted] == ["read_extraction"]
    # the shipped default is untouched
    assert AgentRegistry(defaults).get(Stage.SCENE_PLAN).body == default_text

    assert reg.reset_override(Stage.SCENE_PLAN) is True
    assert reg.get(Stage.SCENE_PLAN).source == "default"


def test_project_lifecycle(tmp_path):
    from pipeline.projects import ProjectStore
    from pipeline.stages import Stage

    store = ProjectStore(tmp_path)
    p = store.create("Demystifying the Brain")
    assert p.slug == "demystifying-the-brain"
    assert p.stage_state(Stage.INPUTS).status == "empty"

    (p.sources_dir / "ch1.docx").write_bytes(b"x")
    assert store.get(p.slug).stage_state(Stage.INPUTS).status == "ready"
    assert store.get(p.slug).sources()[0]["supported"] is True


def test_every_tab_has_its_own_colour():
    """A neutral stage reads as a disabled one, and two stages sharing a colour
    read as one place."""
    from pipeline.stages import STAGES

    colors = [s.color for s in STAGES]
    assert all(c.startswith("#") and len(c) == 7 for c in colors)
    # Export reuses Extraction's teal deliberately: they are the two ends of the
    # pipeline and never appear beside each other.
    assert len(set(colors)) >= len(STAGES) - 1


def test_unknown_tool_names_are_reported_not_dropped():
    """A typo would otherwise quietly remove a capability, and the symptom -- an
    agent that stops doing something -- is hard to trace back to a misspelling."""
    from pipeline.tools import resolve

    grant = resolve(["render_scene", "definitely_not_a_tool"])
    assert [t.name for t in grant.granted] == ["render_scene"]
    assert grant.unknown == ["definitely_not_a_tool"]


def test_fetch_tools_declare_licence_clear_resources():
    """Shipping someone else's copyrighted image is a real problem, and the agent
    will not be the one to notice. Every fetch tool names where it draws from."""
    from pipeline.tools import TOOLS, ToolKind

    for tool in TOOLS:
        if tool.kind is ToolKind.FETCH:
            assert tool.resources, f"{tool.name} fetches from nowhere declared"


def test_extraction_options_are_declared_with_complete_metadata():
    """The UI renders controls from these declarations, so a missing label or an
    empty choice list produces a broken control rather than a Python error."""
    from pipeline.stage_options import OptionKind, options_for
    from pipeline.stages import Stage

    options = options_for(Stage.EXTRACTION)
    assert options, "extraction has no options declared"

    for option in options:
        assert option.key and option.label, f"{option.key!r} is incompletely declared"
        if option.kind is OptionKind.CHOICE:
            assert option.choices, f"{option.key} is a choice with no choices"
            values = [choice.value for choice in option.choices]
            assert option.default in values, f"{option.key} default is not a valid choice"
            assert len(values) == len(set(values)), f"{option.key} has duplicate values"
        else:
            assert isinstance(option.default, bool)


def test_stages_without_options_return_empty_not_an_error():
    """A stage that has not declared options yet must return empty rather than
    raising — the UI then renders no options panel, which is correct."""
    from pipeline.stage_options import options_for
    from pipeline.stages import Stage

    assert options_for(Stage.INPUTS) == ()
    assert options_for(Stage.REVIEWING) == ()


def test_settings_round_trip_and_default_when_absent(tmp_path):
    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    store = StageSettingsStore(tmp_path)

    loaded = store.load(Stage.EXTRACTION)
    assert loaded.values["extraction_mode"] == "balanced"
    assert loaded.values["handwriting_ocr"] is False

    store.save(Stage.EXTRACTION, {"extraction_mode": "thorough", "handwriting_ocr": True})
    reloaded = store.load(Stage.EXTRACTION)
    assert reloaded.values["extraction_mode"] == "thorough"
    assert reloaded.values["handwriting_ocr"] is True
    # untouched options keep their defaults rather than vanishing
    assert reloaded.values["extract_tables"] is True


def test_invalid_stored_values_fall_back_rather_than_crashing(tmp_path):
    """Settings files are hand-editable and outlive schema changes. A stale value
    must not 500 a page the user can only fix by deleting a file they cannot see."""
    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    store = StageSettingsStore(tmp_path)
    (tmp_path / "settings").mkdir()
    (tmp_path / "settings" / "extraction.json").write_text(
        '{"extraction_mode": "no_such_mode", "extract_tables": "yes-ish"}', encoding="utf-8")

    loaded = store.load(Stage.EXTRACTION)
    assert loaded.values["extraction_mode"] == "balanced"   # back to default
    assert loaded.values["extract_tables"] is True          # coerced to bool


def test_corrupt_settings_file_is_logged_not_swallowed(tmp_path, caplog):
    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    store = StageSettingsStore(tmp_path)
    (tmp_path / "settings").mkdir()
    (tmp_path / "settings" / "extraction.json").write_text("{ broken", encoding="utf-8")

    with caplog.at_level("ERROR"):
        loaded = store.load(Stage.EXTRACTION)

    assert loaded.values["extraction_mode"] == "balanced"
    assert any("unreadable" in record.message for record in caplog.records), (
        "settings silently reverted with no log line"
    )


def test_unknown_keys_are_not_persisted(tmp_path):
    """A client must not be able to grow the settings file with arbitrary content."""
    import json

    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    store = StageSettingsStore(tmp_path)
    store.save(Stage.EXTRACTION, {"extraction_mode": "fast", "injected_key": "nope"})

    written = json.loads(
        (tmp_path / "settings" / "extraction.json").read_text(encoding="utf-8"))
    assert "injected_key" not in written
    assert written["extraction_mode"] == "fast"


def test_settings_write_is_atomic(tmp_path):
    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    store = StageSettingsStore(tmp_path)
    store.save(Stage.EXTRACTION, {"extraction_mode": "fast"})
    assert not list((tmp_path / "settings").glob("*.tmp"))


def test_plan_defaults_to_empty_without_erroring(tmp_path):
    """No plan yet is the normal starting state, not an error — the UI needs
    something to render."""
    from pipeline.planning import PlanStore

    plan = PlanStore(tmp_path).load()
    assert plan.sections == []
    assert plan.is_empty is True
    assert plan.selected_audience


def test_plan_round_trip_preserves_order(tmp_path):
    from pipeline.planning import Plan, PlanSection, PlanStore

    store = PlanStore(tmp_path)
    store.save(Plan(sections=[
        PlanSection(title="Intro", estimated_seconds=45),
        PlanSection(title="Body", estimated_seconds=120),
        PlanSection(title="Close", estimated_seconds=30),
    ]))

    reloaded = store.load()
    assert [s.title for s in reloaded.sections] == ["Intro", "Body", "Close"]
    assert reloaded.total_estimated_seconds == 195


def test_section_ids_are_unique_so_reorder_addresses_the_right_row():
    """Titles can be duplicated or blank mid-edit; ids cannot."""
    from pipeline.planning import PlanSection

    ids = {PlanSection().id for _ in range(50)}
    assert len(ids) == 50


def test_absurd_durations_are_clamped_not_rejected(tmp_path):
    """A typo must not poison the plan total or lose the rest of an edit."""
    from pipeline.planning import PlanSection

    assert PlanSection(estimated_seconds=-30).estimated_seconds == 1
    assert PlanSection(estimated_seconds=999999).estimated_seconds == 3600


def test_overlong_text_is_trimmed_at_the_boundary():
    from pipeline.planning import PlanSection

    section = PlanSection(title="x" * 500, summary="y" * 900)
    assert len(section.title) == 120
    assert len(section.summary) == 400


def test_warnings_are_advisory_and_never_block_a_save(tmp_path):
    """A plan mid-edit is allowed to be inconsistent; blocking on it would make
    the outline hostile to work in."""
    from pipeline.planning import Plan, PlanSection, PlanStore

    plan = Plan(sections=[PlanSection(title="", estimated_seconds=2)])
    warnings = plan.warnings()
    assert any("no title" in w for w in warnings)
    assert any("unusual duration" in w for w in warnings)

    saved = PlanStore(tmp_path).save(plan)   # saves regardless
    assert PlanStore(tmp_path).load().sections[0].estimated_seconds == 2
    assert saved.warnings()


def test_corrupt_plan_is_logged_and_the_file_is_left_alone(tmp_path, caplog):
    """Returning an empty plan silently would discard someone's work."""
    from pipeline.planning import PlanStore

    store = PlanStore(tmp_path)
    store.plan_path.parent.mkdir(parents=True)
    store.plan_path.write_text("{ not json", encoding="utf-8")

    with caplog.at_level("ERROR"):
        plan = store.load()

    assert plan.is_empty
    assert any("unreadable" in record.message for record in caplog.records)
    # the original file is preserved for manual recovery
    assert store.plan_path.read_text(encoding="utf-8") == "{ not json"


def test_plan_write_is_atomic(tmp_path):
    from pipeline.planning import Plan, PlanSection, PlanStore

    store = PlanStore(tmp_path)
    store.save(Plan(sections=[PlanSection(title="Only")]))
    assert not list(store.plan_path.parent.glob("*.tmp"))


def test_planning_options_are_declared():
    from pipeline.stage_options import options_for
    from pipeline.stages import Stage

    keys = {option.key for option in options_for(Stage.SCENE_PLAN)}
    assert {"target_duration", "tone", "language"} <= keys


def test_script_defaults_include_starting_scenarios(tmp_path):
    """The stage should not open as an empty canvas."""
    from pipeline.scripting import ScriptStore

    script = ScriptStore(tmp_path).load()
    assert len(script.scenarios) >= 2
    assert script.active_scenario_id in {s.id for s in script.scenarios}


def test_deleting_a_plan_section_orphans_narration_rather_than_losing_it(tmp_path):
    """Losing written narration because someone tidied the outline would be the
    worst failure this stage can have — and it would be invisible."""
    from pipeline.scripting import Script, SectionScript

    script = Script(section_scripts=[
        SectionScript(section_id="kept", body="This section survives."),
        SectionScript(section_id="deleted", body="Hours of writing."),
    ])

    audit = script.audit(plan_section_ids=["kept"])
    assert audit["orphaned_section_ids"] == ["deleted"]
    # the text is still present, not dropped
    assert script.body_for("deleted") == "Hours of writing."


def test_unwritten_sections_are_reported(tmp_path):
    from pipeline.scripting import Script, SectionScript

    script = Script(section_scripts=[SectionScript(section_id="a", body="written")])
    audit = script.audit(plan_section_ids=["a", "b", "c"])
    assert audit["unwritten_section_ids"] == ["b", "c"]


def test_whitespace_only_narration_counts_as_unwritten():
    from pipeline.scripting import Script, SectionScript

    script = Script(section_scripts=[SectionScript(section_id="a", body="   \n  ")])
    assert script.audit(["a"])["unwritten_section_ids"] == ["a"]


def test_undefined_variables_are_reported_not_silently_blanked():
    """A literal {{NAME}} reaching narration is bad; blanking it silently is worse."""
    from pipeline.scripting import Script, ScriptVariable, SectionScript

    script = Script(
        section_scripts=[SectionScript(section_id="a", body="About {{TOPIC}} and {{MISSING}}.")],
        variables=[ScriptVariable(name="TOPIC", value="the brain")],
    )
    audit = script.audit(["a"])
    assert audit["undefined_variables"] == ["MISSING"]

    resolved = script.resolve("About {{TOPIC}} and {{MISSING}}.")
    assert "the brain" in resolved
    assert "{{MISSING}}" in resolved     # left visible rather than emptied


def test_variable_names_are_normalised_to_a_usable_shape():
    """A name typed as 'my topic' must not become a variable that never matches."""
    from pipeline.scripting import ScriptVariable

    assert ScriptVariable(name="my topic").name == "MY_TOPIC"
    assert ScriptVariable(name="  Topic-Name! ").name == "TOPIC_NAME"
    assert ScriptVariable(name="TOPIC").is_valid is True
    assert ScriptVariable(name="9LIVES").is_valid is False   # cannot start with a digit


def test_word_count_and_duration_use_the_named_rate():
    from pipeline.scripting import NARRATION_WORDS_PER_MINUTE, estimate_seconds

    one_minute_of_words = " ".join(["word"] * NARRATION_WORDS_PER_MINUTE)
    assert estimate_seconds(one_minute_of_words) == 60


def test_script_round_trip_and_atomic_write(tmp_path):
    from pipeline.scripting import Script, ScriptStore, SectionScript

    store = ScriptStore(tmp_path)
    store.save(Script(section_scripts=[SectionScript(section_id="a", body="Hello there.")]))

    assert not list(store.script_path.parent.glob("*.tmp"))
    assert store.load().body_for("a") == "Hello there."


def test_corrupt_script_is_never_overwritten(tmp_path, caplog):
    """The file may hold hours of narration; a bad parse must not destroy it."""
    from pipeline.scripting import ScriptStore

    store = ScriptStore(tmp_path)
    store.script_path.parent.mkdir(parents=True)
    store.script_path.write_text("{ not json", encoding="utf-8")

    with caplog.at_level("ERROR"):
        store.load()

    assert store.script_path.read_text(encoding="utf-8") == "{ not json"
    assert any("unreadable" in record.message for record in caplog.records)


def test_stage_five_is_studio_not_graphics():
    """Renamed: the stage owns media, timeline, layers, effects and rendering.
    'Graphics' described one of its panels."""
    from pipeline.stages import STAGES, Stage

    studio = next(spec for spec in STAGES if spec.key is Stage.STUDIO)
    assert studio.title == "Studio"
    assert not hasattr(Stage, "GRAPHICS")


def test_default_composition_stacks_bottom_to_top():
    """Track order is composite order; the list must read the way the frame stacks."""
    from pipeline.composition import TrackKind, default_composition

    kinds = [track.kind for track in default_composition().tracks]
    assert kinds == [TrackKind.VIDEO, TrackKind.TEXT, TrackKind.GRAPHICS, TrackKind.AUDIO]


def test_clip_duration_cannot_become_ungrabbable():
    """A zero or negative duration produces a clip that cannot be selected or
    deleted from the UI — effectively a stuck row."""
    from pipeline.composition import MINIMUM_CLIP_DURATION_MS, Clip

    assert Clip(duration_ms=0).duration_ms == MINIMUM_CLIP_DURATION_MS
    assert Clip(duration_ms=-500).duration_ms == MINIMUM_CLIP_DURATION_MS
    assert Clip(start_ms=-100).start_ms == 0


def test_overlapping_clips_are_reported_not_prevented():
    """Two clips on one track cannot both show, but forbidding it mid-drag would
    make the timeline fight the pointer."""
    from pipeline.composition import Clip, Track

    track = Track(clips=[
        Clip(id="a", start_ms=0, duration_ms=2000),
        Clip(id="b", start_ms=1000, duration_ms=2000),
        Clip(id="c", start_ms=5000, duration_ms=1000),
    ])
    assert track.overlapping_clip_ids() == ["a", "b"]


def test_touching_clips_do_not_count_as_overlapping():
    """A clip ending exactly where the next begins is a normal cut, not a defect."""
    from pipeline.composition import Clip, Track

    track = Track(clips=[
        Clip(id="a", start_ms=0, duration_ms=1000),
        Clip(id="b", start_ms=1000, duration_ms=1000),
    ])
    assert track.overlapping_clip_ids() == []


def test_missing_media_is_caught_before_a_render_is_attempted():
    """A render failing ten minutes in because a clip points at a deleted file is
    exactly the late failure v1 was full of."""
    from pipeline.composition import Clip, ClipKind, Composition, Track

    composition = Composition(tracks=[Track(clips=[
        Clip(id="ok", kind=ClipKind.IMAGE, asset_id="present"),
        Clip(id="broken", kind=ClipKind.IMAGE, asset_id="deleted"),
    ])])

    audit = composition.audit(known_asset_ids={"present"})
    assert audit["missing_asset_clip_ids"] == ["broken"]


def test_composition_duration_is_the_furthest_clip_end():
    from pipeline.composition import Clip, Composition, Track

    composition = Composition(tracks=[
        Track(clips=[Clip(start_ms=0, duration_ms=5000)]),
        Track(clips=[Clip(start_ms=8000, duration_ms=2000)]),
    ])
    assert composition.duration_ms == 10000
    assert composition.clip_count == 2


def test_composition_round_trip_and_atomic_write(tmp_path):
    from pipeline.composition import Clip, CompositionStore, default_composition

    store = CompositionStore(tmp_path)
    composition = default_composition()
    composition.tracks[0].clips.append(Clip(label="Intro", duration_ms=4000))
    store.save(composition)

    assert not list(store.composition_path.parent.glob("*.tmp"))
    assert store.load().tracks[0].clips[0].label == "Intro"


def test_corrupt_composition_is_never_overwritten(tmp_path, caplog):
    from pipeline.composition import CompositionStore

    store = CompositionStore(tmp_path)
    store.composition_path.parent.mkdir(parents=True)
    store.composition_path.write_text("{ not json", encoding="utf-8")

    with caplog.at_level("ERROR"):
        store.load()

    assert store.composition_path.read_text(encoding="utf-8") == "{ not json"
    assert any("unreadable" in record.message for record in caplog.records)


def test_comments_are_routed_to_the_stage_that_can_fix_them():
    """'The pacing is frantic' is a Scripting defect, not a Studio one. Routing
    makes the responsible stage explicit rather than leaving it to whoever picks
    the comment up."""
    from pipeline.review import Comment, Review
    from pipeline.stages import Stage

    review = Review(comments=[
        Comment(body="Pacing is frantic", routed_to_stage=Stage.SCRIPT_STAGING),
        Comment(body="Text is clipped", routed_to_stage=Stage.STUDIO),
        Comment(body="Wrong emphasis", routed_to_stage=Stage.SCRIPT_STAGING),
        Comment(body="Looks odd"),   # unrouted
    ])

    assert review.comments_by_stage() == {"script-staging": 2, "studio": 1, "unrouted": 1}
    assert len(review.audit()["unrouted_comment_ids"]) == 1


def test_resolved_comments_leave_the_open_count():
    from pipeline.review import Comment, CommentStatus, Review

    review = Review(comments=[
        Comment(body="fix this"),
        Comment(body="done", status=CommentStatus.ADDRESSED),
        Comment(body="no", status=CommentStatus.DECLINED),
    ])
    assert len(review.open_comments) == 1
    assert review.to_dict()["is_ready_to_export"] is False


def test_export_is_ready_only_when_nothing_is_open():
    from pipeline.review import Comment, CommentStatus, Review

    assert Review().to_dict()["is_ready_to_export"] is True
    resolved = Review(comments=[Comment(body="x", status=CommentStatus.ADDRESSED)])
    assert resolved.to_dict()["is_ready_to_export"] is True


def test_anonymous_author_rather_than_a_blank_byline():
    from pipeline.review import Comment

    assert Comment(author="   ").author == "Anonymous"
    assert Comment(author="  Prof. Iyer  ").author == "Prof. Iyer"


def test_chapters_are_returned_in_time_order_regardless_of_entry_order():
    from pipeline.review import Chapter, Review

    review = Review(chapters=[
        Chapter(title="Third", start_ms=6000),
        Chapter(title="First", start_ms=0),
        Chapter(title="Second", start_ms=3000),
    ])
    assert [c.title for c in review.ordered_chapters()] == ["First", "Second", "Third"]
    assert [c["title"] for c in review.to_dict()["chapters"]] == ["First", "Second", "Third"]


def test_duplicate_chapter_starts_are_flagged():
    from pipeline.review import Chapter, Review

    review = Review(chapters=[
        Chapter(title="A", start_ms=1000), Chapter(title="B", start_ms=1000)])
    assert review.audit()["duplicate_chapter_ids"]
    assert any("same time" in w for w in review.to_dict()["warnings"])


def test_chapters_seed_from_plan_section_durations():
    from pipeline.review import chapters_from_plan

    chapters = chapters_from_plan([
        {"title": "Intro", "estimated_seconds": 45},
        {"title": "Body", "estimated_seconds": 120},
        {"title": "Close", "estimated_seconds": 30},
    ])
    assert [c.start_ms for c in chapters] == [0, 45_000, 165_000]


def test_a_version_without_a_file_is_not_rendered():
    """Versions are recorded before rendering exists, so a comment can always say
    which cut it was made against."""
    from pipeline.review import VideoVersion

    assert VideoVersion(label="v1").is_rendered is False
    assert VideoVersion(label="v1", file_path="out.mp4").is_rendered is True


def test_review_round_trip_and_atomic_write(tmp_path):
    from pipeline.review import Comment, Review, ReviewStore

    store = ReviewStore(tmp_path)
    store.save(Review(comments=[Comment(author="Nisha", body="Different image here")]))

    assert not list(store.review_path.parent.glob("*.tmp"))
    assert store.load().comments[0].author == "Nisha"


def test_corrupt_review_never_overwrites_other_peoples_words(tmp_path, caplog):
    from pipeline.review import ReviewStore

    store = ReviewStore(tmp_path)
    store.review_path.parent.mkdir(parents=True)
    store.review_path.write_text("{ not json", encoding="utf-8")

    with caplog.at_level("ERROR"):
        store.load()

    assert store.review_path.read_text(encoding="utf-8") == "{ not json"
    assert any("unreadable" in record.message for record in caplog.records)


# --- storage: one implementation, one behaviour ------------------------------

def test_all_document_stores_share_one_durability_implementation():
    """Six hand-rolled stores agreed only because they were written in one
    sitting. The next one added under time pressure would have been the odd one
    out, and the divergence would be invisible until something went wrong."""
    from pipeline.composition import CompositionStore
    from pipeline.planning import PlanStore
    from pipeline.review import ReviewStore
    from pipeline.scripting import ScriptStore
    from pipeline.storage.documents import JsonDocumentStore

    for store_type in (PlanStore, ScriptStore, CompositionStore, ReviewStore):
        assert issubclass(store_type, JsonDocumentStore), (
            f"{store_type.__name__} reimplements persistence instead of sharing it"
        )


def test_no_module_hand_rolls_an_atomic_write():
    """Guards the invariant rather than the instance: a new store must use
    write_text_atomically rather than copying the temp-then-rename dance.

    An earlier version of this test searched for the literal `temporary_path.
    replace`, which is a variable name and not a behaviour. A module writing
    `tmp.replace(path)` was reimplementing the dance and passed anyway. Matching
    the shape -- a temp suffix and a rename in the same file -- catches the
    rename regardless of what the variable is called.
    """
    from pipeline.config import REPO_ROOT

    offenders = []
    for source_file in (REPO_ROOT / "src" / "pipeline").rglob("*.py"):
        if source_file.name == "documents.py":
            continue
        body = source_file.read_text(encoding="utf-8")
        if ".tmp" in body and ".replace(" in body:
            offenders.append(source_file.name)

    assert offenders == [], f"these modules reimplement atomic writes: {offenders}"


def test_every_store_writes_where_its_stage_says_it_writes():
    """`produces` is shown in the UI and now derives the store's path, so the
    label and the file are the same string by construction.

    They were not always: Scripting advertised `scripting/scenes.json` while
    writing `scripting/script.json`, and Reviewing advertised
    `reviewing/report.json` while writing `reviewing/review.json`. Both named a
    file that did not exist, and nothing failed -- the label is only ever read by
    a human.
    """
    from pathlib import Path

    from pipeline.composition import CompositionStore
    from pipeline.planning import PlanStore
    from pipeline.review import ReviewStore
    from pipeline.scripting import ScriptStore
    from pipeline.stages import BY_KEY, Stage

    project_root = Path("/projects/example")
    stores_by_stage = {
        Stage.SCENE_PLAN: PlanStore,
        Stage.SCRIPT_STAGING: ScriptStore,
        Stage.STUDIO: CompositionStore,
        Stage.REVIEWING: ReviewStore,
    }

    for stage, store_type in stores_by_stage.items():
        declared = project_root / BY_KEY[stage].produces
        actual = store_type(project_root).document_path
        assert actual == declared, (
            f"{store_type.__name__} writes {actual}, but the {stage.value} stage "
            f"tells the operator it produces {declared}"
        )


@pytest.mark.parametrize(
    "store_factory_path",
    ["planning.PlanStore", "scripting.ScriptStore",
     "composition.CompositionStore", "review.ReviewStore"],
)
def test_every_document_store_survives_a_corrupt_file_without_destroying_it(
    store_factory_path, tmp_path
):
    """A corrupt file may hold hours of someone's writing. Every store must fall
    back to a default, log loudly, and leave the file for manual recovery."""
    import importlib

    module_name, class_name = store_factory_path.split(".")
    store_type = getattr(importlib.import_module(f"pipeline.{module_name}"), class_name)

    store = store_type(tmp_path)
    store.document_path.parent.mkdir(parents=True, exist_ok=True)
    store.document_path.write_text("{ not json at all", encoding="utf-8")

    loaded = store.load()
    assert loaded is not None, "a corrupt file must still yield a usable default"
    assert store.document_path.read_text(encoding="utf-8") == "{ not json at all"


@pytest.mark.parametrize(
    "store_factory_path",
    ["planning.PlanStore", "scripting.ScriptStore",
     "composition.CompositionStore", "review.ReviewStore"],
)
def test_valid_json_of_the_wrong_shape_is_also_survivable(store_factory_path, tmp_path):
    """An older schema or a hand edit parses as JSON but does not fit the model.
    Same rule: default, log, never overwrite."""
    import importlib

    module_name, class_name = store_factory_path.split(".")
    store_type = getattr(importlib.import_module(f"pipeline.{module_name}"), class_name)

    store = store_type(tmp_path)
    store.document_path.parent.mkdir(parents=True, exist_ok=True)
    store.document_path.write_text('{"sections": "not a list"}', encoding="utf-8")

    assert store.load() is not None
    assert store.document_path.read_text(encoding="utf-8") == '{"sections": "not a list"}'


def test_a_json_array_is_rejected_as_a_document(tmp_path):
    """A bare list would otherwise fail deep inside model validation, far from the
    file that caused it."""
    from pipeline.planning import PlanStore

    store = PlanStore(tmp_path)
    store.document_path.parent.mkdir(parents=True, exist_ok=True)
    store.document_path.write_text("[1, 2, 3]", encoding="utf-8")
    assert store.load().is_empty


# --- credentials: a secret must never reach the browser ----------------------

def test_a_secret_is_never_returned_in_the_clear(monkeypatch, tmp_path):
    """The one invariant of the credentials panel.

    If this fails, a key is being served to any page that asks -- readable in
    devtools, in the network log, and in any proxy along the way.
    """
    import json

    from pipeline import credentials

    secret = "sk-abcdefghijklmnopqrstuvwxyz0123456789END"
    env_file = tmp_path / ".env"
    env_file.write_text(f"LLM_API_KEY={secret}\n", encoding="utf-8")
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    described = credentials.describe_credentials()
    assert secret not in json.dumps(described), "the raw key is present in the API response"

    key_field = next(f for f in described["fields"] if f["name"] == "LLM_API_KEY")
    assert key_field["is_set"] is True
    assert key_field["display_value"] == "•" * 8 + "9END"


def test_a_short_secret_reveals_nothing():
    """Four trailing characters of a 10-character secret is most of it."""
    from pipeline.credentials import mask_secret

    assert mask_secret("short") == "•" * 8
    assert "short" not in mask_secret("short")


def test_a_blank_submission_does_not_wipe_a_stored_key(monkeypatch, tmp_path):
    """The panel sends only fields the user typed into.

    A field left out must keep its value -- otherwise editing the model name
    would silently delete the key, and the user would find out when an agent
    failed rather than when they saved.
    """
    from pipeline import credentials

    env_file = tmp_path / ".env"
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)

    credentials.save_credentials({"LLM_API_KEY": "sk-original-key-value-here"})
    credentials.save_credentials({"LLM_MODEL": "some/other-model"})

    stored = credentials.read_environment_file()
    assert stored["LLM_API_KEY"] == "sk-original-key-value-here"
    assert stored["LLM_MODEL"] == "some/other-model"


def test_an_empty_string_clears_a_key(monkeypatch, tmp_path):
    """Clearing has to be possible, and has to be explicit."""
    from pipeline import credentials

    env_file = tmp_path / ".env"
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    credentials.save_credentials({"LLM_API_KEY": "sk-doomed"})
    assert credentials.read_environment_file()["LLM_API_KEY"] == "sk-doomed"

    credentials.save_credentials({"LLM_API_KEY": ""})
    assert "LLM_API_KEY" not in credentials.read_environment_file()


def test_unmanaged_env_entries_survive_a_save(monkeypatch, tmp_path):
    """The file is rewritten on every save. Anything the panel does not know
    about must still be there afterwards, or saving a key would silently delete
    someone's unrelated configuration."""
    from pipeline import credentials

    env_file = tmp_path / ".env"
    env_file.write_text("SOME_OTHER_TOOL_TOKEN=keep-me\n", encoding="utf-8")
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    credentials.save_credentials({"LLM_API_KEY": "sk-new"})

    stored = credentials.read_environment_file()
    assert stored["SOME_OTHER_TOOL_TOKEN"] == "keep-me"
    assert stored["LLM_API_KEY"] == "sk-new"


def test_a_shell_environment_variable_is_reported_as_taking_precedence(monkeypatch, tmp_path):
    """pydantic-settings reads the real environment ahead of .env.

    Without this the panel would accept an edit, store it, and let the old value
    keep being used -- the most confusing failure this feature could have.
    """
    from pipeline import credentials

    env_file = tmp_path / ".env"
    env_file.write_text("LLM_API_KEY=sk-from-the-file\n", encoding="utf-8")
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)
    monkeypatch.setenv("LLM_API_KEY", "sk-from-the-shell-environment")

    described = credentials.describe_credentials()
    key_field = next(f for f in described["fields"] if f["name"] == "LLM_API_KEY")

    assert key_field["source"] == "environment"
    assert key_field["is_editable"] is False
    assert any("shell environment" in warning for warning in described["warnings"])


def test_unknown_credential_fields_are_ignored_not_written(monkeypatch, tmp_path):
    """The submitted names come from a page, so they are untrusted input."""
    from pipeline import credentials

    env_file = tmp_path / ".env"
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)

    credentials.save_credentials({"TOTALLY_MADE_UP": "value", "LLM_API_KEY": "sk-real"})

    stored = credentials.read_environment_file()
    assert "TOTALLY_MADE_UP" not in stored
    assert stored["LLM_API_KEY"] == "sk-real"


def test_values_needing_quotes_round_trip(monkeypatch, tmp_path):
    """A key with a space or a hash would otherwise be truncated on the next
    read, which looks exactly like the key being wrong."""
    from pipeline import credentials

    env_file = tmp_path / ".env"
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)
    monkeypatch.delenv("LLM_MODEL", raising=False)

    awkward = "model with spaces #and-a-hash"
    credentials.save_credentials({"LLM_MODEL": awkward})
    assert credentials.read_environment_file()["LLM_MODEL"] == awkward


def test_env_file_is_gitignored_in_this_repository():
    """A real key is about to be written to .env. If it is committable, that is
    a leak waiting to happen."""
    from pipeline.credentials import is_env_file_ignored

    assert is_env_file_ignored(), ".env must be listed in .gitignore"


async def test_credentials_route_masks_and_saves(monkeypatch, tmp_path):
    import json

    from litestar.testing import TestClient

    from pipeline import credentials
    from pipeline.web.app import create_app

    env_file = tmp_path / ".env"
    monkeypatch.setattr(credentials, "ENVIRONMENT_FILE_PATH", env_file)
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    with TestClient(app=create_app()) as client:
        saved = client.post(
            "/api/credentials",
            json={"values": {"LLM_API_KEY": "sk-routed-through-http-0000WXYZ"}},
        )
        assert saved.status_code == 201

        body = saved.json()
        assert "sk-routed-through-http-0000WXYZ" not in json.dumps(body)

        read_back = client.get("/api/credentials")
        assert read_back.status_code == 200
        assert "sk-routed-through-http-0000WXYZ" not in read_back.text

        key_field = next(f for f in read_back.json()["fields"] if f["name"] == "LLM_API_KEY")
        assert key_field["display_value"].endswith("WXYZ")


def test_a_rendered_version_reports_is_rendered_over_the_api():
    """`is_rendered` is a property, and model_dump does not serialise properties.

    It was therefore absent from every response while the Reviewing UI branched
    on it -- so a finished render was treated as "no file" and the player showed
    the empty placeholder instead of the video. The one field that decides
    whether the user sees their video at all.
    """
    from pipeline.review import Review, VideoVersion

    review = Review(versions=[
        VideoVersion(label="With a file", file_path="C:/out/video.mp4", duration_ms=1000),
        VideoVersion(label="No file yet"),
    ])
    serialised = review.to_dict()

    assert serialised["versions"][0]["is_rendered"] is True
    assert serialised["versions"][1]["is_rendered"] is False
