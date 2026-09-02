ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Shared geometry / data
        # ------------------------------------------------------------------
        x_min, x_max = -6.0, 2.5
        n_steps = 12
        step_values = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        dx_step = (x_max - x_min) / n_steps

        def f_analog(x):
            return (
                1.5
                + 1.3 * np.sin(1.1 * x) * np.exp(-0.04 * (x + 1))
                + 0.25 * np.cos(2.4 * x)
            )

        def digital_y_at(x):
            idx = int((x - x_min) / dx_step)
            idx = min(max(idx, 0), n_steps - 1)
            return step_values[idx]

        n_curve_pts = 600
        x_vals = np.linspace(x_min, x_max, n_curve_pts)

        analog_pts = np.array([[x, f_analog(x), 0.0] for x in x_vals])
        analog_path = VMobject()
        analog_path.set_points_as_corners(analog_pts)
        analog_path.set_stroke(WHITE, width=5)

        digital_pts = np.array([[x, digital_y_at(x), 0.0] for x in x_vals])
        digital_path = VMobject()
        digital_path.set_points_as_corners(digital_pts)
        digital_path.set_stroke(WHITE, width=5)

        # Ghost of the original analogue curve, revealed later behind the staircase.
        analog_ghost = analog_path.copy()
        analog_ghost.set_stroke(GREY, width=3)
        analog_ghost.set_opacity(0.35)

        # Label that stays under the signal for most of the scene.
        label_analog_signal = Text("Analogue Signal", color=WHITE, font_size=34)
        label_analog_signal.move_to(np.array([-1.75, -0.7, 0.0]))

        # ------------------------------------------------------------------
        # Beat 1: small badge at the right, fade in then out
        # ------------------------------------------------------------------
        badge_bg = RoundedRectangle(
            width=4.6,
            height=0.75,
            corner_radius=0.35,
            stroke_color=GREY_B,
            stroke_width=1.5,
            fill_color="#1A1D24",
            fill_opacity=0.9,
        )
        badge_txt = Text("Amplification & Conditioning", color=WHITE, font_size=22)
        badge_txt.move_to(badge_bg.get_center())
        badge_check = Text("✓", color=GREEN, font_size=26)
        badge_check.next_to(badge_txt, LEFT, buff=0.2)
        badge = VGroup(badge_bg, badge_txt, badge_check)
        badge.scale_to_fit_width(4.2)
        badge.to_corner(UR, buff=0.6)

        self.play(FadeIn(badge), run_time=max(0.05, 0.6))
        self.play(FadeOut(badge), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.48))  # fill gap to next beat

        # ------------------------------------------------------------------
        # Beat 2: analogue waveform and label
        # ------------------------------------------------------------------
        self.play(
            Create(analog_path),
            FadeIn(label_analog_signal),
            run_time=max(0.05, 1.42),
        )

        # ------------------------------------------------------------------
        # Beat 3: pulse two markers on the waveform
        # ------------------------------------------------------------------
        peak_x, trough_x = -4.0, -1.5
        marker_peak = Dot(
            point=np.array([peak_x, f_analog(peak_x), 0.0]),
            radius=0.09,
            color=YELLOW,
            fill_opacity=1,
        )
        marker_trough = Dot(
            point=np.array([trough_x, f_analog(trough_x), 0.0]),
            radius=0.09,
            color=ORANGE,
            fill_opacity=1,
        )

        self.play(GrowFromCenter(marker_peak), GrowFromCenter(marker_trough), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.3))
        self.play(
            marker_peak.animate.scale(2.5).set_opacity(0),
            marker_trough.animate.scale(2.5).set_opacity(0),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 0.16))
        self.remove(marker_peak, marker_trough)

        # ------------------------------------------------------------------
        # Beat 4: subtle emphasis pulse on the waveform
        # ------------------------------------------------------------------
        self.play(analog_path.animate.set_opacity(0.7), run_time=max(0.05, 0.43))
        self.play(analog_path.animate.set_opacity(1.0), run_time=max(0.05, 0.43))

        # ------------------------------------------------------------------
        # Beat 5: hold steady
        # ------------------------------------------------------------------
        self.wait(max(0.05, 1.58))
        self.wait(max(0.05, 0.44))  # gap to beat 6

        # ------------------------------------------------------------------
        # Beat 6: callout to the word "analogue"
        # ------------------------------------------------------------------
        callout_word = Text("analogue", color=YELLOW, font_size=28)
        callout_word.next_to(label_analog_signal, RIGHT, buff=0.6)
        callout_x = 0.5
        callout_point = np.array([callout_x, f_analog(callout_x), 0.0])
        callout_line = Line(
            callout_point,
            callout_word.get_left() + LEFT * 0.1,
            color=YELLOW,
            stroke_width=2,
        )
        callout_dot = Dot(callout_point, color=YELLOW, radius=0.05)

        self.play(
            Create(callout_line),
            FadeIn(callout_word),
            FadeIn(callout_dot),
            run_time=max(0.05, 1.08),
        )

        # ------------------------------------------------------------------
        # Beat 7: moving highlight along the curve
        # ------------------------------------------------------------------
        tracer = Dot(point=analog_path.get_start(), radius=0.07, color=YELLOW, fill_opacity=1)
        self.play(MoveAlongPath(tracer, analog_path), run_time=max(0.05, 2.52))
        self.remove(tracer)

        self.wait(max(0.05, 0.80))  # gap to beat 8

        # ------------------------------------------------------------------
        # Beat 8: stylised computer icon
        # ------------------------------------------------------------------
        computer_frame = RoundedRectangle(
            width=2.2,
            height=1.5,
            corner_radius=0.15,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color="#1A1D24",
            fill_opacity=1,
        )
        screen = Rectangle(
            width=1.8,
            height=1.1,
            color=GREY_B,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
        )
        screen.move_to(computer_frame.get_center())

        stand = Line(
            computer_frame.get_bottom() + DOWN * 0.1,
            computer_frame.get_bottom() + DOWN * 0.45,
            color=WHITE,
            stroke_width=2,
        )
        base = Line(
            stand.get_end() + LEFT * 0.25,
            stand.get_end() + RIGHT * 0.25,
            color=WHITE,
            stroke_width=2,
        )
        computer = VGroup(computer_frame, screen, stand, base)
        computer.move_to(np.array([5.2, 1.5, 0.0]))

        self.play(GrowFromCenter(computer), run_time=max(0.05, 1.34))

        # ------------------------------------------------------------------
        # Beat 9: red X and inactive computer
        # ------------------------------------------------------------------
        red_x = VGroup(
            Line(LEFT * 0.65 + UP * 0.65, RIGHT * 0.65 + DOWN * 0.65, color=RED, stroke_width=12),
            Line(LEFT * 0.65 + DOWN * 0.65, RIGHT * 0.65 + UP * 0.65, color=RED, stroke_width=12),
        ).move_to(np.array([3.3, 1.5, 0.0]))

        self.play(
            Create(red_x),
            computer.animate.set_opacity(0.6).set_color(GREY_B),
            run_time=max(0.05, 3.04),
        )

        # ------------------------------------------------------------------
        # Beat 10: hold red X + inactive computer
        # ------------------------------------------------------------------
        self.wait(max(0.05, 1.02))

        # ------------------------------------------------------------------
        # Beat 11: blank placeholder slots below computer
        # ------------------------------------------------------------------
        slot_rects = VGroup()
        for _ in range(3):
            slot = Rectangle(
                width=0.9,
                height=0.55,
                color=GREY_B,
                fill_color=BLACK,
                fill_opacity=0.3,
                stroke_width=2,
            )
            slot_rects.add(slot)

        slot_rects.arrange(RIGHT, buff=0.25)
        slot_rects.next_to(computer, DOWN, buff=0.7)

        wait_times = [0.17, 0.17, 0.18]
        for slot, wait_t in zip(slot_rects, wait_times):
            self.play(
                slot.animate.set_fill(WHITE, opacity=0.15).set_stroke(WHITE, width=3),
                run_time=max(0.05, 0.6),
            )
            self.wait(max(0.05, wait_t))

        # ------------------------------------------------------------------
        # Beat 12: hold slots + red X
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------------
        # Beat 13: morph to digital staircase + step labels
        # ------------------------------------------------------------------
        step_labels = VGroup()
        for i, val in enumerate(step_values):
            x_center = x_min + i * dx_step + dx_step / 2
            lab = Text(str(val), color=WHITE, font_size=20)
            lab.move_to(np.array([x_center, -0.25, 0.0]))
            step_labels.add(lab)

        self.play(Transform(analog_path, digital_path), run_time=max(0.05, 2.5))
        self.play(
            LaggedStart(
                *[FadeIn(lab) for lab in step_labels],
                lag_ratio=0.05,
            ),
            run_time=max(0.05, 1.42),
        )

        # ------------------------------------------------------------------
        # Beat 14: green check, computer lights up, pulse trace appears
        # ------------------------------------------------------------------
        green_check = Text("✓", color=GREEN, font_size=72)
        green_check.move_to(red_x.get_center())

        pulse_y_low = screen.get_center()[1] - 0.25
        pulse_y_high = screen.get_center()[1] + 0.25
        pulse_x_start = screen.get_left()[0] + 0.2

        pulse_path_points = [
            [pulse_x_start, pulse_y_low, 0.0],
            [pulse_x_start + 0.18, pulse_y_low, 0.0],
            [pulse_x_start + 0.18, pulse_y_high, 0.0],
            [pulse_x_start + 0.36, pulse_y_high, 0.0],
            [pulse_x_start + 0.36, pulse_y_low, 0.0],
            [pulse_x_start + 0.54, pulse_y_low, 0.0],
            [pulse_x_start + 0.54, pulse_y_high, 0.0],
            [pulse_x_start + 0.72, pulse_y_high, 0.0],
            [pulse_x_start + 0.72, pulse_y_low, 0.0],
            [pulse_x_start + 0.90, pulse_y_low, 0.0],
        ]
        pulse = VGroup()
        for j in range(len(pulse_path_points) - 1):
            pulse.add(
                Line(
                    pulse_path_points[j],
                    pulse_path_points[j + 1],
                    color=GREEN,
                    stroke_width=3,
                )
            )
        pulse.set_stroke(GREEN, width=3)

        self.play(
            FadeOut(red_x),
            FadeIn(green_check),
            run_time=max(0.05, 0.6),
        )
        self.play(
            computer.animate.set_opacity(1),
            computer_frame.animate.set_stroke(GREEN, width=3),
            stand.animate.set_stroke(GREEN, width=3),
            base.animate.set_stroke(GREEN, width=3),
            screen.animate.set_stroke(GREEN, width=2).set_fill("#0F1116", opacity=1),
            FadeIn(pulse),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 1.12))

        # ------------------------------------------------------------------
        # Beat 15: four capability words orbit the digital staircase
        # ------------------------------------------------------------------
        store_label = Text("Store", color=WHITE, font_size=34).move_to(np.array([-3.5, 3.3, 0.0]))
        display_label = Text("Display", color=WHITE, font_size=34).move_to(np.array([0.0, 3.3, 0.0]))
        process_label = Text("Process", color=WHITE, font_size=34).move_to(np.array([-3.5, -2.3, 0.0]))
        analyse_label = Text("Analyse", color=WHITE, font_size=34).move_to(np.array([0.0, -2.3, 0.0]))

        for lab in [store_label, display_label, process_label, analyse_label]:
            self.play(FadeIn(lab), run_time=max(0.05, 0.8))
            self.wait(max(0.05, 0.045))

        # ------------------------------------------------------------------
        # Beats 16-19: sequential glows on each capability word
        # ------------------------------------------------------------------
        self.play(store_label.animate.set_color(YELLOW), run_time=max(0.05, 0.35))
        self.play(store_label.animate.set_color(WHITE), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.12))

        self.play(display_label.animate.set_color(YELLOW), run_time=max(0.05, 0.25))
        self.play(display_label.animate.set_color(WHITE), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.10))

        self.play(process_label.animate.set_color(YELLOW), run_time=max(0.05, 0.15))
        self.play(process_label.animate.set_color(WHITE), run_time=max(0.05, 0.15))
        self.wait(max(0.05, 0.04))

        self.play(analyse_label.animate.set_color(YELLOW), run_time=max(0.05, 0.45))
        self.play(analyse_label.animate.set_color(WHITE), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.10))

        # ------------------------------------------------------------------
        # Beat 20: bounding outline + DSP title
        # ------------------------------------------------------------------
        bounding_box = SurroundingRectangle(analog_path, color=GREY_B, stroke_width=2, buff=0.25)
        bounding_box.set_stroke(opacity=0.6)

        dsp_title = Text("Digital Signal Processing", color=YELLOW, font_size=32)
        bottom_labels = VGroup(process_label, analyse_label)
        dsp_title.next_to(bottom_labels, DOWN, buff=0.35)

        self.play(
            FadeIn(bounding_box),
            Write(dsp_title),
            run_time=max(0.05, 2.42),
        )

        self.wait(max(0.05, 0.96))  # gap to beat 21

        # ------------------------------------------------------------------
        # Beat 21: analogue -> digital conversion emphasis
        # ------------------------------------------------------------------
        analogue_to_digital = Text("Analogue → Digital", color=WHITE, font_size=32)
        analogue_to_digital.move_to(np.array([-1.75, -1.15, 0.0]))

        self.play(
            FadeIn(analog_ghost),
            FadeIn(analogue_to_digital),
            computer.animate.set_opacity(0.35),
            store_label.animate.set_opacity(0.35),
            display_label.animate.set_opacity(0.35),
            process_label.animate.set_opacity(0.35),
            analyse_label.animate.set_opacity(0.35),
            analog_path.animate.set_stroke(YELLOW, width=7).set_opacity(1),
            run_time=max(0.05, 3.62),
        )

        # ------------------------------------------------------------------
        # Beat 22: sampling dashed line + dots on staircase
        # ------------------------------------------------------------------
        sample_line = DashedLine(
            start=np.array([x_min, -0.5, 0.0]),
            end=np.array([x_min, 3.3, 0.0]),
            color=YELLOW,
            stroke_width=2,
            dash_length=0.1,
        )

        sample_xs = [x_min + i * dx_step + dx_step / 2 for i in range(n_steps)]
        sample_dots = VGroup()
        for i, xc in enumerate(sample_xs):
            dot = Dot(
                point=np.array([xc, step_values[i], 0.0]),
                radius=0.07,
                color=PINK,
                fill_opacity=1,
            )
            sample_dots.add(dot)

        self.play(
            sample_line.animate.shift(RIGHT * (x_max - x_min)),
            LaggedStart(*[FadeIn(d) for d in sample_dots], lag_ratio=0.05),
            run_time=max(0.05, 0.7),
        )
        self.play(sample_line.animate.shift(LEFT * (x_max - x_min)), run_time=max(0.05, 0.7))
        self.play(sample_line.animate.shift(RIGHT * (x_max - x_min)), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.2))

        # ------------------------------------------------------------------
        # Beat 23: "Sampling" and "ADC" labels
        # ------------------------------------------------------------------
        sampling_label = Text("Sampling", color=YELLOW, font_size=26).move_to(np.array([-4.5, -1.9, 0.0]))
        adc_label = Text("ADC", color=GREEN, font_size=30).move_to(np.array([0.5, -1.9, 0.0]))

        adc_arrow_end = np.array([0.5, digital_y_at(0.5), 0.0])
        adc_arrow = Arrow(
            adc_label.get_top() + UP * 0.1,
            adc_arrow_end,
            color=GREEN,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.1,
        )

        self.play(
            FadeIn(sampling_label),
            FadeIn(adc_label),
            Create(adc_arrow),
            run_time=max(0.05, 1.62),
        )

        # ------------------------------------------------------------------
        # Beat 24: hold final composition
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.94))