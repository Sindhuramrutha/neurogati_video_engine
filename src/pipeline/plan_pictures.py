"""Each section's pictures, and the assets every later layer reads -- through the plan.

The work flows one way: Extraction → Assets & Design → Scene Plan → Script →
Generation → Render. Assets & Design decides which pictures exist and how they
look, with the brand kit and the look; the plan decides which section shows
which picture, and carries all of it on. No later layer reads Assets & Design
directly: the script is written knowing a section's pictures, the shots show
exactly those pictures, and the render draws the look and the brand kit the plan
carried. Re-transfer Assets & Design and the plan is flagged, and through it
everything after.

By rule, a section has every picture from its own slides (or under its own
headings) that is large and clear enough to fill a frame. A person may attach or
detach pictures; the section then keeps that choice (`pictures_chosen`) until
they hand it back to the rule. A picture that is no longer handed on drops out
either way. All of it is deterministic: the same transfers give the same
pictures.
"""

from __future__ import annotations

from typing import Any

from pipeline.assets import AssetLibrary, LibraryFigure
from pipeline.assets_handoff import (
    ConfirmedAssets,
    ConfirmedAssetStore,
    brand_for_later_stages,
    confirmed_library,
)
from pipeline.core import OperationFailed, require_project
from pipeline.planning import Plan, PlanSection, PlanStore, SourceReference


def transferred_assets(project) -> ConfirmedAssets:
    """What Assets & Design last transferred. A project from before transfers is
    taken as transferred once, as it stands (`confirmed_library`)."""
    library = confirmed_library(project)
    confirmed = ConfirmedAssetStore(project.root).load()
    if confirmed.confirmed_at:
        return confirmed
    return ConfirmedAssets(library=library, brand=brand_for_later_stages(project))


def assets_for_later_stages(project) -> ConfirmedAssets:
    """The pictures, brand kit and look every layer after Scene Plan uses: the
    ones the transferred plan carried. Before a plan carried any (it was never
    transferred, or was transferred before plans did), the transferred assets."""
    from pipeline.plan_handoff import TransferredPlanStore

    transferred = TransferredPlanStore(project.root).load()
    if transferred.transferred_at and transferred.assets is not None:
        return transferred.assets
    return transferred_assets(project)


# --- which picture belongs to which section ----------------------------------------------


def _belongs(figure: LibraryFigure, reference: SourceReference) -> bool:
    if reference.slide_number and figure.slide_number:
        return figure.slide_number == reference.slide_number
    # A picture gathered before pictures recorded their slide: its heading is
    # the slide's title, which is where it is.
    # A heading path is a location: a picture under a deeper heading is inside
    # the section, one above it is not.
    heading = list(reference.heading_path)
    return figure.heading_path[:len(heading)] == heading


def by_rule(section: PlanSection, library: AssetLibrary) -> list[str]:
    """The pictures the rule gives a section, in the source's order."""
    return [figure.asset_path for figure in library.usable()
            if any(_belongs(figure, reference) for reference in section.sources)]


def pictures_of(section: PlanSection, plan: Plan, library: AssetLibrary) -> list[LibraryFigure]:
    """The pictures a section shows. A plan that has not had pictures attached
    (from before plans carried them) gets the rule's."""
    usable = {figure.asset_path: figure for figure in library.usable()}
    paths = section.picture_paths if plan.pictures_from else by_rule(section, library)
    return [usable[path] for path in paths if path in usable]


def attach_pictures(project, plan: Plan) -> Plan:
    """Give every section its pictures from the transferred assets. Run on every
    save, so a plan is always attached to the latest transfer."""
    confirmed = ConfirmedAssetStore(project.root).load()
    if not confirmed.confirmed_at:
        return plan            # nothing handed on yet; a person's choices are kept
    library = confirmed.library
    usable = [figure.asset_path for figure in library.usable()]
    for section in plan.sections:
        if section.pictures_chosen:
            # Kept as chosen, in the source's order, without what is gone.
            section.picture_paths = [p for p in usable if p in section.picture_paths]
        else:
            section.picture_paths = by_rule(section, library)
    plan.pictures_from = confirmed.confirmed_at
    return plan


def is_behind(project, plan: Plan) -> bool:
    """Whether Assets & Design was transferred since the plan's pictures were attached."""
    confirmed = ConfirmedAssetStore(project.root).load()
    return bool(confirmed.confirmed_at) and plan.pictures_from != confirmed.confirmed_at


# --- what a person does --------------------------------------------------------------------


def choose_section_pictures(slug: str, section_id: str, paths: list[str] | None) -> Plan:
    """Attach exactly `paths` to a section, or -- with None -- hand it back to the rule."""
    from pipeline.lesson_plan import save_plan

    project = require_project(slug)
    plan = PlanStore(project.root).load()
    section = next((s for s in plan.sections if s.id == section_id), None)
    if section is None:
        raise OperationFailed("That section is not in the plan any more. Reload the page.")
    if paths is None:
        section.pictures_chosen = False
    else:
        confirmed = ConfirmedAssetStore(project.root).load()
        if not confirmed.confirmed_at:
            raise OperationFailed("Assets & Design has not been transferred, so there are "
                                  "no pictures to attach yet.")
        library = confirmed.library
        usable = {figure.asset_path for figure in library.usable()}
        named = {figure.asset_path: figure.name for figure in library.handed_on()}
        refused = [named.get(path, path) for path in paths if path not in usable]
        if refused:
            raise OperationFailed(
                "Only a picture that can fill a frame can be attached; these cannot: "
                + ", ".join(refused) + ".")
        section.pictures_chosen = True
        section.picture_paths = list(dict.fromkeys(paths))
    return save_plan(project, plan)


# --- what the page shows -------------------------------------------------------------------


def pictures_view(project, plan: Plan) -> dict[str, Any]:
    """The pictures that can be attached, and each section's rule, for the page."""
    confirmed = ConfirmedAssetStore(project.root).load()
    library = confirmed.library
    usable = {figure.asset_path for figure in library.usable()}
    return {
        "has_assets": bool(confirmed.confirmed_at),
        "transferred_at": confirmed.confirmed_at,
        "offered": [{
            "path": figure.asset_path, "shown_path": figure.shown_path,
            "name": figure.name, "caption": figure.caption,
            "slide_number": figure.slide_number,
            "can_attach": figure.asset_path in usable,
            "why_not": "" if figure.asset_path in usable else figure.why_not_a_frame,
        } for figure in library.handed_on()],
        "by_rule": {section.id: by_rule(section, library) for section in plan.sections},
    }
