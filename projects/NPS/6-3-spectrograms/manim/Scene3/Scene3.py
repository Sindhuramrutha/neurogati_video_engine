ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def make_waveform(self):
        x_min, x_max = -8.5, 8.5
        step = 0.12
        xs = np.arange(x_min, x_max + step, step)
        ys = (
            1.55
            + 0.42 * np.sin(2 * np.pi * 0.85 * xs - 1.2)
            + 0.18 * np.sin(2 * np.pi * 1.7 * xs + 0.5)
        )
        lines = []
        for k in range(len(xs) - 1):
            lines.append(
                Line(
                    np.array([xs[k], ys[k], 0]),
                    np.array([xs[k + 1], ys[k + 1], 0]),
                    stroke_color=GREY,
                    stroke_width=2,
                )
            )
        wave = VGroup(*lines)
        wave.set_stroke(color=GREY, width=2, opacity=0.9)
        wave.set_z_index(4)
        return wave

    def make_spectrum(self, i):
        height = 1.5
        half_h = height / 2
        axis_x = -0.55
        axis = Line(
            np.array([axis_x, -half_h, 0]),
            np.array([axis_x, half_h, 0]),
            color=GREY_B,
            stroke_width=1.6,
        )
        peaks = [0.22, 0.58, 0.72, 0.30, 0.80]
        second = [0.65, 0.25, 0.45, 0.75, 0.55]
        widths = [0.15, 0.12, 0.18, 0.10, 0.14]
        n_points = 22
        pts = []
        for j in range(n_points):
            f = j / (n_points - 1)
            y = -half_h + f * height
            amp = np.exp(-((f - peaks[i]) ** 2) / (2 * widths[i] ** 2))
            amp += 0.35 * np.exp(-((f - second[i]) ** 2) / (2 * 0.08 ** 2))
            x = axis_x + 0.15 + 0.80 * amp
            pts.append(np.array([x, y, 0]))
        curve = VGroup(
            *[
                Line(pts[j], pts[j + 1], color=WHITE, stroke_width=2.5)
                for j in range(len(pts) - 1)
            ]
        )
        spec_group = VGroup(axis, curve)
        spec_group.set_z_index(3)
        return spec_group

    def make_color_column(self, i, width, height):
        bins = 10
        gradient = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED]
        peaks = [0.20, 0.50, 0.75, 0.34, 0.85]
        widths = [0.18, 0.14, 0.12, 0.16, 0.10]
        column = VGroup()
        for j in range(bins):
            f = j / (bins - 1)
            intensity = np.exp(-((f - peaks[i]) ** 2) / (2 * widths[i] ** 2))
            intensity += 0.25 * np.exp(-((f - 0.55) ** 2) / (2 * 0.08 ** 2))
            intensity = min(1.0, intensity)
            color_idx = int(min(1.0, intensity) * (len(gradient) - 1))
            color = gradient[color_idx]
            rect = Rectangle(
                width=width,
                height=height / bins,
                fill_color=color,
                fill_opacity=0.2 + 0.8 * intensity,
                stroke_width=0,
            )
            rect.move_to(
                np.array([0, -height / 2 + (j + 0.5) * height / bins, 0])
            )
            column.add(rect)
        return column

    def build_smooth_spectrogram(self, width=10.0, height=1.8):
        n_cols = 30
        n_bins = 12
        col_width = width / n_cols
        row_height = height / n_bins
        img = VGroup()
        for i in range(n_cols):
            t_val = i / (n_cols - 1)
            center_freq = 2.0 + 2.5 * t_val + 1.8 * np.sin(2 * np.pi * (t_val - 0.2))
            for j in range(n_bins):
                freq = 1.0 + (8.0 - 1.0) * j / (n_bins - 1)
                intensity = np.exp(-((freq - center_freq) ** 2) / (2 * 0.65 ** 2))
                intensity2 = 0.55 * np.exp(
                    -((freq - (center_freq + 5 * np.exp(-((t_val - 0.7) / 0.2) ** 2))) ** 2)
                    / (2 * 0.5 ** 2)
                )
                intensity = max(intensity, intensity2)
                gradient = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED]
                color_idx = int(min(1.0, intensity) * (len(gradient) - 1))
                color = gradient[color_idx]
                rect = Rectangle(
                    width=col_width,
                    height=row_height,
                    fill_color=color,
                    fill_opacity=0.25 + 0.75 * min(1.0, intensity),
                    stroke_width=0,
                )
                rect.move_to(
                    np.array(
                        [
                            -width / 2 + col_width * (i + 0.5),
                            -height / 2 + row_height * (j + 0.5),
                            0,
                        ]
                    )
                )
                img.add(rect)
        img.set_z_index(2)
        return img

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----- Beat 1: 0.00–5.34 -----
        waveform = self.make_waveform()
        waveform.shift(LEFT * 12)
        self.add(waveform)
        self.play(waveform.animate.shift(RIGHT * 12), run_time=max(0.05, 3.40))
        self.wait(max(0.05, 0.10))

        # Four step circles
        step_circles = []
        step_number_texts = []
        step_circle_group = VGroup()
        for k in range(4):
            c = Circle(
                radius=0.20,
                fill_color=GREY,
                fill_opacity=0.30,
                stroke_color=GREY,
                stroke_width=1.5,
            )
            n = Text(str(k + 1), font_size=18, color=WHITE, weight=BOLD)
            n.move_to(c.get_center())
            step_circles.append(c)
            step_number_texts.append(n)
            step_circle_group.add(VGroup(c, n))
        step_circle_group.arrange(RIGHT, buff=0.55)
        step_circle_group.move_to(np.array([0, -3.25, 0]))
        self.play(FadeIn(step_circle_group), run_time=max(0.05, 1.84))

        # ----- wait to 6.20 -----
        self.wait(max(0.05, 0.86))

        # ----- Beat 2: 6.20–8.40 -----
        step1_label = (
            Text("Step 1: Divide the signal into short windows", font_size=24, color=WHITE)
            .scale_to_fit_width(11)
            .to_edge(UP, buff=0.50)
        )
        self.play(
            step_circles[0].animate.set_fill(YELLOW, opacity=1).set_stroke(YELLOW, width=2),
            FadeIn(step1_label),
            run_time=max(0.05, 0.90),
        )

        WINDOW_SPAN = 12.0
        N_WINDOWS = 5
        SEG_WIDTH = WINDOW_SPAN / N_WINDOWS
        WINDOW_Y = 1.55
        segment_colors = [TEAL, BLUE, GREEN, ORANGE, PURPLE]

        boundary_xs = [-6 + i * SEG_WIDTH for i in range(N_WINDOWS + 1)]
        dashed_lines = VGroup(
            *[
                DashedLine(
                    np.array([x, 0.55, 0]),
                    np.array([x, 2.40, 0]),
                    dash_length=0.12,
                    stroke_color=WHITE,
                    stroke_width=1.5,
                )
                for x in boundary_xs
            ]
        )
        dashed_lines.set_z_index(5)

        initial_tints = VGroup()
        for i in range(N_WINDOWS):
            rect = Rectangle(
                width=SEG_WIDTH,
                height=1.70,
                fill_color=segment_colors[i],
                fill_opacity=0.14,
                stroke_width=0,
            )
            rect.move_to(np.array([-6 + SEG_WIDTH * (i + 0.5), WINDOW_Y, 0]))
            rect.set_z_index(1)
            initial_tints.add(rect)

        self.play(
            FadeIn(dashed_lines),
            FadeIn(initial_tints),
            run_time=max(0.05, 1.30),
        )

        # ----- wait to 9.10 -----
        self.wait(max(0.05, 0.70))

        # ----- Beat 3: 9.10–12.14 -----
        WINDOW_CENTERS = np.array([-4 + 2 * i for i in range(N_WINDOWS)], dtype=float)
        WINDOW_LENGTH = 4.0
        OVERLAP = 2.0

        window_rects = []
        window_rects_vg = VGroup()
        for i in range(N_WINDOWS):
            rect = Rectangle(
                width=SEG_WIDTH,
                height=1.70,
                fill_color=segment_colors[i],
                fill_opacity=0.16,
                stroke_width=0,
            )
            rect.move_to(np.array([-6 + SEG_WIDTH * (i + 0.5), WINDOW_Y, 0]))
            rect.set_z_index(2)
            window_rects.append(rect)
            window_rects_vg.add(rect)

        self.add(window_rects_vg)
        self.play(
            FadeOut(initial_tints),
            FadeOut(dashed_lines),
            *[
                window_rects[i]
                .animate.stretch_to_fit_width(WINDOW_LENGTH)
                .move_to(np.array([WINDOW_CENTERS[i], WINDOW_Y, 0]))
                for i in range(N_WINDOWS)
            ],
            run_time=max(0.05, 1.24),
        )

        overlap_bands = VGroup()
        for i in range(N_WINDOWS - 1):
            band = Rectangle(
                width=OVERLAP,
                height=1.70,
                fill_color=BLACK,
                fill_opacity=0.55,
                stroke_width=0,
            )
            band.move_to(
                np.array([(WINDOW_CENTERS[i] + WINDOW_CENTERS[i + 1]) / 2, WINDOW_Y, 0])
            )
            band.set_z_index(3)
            overlap_bands.add(band)

        overlap_label = (
            Text("overlapping", font_size=22, color=YELLOW)
            .scale_to_fit_width(3)
            .move_to(np.array([-1.0, 0.20, 0]))
        )
        overlap_arrow = Arrow(
            overlap_label.get_top() + UP * 0.05,
            np.array([-1.0, 0.68, 0]),
            buff=0.05,
            color=YELLOW,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.25,
        )
        overlap_label.set_z_index(6)
        overlap_arrow.set_z_index(6)

        self.play(
            FadeIn(overlap_bands),
            FadeIn(overlap_label),
            FadeIn(overlap_arrow),
            run_time=max(0.05, 0.96),
        )
        self.play(
            Indicate(overlap_bands[1], color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.84),
        )

        # ----- wait to 13.06 -----
        self.wait(max(0.05, 0.92))

        # ----- Beat 4: 13.06–14.66 -----
        step2_label = (
            Text("Step 2: Compute the STFT", font_size=24, color=WHITE)
            .scale_to_fit_width(11)
            .to_edge(UP, buff=0.50)
        )
        self.play(
            FadeOut(step1_label),
            FadeOut(overlap_label),
            FadeOut(overlap_arrow),
            FadeIn(step2_label),
            step_circles[0]
            .animate.set_fill(GREY, opacity=0.35)
            .set_stroke(GREY, width=1.5),
            step_circles[1]
            .animate.set_fill(YELLOW, opacity=1)
            .set_stroke(YELLOW, width=2),
            *[
                r.animate.set_stroke(WHITE, width=2.5, opacity=0.65)
                for r in window_rects
            ],
            run_time=max(0.05, 1.60),
        )

        # ----- wait to 15.38 -----
        self.wait(max(0.05, 0.72))

        # ----- Beat 5: 15.38–20.24 -----
        SPEC_INITIAL_Y = -0.25
        SPEC_FINAL_Y = -0.75

        spectrum_groups = [self.make_spectrum(i) for i in range(N_WINDOWS)]
        spec_initial_positions = []
        for i in range(N_WINDOWS):
            pos = np.array([WINDOW_CENTERS[i] + 0.65, SPEC_INITIAL_Y, 0])
            spectrum_groups[i].move_to(pos)
            spec_initial_positions.append(pos)

        connector_arrows = []
        for i in range(N_WINDOWS):
            start = np.array([WINDOW_CENTERS[i], window_rects[i].get_bottom()[1] - 0.05, 0])
            end = np.array(
                [
                    WINDOW_CENTERS[i] + 0.65,
                    spectrum_groups[i].get_top()[1] + 0.05,
                    0,
                ]
            )
            arrow = Arrow(
                start,
                end,
                buff=0.05,
                color=GREY_B,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.30,
            )
            arrow.set_z_index(4)
            connector_arrows.append(arrow)
        connector_arrows_vg = VGroup(*connector_arrows)

        highlight_rect = Rectangle(
            width=4.2,
            height=1.6,
            fill_color=YELLOW,
            fill_opacity=0.30,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        highlight_rect.move_to(window_rects[0].get_center() + DOWN * 0.25)
        highlight_rect.set_z_index(5)

        per_item = 4.86 / N_WINDOWS
        for i in range(N_WINDOWS):
            current_window = window_rects[i]
            current_spectrum = spectrum_groups[i]
            current_arrow = connector_arrows[i]
            if i == 0:
                self.play(
                    FadeIn(highlight_rect),
                    current_window.animate.set_fill(opacity=0.65).set_stroke(
                        YELLOW, width=3, opacity=0.90
                    ),
                    FadeIn(current_spectrum),
                    FadeIn(current_arrow),
                    run_time=max(0.05, 0.70),
                )
                self.wait(max(0.05, per_item - 0.70))
            else:
                prev_window = window_rects[i - 1]
                self.play(
                    highlight_rect.animate.move_to(
                        current_window.get_center() + DOWN * 0.25
                    ),
                    current_window.animate.set_fill(opacity=0.65).set_stroke(
                        YELLOW, width=3, opacity=0.90
                    ),
                    prev_window.animate.set_fill(opacity=0.16).set_stroke(
                        WHITE, width=2.5, opacity=0.65
                    ),
                    FadeIn(current_spectrum),
                    FadeIn(current_arrow),
                    run_time=max(0.05, 0.75),
                )
                self.wait(max(0.05, per_item - 0.75))

        # ----- wait to 21.26 -----
        self.wait(max(0.05, 1.02))

        # ----- Beat 6: 21.26–23.74 -----
        step3_label = (
            Text("Step 3: Arrange the spectra in time order", font_size=24, color=WHITE)
            .scale_to_fit_width(11)
            .to_edge(UP, buff=0.50)
        )
        final_spec_positions = [
            np.array([WINDOW_CENTERS[i], SPEC_FINAL_Y, 0]) for i in range(N_WINDOWS)
        ]
        self.play(
            FadeOut(step2_label),
            FadeIn(step3_label),
            step_circles[2]
            .animate.set_fill(YELLOW, opacity=1)
            .set_stroke(YELLOW, width=2),
            step_circles[0]
            .animate.set_fill(GREY, opacity=0.30)
            .set_stroke(GREY, width=1.5),
            step_circles[1]
            .animate.set_fill(GREY, opacity=0.30)
            .set_stroke(GREY, width=1.5),
            run_time=max(0.05, 1.00),
        )
        self.play(
            *[
                spectrum_groups[i].animate.move_to(final_spec_positions[i])
                for i in range(N_WINDOWS)
            ],
            FadeOut(connector_arrows_vg),
            FadeOut(window_rects_vg),
            FadeOut(overlap_bands),
            FadeOut(highlight_rect),
            FadeOut(waveform),
            run_time=max(0.05, 1.48),
        )

        # ----- wait to 24.56 -----
        self.wait(max(0.05, 0.82))

        # ----- Beat 7: 24.56–28.98 -----
        spectrum_rects = []
        spectrum_rects_vg = VGroup()
        for i in range(N_WINDOWS):
            rect = Rectangle(
                width=2.0,
                height=1.8,
                stroke_color=WHITE,
                stroke_width=2.0,
                stroke_opacity=0.80,
                fill_color=BLACK,
                fill_opacity=0.05,
            )
            rect.move_to(final_spec_positions[i])
            rect.set_z_index(1)
            spectrum_rects.append(rect)
            spectrum_rects_vg.add(rect)
        for g in spectrum_groups:
            g.set_z_index(3)

        self.play(
            *[FadeIn(r) for r in spectrum_rects],
            run_time=max(0.05, 2.00),
        )

        row_left = spectrum_rects_vg.get_left()[0]
        row_right = spectrum_rects_vg.get_right()[0]
        row_bottom = spectrum_rects_vg.get_bottom()[1]
        row_top = spectrum_rects_vg.get_top()[1]

        time_axis = Line(
            np.array([row_left - 0.70, row_bottom - 0.35, 0]),
            np.array([row_right + 0.70, row_bottom - 0.35, 0]),
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.80,
        )
        time_label = Text("Time", font_size=28, color=WHITE).next_to(
            time_axis, DOWN, buff=0.20
        )
        freq_axis = Line(
            np.array([row_left - 1.20, row_bottom - 0.35, 0]),
            np.array([row_left - 1.20, row_top + 0.30, 0]),
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.80,
        )
        freq_label = (
            VGroup(
                Text("Frequency", font_size=20, color=WHITE),
                Text("(Hz)", font_size=20, color=GOLD),
            )
            .arrange(RIGHT, buff=0.10)
            .rotate(PI / 2)
            .next_to(freq_axis, LEFT, buff=0.20)
        )
        time_axis.set_z_index(5)
        freq_axis.set_z_index(5)
        time_label.set_z_index(5)
        freq_label.set_z_index(5)

        self.play(
            FadeIn(time_axis),
            FadeIn(time_label),
            FadeIn(freq_axis),
            FadeIn(freq_label),
            run_time=max(0.05, 2.42),
        )

        # ----- wait to 29.73 -----
        self.wait(max(0.05, 0.75))

        # ----- Beat 8: 29.73–32.36 -----
        step4_label = (
            Text("Step 4: Display the signal as an image", font_size=24, color=WHITE)
            .scale_to_fit_width(11)
            .to_edge(UP, buff=0.50)
        )
        self.play(
            FadeOut(step3_label),
            FadeIn(step4_label),
            step_circles[3]
            .animate.set_fill(YELLOW, opacity=1)
            .set_stroke(YELLOW, width=2),
            step_circles[2]
            .animate.set_fill(GREY, opacity=0.30)
            .set_stroke(GREY, width=1.5),
            run_time=max(0.05, 0.90),
        )

        color_columns = [
            self.make_color_column(i, width=2.0, height=1.8) for i in range(N_WINDOWS)
        ]
        color_columns_vg = VGroup()
        for i, col in enumerate(color_columns):
            col.move_to(spectrum_rects[i].get_center())
            col.set_z_index(4)
            color_columns_vg.add(col)
        self.play(
            FadeOut(VGroup(*spectrum_groups)),
            FadeIn(color_columns_vg),
            run_time=max(0.05, 1.73),
        )

        # ----- wait to 33.34 -----
        self.wait(max(0.05, 0.98))

        # ----- Beat 9: 33.34–36.32 -----
        gradient_colors = [
            BLUE,
            BLUE,
            TEAL,
            TEAL,
            GREEN,
            GREEN,
            YELLOW,
            YELLOW,
            GOLD,
            GOLD,
            ORANGE,
            RED,
        ]
        colorbar = VGroup(
            *[
                Rectangle(
                    width=0.25,
                    height=1.8 / len(gradient_colors),
                    fill_color=c,
                    fill_opacity=1,
                    stroke_width=0,
                )
                for c in gradient_colors
            ]
        )
        colorbar.arrange(DOWN, buff=0)
        colorbar.next_to(spectrum_rects_vg, RIGHT, buff=0.45)
        colorbar.set_z_index(6)

        colour_intensity_label = (
            Text("Colour intensity", font_size=20, color=WHITE)
            .next_to(colorbar, RIGHT, buff=0.22)
            .set_z_index(6)
        )
        self.play(
            FadeIn(colorbar),
            FadeIn(colour_intensity_label),
            run_time=max(0.05, 0.90),
        )
        self.play(
            color_columns_vg.animate.set_opacity(0.72),
            run_time=max(0.05, 0.70),
        )
        self.play(
            color_columns_vg.animate.set_opacity(0.98),
            run_time=max(0.05, 0.70),
        )
        self.play(
            color_columns_vg.animate.set_opacity(0.82),
            run_time=max(0.05, 0.68),
        )

        # ----- wait to 36.84 -----
        self.wait(max(0.05, 0.52))

        # ----- Beat 10: 36.84–43.16 -----
        smooth_spec = self.build_smooth_spectrogram(width=10.0, height=1.8)
        smooth_spec.move_to(spectrum_rects_vg.get_center())
        signal_strength_label = (
            Text("Signal strength", font_size=20, color=YELLOW)
            .next_to(colour_intensity_label, DOWN, buff=0.15)
            .set_z_index(6)
        )

        self.play(
            FadeOut(color_columns_vg),
            FadeOut(spectrum_rects_vg),
            FadeIn(smooth_spec),
            FadeIn(signal_strength_label),
            run_time=max(0.05, 2.32),
        )
        self.play(
            Indicate(time_label, color=YELLOW, scale_factor=1.25),
            run_time=max(0.05, 0.80),
        )
        self.play(
            Indicate(freq_label, color=YELLOW, scale_factor=1.25),
            run_time=max(0.05, 0.80),
        )
        self.play(
            Indicate(signal_strength_label, color=YELLOW, scale_factor=1.25),
            run_time=max(0.05, 0.80),
        )
        self.play(
            FadeOut(step4_label),
            FadeOut(step_circle_group),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 0.80))

        # ----- Beat 11: 43.16–43.80 -----
        self.wait(max(0.05, 0.64))