ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


def generate_eeg_trace(num_points=500, duration=4.0, seed=42):
    """Generate a composite EEG-like signal."""
    np.random.seed(seed)
    t = np.linspace(0, duration, num_points)
    drift = 0.8 * np.sin(2 * np.pi * 0.3 * t) + 0.4 * np.cos(2 * np.pi * 0.15 * t)
    brain = 1.2 * np.sin(2 * np.pi * 10.0 * t) + 0.6 * np.sin(2 * np.pi * 20.0 * t)
    noise = 0.3 * np.random.randn(num_points)
    composite = drift + brain + noise
    return t, composite, drift, brain, noise


def generate_filtered_eeg(num_points=500, duration=4.0, seed=42):
    """Generate the band-pass filtered (1-40 Hz) EEG signal."""
    np.random.seed(seed)
    t = np.linspace(0, duration, num_points)
    brain = 1.2 * np.sin(2 * np.pi * 10.0 * t) + 0.6 * np.sin(2 * np.pi * 20.0 * t)
    return t, brain


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- layout ----------
        panel_width = 12.0
        panel_height = 2.4
        top_panel_center = np.array([0, 1.8, 0])
        bottom_panel_center = np.array([0, -1.8, 0])
        gap_between_panels = 1.2

        num_points = 600
        t_raw, composite_raw, drift_raw, brain_raw, noise_raw = generate_eeg_trace(
            num_points=num_points, duration=5.0, seed=123
        )
        t_filt, clean_signal = generate_filtered_eeg(
            num_points=num_points, duration=5.0, seed=123
        )

        def map_to_panel(signal, center_y, height, amp_scale=0.8):
            max_val = max(np.abs(signal).max(), 1e-9)
            scaled = signal / max_val * amp_scale * height / 2
            x_vals = np.linspace(
                center_y[0] - panel_width / 2,
                center_y[0] + panel_width / 2,
                len(signal),
            )
            points = [
                np.array([x_vals[i], center_y[1] + scaled[i], 0])
                for i in range(len(signal))
            ]
            return points

        raw_points = map_to_panel(composite_raw, top_panel_center, panel_height, amp_scale=0.85)
        filtered_points = map_to_panel(clean_signal, bottom_panel_center, panel_height, amp_scale=0.85)

        raw_trace = VMobject(color=GREY, stroke_width=2)
        raw_trace.set_points_as_corners(raw_points)
        raw_trace.set_z_index(2)

        filtered_trace = VMobject(color=TEAL, stroke_width=2.5)
        filtered_trace.set_points_as_corners(filtered_points)
        filtered_trace.set_z_index(2)
        filtered_trace.set_opacity(0)

        # panel backgrounds
        top_panel_bg = Rectangle(
            width=panel_width + 0.6,
            height=panel_height + 0.6,
            fill_color="#1A1D24",
            fill_opacity=1,
            stroke_color=GREY,
            stroke_width=1,
        )
        top_panel_bg.move_to(top_panel_center)
        top_panel_bg.set_z_index(0)

        bottom_panel_bg = Rectangle(
            width=panel_width + 0.6,
            height=panel_height + 0.6,
            fill_color="#1A1D24",
            fill_opacity=1,
            stroke_color=GREY,
            stroke_width=1,
        )
        bottom_panel_bg.move_to(bottom_panel_center)
        bottom_panel_bg.set_z_index(0)
        bottom_panel_bg.set_opacity(0)  # hidden until beat 8

        # labels
        top_label = Text("Raw EEG", font_size=28, color=GREY, weight="BOLD")
        top_label.next_to(top_panel_bg, UP, buff=0.15)
        top_label.set_z_index(3)

        bottom_label = Text("Filtered EEG (1–40 Hz)", font_size=28, color=TEAL, weight="BOLD")
        bottom_label.next_to(bottom_panel_bg, UP, buff=0.15)
        bottom_label.set_z_index(3)
        bottom_label.set_opacity(0)  # hidden until beat 8

        # ---------- Beat 1: 0.00–2.64 ----------
        # Fade in the whole top panel (background, label, trace)
        self.play(
            FadeIn(top_panel_bg),
            FadeIn(top_label),
            FadeIn(raw_trace),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 2.64 - 1.5))

        # ---------- Beat 2: 2.64–4.44 ----------
        drift_highlight = Rectangle(
            width=panel_width,
            height=0.25,
            fill_color=ORANGE,
            fill_opacity=0.35,
            stroke_width=0,
        )
        drift_highlight.move_to(top_panel_center)
        drift_highlight.set_z_index(1)

        drift_label = Text("slow baseline drift", font_size=22, color=ORANGE, weight="BOLD")
        drift_label.next_to(drift_highlight, DOWN, buff=0.5)

        self.play(
            FadeIn(drift_highlight),
            Write(drift_label),
            run_time=max(0.05, 0.8),
        )
        self.play(
            drift_highlight.animate.set_opacity(0.55),
            run_time=max(0.05, 0.3),
        )
        self.play(
            drift_highlight.animate.set_opacity(0.35),
            run_time=max(0.05, 0.3),
        )
        self.wait(max(0.05, 4.44 - 2.64 - 0.8 - 0.3 - 0.3))

        # Gap before beat 3: 4.44 → 4.94 = 0.50 s
        self.wait(max(0.05, 0.50))

        # ---------- Beat 3: 4.94–5.50 ----------
        brain_highlight = Rectangle(
            width=panel_width,
            height=0.25,
            fill_color=GREEN,
            fill_opacity=0.35,
            stroke_width=0,
        )
        brain_highlight.move_to(top_panel_center)
        brain_highlight.set_z_index(1)

        brain_label = Text("brain activity", font_size=22, color=GREEN, weight="BOLD")
        brain_label.next_to(brain_highlight, DOWN, buff=0.5)

        self.play(
            FadeOut(drift_highlight),
            FadeOut(drift_label),
            FadeIn(brain_highlight),
            Write(brain_label),
            run_time=max(0.05, 0.3),
        )
        self.wait(max(0.05, 5.50 - 4.94 - 0.3))

        # Gap before beat 4: 5.50 → 6.32 = 0.82 s
        self.wait(max(0.05, 0.82))

        # ---------- Beat 4: 6.32–7.88 ----------
        noise_highlight = Rectangle(
            width=panel_width,
            height=0.25,
            fill_color=RED,
            fill_opacity=0.35,
            stroke_width=0,
        )
        noise_highlight.move_to(top_panel_center)
        noise_highlight.set_z_index(1)

        noise_label = Text("electrical noise", font_size=22, color=RED, weight="BOLD")
        noise_label.next_to(noise_highlight, DOWN, buff=0.5)

        self.play(
            FadeOut(brain_highlight),
            FadeOut(brain_label),
            FadeIn(noise_highlight),
            Write(noise_label),
            run_time=max(0.05, 0.3),
        )
        self.wait(max(0.05, 7.88 - 6.32 - 0.3))

        # Gap before beat 5: 7.88 → 8.62 = 0.74 s
        self.wait(max(0.05, 0.74))

        # ---------- Beat 5: 8.62–11.18 ----------
        self.play(
            FadeOut(noise_highlight),
            FadeOut(noise_label),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 11.18 - 8.62 - 0.5))

        # Gap before beat 6: 11.18 → 11.80 = 0.62 s
        self.wait(max(0.05, 0.62))

        # ---------- Beat 6: 11.80–13.34 ----------
        inset_width = 3.0
        inset_height = 1.8
        inset_center = np.array([0, 0.0, 0])

        inset_bg = Rectangle(
            width=inset_width + 0.4,
            height=inset_height + 0.4,
            fill_color="#1A1D24",
            fill_opacity=1,
            stroke_color=GREY,
            stroke_width=1,
        )
        inset_bg.move_to(inset_center)
        inset_bg.set_z_index(3)

        inset_axis = Line(
            start=inset_center + LEFT * (inset_width / 2),
            end=inset_center + RIGHT * (inset_width / 2),
            color=WHITE,
            stroke_width=2,
        )
        inset_axis.set_z_index(4)

        freq_label_inset = Text("Frequency (Hz)", font_size=20, color=GREY)
        freq_label_inset.next_to(inset_axis, DOWN, buff=0.1)
        freq_label_inset.set_z_index(4)

        inset_freq_max = 50.0
        inset_axis_length = inset_width
        inset_x_scale = inset_axis_length / inset_freq_max
        x_1hz_inset = inset_center[0] - inset_axis_length / 2 + 1.0 * inset_x_scale
        x_40hz_inset = inset_center[0] - inset_axis_length / 2 + 40.0 * inset_x_scale

        dashed_1hz = DashedLine(
            start=np.array([x_1hz_inset, inset_center[1] - 0.5, 0]),
            end=np.array([x_1hz_inset, inset_center[1] + 0.5, 0]),
            color=GOLD,
            dash_length=0.15,
            stroke_width=2,
        )
        dashed_1hz.set_z_index(4)

        dashed_40hz = DashedLine(
            start=np.array([x_40hz_inset, inset_center[1] - 0.5, 0]),
            end=np.array([x_40hz_inset, inset_center[1] + 0.5, 0]),
            color=GOLD,
            dash_length=0.15,
            stroke_width=2,
        )
        dashed_40hz.set_z_index(4)

        band_fill = Rectangle(
            width=x_40hz_inset - x_1hz_inset,
            height=1.0,
            fill_color=GREEN,
            fill_opacity=0.25,
            stroke_width=0,
        )
        band_fill.move_to(np.array([(x_1hz_inset + x_40hz_inset) / 2, inset_center[1], 0]))
        band_fill.set_z_index(3)

        band_label_inset = Text("1–40 Hz band", font_size=18, color=GREEN, weight="BOLD")
        band_label_inset.next_to(band_fill, UP, buff=0.15)
        band_label_inset.set_z_index(4)

        tick_1hz = Text("1", font_size=18, color=GOLD)
        tick_1hz.next_to(dashed_1hz, DOWN, buff=0.05)
        tick_1hz.set_z_index(4)

        tick_40hz = Text("40", font_size=18, color=GOLD)
        tick_40hz.next_to(dashed_40hz, DOWN, buff=0.05)
        tick_40hz.set_z_index(4)

        inset_group = VGroup(
            inset_bg, inset_axis, freq_label_inset,
            dashed_1hz, dashed_40hz, band_fill, band_label_inset,
            tick_1hz, tick_40hz,
        )

        self.play(
            FadeIn(inset_group),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 13.34 - 11.80 - 1.0))

        # Gap before beat 7: 13.34 → 13.94 = 0.60 s
        self.wait(max(0.05, 0.60))

        # ---------- Beat 7: 13.94–15.40 ----------
        arrow_filter = Arrow(
            start=top_panel_center + DOWN * 1.5,
            end=bottom_panel_center + UP * 1.5,
            color=TEAL,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.12,
            buff=0,
        )
        arrow_filter.set_z_index(3)

        arrow_label = Text(
            "Band‑pass filter (1–40 Hz)",
            font_size=22,
            color=TEAL,
            weight="BOLD",
        )
        arrow_label.next_to(arrow_filter, RIGHT, buff=0.3)
        arrow_label.set_z_index(4)

        self.play(
            GrowFromCenter(arrow_filter),
            Write(arrow_label),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 15.40 - 13.94 - 0.6))

        # ---------- Beat 8: 15.40–19.02 ----------
        # Reveal bottom panel and cross-fade traces
        self.play(
            FadeIn(bottom_panel_bg),
            bottom_label.animate.set_opacity(1),
            run_time=max(0.05, 0.5),
        )
        self.play(
            raw_trace.animate.set_opacity(0.25),
            FadeIn(filtered_trace),
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 19.02 - 15.40 - 0.5 - 2.5))

        # Gap before beat 9: 19.02 → 20.22 = 1.20 s
        self.wait(max(0.05, 1.20))

        # ---------- Beat 9: 20.22–25.60 ----------
        left_dark = Rectangle(
            width=x_1hz_inset - (inset_center[0] - inset_axis_length / 2),
            height=1.0,
            fill_color="#0F1116",
            fill_opacity=0.7,
            stroke_width=0,
        )
        left_dark.move_to(
            np.array([
                (inset_center[0] - inset_axis_length / 2 + x_1hz_inset) / 2,
                inset_center[1],
                0,
            ])
        )
        left_dark.set_z_index(3)

        right_dark = Rectangle(
            width=(inset_center[0] + inset_axis_length / 2) - x_40hz_inset,
            height=1.0,
            fill_color="#0F1116",
            fill_opacity=0.7,
            stroke_width=0,
        )
        right_dark.move_to(
            np.array([
                (x_40hz_inset + inset_center[0] + inset_axis_length / 2) / 2,
                inset_center[1],
                0,
            ])
        )
        right_dark.set_z_index(3)

        self.play(
            FadeIn(left_dark),
            FadeIn(right_dark),
            run_time=max(0.05, 0.8),
        )
        # pulse the green band
        self.play(band_fill.animate.set_opacity(0.5), run_time=max(0.05, 0.5))
        self.play(band_fill.animate.set_opacity(0.25), run_time=max(0.05, 0.5))
        self.play(band_fill.animate.set_opacity(0.4), run_time=max(0.05, 0.4))
        self.play(band_fill.animate.set_opacity(0.25), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 25.60 - 20.22 - 0.8 - 0.5 - 0.5 - 0.4 - 0.4))

        # Gap before beat 10: 25.60 → 26.98 = 1.38 s
        self.wait(max(0.05, 1.38))

        # ---------- Beat 10: 26.98–30.48 ----------
        bottom_glow = SurroundingRectangle(
            bottom_panel_bg,
            color=TEAL,
            stroke_width=3,
            buff=0.1,
            corner_radius=0.1,
        )
        bottom_glow.set_z_index(1)

        arrow_underline = Underline(
            arrow_label,
            color=GOLD,
            stroke_width=3,
            buff=0.05,
        )

        self.play(
            Create(bottom_glow),
            Create(arrow_underline),
            run_time=max(0.05, 1.0),
        )
        self.play(
            bottom_glow.animate.set_stroke(color=GOLD, width=4),
            run_time=max(0.05, 0.5),
        )
        self.play(
            bottom_glow.animate.set_stroke(color=TEAL, width=3),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 30.48 - 26.98 - 1.0 - 0.5 - 0.5))

        # Gap before beat 11: 30.48 → 31.24 = 0.76 s
        self.wait(max(0.05, 0.76))

        # ---------- Beat 11: 31.24–37.34 ----------
        def make_crosshatch(rect, n_lines=6):
            width = rect.get_width()
            height = rect.get_height()
            cx, cy, _ = rect.get_center()
            lines = VGroup()
            spacing = width / (n_lines + 1)
            for i in range(1, n_lines + 1):
                x = cx - width / 2 + i * spacing
                l1 = Line(
                    start=np.array([x - height / 4, cy - height / 2, 0]),
                    end=np.array([x + height / 4, cy + height / 2, 0]),
                    stroke_color=RED,
                    stroke_width=1,
                    stroke_opacity=0.4,
                )
                l2 = Line(
                    start=np.array([x + height / 4, cy - height / 2, 0]),
                    end=np.array([x - height / 4, cy + height / 2, 0]),
                    stroke_color=RED,
                    stroke_width=1,
                    stroke_opacity=0.4,
                )
                lines.add(l1, l2)
            lines.set_z_index(5)
            return lines

        left_crosshatch = make_crosshatch(left_dark, n_lines=4)
        right_crosshatch = make_crosshatch(right_dark, n_lines=4)

        removed_left = Text("removed", font_size=16, color=RED, weight="BOLD")
        removed_left.move_to(left_dark.get_center()).shift(UP * 0.3)
        removed_left.set_z_index(6)

        removed_right = Text("removed", font_size=16, color=RED, weight="BOLD")
        removed_right.move_to(right_dark.get_center()).shift(UP * 0.3)
        removed_right.set_z_index(6)

        self.play(
            FadeIn(left_crosshatch),
            FadeIn(right_crosshatch),
            Write(removed_left),
            Write(removed_right),
            run_time=max(0.05, 1.0),
        )
        self.play(
            band_fill.animate.set_opacity(0.4),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 37.34 - 31.24 - 1.0 - 0.5))

        # ---------- Beat 12: 37.34–38.15 ----------
        self.wait(max(0.05, 38.15 - 37.34))