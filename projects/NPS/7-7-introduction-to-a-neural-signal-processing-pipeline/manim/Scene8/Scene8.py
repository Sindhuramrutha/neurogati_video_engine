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


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Beat 1: blank screen 0.00-0.56
        self.wait(max(0.05, 0.56))

        # Beat 2: title 0.56-2.60
        title = Text(
            "Neural Signal Processing: A Complete Workflow",
            font_size=32,
            color=WHITE,
            weight="BOLD",
            stroke_color=BLACK,
            stroke_width=3,
        )
        title.scale_to_fit_width(12)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.84))

        # Beat 3: central pipeline 2.60-4.60
        labels = [
            "Raw Signal",
            "Preprocessing",
            "Feature Extraction",
            "Interpretation / Classification",
        ]
        widths = [1.9, 2.0, 2.0, 2.4]
        font_sizes = [16, 16, 15, 13]
        accents = [BLUE, TEAL, GREEN, ORANGE]

        box_groups = []
        box_rects = []
        box_labels = []
        glows = []

        for i, (label, accent, w, fs) in enumerate(zip(labels, accents, widths, font_sizes)):
            rect = RoundedRectangle(
                width=w,
                height=0.95,
                corner_radius=0.16,
                fill_color=GREY,
                fill_opacity=0.18,
                stroke_color=WHITE,
                stroke_width=2,
            )
            label_text = Text(label, font_size=fs, color=WHITE, weight="BOLD")
            label_text.scale_to_fit_width(rect.width - 0.35)
            label_text.move_to(rect.get_center())

            group = VGroup(rect, label_text)
            box_groups.append(group)
            box_rects.append(rect)
            box_labels.append(label_text)

            glow = RoundedRectangle(
                width=rect.width + 0.25,
                height=rect.height + 0.25,
                corner_radius=0.20,
                stroke_color=accent,
                stroke_width=8,
                fill_color=accent,
                fill_opacity=0.0,
            )
            glow.move_to(rect.get_center())
            glow.set_stroke(opacity=0.0)
            glow.set_fill(opacity=0.0)
            glows.append(glow)

        pipeline_group = VGroup(*box_groups)
        pipeline_group.arrange(RIGHT, buff=0.45)
        pipeline_group.move_to(np.array([0.5, 1.35, 0]))

        pipeline_arrows = []
        for i in range(3):
            arrow = Arrow(
                start=box_groups[i].get_right(),
                end=box_groups[i + 1].get_left(),
                buff=0.08,
                color=GREY_B,
                stroke_width=3.5,
                max_tip_length_to_length_ratio=0.22,
            )
            pipeline_arrows.append(arrow)

        self.add(*glows)
        self.play(FadeIn(pipeline_group, *pipeline_arrows), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.8))

        # Beat 4: unity pulse + first caption 4.60-8.00
        caption1 = Text(
            "not a collection of isolated techniques",
            font_size=24,
            color=WHITE,
            weight="SEMIBOLD",
        )
        caption1.scale_to_fit_width(5.8)
        caption1.next_to(pipeline_group, DOWN, buff=0.25)
        caption1.set_opacity(0)
        self.add(caption1)

        def pulse_bright_anims():
            return [
                *[box_rects[i].animate.set_stroke(WHITE, width=5).set_fill(WHITE, opacity=0.30) for i in range(4)],
                *[arrow.animate.set_stroke(WHITE, width=4) for arrow in pipeline_arrows],
            ]

        def pulse_normal_anims():
            return [
                *[box_rects[i].animate.set_stroke(WHITE, width=2).set_fill(GREY, opacity=0.18) for i in range(4)],
                *[arrow.animate.set_stroke(GREY_B, width=3.5) for arrow in pipeline_arrows],
            ]

        self.play(FadeIn(caption1), *pulse_bright_anims(), run_time=max(0.05, 0.7))
        self.play(*pulse_normal_anims(), run_time=max(0.05, 0.5))
        self.play(*pulse_bright_anims(), run_time=max(0.05, 0.7))
        self.play(*pulse_normal_anims(), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.0))

        # Beat 5: hold 8.00-9.00
        self.wait(max(0.05, 1.0))

        # Module icon helpers and left-column layout
        module_x = -5.9

        filter_icon = VGroup(
            Line(LEFT * 0.55, LEFT * 0.12, color=BLUE, stroke_width=4),
            Line(LEFT * 0.12, DOWN * 0.22, color=BLUE, stroke_width=4),
            Line(DOWN * 0.22, RIGHT * 0.12, color=BLUE, stroke_width=4),
            Line(RIGHT * 0.12, RIGHT * 0.55, color=BLUE, stroke_width=4),
        )
        filter_icon.scale_to_fit_width(0.8)

        spec_cells = VGroup()
        for r in range(3):
            for c in range(4):
                cell = Square(side_length=0.14)
                cell.set_fill(TEAL, opacity=0.30 + 0.16 * c + 0.06 * r)
                cell.set_stroke(TEAL, width=0.5, opacity=0.55)
                spec_cells.add(cell)
        spec_cells.arrange_in_grid(rows=3, cols=4, buff=0.05)
        spectrogram_icon = spec_cells
        spectrogram_icon.scale_to_fit_width(0.8)

        brain_mini = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=GREEN,
            fill_opacity=0.9,
            stroke_color=GREEN,
            stroke_width=0.6,
        ).scale_to_fit_height(0.38)

        wave_mini = SVGMobject(
            ASSET_PATHS["activity"],
            fill_color=GREEN,
            fill_opacity=0.9,
            stroke_color=GREEN,
            stroke_width=0.6,
        ).scale_to_fit_height(0.38)

        electrode_tip = VGroup(
            Polygon(
                np.array([-0.12, -0.10, 0]),
                np.array([0.12, -0.10, 0]),
                np.array([0, 0.22, 0]),
                fill_color=GREEN,
                fill_opacity=1,
                stroke_color=GREEN,
                stroke_width=0.8,
            ),
            Line(ORIGIN, UP * 0.28, color=GREEN, stroke_width=2),
        )
        electrode_tip.scale_to_fit_height(0.5)

        modality_icons_row = VGroup(brain_mini, wave_mini, electrode_tip)
        modality_icons_row.arrange(RIGHT, buff=0.16)
        modality_icons_row.scale_to_fit_width(1.3)

        module1_group = VGroup(
            filter_icon,
            Text("Filtering (Module 5)", font_size=14, color=WHITE, weight="SEMIBOLD").scale_to_fit_width(1.9),
        ).arrange(DOWN, buff=0.1)

        module2_group = VGroup(
            spectrogram_icon,
            Text("Time-Frequency (Module 6)", font_size=14, color=WHITE, weight="SEMIBOLD").scale_to_fit_width(1.9),
        ).arrange(DOWN, buff=0.1)

        module3_group = VGroup(
            modality_icons_row,
            Text("Recording Modalities (Module 7)", font_size=14, color=WHITE, weight="SEMIBOLD").scale_to_fit_width(2.0),
        ).arrange(DOWN, buff=0.1)

        module1_group.move_to(np.array([module_x, 2.25, 0]))
        module2_group.move_to(np.array([module_x, 1.15, 0]))
        module3_group.move_to(np.array([module_x, 0.05, 0]))

        def make_dotted_arrow(start, end, color=GREY_B):
            line = DashedLine(start, end, color=color, stroke_width=1.8, dash_length=0.10)
            vec = end - start
            ang = np.arctan2(vec[1], vec[0])
            u = np.array([np.cos(ang), np.sin(ang), 0])
            perp = np.array([-np.sin(ang), np.cos(ang), 0])
            tip_len = 0.09
            tip_width = 0.06
            tip = Polygon(
                end,
                end - tip_len * u + tip_width * perp,
                end - tip_len * u - tip_width * perp,
                color=color,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            return VGroup(line, tip)

        raw_target = box_rects[0].get_left() + LEFT * 0.02
        preproc_target = box_rects[1].get_left() + LEFT * 0.02

        module1_arrow = make_dotted_arrow(filter_icon.get_right() + RIGHT * 0.10, raw_target, BLUE)
        module2_arrow = make_dotted_arrow(spectrogram_icon.get_right() + RIGHT * 0.10, preproc_target, TEAL)
        module3_arrow = make_dotted_arrow(modality_icons_row.get_right() + RIGHT * 0.10, raw_target + DOWN * 0.18, GREEN)

        # Beat 6: first module icon 9.00-10.88
        self.play(FadeIn(module1_group, module1_arrow, shift=RIGHT * 0.2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.88))

        # Beat 7: second module icon 10.88-13.54
        self.play(FadeIn(module2_group, module2_arrow, shift=RIGHT * 0.2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.66))

        # Beat 8: third module icon 13.54-17.46
        self.play(FadeIn(module3_group, module3_arrow, shift=RIGHT * 0.2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.92))

        # Beat 9: sequential module pulses 17.46-20.16
        module_visuals = [filter_icon, spectrogram_icon, modality_icons_row]
        module_accents = [BLUE, TEAL, GREEN]
        module_glows = []

        for vis, accent in zip(module_visuals, module_accents):
            glow = SurroundingRectangle(
                vis,
                color=accent,
                buff=0.10,
                stroke_width=5,
                fill_color=accent,
                fill_opacity=0.0,
            )
            glow.move_to(vis.get_center())
            glow.set_stroke(opacity=0.0)
            glow.set_fill(opacity=0.0)
            module_glows.append(glow)
        self.add(*module_glows)

        for vis, glow, accent in zip(module_visuals, module_glows, module_accents):
            self.play(
                glow.animate.set_stroke(opacity=0.9, width=7).set_fill(opacity=0.14),
                vis.animate.set_color(WHITE),
                run_time=max(0.05, 0.45),
            )
            self.play(
                glow.animate.set_stroke(opacity=0.0, width=5).set_fill(opacity=0.0),
                vis.animate.set_color(accent),
                run_time=max(0.05, 0.45),
            )

        # Beat 10: hold 20.16-22.84
        self.wait(max(0.05, 2.68))

        # Beat 11: highlight Preprocessing and Feature Extraction 22.84-25.46
        self.play(
            glows[1].animate.set_stroke(opacity=0.8).set_fill(opacity=0.16),
            glows[2].animate.set_stroke(opacity=0.8).set_fill(opacity=0.16),
            box_rects[1].animate.set_stroke(TEAL, width=5).set_fill(TEAL, opacity=0.30),
            box_rects[2].animate.set_stroke(GREEN, width=5).set_fill(GREEN, opacity=0.30),
            box_groups[0].animate.set_opacity(0.35),
            box_groups[3].animate.set_opacity(0.35),
            run_time=max(0.05, 1.4),
        )
        self.wait(max(0.05, 1.22))

        # Beat 12: processing strip + noisy waveform enters 25.46-29.36
        strip_left_x = box_rects[0].get_left()[0]
        strip_right_x = box_rects[3].get_right()[0]
        strip_y = -0.65

        strip = Rectangle(
            width=(strip_right_x - strip_left_x) + 0.4,
            height=0.32,
            fill_color=GREY,
            fill_opacity=0.06,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        strip.move_to(np.array([(strip_left_x + strip_right_x) / 2, strip_y, 0]))

        wave_start_x = strip_left_x - 0.5
        wave_end_x = strip_right_x
        p_tracker = ValueTracker(0.0)
        smooth_tracker = ValueTracker(0.0)

        def build_wave():
            p = p_tracker.get_value()
            s = smooth_tracker.get_value()
            cx = wave_start_x + p * (wave_end_x - wave_start_x)
            n = 28
            pts = []
            for j in range(n + 1):
                u = j / n - 0.5
                x = cx + u * 1.8
                noise = 0.20 * np.sin(14.0 * u + 0.9) + 0.09 * np.sin(31.0 * u + 1.8) + 0.045 * np.sin(53.0 * u + 2.4)
                smooth = 0.04 * np.sin(3.0 * u + 0.3)
                y = strip_y + (1 - s) * noise + s * smooth
                pts.append(np.array([x, y, 0]))
            segs = VGroup()
            for j in range(n):
                seg = Line(pts[j], pts[j + 1], color=BLUE, stroke_width=2.4)
                segs.add(seg)
            return segs

        wave_group = always_redraw(build_wave)
        wave_group.set_z_index(2)

        self.play(FadeIn(strip), run_time=max(0.05, 0.6))
        self.add(wave_group)
        self.play(p_tracker.animate.set_value(0.35), run_time=max(0.05, 3.3))

        # Build output symbols now; they will appear in beats 14-16.
        out_xs = [strip_right_x - 0.9, strip_right_x + 0.15, strip_right_x + 1.05]
        out_y = -0.05

        output_label_rect = RoundedRectangle(
            width=1.0,
            height=0.42,
            corner_radius=0.08,
            fill_color=WHITE,
            fill_opacity=0.9,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        output_label_text = Text("Interpreted", font_size=15, color=BLACK, weight="BOLD")
        output_label_text.move_to(output_label_rect.get_center())
        output_label_group = VGroup(output_label_rect, output_label_text)
        output_label_group.move_to(np.array([out_xs[0], out_y, 0]))

        cmd_square = Rectangle(
            width=0.45,
            height=0.45,
            fill_color=ORANGE,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        cmd_arrow_shaft = Line(RIGHT * 0.16, LEFT * 0.12, color=WHITE, stroke_width=3)
        cmd_arrow_head = Polygon(
            LEFT * 0.12,
            LEFT * 0.12 + UP * 0.06,
            LEFT * 0.12 + DOWN * 0.06,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        )
        output_command_group = VGroup(cmd_square, cmd_arrow_shaft, cmd_arrow_head)
        output_command_group.move_to(np.array([out_xs[1], out_y, 0]))

        understand_glow = Circle(radius=0.24, fill_color=PURPLE, fill_opacity=0.25, stroke_width=0)
        understand_brain = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=PURPLE,
            fill_opacity=0.9,
            stroke_color=PURPLE,
            stroke_width=0.6,
        ).scale_to_fit_height(0.40)
        output_understand_group = VGroup(understand_glow, understand_brain)
        output_understand_group.move_to(np.array([out_xs[2], out_y, 0]))

        def make_output_arrow(x, output_group):
            start = np.array([x, strip_y + 0.10, 0])
            end = np.array([x, output_group.get_bottom()[1] - 0.06, 0])
            return Arrow(start, end, color=GREY_B, stroke_width=3, buff=0.02, max_tip_length_to_length_ratio=0.30)

        output_arrow_label = make_output_arrow(out_xs[0], output_label_group)
        output_arrow_command = make_output_arrow(out_xs[1], output_command_group)
        output_arrow_understand = make_output_arrow(out_xs[2], output_understand_group)

        # Beat 13: waveform passes through middle and smooths 29.36-30.70
        self.play(
            glows[1].animate.set_stroke(opacity=1.0).set_fill(opacity=0.22),
            box_rects[1].animate.set_stroke(TEAL, width=6).set_fill(TEAL, opacity=0.34),
            run_time=max(0.05, 0.4),
        )
        self.play(
            p_tracker.animate.set_value(0.55),
            smooth_tracker.animate.set_value(0.35),
            run_time=max(0.05, 0.27),
        )
        self.play(
            glows[2].animate.set_stroke(opacity=1.0).set_fill(opacity=0.22),
            box_rects[2].animate.set_stroke(GREEN, width=6).set_fill(GREEN, opacity=0.34),
            run_time=max(0.05, 0.4),
        )
        self.play(
            p_tracker.animate.set_value(0.8),
            smooth_tracker.animate.set_value(1.0),
            run_time=max(0.05, 0.27),
        )

        # Beat 14: cleaned waveform reaches right end and first output appears 30.70-31.46
        self.play(p_tracker.animate.set_value(1.0), run_time=max(0.05, 0.20))
        wave_group.clear_updaters()
        self.play(wave_group.animate.set_color(GREEN), run_time=max(0.05, 0.13))
        self.play(
            wave_group.animate.set_color(BLUE),
            FadeIn(output_label_group, output_arrow_label),
            run_time=max(0.05, 0.43),
        )

        # Beat 15: command output + control caption 31.46-32.66
        self.play(FadeIn(output_command_group, output_arrow_command), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.36))

        control_caption = Text(
            "or used to control a system",
            font_size=18,
            color=GREY_B,
            weight="SEMIBOLD",
        )
        control_caption.move_to(np.array([output_command_group.get_center()[0], strip_y - 0.55, 0]))
        self.play(FadeIn(control_caption), run_time=max(0.05, 0.24))

        # Beat 16: understanding output 32.66-33.60
        self.play(FadeIn(output_understand_group, output_arrow_understand), run_time=max(0.05, 0.94))

        # Beat 17: final caption and full-composition restore 33.60-34.58
        final_caption = Text(
            "A complete workflow, not isolated techniques",
            font_size=26,
            color=WHITE,
            weight="BOLD",
        )
        final_caption.scale_to_fit_width(11)
        final_caption.to_edge(DOWN, buff=0.30)

        restore_anims = [
            box_groups[0].animate.set_opacity(1.0),
            box_groups[3].animate.set_opacity(1.0),
            box_rects[1].animate.set_stroke(WHITE, width=2).set_fill(GREY, opacity=0.18),
            box_rects[2].animate.set_stroke(WHITE, width=2).set_fill(GREY, opacity=0.18),
            glows[1].animate.set_stroke(opacity=0.0).set_fill(opacity=0.0),
            glows[2].animate.set_stroke(opacity=0.0).set_fill(opacity=0.0),
        ]

        self.play(FadeIn(final_caption), *restore_anims, run_time=max(0.05, 0.4))
        self.play(final_caption.animate.set_color(GOLD), run_time=max(0.05, 0.19))
        self.play(final_caption.animate.set_color(WHITE), run_time=max(0.05, 0.19))
        self.wait(max(0.05, 0.20))