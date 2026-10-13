"""The gate every outside call goes through: what it retries, what it does not,
how long it waits, and the circuit every process shares."""

import pytest

from pipeline import resilience
from pipeline.resilience import (
    OPEN_AFTER,
    ServiceUnavailable,
    breaker_state,
    call,
    classify,
)


@pytest.fixture(autouse=True)
def circuit_opens(monkeypatch):
    monkeypatch.setattr(resilience, "OPEN_AFTER", OPEN_AFTER)


class Refused(Exception):
    """An HTTP answer with a status, as httpx and openai errors carry one."""

    def __init__(self, status, retry_after=None):
        super().__init__(f"status {status}")
        self.status_code = status
        headers = {"retry-after": str(retry_after)} if retry_after is not None else {}
        self.response = type("R", (), {"headers": headers, "status_code": status})()


class NoAudioReceived(Exception):
    pass


def flaky(failures, then="ok"):
    calls = []

    def attempt():
        calls.append(1)
        if len(calls) <= len(failures):
            raise failures[len(calls) - 1]
        return then
    return attempt, calls


def test_a_throttled_or_dropped_call_is_tried_again_until_it_works():
    attempt, calls = flaky([NoAudioReceived(), Refused(429), Refused(503)])
    waits = []

    assert call("svc", attempt, sleep=waits.append) == "ok"
    assert len(calls) == 4 and len(waits) == 3
    assert breaker_state("svc")["failures"] == 0, "a success closes the circuit"


def test_a_permanent_failure_is_raised_at_once_and_never_retried():
    attempt, calls = flaky([Refused(401)])
    with pytest.raises(Refused):
        call("svc", attempt, sleep=lambda s: None)
    assert len(calls) == 1

    for permanent in (Refused(400), ValueError("a bug"),
                      type("SpeechFailed", (Exception,), {"transient": False})("off")):
        assert classify(permanent) == "permanent"


def test_the_wait_the_service_asks_for_is_the_wait_taken():
    attempt, _ = flaky([Refused(429, retry_after=7)])
    waits = []
    call("svc", attempt, sleep=waits.append)
    assert waits == [7.0]


def test_backoff_grows_with_jitter_and_stops_at_the_last_attempt():
    attempt, calls = flaky([NoAudioReceived()] * 10)
    waits = []
    with pytest.raises(ServiceUnavailable) as stopped:
        call("svc", attempt, attempts=4, base_seconds=2, sleep=waits.append)
    assert len(calls) == 4 and len(waits) == 3
    assert all(0 <= wait <= 2 * 2 ** number for number, wait in enumerate(waits))
    assert stopped.value.transient and classify(stopped.value) == "transient"
    assert isinstance(stopped.value.__cause__, NoAudioReceived)


def test_an_error_wrapped_by_the_pipeline_is_classed_by_what_caused_it():
    try:
        try:
            raise NoAudioReceived()
        except NoAudioReceived as inner:
            raise RuntimeError("Edge TTS failed") from inner
    except RuntimeError as outer:
        assert classify(outer) == "transient"


def test_after_repeated_failures_the_circuit_opens_for_every_caller(monkeypatch):
    attempt, _ = flaky([NoAudioReceived()] * OPEN_AFTER)
    with pytest.raises(ServiceUnavailable):
        call("svc", attempt, attempts=OPEN_AFTER, sleep=lambda s: None)
    assert breaker_state("svc")["open_until"] > 0

    # Another caller -- another process reads the same file -- does not call the
    # service while it is open; with no time to wait, it says so at once.
    tried = []
    with pytest.raises(ServiceUnavailable, match="recover"):
        call("svc", lambda: tried.append(1), give_up_after=1, sleep=lambda s: None)
    assert not tried


def test_edge_speech_is_asked_again_when_no_audio_comes(tmp_path, monkeypatch):
    import edge_tts

    from pipeline.speech import _speak_edge

    tries = []

    class Communicate:
        def __init__(self, *args, **kwargs):
            pass

        async def stream(self):
            tries.append(1)
            if len(tries) < 3:
                raise edge_tts.exceptions.NoAudioReceived("No audio was received.")
            yield {"type": "audio", "data": b"ID3audio"}
            yield {"type": "WordBoundary", "text": "Hello", "offset": 0, "duration": 5_000_000}

    monkeypatch.setattr(edge_tts, "Communicate", Communicate)
    words = _speak_edge("Hello", tmp_path / "out.mp3", "en-US-AndrewNeural")

    assert len(tries) == 3 and [w.text for w in words] == ["Hello"]
    assert (tmp_path / "out.mp3").read_bytes() == b"ID3audio"


def test_a_cut_off_answer_is_not_retried_as_if_the_service_were_down():
    from pipeline.llm import ModelOutputTruncated

    assert classify(ModelOutputTruncated("stopped at the limit")) == "permanent"
    assert resilience.is_transient(ServiceUnavailable("svc", "down"))
