ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Layout constants
        # ------------------------------------------------------------
        base_y = 0.0
        left_x = -6.0
        right_x = 6.0
        b10_x = -2.0
        b20_x = 2.0
        b30_x = 6.0
        seg_centers = [-4.0, 0.0, 4.0]
        seg_label_y = -1.45
        sub_label_y = 1.50
        eye_closed_y = 1.00
        caption_y = -2.10
        n_pts = 300

        # ------------------------------------------------------------
        # Baseline
        # ------------------------------------------------------------
        baseline = Line(
            np.array([left_x, base_y, 0]),
            np.array([right_x, base_y, 0]),
            color=GREY_B,
            stroke_width=2,
        )
        baseline.set_z_index(0)

        # ------------------------------------------------------------
        # Global caption under the whole recording
        # ------------------------------------------------------------
        caption = Text("30 s", font_size=26, color=WHITE)
        caption.move_to(np.array([0, caption_y, 0]))
        full_caption = Text("30-second EEG recording", font_size=26, color=WHITE)
        full_caption.move_to(np.array([0, caption_y, 0]))

        # ------------------------------------------------------------
        # Waveform helper and segment definitions
        # ------------------------------------------------------------
        def make_segment(x0, x1, y_func, color=TEAL, stroke_w=3):
            xs = np.linspace(x0, x1, n_pts)
            ys = y_func(xs)
            pts = np.array([xs, ys, np.zeros_like(xs)]).T
            mob = VMobject(
                stroke_color=color,
                stroke_width=stroke_w,
                stroke_opacity=1.0,
            )
            mob.set_points_as_corners(pts)
            mob.set_z_index(2)
            return mob

        # Initial full alpha waveform (all three segments continue alpha pattern)
        def alpha_y(x):
            t = (x + 6.0) / 12.0
            return 0.72 * np.sin(2 * np.pi * 15 * t)

        def mid_reduced_y(x):
            t = (x + 2.0) / 4.0
            return (
                0.17 * np.sin(2 * np.pi * 5 * t)
                + 0.07 * np.sin(2 * np.pi * 11 * t)
                + 0.04 * np.sin(2 * np.pi * 17 * t)
                + 0.045 * np.sin(2 * np.pi * 23 * t)
            )

        def right_reduced_y(x):
            t = (x - 2.0) / 4.0
            return (
                0.16 * np.sin(2 * np.pi * 5 * t)
                + 0.06 * np.sin(2 * np.pi * 11 * t)
                + 0.04 * np.sin(2 * np.pi * 17 * t)
            )

        def right_transient_y(x):
            base = right_reduced_y(x)
            transient = 0.85 * np.exp(-((x - 2.35) / 0.10) ** 2)
            return base + transient

        # Left final segment = initial alpha segment
        left_wave = make_segment(left_x, b10_x, alpha_y)
        # Initial middle/right alpha continuations
        initial_mid_wave = make_segment(b10_x, b20_x, alpha_y)
        initial_right_wave = make_segment(b20_x, b30_x, alpha_y)
        # Final middle and right segments (right starts without the transient)
        mid_wave_final = make_segment(b10_x, b20_x, mid_reduced_y)
        right_wave_no_transient = make_segment(b20_x, b30_x, right_reduced_y)
        right_wave_with_transient = make_segment(b20_x, b30_x, right_transient_y)

        # Convenience references that later stay pointed at the visible objects
        wave_left = left_wave
        wave_mid = initial_mid_wave
        wave_right = initial_right_wave

        # ------------------------------------------------------------
        # Vertical dashed boundaries at 10, 20, and 30 seconds
        # ------------------------------------------------------------
        def make_boundary(x):
            return DashedLine(
                np.array([x, -1.35, 0]),
                np.array([x, 1.35, 0]),
                dash_length=0.14,
                dashed_ratio=0.6,
                color=GREY_B,
                stroke_width=2,
            ).set_z_index(3)

        b1 = make_boundary(b10_x)
        b2 = make_boundary(b20_x)
        b3 = make_boundary(b30_x)

        # ------------------------------------------------------------
        # Segment labels below baseline
        # ------------------------------------------------------------
        seg1_label = Text("Eyes closed (0–10 s)", font_size=22, color=WHITE)
        seg1_label.move_to(np.array([seg_centers[0], seg_label_y, 0]))
        seg2_label = Text("Eyes open (10–20 s)", font_size=22, color=WHITE)
        seg2_label.move_to(np.array([seg_centers[1], seg_label_y, 0]))
        seg3_label = Text("Stimulus (20–30 s)", font_size=22, color=WHITE)
        seg3_label.move_to(np.array([seg_centers[2], seg_label_y, 0]))
        seg_labels = VGroup(seg1_label, seg2_label, seg3_label)
        seg_labels.set_z_index(4)

        # ------------------------------------------------------------
        # Highlight rectangles for each segment
        # ------------------------------------------------------------
        def make_highlight(cx):
            return RoundedRectangle(
                width=3.75,
                height=2.00,
                corner_radius=0.15,
                fill_color=YELLOW,
                fill_opacity=0.0,
                stroke_color=YELLOW,
                stroke_opacity=0.0,
                stroke_width=2,
            ).move_to(np.array([cx, 0, 0]))

        h1 = make_highlight(seg_centers[0])
        h2 = make_highlight(seg_centers[1])
        h3 = make_highlight(seg_centers[2])
        h1.set_z_index(1)
        h2.set_z_index(1)
        h3.set_z_index(1)

        # ------------------------------------------------------------
        # Sub-labels above segments
        # ------------------------------------------------------------
        eye_closed_caption = Text("Eyes closed", font_size=22, color=WHITE)
        eye_closed_caption.move_to(np.array([seg_centers[0], eye_closed_y, 0]))

        alpha_prominent_label = Text("Alpha prominent", font_size=22, color=YELLOW)
        alpha_prominent_label.move_to(np.array([seg_centers[0], sub_label_y, 0]))

        alpha_decrease_label = Text("Alpha decreases", font_size=22, color=YELLOW)
        alpha_decrease_label.move_to(np.array([seg_centers[1], sub_label_y, 0]))

        event_response_label = Text("Event-related response", font_size=22, color=YELLOW)
        event_response_label.move_to(np.array([2.75, sub_label_y, 0]))

        sub_labels = VGroup(
            alpha_prominent_label,
            alpha_decrease_label,
            event_response_label,
        )
        sub_labels.set_z_index(4)
        eye_closed_caption.set_z_index(4)

        # ------------------------------------------------------------
        # Region outlines for the three distinct frequency-content regions
        # ------------------------------------------------------------
        def make_region_outline(cx):
            return RoundedRectangle(
                width=3.75,
                height=1.90,
                corner_radius=0.10,
                fill_opacity=0.0,
                stroke_color=ORANGE,
                stroke_opacity=0.0,
                stroke_width=2.5,
            ).move_to(np.array([cx, 0, 0]))

        region_outline_left = make_region_outline(seg_centers[0])
        region_outline_mid = make_region_outline(seg_centers[1])
        region_outline_right = make_region_outline(seg_centers[2])
        region_outlines = VGroup(
            region_outline_left,
            region_outline_mid,
            region_outline_right,
        )
        region_outlines.set_z_index(5)

        # ------------------------------------------------------------
        # Sweeping highlight for the continuous-evolution beat
        # ------------------------------------------------------------
        sweep_rect = Rectangle(
            width=0.35,
            height=2.00,
            fill_color=YELLOW,
            fill_opacity=0.35,
            stroke_opacity=0.0,
        )
        sweep_rect.move_to(np.array([-6.4, 0, 0]))
        sweep_rect.set_z_index(6)
        sweep_rect.set_opacity(0.0)
        self.add(sweep_rect)

        # ============================================================
        # Beat 1: 0.00-1.22 blank screen
        # ============================================================
        self.wait(max(0.05, 1.22))

        # ============================================================
        # Beat 2: 1.22-1.60 baseline fades in
        # ============================================================
        self.play(FadeIn(baseline), run_time=max(0.05, 0.38))

        # ============================================================
        # Beat 3: 1.60-2.20 "30 s" label fades in
        # ============================================================
        self.play(FadeIn(caption), run_time=max(0.05, 0.60))

        # ============================================================
        # Beat 4: 2.20-3.24 full phrase + waveform starts drawing
        # ============================================================
        self.play(
            Transform(caption, full_caption),
            LaggedStart(
                Create(left_wave),
                Create(initial_mid_wave),
                Create(initial_right_wave),
                lag_ratio=0.5,
            ),
            run_time=max(0.05, 1.04),
        )

        # ============================================================
        # Beat 5: 3.24-4.32 first 10 s drawn, 10 s boundary + label
        # ============================================================
        self.play(
            FadeIn(b1),
            FadeIn(seg1_label),
            run_time=max(0.05, 1.08),
        )

        # ============================================================
        # Beat 6: 4.32-4.84 first label brightens, first highlight appears
        # ============================================================
        self.play(
            seg1_label.animate.set_color(YELLOW),
            h1.animate.set_fill(opacity=0.20).set_stroke(opacity=0.60),
            run_time=max(0.05, 0.52),
        )

        # ============================================================
        # Beat 7: 4.84-5.54 hold
        # ============================================================
        self.wait(max(0.05, 0.70))

        # ============================================================
        # Beat 8: 5.54-7.42 "Eyes closed" caption appears above first segment
        # ============================================================
        self.play(FadeIn(eye_closed_caption), run_time=max(0.05, 1.88))

        # ============================================================
        # Beat 9: 7.42-8.38 pause
        # ============================================================
        self.wait(max(0.05, 0.96))

        # ============================================================
        # Beat 10: 8.38-9.82 "Alpha prominent" label + alpha emphasis
        # ============================================================
        self.play(
            FadeIn(alpha_prominent_label),
            left_wave.animate.set_stroke(color=YELLOW, width=5),
            h1.animate.set_fill(opacity=0.25).set_stroke(opacity=0.70),
            run_time=max(0.05, 1.44),
        )

        # ============================================================
        # Beat 11: 9.82-10.70 brief pause
        # ============================================================
        self.wait(max(0.05, 0.88))

        # ============================================================
        # Beat 12: 10.70-11.70 10 s boundary pulses, first highlight dims
        # ============================================================
        self.play(
            b1.animate.set_stroke(color=WHITE, width=4),
            rate_func=there_and_back,
            run_time=max(0.05, 0.60),
        )
        self.play(
            h1.animate.set_fill(opacity=0.12).set_stroke(opacity=0.30),
            run_time=max(0.05, 0.40),
        )

        # ============================================================
        # Beat 13: 11.70-13.32 waveform changes, 20 s boundary + label,
        #           highlight slides to middle
        # ============================================================
        self.play(
            Transform(wave_mid, mid_wave_final),
            Transform(wave_right, right_wave_no_transient),
            FadeIn(b2),
            FadeIn(seg2_label),
            h2.animate.set_fill(opacity=0.20).set_stroke(opacity=0.60),
            h1.animate.set_fill(opacity=0.05).set_stroke(opacity=0.10),
            run_time=max(0.05, 1.62),
        )

        # ============================================================
        # Beat 14: 13.32-13.70 middle highlight active, brief hold
        # ============================================================
        self.wait(max(0.05, 0.38))

        # ============================================================
        # Beat 15: 13.70-14.88 "Alpha decreases" label fades in
        # ============================================================
        self.play(GrowFromCenter(alpha_decrease_label), run_time=max(0.05, 1.18))

        # ============================================================
        # Beat 16: 14.88-15.92 pause
        # ============================================================
        self.wait(max(0.05, 1.04))

        # ============================================================
        # Beat 17: 15.92-16.90 20 s boundary pulses, 30 s boundary fades in
        # ============================================================
        self.play(
            b2.animate.set_stroke(color=WHITE, width=4),
            rate_func=there_and_back,
            run_time=max(0.05, 0.60),
        )
        self.play(
            FadeIn(b3),
            h2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.10),
            run_time=max(0.05, 0.38),
        )

        # ============================================================
        # Beat 18: 16.90-18.90 third label + highlight slides to third
        # ============================================================
        self.play(
            FadeIn(seg3_label),
            h3.animate.set_fill(opacity=0.20).set_stroke(opacity=0.60),
            h2.animate.set_fill(opacity=0.02).set_stroke(opacity=0.08),
            run_time=max(0.05, 2.00),
        )

        # ============================================================
        # Beat 19: 18.90-20.92 transient deflection + label
        # ============================================================
        self.play(
            Transform(wave_right, right_wave_with_transient),
            FadeIn(event_response_label),
            run_time=max(0.05, 2.02),
        )

        # ============================================================
        # Beat 20: 20.92-21.76 first two segments dimmed
        # ============================================================
        self.play(
            seg1_label.animate.set_color(GREY_B),
            seg2_label.animate.set_color(GREY_B),
            alpha_prominent_label.animate.set_color(GREY_B),
            alpha_decrease_label.animate.set_color(GREY_B),
            eye_closed_caption.animate.set_color(GREY_B),
            h1.animate.set_fill(opacity=0.03).set_stroke(opacity=0.10),
            h2.animate.set_fill(opacity=0.03).set_stroke(opacity=0.10),
            h3.animate.set_fill(opacity=0.20).set_stroke(opacity=0.55),
            run_time=max(0.05, 0.84),
        )

        # ============================================================
        # Beat 21: 21.76-23.72 full display pause
        # ============================================================
        self.wait(max(0.05, 1.96))

        # ============================================================
        # Beat 22: 23.72-24.82 boundaries fade, all highlights equal low
        # ============================================================
        self.play(
            b1.animate.set_stroke(opacity=0.30).set_color(GREY_B),
            b2.animate.set_stroke(opacity=0.30).set_color(GREY_B),
            b3.animate.set_stroke(opacity=0.30).set_color(GREY_B),
            h1.animate.set_fill(opacity=0.08).set_stroke(opacity=0.20),
            h2.animate.set_fill(opacity=0.08).set_stroke(opacity=0.20),
            h3.animate.set_fill(opacity=0.08).set_stroke(opacity=0.20),
            run_time=max(0.05, 1.10),
        )

        # ============================================================
        # Beat 23: 24.82-26.98 sub-labels brighten, region outlines appear
        # ============================================================
        self.play(
            alpha_prominent_label.animate.set_color(YELLOW).scale(1.06),
            alpha_decrease_label.animate.set_color(YELLOW).scale(1.06),
            event_response_label.animate.set_color(YELLOW).scale(1.06),
            region_outlines.animate.set_stroke(opacity=0.60, color=ORANGE),
            run_time=max(0.05, 2.16),
        )

        # ============================================================
        # Beat 24: 26.98-28.08 region outlines glow gently
        # ============================================================
        self.play(
            region_outlines.animate.set_stroke(opacity=0.85, width=3.0),
            rate_func=there_and_back,
            run_time=max(0.05, 1.10),
        )

        # ============================================================
        # Beat 25: 28.08-28.96 baseline + waveform brighten, highlights fade out
        # ============================================================
        self.play(
            baseline.animate.set_stroke(color=WHITE, width=3),
            wave_left.animate.set_stroke(color=WHITE, width=4),
            wave_mid.animate.set_stroke(color=WHITE, width=4),
            wave_right.animate.set_stroke(color=WHITE, width=4),
            h1.animate.set_fill(opacity=0.0).set_stroke(opacity=0.0),
            h2.animate.set_fill(opacity=0.0).set_stroke(opacity=0.0),
            h3.animate.set_fill(opacity=0.0).set_stroke(opacity=0.0),
            run_time=max(0.05, 0.88),
        )

        # ============================================================
        # Beat 26: 28.96-30.40 sweeping highlight travels left to right
        # ============================================================
        self.play(
            sweep_rect.animate.set_opacity(1.0).move_to(np.array([6.4, 0, 0])),
            run_time=max(0.05, 1.44),
            rate_func=linear,
        )

        # ============================================================
        # Beat 27: 30.40-31.86 sweep completes and fades out, brief pause
        # ============================================================
        self.play(sweep_rect.animate.set_opacity(0.0), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 1.16))

        # ============================================================
        # Beat 28: 31.86-33.40 sequential waveform-region pulses
        # ============================================================
        per_pulse = 0.51
        for wave_region in [wave_left, wave_mid, wave_right]:
            self.play(
                wave_region.animate.set_stroke(color=YELLOW, width=6),
                rate_func=there_and_back,
                run_time=max(0.05, per_pulse),
            )
        self.wait(max(0.01, 1.54 - 3 * per_pulse))

        # ============================================================
        # Beat 29: 33.40-34.52 full display hold
        # ============================================================
        self.wait(max(0.05, 1.12))

        # ============================================================
        # Beat 30: 34.52-35.23 final hold
        # ============================================================
        self.wait(max(0.05, 0.71))