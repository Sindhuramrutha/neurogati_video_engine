"""A deck's own slides, and which slide each planned scene refers to.

The plan is the planning agent's; its order and coverage are held by
`plan_order.py`. This reads the deck's slides (number, heading, text) and maps a
scene to the slide it was planned on, for the scene's reference image.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def slides_of(section) -> list[int]:
    numbers: list[int] = []
    for source in section.sources:
        if source.slide_number and source.slide_number not in numbers:
            numbers.append(source.slide_number)
    return numbers


def slide_for_scene(section, scene_index: int, scene_count: int) -> int:
    """Which slide a scene shows. A section of several slides moves through them
    in order as its scenes go, evenly."""
    numbers = slides_of(section)
    if not numbers:
        return 0
    if scene_count <= 0:
        return numbers[0]
    return numbers[min(len(numbers) - 1, scene_index * len(numbers) // scene_count)]


def scene_slide(section, scene_index: int, scene_count: int) -> int:
    """The slide a scene shows: the one the plan gave that scene, or else the
    section's slides in turn."""
    scenes = section.scenes
    if scene_index < len(scenes) and scenes[scene_index].slides:
        return scenes[scene_index].slides[0]
    return slide_for_scene(section, scene_index, scene_count)