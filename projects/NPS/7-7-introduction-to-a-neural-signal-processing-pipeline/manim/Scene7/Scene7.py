ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Beats 1: blank screen 0.00-1.58
        self.wait(max(0.05, 1.58))

        # Build the central horizontal pipeline
        accents = [BLUE, TEAL, GREEN, ORANGE]
        labels = [
            "Raw Signal",
            "Preprocessing",
            "Feature Extraction",
            "Interpretation or Classification",
        ]
        widths = [2.4, 2.4, 2.4, 2.8]
        font_sizes = [20, 20, 20, 16]

        box_groups = []
        box_rects = []
        box_labels = []

        for i, (label, accent, w, fs) in enumerate(zip(labels, accents, widths, font_sizes)):
            rect = RoundedRectangle(
                width=w,
                height=1.0,
                corner_radius=0.16,
                fill_color=GREY,
                fill_opacity=0.18,
                stroke_color=WHITE,
                stroke_width=2,
            )
            label_text = Text(label, font_size=fs, color=WHITE, weight="BOLD")
            label_text.scale_to_fit_width(rect.width - 0.35)
            label_text.move_to(rect.get_center())
            group = VGroup(rect, label_text)
            box_groups.append(group)
            box_rects.append(rect)
            box_labels.append(label_text)

        box_groups = VGroup(*box_groups)
        box_groups.arrange(RIGHT, buff=0.6)
        box_groups.move_to(np.array([0, 0.8, 0]))

        # Reconstruct individual lists after moving the group
        boxes = list(box_groups)
        box_rects = [b[0] for b in boxes]
        box_labels = [b[1] for b in boxes]

        arrows = []
        for i in range(3):
            arrow = Arrow(
                start=boxes[i].get_right(),
                end=boxes[i + 1].get_left(),
                color=GREY_B,
                stroke_width=3.5,
                buff=0.08,
                max_tip_length_to_length_ratio=0.22,
            )
            arrows.append(arrow)

        pipeline_base = VGroup(*boxes, *arrows)
        pipeline_base.move_to(np.array([0, 0.8, 0]))

        # Soft glows behind each box, invisible initially
        glow_rects = []
        for i, box in enumerate(boxes):
            glow = RoundedRectangle(
                width=box.width + 0.22,
                height=box.height + 0.22,
                corner_radius=0.20,
                stroke_color=accents[i],
                stroke_width=9,
                fill_color=accents[i],
                fill_opacity=0.14,
            )
            glow.move_to(box.get_center())
            glow.set_stroke(opacity=0.0)
            glow.set_fill(opacity=0.0)
            glow_rects.append(glow)

        self.add(*glow_rects)

        # Explanatory texts appear beneath boxes as the narration reaches them
        exp_strings = [
            "neural activity + unwanted components",
            "prepares signal for analysis",
            "meaningful quantitative measurements",
            "understand activity or assign category",
        ]
        exp_texts = []
        for i, s in enumerate(exp_strings):
            t = Text(s, font_size=16, color=WHITE, weight="SEMIBOLD")
            t.scale_to_fit_width(boxes[i].width + 0.8)
            t.next_to(boxes[i], DOWN, buff=0.20)
            t.set_opacity(0)
            exp_texts.append(t)

        # Helper animation groups
        def bright_anim(i, accent):
            return [
                box_groups[i].animate.set_opacity(1),
                box_rects[i].animate.set_stroke(accent, width=5).set_fill(accent, opacity=0.32),
                glow_rects[i].animate.set_stroke(opacity=0.55).set_fill(opacity=0.13),
            ]

        def normal_anim(i):
            return [
                box_groups[i].animate.set_opacity(1),
                box_rects[i].animate.set_stroke(WHITE, width=2).set_fill(GREY, opacity=0.18),
                glow_rects[i].animate.set_stroke(opacity=0.0).set_fill(opacity=0.0),
            ]

        def dim_anim(i):
            return box_groups[i].animate.set_opacity(0.28)

        # Beat 2: pipeline fades in and holds 1.58-7.64
        self.play(FadeIn(pipeline_base, shift=UP * 0.1), run_time=max(0.05, 2.2))
        self.wait(max(0.05, 3.86))

        # Beat 3: sweep highlight left to right 7.64-9.26
        sweeper = SurroundingRectangle(
            boxes[0],
            color=YELLOW,
            buff=0.08,
            stroke_width=4,
            fill_color=YELLOW,
            fill_opacity=0.08,
        )
        self.add(sweeper)

        per_sweep = 1.62 / 4.0
        for i in range(4):
            target = SurroundingRectangle(
                boxes[i],
                color=YELLOW,
                buff=0.08,
                stroke_width=4,
                fill_color=YELLOW,
                fill_opacity=0.08,
            )
            self.play(Transform(sweeper, target), run_time=max(0.05, per_sweep * 0.85))
            self.wait(max(0.05, per_sweep * 0.15))
        self.remove(sweeper)

        # Beat 4: Raw Signal bright 9.26-10.78
        self.play(
            *bright_anim(0, BLUE),
            dim_anim(1),
            dim_anim(2),
            dim_anim(3),
            FadeIn(exp_texts[0]),
            run_time=max(0.05, 1.52),
        )
        self.wait(max(0.05, 0.50))

        # Beat 5: Preprocessing bright 11.28-12.50
        self.play(
            *normal_anim(0),
            *bright_anim(1, TEAL),
            dim_anim(2),
            dim_anim(3),
            FadeIn(exp_texts[1]),
            run_time=max(0.05, 1.22),
        )

        # Beat 6: Feature bright, then Interpretation also bright 12.50-15.14
        self.play(
            *normal_anim(1),
            *bright_anim(2, GREEN),
            dim_anim(0),
            dim_anim(3),
            FadeIn(exp_texts[2]),
            run_time=max(0.05, 1.2),
        )
        self.play(
            *bright_anim(3, ORANGE),
            dim_anim(0),
            dim_anim(1),
            FadeIn(exp_texts[3]),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.64))

        # Beat 7: Raw waveform icon then artifact overlay 16.36-21.32
        self.wait(max(0.05, 1.22))

        raw_wave_xs = np.linspace(-0.8, 0.8, 24)
        raw_wave_ys = 0.22 * np.sin(6.0 * raw_wave_xs) + 0.08 * np.sin(18.0 * raw_wave_xs)
        raw_wave_points = [np.array([x, y, 0]) for x, y in zip(raw_wave_xs, raw_wave_ys)]
        raw_wave_segments = VGroup(
            *[
                Line(raw_wave_points[j], raw_wave_points[j + 1], color=BLUE, stroke_width=1.8)
                for j in range(len(raw_wave_points) - 1)
            ]
        )
        raw_baseline = Line(LEFT * 0.8, RIGHT * 0.8, color=GREY_B, stroke_width=1.0)
        raw_wave_icon = VGroup(raw_baseline, raw_wave_segments)
        raw_wave_icon.scale_to_fit_width(1.7)
        raw_wave_icon.next_to(boxes[0], UP, buff=0.16)

        self.play(
            *bright_anim(0, BLUE),
            dim_anim(1),
            dim_anim(2),
            dim_anim(3),
            FadeIn(raw_wave_icon, scale=0.7),
            run_time=max(0.05, 1.2),
        )
        self.play(exp_texts[0].animate.scale(1.08), run_time=max(0.05, 0.25))
        self.play(exp_texts[0].animate.scale(1 / 1.08), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 2.28))

        # Orange-red unwanted component zigzag overlay at 20.34
        zigzag_points = [
            np.array([-0.45, 0.10, 0]),
            np.array([-0.28, -0.10, 0]),
            np.array([-0.11, 0.10, 0]),
            np.array([0.06, -0.10, 0]),
            np.array([0.23, 0.10, 0]),
            np.array([0.40, -0.10, 0]),
        ]
        artifact_zigzag = VGroup(
            *[
                Line(zigzag_points[j], zigzag_points[j + 1], color=RED, stroke_width=2.2)
                for j in range(len(zigzag_points) - 1)
            ]
        )
        artifact_zigzag.scale_to_fit_width(1.4)
        artifact_zigzag.move_to(raw_wave_icon.get_center())

        self.play(FadeIn(artifact_zigzag, scale=0.5), run_time=max(0.05, 0.5))
        self.play(artifact_zigzag.animate.scale(1.15), run_time=max(0.05, 0.2))
        self.play(artifact_zigzag.animate.scale(1 / 1.15), run_time=max(0.05, 0.28))

        # Beat 8: Preprocessing icon 22.34-24.52
        self.wait(max(0.05, 1.02))

        pre_xs_noisy = np.linspace(-1.1, 0.0, 18)
        pre_ys_noisy = 0.14 * np.sin(8.0 * pre_xs_noisy) + 0.06 * np.sin(20.0 * pre_xs_noisy)
        pre_points_noisy = [np.array([x, y, 0]) for x, y in zip(pre_xs_noisy, pre_ys_noisy)]
        noisy_lines = VGroup(
            *[
                Line(pre_points_noisy[j], pre_points_noisy[j + 1], color=TEAL, stroke_width=1.8)
                for j in range(len(pre_points_noisy) - 1)
            ]
        )

        pre_xs_smooth = np.linspace(0.0, 1.1, 18)
        pre_ys_smooth = 0.03 * np.sin(2.5 * pre_xs_smooth)
        pre_points_smooth = [np.array([x, y, 0]) for x, y in zip(pre_xs_smooth, pre_ys_smooth)]
        smooth_lines = VGroup(
            *[
                Line(pre_points_smooth[j], pre_points_smooth[j + 1], color=WHITE, stroke_width=1.8)
                for j in range(len(pre_points_smooth) - 1)
            ]
        )

        pre_baseline = Line(LEFT * 1.1, RIGHT * 1.1, color=GREY_B, stroke_width=1.0)
        pre_icon = VGroup(pre_baseline, noisy_lines, smooth_lines)
        pre_icon.scale_to_fit_width(1.8)
        pre_icon.next_to(boxes[1], UP, buff=0.16)

        self.play(
            *normal_anim(0),
            *bright_anim(1, TEAL),
            dim_anim(2),
            dim_anim(3),
            FadeIn(pre_icon, scale=0.7),
            run_time=max(0.05, 1.1),
        )
        self.play(exp_texts[1].animate.scale(1.08), run_time=max(0.05, 0.25))
        self.play(exp_texts[1].animate.scale(1 / 1.08), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.58))

        # Beat 9: Feature icon 25.25-29.44
        self.wait(max(0.05, 0.73))

        feature_bars = VGroup()
        bar_heights = [0.42, 0.72, 0.55]
        bar_xs = [-0.33, 0.0, 0.33]
        for x, h in zip(bar_xs, bar_heights):
            bar = Rectangle(
                width=0.22,
                height=h,
                fill_color=GREEN,
                fill_opacity=1,
                stroke_width=0,
            )
            bar.move_to(np.array([x, h / 2, 0]))
            feature_bars.add(bar)

        feature_baseline = Line(LEFT * 0.55, RIGHT * 0.55, color=GREY_B, stroke_width=1.0)
        readout_box = RoundedRectangle(
            width=0.38,
            height=0.30,
            corner_radius=0.06,
            fill_color=WHITE,
            fill_opacity=0.95,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        readout_text = Text("…", font_size=17, color=BLACK, weight="BOLD")
        readout_text.move_to(readout_box.get_center())
        readout = VGroup(readout_box, readout_text)
        readout.next_to(feature_baseline, RIGHT, buff=0.20).shift(UP * 0.15)

        feature_icon = VGroup(feature_baseline, feature_bars, readout)
        feature_icon.scale_to_fit_width(1.7)
        feature_icon.next_to(boxes[2], UP, buff=0.22)

        self.play(
            *normal_anim(1),
            *bright_anim(2, GREEN),
            dim_anim(0),
            dim_anim(3),
            FadeIn(feature_icon, scale=0.7),
            run_time=max(0.05, 1.4),
        )
        self.play(exp_texts[2].animate.scale(1.08), run_time=max(0.05, 0.25))
        self.play(exp_texts[2].animate.scale(1 / 1.08), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 2.29))

        # Beat 10: Classification bright and visually splits 30.26-33.24
        self.wait(max(0.05, 0.82))

        class_rect = box_rects[3]
        divider = Line(
            class_rect.get_top() + DOWN * 0.06,
            class_rect.get_bottom() + UP * 0.06,
            color=GREY_B,
            stroke_width=2.0,
        )
        half_width = class_rect.width / 2.0

        left_half_label = Text("Interpretation", font_size=15, color=WHITE, weight="BOLD")
        left_half_label.scale_to_fit_width(half_width - 0.25)
        left_half_label.move_to(class_rect.get_center() + LEFT * (half_width / 2))

        right_half_label = Text("Classification", font_size=15, color=WHITE, weight="BOLD")
        right_half_label.scale_to_fit_width(half_width - 0.25)
        right_half_label.move_to(class_rect.get_center() + RIGHT * (half_width / 2))

        split_group = VGroup(divider, left_half_label, right_half_label)
        for item in split_group:
            item.set_opacity(0)
        self.add(split_group)

        self.play(
            *normal_anim(2),
            *bright_anim(3, ORANGE),
            dim_anim(0),
            dim_anim(1),
            FadeIn(divider),
            FadeIn(left_half_label),
            FadeIn(right_half_label),
            FadeOut(box_labels[3]),
            run_time=max(0.05, 1.6),
        )
        self.play(exp_texts[3].animate.scale(1.08), run_time=max(0.05, 0.25))
        self.play(exp_texts[3].animate.scale(1 / 1.08), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.88))

        # Beat 11: two sub-branches of final stage pulse 33.78-38.96
        self.wait(max(0.05, 0.54))

        left_highlight = Rectangle(
            width=class_rect.width / 2 - 0.07,
            height=class_rect.height - 0.16,
            fill_color=ORANGE,
            fill_opacity=0.22,
            stroke_width=0,
        )
        left_highlight.move_to(class_rect.get_center() + LEFT * (half_width / 2))
        left_highlight.set_opacity(0)

        right_highlight = Rectangle(
            width=class_rect.width / 2 - 0.07,
            height=class_rect.height - 0.16,
            fill_color=ORANGE,
            fill_opacity=0.26,
            stroke_width=0,
        )
        right_highlight.move_to(class_rect.get_center() + RIGHT * (half_width / 2))
        right_highlight.set_opacity(0)

        self.add(left_highlight, right_highlight)

        sub0 = Text("understand neural activity", font_size=14, color=WHITE, weight="SEMIBOLD")
        sub0.scale_to_fit_width(half_width + 0.35)
        sub0.next_to(class_rect, DOWN, buff=0.55).set_x(
            class_rect.get_center()[0] - half_width / 2
        )

        sub1 = Text("assign to predefined categories or commands", font_size=13, color=WHITE, weight="SEMIBOLD")
        sub1.scale_to_fit_width(half_width + 0.35)
        sub1.next_to(class_rect, DOWN, buff=0.55).set_x(
            class_rect.get_center()[0] + half_width / 2
        )

        self.play(
            FadeOut(exp_texts[3]),
            FadeIn(left_highlight),
            FadeIn(sub0),
            run_time=max(0.05, 0.4),
        )
        self.play(left_half_label.animate.scale(1.15), run_time=max(0.05, 0.2))
        self.play(left_half_label.animate.scale(1 / 1.15), run_time=max(0.05, 0.22))

        self.play(
            FadeIn(right_highlight),
            FadeIn(sub1),
            run_time=max(0.05, 0.4),
        )
        self.play(right_half_label.animate.scale(1.15), run_time=max(0.05, 0.2))
        self.play(right_half_label.animate.scale(1 / 1.15), run_time=max(0.05, 0.22))
        self.wait(max(0.05, 3.54))

        # Beat 12: full composition + application icons 40.02-44.73
        self.wait(max(0.05, 1.06))

        self.play(
            *[normal_anim(i) for i in range(4)],
            run_time=max(0.05, 1.2),
        )

        brain_icon = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=0.6,
        )
        brain_icon.scale_to_fit_height(0.75)
        brain_icon.move_to(np.array([0, 3.0, 0]))

        hand_icon = SVGMobject(
            ASSET_PATHS["hand"],
            fill_color=RED,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=0.6,
        )
        hand_icon.scale_to_fit_height(0.75)
        hand_icon.move_to(np.array([0, -2.7, 0]))

        eye_outer = Circle(
            radius=0.4,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        eye_iris = Circle(
            radius=0.17,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_width=0,
        )
        eye_pupil = Dot(radius=0.06, color=BLACK)
        eye_iris.move_to(eye_outer.get_center())
        eye_pupil.move_to(eye_outer.get_center())
        eye_icon = VGroup(eye_outer, eye_iris, eye_pupil)
        eye_icon.scale_to_fit_height(0.7)
        eye_icon.move_to(np.array([-6.0, 1.5, 0]))

        computer_screen = Rectangle(
            width=0.9,
            height=0.6,
            fill_color=GREEN,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=2,
        )
        computer_stand = Line(
            computer_screen.get_bottom(),
            computer_screen.get_bottom() + DOWN * 0.25,
            color=GREY_B,
            stroke_width=3,
        )
        computer_base = Line(
            computer_screen.get_bottom() + DOWN * 0.25 + LEFT * 0.30,
            computer_screen.get_bottom() + DOWN * 0.25 + RIGHT * 0.30,
            color=GREY_B,
            stroke_width=3,
        )
        computer_icon = VGroup(computer_screen, computer_stand, computer_base)
        computer_icon.scale_to_fit_height(0.7)
        computer_icon.move_to(np.array([6.0, 1.5, 0]))

        application_icons = VGroup(brain_icon, hand_icon, eye_icon, computer_icon)

        raw_point = boxes[0].get_center()
        dotted_lines = VGroup(
            *[
                DashedLine(
                    icon.get_center(),
                    raw_point,
                    color=GREY_B,
                    stroke_width=1.6,
                    stroke_opacity=0.55,
                    dash_length=0.12,
                )
                for icon in application_icons
            ]
        )

        self.play(
            FadeIn(application_icons, shift=UP * 0.1),
            FadeIn(dotted_lines),
            run_time=max(0.05, 1.2),
        )
        self.play(dotted_lines.animate.set_stroke(opacity=0.9), run_time=max(0.05, 0.3))
        self.play(dotted_lines.animate.set_stroke(opacity=0.55), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 1.71))