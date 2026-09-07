ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def make_prev_summary(self):
        title = Text(
            "Summary: Time-Locked vs. Induced",
            font_size=34,
            color=WHITE,
            weight="BOLD",
            t2c={"Time-Locked": YELLOW, "Induced": GOLD},
        )

        method_boxes = VGroup()
        for label, color in [("STFT", BLUE), ("Spectrogram", GREEN), ("Wavelet Analysis", ORANGE)]:
            box = RoundedRectangle(
                width=2.2,
                height=0.55,
                corner_radius=0.18,
                fill_color=color,
                fill_opacity=0.25,
                stroke_color=color,
                stroke_width=2,
            )
            text = Text(label, font_size=16, color=WHITE).scale_to_fit_width(1.8)
            text.move_to(box)
            method_boxes.add(VGroup(box, text))

        method_boxes.arrange(RIGHT, buff=0.5)
        method_boxes.next_to(title, DOWN, buff=0.55)

        return VGroup(title, method_boxes).move_to(ORIGIN)

    def make_chip(self, label, color):
        text = Text(label, font_size=22, color=WHITE, weight="BOLD")
        if text.width > 5.8:
            text.scale_to_fit_width(5.8)

        box = RoundedRectangle(
            width=text.width + 0.8,
            height=text.height + 0.45,
            corner_radius=0.25,
            fill_color=color,
            fill_opacity=0.15,
            stroke_color=color,
            stroke_width=3,
        )
        text.move_to(box)
        return VGroup(box, text)

    def construct(self):
        self.camera.background_color = "#0F1116"

        # Blank background behind the previous summary graphic
        blank_bg = Rectangle(
            width=14,
            height=8,
            fill_color="#0F1116",
            fill_opacity=1,
            stroke_width=0,
        )
        blank_bg.set_opacity(0).move_to(ORIGIN)

        previous_summary = self.make_prev_summary()
        self.add(blank_bg, previous_summary)

        labels = [
            "Nonstationary neural signals",
            "STFT: time and frequency information",
            "Spectrogram: visualizes STFT output",
            "Wavelet analysis: multiple scales",
            "ERPs: time-locked averaging",
            "Time-locked vs induced responses",
        ]
        colors = [BLUE, TEAL, GREEN, ORANGE, PURPLE, PINK]

        chips = [self.make_chip(label, color) for label, color in zip(labels, colors)]
        for chip in chips:
            chip.set_opacity(0)

        list_group = VGroup(*chips).arrange(DOWN, buff=0.15)
        list_group.shift(UP * (2.5 - chips[0].get_center()[1]))

        # Helper state animations
        def dim(i):
            color = colors[i]
            box = chips[i][0]
            text = chips[i][1]
            return [
                box.animate.set_fill(color=color, opacity=0.08).set_stroke(color=color, width=3, opacity=0.35),
                text.animate.set_color(WHITE).set_opacity(0.4),
            ]

        def active(i):
            box = chips[i][0]
            text = chips[i][1]
            return [
                box.animate.set_fill(color=GOLD, opacity=0.25).set_stroke(color=GOLD, width=5, opacity=1),
                text.animate.set_color(YELLOW).set_opacity(1),
            ]

        def neutral(i):
            color = colors[i]
            box = chips[i][0]
            text = chips[i][1]
            return [
                box.animate.set_fill(color=color, opacity=0.12).set_stroke(color=color, width=3.5, opacity=0.8),
                text.animate.set_color(WHITE).set_opacity(1),
            ]

        # Beat 1: 0.00-4.42
        self.play(FadeIn(blank_bg), FadeOut(previous_summary), run_time=max(0.05, 1.2))
        self.remove(previous_summary)

        self.add(list_group)
        self.play(FadeIn(chips[0]), run_time=max(0.05, 1.0))
        self.play(Indicate(chips[0], color=GOLD, scale_factor=1.05), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.42))

        # Beat 2: 4.42-7.32
        self.play(*dim(0), FadeIn(chips[1]), run_time=max(0.05, 0.8))
        self.play(*active(1), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.5))

        # Beat 3: 7.32-10.66
        self.play(*dim(1), FadeIn(chips[2]), run_time=max(0.05, 0.8))
        self.play(*active(2), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.94))

        # Gap to next narration beat
        self.wait(max(0.05, 1.18))

        # Beat 4: 11.84-16.60
        self.play(*active(0), *dim(1), *dim(2), run_time=max(0.05, 0.8))
        self.play(list_group.animate.shift(UP * 0.15), run_time=max(0.05, 0.8))
        self.play(Indicate(chips[0], color=GOLD, scale_factor=1.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 2.36))

        # Beat 5: 16.60-18.94
        self.play(*dim(0), *active(1), run_time=max(0.05, 0.7))
        self.play(list_group.animate.shift(UP * 0.10), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.14))

        # Gap
        self.wait(max(0.05, 0.74))

        # Beat 6: 19.68-25.84
        self.play(*dim(1), *active(2), run_time=max(0.05, 0.7))
        self.play(list_group.animate.shift(UP * 0.10), run_time=max(0.05, 0.5))
        self.play(Indicate(chips[2], color=GOLD, scale_factor=1.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 4.16))

        # Beat 7: 25.84-33.10
        self.play(*dim(2), FadeIn(chips[3]), run_time=max(0.05, 0.8))
        self.play(*active(3), run_time=max(0.05, 0.6))
        self.play(list_group.animate.shift(UP * 0.10), run_time=max(0.05, 0.6))
        self.play(Indicate(chips[3], color=GOLD, scale_factor=1.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 4.46))

        # Beat 8: 33.10-40.26
        self.play(*dim(3), FadeIn(chips[4]), run_time=max(0.05, 0.8))
        self.play(*active(4), run_time=max(0.05, 0.6))
        self.play(list_group.animate.shift(UP * 0.10), run_time=max(0.05, 0.6))
        self.play(Indicate(chips[4], color=GOLD, scale_factor=1.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 4.36))

        # Beat 9: 40.26-48.16
        self.play(*dim(4), FadeIn(chips[5]), run_time=max(0.05, 0.8))
        self.play(*active(5), run_time=max(0.05, 0.6))
        self.play(list_group.animate.shift(UP * 0.05), run_time=max(0.05, 0.5))
        self.play(Indicate(chips[5], color=GOLD, scale_factor=1.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 5.20))

        # Beat 10: 48.16-55.30
        unhighlight_anims = []
        for i in range(6):
            unhighlight_anims.extend(neutral(i))
        self.play(*unhighlight_anims, run_time=max(0.05, 1.2))

        self.play(list_group.animate.shift(DOWN * 0.20), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 4.44))

        # Beat 11: 55.30-61.66
        self.play(list_group.animate.move_to(np.array([0, 0.2, 0])), run_time=max(0.05, 0.8))

        brighten_anims = []
        for i in range(6):
            box = chips[i][0]
            text = chips[i][1]
            brighten_anims.append(box.animate.set_fill(color=colors[i], opacity=0.16).set_stroke(color=colors[i], width=4, opacity=1))
            brighten_anims.append(text.animate.set_color(WHITE).set_opacity(1))
        self.play(*brighten_anims, run_time=max(0.05, 0.6))

        self.play(Indicate(list_group, color=GOLD, scale_factor=1.02), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 3.36))

        # Beat 12: 61.66-68.35
        arrow = Arrow(ORIGIN, RIGHT * 1.2, color=GOLD, stroke_width=6, buff=0.1)
        arrow.next_to(list_group, DOWN, buff=0.6)

        self.play(GrowFromCenter(arrow), run_time=max(0.05, 0.8))
        self.play(Indicate(arrow, color=GOLD, scale_factor=1.15), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 5.09))