ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------
        def sine_wave(width=1.0, height=0.6, color=YELLOW, freq=3, n_points=50):
            pts = []
            for i in range(n_points + 1):
                x = -width / 2 + width * i / n_points
                y = (height / 2) * np.sin(2 * PI * freq * i / n_points)
                pts.append(np.array([x, y, 0.0]))
            wave = VMobject().set_points_as_corners(pts)
            wave.set_stroke(color=color, width=3)
            wave.set_fill(opacity=0)
            return wave

        def make_jagged_path(width=0.8, height=0.3, color=RED, n_points=12):
            pts = []
            for i in range(n_points + 1):
                x = -width / 2 + width * i / n_points
                y = (0.5 - (i % 2)) * height
                pts.append(np.array([x, y, 0.0]))
            path = VMobject().set_points_as_corners(pts)
            path.set_stroke(color=color, width=4)
            path.set_fill(opacity=0)
            return path

        def make_sampling_lines(xs):
            group = VGroup()
            for x in xs:
                line = Line(
                    start=np.array([x, -0.38, 0.0]),
                    end=np.array([x, 0.38, 0.0]),
                    color=YELLOW,
                    stroke_width=3,
                )
                group.add(line)
            return group

        def make_red_x(size=0.5, stroke_width=8):
            s = size / 2.0
            l1 = Line(
                start=np.array([-s, -s, 0.0]),
                end=np.array([s, s, 0.0]),
                color=RED,
                stroke_width=stroke_width,
            )
            l2 = Line(
                start=np.array([-s, s, 0.0]),
                end=np.array([s, -s, 0.0]),
                color=RED,
                stroke_width=stroke_width,
            )
            return VGroup(l1, l2)

        def make_spark():
            return VGroup(
                Line(
                    start=np.array([-0.08, 0.18, 0.0]),
                    end=np.array([0.08, 0.06, 0.0]),
                    color=YELLOW,
                    stroke_width=4,
                ),
                Line(
                    start=np.array([0.08, 0.06, 0.0]),
                    end=np.array([-0.06, -0.02, 0.0]),
                    color=YELLOW,
                    stroke_width=4,
                ),
                Line(
                    start=np.array([-0.06, -0.02, 0.0]),
                    end=np.array([0.08, -0.16, 0.0]),
                    color=YELLOW,
                    stroke_width=4,
                ),
            )

        # ------------------------------------------------------------
        # Build the six main acquisition-chain boxes.
        # ------------------------------------------------------------
        box_w = 1.55
        box_h = 1.50

        stage_boxes = []
        stage_groups = []

        # Electrode
        box1 = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=ORANGE,
            fill_opacity=0.90,
        )
        title1 = Text("Electrode", font_size=18, color=WHITE, weight="BOLD")
        title1.scale_to_fit_width(box_w - 0.30)
        title1.move_to(box1.get_top() + DOWN * 0.30)
        body1 = sine_wave(width=1.05, height=0.55, color=YELLOW, freq=3).move_to(
            box1.get_center() + DOWN * 0.18
        )
        stage_electrode = VGroup(box1, title1, body1)

        # Amplifier
        box2 = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=TEAL,
            fill_opacity=0.90,
        )
        title2 = Text("Amplifier", font_size=18, color=WHITE, weight="BOLD")
        title2.scale_to_fit_width(box_w - 0.30)
        title2.move_to(box2.get_top() + DOWN * 0.30)
        body2 = sine_wave(width=1.05, height=0.75, color=YELLOW, freq=4).move_to(
            box2.get_center() + DOWN * 0.18
        )
        stage_amp = VGroup(box2, title2, body2)

        # ADC
        box3 = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=GREEN,
            fill_opacity=0.90,
        )
        title3 = Text("ADC", font_size=18, color=WHITE, weight="BOLD")
        title3.scale_to_fit_width(box_w - 0.30)
        title3.move_to(box3.get_top() + DOWN * 0.30)

        even_xs = np.linspace(-0.55, 0.55, 6)
        irregular_xs = np.array([-0.55, -0.38, -0.05, 0.15, 0.48, 0.62])
        adc_even_lines = make_sampling_lines(even_xs)
        adc_irregular_lines = make_sampling_lines(irregular_xs)
        adc_even_lines.move_to(box3.get_center() + DOWN * 0.10)
        adc_irregular_lines.move_to(box3.get_center() + DOWN * 0.10)
        stage_adc = VGroup(box3, title3, adc_even_lines)

        # Computer
        box4 = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.90,
        )
        title4 = Text("Computer", font_size=18, color=WHITE, weight="BOLD")
        title4.scale_to_fit_width(box_w - 0.30)
        title4.move_to(box4.get_top() + DOWN * 0.30)

        monitor_rect = Rectangle(
            width=1.10,
            height=0.72,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.7,
        )
        monitor_rect.move_to(box4.get_center() + DOWN * 0.15)
        computer_screen = Rectangle(
            width=0.96,
            height=0.58,
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=BLACK,
            fill_opacity=0.85,
        )
        computer_screen.move_to(monitor_rect.get_center())
        computer_clean_wave = sine_wave(
            width=0.75, height=0.32, color=GREEN, freq=5
        ).move_to(computer_screen.get_center())
        body4 = VGroup(monitor_rect, computer_screen, computer_clean_wave)
        stage_computer = VGroup(box4, title4, body4)

        # Processing
        box5 = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=PURPLE,
            fill_opacity=0.90,
        )
        title5 = Text("Processing", font_size=18, color=WHITE, weight="BOLD")
        title5.scale_to_fit_width(box_w - 0.30)
        title5.move_to(box5.get_top() + DOWN * 0.30)
        gear_icon = SVGMobject(
            ASSET_PATHS["gear"],
            height=0.55,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_width=0,
        )
        gear_icon.move_to(box5.get_center() + DOWN * 0.18)
        stage_processing = VGroup(box5, title5, gear_icon)

        # Display / Analysis
        box6 = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=PINK,
            fill_opacity=0.90,
        )
        title6 = Text("Display / Analysis", font_size=18, color=WHITE, weight="BOLD")
        title6.scale_to_fit_width(box_w - 0.20)
        title6.move_to(box6.get_top() + DOWN * 0.30)

        bar_heights = [0.22, 0.42, 0.30, 0.50, 0.36]
        bar_colors = [WHITE, WHITE, WHITE, WHITE, WHITE]
        bars = VGroup()
        for color, h in zip(bar_colors, bar_heights):
            bar = Rectangle(
                width=0.16,
                height=h,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.07)
        bars.move_to(box6.get_center() + DOWN * 0.18)
        stage_display = VGroup(box6, title6, bars)

        stage_groups = [
            stage_electrode,
            stage_amp,
            stage_adc,
            stage_computer,
            stage_processing,
            stage_display,
        ]
        stage_boxes = [box1, box2, box3, box4, box5, box6]

        chain = VGroup(*stage_groups).arrange(RIGHT, buff=0.60)
        chain.move_to(ORIGIN + UP * 0.7)

        # Arrows between chain boxes. They are created here but not added
        # until beat 2.
        chain_arrows = VGroup()
        for i in range(5):
            arrow = Arrow(
                start=stage_boxes[i].get_right(),
                end=stage_boxes[i + 1].get_left(),
                buff=0.18,
                color=YELLOW,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.25,
            )
            chain_arrows.add(arrow)

        # ------------------------------------------------------------
        # Leftover dimmed downstream boxes and caption from previous
        # scene end-state. They fade out in beat 1.
        # ------------------------------------------------------------
        old_downstream_defs = [
            ("Filtering", PURPLE),
            ("Feature Extraction", PINK),
            ("Spectral Analysis", ORANGE),
            ("Classification", GREEN),
        ]
        old_boxes = VGroup()
        for label, color in old_downstream_defs:
            b = Rectangle(
                width=1.8,
                height=0.50,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.12,
            )
            t = Text(label, font_size=14, color=GREY_B)
            t.scale_to_fit_width(1.55)
            t.move_to(b.get_center())
            old_boxes.add(VGroup(b, t))
        old_boxes.arrange(RIGHT, buff=0.25)
        old_boxes.move_to(np.array([2.5, -3.30, 0.0]))
        old_caption = Text(
            "The computer can only work with what it's been given.",
            font_size=22,
            color=GREY_B,
        )
        old_caption.scale_to_fit_width(9.0)
        old_caption.move_to(np.array([0.0, 3.2, 0.0]))

        self.add(chain, old_boxes, old_caption)

        # ------------------------------------------------------------
        # Beat 1: 0.00 - 1.74
        # Fade out previous scene's dimmed downstream boxes / caption.
        # ------------------------------------------------------------
        self.play(
            FadeOut(old_boxes),
            FadeOut(old_caption),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.74))
        self.wait(max(0.05, 0.78))  # gap to 2.52

        # ------------------------------------------------------------
        # Beat 2: 2.52 - 4.74
        # Entire chain framed; caption above; thick arrows appear.
        # ------------------------------------------------------------
        integrated_caption = Text(
            "The acquisition chain is an integrated system",
            font_size=32,
            color=YELLOW,
            weight="BOLD",
        )
        integrated_caption.scale_to_fit_width(12.0)
        integrated_caption.move_to(np.array([0.0, 3.2, 0.0]))

        self.play(Create(chain_arrows), run_time=max(0.05, 1.00))
        self.play(Write(integrated_caption), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.42))

        # gap to 5.16
        self.wait(max(0.05, 0.42))

        # ------------------------------------------------------------
        # Beat 3: 5.16 - 6.66
        # Pulse appears at Electrode, travels through first arrow.
        # ------------------------------------------------------------
        pulse = VGroup(
            Dot(radius=0.09, color=YELLOW, fill_opacity=1),
            Circle(
                radius=0.17,
                color=YELLOW,
                fill_opacity=0.25,
                stroke_width=1,
            ),
        )
        pulse.move_to(stage_boxes[0].get_center() + DOWN * 0.10)

        electrode_label = Text("Electrode", font_size=24, color=YELLOW, weight="BOLD")
        electrode_label.next_to(stage_groups[0], DOWN, buff=0.20)

        self.play(FadeIn(pulse), run_time=max(0.05, 0.30))
        self.play(Write(electrode_label), run_time=max(0.05, 0.40))
        self.play(
            pulse.animate.move_to(stage_boxes[1].get_left()),
            Indicate(stage_groups[0], scale_factor=1.06, color=YELLOW),
            run_time=max(0.05, 0.80),
        )

        # gap to 6.92
        self.wait(max(0.05, 0.26))

        # ------------------------------------------------------------
        # Beat 4: 6.92 - 8.44
        # Pulse enters Amplifier; first arrow stays illuminated.
        # ------------------------------------------------------------
        self.play(
            pulse.animate.move_to(stage_boxes[1].get_center()),
            Indicate(stage_groups[1], scale_factor=1.06, color=YELLOW),
            run_time=max(0.05, 0.70),
        )
        self.play(
            pulse.animate.move_to(stage_boxes[1].get_right()),
            run_time=max(0.05, 0.50),
        )
        self.play(
            Indicate(chain_arrows[0], color=GOLD, scale_factor=1.10),
            run_time=max(0.05, 0.32),
        )

        # gap to 8.80
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------
        # Beat 5: 8.80 - 10.94
        # Pulse passes through ADC, then enters Computer.
        # ------------------------------------------------------------
        self.play(FadeOut(electrode_label), run_time=max(0.05, 0.30))

        adc_label = Text("sampled signal", font_size=22, color=GREEN, weight="BOLD")
        adc_label.next_to(stage_groups[2], DOWN, buff=0.20)

        self.play(
            pulse.animate.move_to(stage_boxes[2].get_center()),
            Write(adc_label),
            Indicate(stage_groups[2], scale_factor=1.06, color=GREEN),
            run_time=max(0.05, 0.90),
        )
        self.play(
            pulse.animate.move_to(stage_boxes[3].get_left()),
            run_time=max(0.05, 0.94),
        )

        # gap to 11.68
        self.wait(max(0.05, 0.74))

        # ------------------------------------------------------------
        # Beat 6: 11.68 - 13.46
        # Electrode shakes; poor electrode contact label and spark appear.
        # ------------------------------------------------------------
        self.play(FadeOut(adc_label), run_time=max(0.05, 0.20))

        spark_icon = make_spark()
        spark_icon.move_to(stage_boxes[0].get_top() + UP * 0.15 + RIGHT * 0.25)

        poor_label = Text(
            "poor electrode contact",
            font_size=20,
            color=RED,
            weight="BOLD",
        )
        poor_label.next_to(stage_groups[0], DOWN, buff=0.30)

        self.play(FadeIn(spark_icon), Write(poor_label), run_time=max(0.05, 0.50))

        for _ in range(4):
            self.play(
                stage_groups[0].animate.shift(UP * 0.07),
                run_time=max(0.05, 0.10),
            )
            self.play(
                stage_groups[0].animate.shift(DOWN * 0.07),
                run_time=max(0.05, 0.10),
            )

        self.wait(max(0.05, 0.28))

        # gap to 13.76
        self.wait(max(0.05, 0.30))

        # ------------------------------------------------------------
        # Beat 7: 13.76 - 15.30
        # Amplifier grows larger; glitches propagate.
        # ------------------------------------------------------------
        self.play(FadeOut(spark_icon), FadeOut(poor_label), run_time=max(0.05, 0.25))

        better_amp_label = Text(
            "better amplifier",
            font_size=18,
            color=YELLOW,
            weight="BOLD",
        )
        better_amp_label.next_to(stage_groups[1], DOWN, buff=0.22)

        glitch_in_amp = make_jagged_path(
            width=0.95, height=0.35, color=RED, n_points=14
        )
        glitch_in_amp.move_to(stage_boxes[1].get_center() + DOWN * 0.12)

        glitch_pulse = make_jagged_path(
            width=0.50, height=0.26, color=RED, n_points=10
        )
        glitch_pulse.move_to(stage_boxes[1].get_right())

        self.play(
            stage_groups[1].animate.scale(1.15),
            Write(better_amp_label),
            run_time=max(0.05, 0.50),
        )
        self.play(
            FadeIn(glitch_in_amp),
            FadeIn(glitch_pulse),
            run_time=max(0.05, 0.25),
        )
        self.play(
            glitch_pulse.animate.move_to(stage_boxes[2].get_center()),
            run_time=max(0.05, 0.30),
        )
        self.play(
            glitch_pulse.animate.move_to(stage_boxes[3].get_left()),
            run_time=max(0.05, 0.24),
        )

        # gap to 16.30
        self.wait(max(0.05, 1.00))

        # ------------------------------------------------------------
        # Beat 8: 16.30 - 18.80
        # Reset to clean chain; ADC shows irregular sampling intervals.
        # ------------------------------------------------------------
        self.play(
            FadeOut(glitch_in_amp),
            FadeOut(glitch_pulse),
            FadeOut(better_amp_label),
            run_time=max(0.05, 0.40),
        )
        self.play(
            stage_groups[1].animate.scale(1 / 1.15),
            run_time=max(0.05, 0.40),
        )

        adc_warning_rect = SurroundingRectangle(
            stage_groups[2],
            color=RED,
            buff=0.12,
            stroke_width=4,
            corner_radius=0.10,
        )

        self.play(
            FadeOut(adc_even_lines),
            FadeIn(adc_irregular_lines),
            FadeIn(adc_warning_rect),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.70))

        # gap to 19.10
        self.wait(max(0.05, 0.30))

        # ------------------------------------------------------------
        # Beat 9: 19.10 - 20.30
        # Computer shows distorted waveform; red X; downstream glitches.
        # ------------------------------------------------------------
        distorted_wave = make_jagged_path(
            width=0.72, height=0.30, color=RED, n_points=14
        )
        distorted_wave.move_to(computer_screen.get_center())

        red_x_computer = make_red_x(size=0.55)
        red_x_computer.move_to(stage_boxes[3].get_top() + UP * 0.10 + RIGHT * 0.15)

        distorted_label = Text(
            "distorted waveform",
            font_size=20,
            color=RED,
            weight="BOLD",
        )
        distorted_label.next_to(stage_groups[3], DOWN, buff=0.22)

        ds_glitch1 = make_jagged_path(width=0.60, height=0.24, color=RED, n_points=10)
        ds_glitch1.move_to(stage_boxes[4].get_center() + DOWN * 0.08)

        ds_glitch2 = make_jagged_path(width=0.60, height=0.24, color=RED, n_points=10)
        ds_glitch2.move_to(stage_boxes[5].get_center() + DOWN * 0.08)

        self.play(
            FadeIn(distorted_wave),
            FadeIn(red_x_computer),
            Write(distorted_label),
            run_time=max(0.05, 0.50),
        )
        self.play(
            FadeIn(ds_glitch1),
            FadeIn(ds_glitch2),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.20))

        # gap to 21.26
        self.wait(max(0.05, 0.96))

        # ------------------------------------------------------------
        # Beat 10: 21.26 - 23.60
        # Hold corrupted Computer; downstream labels/red X; caption.
        # ------------------------------------------------------------
        good_processing_label = Text(
            "good processing",
            font_size=16,
            color=GREEN,
            weight="BOLD",
        )
        good_processing_label.next_to(stage_groups[4], UP, buff=0.12)

        careful_analysis_label = Text(
            "careful analysis",
            font_size=16,
            color=GREEN,
            weight="BOLD",
        )
        careful_analysis_label.next_to(stage_groups[5], UP, buff=0.12)

        red_x_ds4 = make_red_x(size=0.40)
        red_x_ds4.move_to(stage_boxes[4].get_top() + UP * 0.08)

        red_x_ds5 = make_red_x(size=0.40)
        red_x_ds5.move_to(stage_boxes[5].get_top() + UP * 0.08)

        failure_caption = Text(
            "You can't fix a bad acquisition with good processing.",
            font_size=24,
            color=YELLOW,
            weight="BOLD",
        )
        failure_caption.scale_to_fit_width(11.0)
        failure_caption.move_to(np.array([0.0, -2.80, 0.0]))

        self.play(
            FadeIn(good_processing_label),
            FadeIn(careful_analysis_label),
            FadeIn(red_x_ds4),
            FadeIn(red_x_ds5),
            run_time=max(0.05, 0.60),
        )
        self.play(Write(failure_caption), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.94))

        # ------------------------------------------------------------
        # Beat 11: 23.60 - 26.92
        # Transition to clean correct chain; green check; careful caption.
        # ------------------------------------------------------------
        fade_outs = [
            adc_irregular_lines,
            adc_warning_rect,
            red_x_computer,
            red_x_ds4,
            red_x_ds5,
            distorted_wave,
            distorted_label,
            ds_glitch1,
            ds_glitch2,
            good_processing_label,
            careful_analysis_label,
            failure_caption,
        ]
        self.play(
            *[FadeOut(m) for m in fade_outs],
            run_time=max(0.05, 1.00),
        )
        self.play(FadeIn(adc_even_lines), run_time=max(0.05, 0.50))

        green_check = SVGMobject(
            ASSET_PATHS["check_circle"],
            height=0.70,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=0,
        )
        green_check.move_to(np.array([0.0, 2.30, 0.0]))

        careful_caption = Text(
            "Careful acquisition comes first",
            font_size=30,
            color=GREEN,
            weight="BOLD",
        )
        careful_caption.scale_to_fit_width(10.0)
        careful_caption.next_to(chain, DOWN, buff=0.80)

        self.play(
            FadeIn(green_check),
            Write(careful_caption),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------
        # Beat 12: 26.92 - 29.04
        # Caption brightens slightly; green check pulses once.
        # ------------------------------------------------------------
        self.play(
            careful_caption.animate.set_color(YELLOW),
            run_time=max(0.05, 0.60),
        )
        self.play(
            green_check.animate.scale(1.20),
            run_time=max(0.05, 0.40),
        )
        self.play(
            green_check.animate.scale(1 / 1.20),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.72))

        # ------------------------------------------------------------
        # Beat 13: 29.04 - 29.95
        # Final hold.
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.91))