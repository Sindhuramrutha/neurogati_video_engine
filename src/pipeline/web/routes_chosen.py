"""The deck pictures a person chose for the video (`pipeline.chosen_pictures`).

Their own module so `routes_project.py` does not grow.
"""

from __future__ import annotations

from typing import Any

from litestar import get, put
from litestar.exceptions import ClientException
from litestar.params import FromPath
from pydantic import BaseModel

from pipeline import chosen_pictures
from pipeline.core import OperationFailed


class Pick(BaseModel):
    asset_path: str
    name: str = ""
    keep: bool = True


@get("/api/projects/{slug:str}/chosen-pictures", sync_to_thread=False)
def get_chosen_pictures(slug: FromPath[str]) -> dict[str, Any]:
    """The deck pictures chosen for the video, each with its name, and how many may be."""
    try:
        return chosen_pictures.view(slug)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


@put("/api/projects/{slug:str}/chosen-pictures", sync_to_thread=False)
def choose_picture(slug: FromPath[str], data: Pick) -> dict[str, Any]:
    """Choose a deck picture for the video, named -- or, `keep` false, let it go."""
    try:
        return chosen_pictures.choose(slug, data.asset_path, data.name, data.keep)
    except OperationFailed as failure:
        raise ClientException(detail=str(failure)) from failure


CHOSEN_ROUTES = [get_chosen_pictures, choose_picture]
