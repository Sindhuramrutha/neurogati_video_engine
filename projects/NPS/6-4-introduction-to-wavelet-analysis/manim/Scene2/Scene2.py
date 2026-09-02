ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Shared drawing helpers
        # ----------------------------------------------------------------
        def make_endless_wave(center_y, amp, phase=0.0, num_cycles=5, color=WHITE, stroke_width=2.5):
            def func(t):
                x = -8 + 16 * t
                y = center_y + amp * np.sin(2 * np.pi * num_cycles * t + phase)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                func,
                t_range=[0, 1, 0.002],
                color=color,
                stroke_width=stroke_width,
            )

        def make_wavelet(center_x, center_y, x_scale=1.0, color=WHITE, stroke_width=3.5, amp=0.65):
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

        # Neural signal definition — same slow + transient spike structure used earlier.
        def signal_y(t):
            slow_env = 1 / (1 + np.exp((t - 0.55) * 15))
            slow = 0.85 * np.sin(2 * np.pi * 1.5 * t) * slow_env
            spike = 1.15 * np.exp(-(((t - 0.82) / 0.015) ** 2))
            return slow + spike

        SIGNAL_LEFT_X = -6.2
        SIGNAL_RIGHT_X = 5.8
        SIGNAL_CY = 0.0
        SIGNAL_AMP = 0.55
        SIGNAL_WIDTH = SIGNAL_RIGHT_X - SIGNAL_LEFT_X
        SLOW_T = 0.22
        SPIKE_T = 0.82
        slow_x = SIGNAL_LEFT_X + SIGNAL_WIDTH * SLOW_T
        spike_x = SIGNAL_LEFT_X + SIGNAL_WIDTH * SPIKE_T

        def make_signal_waveform():
            def func(t):
                x = SIGNAL_LEFT_X + SIGNAL_WIDTH * t
                y = SIGNAL_CY + SIGNAL_AMP * signal_y(t)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                func,
                t_range=[0, 1, 0.002],
                color=WHITE,
                stroke_width=2.5,
            )

        # Layout constants
        TOP_SINE_Y = 2.3
        COSINE_Y = 0.65
        TOP_SINE_AMP = 0.65
        FOURIER_LABEL_Y = 3.28
        SINE_LABEL_Y = 1.05
        EARLY_WAVELET_Y = -1.7
        EARLY_WAVELET_X = -4.5
        WAVELET_LABEL_EARLY_Y = -3.0

        # ----------------------------------------------------------------
        # Beat 1: infinite sine wave + Fourier basis label
        # ----------------------------------------------------------------
        sine_wave = make_endless_wave(center_y=TOP_SINE_Y, amp=TOP_SINE_AMP, color=WHITE)
        cosine_wave = make_endless_wave(
            center_y=COSINE_Y, amp=TOP_SINE_AMP, phase=np.pi / 2, color=WHITE
        )

        label_sine = Text(
            "Fourier basis: sine wave", font_size=27, color=GOLD
        ).move_to([0, SINE_LABEL_Y, 0])
        label_fourier = Text(
            "Fourier Transform", font_size=28, color=GOLD
        ).move_to([0, FOURIER_LABEL_Y, 0])

        self.play(FadeIn(sine_wave), run_time=max(0.05, 1.0))
        self.play(FadeIn(label_sine), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.52))

        # ----------------------------------------------------------------
        # Beat 2: finite wavelet appears below
        # ----------------------------------------------------------------
        single_wavelet = make_wavelet(
            EARLY_WAVELET_X, EARLY_WAVELET_Y, x_scale=1.0, color=WHITE
        )
        self.play(FadeIn(single_wavelet), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 1.54))

        # ----------------------------------------------------------------
        # Beat 3: wavelet label + pulse
        # ----------------------------------------------------------------
        label_wavelet = Text("Wavelet", font_size=28, color=WHITE).move_to(
            [EARLY_WAVELET_X, WAVELET_LABEL_EARLY_Y, 0]
        )

        self.play(FadeIn(label_wavelet), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.32))
        self.play(
            single_wavelet.animate.scale(1.12, about_point=single_wavelet.get_center()),
            run_time=max(0.05, 0.5),
        )
        self.play(
            single_wavelet.animate.scale(1 / 1.12, about_point=single_wavelet.get_center()),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.10))

        # ----------------------------------------------------------------
        # Beat 4: ghosted wavelet copies at different scales
        # ----------------------------------------------------------------
        ghost_specs = [(-0.8, 1.7), (2.1, 1.0), (4.4, 0.55)]
        ghost_wavelets = VGroup()
        for pos_x, xscale in ghost_specs:
            gw = make_wavelet(pos_x, EARLY_WAVELET_Y, x_scale=xscale, color=WHITE)
            gw.set_opacity(0.25)
            ghost_wavelets.add(gw)

        label_diff = Text("Different scales", font_size=27, color=WHITE).move_to(
            [1.9, -2.9, 0]
        )

        self.play(FadeIn(ghost_wavelets), FadeIn(label_diff), run_time=max(0.05, 1.0))
        for gw in ghost_wavelets:
            self.play(gw.animate.set_opacity(1.0), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.87))

        # gap 11.20 -> 11.68
        self.wait(max(0.05, 0.48))

        # ----------------------------------------------------------------
        # Beat 5: ghosted wavelets leave; cosine joins sine; Fourier label
        # ----------------------------------------------------------------
        self.play(FadeOut(ghost_wavelets), FadeOut(label_diff), run_time=max(0.05, 0.6))
        self.play(
            sine_wave.animate.set_stroke(color=YELLOW, width=5),
            run_time=max(0.05, 0.7),
        )
        self.play(FadeIn(cosine_wave), run_time=max(0.05, 1.0))
        self.play(FadeOut(label_sine), FadeIn(label_fourier), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.76))

        # gap 16.54 -> 17.08
        self.wait(max(0.05, 0.54))

        # ----------------------------------------------------------------
        # Beat 6: row of three identical wavelets
        # ----------------------------------------------------------------
        left_row_wavelet = make_wavelet(-3.3, 0.0, x_scale=1.0, color=WHITE)
        right_row_wavelet = make_wavelet(3.3, 0.0, x_scale=1.0, color=WHITE)
        label_wavelet_transform = Text(
            "Wavelet Transform", font_size=30, color=GOLD
        ).move_to([0, -2.7, 0])

        self.play(
            FadeOut(sine_wave),
            FadeOut(cosine_wave),
            FadeOut(label_fourier),
            FadeOut(label_wavelet),
            single_wavelet.animate.move_to([0, 0, 0]),
            run_time=max(0.05, 1.0),
        )
        self.play(
            FadeIn(left_row_wavelet),
            FadeIn(right_row_wavelet),
            FadeIn(label_wavelet_transform),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.2))

        row_wavelets = VGroup(single_wavelet, left_row_wavelet, right_row_wavelet)
        self.play(row_wavelets.animate.scale(1.08, about_point=ORIGIN), run_time=max(0.05, 0.5))
        self.play(row_wavelets.animate.scale(1 / 1.08, about_point=ORIGIN), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.66))

        # gap 21.94 -> 22.42
        self.wait(max(0.05, 0.48))

        # ----------------------------------------------------------------
        # Beat 7: neural signal + stretching medium wavelet
        # ----------------------------------------------------------------
        signal_mob = make_signal_waveform()
        signal_mob.set_z_index(3)

        slow_wavelet_mob = make_wavelet(
            slow_x, SIGNAL_CY, x_scale=1.0, color=ORANGE
        )
        slow_wavelet_mob.set_z_index(5)

        label_stretchable = Text(
            "Wavelets can be stretched or compressed", font_size=26, color=WHITE
        ).scale_to_fit_width(10)
        label_stretchable.move_to([0, -2.5, 0])

        self.play(
            FadeOut(row_wavelets),
            FadeOut(label_wavelet_transform),
            FadeIn(signal_mob),
            FadeIn(slow_wavelet_mob),
            FadeIn(label_stretchable),
            run_time=max(0.05, 1.2),
        )
        self.play(
            slow_wavelet_mob.animate.stretch(
                1.8, dim=0, about_point=slow_wavelet_mob.get_center()
            ),
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 1.14))

        # gap 27.26 -> 28.14
        self.wait(max(0.05, 0.88))

        # ----------------------------------------------------------------
        # Beat 8: wide wavelet over slow oscillation, blue highlight
        # ----------------------------------------------------------------
        slow_highlight = Rectangle(
            width=5.4,
            height=2.2,
            fill_color=BLUE,
            fill_opacity=0.18,
            stroke_color=BLUE,
            stroke_width=1.5,
        ).move_to([slow_x, SIGNAL_CY, 0])
        slow_highlight.set_z_index(0)

        label_wide = Text(
            "Wide wavelet: better frequency resolution",
            font_size=20,
            color=ORANGE,
        ).scale_to_fit_width(5.0)
        label_wide.move_to([slow_x + 2.0, 1.8, 0])

        self.play(FadeOut(label_stretchable), run_time=max(0.05, 0.5))
        self.play(FadeIn(slow_highlight), run_time=max(0.05, 0.8))
        self.play(
            slow_wavelet_mob.animate.stretch(
                1.4, dim=0, about_point=slow_wavelet_mob.get_center()
            ),
            run_time=max(0.05, 1.6),
        )
        self.play(FadeIn(label_wide), run_time=max(0.05, 1.0))
        self.play(label_wide.animate.set_color(YELLOW).scale(1.1), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.98))

        # gap 33.72 -> 34.78
        self.wait(max(0.05, 1.06))

        # ----------------------------------------------------------------
        # Beat 9: narrow wavelet over spike, red highlight
        # ----------------------------------------------------------------
        spike_highlight = Rectangle(
            width=0.9,
            height=2.2,
            fill_color=RED,
            fill_opacity=0.22,
            stroke_color=RED,
            stroke_width=1.5,
        ).move_to([spike_x, SIGNAL_CY, 0])
        spike_highlight.set_z_index(0)

        spike_wavelet_mob = make_wavelet(
            spike_x, SIGNAL_CY, x_scale=1.0, color=YELLOW
        )
        spike_wavelet_mob.set_z_index(5)

        label_narrow = Text(
            "Narrow wavelet: better time resolution",
            font_size=20,
            color=WHITE,
        ).scale_to_fit_width(5.0)
        label_narrow.move_to([spike_x, 1.8, 0])

        self.play(
            FadeOut(label_wide),
            FadeOut(slow_highlight),
            FadeOut(slow_wavelet_mob),
            run_time=max(0.05, 1.0),
        )
        self.play(
            FadeIn(spike_highlight),
            FadeIn(spike_wavelet_mob),
            run_time=max(0.05, 1.1),
        )
        self.play(
            spike_wavelet_mob.animate.stretch(
                0.45, dim=0, about_point=spike_wavelet_mob.get_center()
            ),
            run_time=max(0.05, 1.2),
        )
        self.play(FadeIn(label_narrow), run_time=max(0.05, 0.7))
        self.play(label_narrow.animate.set_color(YELLOW).scale(1.1), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.3))

        # gap 39.68 -> 40.82
        self.wait(max(0.05, 1.14))

        # ----------------------------------------------------------------
        # Beat 10: both wavelets over the fixed signal, adapt size
        # ----------------------------------------------------------------
        wide_wavelet_both = make_wavelet(
            slow_x, SIGNAL_CY, x_scale=2.52, color=ORANGE
        )
        wide_wavelet_both.set_z_index(5)

        label_adapting = Text(
            "Adapting function size", font_size=28, color=GOLD
        ).move_to([0, -2.6, 0])

        self.play(FadeOut(label_narrow), run_time=max(0.05, 0.5))
        self.play(FadeIn(wide_wavelet_both), run_time=max(0.05, 0.7))
        self.play(FadeIn(label_adapting), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.12))

        for _ in range(4):
            self.play(
                wide_wavelet_both.animate.stretch(
                    1.06, dim=0, about_point=wide_wavelet_both.get_center()
                ),
                spike_wavelet_mob.animate.stretch(
                    0.94, dim=0, about_point=spike_wavelet_mob.get_center()
                ),
                run_time=max(0.05, 0.65),
            )
            self.play(
                wide_wavelet_both.animate.stretch(
                    1 / 1.06, dim=0, about_point=wide_wavelet_both.get_center()
                ),
                spike_wavelet_mob.animate.stretch(
                    1 / 0.94, dim=0, about_point=spike_wavelet_mob.get_center()
                ),
                run_time=max(0.05, 0.65),
            )

        # gap 48.04 -> 48.96
        self.wait(max(0.05, 0.92))

        # ----------------------------------------------------------------
        # Beat 11: single centered wavelet + final definition
        # ----------------------------------------------------------------
        final_wavelet = make_wavelet(0, 0, x_scale=1.0, color=WHITE)
        final_label = Text(
            "Short-duration oscillatory function", font_size=28, color=WHITE
        ).scale_to_fit_width(10)
        final_label.move_to([0, -2.5, 0])

        self.play(
            FadeOut(wide_wavelet_both),
            FadeOut(spike_wavelet_mob),
            FadeOut(signal_mob),
            FadeOut(spike_highlight),
            FadeOut(label_adapting),
            FadeIn(final_wavelet),
            run_time=max(0.05, 1.2),
        )
        self.play(FadeIn(final_label), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 3.5))

        # 54.46 — label brighten + single scale-variation demonstration
        self.play(final_label.animate.set_color(YELLOW).scale(1.12), run_time=max(0.05, 0.35))
        self.play(
            final_wavelet.animate.stretch(1.25, dim=0, about_point=ORIGIN),
            run_time=max(0.05, 0.45),
        )
        self.play(
            final_wavelet.animate.stretch(1 / 1.25, dim=0, about_point=ORIGIN),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 0.17))