ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Constants and layout
        # ----------------------------------------------------------------
        PANEL_W = 3.0
        PANEL_H = 1.45
        PANEL_Y = 2.4
        LEFT_CX = -4.2
        RIGHT_CX = 4.2
        WAVE_BASE = PANEL_Y - 0.1
        WAVE_AMP = 0.38
        INNER_DX = 1.1

        def wave_pts(cx, n=180):
            x_min = cx - INNER_DX
            x_max = cx + INNER_DX
            xs = np.linspace(x_min, x_max, n)
            pts = []
            for x in xs:
                frac = (x - x_min) / (x_max - x_min)
                y = WAVE_BASE + WAVE_AMP * np.sin(2 * PI * 2.2 * frac)
                pts.append([x, y, 0.0])
            return pts

        def sample_pts(cx, count):
            x_min = cx - INNER_DX
            x_max = cx + INNER_DX
            xs = np.linspace(x_min, x_max, count)
            pts = []
            for x in xs:
                frac = (x - x_min) / (x_max - x_min)
                y = WAVE_BASE + WAVE_AMP * np.sin(2 * PI * 2.2 * frac)
                pts.append([x, y, 0.0])
            return pts

        def line_from_pts(pts, color, width):
            vm = VMobject()
            vm.set_stroke(color, width=width)
            vm.set_points_as_corners(pts)
            return vm

        def make_panel(cx):
            frame = Rectangle(width=PANEL_W, height=PANEL_H, color=GREY_B, stroke_width=1.5)
            frame.move_to(np.array([cx, PANEL_Y, 0.0]))
            inner_x_min = cx - INNER_DX
            inner_x_max = cx + INNER_DX
            axis_y = PANEL_Y - 0.35
            x_axis = Line(
                start=np.array([inner_x_min, axis_y, 0.0]),
                end=np.array([inner_x_max, axis_y, 0.0]),
                color=WHITE,
                stroke_width=1.2,
            )
            y_axis = Line(
                start=np.array([inner_x_min, axis_y, 0.0]),
                end=np.array([inner_x_min, axis_y + 0.7, 0.0]),
                color=WHITE,
                stroke_width=1.2,
            )
            wave = VMobject()
            wave.set_stroke(BLUE, width=3)
            wave.set_points_as_corners(wave_pts(cx, n=200))
            wave.set_opacity(0.35)
            return frame, x_axis, y_axis, wave

        def make_chain_node(label, color, center):
            circle = Circle(
                radius=0.36,
                fill_color=color,
                fill_opacity=0.2,
                stroke_color=color,
                stroke_width=2,
            )
            text = Text(label, font_size=16, color=WHITE, weight="BOLD")
            text.scale_to_fit_width(0.66)
            circle.move_to(center)
            text.move_to(center)
            return VGroup(circle, text)

        # ----------------------------------------------------------------
        # Build left panel: sparse sampling
        # ----------------------------------------------------------------
        left_frame, left_x_axis, left_y_axis, left_wave = make_panel(LEFT_CX)
        left_sample_pts = sample_pts(LEFT_CX, 5)
        left_recon = line_from_pts(left_sample_pts, ORANGE, width=4)
        left_sample_points = VGroup(*[Dot(point=p, radius=0.06, color=TEAL, fill_opacity=1) for p in left_sample_pts])

        left_wave_pts = wave_pts(LEFT_CX, n=600)
        arr = np.array(left_wave_pts)
        ys = arr[:, 1]
        max_idx = int(np.argmax(ys))
        min_idx = int(np.argmin(ys))

        missed_peak = VMobject()
        missed_peak.set_stroke(YELLOW, width=6)
        missed_peak.set_points_as_corners(left_wave_pts[max_idx - 20:max_idx + 20])
        missed_peak.set_opacity(0.0)

        missed_valley = VMobject()
        missed_valley.set_stroke(PINK, width=6)
        missed_valley.set_points_as_corners(left_wave_pts[min_idx - 20:min_idx + 20])
        missed_valley.set_opacity(0.0)

        left_label = Text(
            "Too few samples — information lost",
            font_size=17,
            color=WHITE,
            weight="BOLD",
        )
        left_label.scale_to_fit_width(2.95)
        left_label.next_to(left_frame, DOWN, buff=0.18)
        left_label.set_opacity(0.85)

        left_display = VGroup(
            left_frame, left_x_axis, left_y_axis, left_wave,
            left_recon, left_sample_points, left_label,
        )

        # ----------------------------------------------------------------
        # Build right panel: dense sampling
        # ----------------------------------------------------------------
        right_frame, right_x_axis, right_y_axis, right_wave = make_panel(RIGHT_CX)
        right_wave.set_opacity(0.35)

        right_display = VGroup(right_frame, right_x_axis, right_y_axis, right_wave)

        # Build dense samples now, but add them later
        right_sample_pts = sample_pts(RIGHT_CX, 28)
        right_sample_points = VGroup(*[
            Dot(point=p, radius=0.035, color=PURPLE, fill_opacity=1)
            for p in right_sample_pts
        ])
        right_recon = line_from_pts(right_sample_pts, GREEN, width=3)

        right_label = Text(
            "Excessive samples — extra storage,\nlittle added benefit",
            font_size=16,
            color=WHITE,
            weight="BOLD",
        )
        right_label.scale_to_fit_width(2.9)
        right_label.next_to(right_frame, DOWN, buff=0.18)

        # Misannotation arrow preparation
        left_sample_arr = np.array(left_sample_pts)
        peak_x = left_wave_pts[max_idx][0]
        idx_after = int(np.searchsorted(left_sample_arr[:, 0], peak_x))
        idx_before = max(0, idx_after - 1)
        x0, y0 = left_sample_arr[idx_before, 0], left_sample_arr[idx_before, 1]
        x1, y1 = left_sample_arr[idx_after, 0], left_sample_arr[idx_after, 1]
        t = (peak_x - x0) / (x1 - x0)
        flat_y = y0 + t * (y1 - y0)
        missed_arrow_end = np.array([peak_x, flat_y, 0.0])
        missed_arrow_start = missed_arrow_end + UP * 0.8
        missed_annotation_arrow = Arrow(
            start=missed_arrow_start,
            end=missed_arrow_end,
            color=YELLOW,
            stroke_width=3,
            buff=0.1,
        )

        self.add(missed_peak, missed_valley)

        # ----------------------------------------------------------------
        # BEAT 1: 0.00 - 0.90 opening two-panel layout
        # ----------------------------------------------------------------
        self.play(
            FadeIn(left_display),
            FadeIn(right_display),
            run_time=max(0.05, 0.90),
        )

        # ----------------------------------------------------------------
        # BEAT 2: 0.90 - 3.80 brighten left panel, pulse sparse points
        # ----------------------------------------------------------------
        self.play(left_frame.animate.set_stroke(WHITE, width=2.5), run_time=max(0.05, 1.0))
        self.play(Indicate(left_sample_points, color=TEAL, scale_factor=1.18), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.1))

        # ----------------------------------------------------------------
        # BEAT 3: 3.80 - 4.06 hold + left label full opacity
        # ----------------------------------------------------------------
        self.play(left_label.animate.set_opacity(1.0), run_time=max(0.05, 0.26))

        # ----------------------------------------------------------------
        # BEAT 4: 4.06 - 6.38 flash sparse points, trace reconstructed segments
        # ----------------------------------------------------------------
        left_recon_trace = line_from_pts(left_sample_pts, YELLOW, width=5)
        for i, pt in enumerate(left_sample_points):
            self.play(Indicate(pt, color=YELLOW, scale_factor=1.25), run_time=max(0.05, 0.13))
            if i < 4:
                self.wait(max(0.05, 0.03))
        self.play(Create(left_recon_trace), run_time=max(0.05, 0.9))
        self.play(
            missed_peak.animate.set_opacity(0.85),
            missed_valley.animate.set_opacity(0.85),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 0.20))

        # ----------------------------------------------------------------
        # BEAT 5: 6.38 - 10.76 emphasize missed peak/valley and annotation arrow
        # ----------------------------------------------------------------
        self.play(
            missed_peak.animate.set_opacity(1.0),
            missed_valley.animate.set_opacity(1.0),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 1.2))
        self.play(FadeIn(missed_annotation_arrow), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.68))

        # ----------------------------------------------------------------
        # BEAT 6: 10.76 - 11.68 hold left composition
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.92))

        # ----------------------------------------------------------------
        # BEAT 7: 11.68 - 15.10 shift emphasis to right dense panel
        # ----------------------------------------------------------------
        self.play(
            LaggedStart(*[FadeIn(d) for d in right_sample_points], lag_ratio=0.04),
            run_time=max(0.05, 1.2),
        )
        self.play(Create(right_recon), run_time=max(0.05, 0.9))
        self.play(
            FadeIn(right_label),
            right_frame.animate.set_stroke(WHITE, width=2.5),
            left_frame.animate.set_stroke(GREY, width=1.0),
            left_display.animate.set_opacity(0.7),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.52))

        # ----------------------------------------------------------------
        # BEAT 8: 15.10 - 20.98 storage meter filling + dense pulse
        # ----------------------------------------------------------------
        meter_x = 6.0
        meter_center_y = PANEL_Y
        outer_h = 1.3
        meter_bottom_y = meter_center_y - outer_h / 2

        fill_level = ValueTracker(0.15)
        storage_fill = always_redraw(
            lambda: Rectangle(
                width=0.34,
                height=fill_level.get_value(),
                fill_color=ORANGE,
                fill_opacity=1,
                stroke_width=0,
            ).move_to(np.array([meter_x, meter_bottom_y + fill_level.get_value() / 2, 0.0]))
        )
        meter_outer = Rectangle(
            width=0.5,
            height=outer_h,
            color=WHITE,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=0.05,
        ).move_to(np.array([meter_x, meter_center_y, 0.0]))
        storage_label = Text("storage", font_size=16, color=WHITE).next_to(meter_outer, DOWN, buff=0.1)
        storage_meter_group = VGroup(meter_outer, storage_fill, storage_label)

        self.play(FadeIn(storage_meter_group), run_time=max(0.05, 0.5))
        self.play(fill_level.animate.set_value(1.2), run_time=max(0.05, 2.8))
        self.play(Indicate(meter_outer, color=RED, scale_factor=1.2), run_time=max(0.05, 0.5))
        self.play(Indicate(right_sample_points, color=PURPLE, scale_factor=1.05), run_time=max(0.05, 0.7))
        self.play(Indicate(right_recon, color=GREEN, scale_factor=1.03), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.88))

        # ----------------------------------------------------------------
        # BEAT 9: 20.98 - 21.86 hold meter and dense waveform
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.88))

        # ----------------------------------------------------------------
        # BEAT 10: 21.86 - 24.72 sampling-frequency slider
        # ----------------------------------------------------------------
        freq_text = Text("Sampling Frequency", font_size=22, color=WHITE, weight="BOLD")
        design_caption = Text("design consideration", font_size=20, color=YELLOW, weight="BOLD")
        design_box = SurroundingRectangle(design_caption, color=YELLOW, buff=0.10)
        freq_text.move_to(np.array([0, 0.15, 0.0]))
        design_caption.next_to(freq_text, DOWN, buff=0.18)
        design_box.move_to(design_caption)

        down_arrow_freq = Arrow(
            start=freq_text.get_bottom() + DOWN * 0.08,
            end=design_caption.get_top() + UP * 0.08,
            color=WHITE,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.20,
        )
        freq_label_arrow_group = VGroup(freq_text, design_box, design_caption, down_arrow_freq)

        freq_axis = Line(
            start=np.array([-5.6, -0.7, 0.0]),
            end=np.array([5.6, -0.7, 0.0]),
            color=GREY_B,
            stroke_width=2,
        )
        freq_axis_label = Text("sampling frequency", font_size=18, color=GREY).next_to(freq_axis, DOWN, buff=0.12)

        slider = Triangle(color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.15)
        slider.move_to(np.array([-5.6, -0.7, 0.0]))

        self.play(
            FadeIn(freq_label_arrow_group),
            FadeIn(slider),
            run_time=max(0.05, 0.8),
        )
        self.play(
            FadeIn(freq_axis),
            FadeIn(freq_axis_label),
            run_time=max(0.05, 0.7),
        )
        self.play(slider.animate.move_to(np.array([0, -0.7, 0.0])), run_time=max(0.05, 1.36))

        # ----------------------------------------------------------------
        # BEAT 11: 24.72 - 28.80 neural recording schematic + pulse label
        # ----------------------------------------------------------------
        electrode_circle = Circle(
            radius=0.25,
            fill_color=TEAL,
            fill_opacity=0.25,
            stroke_color=TEAL,
            stroke_width=2,
        ).move_to(np.array([-2.5, -1.45, 0.0]))
        electrode_label = Text("electrode", font_size=15, color=TEAL).next_to(electrode_circle, UP, buff=0.08)

        amp_box = Rectangle(
            width=0.9,
            height=0.45,
            fill_color=BLUE,
            fill_opacity=0.25,
            stroke_color=BLUE,
            stroke_width=2,
        ).move_to(np.array([0, -1.45, 0.0]))
        amp_label_text = Text("amp", font_size=15, color=BLUE).move_to(amp_box)

        adc_box = Rectangle(
            width=0.9,
            height=0.45,
            fill_color=ORANGE,
            fill_opacity=0.25,
            stroke_color=ORANGE,
            stroke_width=2,
        ).move_to(np.array([2.5, -1.45, 0.0]))
        adc_label_text = Text("ADC", font_size=15, color=ORANGE).move_to(adc_box)

        line1 = Line(
            start=electrode_circle.get_right() + RIGHT * 0.05,
            end=amp_box.get_left() + LEFT * 0.05,
            color=GREY_B,
            stroke_width=2,
        )
        line2 = Line(
            start=amp_box.get_right() + RIGHT * 0.05,
            end=adc_box.get_left() + LEFT * 0.05,
            color=GREY_B,
            stroke_width=2,
        )

        schematic_group = VGroup(
            electrode_circle, electrode_label,
            amp_box, amp_label_text,
            adc_box, adc_label_text,
            line1, line2,
        )
        schematic_group.set_opacity(0.65)

        self.play(FadeIn(schematic_group), run_time=max(0.05, 1.2))
        self.play(
            Indicate(freq_text, color=YELLOW, scale_factor=1.15),
            Indicate(slider, color=YELLOW, scale_factor=1.15),
            run_time=max(0.05, 0.7),
        )
        self.play(Indicate(freq_axis, color=WHITE, scale_factor=1.0), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.48))

        # ----------------------------------------------------------------
        # BEAT 12: 28.80 - 29.50 hold slider and schematic
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.70))

        # ----------------------------------------------------------------
        # BEAT 13: 29.50 - 31.48 fade frequency UI, show downstream chain
        # ----------------------------------------------------------------
        downstream_phrase = Text(
            "And here's why it matters downstream",
            font_size=24,
            color=WHITE,
            weight="BOLD",
        )
        downstream_phrase.scale_to_fit_width(7.5)
        downstream_phrase.move_to(np.array([0, 3.35, 0.0]))

        filtering_node = make_chain_node("Filtering", GREEN, np.array([0, 0.35, 0.0]))
        spectral_node = make_chain_node("Spectral Analysis", BLUE, np.array([0, -0.60, 0.0]))
        feature_node = make_chain_node("Feature Extraction", PURPLE, np.array([0, -1.55, 0.0]))

        arrow0_1_dim = Arrow(
            start=filtering_node.get_bottom() + DOWN * 0.06,
            end=spectral_node.get_top() + UP * 0.06,
            color=GREY,
            stroke_width=2.5,
            buff=0.05,
        )
        arrow1_2_dim = Arrow(
            start=spectral_node.get_bottom() + DOWN * 0.06,
            end=feature_node.get_top() + UP * 0.06,
            color=GREY,
            stroke_width=2.5,
            buff=0.05,
        )

        for node, arrw in [
            (filtering_node, arrow0_1_dim),
            (spectral_node, arrow1_2_dim),
            (feature_node, arrow0_1_dim),
        ]:
            pass

        filtering_node.set_opacity(0.25)
        spectral_node.set_opacity(0.25)
        feature_node.set_opacity(0.25)
        arrow0_1_dim.set_opacity(0.25)
        arrow1_2_dim.set_opacity(0.25)

        chain_group_faint = VGroup(
            filtering_node, spectral_node, feature_node,
            arrow0_1_dim, arrow1_2_dim,
        )

        self.play(
            FadeOut(schematic_group),
            FadeOut(slider),
            FadeOut(freq_axis),
            FadeOut(freq_axis_label),
            FadeOut(freq_label_arrow_group),
            FadeIn(downstream_phrase),
            FadeIn(chain_group_faint),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.78))

        # ----------------------------------------------------------------
        # BEAT 14: 31.48 - 34.70 brighten Filtering + draw quality arrow
        # ----------------------------------------------------------------
        down_arrow_quality = Arrow(
            start=left_frame.get_bottom() + DOWN * 0.10,
            end=filtering_node.get_top() + UP * 0.05,
            color=YELLOW,
            stroke_width=6,
            buff=0.10,
            max_tip_length_to_length_ratio=0.18,
        )

        self.play(
            filtering_node.animate.set_opacity(1.0),
            filtering_node[0].animate.set_fill(GREEN, opacity=0.85),
            run_time=max(0.05, 0.7),
        )
        self.play(Create(down_arrow_quality), run_time=max(0.05, 1.0))
        self.play(Indicate(down_arrow_quality, color=YELLOW, scale_factor=1.0), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.92))

        # ----------------------------------------------------------------
        # BEAT 15: 34.70 - 36.40 Spectral Analysis
        # ----------------------------------------------------------------
        arrow_hl_1_2 = Arrow(
            start=filtering_node.get_bottom() + DOWN * 0.06,
            end=spectral_node.get_top() + UP * 0.06,
            color=YELLOW,
            stroke_width=4,
            buff=0.05,
        )
        self.play(
            spectral_node.animate.set_opacity(1.0),
            spectral_node[0].animate.set_fill(BLUE, opacity=0.85),
            filtering_node.animate.set_opacity(0.6),
            run_time=max(0.05, 0.7),
        )
        self.play(Create(arrow_hl_1_2), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.4))

        # ----------------------------------------------------------------
        # BEAT 16: 36.40 - 37.94 Feature Extraction
        # ----------------------------------------------------------------
        arrow_hl_2_3 = Arrow(
            start=spectral_node.get_bottom() + DOWN * 0.06,
            end=feature_node.get_top() + UP * 0.06,
            color=YELLOW,
            stroke_width=4,
            buff=0.05,
        )
        self.play(
            feature_node.animate.set_opacity(1.0),
            feature_node[0].animate.set_fill(PURPLE, opacity=0.85),
            spectral_node.animate.set_opacity(0.6),
            run_time=max(0.05, 0.7),
        )
        self.play(Create(arrow_hl_2_3), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.24))

        # ----------------------------------------------------------------
        # BEAT 17: 37.94 - 42.44 add dependency label + flash sampling quality
        # ----------------------------------------------------------------
        depends_on_label = Text("depends on", font_size=20, color=YELLOW, weight="BOLD")
        depends_on_label.move_to(down_arrow_quality.get_center() + np.array([1.0, 0.4, 0.0]))

        self.play(FadeIn(depends_on_label), run_time=max(0.05, 1.0))
        self.play(Indicate(down_arrow_quality, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.8))
        self.play(
            Indicate(left_recon, color=ORANGE, scale_factor=1.1),
            Indicate(left_sample_points, color=TEAL, scale_factor=1.1),
            run_time=max(0.05, 0.8),
        )
        self.play(down_arrow_quality.animate.set_stroke(YELLOW, width=8), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.3))

        # ----------------------------------------------------------------
        # BEAT 18: 42.44 - 43.32 hold full chain + dependency arrow
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.88))

        # ----------------------------------------------------------------
        # BEAT 19: 43.32 - 47.34 warning + corrected output node
        # ----------------------------------------------------------------
        warning_text = Text(
            "Poor digitisation cannot be fully corrected later.",
            font_size=24,
            color=RED,
            weight="BOLD",
        )
        warning_text.scale_to_fit_width(10)
        warning_text.move_to(np.array([0, -3.30, 0.0]))

        corrected_node = make_chain_node("Corrected Output", GREY, np.array([0, -2.45, 0.0]))
        corrected_node.set_opacity(0.35)

        corrective_arrow = Arrow(
            start=feature_node.get_bottom() + DOWN * 0.06,
            end=corrected_node.get_top() + UP * 0.06,
            color=RED,
            stroke_width=4,
            buff=0.05,
        )
        corrective_arrow.set_opacity(0.4)

        self.play(
            FadeIn(warning_text),
            FadeIn(corrected_node),
            FadeIn(corrective_arrow),
            run_time=max(0.05, 0.8),
        )
        self.play(
            left_wave.animate.set_color(RED).set_opacity(0.8),
            left_recon.animate.set_color(RED).set_opacity(0.9),
            run_time=max(0.05, 0.8),
        )
        self.play(Indicate(corrected_node, color=GREY, scale_factor=1.0), run_time=max(0.05, 0.5))
        self.play(Indicate(warning_text, color=RED, scale_factor=1.05), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.32))

        # ----------------------------------------------------------------
        # BEAT 20: 47.34 - 48.25 hold final composition
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.91))