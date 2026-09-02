ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Panels and waveforms
        # ------------------------------------------------------------
        panel_width = 5.6
        panel_height = 3.0

        left_panel = Rectangle(
            width=panel_width,
            height=panel_height,
            fill_color="#1a1d24",
            fill_opacity=1,
            stroke_color="#8a8f98",
            stroke_width=2,
        ).move_to(LEFT * 3.3 + UP * 0.5)

        right_panel = Rectangle(
            width=panel_width,
            height=panel_height,
            fill_color="#1a1d24",
            fill_opacity=1,
            stroke_color="#8a8f98",
            stroke_width=2,
        ).move_to(RIGHT * 3.3 + UP * 0.5)

        panels = VGroup(left_panel, right_panel)

        def signal_y(t):
            slow_env = 1 / (1 + np.exp((t - 0.55) * 15))
            slow = 0.85 * np.sin(2 * np.pi * 1.5 * t) * slow_env
            spike = 1.15 * np.exp(-(((t - 0.82) / 0.015) ** 2))
            return slow + spike

        def x_on_panel(panel, t):
            left_x = panel.get_left()[0] + 0.25
            right_x = panel.get_right()[0] - 0.25
            return left_x + (right_x - left_x) * t

        def make_waveform(panel):
            x0 = panel.get_left()[0] + 0.25
            x1 = panel.get_right()[0] - 0.25
            cy = panel.get_center()[1]
            return ParametricFunction(
                lambda t: np.array([x0 + (x1 - x0) * t, cy + 1.05 * signal_y(t), 0]),
                t_range=[0, 1, 0.002],
                color=WHITE,
                stroke_width=2.5,
            )

        wave_left = make_waveform(left_panel)
        wave_right = make_waveform(right_panel)

        left_label = Text("STFT: Fixed Window", font_size=22, color=WHITE).next_to(
            left_panel, DOWN, buff=0.35
        )
        right_label = Text(
            "Wavelet Analysis: Adaptive Windows", font_size=21, color=WHITE
        ).scale_to_fit_width(5.4)
        right_label.next_to(right_panel, DOWN, buff=0.35)

        # ------------------------------------------------------------
        # Small spectrogram thumbnail
        # ------------------------------------------------------------
        spec_bg = Rectangle(
            width=2.0,
            height=1.0,
            fill_color="#111318",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        )
        spec_band = Rectangle(
            width=1.4,
            height=0.20,
            fill_color=ORANGE,
            fill_opacity=0.80,
            stroke_width=0,
        ).move_to(spec_bg.get_center() + LEFT * 0.4 + DOWN * 0.28)
        spec_band2 = Rectangle(
            width=1.0,
            height=0.15,
            fill_color=GOLD,
            fill_opacity=0.45,
            stroke_width=0,
        ).move_to(spec_bg.get_center() + LEFT * 0.5 + DOWN * 0.22)

        spec_axes = VGroup(
            Line(
                spec_bg.get_corner(DOWN + LEFT),
                spec_bg.get_corner(DOWN + RIGHT),
                color=GREY_B,
                stroke_width=1.5,
            ),
            Line(
                spec_bg.get_corner(DOWN + LEFT),
                spec_bg.get_corner(UP + LEFT),
                color=GREY_B,
                stroke_width=1.5,
            ),
        )

        spectrogram = VGroup(spec_bg, spec_band, spec_band2, spec_axes)
        spectrogram.next_to(left_panel, UP, buff=0.4)

        # ------------------------------------------------------------
        # STFT fixed window
        # ------------------------------------------------------------
        left_window = Rectangle(
            width=1.0,
            height=2.7,
            stroke_color=ORANGE,
            stroke_width=5,
            fill_color=ORANGE,
            fill_opacity=0.12,
            z_index=10,
        ).move_to(
            np.array([x_on_panel(left_panel, 0.2), left_panel.get_center()[1], 0])
        )

        fixed_label_new = Text("Fixed Analysis Window", font_size=22, color=WHITE).move_to(
            left_label
        )

        # ------------------------------------------------------------
        # Wavelet adaptive windows
        # ------------------------------------------------------------
        right_wide_window = Rectangle(
            width=2.2,
            height=2.7,
            stroke_color=GREEN,
            stroke_width=5,
            fill_color=GREEN,
            fill_opacity=0.12,
            z_index=10,
        ).move_to(
            np.array([x_on_panel(right_panel, 0.2), right_panel.get_center()[1], 0])
        )

        right_narrow_window = Rectangle(
            width=0.45,
            height=2.7,
            stroke_color=GREEN,
            stroke_width=5,
            fill_color=GREEN,
            fill_opacity=0.12,
            z_index=10,
        ).move_to(
            np.array([x_on_panel(right_panel, 0.82), right_panel.get_center()[1], 0])
        )

        # ------------------------------------------------------------
        # Blue/red feature highlights and annotations
        # ------------------------------------------------------------
        slow_hl_left = Rectangle(
            width=1.8,
            height=2.0,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.15,
        ).move_to(
            np.array([x_on_panel(left_panel, 0.2), left_panel.get_center()[1], 0])
        )

        slow_hl_right = Rectangle(
            width=2.0,
            height=2.0,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.15,
        ).move_to(
            np.array([x_on_panel(right_panel, 0.2), right_panel.get_center()[1], 0])
        )

        spike_hl_left = Rectangle(
            width=0.7,
            height=1.8,
            stroke_color=RED,
            stroke_width=3,
            fill_color=RED,
            fill_opacity=0.15,
        ).move_to(
            np.array([x_on_panel(left_panel, 0.82), left_panel.get_center()[1], 0])
        )

        spike_hl_right = Rectangle(
            width=0.7,
            height=1.8,
            stroke_color=RED,
            stroke_width=3,
            fill_color=RED,
            fill_opacity=0.15,
        ).move_to(
            np.array([x_on_panel(right_panel, 0.82), right_panel.get_center()[1], 0])
        )

        highlight_group = VGroup(
            slow_hl_left, slow_hl_right, spike_hl_left, spike_hl_right
        )

        slow_annotation = Text("slow oscillation", font_size=18, color=BLUE).move_to(
            np.array([x_on_panel(left_panel, 0.2), left_panel.get_top()[1] - 0.4, 0])
        )
        slow_arrow = Arrow(
            start=slow_annotation.get_bottom() + DOWN * 0.05,
            end=slow_hl_left.get_top() + DOWN * 0.1,
            buff=0.02,
            color=BLUE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        fast_annotation = Text("fast transient", font_size=18, color=RED).move_to(
            np.array([x_on_panel(right_panel, 0.82), right_panel.get_top()[1] - 0.4, 0])
        )
        fast_arrow = Arrow(
            start=fast_annotation.get_bottom() + DOWN * 0.05,
            end=spike_hl_right.get_top() + DOWN * 0.1,
            buff=0.02,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        # ------------------------------------------------------------
        # Red X, final title
        # ------------------------------------------------------------
        red_x = Text("✕", font_size=36, color=RED, z_index=20).move_to(
            np.array([left_window.get_center()[0], left_panel.get_top()[1] - 0.25, 0])
        )

        bottom_title = Text("Wavelet Analysis", font_size=34, color=GOLD).to_edge(
            DOWN, buff=0.4
        )

        # ------------------------------------------------------------
        # Beat 1: empty, then blank panels
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.78))
        self.play(FadeIn(panels), run_time=max(0.05, 0.02))

        # Beat 2: left waveform and label
        self.play(FadeIn(wave_left), run_time=max(0.05, 3.14))
        self.play(FadeIn(left_label), run_time=max(0.05, 0.76))

        # Beat 3: right waveform, sweep, right label
        sweep_rect = Rectangle(
            width=0.1,
            height=2.8,
            fill_color=YELLOW,
            fill_opacity=0.35,
            stroke_width=0,
        ).move_to(left_panel.get_left() + RIGHT * 0.1)

        self.play(FadeIn(wave_right), run_time=max(0.05, 1.40))
        self.play(
            sweep_rect.animate.move_to(left_panel.get_right() + LEFT * 0.1),
            run_time=max(0.05, 1.20),
        )
        self.play(FadeOut(sweep_rect), run_time=max(0.05, 0.20))
        self.play(FadeIn(right_label), run_time=max(0.05, 0.80))

        # Beat 4: dimmed spectrogram thumbnail
        self.play(FadeIn(spectrogram), run_time=max(0.05, 1.20))
        self.play(spectrogram.animate.set_opacity(0.60), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 5.20))
        self.wait(max(0.05, 0.80))

        # Beat 5: fixed window on left, label swap, panel brightens
        self.play(
            left_panel.animate.set_fill("#2a3040", opacity=1).set_stroke(
                color=WHITE, width=3
            ),
            run_time=max(0.05, 0.60),
        )
        self.play(GrowFromCenter(left_window), run_time=max(0.05, 0.80))
        self.play(ReplacementTransform(left_label, fixed_label_new), run_time=max(0.05, 1.20))
        left_label = fixed_label_new
        self.play(left_window.animate.set_stroke(width=6), run_time=max(0.05, 0.60))
        self.play(left_window.animate.set_stroke(width=5), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 2.10))

        # Gap before beat 6
        self.wait(max(0.05, 0.02))

        # Beat 6: fixed window squeezes / glows red
        self.play(
            left_window.animate.scale(0.88, about_point=left_window.get_center()).set_stroke(
                color=RED, width=7
            ),
            run_time=max(0.05, 0.68),
        )
        self.play(
            left_window.animate.scale(
                1 / 0.88, about_point=left_window.get_center()
            ).set_stroke(color=ORANGE, width=5),
            run_time=max(0.05, 0.80),
        )

        # Beat 7: fixed window glides across entire left waveform
        target_pos = np.array(
            [x_on_panel(left_panel, 1.0), left_panel.get_center()[1], 0]
        )
        self.play(left_window.animate.move_to(target_pos), run_time=max(0.05, 4.30))

        # Beat 8: right windows appear and pulse
        self.play(
            right_panel.animate.set_fill("#2a3040", opacity=1).set_stroke(
                color=WHITE, width=3
            ),
            run_time=max(0.05, 0.70),
        )
        self.play(GrowFromCenter(right_wide_window), run_time=max(0.05, 0.70))
        self.play(GrowFromCenter(right_narrow_window), run_time=max(0.05, 0.70))

        pulse_cycle_time = 5.1 / 3
        for _ in range(3):
            self.play(
                right_wide_window.animate.scale(
                    1.04, about_point=right_wide_window.get_center()
                ).set_stroke(width=6),
                right_narrow_window.animate.scale(
                    1.06, about_point=right_narrow_window.get_center()
                ).set_stroke(width=6),
                run_time=max(0.05, pulse_cycle_time * 0.4),
            )
            self.play(
                right_wide_window.animate.scale(
                    1 / 1.04, about_point=right_wide_window.get_center()
                ).set_stroke(width=5),
                right_narrow_window.animate.scale(
                    1 / 1.06, about_point=right_narrow_window.get_center()
                ).set_stroke(width=5),
                run_time=max(0.05, pulse_cycle_time * 0.4),
            )
            self.wait(max(0.05, pulse_cycle_time * 0.2))

        # Gap before beat 9
        self.wait(max(0.05, 1.02))

        # Beat 9: blue slow wave and red fast transient highlights
        self.play(FadeIn(highlight_group), run_time=max(0.05, 1.40))
        self.play(FadeIn(slow_annotation), FadeIn(slow_arrow), run_time=max(0.05, 1.00))
        self.play(FadeIn(fast_annotation), FadeIn(fast_arrow), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 2.28))

        # Gap before beat 10
        self.wait(max(0.05, 0.82))

        # Beat 10: left fixed window dims/red X, right windows light up
        self.play(
            left_window.animate.set_opacity(0.25),
            FadeIn(red_x),
            run_time=max(0.05, 0.70),
        )
        self.play(
            right_wide_window.animate.set_stroke(width=7).set_fill(GREEN, opacity=0.35),
            right_narrow_window.animate.set_stroke(width=7).set_fill(GREEN, opacity=0.35),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 1.38))

        # Gap before beat 11
        self.wait(max(0.05, 0.52))

        # Beat 11: right label enlarges/glows, left window fades, right windows breathe
        self.play(
            right_label.animate.scale(1.4).set_color(GOLD),
            left_window.animate.set_opacity(0.12),
            run_time=max(0.05, 1.20),
        )

        breathe_cycle_time = 1.84
        for _ in range(2):
            self.play(
                right_wide_window.animate.scale(
                    1.04, about_point=right_wide_window.get_center()
                ),
                right_narrow_window.animate.scale(
                    1.06, about_point=right_narrow_window.get_center()
                ),
                run_time=max(0.05, 0.70),
            )
            self.play(
                right_wide_window.animate.scale(
                    1 / 1.04, about_point=right_wide_window.get_center()
                ),
                right_narrow_window.animate.scale(
                    1 / 1.06, about_point=right_narrow_window.get_center()
                ),
                run_time=max(0.05, 0.70),
            )
            self.wait(max(0.05, 0.44))

        # Beat 12: final layout holds, bottom title fades in
        self.play(FadeIn(bottom_title), run_time=max(0.05, 1.08))