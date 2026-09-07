ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png', 'pptx_demystifying-the-brain-chapter-1_slide_04': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\slide_04.png'}

import numpy as np
from manim import *

class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        slide = ImageMobject(ASSET_PATHS["pptx_demystifying-the-brain-chapter-1_slide_04"])
        slide.scale_to_fit_width(config.frame_width)
        slide.move_to(ORIGIN)
        self.add(slide)

        self.wait(max(0.05, 0.96))

        self._highlight_rectangle(7.76, 0.87, [-2.65, 3.14, 0], 3.76)
        self._highlight_rectangle(6.41, 1.52, [-3.33, 1.70, 0], 15.54)
        self._highlight_arrow(
            (-4.869386042317709, -0.9426509257812501, 0),
            [-4.87, 0.46, 0],
            1.80,
        )
        self._highlight_rectangle(5.89, 1.20, [-3.29, -0.38, 0], 11.28)
        self._highlight_arrow(
            (-4.869386042317709, -0.26197917107638924, 0),
            [-4.87, -1.66, 0],
            1.68,
        )
        self._highlight_rectangle(5.89, 1.20, [-3.29, -2.50, 0], 11.03)

    def _highlight_rectangle(self, width, height, pos, duration):
        rect = Rectangle(
            width=width,
            height=height,
            color=YELLOW,
            stroke_width=5,
            fill_opacity=0,
        )
        rect.move_to(np.array(pos))
        self.play(Create(rect), run_time=max(0.05, duration - 0.5))
        self.play(FadeOut(rect), run_time=max(0.05, 0.5))

    def _highlight_arrow(self, start, end, duration):
        arrow = Arrow(
            start=np.array(start),
            end=np.array(end),
            color=YELLOW,
            stroke_width=6,
            buff=0.1,
        )
        self.play(Create(arrow), run_time=max(0.05, duration - 0.5))
        self.play(FadeOut(arrow), run_time=max(0.05, 0.5))