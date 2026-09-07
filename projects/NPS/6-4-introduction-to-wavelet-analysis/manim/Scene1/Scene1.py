ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Shared signal definition (continuity with previous scene)
        # ------------------------------------------------------------
        def signal_y(t):
            slow_env = 1 / (1 + np.exp((t - 0.55) * 15))
            slow = 0.85 * np.sin(2 * np.pi * 1.5 * t) * slow_env
            spike = 1.15 * np.exp(-(((t - 0.82) / 0.015) ** 2))
            return slow + spike

        # Main central waveform geometry
        LEFT_X = -4.5
        RIGHT_X = 3.5
        CY = 0.6
        AMP = 0.9
        SIGNAL_WIDTH = RIGHT_X - LEFT_X

        spike_t = 0.82
        spike_x = LEFT_X + SIGNAL_WIDTH * spike_t

        def wave_t_x(t):
            return LEFT_X + SIGNAL_WIDTH * t

        def wave_t_y(t):
            return CY + AMP * signal_y(t)

        def wave_point(t):
            return np.array([wave_t_x(t), wave_t_y(t), 0.0])

        def make_waveform(left_x=LEFT_X, right_x=RIGHT_X, cy=CY, amp=AMP,
                          color=WHITE, stroke_width=2.5):
            def func(t):
                return np.array(
                    [left_x + (right_x - left_x) * t, cy + amp * signal_y(t), 0.0]
                )

            return ParametricFunction(
                func,
                t_range=[0, 1, 0.002],
                color=color,
                stroke_width=stroke_width,
            )

        # ------------------------------------------------------------
        # Beat 2 central waveform
        # ------------------------------------------------------------
        wave = make_waveform()

        # ------------------------------------------------------------
        # Beat 3 title
        # ------------------------------------------------------------
        title_stft = Text(
            "Short-Time Fourier Transform Limitation",
            font_size=30,
            color=WHITE,
        ).scale_to_fit_width(8)
        title_stft.move_to([-0.5, -2.4, 0])

        # ------------------------------------------------------------
        # Beat 4: large orange window over slow oscillation
        # ------------------------------------------------------------
        t_large_center = 0.22
        t_large_width = 0.33
        large_window_width = t_large_width * SIGNAL_WIDTH

        large_window = Rectangle(
            width=large_window_width,
            height=2.2,
            stroke_color=ORANGE,
            stroke_width=5,
            fill_color=ORANGE,
            fill_opacity=0.12,
            z_index=5,
        ).move_to([wave_t_x(t_large_center), CY, 0])

        dots_large = VGroup(*[
            Dot(wave_point(t), radius=0.055, color=YELLOW, z_index=6)
            for t in np.linspace(
                t_large_center - t_large_width / 2 + 0.015,
                t_large_center + t_large_width / 2 - 0.015,
                14,
            )
        ])

        # ------------------------------------------------------------
        # Beat 5: sharp-peaked frequency spectrum
        # ------------------------------------------------------------
        sharp_panel = Rectangle(
            width=2.4,
            height=2.4,
            fill_color="#15181e",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to([5.3, 1.0, 0])

        spec_left = sharp_panel.get_left()[0] + 0.25
        spec_right = sharp_panel.get_right()[0] - 0.2
        spec_bottom = sharp_panel.get_bottom()[1] + 0.28
        spec_top = sharp_panel.get_top()[1] - 0.25
        spec_peak_x = (spec_left + spec_right) / 2

        sharp_peak = Polygon(
            np.array([spec_peak_x - 0.13, spec_bottom, 0]),
            np.array([spec_peak_x, spec_top, 0]),
            np.array([spec_peak_x + 0.13, spec_bottom, 0]),
            fill_color=ORANGE,
            fill_opacity=0.85,
            stroke_color=ORANGE,
            stroke_width=2.5,
        )

        spec_freq = Text("Frequency", font_size=13, color=GREY_B).move_to(
            [spec_peak_x, spec_bottom - 0.28, 0]
        )
        spec_amp = Text("Amplitude", font_size=13, color=GREY_B).rotate(
            90 * DEGREES
        ).move_to([spec_left - 0.3, (spec_bottom + spec_top) / 2, 0])

        spec_axes = VGroup(
            Line(
                [spec_left, spec_bottom, 0],
                [spec_right, spec_bottom, 0],
                color=GREY_B,
                stroke_width=1.5,
            ),
            Line(
                [spec_left, spec_bottom, 0],
                [spec_left, spec_top, 0],
                color=GREY_B,
                stroke_width=1.5,
            ),
        )

        sharp_spectrum_plot = VGroup(
            sharp_panel, spec_axes, sharp_peak, spec_freq, spec_amp
        )

        label_excellent = Text(
            "Excellent frequency resolution",
            font_size=20,
            color=GOLD,
        ).scale_to_fit_width(3.0)
        label_excellent.move_to([5.3, sharp_panel.get_top()[1] + 0.35, 0])

        label_many_data = Text(
            "Many data points", font_size=20, color=ORANGE
        ).move_to([wave_t_x(t_large_center), large_window.get_top()[1] + 0.35, 0])

        label_large_window_bottom = Text(
            "Large window", font_size=30, color=GOLD
        ).move_to([-0.5, -2.85, 0])

        # ============================================================
        # Beat 1: empty screen
        # ============================================================
        self.wait(max(0.05, 1.46))

        # ============================================================
        # Beat 2: waveform fades in
        # ============================================================
        self.play(FadeIn(wave), run_time=max(0.05, 1.76))

        # ============================================================
        # Beat 3: limitation title
        # ============================================================
        self.play(FadeIn(title_stft), run_time=max(0.05, 1.54))

        # ============================================================
        # Beat 4: large window and data-point dots
        # ============================================================
        self.play(FadeIn(large_window), run_time=max(0.05, 1.2))
        self.play(FadeIn(dots_large), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 0.28))

        # ============================================================
        # Beat 5: sharp spectrum, labels, and peak pulse
        # ============================================================
        self.play(
            FadeIn(sharp_spectrum_plot),
            FadeIn(label_excellent),
            FadeIn(label_many_data),
            FadeIn(label_large_window_bottom),
            run_time=max(0.05, 1.6),
        )
        self.wait(max(0.05, 1.02))  # reaches 9.76
        self.play(
            sharp_peak.animate.scale(1.25, about_point=sharp_peak.get_center()),
            run_time=max(0.05, 0.3),
        )
        self.play(
            sharp_peak.animate.scale(1 / 1.25, about_point=sharp_peak.get_center()),
            run_time=max(0.05, 0.3),
        )
        self.play(FadeOut(label_large_window_bottom), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.08))

        # gap
        self.wait(max(0.05, 0.64))

        # ============================================================
        # Beat 6: large window slides over spike; fuzzy timing band
        # ============================================================
        spike_tint = Rectangle(
            width=1.0,
            height=1.9,
            fill_color=RED,
            fill_opacity=0.22,
            stroke_width=0,
            z_index=3,
        ).move_to([spike_x, CY, 0])

        fuzzy_band = Rectangle(
            width=large_window_width,
            height=0.16,
            fill_color=RED,
            fill_opacity=0.35,
            stroke_color=RED,
            stroke_width=1.5,
        ).move_to([spike_x, CY - 1.25, 0])

        label_timing_uncertain = Text(
            "Timing uncertain", font_size=20, color=RED
        ).move_to([spike_x, CY - 1.75, 0])

        self.play(FadeIn(spike_tint), FadeOut(dots_large), run_time=max(0.05, 0.8))
        self.play(
            FadeOut(label_many_data),
            large_window.animate.move_to([spike_x, CY, 0]),
            sharp_spectrum_plot.animate.set_opacity(0.55),
            label_excellent.animate.set_opacity(0.55),
            run_time=max(0.05, 2.0),
        )
        self.play(
            FadeIn(fuzzy_band),
            FadeIn(label_timing_uncertain),
            run_time=max(0.05, 0.9),
        )
        self.wait(max(0.05, 1.36))

        # gap
        self.wait(max(0.05, 0.70))

        # ============================================================
        # Beat 7: crossfade to fresh waveform; small window appears
        # ============================================================
        fresh_wave = make_waveform()
        small_window = Rectangle(
            width=0.8,
            height=2.2,
            stroke_color=ORANGE,
            stroke_width=5,
            fill_color=ORANGE,
            fill_opacity=0.14,
            z_index=5,
        ).move_to([spike_x, CY, 0])

        old_wave = wave
        overlays_fade = VGroup(
            large_window,
            spike_tint,
            fuzzy_band,
            label_timing_uncertain,
            sharp_spectrum_plot,
            label_excellent,
            title_stft,
        )

        self.play(
            FadeOut(old_wave),
            FadeIn(fresh_wave),
            FadeOut(overlays_fade),
            run_time=max(0.05, 1.4),
        )
        self.remove(old_wave)
        wave = fresh_wave

        self.play(FadeIn(small_window), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.54))

        # ============================================================
        # Beat 8: small window tightens; precise vertical timing line
        # ============================================================
        self.play(
            small_window.animate.scale(0.75, about_point=small_window.get_center()),
            run_time=max(0.05, 1.0),
        )

        vertical_line = Line(
            start=np.array([spike_x, CY + 1.35, 0]),
            end=np.array([spike_x, CY - 1.2, 0]),
            color=YELLOW,
            stroke_width=4,
            z_index=7,
        )
        precise_label = Text("Precise timing", font_size=20, color=YELLOW).move_to(
            [spike_x, CY + 1.7, 0]
        )

        self.play(Create(vertical_line), FadeIn(precise_label), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 1.76))

        # ============================================================
        # Beat 9: broad, smeared spectrum
        # ============================================================
        broad_panel = Rectangle(
            width=2.4,
            height=2.4,
            fill_color="#15181e",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to([5.3, 1.0, 0])

        broad_axes = VGroup(
            Line(
                [spec_left, spec_bottom, 0],
                [spec_right, spec_bottom, 0],
                color=GREY_B,
                stroke_width=1.5,
            ),
            Line(
                [spec_left, spec_bottom, 0],
                [spec_left, spec_top, 0],
                color=GREY_B,
                stroke_width=1.5,
            ),
        )
        broad_peak = Polygon(
            np.array([spec_peak_x - 1.1, spec_bottom, 0]),
            np.array([spec_peak_x, spec_bottom + 0.75, 0]),
            np.array([spec_peak_x + 1.1, spec_bottom, 0]),
            fill_color=RED,
            fill_opacity=0.85,
            stroke_color=RED,
            stroke_width=2.5,
        )
        broad_freq = Text("Frequency", font_size=13, color=GREY_B).move_to(
            [spec_peak_x, spec_bottom - 0.28, 0]
        )
        broad_amp = Text("Amplitude", font_size=13, color=GREY_B).rotate(
            90 * DEGREES
        ).move_to([spec_left - 0.3, (spec_bottom + spec_top) / 2, 0])

        broad_spectrum_plot = VGroup(
            broad_panel, broad_axes, broad_peak, broad_freq, broad_amp
        )

        label_poor = Text(
            "Poor frequency resolution", font_size=20, color=RED
        ).scale_to_fit_width(3.0)
        label_poor.move_to([5.3, broad_panel.get_top()[1] + 0.35, 0])

        label_few = Text("Few data points", font_size=20, color=ORANGE).next_to(
            small_window, LEFT, buff=0.35
        )

        self.play(
            FadeIn(broad_spectrum_plot),
            FadeIn(label_poor),
            FadeIn(label_few),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 3.12))  # reaches 30.26
        self.play(
            broad_peak.animate.scale(1.25, about_point=broad_peak.get_center()),
            run_time=max(0.05, 0.5),
        )
        self.play(
            broad_peak.animate.scale(1 / 1.25, about_point=broad_peak.get_center()),
            run_time=max(0.05, 0.4),
        )

        # gap
        self.wait(max(0.05, 0.78))

        # ============================================================
        # Beat 10: split view of both scenarios
        # ============================================================
        left_panel = Rectangle(
            width=5.4,
            height=2.8,
            fill_color="#1a1d24",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to(LEFT * 3.2 + UP * 0.3)

        right_panel = Rectangle(
            width=5.4,
            height=2.8,
            fill_color="#1a1d24",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to(RIGHT * 3.2 + UP * 0.3)

        left_px0 = left_panel.get_left()[0] + 0.22
        left_px1 = left_panel.get_right()[0] - 0.22
        right_px0 = right_panel.get_left()[0] + 0.22
        right_px1 = right_panel.get_right()[0] - 0.22

        def left_px(t):
            return left_px0 + (left_px1 - left_px0) * t

        def right_px(t):
            return right_px0 + (right_px1 - right_px0) * t

        split_left_wave = make_waveform(
            left_px0, left_px1, left_panel.get_center()[1], 0.75, color=WHITE,
            stroke_width=2.2,
        )
        split_right_wave = make_waveform(
            right_px0, right_px1, right_panel.get_center()[1], 0.75, color=WHITE,
            stroke_width=2.2,
        )

        left_split_window = Rectangle(
            width=1.6,
            height=2.1,
            stroke_color=ORANGE,
            stroke_width=4,
            fill_color=ORANGE,
            fill_opacity=0.12,
        ).move_to([left_px(0.2), left_panel.get_center()[1], 0])

        right_split_window = Rectangle(
            width=0.4,
            height=2.1,
            stroke_color=ORANGE,
            stroke_width=4,
            fill_color=ORANGE,
            fill_opacity=0.14,
        ).move_to([right_px(0.82), right_panel.get_center()[1], 0])

        left_fuzzy = Rectangle(
            width=0.7,
            height=0.1,
            fill_color=RED,
            fill_opacity=0.45,
            stroke_width=0,
        ).move_to([left_px(0.82), left_panel.get_bottom()[1] + 0.18, 0])

        right_vertical = Line(
            start=np.array([right_px(0.82), right_panel.get_top()[1] - 0.15, 0]),
            end=np.array([right_px(0.82), right_panel.get_bottom()[1] + 0.15, 0]),
            color=YELLOW,
            stroke_width=3,
        )

        left_mini_spec_bg = Rectangle(
            width=1.4,
            height=1.2,
            fill_color="#111318",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=1.5,
        ).move_to([left_px1 - 0.55, left_panel.get_top()[1] - 0.45, 0])
        left_mini_peak = Rectangle(
            width=0.12,
            height=0.7,
            fill_color=ORANGE,
            fill_opacity=0.9,
            stroke_width=0,
        ).move_to(left_mini_spec_bg.get_center())
        left_mini_spec = VGroup(left_mini_spec_bg, left_mini_peak)

        right_mini_spec_bg = Rectangle(
            width=1.4,
            height=1.2,
            fill_color="#111318",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=1.5,
        ).move_to([right_px1 - 0.55, right_panel.get_top()[1] - 0.45, 0])
        right_mini_peak = Rectangle(
            width=0.8,
            height=0.45,
            fill_color=RED,
            fill_opacity=0.85,
            stroke_width=0,
        ).move_to(right_mini_spec_bg.get_center())
        right_mini_spec = VGroup(right_mini_spec_bg, right_mini_peak)

        split_view = VGroup(
            left_panel,
            right_panel,
            split_left_wave,
            split_right_wave,
            left_split_window,
            right_split_window,
            left_fuzzy,
            right_vertical,
            left_mini_spec,
            right_mini_spec,
        )

        fixed_window_label = Text(
            "Fixed window size", font_size=28, color=GOLD
        ).move_to([0, -2.5, 0])

        old_scene_group = VGroup(
            wave,
            small_window,
            vertical_line,
            precise_label,
            broad_spectrum_plot,
            label_poor,
            label_few,
        )

        self.play(
            FadeOut(old_scene_group),
            FadeIn(split_view),
            FadeIn(fixed_window_label),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 0.52))  # reaches 34.46

        self.play(
            left_split_window.animate.scale(
                1.05, about_point=left_split_window.get_center()
            ).set_stroke(width=6),
            right_split_window.animate.scale(
                1.08, about_point=right_split_window.get_center()
            ).set_stroke(width=6),
            run_time=max(0.05, 0.5),
        )
        self.play(
            left_split_window.animate.scale(
                1 / 1.05, about_point=left_split_window.get_center()
            ).set_stroke(width=4),
            right_split_window.animate.scale(
                1 / 1.08, about_point=right_split_window.get_center()
            ).set_stroke(width=4),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.54))

        # gap
        self.wait(max(0.05, 0.82))

        # ============================================================
        # Beat 11: full waveform returns; slow event labeled
        # ============================================================
        wave_alone = make_waveform()

        slow_event_label = Text("Slow event", font_size=22, color=BLUE).move_to(
            [wave_t_x(t_large_center), CY + 1.25, 0]
        )
        slow_event_arrow = Arrow(
            start=slow_event_label.get_bottom() + DOWN * 0.08,
            end=wave_point(t_large_center) + UP * 0.1,
            color=BLUE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
            buff=0.05,
        )
        slow_event_group = VGroup(slow_event_label, slow_event_arrow)

        self.play(
            FadeOut(split_view),
            FadeOut(fixed_window_label),
            FadeIn(wave_alone),
            run_time=max(0.05, 1.3),
        )
        self.play(FadeIn(slow_event_group), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.50))

        # ============================================================
        # Beat 12: two copies -- slow blue above, fast red below
        # ============================================================
        upper_y = 1.3
        lower_y = -1.3
        amp_two = 0.55

        upper_wave = make_waveform(
            LEFT_X, RIGHT_X, upper_y, amp_two, color=BLUE, stroke_width=2.5
        )
        lower_wave = make_waveform(
            LEFT_X, RIGHT_X, lower_y, amp_two, color=RED, stroke_width=2.5
        )

        def upper_point(t):
            return np.array([wave_t_x(t), upper_y + amp_two * signal_y(t), 0])

        def lower_point(t):
            return np.array([wave_t_x(t), lower_y + amp_two * signal_y(t), 0])

        upper_slow_tint = Rectangle(
            width=2.2,
            height=1.6,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=0,
        ).move_to([wave_t_x(0.18), upper_y, 0])

        lower_spike_tint = Rectangle(
            width=0.9,
            height=1.6,
            fill_color=RED,
            fill_opacity=0.25,
            stroke_width=0,
        ).move_to([spike_x, lower_y, 0])

        upper_slow_label = Text("Slow event", font_size=20, color=BLUE).move_to(
            [wave_t_x(0.18), upper_y + 0.9, 0]
        )
        upper_slow_arrow = Arrow(
            start=upper_slow_label.get_bottom() + DOWN * 0.08,
            end=upper_point(0.18) + UP * 0.1,
            color=BLUE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
            buff=0.05,
        )
        upper_slow_group = VGroup(upper_slow_label, upper_slow_arrow)

        lower_fast_label = Text(
            "Instantaneous event", font_size=20, color=RED
        ).move_to([spike_x, lower_y + 1.0, 0])
        lower_fast_arrow = Arrow(
            start=lower_fast_label.get_bottom() + DOWN * 0.08,
            end=lower_point(spike_t) + UP * 0.08,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
            buff=0.05,
        )
        lower_fast_group = VGroup(lower_fast_label, lower_fast_arrow)

        self.play(
            FadeOut(wave_alone),
            FadeOut(slow_event_group),
            FadeIn(upper_wave),
            FadeIn(lower_wave),
            run_time=max(0.05, 1.4),
        )
        self.play(
            FadeIn(upper_slow_tint),
            FadeIn(lower_spike_tint),
            FadeIn(upper_slow_group),
            FadeIn(lower_fast_group),
            run_time=max(0.05, 1.0),
        )
        self.play(
            upper_slow_label.animate.set_color(YELLOW).scale(1.1),
            lower_fast_label.animate.set_color(YELLOW).scale(1.1),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 1.70))

        # gap
        self.wait(max(0.05, 0.92))

        # ============================================================
        # Beat 13: merge back; adaptive dashed ghost windows
        # ============================================================
        wave_central3 = make_waveform()

        def dashed_rect(width, height, color=ORANGE, stroke_width=4):
            half_w = width / 2.0
            half_h = height / 2.0
            pts = [
                np.array([half_w, half_h, 0]),
                np.array([half_w, -half_h, 0]),
                np.array([-half_w, -half_h, 0]),
                np.array([-half_w, half_h, 0]),
            ]
            return VGroup(*[
                DashedLine(
                    pts[i],
                    pts[(i + 1) % 4],
                    color=color,
                    stroke_width=stroke_width,
                    dash_length=0.14,
                )
                for i in range(4)
            ])

        wide_ghost = dashed_rect(
            width=t_large_width * SIGNAL_WIDTH, height=2.3
        ).move_to([wave_t_x(t_large_center), CY, 0])
        narrow_ghost = dashed_rect(width=0.85, height=2.3).move_to(
            [spike_x, CY, 0]
        )
        adapt_label = Text("Adapt window size", font_size=30, color=GOLD).move_to(
            [0, -2.5, 0]
        )

        self.play(
            FadeOut(upper_wave),
            FadeOut(lower_wave),
            FadeOut(upper_slow_tint),
            FadeOut(lower_spike_tint),
            FadeOut(upper_slow_group),
            FadeOut(lower_fast_group),
            FadeIn(wave_central3),
            run_time=max(0.05, 1.2),
        )
        self.play(FadeIn(wide_ghost), FadeIn(adapt_label), run_time=max(0.05, 0.9))
        self.play(
            wide_ghost.animate.set_opacity(0.3),
            FadeIn(narrow_ghost),
            run_time=max(0.05, 0.9),
        )
        self.play(
            wide_ghost.animate.set_opacity(1),
            narrow_ghost.animate.set_opacity(1),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 1.42))

        # gap
        self.wait(max(0.05, 0.68))

        # ============================================================
        # Beat 14: final hold, breathing windows, Wavelet Analysis label
        # ============================================================
        wavelet_label = Text("Wavelet Analysis", font_size=34, color=GOLD).move_to(
            [0, -2.9, 0]
        )

        self.play(FadeOut(adapt_label), FadeIn(wavelet_label), run_time=max(0.05, 0.8))

        for _ in range(2):
            self.play(
                wide_ghost.animate.scale(
                    1.045, about_point=wide_ghost.get_center()
                ),
                narrow_ghost.animate.scale(
                    0.96, about_point=narrow_ghost.get_center()
                ),
                run_time=max(0.05, 0.5),
            )
            self.play(
                wide_ghost.animate.scale(
                    1 / 1.045, about_point=wide_ghost.get_center()
                ),
                narrow_ghost.animate.scale(
                    1 / 0.96, about_point=narrow_ghost.get_center()
                ),
                run_time=max(0.05, 0.5),
            )

        # 53.64 label glow once
        self.play(
            wavelet_label.animate.scale(1.15).set_color(YELLOW),
            run_time=max(0.05, 0.35),
        )
        self.play(
            wavelet_label.animate.scale(1 / 1.15).set_color(GOLD),
            run_time=max(0.05, 0.35),
        )
        self.wait(max(0.05, 0.54))