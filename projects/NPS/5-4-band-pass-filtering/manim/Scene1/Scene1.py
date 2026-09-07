ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Beat 1: Title card (0.00 - 2.80, duration 2.80) ----
        title = Text("Learning Objectives", font_size=56, color=WHITE)
        title.to_edge(UP, buff=0.6)

        self.play(Write(title), run_time=max(0.05, 1.5))
        # Gentle pulse while it's the focus
        self.play(
            title.animate.scale(1.04),
            run_time=max(0.05, 0.4),
        )
        self.play(title.animate.scale(1 / 1.04), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.5))  # fills to ~2.80

        # Shared styling for all bullet points
        BULLET_FONT_SIZE = 36
        BULLET_COLOR = WHITE
        CHECK_COLOR = GREEN
        LEFT_MARGIN = -5.5  # start off-screen left
        BULLET_X = -3.5  # final resting x
        BULLET_START_Y = 1.8
        BULLET_VERTICAL_GAP = 0.85

        bullets_text = [
            "Define a band‑pass filter",
            "Explain how it operates",
            "Understand lower and upper cutoff frequencies",
            "Describe applications in neural signal processing",
            "Recognise advantages and limitations",
        ]

        # We'll store them to keep them visible
        bullet_mobs = []
        check_mobs = []

        # ---- Beat 2: First bullet (2.80 - 5.40, duration 2.60) ----
        b1 = Text(bullets_text[0], font_size=BULLET_FONT_SIZE, color=BULLET_COLOR)
        b1.move_to(np.array([LEFT_MARGIN, BULLET_START_Y, 0]))
        check1 = SVGMobject(
            ASSET_PATHS["check_circle"],
            fill_color=CHECK_COLOR,
            fill_opacity=1,
            stroke_width=0,
        ).scale_to_fit_height(0.45)
        check1.next_to(b1, LEFT, buff=0.3)
        target_y = BULLET_START_Y

        self.play(
            b1.animate.move_to(np.array([BULLET_X, target_y, 0])),
            FadeIn(check1, shift=RIGHT * 0.3),
            run_time=max(0.05, 1.5),
        )
        # Small pulse on checkmark to keep it alive
        self.play(check1.animate.scale(1.2), run_time=max(0.05, 0.4))
        self.play(check1.animate.scale(1 / 1.2), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.3))
        bullet_mobs.append(b1)
        check_mobs.append(check1)

        # ---- Beat 3: Second bullet (5.40 - 7.36, duration 1.96) ----
        b2 = Text(bullets_text[1], font_size=BULLET_FONT_SIZE, color=BULLET_COLOR)
        b2.move_to(np.array([LEFT_MARGIN, BULLET_START_Y - BULLET_VERTICAL_GAP, 0]))
        check2 = SVGMobject(
            ASSET_PATHS["check_circle"],
            fill_color=CHECK_COLOR,
            fill_opacity=1,
            stroke_width=0,
        ).scale_to_fit_height(0.45)
        check2.next_to(b2, LEFT, buff=0.3)
        target_y2 = BULLET_START_Y - BULLET_VERTICAL_GAP

        self.play(
            b2.animate.move_to(np.array([BULLET_X, target_y2, 0])),
            FadeIn(check2, shift=RIGHT * 0.3),
            run_time=max(0.05, 1.2),
        )
        self.play(check2.animate.scale(1.2), run_time=max(0.05, 0.3))
        self.play(check2.animate.scale(1 / 1.2), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.16))
        bullet_mobs.append(b2)
        check_mobs.append(check2)

        # ---- Beat 4: Third bullet (7.36 - 10.42, duration 3.06) ----
        b3 = Text(bullets_text[2], font_size=BULLET_FONT_SIZE, color=BULLET_COLOR)
        b3.move_to(np.array([LEFT_MARGIN, BULLET_START_Y - 2 * BULLET_VERTICAL_GAP, 0]))
        check3 = SVGMobject(
            ASSET_PATHS["check_circle"],
            fill_color=CHECK_COLOR,
            fill_opacity=1,
            stroke_width=0,
        ).scale_to_fit_height(0.45)
        check3.next_to(b3, LEFT, buff=0.3)
        target_y3 = BULLET_START_Y - 2 * BULLET_VERTICAL_GAP

        self.play(
            b3.animate.move_to(np.array([BULLET_X, target_y3, 0])),
            FadeIn(check3, shift=RIGHT * 0.3),
            run_time=max(0.05, 1.2),
        )
        self.play(check3.animate.scale(1.2), run_time=max(0.05, 0.3))
        self.play(check3.animate.scale(1 / 1.2), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 1.26))
        bullet_mobs.append(b3)
        check_mobs.append(check3)

        # ---- Beat 5: Fourth bullet (10.42 - 15.18, duration 4.76) ----
        b4 = Text(bullets_text[3], font_size=BULLET_FONT_SIZE, color=BULLET_COLOR)
        b4.move_to(np.array([LEFT_MARGIN, BULLET_START_Y - 3 * BULLET_VERTICAL_GAP, 0]))
        check4 = SVGMobject(
            ASSET_PATHS["check_circle"],
            fill_color=CHECK_COLOR,
            fill_opacity=1,
            stroke_width=0,
        ).scale_to_fit_height(0.45)
        check4.next_to(b4, LEFT, buff=0.3)
        target_y4 = BULLET_START_Y - 3 * BULLET_VERTICAL_GAP

        self.play(
            b4.animate.move_to(np.array([BULLET_X, target_y4, 0])),
            FadeIn(check4, shift=RIGHT * 0.3),
            run_time=max(0.05, 1.5),
        )
        self.play(check4.animate.scale(1.2), run_time=max(0.05, 0.4))
        self.play(check4.animate.scale(1 / 1.2), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 2.46))
        bullet_mobs.append(b4)
        check_mobs.append(check4)

        # ---- Beat 6: Fifth bullet (15.18 - 17.24, duration 2.06) ----
        b5 = Text(bullets_text[4], font_size=BULLET_FONT_SIZE, color=BULLET_COLOR)
        b5.move_to(np.array([LEFT_MARGIN, BULLET_START_Y - 4 * BULLET_VERTICAL_GAP, 0]))
        check5 = SVGMobject(
            ASSET_PATHS["check_circle"],
            fill_color=CHECK_COLOR,
            fill_opacity=1,
            stroke_width=0,
        ).scale_to_fit_height(0.45)
        check5.next_to(b5, LEFT, buff=0.3)
        target_y5 = BULLET_START_Y - 4 * BULLET_VERTICAL_GAP

        self.play(
            b5.animate.move_to(np.array([BULLET_X, target_y5, 0])),
            FadeIn(check5, shift=RIGHT * 0.3),
            run_time=max(0.05, 1.2),
        )
        self.play(check5.animate.scale(1.2), run_time=max(0.05, 0.3))
        self.play(check5.animate.scale(1 / 1.2), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.26))
        bullet_mobs.append(b5)
        check_mobs.append(check5)

        # ---- Beat 7: Hold until end (17.24 - 18.32, duration 1.08) ----
        # Gentle pulse on title while everything remains visible
        self.play(title.animate.scale(1.03), run_time=max(0.05, 0.4))
        self.play(title.animate.scale(1 / 1.03), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.28))