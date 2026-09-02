ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(Scene):
    def make_question_box(self, text, fill_color=BLUE):
        box = RoundedRectangle(
            width=4.4,
            height=1.2,
            corner_radius=0.25,
            fill_color=fill_color,
            fill_opacity=0.25,
            stroke_color=fill_color,
            stroke_width=3,
        )
        label = Text(text, font_size=22, color=WHITE, weight="BOLD").scale_to_fit_width(4.0)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_analysis_box(self, title, icon, fill_color):
        box = RoundedRectangle(
            width=4.0,
            height=1.8,
            corner_radius=0.25,
            fill_color=fill_color,
            fill_opacity=0.30,
            stroke_color=fill_color,
            stroke_width=3,
        )
        title_text = Text(title, font_size=22, color=WHITE, weight="BOLD").scale_to_fit_width(2.2)
        icon.scale_to_fit_width(1.2)
        content = VGroup(icon, title_text).arrange(RIGHT, buff=0.25)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def make_erp_icon(self):
        axes = VGroup(
            Line([-0.8, 0, 0], [0.8, 0, 0], color=GREY_B, stroke_width=2),
            Line([0, -0.2, 0], [0, 0.8, 0], color=GREY_B, stroke_width=2),
        )
        wave = FunctionGraph(
            lambda x: 0.55 * np.exp(-0.5 * ((x - 0.0) / 0.22) ** 2),
            x_range=[-0.8, 0.8, 0.02],
            color=YELLOW,
            stroke_width=2,
        )
        return VGroup(axes, wave)

    def make_tf_icon(self):
        rows, cols = 4, 5
        cell_w, cell_h = 0.28, 0.25
        palette = [BLUE, TEAL, ORANGE, YELLOW]
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                rect = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    fill_color=palette[(r + c) % len(palette)],
                    fill_opacity=0.9,
                    stroke_width=0,
                )
                rect.move_to(
                    np.array([
                        (c - (cols - 1) / 2) * cell_w,
                        (r - (rows - 1) / 2) * cell_h,
                        0,
                    ])
                )
                cells.add(rect)

        border = Rectangle(
            width=cols * cell_w + 0.1,
            height=rows * cell_h + 0.1,
            stroke_color=GREY,
            stroke_width=1.5,
            fill_opacity=0,
        )
        time_line = Line([-0.9, -0.75, 0], [0.9, -0.75, 0], color=GREY, stroke_width=1.5)
        freq_line = Line([-0.9, -0.75, 0], [-0.9, 0.7, 0], color=GREY, stroke_width=1.5)
        t_label = Text("t", font_size=13, color=GREY).next_to(time_line, DOWN, buff=0.05)
        f_label = Text("f", font_size=13, color=GREY).next_to(freq_line, LEFT, buff=0.05)
        return VGroup(cells, border, time_line, freq_line, t_label, f_label)

    def make_empty_layout(self, first_q_pos, second_q_pos, left_analysis_pos, right_analysis_pos, bottom_pos):
        empty = VGroup()
        dims = [
            (4.4, 1.2, first_q_pos),
            (4.4, 1.2, second_q_pos),
            (4.0, 1.8, left_analysis_pos),
            (4.0, 1.8, right_analysis_pos),
            (4.2, 1.1, bottom_pos),
        ]
        for w, h, pos in dims:
            dash_rect = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.25,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_opacity=0,
            )
            dash_rect.move_to(pos)
            empty.add(dash_rect)

        paths = [
            (first_q_pos + DOWN * 0.6 + LEFT * 0.5, left_analysis_pos + UP * 0.9),
            (second_q_pos + DOWN * 0.6 + RIGHT * 0.5, right_analysis_pos + UP * 0.9),
            (left_analysis_pos + DOWN * 0.9 + RIGHT * 0.2, bottom_pos + UP * 0.55),
            (right_analysis_pos + DOWN * 0.9 + LEFT * 0.2, bottom_pos + UP * 0.55),
        ]
        for p1, p2 in paths:
            dashed = DashedLine(p1, p2, dash_length=0.12, color=GREY_B, stroke_width=2)
            empty.add(dashed)

        empty.set_opacity(0.28)
        return empty

    def make_previous_final(self):
        group = VGroup()
        left_rect = Rectangle(
            width=4.5,
            height=2.8,
            fill_color=BLACK,
            fill_opacity=0.4,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to([-3.2, 0, 0])
        right_rect = Rectangle(
            width=4.5,
            height=2.8,
            fill_color=BLACK,
            fill_opacity=0.4,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to([3.2, 0, 0])
        group.add(left_rect, right_rect)

        for cx in [-3.2, 3.2]:
            ax = Line([cx - 2, -0.7, 0], [cx + 2, -0.7, 0], color=GREY, stroke_width=2)
            group.add(ax)

        for xc in [-3.8, -3.2, -2.6]:
            wave = FunctionGraph(
                lambda x, xc=xc: -0.7 + 0.45 * np.exp(-0.5 * ((x - xc) / 0.22) ** 2),
                x_range=[xc - 0.9, xc + 0.9, 0.02],
                color=TEAL,
                stroke_width=2,
            )
            group.add(wave)

        for xc in [2.3, 3.2, 4.0]:
            wave = FunctionGraph(
                lambda x, xc=xc: -0.7 + 0.45 * np.exp(-0.5 * ((x - xc) / 0.22) ** 2),
                x_range=[xc - 0.9, xc + 0.9, 0.02],
                color=ORANGE,
                stroke_width=2,
            )
            group.add(wave)

        t1 = Text("Time-Locked", font_size=20, color=TEAL).move_to([-3.2, 1.2, 0])
        t2 = Text("Induced", font_size=20, color=ORANGE).move_to([3.2, 1.2, 0])
        group.add(t1, t2)
        return group

    def construct(self):
        self.camera.background_color = "#0F1116"

        first_q_pos = np.array([-2.2, 2.4, 0])
        second_q_pos = np.array([2.2, 2.4, 0])
        left_analysis_pos = np.array([-4.0, -0.5, 0])
        right_analysis_pos = np.array([4.0, -0.5, 0])
        bottom_pos = np.array([0.0, -2.7, 0])

        # Beat 1: previous final image fades out, empty layout fades in
        prev_final = self.make_previous_final()
        empty_layout = self.make_empty_layout(
            first_q_pos, second_q_pos, left_analysis_pos, right_analysis_pos, bottom_pos
        )
        self.add(prev_final)
        self.play(FadeOut(prev_final), FadeIn(empty_layout), run_time=max(0.05, 2.54))
        self.remove(prev_final)

        # Beat 2: first top question box
        first_q = self.make_question_box(
            "Objective: consistent responses after each stimulus?", fill_color=BLUE
        ).move_to(first_q_pos)
        self.play(FadeIn(first_q), run_time=max(0.05, 3.12))

        # Beat 3: labeled left arrow (label appears in Beat 5)
        left_arrow = Arrow(
            first_q_pos + DOWN * 0.6 + LEFT * 0.5,
            left_analysis_pos + UP * 0.9 + RIGHT * 0.3,
            color=GREY_B,
            stroke_width=5,
            buff=0.05,
        )
        self.play(FadeIn(left_arrow), run_time=max(0.05, 0.58))
        self.wait(max(0.05, 0.82))

        # Beat 4: highlight first question and brighten left arrow
        self.play(
            first_q[0].animate.set_stroke(color=YELLOW, width=4),
            left_arrow.animate.set_color(GOLD).set_stroke(width=6),
            run_time=max(0.05, 2.16),
        )

        # Beat 5: consistent timing label, dim top question slightly
        consistent_label = Text(
            "Consistent timing", font_size=24, color=GOLD, weight="BOLD"
        ).move_to([-1.4, 1.5, 0])
        self.play(
            FadeIn(consistent_label),
            first_q.animate.set_opacity(0.65),
            run_time=max(0.05, 2.86),
        )

        # Beat 6: left analysis box (ERP)
        erp_icon = self.make_erp_icon()
        erp_box = self.make_analysis_box("ERP analysis", erp_icon, TEAL).move_to(left_analysis_pos)
        self.play(FadeIn(erp_box), run_time=max(0.05, 2.84))
        self.wait(max(0.05, 0.80))

        # Beat 7: second top question box + right arrow
        second_q = self.make_question_box(
            "Objective: oscillatory changes with variable timing?", fill_color=BLUE
        ).move_to(second_q_pos)
        right_arrow = Arrow(
            second_q_pos + DOWN * 0.6 + RIGHT * 0.5,
            right_analysis_pos + UP * 0.9 + LEFT * 0.3,
            color=GREY_B,
            stroke_width=5,
            buff=0.05,
        )
        self.play(FadeIn(second_q), FadeIn(right_arrow), run_time=max(0.05, 1.94))
        top_q_group = VGroup(first_q, second_q)

        # Beat 8: variable timing label, highlight right question, dim left branch
        variable_label = Text(
            "Variable timing", font_size=24, color=GOLD, weight="BOLD"
        ).move_to([1.4, 1.5, 0])
        left_branch = VGroup(left_arrow, consistent_label, erp_box)
        self.play(
            FadeIn(variable_label),
            second_q[0].animate.set_stroke(color=YELLOW, width=4),
            right_arrow.animate.set_color(GOLD).set_stroke(width=6),
            left_branch.animate.set_opacity(0.45),
            run_time=max(0.05, 3.92),
        )

        # Beat 9: right analysis box (time-frequency)
        tf_icon = self.make_tf_icon()
        tf_box = self.make_analysis_box(
            "Time-frequency analysis", tf_icon, ORANGE
        ).move_to(right_analysis_pos)
        self.play(FadeIn(tf_box), run_time=max(0.05, 4.20))

        # Beat 10: both analysis boxes equally emphasized, top questions dim
        right_branch = VGroup(right_arrow, variable_label, tf_box)
        self.play(
            left_branch.animate.set_opacity(1),
            right_branch.animate.set_opacity(1),
            top_q_group.animate.set_opacity(0.55),
            erp_box[0].animate.set_stroke(color=GOLD, width=4),
            tf_box[0].animate.set_stroke(color=GOLD, width=4),
            run_time=max(0.05, 4.84),
        )

        # Beat 11: spectrogram/wavelet label + annotations
        spec_label = Text(
            "Spectrograms & Wavelet analysis",
            font_size=22,
            color=YELLOW,
            weight="BOLD",
        ).scale_to_fit_width(4.0)
        spec_label.move_to([right_analysis_pos[0], 1.6, 0])
        spec_arrow1 = Arrow(
            spec_label.get_bottom() + LEFT * 0.4,
            tf_box[0].get_top() + LEFT * 0.2,
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
        )
        spec_arrow2 = Arrow(
            spec_label.get_bottom() + RIGHT * 0.4,
            tf_box[0].get_top() + RIGHT * 0.2,
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
        )
        spec_annotations = VGroup(spec_arrow1, spec_arrow2)
        self.play(FadeIn(spec_label), FadeIn(spec_annotations), run_time=max(0.05, 2.0))
        self.play(Indicate(spec_label, color=YELLOW, scale_factor=1.1), run_time=max(0.05, 2.68))
        self.wait(max(0.05, 0.72))

        right_branch.add(spec_label)

        # Beat 12: converging arrows from analysis boxes to bottom center
        left_conv = Arrow(
            left_analysis_pos + DOWN * 0.9 + RIGHT * 0.2,
            bottom_pos + UP * 0.55,
            color=GREY_B,
            stroke_width=5,
            buff=0.05,
        )
        right_conv = Arrow(
            right_analysis_pos + DOWN * 0.9 + LEFT * 0.2,
            bottom_pos + UP * 0.55,
            color=GREY_B,
            stroke_width=5,
            buff=0.05,
        )
        self.play(FadeIn(left_conv), FadeIn(right_conv), run_time=max(0.05, 3.60))

        # Beat 13: bottom complementary insights box
        bottom_box = RoundedRectangle(
            width=4.2,
            height=1.1,
            corner_radius=0.25,
            fill_color=PURPLE,
            fill_opacity=0.35,
            stroke_color=GOLD,
            stroke_width=3,
        )
        bottom_text = Text(
            "Complementary insights",
            font_size=24,
            color=WHITE,
            weight="BOLD",
        ).scale_to_fit_width(3.8)
        bottom_text.move_to(bottom_box.get_center())
        bottom_box_group = VGroup(bottom_box, bottom_text).move_to(bottom_pos)
        self.play(FadeIn(bottom_box_group), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.98))

        # Beat 14: left branch highlighted, bottom brightens, ERP pulse + caption
        left_caption = Text(
            "Reveals time-locked neural responses",
            font_size=20,
            color=WHITE,
            weight="BOLD",
        ).scale_to_fit_width(3.8)
        left_caption.move_to([left_analysis_pos[0], -1.75, 0])
        self.play(
            FadeIn(left_caption),
            left_branch.animate.set_opacity(1),
            right_branch.animate.set_opacity(0.5),
            spec_annotations.animate.set_opacity(0.5),
            bottom_box_group[0].animate.set_stroke(color=YELLOW, width=4),
            run_time=max(0.05, 2.0),
        )
        self.play(Indicate(erp_box[0], color=TEAL, scale_factor=1.1), run_time=max(0.05, 2.66))
        self.wait(max(0.05, 0.74))

        # Beat 15: right branch highlighted, bottom remains bright, TF pulse + caption
        right_caption = Text(
            "Reveals induced activity — may not be visible after averaging",
            font_size=20,
            color=WHITE,
            weight="BOLD",
        ).scale_to_fit_width(3.8)
        right_caption.move_to([right_analysis_pos[0], -1.75, 0])
        self.play(
            FadeOut(spec_annotations),
            FadeIn(right_caption),
            right_branch.animate.set_opacity(1),
            left_branch.animate.set_opacity(0.5),
            bottom_box_group[0].animate.set_stroke(color=GOLD, width=4),
            run_time=max(0.05, 1.5),
        )
        self.play(Indicate(tf_box[0], color=ORANGE, scale_factor=1.1), run_time=max(0.05, 2.92))

        # Beat 16: full diagram holds, bottom box glows softly
        self.play(
            bottom_box_group[0].animate.set_stroke(color=YELLOW, width=5).set_fill(opacity=0.45),
            run_time=max(0.05, 1.575),
        )
        self.play(
            bottom_box_group[0].animate.set_stroke(color=GOLD, width=4).set_fill(opacity=0.35),
            run_time=max(0.05, 1.575),
        )