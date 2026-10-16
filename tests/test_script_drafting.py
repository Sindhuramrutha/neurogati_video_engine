"""Scripting: scenes, the text that is actually spoken, drafting from the plan and
source, and knowing when narration no longer matches what it was written from.

The model is stood in for. What is checked is what the agent is shown, what is
kept, and what every later stage reads.
"""

import pytest

from pipeline import operations, script_drafting, script_review
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    Extraction,
    ExtractionStore,
)
from pipeline.operations import OperationFailed
from pipeline.planning import (
    Plan,
    PlanSection,
    PlanStore,
    SourceReference,
)
from pipeline.rendering import _slides_with_scenes
from pipeline.script_drafting import DraftedScene, DraftedSection
from pipeline.scripting import Script, ScriptScene, ScriptStore, ScriptVariable, SectionScript


def _slides_for_narration(narration: str) -> list[str]:
    return [text for text, _scene in _slides_with_scenes(narration)]


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def document(file_name, parts):
    blocks = []
    for heading, text in parts:
        blocks.append(ContentBlock(kind=BlockKind.HEADING, level=1, text=heading,
                                   heading_path=[heading]))
        blocks.append(ContentBlock(kind=BlockKind.PARAGRAPH, text=text, heading_path=[heading]))
    return ExtractedDocument(file_name=file_name, blocks=blocks)


CHAPTER = document("chapter.docx", [
    ("Signals", "Neurons produce tiny signals of about 50 microvolts."),
    ("Electrodes", "Electrodes detect potentials that are already present."),
    ("Amplifiers", "Amplifiers raise the signal a thousandfold before digitising."),
])


def reference(heading):
    return SourceReference(file_name="chapter.docx", heading_path=[heading])


def planned_project(name, *, extraction=CHAPTER):
    """Three sections, each built on one part of the chapter."""
    slug = operations.create_project(name)["slug"]
    project = operations.require_project(slug)
    (project.sources_dir / "chapter.docx").write_text("source", encoding="utf-8")
    ExtractionStore(project.root).save(Extraction(documents=[extraction]))
    PlanStore(project.root).save(Plan(
        audience="Students new to the topic",
        sections=[
            PlanSection(id="s1", title="Signals", summary="How small the signal is.",
                        estimated_seconds=40, sources=[reference("Signals")]),
            PlanSection(id="s2", title="Electrodes", summary="What an electrode detects.",
                        estimated_seconds=40, sources=[reference("Electrodes")]),
            PlanSection(id="s3", title="Amplifiers", summary="Why amplification comes first.",
                        estimated_seconds=40, sources=[reference("Amplifiers")]),
        ],
    ))
    return slug, project


class FakeScriptModel:
    """Two scenes per section, built from the prompt it is shown. Records prompts."""

    def __init__(self, fail_for=(), during_call=None):
        self.prompts = {}
        self.systems = {}
        self.fail_for = set(fail_for)
        self.during_call = during_call

    def __call__(self, response_model, system_prompt, user_prompt, **kwargs):
        assert response_model is DraftedSection
        title = user_prompt.split("--- the section you are writing ---\nTitle: ")[1].split("\n")[0]
        self.prompts[title] = user_prompt
        self.systems[title] = system_prompt
        if self.during_call:
            self.during_call(title)
        if title in self.fail_for:
            from pipeline.llm import ModelCallFailed
            raise ModelCallFailed("provider timed out")
        return DraftedSection(scenes=[
            DraftedScene(narration=f"{title} opens here.", brief=f"Title card: {title}"),
            DraftedScene(narration=f"{title} continues.", brief="The 50 microvolt trace"),
        ])


# --- scenes are the narration -----------------------------------------------------


def test_narration_saved_before_scenes_becomes_one_scene():
    section = SectionScript(section_id="s1", body="Old narration, word for word.")

    assert len(section.scenes) == 1
    assert section.scenes[0].narration == "Old narration, word for word."
    assert section.body == "Old narration, word for word."


def test_the_body_is_always_rebuilt_from_the_scenes():
    section = SectionScript(section_id="s1", body="stale", scenes=[
        ScriptScene(narration="First.", brief="a"), ScriptScene(narration="Second.", brief="b"),
    ])

    assert section.body == "First.\n\nSecond."


def test_writing_narration_through_the_old_command_is_not_lost(project_root):
    """`script write` set `body` alone; the scenes, still holding the old text,
    would have put it back on the next load."""
    slug, project = planned_project("Old Command")
    operations.write_section_script(slug, "s1", "First version.")
    operations.write_section_script(slug, "s1", "Second version.")

    assert ScriptStore(project.root).load().body_for("s1") == "Second version."


def test_a_slide_never_runs_across_two_scenes():
    slides = _slides_for_narration("One short scene.\n\nAnother short scene.")

    assert slides == ["One short scene.", "Another short scene."]


# --- the text that is spoken --------------------------------------------------------


def test_variables_are_filled_in_in_the_video(project_root):
    """The review transcript read "Neuroscience 101" while the video's subtitles
    and timeline said "{{COURSE}}" -- and the voice would have read the braces."""
    slug, project = planned_project("Variables")
    ScriptStore(project.root).save(Script(
        section_scripts=[SectionScript(section_id="s1", body="Welcome to {{COURSE}}.")],
        variables=[ScriptVariable(name="COURSE", value="Neuroscience 101")],
    ))

    operations.render_video(slug, voice_provider="silent")
    output = project.root / "reviewing" / "output"
    subtitles = next(output.glob("*.vtt")).read_text(encoding="utf-8")
    timeline_text = [c["text"] for t in operations.read_artifact(slug, "composition")["tracks"]
                     for c in t["clips"] if "Welcome" in (c.get("text") or "")]
    transcript = operations.read_artifact(slug, "review")["transcript"][0]["body"]

    assert "Welcome to Neuroscience 101." in subtitles
    assert "{{" not in subtitles
    assert timeline_text == ["Welcome to Neuroscience 101."]
    assert transcript == "Welcome to Neuroscience 101."


def test_a_render_warns_about_a_variable_that_is_not_defined(project_root):
    slug, project = planned_project("Undefined")
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id="s1", body="Welcome to {{COURSE}}."),
    ]))

    result = operations.render_video(slug, voice_provider="silent")

    assert any("{{COURSE}} is not defined" in warning for warning in result["warnings"])


# --- drafting a section ------------------------------------------------------------------


def test_a_drafted_section_is_saved_as_scenes_with_briefs(project_root, monkeypatch):
    slug, project = planned_project("Draft One")
    monkeypatch.setattr(script_drafting, "complete_structured", FakeScriptModel())

    result = script_drafting.draft_section(slug, "s2")

    saved = next(s for s in ScriptStore(project.root).load().section_scripts
                 if s.section_id == "s2")
    assert [scene.brief for scene in saved.scenes] == [
        "Title card: Electrodes", "The 50 microvolt trace"]
    assert saved.body == "Electrodes opens here.\n\nElectrodes continues."
    assert result["scene_count"] == 2 and result["is_saved"] is True


def test_the_agent_is_shown_its_section_its_neighbours_and_its_own_source(
    project_root, monkeypatch
):
    slug, project = planned_project("Context")
    operations.write_section_script(slug, "s1", "Signals are tiny, about 50 microvolts.")
    fake = FakeScriptModel()
    monkeypatch.setattr(script_drafting, "complete_structured", fake)

    script_drafting.draft_section(slug, "s2")
    prompt = fake.prompts["Electrodes"]

    # The whole plan, compactly, with this section marked.
    assert "2. Electrodes (~40 s)  <- this section" in prompt
    assert "3. Amplifiers" in prompt
    assert "source_outline" not in prompt and "freshness" not in prompt
    # Its own plan details.
    assert "Target: about 40 seconds, about 100 words" in prompt
    # The narration before it, and what comes after.
    assert "Signals are tiny, about 50 microvolts." in prompt
    assert 'the section after: "Amplifiers"' in prompt
    assert "Why amplification comes first." in prompt
    # Its own source -- and not the others'.
    assert "Electrodes detect potentials that are already present." in prompt
    assert "Amplifiers raise the signal a thousandfold" not in prompt.split(
        "--- source material for this section ---")[1]


def test_the_section_s_presentation_and_audience_reach_the_agent(project_root, monkeypatch):
    slug, _ = planned_project("Presentation")
    fake = FakeScriptModel()
    monkeypatch.setattr(script_drafting, "complete_structured", fake)

    script_drafting.draft_section(slug, "s1")
    prompt = fake.prompts["Signals"]

    assert "Audience: Students new to the topic" in prompt


def test_the_script_fills_exactly_the_planned_scenes(project_root, monkeypatch):
    """The plan owns the scenes: the script keeps their ids, so every later layer
    lines up with what was agreed."""
    from pipeline.planning import PlanScene

    slug, project = planned_project("Planned Scenes")
    plan = PlanStore(project.root).load()
    plan.sections[0].scenes = [PlanScene(id="p1", does="How small", seconds=20),
                               PlanScene(id="p2", does="Microvolts", seconds=20)]
    PlanStore(project.root).save(plan)
    fake = FakeScriptModel()
    monkeypatch.setattr(script_drafting, "complete_structured", fake)

    script_drafting.draft_section(slug, "s1")

    assert "exactly 2 scenes" in fake.systems["Signals"]
    assert "1. (~20 s) How small" in fake.prompts["Signals"]
    written = ScriptStore(project.root).load().section_scripts
    assert [scene.id for scene in written[0].scenes] == ["p1", "p2"]


def test_drafting_one_section_leaves_the_others_alone(project_root, monkeypatch):
    slug, project = planned_project("Leave Others")
    operations.write_section_script(slug, "s1", "Mine, by hand.")
    monkeypatch.setattr(script_drafting, "complete_structured", FakeScriptModel())

    script_drafting.draft_section(slug, "s2")

    assert ScriptStore(project.root).load().body_for("s1") == "Mine, by hand."


def test_what_is_saved_while_one_section_drafts_is_not_overwritten(project_root, monkeypatch):
    slug, project = planned_project("Saved Meanwhile")

    def someone_types(title):
        operations.write_section_script(slug, "s1", "Typed while the draft ran.")

    monkeypatch.setattr(script_drafting, "complete_structured",
                        FakeScriptModel(during_call=someone_types))
    script_drafting.draft_section(slug, "s2")

    script = ScriptStore(project.root).load()
    assert script.body_for("s1") == "Typed while the draft ran."
    assert script.body_for("s2").startswith("Electrodes opens here.")


def test_a_section_about_no_slide_is_written_from_the_rest_of_the_plan(
        project_root, monkeypatch):
    slug, project = planned_project("No Sources")
    plan = PlanStore(project.root).load()
    plan.sections[1].sources = []
    plan.sections[1].how = "Pause and ask the viewer what they expect next."
    PlanStore(project.root).save(plan)
    fake = FakeScriptModel()
    monkeypatch.setattr(script_drafting, "complete_structured", fake)

    script_drafting.draft_section(slug, "s2")

    prompt = fake.prompts["Electrodes"]
    assert "The video's other sections, in order:" in prompt
    assert "How it is told: Pause and ask the viewer" in prompt


def test_drafting_an_unknown_section_is_refused(project_root):
    slug, _ = planned_project("Unknown")
    with pytest.raises(OperationFailed, match="no section"):
        script_drafting.draft_section(slug, "made-up")


# --- drafting every unwritten section ---------------------------------------------------


def test_draft_all_fills_only_the_empty_sections(project_root, monkeypatch):
    slug, project = planned_project("Draft All")
    operations.write_section_script(slug, "s1", "Already written by hand.")
    monkeypatch.setattr(script_drafting, "complete_structured", FakeScriptModel())

    result = script_drafting.draft_unwritten_sections(slug)

    script = ScriptStore(project.root).load()
    assert script.body_for("s1") == "Already written by hand."
    assert sorted(result["drafted_section_ids"]) == ["s2", "s3"]
    assert script.body_for("s3").startswith("Amplifiers opens here.")


def test_text_written_while_drafting_is_kept(project_root, monkeypatch):
    slug, project = planned_project("Typed Meanwhile")

    def someone_types(title):
        if title == "Electrodes":
            operations.write_section_script(slug, "s2", "Typed while the drafts ran.")

    monkeypatch.setattr(script_drafting, "complete_structured",
                        FakeScriptModel(during_call=someone_types))
    result = script_drafting.draft_unwritten_sections(slug)

    assert ScriptStore(project.root).load().body_for("s2") == "Typed while the drafts ran."
    assert any("kept as it is" in note for note in result["notes"])


def test_one_failed_section_does_not_lose_the_rest(project_root, monkeypatch):
    slug, project = planned_project("One Fails")
    monkeypatch.setattr(script_drafting, "complete_structured",
                        FakeScriptModel(fail_for={"Electrodes"}))

    result = script_drafting.draft_unwritten_sections(slug)

    assert sorted(result["drafted_section_ids"]) == ["s1", "s3"]
    assert any('"Electrodes" could not be drafted' in note for note in result["notes"])


def test_draft_all_with_nothing_to_draft_says_so(project_root, monkeypatch):
    slug, _ = planned_project("All Written")
    for section_id in ("s1", "s2", "s3"):
        operations.write_section_script(slug, section_id, "Written.")

    with pytest.raises(OperationFailed, match="already has narration"):
        script_drafting.draft_unwritten_sections(slug)


# --- narration against what it was written from -------------------------------------------


def out_of_date(slug):
    return {entry["section_id"]: entry["reasons"]
            for entry in operations.read_artifact(slug, "script")["out_of_date"]}


def test_changing_the_plan_section_flags_its_narration(project_root):
    slug, project = planned_project("Plan Changed")
    operations.write_section_script(slug, "s1", "Written against the first summary.")
    assert out_of_date(slug) == {}

    plan = PlanStore(project.root).load()
    plan.sections[0].summary = "A different point entirely."
    PlanStore(project.root).save(plan)

    assert out_of_date(slug) == {"s1": ["the plan section changed"]}


def test_changing_the_source_content_flags_its_narration(project_root):
    slug, project = planned_project("Source Changed")
    operations.write_section_script(slug, "s2", "Electrodes detect what is there.")

    reworded = document("chapter.docx", [
        ("Signals", "Neurons produce tiny signals of about 50 microvolts."),
        ("Electrodes", "Electrodes now also inject current."),
        ("Amplifiers", "Amplifiers raise the signal a thousandfold before digitising."),
    ])
    ExtractionStore(project.root).save(Extraction(documents=[reworded]))

    assert out_of_date(slug) == {"s2": ["its source content changed"]}


def test_a_new_target_length_does_not_flag_narration(project_root):
    slug, project = planned_project("Length Only")
    operations.write_section_script(slug, "s1", "Short.")
    plan = PlanStore(project.root).load()
    plan.sections[0].estimated_seconds = 120
    PlanStore(project.root).save(plan)

    assert out_of_date(slug) == {}


def test_keeping_narration_as_is_clears_the_flag(project_root):
    slug, project = planned_project("Keep As Is")
    operations.write_section_script(slug, "s1", "Still right.")
    plan = PlanStore(project.root).load()
    plan.sections[0].summary = "Reworded, same point."
    PlanStore(project.root).save(plan)

    confirmed = operations.confirm_section_narration(slug, "s1")

    assert confirmed["out_of_date"] == []
    assert ScriptStore(project.root).load().body_for("s1") == "Still right."


def test_narration_with_no_record_is_not_called_out_of_date(project_root):
    slug, project = planned_project("No Record")
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id="s1", body="Written before this was tracked."),
    ]))
    plan = PlanStore(project.root).load()
    plan.sections[0].summary = "Changed."
    PlanStore(project.root).save(plan)

    assert out_of_date(slug) == {}


def test_saving_the_script_stamps_only_the_sections_whose_words_changed(project_root):
    """Saving the whole script after editing one section must not declare every
    other section freshly checked against the current plan."""
    slug, project = planned_project("Stamp One")
    operations.write_section_script(slug, "s1", "One.")
    operations.write_section_script(slug, "s2", "Two.")
    plan = PlanStore(project.root).load()
    plan.sections[1].summary = "Section two changed."
    PlanStore(project.root).save(plan)

    script = ScriptStore(project.root).load()
    edited = next(s for s in script.section_scripts if s.section_id == "s1")
    edited.scenes[0].narration = "One, edited."
    operations.save_artifact(slug, "script", script)

    assert out_of_date(slug) == {"s2": ["the plan section changed"]}


# --- what the page is given --------------------------------------------------------------


def test_the_script_carries_each_sections_plan_details(project_root):
    slug, _ = planned_project("Page Data")

    script = operations.read_artifact(slug, "script")
    first = script["plan_sections"][0]

    assert first["sources"] == [
        {"file_name": "chapter.docx", "heading_path": ["Signals"], "slide_number": 0},
    ]
    assert script["audience"] == "Students new to the topic"


def test_narration_no_section_points_at_is_shown(project_root):
    """Module-2 had 1,004 words in this state, visible nowhere."""
    slug, project = planned_project("Stranded")
    ScriptStore(project.root).save(Script(section_scripts=[
        SectionScript(section_id="old-section", body="Words from an earlier plan."),
    ]))

    orphaned = operations.read_artifact(slug, "script")["orphaned"]

    assert orphaned == [{"section_id": "old-section", "word_count": 5, "scene_count": 1,
                         "preview": "Words from an earlier plan."}]


def test_review_comments_for_scripting_appear_on_their_section(project_root):
    slug, _ = planned_project("Comments")
    operations.add_review_comment(slug, body="Too fast here", at_ms=45_000,
                                  routed_to_stage="script-staging")
    operations.add_review_comment(slug, body="Wrong colour", at_ms=45_000,
                                  routed_to_stage="studio")

    placed = operations.read_artifact(slug, "script")["comments_by_section"]

    # Estimated starts: s1 at 0, s2 at 40 s, s3 at 80 s -- 45 s falls in s2.
    assert list(placed) == ["s2"]
    assert placed["s2"][0]["body"] == "Too fast here"


def test_measured_durations_appear_after_a_render(project_root):
    slug, project = planned_project("Measured")
    operations.write_section_script(slug, "s1", "One sentence for the first section.")
    operations.write_section_script(slug, "s2", "Two sentences here. And a second one.")

    operations.render_video(slug, voice_provider="silent")
    measured = operations.read_artifact(slug, "script")["measured_seconds"]

    assert set(measured) == {"s1", "s2"}
    assert all(seconds > 0 for seconds in measured.values())


def test_the_scripting_chip_counts_sections_written(project_root):
    from pipeline.stages import Stage

    slug, project = planned_project("Chip")
    operations.write_section_script(slug, "s1", " ".join(["word"] * 150))

    assert project.stage_state(Stage.SCRIPT_STAGING).detail == "1 of 3 sections written · ~1 min"


# --- agents read a compact plan ------------------------------------------------------------


def test_agents_see_every_section_of_a_large_plan(project_root):
    """A real twelve-section plan was 23,000 characters as the page receives it;
    cut at 12,000, the Scripting agent could see only ten sections."""
    from pipeline.agent_runtime import artifact_for_agents

    slug, project = planned_project("Large Plan")
    plan = PlanStore(project.root).load()
    plan.sections = [
        PlanSection(title=f"Section {n}: " + "a long descriptive title " * 3,
                    summary="A summary that goes on for a while. " * 6,
                    sources=[reference("Signals")])
        for n in range(1, 41)
    ]
    PlanStore(project.root).save(plan)

    for_agents = artifact_for_agents(project, "plan")

    assert all(f"Section {n}:" in for_agents for n in range(1, 41))
    assert "source_outline" not in for_agents and "heading_path" not in for_agents


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


def test_the_scripting_routes(project_root, client, monkeypatch):
    slug, _ = planned_project("Routes")
    monkeypatch.setattr(script_drafting, "complete_structured", FakeScriptModel())

    drafted = client.post(f"/api/projects/{slug}/script/draft-unwritten", json={})
    assert drafted.status_code == 201, drafted.text
    assert sorted(drafted.json()["drafted_section_ids"]) == ["s1", "s2", "s3"]

    confirmed = client.post(f"/api/projects/{slug}/script/sections/s1/confirm")
    assert confirmed.status_code == 201, confirmed.text

    one = client.post(f"/api/projects/{slug}/script/draft", json={"section_id": "s2"})
    assert one.status_code == 201 and one.json()["scene_count"] == 2


async def test_mcp_offers_drafting_every_unwritten_section():
    from pipeline.mcp_server import server

    names = {tool.name for tool in await server.list_tools()}
    assert {"draft_section_script", "draft_unwritten_sections"} <= names


# --- whose voice the narration is in ------------------------------------------------


def test_every_draft_is_told_to_speak_as_the_teacher(project_root, monkeypatch):
    """A finished video said "The chapter opens with a line from Plato": the
    narrator was describing a book instead of teaching the viewer."""
    from pipeline.narration_voice import VOICE_RULE

    slug, _ = planned_project("Voice")
    systems = []

    def fake(response_model, system_prompt, user_prompt, **kwargs):
        systems.append(system_prompt)
        return FakeScriptModel()(response_model, system_prompt, user_prompt)

    monkeypatch.setattr(script_drafting, "complete_structured", fake)
    script_drafting.draft_section(slug, "s1")

    assert VOICE_RULE in systems[0]
    assert "you are the teacher" in systems[0] and '"the chapter"' in systems[0]


def test_narration_that_talks_about_the_source_is_found():
    from pipeline.narration_voice import reporting_phrases

    assert reporting_phrases("The chapter opens with a line from Plato.")
    assert reporting_phrases("This chapter explores the neural systems.")
    assert reporting_phrases("According to the author, vision is built.")
    assert reporting_phrases("Let me tell you about Padma. Plato wrote that love "
                             "makes us poets. You see with your brain.") == []


class SlideModel:
    """Stands in for the check against the slides and the revision, in turn."""

    def __init__(self, *answers):
        self.answers = list(answers)
        self.asked = []

    def __call__(self, response_model, system_prompt, user_prompt, **kwargs):
        self.asked.append((response_model.__name__, system_prompt, user_prompt))
        return self.answers.pop(0)


SLIDES = ("--- slide 7 ---\nCells seen under the microscope. Some believed nerve cells were "
          "fused into one network, a syncytium.")


def two_scenes():
    from pipeline.scripting import ScriptScene

    return [ScriptScene(id="a", narration="Hooke looked down his microscope and saw cells.",
                        brief="PICTURE: Slide 7"),
            ScriptScene(id="b", narration="Synapses grow stronger every year you learn.",
                        brief="DRAW: a synapse")]


@pytest.mark.real_fact_check
def test_a_section_that_leaves_a_slide_point_out_or_leads_away_is_revised_by_the_agent(
        monkeypatch):
    """Demo 001 kept 50 flagged claims and left the syncytium theory unsaid. The
    slides are the direction: what is missing or leads away is fixed by the agent
    before anyone reads it, and only what it kept is listed."""
    from pipeline.scripting import ScriptScene

    review = script_review.SlideReview(
        points=[script_review.SlidePoint(slide="slide 7", point="cells seen", covered=True),
                script_review.SlidePoint(slide="slide 7", point="the syncytium theory",
                                         covered=False)],
        leads_away=["scene 2: synapses grow stronger every year -- slide 7 is about cells"])
    revised = script_review.RevisedSection(scenes=[
        script_review.RevisedScene(narration="Hooke looked down his microscope and saw cells.",
                                   brief="PICTURE: Slide 7"),
        script_review.RevisedScene(narration="Some thought nerve cells were fused into one "
                                             "net: a syncytium.",
                                   brief="DRAW: cells fused into one net")])
    clean = script_review.SlideReview(points=[
        script_review.SlidePoint(slide="slide 7", point="the syncytium theory", covered=True)])
    model = SlideModel(review, revised, clean)
    monkeypatch.setattr("pipeline.llm.complete_structured", model)
    notes = []

    kept = script_review.keep_to_slides(
        "You are the teacher.", SLIDES, two_scenes(), notes, "First Glimpse")

    assert [name for name, *_ in model.asked] == ["SlideReview", "RevisedSection", "SlideReview"]
    assert "the syncytium theory" in model.asked[1][2] and "every year" in model.asked[1][2]
    assert model.asked[1][1].startswith("You are the teacher."), "revised in the same voice"
    assert "syncytium" in kept.scenes[1].narration and kept.scenes[1].id == "b", \
        "the plan's scene ids"
    assert isinstance(kept.scenes[1], ScriptScene)
    assert kept.claims == [] and kept.missing == []
    assert "revised in 1 round(s)" in notes[0]


@pytest.mark.real_fact_check
def test_the_agent_keeps_revising_until_nothing_is_left(monkeypatch):
    """Revised once, what one pass missed stayed on the page as a warning. The agent
    goes round again: check, revise, check, until clean."""
    missing = script_review.SlideReview(points=[
        script_review.SlidePoint(slide="slide 7", point="the syncytium theory", covered=False)])
    same = script_review.RevisedSection(scenes=[
        script_review.RevisedScene(narration=s.narration, brief=s.brief) for s in two_scenes()])
    clean = script_review.SlideReview()
    model = SlideModel(missing, same, missing, same, clean)
    monkeypatch.setattr("pipeline.llm.complete_structured", model)
    notes = []

    kept = script_review.keep_to_slides("", SLIDES, two_scenes(), notes, "x")

    assert [name for name, *_ in model.asked].count("RevisedSection") == 2
    assert kept.missing == [] and "revised in 2 round(s)" in notes[0]


@pytest.mark.real_fact_check
def test_after_three_rounds_what_is_left_goes_to_a_person(monkeypatch):
    left = script_review.SlideReview(wrong=["scene 1: a claim -- what is right"])
    same = script_review.RevisedSection(scenes=[
        script_review.RevisedScene(narration=s.narration, brief=s.brief) for s in two_scenes()])
    model = SlideModel(left, same, left, same, left, same, left)
    monkeypatch.setattr("pipeline.llm.complete_structured", model)
    notes = []

    kept = script_review.keep_to_slides("", SLIDES, two_scenes(), notes, "x")

    assert [name for name, *_ in model.asked].count("RevisedSection") == 3
    assert kept.claims == ["scene 1: a claim -- what is right"]
    assert "after 3 rounds" in notes[0]


@pytest.mark.real_fact_check
def test_what_the_agent_kept_on_purpose_is_told_to_the_next_check(monkeypatch):
    """A sentence kept with no reason was flagged again, and again."""
    flagged = script_review.SlideReview(
        wrong=["scene 2: negative reinforcement removes something unpleasant -- slide 20 "
               "calls it punishment"])
    keeps = script_review.RevisedSection(
        scenes=[script_review.RevisedScene(narration=s.narration, brief=s.brief)
                for s in two_scenes()],
        kept=["scene 2: negative reinforcement -- the textbook definition; the slide errs"])
    accepted = script_review.SlideReview(
        slide_wrong=["slide 20: negative reinforcement (punishment) -- they differ"])
    model = SlideModel(flagged, keeps, accepted)
    monkeypatch.setattr("pipeline.llm.complete_structured", model)

    kept = script_review.keep_to_slides("", SLIDES, two_scenes(), [], "Pavlov")

    assert "the textbook definition; the slide errs" in model.asked[2][2], \
        "the second check reads the reason"
    assert kept.claims == [] and kept.kept and kept.slide_wrong == [
        "slide 20: negative reinforcement (punishment) -- they differ"], \
        "a slide that is wrong goes to a person, apart"


@pytest.mark.real_fact_check
def test_explaining_a_slide_is_not_flagged_and_nothing_is_revised(monkeypatch):
    model = SlideModel(script_review.SlideReview(points=[
        script_review.SlidePoint(slide="slide 7", point="cells seen", covered=True)]))
    monkeypatch.setattr("pipeline.llm.complete_structured", model)

    kept = script_review.keep_to_slides("", SLIDES, two_scenes(), [], "x")

    assert len(model.asked) == 1 and kept.claims == [] and kept.missing == []
    assert "explain, define, give context" in model.asked[0][1], \
        "the slides are the direction, not a word limit"


@pytest.mark.real_fact_check
def test_a_close_with_no_slides_of_its_own_is_not_made_to_cover_every_point(monkeypatch):
    """Held to every point of the whole plan, a one-minute close was revised to cover
    twelve of them and ran to 238 words."""
    review = script_review.SlideReview(points=[
        script_review.SlidePoint(slide="slide 2", point="the heart", covered=False),
        script_review.SlidePoint(slide="slide 7", point="the syncytium", covered=False)])
    model = SlideModel(review)
    monkeypatch.setattr("pipeline.llm.complete_structured", model)

    kept = script_review.keep_to_slides(
        "", "the whole plan", two_scenes(), [], "Close", own_slides=False)

    assert len(model.asked) == 1, "nothing to revise"
    assert kept.scenes == two_scenes() and kept.claims == [] and kept.missing == []


@pytest.mark.real_fact_check
def test_a_revision_that_loses_a_scene_keeps_the_draft_and_names_what_was_found(monkeypatch):
    review = script_review.SlideReview(points=[
        script_review.SlidePoint(slide="slide 7", point="the syncytium theory", covered=False)])
    short = script_review.RevisedSection(scenes=[
        script_review.RevisedScene(narration="Only one scene.", brief="")])
    monkeypatch.setattr("pipeline.llm.complete_structured", SlideModel(review, short))
    notes = []

    kept = script_review.keep_to_slides("", SLIDES, two_scenes(), notes, "x")

    assert kept.scenes == two_scenes(), "the plan decided the scenes: none may be lost"
    assert kept.missing == ["slide 7: the syncytium theory"]
    assert "draft is kept" in notes[0]


def test_the_script_page_names_uncovered_points_and_sentences_that_lead_away(project_root):
    from pipeline.script_handoff import script_checks

    slug, project = planned_project("Follows Slides")
    plan = PlanStore(project.root).load()
    script = ScriptStore(project.root).load()
    script.section_scripts = [SectionScript(
        section_id=plan.sections[0].id, scenes=[ScriptScene(narration="Words.")],
        uncovered=["slide 7: the syncytium theory"], unsupported=["scene 2: synapses"],
        slide_wrong=["slide 20: negative reinforcement (punishment) -- they differ"])]
    ScriptStore(project.root).save(script)

    checks = {c["key"]: c for c in script_checks(project, ScriptStore(project.root).load())}
    assert checks["facts"]["name"] == "Follows the slides"
    assert checks["facts"]["status"] == "warn"
    assert "syncytium" in checks["facts"]["detail"] and "synapses" in checks["facts"]["detail"]
    assert checks["slides-wrong"]["status"] == "warn"
    assert "slide 20" in checks["slides-wrong"]["detail"]


def test_each_section_is_saved_as_it_is_drafted_and_any_error_stays_with_it(
        project_root, monkeypatch):
    """Drafting once saved nothing until every section finished, and an error
    other than a model failure lost them all."""
    slug, project = planned_project("Saved As Drafted")

    def unexpected(title):
        if title == "Electrodes":
            raise RuntimeError("something unexpected")

    monkeypatch.setattr(script_drafting, "complete_structured",
                        FakeScriptModel(during_call=unexpected))
    result = script_drafting.draft_unwritten_sections(slug)

    saved = ScriptStore(project.root).load()
    assert sorted(result["drafted_section_ids"]) == ["s1", "s3"]
    assert saved.body_for("s1").strip() and saved.body_for("s3").strip()
    assert any("something unexpected" in note for note in result["notes"])
