ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png', 'pptx_demystifying-the-brain-chapter-1_slide_03': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\slide_03.png'}

from manim import *
import numpy as np

class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        slide = ImageMobject(ASSET_PATHS["pptx_demystifying-the-brain-chapter-1_slide_03"])
        slide.scale_to_fit_width(config.frame_width)
        slide.move_to(ORIGIN)
        self.add(slide)
        self.wait(max(0.05, 2.14))

        def show_highlight(mobject, total_duration, create_run=1.5, fade_run=0.8):
            self.play(Create(mobject), run_time=max(0.05, create_run))
            wait_time = total_duration - create_run - fade_run
            self.wait(max(0.05, wait_time))
            self.play(FadeOut(mobject), run_time=max(0.05, fade_run))

        rect1 = Rectangle(width=7.60, height=0.94, color=YELLOW, stroke_width=5, fill_opacity=0)
        rect1.move_to(np.array([2.67, 1.36, 0]))
        show_highlight(rect1, 6.24)

        ellipse1 = Ellipse(width=3.73, height=0.58, color=YELLOW, stroke_width=5, fill_opacity=0)
        ellipse1.move_to(np.array([0.96, 0.36, 0]))
        show_highlight(ellipse1, 7.08)

        rect2 = Rectangle(width=7.15, height=1.29, color=YELLOW, stroke_width=5, fill_opacity=0)
        rect2.move_to(np.array([2.67, -0.46, 0]))
        show_highlight(rect2, 10.62)

        ellipse2 = Ellipse(width=2.97, height=0.58, color=YELLOW, stroke_width=5, fill_opacity=0)
        ellipse2.move_to(np.array([0.58, -1.83, 0]))
        show_highlight(ellipse2, 5.10)

        rect3 = Rectangle(width=7.15, height=1.29, color=YELLOW, stroke_width=5, fill_opacity=0)
        rect3.move_to(np.array([2.67, -2.65, 0]))
        show_highlight(rect3, 10.17)