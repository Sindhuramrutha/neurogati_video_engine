ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def make_small_human(self, height=0.5, color=TEAL):
        head = Circle(radius=0.1, fill_color=color, fill_opacity=1,
                      stroke_color=WHITE, stroke_width=1.2).shift(UP * 0.22)
        body = Ellipse(width=0.45, height=0.32, fill_color=color, fill_opacity=1,
                       stroke_color=WHITE, stroke_width=1.2).shift(DOWN * 0.06)
        human = VGroup(head, body)
        human.scale_to_fit_height(height)
        return human

    def make_small_equipment(self, height=0.4, color=BLUE):
        box = RoundedRectangle(corner_radius=0.05, width=0.5, height=0.35,
                               fill_color=color, fill_opacity=1,
                               stroke_color=WHITE, stroke_width=1.2)
        screen = Rectangle(width=0.22, height=0.14, fill_color=WHITE,
                           fill_opacity=0.85, stroke_width=0).move_to(box.get_center() + UP * 0.05)
        knob = Dot(box.get_center() + DOWN * 0.09, radius=0.03, color=YELLOW, stroke_width=0)
        equip = VGroup(box, screen, knob)
        equip.scale_to_fit_height(height)
        return equip

    def make_electrode_icon(self, array=False, color=YELLOW):
        if array:
            tips = VGroup(
                *[Line(UP * 0.1, DOWN * 0.1, color=color, stroke_width=2).shift(RIGHT * x)
                  for x in (-0.2, 0, 0.2)]
            )
            base = Line(LEFT * 0.2 + DOWN * 0.15, RIGHT * 0.2 + DOWN * 0.15,
                        color=WHITE, stroke_width=3)
            return VGroup(base, tips)
        line = Line(DOWN * 0.25, UP * 0.15, color=WHITE, stroke_width=3)
        tip = Circle(radius=0.06, fill_color=color, fill_opacity=1,
                     stroke_color=WHITE, stroke_width=1).move_to(UP * 0.2)
        return VGroup(line, tip)

    def make_smooth_wave_icon(self, width=1.3, height=0.22, color=YELLOW, freq=6):
        xs = np.linspace(-width / 2, width / 2, 60)
        pts = [np.array([x, height * np.sin(freq * x), 0]) for x in xs]
        wave = VMobject().set_points_as_corners(pts).set_stroke(color, width=3)
        return wave

    def make_noisy_wave_icon(self, width=1.3, height=0.25, color=ORANGE):
        xs = np.linspace(-width / 2, width / 2, 70)
        pts = []
        for i, x in enumerate(xs):
            y = 0.18 * np.sin(7 * x) + 0.06 * np.sin(27 * x + i)
            pts.append(np.array([x, y, 0]))
        wave = VMobject().set_points_as_corners(pts).set_stroke(color, width=3)
        return wave

    def make_adc_wave_icon(self, width=1.8, height=0.28, color=YELLOW):
        left_xs = np.linspace(-0.75, -0.2, 28)
        left_pts = [np.array([x, height * np.sin(5 * (x + 0.75)), 0]) for x in left_xs]
        step_xs = [-0.2, -0.05, -0.05, 0.1, 0.1, 0.25, 0.25, 0.4, 0.4, 0.55, 0.55, 0.7, 0.7, 0.85]
        step_ys = [height * 0.8, height * 0.8, -height * 0.5, -height * 0.5,
                   height * 0.5, height * 0.5, -height * 0.7, -height * 0.7,
                   height * 0.7, height * 0.7, -height * 0.4, -height * 0.4,
                   height * 0.4, height * 0.4]
        right_pts = [np.array([x, y, 0]) for x, y in zip(step_xs, step_ys)]
        wave = VMobject().set_points_as_corners(left_pts + right_pts).set_stroke(color, width=3)
        return wave

    def make_card(self, text_str, top_icon, card_width=7.2, card_height=2.4):
        bg = RoundedRectangle(corner_radius=0.18, width=card_width, height=card_height,
                              fill_color=BLUE, fill_opacity=0.12,
                              stroke_color=BLUE, stroke_width=2)
        top_icon_copy = top_icon.copy()
        top_icon_copy.scale_to_fit_width(5.8)
        if top_icon_copy.height > 0.8:
            top_icon_copy.scale_to_fit_height(0.8)
        top_icon_copy.move_to(bg.get_top() + DOWN * 0.45)
        text_m = Text(text_str, font_size=18, color=WHITE, line_spacing=0.6)
        text_m.scale_to_fit_width(6.2)
        text_m.move_to(bg.get_center() + DOWN * 0.55)
        return VGroup(bg, top_icon_copy, text_m)

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Beat 1: 0.00-2.24 ----
        prev_bullets = VGroup(*[
            Text("•  " + t, font_size=20, color=WHITE)
            for t in [
                "Neural recording systems connect electronic equipment to the human body",
                "Electrical safety is essential for protecting both participants and equipment",
                "Electrical isolation separates the participant from hazardous circuits while still allowing physiological signals to be recorded",
                "Safe recording practices and properly designed biomedical equipment are fundamental to every neural signal acquisition system",
            ]
        ]).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(ORIGIN)

        module_title = Text("Module Complete", font_size=72, color=WHITE, weight=BOLD)
        module_subtitle = Text("Neural Signal Acquisition", font_size=30, color=GREY_B)
        module_subtitle.next_to(module_title, DOWN, buff=0.25)
        title_group = VGroup(module_title, module_subtitle).move_to(np.array([0, 3.0, 0]))

        self.add(prev_bullets)
        self.play(FadeOut(prev_bullets), run_time=max(0.05, 1.0))
        self.play(FadeIn(title_group), run_time=max(0.05, 1.24))

        # Gap to 2.76
        self.wait(max(0.05, 0.52))

        # ---- Beat 2: 2.76-6.66 ----
        node_labels = ["Biological Activity", "Electrodes/Sensors", "Amplification",
                       "Signal Conditioning", "ADC", "Digital Data"]
        body_colors = [TEAL, BLUE, PURPLE, GREEN, ORANGE, PINK]
        xs = np.array([-5.75, -3.45, -1.15, 1.15, 3.45, 5.75])
        body_y = 0.75
        label_y = 0.05

        bodies = []
        labels = []
        for i, label in enumerate(node_labels):
            rect = RoundedRectangle(corner_radius=0.12, width=1.7, height=0.85,
                                    fill_color=body_colors[i], fill_opacity=0.85,
                                    stroke_color=WHITE, stroke_width=2)
            rect.move_to(np.array([xs[i], body_y, 0]))
            bodies.append(rect)
            txt = Text(label, font_size=15, color=WHITE)
            txt.move_to(np.array([xs[i], label_y, 0]))
            labels.append(txt)

        arrows = []
        for i in range(5):
            ar = Arrow(bodies[i].get_right(), bodies[i + 1].get_left(), buff=0.2,
                       color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.35)
            arrows.append(ar)

        shield_shape = Polygon(
            np.array([-5.5, -0.85, 0]),
            np.array([5.5, -0.85, 0]),
            np.array([4.6, -1.35, 0]),
            np.array([0, -1.8, 0]),
            np.array([-4.6, -1.35, 0]),
        ).move_to(np.array([0, -0.6, 0]))
        shield_shape.set_fill(GREEN, opacity=0.75).set_stroke(WHITE, width=2)
        shield_label = Text("Safety & Isolation", font_size=18, color=WHITE)
        shield_label.move_to(shield_shape.get_center())
        shield_group = VGroup(shield_shape, shield_label)

        flow_group = VGroup(*bodies, *labels, *arrows, shield_group)

        for i in range(6):
            self.play(GrowFromCenter(bodies[i]), FadeIn(labels[i]), run_time=max(0.05, 0.28))
            if i < 5:
                self.play(Create(arrows[i]), run_time=max(0.05, 0.22))
        self.play(FadeIn(shield_group), run_time=max(0.05, 1.12))

        # Gap to 7.48
        self.wait(max(0.05, 0.82))

        # ---- Beat 3: 7.48-9.02 ----
        glow0 = SurroundingRectangle(bodies[0], color=YELLOW, buff=0.14,
                                     stroke_width=5, corner_radius=0.10).set_fill(YELLOW, opacity=0)
        self.play(FadeIn(glow0), run_time=max(0.05, 0.30))
        self.play(bodies[0].animate.scale(1.18).set_fill(ORANGE, opacity=1.0).set_stroke(YELLOW, width=4),
                  labels[0].animate.set_color(YELLOW), run_time=max(0.05, 0.50))
        self.play(bodies[0].animate.scale(1 / 1.18), run_time=max(0.05, 0.35))
        self.play(glow0.animate.scale(1.35).set_opacity(0), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.09))

        # Gap to 9.32
        self.wait(max(0.05, 0.30))

        # ---- Beat 4: 9.32-13.44 ----
        glow1 = SurroundingRectangle(bodies[1], color=YELLOW, buff=0.14,
                                     stroke_width=5, corner_radius=0.10).set_fill(YELLOW, opacity=0)
        self.play(FadeIn(glow1), run_time=max(0.05, 0.30))
        self.play(bodies[1].animate.scale(1.18).set_fill(ORANGE, opacity=1.0).set_stroke(YELLOW, width=4),
                  labels[1].animate.set_color(YELLOW), run_time=max(0.05, 0.50))
        self.play(bodies[1].animate.scale(1 / 1.18), run_time=max(0.05, 0.35))
        electrode_icon = self.make_electrode_icon().move_to(bodies[1].get_top() + UP * 0.45)
        self.play(Create(electrode_icon), run_time=max(0.05, 0.60))
        self.play(FadeOut(electrode_icon), run_time=max(0.05, 0.60))
        self.play(glow1.animate.scale(1.35).set_opacity(0), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 1.42))

        # Gap to 13.92
        self.wait(max(0.05, 0.48))

        # ---- Beat 5: 13.92-15.44 ----
        glow2 = SurroundingRectangle(bodies[2], color=YELLOW, buff=0.14,
                                     stroke_width=5, corner_radius=0.10).set_fill(YELLOW, opacity=0)
        self.play(FadeIn(glow2), run_time=max(0.05, 0.15))
        self.play(bodies[2].animate.scale(1.18).set_fill(ORANGE, opacity=1.0).set_stroke(YELLOW, width=4),
                  labels[2].animate.set_color(YELLOW), run_time=max(0.05, 0.40))
        self.play(bodies[2].animate.scale(1 / 1.18), run_time=max(0.05, 0.20))
        up_arrow = Arrow(ORIGIN, UP * 0.7, color=GOLD, stroke_width=5,
                         max_tip_length_to_length_ratio=0.35).next_to(bodies[2], UP, buff=0.2)
        self.play(Create(up_arrow), up_arrow.animate.shift(UP * 0.25), run_time=max(0.05, 0.30))
        self.play(FadeOut(up_arrow), run_time=max(0.05, 0.20))
        self.play(glow2.animate.scale(1.35).set_opacity(0), run_time=max(0.05, 0.15))
        self.wait(max(0.05, 0.12))

        # Gap to 16.32
        self.wait(max(0.05, 0.88))

        # ---- Beat 6: 16.32-17.56 ----
        glow3 = SurroundingRectangle(bodies[3], color=YELLOW, buff=0.14,
                                     stroke_width=5, corner_radius=0.10).set_fill(YELLOW, opacity=0)
        self.play(FadeIn(glow3), run_time=max(0.05, 0.15))
        self.play(bodies[3].animate.scale(1.18).set_fill(ORANGE, opacity=1.0).set_stroke(YELLOW, width=4),
                  labels[3].animate.set_color(YELLOW), run_time=max(0.05, 0.35))
        self.play(bodies[3].animate.scale(1 / 1.18), run_time=max(0.05, 0.20))
        smooth_wave_icon = self.make_smooth_wave_icon(width=1.0, height=0.15).move_to(bodies[3].get_center())
        self.play(Create(smooth_wave_icon), run_time=max(0.05, 0.25))
        self.play(FadeOut(smooth_wave_icon), run_time=max(0.05, 0.15))
        self.play(glow3.animate.scale(1.35).set_opacity(0), run_time=max(0.05, 0.14))
        # no additional wait needed, total 1.24

        # Gap to 18.56
        self.wait(max(0.05, 1.0))

        # ---- Beat 7: 18.56-21.64 ----
        glow4 = SurroundingRectangle(bodies[4], color=YELLOW, buff=0.14,
                                     stroke_width=5, corner_radius=0.10).set_fill(YELLOW, opacity=0)
        self.play(FadeIn(glow4), run_time=max(0.05, 0.20))
        self.play(bodies[4].animate.scale(1.18).set_fill(ORANGE, opacity=1.0).set_stroke(YELLOW, width=4),
                  labels[4].animate.set_color(YELLOW), run_time=max(0.05, 0.45))
        self.play(bodies[4].animate.scale(1 / 1.18), run_time=max(0.05, 0.30))
        adc_wave_icon = self.make_adc_wave_icon(width=1.4, height=0.20).move_to(bodies[4].get_center())
        self.play(Create(adc_wave_icon), run_time=max(0.05, 0.70))
        self.play(FadeOut(adc_wave_icon), run_time=max(0.05, 0.60))
        self.play(glow4.animate.scale(1.35).set_opacity(0), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.58))

        # Gap to 22.48
        self.wait(max(0.05, 0.84))

        # ---- Beat 8: 22.48-25.62 ----
        self.play(shield_group.animate.scale(1.12).set_color(GREEN), run_time=max(0.05, 0.40))
        self.play(shield_group.animate.scale(1 / 1.12), run_time=max(0.05, 0.40))
        self.play(flow_group.animate.scale(1.03), run_time=max(0.05, 0.50))
        self.play(flow_group.animate.scale(1 / 1.03), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.34))

        # Gap to 26.74
        self.wait(max(0.05, 1.26))

        # ---- Beat 9: 26.74-33.04 ----
        # Move flow up
        self.play(flow_group.animate.shift(UP * 0.9), run_time=max(0.05, 0.9))

        # Build concept cards
        mini_flow = VGroup(*[
            RoundedRectangle(corner_radius=0.04, width=0.4, height=0.22,
                             fill_color=body_colors[i], fill_opacity=0.9,
                             stroke_color=WHITE, stroke_width=1)
            for i in range(6)
        ]).arrange(RIGHT, buff=0.35)
        mini_flow.scale_to_fit_width(5.8)

        card1 = self.make_card(
            "The acquisition chain provides the complete pathway from biological activity to digital data",
            mini_flow)

        electrode_single = self.make_electrode_icon(array=False).scale_to_fit_height(0.55)
        electrode_array = self.make_electrode_icon(array=True).scale_to_fit_height(0.55)
        e_label1 = Text("Electrodes", font_size=14, color=GOLD)
        e_label2 = Text("Sensors", font_size=14, color=GOLD)
        e1_group = VGroup(electrode_single, e_label1).arrange(DOWN, buff=0.1)
        e2_group = VGroup(electrode_array, e_label2).arrange(DOWN, buff=0.1)
        card2_top = VGroup(e1_group, e2_group).arrange(RIGHT, buff=0.7)
        card2 = self.make_card(
            "Different recording modalities use different electrodes or sensors depending on the application",
            card2_top)

        wave_in_small = self.make_smooth_wave_icon(width=0.75, height=0.14, color=YELLOW)
        wave_out_large = self.make_smooth_wave_icon(width=1.6, height=0.25, color=GOLD)
        amp_tri = Polygon(LEFT * 0.3 + UP * 0.2, LEFT * 0.3 + DOWN * 0.2, RIGHT * 0.35)
        amp_tri.set_fill(ORANGE, opacity=1).set_stroke(WHITE, width=1.5)
        card3_top = VGroup(wave_in_small, amp_tri, wave_out_large).arrange(RIGHT, buff=0.25)
        card3 = self.make_card(
            "Amplification increases the strength of weak biological signals",
            card3_top)

        noisy_in = self.make_noisy_wave_icon(width=0.9, height=0.18)
        filter_block = Rectangle(width=0.7, height=0.6, fill_color=GREEN, fill_opacity=0.85,
                                 stroke_color=WHITE, stroke_width=1.5)
        clean_out = self.make_smooth_wave_icon(width=1.1, height=0.16, color=GREEN)
        card4_top = VGroup(noisy_in, filter_block, clean_out).arrange(RIGHT, buff=0.25)
        card4 = self.make_card(
            "Signal conditioning prepares the signal for accurate digitization",
            card4_top)

        adc_block = VGroup(
            RoundedRectangle(corner_radius=0.08, width=0.7, height=0.5,
                             fill_color=ORANGE, fill_opacity=0.9,
                             stroke_color=WHITE, stroke_width=1.5),
            Text("ADC", font_size=14, color=WHITE)
        )
        adc_continuous = self.make_smooth_wave_icon(width=0.85, height=0.22, color=YELLOW)
        adc_steps = self.make_adc_wave_icon(width=1.3, height=0.18, color=YELLOW)
        card5_top = VGroup(adc_continuous, adc_block, adc_steps).arrange(RIGHT, buff=0.25)
        card5 = self.make_card(
            "Sampling and ADC convert continuous analogue signals into digital data suitable for computer analysis",
            card5_top)

        human_left = self.make_small_human(height=0.45, color=TEAL).move_to(LEFT * 1.15)
        equip_right = self.make_small_equipment(height=0.42, color=BLUE).move_to(RIGHT * 1.15)
        barrier = DashedLine(UP * 0.35, DOWN * 0.35, dash_length=0.08,
                             color=GREY_B, stroke_width=3)
        green_xs = np.linspace(-1.1, 1.1, 40)
        green_wave = VMobject().set_points_as_corners(
            [np.array([x, 0.10 * np.sin(6 * x), 0]) for x in green_xs]
        ).set_stroke(GREEN, width=3)
        red_zig_pts = [np.array([-1.5 + 0.12 * i, 0.10 if i % 2 == 0 else -0.10, 0])
                       for i in range(8)]
        red_zig = VMobject().set_points_as_corners(red_zig_pts).set_stroke(RED, width=3)
        card6_top = VGroup(human_left, equip_right, barrier, green_wave, red_zig)
        card6 = self.make_card(
            "Electrical safety and isolation are essential to protect both participants and recording equipment",
            card6_top)

        self.cards = [card1, card2, card3, card4, card5, card6]
        card_pos = np.array([0, -2.2, 0])
        for card in self.cards:
            card.move_to(card_pos)

        # Show card1
        card1.move_to(card_pos + LEFT * 10).set_opacity(0)
        self.add(card1)
        self.play(card1.animate.move_to(card_pos).set_opacity(1), run_time=max(0.05, 1.4))
        # Wait until end of beat
        self.wait(max(0.05, 4.0))

        # Gap to 33.72
        self.wait(max(0.05, 0.68))

        # ---- Beat 10: 33.72-38.38 ----
        # Flip card1 out, card2 in
        card2.move_to(card_pos + LEFT * 10).set_opacity(0)
        self.add(card2)
        self.play(card1.animate.shift(RIGHT * 10).set_opacity(0),
                  card2.animate.move_to(card_pos).set_opacity(1), run_time=max(0.05, 1.4))
        self.remove(card1)
        self.wait(max(0.05, 3.26))

        # Gap to 39.20
        self.wait(max(0.05, 0.82))

        # ---- Beat 11: 39.20-42.62 ----
        card3.move_to(card_pos + LEFT * 10).set_opacity(0)
        self.add(card3)
        self.play(card2.animate.shift(RIGHT * 10).set_opacity(0),
                  card3.animate.move_to(card_pos).set_opacity(1), run_time=max(0.05, 1.3))
        self.remove(card2)
        self.wait(max(0.05, 2.12))

        # Gap to 43.34
        self.wait(max(0.05, 0.72))

        # ---- Beat 12: 43.34-46.62 ----
        card4.move_to(card_pos + LEFT * 10).set_opacity(0)
        self.add(card4)
        self.play(card3.animate.shift(RIGHT * 10).set_opacity(0),
                  card4.animate.move_to(card_pos).set_opacity(1), run_time=max(0.05, 1.2))
        self.remove(card3)
        self.wait(max(0.05, 2.08))

        # Gap to 47.48
        self.wait(max(0.05, 0.86))

        # ---- Beat 13: 47.48-53.92 ----
        card5.move_to(card_pos + LEFT * 10).set_opacity(0)
        self.add(card5)
        self.play(card4.animate.shift(RIGHT * 10).set_opacity(0),
                  card5.animate.move_to(card_pos).set_opacity(1), run_time=max(0.05, 1.5))
        self.remove(card4)
        self.wait(max(0.05, 4.94))

        # Gap to 54.80
        self.wait(max(0.05, 0.88))

        # ---- Beat 14: 54.80-60.78 ----
        card6.move_to(card_pos + LEFT * 10).set_opacity(0)
        self.add(card6)
        self.play(card5.animate.shift(RIGHT * 10).set_opacity(0),
                  card6.animate.move_to(card_pos).set_opacity(1), run_time=max(0.05, 1.5))
        self.remove(card5)
        self.wait(max(0.05, 4.48))

        # Gap to 61.56
        self.wait(max(0.05, 0.78))

        # ---- Beat 15: 61.56-65.44 ----
        # card6 flips out
        self.play(card6.animate.shift(RIGHT * 10).set_opacity(0), run_time=max(0.05, 0.9))
        self.remove(card6)

        fan_cards = VGroup(*[
            RoundedRectangle(corner_radius=0.08, width=1.2, height=1.6,
                             fill_color=color, fill_opacity=0.85,
                             stroke_color=WHITE, stroke_width=1.5)
            for color in [BLUE, TEAL, GREEN, ORANGE, PURPLE, PINK]
        ])
        for i, cardrect in enumerate(fan_cards):
            cardrect.rotate(PI / 10 * (i - 2.5))
            cardrect.shift(RIGHT * 0.3 * (i - 2.5))
        fan_cards.move_to(np.array([0, -0.4, 0]))

        foundation_text = Text("Foundation of Neural Signal Acquisition",
                               font_size=25, color=GOLD)
        foundation_text.next_to(fan_cards, DOWN, buff=0.45)

        self.play(FadeIn(fan_cards), run_time=max(0.05, 1.0))
        self.play(fan_cards.animate.scale(0.6), run_time=max(0.05, 0.5))

        glow_fan = SurroundingRectangle(fan_cards, color=YELLOW, buff=0.12,
                                        stroke_width=4).set_fill(YELLOW, opacity=0)
        self.play(FadeIn(foundation_text), run_time=max(0.05, 0.8))
        self.add(glow_fan)
        self.play(glow_fan.animate.scale(1.4).set_opacity(0), run_time=max(0.05, 0.68))

        # Gap to 66.54
        self.wait(max(0.05, 1.10))

        # ---- Beat 16: 66.54-77.17 ----
        review_group = VGroup(flow_group, fan_cards, foundation_text)

        module_labels_list = ["Preprocessing", "Filtering & Frequency Analysis", "Applications"]
        module_boxes_list = []
        for mod_label in module_labels_list:
            rect = Rectangle(width=4.2, height=0.8, stroke_color=WHITE,
                             fill_color=BLUE, fill_opacity=0.15, stroke_width=2)
            txt = Text(mod_label, font_size=19, color=WHITE)
            module_boxes_list.append(VGroup(rect, txt))
        module_boxes = VGroup(*module_boxes_list).arrange(DOWN, buff=0.55)
        module_boxes.move_to(np.array([3.4, 0, 0]))

        right_arrow1 = Arrow(module_boxes[0].get_bottom(), module_boxes[1].get_top(),
                             buff=0.15, color=GREY_B, stroke_width=3)
        right_arrow2 = Arrow(module_boxes[1].get_bottom(), module_boxes[2].get_top(),
                             buff=0.15, color=GREY_B, stroke_width=3)

        self.play(review_group.animate.scale(0.45).move_to(np.array([-3.2, 0, 0])), run_time=max(0.05, 1.6))
        self.play(FadeIn(module_boxes[0]), run_time=max(0.05, 1.2))
        self.play(FadeIn(module_boxes[1]), FadeIn(right_arrow1), run_time=max(0.05, 1.2))
        self.play(FadeIn(module_boxes[2]), FadeIn(right_arrow2), run_time=max(0.05, 1.2))

        # Pulse at approx 74.5 (we are at 66.54+1.6+3.6 = 71.74; wait until 74.05? Actually brief says 74.5 seconds approximate)
        # We'll add a small wait then pulse. To keep total, compute remaining: 77.17 - 71.74 = 5.43.
        # Use wait 3.53, pulse 0.45+0.45=0.9, then final wait 1.0
        self.wait(max(0.05, 3.53))
        self.play(module_boxes.animate.scale(1.05), run_time=max(0.05, 0.45))
        self.play(module_boxes.animate.scale(1 / 1.05), run_time=max(0.05, 0.45))

        # Final hold to exact end
        self.wait(max(0.05, 1.0))