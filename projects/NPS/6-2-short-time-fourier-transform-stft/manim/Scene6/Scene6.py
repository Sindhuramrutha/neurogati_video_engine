ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def wave_func(x):
            return 0.8 * np.sin(2.5 * x) * np.cos(0.35 * x) + 0.3 * np.sin(5.0 * x) + 0.15 * np.sin(1.2 * x)

        wave_min_x = -6.5
        wave_max_x = 6.5
        n_segments = 10
        seg_w = (wave_max_x - wave_min_x) / n_segments
        centers = [wave_min_x + (i + 0.5) * seg_w for i in range(n_segments)]
        wave_y_center = 2.4

        # Window geometry: first window from previous scene
        win_left = wave_min_x
        win_right = wave_min_x + seg_w
        win_center_x = (win_left + win_right) / 2
        win_width = seg_w * 1.05
        win_height = 2.6
        win_center_y = 2.05
        win_target = np.array([win_center_x, win_center_y, 0])

        # Full waveform
        wave = FunctionGraph(wave_func, x_range=[wave_min_x, wave_max_x])
        wave.set_stroke(WHITE, width=4)
        wave.shift(UP * wave_y_center)
        self.add(wave)

        # Step numbers at left edge, 1 brightest
        step_texts = [
            Text("1", font_size=30, color=YELLOW, weight="BOLD"),
            Text("2", font_size=30, color=GREY_C),
            Text("3", font_size=30, color=GREY_C),
            Text("4", font_size=30, color=GREY_C),
        ]
        step_texts[0].set_opacity(1)
        for t in step_texts[1:]:
            t.set_opacity(0.4)
        step_numbers = VGroup(*step_texts).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.9)

        # Beat 1: 0.00-3.92
        self.wait(max(0.05, 0.2))
        self.play(FadeIn(step_numbers), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 2.32))

        # Beat 2: 4.80-6.74 -- dim list except 1, slide window outline in
        window_rect = Rectangle(
            width=win_width,
            height=win_height,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=4,
        )
        window_rect.move_to(np.array([win_center_x - 4.0, win_center_y, 0]))

        self.wait(max(0.05, 0.88))
        self.play(
            VGroup(*step_texts[1:]).animate.set_opacity(0.2),
            step_texts[0].animate.set_opacity(1).set_color(YELLOW),
            run_time=max(0.05, 0.5),
        )
        self.add(window_rect)
        self.play(window_rect.animate.move_to(win_target), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.44))

        # Beat 3: 7.44-10.04 -- step 1 label, dim outside, pulse window, faint window-function curve
        label_y = min(win_center_y + win_height / 2 + 0.35, 3.75)
        step1_label = Text("Step 1: Select window", font_size=34, color=WHITE)
        step1_label.move_to(np.array([win_center_x, label_y, 0]))

        bright_segment = FunctionGraph(wave_func, x_range=[win_left, win_right])
        bright_segment.set_stroke(WHITE, width=6)
        bright_segment.shift(UP * wave_y_center)

        win_curve_min_y = win_center_y - win_height / 2 + 0.25
        win_curve_max_y = win_center_y + win_height / 2 - 0.25

        def hann_curve(x):
            frac = (x - win_left) / win_width
            return win_curve_min_y + (win_curve_max_y - win_curve_min_y) * (
                0.5 * (1 - np.cos(2 * np.pi * frac))
            )

        window_curve = FunctionGraph(hann_curve, x_range=[win_left, win_right])
        window_curve.set_stroke(YELLOW, width=2, opacity=0.55)

        self.wait(max(0.05, 0.7))
        self.play(FadeIn(step1_label), run_time=max(0.05, 0.5))
        self.play(
            wave.animate.set_color(GREY_C).set_stroke(width=2),
            FadeIn(bright_segment),
            run_time=max(0.05, 0.7),
        )
        self.play(window_rect.animate.scale(1.1), run_time=max(0.05, 0.35))
        self.play(window_rect.animate.scale(1 / 1.1), run_time=max(0.05, 0.35))
        self.play(FadeIn(window_curve), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.25))

        # Beat 4: 10.50-13.14 -- isolate windowed segment further
        self.wait(max(0.05, 0.46))
        self.play(
            bright_segment.animate.set_stroke(color=YELLOW, width=7),
            wave.animate.set_color(GREY_D).set_stroke(width=1.6).set_opacity(0.7),
            window_rect.animate.set_stroke(width=5),
            run_time=max(0.05, 0.8),
        )
        self.play(window_rect.animate.scale(1.06), run_time=max(0.05, 0.5))
        self.play(window_rect.animate.scale(1 / 1.06), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.84))

        # Beat 5: 14.30-16.26 -- split into left window view and enlarged right extract
        L_center = np.array([-4.5, 1.0, 0])
        R_center = np.array([4.5, 1.0, 0])
        step1_label_target = np.array([L_center[0], L_center[1] + win_height / 2 + 0.35, 0])

        left_window_group = VGroup(window_rect, bright_segment, window_curve)
        shift_to_left = L_center - window_rect.get_center()

        right_extract = bright_segment.copy()
        right_extract.set_stroke(color=YELLOW, width=6)
        right_extract.move_to(bright_segment.get_center())
        self.add(right_extract)

        step2_label = Text("Step 2: Apply Fourier Transform", font_size=34, color=WHITE)
        step2_label.move_to(np.array([4.5, -1.55, 0]))

        self.wait(max(0.05, 1.16))
        self.play(
            FadeOut(wave),
            left_window_group.animate.shift(shift_to_left),
            step1_label.animate.move_to(step1_label_target),
            right_extract.animate.move_to(R_center).scale(1.6),
            FadeIn(step2_label),
            run_time=max(0.05, 1.96),
        )

        # Beat 6: 17.04-19.28 -- small Fourier Transform icon above right extract
        def make_fourier_icon():
            icon = VGroup()
            time_wave = FunctionGraph(lambda x: 0.3 * np.sin(7 * x), x_range=[-0.9, -0.2])
            time_wave.set_stroke(YELLOW, width=4)
            arrow = Arrow(
                start=np.array([-0.1, 0, 0]),
                end=np.array([0.3, 0, 0]),
                buff=0,
                color=YELLOW,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.3,
            )
            baseline = Line(np.array([0.4, -0.1, 0]), np.array([1.1, -0.1, 0]), color=YELLOW, stroke_width=2)
            peak_xs = [0.45, 0.62, 0.79, 0.96]
            peak_heights = [0.25, 0.5, 0.75, 0.45]
            peaks = VGroup()
            for px, ph in zip(peak_xs, peak_heights):
                bar = Rectangle(width=0.1, height=ph, fill_color=YELLOW, fill_opacity=0.85, stroke_width=0)
                bar.move_to(np.array([px, -0.1 + ph / 2, 0]))
                peaks.add(bar)
            icon.add(time_wave, arrow, baseline, peaks)
            icon.scale_to_fit_width(3.2)
            icon.move_to(np.array([4.5, 3.2, 0]))
            return icon

        fourier_icon = make_fourier_icon()

        self.wait(max(0.05, 0.78))
        self.play(Write(fourier_icon), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.04))

        # Beat 7: 19.28-21.06 -- small spectrum plot below right extract and Fourier icon
        spec_center = np.array([4.5, -2.8, 0])
        spec_width = 3.6
        spec_height = 1.5
        spec_left = spec_center[0] - spec_width / 2
        spec_right = spec_center[0] + spec_width / 2
        spec_bottom = spec_center[1] - spec_height / 2
        spec_top = spec_center[1] + spec_height / 2

        bottom_axis = Line(
            np.array([spec_left, spec_bottom, 0]),
            np.array([spec_right, spec_bottom, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        left_axis = Line(
            np.array([spec_left, spec_bottom, 0]),
            np.array([spec_left, spec_top, 0]),
            color=GREY_B,
            stroke_width=3,
        )

        heights = [0.45, 0.8, 0.3, 0.65, 0.2, 0.5]
        n_spec_points = 180
        curve_xs = np.linspace(spec_left, spec_right, n_spec_points)
        peak_xs = np.linspace(spec_left + 0.15 * spec_width, spec_right - 0.15 * spec_width, len(heights))
        sigma = 0.07 * spec_width
        components = [
            h * np.exp(-((curve_xs - px) / sigma) ** 2)
            for px, h in zip(peak_xs, heights)
        ]
        full_raw = np.sum(components, axis=0)
        max_raw = full_raw.max()

        baseline_y = spec_bottom + 0.08 * spec_height
        top_y = spec_top - 0.08 * spec_height

        def render_spectrum_curve(raw_values, color, stroke_width):
            norm_values = raw_values / max_raw
            ys = baseline_y + norm_values * (top_y - baseline_y)
            curve = VMobject()
            curve.set_points_as_corners(
                [np.array([curve_xs[i], ys[i], 0]) for i in range(n_spec_points)]
            )
            curve.set_stroke(color=color, width=stroke_width)
            curve.set_fill(opacity=0)
            return curve

        base_curve = render_spectrum_curve(full_raw, GREY_C, 3)
        peak1_curve = render_spectrum_curve(components[1], YELLOW, 7).set_opacity(0)
        peak2_curve = render_spectrum_curve(components[3], YELLOW, 6).set_opacity(0)

        spec_plot = VGroup(bottom_axis, left_axis, base_curve, peak1_curve, peak2_curve)

        self.play(FadeIn(spec_plot), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.58))

        # Beat 8: 21.06-24.70 -- highlight the two dominant peaks one after another
        self.play(peak1_curve.animate.set_opacity(1), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.4))
        self.play(peak2_curve.animate.set_opacity(1), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.64))