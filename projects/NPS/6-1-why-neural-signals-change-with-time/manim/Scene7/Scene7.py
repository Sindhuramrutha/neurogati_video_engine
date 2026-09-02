ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Heading at top center
        heading = Text("Physiological State", font_size=50, weight="BOLD", color=WHITE)
        heading.to_edge(UP, buff=0.22)

        # Horizontal timeline with three tick marks, four equal segments
        timeline_y = 1.05
        timeline_line = Line(
            np.array([-6, timeline_y, 0]),
            np.array([6, timeline_y, 0]),
            color=WHITE,
            stroke_width=3,
        )
        ticks = VGroup(*[
            Line(
                np.array([x, 0.93, 0]),
                np.array([x, 1.17, 0]),
                color=WHITE,
                stroke_width=3,
            )
            for x in [-3, 0, 3]
        ])
        timeline = VGroup(timeline_line, ticks)

        # 0.00-0.34 heading and empty timeline fade in
        self.play(FadeIn(heading), FadeIn(timeline), run_time=max(0.05, 0.34))

        # 0.34-1.02 heading pulses softly, then returns
        self.play(
            heading.animate.set_color(YELLOW),
            rate_func=there_and_back,
            run_time=max(0.05, 0.68),
        )

        # 1.02-1.66 pause, heading and timeline hold
        self.wait(max(0.05, 0.64))

        # Four segment labels
        label_names = ["Sleep stage", "Alertness", "Fatigue", "Emotional state"]
        label_xs = [-4.5, -1.5, 1.5, 4.5]
        labels = VGroup(*[
            Text(name, font_size=24, color=WHITE).move_to(np.array([lx, 0.25, 0]))
            for name, lx in zip(label_names, label_xs)
        ])

        # 1.66-2.40 labels fade in beneath timeline
        self.play(FadeIn(labels), run_time=max(0.05, 0.74))

        # 2.40-3.44 pause, all labels hold
        self.wait(max(0.05, 1.04))

        # Translucent rounded highlight for active segment
        highlight = RoundedRectangle(
            width=2.8,
            height=0.72,
            corner_radius=0.18,
            fill_color=YELLOW,
            fill_opacity=0.22,
            stroke_color=YELLOW,
            stroke_opacity=0.55,
            stroke_width=2,
        ).move_to(np.array([-4.5, 0.42, 0]))

        # Dynamic waveform parameters
        wave_phase = ValueTracker(0.0)
        wave_amp = ValueTracker(0.70)
        wave_freq = ValueTracker(0.32)
        wave_irreg = ValueTracker(0.05)
        wave_emph = ValueTracker(0.0)
        wave_phase.add_updater(lambda m, dt: m.increment_value(0.18 * dt))
        self.add(wave_phase, wave_amp, wave_freq, wave_irreg, wave_emph)

        base_y = -1.35
        n_wave_pts = 220
        xs = np.linspace(-6, 6, n_wave_pts)

        dynamic_wave = VMobject(stroke_color=TEAL, stroke_width=3, stroke_opacity=1.0)
        dynamic_wave.set_z_index(1)

        def update_dynamic_wave(mob):
            a = wave_amp.get_value()
            f = wave_freq.get_value()
            r = wave_irreg.get_value()
            ph = wave_phase.get_value()
            emph = wave_emph.get_value()

            y = a * np.sin(2 * PI * f * (xs - ph * 0.25))
            y += (a * r) * np.sin(2 * PI * f * 2.7 * (xs + ph * 0.18) + 2.0)
            y += (a * r * 0.6) * np.sin(2 * PI * f * 3.9 * (xs - ph * 0.22) + 4.2)
            y *= 0.75

            points = [np.array([x, base_y + yv, 0]) for x, yv in zip(xs, y)]
            mob.set_points_as_corners(points)

            if emph > 0.6:
                mob.set_stroke(color=YELLOW, width=5)
            else:
                mob.set_stroke(color=TEAL, width=3 + 2.5 * emph)

        dynamic_wave.add_updater(update_dynamic_wave)
        update_dynamic_wave(dynamic_wave)

        # 3.44-3.98 highlight first segment, slow large waveform fades in
        self.play(
            FadeIn(highlight),
            FadeIn(dynamic_wave),
            run_time=max(0.05, 0.54),
        )

        # 3.98-4.44 slow large waves continue
        self.wait(max(0.05, 0.46))

        # 4.44-4.94 hold
        self.wait(max(0.05, 0.50))

        # 4.94-5.36 slide to Alertness, wave becomes faster/smaller
        self.play(
            highlight.animate.move_to(np.array([-1.5, 0.42, 0])),
            wave_amp.animate.set_value(0.22),
            wave_freq.animate.set_value(1.8),
            wave_irreg.animate.set_value(0.08),
            run_time=max(0.05, 0.42),
        )

        # 5.36-5.72 fast small oscillations continue
        self.wait(max(0.05, 0.36))

        # 5.72-6.00 slide to Fatigue, wave flattens
        self.play(
            highlight.animate.move_to(np.array([1.5, 0.42, 0])),
            wave_amp.animate.set_value(0.08),
            wave_freq.animate.set_value(0.60),
            wave_irreg.animate.set_value(0.03),
            run_time=max(0.05, 0.28),
        )

        # 6.00-6.54 flattened trace continues
        self.wait(max(0.05, 0.54))

        # 6.54-6.88 slide to Emotional state, wave becomes irregular
        self.play(
            highlight.animate.move_to(np.array([4.5, 0.42, 0])),
            wave_amp.animate.set_value(0.44),
            wave_freq.animate.set_value(0.90),
            wave_irreg.animate.set_value(0.55),
            run_time=max(0.05, 0.34),
        )

        # 6.88-7.50 irregular wave continues
        self.wait(max(0.05, 0.62))

        # 7.50-8.48 waveform visual emphasis increases gently
        self.play(wave_emph.animate.set_value(0.85), run_time=max(0.05, 0.98))

        # 8.48-9.42 emphasis holds, irregular oscillation continues
        self.wait(max(0.05, 0.94))

        # 9.42-10.16 waveform continues shifting in real time
        self.wait(max(0.05, 0.74))

        # 10.16-10.98 pause with current irregular waveform
        self.wait(max(0.05, 0.82))

        # 10.98-11.28 waveform becomes focal point, highlight dims
        self.play(
            wave_emph.animate.set_value(1.0),
            highlight.animate.set_opacity(0.30),
            run_time=max(0.05, 0.30),
        )

        # 11.28-12.32 waveform remains visual focus, highlight stays dimmed
        self.wait(max(0.05, 1.04))

        # Freeze dynamic motion, prepare static comparative display
        dynamic_wave.clear_updaters()
        wave_phase.clear_updaters()

        def section_points(start, end, mode):
            local_xs = np.linspace(0, end - start, 110)
            if mode == "sleep":
                y = 0.52 * np.sin(2 * PI * 0.5 * local_xs)
                y += 0.08 * np.sin(2 * PI * 1.1 * local_xs + 1.0)
            elif mode == "alert":
                y = 0.19 * np.sin(2 * PI * 2.0 * local_xs)
                y += 0.06 * np.sin(2 * PI * 4.1 * local_xs + 0.5)
            elif mode == "fatigue":
                y = 0.07 * np.sin(2 * PI * 0.8 * local_xs)
                y += 0.04 * np.sin(2 * PI * 1.5 * local_xs + 2.0)
            elif mode == "emotional":
                y = 0.32 * np.sin(2 * PI * 0.9 * local_xs + 0.5)
                y += 0.22 * np.sin(2 * PI * 1.7 * local_xs + 2.3)
                y += 0.10 * np.sin(2 * PI * 3.1 * local_xs + 4.0)
            return [
                np.array([x, base_y + yv, 0])
                for x, yv in zip(start + local_xs, y)
            ]

        modes = ["sleep", "alert", "fatigue", "emotional"]
        bounds = [(-6, -3), (-3, 0), (0, 3), (3, 6)]
        section_wave = VGroup()
        for (start, end), mode in zip(bounds, modes):
            sec = VMobject(stroke_color=TEAL, stroke_width=3, stroke_opacity=1.0)
            sec.set_points_as_corners(section_points(start, end, mode))
            section_wave.add(sec)
        section_wave.set_z_index(2)

        dividers = VGroup(*[
            Line(
                np.array([x, -2.6, 0]),
                np.array([x, -0.15, 0]),
                color=GREY_B,
                stroke_width=2,
            )
            for x in [-3, 0, 3]
        ])
        dividers.set_z_index(3)

        # 12.32-12.74 split into four comparative sections, highlight fades out
        self.play(
            FadeOut(dynamic_wave),
            FadeIn(dividers),
            FadeIn(section_wave),
            highlight.animate.set_opacity(0.0),
            run_time=max(0.05, 0.42),
        )

        # 12.74-13.28 four-section waveform holds
        self.wait(max(0.05, 0.54))

        # 13.28-13.96 labels pulse in sequence left to right
        for label in labels:
            self.play(
                label.animate.set_color(YELLOW),
                rate_func=there_and_back,
                run_time=max(0.05, 0.17),
            )

        # 13.96-14.74 all four waveform sections brighten in unison
        self.play(
            *[sec.animate.set_stroke(color=YELLOW, width=5) for sec in section_wave],
            rate_func=there_and_back,
            run_time=max(0.05, 0.78),
        )

        # 14.74-15.50 soft glow outlines around the four waveform sections
        glow_rects = VGroup(*[
            RoundedRectangle(
                width=2.92,
                height=2.0,
                corner_radius=0.10,
                fill_opacity=0.0,
                stroke_color=ORANGE,
                stroke_opacity=0.0,
                stroke_width=2.5,
            ).move_to(np.array([cx, base_y, 0]))
            for cx in label_xs
        ])
        self.add(glow_rects)
        self.play(
            *[rect.animate.set_stroke(opacity=0.6) for rect in glow_rects],
            run_time=max(0.05, 0.76),
        )

        # 15.50-16.24 glow holds
        self.wait(max(0.05, 0.74))

        # 16.24-16.86 one final soft pulse across all four sections
        self.play(
            *[sec.animate.set_stroke(width=5, color=YELLOW) for sec in section_wave],
            rate_func=there_and_back,
            run_time=max(0.05, 0.62),
        )

        # 16.86-17.85 final hold
        self.wait(max(0.05, 0.99))