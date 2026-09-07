ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene9(Scene):
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
        n_pts = 300

        # ------------------------------------------------
        # Waveform helper and segments
        # ------------------------------------------------
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

        baseline = Line(
            np.array([left_x, base_y, 0]),
            np.array([right_x, base_y, 0]),
            color=GREY_B,
            stroke_width=2,
        )
        baseline.set_z_index(0)

        left_wave = make_segment(left_x, b10_x, alpha_y, color=TEAL)
        mid_wave = make_segment(b10_x, b20_x, mid_reduced_y, color=TEAL)
        right_wave = make_segment(b20_x, b30_x, right_transient_y, color=TEAL)

        # Boundaries
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

        # Segment labels
        left_label = Text("Eyes closed (0–10 s)", font_size=22, color=WHITE)
        left_label.move_to(np.array([seg_centers[0], seg_label_y, 0]))
        mid_label = Text("Eyes open (10–20 s)", font_size=22, color=WHITE)
        mid_label.move_to(np.array([seg_centers[1], seg_label_y, 0]))
        right_label = Text("Stimulus (20–30 s)", font_size=22, color=WHITE)
        right_label.move_to(np.array([seg_centers[2], seg_label_y, 0]))
        labels_initial = VGroup(left_label, mid_label, right_label)
        labels_initial.set_z_index(4)

        # Sub-labels above the waveform
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

        # Left-segment highlight rectangle
        h_left_rect = RoundedRectangle(
            width=3.75,
            height=2.00,
            corner_radius=0.15,
            fill_color=YELLOW,
            fill_opacity=0.0,
            stroke_color=YELLOW,
            stroke_opacity=0.0,
            stroke_width=3,
        )
        h_left_rect.move_to(np.array([seg_centers[0], 0, 0]))
        h_left_rect.set_z_index(1)

        # Core waveform group to shift upward when lower panel arrives
        wave_core = VGroup(
            baseline,
            left_wave,
            mid_wave,
            right_wave,
            b1,
            b2,
            b3,
            h_left_rect,
        )
        wave_core.set_z_index(5)

        # Full-screen dark overlay for skeptical beats
        dark_overlay = Rectangle(
            width=16,
            height=9,
            fill_color=BLACK,
            fill_opacity=0.0,
            stroke_width=0,
        )
        dark_overlay.set_z_index(100)
        dark_overlay.move_to(ORIGIN)

        # Initial add
        self.add(wave_core, labels_initial, sub_labels, dark_overlay)

        # ------------------------------------------------------------
        # Beat 1: 0.00-1.84
        # ------------------------------------------------------------
        self.play(FadeOut(sub_labels), run_time=max(0.05, 1.84))

        # ------------------------------------------------------------
        # Beat 2: 1.84-2.48 subtle darkening
        # ------------------------------------------------------------
        self.play(dark_overlay.animate.set_fill(opacity=0.28), run_time=max(0.05, 0.64))

        # ------------------------------------------------------------
        # Beat 3: 2.48-3.40 brighten and emphasize left third
        # ------------------------------------------------------------
        self.play(
            dark_overlay.animate.set_fill(opacity=0.0),
            left_wave.animate.set_stroke(color=YELLOW, width=5),
            mid_wave.animate.set_stroke(color=TEAL).set_opacity(0.45),
            right_wave.animate.set_stroke(color=TEAL).set_opacity(0.45),
            mid_label.animate.set_opacity(0.45),
            right_label.animate.set_opacity(0.45),
            run_time=max(0.05, 0.92),
        )

        # ------------------------------------------------------------
        # Beat 4: 3.40-4.58 only first segment full contrast
        # ------------------------------------------------------------
        self.play(
            mid_wave.animate.set_stroke(color=GREY_B).set_opacity(0.28),
            right_wave.animate.set_stroke(color=GREY_B).set_opacity(0.28),
            mid_label.animate.set_opacity(0.25),
            right_label.animate.set_opacity(0.25),
            h_left_rect.animate.set_stroke(opacity=0.70),
            left_label.animate.set_color(YELLOW).set_opacity(1.0),
            run_time=max(0.05, 1.18),
        )

        # ------------------------------------------------------------
        # Beat 5: 4.58-6.00 label changes to Neural signal
        # ------------------------------------------------------------
        neural_signal_label = Text("Neural signal", font_size=22, color=YELLOW)
        neural_signal_label.move_to(left_label.get_center())
        self.play(Transform(left_label, neural_signal_label), run_time=max(0.05, 1.42))

        # ------------------------------------------------------------
        # Beat 6: 6.00-6.92 green check mark fades in
        # ------------------------------------------------------------
        check_mark = SVGMobject(ASSET_PATHS["check_circle"], color=GREEN, fill_opacity=1)
        check_mark.scale(0.45)
        check_mark.move_to(np.array([-4.0, 1.45, 0]))
        self.play(FadeIn(check_mark), run_time=max(0.05, 0.92))

        # ------------------------------------------------------------
        # Beat 7: 6.92-7.90 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.98))

        # ------------------------------------------------------------
        # Beat 8: 7.90-8.62 check vanishes, darkening, highlight flicker
        # ------------------------------------------------------------
        self.play(FadeOut(check_mark), run_time=max(0.05, 0.15))
        self.play(dark_overlay.animate.set_fill(opacity=0.32), run_time=max(0.05, 0.20))
        self.play(Indicate(h_left_rect, color=YELLOW, scale_factor=1.05), run_time=max(0.05, 0.37))

        # ------------------------------------------------------------
        # Beat 9: 8.62-10.14 Classical frequency analysis label
        # ------------------------------------------------------------
        classical_title = Text("Classical frequency analysis", font_size=30, color=WHITE)
        classical_title.move_to(np.array([0, 2.0, 0]))
        self.play(
            FadeIn(classical_title),
            FadeOut(left_label),
            FadeOut(mid_label),
            FadeOut(right_label),
            h_left_rect.animate.set_stroke(opacity=0.0),
            dark_overlay.animate.set_fill(opacity=0.0),
            left_wave.animate.set_stroke(color=WHITE, width=3).set_opacity(0.65),
            mid_wave.animate.set_stroke(color=WHITE, width=3).set_opacity(0.65),
            right_wave.animate.set_stroke(color=WHITE, width=3).set_opacity(0.65),
            run_time=max(0.05, 1.52),
        )

        # ------------------------------------------------------------
        # Beat 10: 10.14-11.30 add assume
        # ------------------------------------------------------------
        classical_assume = Text(
            "Classical frequency analysis — assume",
            font_size=28,
            color=WHITE,
            t2c={"assume": YELLOW},
            slant=ITALIC,
        )
        classical_assume.move_to(np.array([0, 2.0, 0]))
        self.play(Transform(classical_title, classical_assume), run_time=max(0.05, 1.16))

        # ------------------------------------------------------------
        # Beat 11: 11.30-12.16 Signal remains unchanged
        # ------------------------------------------------------------
        signal_unchanged_label = Text(
            "Signal remains unchanged",
            font_size=28,
            color=WHITE,
            t2c={"signal": YELLOW},
        )
        signal_unchanged_label.move_to(np.array([0, 2.0, 0]))
        self.play(Transform(classical_title, signal_unchanged_label), run_time=max(0.05, 0.86))

        # ------------------------------------------------------------
        # Beat 12: 12.16-13.16 frozen hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.00))

        # ------------------------------------------------------------
        # Beat 13: 13.16-14.94 observation period banner slides in
        # ------------------------------------------------------------
        obs_banner = VGroup(
            Rectangle(
                width=12.5,
                height=0.7,
                fill_color=BLUE,
                fill_opacity=0.30,
                stroke_color=BLUE,
                stroke_opacity=0.80,
                stroke_width=2,
            ),
            Text("Observation period", font_size=22, color=WHITE),
        )
        obs_banner.arrange(ORIGIN, buff=0.0)
        obs_banner.move_to(np.array([-13.5, -1.80, 0]))
        self.add(obs_banner)
        self.play(
            obs_banner.animate.move_to(np.array([0, -1.80, 0])),
            run_time=max(0.05, 1.78),
        )

        # ------------------------------------------------------------
        # Beat 14: 14.94-15.62 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.68))

        # ------------------------------------------------------------
        # Beat 15: 15.62-17.32 unfreeze and fade banner/label
        # ------------------------------------------------------------
        self.play(
            FadeOut(obs_banner),
            FadeOut(classical_title),
            run_time=max(0.05, 0.70),
        )
        self.play(
            left_wave.animate.set_stroke(color=YELLOW, width=5).set_opacity(1.0),
            mid_wave.animate.set_stroke(color=TEAL, width=3).set_opacity(1.0),
            right_wave.animate.set_stroke(color=TEAL, width=3).set_opacity(1.0),
            rate_func=there_and_back,
            run_time=max(0.05, 0.50),
        )
        self.play(
            left_wave.animate.set_stroke(color=TEAL, width=3),
            run_time=max(0.05, 0.50),
        )

        # ------------------------------------------------------------
        # Beat 16: 17.32-18.72 segment labels reappear
        # ------------------------------------------------------------
        left_seg_label = Text("Eyes closed (0–10 s)", font_size=22, color=WHITE)
        left_seg_label.move_to(np.array([seg_centers[0], seg_label_y, 0]))
        mid_seg_label = Text("Eyes open (10–20 s)", font_size=22, color=WHITE)
        mid_seg_label.move_to(np.array([seg_centers[1], seg_label_y, 0]))
        right_seg_label = Text("Stimulus (20–30 s)", font_size=22, color=WHITE)
        right_seg_label.move_to(np.array([seg_centers[2], seg_label_y, 0]))
        segment_labels_visible = VGroup(left_seg_label, mid_seg_label, right_seg_label)
        segment_labels_visible.set_z_index(4)
        self.add(segment_labels_visible)
        self.play(FadeIn(segment_labels_visible), run_time=max(0.05, 1.40))

        # ------------------------------------------------------------
        # Beat 17: 18.72-20.36 shift waveform up, introduce spectrum axes
        # ------------------------------------------------------------
        spectrum_center = np.array([0, -1.95, 0])
        x_len = 7.0
        y_len = 1.6
        x_arrow = Arrow(
            spectrum_center + LEFT * (x_len / 2),
            spectrum_center + RIGHT * (x_len / 2),
            buff=0,
            color=GREY_B,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.06,
        )
        y_arrow = Arrow(
            spectrum_center + DOWN * (y_len / 2),
            spectrum_center + UP * (y_len / 2),
            buff=0,
            color=GREY_B,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.08,
        )
        spectrum_axes = VGroup(x_arrow, y_arrow)
        spectrum_axes.set_z_index(6)

        single_spectrum_title = Text("Single frequency spectrum", font_size=30, color=WHITE)
        single_spectrum_title.move_to(np.array([0, 3.0, 0]))

        self.play(
            wave_core.animate.shift(UP * 1.0),
            segment_labels_visible.animate.shift(UP * 1.0),
            FadeIn(single_spectrum_title),
            FadeIn(spectrum_axes),
            run_time=max(0.05, 1.64),
        )

        # ------------------------------------------------------------
        # Helper mapping for spectrum curve
        # ------------------------------------------------------------
        def freq_to_x(freq):
            return spectrum_center[0] - x_len / 2 + (freq / 30.0) * x_len

        def amp_to_y(amp):
            return (spectrum_center[1] - y_len / 2) + amp * y_len

        freqs = np.linspace(0, 30, 400)
        amps = 0.85 * np.exp(-((freqs - 10) / 1.4) ** 2) + 0.05
        curve_pts = np.array(
            [freq_to_x(freqs), amp_to_y(amps), np.zeros_like(freqs)]
        ).T
        spectrum_curve = VMobject(
            fill_color=YELLOW,
            fill_opacity=0.0,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        spectrum_curve.set_points_as_corners(curve_pts)
        spectrum_curve.set_z_index(6)

        # ------------------------------------------------------------
        # Beat 18: 20.36-21.56 draw spectrum curve
        # ------------------------------------------------------------
        self.play(Create(spectrum_curve, rate_func=linear), run_time=max(0.05, 1.20))

        # ------------------------------------------------------------
        # Beat 19: 21.56-23.04 solidify curve, overall average label
        # ------------------------------------------------------------
        overall_avg_label = Text("Overall average", font_size=24, color=GREY_B)
        overall_avg_label.move_to(np.array([0, -3.15, 0]))
        self.play(
            spectrum_curve.animate.set_fill(opacity=0.35).set_stroke(color=YELLOW, width=4),
            FadeIn(overall_avg_label),
            run_time=max(0.05, 1.48),
        )

        # ------------------------------------------------------------
        # Beat 20: 23.04-23.60 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.56))

        # ------------------------------------------------------------
        # Beat 21: 23.60-25.42 only flashes
        # ------------------------------------------------------------
        only_word = Text("only", font_size=28, color=YELLOW)
        only_word.move_to(np.array([0, -0.85, 0]))
        self.play(FadeIn(only_word), run_time=max(0.05, 0.50))
        self.play(FadeOut(only_word), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------
        # Beat 22: 25.42-26.32 spectrum dims, question mark appears
        # ------------------------------------------------------------
        question_mark = Text("?", font_size=52, color=WHITE, fill_opacity=0.4)
        question_mark.move_to(np.array([-0.35, 0.15, 0]))
        self.play(
            spectrum_axes.animate.set_opacity(0.60),
            spectrum_curve.animate.set_opacity(0.60),
            FadeIn(question_mark),
            run_time=max(0.05, 0.90),
        )

        # ------------------------------------------------------------
        # Beat 23: 26.32-27.36 question mark bobs
        # ------------------------------------------------------------
        self.play(
            question_mark.animate.scale(1.25),
            rate_func=there_and_back,
            run_time=max(0.05, 1.04),
        )

        # ------------------------------------------------------------
        # Beat 24: 27.36-28.28 faint dashed time-search line
        # ------------------------------------------------------------
        failed_line = DashedLine(
            question_mark.get_left() + LEFT * 0.2,
            question_mark.get_left() + LEFT * 3.2,
            dash_length=0.10,
            dashed_ratio=0.6,
            color=GREY_B,
            stroke_width=2,
        )
        self.play(FadeIn(failed_line), run_time=max(0.05, 0.35))
        self.play(FadeOut(failed_line), run_time=max(0.05, 0.57))

        # ------------------------------------------------------------
        # Beat 25: 28.28-28.94 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.66))

        # ------------------------------------------------------------
        # Beat 26: 28.94-29.52 spectrum dims further
        # ------------------------------------------------------------
        self.play(
            spectrum_axes.animate.set_opacity(0.40),
            spectrum_curve.animate.set_opacity(0.40),
            run_time=max(0.05, 0.58),
        )

        # ------------------------------------------------------------
        # Beat 27: 29.52-31.08 left alpha present label and glow
        # ------------------------------------------------------------
        alpha_present_label = Text("Alpha present (0–10 s)", font_size=22, color=YELLOW)
        alpha_present_label.move_to(left_seg_label.get_center())
        self.play(
            Transform(left_seg_label, alpha_present_label),
            left_wave.animate.set_stroke(color=YELLOW, width=5).set_opacity(1.0),
            mid_wave.animate.set_stroke(color=GREY_B, width=3).set_opacity(0.25),
            right_wave.animate.set_stroke(color=GREY_B, width=3).set_opacity(0.25),
            mid_seg_label.animate.set_opacity(0.30),
            right_seg_label.animate.set_opacity(0.30),
            h_left_rect.animate.set_fill(opacity=0.25).set_stroke(opacity=0.75),
            run_time=max(0.05, 1.56),
        )

        # ------------------------------------------------------------
        # Beat 28: 31.08-32.24 dim other labels and segments
        # ------------------------------------------------------------
        self.play(
            mid_seg_label.animate.set_opacity(0.05),
            right_seg_label.animate.set_opacity(0.05),
            mid_wave.animate.set_opacity(0.15),
            right_wave.animate.set_opacity(0.15),
            run_time=max(0.05, 1.16),
        )

        # ------------------------------------------------------------
        # Beat 29: 32.24-32.86 label pulse and 10 s boundary pulse
        # ------------------------------------------------------------
        self.play(
            alpha_present_label.animate.scale(1.15),
            b1.animate.set_stroke(color=YELLOW, width=4),
            rate_func=there_and_back,
            run_time=max(0.05, 0.62),
        )

        # ------------------------------------------------------------
        # Beat 30: 32.86-34.84 hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.98))

        # ------------------------------------------------------------
        # Beat 31: 34.84-35.70 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.86))

        # ------------------------------------------------------------
        # Beat 32: 35.70-36.70 Conventional Fourier Transform title
        # ------------------------------------------------------------
        conv_title = Text("Conventional Fourier Transform", font_size=28, color=WHITE)
        conv_title.move_to(np.array([0, 3.0, 0]))
        self.play(
            FadeOut(single_spectrum_title),
            FadeIn(conv_title),
            spectrum_axes.animate.set_opacity(1.0),
            spectrum_curve.animate.set_fill(opacity=0.35).set_stroke(color=YELLOW, width=4).set_opacity(1.0),
            run_time=max(0.05, 1.00),
        )

        # ------------------------------------------------------------
        # Beat 33: 36.70-37.68 fan arrow/brace from spectrum peak
        # ------------------------------------------------------------
        peak_point = np.array([freq_to_x(10), amp_to_y(0.9), 0])
        top_left = np.array([-6.0, 1.15, 0])
        top_right = np.array([6.0, 1.15, 0])
        fan_lines = VGroup(
            Arrow(peak_point + UP * 0.1, top_left, buff=0.1, color=YELLOW, stroke_width=3),
            Arrow(peak_point + UP * 0.1, top_right, buff=0.1, color=YELLOW, stroke_width=3),
        )
        fan_lines.set_z_index(7)
        self.play(FadeIn(fan_lines), run_time=max(0.05, 0.98))

        # ------------------------------------------------------------
        # Beat 34: 37.68-38.32 Alpha label next to peak
        # ------------------------------------------------------------
        alpha_peak_label = Text("Alpha", font_size=22, color=YELLOW)
        alpha_peak_label.move_to(peak_point + RIGHT * 0.7 + UP * 0.15)
        self.play(
            FadeIn(alpha_peak_label),
            spectrum_curve.animate.set_stroke(width=5),
            run_time=max(0.05, 0.64),
        )

        # ------------------------------------------------------------
        # Beat 35: 38.32-39.06 Alpha label brightens
        # ------------------------------------------------------------
        self.play(Indicate(alpha_peak_label, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.74))

        # ------------------------------------------------------------
        # Beat 36: 39.06-40.06 sweep fan lines
        # ------------------------------------------------------------
        self.play(
            fan_lines.animate.rotate(angle=0.22, about_point=peak_point),
            rate_func=there_and_back,
            run_time=max(0.05, 1.00),
        )

        # ------------------------------------------------------------
        # Beat 37: 40.06-40.78 settle full width
        # ------------------------------------------------------------
        self.play(fan_lines.animate.set_stroke(opacity=0.75), run_time=max(0.05, 0.72))

        # ------------------------------------------------------------
        # Beat 38: 40.78-41.56 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------
        # Beat 39: 41.56-42.24 fan fades out
        # ------------------------------------------------------------
        self.play(FadeOut(fan_lines), run_time=max(0.05, 0.68))

        # ------------------------------------------------------------
        # Beat 40: 42.24-43.00 clock icon fades in
        # ------------------------------------------------------------
        clock_icon = VGroup(
            Circle(radius=0.18, color=WHITE, fill_opacity=0, stroke_width=2),
            Line(ORIGIN, UP * 0.12, color=WHITE, stroke_width=2),
            Line(ORIGIN, RIGHT * 0.09, color=WHITE, stroke_width=2),
        )
        clock_icon.move_to(alpha_peak_label.get_right() + RIGHT * 0.45)
        self.play(FadeIn(clock_icon), run_time=max(0.05, 0.76))

        # ------------------------------------------------------------
        # Beat 41: 43.00-43.74 clock pulses once
        # ------------------------------------------------------------
        self.play(clock_icon.animate.scale(1.25), rate_func=there_and_back, run_time=max(0.05, 0.74))

        # ------------------------------------------------------------
        # Beat 42: 43.74-44.30 small question mark next to clock
        # ------------------------------------------------------------
        q_mark = Text("?", font_size=26, color=WHITE, fill_opacity=0.6)
        q_mark.next_to(clock_icon, RIGHT, buff=0.25)
        self.play(FadeIn(q_mark), run_time=max(0.05, 0.56))

        # ------------------------------------------------------------
        # Beat 43: 44.30-45.14 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------
        # Beat 44: 45.14-46.54 cluster glow + spectrum brightens
        # ------------------------------------------------------------
        cluster = VGroup(alpha_peak_label, clock_icon, q_mark)
        cluster_glow = SurroundingRectangle(
            cluster,
            color=YELLOW,
            buff=0.15,
            stroke_width=2,
            stroke_opacity=0.65,
            fill_opacity=0.0,
        )
        self.play(
            FadeIn(cluster_glow),
            spectrum_axes.animate.set_opacity(1.0),
            spectrum_curve.animate.set_stroke(width=5),
            run_time=max(0.05, 1.40),
        )

        # ------------------------------------------------------------
        # Beat 45: 46.54-47.34 spectrum peak pulses gently
        # ------------------------------------------------------------
        self.play(
            spectrum_curve.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=max(0.05, 0.80),
        )

        # ------------------------------------------------------------
        # Beat 46: 47.34-48.52 Essential beneath spectrum
        # ------------------------------------------------------------
        essential_label = Text("Essential", font_size=26, color=YELLOW)
        essential_label.move_to(overall_avg_label.get_center())
        self.play(FadeOut(overall_avg_label), FadeIn(essential_label), run_time=max(0.05, 1.18))

        # ------------------------------------------------------------
        # Beat 47: 48.52-49.48 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.96))

        # ------------------------------------------------------------
        # Beat 48: 49.48-50.76 What frequencies are present?
        # ------------------------------------------------------------
        what_freq_text = Text("What frequencies are present?", font_size=26, color=WHITE)
        what_freq_text.move_to(essential_label.get_center())
        self.play(FadeOut(essential_label), FadeIn(what_freq_text), run_time=max(0.05, 1.28))

        # ------------------------------------------------------------
        # Beat 49: 50.76-52.10 spectrum alpha peak brightens
        # ------------------------------------------------------------
        self.play(
            spectrum_curve.animate.set_stroke(color=YELLOW, width=6).set_fill(opacity=0.45),
            Indicate(alpha_peak_label, color=YELLOW, scale_factor=1.15),
            run_time=max(0.05, 1.34),
        )

        # ------------------------------------------------------------
        # Beat 50: 52.10-52.64 pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.54))

        # ------------------------------------------------------------
        # Beat 51: 52.64-53.34 When do they occur?
        # ------------------------------------------------------------
        when_text = Text("When do they occur?", font_size=26, color=WHITE)
        when_text.move_to(what_freq_text.get_center())
        self.play(
            FadeOut(what_freq_text),
            FadeIn(when_text),
            clock_icon.animate.set_color(YELLOW).scale(1.15),
            q_mark.animate.set_color(YELLOW).scale(1.15),
            run_time=max(0.05, 0.70),
        )

        # ------------------------------------------------------------
        # Beat 52: 53.34-53.70 final pulse together
        # ------------------------------------------------------------
        self.play(
            clock_icon.animate.scale(1.1),
            q_mark.animate.scale(1.1),
            spectrum_curve.animate.set_stroke(width=7),
            rate_func=there_and_back,
            run_time=max(0.05, 0.36),
        )

        # ------------------------------------------------------------
        # Beat 53: 53.70-54.42 final hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.72))