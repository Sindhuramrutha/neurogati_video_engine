ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Beat 1: 0.00-1.84
        # Recreate a quiet version of the previous two-panel layout so
        # it can fade out smoothly, while the "Key Definition" badge
        # fades in at the top center.
        # ------------------------------------------------------------
        panel_w = 6.0
        panel_h = 5.8

        left_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            stroke_color=GREY_B,
            stroke_width=2,
            stroke_opacity=0.55,
            fill_color=GREY_B,
            fill_opacity=0.12,
        ).move_to(LEFT * 3.45)

        right_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            stroke_color=GREY_B,
            stroke_width=2,
            stroke_opacity=0.55,
            fill_color=GREY_B,
            fill_opacity=0.12,
        ).move_to(RIGHT * 3.45)

        divider = Line(
            start=np.array([0, -panel_h / 2, 0]),
            end=np.array([0, panel_h / 2, 0]),
            color=GREY_B,
            stroke_width=3,
            stroke_opacity=0.55,
        )

        left_ghost = Text(
            "slow variations removed",
            font_size=18,
            color=RED,
        ).set_opacity(0.45).move_to(left_panel.get_top() + DOWN * 0.75)

        right_ghost = Text(
            "faster variations remain",
            font_size=18,
            color=GREEN,
        ).set_opacity(0.45).move_to(right_panel.get_top() + DOWN * 0.75)

        previous_panels = VGroup(left_panel, right_panel, divider, left_ghost, right_ghost)

        badge_border = RoundedRectangle(
            width=4.4,
            height=0.85,
            corner_radius=0.22,
            stroke_color=YELLOW,
            stroke_width=2.0,
            fill_color=GREY_B,
            fill_opacity=0.20,
        ).move_to(UP * 3.3)

        badge_text = Text(
            "Key Definition",
            font_size=34,
            weight=BOLD,
            color=YELLOW,
        ).move_to(badge_border.get_center())

        badge_group = VGroup(badge_border, badge_text)

        self.add(previous_panels)
        self.play(
            FadeOut(previous_panels),
            FadeIn(badge_group),
            run_time=max(0.05, 1.84),
        )
        self.wait(max(0.05, 0.96))

        # ------------------------------------------------------------
        # Beat 2: 2.80-4.48
        # Neutral label "High-Pass Filter:" appears below the badge.
        # ------------------------------------------------------------
        hp_label = Text(
            "High-Pass Filter:",
            font_size=38,
            weight=BOLD,
            color=WHITE,
        )
        hp_label.next_to(badge_border, DOWN, buff=0.60)

        self.play(FadeIn(hp_label), run_time=max(0.05, 1.68))
        self.wait(max(0.05, 0.52))

        # ------------------------------------------------------------
        # Beat 3: 5.00-6.60
        # Green phrase fading in below the label.
        # ------------------------------------------------------------
        green_phrase = Text(
            "A filter that preserves high-frequency components",
            font_size=30,
            color=WHITE,
            t2c={"preserves high-frequency components": GREEN},
        )
        green_phrase.next_to(hp_label, DOWN, buff=0.50)

        self.play(FadeIn(green_phrase), run_time=max(0.05, 1.60))

        # ------------------------------------------------------------
        # Beat 4: 6.60-7.38
        # The green phrase holds steady.
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------
        # Beat 5: 7.38-9.34
        # Red "while attenuating..." phrase appears below it.
        # ------------------------------------------------------------
        red_phrase = Text(
            "while attenuating low-frequency components",
            font_size=30,
            color=WHITE,
            t2c={"attenuating low-frequency components": RED},
        )
        red_phrase.next_to(green_phrase, DOWN, buff=0.50)

        self.play(FadeIn(red_phrase), run_time=max(0.05, 1.96))

        # ------------------------------------------------------------
        # Beat 6: 9.34-11.50
        # Final line and its thin red underline beneath the last phrase.
        # ------------------------------------------------------------
        below_part = Text("below a ", font_size=30, color=WHITE)
        cutoff_part = Text("selected cutoff frequency", font_size=30, color=RED)
        period_part = Text(".", font_size=30, color=WHITE)

        final_line = VGroup(below_part, cutoff_part, period_part).arrange(RIGHT, buff=0.0)
        final_line.next_to(red_phrase, DOWN, buff=0.50)

        underline = Line(
            start=np.array([
                cutoff_part.get_left()[0],
                cutoff_part.get_bottom()[1] - 0.10,
                0,
            ]),
            end=np.array([
                cutoff_part.get_right()[0],
                cutoff_part.get_bottom()[1] - 0.10,
                0,
            ]),
            color=RED,
            stroke_width=2,
        )

        self.play(
            FadeIn(final_line),
            FadeIn(underline),
            run_time=max(0.05, 2.16),
        )

        # ------------------------------------------------------------
        # Beat 7: 11.50-12.28
        # Full definition card holds. The badge border pulses once gently.
        # ------------------------------------------------------------
        self.play(
            badge_border.animate.set_stroke(width=5).scale(1.05),
            run_time=max(0.05, 0.40),
        )
        self.play(
            badge_border.animate.set_stroke(width=2).scale(1 / 1.05),
            run_time=max(0.05, 0.38),
        )