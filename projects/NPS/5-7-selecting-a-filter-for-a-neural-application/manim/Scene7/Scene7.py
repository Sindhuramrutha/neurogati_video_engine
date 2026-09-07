ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'
}

class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ────────────────────────────────────────────────────────────
        # Data: noisy signal (upper trace)
        # smooth trend + random high-freq noise
        # ────────────────────────────────────────────────────────────
        np.random.seed(507)
        n_pts = 500
        x_vals = np.linspace(-6, 6, n_pts)
        # underlying trend: sum of a few slow components
        trend = (
            0.7 * np.sin(0.6 * x_vals + 0.2)
            + 0.5 * np.sin(1.3 * x_vals - 0.5)
            + 0.35 * np.cos(2.1 * x_vals + 1.0)
        )
        noise = 0.55 * (np.random.rand(n_pts) - 0.5)
        noisy_signal = trend + noise

        # Moving-average smoothed version (window size ~10% of width = 50 pts)
        win = 50
        half_win = win // 2
        smoothed = np.full(n_pts, np.nan)
        for i in range(half_win, n_pts - half_win):
            smoothed[i] = np.mean(noisy_signal[i - half_win:i + half_win])

        # Y positions: noisy signal in upper half, smoothed in lower half
        y_noisy = 1.25
        y_smooth = -1.75
        y_scale_wave = 0.85

        def to_wave_points(signal, y_center):
            pts = []
            for i in range(n_pts):
                pts.append(np.array([x_vals[i], y_center + signal[i] * y_scale_wave, 0]))
            return pts

        noisy_points = to_wave_points(noisy_signal, y_noisy)
        smooth_points = []
        for i in range(n_pts):
            val = smoothed[i]
            if np.isnan(val):
                val = noisy_signal[i]  # fallback for edges (won't be drawn initially)
            smooth_points.append(np.array([x_vals[i], y_smooth + val * y_scale_wave, 0]))

        # Create VMobjects
        noisy_trace = VMobject(stroke_color=ORANGE, stroke_width=2.2)
        noisy_trace.set_points_as_corners(noisy_points)

        smooth_trace = VMobject(stroke_color=GREEN, stroke_width=2.8)
        smooth_trace.set_points_as_corners(smooth_points)

        # Axes labels
        time_label_noisy = Text("Time", font_size=20, color=GREY_B)
        time_label_noisy.next_to(np.array([6.2, y_noisy, 0]), RIGHT, buff=0.3)
        amp_label_noisy = Text("Amplitude", font_size=18, color=GREY_B)
        amp_label_noisy.rotate(90 * DEGREES)
        amp_label_noisy.next_to(np.array([-6.5, y_noisy, 0]), LEFT, buff=0.3)

        time_label_smooth = Text("Time", font_size=20, color=GREY_B)
        time_label_smooth.next_to(np.array([6.2, y_smooth, 0]), RIGHT, buff=0.3)

        # Thin horizontal baselines
        baseline_noisy = Line(
            np.array([-6.5, y_noisy, 0]),
            np.array([6.5, y_noisy, 0]),
            stroke_color=GREY_B,
            stroke_width=1.2,
            stroke_opacity=0.5,
        )
        baseline_smooth = Line(
            np.array([-6.5, y_smooth, 0]),
            np.array([6.5, y_smooth, 0]),
            stroke_color=GREY_B,
            stroke_width=1.2,
            stroke_opacity=0.5,
        )

        # ────────────────────────────────────────────────────────────
        # Boxcar window (moving average window)
        # ────────────────────────────────────────────────────────────
        window_width = (x_vals[-1] - x_vals[0]) * 0.12
        window_height = 2.0  # tall enough to cover signal swings
        win_rect = Rectangle(
            width=window_width,
            height=window_height,
            fill_color=BLUE,
            fill_opacity=0.18,
            stroke_color=BLUE,
            stroke_width=2.5,
        )
        # Place initially at leftmost segment
        win_start_x = x_vals[half_win]
        win_rect.move_to(np.array([win_start_x, y_noisy, 0]))

        win_label = Text("Moving average window", font_size=20, color=BLUE)
        win_label.next_to(win_rect, UP, buff=0.3)

        # ────────────────────────────────────────────────────────────
        # EMG data for beats 6-10
        # ────────────────────────────────────────────────────────────
        n_emg = 400
        t_emg = np.linspace(0, 4 * np.pi, n_emg)
        # amplitude envelope: bursts with a slow modulation
        amp_env = 0.3 + 0.7 * (np.sin(1.2 * t_emg) ** 2) * (np.sin(3.8 * t_emg + 0.6) ** 2)
        # raw EMG: zero-mean carrier * envelope
        carrier_raw = np.random.randn(n_emg) * 0.8
        emg_raw = amp_env * carrier_raw
        # full-wave rectified
        emg_rect = np.abs(emg_raw)
        # moving-average envelope of rectified EMG
        win_emg = 35
        half_win_emg = win_emg // 2
        emg_envelope = np.full(n_emg, np.nan)
        for i in range(half_win_emg, n_emg - half_win_emg):
            emg_envelope[i] = np.mean(emg_rect[i - half_win_emg:i + half_win_emg])

        emg_x_vals = np.linspace(-5.5, 5.5, n_emg)
        y_emg_base = -3.3
        y_emg_scale = 0.7

        def to_emg_points(signal, y_center):
            pts = []
            for i in range(n_emg):
                pts.append(np.array([emg_x_vals[i], y_center + signal[i] * y_emg_scale, 0]))
            return pts

        emg_raw_points = to_emg_points(emg_raw, y_emg_base)
        emg_rect_points = to_emg_points(emg_rect, y_emg_base)
        env_points = []
        for i in range(n_emg):
            val = emg_envelope[i]
            if np.isnan(val):
                val = 0.0
            env_points.append(np.array([emg_x_vals[i], y_emg_base + val * y_emg_scale, 0]))

        emg_raw_trace = VMobject(stroke_color=RED, stroke_width=1.8, stroke_opacity=0.9)
        emg_raw_trace.set_points_as_corners(emg_raw_points)

        emg_rect_trace = VMobject(stroke_color=ORANGE, stroke_width=1.8, stroke_opacity=0.9)
        emg_rect_trace.set_points_as_corners(emg_rect_points)

        emg_env_trace = VMobject(stroke_color=PINK, stroke_width=3.0)
        emg_env_trace.set_points_as_corners(env_points)

        # Labels for EMG section
        label_raw_emg = Text("Raw EMG", font_size=22, color=RED)
        label_raw_emg.next_to(np.array([-5.8, y_emg_base + 0.5, 0]), RIGHT, buff=0.0)

        label_rect_emg = Text("Rectified EMG", font_size=22, color=ORANGE)
        label_rect_emg.next_to(np.array([-5.8, y_emg_base + 0.5, 0]), RIGHT, buff=0.0)

        label_env = Text("Envelope (moving average)", font_size=20, color=PINK)
        label_env.next_to(np.array([2.0, y_emg_base + 0.9, 0]), UR, buff=0.2)

        # ────────────────────────────────────────────────────────────
        # BEAT 1: 0.00 - 1.54  noisy signal fades in (upper half)
        # ────────────────────────────────────────────────────────────
        beat1_dur = max(0.05, 1.54)
        self.play(
            Create(noisy_trace),
            Create(baseline_noisy),
            Write(time_label_noisy),
            Write(amp_label_noisy),
            run_time=max(0.05, beat1_dur),
        )

        # ────────────────────────────────────────────────────────────
        # BEAT 2: 1.54 - 2.42  translucent boxcar window appears
        #          over leftmost segment (~1/10th width)
        # ────────────────────────────────────────────────────────────
        beat2_dur = max(0.05, 2.42 - 1.54)
        # Position boxcar at far left offset
        win_start_x_left = x_vals[half_win + 2]
        win_rect.move_to(np.array([win_start_x_left, y_noisy, 0]))
        win_label.next_to(win_rect, UP, buff=0.3)
        self.play(
            GrowFromCenter(win_rect),
            Write(win_label),
            run_time=max(0.05, beat2_dur),
        )

        # ────────────────────────────────────────────────────────────
        # BEAT 3: 2.42 - 3.68  window slides step by step,
        #          values inside window briefly highlighted
        # ────────────────────────────────────────────────────────────
        beat3_dur = max(0.05, 3.68 - 2.42)
        # Sliding from current position to near right edge, in ~10 steps
        win_end_x = x_vals[-(half_win + 2)]
        n_steps = 10
        per_step_beat3 = beat3_dur / n_steps
        step_x = (win_end_x - win_start_x_left) / n_steps

        for s in range(n_steps):
            target_x = win_start_x_left + step_x * (s + 1)
            # Highlight the region inside the window: flash fill opacity
            self.play(
                win_rect.animate.move_to(np.array([target_x, y_noisy, 0])),
                win_label.animate.move_to(win_rect.get_top() + np.array([0, 0.55, 0])),
                win_rect.animate.set_fill(opacity=0.38),
                run_time=max(0.05, per_step_beat3 * 0.55),
            )
            self.play(
                win_rect.animate.set_fill(opacity=0.18),
                run_time=max(0.05, per_step_beat3 * 0.45),
            )

        # ────────────────────────────────────────────────────────────
        # BEAT 4: 3.68 - 5.82  smooth trace draws in lower half
        #          as window slides, label "Smoothed signal"
        # ────────────────────────────────────────────────────────────
        beat4_dur = max(0.05, 5.82 - 3.68)
        # Smooth trace has been pre-computed; animate its creation
        # while continuing window motion over remaining steps

        # First, show the baseline and label for smooth trace
        # Window also continues a few more steps to finish traversal
        # We'll split beat4: first part draws smooth trace label,
        # then animate trace creation with window completing

        smooth_label = Text("Smoothed signal", font_size=22, color=GREEN)
        smooth_label.next_to(np.array([-5.8, y_smooth + 0.7, 0]), RIGHT, buff=0.0)

        # Window finishes remaining steps (from beat3's end position to far right,
        # then maybe back left? The brief: "completes its traversal across the full
        # width of the signal". So let's define the remainder: from win_end_x to
        # the absolute end (x_vals[-half_win]). Actually beat3 already reached
        # win_end_x = x_vals[-(half_win+2)], so it's already at the right edge.
        # During beat4 we just hold window there, drawing smooth trace.

        self.play(
            Write(smooth_label),
            Create(baseline_smooth),
            run_time=max(0.05, beat4_dur * 0.25),
        )
        # Draw smooth trace stroke-by-stroke
        self.play(
            Create(smooth_trace),
            run_time=max(0.05, beat4_dur * 0.75),
        )

        # ────────────────────────────────────────────────────────────
        # BEAT 5: 5.82 - 7.62  boxcar fades out, hold both traces
        # ────────────────────────────────────────────────────────────
        beat5_dur = max(0.05, 7.62 - 5.82)
        self.play(
            FadeOut(win_rect),
            FadeOut(win_label),
            run_time=max(0.05, beat5_dur * 0.45),
        )
        # Hold
        self.wait(max(0.05, beat5_dur * 0.55))

        # ────────────────────────────────────────────────────────────
        # BEAT 6: 7.62 - 9.14  shrink/slide upper traces upward,
        #          new EMG raw trace appears in lower third
        # ────────────────────────────────────────────────────────────
        beat6_dur = max(0.05, 9.14 - 7.62)
        # Move both traces + labels upward a bit
        shift_up = 0.55
        # Groups for shifting
        upper_group = VGroup(noisy_trace, baseline_noisy, time_label_noisy, amp_label_noisy)
        lower_group = VGroup(smooth_trace, baseline_smooth, smooth_label, time_label_smooth)

        self.play(
            upper_group.animate.shift(UP * shift_up),
            lower_group.animate.shift(UP * shift_up),
            run_time=max(0.05, beat6_dur * 0.4),
        )
        # Show raw EMG
        self.play(
            Create(emg_raw_trace),
            Write(label_raw_emg),
            run_time=max(0.05, beat6_dur * 0.6),
        )

        # ────────────────────────────────────────────────────────────
        # BEAT 7: 9.14 - 10.12  EMG rectified, envelope overlay
        # ────────────────────────────────────────────────────────────
        beat7_dur = max(0.05, 10.12 - 9.14)
        # Morph raw EMG to rectified EMG
        self.play(
            ReplacementTransform(emg_raw_trace, emg_rect_trace),
            FadeOut(label_raw_emg),
            Write(label_rect_emg),
            run_time=max(0.05, beat7_dur * 0.55),
        )
        # Fade in envelope over rectified spikes
        self.play(
            Create(emg_env_trace),
            Write(label_env),
            run_time=max(0.05, beat7_dur * 0.45),
        )

        # ────────────────────────────────────────────────────────────
        # BEAT 8: 10.12 - 11.44  envelope highlighted, pulsing
        # ────────────────────────────────────────────────────────────
        beat8_dur = max(0.05, 11.44 - 10.12)
        # Highlight envelope with color pulse and width change
        self.play(
            emg_env_trace.animate.set_stroke(color=PURPLE, width=4.5),
            run_time=max(0.05, beat8_dur * 0.25),
        )
        # Gentle pulse: scale/wiggle effect simulated by stroke width pulsing
        self.play(
            emg_env_trace.animate.set_stroke(width=6.0),  # broader pulse
            run_time=max(0.05, beat8_dur * 0.15),
        )
        self.play(
            emg_env_trace.animate.set_stroke(width=4.5),  # return
            run_time=max(0.05, beat8_dur * 0.15),
        )
        # Emphasise envelope with surrounding rectangle briefly?
        # Instead, keep it as is, hold
        self.wait(max(0.05, beat8_dur * 0.45))

        # ────────────────────────────────────────────────────────────
        # BEAT 9: 11.44 - 12.40  hold complete example
        #          (fade out upper smoothing example or keep faint)
        # ────────────────────────────────────────────────────────────
        beat9_dur = max(0.05, 12.40 - 11.44)
        # Fade out upper traces to focus on EMG envelope
        self.play(
            upper_group.animate.set_opacity(0.18),
            lower_group.animate.set_opacity(0.18),
            run_time=max(0.05, beat9_dur * 0.5),
        )
        self.wait(max(0.05, beat9_dur * 0.5))

        # ────────────────────────────────────────────────────────────
        # BEAT 10: 12.40 - 13.20  hold static
        # ────────────────────────────────────────────────────────────
        beat10_dur = max(0.05, 13.20 - 12.40)
        self.wait(max(0.05, beat10_dur))