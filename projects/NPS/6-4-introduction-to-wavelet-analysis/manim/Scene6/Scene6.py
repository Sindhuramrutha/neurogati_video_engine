ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------------------------------------------------------------
        # Wave helpers
        # ---------------------------------------------------------------
        def wavelet_shape(center_x, center_y, width=1.0, height=0.4,
                          color=WHITE, stroke_width=3, cycles=5):
            """Damped-sinusoidal wavelet shape centered at center_x, center_y."""

            def f(t):
                x = center_x - width / 2 + width * t
                env = np.exp(-((t - 0.5) ** 2) / (2 * 0.18 ** 2))
                y = center_y + height * env * np.sin(2 * np.pi * cycles * (t - 0.5))
                return np.array([x, y, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.02],
                                      color=color, stroke_width=stroke_width)

        def changing_signal(x_left, x_right, center_y, color=WHITE,
                            stroke_width=2.5, phase=0.0):
            """Nonstationary-ish signal with shifting frequency and amplitude."""
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                freq = 1.8 + 1.5 * np.sin(phase + 2.5 * t)
                amp = 0.25 + 0.12 * np.sin(phase + 5.0 * t)
                y = center_y + amp * np.sin(2 * np.pi * freq * t)
                return np.array([x, y, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.03],
                                      color=color, stroke_width=stroke_width)

        def transient_signal(x_left, x_right, center_y, color=WHITE,
                             stroke_width=2.5):
            """Slow baseline + sharp brief transient spike."""
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                base = 0.15 * np.sin(2 * np.pi * 1.0 * t)
                spike = 1.5 * np.exp(-(((t - 0.5) / 0.015) ** 2)) * np.sin(2 * np.pi * 18 * t)
                return np.array([x, center_y + base + spike, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.01],
                                      color=color, stroke_width=stroke_width)

        def slow_signal(x_left, x_right, center_y, color=WHITE,
                        stroke_width=2.5):
            """Slow, gentle oscillation with many cycles visible."""
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                y = center_y + 0.35 * np.sin(2 * np.pi * 2.0 * t)
                return np.array([x, y, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.03],
                                      color=color, stroke_width=stroke_width)

        # ---------------------------------------------------------------
        # Split-screen layout
        # ---------------------------------------------------------------
        left_panel = Rectangle(width=5.6, height=6.0,
                               fill_color=BLACK, fill_opacity=0.25,
                               stroke_color=GREY_B, stroke_width=2)
        left_panel.move_to([-3.2, 0.4, 0])

        right_panel = Rectangle(width=5.6, height=6.0,
                                fill_color=BLACK, fill_opacity=0.25,
                                stroke_color=GREY_B, stroke_width=2)
        right_panel.move_to([3.2, 0.4, 0])

        divider = Line([0, 3.5, 0], [0, -2.7, 0],
                       color=GREY, stroke_width=2)

        adv_heading = Text("Advantages", font_size=44, color=WHITE, weight="BOLD")
        adv_heading.move_to([-3.2, 3.3, 0])
        lim_heading = Text("Limitations", font_size=44, color=WHITE, weight="BOLD")
        lim_heading.move_to([3.2, 3.3, 0])

        adv_content = VGroup(left_panel, adv_heading)
        right_content = VGroup(right_panel, lim_heading)

        # ---------------------------------------------------------------
        # Beat 1: 0.00-2.92 -- split screen fades in; Advantages highlights
        # ---------------------------------------------------------------
        self.play(FadeIn(adv_content), FadeIn(right_content), FadeIn(divider),
                  run_time=max(0.05, 1.0))
        self.play(adv_heading.animate.set_color(YELLOW), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.32))

        # gap 2.92 -> 3.82
        self.wait(max(0.05, 0.90))

        # ---------------------------------------------------------------
        # Beat 2: 3.82-5.86 -- flexible arrow adapts to changing waveform
        # ---------------------------------------------------------------
        LX, LRX = -6.0, -1.0

        flex_signal_1 = changing_signal(LX, LRX, 1.8, color=TEAL,
                                        stroke_width=2.8, phase=0.0)
        flex_arrow_1 = Arrow(start=np.array([LX, 2.4, 0]),
                             end=np.array([LRX, 2.4, 0]),
                             path_arc=0.40, color=BLUE, stroke_width=5,
                             buff=0)

        flex_signal_2 = changing_signal(LX, LRX, 1.8, color=TEAL,
                                        stroke_width=2.8, phase=1.2)
        flex_arrow_2 = Arrow(start=np.array([LX, 2.4, 0]),
                             end=np.array([LRX, 2.4, 0]),
                             path_arc=-0.30, color=BLUE, stroke_width=5,
                             buff=0)

        flex_signal_3 = changing_signal(LX, LRX, 1.8, color=TEAL,
                                        stroke_width=2.8, phase=2.5)
        flex_arrow_3 = Arrow(start=np.array([LX, 2.4, 0]),
                             end=np.array([LRX, 2.4, 0]),
                             path_arc=0.65, color=BLUE, stroke_width=5,
                             buff=0)

        self.play(FadeIn(flex_arrow_1), FadeIn(flex_signal_1), run_time=max(0.05, 0.8))
        self.play(Transform(flex_arrow_1, flex_arrow_2),
                  Transform(flex_signal_1, flex_signal_2),
                  run_time=max(0.05, 0.6))
        self.play(Transform(flex_arrow_1, flex_arrow_3),
                  Transform(flex_signal_1, flex_signal_3),
                  run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.04))

        adv_content.add(flex_arrow_1, flex_signal_1)

        # gap 5.86 -> 6.48
        self.wait(max(0.05, 0.62))

        # ---------------------------------------------------------------
        # Beat 3: 6.48-8.90 -- narrow wavelet over fast transient
        # ---------------------------------------------------------------
        trans_sig = transient_signal(LX, LRX, 0.8, color=WHITE,
                                     stroke_width=2.5)
        narrow_wavelet = wavelet_shape(-3.5, 0.8, width=0.9, height=0.45,
                                       color=ORANGE, stroke_width=3.2,
                                       cycles=6)

        self.play(FadeIn(trans_sig), run_time=max(0.05, 0.7))
        self.play(Create(narrow_wavelet), run_time=max(0.05, 0.8))
        self.play(Indicate(narrow_wavelet, color=YELLOW), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 0.02))

        adv_content.add(trans_sig, narrow_wavelet)

        # gap 8.90 -> 9.56
        self.wait(max(0.05, 0.66))

        # ---------------------------------------------------------------
        # Beat 4: 9.56-12.84 -- wide wavelet over slow oscillation
        # ---------------------------------------------------------------
        slow_sig = slow_signal(LX, LRX, -0.4, color=WHITE,
                               stroke_width=2.5)
        wide_wavelet = wavelet_shape(-3.5, -0.4, width=2.4, height=0.45,
                                     color=GREEN, stroke_width=3.2,
                                     cycles=3)

        self.play(FadeIn(slow_sig), run_time=max(0.05, 0.7))
        self.play(Create(wide_wavelet), run_time=max(0.05, 1.0))
        self.play(Indicate(wide_wavelet, color=YELLOW), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.08))

        adv_content.add(slow_sig, wide_wavelet)

        # gap 12.84 -> 13.24
        self.wait(max(0.05, 0.40))

        # ---------------------------------------------------------------
        # Beat 5: 13.24-16.74 -- nonstationary waveform + checkmark
        # ---------------------------------------------------------------
        ns_adv = changing_signal(LX, -1.6, -1.6, color=WHITE,
                                 stroke_width=2.5, phase=0.7)
        check = SVGMobject(ASSET_PATHS["check_circle"], height=0.6,
                           color=GREEN, fill_color=GREEN,
                           fill_opacity=1)
        check.next_to(ns_adv, RIGHT, buff=0.2)

        self.play(FadeIn(ns_adv), FadeIn(check), run_time=max(0.05, 0.8))
        self.play(Indicate(check, color=GREEN), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.7))

        adv_content.add(ns_adv, check)

        # gap 16.74 -> 17.62
        self.wait(max(0.05, 0.88))

        # ---------------------------------------------------------------
        # Beat 6: 17.62-20.52 -- Advantages dims, Limitations brightens
        # ---------------------------------------------------------------
        self.play(adv_content.animate.set_opacity(0.55),
                  lim_heading.animate.set_color(YELLOW),
                  right_panel.animate.set_stroke(YELLOW, width=3),
                  run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.90))

        # gap 20.52 -> 21.56
        self.wait(max(0.05, 1.04))

        # ---------------------------------------------------------------
        # Beat 7: 21.56-23.94 -- limitation 1: mother wavelet choice
        # ---------------------------------------------------------------
        lim1_wavelet = wavelet_shape(2.0, 2.0, width=1.4, height=0.45,
                                     color=PURPLE, stroke_width=3.2,
                                     cycles=5)
        lim1_qmark = Text("?", font_size=60, color=YELLOW, weight="BOLD")
        lim1_qmark.move_to([2.0, 2.65, 0])

        lim1_text = Text("mother wavelet choice\ndepends on application",
                         font_size=18, color=WHITE, line_spacing=0.4)
        lim1_text.move_to([2.0, 0.8, 0])

        self.play(FadeIn(lim1_wavelet), FadeIn(lim1_qmark), run_time=max(0.05, 0.8))
        self.play(Write(lim1_text), run_time=max(0.05, 0.8))
        self.play(Indicate(lim1_qmark, color=YELLOW), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.08))

        right_content.add(lim1_wavelet, lim1_qmark, lim1_text)

        # gap 23.94 -> 24.20
        self.wait(max(0.05, 0.26))

        # ---------------------------------------------------------------
        # Beat 8: 24.20-26.92 -- row of different wavelets pulse
        # ---------------------------------------------------------------
        row_wavelets = [
            wavelet_shape(4.3, 2.0, width=0.6, height=0.25,
                          color=TEAL, stroke_width=2.2, cycles=4),
            wavelet_shape(4.8, 2.0, width=0.9, height=0.35,
                          color=ORANGE, stroke_width=2.2, cycles=6),
            wavelet_shape(5.3, 2.0, width=1.2, height=0.25,
                          color=PINK, stroke_width=2.2, cycles=3),
        ]
        row_group = VGroup(*row_wavelets).arrange(RIGHT, buff=0.12)
        row_group.move_to([4.4, 2.0, 0])

        self.play(FadeIn(row_group), run_time=max(0.05, 0.8))
        for shape in row_group:
            self.play(Indicate(shape, color=YELLOW), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.72))

        right_content.add(row_group)

        # gap 26.92 -> 27.92
        self.wait(max(0.05, 1.00))

        # ---------------------------------------------------------------
        # Beat 9: 27.92-34.66 -- computational cost vs STFT
        # ---------------------------------------------------------------
        cpu_main = SVGMobject(ASSET_PATHS["cpu"], height=0.9,
                              color=BLUE, fill_color=BLUE,
                              fill_opacity=1)
        cpu_main.move_to([1.8, -0.3, 0])

        gear_left = SVGMobject(ASSET_PATHS["gear"], height=0.4,
                               color=YELLOW, fill_color=YELLOW,
                               fill_opacity=1)
        gear_left.next_to(cpu_main, LEFT, buff=0.1)

        gear_right = SVGMobject(ASSET_PATHS["gear"], height=0.4,
                                color=YELLOW, fill_color=YELLOW,
                                fill_opacity=1)
        gear_right.next_to(cpu_main, RIGHT, buff=0.1)

        limit2_text = Text("more computationally\ndemanding",
                           font_size=18, color=WHITE, line_spacing=0.4)
        limit2_text.move_to([1.8, -1.35, 0])

        cpu_small = SVGMobject(ASSET_PATHS["cpu"], height=0.45,
                               color=GREY, fill_color=GREY,
                               fill_opacity=1)
        stft_text = Text("Short-Time\nFourier Transform",
                         font_size=16, color=WHITE, line_spacing=0.4)
        stft_group = VGroup(cpu_small, stft_text).arrange(RIGHT, buff=0.15)
        stft_group.move_to([4.5, -0.3, 0])
        stft_group.set_opacity(0.75)

        self.play(FadeIn(cpu_main), FadeIn(limit2_text), run_time=max(0.05, 0.9))
        self.play(FadeIn(gear_left), FadeIn(gear_right), run_time=max(0.05, 0.5))
        self.play(FadeIn(stft_group), run_time=max(0.05, 0.8))

        # moving gears -- three short loops
        for _ in range(3):
            self.play(gear_left.animate.rotate(PI / 2),
                      gear_right.animate.rotate(-PI / 2),
                      run_time=max(0.05, 0.6))
            self.play(gear_left.animate.rotate(PI / 2),
                      gear_right.animate.rotate(-PI / 2),
                      run_time=max(0.05, 0.6))

        self.play(Indicate(cpu_main, color=YELLOW), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.24))

        right_content.add(cpu_main, gear_left, gear_right,
                          limit2_text, stft_group)

        # gap 34.66 -> 35.64
        self.wait(max(0.05, 0.98))

        # ---------------------------------------------------------------
        # Beat 10: 35.64-43.60 -- final merge, central wavelet, bottom text
        # ---------------------------------------------------------------
        central_wavelet = wavelet_shape(0.0, 0.2, width=0.7, height=0.4,
                                        color=YELLOW, stroke_width=3.5,
                                        cycles=5)

        bottom_text = Text("understand both signal and objectives",
                           font_size=26, color=YELLOW, weight="BOLD")
        bottom_text.to_edge(DOWN, buff=0.45)

        self.play(adv_content.animate.set_opacity(1),
                  right_content.animate.set_opacity(1),
                  run_time=max(0.05, 0.9))

        self.play(adv_content.animate.shift(RIGHT * 0.25),
                  right_content.animate.shift(LEFT * 0.25),
                  FadeOut(divider),
                  run_time=max(0.05, 1.2))

        self.play(SpinInFromNothing(central_wavelet, angle=PI / 2),
                  run_time=max(0.05, 0.8))

        self.play(Write(bottom_text), run_time=max(0.05, 0.8))

        self.wait(max(0.05, 4.26))