ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    "brain": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg"
}


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Helpers
        # ----------------------------------------------------------------
        def center_signal(y):
            return y - np.mean(y)

        def make_trace(xs, ys, color=WHITE, stroke_width=2, opacity=1):
            pts = np.array([xs, ys, np.zeros_like(xs)]).T
            trace = VMobject(color=color, stroke_width=stroke_width, fill_opacity=0)
            trace.set_points_as_corners(pts)
            trace.set_opacity(opacity)
            return trace

        def dashed_vline(x, y0, y1, color=GREY_B, dash_len=0.05, gap=0.04, stroke_width=1.5):
            parts = VGroup()
            y = y0
            while y < y1 - 1e-6:
                y2 = min(y + dash_len, y1)
                parts.add(Line([x, y, 0], [x, y2, 0], color=color, stroke_width=stroke_width))
                y = y2 + gap
            return parts

        def stage_box(label, width=1.3, height=0.65, fill_color=BLUE, stroke_color=WHITE):
            rect = RoundedRectangle(
                corner_radius=0.12,
                width=width,
                height=height,
                fill_color=fill_color,
                fill_opacity=0.30,
                stroke_color=stroke_color,
                stroke_width=2,
            )
            text = Text(label, font_size=16, color=WHITE, weight="BOLD")
            text.scale_to_fit_width(max(0.4, width - 0.20))
            text.move_to(rect.get_center())
            return VGroup(rect, text)

        def make_neural_icon(center=ORIGIN):
            in_nodes = VGroup(*[
                Circle(radius=0.07, fill_color=BLUE, fill_opacity=1, stroke_width=0)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.14)
            hid_nodes = VGroup(*[
                Circle(radius=0.07, fill_color=TEAL, fill_opacity=1, stroke_width=0)
                for _ in range(4)
            ]).arrange(DOWN, buff=0.11)
            out_nodes = VGroup(*[
                Circle(radius=0.07, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
                for _ in range(2)
            ]).arrange(DOWN, buff=0.18)

            VGroup(in_nodes, hid_nodes, out_nodes).arrange(RIGHT, buff=0.18)

            links = VGroup()
            for a in in_nodes:
                for b in hid_nodes:
                    links.add(Line(a.get_right(), b.get_left(), color=GREY_B, stroke_width=1))
            for b in hid_nodes:
                for c in out_nodes:
                    links.add(Line(b.get_right(), c.get_left(), color=GREY_B, stroke_width=1))

            icon = VGroup(links, in_nodes, hid_nodes, out_nodes)
            icon.move_to(center)
            icon.scale_to_fit_height(0.9)
            return icon

        # ----------------------------------------------------------------
        # Fade out previous scene's bottom statement + miniature trace
        # ----------------------------------------------------------------
        prev_statement = VGroup(
            Text("Raw waveform", font_size=22, color=BLUE, weight="BOLD"),
            Arrow(LEFT, RIGHT, color=WHITE, stroke_width=4, buff=0.1),
            Text("Relevant measurable features", font_size=22, color=YELLOW, weight="BOLD"),
        ).arrange(RIGHT, buff=0.6).move_to([0, -3.0, 0])

        mini_xs = np.linspace(-0.7, 0.7, 80)
        mini_ys = center_signal(0.2 * np.sin(3 * mini_xs) + 0.1 * np.sin(7 * mini_xs + 0.6))
        prev_mini_trace = make_trace(mini_xs, mini_ys, color=BLUE, stroke_width=3).scale_to_fit_width(1.4)
        prev_mini_trace.move_to([5.0, -3.0, 0])

        # ----------------------------------------------------------------
        # Panels and divider
        # ----------------------------------------------------------------
        panel_w = 6.0
        panel_h = 5.0
        left_center = np.array([-3.1, 0.8, 0])
        right_center = np.array([3.1, 0.8, 0])

        left_bg = Rectangle(width=panel_w, height=panel_h, fill_color=BLUE, fill_opacity=0.03, stroke_width=0)
        left_bg.move_to(left_center)
        left_border = DashedVMobject(
            Rectangle(width=panel_w, height=panel_h, stroke_color=GREY_B, stroke_width=2, fill_opacity=0),
            num_dashes=42,
        ).move_to(left_center)

        right_bg = Rectangle(width=panel_w, height=panel_h, fill_color=BLUE, fill_opacity=0.03, stroke_width=0)
        right_bg.move_to(right_center)
        right_border = DashedVMobject(
            Rectangle(width=panel_w, height=panel_h, stroke_color=GREY_B, stroke_width=2, fill_opacity=0),
            num_dashes=42,
        ).move_to(right_center)

        left_panel = VGroup(left_bg, left_border)
        right_panel = VGroup(right_bg, right_border)

        divider = Line([0, 3.35, 0], [0, -1.55, 0], color=GREY_B, stroke_width=2).set_opacity(0.4)

        left_title = Text("Interpretation", font_size=28, color=GREY_B, weight="BOLD")
        left_title.move_to(left_center + np.array([0, 2.7, 0]))
        right_title = Text("Classification", font_size=28, color=GREY_B, weight="BOLD")
        right_title.move_to(right_center + np.array([0, 2.7, 0]))

        right_panel_group0 = VGroup(right_bg, right_border, right_title)

        # Beat 1: 0.00-2.18
        self.play(
            FadeOut(prev_statement),
            FadeOut(prev_mini_trace),
            FadeIn(left_panel),
            FadeIn(right_panel),
            FadeIn(divider),
            Write(left_title),
            Write(right_title),
            run_time=max(0.05, 2.18),
        )

        # Beat 2: 2.18-4.56
        big_q = Text("?", font_size=150, color=GOLD, weight="BOLD")
        big_q.move_to([0, 0.6, 0])
        what_text = Text("what do features mean?", font_size=28, color=GREY_B)
        what_text.next_to(big_q, DOWN, buff=0.25)

        self.play(GrowFromCenter(big_q), FadeIn(what_text), run_time=max(0.05, 0.70))
        self.play(big_q.animate.scale(1.08), run_time=max(0.05, 0.75))
        self.play(big_q.animate.scale(1 / 1.08), run_time=max(0.05, 0.75))
        self.wait(max(0.05, 0.18))

        # Beat 3: 4.56-6.80
        q_left = Text("?", font_size=54, color=YELLOW, weight="BOLD").move_to(big_q.get_center()).set_opacity(0)
        q_right = Text("?", font_size=54, color=YELLOW, weight="BOLD").move_to(big_q.get_center()).set_opacity(0)
        left_q_pos = np.array([left_center[0], 1.45, 0])
        right_q_pos = np.array([right_center[0], 1.45, 0])
        self.add(q_left, q_right)

        self.play(
            big_q.animate.scale(0.2).set_opacity(0),
            FadeOut(what_text),
            q_left.animate.move_to(left_q_pos).set_opacity(1),
            q_right.animate.move_to(right_q_pos).set_opacity(1),
            left_title.animate.set_color(YELLOW),
            right_title.animate.set_color(YELLOW),
            run_time=max(0.05, 1.60),
        )
        self.play(Indicate(q_left, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.32))
        self.play(Indicate(q_right, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.32))

        # Beat 4: 6.80-7.56
        self.play(
            left_border.animate.set_stroke(YELLOW, width=5),
            left_bg.animate.set_fill(BLUE, opacity=0.16),
            left_title.animate.set_color(WHITE).scale(1.12),
            right_panel_group0.animate.set_opacity(0.28),
            q_right.animate.set_opacity(0),
            run_time=max(0.05, 0.76),
        )

        # Beat 5: 7.56-9.34
        left_xs = np.linspace(-1.6, 1.6, 240)
        left_ys = center_signal(
            0.30 * np.sin(2.2 * left_xs + 0.2)
            + 0.12 * np.sin(5.4 * left_xs + 0.7)
            + 0.07 * np.sin(9.0 * left_xs + 1.2)
        )
        left_eeg = make_trace(left_xs, left_ys, color=BLUE, stroke_width=4)
        left_eeg.scale_to_fit_width(3.0).move_to(np.array([left_center[0], 2.30, 0]))

        left_eeg_label = Text("EEG", font_size=17, color=BLUE, weight="BOLD")
        left_eeg_label.next_to(left_eeg, DOWN, buff=0.08)

        blank_area = DashedVMobject(
            Rectangle(width=2.7, height=0.95, stroke_color=GREY_B, stroke_width=1.5, fill_opacity=0),
            num_dashes=20,
        ).move_to(np.array([left_center[0], 0.05, 0]))

        left_arrow_start = np.array([left_center[0], left_eeg.get_bottom()[1] - 0.08, 0])
        left_arrow = Arrow(
            left_arrow_start,
            np.array([left_center[0], blank_area.get_top()[1] + 0.05, 0]),
            color=GREY_B,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            FadeIn(left_eeg),
            FadeIn(left_eeg_label),
            FadeIn(blank_area),
            FadeIn(left_arrow),
            run_time=max(0.05, 1.78),
        )

        # Beat 6: 9.34-13.04
        meaning_text = Text("meaning of activity", font_size=17, color=GREY_B, slant="ITALIC")
        meaning_text.move_to(blank_area.get_center()).set_opacity(0)

        self.play(Indicate(left_eeg, color=YELLOW, scale_factor=1.06), run_time=max(0.05, 0.70))
        self.play(left_arrow.animate.set_stroke(WHITE, width=5).set_opacity(1), run_time=max(0.05, 0.80))
        self.play(FadeIn(meaning_text), run_time=max(0.05, 0.60))
        self.play(Indicate(left_eeg, color=YELLOW, scale_factor=1.06), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.80))

        # Beat 7: 13.04-13.94
        self.play(FadeOut(meaning_text), FadeOut(blank_area), run_time=max(0.05, 0.90))

        # Beat 8: 13.94-16.62
        spec_center = np.array([left_center[0] - 0.4, -0.35, 0])
        spec_half_w = 1.25
        spec_h = 1.15
        spec_y_base = spec_center[1] - spec_h / 2
        spec_top = spec_y_base + spec_h

        x_axis = Arrow(
            np.array([spec_center[0] - spec_half_w, spec_y_base, 0]),
            np.array([spec_center[0] + spec_half_w, spec_y_base, 0]),
            color=WHITE,
            stroke_width=2,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )
        y_axis = Arrow(
            np.array([spec_center[0] - spec_half_w, spec_y_base, 0]),
            np.array([spec_center[0] - spec_half_w, spec_top, 0]),
            color=WHITE,
            stroke_width=2,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        spec_data_x = np.linspace(0, 2 * spec_half_w, 180)
        spec_vals = (
            0.10 * np.exp(-((spec_data_x - 0.45) ** 2) / (2 * 0.25 ** 2))
            + 0.22 * np.exp(-((spec_data_x - 1.25) ** 2) / (2 * 0.20 ** 2))
            + 0.09 * np.exp(-((spec_data_x - 2.15) ** 2) / (2 * 0.25 ** 2))
        )
        spec_vals = spec_vals / np.max(spec_vals) * (spec_h * 0.78)

        spec_xs_screen = spec_center[0] - spec_half_w + spec_data_x
        spec_ys_screen = spec_y_base + spec_vals
        spec_curve = make_trace(spec_xs_screen, spec_ys_screen, color=GREEN, stroke_width=3)

        alpha_peak_data_x = 1.25
        alpha_peak_screen_x = spec_center[0] - spec_half_w + alpha_peak_data_x
        alpha_peak_screen_y = spec_y_base + spec_h * 0.78
        alpha_label = Text("alpha", font_size=13, color=YELLOW)
        alpha_label.next_to([alpha_peak_screen_x, alpha_peak_screen_y, 0], UP, buff=0.06)

        frequency_label = Text("Frequency", font_size=13, color=WHITE)
        frequency_label.next_to(x_axis, DOWN, buff=0.08)
        power_label = Text("Power", font_size=13, color=WHITE).rotate(PI / 2)
        power_label.next_to(y_axis, LEFT, buff=0.08)

        spec_label = Text("frequency analysis", font_size=18, color=YELLOW, weight="BOLD")
        spec_label.move_to(np.array([left_center[0], 0.55, 0]))

        spectrum_rest = VGroup(x_axis, y_axis, spec_curve, frequency_label, power_label)

        new_left_arrow = Arrow(
            left_arrow_start,
            np.array([spec_center[0], spec_top, 0]),
            color=WHITE,
            stroke_width=5,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            Transform(left_arrow, new_left_arrow),
            FadeIn(spectrum_rest),
            FadeIn(alpha_label),
            FadeIn(spec_label),
            run_time=max(0.05, 2.68),
        )

        # Beat 9: 16.62-19.24
        alpha_peak_point = np.array([alpha_peak_screen_x, alpha_peak_screen_y, 0])
        alpha_glow = Circle(
            radius=0.20,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_color=YELLOW,
            fill_opacity=0.08,
        ).move_to(alpha_peak_point)

        dashed_alpha_line = dashed_vline(
            alpha_peak_point[0],
            spec_y_base,
            alpha_peak_point[1],
            color=YELLOW,
            dash_len=0.05,
            gap=0.04,
            stroke_width=1.8,
        )
        increased_text = Text("increased alpha power", font_size=13, color=YELLOW)
        increased_text.next_to(dashed_alpha_line, RIGHT, buff=0.08).shift(DOWN * 0.05)

        self.play(
            FadeIn(alpha_glow),
            FadeIn(dashed_alpha_line),
            FadeIn(increased_text),
            spectrum_rest.animate.set_opacity(0.35),
            run_time=max(0.05, 1.50),
        )
        self.play(
            Indicate(left_eeg, color=YELLOW, scale_factor=1.06),
            alpha_glow.animate.scale(1.18).set_opacity(1),
            run_time=max(0.05, 0.72),
        )
        self.wait(max(0.05, 0.40))

        # Beat 10: 19.24-21.66
        brain_icon = SVGMobject(ASSET_PATHS["brain"])
        brain_icon.set_fill(WHITE, opacity=1).set_stroke(WHITE, width=0)
        brain_icon.scale_to_fit_height(0.75).move_to(np.array([left_center[0] + 2.0, -0.8, 0]))

        thought_bubble = VGroup(
            Ellipse(width=1.7, height=0.55, fill_color=WHITE, fill_opacity=0.95, stroke_width=0),
            Text("Understanding", font_size=18, color=BLACK, weight="BOLD"),
        )
        thought_bubble[1].move_to(thought_bubble[0].get_center())
        thought_bubble.next_to(brain_icon, UP + RIGHT, buff=0.12)

        brain_arrow = Arrow(
            alpha_peak_point,
            brain_icon.get_center() + LEFT * 0.4,
            color=YELLOW,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.20,
        )

        self.play(
            FadeIn(brain_icon),
            FadeIn(thought_bubble),
            FadeIn(brain_arrow),
            run_time=max(0.05, 1.40),
        )
        self.play(brain_icon.animate.scale(1.18), thought_bubble.animate.scale(1.05), run_time=max(0.05, 0.52))
        self.play(brain_icon.animate.scale(1 / 1.18), run_time=max(0.05, 0.38))
        self.wait(max(0.05, 0.12))

        # Beat 11: 21.66-26.18
        cross = Text("✗", font_size=88, color=RED, fill_opacity=0.22, stroke_width=0)
        cross.move_to(np.array([left_center[0] - 1.8, -0.75, 0]))
        not_class_text = Text("not predefined class", font_size=15, color=GREY_B, slant="ITALIC")
        not_class_text.next_to(cross, DOWN, buff=0.10)

        self.play(FadeIn(cross), FadeIn(not_class_text), run_time=max(0.05, 1.20))
        self.play(cross.animate.scale(1.08).set_opacity(0.30), run_time=max(0.05, 0.80))
        self.play(cross.animate.scale(1 / 1.08).set_opacity(0.22), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 1.72))

        # Beat 12: 26.18-29.10
        ripple1 = Circle(radius=0.20, stroke_color=YELLOW, stroke_width=2, fill_opacity=0)
        ripple1.move_to(brain_icon.get_center())
        ripple2 = ripple1.copy()
        self.add(ripple1, ripple2)

        self.play(
            cross.animate.set_opacity(0.10),
            brain_icon.animate.set_opacity(1).scale(1.15),
            thought_bubble.animate.scale(1.12),
            run_time=max(0.05, 0.90),
        )
        self.play(Indicate(thought_bubble[1], color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.55))
        self.play(
            ripple1.animate.scale(2.6).set_opacity(0),
            ripple2.animate.scale(3.4).set_opacity(0),
            run_time=max(0.05, 0.75),
        )
        self.wait(max(0.05, 0.72))

        # Content group for later dimming / restoration
        left_panel_whole = VGroup(
            left_bg,
            left_border,
            left_title,
            left_eeg,
            left_eeg_label,
            left_arrow,
            spec_label,
            spectrum_rest,
            alpha_label,
            alpha_glow,
            dashed_alpha_line,
            increased_text,
            brain_arrow,
            brain_icon,
            thought_bubble,
            cross,
            not_class_text,
        )

        # Beat 13: 29.10-31.46
        self.play(
            left_panel_whole.animate.set_opacity(0.30),
            right_bg.animate.set_opacity(1).set_fill(BLUE, opacity=0.16),
            right_border.animate.set_opacity(1).set_stroke(YELLOW, width=5),
            right_title.animate.set_opacity(1).set_color(WHITE).scale(1.12),
            run_time=max(0.05, 2.36),
        )

        # Beat 14: 31.46-33.46
        right_eeg = make_trace(left_xs, left_ys, color=BLUE, stroke_width=4)
        right_eeg.scale_to_fit_width(3.0).move_to(np.array([right_center[0], 2.30, 0]))
        right_eeg_label = Text("EEG", font_size=17, color=BLUE, weight="BOLD")
        right_eeg_label.next_to(right_eeg, DOWN, buff=0.08)

        pre_box = stage_box("Preprocessing", width=1.2, height=0.65, fill_color=BLUE)
        pre_box.move_to(np.array([0.9, 0.05, 0]))
        feat_box = stage_box("Feature Extraction", width=1.3, height=0.65, fill_color=TEAL)
        feat_box.move_to(np.array([2.5, 0.05, 0]))

        self.play(FadeIn(right_eeg), FadeIn(right_eeg_label), run_time=max(0.05, 0.70))
        self.play(FadeIn(pre_box), run_time=max(0.05, 0.65))
        self.play(FadeIn(feat_box), run_time=max(0.05, 0.65))

        # Beat 15: 33.46-37.52
        classifier_box = stage_box("Classifier", width=1.6, height=0.80, fill_color=PURPLE, stroke_color=YELLOW)
        classifier_box.move_to(np.array([4.3, 0.05, 0]))

        pipeline_arrow1 = Arrow(
            pre_box.get_right() + RIGHT * 0.05,
            feat_box.get_left() + LEFT * 0.05,
            color=WHITE,
            stroke_width=3,
            buff=0.06,
            max_tip_length_to_length_ratio=0.20,
        )
        pipeline_arrow2 = Arrow(
            feat_box.get_right() + RIGHT * 0.05,
            classifier_box.get_left() + LEFT * 0.05,
            color=WHITE,
            stroke_width=3,
            buff=0.06,
            max_tip_length_to_length_ratio=0.20,
        )

        class_q = Text("?", font_size=22, color=YELLOW)
        class_q.next_to(classifier_box, UP, buff=0.08)

        self.play(FadeIn(classifier_box), run_time=max(0.05, 0.70))
        self.play(Create(pipeline_arrow1), Create(pipeline_arrow2), run_time=max(0.05, 0.80))
        self.play(FadeIn(class_q), run_time=max(0.05, 0.50))
        self.play(Indicate(classifier_box, color=YELLOW, scale_factor=1.05), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 1.06))

        # Beat 16: 37.52-38.30
        self.play(Indicate(classifier_box, color=YELLOW, scale_factor=1.06), run_time=max(0.05, 0.40))
        self.play(Indicate(right_eeg, color=YELLOW, scale_factor=1.06), run_time=max(0.05, 0.38))

        # Beat 17: 38.30-44.66
        out_labels = ["Wake", "NREM Sleep", "REM Sleep"]
        out_slots = VGroup(*[
            RoundedRectangle(
                corner_radius=0.09,
                width=0.85,
                height=0.55,
                fill_color=BLUE,
                fill_opacity=0.20,
                stroke_color=WHITE,
                stroke_width=2,
            )
            for _ in range(3)
        ])
        out_slots.arrange(RIGHT, buff=0.12)
        out_slots.move_to(np.array([classifier_box.get_center()[0], classifier_box.get_bottom()[1] - 0.55, 0]))

        branch_arrows = VGroup(*[
            Arrow(
                classifier_box.get_bottom() + DOWN * 0.05,
                slot.get_top() + UP * 0.05,
                color=WHITE,
                stroke_width=2.5,
                buff=0.05,
                max_tip_length_to_length_ratio=0.18,
            )
            for slot in out_slots
        ])

        out_texts = VGroup()
        for slot, lab in zip(out_slots, out_labels):
            t = Text(lab, font_size=11, color=WHITE, weight="BOLD")
            t.scale_to_fit_width(slot.width - 0.12)
            t.move_to(slot.get_center())
            t.set_opacity(0)
            out_texts.add(t)

        self.play(FadeOut(class_q), FadeIn(out_slots), Create(branch_arrows), run_time=max(0.05, 1.40))
        self.add(out_texts)

        self.play(
            out_texts[0].animate.set_opacity(1),
            out_slots[0].animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, 1.65),
        )
        self.play(
            out_texts[1].animate.set_opacity(1),
            out_slots[1].animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, 1.65),
        )
        self.play(
            out_texts[2].animate.set_opacity(1),
            out_slots[2].animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, 1.66),
        )

        # Beat 18: 44.66-48.12
        seg_rect = RoundedRectangle(
            corner_radius=0.10,
            width=1.0,
            height=0.52,
            stroke_color=YELLOW,
            stroke_width=2.5,
            fill_color=YELLOW,
            fill_opacity=0.16,
        )
        seg_text = Text("segment", font_size=13, color=YELLOW)
        seg_group = VGroup(seg_rect, seg_text).arrange(DOWN, buff=0.06)
        start_x = right_eeg.get_left()[0] + 0.5
        end_x = right_eeg.get_right()[0] - 0.5
        seg_group.move_to(np.array([start_x, right_eeg.get_center()[1], 0]))

        self.play(FadeIn(seg_group), run_time=max(0.05, 0.40))
        self.play(seg_group.animate.move_to(np.array([end_x, right_eeg.get_center()[1], 0])), run_time=max(0.05, 2.50))
        self.wait(max(0.05, 0.56))

        # Beat 19: 48.12-51.30
        ghost = seg_rect.copy().scale(0.45).set_opacity(0.60)
        ghost.move_to(np.array([end_x, right_eeg.get_center()[1], 0]))
        self.add(ghost)

        self.play(ghost.animate.move_to(pre_box.get_center()), run_time=max(0.05, 0.55))
        self.play(ghost.animate.move_to(feat_box.get_center()), run_time=max(0.05, 0.55))
        self.play(ghost.animate.move_to(classifier_box.get_center()), run_time=max(0.05, 0.55))

        ml_label = Text("machine-learning model", font_size=12, color=GREY_B, slant="ITALIC")
        ml_label.next_to(classifier_box, UP, buff=0.12)

        self.play(
            FadeIn(ml_label),
            out_slots[0].animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, 0.45),
            out_texts[0].animate.set_color(YELLOW),
            run_time=max(0.05, 0.53),
        )
        self.play(
            out_slots[0].animate.set_stroke(WHITE, width=2).set_fill(BLUE, 0.20),
            out_texts[0].animate.set_color(WHITE),
            out_slots[1].animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, 0.45),
            out_texts[1].animate.set_color(YELLOW),
            run_time=max(0.05, 0.50),
        )
        self.play(
            out_slots[1].animate.set_stroke(WHITE, width=2).set_fill(BLUE, 0.20),
            out_texts[1].animate.set_color(WHITE),
            out_slots[2].animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, 0.45),
            out_texts[2].animate.set_color(YELLOW),
            run_time=max(0.05, 0.50),
        )

        right_panel_whole = VGroup(
            right_bg,
            right_border,
            right_title,
            right_eeg,
            right_eeg_label,
            pre_box,
            feat_box,
            classifier_box,
            pipeline_arrow1,
            pipeline_arrow2,
            out_slots,
            out_texts,
            branch_arrows,
            ml_label,
        )

        # Beat 20: 51.30-52.04
        checkmark = Text("✓", font_size=22, color=GREEN, weight="BOLD")
        checkmark.next_to(out_slots[2], RIGHT, buff=0.08)
        self.play(FadeIn(checkmark), right_panel_whole.animate.set_opacity(0.72), run_time=max(0.05, 0.74))

        # Beat 21: 52.04-54.54
        bci_area = RoundedRectangle(
            corner_radius=0.10,
            width=12.4,
            height=1.6,
            fill_color=WHITE,
            fill_opacity=0.04,
            stroke_color=GREY_B,
            stroke_width=1.8,
        ).move_to(np.array([0, -3.0, 0]))

        neural_xs = np.linspace(0, 2.2, 90)
        neural_ys = np.zeros_like(neural_xs)
        for spike_x in [0.25, 0.6, 0.95, 1.3, 1.7]:
            neural_ys += 0.7 * np.exp(-((neural_xs - spike_x) ** 2) / (2 * 0.03 ** 2))
        neural_trace = make_trace(neural_xs, neural_ys, color=BLUE, stroke_width=3)
        neural_trace.scale_to_fit_width(2.2).move_to(np.array([-5.0, bci_area.get_center()[1], 0]))
        neural_label = Text("Neural activity", font_size=13, color=BLUE, weight="BOLD")
        neural_label.next_to(neural_trace, DOWN, buff=0.08)

        classifier_icon = make_neural_icon(center=np.array([-1.6, bci_area.get_center()[1], 0]))

        bci_arrow = Arrow(
            neural_trace.get_right() + RIGHT * 0.1,
            classifier_icon.get_left() + LEFT * 0.1,
            color=WHITE,
            stroke_width=2.5,
            buff=0.06,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            FadeIn(bci_area),
            FadeIn(neural_trace),
            FadeIn(neural_label),
            FadeIn(bci_arrow),
            FadeIn(classifier_icon),
            run_time=max(0.05, 2.50),
        )

        # Beat 22: 54.54-57.20
        bci_labels = ["Move left", "Move right", "Select"]
        bci_output_slots = VGroup(*[
            RoundedRectangle(
                corner_radius=0.08,
                width=1.25,
                height=0.50,
                fill_color=BLUE,
                fill_opacity=0.20,
                stroke_color=WHITE,
                stroke_width=2,
            )
            for _ in range(3)
        ])
        bci_output_slots.arrange(RIGHT, buff=0.18)
        bci_output_slots.move_to(np.array([1.8, bci_area.get_center()[1], 0]))

        bci_branch_arrows = VGroup(*[
            Arrow(
                classifier_icon.get_right() + RIGHT * 0.05,
                slot.get_left() + LEFT * 0.05,
                color=WHITE,
                stroke_width=2,
                buff=0.05,
                max_tip_length_to_length_ratio=0.20,
            )
            for slot in bci_output_slots
        ])

        bci_texts = VGroup()
        for slot, lab in zip(bci_output_slots, bci_labels):
            t = Text(lab, font_size=12, color=WHITE, weight="BOLD")
            t.scale_to_fit_width(slot.width - 0.12)
            t.move_to(slot.get_center())
            t.set_opacity(0)
            bci_texts.add(t)

        self.play(FadeIn(bci_output_slots), Create(bci_branch_arrows), run_time=max(0.05, 0.70))
        self.add(bci_texts)

        self.play(
            bci_texts[0].animate.set_opacity(1),
            bci_output_slots[0].animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, 0.65),
        )
        self.play(
            bci_texts[1].animate.set_opacity(1),
            bci_output_slots[1].animate.set_stroke(YELLOW, width=4),
            Indicate(neural_trace, color=YELLOW, scale_factor=1.05),
            run_time=max(0.05, 0.65),
        )
        self.play(
            bci_texts[2].animate.set_opacity(1),
            bci_output_slots[2].animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, 0.66),
        )

        # Beat 23: 57.20-58.10
        pulse_dot = Dot(radius=0.09, color=YELLOW)
        pulse_dot.move_to(brain_icon.get_center())
        pulse_dot.set_z_index(10)
        self.add(pulse_dot)

        self.play(
            left_panel_whole.animate.set_opacity(0.70),
            right_panel_whole.animate.set_opacity(0.95),
            run_time=max(0.05, 0.25),
        )
        self.play(pulse_dot.animate.move_to(classifier_box.get_center()), run_time=max(0.05, 0.30))
        self.play(pulse_dot.animate.move_to(bci_output_slots[2].get_center()), run_time=max(0.05, 0.35))