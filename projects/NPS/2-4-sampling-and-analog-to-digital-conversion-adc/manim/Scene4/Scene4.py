ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # BEAT 1: 0.00 - 3.08
        # Hold briefly, then clean slate with single smooth waveform,
        # time/amplitude axes, and sampling-frequency title.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.40))  # brief hold (previous composition is not inherited here)

        # Initial axes and wave
        init_x_left = -4.8
        init_x_right = 4.8
        init_axes_y = -2.3
        init_wave_x_left = -3.8
        init_wave_x_right = 3.8
        init_wave_base = -1.45
        init_wave_amp = 0.65

        init_x_axis = Line(
            start=np.array([init_x_left, init_axes_y, 0.0]),
            end=np.array([init_x_right, init_axes_y, 0.0]),
            color=WHITE,
            stroke_width=2,
        )
        init_y_axis = Line(
            start=np.array([init_x_left, init_axes_y, 0.0]),
            end=np.array([init_x_left, 0.15, 0.0]),
            color=WHITE,
            stroke_width=2,
        )
        init_time_label = Text("time", font_size=20, color=GREY)
        init_time_label.next_to(init_x_axis, RIGHT, buff=0.2)
        init_amp_label = Text("amplitude", font_size=20, color=GREY)
        init_amp_label.next_to(init_y_axis, UP, buff=0.2)

        def wave_points(x_min, x_max, base_y, amp, phase=0.0, n=200):
            pts = []
            for x in np.linspace(x_min, x_max, n):
                frac = (x - x_min) / (x_max - x_min)
                y = base_y + amp * np.sin(2 * PI * 2.5 * frac + phase)
                pts.append([x, y, 0.0])
            return pts

        init_wave = VMobject()
        init_wave.set_stroke(BLUE, width=4)
        init_wave.set_points_as_corners(
            wave_points(init_wave_x_left, init_wave_x_right, init_wave_base, init_wave_amp)
        )

        init_axes_group = VGroup(init_x_axis, init_y_axis, init_time_label, init_amp_label)

        self.play(FadeIn(init_axes_group), run_time=max(0.05, 0.80))
        self.play(Write(init_wave), run_time=max(0.05, 1.40))

        # Title
        title = Text(
            "sampling frequency (sampling rate)",
            font_size=38,
            color=WHITE,
            weight="BOLD",
        )
        title.scale_to_fit_width(12)
        title.move_to(np.array([0.0, 3.05, 0.0]))
        self.play(FadeIn(title), run_time=max(0.05, 0.48))

        # ----------------------------------------------------------------
        # BEAT 2: 3.46 - 5.74
        # Definition line and soft highlight pulse.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.38))  # gap 3.08 -> 3.46

        definition = Text(
            "number of samples collected every second",
            font_size=30,
            color=WHITE,
        )
        definition.move_to(np.array([0.0, 2.25, 0.0]))
        self.play(FadeIn(definition), run_time=max(0.05, 0.90))
        self.play(
            Indicate(definition, color=YELLOW, scale_factor=1.12),
            run_time=max(0.05, 1.38),
        )

        # ----------------------------------------------------------------
        # BEAT 3: 6.42 - 7.50
        # "measured in Hertz" and small Hz badge.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.68))  # gap 5.74 -> 6.42

        measured_line = Text("measured in Hertz", font_size=26, color=GREY)
        measured_line.move_to(np.array([-0.55, 1.78, 0.0]))
        hz_box = Rectangle(
            width=0.68,
            height=0.50,
            fill_color=YELLOW,
            fill_opacity=0.25,
            stroke_color=YELLOW,
            stroke_width=1.5,
        )
        hz_box.next_to(measured_line, RIGHT, buff=0.55)
        hz_text = Text("Hz", font_size=24, color=YELLOW, weight="BOLD")
        hz_text.move_to(hz_box.get_center())
        hz_badge = VGroup(hz_box, hz_text)

        self.play(FadeIn(measured_line, hz_badge), run_time=max(0.05, 1.08))

        # ----------------------------------------------------------------
        # BEAT 4: 8.24 - 11.64
        # Vertical dashed sweep line repeatedly left-to-right; leaves dots.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.74))  # gap 7.50 -> 8.24

        sample_xs = list(np.linspace(init_wave_x_left, init_wave_x_right, 10))
        sweep_dots = VGroup()
        for sx in sample_xs:
            sy = init_wave_base + init_wave_amp * np.sin(
                2 * PI * 2.5 * ((sx - init_wave_x_left) / (init_wave_x_right - init_wave_x_left))
            )
            dot = Dot(point=np.array([sx, sy, 0.0]), radius=0.065, color=YELLOW, fill_opacity=1)
            sweep_dots.add(dot)

        sweep_line = DashedLine(
            start=np.array([sample_xs[0], init_axes_y, 0.0]),
            end=np.array([sample_xs[0], -0.25, 0.0]),
            dash_length=0.12,
            color=YELLOW,
            stroke_width=2,
        )
        self.add(sweep_line)

        # First sweep: reveals dots as it passes each crossing
        self.play(FadeIn(sweep_dots[0]), run_time=max(0.05, 0.20))
        per_step_4 = 1.80 / 9
        for i in range(1, len(sample_xs)):
            dx = sample_xs[i] - sample_xs[i - 1]
            self.play(
                sweep_line.animate.shift(RIGHT * dx),
                FadeIn(sweep_dots[i]),
                run_time=max(0.05, per_step_4),
            )

        # instant jump back left (no animation time)
        self.remove(sweep_line)
        sweep_line.move_to(np.array([sample_xs[0], init_axes_y - 0.42, 0.0]))
        self.add(sweep_line)

        phrase = Text(
            "how frequently the analog signal is measured",
            font_size=22,
            color=GREY,
        )
        phrase.move_to(np.array([0.0, -2.85, 0.0]))

        # Second sweep + phrase
        self.play(
            sweep_line.animate.shift(RIGHT * (sample_xs[-1] - sample_xs[0])),
            FadeIn(phrase),
            run_time=max(0.05, 0.80),
        )

        # instant jump back left and third sweep
        self.remove(sweep_line)
        sweep_line.move_to(np.array([sample_xs[0], init_axes_y - 0.42, 0.0]))
        self.add(sweep_line)
        self.play(
            sweep_line.animate.shift(RIGHT * (sample_xs[-1] - sample_xs[0])),
            run_time=max(0.05, 0.60),
        )

        initial_group = VGroup(
            title,
            definition,
            measured_line,
            hz_badge,
            init_axes_group,
            init_wave,
            sweep_line,
            sweep_dots,
            phrase,
        )

        # ----------------------------------------------------------------
        # BEAT 5: 12.44 - 17.56
        # Split into three panels. Left panel gets sparse dots and 250 Hz.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.80))  # gap 11.64 -> 12.44

        self.play(FadeOut(initial_group), run_time=max(0.05, 0.80))

        PANEL_W = 3.2
        PANEL_H = 2.2
        PANEL_Y = 1.40
        PANEL_XS = [-4.1, 0.0, 4.1]
        PANEL_WAVE_BASE = PANEL_Y - 0.50
        PANEL_WAVE_AMP = 0.45

        def make_panel_wave(cx):
            x_min = cx - 1.15
            x_max = cx + 1.15
            w = VMobject()
            w.set_stroke(BLUE, width=3)
            w.set_points_as_corners(
                wave_points(x_min, x_max, PANEL_WAVE_BASE, PANEL_WAVE_AMP, n=180)
            )
            return w

        panel_group = VGroup()
        panel_frames = []
        for cx in PANEL_XS:
            frame = Rectangle(
                width=PANEL_W,
                height=PANEL_H,
                color=GREY_B,
                stroke_width=1.5,
            )
            frame.move_to(np.array([cx, PANEL_Y, 0.0]))
            x_axis = Line(
                start=np.array([cx - PANEL_W / 2 + 0.15, PANEL_Y - 0.65, 0.0]),
                end=np.array([cx + PANEL_W / 2 - 0.15, PANEL_Y - 0.65, 0.0]),
                color=WHITE,
                stroke_width=1.2,
            )
            y_axis = Line(
                start=np.array([cx - PANEL_W / 2 + 0.15, PANEL_Y - 0.65, 0.0]),
                end=np.array([cx - PANEL_W / 2 + 0.15, PANEL_Y + 0.55, 0.0]),
                color=WHITE,
                stroke_width=1.2,
            )
            wave = make_panel_wave(cx)
            vis = VGroup(frame, x_axis, y_axis, wave)
            panel_group.add(vis)
            panel_frames.append(frame)

        self.play(FadeIn(panel_group), run_time=max(0.05, 1.00))

        def panel_dots(cx, count, radius, color):
            dots = VGroup()
            x_min = cx - 1.15
            x_max = cx + 1.15
            for x in np.linspace(x_min, x_max, count):
                frac = (x - x_min) / (x_max - x_min)
                y = PANEL_WAVE_BASE + PANEL_WAVE_AMP * np.sin(2 * PI * 2.5 * frac)
                dots.add(Dot(point=np.array([x, y, 0.0]), radius=radius, color=color, fill_opacity=1))
            return dots

        left_dots = panel_dots(PANEL_XS[0], 9, 0.065, TEAL)
        mid_dots = panel_dots(PANEL_XS[1], 18, 0.055, BLUE)
        right_dots = panel_dots(PANEL_XS[2], 80, 0.035, PURPLE)

        # Left label and caption
        left_label = Text("250 Hz", font_size=28, weight="BOLD", color=TEAL)
        left_label.next_to(panel_group[0], UP, buff=0.20)
        left_caption = Text("250 samples per second", font_size=20, color=GREY)
        left_caption.next_to(panel_group[0], DOWN, buff=0.20)

        self.play(
            LaggedStart(*[FadeIn(d) for d in left_dots], lag_ratio=0.25),
            run_time=max(0.05, 2.00),
        )
        self.play(FadeIn(left_label, left_caption), run_time=max(0.05, 0.62))
        self.wait(max(0.05, 0.70))

        # ----------------------------------------------------------------
        # BEAT 6: 18.32 - 21.10
        # Middle panel: denser dots, 500 Hz.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.76))  # gap 17.56 -> 18.32

        mid_label = Text("500 Hz", font_size=28, weight="BOLD", color=BLUE)
        mid_label.next_to(panel_group[1], UP, buff=0.20)
        mid_caption = Text("500 samples per second", font_size=20, color=GREY)
        mid_caption.next_to(panel_group[1], DOWN, buff=0.20)

        self.play(
            LaggedStart(*[FadeIn(d) for d in mid_dots], lag_ratio=0.15),
            run_time=max(0.05, 1.78),
        )
        self.play(FadeIn(mid_label, mid_caption), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.45))

        # ----------------------------------------------------------------
        # BEAT 7: 21.90 - 29.98
        # Right panel: very dense dots, 1000 Hz.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.80))  # gap 21.10 -> 21.90

        right_label = Text("1000 Hz", font_size=28, weight="BOLD", color=PURPLE)
        right_label.next_to(panel_group[2], UP, buff=0.20)
        right_caption = Text("1000 samples per second", font_size=20, color=GREY)
        right_caption.next_to(panel_group[2], DOWN, buff=0.20)

        self.play(
            LaggedStart(*[FadeIn(d) for d in right_dots], lag_ratio=0.035),
            run_time=max(0.05, 4.50),
        )
        self.play(FadeIn(right_label, right_caption), run_time=max(0.05, 0.80))
        self.play(
            Indicate(right_label, color=PURPLE, scale_factor=1.15),
            Indicate(right_dots, color=PURPLE, scale_factor=1.06),
            run_time=max(0.05, 1.18),
        )
        self.wait(max(0.05, 1.60))

        # ----------------------------------------------------------------
        # BEAT 8: 29.98 - 33.46
        # Pulse right panel; note below panels.
        # ----------------------------------------------------------------
        self.play(
            Indicate(right_label, color=PURPLE, scale_factor=1.16),
            run_time=max(0.05, 0.60),
        )
        self.play(
            Indicate(right_dots, color=PURPLE, scale_factor=1.07),
            run_time=max(0.05, 0.60),
        )

        note = Text(
            "more measurements over the same period of time",
            font_size=22,
            color=GREY,
        )
        note.next_to(panel_group, DOWN, buff=0.85)
        self.play(FadeIn(note), run_time=max(0.05, 0.68))
        self.wait(max(0.05, 1.60))

        # ----------------------------------------------------------------
        # BEAT 9: 34.20 - 39.96
        # Storage and Computational Cost bar chart.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.74))  # gap 33.46 -> 34.20
        self.play(FadeOut(note), run_time=max(0.05, 0.40))

        def make_bar_chart(cx, title_text, heights, colors, bar_labels):
            baseline_y = -2.5
            title = Text(title_text, font_size=21, color=WHITE, weight="BOLD")
            title.move_to(np.array([cx, -0.90, 0.0]))
            baseline = Line(
                start=np.array([cx - 1.35, baseline_y, 0.0]),
                end=np.array([cx + 1.35, baseline_y, 0.0]),
                color=GREY_B,
                stroke_width=1.5,
            )
            labels = VGroup()
            bars = VGroup()
            offsets = [-0.95, 0.0, 0.95]
            for i, h in enumerate(heights):
                bx = cx + offsets[i]
                bar = Rectangle(
                    width=0.60,
                    height=h,
                    fill_color=colors[i],
                    fill_opacity=0.95,
                    stroke_width=0,
                )
                bar.move_to(np.array([bx, baseline_y + h / 2, 0.0]))
                bars.add(bar)
                lab = Text(bar_labels[i], font_size=15, color=GREY)
                lab.move_to(np.array([bx, baseline_y - 0.30, 0.0]))
                labels.add(lab)
            base = VGroup(baseline, title, labels)
            return base, bars, title

        cost_colors = [TEAL, BLUE, PURPLE]
        freq_labels = ["250 Hz", "500 Hz", "1000 Hz"]
        cost_heights = [0.75, 1.45, 2.15]

        cost_base, cost_bars, cost_title = make_bar_chart(
            cx=0.0,
            title_text="Storage & Computational Cost",
            heights=cost_heights,
            colors=cost_colors,
            bar_labels=freq_labels,
        )
        self.play(FadeIn(cost_base), run_time=max(0.05, 0.80))
        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in cost_bars],
                lag_ratio=0.28,
            ),
            run_time=max(0.05, 2.20),
        )
        self.play(Indicate(cost_title, color=YELLOW, scale_factor=1.18), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 1.46))

        cost_group = VGroup(cost_base, cost_bars)

        # ----------------------------------------------------------------
        # BEAT 10: 40.60 - 47.02
        # Slide cost chart left, add Accuracy chart, balance arrow.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.64))  # gap 39.96 -> 40.60

        self.play(cost_group.animate.shift(LEFT * 3.2), run_time=max(0.05, 1.00))

        acc_heights = [0.85, 1.55, 2.25]
        acc_base, acc_bars, acc_title = make_bar_chart(
            cx=3.65,
            title_text="Accuracy",
            heights=acc_heights,
            colors=cost_colors,
            bar_labels=freq_labels,
        )

        self.play(FadeIn(acc_base), run_time=max(0.05, 0.70))
        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in acc_bars],
                lag_ratio=0.45,
            ),
            run_time=max(0.05, 2.00),
        )

        accuracy_group = VGroup(acc_base, acc_bars)

        balance_arrow = VGroup(
            Arrow(
                start=np.array([-1.7, -1.85, 0.0]),
                end=np.array([1.7, -1.85, 0.0]),
                color=YELLOW,
                stroke_width=4,
                buff=0.1,
                max_tip_length_to_length_ratio=0.18,
            ),
            Arrow(
                start=np.array([1.7, -1.60, 0.0]),
                end=np.array([-1.7, -1.60, 0.0]),
                color=YELLOW,
                stroke_width=4,
                buff=0.1,
                max_tip_length_to_length_ratio=0.18,
            ),
        )

        self.play(Create(balance_arrow), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.70))
        self.play(FadeOut(balance_arrow), run_time=max(0.05, 1.02))

        # ----------------------------------------------------------------
        # BEAT 11: 48.22 - 57.08
        # Dim gauges into corners, add alignment lines, right-panel pulses,
        # and bold takeaway text.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 1.20))  # gap 47.02 -> 48.22

        cost_corner = np.array([-5.55, -3.15, 0.0])
        acc_corner = np.array([5.55, -3.15, 0.0])

        self.play(
            cost_group.animate.scale(0.55).move_to(cost_corner),
            accuracy_group.animate.scale(0.55).move_to(acc_corner),
            run_time=max(0.05, 1.00),
        )
        self.play(
            cost_group.animate.set_opacity(0.55),
            accuracy_group.animate.set_opacity(0.55),
            run_time=max(0.05, 0.40),
        )

        alignment_y_levels = [
            PANEL_WAVE_BASE - PANEL_WAVE_AMP,
            PANEL_WAVE_BASE,
            PANEL_WAVE_BASE + PANEL_WAVE_AMP,
        ]
        align_lines = VGroup()
        for y_level in alignment_y_levels:
            line = DashedLine(
                start=np.array([-5.75, y_level, 0.0]),
                end=np.array([5.75, y_level, 0.0]),
                dash_length=0.10,
                color=YELLOW,
                stroke_width=1.5,
            )
            line.set_opacity(0.55)
            align_lines.add(line)

        self.play(FadeIn(align_lines), run_time=max(0.05, 1.00))

        self.play(
            Indicate(right_label, color=PURPLE, scale_factor=1.18),
            run_time=max(0.05, 0.63),
        )
        self.play(
            Indicate(right_dots, color=PURPLE, scale_factor=1.06),
            run_time=max(0.05, 0.63),
        )

        takeaway = Text(
            "Sampling frequency must be sufficiently high\nto capture the important characteristics\nof the biological signal without losing information.",
            font_size=22,
            color=YELLOW,
            weight="BOLD",
            line_spacing=0.85,
        )
        takeaway.scale_to_fit_width(12.2)
        takeaway.move_to(np.array([0.0, -1.85, 0.0]))

        self.play(FadeIn(takeaway), run_time=max(0.05, 1.40))
        self.wait(max(0.05, 3.80))

        # ----------------------------------------------------------------
        # BEAT 12: final hold 57.08 - 58.02
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.94))