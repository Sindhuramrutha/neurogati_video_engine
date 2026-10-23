"""The deck pictures a person chose for the video: at most three, each named.

Every other picture in a video is made for it by the image model. The deck's own
pictures were offered to every scene, and a video built from them looked like its
slides -- cropped scraps, a book cover, a badge among them. Now a person picks the
two or three the video must show, on the Extraction page, and names each; nothing
else from the deck is handed on, and no other deck picture needs reviewing.

Kept beside the project (`chosen-pictures.json`), so a pick made before the asset
library is gathered still holds; written into the library as each is chosen, and
again whenever it is gathered.
"""

from __future__ import annotations

import json
from typing import Any

from pipeline.core import OperationFailed, require_project

CHOSEN_FILE = "chosen-pictures.json"
MOST_CHOSEN = 3


def chosen(project) -> dict[str, str]:
    """The chosen pictures, as asset path -> the name the person gave it."""
    return _read(project.root)


def _read(root) -> dict[str, str]:
    try:
        found = json.loads((root / CHOSEN_FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {str(k): str(v) for k, v in found.items()} if isinstance(found, dict) else {}


def view(slug: str) -> dict[str, Any]:
    picks = chosen(require_project(slug))
    return {"chosen": [{"asset_path": path, "name": name} for path, name in picks.items()],
            "most": MOST_CHOSEN}


def choose(slug: str, asset_path: str, name: str = "", keep: bool = True) -> dict[str, Any]:
    """Choose a deck picture for the video, with its name -- or, `keep` false, let it go."""
    from pipeline.extraction import BlockKind, ExtractionCollectionStore, ExtractionStore
    from pipeline.storage.documents import write_text_atomically

    project = require_project(slug)
    figures = {block.asset_path for store in (ExtractionCollectionStore, ExtractionStore)
               for document in store(project.root).load().documents
               for block in document.blocks
               if block.kind == BlockKind.FIGURE and block.asset_path}
    if asset_path not in figures:
        raise OperationFailed("That picture is not in this project's extraction.")
    picks = chosen(project)
    if keep:
        name = name.strip()[:80]
        if not name:
            raise OperationFailed("Give the picture a name: it is how the script and the "
                                  "scenes will know it.")
        if asset_path not in picks and len(picks) >= MOST_CHOSEN:
            raise OperationFailed(f"At most {MOST_CHOSEN} deck pictures are used; let one "
                                  "go first.")
        picks[asset_path] = name
    else:
        picks.pop(asset_path, None)
    write_text_atomically(project.root / CHOSEN_FILE, json.dumps(picks, ensure_ascii=False))
    apply_to_library(project)
    return view(slug)


def apply_to_library(project) -> None:
    """The library hands on the chosen pictures, named as the person named them."""
    from pipeline.assets import AssetLibraryStore

    store = AssetLibraryStore(project.root)
    library = store.load()
    if library.figures:
        store.save(mark(library, project.root))


def mark(library, root):
    """Each chosen picture marked Use, under its name; any other Use undone."""
    from pipeline.assets import FigureUse

    picks = _read(root)
    for figure in library.figures:
        if figure.asset_path in picks:
            figure.use, figure.note = FigureUse.USE, picks[figure.asset_path]
        elif figure.use == FigureUse.USE:
            figure.use, figure.note = FigureUse.UNDECIDED, ""
    return library
