"""Generation: one scene per scene of the script, kept while its brief is unchanged,
and marked out of date when the script is rewritten.
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
from pipeline.generation import VisualPlanStore, brief_fingerprint
from pipeline.operations import OperationFailed
from pipeline.planning import Plan, PlanScene, PlanSection, PlanStore, SourceReference
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


def scripted_project(name, *, figures=1, scenes=2, source_text="Words about it."):
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
        (project.root / stored).write_bytes(picture_bytes(("blue", "green", "red")[index % 3]))
        blocks.append(ContentBlock(
            kind=BlockKind.FIGURE, text=f"Figure {index + 1}", heading_path=["Signals"],
            asset_path=stored))

    ExtractionStore(project.root).save(Extraction(
        documents=[ExtractedDocument(file_name="chapter.docx", blocks=blocks)],
        extracted_at="2026-09-17T00:00:00+00:00"))
    # The chain: the pictures are gathered and transferred before the plan.
    from pipeline.assets_handoff import confirm_assets
    operations.refresh_asset_library(slug)
    confirm_assets(slug)
    PlanStore(project.root).save(Plan(sections=[PlanSection(
        id="s1", title="Signals", estimated_seconds=60,
        sources=[SourceReference(file_name="chapter.docx", heading_path=["Signals"])],
        scenes=[PlanScene(does=f"Scene {n + 1}", seconds=60 // scenes)
                for n in range(scenes)])]))
    ScriptStore(project.root).save(Script(section_scripts=[SectionScript(
        section_id="s1",
        scenes=[ScriptScene(narration=f"Scene {n + 1} narration.", brief=f"Show thing {n + 1}")
                for n in range(scenes)])]))
    return slug, project


# --- deciding ------------------------------------------------------------------------


def test_deciding_again_keeps_what_was_already_decided(project_root):
    slug, project = scripted_project("Kept", figures=1, scenes=1)
    first = operations.plan_visuals(slug)
    visual_id = first["visuals"][0]["id"]
    store = VisualPlanStore(project.root)
    plan = store.load()
    plan.visuals[0].clip_path = "generation/scenes/one/render.mp4"
    store.save(plan)

    again = operations.plan_visuals(slug)

    assert again["visuals"][0]["id"] == visual_id
    assert again["visuals"][0]["clip_path"] == "generation/scenes/one/render.mp4"


def test_rewriting_a_scene_marks_its_picture_out_of_date(project_root):
    """A program for what a scene used to say is exactly what nobody notices."""
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


# --- the video it produces -----------------------------------------------------------


def test_a_project_that_never_opened_generation_still_renders(project_root):
    """The stage is an improvement, not a gate."""
    from pipeline.render_run import shots_for_sections

    slug, project = scripted_project("Skipped", figures=1, scenes=1)

    assert shots_for_sections(project, operations.read_artifact(slug, "plan")) == {}


def test_a_scene_s_slides_all_share_its_shot(project_root):
    """One scene's narration can fill three slides. Restarting the picture on
    each would be the carousel again, one level down."""
    from pathlib import Path

    from pipeline.rendering import RenderedSection, Shot, _shot_for, section_segments

    section = RenderedSection(
        section_id="s1", title="Signals",
        narration="A long first scene. " * 20 + "\n\nA second scene.",
        audio_duration_ms=40_000,
        shots=[Shot(picture=Path("one.png")), Shot(picture=Path("two.png"))],
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


# --- the video preferences ---------------------------------------------------------


def set_preferences(project, **values):
    from pipeline.stage_options import StageSettingsStore
    from pipeline.stages import Stage

    store = StageSettingsStore(project.root)
    store.save(Stage.SCENE_PLAN, values)


def test_the_teaching_tone_reaches_the_narration(project_root, monkeypatch):
    """There is no tone to choose: every video teaches, in one voice."""
    from pipeline import script_drafting

    slug, project = scripted_project("Tone", figures=0, scenes=1)
    set_preferences(project, language="en")
    seen = {}

    def fake(response_model, system_prompt, user_prompt, **kwargs):
        seen["system"] = system_prompt
        return script_drafting.DraftedSection(scenes=[
            script_drafting.DraftedScene(narration="Spoken.", brief="Shown.")])

    monkeypatch.setattr(script_drafting, "complete_structured", fake)
    script_drafting.draft_section(slug, "s1")

    assert 'A teacher explaining to one viewer' in seen["system"]


def test_the_language_reaches_the_narration(project_root, monkeypatch):
    from pipeline import script_drafting

    slug, project = scripted_project("Language", figures=0, scenes=1)
    set_preferences(project, language="hi")
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
    set_preferences(project, language="hi")

    preferences = video_preferences(project.root)

    assert preferences.voice_for("edge") == "hi-IN-SwaraNeural"
    assert preferences.voice_for("kokoro") == "", "a provider with no Hindi voice says so"

