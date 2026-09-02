ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene11(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Beat 1: 0.00–1.90 (1.90 s) ---
        tri_size = 0.7
        p1 = np.array([0, tri_size * 0.75, 0])
        p2 = np.array([-tri_size * 0.85, -tri_size * 0.45, 0])
        p3 = np.array([tri_size * 0.85, -tri_size * 0.45, 0])
        warning_triangle = Polygon(p1, p2, p3,
            fill_opacity=0,
            stroke_color="#E8993A",
            stroke_width=8,
        )
        warning_triangle.move_to(np.array([0, 2.2, 0]))

        exclamation = Text("!", font_size=52, color="#E8993A", weight="BOLD")
        exclamation.move_to(warning_triangle.get_center() + DOWN * 0.05)

        apply_text = Text("Apply with care", font_size=40, color="#E8993A", weight="BOLD")
        apply_text.next_to(warning_triangle, DOWN, buff=0.5)

        self.play(Write(warning_triangle), run_time=max(0.05, 0.8))
        self.play(FadeIn(exclamation), run_time=max(0.05, 0.3))
        self.play(FadeIn(apply_text), run_time=max(0.05, 0.5))
        # fill remaining of beat1
        self.wait(max(0.05, 1.90 - (0.8+0.3+0.5)))  # 0.3 s
        # gap between 1.90 and 2.32
        self.wait(max(0.05, 0.42))

        # --- Beat 2: 2.32–3.46 (1.14 s) ---
        left_plot = Rectangle(width=4.5, height=3.0, color=GREY, stroke_width=1.5, fill_opacity=0)
        left_plot.move_to(np.array([-2.8, -1.0, 0]))
        right_plot = Rectangle(width=4.5, height=3.0, color=GREY, stroke_width=1.5, fill_opacity=0)
        right_plot.move_to(np.array([2.8, -1.0, 0]))

        left_ax_h = Line(left_plot.get_left(), left_plot.get_right(), color=GREY, stroke_width=1)
        left_ax_v = Line(left_plot.get_bottom(), left_plot.get_top(), color=GREY, stroke_width=1)
        right_ax_h = Line(right_plot.get_left(), right_plot.get_right(), color=GREY, stroke_width=1)
        right_ax_v = Line(right_plot.get_bottom(), right_plot.get_top(), color=GREY, stroke_width=1)

        slider_track = Line(
            right_plot.get_right() + RIGHT * 0.5 + DOWN * 1.2,
            right_plot.get_right() + RIGHT * 0.5 + UP * 1.2,
            color=GREY,
            stroke_width=6,
        )
        slider_thumb = Dot(
            point=slider_track.get_center() + DOWN * 0.6,
            radius=0.12,
            color=WHITE,
            fill_opacity=1,
        )
        cutoff_label = Text("cutoff frequency", font_size=18, color=GREY)
        cutoff_label.rotate(90 * DEGREES)
        cutoff_label.next_to(slider_track, RIGHT, buff=0.2)

        self.play(
            FadeIn(left_plot), FadeIn(right_plot),
            FadeIn(left_ax_h), FadeIn(left_ax_v),
            FadeIn(right_ax_h), FadeIn(right_ax_v),
            FadeIn(slider_track), FadeIn(slider_thumb), FadeIn(cutoff_label),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 1.14 - 0.8))  # 0.34 s
        # gap to 4.30
        self.wait(max(0.05, 0.84))

        # --- Beat 3: 4.30–6.42 (2.12 s) ---
        def eeg_func(x):
            slow = 0.35 * np.sin(2 * np.pi * 0.5 * x)
            fast = 0.07 * np.sin(2 * np.pi * 5.0 * x)
            return slow + fast

        def make_eeg_curve(plot_rect, color=WHITE, num_points=300):
            left_x, right_x = plot_rect.get_left()[0] + 0.3, plot_rect.get_right()[0] - 0.3
            bot_y, top_y = plot_rect.get_bottom()[1] + 0.5, plot_rect.get_top()[1] - 0.5
            xs = np.linspace(-2.0, 2.0, num_points)
            ys = eeg_func(xs)
            mapped_xs = left_x + (xs - (-2.0)) / (2.0 - (-2.0)) * (right_x - left_x)
            mapped_ys = bot_y + (ys - (-0.5)) / (0.5 - (-0.5)) * (top_y - bot_y)
            points = [np.array([mx, my, 0]) for mx, my in zip(mapped_xs, mapped_ys)]
            curve = VMobject(stroke_width=2.5, stroke_color=color, fill_opacity=0)
            curve.set_points_smoothly(points)
            return curve

        left_eeg = make_eeg_curve(left_plot, color=WHITE)
        right_eeg = make_eeg_curve(right_plot, color=WHITE)

        self.play(Write(left_eeg), run_time=max(0.05, 0.9))
        thumb_target = slider_track.get_top() + DOWN * 0.2
        self.play(
            Write(right_eeg),
            slider_thumb.animate.move_to(thumb_target),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 2.12 - (0.9 + 1.0)))  # 0.22 s
        # gap to 6.74
        self.wait(max(0.05, 0.32))

        # --- Beat 4: 6.74–11.16 (4.42 s) ---
        def eeg_distorted(x):
            fast = 0.07 * np.sin(2 * np.pi * 5.0 * x)
            return fast

        def make_eeg_distorted(plot_rect, color=RED, num_points=300):
            left_x, right_x = plot_rect.get_left()[0] + 0.3, plot_rect.get_right()[0] - 0.3
            bot_y, top_y = plot_rect.get_bottom()[1] + 0.5, plot_rect.get_top()[1] - 0.5
            xs = np.linspace(-2.0, 2.0, num_points)
            ys = eeg_distorted(xs)
            mapped_xs = left_x + (xs - (-2.0)) / (2.0 - (-2.0)) * (right_x - left_x)
            mapped_ys = bot_y + (ys - (-0.5)) / (0.5 - (-0.5)) * (top_y - bot_y)
            points = [np.array([mx, my, 0]) for mx, my in zip(mapped_xs, mapped_ys)]
            curve = VMobject(stroke_width=2.5, stroke_color=color, fill_opacity=0)
            curve.set_points_smoothly(points)
            return curve

        right_eeg_distorted = make_eeg_distorted(right_plot, color=RED)

        self.play(
            Transform(right_eeg, right_eeg_distorted, replace_mobject_with_target_in_scene=True),
            run_time=max(0.05, 1.2),
        )

        # Red slider zone
        red_zone_bottom = thumb_target[1] - 0.1
        red_zone_top = slider_track.get_top()[1]
        red_zone_y = (red_zone_bottom + red_zone_top) / 2
        red_zone_height = red_zone_top - red_zone_bottom
        red_band = Rectangle(
            width=0.3,
            height=red_zone_height,
            fill_color=RED,
            fill_opacity=0.4,
            stroke_color=RED,
            stroke_width=2,
        )
        red_band.move_to(np.array([slider_track.get_center()[0], red_zone_y, 0]))

        too_high_label = Text("too high", font_size=16, color=RED, weight="BOLD")
        too_high_label.next_to(red_band, RIGHT, buff=0.15)

        arrow_start = red_band.get_right() + RIGHT * 0.3
        arrow_end = right_eeg.get_center() + RIGHT * 0.5 + UP * 0.8
        arrow_to_distorted = Arrow(
            start=arrow_start,
            end=arrow_end,
            color=RED,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15,
            stroke_width=4,
        )

        self.play(FadeIn(red_band), Write(too_high_label), run_time=max(0.05, 0.8))
        self.play(FadeIn(arrow_to_distorted), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 4.42 - (1.2 + 0.8 + 0.8)))  # 1.62 s
        # gap to 12.00
        self.wait(max(0.05, 0.84))

        # --- Beat 5: 12.00–14.60 (2.60 s) ---
        caption_box = RoundedRectangle(
            width=5.0, height=1.0, corner_radius=0.12,
            fill_color="#2A2A2A", fill_opacity=0.9,
            stroke_color=GREY, stroke_width=1.5,
        )
        caption_box.next_to(right_plot, DOWN, buff=0.4)
        caption_text = Text(
            "Slow physiological\ncomponents may be removed",
            font_size=20, color=WHITE, weight="BOLD", line_spacing=1.2,
        )
        caption_text.move_to(caption_box.get_center())

        leader_start = caption_box.get_top() + UP * 0.1
        leader_end = right_eeg.get_center() + DOWN * 0.6
        leader_line = Line(leader_start, leader_end, color=GREY, stroke_width=1.5)

        self.play(
            FadeIn(caption_box), FadeIn(caption_text), FadeIn(leader_line),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 2.60 - 1.0))  # 1.60 s

        # --- Beat 6: 14.60–20.14 (5.54 s) ---
        # 6a: slow-wave flattening emphasized (red glow)
        right_eeg_glow = right_eeg.copy().set_stroke(color=RED, width=8)
        self.play(
            Transform(right_eeg, right_eeg_glow, replace_mobject_with_target_in_scene=True),
            run_time=max(0.05, 0.6),
        )
        self.play(
            Transform(right_eeg_glow, right_eeg_distorted, replace_mobject_with_target_in_scene=True),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 1.5))

        # 6b: sharp transient ERP-like distortion
        def eeg_with_transient(x):
            base = eeg_distorted(x)
            peak = 0.4 * np.exp(-((x - 0.1) * 8) ** 2)
            return base + peak

        def make_eeg_transient(plot_rect, color=RED, num_points=300):
            left_x, right_x = plot_rect.get_left()[0] + 0.3, plot_rect.get_right()[0] - 0.3
            bot_y, top_y = plot_rect.get_bottom()[1] + 0.5, plot_rect.get_top()[1] - 0.5
            xs = np.linspace(-2.0, 2.0, num_points)
            ys = eeg_with_transient(xs)
            mapped_xs = left_x + (xs - (-2.0)) / (2.0 - (-2.0)) * (right_x - left_x)
            mapped_ys = bot_y + (ys - (-0.5)) / (0.5 - (-0.5)) * (top_y - bot_y)
            points = [np.array([mx, my, 0]) for mx, my in zip(mapped_xs, mapped_ys)]
            curve = VMobject(stroke_width=2.5, stroke_color=color, fill_opacity=0)
            curve.set_points_smoothly(points)
            return curve

        right_eeg_transient = make_eeg_transient(right_plot, color=RED)

        self.play(
            Transform(right_eeg, right_eeg_transient, replace_mobject_with_target_in_scene=True),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.3))
        self.play(
            Transform(right_eeg, right_eeg_distorted, replace_mobject_with_target_in_scene=True),
            run_time=max(0.05, 0.5),
        )
        # fill rest of beat6 (total animations used: 0.6+0.4+1.5+0.7+0.3+0.5=4.0)
        self.wait(max(0.05, 5.54 - 4.0))  # 1.54 s
        # gap to 20.72
        self.wait(max(0.05, 0.58))

        # --- Beat 7: 20.72–27.32 (6.60 s) ---
        neutral_thumb_pos = slider_track.get_center() + DOWN * 0.2
        self.play(
            slider_thumb.animate.move_to(neutral_thumb_pos),
            FadeOut(red_band), FadeOut(too_high_label), FadeOut(arrow_to_distorted),
            run_time=max(0.05, 1.2),
        )

        final_caption = Text(
            "Select the cutoff frequency according to the\nrecorded signal and the analysis objectives",
            font_size=20, color=WHITE, weight="BOLD", line_spacing=1.3,
        )
        final_caption.move_to(np.array([0, caption_box.get_bottom()[1] - 0.7, 0]))
        self.play(Write(final_caption), run_time=max(0.05, 1.2))
        # remaining of beat7
        self.wait(max(0.05, 6.60 - (1.2 + 1.2)))  # 4.20 s

        # --- Beat 8: 27.32–28.38 (1.06 s) ---
        self.wait(max(0.05, 1.06 - 0.5))  # 0.56 s
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=max(0.05, 0.5),
        )