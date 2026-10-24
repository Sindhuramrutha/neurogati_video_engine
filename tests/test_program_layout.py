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
