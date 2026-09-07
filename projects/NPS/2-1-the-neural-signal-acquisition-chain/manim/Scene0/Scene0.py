ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import random
import numpy as np
from manim import *


class Scene0(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Layout constants -------------------------------------------------
        brain_center = np.array([-4.2, 0.3, 0])
        monitor_center = np.array([4.2, 0.3, 0])
        ZOOM_FACTOR = 0.42

        # ---- Left: stylized brain cross-section -------------------------------
        brain_svg = SVGMobject(ASSET_PATHS["brain"]).scale_to_fit_height(3.2)
        brain_svg.move_to(brain_center)
        brain_svg.set_fill(PURPLE, opacity=0.25)
        brain_svg.set_stroke(PURPLE, width=3)

        path_offsets = [
            [(-1.3, -0.8), (-0.8, -0.4), (-0.3, 0.0), (0.2, 0.4), (0.7, 0.6)],
            [(-1.2, -1.4), (-0.7, -1.0), (-0.3, -0.5), (0.1, -0.2), (0.6, -0.1)],
            [(-1.4, 0.0), (-0.9, 0.6), (-0.4, 0.9), (0.1, 0.9), (0.6, 0.7)],
            [(-1.3, 1.1), (-0.8, 0.9), (-0.3, 0.6), (0.2, 0.4), (0.7, 0.2)],
            [(-1.0, -0.2), (-0.5, 0.2), (0.0, 0.6), (0.5, 0.8), (0.9, 0.7)],
        ]

        paths = []
        for offset_path in path_offsets:
            pts = [brain_center + np.array([ox, oy, 0]) for ox, oy in offset_path]
            p = VMobject(stroke_color=TEAL, stroke_width=2, stroke_opacity=0.5)
            p.set_points_as_corners(pts)
            paths.append(p)

        neuron_paths = VGroup(*paths)

        def make_pulse_updater(path, speed):
            def updater(mob, dt):
                mob.progress = getattr(mob, "progress", 0.0) + speed * dt
                mob.progress = mob.progress % 1.0
                mob.move_to(path.point_from_proportion(mob.progress))
            return updater

        pulse_list = []
        for i in range(6):
            path = paths[i % len(paths)]
            glow = Dot(radius=0.15, color=ORANGE, fill_opacity=0.4)
            core = Dot(radius=0.07, color=YELLOW)
            pulse = VGroup(glow, core)
            pulse.progress = random.uniform(0.0, 1.0)
            pulse.move_to(path.point_from_proportion(pulse.progress))
            pulse.add_updater(make_pulse_updater(path, 0.07 + random.uniform(0.0, 0.05)))
            pulse_list.append(pulse)

        star_pulse = pulse_list[2]
        star_glow = star_pulse[0]

        # ---- Right: computer monitor with clean waveform ----------------------
        screen_outer = Rectangle(
            width=3.0,
            height=2.0,
            color=GREY_B,
            fill_color=GREY,
            fill_opacity=0.12,
            stroke_width=4,
        )
        screen_inner = Rectangle(
            width=2.6,
            height=1.5,
            color=TEAL,
            fill_color=BLACK,
            fill_opacity=1.0,
            stroke_width=3,
        ).move_to(screen_outer)

        wave_points = [
            np.array([x, 0.55 * np.sin(2 * x), 0])
            for x in np.linspace(-1.15, 1.15, 120)
        ]
        waveform = VMobject(stroke_color=GREEN, stroke_width=4)
        waveform.set_points_as_corners(wave_points)
        waveform.move_to(screen_inner.get_center())

        stand = Line(
            screen_outer.get_bottom() + DOWN * 0.05,
            screen_outer.get_bottom() + DOWN * 0.35,
            color=GREY_B,
            stroke_width=6,
        )
        base = Line(
            stand.get_end() + LEFT * 0.18,
            stand.get_end() + RIGHT * 0.18,
            color=GREY_B,
            stroke_width=8,
        )
        monitor_group = VGroup(screen_outer, screen_inner, waveform, stand, base)
        monitor_group.move_to(monitor_center)

        # ---- Question-mark connector -----------------------------------------
        connect_dashed = DashedLine(
            np.array([-2.6, 0.3, 0]),
            np.array([2.6, 0.3, 0]),
            dash_length=0.18,
            color=GREY_B,
            stroke_width=3,
        )
        q_mark = Text("?", font_size=80, color=YELLOW).move_to([0, 0.3, 0])

        # ---- Beat 1: 0.00-3.00 -----------------------------------------------
        self.play(FadeIn(brain_svg), FadeIn(monitor_group), run_time=max(0.05, 1.4))
        self.play(
            FadeIn(neuron_paths),
            *[FadeIn(p) for p in pulse_list],
            FadeIn(connect_dashed),
            FadeIn(q_mark),
            run_time=max(0.05, 1.0),
        )
        self.play(
            q_mark.animate.scale(1.06),
            rate_func=rate_functions.there_and_back,
            run_time=max(0.05, 0.6),
        )

        # ---- Beat 2: 3.00-7.58, occasional pulse clusters ---------------------
        self.wait(max(0.05, 1.0))
        self.play(
            Indicate(pulse_list[0], scale_factor=1.6, color=YELLOW),
            Indicate(pulse_list[1], scale_factor=1.6, color=YELLOW),
            Indicate(pulse_list[2], scale_factor=1.6, color=YELLOW),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 1.0))
        self.play(
            Indicate(pulse_list[3], scale_factor=1.6, color=YELLOW),
            Indicate(pulse_list[4], scale_factor=1.6, color=YELLOW),
            Indicate(pulse_list[5], scale_factor=1.6, color=YELLOW),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.98))

        # ---- Beat 3: 7.58-11.10, question mark enlarges and pulses ------------
        self.play(q_mark.animate.scale(1.18), run_time=max(0.05, 0.8))
        self.play(q_mark.animate.scale(1.08 / 1.18), run_time=max(0.05, 0.35))
        self.play(q_mark.animate.scale(1.18 / 1.08), run_time=max(0.05, 0.35))
        self.play(q_mark.animate.scale(1.08 / 1.18), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 1.67))

        # ---- Beat 4: 11.10-16.26, blocked attempt line ------------------------
        attempt_line = DashedLine(
            np.array([-2.55, 0.5, 0]),
            np.array([-0.55, 0.5, 0]),
            dash_length=0.15,
            color=ORANGE,
            stroke_width=5,
        )
        self.play(Create(attempt_line), run_time=max(0.05, 1.6))
        self.play(Indicate(q_mark, scale_factor=1.3, color=YELLOW), run_time=max(0.05, 0.8))
        self.play(Indicate(q_mark, scale_factor=1.3, color=YELLOW), run_time=max(0.05, 0.8))
        self.play(FadeOut(attempt_line), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.36))

        # ---- Beat 5: 16.26-22.14, close-up on one trapped pulse --------------
        self.play(
            self.camera.frame.animate.scale(ZOOM_FACTOR).move_to(brain_center + UP * 0.1),
            run_time=max(0.05, 2.2),
        )
        self.play(Indicate(star_pulse, scale_factor=2.2, color=YELLOW), run_time=max(0.05, 1.0))
        self.play(
            star_glow.animate.set_opacity(0.9).scale(2.0),
            run_time=max(0.05, 1.3),
        )
        self.wait(max(0.05, 1.38))

        # ---- Beat 6: 22.14-25.32, side-by-side question mark pulse ------------
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).scale(1 / ZOOM_FACTOR),
            run_time=max(0.05, 1.8),
        )
        self.play(Indicate(q_mark, scale_factor=1.25, color=YELLOW), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.58))

        # ---- Build the acquisition chain -------------------------------------
        def make_brain_icon():
            icon = SVGMobject(ASSET_PATHS["brain"]).scale_to_fit_height(0.5)
            icon.set_fill(WHITE, opacity=1.0)
            icon.set_stroke(WHITE, width=0)
            return icon

        def make_electrode_icon():
            base_rect = Rectangle(
                width=0.30,
                height=0.10,
                fill_color=WHITE,
                fill_opacity=1.0,
                stroke_opacity=0,
            ).move_to(UP * 0.20)
            needle = Line(UP * 0.12, DOWN * 0.28, color=WHITE, stroke_width=4)
            tip = Dot(DOWN * 0.32, radius=0.06, color=YELLOW)
            return VGroup(base_rect, needle, tip).move_to(ORIGIN)

        def make_amplifier_icon():
            tri = Polygon(
                LEFT * 0.30 + UP * 0.30,
                LEFT * 0.30 + DOWN * 0.30,
                RIGHT * 0.32,
                fill_color=WHITE,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=2,
            )
            in_plus = Line(LEFT * 0.45 + UP * 0.15, LEFT * 0.30 + UP * 0.15, color=WHITE, stroke_width=3)
            in_minus = Line(LEFT * 0.45 + DOWN * 0.15, LEFT * 0.30 + DOWN * 0.15, color=WHITE, stroke_width=3)
            out = Line(RIGHT * 0.32, RIGHT * 0.47, color=WHITE, stroke_width=3)
            return VGroup(tri, in_plus, in_minus, out).move_to(ORIGIN)

        def make_filter_icon():
            wave = VMobject(stroke_color=WHITE, stroke_width=3)
            wave.set_points_as_corners(
                [
                    np.array([x, 0.22 * np.sin(3 * x), 0])
                    for x in np.linspace(-0.3, 0.3, 40)
                ]
            )
            line = Line(LEFT * 0.2, RIGHT * 0.2, color=WHITE, stroke_width=3)
            return VGroup(wave, line).move_to(ORIGIN)

        def make_adc_icon():
            left_wave = VMobject(stroke_color=WHITE, stroke_width=3)
            left_wave.set_points_as_corners(
                [
                    np.array([x, 0.18 * np.sin(5 * x), 0])
                    for x in np.linspace(-0.35, -0.05, 20)
                ]
            )
            right_stair = VMobject(stroke_color=WHITE, stroke_width=3)
            right_stair.set_points_as_corners(
                [
                    np.array([0.05, -0.18, 0]),
                    np.array([0.05, 0.18, 0]),
                    np.array([0.15, 0.18, 0]),
                    np.array([0.15, -0.05, 0]),
                    np.array([0.25, -0.05, 0]),
                    np.array([0.25, 0.18, 0]),
                    np.array([0.35, 0.18, 0]),
                ]
            )
            divider = Line([0, -0.22, 0], [0, 0.22, 0], color=GREY_B, stroke_width=2)
            return VGroup(left_wave, right_stair, divider).move_to(ORIGIN)

        def make_computer_icon():
            screen = Rectangle(
                width=0.55,
                height=0.40,
                color=WHITE,
                fill_color=TEAL,
                fill_opacity=0.5,
                stroke_color=WHITE,
                stroke_width=3,
            )
            stand_line = Line(DOWN * 0.20, DOWN * 0.32, color=WHITE, stroke_width=4)
            base_line = Line(
                LEFT * 0.15 + DOWN * 0.32,
                RIGHT * 0.15 + DOWN * 0.32,
                color=WHITE,
                stroke_width=4,
            )
            return VGroup(screen, stand_line, base_line).move_to(ORIGIN)

        box_colors = [PURPLE, ORANGE, BLUE, GREEN, PINK, TEAL]
        icon_makers = [
            make_brain_icon,
            make_electrode_icon,
            make_amplifier_icon,
            make_filter_icon,
            make_adc_icon,
            make_computer_icon,
        ]

        boxes = []
        for color, icon_maker in zip(box_colors, icon_makers):
            icon = icon_maker().scale_to_fit_height(0.48)
            box = Rectangle(
                width=0.78,
                height=0.78,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.18,
                stroke_width=4,
            )
            icon.move_to(box.get_center())
            boxes.append(VGroup(box, icon))

        boxes_group = VGroup(*boxes).arrange(RIGHT, buff=0.45)

        arrow_list = []
        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i].get_right() + RIGHT * 0.08,
                boxes[i + 1].get_left() + LEFT * 0.08,
                buff=0.05,
                stroke_width=2,
                color=GREY_B,
                max_tip_length_to_length_ratio=0.4,
                max_stroke_width_to_length_ratio=12,
            )
            arrow_list.append(arrow)

        chain_group = VGroup(*boxes, *arrow_list)
        chain_group.move_to([0, 0.3, 0])
        chain_group.scale_to_fit_width(5.2)
        chain_parts = boxes + arrow_list

        chain_label = Text("Neural Signal Acquisition Chain", font_size=34, color=YELLOW)
        chain_label.move_to([0, -2.0, 0])
        chain_label.scale_to_fit_width(7)

        # Recording-type labels for beat 9
        rec_names = ["EEG", "EMG", "ECoG", "microelectrode"]
        label_list = []
        for name in rec_names:
            lab = Text(name, font_size=28, color=WHITE)
            label_list.append(lab)

        rec_group = VGroup(*label_list).arrange(RIGHT, buff=0.5)
        rec_group.move_to([0, 1.05, 0])
        rec_group.scale_to_fit_width(5.6)
        for lab in label_list:
            lab.set_opacity(0)
            self.add(lab)

        # ---- Beat 7: 25.32-32.90, replace question with chain ---------------
        self.play(FadeOut(q_mark), FadeOut(connect_dashed), run_time=max(0.05, 0.7))

        self.play(GrowFromCenter(boxes[0]), run_time=max(0.05, 0.65))
        for i in range(len(boxes) - 1):
            self.play(
                FadeIn(arrow_list[i]),
                GrowFromCenter(boxes[i + 1]),
                run_time=max(0.05, 0.65),
            )

        self.play(Write(chain_label), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 2.08))

        # ---- Beat 8: 32.90-35.14, chain settles -----------------------------
        self.play(
            *[Indicate(part, scale_factor=1.04, color=YELLOW) for part in chain_parts],
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 1.04))

        # ---- Beat 9: 35.14-44.10, recording types appear one by one ---------
        per_item = 8.96 / 4
        for lab in label_list:
            self.play(
                lab.animate.set_opacity(1),
                *[Indicate(part, scale_factor=1.05, color=YELLOW) for part in chain_parts],
                run_time=max(0.05, 0.9),
            )
            self.wait(max(0.05, per_item - 0.9))

        # ---- Beat 10: 44.10-49.60, chain pulses once more --------------------
        self.play(*[FadeOut(lab) for lab in label_list], run_time=max(0.05, 0.8))
        self.play(
            *[Indicate(part, scale_factor=1.06, color=YELLOW) for part in chain_parts],
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 3.7))