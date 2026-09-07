ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'
}

class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Frequency axis, ticks, and passband
        # ------------------------------------------------------------
        axis_y = -2.7
        axis_left = -6.0
        axis_right = 6.0
        axis_line = Line(
            np.array([axis_left, axis_y, 0]),
            np.array([axis_right, axis_y, 0]),
            stroke_color=WHITE,
            stroke_width=3,
        )

        tick_freqs = [0, 10, 20, 30, 40, 50]
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i, freq in enumerate(tick_freqs):
            x = axis_left + (axis_right - axis_left) * i / (len(tick_freqs) - 1)
            tick = Line(
                np.array([x, axis_y - 0.12, 0]),
                np.array([x, axis_y + 0.12, 0]),
                stroke_color=GREY_B,
                stroke_width=2,
            )
            label = Text(str(freq), font_size=18, color=GREY)
            label.next_to(tick, DOWN, buff=0.14)
            tick_marks.add(tick)
            tick_labels.add(label)

        freq_label = Text("Frequency (Hz)", font_size=22, color=WHITE)
        freq_label.next_to(axis_line, DOWN, buff=0.35, aligned_edge=RIGHT)

        axis_group = VGroup(axis_line, tick_marks, tick_labels, freq_label)

        # Passband between 10 Hz and 30 Hz
        cutoff_low_x = -3.6
        cutoff_high_x = 1.2
        passband_center_x = (cutoff_low_x + cutoff_high_x) / 2
        passband = Rectangle(
            width=abs(cutoff_high_x - cutoff_low_x),
            height=1.2,
            fill_color=GREEN,
            fill_opacity=0.30,
            stroke_color=GREEN,
            stroke_width=2,
        )
        passband.move_to(np.array([passband_center_x, axis_y, 0]))
        passband.set_z_index(-1)

        def make_cutoff_marker(x):
            line = Line(
                np.array([x, axis_y - 0.55, 0]),
                np.array([x, axis_y + 0.65, 0]),
                stroke_color=YELLOW,
                stroke_width=3,
            )
            handle = Polygon(
                np.array([x - 0.12, axis_y + 0.65, 0]),
                np.array([x + 0.12, axis_y + 0.65, 0]),
                np.array([x, axis_y + 0.85, 0]),
                fill_color=YELLOW,
                fill_opacity=1,
                stroke_width=0,
            )
            return VGroup(line, handle)

        cutoff_marker_low = make_cutoff_marker(cutoff_low_x)
        cutoff_marker_high = make_cutoff_marker(cutoff_high_x)

        # ------------------------------------------------------------
        # Raw and filtered neural traces
        # ------------------------------------------------------------
        n_pts = 700
        x_vals = np.linspace(axis_left, axis_right, n_pts)
        t_vals = np.linspace(0, 4 * np.pi, n_pts)

        raw_signal = (
            0.60 * np.sin(1.5 * t_vals)
            + 0.35 * np.sin(7.0 * t_vals + 0.5)
            + 0.25 * np.sin(16.0 * t_vals + 1.2)
        )
        filtered_signal = 0.90 * np.sin(2.0 * t_vals)

        y_center = -0.3
        y_scale = 0.55

        raw_points = [
            np.array([x_vals[i], y_center + raw_signal[i] * y_scale, 0])
            for i in range(n_pts)
        ]
        filtered_points = [
            np.array([x_vals[i], y_center + filtered_signal[i] * y_scale, 0])
            for i in range(n_pts)
        ]

        raw_trace = VMobject(stroke_color=WHITE, stroke_width=2.5)
        raw_trace.set_points_as_corners(raw_points)

        filtered_trace = VMobject(stroke_color=GREEN, stroke_width=3.5)
        filtered_trace.set_points_as_corners(filtered_points)

        raw_label = Text("Raw signal", font_size=26, color=WHITE)
        raw_label.next_to(raw_trace.get_left(), UP, buff=0.25)

        filtered_label = Text("Filtered signal", font_size=26, color=GREEN)
        filtered_label.next_to(filtered_trace.get_left(), UP, buff=0.25)

        # ------------------------------------------------------------
        # Application icons
        # ------------------------------------------------------------
        def make_eeg_icon():
            brain = SVGMobject(
                ASSET_PATHS["brain"],
                fill_color=TEAL,
                fill_opacity=1,
                stroke_color=TEAL,
                stroke_width=0,
            )
            brain.scale_to_fit_height(0.9)
            cap_line = Line(
                brain.get_top() + LEFT * 0.4 + UP * 0.08,
                brain.get_top() + RIGHT * 0.4 + UP * 0.08,
                color=YELLOW,
                stroke_width=3,
            )
            dots = VGroup(*[
                Dot(
                    brain.get_top() + np.array([-0.25 + 0.25 * i, 0.24, 0]),
                    radius=0.045,
                    color=YELLOW,
                    fill_opacity=1,
                )
                for i in range(3)
            ])
            graphic = VGroup(brain, cap_line, dots)
            label = Text("EEG preprocessing", font_size=20, color=WHITE)
            return VGroup(graphic, label).arrange(DOWN, buff=0.10)

        def make_emg_icon():
            forearm = Ellipse(
                width=2.3,
                height=0.75,
                fill_color=ORANGE,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1,
            )
            center = forearm.get_center()
            dots = VGroup(*[
                Dot(
                    center + np.array([-0.55 + 0.55 * i, 0, 0]),
                    radius=0.06,
                    color=YELLOW,
                    fill_opacity=1,
                )
                for i in range(3)
            ])
            wires = VGroup(*[
                Line(
                    dot.get_center() + UP * 0.16,
                    dot.get_center() + UP * 0.55,
                    color=GREY_B,
                    stroke_width=1.5,
                )
                for dot in dots
            ])
            graphic = VGroup(forearm, wires, dots)
            label = Text("EMG preprocessing", font_size=20, color=WHITE)
            return VGroup(graphic, label).arrange(DOWN, buff=0.10)

        def make_lfp_icon():
            layer_colors = [BLUE, PURPLE, PINK, TEAL]
            layers = VGroup(*[
                Rectangle(
                    width=2.0,
                    height=0.28,
                    fill_color=layer_colors[i],
                    fill_opacity=1,
                    stroke_color=WHITE,
                    stroke_width=0.5,
                )
                for i in range(4)
            ])
            layers.arrange(DOWN, buff=0.06)

            probe_x = layers.get_top()[0] - 0.55
            top_probe = np.array([probe_x, layers.get_top()[1] + 0.85, 0])
            tip_probe = np.array([probe_x, layers.get_top()[1] - 0.08, 0])
            shaft = Line(top_probe, tip_probe, color=GREY_B, stroke_width=2.5)
            tip = Polygon(
                tip_probe + LEFT * 0.07,
                tip_probe + RIGHT * 0.07,
                tip_probe + DOWN * 0.12,
                fill_color=GREY,
                fill_opacity=1,
                stroke_width=0,
            )
            graphic = VGroup(layers, shaft, tip)
            label = Text("LFP analysis", font_size=20, color=WHITE)
            return VGroup(graphic, label).arrange(DOWN, buff=0.10)

        def make_bci_icon():
            brain = SVGMobject(
                ASSET_PATHS["brain"],
                fill_color=GREEN,
                fill_opacity=1,
                stroke_color=GREEN,
                stroke_width=0,
            )
            brain.scale_to_fit_height(0.85)

            monitor = Rectangle(
                width=0.85,
                height=0.70,
                fill_color=BLUE,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1,
            )
            screen = Rectangle(
                width=0.62,
                height=0.48,
                fill_color=GREEN,
                fill_opacity=0.9,
                stroke_width=0,
            )
            screen.move_to(monitor.get_center())
            stand = Line(
                monitor.get_bottom() + DOWN * 0.02,
                monitor.get_bottom() + DOWN * 0.16,
                color=GREY_B,
                stroke_width=2,
            )
            base = Line(
                monitor.get_bottom() + DOWN * 0.16 + LEFT * 0.18,
                monitor.get_bottom() + DOWN * 0.16 + RIGHT * 0.18,
                color=GREY_B,
                stroke_width=2,
            )
            monitor_group = VGroup(monitor, screen, stand, base)

            brain.shift(LEFT * 0.85)
            monitor_group.shift(RIGHT * 0.85)

            arrow1 = Arrow(
                brain.get_right() + UP * 0.12,
                monitor_group.get_left() + UP * 0.18,
                path_arc=0.8,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15,
            )
            arrow2 = Arrow(
                brain.get_right() + DOWN * 0.12,
                monitor_group.get_left() + DOWN * 0.18,
                path_arc=-0.8,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15,
            )

            graphic = VGroup(brain, monitor_group, arrow1, arrow2)
            label = Text("BCI", font_size=20, color=WHITE)
            return VGroup(graphic, label).arrange(DOWN, buff=0.10)

        icon1 = make_eeg_icon()
        icon2 = make_emg_icon()
        icon3 = make_lfp_icon()
        icon4 = make_bci_icon()

        icons = [icon1, icon2, icon3, icon4]
        icon_row = VGroup(*icons).arrange(RIGHT, buff=0.55)
        if icon_row.width > 11.8:
            icon_row.scale_to_fit_width(11.8)
        icon_row.move_to(UP * 2.75)
        final_icon_positions = [icon.get_center().copy() for icon in icons]

        # ------------------------------------------------------------
        # Beat 1: 0.00 - 1.40 — frequency axis and passband
        # ------------------------------------------------------------
        self.play(Create(axis_line), Write(tick_marks), Write(tick_labels), Write(freq_label), run_time=max(0.05, 0.70))
        self.play(
            FadeIn(passband),
            FadeIn(cutoff_marker_low),
            FadeIn(cutoff_marker_high),
            run_time=max(0.05, 0.70),
        )

        # ------------------------------------------------------------
        # Beat 2: 1.40 - 2.20 — raw neural trace
        # ------------------------------------------------------------
        self.play(FadeIn(raw_trace), Write(raw_label), run_time=max(0.05, 0.80))

        # ------------------------------------------------------------
        # Beat 3: 2.20 - 2.92 — passband pulse
        # ------------------------------------------------------------
        self.play(
            passband.animate.set_fill(opacity=0.55).set_stroke(width=5),
            run_time=max(0.05, 0.72),
            rate_func=there_and_back,
        )

        # Gap 2.92 - 3.40
        self.wait(max(0.05, 0.48))

        # ------------------------------------------------------------
        # Beat 4: 3.40 - 5.76 — raw becomes filtered alpha wave
        # ------------------------------------------------------------
        self.play(
            Transform(raw_trace, filtered_trace),
            FadeOut(raw_label),
            FadeIn(filtered_label),
            run_time=max(0.05, 2.36),
        )

        # Gap 5.76 - 6.36
        self.wait(max(0.05, 0.60))

        # ------------------------------------------------------------
        # Beat 5: 6.36 - 9.10 — EEG icon slides in
        # ------------------------------------------------------------
        icon1.move_to(np.array([-8.5, final_icon_positions[0][1], 0]))
        self.add(icon1)
        self.play(
            icon1.animate.move_to(final_icon_positions[0]),
            run_time=max(0.05, 2.74),
            rate_func=smooth,
        )

        # Gap 9.10 - 9.80
        self.wait(max(0.05, 0.70))

        # ------------------------------------------------------------
        # Beat 6: 9.80 - 10.92 — EMG icon slides in
        # ------------------------------------------------------------
        icon2.move_to(np.array([-8.5, final_icon_positions[1][1], 0]))
        self.add(icon2)
        self.play(
            icon2.animate.move_to(final_icon_positions[1]),
            run_time=max(0.05, 1.12),
            rate_func=smooth,
        )

        # Gap 10.92 - 11.64
        self.wait(max(0.05, 0.72))

        # ------------------------------------------------------------
        # Beat 7: 11.64 - 13.06 — LFP icon slides in
        # ------------------------------------------------------------
        icon3.move_to(np.array([-8.5, final_icon_positions[2][1], 0]))
        self.add(icon3)
        self.play(
            icon3.animate.move_to(final_icon_positions[2]),
            run_time=max(0.05, 1.42),
            rate_func=smooth,
        )

        # Gap 13.06 - 13.72
        self.wait(max(0.05, 0.66))

        # ------------------------------------------------------------
        # Beat 8: 13.72 - 15.44 — BCI icon slides in
        # ------------------------------------------------------------
        icon4.move_to(np.array([-8.5, final_icon_positions[3][1], 0]))
        self.add(icon4)
        self.play(
            icon4.animate.move_to(final_icon_positions[3]),
            run_time=max(0.05, 1.72),
            rate_func=smooth,
        )

        # ------------------------------------------------------------
        # Beat 9: 15.44 - 16.95 — hold full composition
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.51))