ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'
}

class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Title
        title = Text("High-Pass Filter", font_size=48, color=WHITE, weight="BOLD")
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=max(0.05, 0.8))

        # --- Beat 1: Remove low-frequency drift, keep high-frequency activity ---
        n_pts = 500
        t = np.linspace(0, 4 * np.pi, n_pts)
        low_drift = 1.5 * np.sin(0.5 * t) + 0.7 * np.cos(0.8 * t)
        high_activity = 0.8 * np.sin(8 * t) + 0.4 * np.sin(14 * t + 0.6)
        raw_signal = low_drift + high_activity
        filtered_signal = high_activity

        x_scale = 5.0 / (n_pts - 1)
        y_scale = 0.5
        y_center = 0.8

        raw_points = [
            np.array([-5.6 + i * x_scale, y_center + raw_signal[i] * y_scale, 0])
            for i in range(n_pts)
        ]
        raw_trace = VMobject(stroke_color=WHITE, stroke_width=2.5)
        raw_trace.set_points_as_corners(raw_points)

        drift_points = [
            np.array([-5.6 + i * x_scale, y_center + low_drift[i] * y_scale, 0])
            for i in range(n_pts)
        ]
        drift_curve = VMobject(stroke_color=RED, stroke_width=3)
        drift_curve.set_points_as_corners(drift_points)

        raw_label = Text("Raw recording", font_size=26, color=WHITE)
        raw_label.next_to(raw_trace, UP, buff=0.2)

        drift_label = Text("Low-frequency drift", font_size=22, color=RED)
        drift_label.next_to(raw_trace, DOWN, buff=0.2)

        filtered_points = [
            np.array([0.6 + i * x_scale, y_center + filtered_signal[i] * y_scale, 0])
            for i in range(n_pts)
        ]
        filtered_trace = VMobject(stroke_color=GREEN, stroke_width=4)
        filtered_trace.set_points_as_corners(filtered_points)

        filtered_label = Text("High-pass filtered", font_size=26, color=GREEN)
        filtered_label.next_to(filtered_trace, UP, buff=0.2)

        arrow = Arrow(LEFT, RIGHT, stroke_color=YELLOW, stroke_width=4, buff=0.4)
        arrow.move_to(np.array([0.0, y_center, 0]))

        self.play(FadeIn(raw_trace), Write(raw_label), run_time=max(0.05, 1.2))
        self.play(FadeIn(drift_curve), Write(drift_label), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.4))
        self.play(GrowArrow(arrow), run_time=max(0.05, 0.5))
        self.play(FadeIn(filtered_trace), Write(filtered_label), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.8))

        # --- Beat 2: Applications ---
        self.play(
            FadeOut(VGroup(raw_trace, drift_curve, raw_label, drift_label, arrow, filtered_trace, filtered_label)),
            run_time=max(0.05, 0.6
        ))

        app_title = Text("Typical Applications", font_size=40, color=YELLOW, weight="BOLD")
        app_title.move_to(UP * 2.5)

        apps = VGroup(
            Text("•  Remove baseline drift", font_size=28, color=WHITE),
            Text("•  Reduce slow motion artefacts", font_size=28, color=WHITE),
            Text("•  Isolate spike activity", font_size=28, color=WHITE),
        )
        apps.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        apps.next_to(app_title, DOWN, buff=0.8)

        self.play(Write(app_title), run_time=max(0.05, 0.8))
        for app in apps:
            self.play(Write(app), run_time=max(0.05, 0.6))
            self.wait(max(0.05, 0.2))

        drift_icon = SVGMobject(ASSET_PATHS["activity"], fill_color=TEAL, fill_opacity=1, stroke_width=0)
        drift_icon.scale(0.5)
        drift_icon.next_to(apps[0], LEFT, buff=0.6)
        self.play(FadeIn(drift_icon), run_time=max(0.05, 0.35))

        move_icon = SVGMobject(ASSET_PATHS["hand"], fill_color=ORANGE, fill_opacity=1, stroke_width=0)
        move_icon.scale(0.5)
        move_icon.next_to(apps[1], LEFT, buff=0.6)
        self.play(FadeIn(move_icon), run_time=max(0.05, 0.35))

        spike_icon = SVGMobject(ASSET_PATHS["soundwave"], fill_color=PURPLE, fill_opacity=1, stroke_width=0)
        spike_icon.scale(0.5)
        spike_icon.next_to(apps[2], LEFT, buff=0.6)
        self.play(FadeIn(spike_icon), run_time=max(0.05, 0.35))

        self.wait(max(0.05, 0.55))

        self.play(
            FadeOut(VGroup(app_title, apps, drift_icon, move_icon, spike_icon)),
            run_time=max(0.05, 0.6
        ))

        # --- Beat 3: Frequency response summary ---
        freq_ax = Line(LEFT * 5.5, RIGHT * 5.5, stroke_color=GREY, stroke_width=2)
        freq_ax.move_to(UP * 0.5)
        freq_label = Text("Frequency", font_size=24, color=GREY)
        freq_label.next_to(freq_ax, DOWN, buff=0.3)

        stop_band = Rectangle(
            width=4.0, height=1.8,
            fill_color=RED, fill_opacity=0.2, stroke_color=RED, stroke_width=2
        )
        stop_band.move_to(np.array([-3.0, 1.4, 0]))

        pass_band = Rectangle(
            width=6.0, height=1.8,
            fill_color=GREEN, fill_opacity=0.3, stroke_color=GREEN, stroke_width=2
        )
        pass_band.move_to(np.array([2.0, 1.4, 0]))

        stop_label = Text("Cut", font_size=30, color=RED, weight="BOLD")
        stop_label.move_to(stop_band.get_center())
        pass_label = Text("Pass", font_size=30, color=GREEN, weight="BOLD")
        pass_label.move_to(pass_band.get_center())

        cutoff_line = DashedLine(
            np.array([-1.0, 0.5, 0]),
            np.array([-1.0, 2.3, 0]),
            stroke_color=YELLOW, stroke_width=3
        )
        cutoff_text = Text("f cutoff", font_size=22, color=YELLOW)
        cutoff_text.next_to(cutoff_line, DOWN, buff=0.1)

        self.play(FadeIn(freq_ax), Write(freq_label), run_time=max(0.05, 0.6))
        self.play(FadeIn(stop_band), Write(stop_label), run_time=max(0.05, 0.7))
        self.play(FadeIn(pass_band), Write(pass_label), run_time=max(0.05, 0.7))
        self.play(FadeIn(cutoff_line), Write(cutoff_text), run_time=max(0.05, 0.6))

        phrase = Text(
            "Remove the drift, keep the spikes",
            font_size=40, color=WHITE, weight="BOLD"
        )
        phrase.to_edge(DOWN, buff=0.5)
        check_icon = SVGMobject(ASSET_PATHS["check_circle"], fill_color=GREEN, fill_opacity=1, stroke_width=0)
        check_icon.scale(0.7)
        check_icon.next_to(phrase, LEFT, buff=0.4)

        self.play(SpinInFromNothing(check_icon), Write(phrase), run_time=max(0.05, 0.92))