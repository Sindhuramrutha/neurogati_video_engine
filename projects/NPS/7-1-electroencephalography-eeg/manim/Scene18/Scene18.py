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


class Scene18(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # helpers
        # ------------------------------------------------------------------
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

        def spike_wave_signal(u):
            y = 0.12 * np.sin(2 * np.pi * 1.5 * u)
            y += 1.4 * np.exp(-((u + 0.4) / 0.06) ** 2)
            y += 1.5 * np.exp(-((u - 0.4) / 0.06) ** 2)
            y += 0.35 * np.sin(2 * np.pi * 3.0 * (u - 0.5)) * np.exp(-((u - 0.5) / 0.25) ** 2)
            y += 0.35 * np.sin(2 * np.pi * 3.0 * (u + 0.5)) * np.exp(-((u + 0.5) / 0.25) ** 2)
            return y

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

        def make_app_panel(label_text, content_mob, accent):
            rect = Rectangle(width=2.8, height=0.95, fill_color=BLACK, fill_opacity=0.6,
                             stroke_color=accent, stroke_width=2)
            label = Text(label_text, font_size=13, color=WHITE)
            content = VGroup(label, content_mob).arrange(DOWN, buff=0.08)
            content.scale_to_fit_width(2.4)
            content.move_to(rect.get_center())
            return VGroup(rect, content)

        def pulse_at(point, color=RED, duration=0.3, radius=0.07):
            dot = Circle(radius=radius, fill_color=color, fill_opacity=0.9, stroke_width=0)
            dot.move_to(point)
            d1 = max(0.05, duration * 0.4)
            d2 = max(0.05, duration - d1)
            self.play(GrowFromCenter(dot), run_time=max(0.05, d1))
            self.play(dot.animate.scale(2.5).set_opacity(0), run_time=max(0.05, d2))
            self.remove(dot)

        def synchronized_wave(nodes, color, count, duration):
            rng_wave = np.random.default_rng(int(10_000_000 + duration * 50 + count))
            chosen = rng_wave.choice(len(nodes), size=min(count, len(nodes)), replace=False)
            circles = VGroup()
            for i in chosen:
                c = Circle(radius=0.07, fill_color=color, fill_opacity=0.9, stroke_width=0)
                c.move_to(nodes[i].get_center())
                circles.add(c)
            d1 = max(0.05, duration * 0.7)
            d2 = max(0.05, duration - d1)
            self.play(
                LaggedStart(*[GrowFromCenter(c) for c in circles], lag_ratio=0.03),
                run_time=max(0.05, d1),
            )
            self.play(*[c.animate.scale(2.5).set_opacity(0) for c in circles], run_time=max(0.05, d2))
            self.remove(*circles)

        def propagate(start_node, end_node, color=BLUE, duration=0.3):
            dot = Dot(radius=0.05, color=color)
            dot.move_to(start_node.get_center())
            d1 = max(0.05, duration * 0.2)
            d2 = max(0.05, duration - d1)
            self.play(GrowFromCenter(dot), run_time=max(0.05, d1))
            self.play(dot.animate.move_to(end_node.get_center()).set_opacity(0), run_time=max(0.05, d2))
            self.remove(dot)

        # ------------------------------------------------------------------
        # opening composition (continued from Scene 17)
        # ------------------------------------------------------------------
        map_shapes = make_world_map_shapes()
        rng_dots = np.random.default_rng(7)
        regions = [
            (-4.2, -2.5, 1.5, 2.8, 20),
            (-3.0, -1.8, 0.2, 1.5, 12),
            (-3.2, -1.8, -2.4, -0.3, 18),
            (-0.4, 1.2, 1.4, 2.4, 18),
            (-0.5, 1.3, -2.3, 0.9, 35),
            (1.5, 5.0, 0.8, 3.1, 55),
            (4.3, 5.5, -2.6, -1.7, 12),
        ]
        dot_mobjects = []
        for x_min, x_max, y_min, y_max, count in regions:
            for _ in range(count):
                x = rng_dots.uniform(x_min, x_max)
                y = rng_dots.uniform(y_min, y_max)
                dot = Circle(radius=0.035, fill_color=ORANGE, fill_opacity=0.6, stroke_width=0)
                dot.move_to(np.array([x, y, 0.0]))
                dot_mobjects.append(dot)
        world_map = VGroup(map_shapes, *dot_mobjects)
        world_map.scale_to_fit_height(4.8)
        world_map.shift(LEFT * 2 + DOWN * 1.1)
        world_map.set_opacity(0.3)

        brain_svg = SVGMobject(ASSET_PATHS["brain"])
        brain_svg.set_stroke(GREY_B, width=2).set_fill(GREY_B, opacity=0.22)
        brain_svg.scale_to_fit_height(3.0)
        brain_start = VGroup(brain_svg).scale(0.4)
        brain_start.move_to(RIGHT * 5.3 + UP * 2.4)

        old_brain_pulses = VGroup()
        for _ in range(6):
            px = brain_start.get_x() + np.random.uniform(-0.4, 0.4)
            py = brain_start.get_y() + np.random.uniform(-0.4, 0.4)
            c = Circle(radius=0.05, fill_color=RED, fill_opacity=0.45, stroke_width=0)
            c.move_to(np.array([px, py, 0.0]))
            old_brain_pulses.add(c)

        eeg_trace_start = make_trace(
            epilepsy_spike_signal,
            width=10.0,
            height=1.15,
            color=YELLOW,
            stroke_width=4,
        )
        eeg_trace_start.move_to(LEFT * 2 + UP * 0.35)

        panel_positions = [
            np.array([-3.0, -1.5, 0.0]),
            np.array([3.0, -1.5, 0.0]),
            np.array([-3.0, -2.7, 0.0]),
            np.array([3.0, -2.7, 0.0]),
        ]
        mini_spike = make_trace(epilepsy_spike_signal, width=1.3, height=0.35, color=YELLOW, stroke_width=2)
        panel1 = make_app_panel("Seizure Type Identification", mini_spike, ORANGE)
        panel1.move_to(panel_positions[0])

        mini_brain2 = SVGMobject(ASSET_PATHS["brain"])
        mini_brain2.set_fill(GREY_B, opacity=0.25).set_stroke(GREY_B, width=1)
        mini_brain2.scale_to_fit_height(0.5)
        focus2 = Circle(radius=0.07, fill_color=RED, fill_opacity=1, stroke_width=0)
        focus2.move_to(mini_brain2.get_center() + LEFT * 0.2 + UP * 0.1)
        panel2 = make_app_panel("Brain Region Localisation", VGroup(mini_brain2, focus2), RED)
        panel2.move_to(panel_positions[1])

        descending_line = Line(LEFT * 0.6 + UP * 0.15, RIGHT * 0.6 + DOWN * 0.15, color=GREEN, stroke_width=3)
        check_mark3 = Text("✓", font_size=16, color=GREEN).next_to(descending_line, RIGHT, buff=0.1)
        panel3 = make_app_panel("Treatment Monitoring", VGroup(descending_line, check_mark3), GREEN)
        panel3.move_to(panel_positions[2])

        mini_brain4 = SVGMobject(ASSET_PATHS["brain"])
        mini_brain4.set_fill(GREY_B, opacity=0.25).set_stroke(GREY_B, width=1)
        mini_brain4.scale_to_fit_height(0.5)
        crosshair_h = Line(mini_brain4.get_left() + RIGHT * 0.2, mini_brain4.get_right() + LEFT * 0.2, color=BLUE, stroke_width=2)
        crosshair_v = Line(mini_brain4.get_bottom() + UP * 0.2, mini_brain4.get_top() + DOWN * 0.2, color=BLUE, stroke_width=2)
        panel4 = make_app_panel("Surgical Planning", VGroup(mini_brain4, crosshair_h, crosshair_v), BLUE)
        panel4.move_to(panel_positions[3])

        app_panels = VGroup(panel1, panel2, panel3, panel4)

        self.add(world_map, brain_start, old_brain_pulses, eeg_trace_start, app_panels)

        # ------------------------------------------------------------------
        # beat 1: 0.00 - 1.48
        # ------------------------------------------------------------------
        self.play(
            FadeOut(world_map),
            FadeOut(app_panels),
            eeg_trace_start.animate.scale(0.4).move_to(RIGHT * 5.5 + UP * 0.2).set_opacity(0),
            brain_start.animate.scale(2.0).move_to(UP * 2.5).set_opacity(1),
            FadeOut(old_brain_pulses),
            run_time=max(0.05, 1.48),
        )

        # ------------------------------------------------------------------
        # beat 2: 1.48 - 2.96
        # ------------------------------------------------------------------
        # definition text constructed as separate pieces to allow later highlighting
        phrase_neurological = Text("neurological disorder", font_size=27, color=ORANGE, weight="BOLD")
        phrase_recurrent = Text("recurrent seizures", font_size=27, color=ORANGE, weight="BOLD")
        phrase_abnormal = Text("abnormal electrical activity", font_size=27, color=ORANGE, weight="BOLD")

        line1 = VGroup(
            Text("Epilepsy = ", font_size=27, color=GREY_B),
            phrase_neurological,
            Text(" characterized by", font_size=27, color=GREY_B),
        ).arrange(RIGHT, buff=0.08)

        line2 = VGroup(
            phrase_recurrent,
            Text(" caused by ", font_size=27, color=GREY_B),
            phrase_abnormal,
        ).arrange(RIGHT, buff=0.08)

        line3 = Text("within the brain.", font_size=27, color=GREY_B)

        def_text = VGroup(line1, line2, line3).arrange(DOWN, buff=0.2)
        def_text.scale_to_fit_width(9.8)

        def_rect = Rectangle(width=11.0, height=2.0, fill_color=BLACK, fill_opacity=0.55,
                              stroke_color=WHITE, stroke_width=1.5)
        def_text.move_to(def_rect.get_center())
        def_box = VGroup(def_rect, def_text).move_to(DOWN * 0.4)

        self.play(FadeIn(def_box), run_time=max(0.05, 1.48))

        # brain pulse spots for later beats
        def spot_in_brain(brain_mob, fx, fy):
            x = brain_mob.get_left()[0] + fx * (brain_mob.get_right()[0] - brain_mob.get_left()[0])
            y = brain_mob.get_bottom()[1] + fy * (brain_mob.get_top()[1] - brain_mob.get_bottom()[1])
            return np.array([x, y, 0.0])

        spot1 = spot_in_brain(brain_start, 0.35, 0.60)
        spot2 = spot_in_brain(brain_start, 0.70, 0.55)
        spot3 = spot_in_brain(brain_start, 0.30, 0.30)
        spot4 = spot_in_brain(brain_start, 0.60, 0.40)
        spot5 = spot_in_brain(brain_start, 0.45, 0.70)

        # ------------------------------------------------------------------
        # beat 3: 2.96 - 4.28
        # ------------------------------------------------------------------
        pulse_at(spot1, color=RED, duration=0.60)
        self.play(phrase_recurrent.animate.set_color(RED), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.32))

        # ------------------------------------------------------------------
        # beat 4: 4.28 - 6.30
        # ------------------------------------------------------------------
        pulse_at(spot2, color=RED, duration=0.45)
        pulse_at(spot3, color=RED, duration=0.45)
        self.play(phrase_abnormal.animate.set_color(RED), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------------
        # beat 5: 6.30 - 7.60
        # ------------------------------------------------------------------
        pulse_at(spot4, color=RED, duration=0.35)
        pulse_at(spot5, color=RED, duration=0.35)
        small_abnormal_label = Text(
            "Abnormal electrical activity within the brain.",
            font_size=20,
            color=ORANGE,
        )
        small_abnormal_label.next_to(def_box, DOWN, buff=0.35)
        self.play(FadeIn(small_abnormal_label), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.25))

        # ------------------------------------------------------------------
        # beat 6: 7.60 - 8.56
        # ------------------------------------------------------------------
        normal_label = Text("Normal Conditions", font_size=24, color=WHITE)
        normal_rect = Rectangle(width=10, height=2.0, fill_color=BLACK, fill_opacity=0.55,
                                stroke_color=BLUE, stroke_width=2)
        normal_label.move_to(normal_rect.get_top() + DOWN * 0.4)
        normal_panel = VGroup(normal_rect, normal_label).move_to(UP * 1.2)

        epilepsy_label = Text("Epilepsy", font_size=24, color=WHITE)
        epilepsy_rect = Rectangle(width=10, height=2.0, fill_color=BLACK, fill_opacity=0.55,
                                  stroke_color=ORANGE, stroke_width=2)
        epilepsy_label.move_to(epilepsy_rect.get_top() + DOWN * 0.4)
        epilepsy_panel = VGroup(epilepsy_rect, epilepsy_label).move_to(DOWN * 1.2)

        self.play(
            FadeOut(brain_start),
            FadeOut(def_box),
            FadeOut(small_abnormal_label),
            FadeIn(normal_panel),
            FadeIn(epilepsy_panel),
            run_time=max(0.05, 0.96),
        )

        # ------------------------------------------------------------------
        # beat 7: 8.56 - 10.18  (top normal network)
        # ------------------------------------------------------------------
        rng_net = np.random.default_rng(512)
        num_nodes = 22
        normal_nodes = VGroup()
        node_positions = []
        for _ in range(num_nodes):
            x = rng_net.uniform(normal_rect.get_left()[0] + 0.5, normal_rect.get_right()[0] - 0.5)
            y = rng_net.uniform(normal_rect.get_bottom()[1] + 0.4, normal_rect.get_top()[1] - 0.7)
            node = Circle(radius=0.07, fill_color=BLUE, fill_opacity=0.7, stroke_width=0)
            node.move_to(np.array([x, y, 0.0]))
            normal_nodes.add(node)
            node_positions.append(np.array([x, y, 0.0]))

        normal_edges = VGroup()
        edge_pairs = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if np.linalg.norm(node_positions[i] - node_positions[j]) < 1.9:
                    edge = Line(node_positions[i], node_positions[j], color=BLUE, stroke_width=1.2,
                                stroke_opacity=0.35)
                    normal_edges.add(edge)
                    edge_pairs.append((normal_nodes[i], normal_nodes[j]))

        organized_label = Text("Organized electrical activity", font_size=20, color=BLUE)
        organized_label.next_to(normal_panel, DOWN, buff=0.12)

        self.play(Create(normal_edges), FadeIn(normal_nodes), run_time=max(0.05, 0.72))
        self.play(FadeIn(organized_label), run_time=max(0.05, 0.30))
        for _ in range(3):
            chosen_node = normal_nodes[int(rng_net.integers(0, num_nodes))]
            pulse_at(chosen_node.get_center(), color=BLUE, duration=0.20, radius=0.06)

        # ------------------------------------------------------------------
        # beat 8: 10.18 - 12.78  (top propagation continues)
        # ------------------------------------------------------------------
        for _ in range(4):
            if edge_pairs:
                n1, n2 = edge_pairs[int(rng_net.integers(0, len(edge_pairs)))]
                propagate(n1, n2, color=BLUE, duration=0.45)
        for _ in range(2):
            chosen_node = normal_nodes[int(rng_net.integers(0, num_nodes))]
            pulse_at(chosen_node.get_center(), color=BLUE, duration=0.20, radius=0.06)
        self.wait(max(0.05, 0.40))

        # gap 12.78 - 13.58
        self.wait(max(0.05, 0.80))

        # ------------------------------------------------------------------
        # beat 9: 13.58 - 14.76  (bottom starts)
        # ------------------------------------------------------------------
        rng_bottom = np.random.default_rng(912)
        num_bottom = 22
        bottom_nodes = VGroup()
        bottom_positions = []
        for _ in range(num_bottom):
            x = rng_bottom.uniform(epilepsy_rect.get_left()[0] + 0.5, epilepsy_rect.get_right()[0] - 0.5)
            y = rng_bottom.uniform(epilepsy_rect.get_bottom()[1] + 0.4, epilepsy_rect.get_top()[1] - 0.7)
            node = Circle(radius=0.07, fill_color=ORANGE, fill_opacity=0.35, stroke_width=0)
            node.move_to(np.array([x, y, 0.0]))
            bottom_nodes.add(node)
            bottom_positions.append(np.array([x, y, 0.0]))

        bottom_edges = VGroup()
        for i in range(num_bottom):
            for j in range(i + 1, num_bottom):
                if np.linalg.norm(bottom_positions[i] - bottom_positions[j]) < 1.9:
                    edge = Line(bottom_positions[i], bottom_positions[j], color=ORANGE,
                                stroke_width=1.2, stroke_opacity=0.20)
                    bottom_edges.add(edge)

        self.play(
            epilepsy_rect.animate.set_stroke(ORANGE, width=3, opacity=0.9).set_fill(BLACK, opacity=0.65),
            FadeIn(bottom_edges),
            FadeIn(bottom_nodes),
            run_time=max(0.05, 0.55),
        )
        for _ in range(2):
            chosen_node = bottom_nodes[int(rng_bottom.integers(0, num_bottom))]
            pulse_at(chosen_node.get_center(), color=ORANGE, duration=0.25, radius=0.06)
        self.wait(max(0.05, 0.13))

        # ------------------------------------------------------------------
        # beat 10: 14.76 - 16.66  (bottom more intense)
        # ------------------------------------------------------------------
        for _ in range(5):
            chosen_node = bottom_nodes[int(rng_bottom.integers(0, num_bottom))]
            pulse_at(chosen_node.get_center(), color=RED, duration=0.30, radius=0.07)
        self.wait(max(0.05, 0.40))

        # ------------------------------------------------------------------
        # beat 11: 16.66 - 19.30  (synchronized waves)
        # ------------------------------------------------------------------
        excess_label = Text("Excessive, synchronized firing", font_size=20, color=RED)
        excess_label.next_to(epilepsy_panel, DOWN, buff=0.12)

        synchronized_wave(bottom_nodes, RED, 7, 0.60)
        synchronized_wave(bottom_nodes, RED, 8, 0.60)
        synchronized_wave(bottom_nodes, RED, 7, 0.60)
        self.play(FadeIn(excess_label), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.49))

        # ------------------------------------------------------------------
        # beat 12: 19.30 - 20.92  (distinct synchronized groups)
        # ------------------------------------------------------------------
        synchronized_wave(bottom_nodes, ORANGE, 5, 0.45)
        synchronized_wave(bottom_nodes, RED, 6, 0.45)
        chosen_top = normal_nodes[int(rng_net.integers(0, num_nodes))]
        pulse_at(chosen_top.get_center(), color=BLUE, duration=0.25, radius=0.06)
        self.wait(max(0.05, 0.47))

        # ------------------------------------------------------------------
        # beat 13: 20.92 - 22.48  (pulse then fade away)
        # ------------------------------------------------------------------
        top_comparison = VGroup(normal_panel, normal_edges, normal_nodes, organized_label)
        bottom_comparison = VGroup(epilepsy_panel, bottom_edges, bottom_nodes, excess_label)

        self.play(
            top_comparison.animate.scale(1.03),
            bottom_comparison.animate.scale(1.05),
            run_time=max(0.05, 0.40),
        )
        self.play(
            top_comparison.animate.scale(1 / 1.03),
            bottom_comparison.animate.scale(1 / 1.05),
            run_time=max(0.05, 0.40),
        )
        self.play(FadeOut(top_comparison), FadeOut(bottom_comparison), run_time=max(0.05, 0.76))

        # ------------------------------------------------------------------
        # beat 14: 22.48 - 25.38  (new brain map)
        # ------------------------------------------------------------------
        brain_map = SVGMobject(ASSET_PATHS["brain"])
        brain_map.set_color(GREY_B).set_fill(opacity=0)
        brain_map.scale_to_fit_height(4.0)
        brain_map.move_to(ORIGIN)

        def make_burst(center, size=0.35, color=RED, count=5):
            burst = VGroup()
            rng_burst = np.random.default_rng(int(abs(center[0] * 1000 + center[1] * 1000)) % 100000)
            for _ in range(count):
                ox = rng_burst.uniform(-size, size)
                oy = rng_burst.uniform(-size, size)
                c = Circle(radius=0.09, fill_color=color, fill_opacity=0.9, stroke_width=0)
                c.move_to(center + np.array([ox, oy, 0.0]))
                burst.add(c)
            return burst

        # temporal lobe burst (lower left of brain)
        burst_temporal = make_burst(brain_map.get_center() + LEFT * 0.9 + DOWN * 0.4, size=0.35, color=RED, count=6)
        # frontal lobe burst (upper right)
        burst_frontal = make_burst(brain_map.get_center() + RIGHT * 0.7 + UP * 0.8, size=0.40, color=ORANGE, count=7)

        distinctive_label = Text("Distinctive electrical patterns", font_size=22, color=RED)
        distinctive_label.next_to(brain_map, DOWN, buff=0.3)

        self.play(GrowFromCenter(brain_map), run_time=max(0.05, 0.80))
        self.play(FadeIn(burst_temporal), FadeIn(burst_frontal), run_time=max(0.05, 0.70))
        self.play(Write(distinctive_label), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.90))

        brain_map_group = VGroup(brain_map, burst_temporal, burst_frontal, distinctive_label)

        # ------------------------------------------------------------------
        # beat 15: 25.38 - 28.50  (EEG appears right, brain shifts left)
        # ------------------------------------------------------------------
        left_brain_group = VGroup(brain_map, burst_temporal, burst_frontal)
        observed_label = Text("Observed in EEG recordings", font_size=22, color=YELLOW)
        observed_label.next_to(brain_map, DOWN, buff=0.3)

        eeg_right = make_trace(
            spike_wave_signal,
            width=5.4,
            height=1.3,
            color=YELLOW,
            stroke_width=3,
        )
        eeg_right.move_to(RIGHT * 3.2 + DOWN * 0.4)

        right_peak1 = Circle(radius=0.11, fill_color=RED, fill_opacity=0.85, stroke_width=0)
        right_peak1.move_to(eeg_right.get_center() + LEFT * 1.2 + UP * 0.5)
        right_peak2 = Circle(radius=0.11, fill_color=RED, fill_opacity=0.85, stroke_width=0)
        right_peak2.move_to(eeg_right.get_center() + RIGHT * 1.2 + UP * 0.5)

        sweep_line_right = Line(eeg_right.get_bottom(), eeg_right.get_top(), color=WHITE, stroke_width=2)
        sweep_line_right.move_to(eeg_right.get_left())

        self.play(
            left_brain_group.animate.shift(LEFT * 3.0).scale(0.8),
            distinctive_label.animate.shift(LEFT * 3.0).scale(0.8).set_opacity(0),
            FadeIn(eeg_right),
            FadeIn(right_peak1),
            FadeIn(right_peak2),
            run_time=max(0.05, 0.80),
        )
        self.play(Create(sweep_line_right), run_time=max(0.05, 0.40))
        self.play(
            FadeOut(distinctive_label),
            FadeIn(observed_label.next_to(brain_map_group, DOWN, buff=0.25)),
            run_time=max(0.05, 0.30),
        )
        self.play(sweep_line_right.animate.move_to(eeg_right.get_right()), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 0.42))

        brain_map_group = VGroup(left_brain_group, observed_label)

        # gap 28.50 - 29.33
        self.wait(max(0.05, 0.83))

        # ------------------------------------------------------------------
        # beat 16: 29.33 - 32.36  (three seizure-type waveforms)
        # ------------------------------------------------------------------
        def sw_3hz_signal(u):
            period = 1.0 / 3.0
            phase = (u % period) / period
            spike = np.exp(-((phase - 0.1) / 0.05) ** 2)
            slow = 0.35 * np.sin(2 * np.pi * phase * 0.5 - np.pi / 2)
            return spike + slow

        def polyspike_signal(u):
            y = np.zeros_like(u)
            for k in range(-3, 4):
                y += 0.8 * np.exp(-((u - k * 0.05) / 0.015) ** 2)
            return y

        def sharp_transient_signal(u):
            spike = np.exp(-((u) / 0.06) ** 2)
            wave = 0.5 * np.exp(-((u - 0.3) / 0.15) ** 2) * np.sin(2 * np.pi * 2 * (u - 0.3))
            return spike + wave

        minitrace1 = make_trace(sw_3hz_signal, width=3.2, height=0.5, color=YELLOW, stroke_width=2)
        minitrace2 = make_trace(polyspike_signal, width=3.2, height=0.5, color=ORANGE, stroke_width=2)
        minitrace3 = make_trace(sharp_transient_signal, width=3.2, height=0.5, color=RED, stroke_width=2)

        mini_traces = VGroup(minitrace1, minitrace2, minitrace3).arrange(DOWN, buff=0.35)
        mini_traces.move_to(RIGHT * 3.5 + UP * 0.1)

        seizure_types_label = Text("Seizure types", font_size=22, color=YELLOW)
        seizure_types_label.next_to(mini_traces, DOWN, buff=0.4)

        self.play(FadeOut(eeg_right), FadeOut(right_peak1), FadeOut(right_peak2), FadeOut(sweep_line_right),
                  FadeOut(observed_label), run_time=max(0.05, 0.40))
        self.play(
            brain_map_group.animate.shift(LEFT * 1.0).set_opacity(0.4),
            run_time=max(0.05, 0.40),
        )
        self.play(FadeIn(minitrace1), FadeIn(minitrace2), FadeIn(minitrace3), run_time=max(0.05, 0.80))
        self.play(Write(seizure_types_label), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 1.13))

        # gap 32.36 - 32.44
        self.wait(max(0.05, 0.08))

        # ------------------------------------------------------------------
        # beat 17: 32.44 - 35.08  (brain regions involved)
        # ------------------------------------------------------------------
        brain_location_map = SVGMobject(ASSET_PATHS["brain"])
        brain_location_map.set_color(GREY_B).set_fill(opacity=0)
        brain_location_map.scale_to_fit_height(3.5)
        brain_location_map.move_to(np.array([-0.2, 0.0, 0.0]))

        temporal_highlight = Circle(radius=0.35, fill_color=RED, fill_opacity=0.85, stroke_width=0)
        temporal_highlight.move_to(brain_location_map.get_center() + LEFT * 0.7 + DOWN * 0.5)

        regions_label = Text("Brain regions involved", font_size=22, color=RED)
        regions_label.next_to(brain_location_map, DOWN, buff=0.3)

        self.play(FadeOut(brain_map_group), FadeOut(seizure_types_label), run_time=max(0.05, 0.25))
        self.play(
            mini_traces.animate.shift(RIGHT * 0.6),
            FadeIn(brain_location_map),
            run_time=max(0.05, 0.45),
        )
        self.play(FadeIn(temporal_highlight), run_time=max(0.05, 0.50))
        self.play(Write(regions_label), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 1.04))

        # gap 35.08 - 35.76
        self.wait(max(0.05, 0.68))

        # ------------------------------------------------------------------
        # beat 18: 35.76 - 38.74  (localized vs widespread)
        # ------------------------------------------------------------------
        localized_brain = SVGMobject(ASSET_PATHS["brain"])
        localized_brain.set_color(GREY_B).set_fill(opacity=0)
        localized_brain.scale_to_fit_height(2.6)
        localized_brain.move_to(LEFT * 3.0 + UP * 0.2)

        localized_spot = Circle(radius=0.16, fill_color=RED, fill_opacity=0.9, stroke_width=0)
        localized_spot.move_to(localized_brain.get_center() + LEFT * 0.5 + DOWN * 0.4)
        localized_label = Text("Localized", font_size=20, color=RED)
        localized_label.next_to(localized_brain, DOWN, buff=0.25)

        widespread_brain = SVGMobject(ASSET_PATHS["brain"])
        widespread_brain.set_color(GREY_B).set_fill(opacity=0)
        widespread_brain.scale_to_fit_height(2.6)
        widespread_brain.move_to(RIGHT * 3.0 + UP * 0.2)

        rng_wide = np.random.default_rng(4)
        widespread_patches = VGroup()
        for _ in range(8):
            ox = rng_wide.uniform(-1.3, 1.3)
            oy = rng_wide.uniform(-1.3, 1.3)
            patch = Circle(radius=0.16, fill_color=ORANGE, fill_opacity=0.9, stroke_width=0)
            patch.move_to(widespread_brain.get_center() + np.array([ox, oy, 0.0]))
            widespread_patches.add(patch)
        widespread_label = Text("Widespread", font_size=20, color=ORANGE)
        widespread_label.next_to(widespread_brain, DOWN, buff=0.25)

        self.play(
            FadeOut(brain_location_map),
            FadeOut(temporal_highlight),
            FadeOut(mini_traces),
            FadeOut(regions_label),
            run_time=max(0.05, 0.60),
        )
        self.play(FadeIn(localized_brain), FadeIn(localized_spot), Write(localized_label), run_time=max(0.05, 0.70))
        self.play(FadeIn(widespread_brain), FadeIn(widespread_patches), Write(widespread_label), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.98))

        # ------------------------------------------------------------------
        # beat 19: 38.74 - 40.80  (fundamentally electrical)
        # ------------------------------------------------------------------
        central_eeg = make_trace(
            spike_wave_signal,
            width=9.0,
            height=1.5,
            color=YELLOW,
            stroke_width=4,
        )
        central_eeg.move_to(ORIGIN)

        peak_left = Circle(radius=0.14, fill_color=RED, fill_opacity=0.9, stroke_width=0)
        peak_left.move_to(central_eeg.get_center() + LEFT * 2.4 + UP * 0.6)
        peak_right = Circle(radius=0.14, fill_color=RED, fill_opacity=0.9, stroke_width=0)
        peak_right.move_to(central_eeg.get_center() + RIGHT * 2.4 + UP * 0.6)

        electrical_label = Text("Fundamentally electrical events", font_size=22, color=RED)
        electrical_label.next_to(central_eeg, DOWN, buff=0.5)

        self.play(
            VGroup(localized_brain, widespread_brain, localized_label, widespread_label).animate.set_opacity(0.2),
            FadeIn(central_eeg),
            run_time=max(0.05, 0.70),
        )
        self.play(GrowFromCenter(peak_left), GrowFromCenter(peak_right), run_time=max(0.05, 0.50))
        self.play(Write(electrical_label), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.56))

        # ------------------------------------------------------------------
        # beat 20: 40.80 - 45.36  (annotations)
        # ------------------------------------------------------------------
        eeg_value_label = Text("EEG = valuable information", font_size=28, color=YELLOW)
        eeg_value_label.to_corner(UP + LEFT, buff=0.5)

        annotation_sweep = Line(central_eeg.get_bottom(), central_eeg.get_top(), color=WHITE, stroke_width=2)
        annotation_sweep.move_to(central_eeg.get_left())

        marker_spike = Text("Sharp spike", font_size=18, color=YELLOW)
        marker_spike.next_to(central_eeg.get_center() + LEFT * 2.4 + UP * 1.1, UP, buff=0.1)
        marker_slow = Text("Slow wave", font_size=18, color=YELLOW)
        marker_slow.next_to(central_eeg.get_center() + LEFT * 0.5 + DOWN * 1.0, DOWN, buff=0.1)
        marker_after = Text("After-discharge", font_size=18, color=ORANGE)
        marker_after.next_to(central_eeg.get_center() + RIGHT * 1.8 + DOWN * 1.15, DOWN, buff=0.1)

        self.play(
            VGroup(localized_brain, widespread_brain, localized_label, widespread_label).animate.set_opacity(0.08),
            FadeIn(eeg_value_label),
            run_time=max(0.05, 0.80),
        )
        self.play(Create(annotation_sweep), run_time=max(0.05, 0.70))
        self.play(Write(marker_spike), run_time=max(0.05, 0.70))
        self.play(Write(marker_slow), run_time=max(0.05, 0.70))
        self.play(Write(marker_after), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.96))

        # ------------------------------------------------------------------
        # beat 21: 45.36 - 48.76  (EEG vs structural imaging)
        # ------------------------------------------------------------------
        left_eeg_group = VGroup(central_eeg, peak_left, peak_right, marker_spike, marker_slow, marker_after, annotation_sweep)
        structural_brain = SVGMobject(ASSET_PATHS["brain"])
        structural_brain.set_color(GREY_B).set_fill(opacity=0)
        structural_brain.scale_to_fit_height(3.0)
        structural_brain.move_to(RIGHT * 4.2 + UP * 0.2)
        structural_label = Text("Structural imaging", font_size=20, color=GREY_B)
        structural_label.next_to(structural_brain, DOWN, buff=0.25)

        caption = Text(
            "Structural imaging alone cannot provide this information.",
            font_size=20,
            color=GREY_B,
        )
        caption.to_edge(DOWN, buff=0.4)

        self.play(
            left_eeg_group.animate.scale(0.75).move_to(LEFT * 3.5 + UP * 0.1),
            FadeOut(eeg_value_label),
            run_time=max(0.05, 0.70),
        )
        self.play(FadeIn(structural_brain), Write(structural_label), run_time=max(0.05, 0.70))
        self.play(Write(caption), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.50))

        # ------------------------------------------------------------------
        # beat 22: 48.76 - 49.58  final hold
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.82))