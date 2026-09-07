ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 1. MODULE 1 flies in from upper right and settles with overshoot
        title = Text("MODULE 1", font_size=72, weight=BOLD, color=WHITE)
        final_title_pos = np.array([0, 3.3, 0])
        overshoot_pos = final_title_pos + np.array([0.35, 0, 0])
        title.move_to(final_title_pos + np.array([9, 0, 0]))
        self.add(title)
        self.play(
            title.animate.move_to(overshoot_pos),
            run_time=max(0.05, 0.60),
            rate_func=rate_functions.ease_out_cubic,
        )
        self.play(
            title.animate.move_to(final_title_pos),
            run_time=max(0.05, 0.20),
            rate_func=rate_functions.ease_out_cubic,
        )
        self.wait(max(0.05, 0.06))
        self.wait(max(0.05, 0.90))

        # 2. Subtitle writes letter by letter
        subtitle = Text("Understanding Neural Signals", font_size=40, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(AddTextLetterByLetter(subtitle), run_time=max(0.05, 1.12))
        self.wait(max(0.05, 0.72))

        # 3. Resting membrane potential baseline
        baseline_y = -1.6
        resting_line = Line(
            np.array([-5.5, baseline_y, 0]),
            np.array([5.5, baseline_y, 0]),
            color=GREEN,
            stroke_width=5,
        )
        rest_label = Text("Resting membrane potential", font_size=30, color=GREY)
        rest_label.next_to(resting_line, DOWN, buff=0.3).shift(LEFT * 2.8)
        self.play(Create(resting_line), run_time=max(0.05, 1.4))
        self.play(FadeIn(rest_label), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.33))
        self.wait(max(0.05, 0.34))

        # 4. Action potential trace draws itself left to right
        ap_points = [
            np.array([-5.5, baseline_y, 0]),
            np.array([-2.0, baseline_y, 0]),
            np.array([-1.2, baseline_y, 0]),
            np.array([-0.5, 1.6, 0]),
            np.array([-0.2, 1.9, 0]),
            np.array([0.0, 1.0, 0]),
            np.array([0.1, -2.6, 0]),
            np.array([0.5, -2.2, 0]),
            np.array([0.9, baseline_y, 0]),
            np.array([5.5, baseline_y, 0]),
        ]
        ap_trace = VMobject(stroke_color=GREEN, stroke_width=5)
        ap_trace.set_points_as_corners(ap_points)
        self.play(Create(ap_trace), run_time=max(0.05, 3.28))
        self.wait(max(0.05, 0.66))

        # 5. Shrink and duplicate into three differently scaled copies
        small_copy = (
            ap_trace.copy()
            .scale_to_fit_width(2.0)
            .move_to(np.array([-5.2, -0.8, 0]))
        )
        medium_copy = (
            ap_trace.copy()
            .scale_to_fit_width(2.8)
            .move_to(np.array([-0.3, -0.8, 0]))
        )
        large_copy = (
            ap_trace.copy()
            .scale_to_fit_width(3.8)
            .move_to(np.array([4.4, -0.8, 0]))
        )
        copies_group = VGroup(small_copy, medium_copy, large_copy)

        self.play(
            FadeOut(resting_line),
            FadeOut(rest_label),
            run_time=max(0.05, 0.25),
        )
        self.play(
            ReplacementTransform(ap_trace, medium_copy),
            GrowFromCenter(small_copy),
            GrowFromCenter(large_copy),
            run_time=max(0.05, 0.75),
        )
        scale_label = Text("same signal, different scales", font_size=32, color=YELLOW)
        scale_label.next_to(copies_group, DOWN, buff=0.4)
        self.play(Write(scale_label), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.88))

        # 6. Three different waveform shapes appear side by side
        def make_smooth_wave():
            pts = [
                np.array([x, 0.35 * np.sin(2 * np.pi * x / 1.3), 0])
                for x in np.linspace(-1.5, 1.5, 90)
            ]
            wave = VMobject(stroke_color=TEAL, stroke_width=5)
            wave.set_points_as_corners(pts)
            return wave

        def make_irregular_wave():
            pts = [
                np.array([-1.5, 0, 0]),
                np.array([-1.25, 0.35, 0]),
                np.array([-1.0, 0.1, 0]),
                np.array([-0.75, 0.55, 0]),
                np.array([-0.5, -0.05, 0]),
                np.array([-0.25, 0.4, 0]),
                np.array([0.0, -0.2, 0]),
                np.array([0.25, 0.5, 0]),
                np.array([0.5, -0.35, 0]),
                np.array([0.75, 0.25, 0]),
                np.array([1.0, -0.4, 0]),
                np.array([1.25, 0.15, 0]),
                np.array([1.5, 0, 0]),
            ]
            wave = VMobject(stroke_color=ORANGE, stroke_width=5)
            wave.set_points_as_corners(pts)
            return wave

        def make_spiky_burst():
            pts = [np.array([-1.5, 0, 0])]
            x = -1.5
            while x < 1.4:
                pts.append(np.array([x + 0.03, 0, 0]))
                pts.append(np.array([x + 0.06, 0.8, 0]))
                pts.append(np.array([x + 0.08, 0, 0]))
                pts.append(np.array([x + 0.10, 0.9, 0]))
                pts.append(np.array([x + 0.12, 0, 0]))
                pts.append(np.array([x + 0.14, -0.7, 0]))
                pts.append(np.array([x + 0.16, 0, 0]))
                x += 0.22
            pts.append(np.array([1.5, 0, 0]))
            wave = VMobject(stroke_color=PURPLE, stroke_width=5)
            wave.set_points_as_corners(pts)
            return wave

        smooth_wave = make_smooth_wave()
        irr_wave = make_irregular_wave()
        spike_wave = make_spiky_burst()

        waves = VGroup(smooth_wave, irr_wave, spike_wave).arrange(RIGHT, buff=0.7)
        waves.move_to(np.array([0, -2.6, 0]))

        smooth_label = Text("smooth wave", font_size=24, color=TEAL).next_to(
            smooth_wave, DOWN, buff=0.15
        )
        irr_label = Text("irregular wave", font_size=24, color=ORANGE).next_to(
            irr_wave, DOWN, buff=0.15
        )
        spike_label = Text("spiky burst", font_size=24, color=PURPLE).next_to(
            spike_wave, DOWN, buff=0.15
        )
        wave_group = VGroup(waves, smooth_label, irr_label, spike_label)

        self.play(
            FadeOut(scale_label),
            FadeIn(wave_group),
            run_time=max(0.05, 0.86),
        )
        self.wait(max(0.05, 0.80))

        # 7. Clear everything and burst in the closing phrase
        everything = VGroup(
            title,
            subtitle,
            small_copy,
            medium_copy,
            large_copy,
            wave_group,
        )
        self.play(FadeOut(everything), run_time=max(0.05, 0.40))

        phrase = Text("Let's get started!", font_size=80, weight=BOLD, color=YELLOW)
        phrase.move_to(ORIGIN)
        self.play(
            GrowFromCenter(phrase),
            Flash(ORIGIN, color=YELLOW, flash_radius=2.5, num_lines=18),
            run_time=max(0.05, 0.60),
        )
        self.wait(max(0.05, 0.47))