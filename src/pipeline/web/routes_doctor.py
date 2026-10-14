"""`GET /api/doctor`: is this machine ready for a job? The work is in `pipeline.doctor`."""

from __future__ import annotations

from typing import Any

from litestar import get

from pipeline.operations import check_readiness


@get("/api/doctor")
async def doctor(deep: bool = False) -> dict[str, Any]:
    """The quick checks, or with `deep=1` also one call to each service (slow, and
    the model calls are paid). Run in a thread: the deep checks take seconds."""
    import anyio

    return await anyio.to_thread.run_sync(check_readiness, deep)


DOCTOR_ROUTES = [doctor]
