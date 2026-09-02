ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Signal / wavelet helpers -- same waveform as Scene 2.
        # ----------------------------------------------------------------
        SIGNAL_LEFT_X = -6.2
        SIGNAL_RIGHT_X = 5.8
        SIGNAL_CY = 0.0
        SIGNAL_AMP = 0.55
        SIGNAL_WIDTH = SIGNAL_RIGHT_X - SIGNAL_LEFT_X
        SLOW_T = 0.22
        SPIKE_T = 0.82
        slow_x = SIGNAL_LEFT_X + SIGNAL_WIDTH * SLOW_T
        spike_x = SIGNAL_LEFT_X + SIGNAL_WIDTH * SPIKE_T

        def signal_y(t):
            slow_env = 1 / (1 + np.exp((t - 0.55) * 15))
            slow = 0.85 * np.sin(2 * np.pi * 1.5 * t) * slow_env
            spike = 1.15 * np.exp(-(((t - 0.82) / 0.015) ** 2))
            return slow + spike

        def make_signal_waveform(x_left, x_right, center_y=SIGNAL_CY, amp=SIGNAL_AMP):
            width = x_right - x_left

            def func(t):
                x = x_left + width * t
                y = center_y + amp * signal_y(t)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                func,
                t_range=[0, 1, 0.002],
                color=WHITE,
                stroke_width=2.5,
            )

        def make_wavelet(center_x, center_y, x_scale=1.0, color=WHITE,
                         stroke_width=3.5, amp=0.65):
            base_half_extent = 1.05
            cycles = 2.8

            def func(t):
                x = center_x + t * x_scale * base_half_extent
                env = np.exp(-(t ** 2) / (2 * 0.34 ** 2))
                y = center_y + amp * env * np.sin(2 * np.pi * cycles * t)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                func,
                t_range=[-1, 1, 0.004],
                color=color,
                stroke_width=stroke_width,
            )

        def make_zoom_inset():
            inset_cx, inset_cy = 4.8, 1.6
            frame_w, frame_h = 3.2, 1.8
            frame = Rectangle(
                width=frame_w, height=frame_h,
                color=WHITE, stroke_width=2
            )
            frame.set_fill("#10141c", opacity=0.9)
            frame.move_to([inset_cx, inset_cy, 0])

            t0, t1 = 0.79, 0.86
            base_y = signal_y(SPIKE_T)

            def zoom_func(u):
                t = t0 + (t1 - t0) * u
                x = inset_cx - frame_w / 2 + frame_w * u
                y = inset_cy + (signal_y(t) - base_y) * 0.7
                return np.array([x, y, 0.0])

            zoom_wave = ParametricFunction(
                zoom_func,
                t_range=[0, 1, 0.002],
                color=WHITE,
                stroke_width=1.8,
            )
            zw1 = make_wavelet(inset_cx - 0.55, inset_cy + 0.05,
                               x_scale=0.30, color=YELLOW,
                               stroke_width=1.8, amp=0.30)
            zw2 = make_wavelet(inset_cx + 0.55, inset_cy + 0.05,
                               x_scale=0.22, color=YELLOW,
                               stroke_width=1.8, amp=0.30)
            return VGroup(frame, zoom_wave, zw1, zw2)

        # ----------------------------------------------------------------
        # Beat 1: 0.00-4.74 -- title + full neural signal.
        # ----------------------------------------------------------------
        prev_wavelet = make_wavelet(0, 0, x_scale=1.0, color=WHITE)
        prev_label = Text("Short-duration oscillatory function",
                          font_size=24, color=WHITE).move_to([0, -2.6, 0])

        title = Text("Multi-Resolution Analysis", font_size=42, color=WHITE)
        title.move_to([0, 3.0, 0])
        title.set_z_index(10)

        signal = make_signal_waveform(SIGNAL_LEFT_X, SIGNAL_RIGHT_X)
        signal.set_z_index(3)

        self.add(prev_wavelet, prev_label)
        self.wait(max(0.05, 0.30))
        self.play(
            FadeOut(prev_wavelet), FadeOut(prev_label),
            FadeIn(title), FadeIn(signal),
            run_time=max(0.05, 2.90),
        )
        self.play(
            title.animate.set_color(YELLOW),
            title.animate.scale(1.04, about_point=title.get_center()),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.84))

        # gap 4.74 -> 5.66
        self.wait(max(0.05, 0.92))

        # ----------------------------------------------------------------
        # Beat 2: 5.66-8.92 -- one fixed window sliding in discrete steps.
        # ----------------------------------------------------------------
        fixed_window = Rectangle(
            width=2.0, height=1.8,
            stroke_color=GOLD, stroke_width=3,
            fill_opacity=0,
        ).move_to([-4.8, SIGNAL_CY, 0])
        fixed_window.set_z_index(6)

        label_fixed = Text("one fixed window", font_size=24, color=WHITE)
        label_fixed.move_to([0, -2.8, 0])
        label_fixed.set_z_index(10)

        self.play(FadeIn(fixed_window), run_time=max(0.05, 0.60))
        self.play(FadeIn(label_fixed), run_time=max(0.05, 0.40))

        fixed_steps = [-4.2, -3.5, -2.8, -2.1, -1.4]
        for sx in fixed_steps:
            self.play(fixed_window.animate.move_to([sx, SIGNAL_CY, 0]),
                      run_time=max(0.05, 0.30))
            self.wait(max(0.05, 0.07))
        self.wait(max(0.05, 0.41))

        # gap 8.92 -> 9.40
        self.wait(max(0.05, 0.48))

        # ----------------------------------------------------------------
        # Beat 3: 9.40-12.64 -- five wavelets at multiple scales.
        # ----------------------------------------------------------------
        wide1 = make_wavelet(-5.2, SIGNAL_CY, x_scale=1.3, color=ORANGE)
        wide2 = make_wavelet(-2.7, SIGNAL_CY, x_scale=1.0, color=ORANGE)
        medium = make_wavelet(0.5, SIGNAL_CY, x_scale=0.7, color=TEAL)
        narrow1 = make_wavelet(2.9, SIGNAL_CY, x_scale=0.30, color=YELLOW)
        narrow2 = make_wavelet(4.3, SIGNAL_CY, x_scale=0.20, color=YELLOW)

        wavelet_group = VGroup(wide1, wide2, medium, narrow1, narrow2)
        for wv in wavelet_group:
            wv.set_z_index(5)

        wide_group = VGroup(wide1, wide2)
        narrow_group = VGroup(narrow1, narrow2)

        label_multiple = Text("multiple scales", font_size=24, color=WHITE)
        label_multiple.move_to([0, -2.8, 0])
        label_multiple.set_z_index(10)

        self.play(FadeOut(fixed_window), FadeOut(label_fixed), run_time=max(0.05, 0.60))
        self.play(FadeIn(wavelet_group), run_time=max(0.05, 1.34))
        self.play(FadeIn(label_multiple), run_time=max(0.05, 0.70))
        self.play(
            wavelet_group.animate.set_stroke(width=6, opacity=1.0),
            run_time=max(0.05, 0.60),
        )

        # gap 12.64 -> 13.50
        self.wait(max(0.05, 0.86))

        # ----------------------------------------------------------------
        # Beat 4: 13.50-16.70 -- large wavelets / slower components.
        # ----------------------------------------------------------------
        label_large = Text("Large wavelets: slower components",
                           font_size=22, color=WHITE)
        label_large.scale_to_fit_width(6.0)
        label_large.move_to([-3.2, 2.1, 0])
        label_large.set_z_index(10)

        self.play(FadeOut(label_multiple), FadeIn(label_large), run_time=max(0.05, 0.60))
        self.play(wide_group.animate.set_stroke(width=6.5, opacity=1.0),
                  run_time=max(0.05, 0.50))
        self.play(
            wide_group.animate.stretch(1.15, dim=0,
                                       about_point=wide_group.get_center()),
            run_time=max(0.05, 0.80),
        )
        self.play(
            wide_group.animate.stretch(1 / 1.15, dim=0,
                                       about_point=wide_group.get_center()),
            run_time=max(0.05, 0.60),
        )
        self.wait(max(0.05, 0.70))

        # gap 16.70 -> 17.06
        self.wait(max(0.05, 0.36))

        # ----------------------------------------------------------------
        # Beat 5: 17.06-20.28 -- small wavelets / rapid transient events.
        # ----------------------------------------------------------------
        label_small = Text("Small wavelets: rapid transient events",
                           font_size=22, color=WHITE)
        label_small.scale_to_fit_width(5.8)
        label_small.move_to([3.0, 2.1, 0])
        label_small.set_z_index(10)

        self.play(FadeOut(label_large), FadeIn(label_small), run_time=max(0.05, 0.60))
        self.play(narrow_group.animate.set_stroke(width=6.5, opacity=1.0),
                  run_time=max(0.05, 0.50))
        self.play(
            narrow_group.animate.stretch(0.85, dim=0,
                                         about_point=narrow_group.get_center()),
            run_time=max(0.05, 0.82),
        )
        self.play(
            narrow_group.animate.stretch(1 / 0.85, dim=0,
                                         about_point=narrow_group.get_center()),
            run_time=max(0.05, 0.60),
        )
        self.wait(max(0.05, 0.70))

        # gap 20.28 -> 21.14
        self.wait(max(0.05, 0.86))

        # ----------------------------------------------------------------
        # Beat 6: 21.14-25.18 -- different resolutions for different parts.
        # ----------------------------------------------------------------
        slow_tint = Rectangle(
            width=5.0, height=2.2,
            fill_color=BLUE, fill_opacity=0.18,
            stroke_color=BLUE, stroke_width=1.5,
        ).move_to([slow_x, SIGNAL_CY, 0])
        slow_tint.set_z_index(1)

        spike_tint = Rectangle(
            width=1.4, height=2.2,
            fill_color=RED, fill_opacity=0.18,
            stroke_color=RED, stroke_width=1.5,
        ).move_to([spike_x, SIGNAL_CY, 0])
        spike_tint.set_z_index(1)

        label_diff = Text("Different resolutions for different parts",
                          font_size=24, color=WHITE)
        label_diff.scale_to_fit_width(10)
        label_diff.move_to([0, -2.8, 0])
        label_diff.set_z_index(10)

        self.play(FadeOut(label_small), run_time=max(0.05, 0.40))
        self.play(FadeIn(slow_tint), FadeIn(spike_tint), run_time=max(0.05, 0.70))
        self.play(FadeIn(label_diff), run_time=max(0.05, 0.50))
        self.play(
            wide_group.animate.set_stroke(color=BLUE, width=7),
            narrow_group.animate.set_stroke(color=RED, width=7),
            run_time=max(0.05, 0.60),
        )
        self.play(
            label_diff.animate.set_color(YELLOW),
            label_diff.animate.scale(1.05,
                                     about_point=label_diff.get_center()),
            run_time=max(0.05, 0.44),
        )
        self.wait(max(0.05, 1.40))

        # gap 25.18 -> 26.18
        self.wait(max(0.05, 1.00))

        # ----------------------------------------------------------------
        # Beat 7: 26.18-31.42 -- slow vs. transient highlight alternation.
        # ----------------------------------------------------------------
        label_same = Text(
            "Slow oscillations and brief events in the same recording",
            font_size=22, color=WHITE,
        )
        label_same.scale_to_fit_width(11)
        label_same.move_to([0, -2.8, 0])
        label_same.set_z_index(10)

        self.play(FadeOut(label_diff), FadeIn(label_same), run_time=max(0.05, 0.70))

        for _ in range(2):
            # Slow oscillation pulses blue.
            self.play(
                slow_tint.animate.set_fill(opacity=0.35),
                slow_tint.animate.scale(1.06,
                                        about_point=slow_tint.get_center()),
                run_time=max(0.05, 0.60),
            )
            self.play(
                slow_tint.animate.set_fill(opacity=0.18),
                slow_tint.animate.scale(1 / 1.06,
                                        about_point=slow_tint.get_center()),
                run_time=max(0.05, 0.50),
            )
            # Transient spike pulses red.
            self.play(
                spike_tint.animate.set_fill(opacity=0.40),
                spike_tint.animate.scale(1.06,
                                         about_point=spike_tint.get_center()),
                run_time=max(0.05, 0.60),
            )
            self.play(
                spike_tint.animate.set_fill(opacity=0.18),
                spike_tint.animate.scale(1 / 1.06,
                                         about_point=spike_tint.get_center()),
                run_time=max(0.05, 0.50),
            )
        self.wait(max(0.05, 0.14))

        # gap 31.42 -> 32.00
        self.wait(max(0.05, 0.58))

        # ----------------------------------------------------------------
        # Beat 8: 32.00-36.76 -- simultaneous highlights + zoomed inset.
        # ----------------------------------------------------------------
        self.play(
            wide_group.animate.scale(1.08, about_point=wide_group.get_center()),
            narrow_group.animate.scale(1.08,
                                       about_point=narrow_group.get_center()),
            run_time=max(0.05, 0.60),
        )
        self.play(
            wide_group.animate.scale(1 / 1.08,
                                     about_point=wide_group.get_center()),
            narrow_group.animate.scale(1 / 1.08,
                                       about_point=narrow_group.get_center()),
            run_time=max(0.05, 0.50),
        )

        inset = make_zoom_inset()
        self.play(GrowFromCenter(inset), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 0.40))
        self.play(FadeOut(inset), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 1.66))

        # gap 36.76 -> 37.66
        self.wait(max(0.05, 0.90))

        # ----------------------------------------------------------------
        # Beat 9: 37.66-39.02 -- split screen + Direct Comparison header.
        # ----------------------------------------------------------------
        left_signal = make_signal_waveform(-6.0, -0.2)
        right_signal = make_signal_waveform(0.2, 6.0)
        left_signal.set_z_index(3)
        right_signal.set_z_index(3)

        vert_line = Line([0, -3.0, 0], [0, 3.0, 0],
                         color=GREY, stroke_width=2)
        vert_line.set_z_index(8)

        header = Text("Direct Comparison", font_size=36, color=GOLD)
        header.move_to([0, 3.0, 0])
        header.set_z_index(10)

        self.play(
            FadeOut(signal),
            FadeOut(wavelet_group),
            FadeOut(slow_tint),
            FadeOut(spike_tint),
            FadeOut(label_same),
            FadeOut(title),
            FadeIn(left_signal),
            FadeIn(right_signal),
            FadeIn(header),
            Create(vert_line),
            run_time=max(0.05, 1.36),
        )

        # gap 39.02 -> 40.00
        self.wait(max(0.05, 0.98))

        # ----------------------------------------------------------------
        # Beat 10: 40.00-42.00 -- left side: STFT fixed window.
        # ----------------------------------------------------------------
        left_window2 = Rectangle(
            width=1.3, height=1.7,
            stroke_color=GOLD, stroke_width=3,
            fill_opacity=0,
        ).move_to([-5.1, SIGNAL_CY, 0])
        left_window2.set_z_index(6)

        stft_label = Text("STFT: one fixed window",
                          font_size=22, color=WHITE)
        stft_label.scale_to_fit_width(5.0)
        stft_label.move_to([-3.2, -2.6, 0])
        stft_label.set_z_index(10)

        self.play(FadeIn(left_window2), run_time=max(0.05, 0.40))
        self.play(FadeIn(stft_label), run_time=max(0.05, 0.40))

        left_steps = [-4.2, -3.4, -2.6, -1.8]
        for sx in left_steps:
            self.play(left_window2.animate.move_to([sx, SIGNAL_CY, 0]),
                      run_time=max(0.05, 0.25))
            self.wait(max(0.05, 0.05))

        # gap 42.00 -> 42.54
        self.wait(max(0.05, 0.54))

        # ----------------------------------------------------------------
        # Beat 11: 42.54-45.38 -- right side: wavelet multiple scales.
        # ----------------------------------------------------------------
        right_wavelets = VGroup(
            make_wavelet(0.9, SIGNAL_CY, x_scale=1.0, color=ORANGE),
            make_wavelet(2.2, SIGNAL_CY, x_scale=0.85, color=ORANGE),
            make_wavelet(3.1, SIGNAL_CY, x_scale=0.55, color=TEAL),
            make_wavelet(4.4, SIGNAL_CY, x_scale=0.20, color=YELLOW),
            make_wavelet(5.5, SIGNAL_CY, x_scale=0.16, color=YELLOW),
        )
        for wv in right_wavelets:
            wv.set_z_index(5)

        wavelet_analysis_label = Text("Wavelet analysis: multiple scales",
                                      font_size=22, color=WHITE)
        wavelet_analysis_label.scale_to_fit_width(5.5)
        wavelet_analysis_label.move_to([3.2, -2.6, 0])
        wavelet_analysis_label.set_z_index(10)

        self.play(FadeIn(right_wavelets), run_time=max(0.05, 0.90))
        self.play(FadeIn(wavelet_analysis_label), run_time=max(0.05, 0.50))
        self.play(
            right_wavelets.animate.scale(
                1.08, about_point=right_wavelets.get_center()
            ),
            run_time=max(0.05, 0.45),
        )
        self.play(
            right_wavelets.animate.scale(
                1 / 1.08, about_point=right_wavelets.get_center()
            ),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 0.54))

        # Final hold to 46.20
        self.wait(max(0.05, 0.82))