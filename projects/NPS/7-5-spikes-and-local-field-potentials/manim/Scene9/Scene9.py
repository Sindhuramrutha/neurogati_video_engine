ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        np.random.seed(7)

        # ---------- helpers ----------
        def make_wave(y_center, amp, n_cycles, color, x_left=-4.3, x_right=3.5,
                      stroke_width=4, opacity=1.0):
            graph = FunctionGraph(
                lambda x: y_center + amp * np.sin(
                    2 * np.pi * n_cycles * (x - x_left) / (x_right - x_left)
                ),
                x_range=[x_left, x_right, 0.02],
                color=color,
                stroke_width=stroke_width,
            )
            graph.set_opacity(opacity)
            return graph

        def make_tissue_blob(center=ORIGIN, rx=4.1, ry=2.55):
            pts = []
            n = 48
            for i in range(n):
                theta = 2 * np.pi * i / n
                rf = (1 + 0.10 * np.sin(3 * theta + 0.4)
                      + 0.06 * np.cos(5 * theta + 1.2)
                      + 0.04 * np.sin(2 * theta + 2.0))
                pts.append(center + np.array([
                    rx * rf * np.cos(theta),
                    ry * rf * np.sin(theta),
                    0,
                ]))
            return Polygon(
                *pts,
                color=WHITE,
                fill_color=BLUE,
                fill_opacity=0.22,
                stroke_width=2,
            )

        def make_neuron(pos):
            soma = Circle(
                radius=0.09,
                fill_color=GREY_B,
                fill_opacity=1,
                stroke_width=0,
            ).move_to(pos)
            dendrites = VGroup()
            for ang in [0.15, np.pi / 2, np.pi, 2.4 * np.pi / 3]:
                dendrites.add(Line(
                    pos,
                    pos + np.array([0.24 * np.cos(ang), 0.24 * np.sin(ang), 0]),
                    color=GREY_B,
                    stroke_width=1.4,
                ))
            return VGroup(soma, dendrites)

        def make_double_arrow(start, end, color=GREY, width=2.5, arc=0.30):
            line = Line(start, end, path_arc=arc, color=color, stroke_width=width)
            line.add_tip(at_start=True)
            line.add_tip(at_start=False)
            return line

        def make_lfp_wave(sd, center_x, center_y, panel_width, phase_shift=0.0):
            x0 = center_x - panel_width / 2 + 0.16
            x1 = center_x + panel_width / 2 - 0.16
            return FunctionGraph(
                lambda x, sd=sd, cy=center_y, ps=phase_shift:
                    cy + sd["lfp_amp"] * np.sin(
                        2 * np.pi * sd["lfp_cycles"] * (x - x0) / (x1 - x0)
                        + sd["lfp_phase"] + ps
                    ),
                x_range=[x0, x1, 0.01],
                color=sd["color"],
                stroke_width=3,
            )

        # ---------- previous-scene remnant ----------
        rem_rect = Rectangle(
            width=9.8, height=5.2,
            stroke_color=GREY_B, stroke_width=3,
            fill_color=GREY, fill_opacity=0.06,
        ).move_to(ORIGIN)
        raw_tick_xs = [12, 18, 25, 40, 55, 70, 82]
        rem_tick_xs = [-4.3 + (x / 90) * 7.8 for x in raw_tick_xs]
        rem_spike_axis = Line([-4.3, 1.2, 0], [3.5, 1.2, 0], color=WHITE, stroke_width=2.5)
        rem_spike_ticks = VGroup(*[
            Line([x, 1.2, 0], [x, 1.75, 0], color=WHITE, stroke_width=3)
            for x in rem_tick_xs
        ])
        rem_lfp_wave = make_wave(-1.15, 0.40, 1.5, ORANGE)
        rem_comp1 = make_wave(-2.0, 0.20, 0.8, ORANGE)
        rem_comp2 = make_wave(-2.6, 0.18, 1.6, TEAL)
        rem_comp3 = make_wave(-3.2, 0.15, 4.5, PURPLE)
        rem_caption = Text(
            "combined spike and LFP analysis",
            font_size=24, color=WHITE, weight=BOLD,
        ).next_to(rem_rect, DOWN, buff=0.25)
        remnant_panel = VGroup(
            rem_rect, rem_spike_axis, rem_spike_ticks,
            rem_lfp_wave, rem_comp1, rem_comp2, rem_comp3, rem_caption,
        )

        # ---------- tissue and neurons ----------
        tissue = make_tissue_blob(ORIGIN)
        neuron_coords = [
            np.array([-2.9, 1.3, 0]),
            np.array([-1.8, 1.9, 0]),
            np.array([-0.8, 2.1, 0]),
            np.array([0.4, 1.6, 0]),
            np.array([1.5, 1.7, 0]),
            np.array([2.6, 0.7, 0]),
            np.array([1.6, -0.5, 0]),
            np.array([0.6, -1.5, 0]),
            np.array([-0.5, -1.7, 0]),
            np.array([-1.6, -1.3, 0]),
            np.array([-2.8, -0.5, 0]),
            np.array([0.0, 0.3, 0]),
        ]
        neuron_group = VGroup(*[make_neuron(pos) for pos in neuron_coords])
        tissue_group = VGroup(tissue, neuron_group)

        neurons_caption = Text(
            "Neurons rarely operate in isolation",
            font_size=32,
            color=WHITE,
            t2c={"rarely": YELLOW},
            t2w={"rarely": BOLD},
        ).to_edge(UP, buff=0.22)

        # ---------- beat 1: 0.00-2.16 ----------
        self.add(remnant_panel)
        self.wait(max(0.05, 0.30))
        self.play(
            FadeOut(remnant_panel),
            FadeIn(tissue),
            FadeIn(neuron_group),
            run_time=max(0.05, 0.80),
        )
        self.play(FadeIn(neurons_caption), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 2.16 - (0.30 + 0.80 + 0.40)))

        # ---------- connections between neurons ----------
        edges = []
        for i in range(len(neuron_coords)):
            for j in range(i + 1, len(neuron_coords)):
                if np.linalg.norm(neuron_coords[i][:2] - neuron_coords[j][:2]) < 2.0:
                    edges.append((i, j))

        connection_lines = VGroup()
        for i, j in edges:
            line = Line(
                neuron_coords[i], neuron_coords[j],
                color=GREY, stroke_width=1.6,
            )
            line.set_stroke(color=GREY, width=1.6, opacity=0.35)
            connection_lines.add(line)

        # clusters
        pop_A_indices = [0, 1, 2, 3, 4]
        pop_B_indices = [6, 7, 8, 9]
        avg_A = np.mean([neuron_coords[i] for i in pop_A_indices], axis=0)
        avg_B = np.mean([neuron_coords[i] for i in pop_B_indices], axis=0)

        halo_a = Ellipse(
            width=3.3, height=1.85,
            color=ORANGE, fill_color=ORANGE, fill_opacity=0.14, stroke_width=1.5,
        ).move_to(avg_A)
        halo_b = Ellipse(
            width=2.95, height=1.75,
            color=TEAL, fill_color=TEAL, fill_opacity=0.14, stroke_width=1.5,
        ).move_to(avg_B)
        pop_a_label = Text("pop. A", font_size=14, color=ORANGE).next_to(halo_a, UP, buff=0.05)
        pop_b_label = Text("pop. B", font_size=14, color=TEAL).next_to(halo_b, UP, buff=0.05)
        local_pop_label = Text(
            "local population",
            font_size=14,
            color=GREY_B,
        ).move_to(tissue.get_center() + np.array([0.0, 0.95, 0.0]))
        clusters_group = VGroup(halo_a, halo_b, local_pop_label, pop_a_label, pop_b_label)

        # ---------- beat 2: 3.18-7.28 ----------
        self.wait(max(0.05, 3.18 - 2.16))  # 1.02

        # connections emerge progressively from 3.86 to 5.08
        self.wait(max(0.05, 3.86 - 3.18))  # 0.68
        n_edges = len(edges)
        per_edge_draw = (5.08 - 3.86) / n_edges
        for line in connection_lines:
            self.play(Create(line), run_time=max(0.05, per_edge_draw))

        # interactions: brighten and pulses
        self.play(
            connection_lines.animate.set_stroke(color=WHITE, width=2.2, opacity=0.85),
            run_time=max(0.05, 0.40),
        )
        pulse_pairs = edges[:4]
        for i, j in pulse_pairs:
            start = neuron_coords[i]
            end = neuron_coords[j]
            dot = Dot(start, radius=0.06, color=YELLOW, fill_opacity=1)
            self.add(dot)
            self.play(dot.animate.move_to(end), run_time=max(0.05, 0.30))
            self.remove(dot)
        self.wait(max(0.05, 6.90 - (5.08 + 0.40 + len(pulse_pairs) * 0.30)))

        # populations become distinct at 6.90
        self.play(
            FadeIn(halo_a),
            FadeIn(halo_b),
            FadeIn(local_pop_label),
            FadeIn(pop_a_label),
            FadeIn(pop_b_label),
            run_time=max(0.05, 0.38),
        )
        self.wait(max(0.05, 7.28 - 6.90 - 0.38))

        # ---------- beat 3: 8.32-10.60 ----------
        self.wait(max(0.05, 8.32 - 7.28))

        self.play(
            FadeOut(neurons_caption),
            tissue_group.animate.set_opacity(0.40),
            connection_lines.animate.set_opacity(0.35),
            clusters_group.animate.set_opacity(0.65),
            run_time=max(0.05, 0.52),
        )

        circuit_label = Text(
            "circuit analysis",
            font_size=36,
            color=WHITE,
            t2c={"analysis": ORANGE},
            t2w={"circuit": BOLD},
        ).to_edge(UP, buff=0.32)

        self.play(
            FadeIn(circuit_label),
            halo_a.animate.set_fill(opacity=0.55).set_stroke(width=2.5),
            halo_b.animate.set_fill(opacity=0.55).set_stroke(width=2.5),
            run_time=max(0.05, 0.60),
        )
        self.wait(max(0.05, 9.54 - 8.84 - 0.60))

        circuit_frame = SurroundingRectangle(
            tissue, color=WHITE, stroke_width=2, buff=0.08,
        )
        self.play(FadeIn(circuit_frame), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 10.14 - 9.54 - 0.50))

        self.play(
            circuit_frame.animate.set_stroke(color=YELLOW, width=4),
            run_time=max(0.05, 0.46),
        )

        # ---------- electrode array data ----------
        site_data = [
            {"num": 1, "letter": "A", "x": 2.3, "y": 1.6, "color": YELLOW,
             "spike_offsets": [-0.38, -0.12, 0.12, 0.32],
             "lfp_amp": 0.13, "lfp_cycles": 3.6, "lfp_phase": 0.3, "prelim_cycles": 3.6},
            {"num": 2, "letter": "B", "x": 3.0, "y": 0.5, "color": TEAL,
             "spike_offsets": [-0.30, 0.03, 0.22, 0.38],
             "lfp_amp": 0.17, "lfp_cycles": 1.5, "lfp_phase": 1.2, "prelim_cycles": 2.8},
            {"num": 3, "letter": "C", "x": 3.7, "y": -0.5, "color": GREEN,
             "spike_offsets": [-0.40, -0.16, 0.10, 0.34],
             "lfp_amp": 0.15, "lfp_cycles": 1.7, "lfp_phase": 2.1, "prelim_cycles": 2.6},
            {"num": 4, "letter": "D", "x": 4.4, "y": -1.6, "color": PURPLE,
             "spike_offsets": [-0.25, 0.02, 0.26, 0.42],
             "lfp_amp": 0.11, "lfp_cycles": 4.0, "lfp_phase": 0.9, "prelim_cycles": 4.0},
        ]

        strip = Rectangle(
            width=2.2, height=5.6,
            fill_color=GREY, fill_opacity=0.08,
            stroke_color=GREY_B, stroke_width=1.5,
        ).move_to(np.array([3.0, 0.0, 0.0]))

        shank_lines = VGroup()
        contact_dots = VGroup()
        contact_labels = VGroup()
        for sd in site_data:
            shank = Line(
                [sd["x"], sd["y"] - 0.55, 0],
                [sd["x"], sd["y"] + 0.55, 0],
                color=WHITE, stroke_width=3,
            )
            dot = Dot([sd["x"], sd["y"], 0], radius=0.07, color=WHITE, fill_opacity=1)
            label = Text(
                f"contact {sd['num']}",
                font_size=11,
                color=WHITE,
            ).next_to(shank, DOWN, buff=0.12)
            shank_lines.add(shank)
            contact_dots.add(dot)
            contact_labels.add(label)

        electrode_strip_group = VGroup(strip, shank_lines, contact_dots, contact_labels)

        phase_tracker = ValueTracker(0)

        def make_prelim_wave(sd, phase):
            x0 = sd["x"] + 0.60
            x1 = x0 + 1.1
            return FunctionGraph(
                lambda x, sd=sd, phase=phase:
                    sd["y"] + 0.12 * np.sin(
                        2 * np.pi * sd["prelim_cycles"] * (x - x0) / (x1 - x0)
                        + phase + sd["lfp_phase"]
                    ),
                x_range=[x0, x1, 0.01],
                color=WHITE,
                stroke_width=2.5,
            )

        prelim_waves = VGroup(*[
            always_redraw(
                lambda sd=sd, tr=phase_tracker: make_prelim_wave(sd, tr.get_value())
            )
            for sd in site_data
        ])

        drop_lines = VGroup()
        site_labels = VGroup()
        for sd in site_data:
            tip = np.array([sd["x"], sd["y"], 0])
            label_pos = np.array([sd["x"] + 0.05, sd["y"] - 1.05, 0])
            site_label = Text(
                f"site {sd['letter']}",
                font_size=13,
                color=GREY_B,
            ).move_to(label_pos)
            dashed = DashedLine(
                tip, label_pos,
                color=GREY, stroke_width=1.5, dash_length=0.07,
            )
            drop_lines.add(dashed)
            site_labels.add(site_label)

        simul_label = Text(
            "simultaneously",
            font_size=20,
            color=YELLOW,
        ).move_to(np.array([3.35, -2.95, 0]))
        time_axis = Line(
            [2.0, -3.15, 0],
            [4.7, -3.15, 0],
            color=GREY_B, stroke_width=2,
        )
        clock_dot = Dot([2.0, -3.15, 0], radius=0.05, color=YELLOW, fill_opacity=1)

        # ---------- beat 4: 11.30-16.84 ----------
        self.wait(max(0.05, 11.30 - 10.60))

        tissue_view_group = VGroup(
            tissue, neuron_group, connection_lines, clusters_group, circuit_frame,
        )
        self.play(
            tissue_view_group.animate.scale(0.5).move_to(
                np.array([-4.55, 0.25, 0])
            ),
            FadeOut(circuit_label),
            FadeIn(electrode_strip_group),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 12.84 - 11.30 - 1.00))

        for dot in contact_dots:
            self.play(dot.animate.set_color(YELLOW), run_time=max(0.05, 0.20))
            self.wait(max(0.05, 0.18))
        self.wait(max(0.05, 14.38 - 12.84 - 4 * 0.38))

        self.play(FadeIn(prelim_waves), run_time=max(0.05, 0.40))
        self.play(
            phase_tracker.animate.set_value(4 * np.pi),
            run_time=max(0.05, 1.04),
            rate_func=linear,
        )

        self.play(
            Create(drop_lines),
            FadeIn(site_labels),
            run_time=max(0.05, 0.50),
        )

        self.play(
            FadeIn(simul_label),
            Create(time_axis),
            run_time=max(0.05, 0.20),
        )
        self.play(clock_dot.animate.move_to([4.7, -3.15, 0]), run_time=max(0.05, 0.32))

        # ---------- compact per-site spike + LFP panels ----------
        old_panel_bgs = VGroup()
        old_spike_all = VGroup()
        old_lfp_all = VGroup()
        selected_ticks = []
        panel_cx = 5.5
        panel_width = 1.45

        for sd in site_data:
            px = panel_cx
            py = sd["y"]
            panel_bg = Rectangle(
                width=panel_width, height=0.98,
                stroke_color=GREY_B, stroke_width=1,
                fill_color=GREY, fill_opacity=0.07,
            ).move_to([px, py, 0])
            spike_y = py + 0.22
            spike_axis = Line(
                [px - 0.50, spike_y, 0],
                [px + 0.50, spike_y, 0],
                color=GREY_B, stroke_width=2,
            )
            spike_ticks = VGroup(*[
                Line(
                    [px + off * 1.2, spike_y, 0],
                    [px + off * 1.2, spike_y + 0.22, 0],
                    color=WHITE, stroke_width=2.5,
                )
                for off in sd["spike_offsets"]
            ])
            site_spike = VGroup(spike_axis, spike_ticks)
            lfp_wave = make_lfp_wave(
                sd, center_x=px, center_y=py - 0.28,
                panel_width=panel_width,
            )
            old_panel_bgs.add(panel_bg)
            old_spike_all.add(site_spike)
            old_lfp_all.add(lfp_wave)
            selected_ticks.append(spike_ticks[1] if len(spike_ticks) > 1 else spike_ticks[0])

        selected_ticks_group = VGroup(*selected_ticks)

        # ---------- beat 5: 18.04-20.38 ----------
        self.wait(max(0.05, 18.04 - 16.84))

        self.play(
            FadeOut(prelim_waves),
            FadeOut(simul_label),
            FadeOut(time_axis),
            FadeOut(clock_dot),
            FadeOut(contact_labels),
            FadeIn(old_panel_bgs),
            FadeIn(old_spike_all),
            FadeIn(old_lfp_all),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 19.50 - 18.04 - 0.80))

        self.play(
            old_spike_all.animate.set_color(YELLOW).set_stroke(width=4),
            run_time=max(0.05, 0.40),
        )
        for tick in selected_ticks_group:
            self.play(
                Indicate(tick, color=YELLOW, scale_factor=1.35),
                run_time=max(0.05, 0.12),
            )

        # ---------- beat 6: 21.04-22.00 ----------
        self.wait(max(0.05, 21.04 - 20.38))
        self.wait(max(0.05, 21.38 - 21.04))
        self.play(
            old_lfp_all.animate.set_color(YELLOW).set_stroke(width=5),
            run_time=max(0.05, 0.62),
        )

        # ---------- build common aligned panels ----------
        common_panel_bgs = VGroup()
        common_spike_target = VGroup()
        common_lfp_target = VGroup()
        common_xs = [-3.9, -1.3, 1.3, 3.9]
        common_y = -2.75
        common_width = 1.6

        for sd, cx in zip(site_data, common_xs):
            panel_bg = Rectangle(
                width=common_width, height=0.98,
                stroke_color=GREY_B, stroke_width=1,
                fill_color=GREY, fill_opacity=0.07,
            ).move_to([cx, common_y, 0])
            spike_y = common_y + 0.22
            spike_axis = Line(
                [cx - 0.55, spike_y, 0],
                [cx + 0.55, spike_y, 0],
                color=GREY_B, stroke_width=2,
            )
            spike_ticks = VGroup(*[
                Line(
                    [cx + off * 1.2, spike_y, 0],
                    [cx + off * 1.2, spike_y + 0.22, 0],
                    color=WHITE, stroke_width=2.5,
                )
                for off in sd["spike_offsets"]
            ])
            common_spike_target.add(VGroup(spike_axis, spike_ticks))
            common_lfp_target.add(
                make_lfp_wave(
                    sd,
                    center_x=cx,
                    center_y=common_y - 0.28,
                    panel_width=common_width,
                )
            )
            common_panel_bgs.add(panel_bg)

        site_positions = [np.array([sd["x"], sd["y"], 0]) for sd in site_data]
        site_arrows = VGroup(
            make_double_arrow(site_positions[0], site_positions[1]),
            make_double_arrow(site_positions[1], site_positions[2]),
            make_double_arrow(site_positions[2], site_positions[3]),
        )

        group_ab = VGroup(shank_lines[0], shank_lines[1])
        group_cd = VGroup(shank_lines[2], shank_lines[3])
        region_rect_1 = SurroundingRectangle(group_ab, color=ORANGE, buff=0.2, stroke_width=2)
        region_rect_2 = SurroundingRectangle(group_cd, color=TEAL, buff=0.2, stroke_width=2)
        region_labels = VGroup(
            Text("region 1", font_size=18, color=ORANGE).next_to(region_rect_1, LEFT, buff=0.12),
            Text("region 2", font_size=18, color=TEAL).next_to(region_rect_2, LEFT, buff=0.12),
        )
        region_arrow = Line(
            region_rect_1.get_center(),
            region_rect_2.get_center(),
            color=WHITE, stroke_width=5,
        )
        region_arrow.add_tip(at_start=True)
        region_arrow.add_tip(at_start=False)

        shank_highlights = VGroup(*[
            SurroundingRectangle(shank, color=WHITE, buff=0.10, stroke_width=1.5)
            for shank in shank_lines
        ])

        # ---------- beat 7: 22.54-26.62 ----------
        self.wait(max(0.05, 22.54 - 22.00))

        self.play(
            self.camera.frame.animate.scale(1.15),
            Create(site_arrows),
            run_time=max(0.05, 0.84),
        )

        self.play(
            FadeOut(old_panel_bgs),
            FadeIn(common_panel_bgs),
            Transform(old_spike_all, common_spike_target),
            run_time=max(0.05, 0.68),
        )

        self.play(
            Transform(old_lfp_all, common_lfp_target),
            run_time=max(0.05, 0.54),
        )

        self.play(
            site_arrows.animate.set_color(YELLOW).set_stroke(width=4, opacity=1),
            run_time=max(0.05, 0.60),
        )
        self.play(
            site_arrows.animate.scale(1.08, about_point=site_arrows.get_center()),
            run_time=max(0.05, 0.35),
        )
        self.play(
            site_arrows.animate.scale(1 / 1.08, about_point=site_arrows.get_center()),
            run_time=max(0.05, 0.35),
        )

        self.play(
            FadeIn(region_rect_1),
            FadeIn(region_rect_2),
            FadeIn(region_labels),
            Create(region_arrow),
            run_time=max(0.05, 0.72),
        )

        # ---------- beat 8: 26.62-29.14 ----------
        multi_label = Text(
            "multiple recording locations",
            font_size=26,
            color=WHITE,
            weight=BOLD,
        ).move_to(np.array([0.0, 3.25, 0.0]))
        self.play(
            FadeIn(multi_label),
            self.camera.frame.animate.scale(1.10),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 28.02 - 26.62 - 1.00))
        self.play(FadeIn(shank_highlights), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 29.14 - 28.02 - 0.50))

        # ---------- beat 9: 29.14-33.08 ----------
        self.wait(max(0.05, 29.78 - 29.14))

        researcher_head = Circle(
            radius=0.16, fill_color=PINK, fill_opacity=1, stroke_width=0,
        ).move_to(np.array([6.1, -3.0, 0]))
        researcher_body = Polygon(
            [6.1, -3.25, 0],
            [5.85, -3.70, 0],
            [6.35, -3.70, 0],
            fill_color=PINK, fill_opacity=1, stroke_width=0,
        )
        researcher_notepad = Rectangle(
            width=0.32, height=0.42,
            fill_color=WHITE, fill_opacity=1, stroke_width=0,
        ).move_to(np.array([6.35, -3.45, 0]))
        researcher_icon = VGroup(researcher_head, researcher_body, researcher_notepad)
        researcher_icon.scale_to_fit_width(0.75)

        self.play(FadeIn(researcher_icon), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.24))
        self.play(FadeOut(researcher_icon), run_time=max(0.05, 0.35))

        tissue_targets = [
            tissue_view_group.get_center() + np.array([-1.4, 1.0, 0]),
            tissue_view_group.get_center() + np.array([-0.6, 0.55, 0]),
            tissue_view_group.get_center() + np.array([-0.6, -0.45, 0]),
            tissue_view_group.get_center() + np.array([-1.4, -1.0, 0]),
        ]
        initial_site_links = VGroup(*[
            DashedLine(
                contact_dots[i].get_center(),
                tissue_targets[i],
                color=GREY,
                stroke_width=2,
                dash_length=0.07,
            )
            for i in range(4)
        ])
        self.play(Create(initial_site_links), run_time=max(0.05, 0.88))

        self.play(
            halo_a.animate.set_fill(opacity=0.55).set_stroke(width=3),
            halo_b.animate.set_fill(opacity=0.55).set_stroke(width=3),
            run_time=max(0.05, 0.40),
        )

        pop_a_links = VGroup(
            DashedLine(
                halo_a.get_center(),
                contact_dots[0].get_center(),
                color=ORANGE, stroke_width=2, dash_length=0.06,
            ),
            DashedLine(
                halo_a.get_center(),
                contact_dots[1].get_center(),
                color=ORANGE, stroke_width=2, dash_length=0.06,
            ),
        )
        pop_b_links = VGroup(
            DashedLine(
                halo_b.get_center(),
                contact_dots[2].get_center(),
                color=TEAL, stroke_width=2, dash_length=0.06,
            ),
            DashedLine(
                halo_b.get_center(),
                contact_dots[3].get_center(),
                color=TEAL, stroke_width=2, dash_length=0.06,
            ),
        )
        self.play(
            FadeIn(pop_a_links),
            FadeIn(pop_b_links),
            FadeOut(initial_site_links),
            run_time=max(0.05, 0.40),
        )

        for link_group in [pop_a_links, pop_b_links]:
            for link in link_group:
                pulse_dot = Dot(link.get_start(), radius=0.05, color=WHITE, fill_opacity=1)
                self.add(pulse_dot)
                self.play(pulse_dot.animate.move_to(link.get_end()), run_time=max(0.05, 0.16))
                self.remove(pulse_dot)

        # ---------- beats 10-11: 33.08-36.55 ----------
        self.wait(max(0.05, 33.88 - 33.08))

        self.play(
            self.camera.frame.animate.scale(1.10),
            run_time=max(0.05, 0.54),
        )

        network_label = Text(
            "network-level phenomena",
            font_size=28,
            color=YELLOW,
            weight=BOLD,
        ).move_to(np.array([0.0, -3.45, 0.0]))
        self.play(FadeIn(network_label), run_time=max(0.05, 0.48))

        pulse_items = [
            site_arrows,
            pop_a_links,
            pop_b_links,
            old_spike_all,
            old_lfp_all,
        ]
        for item in pulse_items:
            self.play(Indicate(item, color=YELLOW, scale_factor=1.07), run_time=max(0.05, 0.08))

        final_caption = Text(
            "multiple recording sites for circuit analysis",
            font_size=24,
            color=WHITE,
            t2c={"circuit analysis": YELLOW},
        ).move_to(np.array([0.0, 3.25, 0.0]))
        self.play(
            FadeOut(multi_label),
            FadeIn(final_caption),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 0.20))

        final_active = VGroup(
            tissue_view_group,
            electrode_strip_group,
            drop_lines,
            site_labels,
            site_arrows,
            region_rect_1,
            region_rect_2,
            region_labels,
            region_arrow,
            common_panel_bgs,
            old_spike_all,
            old_lfp_all,
            pop_a_links,
            pop_b_links,
            shank_highlights,
            network_label,
            final_caption,
        )
        self.play(FadeOut(final_active), run_time=max(0.05, 0.60))