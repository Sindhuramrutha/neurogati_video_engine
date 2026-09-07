ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Card and layout constants
        # ------------------------------------------------------------
        card = Rectangle(
            width=12.4,
            height=7.0,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=GREY_B,
            fill_opacity=0.2,
        ).move_to(ORIGIN)

        heading = Text("Low-Pass Filter — Summary", font_size=30, color=WHITE, weight=BOLD)
        heading.move_to(np.array([0, 1.35, 0]))

        bullet1 = Text("Allows low-frequency components to pass.", font_size=26, color=WHITE)
        bullet1.move_to(np.array([0, 0.30, 0]))
        bullet1.scale_to_fit_width(9)

        bullet2 = Text("Reduces frequencies above the cutoff.", font_size=26, color=WHITE)
        bullet2.move_to(np.array([0, -0.70, 0]))
        bullet2.scale_to_fit_width(9)

        bullet3 = Text("Suppresses high-frequency interference.", font_size=26, color=WHITE)
        bullet3.move_to(np.array([0, -1.70, 0]))
        bullet3.scale_to_fit_width(9)

        bullet4 = Text(
            "Choose cutoff carefully to preserve useful information.",
            font_size=26,
            color=WHITE,
        )
        bullet4.move_to(np.array([0, -2.60, 0]))
        bullet4.scale_to_fit_width(9)

        # ------------------------------------------------------------
        # Waveform trackers and functions
        # ------------------------------------------------------------
        x_min, x_max = -5.5, 5.5
        n_wave = 400
        xs = np.linspace(x_min, x_max, n_wave)

        cutoff_x_tracker = ValueTracker(0.0)
        ripple_tracker = ValueTracker(1.0)

        def smooth_level_from_cutoff():
            c = cutoff_x_tracker.get_value()
            if c <= -3.2:
                return 1.0
            if c >= 0.0:
                return 0.0
            return -c / 3.2

        def get_wave_points():
            s = smooth_level_from_cutoff()
            r = ripple_tracker.get_value()
            low_amp = 0.45 * (1 - 0.9 * s)
            low = low_amp * np.sin(1.2 * xs + 1.0)
            ripple = 0.2 * r * (1 - s) * np.sin(4.5 * xs)
            bump = 0.26 * (1 - s) * np.exp(-((xs - 0.5) ** 2) / (2 * 0.12))
            ys = low + ripple + bump
            y_display = ys * 0.55 + 2.55
            return np.column_stack([xs, y_display, np.zeros_like(xs)])

        wave = VMobject(color=BLUE, stroke_width=4)
        wave.set_points_as_corners(get_wave_points())

        def current_wave_y_at_x(x):
            s = smooth_level_from_cutoff()
            r = ripple_tracker.get_value()
            low_amp = 0.45 * (1 - 0.9 * s)
            low = low_amp * np.sin(1.2 * x + 1.0)
            ripple = 0.2 * r * (1 - s) * np.sin(4.5 * x)
            bump = 0.26 * (1 - s) * np.exp(-((x - 0.5) ** 2) / (2 * 0.12))
            return (low + ripple + bump) * 0.55 + 2.55

        # ------------------------------------------------------------
        # BEAT 1: 0.00 - 2.76
        # ------------------------------------------------------------
        self.play(FadeIn(card), run_time=max(0.05, 0.5))
        self.play(FadeIn(wave, shift=UP * 0.1), run_time=max(0.05, 1.1))
        wave.add_updater(lambda mob: mob.set_points_as_corners(get_wave_points()))
        self.play(FadeIn(heading, shift=UP * 0.1), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------
        # BEAT 2: 2.76 - 5.78
        # ------------------------------------------------------------
        self.play(
            FadeIn(bullet1, shift=UP * 0.3 + RIGHT * 0.4),
            run_time=max(0.05, 0.7),
        )
        self.play(
            wave.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 1.12))

        # gap to 6.64
        self.wait(max(0.05, 0.86))

        # ------------------------------------------------------------
        # BEAT 3: 6.64 - 10.40
        # ------------------------------------------------------------
        travel_tracker = ValueTracker(0.0)
        travel_dot = Dot(radius=0.08, color=YELLOW)
        travel_dot.add_updater(
            lambda mob: mob.move_to(
                np.array(
                    [
                        x_min + travel_tracker.get_value() * (x_max - x_min),
                        current_wave_y_at_x(
                            x_min + travel_tracker.get_value() * (x_max - x_min)
                        ),
                        0,
                    ]
                )
            )
        )
        self.add(travel_dot)

        self.play(FadeIn(bullet2, shift=UP * 0.2), run_time=max(0.05, 0.7))
        self.play(Indicate(bullet1, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 0.9))
        self.play(
            travel_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=max(0.05, 2.0),
        )
        self.play(FadeOut(travel_dot), run_time=max(0.05, 0.16))

        # ------------------------------------------------------------
        # BEAT 4: 10.40 - 14.04
        # ------------------------------------------------------------
        cutoff_line = DashedLine(
            start=np.array([0, 1.8, 0]),
            end=np.array([0, 3.35, 0]),
            dash_length=0.1,
            color=ORANGE,
            stroke_width=3,
        )
        cutoff_line.add_updater(
            lambda mob: mob.put_start_and_end_on(
                np.array([cutoff_x_tracker.get_value(), 1.8, 0]),
                np.array([cutoff_x_tracker.get_value(), 3.35, 0]),
            )
        )

        cutoff_label = Text("Cutoff", font_size=20, color=ORANGE)
        cutoff_label.add_updater(
            lambda mob: mob.move_to(
                np.array([cutoff_x_tracker.get_value() + 0.55, 3.15, 0])
            )
        )

        def make_high_freq_squiggles(center_x):
            squigs = VGroup()
            for dx in [0.0, 0.8, 1.6]:
                cx = center_x + dx
                sx = np.linspace(cx - 0.35, cx + 0.35, 8)
                sy = 3.35 + 0.1 * np.sin((np.pi / 2) * np.arange(8))
                squig = VMobject(color=RED, stroke_width=2)
                squig.set_points_as_corners(
                    np.column_stack([sx, sy, np.zeros_like(sx)])
                )
                squigs.add(squig)
            return squigs

        hf_squiggles_4 = make_high_freq_squiggles(2.5)

        self.play(Write(cutoff_line), Write(cutoff_label), run_time=max(0.05, 0.55))
        self.play(Indicate(bullet2, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 0.8))
        self.play(FadeIn(hf_squiggles_4), run_time=max(0.05, 0.5))
        self.play(
            hf_squiggles_4.animate.shift(LEFT * 2.5).scale(0.5).set_opacity(0),
            run_time=max(0.05, 1.79),
        )

        # gap to 14.80
        self.wait(max(0.05, 0.76))

        # ------------------------------------------------------------
        # BEAT 5: 14.80 - 19.32
        # ------------------------------------------------------------
        hf_squiggles_5 = make_high_freq_squiggles(2.5)

        self.play(FadeIn(bullet3, shift=UP * 0.2), run_time=max(0.05, 0.7))
        self.play(FadeIn(hf_squiggles_5), run_time=max(0.05, 0.5))
        self.play(
            hf_squiggles_5.animate.shift(LEFT * 2.5).scale(0.5).set_opacity(0),
            run_time=max(0.05, 1.8),
        )
        self.play(ripple_tracker.animate.set_value(0.25), run_time=max(0.05, 0.6))
        self.play(ripple_tracker.animate.set_value(1.0), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.52))

        # ------------------------------------------------------------
        # BEAT 6: 19.32 - 20.56
        # ------------------------------------------------------------
        self.play(wave.animate.set_stroke(width=7), run_time=max(0.05, 0.55))
        self.play(Indicate(bullet3, color=YELLOW, scale_factor=1.06), run_time=max(0.05, 0.69))

        # gap to 21.32
        self.wait(max(0.05, 0.76))

        # ------------------------------------------------------------
        # BEAT 7: 21.32 - 24.50
        # ------------------------------------------------------------
        self.play(FadeIn(bullet4, shift=UP * 0.2), run_time=max(0.05, 0.58))
        self.play(cutoff_x_tracker.animate.set_value(-3.0), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.60))

        # ------------------------------------------------------------
        # BEAT 8: 24.50 - 27.92
        # ------------------------------------------------------------
        gx = np.linspace(0.15, 0.85, 100)
        gy = 2.55 + 0.45 * np.exp(-((gx - 0.5) ** 2) / (2 * 0.04))
        ghost_peak = VMobject(color=GREY, stroke_width=2, stroke_opacity=0.45)
        ghost_peak.set_points_as_corners(
            np.column_stack([gx, gy, np.zeros_like(gx)])
        )

        x_mark = Text("✗", font_size=26, color=RED)
        x_mark.move_to(np.array([0.5, 3.2, 0]))

        self.play(
            FadeIn(ghost_peak, shift=UP * 0.1),
            Write(x_mark),
            run_time=max(0.05, 0.55),
        )
        self.play(
            cutoff_x_tracker.animate.set_value(0.0),
            FadeOut(ghost_peak),
            FadeOut(x_mark),
            run_time=max(0.05, 1.2),
        )
        self.play(Indicate(bullet4, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.87))

        # ------------------------------------------------------------
        # BEAT 9: 27.92 - 28.82
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.90))