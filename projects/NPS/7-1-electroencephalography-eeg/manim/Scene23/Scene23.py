ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene23(Scene):
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

        def make_computer_icon():
            monitor = RoundedRectangle(
                width=1.0, height=0.65, corner_radius=0.05,
                fill_color=BLUE, fill_opacity=0.95,
                stroke_color=WHITE, stroke_width=2,
            )
            screen = RoundedRectangle(
                width=0.78, height=0.46, corner_radius=0.03,
                fill_color=BLACK, fill_opacity=0.85, stroke_width=0,
            ).move_to(monitor.get_center())
            stand = Rectangle(
                width=0.12, height=0.12,
                fill_color=GREY_B, fill_opacity=1, stroke_width=0,
            ).next_to(monitor, DOWN, buff=0.04)
            base = Rectangle(
                width=0.38, height=0.06,
                fill_color=GREY_B, fill_opacity=1, stroke_width=0,
            ).next_to(stand, DOWN, buff=0.02)
            return VGroup(monitor, screen, stand, base)

        def make_wheelchair_icon():
            big_wheel = Circle(
                radius=0.24, color=BLUE, fill_color=BLUE, fill_opacity=0.9,
                stroke_color=WHITE, stroke_width=2,
            ).move_to(RIGHT * 0.28 + DOWN * 0.3)
            small_wheel = Circle(
                radius=0.13, color=BLUE, fill_color=BLUE, fill_opacity=0.9,
                stroke_color=WHITE, stroke_width=2,
            ).move_to(LEFT * 0.15 + DOWN * 0.3)
            back = Rectangle(
                width=0.15, height=0.6,
                fill_color=PURPLE, fill_opacity=0.9,
                stroke_color=WHITE, stroke_width=1.5,
            ).move_to(LEFT * 0.25 + UP * 0.15)
            seat = Rectangle(
                width=0.7, height=0.13,
                fill_color=PURPLE, fill_opacity=0.9,
                stroke_color=WHITE, stroke_width=1.5,
            ).move_to(RIGHT * 0.1 + DOWN * 0.05)
            frame = Line(
                seat.get_left() + LEFT * 0.05,
                big_wheel.get_center(),
                color=WHITE, stroke_width=2,
            ).set_opacity(0.8)
            return VGroup(back, seat, big_wheel, small_wheel, frame)

        def make_robot_arm_icon():
            base = Rectangle(
                width=0.55, height=0.20,
                fill_color=ORANGE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ).move_to(DOWN * 0.45)
            lower = Rectangle(
                width=0.16, height=0.50,
                fill_color=ORANGE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.2,
            ).move_to(base.get_top() + UP * 0.25)
            elbow = Circle(
                radius=0.07,
                fill_color=PURPLE, fill_opacity=1, stroke_width=0,
            ).move_to(lower.get_top() + UP * 0.02)
            upper = Rectangle(
                width=0.14, height=0.45,
                fill_color=ORANGE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.2,
            ).move_to(elbow.get_top() + UP * 0.23)
            gripper = VGroup(
                Rectangle(
                    width=0.06, height=0.18,
                    fill_color=GREY_B, fill_opacity=1, stroke_width=0,
                ).move_to(upper.get_top() + UP * 0.09 + LEFT * 0.08),
                Rectangle(
                    width=0.06, height=0.18,
                    fill_color=GREY_B, fill_opacity=1, stroke_width=0,
                ).move_to(upper.get_top() + UP * 0.09 + RIGHT * 0.08),
            )
            return VGroup(base, lower, elbow, upper, gripper)

        def make_communication_icon():
            bubble = RoundedRectangle(
                width=0.95, height=0.60, corner_radius=0.18,
                fill_color=GREEN, fill_opacity=0.9,
                stroke_color=WHITE, stroke_width=2,
            )
            tail = Polygon(
                bubble.get_bottom() + LEFT * 0.15,
                bubble.get_bottom() + RIGHT * 0.10,
                bubble.get_bottom() + LEFT * 0.25 + DOWN * 0.20,
                fill_color=GREEN, fill_opacity=0.9,
                stroke_color=WHITE, stroke_width=1.5,
            )
            dots = VGroup(*[
                Circle(radius=0.05, fill_color=WHITE, fill_opacity=1, stroke_width=0)
                for _ in range(3)
            ]).arrange(RIGHT, buff=0.08).move_to(bubble.get_center())
            return VGroup(tail, bubble, dots)

        def make_device_block(icon, label):
            icon.scale_to_fit_height(0.75)
            if icon.width > 1.10:
                icon.scale_to_fit_width(1.10)
            label_text = Text(label, font_size=12, color=WHITE).scale_to_fit_width(1.7)
            return VGroup(icon, label_text).arrange(DOWN, buff=0.08)

        # ---------- previous scene composition ----------
        prev_title = Text(
            "Brain-Computer Interface (BCI)",
            font_size=36, weight="BOLD", color=YELLOW,
        ).scale_to_fit_width(10.5).move_to(UP * 3.0)

        prev_head_outline = Ellipse(
            width=1.9, height=2.4,
            fill_color=GREY, fill_opacity=0.12,
            stroke_color=WHITE, stroke_width=3,
        )
        prev_brain_icon = SVGMobject(ASSET_PATHS["brain"])
        prev_brain_icon.set_fill(PINK, opacity=0.9).set_stroke(PINK, width=0)
        prev_brain_icon.scale_to_fit_height(1.35)
        prev_brain_icon.move_to(prev_head_outline.get_center() + UP * 0.15)
        prev_head_group = VGroup(prev_head_outline, prev_brain_icon)
        prev_head_group.move_to(LEFT * 4.2 + DOWN * 0.2)

        prev_main_arrow = Arrow(
            prev_head_group.get_right() + RIGHT * 0.25,
            np.array([3.6, prev_head_group.get_center()[1], 0]),
            color=YELLOW, stroke_width=4, buff=0.30,
            max_tip_length_to_length_ratio=0.15,
        )

        prev_signal_on_arrow = make_wave(
            lambda x: 0.08 * np.sin(2 * np.pi * 3.0 * x) + 0.05 * np.sin(2 * np.pi * 7.0 * x),
            -3.3, 3.3, color=YELLOW, stroke_width=2.5,
        ).move_to(prev_main_arrow.get_center() + UP * 0.15)

        prev_device_data = [
            (make_computer_icon(), "Computer"),
            (make_wheelchair_icon(), "Wheelchair"),
            (make_robot_arm_icon(), "Robotic Arm"),
            (make_communication_icon(), "Communication System"),
        ]
        prev_device_blocks = [
            make_device_block(icon, label) for icon, label in prev_device_data
        ]
        prev_device_blocks_group = VGroup(*prev_device_blocks).arrange(DOWN, buff=0.35)
        prev_device_blocks_group.move_to(RIGHT * 5.3 + UP * 0.1)

        prev_branch_arrows = VGroup()
        prev_main_end = np.array([3.6, prev_head_group.get_center()[1], 0])
        for block in prev_device_blocks:
            arr = Arrow(
                prev_main_end,
                block.get_left() + LEFT * 0.10,
                color=GREY_B, stroke_width=2.5, buff=0.05,
                max_tip_length_to_length_ratio=0.25,
            )
            prev_branch_arrows.add(arr)

        prev_group = VGroup(
            prev_title,
            prev_head_group,
            prev_main_arrow,
            prev_signal_on_arrow,
            prev_device_blocks_group,
            prev_branch_arrows,
        )

        # ---------- new clean EEG head ----------
        head_outline = Ellipse(
            width=2.0, height=2.5,
            fill_color=GREY, fill_opacity=0.10,
            stroke_color=WHITE, stroke_width=3,
        )
        brain_icon = SVGMobject(ASSET_PATHS["brain"])
        brain_icon.set_fill(PINK, opacity=0.9).set_stroke(PINK, width=0)
        brain_icon.scale_to_fit_height(1.35)
        brain_icon.move_to(head_outline.get_center() + UP * 0.15)
        new_head_group = VGroup(head_outline, brain_icon)
        new_head_group.move_to(LEFT * 3.5 + DOWN * 0.2)

        eeg_label = Text("EEG", font_size=26, weight="BOLD", color=WHITE)
        eeg_label.next_to(new_head_group, DOWN, buff=0.25)

        trace1 = make_wave(
            lambda x: 0.10 * np.sin(2 * np.pi * 1.8 * x) + 0.08 * np.sin(2 * np.pi * 4.2 * x + 0.6),
            -0.45, 0.45, color=YELLOW, stroke_width=2.4,
        ).move_to(brain_icon.get_center() + UP * 0.08)
        trace2 = make_wave(
            lambda x: 0.08 * np.sin(2 * np.pi * 2.3 * x) + 0.09 * np.sin(2 * np.pi * 5.6 * x + 1.1),
            -0.35, 0.35, color=ORANGE, stroke_width=2.2,
        ).move_to(brain_icon.get_center() + DOWN * 0.10)
        eeg_traces = VGroup(trace1, trace2)

        eeg_phase = ValueTracker(0)
        eeg_phase.add_updater(lambda mob, dt: mob.set_value(mob.get_value() + dt * 2.2))
        eeg_traces.add_updater(
            lambda g: g.set_stroke(
                width=2.4 + 0.8 * np.sin(eeg_phase.get_value()),
                opacity=0.75 + 0.25 * np.sin(eeg_phase.get_value() * 0.9),
            )
        )

        self.add(prev_group, eeg_phase)

        # ---------- beat 1: 0.00-3.38 ----------
        self.play(FadeOut(prev_group), run_time=max(0.05, 1.8))
        self.remove(prev_group)
        self.play(FadeIn(new_head_group, eeg_traces, eeg_label), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.38))

        # gap 3.38-3.98
        self.wait(max(0.05, 0.60))

        # ---------- build observation blocks ----------
        obs_data = [
            ("Brain-State Monitoring", BLUE),
            ("Sleep Staging", TEAL),
            ("Epilepsy Diagnosis", ORANGE),
        ]
        obs_blocks = []
        for label, color in obs_data:
            rect = RoundedRectangle(
                width=2.8, height=0.7, corner_radius=0.10,
                fill_color=color, fill_opacity=0.25,
                stroke_color=color, stroke_width=2,
            )
            txt = Text(label, font_size=13, color=WHITE).scale_to_fit_width(2.4)
            txt.move_to(rect.get_center())
            wave_icon = make_wave(
                lambda x: 0.15 * np.sin(2 * np.pi * 1.5 * x) + 0.08 * np.sin(2 * np.pi * 3.0 * x),
                -0.45, 0.45, color=color, stroke_width=2.2,
            ).scale_to_fit_width(0.9).move_to(rect.get_top() + UP * 0.18)
            obs_blocks.append(VGroup(rect, txt, wave_icon))

        obs_blocks_group = VGroup(*obs_blocks).arrange(DOWN, buff=0.45)
        obs_blocks_group.move_to(RIGHT * 1.5 + DOWN * 0.1)

        obs_lines = VGroup()
        for block in obs_blocks:
            start = np.array([new_head_group.get_right()[0] + 0.2, block.get_center()[1], 0])
            end = block.get_left() + LEFT * 0.1
            line = Line(start, end, color=GREY_B, stroke_width=2).set_opacity(0.8)
            obs_lines.add(line)

        obs_title = Text(
            "Observing Brain Activity",
            font_size=22, weight="BOLD", color=TEAL,
        ).next_to(obs_blocks_group, UP, buff=0.45)

        # ---------- beat 2: 3.98-9.84 ----------
        self.play(Create(obs_lines), FadeIn(obs_blocks_group), run_time=max(0.05, 3.0))
        self.play(FadeIn(obs_title), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.86))

        # gap 9.84-10.86
        self.wait(max(0.05, 1.02))

        # ---------- beat 3: 10.86-14.94 ----------
        measure_label = Text(
            "EEG = Measurement Tool",
            font_size=20, weight="BOLD", color=GREEN,
        ).next_to(obs_blocks_group, DOWN, buff=0.5)

        self.play(
            obs_blocks_group.animate.set_opacity(0.5),
            obs_lines.animate.set_opacity(0.35),
            run_time=max(0.05, 1.2),
        )
        self.play(FadeIn(measure_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.88))

        # gap 14.94-15.84
        self.wait(max(0.05, 0.90))

        # ---------- beat 4: 15.84-19.14 ----------
        diff_label = Text(
            "Different Approach",
            font_size=26, weight="BOLD", color=ORANGE,
        ).next_to(new_head_group, UP, buff=1.1)

        self.play(
            FadeOut(obs_blocks_group),
            FadeOut(obs_lines),
            FadeOut(obs_title),
            FadeOut(measure_label),
            run_time=max(0.05, 1.8),
        )
        self.play(FadeIn(diff_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.50))

        # gap 19.14-19.82
        self.wait(max(0.05, 0.68))

        # ---------- beat 5: 19.82-21.76 ----------
        record_wave_icon = make_wave(
            lambda x: 0.15 * np.sin(2 * np.pi * 1.5 * x) + 0.08 * np.sin(2 * np.pi * 3.0 * x),
            -0.55, 0.55, color=YELLOW, stroke_width=2.6,
        ).scale_to_fit_width(1.3)
        record_wave_icon.move_to(new_head_group.get_top() + UP * 0.4)

        red_cross = Line(
            record_wave_icon.get_left() + DOWN * 0.18 + LEFT * 0.1,
            record_wave_icon.get_right() + UP * 0.18 + RIGHT * 0.1,
            color=RED, stroke_width=8,
        )
        not_just_label = Text(
            "Not just recording", font_size=20, weight="BOLD", color=RED,
        ).next_to(record_wave_icon, DOWN, buff=0.3)

        self.play(FadeIn(record_wave_icon), run_time=max(0.05, 0.4))
        self.play(
            Create(red_cross),
            FadeIn(not_just_label),
            head_outline.animate.set_stroke(color=WHITE, width=4, opacity=1),
            eeg_traces.animate.set_stroke(color=YELLOW, width=3.2),
            run_time=max(0.05, 0.8),
        )
        self.play(FadeOut(not_just_label), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.34))

        # gap 21.76-22.50
        self.wait(max(0.05, 0.74))

        # ---------- beat 6: 22.50-27.62 ----------
        device_outline = RoundedRectangle(
            width=1.5, height=1.1, corner_radius=0.08,
            fill_color=BLACK, fill_opacity=0.4,
            stroke_color=WHITE, stroke_width=3,
        ).move_to(RIGHT * 0.8 + DOWN * 0.2)

        command_arrow = Arrow(
            new_head_group.get_right() + RIGHT * 0.25,
            device_outline.get_left() + LEFT * 0.1,
            color=YELLOW, stroke_width=3, buff=0.2,
            max_tip_length_to_length_ratio=0.15,
        )
        commands_label = Text(
            "Commands", font_size=20, weight="BOLD", color=YELLOW,
        ).next_to(command_arrow, UP, buff=0.25)

        cmd_path_line = Line(
            command_arrow.get_start(), command_arrow.get_end(), stroke_width=0,
        )
        cmd_pulse_dots = VGroup(*[Dot(radius=0.07, color=YELLOW) for _ in range(3)])
        for i, dot in enumerate(cmd_pulse_dots):
            def update_cmd_dot(d, i=i):
                s = cmd_path_line.get_start()
                e = cmd_path_line.get_end()
                d.move_to(s + (e - s) * ((eeg_phase.get_value() * 0.7 + i / 3.0) % 1.0))
            dot.add_updater(update_cmd_dot)

        self.play(
            FadeOut(diff_label),
            FadeOut(record_wave_icon),
            FadeOut(red_cross),
            run_time=max(0.05, 0.8),
        )
        self.play(
            Create(command_arrow),
            FadeIn(device_outline),
            FadeIn(commands_label),
            run_time=max(0.05, 2.0),
        )
        self.add(cmd_pulse_dots)
        self.wait(max(0.05, 2.32))

        # gap 27.62-28.00
        self.wait(max(0.05, 0.38))

        # ---------- beat 7: 28.00-33.18 ----------
        title_bci = Text(
            "Brain-Computer Interface (BCI)",
            font_size=34, weight="BOLD", color=YELLOW,
        ).scale_to_fit_width(10.5).move_to(UP * 3.0)

        self.play(FadeIn(title_bci), run_time=max(0.05, 1.6))
        self.play(command_arrow.animate.set_stroke(color=YELLOW, width=5), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.58))

        # gap 33.18-33.90
        self.wait(max(0.05, 0.72))

        # ---------- beat 8: 33.90-39.28 ----------
        pathway_label = Text(
            "Direct Communication Pathway",
            font_size=20, weight="BOLD", color=YELLOW,
        ).scale_to_fit_width(4.5).move_to(commands_label.get_center())

        self.play(
            command_arrow.animate.set_stroke(color=YELLOW, width=8, opacity=1),
            Transform(commands_label, pathway_label),
            head_outline.animate.set_stroke(color=WHITE, width=4),
            device_outline.animate.set_stroke(color=YELLOW, width=3.5),
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 2.88))

        # gap 39.28-39.78
        self.wait(max(0.05, 0.50))

        # ---------- build four branching device icons ----------
        device_data = [
            (make_computer_icon(), "Computer"),
            (make_wheelchair_icon(), "Wheelchair"),
            (make_robot_arm_icon(), "Robotic Device"),
            (make_communication_icon(), "Communication System"),
        ]
        device_blocks = [
            make_device_block(icon, label) for icon, label in device_data
        ]
        device_blocks_group = VGroup(*device_blocks).arrange_in_grid(rows=2, cols=2, buff=0.55)
        if device_blocks_group.width > 4.2:
            device_blocks_group.scale_to_fit_width(4.2)
        device_blocks_group.move_to(RIGHT * 4.3 + DOWN * 0.1)
        device_blocks_group.set_opacity(0.35)

        branch_start = device_outline.get_right() + RIGHT * 0.20
        branch_arrows = VGroup()
        branch_path_lines = VGroup()
        for block in device_blocks:
            end = block.get_left() + LEFT * 0.10
            arr = Arrow(
                branch_start, end,
                color=GREY_B, stroke_width=2, buff=0.05,
                max_tip_length_to_length_ratio=0.25,
            ).set_opacity(0.35)
            path_line = Line(branch_start, end, stroke_width=0)
            branch_arrows.add(arr)
            branch_path_lines.add(path_line)

        # ---------- beat 9: 39.78-44.80 ----------
        self.play(FadeIn(device_blocks_group), FadeIn(branch_arrows), run_time=max(0.05, 1.0))
        self.play(
            device_blocks[0].animate.set_opacity(1),
            branch_arrows[0].animate.set_opacity(1).set_stroke(color=YELLOW, width=2.5),
            run_time=max(0.05, 1.2),
        )
        self.play(
            device_blocks[1].animate.set_opacity(1),
            branch_arrows[1].animate.set_opacity(1).set_stroke(color=YELLOW, width=2.5),
            run_time=max(0.05, 1.2),
        )
        self.play(
            device_blocks[2].animate.set_opacity(1),
            branch_arrows[2].animate.set_opacity(1).set_stroke(color=YELLOW, width=2.5),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.42))

        # gap 44.80-45.36
        self.wait(max(0.05, 0.56))

        # ---------- beat 10: 45.36-48.30 ----------
        self.play(
            device_blocks[3].animate.set_opacity(1),
            branch_arrows[3].animate.set_opacity(1).set_stroke(color=YELLOW, width=2.5),
            run_time=max(0.05, 0.8),
        )
        for i in range(4):
            pulse_dot = Dot(radius=0.07, color=YELLOW).move_to(branch_path_lines[i].get_start())
            self.add(pulse_dot)
            self.play(pulse_dot.animate.move_to(branch_path_lines[i].get_end()), run_time=max(0.05, 0.3))
            self.remove(pulse_dot)
        self.wait(max(0.05, 0.94))

        # final hold 48.30-49.20
        self.wait(max(0.05, 0.90))