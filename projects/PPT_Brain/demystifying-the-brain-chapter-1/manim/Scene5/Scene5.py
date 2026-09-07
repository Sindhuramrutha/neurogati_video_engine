ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png', 'pptx_demystifying-the-brain-chapter-1_slide_05': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\slide_05.png'}

import numpy as np
from manim import *


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 1. Slide background image, static and fully visible for the whole scene.
        slide = ImageMobject(ASSET_PATHS["pptx_demystifying-the-brain-chapter-1_slide_05"])
        slide.scale_to_fit_width(config.frame_width)
        slide.move_to(ORIGIN)
        self.add(slide)

        # 0.00-6.20: only the slide is shown.
        self.wait(max(0.05, 6.2))

        # 2. 6.20-20.64: highlight Leonardo da Vinci / ventricles region.
        rect1 = Rectangle(
            width=6.37,
            height=1.24,
            color=YELLOW,
            stroke_width=5,
            fill_opacity=0,
        )
        rect1.move_to(np.array([3.33, 0.56, 0]))
        self.play(Create(rect1), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 12.84))
        self.play(FadeOut(rect1), run_time=max(0.05, 0.6))

        # 3. 20.64-41.50: highlight Descartes / dualism region.
        rect2 = Rectangle(
            width=6.37,
            height=1.90,
            color=YELLOW,
            stroke_width=5,
            fill_opacity=0,
        )
        rect2.move_to(np.array([3.33, -1.52, 0]))
        self.play(Create(rect2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 18.86))
        self.play(FadeOut(rect2), run_time=max(0.05, 1.0))