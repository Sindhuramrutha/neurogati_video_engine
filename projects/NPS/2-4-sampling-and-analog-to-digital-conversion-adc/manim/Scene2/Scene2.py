ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Panels and labels
        # ------------------------------------------------------------------
        panel_w = 5.3
        panel_h = 2.55

        left_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            color=WHITE,
            stroke_width=2.5,
        ).move_to(np.array([-3.05, 0.85, 0.0]))

        right_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            color=WHITE,
            stroke_width=2.5,
        ).move_to(np.array([3.05, 0.85, 0.0]))

        label_analogue = Text("Analogue", font_size=26, color=WHITE)
        label_analogue.next_to(left_panel, UP, buff=0.25)

        label_digital = Text("Digital", font_size=26, color=WHITE)
        label_digital.next_to(right_panel, UP, buff=0.25)

        # ------------------------------------------------------------------
        # Analogue curve data
        # ------------------------------------------------------------------
        x_start_l = left_panel.get_left()[0] + 0.25
        x_end_l = left_panel.get_right()[0] - 0.25
        curve_center_y = left_panel.get_center()[1]

        amp_tracker = ValueTracker(0.6)
        wiggle_speed = ValueTracker(0.9)
        phase_state = [0.0]

        def analog_points():
            pts = []
            for x in np.linspace(x_start_l, x_end_l, 160):
                y = curve_center_y + amp_tracker.get_value() * np.sin(
                    2 * np.pi * 1.3 * (x - x_start_l) / (x_end_l - x_start_l)
                    + phase_state[0]
                )
                pts.append(np.array([x, y, 0.0]))
            return pts

        analog_curve = VMobject()
        analog_curve.set_stroke(BLUE, width=4)
        analog_curve.set_points_as_corners(analog_points())
        analog_curve.set_z_index(1)

        analog_glow = VMobject()
        analog_glow.set_stroke(GOLD, width=10, opacity=0.35)
        analog_glow.set_points_as_corners(analog_points())
        analog_glow.set_z_index(0)

        def advance_curve(mob, dt):
            phase_state[0] += dt * wiggle_speed.get_value()
            mob.set_points_as_corners(analog_points())

        def update_glow(mob, dt):
            mob.set_points_as_corners(analog_points())

        # Dashed vertical marker for the sweep
        marker_bottom = left_panel.get_bottom()[1] + 0.25
        marker_top = left_panel.get_top()[1] - 0.25
        marker = DashedLine(
            start=np.array([x_start_l, marker_bottom, 0.0]),
            end=np.array([x_start_l, marker_top, 0.0]),
            color=GREY,
            dash_length=0.08,
            stroke_width=2,
        )

        # ------------------------------------------------------------------
        # Digital bars data
        # ------------------------------------------------------------------
        x_start_r = right_panel.get_left()[0] + 0.25
        x_end_r = right_panel.get_right()[0] - 0.25
        axis_y = right_panel.get_center()[1] - 0.65

        digital_axis = Line(
            start=np.array([x_start_r, axis_y, 0.0]),
            end=np.array([x_end_r, axis_y, 0.0]),
            color=WHITE,
            stroke_width=2.5,
        )

        bar_values = [3, 7, 5, 9, 6, 10, 7, 8, 5, 9, 6, 7]
        n_bars = len(bar_values)
        bar_xs = np.linspace(x_start_r, x_end_r, n_bars)
        bar_width = (bar_xs[1] - bar_xs[0]) * 0.62
        bar_bottom_y = axis_y + 0.08

        digital_bars = VGroup()
        value_labels = VGroup()
        for i, v in enumerate(bar_values):
            h = 0.35 + (v / 10.0) * 1.15
            bar = Rectangle(
                width=bar_width,
                height=h,
                fill_color=ORANGE,
                fill_opacity=1.0,
                stroke_width=0,
            )
            bar.move_to(np.array([bar_xs[i], bar_bottom_y + h / 2.0, 0.0]))
            digital_bars.add(bar)

            val_label = Text(str(v), font_size=16, color=WHITE)
            val_label.next_to(bar, UP, buff=0.07)
            value_labels.add(val_label)

        digital_sub = Text(
            "Digital — discrete numerical values",
            font_size=20,
            color=WHITE,
        )
        digital_sub.scale_to_fit_width(panel_w * 0.95)
        digital_sub.next_to(right_panel, DOWN, buff=0.22)

        # Binary overlay digits
        bit_values = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1]
        binary_digits = VGroup()
        for i, bit in enumerate(bit_values):
            btext = Text(str(bit), font_size=16, color=BLACK, weight="BOLD")
            btext.move_to(digital_bars[i].get_center() + UP * 0.12)
            binary_digits.add(btext)

        # Red warning X
        red_x_center = np.array([
            right_panel.get_center()[0],
            right_panel.get_top()[1] - 0.42,
            0.0,
        ])
        red_size = 0.32
        red_x = VGroup(
            Line(
                red_x_center + UP * red_size + LEFT * red_size,
                red_x_center + DOWN * red_size + RIGHT * red_size,
                color=RED,
                stroke_width=9,
            ),
            Line(
                red_x_center + UP * red_size + RIGHT * red_size,
                red_x_center + DOWN * red_size + LEFT * red_size,
                color=RED,
                stroke_width=9,
            ),
        )

        # ADC chip builder
        def build_adc_chip():
            body = Rectangle(
                width=1.2,
                height=0.8,
                fill_color=BLACK,
                fill_opacity=1.0,
                stroke_color=GOLD,
                stroke_width=2,
            )
            adc_text = Text("ADC", font_size=16, color=WHITE, weight="BOLD")
            adc_text.move_to(body.get_center())

            pins = VGroup()
            for y in [-0.22, 0.0, 0.22]:
                pins.add(
                    Line(
                        np.array([body.get_left()[0], y, 0.0]),
                        np.array([body.get_left()[0] - 0.3, y, 0.0]),
                        color=GOLD,
                        stroke_width=4,
                    )
                )
                pins.add(
                    Line(
                        np.array([body.get_right()[0], y, 0.0]),
                        np.array([body.get_right()[0] + 0.3, y, 0.0]),
                        color=GOLD,
                        stroke_width=4,
                    )
                )

            chip = VGroup(body, pins, adc_text)
            chip.scale_to_fit_height(0.85)
            return chip

        # ------------------------------------------------------------------
        # Beat 1: panels + labels (0.00-1.88)
        # ------------------------------------------------------------------
        self.play(
            FadeIn(left_panel, right_panel, label_analogue, label_digital),
            run_time=max(0.05, 1.88),
        )

        # ------------------------------------------------------------------
        # Beat 2: hold (1.88-2.76)
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.88))

        # ------------------------------------------------------------------
        # Beat 3: draw analogue waveform (2.76-4.44)
        # ------------------------------------------------------------------
        self.play(Write(analog_curve), run_time=max(0.05, 1.68))
        analog_curve.add_updater(advance_curve)

        # ------------------------------------------------------------------
        # Beat 4: dashed marker sweep (4.44-5.52)
        # ------------------------------------------------------------------
        self.add(marker)
        self.play(
            marker.animate.shift(RIGHT * (x_end_l - x_start_l)),
            run_time=max(0.05, 1.08),
        )

        # ------------------------------------------------------------------
        # Beat 5: continue motion + analogue label (5.52-7.08)
        # ------------------------------------------------------------------
        self.play(FadeOut(marker), run_time=max(0.05, 0.25))
        self.play(FadeIn(analog_glow), run_time=max(0.05, 0.30))

        analogue_sub = Text(
            "Analogue — amplitude changes continuously over time",
            font_size=20,
            color=WHITE,
        )
        analogue_sub.scale_to_fit_width(panel_w * 0.95)
        analogue_sub.next_to(left_panel, DOWN, buff=0.22)
        self.play(FadeIn(analogue_sub), run_time=max(0.05, 1.01))

        analog_glow.add_updater(update_glow)
        left_dim_group = VGroup(
            left_panel, label_analogue, analog_curve, analog_glow, analogue_sub
        )

        # ------------------------------------------------------------------
        # Beat 6: hold left panel (7.08-7.78)
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.70))

        # ------------------------------------------------------------------
        # Beat 7: right axis + first bars (7.78-8.94)
        # ------------------------------------------------------------------
        self.play(FadeIn(digital_axis), run_time=max(0.05, 0.65))
        first_bars = digital_bars[0:4]
        per_bar_first = 0.51 / 4
        for bar in first_bars:
            self.play(
                GrowFromEdge(bar, DOWN),
                run_time=max(0.05, per_bar_first),
            )

        # ------------------------------------------------------------------
        # Beat 8: complete bars (8.94-10.26)
        # ------------------------------------------------------------------
        remaining_bars = digital_bars[4:]
        per_bar_remaining = 1.32 / len(remaining_bars)
        for bar in remaining_bars:
            self.play(
                GrowFromEdge(bar, DOWN),
                run_time=max(0.05, per_bar_remaining),
            )

        # ------------------------------------------------------------------
        # Beat 9: numeric labels above bars (10.26-11.56)
        # ------------------------------------------------------------------
        per_label = 1.30 / len(value_labels)
        for label in value_labels:
            self.play(FadeIn(label), run_time=max(0.05, per_label))

        # ------------------------------------------------------------------
        # Beat 10: digital label + sequential pulse (11.56-12.34)
        # ------------------------------------------------------------------
        self.play(FadeIn(digital_sub), run_time=max(0.05, 0.18))
        for bar in digital_bars:
            self.play(
                Indicate(bar, color=YELLOW, scale_factor=1.1),
                run_time=max(0.05, 0.05),
            )

        right_group = VGroup(
            right_panel,
            label_digital,
            digital_axis,
            digital_bars,
            value_labels,
            digital_sub,
        )

        # ------------------------------------------------------------------
        # Beat 11: hold both panels (12.34-13.18)
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------------
        # Beat 12: focus left panel with glow (13.18-14.56)
        # ------------------------------------------------------------------
        self.play(
            analog_glow.animate.set_stroke(opacity=0.75, width=11),
            run_time=max(0.05, 0.70),
        )
        self.play(
            analog_glow.animate.set_stroke(opacity=0.40, width=9),
            run_time=max(0.05, 0.68),
        )

        # ------------------------------------------------------------------
        # Beat 13: make wiggle more pronounced (14.56-16.04)
        # ------------------------------------------------------------------
        self.play(wiggle_speed.animate.set_value(2.2), run_time=max(0.05, 1.48))

        # ------------------------------------------------------------------
        # Beat 14: neural signal tag (16.04-16.54)
        # ------------------------------------------------------------------
        neural_tag = Text("neural signal", font_size=18, color=GOLD)
        neural_tag.move_to(np.array([
            left_panel.get_right()[0] - 1.1,
            left_panel.get_top()[1] - 0.45,
            0.0,
        ]))
        self.play(FadeIn(neural_tag), run_time=max(0.05, 0.50))

        # ------------------------------------------------------------------
        # Beat 15: dim right panel (16.54-17.70)
        # ------------------------------------------------------------------
        self.play(right_group.animate.set_opacity(0.35), run_time=max(0.05, 1.16))

        # ------------------------------------------------------------------
        # Beat 16: amplitude rises and falls (17.70-20.94)
        # ------------------------------------------------------------------
        self.play(
            amp_tracker.animate.set_value(1.05),
            rate_func=there_and_back,
            run_time=max(0.05, 3.24),
        )

        # ------------------------------------------------------------------
        # Beat 17: right panel back to full brightness (20.94-22.00)
        # ------------------------------------------------------------------
        self.play(right_group.animate.set_opacity(1), run_time=max(0.05, 1.06))

        # ------------------------------------------------------------------
        # Beat 18: continuous representation label + pulse (22.00-24.46)
        # ------------------------------------------------------------------
        cont_label = Text("continuous representation", font_size=18, color=WHITE)
        cont_label.move_to(np.array([
            left_panel.get_center()[0],
            left_panel.get_bottom()[1] + 0.35,
            0.0,
        ]))

        self.play(
            analog_glow.animate.set_stroke(opacity=0.95, width=13),
            run_time=max(0.05, 0.70),
        )
        self.play(
            FadeIn(cont_label),
            analog_glow.animate.set_stroke(opacity=0.40, width=9),
            run_time=max(0.05, 0.90),
        )
        self.wait(max(0.05, 0.86))

        # ------------------------------------------------------------------
        # Beat 19: physiological waveform details flash (24.46-27.06)
        # ------------------------------------------------------------------
        detail_fracs = [0.18, 0.34, 0.52, 0.68, 0.84]
        detail_dots = VGroup()
        for frac in detail_fracs:
            x = x_start_l + frac * (x_end_l - x_start_l)
            y = curve_center_y + amp_tracker.get_value() * np.sin(
                2 * np.pi * 1.3 * frac + phase_state[0]
            )
            detail_dots.add(
                Dot(point=np.array([x, y, 0.0]), radius=0.06, color=PINK, fill_opacity=1)
            )

        def update_detail_dots(group, dt):
            for dot, frac in zip(group, detail_fracs):
                x = x_start_l + frac * (x_end_l - x_start_l)
                y = curve_center_y + amp_tracker.get_value() * np.sin(
                    2 * np.pi * 1.3 * frac + phase_state[0]
                )
                dot.move_to(np.array([x, y, 0.0]))

        detail_dots.add_updater(update_detail_dots)

        self.play(FadeIn(detail_dots), run_time=max(0.05, 0.50))
        self.play(
            Indicate(detail_dots, color=WHITE, scale_factor=1.4),
            run_time=max(0.05, 0.70),
        )
        self.play(
            Indicate(detail_dots, color=PINK, scale_factor=1.4),
            run_time=max(0.05, 0.70),
        )
        self.play(FadeOut(detail_dots), run_time=max(0.05, 0.70))

        # ------------------------------------------------------------------
        # Beat 20: red X + dim left panel (27.06-31.36)
        # ------------------------------------------------------------------
        self.play(
            FadeOut(neural_tag, cont_label),
            left_dim_group.animate.set_opacity(0.45),
            run_time=max(0.05, 1.0),
        )
        self.play(SpinInFromNothing(red_x, angle=PI / 4), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 2.40))

        # Brief gap before binary overlay (31.36-31.72)
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------------
        # Beat 21: binary digits overlay (31.72-34.22)
        # ------------------------------------------------------------------
        per_bit = 2.50 / len(binary_digits)
        for bit_digit in binary_digits:
            self.play(FadeIn(bit_digit), run_time=max(0.05, per_bit))

        # ------------------------------------------------------------------
        # Beat 22: bars and binary digits pulse together (34.22-35.02)
        # ------------------------------------------------------------------
        self.play(
            digital_bars.animate.set_opacity(0.75),
            binary_digits.animate.set_opacity(0.75),
            run_time=max(0.05, 0.4),
        )
        self.play(
            digital_bars.animate.set_opacity(1),
            binary_digits.animate.set_opacity(1),
            run_time=max(0.05, 0.4),
        )

        # ------------------------------------------------------------------
        # Beat 23: hold full layout (35.02-35.86)
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------------
        # Beat 24: arrow below panels (35.86-36.64)
        # ------------------------------------------------------------------
        conv_arrow = Arrow(
            start=np.array([left_panel.get_center()[0], -2.35, 0.0]),
            end=np.array([right_panel.get_center()[0], -2.35, 0.0]),
            color=WHITE,
            stroke_width=5,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(Create(conv_arrow), FadeOut(red_x), run_time=max(0.05, 0.78))

        # ------------------------------------------------------------------
        # Beat 25: travelling pulse along arrow (36.64-38.56)
        # ------------------------------------------------------------------
        pulse = VGroup(
            Dot(radius=0.12, color=GOLD, fill_opacity=0.4, stroke_width=0),
            Dot(radius=0.06, color=YELLOW, fill_opacity=1, stroke_width=0),
        )
        pulse.move_to(conv_arrow.get_start())

        pulse_phase = [0.0]
        pulse_period = 1.7

        def update_pulse(group, dt):
            pulse_phase[0] += dt
            frac = (pulse_phase[0] / pulse_period) % 1.0
            start = conv_arrow.get_start()
            end = conv_arrow.get_end()
            group.move_to(start + frac * (end - start))

        pulse.add_updater(update_pulse)
        self.play(FadeIn(pulse), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 1.62))

        # ------------------------------------------------------------------
        # Beat 26: brighten conversion pathway (38.56-40.42)
        # ------------------------------------------------------------------
        self.play(
            left_dim_group.animate.set_opacity(1),
            right_group.animate.set_opacity(1),
            run_time=max(0.05, 1.26),
        )
        self.play(
            analog_glow.animate.set_stroke(opacity=0.40),
            run_time=max(0.05, 0.60),
        )

        # ------------------------------------------------------------------
        # Beat 27: faint convert label (40.42-41.70)
        # ------------------------------------------------------------------
        convert_label = Text("convert", font_size=22, color=GREY)
        convert_label.move_to(conv_arrow.get_center() + UP * 0.45)
        self.play(FadeIn(convert_label), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.73))

        # ------------------------------------------------------------------
        # Beat 28: ADC conversion label (41.70-43.30)
        # ------------------------------------------------------------------
        adc_label = Text("ADC conversion", font_size=28, color=YELLOW, weight="BOLD")
        adc_label.next_to(conv_arrow, DOWN, buff=0.55)
        self.play(FadeOut(convert_label), FadeIn(adc_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.60))

        # ------------------------------------------------------------------
        # Beat 29: hold arrow and ADC label (43.30-44.44)
        # ------------------------------------------------------------------
        self.wait(max(0.05, 1.14))

        # ------------------------------------------------------------------
        # Beat 30: enlarge ADC label + chip icon (44.44-47.74)
        # ------------------------------------------------------------------
        self.play(adc_label.animate.scale(1.2), run_time=max(0.05, 0.5))
        self.play(adc_label.animate.set_color(GOLD), run_time=max(0.05, 0.3))

        adc_chip = build_adc_chip()
        adc_chip.next_to(adc_label, RIGHT, buff=0.35)
        self.play(GrowFromCenter(adc_chip), run_time=max(0.05, 0.9))
        self.play(
            Indicate(adc_chip, color=YELLOW, scale_factor=1.1),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.90))

        # ------------------------------------------------------------------
        # Beat 31: final hold (47.74-48.65)
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.91))