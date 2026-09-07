ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # helper: draw a sine-wave trace (stroke-only VMobject)
        # ------------------------------------------------------------
        def make_wave(amplitude, cycles=1.5, width=1.8, color=BLUE, stroke_width=5):
            wave = VMobject()
            n = 140
            xs = np.linspace(0, width, n)
            ys = amplitude * np.sin(2 * PI * cycles * xs / width)
            pts = [np.array([x - width / 2, y, 0]) for x, y in zip(xs, ys)]
            wave.set_points_as_corners(pts)
            wave.set_stroke(color=color, width=stroke_width)
            wave.set_fill(opacity=0)
            return wave

        # ------------------------------------------------------------
        # previous-scene holdover
        # ------------------------------------------------------------
        prev_box = RoundedRectangle(
            width=6.0, height=1.3, corner_radius=0.2,
            stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.2,
        )
        prev_text = Text(
            "Amplification: increasing amplitude without altering information",
            font_size=28, color=WHITE,
        ).move_to(prev_box.get_center())
        prev_amp = Polygon(
            [-0.5, 0.35, 0], [-0.5, -0.35, 0], [0.5, 0, 0],
        ).set_fill(ORANGE, opacity=0.7).set_stroke(ORANGE, width=2)
        prev_amp.next_to(prev_box, DOWN, buff=0.3)
        prev_group = VGroup(prev_box, prev_text, prev_amp).move_to(ORIGIN)
        self.add(prev_group)

        # ------------------------------------------------------------
        # main diagram pieces
        # ------------------------------------------------------------
        amp_triangle = Polygon(
            [-1.1, 0.8, 0], [-1.1, -0.8, 0], [1.3, 0, 0],
        )
        amp_triangle.set_fill(TEAL, opacity=0.55).set_stroke(TEAL, width=3)
        amp_triangle.move_to(ORIGIN)

        plus_minus_size = 26
        plus_txt = Text("+", font_size=plus_minus_size, color=WHITE)
        minus_txt = Text("−", font_size=plus_minus_size, color=WHITE)
        plus_txt.move_to(amp_triangle.get_right() + LEFT * 0.15 + UP * 0.4)
        minus_txt.move_to(amp_triangle.get_right() + LEFT * 0.15 + DOWN * 0.4)

        input_pos = np.array([-4.6, 0, 0])
        output_pos = np.array([3.0, 0, 0])

        input_wave = make_wave(amplitude=0.32, color=BLUE).move_to(input_pos)
        output_static = make_wave(amplitude=1.45, color=BLUE).move_to(output_pos)

        input_label = Text("Input signal", font_size=24, color=WHITE).next_to(
            input_wave, DOWN, buff=0.2
        )
        output_label = Text("Output signal", font_size=24, color=WHITE).next_to(
            output_static, DOWN, buff=0.2
        )

        input_to_amp_arrow = Arrow(
            input_wave.get_right() + RIGHT * 0.1,
            amp_triangle.get_left() - RIGHT * 0.1,
            color=GREY_A, buff=0.05, stroke_width=2,
        )
        amp_to_output_arrow = Arrow(
            amp_triangle.get_right() + RIGHT * 0.1,
            output_static.get_left() - RIGHT * 0.1,
            color=GREY_A, buff=0.05, stroke_width=2,
        )

        diagram_group = VGroup(
            input_wave, input_label,
            amp_triangle, plus_txt, minus_txt,
            output_static, output_label,
            input_to_amp_arrow, amp_to_output_arrow,
        )

        # ------------------------------------------------------------
        # 0.00-1.66 : transition into block diagram
        # ------------------------------------------------------------
        self.play(FadeOut(prev_group), FadeIn(diagram_group), run_time=max(0.05, 1.66))

        # ------------------------------------------------------------
        # 1.66-3.04 : amplifier border + label
        # ------------------------------------------------------------
        amp_border = SurroundingRectangle(amp_triangle, color=YELLOW, buff=0.15, stroke_width=2)
        amp_label = Text("Amplifier", font_size=24, color=YELLOW).next_to(
            amp_triangle, DOWN, buff=0.45
        )

        self.play(Create(amp_border), FadeIn(amp_label), run_time=max(0.05, 0.80))
        self.play(
            amp_border.animate.scale(1.08, about_point=amp_triangle.get_center()),
            run_time=max(0.05, 0.30),
        )
        self.play(
            amp_border.animate.scale(1 / 1.08, about_point=amp_triangle.get_center()),
            run_time=max(0.05, 0.28),
        )

        # ------------------------------------------------------------
        # 3.04-5.82 : small waveform travels through amplifier and grows
        # ------------------------------------------------------------
        amp_entry = amp_triangle.get_left() + RIGHT * 0.7
        moving_wave = input_wave.copy().move_to(input_wave.get_center())
        self.add(moving_wave)

        big_travel = make_wave(amplitude=1.45, color=BLUE).move_to(amp_entry)

        few_label = Text("few microvolts", font_size=22, color=YELLOW).next_to(
            input_label, DOWN, buff=0.12
        )
        processable_label = Text("processable level", font_size=22, color=GREEN).next_to(
            output_label, DOWN, buff=0.12
        )

        self.play(moving_wave.animate.move_to(amp_entry), run_time=max(0.05, 0.55))
        self.play(
            ReplacementTransform(moving_wave, big_travel),
            FadeOut(output_static),
            run_time=max(0.05, 0.60),
        )
        self.play(big_travel.animate.move_to(output_pos), run_time=max(0.05, 0.83))
        self.play(FadeIn(few_label), FadeIn(processable_label), run_time=max(0.05, 0.80))

        output_wave_current = big_travel

        # gap 5.82-6.58
        self.wait(max(0.05, 0.76))

        # ------------------------------------------------------------
        # 6.58-10.62 : zoom in on amplifier, "no new information" label
        # ------------------------------------------------------------
        info_label = Text(
            "does not create new information — only increases magnitude",
            font_size=27, color=YELLOW,
        ).next_to(amp_triangle, UP, buff=0.45)

        amp_glow = amp_triangle.copy()
        amp_glow.set_fill(opacity=0).set_stroke(YELLOW, width=8).set_opacity(0.35)
        amp_glow.scale(1.12, about_point=amp_triangle.get_center())

        self.play(
            self.camera.frame.animate.scale(0.7).move_to(amp_triangle.get_center()),
            run_time=max(0.05, 0.90),
        )
        self.play(FadeIn(info_label), run_time=max(0.05, 0.70))
        self.play(FadeIn(amp_glow), run_time=max(0.05, 0.45))
        self.play(FadeOut(amp_glow), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 1.54))

        # gap 10.62-11.30 : zoom back out to full diagram, remove label
        self.play(
            self.camera.frame.animate.scale(1 / 0.7).move_to(ORIGIN),
            FadeOut(info_label),
            run_time=max(0.05, 0.68),
        )

        # ------------------------------------------------------------
        # 11.30-16.02 : highlight input/output, amplitude arrow
        # ------------------------------------------------------------
        double_arrow = DoubleArrow(
            start=output_wave_current.get_bottom() + LEFT * 1.0 + DOWN * 0.15,
            end=output_wave_current.get_top() + LEFT * 1.0 + UP * 0.15,
            color=YELLOW, stroke_width=3,
        )

        self.play(
            input_wave.animate.set_stroke(color=YELLOW, width=6),
            output_wave_current.animate.set_stroke(color=YELLOW, width=6),
            run_time=max(0.05, 0.60),
        )
        self.play(Create(double_arrow), run_time=max(0.05, 0.50))
        self.play(
            double_arrow.animate.scale(1.08, about_point=double_arrow.get_center()),
            run_time=max(0.05, 0.30),
        )
        self.play(
            double_arrow.animate.scale(1 / 1.08, about_point=double_arrow.get_center()),
            run_time=max(0.05, 0.30),
        )
        self.play(
            input_wave.animate.set_stroke(color=BLUE, width=5),
            output_wave_current.animate.set_stroke(color=BLUE, width=5),
            FadeOut(double_arrow),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 2.52))

        # ------------------------------------------------------------
        # 16.02-20.56 : acquisition system block
        # ------------------------------------------------------------
        subblock_labels = ["Filtering", "Digitization", "Processing"]
        sub_blocks = VGroup()
        for label in subblock_labels:
            rect = Rectangle(
                width=1.7, height=0.42,
                color=BLUE, fill_color=BLUE, fill_opacity=0.25, stroke_width=2,
            )
            txt = Text(label, font_size=16, color=WHITE)
            sub_blocks.add(VGroup(rect, txt))
        sub_blocks.arrange(DOWN, buff=0.12)

        acq_title = Text("Acquisition system", font_size=18, color=BLUE, weight="BOLD")
        acq_content = VGroup(acq_title, sub_blocks).arrange(DOWN, buff=0.15)

        acq_rect = Rectangle(
            width=acq_content.width + 0.5,
            height=acq_content.height + 0.55,
            color=BLUE, fill_color=BLUE, fill_opacity=0.15, stroke_width=2,
        )
        acq_rect.move_to(acq_content)
        acq_system = VGroup(acq_rect, acq_content).move_to(np.array([5.65, 0.3, 0]))

        acq_arrow = Arrow(
            output_wave_current.get_right() + RIGHT * 0.15,
            acq_system.get_left() + LEFT * 0.08,
            color=BLUE, buff=0.1, stroke_width=3,
        )

        self.play(FadeIn(acq_system), Create(acq_arrow), run_time=max(0.05, 0.90))
        self.play(
            output_wave_current.animate.scale(1.05, about_point=output_wave_current.get_left()),
            run_time=max(0.05, 0.35),
        )
        self.play(
            output_wave_current.animate.scale(1 / 1.05, about_point=output_wave_current.get_left()),
            run_time=max(0.05, 0.35),
        )
        self.play(Indicate(acq_system, color=BLUE, scale_factor=1.05), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 2.34))

        # gap 20.56-21.28
        self.wait(max(0.05, 0.72))

        # ------------------------------------------------------------
        # 21.28-27.56 : close-up on small input waveform
        # ------------------------------------------------------------
        eeg_label = Text("EEG signal", font_size=28, color=YELLOW, weight="BOLD").next_to(
            input_wave, UP, buff=0.30
        )
        few_emph = Text("only a few microvolts", font_size=24, color=GOLD, weight="BOLD").next_to(
            input_wave, DOWN, buff=0.40
        )

        bracket_x = input_wave.get_left()[0] - 0.35
        bracket_top = input_wave.get_top()[1]
        bracket_bottom = input_wave.get_bottom()[1]
        bracket_line = Line(
            np.array([bracket_x, bracket_bottom, 0]),
            np.array([bracket_x, bracket_top, 0]),
            color=WHITE, stroke_width=3,
        )
        bracket_top_tick = Line(
            np.array([bracket_x - 0.08, bracket_top, 0]),
            np.array([bracket_x + 0.08, bracket_top, 0]),
            color=WHITE, stroke_width=3,
        )
        bracket_bottom_tick = Line(
            np.array([bracket_x - 0.08, bracket_bottom, 0]),
            np.array([bracket_x + 0.08, bracket_bottom, 0]),
            color=WHITE, stroke_width=3,
        )
        amp_bracket = VGroup(bracket_line, bracket_top_tick, bracket_bottom_tick)
        microvolt_text = Text("µV", font_size=20, color=WHITE).next_to(amp_bracket, LEFT, buff=0.1)

        self.play(
            self.camera.frame.animate.scale(0.45).move_to(input_wave.get_center() + UP * 0.05),
            FadeOut(input_label, few_label),
            run_time=max(0.05, 0.80),
        )
        self.play(FadeIn(eeg_label), FadeIn(few_emph), run_time=max(0.05, 0.60))
        self.play(Create(amp_bracket), FadeIn(microvolt_text), run_time=max(0.05, 0.70))
        self.play(
            amp_bracket.animate.set_stroke(color=YELLOW, width=5).set_opacity(0.85),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 3.73))

        # ------------------------------------------------------------
        # 27.56-34.00 : pan across amplifier, small waveform grows again
        # ------------------------------------------------------------
        moving2 = input_wave.copy().move_to(input_wave.get_center())
        self.add(moving2)

        amp_entry2 = amp_triangle.get_left() + RIGHT * 0.7
        big_travel2 = make_wave(amplitude=1.45, color=BLUE).move_to(amp_entry2)

        same_shape_label = Text(
            "same shape, larger amplitude", font_size=22, color=YELLOW
        ).next_to(output_wave_current, UP, buff=0.30)

        self.play(
            self.camera.frame.animate.move_to(amp_triangle.get_center()),
            moving2.animate.move_to(amp_entry2),
            run_time=max(0.05, 1.00),
        )
        self.play(ReplacementTransform(moving2, big_travel2), run_time=max(0.05, 0.80))
        self.play(
            self.camera.frame.animate.move_to(output_wave_current.get_center() + UP * 0.1),
            big_travel2.animate.move_to(output_wave_current.get_center()),
            run_time=max(0.05, 1.20),
        )
        self.play(FadeOut(big_travel2), FadeIn(same_shape_label), run_time=max(0.05, 0.50))

        output_bracket_x = output_wave_current.get_left()[0] - 0.35
        output_bracket_top = output_wave_current.get_top()[1]
        output_bracket_bottom = output_wave_current.get_bottom()[1]
        output_bracket_line = Line(
            np.array([output_bracket_x, output_bracket_bottom, 0]),
            np.array([output_bracket_x, output_bracket_top, 0]),
            color=GREEN, stroke_width=3,
        )
        output_bracket_top_tick = Line(
            np.array([output_bracket_x - 0.08, output_bracket_top, 0]),
            np.array([output_bracket_x + 0.08, output_bracket_top, 0]),
            color=GREEN, stroke_width=3,
        )
        output_bracket_bottom_tick = Line(
            np.array([output_bracket_x - 0.08, output_bracket_bottom, 0]),
            np.array([output_bracket_x + 0.08, output_bracket_bottom, 0]),
            color=GREEN, stroke_width=3,
        )
        output_bracket = VGroup(output_bracket_line, output_bracket_top_tick, output_bracket_bottom_tick)
        larger_voltage_label = Text("larger voltage", font_size=20, color=GREEN).next_to(
            output_bracket, LEFT, buff=0.1
        )

        self.play(Create(output_bracket), FadeIn(larger_voltage_label), run_time=max(0.05, 0.60))
        self.play(
            output_bracket.animate.set_stroke(color=GREEN, width=5),
            run_time=max(0.05, 0.30),
        )
        self.play(FadeOut(same_shape_label), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 1.64))

        # gap 34.00-34.76 : clear close-up labels/brackets
        closeup_clear = VGroup(
            eeg_label, few_emph, amp_bracket, microvolt_text,
            output_bracket, larger_voltage_label,
        )
        self.play(FadeOut(closeup_clear), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.16))

        # ------------------------------------------------------------
        # 34.76-41.18 : zoom on output, tiny noise spikes, then fade
        # ------------------------------------------------------------
        np.random.seed(42)

        def make_noise_trace(color=PINK, stroke_width=2):
            trace = VMobject()
            n_points = 60
            xs = np.linspace(-0.85, 0.85, n_points)
            ys = 0.22 * (np.random.rand(n_points) - 0.5)
            pts = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
            trace.set_points_as_corners(pts)
            trace.set_stroke(color=color, width=stroke_width)
            trace.set_fill(opacity=0)
            trace.move_to(output_wave_current.get_center())
            return trace

        noise_trace = make_noise_trace()
        noise_label = Text(
            "minimal added noise/distortion", font_size=20, color=PINK
        ).next_to(output_wave_current, RIGHT, buff=0.25)
        noise_label.scale_to_fit_width(2.8)

        self.play(
            self.camera.frame.animate.scale(0.7).move_to(output_wave_current.get_center()),
            run_time=max(0.05, 0.80),
        )
        self.play(Create(noise_trace), run_time=max(0.05, 0.80))
        self.play(Indicate(output_wave_current, color=GREEN, scale_factor=1.02), run_time=max(0.05, 0.80))
        self.play(FadeOut(noise_trace), FadeIn(noise_label), run_time=max(0.05, 0.90))
        self.play(noise_label.animate.set_opacity(0.7), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 2.72))

        # gap 41.18-42.34 : zoom out to full diagram
        self.play(
            self.camera.frame.animate.scale(1 / 0.315).move_to(ORIGIN),
            FadeOut(noise_label),
            run_time=max(0.05, 1.16),
        )

        # ------------------------------------------------------------
        # 42.34-47.20 : callout box with pointer
        # ------------------------------------------------------------
        call_line1 = Text("Purpose: increase signal level", font_size=23, color=WHITE)
        call_line2 = Text("so later stages can operate correctly", font_size=23, color=WHITE)
        not_word = Text("NOT", font_size=23, color=RED, weight="BOLD")
        rest_word = Text(" to improve signal quality", font_size=23, color=WHITE)
        call_line3 = VGroup(not_word, rest_word).arrange(RIGHT, buff=0.08)

        callout_text = VGroup(call_line1, call_line2, call_line3).arrange(DOWN, buff=0.14)

        callout_box = RoundedRectangle(
            width=5.5, height=1.7, corner_radius=0.15,
            stroke_color=YELLOW, fill_color=BLACK, fill_opacity=0.65,
            stroke_width=2,
        )
        callout_box.move_to(np.array([1.6, 2.6, 0]))
        callout_text.scale_to_fit_width(callout_box.width - 0.45)
        callout_text.move_to(callout_box.get_center())

        callout_group = VGroup(callout_box, callout_text)

        pointer_arrow = Arrow(
            start=callout_box.get_bottom() + DOWN * 0.05 + LEFT * 0.4,
            end=amp_triangle.get_right() + UP * 0.2 + LEFT * 0.1,
            color=YELLOW, buff=0.05, stroke_width=3,
        )

        self.play(
            GrowFromCenter(callout_box),
            FadeIn(callout_text),
            Create(pointer_arrow),
            run_time=max(0.05, 1.20),
        )
        self.play(Indicate(pointer_arrow, color=YELLOW, scale_factor=1.1), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 3.06))

        # gap 47.20-48.02
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------
        # 48.02-54.62 : dim diagram, pulse arrow, highlight callout lines
        # ------------------------------------------------------------
        dim_group = VGroup(
            input_wave, output_wave_current, acq_system,
            output_label, processable_label,
        )
        self.play(dim_group.animate.set_opacity(0.3), run_time=max(0.05, 0.70))

        self.play(Indicate(acq_arrow, color=YELLOW, scale_factor=1.1), run_time=max(0.05, 0.80))

        self.play(call_line1.animate.set_color(YELLOW), run_time=max(0.05, 1.50))
        self.play(
            call_line2.animate.set_color(YELLOW),
            call_line1.animate.set_color(WHITE),
            run_time=max(0.05, 1.70),
        )
        self.play(
            rest_word.animate.set_color(YELLOW),
            call_line2.animate.set_color(WHITE),
            run_time=max(0.05, 1.90),
        )

        # ------------------------------------------------------------
        # 54.62-55.55 : final hold and fade, leaving amplifier + callout
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.23))
        final_fade_group = VGroup(
            input_wave, output_wave_current, acq_system, acq_arrow,
            output_label, processable_label,
        )
        self.play(FadeOut(final_fade_group), run_time=max(0.05, 0.70))