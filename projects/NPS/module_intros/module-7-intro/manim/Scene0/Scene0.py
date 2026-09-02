ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 0.00-0.50 MODULE flies in from left
        module_text = Text("MODULE", font_size=72, weight=BOLD, color=WHITE)
        seven_text = Text("7", font_size=72, weight=BOLD, color=GOLD)
        title_group = VGroup(module_text, seven_text).arrange(RIGHT, buff=0.3)
        title_group.move_to(UP * 3.0)
        module_final = module_text.get_center()
        seven_final = seven_text.get_center()

        module_text.move_to(LEFT * 9 + UP * module_final[1])
        seven_text.set_opacity(0).move_to(RIGHT * 9 + UP * seven_final[1])

        self.play(
            module_text.animate.move_to(module_final),
            run_time=max(0.05, 0.50),
            rate_func=lambda t: 1 - (1 - t) ** 3,
        )
        self.play(
            seven_text.animate.set_opacity(1).move_to(seven_final),
            run_time=max(0.05, 0.44),
            rate_func=lambda t: 1 - (1 - t) ** 3,
        )

        # Hold title until 1.78
        self.wait(max(0.05, 0.84))

        # 1.78-2.42 Electroencephalography writes letter by letter
        subtitle = Text("Electroencephalography", font_size=42, color=WHITE)
        subtitle.next_to(title_group, DOWN, buff=0.35)
        self.play(AddTextLetterByLetter(subtitle), run_time=max(0.05, 0.64))

        # Hold until 3.40
        self.wait(max(0.05, 0.98))

        # 3.40-4.04 head outline draws itself
        head_center_y = -0.6
        head_rx, head_ry = 1.4, 1.7
        head_outline = ParametricFunction(
            lambda t: np.array([head_rx * np.cos(t), head_ry * np.sin(t) + head_center_y, 0]),
            t_range=[PI / 2, PI / 2 + 2 * PI],
            stroke_color=WHITE,
            stroke_width=3,
            fill_opacity=0,
        )
        self.play(Create(head_outline), run_time=max(0.05, 0.64))

        # Hold until 4.70
        self.wait(max(0.05, 0.66))

        # 4.70-4.88 subtle pulsing glow around head
        head_glow = (
            head_outline.copy()
            .set_stroke(color=YELLOW, width=12, opacity=0.0)
            .set_fill(opacity=0)
            .set_z_index(-1)
        )
        self.add(head_glow)
        self.play(head_glow.animate.set_stroke(opacity=0.65), run_time=max(0.05, 0.09))
        self.play(head_glow.animate.set_stroke(opacity=0.3), run_time=max(0.05, 0.09))

        # Hold until 5.12
        self.wait(max(0.05, 0.24))

        # 5.12-5.38 five electrode dots grow in
        electrode_ts = [PI / 2, 2 * PI / 3, PI / 3, 5 * PI / 6, PI / 6]
        electrode_positions = [
            np.array([head_rx * np.cos(t), head_ry * np.sin(t) + head_center_y, 0])
            for t in electrode_ts
        ]
        electrode_dots = VGroup(*[
            Dot(pos, radius=0.12, color=ORANGE, fill_opacity=1)
            for pos in electrode_positions
        ])

        per_dot = max(0.05, 0.26 / 5)
        for dot in electrode_dots:
            self.play(GrowFromCenter(dot), run_time=max(0.05, per_dot))

        # 5.38-5.92 lead lines converge into a bundle
        converge_pt = np.array([0, -3.0, 0])
        bundle_end = np.array([0, -4.0, 0])
        leads = VGroup(*[
            Line(pos, converge_pt, color=GREY_B, stroke_width=2)
            for pos in electrode_positions
        ])
        bundle = Line(converge_pt, bundle_end, color=GREY_B, stroke_width=2)
        all_leads = VGroup(*leads, bundle)
        all_leads.set_z_index(1)
        self.play(
            LaggedStart(*[Create(mob) for mob in all_leads], lag_ratio=0.12),
            run_time=max(0.05, 0.54),
        )

        # Hold until 6.24
        self.wait(max(0.05, 0.32))

        # 6.24-7.16 EEG waveform begins flowing
        base_y = -3.1
        wave_t = ValueTracker(0)
        activity = ValueTracker(1.0)
        rhythm_mix = ValueTracker(0.0)
        flat_amt = ValueTracker(0.7)

        def compute_wave_points():
            xs = np.linspace(-7, 7, 260)
            t = wave_t.get_value()
            act = activity.get_value()
            rhy = rhythm_mix.get_value()
            fa = flat_amt.get_value()

            irregular = (
                np.sin(2.2 * xs - t * 10)
                + 0.8 * np.sin(4.7 * xs + t * 15)
                + 0.6 * np.sin(7.3 * xs - t * 21)
                + 0.4 * np.sin(11.0 * xs + t * 28)
            ) / 2.8
            rhythmic = np.sin(1.2 * xs - t * 5)

            signal = (1 - rhy) * irregular + rhy * rhythmic

            left_fade = np.clip((xs + 6.5) / 3.0, 0, 1)
            right_flat = 1 - fa * np.clip((xs - 2.0) / 5.0, 0, 1)
            env = left_fade * right_flat

            y = base_y + act * 0.25 * env * signal
            return np.array([xs, y, np.zeros(len(xs))]).T

        waveform = VMobject(stroke_color=TEAL, stroke_width=3, fill_opacity=0)
        waveform.set_points_as_corners(compute_wave_points())
        waveform.set_z_index(2)
        waveform.add_updater(lambda mob: mob.set_points_as_corners(compute_wave_points()))

        self.play(
            FadeIn(waveform),
            wave_t.animate.set_value(1.0),
            run_time=max(0.05, 0.92),
        )

        # 7.16-7.58 waveform more active, electrode dots pulse
        self.play(
            activity.animate.set_value(1.6),
            wave_t.animate.set_value(wave_t.get_value() + 0.9),
            LaggedStart(
                *[Indicate(dot, color=YELLOW, scale_factor=1.25) for dot in electrode_dots],
                lag_ratio=0.1,
            ),
            run_time=max(0.05, 0.42),
        )

        # 7.58-8.38 soft glow traces between electrodes and waveform
        wave_pt = np.array([0, base_y + 0.15, 0])
        tracer_halo = Circle(
            radius=0.26,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_opacity=0.4,
            stroke_width=6,
        )
        tracer_core = Dot(radius=0.10, color=YELLOW, fill_opacity=1)
        tracer = VGroup(tracer_halo, tracer_core).move_to(electrode_dots[0].get_center())
        tracer.set_z_index(4)
        self.add(tracer)

        self.play(
            tracer.animate.move_to(wave_pt),
            wave_t.animate.set_value(wave_t.get_value() + 0.8),
            run_time=max(0.05, 0.40),
        )
        self.play(
            tracer.animate.move_to(electrode_dots[0].get_center()),
            wave_t.animate.set_value(wave_t.get_value() + 0.8),
            run_time=max(0.05, 0.40),
        )

        # Hold until 8.78
        self.wait(max(0.05, 0.40))

        # 8.78-10.20 rhythm becomes more interpretable
        self.play(
            rhythm_mix.animate.set_value(1.0),
            wave_t.animate.set_value(wave_t.get_value() + 2.8),
            run_time=max(0.05, 1.42),
        )

        # 10.20-10.70 waveform flattens toward its right edge
        self.play(
            flat_amt.animate.set_value(0.95),
            wave_t.animate.set_value(wave_t.get_value() + 1.2),
            run_time=max(0.05, 0.50),
        )

        # 10.70-11.58 slow continued flow
        self.play(
            wave_t.animate.set_value(wave_t.get_value() + 0.8),
            run_time=max(0.05, 0.88),
        )

        # 11.58-12.24 diagram fades, "Let's get started!" bursts in
        diagram_group = VGroup(
            head_outline,
            head_glow,
            electrode_dots,
            all_leads,
            waveform,
            tracer,
        )

        start_text = Text(
            "Let's get started!",
            font_size=68,
            weight=BOLD,
            color=YELLOW,
        )
        start_text.move_to(ORIGIN)
        start_text.scale(0.01).set_opacity(0)
        self.add(start_text)

        self.play(
            FadeOut(diagram_group),
            start_text.animate.scale(150).set_opacity(1).set_color(WHITE),
            run_time=max(0.05, 0.32),
        )
        self.play(
            start_text.animate.scale(1 / 1.5).set_color(YELLOW),
            run_time=max(0.05, 0.34),
        )

        # 12.24-13.00 gentle pulsing bounce
        self.play(start_text.animate.scale(1.06), run_time=max(0.05, 0.38))
        self.play(start_text.animate.scale(1 / 1.06), run_time=max(0.05, 0.38))