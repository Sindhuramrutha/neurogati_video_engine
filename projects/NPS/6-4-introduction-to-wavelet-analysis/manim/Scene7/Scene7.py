ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Soft background tint used only at the very end
        bg_tint = Rectangle(
            width=16, height=10,
            fill_color=BLUE, fill_opacity=0,
            stroke_width=0
        ).set_z_index(-5)
        self.add(bg_tint)

        # ------------------------------------------------------------
        # Drawing helpers
        # ------------------------------------------------------------
        def make_signal(x_left, x_right, center_y, color=WHITE,
                        stroke_width=2.5, mode="init"):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                if mode == "drift":
                    freq = 1.5 + 3.5 * t
                    amp = 0.18 + 0.18 * t
                    y = center_y + amp * np.sin(2 * np.pi * freq * t)
                    for pos, mag in [(0.28, 0.45), (0.52, 0.38), (0.78, 0.50)]:
                        y += mag * np.exp(-((t - pos) / 0.025) ** 2) * np.sin(2 * np.pi * 22 * t)
                elif mode == "eeg":
                    y = center_y + 0.22 * np.sin(2 * np.pi * 2.5 * t)
                    for pos, mag in [(0.24, 0.85), (0.72, 0.95)]:
                        y += mag * np.exp(-((t - pos) / 0.02) ** 2) * np.sin(2 * np.pi * 30 * t)
                elif mode == "continuous":
                    y = center_y + 0.22 * np.sin(2 * np.pi * 2.2 * t) + 0.10 * np.sin(2 * np.pi * 8 * t)
                else:  # init
                    y = center_y + 0.30 * np.sin(2 * np.pi * 2.0 * t)
                    y += 0.18 * np.sin(2 * np.pi * 6 * t + 1.0)
                    y += 0.90 * np.exp(-((t - 0.35) / 0.02) ** 2) * np.sin(2 * np.pi * 18 * t)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                f, t_range=[0, 1, 0.01],
                color=color, stroke_width=stroke_width
            )

        def make_wavelet(center_x, center_y, width=1.0, height=0.5,
                         color=WHITE, stroke_width=3, cycles=5):
            def f(t):
                x = center_x - width / 2 + width * t
                env = np.exp(-((t - 0.5) ** 2) / (2 * 0.18 ** 2))
                y = center_y + height * env * np.sin(2 * np.pi * cycles * (t - 0.5))
                return np.array([x, y, 0.0])

            return ParametricFunction(
                f, t_range=[0, 1, 0.01],
                color=color, stroke_width=stroke_width
            )

        def make_erp(x_event, y_center, color=WHITE, stroke_width=3):
            left = x_event - 1.4
            right = x_event + 1.4

            def f(t):
                x = left + (right - left) * t
                y = y_center + 0.60 * np.exp(-((t - 0.38) / 0.08) ** 2)
                y -= 0.45 * np.exp(-((t - 0.62) / 0.10) ** 2)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                f, t_range=[0, 1, 0.01],
                color=color, stroke_width=stroke_width
            )

        def make_visual_icon():
            frame = Rectangle(
                width=0.9, height=0.65,
                fill_color=BLUE, fill_opacity=1, stroke_width=0
            )
            sun = Dot(point=[0.20, 0.15, 0], radius=0.07, color=YELLOW)
            mountain = Polygon(
                [-0.20, -0.20, 0],
                [0.00, 0.20, 0],
                [0.20, -0.20, 0],
                fill_color=GREEN, fill_opacity=1, stroke_width=0
            )
            return VGroup(frame, sun, mountain)

        def make_audio_icon():
            body = Rectangle(
                width=0.30, height=0.50,
                fill_color=ORANGE, fill_opacity=1, stroke_width=0
            )
            cone = Polygon(
                [-0.15, -0.25, 0],
                [-0.15, 0.25, 0],
                [0.25, 0.45, 0],
                [0.25, -0.45, 0],
                fill_color=ORANGE, fill_opacity=1, stroke_width=0
            )
            return VGroup(body, cone)

        def make_button_icon():
            outer = Circle(
                radius=0.35, fill_color=RED, fill_opacity=1,
                stroke_width=0
            )
            inner = Circle(
                radius=0.10, fill_color=WHITE, fill_opacity=1,
                stroke_width=0
            )
            return VGroup(outer, inner)

        # ------------------------------------------------------------
        # Beat 1: 0.00-3.00
        # ------------------------------------------------------------
        main_left, main_right, main_y = -5.8, 5.8, 1.0

        signal_main = make_signal(main_left, main_right, main_y,
                                  color=WHITE, stroke_width=2.8, mode="init")
        narrow_wavelet = make_wavelet(-1.75, main_y, width=0.65, height=0.5,
                                      color=ORANGE, stroke_width=3, cycles=5)
        wide_wavelet = make_wavelet(3.20, main_y, width=1.9, height=0.5,
                                    color=GREEN, stroke_width=3, cycles=3)

        wave_group = VGroup(signal_main, narrow_wavelet, wide_wavelet)

        top_text = Text("Adaptive time–frequency analysis",
                        font_size=32, color=WHITE, weight="BOLD")
        top_text.move_to([0, 3.0, 0])
        bottom_text = Text("Multi-resolution",
                           font_size=28, color=YELLOW)
        bottom_text.move_to([0, -2.3, 0])

        self.play(FadeIn(signal_main), run_time=max(0.05, 1.2))
        self.play(Create(narrow_wavelet), FadeIn(wide_wavelet), run_time=max(0.05, 0.9))
        self.play(Write(top_text), Write(bottom_text), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.3))

        # gap 3.00 -> 3.78
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------
        # Beat 2: 3.78-7.10
        # ------------------------------------------------------------
        self.play(top_text.animate.set_opacity(0.5),
                  bottom_text.animate.set_opacity(0.5),
                  run_time=max(0.05, 0.4))

        narrow2 = make_wavelet(-1.75, main_y, width=0.50, height=0.55,
                               color=ORANGE, stroke_width=3.5, cycles=6)
        wide2 = make_wavelet(3.25, main_y, width=2.3, height=0.55,
                             color=GREEN, stroke_width=3.5, cycles=3)

        self.play(signal_main.animate.set_color(TEAL),
                  Transform(narrow_wavelet, narrow2),
                  Transform(wide_wavelet, wide2),
                  run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.92))

        # gap 7.10 -> 7.88
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------
        # Beat 3: 7.88-11.10
        # ------------------------------------------------------------
        fixed_text = Text("fixed-window", font_size=30,
                          color=RED, weight="BOLD")
        fixed_text.move_to([-4.5, 2.4, 0])

        rigid_rect = Rectangle(width=2.0, height=1.5,
                               color=RED, stroke_width=4)
        rigid_rect.move_to([1.5, main_y, 0])

        stft_caption = Text("Short-Time Fourier Transform",
                            font_size=22, color=YELLOW)
        stft_caption.to_corner(DL, buff=0.4)

        self.play(FadeIn(fixed_text), run_time=max(0.05, 0.5))
        self.play(Indicate(fixed_text, color=YELLOW), run_time=max(0.05, 0.6))
        self.play(Create(rigid_rect), run_time=max(0.05, 0.6))

        self.play(FadeOut(rigid_rect),
                  narrow_wavelet.animate.scale(0.8),
                  wide_wavelet.animate.scale(1.2),
                  run_time=max(0.05, 0.8))
        self.play(FadeIn(stft_caption), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.12))

        # gap 11.10 -> 12.14
        self.wait(max(0.05, 1.04))

        # ------------------------------------------------------------
        # Beat 4: 12.14-15.98
        # ------------------------------------------------------------
        new_top = Text("Wavelet Analysis examines signals at multiple scales",
                       font_size=28, color=WHITE, weight="BOLD")
        new_top.move_to([0, 3.0, 0])

        self.play(FadeOut(top_text),
                  FadeOut(bottom_text),
                  FadeOut(stft_caption),
                  FadeOut(fixed_text),
                  Write(new_top),
                  run_time=max(0.05, 0.8))

        # narrow and wide wavelets gently pulse in turn
        self.play(narrow_wavelet.animate.scale(1.15), run_time=max(0.05, 0.5))
        self.play(narrow_wavelet.animate.scale(1 / 1.15), run_time=max(0.05, 0.5))
        self.play(wide_wavelet.animate.scale(1.15), run_time=max(0.05, 0.5))
        self.play(wide_wavelet.animate.scale(1 / 1.15), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.04))

        # gap 15.98 -> 16.58
        self.wait(max(0.05, 0.60))

        # ------------------------------------------------------------
        # Beat 5: 16.58-22.56
        # ------------------------------------------------------------
        line1 = Text("Good time resolution for rapid events",
                     font_size=24, color=WHITE)
        line2 = Text("Good frequency resolution for slower oscillations",
                     font_size=24, color=WHITE)
        subtitle = VGroup(line1, line2).arrange(DOWN, buff=0.25)
        subtitle.move_to([0, -2.7, 0])

        self.play(FadeIn(line1), run_time=max(0.05, 0.8))
        self.play(Indicate(narrow_wavelet, color=YELLOW), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.8))
        self.play(FadeIn(line2), run_time=max(0.05, 0.8))
        self.play(Indicate(wide_wavelet, color=YELLOW), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.6))
        self.play(FadeOut(subtitle), run_time=max(0.05, 0.98))

        # Beat 6 starts immediately at 22.56

        # ------------------------------------------------------------
        # Beat 6: 22.56-29.40
        # ------------------------------------------------------------
        signal_drift = make_signal(main_left, main_right, main_y,
                                   color=TEAL, stroke_width=2.8, mode="drift")
        narrow_drift = make_wavelet(-1.75, main_y, width=0.55, height=0.5,
                                    color=ORANGE, stroke_width=3, cycles=6)
        wide_drift = make_wavelet(2.80, main_y, width=2.5, height=0.55,
                                  color=GREEN, stroke_width=3, cycles=3)

        adapt_label = Text("Adaptability", font_size=40,
                           color=YELLOW, weight="BOLD")
        adapt_label.move_to([0, 3.1, 0])

        self.play(FadeOut(new_top), FadeIn(adapt_label), run_time=max(0.05, 0.5))
        self.play(Transform(signal_main, signal_drift),
                  Transform(narrow_wavelet, narrow_drift),
                  Transform(wide_wavelet, wide_drift),
                  run_time=max(0.05, 2.5))

        for _ in range(2):
            self.play(adapt_label.animate.set_color(YELLOW), run_time=max(0.05, 0.5))
            self.play(adapt_label.animate.set_color(WHITE), run_time=max(0.05, 0.5))
        self.play(adapt_label.animate.set_color(YELLOW), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.34))

        # ------------------------------------------------------------
        # Beat 7: 29.40-33.38
        # ------------------------------------------------------------
        eeg_signal = make_signal(-4.8, 4.8, -1.2, color=GREEN,
                                 stroke_width=2.5, mode="eeg")
        burst_xs = [-2.5, 2.1]
        eeg_markers = VGroup(*[
            DashedLine(start=[x, -0.4, 0], end=[x, -2.0, 0],
                       color=YELLOW, stroke_width=2, dash_length=0.05)
            for x in burst_xs
        ])

        eeg_label = Text("EEG recording", font_size=23, color=GREEN)
        eeg_label.next_to(eeg_signal, DOWN, buff=0.3)

        eeg_narrow = make_wavelet(-2.5, -1.2, width=0.6, height=0.5,
                                  color=ORANGE, stroke_width=3, cycles=6)
        eeg_wide = make_wavelet(0.5, -1.2, width=1.8, height=0.5,
                                color=GREEN, stroke_width=3, cycles=3)

        self.play(FadeIn(eeg_signal), FadeIn(eeg_markers), run_time=max(0.05, 0.8))
        self.play(Transform(narrow_wavelet, eeg_narrow),
                  Transform(wide_wavelet, eeg_wide),
                  FadeIn(eeg_label),
                  run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.98))

        wave_group.add(eeg_signal, eeg_markers)

        # gap 33.38 -> 34.10
        self.wait(max(0.05, 0.72))

        # ------------------------------------------------------------
        # Beat 8: 34.10-40.98
        # ------------------------------------------------------------
        summary_text = Text(
            "We have focused on analyzing how neural activity\n"
            "changes over time and across different frequencies",
            font_size=24, color=WHITE, line_spacing=0.6
        )
        summary_text.move_to([0, -2.9, 0])

        self.play(wave_group.animate.set_opacity(0.55),
                  FadeOut(eeg_label),
                  adapt_label.animate.set_opacity(0.35),
                  run_time=max(0.05, 0.8))
        self.play(Write(summary_text), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 4.58))

        # gap 40.98 -> 41.68
        self.wait(max(0.05, 0.70))

        # ------------------------------------------------------------
        # Beat 9: 41.68-50.90
        # ------------------------------------------------------------
        self.play(FadeOut(wave_group),
                  FadeOut(adapt_label),
                  FadeOut(summary_text),
                  run_time=max(0.05, 0.7))

        tl_line = Line(np.array([-5.8, -0.5, 0]),
                       np.array([5.8, -0.5, 0]),
                       color=GREY_B, stroke_width=4)
        self.play(FadeIn(tl_line), run_time=max(0.05, 0.6))

        event_visuals = VGroup(tl_line)
        event_markers = []
        response_waves = []

        event_data = [
            (-4.0, make_visual_icon(), "Visual image", BLUE),
            (0.0, make_audio_icon(), "Auditory tone", ORANGE),
            (4.0, make_button_icon(), "Button press", RED),
        ]

        for x, icon, name, col in event_data:
            marker = Dot(point=[x, -0.5, 0], radius=0.1, color=col)
            icon.scale(0.7).move_to([x, -0.05, 0])
            label = Text(name, font_size=22, color=WHITE)
            label.move_to([x, -1.2, 0])
            resp = make_erp(x, 1.4, color=col, stroke_width=3)

            self.play(GrowFromCenter(marker),
                      FadeIn(icon),
                      Write(label),
                      run_time=max(0.05, 0.7))
            self.play(Create(resp), run_time=max(0.05, 0.8))
            self.play(Indicate(marker, color=YELLOW), run_time=max(0.05, 0.7))
            self.wait(max(0.05, 0.4))

            event_visuals.add(marker, icon, label, resp)
            event_markers.append(marker)
            response_waves.append(resp)

        self.wait(max(0.05, 0.12))

        # gap 50.90 -> 50.94
        self.wait(max(0.05, 0.04))

        # ------------------------------------------------------------
        # Beat 10: 50.94-58.86
        # ------------------------------------------------------------
        continuous_wave = make_signal(-5.8, 5.8, 2.7, color=TEAL,
                                      stroke_width=2.2, mode="continuous")
        beat10_text = Text("Measuring the brain's response to events",
                           font_size=28, color=GOLD, weight="BOLD")
        beat10_text.move_to([0, -2.7, 0])

        marker_group = VGroup(*event_markers)

        self.play(FadeIn(continuous_wave), run_time=max(0.05, 0.9))
        self.play(continuous_wave.animate.set_opacity(0.35), run_time=max(0.05, 0.6))
        self.play(Write(beat10_text), run_time=max(0.05, 0.8))

        self.play(*[resp.animate.set_stroke(width=5, opacity=1)
                    for resp in response_waves],
                  run_time=max(0.05, 0.8))

        self.play(marker_group.animate.scale(1.3), run_time=max(0.05, 0.3))
        self.play(marker_group.animate.scale(1 / 1.3), run_time=max(0.05, 0.3))

        self.wait(max(0.05, 2.0))
        self.play(continuous_wave.animate.set_opacity(0.25), run_time=max(0.05, 2.22))

        # gap 58.86 -> 59.76
        self.wait(max(0.05, 0.90))

        # ------------------------------------------------------------
        # Beat 11: 59.76-65.44
        # ------------------------------------------------------------
        self.play(FadeOut(event_visuals),
                  FadeOut(continuous_wave),
                  FadeOut(beat10_text),
                  run_time=max(0.05, 0.8))

        erp_title = Text("Event-Related Potential", font_size=56,
                         color=WHITE, weight="BOLD")
        erp_title.move_to([0, 0.6, 0])
        erp_acronym = Text("ERP", font_size=44,
                           color=YELLOW, weight="BOLD")
        erp_acronym.move_to([0, -0.7, 0])

        self.play(Write(erp_title), run_time=max(0.05, 1.0))
        self.play(Write(erp_acronym), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 3.18))

        # gap 65.44 -> 65.88
        self.wait(max(0.05, 0.44))

        # ------------------------------------------------------------
        # Beat 12: 65.88-68.47
        # ------------------------------------------------------------
        next_label = Text("Next section: Event-Related Potentials (ERP)",
                          font_size=28, color=YELLOW, weight="BOLD")
        next_label.next_to(erp_acronym, DOWN, buff=0.5)

        self.play(FadeIn(next_label), run_time=max(0.05, 0.7))
        self.play(bg_tint.animate.set_fill(opacity=0.22), run_time=max(0.05, 1.89))