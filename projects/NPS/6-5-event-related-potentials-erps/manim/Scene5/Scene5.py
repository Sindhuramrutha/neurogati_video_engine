ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 1. Title fades in near top center
        title = Text("ERP ANALYSIS", font_size=36, color=WHITE, weight="BOLD")
        title.to_edge(UP, buff=0.55)
        self.play(FadeIn(title, run_time=max(0.05, 2.92)))

        # Final position/scale for the shifted title
        title_final = title.copy().scale(0.78).to_edge(UP, buff=0.18)
        subtitle = Text("provides several important advantages", font_size=20, color=GREY_B)
        subtitle.next_to(title_final, DOWN, buff=0.12)

        # Build the four empty list slots
        rows = VGroup()
        row_lines = []
        for _ in range(4):
            checkbox = Square(side_length=0.26, color=WHITE, stroke_width=2.5, fill_opacity=0)
            line = Line(LEFT * 3.1, RIGHT * 3.1, color=GREY_B, stroke_width=3)
            row = VGroup(checkbox, line).arrange(RIGHT, buff=0.4)
            rows.add(row)
            row_lines.append(line)

        rows.arrange(DOWN, buff=0.8)
        rows.next_to(subtitle, DOWN, buff=0.4)

        # 2. Title shifts upward/shrinks; subtitle and slots appear
        self.play(
            title.animate.scale(0.78).to_edge(UP, buff=0.18),
            FadeIn(subtitle),
            FadeIn(rows),
            run_time=max(0.05, 1.4),
        )

        # Item texts
        item_texts = [
            Text("Excellent temporal resolution", color=WHITE, font_size=26),
            Text("Direct measurement of stimulus-related neural activity", color=WHITE, font_size=26),
            Text("Widely used in cognitive neuroscience", color=WHITE, font_size=26),
            Text("Relatively simple experimental design", color=WHITE, font_size=26),
        ]

        for txt in item_texts:
            if txt.width > 6.0:
                txt.scale_to_fit_width(6.0)

        for i, txt in enumerate(item_texts):
            txt.next_to(rows[i][0], RIGHT, buff=0.45, aligned_edge=LEFT)

        # Checkmarks
        checkmarks = []
        for i in range(4):
            checkbox = rows[i][0]
            center = checkbox.get_center()
            p1 = center + np.array([-0.10, -0.04, 0.0])
            p2 = center + np.array([-0.02, 0.05, 0.0])
            p3 = center + np.array([0.12, -0.08, 0.0])
            check = VGroup(
                Line(p1, p2, color=GREEN, stroke_width=5),
                Line(p2, p3, color=GREEN, stroke_width=5),
            )
            checkmarks.append(check)

        # 3. Item 1
        self.play(
            AddTextLetterByLetter(item_texts[0]),
            FadeOut(row_lines[0]),
            run_time=max(0.05, 0.94),
        )
        self.play(Create(checkmarks[0], run_time=max(0.05, 0.40)))
        self.wait(max(0.05, 0.60))

        # 4. Item 2
        self.play(
            AddTextLetterByLetter(item_texts[1]),
            FadeOut(row_lines[1]),
            run_time=max(0.05, 2.32),
        )
        self.play(Create(checkmarks[1], run_time=max(0.05, 0.40)))
        self.wait(max(0.05, 0.54))

        # 5. Item 3
        self.play(
            AddTextLetterByLetter(item_texts[2]),
            FadeOut(row_lines[2]),
            run_time=max(0.05, 1.56),
        )
        self.play(Create(checkmarks[2], run_time=max(0.05, 0.40)))
        self.wait(max(0.05, 0.66))

        # 6. Item 4
        self.play(
            AddTextLetterByLetter(item_texts[3]),
            FadeOut(row_lines[3]),
            run_time=max(0.05, 1.94),
        )
        self.play(Create(checkmarks[3], run_time=max(0.05, 0.40)))

        # 7. Completed list holds; very subtle settle only
        completed_list = VGroup(rows, *item_texts, *checkmarks)
        self.play(completed_list.animate.shift(DOWN * 0.015), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.52))