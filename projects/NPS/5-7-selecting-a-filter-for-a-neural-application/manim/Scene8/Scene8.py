ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ─── Generate neural signal with isolated spikes ──────────
        np.random.seed(812)
        n_pts = 500
        x_vals = np.linspace(-6.0, 6.0, n_pts)

        smooth = (
            0.8 * np.sin(0.6 * x_vals + 0.2)
            + 0.6 * np.sin(1.5 * x_vals - 0.4)
            + 0.4 * np.cos(2.3 * x_vals + 1.0)
        )
        noise = 0.18 * (np.random.rand(n_pts) - 0.5)
        contaminated = smooth + noise

        spike_indices = [80, 195, 320, 435]
        spike_values = [2.0, 2.2, -2.0, 2.0]
        for idx, val in zip(spike_indices, spike_values):
            contaminated[idx] += val
            if idx - 1 >= 0:
                contaminated[idx - 1] += val * 0.35
            if idx + 1 < n_pts:
                contaminated[idx + 1] += val * 0.35

        # Median and moving-average filtered versions (window size 41)
        half_win = 20
        median_signal = np.full(n_pts, np.nan)
        ma_signal = np.full(n_pts, np.nan)
        for i in range(half_win, n_pts - half_win):
            window = contaminated[i - half_win:i + half_win + 1]
            median_signal[i] = np.median(window)
            ma_signal[i] = np.mean(window)

        # Layout constants
        y_noisy = 1.3
        y_clean = -0.8
        scale_y = 0.42

        def make_trace(signal, y_center):
            return [
                np.array([x_vals[i], y_center + signal[i] * scale_y, 0])
                for i in range(n_pts)
            ]

        # Upper trace: spike-contaminated signal
        noisy_trace = VMobject(stroke_color=ORANGE, stroke_width=2.0)
        noisy_trace.set_points_as_corners(make_trace(contaminated, y_noisy))

        base_noisy = Line(
            np.array([-6.8, y_noisy, 0]),
            np.array([6.8, y_noisy, 0]),
            stroke_color=GREY_B,
            stroke_width=1.2,
            stroke_opacity=0.5,
        )

        time_noisy = Text("Time", font_size=22, color=GREY_B)
        time_noisy.move_to(np.array([6.4, y_noisy, 0]))
        amp_noisy = Text("Amplitude", font_size=20, color=GREY_B)
        amp_noisy.rotate(90 * DEGREES)
        amp_noisy.move_to(np.array([-6.6, y_noisy, 0]))

        # ─── Median filter window ─────────────────────────────────
        window_width = 1.0
        window_height = 2.0
        win_rect = Rectangle(
            width=window_width,
            height=window_height,
            fill_color=BLUE,
            fill_opacity=0.18,
            stroke_color=BLUE,
            stroke_width=2.5,
        )
        win_rect.move_to(np.array([-5.5, y_noisy, 0]))
        win_label = Text("Median filter window", font_size=22, color=BLUE)
        win_label.next_to(win_rect, UP, buff=0.35)

        # Window center positions and median output points
        total_steps = 40
        beat3_steps = 16
        centers_x = np.linspace(-5.5, 5.5, total_steps)
        center_indices = [np.argmin(np.abs(x_vals - cx)) for cx in centers_x]
        median_points = [
            np.array([centers_x[i], y_clean + median_signal[center_indices[i]] * scale_y, 0])
            for i in range(total_steps)
        ]

        spike_xs = np.array([x_vals[i] for i in spike_indices])

        # ─────────────── BEAT 1: 0.00 – 0.60 ──────────────────────
        d1 = 0.60
        self.play(
            Create(noisy_trace),
            Create(base_noisy),
            Write(time_noisy),
            Write(amp_noisy),
            run_time=max(0.05, d1
        ))

        # ─────────────── BEAT 2: 0.60 – 1.24 ──────────────────────
        d2 = 0.64
        self.play(
            GrowFromCenter(win_rect),
            Write(win_label),
            run_time=max(0.05, d2
        ))

        # ─────────────── BEAT 3: 1.24 – 2.72 ──────────────────────
        d3 = 1.48
        per_step3 = d3 / beat3_steps
        label_y = y_noisy + window_height / 2 + 0.4

        for s in range(beat3_steps):
            cx = centers_x[s]
            w_left = cx - window_width / 2
            w_right = cx + window_width / 2
            spike_inside = np.any((spike_xs >= w_left) & (spike_xs <= w_right))

            new_win_center = np.array([cx, y_noisy, 0])
            new_label_pos = np.array([cx, label_y, 0])

            if spike_inside:
                flash_time = per_step3 * 0.5
                rest_time = per_step3 - flash_time
                self.play(
                    win_rect.animate.move_to(new_win_center).set_fill(opacity=0.55),
                    win_label.animate.move_to(new_label_pos),
                    run_time=max(0.05, flash_time
                ))
                self.play(
                    win_rect.animate.set_fill(opacity=0.18),
                    run_time=max(0.05, rest_time
                ))
            else:
                self.play(
                    win_rect.animate.move_to(new_win_center),
                    win_label.animate.move_to(new_label_pos),
                    run_time=max(0.05, per_step3
                ))

        # ─────────────── BEAT 4: 2.72 – 5.26 ──────────────────────
        d4 = 2.54
        beat4_steps = total_steps - beat3_steps

        intro_time = 0.35
        remaining4 = d4 - intro_time
        per_step4 = remaining4 / beat4_steps

        median_vgroup = VGroup()
        self.add(median_vgroup)

        base_clean = Line(
            np.array([-6.8, y_clean, 0]),
            np.array([6.8, y_clean, 0]),
            stroke_color=GREY_B,
            stroke_width=1.2,
            stroke_opacity=0.5,
        )
        label_clean = Text("Median-filtered signal", font_size=22, color=TEAL)
        label_clean.move_to(np.array([-4.5, y_clean - 1.0, 0]))

        prev_pt = median_points[beat3_steps - 1]
        first_dot = Dot(point=prev_pt, radius=0.05, color=TEAL, fill_opacity=1)

        self.play(
            Write(base_clean),
            Write(label_clean),
            FadeIn(first_dot),
            run_time=max(0.05, intro_time
        ))
        median_vgroup.add(first_dot)

        for s in range(beat4_steps):
            idx = beat3_steps + s
            cx = centers_x[idx]
            curr_pt = median_points[idx]
            segment = Line(prev_pt, curr_pt, color=TEAL, stroke_width=2.8)

            w_left = cx - window_width / 2
            w_right = cx + window_width / 2
            spike_inside = np.any((spike_xs >= w_left) & (spike_xs <= w_right))

            new_win_center = np.array([cx, y_noisy, 0])
            new_label_pos = np.array([cx, label_y, 0])

            if spike_inside:
                flash_time = per_step4 * 0.5
                rest_time = per_step4 - flash_time
                self.play(
                    win_rect.animate.move_to(new_win_center).set_fill(opacity=0.55),
                    win_label.animate.move_to(new_label_pos),
                    Create(segment),
                    run_time=max(0.05, flash_time
                ))
                median_vgroup.add(segment)
                self.play(
                    win_rect.animate.set_fill(opacity=0.18),
                    run_time=max(0.05, rest_time
                ))
            else:
                self.play(
                    win_rect.animate.move_to(new_win_center),
                    win_label.animate.move_to(new_label_pos),
                    Create(segment),
                    run_time=max(0.05, per_step4
                ))
                median_vgroup.add(segment)

            prev_pt = curr_pt

        # ─────────────── BEAT 5: 5.26 – 6.06 ──────────────────────
        d5 = 0.80
        self.play(FadeOut(win_rect), FadeOut(win_label), run_time=max(0.05, d5 * 0.5))
        self.wait(max(0.05, d5 * 0.5))

        # ─────────────── BEAT 6: 6.06 – 9.26 ──────────────────────
        d6 = 3.20
        d6a = 0.45
        d6b = 0.80
        d6c = 1.10
        d6d = 0.30
        d6e = 0.30
        d6f = 0.25

        # Divider / gap
        divider_y = -2.4
        divider = Line(
            np.array([-6.8, divider_y, 0]),
            np.array([6.8, divider_y, 0]),
            stroke_color=GREY,
            stroke_width=2.0,
            stroke_opacity=0.7,
        )
        compare_label = Text("Comparison", font_size=20, color=GREY)
        compare_label.next_to(divider, DOWN, buff=0.18).shift(RIGHT * 4.5)

        self.play(Create(divider), Write(compare_label), run_time=max(0.05, d6a))

        # Callout on one isolated spike
        spike_idx = 195
        spike_x = x_vals[spike_idx]
        spike_y = y_noisy + contaminated[spike_idx] * scale_y

        callout_circle = Circle(radius=0.4, stroke_color=YELLOW, stroke_width=3.0, fill_opacity=0)
        callout_circle.move_to(np.array([spike_x, spike_y, 0]))
        callout_label = Text("Zoom on spike", font_size=20, color=YELLOW)
        callout_label.next_to(callout_circle, UP, buff=0.15)

        # Small magnified original
        zoom_box = Rectangle(width=2.0, height=1.2, color=YELLOW, stroke_width=2.0, fill_opacity=0.0)
        zoom_box.move_to(np.array([-4.2, -2.9, 0]))
        zoom_label = Text("Original spike", font_size=16, color=YELLOW)
        zoom_label.next_to(zoom_box.get_top(), DOWN, buff=0.07).align_to(zoom_box.get_left(), LEFT).shift(RIGHT * 0.1)

        local_half = 0.55
        local_mask = (x_vals >= spike_x - local_half) & (x_vals <= spike_x + local_half)
        local_indices = np.where(local_mask)[0]

        panel_scale_x = 0.85
        panel_scale_y = 0.42

        orig_base = np.median(contaminated[local_indices])
        orig_pts = [
            zoom_box.get_center() + np.array([
                (x_vals[i] - spike_x) * panel_scale_x,
                (contaminated[i] - orig_base) * scale_y * panel_scale_y,
                0,
            ])
            for i in local_indices
        ]
        orig_line = VMobject(stroke_color=ORANGE, stroke_width=2.0)
        orig_line.set_points_as_corners(orig_pts)

        self.play(
            Create(callout_circle),
            Write(callout_label),
            FadeIn(zoom_box),
            Write(zoom_label),
            Create(orig_line),
            run_time=max(0.05, d6b
        ))

        # Two comparison panels
        box_median = Rectangle(width=1.7, height=1.2, color=TEAL, stroke_width=2.5, fill_opacity=0.0)
        box_median.move_to(np.array([0.1, -2.9, 0]))
        label_med_box = Text("Median filter\noutput", font_size=15, color=TEAL, line_spacing=0.9)
        label_med_box.next_to(box_median.get_top(), DOWN, buff=0.07).align_to(box_median.get_left(), LEFT).shift(RIGHT * 0.08)

        box_ma = Rectangle(width=1.7, height=1.2, color=ORANGE, stroke_width=2.5, fill_opacity=0.0)
        box_ma.move_to(np.array([2.7, -2.9, 0]))
        label_ma_box = Text("Moving average\noutput", font_size=15, color=ORANGE, line_spacing=0.9)
        label_ma_box.next_to(box_ma.get_top(), DOWN, buff=0.07).align_to(box_ma.get_left(), LEFT).shift(RIGHT * 0.08)

        med_base = np.median(median_signal[local_indices])
        med_pts = [
            box_median.get_center() + np.array([
                (x_vals[i] - spike_x) * panel_scale_x,
                (median_signal[i] - med_base) * scale_y * panel_scale_y,
                0,
            ])
            for i in local_indices
        ]
        med_line = VMobject(stroke_color=TEAL, stroke_width=3.0)
        med_line.set_points_as_corners(med_pts)

        ma_base = np.median(ma_signal[local_indices])
        ma_pts = [
            box_ma.get_center() + np.array([
                (x_vals[i] - spike_x) * panel_scale_x,
                (ma_signal[i] - ma_base) * scale_y * panel_scale_y,
                0,
            ])
            for i in local_indices
        ]
        ma_line = VMobject(stroke_color=ORANGE, stroke_width=3.0)
        ma_line.set_points_as_corners(ma_pts)

        self.play(
            FadeIn(box_median),
            FadeIn(box_ma),
            Write(label_med_box),
            Write(label_ma_box),
            Create(med_line),
            Create(ma_line),
            run_time=max(0.05, d6c
        ))

        # Highlight median panel
        med_glow = SurroundingRectangle(box_median, color=GOLD, buff=0.08, stroke_width=4)
        self.play(Create(med_glow), run_time=max(0.05, d6d))
        self.wait(max(0.05, d6e))
        self.play(FadeOut(med_glow), run_time=max(0.05, d6f))

        # ─────────────── BEAT 7: 9.26 – 11.72 ─────────────────────
        d7_a = 0.45
        d7_b = 0.30
        d7_c = 0.45
        d7_d = 0.30
        d7_wait = 0.96

        self.play(median_vgroup.animate.set_color(GOLD), run_time=max(0.05, d7_a))
        self.play(median_vgroup.animate.set_color(TEAL), run_time=max(0.05, d7_b))
        self.play(median_vgroup.animate.set_color(GOLD), run_time=max(0.05, d7_c))
        self.play(median_vgroup.animate.set_color(TEAL), run_time=max(0.05, d7_d))
        self.wait(max(0.05, d7_wait))

        # ─────────────── BEAT 8: 11.72 – 14.40 ────────────────────
        d8 = 2.68
        self.wait(max(0.05, d8))

        # ─────────────── BEAT 9: 14.40 – 15.32 ────────────────────
        d9 = 0.92
        self.wait(max(0.05, d9))