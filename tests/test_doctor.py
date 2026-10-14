"""The doctor: a job asks before it spends anything, and every client asks the same way."""
# The fixtures are shared with the render-job tests by import, which ruff
# reads as redefinition when a test takes them as arguments.
# ruff: noqa: F811

import tempfile

import pytest

from pipeline import doctor, render_queue
from pipeline.operations import OperationFailed
from tests.test_render_job import fakes, project_root, three_sections  # noqa: F401
from tests.test_render_queue import statuses, wait_for


def failing_check():
    return [doctor._check("memory", "Free memory", doctor.FAIL, "0.4 GB available.",
                          "Close other programs.")]


def test_the_quick_checks_name_every_tool_folder_and_the_memory(project_root):
    keys = [check["key"] for check in doctor.quick()]

    assert keys[:3] == ["tool-ffmpeg", "tool-ffprobe", "tool-uv"]
    for key in ("disk-projects", "disk-working files", "memory",
                "write-projects", "write-working files"):
        assert key in keys


def test_a_missing_tool_fails_and_says_how_to_fix_it(project_root, monkeypatch):
    monkeypatch.setattr(doctor.shutil, "which",
                        lambda tool: None if tool == "uv" else f"/bin/{tool}")

    uv = next(c for c in doctor.quick() if c["key"] == "tool-uv")

    assert uv["status"] == doctor.FAIL
    assert "Install uv" in uv["fix"]


def test_a_passing_check_carries_no_fix():
    assert doctor._check("k", "n", doctor.PASS, "fine", "do something")["fix"] == ""


def test_readiness_is_the_worst_of_its_checks(monkeypatch):
    def checks(*statuses):
        return [doctor._check(str(i), "n", s, "") for i, s in enumerate(statuses)]

    monkeypatch.setattr(doctor, "quick", lambda: checks(doctor.PASS, doctor.WARN))
    assert doctor.check_readiness()["status"] == doctor.WARN
    monkeypatch.setattr(doctor, "quick",
                        lambda: checks(doctor.WARN, doctor.FAIL, doctor.PASS))
    assert doctor.check_readiness()["status"] == doctor.FAIL


def test_the_deep_checks_ask_each_service_once(monkeypatch):
    monkeypatch.setattr(doctor, "quick", lambda: [])
    for name in ("_encode", "_scene_environment", "_text_model", "_vision_model", "_voice"):
        monkeypatch.setattr(doctor, name,
                            lambda name=name: doctor._check(name, name, doctor.PASS, ""))

    found = doctor.check_readiness(True)

    assert [c["key"] for c in found["checks"]] == [
        "_encode", "_scene_environment", "_text_model", "_vision_model", "_voice"]


def test_a_service_that_raises_is_a_failed_check_not_a_crash():
    def broken():
        raise ConnectionError("the provider is down")

    check = doctor._answers("model", "The writing model answers", broken, "Try later.")

    assert check["status"] == doctor.FAIL
    assert "provider is down" in check["detail"] and check["fix"] == "Try later."


@pytest.mark.real_preflight
def test_not_ready_names_every_failure_and_is_transient(monkeypatch):
    from pipeline.resilience import is_transient

    monkeypatch.setattr(doctor, "quick", failing_check)

    with pytest.raises(doctor.NotReady, match="The render cannot start yet.*0.4 GB") as said:
        doctor.require_ready("The render")

    assert isinstance(said.value, OperationFailed)
    assert is_transient(said.value)


@pytest.mark.real_preflight
def test_a_render_does_not_start_on_a_machine_that_is_not_ready(project_root, fakes,
                                                                monkeypatch):
    from pipeline import progress
    from pipeline.render_run import render_video

    slug, _ = three_sections("Not Ready")
    monkeypatch.setattr(doctor, "quick", failing_check)

    with pytest.raises(doctor.NotReady):
        render_video(slug, "silent")

    assert not fakes["spoken"]
    assert not any(entry["slug"] == slug for entry in progress.running())


@pytest.mark.real_preflight
def test_a_queued_render_waits_for_the_machine_and_does_not_start_over(project_root, fakes,
                                                                       monkeypatch):
    slug, _ = three_sections("Waits")
    monkeypatch.setattr(doctor, "quick", failing_check)

    render_queue.add_job(slug, "silent")
    view = wait_for(lambda v: statuses(v) == ["waiting"])

    assert "0.4 GB" in view["jobs"][0]["message"]
    assert not fakes["spoken"]


@pytest.mark.real_preflight
def test_scenes_are_not_queued_on_a_machine_that_is_not_ready(project_root, monkeypatch):
    from pipeline import scene_agent
    from pipeline.operations import create_project

    create_project("Scenes Wait")
    monkeypatch.setattr(doctor, "quick", failing_check)

    with pytest.raises(doctor.NotReady, match="Making scenes cannot start yet"):
        scene_agent.start("scenes-wait", ["any"])


def test_working_files_go_where_the_setting_says(tmp_path, monkeypatch):
    from pipeline.config import get_settings, use_work_dir

    monkeypatch.setenv("PIPELINE_TEMP", str(tmp_path / "work"))
    for name in ("TMP", "TEMP", "TMPDIR"):
        monkeypatch.setenv(name, str(tmp_path))
    monkeypatch.setattr(tempfile, "tempdir", None)
    get_settings.cache_clear()
    try:
        use_work_dir()
        assert tempfile.gettempdir() == str(tmp_path / "work")
        assert (tmp_path / "work").is_dir()
    finally:
        get_settings.cache_clear()


# --- every client asks the same way ------------------------------------------------------

def test_the_web_app_answers_the_doctor(monkeypatch):
    from litestar.testing import TestClient

    from pipeline.web.app import create_app

    monkeypatch.setattr(doctor, "quick", failing_check)
    with TestClient(app=create_app()) as client:
        answer = client.get("/api/doctor").json()

    assert answer["status"] == doctor.FAIL
    assert answer["checks"][0]["fix"] == "Close other programs."


async def test_the_doctor_is_an_mcp_tool():
    from pipeline.mcp_server import server

    assert "check_readiness" in {tool.name for tool in await server.list_tools()}


def test_the_cli_exits_non_zero_when_a_check_fails(monkeypatch, capsys):
    import sys

    from pipeline import cli

    monkeypatch.setattr(doctor, "quick", failing_check)
    monkeypatch.setattr(sys, "argv", ["pipeline", "doctor"])
    monkeypatch.setattr(cli, "use_work_dir", lambda: None)

    assert cli.main() == 1
    assert '"status": "fail"' in capsys.readouterr().out
