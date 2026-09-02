ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene21(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helper: small EEG-style curve as a VMobject
        # ------------------------------------------------------------
        def make_curve(x_start, x_end, func, color=YELLOW, stroke_width=3):
            x = np.linspace(x_start, x_end, 800)
            y = func(x)
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        # ------------------------------------------------------------
        # Previous-scene placeholder composition (fades out at start)
        # ------------------------------------------------------------
        prev_comp = VGroup(
            *[
                Rectangle(
                    width=2.0, height=1.2,
                    fill_color=GREY_B, fill_opacity=0.3,
                    stroke_color=GREY_B, stroke_width=1.5,
                )
                for _ in range(3)
            ]
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.5)

        # ------------------------------------------------------------
        # Heading
        # ------------------------------------------------------------
        heading = Text("Clinical Applications of EEG", font_size=46, weight="BOLD", color=WHITE)
        heading.scale_to_fit_width(12)
        heading.to_edge(UP, buff=0.35)

        # ------------------------------------------------------------
        # Four clinical application panels (2x2 grid)
        # ------------------------------------------------------------
        panel_titles = [
            "Diagnosis",
            "Seizure Classification",
            "Monitoring Treatment",
            "Presurgical Evaluation",
        ]
        panel_bgs = []
        panel_groups = []
        for title in panel_titles:
            bg = Rectangle(
                width=5.3, height=2.3,
                fill_color=BLACK, fill_opacity=0.75,
                stroke_color=GREY_B, stroke_width=1.5,
            )
            label = Text(title, font_size=22, weight="BOLD", color=WHITE)
            label.move_to(bg.get_center() + UP * 0.8)
            group = VGroup(bg, label)
            group.set_opacity(0.4)
            panel_bgs.append(bg)
            panel_groups.append(group)

        panel_grid = VGroup(*panel_groups).arrange_in_grid(rows=2, cols=2, buff=0.45)
        panel_grid.move_to(DOWN * 0.2)
        panel_centers = [g.get_center() for g in panel_groups]

        # Scale/opacity state for panel-focus transitions
        panel_scales = [1.0, 1.0, 1.0, 1.0]
        panel_opacities = [0.4, 0.4, 0.4, 0.4]

        def build_focus_anims(active_idx):
            anims = []
            for i in range(4):
                if i == active_idx:
                    target_scale = 1.08
                    target_opacity = 1.0
                    stroke_col = YELLOW
                    stroke_w = 3
                else:
                    target_scale = 0.93
                    target_opacity = 0.3
                    stroke_col = GREY_B
                    stroke_w = 1.5
                ratio = target_scale / panel_scales[i]
                anims.append(panel_groups[i].animate.scale(ratio).set_opacity(target_opacity))
                anims.append(panel_bgs[i].animate.set_stroke(color=stroke_col, width=stroke_w))
                panel_scales[i] = target_scale
                panel_opacities[i] = target_opacity
            return anims

        # ------------------------------------------------------------
        # Panel 1 content: Diagnosis
        # ------------------------------------------------------------
        diag_wave = make_curve(
            -2.1, 2.1,
            lambda x: 0.07 * np.sin(2 * np.pi * 1.2 * x) + 0.55 * np.exp(-(x / 0.08) ** 2),
            color=YELLOW, stroke_width=3,
        )
        diag_wave.move_to(UP * 0.25)

        diag_highlight = Rectangle(
            width=0.85, height=0.75, stroke_color=YELLOW, stroke_width=2, fill_opacity=0
        ).move_to([0, 0.48, 0])

        diag_check_circle = Circle(radius=0.16, fill_color=GREEN, fill_opacity=1, stroke_width=0)
        diag_check_text = Text("✓", font_size=14, color=BLACK).move_to(diag_check_circle.get_center())
        diag_check = VGroup(diag_check_circle, diag_check_text).move_to([1.6, 0.48, 0])

        diag_label = Text("Supports Diagnosis", font_size=16, color=WHITE)
        diag_label.scale_to_fit_width(2.4)
        diag_label.next_to(diag_check, DOWN, buff=0.1)

        diag_arrow = Arrow(
            [0.42, 0.48, 0],
            [1.42, 0.48, 0],
            color=GREEN, stroke_width=2.5, buff=0.05,
            max_tip_length_to_length_ratio=0.2,
        )

        diag_content = VGroup(diag_wave, diag_highlight, diag_check, diag_label, diag_arrow)
        diag_content.move_to(panel_centers[0])

        # ------------------------------------------------------------
        # Panel 2 content: Seizure Classification
        # ------------------------------------------------------------
        def gen_seizure_func(x):
            return 0.2 * np.sin(2 * np.pi * 2.5 * x) + 0.35 * np.exp(-((x + 0.5) / 0.13) ** 2) + 0.35 * np.exp(-(x / 0.13) ** 2) + 0.35 * np.exp(-((x - 0.5) / 0.13) ** 2)

        def focal_seizure_func(x):
            return 0.08 * np.sin(2 * np.pi * 1.1 * x) + 0.42 * np.exp(-((x + 0.25) / 0.08) ** 2) + 0.3 * np.exp(-((x - 0.8) / 0.18) ** 2)

        def absence_seizure_func(x):
            return 0.12 * np.sin(2 * np.pi * 2.1 * x) + 0.18 * np.sin(2 * np.pi * 1.0 * x + 1.5)

        seizure_wave_specs = [
            ("Generalized", gen_seizure_func),
            ("Focal", focal_seizure_func),
            ("Absence", absence_seizure_func),
        ]
        seizure_patterns = []
        for name, func in seizure_wave_specs:
            wave = make_curve(-0.7, 0.7, func, color=YELLOW, stroke_width=2.5)
            wave.scale_to_fit_width(1.1)
            label = Text(name, font_size=14, color=WHITE)
            label.scale_to_fit_width(1.2)
            pattern = VGroup(wave, label).arrange(DOWN, buff=0.08)
            seizure_patterns.append(pattern)

        seizure_pattern_row = VGroup(*seizure_patterns).arrange(RIGHT, buff=0.5)
        seizure_pattern_row.move_to(UP * 0.55)

        treatment_box = RoundedRectangle(
            width=2.4, height=0.55, corner_radius=0.12,
            fill_color=ORANGE, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        )
        treatment_text = Text("Treatment Decision", font_size=15, color=BLACK)
        treatment_text.move_to(treatment_box.get_center())
        treatment_decision = VGroup(treatment_box, treatment_text).move_to(DOWN * 0.72)

        classification_arrows = []
        for pat in seizure_patterns:
            start = pat.get_bottom() + DOWN * 0.05
            end = treatment_decision.get_top() + UP * 0.05
            arrow = Arrow(
                start, end,
                color=YELLOW, stroke_width=2, buff=0.03,
                max_tip_length_to_length_ratio=0.25,
            )
            classification_arrows.append(arrow)

        class_content = VGroup(seizure_pattern_row, treatment_decision, *classification_arrows)
        class_content.move_to(panel_centers[1])

        # ------------------------------------------------------------
        # Panel 3 content: Monitoring Treatment
        # ------------------------------------------------------------
        monitor_funcs = [
            lambda x: 0.4 * np.sin(2 * np.pi * 5 * x) + 0.4 * np.sin(2 * np.pi * 11 * x),
            lambda x: 0.35 * np.sin(2 * np.pi * 4 * x) + 0.3 * np.sin(2 * np.pi * 9 * x),
            lambda x: 0.25 * np.sin(2 * np.pi * 3 * x) + 0.2 * np.sin(2 * np.pi * 7 * x),
            lambda x: 0.2 * np.sin(2 * np.pi * 2.5 * x) + 0.15 * np.sin(2 * np.pi * 5 * x),
            lambda x: 0.12 * np.sin(2 * np.pi * 1.8 * x) + 0.05 * np.sin(2 * np.pi * 3 * x),
        ]
        monitor_xs = np.linspace(-2.0, 2.0, 5)
        monitor_snaps = []
        for i, x_pos in enumerate(monitor_xs):
            box = Rectangle(
                width=0.85, height=0.7,
                fill_color=BLACK, fill_opacity=0.5,
                stroke_color=GREY_B, stroke_width=1,
            )
            wave_color = GREEN if i == 4 else YELLOW
            wave = make_curve(-0.3, 0.3, monitor_funcs[i], color=wave_color, stroke_width=2)
            wave.move_to(box.get_center())
            snap = VGroup(box, wave).move_to([x_pos, 0, 0])
            monitor_snaps.append(snap)

        monitor_snap_row = VGroup(*monitor_snaps).move_to(ORIGIN)

        timeline_arrow = Arrow(
            LEFT * 2.5, RIGHT * 2.5,
            color=GREY_B, stroke_width=2, buff=0.05,
            max_tip_length_to_length_ratio=0.1,
        ).move_to(DOWN * 0.75)
        timeline_label = Text("Time", font_size=14, color=GREY_B).next_to(timeline_arrow, DOWN, buff=0.08)

        pill_body = RoundedRectangle(
            width=0.5, height=0.65, corner_radius=0.08,
            fill_color=WHITE, fill_opacity=0.95,
            stroke_color=WHITE, stroke_width=1,
        )
        pill_cap = Rectangle(width=0.62, height=0.2, fill_color=ORANGE, fill_opacity=1, stroke_width=0)
        pill_bottle = VGroup(pill_cap, pill_body).arrange(DOWN, buff=0)
        med_label = Text("Anti-Seizure Medication", font_size=13, color=WHITE)
        med_label.scale_to_fit_width(2.2)
        med_group = VGroup(pill_bottle, med_label).arrange(DOWN, buff=0.05)
        med_group.move_to(UP * 0.98)

        med_arrow = Arrow(
            med_group.get_bottom() + DOWN * 0.05,
            monitor_snap_row[4].get_top() + UP * 0.05,
            color=GREEN, stroke_width=2.5, buff=0.03,
            max_tip_length_to_length_ratio=0.2,
        )

        monitor_content = VGroup(
            timeline_arrow, timeline_label,
            monitor_snap_row, med_group, med_arrow,
        )
        monitor_content.move_to(panel_centers[2])

        # ------------------------------------------------------------
        # Panel 4 content: Presurgical Evaluation
        # ------------------------------------------------------------
        head = Ellipse(
            width=1.2, height=1.9,
            fill_color=BLACK, fill_opacity=0.7,
            stroke_color=WHITE, stroke_width=3,
        ).move_to(LEFT * 1.4)

        brain_asset = SVGMobject(ASSET_PATHS["brain"])
        brain_asset.scale_to_fit_height(1.05)
        brain_asset.set_color(PINK)
        brain_asset.set_fill(PINK, opacity=0.85)
        brain_asset.set_stroke(PINK, width=1, opacity=0.8)
        brain_asset.move_to(head.get_center())

        focus_dot = Dot(radius=0.13, color=YELLOW).move_to(brain_asset.get_center() + RIGHT * 0.25 + UP * 0.35)
        focus_label = Text("Seizure Focus", font_size=15, color=YELLOW).next_to(head, RIGHT, buff=0.4).shift(UP * 0.6)

        presurg_content = VGroup(head, brain_asset, focus_dot, focus_label)

        mri_rect = Rectangle(
            width=1.35, height=2.0,
            fill_color=TEAL, fill_opacity=0.15,
            stroke_color=TEAL, stroke_width=1.2,
        ).move_to(head.get_center())
        mri_h_line = Line(
            mri_rect.get_left() + DOWN * 0.5,
            mri_rect.get_right() + DOWN * 0.5,
            color=TEAL, stroke_opacity=0.45, stroke_width=1,
        )
        mri_v_line = Line(
            mri_rect.get_top() + LEFT * 0.2,
            mri_rect.get_bottom() + LEFT * 0.2,
            color=TEAL, stroke_opacity=0.45, stroke_width=1,
        )
        mri_focus_cross = Circle(radius=0.18, color=YELLOW, stroke_width=2, fill_opacity=0)
        mri_focus_cross.move_to(focus_dot.get_center())
        mri_overlay = VGroup(mri_rect, mri_h_line, mri_v_line, mri_focus_cross)

        combined_label = Text("Combined with Other Imaging", font_size=14, color=TEAL)
        combined_label.scale_to_fit_width(2.3)
        combined_label.next_to(head, RIGHT, buff=0.4).shift(DOWN * 0.65)

        # ------------------------------------------------------------
        # Advantages checklist panel
        # ------------------------------------------------------------
        adv_bg = RoundedRectangle(
            width=9.8, height=4.4, corner_radius=0.12,
            fill_color=BLACK, fill_opacity=0.7,
            stroke_color=BLUE, stroke_width=2,
        ).move_to(DOWN * 0.4)

        adv_title = Text("Advantages of EEG", font_size=26, weight="BOLD", color=YELLOW)
        adv_title.move_to(adv_bg.get_top() + DOWN * 0.45)

        row_texts_spec = [
            "Direct Measurement of Brain Electrical Activity",
            "Excellent Temporal Resolution",
            "Non-invasive and Widely Available",
            "Useful for Long-term Monitoring",
            "Supports Visual Interpretation and Automated Analysis",
        ]
        row_boxes = []
        row_lines = []
        row_texts = []
        check_marks = []

        p = adv_bg.get_center()
        y_shifts = [0.8, 0.1, -0.6, -1.3, -2.0]
        for spec, y_shift in zip(row_texts_spec, y_shifts):
            y = p[1] + y_shift
            box = Square(
                side_length=0.32,
                stroke_color=GREY_B, stroke_width=2,
                fill_color=BLACK, fill_opacity=0.5,
            ).move_to([-3.5, y, 0])
            line = Line([-3.1, y, 0], [3.8, y, 0], color=GREY_B, stroke_width=2)
            text = Text(spec, font_size=20, color=WHITE)
            text.scale_to_fit_width(7.0)
            start_x = box.get_right()[0] + 0.35
            text.move_to([start_x + text.get_width() / 2, y, 0])
            check = Text("✓", font_size=22, color=GREEN).move_to(box.get_center())
            check.set_opacity(0)
            text.set_opacity(0)
            row_boxes.append(box)
            row_lines.append(line)
            row_texts.append(text)
            check_marks.append(check)

        adv_panel = VGroup(
            adv_bg, adv_title,
            *row_boxes, *row_lines, *row_texts, *check_marks,
        )

        # ------------------------------------------------------------
        # Caution note
        # ------------------------------------------------------------
        caution_bg = RoundedRectangle(
            width=6.2, height=2.4, corner_radius=0.15,
            fill_color=BLACK, fill_opacity=0.7,
            stroke_color=YELLOW, stroke_width=3,
        )
        caution_title = Text("Caution", font_size=26, weight="BOLD", color=YELLOW)
        caution_title.move_to(caution_bg.get_top() + DOWN * 0.45)

        caution_sentence = Text("A normal EEG does not necessarily rule out epilepsy.", font_size=20, color=WHITE)
        caution_sentence.scale_to_fit_width(5.4)
        caution_sentence.next_to(caution_title, DOWN, buff=0.25)

        caution_note = VGroup(caution_bg, caution_title, caution_sentence)
        caution_note.move_to(ORIGIN)

        # ------------------------------------------------------------
        # Patient + normal-EEG-between-seizures timeline
        # ------------------------------------------------------------
        def build_patient_timeline():
            timeline_line = Line(LEFT * 2.2, RIGHT * 2.2, color=GREY_B, stroke_width=3)
            marker_left = Line(UP * 0.25, DOWN * 0.25, color=RED, stroke_width=3).move_to(LEFT * 1.6)
            marker_right = Line(UP * 0.25, DOWN * 0.25, color=RED, stroke_width=3).move_to(RIGHT * 1.6)
            highlight = Rectangle(
                width=3.0, height=0.55,
                fill_color=GREEN, fill_opacity=0.18,
                stroke_color=GREEN, stroke_width=1.5,
            ).move_to(ORIGIN)
            flat_wave = make_curve(
                -1.4, 1.4,
                lambda x: 0.07 * np.sin(2 * np.pi * 1.0 * x),
                color=GREEN, stroke_width=2,
            ).move_to(ORIGIN)

            seizure_left_label = Text("Seizure", font_size=16, color=RED)
            seizure_left_label.move_to([marker_left.get_center()[0], timeline_line.get_center()[1] - 0.4, 0])
            normal_eeg_label = Text("Normal EEG", font_size=16, color=GREEN).move_to([0, timeline_line.get_center()[1] - 0.4, 0])
            seizure_right_label = Text("Seizure", font_size=16, color=RED)
            seizure_right_label.move_to([marker_right.get_center()[0], timeline_line.get_center()[1] - 0.4, 0])

            timeline = VGroup(
                timeline_line, marker_left, marker_right,
                highlight, flat_wave,
                seizure_left_label, normal_eeg_label, seizure_right_label,
            )

            human_head = Circle(radius=0.16, color=BLUE, fill_color=BLUE, fill_opacity=1, stroke_width=0)
            human_body = RoundedRectangle(
                width=0.7, height=0.9, corner_radius=0.2,
                fill_color=BLUE, fill_opacity=1, stroke_width=0,
            )
            human_body.next_to(human_head, DOWN, buff=0.05)
            arms = VGroup(
                Line(
                    human_body.get_left() + UP * 0.1,
                    human_body.get_left() + LEFT * 0.35 + DOWN * 0.2,
                    color=BLUE, stroke_width=4,
                ),
                Line(
                    human_body.get_right() + UP * 0.1,
                    human_body.get_right() + RIGHT * 0.35 + DOWN * 0.2,
                    color=BLUE, stroke_width=4,
                ),
            )
            legs = VGroup(
                Line(
                    human_body.get_bottom() + LEFT * 0.15,
                    human_body.get_bottom() + LEFT * 0.2 + DOWN * 0.4,
                    color=BLUE, stroke_width=4,
                ),
                Line(
                    human_body.get_bottom() + RIGHT * 0.15,
                    human_body.get_bottom() + RIGHT * 0.2 + DOWN * 0.4,
                    color=BLUE, stroke_width=4,
                ),
            )
            human = VGroup(human_head, human_body, arms, legs)
            patient = VGroup(human, timeline).arrange(DOWN, buff=0.25)
            return patient

        patient_timeline = build_patient_timeline()
        patient_timeline.move_to(RIGHT * 4.3 + UP * 0.1)

        # ------------------------------------------------------------
        # Three interpretation input blocks
        # ------------------------------------------------------------
        input_labels = [
            "Clinical History",
            "Observed Symptoms",
            "Additional Diagnostic Investigations",
        ]

        def build_input_blocks():
            clipboard_icon = SVGMobject(ASSET_PATHS["clipboard_pulse"])
            clipboard_icon.scale_to_fit_height(0.55)
            clipboard_icon.set_color(WHITE)

            eye_icon = VGroup(
                Ellipse(width=0.7, height=0.4, fill_color=WHITE, fill_opacity=1, stroke_color=WHITE, stroke_width=1),
                Circle(radius=0.12, fill_color=BLUE, fill_opacity=1, stroke_width=0),
            )
            eye_icon[1].move_to(eye_icon[0].get_center())

            lens = Circle(radius=0.22, color=WHITE, fill_color=WHITE, fill_opacity=0.0, stroke_color=WHITE, stroke_width=3)
            handle = Line(
                lens.get_right() + DOWN * 0.05,
                lens.get_right() + RIGHT * 0.35 + DOWN * 0.35,
                color=WHITE, stroke_width=3,
            )
            magnifier_icon = VGroup(lens, handle)

            icons = [clipboard_icon, eye_icon, magnifier_icon]
            blocks = []
            for label, icon in zip(input_labels, icons):
                bg = RoundedRectangle(
                    width=2.7, height=1.9, corner_radius=0.12,
                    fill_color=BLACK, fill_opacity=0.65,
                    stroke_color=BLUE, stroke_width=1.5,
                )
                icon_place = icon.copy().scale_to_fit_height(0.55)
                icon_place.move_to(bg.get_center() + UP * 0.4)
                text = Text(label, font_size=13, color=WHITE)
                text.scale_to_fit_width(2.2)
                text.next_to(icon_place, DOWN, buff=0.15)
                block = VGroup(bg, icon_place, text)
                blocks.append(block)
            row = VGroup(*blocks).arrange(RIGHT, buff=0.35)
            row.move_to(DOWN * 2.1)
            return row, blocks

        input_blocks_row, input_blocks = build_input_blocks()

        # ------------------------------------------------------------
        # Beat 1: 0.00 - 3.42
        # ------------------------------------------------------------
        self.play(
            FadeOut(prev_comp),
            FadeIn(heading),
            FadeIn(panel_grid),
            run_time=max(0.05, 3.42),
        )
        self.wait(max(0.05, 0.88))

        # ------------------------------------------------------------
        # Beat 2: 4.30 - 10.78
        # ------------------------------------------------------------
        self.play(*build_focus_anims(0), run_time=max(0.05, 2.0))
        self.play(FadeIn(diag_content), run_time=max(0.05, 2.5))
        self.wait(max(0.05, 1.98))

        # ------------------------------------------------------------
        # Beat 3: 11.92 - 19.56
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.14))
        self.play(
            FadeOut(diag_content),
            *build_focus_anims(1),
            run_time=max(0.05, 3.0),
        )
        self.play(FadeIn(class_content), run_time=max(0.05, 2.5))
        self.wait(max(0.05, 2.14))

        # ------------------------------------------------------------
        # Beat 4: 20.66 - 29.00
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.10))
        self.play(
            FadeOut(class_content),
            *build_focus_anims(2),
            run_time=max(0.05, 3.0),
        )
        self.play(FadeIn(monitor_content), run_time=max(0.05, 2.5))
        self.wait(max(0.05, 2.84))

        # ------------------------------------------------------------
        # Beat 5: 30.00 - 45.58
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.00))
        self.play(
            FadeOut(monitor_content),
            *build_focus_anims(3),
            run_time=max(0.05, 3.0),
        )
        self.play(FadeIn(presurg_content), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 1.5))

        self.play(focus_dot.animate.scale(1.8), run_time=max(0.05, 0.6))
        self.play(focus_dot.animate.scale(1 / 1.8), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.8))
        self.play(FadeIn(mri_overlay), FadeIn(combined_label), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 5.08))

        # ------------------------------------------------------------
        # Beat 6: 46.58 - 50.32
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.00))
        self.play(
            *[g.animate.scale(0.7).set_opacity(0) for g in panel_groups],
            FadeOut(presurg_content),
            FadeOut(mri_overlay),
            FadeOut(combined_label),
            FadeIn(adv_panel),
            run_time=max(0.05, 3.74),
        )

        # ------------------------------------------------------------
        # Beat 7: 51.34 - 53.56
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.02))
        self.play(
            FadeIn(check_marks[0]),
            FadeIn(row_texts[0]),
            row_boxes[0].animate.set_stroke(color=GREEN, width=2),
            run_time=max(0.05, 1.6),
        )
        self.wait(max(0.05, 0.62))

        # ------------------------------------------------------------
        # Beat 8: 54.32 - 55.44
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.76))
        self.play(
            FadeIn(check_marks[1]),
            FadeIn(row_texts[1]),
            row_boxes[1].animate.set_stroke(color=GREEN, width=2),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.12))

        # ------------------------------------------------------------
        # Beat 9: 55.44 - 57.88
        # ------------------------------------------------------------
        self.play(
            FadeIn(check_marks[2]),
            FadeIn(row_texts[2]),
            row_boxes[2].animate.set_stroke(color=GREEN, width=2),
            run_time=max(0.05, 1.8),
        )
        self.wait(max(0.05, 0.64))

        # ------------------------------------------------------------
        # Beat 10: 58.30 - 59.92
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.42))
        self.play(
            FadeIn(check_marks[3]),
            FadeIn(row_texts[3]),
            row_boxes[3].animate.set_stroke(color=GREEN, width=2),
            run_time=max(0.05, 1.3),
        )
        self.wait(max(0.05, 0.32))

        # ------------------------------------------------------------
        # Beat 11: 60.48 - 64.10
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.56))
        self.play(
            FadeIn(check_marks[4]),
            FadeIn(row_texts[4]),
            row_boxes[4].animate.set_stroke(color=GREEN, width=2),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 2.12))

        # ------------------------------------------------------------
        # Beat 12: 65.06 - 68.22
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.96))
        self.play(
            adv_panel.animate.scale(0.85).set_opacity(0.35),
            FadeIn(caution_note),
            run_time=max(0.05, 1.96),
        )
        self.play(caution_note.animate.scale(1.03), run_time=max(0.05, 0.6))
        self.play(caution_note.animate.scale(1 / 1.03), run_time=max(0.05, 0.6))

        # ------------------------------------------------------------
        # Beat 13: 69.14 - 73.64
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.92))
        self.play(
            caution_note.animate.move_to(LEFT * 1.7 + UP * 0.1),
            FadeIn(patient_timeline),
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 2.0))

        # ------------------------------------------------------------
        # Beat 14: 74.72 - 85.88
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.08))
        self.play(
            caution_note.animate.move_to(LEFT * 1.5 + UP * 0.4).scale(0.96).set_opacity(0.75),
            patient_timeline.animate.move_to(RIGHT * 4.3 + UP * 0.2).scale(0.9).set_opacity(0.45),
            FadeIn(input_blocks_row),
            run_time=max(0.05, 3.0),
        )

        # Arrows from each input block pointing up to caution note
        input_arrows = VGroup()
        for i, block in enumerate(input_blocks):
            start = block.get_top() + UP * 0.05
            end_x = caution_bg.get_bottom()[0] + (i - 1) * 0.8
            end = np.array([end_x, caution_bg.get_bottom()[1] - 0.05, 0])
            arrow = Arrow(
                start, end,
                color=YELLOW, stroke_width=2.5, buff=0.03,
                max_tip_length_to_length_ratio=0.2,
            )
            input_arrows.add(arrow)

        self.play(*[Create(a) for a in input_arrows], run_time=max(0.05, 2.0))

        self.play(
            caution_bg.animate.set_stroke(color=YELLOW, width=4),
            caution_note.animate.set_opacity(1),
            run_time=max(0.05, 1.0),
        )

        self.wait(max(0.05, 5.16))
        self.wait(max(0.05, 0.77))