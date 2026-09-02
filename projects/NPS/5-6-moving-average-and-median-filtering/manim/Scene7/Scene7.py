ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

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

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Helper functions to build signal VMobjects
        # ------------------------------------------------------------------
        def make_signal(axes, x_arr, y_arr, color=WHITE, stroke_width=3):
            points = [axes.c2p(x, y) for x, y in zip(x_arr, y_arr)]
            mob = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
            mob.set_points_as_corners(points)
            return mob

        # ------------------------------------------------------------------
        # Common x range
        # ------------------------------------------------------------------
        x_fine = np.linspace(0, 10, 250)

        # Original signal: low baseline, sharp step at x=3, narrow spike at x=6
        baseline = 0.2
        step = 0.8 * (x_fine >= 3).astype(float)
        spike = 1.0 * np.exp(-0.5 * ((x_fine - 6) / 0.08) ** 2)
        y_original = baseline + step + spike

        # Median-filtered: spike removed, step intact
        y_median = baseline + step

        # Moving-average smoothed: step → ramp, spike → broadened and reduced
        smooth_step = 0.2 + 0.8 / (1 + np.exp(-(x_fine - 3) / 0.07))
        broad_spike = 0.4 * np.exp(-0.5 * ((x_fine - 6) / 0.5) ** 2)
        y_smoothed = smooth_step + broad_spike

        # ------------------------------------------------------------------
        # BEAT 1 [0.00 – 2.04]  Single plot with sharp step and spike
        # ------------------------------------------------------------------
        axes1 = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 2.2, 0.5],
            x_length=6.5,
            y_length=3.5,
            axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 2},
            tips=False,
        ).move_to(ORIGIN)

        signal_orig = make_signal(axes1, x_fine, y_original, color=WHITE, stroke_width=3)

        self.play(FadeIn(axes1), Write(signal_orig), run_time=max(0.05, 2.04))

        # ------------------------------------------------------------------
        # BEAT 2 [2.04 – 5.38]  Spike shrinks (median filter), then split
        # ------------------------------------------------------------------
        signal_median = make_signal(axes1, x_fine, y_median, color=WHITE, stroke_width=3)
        self.play(Transform(signal_orig, signal_median), run_time=max(0.05, 1.5))

        # Prepare left panel: move the existing axes + signal to the left
        left_panel = VGroup(axes1, signal_orig)
        left_panel.generate_target()
        left_panel.target.scale(0.75).move_to(LEFT * 3.5)

        # Prepare right panel: new axes and a copy of the original signal
        right_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 2.2, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 2},
            tips=False,
        ).move_to(RIGHT * 3.5)
        signal_orig_right = make_signal(right_axes, x_fine, y_original, color=WHITE, stroke_width=3)
        right_panel = VGroup(right_axes, signal_orig_right)

        # Split animation
        self.play(MoveToTarget(left_panel), FadeIn(right_panel), run_time=max(0.05, 1.84))

        # ------------------------------------------------------------------
        # BEAT 3 [5.38 – 6.96]  Moving-average on right panel
        # ------------------------------------------------------------------
        signal_smoothed = make_signal(right_axes, x_fine, y_smoothed, color=WHITE, stroke_width=3)
        self.play(Transform(signal_orig_right, signal_smoothed), run_time=max(0.05, 1.58))

        # ------------------------------------------------------------------
        # BEAT 4 [6.96 – 9.84]  Annotation beneath panels
        # ------------------------------------------------------------------
        annotation = Text(
            "Median filter (left) preserves sharp edges;\nMoving average (right) blurs them.",
            font_size=26,
            color=WHITE,
            line_spacing=1.0,
            t2c={"Median filter (left)": YELLOW, "Moving average (right)": ORANGE}
        )
        annotation.scale_to_fit_width(10)
        annotation.next_to(VGroup(axes1, right_axes), DOWN, buff=0.5)
        self.play(FadeIn(annotation), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.88))

        # ------------------------------------------------------------------
        # BEAT 5 [9.84 – 11.64]  Sharp step in left panel glows/pulses
        # ------------------------------------------------------------------
        step_point = axes1.c2p(3, 0.6)  # midpoint of the step
        step_dot = Dot(point=step_point, radius=0.18, color=YELLOW, fill_opacity=1)
        self.play(GrowFromCenter(step_dot), run_time=max(0.05, 0.3))
        self.play(step_dot.animate.scale(1.5).set_opacity(0.5), run_time=max(0.05, 0.5))
        self.play(step_dot.animate.scale(1 / 1.5).set_opacity(1), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.5))

        # ------------------------------------------------------------------
        # BEAT 6 [11.64 – 12.36]  Fade out panels, annotation, highlight;
        #                           show new high‑frequency noise plot
        # ------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(left_panel, right_panel, annotation, step_dot)),
            run_time=max(0.05, 0.4
        ))

        # Generate noise
        np.random.seed(42)
        noise_n = 200
        noise_x = np.linspace(0, 10, noise_n)
        noise_steps = np.random.randn(noise_n) * 0.1
        noise_y = np.cumsum(noise_steps) + 0.5
        noise_y = (noise_y - noise_y.min()) / (noise_y.max() - noise_y.min()) * 1.0 + 0.2

        noise_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.5, 0.5],
            x_length=6.5,
            y_length=3.5,
            axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 2},
            tips=False,
        ).move_to(ORIGIN)

        noise_signal = make_signal(noise_axes, noise_x, noise_y, color=WHITE, stroke_width=2.5)

        self.play(FadeIn(noise_axes), FadeIn(noise_signal), run_time=max(0.05, 0.32))

        # ------------------------------------------------------------------
        # BEAT 7 [12.36 – 14.00]  Split into two panels (both noisy)
        # ------------------------------------------------------------------
        left_noise_panel = VGroup(noise_axes, noise_signal)
        left_noise_panel.generate_target()
        left_noise_panel.target.scale(0.75).move_to(LEFT * 3.5)

        right_noise_axes = noise_axes.copy().move_to(RIGHT * 3.5)
        right_noise_signal = make_signal(right_noise_axes, noise_x, noise_y, color=WHITE, stroke_width=2.5)
        right_noise_panel = VGroup(right_noise_axes, right_noise_signal)

        self.play(
            MoveToTarget(left_noise_panel),
            FadeIn(right_noise_panel),
            run_time=max(0.05, 1.64
        ))

        # ------------------------------------------------------------------
        # BEAT 8 [14.00 – 16.92]  Label “High‑frequency noise” near left
        # ------------------------------------------------------------------
        label_hf = Text("High‑frequency noise", font_size=22, color=WHITE, weight="BOLD")
        label_hf.next_to(left_noise_panel, DOWN, buff=0.4)
        self.play(Write(label_hf), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.72))

        # ------------------------------------------------------------------
        # BEAT 9 [16.92 – 21.28]  “Prefers frequency‑domain filtering”
        # ------------------------------------------------------------------
        label_freq = Text(
            "Prefers frequency‑domain filtering",
            font_size=22,
            color=WHITE,
            weight="BOLD",
            t2c={"Prefers": YELLOW}
        )
        label_freq.next_to(right_noise_panel, DOWN, buff=0.4)
        self.play(Write(label_freq), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 2.86))

        # ------------------------------------------------------------------
        # BEAT 10 [21.28 – 24.73]  Noise panels fade out; circular inset
        #                            with isolated spike → median filter
        # ------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(left_noise_panel, right_noise_panel, label_hf, label_freq)),
            run_time=max(0.05, 0.5
        ))

        # Inset: small axes inside a circle
        inset_axes = Axes(
            x_range=[4, 8, 1],
            y_range=[0, 2.2, 0.5],
            x_length=2.5,
            y_length=1.8,
            axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 1.5},
            tips=False,
        ).move_to(ORIGIN)

        inset_circle = Circle(
            radius=inset_axes.get_width() * 0.65,
            stroke_color=WHITE,
            stroke_width=2,
            fill_opacity=0,
        ).move_to(inset_axes)

        x_inset = np.linspace(4, 8, 100)
        spike_inset = 1.0 * np.exp(-0.5 * ((x_inset - 6) / 0.08) ** 2)
        y_inset_spike = 0.2 + spike_inset
        y_inset_flat = np.full_like(x_inset, 0.2)

        signal_inset_spike = make_signal(inset_axes, x_inset, y_inset_spike, color=WHITE, stroke_width=3)
        signal_inset_flat = make_signal(inset_axes, x_inset, y_inset_flat, color=WHITE, stroke_width=3)

        inset_group = VGroup(inset_axes, inset_circle, signal_inset_spike)
        self.play(FadeIn(inset_group), run_time=max(0.05, 0.5))

        # Median filter: spike shrinks to zero
        self.play(Transform(signal_inset_spike, signal_inset_flat), run_time=max(0.05, 1.0))

        # Text “isolated artifacts”
        text_iso = Text("isolated artifacts", font_size=28, color=WHITE, weight="BOLD")
        text_iso.next_to(inset_group, RIGHT, buff=0.5)
        self.play(FadeIn(text_iso), run_time=max(0.05, 0.5))

        # Remainder of the beat
        self.wait(max(0.05, 0.95))

        # Ensure everything stays until the very end
        self.wait(max(0.05, 0.01))  # tiny buffer to hit exactly 24.73