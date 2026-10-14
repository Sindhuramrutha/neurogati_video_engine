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
