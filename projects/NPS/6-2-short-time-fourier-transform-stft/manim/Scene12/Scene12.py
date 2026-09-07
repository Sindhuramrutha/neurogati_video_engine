ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene12(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Coordinates / functions
        # ------------------------------------------------------------
        slow_freq = 0.5
        slow_amp = 0.6
        spike_center = 6.5

        def slow_func(x):
            return slow_amp * np.sin(2 * PI * slow_freq * x)

        def spike_func(x):
            return 1.15 * np.exp(-((x - spike_center) ** 2) / (2 * 0.16 ** 2))

        def full_func(x):
            return slow_func(x) + spike_func(x)

        def blurred_spike_func(x):
            return 0.6 * np.exp(-((x - spike_center) ** 2) / (2 * 0.95 ** 2))

        def make_curve(func, x_min, x_max, color=WHITE, stroke_w=3, n=400):
            pts = [
                axes.coords_to_point(x, func(x))
                for x in np.linspace(x_min, x_max, n)
            ]
            curve = VMobject(stroke_color=color, stroke_width=stroke_w)
            curve.set_points_as_corners(pts)
            return curve

        # ------------------------------------------------------------
        # Main warning card layout
        # ------------------------------------------------------------
        card = RoundedRectangle(
            width=7.4,
            height=5.6,
            corner_radius=0.2,
            fill_color=MAROON,
            fill_opacity=0.2,
            stroke_color=ORANGE,
            stroke_width=4,
        ).move_to(np.array([-2.2, 0.0, 0.0]))
        card.set_z_index(-10)

        title = Text("Limitations", font_size=46, color=YELLOW, weight=BOLD)
        title.move_to(card.get_top() + DOWN * 0.65)

        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[-1.4, 2.0, 0.5],
            x_length=6.2,
            y_length=2.4,
            axis_config={"color": GREY_B, "stroke_width": 2},
            x_axis_config={"include_numbers": False, "include_ticks": False},
            y_axis_config={"include_numbers": False, "include_ticks": False},
        ).move_to(np.array([-2.2, -0.1, 0.0]))
        axes.set_z_index(-5)

        full_curve = make_curve(full_func, 0, 12, color=WHITE, stroke_w=3, n=600)
        full_curve.set_z_index(3)

        # ------------------------------------------------------------
        # BEAT 1: 0.00 - 4.38
        # ------------------------------------------------------------
        self.play(FadeIn(card), run_time=max(0.05, 0.8))
        self.play(Write(title), run_time=max(0.05, 0.6))
        self.play(Create(full_curve), run_time=max(0.05, 2.6))
        self.wait(max(0.05, 0.38))

        # ------------------------------------------------------------
        # BEAT 2: 4.38 - 6.40  -- wide fixed window
        # ------------------------------------------------------------
        fixed_window_left = axes.coords_to_point(1.2, 0)
        fixed_window_right = axes.coords_to_point(5.2, 0)
        fixed_window_width = fixed_window_right[0] - fixed_window_left[0]
        fixed_window = Rectangle(
            width=fixed_window_width,
            height=3.0,
            stroke_color=YELLOW,
            stroke_width=5,
            fill_color=YELLOW,
            fill_opacity=0.15,
        ).move_to(axes.coords_to_point(3.2, 0))
        fixed_window.set_z_index(1)

        self.play(
            GrowFromCenter(fixed_window),
            card.animate.set_stroke(color=ORANGE, width=6),
            run_time=max(0.05, 2.02),
        )

        # ------------------------------------------------------------
        # GAP: 6.40 - 7.04
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.64))

        # ------------------------------------------------------------
        # BEAT 3: 7.04 - 8.84  -- focused edges + side-by-side attempts
        # ------------------------------------------------------------
        self.play(Indicate(fixed_window, scale_factor=1.05, color=YELLOW), run_time=max(0.05, 0.4))

        edge_left = Line(
            axes.coords_to_point(1.2, -1.2),
            axes.coords_to_point(1.2, 1.8),
            color=ORANGE,
            stroke_width=8,
        )
        edge_right = Line(
            axes.coords_to_point(5.2, -1.2),
            axes.coords_to_point(5.2, 1.8),
            color=ORANGE,
            stroke_width=8,
        )
        window_edges = VGroup(edge_left, edge_right)
        window_edges.set_z_index(5)
        self.play(Create(window_edges), run_time=max(0.05, 0.4))

        def make_mini_panel(kind, center_pos):
            mini_axes = Axes(
                x_range=[0, 4, 1],
                y_range=[-1.2, 1.5, 0.5],
                x_length=1.7,
                y_length=1.0,
                axis_config={"color": GREY, "stroke_width": 2},
                x_axis_config={"include_numbers": False, "include_ticks": False},
                y_axis_config={"include_numbers": False, "include_ticks": False},
            ).move_to(center_pos)

            if kind == "slow":
                mini_func = lambda x: 0.7 * np.sin(2 * PI * 1.2 * x)
                curve_color = TEAL
            else:
                mini_func = lambda x: 1.0 * np.exp(-((x - 2.0) ** 2) / (2 * 0.15 ** 2))
                curve_color = PINK

            pts = [
                mini_axes.coords_to_point(x, mini_func(x))
                for x in np.linspace(0.4, 3.6, 160)
            ]
            mini_curve = VMobject(stroke_color=curve_color, stroke_width=3)
            mini_curve.set_points_as_corners(pts)

            mini_bg = RoundedRectangle(
                width=2.1,
                height=1.5,
                corner_radius=0.1,
                fill_color=GREY_B,
                fill_opacity=0.18,
                stroke_color=GREY,
                stroke_width=2,
            ).move_to(center_pos)

            mini_left = mini_axes.coords_to_point(1.2, -0.6)
            mini_right = mini_axes.coords_to_point(2.8, 0.8)
            mini_window = Rectangle(
                width=mini_right[0] - mini_left[0],
                height=1.0,
                stroke_color=YELLOW,
                stroke_width=3,
                fill_color=YELLOW,
                fill_opacity=0.2,
            ).move_to(mini_axes.coords_to_point(2.0, 0))

            return VGroup(mini_bg, mini_axes, mini_curve, mini_window)

        mini_slow = make_mini_panel("slow", np.array([2.8, 0.6, 0.0]))
        mini_spike = make_mini_panel("spike", np.array([5.1, 0.6, 0.0]))
        mini_slow.set_z_index(6)
        mini_spike.set_z_index(6)

        self.play(FadeIn(mini_slow), FadeIn(mini_spike), run_time=max(0.05, 1.0))

        # ------------------------------------------------------------
        # GAP: 8.84 - 9.28
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.44))

        # ------------------------------------------------------------
        # BEAT 4: 9.28 - 12.10  -- high frequency resolution, blurred transient
        # ------------------------------------------------------------
        self.play(FadeOut(mini_slow), FadeOut(mini_spike), run_time=max(0.05, 0.4))

        inside_curve = make_curve(slow_func, 1.2, 5.2, color=GREEN, stroke_w=5, n=260)
        inside_curve.set_z_index(4)
        self.play(Create(inside_curve), run_time=max(0.05, 1.2))

        smeared_spike = make_curve(
            blurred_spike_func, 4.5, 8.5, color=PINK, stroke_w=10, n=300
        )
        smeared_spike.set_z_index(5)
        self.play(FadeIn(smeared_spike), run_time=max(0.05, 0.8))

        high_freq_label = Text(
            "High frequency resolution", font_size=26, color=GREEN
        )
        high_freq_label.next_to(fixed_window, DOWN, buff=0.25)
        self.play(Write(high_freq_label), run_time=max(0.05, 0.42))

        # ------------------------------------------------------------
        # BEAT 5: 12.10 - 14.20  -- high time resolution dashed window
        # ------------------------------------------------------------
        narrow_data_left = axes.coords_to_point(6.0, 0)
        narrow_data_right = axes.coords_to_point(7.0, 0)
        narrow_rect = Rectangle(
            width=narrow_data_right[0] - narrow_data_left[0],
            height=3.0,
            stroke_color=PINK,
            stroke_width=4,
            fill_color=PINK,
            fill_opacity=0.12,
        ).move_to(axes.coords_to_point(6.5, 0))
        narrow_window = DashedVMobject(narrow_rect, num_dashes=22)
        narrow_window.set_z_index(6)

        self.play(FadeIn(narrow_window), run_time=max(0.05, 0.5))

        time_res_label = Text("High time resolution", font_size=26, color=PINK)
        time_res_label.next_to(narrow_window, UP, buff=0.3)
        self.play(Write(time_res_label), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.55))
        self.play(FadeOut(narrow_window), FadeOut(time_res_label), run_time=max(0.05, 0.55))

        # ------------------------------------------------------------
        # GAP: 14.20 - 15.10
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.90))

        # ------------------------------------------------------------
        # BEAT 6: 15.10 - 17.38  -- zoom into smeared transient
        # ------------------------------------------------------------
        timestamp_text = Text("██:██:██", font_size=24, color=PINK)
        timestamp_text.set_opacity(0.55)
        timestamp_text.move_to(axes.coords_to_point(6.5, -1.2))

        timestamp_line = Line(
            axes.coords_to_point(5.7, -1.35),
            axes.coords_to_point(7.3, -1.35),
            color=PINK,
            stroke_width=4,
        )
        timestamp_line.set_opacity(0.55)

        self.play(
            fixed_window.animate.move_to(axes.coords_to_point(6.5, 0)),
            FadeOut(high_freq_label),
            FadeOut(window_edges),
            FadeIn(timestamp_text),
            FadeIn(timestamp_line),
            run_time=max(0.05, 0.7),
        )
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(axes.coords_to_point(6.5, 0.1)),
            run_time=max(0.05, 1.58),
        )

        # ------------------------------------------------------------
        # BEAT 7: 17.38 - 19.04  -- "Neural signals" label
        # ------------------------------------------------------------
        neural_label = Text("Neural signals", font_size=32, color=WHITE)
        frame_top = self.camera.frame.get_center() + UP * (
            self.camera.frame.get_height() / 2 - 0.6
        )
        neural_label.move_to(frame_top)
        neural_label.set_z_index(10)

        self.play(FadeIn(neural_label, shift=UP * 0.2), run_time=max(0.05, 0.6))
        self.play(Indicate(smeared_spike, color=PINK, scale_factor=1.1), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.46))

        # ------------------------------------------------------------
        # BEAT 8: 19.04 - 21.24  -- pull back, show both components
        # ------------------------------------------------------------
        self.play(
            self.camera.frame.animate.scale(1.5).move_to(axes.coords_to_point(4.2, 0.1)),
            run_time=max(0.05, 1.2),
        )

        slow_label = Text("Slow oscillations", font_size=28, color=TEAL)
        slow_label.move_to(axes.coords_to_point(3.0, 1.6))
        arrow_slow = Arrow(
            start=slow_label.get_bottom(),
            end=axes.coords_to_point(2.5, slow_func(2.5)),
            buff=0.1,
            color=TEAL,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.08,
        )
        self.play(Write(slow_label), Create(arrow_slow), run_time=max(0.05, 1.0))

        # ------------------------------------------------------------
        # BEAT 9: 21.24 - 22.70  -- same fixed window over rapid transient
        # ------------------------------------------------------------
        self.play(Indicate(fixed_window, scale_factor=1.05, color=YELLOW), run_time=max(0.05, 0.5))

        rapid_label = Text("Rapid transient events", font_size=28, color=PINK)
        rapid_label.move_to(axes.coords_to_point(9.0, 1.7))
        arrow_rapid = Arrow(
            start=rapid_label.get_bottom(),
            end=axes.coords_to_point(6.5, 0.5),
            buff=0.1,
            color=PINK,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.08,
        )
        self.play(Write(rapid_label), Create(arrow_rapid), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.41))

        # ------------------------------------------------------------
        # GAP: 22.70 - 23.60  -- reset camera before wavelet region
        # ------------------------------------------------------------
        stale_group = VGroup(
            neural_label,
            slow_label,
            arrow_slow,
            rapid_label,
            arrow_rapid,
            timestamp_text,
            timestamp_line,
        )
        self.play(FadeOut(stale_group), run_time=max(0.05, 0.4))
        self.play(
            self.camera.frame.animate.scale(1.333).move_to(ORIGIN),
            run_time=max(0.05, 0.5),
        )

        # ------------------------------------------------------------
        # BEAT 10: 23.60 - 25.74  -- wavelet diagram appears
        # ------------------------------------------------------------
        wavelet_panel = RoundedRectangle(
            width=3.4,
            height=2.8,
            corner_radius=0.15,
            fill_color=TEAL,
            fill_opacity=0.1,
            stroke_color=TEAL,
            stroke_width=3,
        ).move_to(np.array([3.8, 0.2, 0.0]))

        wavelet_pts = []
        for u in np.linspace(-1.6, 1.6, 320):
            y = np.cos(2 * PI * 1.8 * u) * np.exp(-(u ** 2) / (2 * 0.3 ** 2))
            wavelet_pts.append(
                np.array([3.8 + u * 0.9, 0.2 + y * 0.75, 0.0])
            )
        wavelet_curve = VMobject(stroke_color=TEAL, stroke_width=3)
        wavelet_curve.set_points_as_corners(wavelet_pts)
        wavelet_curve.set_z_index(5)

        self.play(FadeIn(wavelet_panel), run_time=max(0.05, 0.7))
        self.play(Create(wavelet_curve), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.44))

        # ------------------------------------------------------------
        # BEAT 11: 25.74 - 27.28  -- "Wavelet analysis" + moving/stretching wavelet
        # ------------------------------------------------------------
        wavelet_text = Text("Wavelet analysis", font_size=30, color=TEAL)
        wavelet_text.next_to(wavelet_panel, DOWN, buff=0.35)

        moving_wavelet = wavelet_curve.copy()
        moving_wavelet.set_color(YELLOW).set_stroke(width=4)
        moving_wavelet.set_z_index(20)

        self.play(FadeIn(wavelet_text), run_time=max(0.05, 0.5))

        self.play(
            moving_wavelet.animate.move_to(axes.coords_to_point(3.2, 0.3))
            .scale_to_fit_width(1.8),
            run_time=max(0.05, 0.5),
        )
        self.play(
            moving_wavelet.animate.move_to(axes.coords_to_point(6.5, 0.5))
            .scale_to_fit_width(0.45),
            run_time=max(0.05, 0.54),
        )

        # ------------------------------------------------------------
        # BEAT 12: 27.28 - 29.57  -- wavelet settles, sharp localization
        # ------------------------------------------------------------
        sharp_localized = make_curve(
            lambda x: 0.85 * np.exp(-((x - 6.5) ** 2) / (2 * 0.12 ** 2)),
            6.0,
            7.0,
            color=YELLOW,
            stroke_w=5,
            n=140,
        )
        sharp_localized.set_z_index(7)

        self.play(
            FadeOut(smeared_spike),
            FadeIn(sharp_localized),
            run_time=max(0.05, 0.7),
        )
        self.play(
            Indicate(moving_wavelet, color=YELLOW, scale_factor=1.1),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 0.99))