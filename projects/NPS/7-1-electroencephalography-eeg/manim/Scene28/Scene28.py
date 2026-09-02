ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\ruler.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}


class Scene28(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_checkmark():
            return VGroup(
                Line(LEFT * 0.09 + DOWN * 0.01, ORIGIN, color=GREEN, stroke_width=3),
                Line(ORIGIN, RIGHT * 0.10 + UP * 0.08, color=GREEN, stroke_width=3),
            )

        def make_head_safe_icon():
            icon = VGroup()
            ring = Circle(radius=0.32, color=GREEN, stroke_width=3)
            head = Circle(radius=0.22, color=WHITE, fill_color=WHITE, fill_opacity=0.25, stroke_width=2)
            headset_arc = Arc(radius=0.15, start_angle=0, angle=PI, color=YELLOW, stroke_width=2.5)
            headset_arc.move_to(head.get_center() + UP * 0.03)
            d1 = Dot(head.get_center() + LEFT * 0.08 + UP * 0.05, radius=0.025, color=YELLOW)
            d2 = Dot(head.get_center() + RIGHT * 0.08 + UP * 0.05, radius=0.025, color=YELLOW)
            icon.add(ring, head, headset_arc, d1, d2)
            return icon

        def make_temporal_icon():
            icon = VGroup()
            timeline = Line(LEFT * 0.9, RIGHT * 0.9, color=GREY_B, stroke_width=2)
            ticks = VGroup(*[
                Line(np.array([x, -0.06, 0]), np.array([x, 0.06, 0]), color=WHITE, stroke_width=1.2)
                for x in np.linspace(-0.8, 0.8, 13)
            ])
            pts = [(-0.8, 0.05), (-0.55, 0.05), (-0.45, 0.22), (-0.35, -0.12), (-0.2, 0.08),
                   (-0.02, 0.08), (0.12, -0.10), (0.30, 0.18), (0.55, 0.02), (0.8, 0.02)]
            wave = VMobject()
            wave.set_points_as_corners([np.array([x, y, 0]) for x, y in pts])
            wave.set_stroke(TEAL, width=3)
            icon.add(timeline, ticks, wave)
            return icon

        def make_portable_icon():
            icon = VGroup()
            box = RoundedRectangle(width=0.9, height=0.55, corner_radius=0.08,
                                   fill_color=BLUE, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            handle = Arc(radius=0.3, start_angle=0, angle=PI, color=WHITE, stroke_width=2)
            handle.move_to(box.get_top() + UP * 0.02)
            tag = RoundedRectangle(width=0.36, height=0.25, fill_color=WHITE, fill_opacity=1, stroke_width=0)
            tag.move_to(box.get_right() + RIGHT * 0.35)
            down_arrow = Arrow(tag.get_top() + DOWN * 0.08, tag.get_bottom() + DOWN * 0.08,
                               color=GREEN, stroke_width=3, buff=0.02,
                               max_tip_length_to_length_ratio=0.4)
            icon.add(box, handle, tag, down_arrow)
            return icon

        def make_realtime_icon():
            icon = VGroup()
            in_pts = [(-1.1, 0.1), (-0.8, 0.1), (-0.7, 0.22), (-0.6, -0.1), (-0.4, 0.1), (-0.3, 0.1)]
            wave_in = VMobject()
            wave_in.set_points_as_corners([np.array([x, y, 0]) for x, y in in_pts])
            wave_in.set_stroke(YELLOW, width=2)
            node = Square(side_length=0.4, fill_color=PURPLE, fill_opacity=1,
                          stroke_color=WHITE, stroke_width=2).move_to(ORIGIN)
            out_pts = [(0.3, 0.1), (0.5, 0.1), (0.6, 0.24), (0.7, 0.0), (0.9, 0.1)]
            wave_out = VMobject()
            wave_out.set_points_as_corners([np.array([x, y, 0]) for x, y in out_pts])
            wave_out.set_stroke(GREEN, width=2)
            clock = Circle(radius=0.15, color=WHITE, stroke_width=2,
                           fill_color=GREY_E, fill_opacity=0.5).move_to(node.get_top() + UP * 0.45)
            h1 = Line(clock.get_center(), clock.get_center() + UP * 0.08, color=WHITE, stroke_width=2)
            h2 = Line(clock.get_center(), clock.get_center() + RIGHT * 0.07, color=WHITE, stroke_width=2)
            icon.add(wave_in, node, wave_out, VGroup(clock, h1, h2))
            return icon

        def make_continuous_icon():
            icon = VGroup()
            timeline = Line(LEFT * 1.3, RIGHT * 1.1, color=GREY_B, stroke_width=2)
            pts = [np.array([x, 0.18 * np.sin(3.5 * x) + 0.05 * np.sin(7 * x), 0])
                   for x in np.linspace(-1.2, 1.0, 80)]
            wave = VMobject()
            wave.set_points_as_corners(pts)
            wave.set_stroke(TEAL, width=2.5)
            brain = SVGMobject(ASSET_PATHS["brain"]).set_color(WHITE).scale_to_fit_height(0.35)
            brain.move_to(RIGHT * 1.35)
            icon.add(timeline, wave, brain)
            return icon

        def make_noisy_icon():
            icon = VGroup()
            signal = VMobject()
            signal.set_points_as_corners([np.array([x, 0.12 * np.sin(2.5 * x), 0])
                                          for x in np.linspace(-1.0, 1.0, 50)])
            signal.set_stroke(BLUE, width=2)
            noise_pts = [(-1.0, 0.05), (-0.7, 0.25), (-0.5, -0.20), (-0.3, 0.30),
                         (-0.05, -0.25), (0.15, 0.20), (0.35, -0.10), (0.55, 0.25),
                         (0.75, -0.05), (0.95, 0.20), (1.0, 0.05)]
            noise = VMobject()
            noise.set_points_as_corners([np.array([x, y, 0]) for x, y in noise_pts])
            noise.set_stroke(RED, width=1.4)
            icon.add(signal, noise)
            return icon

        def make_individual_variability_icon():
            icon = VGroup()
            brains = VGroup()
            for x in [-0.6, 0.0, 0.6]:
                b = SVGMobject(ASSET_PATHS["brain"]).set_color(WHITE).scale_to_fit_height(0.28)
                b.move_to(np.array([x, -0.05, 0]))
                brains.add(b)
            w1 = VMobject()
            w1.set_points_as_corners([np.array([x, 0.08 * np.sin(2 * x) + 0.04, 0])
                                      for x in np.linspace(-0.25, 0.25, 20)])
            w1.set_stroke(TEAL, width=2).move_to(np.array([-0.6, 0.22, 0]))
            w2 = VMobject()
            w2.set_points_as_corners([np.array([x, 0.10 * np.sin(7 * x), 0])
                                      for x in np.linspace(-0.25, 0.25, 24)])
            w2.set_stroke(ORANGE, width=2).move_to(np.array([0.0, 0.22, 0]))
            w3 = VMobject()
            w3.set_points_as_corners([np.array([x, 0.07 * np.sin(1.8 * x), 0])
                                      for x in np.linspace(-0.25, 0.25, 20)])
            w3.set_stroke(PURPLE, width=2).move_to(np.array([0.6, 0.22, 0]))
            icon.add(brains, w1, w2, w3)
            return icon

        def make_fatigue_icon():
            icon = VGroup()
            face = Circle(radius=0.32, fill_color=ORANGE, fill_opacity=0.35,
                          stroke_color=WHITE, stroke_width=2)
            eye_l = Line(LEFT * 0.16 + UP * 0.10, LEFT * 0.04 + UP * 0.04,
                         color=WHITE, stroke_width=2)
            eye_r = Line(RIGHT * 0.04 + UP * 0.04, RIGHT * 0.16 + UP * 0.10,
                         color=WHITE, stroke_width=2)
            mouth = Arc(radius=0.12, start_angle=0, angle=PI, color=WHITE, stroke_width=2)
            mouth.move_to(DOWN * 0.16)
            wave = VMobject()
            wave.set_points_as_corners([np.array([x, 0.12 * np.exp(-2.2 * (x + 0.05)) * np.sin(5 * x), 0])
                                        for x in np.linspace(-0.15, 1.0, 60)])
            wave.set_stroke(GREY_B, width=2).move_to(face.get_right() + RIGHT * 0.50)
            icon.add(face, eye_l, eye_r, mouth, wave)
            icon.rotate(-0.10)
            return icon

        def make_ml_icon():
            icon = VGroup()
            node1 = Circle(radius=0.09, fill_color=TEAL, fill_opacity=1,
                           stroke_color=WHITE, stroke_width=2).move_to(LEFT * 0.25 + UP * 0.22)
            node2 = Circle(radius=0.09, fill_color=TEAL, fill_opacity=1,
                           stroke_color=WHITE, stroke_width=2).move_to(LEFT * 0.25)
            node3 = Circle(radius=0.09, fill_color=TEAL, fill_opacity=1,
                           stroke_color=WHITE, stroke_width=2).move_to(LEFT * 0.25 + DOWN * 0.22)
            nodes = VGroup(node1, node2, node3)
            central = Circle(radius=0.10, fill_color=ORANGE, fill_opacity=1,
                             stroke_color=WHITE, stroke_width=2).move_to(RIGHT * 0.15)
            input_arrows = VGroup(*[
                Arrow(node.get_center() + LEFT * 0.35, node.get_center(),
                      color=YELLOW, stroke_width=2, buff=0.06,
                      max_tip_length_to_length_ratio=0.4)
                for node in nodes
            ])
            edges = VGroup(*[
                Line(node.get_center(), central.get_center(), color=GREY_B, stroke_width=2)
                for node in nodes
            ])
            out_box = RoundedRectangle(width=0.42, height=0.24, corner_radius=0.06,
                                       fill_color=GREEN, fill_opacity=0.8,
                                       stroke_color=WHITE, stroke_width=1.5).move_to(RIGHT * 0.62)
            out_arrow = Arrow(central.get_center(), out_box.get_left(),
                              color=GREEN, stroke_width=3, buff=0.06,
                              max_tip_length_to_length_ratio=0.35)
            icon.add(nodes, central, input_arrows, edges, out_arrow, out_box)
            refs = {
                "nodes": nodes,
                "central": central,
                "edges": edges,
                "input_arrows": input_arrows,
                "out_arrow": out_arrow,
                "out_box": out_box,
            }
            return icon, refs

        def make_thought_bubble():
            cloud = VGroup()
            base = Ellipse(width=2.2, height=1.0, fill_color=WHITE,
                           fill_opacity=0.9, stroke_width=0)
            cloud.add(base)
            for dx, dy, r in [(-0.7, 0.25, 0.45), (0.7, 0.20, 0.5),
                              (0.0, -0.15, 0.6), (-0.4, -0.05, 0.5),
                              (0.4, -0.10, 0.55)]:
                cloud.add(Circle(radius=r, fill_color=WHITE, fill_opacity=0.9,
                                 stroke_width=0).move_to(np.array([dx, dy, 0])))
            dots = VGroup(*[Circle(radius=0.07, fill_color=WHITE, fill_opacity=0.85,
                                   stroke_width=0) for _ in range(3)]).arrange(DOWN, buff=0.11)
            dots.next_to(base, DOWN, buff=0.08)
            bubble = VGroup(cloud, dots).move_to(ORIGIN)
            return bubble

        def make_pattern_parts():
            wave = VMobject()
            pts = [np.array([x, 0.22 * np.sin(4 * x) + 0.08 * np.sin(9 * x), 0])
                   for x in np.linspace(-1.0, 0.75, 80)]
            wave.set_points_as_corners(pts)
            wave.set_stroke(WHITE, width=3)

            x0, x1 = 0.10, 0.52
            highlight = Rectangle(width=x1 - x0, height=0.75, stroke_color=YELLOW,
                                  stroke_width=3, fill_color=YELLOW,
                                  fill_opacity=0.12).move_to(np.array([(x0 + x1) / 2, 0, 0]))
            check = VGroup(
                Line(LEFT * 0.06 + UP * 0.00, ORIGIN, color=GREEN, stroke_width=3),
                Line(ORIGIN, RIGHT * 0.08 + UP * 0.06, color=GREEN, stroke_width=3),
            )
            check.move_to(highlight.get_top() + UP * 0.18)

            pattern_wave_group = VGroup(wave, highlight, check)
            pattern_wave_group.move_to(LEFT * 0.9)

            command_rect = RoundedRectangle(width=2.0, height=0.55, corner_radius=0.08,
                                            fill_color=GREY_C, fill_opacity=0.85,
                                            stroke_color=WHITE, stroke_width=2)
            command_text = Text("Predefined Control Command", font_size=16,
                                color=WHITE, weight="BOLD").scale_to_fit_width(1.7)
            command_text.move_to(command_rect)
            command_group = VGroup(command_rect, command_text)
            command_group.move_to(RIGHT * 1.45)

            arrow = Arrow(highlight.get_right(), command_group.get_left(),
                          color=GREEN, stroke_width=4, buff=0.12,
                          max_tip_length_to_length_ratio=0.30)
            return pattern_wave_group, command_group, arrow, highlight

        # ---------- initial previous panel fade-out ----------
        prev_labels = ["Assistive Communication", "Wheelchair Control",
                       "Prosthetic Device Control", "Neurorehabilitation", "Research and HCI"]
        prev_colors = [BLUE, TEAL, PURPLE, ORANGE, PINK]
        prev_panels = VGroup()
        for i, lab in enumerate(prev_labels):
            rect = Rectangle(width=2.35, height=3.0, fill_color=prev_colors[i],
                             fill_opacity=0.22, stroke_color=prev_colors[i], stroke_width=2)
            rect.move_to(np.array([-5.3 + i * 2.65, 0.4, 0]))
            txt = Text(lab, font_size=15, weight="BOLD", color=WHITE).scale_to_fit_width(2.2)
            txt.next_to(rect, DOWN, buff=0.12)
            prev_panels.add(VGroup(rect, txt))
        self.add(prev_panels)
        self.play(FadeOut(prev_panels), run_time=max(0.05, 1.5))

        # ---------- Beat 1: empty advantages checklist ----------
        adv_slot_rects = []
        adv_checkboxes = []
        adv_rows = []
        for _ in range(5):
            checkbox = Square(side_length=0.26, color=WHITE, stroke_width=2.5)
            slot = Rectangle(width=3.4, height=0.38, stroke_color=GREY_B,
                             stroke_width=2, fill_color=GREY_E, fill_opacity=0.08)
            row = VGroup(checkbox, slot).arrange(RIGHT, buff=0.18)
            adv_rows.append(row)
            adv_slot_rects.append(slot)
            adv_checkboxes.append(checkbox)
        adv_group = VGroup(*adv_rows).arrange(DOWN, buff=0.18).move_to(LEFT * 4.4 + UP * 0.2)

        self.play(Create(adv_group), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.42))

        # ---------- Beats 2-6: fill advantages one by one ----------
        adv_text_strs = [
            "Non-invasive recording.",
            "Excellent temporal resolution.",
            "Portable and relatively inexpensive systems.",
            "Suitable for real-time signal processing.",
            "Supports continuous monitoring of brain activity.",
        ]
        adv_durations = [1.62, 1.70, 2.40, 2.42, 2.46]
        ml_refs = None
        ml_icon = None

        for i, (txt_str, dur) in enumerate(zip(adv_text_strs, adv_durations)):
            text = Text(txt_str, font_size=15, weight="BOLD", color=WHITE).scale_to_fit_width(
                adv_slot_rects[i].width - 0.1)
            text.move_to(adv_slot_rects[i])
            check = make_checkmark().move_to(adv_checkboxes[i])

            if i == 0:
                icon = make_head_safe_icon()
            elif i == 1:
                icon = make_temporal_icon()
            elif i == 2:
                icon = make_portable_icon()
            elif i == 3:
                icon = make_realtime_icon()
            else:
                icon = make_continuous_icon()

            icon.scale_to_fit_height(0.60)
            icon.next_to(adv_slot_rects[i], RIGHT, buff=0.28)
            adv_rows[i].add(icon)

            text_dur = max(0.05, dur * 0.35)
            check_dur = max(0.05, dur * 0.20)
            icon_dur = max(0.05, dur * 0.30)
            wait_dur = max(0.05, dur * 0.15)

            self.play(FadeIn(text), run_time=max(0.05, text_dur))
            self.play(Create(check), run_time=max(0.05, check_dur))
            self.play(GrowFromCenter(icon), run_time=max(0.05, icon_dur))
            self.wait(max(0.05, wait_dur))

        # ---------- Beat 7: shift advantages left, brighten right ----------
        right_glow = Rectangle(width=7.0, height=5.5, fill_color=YELLOW,
                               fill_opacity=0.07, stroke_width=0).move_to(RIGHT * 4.6 + UP * 0.2)
        self.play(adv_group.animate.shift(LEFT * 0.4), FadeIn(right_glow), run_time=max(0.05, 0.94))

        # ---------- Beat 8: Challenges title and empty slots ----------
        ch_slot_rects = []
        ch_placeholders = []
        ch_rows = []
        for _ in range(4):
            ph = RoundedRectangle(width=1.0, height=0.62, fill_color=GREY_E,
                                  fill_opacity=0.05, stroke_color=GREY_B, stroke_width=2)
            slot = Rectangle(width=3.2, height=0.38, stroke_color=GREY_B,
                             stroke_width=2, fill_color=GREY_E, fill_opacity=0.08)
            row = VGroup(ph, slot).arrange(RIGHT, buff=0.14)
            ch_rows.append(row)
            ch_slot_rects.append(slot)
            ch_placeholders.append(ph)
        ch_group = VGroup(*ch_rows).arrange(DOWN, buff=0.16).move_to(RIGHT * 4.3 + UP * 0.1)
        ch_title = Text("Challenges", font_size=32, weight="BOLD", color=ORANGE)
        ch_title.next_to(ch_group, UP, buff=0.28)

        self.play(Write(ch_title), run_time=max(0.05, 1.2))
        self.play(FadeIn(ch_group), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.78))

        # ---------- Beats 9-12: fill challenge items ----------
        ch_text_strs = [
            "Weak signals affected by noise.",
            "Individual variability in brain activity.",
            "User fatigue during long sessions.",
            "Requires robust signal-processing and ML algorithms.",
        ]
        ch_durations = [1.40, 3.60, 2.48, 3.66]

        for i, (txt_str, dur) in enumerate(zip(ch_text_strs, ch_durations)):
            text = Text(txt_str, font_size=15, weight="BOLD", color=WHITE).scale_to_fit_width(
                ch_slot_rects[i].width - 0.1)
            text.move_to(ch_slot_rects[i])

            if i == 0:
                icon = make_noisy_icon()
            elif i == 1:
                icon = make_individual_variability_icon()
            elif i == 2:
                icon = make_fatigue_icon()
            else:
                icon, ml_refs = make_ml_icon()
                ml_icon = icon

            icon.scale_to_fit_width(0.95)
            icon.scale_to_fit_height(0.58)
            icon.move_to(ch_placeholders[i])
            ch_rows[i].add(icon)

            text_dur = max(0.05, dur * 0.45)
            icon_dur = max(0.05, dur * 0.40)
            wait_dur = max(0.05, dur * 0.15)

            self.play(FadeIn(text), run_time=max(0.05, text_dur))
            self.play(GrowFromCenter(icon), run_time=max(0.05, icon_dur))
            self.wait(max(0.05, wait_dur))

        # ---------- Beat 13: ML icon pulse and signal trace ----------
        trace_line = VMobject()
        trace_line.set_points_as_corners([
            ml_refs["input_arrows"][0].get_start(),
            ml_refs["nodes"][0].get_center(),
            ml_refs["central"].get_center(),
            ml_refs["out_box"].get_center(),
        ])
        trace_line.set_stroke(YELLOW, width=2.5)

        self.play(ml_icon.animate.scale(1.12), run_time=max(0.05, 0.8))
        self.play(ml_icon.animate.scale(1 / 1.12), run_time=max(0.05, 0.8))
        self.play(Create(trace_line), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 1.54))

        # ---------- Beat 14: continuing research arrow ----------
        improve_arrow = Arrow(
            ch_group.get_bottom() + RIGHT * 0.8 + DOWN * 0.1,
            ch_group.get_bottom() + RIGHT * 2.1 + UP * 0.7,
            color=GREEN, stroke_width=4, max_tip_length_to_length_ratio=0.25,
        )
        self.play(FadeIn(improve_arrow), run_time=max(0.05, 0.4))
        self.play(improve_arrow.animate.scale(1.25), run_time=max(0.05, 0.28))
        self.play(improve_arrow.animate.scale(1 / 1.25), run_time=max(0.05, 0.28))

        # ---------- Beat 15: hold both lists ----------
        self.wait(max(0.05, 5.74))

        # ---------- Beat 16: thought bubble crossed out ----------
        center_glow = Rectangle(width=7.0, height=5.4, fill_color=WHITE,
                                fill_opacity=0.12, stroke_width=0).move_to(ORIGIN)
        thought_bubble = make_thought_bubble()
        red_x = VGroup(
            Line(thought_bubble.get_corner(UL), thought_bubble.get_corner(DR),
                 color=RED, stroke_width=8),
            Line(thought_bubble.get_corner(UR), thought_bubble.get_corner(DL),
                 color=RED, stroke_width=8),
        )

        self.play(adv_group.animate.set_opacity(0.35),
                  ch_group.animate.set_opacity(0.35),
                  run_time=max(0.05, 0.6))
        self.play(FadeIn(center_glow), run_time=max(0.05, 0.4))
        self.play(FadeIn(thought_bubble), run_time=max(0.05, 0.8))
        self.play(Create(red_x), run_time=max(0.05, 1.2))

        # ---------- Beat 17: pattern -> command visual ----------
        pattern_wave_group, command_group, pattern_arrow, _ = make_pattern_parts()
        cross_group = VGroup(thought_bubble, red_x)

        self.play(cross_group.animate.scale(0.45).move_to(LEFT * 4.0 + UP * 1.2),
                  run_time=max(0.05, 1.2))
        self.play(FadeIn(pattern_wave_group), run_time=max(0.05, 1.5))
        self.play(Create(pattern_arrow), run_time=max(0.05, 1.2))
        self.play(FadeIn(command_group), run_time=max(0.05, 1.2))
        self.play(Indicate(pattern_wave_group, color=GREEN, scale_factor=1.1), run_time=max(0.05, 0.6))
        self.play(Indicate(command_group, color=GREEN, scale_factor=1.05), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.78))

        pattern_group = VGroup(pattern_wave_group, pattern_arrow, command_group)
        self.add(pattern_group)

        # ---------- Beat 18: transition upward ----------
        self.play(FadeOut(cross_group), run_time=max(0.05, 0.35))
        self.play(pattern_group.animate.scale(0.7).move_to(np.array([0, 1.7, 0])),
                  run_time=max(0.05, 0.41))

        # ---------- Beat 19: BCI pipeline ----------
        labels = ["Signal Acquisition", "Signal Processing",
                  "Feature Extraction", "Classification"]
        block_colors = [BLUE, TEAL, ORANGE, PURPLE]
        blocks = []
        for lab, col in zip(labels, block_colors):
            rect = RoundedRectangle(width=2.1, height=0.68, corner_radius=0.08,
                                    fill_color=col, fill_opacity=0.25,
                                    stroke_color=col, stroke_width=2)
            txt = Text(lab, font_size=16, weight="BOLD", color=WHITE).scale_to_fit_width(1.8)
            txt.move_to(rect)
            blocks.append(VGroup(rect, txt))

        block_group = VGroup(*blocks).arrange(RIGHT, buff=0.55)
        block_group.move_to(DOWN * 0.3)
        block_arrows = []
        for i in range(3):
            arr = Arrow(blocks[i].get_right(), blocks[i + 1].get_left(),
                        color=GREY_B, stroke_width=2, buff=0.12,
                        max_tip_length_to_length_ratio=0.35)
            block_arrows.append(arr)
        pipeline_group = VGroup(block_group, *block_arrows)
        pipeline_group.scale_to_fit_width(11.0)
        pipeline_group.move_to(DOWN * 0.3)

        per_block = 2.28
        for i in range(4):
            self.play(FadeIn(blocks[i]), run_time=max(0.05, per_block * 0.5))
            self.play(Indicate(blocks[i], color=block_colors[i], scale_factor=1.1),
                      run_time=max(0.05, per_block * 0.25))
            if i < 3:
                self.play(Create(block_arrows[i]), run_time=max(0.05, per_block * 0.10))
            else:
                self.wait(max(0.05, per_block * 0.10))
            self.wait(max(0.05, per_block * 0.15))