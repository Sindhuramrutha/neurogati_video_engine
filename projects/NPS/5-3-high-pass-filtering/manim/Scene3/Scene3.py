ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Beat 1: empty side-by-side panels with a thin divider
        # ------------------------------------------------------------
        panel_w = 6.0
        panel_h = 5.8
        left_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            stroke_color=GREY_B,
            stroke_width=2.0,
            stroke_opacity=0.55,
        ).move_to(LEFT * 3.45)

        right_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            stroke_color=GREY_B,
            stroke_width=2.0,
            stroke_opacity=0.55,
        ).move_to(RIGHT * 3.45)

        divider = Line(
            start=np.array([0, -panel_h / 2, 0]),
            end=np.array([0, panel_h / 2, 0]),
            color=GREY_B,
            stroke_width=3,
            stroke_opacity=0.55,
        )

        self.play(FadeIn(left_panel), FadeIn(right_panel), Create(divider), run_time=max(0.05, 1.06))
        self.wait(max(0.05, 0.64))

        # ------------------------------------------------------------
        # Beat 2: left panel gets road, tollbooth gate with raised arm,
        # and HP sign; right panel remains empty.
        # ------------------------------------------------------------
        road_center_y = -1.1
        road_top_y = -0.98

        road_base = Rectangle(
            width=5.6,
            height=0.24,
            fill_color=GREY_B,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to(np.array([-3.45, road_center_y, 0]))

        road_line = DashedLine(
            start=np.array([-6.1, road_center_y, 0]),
            end=np.array([-0.8, road_center_y, 0]),
            dash_length=0.16,
            dashed_ratio=0.5,
            color=WHITE,
            stroke_width=2,
        )

        # Gate pivot: the point around which the barrier arm rotates
        pivot = np.array([-4.8, -0.68, 0])

        gate_arm = Line(
            start=pivot,
            end=pivot + RIGHT * 3.3,
            color=YELLOW,
            stroke_width=9,
        )
        gate_arm.rotate(PI / 3, about_point=pivot)  # raised position

        booth_pole = Line(
            start=pivot,
            end=pivot + UP * 1.9,
            color=GREY,
            stroke_width=5,
        )

        booth = Rectangle(
            width=0.85,
            height=0.8,
            fill_color=BLUE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).move_to(np.array([-4.8, 0.85, 0]))

        hp_sign = Text("HP", font_size=24, weight=BOLD, color=YELLOW).move_to(booth.get_center())

        left_scene = VGroup(road_base, road_line, booth_pole, booth, hp_sign, gate_arm)
        self.play(FadeIn(left_scene), run_time=max(0.05, 2.52))
        self.wait(max(0.05, 0.72))

        # ------------------------------------------------------------
        # Beat 3: right panel gets noisy signal trace (red slow baseline
        # plus bright green rapid oscillations).
        # ------------------------------------------------------------
        x_min = 0.7
        x_max = 6.15
        x_step = 0.025
        x_vals = np.arange(x_min, x_max + x_step, x_step)

        def red_baseline_points():
            return [
                np.array([x, 0.45 * np.sin(2 * np.pi * 0.25 * (x - x_min)), 0])
                for x in x_vals
            ]

        red_baseline = VMobject(color=RED, stroke_width=4)
        red_baseline.set_points_as_corners(red_baseline_points())

        green_amp = 0.22
        green_freq = 4.0
        self.green_phase = 0.0

        def green_wave_points(phase):
            return [
                np.array([x, green_amp * np.sin(2 * np.pi * green_freq * (x - phase)), 0])
                for x in x_vals
            ]

        green_wave = VMobject(color=GREEN, stroke_width=3)
        green_wave.set_points_as_corners(green_wave_points(0.0))

        def update_green_wave(mob, dt):
            self.green_phase += dt * 0.55
            mob.set_points_as_corners(green_wave_points(self.green_phase))

        green_wave.add_updater(update_green_wave)

        self.play(FadeIn(red_baseline), FadeIn(green_wave), run_time=max(0.05, 1.58))
        self.wait(max(0.05, 1.22))

        # ------------------------------------------------------------
        # Beat 4: red baseline dims, green oscillations stay bright,
        # right label fades in.
        # ------------------------------------------------------------
        right_label = Text(
            "faster variations remain",
            font_size=30,
            weight=BOLD,
            color=GREEN,
        ).move_to(np.array([right_panel.get_center()[0], right_panel.get_top()[1] - 0.6, 0]))

        self.play(
            red_baseline.animate.set_opacity(0.35),
            FadeIn(right_label),
            run_time=max(0.05, 3.30),
        )
        self.wait(max(0.05, 0.96))

        # ------------------------------------------------------------
        # Beat 5: left label fades in.
        # ------------------------------------------------------------
        left_label = Text(
            "slow variations removed",
            font_size=30,
            weight=BOLD,
            color=RED,
        ).move_to(np.array([left_panel.get_center()[0], left_panel.get_top()[1] - 0.6, 0]))

        self.play(FadeIn(left_label), run_time=max(0.05, 0.92))

        # ------------------------------------------------------------
        # Vehicles: helpers
        # ------------------------------------------------------------
        def make_vehicle(body_color):
            body = RoundedRectangle(
                corner_radius=0.08,
                width=0.75,
                height=0.32,
                fill_color=body_color,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=1.2,
            ).move_to(ORIGIN)

            wheel1 = Circle(
                radius=0.07,
                color=GREY,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to(np.array([-0.2, body.get_bottom()[1] - 0.07, 0]))

            wheel2 = Circle(
                radius=0.07,
                color=GREY,
                fill_opacity=1.0,
                stroke_width=0,
            ).move_to(np.array([0.2, body.get_bottom()[1] - 0.07, 0]))

            return VGroup(body, wheel1, wheel2)

        def place_body_at(vehicle, x, y):
            body = vehicle[0]
            vehicle.shift(np.array([x, y, 0]) - body.get_center())

        body_y = road_top_y + 0.30  # wheels sit on road

        def make_checkmark(color=GREEN):
            line1 = Line(
                start=np.array([-0.18, -0.05, 0]),
                end=np.array([0.0, 0.18, 0]),
                color=color,
                stroke_width=6,
            )
            line2 = Line(
                start=np.array([0.0, 0.18, 0]),
                end=np.array([0.28, -0.22, 0]),
                color=color,
                stroke_width=6,
            )
            return VGroup(line1, line2)

        def make_cross(color=RED):
            line1 = Line(
                start=np.array([-0.15, -0.15, 0]),
                end=np.array([0.15, 0.15, 0]),
                color=color,
                stroke_width=6,
            )
            line2 = Line(
                start=np.array([-0.15, 0.15, 0]),
                end=np.array([0.15, -0.15, 0]),
                color=color,
                stroke_width=6,
            )
            return VGroup(line1, line2)

        # ------------------------------------------------------------
        # Beat 6: fast vehicle passes through the raised gate.
        # ------------------------------------------------------------
        fast_vehicle = make_vehicle(BLUE)
        place_body_at(fast_vehicle, -6.8, body_y)

        gate_pos = np.array([-3.2, body_y, 0])
        exit_pos = np.array([-0.55, body_y, 0])

        checkmark_pos = np.array([gate_pos[0], body_y + 0.55, 0])
        checkmark = make_checkmark().move_to(checkmark_pos)

        self.play(fast_vehicle.animate.move_to(gate_pos), run_time=max(0.05, 0.8), rate_func=linear)
        self.play(FadeIn(checkmark), run_time=max(0.05, 0.18))
        self.play(
            fast_vehicle.animate.move_to(exit_pos),
            checkmark.animate.set_opacity(0),
            run_time=max(0.05, 1.0),
            rate_func=linear,
        )
        self.play(FadeOut(fast_vehicle), run_time=max(0.05, 0.2))

        # ------------------------------------------------------------
        # Beat 7: slow vehicle approaches, gate arm drops, red X appears.
        # ------------------------------------------------------------
        slow_vehicle = make_vehicle(ORANGE)
        place_body_at(slow_vehicle, -6.8, body_y)

        slow_stop_pos = np.array([-5.6, body_y, 0])
        cross_pos = np.array([slow_stop_pos[0], body_y + 0.55, 0])
        cross = make_cross().move_to(cross_pos)

        self.play(slow_vehicle.animate.move_to(slow_stop_pos), run_time=max(0.05, 1.3), rate_func=linear)
        self.play(
            gate_arm.animate.rotate(-PI / 3, about_point=pivot),
            FadeIn(cross),
            run_time=max(0.05, 0.58),
        )

        # Gap between beats 7 and 8
        self.wait(max(0.05, 0.72))

        # ------------------------------------------------------------
        # Beat 8: hold with slow vehicle stopped and fast vehicle gone.
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.44))
        self.wait(max(0.05, 0.22))

        # ------------------------------------------------------------
        # Beat 9: dashed translucent filter window sweeps across the
        # right-panel signal while the red baseline fades further.
        # ------------------------------------------------------------
        window_w = 1.7
        window_h = 3.0
        win_left_x = 0.85
        win_mid_x = 3.5

        window_fill = Rectangle(
            width=window_w,
            height=window_h,
            fill_color=TEAL,
            fill_opacity=0.18,
            stroke_width=0,
        )
        top_dash = DashedLine(
            start=np.array([-window_w / 2, window_h / 2, 0]),
            end=np.array([window_w / 2, window_h / 2, 0]),
            dash_length=0.12,
            dashed_ratio=0.5,
            color=WHITE,
            stroke_width=1.8,
        )
        bottom_dash = DashedLine(
            start=np.array([-window_w / 2, -window_h / 2, 0]),
            end=np.array([window_w / 2, -window_h / 2, 0]),
            dash_length=0.12,
            dashed_ratio=0.5,
            color=WHITE,
            stroke_width=1.8,
        )
        left_dash = DashedLine(
            start=np.array([-window_w / 2, -window_h / 2, 0]),
            end=np.array([-window_w / 2, window_h / 2, 0]),
            dash_length=0.12,
            dashed_ratio=0.5,
            color=WHITE,
            stroke_width=1.8,
        )
        right_dash = DashedLine(
            start=np.array([window_w / 2, -window_h / 2, 0]),
            end=np.array([window_w / 2, window_h / 2, 0]),
            dash_length=0.12,
            dashed_ratio=0.5,
            color=WHITE,
            stroke_width=1.8,
        )
        filter_window = VGroup(window_fill, top_dash, bottom_dash, left_dash, right_dash)
        filter_window.move_to(np.array([win_left_x, 0.0, 0]))

        self.play(
            filter_window.animate.move_to(np.array([win_mid_x, 0.0, 0])),
            red_baseline.animate.set_opacity(0.12),
            run_time=max(0.05, 4.36),
            rate_func=linear,
        )

        # Gap between beats 9 and 10
        self.wait(max(0.05, 0.64))

        # ------------------------------------------------------------
        # Beat 10: window reaches right edge and fades, red baseline
        # nearly disappears, red left label pulses once.
        # ------------------------------------------------------------
        win_right_x = 6.0

        self.play(
            filter_window.animate.move_to(np.array([win_right_x, 0.0, 0])),
            red_baseline.animate.set_opacity(0.04),
            left_label.animate.scale(1.04),
            run_time=max(0.05, 0.91),
            rate_func=linear,
        )
        self.play(
            left_label.animate.scale(1 / 1.04),
            filter_window.animate.set_opacity(0),
            run_time=max(0.05, 0.91),
        )

        # ------------------------------------------------------------
        # Beat 11: hold the finished two-panel composition until end.
        # ------------------------------------------------------------
        self.wait(max(0.05, 8.15))