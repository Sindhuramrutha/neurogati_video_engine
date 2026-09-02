ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def brain_y(x):
            return 0.28 * np.sin(2.2 * x) + 0.12 * np.sin(5.0 * x + 1.0) + 0.06 * np.sin(9.0 * x)

        def pulse_y(t, amp):
            return amp * np.exp(-0.5 * (t / 0.22) ** 2)

        def make_noise_curve(color, y_offset, seed):
            def f(t, seed=seed):
                y = (0.85 + 0.25 * np.sin(seed * 3)) * np.sin(2.1 * t + seed)
                y += 0.6 * np.sin(5.1 * t + seed * 2 + 1.0)
                y += 0.32 * np.sin(10.3 * t + seed * 3 + 0.4)
                centers = [-1.2, 0.0, 1.3]
                amps = [1.8, -2.0, 1.5]
                widths = [0.22, 0.26, 0.20]
                for c, a, w in zip(centers, amps, widths):
                    y += a * np.exp(-((t - c) / w) ** 2)
                return y

            return ParametricFunction(
                lambda t: np.array([t, y_offset + f(t), 0]),
                t_range=[-2.2, 2.2, 0.02],
                color=color,
                stroke_width=5,
            )

        # ---------- beat 1 starting setup ----------
        clean_trace_full = ParametricFunction(
            lambda t: np.array([t, 1.8 * brain_y(t), 0]),
            t_range=[-5.0, 5.0, 0.01],
            color=TEAL,
            stroke_width=7,
        )
        preserved_label = Text("Preserved signal", color=TEAL, font_size=30).next_to(clean_trace_full, DOWN, buff=0.5)
        def_text = Text(
            "Signal filtering = preserving useful signal components while attenuating unwanted components.",
            color=WHITE,
            font_size=28,
        ).scale_to_fit_width(10).to_edge(DOWN, buff=0.4)

        bin_rect = Rectangle(width=2.0, height=1.4, color=GREY, fill_color=BLACK, fill_opacity=0.4, stroke_width=1.5)
        bin_text = Text("Removed", font_size=24, color=GREY).move_to(bin_rect.get_center())
        removed_bin = VGroup(bin_rect, bin_text).move_to(RIGHT * 4.5 + DOWN * 1.0)

        self.add(clean_trace_full, preserved_label, def_text, removed_bin)

        # Small left trace target
        small_trace = ParametricFunction(
            lambda t: np.array([t, 0.16 * np.sin(2.0 * t) + 0.08 * np.sin(4.5 * t + 0.8), 0]),
            t_range=[-1.8, 1.8, 0.01],
            color=TEAL,
            stroke_width=2.2,
        ).move_to(LEFT * 4.2 + UP * 0.5)
        small_label = Text("Neural signal — microvolts", color=WHITE, font_size=26).next_to(small_trace, DOWN, buff=0.35)

        # Beat 1: 0.00-2.72
        self.play(
            FadeOut(def_text),
            FadeOut(removed_bin),
            FadeOut(preserved_label),
            Transform(clean_trace_full, small_trace),
            FadeIn(small_label),
            run_time=max(0.05, 2.72),
        )

        # gap to beat 2
        self.wait(max(0.05, 0.96))

        # Beat 2: 3.68-6.56
        d1 = make_noise_curve(ORANGE, 0.2, 0.0)
        d2 = make_noise_curve(RED, -0.6, 1.3)
        d3 = make_noise_curve(YELLOW, 0.8, 2.1)
        disturbances = VGroup(d1, d2, d3).scale_to_fit_height(4.4).move_to(RIGHT * 3.1 + UP * 0.2)
        disturbance_label = Text("Disturbances", color=RED, font_size=40).next_to(disturbances, UP, buff=0.3)

        self.play(FadeIn(disturbances), FadeIn(disturbance_label), run_time=max(0.05, 2.88))

        # gap to beat 3
        self.wait(max(0.05, 0.58))

        # Beat 3: 7.14-10.02
        self.play(
            Wiggle(small_trace, scale_value=0.03),
            Wiggle(disturbances, scale_value=0.05),
            run_time=max(0.05, 2.88),
        )

        # gap to beat 4
        self.wait(max(0.05, 0.76))

        # Beat 4: 10.78-13.88
        dist_pulse = ParametricFunction(
            lambda t: np.array([t, pulse_y(t, 1.1), 0]),
            t_range=[-0.8, 0.8, 0.01],
            color=YELLOW,
            stroke_width=8,
        ).move_to(d1.get_center() + DOWN * 1.0)
        neural_pulse = ParametricFunction(
            lambda t: np.array([t, pulse_y(t, 1.1), 0]),
            t_range=[-0.8, 0.8, 0.01],
            color=TEAL,
            stroke_width=8,
        ).set_opacity(0.75).move_to(small_trace.get_center() + DOWN * 1.0)

        self.play(d1.animate.set_color(YELLOW).set_stroke(width=8), run_time=max(0.05, 0.5))
        self.play(GrowFromCenter(dist_pulse), GrowFromCenter(neural_pulse), run_time=max(0.05, 0.8))
        self.play(
            dist_pulse.animate.move_to(UP * 0.4 + RIGHT * 0.3),
            neural_pulse.animate.move_to(UP * 0.4 + LEFT * 0.3),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 0.3))

        # Beat 5: 13.88-18.50
        self.play(dist_pulse.animate.stretch(3.2, dim=1), run_time=max(0.05, 3.2))
        self.wait(max(0.05, 1.42))

        # gap to beat 6
        self.wait(max(0.05, 1.04))

        # Beat 6: 19.54-21.62
        self.play(
            FadeOut(small_trace),
            FadeOut(small_label),
            FadeOut(disturbances),
            FadeOut(disturbance_label),
            FadeOut(dist_pulse),
            FadeOut(neural_pulse),
            run_time=max(0.05, 0.8),
        )

        title = Text("Common reasons for filtering", color=WHITE, font_size=48).to_edge(UP, buff=0.35)

        checkbox_labels = [
            "Remove baseline drift",
            "Reduce high-frequency noise",
            "Eliminate power-line interference",
            "Improve SNR",
            "Prepare signals for feature extraction",
        ]
        check_rows = []
        checkmarks = []
        for label_text in checkbox_labels:
            box = Square(side_length=0.4, color=GREY_B, stroke_width=3)
            label = Text(label_text, font_size=32, color=GREY_B)
            row = VGroup(box, label).arrange(RIGHT, buff=0.35, aligned_edge=LEFT)
            check = Text("✓", color=GREEN, font_size=30).move_to(box.get_center()).set_opacity(0)
            row.add(check)
            check_rows.append(row)
            checkmarks.append(check)
        checklist = VGroup(*check_rows).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        checklist.scale_to_fit_width(9).next_to(title, DOWN, buff=0.45)

        self.play(FadeIn(title), FadeIn(checklist), run_time=max(0.05, 1.28))

        # Beat 7: 21.62-24.04
        self.play(
            checkmarks[0].animate.set_opacity(1),
            check_rows[0][1].animate.set_color(WHITE),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 0.42))

        # gap to beat 8
        self.wait(max(0.05, 0.48))

        # Beat 8: 24.52-26.62
        self.play(
            checkmarks[1].animate.set_opacity(1),
            check_rows[1][1].animate.set_color(WHITE),
            run_time=max(0.05, 1.7),
        )
        self.wait(max(0.05, 0.40))

        # Beat 9: 26.62-28.70
        self.play(
            checkmarks[2].animate.set_opacity(1),
            check_rows[2][1].animate.set_color(WHITE),
            run_time=max(0.05, 1.6),
        )
        self.wait(max(0.05, 0.48))

        # gap to beat 10
        self.wait(max(0.05, 0.66))

        # Beat 10: 29.36-31.18
        self.play(
            checkmarks[3].animate.set_opacity(1),
            check_rows[3][1].animate.set_color(WHITE),
            run_time=max(0.05, 1.4),
        )
        self.wait(max(0.05, 0.42))

        # gap to beat 11
        self.wait(max(0.05, 0.48))

        # Beat 11: 31.66-34.52
        self.play(
            checkmarks[4].animate.set_opacity(1),
            check_rows[4][1].animate.set_color(WHITE),
            run_time=max(0.05, 2.2),
        )
        self.wait(max(0.05, 0.66))

        # gap to beat 12
        self.wait(max(0.05, 1.12))

        # Beat 12: 35.64-38.38
        raw_box = VGroup(
            Rectangle(width=2.7, height=1.0, color=BLUE, fill_color=BLUE, fill_opacity=0.2, stroke_width=3),
            Text("Raw signal", color=WHITE, font_size=26),
        )
        filt_box = VGroup(
            Rectangle(width=2.7, height=1.0, color=ORANGE, fill_color=ORANGE, fill_opacity=0.25, stroke_width=4),
            Text("Filtering", color=WHITE, font_size=26),
        )
        clean_box = VGroup(
            Rectangle(width=2.7, height=1.0, color=GREEN, fill_color=GREEN, fill_opacity=0.2, stroke_width=3),
            Text("Clean signal", color=WHITE, font_size=26),
        )
        analysis_box = VGroup(
            Rectangle(width=2.7, height=1.0, color=PURPLE, fill_color=PURPLE, fill_opacity=0.2, stroke_width=3),
            Text("Analysis", color=WHITE, font_size=26),
        )

        for box_group in (raw_box, filt_box, clean_box, analysis_box):
            box_group[1].move_to(box_group[0].get_center())

        boxes = VGroup(raw_box, filt_box, clean_box, analysis_box).arrange(RIGHT, buff=0.9)

        arrow1 = Arrow(start=raw_box.get_right(), end=filt_box.get_left(), buff=0.25, color=GREY_B, stroke_width=4)
        arrow2 = Arrow(start=filt_box.get_right(), end=clean_box.get_left(), buff=0.25, color=GREY_B, stroke_width=4)
        arrow3 = Arrow(start=clean_box.get_right(), end=analysis_box.get_left(), buff=0.25, color=GREY_B, stroke_width=4)

        pipeline = VGroup(raw_box, filt_box, clean_box, analysis_box, arrow1, arrow2, arrow3)
        pipeline.scale_to_fit_width(11).move_to(DOWN * 2.1)

        self.play(
            checklist.animate.scale(0.72).next_to(title, DOWN, buff=0.35),
            run_time=max(0.05, 1.0),
        )
        self.play(Write(pipeline), run_time=max(0.05, 1.74))

        # Beat 13: 38.38-41.76
        filter_glow = SurroundingRectangle(filt_box, color=ORANGE, buff=0.12, stroke_width=5)
        filter_glow.set_fill(ORANGE, opacity=0.12)

        self.play(
            FadeIn(filter_glow),
            arrow1.animate.set_color(YELLOW).set_stroke(width=6),
            run_time=max(0.05, 0.9),
        )
        self.play(arrow2.animate.set_color(YELLOW).set_stroke(width=6), run_time=max(0.05, 0.8))
        self.play(arrow3.animate.set_color(YELLOW).set_stroke(width=6), run_time=max(0.05, 0.8))
        self.play(Wiggle(filter_glow, scale_value=0.03), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.38))

        # Beat 14: 41.76-42.58
        self.wait(max(0.05, 0.82))