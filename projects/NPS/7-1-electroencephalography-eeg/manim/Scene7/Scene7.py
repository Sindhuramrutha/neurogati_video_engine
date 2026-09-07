ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Raw EEG waveform (continuity from Scene 6)
        # ------------------------------------------------------------
        wave_xs = np.linspace(-6.0, 6.0, 520)
        wave_y_center = 2.45

        def alpha_points():
            u = (wave_xs + 6.0) / 12.0
            ys = 0.28 * np.sin(2 * np.pi * 10.0 * u) + 0.05 * np.sin(
                2 * np.pi * 18.0 * u + 1.2
            )
            return ys

        def raw_mixed_points(shift):
            u = (wave_xs + 6.0) / 12.0
            y = (
                0.16 * np.sin(2 * np.pi * 1.5 * u + shift * 0.5)
                + 0.13 * np.sin(2 * np.pi * 5.0 * u + 1.3 * shift)
                + 0.11 * np.sin(2 * np.pi * 10.5 * u + 2.3 * shift)
                + 0.08 * np.sin(2 * np.pi * 21.0 * u + 3.1 * shift)
                + 0.04 * np.sin(2 * np.pi * 40.0 * u + 4.2 * shift)
            )
            amp = 0.70 + 0.30 * np.sin(2 * np.pi * 0.35 * u + 5.0 * shift)
            return 0.55 * amp * y

        mix_tracker = ValueTracker(0.0)
        shift_tracker = ValueTracker(0.0)

        def update_raw_wave(wave):
            mix = mix_tracker.get_value()
            shift = shift_tracker.get_value()
            y_alpha = alpha_points()
            y_raw = raw_mixed_points(shift)
            ys = (1.0 - mix) * y_alpha + mix * y_raw
            pts = [
                np.array([x, wave_y_center + y, 0.0])
                for x, y in zip(wave_xs, ys)
            ]
            wave.set_points_as_corners(pts)

        raw_wave = VMobject()
        raw_wave.set_stroke(WHITE, width=2.5)
        raw_wave.set_fill(opacity=0)
        raw_wave.add_updater(update_raw_wave)
        update_raw_wave(raw_wave)

        # ------------------------------------------------------------
        # Frequency bars from previous scene (alpha lit, others dimmed)
        # ------------------------------------------------------------
        bands = [
            {"name": "delta", "color": BLUE, "start": 0.5, "end": 4},
            {"name": "theta", "color": TEAL, "start": 4, "end": 8},
            {"name": "alpha", "color": GREEN, "start": 8, "end": 13},
            {"name": "beta", "color": ORANGE, "start": 13, "end": 30},
            {"name": "gamma", "color": RED, "start": 30, "end": 50},
        ]

        AXIS_LEFT_X = -5.2
        AXIS_RIGHT_X = 5.2

        def fx(f):
            return AXIS_LEFT_X + (f / 50.0) * (AXIS_RIGHT_X - AXIS_LEFT_X)

        bar_y_positions = [0.10, 0.45, 0.80, 1.15, 1.50]
        band_bars = VGroup()
        band_rects = []
        for i, band in enumerate(bands):
            x_left = fx(band["start"])
            x_right = fx(band["end"])
            width = x_right - x_left
            bar = Rectangle(
                width=width,
                height=0.30,
                fill_color=band["color"],
                fill_opacity=0.9 if i == 2 else 0.2,
                stroke_width=0,
            )
            bar.move_to(np.array([(x_left + x_right) / 2.0, bar_y_positions[i], 0.0]))
            band_bars.add(bar)
            band_rects.append(bar)

        # ------------------------------------------------------------
        # Four empty panels
        # ------------------------------------------------------------
        panel_width = 2.6
        panel_height = 1.35
        panel_xs = [-4.575, -1.525, 1.525, 4.575]
        panel_y = -1.70
        panel_rects = []
        for x in panel_xs:
            panel = RoundedRectangle(
                corner_radius=0.10,
                width=panel_width,
                height=panel_height,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_color="#1A1D26",
                fill_opacity=0.9,
            )
            panel.move_to(np.array([x, panel_y, 0.0]))
            panel_rects.append(panel)
        panel_group = VGroup(*panel_rects)

        # ------------------------------------------------------------
        # Faint placeholder icons (all built from primitives)
        # ------------------------------------------------------------
        def make_filter_placeholder():
            icon = VGroup()
            block = Rectangle(
                width=0.75,
                height=0.55,
                fill_color=WHITE,
                fill_opacity=0.25,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            line1 = Line(
                block.get_left() + RIGHT * 0.10,
                block.get_right() + LEFT * 0.10,
                color=WHITE,
                stroke_width=1.5,
            ).move_to(block.get_center() + UP * 0.14)
            line2 = Line(
                block.get_left() + RIGHT * 0.10,
                block.get_right() + LEFT * 0.10,
                color=WHITE,
                stroke_width=1.5,
            ).move_to(block.get_center() + DOWN * 0.14)
            icon.add(block, line1, line2)
            icon.scale_to_fit_height(0.55)
            return icon

        def make_bar_chart_placeholder():
            bars = VGroup()
            heights = [0.25, 0.45, 0.35, 0.55, 0.30]
            widths = [0.12] * 5
            for i, (h, w) in enumerate(zip(heights, widths)):
                bar = Rectangle(
                    width=w,
                    height=h,
                    fill_color=WHITE,
                    fill_opacity=0.45,
                    stroke_width=0,
                )
                bar.shift(RIGHT * (i - 2) * 0.18)
                bar.align_to(bars, DOWN) if bars else bar.move_to(ORIGIN)
                bars.add(bar)
            bars.scale_to_fit_height(0.55)
            return bars

        def make_heatmap_placeholder():
            grid = VGroup()
            for r in range(3):
                for c in range(3):
                    cell = Rectangle(
                        width=0.15,
                        height=0.15,
                        fill_color=WHITE,
                        fill_opacity=0.35,
                        stroke_color=WHITE,
                        stroke_width=0.8,
                    )
                    cell.move_to(np.array([(c - 1) * 0.19, (r - 1) * 0.19, 0.0]))
                    grid.add(cell)
            grid.scale_to_fit_height(0.55)
            return grid

        def make_wavelet_placeholder():
            xs = np.linspace(-0.45, 0.45, 80)
            ys = 0.18 * np.sin(2 * np.pi * 2.2 * xs / 0.9) * np.exp(
                -((xs - 0.05) ** 2) / 0.03
            ) + 0.12 * np.sin(2 * np.pi * 3.0 * xs / 0.9) * np.exp(
                -((xs + 0.15) ** 2) / 0.02
            )
            wave = VMobject()
            wave.set_points_as_corners(
                [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
            )
            wave.set_stroke(WHITE, width=1.8)
            wave.set_fill(opacity=0)
            wave.scale_to_fit_height(0.55)
            return wave

        placeholder_icons = [
            make_filter_placeholder(),
            make_bar_chart_placeholder(),
            make_heatmap_placeholder(),
            make_wavelet_placeholder(),
        ]
        for icon, panel in zip(placeholder_icons, panel_rects):
            icon.move_to(panel.get_center())
            icon.set_opacity(0.35)

        # Containers for labels and detailed panel contents
        panel_labels = []
        panel_contents = [None, None, None, None]

        # ------------------------------------------------------------
        # Beat 1: 0.00-1.60 -- dim alpha to neutral, raw becomes mixed
        # ------------------------------------------------------------
        self.add(raw_wave, band_bars)

        self.wait(max(0.05, 0.70))
        self.play(
            mix_tracker.animate.set_value(1.0),
            *[bar.animate.set_fill(opacity=0.25) for bar in band_rects],
            run_time=max(0.05, 0.90),
        )

        # ------------------------------------------------------------
        # Beat 2: 1.60-4.36 -- raw, noisy, question mark appears/fades
        # ------------------------------------------------------------
        self.play(shift_tracker.animate.set_value(0.55), run_time=max(0.05, 1.20))
        question_mark = Text("?", font_size=80, color=YELLOW, weight="BOLD")
        question_mark.to_corner(UR, buff=0.4)
        self.play(FadeIn(question_mark), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.40))
        self.play(FadeOut(question_mark), run_time=max(0.05, 0.35))
        self.play(shift_tracker.animate.set_value(0.90), run_time=max(0.05, 0.46))

        raw_wave.clear_updaters()

        # ------------------------------------------------------------
        # Beat 3: 4.36-5.42 -- hold, no annotations
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.06))

        # ------------------------------------------------------------
        # Beat 4: 5.42-10.16 -- four empty panels + faint icons
        # ------------------------------------------------------------
        self.play(FadeIn(panel_group), run_time=max(0.05, 0.90))
        per_icon_dur = 0.96
        for icon in placeholder_icons:
            self.play(GrowFromCenter(icon), run_time=max(0.05, 0.55))
            self.wait(max(0.05, per_icon_dur - 0.55))

        # Gap 10.16-11.10
        self.wait(max(0.05, 0.94))

        # ------------------------------------------------------------
        # Beat 5: 11.10-12.72 -- arrow from raw waveform to panel 1
        # ------------------------------------------------------------
        arrow_start = np.array([panel_rects[0].get_center()[0], wave_y_center - 0.40, 0.0])
        arrow_end = panel_rects[0].get_top() + UP * 0.08
        arrow_raw_to_panel1 = Arrow(
            start=arrow_start,
            end=arrow_end,
            color=GREY_B,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.18,
        )
        self.play(Create(arrow_raw_to_panel1), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.62))

        # ------------------------------------------------------------
        # Beat 6: 12.72-16.86 -- panel 1: band-pass filter
        # ------------------------------------------------------------
        self.play(FadeOut(placeholder_icons[0]), run_time=max(0.05, 0.20))

        panel = panel_rects[0]
        x_left = panel.get_left()[0] + 0.35
        x_right = panel.get_right()[0] - 0.35
        mid_y = panel.get_center()[1]

        block = RoundedRectangle(
            corner_radius=0.08,
            width=0.95,
            height=0.85,
            fill_color=TEAL,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        block.move_to(panel.get_center())
        block_text = Text("Band-pass\nfilter", font_size=9, color=BLACK, line_spacing=0.5)
        block_text.scale_to_fit_width(0.70)
        block_text.move_to(block.get_center())

        xs_in = np.linspace(x_left, block.get_left()[0] - 0.10, 70)
        ys_in = 0.10 * np.sin(2 * np.pi * 7.0 * (xs_in - xs_in[0]) / 0.6) + 0.05 * np.sin(
            2 * np.pi * 15.0 * (xs_in - xs_in[0]) / 0.6
        )
        raw_in = VMobject()
        raw_in.set_points_as_corners(
            [np.array([x, mid_y + y, 0.0]) for x, y in zip(xs_in, ys_in)]
        )
        raw_in.set_stroke(GREY_B, width=2)
        raw_in.set_fill(opacity=0)

        xs_out = np.linspace(block.get_right()[0] + 0.10, x_right, 70)
        ys_out = 0.12 * np.sin(2 * np.pi * 4.0 * (xs_out - xs_out[0]) / 0.6)
        smooth_out = VMobject()
        smooth_out.set_points_as_corners(
            [np.array([x, mid_y + y, 0.0]) for x, y in zip(xs_out, ys_out)]
        )
        smooth_out.set_stroke(GREEN, width=2.5)
        smooth_out.set_fill(opacity=0)

        arrow_in = Arrow(
            raw_in.get_right(),
            block.get_left() + LEFT * 0.02,
            color=WHITE,
            stroke_width=2,
            buff=0.04,
            max_tip_length_to_length_ratio=0.3,
        )
        arrow_out = Arrow(
            block.get_right() + RIGHT * 0.02,
            smooth_out.get_left(),
            color=WHITE,
            stroke_width=2,
            buff=0.04,
            max_tip_length_to_length_ratio=0.3,
        )

        # Subtle shaded frequency band overlay behind the filter block
        shade_band = Rectangle(
            width=0.95,
            height=0.50,
            fill_color=GREEN,
            fill_opacity=0.25,
            stroke_width=0,
        )
        shade_band.move_to(block.get_center() + UP * 0.05)

        panel1_content = VGroup(
            shade_band, block, block_text, raw_in, smooth_out, arrow_in, arrow_out
        )
        panel1_content.scale_to_fit_width(panel_width - 0.35)
        panel1_content.scale_to_fit_height(panel_height - 0.35)
        panel1_content.move_to(panel.get_center())
        panel_contents[0] = panel1_content

        self.play(GrowFromCenter(panel1_content), run_time=max(0.05, 0.90))

        label1 = Text("Band-pass filtering", font_size=14, color=WHITE)
        label1.next_to(panel_rects[0], DOWN, buff=0.14)
        self.play(
            Write(label1),
            arrow_raw_to_panel1.animate.set_color(YELLOW).set_stroke(width=4),
            run_time=max(0.05, 0.80),
        )
        self.play(Indicate(panel1_content, scale_factor=1.03), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 1.54))
        panel_labels.append(label1)

        # Gap 16.86-17.90
        self.wait(max(0.05, 1.04))

        # ------------------------------------------------------------
        # Beat 7: 17.90-20.72 -- panel 2: spectral analysis
        # ------------------------------------------------------------
        self.play(
            panel1_content.animate.set_opacity(0.7),
            panel_rects[0].animate.set_fill(opacity=0.8),
            run_time=max(0.05, 0.30),
        )
        self.play(FadeOut(placeholder_icons[1]), run_time=max(0.05, 0.20))

        panel = panel_rects[1]
        x0 = panel.get_left()[0] + 0.22
        x1 = panel.get_right()[0] - 0.22
        y0 = panel.get_bottom()[1] + 0.22
        y1 = panel.get_top()[1] - 0.30

        x_axis = Line(np.array([x0, y0, 0.0]), np.array([x1, y0, 0.0]), color=GREY_B, stroke_width=2)
        y_axis = Line(np.array([x0, y0, 0.0]), np.array([x0, y1, 0.0]), color=GREY_B, stroke_width=2)

        ticks = VGroup()
        tick_labels = VGroup()
        for val in [4, 8, 13, 30]:
            xt = x0 + (val / 50.0) * (x1 - x0)
            ticks.add(
                Line(
                    np.array([xt, y0 - 0.06, 0.0]),
                    np.array([xt, y0 + 0.06, 0.0]),
                    color=GREY_B,
                    stroke_width=1.5,
                )
            )
            tick_labels.add(Text(str(val), font_size=7, color=GREY_B).move_to(np.array([xt, y0 - 0.16, 0.0])))

        power_label = Text("Power", font_size=8, color=GREY_B).rotate(PI / 2)
        power_label.next_to(y_axis, LEFT, buff=0.10)
        freq_label = Text("Frequency (Hz)", font_size=8, color=GREY_B)
        freq_label.move_to(np.array([(x0 + x1) / 2.0, y0 - 0.28, 0.0]))

        alpha_band_left = x0 + (8.0 / 50.0) * (x1 - x0)
        alpha_band_right = x0 + (13.0 / 50.0) * (x1 - x0)
        alpha_band = Rectangle(
            width=alpha_band_right - alpha_band_left,
            height=y1 - y0,
            fill_color=GREEN,
            fill_opacity=0.12,
            stroke_width=0,
        )
        alpha_band.move_to(np.array([(alpha_band_left + alpha_band_right) / 2.0, (y0 + y1) / 2.0, 0.0]))

        freqs = np.linspace(0.0, 50.0, 120)
        power = (
            np.exp(-((freqs - 10.5) / 2.5) ** 2)
            + 0.25 * np.exp(-((freqs - 21.0) / 4.0) ** 2)
            + 0.18 * np.exp(-((freqs - 6.0) / 1.5) ** 2)
        )
        power_max = np.max(power)
        curve_points = [
            np.array([
                x0 + (f / 50.0) * (x1 - x0),
                y0 + (p / power_max) * (y1 - y0) * 0.75,
                0.0,
            ])
            for f, p in zip(freqs, power)
        ]
        spectrum_curve = VMobject()
        spectrum_curve.set_points_as_corners(curve_points)
        spectrum_curve.set_stroke(GREEN, width=2.5)
        spectrum_curve.set_fill(opacity=0)

        area_points = [np.array([x0, y0, 0.0])] + curve_points + [
            np.array([x1, y0, 0.0]),
            np.array([x0, y0, 0.0]),
        ]
        spectrum_area = VMobject()
        spectrum_area.set_points_as_corners(area_points)
        spectrum_area.set_fill(GREEN, opacity=0.25)
        spectrum_area.set_stroke(width=0)

        alpha_peak_label = Text("Alpha", font_size=8, color=GREEN)
        alpha_peak_x = x0 + (10.5 / 50.0) * (x1 - x0)
        alpha_peak_y = y0 + (1.0 / power_max) * (y1 - y0) * 0.75
        alpha_peak_label.move_to(np.array([alpha_peak_x + 0.28, alpha_peak_y + 0.12, 0.0]))

        panel2_content = VGroup(
            spectrum_area,
            alpha_band,
            x_axis,
            y_axis,
            ticks,
            tick_labels,
            spectrum_curve,
            power_label,
            freq_label,
            alpha_peak_label,
        )
        panel2_content.scale_to_fit_width(panel_width - 0.25)
        panel2_content.scale_to_fit_height(panel_height - 0.25)
        panel2_content.move_to(panel.get_center())
        panel_contents[1] = panel2_content

        self.play(GrowFromCenter(panel2_content), run_time=max(0.05, 0.70))

        label2 = Text("Spectral analysis", font_size=14, color=WHITE)
        label2.next_to(panel_rects[1], DOWN, buff=0.14)
        self.play(Write(label2), run_time=max(0.05, 0.50))

        arrow_1_2 = Arrow(
            start=panel_rects[0].get_right() + RIGHT * 0.15,
            end=panel_rects[1].get_left() + LEFT * 0.15,
            color=GREY_B,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.18,
        )
        self.play(Create(arrow_1_2), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.62))
        panel_labels.append(label2)

        # Gap 20.72-21.46
        self.wait(max(0.05, 0.74))

        # ------------------------------------------------------------
        # Beat 8: 21.46-24.62 -- panel 3: spectrogram
        # ------------------------------------------------------------
        self.play(
            panel2_content.animate.set_opacity(0.7),
            panel_rects[1].animate.set_fill(opacity=0.8),
            run_time=max(0.05, 0.30),
        )
        self.play(FadeOut(placeholder_icons[2]), run_time=max(0.05, 0.20))

        panel = panel_rects[2]
        left = panel.get_left()[0] + 0.20
        right = panel.get_right()[0] - 0.20
        bottom = panel.get_bottom()[1] + 0.24
        top = panel.get_top()[1] - 0.28

        def freq_to_y(f):
            return bottom + (f / 50.0) * (top - bottom)

        cols = 12
        rows = 5
        row_names = ["delta", "theta", "alpha", "beta", "gamma"]
        row_bounds = [0.5, 4.0, 8.0, 13.0, 30.0, 50.0]

        spectro_cells = VGroup()
        spectro_rows = {}
        cell_w = (right - left) / cols
        for r in range(rows):
            row_cells = VGroup()
            rb = freq_to_y(row_bounds[r])
            rt = freq_to_y(row_bounds[r + 1])
            row_h = rt - rb
            cy = (rb + rt) / 2.0
            for c in range(cols):
                cell = Rectangle(
                    width=cell_w * 0.95,
                    height=row_h * 0.95,
                    fill_color=BLACK,
                    fill_opacity=0.65,
                    stroke_color=GREY_B,
                    stroke_width=0.5,
                )
                cell.move_to(np.array([left + (c + 0.5) * cell_w, cy, 0.0]))
                row_cells.add(cell)
                spectro_cells.add(cell)
            spectro_rows[row_names[r]] = row_cells

        # Initial alpha band bright
        spectro_rows["alpha"].set_fill(YELLOW, opacity=0.85)

        spec_ticks = VGroup()
        spec_tick_labels = VGroup()
        for val in [4, 8, 13, 30]:
            yt = freq_to_y(val)
            spec_ticks.add(
                Line(
                    np.array([left - 0.07, yt, 0.0]),
                    np.array([left + 0.02, yt, 0.0]),
                    color=GREY_B,
                    stroke_width=1.2,
                )
            )
            spec_tick_labels.add(Text(str(val), font_size=7, color=GREY_B).move_to(np.array([left - 0.25, yt, 0.0])))

        time_label = Text("Time", font_size=8, color=GREY_B)
        time_label.move_to(np.array([(left + right) / 2.0, bottom - 0.18, 0.0]))
        freq_label_spec = Text("Freq (Hz)", font_size=8, color=GREY_B).rotate(PI / 2)
        freq_label_spec.next_to(spec_ticks, LEFT, buff=0.08)

        panel3_content = VGroup(
            spectro_cells, spec_ticks, spec_tick_labels, time_label, freq_label_spec
        )
        panel3_content.scale_to_fit_width(panel_width - 0.20)
        panel3_content.scale_to_fit_height(panel_height - 0.20)
        panel3_content.move_to(panel.get_center())
        panel_contents[2] = panel3_content

        self.play(GrowFromCenter(panel3_content), run_time=max(0.05, 0.60))

        label3 = Text("Spectrogram", font_size=14, color=WHITE)
        label3.next_to(panel_rects[2], DOWN, buff=0.14)
        self.play(Write(label3), run_time=max(0.05, 0.40))

        arrow_2_3 = Arrow(
            start=panel_rects[1].get_right() + RIGHT * 0.15,
            end=panel_rects[2].get_left() + LEFT * 0.15,
            color=GREY_B,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.18,
        )
        self.play(Create(arrow_2_3), run_time=max(0.05, 0.40))

        # Spectrogram band shifts: alpha -> beta -> theta
        def set_spectro_rows(bright_name, bright_color):
            anims = []
            for name, row in spectro_rows.items():
                if name == bright_name:
                    anims.append(row.animate.set_fill(bright_color, opacity=0.85))
                else:
                    anims.append(row.animate.set_fill(BLACK, opacity=0.65))
            return anims

        self.play(*set_spectro_rows("beta", ORANGE), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.10))
        self.play(*set_spectro_rows("theta", TEAL), run_time=max(0.05, 0.51))
        self.wait(max(0.05, 0.20))
        panel_labels.append(label3)

        # Gap 24.62-24.90
        self.wait(max(0.05, 0.28))

        # ------------------------------------------------------------
        # Beat 9: 24.90-29.24 -- panel 4: wavelet analysis
        # ------------------------------------------------------------
        self.play(
            panel3_content.animate.set_opacity(0.7),
            panel_rects[2].animate.set_fill(opacity=0.8),
            run_time=max(0.05, 0.30),
        )
        self.play(FadeOut(placeholder_icons[3]), run_time=max(0.05, 0.20))

        panel = panel_rects[3]
        left = panel.get_left()[0] + 0.20
        right = panel.get_right()[0] - 0.20
        bottom = panel.get_bottom()[1] + 0.24
        top = panel.get_top()[1] - 0.28

        def wfreq_to_y(f):
            return bottom + (f / 50.0) * (top - bottom)

        wcols = 16
        wrows = 7
        wcell_w = (right - left) / wcols
        wcell_h = (top - bottom) / wrows

        wavelet_grid = VGroup()
        for r in range(wrows):
            cy = bottom + (r + 0.5) * wcell_h
            for c in range(wcols):
                cell = Rectangle(
                    width=wcell_w * 0.92,
                    height=wcell_h * 0.92,
                    fill_color=BLACK,
                    fill_opacity=0.60,
                    stroke_color=GREY_B,
                    stroke_width=0.5,
                )
                cell.move_to(np.array([left + (c + 0.5) * wcell_w, cy, 0.0]))
                wavelet_grid.add(cell)

        # Localized transient burst in beta/gamma range
        burst_x = left + 0.55 * (right - left)
        burst_y = wfreq_to_y(28.0)
        burst = Ellipse(
            width=0.55,
            height=0.30,
            fill_color=RED,
            fill_opacity=0.9,
            stroke_width=0,
        )
        burst.move_to(np.array([burst_x, burst_y, 0.0]))
        burst.set_opacity(0.0)

        w_ticks = VGroup()
        w_tick_labels = VGroup()
        for val in [4, 8, 13, 30]:
            yt = wfreq_to_y(val)
            w_ticks.add(
                Line(
                    np.array([left - 0.07, yt, 0.0]),
                    np.array([left + 0.02, yt, 0.0]),
                    color=GREY_B,
                    stroke_width=1.2,
                )
            )
            w_tick_labels.add(Text(str(val), font_size=7, color=GREY_B).move_to(np.array([left - 0.25, yt, 0.0])))

        w_time_label = Text("Time", font_size=8, color=GREY_B)
        w_time_label.move_to(np.array([(left + right) / 2.0, bottom - 0.18, 0.0]))
        w_freq_label = Text("Freq (Hz)", font_size=8, color=GREY_B).rotate(PI / 2)
        w_freq_label.next_to(w_ticks, LEFT, buff=0.08)

        panel4_content = VGroup(
            wavelet_grid, burst, w_ticks, w_tick_labels, w_time_label, w_freq_label
        )
        panel4_content.scale_to_fit_width(panel_width - 0.20)
        panel4_content.scale_to_fit_height(panel_height - 0.20)
        panel4_content.move_to(panel.get_center())
        panel_contents[3] = panel4_content

        self.play(GrowFromCenter(panel4_content), run_time=max(0.05, 0.70))

        label4 = Text("Wavelet analysis", font_size=14, color=WHITE)
        label4.next_to(panel_rects[3], DOWN, buff=0.14)
        self.play(Write(label4), run_time=max(0.05, 0.50))

        arrow_3_4 = Arrow(
            start=panel_rects[2].get_right() + RIGHT * 0.15,
            end=panel_rects[3].get_left() + LEFT * 0.15,
            color=GREY_B,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.18,
        )
        self.play(Create(arrow_3_4), run_time=max(0.05, 0.40))

        self.play(burst.animate.set_opacity(1.0), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.30))
        self.play(burst.animate.set_opacity(0.0), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.94))
        panel_labels.append(label4)

        # Gap 29.24-30.22
        self.wait(max(0.05, 0.98))

        # ------------------------------------------------------------
        # Beat 10: 30.22-33.78 -- raw recedes, pipeline brightens
        # ------------------------------------------------------------
        all_arrows = VGroup(arrow_raw_to_panel1, arrow_1_2, arrow_2_3, arrow_3_4)
        self.play(
            raw_wave.animate.set_opacity(0.25).scale(0.85),
            *[p.animate.set_fill(opacity=0.95) for p in panel_rects],
            *[c.animate.set_opacity(1.0) for c in panel_contents],
            run_time=max(0.05, 1.50),
        )
        self.play(
            *[a.animate.set_color(YELLOW).set_stroke(width=4) for a in all_arrows],
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 1.06))

        # ------------------------------------------------------------
        # Beat 11: 33.78-37.18 -- highlight pipeline + confirmation
        # ------------------------------------------------------------
        labels_group = VGroup(*panel_labels)
        pipeline_group = VGroup(
            raw_wave,
            band_bars,
            panel_group,
            *panel_contents,
            labels_group,
            all_arrows,
        )
        highlight = SurroundingRectangle(
            pipeline_group,
            color=YELLOW,
            stroke_width=3,
            buff=0.15,
            corner_radius=0.08,
        )
        self.play(Create(highlight), run_time=max(0.05, 0.80))

        # Checkmark indicator built from primitives
        check_circle = Circle(
            radius=0.26,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=0,
        )
        check_line1 = Line(
            check_circle.get_center() + LEFT * 0.13 + DOWN * 0.03,
            check_circle.get_center() + LEFT * 0.02 + UP * 0.12,
            color=WHITE,
            stroke_width=4,
        )
        check_line2 = Line(
            check_circle.get_center() + LEFT * 0.02 + UP * 0.12,
            check_circle.get_center() + RIGHT * 0.15 + DOWN * 0.10,
            color=WHITE,
            stroke_width=4,
        )
        check_icon = VGroup(check_circle, check_line1, check_line2)
        check_icon.scale_to_fit_height(0.55)
        check_icon.next_to(highlight, RIGHT, buff=0.35).shift(UP * 1.25)

        self.play(GrowFromCenter(check_icon), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 2.10))

        # ------------------------------------------------------------
        # Beat 12: 37.18-37.88 -- final hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.70))