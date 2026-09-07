ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


def generate_waveform(duration=10, sample_rate=1000, interference_freq=50):
    """Generate a synthetic composite signal: blue complex waveform + red sine hum"""
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    # blue complex waveform: sum of a few sinusoids at various frequencies
    blue = (
        0.6 * np.sin(2 * np.pi * 3 * t)
        + 0.4 * np.sin(2 * np.pi * 7 * t + 1.2)
        + 0.3 * np.sin(2 * np.pi * 12 * t + 0.5)
        + 0.15 * np.sin(2 * np.pi * 21 * t + 2.3)
    )
    # red interference hum at the specified frequency
    red = 0.4 * np.sin(2 * np.pi * interference_freq * t)
    composite = blue + red
    return t, blue, red, composite


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- generate waveform data ---
        t, blue, red, composite = generate_waveform(
            duration=10, sample_rate=500, interference_freq=50
        )

        # --- time axis ---
        axis_width = 12.0
        time_axis = Line(
            np.array([-axis_width / 2, -2.0, 0]),
            np.array([axis_width / 2, -2.0, 0]),
            color=GREY,
            stroke_width=4,
        )
        # tick marks and labels
        ticks = VGroup()
        for sec in range(0, 11):
            x = -axis_width / 2 + (sec / 10.0) * axis_width
            tick = Line(
                np.array([x, -2.0, 0]), np.array([x, -1.85, 0]),
                color=GREY,
                stroke_width=2,
            )
            ticks.add(tick)
            label = Text(f"{sec}s", font_size=20, color=GREY)
            label.move_to(np.array([x, -2.3, 0]))
            ticks.add(label)

        # --- create the scrolling waveform as a single polyline ---
        def signal_to_points(signal, y_scale=1.0, y_center=0.0):
            """Map time-series signal to screen coordinates within the axis width"""
            n_points = min(len(signal), 800)
            pts = []
            for i in range(n_points):
                x = -axis_width / 2 + (i / n_points) * axis_width
                y = y_center + signal[i] * y_scale
                pts.append(np.array([x, y, 0]))
            return pts

        # Initial composite signal (full red amplitude)
        composite_pts = signal_to_points(composite[:800], y_scale=1.5, y_center=0.5)
        composite_trace = VMobject(color=WHITE, stroke_width=3)
        composite_trace.set_points_as_corners(composite_pts)

        # Blue component alone (drawn on top to keep it visible)
        blue_pts = signal_to_points(blue[:800], y_scale=1.5, y_center=0.5)
        blue_trace = VMobject(color=BLUE, stroke_width=4)
        blue_trace.set_points_as_corners(blue_pts)

        # Red component alone (drawn on top so it's visible atop the mixture)
        red_pts = signal_to_points(red[:800], y_scale=1.5, y_center=0.5)
        red_trace = VMobject(color=RED, stroke_width=4)
        red_trace.set_points_as_corners(red_pts)

        # "Composite Signal" label
        label_composite = Text("Composite Signal", font_size=40, color=WHITE, weight="BOLD")
        label_composite.move_to(np.array([0, 2.5, 0]))

        # --- notch filter icon (stylized frequency response) ---
        def build_notch_icon():
            """Build a stylized notch filter frequency response: flat line with V-notch"""
            icon = VGroup()
            # left flat segment
            left = Line(
                np.array([-1.5, 0, 0]),
                np.array([-0.3, 0, 0]),
                color=WHITE,
                stroke_width=6,
            )
            # V-notch dip
            notch = Line(
                np.array([-0.3, 0, 0]),
                np.array([0.0, -0.9, 0]),
                color=WHITE,
                stroke_width=6,
            )
            # right flat segment
            notch_right = Line(
                np.array([0.0, -0.9, 0]),
                np.array([0.3, 0, 0]),
                color=WHITE,
                stroke_width=6,
            )
            right = Line(
                np.array([0.3, 0, 0]),
                np.array([1.5, 0, 0]),
                color=WHITE,
                stroke_width=6,
            )
            icon.add(left, notch, notch_right, right)
            # label below
            notch_label = Text("Notch", font_size=24, color=WHITE)
            notch_label.next_to(icon, DOWN, buff=0.3)
            icon.add(notch_label)
            return icon

        notch_icon = build_notch_icon()
        notch_icon.scale(0.8)
        notch_icon.move_to(np.array([0, 3.3, 0]))  # start off-screen at top

        # --- interference hum label ---
        interference_label = Text("Interference hum", font_size=32, color=RED, weight="BOLD")
        interference_label.next_to(red_trace, UP, buff=0.8)
        interference_label.shift(RIGHT * 1.5)

        # --- concluding text ---
        notch_text = Text(
            "Notch Filter — attenuates a narrow band centered on one specific frequency.",
            font_size=32,
            color=WHITE,
            weight="BOLD",
            t2c={"Notch Filter": YELLOW},
        )
        notch_text.scale_to_fit_width(12)
        notch_text.move_to(np.array([0, -3.3, 0]))

        # ========================
        # BEAT 1: 0.00 - 2.68
        # Screen fades in to time axis with scrolling composite waveform
        # ========================
        beat1_duration = 2.68

        self.play(
            FadeIn(time_axis),
            FadeIn(composite_trace),
            FadeIn(blue_trace),
            FadeIn(red_trace),
            FadeIn(label_composite),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, beat1_duration - 1.5))

        # ========================
        # BEAT 2: 2.68 - 9.96
        # Notch filter icon descends from top center to above the waveform
        # ========================
        beat2_duration = 9.96 - 2.68  # 7.28

        notch_target_y = 2.2
        notch_target = np.array([0, notch_target_y, 0])

        # Icon appears at top (off-screen-ish) then descends
        notch_icon.move_to(np.array([0, 4.5, 0]))
        self.play(FadeIn(notch_icon), run_time=max(0.05, 0.7))

        descend_duration = max(0.05, 3.0)  # arrive by ~4.84 → 4.84 - 2.68 = 2.16, round generously
        self.play(
            notch_icon.animate.move_to(notch_target),
            run_time=max(0.05, descend_duration),
        )
        # remaining wait until 9.96
        remaining = 9.96 - (2.68 + 0.7 + descend_duration)
        if remaining > 0:
            self.wait(max(0.05, remaining))

        # ========================
        # BEAT 3: 9.96 - 18.42
        # "Interference hum" label appears near the red sine wave
        # ========================
        beat3_duration = 18.42 - 9.96  # 8.46

        self.play(
            Write(interference_label),
            run_time=max(0.05, 2.0),
        )
        remaining = beat3_duration - 2.0
        if remaining > 0:
            self.wait(max(0.05, remaining))

        # ========================
        # BEAT 4: 18.42 - 25.70
        # Glow on notch icon; red sine wave shrinks to zero amplitude
        # ========================
        beat4_duration = 25.70 - 18.42  # 7.28

        # brief glow on notch icon
        glow_rect = SurroundingRectangle(
            notch_icon,
            color=YELLOW,
            buff=0.2,
            stroke_width=4,
            fill_opacity=0.2,
            fill_color=YELLOW,
        )
        self.play(FadeIn(glow_rect), run_time=max(0.05, 0.6))
        self.play(FadeOut(glow_rect), run_time=max(0.05, 0.6))
        glow_elapsed = 1.2

        # red trace fades out / shrinks — use a ValueTracker to modulate amplitude
        fade_duration = 22.38 - (18.42 + glow_elapsed)  # 22.38 is target zero point
        # Actually 22.38 - (18.42 + 1.2) = 2.76
        fade_duration = max(0.05, 2.76)

        def get_red_trace(alpha):
            """Rebuild red trace with amplitude scaled by alpha"""
            scaled = red[:800] * alpha
            pts = signal_to_points(scaled, y_scale=1.5, y_center=0.5)
            new_trace = VMobject(color=RED, stroke_width=4)
            new_trace.set_points_as_corners(pts)
            return new_trace

        # We'll use interpolation between current and zero
        self.play(
            Transform(red_trace, get_red_trace(0.0)),
            run_time=max(0.05, fade_duration),
        )
        # red_trace is now flat/zero
        red_trace.set_opacity(0)

        remaining = beat4_duration - glow_elapsed - fade_duration
        if remaining > 0:
            self.wait(max(0.05, remaining))

        # ========================
        # BEAT 5: 25.70 - 34.46
        # V-shaped notch brightens; clean blue trace scrolls
        # ========================
        beat5_duration = 34.46 - 25.70  # 8.76

        # Brighten the V-notch section of the icon
        # notch_icon[1] and notch_icon[2] are the two legs of the V
        v_notch_left = notch_icon[1]
        v_notch_right = notch_icon[2]

        # briefly brighten them
        self.play(
            v_notch_left.animate.set_color(YELLOW).set_stroke(width=10),
            v_notch_right.animate.set_color(YELLOW).set_stroke(width=10),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 1.5))
        self.play(
            v_notch_left.animate.set_color(WHITE).set_stroke(width=6),
            v_notch_right.animate.set_color(WHITE).set_stroke(width=6),
            run_time=max(0.05, 1.0),
        )
        highlight_elapsed = 1.0 + 1.5 + 1.0  # 3.5
        remaining = beat5_duration - highlight_elapsed
        if remaining > 0:
            self.wait(max(0.05, remaining))

        # ========================
        # BEAT 6: 34.46 - 39.30
        # Notch filter text fades in below waveform
        # ========================
        beat6_duration = 39.30 - 34.46  # 4.84

        self.play(
            FadeOut(interference_label),
            FadeIn(notch_text),
            run_time=max(0.05, 2.0),
        )
        remaining = beat6_duration - 2.0
        if remaining > 0:
            self.wait(max(0.05, remaining))

        # ========================
        # BEAT 7: 39.30 (scene fades out)
        # ========================
        # the target duration is 39.30, so this is the end — all visuals disappear
        self.play(
            FadeOut(time_axis, ticks, composite_trace, blue_trace, red_trace,
                    label_composite, notch_icon, notch_text),
            run_time=max(0.05, 0.8),
        )