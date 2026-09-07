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

class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ============================================================
        # Spectrum axes + baseline structure (upper half)
        # ============================================================
        spectrum_axis_y = 1.6
        spectrum_axis_left = -6.0
        spectrum_axis_right = 6.0

        spec_axis_line = Line(
            np.array([spectrum_axis_left, spectrum_axis_y, 0]),
            np.array([spectrum_axis_right, spectrum_axis_y, 0]),
            stroke_color=WHITE,
            stroke_width=3,
        )

        spec_tick_freqs = [0, 10, 20, 30, 40, 50, 60]
        spec_tick_marks = VGroup()
        spec_tick_labels = VGroup()
        for freq in spec_tick_freqs:
            x = spectrum_axis_left + (spectrum_axis_right - spectrum_axis_left) * freq / 60.0
            tick = Line(
                np.array([x, spectrum_axis_y - 0.10, 0]),
                np.array([x, spectrum_axis_y + 0.10, 0]),
                stroke_color=GREY_B,
                stroke_width=2,
            )
            label = Text(str(freq), font_size=16, color=GREY)
            label.next_to(tick, DOWN, buff=0.12)
            spec_tick_marks.add(tick)
            spec_tick_labels.add(label)

        spec_freq_label = Text("Frequency (Hz)", font_size=20, color=WHITE)
        spec_freq_label.next_to(spec_axis_line, DOWN, buff=0.30, aligned_edge=RIGHT)

        spec_axis_group = VGroup(spec_axis_line, spec_tick_marks, spec_tick_labels, spec_freq_label)

        # Vertical axis label for magnitude
        mag_label = Text("Magnitude", font_size=18, color=GREY)
        mag_label.rotate(90 * DEGREES)
        mag_label.next_to(spec_axis_line, LEFT, buff=0.55)
        mag_label.shift(UP * 1.0)

        # Build frequency spectrum data (with prominent 50 Hz peak)
        n_spec = 400
        freq_vals = np.linspace(0, 60, n_spec)
        # Base noise floor with scattered peaks
        np.random.seed(42)
        base_spectrum = 0.15 + 0.08 * np.sin(3 * freq_vals) + 0.06 * np.sin(7 * freq_vals) + 0.05 * np.random.rand(n_spec)
        # Tall narrow 50 Hz peak (Gaussian)
        peak_50 = 2.5 * np.exp(-((freq_vals - 50) ** 2) / 0.15)
        # Smaller peaks elsewhere
        peak_15 = 0.70 * np.exp(-((freq_vals - 15) ** 2) / 0.5)
        peak_30 = 0.55 * np.exp(-((freq_vals - 30) ** 2) / 0.6)
        peak_42 = 0.40 * np.exp(-((freq_vals - 42) ** 2) / 0.4)

        spec_mag = base_spectrum + peak_50 + peak_15 + peak_30 + peak_42
        spec_mag_clean = base_spectrum + peak_15 + peak_30 + peak_42  # no 50 Hz

        y_scale_spec = 1.4
        spec_points = [
            np.array([
                spectrum_axis_left + (spectrum_axis_right - spectrum_axis_left) * freq_vals[i] / 60.0,
                spectrum_axis_y + spec_mag[i] * y_scale_spec,
                0
            ])
            for i in range(n_spec)
        ]
        spec_clean_points = [
            np.array([
                spectrum_axis_left + (spectrum_axis_right - spectrum_axis_left) * freq_vals[i] / 60.0,
                spectrum_axis_y + spec_mag_clean[i] * y_scale_spec,
                0
            ])
            for i in range(n_spec)
        ]

        spectrum_curve = VMobject(stroke_color=TEAL, stroke_width=2.8, fill_color=TEAL, fill_opacity=0.12)
        spectrum_curve.set_points_as_corners(spec_points)

        spectrum_curve_clean = VMobject(stroke_color=TEAL, stroke_width=2.8, fill_color=TEAL, fill_opacity=0.12)
        spectrum_curve_clean.set_points_as_corners(spec_clean_points)

        # ============================================================
        # Time-domain waveform (lower half) — with 50 Hz hum
        # ============================================================
        waveform_y = -2.2
        n_wave = 600
        t_wave = np.linspace(0, 6 * np.pi, n_wave)
        wave_x_left = -5.5
        wave_x_right = 5.5
        wave_x_vals = np.linspace(wave_x_left, wave_x_right, n_wave)

        # Neural signal (irregular low freq) + 50 Hz hum
        neural_component = 0.35 * np.sin(1.7 * t_wave) + 0.28 * np.sin(4.2 * t_wave + 0.8) + 0.15 * np.sin(8.0 * t_wave)
        hum_50_component = 0.90 * np.sin(50 * 2 * np.pi * t_wave / 60.0)  # scaled to fit visually
        noisy_wave = neural_component + hum_50_component
        clean_wave = neural_component  # after removing 50 Hz

        wave_y_scale = 0.55
        noisy_wave_points = [
            np.array([wave_x_vals[i], waveform_y + noisy_wave[i] * wave_y_scale, 0])
            for i in range(n_wave)
        ]
        clean_wave_points = [
            np.array([wave_x_vals[i], waveform_y + clean_wave[i] * wave_y_scale, 0])
            for i in range(n_wave)
        ]

        noisy_waveform = VMobject(stroke_color=ORANGE, stroke_width=2.0, stroke_opacity=0.55)
        noisy_waveform.set_points_as_corners(noisy_wave_points)

        clean_waveform = VMobject(stroke_color=GREEN, stroke_width=2.5)
        clean_waveform.set_points_as_corners(clean_wave_points)

        # Waveform labels
        wave_label_noisy = Text("Recording with interference", font_size=22, color=ORANGE)
        wave_label_noisy.next_to(np.array([wave_x_left, waveform_y + 0.75, 0]), RIGHT, buff=0.0)

        wave_label_clean = Text("Filtered signal", font_size=22, color=GREEN)
        wave_label_clean.next_to(np.array([wave_x_left, waveform_y + 0.75, 0]), RIGHT, buff=0.0)

        # ============================================================
        # Notch filter overlay curve
        # ============================================================
        notch_depth_db = -40  # visual depth, not literal dB
        notch_width = 1.0

        # Transfer function: 0 dB flat, deep notch at 50 Hz
        notch_curve_y = spectrum_axis_y + 1.15 * y_scale_spec  # "0 dB" line
        notch_points = []
        for i in range(n_spec):
            x = spectrum_axis_left + (spectrum_axis_right - spectrum_axis_left) * freq_vals[i] / 60.0
            dist_from_50 = abs(freq_vals[i] - 50)
            if dist_from_50 < 0.4:
                depth = notch_depth_db * np.exp(-dist_from_50**2 / 0.08)
            else:
                depth = 0
            y = notch_curve_y + depth * (y_scale_spec / 40.0)  # scale to visual
            notch_points.append(np.array([x, y, 0]))
        # Cap at spectrum_axis_y (the baseline)
        for i in range(len(notch_points)):
            if notch_points[i][1] < spectrum_axis_y + 0.05:
                notch_points[i][1] = spectrum_axis_y + 0.05

        notch_overlay = VMobject(stroke_color=RED, stroke_width=3.5)
        notch_overlay.set_points_as_corners(notch_points)

        # 60 Hz version (for beat 8)
        notch_60_points = []
        for i in range(n_spec):
            x = spectrum_axis_left + (spectrum_axis_right - spectrum_axis_left) * freq_vals[i] / 60.0
            dist_from_60 = abs(freq_vals[i] - 60)
            if dist_from_60 < 0.4:
                depth = notch_depth_db * np.exp(-dist_from_60**2 / 0.08)
            else:
                depth = 0
            y = notch_curve_y + depth * (y_scale_spec / 40.0)
            notch_60_points.append(np.array([x, y, 0]))
        for i in range(len(notch_60_points)):
            if notch_60_points[i][1] < spectrum_axis_y + 0.05:
                notch_60_points[i][1] = spectrum_axis_y + 0.05

        notch_overlay_60 = VMobject(stroke_color=RED, stroke_width=3.5)
        notch_overlay_60.set_points_as_corners(notch_60_points)

        # ============================================================
        # Text labels
        # ============================================================
        interference_label = Text("50 Hz interference", font_size=26, color=YELLOW)
        interference_label.next_to(np.array([spectrum_axis_left + 11.0 * 50/60.0, spectrum_axis_y + 1.8, 0]), UP, buff=0.15)
        # Position near the 50 Hz peak
        peak_50_x = spectrum_axis_left + (spectrum_axis_right - spectrum_axis_left) * 50 / 60.0
        interference_label.move_to(np.array([peak_50_x, spectrum_axis_y + 1.8, 0]), aligned_edge=DOWN)

        removed_label = Text("50 Hz removed", font_size=26, color=GREEN)
        removed_label.move_to(np.array([peak_50_x, spectrum_axis_y + 0.5, 0]))

        or_60_label = Text("or 60 Hz", font_size=24, color=YELLOW)
        peak_60_x = spectrum_axis_left + (spectrum_axis_right - spectrum_axis_left) * 60 / 60.0
        or_60_label.move_to(np.array([peak_60_x, spectrum_axis_y + 1.8, 0]), aligned_edge=DOWN)

        center_text = Text("50 Hz interference removed", font_size=36, color=GREEN, weight="BOLD")
        center_text.move_to(ORIGIN)

        # ============================================================
        # Dashed vertical line at 50 Hz
        # ============================================================
        dash_line_50 = DashedLine(
            np.array([peak_50_x, spectrum_axis_y - 0.4, 0]),
            np.array([peak_50_x, spectrum_axis_y + 2.5, 0]),
            dash_length=0.15,
            dashed_ratio=0.5,
            stroke_color=YELLOW,
            stroke_width=2.5,
        )

        # ============================================================
        # BEAT 1: 0.00 - 1.18 — Spectrum fades in
        # ============================================================
        beat1_dur = max(0.05, 1.18)
        self.play(
            Create(spec_axis_line),
            Write(spec_tick_marks),
            Write(spec_tick_labels),
            Write(spec_freq_label),
            Write(mag_label),
            run_time=max(0.05, beat1_dur * 0.4),
        )
        self.play(
            Create(spectrum_curve),
            run_time=max(0.05, beat1_dur * 0.6),
        )

        # ============================================================
        # BEAT 2: 1.18 - 2.10 — Faint waveform with 50 Hz hum appears
        # ============================================================
        beat2_dur = max(0.05, 2.10 - 1.18)
        self.play(
            FadeIn(noisy_waveform),
            Write(wave_label_noisy),
            run_time=max(0.05, beat2_dur),
        )

        # Gap 2.10 - 2.54
        gap1 = max(0.05, 2.54 - 2.10)
        self.wait(max(0.05, gap1))

        # ============================================================
        # BEAT 3: 2.54 - 3.54 — Dashed line + "50 Hz interference" + pulse
        # ============================================================
        beat3_dur = max(0.05, 3.54 - 2.54)
        self.play(
            Create(dash_line_50),
            Write(interference_label),
            run_time=max(0.05, beat3_dur * 0.5),
        )
        # Pulse the 50 Hz peak region
        self.play(
            spectrum_curve.animate.set_stroke(width=5.5),
            run_time=max(0.05, beat3_dur * 0.15),
            rate_func=there_and_back,
        )
        # Fade out label
        self.play(
            FadeOut(interference_label),
            run_time=max(0.05, beat3_dur * 0.35),
        )

        # Gap 3.54 - 3.84
        gap2 = max(0.05, 3.84 - 3.54)
        self.wait(max(0.05, gap2))

        # ============================================================
        # BEAT 4: 3.84 - 5.60 — Notch filter transfer function overlays
        # ============================================================
        beat4_dur = max(0.05, 5.60 - 3.84)
        self.play(
            Create(notch_overlay),
            run_time=max(0.05, beat4_dur),
        )

        # ============================================================
        # BEAT 5: 5.60 - 6.20 — Hold static with notch aligned
        # ============================================================
        beat5_dur = max(0.05, 6.20 - 5.60)
        self.wait(max(0.05, beat5_dur))

        # Gap 6.20 - 6.94
        gap3 = max(0.05, 6.94 - 6.20)
        self.wait(max(0.05, gap3))

        # ============================================================
        # BEAT 6: 6.94 - 8.54 — 50 Hz peak shrinks, notch fades, "50 Hz removed"
        # ============================================================
        beat6_dur = max(0.05, 8.54 - 6.94)
        # Morph spectrum to clean version (no 50 Hz peak)
        self.play(
            Transform(spectrum_curve, spectrum_curve_clean),
            FadeOut(notch_overlay),
            FadeOut(dash_line_50),
            run_time=max(0.05, beat6_dur * 0.7),
        )
        # Show "50 Hz removed"
        self.play(
            Write(removed_label),
            run_time=max(0.05, beat6_dur * 0.15),
        )
        self.play(
            FadeOut(removed_label),
            run_time=max(0.05, beat6_dur * 0.15),
        )

        # ============================================================
        # BEAT 7: 8.54 - 9.92 — Waveform cleans up (50 Hz hum fades)
        # ============================================================
        beat7_dur = max(0.05, 9.92 - 8.54)
        self.play(
            Transform(noisy_waveform, clean_waveform),
            FadeOut(wave_label_noisy),
            FadeIn(wave_label_clean),
            run_time=max(0.05, beat7_dur),
        )

        # Gap 9.92 - 10.40
        gap4 = max(0.05, 10.40 - 9.92)
        self.wait(max(0.05, gap4))

        # ============================================================
        # BEAT 8: 10.40 - 11.32 — 60 Hz notch briefly appears + "or 60 Hz"
        # ============================================================
        beat8_dur = max(0.05, 11.32 - 10.40)
        self.play(
            Create(notch_overlay_60),
            Write(or_60_label),
            run_time=max(0.05, beat8_dur * 0.5),
        )
        self.play(
            FadeOut(notch_overlay_60),
            FadeOut(or_60_label),
            run_time=max(0.05, beat8_dur * 0.5),
        )

        # Gap 11.32 - 11.58
        gap5 = max(0.05, 11.58 - 11.32)
        self.wait(max(0.05, gap5))

        # ============================================================
        # BEAT 9: 11.58 - 12.76 — Center text flash + hold
        # ============================================================
        beat9_dur = max(0.05, 12.76 - 11.58)
        self.play(
            Write(center_text),
            run_time=max(0.05, beat9_dur * 0.35),
        )
        # Flash by briefly scaling up and back
        self.play(
            center_text.animate.scale(1.15),
            run_time=max(0.05, beat9_dur * 0.15),
        )
        self.play(
            center_text.animate.scale(1 / 1.15),
            run_time=max(0.05, beat9_dur * 0.15),
        )
        self.play(
            FadeOut(center_text),
            run_time=max(0.05, beat9_dur * 0.35),
        )

        # ============================================================
        # BEAT 10: 12.76 - 13.68 — Hold final cleaned state
        # ============================================================
        beat10_dur = max(0.05, 13.68 - 12.76)
        self.wait(max(0.05, beat10_dur))