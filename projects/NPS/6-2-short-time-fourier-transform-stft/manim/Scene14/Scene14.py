ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene14(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helper
        # ------------------------------------------------------------
        def rot_vec(vec, angle):
            x, y = vec[0], vec[1]
            return np.array([
                x * np.cos(angle) - y * np.sin(angle),
                x * np.sin(angle) + y * np.cos(angle),
                0.0,
            ])

        # ------------------------------------------------------------
        # Summary layout from previous scene: title + three cards
        # ------------------------------------------------------------
        summary_title = Text(
            "Short-Time Fourier Transform",
            font_size=42, color=YELLOW, weight=BOLD,
        ).scale_to_fit_width(11).to_edge(UP, buff=0.35)

        card_w, card_h = 3.8, 2.7
        card1 = Rectangle(
            width=card_w, height=card_h,
            stroke_color=GREY_B, stroke_width=2.5,
            fill_color=GREY_B, fill_opacity=0.06,
        )
        card2 = card1.copy()
        card3 = card1.copy()
        cards = VGroup(card1, card2, card3).arrange(RIGHT, buff=0.8).move_to(np.array([0, 0.55, 0]))
        card1, card2, card3 = cards

        # --- Card 1: windowed waveform, fades out quickly ---
        card1_ax = Axes(
            x_range=[0, 10, 2.5],
            y_range=[-1.1, 1.1, 0.5],
            x_length=3.1,
            y_length=1.5,
            axis_config={"color": GREY_B, "stroke_width": 2},
            x_axis_config={"include_numbers": False, "include_ticks": False},
            y_axis_config={"include_numbers": False, "include_ticks": False},
        ).move_to(card1.get_center() + UP * 0.05)

        def card1_wave_func(x):
            return 0.85 * np.sin(2 * PI * 0.45 * x + 0.7) * np.sin(2 * PI * 0.13 * x + 0.3) + 0.2 * np.sin(2 * PI * 1.1 * x)

        wave_pts = [
            card1_ax.coords_to_point(x, card1_wave_func(x))
            for x in np.linspace(0.3, 9.7, 320)
        ]
        wave = VMobject(stroke_color=TEAL, stroke_width=3)
        wave.set_points_as_corners(wave_pts)

        win_center_x = 4.25
        win_width = card1_ax.c2p(5.0, 0)[0] - card1_ax.c2p(3.5, 0)[0]
        window = Rectangle(
            width=win_width,
            height=1.5,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.28,
        ).move_to(card1_ax.c2p(win_center_x, 0))
        label1 = Text("STFT", font_size=28, color=WHITE, weight=BOLD).next_to(card1, DOWN, buff=0.35)
        card1_group = VGroup(card1, card1_ax, wave, window, label1)

        # --- Card 2: time-varying spectra card ---
        mini_axes = []
        for _ in range(3):
            ax = Axes(
                x_range=[0, 10, 5],
                y_range=[0, 1.2, 0.5],
                x_length=0.9,
                y_length=1.2,
                axis_config={"color": GREY_B, "stroke_width": 2},
                x_axis_config={"include_numbers": False, "include_ticks": False},
                y_axis_config={"include_numbers": False, "include_ticks": False},
            )
            mini_axes.append(ax)
        spectra_axes_group = VGroup(*mini_axes).arrange(RIGHT, buff=0.22).move_to(card2.get_center() + UP * 0.1)

        peak_specs = [
            {"center": 2.6, "height": 0.9, "color": TEAL},
            {"center": 4.8, "height": 1.05, "color": GREEN},
            {"center": 7.0, "height": 0.75, "color": ORANGE},
        ]
        old_peaks = []
        for ax, spec in zip(mini_axes, peak_specs):
            xs = np.linspace(0.5, 9.5, 160)
            ys = spec["height"] * np.exp(-((xs - spec["center"]) ** 2) / (2 * 0.8 ** 2))
            curve = VMobject(stroke_color=spec["color"], stroke_width=4)
            curve.set_points_as_corners([ax.c2p(xs[i], ys[i]) for i in range(len(xs))])
            old_peaks.append(curve)
        old_spectra = VGroup(spectra_axes_group, *old_peaks)

        label2 = Text("Frequency content over time", font_size=24, color=WHITE).scale_to_fit_width(3.4).next_to(card2, DOWN, buff=0.35)

        time_axis_line = Line(
            start=spectra_axes_group.get_left() + DOWN * 0.55,
            end=spectra_axes_group.get_right() + DOWN * 0.55,
            color=GREY_B, stroke_width=2, stroke_opacity=0.8,
        )
        time_label = Text("time", font_size=22, color=GREY_B).next_to(time_axis_line, DOWN, buff=0.08)
        arrow_time = Arrow(
            start=spectra_axes_group.get_bottom() + DOWN * 0.1,
            end=time_axis_line.get_top(),
            buff=0.08, color=GREY_B, stroke_width=3,
            max_tip_length_to_length_ratio=0.2, stroke_opacity=0.8,
        )
        card2_group = VGroup(card2, old_spectra, label2, time_axis_line, arrow_time, time_label)

        # --- Card 3: balance scale, fades out quickly ---
        apex = card3.get_center() + UP * 0.18
        beam_angle = -0.08
        left_top = apex + rot_vec(LEFT * 1.4, beam_angle)
        right_top = apex + rot_vec(RIGHT * 1.4, beam_angle)
        left_pan_top = left_top + DOWN * 0.55
        right_pan_top = right_top + DOWN * 0.55

        beam_line = Line(left_top, right_top, color=WHITE, stroke_width=5)
        left_string = Line(left_top, left_pan_top, color=WHITE, stroke_width=2)
        right_string = Line(right_top, right_pan_top, color=WHITE, stroke_width=2)
        left_pan = Polygon(
            left_pan_top + LEFT * 0.3,
            left_pan_top + RIGHT * 0.3,
            left_pan_top + DOWN * 0.2,
        ).set_fill(GREY_B, opacity=0.4).set_stroke(WHITE, width=2)
        right_pan = Polygon(
            right_pan_top + LEFT * 0.3,
            right_pan_top + RIGHT * 0.3,
            right_pan_top + DOWN * 0.2,
        ).set_fill(GREY_B, opacity=0.4).set_stroke(WHITE, width=2)
        left_win_icon = Rectangle(
            width=0.35, height=0.45,
            fill_color=TEAL, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(left_pan_top + DOWN * 0.02)
        right_win_icon = Rectangle(
            width=0.85, height=0.45,
            fill_color=ORANGE, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(right_pan_top + DOWN * 0.02)
        fulcrum = Polygon(
            apex,
            apex + LEFT * 0.2 + DOWN * 0.45,
            apex + RIGHT * 0.2 + DOWN * 0.45,
        ).set_fill(GREY_B, opacity=0.8).set_stroke(WHITE, width=2)
        balance_rig = VGroup(
            beam_line, left_string, right_string,
            left_pan, right_pan,
            left_win_icon, right_win_icon,
        )
        balance_label = Text("Fixed analysis window", font_size=24, color=WHITE).scale_to_fit_width(3.4).next_to(card3, DOWN, buff=0.35)
        card3_group = VGroup(card3, fulcrum, balance_rig, balance_label)

        # ------------------------------------------------------------
        # Build the dense row of many small spectrum plots
        # ------------------------------------------------------------
        n_plots = 70
        plot_h = 3.2
        plot_w = 0.2
        gap = 0.08
        step = plot_w + gap
        left_edge = -5.9
        y_center = 0.6

        peak_norms = []
        for i in range(n_plots):
            p = 0.52 + 0.22 * np.sin(0.13 * i) + 0.06 * np.cos(0.07 * i)
            p = float(np.clip(p, 0.08, 0.92))
            peak_norms.append(p)

        row_plots = VGroup()
        for i, p in enumerate(peak_norms):
            axis = Line(
                start=np.array([0, -plot_h / 2, 0]),
                end=np.array([0, plot_h / 2, 0]),
                color=GREY_B, stroke_width=1.4,
            )
            y_peak = -plot_h / 2 + p * plot_h
            peak_color = [TEAL, GREEN, ORANGE][i % 3]
            stem = Line(
                start=np.array([0, y_peak, 0]),
                end=np.array([plot_w * 0.5, y_peak, 0]),
                color=peak_color, stroke_width=2,
            )
            dot = Dot(
                point=np.array([plot_w * 0.5, y_peak, 0]),
                radius=0.025, color=peak_color,
            )
            mini = VGroup(axis, stem, dot)
            x_center = left_edge + plot_w / 2 + i * step
            mini.move_to(np.array([x_center, y_center, 0]))
            row_plots.add(mini)
        row_plots.set_stroke(width=1.4, family=True)

        # Labels beneath first few plots, then ellipsis
        window_label_group = VGroup()
        for j, idx in enumerate([0, 3, 6]):
            lbl = Text(f"Window {j+1}", font_size=16, color=WHITE)
            lbl.next_to(row_plots[idx], DOWN, buff=0.3)
            window_label_group.add(lbl)
        ellipsis_label = Text("...", font_size=24, color=GREY_B).next_to(row_plots[9], DOWN, buff=0.35)
        window_label_group_total = VGroup(window_label_group, ellipsis_label)

        # ------------------------------------------------------------
        # Build the vertical colored-strip version of each spectrum
        # ------------------------------------------------------------
        strip_h = plot_h
        strip_w = plot_w
        n_seg = 18
        strips_group = VGroup()
        for i, p in enumerate(peak_norms):
            strip = VGroup()
            for j in range(n_seg):
                norm_y = (j + 0.5) / n_seg
                intensity = np.exp(-((norm_y - p) ** 2) / (2 * 0.18 ** 2))
                color = interpolate_color(GREY_B, YELLOW, float(intensity))
                seg = Rectangle(
                    width=strip_w,
                    height=strip_h / n_seg,
                    fill_color=color,
                    fill_opacity=1.0,
                    stroke_width=0,
                    stroke_opacity=0,
                )
                x_center = left_edge + plot_w / 2 + i * step
                seg_y = y_center - strip_h / 2 + (j + 0.5) * strip_h / n_seg
                seg.move_to(np.array([x_center, seg_y, 0]))
                strip.add(seg)
            strips_group.add(strip)

        # ------------------------------------------------------------
        # Initial state: previous summary layout already on screen
        # ------------------------------------------------------------
        self.add(summary_title, card1_group, card2_group, card3_group)

        # ------------------------------------------------------------
        # BEAT 1: 0.00 - 2.34
        # ------------------------------------------------------------
        self.play(FadeOut(card1_group, card3_group, summary_title), run_time=max(0.05, 0.8))

        self.play(
            LaggedStart(
                *[GrowFromCenter(p, point_color=TEAL) for p in row_plots],
                lag_ratio=0.005,
            ),
            FadeOut(card2_group),
            run_time=max(0.05, 0.8),
        )

        self.play(FadeIn(window_label_group), run_time=max(0.05, 0.4))
        self.play(FadeOut(window_label_group), FadeIn(ellipsis_label), run_time=max(0.05, 0.34))

        # ------------------------------------------------------------
        # BEAT 2: 2.34 - 5.16
        # ------------------------------------------------------------
        highlight = SurroundingRectangle(
            row_plots[0], color=YELLOW, buff=0.08,
            stroke_width=3, fill_color=YELLOW, fill_opacity=0.14,
        )

        self.play(
            self.camera.frame.animate.scale(1.7).move_to(row_plots.get_center()),
            FadeIn(highlight),
            run_time=max(0.05, 1.42),
        )

        for target_idx in [1, 2, 3, 4]:
            self.play(
                highlight.animate.move_to(row_plots[target_idx].get_center()),
                run_time=max(0.05, 0.35),
            )

        # ------------------------------------------------------------
        # BEAT 3: 5.16 - 7.76
        # ------------------------------------------------------------
        self.play(
            self.camera.frame.animate.scale(1.15),
            row_plots.animate.set_stroke(width=0.6),
            run_time=max(0.05, 2.6),
        )

        # ------------------------------------------------------------
        # BEAT 4: 7.76 - 13.76
        # ------------------------------------------------------------
        self.play(FadeOut(window_label_group_total), run_time=max(0.05, 0.8))
        self.play(ReplacementTransform(row_plots, strips_group), run_time=max(0.05, 5.2))

        spectrogram = row_plots  # row_plots has now been replaced by colored strips

        # ------------------------------------------------------------
        # BEAT 5: 13.76 - 19.64
        # ------------------------------------------------------------
        grid_target = spectrogram.copy()
        grid_target.arrange(RIGHT, buff=0).move_to(spectrogram.get_center())
        self.play(Transform(spectrogram, grid_target), run_time=max(0.05, 2.8))

        time_line = Line(
            spectrogram.get_left() + DOWN * 0.5,
            spectrogram.get_right() + DOWN * 0.5,
            color=WHITE, stroke_width=3,
        )
        time_axis_label = Text("Time", font_size=24, color=WHITE).next_to(time_line, DOWN, buff=0.15)

        freq_line = Line(
            spectrogram.get_bottom() + LEFT * 0.5,
            spectrogram.get_top() + LEFT * 0.5,
            color=WHITE, stroke_width=3,
        )
        freq_axis_label = Text("Frequency", font_size=24, color=WHITE).rotate(PI / 2).next_to(freq_line, LEFT, buff=0.15)

        colorbar = VGroup(*[
            Rectangle(
                width=0.22,
                height=spectrogram.get_height() / 20,
                fill_color=interpolate_color(GREY_B, YELLOW, i / 19),
                fill_opacity=1.0,
                stroke_width=0,
                stroke_opacity=0,
            )
            for i in range(20)
        ]).arrange(DOWN, buff=0).next_to(spectrogram, RIGHT, buff=0.6)

        self.play(
            FadeIn(time_line, time_axis_label, freq_line, freq_axis_label, colorbar),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 1.08))

        # ------------------------------------------------------------
        # BEAT 6: 19.64 - 23.26
        # ------------------------------------------------------------
        magnitude_label = Text("Magnitude", font_size=22, color=WHITE).next_to(colorbar, RIGHT, buff=0.2)
        self.play(FadeIn(magnitude_label), run_time=max(0.05, 1.2))
        self.play(Indicate(spectrogram, scale_factor=1.02, color=YELLOW), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.42))

        # ------------------------------------------------------------
        # BEAT 7: 23.26 - 26.45
        # ------------------------------------------------------------
        spectrogram_title = Text(
            "Spectrogram", font_size=50, color=YELLOW, weight=BOLD,
        ).scale_to_fit_width(8).next_to(spectrogram, UP, buff=0.7)

        self.play(FadeIn(spectrogram_title), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.99))