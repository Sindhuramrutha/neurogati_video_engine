ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        PATH_Y = 1.5

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------
        def make_sine_wave(amp=0.3, cycles=3, span=1.2, color=WHITE):
            return ParametricFunction(
                lambda t: np.array([
                    span * t / (2 * PI * cycles),
                    amp * np.sin(t),
                    0.0,
                ]),
                t_range=[0, 2 * PI * cycles],
                color=color,
                stroke_width=3,
            )

        def make_spikes(level=3, span=1.2, seed=0):
            rng = np.random.default_rng(seed)
            spikes = VGroup()
            xs = np.linspace(-span / 2, span / 2, level + 2)[1:-1]
            for idx, x in enumerate(xs):
                direction = 1 if idx % 2 == 0 else -1
                height = (0.15 + 0.05 * level) * rng.uniform(0.7, 1.1)
                p1 = np.array([x - 0.08, 0, 0])
                p2 = np.array([x, direction * height, 0])
                p3 = np.array([x + 0.08, direction * height * 0.35, 0])
                spikes.add(Line(p1, p2, color=RED, stroke_width=3))
                spikes.add(Line(p2, p3, color=RED, stroke_width=3))
            return spikes

        def build_stick_figure(center, has_mouth=False):
            fig = VGroup()

            head = Circle(
                radius=0.22,
                fill_color=GREY_B,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=2,
            )
            head.move_to(UP * 1.1)

            body = Line(UP * 0.88, DOWN * 0.55, color=WHITE, stroke_width=3)
            arms = Line(
                UP * 0.35 + LEFT * 0.35,
                UP * 0.35 + RIGHT * 0.35,
                color=WHITE,
                stroke_width=3,
            )
            left_leg = Line(
                DOWN * 0.55,
                DOWN * 1.05 + LEFT * 0.35,
                color=WHITE,
                stroke_width=3,
            )
            right_leg = Line(
                DOWN * 0.55,
                DOWN * 1.05 + RIGHT * 0.35,
                color=WHITE,
                stroke_width=3,
            )

            fig.add(head, body, arms, left_leg, right_leg)

            mouth = None
            if has_mouth:
                mouth = Ellipse(
                    width=0.10,
                    height=0.14,
                    fill_color=BLACK,
                    fill_opacity=1,
                    stroke_width=0,
                )
                mouth.move_to(head.get_center() + RIGHT * 0.16 + UP * 0.05)
                fig.add(mouth)

            fig.move_to(center)
            return fig, mouth

        # ------------------------------------------------------------
        # 1. Whisper in a crowded room (stick figures)
        # ------------------------------------------------------------
        central_pos = np.array([-2.8, -1.0, 0])
        central_fig, central_mouth = build_stick_figure(central_pos, has_mouth=True)

        surrounding_positions = [
            np.array([-4.5, 1.4, 0]),
            np.array([0.5, 2.3, 0]),
            np.array([4.3, -0.7, 0]),
            np.array([-1.0, -2.8, 0]),
        ]
        surrounding_figs = VGroup()
        for pos in surrounding_positions:
            fig, _ = build_stick_figure(pos)
            surrounding_figs.add(fig)

        # Large overlapping noise rings around surrounding figures
        noise_rings = VGroup()
        ring_colors = [ORANGE, PURPLE, PINK, TEAL]
        for pos, color in zip(surrounding_positions, ring_colors):
            for radius in [0.75, 1.0, 1.25]:
                ring = Circle(
                    radius=radius,
                    color=color,
                    fill_opacity=0,
                    stroke_opacity=0.6,
                    stroke_width=2.5,
                )
                ring.move_to(pos + UP * 0.2)
                noise_rings.add(ring)

        # Small faint whisper arcs from central mouth
        whisper_arcs = VGroup()
        for radius in [0.30, 0.44, 0.58]:
            arc = Arc(
                radius=radius,
                start_angle=-PI / 3,
                angle=2 * PI / 3,
                stroke_color=WHITE,
                stroke_width=2,
                stroke_opacity=0.35,
            )
            arc.move_arc_center_to(central_mouth.get_center())
            whisper_arcs.add(arc)

        stick_scene = VGroup(
            central_fig,
            surrounding_figs,
            noise_rings,
            whisper_arcs,
        )

        # Previous scene's title card
        title_bg = Rectangle(
            width=20,
            height=12,
            fill_color="#0F1116",
            fill_opacity=1,
            stroke_width=0,
        )
        title_text = Text("2.3.2 · Learning Objectives", font_size=52, color=WHITE)
        subtitle = Text(
            "Why Do Neural Signals Need Amplification?",
            font_size=32,
            color=GREY_B,
        )
        title_text_group = VGroup(title_text, subtitle).arrange(DOWN, buff=0.30)
        title_text_group.move_to(ORIGIN)
        title_card = VGroup(title_bg, title_text_group)

        self.add(title_card)
        self.play(
            FadeOut(title_card),
            FadeIn(stick_scene),
            run_time=max(0.05, 2.96),
        )
        self.wait(max(0.05, 0.64))  # 3.60

        # ------------------------------------------------------------
        # 2. Whisper arcs pulse weakly, surrounding noise dominates
        # ------------------------------------------------------------
        for _ in range(4):
            self.play(
                whisper_arcs.animate.scale(1.06),
                noise_rings.animate.scale(1.12),
                run_time=max(0.05, 0.705),
            )
            self.play(
                whisper_arcs.animate.scale(1 / 1.06),
                noise_rings.animate.scale(1 / 1.12),
                run_time=max(0.05, 0.705),
            )
        self.wait(max(0.05, 0.78))  # 10.02

        # ------------------------------------------------------------
        # 3. Transition to small neural signal schematic
        # ------------------------------------------------------------
        tissue_line = Line(
            np.array([-6.2, PATH_Y, 0]),
            np.array([-3.2, PATH_Y, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        waveform_vg = make_sine_wave(amp=0.30, cycles=3, span=1.2, color=YELLOW)
        start_pos = np.array([-5.5, PATH_Y, 0])
        waveform_vg.move_to(start_pos)

        initial_schematic_group = VGroup(tissue_line, waveform_vg)

        self.play(
            FadeOut(stick_scene),
            FadeIn(initial_schematic_group),
            run_time=max(0.05, 2.12),
        )
        self.remove(initial_schematic_group)
        self.add(tissue_line, waveform_vg)
        self.wait(max(0.05, 0.72))  # 12.86

        # ------------------------------------------------------------
        # 4. Small waveform labeled and amplitude emphasized
        # ------------------------------------------------------------
        label_neural = Text("Neural signal", font_size=28, color=YELLOW)
        label_neural.next_to(waveform_vg, DOWN, buff=0.70)

        left_br_x = start_pos[0] - 0.80
        top_y = PATH_Y + 0.35
        bottom_y = PATH_Y - 0.35
        amp_bracket = VGroup(
            Line(
                np.array([left_br_x, top_y, 0]),
                np.array([left_br_x, bottom_y, 0]),
                color=WHITE,
                stroke_width=3,
            ),
            Line(
                np.array([left_br_x, top_y, 0]),
                np.array([left_br_x + 0.18, top_y, 0]),
                color=WHITE,
                stroke_width=3,
            ),
            Line(
                np.array([left_br_x, bottom_y, 0]),
                np.array([left_br_x + 0.18, bottom_y, 0]),
                color=WHITE,
                stroke_width=3,
            ),
        )

        self.play(Write(label_neural), Create(amp_bracket), run_time=max(0.05, 0.6))
        self.play(waveform_vg.animate.scale(1.12), run_time=max(0.05, 1.6))
        self.play(waveform_vg.animate.scale(1 / 1.12), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 0.86))  # 17.52

        # ------------------------------------------------------------
        # 5. Signal path extends through four segments
        # ------------------------------------------------------------
        tissue_center = np.array([-4.7, PATH_Y, 0])
        electrode_center = np.array([-2.6, PATH_Y, 0])
        cable_center = np.array([0.65, PATH_Y, 0])
        circuits_center = np.array([3.7, PATH_Y, 0])
        recording_pos = np.array([5.7, PATH_Y, 0])

        tissue_label = Text("Biological tissue", font_size=22, color=WHITE)
        tissue_label.next_to(tissue_line, UP, buff=0.25)

        electrode_line = Line(
            np.array([-3.2, PATH_Y, 0]),
            np.array([-2.0, PATH_Y, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        electrode_vertical = Line(
            np.array([-2.6, PATH_Y - 0.35, 0]),
            np.array([-2.6, PATH_Y + 0.35, 0]),
            color=WHITE,
            stroke_width=4,
        )
        electrode_group = VGroup(electrode_line, electrode_vertical)
        electrode_label = Text("Electrode", font_size=22, color=WHITE)
        electrode_label.next_to(electrode_group, UP, buff=0.25)

        cable_line = ParametricFunction(
            lambda u: np.array([
                -0.7 + 2.7 * u / (4 * PI),
                PATH_Y + 0.35 * np.sin(u),
                0.0,
            ]),
            t_range=[0, 4 * PI],
            color=GREY_B,
            stroke_width=3,
        )
        cable_label = Text("Cables", font_size=22, color=WHITE)
        cable_label.next_to(cable_line, UP, buff=0.25)

        circuits_box = Rectangle(
            width=2.4,
            height=0.9,
            color=PURPLE,
            fill_color=PURPLE,
            fill_opacity=0.2,
            stroke_width=3,
        )
        circuits_box.move_to(circuits_center)
        circuits_label = Text("Electronic circuits", font_size=22, color=WHITE)
        circuits_label.next_to(circuits_box, UP, buff=0.25)

        self.play(FadeOut(label_neural), FadeOut(amp_bracket), run_time=max(0.05, 0.5))
        self.play(
            Write(tissue_label),
            waveform_vg.animate.move_to(tissue_center),
            run_time=max(0.05, 1.5),
        )
        self.play(
            Create(electrode_group),
            Write(electrode_label),
            waveform_vg.animate.move_to(electrode_center),
            run_time=max(0.05, 1.9),
        )
        self.play(
            Create(cable_line),
            Write(cable_label),
            waveform_vg.animate.move_to(cable_center),
            run_time=max(0.05, 1.9),
        )
        self.play(
            Create(circuits_box),
            Write(circuits_label),
            waveform_vg.animate.move_to(circuits_center),
            run_time=max(0.05, 1.9),
        )
        self.wait(max(0.05, 0.38))
        self.wait(max(0.05, 0.82))  # 26.42

        # ------------------------------------------------------------
        # 6. Interference accumulates across segments
        # ------------------------------------------------------------
        segment_positions = [
            tissue_center,
            electrode_center,
            cable_center,
            circuits_center,
        ]
        spike_levels = [3, 5, 7, 9]

        self.play(waveform_vg.animate.move_to(start_pos), run_time=max(0.05, 0.6))

        self.remove(waveform_vg)
        distortion_overlay = VGroup()
        moving_group = VGroup(waveform_vg, distortion_overlay)
        moving_group.move_to(start_pos)
        self.add(moving_group)

        per_item = (5.24 - 0.6) / 4.0
        for idx, pos in enumerate(segment_positions):
            self.play(
                moving_group.animate.move_to(pos),
                run_time=max(0.05, per_item * 0.58),
            )
            spikes = make_spikes(level=spike_levels[idx], seed=idx)
            spikes.move_to(pos)
            self.play(FadeIn(spikes), run_time=max(0.05, per_item * 0.58))
            self.remove(spikes)
            distortion_overlay.add(spikes)

        self.wait(max(0.05, 0.80))  # 32.46

        # ------------------------------------------------------------
        # 7. Dirty signal reaches recording system, red risk glow
        # ------------------------------------------------------------
        recording_line = DashedLine(
            np.array([6.1, PATH_Y - 0.5, 0]),
            np.array([6.1, PATH_Y + 0.5, 0]),
            color=GREY_B,
            stroke_opacity=0.7,
            stroke_width=3,
        )
        recording_label = Text("Recording system", font_size=22, color=GREY_B)
        recording_label.next_to(recording_line, DOWN, buff=0.2)
        recording_label.shift(LEFT * 0.4)

        self.play(
            Create(recording_line),
            Write(recording_label),
            run_time=max(0.05, 1.4),
        )
        self.play(moving_group.animate.move_to(recording_pos), run_time=max(0.05, 1.6))

        red_glow = SurroundingRectangle(
            moving_group,
            color=RED,
            buff=0.22,
            corner_radius=0.2,
            stroke_width=5,
        )
        self.play(Create(red_glow), run_time=max(0.05, 1.5))
        self.play(FadeOut(red_glow), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 0.74))  # 39.10

        # ------------------------------------------------------------
        # 8. First electronic component after electrode: amplifier
        # ------------------------------------------------------------
        amp_pos = np.array([-1.35, PATH_Y, 0])
        tri_vertices = [
            np.array([-0.6, 0.5, 0]),
            np.array([-0.6, -0.5, 0]),
            np.array([0.7, 0, 0]),
        ]
        triangle = Polygon(
            *tri_vertices,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=3,
        )
        halo = Circle(
            radius=0.85,
            color=GREEN,
            fill_opacity=0.22,
            stroke_width=0,
        )
        halo.move_to(triangle.get_center())

        plus_sign = Text("+", font_size=30, color=WHITE)
        plus_sign.next_to(triangle, RIGHT, buff=0.18).shift(UP * 0.28)
        minus_sign = Text("−", font_size=30, color=WHITE)
        minus_sign.next_to(triangle, RIGHT, buff=0.18).shift(DOWN * 0.28)

        amp_label = Text("Amplifier", font_size=26, color=YELLOW)
        amp_label.next_to(triangle, DOWN, buff=0.30)

        amplifier_group = VGroup(halo, triangle, plus_sign, minus_sign, amp_label)
        amplifier_group.move_to(amp_pos)
        amplifier_group.shift(RIGHT * 5)

        self.play(
            self.camera.frame.animate.scale(0.45).move_to(np.array([-1.35, PATH_Y, 0])),
            run_time=max(0.05, 1.5),
        )
        self.play(amplifier_group.animate.shift(LEFT * 5), run_time=max(0.05, 1.3))
        self.play(halo.animate.set_opacity(0.9), run_time=max(0.05, 0.63))
        self.play(halo.animate.set_opacity(0.22), run_time=max(0.05, 0.63))
        self.wait(max(0.05, 1.06))  # 44.22

        # ------------------------------------------------------------
        # 9. Key definition and amplitude comparison
        # ------------------------------------------------------------
        def_box = Rectangle(
            width=7.8,
            height=3.0,
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.15,
            stroke_width=3,
        )
        def_box.move_to(np.array([0, -1.2, 0]))

        heading = Text("Amplification", font_size=40, color=YELLOW, weight="BOLD")
        line1 = Text(
            "increasing the amplitude of a biological signal",
            font_size=26,
            color=WHITE,
        ).scale_to_fit_width(4.3)
        line2 = Text(
            "without altering the information it contains",
            font_size=26,
            color=WHITE,
        ).scale_to_fit_width(4.3)

        text_block = VGroup(heading, line1, line2).arrange(
            DOWN,
            buff=0.28,
            aligned_edge=LEFT,
        )
        text_block.move_to(def_box.get_center()).shift(LEFT * 1.7)

        small_wave = make_sine_wave(amp=0.32, cycles=3, span=1.2, color=GREEN)
        small_wave.move_to(np.array([2.5, -2.35, 0]))
        tall_wave = make_sine_wave(amp=0.90, cycles=3, span=1.2, color=GREEN)
        tall_wave.move_to(np.array([2.5, -0.60, 0]))

        compare_arrow = Arrow(
            small_wave.get_top(),
            tall_wave.get_bottom(),
            buff=0.08,
            color=YELLOW,
        )

        self.play(
            self.camera.frame.animate.scale(1 / 0.45).move_to(ORIGIN),
            run_time=max(0.05, 1.0),
        )
        self.play(
            amplifier_group.animate.set_opacity(0.35),
            tissue_line.animate.set_opacity(0.30),
            electrode_group.animate.set_opacity(0.30),
            cable_line.animate.set_opacity(0.30),
            circuits_box.animate.set_opacity(0.30),
            tissue_label.animate.set_opacity(0.30),
            electrode_label.animate.set_opacity(0.30),
            cable_label.animate.set_opacity(0.30),
            circuits_label.animate.set_opacity(0.30),
            moving_group.animate.set_opacity(0.30),
            recording_line.animate.set_opacity(0.20),
            recording_label.animate.set_opacity(0.20),
            run_time=max(0.05, 0.4),
        )
        self.play(Create(def_box), Write(heading), run_time=max(0.05, 1.2))
        self.play(Write(line1), run_time=max(0.05, 1.6))
        self.play(Write(line2), run_time=max(0.05, 1.6))
        self.play(
            Create(small_wave),
            Create(tall_wave),
            Create(compare_arrow),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 1.71))