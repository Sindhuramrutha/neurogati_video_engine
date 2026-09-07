ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        rng = np.random.default_rng(5)

        # ---------- helpers ----------
        def v2(x, y):
            return np.array([x, y, 0.0])

        def make_neuron(center, color=BLUE, radius=0.20, fill_opacity=0.55,
                        stroke_color=GREY_B):
            soma = Circle(
                radius=radius,
                fill_color=color,
                fill_opacity=fill_opacity,
                stroke_color=stroke_color,
                stroke_width=1.5,
            ).move_to(center)

            dirs = [
                v2(1.0, 0.8),
                v2(0.2, -1.0),
                v2(-0.9, 0.4),
                v2(-0.4, -0.8),
            ]
            dendrites = VGroup()
            for d in dirs:
                d = d / np.linalg.norm(d)
                dendrites.add(
                    Line(
                        center + d * radius,
                        center + d * (radius + 0.22),
                        color=stroke_color,
                        stroke_width=2.2,
                    )
                )
            return VGroup(soma, dendrites)

        def get_synapse_info(neuron, rng):
            dendrites = neuron[1]
            idx = int(rng.integers(0, len(dendrites.submobjects)))
            dendrite = dendrites.submobjects[idx]
            start = dendrite.get_start()
            end = dendrite.get_end()
            direction = end - start
            norm = np.linalg.norm(direction)
            if norm == 0:
                direction = v2(1.0, 0.0)
            else:
                direction = direction / norm
            synapse_pos = end
            outside_pos = end + direction * 0.22
            return synapse_pos, outside_pos, direction

        # ---------- electrode tip ----------
        electrode_center = v2(0.0, 1.0)
        shaft = Line(
            electrode_center + LEFT * 0.8,
            electrode_center + LEFT * 0.25,
            color=GREY_B,
            stroke_width=5,
        )
        tip_triangle = Polygon(
            electrode_center + UP * 0.11,
            electrode_center + DOWN * 0.11,
            electrode_center + RIGHT * 0.28,
            color=GREY_B,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        )
        electrode_group = VGroup(shaft, tip_triangle)
        tip_point = electrode_center + RIGHT * 0.28

        # ---------- dense surrounding neuron cluster ----------
        neuron_list = []
        inner_r, outer_r = 1.05, 1.75
        inner_angles = np.linspace(0, 2 * np.pi, 8, endpoint=False) + 0.35
        outer_angles = np.linspace(0, 2 * np.pi, 10, endpoint=False) + 0.10

        for a in inner_angles:
            pos = electrode_center + v2(inner_r * np.cos(a), inner_r * np.sin(a))
            neuron_list.append(make_neuron(pos, color=BLUE, fill_opacity=0.55))

        for a in outer_angles:
            pos = electrode_center + v2(outer_r * np.cos(a), outer_r * np.sin(a))
            neuron_list.append(make_neuron(pos, color=BLUE, fill_opacity=0.55))

        neuron_cluster = VGroup(*neuron_list)

        # ---------- 1. [0.00-2.46] ----------
        self.play(FadeIn(electrode_group), run_time=max(0.05, 0.78))
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in neuron_list], lag_ratio=0.08),
            run_time=max(0.05, 1.68),
        )
        self.wait(max(0.05, 0.36))  # gap to 2.82

        # ---------- 2. [2.82-5.08] ----------
        lfp_title = Text(
            "local field potential (LFP)", font_size=46, color=WHITE
        ).to_edge(UP, buff=0.25)
        cluster_outline = SurroundingRectangle(
            neuron_cluster,
            color=BLUE,
            stroke_width=2.5,
            buff=0.35,
            fill_color=BLUE,
            fill_opacity=0.05,
            corner_radius=0.2,
        )
        self.play(FadeIn(lfp_title), run_time=max(0.05, 0.9))
        self.play(FadeIn(cluster_outline), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.76))
        self.wait(max(0.05, 0.48))  # gap to 5.56

        # ---------- 3. [5.56-11.78] ----------
        self.wait(max(0.05, 0.38))

        selected_indices = [1, 4, 7, 10, 13, 16]
        selected_neurons_initial = [neuron_list[i] for i in selected_indices]
        initial_arrows = VGroup()
        initial_lines = VGroup()

        for n in selected_neurons_initial:
            synapse_pos, outside_pos, _ = get_synapse_info(n, rng)
            arrow = Arrow(
                outside_pos,
                synapse_pos,
                color=BLUE,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.35,
                buff=0.0,
            ).set_opacity(0)
            line = Line(
                synapse_pos,
                tip_point,
                color=BLUE,
                stroke_width=1.5,
                stroke_opacity=0.30,
            )
            initial_arrows.add(arrow)
            initial_lines.add(line)

        initial_current_group = VGroup(*initial_arrows, *initial_lines)

        self.play(
            LaggedStart(*[FadeIn(a) for a in initial_arrows], lag_ratio=0.25),
            run_time=max(0.05, 0.72),
        )
        self.play(*[a.animate.set_opacity(0.35) for a in initial_arrows], run_time=max(0.05, 0.40))
        self.play(*[a.animate.set_opacity(0.90) for a in initial_arrows], run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.21))

        self.play(
            LaggedStart(*[Create(line) for line in initial_lines], lag_ratio=0.25),
            run_time=max(0.05, 1.80),
        )
        self.wait(max(0.05, 1.52))

        recording_label = Text(
            "recording electrode", font_size=24, color=GREY_B
        ).next_to(electrode_group, DOWN, buff=0.25)
        self.play(FadeIn(recording_label), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.34))
        self.wait(max(0.05, 0.80))  # gap to 12.58

        # ---------- 4. [12.58-16.68] ----------
        glow = Circle(
            radius=0.35,
            color=BLUE,
            fill_opacity=0.25,
            stroke_width=0,
        ).move_to(tip_point)
        self.play(FadeIn(glow), run_time=max(0.05, 0.50))

        single_neuron = min(neuron_list, key=lambda n: n.get_center()[0])
        single_outline = SurroundingRectangle(
            single_neuron,
            color=YELLOW,
            stroke_width=3,
            buff=0.18,
            fill_opacity=0,
        )
        self.play(GrowFromCenter(single_outline), run_time=max(0.05, 0.45))

        cross = VGroup(
            Line(
                single_neuron.get_center() + UP * 0.10 + LEFT * 0.10,
                single_neuron.get_center() + DOWN * 0.10 + RIGHT * 0.10,
                color=RED,
                stroke_width=4,
            ),
            Line(
                single_neuron.get_center() + UP * 0.10 + RIGHT * 0.10,
                single_neuron.get_center() + DOWN * 0.10 + LEFT * 0.10,
                color=RED,
                stroke_width=4,
            ),
        )
        self.play(FadeIn(cross), run_time=max(0.05, 0.35))
        self.play(Indicate(single_neuron, color=RED, scale_factor=1.2), run_time=max(0.05, 0.50))
        self.play(FadeOut(single_outline), FadeOut(cross), run_time=max(0.05, 0.40))
        self.play(
            cluster_outline.animate.set_stroke(YELLOW, width=4).set_fill(YELLOW, opacity=0.06),
            Indicate(neuron_cluster, color=YELLOW, scale_factor=1.03),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 1.10))
        self.wait(max(0.05, 0.66))  # gap to 17.34

        # ---------- 5. [17.34-23.58] ----------
        self.play(FadeOut(initial_current_group), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.16))

        beat5_indices = [2, 5, 8, 11, 14, 17, 3]
        beat5_neurons = [neuron_list[i] for i in beat5_indices]
        beat5_arrows = VGroup()
        beat5_lines = VGroup()

        for n in beat5_neurons:
            synapse_pos, outside_pos, _ = get_synapse_info(n, rng)
            arrow = Arrow(
                outside_pos,
                synapse_pos,
                color=BLUE,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.30,
                buff=0.0,
            ).set_opacity(0)
            line = Line(
                synapse_pos,
                tip_point,
                color=BLUE,
                stroke_width=2,
                stroke_opacity=0.25,
            )
            beat5_arrows.add(arrow)
            beat5_lines.add(line)

        beat5_activity_group = VGroup(*beat5_arrows, *beat5_lines)

        lfp_wave_low = ParametricFunction(
            lambda t: np.array([
                -5.2 + t * 10.4,
                -2.1 + 0.35 * np.sin(2 * np.pi * 0.8 * t),
                0,
            ]),
            t_range=[0, 1, 0.01],
            color=BLUE,
            stroke_width=3,
        )
        lfp_wave = lfp_wave_low

        self.play(
            Create(lfp_wave_low),
            LaggedStart(
                *[Indicate(n, color=YELLOW, scale_factor=1.15) for n in beat5_neurons],
                lag_ratio=0.60,
            ),
            LaggedStart(*[FadeIn(a) for a in beat5_arrows], lag_ratio=0.60),
            LaggedStart(*[FadeIn(line) for line in beat5_lines], lag_ratio=0.60),
            run_time=max(0.05, 4.80),
        )

        measured_signal_label = Text(
            "measured signal", font_size=24, color=GREY_B
        ).next_to(lfp_wave, UP, buff=0.25)
        self.play(FadeIn(measured_signal_label), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.38))
        self.wait(max(0.05, 0.66))  # gap to 24.24

        # ---------- 6. [24.24-28.08] ----------
        lfp_label_wave = Text("LFP", font_size=44, color=YELLOW).next_to(
            lfp_wave, UP, buff=0.45
        )
        lfp_wave_big = ParametricFunction(
            lambda t: np.array([
                -5.2 + t * 10.4,
                -2.1 + 0.75 * np.sin(2 * np.pi * 1.2 * t)
                + 0.15 * np.sin(2 * np.pi * 2.4 * t),
                0,
            ]),
            t_range=[0, 1, 0.01],
            color=BLUE,
            stroke_width=3.5,
        )
        slower_collective_note = Text(
            "slower, collective", font_size=28, color=PURPLE
        ).next_to(lfp_wave, DOWN, buff=0.35)

        self.play(
            FadeOut(beat5_activity_group),
            FadeOut(measured_signal_label),
            FadeIn(lfp_label_wave),
            run_time=max(0.05, 0.50),
        )
        self.play(Transform(lfp_wave, lfp_wave_big), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.06))
        self.play(FadeIn(slower_collective_note), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.62))
        self.play(FadeOut(slower_collective_note), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.96))
        self.wait(max(0.05, 1.12))  # gap to 29.20

        # ---------- 7. [29.20-34.64] ----------
        zoom_center_target = v2(0.2, 1.2)
        zoom_neurons = sorted(
            neuron_list,
            key=lambda n: np.linalg.norm(n.get_center() - zoom_center_target),
        )[:4]
        zoom_center = VGroup(*zoom_neurons).get_center()

        self.play(
            self.camera.frame.animate.scale(0.45).move_to(zoom_center),
            run_time=max(0.05, 1.40),
        )

        synapse_current_pairs = VGroup()
        for n in zoom_neurons:
            synapse_pos, outside_pos, _ = get_synapse_info(n, rng)
            arrow = Arrow(
                outside_pos,
                synapse_pos,
                color=BLUE,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.35,
                buff=0.0,
            )
            return_path = DashedLine(
                synapse_pos,
                n.get_center(),
                color=BLUE,
                stroke_width=1.5,
                dash_length=0.06,
            ).set_opacity(0.35)
            pair = VGroup(arrow, return_path)
            synapse_current_pairs.add(pair)

        self.play(
            LaggedStart(*[FadeIn(p) for p in synapse_current_pairs], lag_ratio=0.25),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.04))

        synaptic_transmembrane_label = Text(
            "synaptic & transmembrane currents", font_size=30, color=TEAL
        ).scale_to_fit_width(5.8)
        synaptic_transmembrane_label.move_to(
            v2(zoom_center[0], zoom_center[1] + 1.40)
        )
        self.play(FadeIn(synaptic_transmembrane_label), run_time=max(0.05, 0.50))

        self.play(*[p.animate.set_opacity(0.40) for p in synapse_current_pairs], run_time=max(0.05, 0.50))
        self.play(*[p.animate.set_opacity(0.90) for p in synapse_current_pairs], run_time=max(0.05, 0.50))
        self.play(*[p.animate.set_opacity(0.40) for p in synapse_current_pairs], run_time=max(0.05, 0.50))
        self.play(*[p.animate.set_opacity(0.90) for p in synapse_current_pairs], run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.80))
        self.wait(max(0.05, 0.68))  # gap to 35.32

        # ---------- 8. [35.32-41.12] ----------
        pulse_neuron = zoom_neurons[0]
        pulse_synapse, pulse_outside, pulse_dir = get_synapse_info(pulse_neuron, rng)
        pulse_dot = Dot(pulse_synapse, radius=0.06, color=YELLOW, fill_opacity=1)

        fan_dirs = [
            v2(0.0, 1.0),
            v2(0.7, 0.7),
            v2(1.0, 0.0),
            v2(0.7, -0.7),
            v2(0.0, -1.0),
        ]
        fan_arrows = VGroup()
        for d in fan_dirs:
            d = d / np.linalg.norm(d)
            fan_arrows.add(
                Arrow(
                    pulse_synapse,
                    pulse_synapse + d * 0.80,
                    color=BLUE,
                    stroke_width=1.8,
                    max_tip_length_to_length_ratio=0.30,
                    buff=0.0,
                ).set_opacity(0)
            )

        currents_flow_label = Text(
            "currents flow across membranes and through tissue",
            font_size=28,
            color=TEAL,
        ).scale_to_fit_width(6.0)
        currents_flow_label.move_to(
            v2(zoom_center[0], zoom_center[1] + 1.40)
        )

        self.play(
            FadeOut(synaptic_transmembrane_label),
            LaggedStart(*[FadeIn(a) for a in fan_arrows], lag_ratio=0.10),
            run_time=max(0.05, 0.60),
        )
        self.play(
            pulse_dot.animate.move_to(pulse_neuron.get_center()),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.72))
        self.play(FadeIn(currents_flow_label), run_time=max(0.05, 0.70))
        self.play(fan_arrows.animate.set_opacity(0.40), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 1.98))
        self.wait(max(0.05, 0.96))  # gap to 42.08

        # ---------- 9. [42.08-46.14] ----------
        self.play(
            FadeOut(synapse_current_pairs),
            FadeOut(fan_arrows),
            FadeOut(currents_flow_label),
            FadeOut(pulse_dot),
            run_time=max(0.05, 0.70),
        )

        visible_bottom_y = zoom_center[1] - 1.50
        visible_center_x = zoom_center[0]

        baseline_zoom = Line(
            v2(visible_center_x - 2.6, visible_bottom_y),
            v2(visible_center_x + 2.6, visible_bottom_y),
            color=GREY_A,
            stroke_width=2,
        )
        tiny_deflection = ParametricFunction(
            lambda t: np.array([
                visible_center_x - 0.4 + t * 0.8,
                visible_bottom_y
                + 0.08 * np.exp(-((t - 0.5) ** 2) / (2 * 0.08 ** 2)),
                0,
            ]),
            t_range=[0, 1, 0.02],
            color=YELLOW,
            stroke_width=2.5,
        )
        single_event_arrow = Arrow(
            pulse_outside,
            pulse_synapse,
            color=YELLOW,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.35,
            buff=0.0,
        )
        single_event_line = Line(
            pulse_synapse,
            tip_point,
            color=YELLOW,
            stroke_width=1.5,
            stroke_opacity=0.40,
        )

        self.play(
            Create(baseline_zoom),
            Create(tiny_deflection),
            FadeIn(single_event_arrow),
            Create(single_event_line),
            run_time=max(0.05, 1.20),
        )

        tiny_bracket = Brace(tiny_deflection, direction=DOWN, color=YELLOW)
        tiny_bracket_label = Text(
            "single synaptic event", font_size=20, color=YELLOW
        ).next_to(tiny_bracket, DOWN, buff=0.08)
        single_event_tag = VGroup(tiny_bracket, tiny_bracket_label)
        self.play(FadeIn(single_event_tag), run_time=max(0.05, 0.50))

        tiny_caption = Text(
            "very small electrical signal", font_size=22, color=GREY_B
        ).next_to(single_event_tag, DOWN, buff=0.15)
        self.play(FadeIn(tiny_caption), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.16))

        single_event_visuals = VGroup(
            baseline_zoom,
            tiny_deflection,
            single_event_arrow,
            single_event_line,
            tiny_bracket,
            tiny_bracket_label,
            tiny_caption,
        )
        self.wait(max(0.05, 0.68))  # gap to 46.82

        # ---------- 10. [46.82-53.62] ----------
        self.play(
            self.camera.frame.animate.scale(1 / 0.45).move_to(ORIGIN),
            FadeOut(single_event_visuals),
            run_time=max(0.05, 1.20),
        )

        population_current_arrows = VGroup()
        population_thin_lines = VGroup()
        for n in neuron_list:
            synapse_pos, outside_pos, _ = get_synapse_info(n, rng)
            arrow = Arrow(
                outside_pos,
                synapse_pos,
                color=BLUE,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.30,
                buff=0.0,
            ).set_opacity(0)
            line = Line(
                synapse_pos,
                tip_point,
                color=BLUE,
                stroke_width=1.0,
                stroke_opacity=0.25,
            )
            population_current_arrows.add(arrow)
            population_thin_lines.add(line)

        stream_starts = [
            neuron_list[0].get_center(),
            neuron_list[6].get_center(),
            neuron_list[12].get_center(),
        ]
        population_thick_streams = VGroup()
        for s in stream_starts:
            population_thick_streams.add(
                Line(
                    s,
                    tip_point,
                    color=BLUE,
                    stroke_width=6,
                    stroke_opacity=0.45,
                )
            )

        lfp_wave_large = ParametricFunction(
            lambda t: np.array([
                -5.2 + t * 10.4,
                -2.1 + 0.95 * np.sin(2 * np.pi * 1.0 * t)
                + 0.20 * np.sin(2 * np.pi * 2.3 * t),
                0,
            ]),
            t_range=[0, 1, 0.01],
            color=BLUE,
            stroke_width=4,
        )

        self.play(
            LaggedStart(
                *[Indicate(n, color=YELLOW, scale_factor=1.12) for n in neuron_list],
                lag_ratio=0.50,
            ),
            LaggedStart(
                *[FadeIn(a) for a in population_current_arrows],
                lag_ratio=0.50,
            ),
            Create(population_thin_lines),
            run_time=max(0.05, 1.80),
        )

        self.play(
            FadeOut(population_current_arrows),
            FadeOut(population_thin_lines),
            FadeIn(population_thick_streams),
            Transform(lfp_wave, lfp_wave_large),
            run_time=max(0.05, 1.40),
        )
        self.wait(max(0.05, 1.54))

        measurable_signal_label = Text(
            "measurable signal", font_size=26, color=GREEN
        ).next_to(lfp_wave, DOWN, buff=0.25)
        self.play(FadeIn(measurable_signal_label), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.36))
        self.wait(max(0.05, 0.72))  # gap to 54.34

        # ---------- 11. [54.34-57.18] ----------
        left_panel_bg = Rectangle(
            width=5.6,
            height=4.8,
            stroke_color=RED,
            stroke_width=3,
            fill_color=GREY,
            fill_opacity=0.10,
        ).move_to(LEFT * 3.0 + UP * 0.1)
        right_panel_bg = Rectangle(
            width=5.6,
            height=4.8,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=GREY,
            fill_opacity=0.10,
        ).move_to(RIGHT * 3.0 + UP * 0.1)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            FadeIn(left_panel_bg),
            FadeIn(right_panel_bg),
            run_time=max(0.05, 0.80),
        )

        left_panel_center = left_panel_bg.get_center()
        spike_neuron = make_neuron(
            left_panel_center + UP * 0.50,
            color=RED,
            radius=0.24,
            fill_opacity=1.0,
            stroke_color=WHITE,
        )
        spike_title = Text("spike", font_size=32, color=RED).move_to(
            left_panel_bg.get_top() + DOWN * 0.45
        )
        left_axis_y = left_panel_bg.get_bottom()[1] + 0.80
        spike_wave_left = ParametricFunction(
            lambda t: np.array([
                left_panel_center[0] - 0.6 + t * 1.2,
                left_axis_y
                - 0.9 * np.exp(-((t - 0.5) ** 2) / (2 * 0.03 ** 2)),
                0,
            ]),
            t_range=[0, 1, 0.05],
            color=RED,
            stroke_width=3,
        )
        left_bottom_label = Text(
            "spike: rapid activity of one neuron", font_size=18, color=WHITE
        ).scale_to_fit_width(5.0).next_to(left_panel_bg, DOWN, buff=0.2)

        self.play(
            FadeIn(spike_neuron),
            FadeIn(spike_title),
            Create(spike_wave_left),
            FadeIn(left_bottom_label),
            run_time=max(0.05, 0.60),
        )
        self.play(
            Indicate(spike_neuron, color=RED, scale_factor=1.40),
            Indicate(spike_wave_left, color=RED, scale_factor=1.05),
            run_time=max(0.05, 0.50),
        )
        self.play(
            Indicate(spike_neuron, color=RED, scale_factor=1.40),
            Indicate(spike_wave_left, color=RED, scale_factor=1.05),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.44))
        self.wait(max(0.05, 0.62))  # gap to 57.80

        # ---------- 12. [57.80-62.66] ----------
        right_panel_center = right_panel_bg.get_center()
        mini_offsets = [
            (-1.6, 0.7), (0.0, 1.1), (1.6, 0.7),
            (-1.8, 0.0), (0.0, 0.2), (1.8, 0.0),
            (-1.2, -0.8), (0.0, -0.7), (1.2, -0.8),
        ]
        right_panel_neurons = VGroup()
        for dx, dy in mini_offsets:
            pos = right_panel_center + v2(dx, dy)
            right_panel_neurons.add(
                make_neuron(
                    pos,
                    color=BLUE,
                    radius=0.14,
                    fill_opacity=0.80,
                    stroke_color=GREY_B,
                )
            )

        right_title = Text("LFP", font_size=32, color=BLUE).move_to(
            right_panel_bg.get_top() + DOWN * 0.45
        )
        right_wave_x_left = right_panel_bg.get_left()[0] + 0.50
        right_wave_x_right = right_panel_bg.get_right()[0] - 0.50
        right_wave_y = right_panel_bg.get_bottom()[1] + 0.80
        right_lfp_wave = ParametricFunction(
            lambda t: np.array([
                right_wave_x_left + t * (right_wave_x_right - right_wave_x_left),
                right_wave_y + 0.45 * np.sin(2 * np.pi * 1.3 * t),
                0,
            ]),
            t_range=[0, 1, 0.01],
            color=BLUE,
            stroke_width=3,
        )
        right_bottom_label = Text(
            "LFP: slower collective activity of a local population",
            font_size=18,
            color=WHITE,
        ).scale_to_fit_width(5.2).next_to(right_panel_bg, DOWN, buff=0.2)

        right_current_arrows = VGroup()
        for mini_neuron in [
            right_panel_neurons[0],
            right_panel_neurons[2],
            right_panel_neurons[4],
            right_panel_neurons[7],
        ]:
            synapse_pos, outside_pos, _ = get_synapse_info(mini_neuron, rng)
            arrow = Arrow(
                outside_pos,
                synapse_pos,
                color=BLUE,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.30,
                buff=0.0,
            ).set_opacity(0)
            right_current_arrows.add(arrow)

        self.play(
            FadeIn(right_panel_neurons),
            FadeIn(right_title),
            run_time=max(0.05, 0.80),
        )
        self.play(
            Create(right_lfp_wave),
            LaggedStart(*[FadeIn(a) for a in right_current_arrows], lag_ratio=0.30),
            run_time=max(0.05, 1.40),
        )
        self.play(FadeIn(right_bottom_label), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 2.06))
        self.wait(max(0.05, 0.92))  # gap to 63.58

        # ---------- 13. [63.58-67.96] ----------
        self.play(
            Indicate(spike_neuron, color=RED, scale_factor=1.40),
            Indicate(right_lfp_wave, color=BLUE, scale_factor=1.10),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 0.18))

        distinction_caption = Text(
            "fundamental distinction in extracellular recordings",
            font_size=30,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(distinction_caption), run_time=max(0.05, 0.60))
        self.play(
            Indicate(spike_neuron, color=RED, scale_factor=1.40),
            Indicate(right_lfp_wave, color=BLUE, scale_factor=1.10),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 2.00))

        # ---------- 14. [67.96-68.85] ----------
        self.play(
            Indicate(spike_neuron, color=RED, scale_factor=1.40),
            Indicate(right_lfp_wave, color=BLUE, scale_factor=1.10),
            run_time=max(0.05, 0.59),
        )
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=max(0.05, 0.30))