ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Invisible time source for continuous signal drift.
        self.time_tracker = ValueTracker(0)
        self.add(self.time_tracker)

        # ------------------------------------------------------------
        # Beat 1: 0.00-2.88 -- low-pass filter block diagram at top.
        # ------------------------------------------------------------
        box = Rectangle(
            width=2.2,
            height=1.0,
            fill_color=BLUE,
            fill_opacity=0.25,
            stroke_color=BLUE,
            stroke_width=3,
        )
        box_label = Text("Low-pass", font_size=30, weight=BOLD, color=WHITE)
        box_label.move_to(box)

        input_arrow = Arrow(
            start=box.get_left() + LEFT * 1.8,
            end=box.get_left(),
            color=TEAL,
            stroke_color=TEAL,
            fill_color=TEAL,
            buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        )
        output_arrow = Arrow(
            start=box.get_right(),
            end=box.get_right() + RIGHT * 1.8,
            color=TEAL,
            stroke_color=TEAL,
            fill_color=TEAL,
            buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        )
        input_label = Text("input", font_size=30, color=WHITE).next_to(input_arrow, UP, buff=0.15)
        output_label = Text("output", font_size=30, color=WHITE).next_to(output_arrow, UP, buff=0.15)

        diagram = VGroup(box, box_label, input_arrow, output_arrow, input_label, output_label)
        diagram.move_to(UP * 2.5)

        self.play(FadeIn(diagram), run_time=max(0.05, 2.6))
        self.wait(max(0.05, 0.28))

        # ------------------------------------------------------------
        # Beat 2: 2.88-5.16 -- clarifying low-pass text.
        # ------------------------------------------------------------
        clar1 = Text("Keeps low-frequency components,", font_size=30, color=WHITE)
        clar2 = Text("reduces high-frequency ones", font_size=30, color=WHITE)
        clar_row = VGroup(clar1, clar2).arrange(RIGHT, buff=0.45).next_to(diagram, DOWN, buff=0.7)

        self.play(FadeIn(clar1), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.4))
        self.play(FadeIn(clar2), run_time=max(0.05, 0.88))

        # ------------------------------------------------------------
        # Beat 3: 5.16-7.52 -- counterpoint caption.
        # ------------------------------------------------------------
        caption = Text(
            "Not all unwanted signals are high-frequency.",
            font_size=36,
            weight=BOLD,
            color=YELLOW,
        ).next_to(clar_row, DOWN, buff=0.8)

        self.play(FadeIn(caption), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------
        # Beat 4: 7.52-13.46 -- clear top, split screen, left curve.
        # ------------------------------------------------------------
        top_content = VGroup(diagram, clar1, clar2, caption)
        self.play(FadeOut(top_content), run_time=max(0.05, 1.3))

        # Signal geometry parameters.
        self.sig_x_start = -5.8
        self.sig_x_end = -0.6
        self.sig_wavelength = self.sig_x_end - self.sig_x_start
        self.slow_amp = 0.9
        self.fast_amp = 0.12
        self.drift_amp = 0.30
        self.drift_period = 5.0
        self.fast_wavelength = 0.22
        self.fast_time_speed = 12.0

        def drift_offset(t):
            return self.drift_amp * np.sin(2 * np.pi * t / self.drift_period)

        def baseline_y_at(t, x):
            slow = self.slow_amp * np.sin(2 * np.pi * (x - self.sig_x_start) / self.sig_wavelength)
            return slow + drift_offset(t)

        def signal_y_at(t, x):
            fast = self.fast_amp * np.sin(
                2 * np.pi * (x - self.sig_x_start) / self.fast_wavelength
                - self.fast_time_speed * t
            )
            return baseline_y_at(t, x) + fast

        def compute_signal_points(t):
            xs = np.linspace(self.sig_x_start, self.sig_x_end, 300)
            ys = signal_y_at(t, xs)
            pts = np.array([xs, ys, np.zeros_like(xs)]).T
            return pts.tolist()

        def compute_baseline_points(t):
            xs = np.linspace(self.sig_x_start, self.sig_x_end, 300)
            ys = baseline_y_at(t, xs)
            pts = np.array([xs, ys, np.zeros_like(xs)]).T
            return pts.tolist()

        # Jagged signal curve.
        self.signal_curve = VMobject()
        self.signal_curve.set_stroke(color=WHITE, width=3)
        self.signal_curve.set_fill(opacity=0)
        self.signal_curve.set_points_as_corners(compute_signal_points(0))
        self.signal_curve.add_updater(
            lambda mob: mob.set_points_as_corners(
                compute_signal_points(self.time_tracker.get_value())
            )
        )

        # Highlight-only baseline curve, initially invisible.
        self.baseline_curve = VMobject()
        self.baseline_curve.set_stroke(color=YELLOW, width=6, opacity=0)
        self.baseline_curve.set_fill(opacity=0)
        self.baseline_curve.set_points_as_corners(compute_baseline_points(0))
        self.baseline_curve.add_updater(
            lambda mob: mob.set_points_as_corners(
                compute_baseline_points(self.time_tracker.get_value())
            )
        )

        divider = Line(UP * 3.4, DOWN * 3.4, color=GREY_B, stroke_width=2)
        left_panel = Rectangle(width=6.3, height=6.8, stroke_color=GREY_B, stroke_width=1, fill_opacity=0)
        left_panel.move_to(LEFT * 3.15)
        right_panel = Rectangle(width=6.3, height=6.8, stroke_color=GREY_B, stroke_width=1, fill_color=WHITE, fill_opacity=0)
        right_panel.move_to(RIGHT * 3.15)

        # Start the clock before the curve is added.
        self.time_tracker.set_value(0)
        self.time_tracker.add_updater(lambda mob, dt: mob.increment_value(dt))

        self.add(self.baseline_curve)
        self.play(FadeIn(divider, left_panel, right_panel, self.signal_curve), run_time=max(0.05, 2.4))
        self.wait(max(0.05, 2.24))

        # ------------------------------------------------------------
        # Beat 5: 13.46-18.22 -- yellow slow-drift highlight and arrow.
        # ------------------------------------------------------------
        arrow_x = self.sig_x_start + self.sig_wavelength / 2

        def make_slow_arrow_group():
            t0 = self.time_tracker.get_value()
            d0 = drift_offset(t0)
            bottom0 = np.array([arrow_x, d0 - self.slow_amp, 0.0])
            top0 = np.array([arrow_x, d0 + self.slow_amp, 0.0])

            arrow_up = Arrow(
                start=bottom0,
                end=top0,
                color=YELLOW,
                stroke_color=YELLOW,
                fill_color=YELLOW,
                stroke_width=4,
                buff=0,
                max_tip_length_to_length_ratio=0.08,
            )
            arrow_down = Arrow(
                start=top0,
                end=bottom0,
                color=YELLOW,
                stroke_color=YELLOW,
                fill_color=YELLOW,
                stroke_width=4,
                buff=0,
                max_tip_length_to_length_ratio=0.08,
            )
            slow_drift_label = Text("slow drift", font_size=28, color=YELLOW)
            slow_drift_label.next_to(arrow_up, RIGHT, buff=0.25)

            group = VGroup(arrow_up, arrow_down, slow_drift_label)

            def update_slow_arrow(g, au=arrow_up, ad=arrow_down, lab=slow_drift_label):
                t = self.time_tracker.get_value()
                d = drift_offset(t)
                b = np.array([arrow_x, d - self.slow_amp, 0.0])
                tp = np.array([arrow_x, d + self.slow_amp, 0.0])
                au.put_start_and_end_on(b, tp)
                ad.put_start_and_end_on(tp, b)
                lab.next_to(au, RIGHT, buff=0.25)

            group.add_updater(update_slow_arrow)
            return group

        self.slow_arrow_group = make_slow_arrow_group()

        self.play(
            self.baseline_curve.animate.set_stroke(color=YELLOW, width=6, opacity=1),
            FadeIn(self.slow_arrow_group),
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 2.26))

        # ------------------------------------------------------------
        # Beats 6-7: 18.22-28.74 -- four source labels with dotted connectors.
        # ------------------------------------------------------------
        label_specs = [
            ("electrode movement", np.array([-5.0, 2.2, 0.0]), -4.6),
            ("respiration", np.array([-3.4, -2.3, 0.0]), -2.2),
            ("electrode impedance change", np.array([-2.1, 1.5, 0.0]), -1.2),
            ("baseline shift", np.array([-0.9, -2.0, 0.0]), -0.6),
        ]

        def make_source_label(text, pos, target_x):
            label = Text(text, font_size=20, color=WHITE)
            label.move_to(pos)
            above = pos[1] > 0

            t0 = self.time_tracker.get_value()
            target0 = np.array([target_x, baseline_y_at(t0, target_x), 0.0])
            start0 = label.get_bottom() if above else label.get_top()
            connector = DashedLine(
                start0,
                target0,
                color=YELLOW,
                stroke_width=1.5,
                dash_length=0.08,
            )

            def update_connector(c, lbl=label, tx=target_x, ab=above):
                t = self.time_tracker.get_value()
                target = np.array([tx, baseline_y_at(t, tx), 0.0])
                start = lbl.get_bottom() if ab else lbl.get_top()
                c.put_start_and_end_on(start, target)

            connector.add_updater(update_connector)
            return label, connector

        self.labels = []
        self.connectors = []
        for text, pos, tx in label_specs:
            lab, conn = make_source_label(text, pos, tx)
            self.labels.append(lab)
            self.connectors.append(conn)

        # Beat 6: first three labels.
        self.wait(max(0.05, 0.38))
        self.play(FadeIn(self.labels[0], self.connectors[0]), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 2.10))
        self.play(FadeIn(self.labels[1], self.connectors[1]), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.80))
        self.play(FadeIn(self.labels[2], self.connectors[2]), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.28))

        # Beat 7: fourth label.
        self.wait(max(0.05, 0.22))
        self.play(FadeIn(self.labels[3], self.connectors[3]), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 2.54))

        # ------------------------------------------------------------
        # Beat 8: 28.74-35.64 -- left panel dims to gray, right brightens.
        # ------------------------------------------------------------
        self.left_content = VGroup(
            self.signal_curve,
            self.baseline_curve,
            self.slow_arrow_group,
            *self.labels,
            *self.connectors,
        )

        self.play(
            self.left_content.animate.set_color(GREY),
            right_panel.animate.set_fill(WHITE, opacity=0.10).set_stroke(color=WHITE, width=3),
            run_time=max(0.05, 6.9),
        )

        # ------------------------------------------------------------
        # Beat 9: 35.64-42.92 -- right panel high-pass filter box/icon.
        # ------------------------------------------------------------
        hp_box = Rectangle(
            width=3.6,
            height=3.4,
            fill_color=BLUE,
            fill_opacity=0.25,
            stroke_color=BLUE,
            stroke_width=4,
        )
        hp_title = Text("High-pass filter", font_size=36, weight=BOLD, color=WHITE)

        dashed_line = DashedLine(
            DOWN * 0.85,
            UP * 0.85,
            color=WHITE,
            stroke_width=3,
            dash_length=0.09,
        )
        high_arrow = Arrow(
            start=UP * 0.05,
            end=UP * 0.65,
            color=GREEN,
            stroke_color=GREEN,
            fill_color=GREEN,
            stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        low_arrow = Arrow(
            start=DOWN * 0.05,
            end=DOWN * 0.65,
            color=GREY_B,
            stroke_color=GREY_B,
            fill_color=GREY_B,
            stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        high_label = Text("high pass", font_size=20, color=GREEN).next_to(high_arrow, RIGHT, buff=0.08)
        low_label = Text("low reduced", font_size=20, color=GREY_B).next_to(low_arrow, RIGHT, buff=0.08)

        icon = VGroup(dashed_line, high_arrow, low_arrow, high_label, low_label)
        hp_inner = VGroup(hp_title, icon).arrange(DOWN, buff=0.25).move_to(hp_box.get_center())
        hp_group = VGroup(hp_box, hp_inner).move_to(RIGHT * 3.0)

        self.hp_dashed_line = dashed_line

        self.play(FadeIn(hp_group), run_time=max(0.05, 2.2))
        self.wait(max(0.05, 5.08))

        # ------------------------------------------------------------
        # Beat 10: 42.92-47.56 -- pulse the vertical dashed line once.
        # ------------------------------------------------------------
        self.play(
            self.hp_dashed_line.animate.set_stroke(width=9, color=YELLOW),
            rate_func=there_and_back,
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 2.14))

        # ------------------------------------------------------------
        # Beat 11: 47.56-51.34 -- cutoff frequency label and mark.
        # ------------------------------------------------------------
        cutoff_label = Text("cutoff frequency", font_size=30, weight=BOLD, color=GOLD)
        cutoff_label.next_to(hp_group, DOWN, buff=0.4)

        cutoff_mark = Line(LEFT * 0.7, RIGHT * 0.7, color=GOLD, stroke_width=5)
        cutoff_mark.move_to(self.hp_dashed_line.get_center())

        self.play(FadeIn(cutoff_label), FadeIn(cutoff_mark), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 2.28))

        # ------------------------------------------------------------
        # Beat 12: 51.34-55.10 -- applications caption, hold, then black.
        # ------------------------------------------------------------
        app_text = Text(
            "Applications in neural signal processing",
            font_size=28,
            color=WHITE,
        ).next_to(cutoff_label, DOWN, buff=0.35)

        self.play(FadeIn(app_text), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.76))

        full_black = Rectangle(width=14, height=8, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(full_black), run_time=max(0.05, 0.8))