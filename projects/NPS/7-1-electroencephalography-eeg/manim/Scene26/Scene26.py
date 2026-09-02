ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene26(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helper functions ----------
        def make_wave(func, x_min, x_max, color=YELLOW, stroke_width=2.5,
                      num_points=220):
            vm = VMobject()
            vm.set_stroke(color=color, width=stroke_width, opacity=1)
            x = np.linspace(x_min, x_max, num_points)
            y = func(x)
            pts = np.array([x, y, np.zeros_like(x)]).T
            vm.set_points_as_corners(pts)
            return vm

        def make_gaussian_peak(center, amp, sigma, color, x_min=-0.55,
                               x_max=0.55, num_points=100):
            vm = VMobject()
            vm.set_stroke(color=color, width=2, opacity=1)
            x = np.linspace(x_min, x_max, num_points)
            y = amp * np.exp(-((x - center) / sigma) ** 2)
            vm.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return vm

        def make_jagged(color, width=0.35):
            vm = VMobject()
            vm.set_stroke(color=color, width=2.5, opacity=1)
            pts = [[-0.5, 0, 0], [-0.25, 0.18, 0], [0, 0, 0],
                   [0.2, 0.16, 0], [0.4, -0.05, 0], [0.5, 0, 0]]
            vm.set_points_as_corners(np.array(pts))
            vm.scale_to_fit_width(width)
            return vm

        def make_funnel_icon():
            funnel = Polygon(
                LEFT * 0.32 + UP * 0.3,
                RIGHT * 0.32 + UP * 0.3,
                RIGHT * 0.1 + DOWN * 0.3,
                LEFT * 0.1 + DOWN * 0.3,
                fill_color=BLUE, fill_opacity=0.5,
                stroke_color=WHITE, stroke_width=2,
            )
            label = Text("Filter", font_size=13, color=WHITE)
            return VGroup(funnel, label).arrange(DOWN, buff=0.06)

        def make_artifacts():
            j1 = make_jagged(ORANGE, width=0.28)
            j2 = make_jagged(PINK, width=0.28).scale(0.8)
            drift1 = make_wave(lambda x: 0.09 * np.sin(2 * np.pi * 2 * x),
                               -0.32, 0.32, color=PINK, stroke_width=2)
            drift2 = make_wave(lambda x: 0.07 * np.sin(2 * np.pi * 1.5 * x),
                               -0.3, 0.3, color=ORANGE, stroke_width=2)
            return VGroup(j1, j2, drift1, drift2).arrange(RIGHT, buff=0.1)

        # ---------- Beat 1: raw waveform enters lower portion ----------
        prog_line = Line(LEFT * 6.2, RIGHT * 6.2, color=GREY_B, stroke_width=2)
        prog_line.move_to(np.array([0, 0.6, 0]))
        self.add(prog_line)

        raw_eeg = make_wave(
            lambda x: 0.28 * np.sin(2 * np.pi * 1.3 * x)
            + 0.20 * np.sin(2 * np.pi * 5.7 * x)
            + 0.14 * np.sin(2 * np.pi * 13.0 * x),
            -6.2, 6.2, color=GREY_B, stroke_width=2.0,
        )
        raw_eeg.move_to(np.array([0, -2.0, 0]))
        self.play(Create(raw_eeg), run_time=max(0.05, 1.62))

        # ---------- Beat 2: arrow appears + waveform shifts toward line ----------
        beat2_arrow = Arrow(
            np.array([3.0, 0.6, 0]),
            np.array([4.4, 0.6, 0]),
            color=GREY_B, stroke_width=3, buff=0.0,
        )
        self.play(
            Create(beat2_arrow),
            raw_eeg.animate.shift(UP * 1.6),
            run_time=max(0.05, 2.60),
        )

        self.wait(max(0.05, 0.48))  # gap 4.22-4.70

        # ---------- Beat 3: waveform moves onto progression line, brightens ----------
        self.play(
            raw_eeg.animate.shift(UP * 1.0).set_color(YELLOW).set_stroke(width=4),
            run_time=max(0.05, 3.38),
        )

        # ---------- Beat 4: amplitude grows, jitter, annotations ----------
        self.play(
            raw_eeg.animate.stretch(1.25, dim=1),
            run_time=max(0.05, 0.80),
        )
        for _ in range(3):
            self.play(raw_eeg.animate.shift(UP * 0.03), run_time=max(0.05, 0.15))
            self.play(raw_eeg.animate.shift(DOWN * 0.03), run_time=max(0.05, 0.15))

        ann_var = VGroup(
            make_jagged(ORANGE, width=0.35),
            Text("High Variability", font_size=18, color=ORANGE, weight="BOLD"),
        ).arrange(DOWN, buff=0.08)
        ann_var.move_to(raw_eeg.get_center() + LEFT * 1.5 + UP * 0.85)

        ann_noise = VGroup(
            make_jagged(PINK, width=0.35),
            Text("Noise", font_size=18, color=PINK, weight="BOLD"),
        ).arrange(DOWN, buff=0.08)
        ann_noise.move_to(raw_eeg.get_center() + RIGHT * 1.5 + UP * 0.85)

        self.play(FadeIn(ann_var), FadeIn(ann_noise), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 1.58))  # hold annotations through the jitter description

        # ---------- Beat 5: five blocks fade in sequentially ----------
        self.play(FadeOut(ann_var), FadeOut(ann_noise), run_time=max(0.05, 0.30))

        block_colors = [BLUE, TEAL, GREEN, PURPLE, ORANGE]
        labels_text = [
            "Filtering",
            "Spectral Analysis",
            "Time-Frequency Analysis",
            "Feature Extraction",
            "Machine Learning",
        ]
        block_xs = [-5.0, -2.5, 0.0, 2.5, 5.0]

        block_rects = []
        block_labels = []
        block_groups = []
        for i, lab_text in enumerate(labels_text):
            rect = RoundedRectangle(
                width=2.2, height=1.0, corner_radius=0.1,
                fill_color=GREY_B, fill_opacity=0.12,
                stroke_color=GREY_B, stroke_width=2.5,
            )
            rect.move_to(np.array([block_xs[i], 0.6, 0]))
            lab = Text(lab_text, font_size=15, weight="BOLD", color=GREY_B)
            lab.scale_to_fit_width(1.8)
            lab.move_to(rect.get_center())
            group = VGroup(rect, lab)
            block_rects.append(rect)
            block_labels.append(lab)
            block_groups.append(group)

        block_fade_time = 0.5
        for block_group in block_groups:
            self.play(FadeIn(block_group), run_time=max(0.05, block_fade_time))

        short_raw_wave = make_wave(
            lambda x: 0.12 * np.sin(2 * np.pi * 4 * x)
            + 0.10 * np.sin(2 * np.pi * 11 * x)
            + 0.08 * np.sin(2 * np.pi * 19 * x),
            -0.8, 0.8, color=YELLOW, stroke_width=3,
        )
        short_raw_wave.scale_to_fit_width(1.6)
        short_raw_wave.move_to(block_rects[0].get_left() + RIGHT * 0.4)
        self.play(Transform(raw_eeg, short_raw_wave), run_time=max(0.05, 0.62))

        self.wait(max(0.05, 0.86))  # gap 16.46-17.32

        # ---------- Beat 6: Filtering block ----------
        filter_icon = make_funnel_icon()
        filter_icon.scale_to_fit_height(0.5)
        filter_icon.move_to(block_rects[0].get_center() + DOWN * 0.1)

        clean_center_wave = make_wave(
            lambda x: 0.09 * np.sin(2 * np.pi * 1.8 * x),
            -0.8, 0.8, color=GREEN, stroke_width=3.5,
        )
        clean_center_wave.scale_to_fit_width(1.6)
        clean_center_wave.move_to(block_rects[0].get_center() + DOWN * 0.1)

        artifacts = make_artifacts()
        artifacts.scale_to_fit_width(0.9)
        artifacts.move_to(block_rects[0].get_center() + LEFT * 0.4 + DOWN * 0.05)

        # light block 0
        self.play(
            block_rects[0].animate.set_stroke(BLUE, width=4).set_fill(BLUE, opacity=0.25).scale(1.1),
            run_time=max(0.05, 0.6),
        )
        self.play(
            block_labels[0].animate.set_color(WHITE).move_to(
                block_rects[0].get_top() + DOWN * 0.22
            ),
            run_time=max(0.05, 0.4),
        )

        self.play(FadeIn(filter_icon), run_time=max(0.05, 0.4))
        self.play(raw_eeg.animate.move_to(block_rects[0].get_center() + LEFT * 0.1),
                  run_time=max(0.05, 0.5))
        self.play(
            Transform(raw_eeg, clean_center_wave),
            FadeOut(artifacts, shift=RIGHT * 0.5 + UP * 0.3),
            run_time=max(0.05, 0.6),
        )
        self.play(raw_eeg.animate.move_to(block_rects[0].get_right() + LEFT * 0.3),
                  run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.64))  # fill beat 6 to 20.96

        self.wait(max(0.05, 0.96))  # gap 20.96-21.92

        # ---------- Beat 7: Spectral Analysis block ----------
        # build spectrum plot inside block 1
        ax_x = Line(LEFT * 0.7, RIGHT * 0.7, color=GREY_B, stroke_width=2)
        ax_y = Line(UP * 0.35, DOWN * 0.35, color=GREY_B, stroke_width=2)
        ax_x.move_to(DOWN * 0.28)
        ax_y.move_to(LEFT * 0.7)
        freq_lab = Text("Frequency", font_size=10, color=GREY_B)
        freq_lab.next_to(ax_x, DOWN, buff=0.04)
        power_lab = Text("Power", font_size=10, color=GREY_B).rotate(90 * DEGREES)
        power_lab.next_to(ax_y, LEFT, buff=0.04)

        peak_alpha = make_gaussian_peak(-0.22, 0.26, 0.09, BLUE)
        peak_beta = make_gaussian_peak(0.04, 0.24, 0.08, GREEN)
        peak_theta = make_gaussian_peak(0.34, 0.22, 0.10, ORANGE)
        alpha_lab = Text("Alpha", font_size=11, color=BLUE).next_to(
            peak_alpha, UP, buff=0.03
        )
        beta_lab = Text("Beta", font_size=11, color=GREEN).next_to(
            peak_beta, UP, buff=0.03
        )
        theta_lab = Text("Theta", font_size=11, color=ORANGE).next_to(
            peak_theta, UP, buff=0.03
        )
        peaks_group = VGroup(peak_alpha, peak_beta, peak_theta)

        spectrum_group = VGroup(
            ax_x, ax_y, freq_lab, power_lab,
            peak_alpha, peak_beta, peak_theta,
            alpha_lab, beta_lab, theta_lab,
        )
        spectrum_group.scale_to_fit_width(1.7)
        spectrum_group.scale_to_fit_height(0.75)
        spectrum_group.move_to(block_rects[1].get_center() + DOWN * 0.08)

        # light block 1
        self.play(
            block_rects[1].animate.set_stroke(TEAL, width=4).set_fill(TEAL, opacity=0.25).scale(1.1),
            run_time=max(0.05, 0.6),
        )
        self.play(
            block_labels[1].animate.set_color(WHITE).move_to(
                block_rects[1].get_top() + DOWN * 0.22
            ),
            run_time=max(0.05, 0.4),
        )

        self.play(raw_eeg.animate.move_to(block_rects[1].get_center() + LEFT * 0.1),
                  run_time=max(0.05, 0.9))
        self.play(FadeIn(spectrum_group), run_time=max(0.05, 1.2))

        source_pt = raw_eeg.get_right() + UP * 0.05
        target_pt = spectrum_group.get_left() + UP * 0.2
        arr_to_spec_1 = Arrow(source_pt, target_pt, color=WHITE, stroke_width=2,
                              buff=0.05)
        arr_to_spec_2 = Arrow(
            raw_eeg.get_left() + UP * 0.05,
            spectrum_group.get_left() + DOWN * 0.15,
            color=WHITE, stroke_width=2, buff=0.05,
        )
        self.play(Create(arr_to_spec_1), Create(arr_to_spec_2), run_time=max(0.05, 0.8))

        # subtle peak adjustment
        self.play(peaks_group.animate.shift(RIGHT * 0.06), run_time=max(0.05, 0.5))
        self.play(peaks_group.animate.shift(LEFT * 0.06), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.14))  # fill beat 7 to 27.96

        self.wait(max(0.05, 0.74))  # gap 27.96-28.70

        # ---------- Beat 8: Time-Frequency Analysis block ----------
        # build heatmap
        heat_cols, heat_rows = 8, 5
        cell_w, cell_h = 0.15, 0.11
        heat_colors = [BLUE, TEAL, GREEN, ORANGE, YELLOW, PURPLE, PINK, RED]
        heat_cells = VGroup()
        for j in range(heat_rows):
            for i in range(heat_cols):
                cell = Rectangle(
                    width=cell_w, height=cell_h,
                    fill_color=heat_colors[(i + j) % len(heat_colors)],
                    fill_opacity=0.4 + 0.5 * (j / max(1, heat_rows - 1)),
                    stroke_color=GREY_B, stroke_width=0.6,
                )
                heat_cells.add(cell)
        heat_cells.arrange_in_grid(rows=heat_rows, cols=heat_cols, buff=0.025)
        heatmap_group = VGroup(heat_cells)
        heatmap_group.scale_to_fit_width(1.5)
        heatmap_group.scale_to_fit_height(0.7)
        heatmap_group.move_to(block_rects[2].get_center() + DOWN * 0.08)

        # bright vertical stripe
        heat_stripe = Rectangle(
            width=cell_w * 1.05,
            height=heatmap_group.get_height(),
            fill_color=YELLOW, fill_opacity=0.8, stroke_width=0,
        )
        heat_stripe.move_to(heatmap_group.get_left() + RIGHT * cell_w * 0.5)

        stft_label = Text("STFT", font_size=14, color=YELLOW, weight="BOLD")
        wavelet_label = Text("Wavelet Analysis", font_size=14, color=WHITE,
                             weight="BOLD")

        # light block 2
        self.play(
            block_rects[2].animate.set_stroke(GREEN, width=4).set_fill(GREEN, opacity=0.25).scale(1.1),
            run_time=max(0.05, 0.6),
        )
        self.play(
            block_labels[2].animate.set_color(WHITE).move_to(
                block_rects[2].get_top() + DOWN * 0.22
            ),
            run_time=max(0.05, 0.4),
        )

        self.play(raw_eeg.animate.move_to(block_rects[2].get_center() + LEFT * 0.1),
                  run_time=max(0.05, 0.8))
        self.play(FadeIn(heatmap_group), run_time=max(0.05, 1.2))

        stft_label.move_to(block_rects[2].get_center() + UP * 0.28 + LEFT * 0.3)
        self.play(FadeIn(stft_label), run_time=max(0.05, 0.5))

        self.add(heat_stripe)
        self.play(heat_stripe.animate.move_to(heatmap_group.get_right() - RIGHT * cell_w * 0.5),
                  run_time=max(0.05, 1.5))

        wavelet_label.next_to(stft_label, RIGHT, buff=0.2)
        self.play(FadeIn(wavelet_label), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.36))  # fill beat 8 to 35.56

        self.wait(max(0.05, 0.90))  # gap 35.56-36.46

        # ---------- Beat 9: Feature Extraction block ----------
        feature_names = ["Band Power", "Frequency Ratio",
                         "Wavelet Coefficient", "P300 Amplitude"]
        feature_values = ["12.4", "1.8", "0.72", "5.3"]
        table_rows = VGroup()
        for name, val in zip(feature_names, feature_values):
            row_rect = Rectangle(
                width=1.8, height=0.22,
                fill_color=BLUE, fill_opacity=0.15,
                stroke_color=GREY_B, stroke_width=1.5,
            )
            lab = Text(name, font_size=11, color=WHITE)
            lab.scale_to_fit_width(0.65)
            lab.move_to(row_rect.get_left() + RIGHT * 0.2)
            val_text = Text(val, font_size=11, color=YELLOW, weight="BOLD")
            val_text.scale_to_fit_width(0.4)
            val_text.move_to(row_rect.get_right() + LEFT * 0.2)
            row = VGroup(row_rect, lab, val_text)
            table_rows.add(row)
        table_rows.arrange(DOWN, buff=0.07)
        feature_table = VGroup(table_rows)
        feature_table.scale_to_fit_width(1.7)
        feature_table.scale_to_fit_height(0.8)
        feature_table.move_to(block_rects[3].get_center())

        # light block 3
        self.play(
            block_rects[3].animate.set_stroke(PURPLE, width=4).set_fill(PURPLE, opacity=0.25).scale(1.1),
            run_time=max(0.05, 0.6),
        )
        self.play(
            block_labels[3].animate.set_color(WHITE).move_to(
                block_rects[3].get_top() + DOWN * 0.22
            ),
            run_time=max(0.05, 0.4),
        )

        self.play(
            raw_eeg.animate.move_to(block_rects[3].get_center() + LEFT * 0.1),
            heatmap_group.animate.move_to(block_rects[3].get_center() + RIGHT * 0.1),
            run_time=max(0.05, 0.8),
        )

        flow_group = VGroup(raw_eeg, heatmap_group)
        self.play(ReplacementTransform(flow_group, feature_table), run_time=max(0.05, 1.2))

        for row in table_rows:
            self.play(Indicate(row, color=YELLOW), run_time=max(0.05, 0.55))

        self.wait(max(0.05, 1.06))  # fill beat 9 to 42.72

        self.wait(max(0.05, 1.04))  # gap 42.72-43.76

        # ---------- Beat 10: Machine Learning block ----------
        # classification plot
        plot_ax_x = Line(LEFT * 0.7, RIGHT * 0.7, color=GREY_B, stroke_width=2)
        plot_ax_y = Line(UP * 0.4, DOWN * 0.4, color=GREY_B, stroke_width=2)
        plot_ax_x.move_to(DOWN * 0.3)
        plot_ax_y.move_to(LEFT * 0.7)

        cluster_a = VGroup(*[
            Dot(np.array([-0.4 + dx, 0.15 + dy, 0]), radius=0.04, color=BLUE)
            for dx, dy in [(0.1, 0.06), (-0.08, 0.02), (0.05, -0.1),
                           (0.16, 0.0), (-0.15, -0.05)]
        ])
        cluster_b = VGroup(*[
            Dot(np.array([0.35 + dx, -0.2 + dy, 0]), radius=0.04, color=ORANGE)
            for dx, dy in [(0.1, 0.05), (-0.05, 0.03), (0.08, -0.1),
                           (0.18, -0.02), (-0.12, -0.09)]
        ])
        boundary_line = Line(
            np.array([-0.7, 0.55, 0]),
            np.array([0.7, -0.55, 0]),
            color=WHITE, stroke_width=3,
        )

        class_plot = VGroup(plot_ax_x, plot_ax_y, cluster_a, cluster_b,
                            boundary_line)
        class_plot.scale_to_fit_width(1.7)
        class_plot.scale_to_fit_height(0.8)
        class_plot.move_to(block_rects[4].get_center())

        # light block 4
        self.play(
            block_rects[4].animate.set_stroke(ORANGE, width=4).set_fill(ORANGE, opacity=0.25).scale(1.1),
            run_time=max(0.05, 0.6),
        )
        self.play(
            block_labels[4].animate.set_color(WHITE).move_to(
                block_rects[4].get_top() + DOWN * 0.22
            ),
            run_time=max(0.05, 0.4),
        )

        self.play(feature_table.animate.move_to(block_rects[4].get_center()),
                  run_time=max(0.05, 0.8))
        self.play(ReplacementTransform(feature_table, class_plot), run_time=max(0.05, 1.1))

        cmd_arrow = Arrow(
            block_rects[4].get_right() + RIGHT * 0.05,
            block_rects[4].get_right() + RIGHT * 1.9,
            color=ORANGE, stroke_width=8, buff=0.05,
        )
        cmd_label = Text("Control Command", font_size=18, color=ORANGE,
                         weight="BOLD").next_to(cmd_arrow, UP, buff=0.1)
        cmd_group = VGroup(cmd_arrow, cmd_label)

        self.play(FadeIn(cmd_group), run_time=max(0.05, 0.8))
        self.play(cmd_group.animate.scale(1.15), run_time=max(0.05, 0.45))
        self.play(cmd_group.animate.scale(1 / 1.15), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 2.08))  # fill beat 10 to 50.44

        self.wait(max(0.05, 0.84))  # gap 50.44-51.28

        # ---------- Beat 11: unified pipeline, gentle pulse ----------
        connect_arrows = VGroup(*[
            Arrow(
                block_rects[i].get_right() + RIGHT * 0.02,
                block_rects[i + 1].get_left() + LEFT * 0.02,
                color=GREY_B, stroke_width=3, buff=0.02,
            )
            for i in range(4)
        ])
        self.play(FadeIn(connect_arrows), run_time=max(0.05, 0.6))

        final_raw_wave = make_wave(
            lambda x: 0.10 * np.sin(2 * np.pi * 4 * x)
            + 0.08 * np.sin(2 * np.pi * 11 * x)
            + 0.07 * np.sin(2 * np.pi * 19 * x),
            -0.8, 0.8, color=YELLOW, stroke_width=3,
        )
        final_raw_wave.scale_to_fit_width(1.2)
        final_raw_wave.move_to(block_rects[0].get_left() + LEFT * 0.25)
        self.play(Create(final_raw_wave), run_time=max(0.05, 0.7))

        pulse_colors = [BLUE, TEAL, GREEN, PURPLE, ORANGE]
        self.play(
            *[
                rect.animate.set_fill(color, opacity=0.45).set_stroke(color, width=6)
                for rect, color in zip(block_rects, pulse_colors)
            ],
            run_time=max(0.05, 0.8),
        )
        self.play(
            *[
                rect.animate.set_fill(color, opacity=0.25).set_stroke(color, width=4)
                for rect, color in zip(block_rects, pulse_colors)
            ],
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 2.4))  # hold steadily through final 56.58 mark