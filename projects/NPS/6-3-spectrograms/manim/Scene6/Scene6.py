ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def make_check_mark(self, center):
        p1 = center + LEFT * 0.17 + DOWN * 0.04
        p2 = center + LEFT * 0.01 + UP * 0.11
        p3 = center + RIGHT * 0.22 + DOWN * 0.13
        mark = VGroup(
            Line(p1, p2, color=GREEN, stroke_width=7),
            Line(p2, p3, color=GREEN, stroke_width=7),
        )
        return mark

    def build_prev_grid(self):
        panel_w, panel_h = 5.6, 2.8
        gap_x, gap_y = 0.8, 0.8
        centers = {
            "eeg": np.array([-(panel_w + gap_x) / 2, (panel_h + gap_y) / 2, 0]),
            "emg": np.array([(panel_w + gap_x) / 2, (panel_h + gap_y) / 2, 0]),
            "bci": np.array([-(panel_w + gap_x) / 2, -(panel_h + gap_y) / 2, 0]),
            "er": np.array([(panel_w + gap_x) / 2, -(panel_h + gap_y) / 2, 0]),
        }
        labels = {
            "eeg": "EEG Analysis",
            "emg": "EMG Analysis",
            "bci": "Brain–Computer Interfaces",
            "er": "Event-Related Studies",
        }
        colors = {"eeg": ORANGE, "emg": TEAL, "bci": GOLD, "er": PURPLE}

        group = VGroup()
        for key, center in centers.items():
            panel = RoundedRectangle(
                width=panel_w,
                height=panel_h,
                corner_radius=0.14,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_color=GREY_B,
                stroke_width=1.5,
            )
            panel.move_to(center)

            label = Text(labels[key], font_size=20, color=WHITE, weight=BOLD)
            label.scale_to_fit_width(panel_w - 0.6)
            label.move_to(panel.get_top() + DOWN * 0.32)

            spec = Rectangle(
                width=panel_w - 0.9,
                height=1.5,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_color=GREY_B,
                stroke_width=0.8,
            )
            spec.move_to(panel.get_center() + DOWN * 0.02)

            group.add(panel, label, spec)

            if key == "er":
                bar = Rectangle(
                    width=spec.width - 0.3,
                    height=0.28,
                    fill_color=PURPLE,
                    fill_opacity=0.45,
                    stroke_width=0,
                ).move_to(spec.get_center() + UP * 0.2)
                group.add(bar)
                stim_left = spec.get_left() + RIGHT * 0.7 + UP * 0.42
                stim_right = spec.get_left() + RIGHT * 0.7 + UP * 0.92
                stim_line = Line(stim_left, stim_right, color=YELLOW, stroke_width=2)
                group.add(stim_line)
            else:
                bar = Rectangle(
                    width=spec.width - 0.3,
                    height=0.20 if key != "bci" else 0.10,
                    fill_color=colors[key],
                    fill_opacity=0.55 if key != "bci" else 0.70,
                    stroke_width=0,
                ).move_to(spec.get_center() + UP * 0.1)
                group.add(bar)

        return group

    def get_inner_bounds(self, panel):
        return {
            "x0": panel.get_left()[0] + 0.18,
            "x1": panel.get_right()[0] - 0.18,
            "y0": panel.get_bottom()[1] + 0.16,
            "y1": panel.get_top()[1] - 0.16,
        }

    def make_small_spec(self, bounds, col_width_frac=0.18, blur_sigma=0.22):
        x0, x1, y0, y1 = bounds["x0"], bounds["x1"], bounds["y0"], bounds["y1"]
        group = VGroup()

        n_cols = 3
        n_slices = 14
        colors = [ORANGE, PURPLE, TEAL]
        x_fracs = [0.22, 0.50, 0.78]
        freq_centers = [0.50, 0.35, 0.65]

        for col_i, x_frac in enumerate(x_fracs):
            x_center = x0 + x_frac * (x1 - x0)
            col_width = col_width_frac * (x1 - x0)
            color = colors[col_i]
            center_frac = freq_centers[col_i]

            for slice_i in range(n_slices):
                y_frac = slice_i / (n_slices - 1)
                y_center = y0 + y_frac * (y1 - y0)
                op = 0.95 * np.exp(-((y_frac - center_frac) ** 2) / (2 * blur_sigma**2))
                op = float(max(0.05, min(op, 0.95)))

                rect = Rectangle(
                    width=col_width,
                    height=(y1 - y0) / n_slices * 1.02,
                    fill_color=color,
                    fill_opacity=op,
                    stroke_width=0,
                )
                rect.move_to([x_center, y_center, 0])
                group.add(rect)

        return group

    def make_large_spec(self, bounds, edge_ramp=0.25, band_height_frac=0.06):
        x0, x1, y0, y1 = bounds["x0"], bounds["x1"], bounds["y0"], bounds["y1"]
        group = VGroup()

        n_bands = 5
        n_slivers = 30
        colors = [BLUE, GOLD, PINK, TEAL, ORANGE]
        y_fracs = [0.20, 0.40, 0.55, 0.70, 0.85]

        for band_i, y_frac in enumerate(y_fracs):
            band_h = (y1 - y0) * band_height_frac
            y_center = y0 + y_frac * (y1 - y0)
            color = colors[band_i]

            for sliver_i in range(n_slivers):
                x_frac = sliver_i / (n_slivers - 1)
                x_center = x0 + x_frac * (x1 - x0)
                sliver_w = (x1 - x0) / n_slivers

                if x_frac < edge_ramp:
                    op = 0.9 * (x_frac / edge_ramp)
                elif x_frac > 1 - edge_ramp:
                    op = 0.9 * ((1 - x_frac) / edge_ramp)
                else:
                    op = 0.9
                op = float(max(0.05, min(op, 0.9)))

                rect = Rectangle(
                    width=sliver_w * 1.02,
                    height=band_h,
                    fill_color=color,
                    fill_opacity=op,
                    stroke_width=0,
                )
                rect.move_to([x_center, y_center, 0])
                group.add(rect)

        return group

    def construct(self):
        self.camera.background_color = "#0F1116"

        # Start with the previous scene's 4-panel grid visible.
        prev_grid = self.build_prev_grid()
        self.add(prev_grid)

        # Checklist rows (left side).
        item_texts = [
            "Simultaneously display time and frequency information",
            "Make nonstationary signals easier to interpret",
            "Provide an intuitive visual representation of STFT results",
            "Help identify transient neural events",
        ]
        rows = []
        for text in item_texts:
            label = Text(text, font_size=22, color=WHITE)
            label.scale_to_fit_width(4.2)
            slot = Line(ORIGIN, RIGHT * 0.7, color=GREY_B, stroke_width=3)
            row = VGroup(label, slot)
            row.arrange(RIGHT, buff=0.4)
            rows.append(row)

        # Position checklist rows manually.
        start_y = 1.0
        row_gap = 0.65
        for i, row in enumerate(rows):
            row.move_to(np.array([-3.2, start_y - i * row_gap, 0]))

        checklist = VGroup(*rows)

        # Create check marks and attach them to their rows.
        check_marks = []
        for row in rows:
            check = self.make_check_mark(row[1].get_center())
            row.add(check)
            check_marks.append(check)

        r1, r2, r3, r4 = rows
        c1, c2, c3, c4 = check_marks

        # --- Beat 1: 0.00–2.56 ---
        self.play(FadeOut(prev_grid), run_time=max(0.05, 1.15))
        self.play(FadeIn(r1), run_time=max(0.05, 1.41))

        # Gap to 3.38
        self.wait(max(0.05, 0.82))

        # --- Beat 2: 3.38–6.42 ---
        self.play(Create(c1), run_time=max(0.05, 1.8))
        self.play(c1.animate.set_color(WHITE).set_stroke(width=9), run_time=max(0.05, 0.25))
        self.play(c1.animate.set_color(GREEN).set_stroke(width=6), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.64))

        # Gap to 7.10
        self.wait(max(0.05, 0.68))

        # --- Beat 3: 7.10–9.94 ---
        self.play(FadeIn(r2), run_time=max(0.05, 1.1))
        self.play(Create(c2), run_time=max(0.05, 1.0))
        self.play(c2.animate.set_color(WHITE).set_stroke(width=9), run_time=max(0.05, 0.2))
        self.play(c2.animate.set_color(GREEN).set_stroke(width=6), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.24))

        # Gap to 10.58
        self.wait(max(0.05, 0.64))

        # --- Beat 4: 10.58–14.18 ---
        self.play(FadeIn(r3), run_time=max(0.05, 1.2))
        self.play(Create(c3), run_time=max(0.05, 1.3))
        self.play(c3.animate.set_color(WHITE).set_stroke(width=9), run_time=max(0.05, 0.25))
        self.play(c3.animate.set_color(GREEN).set_stroke(width=6), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.55))

        # Gap to 14.90
        self.wait(max(0.05, 0.72))

        # --- Beat 5: 14.90–17.14 ---
        self.play(FadeIn(r4), run_time=max(0.05, 0.9))
        self.play(Create(c4), run_time=max(0.05, 0.8))
        self.play(c4.animate.set_color(WHITE).set_stroke(width=9), run_time=max(0.05, 0.2))
        self.play(c4.animate.set_color(GREEN).set_stroke(width=6), run_time=max(0.05, 0.22))
        self.wait(max(0.05, 0.12))

        # Gap to 17.86
        self.wait(max(0.05, 0.72))

        # --- Build right-side panels and spectrograms ---
        panel_w, panel_h = 2.85, 2.5
        panel_gap = 0.35

        small_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        large_panel = Rectangle(
            width=panel_w,
            height=panel_h,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )

        small_panel.move_to(np.array([2.5 - (panel_w + panel_gap) / 2, 0, 0]))
        large_panel.move_to(np.array([2.5 + (panel_w + panel_gap) / 2, 0, 0]))
        panels_group = VGroup(small_panel, large_panel)

        small_bounds = self.get_inner_bounds(small_panel)
        large_bounds = self.get_inner_bounds(large_panel)

        small_spec_group = self.make_small_spec(
            small_bounds, col_width_frac=0.18, blur_sigma=0.22
        )
        small_spec_sharper = self.make_small_spec(
            small_bounds, col_width_frac=0.10, blur_sigma=0.38
        )
        large_spec_group = self.make_large_spec(
            large_bounds, edge_ramp=0.25, band_height_frac=0.06
        )
        large_spec_sharper = self.make_large_spec(
            large_bounds, edge_ramp=0.42, band_height_frac=0.035
        )

        small_label = Text(
            "Small window:\ngood time resolution,\npoor frequency resolution",
            font_size=15,
            color=WHITE,
        )
        small_label.scale_to_fit_width(3.3)
        small_label.next_to(small_panel, UP, buff=0.12)

        large_label = Text(
            "Large window:\npoor time resolution,\ngood frequency resolution",
            font_size=15,
            color=WHITE,
        )
        large_label.scale_to_fit_width(3.3)
        large_label.next_to(large_panel, UP, buff=0.12)

        heading = Text("Window size", font_size=24, color=WHITE)
        heading.next_to(panels_group, DOWN, buff=0.55)

        final_text = Text(
            "Every spectrogram reflects a time–frequency trade-off",
            font_size=26,
            color=WHITE,
            weight=BOLD,
        )
        final_text.scale_to_fit_width(11.0)
        final_text.to_edge(DOWN, buff=0.55)

        # --- Beat 6: 17.86–23.64 ---
        self.play(
            checklist.animate.set_opacity(0.35).shift(LEFT * 0.8),
            run_time=max(0.05, 1.4),
        )
        self.play(FadeIn(panels_group), run_time=max(0.05, 1.9))
        self.wait(max(0.05, 2.48))

        # Gap to 24.18
        self.wait(max(0.05, 0.54))

        # --- Beat 7: 24.18–27.68 ---
        self.play(FadeIn(heading), run_time=max(0.05, 3.5))

        # --- Beat 8: 27.68–30.72 ---
        self.play(FadeIn(small_label), run_time=max(0.05, 0.7))
        self.play(FadeIn(small_spec_group), run_time=max(0.05, 1.9))
        self.wait(max(0.05, 0.44))

        # Gap to 31.46
        self.wait(max(0.05, 0.74))

        # --- Beat 9: 31.46–33.18 ---
        self.play(Transform(small_spec_group, small_spec_sharper), run_time=max(0.05, 1.72))

        # Gap to 33.98
        self.wait(max(0.05, 0.80))

        # --- Beat 10: 33.98–36.54 ---
        self.play(FadeIn(large_label), run_time=max(0.05, 0.7))
        self.play(FadeIn(large_spec_group), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.36))

        # Gap to 36.98
        self.wait(max(0.05, 0.44))

        # --- Beat 11: 36.98–38.44 ---
        self.play(Transform(large_spec_group, large_spec_sharper), run_time=max(0.05, 1.46))

        # Gap to 39.42
        self.wait(max(0.05, 0.98))

        # --- Beat 12: 39.42–47.42 ---
        self.play(FadeIn(final_text), run_time=max(0.05, 2.0))

        # Sequential soft pulses: small window first, then large window.
        self.play(small_panel.animate.set_stroke(YELLOW, width=3.0), run_time=max(0.05, 0.6))
        self.play(small_panel.animate.set_stroke(GREY_B, width=1.5), run_time=max(0.05, 0.6))
        self.play(large_panel.animate.set_stroke(YELLOW, width=3.0), run_time=max(0.05, 0.6))
        self.play(large_panel.animate.set_stroke(GREY_B, width=1.5), run_time=max(0.05, 0.6))

        self.wait(max(0.05, 3.60))