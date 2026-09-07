ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Data: reuse the same noisy signal with a spike as Scene 3
        # ------------------------------------------------------------------
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

        # Moving averages – edge-clamped
        smooth_y5 = np.array([
            np.mean(y[max(0, i - 2):min(n, i + 3)]) for i in range(n)
        ])
        smooth_y25 = np.array([
            np.mean(y[max(0, i - 12):min(n, i + 13)]) for i in range(n)
        ])

        # ------------------------------------------------------------------
        # Axes – unlabelled, identical for left and right
        # ------------------------------------------------------------------
        left_axes = Axes(
            x_range=[-5.5, 5.5, 1],
            y_range=[-2.5, 2.5, 0.5],
            x_length=6,
            y_length=4.5,
            axis_config={"include_numbers": False, "include_ticks": False,
                         "stroke_color": GREY, "stroke_width": 2},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False,
        ).move_to(np.array([-3.5, 0, 0]))

        right_axes = Axes(
            x_range=[-5.5, 5.5, 1],
            y_range=[-2.5, 2.5, 0.5],
            x_length=6,
            y_length=4.5,
            axis_config={"include_numbers": False, "include_ticks": False,
                         "stroke_color": GREY, "stroke_width": 2},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False,
        ).move_to(np.array([3.5, 0, 0]))

        # Thin vertical divider
        divider = DashedLine(
            np.array([0, -3.2, 0]), np.array([0, 3.2, 0]),
            color=GREY, stroke_width=1.5, dash_length=0.12
        )

        # ------------------------------------------------------------------
        # Original traces (light‑blue, jagged)
        # ------------------------------------------------------------------
        left_orig = VMobject(stroke_color=BLUE, stroke_width=1.5).set_points_as_corners(
            [left_axes.c2p(xs[i], y[i]) for i in range(n)]
        )
        right_orig = VMobject(stroke_color=BLUE, stroke_width=1.5).set_points_as_corners(
            [right_axes.c2p(xs[i], y[i]) for i in range(n)]
        )

        # ------------------------------------------------------------------
        # Plot spacing for band widths
        # ------------------------------------------------------------------
        plot_spacing_left = left_axes.x_length / (n - 1)
        plot_spacing_right = right_axes.x_length / (n - 1)

        # ------------------------------------------------------------------
        # Left side: window size 5
        # ------------------------------------------------------------------
        left_band_width = 4 * plot_spacing_left
        left_band = Rectangle(
            width=left_band_width,
            height=left_axes.y_length,
            fill_color=TEAL, fill_opacity=0.15,
            stroke_color=TEAL, stroke_width=2.5, stroke_opacity=0.8,
        ).set_z_index(3)
        left_smooth = VMobject(stroke_color=ORANGE, stroke_width=4.5,
                               fill_opacity=0).set_z_index(2)
        left_tracker = ValueTracker(2)  # first full 5‑sample window centre

        left_band.add_updater(
            lambda m: m.move_to(left_axes.c2p(xs[int(left_tracker.get_value())], 0))
        )
        left_smooth.add_updater(
            lambda m: m.set_points_as_corners(
                [left_axes.c2p(xs[i], smooth_y5[i]) for i in range(int(left_tracker.get_value()) + 1)]
            )
        )

        left_label = Text("Window size = 5", font_size=30, color=YELLOW, weight="BOLD")
        left_label.next_to(left_axes, UP, buff=0.4)

        # ------------------------------------------------------------------
        # Right side: window size 25
        # ------------------------------------------------------------------
        right_band_width = 24 * plot_spacing_right
        right_band = Rectangle(
            width=right_band_width,
            height=right_axes.y_length,
            fill_color=TEAL, fill_opacity=0.15,
            stroke_color=TEAL, stroke_width=2.5, stroke_opacity=0.8,
        ).set_z_index(3)
        right_smooth = VMobject(stroke_color=MAROON, stroke_width=5,
                                fill_opacity=0).set_z_index(2)
        right_tracker = ValueTracker(12)  # first full 25‑sample window centre

        right_band.add_updater(
            lambda m: m.move_to(right_axes.c2p(xs[int(right_tracker.get_value())], 0))
        )
        right_smooth.add_updater(
            lambda m: m.set_points_as_corners(
                [right_axes.c2p(xs[i], smooth_y25[i]) for i in range(int(right_tracker.get_value()) + 1)]
            )
        )

        right_label = Text("Window size = 25", font_size=30, color=YELLOW, weight="BOLD")
        right_label.next_to(right_axes, UP, buff=0.4)

        # ==================================================================
        # BEAT 1  [0.00 – 1.36]  Fade in split view
        # ==================================================================
        self.play(
            FadeIn(left_axes), FadeIn(right_axes), FadeIn(divider),
            Create(left_orig), Create(right_orig),
            run_time=max(0.05, 1.36
        ))

        # ==================================================================
        # BEAT 2  [1.36 – 5.20]  Left sweep (window 5) & orange trace
        # ==================================================================
        self.add(left_band, left_smooth)
        self.play(
            left_tracker.animate.set_value(97),   # last full 5‑sample window centre
            FadeIn(left_label),
            run_time=max(0.05, 3.84
        ))
        left_band.clear_updaters()
        left_smooth.clear_updaters()

        # ==================================================================
        # BEAT 3  [5.20 – 8.20]  Left holds, original fades
        # ==================================================================
        self.play(left_orig.animate.set_stroke(opacity=0.3, width=1.0), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.5))

        # ==================================================================
        # BEAT 4  [8.20 – 9.20]  White glow around left smoothed spike
        # ==================================================================
        left_spike_smooth = left_axes.c2p(xs[spike_idx], smooth_y5[spike_idx])
        spike_glow = Circle(radius=0.3, color=WHITE, stroke_width=2,
                            fill_opacity=0).move_to(left_spike_smooth)
        self.play(GrowFromCenter(spike_glow), run_time=max(0.05, 0.2))
        self.play(spike_glow.animate.set_stroke(width=6, opacity=0.8), run_time=max(0.05, 0.3))
        self.play(spike_glow.animate.set_stroke(width=0, opacity=0), run_time=max(0.05, 0.5))

        # ==================================================================
        # BEAT 5  [9.20 – 11.78]  Right sweep (window 25) & dark‑red trace
        # ==================================================================
        self.add(right_band, right_smooth)
        self.play(
            right_tracker.animate.set_value(87),  # last full 25‑sample window centre
            FadeIn(right_label),
            run_time=max(0.05, 2.58
        ))
        right_band.clear_updaters()
        right_smooth.clear_updaters()

        # ==================================================================
        # BEAT 6  [11.78 – 13.26]  Right original fades
        # ==================================================================
        self.play(right_orig.animate.set_stroke(opacity=0.3, width=1.0), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.98))

        # ==================================================================
        # BEAT 7  [13.26 – 17.80]  Digital zoom onto spike region
        # ==================================================================
        left_spike_orig = left_axes.c2p(xs[spike_idx], y[spike_idx])
        right_spike_orig = right_axes.c2p(xs[spike_idx], y[spike_idx])
        left_circle = Circle(radius=0.15, color=GREY, stroke_width=1.5,
                             fill_opacity=0).move_to(left_spike_orig)
        right_circle = Circle(radius=0.15, color=GREY, stroke_width=1.5,
                              fill_opacity=0).move_to(right_spike_orig)

        self.add(left_circle, right_circle)
        self.play(
            self.camera.frame.animate.scale(0.6).move_to(np.array([0.44, 0, 0])),
            FadeIn(left_circle), FadeIn(right_circle),
            run_time=max(0.05, 4.54
        ))

        # ==================================================================
        # BEAT 8  [17.80 – 20.00]  Red glow on right flattened spike, then zoom out
        # ==================================================================
        right_spike_smooth = right_axes.c2p(xs[spike_idx], smooth_y25[spike_idx])
        right_glow = Circle(radius=0.25, color=RED, stroke_width=3,
                            fill_opacity=0.2).move_to(right_spike_smooth)
        self.play(GrowFromCenter(right_glow), run_time=max(0.05, 0.3))
        self.play(right_glow.animate.set_stroke(width=8, opacity=0.8).set_fill(opacity=0.4),
                  run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.58))   # until 19.08

        self.play(
            self.camera.frame.animate.scale(1).move_to(ORIGIN),
            FadeOut(left_circle), FadeOut(right_circle), FadeOut(right_glow),
            run_time=max(0.05, 0.92
        ))

        # ==================================================================
        # BEAT 9  [20.00 – 22.90]  "Window size matters" text
        # ==================================================================
        text = Text("Window size matters", font_size=64, color=YELLOW, weight="BOLD")
        text.move_to(np.array([0, -3.2, 0]))
        self.play(FadeIn(text), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.4))   # hold until 22.90