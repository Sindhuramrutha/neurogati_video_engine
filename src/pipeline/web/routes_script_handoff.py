"""Script & Staging: its checks, transferring it, and clearing leftover narration.

Its own module so `routes_project.py` does not grow; the work is in
`pipeline.script_handoff`.
"""

from __future__ import annotations

from typing import Any

from litestar import get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath

from pipeline.core import OperationFailed
from pipeline.script_handoff import (
    delete_unattached_narration,
    read_script_handoff,
    transfer_script,
)


def _client_error(call, *args) -> dict[str, Any]:
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/script/handoff", sync_to_thread=False)
def get_script_handoff(slug: FromPath[str]) -> dict[str, Any]:
    """Every check the script goes through, and whether it is transferred."""
    return _client_error(read_script_handoff, slug)


@post("/api/projects/{slug:str}/script/transfer", sync_to_thread=False)
def transfer_script_route(slug: FromPath[str]) -> dict[str, Any]:
    """Hand the script to the stages after it. Refused while a check fails."""
    return _client_error(transfer_script, slug)


@post("/api/projects/{slug:str}/script/unattached/delete", sync_to_thread=False)
def delete_unattached_route(slug: FromPath[str]) -> dict[str, Any]:
    """Delete all narration that belongs to no section of the plan."""
    return _client_error(delete_unattached_narration, slug)


SCRIPT_HANDOFF_ROUTES = [get_script_handoff, transfer_script_route, delete_unattached_route]
