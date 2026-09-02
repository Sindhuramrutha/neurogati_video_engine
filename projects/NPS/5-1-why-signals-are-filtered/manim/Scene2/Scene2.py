ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- component functions ----------
        def brain_y(x):
            return 0.28 * np.sin(2.2 * x) + 0.12 * np.sin(5.0 * x + 1.0) + 0.06 * np.sin(9.0 * x)

        def drift_y(x):
            return 0.5 * np.sin(0.45 * x + 0.8) + 0.15 * np.sin(0.9 * x)

        def elec_y(x):
            return 0.10 * np.sin(22.0 * x) + 0.05 * np.sin(37.0 * x)

        def muscle_y(x):
            y = np.zeros_like(x)
            centers = [-1.8, -1.0, -0.2, 0.6, 1.4]
            amps = [0.6, -0.8, 0.9, -0.7, 0.6]
            widths = [0.15, 0.12, 0.1, 0.13, 0.12]
            for c, a, w in zip(centers, amps, widths):
                y += a * np.exp(-((x - c) / w) ** 2)
            return y

        def power_y(x):
            return 0.22 * np.sin(12.0 * x)

        def trace_point(f, y_center=1.3, y_scale=1.0):
            return lambda t: np.array([t, y_center + y_scale * f(t), 0])

        def mini_trace_point(f, x_scale=0.45, y_scale=0.5):
            return lambda t: np.array([t * x_scale, y_scale * f(t), 0])

        # ---------- main trace components ----------
        main_y = 1.3
        brain_curve = ParametricFunction(
            trace_point(brain_y),
            t_range=[-6, 6, 0.01],
            color=BLUE,
            stroke_width=4,
        )
        drift_curve = ParametricFunction(
            trace_point(drift_y),
            t_range=[-6, 6, 0.01],
            color=ORANGE,
            stroke_width=4,
        )
        elec_curve = ParametricFunction(
            trace_point(elec_y),
            t_range=[-6, 6, 0.01],
            color=PURPLE,
            stroke_width=2,
        )
        muscle_curve = ParametricFunction(
            trace_point(muscle_y),
            t_range=[-6, 6, 0.01],
            color=RED,
            stroke_width=3,
        )
        power_curve = ParametricFunction(
            trace_point(power_y),
            t_range=[-6, 6, 0.01],
            color=YELLOW,
            stroke_width=2,
        )
        power_curve.set_opacity(0)

        baseline = Line(LEFT * 6 + UP * main_y, RIGHT * 6 + UP * main_y, color=GREY, stroke_width=1).set_opacity(0.3)
        self.add(baseline)

        # Beat 1: 0.00-1.52
        self.play(FadeIn(brain_curve), run_time=max(0.05, 1.52))

        # Beat 2: 1.52-2.64
        self.wait(max(0.05, 1.12))

        # Beat 3: 2.64-5.34
        self.play(FadeIn(drift_curve), run_time=max(0.05, 2.70))

        # Beat 4: 5.34-7.38
        self.play(FadeIn(elec_curve), run_time=max(0.05, 2.04))

        # Beat 5: 7.38-8.74
        self.play(FadeIn(muscle_curve), run_time=max(0.05, 1.36))

        # Beat 6: 8.74-10.86
        self.play(brain_curve.animate.set_opacity(0.9), run_time=max(0.05, 2.12))

        # Beat 7: 10.86-12.20
        self.wait(max(0.05, 1.34))

        # Beat 8: 12.20-15.36
        label1 = Text("Filtering does not create new information.", color=WHITE, font_size=36).move_to(DOWN * 1.8)
        self.play(FadeIn(label1), run_time=max(0.05, 3.16))

        # Beat 9: 15.36-16.24
        self.wait(max(0.05, 0.88))

        # Beat 10: 16.24-19.66
        self.play(FadeOut(label1), run_time=max(0.05, 1.0))
        self.play(
            drift_curve.animate.set_opacity(0.25),
            elec_curve.animate.set_opacity(0.25),
            muscle_curve.animate.set_opacity(0.25),
            brain_curve.animate.set_opacity(1.0),
            run_time=max(0.05, 2.42),
        )

        # Beat 11: 19.66-23.32
        label2 = Text(
            "Removes components unlikely to contain useful physiological information.",
            color=WHITE,
            font_size=32,
        ).scale_to_fit_width(10).move_to(DOWN * 1.8)
        self.play(FadeIn(label2), run_time=max(0.05, 3.66))

        # Beat 12: 23.32-24.26
        self.play(
            FadeOut(label2),
            drift_curve.animate.set_opacity(0.6),
            elec_curve.animate.set_opacity(0.6),
            muscle_curve.animate.set_opacity(0.6),
            run_time=max(0.05, 0.94),
        )

        # Beat 13: 24.26-26.02
        title = Text("EEG Recording", color=WHITE, font_size=44).to_edge(UP, buff=0.3)
        self.play(
            FadeOut(drift_curve),
            FadeOut(elec_curve),
            FadeOut(muscle_curve),
            FadeIn(title),
            run_time=max(0.05, 1.76),
        )

        # Beat 14: 26.02-30.32
        big_brain = ParametricFunction(
            trace_point(brain_y, y_center=-0.5, y_scale=1.6),
            t_range=[-6, 6, 0.01],
            color=TEAL,
            stroke_width=8,
        )
        brain_label = Text("Brain activity", color=TEAL, font_size=38).next_to(big_brain, UP, buff=0.3)
        self.play(
            brain_curve.animate.set_opacity(0.25),
            FadeIn(big_brain),
            FadeIn(brain_label),
            run_time=max(0.05, 4.30),
        )

        # Beat 15: 30.32-30.86
        self.wait(max(0.05, 0.54))

        # Beat 16: 30.86-32.58
        self.play(Indicate(big_brain, scale_factor=1.1, color=TEAL), run_time=max(0.05, 1.72))

        # gap 32.58-33.18
        self.wait(max(0.05, 0.60))

        # Beat 17: 33.18-35.44
        big_drift = ParametricFunction(
            trace_point(drift_y, y_center=-0.5, y_scale=1.6),
            t_range=[-6, 6, 0.01],
            color=ORANGE,
            stroke_width=8,
        )
        drift_label = Text("Baseline drift", color=ORANGE, font_size=38).next_to(big_drift, UP, buff=0.3)
        self.play(FadeOut(big_brain), FadeOut(brain_label), run_time=max(0.05, 0.7))
        self.play(FadeIn(big_drift), FadeIn(drift_label), run_time=max(0.05, 1.56))

        # Beat 18: 35.44-36.32
        self.wait(max(0.05, 0.88))

        # gap 36.32-36.80
        self.wait(max(0.05, 0.48))

        # Beat 19: 36.80-38.92
        big_elec = ParametricFunction(
            trace_point(elec_y, y_center=-0.5, y_scale=2.0),
            t_range=[-6, 6, 0.01],
            color=PURPLE,
            stroke_width=8,
        )
        elec_label = Text("Electrical interference", color=PURPLE, font_size=36).next_to(big_elec, UP, buff=0.3)
        self.play(FadeOut(big_drift), FadeOut(drift_label), run_time=max(0.05, 0.6))
        self.play(FadeIn(big_elec), FadeIn(elec_label), run_time=max(0.05, 1.52))

        # Beat 20: 38.92-39.50
        self.wait(max(0.05, 0.58))

        # Beat 21: 39.50-41.34
        big_muscle = ParametricFunction(
            trace_point(muscle_y, y_center=-0.5, y_scale=2.0),
            t_range=[-6, 6, 0.01],
            color=RED,
            stroke_width=8,
        )
        muscle_label = Text("Muscle activity", color=RED, font_size=36).next_to(big_muscle, UP, buff=0.3)
        self.play(FadeOut(big_elec), FadeOut(elec_label), run_time=max(0.05, 0.6))
        self.play(FadeIn(big_muscle), FadeIn(muscle_label), run_time=max(0.05, 1.24))

        # Beat 22: 41.34-41.76
        self.wait(max(0.05, 0.42))

        # Beat 23: 41.76-42.76
        big_power = ParametricFunction(
            trace_point(power_y, y_center=-0.5, y_scale=2.0),
            t_range=[-6, 6, 0.01],
            color=YELLOW,
            stroke_width=8,
        )
        power_label = Text("Power-line interference", color=YELLOW, font_size=36).next_to(big_power, UP, buff=0.3)
        self.play(FadeOut(big_muscle), FadeOut(muscle_label), run_time=max(0.05, 0.4))
        self.play(FadeIn(big_power), FadeIn(power_label), run_time=max(0.05, 0.6))

        # Beat 24: 42.76-43.76
        artifacts_info = [
            (drift_y, ORANGE, "Baseline drift"),
            (elec_y, PURPLE, "Electrical interference"),
            (muscle_y, RED, "Muscle activity"),
            (power_y, YELLOW, "Power-line interference"),
        ]
        mini_cards = []
        for func, color, label_text in artifacts_info:
            mini_curve = ParametricFunction(
                mini_trace_point(func),
                t_range=(-2.5, 2.5, 0.05),
                color=color,
                stroke_width=5,
            )
            mini_label = Text(label_text, font_size=20, color=color).next_to(mini_curve, DOWN, buff=0.15)
            mini_cards.append(VGroup(mini_curve, mini_label))
        mini_artifact_row = VGroup(*mini_cards).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)

        self.play(FadeOut(big_power), FadeOut(power_label), run_time=max(0.05, 0.35))
        self.play(FadeIn(mini_artifact_row), run_time=max(0.05, 0.65))

        # Beat 25: 43.76-45.92
        self.play(
            FadeIn(drift_curve),
            FadeIn(elec_curve),
            FadeIn(muscle_curve),
            FadeIn(power_curve),
            brain_curve.animate.set_opacity(0.3),
            mini_artifact_row.animate.set_opacity(0.5),
            run_time=max(0.05, 2.16),
        )

        # Beat 26: 45.92-46.52
        self.play(
            drift_curve.animate.set_opacity(0.7),
            elec_curve.animate.set_opacity(0.7),
            muscle_curve.animate.set_opacity(0.7),
            power_curve.animate.set_opacity(0.7),
            run_time=max(0.05, 0.60),
        )

        # Beat 27: 46.52-48.36
        difficult_label = Text("Difficult to identify brain activity.", color=WHITE, font_size=34).move_to(DOWN * 1.0)
        self.play(FadeIn(difficult_label), run_time=max(0.05, 1.84))

        # Beat 28: 48.36-50.12
        self.play(Indicate(brain_curve, scale_factor=1.1, color=BLUE), run_time=max(0.05, 0.88))
        self.play(brain_curve.animate.set_opacity(0.2), run_time=max(0.05, 0.88))

        # Beat 29: 50.12-50.90
        self.play(FadeOut(difficult_label), run_time=max(0.05, 0.78))

        # Beat 30: 50.90-53.96
        boundary = DashedLine(start=UP * 3.5, end=DOWN * 3.5, color=GREY, stroke_width=1.5)
        self.play(FadeIn(boundary), run_time=max(0.05, 3.06))

        # Beat 31: 53.96-54.56
        bin_rect = Rectangle(width=2.2, height=1.6, color=GREY, fill_color=BLACK, fill_opacity=0.4, stroke_width=1.5)
        bin_text = Text("Removed", font_size=26, color=GREY).move_to(bin_rect.get_center())
        removed_bin = VGroup(bin_rect, bin_text).move_to(RIGHT * 4.5 + DOWN * 1.2)

        artifact_curves_main = VGroup(drift_curve, elec_curve, muscle_curve, power_curve)
        self.play(
            artifact_curves_main.animate.scale(0.15).move_to(removed_bin.get_center()).set_opacity(0.25),
            FadeOut(mini_artifact_row),
            FadeIn(removed_bin),
            run_time=max(0.05, 0.60),
        )

        # Beat 32: 54.56-57.78
        preserved_curve = ParametricFunction(
            trace_point(brain_y, y_center=0, y_scale=1.8),
            t_range=[-5.5, 5.5, 0.01],
            color=TEAL,
            stroke_width=7,
        )
        preserved_label = Text("Preserved signal", color=TEAL, font_size=40).next_to(preserved_curve, DOWN, buff=0.5)
        self.play(
            FadeOut(brain_curve),
            FadeIn(preserved_curve),
            FadeIn(preserved_label),
            run_time=max(0.05, 3.22),
        )

        # Beat 33: 57.78-58.62
        self.wait(max(0.05, 0.84))

        # Beat 34: 58.62-63.34
        self.play(
            preserved_curve.animate.scale(1.08),
            preserved_label.animate.scale(1.05),
            run_time=max(0.05, 2.36),
        )
        self.play(
            preserved_curve.animate.scale(1 / 1.08),
            preserved_label.animate.scale(1 / 1.05),
            run_time=max(0.05, 2.36),
        )

        # Beat 35: 63.34-64.26
        self.wait(max(0.05, 0.92))

        # Beat 36: 64.26-67.64
        self.play(Indicate(preserved_curve, scale_factor=1.05, color=TEAL), run_time=max(0.05, 3.38))

        # Beat 37: 67.64-68.84
        self.wait(max(0.05, 1.20))

        # Beat 38: 68.84-71.44
        def_text_partial = Text(
            "Signal filtering = preserving useful signal components...",
            color=WHITE,
            font_size=28,
        ).scale_to_fit_width(10).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(def_text_partial), run_time=max(0.05, 2.60))

        # Beat 39: 71.44-73.94
        def_text_full = Text(
            "Signal filtering = preserving useful signal components while attenuating unwanted components.",
            color=WHITE,
            font_size=28,
        ).scale_to_fit_width(10).to_edge(DOWN, buff=0.4)
        self.play(ReplacementTransform(def_text_partial, def_text_full), run_time=max(0.05, 2.50))

        # Beat 40: 73.94-76.48
        self.play(Indicate(preserved_curve, scale_factor=1.05, color=TEAL), run_time=max(0.05, 2.54))

        # Beat 41: 76.48-77.38
        self.wait(max(0.05, 0.90))