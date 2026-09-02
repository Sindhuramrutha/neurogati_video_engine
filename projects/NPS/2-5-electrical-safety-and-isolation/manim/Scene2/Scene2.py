ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(MovingCameraScene):
    def make_shield(self, color=GREEN):
        shield = Polygon(
            np.array([-0.40, 0.35, 0]),
            np.array([0.40, 0.35, 0]),
            np.array([0.40, -0.15, 0]),
            np.array([0.25, -0.15, 0]),
            np.array([0.00, -0.65, 0]),
            np.array([-0.25, -0.15, 0]),
            np.array([-0.40, -0.15, 0]),
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=color,
            fill_opacity=1,
        )
        return shield

    def make_shield_check(self, color=GREEN):
        shield = self.make_shield(color)
        check_1 = Line(
            np.array([-0.12, -0.04, 0]),
            np.array([-0.02, 0.06, 0]),
            color=WHITE,
            stroke_width=4,
        )
        check_2 = Line(
            np.array([-0.02, 0.06, 0]),
            np.array([0.15, -0.18, 0]),
            color=WHITE,
            stroke_width=4,
        )
        return VGroup(shield, check_1, check_2)

    def make_lightning_icon(self, color=YELLOW, scale=1.0):
        bolt = Polygon(
            np.array([0.12, 0.35, 0]) * scale,
            np.array([-0.20, -0.08, 0]) * scale,
            np.array([0.02, -0.08, 0]) * scale,
            np.array([-0.12, -0.35, 0]) * scale,
            np.array([0.20, 0.08, 0]) * scale,
            np.array([0.00, 0.08, 0]) * scale,
            stroke_color=color,
            stroke_width=2,
            fill_color=color,
            fill_opacity=1,
        )
        return bolt

    def make_sine_wave(self, color=GREEN, width=1.8, height=0.30, stroke_width=5):
        wave = VMobject().set_stroke(color=color, width=stroke_width, opacity=1)
        n = 80
        pts = []
        for i in range(n + 1):
            x = -width / 2 + width * i / n
            y = height * np.sin(2 * PI * 2.5 * i / n)
            pts.append(np.array([x, y, 0]))
        wave.set_points_as_corners(pts)
        return wave

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------------- Build five-node diagram ----------------
        box_defs = [
            ("Participant", TEAL, 20, False),
            ("Electrodes", TEAL, 20, False),
            ("Isolation\nCircuit", GOLD, 17, True),
            ("Acquisition\nSystem", PURPLE, 17, False),
            ("Computer", PURPLE, 20, False),
        ]

        nodes = VGroup()
        box_shapes = []
        box_texts = []

        for label, fill, font, special in box_defs:
            shape = RoundedRectangle(
                corner_radius=0.18,
                width=2.2,
                height=1.0,
                fill_color=fill,
                fill_opacity=0.20,
                stroke_color=WHITE,
                stroke_width=2,
            )
            if special:
                shape.set_stroke(GOLD, width=4)
                shape.set_fill(YELLOW, opacity=0.28)

            txt = Text(label, font_size=font, color=WHITE, line_spacing=1)
            txt.scale_to_fit_width(shape.width - 0.35)
            txt.move_to(shape.get_center())

            node = VGroup(shape, txt)
            nodes.add(node)
            box_shapes.append(shape)
            box_texts.append(txt)

        nodes.arrange(RIGHT, buff=0.45)
        nodes.move_to(UP * 1.2)

        participant_box, electrodes_box, isolation_box, acquisition_box, computer_box = box_shapes
        participant_node, electrodes_node, isolation_node, acquisition_node, computer_node = nodes
        participant_text, electrodes_text, isolation_text, acquisition_text, computer_text = box_texts

        arrows = VGroup()
        for i in range(4):
            left_box = box_shapes[i]
            right_box = box_shapes[i + 1]
            arrow = Arrow(
                left_box.get_right() + RIGHT * 0.05,
                right_box.get_left() + LEFT * 0.05,
                buff=0.05,
                color=WHITE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.20,
            )
            arrows.add(arrow)

        diagram = VGroup(nodes, arrows)

        # ---------------- Beat 1: 0.00-4.06 ----------------
        per_reveal = 0.55
        for i, node in enumerate(nodes):
            if i == 0:
                self.play(FadeIn(node), run_time=max(0.05, 0.40))
            else:
                self.play(FadeIn(node), FadeIn(arrows[i - 1]), run_time=max(0.05, 0.40))
            self.wait(max(0.05, per_reveal - 0.40))

        self.play(
            Indicate(isolation_node, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 4.06 - (len(nodes) * per_reveal + 0.70)))

        # Gap 4.06-5.18
        self.wait(max(0.05, 1.12))

        # ---------------- Beat 2: 5.18-10.34 ----------------
        barrier_x = (isolation_box.get_right()[0] + acquisition_box.get_left()[0]) / 2
        barrier_start = np.array([barrier_x, isolation_box.get_top()[1] + 0.10, 0])
        barrier_end = np.array([barrier_x, isolation_box.get_bottom()[1] - 0.25, 0])
        barrier = DashedLine(
            barrier_start,
            barrier_end,
            color=RED,
            stroke_width=3,
            dash_length=0.15,
        )

        self.play(Create(barrier), run_time=max(0.05, 0.82))

        left_side_label = Text("participant side", font_size=20, color=TEAL)
        left_side_label.next_to(VGroup(participant_node, electrodes_node), DOWN, buff=0.30)

        right_side_label = Text("powered equipment side", font_size=20, color=PURPLE)
        right_side_label.next_to(VGroup(acquisition_node, computer_node), DOWN, buff=0.30)

        self.play(FadeIn(left_side_label), FadeIn(right_side_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.76))

        acq_glow = SurroundingRectangle(acquisition_box, color=RED, buff=0.10, stroke_width=5)
        small_lightning = self.make_lightning_icon(YELLOW, scale=0.22).move_to(
            acquisition_box.get_top() + DOWN * 0.25 + LEFT * 0.50
        )

        self.play(
            Create(acq_glow),
            FadeIn(small_lightning),
            acquisition_box.animate.set_stroke(color=RED, width=4),
            run_time=max(0.05, 0.48),
        )
        self.play(
            FadeOut(acq_glow),
            FadeOut(small_lightning),
            acquisition_box.animate.set_stroke(color=PURPLE, width=2),
            run_time=max(0.05, 0.36),
        )
        self.wait(max(0.05, 0.30))

        solid_barrier = Line(barrier_start, barrier_end, color=RED, stroke_width=7)
        self.play(Transform(barrier, solid_barrier), run_time=max(0.05, 0.44))

        # Gap 10.34-10.68
        self.wait(max(0.05, 0.34))

        # ---------------- Beat 3: 10.68-13.68 ----------------
        wave_start = arrows[1].get_center()
        wave_end = computer_box.get_right() + RIGHT * 0.30
        wave_path = Line(wave_start, wave_end, color=GREEN, stroke_width=0)

        wave_curve = self.make_sine_wave(color=GREEN, width=1.80, height=0.30, stroke_width=5)
        wave_arrowhead = Polygon(
            np.array([0.70, -0.12, 0]),
            np.array([1.10, 0.00, 0]),
            np.array([0.70, 0.12, 0]),
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=0,
        )
        wave_group = VGroup(wave_curve, wave_arrowhead)
        wave_tracker = ValueTracker(0)

        wave_group.add_updater(
            lambda m: m.move_to(wave_path.point_from_proportion(wave_tracker.get_value()))
        )
        self.add(wave_group)

        physiological_label = Text("physiological signals", font_size=22, color=GREEN)
        physiological_label.move_to(np.array([wave_path.get_center()[0], 0.00, 0]))

        self.play(
            wave_tracker.animate.set_value(1),
            FadeIn(physiological_label),
            run_time=max(0.05, 2.40),
        )
        self.wait(max(0.05, 3.00 - 2.40))

        # Gap 13.68-14.66
        self.wait(max(0.05, 0.98))

        # ---------------- Beat 4: 14.66-16.44 ----------------
        caption_pass_hazard = Text(
            "signals pass through — hazardous paths do not.",
            font_size=25,
            color=WHITE,
        )
        caption_pass_hazard.to_edge(DOWN, buff=1.10)

        self.play(
            wave_group.animate.set_opacity(0.22),
            FadeOut(physiological_label),
            run_time=max(0.05, 0.40),
        )
        self.play(FadeIn(caption_pass_hazard), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 1.78 - 0.40 - 0.60))

        # Gap 16.44-17.46
        self.wait(max(0.05, 1.02))

        # ---------------- Beat 5: 17.46-21.64 ----------------
        full_start = participant_box.get_left() + LEFT * 0.10
        full_end = computer_box.get_right() + RIGHT * 0.10
        wave_path.put_start_and_end_on(full_start, full_end)

        wave_tracker.set_value(0)
        wave_group.set_opacity(1)

        iso_exit_x = isolation_box.get_right()[0] + 0.25
        mid_t = (iso_exit_x - full_start[0]) / (full_end[0] - full_start[0])

        self.play(wave_tracker.animate.set_value(mid_t), run_time=max(0.05, 1.40))

        allowed_label = Text("allowed to pass", font_size=22, color=GREEN)
        allowed_label.move_to(np.array([iso_exit_x, isolation_box.get_bottom()[1] - 0.40, 0]))

        self.play(FadeIn(allowed_label), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.35))
        self.play(FadeOut(allowed_label), run_time=max(0.05, 0.30))
        self.play(wave_tracker.animate.set_value(1), run_time=max(0.05, 1.30))
        self.wait(max(0.05, 4.18 - (1.40 + 0.35 + 0.35 + 0.30 + 1.30)))

        # Gap 21.64-22.38
        self.wait(max(0.05, 0.74))

        # ---------------- Beat 6: 22.38-26.32 ----------------
        bolt_start = acquisition_box.get_left() + LEFT * 0.05
        bolt_end = isolation_box.get_right() + RIGHT * 0.15
        red_bolt_path = Line(bolt_start, bolt_end, color=RED, stroke_width=0)

        red_bolt = self.make_lightning_icon(RED, scale=0.80)
        red_bolt_tracker = ValueTracker(0)
        red_bolt.add_updater(
            lambda m: m.move_to(red_bolt_path.point_from_proportion(red_bolt_tracker.get_value()))
        )
        self.add(red_bolt)

        self.play(FadeIn(red_bolt), run_time=max(0.05, 0.28))
        self.play(red_bolt_tracker.animate.set_value(0.95), run_time=max(0.05, 1.20), rate_func=linear)

        collision_point = red_bolt_path.point_from_proportion(0.95)

        fragments = VGroup()
        fragment_directions = np.linspace(0, 2 * PI, 10, endpoint=False)
        for angle in fragment_directions:
            end = collision_point + np.array([np.cos(angle), np.sin(angle), 0]) * 0.7
            frag = Line(collision_point, end, color=RED, stroke_width=3)
            fragments.add(frag)

        x_line_1 = Line(
            collision_point + LEFT * 0.22 + UP * 0.22,
            collision_point + RIGHT * 0.22 + DOWN * 0.22,
            color=RED,
            stroke_width=5,
        )
        x_line_2 = Line(
            collision_point + LEFT * 0.22 + DOWN * 0.22,
            collision_point + RIGHT * 0.22 + UP * 0.22,
            color=RED,
            stroke_width=5,
        )
        x_mark = VGroup(x_line_1, x_line_2)

        blocked_label = Text("blocked", font_size=24, color=RED)
        blocked_label.next_to(barrier, RIGHT, buff=0.25).shift(DOWN * 0.20)

        self.play(FadeOut(red_bolt), run_time=max(0.05, 0.08))
        self.play(
            *[GrowFromPoint(f, collision_point) for f in fragments],
            FadeIn(x_mark),
            run_time=max(0.05, 0.30),
        )
        self.play(
            FadeOut(fragments),
            FadeOut(x_mark),
            FadeIn(blocked_label),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 3.94 - (0.28 + 1.20 + 0.08 + 0.30 + 0.30)))

        # ---------------- Beat 7: 26.32-34.12 ----------------
        self.play(
            FadeOut(blocked_label),
            isolation_text.animate.shift(UP * 0.22),
            run_time=max(0.05, 0.30),
        )

        protective_shield = self.make_shield(GREEN).scale_to_fit_height(0.45)
        protective_shield.move_to(isolation_box.get_center() + DOWN * 0.15)

        iso_glow = SurroundingRectangle(isolation_node, color=GREEN, buff=0.15, stroke_width=5)

        self.play(
            GrowFromCenter(protective_shield),
            Create(iso_glow),
            isolation_box.animate.set_stroke(GREEN, width=4),
            run_time=max(0.05, 0.50),
        )
        self.play(Indicate(isolation_node, color=GREEN, scale_factor=1.08), run_time=max(0.05, 0.50))

        wave_tracker.set_value(0)
        self.play(wave_tracker.animate.set_value(1), run_time=max(0.05, 3.00))

        protective_barrier_label = Text("protective barrier", font_size=24, color=GREEN)
        protective_barrier_label.next_to(isolation_node, UP, buff=0.35)

        between_caption = Text(
            "between participant and powered equipment",
            font_size=24,
            color=WHITE,
        )
        between_caption.to_edge(DOWN, buff=1.20)

        self.play(
            FadeOut(caption_pass_hazard),
            FadeIn(protective_barrier_label),
            FadeIn(between_caption),
            run_time=max(0.05, 0.70),
        )
        self.play(Indicate(isolation_node, color=GREEN, scale_factor=1.06), run_time=max(0.05, 0.40))

        wave_tracker.set_value(0)
        self.play(wave_tracker.animate.set_value(1), run_time=max(0.05, 1.60))
        self.wait(max(0.05, 0.80))

        # Gap 34.12-34.98
        self.wait(max(0.05, 0.86))

        # ---------------- Beat 8: 34.98-40.56 ----------------
        schematic_grid = VGroup()
        for x in np.arange(-7, 7.01, 1.0):
            schematic_grid.add(
                Line(
                    np.array([x, -4, 0]),
                    np.array([x, 4, 0]),
                    color=BLUE,
                    stroke_width=1,
                    stroke_opacity=0.20,
                )
            )
        for y in np.arange(-4, 4.01, 1.0):
            schematic_grid.add(
                Line(
                    np.array([-7, y, 0]),
                    np.array([7, y, 0]),
                    color=BLUE,
                    stroke_width=1,
                    stroke_opacity=0.20,
                )
            )
        schematic_grid.set_opacity(0)
        self.add(schematic_grid)
        self.bring_to_back(schematic_grid)
        self.play(schematic_grid.animate.set_opacity(0.35), run_time=max(0.05, 0.60))

        mini_shield_check = self.make_shield_check(GREEN).scale(0.25)
        mini_shield_check.move_to(
            isolation_box.get_corner(UR) + LEFT * 0.18 + DOWN * 0.20
        )
        self.play(GrowFromCenter(mini_shield_check), run_time=max(0.05, 0.60))

        standard_safety_caption = Text(
            "standard safety feature",
            font_size=26,
            color=YELLOW,
        )
        standard_safety_caption.to_edge(DOWN, buff=1.20)

        self.play(
            FadeOut(between_caption),
            FadeIn(standard_safety_caption),
            run_time=max(0.05, 0.60),
        )

        wave_tracker.set_value(0)
        self.play(wave_tracker.animate.set_value(1), run_time=max(0.05, 3.28))
        self.wait(max(0.05, 5.58 - (0.60 + 0.60 + 0.60 + 3.28)))

        # Gap 40.56-41.12
        self.wait(max(0.05, 0.56))

        # ---------------- Beat 9: 41.12-45.18 ----------------
        neural_signals_label = Text("neural signals recorded", font_size=20, color=TEAL)
        neural_signals_label.next_to(electrodes_box, UP, buff=0.25)

        participant_safety_label = Text("participant safety maintained", font_size=20, color=GREEN)
        participant_safety_label.next_to(participant_box, DOWN, buff=0.35)

        self.play(
            FadeOut(left_side_label),
            FadeOut(right_side_label),
            FadeIn(neural_signals_label),
            FadeIn(participant_safety_label),
            run_time=max(0.05, 0.60),
        )

        wave_tracker.set_value(0)
        left_region_center = np.array([-1.0, 1.2, 0])
        self.play(
            self.camera.frame.animate.scale(0.94).move_to(left_region_center),
            wave_tracker.animate.set_value(1),
            run_time=max(0.05, 2.20),
        )
        self.play(
            Indicate(isolation_node, color=GREEN, scale_factor=1.08),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 4.06 - (0.60 + 2.20 + 0.30)))

        # ---------------- Beat 10: 45.18-46.08 ----------------
        isolation_protects_caption = Text(
            "isolation protects the participant",
            font_size=27,
            color=YELLOW,
        )
        isolation_protects_caption.to_edge(DOWN, buff=0.90)

        self.play(
            FadeOut(standard_safety_caption),
            FadeIn(isolation_protects_caption),
            run_time=max(0.05, 0.30),
        )
        self.play(
            iso_glow.animate.set_stroke(width=4).set_opacity(1),
            run_time=max(0.05, 0.15),
        )
        self.wait(max(0.05, 0.90 - (0.30 + 0.15)))