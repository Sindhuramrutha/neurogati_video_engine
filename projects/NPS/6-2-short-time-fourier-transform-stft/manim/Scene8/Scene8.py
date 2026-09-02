ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- Geometry ----------
        panel_width = 6.0
        panel_height = 5.8
        panel_center_y = 0.2
        left_panel_x = -3.3
        right_panel_x = 3.3

        top_center_y = 1.55
        lower_center_y = -1.25
        signal_half_width = 2.7
        signal_scale = 1.05

        window_y = top_center_y
        narrow_width = 0.8
        wide_width = 2.8
        window_height = 2.2
        bright_half = 0.4

        burst_center_x = left_panel_x

        # ---------- Panels ----------
        left_panel_rect = Rectangle(
            width=panel_width,
            height=panel_height,
            color=GREY_B,
            stroke_width=2.0,
            fill_color=GREY,
            fill_opacity=0.10,
        )
        left_panel_rect.move_to(np.array([left_panel_x, panel_center_y, 0]))

        right_panel_rect = Rectangle(
            width=panel_width,
            height=panel_height,
            color=GREY_B,
            stroke_width=2.0,
            fill_color=GREY,
            fill_opacity=0.10,
        )
        right_panel_rect.move_to(np.array([right_panel_x, panel_center_y, 0]))

        left_divider = Line(
            np.array([left_panel_x - panel_width / 2, panel_center_y, 0]),
            np.array([left_panel_x + panel_width / 2, panel_center_y, 0]),
            color=GREY_B,
            stroke_width=2,
        )
        right_divider = Line(
            np.array([right_panel_x - panel_width / 2, panel_center_y, 0]),
            np.array([right_panel_x + panel_width / 2, panel_center_y, 0]),
            color=GREY_B,
            stroke_width=2,
        )

        panels = VGroup(left_panel_rect, right_panel_rect, left_divider, right_divider)
        self.add(panels)

        # ---------- Signal ----------
        def signal_shape(local_x):
            low = 0.13 * np.sin(2 * np.pi * 0.75 * local_x)
            burst = 0.52 * np.sin(2 * np.pi * 3.0 * local_x) * np.exp(-((local_x) / 0.28) ** 2)
            return low + burst

        def left_signal_y(x):
            local_x = x - left_panel_x
            return top_center_y + signal_scale * signal_shape(local_x)

        def right_signal_y(x):
            local_x = x - right_panel_x
            return top_center_y + signal_scale * signal_shape(local_x)

        left_signal = FunctionGraph(
            left_signal_y,
            x_range=[left_panel_x - signal_half_width, left_panel_x + signal_half_width],
        )
        left_signal.set_stroke(color=TEAL, width=3)

        right_signal = FunctionGraph(
            right_signal_y,
            x_range=[right_panel_x - signal_half_width, right_panel_x + signal_half_width],
        )
        right_signal.set_stroke(color=TEAL, width=3)

        # ---------- Windows ----------
        narrow_window = Rectangle(
            width=narrow_width,
            height=window_height,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=4,
        )
        narrow_window.move_to(np.array([left_panel_x, window_y, 0]))

        wide_window = Rectangle(
            width=wide_width,
            height=window_height,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=4,
        )
        wide_window.move_to(np.array([right_panel_x, window_y, 0]))

        # Bright segment inside the narrow window
        def make_left_bright(wx, opacity, sw):
            seg = FunctionGraph(
                left_signal_y,
                x_range=[wx - bright_half, wx + bright_half],
            )
            seg.set_stroke(color=YELLOW, width=sw, opacity=opacity)
            return seg

        current_left_bright = make_left_bright(burst_center_x, opacity=0.0, sw=6)
        self.add(current_left_bright)

        # ---------- Frequency spectrums ----------
        def make_spectrum_curve(cx, cy, w, h, peaks, color, sw):
            n_points = 300
            xs = np.linspace(cx - w / 2, cx + w / 2, n_points)
            baseline_y = cy - h / 2 + 0.10 * h
            top_y = cy + h / 2 - 0.10 * h
            raw = np.zeros(n_points)
            for px_local, amp, sig in peaks:
                px = cx + px_local * (w / 2)
                raw += amp * np.exp(-((xs - px) / sig) ** 2)

            raw_max = raw.max() if raw.size else 1
            if raw_max > 0:
                ys = baseline_y + (raw / raw_max) * (top_y - baseline_y)
            else:
                ys = np.full(n_points, baseline_y)

            curve = VMobject()
            curve.set_points_as_corners([np.array([xs[i], ys[i], 0]) for i in range(n_points)])
            curve.set_stroke(color=color, width=sw)
            curve.set_fill(opacity=0)
            return curve, xs, ys

        def make_spectrum_axes(cx, cy, w, h):
            bottom = Line(
                np.array([cx - w / 2, cy - h / 2, 0]),
                np.array([cx + w / 2, cy - h / 2, 0]),
                color=GREY_B,
                stroke_width=2.5,
            )
            left_axis = Line(
                np.array([cx - w / 2, cy - h / 2, 0]),
                np.array([cx - w / 2, cy + h / 2, 0]),
                color=GREY_B,
                stroke_width=2.5,
            )
            return VGroup(bottom, left_axis)

        broad_peaks = [
            (-0.66, 0.65, 0.60),
            (-0.30, 0.45, 0.45),
            (0.05, 0.70, 0.55),
            (0.35, 0.55, 0.50),
            (0.70, 0.50, 0.65),
        ]
        sharp_peaks = [
            (-0.60, 0.50, 0.12),
            (-0.15, 0.75, 0.10),
            (0.25, 0.95, 0.12),
            (0.60, 0.55, 0.10),
        ]

        left_spectrum_axes = make_spectrum_axes(left_panel_x, lower_center_y, 4.6, 1.6)
        left_broad_curve, left_xs, left_ys = make_spectrum_curve(
            left_panel_x, lower_center_y, 4.6, 1.6, broad_peaks, ORANGE, 6
        )
        left_spectrum_group = VGroup(left_spectrum_axes, left_broad_curve)

        right_spectrum_axes = make_spectrum_axes(right_panel_x, lower_center_y, 4.6, 1.6)
        right_sharp_curve, right_xs, right_ys = make_spectrum_curve(
            right_panel_x, lower_center_y, 4.6, 1.6, sharp_peaks, BLUE, 6
        )
        right_spectrum_group = VGroup(right_spectrum_axes, right_sharp_curve)

        right_peak_idx = int(np.argmax(right_ys))
        right_peak_point = np.array([right_xs[right_peak_idx], right_ys[right_peak_idx], 0])
        right_peak_dot = Dot(point=right_peak_point, radius=0.07, color=WHITE)

        left_spectrum_glow = SurroundingRectangle(
            left_broad_curve,
            color=YELLOW,
            buff=0.22,
            fill_color=YELLOW,
            fill_opacity=0.05,
            stroke_width=3,
        )

        uncertainty_band = Rectangle(
            width=1.8,
            height=2.4,
            fill_color=PINK,
            fill_opacity=0.18,
            stroke_width=0,
        )
        uncertainty_band.move_to(np.array([right_panel_x, top_center_y, 0]))

        # ---------- Beat 1: 0.00-3.50 ----------
        self.play(FadeIn(left_signal, right_signal), run_time=max(0.05, 1.3))
        self.wait(max(0.05, 0.7))
        self.play(FadeIn(narrow_window, wide_window), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.7))

        # Gap to 4.26
        self.wait(max(0.05, 0.76))

        # ---------- Beat 2: 4.26-7.52 ----------
        self.play(
            narrow_window.animate.set_stroke(width=6, color=YELLOW).set_fill(opacity=0.25),
            wide_window.animate.set_stroke(width=6, color=YELLOW).set_fill(opacity=0.25),
            run_time=max(0.05, 0.5),
        )

        for _ in range(2):
            off_seg = make_left_bright(burst_center_x - 0.22, opacity=0.25, sw=6)
            self.play(
                narrow_window.animate.move_to(np.array([burst_center_x - 0.22, window_y, 0])),
                Transform(current_left_bright, off_seg),
                run_time=max(0.05, 0.42),
                rate_func=linear,
            )
            current_left_bright = off_seg

            off_seg = make_left_bright(burst_center_x + 0.22, opacity=0.25, sw=6)
            self.play(
                narrow_window.animate.move_to(np.array([burst_center_x + 0.22, window_y, 0])),
                Transform(current_left_bright, off_seg),
                run_time=max(0.05, 0.42),
                rate_func=linear,
            )
            current_left_bright = off_seg

            center_seg = make_left_bright(burst_center_x, opacity=1.0, sw=10)
            self.play(
                narrow_window.animate.move_to(np.array([burst_center_x, window_y, 0])),
                Transform(current_left_bright, center_seg),
                run_time=max(0.05, 0.30),
                rate_func=linear,
            )
            current_left_bright = center_seg

            self.play(
                current_left_bright.animate.set_stroke(opacity=0.25, width=6),
                run_time=max(0.05, 0.24),
            )

        # Gap to 8.38
        self.wait(max(0.05, 0.86))

        # ---------- Beat 3: 8.38-13.50 ----------
        away_seg = make_left_bright(burst_center_x + 0.20, opacity=0.25, sw=6)
        self.play(
            narrow_window.animate.move_to(np.array([burst_center_x + 0.20, window_y, 0])),
            Transform(current_left_bright, away_seg),
            run_time=max(0.05, 0.4),
            rate_func=linear,
        )
        current_left_bright = away_seg

        final_center_seg = make_left_bright(burst_center_x, opacity=1.0, sw=11)
        self.play(
            narrow_window.animate.move_to(np.array([burst_center_x, window_y, 0])),
            Transform(current_left_bright, final_center_seg),
            FadeIn(left_spectrum_group),
            run_time=max(0.05, 0.6),
            rate_func=linear,
        )
        current_left_bright = final_center_seg

        self.play(
            current_left_bright.animate.set_stroke(opacity=0.25, width=6),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 3.72))

        # Gap to 14.24
        self.wait(max(0.05, 0.74))

        # ---------- Beat 4: 14.24-18.24 ----------
        self.play(FadeIn(left_spectrum_glow), run_time=max(0.05, 0.7))
        self.play(Indicate(narrow_window, scale_factor=1.1, color=YELLOW), run_time=max(0.05, 0.7))
        self.play(
            left_spectrum_glow.animate.set_fill(opacity=0.14).set_stroke(width=5),
            run_time=max(0.05, 1.0),
        )
        self.play(
            left_spectrum_glow.animate.set_fill(opacity=0.07).set_stroke(width=3),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.6))

        # Gap to 19.20
        self.wait(max(0.05, 0.96))

        # ---------- Beat 5: 19.20-24.10 ----------
        self.play(
            FadeIn(right_spectrum_group),
            wide_window.animate.set_stroke(width=7, color=YELLOW).set_fill(opacity=0.30),
            run_time=max(0.05, 1.4),
        )
        self.play(FadeIn(uncertainty_band), run_time=max(0.05, 1.0))
        self.play(uncertainty_band.animate.set_fill(opacity=0.32), run_time=max(0.05, 0.5))
        self.play(uncertainty_band.animate.set_fill(opacity=0.18), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.5))

        # Gap to 25.04
        self.wait(max(0.05, 0.94))

        # ---------- Beat 6: 25.04-28.82 ----------
        self.play(
            narrow_window.animate.set_stroke(color=WHITE, width=8),
            GrowFromCenter(right_peak_dot),
            uncertainty_band.animate.set_fill(opacity=0.32),
            run_time=max(0.05, 0.7),
        )
        self.play(
            narrow_window.animate.set_stroke(color=YELLOW, width=6),
            uncertainty_band.animate.set_fill(opacity=0.18),
            run_time=max(0.05, 0.7),
        )
        self.play(Indicate(right_peak_dot, scale_factor=2.0, color=WHITE), run_time=max(0.05, 0.6))
        self.play(FadeOut(right_peak_dot), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 1.48))

        # ---------- Beat 7: 28.82-29.68 ----------
        left_label = Text(
            "Small window: good time, poor frequency",
            font_size=26,
            color=WHITE,
            t2c={"good time": YELLOW, "poor frequency": GREY_B},
        )
        left_label.scale_to_fit_width(5.6)
        left_label.next_to(left_panel_rect, DOWN, buff=0.15)

        right_label = Text(
            "Large window: good frequency, poor time",
            font_size=26,
            color=WHITE,
            t2c={"good frequency": YELLOW, "poor time": GREY_B},
        )
        right_label.scale_to_fit_width(5.6)
        right_label.next_to(right_panel_rect, DOWN, buff=0.15)

        self.play(FadeIn(left_label, right_label), run_time=max(0.05, 0.86))