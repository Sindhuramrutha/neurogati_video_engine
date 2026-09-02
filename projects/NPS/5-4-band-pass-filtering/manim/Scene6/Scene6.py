ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\test_heart.svg',
    'brain': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\brain_test.svg',
    'stopwatch': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\stopwatch.svg',
    'activity': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\activity.svg',
    'soundwave': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\soundwave.svg',
    'grid_matrix': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\grid-3x3-gap-fill.svg',
    'bar_chart': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\bar-chart.svg',
    'graph_trend': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\graph-up-arrow.svg',
    'cpu': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\cpu.svg',
    'funnel': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\funnel.svg',
    'table': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\table.svg',
    'hospital': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\hospital.svg',
    'capsule': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\capsule.svg',
    'clipboard_pulse': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\clipboard2-pulse.svg',
    'hand': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\hand-index-thumb.svg',
    'broadcast': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\broadcast-pin.svg',
    'gear': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\gear.svg',
    'arrow_repeat': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\arrow-repeat.svg',
    'lightbulb': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\lightbulb.svg',
    'bell': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\bell.svg',
    'check_circle': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\check-circle.svg',
    'x_circle': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\x-circle.svg',
    'rulers': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\rulers.svg',
    'puzzle': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\puzzle.svg',
    'fig_measurement_funnel': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\fig_mindmap_full.png',
}


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Beat 1: Title (0.00 - 4.34) ---
        title = Text("Advantages", font_size=48, color=WHITE, weight="BOLD")
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 4.34 - 0.8))

        # --- Bullet text data ---
        bullets = [
            "Removes low‑frequency and high‑frequency interference",
            "Improves signal‑to‑noise ratio",
            "Preserves only the relevant frequency range",
            "Widely applicable across neural recording modalities",
        ]

        # --- Tick mark icon (reusable template) ---
        tick = SVGMobject(
            ASSET_PATHS["check_circle"],
            fill_color=GREEN,
            fill_opacity=1,
            stroke_color=GREEN,
            stroke_width=0,
        ).scale_to_fit_height(0.45)

        # --- Beat 2: Bullet 1 (4.34 - 8.30), duration = 3.96 ---
        bullet1 = Text(bullets[0], font_size=28, color=WHITE)
        tick1 = tick.copy()
        row1 = VGroup(tick1, bullet1).arrange(RIGHT, buff=0.3)
        row1.next_to(title, DOWN, buff=0.7)
        row1.shift(LEFT * 0.5)  # nudge left for visual balance
        # Entrance: slide in from off-screen left
        row1.move_to(LEFT * 9 + row1.get_y() * UP)
        self.play(row1.animate.move_to(np.array([-0.5, row1.get_y(), 0])), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 8.30 - 4.34 - 1.5))

        # --- Beat 3: Bullet 2 (8.30 - 10.88), duration = 2.58 ---
        bullet2 = Text(bullets[1], font_size=28, color=WHITE)
        tick2 = tick.copy()
        row2 = VGroup(tick2, bullet2).arrange(RIGHT, buff=0.3)
        row2.next_to(row1, DOWN, buff=0.55, aligned_edge=LEFT)
        row2.move_to(LEFT * 9 + row2.get_y() * UP)
        self.play(row2.animate.move_to(row1.get_left() + DOWN * 0.55), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 10.88 - 8.30 - 1.2))

        # --- Beat 4: Bullet 3 (10.88 - 14.84), duration = 3.96 ---
        bullet3 = Text(bullets[2], font_size=28, color=WHITE)
        tick3 = tick.copy()
        row3 = VGroup(tick3, bullet3).arrange(RIGHT, buff=0.3)
        row3.next_to(row2, DOWN, buff=0.55, aligned_edge=LEFT)
        row3.move_to(LEFT * 9 + row3.get_y() * UP)
        self.play(row3.animate.move_to(row2.get_left() + DOWN * 0.55), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 14.84 - 10.88 - 1.5))

        # --- Beat 5: Bullet 4 (14.84 - 19.27), duration = 4.43 ---
        bullet4 = Text(bullets[3], font_size=28, color=WHITE)
        tick4 = tick.copy()
        row4 = VGroup(tick4, bullet4).arrange(RIGHT, buff=0.3)
        row4.next_to(row3, DOWN, buff=0.55, aligned_edge=LEFT)
        row4.move_to(LEFT * 9 + row4.get_y() * UP)
        self.play(row4.animate.move_to(row3.get_left() + DOWN * 0.55), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 19.27 - 14.84 - 1.5))