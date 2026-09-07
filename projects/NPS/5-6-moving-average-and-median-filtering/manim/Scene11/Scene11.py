ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene11(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------------
        def make_signal(axes, x_arr, y_arr, color=WHITE, stroke_width=3):
            points = [axes.c2p(x, y) for x, y in zip(x_arr, y_arr)]
            mob = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
            mob.set_points_as_corners(points)
            return mob

        def add_grid(axes):
            x_ticks = np.linspace(0, 1, 6)
            y_ticks = np.linspace(-1.5, 1.5, 7)
            lines = VGroup()
            for yt in y_ticks:
                lines.add(Line(
                    axes.c2p(0, yt), axes.c2p(1, yt),
                    stroke_color=GREY, stroke_width=0.5, stroke_opacity=0.3
                ))
            for xt in x_ticks:
                lines.add(Line(
                    axes.c2p(xt, -1.5), axes.c2p(xt, 1.5),
                    stroke_color=GREY, stroke_width=0.5, stroke_opacity=0.3
                ))
            return lines

        n_pts = 300
        x_arr = np.linspace(0, 1, n_pts)

        # ------------------------------------------------------------------
        # Signal data (identical to Scene10)
        # ------------------------------------------------------------------
        np.random.seed(41)
        eeg_low = 0.6 * np.sin(2*np.pi*8*x_arr)
        eeg_noise = 0.15 * np.sin(2*np.pi*45*x_arr) + 0.08*np.random.randn(n_pts)
        eeg_raw_y = eeg_low + eeg_noise

        win_half = 0.04
        eeg_smooth_y = np.zeros_like(x_arr)
        for i in range(n_pts):
            mask = (x_arr >= x_arr[i]-win_half) & (x_arr <= x_arr[i]+win_half)
            if np.sum(mask) > 0:
                eeg_smooth_y[i] = np.mean(eeg_raw_y[mask])
            else:
                eeg_smooth_y[i] = eeg_raw_y[i]

        np.random.seed(42)
        emg_noise = np.cumsum(np.random.randn(n_pts)*0.12)
        emg_noise -= emg_noise.mean()
        emg_noise = 0.7 * emg_noise / (np.max(np.abs(emg_noise)) + 1e-9)
        spike_center = 0.5
        spike = 2.2 * np.exp(-0.5*((x_arr-spike_center)/0.015)**2)
        emg_raw_y = emg_noise + spike
        emg_clean_y = emg_noise.copy()

        # ------------------------------------------------------------------
        # Panels and grid
        # ------------------------------------------------------------------
        x_range = [0, 1, 0.2]
        y_range = [-1.5, 1.5, 0.5]
        x_length = 6.0
        y_length = 4.0

        left_axes = Axes(
            x_range=x_range, y_range=y_range,
            x_length=x_length, y_length=y_length,
            axis_config={"include_numbers": False, "include_ticks": False,
                         "stroke_color": GREY, "stroke_width": 2},
            tips=False,
        ).move_to(np.array([-3.5, 0, 0]))

        right_axes = Axes(
            x_range=x_range, y_range=y_range,
            x_length=x_length, y_length=y_length,
            axis_config={"include_numbers": False, "include_ticks": False,
                         "stroke_color": GREY, "stroke_width": 2},
            tips=False,
        ).move_to(np.array([3.5, 0, 0]))

        divider = Line(start=UP*4, end=DOWN*4, stroke_color=GREY, stroke_width=2)

        left_grid = add_grid(left_axes)
        right_grid = add_grid(right_axes)

        # ------------------------------------------------------------------
        # Traces
        # ------------------------------------------------------------------
        eeg_smooth_trace = make_signal(left_axes, x_arr, eeg_smooth_y, color=YELLOW, stroke_width=5)
        emg_clean_trace = make_signal(right_axes, x_arr, emg_clean_y, color=GREEN, stroke_width=3)

        eeg_raw_trace = make_signal(left_axes, x_arr, eeg_raw_y, color=TEAL, stroke_width=2.5)
        eeg_raw_trace.set_opacity(0)

        emg_raw_trace = make_signal(right_axes, x_arr, emg_raw_y, color=WHITE, stroke_width=1.5)
        emg_raw_trace.set_opacity(0)

        # ------------------------------------------------------------------
        # Icons
        # ------------------------------------------------------------------
        fe_circle = Circle(radius=0.6, fill_color=BLUE, fill_opacity=1,
                           stroke_color=WHITE, stroke_width=2)
        fe_text = Text("Feature\nextraction", font_size=14, color=WHITE,
                       line_spacing=0.9, weight="BOLD").move_to(fe_circle.get_center())
        left_icon = VGroup(fe_circle, fe_text).scale(0.85)
        left_icon.move_to(left_axes.get_corner(DR) + UP*0.4 + LEFT*0.4)

        class_circle = Circle(radius=0.6, fill_color=BLUE, fill_opacity=1,
                              stroke_color=WHITE, stroke_width=2)
        class_text = Text("Classification", font_size=14, color=WHITE, weight="BOLD")
        class_text.move_to(class_circle.get_center())
        right_icon = VGroup(class_circle, class_text).scale(0.85)
        right_icon.move_to(right_axes.get_corner(DR) + UP*0.4 + LEFT*0.4)

        # ------------------------------------------------------------------
        # Initial labels
        # ------------------------------------------------------------------
        left_label_init = Text("EEG smoothing", font_size=28, color=WHITE)
        left_label_init.next_to(left_axes, DOWN, buff=0.4)

        right_label_init = Text("Artefact removal", font_size=28, color=WHITE)
        right_label_init.next_to(right_axes, DOWN, buff=0.4)

        # ------------------------------------------------------------------
        # BEAT 1 (0.00 - 0.64) — split-screen already visible
        # ------------------------------------------------------------------
        initial_group = VGroup(left_axes, right_axes, divider,
                               left_grid, right_grid,
                               eeg_smooth_trace, emg_clean_trace,
                               left_icon, right_icon,
                               left_label_init, right_label_init)
        self.play(FadeIn(initial_group), run_time=max(0.05, 0.64))

        # ------------------------------------------------------------------
        # BEAT 2 (0.64 - 2.22) — freeze, dim, icons shrink, grids soften
        # ------------------------------------------------------------------
        self.play(
            eeg_smooth_trace.animate.set_opacity(0.4),
            emg_clean_trace.animate.set_opacity(0.4),
            left_icon.animate.scale(0).set_opacity(0),
            right_icon.animate.scale(0).set_opacity(0),
            left_grid.animate.set_opacity(0.1),
            right_grid.animate.set_opacity(0.1),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 2.22 - 1.64))  # 0.58 sec

        # ------------------------------------------------------------------
        # BEAT 3 (2.22 - 4.00) — moving-average window on left panel
        # ------------------------------------------------------------------
        # Brighten left panel and reveal raw trace
        self.play(left_grid.animate.set_opacity(0.3),
                  eeg_smooth_trace.animate.set_opacity(0.0),
                  run_time=max(0.05, 0.15))
        self.play(FadeIn(eeg_raw_trace), run_time=max(0.05, 0.15))

        win_width_data = 0.08
        win_rect_width = win_width_data * x_length
        y_mid_left = (y_range[0] + y_range[1]) / 2
        start_point = left_axes.c2p(win_width_data/2, y_mid_left)
        end_point = left_axes.c2p(1 - win_width_data/2, y_mid_left)

        ma_window = Rectangle(
            width=win_rect_width, height=y_length,
            stroke_color=YELLOW, stroke_width=2,
            fill_color=YELLOW, fill_opacity=0.15,
        ).move_to(start_point)

        self.play(FadeIn(ma_window), run_time=max(0.05, 0.08))

        smooth_draw = make_signal(left_axes, x_arr, eeg_smooth_y, color=YELLOW, stroke_width=5)
        self.add(smooth_draw)

        self.play(
            ma_window.animate.move_to(end_point),
            Create(smooth_draw, rate_func=linear),
            run_time=max(0.05, 1.32),
        )
        self.play(FadeOut(ma_window), run_time=max(0.05, 0.08))

        # Keep reference to the now-drawn smooth trace
        eeg_smooth_trace = smooth_draw
        glow = None

        # Gap 4.00 -> 4.82
        self.wait(max(0.05, 4.82 - 4.00))  # 0.82 sec

        # ------------------------------------------------------------------
        # BEAT 4 (4.82 - 5.88) — replace left label with annotation
        # ------------------------------------------------------------------
        left_annotation1 = Text("Averages neighbouring samples", font_size=24, color=WHITE)
        left_annotation1.next_to(left_axes, DOWN, buff=0.6)

        self.play(FadeOut(left_label_init), run_time=max(0.05, 0.3))
        self.play(FadeIn(left_annotation1), run_time=max(0.05, 0.76))

        # ------------------------------------------------------------------
        # BEAT 5 (5.88 - 7.40) — ripple pulse, smooth trace glow
        # ------------------------------------------------------------------
        self.play(Indicate(eeg_raw_trace, color=TEAL, scale_factor=1.05), run_time=max(0.05, 0.5))

        glow = eeg_smooth_trace.copy()
        glow.set_stroke(color=YELLOW, width=10, opacity=0.25)
        glow.set_fill(opacity=0)

        self.play(
            eeg_raw_trace.animate.set_opacity(0.3),
            FadeIn(glow),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 7.40 - 5.88 - 1.0))  # 0.52 sec

        # ------------------------------------------------------------------
        # BEAT 6 (7.40 - 10.74) — glow intensify + second left annotation
        # ------------------------------------------------------------------
        self.play(
            glow.animate.set_stroke(width=12, opacity=0.5),
            run_time=max(0.05, 0.8),
        )

        left_annotation2 = Text("Produces a smoother signal", font_size=24, color=WHITE)
        left_annotation2.move_to(left_annotation1.get_center() + DOWN*0.8 + RIGHT*4)
        left_annotation2_final = left_annotation1.get_center() + DOWN*0.8
        self.play(left_annotation2.animate.move_to(left_annotation2_final), run_time=max(0.05, 0.8))

        self.wait(max(0.05, 10.74 - 7.40 - 1.6))  # 1.74 sec

        # ------------------------------------------------------------------
        # BEAT 7 (10.74 - 12.20) — median filter replay on right panel
        # ------------------------------------------------------------------
        # Dim left slightly, brighten right grid
        self.play(
            left_grid.animate.set_opacity(0.15),
            eeg_smooth_trace.animate.set_opacity(0.5),
            glow.animate.set_opacity(0.2),
            eeg_raw_trace.animate.set_opacity(0.15),
            right_grid.animate.set_opacity(0.3),
            run_time=max(0.05, 0.3),
        )

        # Swap clean EMG for raw EMG (spiked)
        self.play(FadeOut(emg_clean_trace), FadeIn(emg_raw_trace), run_time=max(0.05, 0.15))

        # Median window + sample dots
        med_win_width_data = 0.1
        med_win_rect_width = med_win_width_data * right_axes.x_length
        y_mid_right = (y_range[0] + y_range[1]) / 2
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

        self.play(FadeIn(med_window), FadeIn(sample_dots), run_time=max(0.05, 0.1))

        # Sort, highlight median, spike disappears and clean baseline returns
        self.play(
            *[dot.animate.move_to(pos) for dot, pos in zip(sample_dots, dot_targets)],
            median_dot.animate.scale(2.5).set_color(YELLOW),
            extreme_dot.animate.set_opacity(0).scale(0.1),
            FadeOut(emg_raw_trace),
            FadeIn(emg_clean_trace),
            run_time=max(0.05, 0.55),
        )

        self.play(FadeOut(med_window), FadeOut(sample_dots), run_time=max(0.05, 0.1))

        # leftover beat time
        self.wait(max(0.05, 12.20 - 10.74 - 1.20))  # 0.26 sec

        # ------------------------------------------------------------------
        # BEAT 8 (12.20 - 13.58) — replace right label with annotation
        # ------------------------------------------------------------------
        right_annotation1 = Text("Uses median of neighbouring values", font_size=24, color=WHITE)
        right_annotation1.next_to(right_axes, DOWN, buff=0.6)

        self.play(FadeOut(right_label_init), run_time=max(0.05, 0.3))
        self.play(FadeIn(right_annotation1), run_time=max(0.05, 1.08))

        # ------------------------------------------------------------------
        # BEAT 9 (13.58 - 17.18) — second right annotation + clean pulse
        # ------------------------------------------------------------------
        self.play(Indicate(emg_clean_trace, color=GREEN, scale_factor=1.05), run_time=max(0.05, 0.6))

        right_annotation2 = Text("Removes impulsive noise, preserves sharp features",
                                 font_size=24, color=WHITE)
        right_annotation2.move_to(right_annotation1.get_center() + DOWN*0.8 + RIGHT*4)
        right_annotation2_final = right_annotation1.get_center() + DOWN*0.8
        self.play(right_annotation2.animate.move_to(right_annotation2_final), run_time=max(0.05, 0.8))

        self.wait(max(0.05, 17.18 - 13.58 - 1.4))  # 2.2 sec

        # ------------------------------------------------------------------
        # BEAT 10 (17.18 - 19.24) — sharp-feature highlight on right trace
        # ------------------------------------------------------------------
        # Find a local high-amplitude feature away from the former spike
        feature_mask = (x_arr > 0.7) & (x_arr < 0.9)
        region_indices = np.where(feature_mask)[0]
        local_abs = np.abs(emg_clean_y[region_indices])
        peak_offset = np.argmax(local_abs)
        idx_feature = region_indices[peak_offset]
        feature_point = right_axes.c2p(x_arr[idx_feature], emg_clean_y[idx_feature])

        feature_highlight = Circle(
            radius=0.18, stroke_color=ORANGE, stroke_width=5, fill_opacity=0,
        ).move_to(feature_point)

        self.play(FadeIn(feature_highlight), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.36))  # until 18.34
        self.play(FadeOut(feature_highlight), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 19.24 - 17.18 - 1.16))  # 0.90 sec

        # ------------------------------------------------------------------
        # BEAT 11 (19.24 - 19.72) — both panels brighten evenly
        # ------------------------------------------------------------------
        self.play(
            left_grid.animate.set_opacity(0.3),
            right_grid.animate.set_opacity(0.3),
            eeg_smooth_trace.animate.set_opacity(1.0),
            emg_clean_trace.animate.set_opacity(1.0),
            run_time=max(0.05, 0.48),
        )

        # ------------------------------------------------------------------
        # BEAT 12 (19.72 - 21.18) — pulse both traces + headline
        # ------------------------------------------------------------------
        self.play(
            Indicate(eeg_smooth_trace, color=YELLOW, scale_factor=1.02),
            Indicate(emg_clean_trace, color=GREEN, scale_factor=1.02),
            run_time=max(0.05, 0.6),
        )

        headline1 = Text("Both improve signal quality", font_size=36, color=YELLOW, weight="BOLD")
        headline1.to_edge(UP, buff=0.4)
        self.play(FadeIn(headline1), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 21.18 - 19.72 - 1.2))  # 0.26 sec

        # ------------------------------------------------------------------
        # BEAT 13 (21.18 - 23.48) — headline shift + noise contrast flicker
        # ------------------------------------------------------------------
        headline2 = Text("But target different noise types", font_size=36, color=YELLOW, weight="BOLD")
        headline2.to_edge(UP, buff=0.4)

        self.play(Transform(headline1, headline2), run_time=max(0.05, 0.5))

        # Flicker: left raw high-freq, right ghost spike
        self.play(
            eeg_raw_trace.animate.set_opacity(0.8),
            emg_raw_trace.animate.set_opacity(0.4),
            run_time=max(0.05, 0.25),
        )
        self.play(
            eeg_raw_trace.animate.set_opacity(0.15),
            emg_raw_trace.animate.set_opacity(0.0),
            run_time=max(0.05, 0.25),
        )
        self.wait(max(0.05, 23.48 - 21.18 - 1.0))  # 1.00 sec

        # ------------------------------------------------------------------
        # BEAT 14 (23.48 - 25.00) — remove annotations, bottom message
        # ------------------------------------------------------------------
        annotations_group = VGroup(left_annotation1, left_annotation2,
                                   right_annotation1, right_annotation2)
        self.play(FadeOut(annotations_group), run_time=max(0.05, 0.6))

        bottom_message = Text("Choose based on your recording’s characteristics",
                              font_size=28, color=WHITE)
        bottom_message.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(bottom_message), run_time=max(0.05, 0.92))

        # ------------------------------------------------------------------
        # BEAT 15 (25.00 - 26.35) — hold, then slowly fade to black
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.28))  # hold until 25.28

        fade_rect = Rectangle(
            width=14, height=8,
            fill_color="#0F1116", fill_opacity=0,
            stroke_width=0,
        ).move_to(ORIGIN)
        self.bring_to_front(fade_rect)
        self.play(fade_rect.animate.set_fill(opacity=1), run_time=max(0.05, 1.07))