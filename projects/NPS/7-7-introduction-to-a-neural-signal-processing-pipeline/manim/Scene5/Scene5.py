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


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        C_RAW = BLUE
        C_PRE = TEAL
        C_FEAT = GREEN
        C_INT = ORANGE
        C_OUT = GOLD

        def make_box(label, color, w, h, fill_opacity, text_size):
            rect = Rectangle(
                width=w,
                height=h,
                fill_color=color,
                fill_opacity=fill_opacity,
                stroke_color=WHITE,
                stroke_width=2,
            )
            text = Text(label, font_size=text_size, color=WHITE, weight="BOLD")
            text.scale_to_fit_width(w - 0.25)
            text.move_to(rect.get_center())
            return VGroup(rect, text)

        def make_row(labels, colors, y, box_w, box_h, fill_opacity, text_size,
                     arrow_opacity=0.8, ghost=False):
            boxes = []
            for lab, col in zip(labels, colors):
                b = make_box(lab, col, box_w, box_h, fill_opacity, text_size)
                if ghost:
                    b[1].set_opacity(0)
                boxes.append(b)
            box_group = VGroup(*boxes).arrange(RIGHT, buff=0.4)
            arrows = VGroup()
            for i in range(len(labels) - 1):
                arr = Arrow(
                    boxes[i].get_right() + RIGHT * 0.05,
                    boxes[i + 1].get_left() + LEFT * 0.05,
                    color=GREY_B,
                    stroke_width=2.5,
                    buff=0.05,
                    max_tip_length_to_length_ratio=0.15,
                )
                arr.set_opacity(arrow_opacity)
                arrows.add(arr)
            whole = VGroup(box_group, arrows)
            whole.move_to(np.array([0, y, 0]))
            return whole, boxes, arrows

        # Top general pipeline
        top_labels = ["Raw Neural Signal", "Preprocessing",
                      "Feature Extraction", "Interpretation / Classification"]
        top_colors = [C_RAW, C_PRE, C_FEAT, C_INT]
        top_whole, top_boxes, top_arrows = make_row(
            top_labels, top_colors, y=2.7,
            box_w=2.3, box_h=0.8,
            fill_opacity=0.85, text_size=13,
            arrow_opacity=0.9, ghost=False,
        )

        # Beat 1: 0.00-3.50
        self.play(FadeIn(top_whole), run_time=max(0.05, 3.5))

        # Beat 2: 3.50-4.70
        self.play(Indicate(top_boxes[0], color=YELLOW, scale_factor=1.12),
                  run_time=max(0.05, 1.2))

        # Beat 3: 4.70-5.68
        self.play(
            top_boxes[0].animate.set_fill(C_RAW, opacity=0.55).set_stroke(WHITE, width=2),
            Indicate(top_boxes[1], color=YELLOW, scale_factor=1.12),
            top_arrows[0].animate.set_stroke(YELLOW, width=5).set_opacity(1),
            run_time=max(0.05, 0.98),
        )

        # Beat 4: 5.68-7.02
        self.play(
            top_boxes[1].animate.set_fill(C_PRE, opacity=0.55).set_stroke(WHITE, width=2),
            Indicate(top_boxes[2], color=YELLOW, scale_factor=1.12),
            top_arrows[1].animate.set_stroke(YELLOW, width=5).set_opacity(1),
            run_time=max(0.05, 1.34),
        )

        # Beat 5: 7.02-8.32
        self.play(
            top_boxes[2].animate.set_fill(C_FEAT, opacity=0.55).set_stroke(WHITE, width=2),
            Indicate(top_boxes[3], color=YELLOW, scale_factor=1.12),
            top_arrows[2].animate.set_stroke(YELLOW, width=5).set_opacity(1),
            run_time=max(0.05, 0.9),
        )
        self.play(
            top_boxes[0].animate.set_fill(C_RAW, opacity=0.85),
            top_boxes[1].animate.set_fill(C_PRE, opacity=0.85),
            top_boxes[2].animate.set_fill(C_FEAT, opacity=0.85),
            top_boxes[3].animate.set_fill(C_INT, opacity=0.85),
            top_arrows[0].animate.set_stroke(WHITE, width=3).set_opacity(1),
            top_arrows[1].animate.set_stroke(WHITE, width=3).set_opacity(1),
            top_arrows[2].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 0.4),
        )

        # Gap 8.32-9.60
        self.wait(max(0.05, 1.28))

        # ------ Pipeline 1: Sleep Staging ------
        p1_labels = ["Raw EEG", "Filtering", "Frequency features",
                     "Classification", "Sleep stage"]
        p1_colors = [C_RAW, C_PRE, C_FEAT, C_INT, C_OUT]
        p1_whole, p1_boxes, p1_arrows = make_row(
            p1_labels, p1_colors, y=0.75,
            box_w=1.65, box_h=0.55,
            fill_opacity=0.12, text_size=12,
            arrow_opacity=0.4, ghost=True,
        )
        p1_label = Text("Sleep Staging", font_size=18, color=WHITE, weight="BOLD")
        p1_label.move_to(p1_whole.get_top() + UP * 0.3)
        p1_label.set_opacity(0)

        p1_icon = Text("☾", font_size=28, color=WHITE).set_opacity(0)
        p1_icon.move_to([p1_whole.get_right()[0] - 0.4, p1_label.get_center()[1], 0])

        p1_group = VGroup(p1_whole, p1_label, p1_icon)

        # Beat 6: 9.60-13.46
        connector = Arrow(
            np.array([0, top_whole.get_bottom()[1] - 0.1, 0]),
            np.array([0, p1_whole.get_top()[1] + 0.15, 0]),
            color=GREY_B, stroke_width=2.5, buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(Create(connector), FadeIn(p1_whole), run_time=max(0.05, 3.86))

        # Beat 7: 13.46-14.72
        self.play(
            p1_boxes[0][0].animate.set_fill(C_RAW, opacity=0.85),
            p1_boxes[0][1].animate.set_opacity(1),
            p1_label.animate.set_opacity(1),
            p1_icon.animate.set_opacity(0.4),
            run_time=max(0.05, 0.9),
        )
        self.play(Indicate(p1_boxes[0], color=YELLOW, scale_factor=1.12),
                  run_time=max(0.05, 0.36))

        # Gap 14.72-15.44
        self.wait(max(0.05, 0.72))

        # Beat 8: 15.44-16.30
        self.play(
            p1_boxes[1][0].animate.set_fill(C_PRE, opacity=0.85),
            p1_boxes[1][1].animate.set_opacity(1),
            p1_arrows[0].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 0.86),
        )

        # Gap 16.30-16.96
        self.wait(max(0.05, 0.66))

        # Beat 9: 16.96-18.22
        self.play(
            p1_boxes[2][0].animate.set_fill(C_FEAT, opacity=0.85),
            p1_boxes[2][1].animate.set_opacity(1),
            p1_arrows[1].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.26),
        )

        # Beat 10: 18.22-19.34
        self.play(
            p1_boxes[3][0].animate.set_fill(C_INT, opacity=0.85),
            p1_boxes[3][1].animate.set_opacity(1),
            p1_arrows[2].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.12),
        )

        # Beat 11: 19.34-19.96
        self.play(
            p1_boxes[4][0].animate.set_fill(C_OUT, opacity=0.85),
            p1_boxes[4][1].animate.set_opacity(1),
            p1_arrows[3].animate.set_stroke(WHITE, width=3).set_opacity(1),
            p1_icon.animate.set_opacity(0.9),
            run_time=max(0.05, 0.62),
        )

        # Gap 19.96-20.72
        self.wait(max(0.05, 0.76))

        # ------ Pipeline 2: Epilepsy Detection ------
        p2_labels = ["Raw EEG", "Preprocessing", "Relevant signal features",
                     "Classification", "Seizure / non-seizure"]
        p2_colors = [C_RAW, C_PRE, C_FEAT, C_INT, C_OUT]
        p2_whole, p2_boxes, p2_arrows = make_row(
            p2_labels, p2_colors, y=-0.30,
            box_w=1.65, box_h=0.55,
            fill_opacity=0.12, text_size=11,
            arrow_opacity=0.4, ghost=True,
        )
        p2_label = Text("Epilepsy Detection", font_size=18, color=WHITE, weight="BOLD")
        p2_label.move_to(p2_whole.get_top() + UP * 0.3)
        p2_label.set_opacity(0)

        p2_icon = SVGMobject(ASSET_PATHS["activity"]).set_color(WHITE).scale_to_fit_height(0.4)
        p2_icon.set_opacity(0)
        p2_icon.move_to([p2_whole.get_right()[0] - 0.4, p2_label.get_center()[1], 0])

        p2_group = VGroup(p2_whole, p2_label, p2_icon)

        # Beat 12: 20.72-22.38
        self.play(
            p1_group.animate.shift(UP * 0.25).set_opacity(0.45),
            FadeIn(p2_whole),
            p2_boxes[0][0].animate.set_fill(C_RAW, opacity=0.85),
            p2_boxes[0][1].animate.set_opacity(1),
            p2_label.animate.set_opacity(1),
            run_time=max(0.05, 1.66),
        )

        # Beat 13: 22.38-23.46
        self.play(
            p2_boxes[1][0].animate.set_fill(C_PRE, opacity=0.85),
            p2_boxes[1][1].animate.set_opacity(1),
            p2_arrows[0].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.08),
        )

        # Gap 23.46-24.36
        self.wait(max(0.05, 0.90))

        # Beat 14: 24.36-26.08
        self.play(
            p2_boxes[2][0].animate.set_fill(C_FEAT, opacity=0.85),
            p2_boxes[2][1].animate.set_opacity(1),
            p2_arrows[1].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.72),
        )

        # Beat 15: 26.08-27.46
        self.play(
            p2_boxes[3][0].animate.set_fill(C_INT, opacity=0.85),
            p2_boxes[3][1].animate.set_opacity(1),
            p2_arrows[2].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.38),
        )

        # Beat 16: 27.46-28.98 (adjusted from 29.22 to avoid overlap)
        self.play(
            p2_boxes[4][0].animate.set_fill(C_OUT, opacity=0.85),
            p2_boxes[4][1].animate.set_opacity(1),
            p2_arrows[3].animate.set_stroke(WHITE, width=3).set_opacity(1),
            p2_icon.animate.set_opacity(0.9),
            run_time=max(0.05, 1.52),
        )

        # ------ Pipeline 3: Movement Analysis ------
        p3_labels = ["Raw EMG", "Filtering", "Amplitude/frequency features",
                     "Interpretation / classification", "Movement information"]
        p3_colors = [C_RAW, C_PRE, C_FEAT, C_INT, C_OUT]
        p3_whole, p3_boxes, p3_arrows = make_row(
            p3_labels, p3_colors, y=-1.45,
            box_w=1.65, box_h=0.55,
            fill_opacity=0.12, text_size=11,
            arrow_opacity=0.4, ghost=True,
        )
        p3_label = Text("Movement Analysis", font_size=18, color=WHITE, weight="BOLD")
        p3_label.move_to(p3_whole.get_top() + UP * 0.3)
        p3_label.set_opacity(0)

        p3_icon_near = SVGMobject(ASSET_PATHS["hand"]).set_color(WHITE).scale_to_fit_height(0.4)
        p3_icon_near.move_to(p3_boxes[0].get_top() + UP * 0.3)
        p3_icon_near.set_opacity(0)

        p3_icon_right = SVGMobject(ASSET_PATHS["hand"]).set_color(WHITE).scale_to_fit_height(0.4)
        p3_icon_right.move_to([p3_whole.get_right()[0] - 0.4, p3_label.get_center()[1], 0])
        p3_icon_right.set_opacity(0)

        # Split-fill overlay for dual interpretation/classification box
        split_overlay = Rectangle(
            width=1.65 / 2,
            height=0.55,
            fill_color=RED,
            fill_opacity=0.85,
            stroke_width=0,
        )
        split_overlay.move_to(p3_boxes[3][0].get_center() + RIGHT * (1.65 / 4))
        split_overlay.set_opacity(0)

        p3_group = VGroup(p3_whole, p3_label, p3_icon_near, p3_icon_right, split_overlay)

        # Beat 17: 28.98-31.66
        self.play(
            p1_group.animate.shift(UP * 0.25).set_opacity(0.35),
            p2_group.animate.shift(UP * 0.25).set_opacity(0.35),
            FadeIn(p3_whole),
            p3_boxes[0][0].animate.set_fill(C_RAW, opacity=0.85),
            p3_boxes[0][1].animate.set_opacity(1),
            p3_label.animate.set_opacity(1),
            p3_icon_near.animate.set_opacity(0.7),
            run_time=max(0.05, 2.68),
        )

        # Beat 18: 31.66-32.82
        self.play(
            p3_boxes[1][0].animate.set_fill(C_PRE, opacity=0.85),
            p3_boxes[1][1].animate.set_opacity(1),
            p3_arrows[0].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.16),
        )

        # Gap 32.82-33.60
        self.wait(max(0.05, 0.78))

        # Beat 19: 33.60-35.32
        self.play(
            p3_boxes[2][0].animate.set_fill(C_FEAT, opacity=0.85),
            p3_boxes[2][1].animate.set_opacity(1),
            p3_arrows[1].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.72),
        )

        # Gap 35.32-35.76
        self.wait(max(0.05, 0.44))

        # Beat 20: 35.76-37.18
        self.play(
            p3_boxes[3][0].animate.set_fill(C_INT, opacity=0.85),
            p3_boxes[3][1].animate.set_opacity(1),
            p3_arrows[2].animate.set_stroke(WHITE, width=3).set_opacity(1),
            split_overlay.animate.set_opacity(1),
            run_time=max(0.05, 1.42),
        )

        # Gap 37.18-38.14
        self.wait(max(0.05, 0.96))

        # Beat 21: 38.14-38.96
        self.play(
            p3_boxes[4][0].animate.set_fill(C_OUT, opacity=0.85),
            p3_boxes[4][1].animate.set_opacity(1),
            p3_arrows[3].animate.set_stroke(WHITE, width=3).set_opacity(1),
            p3_icon_right.animate.set_opacity(0.9),
            run_time=max(0.05, 0.82),
        )

        # Gap 38.96-40.08
        self.wait(max(0.05, 1.12))

        # ------ Pipeline 4: Brain-Computer Interface ------
        p4_labels = ["Raw EEG", "Preprocessing", "Neural features",
                     "Classification", "Control command"]
        p4_colors = [C_RAW, C_PRE, C_FEAT, C_INT, C_OUT]
        p4_whole, p4_boxes, p4_arrows = make_row(
            p4_labels, p4_colors, y=-2.40,
            box_w=1.65, box_h=0.55,
            fill_opacity=0.12, text_size=12,
            arrow_opacity=0.4, ghost=True,
        )
        p4_label = Text("Brain-Computer Interface", font_size=18, color=WHITE, weight="BOLD")
        p4_label.move_to(p4_whole.get_top() + UP * 0.3)
        p4_label.set_opacity(0)

        p4_icon_near = SVGMobject(ASSET_PATHS["brain"]).set_color(WHITE).scale_to_fit_height(0.4)
        p4_icon_near.move_to(p4_boxes[0].get_top() + UP * 0.3)
        p4_icon_near.set_opacity(0)

        p4_group = VGroup(p4_whole, p4_label, p4_icon_near)

        # Beat 22: 40.08-42.04
        self.play(
            p1_group.animate.shift(UP * 0.25).set_opacity(0.25),
            p2_group.animate.shift(UP * 0.25).set_opacity(0.25),
            p3_group.animate.shift(UP * 0.25).set_opacity(0.25),
            FadeIn(p4_whole),
            p4_boxes[0][0].animate.set_fill(C_RAW, opacity=0.85),
            p4_boxes[0][1].animate.set_opacity(1),
            p4_label.animate.set_opacity(1),
            p4_icon_near.animate.set_opacity(0.8),
            run_time=max(0.05, 1.96),
        )

        # Beat 23: 42.04-43.30
        self.play(
            p4_boxes[1][0].animate.set_fill(C_PRE, opacity=0.85),
            p4_boxes[1][1].animate.set_opacity(1),
            p4_arrows[0].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.26),
        )

        # Gap 43.30-44.30
        self.wait(max(0.05, 1.00))

        # Beat 24: 44.30-45.52
        self.play(
            p4_boxes[2][0].animate.set_fill(C_FEAT, opacity=0.85),
            p4_boxes[2][1].animate.set_opacity(1),
            p4_arrows[1].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.22),
        )

        # Gap 45.52-45.66
        self.wait(max(0.05, 0.14))

        # Beat 25: 45.66-46.96
        self.play(
            p4_boxes[3][0].animate.set_fill(C_INT, opacity=0.85),
            p4_boxes[3][1].animate.set_opacity(1),
            p4_arrows[2].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.30),
        )

        # Beat 26: 46.96-48.06
        self.play(
            p4_boxes[4][0].animate.set_fill(C_OUT, opacity=0.85),
            p4_boxes[4][1].animate.set_opacity(1),
            p4_arrows[3].animate.set_stroke(WHITE, width=3).set_opacity(1),
            run_time=max(0.05, 1.10),
        )

        # Beat 27: 48.06-50.44
        self.play(
            p1_group.animate.set_opacity(1),
            p2_group.animate.set_opacity(1),
            p3_group.animate.set_opacity(1),
            p4_group.animate.set_opacity(1),
            top_whole.animate.scale(1.03),
            run_time=max(0.05, 1.2),
        )
        self.play(top_whole.animate.scale(1 / 1.03), run_time=max(0.05, 1.18))

        # Beat 28: 50.44-52.44
        slot2 = [p1_boxes[1], p2_boxes[1], p3_boxes[1], p4_boxes[1]]
        slot3 = [p1_boxes[2], p2_boxes[2], p3_boxes[2], p4_boxes[2]]
        final_out = [p1_boxes[4], p2_boxes[4], p3_boxes[4], p4_boxes[4]]

        for group in (slot2, slot3, final_out):
            for box in group:
                self.play(Indicate(box, color=YELLOW, scale_factor=1.06),
                          run_time=max(0.05, 0.16))
        self.wait(max(0.05, 0.08))

        # Beat 29: 52.44-55.65
        caption = Text("Same general framework, different specifics",
                       font_size=30, color=YELLOW, weight="BOLD")
        caption.to_edge(DOWN, buff=0.25)

        self.play(FadeIn(caption), run_time=max(0.05, 1.2))
        self.play(caption.animate.scale(1.06), run_time=max(0.05, 0.9))
        self.play(caption.animate.scale(1 / 1.06), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 0.21))