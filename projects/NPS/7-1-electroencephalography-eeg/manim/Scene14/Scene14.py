ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene14(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----- helper: previous scene composition that fades out -----
        prev_deep = Text("Deep sleep", font_size=26, color=WHITE, weight="BOLD").move_to(np.array([-3.0, 2.6, 0]))
        prev_rem = Text("REM sleep", font_size=26, color=PINK, weight="BOLD").move_to(np.array([3.0, 2.6, 0]))
        prev_deep_panel = RoundedRectangle(width=4.4, height=1.2, fill_color=BLACK, fill_opacity=0.5,
                                           stroke_color=PURPLE, stroke_width=1.5).move_to(np.array([-3.0, 0.3, 0]))
        prev_rem_panel = RoundedRectangle(width=4.4, height=1.2, fill_color=BLACK, fill_opacity=0.5,
                                          stroke_color=PINK, stroke_width=1.5).move_to(np.array([3.0, 0.0, 0]))

        # simple line traces in panels
        deep_trace = VMobject().set_stroke(color=YELLOW, width=3, opacity=1)
        deep_trace.set_points_as_corners([
            np.array([-4.8, 0.55, 0]), np.array([-4.2, 0.1, 0]), np.array([-3.6, 0.65, 0]),
            np.array([-3.0, 0.15, 0]), np.array([-2.4, 0.6, 0]), np.array([-1.8, 0.1, 0])
        ])
        rem_trace = VMobject().set_stroke(color=TEAL, width=2, opacity=1)
        rem_trace.set_points_as_corners([
            np.array([1.0, 0.35, 0]), np.array([1.3, -0.25, 0]), np.array([1.7, 0.3, 0]),
            np.array([2.1, -0.2, 0]), np.array([2.5, 0.28, 0]), np.array([2.9, -0.18, 0]),
            np.array([3.3, 0.25, 0]), np.array([3.7, -0.2, 0]), np.array([4.1, 0.3, 0])
        ])

        # simple previous icons
        prev_heart = Circle(radius=0.26, fill_color=RED, fill_opacity=1, stroke_width=0).move_to(np.array([-4.6, -2.2, 0]))
        prev_brain = Circle(radius=0.26, fill_color=PURPLE, fill_opacity=1, stroke_width=0).move_to(np.array([-1.8, -2.5, 0]))
        prev_eye = Ellipse(width=0.6, height=0.35, fill_color=WHITE, fill_opacity=1,
                           stroke_color=WHITE, stroke_width=1).move_to(np.array([1.6, -2.4, 0]))
        prev_muscle = Line(np.array([2.4, -2.0, 0]), np.array([3.0, -2.8, 0]), color=RED, stroke_width=8).move_to(np.array([2.6, -2.4, 0]))
        prev_cloud = VGroup(
            Circle(radius=0.25, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(np.array([-3.4, -2.0, 0])),
            Circle(radius=0.3, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(np.array([-3.0, -2.1, 0])),
            Circle(radius=0.25, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(np.array([-2.6, -2.0, 0]))
        )

        prev_group = VGroup(
            prev_deep, prev_rem, prev_deep_panel, prev_rem_panel,
            deep_trace, rem_trace, prev_heart, prev_brain, prev_eye, prev_muscle, prev_cloud
        )
        prev_group.scale_to_fit_width(11.0)
        self.add(prev_group)

        # ----- raw EEG panel, central -----
        raw_panel_bg = RoundedRectangle(
            corner_radius=0.15, width=7.0, height=3.2,
            fill_color=BLACK, fill_opacity=0.55,
            stroke_color=YELLOW, stroke_width=2,
        ).move_to(ORIGIN)

        raw_label = Text("Raw EEG (all night)", font_size=26, color=WHITE, weight="BOLD")
        raw_label.next_to(raw_panel_bg, UP, buff=0.25)

        raw_panel_group = VGroup(raw_panel_bg, raw_label)

        noise_amt = ValueTracker(1.0)

        raw_wave = VMobject()
        raw_wave.set_stroke(color=YELLOW, width=2.5, opacity=0)

        def update_raw_wave(mob):
            left = raw_panel_bg.get_left()[0] + 0.3
            right = raw_panel_bg.get_right()[0] - 0.3
            cy = raw_panel_bg.get_center()[1]
            u = np.linspace(0, 1, 220)
            xs = left + u * (right - left)

            slow = (0.55 * np.sin(2 * np.pi * 0.8 * u - 1.2)
                    + 0.25 * np.sin(2 * np.pi * 0.35 * u + 2.1))
            fast = (0.12 * np.sin(2 * np.pi * 11.0 * u + 0.4)
                    + 0.07 * np.sin(2 * np.pi * 23.3 * u + 2.5)
                    + 0.05 * np.sin(2 * np.pi * 37.7 * u + 1.1))

            y = slow + noise_amt.get_value() * fast
            mob.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )

        raw_wave.add_updater(update_raw_wave)
        self.add(raw_wave)

        # ----- Beat 1: 0.00-3.50 fade previous composition, central raw panel -----
        self.play(FadeOut(prev_group), run_time=max(0.05, 1.5))
        self.play(FadeIn(raw_panel_bg, raw_label), raw_wave.animate.set_opacity(1), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 0.4))

        # ----- Beat 2: 4.38-7.88 shift left, show empty pipeline -----
        self.wait(max(0.05, 0.88))  # 3.50-4.38

        pipeline_x = -0.3
        block_width = 2.5
        block_height = 0.9
        block_ys = [3.05, 1.55, 0.05, -1.45, -2.95]

        pipeline_blocks = []
        for y in block_ys:
            block = RoundedRectangle(
                corner_radius=0.1,
                width=block_width,
                height=block_height,
                fill_opacity=0,
                stroke_color=GREY_B,
                stroke_width=2,
            ).move_to(np.array([pipeline_x, y, 0]))
            pipeline_blocks.append(block)

        pipeline_arrows = []
        for i in range(4):
            arrow = Arrow(
                pipeline_blocks[i].get_bottom(),
                pipeline_blocks[i + 1].get_top(),
                buff=0.12,
                color=GREY_B,
                stroke_width=3,
            )
            pipeline_arrows.append(arrow)

        pipeline_structure = VGroup(*pipeline_blocks, *pipeline_arrows)

        self.play(
            raw_panel_group.animate.scale(0.55).move_to(np.array([-4.8, -0.2, 0])),
            run_time=max(0.05, 1.2),
        )
        self.play(Create(pipeline_structure), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 0.7))

        # ----- Beat 3: 8.74-12.22 sequential subtle highlights -----
        self.wait(max(0.05, 0.86))  # 7.88-8.74

        per_block_duration = 3.48 / 5.0  # 0.696
        for block in pipeline_blocks:
            self.play(Indicate(block, scale_factor=1.06, color=YELLOW), run_time=max(0.05, 0.55))
            self.wait(max(0.05, 0.146))
        self.wait(max(0.05, 0.78))  # 12.22-13.00

        # ----- Beat 4: 13.00-17.86 Filtering label, smoothing, arrow pulse -----
        filter_label = Text("Filtering", font_size=20, color=WHITE, weight="BOLD").move_to(
            pipeline_blocks[0].get_center() + UP * 0.22
        )
        filter_caption = Text("noise removal", font_size=14, color=GREY).move_to(
            pipeline_blocks[0].get_center() + DOWN * 0.28
        )

        filter_arrow = Arrow(
            raw_panel_bg.get_right(),
            pipeline_blocks[0].get_left(),
            buff=0.25,
            color=YELLOW,
            stroke_width=4,
        )

        self.play(
            pipeline_blocks[0].animate.set_fill(BLUE, opacity=0.35).set_stroke(YELLOW, width=2),
            FadeIn(filter_label),
            FadeIn(filter_caption),
            noise_amt.animate.set_value(0),
            run_time=max(0.05, 2.0),
        )
        self.play(Create(filter_arrow), run_time=max(0.05, 0.7))
        self.play(Indicate(filter_arrow, scale_factor=1.2, color=YELLOW), run_time=max(0.05, 0.6))
        self.play(FadeOut(filter_arrow), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.06))

        # ----- Beat 5: 18.74-27.96 Spectral Analysis + frequency plot -----
        self.wait(max(0.05, 0.88))  # 17.86-18.74

        spectral_label = Text("Spectral Analysis", font_size=18, color=WHITE, weight="BOLD")
        spectral_label.scale_to_fit_width(block_width - 0.4)
        spectral_label.move_to(pipeline_blocks[1].get_center())

        def make_frequency_plot():
            group = VGroup()
            axis = Line(LEFT * 1.4, RIGHT * 1.4, color=GREY_B, stroke_width=2)
            y_axis = Line(LEFT * 1.4, LEFT * 1.4 + UP * 2.0, color=GREY_B, stroke_width=2)
            group.add(axis, y_axis)

            bands = [
                ("delta", -1.15, "0.5–4 Hz", PURPLE, 1.3),
                ("theta", -0.65, "4–8 Hz", BLUE, 0.85),
                ("alpha", -0.2, "8–12 Hz", TEAL, 0.75),
                ("sigma", 0.22, "12–15 Hz", GREEN, 0.55),
                ("beta", 0.8, "15–30 Hz", ORANGE, 0.42),
            ]
            bars = {}

            for name, x, freq_range, color, h in bands:
                bar = Rectangle(
                    width=0.42,
                    height=h,
                    fill_color=color,
                    fill_opacity=0.9,
                    stroke_color=WHITE,
                    stroke_width=1,
                )
                bar.move_to(np.array([x, h / 2.0, 0]))
                bars[name] = bar
                group.add(bar)

                name_label = Text(name, font_size=12, color=WHITE)
                name_label.move_to(np.array([x, 2.1, 0]))
                group.add(name_label)

                range_label = Text(freq_range, font_size=11, color=GREY_B)
                range_label.move_to(np.array([x, -0.35, 0]))
                group.add(range_label)

            x_label = Text("Frequency (Hz)", font_size=15, color=WHITE)
            x_label.move_to(np.array([0, -0.8, 0]))
            group.add(x_label)

            y_label = Text("Power", font_size=15, color=WHITE).rotate(PI / 2)
            y_label.move_to(np.array([-2.0, 1.0, 0]))
            group.add(y_label)

            return group, bars

        freq_plot_group, freq_bars = make_frequency_plot()
        freq_plot_group.move_to(np.array([3.7, 2.5, 0]))

        target_heights = {
            "delta": 1.9,
            "theta": 0.5,
            "alpha": 0.4,
            "sigma": 0.32,
            "beta": 0.25,
        }

        self.play(
            pipeline_blocks[1].animate.set_fill(PURPLE, opacity=0.35).set_stroke(YELLOW, width=2),
            FadeIn(spectral_label),
            run_time=max(0.05, 0.8),
        )
        self.play(FadeIn(freq_plot_group), run_time=max(0.05, 1.4))

        bar_anims = [
            freq_bars[name].animate.stretch_to_fit_height(target_heights[name], about_edge=DOWN)
            for name in target_heights
        ]
        self.play(*bar_anims, run_time=max(0.05, 2.2))
        self.play(Indicate(freq_plot_group, color=YELLOW, scale_factor=1.03), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 4.02))

        # ----- Beat 6: 27.96-39.50 Spectrogram + time-frequency heatmap -----
        spec_label = Text("Spectrogram", font_size=18, color=WHITE, weight="BOLD")
        spec_label.scale_to_fit_width(block_width - 0.4)
        spec_label.move_to(pipeline_blocks[2].get_center())

        def make_heatmap():
            rows, cols = 10, 12
            side = 0.2
            buff = 0.02
            cells = VGroup(*[
                Square(
                    side_length=side,
                    fill_color=BLACK,
                    fill_opacity=1,
                    stroke_color=BLACK,
                    stroke_width=0.5,
                )
                for _ in range(rows * cols)
            ])
            cells.arrange_in_grid(rows=rows, cols=cols, buff=buff)

            # Static power pattern: early night low freq is warm, later mixed bursts.
            # row 0 = 0 Hz (bottom), row rows-1 = 30 Hz (top)
            for r in range(rows):
                for c in range(cols):
                    u = c / (cols - 1)
                    lowfreq = 1 - r / (rows - 1)

                    # Early low-frequency dominance
                    early = 0.85 * np.exp(-((u - 0.15) / 0.35) ** 2) * np.exp(-((lowfreq - 0.85) / 0.28) ** 2)
                    # Spindle/mixed bursts near middle of the night
                    spindle = 0.7 * np.exp(-((u - 0.47) / 0.18) ** 2) * np.exp(-((lowfreq - 0.45) / 0.2) ** 2)
                    # REM-like mixed frequency later
                    rem = 0.6 * np.exp(-((u - 0.80) / 0.22) ** 2) * np.exp(-((lowfreq - 0.2) / 0.22) ** 2)
                    # Wake at end
                    wake = 0.5 * np.exp(-((u - 0.95) / 0.08) ** 2) * (0.3 + 0.5 * lowfreq)

                    power = early + spindle + rem + wake
                    idx = r * cols + c

                    # Map power to a heat color
                    if power < 0.15:
                        color = BLACK
                    elif power < 0.35:
                        color = MAROON
                    elif power < 0.6:
                        color = RED
                    elif power < 0.85:
                        color = ORANGE
                    else:
                        color = YELLOW

                    cells[idx].set_fill(color, opacity=1)

            hz_0 = Text("0 Hz", font_size=13, color=GREY_B)
            hz_0.next_to(cells.get_corner(DL), DOWN, buff=0.2)
            hz_30 = Text("30 Hz", font_size=13, color=GREY_B)
            hz_30.next_to(cells.get_corner(UL), UP, buff=0.2)
            time_label = Text("Time (full night)", font_size=13, color=GREY_B)
            time_label.next_to(cells, DOWN, buff=0.5)

            group = VGroup(cells, hz_0, hz_30, time_label)
            return group, cells

        heatmap_group, heatmap_cells = make_heatmap()
        heatmap_group.move_to(np.array([3.7, -0.5, 0]))
        heatmap_group.set_opacity(0)

        time_cursor = Line(
            heatmap_cells.get_left(),
            heatmap_cells.get_right(),
            color=WHITE,
            stroke_width=2,
        ).move_to(np.array([heatmap_cells.get_left()[0], heatmap_cells.get_center()[1], 0]))

        stage_cols = [1, 3, 5, 8, 10, 11]
        stage_names = ["N3", "N2", "REM", "Wake", "N2", "N3"]

        transition_lines = VGroup()
        stage_labels = VGroup()
        for col, name in zip(stage_cols, stage_names):
            x = heatmap_cells[col].get_center()[0]
            top_y = heatmap_cells.get_top()[1]
            bottom_y = heatmap_cells.get_bottom()[1]
            line = Line(
                np.array([x, top_y, 0]),
                np.array([x, bottom_y, 0]),
                color=WHITE,
                stroke_width=2,
            )
            label = Text(name, font_size=13, color=YELLOW)
            label.move_to(np.array([x, bottom_y - 0.28, 0]))
            transition_lines.add(line)
            stage_labels.add(label)

        self.play(
            pipeline_blocks[2].animate.set_fill(TEAL, opacity=0.35).set_stroke(YELLOW, width=2),
            FadeIn(spec_label),
            run_time=max(0.05, 0.6),
        )
        self.play(FadeIn(heatmap_group), run_time=max(0.05, 0.8))
        self.play(
            time_cursor.animate.move_to(np.array([heatmap_cells.get_right()[0], time_cursor.get_center()[1], 0])),
            run_time=max(0.05, 3.8),
        )
        self.play(FadeIn(transition_lines), FadeIn(stage_labels), run_time=max(0.05, 1.8))
        self.play(Indicate(heatmap_group, color=YELLOW, scale_factor=1.02), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 3.74))

        # ----- Beat 7: 40.32-50.36 Feature Extraction, Classification, ML output -----
        self.wait(max(0.05, 0.82))  # 39.50-40.32

        feat_label = Text("Feature Extraction", font_size=17, color=WHITE, weight="BOLD")
        feat_label.scale_to_fit_width(block_width - 0.25)
        feat_label.move_to(pipeline_blocks[3].get_center() + UP * 0.18)

        class_label = Text("Classification", font_size=17, color=WHITE, weight="BOLD")
        class_label.scale_to_fit_width(block_width - 0.25)
        class_label.move_to(pipeline_blocks[4].get_center() + UP * 0.22)

        def make_feature_table():
            features = ["Feature", "delta power", "theta power", "alpha power",
                        "sigma power", "beta power", "spectral entropy"]
            values = ["Value", "—", "—", "—", "—", "—", "—"]

            col1 = VGroup()
            col2 = VGroup()
            for f, v in zip(features, values):
                f_text = Text(
                    f,
                    font_size=14,
                    color=YELLOW if f == "Feature" else WHITE,
                    weight="BOLD" if f == "Feature" else "NORMAL",
                )
                v_text = Text(
                    v,
                    font_size=14,
                    color=YELLOW if v == "Value" else WHITE,
                    weight="BOLD" if v == "Value" else "NORMAL",
                )
                col1.add(f_text)
                col2.add(v_text)

            col1.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            col2.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            body = VGroup(col1, col2).arrange(RIGHT, buff=0.6)
            border = SurroundingRectangle(body, color=GREY_B, buff=0.22, stroke_width=1.5)
            return VGroup(border, body)

        feature_table = make_feature_table()
        feature_table.scale_to_fit_width(3.1)
        feature_table.move_to(np.array([3.7, -2.25, 0]))

        def make_ml_icon():
            root = Circle(radius=0.1, fill_color=BLUE, fill_opacity=1,
                          stroke_color=WHITE, stroke_width=1).move_to(UP * 0.3)
            left_child = Circle(radius=0.1, fill_color=TEAL, fill_opacity=1,
                                stroke_color=WHITE, stroke_width=1).move_to(DOWN * 0.2 + LEFT * 0.25)
            right_child = Circle(radius=0.1, fill_color=GREEN, fill_opacity=1,
                                 stroke_color=WHITE, stroke_width=1).move_to(DOWN * 0.2 + RIGHT * 0.25)
            e1 = Line(root.get_bottom(), left_child.get_top(), color=WHITE, stroke_width=2)
            e2 = Line(root.get_bottom(), right_child.get_top(), color=WHITE, stroke_width=2)
            graph = VGroup(root, left_child, right_child, e1, e2)
            ml_text = Text("ML algorithm", font_size=12, color=WHITE)
            ml_text.next_to(graph, DOWN, buff=0.06)
            return VGroup(graph, ml_text)

        ml_icon_group = make_ml_icon()
        ml_icon_group.scale_to_fit_width(1.9)
        ml_icon_group.move_to(pipeline_blocks[4].get_center() + DOWN * 0.3)

        stage_out_names = ["Wake", "N1", "N2", "N3", "REM"]
        stage_out_labels = VGroup(*[
            Text(name, font_size=14, color=WHITE) for name in stage_out_names
        ])
        stage_out_labels.arrange(RIGHT, buff=0.28)
        stage_out_labels.move_to(np.array([3.7, -3.5, 0]))
        stage_out_labels.set_opacity(0)

        self.add(stage_out_labels)

        self.play(
            pipeline_blocks[3].animate.set_fill(GREEN, opacity=0.35).set_stroke(YELLOW, width=2),
            pipeline_blocks[4].animate.set_fill(ORANGE, opacity=0.35).set_stroke(YELLOW, width=2),
            FadeIn(feat_label),
            FadeIn(class_label),
            run_time=max(0.05, 0.8),
        )
        self.play(FadeIn(feature_table), run_time=max(0.05, 1.4))
        self.play(FadeIn(ml_icon_group), run_time=max(0.05, 1.2))

        prev_rect = None
        for i, label in enumerate(stage_out_labels):
            anims = [label.animate.set_opacity(1).set_color(YELLOW)]
            if i > 0:
                anims.append(stage_out_labels[i - 1].animate.set_color(GREY))
                if prev_rect is not None:
                    anims.append(FadeOut(prev_rect))
            self.play(*anims, run_time=max(0.05, 0.3))
            prev_rect = SurroundingRectangle(label, color=YELLOW, buff=0.1)
            self.play(Create(prev_rect), run_time=max(0.05, 0.15))
            self.wait(max(0.05, 0.05))

        self.play(Indicate(prev_rect, color=YELLOW, scale_factor=1.1), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 3.64))

        # ----- Beat 8: 50.36-51.10 hold full composition -----
        self.wait(max(0.05, 0.74))