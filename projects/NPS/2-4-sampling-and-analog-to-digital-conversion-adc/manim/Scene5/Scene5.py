ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Helper: continuous sine waveform points.
        # ----------------------------------------------------------------
        def wave_points(x_min, x_max, base_y, amp, phase=0.0, n=180):
            pts = []
            for x in np.linspace(x_min, x_max, n):
                frac = (x - x_min) / (x_max - x_min)
                y = base_y + amp * np.sin(2 * PI * 2.5 * frac + phase)
                pts.append([x, y, 0.0])
            return pts

        # ----------------------------------------------------------------
        # BEAT 1: 0.00 - 3.46
        # Re-create the previous scene's ending composition: three waveform
        # panels with sparse/medium/dense dots + the bold takeaway.
        # ----------------------------------------------------------------
        PANEL_W = 3.2
        PANEL_H = 2.2
        PANEL_Y = 1.40
        PANEL_XS = [-4.1, 0.0, 4.1]
        PANEL_WAVE_BASE = PANEL_Y - 0.50
        PANEL_WAVE_AMP = 0.45

        prev_comp = VGroup()
        panel_frames = VGroup()

        for cx in PANEL_XS:
            frame = Rectangle(width=PANEL_W, height=PANEL_H, color=GREY_B, stroke_width=1.5)
            frame.move_to(np.array([cx, PANEL_Y, 0.0]))
            x_axis = Line(
                start=np.array([cx - PANEL_W / 2 + 0.15, PANEL_Y - 0.65, 0.0]),
                end=np.array([cx + PANEL_W / 2 - 0.15, PANEL_Y - 0.65, 0.0]),
                color=WHITE,
                stroke_width=1.2,
            )
            y_axis = Line(
                start=np.array([cx - PANEL_W / 2 + 0.15, PANEL_Y - 0.65, 0.0]),
                end=np.array([cx - PANEL_W / 2 + 0.15, PANEL_Y + 0.55, 0.0]),
                color=WHITE,
                stroke_width=1.2,
            )
            wave = VMobject()
            wave.set_stroke(BLUE, width=3)
            wave.set_points_as_corners(
                wave_points(cx - 1.15, cx + 1.15, PANEL_WAVE_BASE, PANEL_WAVE_AMP, n=200)
            )
            panel_frames.add(VGroup(frame, x_axis, y_axis, wave))

        prev_comp.add(panel_frames)

        dot_counts = [9, 18, 80]
        dot_colors = [TEAL, BLUE, PURPLE]
        dot_radii = [0.065, 0.055, 0.035]
        panel_dots_group = VGroup()

        for i, cx in enumerate(PANEL_XS):
            dots = VGroup()
            for x in np.linspace(cx - 1.15, cx + 1.15, dot_counts[i]):
                frac = (x - (cx - 1.15)) / 2.3
                y = PANEL_WAVE_BASE + PANEL_WAVE_AMP * np.sin(2 * PI * 2.5 * frac)
                dots.add(
                    Dot(
                        point=np.array([x, y, 0.0]),
                        radius=dot_radii[i],
                        color=dot_colors[i],
                        fill_opacity=1,
                    )
                )
            panel_dots_group.add(dots)

        prev_comp.add(panel_dots_group)

        left_panel_label = Text("250 Hz", font_size=28, weight="BOLD", color=TEAL)
        left_panel_label.next_to(panel_frames[0], UP, buff=0.20)
        mid_panel_label = Text("500 Hz", font_size=28, weight="BOLD", color=BLUE)
        mid_panel_label.next_to(panel_frames[1], UP, buff=0.20)
        right_panel_label = Text("1000 Hz", font_size=28, weight="BOLD", color=PURPLE)
        right_panel_label.next_to(panel_frames[2], UP, buff=0.20)
        prev_comp.add(left_panel_label, mid_panel_label, right_panel_label)

        takeaway = Text(
            "Sampling frequency must be sufficiently high\n"
            "to capture the important characteristics\n"
            "of the biological signal without losing information.",
            font_size=22,
            color=YELLOW,
            weight="BOLD",
            line_spacing=0.85,
        )
        takeaway.scale_to_fit_width(12.2)
        takeaway.move_to(np.array([0.0, -1.85, 0.0]))
        prev_comp.add(takeaway)

        self.add(prev_comp)
        self.wait(max(0.05, 0.68))
        self.play(FadeOut(prev_comp), run_time=max(0.05, 0.62))

        # ----------------------------------------------------------------
        # Build the Figure 2.4-style flow diagram.
        # ----------------------------------------------------------------
        main_y = 0.45
        wave_center = np.array([-4.8, main_y, 0.0])
        sampling_center = np.array([-2.5, main_y, 0.0])
        adc_center = np.array([0.1, main_y, 0.0])
        digital_center = np.array([3.8, main_y, 0.0])

        # Left: small analog waveform axes.
        wave_frame = Rectangle(width=2.0, height=1.25, color=WHITE, stroke_width=1.5)
        wave_frame.move_to(wave_center)
        wave_x_min = wave_center[0] - 0.75
        wave_x_max = wave_center[0] + 0.75
        wave_axis_y = wave_center[1] - 0.40
        wave_axis_top = wave_center[1] + 0.45

        wave_x_axis = Line(
            start=np.array([wave_x_min, wave_axis_y, 0.0]),
            end=np.array([wave_x_max, wave_axis_y, 0.0]),
            color=WHITE,
            stroke_width=1.2,
        )
        wave_y_axis = Line(
            start=np.array([wave_x_min, wave_axis_y, 0.0]),
            end=np.array([wave_x_min, wave_axis_top, 0.0]),
            color=WHITE,
            stroke_width=1.2,
        )
        flow_wave = VMobject()
        flow_wave.set_stroke(BLUE, width=3.5)
        flow_wave.set_points_as_corners(
            wave_points(wave_x_min, wave_x_max, wave_center[1] + 0.05, 0.30, n=220)
        )
        analog_label = Text("analog waveform", font_size=18, color=GREY)
        analog_label.next_to(wave_frame, UP, buff=0.12)
        wave_group = VGroup(wave_frame, wave_x_axis, wave_y_axis, flow_wave, analog_label)
        wave_group.set_opacity(0.65)

        # Sampling box.
        sampling_box = Rectangle(
            width=1.5,
            height=0.9,
            fill_color=BLUE,
            fill_opacity=0.30,
            stroke_color=BLUE,
            stroke_width=2,
        )
        sampling_box.move_to(sampling_center)
        sampling_text = Text("Sampling", font_size=22, color=WHITE, weight="BOLD")
        sampling_text.move_to(sampling_box.get_center())
        sampling_box_group = VGroup(sampling_box, sampling_text)
        sampling_box_group.set_opacity(0.65)

        # ADC chip-shaped component.
        adc_body = Rectangle(
            width=1.6,
            height=0.9,
            fill_color=ORANGE,
            fill_opacity=0.85,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        adc_body.move_to(adc_center)
        adc_text = Text("ADC", font_size=26, color=BLACK, weight="BOLD")
        adc_text.move_to(adc_body.get_center())
        adc_pins = VGroup()
        for i in range(4):
            off = -0.3 + i * 0.2
            adc_pins.add(
                Rectangle(
                    width=0.13,
                    height=0.10,
                    fill_color=GREY,
                    fill_opacity=0.9,
                    stroke_width=0,
                ).move_to(adc_center + np.array([-0.85, off, 0.0]))
            )
            adc_pins.add(
                Rectangle(
                    width=0.13,
                    height=0.10,
                    fill_color=GREY,
                    fill_opacity=0.9,
                    stroke_width=0,
                ).move_to(adc_center + np.array([0.85, off, 0.0]))
            )
        adc_chip = VGroup(adc_body, adc_pins, adc_text)
        adc_chip.set_opacity(0.55)

        # Right: discrete digital bars/dots.
        digital_bar_xs = np.linspace(digital_center[0] - 1.0, digital_center[0] + 1.0, 8)
        digital_bar_heights = []
        digital_bars = VGroup()
        digital_bar_bottom = digital_center[1] - 0.45

        for i, x in enumerate(digital_bar_xs):
            h = 0.25 + 0.5 * (0.5 + 0.5 * np.sin(2 * PI * 0.55 * i / 7))
            digital_bar_heights.append(h)
            bar = Rectangle(
                width=0.12,
                height=h,
                fill_color=PURPLE,
                fill_opacity=0.75,
                stroke_width=0,
            )
            bar.move_to(np.array([x, digital_bar_bottom + h / 2, 0.0]))
            digital_bars.add(bar)

        digital_label = Text("Digital Data", font_size=22, color=PURPLE, weight="BOLD")
        digital_label.next_to(digital_bars, UP, buff=0.15)
        digital_group = VGroup(digital_bars, digital_label)
        digital_group.set_opacity(0.65)

        # Arrows.
        arrow_y = main_y
        arrow1 = Arrow(
            start=np.array([wave_center[0] + 1.0, arrow_y, 0.0]),
            end=np.array([sampling_center[0] - 0.75, arrow_y, 0.0]),
            color=GREY_B,
            stroke_width=3,
            buff=0.06,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow2 = Arrow(
            start=np.array([sampling_center[0] + 0.75, arrow_y, 0.0]),
            end=adc_chip.get_left() + RIGHT * 0.06,
            color=GREY_B,
            stroke_width=3,
            buff=0.06,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow3 = Arrow(
            start=adc_chip.get_right() + LEFT * 0.06,
            end=np.array([digital_center[0] - 1.0, arrow_y, 0.0]),
            color=GREY_B,
            stroke_width=3,
            buff=0.06,
            max_tip_length_to_length_ratio=0.18,
        )

        flow_group = VGroup(
            wave_group,
            sampling_box_group,
            adc_chip,
            digital_group,
            arrow1,
            arrow2,
            arrow3,
        )

        # Build the flow diagram, then soften the ADC in as the component
        # that actually does the conversion.
        self.play(FadeIn(flow_group), run_time=max(0.05, 1.30))
        self.play(adc_chip.animate.set_opacity(1.0).scale(1.03), run_time=max(0.05, 0.45))
        self.play(adc_body.animate.set_stroke(YELLOW, width=4), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.21))

        # ----------------------------------------------------------------
        # BEAT 2: 3.46 - 6.24
        # Pulse the ADC and label it analog-to-digital converter.
        # ----------------------------------------------------------------
        adc_label = Text(
            "analog-to-digital converter (ADC)",
            font_size=24,
            color=YELLOW,
            weight="BOLD",
        )
        adc_label.next_to(adc_chip, UP, buff=0.25)

        self.play(Indicate(adc_chip, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 1.20))
        self.play(FadeIn(adc_label), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.78))

        # ----------------------------------------------------------------
        # BEAT 3: 6.24 - 11.22
        # Definition beneath the diagram + eye flow from analog to digital.
        # ----------------------------------------------------------------
        definition = Text(
            "converts an analog electrical signal into a sequence of digital numbers",
            font_size=28,
            color=WHITE,
        )
        definition.scale_to_fit_width(12)
        definition.move_to(np.array([0.0, -2.0, 0.0]))
        self.play(FadeIn(definition), run_time=max(0.05, 0.80))

        self.play(Indicate(wave_group, color=BLUE, scale_factor=1.04), run_time=max(0.05, 0.70))
        self.play(Indicate(sampling_box_group, color=BLUE, scale_factor=1.04), run_time=max(0.05, 0.70))
        self.play(Indicate(adc_chip, color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.70))
        self.play(Indicate(digital_group, color=PURPLE, scale_factor=1.04), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 1.38))

        # ----------------------------------------------------------------
        # BEAT 4: 11.22 - 12.00
        # Hold definition + diagram, ADC highlight settles.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.78))

        # ----------------------------------------------------------------
        # BEAT 5: 12.00 - 15.58
        # Full path emphasis + bridge caption.
        # ----------------------------------------------------------------
        self.play(FadeOut(definition), run_time=max(0.05, 0.40))
        self.play(Indicate(wave_group, color=BLUE, scale_factor=1.06), run_time=max(0.05, 0.40))
        self.play(Indicate(arrow1, color=YELLOW, scale_factor=1.10), run_time=max(0.05, 0.35))
        self.play(Indicate(arrow2, color=YELLOW, scale_factor=1.10), run_time=max(0.05, 0.35))
        self.play(Indicate(digital_group, color=PURPLE, scale_factor=1.06), run_time=max(0.05, 0.40))

        bridge_caption = Text(
            "bridge between the analog world and the digital world",
            font_size=30,
            color=WHITE,
            weight="BOLD",
            t2c={"analog world": BLUE, "digital world": PURPLE},
        )
        bridge_caption.scale_to_fit_width(12)
        bridge_caption.move_to(np.array([0.0, -2.0, 0.0]))
        self.play(FadeIn(bridge_caption), run_time=max(0.05, 0.55))
        self.play(wave_group.animate.set_opacity(1.0), run_time=max(0.05, 0.35))
        self.play(digital_group.animate.set_opacity(1.0), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.43))

        # ----------------------------------------------------------------
        # BEAT 6: 15.58 - 16.18
        # Hold bridge caption and highlighted diagram.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.60))

        # ----------------------------------------------------------------
        # BEAT 7: 16.18 - 20.76
        # Conditioned biological signal entering the ADC path.
        # ----------------------------------------------------------------
        self.play(bridge_caption.animate.set_opacity(0.35), run_time=max(0.05, 0.40))

        entry_label = Text(
            "amplified and conditioned biological signal",
            font_size=20,
            color=GREY,
        )
        entry_label.scale_to_fit_width(4.8)
        entry_label.next_to(wave_group, DOWN, buff=0.35)
        self.play(FadeIn(entry_label), run_time=max(0.05, 0.60))

        signal_dot = Dot(radius=0.07, color=YELLOW, fill_opacity=1)
        signal_dot.move_to(np.array([wave_center[0] + 1.0, main_y, 0.0]))
        self.add(signal_dot)
        self.play(signal_dot.animate.move_to(sampling_center), run_time=max(0.05, 0.80))
        self.play(
            signal_dot.animate.move_to(adc_chip.get_left() + RIGHT * 0.08),
            run_time=max(0.05, 0.80),
        )

        enters_text = Text("enters the ADC", font_size=22, color=YELLOW, weight="BOLD")
        enters_text.next_to(adc_chip, DOWN, buff=0.25)
        self.play(adc_chip.animate.set_opacity(1.0), FadeIn(enters_text), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 1.28))

        # ----------------------------------------------------------------
        # BEAT 8: 20.76 - 21.74
        # Hold with signal visibly entering the ADC.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.98))

        # ----------------------------------------------------------------
        # BEAT 9: 21.74 - 24.04
        # ADC front and center + two numbered task slots.
        # ----------------------------------------------------------------
        self.play(
            FadeOut(entry_label),
            FadeOut(enters_text),
            FadeOut(signal_dot),
            run_time=max(0.05, 0.50),
        )

        self.play(
            adc_chip.animate.scale(1.25).set_opacity(1.0),
            wave_group.animate.set_opacity(0.35),
            sampling_box_group.animate.set_opacity(0.35),
            digital_group.animate.set_opacity(0.35),
            arrow1.animate.set_opacity(0.30),
            arrow2.animate.set_opacity(0.30),
            arrow3.animate.set_opacity(0.30),
            run_time=max(0.05, 1.20),
        )

        # Keep the long ADC label positioned above the scaled chip.
        adc_label.next_to(adc_chip, UP, buff=0.25)

        slot1_box = Rectangle(
            width=2.9,
            height=0.8,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        slot1_box.move_to(adc_chip.get_center() + LEFT * 2.0 + DOWN * 0.85)
        slot1_num = Text("1", font_size=22, color=YELLOW, weight="BOLD")
        slot1_num.move_to(slot1_box.get_left() + RIGHT * 0.35)

        slot2_box = Rectangle(
            width=2.9,
            height=0.8,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        slot2_box.move_to(adc_chip.get_center() + RIGHT * 2.0 + DOWN * 0.85)
        slot2_num = Text("2", font_size=22, color=YELLOW, weight="BOLD")
        slot2_num.move_to(slot2_box.get_left() + RIGHT * 0.35)

        task_slots = VGroup(slot1_box, slot1_num, slot2_box, slot2_num)
        self.play(FadeIn(task_slots), run_time=max(0.05, 0.60))

        # ----------------------------------------------------------------
        # BEAT 10: 24.04 - 24.86
        # Hold the two numbered task slots.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.82))

        # ----------------------------------------------------------------
        # BEAT 11: 24.86 - 28.36
        # Regular sampling lines on waveform + task slot 1 text.
        # ----------------------------------------------------------------
        sampling_xs = np.linspace(wave_center[0] - 0.65, wave_center[0] + 0.65, 8)
        sampling_lines = VGroup()
        for sx in sampling_xs:
            sampling_lines.add(
                DashedLine(
                    start=np.array([sx, wave_center[1] - 0.40, 0.0]),
                    end=np.array([sx, wave_center[1] + 0.45, 0.0]),
                    dash_length=0.08,
                    color=YELLOW,
                    stroke_width=2,
                )
            )
        sampling_lines.set_opacity(0.80)

        self.play(
            LaggedStart(*[FadeIn(line) for line in sampling_lines], lag_ratio=0.30),
            run_time=max(0.05, 1.80),
        )
        self.play(Indicate(sampling_lines, color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.80))

        task1_text = Text("sample at regular intervals", font_size=18, color=WHITE)
        task1_text.scale_to_fit_width(2.3)
        task1_text.move_to(slot1_box.get_center() + RIGHT * 0.25)
        self.play(FadeIn(task1_text), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.20))

        # ----------------------------------------------------------------
        # BEAT 12: 28.36 - 29.30
        # Hold the sampling-lines moment and task slot 1.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.94))

        # ----------------------------------------------------------------
        # BEAT 13: 29.30 - 34.52
        # Numeric values on digital bars + task slot 2 text.
        # ----------------------------------------------------------------
        sample_markers = VGroup()
        for i, x in enumerate(digital_bar_xs):
            top_y = digital_bar_bottom + digital_bar_heights[i]
            dot = Dot(point=np.array([x, top_y, 0.0]), radius=0.06, color=YELLOW, fill_opacity=1)
            value_text = Text(f"{0.6 * np.sin(2 * PI * 2.5 * i / 7):.2f}", font_size=16, color=PURPLE)
            value_text.move_to(np.array([x, digital_bar_bottom - 0.25, 0.0]))
            sample_markers.add(VGroup(dot, value_text))

        self.play(
            LaggedStart(*[FadeIn(m) for m in sample_markers], lag_ratio=0.35),
            run_time=max(0.05, 3.00),
        )
        self.play(Indicate(sample_markers, color=PURPLE, scale_factor=1.03), run_time=max(0.05, 0.60))

        task2_text = Text("convert each sample to a number", font_size=18, color=WHITE)
        task2_text.scale_to_fit_width(2.3)
        task2_text.move_to(slot2_box.get_center() + RIGHT * 0.25)
        self.play(FadeIn(task2_text), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.82))

        # ----------------------------------------------------------------
        # BEAT 14: 34.52 - 35.48
        # Hold numbered sample dots and both completed task slots.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.96))

        # ----------------------------------------------------------------
        # BEAT 15: 35.48 - 40.76
        # Emphasize numeric sequence left-to-right + digital representation caption.
        # ----------------------------------------------------------------
        self.play(
            slot1_box.animate.set_opacity(0.45),
            slot1_num.animate.set_opacity(0.60),
            task1_text.animate.set_opacity(0.60),
            slot2_box.animate.set_opacity(0.45),
            slot2_num.animate.set_opacity(0.60),
            task2_text.animate.set_opacity(0.60),
            run_time=max(0.05, 0.60),
        )

        self.play(
            LaggedStart(
                *[Indicate(m, color=PURPLE, scale_factor=1.12) for m in sample_markers],
                lag_ratio=0.18,
            ),
            run_time=max(0.05, 2.20),
        )

        self.play(FadeOut(bridge_caption), run_time=max(0.05, 0.30))

        digital_caption = Text(
            "digital representation of the original neural signal",
            font_size=28,
            color=WHITE,
            t2c={"neural signal": YELLOW},
        )
        digital_caption.scale_to_fit_width(12)
        digital_caption.move_to(np.array([0.0, -2.0, 0.0]))
        self.play(FadeIn(digital_caption), run_time=max(0.05, 0.80))
        self.play(Indicate(digital_caption, color=YELLOW, scale_factor=1.03), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.58))

        # ----------------------------------------------------------------
        # BEAT 16: 40.76 - 41.52
        # Hold the digital representation caption and right-side numbers.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.76))

        # ----------------------------------------------------------------
        # BEAT 17: 41.52 - 49.42
        # Modern digital storage / visualization / signal processing list,
        # then return full diagram emphasis to the ADC centerpiece.
        # ----------------------------------------------------------------
        self.play(digital_caption.animate.set_opacity(0.20), run_time=max(0.05, 0.40))
        self.play(FadeOut(digital_caption), run_time=max(0.05, 0.30))

        list_items = VGroup(
            Text("modern digital storage", font_size=22, color=WHITE, weight="BOLD"),
            Text("visualization", font_size=22, color=WHITE, weight="BOLD"),
            Text("signal processing", font_size=22, color=WHITE, weight="BOLD"),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        list_items.scale_to_fit_width(3.8)
        if list_items.height > 1.40:
            list_items.scale_to_fit_height(1.40)
        list_items.next_to(digital_group, DOWN, buff=0.20)

        for i, item in enumerate(list_items):
            self.play(FadeIn(item), run_time=max(0.05, 0.45))
            if i == 0:
                self.play(digital_bars.animate.set_opacity(1.0), run_time=max(0.05, 0.35))
            elif i == 1:
                self.play(digital_label.animate.set_opacity(1.0), run_time=max(0.05, 0.35))
            else:
                self.play(sample_markers.animate.set_opacity(1.0), run_time=max(0.05, 0.35))
            self.wait(max(0.05, 0.15))

        self.play(FadeOut(list_items), run_time=max(0.05, 0.60))

        self.play(
            adc_chip.animate.set_opacity(1.0).scale(1.02),
            wave_group.animate.set_opacity(0.80),
            sampling_box_group.animate.set_opacity(0.80),
            digital_group.animate.set_opacity(0.80),
            arrow1.animate.set_opacity(0.75),
            arrow2.animate.set_opacity(0.75),
            arrow3.animate.set_opacity(0.75),
            run_time=max(0.05, 1.20),
        )

        self.wait(max(0.05, 2.55))