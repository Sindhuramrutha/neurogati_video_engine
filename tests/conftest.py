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


def pytest_configure(config):
    config.addinivalue_line("markers", "real_fact_check: run the script's fact-check")
    config.addinivalue_line("markers", "real_vetting: vet pictures with the stand-in model")
