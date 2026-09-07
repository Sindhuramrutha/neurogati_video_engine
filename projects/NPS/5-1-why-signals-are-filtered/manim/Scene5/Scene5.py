ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- tiny helper ----------
        def make_wave(func, t_range, color, stroke_width=3, stroke_opacity=1):
            return ParametricFunction(
                lambda t: np.array([t, func(t), 0]),
                t_range=t_range,
                color=color,
                stroke_width=stroke_width,
                stroke_opacity=stroke_opacity,
            )

        def make_aggressive_icon():
            base_wave = make_wave(
                lambda x: 0.28 * np.sin(4 * x) + 0.10 * np.sin(7 * x),
                [-0.7, 0.7, 0.01],
                GREY_B,
                stroke_width=2.5,
                stroke_opacity=0.35,
            )
            flat_line = Line(LEFT * 0.65, RIGHT * 0.65, color=GREY_B, stroke_width=6)
            red_x = VGroup(
                Line(LEFT * 0.35 + UP * 0.35, RIGHT * 0.35 + DOWN * 0.35, color=RED, stroke_width=7),
                Line(LEFT * 0.35 + DOWN * 0.35, RIGHT * 0.35 + UP * 0.35, color=RED, stroke_width=7),
            )
            icon = VGroup(base_wave, flat_line, red_x).scale_to_fit_width(1.0)
            icon.set_opacity(0)
            return icon

        def make_weak_icon():
            signal_wave = make_wave(
                lambda x: 0.22 * np.sin(3.2 * x) + 0.08 * np.sin(6.0 * x),
                [-0.7, 0.7, 0.01],
                TEAL,
                stroke_width=3,
            )
            noise_wave = make_wave(
                lambda x: 0.14 * np.sign(np.sin(24 * x)),
                [-0.7, 0.7, 0.005],
                RED,
                stroke_width=2,
            )
            dashed_filter = DashedLine(
                LEFT * 0.6,
                RIGHT * 0.6,
                color=GREY,
                stroke_width=2,
                dash_length=0.08,
                stroke_opacity=0.55,
            )
            icon = VGroup(signal_wave, noise_wave, dashed_filter).scale_to_fit_width(1.0)
            icon.set_opacity(0)
            return icon

        def make_moderate_icon():
            clean_wave = make_wave(
                lambda x: 0.22 * np.sin(3.4 * x) + 0.06 * np.sin(6.8 * x),
                [-0.7, 0.7, 0.01],
                BLUE,
                stroke_width=4,
            )
            icon = VGroup(clean_wave).scale_to_fit_width(1.0)
            icon.set_opacity(0)
            return icon

        # ---------- previous scene visual ----------
        prev_divider = Line(UP * 2.3, DOWN * 2.1, color=GREY_B, stroke_width=3)
        prev_signal_title = Text("Signal", font_size=32, color=GREEN, weight="BOLD")
        prev_signal_title.move_to(LEFT * 3.3 + UP * 1.5)
        prev_noise_title = Text("Noise", font_size=32, color=RED, weight="BOLD")
        prev_noise_title.move_to(RIGHT * 3.3 + UP * 1.5)
        prev_signal_wave = make_wave(
            lambda x: 0.25 * np.sin(3 * x) + 0.10 * np.sin(7 * x),
            [-0.9, 0.9, 0.01],
            GREEN,
            stroke_width=3,
        ).scale_to_fit_width(1.8)
        prev_signal_wave.move_to(LEFT * 3.3 + DOWN * 0.2)
        prev_noise_wave = make_wave(
            lambda x: 0.18 * np.sign(np.sin(15 * x)) + 0.06 * np.sin(40 * x),
            [-0.9, 0.9, 0.005],
            RED,
            stroke_width=3,
        ).scale_to_fit_width(1.8)
        prev_noise_wave.move_to(RIGHT * 3.3 + DOWN * 0.2)
        prev_layout = VGroup(
            prev_divider,
            prev_signal_title,
            prev_noise_title,
            prev_signal_wave,
            prev_noise_wave,
        )
        self.add(prev_layout)

        # ---------- balance scale geometry ----------
        PIVOT = np.array([0.0, 1.6, 0.0])
        LEFT_END = np.array([-4.5, 0.0, 0.0])
        RIGHT_END = np.array([4.5, 0.0, 0.0])

        # static support
        stand_line = Line(PIVOT, np.array([0, -2.3, 0]), color=GREY_B, stroke_width=8)
        base_line = Line(np.array([-0.45, -2.35, 0]), np.array([0.45, -2.35, 0]), color=GREY_B, stroke_width=12)
        pivot_dot = Dot(PIVOT, radius=0.09, color=GREY_B, fill_opacity=1)
        static_scale = VGroup(stand_line, base_line, pivot_dot)

        # moving beam + empty pans
        beam_line = Line(LEFT_END, RIGHT_END, color=GREY_B, stroke_width=12)

        left_string_l = Line(np.array([-4.5, 0, 0]), np.array([-5.0, -0.8, 0]), color=GREY_B, stroke_width=3)
        left_string_r = Line(np.array([-4.5, 0, 0]), np.array([-4.0, -0.8, 0]), color=GREY_B, stroke_width=3)
        left_bowl = Arc(
            radius=0.5,
            start_angle=PI,
            angle=PI,
            arc_center=np.array([-4.5, -0.8, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        left_pan = VGroup(left_string_l, left_string_r, left_bowl)

        right_string_l = Line(np.array([4.5, 0, 0]), np.array([5.0, -0.8, 0]), color=GREY_B, stroke_width=3)
        right_string_r = Line(np.array([4.5, 0, 0]), np.array([4.0, -0.8, 0]), color=GREY_B, stroke_width=3)
        right_bowl = Arc(
            radius=0.5,
            start_angle=0,
            angle=PI,
            arc_center=np.array([4.5, -0.8, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        right_pan = VGroup(right_string_l, right_string_r, right_bowl)

        beam_group = VGroup(beam_line, left_pan, right_pan)

        # ---------- pan-attached icons and labels ----------
        aggressive_icon = make_aggressive_icon()
        aggressive_icon.move_to(np.array([-4.5, -0.25, 0]))
        too_aggressive_label = Text("Too aggressive", font_size=22, color=RED).set_opacity(0)
        too_aggressive_label.move_to(np.array([-4.5, -1.55, 0]))
        removes_signal_label = Text("Removes signal too", font_size=22, color=RED).set_opacity(0)
        removes_signal_label.move_to(np.array([-4.5, -2.0, 0]))

        weak_icon = make_weak_icon()
        weak_icon.move_to(np.array([4.5, -0.25, 0]))
        too_weak_label = Text("Too weak", font_size=22, color=ORANGE).set_opacity(0)
        too_weak_label.move_to(np.array([4.5, -1.55, 0]))
        interference_remains_label = Text("Interference remains", font_size=22, color=ORANGE).set_opacity(0)
        interference_remains_label.move_to(np.array([4.5, -2.0, 0]))

        moderate_left_icon = make_moderate_icon()
        moderate_left_icon.move_to(np.array([-4.5, -0.25, 0]))
        moderate_right_icon = make_moderate_icon()
        moderate_right_icon.move_to(np.array([4.5, -0.25, 0]))

        beam_group.add(
            aggressive_icon,
            too_aggressive_label,
            removes_signal_label,
            weak_icon,
            too_weak_label,
            interference_remains_label,
            moderate_left_icon,
            moderate_right_icon,
        )
        beam_group.shift(PIVOT)

        # ---------- balanced label and caption ----------
        appropriate_label = Text("Appropriate filter", font_size=44, color=BLUE, weight="BOLD")
        appropriate_label.move_to(PIVOT + UP * 1.5)

        bottom_caption = Text(
            "Different applications → different filtering strategies.",
            font_size=30,
            color=WHITE,
            t2c={"different filtering strategies": BLUE},
        ).scale_to_fit_width(11)
        bottom_caption.move_to(DOWN * 3.0)

        # ---------- exact beat durations ----------
        beat1_dur = 2.12
        gap1_dur = 1.00
        beat2_dur = 1.24
        beat3_dur = 4.46
        gap2_dur = 0.82
        beat4_dur = 2.28
        beat5_dur = 2.12
        gap3_dur = 1.06
        beat6_dur = 3.36
        beat7_dur = 4.88
        beat8_dur = 5.32
        beat9_dur = 1.39

        # ---------- beat 1: transition to scale ----------
        self.play(
            FadeOut(prev_layout),
            Create(static_scale),
            Create(beam_group),
            run_time=max(0.05, beat1_dur),
        )
        self.wait(max(0.05, gap1_dur))

        # ---------- beat 2: aggressive filter sinks left pan ----------
        self.play(
            beam_group.animate.rotate(-0.24, about_point=PIVOT),
            aggressive_icon.animate.set_opacity(1),
            too_aggressive_label.animate.set_opacity(1),
            run_time=max(0.05, beat2_dur),
        )

        # ---------- beat 3: loss of signal is called out ----------
        self.play(FadeIn(removes_signal_label), run_time=max(0.05, 1.5))
        self.play(Wiggle(aggressive_icon, scale_value=0.04), run_time=max(0.05, 1.0))
        self.wait(max(0.05, beat3_dur - 2.5))

        self.wait(max(0.05, gap2_dur))

        # ---------- beat 4: weak filter sinks right pan ----------
        self.play(
            beam_group.animate.rotate(0.48, about_point=PIVOT),
            weak_icon.animate.set_opacity(1),
            too_weak_label.animate.set_opacity(1),
            run_time=max(0.05, beat4_dur),
        )

        # ---------- beat 5: interference remains ----------
        self.play(FadeIn(interference_remains_label), run_time=max(0.05, 1.0))
        self.play(Wiggle(weak_icon, scale_value=0.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, beat5_dur - 1.8))

        self.wait(max(0.05, gap3_dur))

        # ---------- beat 6: settle toward horizontal, fade extreme labels ----------
        self.play(
            beam_group.animate.rotate(-0.24, about_point=PIVOT),
            FadeOut(too_aggressive_label),
            FadeOut(removes_signal_label),
            FadeOut(too_weak_label),
            FadeOut(interference_remains_label),
            run_time=max(0.05, beat6_dur),
        )

        # ---------- beat 7: balanced scale, moderate symbols, appropriate filter label ----------
        self.play(
            FadeOut(aggressive_icon),
            FadeOut(weak_icon),
            moderate_left_icon.animate.set_opacity(1),
            moderate_right_icon.animate.set_opacity(1),
            run_time=max(0.05, 2.0),
        )
        self.play(FadeIn(appropriate_label), run_time=max(0.05, 1.6))
        self.wait(max(0.05, beat7_dur - 3.6))

        # ---------- beat 8: bottom caption ----------
        self.play(FadeIn(bottom_caption), run_time=max(0.05, 2.2))
        self.wait(max(0.05, beat8_dur - 2.2))

        # ---------- beat 9: final hold ----------
        self.wait(max(0.05, beat9_dur))