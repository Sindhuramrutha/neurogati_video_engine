ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- Pipeline geometry ----------
        BOX_W = 3.2
        BOX_H = 0.85
        GAP = 0.6
        center_x = -3.0
        top_y = (3 * (BOX_H + GAP)) / 2.0
        centers = [
            np.array([center_x, top_y - i * (BOX_H + GAP), 0])
            for i in range(4)
        ]

        boxes = VGroup(*[
            RoundedRectangle(
                corner_radius=0.15,
                width=BOX_W,
                height=BOX_H,
                fill_color=BLUE,
                fill_opacity=0.10,
                stroke_color=BLUE_B,
                stroke_width=2,
            ).move_to(centers[i])
            for i in range(4)
        ])
        raw_box = boxes[0]
        prep_box = boxes[1]
        feature_box = boxes[2]
        interp_box = boxes[3]

        labels_text = [
            "Raw Signal",
            "Preprocessing",
            "Feature Extraction",
            "Interpretation or Classification",
        ]
        box_labels = VGroup()
        for box, txt in zip(boxes, labels_text):
            lab = Text(txt, font_size=20, color=WHITE, weight="BOLD")
            lab.scale_to_fit_width(BOX_W - 0.5)
            lab.move_to(box.get_center())
            box_labels.add(lab)

        arrows = VGroup(*[
            Arrow(
                boxes[i].get_bottom() + DOWN * 0.04,
                boxes[i + 1].get_top() + UP * 0.04,
                buff=0,
                color=GREY_B,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.22,
            )
            for i in range(3)
        ])

        pipeline_group = VGroup(boxes, box_labels, arrows)

        # Faint ghost outline shown first, before the real blueprint fades in.
        pipeline_ghost = VGroup(
            boxes.copy().set_fill(BLUE, opacity=0.0).set_stroke(BLUE_B, width=1.0),
            arrows.copy().set_stroke(BLUE_B, width=1.0),
        )

        # ---------- Icons ----------
        sine_curve = ParametricFunction(
            lambda t: np.array([t, 0.16 * np.sin(4 * t), 0]),
            t_range=(-1.0, 1.0),
            color=TEAL,
            stroke_width=4,
        )
        sine_icon = VGroup(sine_curve)
        sine_icon.move_to(np.array([0.8, raw_box.get_center()[1] + 0.2, 0]))

        x_vals = np.linspace(-1.0, 1.0, 100)
        noise_points = [
            np.array([x, 0.08 * np.sin(8 * x) + 0.03 * np.sin(20 * x), 0])
            for x in x_vals
        ]
        noise_jagged_points = [
            np.array([
                x,
                0.16 * np.sin(10 * x) + 0.08 * np.sin(31 * x) + 0.04 * np.sin(47 * x),
                0,
            ])
            for x in x_vals
        ]
        noise_trace = VMobject(color=ORANGE, stroke_width=3).set_points_as_corners(noise_points)
        noise_trace_jagged = VMobject(color=ORANGE, stroke_width=8).set_points_as_corners(noise_jagged_points)

        electrode = VGroup(
            Line(UP * 0.30, DOWN * 0.05, color=YELLOW, stroke_width=3),
            Circle(radius=0.06, color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            .move_to(UP * 0.35),
        )
        electrode.move_to(noise_trace.get_start() + LEFT * 0.18 + UP * 0.05)

        noise_icon_group = VGroup(noise_trace, electrode)
        noise_icon_group.move_to(np.array([0.8, 1.2, 0]))

        filter_line = Line(LEFT * 0.9, RIGHT * 0.9, color=YELLOW, stroke_width=5)
        filter_wave = ParametricFunction(
            lambda t: np.array([t, 0.15 * np.sin(5 * t), 0]),
            t_range=(-0.9, 0.9),
            color=PURPLE,
            stroke_width=4,
        )
        filter_icon = VGroup(filter_line, filter_wave)
        filter_icon.move_to(np.array([0.8, prep_box.get_center()[1], 0]))

        spect_colors = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED]
        rows, cols = 5, 6
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                val = (r + c) / (rows + cols - 2)
                color = spect_colors[int(round(val * (len(spect_colors) - 1)))]
                sq = Rectangle(
                    width=0.22,
                    height=0.22,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_color=GREY_D,
                    stroke_width=1,
                )
                cells.add(sq)
        cells.arrange_in_grid(rows=rows, cols=cols, buff=0.04)

        time_label = Text("time", font_size=15, color=WHITE).next_to(cells, DOWN, buff=0.15)
        freq_label = Text("frequency", font_size=15, color=WHITE).rotate(PI / 2).next_to(cells, LEFT, buff=0.15)
        spectrogram_icon = VGroup(cells, time_label, freq_label)
        spectrogram_icon.move_to(np.array([0.8, feature_box.get_center()[1], 0]))

        icons_group = VGroup(sine_icon, noise_icon_group, filter_icon, spectrogram_icon)

        # ---------- Recording-modality chips ----------
        def make_chip(text):
            lab = Text(text, font_size=18, color=WHITE, weight="BOLD")
            rect = RoundedRectangle(
                corner_radius=0.12,
                width=lab.width + 0.45,
                height=lab.height + 0.25,
                fill_color=BLUE,
                fill_opacity=0.18,
                stroke_color=WHITE,
                stroke_width=1.2,
            )
            return VGroup(rect, lab)

        modality_names = ["EEG", "ECoG", "EMG", "EOG", "Spikes", "LFP", "MEG"]
        chips = [make_chip(name) for name in modality_names]

        initial_positions = [
            np.array([-5.6, 3.4, 0]),
            np.array([-4.85, 3.55, 0]),
            np.array([-5.7, 2.9, 0]),
            np.array([-4.95, 2.9, 0]),
            np.array([-5.7, 2.4, 0]),
            np.array([-4.95, 2.35, 0]),
            np.array([-5.3, 1.9, 0]),
        ]
        final_positions = [
            np.array([-5.7, 3.55, 0]),
            np.array([-4.85, 3.7, 0]),
            np.array([-5.75, 3.05, 0]),
            np.array([-5.0, 3.05, 0]),
            np.array([-5.7, 2.5, 0]),
            np.array([-5.0, 2.45, 0]),
            np.array([-5.35, 1.95, 0]),
        ]

        for chip, pos in zip(chips, initial_positions):
            chip.move_to(pos)

        labels_group = VGroup(*chips)

        # ---------- Beat 1: faint ghost outline ----------
        self.play(FadeIn(pipeline_ghost), run_time=max(0.05, 0.44))

        # ---------- Beat 2: unlit blueprint pipeline ----------
        self.play(
            FadeOut(pipeline_ghost),
            FadeIn(pipeline_group),
            run_time=max(0.05, 2.04),
        )

        # ---------- Beat 3: slow top-to-bottom stage sweep ----------
        for box in boxes:
            self.play(
                box.animate.set_stroke(YELLOW, width=4).set_fill(BLUE_D, opacity=0.45),
                run_time=max(0.05, 0.345),
            )

        # Gap 3.86-4.66: settle back to unlit blueprint.
        self.play(
            *[
                box.animate.set_stroke(BLUE_B, width=2).set_fill(BLUE, opacity=0.10)
                for box in boxes
            ],
            run_time=max(0.05, 0.80),
        )

        # ---------- Beat 4: sine wave and noisy electrode trace ----------
        self.play(
            FadeIn(sine_icon, scale=0.8),
            raw_box.animate.set_stroke(YELLOW, width=5).set_fill(BLUE_D, opacity=0.50),
            run_time=max(0.05, 0.80),
        )
        self.play(sine_icon.animate.scale(1.15), run_time=max(0.05, 0.50))
        self.play(sine_icon.animate.scale(1 / 1.15), run_time=max(0.05, 0.40))
        self.play(GrowFromCenter(noise_icon_group), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.30))

        # Gap 7.16-7.72.
        self.wait(max(0.05, 0.56))

        # ---------- Beat 5: noise trace thickens/jags, raw dims slightly ----------
        self.play(
            Transform(noise_trace, noise_trace_jagged),
            noise_icon_group.animate.rotate(angle=0.08).shift(UP * 0.05),
            raw_box.animate.set_stroke(YELLOW, width=4).set_fill(BLUE_D, opacity=0.30),
            run_time=max(0.05, 1.72),
        )

        # Gap 9.44-10.08.
        self.wait(max(0.05, 0.64))

        # ---------- Beat 6: filter icon beside Preprocessing ----------
        self.play(
            GrowFromCenter(filter_icon),
            prep_box.animate.set_stroke(YELLOW, width=5).set_fill(BLUE_D, opacity=0.50),
            run_time=max(0.05, 1.90),
        )

        # Gap 11.98-12.36.
        self.wait(max(0.05, 0.38))

        # ---------- Beat 7: spectrogram icon beside Feature Extraction ----------
        self.play(
            GrowFromCenter(spectrogram_icon),
            feature_box.animate.set_stroke(YELLOW, width=5).set_fill(BLUE_D, opacity=0.50),
            run_time=max(0.05, 1.40),
        )
        self.play(spectrogram_icon.animate.scale(1.08), run_time=max(0.05, 1.00))
        self.play(spectrogram_icon.animate.scale(1 / 1.08), run_time=max(0.05, 1.60))

        # Gap 16.36-16.96.
        self.wait(max(0.05, 0.60))

        # ---------- Beat 8: icons recede ----------
        self.play(
            icons_group.animate.scale(0.85).set_opacity(0.55),
            run_time=max(0.05, 2.66),
        )

        # ---------- Beat 9: modality labels pop in one by one ----------
        cue_times = [0.00, 1.74, 2.18, 3.10, 3.80, 4.60, 5.42]
        elapsed = 0.0
        for i, chip in enumerate(chips):
            wait_dur = cue_times[i] - elapsed
            if wait_dur > 1e-6:
                self.wait(max(0.05, wait_dur))

            if i < 6:
                self.play(GrowFromCenter(chip), run_time=max(0.05, 0.25))
                self.play(Indicate(chip, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.15))
                elapsed = cue_times[i] + 0.40
            else:
                anim_dur = 5.56 - cue_times[i]
                self.play(GrowFromCenter(chip), run_time=max(0.05, anim_dur))
                elapsed = cue_times[i] + anim_dur

        # Gap 25.18-25.88.
        self.wait(max(0.05, 0.70))

        # ---------- Beat 10: labels rearrange into loose arc, raw box brightens ----------
        self.play(
            *[
                chips[i].animate.move_to(final_positions[i])
                for i in range(len(chips))
            ],
            run_time=max(0.05, 1.00),
        )
        self.play(
            *[chip.animate.scale(1.12) for chip in chips],
            raw_box.animate.set_stroke(YELLOW, width=5).set_fill(BLUE_D, opacity=0.50),
            run_time=max(0.05, 0.28),
        )
        self.play(
            *[chip.animate.scale(1 / 1.12) for chip in chips],
            run_time=max(0.05, 0.38),
        )

        # Gap 27.54-28.42.
        self.wait(max(0.05, 0.88))

        # ---------- Beat 11: pipeline becomes brightest, icons/labels move outward ----------
        self.play(
            icons_group.animate.shift(RIGHT * 0.35).set_opacity(0.35),
            labels_group.animate.shift(LEFT * 0.12).set_opacity(0.35),
            boxes.animate.set_stroke(YELLOW, width=5).set_fill(BLUE, opacity=0.30),
            arrows.animate.set_stroke(YELLOW, width=6),
            run_time=max(0.05, 4.38),
        )

        # ---------- Beat 12: pipeline shifts center-left, traveling highlight ----------
        self.play(
            pipeline_group.animate.shift(RIGHT * 0.8),
            run_time=max(0.05, 1.00),
        )

        traveller = VGroup(
            Circle(radius=0.18, color=YELLOW, fill_opacity=0.25, stroke_width=0).move_to(boxes[0].get_center()),
            Dot(radius=0.07, color=YELLOW, stroke_width=0).move_to(boxes[0].get_center()),
        ).set_z_index(10)

        step_dur = (7.26 - 1.00) / 4.0
        for i, box in enumerate(boxes):
            if i == 0:
                self.play(
                    GrowFromCenter(traveller),
                    box.animate.set_stroke(YELLOW, width=6).set_fill(BLUE_D, opacity=0.60),
                    run_time=max(0.05, step_dur),
                )
            else:
                self.play(
                    traveller.animate.move_to(box.get_center()),
                    box.animate.set_stroke(YELLOW, width=6).set_fill(BLUE_D, opacity=0.60),
                    arrows[i - 1].animate.set_stroke(YELLOW, width=7),
                    run_time=max(0.05, step_dur),
                )

        # Gap 40.06-40.92: clear traveling highlight, reset boxes to medium.
        self.play(
            FadeOut(traveller),
            *[box.animate.set_stroke(BLUE_B, width=3).set_fill(BLUE, opacity=0.15) for box in boxes],
            *[arrow.animate.set_stroke(BLUE_B, width=3) for arrow in arrows],
            run_time=max(0.05, 0.86),
        )

        # ---------- Beat 13: one-at-a-time synchronized stage lighting ----------
        schedule = [(1.56, 0), (2.80, 1), (4.02, 2), (5.56, 3)]
        current = 0.0
        for rel_cue, idx in schedule:
            wait_dur = rel_cue - current
            if wait_dur > 1e-6:
                self.wait(max(0.05, wait_dur))

            anim_dur = 0.30 if idx == 3 else 0.25
            anims = [
                boxes[idx].animate.set_stroke(YELLOW, width=6).set_fill(BLUE_D, opacity=0.55)
            ]
            for i, box in enumerate(boxes):
                if i != idx:
                    anims.append(
                        box.animate.set_stroke(BLUE_B, width=3).set_fill(BLUE, opacity=0.15)
                    )

            for j, arrow in enumerate(arrows):
                if j == idx - 1:
                    anims.append(arrow.animate.set_stroke(YELLOW, width=6))
                else:
                    anims.append(arrow.animate.set_stroke(BLUE_B, width=3))

            self.play(*anims, run_time=max(0.05, anim_dur))
            current = rel_cue + anim_dur

        if 6.92 - current > 1e-6:
            self.wait(max(0.05, 6.92 - current))

        # Gap 47.84-49.18.
        self.wait(max(0.05, 1.34))

        # ---------- Beat 14: pipeline shifts right, icons/labels fade back quietly ----------
        self.play(
            pipeline_group.animate.shift(RIGHT * 1.0),
            icons_group.animate.shift(RIGHT * 1.0).set_opacity(0.80),
            labels_group.animate.shift(RIGHT * 1.0).scale(0.9).set_opacity(0.85),
            run_time=max(0.05, 5.82),
        )

        # ---------- Beat 15: whole workflow pulses softly ----------
        whole_workflow = VGroup(pipeline_group, icons_group, labels_group)
        self.play(whole_workflow.animate.scale(1.03), run_time=max(0.05, 0.30))
        self.play(whole_workflow.animate.scale(1 / 1.03), run_time=max(0.05, 0.30))
        self.play(whole_workflow.animate.scale(1.02), run_time=max(0.05, 0.30))
        self.play(whole_workflow.animate.scale(1 / 1.02), run_time=max(0.05, 0.37))