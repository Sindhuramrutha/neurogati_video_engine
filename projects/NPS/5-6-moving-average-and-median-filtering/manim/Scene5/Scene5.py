ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Data: a mostly flat, low-amplitude trace with one sharp spike
        # The seven window values are arranged so the spike is the center
        # sample, keeping the later "center sample" animation coherent.
        # ------------------------------------------------------------------
        n = 41
        xs = np.arange(n)
        spike_idx = 20

        rng = np.random.default_rng(42)
        baseline = (
            0.35
            + 0.15 * np.sin(0.55 * xs + 0.4)
            + 0.10 * rng.normal(size=n)
        )
        y = baseline.copy()

        # Exact seven sample values around the spike, spike centered:
        # 0.2, 0.3, 0.1, 5.8, 0.4, 0.3, 0.2
        window_indices = np.arange(spike_idx - 3, spike_idx + 4)
        window_vals = np.array([0.2, 0.3, 0.1, 5.8, 0.4, 0.3, 0.2])
        y[window_indices] = window_vals

        # Keep baseline elsewhere low amplitude.
        y = np.clip(y, 0.05, 0.65)

        # ------------------------------------------------------------------
        # Axes, unlabeled
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[0, n - 1, 1],
            y_range=[-0.2, 6.5, 1],
            x_length=12.5,
            y_length=4.6,
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "stroke_color": GREY,
                "stroke_width": 2,
            },
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False,
        ).move_to(ORIGIN)

        trace = VMobject(
            stroke_color=BLUE, stroke_width=3, fill_opacity=0
        ).set_points_as_corners(
            [axes.c2p(xs[i], y[i]) for i in range(n)]
        )

        # ==================================================================
        # BEAT 1  [0.00 - 0.96]  Fade in the waveform plot
        # ==================================================================
        self.play(FadeIn(axes), FadeIn(trace), run_time=max(0.05, 0.96))

        # ==================================================================
        # BEAT 2  [0.96 - 2.80]  Title appears
        # ==================================================================
        title = Text("Median Filter", font_size=56, color=WHITE, weight="BOLD")
        title.next_to(axes, UP, buff=0.4)
        self.play(FadeIn(title), run_time=max(0.05, 1.84))

        # ==================================================================
        # Gap  [2.80 - 3.52]
        # ==================================================================
        self.wait(max(0.05, 0.72))

        # ==================================================================
        # BEAT 3  [3.52 - 4.26]  Window + highlighted sample dots
        # ==================================================================
        dx = axes.x_length / (n - 1)
        window_width = 6 * dx + 0.30

        window_rect = Rectangle(
            width=window_width,
            height=axes.y_length,
            fill_color=TEAL,
            fill_opacity=0.12,
            stroke_color=TEAL,
            stroke_width=2.5,
            stroke_opacity=0.7,
        )
        window_rect.move_to(
            axes.c2p(xs[spike_idx], (axes.y_range[0] + axes.y_range[1]) / 2)
        )

        sample_dots = []
        for idx in window_indices:
            dot = Dot(
                point=axes.c2p(xs[idx], y[idx]),
                radius=0.09,
                color=WHITE,
                fill_opacity=1,
            )
            sample_dots.append(dot)

        self.play(
            FadeIn(window_rect),
            *[GrowFromCenter(dot) for dot in sample_dots],
            trace.animate.set_stroke(opacity=0.38),
            run_time=max(0.05, 0.74),
        )

        # ==================================================================
        # Gap  [4.26 - 4.90]
        # ==================================================================
        self.wait(max(0.05, 0.64))

        # ==================================================================
        # BEAT 4  [4.90 - 7.64]  Values next to the dots
        # ==================================================================
        value_strings = ["0.2", "0.3", "0.1", "5.8", "0.4", "0.3", "0.2"]
        sample_labels = []
        for dot, val_str in zip(sample_dots, value_strings):
            label = Text(val_str, font_size=18, color=WHITE)
            label.next_to(dot, UP, buff=0.10)
            sample_labels.append(label)

        self.play(
            *[Write(label) for label in sample_labels],
            run_time=max(0.05, 2.74),
        )

        # ==================================================================
        # Gap  [7.64 - 8.64]
        # ==================================================================
        self.wait(max(0.05, 1.00))

        # ==================================================================
        # BEAT 5  [8.64 - 12.00]  Lift and sort ascending below the plot
        # ==================================================================
        self.play(
            *[label.animate.shift(UP * 0.35) for label in sample_labels],
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 0.56))

        sorted_values = ["0.1", "0.2", "0.2", "0.3", "0.3", "0.4", "5.8"]
        sorted_pairs = sorted(
            zip(sample_labels, sorted_values), key=lambda pair: float(pair[1])
        )

        row_y = axes.get_bottom()[1] - 0.62
        target_centers = [
            np.array([-3.0 + i * 1.0, row_y, 0])
            for i in range(7)
        ]

        self.play(
            *[
                label.animate.move_to(target_centers[j])
                for j, (label, _) in enumerate(sorted_pairs)
            ],
            run_time=max(0.05, 2.00),
        )

        # ==================================================================
        # Gap  [12.00 - 12.54]
        # ==================================================================
        self.wait(max(0.05, 0.54))

        # ==================================================================
        # BEAT 6  [12.54 - 13.42]  Median glows, others dim
        # ==================================================================
        median_label = sorted_pairs[3][0]
        other_labels = [label for label in sample_labels if label is not median_label]

        self.play(
            median_label.animate.scale(1.35).set_color(ORANGE),
            *[label.animate.set_color(GREY).set_opacity(0.35) for label in other_labels],
            run_time=max(0.05, 0.50),
        )

        underline = Line(
            start=median_label.get_left() + DOWN * 0.18,
            end=median_label.get_right() + DOWN * 0.18,
            color=ORANGE,
            stroke_width=4,
        )
        self.play(Create(underline), run_time=max(0.05, 0.38))

        # ==================================================================
        # Gap  [13.42 - 14.22]
        # ==================================================================
        self.wait(max(0.05, 0.80))

        # ==================================================================
        # BEAT 7  [14.22 - 17.64]  Replace spike value with median
        # ==================================================================
        y_clean = y.copy()
        y_clean[spike_idx] = 0.3
        new_trace = VMobject(
            stroke_color=BLUE, stroke_width=3, fill_opacity=0
        ).set_points_as_corners(
            [axes.c2p(xs[i], y_clean[i]) for i in range(n)]
        ).set_stroke(opacity=0.38)

        original_spike_dot = sample_dots[3]
        new_spike_pos = axes.c2p(xs[spike_idx], 0.3)

        self.play(
            Transform(trace, new_trace),
            original_spike_dot.animate.move_to(new_spike_pos),
            run_time=max(0.05, 1.30),
        )

        median_text = Text("median", font_size=26, color=YELLOW, weight="BOLD")
        median_text.next_to(new_spike_pos, UP + RIGHT, buff=0.70)
        median_arrow = Arrow(
            start=median_text.get_bottom(),
            end=new_spike_pos,
            buff=0.10,
            color=YELLOW,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.20,
        )

        self.play(FadeIn(median_text), FadeIn(median_arrow), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 1.25))
        self.play(FadeOut(median_text), FadeOut(median_arrow), run_time=max(0.05, 0.42))

        # ==================================================================
        # BEAT 8  [17.64 - 19.88]  Remove annotations, mark former spike
        # ==================================================================
        annotations = VGroup(
            window_rect,
            *sample_dots,
            *sample_labels,
            underline,
        )
        self.play(FadeOut(annotations), run_time=max(0.05, 1.00))

        former_spike_pos = axes.c2p(xs[spike_idx], 5.8)
        faint_dashed_circle = DashedVMobject(
            Circle(radius=0.32, color=GREY, stroke_width=2, fill_opacity=0),
            num_dashes=24,
        ).move_to(former_spike_pos)

        self.play(FadeIn(faint_dashed_circle), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.36))
        self.play(FadeOut(faint_dashed_circle), run_time=max(0.05, 0.38))

        # ==================================================================
        # BEAT 9  [19.88 - 23.48]  Takeaway text below the cleaned plot
        # ==================================================================
        final_text = Text(
            "Extreme values have very little\ninfluence on the median",
            font_size=38,
            color=WHITE,
            line_spacing=0.7,
        )
        final_text.scale_to_fit_width(10.5)
        final_text.next_to(axes, DOWN, buff=0.35)

        self.play(FadeIn(final_text), run_time=max(0.05, 1.50))
        self.wait(max(0.05, 2.10))