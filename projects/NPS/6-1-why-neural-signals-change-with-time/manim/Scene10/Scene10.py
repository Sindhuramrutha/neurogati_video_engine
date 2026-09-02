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


class Scene10(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_wave_segment(x0, x1, base_y, amp, freq, color, width):
            xs = np.linspace(x0, x1, 200)
            ys = base_y + amp * np.sin(2 * np.pi * freq * (xs - x0) / (x1 - x0))
            pts = np.array([xs, ys, np.zeros_like(xs)]).T
            return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)

        def make_clock_icon(color=YELLOW, radius=0.30):
            circle = Circle(radius=radius, color=color, fill_opacity=0, stroke_width=3)
            hand_min = Line(ORIGIN, UP * radius * 0.55, color=color, stroke_width=2.5)
            hand_hr = Line(ORIGIN, RIGHT * radius * 0.40, color=color, stroke_width=2.5)
            return VGroup(circle, hand_min, hand_hr)

        def make_bullet(text_str, font_size=26, weight="NORMAL"):
            dot = Dot(radius=0.06, color=YELLOW)
            text = Text(text_str, font_size=font_size, color=WHITE, weight=weight)
            group = VGroup(dot, text).arrange(RIGHT, buff=0.22)
            return group, text

        def build_spectrum_widget():
            x_axis = Line(LEFT * 1.1, RIGHT * 1.1, color=GREY_B, stroke_width=2)
            y_axis = Line(DOWN * 0.7, UP * 0.7, color=GREY_B, stroke_width=2)
            xs = np.linspace(-1.0, 1.0, 120)
            ys = 0.55 * np.exp(-(xs ** 2) / 0.12)
            pts = np.array([xs, ys, np.zeros_like(xs)]).T
            curve = VMobject(stroke_color=YELLOW, stroke_width=2.5)
            curve.set_points_as_corners(pts)
            widget = VGroup(x_axis, y_axis, curve)
            widget.scale(0.9)
            widget.set_opacity(0.7)
            return widget

        # ---------- beat 1: previous display fades out ----------
        prev_group = VGroup()

        base_y = 1.15
        left_x, right_x = -6.0, 6.0
        baseline = Line(
            np.array([left_x, base_y, 0]),
            np.array([right_x, base_y, 0]),
            color=GREY_B,
            stroke_width=2,
        )
        left_wave = make_wave_segment(left_x, -2.0, base_y, 0.55, 14, YELLOW, 5)
        mid_wave = make_wave_segment(-2.0, 2.0, base_y, 0.14, 8, TEAL, 3).set_opacity(0.25)
        right_wave = make_wave_segment(2.0, 6.0, base_y, 0.14, 8, TEAL, 3).set_opacity(0.25)

        b1 = DashedLine(
            np.array([-2.0, base_y - 0.8, 0]),
            np.array([-2.0, base_y + 0.8, 0]),
            dash_length=0.12,
            dashed_ratio=0.6,
            color=GREY_B,
            stroke_width=2,
        )
        b2 = DashedLine(
            np.array([2.0, base_y - 0.8, 0]),
            np.array([2.0, base_y + 0.8, 0]),
            dash_length=0.12,
            dashed_ratio=0.6,
            color=GREY_B,
            stroke_width=2,
        )
        alpha_prev_label = Text("Alpha present (0–10 s)", font_size=18, color=YELLOW)
        alpha_prev_label.move_to(np.array([-4.0, 0.35, 0]))

        spec_center = np.array([0, -1.9, 0])
        spec_x_axis = Line(
            spec_center + LEFT * 3,
            spec_center + RIGHT * 3,
            color=GREY_B,
            stroke_width=2,
        )
        spec_y_axis = Line(
            spec_center + DOWN * 0.7,
            spec_center + UP * 0.7,
            color=GREY_B,
            stroke_width=2,
        )
        freqs = np.linspace(0, 30, 300)
        amps = 0.7 * np.exp(-((freqs - 10) / 1.5) ** 2)

        def freq_to_x(freq):
            return spec_center[0] - 3 + (freq / 30.0) * 6

        spec_pts = np.array(
            [freq_to_x(freqs), spec_center[1] - 0.7 + amps * 0.7, np.zeros_like(freqs)]
        ).T
        spec_curve = VMobject(stroke_color=YELLOW, stroke_width=3)
        spec_curve.set_points_as_corners(spec_pts)

        alpha_peak_prev = Text("Alpha", font_size=18, color=YELLOW)
        alpha_peak_prev.move_to(spec_center + np.array([-0.9, 0.55, 0]))

        clock_prev = make_clock_icon(WHITE, radius=0.18)
        clock_prev.move_to(alpha_peak_prev.get_right() + RIGHT * 0.45)

        question_prev = Text("?", font_size=26, color=WHITE, fill_opacity=0.6)
        question_prev.next_to(clock_prev, RIGHT, buff=0.20)

        prev_group.add(
            baseline,
            left_wave,
            mid_wave,
            right_wave,
            b1,
            b2,
            alpha_prev_label,
            spec_x_axis,
            spec_y_axis,
            spec_curve,
            alpha_peak_prev,
            clock_prev,
            question_prev,
        )

        self.add(prev_group)
        self.play(FadeOut(prev_group), run_time=max(0.05, 3.16))

        # ---------- beat 2: first question ----------
        q1_text = Text("Which frequencies are present?", font_size=38, color=WHITE)
        q1_text.scale_to_fit_width(10)
        q1_text.move_to(ORIGIN)
        self.play(FadeIn(q1_text), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 0.84))

        # ---------- beat 3: strike through first question ----------
        self.wait(max(0.05, 0.56))
        strike_line = Line(
            q1_text.get_corner(UL),
            q1_text.get_corner(DR),
            color=RED,
            stroke_width=6,
        )
        self.play(
            Create(strike_line),
            q1_text.animate.set_color(GREY_B),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.46))
        q1_bundle = VGroup(q1_text, strike_line)

        # ---------- beat 4: second, expanded question ----------
        q2_text = Text(
            "Which frequencies are present, and when do they occur?",
            font_size=40,
            color=YELLOW,
        )
        q2_text.scale_to_fit_width(10.5)
        q2_clock = make_clock_icon(YELLOW, radius=0.32)
        q2_group = VGroup(q2_text, q2_clock).arrange(RIGHT, buff=0.60)
        q2_group.scale_to_fit_width(12.5)
        q2_group.move_to(ORIGIN)

        self.play(
            FadeOut(q1_bundle, shift=LEFT * 6),
            FadeIn(q2_group),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.40))
        self.play(
            q2_clock.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.18))

        # ---------- beat 5: time-frequency analysis label + arrow ----------
        tfa_text = Text("Time–Frequency Analysis", font_size=30, color=WHITE)
        forward_arrow = Arrow(
            LEFT * 1.2,
            RIGHT * 1.2,
            color=YELLOW,
            stroke_width=4,
            buff=0.0,
        )
        tfa_group = VGroup(tfa_text, forward_arrow).arrange(RIGHT, buff=0.50)
        tfa_group.next_to(q2_group, DOWN, buff=1.0)

        self.wait(max(0.05, 0.84))
        self.play(FadeIn(tfa_group), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 2.46))

        # ---------- beat 6: hold ----------
        self.wait(max(0.05, 2.58))

        # ---------- beat 7: summary panel ----------
        summary_rect = Rectangle(
            width=12.0,
            height=7.0,
            fill_color=BLACK,
            fill_opacity=0.35,
            stroke_color=GREY_B,
            stroke_width=2.5,
        )
        summary_header = Text("Summary", font_size=34, color=YELLOW)
        summary_header.move_to(np.array([0, 2.85, 0]))
        summary_panel = VGroup(summary_rect, summary_header)

        self.wait(max(0.05, 0.42))
        self.play(
            FadeOut(q2_group),
            FadeOut(tfa_group),
            FadeIn(summary_panel),
            run_time=max(0.05, 1.80),
        )
        self.wait(max(0.05, 0.78))

        panel_left_x = summary_rect.get_left()[0] + 0.9

        # ---------- beat 8: first bullet ----------
        bullet1_group, bullet1_text = make_bullet("Nonstationary signals introduced", font_size=26)
        bullet1_group.move_to(np.array([panel_left_x, 2.10, 0]), aligned_edge=LEFT)
        self.play(FadeIn(bullet1_group), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 2.24))

        # ---------- beat 9: second bullet ----------
        bullet2_group, bullet2_text = make_bullet("Neural recordings generally nonstationary", font_size=26)
        bullet2_group.move_to(np.array([panel_left_x, 1.45, 0]), aligned_edge=LEFT)
        self.wait(max(0.05, 0.66))
        self.play(FadeIn(bullet2_group), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 2.74))

        # ---------- beat 10: third bullet, highlight behaviour ----------
        full_causes = "Causes: behaviour, sensory stimulation, cognitive processes, physiological state"

        def make_bullet3_text(color_map=None):
            if color_map is None:
                text = Text(full_causes, font_size=22, color=WHITE)
            else:
                text = Text(full_causes, font_size=22, color=WHITE, t2c=color_map)
            text.scale_to_fit_width(9.0)
            return text

        bullet3_dot = Dot(radius=0.06, color=YELLOW)
        bullet3_text = make_bullet3_text()
        bullet3_group = VGroup(bullet3_dot, bullet3_text).arrange(RIGHT, buff=0.22)
        bullet3_group.move_to(np.array([panel_left_x, 0.75, 0]), aligned_edge=LEFT)

        behaviour_highlight = make_bullet3_text({"behaviour": YELLOW})
        behaviour_highlight.move_to(bullet3_text.get_center())
        bullet3_neutral = make_bullet3_text()
        bullet3_neutral.move_to(bullet3_text.get_center())

        self.play(FadeIn(bullet3_group), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 0.30))
        self.play(Transform(bullet3_text, behaviour_highlight), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.35))
        self.play(Transform(bullet3_text, bullet3_neutral), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 1.41))

        # ---------- beat 11: highlight remaining causes ----------
        sensory_highlight = make_bullet3_text({"sensory stimulation": YELLOW})
        sensory_highlight.move_to(bullet3_text.get_center())
        cognitive_highlight = make_bullet3_text({"cognitive processes": YELLOW})
        cognitive_highlight.move_to(bullet3_text.get_center())
        physio_highlight = make_bullet3_text({"physiological state": YELLOW})
        physio_highlight.move_to(bullet3_text.get_center())

        self.wait(max(0.05, 0.72))
        self.play(Transform(bullet3_text, sensory_highlight), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.20))
        self.play(Transform(bullet3_text, bullet3_neutral), run_time=max(0.05, 0.50))
        self.play(Transform(bullet3_text, cognitive_highlight), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.20))
        self.play(Transform(bullet3_text, bullet3_neutral), run_time=max(0.05, 0.50))
        self.play(Transform(bullet3_text, physio_highlight), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.20))
        self.play(Transform(bullet3_text, bullet3_neutral), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.48))

        # ---------- beat 12: fourth bullet ----------
        bullet4_group, bullet4_text = make_bullet(
            "Single spectrum insufficient",
            font_size=26,
            weight="BOLD",
        )
        bullet4_group.move_to(np.array([panel_left_x, -0.10, 0]), aligned_edge=LEFT)
        self.wait(max(0.05, 0.80))
        self.play(FadeIn(bullet4_group), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 1.80))

        # ---------- beat 13: highlight fourth bullet ----------
        bullet4_glow = SurroundingRectangle(
            bullet4_group,
            color=YELLOW,
            buff=0.15,
            stroke_width=3,
            stroke_opacity=0.6,
            fill_color=YELLOW,
            fill_opacity=0.10,
        )
        self.wait(max(0.05, 0.40))
        self.play(
            bullet4_text.animate.set_color(YELLOW),
            FadeIn(bullet4_glow),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 2.50))

        # ---------- beat 14: small waveform icon beside fourth bullet ----------
        wave_icon = SVGMobject(
            ASSET_PATHS["activity"],
            color=TEAL,
            fill_opacity=1,
            stroke_opacity=0,
        )
        wave_icon.scale(0.35)
        wave_icon.next_to(bullet4_group, RIGHT, buff=0.35)

        self.wait(max(0.05, 0.44))
        self.play(FadeIn(wave_icon), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.50))
        self.play(
            wave_icon.animate.scale(1.25),
            rate_func=there_and_back,
            run_time=max(0.05, 0.50),
        )
        self.play(
            FadeOut(wave_icon),
            FadeOut(bullet4_glow),
            bullet4_text.animate.set_color(WHITE),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 0.72))

        # ---------- beat 15: Next topic heading ----------
        next_topic_text = Text("Next topic", font_size=22, color=YELLOW)
        next_topic_text.move_to(np.array([panel_left_x, -1.00, 0]), aligned_edge=LEFT)

        self.wait(max(0.05, 0.88))
        self.play(FadeIn(next_topic_text), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 2.34))

        # ---------- beat 16: STFT text ----------
        stft_text = Text(
            "Short-Time Fourier Transform (STFT)",
            font_size=24,
            weight="BOLD",
            color=WHITE,
        )
        stft_text.scale_to_fit_width(7.5)
        stft_text.move_to(np.array([panel_left_x, -1.65, 0]), aligned_edge=LEFT)

        self.wait(max(0.05, 0.68))
        self.play(FadeIn(stft_text), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.56))

        # ---------- beat 17: highlight STFT abbreviation ----------
        stft_highlight = Text(
            "Short-Time Fourier Transform (STFT)",
            font_size=24,
            weight="BOLD",
            color=WHITE,
            t2c={"STFT": YELLOW},
        )
        stft_highlight.scale_to_fit_width(7.5)
        stft_highlight.move_to(stft_text.get_center())

        stft_neutral = Text(
            "Short-Time Fourier Transform (STFT)",
            font_size=24,
            weight="BOLD",
            color=WHITE,
        )
        stft_neutral.scale_to_fit_width(7.5)
        stft_neutral.move_to(stft_text.get_center())

        self.wait(max(0.05, 0.64))
        self.play(Transform(stft_text, stft_highlight), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.30))
        self.play(Transform(stft_text, stft_neutral), run_time=max(0.05, 0.25))

        # ---------- beat 18: brighten STFT, link to faint spectrum ----------
        spectrum_widget = build_spectrum_widget()
        spectrum_widget.move_to(np.array([4.10, -1.60, 0]))

        arrow_to_spectrum = Arrow(
            stft_text.get_right() + RIGHT * 0.25,
            spectrum_widget.get_left() + LEFT * 0.15,
            buff=0.05,
            color=YELLOW,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )

        self.wait(max(0.05, 0.46))
        self.play(
            stft_text.animate.set_color(YELLOW),
            FadeIn(arrow_to_spectrum),
            FadeIn(spectrum_widget),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 1.58))

        # ---------- beat 19: highlight time then frequency ----------
        annotation_text = Text("time + frequency", font_size=18, color=GREY_B)
        annotation_text.move_to(np.array([panel_left_x, -2.15, 0]), aligned_edge=LEFT)

        annotation_time_highlight = Text(
            "time + frequency",
            font_size=18,
            color=WHITE,
            t2c={"time": YELLOW},
        )
        annotation_time_highlight.move_to(annotation_text.get_center())

        annotation_neutral = Text(
            "time + frequency",
            font_size=18,
            color=GREY_B,
        )
        annotation_neutral.move_to(annotation_text.get_center())

        annotation_freq_highlight = Text(
            "time + frequency",
            font_size=18,
            color=WHITE,
            t2c={"frequency": YELLOW},
        )
        annotation_freq_highlight.move_to(annotation_text.get_center())

        annotation_both_soft = Text(
            "time + frequency",
            font_size=18,
            color=WHITE,
            t2c={"time": GOLD, "frequency": GOLD},
        ).set_opacity(0.85)
        annotation_both_soft.move_to(annotation_text.get_center())

        self.wait(max(0.05, 0.38))
        self.play(FadeIn(annotation_text), run_time=max(0.05, 0.40))
        self.play(Transform(annotation_text, annotation_time_highlight), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.20))
        self.play(Transform(annotation_text, annotation_neutral), run_time=max(0.05, 0.50))
        self.play(Transform(annotation_text, annotation_freq_highlight), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.20))
        self.play(Transform(annotation_text, annotation_both_soft), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.56))

        # ---------- beat 20: final hold ----------
        self.wait(max(0.05, 0.73))