"""The fact ledger (`pipeline.fact_ledger`): the deck's facts, checked by two models,
and a person's decisions where a slide is wrong. Its own module so `routes_project.py`
does not grow."""

from __future__ import annotations

from typing import Any

import anyio
from litestar import get, post, put
from litestar.exceptions import ClientException
from litestar.params import FromPath

from pipeline import fact_ledger
from pipeline.core import OperationFailed


async def _in_thread(call, *args) -> Any:
    try:
        return await anyio.to_thread.run_sync(call, *args)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@get("/api/projects/{slug:str}/facts", sync_to_thread=False)
def get_facts(slug: FromPath[str]) -> dict[str, Any]:
    """Every claim the deck makes: verified, disputed or uncertain, and what was decided."""
    try:
        return fact_ledger.view(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@put("/api/projects/{slug:str}/facts/{claim_id:str}", sync_to_thread=False)
def decide_fact(slug: FromPath[str], claim_id: FromPath[str],
                data: dict[str, Any]) -> dict[str, Any]:
    """Follow the slide ('slide') or the fact ('fact'); empty takes it back."""
    try:
        return fact_ledger.decide(slug, claim_id, str(data.get("decision", "")))
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@post("/api/projects/{slug:str}/facts/build")
async def build_facts(slug: FromPath[str]) -> dict[str, Any]:
    """Take the deck's claims out and check them (from the cache when this deck was
    checked before)."""
    return await _in_thread(fact_ledger.build, slug)


@post("/api/projects/{slug:str}/facts/apply")
async def apply_facts(slug: FromPath[str]) -> dict[str, Any]:
    """Draft again the sections that teach a decided fact."""
    return await _in_thread(fact_ledger.apply, slug)


FACT_ROUTES = [get_facts, decide_fact, build_facts, apply_facts]
