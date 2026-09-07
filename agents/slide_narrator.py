"""Slide Narrator agent: writes spoken narration for a slide when the
professor didn't supply one.

Fidelity to the slide's own content is the whole point -- this narrates
what's already on the slide, it doesn't add outside facts, examples, or
embellishment the slide doesn't contain. Mirrors the same grounding
discipline agents/scene_script.py already enforces for chapter content.
"""

from utils.llm import generate
from utils.pptx_reader import SlideContent

SYSTEM_PROMPT = """You are narrating a single slide from a lecture deck, in a natural \
spoken voice a student would actually hear a professor use -- not reading bullet points \
verbatim, but speaking the content naturally.

Given the slide's own extracted text (in reading order) and any speaker notes, write 1-3 \
sentences of spoken narration that convey everything on the slide.

Rules:
- Narrate only what the slide actually says. Do not add outside facts, examples, statistics, \
or context the slide doesn't contain, even if it would be pedagogically nice to include.
- Never reuse the slide's own sentence structure or phrase order verbatim, even for a short, \
terse slide. Genuinely reword it -- combine short bullet fragments into full spoken sentences, \
add natural connective phrasing ("what this means is...", "in other words...", "so..."), and \
reorder ideas if that reads more naturally aloud, while keeping every fact intact and adding \
none. The test: if a listener followed along on the slide while hearing this, it should sound \
like a professor explaining the slide, not like the slide's text read aloud at them. A bullet \
list of short fragments narrated as the same short fragments back-to-back always fails this \
test -- turn it into connected spoken sentences instead.
- If speaker notes are present, they are the professor's own intended narration for this \
slide -- prefer them as the basis for what to say, adapted into natural spoken phrasing, \
rather than re-deriving narration purely from the bullet text.
- Cover the whole slide, not just the title -- if the slide has several bullets, a quote, or \
an attribution, work all of it into the narration.
- Do not describe the slide's layout or visuals ("this slide shows a diagram of..."). Speak \
the content itself, the way a professor would say the words, not describe the slide as an \
object.
- Exception: a direct quotation on the slide (in quotation marks, clearly attributed) should \
be spoken close to verbatim, since it's meant to be read aloud as a quote -- the "reword it" \
rule is for the slide's own bullets/prose, not for quoted material.

Respond with ONLY the narration text. No commentary, no markdown, no surrounding quotation \
marks.
"""


def _slide_text_block(slide: SlideContent) -> str:
    lines = [s.text for s in slide.shapes if s.text]
    return "\n".join(lines) if lines else "(no extractable text on this slide)"


def auto_narrate_slide(slide: SlideContent) -> str:
    prompt = f"Slide text (reading order):\n{_slide_text_block(slide)}"
    if slide.notes_text:
        prompt += f"\n\nSpeaker notes:\n{slide.notes_text}"
    return generate(system=SYSTEM_PROMPT, prompt=prompt, max_tokens=1024).strip()
