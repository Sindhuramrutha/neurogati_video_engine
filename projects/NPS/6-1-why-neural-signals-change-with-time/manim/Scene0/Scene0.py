ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


def make_wave(components, x_min=-6.0, x_max=6.0, n_points=800, color=TEAL, stroke_width=3.0):
    pts = []
    for i in range(n_points):
        x = x_min + (x_max - x_min) * i / (n_points - 1)
        y = 0.0
        for cycles, amp, phase in components:
            y += amp * np.sin(2 * np.pi * cycles * (x - x_min) / (x_max - x_min) + phase)
        pts.append([x, y, 0])
    obj = VMobject(stroke_color=color, stroke_width=stroke_width)
    obj.set_points_smoothly(np.array(pts))
    return obj


def make_noise_layer(components, jitter=0.15, offset=0.2, color=GREY_B, n_points=500, seed=0):
    np.random.seed(seed)
    pts = []
    for i in range(n_points):
        x = -6.0 + 12.0 * i / (n_points - 1)
        base_y = 0.0
        for cycles, amp, phase in components:
            base_y += amp * np.sin(2 * np.pi * cycles * (x + 6.0) / 12.0 + phase)
        y = base_y + offset + np.random.uniform(-jitter, jitter)
        pts.append([x, y, 0])
    obj = VMobject(stroke_color=color, stroke_width=1.2)
    obj.set_points_smoothly(np.array(pts))
    obj.set_stroke(opacity=0.55)
    return obj


def make_marker(label, x, color, timeline_y=-2.2):
    tick = Line(UP * 0.12, DOWN * 0.12, color=color, stroke_width=4)
    text = Text(label, font_size=24, color=color)
    group = VGroup(tick, text).arrange(DOWN, buff=0.12)
    group.move_to(np.array([x, timeline_y, 0]))
    return group


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Stable waveform and axis
        stable_components = [(3.5, 0.55, 0.0), (7.0, 0.12, 0.5)]
        wave = make_wave(stable_components, color=TEAL)
        axis = Line(LEFT * 6, RIGHT * 6, color=GREY_B, stroke_width=2)
        neural_label = Text("neural recording", font_size=28, color=WHITE)
        neural_label.move_to(np.array([-4.3, -0.8, 0]))

        # Noise layers around the early waveform, faded out in beat 3
        noise1 = make_noise_layer(stable_components, offset=0.25, jitter=0.15, seed=101)
        noise2 = make_noise_layer(stable_components, offset=-0.20, jitter=0.18, seed=102)
        noise3 = make_noise_layer(stable_components, offset=0.45, jitter=0.12, seed=103)

        # Timeline and markers below the waveform
        timeline_line = Line(LEFT * 6, RIGHT * 6, color=GREY_B, stroke_width=2)
        timeline_line.move_to(np.array([0, -2.2, 0]))
        rest_marker = make_marker("Rest", -5.0, BLUE)
        movement_marker = make_marker("Movement", -2.5, ORANGE)
        stimulus_marker = make_marker("Stimulus", 0.0, RED)
        sleep_marker = make_marker("Sleep", 2.5, PURPLE)
        cogn_marker = make_marker("Cognition", 5.0, GREEN)
        marker_group = VGroup(rest_marker, movement_marker, stimulus_marker, sleep_marker, cogn_marker)

        # Question, question mark, No stamp
        question_text = Text("Constant throughout?", font_size=40, color=YELLOW, weight="BOLD")
        question_text.move_to(np.array([0.8, 2.3, 0]))
        qmark = Text("?", font_size=80, color=RED, weight="BOLD")
        qmark.next_to(question_text, RIGHT, buff=0.25)

        no_text = Text("No.", font_size=48, color=RED, weight="BOLD")
        no_box = SurroundingRectangle(no_text, color=RED, stroke_width=3, buff=0.1).rotate(0.05)
        no_stamp = VGroup(no_text, no_box)
        no_stamp.next_to(qmark, DOWN, buff=0.2)

        # Title, revealed when the earlier question is replaced
        title_text = Text("Nonstationary Signals", font_size=56, color=YELLOW, weight="BOLD")
        title_text.scale_to_fit_width(10)
        title_text.move_to(question_text)

        # Inset frequency panel and axes
        panel = Rectangle(width=3.0, height=2.2, color=GREY_B, fill_color="#1A1D24", fill_opacity=0.9, stroke_width=1.5)
        panel.move_to(np.array([4.8, 1.8, 0]))
        axes = Axes(
            x_range=[0, 60, 20],
            y_range=[0, 1, 0.5],
            x_length=2.2,
            y_length=1.3,
            axis_config={"color": GREY_B, "stroke_width": 1.5, "include_tip": False},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        )
        axes.move_to(np.array([4.8, 1.8, 0]))
        x_label = Text("Frequency (Hz)", font_size=16, color=GREY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.12)
        y_label = Text("Power", font_size=16, color=GREY).rotate(PI / 2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.12)

        # Different waveform targets for the behavioural-state shifts
        wave_complex1 = make_wave([(4.5, 0.55, 0.3), (9.0, 0.20, 1.0)], color=TEAL)
        wave_complex2 = make_wave([(5.5, 0.50, 0.8), (11.0, 0.25, 0.2), (2.0, 0.30, 0.5)], color=TEAL)
        wave_rest = make_wave([(1.2, 0.70, 0.0)], color=TEAL)
        wave_movement = make_wave([(7.0, 0.80, 0.2), (14.0, 0.15, 0.5)], color=TEAL)
        wave_stimulus = make_wave([(12.0, 0.70, 0.0), (20.0, 0.30, 0.7), (5.0, 0.40, 0.0)], color=TEAL)
        wave_moderate = make_wave([(4.0, 0.60, 0.0)], color=TEAL)
        wave_sleep = make_wave([(0.6, 1.10, 0.0), (1.2, 0.30, 0.5)], color=TEAL)
        wave_cog = make_wave([(9.0, 0.40, 0.3), (15.0, 0.35, 1.1), (3.0, 0.50, 0.7), (18.0, 0.20, 0.1)], color=TEAL)

        wave_var1 = make_wave([(6.0, 0.50, 0.1), (10.0, 0.30, 0.9), (2.5, 0.40, 0.3)], color=TEAL)
        wave_var2 = make_wave([(8.0, 0.45, 1.2), (13.0, 0.25, 0.4), (4.0, 0.30, 0.8), (20.0, 0.15, 0.2)], color=TEAL)
        wave_var3 = make_wave([(5.0, 0.65, 0.5), (11.0, 0.30, 0.0), (7.0, 0.20, 0.7)], color=TEAL)
        wave_var4 = make_wave([(9.0, 0.50, 0.9), (14.0, 0.20, 0.3), (3.5, 0.45, 1.0), (17.0, 0.25, 0.0)], color=TEAL)
        wave_final = make_wave([(10.0, 0.55, 0.2), (16.0, 0.30, 0.8), (4.0, 0.30, 1.0), (22.0, 0.20, 0.4)], color=TEAL)
        wave_final.shift(RIGHT * 0.2)

        # Beat 1: axis appears, waveform draws left to right
        self.play(FadeIn(axis), run_time=max(0.05, 0.3))
        self.play(Create(wave), run_time=max(0.05, 0.7))
        self.add(noise1, noise2, noise3)
        self.wait(max(0.05, 0.1))

        # Beat 2: ripple pulse, then neural recording label
        self.wait(max(0.05, 0.96))
        pulse = Rectangle(width=0.08, height=2.2, fill_color=YELLOW, fill_opacity=0.4, stroke_width=0)
        pulse.move_to(np.array([-6, 0, 0]))
        self.play(FadeIn(pulse), run_time=max(0.05, 0.1))
        self.play(pulse.animate.move_to(np.array([6, 0, 0])), run_time=max(0.05, 1.0))
        self.play(FadeOut(pulse), run_time=max(0.05, 0.1))
        self.wait(max(0.05, 0.30))
        self.play(FadeIn(neural_label), run_time=max(0.05, 0.82))

        # Beat 3: noise layers fade out one at a time, waveform becomes cleaner
        self.wait(max(0.05, 0.20))
        self.play(FadeOut(noise1), run_time=max(0.05, 0.65))
        self.play(FadeOut(noise2), run_time=max(0.05, 0.65))
        self.play(FadeOut(noise3), run_time=max(0.05, 0.65))
        self.wait(max(0.05, 0.43))
        self.wait(max(0.05, 0.88))

        # Beat 4: blank inset panel, then frequency axes
        self.play(FadeIn(panel), run_time=max(0.05, 0.8))
        self.play(panel.animate.scale(1.2), Create(axes), Write(x_label), Write(y_label), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.2))

        # Beat 5: frequency peaks rise one at a time, faint arrow connects waveform to inset
        peak_specs = [(8, 0.7, YELLOW), (15, 0.9, ORANGE), (25, 0.6, GREEN), (40, 0.8, PURPLE)]
        arrow_to_inset = Arrow(
            start=np.array([2.2, 0.5, 0]),
            end=panel.get_left() + DOWN * 0.2,
            color=GREY_B,
            stroke_opacity=0.4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.08,
            stroke_width=2,
        )
        peak_lines = VGroup()
        per_peak = 3.04 / 4
        for i, (freq, power, color) in enumerate(peak_specs):
            peak = Line(axes.coords_to_point(freq, 0), axes.coords_to_point(freq, power), color=color, stroke_width=6)
            peak_lines.add(peak)
            if i == 0:
                self.play(Create(peak), FadeIn(arrow_to_inset), run_time=max(0.05, 0.5))
            else:
                self.play(Create(peak), run_time=max(0.05, 0.5))
            self.play(Indicate(peak, scale_factor=1.15, color=WHITE), run_time=max(0.05, 0.26))

        inset_group = VGroup(panel, axes, x_label, y_label, peak_lines, arrow_to_inset)

        # Beat 6: inset fades slightly, main waveform remains settled
        self.play(inset_group.animate.set_opacity(0.4), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.5))

        # Beat 7: question text appears, then question mark at boundary
        self.play(FadeIn(question_text), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.88))
        self.add(qmark)

        # Beat 8: question mark scales up and down, waveform highlighted
        self.wait(max(0.05, 1.24))
        highlight = SurroundingRectangle(wave, color=YELLOW, buff=0.1, stroke_width=3, stroke_opacity=0.85)
        self.play(Create(highlight), qmark.animate.scale(1.3), run_time=max(0.05, 1.2))
        self.play(qmark.animate.scale(1 / 1.3), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.66))

        # Beat 9: question mark dims, red No stamp answers the question
        self.play(qmark.animate.set_opacity(0.6), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.24))
        self.play(FadeIn(no_stamp), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 2.98))
        self.play(Indicate(no_stamp, scale_factor=1.08, color=RED), run_time=max(0.05, 0.56))

        # Beat 10: No and question mark fade out, waveform starts morphing
        self.play(FadeOut(qmark), FadeOut(no_stamp), FadeOut(highlight), run_time=max(0.05, 0.56))
        self.play(Transform(wave, wave_complex1), run_time=max(0.05, 1.0))
        self.play(Transform(wave, wave_complex2), run_time=max(0.05, 1.72))

        # Beat 11: timeline appears, Rest marker, waveform relaxes
        self.play(FadeIn(timeline_line), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.36))
        self.play(GrowFromCenter(rest_marker), Transform(wave, wave_rest), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.27))

        # Beat 12: Movement marker, high-frequency large-amplitude waveform
        self.play(GrowFromCenter(movement_marker), Transform(wave, wave_movement), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.38))

        # Beat 13: Stimulus marker, spiky burst then moderate oscillation
        self.play(GrowFromCenter(stimulus_marker), Transform(wave, wave_stimulus), run_time=max(0.05, 0.5))
        self.play(Transform(wave, wave_moderate), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.74))

        # Beat 14: Sleep, then Cognition markers and corresponding waveform states
        self.play(GrowFromCenter(sleep_marker), Transform(wave, wave_sleep), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.48))
        self.play(GrowFromCenter(cogn_marker), Transform(wave, wave_cog), run_time=max(0.05, 0.38))

        # Beat 15: waveform cycles through the five named states
        cycle_targets = [wave_rest, wave_movement, wave_stimulus, wave_sleep, wave_cog]
        per_cycle = 4.52 / 5
        for target in cycle_targets:
            self.play(Transform(wave, target), run_time=max(0.05, 0.72))
            self.wait(max(0.05, per_cycle - 0.72))

        # Beat 16: further non-repeating morphological changes
        variant_targets = [wave_var1, wave_var2, wave_var3, wave_var4]
        per_variant = 1.15
        for target in variant_targets:
            self.play(Transform(wave, target), run_time=max(0.05, per_variant * 0.8))
            self.wait(max(0.05, per_variant * 0.2))

        wave_timeline_group = VGroup(wave, timeline_line, marker_group)

        # Beat 17: freeze moment, soft glow, slow pan, title replaces question
        self.wait(max(0.05, 0.62))
        self.play(Indicate(wave, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 0.5))
        self.play(wave_timeline_group.animate.shift(RIGHT * 0.2), run_time=max(0.05, 2.26))
        self.play(FadeOut(question_text), FadeIn(title_text), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.54))

        # Beat 18: timeline markers dim slightly, waveform resumes morphing to the end
        self.play(marker_group.animate.set_opacity(0.6), Transform(wave, wave_final), run_time=max(0.05, 0.78))