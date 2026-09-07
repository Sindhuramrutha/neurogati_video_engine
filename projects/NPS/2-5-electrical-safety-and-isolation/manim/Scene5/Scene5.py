ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def make_human(self, height=0.7, color=TEAL):
        head = Circle(
            radius=0.14,
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).shift(UP * 0.32)
        body = Ellipse(
            width=0.70,
            height=0.48,
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).shift(DOWN * 0.10)
        human = VGroup(head, body)
        human.scale_to_fit_height(height)
        return human

    def make_equipment(self, height=0.5, color=BLUE):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=0.70,
            height=0.55,
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        screen = Rectangle(
            width=0.34,
            height=0.22,
            fill_color=WHITE,
            fill_opacity=0.85,
            stroke_width=0,
        ).move_to(box.get_center() + UP * 0.08)
        knob = Dot(
            box.get_center() + DOWN * 0.14,
            radius=0.045,
            color=YELLOW,
            stroke_width=0,
        )
        equip = VGroup(box, screen, knob)
        equip.scale_to_fit_height(height)
        return equip

    def make_cable_icon(self, height=0.8):
        human = self.make_human(height=0.62, color=TEAL).move_to(LEFT * 0.72)
        equip = self.make_equipment(height=0.50, color=BLUE).move_to(RIGHT * 0.72)
        cable = Line(
            human.get_right(),
            equip.get_left(),
            color=GREY_B,
            stroke_width=3,
        )
        conn_left = Dot(
            human.get_right(),
            radius=0.05,
            color=GREY_B,
            fill_opacity=0.7,
        )
        conn_right = Dot(
            equip.get_left(),
            radius=0.05,
            color=GREY_B,
            fill_opacity=0.7,
        )
        icon = VGroup(human, equip, cable, conn_left, conn_right)
        icon.scale_to_fit_height(height)
        return icon, cable, conn_left, conn_right

    def make_shield_icon(self, height=0.8):
        body = Polygon(
            UP * 0.42,
            RIGHT * 0.38 + UP * 0.22,
            RIGHT * 0.28 + DOWN * 0.05,
            DOWN * 0.45,
            LEFT * 0.28 + DOWN * 0.05,
            LEFT * 0.38 + UP * 0.22,
        )
        body.set_fill(GREEN, opacity=1)
        body.set_stroke(WHITE, width=2.5)

        bolt = Polygon(
            np.array([0.06, 0.18, 0]),
            np.array([-0.12, 0.02, 0]),
            np.array([-0.02, 0.02, 0]),
            np.array([-0.08, -0.18, 0]),
            np.array([0.12, -0.02, 0]),
            np.array([0.02, -0.02, 0]),
        )
        bolt.set_fill(YELLOW, opacity=1)
        bolt.set_stroke(WHITE, width=1.2)

        icon = VGroup(body, bolt)
        icon.scale_to_fit_height(height)
        return icon, body

    def make_checkmark(self):
        check = VGroup(
            Line(LEFT * 0.10, RIGHT * 0.02, color=GREEN, stroke_width=5),
            Line(RIGHT * 0.02, RIGHT * 0.14 + UP * 0.10, color=GREEN, stroke_width=5),
        )
        return check

    def make_checklist_icon(self, height=0.85):
        body = RoundedRectangle(
            corner_radius=0.10,
            width=0.95,
            height=1.05,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=0,
        )
        lines = VGroup(
            *[
                Line(LEFT * 0.30, RIGHT * 0.30, color=GREY_B, stroke_width=3)
                for _ in range(3)
            ]
        ).arrange(DOWN, buff=0.17).move_to(body.get_center())

        checks = []
        for line in lines:
            check = self.make_checkmark()
            check.move_to(line.get_center() + LEFT * 0.02)
            checks.append(check)

        icon = VGroup(body, lines, *checks)
        icon.scale_to_fit_height(height)
        return icon, checks

    def construct(self):
        self.camera.background_color = "#0F1116"

        icon_x = -4.8
        y_positions = [2.8, 1.35, -0.2, -1.8]

        # ---- Beat 1: 0.00-1.48 ----
        title = Text("Section Summary", font_size=82, color=WHITE, weight=BOLD)
        divider = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_B, stroke_width=3)
        divider.next_to(title, DOWN, buff=0.35)
        title_group = VGroup(title, divider).move_to(ORIGIN)

        self.play(FadeIn(title_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.48))

        # ---- Gap, title moves toward bottom: 1.48-2.46 ----
        self.play(
            title_group.animate.shift(DOWN * 4.8).set_opacity(0),
            run_time=max(0.05, 0.98),
        )

        # ---- Beat 2: 2.46-5.98 ----
        icon1, cable1, conn_left1, conn_right1 = self.make_cable_icon(height=0.85)
        icon1.move_to(np.array([icon_x, y_positions[0], 0]))
        text1 = Text(
            "Neural recording systems connect electronic equipment to the human body",
            font_size=22,
            color=WHITE,
        )
        if text1.width > 7.0:
            text1.scale_to_fit_width(7.0)
        text1.next_to(icon1, RIGHT, buff=0.5)
        bullet1_group = VGroup(icon1, text1)

        self.play(FadeIn(bullet1_group), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.5))

        # Cable pulse and connection points brighten in sequence.
        self.play(cable1.animate.set_stroke(YELLOW, width=6), run_time=max(0.05, 0.4))
        self.play(cable1.animate.set_stroke(GREY_B, width=3), run_time=max(0.05, 0.4))
        self.play(
            conn_left1.animate.scale(1.6).set_color(YELLOW).set_opacity(1),
            run_time=max(0.05, 0.25),
        )
        self.play(
            conn_right1.animate.scale(1.6).set_color(YELLOW).set_opacity(1),
            run_time=max(0.05, 0.25),
        )
        self.wait(max(0.05, 0.52))

        # ---- Gap before Beat 3: 5.98-6.58 ----
        self.wait(max(0.05, 0.6))

        # ---- Beat 3: 6.58-10.96 ----
        icon2, shield_body = self.make_shield_icon(height=0.85)
        icon2.move_to(np.array([icon_x, y_positions[1], 0]))
        text2 = Text(
            "Electrical safety is essential for protecting both participants and equipment",
            font_size=22,
            color=WHITE,
        )
        if text2.width > 7.0:
            text2.scale_to_fit_width(7.0)
        text2.next_to(icon2, RIGHT, buff=0.5)
        bullet2_group = VGroup(icon2, text2)

        human_inside = self.make_human(height=0.32, color=WHITE).move_to(icon2.get_center())
        equip_inside = self.make_equipment(height=0.28, color=WHITE).move_to(icon2.get_center())

        self.play(FadeIn(bullet2_group), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.5))

        # Participants -> small human inside shield.
        self.play(GrowFromCenter(human_inside), run_time=max(0.05, 0.45))
        self.play(FadeOut(human_inside), run_time=max(0.05, 0.35))

        # Equipment -> small equipment box inside shield.
        self.play(GrowFromCenter(equip_inside), run_time=max(0.05, 0.45))
        self.play(FadeOut(equip_inside), run_time=max(0.05, 0.35))

        # Shield pulses gently once in green.
        self.play(icon2.animate.scale(1.12), run_time=max(0.05, 0.3))
        self.play(icon2.animate.scale(1 / 1.12), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.48))

        # ---- Gap before Beat 4: 10.96-12.24 ----
        self.wait(max(0.05, 1.28))

        # ---- Beat 4: 12.24-20.12 ----
        y3 = y_positions[2]
        left_block = Rectangle(
            width=0.55,
            height=0.65,
            fill_color=TEAL,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).move_to(np.array([icon_x - 0.72, y3, 0]))
        right_block = Rectangle(
            width=0.55,
            height=0.65,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).move_to(np.array([icon_x + 0.72, y3, 0]))

        barrier_line = DashedVMobject(
            Line(UP * 0.5, DOWN * 0.5, color=GREY_B, stroke_width=2.5),
            num_dashes=8,
        ).move_to(np.array([icon_x, y3, 0]))

        green_xs = np.linspace(icon_x - 0.42, icon_x + 0.42, 50)
        green_wave = VMobject().set_stroke(GREEN, width=3)
        green_phase = 0.0

        def update_green(m, dt):
            nonlocal green_phase
            green_phase += dt * 3.0
            pts = []
            for x in green_xs:
                rel_x = x - icon_x
                yy = y3 + 0.14 * np.sin(6.0 * rel_x - green_phase)
                pts.append(np.array([x, yy, 0]))
            m.set_points_as_corners(pts)

        update_green(green_wave, 0)
        green_wave.add_updater(update_green)

        red_base_pts = []
        red_xs = np.linspace(icon_x - 1.05, icon_x - 0.50, 12)
        for i, rx in enumerate(red_xs):
            ry = y3 + (0.08 if i % 2 == 0 else -0.08)
            red_base_pts.append(np.array([rx, ry, 0]))

        red_zig = VMobject().set_stroke(RED, width=3)
        red_progress = 0.0

        def update_red(m, dt):
            nonlocal red_progress
            red_progress += dt * 0.45
            cycle = red_progress % 1.0
            if cycle < 0.55:
                shift_x = 0.45 * (cycle / 0.55)
            else:
                shift_x = 0.45
            pts = [np.array([p[0] + shift_x, p[1], p[2]]) for p in red_base_pts]
            m.set_points_as_corners(pts)

        update_red(red_zig, 0)
        red_zig.add_updater(update_red)

        barrier_icon_group = VGroup(left_block, right_block, barrier_line, green_wave, red_zig)

        text3 = Text(
            "Electrical isolation separates the participant from hazardous circuits\n"
            "while still allowing physiological signals to be recorded",
            font_size=19,
            color=WHITE,
            line_spacing=0.7,
        )
        if text3.width > 7.0:
            text3.scale_to_fit_width(7.0)
        text3.next_to(right_block, RIGHT, buff=0.5)

        bullet3_group = VGroup(barrier_icon_group, text3)

        self.play(FadeIn(bullet3_group), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 6.38))

        # ---- Gap before Beat 5: 20.12-21.06 ----
        self.wait(max(0.05, 0.94))

        # ---- Beat 5: 21.06-29.40 ----
        icon4, checks4 = self.make_checklist_icon(height=0.85)
        icon4.move_to(np.array([icon_x, y_positions[3], 0]))
        text4 = Text(
            "Safe recording practices and properly designed biomedical equipment\n"
            "are fundamental to every neural signal acquisition system",
            font_size=19,
            color=WHITE,
            line_spacing=0.7,
        )
        if text4.width > 7.0:
            text4.scale_to_fit_width(7.0)
        text4.next_to(icon4, RIGHT, buff=0.5)
        bullet4_group = VGroup(icon4, text4)

        for check in checks4:
            check.set_opacity(0)
            check.shift(UP * 0.30)

        self.play(FadeIn(bullet4_group), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.2))

        # Check 1: safe recording practices.
        self.play(
            checks4[0].animate.shift(DOWN * 0.50).set_opacity(1),
            run_time=max(0.05, 0.25),
            rate_func=smooth,
        )
        self.play(checks4[0].animate.shift(UP * 0.20), run_time=max(0.05, 0.20), rate_func=smooth)
        self.wait(max(0.05, 1.6))

        # Check 2: properly designed biomedical equipment.
        self.play(
            checks4[1].animate.shift(DOWN * 0.50).set_opacity(1),
            run_time=max(0.05, 0.25),
            rate_func=smooth,
        )
        self.play(checks4[1].animate.shift(UP * 0.20), run_time=max(0.05, 0.20), rate_func=smooth)
        self.wait(max(0.05, 1.8))

        # Check 3: every neural signal acquisition system.
        self.play(
            checks4[2].animate.shift(DOWN * 0.50).set_opacity(1),
            run_time=max(0.05, 0.25),
            rate_func=smooth,
        )
        self.play(checks4[2].animate.shift(UP * 0.20), run_time=max(0.05, 0.20), rate_func=smooth)
        self.wait(max(0.05, 1.19))

        # ---- Beat 6: 29.40-30.07 ----
        icon_groups = [icon1, icon2, barrier_icon_group, icon4]
        pulse_rings = VGroup(
            *[
                SurroundingRectangle(
                    icon,
                    color=GREEN,
                    buff=0.12,
                    corner_radius=0.10,
                    stroke_width=5,
                ).set_fill(GREEN, opacity=0)
                for icon in icon_groups
            ]
        )

        self.play(
            pulse_rings.animate.scale(1.18).set_opacity(0),
            run_time=max(0.05, 0.6),
            rate_func=linear,
        )
        self.wait(max(0.05, 0.07))