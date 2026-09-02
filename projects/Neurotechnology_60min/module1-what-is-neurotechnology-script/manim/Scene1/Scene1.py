ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png', 'eeg_device': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\eeg.svg', 'mri_scan': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\mri.svg', 'robotic_arm': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\robotic_arm.svg', 'electrode_pads': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\electrodes.svg', 'wheelchair': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\wheelchair.svg', 'xray_scan': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\xray.svg', 'smartwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\smartwatch.svg', 'nerve_cell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\nerve.svg'}

from manim import *
import numpy as np

class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        objectives = [
            ("Define neurotechnology and\nexplain the different ways technology\ncan interact with the nervous system", WHITE),
            ("Understand the nervous system from\nelectrical, chemical, and computational\nperspectives", WHITE),
            ("Describe the basic pathway from\nneural activity to a technological output", WHITE),
            ("Distinguish between recording,\ndecoding, and modulation", WHITE),
            ("Understand the difference between\nreading from the nervous system and\ninfluencing or writing to it", WHITE),
            ("Recognize how these ideas connect\nthe different technologies covered\nin the rest of the course", ORANGE),
        ]

        rows = []
        texts = []
        placeholders = []

        for text, color in objectives:
            text_mob = Text(text, font_size=19, color=color, line_spacing=0.6)
            ph = self.make_checkmark(GREEN, opacity=0.25)
            row = VGroup(ph, text_mob).arrange(RIGHT, buff=0.25)
            rows.append(row)
            texts.append(text_mob)
            placeholders.append(ph)

        checklist = VGroup(*rows).arrange(DOWN, buff=0.20).move_to(ORIGIN)
        scale_factor = min(6.8 / checklist.height, 12.0 / checklist.width, 1.0)
        if scale_factor < 1.0:
            checklist.scale(scale_factor)

        draws = []
        for ph in placeholders:
            draw = self.make_checkmark(GREEN, opacity=1.0).scale(scale_factor)
            draw.move_to(ph.get_center())
            draws.append(draw)

        soft_glow = SurroundingRectangle(
            texts[5],
            color=ORANGE,
            buff=0.18,
            corner_radius=0.1,
            stroke_width=1.5,
            stroke_opacity=0.35,
            fill_color=ORANGE,
            fill_opacity=0.06,
        )
        soft_glow.set_z_index(-1)

        # Beat 1: 0.00 - 2.50
        self.play(FadeIn(rows[0]), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.3))
        self.wait(max(0.05, 0.76))  # gap to 3.26

        # Beat 2: 3.26 - 8.54
        self.play(texts[0].animate.set_color(GOLD), run_time=max(0.05, 0.6))
        self.play(FadeOut(placeholders[0]), run_time=max(0.05, 0.5))
        self.play(Create(draws[0][0]), run_time=max(0.05, 1.0))
        self.play(Create(draws[0][1]), run_time=max(0.05, 1.0))
        self.play(Indicate(rows[0], color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.7))
        self.play(texts[0].animate.set_color(WHITE), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 1.08))
        self.wait(max(0.05, 0.70))  # gap to 9.24

        # Beat 3: 9.24 - 13.80
        self.play(FadeIn(rows[1]), run_time=max(0.05, 0.8))
        self.play(FadeOut(placeholders[1]), run_time=max(0.05, 0.5))
        self.play(Create(draws[1][0]), run_time=max(0.05, 0.8))
        self.play(Create(draws[1][1]), run_time=max(0.05, 0.8))
        self.play(Indicate(rows[1], color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.06))
        self.wait(max(0.05, 0.98))  # gap to 14.78

        # Beat 4: 14.78 - 19.14
        self.play(FadeIn(rows[2]), run_time=max(0.05, 0.8))
        self.play(FadeOut(placeholders[2]), run_time=max(0.05, 0.5))
        self.play(Create(draws[2][0]), run_time=max(0.05, 0.8))
        self.play(Create(draws[2][1]), run_time=max(0.05, 0.8))
        self.play(Indicate(rows[2], color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.86))
        self.wait(max(0.05, 0.86))  # gap to 20.00

        # Beat 5: 20.00 - 23.00
        self.play(FadeIn(rows[3]), run_time=max(0.05, 0.6))
        self.play(FadeOut(placeholders[3]), run_time=max(0.05, 0.4))
        self.play(Create(draws[3][0]), run_time=max(0.05, 0.6))
        self.play(Create(draws[3][1]), run_time=max(0.05, 0.6))
        self.play(Indicate(rows[3], color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.30))
        self.wait(max(0.05, 0.94))  # gap to 23.94

        # Beat 6: 23.94 - 29.90
        self.play(FadeIn(rows[4]), run_time=max(0.05, 0.8))
        self.play(FadeOut(placeholders[4]), run_time=max(0.05, 0.5))
        self.play(Create(draws[4][0]), run_time=max(0.05, 0.9))
        self.play(Create(draws[4][1]), run_time=max(0.05, 0.9))
        self.play(Indicate(rows[4], color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 2.16))
        self.wait(max(0.05, 0.58))  # gap to 30.48

        # Beat 7: 30.48 - 36.17
        self.play(FadeIn(rows[5]), run_time=max(0.05, 0.8))
        self.play(FadeOut(placeholders[5]), run_time=max(0.05, 0.5))
        self.play(Create(draws[5][0]), run_time=max(0.05, 0.9))
        self.play(Create(draws[5][1]), run_time=max(0.05, 0.9))
        self.play(
            FadeIn(soft_glow),
            Indicate(rows[5], color=ORANGE, scale_factor=1.05),
            run_time=max(0.05, 0.8),
        )
        self.play(soft_glow.animate.scale(1.03), run_time=max(0.05, 0.6))
        self.play(soft_glow.animate.scale(1 / 1.03), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.59))

    def make_checkmark(self, color=GREEN, opacity=1.0):
        bottom = np.array([-0.22, -0.18, 0.0])
        middle = np.array([0.0, 0.04, 0.0])
        top = np.array([0.28, 0.22, 0.0])
        line1 = Line(bottom, middle, color=color, stroke_width=5, stroke_opacity=opacity)
        line2 = Line(middle, top, color=color, stroke_width=5, stroke_opacity=opacity)
        return VGroup(line1, line2)