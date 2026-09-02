ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helper: drawn checkmark (stroke only) ----------
        def make_checkmark(color=GREEN, stroke_width=5):
            return VGroup(
                Line(
                    np.array([-0.14, -0.05, 0]),
                    np.array([-0.02, 0.12, 0]),
                    color=color,
                    stroke_width=stroke_width,
                ),
                Line(
                    np.array([-0.02, 0.12, 0]),
                    np.array([0.18, -0.16, 0]),
                    color=color,
                    stroke_width=stroke_width,
                ),
            )

        # ---------- heading ----------
        heading = Text("Learning Objectives", font_size=56, color=WHITE)
        heading.move_to(np.array([0, 2.7, 0]))

        # ---------- bullet text mobjects ----------
        bullet_font = 28
        b1_text = Text(
            "Explain why neural signals require amplification.",
            font_size=bullet_font,
            color=WHITE,
        )
        b2_text = Text(
            "Describe the function of an amplifier.",
            font_size=bullet_font,
            color=WHITE,
        )
        b3_text = Text(
            "Understand the concept of signal conditioning.",
            font_size=bullet_font,
            color=WHITE,
        )
        part1_text = Text(
            "Explain why amplification must occur",
            font_size=bullet_font,
            color=WHITE,
        )
        part2_text = Text(
            " before further signal processing.",
            font_size=bullet_font,
            color=WHITE,
        )

        # Keep long lines within the frame.
        max_bullet_width = max(
            b1_text.width,
            b2_text.width,
            b3_text.width,
            part1_text.width + part2_text.width,
        )
        if max_bullet_width > 9.4:
            scale_factor = 9.4 / max_bullet_width
            for t in (b1_text, b2_text, b3_text, part1_text, part2_text):
                t.scale(scale_factor)

        max_bullet_width = max(
            b1_text.width,
            b2_text.width,
            b3_text.width,
            part1_text.width + part2_text.width,
        )
        left_x = -max_bullet_width / 2

        y1 = 1.6
        y2 = 0.6
        y3 = -0.4
        y4 = -1.4

        # ---------- final positions and checkmarks ----------
        # bullet 1
        b1_final = np.array([left_x + b1_text.width / 2, y1, 0])
        b1_text.move_to(b1_final)
        b1_check = make_checkmark().scale_to_fit_height(0.26).next_to(b1_text, LEFT, buff=0.3)
        b1_start = b1_final + LEFT * 9
        b1_text.move_to(b1_start)

        # bullet 2
        b2_final = np.array([left_x + b2_text.width / 2, y2, 0])
        b2_text.move_to(b2_final)
        b2_check = make_checkmark().scale_to_fit_height(0.26).next_to(b2_text, LEFT, buff=0.3)
        b2_start = b2_final + LEFT * 9
        b2_text.move_to(b2_start)

        # bullet 3
        b3_final = np.array([left_x + b3_text.width / 2, y3, 0])
        b3_text.move_to(b3_final)
        b3_check = make_checkmark().scale_to_fit_height(0.26).next_to(b3_text, LEFT, buff=0.3)
        b3_start = b3_final + LEFT * 9
        b3_text.move_to(b3_start)

        # bullet 4, two parts
        part1_final = np.array([left_x + part1_text.width / 2, y4, 0])
        part1_text.move_to(part1_final)
        part2_text.next_to(part1_text, RIGHT, buff=0)
        part2_final = part2_text.get_center()
        b4_check = make_checkmark().scale_to_fit_height(0.26).next_to(part1_text, LEFT, buff=0.3)
        part1_start = part1_final + LEFT * 9
        part2_start = part2_final + LEFT * 9
        part1_text.move_to(part1_start)
        part2_text.move_to(part2_start)

        # ======================== TIMELINE ========================
        # Beat 1: 0.00–2.66 — clean title card
        self.play(FadeIn(heading), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.66))

        # Beat 2: 2.66–6.34 — first bullet
        self.add(b1_text)
        self.play(b1_text.animate.move_to(b1_final), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.3))
        self.play(Create(b1_check), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.58))

        # Gap 6.34–6.88, then hold through 6.88–7.26
        self.wait(max(0.05, 0.54))
        self.wait(max(0.05, 0.38))

        # Beat 4: 7.26–8.78 — second bullet
        self.add(b2_text)
        self.play(b2_text.animate.move_to(b2_final), run_time=max(0.05, 0.9))
        self.play(Create(b2_check), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.12))

        # Gap 8.78–9.24
        self.wait(max(0.05, 0.46))

        # Beat 5: 9.24–11.56 — third bullet
        self.add(b3_text)
        self.play(b3_text.animate.move_to(b3_final), run_time=max(0.05, 1.2))
        self.play(Create(b3_check), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.42))

        # Gap 11.56–12.38
        self.wait(max(0.05, 0.82))

        # Beat 6: 12.38–14.76 — fourth bullet, first part
        self.add(part1_text)
        self.play(part1_text.animate.move_to(part1_final), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.18))

        # Beat 7: 14.76–17.27 — fourth bullet, second part + check
        self.add(part2_text)
        self.play(part2_text.animate.move_to(part2_final), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.2))
        self.play(Create(b4_check), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.41))