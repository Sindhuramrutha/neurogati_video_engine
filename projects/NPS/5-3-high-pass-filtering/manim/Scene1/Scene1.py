ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Title
        title = Text("Learning Objectives", font_size=56, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.6)

        # Ellipsis placeholder
        ellipsis = Text("...", font_size=48, color=GREY_B)
        ellipsis.next_to(title, DOWN, buff=0.30)

        # Objectives
        objective_texts = [
            "Define a high-pass filter.",
            "Explain how a high-pass filter operates.",
            "Describe the role of cutoff frequency.",
            "Identify applications of high-pass filtering in neuroscience.",
            "Understand the advantages and limitations of high-pass filtering.",
        ]

        items = []
        for obj_text in objective_texts:
            bullet = Rectangle(
                width=0.26,
                height=0.26,
                fill_color=GREY_D,
                fill_opacity=1,
                stroke_color=GREY_B,
                stroke_width=2,
            )
            text = Text(obj_text, font_size=30, color=WHITE)
            item = VGroup(bullet, text).arrange(RIGHT, buff=0.25)
            items.append(item)

        checklist = VGroup(*items).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        checklist.next_to(title, DOWN, buff=1.1)

        item0, item1, item2, item3, item4 = items
        targets = [item.get_center().copy() for item in items]

        # Beat 1: 0.00-0.50 — title fades in
        self.play(FadeIn(title), run_time=max(0.05, 0.50))

        # Beat 2: 0.50-2.04 — title only
        self.wait(max(0.05, 1.54))

        # Beat 3: 2.04-2.80 — ellipsis fades in
        self.play(FadeIn(ellipsis), run_time=max(0.05, 0.76))

        # Beat 4: 2.80-4.52 — first objective slides in from left, ellipsis fades out
        item0.move_to(targets[0]).shift(LEFT * 10)
        self.add(item0)
        self.play(
            item0.animate.move_to(targets[0]),
            FadeOut(ellipsis),
            run_time=max(0.05, 1.72),
        )

        # 4.52-5.22 — hold
        self.wait(max(0.05, 0.70))

        # Beat 5: 5.22-7.30 — second objective slides in, first dims to half
        item1.move_to(targets[1]).shift(LEFT * 10)
        self.add(item1)
        self.play(
            item1.animate.move_to(targets[1]),
            item0.animate.set_opacity(0.5),
            run_time=max(0.05, 2.08),
        )

        # 7.30-8.06 — hold
        self.wait(max(0.05, 0.76))

        # Beat 6: 8.06-9.84 — third objective slides in, previous two dim further
        item2.move_to(targets[2]).shift(LEFT * 10)
        self.add(item2)
        self.play(
            item2.animate.move_to(targets[2]),
            item0.animate.set_opacity(0.3),
            item1.animate.set_opacity(0.5),
            run_time=max(0.05, 1.78),
        )

        # 9.84-10.92 — hold
        self.wait(max(0.05, 1.08))

        # Beat 7: 10.92-13.72 — fourth objective slides in, previous three remain dimmed
        item3.move_to(targets[3]).shift(LEFT * 10)
        self.add(item3)
        self.play(
            item3.animate.move_to(targets[3]),
            item0.animate.set_opacity(0.2),
            item1.animate.set_opacity(0.3),
            item2.animate.set_opacity(0.5),
            run_time=max(0.05, 2.80),
        )

        # 13.72-14.76 — hold
        self.wait(max(0.05, 1.04))

        # Beat 8: 14.76-18.04 — fifth objective slides in, fourth dims slightly
        item4.move_to(targets[4]).shift(LEFT * 10)
        self.add(item4)
        self.play(
            item4.animate.move_to(targets[4]),
            item3.animate.set_opacity(0.7),
            run_time=max(0.05, 3.28),
        )

        # Beat 9: 18.04-18.77 — equalize to full brightness, then fade out
        self.play(
            item0.animate.set_opacity(1),
            item1.animate.set_opacity(1),
            item2.animate.set_opacity(1),
            item3.animate.set_opacity(1),
            item4.animate.set_opacity(1),
            run_time=max(0.05, 0.25),
        )
        self.play(
            FadeOut(title),
            FadeOut(item0),
            FadeOut(item1),
            FadeOut(item2),
            FadeOut(item3),
            FadeOut(item4),
            run_time=max(0.05, 0.48),
        )