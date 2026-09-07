ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png', 'pptx_demystifying-the-brain-chapter-1_slide_01': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\slide_01.png'}

import numpy as np
from manim import *


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Slide background: static for the whole scene
        slide = ImageMobject(
            ASSET_PATHS["pptx_demystifying-the-brain-chapter-1_slide_01"]
        )
        slide.scale_to_fit_width(config.frame_width)
        slide.move_to(ORIGIN)
        self.add(slide)

        # 0.00 - 1.70: slide only
        self.wait(max(0.05, 1.70))

        # 1.70 - 21.20: 'Demystifying the Brain'
        rect = (
            Rectangle(
                width=4.91,
                height=0.78,
                color=YELLOW,
                stroke_width=5,
                fill_opacity=0,
            )
            .move_to(np.array([-4.17, 3.25, 0]))
        )
        self.play(Create(rect), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 17.5))
        self.play(FadeOut(rect), run_time=max(0.05, 0.5))

        # 21.20 - 27.90: 'Cognitive Complexity'
        ellipse1 = (
            Ellipse(
                width=2.42,
                height=0.51,
                color=YELLOW,
                stroke_width=5,
                fill_opacity=0,
            )
            .move_to(np.array([-1.18, -0.04, 0]))
        )
        self.play(Create(ellipse1), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 4.9))
        self.play(FadeOut(ellipse1), run_time=max(0.05, 0.6))

        # 27.90 - 34.62: 'Technological Integration'
        ellipse2 = (
            Ellipse(
                width=2.83,
                height=0.51,
                color=YELLOW,
                stroke_width=5,
                fill_opacity=0,
            )
            .move_to(np.array([-0.97, -2.28, 0]))
        )
        self.play(Create(ellipse2), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 4.92))
        self.play(FadeOut(ellipse2), run_time=max(0.05, 0.6))