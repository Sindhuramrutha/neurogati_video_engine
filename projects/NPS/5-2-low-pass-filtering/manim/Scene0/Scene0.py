ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene0(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))

        def low_signal(x, t):
            return 0.55 * np.sin(0.6 * x + 0.8 * t) + 0.10 * np.sin(
                0.3 * x - 0.4 * t
            )

        def high_signal(x, t):
            return (
                0.28 * np.sin(8.0 * x + 6.0 * t)
                + 0.13 * np.sin(15.0 * x - 8.0 * t)
                + 0.06 * np.sin(24.0 * x + 4.0 * t)
            )

        def combined_signal(x, t):
            return low_signal(x, t) + high_signal(x, t)

        def make_wave(
            signal_func,
            y_tracker,
            color,
            x_range=(-6.2, 6.2),
            stroke_width=4,
        ):
            x0, x1 = x_range
            n = 150
            xs = np.linspace(x0, x1, n)
            zs = np.zeros_like(xs)

            wave = VMobject(color=color, stroke_width=stroke_width)
            wave.set_points_as_corners([ORIGIN])
            wave.set_opacity(0)

            def update(mob):
                t = time_tracker.get_value()
                yoff = y_tracker.get_value()
                ys = signal_func(xs, t)
                mob.set_points_as_corners(
                    np.column_stack((xs, ys + yoff, zs))
                )

            wave.add_updater(update)
            update(wave)
            return wave

        # Beat 1: title card
        title = Text("5.2 Low-Pass Filtering", font_size=72, color=WHITE)
        title.move_to(ORIGIN)
        self.play(FadeIn(title), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.46))

        # Beat 2: raw recording waveform
        raw_y = ValueTracker(0.8)
        raw_wave = make_wave(combined_signal, raw_y, WHITE, stroke_width=5)
        self.add(raw_wave)
        self.play(
            FadeOut(title),
            raw_wave.animate.set_opacity(1),
            run_time=max(0.05, 1.78),
        )

        # Beat 3: separate into smooth lower and jagged upper layers
        low_y = ValueTracker(0.8)
        high_y = ValueTracker(0.8)

        low_wave = make_wave(low_signal, low_y, TEAL, stroke_width=4)
        red_pre = make_wave(
            high_signal, high_y, RED, x_range=(-6.2, 0), stroke_width=4
        )
        red_post = make_wave(
            high_signal, high_y, RED, x_range=(0, 6.2), stroke_width=4
        )
        self.add(low_wave, red_pre, red_post)

        self.play(
            FadeOut(raw_wave),
            low_wave.animate.set_opacity(1),
            red_pre.animate.set_opacity(1),
            red_post.animate.set_opacity(1),
            low_y.animate.set_value(-1.0),
            high_y.animate.set_value(1.5),
            run_time=max(0.05, 2.4),
        )
        raw_wave.clear_updaters()
        self.remove(raw_wave)

        for _ in range(2):
            self.play(
                red_pre.animate.set_stroke(width=7),
                red_post.animate.set_stroke(width=7),
                run_time=max(0.05, 0.2),
            )
            self.play(
                red_pre.animate.set_stroke(width=4),
                red_post.animate.set_stroke(width=4),
                run_time=max(0.05, 0.2),
            )
        self.wait(max(0.05, 0.72))

        # Beat 4: alternate emphasis between high and low layers
        self.play(
            red_pre.animate.set_stroke(width=8, color=WHITE),
            red_post.animate.set_stroke(width=8, color=WHITE),
            run_time=max(0.05, 0.9),
        )
        self.play(
            red_pre.animate.set_stroke(width=4, color=RED),
            red_post.animate.set_stroke(width=4, color=RED),
            run_time=max(0.05, 0.9),
        )
        self.play(
            low_wave.animate.set_stroke(width=9, color=YELLOW),
            run_time=max(0.05, 0.9),
        )
        self.play(
            low_wave.animate.set_stroke(width=4, color=TEAL),
            run_time=max(0.05, 0.9),
        )

        # Beat 5: fast high-frequency pulse vs slow low-frequency pulse
        for _ in range(3):
            self.play(
                red_pre.animate.set_stroke(width=8),
                red_post.animate.set_stroke(width=8),
                run_time=max(0.05, 0.25),
            )
            self.play(
                red_pre.animate.set_stroke(width=4),
                red_post.animate.set_stroke(width=4),
                run_time=max(0.05, 0.25),
            )

        self.play(low_wave.animate.set_stroke(width=10), run_time=max(0.05, 1.2))
        self.play(low_wave.animate.set_stroke(width=4), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.94))

        # Beat 6: labels for each layer
        label_low = Text(
            "Physiological Activity", font_size=28, color=TEAL
        ).move_to(np.array([3.6, -2.3, 0]))
        label_high = Text(
            "High-Frequency Noise", font_size=28, color=RED
        ).move_to(np.array([3.6, 3.0, 0]))

        self.play(Write(label_low), Write(label_high), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 4.14))

        # Beat 7: sliding low-pass filter gate between layers
        filter_gate = self.build_filter_gate()
        filter_gate.move_to(np.array([-8, 1.0, 0]))
        self.add(filter_gate)
        self.play(
            filter_gate.animate.move_to(np.array([0, 1.0, 0])),
            run_time=max(0.05, 3.0),
        )
        self.wait(max(0.05, 0.52))

        # Beat 8: highlight open-bottom passage and flow
        passage_box = Rectangle(
            width=2.6,
            height=1.4,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.15,
            stroke_width=3,
        ).move_to(np.array([0, -1.0, 0]))

        green_arrow = Arrow(
            start=np.array([-3.2, -1.0, 0]),
            end=np.array([3.2, -1.0, 0]),
            color=GREEN,
            stroke_width=4,
            buff=0.15,
            max_tip_length_to_length_ratio=0.08,
        )

        red_arrow = Arrow(
            start=np.array([-3.2, 1.5, 0]),
            end=np.array([-1.35, 1.5, 0]),
            color=RED,
            stroke_width=4,
            buff=0.15,
            max_tip_length_to_length_ratio=0.12,
        )

        x_circ = Circle(
            radius=0.3,
            color=RED,
            fill_color=RED,
            fill_opacity=0.15,
            stroke_width=3,
        )
        x_line1 = Line(
            LEFT * 0.16 + UP * 0.16,
            RIGHT * 0.16 + DOWN * 0.16,
            color=RED,
            stroke_width=4,
        )
        x_line2 = Line(
            LEFT * 0.16 + DOWN * 0.16,
            RIGHT * 0.16 + UP * 0.16,
            color=RED,
            stroke_width=4,
        )
        x_mark = VGroup(x_circ, x_line1, x_line2).move_to(
            np.array([-1.2, 1.5, 0])
        )

        self.play(
            GrowFromCenter(passage_box),
            Create(green_arrow),
            Create(red_arrow),
            GrowFromCenter(x_mark),
            run_time=max(0.05, 1.8),
        )
        self.play(
            low_wave.animate.set_stroke(width=9, color=YELLOW),
            run_time=max(0.05, 1.2),
        )
        self.play(
            low_wave.animate.set_stroke(width=4, color=TEAL),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.56))

        # Beat 9: red high-frequency layer is removed after the filter
        self.play(FadeOut(red_post), run_time=max(0.05, 1.4))
        red_post.clear_updaters()
        self.remove(red_post)
        self.wait(max(0.05, 0.44))

        # Beat 10: broader context, caption, and pulse traveling along smooth wave
        caption = Text(
            "Neural Signal Processing", font_size=36, color=YELLOW
        ).to_edge(DOWN, buff=0.35)

        pulse_progress = ValueTracker(-6.0)
        pulse = Dot(radius=0.09, color=YELLOW, fill_opacity=1)

        def update_pulse(m):
            t = time_tracker.get_value()
            x = pulse_progress.get_value()
            y = low_signal(x, t) + low_y.get_value()
            m.move_to(np.array([x, y, 0]))

        pulse.add_updater(update_pulse)
        self.add(pulse)

        self.play(
            FadeIn(caption, shift=UP * 0.3),
            self.camera.frame.animate.scale(1.12),
            run_time=max(0.05, 0.9),
        )
        self.play(
            pulse_progress.animate.set_value(6.0),
            run_time=max(0.05, 2.2),
            rate_func=linear,
        )
        self.wait(max(0.05, 0.47))

    @staticmethod
    def build_filter_gate():
        top = Line(
            LEFT * 1.1 + UP * 1.3,
            RIGHT * 1.1 + UP * 1.3,
            color=BLUE,
            stroke_width=8,
        )
        left = Line(
            LEFT * 1.1 + DOWN * 1.3,
            LEFT * 1.1 + UP * 1.3,
            color=BLUE,
            stroke_width=8,
        )
        right = Line(
            RIGHT * 1.1 + DOWN * 1.3,
            RIGHT * 1.1 + UP * 1.3,
            color=BLUE,
            stroke_width=8,
        )

        slats = VGroup(
            *[
                Line(
                    LEFT * 0.95 + UP * y,
                    RIGHT * 0.95 + UP * y,
                    color=BLUE,
                    stroke_width=5,
                )
                for y in [-0.8, -0.4, 0.0, 0.4, 0.8, 1.1]
            ]
        )

        return VGroup(top, left, right, slats)