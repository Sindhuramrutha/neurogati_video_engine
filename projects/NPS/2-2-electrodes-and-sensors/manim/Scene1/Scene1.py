ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Title
        title = Text("Learning Objectives", font_size=46, weight="BOLD", color=WHITE)
        title.to_edge(UP, buff=0.55)

        bullet_texts = [
            "Explain the purpose of an electrode or sensor.",
            "Distinguish between surface electrodes, needle electrodes, and microelectrodes.",
            "Describe the electrodes used in EEG and ECoG recordings.",
            "Explain why MEG uses magnetic sensors instead of electrodes.",
            "Compare the advantages and limitations of different recording sensors."
        ]

        square_side = 0.42
        square_x = -3.8
        y_positions = [1.9, 1.0, 0.1, -0.8, -1.7]

        squares = []
        texts = []
        for i, btext in enumerate(bullet_texts):
            square = Square(
                side_length=square_side,
                color=WHITE,
                stroke_width=3,
                fill_opacity=0
            )
            square.set_opacity(0.0)
            square.move_to(np.array([square_x, y_positions[i], 0]))
            squares.append(square)

            text = Text(btext, font_size=24, color=WHITE)
            if text.width > 10.0:
                text.scale_to_fit_width(10.0)
            text.next_to(square, RIGHT, buff=0.3)
            texts.append(text)

        placeholders = VGroup(*squares)
        self.add(placeholders)

        def make_checkmark(square):
            return VGroup(
                Line(
                    square.get_center() + LEFT * 0.15 + DOWN * 0.05,
                    square.get_center() + LEFT * 0.02 + UP * 0.09,
                    color=GREEN,
                    stroke_width=4
                ),
                Line(
                    square.get_center() + LEFT * 0.02 + UP * 0.09,
                    square.get_center() + RIGHT * 0.14 + DOWN * 0.12,
                    color=GREEN,
                    stroke_width=4
                )
            )

        # Beat 1: title appears, placeholder boxes fade to 20% opacity (0.00-2.84)
        self.play(
            FadeIn(title),
            placeholders.animate.set_opacity(0.2),
            run_time=max(0.05, 0.8
        ))
        self.wait(max(0.05, 2.04))

        # Beat 2: first bullet (2.84-5.80)
        check0 = make_checkmark(squares[0])
        self.play(
            FadeIn(texts[0]),
            Create(check0),
            squares[0].animate.set_opacity(1),
            run_time=max(0.05, 1.0
        ))
        self.wait(max(0.05, 1.96))

        # Gap to 6.40
        self.wait(max(0.05, 0.60))

        # Beat 3: second bullet (6.40-10.92)
        check1 = make_checkmark(squares[1])
        self.play(
            FadeIn(texts[1]),
            Create(check1),
            squares[1].animate.set_opacity(1),
            run_time=max(0.05, 1.1
        ))
        self.wait(max(0.05, 3.42))

        # Gap to 11.20
        self.wait(max(0.05, 0.28))

        # Beat 4: third bullet (11.20-15.04)
        check2 = make_checkmark(squares[2])
        self.play(
            FadeIn(texts[2]),
            Create(check2),
            squares[2].animate.set_opacity(1),
            run_time=max(0.05, 1.1
        ))
        self.wait(max(0.05, 2.74))

        # Gap to 15.78
        self.wait(max(0.05, 0.74))

        # Beat 5: fourth bullet (15.78-19.22)
        check3 = make_checkmark(squares[3])
        self.play(
            FadeIn(texts[3]),
            Create(check3),
            squares[3].animate.set_opacity(1),
            run_time=max(0.05, 1.0
        ))
        self.wait(max(0.05, 2.44))

        # Gap to 19.76
        self.wait(max(0.05, 0.54))

        # Beat 6: fifth bullet (19.76-23.54)
        check4 = make_checkmark(squares[4])
        self.play(
            FadeIn(texts[4]),
            Create(check4),
            squares[4].animate.set_opacity(1),
            run_time=max(0.05, 1.0
        ))
        self.wait(max(0.05, 2.78))

        # Beat 7: final hold (23.54-24.35)
        self.wait(max(0.05, 0.81))