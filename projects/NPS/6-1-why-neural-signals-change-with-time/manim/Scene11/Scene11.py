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
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene11(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----- animation trackers for the continuously changing waveform -----
        time_tracker = ValueTracker(0.0)
        wave_visibility_tracker = ValueTracker(0.0)
        wave_glow_tracker = ValueTracker(0.0)
        wave_dim_tracker = ValueTracker(1.0)

        # ----- changing waveform builders -----
        def wave_points(t):
            xs = np.linspace(-6.5, 6.5, 420)
            freq = 0.42 + 0.10 * np.sin(0.55 * t)
            amp = 0.27 + 0.07 * np.sin(0.42 * t + 1.2)
            phase = 1.15 * t
            envelope = 0.82 + 0.18 * np.sin(0.32 * t + 0.08 * xs)
            ys = 2.40 + amp * envelope * np.sin(2 * np.pi * freq * xs + phase)
            return np.array([xs, ys, np.zeros_like(xs)]).T

        def make_wave(t, width, opacity):
            pts = wave_points(t)
            wave = VMobject(stroke_color=YELLOW, stroke_width=width, stroke_opacity=opacity)
            wave.set_points_as_corners(pts)
            return wave

        main_wave = always_redraw(
            lambda: make_wave(
                time_tracker.get_value(),
                5,
                wave_visibility_tracker.get_value() * wave_dim_tracker.get_value(),
            )
        )
        glow_wave = always_redraw(
            lambda: make_wave(
                time_tracker.get_value(),
                16,
                wave_glow_tracker.get_value() * wave_dim_tracker.get_value(),
            )
        )
        wave_group = VGroup(glow_wave, main_wave)

        # ----- static frequency spectrum -----
        spec_origin = np.array([0.0, -1.45, 0.0])
        x_axis = Line(
            spec_origin + LEFT * 3.2,
            spec_origin + RIGHT * 3.2,
            color=GREY_B,
            stroke_width=2,
        )
        y_axis = Line(
            spec_origin + DOWN * 0.7,
            spec_origin + UP * 0.9,
            color=GREY_B,
            stroke_width=2,
        )

        freqs = np.linspace(0, 30, 320)
        amps = 0.65 * np.exp(-((freqs - 10) / 2.4) ** 2) + 0.40 * np.exp(-((freqs - 20) / 3.0) ** 2)
        amp_max = np.max(amps)

        spec_x = spec_origin[0] - 3.2 + (freqs / 30.0) * 6.4
        spec_y = spec_origin[1] - 0.7 + (amps / amp_max) * 1.4
        spec_pts = np.array([spec_x, spec_y, np.zeros_like(freqs)]).T

        glow_curve = VMobject(stroke_color=ORANGE, stroke_width=12, stroke_opacity=0.0)
        glow_curve.set_points_as_corners(spec_pts)
        main_spec_curve = VMobject(stroke_color=TEAL, stroke_width=4)
        main_spec_curve.set_points_as_corners(spec_pts)

        spectrum_group = VGroup(x_axis, y_axis, glow_curve, main_spec_curve)
        spectrum_group.set_opacity(0.0)

        spectrum_box = SurroundingRectangle(
            spectrum_group,
            color=ORANGE,
            buff=0.22,
            corner_radius=0.08,
            stroke_width=3,
            stroke_opacity=0.0,
            fill_color=ORANGE,
            fill_opacity=0.08,
        )

        # ----- previous summary panel placeholder -----
        prev_panel = Rectangle(
            width=14.2,
            height=8.2,
            fill_color="#1D222D",
            fill_opacity=0.95,
            stroke_color=GREY_B,
            stroke_width=2,
        )

        self.add(wave_group, spectrum_group, spectrum_box, prev_panel)

        # ----- beat 1: 0.00-1.52 previous panel fades out, waveform and spectrum fade in -----
        self.play(
            FadeOut(prev_panel),
            spectrum_group.animate.set_opacity(1.0),
            wave_visibility_tracker.animate.set_value(1.0),
            time_tracker.animate.increment_value(1.52),
            run_time=max(0.05, 1.52),
        )
        self.remove(prev_panel)

        # ----- beat 2: 1.52-2.40 waveform continues, spectrum stays fixed -----
        self.play(time_tracker.animate.increment_value(0.88), run_time=max(0.05, 0.88))

        # ----- beat 3: 2.40-4.80 waveform glow + neural signal label -----
        wave_label = Text(
            "Neural signal — changes over time",
            font_size=26,
            color=WHITE,
        )
        wave_label.scale_to_fit_width(9.0)
        wave_label.move_to(np.array([0.0, 1.78, 0.0]))

        self.play(
            wave_glow_tracker.animate.set_value(0.45),
            FadeIn(wave_label),
            time_tracker.animate.increment_value(1.4),
            run_time=max(0.05, 1.4),
        )
        self.play(time_tracker.animate.increment_value(1.0), run_time=max(0.05, 1.0))

        # ----- beat 4: 4.80-6.00 static spectrum highlighted + its label -----
        spectrum_label = Text(
            "Conventional Fourier Transform — one spectrum for the whole recording",
            font_size=22,
            color=WHITE,
        )
        spectrum_label.scale_to_fit_width(6.0)
        spectrum_label.next_to(spectrum_group, DOWN, buff=0.35)

        self.play(
            glow_curve.animate.set_opacity(0.65),
            FadeIn(spectrum_label),
            time_tracker.animate.increment_value(1.2),
            run_time=max(0.05, 1.2),
        )

        # ----- beat 5: 6.00-10.94 box the static spectrum, waveform continues -----
        spectrum_box.set_opacity(0.0)
        self.play(
            spectrum_box.animate.set_opacity(1.0),
            time_tracker.animate.increment_value(1.0),
            run_time=max(0.05, 1.0),
        )
        self.play(time_tracker.animate.increment_value(3.94), run_time=max(0.05, 3.94))

        # ----- beat 6/7: 10.94-14.22 hold then question mark appears -----
        self.play(time_tracker.animate.increment_value(0.88), run_time=max(0.05, 0.88))

        question_mark = Text("?", font_size=170, color=GOLD, weight="BOLD")
        question_mark.move_to(np.array([0.0, 0.35, 0.0]))

        self.play(
            FadeIn(question_mark),
            time_tracker.animate.increment_value(0.80),
            run_time=max(0.05, 0.80),
        )
        self.play(time_tracker.animate.increment_value(1.60), run_time=max(0.05, 1.60))

        # ----- beat 8: 14.22-15.54 question pulses once, clock appears -----
        clock_icon = SVGMobject(
            ASSET_PATHS["stopwatch"],
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=YELLOW,
            stroke_width=0,
        )
        clock_icon.scale_to_fit_height(0.65)
        clock_icon.move_to(np.array([2.6, 0.55, 0.0]))

        self.play(
            question_mark.animate.scale(1.12),
            FadeIn(clock_icon),
            time_tracker.animate.increment_value(0.80),
            rate_func=there_and_back,
            run_time=max(0.05, 0.80),
        )
        self.play(time_tracker.animate.increment_value(0.52), run_time=max(0.05, 0.52))

        # short gap before STFT transition
        self.play(time_tracker.animate.increment_value(0.74), run_time=max(0.05, 0.74))

        # ----- surface helpers -----
        surf_center = np.array([0.0, 0.35, 0.0])
        FL = surf_center + np.array([-2.1, -0.7, 0.0])
        FR = surf_center + np.array([2.2, -0.7, 0.0])
        BR = surf_center + np.array([1.2, 0.7, 0.0])
        BL = surf_center + np.array([-2.8, 0.7, 0.0])

        def surface_base_point(t, f):
            x = (
                FL[0] * (1 - t) * (1 - f)
                + FR[0] * t * (1 - f)
                + BR[0] * t * f
                + BL[0] * (1 - t) * f
            )
            y = (
                FL[1] * (1 - t) * (1 - f)
                + FR[1] * t * (1 - f)
                + BR[1] * t * f
                + BL[1] * (1 - t) * f
            )
            return np.array([x, y, 0.0])

        def height_fn(t, f):
            h1 = 0.95 * np.exp(-(((t - 0.35) / 0.22) ** 2 + ((f - 0.60) / 0.28) ** 2))
            h2 = 0.65 * np.exp(-(((t - 0.78) / 0.18) ** 2 + ((f - 0.35) / 0.22) ** 2))
            h3 = 0.30 * np.exp(-(((t - 0.50) / 0.30) ** 2 + ((f - 0.10) / 0.35) ** 2))
            return h1 + h2 + h3

        n_t, n_f = 7, 5
        base_pts = [[None] * n_f for _ in range(n_t)]
        top_pts = [[None] * n_f for _ in range(n_t)]

        for i in range(n_t):
            t = i / (n_t - 1)
            for j in range(n_f):
                f = j / (n_f - 1)
                base = surface_base_point(t, f)
                h = height_fn(t, f)
                top = base + np.array([0.0, 0.0, 0.0])
                top[1] += h * 1.15
                base_pts[i][j] = base
                top_pts[i][j] = top

        base_poly = Polygon(
            FL, FR, BR, BL,
            fill_color=BLUE,
            fill_opacity=0.25,
            stroke_color=WHITE,
            stroke_width=1.5,
        )

        verticals = VGroup()
        for i in range(n_t):
            for j in range(n_f):
                verticals.add(
                    Line(
                        base_pts[i][j],
                        top_pts[i][j],
                        color=GREY_B,
                        stroke_width=1.2,
                        stroke_opacity=0.45,
                    )
                )

        quads = VGroup()
        color_ramp = [BLUE, TEAL, GREEN, ORANGE]
        for i in range(n_t - 1):
            for j in range(n_f - 1):
                p0 = top_pts[i][j]
                p1 = top_pts[i + 1][j]
                p2 = top_pts[i + 1][j + 1]
                p3 = top_pts[i][j + 1]
                h_avg = (
                    height_fn(i / (n_t - 1), j / (n_f - 1))
                    + height_fn((i + 1) / (n_t - 1), j / (n_f - 1))
                    + height_fn((i + 1) / (n_t - 1), (j + 1) / (n_f - 1))
                    + height_fn(i / (n_t - 1), (j + 1) / (n_f - 1))
                ) / 4.0
                color_idx = min(3, int(h_avg / 1.2 * 4))
                quads.add(
                    Polygon(
                        p0, p1, p2, p3,
                        fill_color=color_ramp[color_idx],
                        fill_opacity=0.68,
                        stroke_color=WHITE,
                        stroke_width=0.7,
                    )
                )

        surface_form = VGroup(base_poly, verticals, quads)
        surface_form.center()

        # ----- beat 9: 16.28-17.56 question mark morphs into time-frequency surface -----
        spectrum_zone = VGroup(spectrum_group, spectrum_box, spectrum_label)
        spectrum_final_pos = np.array([-2.2, -2.0, 0.0])

        self.play(
            Transform(question_mark, surface_form),
            spectrum_zone.animate.move_to(spectrum_final_pos).scale(0.72).set_opacity(0.75),
            time_tracker.animate.increment_value(1.28),
            run_time=max(0.05, 1.28),
        )

        # ----- beat 10: 17.56-18.68 axes appear one at a time -----
        time_axis = Arrow(FL, FR, color=WHITE, stroke_width=3, buff=0.0, max_tip_length_to_length_ratio=0.15)
        time_label = Text("Time", font_size=24, color=YELLOW)
        time_label.next_to(time_axis.get_center(), DOWN, buff=0.2)

        freq_axis = Arrow(FR, BR, color=WHITE, stroke_width=3, buff=0.0, max_tip_length_to_length_ratio=0.15)
        freq_label = Text("Frequency", font_size=24, color=YELLOW)
        freq_label.next_to(freq_axis.get_center(), RIGHT, buff=0.15)

        power_axis = Arrow(FL, FL + UP * 1.6, color=WHITE, stroke_width=3, buff=0.0, max_tip_length_to_length_ratio=0.15)
        power_label = Text("Power", font_size=24, color=YELLOW)
        power_label.next_to(power_axis.get_end(), RIGHT, buff=0.2)

        self.play(
            Create(time_axis),
            FadeIn(time_label),
            time_tracker.animate.increment_value(0.37),
            run_time=max(0.05, 0.37),
        )
        self.play(
            Create(freq_axis),
            FadeIn(freq_label),
            time_tracker.animate.increment_value(0.37),
            run_time=max(0.05, 0.37),
        )
        self.play(
            Create(power_axis),
            FadeIn(power_label),
            time_tracker.animate.increment_value(0.38),
            run_time=max(0.05, 0.38),
        )

        # ----- beat 11: 18.68-20.26 STFT label with abbreviation highlight -----
        stft_highlight = Text(
            "Short-Time Fourier Transform (STFT)",
            font_size=28,
            weight="BOLD",
            color=WHITE,
            t2c={"STFT": YELLOW},
        )
        stft_highlight.scale_to_fit_width(4.8)
        stft_highlight.move_to(np.array([3.7, 0.35, 0.0]))

        stft_neutral = Text(
            "Short-Time Fourier Transform (STFT)",
            font_size=28,
            weight="BOLD",
            color=WHITE,
        )
        stft_neutral.scale_to_fit_width(4.8)
        stft_neutral.move_to(stft_highlight.get_center())

        self.play(
            FadeIn(stft_highlight),
            time_tracker.animate.increment_value(0.90),
            run_time=max(0.05, 0.90),
        )
        self.play(
            Transform(stft_highlight, stft_neutral),
            time_tracker.animate.increment_value(0.68),
            run_time=max(0.05, 0.68),
        )

        # short beat gap before forward arrow
        self.play(time_tracker.animate.increment_value(0.50), run_time=max(0.05, 0.50))

        # ----- beat 12: 20.76-22.44 forward arrow, dim waveform and static spectrum -----
        forward_arrow = Arrow(
            stft_neutral.get_right() + RIGHT * 0.35,
            np.array([7.2, stft_neutral.get_center()[1], 0.0]),
            color=YELLOW,
            stroke_width=5,
            buff=0.0,
            max_tip_length_to_length_ratio=0.22,
        )

        self.play(
            FadeIn(forward_arrow),
            wave_dim_tracker.animate.set_value(0.35),
            wave_label.animate.set_opacity(0.5),
            spectrum_zone.animate.set_opacity(0.45),
            time_tracker.animate.increment_value(1.68),
            run_time=max(0.05, 1.68),
        )

        # ----- beat 13: 22.44-23.15 final hold -----
        self.play(time_tracker.animate.increment_value(0.71), run_time=max(0.05, 0.71))