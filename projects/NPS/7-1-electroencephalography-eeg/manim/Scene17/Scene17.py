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
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene17(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_trace(signal, width=6.0, height=0.8, color=YELLOW, stroke_width=3.0, num_points=700):
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            u = np.linspace(-1, 1, num_points)
            x = u * width / 2.0
            y = signal(u) * height / 2.0
            y = np.clip(y, -height, height)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        def normal_eeg_signal(u):
            return (
                0.14 * np.sin(2 * np.pi * 8 * u)
                + 0.09 * np.sin(2 * np.pi * 15 * u)
                + 0.05 * np.sin(2 * np.pi * 25 * u)
            )

        def epilepsy_spike_signal(u):
            y = 0.18 * np.sin(2 * np.pi * 2.2 * u) + 0.07 * np.sin(2 * np.pi * 6.0 * u)
            for u0, amp, w in [(-0.55, 2.0, 0.030), (0.05, 2.3, 0.026), (0.65, 1.9, 0.032)]:
                y += amp * np.exp(-((u - u0) / w) ** 2)
                y += 0.22 * np.sin(2 * np.pi * 32 * u) * np.exp(-((u - u0) / 0.1) ** 2)
            return y

        # ---------- beat 1: title (0.00 - 2.40) ----------
        epilepsy_title = Text("Epilepsy", font_size=80, weight="BOLD", color=ORANGE)
        epilepsy_title.move_to(UP * 2.2)
        self.play(FadeIn(epilepsy_title), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.2))

        # ---------- beat 2: title shift + world map (2.40 - 3.22) ----------
        def make_world_map_shapes():
            polygons = [
                [(-4.2, 2.4), (-2.8, 2.8), (-1.5, 2.7), (-0.5, 2.2), (-1.0, 1.2),
                 (-1.8, 0.6), (-2.5, 0.2), (-3.0, -0.4), (-4.3, 0.5), (-4.6, 1.6), (-4.2, 2.4)],
                [(-2.9, -0.2), (-2.0, 0.0), (-1.7, -0.8), (-2.2, -1.8), (-3.3, -2.5),
                 (-4.0, -1.8), (-3.8, -1.0), (-3.4, -0.5)],
                [(-0.6, 2.0), (0.3, 2.5), (1.2, 2.3), (1.0, 1.6), (0.4, 1.3),
                 (0.0, 1.2), (-0.1, 1.6)],
                [(-0.5, 1.0), (0.6, 1.3), (1.5, 0.8), (1.8, -0.2), (1.3, -1.5),
                 (0.5, -2.2), (-0.3, -2.5), (-0.8, -1.8), (-0.7, -0.8), (-0.6, 0.2), (-0.5, 1.0)],
                [(1.2, 2.2), (2.0, 2.8), (3.8, 3.2), (5.2, 2.6), (6.0, 1.8),
                 (5.8, 1.0), (5.0, 0.4), (4.0, -0.2), (3.0, 0.0), (2.2, 0.8),
                 (1.8, 1.4), (1.2, 2.2)],
                [(4.6, -2.8), (5.4, -2.4), (5.6, -1.9), (5.0, -1.6), (4.3, -2.0), (4.2, -2.6)],
            ]
            shapes = []
            for pts in polygons:
                poly = Polygon(
                    *[np.array([x, y, 0.0]) for x, y in pts],
                    stroke_color=GREY_B,
                    stroke_width=1.2,
                    fill_color=GREY_B,
                    fill_opacity=0.08,
                )
                shapes.append(poly)
            return VGroup(*shapes)

        map_shapes = make_world_map_shapes()

        rng_dots = np.random.default_rng(7)
        regions = [
            (-4.2, -2.5, 1.5, 2.8, 20),  # North America
            (-3.0, -1.8, 0.2, 1.5, 12),   # Central America
            (-3.2, -1.8, -2.4, -0.3, 18), # South America
            (-0.4, 1.2, 1.4, 2.4, 18),    # Europe
            (-0.5, 1.3, -2.3, 0.9, 35),   # Africa
            (1.5, 5.0, 0.8, 3.1, 55),     # Asia
            (4.3, 5.5, -2.6, -1.7, 12),   # Oceania
        ]
        dot_mobjects = []
        for x_min, x_max, y_min, y_max, count in regions:
            for _ in range(count):
                x = rng_dots.uniform(x_min, x_max)
                y = rng_dots.uniform(y_min, y_max)
                dot = Circle(
                    radius=0.035,
                    fill_color=ORANGE,
                    fill_opacity=0.0,
                    stroke_width=0,
                ).move_to(np.array([x, y, 0.0]))
                dot_mobjects.append(dot)

        world_map = VGroup(map_shapes, *dot_mobjects)
        world_map.scale_to_fit_height(4.8).move_to(DOWN * 0.1)

        self.play(
            epilepsy_title.animate.shift(UP * 0.5),
            FadeIn(world_map),
            run_time=max(0.05, 0.82),
        )

        # gap 3.22 - 3.70
        self.wait(max(0.05, 0.48))

        # ---------- beat 3: dots in waves + caption (3.70 - 5.60) ----------
        wave1 = dot_mobjects[0::3]
        wave2 = dot_mobjects[1::3]
        wave3 = dot_mobjects[2::3]

        self.play(
            LaggedStart(*[FadeIn(dot) for dot in wave1], lag_ratio=0.012, run_time=max(0.05, 0.62))
        )
        self.play(
            LaggedStart(*[FadeIn(dot) for dot in wave2], lag_ratio=0.012, run_time=max(0.05, 0.58))
        )
        self.play(
            LaggedStart(*[FadeIn(dot) for dot in wave3], lag_ratio=0.012, run_time=max(0.05, 0.45))
        )

        millions_caption = Text(
            "Millions affected worldwide.",
            font_size=26,
            color=GREY_B,
        ).next_to(world_map, DOWN, buff=0.4)
        self.play(FadeIn(millions_caption), run_time=max(0.05, 0.25))

        # ---------- beat 4: pulse + fade down/left (5.60 - 6.66) ----------
        self.play(world_map.animate.scale(1.04), run_time=max(0.05, 0.28))
        self.play(world_map.animate.scale(1 / 1.04), run_time=max(0.05, 0.28))
        self.play(
            world_map.animate.shift(DOWN * 1.0 + LEFT * 2.0).set_opacity(0.3),
            millions_caption.animate.shift(DOWN * 1.0 + LEFT * 2.0).set_opacity(0.3),
            run_time=max(0.05, 0.50),
        )

        # ---------- beat 5: brain illustration (6.66 - 8.50) ----------
        brain_svg = SVGMobject(ASSET_PATHS["brain"])
        brain_svg.set_stroke(GREY_B, width=2).set_fill(GREY_B, opacity=0.22)
        brain_svg.rotate(PI, axis=UP)  # face left
        brain_svg.scale_to_fit_height(3.0)
        brain_svg.move_to(RIGHT * 3.3 + DOWN * 0.5)

        brain_label_recurrent = Text(
            "Recurrent seizures", font_size=26, color=ORANGE
        ).next_to(brain_svg, DOWN, buff=0.3)

        self.play(
            FadeIn(brain_svg),
            run_time=max(0.05, 1.0),
        )
        self.play(
            GrowFromCenter(brain_label_recurrent),
            run_time=max(0.05, 0.84),
        )

        # ---------- beat 6: scattered abnormal pulses + label change (8.50 - 10.26) ----------
        # compute brain bounds without get_bounding_box
        x_min = brain_svg.get_left()[0]
        x_max = brain_svg.get_right()[0]
        y_min = brain_svg.get_bottom()[1]
        y_max = brain_svg.get_top()[1]
        rng_pulse = np.random.default_rng(42)

        pulse_dots = VGroup()
        for _ in range(6):
            px = rng_pulse.uniform(x_min + 0.15, x_max - 0.15)
            py = rng_pulse.uniform(y_min + 0.15, y_max - 0.15)
            pulse_dots.add(
                Circle(
                    radius=0.07,
                    fill_color=RED,
                    fill_opacity=0.9,
                    stroke_width=0,
                ).move_to(np.array([px, py, 0.0])).set_opacity(0.0)
            )

        self.play(
            LaggedStart(
                *[p.animate.set_opacity(0.85) for p in pulse_dots],
                lag_ratio=0.18,
                run_time=max(0.05, 0.55),
            )
        )
        self.play(
            *[p.animate.set_opacity(0.25) for p in pulse_dots],
            run_time=max(0.05, 0.25),
        )
        self.play(
            *[p.animate.set_opacity(0.9) for p in pulse_dots],
            run_time=max(0.05, 0.25),
        )

        brain_label_abnormal = Text(
            "Abnormal activity", font_size=26, color=RED
        ).next_to(brain_svg, DOWN, buff=0.3)

        self.play(
            FadeOut(brain_label_recurrent),
            FadeIn(brain_label_abnormal),
            run_time=max(0.05, 0.46),
        )
        self.wait(max(0.05, 0.25))

        # gap 10.26 - 10.86
        self.wait(max(0.05, 0.60))

        # ---------- beat 7: pulses multiply/densify (10.86 - 12.00) ----------
        excess_pulses = VGroup()
        for _ in range(10):
            px = rng_pulse.uniform(x_min + 0.15, x_max - 0.15)
            py = rng_pulse.uniform(y_min + 0.15, y_max - 0.15)
            excess_pulses.add(
                Circle(
                    radius=0.07,
                    fill_color=RED,
                    fill_opacity=0.9,
                    stroke_width=0,
                ).move_to(np.array([px, py, 0.0])).set_opacity(0.0)
            )

        self.play(
            LaggedStart(
                *[p.animate.set_opacity(1.0) for p in excess_pulses],
                lag_ratio=0.04,
                run_time=max(0.05, 0.35),
            ),
            pulse_dots.animate.set_opacity(1.0),
        )
        self.play(
            pulse_dots.animate.set_opacity(1.0),
            excess_pulses.animate.set_opacity(1.0),
            run_time=max(0.05, 0.20),
        )
        self.play(
            pulse_dots.animate.set_opacity(0.3),
            excess_pulses.animate.set_opacity(0.3),
            run_time=max(0.05, 0.12),
        )
        self.play(
            pulse_dots.animate.set_opacity(1.0),
            excess_pulses.animate.set_opacity(1.0),
            run_time=max(0.05, 0.12),
        )

        brain_label_excess = Text(
            "Excessive firing", font_size=26, color=RED
        ).next_to(brain_svg, DOWN, buff=0.3)
        self.play(
            FadeOut(brain_label_abnormal),
            FadeIn(brain_label_excess),
            run_time=max(0.05, 0.35),
        )

        # ---------- beat 8: synchronize into unified ripple (12.00 - 14.16) ----------
        sync_line = Line(
            brain_svg.get_bottom(),
            brain_svg.get_top(),
            color=RED,
            stroke_width=7,
        ).set_opacity(0.75).move_to(brain_svg.get_left())

        sync_caption = Text(
            "Synchronous electrical activity.",
            font_size=22,
            color=WHITE,
        ).next_to(brain_svg, DOWN, buff=0.3)

        self.play(
            FadeOut(brain_label_excess),
            pulse_dots.animate.set_opacity(0.05),
            excess_pulses.animate.set_opacity(0.05),
            run_time=max(0.05, 0.30),
        )
        self.play(
            sync_line.animate.move_to(brain_svg.get_right()),
            run_time=max(0.05, 1.20),
            rate_func=linear,
        )
        self.play(FadeIn(sync_caption), run_time=max(0.05, 0.56))
        self.wait(max(0.05, 0.10))

        # gap 14.16 - 15.22
        self.wait(max(0.05, 1.06))

        # ---------- beat 9: brain becomes inset, EEG appears (15.22 - 17.54) ----------
        brain_inset_group = VGroup(brain_svg, pulse_dots, excess_pulses)

        self.play(
            FadeOut(sync_caption),
            FadeOut(sync_line),
            brain_inset_group.animate.scale(0.4).move_to(RIGHT * 5.3 + UP * 2.4).set_opacity(0.85),
            run_time=max(0.05, 0.90),
        )

        eeg_pos = LEFT * 2.0 + UP * 0.35
        flat_line = Line(
            eeg_pos + LEFT * 4.0,
            eeg_pos + RIGHT * 4.0,
            color=YELLOW,
            stroke_width=3,
        )
        self.play(Create(flat_line), run_time=max(0.05, 0.40))

        eeg_trace = make_trace(
            normal_eeg_signal,
            width=10.0,
            height=0.7,
            color=YELLOW,
            stroke_width=3,
        ).move_to(eeg_pos)

        self.play(ReplacementTransform(flat_line, eeg_trace), run_time=max(0.05, 0.60))

        eeg_label = Text(
            "EEG — direct recording", font_size=22, color=WHITE
        ).next_to(eeg_trace, DOWN, buff=0.4)
        self.play(FadeIn(eeg_label), run_time=max(0.05, 0.32))
        self.wait(max(0.05, 0.10))

        # ---------- beat 10: temporal resolution sweep (17.54 - 20.84) ----------
        ticks_marker = VGroup(*[
            Line(UP * 0.12, DOWN * 0.12, color=GREY_B, stroke_width=1.5)
            .move_to(eeg_trace.get_bottom() + DOWN * 0.25 + RIGHT * x)
            for x in [-4, -2, 0, 2, 4]
        ])
        sweep_line = Line(
            eeg_trace.get_bottom(),
            eeg_trace.get_top(),
            color=WHITE,
            stroke_width=2,
        ).move_to(eeg_trace.get_left())

        high_res_label = Text(
            "High temporal resolution", font_size=22, color=WHITE
        ).next_to(eeg_trace, DOWN, buff=0.4)

        self.play(Create(ticks_marker), run_time=max(0.05, 0.30))
        self.play(
            sweep_line.animate.move_to(eeg_trace.get_right()),
            eeg_trace.animate.shift(LEFT * 0.3),
            run_time=max(0.05, 2.40),
            rate_func=linear,
        )
        self.play(
            FadeOut(eeg_label),
            FadeIn(high_res_label),
            FadeOut(sweep_line),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.10))

        # gap 20.84 - 21.50
        self.wait(max(0.05, 0.66))

        # ---------- beat 11: EEG grows, title glows, brain inset pulses (21.50 - 25.56) ----------
        self.play(
            FadeOut(high_res_label),
            run_time=max(0.05, 0.30),
        )
        self.play(
            Indicate(epilepsy_title, scale_factor=1.08, color=ORANGE),
            run_time=max(0.05, 0.80),
        )
        self.play(eeg_trace.animate.scale(1.12), run_time=max(0.05, 1.00))

        subtitle_primary = Text(
            "Primary tool for epilepsy evaluation",
            font_size=20,
            color=WHITE,
        ).next_to(eeg_trace, DOWN, buff=0.7)
        self.play(FadeIn(subtitle_primary), run_time=max(0.05, 0.80))

        self.play(brain_inset_group.animate.scale(1.06), run_time=max(0.05, 0.40))
        self.play(brain_inset_group.animate.scale(1 / 1.06), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.36))

        # gap 25.56 - 26.56
        self.wait(max(0.05, 1.00))

        # ---------- beat 12: abnormal spike-wave trace (26.56 - 29.88) ----------
        spike_trace = make_trace(
            epilepsy_spike_signal,
            width=10.0,
            height=1.15,
            color=YELLOW,
            stroke_width=4,
        ).move_to(eeg_trace.get_center())

        self.play(Transform(eeg_trace, spike_trace), run_time=max(0.05, 0.90))

        peak_pos = eeg_trace.get_center() + np.array([0.25, 0.8, 0.0])
        spike_glow_dot = Circle(
            radius=0.12,
            fill_color=RED,
            fill_opacity=0.85,
            stroke_width=0,
        ).move_to(peak_pos)
        self.play(FadeIn(spike_glow_dot), run_time=max(0.05, 0.30))

        for _ in range(3):
            self.play(brain_inset_group.animate.scale(1.06), run_time=max(0.05, 0.17))
            self.play(brain_inset_group.animate.scale(1 / 1.06), run_time=max(0.05, 0.17))

        detecting_label = Text(
            "Detecting abnormal activity", font_size=20, color=WHITE
        ).next_to(eeg_trace, DOWN, buff=0.7)
        self.play(
            FadeOut(subtitle_primary),
            FadeIn(detecting_label),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.70))

        # gap 29.88 - 31.00
        self.wait(max(0.05, 1.12))

        # ---------- beat 13: first application panel (31.00 - 34.34) ----------
        panel_positions = [
            np.array([-3.0, -1.5, 0.0]),  # top-left
            np.array([3.0, -1.5, 0.0]),   # top-right
            np.array([-3.0, -2.7, 0.0]),  # bottom-left
            np.array([3.0, -2.7, 0.0]),   # bottom-right
        ]

        def make_panel(label_text, content_mob, accent=BLUE):
            rect = RoundedRectangle(
                width=2.8,
                height=0.95,
                corner_radius=0.1,
                fill_color=BLACK,
                fill_opacity=0.6,
                stroke_color=accent,
                stroke_width=2,
            )
            label = Text(label_text, font_size=14, color=WHITE)
            content = VGroup(label, content_mob).arrange(DOWN, buff=0.08)
            content.scale_to_fit_width(2.4)
            content.move_to(rect.get_center())
            return VGroup(rect, content)

        mini_spike_panel = make_trace(
            epilepsy_spike_signal, width=1.3, height=0.35, color=YELLOW, stroke_width=2
        )
        panel1 = make_panel(
            "Seizure Type Identification", mini_spike_panel, accent=ORANGE
        )
        panel1.move_to(panel_positions[0])

        self.play(GrowFromCenter(panel1), run_time=max(0.05, 0.70))
        self.play(
            panel1.animate.scale(1.05),
            run_time=max(0.05, 0.80),
        )
        self.play(
            panel1.animate.scale(1 / 1.05),
            run_time=max(0.05, 0.60),
        )
        self.wait(max(0.05, 1.24))

        # gap 34.34 - 34.96
        self.wait(max(0.05, 0.62))

        # ---------- beat 14: second application panel (34.96 - 37.06) ----------
        mini_brain2 = SVGMobject(ASSET_PATHS["brain"])
        mini_brain2.set_color(GREY_B).set_fill(GREY_B, opacity=0.25)
        mini_brain2.scale_to_fit_height(0.5)
        focus_region2 = Circle(
            radius=0.07,
            fill_color=RED,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(mini_brain2.get_center() + LEFT * 0.2 + UP * 0.1)
        panel2_content = VGroup(mini_brain2, focus_region2)
        panel2 = make_panel(
            "Brain Region Localisation", panel2_content, accent=RED
        )
        panel2.move_to(panel_positions[1])

        self.play(GrowFromCenter(panel2), run_time=max(0.05, 0.70))
        self.play(Indicate(panel2, color=RED, scale_factor=1.05), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.90))

        # gap 37.06 - 37.66
        self.wait(max(0.05, 0.60))

        # ---------- beat 15: third application panel (37.66 - 38.48) ----------
        descending_line = Line(
            LEFT * 0.6 + UP * 0.15,
            RIGHT * 0.6 + DOWN * 0.15,
            color=GREEN,
            stroke_width=3,
        )
        check_mark3 = Text("✓", font_size=16, color=GREEN).next_to(
            descending_line, RIGHT, buff=0.1
        )
        treatment_chart = VGroup(descending_line, check_mark3)
        panel3 = make_panel(
            "Treatment Monitoring", treatment_chart, accent=GREEN
        )
        panel3.move_to(panel_positions[2])

        self.play(GrowFromCenter(panel3), run_time=max(0.05, 0.50))
        self.play(Indicate(panel3, color=GREEN, scale_factor=1.08), run_time=max(0.05, 0.32))

        # gap 38.48 - 39.02
        self.wait(max(0.05, 0.54))

        # ---------- beat 16: fourth application panel (39.02 - 40.48) ----------
        mini_brain4 = SVGMobject(ASSET_PATHS["brain"])
        mini_brain4.set_color(GREY_B).set_fill(GREY_B, opacity=0.25)
        mini_brain4.scale_to_fit_height(0.5)
        crosshair_h = Line(
            mini_brain4.get_left() + RIGHT * 0.2,
            mini_brain4.get_right() + LEFT * 0.2,
            color=BLUE,
            stroke_width=2,
        )
        crosshair_v = Line(
            mini_brain4.get_bottom() + UP * 0.2,
            mini_brain4.get_top() + DOWN * 0.2,
            color=BLUE,
            stroke_width=2,
        )
        target_icon4 = VGroup(mini_brain4, crosshair_h, crosshair_v)
        panel4 = make_panel(
            "Surgical Planning", target_icon4, accent=BLUE
        )
        panel4.move_to(panel_positions[3])

        self.play(GrowFromCenter(panel4), run_time=max(0.05, 0.60))
        self.play(Indicate(panel4, color=BLUE, scale_factor=1.08), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.36))

        # ---------- beat 17: final hold (40.48 - 41.23) ----------
        self.wait(max(0.05, 0.75))