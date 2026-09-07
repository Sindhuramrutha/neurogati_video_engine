ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Title
        title = Text("High-Pass Filter", font_size=54, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.55)

        # Empty rounded-rectangle text box
        box = RoundedRectangle(
            corner_radius=0.25,
            width=11.5,
            height=4.8,
            stroke_color=GREY_B,
            stroke_width=2.0,
            stroke_opacity=0.45,
        )
        box.next_to(title, DOWN, buff=0.55)

        # Helper to build an invisible word-by-word line
        def make_words(data, font_size=28):
            words = []
            for word_text, color in data:
                word = Text(
                    word_text,
                    font_size=font_size,
                    color=color,
                    weight=BOLD if color == YELLOW else NORMAL,
                )
                word.set_opacity(0)
                words.append(word)
            line = VGroup(*words).arrange(RIGHT, buff=0.18)
            if line.width > box.width - 1.2:
                line.scale_to_fit_width(box.width - 1.2)
            return line, words

        # Definition lines
        line1_data = [
            ("A", WHITE),
            ("filter", WHITE),
            ("that", WHITE),
            ("allows", WHITE),
            ("high-frequency", YELLOW),
            ("components", YELLOW),
            ("of", WHITE),
            ("a", WHITE),
            ("signal", WHITE),
            ("to", WHITE),
            ("pass", WHITE),
        ]
        line2_data = [
            ("while", WHITE),
            ("attenuating", WHITE),
            ("or", WHITE),
            ("removing", WHITE),
            ("low-frequency", YELLOW),
            ("components", YELLOW),
        ]
        line3_data = [
            ("below", WHITE),
            ("a", WHITE),
            ("selected", WHITE),
            ("cutoff", WHITE),
            ("frequency.", WHITE),
        ]

        line1, line1_words = make_words(line1_data)
        line2, line2_words = make_words(line2_data)
        line3, line3_words = make_words(line3_data)

        # Position lines inside the box, left-aligned
        margin_left = 0.6
        top_margin = 0.7
        line_spacing = 0.65

        line1.move_to(np.array([
            box.get_left()[0] + margin_left + line1.width / 2,
            box.get_top()[1] - top_margin - line1.height / 2,
            0,
        ]))
        line2.align_to(line1, LEFT)
        line2.next_to(line1, DOWN, buff=line_spacing)
        line3.align_to(line2, LEFT)
        line3.next_to(line2, DOWN, buff=line_spacing)

        # Add invisible lines so their words can be faded in later
        self.add(line1, line2, line3)

        # Beat 1: 0.00-1.72 — title fades in, empty box drawn lightly
        self.play(FadeIn(title), Create(box), run_time=max(0.05, 1.72))

        # Gap: 1.72-2.86
        self.wait(max(0.05, 1.14))

        # Beat 2: 2.86-4.54 — first line fades in word by word
        per_word_1 = 1.68 / len(line1_words)
        for word in line1_words:
            self.play(word.animate.set_opacity(1), run_time=max(0.05, per_word_1))

        # Beat 3: 4.54-6.52 — green up-arrow fades in beside high-frequency phrase, pulses twice
        phrase1_left = line1_words[4].get_left()[0]
        phrase1_right = line1_words[5].get_right()[0]
        phrase1_top = max(line1_words[4].get_top()[1], line1_words[5].get_top()[1])

        up_arrow = Arrow(
            start=np.array([0, -0.28, 0]),
            end=np.array([0, 0.28, 0]),
            color=GREEN,
            stroke_width=6,
            buff=0,
        ).move_to(np.array([(phrase1_left + phrase1_right) / 2, phrase1_top + 0.45, 0]))

        self.play(FadeIn(up_arrow), run_time=max(0.05, 0.42))
        self.play(up_arrow.animate.scale(1.2), run_time=max(0.05, 0.39))
        self.play(up_arrow.animate.scale(1 / 1.2), run_time=max(0.05, 0.39))
        self.play(up_arrow.animate.scale(1.2), run_time=max(0.05, 0.39))
        self.play(up_arrow.animate.scale(1 / 1.2), run_time=max(0.05, 0.39))

        # Beat 4: 6.52-8.54 — arrow steady, first line holds
        self.wait(max(0.05, 2.02))

        # Gap: 8.54-9.10
        self.wait(max(0.05, 0.56))

        # Beat 5: 9.10-11.24 — second line word by word + red down-arrow pulses twice
        # Position the red arrow relative to the low-frequency phrase
        phrase2_left = line2_words[4].get_left()[0]
        phrase2_right = line2_words[5].get_right()[0]
        phrase2_bottom = min(line2_words[4].get_bottom()[1], line2_words[5].get_bottom()[1])

        down_arrow = Arrow(
            start=np.array([0, 0.28, 0]),
            end=np.array([0, -0.28, 0]),
            color=RED,
            stroke_width=6,
            buff=0,
        ).move_to(np.array([(phrase2_left + phrase2_right) / 2, phrase2_bottom - 0.45, 0]))

        # First four words
        for word in line2_words[:4]:
            self.play(word.animate.set_opacity(1), run_time=max(0.05, 0.18))

        # Low-frequency
        self.play(line2_words[4].animate.set_opacity(1), run_time=max(0.05, 0.22))

        # Components + red arrow appears
        self.play(
            line2_words[5].animate.set_opacity(1),
            FadeIn(down_arrow),
            run_time=max(0.05, 0.30),
        )

        # Red arrow pulses subtly two times
        self.play(down_arrow.animate.scale(1.2), run_time=max(0.05, 0.225))
        self.play(down_arrow.animate.scale(1 / 1.2), run_time=max(0.05, 0.225))
        self.play(down_arrow.animate.scale(1.2), run_time=max(0.05, 0.225))
        self.play(down_arrow.animate.scale(1 / 1.2), run_time=max(0.05, 0.225))

        # Beat 6: 11.24-13.84 — third line types out, no arrow
        per_word_3 = 2.60 / len(line3_words)
        for word in line3_words:
            self.play(word.animate.set_opacity(1), run_time=max(0.05, per_word_3))

        # Beat 7: 13.84-15.18 — border around the text box fades in completely
        self.play(
            box.animate.set_stroke(color=WHITE, width=2.5, opacity=1.0),
            run_time=max(0.05, 1.34),
        )