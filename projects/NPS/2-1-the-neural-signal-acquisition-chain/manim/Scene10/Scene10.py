ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene10(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helper: build a six-box acquisition chain.
        # ------------------------------------------------------------
        def build_chain(labels, colors, box_w=1.8, box_h=1.45, buff=0.45):
            stage_groups = []
            boxes = []
            for label, color in zip(labels, colors):
                box = Rectangle(
                    width=box_w,
                    height=box_h,
                    stroke_color=WHITE,
                    stroke_width=3,
                    fill_color=color,
                    fill_opacity=0.9,
                )
                title = Text(label, font_size=16, color=WHITE, weight="BOLD")
                title.scale_to_fit_width(box_w - 0.25)
                title.move_to(box.get_center())
                stage_groups.append(VGroup(box, title))
                boxes.append(box)

            chain_boxes = VGroup(*stage_groups).arrange(RIGHT, buff=buff)

            arrows = VGroup()
            for i in range(len(boxes) - 1):
                arrow = Arrow(
                    start=boxes[i].get_right(),
                    end=boxes[i + 1].get_left(),
                    buff=0.18,
                    color=YELLOW,
                    stroke_width=6,
                    max_tip_length_to_length_ratio=0.25,
                )
                arrows.add(arrow)

            full_chain = VGroup(chain_boxes, arrows)
            full_chain.scale_to_fit_width(12.8)
            return full_chain, boxes, arrows

        # ------------------------------------------------------------
        # Previous scene's clean end state: old chain + caption.
        # ------------------------------------------------------------
        old_labels = [
            "Electrode",
            "Amplifier",
            "ADC",
            "Computer",
            "Processing",
            "Display / Analysis",
        ]
        old_colors = [ORANGE, TEAL, GREEN, BLUE, PURPLE, PINK]
        old_full, old_boxes, old_arrows = build_chain(old_labels, old_colors)
        old_full.move_to(ORIGIN + UP * 0.7)

        old_caption = Text(
            "Careful acquisition comes first",
            font_size=28,
            color=GREEN,
            weight="BOLD",
        )
        old_caption.scale_to_fit_width(10.0)
        old_caption.next_to(old_full, DOWN, buff=0.60)

        self.add(old_full, old_caption)

        # ------------------------------------------------------------
        # Beat 1: 0.00 - 1.50
        # Old chain/caption fade out; new six-box chain fades in.
        # ------------------------------------------------------------
        new_labels = [
            "Biological Source",
            "Electrode/Sensor",
            "Amplifier",
            "Filter",
            "ADC",
            "Computer",
        ]
        new_colors = [BLUE, ORANGE, TEAL, PURPLE, GREEN, PINK]
        new_full, new_boxes, new_arrows = build_chain(new_labels, new_colors)
        new_full.move_to(ORIGIN + UP * 0.7)

        self.play(FadeOut(old_full, old_caption), run_time=max(0.05, 0.75))
        self.play(FadeIn(new_full), run_time=max(0.05, 0.75))

        # ------------------------------------------------------------
        # Beat 2: 1.50 - 4.62
        # Full chain steady; caption above fades in.
        # ------------------------------------------------------------
        caption1 = Text(
            "The neural signal acquisition chain",
            font_size=30,
            color=YELLOW,
            weight="BOLD",
        )
        caption1.scale_to_fit_width(11.0)
        caption1.move_to(UP * 3.1)

        self.play(Write(caption1), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 2.12))

        # ------------------------------------------------------------
        # Beat 3: 4.62 - 6.60
        # Camera pans left-to-right; each box highlights as it passes.
        # ------------------------------------------------------------
        first_pos = new_boxes[0].get_center()
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(first_pos),
            run_time=max(0.05, 0.28),
        )

        for i in range(6):
            self.play(
                Indicate(new_boxes[i], scale_factor=1.10, color=YELLOW),
                run_time=max(0.05, 0.14),
            )
            if i < 5:
                self.play(
                    self.camera.frame.animate.move_to(new_boxes[i + 1].get_center()),
                    run_time=max(0.05, 0.10),
                )

        self.wait(max(0.05, 0.36))  # finishes beat 3
        self.wait(max(0.05, 0.94))  # gap to beat 4

        # ------------------------------------------------------------
        # Beat 4: 7.54 - 12.60
        # Pull back to full chain; new caption; sequential box pulses.
        # ------------------------------------------------------------
        caption2 = Text(
            "Every neural recording system follows the same workflow",
            font_size=26,
            color=YELLOW,
            weight="BOLD",
        )
        caption2.scale_to_fit_width(12.0)
        caption2.move_to(UP * 3.1)

        self.play(
            self.camera.frame.animate.scale(2.0).move_to(ORIGIN),
            run_time=max(0.05, 0.60),
        )
        self.play(FadeOut(caption1), Write(caption2), run_time=max(0.05, 0.90))

        for box in new_boxes:
            self.play(
                Indicate(box, scale_factor=1.12, color=YELLOW),
                run_time=max(0.05, 0.42),
            )

        self.wait(max(0.05, 1.04))  # fills beat 4

        # ------------------------------------------------------------
        # Prepare summary labels under each box.
        # ------------------------------------------------------------
        common_label_y = new_full.get_bottom()[1] - 0.32

        label_texts = [
            "Biological Source",
            "Electrode or Sensor",
            "Amplifier",
            "Filter",
            "Analog-to-Digital\nConverter",
            "Computer",
        ]

        under_labels = []
        for i, text in enumerate(label_texts):
            lab = Text(text, font_size=16, color=YELLOW, weight="BOLD")
            lab.scale_to_fit_width(1.9)
            lab.move_to(np.array([new_boxes[i].get_center()[0], common_label_y, 0.0]))
            under_labels.append(lab)

        # ------------------------------------------------------------
        # Beat 5: 12.60 - 14.20
        # Label under first box + highlight.
        # ------------------------------------------------------------
        self.play(Write(under_labels[0]), run_time=max(0.05, 0.70))
        self.play(
            Indicate(new_boxes[0], scale_factor=1.12, color=YELLOW),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.40))
        self.wait(max(0.05, 0.34))  # gap to beat 6

        # ------------------------------------------------------------
        # Beat 6: 14.54 - 15.38
        # Label under second box + highlight.
        # ------------------------------------------------------------
        self.play(
            Write(under_labels[1]),
            Indicate(new_boxes[1], scale_factor=1.12, color=YELLOW),
            run_time=max(0.05, 0.84),
        )
        self.wait(max(0.05, 0.52))  # gap to beat 7

        # ------------------------------------------------------------
        # Beat 7: 15.90 - 16.28
        # Label under third box + highlight.
        # ------------------------------------------------------------
        self.play(
            FadeIn(under_labels[2]),
            Indicate(new_boxes[2], scale_factor=1.12, color=YELLOW),
            run_time=max(0.05, 0.38),
        )
        self.wait(max(0.05, 0.60))  # gap to beat 8

        # ------------------------------------------------------------
        # Beat 8: 16.88 - 17.12
        # Label under fourth box + highlight.
        # ------------------------------------------------------------
        self.play(
            FadeIn(under_labels[3]),
            Indicate(new_boxes[3], scale_factor=1.12, color=YELLOW),
            run_time=max(0.05, 0.24),
        )
        self.wait(max(0.05, 0.60))  # gap to beat 9

        # ------------------------------------------------------------
        # Beat 9: 17.72 - 19.52
        # Labels under fifth and sixth boxes; sequential highlights.
        # ------------------------------------------------------------
        self.play(
            Write(under_labels[4]),
            Indicate(new_boxes[4], scale_factor=1.12, color=YELLOW),
            run_time=max(0.05, 0.75),
        )
        self.play(
            Write(under_labels[5]),
            Indicate(new_boxes[5], scale_factor=1.12, color=YELLOW),
            run_time=max(0.05, 0.75),
        )
        self.wait(max(0.05, 0.30))
        self.wait(max(0.05, 0.92))  # gap to beat 10

        # ------------------------------------------------------------
        # Beat 10: 20.44 - 25.58
        # Fade out under labels; modality icons connect to chain.
        # ------------------------------------------------------------
        self.play(*[FadeOut(lab) for lab in under_labels], run_time=max(0.05, 0.60))

        modality_names = ["EEG", "EMG", "ECoG", "MEG"]
        modality_colors = [BLUE, ORANGE, TEAL, PURPLE]

        modality_icons = VGroup()
        for name, color in zip(modality_names, modality_colors):
            icon = RoundedRectangle(
                width=1.6,
                height=0.6,
                corner_radius=0.18,
                stroke_color=WHITE,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.9,
            )
            label = Text(name, font_size=18, color=WHITE, weight="BOLD")
            label.move_to(icon.get_center())
            modality_icons.add(VGroup(icon, label))

        modality_icons.arrange(RIGHT, buff=0.45)
        modality_icons.move_to(np.array([0.0, common_label_y - 0.95, 0.0]))

        meeting_point = np.array([
            new_boxes[1].get_center()[0],
            new_boxes[1].get_bottom()[1] - 0.08,
            0.0,
        ])

        connection_lines = VGroup()
        for modal in modality_icons:
            modal_group = modal
            line = Arrow(
                start=modal_group.get_top(),
                end=meeting_point,
                buff=0.12,
                color=GREY_B,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.10,
            )
            connection_lines.add(line)

        self.play(
            FadeIn(modality_icons),
            Create(connection_lines),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 3.34))  # fills beat 10

        # ------------------------------------------------------------
        # Beat 11: 25.58 - 27.50
        # Bottom caption fades in.
        # ------------------------------------------------------------
        bottom_caption = Text(
            "The acquisition process remains essentially the same",
            font_size=24,
            color=YELLOW,
            weight="BOLD",
        )
        bottom_caption.scale_to_fit_width(11.0)
        bottom_caption.next_to(modality_icons, DOWN, buff=0.45)

        self.play(Write(bottom_caption), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.92))

        # ------------------------------------------------------------
        # Beat 12: 27.50 - 29.65
        # Entire chain pulses once: brighten, then return.
        # ------------------------------------------------------------
        self.play(
            *[
                b.animate.set_fill(color, opacity=1).set_stroke(YELLOW, width=6)
                for b, color in zip(new_boxes, new_colors)
            ],
            run_time=max(0.05, 0.65),
        )
        self.play(
            *[
                b.animate.set_fill(color, opacity=0.9).set_stroke(WHITE, width=3)
                for b, color in zip(new_boxes, new_colors)
            ],
            run_time=max(0.05, 0.65),
        )
        self.wait(max(0.05, 0.85))  # total runtime to 29.65