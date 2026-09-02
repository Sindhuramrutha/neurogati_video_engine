ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # helper: parametric waveform
        # ------------------------------------------------------------
        def make_wave(func, color, stroke_width, use_smoothing=False):
            return ParametricFunction(
                lambda t: np.array([t, func(t), 0]),
                t_range=[0, 4.0, 0.004],
                color=color,
                stroke_width=stroke_width,
                use_smoothing=use_smoothing,
            )

        def raw_func(t):
            base = 0.35 * np.sin(2 * np.pi * 1.0 * t + 0.4)
            rough = 0.12 * np.sin(2 * np.pi * 6.0 * t)
            rough2 = 0.05 * np.sin(2 * np.pi * 19 * t)
            spike1 = 0.45 * np.exp(-((t - 0.80) / 0.03) ** 2)
            spike2 = -0.50 * np.exp(-((t - 1.90) / 0.03) ** 2)
            spike3 = 0.55 * np.exp(-((t - 3.10) / 0.03) ** 2)
            return base + rough + rough2 + spike1 + spike2 + spike3

        def clean_func(t):
            return 0.38 * np.sin(2 * np.pi * 1.0 * t + 0.4) + 0.06 * np.sin(2 * np.pi * 2.0 * t)

        # ------------------------------------------------------------
        # previous scene's balanced scale visual
        # ------------------------------------------------------------
        prev_pivot = Dot(ORIGIN, radius=0.07, color=GREY_B, fill_opacity=1)
        prev_stand = Line(ORIGIN, DOWN * 1.2, color=GREY_B, stroke_width=6)
        prev_base = Line(LEFT * 0.4 + DOWN * 1.2, RIGHT * 0.4 + DOWN * 1.2, color=GREY_B, stroke_width=10)
        prev_beam = Line(LEFT * 2.6, RIGHT * 2.6, color=GREY_B, stroke_width=7)
        prev_left_support = Line(LEFT * 2.6, LEFT * 2.6 + DOWN * 0.35, color=GREY_B, stroke_width=3)
        prev_right_support = Line(RIGHT * 2.6, RIGHT * 2.6 + DOWN * 0.35, color=GREY_B, stroke_width=3)
        prev_left_pan = Arc(
            radius=0.35,
            start_angle=PI,
            angle=PI,
            arc_center=LEFT * 2.6 + DOWN * 0.35,
            color=GREY_B,
            stroke_width=3,
        )
        prev_right_pan = Arc(
            radius=0.35,
            start_angle=0,
            angle=PI,
            arc_center=RIGHT * 2.6 + DOWN * 0.35,
            color=GREY_B,
            stroke_width=3,
        )
        prev_label = Text("Appropriate filter", font_size=32, color=BLUE, weight="BOLD")
        prev_label.move_to(UP * 0.8)

        prev_scale = VGroup(
            prev_stand,
            prev_base,
            prev_pivot,
            prev_beam,
            prev_left_support,
            prev_right_support,
            prev_left_pan,
            prev_right_pan,
            prev_label,
        )
        prev_scale.move_to(ORIGIN)
        self.add(prev_scale)

        # ------------------------------------------------------------
        # clean empty summary canvas
        # ------------------------------------------------------------
        canvas = Rectangle(
            width=14.2,
            height=8.2,
            fill_color=WHITE,
            fill_opacity=0.07,
            stroke_width=0,
        )

        # ------------------------------------------------------------
        # exact beat durations / gaps
        # ------------------------------------------------------------
        d1 = 1.26
        d2 = 2.18
        gap2 = 0.80
        d3 = 6.90
        gap4 = 0.84
        d4 = 7.30
        gap5 = 1.08
        d5 = 7.14
        gap6 = 0.82
        d6 = 2.92
        gap7 = 0.68
        d7 = 5.38
        gap8 = 0.80
        d8 = 5.70
        gap9 = 0.64
        d9 = 1.81

        # ------------------------------------------------------------
        # beat 1: previous scale fades out, summary canvas fades in
        # ------------------------------------------------------------
        self.play(
            FadeOut(prev_scale),
            FadeIn(canvas),
            run_time=max(0.05, d1),
        )

        # ------------------------------------------------------------
        # build left raw signal
        # ------------------------------------------------------------
        raw_wave = make_wave(raw_func, ORANGE, stroke_width=3, use_smoothing=False)
        raw_wave.scale_to_fit_width(3.0)
        raw_wave.move_to(LEFT * 4.2 + UP * 1.0)

        raw_label = Text("Raw signal", font_size=30, color=WHITE, weight="BOLD")
        raw_label.next_to(raw_wave, DOWN, buff=0.3)
        raw_group = VGroup(raw_wave, raw_label)

        # ------------------------------------------------------------
        # build center filtering arrow
        # ------------------------------------------------------------
        filter_arrow = Arrow(
            LEFT * 1.7,
            RIGHT * 1.7,
            color=YELLOW,
            stroke_width=9,
            buff=0,
            max_tip_length_to_length_ratio=0.22,
        )
        filter_arrow.move_to(UP * 1.0)

        filter_label = Text("Filtering", font_size=34, color=YELLOW, weight="BOLD")
        filter_label.next_to(filter_arrow, UP, buff=0.35)
        arrow_group = VGroup(filter_arrow, filter_label)

        # ------------------------------------------------------------
        # build right clean signal
        # ------------------------------------------------------------
        clean_wave = make_wave(clean_func, TEAL, stroke_width=4, use_smoothing=True)
        clean_wave.scale_to_fit_width(3.0)
        clean_wave.move_to(RIGHT * 4.2 + UP * 1.0)

        clean_label = Text("Clean signal", font_size=30, color=WHITE, weight="BOLD")
        clean_label.next_to(clean_wave, DOWN, buff=0.3)
        clean_group = VGroup(clean_wave, clean_label)

        flow_group = VGroup(raw_group, arrow_group, clean_group)

        # ------------------------------------------------------------
        # beat 2: raw signal draws itself
        # ------------------------------------------------------------
        self.play(
            Create(raw_wave),
            Write(raw_label),
            run_time=max(0.05, d2),
        )
        self.wait(max(0.05, gap2))

        # ------------------------------------------------------------
        # beat 3: filtering arrow and clean signal appear
        # ------------------------------------------------------------
        self.play(Create(filter_arrow), Write(filter_label), run_time=max(0.05, 2.2))
        self.play(Create(clean_wave), Write(clean_label), run_time=max(0.05, 2.5))
        self.wait(max(0.05, d3 - 4.7))
        self.wait(max(0.05, gap4))

        # ------------------------------------------------------------
        # checklist helpers
        # ------------------------------------------------------------
        def make_checkbox_point(label_text):
            box = Square(
                side_length=0.34,
                color=GREEN,
                stroke_width=3,
                fill_color=GREEN,
                fill_opacity=0.12,
            )
            check = VGroup(
                Line(
                    box.get_corner(DL) + np.array([0.07, 0.08, 0]),
                    box.get_center() + np.array([-0.02, 0.05, 0]),
                    color=GREEN,
                    stroke_width=5,
                ),
                Line(
                    box.get_center() + np.array([-0.02, 0.05, 0]),
                    box.get_corner(UR) + np.array([-0.03, -0.07, 0]),
                    color=GREEN,
                    stroke_width=5,
                ),
            )
            marker = VGroup(box, check)
            label = Text(label_text, font_size=30, color=WHITE)
            return VGroup(marker, label).arrange(RIGHT, buff=0.3)

        checkbox1 = make_checkbox_point("Reduces unwanted components.")
        checkbox1.next_to(flow_group, DOWN, buff=0.7)

        spike_props = [0.2, 0.475, 0.775]
        spike_highlights = VGroup(*[
            VGroup(
                Circle(radius=0.18, color=PINK, stroke_width=3)
                .set_fill(PINK, opacity=0.12)
                .move_to(raw_wave.point_from_proportion(p)),
                Dot(raw_wave.point_from_proportion(p), radius=0.07, color=PINK, fill_opacity=0.9),
            )
            for p in spike_props
        ])

        # ------------------------------------------------------------
        # beat 4: first checklist point + raw spike highlight
        # ------------------------------------------------------------
        self.play(
            FadeIn(checkbox1),
            FadeIn(spike_highlights),
            run_time=max(0.05, 2.5),
        )
        self.play(FadeOut(spike_highlights), run_time=max(0.05, 1.6))
        self.wait(max(0.05, d4 - 4.1))
        self.wait(max(0.05, gap5))

        # ------------------------------------------------------------
        # beat 5: second checklist point + clean signal highlight
        # ------------------------------------------------------------
        clean_highlight = SurroundingRectangle(
            clean_wave,
            color=TEAL,
            buff=0.2,
            stroke_width=5,
        )
        clean_highlight.set_fill(TEAL, opacity=0.15)

        checkbox2 = make_checkbox_point("Preserves relevant information.")
        checkbox2.next_to(checkbox1, DOWN, buff=0.4)

        self.play(
            FadeIn(checkbox2),
            FadeIn(clean_highlight),
            run_time=max(0.05, 2.5),
        )
        self.play(FadeOut(clean_highlight), run_time=max(0.05, 1.6))
        self.wait(max(0.05, d5 - 4.1))
        self.wait(max(0.05, gap6))

        # ------------------------------------------------------------
        # beat 6: entire summary slide shrinks and fades toward center
        # ------------------------------------------------------------
        summary_group = VGroup(
            canvas,
            raw_group,
            arrow_group,
            clean_group,
            checkbox1,
            checkbox2,
        )
        self.play(
            summary_group.animate.scale(0.04).move_to(ORIGIN).set_opacity(0),
            run_time=max(0.05, d6),
        )
        self.wait(max(0.05, gap7))

        # ------------------------------------------------------------
        # beat 7: large question mark + question text
        # ------------------------------------------------------------
        question_mark = Text("?", font_size=240, color=GOLD, weight="BOLD")
        question_mark.move_to(UP * 0.7)

        question_text = Text(
            "How does a filter decide what to keep?",
            font_size=40,
            color=WHITE,
            weight="BOLD",
        )
        question_text.scale_to_fit_width(10)
        question_text.next_to(question_mark, DOWN, buff=0.5)

        self.play(Write(question_mark), run_time=max(0.05, 2.0))
        self.play(FadeIn(question_text), run_time=max(0.05, 2.0))
        self.wait(max(0.05, d7 - 4.0))
        self.wait(max(0.05, gap8))

        # ------------------------------------------------------------
        # beat 8: question mark morphs into forward arrow
        # ------------------------------------------------------------
        next_arrow = Arrow(
            LEFT * 2.0,
            RIGHT * 2.0,
            color=GOLD,
            stroke_width=10,
            buff=0,
            max_tip_length_to_length_ratio=0.22,
        )
        next_arrow.move_to(UP * 0.7)

        next_label = Text(
            "Next: The Low-pass Filter.",
            font_size=40,
            color=WHITE,
            t2c={"Low-pass Filter": GOLD},
        )
        next_label.next_to(next_arrow, DOWN, buff=0.6)

        self.play(
            ReplacementTransform(question_mark, next_arrow),
            FadeOut(question_text),
            run_time=max(0.05, 3.0),
        )
        self.play(FadeIn(next_label), run_time=max(0.05, 2.7))
        self.wait(max(0.05, gap9))

        # ------------------------------------------------------------
        # beat 9: final hold
        # ------------------------------------------------------------
        self.wait(max(0.05, d9))