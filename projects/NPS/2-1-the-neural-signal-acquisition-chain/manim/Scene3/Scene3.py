ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Geometry / palette -------------------------------------------------
        GREY_SIL = GREY_B
        head_center = np.array([0.0, 2.55, 0.0])
        arm_center = np.array([0.65, 1.45, 0.0])
        eye_center = np.array([0.13, 2.68, 0.0])

        # ---- Human silhouette ---------------------------------------------------
        head_circle = Circle(
            radius=0.35,
            stroke_color=GREY_SIL,
            stroke_width=4.5,
            fill_opacity=0,
        ).move_to(head_center)

        neck_line = Line(
            [0, 2.20, 0], [0, 2.00, 0],
            color=GREY_SIL,
            stroke_width=4.5,
        )
        torso = Polygon(
            [-0.55, 2.00, 0],
            [0.55, 2.00, 0],
            [0.35, -1.10, 0],
            [-0.35, -1.10, 0],
            stroke_color=GREY_SIL,
            stroke_width=4.5,
            fill_opacity=0,
        )
        left_arm = Line(
            [-0.55, 2.00, 0], [-0.95, 0.70, 0],
            color=GREY_SIL,
            stroke_width=4.5,
        )
        right_arm = Line(
            [0.55, 2.00, 0], [0.95, 0.70, 0],
            color=GREY_SIL,
            stroke_width=4.5,
        )
        left_leg = Line(
            [-0.35, -1.10, 0], [-0.45, -2.90, 0],
            color=GREY_SIL,
            stroke_width=4.5,
        )
        right_leg = Line(
            [0.35, -1.10, 0], [0.45, -2.90, 0],
            color=GREY_SIL,
            stroke_width=4.5,
        )

        silhouette = VGroup(
            head_circle, neck_line, torso, left_arm, right_arm, left_leg, right_leg
        )
        silhouette.move_to(ORIGIN)

        # ---- Head highlight & tiny neurons --------------------------------------
        head_highlight = Circle(
            radius=0.52,
            fill_color=ORANGE,
            fill_opacity=0.0,
            stroke_width=0,
        ).move_to(head_center)

        def make_neuron(color=YELLOW, scale=0.28):
            soma = Circle(
                radius=0.12,
                fill_color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=0.5,
            )
            d1 = Line(ORIGIN, [0.18, 0.16, 0], color=color, stroke_width=1.4)
            d2 = Line(ORIGIN, [-0.18, 0.14, 0], color=color, stroke_width=1.4)
            d3 = Line(ORIGIN, [0.02, -0.20, 0], color=color, stroke_width=1.4)
            axon = Line(ORIGIN, [0.24, 0.0, 0], color=color, stroke_width=1.4)
            return VGroup(soma, d1, d2, d3, axon).scale(scale)

        neuron_positions = [
            np.array([-0.15, 2.78, 0]),
            np.array([0.20, 2.52, 0]),
            np.array([0.05, 2.38, 0]),
            np.array([-0.28, 2.48, 0]),
            np.array([0.30, 2.65, 0]),
        ]
        neurons_group = VGroup()
        for pos in neuron_positions:
            n = make_neuron(color=YELLOW, scale=0.28)
            n.move_to(pos)
            neurons_group.add(n)

        # ---- Labels / captions ----------------------------------------------------
        bio_label = Text("Biological Source", font_size=36, color=YELLOW, weight="BOLD")
        bio_label.next_to(silhouette, DOWN, buff=0.2)

        bio_caption = Text(
            "Every recording begins with a biological event occurring inside the body.",
            font_size=24,
            color=WHITE,
        )
        bio_caption.next_to(bio_label, DOWN, buff=0.15)

        head_label = Text("Cortical neurons", font_size=26, color=YELLOW, weight="BOLD")

        arm_label = Text("Muscle fibers", font_size=26, color=YELLOW, weight="BOLD")

        eye_label = Text("Eye muscles", font_size=26, color=YELLOW, weight="BOLD")

        # ---- Prospective region outlines -----------------------------------------
        head_region_outline = Circle(
            radius=0.55,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_opacity=0,
        ).move_to(head_center)

        arm_region_outline = Circle(
            radius=0.42,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_opacity=0,
        ).move_to(arm_center)

        eye_region_outline = Circle(
            radius=0.17,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_opacity=0,
        ).move_to(eye_center)

        small_inset_rect = Rectangle(
            width=1.10,
            height=1.10,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color=GREY,
            fill_opacity=0.08,
        ).move_to([4.50, 0.80, 0])

        head_label.next_to(head_region_outline, UP, buff=0.10)
        arm_label.next_to(arm_region_outline, RIGHT, buff=0.18)
        eye_label.next_to(eye_region_outline, LEFT, buff=0.15)

        # ---- Arm flashes & eye pulses ---------------------------------------------
        def make_jag(start, end, color=YELLOW, stroke_width=2.4):
            v = end - start
            length = np.linalg.norm(v)
            if length < 1e-6:
                return VGroup(Line(start, end, color=color, stroke_width=stroke_width))
            dirn = v / length
            perp = np.array([-dirn[1], dirn[0], 0])
            pts = [start]
            for i in range(1, 3):
                frac = i / 3.0
                off = 0.08 * (1 if i % 2 == 1 else -1)
                pts.append(start + v * frac + perp * off)
            pts.append(end)
            return VGroup(
                *[
                    Line(pts[i], pts[i + 1], color=color, stroke_width=stroke_width)
                    for i in range(len(pts) - 1)
                ]
            )

        arm_lightning = VGroup()
        for offset in [
            np.array([-0.12, 0.24, 0]),
            np.array([0.18, 0.04, 0]),
            np.array([-0.08, -0.22, 0]),
        ]:
            jag = make_jag(np.array([0, 0, 0]), np.array([0.24, 0.14, 0]))
            jag.move_to(arm_center + offset)
            arm_lightning.add(jag)

        eye_pulses = VGroup(
            Line(eye_center + LEFT * 0.25, eye_center + LEFT * 0.10, color=YELLOW, stroke_width=2.4),
            Line(eye_center + UP * 0.25, eye_center + UP * 0.10, color=YELLOW, stroke_width=2.4),
            Line(eye_center + RIGHT * 0.25, eye_center + RIGHT * 0.10, color=YELLOW, stroke_width=2.4),
        )

        # ---- Inset big neuron ------------------------------------------------------
        big_panel_rect = Rectangle(
            width=3.40,
            height=3.00,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color=GREY,
            fill_opacity=0.08,
        ).move_to([4.50, 0.20, 0])

        big_soma = Circle(
            radius=0.16,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to([3.15, 0.15, 0])

        dend1 = Line(big_soma.get_center(), [2.55, 0.60, 0], color=TEAL, stroke_width=3)
        dend2 = Line(big_soma.get_center(), [2.58, 0.05, 0], color=TEAL, stroke_width=3)
        dend3 = Line(big_soma.get_center(), [2.48, -0.45, 0], color=TEAL, stroke_width=3)
        dendb1 = Line([2.55, 0.60, 0], [2.28, 0.88, 0], color=TEAL, stroke_width=2)
        dendb2 = Line([2.58, 0.05, 0], [2.32, 0.20, 0], color=TEAL, stroke_width=2)
        dendrites_group = VGroup(dend1, dend2, dend3, dendb1, dendb2)

        axon_line = Line(big_soma.get_center(), [5.35, 0.15, 0], color=PINK, stroke_width=3)
        big_neuron_group = VGroup(big_soma, dendrites_group, axon_line)

        soma_label = Text("soma", font_size=18, color=WHITE, weight="BOLD")
        soma_label.next_to(big_soma, DOWN, buff=0.08)
        dendrite_label = Text("dendrites", font_size=18, color=TEAL, weight="BOLD")
        dendrite_label.next_to(dendrites_group, UP, buff=0.05)
        axon_label = Text("axon", font_size=18, color=PINK, weight="BOLD")
        axon_label.next_to(axon_line, UP, buff=0.08)
        neuron_labels_group = VGroup(soma_label, dendrite_label, axon_label)

        inset_label = Text("Individual neurons", font_size=28, color=YELLOW, weight="BOLD")
        inset_label.next_to(big_panel_rect, DOWN, buff=0.10)

        spike_dot = Dot(radius=0.07, color=YELLOW)
        spike_dot.move_to(axon_line.get_start())

        # ---- Region highlights (initially invisible) --------------------------------
        arm_highlight = Circle(
            radius=0.42,
            fill_color=ORANGE,
            fill_opacity=0.0,
            stroke_width=0,
        ).move_to(arm_center)

        eye_highlight = Circle(
            radius=0.17,
            fill_color=ORANGE,
            fill_opacity=0.0,
            stroke_width=0,
        ).move_to(eye_center)

        # =====================================================================
        # Beat 1: 0.00–1.46
        # =====================================================================
        self.play(FadeIn(silhouette), run_time=max(0.05, 1.46))

        # Gap: 1.46–2.56
        self.wait(max(0.05, 1.10))

        # =====================================================================
        # Beat 2: 2.56–3.84
        # =====================================================================
        self.play(
            head_highlight.animate.set_fill(ORANGE, opacity=0.55),
            FadeIn(neurons_group),
            FadeIn(bio_label),
            run_time=max(0.05, 1.28),
        )

        # Gap: 3.84–4.56
        self.wait(max(0.05, 0.72))

        # =====================================================================
        # Beat 3: 4.56–8.46
        # =====================================================================
        self.play(FadeIn(bio_caption), run_time=max(0.05, 0.70))

        flash_per = 0.64  # 5 neurons over remaining 3.20 seconds
        for n in neurons_group:
            self.play(
                n.animate.set_color(WHITE).scale(1.2),
                rate_func=rate_functions.there_and_back,
                run_time=max(0.05, flash_per),
            )

        # Gap: 8.46–9.04
        self.wait(max(0.05, 0.58))

        # =====================================================================
        # Beat 4: 9.04–10.44
        # =====================================================================
        self.play(
            head_highlight.animate.set_fill(ORANGE, opacity=0.15),
            neurons_group.animate.set_opacity(0.15),
            FadeIn(head_region_outline),
            FadeIn(arm_region_outline),
            FadeIn(eye_region_outline),
            FadeIn(small_inset_rect),
            FadeOut(bio_caption),
            FadeOut(bio_label),
            run_time=max(0.05, 1.40),
        )

        # Gap: 10.44–11.80
        self.wait(max(0.05, 1.36))

        # =====================================================================
        # Beat 5: 11.80–14.02
        # =====================================================================
        self.play(
            head_highlight.animate.set_fill(ORANGE, opacity=0.60),
            neurons_group.animate.set_opacity(1.0),
            FadeIn(head_label),
            run_time=max(0.05, 0.60),
        )

        flash_per = 0.324  # remaining 1.62 seconds / 5 neurons
        for n in neurons_group:
            self.play(
                n.animate.set_color(WHITE).scale(1.25),
                rate_func=rate_functions.there_and_back,
                run_time=max(0.05, flash_per),
            )

        # Gap: 14.02–14.92
        self.wait(max(0.05, 0.90))

        # =====================================================================
        # Beat 6: 14.92–15.20
        # =====================================================================
        self.play(
            head_highlight.animate.set_fill(ORANGE, opacity=0.15),
            arm_highlight.animate.set_fill(ORANGE, opacity=0.55),
            FadeIn(arm_lightning),
            FadeIn(arm_label),
            run_time=max(0.05, 0.28),
        )

        # Gap: 15.20–15.80
        self.wait(max(0.05, 0.60))

        # =====================================================================
        # Beat 7: 15.80–16.24
        # =====================================================================
        self.play(
            arm_highlight.animate.set_fill(ORANGE, opacity=0.15),
            arm_lightning.animate.set_opacity(0),
            eye_highlight.animate.set_fill(ORANGE, opacity=0.60),
            FadeIn(eye_pulses),
            FadeIn(eye_label),
            run_time=max(0.05, 0.44),
        )

        # Gap: 16.24–16.68
        self.wait(max(0.05, 0.44))

        # =====================================================================
        # Beat 8: 16.68–17.68
        # =====================================================================
        self.play(
            ReplacementTransform(small_inset_rect, big_panel_rect),
            FadeIn(big_neuron_group),
            FadeIn(neuron_labels_group),
            FadeIn(inset_label),
            FadeIn(spike_dot),
            eye_highlight.animate.set_fill(ORANGE, opacity=0.15),
            eye_pulses.animate.set_opacity(0),
            run_time=max(0.05, 0.60),
        )

        self.play(
            spike_dot.animate.move_to(axon_line.get_end()),
            rate_func=linear,
            run_time=max(0.05, 0.40),
        )

        # Gap: 17.68–18.68
        self.wait(max(0.05, 1.00))

        # =====================================================================
        # Beat 9: 18.68–20.50
        # =====================================================================
        no_signal_caption = Text(
            "Without this physiological activity, there is simply no signal to record.",
            font_size=24,
            color=WHITE,
        )
        no_signal_caption.move_to([0, -3.20, 0])

        self.play(
            head_highlight.animate.set_fill(ORANGE, opacity=0.22),
            arm_highlight.animate.set_fill(ORANGE, opacity=0.22),
            eye_highlight.animate.set_fill(ORANGE, opacity=0.22),
            big_neuron_group.animate.set_opacity(0.85),
            FadeIn(no_signal_caption),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.62))

        # Gap: 20.50–21.30
        self.wait(max(0.05, 0.80))

        # =====================================================================
        # Beat 10: 21.30–22.86
        # =====================================================================
        head_region_group = VGroup(
            head_highlight, head_region_outline, neurons_group, head_label
        )
        arm_region_group = VGroup(
            arm_highlight, arm_region_outline, arm_label, arm_lightning
        )
        eye_region_group = VGroup(
            eye_highlight, eye_region_outline, eye_label, eye_pulses
        )
        inset_region_group = VGroup(
            big_panel_rect,
            big_neuron_group,
            neuron_labels_group,
            inset_label,
            spike_dot,
        )

        for group in [
            head_region_group,
            arm_region_group,
            eye_region_group,
            inset_region_group,
        ]:
            self.play(FadeOut(group), run_time=max(0.05, 0.39))

        # Gap: 22.86–23.30
        self.wait(max(0.05, 0.44))

        # =====================================================================
        # Beat 11: 23.30–25.80
        # =====================================================================
        bold_caption = Text(
            "no activity = no signal",
            font_size=38,
            color=WHITE,
            weight="BOLD",
        )
        bold_caption.move_to(no_signal_caption.get_center())

        self.play(
            silhouette.animate.set_opacity(0.45),
            Transform(no_signal_caption, bold_caption),
            run_time=max(0.05, 1.0),
        )

        self.wait(max(0.05, 1.50))