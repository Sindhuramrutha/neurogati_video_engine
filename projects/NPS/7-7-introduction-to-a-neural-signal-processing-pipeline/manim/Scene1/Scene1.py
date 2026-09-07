ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # PIPELINE (visible from previous scene, recedes/dims at opening)
        # ----------------------------------------------------------------
        BOX_W = 2.4
        BOX_H = 0.6
        GAP = 0.38
        center_x = 3.45
        top_y = 2.1
        box_centers = [
            np.array([center_x, top_y - i * (BOX_H + GAP), 0])
            for i in range(4)
        ]

        pipeline_boxes = VGroup(*[
            RoundedRectangle(
                corner_radius=0.12,
                width=BOX_W,
                height=BOX_H,
                fill_color=BLUE,
                fill_opacity=0.10,
                stroke_color=BLUE_B,
                stroke_width=2,
            ).move_to(box_centers[i])
            for i in range(4)
        ])

        pipeline_labels = [
            "Raw Signal",
            "Preprocessing",
            "Feature Extraction",
            "Interpretation or Classification",
        ]
        pipeline_text = VGroup()
        for box, txt in zip(pipeline_boxes, pipeline_labels):
            lab = Text(txt, font_size=15, color=WHITE, weight="BOLD")
            lab.scale_to_fit_width(BOX_W - 0.5)
            lab.move_to(box.get_center())
            pipeline_text.add(lab)

        pipeline_arrows = VGroup(*[
            Arrow(
                pipeline_boxes[i].get_bottom() + DOWN * 0.04,
                pipeline_boxes[i + 1].get_top() + UP * 0.04,
                buff=0,
                color=GREY_B,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.22,
            )
            for i in range(3)
        ])

        pipeline_group = VGroup(pipeline_boxes, pipeline_text, pipeline_arrows)
        pipeline_group.set_opacity(0.65)
        self.add(pipeline_group)

        # ----------------------------------------------------------------
        # HEAD OUTLINE
        # ----------------------------------------------------------------
        head_center = np.array([-3.4, 1.3, 0])
        head_rx = 1.05
        head_ry = 1.4

        head_ellipse = Ellipse(
            width=2 * head_rx,
            height=2 * head_ry,
            stroke_color=GREY_B,
            stroke_width=2.5,
            fill_color=BLUE_D,
            fill_opacity=0.08,
        ).move_to(head_center)

        nose = Polygon(
            head_center + np.array([head_rx, 0.10, 0]),
            head_center + np.array([head_rx + 0.25, -0.10, 0]),
            head_center + np.array([head_rx, -0.50, 0]),
            fill_color=GREY_D,
            fill_opacity=0.35,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )

        head_outline = VGroup(head_ellipse, nose)
        head_outline.set_opacity(0)
        self.add(head_outline)

        # ----------------------------------------------------------------
        # SCALP ELECTRODES
        # ----------------------------------------------------------------
        electrode_angles = [20, 45, 75, 105, 135, 170]
        electrodes = VGroup()
        electrode_positions = []

        for ang_deg in electrode_angles:
            rad = ang_deg * PI / 180
            radial = np.array([np.cos(rad) * head_rx, np.sin(rad) * head_ry, 0])
            point = head_center + np.array([np.cos(rad) * head_rx, np.sin(rad) * head_ry, 0])

            # Small outward nudge, scaled for the ellipse boundary.
            grad = np.array([np.cos(rad) / head_rx, np.sin(rad) / head_ry, 0])
            grad = grad / np.linalg.norm(grad)
            circ_center = point + grad * 0.10

            dot = Circle(
                radius=0.055,
                fill_color=GREY_D,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=0.8,
            ).move_to(circ_center)

            lead_line = Line(
                circ_center + DOWN * 0.02,
                circ_center + DOWN * 0.26,
                color=GREY_B,
                stroke_width=1.6,
            )

            electrode = VGroup(dot, lead_line)
            electrodes.add(electrode)
            electrode_positions.append(circ_center)

        # ----------------------------------------------------------------
        # RECORDING DEVICE AND WIRES
        # ----------------------------------------------------------------
        device_box = Rectangle(
            width=1.5,
            height=0.65,
            fill_color=BLUE_D,
            fill_opacity=0.85,
            stroke_color=GREY_B,
            stroke_width=1.5,
        ).move_to(np.array([-4.8, -1.05, 0]))

        indicator = Circle(
            radius=0.07,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(device_box.get_center() + LEFT * 0.42 + UP * 0.12)

        recording_label = Text(
            "Recording System", font_size=13, color=WHITE
        ).next_to(device_box, RIGHT, buff=0.18)

        recording_system = VGroup(device_box, indicator, recording_label)

        convergence = np.array([-4.8, -0.30, 0])
        wires_group = VGroup()
        for pos in electrode_positions:
            wires_group.add(
                Line(pos, convergence, color=GREY_B, stroke_width=1.2)
            )
        cable = Line(
            convergence,
            device_box.get_top() + UP * 0.02,
            color=GREY_B,
            stroke_width=2.0,
        )
        wires_group.add(cable)

        # ----------------------------------------------------------------
        # NOISY VOLTAGE TRACES
        # ----------------------------------------------------------------
        trace_bases = [-1.45, -1.72, -1.99, -2.26, -2.53, -2.80]
        plot_left = -6.0
        plot_right = 3.6

        trace_lines = VGroup()
        xs = np.linspace(plot_left, plot_right, 220)

        for idx, base_y in enumerate(trace_bases):
            rng = np.random.default_rng(100 + idx)
            ys = (
                base_y
                + 0.09 * np.sin(5.3 * xs + rng.uniform(0, TAU))
                + 0.07 * np.sin(14.7 * xs + rng.uniform(0, TAU))
                + 0.05 * np.sin(31.2 * xs + rng.uniform(0, TAU))
                + rng.normal(0, 0.025, len(xs))
            )
            points = np.array([xs, ys, np.zeros_like(xs)]).T
            trace = VMobject(
                color=WHITE,
                stroke_width=2,
                fill_opacity=0,
            ).set_points_as_corners(points)
            trace.set_opacity(0.85)
            trace_lines.add(trace)

        # ----------------------------------------------------------------
        # LABELS / CHIPS / HIGHLIGHTS
        # ----------------------------------------------------------------
        raw_signal_label = Text(
            "Raw Signal", font_size=27, color=WHITE, weight="BOLD"
        ).move_to(np.array([-1.2, -0.85, 0]))

        chip_names = ["EEG", "ECoG", "EMG", "EOG", "Spike Recordings", "LFP", "MEG"]
        chip_positions = [
            np.array([-1.5, 3.05, 0]),
            np.array([-0.4, 3.25, 0]),
            np.array([-1.6, 2.5, 0]),
            np.array([-0.3, 2.6, 0]),
            np.array([-1.9, 1.9, 0]),
            np.array([-0.2, 2.0, 0]),
            np.array([-1.0, 1.3, 0]),
        ]

        def make_chip(name):
            lab = Text(name, font_size=14, color=WHITE, weight="BOLD")
            rect = RoundedRectangle(
                corner_radius=0.10,
                width=lab.width + 0.4,
                height=lab.height + 0.22,
                fill_color=BLUE,
                fill_opacity=0.15,
                stroke_color=WHITE,
                stroke_width=1.2,
            )
            return VGroup(rect, lab)

        chips = [make_chip(name) for name in chip_names]
        for chip, pos in zip(chips, chip_positions):
            chip.move_to(pos)

        # Blue highlighted oscillatory activity.
        blue_segments_data = [
            (0, -4.8, -3.6, 0.22),
            (2, -2.8, -1.9, 0.20),
            (3, -0.2, 0.8, 0.18),
            (5, -4.0, -3.0, 0.20),
        ]
        blue_segments = VGroup()
        for idx, x0, x1, amp in blue_segments_data:
            seg_xs = np.linspace(x0, x1, 100)
            seg_ys = (
                trace_bases[idx]
                + amp * np.sin(4.5 * seg_xs)
                + 0.04 * np.sin(17 * seg_xs)
            )
            seg_points = np.array([seg_xs, seg_ys, np.zeros_like(seg_xs)]).T
            seg = VMobject(
                color=BLUE,
                stroke_width=6,
                stroke_opacity=0.8,
                fill_opacity=0,
            ).set_points_as_corners(seg_points)
            blue_segments.add(seg)

        # Red arrows + labels for noise and artifact.
        noise_target = np.array([-3.8, trace_bases[1], 0])
        noise_arrow = Arrow(
            start=noise_target + UP * 0.80 + RIGHT * 0.90,
            end=noise_target,
            color=RED,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        )
        noise_label = Text(
            "Noise", font_size=18, color=RED, weight="BOLD"
        ).move_to(noise_arrow.get_start() + UP * 0.30 + LEFT * 0.20)

        artifact_target = np.array([1.4, trace_bases[4], 0])
        artifact_arrow = Arrow(
            start=artifact_target + UP * 1.0 + LEFT * 0.8,
            end=artifact_target,
            color=RED,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        )
        artifact_label = Text(
            "Physiological Artifacts", font_size=16, color=RED, weight="BOLD"
        )
        artifact_label.scale_to_fit_width(2.2)
        artifact_label.move_to(artifact_arrow.get_start() + UP * 0.40 + RIGHT * 0.25)

        # Warning triangle.
        tri = Polygon(
            UP * 0.28,
            DOWN * 0.28 + LEFT * 0.24,
            DOWN * 0.28 + RIGHT * 0.24,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=ORANGE,
            stroke_width=2,
        )
        excl = Text("!", font_size=16, color=BLACK, weight="BOLD").move_to(tri)
        warning_symbol = VGroup(tri, excl)
        warning_symbol.next_to(recording_label, RIGHT, buff=0.25)

        # Caption below plot.
        caption = Text(
            "Not ready for direct interpretation.",
            font_size=17,
            color=WHITE,
            weight="BOLD",
        ).move_to(np.array([-0.6, -3.30, 0]))

        # Axis labels.
        voltage_label = Text("Voltage", font_size=16, color=GREY_B)
        voltage_label.rotate(PI / 2).next_to(trace_lines, LEFT, buff=0.20)
        time_label = Text("Time", font_size=16, color=GREY_B)
        time_label.next_to(trace_lines, DOWN, buff=0.20)

        # Dim overlay for final settling beat.
        dimmer = Rectangle(
            width=16,
            height=9,
            fill_color=BLACK,
            fill_opacity=0.0,
            stroke_width=0,
        ).move_to(ORIGIN)
        dimmer.set_z_index(20)
        self.add(dimmer)

        # ----------------------------------------------------------------
        # BEAT 1 (0.00-1.46): pipeline dims/recedes right, head faintly appears
        # ----------------------------------------------------------------
        self.play(
            pipeline_group.animate.shift(RIGHT * 0.25).set_opacity(0.38),
            head_outline.animate.set_opacity(0.25),
            run_time=max(0.05, 1.46),
        )

        # ----------------------------------------------------------------
        # GAP 1.46-1.96
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.50))

        # ----------------------------------------------------------------
        # BEAT 2 (1.96-2.76): head brightens, Raw Signal box lights
        # ----------------------------------------------------------------
        self.play(
            head_outline.animate.set_opacity(1).set_stroke(WHITE, width=3),
            pipeline_boxes[0].animate.set_stroke(YELLOW, width=5).set_fill(
                BLUE_D, opacity=0.55
            ),
            *[
                pipeline_boxes[i].animate.set_stroke(BLUE_B, width=2).set_fill(
                    BLUE, opacity=0.10
                )
                for i in range(1, 4)
            ],
            run_time=max(0.05, 0.80),
        )

        # ----------------------------------------------------------------
        # GAP 2.76-3.50
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.74))

        # ----------------------------------------------------------------
        # BEAT 3 (3.50-5.22): six scalp electrodes appear one by one
        # ----------------------------------------------------------------
        per_electrode = 1.72 / 6.0
        for electrode in electrodes:
            self.play(
                GrowFromCenter(electrode),
                run_time=max(0.05, per_electrode * 0.65),
            )
            self.wait(max(0.05, per_electrode * 0.35))

        # ----------------------------------------------------------------
        # BEAT 4 (5.22-7.38): wires converge to recording system
        # ----------------------------------------------------------------
        self.play(Create(wires_group), run_time=max(0.05, 1.10))
        self.play(FadeIn(recording_system), run_time=max(0.05, 1.06))

        # ----------------------------------------------------------------
        # BEAT 5 (7.38-9.80): noisy multi-channel traces fade in
        # ----------------------------------------------------------------
        self.play(Create(trace_lines), run_time=max(0.05, 2.42))

        # ----------------------------------------------------------------
        # BEAT 6 (10.64-18.92): Raw Signal label + modality chips
        # ----------------------------------------------------------------
        # Gap 9.80-10.64
        self.wait(max(0.05, 0.84))

        # Raw Signal label appears.
        self.play(Write(raw_signal_label), run_time=max(0.05, 0.70))

        # Wait to EEG chip cue at 13.28.
        self.wait(max(0.05, 1.94))

        # EEG chip pops and glows.
        self.play(GrowFromCenter(chips[0]), run_time=max(0.05, 0.30))
        self.play(
            Indicate(chips[0], color=YELLOW, scale_factor=1.15),
            run_time=max(0.05, 0.25),
        )

        # Additional modality chips, roughly 1-second intervals through 18.92.
        chip_cues = [13.28, 14.36, 15.32, 16.28, 17.24, 18.20, 18.92]
        current_after_first = 13.83

        for i in range(1, len(chips)):
            cue = chip_cues[i]
            wait_t = cue - current_after_first
            if wait_t > 1e-6:
                self.wait(max(0.05, wait_t))

            self.play(GrowFromCenter(chips[i]), run_time=max(0.05, 0.25))
            self.play(
                Indicate(chips[i], color=YELLOW, scale_factor=1.12),
                run_time=max(0.05, 0.12),
            )
            current_after_first = cue + 0.37

        # Tiny gap to beat 7 at 19.34.
        self.wait(max(0.05, 0.05))

        # ----------------------------------------------------------------
        # BEAT 7 (19.34-24.66): EEG glows, other chips dim, electrodes pulse
        # ----------------------------------------------------------------
        self.play(
            Indicate(chips[0], color=YELLOW, scale_factor=1.25),
            *[chips[i].animate.set_opacity(0.30) for i in range(1, len(chips))],
            run_time=max(0.05, 0.60),
        )

        pulse_remaining = 24.66 - 19.94
        pulse_per = pulse_remaining / 6.0

        for i, electrode in enumerate(electrodes):
            self.play(
                electrode.animate.scale(1.35).set_color(YELLOW),
                trace_lines[i].animate.set_color(TEAL).set_opacity(1),
                run_time=max(0.05, pulse_per * 0.55),
            )
            self.play(
                electrode.animate.scale(1 / 1.35).set_color(GREY_B),
                trace_lines[i].animate.set_color(WHITE).set_opacity(0.85),
                run_time=max(0.05, pulse_per * 0.45),
            )

        # ----------------------------------------------------------------
        # BEAT 8 (24.66-28.16): Voltage / Time axis labels fade in
        # ----------------------------------------------------------------
        self.play(
            FadeIn(voltage_label),
            FadeIn(time_label),
            run_time=max(0.05, 0.90),
        )
        self.wait(max(0.05, 2.60))

        # ----------------------------------------------------------------
        # BEAT 9 (28.16-30.42): blue oscillatory segments appear
        # ----------------------------------------------------------------
        self.play(Write(blue_segments), run_time=max(0.05, 1.36))
        self.wait(max(0.05, 0.90))

        # ----------------------------------------------------------------
        # BEAT 10 (30.42-33.10): Noise arrow + label, pulses twice
        # ----------------------------------------------------------------
        self.play(
            FadeIn(noise_arrow),
            FadeIn(noise_label),
            run_time=max(0.05, 1.10),
        )
        self.play(
            Indicate(noise_label, color=RED, scale_factor=1.25),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.20))
        self.play(
            Indicate(noise_label, color=RED, scale_factor=1.25),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.58))

        # ----------------------------------------------------------------
        # BEAT 11 (33.10-34.80): Artifact arrow + label, blue dims slightly
        # ----------------------------------------------------------------
        self.play(
            FadeIn(artifact_arrow),
            FadeIn(artifact_label),
            blue_segments.animate.set_opacity(0.55),
            run_time=max(0.05, 1.00),
        )
        self.play(
            Indicate(artifact_label, color=RED, scale_factor=1.20),
            run_time=max(0.05, 0.35),
        )
        self.play(
            Indicate(artifact_label, color=RED, scale_factor=1.20),
            run_time=max(0.05, 0.35),
        )

        # ----------------------------------------------------------------
        # GAP 34.80-35.62
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.82))

        # ----------------------------------------------------------------
        # BEAT 12 (35.62-37.60): indicator amber + warning triangle
        # ----------------------------------------------------------------
        self.play(
            indicator.animate.set_fill(ORANGE),
            run_time=max(0.05, 0.80),
        )
        self.play(FadeIn(warning_symbol), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.38))

        # ----------------------------------------------------------------
        # BEAT 13 (37.60-39.74): warning pulses, red labels pulse, caption
        # ----------------------------------------------------------------
        self.play(
            Indicate(noise_label, color=RED, scale_factor=1.15),
            Indicate(artifact_label, color=RED, scale_factor=1.15),
            run_time=max(0.05, 0.55),
        )
        self.play(
            blue_segments.animate.set_opacity(0.30),
            FadeIn(caption),
            run_time=max(0.05, 0.65),
        )

        self.play(warning_symbol.animate.scale(1.20), run_time=max(0.05, 0.28))
        self.play(warning_symbol.animate.scale(1 / 1.20), run_time=max(0.05, 0.28))
        self.play(warning_symbol.animate.scale(1.20), run_time=max(0.05, 0.28))
        self.play(warning_symbol.animate.scale(1 / 1.20), run_time=max(0.05, 0.10))

        # ----------------------------------------------------------------
        # BEAT 14 (39.74-40.60): full scene dims gently to settle
        # ----------------------------------------------------------------
        self.play(
            dimmer.animate.set_fill(BLACK, opacity=0.16),
            run_time=max(0.05, 0.86),
        )