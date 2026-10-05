"""Generation: its checks, what making would do, and transferring the shots.

Its own module so `routes_project.py` does not grow; the work is in
`pipeline.generation_handoff`.
"""

from __future__ import annotations

from typing import Any

from litestar import get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath

from pipeline.core import OperationFailed
from pipeline.generation_handoff import read_generation_handoff, transfer_generation


def _client_error(call, *args) -> dict[str, Any]:
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/visuals/handoff", sync_to_thread=False)
def get_generation_handoff(slug: FromPath[str]) -> dict[str, Any]:
    """The checks, what Make would do, the decision rules, and the transfer state."""
    return _client_error(read_generation_handoff, slug)


@post("/api/projects/{slug:str}/visuals/transfer", sync_to_thread=False)
def transfer_generation_route(slug: FromPath[str]) -> dict[str, Any]:
    """Freeze the shots and hand them to the render. Refused while a check fails."""
    return _client_error(transfer_generation, slug)


GENERATION_HANDOFF_ROUTES = [get_generation_handoff, transfer_generation_route]
