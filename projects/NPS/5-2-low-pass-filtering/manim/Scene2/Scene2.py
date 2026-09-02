ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # -- Beat 1: continuity fade to question ---------------------------------
        prev_title = Text("Learning Objectives", font_size=34, color=WHITE).to_edge(UP, buff=0.55)
        prev_items = VGroup(
            *[
                Text(t, font_size=18, color=WHITE)
                for t in [
                    "Define a low-pass filter",
                    "Explain its operating principle.",
                    "Describe the cutoff frequency.",
                    "Identify situations where low-pass filtering is useful.",
                    "Understand both its advantages and its limitations.",
                ]
            ]
        )
        prev_items.arrange(DOWN, buff=0.18)
        prev_items.next_to(prev_title, DOWN, buff=0.30)
        prev_objectives = VGroup(prev_title, prev_items).set_opacity(0.35)

        question_mark = Text("?", font_size=170, color=YELLOW)
        question_title = Text("Low-Pass Filter", font_size=46, color=WHITE)
        question_group = VGroup(question_mark, question_title).arrange(DOWN, buff=0.25)
        question_group.move_to(ORIGIN)

        self.add(prev_objectives)
        self.play(
            FadeOut(prev_objectives),
            FadeIn(question_group),
            run_time=max(0.05, 1.46),
        )
        self.wait(max(0.05, 0.68))

        # -- Beat 2: road and gate appear ----------------------------------------
        CAR_Y = -0.3
        ROAD_Y = -0.8
        PIVOT_X = 0.0
        GATE_PIVOT = np.array([PIVOT_X, CAR_Y, 0])

        road_line = Line(
            np.array([-7.2, ROAD_Y, 0]),
            np.array([7.2, ROAD_Y, 0]),
            color=GREY_B,
            stroke_width=5,
        )

        post = Line(
            np.array([PIVOT_X, -0.65, 0]),
            np.array([PIVOT_X, 1.05, 0]),
            color=GREY_B,
            stroke_width=7,
        )
        pivot_dot = Dot(GATE_PIVOT, radius=0.07, color=YELLOW)
        gate_arm = Line(
            GATE_PIVOT,
            GATE_PIVOT + UP * 1.0,
            color=RED,
            stroke_width=7,
        )

        gate_grp = VGroup(post, pivot_dot, gate_arm)
        road_gate_grp = VGroup(road_line, gate_grp)

        self.play(
            FadeOut(question_group),
            FadeIn(road_gate_grp),
            run_time=max(0.05, 1.22),
        )

        # -- helper: make car -------------------------------------------------------
        def make_car(label_text, color):
            body = RoundedRectangle(
                width=1.3,
                height=0.5,
                corner_radius=0.12,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=0,
            )
            cabin = RoundedRectangle(
                width=0.6,
                height=0.28,
                corner_radius=0.07,
                fill_color=WHITE,
                fill_opacity=0.8,
                stroke_width=0,
            )
            cabin.move_to(body.get_top() + DOWN * 0.18)
            wheel1 = Dot(radius=0.07, color=GREY_B).move_to(
                body.get_left() + RIGHT * 0.25 + DOWN * 0.20
            )
            wheel2 = Dot(radius=0.07, color=GREY_B).move_to(
                body.get_right() + LEFT * 0.25 + DOWN * 0.20
            )
            body_grp = VGroup(body, cabin, wheel1, wheel2)

            arrow = Arrow(
                ORIGIN,
                RIGHT * 0.40,
                buff=0.05,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.4,
            )
            label = Text(label_text, font_size=18, color=WHITE)
            label_row = VGroup(arrow, label).arrange(RIGHT, buff=0.10)
            label_row.next_to(body_grp, DOWN, buff=0.16)

            car = VGroup(body_grp, label_row)
            car.body = body_grp
            return car

        def car_target(car, x, y):
            # Center the body at (x, y); label will follow.
            body_center = car.body.get_center()
            offset = car.get_center() - body_center
            return np.array([x, y, 0]) + offset

        def add_car_at(car, x, y):
            car.move_to(car_target(car, x, y))
            return car

        cars_on_screen = []

        # -- Beat 3: three slow cars pass ----------------------------------------
        slow_cars = [make_car("Low Frequency", TEAL) for _ in range(3)]
        for car, x in zip(slow_cars, [-11.0, -8.0, -5.0]):
            add_car_at(car, x, CAR_Y)
        slow_convoy = VGroup(*slow_cars)
        self.add(slow_convoy)
        cars_on_screen.append(slow_convoy)

        self.play(slow_convoy.animate.shift(RIGHT * 19), run_time=max(0.05, 2.24))
        self.wait(max(0.05, 0.50))

        # -- Beat 4: fast cars approach, gate drops --------------------------------
        fast1 = make_car("High Frequency", ORANGE)
        add_car_at(fast1, -11.0, CAR_Y)
        self.add(fast1)
        cars_on_screen.append(fast1)

        self.play(
            fast1.animate.move_to(car_target(fast1, -3.7, CAR_Y)),
            gate_arm.animate.rotate(PI / 2, about_point=GATE_PIVOT),
            run_time=max(0.05, 0.55),
        )

        fast2 = make_car("High Frequency", ORANGE)
        add_car_at(fast2, -9.5, CAR_Y)
        self.add(fast2)
        cars_on_screen.append(fast2)

        self.play(
            fast2.animate.move_to(car_target(fast2, -6.2, CAR_Y)),
            run_time=max(0.05, 0.55),
        )

        atten_text = Text(
            "attenuating high-frequency components.",
            font_size=24,
            color=ORANGE,
        )
        atten_text.next_to(gate_grp, UP, buff=1.1)
        self.play(FadeIn(atten_text), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 2.44))

        self.wait(max(0.05, 0.64))

        # -- Beat 5: highlight low-pass -------------------------------------------
        lp_word = Text("low-pass", font_size=40, color=YELLOW)
        filter_word = Text(" filter", font_size=40, color=WHITE)
        lp_label = VGroup(lp_word, filter_word).arrange(RIGHT, buff=0.10)
        lp_label.next_to(gate_grp, UP, buff=1.0)

        self.play(FadeOut(atten_text), FadeIn(lp_label), run_time=max(0.05, 0.50))
        self.play(Indicate(lp_word, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.96))

        self.wait(max(0.05, 0.72))

        # -- Beat 6: slow car continues, caption ----------------------------------
        low_pass_caption = Text(
            "low frequencies allowed to pass",
            font_size=20,
            color=GREEN,
        )
        low_pass_caption.move_to(np.array([3.2, 0.6, 0]))

        self.play(
            gate_arm.animate.rotate(-PI / 2, about_point=GATE_PIVOT),
            FadeIn(low_pass_caption),
            run_time=max(0.05, 0.80),
        )

        slow_pass_car = make_car("Low Frequency", TEAL)
        add_car_at(slow_pass_car, -11.0, CAR_Y)
        self.add(slow_pass_car)
        cars_on_screen.append(slow_pass_car)

        self.play(
            slow_pass_car.animate.move_to(car_target(slow_pass_car, 9.0, CAR_Y)),
            run_time=max(0.05, 2.00),
        )
        self.wait(max(0.05, 0.78))

        self.wait(max(0.05, 0.42))

        # -- Beat 7: fast cars reduced, caption update -----------------------------
        high_pass_caption = Text(
            "higher frequencies progressively reduced",
            font_size=20,
            color=ORANGE,
        )
        high_pass_caption.move_to(low_pass_caption.get_center())

        self.play(
            FadeOut(low_pass_caption),
            FadeIn(high_pass_caption),
            fast1.animate.scale(0.5).set_opacity(0.35),
            fast2.animate.scale(0.5).set_opacity(0.35),
            run_time=max(0.05, 0.90),
        )

        slow_cont_car = make_car("Low Frequency", TEAL)
        add_car_at(slow_cont_car, -11.0, CAR_Y)
        self.add(slow_cont_car)
        cars_on_screen.append(slow_cont_car)

        self.play(
            slow_cont_car.animate.move_to(car_target(slow_cont_car, 9.0, CAR_Y)),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.30))

        self.wait(max(0.05, 0.92))

        # -- Beat 8: demonstration cycle with camera zoom --------------------------
        self.camera.frame.save_state()
        gate_focus = GATE_PIVOT + UP * 0.3

        self.play(
            self.camera.frame.animate.scale(0.75).move_to(gate_focus),
            FadeOut(high_pass_caption),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.40))

        # Lower arm quickly to start cycle
        self.play(
            gate_arm.animate.rotate(PI / 2, about_point=GATE_PIVOT),
            run_time=max(0.05, 0.30),
        )

        demo_slow_car = make_car("Low Frequency", TEAL)
        add_car_at(demo_slow_car, -11.0, CAR_Y)
        self.add(demo_slow_car)
        cars_on_screen.append(demo_slow_car)

        self.play(
            gate_arm.animate.rotate(-PI / 2, about_point=GATE_PIVOT),
            demo_slow_car.animate.move_to(car_target(demo_slow_car, 9.0, CAR_Y)),
            run_time=max(0.05, 1.40),
        )

        demo_fast_car = make_car("High Frequency", ORANGE)
        add_car_at(demo_fast_car, -9.5, CAR_Y)
        self.add(demo_fast_car)
        cars_on_screen.append(demo_fast_car)

        self.play(
            gate_arm.animate.rotate(PI / 2, about_point=GATE_PIVOT),
            demo_fast_car.animate.move_to(car_target(demo_fast_car, -3.7, CAR_Y)),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 2.28))

        # -- Beat 9: cross-fade to signal representation ---------------------------
        self.play(
            Restore(self.camera.frame),
            *[FadeOut(mobj) for mobj in cars_on_screen],
            FadeOut(road_line),
            FadeOut(lp_label),
            gate_arm.animate.rotate(-PI / 2, about_point=GATE_PIVOT),
            run_time=max(0.05, 1.20),
        )

        low_wave, low_tracker = self.make_wave(
            amplitude_left=0.5,
            amplitude_right=0.5,
            wave_number=1.2,
            y_center=-0.15,
            color=TEAL,
            stroke_width=5,
            initial_shift=-11.0,
        )
        low_freq_label = Text("Low Frequency", font_size=20, color=TEAL)
        low_freq_label.move_to(np.array([-5.5, -1.0, 0]))

        self.add(low_wave)
        self.play(
            FadeIn(low_freq_label),
            run_time=max(0.05, 0.40),
        )
        self.play(
            low_tracker.animate.set_value(7.0),
            run_time=max(0.05, 3.60),
        )
        self.wait(max(0.05, 0.60))

        self.wait(max(0.05, 0.58))

        # -- Beat 10: high-frequency wave attenuated -------------------------------
        high_wave1, high_tracker1 = self.make_wave(
            amplitude_left=0.5,
            amplitude_right=0.16,
            wave_number=3.5,
            y_center=0.5,
            color=ORANGE,
            stroke_width=5,
            initial_shift=-11.0,
        )
        high_freq_label = Text("High Frequency", font_size=20, color=ORANGE)
        high_freq_label.move_to(np.array([-5.5, 1.4, 0]))

        self.add(high_wave1)
        self.play(
            high_tracker1.animate.set_value(5.0),
            FadeIn(high_freq_label),
            run_time=max(0.05, 1.60),
        )

        sep_caption = Text(
            "separates signal components by frequency",
            font_size=22,
            color=WHITE,
        )
        sep_caption.to_edge(UP, buff=0.7)
        self.play(FadeIn(sep_caption), run_time=max(0.05, 0.64))

        self.wait(max(0.05, 0.74))

        # -- Beat 11: low wave unchanged, bright ----------------------------------
        self.play(FadeOut(low_wave), FadeOut(low_freq_label), run_time=max(0.05, 0.30))

        low_wave2, low_tracker2 = self.make_wave(
            amplitude_left=0.5,
            amplitude_right=0.5,
            wave_number=1.2,
            y_center=-0.15,
            color=YELLOW,
            stroke_width=8,
            initial_shift=-11.0,
        )
        self.add(low_wave2)
        low_freq_label2 = Text("Low Frequency", font_size=20, color=YELLOW)
        low_freq_label2.move_to(np.array([-5.5, -1.0, 0]))
        self.add(low_freq_label2)

        low_change_text = Text(
            "little or no change",
            font_size=24,
            color=TEAL,
        )
        low_change_text.to_edge(DOWN, buff=0.9)

        self.play(
            low_tracker2.animate.set_value(6.0),
            FadeIn(low_change_text),
            run_time=max(0.05, 2.40),
        )
        self.wait(max(0.05, 0.96))

        self.wait(max(0.05, 0.54))

        # -- Beat 12: high wave attenuated, final hold -----------------------------
        self.play(FadeOut(high_wave1), FadeOut(high_freq_label), run_time=max(0.05, 0.30))

        high_wave2, high_tracker2 = self.make_wave(
            amplitude_left=0.5,
            amplitude_right=0.14,
            wave_number=3.5,
            y_center=0.5,
            color=ORANGE,
            stroke_width=5,
            initial_shift=-11.0,
        )
        self.add(high_wave2)
        high_freq_label2 = Text("High Frequency", font_size=20, color=ORANGE)
        high_freq_label2.move_to(np.array([-5.5, 1.4, 0]))
        self.add(high_freq_label2)

        attenuated_label = Text("attenuated", font_size=26, color=ORANGE)
        attenuated_label.move_to(np.array([4.5, 0.9, 0]))

        self.play(
            high_tracker2.animate.set_value(5.0),
            FadeIn(attenuated_label),
            run_time=max(0.05, 1.80),
        )
        self.wait(max(0.05, 0.86))

    def make_wave(
        self,
        amplitude_left,
        amplitude_right,
        wave_number,
        y_center,
        color,
        stroke_width,
        initial_shift,
    ):
        """Return a traveling-wave VMobject and its shift ValueTracker."""
        xs = np.linspace(-7.0, 7.0, 240)
        zs = np.zeros_like(xs)
        tracker = ValueTracker(initial_shift)

        wave = VMobject(
            stroke_color=color,
            stroke_width=stroke_width,
            fill_opacity=0,
        )

        def update_wave(mob):
            shift = tracker.get_value()
            shifted_xs = xs + shift
            amps = np.where(shifted_xs < 0.0, amplitude_left, amplitude_right)
            ys = y_center + amps * np.sin(wave_number * xs)
            points = np.column_stack((shifted_xs, ys, zs))
            mob.set_points_as_corners(points)

        wave.add_updater(update_wave)
        return wave, tracker