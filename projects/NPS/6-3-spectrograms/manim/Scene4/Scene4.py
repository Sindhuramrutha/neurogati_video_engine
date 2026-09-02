ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(Scene):
    X_LEFT = -5.25
    X_RIGHT = 5.25
    WAVE_CY = 2.35
    WAVE_TOP = 3.05
    WAVE_BOT = 1.70
    WAVE_TIME_Y = 1.20
    SPEC_TOP = -0.25
    SPEC_BOT = -2.25
    SPEC_CY = -1.25
    FREQ_AXIS_X = -6.05
    SPEC_TIME_Y = -2.75

    def time_x(self, t):
        return self.X_LEFT + (t / 15.0) * (self.X_RIGHT - self.X_LEFT)

    def freq_y(self, f):
        return self.SPEC_BOT + (f / 60.0) * (self.SPEC_TOP - self.SPEC_BOT)

    def make_time_axis(self, y, label="Time (s)"):
        axis = Line(
            np.array([self.X_LEFT, y, 0]),
            np.array([self.X_RIGHT, y, 0]),
            color=WHITE,
            stroke_width=2,
        )
        items = VGroup(axis)
        for t in [0, 5, 10, 15]:
            x = self.time_x(t)
            tick = Line(
                np.array([x, y - 0.06, 0]),
                np.array([x, y + 0.06, 0]),
                color=WHITE,
                stroke_width=2,
            )
            lab = Text(str(t), font_size=16, color=WHITE)
            lab.next_to(tick, DOWN, buff=0.05)
            items.add(tick, lab)
        axis_label = Text(label, font_size=20, color=WHITE)
        axis_label.next_to(items, DOWN, buff=0.10)
        items.add(axis_label)
        items.set_z_index(5)
        return items

    def make_spectrogram_panel_group(self):
        panel = Rectangle(
            width=self.X_RIGHT - self.X_LEFT,
            height=self.SPEC_TOP - self.SPEC_BOT,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        panel.move_to(np.array([0, self.SPEC_CY, 0]))
        panel.set_z_index(1)

        freq_axis = Line(
            np.array([self.FREQ_AXIS_X, self.SPEC_BOT, 0]),
            np.array([self.FREQ_AXIS_X, self.SPEC_TOP, 0]),
            color=WHITE,
            stroke_width=2,
        )
        freq_axis.set_z_index(5)

        freq_label = Text("Frequency (Hz)", font_size=20, color=WHITE).rotate(PI / 2)
        freq_label.next_to(freq_axis, LEFT, buff=0.12)
        freq_label.set_z_index(5)

        freq_ticks = VGroup()
        for f in [0, 20, 40, 60]:
            fy = self.freq_y(f)
            tick = Line(
                np.array([self.FREQ_AXIS_X - 0.05, fy, 0]),
                np.array([self.FREQ_AXIS_X + 0.05, fy, 0]),
                color=WHITE,
                stroke_width=1.5,
            )
            tick.set_z_index(5)
            freq_ticks.add(tick)

        spec_time_axis = self.make_time_axis(self.SPEC_TIME_Y, label="Time (s)")

        group = VGroup(panel, freq_axis, freq_label, freq_ticks, spec_time_axis)
        return group, panel

    def make_line_trace(self, t0, t1, y_func, color, stroke_width):
        n = max(4, int((t1 - t0) * 50) + 2)
        ts = np.linspace(t0, t1, n)
        pts = [np.array([self.time_x(t), y_func(t), 0]) for t in ts]
        trace = VGroup(
            *[
                Line(pts[i], pts[i + 1], color=color, stroke_width=stroke_width)
                for i in range(len(pts) - 1)
            ]
        )
        return trace

    def base_y(self, t):
        return (
            self.WAVE_CY
            + 0.07 * np.sin(2 * np.pi * 1.7 * t + 0.8)
            + 0.04 * np.sin(2 * np.pi * 4.2 * t + 1.4)
        )

    def alpha_y(self, t):
        envelope = np.sin(np.pi * (t - 5.0) / 5.0) ** 2
        return self.WAVE_CY + 0.17 * np.sin(2 * np.pi * 10.0 * t) * envelope

    def highfreq_y(self, t):
        envelope = np.exp(-(((t - 12.5) / 0.15) ** 2))
        return self.WAVE_CY + 0.08 * np.sin(2 * np.pi * 40.0 * t) * envelope

    def make_alpha_spec_band(self):
        x0, x1 = self.time_x(5), self.time_x(10)
        y_bot, y_top = self.freq_y(8), self.freq_y(13)
        colors = [YELLOW, GOLD, ORANGE, RED, MAROON]
        n = len(colors)
        ys = np.linspace(y_bot, y_top, n + 1)
        strips = VGroup()
        for i, color in enumerate(colors):
            strip = Rectangle(
                width=x1 - x0,
                height=ys[i + 1] - ys[i],
                fill_color=color,
                fill_opacity=0.85,
                stroke_width=0,
            )
            strip.move_to(np.array([(x0 + x1) / 2, (ys[i] + ys[i + 1]) / 2, 0]))
            strip.set_z_index(2)
            strips.add(strip)
        return strips

    def make_highfreq_spec_burst(self):
        x0, x1 = self.time_x(12.1), self.time_x(13.0)
        y_bot, y_top = self.freq_y(30), self.freq_y(50)
        colors = [YELLOW, GOLD, ORANGE, RED, MAROON, ORANGE, GOLD, YELLOW]
        n = len(colors)
        ys = np.linspace(y_bot, y_top, n + 1)
        strips = VGroup()
        for i, color in enumerate(colors):
            strip = Rectangle(
                width=x1 - x0,
                height=ys[i + 1] - ys[i],
                fill_color=color,
                fill_opacity=0.9,
                stroke_width=0,
            )
            strip.move_to(np.array([(x0 + x1) / 2, (ys[i] + ys[i + 1]) / 2, 0]))
            strip.set_z_index(2)
            strips.add(strip)
        return strips

    def make_static_spectrum(self):
        panel = Rectangle(
            width=2.6,
            height=1.6,
            fill_color=BLACK,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        x_min, x_max, y_min, y_max = -1.1, 1.1, -0.7, 0.7
        axis_h = Line(
            np.array([x_min, y_min, 0]),
            np.array([x_max, y_min, 0]),
            color=WHITE,
            stroke_width=1.5,
        )
        axis_v = Line(
            np.array([x_min, y_min, 0]),
            np.array([x_min, y_max, 0]),
            color=WHITE,
            stroke_width=1.5,
        )
        freqs = np.linspace(0, 60, 80)
        amps = np.exp(-((freqs - 10) ** 2) / (2 * 3.0 ** 2)) + 0.45 * np.exp(
            -((freqs - 40) ** 2) / (2 * 4.0 ** 2)
        )
        amp_max = max(amps)
        pts = []
        for f, a in zip(freqs, amps):
            x = x_min + 0.30 + (a / amp_max) * (x_max - x_min - 0.45)
            y = y_min + (f / 60.0) * (y_max - y_min)
            pts.append(np.array([x, y, 0]))
        curve = VGroup(
            *[
                Line(pts[i], pts[i + 1], color=GOLD, stroke_width=2.0)
                for i in range(len(pts) - 1)
            ]
        )
        label = Text(
            "Conventional frequency spectrum", font_size=16, color=WHITE
        ).scale_to_fit_width(2.6)
        label.next_to(panel, DOWN, buff=0.12)
        group = VGroup(panel, axis_h, axis_v, curve, label)
        group.move_to(np.array([4.05, 1.70, 0]))
        group.set_z_index(10)
        return group

    def construct(self):
        self.camera.background_color = "#0F1116"

        # Beat 1: 0.00 - 4.76
        title = Text(
            "Interpreting a spectrogram", font_size=44, color=WHITE, weight=BOLD
        ).scale_to_fit_width(12)
        title.to_edge(UP, buff=0.8)
        subtitle = Text("Neural signal processing", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 2.2))
        self.play(FadeOut(title), FadeOut(subtitle), run_time=max(0.05, 1.36))

        self.wait(max(0.05, 0.80))

        # Beat 2: 5.56 - 8.44
        baseline_wave = self.make_line_trace(0, 15, self.base_y, GREY, 2.0)
        baseline_wave.set_z_index(4)
        baseline_wave.shift(LEFT * 12)
        self.add(baseline_wave)
        wave_time_axis_group = self.make_time_axis(self.WAVE_TIME_Y, label="Time (s)")
        self.spec_panel_group, self.spec_panel = self.make_spectrogram_panel_group()

        self.play(baseline_wave.animate.shift(RIGHT * 12), run_time=max(0.05, 1.80))
        self.play(
            FadeIn(wave_time_axis_group),
            FadeIn(self.spec_panel_group),
            run_time=max(0.05, 1.08),
        )

        self.wait(max(0.05, 0.82))

        # Beat 3: 9.26 - 14.14
        x5 = self.time_x(5)
        x10 = self.time_x(10)

        alpha_band_highlight = Rectangle(
            width=x10 - x5,
            height=self.WAVE_TOP - self.WAVE_BOT,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=0,
        )
        alpha_band_highlight.move_to(
            np.array([(x5 + x10) / 2, (self.WAVE_TOP + self.WAVE_BOT) / 2, 0])
        )
        alpha_band_highlight.set_z_index(1)

        alpha_dash5 = DashedLine(
            np.array([x5, self.WAVE_TOP, 0]),
            np.array([x5, self.WAVE_BOT, 0]),
            dash_length=0.12,
            color=GREY_B,
            stroke_width=2,
        )
        alpha_dash10 = DashedLine(
            np.array([x10, self.WAVE_TOP, 0]),
            np.array([x10, self.WAVE_BOT, 0]),
            dash_length=0.12,
            color=GREY_B,
            stroke_width=2,
        )
        alpha_dash5.set_z_index(7)
        alpha_dash10.set_z_index(7)

        alpha_label5 = Text("5 s", font_size=20, color=YELLOW)
        alpha_label10 = Text("10 s", font_size=20, color=YELLOW)
        alpha_label5.move_to(np.array([x5, self.WAVE_BOT - 0.30, 0]))
        alpha_label10.move_to(np.array([x10, self.WAVE_BOT - 0.30, 0]))

        alpha_activity_label = Text(
            "Alpha activity: 5–10 s", font_size=24, color=GOLD
        )
        alpha_activity_label.move_to(np.array([(x5 + x10) / 2, 3.40, 0]))

        self.play(FadeIn(alpha_band_highlight), run_time=max(0.05, 1.0))
        self.play(Create(alpha_dash5), Create(alpha_dash10), run_time=max(0.05, 1.0))
        self.play(FadeIn(alpha_label5), FadeIn(alpha_label10), run_time=max(0.05, 0.8))
        self.play(FadeIn(alpha_activity_label), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.88))

        self.wait(max(0.05, 0.86))

        # Beat 4: 15.00 - 20.52
        alpha_spec_band = self.make_alpha_spec_band()
        alpha_wave_overlay = self.make_line_trace(
            5, 10, self.alpha_y, ORANGE, 3.0
        )
        alpha_wave_overlay.set_z_index(5)

        self.play(
            alpha_dash5.animate.put_start_and_end_on(
                np.array([x5, self.WAVE_TOP, 0]),
                np.array([x5, self.SPEC_BOT, 0]),
            ),
            alpha_dash10.animate.put_start_and_end_on(
                np.array([x10, self.WAVE_TOP, 0]),
                np.array([x10, self.SPEC_BOT, 0]),
            ),
            FadeIn(alpha_spec_band),
            run_time=max(0.05, 1.0),
        )
        self.play(FadeIn(alpha_wave_overlay), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.0))
        self.wait(max(0.05, 1.0))
        self.wait(max(0.05, 1.32))

        self.wait(max(0.05, 0.84))

        # Beat 5: 21.36 - 23.82
        alpha_band_label = Text(
            "Alpha band: 8–13 Hz", font_size=15, color=YELLOW
        ).scale_to_fit_width(2.0)
        alpha_band_label.move_to(np.array([-4.70, self.freq_y(10.5), 0]))
        self.play(FadeIn(alpha_band_label), run_time=max(0.05, 0.8))
        self.play(
            Indicate(alpha_spec_band, color=YELLOW, scale_factor=1.07),
            run_time=max(0.05, 0.86),
        )
        self.wait(max(0.05, 0.80))

        self.wait(max(0.05, 0.82))

        # Beat 6: 24.64 - 29.28
        self.play(FadeOut(alpha_band_label), run_time=max(0.05, 1.2))

        stim_x = self.time_x(12)
        stim_line = Line(
            np.array([stim_x, self.WAVE_TOP + 0.10, 0]),
            np.array([stim_x, self.WAVE_BOT, 0]),
            color=WHITE,
            stroke_width=2.5,
        )
        stim_line.set_z_index(7)
        stim_label = Text("Stimulus", font_size=20, color=YELLOW)
        stim_label.next_to(stim_line, UP, buff=0.10)

        self.play(Create(stim_line), run_time=max(0.05, 1.2))
        self.play(FadeIn(stim_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.24))

        # Beat 7: 29.28 - 34.06
        x12_1 = self.time_x(12.1)
        x13 = self.time_x(13.0)

        high_dash12 = DashedLine(
            np.array([x12_1, self.WAVE_TOP, 0]),
            np.array([x12_1, self.SPEC_BOT, 0]),
            dash_length=0.12,
            color=GREY_B,
            stroke_width=2,
        )
        high_dash13 = DashedLine(
            np.array([x13, self.WAVE_TOP, 0]),
            np.array([x13, self.SPEC_BOT, 0]),
            dash_length=0.12,
            color=GREY_B,
            stroke_width=2,
        )
        high_dash12.set_z_index(7)
        high_dash13.set_z_index(7)

        highfreq_wave_overlay = self.make_line_trace(
            12.1, 13.0, self.highfreq_y, GOLD, 2.8
        )
        highfreq_wave_overlay.set_z_index(5)

        highfreq_spec_burst = self.make_highfreq_spec_burst()

        self.play(Create(high_dash12), Create(high_dash13), run_time=max(0.05, 0.6))
        self.play(FadeIn(highfreq_wave_overlay), run_time=max(0.05, 0.7))
        self.play(FadeIn(highfreq_spec_burst), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.5))
        self.play(highfreq_spec_burst.animate.set_opacity(0.20), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.68))

        self.wait(max(0.05, 0.78))

        # Beat 8: 34.84 - 40.38
        self.play(FadeOut(highfreq_spec_burst), run_time=max(0.05, 1.2))
        static_spec_group = self.make_static_spectrum()
        self.play(FadeIn(static_spec_group), run_time=max(0.05, 1.4))
        self.play(
            Indicate(static_spec_group, color=GOLD, scale_factor=1.08),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 2.14))

        self.wait(max(0.05, 0.48))

        # Beat 9: 40.86 - 43.84
        alpha_region_marker = Rectangle(
            width=x10 - x5,
            height=0.20,
            fill_color=YELLOW,
            fill_opacity=0.25,
            stroke_width=0,
        )
        alpha_region_marker.move_to(
            np.array([(x5 + x10) / 2, self.SPEC_TIME_Y - 0.22, 0])
        )
        burst_marker = Rectangle(
            width=x13 - x12_1,
            height=0.20,
            fill_color=ORANGE,
            fill_opacity=0.25,
            stroke_width=0,
        )
        burst_marker.move_to(
            np.array([(x12_1 + x13) / 2, self.SPEC_TIME_Y - 0.22, 0])
        )
        region_markers = VGroup(alpha_region_marker, burst_marker)
        region_markers.set_z_index(8)

        when_changes_label = Text(
            "When changes occur", font_size=24, color=YELLOW
        )
        when_changes_label.move_to(np.array([0, 0.55, 0]))

        self.play(
            FadeOut(static_spec_group),
            self.spec_panel.animate.set_stroke(YELLOW, width=2.5),
            run_time=max(0.05, 0.8),
        )
        self.play(
            Indicate(alpha_spec_band, color=YELLOW, scale_factor=1.10),
            highfreq_spec_burst.animate.set_opacity(0.60),
            run_time=max(0.05, 0.6),
        )
        self.play(
            FadeIn(region_markers),
            FadeIn(when_changes_label),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.78))

        self.wait(max(0.05, 0.90))

        # Beat 10: 44.74 - 52.20
        cleanup_group = VGroup(
            alpha_band_highlight,
            alpha_dash5,
            alpha_dash10,
            alpha_label5,
            alpha_label10,
            alpha_activity_label,
            stim_line,
            stim_label,
            high_dash12,
            high_dash13,
            region_markers,
            when_changes_label,
        )

        nonstationary_label = Text(
            "Non-stationary neural signals", font_size=30, color=GOLD
        ).scale_to_fit_width(11)
        nonstationary_label.to_edge(UP, buff=0.35)

        self.play(FadeOut(cleanup_group), run_time=max(0.05, 0.8))
        self.play(FadeIn(nonstationary_label), run_time=max(0.05, 1.0))
        self.play(
            Indicate(alpha_spec_band, color=YELLOW, scale_factor=1.15),
            run_time=max(0.05, 1.0),
        )
        self.play(
            Indicate(highfreq_spec_burst, color=GOLD, scale_factor=1.15),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 3.66))

        # Beat 11: 52.20 - 52.95
        self.wait(max(0.05, 0.75))