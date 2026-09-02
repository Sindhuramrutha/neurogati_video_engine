ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(Scene):
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
                intensity = np.exp(-((freq - center_freq) ** 2) / (2 * 0.65 ** 2))
                intensity2 = 0.55 * np.exp(
                    -((freq - (center_freq + 5 * np.exp(-((t_val - 0.7) / 0.2) ** 2))) ** 2)
                    / (2 * 0.5 ** 2)
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

        # --- Build the already-on-screen spectrogram + faint axes + dim colour bar ---
        spec_image = self.build_spectrogram()
        spec_image.move_to(np.array([0, 0.6, 0]))
        spec_image.set_z_index(0)

        spec_left = spec_image.get_left()[0]
        spec_right = spec_image.get_right()[0]
        spec_top = spec_image.get_top()[1]
        spec_bottom = spec_image.get_bottom()[1]

        x_axis_line = Line(
            np.array([spec_left - 0.2, spec_bottom - 0.15, 0]),
            np.array([spec_right + 0.2, spec_bottom - 0.15, 0]),
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.35,
        )
        y_axis_line = Line(
            np.array([spec_left - 0.15, spec_bottom - 0.2, 0]),
            np.array([spec_left - 0.15, spec_top + 0.2, 0]),
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.35,
        )
        x_axis_line.set_z_index(2)
        y_axis_line.set_z_index(2)

        gradient_colors = [BLUE, BLUE, TEAL, TEAL, GREEN, GREEN, YELLOW, YELLOW, GOLD, GOLD, ORANGE, RED]
        colorbar = VGroup(
            *[
                Rectangle(
                    width=0.22,
                    height=3.2 / len(gradient_colors),
                    fill_color=c,
                    fill_opacity=1,
                    stroke_width=0,
                )
                for c in gradient_colors
            ]
        )
        colorbar.arrange(DOWN, buff=0)
        colorbar.next_to(spec_image, RIGHT, buff=0.35)
        colorbar.set_opacity(0.3)
        colorbar.set_z_index(2)

        # Cool overlay and warm patches are created now but invisible until beat 10
        cool_overlay = Rectangle(
            width=spec_image.width,
            height=spec_image.height,
            fill_color=BLUE,
            fill_opacity=0,
            stroke_width=0,
        ).move_to(spec_image.get_center())
        cool_overlay.set_z_index(1)

        warm_patch_group = VGroup(
            Ellipse(width=1.6, height=0.9, fill_color=YELLOW, fill_opacity=0, stroke_width=0)
            .move_to(np.array([spec_left + 1.4, spec_bottom + 1.9, 0])),
            Ellipse(width=1.2, height=0.8, fill_color=GOLD, fill_opacity=0, stroke_width=0)
            .move_to(np.array([spec_image.get_center()[0], spec_bottom + 1.2, 0])),
            Ellipse(width=1.4, height=0.9, fill_color=ORANGE, fill_opacity=0, stroke_width=0)
            .move_to(np.array([spec_right - 1.3, spec_bottom + 1.7, 0])),
        ).set_z_index(5)

        self.add(spec_image, x_axis_line, y_axis_line, colorbar, cool_overlay, warm_patch_group)

        # --- 1. 0.00–2.00 — spectrogram rests, components introduced ---
        self.wait(max(0.05, 2.00))

        # --- 2. 2.84–4.08 — horizontal axis brightens, Time label + arrow appear ---
        self.wait(max(0.05, 0.84))

        time_label = Text("Time", font_size=28, color=WHITE).next_to(x_axis_line, DOWN, buff=0.15)
        time_label.set_z_index(2)

        time_arrow = Arrow(
            np.array([spec_left, x_axis_line.get_center()[1] + 0.12, 0]),
            np.array([spec_right, x_axis_line.get_center()[1] + 0.12, 0]),
            buff=0,
            color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.65,
            max_tip_length_to_length_ratio=0.08,
        )
        time_arrow.set_z_index(2)

        self.play(
            x_axis_line.animate.set_stroke(opacity=1.0),
            FadeIn(time_label),
            FadeIn(time_arrow),
            y_axis_line.animate.set_stroke(opacity=0.20),
            run_time=max(0.05, 1.24),
        )

        # --- 3. 4.82–6.64 — gentle sweep along time, marker dot begins moving ---
        self.wait(max(0.05, 0.74))

        x_highlight = Rectangle(
            width=x_axis_line.get_length() + 0.3,
            height=0.28,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=0,
        ).move_to(x_axis_line.get_center())
        x_highlight.set_z_index(1)

        marker_dot = Dot(
            point=np.array([spec_left, x_axis_line.get_center()[1], 0]),
            radius=0.09,
            color=YELLOW,
        )
        marker_dot.set_z_index(6)

        time_sweep_arrow = Arrow(
            LEFT * 0.2,
            RIGHT * 0.2,
            buff=0,
            color=ORANGE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.35,
        )
        time_sweep_arrow.move_to(np.array([spec_left, x_axis_line.get_center()[1] + 0.12, 0]))
        time_sweep_arrow.set_z_index(7)

        self.play(FadeIn(x_highlight), FadeIn(marker_dot), FadeIn(time_sweep_arrow), run_time=max(0.05, 0.30))

        mid_progress = 0.35
        mid_x = spec_left + mid_progress * (spec_right - spec_left)
        marker_mid = np.array([mid_x, x_axis_line.get_center()[1], 0])
        sweep_mid = np.array([mid_x, x_axis_line.get_center()[1] + 0.12, 0])

        self.play(
            marker_dot.animate.move_to(marker_mid),
            time_sweep_arrow.animate.move_to(sweep_mid),
            run_time=max(0.05, 1.52),
        )

        # --- 4. 7.04–11.32 — arrow completes sweep, marker travels full horizontal extent ---
        self.wait(max(0.05, 0.40))

        marker_end = np.array([spec_right, x_axis_line.get_center()[1], 0])
        sweep_end = np.array([spec_right, x_axis_line.get_center()[1] + 0.12, 0])

        self.play(
            marker_dot.animate.move_to(marker_end),
            time_sweep_arrow.animate.move_to(sweep_end),
            run_time=max(0.05, 4.28),
        )

        # --- 5. 12.08–14.06 — switch attention to vertical axis ---
        self.wait(max(0.05, 0.76))

        freq_text = Text("Frequency", font_size=24, color=WHITE)
        hz_text = Text("(Hz)", font_size=24, color=GOLD)
        freq_label_group = VGroup(freq_text, hz_text).arrange(RIGHT, buff=0.12)
        freq_label_group.rotate(PI / 2)
        freq_label_group.next_to(y_axis_line, LEFT, buff=0.18)
        freq_label_group.set_z_index(2)

        vertical_arrow = Arrow(
            np.array([spec_left + 0.25, spec_bottom + 0.1, 0]),
            np.array([spec_left + 0.25, spec_top - 0.1, 0]),
            buff=0,
            color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.65,
            max_tip_length_to_length_ratio=0.08,
        )
        vertical_arrow.set_z_index(2)

        self.play(
            FadeOut(x_highlight),
            FadeOut(time_arrow),
            FadeOut(time_sweep_arrow),
            FadeOut(marker_dot),
            y_axis_line.animate.set_stroke(opacity=1.0),
            FadeIn(freq_label_group),
            FadeIn(vertical_arrow),
            run_time=max(0.05, 1.98),
        )

        # --- 6. 14.84–18.48 — vertical sweep and (Hz) pulse ---
        self.wait(max(0.05, 0.78))

        vertical_sweep_arrow = Arrow(
            DOWN * 0.2,
            UP * 0.2,
            buff=0,
            color=ORANGE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.35,
        )
        vertical_sweep_arrow.move_to(np.array([spec_left + 0.25, spec_bottom + 0.1, 0]))
        vertical_sweep_arrow.set_z_index(7)

        self.play(FadeIn(vertical_sweep_arrow), run_time=max(0.05, 0.25))
        self.play(
            vertical_sweep_arrow.animate.move_to(np.array([spec_left + 0.25, spec_top - 0.1, 0])),
            run_time=max(0.05, 2.65),
        )
        self.play(Indicate(hz_text, color=YELLOW, scale_factor=1.3), run_time=max(0.05, 0.74))

        # --- 7. 19.06–21.70 — low frequency marker appears near bottom ---
        self.wait(max(0.05, 0.58))

        low_freq_label = Text("Low frequency", font_size=17, color=GREY_B)
        low_freq_label.move_to(
            np.array([y_axis_line.get_left()[0] - 0.9, y_axis_line.get_bottom()[1] + 0.22, 0])
        )

        low_highlight = Line(
            y_axis_line.get_bottom(),
            np.array([y_axis_line.get_center()[0], spec_bottom + 0.7, 0]),
            color=YELLOW,
            stroke_width=7,
            stroke_opacity=0.35,
        )
        low_highlight.set_z_index(1)

        self.play(FadeIn(low_freq_label), FadeIn(low_highlight), run_time=max(0.05, 2.64))

        # --- 8. 22.06–24.30 — high frequency marker appears near top ---
        self.wait(max(0.05, 0.36))

        high_freq_label = Text("High frequency", font_size=17, color=GREY_B)
        high_freq_label.move_to(
            np.array([y_axis_line.get_left()[0] - 0.9, y_axis_line.get_top()[1] - 0.22, 0])
        )

        high_highlight = Line(
            np.array([y_axis_line.get_center()[0], spec_top - 1.2, 0]),
            y_axis_line.get_top(),
            color=YELLOW,
            stroke_width=7,
            stroke_opacity=0.35,
        )
        high_highlight.set_z_index(1)

        self.play(FadeIn(high_freq_label), FadeIn(high_highlight), run_time=max(0.05, 2.24))

        # --- 9. 24.86–26.60 — vertical emphasis rests, colour bar brightens ---
        self.wait(max(0.05, 0.56))

        colour_intensity_label = Text("Colour intensity", font_size=24, color=WHITE)
        colour_intensity_label.next_to(colorbar, RIGHT, buff=0.22)
        colour_intensity_label.set_z_index(2)

        self.play(
            FadeOut(vertical_arrow),
            FadeOut(vertical_sweep_arrow),
            FadeOut(low_highlight),
            FadeOut(high_highlight),
            low_freq_label.animate.set_opacity(0.65),
            high_freq_label.animate.set_opacity(0.65),
            colorbar.animate.set_opacity(1.0),
            FadeIn(colour_intensity_label),
            run_time=max(0.05, 1.74),
        )

        # --- 10. 27.36–32.98 — colour meaning: warm strong regions, cool weak regions ---
        self.wait(max(0.05, 0.76))

        self.play(
            cool_overlay.animate.set_fill(opacity=0.35),
            warm_patch_group.animate.set_fill(opacity=0.85),
            run_time=max(0.05, 3.20),
        )
        self.play(warm_patch_group.animate.set_fill(opacity=1.0), run_time=max(0.05, 1.20))
        self.play(warm_patch_group.animate.set_fill(opacity=0.80), run_time=max(0.05, 1.22))

        # --- 11. 33.62–37.34 — Weak/Strong labels appear, warm regions pulse ---
        self.wait(max(0.05, 0.64))

        weak_label = Text("Weak", font_size=17, color=GREY_B).next_to(colorbar, DOWN, buff=0.08)
        strong_label = Text("Strong", font_size=17, color=WHITE).next_to(colorbar, UP, buff=0.08)

        self.play(
            FadeIn(weak_label),
            FadeIn(strong_label),
            warm_patch_group.animate.set_fill(opacity=0.95),
            run_time=max(0.05, 1.30),
        )
        self.play(warm_patch_group.animate.set_fill(opacity=1.0), run_time=max(0.05, 1.20))
        self.play(warm_patch_group.animate.set_fill(opacity=0.82), run_time=max(0.05, 1.22))

        # --- 12. 38.20–40.94 — cool regions dim further, warm regions settle ---
        self.wait(max(0.05, 0.86))

        self.play(
            cool_overlay.animate.set_fill(opacity=0.55),
            warm_patch_group.animate.set_fill(opacity=0.85),
            run_time=max(0.05, 2.00),
        )
        self.wait(max(0.05, 0.74))

        # --- 13. 40.94–41.75 — fully annotated spectrogram holds ---
        self.wait(max(0.05, 0.81))