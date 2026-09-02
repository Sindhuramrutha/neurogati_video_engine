ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        heading = Text("Learning Objectives", font_size=56, weight="BOLD", color=WHITE)
        heading.to_edge(UP, buff=0.6)

        bullet_texts = [
            "Define stationary and nonstationary signals",
            "Explain why neural signals are nonstationary",
            "Identify causes of time-varying neural activity",
            "Understand why specialised analysis is needed",
        ]

        bullet_items = []
        for text in bullet_texts:
            text_mob = Text(text, font_size=36, color=WHITE, weight="NORMAL")
            if text_mob.width > 9.0:
                text_mob.scale_to_fit_width(9.0)
            dot_mob = Dot(radius=0.07, color=YELLOW, fill_opacity=1)
            item = VGroup(dot_mob, text_mob).arrange(RIGHT, buff=0.28)
            bullet_items.append(item)

        bullet_group = VGroup(*bullet_items).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        first_text = bullet_items[0][1]
        offset_x = first_text.get_left()[0] - bullet_group.get_left()[0]
        bullet_group.align_to(heading, LEFT)
        bullet_group.shift(LEFT * offset_x)

        top_y = heading.get_bottom()[1] - 0.9
        bullet_group.move_to(np.array([
            bullet_group.get_center()[0],
            top_y - bullet_group.height / 2,
            0.0
        ]))

        b1, b2, b3, b4 = bullet_items

        # 0.00 - 2.06
        self.play(FadeIn(heading), run_time=max(0.05, 1.48))
        self.wait(max(0.05, 2.06 - 1.48))

        # 2.06 - 3.54
        self.wait(max(0.05, 1.48))

        # 3.54 - 6.06
        self.play(FadeIn(b1), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 2.52 - 1.2))

        # 6.06 - 10.24
        self.play(FadeIn(b2), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 4.18 - 1.5))

        # 10.24 - 14.04
        self.play(FadeIn(b3), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 3.80 - 1.5))

        # 14.04 - 19.16
        self.play(FadeIn(b4), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 5.12 - 1.5))

        # 19.16 - 20.00
        self.wait(max(0.05, 0.30))
        self.play(FadeOut(heading, *bullet_items), run_time=max(0.05, 0.54))