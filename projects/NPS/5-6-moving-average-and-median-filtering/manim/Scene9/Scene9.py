ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Helper: build a waveform from axes and data arrays
        def make_signal(axes, x_arr, y_arr, color=WHITE, stroke_width=3):
            points = [axes.c2p(x, y) for x, y in zip(x_arr, y_arr)]
            mob = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
            mob.set_points_as_corners(points)
            return mob

        # Axes: full width, no ticks or numbers
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-0.2, 1.6, 0.5],
            x_length=12,
            y_length=3.5,
            axis_config={"include_numbers": False,
                         "include_ticks": False,
                         "stroke_color": GREY,
                         "stroke_width": 2},
            tips=False,
        ).move_to(ORIGIN)

        # Create signal: high‑frequency noise + narrow spike at t=5
        np.random.seed(43)
        n_pts = 300
        x = np.linspace(0, 10, n_pts)

        # noise part
        noise = np.cumsum(np.random.randn(n_pts) * 0.08)
        noise = (noise - noise.min()) / (noise.max() - noise.min()) * 0.9
        baseline = 0.25
        noise -= noise.mean()  # center around 0
        noise += baseline

        # spike
        spike = 1.2 * np.exp(-0.5 * ((x - 5) / 0.08) ** 2)

        y_raw = noise + spike
        orig_signal = make_signal(axes, x, y_raw, color=WHITE, stroke_width=2.5)

        # -----------------------------------------------------------
        # BEAT 1 [0.00 – 1.70]  waveform appears
        # -----------------------------------------------------------
        self.play(FadeIn(axes), FadeIn(orig_signal), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.2))

        # -----------------------------------------------------------
        # BEAT 2 [1.70 – 2.12]  moving‑average window appears at left
        # -----------------------------------------------------------
        # window geometry
        win_width = 1.0  # time units
        time_per_unit = (axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0])
        win_rect_width = win_width * time_per_unit
        win_rect_height = axes.c2p(0, axes.y_range[1])[1] - axes.c2p(0, axes.y_range[0])[1]

        y_mid = (axes.y_range[0] + axes.y_range[1]) / 2

        # start at left edge (center at 0.5)
        ma_win_start = Rectangle(
            width=win_rect_width,
            height=win_rect_height,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_opacity=0,
        ).move_to(axes.c2p(0.5, y_mid))

        self.play(FadeIn(ma_win_start), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.12))

        # -----------------------------------------------------------
        # BEAT 3 [2.12 – 4.32]  window slides → draws smoothed trace
        # -----------------------------------------------------------
        # pre‑compute moving‑average smoothed signal
        half_width = 0.5
        ma_y = np.zeros_like(x)
        for i in range(n_pts):
            mask = (x >= x[i] - half_width) & (x <= x[i] + half_width)
            if np.sum(mask) > 0:
                ma_y[i] = np.mean(y_raw[mask])
            else:
                ma_y[i] = y_raw[i]
        ma_trace = make_signal(axes, x, ma_y, color=YELLOW, stroke_width=4)

        # slide window to right edge (center at 9.5)
        target_win_pos = axes.c2p(9.5, y_mid)

        self.play(
            ma_win_start.animate.move_to(target_win_pos),
            Create(ma_trace, rate_func=linear),
            run_time=max(0.05, 2.2),  # 2.12 → 4.32
        )

        # -----------------------------------------------------------
        # BEAT 4 [4.32 – 5.32]  moving‑average window fades away,
        #                         original signal becomes faint
        # -----------------------------------------------------------
        self.play(
            FadeOut(ma_win_start),
            orig_signal.animate.set_stroke(width=1, opacity=0.3),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.5))

        # -----------------------------------------------------------
        # BEAT 5 [5.32 – 5.92]  median window appears over spike area
        # -----------------------------------------------------------
        median_win = Rectangle(
            width=win_rect_width,
            height=win_rect_height,
            stroke_color=ORANGE,
            stroke_width=2,
            fill_opacity=0,
        ).move_to(axes.c2p(5.0, y_mid))

        self.play(FadeIn(median_win), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.2))

        # -----------------------------------------------------------
        # BEAT 6 [5.92 – 7.54]  median filter inside window
        # -----------------------------------------------------------
        # sample points from the moving‑average trace inside the window
        n_dots = 11
        x_samples = np.linspace(4.5, 5.5, n_dots)
        # corresponding y from the moving average
        y_samples = np.interp(x_samples, x, ma_y)

        dots = VGroup()
        for xs, ys in zip(x_samples, y_samples):
            d = Dot(point=axes.c2p(xs, ys), radius=0.07, color=BLUE, fill_opacity=1)
            dots.add(d)

        # 6a – show sample points
        self.play(Create(dots), run_time=max(0.05, 0.3))

        # 6b – rearrange vertically by amplitude
        sort_idx = np.argsort(y_samples)   # indices of vals from low to high
        sorted_y = y_samples[sort_idx]
        targets = []
        for i, dot in enumerate(dots):
            rank = np.where(sort_idx == i)[0][0]
            target_pos = axes.c2p(5.0, sorted_y[rank])
            targets.append((dot, target_pos))

        self.play(
            *[dot.animate.move_to(pos) for dot, pos in targets],
            run_time=max(0.05, 1.0),
        )

        # 6c – highlight median, discard spike, and morph trace
        median_idx = n_dots // 2          # index 5
        median_dot = dots[sort_idx[median_idx]]
        extreme_dot = dots[sort_idx[-1]]  # highest amplitude

        # prepare the final clean trace (spike region replaced by baseline)
        final_y = ma_y.copy()
        spike_zone = (x >= 4.5) & (x <= 5.5)
        final_y[spike_zone] = baseline
        clean_trace = make_signal(axes, x, final_y, color=YELLOW, stroke_width=4)

        self.play(
            median_dot.animate.scale(2.5).set_color(YELLOW),
            extreme_dot.animate.set_opacity(0).scale(0.1),
            Transform(ma_trace, clean_trace),
            run_time=max(0.05, 0.32),
        )

        # Hold until 7.54
        # after 0.32 from 7.22 it's 7.54, no wait needed

        # gap between beats: 7.54 → 8.16
        self.wait(max(0.05, 0.62))

        # -----------------------------------------------------------
        # BEAT 7 [8.16 – 11.06]  median window fades, final highlight,
        #                        text appears
        # -----------------------------------------------------------
        self.play(FadeOut(median_win), run_time=max(0.05, 0.5))

        text = Text("Complementary, not competing",
                    font_size=36, color=WHITE, weight="BOLD")
        text.next_to(axes, DOWN, buff=0.8)

        self.play(FadeIn(text), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.4))

        # -----------------------------------------------------------
        # FINAL HOLD [11.06 – 18.82]
        # -----------------------------------------------------------
        self.wait(max(0.05, 7.76))