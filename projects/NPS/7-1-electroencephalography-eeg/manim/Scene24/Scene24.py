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


class Scene24(Scene):
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

        def make_block(label, color, width=1.6, height=0.9):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.1,
                fill_color=color, fill_opacity=0.35,
                stroke_color=color, stroke_width=2.5,
            )
            txt = Text(label, font_size=14, weight="BOLD", color=WHITE)
            txt.scale_to_fit_width(width - 0.35)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

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

        # ---------- previous scene composition (opening) ----------
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
        self.add(prev_group)

        # ---------- definition box ----------
        neutral = WHITE
        amber = GOLD

        seg_intro = Text("BCI = system that ", color=neutral, font_size=26)
        seg_acquires = Text("acquires brain signals", color=neutral, font_size=26)
        seg_comma = Text(",", color=neutral, font_size=26)
        line1 = VGroup(seg_intro, seg_acquires, seg_comma).arrange(RIGHT, buff=0.06)

        seg_processes = Text("processes them", color=neutral, font_size=26)
        seg_and = Text(", and ", color=neutral, font_size=26)
        seg_converts = Text("converts them into commands", color=neutral, font_size=26)
        seg_that = Text(" that ", color=neutral, font_size=26)
        seg_control = Text("control an external device", color=neutral, font_size=26)
        seg_period = Text(".", color=neutral, font_size=26)
        line2 = VGroup(
            seg_processes, seg_and, seg_converts, seg_that, seg_control, seg_period
        ).arrange(RIGHT, buff=0.06)

        def_text_group = VGroup(line1, line2).arrange(DOWN, buff=0.18)
        def_text_group.scale_to_fit_width(9.0)

        def_rect = SurroundingRectangle(
            def_text_group,
            color=WHITE,
            stroke_width=2,
            buff=0.35,
            corner_radius=0.1,
            fill_color=BLACK,
            fill_opacity=0.25,
        )
        def_box = VGroup(def_rect, def_text_group).move_to(ORIGIN)

        # ---------- beat 1: 0.00-2.38 ----------
        self.play(FadeOut(prev_group), run_time=max(0.05, 1.2))
        self.remove(prev_group)
        self.play(FadeIn(def_box), run_time=max(0.05, 1.18))

        # gap 2.38-2.62
        self.wait(max(0.05, 0.24))

        # ---------- beat 2: 2.62-5.34 ----------
        wave_icon_small = SVGMobject(ASSET_PATHS["soundwave"])
        wave_icon_small.set_color(GOLD)
        wave_icon_small.scale_to_fit_height(0.55)
        wave_icon_small.next_to(def_box, UP, buff=0.30)

        self.play(
            FadeIn(wave_icon_small),
            seg_acquires.animate.set_color(GOLD),
            run_time=max(0.05, 1.0),
        )
        self.play(wave_icon_small.animate.scale(1.15), run_time=max(0.05, 0.4))
        self.play(wave_icon_small.animate.scale(1 / 1.15), run_time=max(0.05, 0.4))
        self.play(wave_icon_small.animate.scale(1.15), run_time=max(0.05, 0.4))
        self.play(wave_icon_small.animate.scale(1 / 1.15), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.12))

        # ---------- beat 3: 5.34-9.76 ----------
        device_outline = RoundedRectangle(
            width=1.0, height=0.8, corner_radius=0.06,
            stroke_color=WHITE, stroke_width=2.5,
            fill_color=BLACK, fill_opacity=0.35,
        )
        device_outline.move_to(def_box.get_right() + RIGHT * 1.0)

        command_arrow = Arrow(
            seg_converts.get_right() + RIGHT * 0.05,
            device_outline.get_left() + LEFT * 0.05,
            color=WHITE, stroke_width=2.5, buff=0.05,
            max_tip_length_to_length_ratio=0.2,
        )

        self.play(
            seg_acquires.animate.set_color(WHITE),
            seg_processes.animate.set_color(GOLD),
            FadeOut(wave_icon_small),
            run_time=max(0.05, 1.2),
        )
        self.play(
            seg_processes.animate.set_color(WHITE),
            seg_converts.animate.set_color(GOLD),
            run_time=max(0.05, 1.2),
        )
        self.play(
            seg_converts.animate.set_color(WHITE),
            seg_control.animate.set_color(GOLD),
            run_time=max(0.05, 1.2),
        )
        self.play(
            FadeIn(device_outline),
            Create(command_arrow),
            run_time=max(0.05, 0.82),
        )

        # gap 9.76-10.64
        self.wait(max(0.05, 0.88))

        # ---------- beat 4: 10.64-15.48 ----------
        # traditional interface panel
        keyboard_rect = Rectangle(
            width=1.5, height=0.45,
            fill_color=BLUE, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        )
        keyboard_keys = VGroup(*[
            Rectangle(
                width=0.09, height=0.09,
                fill_color=WHITE, fill_opacity=0.7,
                stroke_width=0,
            )
            for _ in range(10)
        ]).arrange_in_grid(rows=2, cols=5, buff=0.05)
        keyboard_keys.move_to(keyboard_rect.get_center())
        keyboard_icon_trad = VGroup(keyboard_rect, keyboard_keys)

        mouse_trad = RoundedRectangle(
            width=0.5, height=0.75, corner_radius=0.15,
            fill_color=GREY_B, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        )
        hand_trad = SVGMobject(ASSET_PATHS["hand"])
        hand_trad.set_fill(ORANGE, opacity=0.9).set_stroke(WHITE, width=1.5)
        hand_trad.scale_to_fit_height(0.6)
        hand_trad.move_to(mouse_trad.get_top() + UP * 0.15)

        trad_visual = VGroup(keyboard_icon_trad, mouse_trad).arrange(RIGHT, buff=0.7)
        # move the hand relative to the mouse after arranging
        hand_trad.move_to(mouse_trad.get_top() + UP * 0.15)
        trad_panel = VGroup(trad_visual, hand_trad)
        trad_panel.move_to(LEFT * 4.6 + DOWN * 1.7)

        trad_label = Text(
            "Traditional Interface", font_size=20, weight="BOLD", color=WHITE
        )
        trad_label.next_to(trad_panel, DOWN, buff=0.25)
        trad_panel_group = VGroup(trad_panel, trad_label)

        # muscle movement icon
        upper_arm = Rectangle(
            width=0.18, height=0.6,
            fill_color=RED, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(UP * 0.35)
        forearm = Rectangle(
            width=0.6, height=0.18,
            fill_color=RED, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(RIGHT * 0.3 + UP * 0.0)
        elbow = Circle(
            radius=0.10,
            fill_color=RED, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(UP * 0.0)
        muscle_icon = VGroup(upper_arm, forearm, elbow)
        muscle_label = Text(
            "Muscle Movement", font_size=16, weight="BOLD", color=GREY_B
        )
        muscle_label.next_to(muscle_icon, DOWN, buff=0.15)
        muscle_group = VGroup(muscle_icon, muscle_label)
        muscle_group.next_to(trad_panel_group, UP, buff=0.15).shift(RIGHT * 0.5)

        self.play(
            def_box.animate.scale(0.65).move_to(UP * 2.8),
            FadeOut(command_arrow),
            run_time=max(0.05, 1.0),
        )
        self.play(FadeIn(trad_panel_group), run_time=max(0.05, 1.4))
        self.play(FadeIn(muscle_group), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.24))

        # ---------- beat 5: 15.48-21.26 ----------
        # three labeled icons for traditional input methods
        def make_labeled_icon(shape_group, label, color):
            shape_group.set_fill(color, opacity=0.9)
            shape_group.set_stroke(WHITE, width=1.5)
            txt = Text(label, font_size=13, color=WHITE)
            txt.scale_to_fit_width(1.5)
            txt.next_to(shape_group, DOWN, buff=0.1)
            return VGroup(shape_group, txt)

        # keyboard icon
        kb_icon_rect = Rectangle(
            width=1.0, height=0.35,
            fill_color=BLUE, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        )
        kb_icon_keys = VGroup(*[
            Rectangle(
                width=0.06, height=0.06,
                fill_color=WHITE, fill_opacity=0.7, stroke_width=0,
            )
            for _ in range(8)
        ]).arrange_in_grid(rows=2, cols=4, buff=0.04)
        kb_icon_keys.move_to(kb_icon_rect.get_center())
        kb_icon_group = VGroup(kb_icon_rect, kb_icon_keys)
        icon_keyboard = make_labeled_icon(kb_icon_group, "Keyboard", BLUE)

        # mouse icon
        mouse_icon_shape = RoundedRectangle(
            width=0.45, height=0.65, corner_radius=0.12,
            fill_color=GREY_B, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        )
        icon_mouse = make_labeled_icon(mouse_icon_shape, "Mouse", GREY_B)

        # touchscreen icon
        tablet_rect = RoundedRectangle(
            width=0.7, height=1.0, corner_radius=0.06,
            fill_color=TEAL, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        )
        tablet_screen = RoundedRectangle(
            width=0.55, height=0.8, corner_radius=0.03,
            fill_color=BLACK, fill_opacity=0.7, stroke_width=0,
        ).move_to(tablet_rect.get_center())
        tablet_group = VGroup(tablet_rect, tablet_screen)
        icon_touchscreen = make_labeled_icon(tablet_group, "Touchscreen", TEAL)

        icon_keyboard.next_to(trad_panel_group, DOWN, buff=0.55).shift(LEFT * 0.7)
        icon_mouse.next_to(icon_keyboard, RIGHT, buff=0.6)
        icon_touchscreen.next_to(icon_mouse, RIGHT, buff=0.6)

        trad_side_group = VGroup(
            trad_panel_group,
            muscle_group,
            icon_keyboard,
            icon_mouse,
            icon_touchscreen,
        )

        # BCI panel objects
        bci_head_ellipse = Ellipse(
            width=1.6, height=2.0,
            fill_color=GREY, fill_opacity=0.10,
            stroke_color=WHITE, stroke_width=3,
        )
        bci_brain = SVGMobject(ASSET_PATHS["brain"])
        bci_brain.set_fill(PINK, opacity=0.9).set_stroke(PINK, width=0)
        bci_brain.scale_to_fit_height(1.1)
        bci_brain.move_to(bci_head_ellipse.get_center() + UP * 0.1)
        bci_head_group = VGroup(bci_head_ellipse, bci_brain)

        bci_label = Text("BCI", font_size=22, weight="BOLD", color=YELLOW)
        bci_label.next_to(bci_head_group, DOWN, buff=0.2)
        bci_panel = VGroup(bci_head_group, bci_label)
        bci_panel.move_to(RIGHT * 4.1 + DOWN * 0.3)

        desired_device_pos = RIGHT * 6.0 + DOWN * 0.3
        bci_arrow = Arrow(
            bci_brain.get_right() + RIGHT * 0.10,
            desired_device_pos + LEFT * 0.55,
            color=YELLOW, stroke_width=5, buff=0.20,
            max_tip_length_to_length_ratio=0.12,
        )
        bci_arrow_label = Text(
            "Direct Brain Activity", font_size=15, color=YELLOW
        ).scale_to_fit_width(2.4)
        bci_arrow_label.next_to(bci_arrow, UP, buff=0.1)

        self.play(FadeIn(icon_keyboard), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.58))
        self.play(FadeIn(icon_mouse), run_time=max(0.05, 0.66))
        self.play(FadeIn(icon_touchscreen), run_time=max(0.05, 0.66))
        self.play(device_outline.animate.move_to(desired_device_pos), run_time=max(0.05, 0.38))
        self.play(
            FadeIn(bci_panel),
            FadeIn(bci_arrow),
            FadeIn(bci_arrow_label),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 1.5))

        bci_full_group = VGroup(bci_panel, bci_arrow, bci_arrow_label, device_outline)

        # gap 21.26-22.00
        self.wait(max(0.05, 0.74))

        # ---------- beat 6: 22.00-25.74 ----------
        self.play(FadeOut(trad_side_group), run_time=max(0.05, 0.9))
        self.play(
            bci_full_group.animate.scale(1.25).move_to(ORIGIN + DOWN * 0.3),
            run_time=max(0.05, 1.2),
        )

        # continuous EEG waveform after expansion
        start_pt = bci_brain.get_right() + RIGHT * 0.1
        end_pt = device_outline.get_left() + LEFT * 0.1
        distance = np.linalg.norm(end_pt - start_pt)
        eeg_wave = make_wave(
            lambda x: 0.12 * np.sin(2 * np.pi * 2.0 * x) + 0.05 * np.sin(2 * np.pi * 5.0 * x),
            -0.5, 0.5,
            color=YELLOW, stroke_width=2.8,
        )
        eeg_wave.scale_to_fit_width(distance)
        eeg_wave.move_to((start_pt + end_pt) / 2)

        eeg_recording_label = Text(
            "Continuous EEG Recording", font_size=16, color=YELLOW
        )
        eeg_recording_label.next_to(eeg_wave, DOWN, buff=0.2)

        eeg_phase = ValueTracker(0)
        eeg_phase.add_updater(lambda mob, dt: mob.set_value(mob.get_value() + dt * 1.5))
        eeg_wave.add_updater(
            lambda m: m.set_stroke(
                width=2.8 + 0.6 * np.sin(eeg_phase.get_value()),
                opacity=0.75 + 0.25 * np.sin(eeg_phase.get_value() * 0.8),
            )
        )
        self.add(eeg_phase)

        self.play(
            bci_brain.animate.set_fill(YELLOW, opacity=1).set_stroke(YELLOW, width=1),
            bci_head_ellipse.animate.set_stroke(YELLOW, width=5),
            Create(eeg_wave),
            FadeIn(eeg_recording_label),
            run_time=max(0.05, 1.34),
        )
        self.wait(max(0.05, 0.30))

        # ---------- beat 7: 25.74-29.42 ----------
        feature_block = make_block("Feature Extraction", BLUE, width=1.6)
        feature_block.move_to(LEFT * 0.9 + DOWN * 0.2)

        self.play(FadeIn(feature_block), run_time=max(0.05, 0.8))

        feature_markers = VGroup(
            Square(
                side_length=0.16,
                fill_color=GREEN, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ),
            Triangle(
                fill_color=ORANGE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ).scale(0.18),
        ).arrange(RIGHT, buff=0.15)
        feature_markers.move_to(feature_block.get_right() + RIGHT * 0.25)

        self.play(FadeIn(feature_markers), run_time=max(0.05, 0.25))
        self.play(
            feature_markers.animate.shift(RIGHT * 1.8).set_opacity(0.6),
            run_time=max(0.05, 1.55),
        )
        self.play(FadeOut(feature_markers), run_time=max(0.05, 0.28))
        self.wait(max(0.05, 0.80))

        # ---------- beat 8: 29.42-33.24 ----------
        command_block = make_block("Command Translation", PURPLE, width=1.6)
        command_block.move_to(RIGHT * 1.3 + DOWN * 0.2)

        external_device_label = Text(
            "External Device", font_size=16, color=YELLOW
        )
        external_device_label.next_to(device_outline, DOWN, buff=0.15)

        self.play(FadeIn(command_block), run_time=max(0.05, 0.7))

        stream_markers = VGroup(
            Square(
                side_length=0.15,
                fill_color=GREEN, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ),
            Triangle(
                fill_color=ORANGE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ).scale(0.17),
        ).arrange(RIGHT, buff=0.15)
        stream_markers.move_to(feature_block.get_right() + RIGHT * 0.25)

        self.play(FadeIn(stream_markers), run_time=max(0.05, 0.2))
        self.play(
            stream_markers.animate.move_to(command_block.get_left() + LEFT * 0.1),
            run_time=max(0.05, 0.6),
        )
        self.remove(stream_markers)

        self.play(FadeIn(external_device_label), run_time=max(0.05, 0.3))

        for _ in range(3):
            pulse = Dot(radius=0.08, color=YELLOW)
            pulse.move_to(command_block.get_right() + RIGHT * 0.1)
            self.play(pulse.animate.move_to(device_outline.get_left()), run_time=max(0.05, 0.4))
            self.play(
                device_outline.animate.set_stroke(color=YELLOW, width=5),
                run_time=max(0.05, 0.1),
            )
            self.play(
                device_outline.animate.set_stroke(color=WHITE, width=2.5),
                run_time=max(0.05, 0.05),
            )
            self.remove(pulse)

        self.wait(max(0.05, 0.37))

        # gap 33.24-34.12
        self.wait(max(0.05, 0.88))

        # ---------- beat 9: 34.12-38.34 ----------
        # top-down head illustration
        top_head_outline = Ellipse(
            width=4.0, height=3.0,
            fill_color=GREY, fill_opacity=0.08,
            stroke_color=WHITE, stroke_width=3,
        )
        left_hemi = Ellipse(
            width=1.5, height=2.3,
            fill_color=PINK, fill_opacity=0.35,
            stroke_color=PINK, stroke_width=2,
        ).move_to(LEFT * 0.9 + UP * 0.1)
        right_hemi = Ellipse(
            width=1.5, height=2.3,
            fill_color=PINK, fill_opacity=0.35,
            stroke_color=PINK, stroke_width=2,
        ).move_to(RIGHT * 0.9 + UP * 0.1)
        mid_line = Line(
            top_head_outline.get_top(), top_head_outline.get_bottom(),
            color=WHITE, stroke_width=1, stroke_opacity=0.5,
        )
        top_brain_group = VGroup(left_hemi, right_hemi, mid_line)
        top_head_group = VGroup(top_head_outline, top_brain_group)
        top_head_group.move_to(UP * 1.5)

        left_hand_label = Text(
            "Left Hand", font_size=20, weight="BOLD", color=GREY_B
        )
        left_hand_label.next_to(left_hemi, LEFT, buff=0.35).shift(UP * 0.4)
        right_hand_label = Text(
            "Right Hand", font_size=20, weight="BOLD", color=GREY_B
        )
        right_hand_label.next_to(right_hemi, RIGHT, buff=0.35).shift(UP * 0.4)

        # thought bubble above head with hand inside
        bubble_dots = VGroup(*[
            Circle(
                radius=0.05, fill_color=WHITE, fill_opacity=0.8,
                stroke_width=0,
            )
            for _ in range(3)
        ]).arrange(DOWN, buff=0.15)
        bubble_dots.move_to(top_head_outline.get_top() + UP * 0.5)

        bubble_circle = Circle(
            radius=0.55,
            fill_color=WHITE, fill_opacity=0.12,
            stroke_color=WHITE, stroke_width=2,
        )
        bubble_circle.move_to(bubble_dots.get_top() + UP * 0.55)

        hand_in_bubble = SVGMobject(ASSET_PATHS["hand"])
        hand_in_bubble.set_fill(YELLOW, opacity=0.9).set_stroke(WHITE, width=1)
        hand_in_bubble.scale_to_fit_height(0.55)
        hand_in_bubble.move_to(bubble_circle.get_center())
        thought_bubble_group = VGroup(bubble_dots, bubble_circle, hand_in_bubble)

        old_bci_comp = VGroup(
            bci_full_group,
            eeg_wave,
            eeg_recording_label,
            feature_block,
            command_block,
            external_device_label,
        )

        self.play(
            FadeOut(old_bci_comp),
            FadeOut(def_box),
            run_time=max(0.05, 1.1),
        )
        self.play(
            FadeIn(top_head_group),
            FadeIn(left_hand_label),
            FadeIn(right_hand_label),
            run_time=max(0.05, 1.5),
        )
        self.play(FadeIn(thought_bubble_group), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.92))

        # ---------- beat 10: 38.34-44.92 ----------
        def make_left_hand_wave():
            vm = VMobject()
            vm.set_stroke(color=GOLD, width=3, opacity=1)
            x = np.linspace(-1.0, 1.0, 500)
            y = np.zeros_like(x)
            for i, xi in enumerate(x):
                if xi < -0.3:
                    y[i] = 0.05 * np.sin(2 * np.pi * 1.8 * xi)
                elif xi < -0.1:
                    y[i] = -0.4 * ((xi + 0.3) / 0.2)
                elif xi < 0.1:
                    y[i] = -0.4 + 0.7 * ((xi + 0.1) / 0.2)
                else:
                    y[i] = 0.05 * np.sin(2 * np.pi * 1.8 * xi) + 0.08
            vm.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return vm

        right_hand_trace = make_wave(
            lambda x: 0.03 * np.sin(2 * np.pi * 1.2 * x) + 0.02 * np.sin(2 * np.pi * 2.4 * x),
            -0.5, 0.5,
            color=GREY_B, stroke_width=2.0,
        )
        left_hand_trace = make_left_hand_wave()

        left_hand_trace.scale_to_fit_width(2.2)
        right_hand_trace.scale_to_fit_width(2.2)

        left_hand_trace.move_to(LEFT * 2.2 + DOWN * 0.7)
        right_hand_trace.move_to(RIGHT * 2.2 + DOWN * 0.7)

        left_eeg_label = Text(
            "Left-Hand EEG", font_size=16, weight="BOLD", color=WHITE
        )
        left_eeg_label.next_to(left_hand_trace, DOWN, buff=0.2)
        right_eeg_label = Text(
            "Right-Hand EEG", font_size=16, weight="BOLD", color=GREY_B
        )
        right_eeg_label.next_to(right_hand_trace, DOWN, buff=0.2)

        classifier_block = make_block("Classifier", GREEN, width=1.8)
        classifier_block.move_to(DOWN * 2.7)

        left_feed_arrow = Arrow(
            left_hand_trace.get_bottom() + DOWN * 0.1,
            classifier_block.get_top() + UP * 0.2 + LEFT * 0.4,
            color=GREY_B, stroke_width=2.5, buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )
        right_feed_arrow = Arrow(
            right_hand_trace.get_bottom() + DOWN * 0.1,
            classifier_block.get_top() + UP * 0.2 + RIGHT * 0.4,
            color=GREY_B, stroke_width=2.5, buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        self.play(
            left_hand_label.animate.set_color(GOLD),
            right_hand_label.animate.set_color(GREY_B),
            FadeIn(left_hand_trace),
            FadeIn(right_hand_trace),
            FadeIn(left_eeg_label),
            FadeIn(right_eeg_label),
            run_time=max(0.05, 2.0),
        )
        self.play(
            FadeIn(classifier_block),
            Create(left_feed_arrow),
            Create(right_feed_arrow),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 3.08))

        # ---------- beat 11: 44.92-49.26 ----------
        axis_line = Line(
            LEFT * 2.8 + DOWN * 3.2,
            RIGHT * 2.8 + DOWN * 3.2,
            color=WHITE, stroke_width=2,
        )

        cursor = Polygon(
            np.array([0.0, 0.0, 0.0]),
            np.array([0.18, -0.06, 0.0]),
            np.array([0.03, 0.18, 0.0]),
            fill_color=WHITE, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1,
        )
        cursor.move_to(ORIGIN + DOWN * 3.2)

        move_arrow = Arrow(
            classifier_block.get_bottom() + DOWN * 0.1,
            cursor.get_top() + UP * 0.2,
            color=YELLOW, stroke_width=5, buff=0.1,
            max_tip_length_to_length_ratio=0.15,
        )
        move_label = Text(
            "Move Cursor Left", font_size=16, color=YELLOW
        ).scale_to_fit_width(1.8)
        move_label.next_to(move_arrow, RIGHT, buff=0.1)

        self.play(Create(axis_line), FadeIn(cursor), run_time=max(0.05, 0.6))
        self.play(
            Create(move_arrow),
            FadeIn(move_label),
            run_time=max(0.05, 1.0),
        )
        self.play(cursor.animate.shift(LEFT * 0.85), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.54))

        hand_classification_group = VGroup(
            top_head_group,
            left_hand_label,
            right_hand_label,
            thought_bubble_group,
            left_hand_trace,
            right_hand_trace,
            left_eeg_label,
            right_eeg_label,
            classifier_block,
            left_feed_arrow,
            right_feed_arrow,
            axis_line,
            cursor,
            move_arrow,
            move_label,
        )

        # ---------- beat 12: 49.26-56.25 ----------
        # set all three definition phrases highlighted for the reappearance
        seg_acquires.set_color(GOLD)
        seg_processes.set_color(GOLD)
        seg_converts.set_color(GOLD)
        seg_intro.set_color(WHITE)
        seg_comma.set_color(WHITE)
        seg_and.set_color(WHITE)
        seg_that.set_color(WHITE)
        seg_control.set_color(WHITE)
        seg_period.set_color(WHITE)

        # final end-to-end pipeline
        final_head_outline = Ellipse(
            width=1.7, height=2.2,
            fill_color=GREY, fill_opacity=0.10,
            stroke_color=WHITE, stroke_width=3,
        )
        final_brain = SVGMobject(ASSET_PATHS["brain"])
        final_brain.set_fill(PINK, opacity=0.9).set_stroke(PINK, width=0)
        final_brain.scale_to_fit_height(1.15)
        final_brain.move_to(final_head_outline.get_center() + UP * 0.15)
        final_head_group = VGroup(final_head_outline, final_brain)
        final_head_group.move_to(LEFT * 5.2 + DOWN * 0.3)

        final_feature_block = make_block("Feature Extraction", BLUE, width=1.5)
        final_feature_block.move_to(LEFT * 1.5 + DOWN * 0.3)

        final_command_block = make_block("Command Translation", PURPLE, width=1.7)
        final_command_block.move_to(RIGHT * 1.5 + DOWN * 0.3)

        final_device_outline = RoundedRectangle(
            width=1.1, height=0.9, corner_radius=0.06,
            stroke_color=WHITE, stroke_width=2.5,
            fill_color=BLACK, fill_opacity=0.35,
        )
        final_device_outline.move_to(RIGHT * 5.1 + DOWN * 0.3)

        # EEG waveform trace between brain and feature extraction
        start_final = final_head_group.get_right() + RIGHT * 0.2
        end_final = final_feature_block.get_left() + LEFT * 0.1
        dist_final = np.linalg.norm(end_final - start_final)
        final_eeg_wave = make_wave(
            lambda x: 0.10 * np.sin(2 * np.pi * 2.2 * x) + 0.04 * np.sin(2 * np.pi * 5.0 * x),
            -0.5, 0.5,
            color=YELLOW, stroke_width=2.6,
        )
        final_eeg_wave.scale_to_fit_width(dist_final)
        final_eeg_wave.move_to((start_final + end_final) / 2)

        # continuous flowing arrow labeled Direct Interaction
        final_flow_arrow = Arrow(
            final_head_group.get_right() + RIGHT * 0.2 + DOWN * 1.6,
            final_device_outline.get_left() + LEFT * 0.1 + DOWN * 1.6,
            color=YELLOW, stroke_width=5, buff=0.2,
            max_tip_length_to_length_ratio=0.10,
        )
        final_flow_label = Text(
            "Direct Interaction", font_size=18, weight="BOLD", color=YELLOW
        )
        final_flow_label.next_to(final_flow_arrow, DOWN, buff=0.15)

        final_pipeline_group = VGroup(
            final_head_group,
            final_eeg_wave,
            final_feature_block,
            final_command_block,
            final_device_outline,
            final_flow_arrow,
            final_flow_label,
        )

        self.play(FadeOut(hand_classification_group), run_time=max(0.05, 1.0))
        self.play(FadeIn(def_box), run_time=max(0.05, 0.8))
        self.play(FadeIn(final_pipeline_group), run_time=max(0.05, 1.6))

        # gentle sequential pulse
        final_pulse_targets = [
            final_head_group,
            final_eeg_wave,
            final_feature_block,
            final_command_block,
            final_device_outline,
            final_flow_arrow,
        ]
        for target in final_pulse_targets:
            self.play(target.animate.scale(1.04), run_time=max(0.05, 0.25))
            self.play(target.animate.scale(1 / 1.04), run_time=max(0.05, 0.25))

        self.wait(max(0.05, 0.59))