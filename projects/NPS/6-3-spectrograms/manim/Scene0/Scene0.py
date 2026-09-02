ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene0(Scene):
    def wave_func(
        self,
        t,
        amp1=0.55,
        amp2=0.35,
        amp3=0.25,
        freq1=2.5,
        freq2=4.8,
        freq3=0.8,
        phase2=1.2,
        phase3=0.5,
        extra_amp=0.0,
        extra_freq=8.0,
    ):
        return (
            1.6
            + amp1 * np.sin(freq1 * t)
            + amp2 * np.sin(freq2 * t + phase2)
            + amp3 * np.sin(freq3 * t + phase3)
            + extra_amp * np.sin(extra_freq * t)
        )

    def make_wave(self, color=BLUE_B, amp1=0.55, amp2=0.35, amp3=0.25, **kwargs):
        def path(t):
            y = self.wave_func(t, amp1=amp1, amp2=amp2, amp3=amp3, **kwargs)
            return np.array([t, y, 0.0])

        return ParametricFunction(path, t_range=[-5, 5], color=color, stroke_width=4)

    def make_spectrum(self, color, origin_x, origin_y, width=1.2, height=2.0):
        spec = VGroup()
        rect = Rectangle(
            width=width,
            height=height,
            fill_color=color,
            fill_opacity=0.18,
            stroke_color=color,
            stroke_width=1.5,
        )
        horiz_axis = Line(
            LEFT * (width / 2 - 0.15), RIGHT * (width / 2 - 0.15), color=WHITE, stroke_width=2
        )
        vert_axis = Line(
            DOWN * (height / 2 - 0.15), UP * (height / 2 - 0.15), color=WHITE, stroke_width=2
        )
        curve = ParametricFunction(
            lambda t: np.array(
                [
                    0.35 * np.exp(-((t + 0.4) / 0.35) ** 2)
                    + 0.45 * np.exp(-((t - 0.2) / 0.3) ** 2),
                    t,
                    0.0,
                ]
            ),
            t_range=[-height / 2 + 0.2, height / 2 - 0.2],
            color=WHITE,
            stroke_width=2,
        )
        spec.add(rect, horiz_axis, vert_axis, curve)
        spec.move_to(np.array([origin_x, origin_y, 0.0]))
        return spec

    def make_mini_spec(self, x, color, width, height, y=-1.5):
        rect = Rectangle(
            width=width,
            height=height,
            fill_color=color,
            fill_opacity=0.9,
            stroke_color=color,
            stroke_width=0.5,
        )
        line = Line(UP * height * 0.3, DOWN * height * 0.3, color=WHITE, stroke_width=1.5)
        group = VGroup(rect, line)
        group.move_to(np.array([x, y, 0.0]))
        return group

    def build_spectrogram(self):
        n_cols = 36
        n_bins = 20
        col_width = 0.15
        row_height = 3.0 / n_bins
        img = VGroup()
        for i in range(n_cols):
            t_val = i / (n_cols - 1)
            center_freq = 2.0 + 2.5 * t_val + 1.8 * np.sin(2 * np.pi * (t_val - 0.2))
            column = VGroup()
            for j in range(n_bins):
                freq = 1.0 + (8.0 - 1.0) * j / (n_bins - 1)
                intensity = np.exp(-((freq - center_freq) ** 2) / (2 * 0.65**2))
                intensity2 = 0.55 * np.exp(
                    -((freq - (center_freq + 5 * np.exp(-((t_val - 0.7) / 0.2) ** 2))) ** 2)
                    / (2 * 0.5**2)
                )
                intensity = max(intensity, intensity2)
                color_idx = int(min(1.0, intensity) * 6)
                color = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED][color_idx]
                rect = Rectangle(
                    width=col_width,
                    height=row_height,
                    fill_color=color,
                    fill_opacity=intensity,
                    stroke_width=0,
                )
                rect.move_to(np.array([0, -1.5 + row_height * (j + 0.5), 0]))
                column.add(rect)
            column.move_to(np.array([-(n_cols - 1) * col_width / 2 + i * col_width, 0, 0]))
            img.add(column)
        return img

    def construct(self):
        self.camera.background_color = "#0F1116"

        # 1. 0.00-1.10 — blank dark background, one pale blue-grey waveform centred high.
        self.signal = self.make_wave(color=BLUE_B)
        self.play(FadeIn(self.signal), run_time=max(0.05, 1.1))

        # 2. 1.10-3.60 — waveform title and abbreviation.
        title = Text("Short-Time Fourier Transform", font_size=34, color=WHITE)
        title.next_to(self.signal, DOWN, buff=0.6)
        abbr = Text("STFT", font_size=26, color=GREY_B)
        abbr.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), run_time=max(0.05, 1.1))
        self.play(FadeIn(abbr), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.7))

        # 3. 3.60-7.00 — waveform highlights, bracket moves in short equal steps.
        self.play(self.signal.animate.set_color(YELLOW), run_time=max(0.05, 0.3))

        positions3 = np.linspace(-4.2, 3.8, 7)
        step3 = float(positions3[1] - positions3[0])
        bracket = Line(
            [positions3[0], 0.4, 0.0],
            [positions3[0], 2.8, 0.0],
            color=YELLOW,
            stroke_width=6,
        )
        self.play(Create(bracket), run_time=max(0.05, 0.3))

        per_iter3 = 0.40
        for i, pos in enumerate(positions3):
            if i > 0:
                self.play(bracket.animate.shift(RIGHT * step3), run_time=max(0.05, 0.16))
            flash_line = Line(
                [pos, 0.4, 0.0],
                [pos, 2.8, 0.0],
                color=WHITE,
                stroke_width=2,
            )
            self.play(FadeIn(flash_line), run_time=max(0.05, 0.08))
            self.play(FadeOut(flash_line), run_time=max(0.05, 0.08))
            if i < len(positions3) - 1:
                self.wait(max(0.05, 0.08))

        # 4. 7.00-10.30 — pulsing analysis windows; windows visibly overlap.
        self.window_rects = VGroup()
        self.overlap_bands = VGroup()

        positions4 = np.array([-4.5, -3.6, -2.7, -1.8, -0.9, 0.0, 0.9])
        step4 = 0.9
        win_w = 1.2

        self.play(bracket.animate.set_x(positions4[0]), run_time=max(0.05, 0.2))

        for i, pos in enumerate(positions4):
            if i > 0:
                self.play(bracket.animate.shift(RIGHT * step4), run_time=max(0.05, 0.08))

                prev_right = positions4[i - 1] + win_w
                new_left = pos
                overlap_width = prev_right - new_left
                overlap_band = Rectangle(
                    width=overlap_width,
                    height=0.7,
                    fill_color=WHITE,
                    fill_opacity=0.25,
                    stroke_width=0,
                ).move_to(np.array([(prev_right + new_left) / 2, 1.6, 0.0]))
                self.add(overlap_band)
                self.overlap_bands.add(overlap_band)
                self.play(FadeIn(overlap_band), run_time=max(0.05, 0.05))
                self.play(FadeOut(overlap_band), run_time=max(0.05, 0.05))

            rect = Rectangle(
                width=win_w,
                height=2.4,
                color=WHITE,
                stroke_opacity=0.25,
                fill_opacity=0,
            ).move_to(np.array([pos + win_w / 2, 1.6, 0.0]))
            self.play(GrowFromCenter(rect), run_time=max(0.05, 0.12))
            self.window_rects.add(rect)
            self.play(rect.animate.set_stroke(opacity=0.55, width=3), run_time=max(0.05, 0.08))
            self.play(rect.animate.set_stroke(opacity=0.15), run_time=max(0.05, 0.08))

        self.wait(max(0.05, 0.06))

        # 5. 10.30-13.10 — remove window indicators; conventional FT badge + summary curve.
        self.play(
            FadeOut(title),
            FadeOut(abbr),
            FadeOut(bracket),
            FadeOut(self.window_rects),
            FadeOut(self.overlap_bands),
            run_time=max(0.05, 0.4),
        )

        ft_badge_rect = RoundedRectangle(
            width=1.0,
            height=0.6,
            corner_radius=0.2,
            fill_color=BLUE,
            fill_opacity=0.85,
            stroke_color=WHITE,
            stroke_width=2,
        )
        ft_badge_text = Text("FT", font_size=24, color=WHITE).move_to(ft_badge_rect)
        ft_badge_group = VGroup(ft_badge_rect, ft_badge_text)

        ft_curve = ParametricFunction(
            lambda t: np.array(
                [
                    t / 1.5,
                    0.5 * np.exp(-((t - 0.5) / 0.35) ** 2)
                    + 0.35 * np.exp(-((t - 1.0) / 0.4) ** 2),
                    0.0,
                ]
            ),
            t_range=[0, 1.5],
            color=BLUE_B,
            stroke_width=4,
        )
        ft_curve.scale_to_fit_width(1.6)
        ft_curve.next_to(ft_badge_group, RIGHT, buff=0.25)

        ft_text = Text(
            "conventional FT: frequencies present overall",
            font_size=18,
            color=GREY_B,
        )
        ft_text.next_to(ft_curve, RIGHT, buff=0.35)
        ft_group_full = VGroup(ft_badge_group, ft_curve, ft_text)
        ft_group_full.move_to(LEFT * 4.2 + DOWN * 2.2)

        self.play(
            GrowFromCenter(ft_badge_group),
            Write(ft_curve),
            FadeIn(ft_text),
            run_time=max(0.05, 1.2),
        )
        self.play(ft_group_full.animate.set_opacity(0.55), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.7))

        # 6. 13.10-16.10 — STFT badge, time/frequency ticks, labels highlighted.
        self.play(
            ft_group_full.animate.scale(0.55).move_to(LEFT * 5.5 + DOWN * 3.0),
            self.signal.animate.set_color(YELLOW).set_stroke(width=5),
            run_time=max(0.05, 0.8),
        )

        stft_badge_rect = RoundedRectangle(
            width=1.2,
            height=0.55,
            corner_radius=0.15,
            fill_color=GOLD,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=2,
        )
        stft_badge_text = Text("STFT", font_size=22, color=WHITE).move_to(stft_badge_rect)
        stft_badge = VGroup(stft_badge_rect, stft_badge_text)
        stft_badge.next_to(self.signal, LEFT, buff=0.5).shift(UP * 0.6)
        self.play(GrowFromCenter(stft_badge), run_time=max(0.05, 0.7))

        axis_origin = np.array([2.8, 0.4, 0.0])
        time_axis = Line(
            axis_origin + LEFT * 0.45,
            axis_origin + RIGHT * 0.45,
            color=WHITE,
            stroke_width=3,
        )
        freq_axis = Line(
            axis_origin + DOWN * 0.45,
            axis_origin + UP * 0.45,
            color=WHITE,
            stroke_width=3,
        )
        time_label = Text("time", font_size=20, color=WHITE).next_to(time_axis, DOWN, buff=0.1)
        freq_label = Text("frequency", font_size=20, color=WHITE).next_to(freq_axis, LEFT, buff=0.1)
        axis_group = VGroup(time_axis, freq_axis, time_label, freq_label)

        self.play(
            Write(time_axis),
            Write(freq_axis),
            FadeIn(time_label),
            FadeIn(freq_label),
            run_time=max(0.05, 0.5),
        )
        self.play(Indicate(time_label, color=YELLOW), run_time=max(0.05, 0.5))
        self.play(Indicate(freq_label, color=YELLOW), run_time=max(0.05, 0.5))

        # 7. 16.10-20.20 — the waveform itself changes shape in place.
        slower_wave = self.make_wave(
            color=YELLOW,
            amp1=0.75,
            amp2=0.2,
            amp3=0.2,
            freq1=1.2,
            freq2=2.5,
            freq3=0.6,
        )
        faster_wave = self.make_wave(
            color=YELLOW,
            amp1=0.5,
            amp2=0.35,
            amp3=0.25,
            freq1=5.0,
            freq2=6.5,
            freq3=1.0,
        )
        super_wave = self.make_wave(
            color=YELLOW,
            amp1=0.45,
            amp2=0.25,
            amp3=0.25,
            freq1=5.0,
            freq2=8.0,
            freq3=1.2,
            extra_amp=0.3,
            extra_freq=12.0,
        )

        self.play(
            Transform(self.signal, slower_wave),
            time_label.animate.set_color(YELLOW),
            freq_label.animate.set_color(YELLOW),
            run_time=max(0.05, 1.4),
        )
        self.play(
            Transform(self.signal, faster_wave),
            time_label.animate.set_color(YELLOW),
            freq_label.animate.set_color(YELLOW),
            run_time=max(0.05, 1.4),
        )
        self.play(Transform(self.signal, super_wave), run_time=max(0.05, 1.3))

        # 8. 20.20-26.90 — waveform freezes, warning flash, problem label.
        warning_bottom = Rectangle(
            width=14,
            height=1.2,
            fill_color=YELLOW,
            fill_opacity=0.0,
            stroke_width=0,
        ).to_edge(DOWN, buff=0)
        self.add(warning_bottom)

        self.wait(max(0.05, 0.3))
        self.play(warning_bottom.animate.set_fill(opacity=0.4), run_time=max(0.05, 0.35))
        self.play(warning_bottom.animate.set_fill(opacity=0.1), run_time=max(0.05, 0.35))
        self.play(warning_bottom.animate.set_fill(opacity=0.45), run_time=max(0.05, 0.25))
        self.play(warning_bottom.animate.set_fill(opacity=0.0), run_time=max(0.05, 0.25))

        problem_text = Text("A practical problem", font_size=42, color=YELLOW)
        problem_text.next_to(self.signal, DOWN, buff=0.9)
        self.play(Write(problem_text), run_time=max(0.05, 2.0))
        self.play(problem_text.animate.scale(1.1), run_time=max(0.05, 0.5))
        self.play(problem_text.animate.scale(1 / 1.1), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.2))

        # 9. 26.90-32.50 — waveform moves up, first spectrum appears below.
        self.play(
            FadeOut(problem_text),
            FadeOut(stft_badge),
            FadeOut(axis_group),
            FadeOut(ft_group_full),
            run_time=max(0.05, 0.4),
        )
        self.play(self.signal.animate.scale(0.75).move_to(UP * 2.2), run_time=max(0.05, 1.3))

        first_spec = self.make_spectrum(
            color=BLUE, origin_x=-3.5, origin_y=-1.5, width=1.2, height=2.0
        )
        self.play(FadeIn(first_spec), run_time=max(0.05, 1.2))

        connector = Line(
            np.array([-3.5, 2.8, 0.0]),
            np.array([-3.5, -0.5, 0.0]),
            color=WHITE,
            stroke_width=2,
        )
        self.play(Create(connector), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.7))

        # 10. 32.50-37.40 — many coloured spectra stream in left-to-right.
        colors_cycle = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED]
        n_spec = 45
        start_x = -2.6
        gaps = np.linspace(0.30, 0.06, n_spec - 1)
        xs = [start_x]
        for gap in gaps:
            xs.append(xs[-1] + gap)

        new_spec_list = []
        for i, xpos in enumerate(xs[1:], start=1):
            color = colors_cycle[i % len(colors_cycle)]
            width = max(0.12, min(0.30, gap * 0.7))
            new_spec_list.append(
                self.make_mini_spec(xpos, color=color, width=width, height=1.8)
            )

        all_specs = [first_spec] + new_spec_list
        spectra_group = VGroup(*all_specs)

        animations = [FadeIn(s, shift=RIGHT * 0.4) for s in new_spec_list]
        self.play(LaggedStart(*animations, lag_ratio=0.04), run_time=max(0.05, 4.9))

        # 11. 37.40-40.80 — crowded row jitters, question mark and caption appear.
        self.play(*[spec.animate.stretch(0.7, 0) for spec in all_specs], run_time=max(0.05, 1.0))

        jitter_specs = [all_specs[i] for i in range(0, len(all_specs), 6)]
        self.play(*[spec.animate.shift(UP * 0.04) for spec in jitter_specs], run_time=max(0.05, 0.25))
        self.play(*[spec.animate.shift(DOWN * 0.08) for spec in jitter_specs], run_time=max(0.05, 0.25))
        self.play(*[spec.animate.shift(UP * 0.04) for spec in jitter_specs], run_time=max(0.05, 0.25))

        question_mark = Text("?", font_size=80, color=YELLOW)
        question_mark.next_to(spectra_group, RIGHT, buff=0.4)
        self.play(FadeIn(question_mark), run_time=max(0.05, 0.6))
        self.play(question_mark.animate.scale(1.2), run_time=max(0.05, 0.25))
        self.play(question_mark.animate.scale(1 / 1.2), run_time=max(0.05, 0.25))

        read_caption = Text("how do we read this?", font_size=26, color=WHITE)
        read_caption.next_to(question_mark, DOWN, buff=0.3)
        self.play(GrowFromCenter(read_caption), run_time=max(0.05, 0.55))

        # 12. 40.80-45.20 — question/caption vanish, clean highlight is drawn.
        self.play(FadeOut(question_mark), FadeOut(read_caption), run_time=max(0.05, 0.5))

        highlight = SurroundingRectangle(
            spectra_group, color=WHITE, buff=0.2, corner_radius=0.2, stroke_width=2
        )
        self.play(Create(highlight), run_time=max(0.05, 0.9))

        self.play(*[spec.animate.set_fill(opacity=0.95) for spec in all_specs], run_time=max(0.05, 0.5))
        self.play(*[spec.animate.set_fill(opacity=0.8) for spec in all_specs], run_time=max(0.05, 0.5))
        self.play(*[spec.animate.set_fill(opacity=0.95) for spec in all_specs], run_time=max(0.05, 0.5))
        self.play(*[spec.animate.set_fill(opacity=0.8) for spec in all_specs], run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.0))

        # 13. 45.20-49.30 — highlight tightens; spectra merge into one continuous image.
        spectrogram_img = self.build_spectrogram()
        spectrogram_img.move_to(DOWN * 0.6)
        new_highlight = SurroundingRectangle(
            spectrogram_img, color=WHITE, buff=0.2, corner_radius=0.2, stroke_width=2
        )

        self.play(
            Transform(highlight, new_highlight),
            FadeOut(spectra_group),
            FadeIn(spectrogram_img),
            connector.animate.set_opacity(0.0),
            run_time=max(0.05, 4.1),
        )

        # 14. 49.30-52.30 — spectrogram resolves; frequency/time labels and magnitude bar.
        time_label_final = Text("time", font_size=24, color=WHITE)
        time_label_final.next_to(spectrogram_img, DOWN, buff=0.25)

        freq_label_final = Text("frequency", font_size=24, color=WHITE)
        freq_label_final.rotate(PI / 2)
        freq_label_final.next_to(spectrogram_img, LEFT, buff=0.2)

        gradient_colors = [BLUE, BLUE, TEAL, TEAL, GREEN, GREEN, YELLOW, YELLOW, GOLD, GOLD, ORANGE, RED]
        colorbar = VGroup(
            *[
                Rectangle(width=0.25, height=3.2 / len(gradient_colors),
                          fill_color=c, fill_opacity=1, stroke_width=0)
                for c in gradient_colors
            ]
        )
        colorbar.arrange(DOWN, buff=0)
        colorbar.next_to(spectrogram_img, RIGHT, buff=0.4)

        weak_label = Text("weak", font_size=16, color=GREY_B)
        weak_label.next_to(colorbar, DOWN, buff=0.05)
        strong_label = Text("strong", font_size=16, color=WHITE)
        strong_label.next_to(colorbar, UP, buff=0.05)

        magnitude_label = Text("magnitude", font_size=18, color=WHITE)
        magnitude_label.rotate(PI / 2)
        magnitude_label.next_to(colorbar, RIGHT, buff=0.15)

        self.play(
            FadeIn(time_label_final),
            FadeIn(freq_label_final),
            FadeIn(colorbar),
            FadeIn(weak_label),
            FadeIn(strong_label),
            FadeIn(magnitude_label),
            run_time=max(0.05, 1.3),
        )
        self.play(Indicate(time_label_final, color=YELLOW), run_time=max(0.05, 0.4))
        self.play(Indicate(freq_label_final, color=YELLOW), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.9))

        # 15. 52.30-53.10 — single clean word "Spectrogram".
        spectrogram_caption = Text("Spectrogram", font_size=38, color=WHITE)
        spectrogram_caption.next_to(time_label_final, DOWN, buff=0.45)
        self.play(FadeIn(spectrogram_caption), run_time=max(0.05, 0.8))

        # 16. 53.10-54.35 — final rest.
        self.wait(max(0.05, 1.25))