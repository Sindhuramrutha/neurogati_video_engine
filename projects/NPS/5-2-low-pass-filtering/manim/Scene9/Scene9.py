ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Previous scene's summary card (visible at start, fades out)
        # ------------------------------------------------------------
        summary_card = VGroup()
        card_rect = Rectangle(
            width=11.0,
            height=6.5,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=GREY_B,
            fill_opacity=0.2,
        )
        card_title = Text(
            "Low-Pass Filter — Summary",
            font_size=30,
            color=WHITE,
            weight=BOLD,
        ).move_to(UP * 1.4)
        card_bullets = VGroup(
            Text("Allows low-frequency components to pass.", font_size=22, color=WHITE),
            Text("Reduces frequencies above the cutoff.", font_size=22, color=WHITE),
            Text("Suppresses high-frequency interference.", font_size=22, color=WHITE),
            Text("Choose cutoff carefully to preserve useful information.", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.2)
        summary_card.add(card_rect, card_title, card_bullets).move_to(ORIGIN)
        self.add(summary_card)

        # ------------------------------------------------------------
        # Waveform data and component trackers
        # ------------------------------------------------------------
        x_min, x_max = -5.5, 5.5
        n_points = 300
        xs = np.linspace(x_min, x_max, n_points)

        drift_amp_tracker = ValueTracker(0.50)
        drift_phase_tracker = ValueTracker(0.4)
        ripple_amp_tracker = ValueTracker(0.14)
        ripple_phase_tracker = ValueTracker(0.2)

        def drift_y_arr():
            amp = drift_amp_tracker.get_value()
            phase = drift_phase_tracker.get_value()
            return amp * np.sin(0.75 * xs + phase)

        def ripple_y_arr():
            amp = ripple_amp_tracker.get_value()
            phase = ripple_phase_tracker.get_value()
            return amp * np.sin(5.0 * xs + phase)

        def total_points():
            y = drift_y_arr() + ripple_y_arr()
            return np.column_stack([xs, y, np.zeros_like(xs)])

        def drift_points():
            y = drift_y_arr()
            return np.column_stack([xs, y, np.zeros_like(xs)])

        wave = VMobject(color=TEAL, stroke_width=4)
        wave.set_points_as_corners(total_points())

        drift_line = VMobject(color=GOLD, stroke_width=5)
        drift_line.set_points_as_corners(drift_points())

        # ------------------------------------------------------------
        # BEAT 1: 0.00 - 2.82
        # ------------------------------------------------------------
        self.play(FadeOut(summary_card), run_time=max(0.05, 0.8))
        self.play(Create(wave), run_time=max(0.05, 1.2))
        wave.add_updater(lambda mob: mob.set_points_as_corners(total_points()))
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------
        # BEAT 2: 2.82 - 4.40
        # ------------------------------------------------------------
        self.play(Write(drift_line), run_time=max(0.05, 0.6))
        drift_line.add_updater(lambda mob: mob.set_points_as_corners(drift_points()))
        self.play(
            Indicate(drift_line, color=GOLD, scale_factor=1.08),
            wave.animate.set_opacity(0.55),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 0.38))

        # gap to 5.46
        self.wait(max(0.05, 1.06))

        # ------------------------------------------------------------
        # BEAT 3: 5.46 - 8.06
        # ------------------------------------------------------------
        self.play(
            wave.animate.set_stroke(color=GREY_B, width=3, opacity=0.7),
            run_time=max(0.05, 0.8),
        )
        self.play(
            drift_line.animate.set_stroke(color=RED, width=7),
            run_time=max(0.05, 0.6),
        )
        self.play(
            Indicate(drift_line, color=RED, scale_factor=1.10),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 0.6))

        # gap to 9.28
        self.wait(max(0.05, 1.22))

        # ------------------------------------------------------------
        # BEAT 4: 9.28 - 12.04
        # ------------------------------------------------------------
        label_drift = Text(
            "Unwanted Low-Frequency Drift",
            font_size=22,
            color=RED,
        ).move_to(np.array([-2.7, 2.15, 0]))

        label_fast = Text(
            "Useful High-Frequency Signal",
            font_size=22,
            color=GREEN,
        ).move_to(np.array([2.8, 2.15, 0]))

        drift_anchor_x = -2.2
        fast_anchor_x = 2.2
        drift_anchor_y = drift_amp_tracker.get_value() * np.sin(
            0.75 * drift_anchor_x + drift_phase_tracker.get_value()
        )
        fast_anchor_y = drift_anchor_y + ripple_amp_tracker.get_value() * np.sin(
            5.0 * fast_anchor_x + ripple_phase_tracker.get_value()
        )

        drift_leader = Line(
            start=label_drift.get_bottom() + DOWN * 0.05,
            end=np.array([drift_anchor_x, drift_anchor_y, 0]),
            color=RED,
            stroke_width=1.5,
        )
        fast_leader = Line(
            start=label_fast.get_bottom() + DOWN * 0.05,
            end=np.array([fast_anchor_x, fast_anchor_y, 0]),
            color=GREEN,
            stroke_width=1.5,
        )

        labels_group = VGroup(label_drift, label_fast, drift_leader, fast_leader)

        self.play(
            FadeIn(labels_group, shift=UP * 0.2),
            run_time=max(0.05, 0.9),
        )
        self.play(
            Indicate(label_drift, color=RED, scale_factor=1.08),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 1.16))

        wave_group = VGroup(wave, drift_line, labels_group)

        # ------------------------------------------------------------
        # BEAT 5: 12.70 - 15.24
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.66))

        self.play(
            drift_phase_tracker.animate.set_value(drift_phase_tracker.get_value() + 2.0),
            drift_amp_tracker.animate.set_value(0.8),
            run_time=max(0.05, 0.7),
        )
        self.play(
            drift_phase_tracker.animate.set_value(drift_phase_tracker.get_value() + 0.7),
            drift_amp_tracker.animate.set_value(0.1),
            run_time=max(0.05, 0.5),
        )
        self.play(
            drift_amp_tracker.animate.set_value(0.45),
            run_time=max(0.05, 0.4),
        )
        self.play(
            Indicate(label_drift, color=RED, scale_factor=1.06),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 0.54))

        # ------------------------------------------------------------
        # BEAT 6: 15.90 - 19.18
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.66))

        self.play(
            wave.animate.set_stroke(color=TEAL, width=5, opacity=1.0),
            drift_line.animate.set_opacity(0.35),
            run_time=max(0.05, 0.7),
        )
        self.play(
            Indicate(label_fast, color=GREEN, scale_factor=1.12),
            run_time=max(0.05, 0.7),
        )
        self.play(
            ripple_amp_tracker.animate.set_value(0.24),
            run_time=max(0.05, 0.6),
        )
        self.play(
            ripple_amp_tracker.animate.set_value(0.14),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------
        # BEAT 7: 20.20 - 21.18
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.02))

        self.play(
            Indicate(drift_line, color=RED, scale_factor=1.05),
            drift_line.animate.set_opacity(0.55),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.48))

        # ------------------------------------------------------------
        # BEAT 8: 21.70 - 24.04
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.52))

        hp_title = Text(
            "High-Pass Filter",
            font_size=44,
            color=YELLOW,
            weight=BOLD,
        ).move_to(np.array([0, 2.85, 0]))

        hp_arrow = Arrow(
            start=hp_title.get_right() + RIGHT * 0.4,
            end=hp_title.get_right() + RIGHT * 2.0,
            color=GOLD,
            buff=0.1,
            stroke_width=5,
        )
        next_label = Text("Next Section", font_size=18, color=WHITE).next_to(
            hp_arrow, UP, buff=0.1
        )

        self.play(
            FadeIn(hp_title, shift=UP * 0.3),
            wave_group.animate.shift(DOWN * 1.7 + LEFT * 0.3),
            run_time=max(0.05, 1.2),
        )
        self.play(
            FadeIn(hp_arrow),
            FadeIn(next_label),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 0.54))

        # ------------------------------------------------------------
        # BEAT 9: 24.04 - 24.90
        # ------------------------------------------------------------
        self.play(
            Indicate(hp_title, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.4),
        )
        self.play(
            hp_arrow.animate.set_stroke(color=YELLOW, width=7),
            drift_amp_tracker.animate.set_value(0.04),
            ripple_amp_tracker.animate.set_value(0.22),
            wave.animate.set_stroke(color=TEAL, width=5, opacity=1.0),
            drift_line.animate.set_opacity(0.15),
            run_time=max(0.05, 0.46),
        )

        # ------------------------------------------------------------
        # BEAT 10: 24.90 - 25.65
        # ------------------------------------------------------------
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.3, 0.2],
            x_length=3.0,
            y_length=1.6,
            axis_config={"include_tip": False, "color": GREY_B},
            x_axis_config={"include_numbers": False, "color": GREY_B},
            y_axis_config={"include_numbers": False, "color": GREY_B},
        ).to_edge(RIGHT).shift(LEFT * 0.3 + DOWN * 0.2)

        hp_curve = axes.plot(
            lambda x: 1 / (1 + np.exp(-(x - 5) * 1.6)),
            x_range=[0, 10, 0.05],
            color=GREEN,
            stroke_width=4,
        )

        cutoff_dash = DashedLine(
            start=axes.c2p(5, 0),
            end=axes.c2p(5, 1.25),
            color=ORANGE,
            stroke_width=3,
        )
        cutoff_label = Text("Cutoff", font_size=13, color=ORANGE).next_to(
            cutoff_dash, UP, buff=0.05
        )

        preview = VGroup(axes, hp_curve, cutoff_dash, cutoff_label)
        self.play(FadeIn(preview, shift=UP * 0.1), run_time=max(0.05, 0.75))