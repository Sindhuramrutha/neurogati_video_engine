ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Constants for the analog waveform and sampling
        # ------------------------------------------------------------
        SHIFT_LEFT = 0.7
        INITIAL_SAMPLE_XS = np.array([-4.8, -3.9, -3.0, -2.1, -1.2, -0.3])
        FINAL_SAMPLE_XS = INITIAL_SAMPLE_XS - SHIFT_LEFT
        SAMPLE_VALUES = [0.2, 0.5, 0.8, 0.6, 0.9, 0.4]
        AXIS_Y = -1.4
        VALUE_SCALE = 2.0

        initial_sample_points = [
            np.array([x, AXIS_Y + VALUE_SCALE * v, 0.0])
            for x, v in zip(INITIAL_SAMPLE_XS, SAMPLE_VALUES)
        ]

        # ------------------------------------------------------------
        # Catmull-Rom interpolation to draw a smooth continuous curve
        # ------------------------------------------------------------
        def catmull_rom(points, n_per_seg=90):
            pts = []
            p = [np.array(pt, dtype=float) for pt in points]
            for i in range(len(p) - 1):
                p0 = p[max(i - 1, 0)]
                p1 = p[i]
                p2 = p[i + 1]
                p3 = p[min(i + 2, len(p) - 1)]
                for j in range(n_per_seg):
                    t = j / n_per_seg
                    t2 = t * t
                    t3 = t2 * t
                    pt = 0.5 * (
                        (2.0 * p1)
                        + (-p0 + p2) * t
                        + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2
                        + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3
                    )
                    pts.append(pt)
            pts.append(p[-1])
            return pts

        # ------------------------------------------------------------
        # Previous scene leftovers: filter box and frequency panels
        # ------------------------------------------------------------
        def make_prev_spectrum(center, include_red=True):
            axis = Line(
                start=center + LEFT * 2.8,
                end=center + RIGHT * 2.8,
                color=GREY_B,
                stroke_width=3,
            )
            bars = VGroup()
            low_xs = np.linspace(center[0] - 2.4, center[0] - 0.5, 6)
            heights = [0.45, 0.60, 0.50, 0.70, 0.45, 0.60]
            for x, h in zip(low_xs, heights):
                bar = Rectangle(
                    width=0.16,
                    height=h,
                    fill_color=GREEN,
                    fill_opacity=1,
                    stroke_width=0,
                )
                bar.move_to(np.array([x, center[1] + h / 2.0, 0.0]))
                bars.add(bar)

            if include_red:
                high_xs = np.linspace(center[0] + 0.5, center[0] + 2.4, 5)
                red_heights = [0.20, 0.28, 0.16, 0.24, 0.18]
                for x, h in zip(high_xs, red_heights):
                    bar = Rectangle(
                        width=0.12,
                        height=h,
                        fill_color=RED,
                        fill_opacity=1,
                        stroke_width=0,
                    )
                    bar.move_to(np.array([x, center[1] + h / 2.0, 0.0]))
                    bars.add(bar)

            return VGroup(axis, bars)

        prev_filter_box = Rectangle(
            width=2.6,
            height=1.7,
            stroke_color=BLUE,
            stroke_width=4,
            fill_color=BLUE,
            fill_opacity=0.15,
        )
        prev_filter_box.move_to(np.array([0.8, 1.2, 0.0]))
        prev_filter_label = Text("Filter", font_size=32, color=WHITE)
        prev_filter_label.move_to(prev_filter_box.get_center())

        spectrum1 = make_prev_spectrum(np.array([-0.3, -1.5, 0.0]), include_red=True)
        spectrum2 = make_prev_spectrum(np.array([-0.3, -3.0, 0.0]), include_red=False)
        before_label = Text("before filtering", font_size=20, color=GREY_B)
        before_label.next_to(spectrum1, LEFT, buff=0.55)
        after_label = Text("after filtering", font_size=20, color=GREY_B)
        after_label.next_to(spectrum2, LEFT, buff=0.55)

        previous_scene_group = VGroup(
            prev_filter_box,
            prev_filter_label,
            spectrum1,
            spectrum2,
            before_label,
            after_label,
        )
        self.add(previous_scene_group)

        # ------------------------------------------------------------
        # The analog waveform
        # ------------------------------------------------------------
        analog_wave_points = catmull_rom(initial_sample_points, n_per_seg=90)
        analog_wave = VMobject().set_points_as_corners(analog_wave_points)
        analog_wave.set_stroke(color=ORANGE, width=6)
        analog_wave.set_fill(opacity=0)

        axis_left = INITIAL_SAMPLE_XS[0] - 0.65
        axis_right = INITIAL_SAMPLE_XS[-1] + 0.65
        analog_axis = Line(
            start=np.array([axis_left, AXIS_Y, 0.0]),
            end=np.array([axis_right, AXIS_Y, 0.0]),
            color=GREY_B,
            stroke_width=3,
        )

        analog_label = Text("analog signal", font_size=28, color=YELLOW)
        analog_label.next_to(analog_wave, UP, buff=0.25)

        shifting_content = VGroup(analog_wave, analog_axis, analog_label)

        caption_cont = Text("continuous voltage", font_size=24, color=WHITE)
        caption_cont.next_to(analog_axis, DOWN, buff=0.30)

        subtitle_smooth = Text("varies smoothly in time", font_size=24, color=YELLOW)
        subtitle_smooth.next_to(caption_cont, DOWN, buff=0.18)

        # Captions are added later, but they must move with the waveform when it shifts left.
        shifting_content.add(caption_cont, subtitle_smooth)

        # ------------------------------------------------------------
        # Computer icon on the right
        # ------------------------------------------------------------
        monitor = Rectangle(
            width=1.15,
            height=0.85,
            stroke_color=BLUE,
            stroke_width=4,
            fill_color=BLUE,
            fill_opacity=0.25,
        )
        screen = Rectangle(
            width=0.90,
            height=0.60,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.90,
        )
        screen.move_to(monitor.get_center() + UP * 0.05)
        stand = Line(
            monitor.get_bottom(),
            monitor.get_bottom() + DOWN * 0.28,
            color=BLUE,
            stroke_width=4,
        )
        base = Line(
            stand.get_end() + LEFT * 0.22,
            stand.get_end() + RIGHT * 0.22,
            color=BLUE,
            stroke_width=4,
        )
        computer_icon = VGroup(monitor, screen, stand, base)
        computer_icon.move_to(np.array([5.6, 0.8, 0.0]))

        slash1 = Line(
            monitor.get_corner(UL),
            monitor.get_corner(DR),
            color=RED,
            stroke_width=5,
        )
        slash2 = Line(
            monitor.get_corner(UR),
            monitor.get_corner(DL),
            color=RED,
            stroke_width=5,
        )
        x_mark = VGroup(slash1, slash2)

        computer_label = Text("digital information", font_size=24, color=WHITE)
        computer_label.next_to(computer_icon, DOWN, buff=0.20)
        computer_group = VGroup(computer_icon, x_mark, computer_label)

        # ------------------------------------------------------------
        # ADC block
        # ------------------------------------------------------------
        adc_box = Rectangle(
            width=2.4,
            height=1.6,
            stroke_color=TEAL,
            stroke_width=4,
            fill_color=TEAL,
            fill_opacity=0.90,
        )
        adc_box.move_to(np.array([0.6, 0.4, 0.0]))
        adc_abbr = Text("ADC", font_size=40, color=YELLOW)
        adc_full = Text("Analog-to-Digital Converter", font_size=14, color=WHITE)
        adc_full.scale_to_fit_width(2.05)
        adc_text = VGroup(adc_abbr, adc_full).arrange(DOWN, buff=0.15)
        adc_text.move_to(adc_box.get_center())

        # ------------------------------------------------------------
        # Sampling gridlines and equal-gap arrows
        # ------------------------------------------------------------
        sample_gridlines = VGroup()
        for x, v in zip(FINAL_SAMPLE_XS, SAMPLE_VALUES):
            y_wave = AXIS_Y + VALUE_SCALE * v
            gridline = Line(
                start=np.array([x, AXIS_Y, 0.0]),
                end=np.array([x, y_wave + 0.35, 0.0]),
                color=BLUE,
                stroke_width=4,
            )
            sample_gridlines.add(gridline)

        gap_y = AXIS_Y - 0.55
        gap_arrows = VGroup()
        for i in range(len(FINAL_SAMPLE_XS) - 1):
            gap = DoubleArrow(
                start=np.array([FINAL_SAMPLE_XS[i], gap_y, 0.0]),
                end=np.array([FINAL_SAMPLE_XS[i + 1], gap_y, 0.0]),
                buff=0,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15,
            )
            gap_arrows.add(gap)

        # ------------------------------------------------------------
        # Sampling dots and numerical labels
        # ------------------------------------------------------------
        sample_dots = VGroup()
        sample_labels = VGroup()
        for x, v in zip(FINAL_SAMPLE_XS, SAMPLE_VALUES):
            y_wave = AXIS_Y + VALUE_SCALE * v
            dot = Dot(point=np.array([x, y_wave, 0.0]), radius=0.08, color=YELLOW)
            sample_dots.add(dot)
            label = Text(str(v), font_size=22, color=YELLOW)
            label.next_to(dot, UP, buff=0.16)
            sample_labels.add(label)

        # ------------------------------------------------------------
        # Digital staircase representation on the right
        # ------------------------------------------------------------
        DIG_XS = np.array([2.0, 2.6, 3.2, 3.8, 4.4, 5.0])
        stair_ys = AXIS_Y + VALUE_SCALE * np.array(SAMPLE_VALUES)

        stair_axis = Line(
            start=np.array([DIG_XS[0], AXIS_Y, 0.0]),
            end=np.array([DIG_XS[-1], AXIS_Y, 0.0]),
            color=GREY_B,
            stroke_width=3,
        )

        stair_pts = [np.array([DIG_XS[0], stair_ys[0], 0.0])]
        for i in range(len(DIG_XS) - 1):
            stair_pts.append(np.array([DIG_XS[i + 1], stair_ys[i], 0.0]))
            stair_pts.append(np.array([DIG_XS[i + 1], stair_ys[i + 1], 0.0]))

        stair_path = VMobject().set_points_as_corners(stair_pts)
        stair_path.set_stroke(color=GREEN, width=6)
        stair_path.set_fill(opacity=0)

        digital_label = Text("digital representation", font_size=24, color=GREEN)
        digital_label.next_to(stair_axis, DOWN, buff=0.25)

        # ------------------------------------------------------------
        # "a sequence of numbers" row beneath the analog samples
        # ------------------------------------------------------------
        sequence_caption = Text("a sequence of numbers", font_size=24, color=YELLOW)
        sequence_caption.move_to(
            np.array([np.mean(FINAL_SAMPLE_XS), AXIS_Y - 1.05, 0.0])
        )

        row_number_labels = VGroup()
        row_y = AXIS_Y - 1.50
        for x, v in zip(FINAL_SAMPLE_XS, SAMPLE_VALUES):
            number = Text(str(v), font_size=22, color=WHITE)
            number.move_to(np.array([x, row_y, 0.0]))
            row_number_labels.add(number)

        sweep_line = Line(
            start=np.array([DIG_XS[0], AXIS_Y - 0.5, 0.0]),
            end=np.array([DIG_XS[0], max(stair_ys) + 0.6, 0.0]),
            color=YELLOW,
            stroke_width=4,
        )

        # ============================================================
        # Beat 1: 0.00 - 1.00
        # Filter box and spectra fade away, analog signal appears.
        # ============================================================
        self.play(
            FadeOut(previous_scene_group),
            FadeIn(analog_wave),
            FadeIn(analog_axis),
            Write(analog_label),
            run_time=max(0.05, 1.00),
        )

        # Gap to 1.32
        self.wait(max(0.05, 0.32))

        # ============================================================
        # Beat 2: 1.32 - 3.20
        # Waveform pulses, "continuous voltage" appears.
        # ============================================================
        self.play(
            analog_wave.animate.set_stroke(color=WHITE, width=9),
            run_time=max(0.05, 0.35),
        )
        self.play(
            analog_wave.animate.set_stroke(color=ORANGE, width=6),
            Write(caption_cont),
            run_time=max(0.05, 1.53),
        )

        # Gap to 3.74
        self.wait(max(0.05, 0.54))

        # ============================================================
        # Beat 3: 3.74 - 6.46
        # Smoothness emphasized, "varies smoothly in time" appears.
        # ============================================================
        self.play(
            analog_wave.animate.set_stroke(color=YELLOW, width=9),
            run_time=max(0.05, 0.35),
        )
        self.play(
            analog_wave.animate.set_stroke(color=ORANGE, width=6),
            Write(subtitle_smooth),
            run_time=max(0.05, 2.37),
        )

        # Gap to 7.10
        self.wait(max(0.05, 0.64))

        # ============================================================
        # Beat 4: 7.10 - 9.44
        # Analog waveform shifts left, computer icon + X appears.
        # ============================================================
        self.play(
            shifting_content.animate.shift(LEFT * SHIFT_LEFT),
            run_time=max(0.05, 0.80),
        )
        self.play(
            FadeIn(computer_icon),
            Create(x_mark),
            Write(computer_label),
            run_time=max(0.05, 1.00),
        )
        self.play(
            analog_wave.animate.set_opacity(0.65),
            analog_axis.animate.set_opacity(0.65),
            run_time=max(0.05, 0.54),
        )

        # Gap to 10.34
        self.wait(max(0.05, 0.90))

        # ============================================================
        # Beat 5: 10.34 - 12.84
        # ADC block appears between analog wave and computer.
        # ============================================================
        self.play(
            FadeIn(adc_box),
            Write(adc_abbr),
            Write(adc_full),
            run_time=max(0.05, 2.50),
        )

        # Gap to 13.56
        self.wait(max(0.05, 0.72))

        # ============================================================
        # Beat 6: 13.56 - 16.28
        # Sampling gridlines appear, equal intervals highlighted.
        # ============================================================
        self.play(
            FadeOut(caption_cont),
            FadeOut(subtitle_smooth),
            run_time=max(0.05, 0.40),
        )
        self.play(
            LaggedStart(*[Create(gl) for gl in sample_gridlines], lag_ratio=0.12),
            LaggedStart(*[Create(ga) for ga in gap_arrows], lag_ratio=0.12),
            run_time=max(0.05, 1.40),
        )
        self.play(
            sample_gridlines.animate.set_stroke(color=YELLOW, width=7),
            gap_arrows.animate.set_stroke(color=WHITE, width=6),
            run_time=max(0.05, 0.35),
        )
        self.play(
            sample_gridlines.animate.set_stroke(color=BLUE, width=4),
            gap_arrows.animate.set_stroke(color=YELLOW, width=3),
            run_time=max(0.05, 0.57),
        )

        # Gap to 16.76
        self.wait(max(0.05, 0.48))

        # ============================================================
        # Beat 7: 16.76 - 19.50
        # Dots and numerical sample values appear.
        # ============================================================
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in sample_dots], lag_ratio=0.10),
            run_time=max(0.05, 1.20),
        )
        self.play(
            LaggedStart(*[Write(label) for label in sample_labels], lag_ratio=0.08),
            run_time=max(0.05, 1.54),
        )

        # Gap to 20.08
        self.wait(max(0.05, 0.58))

        # ============================================================
        # Beat 8: 20.08 - 24.06
        # Staircase digital representation appears on right.
        # ============================================================
        self.play(
            FadeOut(computer_group),
            FadeIn(stair_axis),
            run_time=max(0.05, 0.60),
        )
        self.play(
            Create(stair_path),
            run_time=max(0.05, 2.20),
        )
        self.play(
            Write(digital_label),
            run_time=max(0.05, 1.18),
        )

        # Gap to 24.54
        self.wait(max(0.05, 0.48))

        # ============================================================
        # Beat 9: 24.54 - 27.28
        # Show sequence of numbers, sweep highlight across staircase.
        # ============================================================
        self.play(
            FadeOut(gap_arrows),
            Write(sequence_caption),
            LaggedStart(*[Write(num) for num in row_number_labels], lag_ratio=0.08),
            run_time=max(0.05, 1.20),
        )

        self.add(sweep_line)
        self.play(
            sweep_line.animate.shift(RIGHT * (DIG_XS[-1] - DIG_XS[0])),
            run_time=max(0.05, 1.00),
        )
        self.play(
            FadeOut(sweep_line),
            run_time=max(0.05, 0.54),
        )

        # ============================================================
        # Beat 10: 27.28 - 27.95
        # Hold the complete final frame.
        # ============================================================
        self.wait(max(0.05, 0.67))