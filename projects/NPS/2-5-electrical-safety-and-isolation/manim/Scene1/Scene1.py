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


class Scene1(Scene):
    def make_shield(self, color):
        shield = Polygon(
            np.array([-0.4, 0.35, 0]),
            np.array([0.4, 0.35, 0]),
            np.array([0.4, -0.15, 0]),
            np.array([0.25, -0.15, 0]),
            np.array([0, -0.65, 0]),
            np.array([-0.25, -0.15, 0]),
            np.array([-0.4, -0.15, 0]),
            stroke_width=3,
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
        )
        return shield

    def make_lightning(self, color=YELLOW, scale=1.0):
        bolt = Polygon(
            np.array([0.08, 0.22, 0]) * scale,
            np.array([-0.20, -0.06, 0]) * scale,
            np.array([0.00, -0.06, 0]) * scale,
            np.array([-0.08, -0.28, 0]) * scale,
            np.array([0.24, 0.08, 0]) * scale,
            np.array([0.04, 0.08, 0]) * scale,
            stroke_width=2,
            fill_color=color,
            fill_opacity=1,
            stroke_color=color,
        )
        return bolt

    def make_wave(self, color=YELLOW, width=1.2, height=0.3, stroke_width=5, irregular=False):
        wave = VMobject()
        wave.set_stroke(color=color, width=stroke_width, opacity=1)
        pts = []
        n = 60
        for i in range(n + 1):
            x = -width / 2 + width * i / n
            if irregular:
                y = height * (
                    np.sin(4 * PI * (x + width / 2) / width)
                    + 0.25 * np.sin(13 * PI * (x + width / 2) / width)
                )
            else:
                y = height * np.sin(4 * PI * (x + width / 2) / width)
            pts.append(np.array([x, y, 0]))
        wave.set_points_as_corners(pts)
        return wave

    def make_equipment_box_with_plug(self):
        box = Rectangle(
            width=1.4,
            height=0.9,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        plug_base = Rectangle(
            width=0.5,
            height=0.15,
            fill_color=GREY,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
        ).move_to(box.get_top() + UP * 0.1)
        prong1 = Line(
            plug_base.get_top() + UP * 0.05,
            plug_base.get_top() + UP * 0.3,
            color=WHITE,
            stroke_width=3,
        )
        prong2 = prong1.copy().shift(RIGHT * 0.18)
        prong3 = prong1.copy().shift(LEFT * 0.18)
        plug_icon = VGroup(plug_base, prong1, prong2, prong3)
        return VGroup(box, plug_icon)

    def make_jagged_arrow(self, start, end, color=RED, stroke_width=6):
        jagged = VMobject()
        jagged.set_stroke(color=color, width=stroke_width)
        n = 12
        pts = []
        direction = np.array(end) - np.array(start)
        perp = np.array([-direction[1], direction[0], 0])
        norm = np.linalg.norm(perp)
        if norm > 0:
            perp = perp / norm
        for i in range(n + 1):
            t = i / n
            base = np.array(start) * (1 - t) + np.array(end) * t
            if i == 0 or i == n:
                offset = 0.0
            else:
                offset = 0.15 * np.sin(10 * PI * t)
            pts.append(base + perp * offset)
        jagged.set_points_as_corners(pts)

        dir_vec = np.array(end) - np.array(start)
        angle = np.arctan2(dir_vec[1], dir_vec[0])
        arrowhead = Polygon(
            np.array(end),
            np.array(end) - 0.3 * np.array([np.cos(angle - 0.4), np.sin(angle - 0.4), 0]),
            np.array(end) - 0.3 * np.array([np.cos(angle + 0.4), np.sin(angle + 0.4), 0]),
            fill_color=color,
            fill_opacity=1,
            stroke_color=color,
            stroke_width=2,
        )
        return VGroup(jagged, arrowhead)

    def make_eeg_diagram(self):
        head_outline = Circle(
            radius=1.0,
            stroke_color=WHITE,
            stroke_width=3,
            fill_opacity=0,
        ).move_to(LEFT * 2.2)
        nose = Line(
            head_outline.get_right() + DOWN * 0.2,
            head_outline.get_right() + RIGHT * 0.35 + DOWN * 0.4,
            color=WHITE,
            stroke_width=3,
        )
        electrodes = VGroup()
        for angle in [70, 95, 120, 145]:
            dx = 1.0 * np.cos(angle * PI / 180)
            dy = 1.0 * np.sin(angle * PI / 180)
            electrode = Circle(
                radius=0.1,
                fill_color=TEAL,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1,
            ).move_to(head_outline.get_center() + np.array([dx, dy, 0]))
            electrodes.add(electrode)
        cable_start = electrodes[0].get_center()
        equipment = self.make_equipment_box_with_plug().move_to(RIGHT * 4.5)
        cable = Line(cable_start, equipment.get_left() + LEFT * 0.2, color=GREY, stroke_width=4)
        label = Text("EEG", font_size=36, color=YELLOW)
        label.next_to(head_outline, UP, buff=0.4)
        return VGroup(head_outline, nose, electrodes, cable, equipment, label)

    def make_emg_diagram(self):
        outer = Ellipse(
            width=1.8,
            height=1.4,
            fill_color=MAROON,
            fill_opacity=0.45,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(LEFT * 2.2)
        inner = Ellipse(
            width=1.25,
            height=0.9,
            fill_color=PINK,
            fill_opacity=0.35,
            stroke_color=GREY,
            stroke_width=1,
        ).move_to(outer.get_center())

        skin_needle = Line(
            outer.get_top() + UP * 0.05,
            outer.get_top() + UP * 0.25,
            color=YELLOW,
            stroke_width=3,
        )
        muscle_needle = Line(
            outer.get_top() + DOWN * 0.1,
            inner.get_center() + UP * 0.1,
            color=YELLOW,
            stroke_width=3,
        )
        muscle_tip = Dot(muscle_needle.get_end(), radius=0.06, color=YELLOW)

        equipment = self.make_equipment_box_with_plug().move_to(RIGHT * 4.5)
        cable = Line(
            skin_needle.get_center(),
            equipment.get_left() + LEFT * 0.2,
            color=GREY,
            stroke_width=4,
        )
        label = Text("EMG", font_size=36, color=YELLOW)
        label.next_to(outer, UP, buff=0.4)
        return VGroup(outer, inner, skin_needle, muscle_needle, muscle_tip, cable, equipment, label)

    def make_ecog_diagram(self):
        brain = SVGMobject(
            ASSET_PATHS["brain"],
            fill_opacity=0,
            stroke_color=WHITE,
            stroke_width=2,
        ).scale_to_fit_height(2.0).move_to(LEFT * 2.2)

        grid_dots = VGroup()
        for i in range(4):
            for j in range(3):
                dot = Circle(
                    radius=0.06,
                    fill_color=TEAL,
                    fill_opacity=1,
                    stroke_color=WHITE,
                    stroke_width=0.5,
                ).move_to(
                    brain.get_center() + np.array([(i - 1.5) * 0.3, (j - 1) * 0.3 + 0.2, 0])
                )
                grid_dots.add(dot)

        cutaway = Arc(
            radius=1.3,
            start_angle=PI,
            angle=1.2,
            color=GREY,
            stroke_width=2,
        ).move_to(brain.get_center() + RIGHT * 0.2 + UP * 0.2)

        equipment = self.make_equipment_box_with_plug().move_to(RIGHT * 4.5)
        cable = Line(
            grid_dots[0].get_center(),
            equipment.get_left() + LEFT * 0.2,
            color=GREY,
            stroke_width=4,
        )
        label = Text("ECoG", font_size=36, color=YELLOW)
        label.next_to(brain, UP, buff=0.4)
        return VGroup(brain, grid_dots, cutaway, cable, equipment, label)

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------------- Base full frame (continuity from previous scene) ----------------
        # Human figure left
        head = Circle(
            radius=0.35,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=3,
        ).move_to(np.array([-5.2, 1.45, 0]))
        torso = Line(np.array([-5.2, 1.05, 0]), np.array([-5.2, -1.0, 0]), color=WHITE, stroke_width=6)
        left_arm = Line(np.array([-5.2, 0.70, 0]), np.array([-6.0, 0.0, 0]), color=WHITE, stroke_width=5)
        right_arm = Line(np.array([-5.2, 0.70, 0]), np.array([-4.4, -0.1, 0]), color=WHITE, stroke_width=5)
        left_leg = Line(np.array([-5.2, -1.0, 0]), np.array([-5.7, -2.2, 0]), color=WHITE, stroke_width=6)
        right_leg = Line(np.array([-5.2, -1.0, 0]), np.array([-4.7, -2.2, 0]), color=WHITE, stroke_width=6)
        human = VGroup(head, torso, left_arm, right_arm, left_leg, right_leg)

        head_conn = head.get_right() + np.array([0.05, 0, 0])
        arm_point = right_arm.get_center() + np.array([0.2, -0.15, 0])

        # Equipment right (amp + computer)
        amp_box = Rectangle(
            width=1.4,
            height=0.9,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(np.array([-0.6, 1.5, 0]))
        amp_text = Text("amp", font_size=26, color=WHITE).move_to(amp_box.get_center())
        amp = VGroup(amp_box, amp_text)

        monitor_frame = Rectangle(
            width=1.8,
            height=1.2,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(np.array([4.0, 1.55, 0]))
        screen = Rectangle(
            width=1.5,
            height=0.85,
            fill_color=TEAL,
            fill_opacity=0.35,
            stroke_color=WHITE,
            stroke_width=1,
        ).move_to(monitor_frame.get_center())
        monitor = VGroup(monitor_frame, screen)
        tower = Rectangle(
            width=0.8,
            height=1.4,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(np.array([4.0, 0.1, 0]))
        computer = VGroup(monitor, tower)
        equipment = VGroup(amp, computer)

        amp_left = amp_box.get_left()
        amp_right = amp_box.get_right()
        comp_left = monitor_frame.get_left()

        # Isolation gap in cable
        gap_left_x = -3.55
        gap_right_x = -2.9
        gap_cable_1 = Line(head_conn, np.array([gap_left_x, 1.48, 0]), color=WHITE, stroke_width=5)
        gap_cable_2 = Line(np.array([gap_right_x, 1.50, 0]), amp_left, color=WHITE, stroke_width=5)
        barrier_line_1 = Line(
            np.array([gap_left_x, 1.20, 0]),
            np.array([gap_left_x, 1.75, 0]),
            color=YELLOW,
            stroke_width=6,
        )
        barrier_line_2 = Line(
            np.array([gap_right_x, 1.20, 0]),
            np.array([gap_right_x, 1.75, 0]),
            color=YELLOW,
            stroke_width=6,
        )
        isolation_barrier = VGroup(barrier_line_1, barrier_line_2)
        cable_right = Line(amp_right, comp_left, color=GREY, stroke_width=5)

        # Warning triangle + labels
        warning_tri = Polygon(
            np.array([-0.3, -0.25, 0]),
            np.array([0.3, -0.25, 0]),
            np.array([0, 0.35, 0]),
            stroke_width=3,
            stroke_color=WHITE,
            fill_color=YELLOW,
            fill_opacity=1,
        )
        warning_bolt = self.make_lightning(color=GREY, scale=0.5).move_to(warning_tri.get_center())
        warning_icon = VGroup(warning_tri, warning_bolt)
        warning_label = Text("Electrical Safety", font_size=24, color=GREY_B)
        warning_group = VGroup(warning_icon, warning_label).arrange(RIGHT, buff=0.25)
        warning_group.scale(0.7).move_to(np.array([-5.3, 3.1, 0]))

        iso_label = Text("Electrical Isolation", font_size=28, color=BLUE).to_edge(UP, buff=0.3)

        self.add(human, equipment, gap_cable_1, gap_cable_2, isolation_barrier, cable_right,
                 warning_group, iso_label)

        # ---------------- Beat 1: 0.00-2.64 ----------------
        self.play(
            warning_label.animate.set_color(YELLOW).set_opacity(1),
            isolation_barrier.animate.set_opacity(0.5),
            run_time=max(0.05, 0.45),
        )

        shield_human = self.make_shield(GREEN).scale(0.6).move_to(human.get_center() + UP * 0.3)
        shield_equip = self.make_shield(BLUE).scale(0.7).move_to(equipment.get_center() + UP * 0.3)

        self.play(GrowFromCenter(shield_human), run_time=max(0.05, 0.25))
        self.play(shield_human.animate.scale(1.2), rate_func=there_and_back, run_time=max(0.05, 0.35))
        self.play(FadeOut(shield_human), run_time=max(0.05, 0.2))
        self.play(GrowFromCenter(shield_equip), run_time=max(0.05, 0.25))
        self.play(shield_equip.animate.scale(1.2), rate_func=there_and_back, run_time=max(0.05, 0.35))
        self.play(FadeOut(shield_equip), run_time=max(0.05, 0.2))

        beat1_remain = 2.64 - (0.45 + 0.25 + 0.35 + 0.2 + 0.25 + 0.35 + 0.2)
        self.wait(max(0.05, beat1_remain))

        # ---------------- Gap 2.64-2.82 ----------------
        self.wait(max(0.05, 0.18))

        # ---------------- Beat 2: 2.82-6.48 ----------------
        icon_y = -2.25
        x_icons = [-4.5, 0, 4.5]

        participant_head = Circle(
            radius=0.25,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        participant_shoulder = Line(
            participant_head.get_bottom() + LEFT * 0.25,
            participant_head.get_bottom() + RIGHT * 0.25,
            color=WHITE,
            stroke_width=3,
        )
        participant_icon = VGroup(participant_head, participant_shoulder).move_to(
            np.array([x_icons[0], icon_y, 0])
        )

        operator_head = Circle(
            radius=0.2,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(np.array([x_icons[1], icon_y + 0.35, 0]))
        operator_torso = Line(
            operator_head.get_bottom(),
            operator_head.get_bottom() + DOWN * 0.45,
            color=WHITE,
            stroke_width=3,
        )
        operator_arm_l = Line(
            operator_torso.get_start() + DOWN * 0.1,
            operator_torso.get_start() + DOWN * 0.35 + LEFT * 0.3,
            color=WHITE,
            stroke_width=2,
        )
        operator_arm_r = Line(
            operator_torso.get_start() + DOWN * 0.1,
            operator_torso.get_start() + DOWN * 0.35 + RIGHT * 0.3,
            color=WHITE,
            stroke_width=2,
        )
        operator_leg_l = Line(
            operator_torso.get_end(),
            operator_torso.get_end() + DOWN * 0.4 + LEFT * 0.15,
            color=WHITE,
            stroke_width=2,
        )
        operator_leg_r = Line(
            operator_torso.get_end(),
            operator_torso.get_end() + DOWN * 0.4 + RIGHT * 0.15,
            color=WHITE,
            stroke_width=2,
        )
        operator_icon = VGroup(
            operator_head, operator_torso, operator_arm_l, operator_arm_r, operator_leg_l, operator_leg_r
        ).move_to(np.array([x_icons[1], icon_y - 0.2, 0]))

        equipment_box_icon = Rectangle(
            width=0.7,
            height=0.5,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(np.array([x_icons[2], icon_y, 0]))
        equipment_inner = Rectangle(
            width=0.4,
            height=0.25,
            fill_color=TEAL,
            fill_opacity=0.35,
            stroke_color=WHITE,
            stroke_width=1,
        ).move_to(equipment_box_icon.get_center())
        equipment_small_icon = VGroup(equipment_box_icon, equipment_inner)

        label_participant = Text("participant", font_size=20, color=WHITE).next_to(
            participant_icon, DOWN, buff=0.25
        )
        label_operator = Text("operator", font_size=20, color=WHITE).next_to(
            operator_icon, DOWN, buff=0.25
        )
        label_equipment = Text("equipment", font_size=20, color=WHITE).next_to(
            equipment_small_icon, DOWN, buff=0.25
        )

        icons_group = VGroup(
            participant_icon, operator_icon, equipment_small_icon,
            label_participant, label_operator, label_equipment,
        )
        self.play(FadeIn(icons_group), run_time=max(0.05, 0.8))  # 2.82-3.62

        ring1 = Circle(radius=0.45, stroke_color=GREEN, stroke_width=2.5).move_to(participant_icon.get_center())
        ring2 = Circle(radius=0.5, stroke_color=GREEN, stroke_width=2.5).move_to(operator_icon.get_center())
        ring3 = Circle(radius=0.55, stroke_color=GREEN, stroke_width=2.5).move_to(equipment_small_icon.get_center())
        rings = [ring1, ring2, ring3]

        ring_time = 5.68 - 3.62
        per_ring = ring_time / 3
        for ring in rings:
            self.play(Create(ring), run_time=max(0.05, per_ring * 0.8))
            self.wait(max(0.05, per_ring * 0.2))

        # Hazard 5.68-6.48
        hazard_bolt = self.make_lightning(color=YELLOW, scale=0.9).move_to(np.array([0, -1.0, 0]))
        hazard_line_1 = Line(
            hazard_bolt.get_left() + UP * 0.15,
            hazard_bolt.get_right() + DOWN * 0.15,
            color=RED,
            stroke_width=6,
        )
        hazard_line_2 = Line(
            hazard_bolt.get_left() + DOWN * 0.15,
            hazard_bolt.get_right() + UP * 0.15,
            color=RED,
            stroke_width=6,
        )
        hazard_cross = VGroup(hazard_line_1, hazard_line_2)
        hazard_group = VGroup(hazard_bolt, hazard_cross)

        self.play(FadeIn(hazard_bolt), run_time=max(0.05, 0.25))
        self.play(Create(hazard_cross), run_time=max(0.05, 0.25))
        self.play(FadeOut(hazard_group), run_time=max(0.05, 0.30))

        icons_plus_rings = VGroup(icons_group, ring1, ring2, ring3)

        # ---------------- Beat 3: 6.48-8.54 ----------------
        self.play(FadeOut(icons_plus_rings), run_time=max(0.05, 0.35))

        self.play(
            human.animate.set_opacity(0.55),
            equipment.animate.set_opacity(0.55),
            isolation_barrier.animate.set_opacity(0.45),
            cable_right.animate.set_opacity(0.4),
            run_time=max(0.05, 0.45),
        )

        recording_label = Text("biomedical signal recording", font_size=30, color=WHITE).to_edge(UP, buff=0.3)
        self.play(
            warning_label.animate.set_opacity(0.25),
            warning_icon.animate.set_opacity(0.5),
            FadeOut(iso_label),
            FadeIn(recording_label),
            run_time=max(0.05, 0.25),
        )

        wave_path = Line(head_conn, amp_left, stroke_width=0, stroke_opacity=0)
        signal_wave = self.make_wave(
            color=YELLOW, width=1.0, height=0.22, stroke_width=4, irregular=True
        ).set_opacity(0.8)
        wave_tracker = ValueTracker(0)
        signal_wave.add_updater(lambda m: m.move_to(wave_path.point_from_proportion(wave_tracker.get_value())))
        self.add(signal_wave)

        self.play(wave_tracker.animate.set_value(1), run_time=max(0.05, 0.65), rate_func=linear)

        signal_label = Text("biomedical signal", font_size=22, color=YELLOW)
        signal_label.next_to(signal_wave, DOWN, buff=0.35)
        self.play(FadeIn(signal_label), run_time=max(0.05, 0.25))

        beat3_remain = 2.06 - (0.35 + 0.45 + 0.25 + 0.65 + 0.25)
        self.wait(max(0.05, beat3_remain))

        # ---------------- Gap 8.54-9.60 ----------------
        self.wait(max(0.05, 1.06))

        # ---------------- Beat 4: 9.60-13.30 ----------------
        self.play(FadeOut(signal_wave), FadeOut(signal_label), FadeOut(recording_label), run_time=max(0.05, 0.4))
        self.play(
            equipment.animate.set_opacity(0.45).shift(RIGHT * 1.4),
            run_time=max(0.05, 0.7),
        )

        meter_box = Rectangle(
            width=1.0,
            height=0.7,
            fill_color=GREY,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(np.array([-5.4, -2.6, 0]))
        meter_dial = Circle(radius=0.25, color=WHITE, stroke_width=2, fill_opacity=0).move_to(meter_box.get_center())
        meter_needle = Line(
            meter_dial.get_center(),
            meter_dial.get_center() + np.array([0.15, 0.1, 0]),
            color=RED,
            stroke_width=3,
        )
        meter_face = VGroup(meter_box, meter_dial, meter_needle)

        probe_wire_1 = Line(
            meter_box.get_left() + DOWN * 0.1,
            meter_box.get_left() + DOWN * 0.9 + LEFT * 0.2,
            color=GREY_B,
            stroke_width=3,
        )
        probe_wire_2 = Line(
            meter_box.get_right() + DOWN * 0.1,
            meter_box.get_right() + DOWN * 0.9 + RIGHT * 0.2,
            color=GREY_B,
            stroke_width=3,
        )
        probe_tip_1 = Circle(
            radius=0.07, fill_color=GREY_B, fill_opacity=1, stroke_color=WHITE, stroke_width=1
        ).move_to(probe_wire_1.get_end())
        probe_tip_2 = Circle(
            radius=0.07, fill_color=GREY_B, fill_opacity=1, stroke_color=WHITE, stroke_width=1
        ).move_to(probe_wire_2.get_end())
        probes = VGroup(probe_wire_1, probe_wire_2, probe_tip_1, probe_tip_2)

        meter_label = Text("ordinary measurement", font_size=23, color=WHITE).next_to(
            meter_face, DOWN, buff=0.45
        )
        ordinary_group = VGroup(meter_face, probes, meter_label)

        self.play(FadeIn(meter_face), FadeIn(probes), run_time=max(0.05, 1.0))
        self.play(FadeIn(meter_label), run_time=max(0.05, 0.3))

        check_mark = SVGMobject(ASSET_PATHS["check_circle"], height=0.35).set_color(GREEN)
        check_mark.next_to(meter_face, RIGHT, buff=0.35).shift(UP * 0.2)
        self.play(FadeIn(check_mark), run_time=max(0.05, 0.5))

        self.wait(max(0.05, 0.1))
        self.play(FadeOut(ordinary_group), FadeOut(check_mark), run_time=max(0.05, 0.7))

        # ---------------- Gap 13.30-14.16 ----------------
        self.wait(max(0.05, 0.86))

        # ---------------- Beat 5: 14.16-19.58 ----------------
        contact_head = Dot(head_conn, radius=0.1, color=GOLD)
        contact_arm = Dot(arm_point, radius=0.1, color=GOLD)
        direct_cable_head = Line(head_conn, amp_left, color=GOLD, stroke_width=8)
        direct_cable_arm = Line(arm_point, amp_left, color=GOLD, stroke_width=8)
        direct_contact_label = Text("direct contact", font_size=24, color=YELLOW)
        direct_contact_label.next_to(contact_arm, DOWN, buff=0.35)

        self.play(
            human.animate.set_opacity(1.0),
            equipment.animate.set_opacity(0.75),
            run_time=max(0.05, 0.4),
        )
        self.play(
            FadeOut(gap_cable_1),
            FadeOut(gap_cable_2),
            FadeOut(isolation_barrier),
            FadeIn(contact_head),
            FadeIn(contact_arm),
            Create(direct_cable_head),
            Create(direct_cable_arm),
            run_time=max(0.05, 1.3),
        )
        self.play(FadeIn(direct_contact_label), run_time=max(0.05, 0.4))
        self.play(
            warning_icon.animate.set_color(ORANGE).set_opacity(1).scale(1.25),
            rate_func=there_and_back,
            run_time=max(0.05, 0.6),
        )

        beat5_remain = 5.42 - (0.4 + 1.3 + 0.4 + 0.6)
        self.wait(max(0.05, beat5_remain))

        # ---------------- Gap 19.58-20.32 ----------------
        self.wait(max(0.05, 0.74))

        # ---------------- Beat 6: 20.32-22.06 ----------------
        eeg_diagram = self.make_eeg_diagram()
        current_full = VGroup(
            human, equipment, direct_cable_head, direct_cable_arm,
            contact_head, contact_arm, direct_contact_label,
            warning_icon, warning_label, cable_right,
        )
        self.play(FadeOut(current_full), FadeIn(eeg_diagram), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 0.84))

        # ---------------- Gap 22.06-22.88 ----------------
        self.wait(max(0.05, 0.82))

        # ---------------- Beat 7: 22.88-26.32 ----------------
        emg_diagram = self.make_emg_diagram()
        self.play(FadeOut(eeg_diagram), FadeIn(emg_diagram), run_time=max(0.05, 0.9))

        muscle_needle = emg_diagram[3]
        muscle_tip = emg_diagram[4]
        self.play(
            muscle_needle.animate.set_color(ORANGE).scale(1.2),
            muscle_tip.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 1.74))

        # ---------------- Gap 26.32-27.20 ----------------
        self.wait(max(0.05, 0.88))

        # ---------------- Beat 8: 27.20-31.54 ----------------
        ecog_diagram = self.make_ecog_diagram()
        self.play(FadeOut(emg_diagram), FadeIn(ecog_diagram), run_time=max(0.05, 0.9))

        surgery_tag = Text("surgery", font_size=24, color=ORANGE)
        surgery_tag.next_to(ecog_diagram[0], RIGHT, buff=0.4).shift(UP * 0.2)
        self.play(FadeIn(surgery_tag), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 2.84))

        # ---------------- Gap 31.54-32.38 ----------------
        self.wait(max(0.05, 0.84))

        # ---------------- Beat 9: 32.38-35.50 ----------------
        thumb_eeg = Circle(
            radius=0.3, stroke_color=WHITE, stroke_width=2, fill_opacity=0
        ).move_to(LEFT * 4.5)
        thumb_emg = Ellipse(
            width=0.6, height=0.45,
            fill_color=MAROON, fill_opacity=0.45,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(ORIGIN)
        thumb_ecog = SVGMobject(
            ASSET_PATHS["brain"], fill_opacity=0, stroke_color=WHITE, stroke_width=1.5
        ).scale_to_fit_height(0.6).move_to(RIGHT * 4.3)
        thumbnails = VGroup(thumb_eeg, thumb_emg, thumb_ecog).arrange(RIGHT, buff=0.9)
        thumbnails.to_edge(UP, buff=1.0)

        wave_eeg = self.make_wave(color=YELLOW, width=0.6, height=0.12, stroke_width=3).next_to(
            thumb_eeg, DOWN, buff=0.2
        )
        wave_emg = self.make_wave(color=YELLOW, width=0.6, height=0.12, stroke_width=3).next_to(
            thumb_emg, DOWN, buff=0.2
        )
        wave_ecog = self.make_wave(color=YELLOW, width=0.6, height=0.12, stroke_width=3).next_to(
            thumb_ecog, DOWN, buff=0.2
        )

        small_signals_label = Text("extremely small biological signals", font_size=24, color=WHITE)
        small_signals_label.next_to(thumbnails, DOWN, buff=0.9)

        powered_box = self.make_equipment_box_with_plug().scale_to_fit_height(1.2).move_to(
            np.array([0, -2.0, 0])
        )
        powered_box_glow = SurroundingRectangle(powered_box, color=RED, buff=0.15, stroke_width=2)
        powered_devices_label = Text("powered devices", font_size=22, color=WHITE).next_to(
            powered_box, DOWN, buff=0.3
        )

        comparison_group = VGroup(
            thumbnails, wave_eeg, wave_emg, wave_ecog,
            small_signals_label, powered_box, powered_box_glow, powered_devices_label,
        )

        self.play(
            FadeOut(ecog_diagram),
            FadeOut(surgery_tag),
            FadeIn(comparison_group),
            run_time=max(0.05, 0.9),
        )
        self.play(
            powered_box_glow.animate.set_stroke(width=4).set_opacity(1),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 1.62))

        # ---------------- Gap 35.50-35.98 ----------------
        self.wait(max(0.05, 0.48))

        # ---------------- Beat 10: 35.98-38.56 ----------------
        contact_point = thumbnails.get_center() + DOWN * 0.4
        plug_icon_top = powered_box.get_top() + UP * 0.3
        trace_line = Arrow(
            plug_icon_top,
            contact_point,
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.08,
        )
        self.play(Create(trace_line), run_time=max(0.05, 1.0))
        self.play(trace_line.animate.set_color(RED), run_time=max(0.05, 0.5))

        flash_dot = Dot(contact_point, radius=0.15, color=RED, fill_opacity=0.5)
        self.play(GrowFromCenter(flash_dot), run_time=max(0.05, 0.15))
        self.play(FadeOut(flash_dot), run_time=max(0.05, 0.15))

        connected_label = Text("connected to powered electronic devices", font_size=24, color=RED)
        connected_label.next_to(trace_line, UP, buff=0.2).shift(LEFT * 0.5)
        self.play(FadeIn(connected_label), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.38))

        # ---------------- Gap 38.56-39.52 ----------------
        self.wait(max(0.05, 0.96))

        # ---------------- Beat 11: 39.52-44.20 ----------------
        full_return = VGroup(
            human, equipment, direct_cable_head, direct_cable_arm,
            contact_head, contact_arm, warning_icon, warning_label, cable_right,
        )
        full_return.set_opacity(1)

        self.play(
            FadeOut(comparison_group),
            FadeOut(trace_line),
            FadeOut(connected_label),
            FadeIn(full_return),
            run_time=max(0.05, 0.9),
        )

        current_arrow = self.make_jagged_arrow(
            start=equipment.get_left() + DOWN * 0.2,
            end=contact_head.get_center() + RIGHT * 0.1,
            color=RED,
            stroke_width=6,
        )
        self.play(Create(current_arrow), run_time=max(0.05, 1.2))

        glow_rect = Rectangle(
            width=14,
            height=8,
            fill_color=RED,
            fill_opacity=0,
            stroke_width=0,
        ).move_to(ORIGIN)
        self.add(glow_rect)
        self.bring_to_back(glow_rect)

        self.play(
            warning_icon.animate.set_color(RED).set_opacity(1).scale(1.2),
            glow_rect.animate.set_fill(opacity=0.2),
            run_time=max(0.05, 0.5),
        )
        self.play(FadeOut(current_arrow), run_time=max(0.05, 0.35))

        risk_label = Text("unintended current → serious safety risk", font_size=30, color=RED)
        risk_label.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(risk_label), run_time=max(0.05, 0.7))
        self.play(glow_rect.animate.set_fill(opacity=0), run_time=max(0.05, 0.3))

        beat11_remain = 4.68 - (0.9 + 1.2 + 0.5 + 0.35 + 0.7 + 0.3)
        self.wait(max(0.05, beat11_remain))

        # ---------------- Gap 44.20-44.74 ----------------
        self.wait(max(0.05, 0.54))

        # ---------------- Beat 12: 44.74-48.50 ----------------
        self.play(
            FadeOut(risk_label),
            FadeOut(glow_rect),
            warning_icon.animate.set_color(YELLOW).set_opacity(1),
            run_time=max(0.05, 0.5),
        )

        clipboard_rect = Rectangle(
            width=1.4,
            height=1.8,
            fill_color=GREY,
            fill_opacity=0.15,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(ORIGIN)
        clip_band = Rectangle(
            width=0.8,
            height=0.2,
            fill_color=GREY,
            fill_opacity=0.5,
            stroke_color=WHITE,
            stroke_width=1,
        ).move_to(clipboard_rect.get_top() + DOWN * 0.35)
        blank_lines = VGroup()
        for i in range(3):
            line = Line(
                clipboard_rect.get_left() + RIGHT * 0.2 + DOWN * (0.8 + i * 0.3),
                clipboard_rect.get_right() + LEFT * 0.2 + DOWN * (0.8 + i * 0.3),
                color=GREY,
                stroke_width=2,
            )
            blank_lines.add(line)
        clipboard = VGroup(clipboard_rect, clip_band, blank_lines)

        glp_label = Text("good laboratory practice", font_size=26, color=WHITE)
        glp_label.next_to(clipboard_rect, DOWN, buff=0.4)
        clipboard_check = SVGMobject(ASSET_PATHS["check_circle"], height=0.4).set_color(GREEN)
        clipboard_check.next_to(clipboard_rect, RIGHT, buff=0.35).shift(UP * 0.3)

        self.play(FadeIn(clipboard), FadeIn(glp_label), run_time=max(0.05, 0.7))
        self.play(FadeIn(clipboard_check), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.5))
        self.play(FadeOut(clipboard), FadeOut(clipboard_check), FadeOut(glp_label), run_time=max(0.05, 0.7))

        beat12_remain = 3.76 - (0.5 + 0.7 + 0.5 + 0.5 + 0.7)
        self.wait(max(0.05, beat12_remain))

        # ---------------- Gap 48.50-49.32 ----------------
        self.wait(max(0.05, 0.82))

        # ---------------- Beat 13: 49.32-53.04 ----------------
        self.play(FadeIn(warning_label), FadeIn(iso_label), run_time=max(0.05, 0.4))
        self.play(
            warning_icon.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=max(0.05, 0.4),
        )

        gap_cable_1_new = Line(head_conn, np.array([gap_left_x, 1.48, 0]), color=WHITE, stroke_width=5)
        gap_cable_2_new = Line(np.array([gap_right_x, 1.50, 0]), amp_left, color=WHITE, stroke_width=5)
        barrier_line_1_new = Line(
            np.array([gap_left_x, 1.20, 0]),
            np.array([gap_left_x, 1.75, 0]),
            color=YELLOW,
            stroke_width=6,
        )
        barrier_line_2_new = Line(
            np.array([gap_right_x, 1.20, 0]),
            np.array([gap_right_x, 1.75, 0]),
            color=YELLOW,
            stroke_width=6,
        )
        isolation_barrier_new = VGroup(barrier_line_1_new, barrier_line_2_new)

        self.play(
            FadeOut(direct_cable_head),
            FadeOut(direct_cable_arm),
            FadeOut(contact_head),
            FadeOut(contact_arm),
            FadeIn(gap_cable_1_new),
            FadeIn(gap_cable_2_new),
            FadeIn(isolation_barrier_new),
            run_time=max(0.05, 0.6),
        )

        top_icon_eeg = Circle(radius=0.22, stroke_color=WHITE, stroke_width=2, fill_opacity=0)
        top_icon_emg = Ellipse(
            width=0.45,
            height=0.35,
            fill_color=MAROON,
            fill_opacity=0.45,
            stroke_color=WHITE,
            stroke_width=2,
        )
        top_icon_ecog = SVGMobject(
            ASSET_PATHS["brain"], fill_opacity=0, stroke_color=WHITE, stroke_width=1.5
        ).scale_to_fit_height(0.45)
        top_icons = VGroup(top_icon_eeg, top_icon_emg, top_icon_ecog).arrange(RIGHT, buff=0.7)
        top_icons.to_edge(UP, buff=1.4)

        shields = VGroup(
            self.make_shield(GREEN).scale(0.4).move_to(top_icon_eeg.get_center() + DOWN * 0.1),
            self.make_shield(BLUE).scale(0.4).move_to(top_icon_emg.get_center() + DOWN * 0.1),
            self.make_shield(GREEN).scale(0.4).move_to(top_icon_ecog.get_center() + DOWN * 0.1),
        )

        key_requirement = Text(
            "fundamental requirement of every biomedical recording system",
            font_size=24,
            color=WHITE,
        )
        key_requirement.next_to(top_icons, DOWN, buff=0.6)

        self.play(FadeIn(top_icons), FadeIn(shields), run_time=max(0.05, 0.5))
        self.play(FadeIn(key_requirement), run_time=max(0.05, 0.6))
        self.play(
            isolation_barrier_new.animate.set_opacity(0.5),
            rate_func=there_and_back,
            run_time=max(0.05, 0.5),
        )

        beat13_remain = 3.72 - (0.4 + 0.4 + 0.6 + 0.5 + 0.6 + 0.5)
        self.wait(max(0.05, beat13_remain))

        # ---------------- Beat 14: 53.04-53.77 ----------------
        self.play(
            isolation_barrier_new.animate.set_opacity(0.7),
            rate_func=there_and_back,
            run_time=max(0.05, 0.73),
        )