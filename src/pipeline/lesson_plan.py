"""Saving a plan, and what a section with no slides is written from.

There are no fixed kinds of section. The planning agent says, in its own words,
how each section is told (`PlanSection.how`). A section that covers no slides --
an opening, a recap, a close, or anything else the video needs -- is written
from the rest of the plan, and from what the other sections actually said.
"""

from __future__ import annotations

from pipeline.planning import Plan, PlanSection


def shape_plan(project, plan: Plan) -> Plan:
    """The pictures, attached again. Deterministic: run on every save."""
    from pipeline.plan_pictures import attach_pictures

    attach_pictures(project, plan)
    return plan


def save_plan(project, plan: Plan) -> Plan:
    from pipeline.planning import PlanStore

    return PlanStore(project.root).save(shape_plan(project, plan))


def plan_source(plan: Plan, script, section: PlanSection) -> str:
    """What a section with no slides is written from: the other sections, and --
    once they are written -- what they said."""
    lines = ["The video's other sections, in order:"]
    for other in plan.sections:
        if other.id == section.id:
            lines.append(f"- (this section) {other.title}")
            continue
        lines.append(f"- {other.title}: {other.summary}")
        if script is not None:
            spoken = script.spoken_text(other.id).strip()
            if spoken:
                lines.append(f"  What it said: {spoken[:600]}")
    return "\n".join(lines)
