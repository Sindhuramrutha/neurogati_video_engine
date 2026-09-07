"""Audio-Visual Scene Script agent: turns textbook content into spoken scenes.

The LLM decides scene boundaries, writes the actual spoken narration
(adapting the textbook-style detailed script into something meant to
be heard, not read), the animation for each scene, and which renderer
it needs. It makes no rendering decisions itself — that happens in the
Visual branch, which dispatches each scene to its chosen renderer
(Manim or Matplotlib, for now).
"""

import json

from state import Scene, VideoState
from utils.llm import generate
from utils.notify import notify
from utils.revision import build_revision_prompt


SYSTEM_PROMPT = """You are an expert video director for STEM educational videos, in the style \
of 3Blue1Brown.

You are given the detailed content for this video, written as textbook prose (sections, \
subsections, equations, worked examples). Break it into a sequence of short scenes.

Fidelity to the source — the single most important rule, above pacing, engagement, or scene \
count:
- Every fact, number, equation, example, and claim in the narration must be traceable to the \
detailed content given to you. Do not invent additional facts, statistics, historical \
anecdotes, "fun" trivia, or analogies that are not in the source, no matter how plausible or \
pedagogically appealing they sound.
- Do not add unscientific claims, folk explanations, or narrative flourishes to make a scene \
sound more engaging. Accuracy and grounding in the source always outrank color or storytelling.
- If the source material for a subtopic is thin, write a short scene rather than padding it \
with invented content.
- Not inventing content is different from compressing it — by default, do not summarize the \
source down. If the source explains why something is true, works through an example, gives an \
aside, or adds a nuance, narrate all of that in full, in natural spoken words.
- Adapting to spoken style means changing phrasing and pacing, not shortening or skipping \
explanation that's already there.

For each scene, decide:
- The spoken narration for that scene: rephrase the textbook content into natural spoken \
English — conversational, paced for listening, rather than read verbatim off the page — while \
preserving its full depth.
- A concrete description of the animation: what is drawn, what moves, what appears or \
disappears, in enough detail that a programmer could implement it.
- The scene type:
  - "manim": stylized or constructed scenes — equations, diagrams, geometric constructions, \
code walkthroughs, or physical systems in motion.
  - "matplotlib": real computed data rendered as an actual plot — numeric time series, \
waveforms, histograms, scientific charts, or computed curves.
  - "image_only": only for genuinely brief moments where a static visual is acceptable.
  - "audio_only": only for genuinely brief transitions or pure exposition.

Prefer "manim" or "matplotlib" when meaningful animation is needed.

Critical rule for "manim" scenes:
- Depict concepts concretely, not just abstractly.
- If the content describes a physical system, show the physical object in motion.
- The animation must track what the narration is saying at each moment.
- Describe the visual sequence scene by scene and beat by beat.

Scenes should be short, roughly 15-45 seconds of spoken narration each.
Cover the entire content with no gaps and no overlaps, in order.

Respond with ONLY a JSON array, no markdown fences, no commentary, in this exact shape:
[
  {"subtopic": "...", "narration": "...", "animation_description": "...", "scene_type": "manim"},
  ...
]
"""


def _base_prompt(state: VideoState) -> str:
    return (
        f"Topic: {state.topic}\n"
        f"Audience: {state.audience}\n"
        f"Target total duration: approximately {state.duration_minutes} minutes across all "
        f"scenes combined — use this to guide how many scenes you produce and how much each "
        f"covers, not as a per-scene figure.\n\n"
        f"Detailed content:\n{state.detailed_script}\n"
    )


# ---------------------------------------------------------------------------
# PREVIOUS VERSION
# Kept here as comments for reference.
# ---------------------------------------------------------------------------

# def _parse_scenes(raw: str) -> list[Scene]:
#     data = json.loads(raw)
#     return [
#         Scene(
#             id=i,
#             subtopic=item["subtopic"],
#             narration=item["narration"],
#             animation_description=item["animation_description"],
#             scene_type=item["scene_type"],
#         )
#         for i, item in enumerate(data)
#     ]


# ---------------------------------------------------------------------------
# NEW VERSION
# Handles empty/None responses and validates that the LLM returned
# the expected JSON array.
# ---------------------------------------------------------------------------

def _parse_scenes(raw: str) -> list[Scene]:
    if not raw:
        raise ValueError("LLM returned an empty response")

    data = json.loads(raw)

    if not isinstance(data, list):
        raise ValueError("LLM response is not a JSON array")

    return [
        Scene(
            id=i,
            subtopic=item["subtopic"],
            narration=item["narration"],
            animation_description=item["animation_description"],
            scene_type=item["scene_type"],
        )
        for i, item in enumerate(data)
    ]


MAX_JSON_ATTEMPTS = 3


# ---------------------------------------------------------------------------
# PREVIOUS VERSION
# Kept here as comments for reference.
# ---------------------------------------------------------------------------

# def _generate_scenes(system: str, prompt: str) -> list[Scene]:
#     # Long, technical outputs occasionally slip on strict JSON syntax
#     # (a stray "=" instead of ": ", a dropped comma). Rare and stochastic —
#     # retrying the same call is far more reliable than trying to
#     # string-patch malformed JSON.
#     last_error = None
#     for _ in range(MAX_JSON_ATTEMPTS):
#         raw = generate(system=system, prompt=prompt, max_tokens=8192)
#         try:
#             return _parse_scenes(raw)
#         except (json.JSONDecodeError, KeyError) as exc:
#             last_error = exc
#     raise last_error


# ---------------------------------------------------------------------------
# NEW VERSION
# Handles None/empty responses and prints useful retry information.
# ---------------------------------------------------------------------------

def _generate_scenes(system: str, prompt: str) -> list[Scene]:
    last_error = None

    for attempt in range(1, MAX_JSON_ATTEMPTS + 1):
        try:
            raw = generate(
                system=system,
                prompt=prompt,
                max_tokens=8192,
            )

            print(
                f"  Scene-script LLM attempt {attempt}: "
                f"{len(raw) if raw else 0} characters returned"
            )

            return _parse_scenes(raw)

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            last_error = exc

            print(
                f"  Scene-script attempt "
                f"{attempt}/{MAX_JSON_ATTEMPTS} failed: "
                f"{type(exc).__name__}: {exc}"
            )

    raise last_error


def scene_script_node(state: VideoState) -> dict:
    scenes = _generate_scenes(
        SYSTEM_PROMPT,
        _base_prompt(state),
    )

    notify("Scene Script done — review the scenes")

    return {"scenes": scenes}


def revise_scenes(state: VideoState, instruction: str) -> dict:
    previous_output = json.dumps(
        [s.model_dump() for s in state.scenes]
    )

    prompt = build_revision_prompt(
        _base_prompt(state),
        previous_output,
        instruction,
    )

    scenes = _generate_scenes(
        SYSTEM_PROMPT,
        prompt,
    )

    return {"scenes": scenes}