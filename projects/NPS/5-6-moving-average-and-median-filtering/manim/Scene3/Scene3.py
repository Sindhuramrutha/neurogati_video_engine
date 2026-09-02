ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Generate a noisy time series with an upward spike.
        # ------------------------------------------------------------
        n = 100
        x_min, x_max = -5.5, 5.5
        xs = np.linspace(x_min, x_max, n)
        spacing = float(xs[1] - xs[0])

        rng = np.random.default_rng(42)
        smooth_component = 0.35 * np.sin(0.4 * xs + 0.7) + 0.2 * np.cos(0.9 * xs - 1.0)
        noise = 0.35 * rng.normal(size=n)
        y = smooth_component + noise
        y = y - np.mean(y)

        spike_idx = 65
        y[spike_idx] += 1.35

        # 5-sample moving average, full width with edge clamping.
        smooth_y = np.array([
            np.mean(y[max(0, i - 2):min(n, i + 3)])
            for i in range(n)
        ])

        # ------------------------------------------------------------
        # Plot construction: unlabeled axes + jagged light-blue trace.
        # ------------------------------------------------------------
        x_axis = Line(np.array([-6.5, -2.4, 0]), np.array([6.5, -2.4, 0]), color=GREY, stroke_width=2)
        y_axis = Line(np.array([-6.5, -2.4, 0]), np.array([-6.5, 2.4, 0]), color=GREY, stroke_width=2)
        axes = VGroup(x_axis, y_axis)

        trace_lines = VGroup(*[
            Line(np.array([xs[i], y[i], 0]), np.array([xs[i + 1], y[i + 1], 0]), color=BLUE, stroke_width=2.2)
            for i in range(n - 1)
        ])
        sample_dots = VGroup(*[
            Dot(point=np.array([xs[i], y[i], 0]), radius=0.035, fill_color=BLUE, fill_opacity=1, stroke_width=0)
            for i in range(n)
        ])
        original_trace = VGroup(trace_lines, sample_dots)
        original_trace.set_z_index(1)

        # 1. [0.00-1.68] Axes fade in, waveform is drawn.
        self.play(FadeIn(axes), Create(original_trace), run_time=max(0.05, 1.68))

        # ------------------------------------------------------------
        # Window helper + label
        # ------------------------------------------------------------
        label = Text("Window size = 5", font_size=34, color=YELLOW, weight="BOLD")
        label.move_to(np.array([0.0, 2.9, 0.0]))
        label.set_z_index(5)

        def make_window(center_idx):
            idxs = list(range(center_idx - 2, center_idx + 3))
            center_x = float(xs[center_idx])
            band = Rectangle(
                width=5 * spacing + 0.18,
                height=3.6,
                fill_color=TEAL,
                fill_opacity=0.15,
                stroke_color=TEAL,
                stroke_width=2.5,
                stroke_opacity=0.8,
            ).move_to(np.array([center_x, 0, 0]))

            dots = VGroup(*[
                Dot(
                    point=np.array([xs[i], y[i], 0]),
                    radius=0.07,
                    fill_color=YELLOW,
                    fill_opacity=1,
                    stroke_color=WHITE,
                    stroke_width=1.2,
                )
                for i in idxs
            ])
            return VGroup(band, dots).set_z_index(3)

        # 2. [1.68-3.60] First 5-sample window appears with label.
        window_group = make_window(2)
        self.play(FadeIn(window_group), FadeIn(label), run_time=max(0.05, 1.92))

        # Hold the initial window on screen before it slides.
        self.wait(max(0.05, 1.00))

        # ------------------------------------------------------------
        # 3. [4.60-6.74] Slide to spiked sample and dim the rest.
        # ------------------------------------------------------------
        window_spike = make_window(spike_idx)

        spike_dot = Dot(
            point=np.array([xs[spike_idx], y[spike_idx], 0]),
            radius=0.10,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        spike_ring = Circle(radius=0.16, color=YELLOW, stroke_width=3).move_to(spike_dot.get_center())
        spike_marker = VGroup(spike_ring, spike_dot).set_z_index(4)

        self.play(
            Transform(window_group, window_spike),
            FadeIn(spike_marker),
            original_trace.animate.set_opacity(0.35),
            run_time=max(0.05, 2.14),
        )

        self.wait(max(0.05, 0.62))

        # ------------------------------------------------------------
        # 4. [7.36-9.62] Average line and output dot for the spike window.
        # ------------------------------------------------------------
        avg_y = float(np.mean(y[spike_idx - 2:spike_idx + 3]))
        avg_line = DashedLine(
            start=np.array([xs[spike_idx - 2], avg_y, 0]),
            end=np.array([xs[spike_idx + 2], avg_y, 0]),
            color=GREY_B,
            stroke_width=2.5,
            dash_length=0.08,
        ).set_z_index(3)

        avg_dot = Dot(
            point=np.array([xs[spike_idx], avg_y, 0]),
            radius=0.09,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).set_z_index(4)

        self.play(Create(avg_line), GrowFromCenter(avg_dot), run_time=max(0.05, 1.40))
        self.wait(max(0.05, 0.86))
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------
        # 5. [10.46-11.86] Sliding window left-to-right, smoothed trace generated.
        # ------------------------------------------------------------
        smoothed_trace = VMobject(stroke_color=ORANGE, stroke_width=4.5, fill_opacity=0)
        smoothed_trace.set_points_as_corners([np.array([xs[i], smooth_y[i], 0]) for i in range(n)])
        smoothed_trace.set_z_index(2)

        window_left = make_window(2)
        window_right = make_window(n - 3)

        self.play(
            FadeOut(avg_line),
            FadeOut(avg_dot),
            FadeOut(spike_marker),
            Transform(window_group, window_left),
            run_time=max(0.05, 0.40),
        )
        self.play(
            Transform(window_group, window_right),
            Create(smoothed_trace),
            run_time=max(0.05, 1.00),
        )

        self.wait(max(0.05, 0.60))

        # ------------------------------------------------------------
        # 6. [12.46-14.48] Remove window, leave overlaid waveforms.
        # ------------------------------------------------------------
        self.play(FadeOut(window_group), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 1.42))
        self.wait(max(0.05, 0.62))

        # ------------------------------------------------------------
        # 7. [15.10-18.12] Hold steady; caption appears at 16.66.
        # ------------------------------------------------------------
        caption = Text("Figure 5.6A", font_size=26, color=GREY_B)
        caption.move_to(np.array([0.0, -3.15, 0.0]))
        caption.set_z_index(5)

        self.wait(max(0.05, 1.56))
        self.play(FadeIn(caption), run_time=max(0.05, 1.46))
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------
        # 8. [18.48-22.12] Ghost original, flash along smoothed trace, text.
        # ------------------------------------------------------------
        vis_text = Text("visibly less jagged", font_size=28, color=ORANGE)
        vis_text.move_to(np.array([4.0, 1.8, 0.0]))
        vis_text.set_z_index(5)

        self.play(original_trace.animate.set_opacity(0.12), run_time=max(0.05, 2.04))
        self.play(
            ShowPassingFlash(smoothed_trace, time_width=0.25, lag_ratio=0.05),
            FadeIn(vis_text),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 0.50))