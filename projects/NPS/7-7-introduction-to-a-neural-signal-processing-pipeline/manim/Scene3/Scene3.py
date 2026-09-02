ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np
import json


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Helpers
        # ----------------------------------------------------------------
        def center_signal(y, y_center=0.0):
            return y - np.mean(y) + y_center

        def make_trace(xs, ys, color=WHITE, stroke_width=2, opacity=1):
            pts = np.array([xs, ys, np.zeros_like(xs)]).T
            trace = VMobject(color=color, stroke_width=stroke_width, fill_opacity=0)
            trace.set_points_as_corners(pts)
            trace.set_opacity(opacity)
            return trace

        def dashed_hline(x0, x1, y, color=GREY_B, dash_len=0.07, gap=0.05, stroke_width=2):
            parts = VGroup()
            x = x0
            while x < x1 - 1e-6:
                x2 = min(x + dash_len, x1)
                parts.add(Line([x, y, 0], [x2, y, 0], color=color, stroke_width=stroke_width))
                x = x2 + gap
            return parts

        def dashed_vline(x, y0, y1, color=GREY_B, dash_len=0.07, gap=0.05, stroke_width=2):
            parts = VGroup()
            y = y0
            while y < y1 - 1e-6:
                y2 = min(y + dash_len, y1)
                parts.add(Line([x, y, 0], [x, y2, 0], color=color, stroke_width=stroke_width))
                y = y2 + gap
            return parts

        def dashed_arrow(start, end, color=GREY_B, stroke_width=2, dash_len=0.12, gap=0.08):
            vec = end - start
            length = np.linalg.norm(vec)
            if length < 1e-6:
                return VGroup()
            unit = vec / length
            parts = VGroup()
            t = 0.0
            while t < length - dash_len:
                p1 = start + unit * t
                p2 = start + unit * (t + dash_len)
                parts.add(Line(p1, p2, color=color, stroke_width=stroke_width))
                t += dash_len + gap
            head_len = 0.22
            head_width = 0.10
            head_base = end - unit * head_len
            perp = np.array([-unit[1], unit[0], 0.0])
            b1 = head_base + perp * head_width
            b2 = head_base - perp * head_width
            parts.add(Polygon(end, b1, b2, color=color, fill_color=color, fill_opacity=1, stroke_width=0))
            return parts

        def make_card_label(text, rect, font_size=11):
            lab = Text(text, font_size=font_size, color=WHITE, weight="BOLD")
            lab.scale_to_fit_width(rect.width - 0.35)
            lab.move_to(rect.get_center())
            return lab

        # ----------------------------------------------------------------
        # Clean EEG trace from previous scene (placed initially at center)
        # ----------------------------------------------------------------
        xs = np.linspace(-2.8, 2.8, 420)
        clean_ys = center_signal(
            0.38 * np.sin(2.3 * xs + 0.2)
            + 0.12 * np.sin(5.8 * xs + 0.7)
            + 0.08 * np.sin(9.5 * xs + 1.2)
        )
        eeg_trace = make_trace(xs, clean_ys, color=BLUE, stroke_width=5)
        eeg_trace.scale_to_fit_width(5.3).move_to(ORIGIN)

        # Previous scene residue: boxes, side panel, label
        old_boxes = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=0.72, height=0.38,
                             stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0)
            for _ in range(6)
        ]).arrange(RIGHT, buff=0.14).move_to(np.array([-0.3, -1.55, 0]))

        old_panel = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=1.45, height=0.45,
                             stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.12).move_to(np.array([5.2, -0.15, 0]))

        old_label = Text("Preprocessing Pipeline", font_size=16, color=GREY_B)
        old_label.next_to(old_boxes, DOWN, buff=0.15)

        self.add(eeg_trace, old_boxes, old_panel, old_label)

        # ----------------------------------------------------------------
        # Layout constants
        # ----------------------------------------------------------------
        eeg_center = np.array([-4.35, 2.10, 0])
        trace_target_width = 4.2
        trace_scale = trace_target_width / eeg_trace.get_width()

        # ----------------------------------------------------------------
        # Beat 1 (0.00-1.80): trace to top-left, old state fades, divider
        # ----------------------------------------------------------------
        divider_right = Line(
            np.array([-2.2, 0.1, 0]),
            np.array([6.5, 0.1, 0]),
            color=GREY_B,
            stroke_width=2,
        ).set_opacity(0.28)

        self.play(
            eeg_trace.animate.scale(trace_scale).move_to(eeg_center),
            FadeOut(old_boxes),
            FadeOut(old_panel),
            FadeOut(old_label),
            FadeIn(divider_right),
            run_time=max(0.05, 1.80),
        )

        # ----------------------------------------------------------------
        # Beat 2 (1.80-3.04): pulse, question mark, "Extract?"
        # ----------------------------------------------------------------
        question_mark = Text("?", font_size=80, color=GREY_B, fill_opacity=0.16)
        question_mark.move_to(np.array([-1.65, 2.15, 0]))
        question_mark.set_stroke(GREY_B, width=1.2, opacity=0.45)

        extract_word = Text("Extract?", font_size=22, color=GREY_B)
        extract_word.next_to(question_mark, DOWN, buff=0.08)

        self.play(
            Indicate(eeg_trace, color=YELLOW, scale_factor=1.05),
            FadeIn(question_mark),
            FadeIn(extract_word),
            run_time=max(0.05, 1.24),
        )

        # ----------------------------------------------------------------
        # Beat 3 (3.04-5.64): five empty cards + dashed downward arrow
        # ----------------------------------------------------------------
        eeg_card_rects = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=2.35, height=0.48,
                             stroke_color=WHITE, stroke_width=2, fill_opacity=0)
            for _ in range(5)
        ]).arrange(DOWN, buff=0.12).move_to(np.array([1.45, 0.65, 0]))

        arrow_start = np.array([-2.05, 1.92, 0])
        arrow_end = np.array([0.15, 1.72, 0])
        dashed_arrow_grp = dashed_arrow(arrow_start, arrow_end, color=GREY_B, stroke_width=2)

        self.play(
            FadeIn(eeg_card_rects, shift=UP * 0.15),
            FadeIn(dashed_arrow_grp),
            run_time=max(0.05, 2.60),
        )

        # ----------------------------------------------------------------
        # Beat 4 (5.64-7.42): title, bright trace, solid arrow
        # ----------------------------------------------------------------
        feature_title = Text("Feature Extraction", font_size=32, color=WHITE, weight="BOLD")
        feature_title.move_to(np.array([-4.35, 3.35, 0]))

        solid_arrow = Arrow(
            arrow_start,
            arrow_end,
            color=WHITE,
            stroke_width=5,
            buff=0.08,
            max_tip_length_to_length_ratio=0.20,
        )

        self.play(
            Write(feature_title),
            eeg_trace.animate.set_stroke(width=6).set_opacity(1),
            FadeOut(dashed_arrow_grp),
            FadeIn(solid_arrow),
            run_time=max(0.05, 1.78),
        )

        # ----------------------------------------------------------------
        # Beat 5 (7.42-9.90): measurement grid and guide lines
        # ----------------------------------------------------------------
        pts = eeg_trace.get_all_points()
        tmin_y = pts[:, 1].min()
        tmax_y = pts[:, 1].max()
        gx0 = eeg_trace.get_left()[0] - 0.20
        gx1 = eeg_trace.get_right()[0] + 0.20
        gy0 = tmin_y - 0.22
        gy1 = tmax_y + 0.22

        measurement_grid = VGroup(
            *[Line([gx0, y, 0], [gx1, y, 0], color=GREY_B, stroke_width=1)
              for y in np.linspace(gy0, gy1, 4)],
            *[Line([x, gy0, 0], [x, gy1, 0], color=GREY_B, stroke_width=1)
              for x in np.linspace(gx0, gx1, 5)],
        ).set_opacity(0.22)

        measure_guides = VGroup(
            Line([gx0, tmin_y, 0], [gx0, tmax_y, 0], color=WHITE, stroke_width=1.5),
            Line([gx1, tmin_y, 0], [gx1, tmax_y, 0], color=WHITE, stroke_width=1.5),
            dashed_hline(gx0, gx1, tmax_y, color=WHITE, dash_len=0.06, gap=0.05, stroke_width=1.5),
            dashed_hline(gx0, gx1, tmin_y, color=WHITE, dash_len=0.06, gap=0.05, stroke_width=1.5),
        )

        self.play(
            FadeIn(measurement_grid),
            Create(measure_guides),
            run_time=max(0.05, 2.48),
        )

        # ----------------------------------------------------------------
        # Beat 6 (9.90-12.52): "x =", cursor, dotted measurement lines
        # ----------------------------------------------------------------
        sample_xs = [gx0 + 0.45, gx0 + 1.05, gx0 + 1.70, gx0 + 2.35, gx0 + 3.05]
        meas_vlines = VGroup(*[
            dashed_vline(x, gy0 + 0.08, gy1 - 0.08, color=WHITE, dash_len=0.04, gap=0.04, stroke_width=1.2)
            for x in sample_xs
        ]).set_opacity(0.70)

        x_eq = Text("x =", font_size=27, color=WHITE).move_to(np.array([-3.10, 1.10, 0]))
        cursor = Line(
            np.array([-2.72, 1.00, 0]),
            np.array([-2.72, 1.38, 0]),
            color=WHITE,
            stroke_width=3,
        )

        quant_label = Text("Quantitative measurements", font_size=20, color=WHITE)
        quant_label.move_to(np.array([1.45, 2.95, 0]))

        self.play(
            Write(x_eq),
            FadeIn(cursor),
            FadeIn(meas_vlines),
            FadeIn(quant_label),
            run_time=max(0.05, 1.42),
        )

        # Cursor blink
        for _ in range(2):
            self.play(cursor.animate.set_opacity(0.22), run_time=max(0.05, 0.20))
            self.play(cursor.animate.set_opacity(1), run_time=max(0.05, 0.20))

        self.wait(max(0.05, 0.40))

        # ----------------------------------------------------------------
        # Beat 7 (12.52-16.28): remove x/grid, add depends + EEG badge
        # ----------------------------------------------------------------
        depends_label = Text("Depends on application", font_size=18, color=GREY_B, slant="ITALIC")
        depends_label.move_to(np.array([1.45, 3.35, 0]))

        eeg_badge = Text("EEG", font_size=20, color=BLUE, weight="BOLD")
        eeg_badge.move_to(np.array([-4.35, 1.35, 0]))

        remove_meas_group = VGroup(measurement_grid, measure_guides, meas_vlines, x_eq, cursor)

        self.play(FadeOut(remove_meas_group), run_time=max(0.05, 1.40))
        self.play(FadeIn(depends_label), FadeIn(eeg_badge), run_time=max(0.05, 1.26))
        self.wait(max(0.05, 1.10))

        # ----------------------------------------------------------------
        # Build EEG card labels (invisible)
        # ----------------------------------------------------------------
        eeg_feature_names = [
            "Signal Amplitude",
            "Frequency-Band Power",
            "Spectral Characteristics",
            "Time-Frequency Features",
            "Event-Related Responses",
        ]
        eeg_card_labels = VGroup(*[
            make_card_label(name, rect, font_size=11)
            for name, rect in zip(eeg_feature_names, eeg_card_rects)
        ])
        eeg_card_labels.set_opacity(0)
        self.add(eeg_card_labels)

        # ----------------------------------------------------------------
        # Beat 8 (16.28-19.46): first EEG card: Signal Amplitude
        # ----------------------------------------------------------------
        self.play(
            eeg_card_rects[0].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            eeg_card_labels[0].animate.set_opacity(1),
            run_time=max(0.05, 0.70),
        )

        pts = eeg_trace.get_all_points()
        tmin_y = pts[:, 1].min()
        tmax_y = pts[:, 1].max()
        ax0 = eeg_trace.get_left()[0] - 0.10
        ax1 = eeg_trace.get_right()[0] + 0.10

        amp_h_top = dashed_hline(ax0, ax1, tmax_y, color=YELLOW, dash_len=0.06, gap=0.04, stroke_width=1.5)
        amp_h_bot = dashed_hline(ax0, ax1, tmin_y, color=YELLOW, dash_len=0.06, gap=0.04, stroke_width=1.5)
        extent_rect = Rectangle(
            width=ax1 - ax0,
            height=tmax_y - tmin_y,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=0,
        ).move_to(np.array([(ax0 + ax1) / 2, (tmin_y + tmax_y) / 2, 0]))

        amp_darrow = DoubleArrow(
            start=np.array([ax1 + 0.30, tmin_y, 0]),
            end=np.array([ax1 + 0.30, tmax_y, 0]),
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )
        amp_label = Text("peak-to-peak", font_size=12, color=YELLOW)
        amp_label.next_to(amp_darrow, RIGHT, buff=0.08)

        amplitude_group = VGroup(amp_h_top, amp_h_bot, extent_rect, amp_darrow, amp_label)

        self.play(
            FadeIn(extent_rect),
            Create(amp_h_top),
            Create(amp_h_bot),
            FadeIn(amp_darrow),
            FadeIn(amp_label),
            run_time=max(0.05, 1.60),
        )
        self.wait(max(0.05, 0.88))

        # ----------------------------------------------------------------
        # Beat 9 (19.46-21.62): second EEG card: Frequency-Band Power
        # ----------------------------------------------------------------
        self.play(FadeOut(amplitude_group), run_time=max(0.05, 0.30))
        self.play(
            eeg_card_rects[1].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            eeg_card_labels[1].animate.set_opacity(1),
            run_time=max(0.05, 0.60),
        )

        band_names = ["delta", "theta", "alpha", "beta", "gamma"]
        band_heights = [0.55, 0.75, 1.15, 0.85, 0.60]
        band_colors = [BLUE, TEAL, GREEN, ORANGE, PURPLE]
        band_bars = VGroup(*[
            Rectangle(width=0.34, height=h, fill_color=c, fill_opacity=1, stroke_width=0)
            for h, c in zip(band_heights, band_colors)
        ]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)

        band_labels = VGroup()
        for bar, name in zip(band_bars, band_names):
            lab = Text(name, font_size=10, color=WHITE)
            lab.next_to(bar, DOWN, buff=0.06)
            band_labels.add(lab)

        band_chart_group = VGroup(band_bars, band_labels)
        band_chart_group.move_to(np.array([4.15, eeg_card_rects[1].get_center()[1], 0]))

        self.play(
            Create(band_bars),
            FadeIn(band_labels),
            run_time=max(0.05, 0.90),
        )
        self.wait(max(0.05, 0.36))

        # ----------------------------------------------------------------
        # Beat 10 (21.62-23.92): third card: Spectral Characteristics
        # ----------------------------------------------------------------
        self.play(FadeOut(band_chart_group), run_time=max(0.05, 0.25))
        self.play(
            eeg_card_rects[2].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            eeg_card_labels[2].animate.set_opacity(1),
            run_time=max(0.05, 0.45),
        )

        card_y3 = eeg_card_rects[2].get_center()[1]
        spec_origin = np.array([3.00, card_y3 - 0.50, 0])
        x_axis = Arrow(
            spec_origin,
            spec_origin + np.array([2.30, 0, 0]),
            color=WHITE,
            stroke_width=2,
            buff=0.04,
            max_tip_length_to_length_ratio=0.10,
        )
        y_axis = Arrow(
            spec_origin + np.array([0, -0.15, 0]),
            spec_origin + np.array([0, 1.30, 0]),
            color=WHITE,
            stroke_width=2,
            buff=0.04,
            max_tip_length_to_length_ratio=0.10,
        )

        xs_spec = np.linspace(spec_origin[0] + 0.06, spec_origin[0] + 2.24, 130)
        ys_spec = (
            spec_origin[1]
            + 0.12
            + 0.92 * np.exp(-((xs_spec - (spec_origin[0] + 1.00)) ** 2) / (2 * 0.25 ** 2))
            + 0.08 * np.sin(7 * xs_spec - 1.0)
        )
        spectrum_curve = make_trace(xs_spec, ys_spec, color=GREEN, stroke_width=3)

        freq_label = Text("Frequency", font_size=12, color=WHITE)
        freq_label.next_to(x_axis, DOWN, buff=0.08)
        power_label = Text("Power", font_size=12, color=WHITE)
        power_label.rotate(PI / 2)
        power_label.next_to(y_axis, LEFT, buff=0.06)

        spectrum_group = VGroup(x_axis, y_axis, spectrum_curve, freq_label, power_label)

        self.play(
            Create(VGroup(x_axis, y_axis)),
            Create(spectrum_curve),
            FadeIn(freq_label),
            FadeIn(power_label),
            run_time=max(0.05, 1.30),
        )
        self.wait(max(0.05, 0.30))

        # ----------------------------------------------------------------
        # Beat 11 (23.92-25.38): fourth card: Time-Frequency Features
        # ----------------------------------------------------------------
        self.play(FadeOut(spectrum_group), run_time=max(0.05, 0.20))
        self.play(
            eeg_card_rects[3].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            eeg_card_labels[3].animate.set_opacity(1),
            run_time=max(0.05, 0.40),
        )

        spec_grid_colors = [
            [BLUE, BLUE, TEAL, TEAL, GREEN, GREEN],
            [BLUE, TEAL, GREEN, ORANGE, ORANGE, PINK],
            [TEAL, GREEN, ORANGE, ORANGE, PINK, RED],
            [GREEN, ORANGE, ORANGE, PINK, RED, PURPLE],
            [ORANGE, PINK, RED, RED, PURPLE, PURPLE],
        ]
        spec_cells = VGroup()
        for row in range(5):
            for col in range(6):
                cell = Rectangle(width=0.31, height=0.22,
                                 fill_color=spec_grid_colors[row][col],
                                 fill_opacity=1, stroke_width=0)
                spec_cells.add(cell)
        spec_cells.arrange_in_grid(rows=5, cols=6, buff=0.04)
        spec_cells.move_to(np.array([3.85, eeg_card_rects[3].get_center()[1] + 0.10, 0]))

        colorbar_colors = [BLUE, TEAL, GREEN, ORANGE, PINK, RED, PURPLE]
        colorbar_rects = VGroup(*[
            Rectangle(width=0.12, height=0.15, fill_color=c, fill_opacity=1, stroke_width=0)
            for c in reversed(colorbar_colors)
        ]).arrange(UP, buff=0)
        colorbar_rects.next_to(spec_cells, RIGHT, buff=0.14)
        colorbar_power_label = Text("Power", font_size=11, color=WHITE)
        colorbar_power_label.next_to(colorbar_rects, UP, buff=0.05)

        spectrogram_group = VGroup(spec_cells, colorbar_rects, colorbar_power_label)

        self.play(FadeIn(spectrogram_group), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.16))

        # ----------------------------------------------------------------
        # Beat 12 (25.38-26.34): fifth card: Event-Related Responses
        # ----------------------------------------------------------------
        self.play(FadeOut(spectrogram_group), run_time=max(0.05, 0.15))
        self.play(
            eeg_card_rects[4].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            eeg_card_labels[4].animate.set_opacity(1),
            run_time=max(0.05, 0.25),
        )

        xs_erp = np.linspace(0, 2, 100)
        ys_erp = (
            0.60 * np.exp(-((xs_erp - 0.85) ** 2) / (2 * 0.15 ** 2))
            - 0.22 * np.exp(-((xs_erp - 1.15) ** 2) / (2 * 0.12 ** 2))
        )
        avg_wave = make_trace(xs_erp, ys_erp, color=BLUE, stroke_width=3)
        avg_wave.scale_to_fit_width(1.60)
        avg_wave.move_to(np.array([4.10, eeg_card_rects[4].get_center()[1], 0]))

        erp_line_positions = [0.25, 0.60, 0.95, 1.30, 1.65]
        erp_lines = VGroup(*[
            Line(
                np.array([avg_wave.get_left()[0] + dx * avg_wave.get_width() / 2,
                          avg_wave.get_center()[1] - 0.28, 0]),
                np.array([avg_wave.get_left()[0] + dx * avg_wave.get_width() / 2,
                          avg_wave.get_center()[1] + 0.28, 0]),
                color=WHITE,
                stroke_width=1.2,
            )
            for dx in erp_line_positions
        ])
        event_label = Text("event", font_size=10, color=WHITE)
        event_label.next_to(erp_lines[0], DOWN, buff=0.04)

        erp_group = VGroup(avg_wave, erp_lines, event_label)

        self.play(
            Create(avg_wave),
            FadeIn(erp_lines),
            FadeIn(event_label),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.16))

        # ----------------------------------------------------------------
        # Beat 13 (26.34-27.64): EEG dims, right clears, spike train appears
        # ----------------------------------------------------------------
        eeg_section_group = VGroup(
            eeg_trace,
            eeg_card_rects,
            eeg_card_labels,
            feature_title,
            quant_label,
            depends_label,
            eeg_badge,
            solid_arrow,
            question_mark,
            extract_word,
        )

        self.play(
            eeg_section_group.animate.set_opacity(0.38),
            FadeOut(erp_group),
            run_time=max(0.05, 0.60),
        )

        # Horizontal divider between upper and spike areas
        middle_divider = Line(
            np.array([-6.5, -0.5, 0]),
            np.array([6.5, -0.5, 0]),
            color=GREY_B,
            stroke_width=2,
        ).set_opacity(0.45)
        self.play(Create(middle_divider), run_time=max(0.05, 0.30))

        # Spike train on right side
        spike_line_left = 3.2
        spike_line_right = 6.3
        spike_y = 1.6
        spike_train_line = Line(
            np.array([spike_line_left, spike_y, 0]),
            np.array([spike_line_right, spike_y, 0]),
            color=WHITE,
            stroke_width=2,
        )
        # Irregular cluster positions
        spike_x_rel = [
            3.35, 3.45, 4.1, 4.18, 4.22, 4.9, 5.0, 5.05, 5.7, 5.78, 6.15
        ]
        spike_ticks = VGroup(*[
            Line(
                np.array([x, spike_y + 0.55, 0]),
                np.array([x, spike_y - 0.55, 0]),
                color=WHITE,
                stroke_width=3,
            )
            for x in spike_x_rel
        ])
        spike_train_group = VGroup(spike_train_line, spike_ticks)

        self.play(Create(spike_train_group), run_time=max(0.05, 0.40))

        # ----------------------------------------------------------------
        # Beat 14 (26.34-28.80): magnified spike waveforms
        # ----------------------------------------------------------------
        mag_waves = []
        mag_group = VGroup()
        mag_colors = [TEAL, BLUE, PURPLE, ORANGE]
        mag_xs = np.linspace(-0.6, 0.6, 90)
        for i, color in enumerate(mag_colors):
            if i % 2 == 0:
                mag_ys = (
                    1.70 * np.exp(-((mag_xs - 0.02) ** 2) / (2 * 0.045 ** 2))
                    - 0.55 * np.exp(-((mag_xs + 0.12) ** 2) / (2 * 0.07 ** 2))
                )
            else:
                mag_ys = (
                    -1.45 * np.exp(-((mag_xs + 0.02) ** 2) / (2 * 0.04 ** 2))
                    + 0.50 * np.exp(-((mag_xs - 0.10) ** 2) / (2 * 0.06 ** 2))
                )
            box = RoundedRectangle(
                corner_radius=0.08,
                width=0.9,
                height=0.55,
                stroke_color=GREY_B,
                stroke_width=1.5,
                fill_color=BLUE_D,
                fill_opacity=0.08,
            )
            wave = make_trace(mag_xs, mag_ys, color=color, stroke_width=3)
            wave.scale_to_fit_width(0.65)
            wave.move_to(box.get_center())
            mag_waves.append(wave)
            mag_group.add(box, wave)

        mag_group.arrange(RIGHT, buff=0.12).move_to(np.array([4.8, 0.55, 0]))

        self.play(FadeIn(mag_group), run_time=max(0.05, 1.16))

        # ----------------------------------------------------------------
        # Beat 15 (28.80-30.74): spike cards + first: Spike Count
        # ----------------------------------------------------------------
        spike_card_rects = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=0.85, height=0.48,
                             stroke_color=WHITE, stroke_width=2, fill_opacity=0)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.12).move_to(np.array([4.7, -0.95, 0]))

        spike_card_names = [
            "Spike Count",
            "Firing Rate",
            "Spike Timing",
            "Spike Waveform Characteristics",
        ]
        spike_card_labels = VGroup(*[
            make_card_label(name, rect, font_size=9)
            for name, rect in zip(spike_card_names, spike_card_rects)
        ])
        spike_card_labels.set_opacity(0)
        self.add(spike_card_labels)

        self.play(FadeIn(spike_card_rects), run_time=max(0.05, 0.30))
        self.play(
            spike_card_rects[0].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            spike_card_labels[0].animate.set_opacity(1),
            run_time=max(0.05, 0.40),
        )

        # Tally marks
        tally_lines = []
        for i in range(len(spike_x_rel)):
            row, col = divmod(i, 5)
            x = 5.65 + col * 0.16
            y = 1.72 + row * 0.20
            tally_lines.append(
                Line(
                    np.array([x, y, 0]),
                    np.array([x, y + 0.34, 0]),
                    color=WHITE,
                    stroke_width=3,
                )
            )
        tally_visual_group = VGroup(*tally_lines)

        per_tally = max(0.05, 1.24 / len(spike_x_rel))
        for i in range(len(spike_x_rel)):
            self.play(
                GrowFromCenter(tally_lines[i]),
                spike_ticks[i].animate.set_color(YELLOW),
                run_time=max(0.05, per_tally),
            )

        # ----------------------------------------------------------------
        # Beat 16 (30.74-31.86): second spike card: Firing Rate
        # ----------------------------------------------------------------
        self.play(FadeOut(tally_visual_group), run_time=max(0.05, 0.20))
        self.play(
            spike_card_rects[1].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            spike_card_labels[1].animate.set_opacity(1),
            run_time=max(0.05, 0.40),
        )

        firing_counts = [2, 1, 4, 3]
        firing_bars = VGroup(*[
            Rectangle(width=0.40, height=0.16 * count,
                      fill_color=ORANGE, fill_opacity=1, stroke_width=0)
            for count in firing_counts
        ]).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        firing_bars.move_to(np.array([5.05, 1.35, 0]))

        axis_bottom = firing_bars[0].get_bottom()[1]
        axis_line = Line(
            np.array([firing_bars[0].get_left()[0] - 0.15, axis_bottom, 0]),
            np.array([firing_bars[-1].get_right()[0] + 0.15, axis_bottom, 0]),
            color=WHITE,
            stroke_width=2,
        )
        bin_ticks = VGroup(*[
            Line(
                np.array([bar.get_center()[0], axis_bottom - 0.05, 0]),
                np.array([bar.get_center()[0], axis_bottom + 0.03, 0]),
                color=WHITE,
                stroke_width=1.5,
            )
            for bar in firing_bars
        ])
        rate_label = Text("spikes/sec", font_size=10, color=WHITE)
        rate_label.next_to(axis_line, RIGHT, buff=0.08).shift(DOWN * 0.1)
        firing_chart = VGroup(firing_bars, axis_line, bin_ticks, rate_label)

        self.play(Create(firing_chart), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.02))

        # ----------------------------------------------------------------
        # Beat 17 (31.86-32.80): third spike card: Spike Timing
        # ----------------------------------------------------------------
        self.play(FadeOut(firing_chart), run_time=max(0.05, 0.12))
        self.play(
            spike_card_rects[2].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            spike_card_labels[2].animate.set_opacity(1),
            run_time=max(0.05, 0.25),
        )

        interval_xs = [3.9, 4.7, 5.4, 6.0]
        timing_ref_lines = VGroup(*[
            dashed_vline(x, spike_y - 0.65, spike_y + 0.65, color=WHITE, dash_len=0.05, gap=0.04, stroke_width=1.5)
            for x in interval_xs
        ])
        timing_labels = VGroup(*[
            Text(f"{tick.get_center()[0]:.2f}", font_size=9, color=YELLOW)
            .move_to(np.array([tick.get_center()[0], spike_y - 0.88, 0]))
            for tick in spike_ticks
        ])
        spike_timing_overlay = VGroup(timing_ref_lines, timing_labels)

        self.play(FadeIn(spike_timing_overlay), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.07))

        # ----------------------------------------------------------------
        # Beat 18 (32.80-35.34): fourth spike card: Waveform Characteristics
        # ----------------------------------------------------------------
        self.play(FadeOut(spike_timing_overlay), run_time=max(0.05, 0.20))
        self.play(
            spike_card_rects[3].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            spike_card_labels[3].animate.set_opacity(1),
            run_time=max(0.05, 0.35),
        )
        self.play(
            *[wave.animate.set_stroke(YELLOW, width=4) for wave in mag_waves],
            run_time=max(0.05, 0.40),
        )

        wave_pts = mag_waves[0].get_all_points()
        wx = wave_pts[:, 0]
        wy = wave_pts[:, 1]
        wmin_y = wy.min()
        wmax_y = wy.max()
        wpeak_idx = int(np.argmax(wy))
        wpeak_x = wx[wpeak_idx]
        wpeak_y = wy[wpeak_idx]
        half_y = wmin_y + 0.5 * (wmax_y - wmin_y)
        above_idx = np.where(wy >= half_y)[0]
        wx1 = wx[above_idx[0]]
        wx2 = wx[above_idx[-1]]

        area_poly = Polygon(
            *[[wx[i], wy[i], 0] for i in range(len(wx))],
            *[[wx[-1], wmin_y, 0], [wx[0], wmin_y, 0]],
            fill_color=YELLOW,
            fill_opacity=0.22,
            stroke_width=0,
        )
        peak_measure_line = dashed_vline(
            wpeak_x, wmin_y - 0.10, wmax_y + 0.10, color=YELLOW, dash_len=0.05, gap=0.04, stroke_width=1.5
        )
        width_measure_arrow = DoubleArrow(
            start=np.array([wx1, half_y, 0]),
            end=np.array([wx2, half_y, 0]),
            color=WHITE,
            stroke_width=2.5,
            buff=0.04,
            max_tip_length_to_length_ratio=0.20,
        )
        amplitude_measure_label = Text("amplitude", font_size=10, color=YELLOW)
        amplitude_measure_label.next_to(peak_measure_line, RIGHT, buff=0.05)
        width_measure_label = Text("width", font_size=10, color=WHITE)
        width_measure_label.next_to(width_measure_arrow, UP, buff=0.05)

        spike_measurement_group = VGroup(
            area_poly, peak_measure_line, width_measure_arrow,
            amplitude_measure_label, width_measure_label,
        )

        self.play(FadeIn(spike_measurement_group), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.59))

        # ----------------------------------------------------------------
        # Beat 19 (35.34-40.12): clear upper sections, EMG appears
        # ----------------------------------------------------------------
        spike_section_group = VGroup(
            spike_train_group,
            mag_group,
            spike_card_rects,
            spike_card_labels,
            spike_measurement_group,
        )

        bottom_divider = Line(
            np.array([-6.5, -2.55, 0]),
            np.array([6.5, -2.55, 0]),
            color=GREY_B,
            stroke_width=2,
        ).set_opacity(0.30)

        emg_xs = np.linspace(-2.6, 2.6, 480)
        env_bursts = (
            np.exp(-((emg_xs + 1.35) ** 2) / (2 * 0.35 ** 2))
            + 0.45 * np.exp(-((emg_xs - 1.10) ** 2) / (2 * 0.40 ** 2))
        )
        envelope = 0.18 + 0.80 * env_bursts
        envelope_centered = envelope - np.mean(envelope)
        emg_raw = envelope_centered * (np.sin(27 * emg_xs) + 0.35 * np.sin(61 * emg_xs))
        emg_y_centered = center_signal(emg_raw)

        emg_trace = make_trace(emg_xs, emg_y_centered, color=ORANGE, stroke_width=3)
        emg_trace.scale_to_fit_width(4.2).move_to(np.array([-3.8, -3.25, 0]))
        emg_envelope_line = make_trace(emg_xs, envelope_centered, color=YELLOW, stroke_width=2.5)
        emg_envelope_line.scale_to_fit_width(4.2).move_to(emg_trace.get_center())

        emg_label = Text("EMG", font_size=18, color=ORANGE, weight="BOLD")
        emg_label.next_to(emg_trace, DOWN, buff=0.12)

        self.play(
            eeg_section_group.animate.set_opacity(0),
            spike_section_group.animate.set_opacity(0),
            Create(bottom_divider),
            Create(emg_trace),
            FadeIn(emg_label),
            run_time=max(0.05, 1.10),
        )

        # ----------------------------------------------------------------
        # Beat 20 (36.44-39.06): EMG feature cards
        # ----------------------------------------------------------------
        emg_card_rects = VGroup(
            RoundedRectangle(corner_radius=0.08, width=2.0, height=0.52,
                             stroke_color=WHITE, stroke_width=2, fill_opacity=0),
            RoundedRectangle(corner_radius=0.08, width=2.0, height=0.52,
                             stroke_color=WHITE, stroke_width=2, fill_opacity=0),
        ).arrange(DOWN, buff=0.18).move_to(np.array([2.8, -3.25, 0]))

        emg_card_labels = VGroup(
            make_card_label("Strength", emg_card_rects[0], font_size=11),
            make_card_label("Temporal Characteristics", emg_card_rects[1], font_size=10),
        )
        emg_card_labels.set_opacity(0)

        self.play(FadeIn(emg_card_rects), run_time=max(0.05, 0.20))

        # Strength overlay: envelope line + vertical bars
        emg_disp_xs = [
            emg_trace.get_left()[0] + frac * emg_trace.get_width()
            for frac in [0.10, 0.22, 0.34, 0.50, 0.66, 0.78, 0.90]
        ]
        envelope_points = emg_envelope_line.get_all_points()
        env_xs_vals = envelope_points[:, 0]
        env_ys_vals = envelope_points[:, 1]
        base_emg_y = emg_trace.get_center()[1]

        strength_bars = VGroup()
        for x in emg_disp_xs:
            idx = int(np.argmin(np.abs(env_xs_vals - x)))
            env_y = env_ys_vals[idx]
            strength_bars.add(
                Line(
                    np.array([x, base_emg_y, 0]),
                    np.array([x, env_y, 0]),
                    color=GREY_B,
                    stroke_width=2,
                )
            )
        strength_overlay = VGroup(strength_bars, emg_envelope_line)

        self.play(
            emg_card_rects[0].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            emg_card_labels[0].animate.set_opacity(1),
            FadeIn(strength_bars),
            FadeIn(emg_envelope_line),
            run_time=max(0.05, 0.70),
        )

        # Temporal Characteristics overlay: burst durations and interval
        emg_left = emg_trace.get_left()[0]
        emg_width = emg_trace.get_width()
        burst1_x0 = emg_left + 0.08 * emg_width
        burst1_x1 = emg_left + 0.38 * emg_width
        burst2_x0 = emg_left + 0.64 * emg_width
        burst2_x1 = emg_left + 0.94 * emg_width
        burst_y = base_emg_y - 0.65

        burst_arrow1 = DoubleArrow(
            start=np.array([burst1_x0, burst_y, 0]),
            end=np.array([burst1_x1, burst_y, 0]),
            color=WHITE,
            stroke_width=2.5,
            buff=0.04,
            max_tip_length_to_length_ratio=0.16,
        )
        burst_arrow2 = DoubleArrow(
            start=np.array([burst2_x0, burst_y, 0]),
            end=np.array([burst2_x1, burst_y, 0]),
            color=WHITE,
            stroke_width=2.5,
            buff=0.04,
            max_tip_length_to_length_ratio=0.16,
        )
        interval_arrow = DoubleArrow(
            start=np.array([burst1_x1 + 0.06, burst_y - 0.25, 0]),
            end=np.array([burst2_x0 - 0.06, burst_y - 0.25, 0]),
            color=GREY_B,
            stroke_width=2,
            buff=0.04,
            max_tip_length_to_length_ratio=0.16,
        )
        burst_label1 = Text("burst", font_size=10, color=YELLOW)
        burst_label1.next_to(burst_arrow1, UP, buff=0.04)
        burst_label2 = Text("burst", font_size=10, color=YELLOW)
        burst_label2.next_to(burst_arrow2, UP, buff=0.04)
        interval_label = Text("interval", font_size=10, color=GREY_B)
        interval_label.next_to(interval_arrow, UP, buff=0.04)

        temporal_overlay = VGroup(
            burst_arrow1, burst_arrow2, interval_arrow,
            burst_label1, burst_label2, interval_label,
        )

        self.play(
            emg_card_rects[1].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(YELLOW, width=3),
            emg_card_labels[1].animate.set_opacity(1),
            FadeIn(temporal_overlay),
            run_time=max(0.05, 1.00),
        )

        self.wait(max(0.05, 0.72))
        self.wait(max(0.05, 1.06))

        # ----------------------------------------------------------------
        # Beat 21 (40.12-41.10): all three sections visible simultaneously
        # ----------------------------------------------------------------
        emg_section_full = VGroup(
            emg_trace,
            emg_label,
            emg_card_rects,
            emg_card_labels,
            strength_overlay,
            temporal_overlay,
        )

        layout_dividers = VGroup(middle_divider, bottom_divider)

        self.play(
            eeg_section_group.animate.set_opacity(0.78),
            spike_section_group.animate.set_opacity(0.78),
            run_time=max(0.05, 0.50),
        )
        self.play(
            Indicate(layout_dividers, color=YELLOW, scale_factor=1.06),
            run_time=max(0.05, 0.48),
        )

        # ----------------------------------------------------------------
        # Beat 22 (41.10-45.40): layout shrinks, bottom statement
        # ----------------------------------------------------------------
        whole_layout = VGroup(
            eeg_section_group,
            spike_section_group,
            emg_section_full,
            middle_divider,
            bottom_divider,
        )

        raw_word = Text("Raw waveform", font_size=30, color=BLUE, weight="BOLD")
        rel_word = Text("Relevant measurable features", font_size=30, color=YELLOW, weight="BOLD")
        statement_group = VGroup(raw_word, rel_word).arrange(RIGHT, buff=1.55)
        statement_arrow = Arrow(
            raw_word.get_right() + RIGHT * 0.15,
            rel_word.get_left() + LEFT * 0.15,
            color=WHITE,
            stroke_width=5,
            buff=0.05,
            max_tip_length_to_length_ratio=0.25,
        )
        statement_group.add(statement_arrow)
        statement_group.move_to(np.array([0, -3.05, 0]))
        travel_dot = Dot(radius=0.06, color=YELLOW).move_to(statement_arrow.get_start())

        self.play(
            whole_layout.animate.scale(0.72).shift(UP * 0.75),
            run_time=max(0.05, 0.70),
        )
        self.play(
            FadeIn(statement_group),
            FadeIn(travel_dot),
            run_time=max(0.05, 0.55),
        )
        self.play(
            Indicate(eeg_trace, color=BLUE, scale_factor=1.07),
            run_time=max(0.05, 0.60),
        )

        per_glow = max(0.05, 1.70 / 5)
        for rect in eeg_card_rects:
            self.play(
                Indicate(rect, color=YELLOW, scale_factor=1.10),
                run_time=max(0.05, per_glow),
            )

        self.play(
            travel_dot.animate.move_to(statement_arrow.get_end()),
            run_time=max(0.05, 0.75),
        )

        # ----------------------------------------------------------------
        # Beat 23 (45.40-46.92): statement dominates, layout dims
        # ----------------------------------------------------------------
        self.play(
            whole_layout.animate.set_opacity(0.30),
            statement_group.animate.set_opacity(1).scale(1.05),
            run_time=max(0.05, 0.70),
        )
        self.play(
            Indicate(statement_group, color=YELLOW, scale_factor=1.03),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 0.37))

        # ----------------------------------------------------------------
        # Beat 24 (46.92-52.10): mini trace → numeric values
        # ----------------------------------------------------------------
        mini_xs = np.linspace(-1.5, 1.5, 160)
        mini_ys = center_signal(
            0.25 * np.sin(3 * mini_xs) + 0.15 * np.sin(7 * mini_xs + 0.6)
        )
        mini_trace = make_trace(mini_xs, mini_ys, color=BLUE, stroke_width=3)
        mini_trace.scale_to_fit_width(1.75)
        mini_trace.move_to(np.array([5.0, -2.75, 0]))

        mini_x_eq = Text("x =", font_size=16, color=WHITE)
        mini_x_eq.next_to(mini_trace, LEFT, buff=0.18)

        num_values = ["−0.4", "0.6", "−0.2", "0.5", "−0.3"]
        num_boxes = VGroup()
        for val in num_values:
            box = RoundedRectangle(
                corner_radius=0.06,
                width=0.52,
                height=0.40,
                fill_color=BLUE_D,
                fill_opacity=0.85,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            txt = Text(val, font_size=13, color=WHITE)
            txt.move_to(box.get_center())
            num_boxes.add(VGroup(box, txt))
        num_boxes.arrange(RIGHT, buff=0.14)
        num_boxes.move_to(mini_trace.get_center())
        num_boxes.set_opacity(0)

        self.play(FadeIn(mini_trace), FadeIn(mini_x_eq), run_time=max(0.05, 0.70))

        for i in range(5):
            self.play(
                FadeIn(num_boxes[i], scale=0.6),
                mini_trace.animate.scale(0.88).set_opacity(max(0.25, 1 - 0.14 * (i + 1))),
                run_time=max(0.05, 0.60),
            )

        self.wait(max(0.05, 1.48))

        # ----------------------------------------------------------------
        # Beat 25 (52.10-52.90): final pulse and hold
        # ----------------------------------------------------------------
        self.play(
            Indicate(statement_group, color=YELLOW, scale_factor=1.03),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.40))