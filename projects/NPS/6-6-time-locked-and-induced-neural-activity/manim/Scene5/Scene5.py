ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def make_previous_flow(self):
        g = VGroup()

        data = [
            ("ERP analysis", BLUE, np.array([-3.0, 1.3, 0])),
            ("Time-frequency analysis", ORANGE, np.array([3.0, 1.3, 0])),
            ("Complementary insights", PURPLE, np.array([0.0, -1.6, 0])),
        ]
        for label, color, pos in data:
            box = RoundedRectangle(
                width=4.2,
                height=0.9,
                corner_radius=0.2,
                fill_color=color,
                fill_opacity=0.25,
                stroke_color=color,
                stroke_width=3,
            )
            text = Text(label, font_size=22, color=WHITE).scale_to_fit_width(3.8)
            text.move_to(box)
            group = VGroup(box, text).move_to(pos)
            g.add(group)

        arrow1 = Arrow([-3.0, 0.75, 0], [-1.0, -0.9, 0], color=GREY_B, stroke_width=4, buff=0.1)
        arrow2 = Arrow([3.0, 0.75, 0], [1.0, -0.9, 0], color=GREY_B, stroke_width=4, buff=0.1)
        g.add(arrow1, arrow2)

        return g

    def make_wave_row(self, center_x, y, peak_shift, color=TEAL, stroke_width=2.5):
        half_width = 1.3
        axis = Line(
            [center_x - half_width, y, 0],
            [center_x + half_width, y, 0],
            color=GREY_B,
            stroke_width=1.5,
        )
        curve = FunctionGraph(
            lambda x, p=peak_shift: 0.55 * np.exp(-0.5 * ((x - p) / 0.22) ** 2),
            x_range=[-half_width, half_width, 0.02],
            color=color,
            stroke_width=stroke_width,
        )
        curve.shift(np.array([center_x, y, 0]))
        return VGroup(axis, curve)

    def make_avg_wave(self, center_x, y, color=TEAL, stroke_width=5, smear=False):
        half_width = 1.3
        axis = Line(
            [center_x - half_width, y, 0],
            [center_x + half_width, y, 0],
            color=GREY_B,
            stroke_width=1.5,
        )

        if smear:
            curve = FunctionGraph(
                lambda x: (
                    0.14 * np.exp(-0.5 * (x / 1.15) ** 2)
                    + 0.10 * np.exp(-0.5 * ((x + 0.4) / 0.75) ** 2)
                    + 0.10 * np.exp(-0.5 * ((x - 0.4) / 0.75) ** 2)
                ),
                x_range=[-half_width, half_width, 0.02],
                color=color,
                stroke_width=stroke_width,
            )
            curve.shift(np.array([center_x, y, 0]))
            curve.set_opacity(0.55)
        else:
            curve = FunctionGraph(
                lambda x: 0.75 * np.exp(-0.5 * (x / 0.24) ** 2),
                x_range=[-half_width, half_width, 0.02],
                color=color,
                stroke_width=stroke_width,
            )
            curve.shift(np.array([center_x, y, 0]))

        return VGroup(axis, curve)

    def make_method_box(self, label):
        box = RoundedRectangle(
            width=2.5,
            height=0.55,
            corner_radius=0.2,
            fill_color=BLUE,
            fill_opacity=0.25,
            stroke_color=BLUE,
            stroke_width=3,
        )
        text = Text(label, font_size=20, color=WHITE).scale_to_fit_width(2.1)
        text.move_to(box)
        return VGroup(box, text)

    def construct(self):
        self.camera.background_color = "#0F1116"

        # Beat 1: previous full flow diagram fades out; heading and divider fade in
        prev_diagram = self.make_previous_flow()
        self.add(prev_diagram)

        heading = Text(
            "Summary: Time-Locked vs. Induced",
            font_size=44,
            color=WHITE,
            weight="BOLD",
            t2c={"Time-Locked": YELLOW, "Induced": GOLD},
        ).move_to([0, 3.3, 0])

        divider = Line([0, 2.6, 0], [0, -1.0, 0], color=GREY_B, stroke_width=3)

        self.play(FadeOut(prev_diagram), run_time=max(0.05, 1.8))
        self.remove(prev_diagram)
        self.play(FadeIn(heading), FadeIn(divider), run_time=max(0.05, 2.3))
        self.wait(max(0.05, 0.84))

        # Beat 2: left aligned stack + clean average
        left_center = -3.2
        right_center = 3.2
        row_ys = [1.5, 1.0, 0.5, 0.0, -0.5]

        left_stack = VGroup()
        for y in row_ys:
            row = self.make_wave_row(left_center, y, 0.0, color=TEAL)
            left_stack.add(row)

        left_avg = self.make_avg_wave(left_center, -1.8, color=TEAL, stroke_width=5, smear=False)
        left_arrow = Arrow(
            left_stack.get_bottom() + DOWN * 0.15,
            left_avg.get_top() + UP * 0.08,
            color=WHITE,
            stroke_width=4,
            buff=0.05,
        )
        left_label = Text(
            "Time-Locked: ERP averaging works",
            font_size=22,
            color=GREEN,
            weight="BOLD",
        ).next_to(left_avg, DOWN, buff=0.28)
        left_whole = VGroup(left_stack, left_arrow, left_avg, left_label)

        for row in left_stack:
            self.play(Write(row), run_time=max(0.05, 0.55))
        self.play(FadeIn(left_arrow), run_time=max(0.05, 0.5))
        self.play(Write(left_avg), run_time=max(0.05, 1.2))
        self.play(FadeIn(left_label), run_time=max(0.05, 0.6))
        self.play(
            Indicate(left_stack, color=TEAL, scale_factor=1.04),
            Indicate(left_avg, color=TEAL, scale_factor=1.06),
            run_time=max(0.05, 1.65),
        )
        self.wait(max(0.05, 1.24))

        # Beat 3: right misaligned stack + smeared average
        right_shifts = [-0.9, -0.3, 0.6, 0.05, -0.7]
        right_stack = VGroup()
        for y, shift in zip(row_ys, right_shifts):
            row = self.make_wave_row(right_center, y, shift, color=TEAL)
            right_stack.add(row)

        right_avg = self.make_avg_wave(right_center, -1.8, color=TEAL, stroke_width=4, smear=True)
        right_arrow = Arrow(
            right_stack.get_bottom() + DOWN * 0.15,
            right_avg.get_top() + UP * 0.08,
            color=WHITE,
            stroke_width=4,
            buff=0.05,
        )
        right_label = Text(
            "Induced: Averaging fails",
            font_size=22,
            color=ORANGE,
            weight="BOLD",
        ).next_to(right_avg, DOWN, buff=0.28)
        right_whole = VGroup(right_stack, right_arrow, right_avg, right_label)

        for row in right_stack:
            self.play(Write(row), run_time=max(0.05, 0.5))
        self.play(FadeIn(right_arrow), run_time=max(0.05, 0.4))
        self.play(Write(right_avg), run_time=max(0.05, 1.0))
        self.play(FadeIn(right_label), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.16))
        self.wait(max(0.05, 0.84))

        # Beat 4: right brightens, left dims, caption + bottom method section
        self.play(left_whole.animate.set_opacity(0.35), run_time=max(0.05, 1.5))

        right_caption = Text(
            "Because averaging reduces these responses",
            font_size=22,
            color=WHITE,
        ).move_to([3.4, 2.4, 0])
        self.play(FadeIn(right_caption), run_time=max(0.05, 1.0))

        bottom_label = Text(
            "Use time-frequency analysis for induced activity",
            font_size=24,
            color=WHITE,
            weight="BOLD",
        ).scale_to_fit_width(10)
        bottom_label.move_to([0, -2.65, 0])
        self.play(FadeIn(bottom_label), run_time=max(0.05, 0.8))

        method_boxes = VGroup(
            self.make_method_box("STFT"),
            self.make_method_box("Spectrogram"),
            self.make_method_box("Wavelet Analysis"),
        ).arrange(RIGHT, buff=0.8)
        method_boxes.move_to([0, -3.2, 0])
        self.play(FadeIn(method_boxes), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 2.0))

        # Beat 5: highlight STFT
        first, second, third = method_boxes[0], method_boxes[1], method_boxes[2]
        self.play(
            first[0].animate.set_stroke(color=YELLOW, width=4).set_fill(opacity=0.45),
            first[1].animate.set_opacity(1),
            second[0].animate.set_opacity(0.45),
            second[1].animate.set_opacity(0.45),
            third[0].animate.set_opacity(0.45),
            third[1].animate.set_opacity(0.45),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.12))
        self.wait(max(0.05, 0.74))

        # Beat 6: highlight Spectrogram
        self.play(
            first[0].animate.set_stroke(color=BLUE, width=3).set_fill(opacity=0.25),
            first[1].animate.set_opacity(0.45),
            second[0].animate.set_stroke(color=YELLOW, width=4).set_fill(opacity=0.45),
            second[1].animate.set_opacity(1),
            third[0].animate.set_opacity(0.45),
            third[1].animate.set_opacity(0.45),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.10))
        self.wait(max(0.05, 0.46))

        # Beat 7: highlight Wavelet Analysis
        self.play(
            second[0].animate.set_stroke(color=BLUE, width=3).set_fill(opacity=0.25),
            second[1].animate.set_opacity(0.45),
            third[0].animate.set_stroke(color=YELLOW, width=4).set_fill(opacity=0.45),
            third[1].animate.set_opacity(1),
            first[0].animate.set_opacity(0.45),
            first[1].animate.set_opacity(0.45),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.16))
        self.wait(max(0.05, 1.18))

        # Beat 8: all method boxes equal, full summary holds, subtitle in
        self.play(
            first[0].animate.set_stroke(color=BLUE, width=3).set_fill(opacity=0.25).set_opacity(1),
            first[1].animate.set_opacity(1),
            second[0].animate.set_stroke(color=BLUE, width=3).set_fill(opacity=0.25).set_opacity(1),
            second[1].animate.set_opacity(1),
            third[0].animate.set_stroke(color=BLUE, width=3).set_fill(opacity=0.25).set_opacity(1),
            third[1].animate.set_opacity(1),
            run_time=max(0.05, 1.5),
        )

        subtitle = Text(
            "Understanding this distinction is essential for selecting appropriate analytical techniques",
            font_size=20,
            color=WHITE,
        ).scale_to_fit_width(13)
        subtitle.move_to([0, -3.8, 0])
        self.play(FadeIn(subtitle), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 3.2))

        # Beat 9: final pulse near center
        final_caption = Text(
            "Correctly interpreting neural recordings",
            font_size=30,
            color=GOLD,
            weight="BOLD",
        ).scale_to_fit_width(10)
        final_caption.move_to([0, 0.3, 0])

        self.play(FadeIn(final_caption), run_time=max(0.05, 0.7))
        self.play(final_caption.animate.scale(1.04), run_time=max(0.05, 0.6))
        self.play(final_caption.animate.scale(1 / 1.04), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.96))