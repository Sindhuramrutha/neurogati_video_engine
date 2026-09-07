ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Coordinate system ----
        AXIS_LEFT_X = -4.5
        AXIS_RIGHT_X = 4.5
        AXIS_Y = -1.5
        GAIN_HEIGHT = 4.0
        GAIN_TOP = AXIS_Y + GAIN_HEIGHT  # 2.5

        def freq_to_point(t, gain):
            x = AXIS_LEFT_X + t * (AXIS_RIGHT_X - AXIS_LEFT_X)
            y = AXIS_Y + gain * GAIN_HEIGHT
            return np.array([x, y, 0.0])

        def make_curve(gain_func, color):
            pts = [freq_to_point(t, gain_func(t)) for t in np.linspace(0, 1, 300)]
            curve = VMobject()
            curve.set_points_as_corners(pts)
            curve.set_stroke(color=color, width=6)
            curve.set_fill(opacity=0)
            curve.set_z_index(2)
            return curve

        def sigmoid(z):
            return 1.0 / (1.0 + np.exp(-z))

        def lp_gain(t):
            return sigmoid(-(t - 0.55) * 16)

        def hp_gain(t):
            return sigmoid((t - 0.45) * 16)

        def bp_gain(t):
            return sigmoid((t - 0.32) * 20) * sigmoid(-(t - 0.68) * 20)

        # ---- Beat 1: frequency axis and labels ----
        h_axis = Line(
            np.array([AXIS_LEFT_X, AXIS_Y, 0]),
            np.array([AXIS_RIGHT_X, AXIS_Y, 0]),
            color=WHITE,
            stroke_width=5,
        )
        v_axis = Line(
            np.array([AXIS_LEFT_X, AXIS_Y, 0]),
            np.array([AXIS_LEFT_X, GAIN_TOP, 0]),
            color=WHITE,
            stroke_width=4,
        )

        freq_label = Text("Frequency", font_size=34, color=WHITE)
        freq_label.next_to(h_axis, DOWN, buff=0.35)

        low_label = Text("Low", font_size=28, color=GREY_B)
        low_label.next_to(h_axis, DOWN, buff=0.35, aligned_edge=LEFT)

        high_label = Text("High", font_size=28, color=GREY_B)
        high_label.next_to(h_axis, DOWN, buff=0.35, aligned_edge=RIGHT)

        gain_label = Text("Gain", font_size=30, color=GREY_B)
        gain_label.rotate(PI / 2)
        gain_label.next_to(v_axis, LEFT, buff=0.25)

        self.play(
            Create(h_axis),
            Create(v_axis),
            Write(freq_label),
            FadeIn(low_label, high_label, gain_label),
            run_time=max(0.05, 1.56),
        )

        # ---- Beat 2: low-pass filter curve ----
        lp_curve = make_curve(lp_gain, BLUE)
        lp_label = Text("Low-pass", font_size=36, color=BLUE)
        lp_label.move_to(np.array([-2.0, 3.0, 0]))

        self.play(Create(lp_curve), Write(lp_label), run_time=max(0.05, 3.06))

        # ---- Beat 3: high-pass filter curve ----
        hp_curve = make_curve(hp_gain, GREEN)
        hp_label = Text("High-pass", font_size=36, color=GREEN)
        hp_label.move_to(np.array([2.0, 3.0, 0]))

        self.play(Create(hp_curve), Write(hp_label), run_time=max(0.05, 1.26))

        # ---- Beat 4: highlight low-pass curve ----
        lp_atten = Rectangle(
            width=3.0,
            height=GAIN_HEIGHT,
            fill_color=RED,
            fill_opacity=0.25,
            stroke_width=0,
        )
        lp_atten.move_to(np.array([2.9, (AXIS_Y + GAIN_TOP) / 2, 0]))
        lp_atten.set_z_index(-1)

        self.play(
            FadeIn(lp_atten),
            lp_curve.animate.set_stroke(color=YELLOW, width=12),
            run_time=max(0.05, 1.2),
        )
        self.play(lp_curve.animate.set_stroke(color=BLUE, width=6), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.6))

        # ---- Beat 5: highlight high-pass curve ----
        hp_atten = Rectangle(
            width=3.0,
            height=GAIN_HEIGHT,
            fill_color=RED,
            fill_opacity=0.25,
            stroke_width=0,
        )
        hp_atten.move_to(np.array([-2.9, (AXIS_Y + GAIN_TOP) / 2, 0]))
        hp_atten.set_z_index(-1)

        self.play(FadeOut(lp_atten), run_time=max(0.05, 0.4))
        self.play(
            FadeIn(hp_atten),
            hp_curve.animate.set_stroke(color=YELLOW, width=12),
            run_time=max(0.05, 1.2),
        )
        self.play(hp_curve.animate.set_stroke(color=GREEN, width=6), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.62))

        # ---- Beat 6: fade out low/high, fade in band-pass ----
        bp_curve = make_curve(bp_gain, PURPLE)
        bp_label = Text("Band-pass", font_size=40, color=PURPLE)
        bp_label.move_to(np.array([0.0, 3.1, 0]))
        bp_label.set_opacity(0.55)

        self.play(
            FadeOut(lp_curve, hp_curve, lp_label, hp_label, lp_atten, hp_atten),
            FadeIn(bp_curve, bp_label),
            run_time=max(0.05, 3.0),
        )
        self.wait(max(0.05, 1.3))

        # ---- Beat 7: highlight central passband region ----
        passband_rect = Rectangle(
            width=3.2,
            height=GAIN_HEIGHT,
            fill_color=GREEN,
            fill_opacity=0.2,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        passband_rect.move_to(np.array([0.0, (AXIS_Y + GAIN_TOP) / 2, 0]))
        passband_rect.set_z_index(-1)

        self.play(FadeIn(passband_rect), run_time=max(0.05, 1.2))
        self.play(
            passband_rect.animate.set_stroke(color=YELLOW, width=3.5),
            run_time=max(0.05, 0.8),
        )
        self.play(
            passband_rect.animate.set_fill(GREEN, opacity=0.22),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.44))

        # ---- Beat 8: intensify passband, pulse attenuated ends ----
        bp_atten_left = Rectangle(
            width=2.8,
            height=GAIN_HEIGHT,
            fill_color=RED,
            fill_opacity=0.12,
            stroke_width=0,
        )
        bp_atten_left.move_to(np.array([-3.1, (AXIS_Y + GAIN_TOP) / 2, 0]))
        bp_atten_left.set_z_index(-1)

        bp_atten_right = Rectangle(
            width=2.8,
            height=GAIN_HEIGHT,
            fill_color=RED,
            fill_opacity=0.12,
            stroke_width=0,
        )
        bp_atten_right.move_to(np.array([3.1, (AXIS_Y + GAIN_TOP) / 2, 0]))
        bp_atten_right.set_z_index(-1)

        self.play(
            passband_rect.animate.set_fill(GREEN, opacity=0.5),
            run_time=max(0.05, 1.1),
        )
        self.play(
            passband_rect.animate.set_stroke(color=YELLOW, width=6),
            run_time=max(0.05, 1.0),
        )
        self.play(FadeIn(bp_atten_left, bp_atten_right), run_time=max(0.05, 1.2))

        self.play(
            bp_atten_left.animate.set_fill(RED, opacity=0.45),
            run_time=max(0.05, 0.8),
        )
        self.play(
            bp_atten_left.animate.set_fill(RED, opacity=0.12),
            run_time=max(0.05, 0.6),
        )
        self.play(
            bp_atten_right.animate.set_fill(RED, opacity=0.45),
            run_time=max(0.05, 0.8),
        )
        self.play(
            bp_atten_right.animate.set_fill(RED, opacity=0.12),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 2.02))

        # ---- Beat 9: band-pass label becomes prominent ----
        self.play(
            bp_label.animate.set_opacity(1).set_color(YELLOW),
            run_time=max(0.05, 0.8),
        )
        self.play(bp_label.animate.scale(1.15), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.82))

        # ---- Beat 10: brain signal icon ----
        brain = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=PURPLE,
            fill_opacity=0.25,
            stroke_color=PURPLE,
            stroke_width=2,
        ).scale_to_fit_height(1.3)

        wave_pts = [
            np.array([x, 0.35 * np.sin(2 * PI * 2 * x / 1.6), 0])
            for x in np.linspace(-0.7, 0.7, 100)
        ]
        wave = VMobject()
        wave.set_points_as_corners(wave_pts)
        wave.set_stroke(color=PINK, width=4)
        wave.set_fill(opacity=0)

        brain_signal = VGroup(brain, wave)
        brain_signal.scale_to_fit_height(1.4)
        brain_signal.move_to(np.array([5.5, 0.5, 0]))
        brain_signal.set_z_index(3)

        self.play(FadeIn(brain_signal, scale=0.8), run_time=max(0.05, 1.2))
        self.play(brain_signal.animate.scale(1.06), run_time=max(0.05, 0.8))
        self.play(brain_signal.animate.scale(1 / 1.06), run_time=max(0.05, 0.8))
        self.play(brain_signal.animate.scale(1.06), run_time=max(0.05, 0.8))
        self.play(brain_signal.animate.scale(1 / 1.06), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.08))

        # ---- Beat 11: subtitle ----
        subtitle = Text("Neural Signal Processing", font_size=38, color=WHITE)
        subtitle.next_to(h_axis, DOWN, buff=1.65).shift(RIGHT * 0.5)

        self.play(FadeIn(subtitle, shift=DOWN * 0.3), run_time=max(0.05, 1.2))
        self.play(brain_signal.animate.scale(1.04), run_time=max(0.05, 0.8))
        self.play(brain_signal.animate.scale(1 / 1.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 2.76))

        # ---- Beat 12: final hold ----
        self.wait(max(0.05, 1.05))