ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

np.random.seed(42)


class Scene0(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # 1. Noisy waveform + "Time domain" label  (0.00 – 4.90 s)
        # ----------------------------------------------------------------
        x_vals = np.linspace(-4, 4, 200)
        y_vals = 0.7 * np.sin(2 * np.pi * 0.45 * x_vals) + 0.25 * np.random.randn(len(x_vals))
        points = [np.array([xi, yi, 0]) for xi, yi in zip(x_vals, y_vals)]

        waveform = VMobject(stroke_color=WHITE, stroke_width=2.5, fill_opacity=0)
        waveform.set_points_as_corners(points)
        waveform.scale_to_fit_width(7)

        label_time = Text("Time domain", color=WHITE, font_size=32)
        label_time.next_to(waveform, DOWN, buff=0.3)

        signal_group = VGroup(waveform, label_time).shift(LEFT * 1.2)

        self.play(
            Create(waveform, run_time=max(0.05, 3.0)),
            Write(label_time, run_time=max(0.05, 3.0)),
        )
        self.wait(max(0.05, 1.9))  # total beat 4.9 s

        # ----------------------------------------------------------------
        # 2. Three filter-symbol icons appear  (4.90 – 7.70 s)
        # ----------------------------------------------------------------
        def low_pass_fn(t):
            return np.array([t, 1 / (1 + np.exp((t - 0.5) / 0.25)), 0])

        def high_pass_fn(t):
            return np.array([t, 1 - 1 / (1 + np.exp((t + 0.5) / 0.25)), 0])

        def band_pass_fn(t):
            return np.array([t, np.exp(-((t) / 0.6) ** 2), 0])

        low_pass = ParametricFunction(
            low_pass_fn,
            t_range=np.array([-2, 2, 0.05]),
            stroke_color=ORANGE,
            stroke_width=4,
        ).scale(0.4)
        high_pass = ParametricFunction(
            high_pass_fn,
            t_range=np.array([-2, 2, 0.05]),
            stroke_color=BLUE,
            stroke_width=4,
        ).scale(0.4)
        band_pass = ParametricFunction(
            band_pass_fn,
            t_range=np.array([-2, 2, 0.05]),
            stroke_color=GREEN,
            stroke_width=4,
        ).scale(0.4)

        filter_icons = VGroup(low_pass, high_pass, band_pass).arrange(DOWN, buff=0.4)
        filter_icons.next_to(waveform, RIGHT, buff=0.8)

        self.play(
            AnimationGroup(
                GrowFromCenter(low_pass),
                GrowFromCenter(high_pass),
                GrowFromCenter(band_pass),
                lag_ratio=0.4,
            ),
            run_time=max(0.05, 1.8),
        )
        self.wait(max(0.05, 1.0))  # total beat 2.8 s

        # ----------------------------------------------------------------
        # 3. Large red X over the icons, then dim  (7.70 – 8.58 s)
        # ----------------------------------------------------------------
        cross = Text("X", color=RED, font_size=80).move_to(filter_icons)

        self.play(Write(cross, run_time=max(0.05, 0.5)))
        self.play(filter_icons.animate.set_opacity(0.5), run_time=max(0.05, 0.38))

        # ----------------------------------------------------------------
        # 4. Crossed-out icons slide away, waveform highlighted  (8.58 – 15.86 s)
        # ----------------------------------------------------------------
        self.play(
            filter_icons.animate.shift(RIGHT * 5),
            FadeOut(cross),
            waveform.animate.set_stroke(color=YELLOW, width=6),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 5.78))  # total beat 7.28 s

        # ----------------------------------------------------------------
        # 5. Cursor moves step-by-step along the waveform (15.86 – 17.02 s)
        # ----------------------------------------------------------------
        wave_points = waveform.get_points()
        sample_indices = np.linspace(0, len(wave_points) - 1, 8, dtype=int)
        sample_points = [wave_points[i] for i in sample_indices]

        cursor = Line(
            sample_points[0] + UP * 0.25,
            sample_points[0] + DOWN * 0.25,
            stroke_color=TEAL,
            stroke_width=5,
        )

        self.play(FadeIn(cursor, run_time=max(0.05, 0.08)))
        for i in range(1, len(sample_points)):
            self.play(cursor.animate.move_to(sample_points[i]), run_time=max(0.05, 0.12))
            if i < len(sample_points) - 1:
                self.wait(max(0.05, 0.02))
        self.play(FadeOut(cursor, run_time=max(0.05, 0.12)))
        # Total cursor beat = 1.16 s

        # ----------------------------------------------------------------
        # Long gap: keep waveform alive with a gentle pulse  (17.02 – 27.14 s)
        # ----------------------------------------------------------------
        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        waveform.add_updater(
            lambda mob: mob.set_stroke(
                color=YELLOW,
                width=5 + 0.5 * np.sin(2 * np.pi * 0.8 * time_tracker.get_value()),
            )
        )
        self.wait(max(0.05, 10.12))

        waveform.clear_updaters()
        time_tracker.clear_updaters()

        # ----------------------------------------------------------------
        # 6. Moving-average and Median icons appear  (27.14 – 30.16 s)
        # ----------------------------------------------------------------
        avg_bar = Rectangle(
            width=0.5,
            height=0.7,
            fill_color=GREY,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=2,
        )
        avg_overline = Line(
            avg_bar.get_left() + LEFT * 0.1,
            avg_bar.get_right() + RIGHT * 0.1,
            stroke_color=YELLOW,
            stroke_width=4,
        ).next_to(avg_bar, UP, buff=0.05)
        avg_icon = VGroup(avg_bar, avg_overline)
        avg_label = Text("Moving-Average", color=WHITE, font_size=28)
        avg_label.next_to(avg_icon, DOWN, buff=0.15)
        avg_group = VGroup(avg_icon, avg_label)

        med_marks = VGroup(*[
            Line(ORIGIN, UP * h, stroke_color=WHITE, stroke_width=3)
            for h in [0.4, 0.7, 0.5]
        ]).arrange(RIGHT, buff=0.25)
        med_marks[1].set_color(YELLOW).set_stroke(width=5)
        med_label = Text("Median", color=WHITE, font_size=28)
        med_label.next_to(med_marks, DOWN, buff=0.15)
        med_group = VGroup(med_marks, med_label)

        avg_group.next_to(waveform, RIGHT, buff=1.0)
        med_group.next_to(avg_group, RIGHT, buff=0.7)

        self.play(GrowFromCenter(avg_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.64))

        self.play(GrowFromCenter(med_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.38))  # total beat 3.02 s

        # ----------------------------------------------------------------
        # 7. Zoom slightly to center the two filter icons  (30.16 – 33.54 s)
        # ----------------------------------------------------------------
        target_center = VGroup(avg_group, med_group).get_center()

        self.play(
            self.camera.frame.animate.scale(0.6).move_to(target_center),
            waveform.animate.set_opacity(0.35),
            label_time.animate.set_opacity(0.35),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 1.38))  # total beat 3.38 s

        # ----------------------------------------------------------------
        # 8. Slow fade-out to transition  (33.54 – 34.48 s)
        # ----------------------------------------------------------------
        everything = VGroup(waveform, label_time, avg_group, med_group)
        self.play(FadeOut(everything), run_time=max(0.05, 0.94))