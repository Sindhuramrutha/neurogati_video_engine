ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene10(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Helper: build a waveform from axes and data arrays
        def make_signal(axes, x_arr, y_arr, color=WHITE, stroke_width=3):
            points = [axes.c2p(x, y) for x, y in zip(x_arr, y_arr)]
            mob = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
            mob.set_points_as_corners(points)
            return mob

        # Light grid behind each panel
        def add_grid(axes, x_range, y_range):
            x_ticks = np.linspace(x_range[0], x_range[1], 6)
            y_ticks = np.linspace(y_range[0], y_range[1], 7)
            lines = VGroup()
            for yt in y_ticks:
                lines.add(Line(
                    axes.c2p(x_range[0], yt), axes.c2p(x_range[1], yt),
                    stroke_color=GREY, stroke_width=0.5, stroke_opacity=0.3
                ))
            for xt in x_ticks:
                lines.add(Line(
                    axes.c2p(xt, y_range[0]), axes.c2p(xt, y_range[1]),
                    stroke_color=GREY, stroke_width=0.5, stroke_opacity=0.3
                ))
            return lines

        # Axes dimensions
        x_range = [0, 1, 0.2]
        y_range_eeg = [-1.5, 1.5, 0.5]
        y_range_emg = [-1.5, 1.5, 0.5]
        x_length = 6.0
        y_length = 4.0

        left_axes = Axes(
            x_range=x_range, y_range=y_range_eeg,
            x_length=x_length, y_length=y_length,
            axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 2},
            tips=False,
        ).move_to(np.array([-3.5, 0, 0]))

        right_axes = Axes(
            x_range=x_range, y_range=y_range_emg,
            x_length=x_length, y_length=y_length,
            axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 2},
            tips=False,
        ).move_to(np.array([3.5, 0, 0]))

        # Dividing line
        divider = Line(start=UP*4, end=DOWN*4, stroke_color=GREY, stroke_width=2)

        left_grid = add_grid(left_axes, x_range, y_range_eeg)
        right_grid = add_grid(right_axes, x_range, y_range_emg)

        # --- Signals ---
        n_pts = 300
        x_arr = np.linspace(0, 1, n_pts)

        # EEG: slow oscillation + high-frequency ripple
        np.random.seed(41)
        eeg_low = 0.6 * np.sin(2*np.pi*8*x_arr)
        eeg_noise = 0.15 * np.sin(2*np.pi*45*x_arr) + 0.08*np.random.randn(n_pts)
        eeg_raw_y = eeg_low + eeg_noise
        eeg_raw_trace = make_signal(left_axes, x_arr, eeg_raw_y, color=TEAL, stroke_width=2.5)

        # Moving average of EEG
        win_half = 0.04
        eeg_smooth_y = np.zeros_like(x_arr)
        for i in range(n_pts):
            mask = (x_arr >= x_arr[i]-win_half) & (x_arr <= x_arr[i]+win_half)
            if np.sum(mask) > 0:
                eeg_smooth_y[i] = np.mean(eeg_raw_y[mask])
            else:
                eeg_smooth_y[i] = eeg_raw_y[i]
        eeg_smooth_trace = make_signal(left_axes, x_arr, eeg_smooth_y, color=YELLOW, stroke_width=5)

        # EMG: dense high-frequency noise + isolated spike
        np.random.seed(42)
        emg_noise = np.cumsum(np.random.randn(n_pts)*0.12)
        emg_noise -= emg_noise.mean()
        emg_noise = 0.7 * emg_noise / (np.max(np.abs(emg_noise)) + 1e-9)
        spike_center = 0.5
        spike = 2.2 * np.exp(-0.5*((x_arr-spike_center)/0.015)**2)
        emg_raw_y = emg_noise + spike
        emg_raw_trace = make_signal(right_axes, x_arr, emg_raw_y, color=WHITE, stroke_width=1.5)

        # Cleaned EMG after median: spike removed, baseline noise remains
        emg_clean_y = emg_noise.copy()
        emg_clean_trace = make_signal(right_axes, x_arr, emg_clean_y, color=GREEN, stroke_width=3)

        # -----------------------------------------------------------
        # BEAT 1 [0.00 – 2.02]
        # -----------------------------------------------------------
        all_init = VGroup(left_axes, right_axes, divider, left_grid, right_grid,
                          eeg_raw_trace, emg_raw_trace)
        self.play(FadeIn(all_init), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 0.22))

        # -----------------------------------------------------------
        # BEAT 2 [2.02 – 3.40]
        # -----------------------------------------------------------
        win_width_data = 0.08
        win_rect_width = win_width_data * x_length
        y_mid_left = (y_range_eeg[0] + y_range_eeg[1]) / 2
        start_point = left_axes.c2p(win_width_data/2, y_mid_left)
        end_point = left_axes.c2p(1 - win_width_data/2, y_mid_left)

        ma_window = Rectangle(
            width=win_rect_width, height=left_axes.y_length,
            stroke_color=YELLOW, stroke_width=2,
            fill_color=YELLOW, fill_opacity=0.15,
        ).move_to(start_point)

        self.play(FadeIn(ma_window), run_time=max(0.05, 0.15))
        self.play(
            ma_window.animate.move_to(end_point),
            Create(eeg_smooth_trace, rate_func=linear),
            run_time=max(0.05, 1.08),
        )
        self.play(FadeOut(ma_window), run_time=max(0.05, 0.15))

        # -----------------------------------------------------------
        # to 4.10
        # -----------------------------------------------------------
        self.wait(max(0.05, 0.70))

        # -----------------------------------------------------------
        # BEAT 3 [4.10 – 5.72]
        # -----------------------------------------------------------
        eeg_label = Text("EEG smoothing", font_size=28, color=WHITE)
        eeg_label.next_to(left_axes, DOWN, buff=0.4)

        fe_circle = Circle(radius=0.6, fill_color=BLUE, fill_opacity=1,
                           stroke_color=WHITE, stroke_width=2)
        fe_text = Text("Feature\nextraction", font_size=14, color=WHITE,
                       line_spacing=0.9, weight="BOLD")
        fe_text.move_to(fe_circle.get_center())
        fe_icon = VGroup(fe_circle, fe_text)
        fe_icon.scale(0.85)
        fe_icon.move_to(left_axes.get_corner(DR) + UP*0.4 + LEFT*0.4)

        self.play(FadeIn(eeg_label), FadeIn(fe_icon), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.02))

        # -----------------------------------------------------------
        # BEAT 4 [5.72 – 6.56]
        # -----------------------------------------------------------
        glow_eeg = eeg_smooth_trace.copy()
        glow_eeg.set_stroke(color=YELLOW, width=8, opacity=0.25)
        self.play(FadeIn(glow_eeg), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.2))
        self.play(FadeOut(glow_eeg), run_time=max(0.05, 0.34))

        # -----------------------------------------------------------
        # to 7.98
        # -----------------------------------------------------------
        self.wait(max(0.05, 1.42))

        # -----------------------------------------------------------
        # BEAT 5 [7.98 – 9.64]
        # -----------------------------------------------------------
        self.play(Indicate(emg_raw_trace, color=YELLOW, scale_factor=1.0), run_time=max(0.05, 0.3))

        env_half = np.max(np.abs(emg_noise)) * 1.2
        env_top = DashedLine(
            right_axes.c2p(0, env_half), right_axes.c2p(1, env_half),
            stroke_color=ORANGE, stroke_width=2, dash_length=0.15
        )
        env_bot = DashedLine(
            right_axes.c2p(0, -env_half), right_axes.c2p(1, -env_half),
            stroke_color=ORANGE, stroke_width=2, dash_length=0.15
        )

        self.play(FadeIn(env_top), FadeIn(env_bot), run_time=max(0.05, 0.6))
        self.play(FadeOut(env_top), FadeOut(env_bot), run_time=max(0.05, 0.76))

        # -----------------------------------------------------------
        # to 10.34
        # -----------------------------------------------------------
        self.wait(max(0.05, 0.70))

        # -----------------------------------------------------------
        # BEAT 6 [10.34 – 11.30]
        # -----------------------------------------------------------
        self.play(Indicate(emg_raw_trace, color=YELLOW, scale_factor=1.0), run_time=max(0.05, 0.96))

        # -----------------------------------------------------------
        # to 12.08
        # -----------------------------------------------------------
        self.wait(max(0.05, 0.78))

        # -----------------------------------------------------------
        # BEAT 7 [12.08 – 14.20]
        # -----------------------------------------------------------
        self.play(fe_icon.animate.scale(1.15), run_time=max(0.05, 0.22))
        self.play(fe_icon.animate.scale(1/1.15), run_time=max(0.05, 0.22))

        class_circle = Circle(radius=0.6, fill_color=GREY, fill_opacity=0.3,
                              stroke_color=GREY, stroke_width=2)
        class_text = Text("Classification", font_size=14, color=GREY, weight="BOLD")
        class_text.move_to(class_circle.get_center())
        class_icon = VGroup(class_circle, class_text)
        class_icon.scale(0.85)
        class_icon.move_to(right_axes.get_corner(DR) + UP*0.4 + LEFT*0.4)

        self.play(FadeIn(class_icon), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 1.28))

        # -----------------------------------------------------------
        # BEAT 8 [14.20 – 15.82]
        # -----------------------------------------------------------
        y_mid_right = (y_range_emg[0] + y_range_emg[1]) / 2
        med_win_width_data = 0.1
        med_win_rect_width = med_win_width_data * x_length
        med_window = Rectangle(
            width=med_win_rect_width, height=right_axes.y_length,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.1,
        ).move_to(right_axes.c2p(0.5, y_mid_right))

        win_x_min, win_x_max = 0.5 - med_win_width_data/2, 0.5 + med_win_width_data/2
        n_samples = 15
        sample_x = np.linspace(win_x_min, win_x_max, n_samples)
        sample_y = np.interp(sample_x, x_arr, emg_raw_y)
        sample_dots = VGroup()
        for sx, sy in zip(sample_x, sample_y):
            d = Dot(point=right_axes.c2p(sx, sy), radius=0.06, color=BLUE, fill_opacity=1)
            sample_dots.add(d)

        sort_idx = np.argsort(sample_y)
        sorted_y = sample_y[sort_idx]
        target_positions = [right_axes.c2p(0.5, sorted_y[rank]) for rank in range(n_samples)]
        dot_targets = []
        for i in range(n_samples):
            rank = np.where(sort_idx == i)[0][0]
            dot_targets.append(target_positions[rank])

        median_dot = sample_dots[sort_idx[n_samples // 2]]
        extreme_dot = sample_dots[sort_idx[-1]]

        # Copy raw trace for ghost later
        original_emg_raw_trace = emg_raw_trace.copy()

        self.play(FadeIn(med_window), FadeIn(sample_dots), run_time=max(0.05, 0.3))
        self.play(
            *[dot.animate.move_to(pos) for dot, pos in zip(sample_dots, dot_targets)],
            run_time=max(0.05, 0.5),
        )
        self.play(
            median_dot.animate.scale(2.5).set_color(YELLOW),
            extreme_dot.animate.set_opacity(0).scale(0.1),
            run_time=max(0.05, 0.2),
        )
        self.play(Transform(emg_raw_trace, emg_clean_trace), run_time=max(0.05, 0.4))
        self.play(FadeOut(med_window), FadeOut(sample_dots), run_time=max(0.05, 0.22))

        # -----------------------------------------------------------
        # to 16.50
        # -----------------------------------------------------------
        self.wait(max(0.05, 0.68))

        # -----------------------------------------------------------
        # BEAT 9 [16.50 – 20.08]
        # -----------------------------------------------------------
        ghost_trace = original_emg_raw_trace.copy()
        ghost_trace.set_stroke(color=WHITE, width=1, opacity=0.25)
        self.play(FadeIn(ghost_trace), run_time=max(0.05, 0.3))

        self.play(Indicate(emg_clean_trace, color=GREEN, scale_factor=1.0), run_time=max(0.05, 0.4))

        artefact_label = Text("Artefact removal", font_size=28, color=WHITE)
        artefact_label.next_to(right_axes, DOWN, buff=0.4)
        self.play(FadeIn(artefact_label), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.38))

        # -----------------------------------------------------------
        # BEAT 10 [20.08 – 20.80]
        # -----------------------------------------------------------
        self.play(emg_clean_trace.animate.scale(1.05), run_time=max(0.05, 0.12))
        self.play(emg_clean_trace.animate.scale(1/1.05), run_time=max(0.05, 0.12))

        gap_rect = Rectangle(
            width=med_win_rect_width, height=right_axes.y_length,
            stroke_color=YELLOW, stroke_width=2, fill_opacity=0,
        ).move_to(right_axes.c2p(0.5, y_mid_right))
        self.play(FadeIn(gap_rect), run_time=max(0.05, 0.1))
        self.play(FadeOut(gap_rect), run_time=max(0.05, 0.1))

        self.play(
            class_icon[0].animate.set_fill(BLUE, opacity=1).set_stroke(color=BLUE, width=2),
            class_icon[1].animate.set_color(WHITE),
            class_icon.animate.scale(1.2),
            run_time=max(0.05, 0.14),
        )
        self.play(class_icon.animate.scale(1/1.2), run_time=max(0.05, 0.14))

        # -----------------------------------------------------------
        # BEAT 11 [22.78 – 24.73]
        # -----------------------------------------------------------
        self.wait(max(0.05, 1.98))
        self.wait(max(0.05, 1.95))