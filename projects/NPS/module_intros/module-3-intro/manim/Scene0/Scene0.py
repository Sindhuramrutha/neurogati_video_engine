ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 1. Title flies in from off-screen left
        title = Text("MODULE 3", font_size=60, weight="BOLD", color=YELLOW)
        title.to_edge(UP, buff=0.35)
        title_center = title.get_center()
        title.move_to(np.array([-9, title_center[1], 0]))
        self.add(title)
        self.play(
            title.animate.move_to(title_center),
            run_time=max(0.05, 0.48),
            rate_func=rate_functions.ease_out_cubic
        )

        # 2. Subtitle writes itself letter by letter
        subtitle = Text("Noise, Artifacts, and Preprocessing", font_size=36, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(AddTextLetterByLetter(subtitle), run_time=max(0.05, 1.02))

        # 3. Clean sine-like waveform draws across the middle
        def clean_func(x):
            return 0.55 * np.sin(1.5 * x)

        clean_wave = FunctionGraph(clean_func, x_range=[-5, 5], color=TEAL, stroke_width=4)
        clean_wave.move_to(np.array([0, -0.25, 0]))
        self.play(Create(clean_wave), run_time=max(0.05, 0.54))

        # 4. Jitter wiggles and large spikes overlay the clean trace
        main_y = -0.25
        rng = np.random.default_rng(42)

        def make_jitter(x0):
            xs = np.linspace(x0 - 0.18, x0 + 0.18, 9)
            y = main_y + clean_func(xs) + rng.uniform(-0.12, 0.12, size=9)
            pts = np.column_stack([xs, y, np.zeros_like(xs)])
            jitter = VMobject(stroke_color=ORANGE, stroke_width=3)
            jitter.set_points_as_corners(pts)
            return jitter

        def make_spike(x0):
            y0 = main_y + clean_func(x0)
            start = np.array([x0, y0, 0])
            end = np.array([x0, y0 + 0.75, 0])
            return Line(start, end, color=RED, stroke_width=7)

        jitter_xs = [-3.6, -1.2, 0.9, 3.2]
        spike_xs = [-2.6, 0.0, 2.4]
        jitters = [make_jitter(x) for x in jitter_xs]
        spikes = [make_spike(x) for x in spike_xs]

        # Small rough wiggles first
        for jitter in jitters:
            self.play(Create(jitter), run_time=max(0.05, 0.22))
            self.wait(max(0.05, 0.08))

        # Abrupt spikes next
        spike_wait = 1.10 / len(spikes) - 0.28
        for spike in spikes:
            self.play(GrowFromCenter(spike), run_time=max(0.05, 0.28))
            self.wait(max(0.05, spike_wait))

        # 5. Main waveform moves up; two comparison traces appear below
        shift_up = 0.4
        self.play(
            clean_wave.animate.shift(UP * shift_up),
            *[jitter.animate.shift(UP * shift_up) for jitter in jitters],
            *[spike.animate.shift(UP * shift_up) for spike in spikes],
            run_time=max(0.05, 0.6
        ))

        left_trace = FunctionGraph(
            lambda x: 0.25 * np.sin(2.0 * x),
            x_range=[-2, 2],
            color=GREEN,
            stroke_width=5
        )
        left_trace.move_to(np.array([-3.0, -1.7, 0]))

        right_seg1 = FunctionGraph(
            lambda x: 0.2 * np.sin(1.5 * x),
            x_range=[-2, 0],
            color=PURPLE,
            stroke_width=5
        )
        right_seg2 = FunctionGraph(
            lambda x: 0.55 * np.sin(3.5 * x),
            x_range=[0, 2],
            color=PURPLE,
            stroke_width=5
        )
        right_group = VGroup(right_seg1, right_seg2)
        right_group.move_to(np.array([3.0, -1.7, 0]))

        self.play(
            Create(left_trace),
            Create(right_seg1),
            Create(right_seg2),
            run_time=max(0.05, 1.6
        ))
        self.wait(max(0.05, 1.06))

        # 6. Comparison traces fade; labels appear near their former locations
        down_shift = 0.4
        self.play(
            FadeOut(left_trace),
            FadeOut(right_seg1),
            FadeOut(right_seg2),
            clean_wave.animate.shift(DOWN * down_shift),
            *[jitter.animate.shift(DOWN * down_shift) for jitter in jitters],
            *[spike.animate.shift(DOWN * down_shift) for spike in spikes],
            run_time=max(0.05, 0.90
        ))

        stationary_label = Text("Stationary", font_size=36, color=GREEN)
        stationary_label.move_to(np.array([-3.0, -2.3, 0]))
        nonstationary_label = Text("Nonstationary", font_size=36, color=PURPLE)
        nonstationary_label.move_to(np.array([3.0, -2.3, 0]))

        self.play(Write(stationary_label), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.25))
        self.play(
            FadeOut(stationary_label),
            Write(nonstationary_label),
            run_time=max(0.05, 0.60
        ))
        self.wait(max(0.05, 0.45))

        # 7. Spikes and jitter fade left to right, restoring the clean trace
        for spike in spikes:
            self.play(FadeOut(spike), run_time=max(0.05, 0.32))
            self.wait(max(0.05, 0.08))

        jitter_play = 0.38
        jitter_wait = (3.36 - len(spikes) * (0.32 + 0.08)) / len(jitters) - jitter_play
        for jitter in jitters:
            self.play(FadeOut(jitter), run_time=max(0.05, jitter_play))
            self.wait(max(0.05, jitter_wait))

        # 8. Clean waveform and remaining labels fade, leaving title/subtitle briefly
        self.play(
            FadeOut(clean_wave),
            FadeOut(nonstationary_label),
            run_time=max(0.05, 0.92
        ))

        # 9. Title and subtitle clear; closing phrase bursts in
        self.play(FadeOut(title), FadeOut(subtitle), run_time=max(0.05, 0.35))

        phrase = Text("Let's get started!", font_size=72, weight="BOLD", color=YELLOW)
        phrase.move_to(ORIGIN)
        phrase.scale(0.12)
        phrase.set_opacity(0)
        self.add(phrase)

        self.play(
            phrase.animate.scale(1 / 0.12).set_opacity(1),
            run_time=max(0.05, 0.45),
            rate_func=rate_functions.ease_out_cubic
        )
        self.play(
            Flash(phrase, color=YELLOW, line_length=0.3, flash_radius=1.4, num_lines=24),
            run_time=max(0.05, 0.25
        ))
        self.wait(max(0.05, 0.37))