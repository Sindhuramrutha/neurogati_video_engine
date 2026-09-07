ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Same waveform / window geometry as previous scene ---
        def wave_func(x):
            return 0.8 * np.sin(2.5 * x) * np.cos(0.35 * x) + 0.3 * np.sin(5.0 * x) + 0.15 * np.sin(1.2 * x)

        wave_min_x = -6.5
        wave_max_x = 6.5
        n_segments = 10
        seg_w = (wave_max_x - wave_min_x) / n_segments

        wave_y_center = 2.4
        win_height = 2.6
        win_center_y = 2.05
        win_width = seg_w * 1.05

        def win_left(i):
            return wave_min_x + i * seg_w

        def win_center(i):
            return win_left(i) + seg_w / 2

        def win_target(i):
            return np.array([win_center(i), win_center_y, 0])

        # Full dim waveform
        wave = FunctionGraph(wave_func, x_range=[wave_min_x, wave_max_x])
        wave.set_stroke(GREY_D, width=2)
        wave.shift(UP * wave_y_center)

        def make_bright_segment(i):
            seg = FunctionGraph(wave_func, x_range=[win_left(i), win_left(i) + seg_w])
            seg.set_stroke(color=YELLOW, width=7)
            seg.shift(UP * wave_y_center)
            return seg

        current_bright = make_bright_segment(0)

        # First-window rectangle
        window_rect = Rectangle(
            width=win_width,
            height=win_height,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=4,
        )
        window_rect.move_to(win_target(0))

        # Step list on the left, starting with steps 1 and 2 bright
        step_texts = [
            Text("1", font_size=30, color=YELLOW, weight="BOLD"),
            Text("2", font_size=30, color=YELLOW, weight="BOLD"),
            Text("3", font_size=30, color=GREY_C, weight="BOLD"),
            Text("4", font_size=30, color=GREY_C, weight="BOLD"),
        ]
        step_texts[0].set_opacity(1)
        step_texts[1].set_opacity(1)
        step_texts[2].set_opacity(0.4)
        step_texts[3].set_opacity(0.4)
        step_numbers = VGroup(*step_texts).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.45)

        # Labels above the window
        def label_pos(i):
            x = max(win_center(i), -4.5)
            label_y = win_center_y + win_height / 2 + 0.3
            return np.array([x, label_y, 0])

        step_label = Text("Step 2: Apply Fourier Transform", font_size=26, color=WHITE)
        step_label.scale_to_fit_width(3.6)
        step_label.move_to(label_pos(0))

        step3_label = Text("Step 3: Move window", font_size=26, color=WHITE)
        step3_label.scale_to_fit_width(3.6)
        step3_label.move_to(label_pos(0))

        # Spectrum helper
        def make_spectrum_curve(center, width, height, heights, color=YELLOW, stroke_width=5):
            n_points = 160
            xs = np.linspace(center[0] - width / 2, center[0] + width / 2, n_points)
            baseline_y = center[1] - height / 2 + 0.08 * height
            top_y = center[1] + height / 2 - 0.08 * height
            peak_xs = np.linspace(
                center[0] - width / 2 + 0.15 * width,
                center[0] + width / 2 - 0.15 * width,
                len(heights),
            )
            sigma = 0.09 * width
            components = [h * np.exp(-((xs - px) / sigma) ** 2) for px, h in zip(peak_xs, heights)]
            raw = np.sum(components, axis=0)
            max_raw = raw.max()
            ys = baseline_y + (raw / max_raw) * (top_y - baseline_y)

            curve = VMobject()
            curve.set_points_as_corners([np.array([xs[i], ys[i], 0]) for i in range(n_points)])
            curve.set_stroke(color=color, width=stroke_width)
            curve.set_fill(opacity=0)
            return curve

        # Right-side spectrum plot
        right_spec_center = np.array([4.6, -0.5, 0])
        spec_width = 3.8
        spec_height = 1.6

        bottom_axis = Line(
            np.array([right_spec_center[0] - spec_width / 2, right_spec_center[1] - spec_height / 2, 0]),
            np.array([right_spec_center[0] + spec_width / 2, right_spec_center[1] - spec_height / 2, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        left_axis = Line(
            np.array([right_spec_center[0] - spec_width / 2, right_spec_center[1] - spec_height / 2, 0]),
            np.array([right_spec_center[0] - spec_width / 2, right_spec_center[1] + spec_height / 2, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        right_axes = VGroup(bottom_axis, left_axis)

        # Spectrum patterns for successive windows
        spec_heights = [
            [0.45, 0.8, 0.3, 0.65, 0.2, 0.5],
            [0.8, 0.25, 0.6, 0.2, 0.7, 0.35],
            [0.2, 0.7, 0.15, 0.8, 0.4, 0.55],
            [0.65, 0.3, 0.8, 0.2, 0.5, 0.45],
            [0.3, 0.55, 0.2, 0.7, 0.65, 0.4],
        ]

        current_right_curve = make_spectrum_curve(
            right_spec_center, spec_width, spec_height, spec_heights[0],
            color=YELLOW, stroke_width=5,
        )

        # Small Fourier Transform icon above the spectrum plot
        def make_fourier_icon():
            icon = VGroup()
            time_wave = FunctionGraph(lambda x: 0.25 * np.sin(6 * x), x_range=[-0.8, -0.15])
            time_wave.set_stroke(YELLOW, width=3)
            arrow = Arrow(
                start=np.array([-0.05, 0, 0]),
                end=np.array([0.3, 0, 0]),
                buff=0,
                color=YELLOW,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.3,
            )
            baseline = Line(
                np.array([0.45, -0.15, 0]),
                np.array([1.05, -0.15, 0]),
                color=YELLOW,
                stroke_width=2,
            )
            peak_xs = [0.45, 0.6, 0.75, 0.9]
            peak_heights = [0.2, 0.4, 0.6, 0.35]
            bars = VGroup()
            for px, ph in zip(peak_xs, peak_heights):
                bar = Rectangle(width=0.08, height=ph, fill_color=YELLOW, fill_opacity=0.85, stroke_width=0)
                bar.move_to(np.array([px, -0.15 + ph / 2, 0]))
                bars.add(bar)
            icon.add(time_wave, arrow, baseline, bars)
            icon.scale_to_fit_width(2.2)
            icon.move_to(np.array([4.6, 1.0, 0]))
            return icon

        fourier_icon = make_fourier_icon()

        # Mini spectra for the bottom row
        def make_mini_spectrum(i):
            w = 1.4
            h = 0.9
            center = np.array([0, 0, 0])
            mini_bottom = Line(
                center + LEFT * w / 2 + DOWN * h / 2,
                center + RIGHT * w / 2 + DOWN * h / 2,
                color=GREY_B,
                stroke_width=2,
            )
            mini_curve = make_spectrum_curve(center, w, h, spec_heights[i], color=YELLOW, stroke_width=4)
            return VGroup(mini_bottom, mini_curve)

        mini_items = [make_mini_spectrum(i) for i in range(5)]
        mini_row = VGroup(*mini_items).arrange(RIGHT, buff=0.2).move_to(np.array([0, -2.8, 0]))

        # Add the initial frame
        self.add(
            wave,
            current_bright,
            window_rect,
            step_numbers,
            step_label,
            right_axes,
            current_right_curve,
            fourier_icon,
        )

        # --- Beat 1: 0.00-1.03 ---
        self.play(
            step_texts[1].animate.set_opacity(0.4).set_color(GREY_C),
            step_texts[2].animate.set_opacity(1).set_color(YELLOW),
            Transform(step_label, step3_label),
            run_time=max(0.05, 1.03),
        )

        # Gap to beat 2 at 1.58
        self.wait(max(0.05, 0.55))

        # --- Beat 2: 1.58-4.42 ---
        def slide_to(new_i, run_time):
            nonlocal current_bright
            new_bright = make_bright_segment(new_i)
            self.play(
                window_rect.animate.move_to(win_target(new_i)),
                Transform(current_bright, new_bright),
                step_label.animate.move_to(label_pos(new_i)),
                run_time=max(0.05, run_time),
            )

        slide_to(1, run_time=max(0.05, 2.84))

        # Gap to beat 3 at 5.18
        self.wait(max(0.05, 0.76))

        # --- Beat 3: 5.18-6.70 ---
        self.play(
            current_bright.animate.set_stroke(width=8, color=YELLOW),
            window_rect.animate.set_stroke(width=6),
            run_time=max(0.05, 0.8),
        )
        self.play(
            current_bright.animate.set_stroke(width=7, color=YELLOW),
            window_rect.animate.set_stroke(width=4),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 0.32))

        # --- Beat 4: 7.80-9.30 (after a dry gap) ---
        self.wait(max(0.05, 1.10))

        step4_label = Text("Step 4: Repeat the process", font_size=26, color=WHITE)
        step4_label.scale_to_fit_width(3.6)
        step4_label.move_to(step_label.get_center())

        self.play(
            step_texts[2].animate.set_opacity(0.4).set_color(GREY_C),
            step_texts[3].animate.set_opacity(1).set_color(YELLOW),
            Transform(step_label, step4_label),
            run_time=max(0.05, 1.5),
        )

        # --- Beat 5: 10.14-12.86 (after a dry gap) ---
        self.wait(max(0.05, 0.84))

        new_curve_1 = make_spectrum_curve(
            right_spec_center, spec_width, spec_height, spec_heights[1],
            color=YELLOW, stroke_width=5,
        )
        self.play(
            fourier_icon.animate.scale(1.2),
            FadeOut(current_right_curve),
            FadeIn(new_curve_1),
            run_time=max(0.05, 1.1),
        )
        self.play(fourier_icon.animate.scale(1 / 1.2), run_time=max(0.05, 0.7))
        current_right_curve = new_curve_1
        self.wait(max(0.05, 0.92))

        # --- Transition into faster sliding: dim step list, then beat 6 13.72-16.28 ---
        self.play(step_numbers.animate.set_opacity(0.35), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.56))

        def update_spectrum(i, run_time):
            nonlocal current_right_curve
            new_curve = make_spectrum_curve(
                right_spec_center, spec_width, spec_height, spec_heights[i],
                color=YELLOW, stroke_width=5,
            )
            self.play(
                current_bright.animate.set_stroke(width=8, color=YELLOW),
                window_rect.animate.set_stroke(width=6),
                FadeOut(current_right_curve),
                FadeIn(new_curve),
                run_time=max(0.05, run_time),
            )
            current_right_curve = new_curve

        # Two more positions, each faster than the previous slide
        slide_to(2, run_time=max(0.05, 1.0))
        update_spectrum(2, run_time=max(0.05, 0.5))

        slide_to(3, run_time=max(0.05, 0.7))
        update_spectrum(3, run_time=max(0.05, 0.36))

        # --- Beat 7: 16.28-18.94 ---
        # Show the first four mini spectra along the bottom, then final fast slide
        for i in range(4):
            self.play(GrowFromCenter(mini_items[i]), run_time=max(0.05, 0.2))

        final_bright = make_bright_segment(4)
        new_curve_5 = make_spectrum_curve(
            right_spec_center, spec_width, spec_height, spec_heights[4],
            color=YELLOW, stroke_width=5,
        )

        self.play(
            window_rect.animate.move_to(win_target(4)),
            Transform(current_bright, final_bright),
            step_label.animate.move_to(label_pos(4)),
            FadeOut(current_right_curve),
            FadeIn(new_curve_5),
            GrowFromCenter(mini_items[4]),
            run_time=max(0.05, 0.6),
        )
        current_right_curve = new_curve_5
        self.wait(max(0.05, 1.26))

        # --- Beat 8: 18.94-21.54 ---
        top_group = VGroup(wave, current_bright, window_rect, step_label, step_numbers)
        self.play(
            top_group.animate.shift(UP * 0.5).set_opacity(0.6),
            right_axes.animate.set_opacity(0.5),
            current_right_curve.animate.set_opacity(0.5),
            fourier_icon.animate.set_opacity(0.5),
            mini_row.animate.shift(UP * 0.3),
            run_time=max(0.05, 1.4),
        )

        # Arrows above the row, pointing left to right
        progress_arrows = VGroup()
        for i in range(4):
            x1 = mini_items[i].get_right()[0]
            x2 = mini_items[i + 1].get_left()[0]
            mid_x = (x1 + x2) / 2
            y = mini_row.get_top()[1] + 0.25
            arr = Arrow(
                start=np.array([mid_x - 0.12, y, 0]),
                end=np.array([mid_x + 0.12, y, 0]),
                buff=0,
                color=ORANGE,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.4,
            )
            progress_arrows.add(arr)

        self.play(
            FadeIn(progress_arrows),
            *[mini_items[i][1].animate.set_color(GREY_C).set_stroke(width=3) for i in range(4)],
            mini_items[4][1].animate.set_color(GOLD).set_stroke(width=5),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.4))

        # --- Beat 9: 21.54-22.23 ---
        self.wait(max(0.05, 0.69))