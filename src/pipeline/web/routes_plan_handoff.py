"""Scene Plan: its checks, and transferring it to the next layer.

Its own module so `routes_project.py` does not grow; the work is in
`pipeline.plan_handoff`.
"""

from __future__ import annotations

from typing import Any

from litestar import get, post
from litestar.exceptions import ClientException
from litestar.params import FromPath

from pipeline.core import OperationFailed
from pipeline.plan_handoff import read_plan_handoff, transfer_plan


def _client_error(call, *args) -> dict[str, Any]:
    try:
        return call(*args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/plan/handoff", sync_to_thread=False)
def get_plan_handoff(slug: FromPath[str]) -> dict[str, Any]:
    """Every check the plan goes through, and whether it is transferred."""
    return _client_error(read_plan_handoff, slug)


@post("/api/projects/{slug:str}/plan/transfer", sync_to_thread=False)
def transfer_plan_route(slug: FromPath[str]) -> dict[str, Any]:
    """Hand the plan to the stages after it. Refused while a check fails."""
    return _client_error(transfer_plan, slug)


PLAN_HANDOFF_ROUTES = [get_plan_handoff, transfer_plan_route]
