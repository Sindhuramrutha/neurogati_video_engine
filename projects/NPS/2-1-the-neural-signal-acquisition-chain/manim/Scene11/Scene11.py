ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene11(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helper: build the six-box acquisition chain used in Scene 10.
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
            return full_chain, stage_groups, boxes, arrows

        # ------------------------------------------------------------
        # Recreate the previous scene's exact final state.
        # ------------------------------------------------------------
        labels = [
            "Biological Source",
            "Electrode/Sensor",
            "Amplifier",
            "Filter",
            "ADC",
            "Computer",
        ]
        colors = [BLUE, ORANGE, TEAL, PURPLE, GREEN, PINK]

        full_chain, stage_groups, boxes, arrows = build_chain(labels, colors)
        full_chain.move_to(ORIGIN + UP * 0.7)

        top_caption = Text(
            "Every neural recording system follows the same workflow",
            font_size=26,
            color=YELLOW,
            weight="BOLD",
        )
        top_caption.scale_to_fit_width(12.0)
        top_caption.move_to(UP * 3.1)

        common_label_y = full_chain.get_bottom()[1] - 0.32

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
            boxes[1].get_center()[0],
            boxes[1].get_bottom()[1] - 0.08,
            0.0,
        ])

        connection_lines = VGroup()
        for modal in modality_icons:
            line = Arrow(
                start=modal.get_top(),
                end=meeting_point,
                buff=0.12,
                color=GREY_B,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.10,
            )
            connection_lines.add(line)

        bottom_caption = Text(
            "The acquisition process remains essentially the same",
            font_size=24,
            color=YELLOW,
            weight="BOLD",
        )
        bottom_caption.scale_to_fit_width(11.0)
        bottom_caption.next_to(modality_icons, DOWN, buff=0.45)

        self.add(full_chain, top_caption, modality_icons, connection_lines, bottom_caption)

        # ------------------------------------------------------------
        # Beat 1: 0.00 - 2.30
        # Fade everything except the chain; center the chain.
        # ------------------------------------------------------------
        fade_extras = [top_caption, modality_icons, connection_lines, bottom_caption]
        self.play(
            FadeOut(*fade_extras),
            full_chain.animate.move_to(ORIGIN),
            run_time=max(0.05, 2.30),
        )

        # ------------------------------------------------------------
        # Beat 2: 2.30 - 3.64
        # Gentle camera zoom toward Electrode/Sensor; dim other boxes.
        # ------------------------------------------------------------
        electrode_group = stage_groups[1]
        other_indices = [0, 2, 3, 4, 5]
        dim_anims = [stage_groups[i].animate.set_opacity(0.25) for i in other_indices]

        self.play(
            self.camera.frame.animate.scale(0.72).move_to(electrode_group.get_center()),
            *dim_anims,
            arrows.animate.set_opacity(0.30),
            run_time=max(0.05, 1.34),
        )

        # ------------------------------------------------------------
        # Beat 3: 3.64 - 6.00
        # Fade all but Electrode/Sensor; move it to center and enlarge.
        # Then settle a soft glow around it.
        # ------------------------------------------------------------
        cam_reset_scale = 1.0 / 0.72
        fade_others = [
            FadeOut(stage_groups[i]) for i in other_indices
        ] + [FadeOut(arrows)]

        self.play(
            self.camera.frame.animate.scale(cam_reset_scale).move_to(ORIGIN),
            *fade_others,
            electrode_group.animate.move_to(ORIGIN).scale(2.5),
            run_time=max(0.05, 1.56),
        )

        glow = VGroup()
        for size_mult, fill_op, stroke_w in [(1.18, 0.10, 4), (1.36, 0.05, 2)]:
            halo = RoundedRectangle(
                width=electrode_group.width * size_mult,
                height=electrode_group.height * size_mult,
                corner_radius=0.35,
                stroke_color=YELLOW,
                stroke_width=stroke_w,
                fill_color=YELLOW,
                fill_opacity=fill_op,
            )
            halo.move_to(electrode_group.get_center())
            glow.add(halo)

        self.play(FadeIn(glow), run_time=max(0.05, 0.80))

        # ------------------------------------------------------------
        # Beat 4: 6.00 - 9.06
        # Hold the glowing box; run a subtle pulse animation.
        # ------------------------------------------------------------
        pulse_scale = 1.04
        for _ in range(2):
            self.play(
                electrode_group.animate.scale(pulse_scale),
                glow.animate.scale(pulse_scale),
                run_time=max(0.05, 0.65),
            )
            self.play(
                electrode_group.animate.scale(1 / pulse_scale),
                glow.animate.scale(1 / pulse_scale),
                run_time=max(0.05, 0.65),
            )
        self.wait(max(0.05, 0.46))

        # ------------------------------------------------------------
        # Beat 5: 9.06 - 10.90
        # Shift box/glow left, widen out slightly, and add arrow.
        # ------------------------------------------------------------
        shift_vec = LEFT * 1.6
        self.play(
            self.camera.frame.animate.scale(1.25).move_to(ORIGIN),
            electrode_group.animate.shift(shift_vec),
            glow.animate.shift(shift_vec),
            run_time=max(0.05, 1.00),
        )

        arrow = Arrow(
            start=electrode_group.get_right() + RIGHT * 0.20,
            end=electrode_group.get_right() + RIGHT * 2.80,
            buff=0.0,
            color=YELLOW,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.22,
        )
        self.play(FadeIn(arrow), run_time=max(0.05, 0.84))

        # ------------------------------------------------------------
        # Beat 6: 10.90 - 13.96
        # Add the next-section label at the arrow's end.
        # ------------------------------------------------------------
        next_label = Text(
            "Next section: Electrodes and Sensors",
            font_size=26,
            color=YELLOW,
            weight="BOLD",
        )
        next_label.next_to(arrow, RIGHT, buff=0.45)

        # Keep it inside the visible frame.
        old_left = next_label.get_left()[0]
        max_right = 8.4
        if next_label.get_right()[0] > max_right:
            next_label.scale_to_fit_width(max_right - old_left)
            next_label.shift(np.array([old_left - next_label.get_left()[0], 0.0, 0.0]))

        self.play(Write(next_label), run_time=max(0.05, 1.90))
        self.wait(max(0.05, 1.16))

        # ------------------------------------------------------------
        # Beat 7: 13.96 - 16.24
        # One gentle arrow pulse.
        # ------------------------------------------------------------
        self.play(
            arrow.animate.set_color(WHITE).set_stroke(width=10, opacity=1.0),
            run_time=max(0.05, 1.14),
        )
        self.play(
            arrow.animate.set_color(YELLOW).set_stroke(width=7, opacity=1.0),
            run_time=max(0.05, 1.14),
        )

        # ------------------------------------------------------------
        # Beat 8: 16.24 - 18.92
        # Brief brightening of the label, then return to normal.
        # ------------------------------------------------------------
        self.play(
            next_label.animate.set_color(WHITE),
            run_time=max(0.05, 1.34),
        )
        self.play(
            next_label.animate.set_color(YELLOW),
            run_time=max(0.05, 1.34),
        )

        # ------------------------------------------------------------
        # Beat 9: 18.92 - 19.65
        # Final stable hold.
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.73))