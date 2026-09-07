ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


ASSET_PATHS = {
    "heart": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg",
    "brain": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg",
    "stopwatch": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg",
    "activity": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg",
    "soundwave": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg",
    "grid_matrix": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg",
    "bar_chart": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg",
    "graph_trend": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg",
    "cpu": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg",
    "funnel": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg",
    "table": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg",
    "hospital": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg",
    "capsule": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg",
    "clipboard_pulse": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg",
    "hand": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg",
    "broadcast": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg",
    "gear": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg",
    "arrow_repeat": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg",
    "lightbulb": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg",
    "bell": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg",
    "check_circle": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg",
    "x_circle": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg",
    "rulers": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg",
    "puzzle": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg",
    "fig_measurement_funnel": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png",
    "fig_mindmap_three_pillars": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png",
    "fig_mindmap_full": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png",
}


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_wave(func, t_range, color, stroke_width=3):
            return ParametricFunction(
                lambda t: np.array([t, func(t), 0]),
                t_range=t_range,
                color=color,
                stroke_width=stroke_width,
            )

        def normalize_visual(vis, width=1.4, height=0.5):
            vis.scale_to_fit_width(width)
            if vis.get_height() > height:
                vis.scale_to_fit_height(height)
            return vis

        def make_row(visual, label_text):
            label = Text(label_text, font_size=18, color=WHITE)
            row = VGroup(visual, label).arrange(RIGHT, buff=0.25)
            return row

        # ---------- neutral two-column skeleton ----------
        divider = Line(UP * 2.9, DOWN * 2.5, color=GREY_B, stroke_width=3)

        left_bg = Rectangle(
            width=6.2,
            height=5.4,
            color=GREY,
            fill_color=GREY,
            fill_opacity=0.06,
            stroke_color=GREY,
            stroke_opacity=0.35,
            stroke_width=1,
        ).move_to(LEFT * 3.3 + UP * 0.2)

        right_bg = Rectangle(
            width=6.2,
            height=5.4,
            color=GREY,
            fill_color=GREY,
            fill_opacity=0.06,
            stroke_color=GREY,
            stroke_opacity=0.35,
            stroke_width=1,
        ).move_to(RIGHT * 3.3 + UP * 0.2)

        left_header = Text("Signal", color=GREEN, font_size=48, weight="BOLD").move_to(
            LEFT * 3.3 + UP * 2.35
        )
        right_header = Text("Noise", color=RED, font_size=48, weight="BOLD").move_to(
            RIGHT * 3.3 + UP * 2.35
        )

        # ---------- left column: Signal items ----------
        brain_icon = (
            SVGMobject(ASSET_PATHS["brain"])
            .set_color(GREEN)
            .set_fill(GREEN, opacity=0.45)
            .scale_to_fit_height(0.30)
        )
        brain_icon.scale_to_fit_width(0.32)

        eeg_wave = normalize_visual(
            make_wave(
                lambda x: 0.28 * np.sin(3.2 * x) + 0.12 * np.sin(7.0 * x) + 0.06 * np.sin(12.0 * x),
                [-0.8, 0.8, 0.01],
                GREEN,
            )
        )
        eeg_visual = VGroup(brain_icon, eeg_wave).arrange(DOWN, buff=0.03).scale_to_fit_width(1.3)

        emg_wave = normalize_visual(
            make_wave(
                lambda x: 0.30 * np.exp(-0.5 * (x / 0.28) ** 2) * np.sin(22 * x),
                [-0.8, 0.8, 0.01],
                GREEN,
            )
        )
        emg_tag = Text("EMG", font_size=13, color=YELLOW).next_to(emg_wave, UP, buff=0.02)
        emg_visual = VGroup(emg_wave, emg_tag).arrange(DOWN, buff=0.02)

        lfp_wave = normalize_visual(
            make_wave(
                lambda x: 0.30 * np.sin(1.8 * x) + 0.08 * np.sin(3.6 * x),
                [-0.8, 0.8, 0.01],
                TEAL,
            )
        )
        lfp_visual = lfp_wave

        spike_positions = np.linspace(-0.65, 0.65, 5)
        spike_lines = VGroup(
            *[
                Line(np.array([x, -0.18, 0]), np.array([x, 0.18, 0]), color=GREEN, stroke_width=2.5)
                for x in spike_positions
            ]
        )
        spike_visual = normalize_visual(spike_lines)

        eeg_row = make_row(eeg_visual, "Brain activity — EEG")
        emg_row = make_row(emg_visual, "Muscle activity — EMG")
        lfp_row = make_row(lfp_visual, "Local field potentials")
        spike_row = make_row(spike_visual, "Neural spikes")

        left_rows = [eeg_row, emg_row, lfp_row, spike_row]
        left_visuals = [eeg_visual, emg_visual, lfp_visual, spike_visual]

        left_items = (
            VGroup(*left_rows)
            .arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            .next_to(left_header, DOWN, buff=0.35)
        )

        # ---------- right column: Noise items ----------
        interference_wave = normalize_visual(
            make_wave(
                lambda x: 0.22 * np.sign(np.sin(15 * x)) + 0.04 * np.sin(40 * x),
                [-0.9, 0.9, 0.005],
                RED,
            )
        )
        interference_visual = interference_wave

        motion_wave = normalize_visual(
            make_wave(
                lambda x: 0.28 * np.sin(1.7 * x) + 0.10 * np.sin(4.3 * x),
                [-0.9, 0.9, 0.01],
                ORANGE,
            )
        )
        motion_visual = motion_wave

        muscle_artifact_wave = normalize_visual(
            make_wave(
                lambda x: 0.35 * np.exp(-0.5 * (x / 0.25) ** 2) * np.sin(30 * x)
                + 0.15 * np.exp(-0.5 * ((x - 0.45) / 0.20) ** 2) * np.sin(45 * x),
                [-0.9, 0.9, 0.01],
                RED,
            )
        )
        muscle_artifact_visual = muscle_artifact_wave

        baseline_drift_wave = normalize_visual(
            make_wave(
                lambda x: 0.30 * np.tanh(1.4 * x) + 0.08 * np.sin(3.2 * x),
                [-0.9, 0.9, 0.01],
                PINK,
            )
        )
        baseline_drift_visual = baseline_drift_wave

        powerline_wave = normalize_visual(
            make_wave(
                lambda x: 0.24 * np.sin(36 * x),
                [-0.9, 0.9, 0.005],
                YELLOW,
            )
        )
        powerline_visual = powerline_wave

        interference_row = make_row(interference_visual, "Electrical interference")
        motion_row = make_row(motion_visual, "Motion artifacts")
        muscle_artifact_row = make_row(muscle_artifact_visual, "Muscle artifacts in EEG")
        baseline_drift_row = make_row(baseline_drift_visual, "Baseline drift")
        powerline_row = make_row(powerline_visual, "Power-line interference")

        right_rows = [
            interference_row,
            motion_row,
            muscle_artifact_row,
            baseline_drift_row,
            powerline_row,
        ]
        right_visuals = [
            interference_visual,
            motion_visual,
            muscle_artifact_visual,
            baseline_drift_visual,
            powerline_visual,
        ]

        right_items = (
            VGroup(*right_rows)
            .arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            .next_to(right_header, DOWN, buff=0.35)
        )

        # ---------- bottom goal note ----------
        goal_text = Text(
            "Goal: improve visibility of signal, preserve its characteristics.",
            font_size=26,
            color=WHITE,
            t2c={"Goal:": YELLOW},
        ).scale_to_fit_width(11)

        goal_bg = Rectangle(
            width=goal_text.width + 1.2,
            height=goal_text.height + 0.55,
            color=YELLOW,
            fill_color=BLACK,
            fill_opacity=0.6,
            stroke_width=1.5,
        )
        goal_text.move_to(goal_bg.get_center())
        goal_note = VGroup(goal_bg, goal_text).move_to(DOWN * 3.1)

        # ---------- timeline ----------
        # Beat 1: 0.00-3.68
        self.play(Create(divider), FadeIn(left_bg), FadeIn(right_bg), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 1.68))

        # Beat 2: 3.68-7.68
        self.play(
            FadeIn(left_header),
            left_bg.animate.set_fill(GREEN, opacity=0.12).set_stroke(GREEN, width=1.5, opacity=0.5),
            run_time=max(0.05, 4.0),
        )

        # gap 7.68-8.76
        self.wait(max(0.05, 1.08))

        # Beat 3: 8.76-10.60
        self.play(FadeIn(left_rows[0]), run_time=max(0.05, 0.8))
        self.play(Wiggle(left_visuals[0], scale_value=0.04), run_time=max(0.05, 1.04))

        # gap 10.60-11.36
        self.wait(max(0.05, 0.76))

        # Beat 4: 11.36-12.84
        self.play(FadeIn(left_rows[1]), run_time=max(0.05, 1.48))

        # gap 12.84-13.32
        self.wait(max(0.05, 0.48))

        # Beat 5: 13.32-15.12
        self.play(FadeIn(left_rows[2]), FadeIn(left_rows[3]), run_time=max(0.05, 1.80))

        # gap 15.12-16.18
        self.wait(max(0.05, 1.06))

        # Beat 6: 16.18-20.36
        self.play(
            FadeIn(right_header),
            right_bg.animate.set_fill(RED, opacity=0.12).set_stroke(RED, width=1.5, opacity=0.5),
            run_time=max(0.05, 4.18),
        )

        # gap 20.36-21.32
        self.wait(max(0.05, 0.96))

        # Beat 7: 21.32-22.94
        self.play(FadeIn(right_rows[0]), run_time=max(0.05, 1.62))

        # gap 22.94-23.66
        self.wait(max(0.05, 0.72))

        # Beat 8: 23.66-26.28
        self.play(FadeIn(right_rows[1]), FadeIn(right_rows[2]), run_time=max(0.05, 2.62))

        # gap 26.28-27.24
        self.wait(max(0.05, 0.96))

        # Beat 9: 27.24-28.94
        self.play(FadeIn(right_rows[3]), FadeIn(right_rows[4]), run_time=max(0.05, 1.70))

        # gap 28.94-29.78
        self.wait(max(0.05, 0.84))

        # Beat 10: 29.78-34.92
        self.play(
            Wiggle(left_header, scale_value=0.02),
            Wiggle(right_header, scale_value=0.02),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 3.14))

        # gap 34.92-35.60
        self.wait(max(0.05, 0.68))

        # Beat 11: 35.60-42.50
        self.play(FadeIn(goal_note), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 4.90))

        # Beat 12: 42.50-43.50
        self.wait(max(0.05, 1.00))