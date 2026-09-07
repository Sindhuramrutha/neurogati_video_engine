ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
from manim.utils.color import interpolate_color
import numpy as np


class Scene2(Scene):
    def build_previous_final(self):
        """Small mute placeholder of the end of Scene 1, used only so it can fade out."""
        prev_title = Text(
            "Time-Locked Neural Activity",
            font_size=32,
            color=WHITE,
            weight="BOLD",
        ).to_edge(UP, buff=0.4)

        prev_epochs = VGroup()
        for y in [0.85, 0.5, 0.15, -0.2, -0.55]:
            def wave(x, y=y):
                return y + 0.2 * np.exp(-0.5 * ((x + 0.6) / 0.24) ** 2)

            graph = FunctionGraph(
                wave,
                x_range=[-5.2, -0.4, 0.05],
                color=TEAL,
                stroke_width=2,
                stroke_opacity=0.7,
            )
            prev_epochs.add(graph)

        prev_dash = DashedLine(
            [-0.6, 1.7, 0],
            [-0.6, -1.2, 0],
            dash_length=0.1,
            stroke_color=YELLOW,
            stroke_width=2.5,
            stroke_opacity=0.8,
        )

        prev_avg_panel = Rectangle(
            width=3.4,
            height=2.4,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.25,
        ).move_to([2.5, 0.0, 0])

        def avg_wave(x):
            return -0.1 + 0.4 * np.exp(-0.5 * ((x - 2.7) / 0.22) ** 2)

        prev_avg_graph = FunctionGraph(
            avg_wave,
            x_range=[1.0, 4.0, 0.05],
            color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.9,
        )

        return VGroup(
            prev_title,
            prev_epochs,
            prev_dash,
            prev_avg_panel,
            prev_avg_graph,
        ).move_to([-0.4, 0.1, 0])

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Geometry constants for the new induced-activity scene
        # ------------------------------------------------------------------
        stim_x = -5.0
        tick_interval = 1.5          # 100 ms per tick interval
        time_end_x = stim_x + 4 * tick_interval
        time_y = -2.2

        epoch_colors = [TEAL, BLUE, ORANGE]
        latencies = [250, 320, 280]  # ms
        y_epochs = [1.4, 0.5, -0.4]
        amps = [0.8, 0.7, 1.0]

        peak_xs = [stim_x + (latencies[i] / 100.0) * tick_interval for i in range(3)]
        peak_ys = [y_epochs[i] + amps[i] for i in range(3)]

        # ------------------------------------------------------------------
        # Helper for individual induced EEG epochs
        # ------------------------------------------------------------------
        def make_epoch(latency_ms, amp, y_base, color):
            x_lat = stim_x + (latency_ms / 100.0) * tick_interval
            sigma_x = 0.45

            def wave(x, x_lat=x_lat, y_base=y_base, amp=amp, sigma_x=sigma_x):
                return y_base + amp * np.exp(-0.5 * ((x - x_lat) / sigma_x) ** 2)

            graph = FunctionGraph(
                wave,
                x_range=[stim_x, time_end_x, 0.015],
                color=color,
            )
            graph.set_stroke(color=color, width=3.5, opacity=0.95)
            return graph

        # ------------------------------------------------------------------
        # Beat 1 | 0.00 - 1.64
        # ------------------------------------------------------------------
        prev_final = self.build_previous_final()
        self.add(prev_final)

        stim_line = Line(
            [stim_x, 3.5, 0],
            [stim_x, -3.5, 0],
            stroke_color=GREY,
            stroke_width=2.5,
            stroke_opacity=0.8,
        )
        stim_label = Text("Stimulus", font_size=24, color=YELLOW, weight="BOLD")
        stim_label.next_to(stim_line, LEFT, buff=0.15)

        self.play(
            FadeOut(prev_final),
            Create(stim_line),
            FadeIn(stim_label),
            run_time=max(0.05, 1.64),
        )

        # ------------------------------------------------------------------
        # Beat 2 | 1.64 - 3.62
        # ------------------------------------------------------------------
        title = Text(
            "Induced Neural Activity",
            font_size=46,
            color=WHITE,
            weight="BOLD",
        )
        title.move_to([0.0, 2.55, 0])

        self.play(FadeIn(title), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------------
        # Beat 3 | 3.62 - 7.24
        # ------------------------------------------------------------------
        self.play(title.animate.move_to([0.0, 3.15, 0]), run_time=max(0.05, 0.80))

        time_axis = Line(
            [stim_x, time_y, 0],
            [time_end_x, time_y, 0],
            stroke_color=GREY,
            stroke_width=3,
            stroke_opacity=0.7,
        )

        tick_xs = [stim_x + i * tick_interval for i in range(5)]
        tick_marks = VGroup(
            *[
                Line(
                    [x, time_y - 0.12, 0],
                    [x, time_y + 0.12, 0],
                    stroke_color=GREY,
                    stroke_width=3,
                )
                for x in tick_xs
            ]
        )
        tick_labels = VGroup(
            *[
                Text("0" if i == 0 else f"{i * 100} ms", font_size=20, color=GREY)
                .next_to(tick_marks[i], DOWN, buff=0.08)
                for i in range(5)
            ]
        )
        time_group = VGroup(time_axis, tick_marks, tick_labels)

        self.play(Create(time_axis), run_time=max(0.05, 0.70))
        self.play(Create(tick_marks), FadeIn(tick_labels), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 0.92))

        # ------------------------------------------------------------------
        # Beat 4 | 7.24 - 11.00
        # ------------------------------------------------------------------
        align_arrow = Arrow(
            [stim_x + 0.55, time_y + 0.75, 0],
            [stim_x, time_y + 0.08, 0],
            buff=0.12,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.22,
        )

        self.play(
            stim_line.animate.set_stroke(color=YELLOW, width=5, opacity=1.0),
            run_time=max(0.05, 0.55),
        )
        self.play(Create(align_arrow), run_time=max(0.05, 1.00))
        self.play(Wiggle(align_arrow, scale_value=0.08), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 1.21))

        # ------------------------------------------------------------------
        # Beat 5 | 11.00 - 13.80
        # ------------------------------------------------------------------
        epochs = [
            make_epoch(latencies[i], amps[i], y_epochs[i], epoch_colors[i])
            for i in range(3)
        ]

        self.play(Create(epochs[0]), run_time=max(0.05, 1.80))
        self.wait(max(0.05, 1.00))

        # ------------------------------------------------------------------
        # Beat 6 | 13.80 - 17.08
        # ------------------------------------------------------------------
        self.play(Create(epochs[1]), run_time=max(0.05, 1.90))
        self.wait(max(0.05, 1.38))

        # ------------------------------------------------------------------
        # Beat 7 | 17.08 - 21.40
        # ------------------------------------------------------------------
        self.play(Create(epochs[2]), run_time=max(0.05, 2.00))
        self.wait(max(0.05, 2.32))

        # ------------------------------------------------------------------
        # Beat 8 | 21.40 - 24.26
        # ------------------------------------------------------------------
        markers = [
            Dot(
                [peak_xs[i], peak_ys[i], 0],
                radius=0.09,
                color=epoch_colors[i],
                fill_opacity=1,
            )
            for i in range(3)
        ]

        lat_texts = [
            Text("250 ms", font_size=22, color=TEAL, weight="BOLD")
            .next_to(markers[0], LEFT, buff=0.12),
            Text("320 ms", font_size=22, color=BLUE, weight="BOLD")
            .next_to(markers[1], RIGHT, buff=0.12),
            Text("280 ms", font_size=22, color=ORANGE, weight="BOLD")
            .next_to(markers[2], DOWN, buff=0.10),
        ]

        for i in range(3):
            self.play(
                GrowFromCenter(markers[i]),
                FadeIn(lat_texts[i]),
                run_time=max(0.05, 0.66),
            )
            self.wait(max(0.05, 0.29))
        self.wait(max(0.05, 0.01))

        # ------------------------------------------------------------------
        # Beat 9 | 24.26 - 28.60
        # ------------------------------------------------------------------
        hl_ticks = VGroup(
            *[
                Line(
                    [peak_xs[i], time_y - 0.14, 0],
                    [peak_xs[i], time_y + 0.14, 0],
                    stroke_color=epoch_colors[i],
                    stroke_width=5,
                    stroke_opacity=0.0,
                )
                for i in range(3)
            ]
        )

        self.play(
            Indicate(markers[0], color=YELLOW, scale_factor=1.5),
            hl_ticks[0].animate.set_stroke(opacity=1),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.97))

        self.play(
            Indicate(markers[1], color=YELLOW, scale_factor=1.5),
            hl_ticks[1].animate.set_stroke(opacity=1),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.97))

        # ------------------------------------------------------------------
        # Beat 10 | 28.60 - 32.32
        # ------------------------------------------------------------------
        self.play(
            Indicate(markers[2], color=YELLOW, scale_factor=1.5),
            hl_ticks[2].animate.set_stroke(opacity=1),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 2.52))

        # ------------------------------------------------------------------
        # Beat 11 | 32.32 - 36.50
        # ------------------------------------------------------------------
        left_data_group = VGroup(
            time_group,
            *epochs,
            *markers,
            *lat_texts,
            hl_ticks,
        )

        band_left = min(peak_xs) - 0.05
        band_right = max(peak_xs) + 0.05
        mid_lat_x = (min(peak_xs) + max(peak_xs)) / 2

        band = Rectangle(
            width=(band_right - band_left),
            height=1.5,
            fill_color=GOLD,
            fill_opacity=0.08,
            stroke_width=0,
        ).move_to([mid_lat_x, 1.7, 0])

        bracket_top_y = 2.75
        bracket = VGroup(
            Line(
                [band_left, bracket_top_y, 0],
                [band_right, bracket_top_y, 0],
                color=GREY_B,
                stroke_width=3,
            ),
            Line(
                [band_left, bracket_top_y + 0.12, 0],
                [band_left, bracket_top_y - 0.12, 0],
                color=GREY_B,
                stroke_width=3,
            ),
            Line(
                [band_right, bracket_top_y + 0.12, 0],
                [band_right, bracket_top_y - 0.12, 0],
                color=GREY_B,
                stroke_width=3,
            ),
        )

        same_task_label = Text(
            "same task, different timing",
            font_size=26,
            color=YELLOW,
            weight="BOLD",
        ).move_to([mid_lat_x, bracket_top_y - 0.35, 0])

        self.play(FadeIn(band), run_time=max(0.05, 1.20))
        self.play(Create(bracket), FadeIn(same_task_label), run_time=max(0.05, 1.50))
        self.wait(max(0.05, 1.48))

        # ------------------------------------------------------------------
        # Beat 12 | 36.50 - 39.24
        # ------------------------------------------------------------------
        for marker in markers:
            self.play(
                Indicate(marker, color=YELLOW, scale_factor=1.3),
                run_time=max(0.05, 0.50),
            )

        avg_lat_ms = (latencies[0] + latencies[1] + latencies[2]) / 3.0
        avg_lat_x = stim_x + (avg_lat_ms / 100.0) * tick_interval
        avg_dashed = DashedLine(
            [avg_lat_x, 2.6, 0],
            [avg_lat_x, time_y + 0.15, 0],
            dash_length=0.1,
            stroke_color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.9,
        )

        self.play(Create(avg_dashed), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.35))
        self.play(FadeOut(avg_dashed), run_time=max(0.05, 0.39))

        # ------------------------------------------------------------------
        # Beat 13 | 39.24 - 42.30
        # ------------------------------------------------------------------
        avg_panel = Rectangle(
            width=4.0,
            height=2.4,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.20,
        ).move_to([2.7, 1.1, 0])

        avg_title = Text("Average", font_size=30, color=YELLOW, weight="BOLD")
        avg_title.move_to([2.7, 2.35, 0])

        avg_panel_group = VGroup(avg_panel, avg_title)

        self.play(
            FadeOut(VGroup(band, bracket, same_task_label)),
            left_data_group.animate.scale(0.9, about_point=[stim_x, time_y, 0]),
            FadeIn(avg_panel_group),
            run_time=max(0.05, 2.00),
        )
        self.wait(max(0.05, 1.06))

        # ------------------------------------------------------------------
        # Beat 14 | 42.30 - 46.42
        # ------------------------------------------------------------------
        avg_left = 0.8
        avg_right = 4.6
        avg_baseline = 0.35
        avg_amp = 0.50
        avg_sigma = 0.45
        avg_center_x = avg_left + (285 / 400.0) * (avg_right - avg_left)

        def avg_wave_func(x):
            return avg_baseline + avg_amp * np.exp(
                -0.5 * ((x - avg_center_x) / avg_sigma) ** 2
            )

        avg_wave = FunctionGraph(
            avg_wave_func,
            x_range=[avg_left, avg_right, 0.015],
            color=YELLOW,
        )
        avg_wave.set_stroke(color=YELLOW, width=5, opacity=0.95)

        self.play(Create(avg_wave), run_time=max(0.05, 3.00))
        self.wait(max(0.05, 1.12))

        # ------------------------------------------------------------------
        # Beat 15 | 46.42 - 49.40
        # ------------------------------------------------------------------
        self.play(
            avg_panel_group.animate.scale(1.06),
            avg_wave.animate.scale(1.06),
            run_time=max(0.05, 1.20),
        )

        avg_conclusion = Text(
            "Averaging reduces induced activity",
            font_size=28,
            color=WHITE,
            weight="BOLD",
        )
        avg_conclusion.next_to(avg_panel, DOWN, buff=0.20)

        self.play(FadeIn(avg_conclusion), run_time=max(0.05, 0.90))
        self.play(
            Indicate(avg_wave, color=YELLOW, scale_factor=1.12),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 0.08))

        # ------------------------------------------------------------------
        # Beat 16 | 49.40 - 52.84
        # ------------------------------------------------------------------
        tf_panel = Rectangle(
            width=4.0,
            height=2.4,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.20,
        ).move_to([2.7, -2.15, 0])

        tf_title = Text(
            "Time-frequency analysis",
            font_size=26,
            color=WHITE,
            weight="BOLD",
        )
        tf_title.move_to([2.7, tf_panel.get_top()[1] - 0.35, 0])

        # Build a spectrogram heatmap from colored rectangles.
        n_time = 40
        n_freq = 16
        times_arr = np.linspace(0, 400, n_time)
        freqs_arr = np.linspace(5, 40, n_freq)
        T, F = np.meshgrid(times_arr, freqs_arr)
        power = 0.05 + 0.75 * np.exp(-0.5 * ((T - 285) / 45) ** 2) * np.exp(
            -0.5 * ((F - 22) / 14) ** 2
        )
        power += 0.05 * np.exp(-0.5 * ((F - 14) / 8) ** 2)
        power_min = power.min()
        power_max = power.max()
        norm_power = (power - power_min) / (power_max - power_min)

        spectrogram_grid = VGroup()
        cell_w = 0.08
        cell_h = 0.10
        for i in range(n_freq):
            for j in range(n_time):
                p = np.clip(norm_power[i, j], 0.0, 1.0)
                color = interpolate_color(BLUE, YELLOW, p)
                cell = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_width=0,
                )
                spectrogram_grid.add(cell)

        spectrogram_grid.arrange_in_grid(rows=n_freq, cols=n_time, buff=0)
        spectrogram_grid.scale_to_fit_width(3.6)
        if spectrogram_grid.height > 1.8:
            spectrogram_grid.scale_to_fit_height(1.8)
        spectrogram_grid.move_to(tf_panel.get_center())

        tf_freq_label = Text("Frequency", font_size=16, color=GREY)
        tf_freq_label.rotate(PI / 2)
        tf_freq_label.next_to(tf_panel, LEFT, buff=0.15)

        tf_time_label = Text("Time", font_size=16, color=GREY)
        tf_time_label.next_to(tf_panel, DOWN, buff=0.12)

        tf_panel_group = VGroup(
            spectrogram_grid,
            tf_panel,
            tf_freq_label,
            tf_time_label,
        )

        self.play(
            FadeIn(tf_panel_group),
            FadeIn(tf_title),
            run_time=max(0.05, 2.50),
        )
        self.wait(max(0.05, 0.94))

        # ------------------------------------------------------------------
        # Beat 17 | 52.84 - 57.20
        # ------------------------------------------------------------------
        # Highlight the 250-320 ms band on the spectrogram.
        tf_t0 = spectrogram_grid.get_left()[0]
        tf_t400 = spectrogram_grid.get_right()[0]
        x_250 = interpolate(tf_t0, tf_t400, 250 / 400.0)
        x_320 = interpolate(tf_t0, tf_t400, 320 / 400.0)
        band_center_x = (x_250 + x_320) / 2.0

        band_hl = Rectangle(
            width=(x_320 - x_250),
            height=spectrogram_grid.get_height() + 0.12,
            fill_color=YELLOW,
            fill_opacity=0.10,
            stroke_color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.9,
        )
        band_hl.move_to([band_center_x, spectrogram_grid.get_center()[1], 0])

        self.play(tf_title.animate.set_color(YELLOW), run_time=max(0.05, 0.80))
        self.play(FadeIn(band_hl), run_time=max(0.05, 1.20))
        self.play(
            Indicate(band_hl, color=YELLOW, scale_factor=1.1),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 1.36))

        # ------------------------------------------------------------------
        # Beat 18 | 57.20 - 58.02
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.82))