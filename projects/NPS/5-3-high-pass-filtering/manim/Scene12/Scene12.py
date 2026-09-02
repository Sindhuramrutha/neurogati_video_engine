ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene12(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Helper: generic filter icon (funnel-like trapezoid + center line)
        def make_filter_icon(color, fill_color, fill_opacity):
            h = 1.0
            vertices = [
                np.array([-0.45, 0.45, 0]),
                np.array([0.45, 0.45, 0]),
                np.array([0.15, -0.45, 0]),
                np.array([-0.15, -0.45, 0]),
            ]
            polygon = Polygon(
                *vertices,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_color=color,
                stroke_width=4,
            )
            center_line = Line(
                np.array([-0.15, 0.0, 0]),
                np.array([0.15, 0.0, 0]),
                color=color,
                stroke_width=3,
            )
            return VGroup(polygon, center_line)

        # ------------------------------------------------------------
        # Beat 1: 0.00–1.20
        # Open with a small caution-layout remnant that fades away.
        caution_tri = Polygon(
            np.array([0, 0.55, 0]),
            np.array([-0.62, -0.32, 0]),
            np.array([0.62, -0.32, 0]),
            fill_opacity=0,
            stroke_color="#E8993A",
            stroke_width=6,
        )
        caution_ex = Text("!", font_size=38, color="#E8993A", weight="BOLD")
        caution_ex.move_to(caution_tri.get_center() + DOWN * 0.02)
        caution_text = Text("Apply with care", font_size=26, color="#E8993A", weight="BOLD")
        caution_text.next_to(caution_tri, DOWN, buff=0.35)
        caution_group = VGroup(caution_tri, caution_ex, caution_text)
        caution_group.move_to(UP * 2.7)
        self.add(caution_group)

        self.play(FadeOut(caution_group), run_time=max(0.05, 0.35))

        important_text = Text("Important Note", font_size=64, weight="BOLD", color=YELLOW)
        important_text.move_to(UP * 2.7)
        important_border = SurroundingRectangle(
            important_text,
            color=YELLOW,
            buff=0.2,
            stroke_width=4,
        )
        self.play(FadeIn(important_text), run_time=max(0.05, 0.5))
        self.play(Create(important_border), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 1.20 - (0.35 + 0.5 + 0.30)))  # 0.05

        # Gap to 1.70
        self.wait(max(0.05, 1.70 - 1.20))

        # ------------------------------------------------------------
        # Beat 2: 1.70–4.40
        low_text = Text("Low-frequency components", font_size=34, color=WHITE, weight="BOLD")
        neq_text = Text("≠", font_size=56, color=YELLOW, weight="BOLD")
        noise_text = Text("noise", font_size=34, color=WHITE)

        statement = VGroup(low_text, neq_text, noise_text).arrange(RIGHT, buff=0.35)
        statement.move_to(UP * 1.2)

        self.play(Write(low_text), run_time=max(0.05, 1.0))
        self.play(Write(neq_text), run_time=max(0.05, 0.9))
        self.play(Write(noise_text), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 2.70 - (1.0 + 0.9 + 0.6)))  # 0.20

        # Gap to 5.00
        self.wait(max(0.05, 5.00 - 4.40))

        # ------------------------------------------------------------
        # Beat 3: 5.00–5.84
        red_underline = Line(
            neq_text.get_left() + DOWN * 0.18,
            neq_text.get_right() + DOWN * 0.18,
            color=RED,
            stroke_width=8,
        )
        self.play(Create(red_underline), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.84 - 0.6))  # 0.24

        # Gap to 6.72
        self.wait(max(0.05, 6.72 - 5.84))

        # ------------------------------------------------------------
        # Beat 4: 6.72–10.96
        self.play(
            statement.animate.scale(0.8).shift(UP * 0.6),
            run_time=max(0.05, 0.8),
        )

        left_label = Text("one fixed filter setting", font_size=22, color=GREY)
        left_label.move_to(np.array([-3.2, 0.5, 0]))

        left_filter = make_filter_icon(
            color=GREY,
            fill_color=GREY,
            fill_opacity=0.4,
        )
        left_filter.scale(0.8).move_to(np.array([-3.2, -0.6, 0]))

        red_x_line1 = Line(
            left_filter.get_corner(UP + LEFT) + RIGHT * 0.12 + DOWN * 0.12,
            left_filter.get_corner(DOWN + RIGHT) + LEFT * 0.12 + UP * 0.12,
            color=RED,
            stroke_width=6,
        )
        red_x_line2 = Line(
            left_filter.get_corner(UP + RIGHT) + LEFT * 0.12 + DOWN * 0.12,
            left_filter.get_corner(DOWN + LEFT) + RIGHT * 0.12 + UP * 0.12,
            color=RED,
            stroke_width=6,
        )
        red_x = VGroup(red_x_line1, red_x_line2)
        left_icon_group = VGroup(left_filter, red_x)

        self.play(Write(left_label), run_time=max(0.05, 0.6))
        self.play(GrowFromCenter(left_filter), run_time=max(0.05, 0.6))
        self.play(Write(red_x), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 4.24 - (0.8 + 0.6 + 0.6 + 0.5)))  # 1.74

        # Gap to 11.60
        self.wait(max(0.05, 11.60 - 10.96))

        # ------------------------------------------------------------
        # Beat 5: 11.60–13.82
        arrow_fixed = Arrow(
            start=left_filter.get_top() + UP * 0.1,
            end=np.array([-2.5, statement.get_bottom()[1] - 0.1, 0]),
            color=RED,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15,
            stroke_width=4,
        )

        right_label = Text("setting chosen for this signal", font_size=22, color=WHITE)
        right_label.move_to(np.array([3.2, 0.5, 0]))
        right_filter = make_filter_icon(
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=0.8,
        )
        right_filter.scale(0.8).move_to(np.array([3.2, -0.6, 0]))
        checkmark = Text("✓", font_size=30, color=GREEN, weight="BOLD")
        checkmark.next_to(right_filter, RIGHT, buff=0.25)

        self.play(FadeIn(arrow_fixed), run_time=max(0.05, 0.5))
        self.play(
            Indicate(left_icon_group, color=RED, scale_factor=1.2),
            run_time=max(0.05, 0.6),
        )
        self.play(
            FadeIn(right_label),
            GrowFromCenter(right_filter),
            Write(checkmark),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 2.22 - (0.5 + 0.6 + 0.8)))  # 0.22

        # Gap to 14.58
        self.wait(max(0.05, 14.58 - 13.82))

        # ------------------------------------------------------------
        # Beat 6: 14.58–19.46
        arrow_to_label = Arrow(
            start=right_filter.get_top() + UP * 0.1,
            end=right_label.get_bottom() + DOWN * 0.1,
            color=GREEN,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15,
            stroke_width=4,
        )

        line_to_statement = Line(
            right_filter.get_top() + UP * 0.2,
            statement.get_bottom() + RIGHT * 1.5 + DOWN * 0.1,
            color=TEAL,
            stroke_width=3,
        )

        self.play(left_icon_group.animate.set_opacity(0.35), run_time=max(0.05, 0.6))
        self.play(
            right_filter.animate.set_fill(color=TEAL, opacity=1).set_stroke(color=TEAL, width=5),
            run_time=max(0.05, 0.8),
        )
        self.play(FadeIn(arrow_to_label), run_time=max(0.05, 0.6))
        self.play(FadeIn(line_to_statement), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 4.88 - (0.6 + 0.8 + 0.6 + 0.6)))  # 2.28

        # Gap to 19.84
        self.wait(max(0.05, 19.84 - 19.46))

        # ------------------------------------------------------------
        # Beat 7: 19.84–22.76
        final_caption = Text(
            "Choose settings for each signal, not one fixed value for everything.",
            font_size=24,
            color=WHITE,
        )
        final_caption.scale_to_fit_width(13)
        final_caption.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(final_caption), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.92 - 1.0))  # 1.92

        # ------------------------------------------------------------
        # Beat 8: 22.76–23.57
        self.wait(max(0.05, 0.31))
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=max(0.05, 0.5),
        )