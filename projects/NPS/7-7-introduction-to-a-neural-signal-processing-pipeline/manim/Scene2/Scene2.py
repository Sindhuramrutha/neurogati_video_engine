ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Layout constants
        # ----------------------------------------------------------------
        raw_center_y = 1.7
        raw_center = np.array([-1.0, raw_center_y, 0])
        processed_center_y = -1.5
        processed_center = np.array([-1.0, processed_center_y, 0])
        box_y = 0.0

        # ----------------------------------------------------------------
        # Signal construction
        # ----------------------------------------------------------------
        xs = np.linspace(-5.6, 3.8, 400)

        def center_signal(y, y_center=raw_center_y):
            return y - np.mean(y) + y_center

        def triangular_spike(xs, center=0.4, half_width=0.45, amp=0.55):
            y = np.zeros_like(xs)
            mask = np.abs(xs - center) < half_width
            y[mask] = amp * (1 - np.abs(xs[mask] - center) / half_width)
            return y

        drift = 0.06 * xs + 0.16 * np.sin(0.35 * xs + 1.3) + 0.10
        neural = 0.22 * np.sin(1.7 * xs) + 0.10 * np.sin(4.3 * xs + 0.5)
        highfreq = 0.055 * np.sin(27 * xs + 0.2) + 0.025 * np.sin(47 * xs + 0.9)
        spike = triangular_spike(xs, center=0.4, half_width=0.45, amp=0.55)

        raw_ys = center_signal(drift + neural + highfreq + spike, raw_center_y)
        filtered_ys = center_signal(drift + neural + spike, raw_center_y)
        no_spike_ys = center_signal(drift + neural, raw_center_y)
        flat_ys = center_signal(neural, raw_center_y)
        norm_neural = neural / np.max(np.abs(neural)) * 0.62
        normalized_ys = center_signal(norm_neural, raw_center_y)
        highfreq_ys = center_signal(highfreq, raw_center_y)
        neural_ys = center_signal(neural, raw_center_y)

        def make_trace(xs, ys, color=WHITE, stroke_width=2, opacity=1):
            points = np.array([xs, ys, np.zeros_like(xs)]).T
            trace = VMobject(color=color, stroke_width=stroke_width, fill_opacity=0)
            trace.set_points_as_corners(points)
            trace.set_opacity(opacity)
            return trace

        def gen_other_signal(seed):
            rng = np.random.default_rng(seed)
            y = (
                0.14 * np.sin(1.4 * xs + rng.uniform(0, TAU))
                + 0.05 * np.sin(11 * xs + rng.uniform(0, TAU))
                + rng.normal(0, 0.03, len(xs))
            )
            return y

        # ----------------------------------------------------------------
        # Old scene state: previous scene's head, electrodes, wires, device
        # ----------------------------------------------------------------
        head_center_old = np.array([-3.4, 1.3, 0])
        head_ellipse = Ellipse(
            width=2.2,
            height=3.0,
            fill_color=BLUE_D,
            fill_opacity=0.08,
            stroke_color=GREY_B,
            stroke_width=2.5,
        ).move_to(head_center_old)
        nose = Polygon(
            head_center_old + np.array([1.1, 0.10, 0]),
            head_center_old + np.array([1.35, -0.10, 0]),
            head_center_old + np.array([1.1, -0.50, 0]),
            fill_color=GREY_D,
            fill_opacity=0.35,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )

        electrode_positions = []
        old_electrodes = VGroup()
        for angle_deg in [15, 45, 75, 105, 145]:
            rad = angle_deg * PI / 180
            pos = head_center_old + np.array([1.1 * np.cos(rad), 1.5 * np.sin(rad), 0])
            electrode_positions.append(pos)
            dot = Circle(
                radius=0.055,
                fill_color=GREY_D,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1,
            ).move_to(pos)
            old_electrodes.add(dot)

        convergence = np.array([-4.8, -0.30, 0])
        old_wires = VGroup()
        for pos in electrode_positions:
            old_wires.add(Line(pos, convergence, color=GREY_B, stroke_width=1.2))
        device_box = Rectangle(
            width=1.6,
            height=0.7,
            fill_color=BLUE_D,
            fill_opacity=0.85,
            stroke_color=GREY_B,
            stroke_width=1.5,
        ).move_to(np.array([-4.8, -1.2, 0]))
        recording_label = Text("Recording System", font_size=13, color=WHITE).next_to(
            device_box, RIGHT, buff=0.15
        )
        recording_system = VGroup(device_box, recording_label)
        old_scene = VGroup(
            head_ellipse, nose, old_electrodes, old_wires, recording_system
        )

        # ----------------------------------------------------------------
        # Initial multi-channel traces, one central raw trace
        # ----------------------------------------------------------------
        initial_multi_centers = [-1.4, -1.7, -2.0, -1.5, -2.35, -2.7]
        central_idx = 3

        multi_ys_list = []
        for i, yc in enumerate(initial_multi_centers):
            if i == central_idx:
                multi_ys_list.append(raw_ys - (raw_center_y - yc))
            else:
                multi_ys_list.append(gen_other_signal(i) + yc)

        multi_traces = VGroup(
            *[
                make_trace(xs, ys, color=WHITE, stroke_width=2, opacity=0.85)
                for ys in multi_ys_list
            ]
        )
        raw_trace = multi_traces[central_idx]

        # ----------------------------------------------------------------
        # Processing boxes
        # ----------------------------------------------------------------
        box_labels_names = [
            "Filtering",
            "Artifact Detection",
            "Artifact Removal",
            "Signal Segmentation",
            "Baseline Correction",
            "Normalization",
        ]
        box_w = 1.15
        box_h = 0.55

        box_rects = []
        box_labels = []
        box_groups = []
        for name in box_labels_names:
            rect = RoundedRectangle(
                corner_radius=0.10,
                width=box_w,
                height=box_h,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_opacity=0,
            )
            lab = Text(name, font_size=13, color=WHITE, weight="BOLD")
            lab.scale_to_fit_width(box_w - 0.25)
            lab.set_opacity(0)
            group = VGroup(rect, lab)
            box_groups.append(group)
            box_rects.append(rect)
            box_labels.append(lab)

        boxes_group = VGroup(*box_groups).arrange(RIGHT, buff=0.18).move_to(
            np.array([0, box_y, 0])
        )
        box_rects_group = VGroup(*box_rects)

        # Targets for later transformations
        filtered_trace = make_trace(xs, filtered_ys, color=WHITE, stroke_width=3)
        no_spike_trace = make_trace(xs, no_spike_ys, color=WHITE, stroke_width=3)
        baseline_corrected_trace = make_trace(xs, flat_ys, color=WHITE, stroke_width=3)
        normalized_trace = make_trace(xs, normalized_ys, color=WHITE, stroke_width=3)

        # ----------------------------------------------------------------
        # Overlays and labels
        # ----------------------------------------------------------------
        highfreq_overlay = make_trace(
            xs, highfreq_ys, color=ORANGE, stroke_width=2, opacity=0.45
        )
        neural_outline = make_trace(
            xs, neural_ys, color=BLUE, stroke_width=4, opacity=0.75
        )

        preprocessing_title = Text(
            "Preprocessing", font_size=40, color=WHITE, weight="BOLD"
        ).move_to(np.array([-1.0, 3.15, 0]))

        goal_group = VGroup(
            Text("Goal: ", font_size=21, color=WHITE, weight="BOLD"),
            Text("Reduce", font_size=21, color=WHITE, weight="BOLD"),
            Text(" unwanted components", font_size=21, color=WHITE, weight="BOLD"),
        ).arrange(RIGHT, buff=0.10)
        goal_group.move_to(np.array([-2.8, 0.70, 0]))
        goal_group.set_opacity(0)

        preserve_label = Text(
            "Preserve neural information", font_size=20, color=BLUE, weight="BOLD"
        ).move_to(np.array([2.8, 0.70, 0]))
        preserve_label.set_opacity(0)

        cleaner_label = Text("Cleaner", font_size=24, color=GREY_B, weight="BOLD").move_to(
            np.array([-2.3, -0.65, 0])
        )
        clean_label = Text("Clean", font_size=24, color=GREY_B, weight="BOLD").move_to(
            np.array([0.4, -0.65, 0])
        )
        cleaner_red_x = Text("✗", font_size=34, color=RED, weight="BOLD").move_to(
            cleaner_label.get_center()
        )
        cleaner_red_x.set_opacity(0)

        # ----------------------------------------------------------------
        # Helper dashed constructors
        # ----------------------------------------------------------------
        def dashed_hline(x0, x1, y, color=GREY_B, dash_len=0.07, gap=0.05):
            parts = VGroup()
            x = x0
            while x < x1 - 1e-6:
                x2 = min(x + dash_len, x1)
                parts.add(
                    Line(
                        np.array([x, y, 0]),
                        np.array([x2, y, 0]),
                        color=color,
                        stroke_width=2,
                    )
                )
                x = x2 + gap
            return parts

        def dashed_vline(x, y0, y1, color=GREY_B, dash_len=0.07, gap=0.05):
            parts = VGroup()
            y = y0
            while y < y1 - 1e-6:
                y2 = min(y + dash_len, y1)
                parts.add(
                    Line(
                        np.array([x, y, 0]),
                        np.array([x, y2, 0]),
                        color=color,
                        stroke_width=2,
                    )
                )
                y = y2 + gap
            return parts

        def dashed_rectangle(x0, x1, y0, y1, color=GREY_B):
            return VGroup(
                dashed_hline(x0, x1, y0, color),
                dashed_hline(x0, x1, y1, color),
                dashed_vline(x0, y0, y1, color),
                dashed_vline(x1, y0, y1, color),
            )

        dotted_cleaner_line = dashed_hline(
            cleaner_label.get_left()[0] - 0.1,
            cleaner_label.get_right()[0] + 0.1,
            cleaner_label.get_center()[1],
            color=RED,
        )
        dotted_cleaner_line.set_opacity(0)

        # ----------------------------------------------------------------
        # Initial visibility
        # ----------------------------------------------------------------
        self.add(old_scene, multi_traces)

        # ----------------------------------------------------------------
        # Beat 1 (0.00-1.66): keep central trace, fade others and old scene
        # ----------------------------------------------------------------
        noncentral = [t for i, t in enumerate(multi_traces) if i != central_idx]
        self.play(
            FadeOut(old_scene),
            *[FadeOut(t) for t in noncentral],
            raw_trace.animate.shift(raw_center - raw_trace.get_center()),
            run_time=max(0.05, 1.66),
        )

        # ----------------------------------------------------------------
        # Beat 2 (1.66-2.38): six empty boxes fade in below trace
        # ----------------------------------------------------------------
        self.play(FadeIn(box_rects_group), run_time=max(0.05, 0.72))

        # ----------------------------------------------------------------
        # Beat 3 (2.38-2.92): title appears, raw trace brightens
        # ----------------------------------------------------------------
        self.play(
            Write(preprocessing_title),
            raw_trace.animate.set_stroke(width=4).set_opacity(1),
            run_time=max(0.05, 0.54),
        )

        # ----------------------------------------------------------------
        # Beat 4 (2.92-4.22): first box lights with Filtering
        # ----------------------------------------------------------------
        self.play(
            box_rects[0].animate.set_fill(BLUE_D, opacity=0.72).set_stroke(
                YELLOW, width=4
            ),
            box_labels[0].animate.set_opacity(1),
            run_time=max(0.05, 1.30),
        )

        # ----------------------------------------------------------------
        # Beat 5 (4.22-6.24): high-frequency overlay and downward arrow
        # ----------------------------------------------------------------
        down_arrow = Arrow(
            start=raw_center + np.array([-3.3, -0.3, 0]),
            end=raw_center + np.array([-3.3, -2.0, 0]),
            color=WHITE,
            stroke_width=4,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )
        down_arrow.set_opacity(0)
        self.play(FadeIn(highfreq_overlay), run_time=max(0.05, 1.0))
        self.play(down_arrow.animate.set_opacity(1), run_time=max(0.05, 1.02))

        # ----------------------------------------------------------------
        # Beat 6 (6.24-7.18): lift/settle, dashed processing region
        # ----------------------------------------------------------------
        dashed_region = dashed_rectangle(-5.8, 3.8, 0.90, 2.60, GREY_B)
        dashed_region.set_stroke(GREY_B, width=1.5).set_opacity(0.35)
        dashed_region.set_opacity(0)
        self.play(raw_trace.animate.shift(UP * 0.10), run_time=max(0.05, 0.31))
        self.play(raw_trace.animate.shift(DOWN * 0.10), run_time=max(0.05, 0.31))
        self.play(dashed_region.animate.set_opacity(0.35), run_time=max(0.05, 0.32))

        # Gap 7.18-8.14
        self.wait(max(0.05, 0.96))

        # ----------------------------------------------------------------
        # Beat 7 (8.14-8.92): Cleaner / Clean labels
        # ----------------------------------------------------------------
        self.play(FadeIn(cleaner_label), FadeIn(clean_label), run_time=max(0.05, 0.78))

        # ----------------------------------------------------------------
        # Beat 8 (8.92-10.68): Cleaner red X flash, dotted strike line
        # ----------------------------------------------------------------
        self.play(cleaner_red_x.animate.set_opacity(1), run_time=max(0.05, 0.42))
        self.play(cleaner_red_x.animate.set_opacity(0), run_time=max(0.05, 0.42))
        self.play(dotted_cleaner_line.animate.set_opacity(1), run_time=max(0.05, 0.92))

        # Gap 10.68-11.44
        self.wait(max(0.05, 0.76))

        # ----------------------------------------------------------------
        # Beat 9 (11.44-12.54): goal label appears, cleaner fades
        # ----------------------------------------------------------------
        cleaner_group = VGroup(cleaner_label, dotted_cleaner_line)
        self.play(
            FadeOut(cleaner_group),
            FadeOut(down_arrow),
            FadeOut(dashed_region),
            FadeIn(goal_group),
            run_time=max(0.05, 1.10),
        )

        # ----------------------------------------------------------------
        # Beat 10 (12.54-13.42): Reduce glows, highfreq pulses
        # ----------------------------------------------------------------
        reduce_word = goal_group[1]
        self.play(
            reduce_word.animate.set_color(YELLOW).scale(1.25),
            highfreq_overlay.animate.set_opacity(0.9),
            run_time=max(0.05, 0.44),
        )
        self.play(
            reduce_word.animate.scale(1 / 1.25).set_color(WHITE),
            highfreq_overlay.animate.set_opacity(0.45),
            run_time=max(0.05, 0.44),
        )

        # ----------------------------------------------------------------
        # Beat 11 (13.42-14.96): preserve label + blue neural outline
        # ----------------------------------------------------------------
        self.play(
            FadeIn(preserve_label),
            Write(neural_outline),
            run_time=max(0.05, 1.54),
        )

        # ----------------------------------------------------------------
        # Beat 12 (14.96-16.98): blue outline pulses, magnifier appears
        # ----------------------------------------------------------------
        def magnifier_icon(color=YELLOW, scale=1):
            circle = Circle(radius=0.22, color=color, stroke_width=3, fill_opacity=0)
            handle = Line(
                circle.get_center() + RIGHT * 0.15 + DOWN * 0.15,
                circle.get_center() + RIGHT * 0.42 + DOWN * 0.42,
                color=color,
                stroke_width=4,
            )
            grp = VGroup(circle, handle).scale(scale)
            return grp

        neural_magnifier = magnifier_icon(YELLOW, scale=0.65).move_to(
            np.array([0.1, 2.15, 0])
        )
        self.play(
            Indicate(neural_outline, color=BLUE, scale_factor=1.08),
            run_time=max(0.05, 0.85),
        )
        self.play(FadeIn(neural_magnifier), run_time=max(0.05, 1.17))

        # Gap 16.98-17.82
        self.wait(max(0.05, 0.84))

        # ----------------------------------------------------------------
        # Beat 13 (17.82-18.36): goal dims, boxes become focal
        # ----------------------------------------------------------------
        self.play(
            goal_group.animate.set_opacity(0.40),
            *[rect.animate.set_stroke(WHITE, width=3) for rect in box_rects],
            boxes_group.animate.shift(UP * 0.08).scale(1.05),
            run_time=max(0.05, 0.54),
        )

        # ----------------------------------------------------------------
        # Beat 14 (18.36-19.62): Filtering removes high-frequency noise
        # ----------------------------------------------------------------
        work_trace = raw_trace.copy()
        raw_trace.set_opacity(0)
        self.add(work_trace)

        self.play(
            box_groups[0].animate.shift(UP * 0.06).set_stroke(YELLOW, width=5),
            run_time=max(0.05, 0.20),
        )
        self.play(
            highfreq_overlay.animate.shift(UP * 0.25).set_opacity(0.20),
            run_time=max(0.05, 0.32),
        )
        self.play(
            FadeOut(highfreq_overlay),
            Transform(work_trace, filtered_trace),
            run_time=max(0.05, 0.74),
        )

        # ----------------------------------------------------------------
        # Beat 15 (19.62-21.06): Artifact Detection
        # ----------------------------------------------------------------
        self.play(
            box_rects[1].animate.set_fill(BLUE_D, opacity=0.72).set_stroke(
                YELLOW, width=4
            ),
            box_labels[1].animate.set_opacity(1),
            run_time=max(0.05, 0.62),
        )

        spike_x = 0.4
        spike_idx = int(np.argmin(np.abs(xs - spike_x)))
        spike_peak_y = filtered_ys[spike_idx]

        artifact_highlight = Circle(
            radius=0.30,
            color=RED,
            fill_color=RED,
            fill_opacity=0.14,
            stroke_width=3,
        ).move_to(np.array([spike_x, spike_peak_y, 0]))
        artifact_magnifier = magnifier_icon(RED, scale=0.55).move_to(
            np.array([spike_x + 0.55, spike_peak_y + 0.38, 0])
        )
        artifact_label = Text("Artifact", font_size=16, color=RED, weight="BOLD")
        artifact_label.next_to(artifact_magnifier, UR, buff=0.08)
        self.play(
            FadeIn(artifact_highlight),
            FadeIn(artifact_magnifier),
            FadeIn(artifact_label),
            run_time=max(0.05, 0.82),
        )

        # ----------------------------------------------------------------
        # Beat 16 (21.06-22.32): Artifact Removal
        # ----------------------------------------------------------------
        self.play(
            box_rects[2].animate.set_fill(BLUE_D, opacity=0.72).set_stroke(
                YELLOW, width=4
            ),
            box_labels[2].animate.set_opacity(1),
            run_time=max(0.05, 0.32),
        )
        self.play(
            Indicate(artifact_highlight, color=RED, scale_factor=1.22),
            run_time=max(0.05, 0.25),
        )
        self.play(
            Indicate(artifact_highlight, color=RED, scale_factor=1.22),
            run_time=max(0.05, 0.25),
        )
        self.play(
            Transform(work_trace, no_spike_trace),
            FadeOut(artifact_highlight),
            FadeOut(artifact_magnifier),
            FadeOut(artifact_label),
            run_time=max(0.05, 0.44),
        )

        # ----------------------------------------------------------------
        # Beat 17 (22.32-23.92): Signal Segmentation
        # ----------------------------------------------------------------
        self.play(
            box_rects[3].animate.set_fill(BLUE_D, opacity=0.72).set_stroke(
                YELLOW, width=4
            ),
            box_labels[3].animate.set_opacity(1),
            run_time=max(0.05, 0.42),
        )

        seg_boundaries = [-3.3, -0.9, 1.5]
        top_segment_lines = VGroup(
            *[
                dashed_vline(x, raw_center_y - 0.85, raw_center_y + 0.85, GREY_B)
                for x in seg_boundaries
            ]
        )
        seg_name_positions = [
            np.array([-4.45, 0.45, 0]),
            np.array([-2.10, 0.45, 0]),
            np.array([0.30, 0.45, 0]),
            np.array([2.65, 0.45, 0]),
        ]
        top_segment_labels = VGroup(
            *[
                Text(f"Segment {i+1}", font_size=12, color=GREY_B).move_to(pos)
                for i, pos in enumerate(seg_name_positions)
            ]
        )
        self.play(
            FadeIn(top_segment_lines),
            FadeIn(top_segment_labels),
            run_time=max(0.05, 1.18),
        )

        # ----------------------------------------------------------------
        # Beat 18 (23.92-25.04): Baseline Correction
        # ----------------------------------------------------------------
        zero_reference = dashed_hline(
            -5.6, 3.8, raw_center_y, color=GREY_B, dash_len=0.09, gap=0.06
        )
        zero_reference.set_opacity(0.45)
        zero_reference.set_opacity(0)
        self.play(
            box_rects[4].animate.set_fill(BLUE_D, opacity=0.72).set_stroke(
                YELLOW, width=4
            ),
            box_labels[4].animate.set_opacity(1),
            run_time=max(0.05, 0.32),
        )
        self.play(
            Transform(work_trace, baseline_corrected_trace),
            zero_reference.animate.set_opacity(0.45),
            run_time=max(0.05, 0.80),
        )

        # ----------------------------------------------------------------
        # Beat 19 (25.04-26.46): Normalization
        # ----------------------------------------------------------------
        self.play(
            box_rects[5].animate.set_fill(BLUE_D, opacity=0.72).set_stroke(
                YELLOW, width=4
            ),
            box_labels[5].animate.set_opacity(1),
            run_time=max(0.05, 0.32),
        )
        self.play(Transform(work_trace, normalized_trace), run_time=max(0.05, 1.10))

        # ----------------------------------------------------------------
        # Beat 20 (26.46-27.34): all boxes pulse, processed trace below raw
        # ----------------------------------------------------------------
        processed_trace = normalized_trace.copy().shift(
            np.array([0, processed_center_y - raw_center_y, 0])
        )
        processed_segment_lines = VGroup(
            *[
                dashed_vline(
                    x,
                    processed_center_y - 0.80,
                    processed_center_y + 0.80,
                    GREY_B,
                )
                for x in seg_boundaries
            ]
        )
        processed_segment_labels = VGroup(
            *[
                Text(f"Segment {i+1}", font_size=12, color=GREY_B).move_to(
                    np.array([pos[0], processed_center_y - 1.05, 0])
                )
                for i, pos in enumerate(seg_name_positions)
            ]
        )
        processed_trace_group = VGroup(
            processed_trace, processed_segment_lines, processed_segment_labels
        )
        processed_trace_group.set_opacity(0)

        self.play(
            raw_trace.animate.set_opacity(0.30),
            FadeOut(work_trace),
            FadeIn(processed_trace_group),
            run_time=max(0.05, 0.50),
        )
        pulse_t = 0.38 / 6
        for box_group in box_groups:
            self.play(
                Indicate(box_group, color=YELLOW, scale_factor=1.08),
                run_time=max(0.05, pulse_t),
            )

        # ----------------------------------------------------------------
        # Beat 21 (27.34-29.44): side panel with four artifact cards
        # ----------------------------------------------------------------
        mini_xs = np.linspace(-1.1, 1.1, 120)
        mini_power = 0.10 * np.sin(8 * mini_xs + 0.2)
        mini_eye = triangular_spike(mini_xs, center=0, half_width=0.55, amp=0.38)
        mini_muscle = 0.08 * np.sin(20 * mini_xs) + 0.06 * np.sin(43 * mini_xs + 1.4)
        mini_drift = 0.18 * mini_xs + 0.04 * np.sin(1.8 * mini_xs + 0.4)
        mini_signals = [mini_power, mini_eye, mini_muscle, mini_drift]
        card_colors = [ORANGE, RED, PINK, TEAL]
        card_names = [
            "Power-line Interference",
            "Eye-blink Artifact",
            "Muscle Activity",
            "Baseline Drift",
        ]

        card_groups = []
        card_rects = []
        card_waves = []
        card_xs = []
        side_panel_group = VGroup()
        for i in range(4):
            rect = RoundedRectangle(
                corner_radius=0.10,
                width=2.55,
                height=0.72,
                fill_color=BLUE_D,
                fill_opacity=0.10,
                stroke_color=GREY_B,
                stroke_width=2,
            )
            lab = Text(card_names[i], font_size=11, color=WHITE, weight="BOLD")
            lab.scale_to_fit_width(2.15)
            wave = make_trace(mini_xs, mini_signals[i], color=card_colors[i], stroke_width=2)
            wave.scale_to_fit_width(2.10)
            wave.move_to(rect.get_center() + DOWN * 0.14)
            lab.move_to(rect.get_center() + UP * 0.20)
            card = VGroup(rect, lab, wave)
            card_groups.append(card)
            card_rects.append(rect)
            card_waves.append(wave)
            side_panel_group.add(card)

        side_panel_group.arrange(DOWN, buff=0.18).move_to(np.array([5.5, -0.15, 0]))

        card_x_marks = []
        for card in card_groups:
            x_mark = Text("✗", color=RED, font_size=24, weight="BOLD").move_to(
                card.get_center() + UP * 0.22
            )
            x_mark.set_opacity(0)
            card_x_marks.append(x_mark)
            side_panel_group.add(x_mark)

        self.play(FadeIn(side_panel_group), run_time=max(0.05, 2.10))

        # ----------------------------------------------------------------
        # Card extraction helper
        # ----------------------------------------------------------------
        raw_copy_target = raw_trace.get_center()

        # Beat 22 (29.44-31.20): Power-line Interference
        power_card = card_groups[0]
        self.play(
            card_rects[0].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(
                YELLOW, width=3
            ),
            run_time=max(0.05, 0.20),
        )
        power_copy = card_waves[0].copy().set_opacity(1)
        self.add(power_copy)
        self.play(
            power_copy.animate.scale(3.2).move_to(raw_copy_target),
            run_time=max(0.05, 0.55),
        )
        self.play(power_copy.animate.scale(0.4).set_opacity(0), run_time=max(0.05, 0.50))
        self.remove(power_copy)
        self.play(
            card_x_marks[0].animate.set_opacity(1),
            power_card.animate.set_opacity(0.32),
            run_time=max(0.05, 0.51),
        )

        # Beat 23 (31.20-32.68): Eye-blink Artifact
        eye_card = card_groups[1]
        self.play(
            card_rects[1].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(
                YELLOW, width=3
            ),
            run_time=max(0.05, 0.20),
        )
        eye_copy = card_waves[1].copy().set_opacity(1)
        self.add(eye_copy)
        self.play(
            eye_copy.animate.scale(3.0).move_to(raw_copy_target),
            run_time=max(0.05, 0.50),
        )
        self.play(
            eye_copy.animate.scale(0.5).rotate(PI / 18).set_opacity(0),
            run_time=max(0.05, 0.45),
        )
        self.remove(eye_copy)
        self.play(
            card_x_marks[1].animate.set_opacity(1),
            eye_card.animate.set_opacity(0.32),
            run_time=max(0.05, 0.33),
        )

        # Beat 24 (32.68-34.08): Muscle Activity
        muscle_card = card_groups[2]
        self.play(
            card_rects[2].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(
                YELLOW, width=3
            ),
            run_time=max(0.05, 0.18),
        )
        muscle_copy = card_waves[2].copy().set_opacity(1)
        self.add(muscle_copy)
        self.play(
            muscle_copy.animate.scale(3.0).move_to(raw_copy_target),
            run_time=max(0.05, 0.48),
        )
        self.play(muscle_copy.animate.scale(0.5).set_opacity(0), run_time=max(0.05, 0.42))
        self.remove(muscle_copy)
        self.play(
            card_x_marks[2].animate.set_opacity(1),
            muscle_card.animate.set_opacity(0.32),
            run_time=max(0.05, 0.32),
        )

        # Beat 25 (34.08-35.26): Baseline Drift
        drift_card = card_groups[3]
        self.play(
            card_rects[3].animate.set_fill(BLUE_D, opacity=0.55).set_stroke(
                YELLOW, width=3
            ),
            run_time=max(0.05, 0.16),
        )
        drift_copy = card_waves[3].copy().set_opacity(1)
        self.add(drift_copy)
        self.play(
            drift_copy.animate.scale(3.2).move_to(raw_copy_target),
            run_time=max(0.05, 0.40),
        )
        self.play(
            drift_copy.animate.rotate(-PI / 18).set_opacity(0),
            run_time=max(0.05, 0.36),
        )
        self.remove(drift_copy)
        self.play(
            card_x_marks[3].animate.set_opacity(1),
            drift_card.animate.set_opacity(0.32),
            run_time=max(0.05, 0.26),
        )

        # ----------------------------------------------------------------
        # Beat 26 (35.26-36.18): all cards struck/dimmed, clean trace blue
        # ----------------------------------------------------------------
        self.play(
            processed_trace.animate.set_color(BLUE).set_stroke(width=5),
            *[x.animate.set_opacity(1) for x in card_x_marks],
            run_time=max(0.05, 0.92),
        )

        # ----------------------------------------------------------------
        # Beat 27 (36.18-39.32): clean trace center, boxes compact strip
        # ----------------------------------------------------------------
        final_clean_center = np.array([-1.0, 0.20, 0])
        self.play(
            processed_trace_group.animate.move_to(final_clean_center).scale(1.12),
            FadeOut(raw_trace),
            FadeOut(neural_outline),
            FadeOut(neural_magnifier),
            FadeOut(top_segment_lines),
            FadeOut(top_segment_labels),
            run_time=max(0.05, 1.40),
        )

        compact_centers = [
            np.array([-2.55 + i * 0.98, -1.75, 0]) for i in range(6)
        ]
        for group, target in zip(box_groups, compact_centers):
            self.play(
                group.animate.scale(0.72).move_to(target),
                run_time=max(0.05, 1.10 / 6),
            )

        pipeline_strip_label = Text(
            "Preprocessing Pipeline", font_size=18, color=WHITE, weight="BOLD"
        ).move_to(np.array([-1.0, -2.45, 0]))
        self.play(FadeIn(pipeline_strip_label), run_time=max(0.05, 0.64))

        # ----------------------------------------------------------------
        # Beat 28 (39.32-40.34): soft connected path illumination
        # ----------------------------------------------------------------
        connection_lines = VGroup()
        for group in box_groups:
            connection_lines.add(
                Line(
                    group.get_top(),
                    processed_trace.get_bottom() + UP * 0.15,
                    color=GREY_B,
                    stroke_opacity=0.45,
                    stroke_width=2,
                )
            )
        self.play(Create(connection_lines), run_time=max(0.05, 0.62))
        self.play(FadeOut(connection_lines), run_time=max(0.05, 0.40))

        # ----------------------------------------------------------------
        # Beat 29 (40.34-43.60): Filtering box + Power-line card, Earlier Modules
        # ----------------------------------------------------------------
        self.play(
            Indicate(box_groups[0], color=YELLOW, scale_factor=1.10),
            card_rects[0].animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, 0.75),
        )
        magnifier_icon2 = magnifier_icon(YELLOW, scale=0.90).move_to(
            processed_trace.get_center() + LEFT * 3.0 + UP * 0.7
        )
        earlier_modules_label = Text(
            "Earlier Modules", font_size=18, color=GREY_B
        ).move_to(np.array([-1.0, -3.10, 0]))
        self.play(FadeIn(magnifier_icon2), run_time=max(0.05, 0.55))
        self.play(FadeIn(earlier_modules_label), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 1.41))

        # ----------------------------------------------------------------
        # Beat 30 (43.60-44.46): filtering pulse, un-strike/re-strike card
        # ----------------------------------------------------------------
        self.play(
            Indicate(box_groups[0], color=YELLOW, scale_factor=1.12),
            run_time=max(0.05, 0.24),
        )
        flicker = highfreq_overlay.copy().move_to(processed_trace.get_center())
        flicker.set_opacity(0.8)
        self.play(
            card_groups[0].animate.set_opacity(1.0),
            card_x_marks[0].animate.set_opacity(0),
            run_time=max(0.05, 0.18),
        )
        card_groups[0].set_opacity(1.0)
        card_x_marks[0].set_opacity(0)
        self.play(FadeIn(flicker), run_time=max(0.05, 0.08))
        self.play(FadeOut(flicker), run_time=max(0.05, 0.08))
        self.play(
            card_groups[0].animate.set_opacity(0.32),
            card_x_marks[0].animate.set_opacity(1),
            run_time=max(0.05, 0.28),
        )

        # ----------------------------------------------------------------
        # Beat 31 (44.46-45.14): artifacts glow, Artifacts label + arrow
        # ----------------------------------------------------------------
        artifacts_label = Text("Artifacts", font_size=20, color=RED, weight="BOLD")
        artifacts_label.next_to(side_panel_group, DOWN, buff=0.12)
        artifacts_arrow = Arrow(
            side_panel_group.get_bottom(),
            processed_trace.get_center() + LEFT * 2.2 + DOWN * 0.3,
            color=RED,
            stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(
            Indicate(card_groups[1], color=RED, scale_factor=1.08),
            Indicate(card_groups[2], color=PINK, scale_factor=1.08),
            run_time=max(0.05, 0.22),
        )
        self.play(FadeIn(artifacts_label), FadeIn(artifacts_arrow), run_time=max(0.05, 0.46))

        # ----------------------------------------------------------------
        # Beat 32 (45.14-46.40): Signal Cleaning label, sweeping magnifier
        # ----------------------------------------------------------------
        signal_cleaning_label = Text(
            "Signal Cleaning", font_size=26, color=WHITE, weight="BOLD"
        ).move_to(np.array([-1.0, -0.90, 0]))
        soft_highlight = processed_trace.copy().set_stroke(
            BLUE, width=8, opacity=0.25
        )
        soft_highlight.move_to(processed_trace.get_center())
        soft_highlight.set_opacity(0)

        self.play(FadeIn(signal_cleaning_label), run_time=max(0.05, 0.30))
        sweep_left = processed_trace.get_center() + LEFT * 3.0 + UP * 0.8
        sweep_right = processed_trace.get_center() + RIGHT * 3.0 + UP * 0.8
        self.play(
            magnifier_icon2.animate.scale(1.6).move_to(sweep_left),
            run_time=max(0.05, 0.30),
        )
        self.play(magnifier_icon2.animate.move_to(sweep_right), run_time=max(0.05, 0.40))
        self.play(
            FadeIn(soft_highlight),
            magnifier_icon2.animate.scale(1 / 1.6).move_to(
                processed_trace.get_center() + RIGHT * 2.4 + UP * 0.7
            ),
            run_time=max(0.05, 0.26),
        )

        # ----------------------------------------------------------------
        # Beat 33 (46.40-47.17): settle, clean trace pulses once, hold
        # ----------------------------------------------------------------
        self.play(
            Indicate(processed_trace, color=BLUE, scale_factor=1.05),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.37))