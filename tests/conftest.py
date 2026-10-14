"""No test may reach a real model.

Every paid call goes through `pipeline.llm._build_client`. A test that forgets to
stand the model in would make a real call on every run, unnoticed until the
provider rate-limits it. Here that fails the test instead.
A test that means to exercise the client patches `_build_client` itself, which
replaces this.
"""

import pytest


class RealModelCallInATest(AssertionError):
    pass


@pytest.fixture(autouse=True)
def no_real_model_calls(monkeypatch):
    def refuse(base_url, api_key, purpose):
        raise RealModelCallInATest(
            f"a test reached the real model ({purpose}); stand the model in first")

    monkeypatch.setattr("pipeline.llm._build_client", refuse)


@pytest.fixture(autouse=True)
def no_online_voice(monkeypatch):
    """A scene's narration is measured by speaking it. In tests the built-in silent
    voice speaks it -- a measured length, no network -- never an online voice."""
    monkeypatch.setattr("pipeline.scene_program._voice", lambda project: ("silent", ""))


@pytest.fixture(autouse=True)
def no_preflight(request, monkeypatch):
    """Renders and scene making ask the doctor first (free memory, disk). A test
    does not depend on how much memory the machine running it has free: off
    unless a test is marked `real_preflight`."""
    if request.node.get_closest_marker("real_preflight") is None:
        monkeypatch.setattr("pipeline.doctor.require_ready", lambda job: [])


@pytest.fixture(autouse=True)
def no_fact_check(request, monkeypatch):
    """Drafting a section ends with a fact-check: a second model call that the
    tests standing a model in for the drafting do not expect. Off unless a test
    is marked `real_fact_check`, where it stands that model in itself."""
    if request.node.get_closest_marker("real_fact_check") is None:
        monkeypatch.setattr("pipeline.script_drafting._fact_check",
                            lambda source, scenes, notes, title: [])


@pytest.fixture(autouse=True)
def pictures_teach(request, monkeypatch):
    """Every picture is vetted by the vision model before a scene is offered it;
    in tests each one teaches, unless a test is marked `real_vetting`."""
    if request.node.get_closest_marker("real_vetting") is None:
        monkeypatch.setattr("pipeline.scene_vetting._ask",
                            lambda path: {"teaches": True, "what": "a figure"})


@pytest.fixture(autouse=True)
def shared_state_in_tmp(tmp_path, monkeypatch):
    """The request window and the circuit breakers are shared through files in
    .cache; each test gets its own, and the gate's waits take no time."""
    monkeypatch.setattr("pipeline.llm_pace._shared_file", lambda: tmp_path / "pace.json")
    monkeypatch.setattr("pipeline.resilience._breakers", lambda: tmp_path / "breakers")
    monkeypatch.setattr("pipeline.resilience._SLEEP", lambda seconds: None)
    # With waits taking no time, an open circuit would be waited out in real time;
    # it opens only in the tests about it (test_resilience.py).
    monkeypatch.setattr("pipeline.resilience.OPEN_AFTER", 10**6)


def pytest_configure(config):
    config.addinivalue_line("markers", "real_fact_check: run the script's fact-check")
    config.addinivalue_line("markers", "real_vetting: vet pictures with the stand-in model")


# Two seconds or more each (measured on the machine Demo 001 was made on): renders,
# scene making with real renderers, layout. Marked `slow`, so the pre-commit hook's
# fast suite (`pytest -m "not slow"`) runs in about a minute and a half with the
# smoke test in it. The whole suite is still `uv run pytest`.
SLOW_TESTS = {
    "test_brand_kit.py": {
        "test_the_brand_pass_puts_the_logo_where_and_when_it_was_set",
    },
    "test_operations_and_clients.py": {
        "test_a_chapter_is_a_section_even_though_a_clip_is_a_scene",
        "test_a_forged_marker_does_not_defeat_the_guard",
        "test_an_edited_timeline_survives_a_re_render",
        "test_an_untouched_generated_timeline_is_still_rebuilt",
        "test_edited_chapters_are_not_overwritten_but_are_flagged",
        "test_every_render_is_kept_as_its_own_file",
        "test_render_frames_are_cleaned_up",
        "test_the_first_render_seeds_chapters_from_measured_timing",
        "test_two_renders_in_the_same_second_are_still_separate_versions",
    },
    "test_scene_agent.py": {
        "test_a_change_that_breaks_a_passing_scene_is_undone_and_it_ends_made",
        "test_a_crash_is_fixed_with_a_few_line_edit",
        "test_a_cut_off_answer_is_asked_again_for_less",
        "test_a_later_scene_is_told_what_the_ones_before_it_did",
        "test_a_model_call_that_fails_once_is_tried_again",
        "test_a_model_that_keeps_failing_ends_the_scene_with_the_reason",
        "test_a_new_run_clears_below_the_bar",
        "test_a_pass_with_only_polish_left_ends_the_scene",
        "test_a_refinement_the_reviewer_likes_less_does_not_replace_the_kept_one",
        "test_a_scene_is_written_rendered_reviewed_and_done",
        "test_a_storyboard_note_reaches_the_scene_as_what_the_person_asked_for",
        "test_an_edit_that_matches_nothing_is_sent_back_not_guessed",
        "test_an_unusable_answer_is_asked_again_with_what_the_render_found",
        "test_below_the_bar_after_its_rounds_a_scene_starts_over_with_a_different_shot",
        "test_out_of_rounds_with_nothing_drawn_a_plain_stand_in_is_made_and_nothing_asked",
        "test_out_of_rounds_with_passing_checks_it_is_made_with_the_remarks",
        "test_the_reviewers_notes_come_back_as_must_fix_and_polish",
        "test_with_the_ladder_spent_the_best_version_is_used_and_named",
    },
    "test_scene_lab.py": {
        "test_a_program_s_clip_is_frozen_with_the_transfer",
        "test_a_program_that_does_not_use_the_renderer_it_names_fails",
        "test_a_program_that_fails_a_check_is_not_used",
        "test_a_program_that_passes_every_check_has_a_preview_and_waits_for_approval",
        "test_a_scene_program_never_sees_the_server_s_secrets",
        "test_approval_needs_a_passing_program_and_a_new_run_withdraws_it",
        "test_every_passed_scene_can_be_approved_at_once",
    },
    "test_scene_layout.py": {
        "test_every_shot_template_passes_the_layout_checks_by_construction",
        "test_manimkit_lays_out_diagrams_cleanly_and_records_what_collides",
    },
    "test_scene_revideo.py": {
        "test_a_revideo_scene_renders_at_the_narration_s_length",
    },
    "test_scene_web.py": {
        "test_a_web_scene_is_recorded_measured_and_checked",
    },
    "test_script_drafting.py": {
        "test_a_render_warns_about_a_variable_that_is_not_defined",
        "test_measured_durations_appear_after_a_render",
        "test_variables_are_filled_in_in_the_video",
    },
    "test_video_setup.py": {
        "test_a_render_lays_the_bed_under_the_voice_in_stereo",
        "test_for_youtube_the_export_has_a_thumbnail_and_srt_subtitles",
    },
}


def pytest_collection_modifyitems(items):
    for item in items:
        if item.originalname in SLOW_TESTS.get(item.path.name, ()):
            item.add_marker(pytest.mark.slow)
