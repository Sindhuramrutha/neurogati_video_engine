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
