ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------
        # Constants for the two-panel comparison layout
        # ----------------------------------------------------------
        axis_width = 5.0
        y_time = -2.2
        left_x0 = -6.1
        left_x1 = left_x0 + axis_width
        right_x0 = 1.1
        right_x1 = right_x0 + axis_width

        y_epoch_bases = [-1.4, -0.75, -0.1, 0.55, 1.2]
        amp_epoch = 0.42

        left_latencies = [100, 100, 100, 100, 100]  # ms
        right_latencies = [80, 170, 240, 320, 360]  # ms

        # ----------------------------------------------------------
        # Placeholder for the final image of the previous scene
        # ----------------------------------------------------------
        def build_previous_final():
            prev_left = VGroup()
            prev_cols = [TEAL, BLUE, ORANGE]
            prev_xs = [-1.25, -0.20, -0.80]
            prev_ybs = [1.0, 0.2, -0.6]
            for xc, yb, col in zip(prev_xs, prev_ybs, prev_cols):
                def wave(x, xc=xc, yb=yb):
                    return yb + 0.6 * np.exp(-0.5 * ((x - xc) / 0.24) ** 2)

                graph = FunctionGraph(
                    wave,
                    x_range=[-2.6, 0.4, 0.02],
                    color=col,
                )
                graph.set_stroke(color=col, width=3, opacity=0.9)
                prev_left.add(graph)

            prev_avg_rect = Rectangle(
                width=3.6,
                height=2.4,
                fill_color=BLACK,
                fill_opacity=0.30,
                stroke_color=GREY_B,
                stroke_width=2,
            ).move_to([2.7, 1.1, 0])

            def avg_wave(x):
                return 1.0 + 0.45 * np.exp(-0.5 * ((x - 3.4) / 0.30) ** 2)

            prev_avg_wave = FunctionGraph(
                avg_wave,
                x_range=[0.9, 4.5, 0.02],
                color=YELLOW,
            )
            prev_avg_wave.set_stroke(color=YELLOW, width=3, opacity=0.9)

            prev_spec_rect = Rectangle(
                width=3.6,
                height=2.0,
                fill_color=BLUE,
                fill_opacity=0.25,
                stroke_color=GREY_B,
                stroke_width=2,
            ).move_to([2.7, -1.8, 0])

            spec_bars = VGroup()
            bar_cols = [TEAL, ORANGE, YELLOW, BLUE]
            for i in range(6):
                for j in range(8):
                    cell = Rectangle(
                        width=0.34,
                        height=0.28,
                        fill_color=bar_cols[(i + j) % len(bar_cols)],
                        fill_opacity=0.85,
                        stroke_width=0,
                    )
                    cell.move_to([1.05 + 0.34 * j, -2.65 + 0.28 * i, 0])
                    spec_bars.add(cell)

            return VGroup(
                prev_left,
                prev_avg_rect,
                prev_avg_wave,
                prev_spec_rect,
                spec_bars,
            )

        prev_final = build_previous_final()
        self.add(prev_final)

        center_line = Line(
            [0, 3.4, 0],
            [0, -3.4, 0],
            color=GREY_B,
            stroke_width=2,
            stroke_opacity=0.7,
        )

        self.play(
            FadeOut(prev_final),
            FadeIn(center_line),
            run_time=max(0.05, 1.86),
        )

        # ----------------------------------------------------------
        # Beat 2: time axes in both panels
        # ----------------------------------------------------------
        def make_time_axis(x_start, x_end, y_axis):
            axis = Line(
                [x_start, y_axis, 0],
                [x_end, y_axis, 0],
                color=GREY,
                stroke_width=3,
                stroke_opacity=0.7,
            )
            ticks = VGroup()
            labels = VGroup()
            tick_label_texts = ["0", "100 ms", "200 ms", "300 ms", "400 ms"]
            for i, label_str in enumerate(tick_label_texts):
                x_tick = x_start + i * (x_end - x_start) / 4.0
                tick = Line(
                    [x_tick, y_axis - 0.10, 0],
                    [x_tick, y_axis + 0.10, 0],
                    color=GREY,
                    stroke_width=3,
                )
                label = Text(label_str, font_size=18, color=GREY).next_to(
                    tick, DOWN, buff=0.08
                )
                ticks.add(tick)
                labels.add(label)
            return VGroup(axis, ticks, labels)

        left_time_group = make_time_axis(left_x0, left_x1, y_time)
        right_time_group = make_time_axis(right_x0, right_x1, y_time)

        self.play(
            FadeIn(left_time_group),
            FadeIn(right_time_group),
            run_time=max(0.05, 1.60),
        )

        # ----------------------------------------------------------
        # Beat 3: five epochs stacked in each panel
        # ----------------------------------------------------------
        def make_epochs(x_start, x_end, y_bases, latencies_ms, color):
            graphs = []
            for yb, lat_ms in zip(y_bases, latencies_ms):
                x_lat = x_start + (lat_ms / 400.0) * (x_end - x_start)
                sigma = 0.22

                def wave(x, x_lat=x_lat, yb=yb):
                    return yb + amp_epoch * np.exp(-0.5 * ((x - x_lat) / sigma) ** 2)

                graph = FunctionGraph(
                    wave,
                    x_range=[x_start, x_end, 0.015],
                    color=color,
                )
                graph.set_stroke(color=color, width=3, opacity=0.95)
                graphs.append(graph)
            return VGroup(*graphs)

        left_epochs = make_epochs(
            left_x0, left_x1, y_epoch_bases, left_latencies, TEAL
        )
        right_epochs = make_epochs(
            right_x0, right_x1, y_epoch_bases, right_latencies, ORANGE
        )

        self.play(
            FadeIn(left_epochs),
            FadeIn(right_epochs),
            run_time=max(0.05, 2.12),
        )

        # ----------------------------------------------------------
        # Beat 4: vertical dashed line through the left deflections
        # ----------------------------------------------------------
        left_lat_x = left_x0 + (100 / 400.0) * (left_x1 - left_x0)
        dashed_line = DashedLine(
            [left_lat_x, 1.8, 0],
            [left_lat_x, -1.15, 0],
            dash_length=0.1,
            stroke_color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.9,
        )

        self.play(FadeIn(dashed_line), run_time=max(0.05, 2.62))

        # ----------------------------------------------------------
        # Beat 5: brighten left panel, highlight line, add left label
        # ----------------------------------------------------------
        left_highlight_rect = Rectangle(
            width=6.3,
            height=6.0,
            fill_color=WHITE,
            fill_opacity=0.03,
            stroke_width=0,
        ).move_to([-3.2, 0.0, 0])

        label_left = Text(
            "Time-Locked: Consistent Timing",
            font_size=26,
            color=WHITE,
            weight="BOLD",
            t2c={"Time-Locked": TEAL},
        ).scale_to_fit_width(5.8)
        label_left.move_to([-3.0, 2.7, 0])

        self.play(
            FadeIn(left_highlight_rect),
            dashed_line.animate.set_stroke(color=GOLD, width=5, opacity=1),
            run_time=max(0.05, 1.5),
        )
        self.play(FadeIn(label_left), run_time=max(0.05, 1.0))
        self.play(
            Indicate(dashed_line, color=GOLD, scale_factor=1.1),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.82))

        # Small pause to align with the brief's beat boundary
        self.wait(max(0.05, 0.02))

        # ----------------------------------------------------------
        # Beat 6: right label, dim left, highlight right deflections
        # ----------------------------------------------------------
        label_right = Text(
            "Induced: Variable Timing",
            font_size=26,
            color=WHITE,
            weight="BOLD",
            t2c={"Induced": ORANGE},
        ).scale_to_fit_width(5.8)
        label_right.move_to([3.0, 2.7, 0])

        left_group = VGroup(
            left_time_group,
            left_epochs,
            dashed_line,
            left_highlight_rect,
            label_left,
        )

        self.play(
            FadeIn(label_right),
            left_group.animate.set_opacity(0.5),
            run_time=max(0.05, 0.7),
        )

        # Marker dots for each right deflection's peak
        right_markers = []
        for i in range(5):
            x_peak = right_x0 + (right_latencies[i] / 400.0) * (
                right_x1 - right_x0
            )
            y_peak = y_epoch_bases[i] + amp_epoch
            right_markers.append(
                Dot([x_peak, y_peak, 0], radius=0.07, color=YELLOW, fill_opacity=1)
            )

        per_item = 0.492
        for i in range(5):
            self.play(
                GrowFromCenter(right_markers[i]),
                Indicate(right_epochs[i], color=YELLOW, scale_factor=1.12),
                run_time=max(0.05, 0.35),
            )
            self.wait(max(0.05, 0.142))

        # ----------------------------------------------------------
        # Beat 7: final hold
        # ----------------------------------------------------------
        self.wait(max(0.05, 0.78))