ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene22(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_wave(func, x_min, x_max, color=YELLOW, stroke_width=2.5, num_points=120):
            vm = VMobject()
            vm.set_stroke(color=color, width=stroke_width, opacity=1)
            x = np.linspace(x_min, x_max, num_points)
            y = func(x)
            vm.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return vm

        def make_checkmark(size=0.10, color=GREEN):
            l1 = Line(
                np.array([-0.55 * size, -0.25 * size, 0]),
                np.array([0, 0.30 * size, 0]),
                color=color, stroke_width=3,
            )
            l2 = Line(
                np.array([0, 0.30 * size, 0]),
                np.array([0.75 * size, -0.35 * size, 0]),
                color=color, stroke_width=3,
            )
            return VGroup(l1, l2)

        # background layer + fade cover for previous scene
        bg_rect = Rectangle(
            width=16, height=9,
            fill_color="#0F1116", fill_opacity=1, stroke_width=0,
        ).move_to(ORIGIN)
        prev_cover = Rectangle(
            width=16, height=9,
            fill_color=BLACK, fill_opacity=1, stroke_width=0,
        ).move_to(ORIGIN)
        self.add(bg_rect, prev_cover)

        # ---------- heading ----------
        heading = Text(
            "Summary: EEG in Epilepsy Diagnosis",
            font_size=34, weight="BOLD", color=WHITE,
        ).scale_to_fit_width(11)
        heading.to_edge(UP, buff=0.3)

        # ---------- brain / head ----------
        head_outline = Ellipse(
            width=1.9, height=2.4,
            fill_color=GREY, fill_opacity=0.12,
            stroke_color=WHITE, stroke_width=3,
        )
        brain_icon = SVGMobject(ASSET_PATHS["brain"])
        brain_icon.set_fill(PINK, opacity=0.9).set_stroke(PINK, width=0)
        brain_icon.scale_to_fit_height(1.35)
        brain_icon.move_to(head_outline.get_center() + UP * 0.15)
        brain_head_group = VGroup(head_outline, brain_icon)
        brain_head_group.move_to(LEFT * 4.2 + DOWN * 0.2)

        # abnormal traces inside brain
        def irreg1(x):
            return 0.14 * np.sin(2 * np.pi * 1.7 * x) + 0.18 * np.sin(2 * np.pi * 4.3 * x + 1.0) + 0.08 * np.cos(2 * np.pi * 8.1 * x + 0.5)
        def irreg2(x):
            return 0.10 * np.sin(2 * np.pi * 2.1 * x) + 0.15 * np.sin(2 * np.pi * 5.5 * x + 0.3)
        trace1 = make_wave(irreg1, -0.40, 0.40, color=YELLOW, stroke_width=2.5).move_to(brain_icon.get_center() + UP * 0.05)
        trace2 = make_wave(irreg2, -0.30, 0.30, color=ORANGE, stroke_width=2.2).move_to(brain_icon.get_center() + DOWN * 0.02)
        abnormal_traces = VGroup(trace1, trace2)

        abnormal_label = Text("Abnormal Electrical Activity", font_size=14, color=RED)
        abnormal_label.next_to(brain_head_group, DOWN, buff=0.25)

        # ---------- beat 1: 0.00-4.64 ----------
        self.play(
            FadeOut(prev_cover),
            FadeIn(heading),
            FadeIn(brain_head_group),
            FadeIn(abnormal_traces),
            FadeIn(abnormal_label),
            run_time=max(0.05, 4.0),
        )
        self.wait(max(0.05, 0.64))

        # gap 4.64-5.52
        self.wait(max(0.05, 0.88))

        # ---------- right panel: initial readout box ----------
        readout_box = RoundedRectangle(
            width=2.8, height=1.3, corner_radius=0.1,
            fill_color=BLACK, fill_opacity=0.7,
            stroke_color=TEAL, stroke_width=2,
        )
        readout_box.move_to(RIGHT * 1.8 + UP * 0.4)

        def base_eeg(x):
            return 0.10 * np.sin(2 * np.pi * 1.2 * x) + 0.06 * np.sin(2 * np.pi * 2.6 * x)
        readout_base_wave = make_wave(base_eeg, -1.0, 1.0, color=GREEN, stroke_width=2.5)
        readout_base_wave.move_to(readout_box.get_center())

        def spiky_eeg(x):
            y = 0.10 * np.sin(2 * np.pi * 1.2 * x) + 0.10 * np.sin(2 * np.pi * 2.5 * x)
            y = y + 0.55 * np.exp(-((x - 0.35) / 0.08) ** 2)
            return y
        readout_spiky_wave = make_wave(spiky_eeg, -1.0, 1.0, color=YELLOW, stroke_width=2.8)
        readout_spiky_wave.move_to(readout_box.get_center())

        right_panel = VGroup(readout_box, readout_base_wave)

        # ---------- beat 2: 5.52-7.60 ----------
        connect_line = Line(
            brain_head_group.get_right() + RIGHT * 0.15,
            readout_box.get_left() + LEFT * 0.15,
            color=GREY_B, stroke_width=3,
        ).set_opacity(0.8)

        diag_label = Text("Diagnosis", font_size=15, color=GREEN)
        mon_label = Text("Monitoring", font_size=15, color=GREEN)
        check_d = make_checkmark(size=0.10, color=GREEN)
        check_m = make_checkmark(size=0.10, color=GREEN)
        diag_item = VGroup(check_d, diag_label).arrange(RIGHT, buff=0.12)
        mon_item = VGroup(check_m, mon_label).arrange(RIGHT, buff=0.12)
        diag_mon_group = VGroup(diag_item, mon_item).arrange(RIGHT, buff=0.55)
        diag_mon_group.next_to(readout_box, DOWN, buff=0.35)

        self.play(
            head_outline.animate.set_stroke(color=WHITE, width=4, opacity=1),
            brain_icon.animate.set_fill(opacity=1),
            Create(connect_line),
            FadeIn(right_panel),
            FadeIn(diag_mon_group),
            run_time=max(0.05, 2.08),
        )

        # gap 7.60-8.58
        self.wait(max(0.05, 0.98))

        # ---------- beat 3: 8.58-15.44 ----------
        brain_to_readout_arrow = Arrow(
            brain_head_group.get_right() + RIGHT * 0.2,
            readout_box.get_left() + LEFT * 0.2,
            color=YELLOW, stroke_width=3, buff=0.15,
            max_tip_length_to_length_ratio=0.20,
        )
        detected_label = Text("Detected with EEG", font_size=15, color=YELLOW)
        detected_label.next_to(readout_box, DOWN, buff=0.35)

        self.play(FadeOut(diag_mon_group), run_time=max(0.05, 0.6))
        self.play(abnormal_traces.animate.scale(1.35).set_color(RED), run_time=max(0.05, 0.7))
        self.play(abnormal_traces.animate.scale(1 / 1.35).set_color(YELLOW), run_time=max(0.05, 0.6))
        self.play(
            Create(brain_to_readout_arrow),
            FadeOut(readout_base_wave),
            FadeIn(readout_spiky_wave),
            run_time=max(0.05, 2.0),
        )
        right_panel.add(readout_spiky_wave)
        self.play(FadeIn(detected_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.96))

        # gap 15.44-16.54
        self.wait(max(0.05, 1.10))

        # ---------- build processing blocks ----------
        proc_labels = ["Filtering", "Time-Domain Analysis", "Time-Frequency Analysis", "Automated Detection"]
        proc_colors = [BLUE, ORANGE, GREEN, PURPLE]
        proc_blocks = []
        proc_rects = []
        for label, color in zip(proc_labels, proc_colors):
            rect = RoundedRectangle(
                width=2.7, height=0.65, corner_radius=0.10,
                fill_color=color, fill_opacity=0.25,
                stroke_color=color, stroke_width=2,
            )
            txt = Text(label, font_size=12, color=WHITE)
            txt.scale_to_fit_width(2.4)
            txt.move_to(rect.get_center())
            proc_rects.append(rect)
            proc_blocks.append(VGroup(rect, txt))
        proc_blocks_group = VGroup(*proc_blocks).arrange(RIGHT, buff=0.55)
        proc_blocks_group.next_to(readout_box, DOWN, buff=0.9)
        proc_blocks_group.set_opacity(0)

        proc_arrows = []
        for block, color in zip(proc_blocks, proc_colors):
            start = np.array([block.get_center()[0], readout_box.get_bottom()[1], 0])
            end = block.get_top() + UP * 0.05
            arr = Arrow(
                start, end,
                color=color, stroke_width=2, buff=0.05,
                max_tip_length_to_length_ratio=0.25,
            )
            arr.set_opacity(0)
            proc_arrows.append(arr)
        proc_arrows_group = VGroup(*proc_arrows)
        right_panel.add(proc_blocks_group, proc_arrows_group)

        # ---------- beat 4: 16.54-28.64 ----------
        self.play(FadeOut(detected_label), run_time=max(0.05, 1.0))
        for i in range(4):
            self.play(
                proc_blocks[i].animate.set_opacity(1),
                proc_arrows[i].animate.set_opacity(1),
                run_time=max(0.05, 2.0),
            )
        spike_highlight = Circle(
            radius=0.10,
            fill_color=RED, fill_opacity=0.25,
            stroke_color=YELLOW, stroke_width=2,
        ).move_to(readout_box.get_center() + RIGHT * 0.35 + UP * 0.30)
        right_panel.add(spike_highlight)
        self.play(
            readout_spiky_wave.animate.set_stroke(color=WHITE, width=3.5),
            FadeIn(spike_highlight),
            run_time=max(0.05, 1.8),
        )
        self.wait(max(0.05, 1.3))

        # gap 28.64-29.63
        self.wait(max(0.05, 0.99))

        # ---------- build output blocks ----------
        output_labels = ["Diagnosis", "Treatment Planning", "Long-term Monitoring", "Epilepsy Research"]
        output_colors = [TEAL, PURPLE, BLUE, GREEN]
        output_blocks = []
        for label, color in zip(output_labels, output_colors):
            rect = RoundedRectangle(
                width=2.7, height=0.62, corner_radius=0.10,
                fill_color=color, fill_opacity=0.18,
                stroke_color=color, stroke_width=2,
            )
            txt = Text(label, font_size=12, color=WHITE)
            txt.scale_to_fit_width(2.4)
            txt.move_to(rect.get_center())
            output_blocks.append(VGroup(rect, txt))
        output_blocks_group = VGroup(*output_blocks).arrange(RIGHT, buff=0.55)
        output_blocks_group.next_to(proc_blocks_group, DOWN, buff=0.8)
        output_blocks_group.set_opacity(0)

        output_arrows = []
        for pb, ob, color in zip(proc_blocks, output_blocks, output_colors):
            start = np.array([pb.get_center()[0], pb.get_bottom()[1], 0])
            end = ob.get_top() + UP * 0.05
            arr = Arrow(
                start, end,
                color=color, stroke_width=2, buff=0.05,
                max_tip_length_to_length_ratio=0.25,
            )
            arr.set_opacity(0)
            output_arrows.append(arr)
        output_arrows_group = VGroup(*output_arrows)
        right_panel.add(output_blocks_group, output_arrows_group)

        # ---------- beat 5: 29.63-35.88 ----------
        glow_anims = [
            r.animate.set_stroke(color=WHITE, width=4).set_fill(opacity=0.45)
            for r in proc_rects
        ]
        self.play(*glow_anims, run_time=max(0.05, 1.0))
        for i in range(4):
            self.play(
                output_blocks[i].animate.set_opacity(1),
                output_arrows[i].animate.set_opacity(1),
                run_time=max(0.05, 0.7),
            )
        self.wait(max(0.05, 2.45))

        # gap 35.88-36.66
        self.wait(max(0.05, 0.78))

        # ---------- condensed blocks ----------
        bs_wave_icon = make_wave(lambda x: 0.15 * np.sin(2 * np.pi * 1.4 * x), -0.4, 0.4, color=BLUE, stroke_width=2.5)
        sleep_bands = VGroup(
            Rectangle(width=0.7, height=0.10, fill_color=TEAL, fill_opacity=1, stroke_width=0),
            Rectangle(width=0.9, height=0.10, fill_color=ORANGE, fill_opacity=1, stroke_width=0),
            Rectangle(width=0.5, height=0.10, fill_color=PURPLE, fill_opacity=1, stroke_width=0),
        ).arrange(DOWN, buff=0.08)
        neuro_icon = make_checkmark(size=0.18, color=GREEN)

        def make_condensed_block(label, icon):
            rect = RoundedRectangle(
                width=3.7, height=0.85, corner_radius=0.10,
                fill_color=BLACK, fill_opacity=0.65,
                stroke_color=GREY_B, stroke_width=1.5,
            )
            label_text = Text(label, font_size=13, color=WHITE)
            label_text.scale_to_fit_width(2.4)
            icon.scale_to_fit_height(0.40)
            if icon.width > 0.65:
                icon.scale_to_fit_width(0.65)
            icon.move_to(rect.get_left() + RIGHT * 0.5)
            label_text.next_to(icon, RIGHT, buff=0.20)
            return VGroup(rect, icon, label_text)

        condensed_blocks = VGroup(
            make_condensed_block("Brain-State Analysis", bs_wave_icon),
            make_condensed_block("Sleep Staging", sleep_bands),
            make_condensed_block("Neurological Disorder Diagnosis", neuro_icon),
        ).arrange(DOWN, buff=0.35)
        condensed_blocks.move_to(LEFT * 1.0 + DOWN * 0.1)
        condensed_blocks.set_opacity(0)
        self.add(condensed_blocks)

        # ---------- beat 6: 36.66-48.66 ----------
        self.play(
            right_panel.animate.scale(0.68).set_opacity(0.55).move_to(np.array([3.6, -1.4, 0])),
            FadeOut(connect_line),
            FadeOut(brain_to_readout_arrow),
            FadeOut(abnormal_label),
            run_time=max(0.05, 2.5),
        )
        for block in condensed_blocks:
            self.play(GrowFromCenter(block), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 3.5))

        # gap 48.66-49.72
        self.wait(max(0.05, 1.06))

        # ---------- clean brain + background shift ----------
        active_traces = VGroup(
            make_wave(lambda x: 0.12 * np.sin(2 * np.pi * 1.9 * x) + 0.14 * np.sin(2 * np.pi * 4.1 * x + 0.8), -0.45, 0.45, color=YELLOW, stroke_width=2.4),
            make_wave(lambda x: 0.10 * np.sin(2 * np.pi * 2.5 * x) + 0.12 * np.sin(2 * np.pi * 6.3 * x + 1.2), -0.35, 0.35, color=ORANGE, stroke_width=2.2),
        ).move_to(brain_icon.get_center() + UP * 0.05)

        # ---------- beat 7: 49.72-56.52 ----------
        self.play(
            FadeOut(heading),
            FadeOut(right_panel),
            FadeOut(condensed_blocks),
            FadeOut(abnormal_traces),
            FadeIn(active_traces),
            bg_rect.animate.set_fill("#191D26", opacity=1),
            run_time=max(0.05, 3.0),
        )
        self.play(Wiggle(brain_head_group, scale_value=0.08, rotation_angle=0.05), run_time=max(0.05, 1.2))
        self.play(active_traces.animate.scale(1.25).set_color(RED), run_time=max(0.05, 0.8))
        self.play(active_traces.animate.scale(1 / 1.25).set_color(YELLOW), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.0))

        # gap 56.52-57.08
        self.wait(max(0.05, 0.56))

        # ---------- devices ----------
        def make_computer_icon():
            monitor = RoundedRectangle(width=1.0, height=0.65, corner_radius=0.05, fill_color=BLUE, fill_opacity=0.95, stroke_color=WHITE, stroke_width=2)
            screen = RoundedRectangle(width=0.8, height=0.48, corner_radius=0.03, fill_color=BLACK, fill_opacity=0.85, stroke_width=0).move_to(monitor)
            stand = Rectangle(width=0.12, height=0.12, fill_color=GREY_B, fill_opacity=1, stroke_width=0).next_to(monitor, DOWN, buff=0.04)
            base = Rectangle(width=0.38, height=0.07, fill_color=GREY_B, fill_opacity=1, stroke_width=0).next_to(stand, DOWN, buff=0.02)
            return VGroup(monitor, screen, stand, base)

        def make_wheelchair_icon():
            big_wheel = Circle(radius=0.24, color=BLUE, fill_color=BLUE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2).move_to(RIGHT * 0.28 + DOWN * 0.3)
            small_wheel = Circle(radius=0.13, color=BLUE, fill_color=BLUE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2).move_to(LEFT * 0.15 + DOWN * 0.3)
            back = Rectangle(width=0.15, height=0.6, fill_color=PURPLE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1.5).move_to(LEFT * 0.25 + UP * 0.15)
            seat = Rectangle(width=0.7, height=0.13, fill_color=PURPLE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1.5).move_to(RIGHT * 0.1 + DOWN * 0.05)
            frame = Line(seat.get_left() + LEFT * 0.05, big_wheel.get_center(), color=WHITE, stroke_width=2).set_opacity(0.8)
            return VGroup(back, seat, big_wheel, small_wheel, frame)

        def make_robot_arm_icon():
            base = Rectangle(width=0.55, height=0.20, fill_color=ORANGE, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to(DOWN * 0.4)
            lower = Rectangle(width=0.16, height=0.50, fill_color=ORANGE, fill_opacity=1, stroke_color=WHITE, stroke_width=1.2).move_to(base.get_top() + UP * 0.25)
            elbow = Circle(radius=0.07, fill_color=PURPLE, fill_opacity=1, stroke_width=0).move_to(lower.get_top() + UP * 0.02)
            upper = Rectangle(width=0.14, height=0.45, fill_color=ORANGE, fill_opacity=1, stroke_color=WHITE, stroke_width=1.2).move_to(elbow.get_top() + UP * 0.23)
            gripper = VGroup(
                Rectangle(width=0.06, height=0.18, fill_color=GREY_B, fill_opacity=1, stroke_width=0).move_to(upper.get_top() + UP * 0.09 + LEFT * 0.08),
                Rectangle(width=0.06, height=0.18, fill_color=GREY_B, fill_opacity=1, stroke_width=0).move_to(upper.get_top() + UP * 0.09 + RIGHT * 0.08),
            )
            return VGroup(base, lower, elbow, upper, gripper)

        def make_communication_icon():
            bubble = RoundedRectangle(width=0.95, height=0.60, corner_radius=0.18, fill_color=GREEN, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
            tail = Polygon(
                bubble.get_bottom() + LEFT * 0.15,
                bubble.get_bottom() + RIGHT * 0.10,
                bubble.get_bottom() + LEFT * 0.25 + DOWN * 0.20,
                fill_color=GREEN, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1.5,
            )
            dots = VGroup(*[Circle(radius=0.05, fill_color=WHITE, fill_opacity=1, stroke_width=0) for _ in range(3)]).arrange(RIGHT, buff=0.08).move_to(bubble.get_center())
            return VGroup(tail, bubble, dots)

        def make_device_block(icon, label):
            icon.scale_to_fit_height(0.85)
            if icon.width > 1.20:
                icon.scale_to_fit_width(1.20)
            label_text = Text(label, font_size=13, color=WHITE).scale_to_fit_width(2.0)
            block = VGroup(icon, label_text).arrange(DOWN, buff=0.10)
            return block

        device_blocks = [
            make_device_block(make_computer_icon(), "Computer"),
            make_device_block(make_wheelchair_icon(), "Wheelchair"),
            make_device_block(make_robot_arm_icon(), "Robotic Arm"),
            make_device_block(make_communication_icon(), "Communication System"),
        ]
        device_blocks_group = VGroup(*device_blocks).arrange(DOWN, buff=0.35)
        device_blocks_group.move_to(RIGHT * 5.3 + UP * 0.1)
        device_blocks_group.set_opacity(0.35)

        main_start = brain_head_group.get_right() + RIGHT * 0.25
        main_end = np.array([3.6, brain_head_group.get_center()[1], 0])
        main_arrow = Arrow(
            main_start, main_end,
            color=YELLOW, stroke_width=4, buff=0.30,
            max_tip_length_to_length_ratio=0.15,
        )

        branch_arrows = VGroup()
        for device_block, color in zip(device_blocks, [BLUE, PURPLE, ORANGE, GREEN]):
            end = device_block.get_left() + LEFT * 0.10
            arr = Arrow(
                main_end, end,
                color=GREY_B, stroke_width=2.5, buff=0.05,
                max_tip_length_to_length_ratio=0.25,
            ).set_opacity(0.35)
            branch_arrows.add(arr)

        # ---------- beat 8: 57.08-61.70 ----------
        self.play(Create(main_arrow), run_time=max(0.05, 1.2))
        self.play(FadeIn(device_blocks_group), FadeIn(branch_arrows), run_time=max(0.05, 1.3))
        self.play(
            device_blocks[0].animate.set_opacity(1),
            branch_arrows[0].animate.set_opacity(1).set_stroke(color=YELLOW, width=3),
            run_time=max(0.05, 1.32),
        )
        self.wait(max(0.05, 0.80))

        # gap 61.70-62.70
        self.wait(max(0.05, 1.00))

        # ---------- beat 9: 62.70-63.24 ----------
        self.play(
            device_blocks[1].animate.set_opacity(1),
            branch_arrows[1].animate.set_opacity(1).set_stroke(color=YELLOW, width=3),
            run_time=max(0.05, 0.54),
        )

        # gap 63.24-63.66
        self.wait(max(0.05, 0.42))

        # ---------- beat 10: 63.66-64.40 ----------
        self.play(
            device_blocks[2].animate.set_opacity(1),
            branch_arrows[2].animate.set_opacity(1).set_stroke(color=YELLOW, width=3),
            run_time=max(0.05, 0.74),
        )

        # gap 64.40-64.84
        self.wait(max(0.05, 0.44))

        # ---------- beat 11: 64.84-65.90 ----------
        self.play(
            device_blocks[3].animate.set_opacity(1),
            branch_arrows[3].animate.set_opacity(1).set_stroke(color=YELLOW, width=3),
            run_time=max(0.05, 1.06),
        )

        # gap 65.90-66.94
        self.wait(max(0.05, 1.04))

        # ---------- beat 12: 66.94-70.86 ----------
        title_bci = Text(
            "Brain-Computer Interface (BCI)",
            font_size=36, weight="BOLD", color=YELLOW,
        ).scale_to_fit_width(10.5)
        title_bci.move_to(UP * 3.0)

        signal_on_arrow = make_wave(
            lambda x: 0.08 * np.sin(2 * np.pi * 3.0 * x) + 0.05 * np.sin(2 * np.pi * 7.0 * x),
            -3.3, 3.3, color=YELLOW, stroke_width=2.5,
        ).move_to(main_arrow.get_center() + UP * 0.15)

        self.play(FadeIn(title_bci), run_time=max(0.05, 1.0))
        self.play(Create(signal_on_arrow), run_time=max(0.05, 1.2))
        for device_block in device_blocks:
            self.play(Indicate(device_block, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.12))

        # gap 70.86-71.16
        self.wait(max(0.05, 0.30))

        # ---------- beat 13: 71.16-73.24 + hold to 73.95 ----------
        next_arrow = Arrow(
            LEFT * 0.4, RIGHT * 0.4,
            color=YELLOW, stroke_width=3, buff=0.1,
            max_tip_length_to_length_ratio=0.3,
        )
        next_text = Text("Next Section", font_size=14, color=YELLOW)
        next_marker = VGroup(next_text, next_arrow).arrange(LEFT, buff=0.20)
        next_marker.to_corner(DOWN + RIGHT, buff=0.4)

        self.play(FadeIn(next_marker), run_time=max(0.05, 0.85))
        self.wait(max(0.05, 1.23))
        self.wait(max(0.05, 0.71))  # final hold to 73.95