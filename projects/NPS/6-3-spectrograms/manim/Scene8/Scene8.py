ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def make_spectrogram_cells(self, center, width, height, grey=False, seed=0):
        rng = np.random.default_rng(seed)
        n_cols, n_rows = 10, 8
        cell_w = width / n_cols
        cell_h = height / n_rows
        x_left = center[0] - width / 2
        y_bottom = center[1] - height / 2

        group = VGroup()
        warm_colors = [RED, ORANGE, YELLOW, GOLD]

        for col in range(n_cols):
            center_row = 3 + 2.5 * np.sin(col / 3 + seed)
            strength = rng.uniform(0, 1)
            for row in range(n_rows):
                dist = np.abs(row - center_row)
                op = np.exp(-0.5 * (dist / 1.5) ** 2) * (0.7 + 0.3 * strength) + 0.05
                op = float(np.clip(op, 0.05, 0.95))
                if grey:
                    fill_color = GREY
                    fill_opacity = 0.25
                else:
                    fill_color = warm_colors[(col + row + seed) % 4]
                    fill_opacity = op

                rect = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    fill_color=fill_color,
                    fill_opacity=fill_opacity,
                    stroke_width=0,
                )
                rect.move_to([x_left + col * cell_w + cell_w / 2,
                              y_bottom + row * cell_h + cell_h / 2, 0])
                group.add(rect)
        return group

    def make_corner_brackets(self, rect, length=0.18, color=YELLOW, stroke_width=2.5):
        brackets = VGroup()
        corners = [
            rect.get_corner(UL),
            rect.get_corner(UR),
            rect.get_corner(DL),
            rect.get_corner(DR),
        ]
        for p in corners:
            horiz_dir = RIGHT if p[0] < rect.get_center()[0] else LEFT
            vert_dir = DOWN if p[1] > rect.get_center()[1] else UP
            l1 = Line(start=p, end=p + horiz_dir * length, color=color, stroke_width=stroke_width)
            l2 = Line(start=p, end=p + vert_dir * length, color=color, stroke_width=stroke_width)
            brackets.add(l1, l2)
        return brackets

    def construct(self):
        self.camera.background_color = "#0F1116"

        # Spectrogram layout
        spec_width = 6.0
        spec_height = 3.0
        spec_center = np.array([0, 0.6, 0])

        border = Rectangle(
            width=spec_width,
            height=spec_height,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_color=GREY_B,
            stroke_width=1.2,
        ).move_to(spec_center)

        full_cells = self.make_spectrogram_cells(spec_center, spec_width, spec_height, grey=False, seed=42)
        grey_cells = self.make_spectrogram_cells(spec_center, spec_width, spec_height, grey=True, seed=42)

        spec_cells = full_cells  # will become grey after Transform
        self.add(border, spec_cells)

        # Fixed analysis window overlay
        overlay_rect = Rectangle(
            width=2.4,
            height=1.7,
            stroke_color=YELLOW,
            stroke_width=4.0,
            fill_color=YELLOW,
            fill_opacity=0.15,
        ).move_to(spec_center)

        corner_brackets = self.make_corner_brackets(overlay_rect)
        overlay_group = VGroup(overlay_rect, corner_brackets)

        # Glow rectangle behind overlay (emerges in Beat 3)
        overlay_glow = Rectangle(
            width=overlay_rect.width + 0.25,
            height=overlay_rect.height + 0.25,
            stroke_color=YELLOW,
            stroke_width=8.0,
            stroke_opacity=0.0,
            fill_opacity=0.0,
        ).move_to(spec_center)
        overlay_glow.set_opacity(0.0)

        label_fixed_analysis = Text(
            "Fixed analysis window",
            font_size=22,
            color=WHITE,
        ).move_to([overlay_rect.get_center()[0], border.get_bottom()[1] - 0.35, 0])

        # Beat 2 bands
        vertical_band = Rectangle(
            width=0.45,
            height=spec_height,
            fill_color=ORANGE,
            fill_opacity=0.35,
            stroke_color=YELLOW,
            stroke_width=1.5,
        ).move_to([spec_center[0] - 0.3 * spec_width, spec_center[1], 0])

        horizontal_band = Rectangle(
            width=spec_width,
            height=0.4,
            fill_color=ORANGE,
            fill_opacity=0.35,
            stroke_color=YELLOW,
            stroke_width=1.5,
        ).move_to([spec_center[0], spec_center[1] - 0.25 * spec_height, 0])

        label_when = Text("when", font_size=20, color=YELLOW).next_to(vertical_band, UP, buff=0.15)
        label_freq = Text("what frequency", font_size=20, color=YELLOW).next_to(horizontal_band, RIGHT, buff=0.25)

        # Beat 3 texts
        fixed_window_text = Text("Fixed window", font_size=24, color=YELLOW, weight=BOLD)
        fixed_window_text.next_to(border, DOWN, buff=0.45).align_to(overlay_rect, LEFT)
        stft_text = Text("Short-Time Fourier Transform", font_size=22, color=WHITE)
        stft_text.next_to(fixed_window_text, RIGHT, buff=0.6)
        stft_text.scale_to_fit_width(4.2)

        # Beat 4 axes
        time_res_line = Line(
            start=overlay_rect.get_corner(DL),
            end=overlay_rect.get_corner(DL) + DOWN * 1.2,
            color=GREY_B,
            stroke_width=2.5,
        )
        freq_res_line = Line(
            start=overlay_rect.get_corner(DR),
            end=overlay_rect.get_corner(DR) + DOWN * 1.2,
            color=GREY_B,
            stroke_width=2.5,
        )
        time_res_label = Text("Time resolution", font_size=18, color=WHITE)
        time_res_label.next_to(time_res_line, DOWN, buff=0.15)
        freq_res_label = Text("Frequency resolution", font_size=18, color=WHITE)
        freq_res_label.next_to(freq_res_line, DOWN, buff=0.15)

        # Question mark and text
        question_mark = Text("?", font_size=140, color=YELLOW, weight=BOLD).move_to([0, 0.5, 0])
        question_text = Text(
            "Can we adapt to different types of neural activity?",
            font_size=28,
            color=WHITE,
        ).scale_to_fit_width(10)
        question_text.next_to(question_mark, DOWN, buff=0.4)

        # Wavelet analysis text
        wavelet_text = Text("Wavelet Analysis", font_size=64, color=YELLOW, weight=BOLD).move_to(ORIGIN)

        # Arrow for continuation
        arrow = Arrow(
            start=wavelet_text.get_right() + RIGHT * 0.4,
            end=wavelet_text.get_right() + RIGHT * 3.5,
            stroke_width=3.0,
            color=WHITE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        # Group of everything spectrogram-related for dimming
        scene_group = VGroup(
            border,
            spec_cells,
            overlay_rect,
            corner_brackets,
            overlay_glow,
            vertical_band,
            horizontal_band,
            label_when,
            label_freq,
            fixed_window_text,
            stft_text,
            time_res_line,
            freq_res_line,
            time_res_label,
            freq_res_label,
        )

        # --- Beat 1: 0.00–4.24 ---
        self.play(Transform(spec_cells, grey_cells), run_time=max(0.05, 1.8))
        self.play(
            FadeIn(overlay_group, shift=UP * 0.1),
            FadeIn(label_fixed_analysis, shift=UP * 0.1),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 1.24))

        # --- Beat 2: 4.24–8.10 ---
        self.play(FadeIn(vertical_band), FadeIn(label_when), run_time=max(0.05, 0.4))
        self.play(vertical_band.animate.set_fill(opacity=0.7), run_time=max(0.05, 0.5))
        self.play(vertical_band.animate.set_fill(opacity=0.3), run_time=max(0.05, 0.5))
        self.play(FadeOut(vertical_band), FadeOut(label_when), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.1))
        self.play(FadeIn(horizontal_band), FadeIn(label_freq), run_time=max(0.05, 0.4))
        self.play(horizontal_band.animate.set_fill(opacity=0.7), run_time=max(0.05, 0.5))
        self.play(horizontal_band.animate.set_fill(opacity=0.3), run_time=max(0.05, 0.5))
        self.play(FadeOut(horizontal_band), FadeOut(label_freq), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.16))

        # --- Beat 3: 8.10–14.38 ---
        self.play(FadeOut(label_fixed_analysis), run_time=max(0.05, 0.3))
        self.play(FadeIn(fixed_window_text), run_time=max(0.05, 0.6))
        self.play(FadeIn(stft_text), run_time=max(0.05, 0.6))
        self.play(
            overlay_rect.animate.set_stroke(YELLOW, width=6.0).set_fill(opacity=0.25),
            overlay_glow.animate.set_opacity(0.6),
            run_time=max(0.05, 0.7),
        )
        self.play(
            overlay_rect.animate.set_stroke(YELLOW, width=4.0).set_fill(opacity=0.15),
            overlay_glow.animate.set_opacity(0.3),
            run_time=max(0.05, 0.7),
        )
        self.play(
            overlay_rect.animate.set_stroke(YELLOW, width=6.0).set_fill(opacity=0.25),
            overlay_glow.animate.set_opacity(0.6),
            run_time=max(0.05, 0.7),
        )
        self.play(
            overlay_rect.animate.set_stroke(YELLOW, width=4.0).set_fill(opacity=0.15),
            overlay_glow.animate.set_opacity(0.3),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 1.98))

        # --- Beat 4: 14.38–20.48 ---
        self.play(
            FadeIn(time_res_line),
            FadeIn(freq_res_line),
            FadeIn(time_res_label),
            FadeIn(freq_res_label),
            run_time=max(0.05, 0.8),
        )
        self.play(
            time_res_line.animate.scale(1.3, about_point=time_res_line.get_start()),
            freq_res_line.animate.scale(0.7, about_point=freq_res_line.get_start()),
            run_time=max(0.05, 1.0),
        )
        self.play(
            time_res_line.animate.scale(1.0 / 1.3, about_point=time_res_line.get_start()),
            freq_res_line.animate.scale(1.0 / 0.7, about_point=freq_res_line.get_start()),
            run_time=max(0.05, 1.0),
        )
        self.play(
            time_res_line.animate.set_stroke(ORANGE, width=4.0).set_opacity(1),
            freq_res_line.animate.set_stroke(ORANGE, width=1.5).set_opacity(0.5),
            run_time=max(0.05, 0.6),
        )
        self.play(
            time_res_line.animate.set_stroke(GREY_B, width=2.5).set_opacity(1),
            freq_res_line.animate.set_stroke(GREY_B, width=2.5).set_opacity(1),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 2.10))

        # --- Beat 5: 20.48–25.32 ---
        self.play(scene_group.animate.set_opacity(0.15), run_time=max(0.05, 1.2))
        self.play(FadeIn(question_mark, scale=0.8), run_time=max(0.05, 0.8))
        self.play(FadeIn(question_text), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 2.04))

        # --- Beat 6: 25.32–28.08 ---
        self.play(FadeOut(question_mark), FadeOut(question_text), run_time=max(0.05, 0.8))
        self.play(FadeIn(wavelet_text, scale=0.9), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.16))

        # --- Beat 7: 28.08–31.32 ---
        self.play(Create(arrow), run_time=max(0.05, 1.0))
        self.play(arrow.animate.set_stroke(YELLOW, width=5.0).set_opacity(1), run_time=max(0.05, 0.4))
        self.play(arrow.animate.set_stroke(WHITE, width=3.0), run_time=max(0.05, 0.4))
        self.play(FadeOut(wavelet_text, arrow, scene_group), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.64))