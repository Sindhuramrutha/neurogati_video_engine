"""The program written from a scene's shots reads like code a person wrote."""

import ast

from pipeline.program_layout import WIDTH, _laid_out


def test_a_long_call_is_broken_one_argument_per_line_and_still_says_the_same():
    line = ("self.compare(('cognitive complexity', None, ['thought is segmented', "
            "'divided into parts'], 'cognitive'), ('technological integration', None, "
            "['robotics', 'AI model neural functions'], 'robots'), "
            "title='The two ideas', cue=None)")
    written = _laid_out(line, 8)
    assert len(written.splitlines()) > 3
    assert all(len(row) <= WIDTH for row in written.splitlines())
    assert ast.dump(ast.parse(written.strip())) == ast.dump(ast.parse(line))


def test_short_lines_and_comments_are_left_alone():
    assert _laid_out("self.clear()", 8) == "        self.clear()"
    assert _laid_out("# Shot 2: hero", 8) == "        # Shot 2: hero"


def test_the_program_names_its_pictures_and_waits_for_seconds_and_places():
    """Everything about where and when is in the file: the pictures it shows by
    file, each moment as the second its words are spoken, and -- after a render --
    the place the kit chose for each part."""
    from pipeline.scene_shots import Pictures
    from pipeline.shot_program import program_for
    from pipeline.shot_values import Timing

    words = tuple({"text": w, "start_ms": 1000 * i} for i, w in enumerate(
        "the brain sits in the skull and the cortex covers it".split()))
    timing = Timing(words, " ".join(w["text"] for w in words), 30.0)
    pictures = Pictures(1, {0: [{"name": "cortex", "box": [0.2, 0.1, 0.8, 0.5], "sure": True}]},
                        files=("illustration-1.png",), about=("a brain in a skull",))
    spec = {"shots": [
        {"template": "hero", "picture": 0, "title": "The brain",
         "callouts": [{"label": "Cortex", "part": "cortex", "when": "the cortex"}]},
        {"template": "key_idea", "statement": "The cortex covers the brain",
         "when": "covers it"}]}
    layouts = [{"call": "hero", "layout": {"picture": [0.0, -0.2, 9.5], "tag: Cortex": [4.1, 1]}},
               {"call": "key_idea", "layout": {"card": [0, 0.3]}}]

    program = program_for(spec, pictures, timing, layouts)

    assert "PICTURE_1 = 'illustration-1.png'  # a brain in a skull" in program
    assert "self.hero(\n            PICTURE_1," in program
    assert "at=7.0" in program, "the cortex is said at 7 s"
    assert "self.until(9.0)" in program and "cue=9.0" in program
    assert "'picture': (0, -0.2, 9.5)" in program and "'tag: Cortex': (4.1, 1)" in program
    assert '7.00 s  tag "Cortex"' in program
    compile(program, "scene.py", "exec")
