ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Beat 1: electrode, skin, biological source, still
        electrode = Ellipse(
            width=0.9, height=0.28,
            color=GREY, fill_color=GREY, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2
        ).move_to(np.array([0, 2.85, 0]))

        skin = Line(LEFT * 6.2 + UP * 1.55, RIGHT * 6.2 + UP * 1.55,
                    color=GREY_B, stroke_width=5)

        source_circle = Circle(radius=0.18, color=YELLOW,
                               fill_color=YELLOW, fill_opacity=0.3,
                               stroke_width=0)
        source_dot = Dot(point=np.array([0, 0.35, 0]), radius=0.10,
                         color=YELLOW, fill_opacity=1)
        source_glow = VGroup(source_circle, source_dot)
        source_glow.move_to(np.array([0, 0.35, 0]))

        dashed_line = DashedLine(
            electrode.get_bottom(), source_glow.get_top(),
            color=GREY_B, stroke_width=2, dash_length=0.08
        )
        source_label = Text("biological source", font_size=22, color=GREY_B)
        source_label.next_to(source_glow, RIGHT, buff=0.3)

        self.add(electrode, skin, dashed_line, source_glow, source_label)
        self.wait(max(0.05, 2.06))

        # Beat 2: pulse source and emphasize distance
        self.wait(max(0.05, 0.74))

        distance_arrow = DoubleArrow(
            electrode.get_bottom() + DOWN * 0.05,
            source_glow.get_top() + UP * 0.05,
            buff=0.05,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.1
        )
        distance_label = Text("distance", font_size=24, color=YELLOW)
        distance_label.next_to(distance_arrow, RIGHT, buff=0.2)

        self.play(
            FadeOut(dashed_line),
            FadeIn(distance_arrow),
            Write(distance_label),
            run_time=max(0.05, 0.9
        ))
        self.play(
            source_glow.animate.scale(1.25).set_opacity(0.45),
            run_time=max(0.05, 1.28),
            rate_func=there_and_back
        )
        self.play(
            source_glow.animate.scale(1.25).set_opacity(0.45),
            run_time=max(0.05, 1.28),
            rate_func=there_and_back
        )

        # Beat 3: small waveform + larger ghosted comparison
        self.wait(max(0.05, 0.80))

        small_wave = FunctionGraph(
            lambda x: 0.15 * np.sin(4 * x),
            x_range=[-1.6, 1.6, 0.01],
            color=TEAL, stroke_width=3
        ).scale_to_fit_width(3.4).move_to(np.array([-2.2, -0.6, 0]))

        ghost_large = FunctionGraph(
            lambda x: 1.0 * np.sin(4 * x),
            x_range=[-1.6, 1.6, 0.01],
            color=PURPLE, stroke_width=3
        ).scale_to_fit_width(3.4).move_to(np.array([2.2, -0.5, 0]))
        ghost_large.set_opacity(0.35)

        weaker_label = Text("weaker signal", font_size=26, color=WHITE)
        weaker_label.next_to(small_wave, DOWN, buff=0.2)

        self.play(
            FadeOut(source_glow),
            FadeOut(source_label),
            FadeOut(distance_arrow),
            FadeOut(distance_label),
            run_time=max(0.05, 0.5
        ))
        self.play(
            Create(small_wave),
            FadeIn(ghost_large),
            Write(weaker_label),
            run_time=max(0.05, 2.04
        ))

        # Beat 4: coarse spatial grid + more invasive comparison dimming
        grid_row = VGroup(*[
            Square(side_length=0.7, fill_color=BLUE, fill_opacity=0.6,
                   stroke_color=WHITE, stroke_width=1.5)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.15)
        grid_row.next_to(weaker_label, DOWN, buff=0.35)

        lower_res_label = Text("lower spatial resolution", font_size=24, color=WHITE)
        lower_res_label.next_to(grid_row, DOWN, buff=0.2)

        more_invasive_label = Text("more invasive electrodes", font_size=22, color=WHITE)
        more_invasive_label.next_to(ghost_large, UP, buff=0.25)

        self.play(
            FadeIn(grid_row),
            Write(lower_res_label),
            run_time=max(0.05, 1.2
        ))
        self.play(FadeIn(more_invasive_label), run_time=max(0.05, 0.8))
        self.play(
            ghost_large.animate.set_opacity(0.15),
            more_invasive_label.animate.set_opacity(0.30),
            run_time=max(0.05, 1.0
        ))
        self.wait(max(0.05, 2.36))

        # Beat 5: clear first segment, open two-column layout
        self.wait(max(0.05, 1.02))

        first_segment = VGroup(
            electrode, skin, small_wave, ghost_large,
            weaker_label, grid_row, lower_res_label,
            more_invasive_label
        )
        self.play(FadeOut(first_segment), run_time=max(0.05, 0.8))

        left_header = Text("Advantages", font_size=40, weight="BOLD", color=WHITE)
        left_header.move_to(np.array([-3.4, 2.4, 0]))

        right_header = Text("Limitations", font_size=40, weight="BOLD", color=GREY_B)
        right_header.set_opacity(0.5)
        right_header.move_to(np.array([3.4, 2.4, 0]))

        def make_card(text, icon_kind):
            if icon_kind == "check":
                icon = SVGMobject(
                    ASSET_PATHS["check_circle"],
                    color=GREEN, fill_color=GREEN, fill_opacity=1,
                    stroke_color=GREEN, stroke_width=0
                ).scale_to_fit_height(0.45)
            else:
                icon = SVGMobject(
                    ASSET_PATHS["x_circle"],
                    color=RED, fill_color=RED, fill_opacity=1,
                    stroke_color=RED, stroke_width=0
                ).scale_to_fit_height(0.45)

            label = Text(text, font_size=26, color=WHITE)
            content = VGroup(icon, label).arrange(RIGHT, buff=0.25)

            rect = Rectangle(
                width=4.9, height=0.9,
                fill_color=DARK_GREY, fill_opacity=0.9,
                stroke_color=GREY_B, stroke_width=2
            )
            card = VGroup(rect, content)
            content.move_to(rect.get_center())
            return card

        adv_texts = [
            "Non-invasive",
            "Comfortable",
            "Easy to apply",
            "Long-duration recordings"
        ]
        lim_texts = [
            "Lower signal amplitude",
            "Motion artifacts",
            "Lower spatial resolution"
        ]

        left_cards = [make_card(t, "check") for t in adv_texts]
        right_cards = [make_card(t, "x") for t in lim_texts]

        prev = left_header
        for card in left_cards:
            card.next_to(prev, DOWN, buff=0.35)
            prev = card

        prev = right_header
        for card in right_cards:
            card.next_to(prev, DOWN, buff=0.35)
            prev = card

        self.play(
            Write(left_header),
            FadeIn(right_header),
            FadeIn(left_cards[0]),
            run_time=max(0.05, 1.28
        ))

        # Beat 6: second advantage card
        self.wait(max(0.05, 0.80))
        self.play(FadeIn(left_cards[1], shift=UP * 0.3), run_time=max(0.05, 0.90))

        # Beat 7: third advantage card
        self.wait(max(0.05, 0.66))
        self.play(FadeIn(left_cards[2], shift=UP * 0.3), run_time=max(0.05, 0.74))

        # Beat 8: fourth advantage card
        self.wait(max(0.05, 0.50))
        self.play(FadeIn(left_cards[3], shift=UP * 0.3), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.28))

        # Beat 9: limitations header bright, first limitation card
        self.play(
            right_header.animate.set_color(WHITE).set_opacity(1),
            FadeIn(right_cards[0], shift=UP * 0.3),
            run_time=max(0.05, 1.6
        ))
        self.wait(max(0.05, 1.70))

        # Beat 10: second limitation card
        self.wait(max(0.05, 0.78))
        self.play(FadeIn(right_cards[1], shift=UP * 0.3), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 0.86))

        # Beat 11: third limitation card
        self.wait(max(0.05, 0.60))
        self.play(FadeIn(right_cards[2], shift=UP * 0.3), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 0.56))

        # Beat 12: faint small-vs-larger waveform at top
        small_top = FunctionGraph(
            lambda x: 0.10 * np.sin(4 * x),
            x_range=[-1.2, 1.2, 0.01],
            color=TEAL, stroke_width=2
        ).scale_to_fit_width(2.6).move_to(np.array([-2.0, 3.6, 0]))
        small_top.set_opacity(0.6)

        large_top = FunctionGraph(
            lambda x: 0.35 * np.sin(4 * x),
            x_range=[-1.2, 1.2, 0.01],
            color=PURPLE, stroke_width=2
        ).scale_to_fit_width(2.6).move_to(np.array([2.0, 3.6, 0]))
        large_top.set_opacity(0.35)

        self.play(FadeIn(small_top), FadeIn(large_top), run_time=max(0.05, 0.65))
        self.wait(max(0.05, 0.16))