ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def wave_func(x):
            return 0.8 * np.sin(2.5 * x) * np.cos(0.35 * x) + 0.3 * np.sin(5.0 * x) + 0.15 * np.sin(1.2 * x)

        wave_min_x = -6.5
        wave_max_x = 6.5
        n_segments = 10
        seg_w = (wave_max_x - wave_min_x) / n_segments
        lefts = [wave_min_x + i * seg_w for i in range(n_segments)]
        centers = [left + seg_w / 2 for left in lefts]

        wave_y_center = 2.4
        small_y = 0.1
        small_width = 1.05
        small_height = 1.15

        spectrogram_center_y = -0.7
        spectrogram_width = 12.2
        spectrogram_height = 2.2
        col_width = 0.92
        col_height = 1.6
        n_freq_bins = 8

        height_sets = [
            [0.45, 0.8, 0.3, 0.65, 0.2, 0.5],
            [0.2, 0.6, 0.9, 0.4, 0.7, 0.3],
            [0.75, 0.3, 0.45, 0.95, 0.2, 0.55],
            [0.3, 0.9, 0.5, 0.2, 0.65, 0.85],
            [0.55, 0.25, 0.8, 0.35, 0.6, 0.95],
            [0.9, 0.5, 0.2, 0.75, 0.3, 0.6],
            [0.25, 0.45, 0.7, 0.9, 0.55, 0.35],
            [0.6, 0.3, 0.85, 0.4, 0.9, 0.2],
            [0.4, 0.7, 0.2, 0.55, 0.3, 0.8],
            [0.85, 0.2, 0.65, 0.3, 0.75, 0.5],
        ]

        # Full waveform, same shape as previous scene, positioned in upper portion
        wave = FunctionGraph(wave_func, x_range=[wave_min_x, wave_max_x])
        wave.set_stroke(WHITE, width=4)
        wave.shift(UP * wave_y_center)
        self.add(wave)

        def make_small_axes(center_x, center_y):
            half_w = small_width / 2
            half_h = small_height / 2
            bottom = Line(
                np.array([center_x - half_w, center_y - half_h, 0]),
                np.array([center_x + half_w, center_y - half_h, 0]),
                color=GREY_B,
                stroke_width=2,
            )
            left = Line(
                np.array([center_x - half_w, center_y - half_h, 0]),
                np.array([center_x - half_w, center_y + half_h, 0]),
                color=GREY_B,
                stroke_width=2,
            )
            return VGroup(bottom, left)

        def make_small_curve(center_x, center_y, heights):
            n_points = 90
            xs = np.linspace(-small_width / 2, small_width / 2, n_points)
            peak_xs = np.linspace(-0.42 * small_width, 0.42 * small_width, len(heights))
            raw = np.zeros_like(xs)
            for px, h in zip(peak_xs, heights):
                raw += h * np.exp(-((xs - px) / (0.08 * small_width)) ** 2)
            raw = raw / np.max(raw)

            baseline_y = center_y - small_height / 2 + 0.12 * small_height
            top_y = center_y + small_height / 2 - 0.12 * small_height
            ys = baseline_y + raw * (top_y - baseline_y)

            curve = VMobject()
            curve.set_points_as_corners(
                [np.array([center_x + xs[i], ys[i], 0]) for i in range(n_points)]
            )
            curve.set_stroke(color=WHITE, width=3)
            curve.set_fill(opacity=0)
            return curve

        spectrum_plots = VGroup()
        curves_group = VGroup()
        axes_group = VGroup()
        for i, heights in enumerate(height_sets):
            cx = centers[i]
            ax = make_small_axes(cx, small_y)
            curve = make_small_curve(cx, small_y, heights)
            plot = VGroup(ax, curve)
            spectrum_plots.add(plot)
            curves_group.add(curve)
            axes_group.add(ax)

        # Beat 1: first spectrum fades in under first window position
        self.play(FadeIn(spectrum_plots[0]), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.5))
        self.play(Indicate(curves_group[0], scale_factor=1.08, color=YELLOW), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.47))

        # Beat 2: second spectrum fades in under second window position
        self.wait(max(0.05, 0.9))
        self.play(FadeIn(spectrum_plots[1]), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.46))

        # Beat 3: remaining spectra appear left to right
        self.wait(max(0.05, 0.68))
        per_item = 0.35
        for idx in range(2, n_segments):
            self.play(FadeIn(spectrum_plots[idx]), run_time=max(0.05, 0.22))
            self.wait(max(0.05, per_item - 0.22))

        # Subtle highlight sweep left to right across the spectrum row
        sweep_rect = Rectangle(
            width=1.0,
            height=small_height,
            fill_color=YELLOW,
            fill_opacity=0.15,
            stroke_width=0,
        )
        sweep_rect.move_to(np.array([centers[0], small_y, 0]))
        self.add(sweep_rect)
        self.play(
            sweep_rect.animate.move_to(np.array([centers[-1], small_y, 0])),
            run_time=max(0.05, 0.32),
        )
        self.play(FadeOut(sweep_rect), run_time=max(0.05, 0.12))
        self.wait(max(0.05, 0.18))

        # Main time-frequency plotting region
        main_rect = Rectangle(
            width=spectrogram_width,
            height=spectrogram_height,
            color=GREY_B,
            stroke_width=3,
        )
        main_rect.move_to(np.array([0, spectrogram_center_y, 0]))

        freq_axis_line = Line(
            main_rect.get_corner(DL),
            main_rect.get_corner(UL),
            color=GREY_B,
            stroke_width=3,
        )
        time_axis_line = Line(
            main_rect.get_corner(DL),
            main_rect.get_corner(DR),
            color=GREY_B,
            stroke_width=3,
        )
        main_frame_group = VGroup(main_rect, freq_axis_line, time_axis_line)

        def column_opacities(heights):
            peak_positions = np.linspace(0.15, 0.85, len(heights))
            fracs = np.linspace(0.0, 1.0, n_freq_bins)
            raw = np.zeros_like(fracs)
            for px, h in zip(peak_positions, heights):
                raw += h * np.exp(-((fracs - px) / 0.12) ** 2)
            raw = raw / np.max(raw)
            return 0.15 + 0.85 * raw

        def make_lattice_column(center_x, heights):
            vals = column_opacities(heights)
            bin_h = col_height / n_freq_bins
            bottom_y = spectrogram_center_y - col_height / 2
            cells = VGroup()
            for j in range(n_freq_bins):
                cell = Rectangle(
                    width=col_width,
                    height=bin_h * 0.92,
                    fill_color=TEAL,
                    fill_opacity=vals[j],
                    stroke_width=0,
                )
                cell.move_to(np.array([center_x, bottom_y + (j + 0.5) * bin_h, 0]))
                cells.add(cell)
            return cells

        lattice_columns = VGroup(
            make_lattice_column(centers[i], height_sets[i]) for i in range(n_segments)
        )

        # Beat 4: row compresses vertically and merges into the compact representation
        self.wait(max(0.05, 0.98))
        merge_center = np.array([0, spectrogram_center_y, 0])
        self.play(
            spectrum_plots.animate.stretch(0.25, dim=1).move_to(merge_center),
            run_time=max(0.05, 0.9),
        )
        self.play(
            ReplacementTransform(curves_group, lattice_columns),
            FadeOut(axes_group),
            FadeIn(main_frame_group),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.56))

        # Beat 5: labels, frequency axis brightens, vertical structure emphasized
        time_label = Text("time", font_size=34, color=GREY_B)
        time_label.next_to(main_rect, DOWN, buff=0.2)

        freq_label = Text("frequency", font_size=34, color=GREY_B).rotate(PI / 2)
        freq_label.next_to(main_rect, LEFT, buff=0.2)

        self.play(Write(time_label), Write(freq_label), run_time=max(0.05, 0.9))
        self.play(
            freq_label.animate.set_color(YELLOW).scale(1.2),
            freq_axis_line.animate.set_stroke(color=YELLOW, width=5),
            run_time=max(0.05, 0.5),
        )
        self.play(
            lattice_columns.animate.set_stroke(color=WHITE, width=1),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.54))

        # Beat 6: time axis brightens, waveform dims, subtle left-to-right shading
        surge_overlays = VGroup()
        for i in range(n_segments):
            overlay = Rectangle(
                width=col_width * 0.95,
                height=col_height,
                fill_color=YELLOW,
                fill_opacity=0,
                stroke_width=0,
            )
            overlay.move_to(np.array([centers[i], spectrogram_center_y, 0]))
            surge_overlays.add(overlay)

        self.add(surge_overlays)
        self.play(
            time_label.animate.set_color(YELLOW).scale(1.2),
            time_axis_line.animate.set_stroke(color=YELLOW, width=5),
            wave.animate.set_color(GREY).set_stroke(width=2.5),
            run_time=max(0.05, 0.6),
        )
        self.play(
            LaggedStart(
                *[overlay.animate.set_fill(opacity=0.3) for overlay in surge_overlays],
                lag_ratio=0.15,
            ),
            run_time=max(0.05, 1.3),
        )
        self.play(
            LaggedStart(
                *[overlay.animate.set_fill(opacity=0.0) for overlay in surge_overlays],
                lag_ratio=0.15,
            ),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.41))