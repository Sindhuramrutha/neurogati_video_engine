ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Layout constants -------------------------------------------------
        panel = Rectangle(
            width=11.0,
            height=6.2,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color=GREY,
            fill_opacity=0.12,
        )
        panel.move_to(ORIGIN)

        header = Text("Learning Objectives", font_size=46, color=WHITE, weight="BOLD")
        header.move_to([0, 2.45, 0])

        row_y = [1.35, 0.0, -1.35]
        square_x = -4.55
        content_left_x = -3.85
        line_end_x = 5.0

        squares = []
        blank_lines = []
        for y in row_y:
            square = Rectangle(
                width=0.46,
                height=0.46,
                color=WHITE,
                stroke_width=3,
                fill_opacity=0,
            )
            square.move_to([square_x, y, 0])
            squares.append(square)

            blank = Line(
                [content_left_x, y, 0],
                [line_end_x, y, 0],
                color=GREY_B,
                stroke_width=3,
                stroke_opacity=0.7,
            )
            blank_lines.append(blank)

        def build_check(center):
            p1 = center + np.array([-0.17, -0.02, 0])
            p2 = center + np.array([-0.05, -0.14, 0])
            p3 = center + np.array([0.16, 0.11, 0])
            check = VMobject(stroke_color=GREEN, stroke_width=5)
            check.set_points_as_corners([p1, p2, p3])
            return check

        # ---- Beat 1: 0.00-3.02 -----------------------------------------------
        empty_panel = VGroup(panel, header, *squares, *blank_lines)
        self.play(FadeIn(empty_panel, run_time=max(0.05, 3.02)))

        # ---- Beat 2: 3.02-4.02 -----------------------------------------------
        self.play(
            squares[0].animate.set_stroke(YELLOW, width=5),
            rate_func=rate_functions.there_and_back,
            run_time=max(0.05, 1.0),
        )

        # ---- Beat 3: 4.02-7.02 -----------------------------------------------
        text1 = Text("Define what the neural signal acquisition chain is", font_size=28, color=WHITE)
        if text1.width > 8.7:
            text1.scale_to_fit_width(8.7)
        text1.move_to([content_left_x, row_y[0], 0], aligned_edge=LEFT)

        self.play(FadeOut(blank_lines[0]), Write(text1), run_time=max(0.05, 2.6))
        self.play(Create(build_check([square_x, row_y[0], 0])), run_time=max(0.05, 0.4))

        # ---- Beat 4: 7.02-7.80 -----------------------------------------------
        self.play(
            squares[1].animate.set_stroke(YELLOW, width=5),
            rate_func=rate_functions.there_and_back,
            run_time=max(0.05, 0.78),
        )

        # ---- Beat 5: 7.80-9.74 -----------------------------------------------
        text2 = Text("Identify its major components", font_size=28, color=WHITE)
        if text2.width > 8.7:
            text2.scale_to_fit_width(8.7)
        text2.move_to([content_left_x, row_y[1], 0], aligned_edge=LEFT)

        self.play(FadeOut(blank_lines[1]), Write(text2), run_time=max(0.05, 1.6))
        self.play(Create(build_check([square_x, row_y[1], 0])), run_time=max(0.05, 0.34))

        # ---- Beat 6: 9.74-10.72 ----------------------------------------------
        self.play(
            squares[2].animate.set_stroke(YELLOW, width=5),
            rate_func=rate_functions.there_and_back,
            run_time=max(0.05, 0.98),
        )

        # ---- Beat 7: 10.72-12.96 ---------------------------------------------
        text3 = Text("Explain the function of each stage", font_size=28, color=WHITE)
        if text3.width > 8.7:
            text3.scale_to_fit_width(8.7)
        text3.move_to([content_left_x, row_y[2], 0], aligned_edge=LEFT)

        self.play(FadeOut(blank_lines[2]), Write(text3), run_time=max(0.05, 1.8))
        self.play(Create(build_check([square_x, row_y[2], 0])), run_time=max(0.05, 0.44))

        # ---- Beat 8: 12.96-15.72 ---------------------------------------------
        full_panel = VGroup(
            panel,
            header,
            squares[0],
            squares[1],
            squares[2],
            text1,
            text2,
            text3,
            *[mob for mob in self.mobjects if isinstance(mob, VMobject) and mob not in [blank_lines[0], blank_lines[1], blank_lines[2]]]
        )
        self.play(
            full_panel.animate.scale(1.02),
            rate_func=rate_functions.there_and_back,
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 1.76))