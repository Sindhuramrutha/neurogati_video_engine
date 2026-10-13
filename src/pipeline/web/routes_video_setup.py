"""Video setup: the learners, the voice, the music and the platforms, with samples
of each voice and bed to listen to before choosing. The work is in
`pipeline.video_setup`.
"""

from __future__ import annotations

from typing import Annotated, Any

from litestar import Request, Response, get, post
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException
from litestar.params import Body, FromPath

from pipeline import video_setup
from pipeline.core import OperationFailed, require_project
from pipeline.web.routes_project import media_response


def _guarded(call, *args, **kwargs):
    try:
        return call(*args, **kwargs)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/video-setup", sync_to_thread=False)
def read_video_setup(slug: FromPath[str]) -> dict[str, Any]:
    """The setup, and every learner, voice, pace, bed and platform to choose from."""
    return _guarded(video_setup.read, slug)


@post("/api/projects/{slug:str}/video-setup", sync_to_thread=False)
def save_video_setup(slug: FromPath[str], data: dict[str, Any]) -> dict[str, Any]:
    return _guarded(video_setup.save, slug, data)


@get("/api/voice-samples/{voice:str}", sync_to_thread=True)
def voice_sample(voice: FromPath[str], request: Request, pace: str = "normal") -> Response:
    """A few seconds of a voice at a pace -- spoken once (over the network, by
    Edge), then kept."""
    return media_response(_guarded(video_setup.voice_sample, voice, pace), request)


@get("/api/projects/{slug:str}/music-sample", sync_to_thread=True)
def music_sample(slug: FromPath[str], request: Request, music: str, intensity: str = "soft",
                 voice: str = "", pace: str = "normal") -> Response:
    """A bed alone, or under a voice at an intensity, mixed as the render mixes it."""
    root = _guarded(require_project, slug).root
    return media_response(
        _guarded(video_setup.music_sample, root, music, intensity, voice, pace), request)


@post("/api/projects/{slug:str}/video-setup/suggest-pronunciations")
async def suggest_pronunciations(slug: FromPath[str]) -> dict[str, Any]:
    """Names in the script a voice may say wrong, with respellings (AI, one call)."""
    import anyio

    return await anyio.to_thread.run_sync(
        lambda: _guarded(video_setup.suggest_pronunciations, slug))


@get("/api/projects/{slug:str}/say", sync_to_thread=True)
def say(slug: FromPath[str], request: Request, text: str) -> Response:
    """A few words in the project's voice, with its pronunciations."""
    root = _guarded(require_project, slug).root
    return media_response(_guarded(video_setup.say_sample, root, text), request)


@post("/api/projects/{slug:str}/music")
async def upload_music(
    slug: FromPath[str],
    data: Annotated[dict[str, Any], Body(media_type=RequestEncodingType.MULTI_PART)],
) -> dict[str, Any]:
    """A track the person has the rights to, kept in the project's music."""
    uploaded = next((part for part in data.values() if hasattr(part, "read")), None)
    if uploaded is None:
        raise ClientException(detail="No file was sent.")
    content = await uploaded.read()
    return _guarded(video_setup.add_music, slug, getattr(uploaded, "filename", "") or "track",
                    content)


VIDEO_SETUP_ROUTES = [read_video_setup, save_video_setup, voice_sample, music_sample,
                      upload_music, suggest_pronunciations, say]
