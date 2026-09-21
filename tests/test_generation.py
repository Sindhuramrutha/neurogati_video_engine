"""Generation: deciding what each scene shows, making it, and moving over it.

The stage exists because the output was "narration over static slides", which is
what every simple tool already makes. What is checked here is the part that
changes that: a scene gets a picture chosen for *it*, the picture is traceable to
where it came from, and the camera moves.
"""

import io

import pytest
from PIL import Image, ImageDraw

from pipeline import operations
from pipeline.extraction import (
    BlockKind,
    ContentBlock,
    ExtractedDocument,
    Extraction,
    ExtractionStore,
)
from pipeline.generation import (
    Motion,
    VisualKind,
    brief_fingerprint,
    numbers_in,
)
from pipeline.operations import OperationFailed
from pipeline.planning import Plan, PlanSection, PlanStore, SourceReference
from pipeline.scripting import Script, ScriptScene, ScriptStore, SectionScript


@pytest.fixture
def project_root(tmp_path, monkeypatch):
    from pipeline.config import get_settings

    monkeypatch.setenv("PROJECTS_DIR", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def picture_bytes(colour="blue", size=(400, 300)):
    """Something shaped like a figure: content inside a margin.

    Not a flat block with one stray pixel. The library now opens each picture,
    trims its border and says what is in it, and a flat block is a divider rule.
    """
    image = Image.new("RGB", size, colour)
    draw = ImageDraw.Draw(image)
    inset = (max(1, size[0] // 8), max(1, size[1] // 8))
    draw.rectangle([inset, (size[0] - inset[0], size[1] - inset[1])],
                   outline=(0, 0, 0), width=max(1, size[0] // 80))
    draw.line([inset, (size[0] - inset[0], size[1] - inset[1])],
              fill=(255, 255, 255), width=2)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def scripted_project(name, *, figures=1, scenes=2, approach="", source_text="Words about it."):
    """A project with one section, its source, and a script of scenes."""
    slug = operations.create_project(name)["slug"]
    project = operations.require_project(slug)
    (project.root / "extraction" / "assets").mkdir(parents=True, exist_ok=True)

    blocks = [
        ContentBlock(kind=BlockKind.HEADING, text="Signals", heading_path=["Signals"]),
        ContentBlock(kind=BlockKind.PARAGRAPH, text=source_text, heading_path=["Signals"]),
    ]
    for index in range(figures):
        stored = f"extraction/assets/fig{index}.png"
        (project.root / stored).write_bytes(picture_bytes())
        blocks.append(ContentBlock(
            kind=BlockKind.FIGURE, text=f"Figure {index + 1}", heading_path=["Signals"],
            asset_path=stored))

    ExtractionStore(project.root).save(Extraction(
        documents=[ExtractedDocument(file_name="chapter.docx", blocks=blocks)],
        extracted_at="2026-09-17T00:00:00+00:00"))
    PlanStore(project.root).save(Plan(sections=[PlanSection(
        id="s1", title="Signals", estimated_seconds=60, rendering_approach=approach,
        sources=[SourceReference(file_name="chapter.docx", heading_path=["Signals"])])]))
    ScriptStore(project.root).save(Script(section_scripts=[SectionScript(
        section_id="s1",
        scenes=[ScriptScene(narration=f"Scene {n + 1} narration.", brief=f"Show thing {n + 1}")
                for n in range(scenes)])]))
    return slug, project


# --- deciding ------------------------------------------------------------------------


def test_each_scene_gets_its_own_picture_from_the_source(project_root):
    """One diagram shown four times is the slideshow this stage exists to end."""
    slug, _ = scripted_project("Two Figures", figures=2, scenes=2)

    planned = operations.plan_visuals(slug)

    kinds = [visual["kind"] for visual in planned["visuals"]]
    paths = [visual["asset_path"] for visual in planned["visuals"]]
    assert kinds == [VisualKind.SOURCE_PICTURE, VisualKind.SOURCE_PICTURE]
    assert len(set(paths)) == 2, "two scenes, two different pictures"


def test_the_source_wins_over_anything_generated(project_root, monkeypatch):
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: True)
    slug, _ = scripted_project("Source First", figures=1, scenes=1)

    planned = operations.plan_visuals(slug)

    assert planned["visuals"][0]["kind"] == VisualKind.SOURCE_PICTURE
    assert planned["visuals"][0]["origin"] == "source"


def test_a_scene_with_nothing_to_show_is_drawn_when_a_model_is_configured(
    project_root, monkeypatch
):
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: True)
    slug, _ = scripted_project("Nothing To Show", figures=0, scenes=1)

    planned = operations.plan_visuals(slug)
    visual = planned["visuals"][0]

    assert visual["kind"] == VisualKind.GENERATED_IMAGE
    assert "Show thing 1" in visual["prompt"], "the prompt is built from the scene's own brief"
    assert "Do not invent" in visual["prompt"]


def test_with_no_model_a_scene_falls_back_to_its_words(project_root, monkeypatch):
    """Words on screen is a real answer. A decorative stock image would be worse."""
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: False)
    slug, _ = scripted_project("No Model", figures=0, scenes=1)

    planned = operations.plan_visuals(slug)

    assert planned["visuals"][0]["kind"] == VisualKind.TEXT
    assert any("no model key is set" in note.lower() for note in planned["notes"])


def test_a_section_shown_as_a_plot_with_real_numbers_gets_a_chart(project_root, monkeypatch):
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: True)
    slug, _ = scripted_project(
        "Numbers", figures=0, scenes=1, approach="plot",
        source_text="The signal is 50 microvolts, sampled at 1000 Hz, with 20 dB of gain.")

    planned = operations.plan_visuals(slug)

    assert planned["visuals"][0]["kind"] == VisualKind.CHART
    assert "3 figure(s)" in planned["visuals"][0]["note"]


def test_two_numbers_are_not_a_chart(project_root, monkeypatch):
    """Two points are a sentence. Charting them implies a trend nobody stated."""
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: False)
    slug, _ = scripted_project(
        "Too Few", figures=0, scenes=1, approach="plot",
        source_text="It runs at 50 Hz and costs 20 dB.")

    planned = operations.plan_visuals(slug)

    assert planned["visuals"][0]["kind"] == VisualKind.TEXT


def test_numbers_are_read_with_their_units():
    found = numbers_in("Sampled at 1,000 Hz for 30 ms, losing 12% of the signal.")

    assert [(value, unit) for value, unit, _context in found] == [
        (1000.0, "hz"), (30.0, "ms"), (12.0, "%")]


def test_deciding_again_keeps_what_was_already_decided(project_root):
    slug, _ = scripted_project("Kept", figures=1, scenes=1)
    first = operations.plan_visuals(slug)
    visual_id = first["visuals"][0]["id"]
    operations.set_scene_visual(slug, visual_id, motion=Motion.PAN_LEFT)

    again = operations.plan_visuals(slug)

    assert again["visuals"][0]["id"] == visual_id
    assert again["visuals"][0]["motion"] == Motion.PAN_LEFT


def test_rewriting_a_scene_marks_its_picture_out_of_date(project_root):
    """A picture of what a scene used to say is exactly what nobody notices."""
    slug, project = scripted_project("Rewritten", figures=1, scenes=1)
    operations.plan_visuals(slug)

    script = ScriptStore(project.root).load()
    script.section_scripts[0].scenes[0].brief = "Show something else entirely"
    ScriptStore(project.root).save(script)

    current = operations.read_visuals(slug)

    assert current["visuals"][0]["is_stale"] is True
    assert any("rewritten" in warning for warning in current["warnings"])


def test_planning_without_a_plan_is_refused(project_root):
    slug = operations.create_project("Empty")["slug"]

    with pytest.raises(OperationFailed, match="no sections"):
        operations.plan_visuals(slug)


# --- making --------------------------------------------------------------------------


def test_a_drawn_picture_is_saved_and_keeps_its_prompt(project_root, monkeypatch):
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: True)
    slug, project = scripted_project("Drawn", figures=0, scenes=1)
    operations.plan_visuals(slug)
    asked = {}

    def fake_draw(prompt, **kwargs):
        asked["prompt"] = prompt
        return picture_bytes("green")

    monkeypatch.setattr("pipeline.llm.draw_image", fake_draw)

    built = operations.build_visuals(slug)
    visual = built["visuals"][0]

    assert len(built["built_ids"]) == 1
    assert visual["asset_path"].startswith("generation/assets/")
    assert (project.root / visual["asset_path"]).exists()
    assert visual["prompt"] and asked["prompt"] == visual["prompt"], \
        "what was asked for is kept, so a drawn picture can be checked"


def test_a_chart_is_drawn_from_the_source_s_own_numbers(project_root, monkeypatch):
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: False)
    slug, project = scripted_project(
        "Charted", figures=0, scenes=1, approach="plot",
        source_text="50 microvolts at 1000 Hz with 20 dB of gain and 12% loss.")
    operations.plan_visuals(slug)

    built = operations.build_visuals(slug)
    visual = built["visuals"][0]

    chart = project.root / visual["asset_path"]
    assert chart.exists()
    with Image.open(chart) as drawn:
        assert drawn.size[0] > 400 and drawn.size[1] > 300


def test_one_failed_drawing_does_not_lose_the_others(project_root, monkeypatch):
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: True)
    slug, _ = scripted_project("Partly Drawn", figures=0, scenes=3)
    operations.plan_visuals(slug)
    calls = {"n": 0}

    def sometimes_fails(prompt, **kwargs):
        calls["n"] += 1
        if calls["n"] == 2:
            from pipeline.llm import ModelCallFailed

            raise ModelCallFailed("Could not reach the model provider.")
        return picture_bytes()

    monkeypatch.setattr("pipeline.llm.draw_image", sometimes_fails)

    built = operations.build_visuals(slug)

    assert len(built["built_ids"]) == 2
    assert any("could not reach" in note.lower() for note in built["notes"])


def test_building_twice_does_not_redraw_what_is_already_there(project_root, monkeypatch):
    monkeypatch.setattr("pipeline.llm.is_configured", lambda: True)
    slug, _ = scripted_project("Once", figures=0, scenes=1)
    operations.plan_visuals(slug)
    calls = {"n": 0}

    def counted(prompt, **kwargs):
        calls["n"] += 1
        return picture_bytes()

    monkeypatch.setattr("pipeline.llm.draw_image", counted)
    operations.build_visuals(slug)
    again = operations.build_visuals(slug)

    assert calls["n"] == 1
    assert again["built_ids"] == []


def test_changing_what_a_scene_shows_clears_the_old_picture(project_root):
    slug, _ = scripted_project("Changed", figures=1, scenes=1)
    planned = operations.plan_visuals(slug)
    visual_id = planned["visuals"][0]["id"]

    changed = operations.set_scene_visual(slug, visual_id, kind=VisualKind.TEXT)

    assert changed["visuals"][0]["kind"] == VisualKind.TEXT
    assert changed["visuals"][0]["asset_path"] == ""


def test_an_unknown_kind_is_refused(project_root):
    slug, _ = scripted_project("Bad Kind", figures=1, scenes=1)
    visual_id = operations.plan_visuals(slug)["visuals"][0]["id"]

    with pytest.raises(OperationFailed, match="not a kind"):
        operations.set_scene_visual(slug, visual_id, kind="interpretive dance")


# --- the video it produces -----------------------------------------------------------


def test_the_render_shows_each_scene_what_generation_chose(project_root):
    from pipeline.render_run import shots_for_sections

    slug, project = scripted_project("Shots", figures=2, scenes=2)
    operations.plan_visuals(slug)

    shots = shots_for_sections(project, operations.read_artifact(slug, "plan"))

    assert [shot.picture.name for shot in shots["s1"]] == ["fig0.png", "fig1.png"]
    assert {shot.motion for shot in shots["s1"]} != {"hold"}, "the camera has to move"


def test_a_project_that_never_opened_generation_still_renders(project_root):
    """The stage is an improvement, not a gate."""
    from pipeline.render_run import shots_for_sections

    slug, project = scripted_project("Skipped", figures=1, scenes=1)

    assert shots_for_sections(project, operations.read_artifact(slug, "plan")) == {}


def test_the_camera_moves_over_a_shot():
    """`hold` is a still; everything else has to actually pan or zoom, or the
    output is the slideshow this stage was added to replace."""
    from pipeline.rendering import _motion_filter

    still = _motion_filter(Motion.HOLD, 4000)
    push = _motion_filter(Motion.PUSH_IN, 4000)
    pan = _motion_filter(Motion.PAN_RIGHT, 4000)

    assert "zoompan" in still and "z=1:" in still
    assert "on/120" in push, "the zoom has to be a function of the frame number"
    assert "iw-iw/zoom" in pan


def test_a_scene_s_slides_all_share_its_shot(project_root):
    """One scene's narration can fill three slides. Restarting the picture on
    each would be the carousel again, one level down."""
    from pathlib import Path

    from pipeline.rendering import RenderedSection, Shot, _shot_for, section_segments

    section = RenderedSection(
        section_id="s1", title="Signals",
        narration="A long first scene. " * 20 + "\n\nA second scene.",
        audio_duration_ms=40_000,
        shots=[Shot(picture=Path("one.png"), motion=Motion.PUSH_IN),
               Shot(picture=Path("two.png"), motion=Motion.PAN_LEFT)],
    )
    segments = section_segments(section)
    slides = [segment for segment in segments if segment.kind == "slide"]

    first_scene = [s for s in slides if s.scene_index == 0]
    assert len(first_scene) > 1, "this scene should need more than one slide"
    assert {_shot_for(section, s).picture.name for s in first_scene} == {"one.png"}
    assert _shot_for(section, [s for s in slides if s.scene_index == 1][0]).picture.name \
        == "two.png"


def test_the_brief_fingerprint_changes_with_the_words():
    assert brief_fingerprint("show a neuron", "narration") \
        != brief_fingerprint("show a synapse", "narration")
    assert brief_fingerprint("show a neuron", "a") != brief_fingerprint("show a neuron", "b")


# --- the video preferences, which were three controls that did nothing ----------------


def set_preferences(project, **values):
    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    store = StageSettingsStore(project.root)
    store.save(Stage.SCENE_PLAN, values)


def test_the_tone_reaches_the_narration(project_root, monkeypatch):
    """It was a dropdown that saved a word and changed nothing."""
    from pipeline import script_drafting

    slug, project = scripted_project("Tone", figures=0, scenes=1)
    set_preferences(project, tone="conversational", target_duration="7-10", language="en")
    seen = {}

    def fake(response_model, system_prompt, user_prompt, **kwargs):
        seen["system"] = system_prompt
        return script_drafting.DraftedSection(scenes=[
            script_drafting.DraftedScene(narration="Spoken.", brief="Shown.")])

    monkeypatch.setattr(script_drafting, "complete_structured", fake)
    script_drafting.draft_section(slug, "s1")

    assert 'Address the viewer as "you"' in seen["system"]


def test_the_language_reaches_the_narration(project_root, monkeypatch):
    from pipeline import script_drafting

    slug, project = scripted_project("Language", figures=0, scenes=1)
    set_preferences(project, tone="professional", target_duration="7-10", language="hi")
    seen = {}

    def fake(response_model, system_prompt, user_prompt, **kwargs):
        seen["system"] = system_prompt
        return script_drafting.DraftedSection(scenes=[
            script_drafting.DraftedScene(narration="बोला गया।", brief="दिखाया गया।")])

    monkeypatch.setattr(script_drafting, "complete_structured", fake)
    script_drafting.draft_section(slug, "s1")

    assert "in Hindi" in seen["system"]
    assert "every brief" in seen["system"], "what is on screen is in the same language"


def test_the_language_picks_the_voice_that_speaks_it(project_root):
    """Narration written in Hindi and spoken by an English voice is unusable
    audio, and nothing would have said so."""
    from pipeline.stage_options import video_preferences

    slug, project = scripted_project("Spoken", figures=0, scenes=1)
    set_preferences(project, tone="professional", target_duration="7-10", language="hi")

    preferences = video_preferences(project.root)

    assert preferences.voice_for("edge") == "hi-IN-SwaraNeural"
    assert preferences.voice_for("kokoro") == "", "a provider with no Hindi voice says so"


def test_the_target_duration_reaches_the_plan_draft(project_root, monkeypatch):
    from pipeline import plan_drafting

    slug, project = scripted_project("Duration", figures=0, scenes=1)
    set_preferences(project, tone="professional", target_duration="3-5", language="en")
    seen = {}

    def fake(response_model, system_prompt, user_prompt, **kwargs):
        seen.setdefault("system", system_prompt)
        if response_model is plan_drafting.DraftOutline:
            return plan_drafting.DraftOutline(
                sections=[plan_drafting.OutlineSection(
                    title="Signals", source_ids=["d1"], estimated_seconds=900,
                    objective_numbers=[])],
                learning_objectives=["Understand signals"], key_themes=["signals"])
        return plan_drafting.SectionDetail(
            summary="About signals.", rendering_approach="still",
            rendering_reason="Nothing moves.", estimated_seconds=900)

    monkeypatch.setattr(plan_drafting, "complete_structured", fake)
    drafted = plan_drafting.draft_plan(slug)

    assert "about 3 to 5 minutes" in seen["system"]
    assert any("against your target of 3 to 5 minutes" in note for note in drafted["notes"]), \
        "a draft that misses the target says so rather than being padded or cut"
