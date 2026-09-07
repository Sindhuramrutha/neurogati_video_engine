ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Layout ----------------------------------------------------------
        STAGE_LABELS = [
            "Biological Source",
            "Electrode/Sensor",
            "Amplifier",
            "Filter",
            "Analog-to-Digital Converter",
            "Computer",
        ]
        STAGE_COLORS = [BLUE, TEAL, GREEN, ORANGE, PURPLE, PINK]
        slot_centers = [np.array([-5.5 + i * 2.2, 0.0, 0.0]) for i in range(6)]
        box_w = 1.85
        box_h = 1.15

        # Guide line across the middle.
        guide_line = Line(LEFT * 6.8, RIGHT * 6.8, color=GREY_B, stroke_width=1.5)
        guide_line.set_opacity(0.5)

        # Six dim placeholder rectangles.
        slot_rects = []
        for center in slot_centers:
            rect = Rectangle(
                width=box_w,
                height=box_h,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_color=GREY,
                fill_opacity=0.10,
            )
            rect.move_to(center)
            slot_rects.append(rect)
        slot_group = VGroup(*slot_rects)

        # Small arrows between adjacent slots.
        arrows = VGroup()
        for i in range(5):
            start = slot_rects[i].get_right() + RIGHT * 0.03
            end = slot_rects[i + 1].get_left() + LEFT * 0.03
            arrow = Arrow(
                start=start,
                end=end,
                buff=0,
                color=GREY_B,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.35,
            )
            arrow.set_stroke(opacity=0.65)
            arrows.add(arrow)

        # ---- Beat 1: 0.00-2.82 ----------------------------------------------
        self.play(Create(guide_line), run_time=max(0.05, 0.8))
        self.play(FadeIn(slot_group), FadeIn(arrows), run_time=max(0.05, 2.02))

        # ---- Beat 2: 2.82-5.56 ----------------------------------------------
        title = Text("The Acquisition Chain", font_size=46, color=WHITE, weight="BOLD")
        title.move_to([0, 2.2, 0])
        self.play(FadeIn(title), run_time=max(0.05, 1.28))

        seq_pulse_time = 1.46
        per_slot = seq_pulse_time / 6.0
        for i in range(6):
            self.play(
                slot_rects[i].animate.set_stroke(YELLOW, width=4),
                rate_func=rate_functions.there_and_back,
                run_time=max(0.05, per_slot),
            )

        # ---- Beat 3: 5.56-9.18 ----------------------------------------------
        bio_text = Text("biological activity", font_size=26, color=GREY_B)
        small_arrow = Arrow(
            start=LEFT * 0.25,
            end=RIGHT * 0.25,
            buff=0,
            color=GREY_B,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.35,
        )
        small_arrow.set_stroke(opacity=0.7)
        data_text = Text("digital data", font_size=26, color=GREY_B)
        label_strip = VGroup(bio_text, small_arrow, data_text).arrange(RIGHT, buff=0.3)
        label_strip.move_to([0, -1.2, 0])

        self.play(FadeIn(label_strip), run_time=max(0.05, 2.98))
        self.wait(max(0.05, 0.64))

        # ---- Beat 4: 9.18-15.34 ---------------------------------------------
        note = Text("Different sensors, same workflow.", font_size=32, color=WHITE, weight="BOLD")
        note.move_to([0, 2.2, 0])

        self.play(FadeOut(title), FadeOut(label_strip), run_time=max(0.05, 1.2))
        self.play(FadeIn(note), run_time=max(0.05, 1.3))
        self.wait(max(0.05, 3.66))

        # Pre-build stage labels, scaled to fit inside the boxes.
        labels = []
        for i, label_text in enumerate(STAGE_LABELS):
            txt = Text(label_text, font_size=20, color=WHITE, weight="BOLD")
            if txt.width > box_w - 0.3:
                txt.scale_to_fit_width(box_w - 0.3)
            txt.move_to(slot_centers[i])
            labels.append(txt)

        # ---- Beat 5: 15.34-16.42 --------------------------------------------
        self.play(
            FadeOut(note),
            slot_rects[0].animate.scale(1.12).set_fill(BLUE, opacity=0.55).set_stroke(WHITE, width=5),
            run_time=max(0.05, 0.40),
        )
        self.play(
            slot_rects[0].animate.scale(1 / 1.12).set_fill(BLUE, opacity=0.30).set_stroke(WHITE, width=3),
            Write(labels[0]),
            run_time=max(0.05, 0.68),
        )

        # ---- Beat 6: 16.42-17.74 --------------------------------------------
        self.play(
            slot_rects[0].animate.set_fill(BLUE, opacity=0.55).set_stroke(YELLOW, width=5),
            rate_func=rate_functions.there_and_back,
            run_time=max(0.05, 1.32),
        )

        # ---- Beat 7: 17.74-18.80 --------------------------------------------
        self.play(
            slot_rects[1].animate.scale(1.12).set_fill(TEAL, opacity=0.55).set_stroke(WHITE, width=5),
            run_time=max(0.05, 0.40),
        )
        self.play(
            slot_rects[1].animate.scale(1 / 1.12).set_fill(TEAL, opacity=0.30).set_stroke(WHITE, width=3),
            Write(labels[1]),
            slot_rects[0].animate.set_fill(BLUE, opacity=0.25).set_stroke(WHITE, width=3),
            run_time=max(0.05, 0.66),
        )

        self.wait(max(0.05, 0.62))

        # ---- Beat 8: 19.42-20.06 --------------------------------------------
        self.play(
            slot_rects[2].animate.scale(1.12).set_fill(GREEN, opacity=0.55).set_stroke(WHITE, width=5),
            run_time=max(0.05, 0.24),
        )
        self.play(
            slot_rects[2].animate.scale(1 / 1.12).set_fill(GREEN, opacity=0.30).set_stroke(WHITE, width=3),
            Write(labels[2]),
            run_time=max(0.05, 0.40),
        )

        self.wait(max(0.05, 0.44))

        # ---- Beat 9: 20.50-21.30 --------------------------------------------
        self.play(
            slot_rects[3].animate.scale(1.12).set_fill(ORANGE, opacity=0.55).set_stroke(WHITE, width=5),
            run_time=max(0.05, 0.30),
        )
        self.play(
            slot_rects[3].animate.scale(1 / 1.12).set_fill(ORANGE, opacity=0.30).set_stroke(WHITE, width=3),
            Write(labels[3]),
            run_time=max(0.05, 0.50),
        )

        self.wait(max(0.05, 0.20))

        # ---- Beat 10: 21.50-23.20 -------------------------------------------
        self.play(
            slot_rects[4].animate.scale(1.12).set_fill(PURPLE, opacity=0.55).set_stroke(WHITE, width=5),
            run_time=max(0.05, 0.60),
        )
        self.play(
            slot_rects[4].animate.scale(1 / 1.12).set_fill(PURPLE, opacity=0.30).set_stroke(WHITE, width=3),
            Write(labels[4]),
            run_time=max(0.05, 1.10),
        )

        self.wait(max(0.05, 0.20))

        # ---- Beat 11: 23.40-24.50 -------------------------------------------
        self.play(
            slot_rects[5].animate.scale(1.12).set_fill(PINK, opacity=0.55).set_stroke(WHITE, width=5),
            run_time=max(0.05, 0.40),
        )
        self.play(
            slot_rects[5].animate.scale(1 / 1.12).set_fill(PINK, opacity=0.30).set_stroke(WHITE, width=3),
            Write(labels[5]),
            run_time=max(0.05, 0.70),
        )

        # ---- Beat 12: 24.50-27.92 -------------------------------------------
        highlight_per = 0.40
        for i in range(6):
            self.play(
                slot_rects[i].animate.set_stroke(YELLOW, width=6).set_fill(STAGE_COLORS[i], opacity=0.55),
                rate_func=rate_functions.there_and_back,
                run_time=max(0.05, highlight_per),
            )

        caption = Text("Specific function per stage.", font_size=28, color=WHITE)
        caption.move_to([0, -2.0, 0])
        self.play(FadeIn(caption), run_time=max(0.05, 1.02))

        # ---- Beat 13: 27.92-33.88 -------------------------------------------
        self.play(
            *[
                slot_rects[i].animate.set_stroke(YELLOW, width=5).set_fill(STAGE_COLORS[i], opacity=0.55)
                for i in range(6)
            ],
            rate_func=rate_functions.there_and_back,
            run_time=max(0.05, 2.0),
        )

        quality_caption = Text("Quality depends on every stage.", font_size=28, color=YELLOW)
        quality_caption.move_to(caption.get_center())
        self.play(Transform(caption, quality_caption), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.32))
        self.wait(max(0.05, 1.14))  # gap before failure beat

        # ---- Beat 14: 33.88-36.50 -------------------------------------------
        fail_caption = Text("If one stage fails, the whole recording suffers.", font_size=28, color=RED)
        fail_caption.move_to(caption.get_center())

        warning_x = Text("×", font_size=40, color=RED, weight="BOLD")
        warning_x.next_to(slot_rects[3], UP, buff=0.15)

        self.play(
            slot_rects[3].animate.set_fill(RED, opacity=0.50).set_stroke(RED, width=4),
            FadeIn(warning_x),
            Transform(caption, fail_caption),
            run_time=max(0.05, 2.62),
        )

        # ---- Beat 15: 36.50-37.35 -------------------------------------------
        self.wait(max(0.05, 0.85))