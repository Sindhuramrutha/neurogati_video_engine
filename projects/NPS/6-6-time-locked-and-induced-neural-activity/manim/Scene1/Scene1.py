ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Geometry constants -- phase 1 (large left-side display)
        # ------------------------------------------------------------------
        x_axis_start = -6.0
        x_axis_end = -0.2
        y_axis = -1.8
        t0_x = -3.2
        x_100 = -1.2
        x_epoch_end = 0.8

        y_epoch_top = 0.6
        epoch_gap = 0.42
        y_epochs = [y_epoch_top - i * epoch_gap for i in range(5)]

        amp_list = [0.20, 0.30, 0.16, 0.26, 0.22]
        sigma_peak = 0.24

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------
        def make_epoch(baseline, amp, noise_level=0.0, color=TEAL):
            def wave(x):
                bump = amp * np.exp(-0.5 * ((x - x_100) / sigma_peak) ** 2)
                noise = noise_level * np.sin(18.0 * x) if noise_level else 0.0
                return baseline + bump + noise

            graph = FunctionGraph(wave, x_range=[t0_x, x_epoch_end, 0.015], color=color)
            graph.set_stroke(color=color, width=3, opacity=0.9)
            return graph

        def make_speaker():
            speaker = VGroup()

            body = Rectangle(
                width=0.22,
                height=0.60,
                fill_color=YELLOW,
                fill_opacity=1,
                stroke_width=0,
            ).move_to([-0.18, 0, 0])

            cone = Polygon(
                [-0.08, 0.28, 0],
                [0.22, 0.42, 0],
                [0.22, -0.42, 0],
                [-0.08, -0.28, 0],
                fill_color=YELLOW,
                fill_opacity=1,
                stroke_width=0,
            )

            front = Rectangle(
                width=0.06,
                height=0.84,
                fill_color=YELLOW,
                fill_opacity=1,
                stroke_width=0,
            ).move_to([0.27, 0, 0])

            speaker.add(body, cone, front)
            speaker.scale(0.38)
            return speaker

        # ------------------------------------------------------------------
        # Phase 1 mobjects
        # ------------------------------------------------------------------
        partial_axis = Line(
            [x_axis_start, y_axis, 0],
            [x_axis_end, y_axis, 0],
            stroke_color=GREY_B,
            stroke_width=4,
            stroke_opacity=0.55,
        )

        tick = Line(
            [t0_x, y_axis - 0.18, 0],
            [t0_x, y_axis + 0.18, 0],
            stroke_color=YELLOW,
            stroke_width=5,
            stroke_opacity=1.0,
        )

        stimulus_label = Text(
            "Stimulus", font_size=28, color=YELLOW, weight="BOLD"
        ).next_to(tick, DOWN, buff=0.12)

        title = Text(
            "Time-Locked Neural Activity",
            font_size=40,
            color=WHITE,
            weight="BOLD",
        )
        title.to_edge(UP, buff=0.45)

        t0_dashed = DashedLine(
            [t0_x, y_axis + 0.25, 0],
            [t0_x, 1.45, 0],
            dash_length=0.12,
            stroke_color=GREY_B,
            stroke_width=2,
            stroke_opacity=0.55,
        )

        epochs = [make_epoch(y_epochs[i], amp_list[i]) for i in range(5)]

        peak_dashed = DashedLine(
            [x_100, 2.05, 0],
            [x_100, y_axis - 0.30, 0],
            dash_length=0.12,
            stroke_color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.9,
        )

        tone_group = make_speaker()
        tone_group.move_to([t0_x - 2.1, y_axis + 0.35, 0])
        tone_label = Text("tone", font_size=24, color=WHITE, weight="BOLD")
        tone_label.next_to(tone_group, DOWN, buff=0.15)

        left_group = VGroup(
            partial_axis,
            tick,
            stimulus_label,
            t0_dashed,
            *epochs,
            peak_dashed,
        )

        # ------------------------------------------------------------------
        # Right panel mobjects (phase 2)
        # ------------------------------------------------------------------
        right_panel = Rectangle(
            width=4.0,
            height=3.0,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.18,
        ).move_to([3.6, 0.0, 0])

        avg_label = Text("Average", font_size=32, color=YELLOW, weight="BOLD")
        avg_label.next_to(right_panel, DOWN, buff=0.20)

        right_x_start = 1.8
        right_x_end = 5.2
        right_t0 = 2.2
        right_x_100 = 3.8
        right_baseline = -0.2
        right_amp = 0.35
        right_sigma = 0.20

        def make_right_wave(noise_level=0.0, color=YELLOW, width=3.5):
            def wave(x):
                bump = right_amp * np.exp(-0.5 * ((x - right_x_100) / right_sigma) ** 2)
                noise = noise_level * np.sin(38.0 * x) if noise_level else 0.0
                return right_baseline + bump + noise

            graph = FunctionGraph(
                wave,
                x_range=[right_x_start, right_x_end, 0.015],
                color=color,
            )
            graph.set_stroke(color=color, width=width, opacity=0.95)
            return graph

        right_avg_noisy = make_right_wave(noise_level=0.065, color=YELLOW, width=3.0)
        right_avg_clean = make_right_wave(noise_level=0.0, color=YELLOW, width=6.0)

        right_peak_dashed = DashedLine(
            [right_x_100, 1.25, 0],
            [right_x_100, -0.85, 0],
            dash_length=0.10,
            stroke_color=YELLOW,
            stroke_width=2.5,
            stroke_opacity=0.85,
        )

        right_ms_label = Text("100 ms", font_size=26, color=YELLOW, weight="BOLD")
        right_ms_label.move_to([right_x_100, -0.65, 0])

        left_panel = Rectangle(
            width=4.0,
            height=4.0,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.15,
        ).move_to([-4.2, -0.1, 0])
        left_panel_center = np.array([-4.2, -0.1, 0])

        # ------------------------------------------------------------------
        # Beat 1 | 0.00 - 3.00
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.5))
        self.play(Create(partial_axis), run_time=max(0.05, 1.4))
        self.play(Create(tick), FadeIn(stimulus_label), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.4))

        # ------------------------------------------------------------------
        # Beat 2 | 3.00 - 6.26
        # ------------------------------------------------------------------
        self.play(FadeIn(title), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.26))

        # ------------------------------------------------------------------
        # Beat 3 | 6.26 - 11.26
        # ------------------------------------------------------------------
        self.play(Create(t0_dashed), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 3.0))

        # ------------------------------------------------------------------
        # Beat 4 | 11.26 - 14.50
        # ------------------------------------------------------------------
        self.play(FadeIn(tone_group), FadeIn(tone_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.24))

        # ------------------------------------------------------------------
        # Beat 5 | 14.50 - 19.60
        # ------------------------------------------------------------------
        self.play(Create(epochs[0]), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 3.3))

        # ------------------------------------------------------------------
        # Beat 6 | 19.60 - 21.94
        # ------------------------------------------------------------------
        self.play(Create(peak_dashed), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 0.54))

        # ------------------------------------------------------------------
        # Beat 7 | 21.94 - 25.70
        # ------------------------------------------------------------------
        self.play(Create(epochs[1]), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 2.16))

        # ------------------------------------------------------------------
        # Beat 8 | 25.70 - 29.36
        # ------------------------------------------------------------------
        self.play(Create(epochs[2]), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 2.06))

        # ------------------------------------------------------------------
        # Beat 9 | 29.36 - 33.12
        # ------------------------------------------------------------------
        for i in (3, 4):
            self.play(Create(epochs[i]), run_time=max(0.05, 0.9))
            self.wait(max(0.05, 0.98))

        # ------------------------------------------------------------------
        # Beat 10 | 33.12 - 36.72
        # ------------------------------------------------------------------
        self.play(Create(right_panel), FadeIn(avg_label), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 2.4))

        # ------------------------------------------------------------------
        # Beat 11 | 36.72 - 42.36
        # ------------------------------------------------------------------
        self.play(FadeOut(tone_group), FadeOut(tone_label), run_time=max(0.05, 0.5))
        self.play(
            left_group.animate.scale(0.55).move_to(left_panel_center),
            Create(right_avg_noisy),
            Create(left_panel),
            run_time=max(0.05, 3.0),
        )
        self.wait(max(0.05, 2.14))

        # ------------------------------------------------------------------
        # Beat 12 | 42.36 - 46.88
        # ------------------------------------------------------------------
        self.play(
            left_panel.animate.set_stroke(width=2, opacity=0.35),
            left_group.animate.set_opacity(0.40),
            peak_dashed.animate.set_opacity(0.90),
            right_panel.animate.set_stroke(color=YELLOW, width=4, opacity=1.0),
            right_avg_noisy.animate.set_stroke(width=5, opacity=1.0),
            run_time=max(0.05, 1.6),
        )
        self.play(Create(right_peak_dashed), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 1.32))

        # ------------------------------------------------------------------
        # Beat 13 | 46.88 - 52.46
        # ------------------------------------------------------------------
        # Highlight 100 ms on left panel time axis.
        time_start = partial_axis.get_start()
        time_end = partial_axis.get_end()
        alpha_100 = (x_100 - x_axis_start) / (x_axis_end - x_axis_start)
        x100_now = interpolate(time_start[0], time_end[0], alpha_100)
        y_axis_now = partial_axis.get_center()[1]

        left_ms_tick = Line(
            [x100_now, y_axis_now - 0.12, 0],
            [x100_now, y_axis_now + 0.12, 0],
            stroke_color=YELLOW,
            stroke_width=5,
            stroke_opacity=1.0,
        )
        left_ms_glow = Dot(
            [x100_now, y_axis_now, 0],
            radius=0.08,
            color=YELLOW,
            fill_opacity=1,
        )

        self.play(
            FadeIn(right_ms_label),
            Create(left_ms_tick),
            GrowFromCenter(left_ms_glow),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 3.58))

        # ------------------------------------------------------------------
        # Beat 14 | 52.46 - 56.24
        # ------------------------------------------------------------------
        self.play(
            right_avg_noisy.animate.set_stroke(width=6, opacity=1, color=YELLOW),
            run_time=max(0.05, 1.0),
        )
        self.play(Transform(right_avg_noisy, right_avg_clean), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------------
        # Beat 15 | 56.24 - 59.52
        # ------------------------------------------------------------------
        # Current scaled left-panel coordinates for a faint stack of additional epochs.
        x_start_now = interpolate(time_start[0], time_end[0],
                                  (t0_x - x_axis_start) / (x_axis_end - x_axis_start))
        x_end_now = interpolate(time_start[0], time_end[0],
                                (x_epoch_end - x_axis_start) / (x_axis_end - x_axis_start))
        peak_now = x100_now

        def make_faint_epoch(y_row):
            def wave(x):
                return y_row + 0.18 * np.exp(-0.5 * ((x - peak_now) / 0.22) ** 2)

            graph = FunctionGraph(
                wave,
                x_range=[x_start_now, x_end_now, 0.02],
                color=TEAL,
            )
            graph.set_stroke(color=TEAL, width=1.5, opacity=0.22)
            return graph

        faint_ys = np.linspace(-1.35, 0.70, 20)
        additional_epochs = [make_faint_epoch(y) for y in faint_ys]

        for graph in additional_epochs:
            self.play(FadeIn(graph), run_time=max(0.05, 0.13))

        count_label = Text("100 epochs", font_size=24, color=WHITE, weight="BOLD")
        count_label.move_to([left_panel_center[0], -1.85, 0])
        self.play(FadeIn(count_label), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.28))

        # ------------------------------------------------------------------
        # Beat 16 | 59.52 - 64.65
        # ------------------------------------------------------------------
        self.play(
            right_avg_clean.animate.set_stroke(width=7, opacity=1.0),
            run_time=max(0.05, 1.0),
        )
        self.play(
            right_avg_clean.animate.set_stroke(width=6, opacity=1.0),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 3.13))