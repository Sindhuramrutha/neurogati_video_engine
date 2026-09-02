ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(Scene):
    def make_electrode(self, color=GREY_B):
        electrode = Circle(
            radius=0.13,
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        return electrode

    def make_equipment_box(self):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=0.55,
            height=0.45,
            fill_color=BLUE,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=2,
        )
        return box

    def make_frayed_segment(self, x_start, y, x_end):
        main = Line(
            np.array([x_start, y, 0]),
            np.array([x_end, y, 0]),
            color=RED,
            stroke_width=3,
        )
        stubs = VGroup()
        stub_offsets = [
            (x_start + 0.18, -0.10, 0.05),
            (x_start + 0.48, -0.13, 0.02),
            (x_start + 0.78, -0.12, -0.06),
            (x_end - 0.18, -0.08, -0.10),
        ]
        for sx, dx, dy in stub_offsets:
            stub = Line(
                np.array([sx, y, 0]),
                np.array([sx + dx, y + dy, 0]),
                color=RED,
                stroke_width=2,
            )
            stubs.add(stub)
        return VGroup(main, stubs)

    def make_hazard_icon(self, height=0.45):
        triangle = Polygon(
            UP * 0.24,
            DOWN * 0.22 + LEFT * 0.30,
            DOWN * 0.22 + RIGHT * 0.30,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        ex_line = Line(UP * 0.10, DOWN * 0.03, color=BLACK, stroke_width=4)
        ex_dot = Dot(DOWN * 0.14, radius=0.045, color=BLACK)
        icon = VGroup(triangle, ex_line, ex_dot)
        icon.scale_to_fit_height(height)
        return icon

    def make_wrench_icon(self, height=0.45):
        head = Circle(
            radius=0.15,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        head.move_to(LEFT * 0.25)
        handle = Rectangle(
            width=0.55,
            height=0.12,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        handle.move_to(head.get_right() + RIGHT * 0.27)
        cut = Rectangle(
            width=0.08,
            height=0.18,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
        )
        cut.move_to(head.get_center())
        icon = VGroup(handle, head, cut)
        icon.scale_to_fit_height(height)
        return icon

    def make_calendar_check(self, height=0.8):
        body = RoundedRectangle(
            corner_radius=0.10,
            width=0.85,
            height=0.75,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=0,
        )
        header = Rectangle(
            width=0.85,
            height=0.20,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_width=0,
        )
        header.move_to(body.get_top() + DOWN * 0.10)

        ring_left = Circle(
            radius=0.045,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(body.get_top() + UP * 0.08 + LEFT * 0.22)
        ring_right = Circle(
            radius=0.045,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(body.get_top() + UP * 0.08 + RIGHT * 0.22)

        check1 = Line(
            np.array([-0.14, -0.04, 0]),
            np.array([0.00, 0.08, 0]),
            color=GREEN,
            stroke_width=7,
        )
        check2 = Line(
            np.array([0.00, 0.08, 0]),
            np.array([0.20, -0.12, 0]),
            color=GREEN,
            stroke_width=7,
        )

        icon = VGroup(body, header, ring_left, ring_right, check1, check2)
        icon.scale_to_fit_height(height)
        icon.move_to(ORIGIN)
        return icon

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Beat 1: 0.00-3.90 ----
        left_panel = Rectangle(
            width=6.7,
            height=7.0,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_color=GREY_B,
            stroke_width=1,
        ).move_to(np.array([-3.35, -0.1, 0]))
        right_panel = Rectangle(
            width=6.7,
            height=7.0,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_color=GREY_B,
            stroke_width=1,
        ).move_to(np.array([3.35, -0.1, 0]))
        divider = Line(UP * 3.4, DOWN * 3.4, color=GREY_B, stroke_width=2)

        left_elec = self.make_electrode().move_to(np.array([-5.9, 2.0, 0]))
        right_elec = self.make_electrode().move_to(np.array([0.9, 2.0, 0]))
        left_equip = self.make_equipment_box().move_to(np.array([-1.2, 2.0, 0]))
        right_equip = self.make_equipment_box().move_to(np.array([6.0, 2.0, 0]))

        left_cable = Line(
            left_elec.get_right(),
            left_equip.get_left(),
            color=GREY_B,
            stroke_width=5,
        )

        fray_start = np.array([2.6, 2.0, 0])
        fray_end = np.array([3.6, 2.0, 0])
        right_cable_left = Line(
            right_elec.get_right(),
            fray_start,
            color=GREY_B,
            stroke_width=5,
        )
        frayed_segment = self.make_frayed_segment(
            fray_start[0], fray_start[1], fray_end[0]
        )
        connector = Rectangle(
            width=0.28,
            height=0.20,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
        ).move_to(np.array([5.15, 2.0, 0]))
        right_cable_right = Line(
            fray_end,
            np.array([5.01, 2.0, 0]),
            color=GREY_B,
            stroke_width=5,
        )

        baseline_y = -1.8
        left_xs = np.linspace(-6.1, -0.6, 90)
        right_xs = np.linspace(0.6, 6.1, 90)

        left_wave = VMobject().set_stroke(GREEN, width=4)
        left_wave.set_points_as_corners(
            [np.array([x, baseline_y, 0]) for x in left_xs]
        )
        right_wave = VMobject().set_stroke(RED, width=4)
        right_wave.set_points_as_corners(
            [np.array([x, baseline_y, 0]) for x in right_xs]
        )

        left_phase = 0.0
        right_phase = 0.0

        def update_left(m, dt):
            nonlocal left_phase
            left_phase += dt
            pts = []
            for i, x in enumerate(left_xs):
                xr = (x - left_xs[0]) / (left_xs[-1] - left_xs[0])
                y = baseline_y + 0.18 * np.sin(2 * PI * 1.8 * xr - 2 * PI * 0.25 * left_phase)
                pts.append(np.array([x, y, 0]))
            m.set_points_as_corners(pts)

        noise_state = {"noise_amp": 0.20, "spike_prob": 0.06, "spike_amp": 0.30}

        def update_right(m, dt):
            nonlocal right_phase
            right_phase += dt
            pts = []
            for i, x in enumerate(right_xs):
                if i == 0 or i == len(right_xs) - 1:
                    y = baseline_y
                else:
                    y = baseline_y + np.random.uniform(-noise_state["noise_amp"], noise_state["noise_amp"])
                    if np.random.random() < noise_state["spike_prob"]:
                        y += np.random.choice([-1, 1]) * noise_state["spike_amp"] * np.random.uniform(0.5, 1.0)
                pts.append(np.array([x, y, 0]))
            m.set_points_as_corners(pts)

        left_wave.add_updater(update_left)
        right_wave.add_updater(update_right)

        split_screen = VGroup(
            left_panel,
            right_panel,
            divider,
            left_elec,
            left_equip,
            left_cable,
            left_wave,
            right_elec,
            right_equip,
            right_cable_left,
            frayed_segment,
            right_cable_right,
            connector,
            right_wave,
        )

        self.play(FadeIn(split_screen), run_time=max(0.05, 3.6))
        self.wait(max(0.05, 0.30))  # Beat 1 total 3.90

        # ---- Gap before Beat 2 ----
        self.wait(max(0.05, 0.62))

        # ---- Beat 2: 4.52-9.10 ----
        noise_state["noise_amp"] = 0.40
        noise_state["spike_prob"] = 0.28
        noise_state["spike_amp"] = 0.38

        self.play(frayed_segment.animate.set_stroke(RED, width=6), run_time=max(0.05, 0.35))
        self.play(frayed_segment.animate.set_stroke(RED, width=3), run_time=max(0.05, 0.35))
        self.play(connector.animate.shift(UP * 0.06), run_time=max(0.05, 0.30))
        self.play(connector.animate.shift(DOWN * 0.12), run_time=max(0.05, 0.40))
        self.play(connector.animate.shift(UP * 0.06), run_time=max(0.05, 0.30))
        self.play(frayed_segment.animate.set_stroke(RED, width=6), run_time=max(0.05, 0.35))
        self.play(frayed_segment.animate.set_stroke(RED, width=3), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 2.18))  # Beat 2 total 4.58

        # ---- Beat 3: 9.10-14.20 ----
        noise_state["noise_amp"] = 0.55
        noise_state["spike_prob"] = 0.45
        noise_state["spike_amp"] = 0.55

        hazard_icon = self.make_hazard_icon(height=0.45)
        hazard_icon.move_to(right_equip.get_top() + UP * 0.50)

        self.play(right_wave.animate.set_opacity(0.40), run_time=max(0.05, 0.40))
        self.play(right_wave.animate.set_opacity(0.15), run_time=max(0.05, 0.20))
        self.play(right_wave.animate.set_opacity(0.40), run_time=max(0.05, 0.20))
        self.play(right_wave.animate.set_opacity(0.80), run_time=max(0.05, 0.20))
        self.play(right_wave.animate.set_opacity(0.35), run_time=max(0.05, 0.20))

        self.play(
            frayed_segment.animate.set_stroke(RED, width=8).set_color(RED),
            connector.animate.set_fill(RED, opacity=1).set_stroke(YELLOW, width=3),
            run_time=max(0.05, 0.60),
        )
        self.play(GrowFromCenter(hazard_icon), run_time=max(0.05, 0.40))
        self.play(FadeOut(hazard_icon), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 2.50))  # Beat 3 total 5.10

        # ---- Gap before Beat 4 ----
        self.wait(max(0.05, 0.86))

        # ---- Beat 4: 15.06-19.66 ----
        calendar_icon = self.make_calendar_check(height=0.8)
        calendar_ring = DashedVMobject(
            Circle(radius=0.70, stroke_color=GREEN, stroke_width=3),
            num_dashes=24,
        ).move_to(ORIGIN)
        inspection_circle = DashedVMobject(
            Circle(radius=0.40, stroke_color=YELLOW, stroke_width=3),
            num_dashes=24,
        ).move_to(ORIGIN)

        self.play(
            GrowFromCenter(calendar_icon),
            GrowFromCenter(calendar_ring),
            run_time=max(0.05, 1.00),
        )
        self.play(
            Rotate(calendar_ring, angle=2 * PI, about_point=ORIGIN),
            run_time=max(0.05, 1.20),
            rate_func=linear,
        )
        self.play(GrowFromCenter(inspection_circle), run_time=max(0.05, 0.40))
        self.play(inspection_circle.animate.scale(6), run_time=max(0.05, 1.80), rate_func=smooth)
        self.wait(max(0.05, 0.20))  # Beat 4 total 4.60

        # ---- Gap before Beat 5 ----
        self.wait(max(0.05, 1.20))

        # ---- Beat 5: 20.86-24.08 ----
        self.play(
            inspection_circle.animate.move_to(frayed_segment.get_center()).scale(0.27),
            run_time=max(0.05, 0.60),
        )

        wrench_icon = self.make_wrench_icon(height=0.45)
        wrench_icon.next_to(right_equip, UP, buff=0.45)
        self.play(GrowFromCenter(wrench_icon), run_time=max(0.05, 0.35))

        clean_replacement = Line(
            fray_start,
            fray_end,
            color=GREY_B,
            stroke_width=5,
        )
        clean_replacement.set_opacity(0)
        self.play(
            FadeOut(frayed_segment),
            FadeIn(clean_replacement),
            run_time=max(0.05, 0.60),
        )

        seat_pos = np.array([right_equip.get_left()[0] - 0.18, 2.0, 0])
        self.play(connector.animate.move_to(seat_pos), run_time=max(0.05, 0.45))
        self.play(
            clean_replacement.animate.set_stroke(WHITE, width=8),
            run_time=max(0.05, 0.35),
        )
        self.play(
            FadeOut(wrench_icon),
            FadeOut(inspection_circle),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.47))  # Beat 5 total 3.22

        # ---- Gap before Beat 6 ----
        self.wait(max(0.05, 0.78))

        # ---- Beat 6: 24.86-27.98 ----
        right_wave.clear_updaters()

        right_clean_wave = VMobject().set_stroke(GREEN, width=4)
        clean_pts = []
        for i, x in enumerate(right_xs):
            xr = (x - right_xs[0]) / (right_xs[-1] - right_xs[0])
            y = baseline_y + 0.18 * np.sin(2 * PI * 1.8 * xr)
            clean_pts.append(np.array([x, y, 0]))
        right_clean_wave.set_points_as_corners(clean_pts)

        self.play(
            Transform(right_wave, right_clean_wave),
            run_time=max(0.05, 1.80),
            rate_func=smooth,
        )

        right_smooth_phase = 0.0

        def update_right_smooth(m, dt):
            nonlocal right_smooth_phase
            right_smooth_phase += dt
            pts = []
            for i, x in enumerate(right_xs):
                xr = (x - right_xs[0]) / (right_xs[-1] - right_xs[0])
                y = baseline_y + 0.18 * np.sin(2 * PI * 1.8 * xr - 2 * PI * 0.25 * right_smooth_phase)
                pts.append(np.array([x, y, 0]))
            m.set_points_as_corners(pts)

        right_wave.add_updater(update_right_smooth)

        self.play(calendar_icon.animate.scale(1.2), run_time=max(0.05, 0.30))
        self.play(calendar_icon.animate.scale(1 / 1.2), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.72))  # Beat 6 total 3.12