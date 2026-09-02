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
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene12(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helper: generate a raw noisy signal ----------
        def make_raw_signal(seed, n_pts=200):
            rng = np.random.RandomState(seed)
            t = np.linspace(0, 4 * np.pi, n_pts)
            drift = 0.4 * np.sin(0.5 * t)
            mid_freq = 0.5 * np.sin(3.0 * t + 1.2)
            noise = rng.randn(n_pts) * 0.15
            return drift + mid_freq + noise

        # ---------- helper: draw a trace inside a given rect ----------
        def make_trace_in_rect(signal, rect, color, stroke_w=2):
            w = rect.width * 0.85
            h = rect.height * 0.38
            n = len(signal)
            x_vals = np.linspace(-w / 2, w / 2, n)
            y_vals = signal - np.mean(signal)
            y_vals = y_vals / (np.max(np.abs(y_vals)) * 1.1 + 1e-12) * (h / 2)
            points = [np.array([x_vals[i], y_vals[i], 0]) for i in range(n)]
            trace = VMobject(stroke_color=color, stroke_width=stroke_w, fill_opacity=0)
            trace.set_points_as_corners(points)
            trace.move_to(rect.get_center() + UP * rect.height * 0.18)
            return trace

        # ---------- helper: draw filtered signal variants ----------
        def low_pass(sig, alpha=0.08):
            out = np.zeros_like(sig)
            out[0] = sig[0]
            for i in range(1, len(sig)):
                out[i] = alpha * sig[i] + (1 - alpha) * out[i - 1]
            return out

        def high_pass(sig, alpha=0.95):
            out = np.zeros_like(sig)
            out[0] = sig[0]
            for i in range(1, len(sig)):
                out[i] = alpha * (out[i - 1] + sig[i] - sig[i - 1])
            return out

        def band_pass(sig, low=0.05, high=0.15):
            lp = low_pass(sig, low)
            return high_pass(lp, high)

        def moving_avg(sig, window=10):
            return np.convolve(sig, np.ones(window) / window, mode='same')

        def median_filter(sig, window=7):
            out = np.zeros_like(sig)
            half = window // 2
            n = len(sig)
            for i in range(n):
                start = max(0, i - half)
                end = min(n, i + half + 1)
                out[i] = np.median(sig[start:end])
            return out

        # ---------- build the 2x3 grid ----------
        window_w, window_h = 3.6, 2.0
        gap_x, gap_y = 0.45, 0.55
        rows, cols = 2, 3
        grid_center = ORIGIN + UP * 0.2

        # positions of all 6 windows
        xs = [(c - (cols - 1) / 2) * (window_w + gap_x) for c in range(cols)]
        ys = [(r - (rows - 1) / 2) * (window_h + gap_y) for r in range(rows)]
        positions_2x3 = [[np.array([xs[c], -ys[r], 0]) + grid_center for c in range(cols)] for r in range(rows)]

        labels_top = ["Low-pass", "High-pass", "Band-pass"]
        labels_bot = ["Notch", "Moving-average", "Median"]
        all_labels = labels_top + labels_bot

        windows = []
        raw_traces = []
        lower_lines = []
        label_mobs = []

        seeds = [10, 20, 30, 40, 50, 60]
        raw_signals = [make_raw_signal(s, 200) for s in seeds]

        for idx in range(6):
            r, c = divmod(idx, 3)
            pos = positions_2x3[r][c]

            rect = Rectangle(
                width=window_w, height=window_h,
                fill_color="#1A1D24", fill_opacity=1.0,
                stroke_color="#3A3D44", stroke_width=1.5,
            )
            rect.move_to(pos)

            raw_sig = raw_signals[idx]
            raw_tr = make_trace_in_rect(raw_sig, rect, "#88AACC", stroke_w=2)

            # dim lower reference line
            ref_line = Line(
                start=rect.get_left() + RIGHT * rect.width * 0.08 + DOWN * rect.height * 0.2,
                end=rect.get_right() + LEFT * rect.width * 0.08 + DOWN * rect.height * 0.2,
                stroke_color="#3A3D44", stroke_width=1,
            )

            lbl = Text(all_labels[idx], font_size=16, color="#555555", weight=BOLD)
            lbl.next_to(rect, DOWN, buff=0.12)

            windows.append(rect)
            raw_traces.append(raw_tr)
            lower_lines.append(ref_line)
            label_mobs.append(lbl)

        window_group = VGroup(*[VGroup(w, r, lr, lb) for w, r, lr, lb in zip(windows, raw_traces, lower_lines, label_mobs)])

        # ---------- filtered signals for the lower traces ----------
        filtered_signals = {
            0: low_pass(raw_signals[0], alpha=0.06),
            1: high_pass(raw_signals[1], alpha=0.94),
            2: band_pass(raw_signals[2], low=0.05, high=0.15),
            3: high_pass(raw_signals[3], alpha=0.99),  # notch-like: remove low hum
            4: moving_avg(raw_signals[4], window=12),
            5: median_filter(raw_signals[5], window=9),
        }

        low_traces = [None] * 6
        for idx in range(6):
            lt = make_trace_in_rect(filtered_signals[idx], windows[idx], "#88AACC", stroke_w=2)
            lt.move_to(windows[idx].get_center() + DOWN * windows[idx].height * 0.18)
            lt.set_opacity(0)
            low_traces[idx] = lt

        # ---------- BEAT 1: 0.00 → 8.62 ----------
        beat1_dur = 8.62
        self.play(
            FadeIn(window_group, shift=UP * 0.3),
            run_time=max(0.05, 1.5
        ))
        self.wait(max(0.05, beat1_dur - 1.5))

        # ---------- BEAT 2: 8.62 → 12.94 (4.32 s) ----------
        beat2_dur = 4.32

        # surge extra jitter + burst
        surge_signals = []
        for sig in raw_signals:
            rng = np.random.RandomState(99)
            burst = np.zeros_like(sig)
            burst[80:110] = 1.8 * np.sin(np.linspace(0, 6 * np.pi, 30))
            surge_sig = sig + rng.randn(len(sig)) * 0.55 + burst
            surge_signals.append(surge_sig)

        surge_traces = []
        for idx in range(6):
            st = make_trace_in_rect(surge_signals[idx], windows[idx], "#FF6666", stroke_w=2.5)
            st.move_to(raw_traces[idx].get_center())
            st.set_opacity(0)
            surge_traces.append(st)

        # fade in surge
        surge_anims = [st.animate.set_opacity(1) for st in surge_traces]
        surge_fade_outs = [rt.animate.set_opacity(0) for rt in raw_traces]
        self.play(
            AnimationGroup(*(surge_anims + surge_fade_outs), lag_ratio=0.0),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.8))

        # fade back to normal
        restore_anims = []
        for idx in range(6):
            restore_anims.append(surge_traces[idx].animate.set_opacity(0))
            restore_anims.append(raw_traces[idx].animate.set_opacity(1))
        self.play(AnimationGroup(*restore_anims, lag_ratio=0.0), run_time=max(0.05, 1.2))
        self.wait(max(0.05, beat2_dur - 1.2 - 0.8 - 1.2))

        # remove surge traces
        for st in surge_traces:
            self.remove(st)

        # ---------- BEAT 3: 12.94 → 18.06 (5.12 s) Low-pass ----------
        beat3_dur = 5.12
        idx = 0
        rect = windows[idx]
        glow = SurroundingRectangle(rect, color=GREEN, stroke_width=3, buff=0.06)

        lt = low_traces[idx]
        self.play(
            Create(glow),
            label_mobs[idx].animate.set_color(WHITE),
            lt.animate.set_opacity(1),
            run_time=max(0.05, min(beat3_dur * 0.7, 2.5)),
        )
        self.wait(max(0.05, beat3_dur - min(beat3_dur * 0.7, 2.5)))

        glow_lp = glow

        # ---------- BEAT 4: 18.06 → 23.66 (5.60 s) High-pass ----------
        beat4_dur = 5.60
        idx = 1
        rect = windows[idx]
        glow_hp = SurroundingRectangle(rect, color=BLUE, stroke_width=3, buff=0.06)
        lt = low_traces[idx]

        self.play(
            Create(glow_hp),
            label_mobs[idx].animate.set_color(WHITE),
            lt.animate.set_opacity(1),
            run_time=max(0.05, min(beat4_dur * 0.7, 2.5)),
        )
        self.wait(max(0.05, beat4_dur - min(beat4_dur * 0.7, 2.5)))

        # ---------- BEAT 5: 23.66 → 27.72 (4.06 s) Band-pass ----------
        beat5_dur = 4.06
        idx = 2
        rect = windows[idx]
        glow_bp = SurroundingRectangle(rect, color=PURPLE, stroke_width=3, buff=0.06)
        lt = low_traces[idx]

        self.play(
            Create(glow_bp),
            label_mobs[idx].animate.set_color(WHITE),
            lt.animate.set_opacity(1),
            run_time=max(0.05, min(beat5_dur * 0.7, 2.5)),
        )
        self.wait(max(0.05, beat5_dur - min(beat5_dur * 0.7, 2.5)))

        # ---------- BEAT 6: 27.72 → 32.20 (4.48 s) Notch ----------
        beat6_dur = 4.48
        idx = 3
        rect = windows[idx]
        glow_notch = SurroundingRectangle(rect, color=ORANGE, stroke_width=3, buff=0.06)
        lt = low_traces[idx]

        self.play(
            Create(glow_notch),
            label_mobs[idx].animate.set_color(WHITE),
            lt.animate.set_opacity(1),
            run_time=max(0.05, min(beat6_dur * 0.7, 2.5)),
        )
        self.wait(max(0.05, beat6_dur - min(beat6_dur * 0.7, 2.5)))

        # ---------- BEAT 7: 32.20 → 36.62 (4.42 s) Moving-average ----------
        beat7_dur = 4.42
        idx = 4
        rect = windows[idx]
        glow_ma = SurroundingRectangle(rect, color=YELLOW, stroke_width=3, buff=0.06)
        lt = low_traces[idx]

        self.play(
            Create(glow_ma),
            label_mobs[idx].animate.set_color(WHITE),
            lt.animate.set_opacity(1),
            run_time=max(0.05, min(beat7_dur * 0.7, 2.5)),
        )
        self.wait(max(0.05, beat7_dur - min(beat7_dur * 0.7, 2.5)))

        # ---------- BEAT 8: 36.62 → 48.96 (12.34 s) Median ----------
        beat8_dur = 12.34
        idx = 5
        rect = windows[idx]
        glow_med = SurroundingRectangle(rect, color=RED, stroke_width=3, buff=0.06)
        lt = low_traces[idx]

        self.play(
            Create(glow_med),
            label_mobs[idx].animate.set_color(WHITE),
            lt.animate.set_opacity(1),
            run_time=max(0.05, min(beat8_dur * 0.4, 3.0)),
        )
        self.wait(max(0.05, beat8_dur - min(beat8_dur * 0.4, 3.0)))

        # collect all glow rectangles
        all_glows = [glow_lp, glow_hp, glow_bp, glow_notch, glow_ma, glow_med]

        # ---------- BEAT 9: 48.96 → 53.30 (4.34 s) Shrink + move up, timeline appears ----------
        beat9_dur = 4.34

        # targets for each window in the top quarter
        small_w, small_h = window_w * 0.55, window_h * 0.55
        small_gap_x, small_gap_y = gap_x * 0.55, gap_y * 0.55
        xs_small = [(c - (cols - 1) / 2) * (small_w + small_gap_x) for c in range(cols)]
        ys_small = [(r - (rows - 1) / 2) * (small_h + small_gap_y) for r in range(rows)]
        small_positions = [[np.array([xs_small[c], -ys_small[r] + 3.0, 0]) for c in range(cols)] for r in range(rows)]

        anims_shrink = []
        for idx in range(6):
            r, c = divmod(idx, 3)
            target_pos = small_positions[r][c]

            # shrink rect
            rect_anim = windows[idx].animate.stretch_to_fit_width(small_w).stretch_to_fit_height(small_h).move_to(target_pos)
            anims_shrink.append(rect_anim)

            # raw trace
            anims_shrink.append(raw_traces[idx].animate.move_to(target_pos + UP * small_h * 0.18).scale(0.55))
            anims_shrink.append(low_traces[idx].animate.move_to(target_pos + DOWN * small_h * 0.18).scale(0.55))
            anims_shrink.append(lower_lines[idx].animate.move_to(target_pos + DOWN * small_h * 0.18).scale(0.55))

            # glow
            anims_shrink.append(all_glows[idx].animate.stretch_to_fit_width(small_w).stretch_to_fit_height(small_h).move_to(target_pos))

            # label
            anims_shrink.append(label_mobs[idx].animate.next_to(
                Rectangle(width=small_w, height=small_h).move_to(target_pos), DOWN, buff=0.08
            ).scale(0.65))

        toptime_y = -1.8  # lower 3/4 area starts here roughly

        # timeline
        timeline = Line(
            start=np.array([-5.5, toptime_y + 0.5, 0]),
            end=np.array([5.5, toptime_y + 0.5, 0]),
            stroke_color="#555555", stroke_width=2,
        )
        timeline.set_opacity(0.3)

        # sliding window graphic
        slide_rect = Rectangle(
            width=0.7, height=0.35,
            fill_color="#3A3D44", fill_opacity=0.7,
            stroke_color="#888888", stroke_width=1,
        )
        slide_rect.move_to(np.array([-5.5 + 0.35, toptime_y + 0.5, 0]))

        # T markers
        t_marks = VGroup()
        for t_x in np.linspace(-5.5, 5.5, 11):
            tick = Line(
                start=np.array([t_x, toptime_y + 0.5 - 0.1, 0]),
                end=np.array([t_x, toptime_y + 0.5 + 0.1, 0]),
                stroke_color="#555555", stroke_width=1,
            )
            t_marks.add(tick)

        timeline_grp = VGroup(timeline, t_marks, slide_rect)
        timeline_grp.set_opacity(0.3)

        self.play(
            AnimationGroup(*anims_shrink, lag_ratio=0.0),
            FadeIn(timeline_grp),
            run_time=max(0.05, min(beat9_dur * 0.8, 3.5)),
        )
        self.wait(max(0.05, beat9_dur - min(beat9_dur * 0.8, 3.5)))

        # ---------- BEAT 10: 53.30 → 60.30 (7.00 s) Sliding window + spectrogram ----------
        beat10_dur = 7.00

        # brighten timeline
        self.play(
            timeline_grp.animate.set_opacity(1),
            run_time=max(0.05, 0.6),
        )
        beat10_remaining = beat10_dur - 0.6

        # sliding window moves left to right
        slide_path = np.array([11.0, 0, 0])  # full width travel

        # spectrogram: build columns as sliding window advances
        spec_cols_n = 50
        spec_col_w = 0.18
        spec_col_h = 2.8
        spec_bottom = toptime_y - 0.5 - spec_col_h / 2
        spec_xs = np.linspace(-5.2, 5.2, spec_cols_n)

        spectro_cols = VGroup()
        for i in range(spec_cols_n):
            col = Rectangle(
                width=spec_col_w, height=spec_col_h,
                fill_color=BLUE, fill_opacity=0.0,
                stroke_width=0,
            )
            col.move_to(np.array([spec_xs[i], spec_bottom, 0]))
            col.target_opacity = 0.9
            spectro_cols.add(col)

        # animate sliding window
        num_frames = 15
        frame_dur = beat10_remaining / num_frames

        slide_start = slide_rect.get_center()[0]
        slide_end = slide_start + 11.0

        for f_idx in range(num_frames):
            alpha = (f_idx + 1) / num_frames
            new_x = slide_start + alpha * 11.0
            slide_pos = np.array([new_x, toptime_y + 0.5, 0])

            cols_to_reveal = max(1, int(alpha * spec_cols_n))
            anims = [slide_rect.animate.move_to(slide_pos)]

            for c in range(min(cols_to_reveal, spec_cols_n)):
                if spectro_cols[c].fill_opacity < 0.01:
                    col = spectro_cols[c]
                    hue = (c / spec_cols_n) * 0.6 + 0.55
                    anims.append(col.animate.set_fill(
                        interpolate_color(BLUE, TEAL, (c % 10) / 9),
                        opacity=0.85,
                    ))

            self.play(AnimationGroup(*anims), run_time=max(0.05, frame_dur))

        # ensure spectrogram is fully built
        for col in spectro_cols:
            if col.fill_opacity < 0.01:
                col.set_fill(
                    interpolate_color(BLUE, TEAL, np.random.random()),
                    opacity=0.85,
                )
        self.wait(max(0.05, beat10_dur - 0.6 - beat10_remaining))

        # ---------- BEAT 11: 60.30 → 61.58 (1.28 s) Wavelet scale graphic ----------
        beat11_dur = 1.28

        wavelet_group = VGroup()
        wavelet_scales = [0.4, 0.65, 1.0, 1.5, 2.2]
        wavelet_y = toptime_y - 0.8
        wavelet_x = 6.3

        for i, sc in enumerate(wavelet_scales):
            y_pos = wavelet_y - i * 0.55
            t = np.linspace(-1.5, 1.5, 120)
            wav_sig = np.cos(5 * t) * np.exp(-t**2 / (0.3 * sc))
            wav_sig = wav_sig / (np.max(np.abs(wav_sig)) + 1e-12) * 0.2 * sc

            pts = [np.array([wavelet_x + t_i * 0.5, y_pos + wav_sig[i], 0]) for i, t_i in enumerate(t)]
            wav_line = VMobject(stroke_color=PURPLE, stroke_width=1.5, fill_opacity=0)
            wav_line.set_points_as_corners(pts)

            lbl = Text(f"scale {sc:.1f}", font_size=11, color="#888888")
            lbl.next_to(wav_line, RIGHT, buff=0.1)
            wavelet_group.add(VGroup(wav_line, lbl))

        wavelet_group.scale_to_fit_height(2.2)
        wavelet_group.move_to(np.array([6.2, toptime_y - 1.3, 0]))
        wavelet_group.set_opacity(0)

        self.play(FadeIn(wavelet_group), run_time=max(0.05, min(beat11_dur, 1.0)))
        self.wait(max(0.05, beat11_dur - min(beat11_dur, 1.0)))

        # ---------- BEAT 12: 61.58 → 62.98 (1.40 s) ERP plot ----------
        beat12_dur = 1.40

        erp_group = VGroup()
        erp_x = 6.2
        erp_bottom = toptime_y - 3.0

        # ERP waveform
        erp_t = np.linspace(-0.2, 0.8, 200)
        erp_sig = (
            -1.2 * np.exp(-((erp_t - 0.1) ** 2) / 0.015)   # N1
            + 1.5 * np.exp(-((erp_t - 0.2) ** 2) / 0.02)   # P2
            - 0.9 * np.exp(-((erp_t - 0.3) ** 2) / 0.025)   # N2
        )
        erp_sig = erp_sig / np.max(np.abs(erp_sig)) * 0.5

        erp_pts = [np.array([erp_x + erp_t[i] * 1.8, erp_bottom + erp_sig[i], 0]) for i in range(len(erp_t))]
        erp_line = VMobject(stroke_color="#FFCC66", stroke_width=2.5, fill_opacity=0)
        erp_line.set_points_as_corners(erp_pts)

        # axis
        axis = Line(
            start=np.array([erp_x - 0.5, erp_bottom, 0]),
            end=np.array([erp_x + 1.6, erp_bottom, 0]),
            stroke_color="#888888", stroke_width=1.5,
        )

        # peak markers
        peaks = {
            "N1": (0.1, -1.2, RED),
            "P2": (0.2, 1.5, GREEN),
            "N2": (0.3, -0.9, YELLOW),
        }
        peak_dots = VGroup()
        for name, (tp, amp, col) in peaks.items():
            xp = erp_x + tp * 1.8
            yp = erp_bottom + (amp / np.max(np.abs(erp_sig))) * 0.5
            dot = Dot(point=np.array([xp, yp, 0]), color=col, radius=0.06)
            lbl = Text(name, font_size=14, color=col, weight=BOLD)
            lbl.next_to(dot, UP, buff=0.08)
            peak_dots.add(dot, lbl)

        erp_group.add(axis, erp_line, peak_dots)
        erp_group.scale_to_fit_height(1.1)
        erp_group.move_to(np.array([6.2, toptime_y - 2.8, 0]))
        erp_group.set_opacity(0)

        self.play(FadeIn(erp_group), run_time=max(0.05, min(beat12_dur, 1.0)))
        self.wait(max(0.05, beat12_dur - min(beat12_dur, 1.0)))

        # ---------- BEAT 13: 62.98 → 66.40 (3.42 s) "Next: Non-stationary signals" ----------
        beat13_dur = 66.40 - 62.98

        next_text = Text(
            "Next: Non-stationary signals",
            font_size=32, color=WHITE, weight=BOLD,
        )
        next_text.to_edge(DOWN, buff=0.3)
        # subtle shadow via a second copy
        shadow = Text(
            "Next: Non-stationary signals",
            font_size=32, color="#000000", weight=BOLD,
        )
        shadow.move_to(next_text.get_center() + np.array([0.04, -0.04, 0]))
        shadow.set_opacity(0.6)

        next_group = VGroup(shadow, next_text)
        next_group.set_opacity(0)

        self.play(FadeIn(next_group, shift=UP * 0.2), run_time=max(0.05, 1.2))
        beat13_remaining = beat13_dur - 1.2

        # continue sliding window + spectrogram fill for remaining time
        if beat13_remaining > 0.2:
            num_extra_frames = int(beat13_remaining / 0.35)
            for f_idx in range(num_extra_frames):
                alpha = min(1.0, 0.9 + (f_idx + 1) * 0.007)
                new_x = slide_start + alpha * 11.0
                new_x = min(new_x, slide_start + 10.8)
                self.play(
                    slide_rect.animate.move_to(np.array([new_x, toptime_y + 0.5, 0])),
                    run_time=max(0.05, 0.35),
                )
            self.wait(max(0.05, beat13_remaining - num_extra_frames * 0.35))
        else:
            self.wait(max(0.05, beat13_remaining))

        # ensure total duration
        self.wait(max(0.05, 66.40 - self.renderer.time))