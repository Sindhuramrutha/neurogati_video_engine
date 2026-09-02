ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene11(Scene):
    def build_acquisition_chain(self):
        block_names = ["sensors", "amplification", "filtering", "digitization", "recording"]
        blocks = []
        for name in block_names:
            rect = Rectangle(
                width=1.9,
                height=0.60,
                fill_color=BLUE,
                fill_opacity=0.25,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            label = Text(name, font_size=15, color=WHITE).scale_to_fit_width(1.6)
            block = VGroup(rect, label)
            blocks.append(block)

        first_rect = blocks[0][0]
        first_label = blocks[0][1]
        first_rect.set_fill(YELLOW, opacity=0.9)
        first_rect.set_stroke(YELLOW, width=3)
        first_label.set_color(BLACK)

        blocks_row = VGroup(*blocks).arrange(RIGHT, buff=0.32)
        arrows = VGroup()
        for i in range(len(blocks) - 1):
            arr = Arrow(
                start=blocks[i].get_right(),
                end=blocks[i + 1].get_left(),
                color=GREY_B,
                stroke_width=3,
                buff=0.06,
                max_tip_length_to_length_ratio=0.18,
            )
            arrows.add(arr)

        chain = VGroup(blocks_row, arrows)
        return chain, blocks[0]

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Beat 1: 0.00–1.46 — faint previous acquisition chain + centered text
        # ------------------------------------------------------------------
        chain_blocks, first_chain_block = self.build_acquisition_chain()
        chain_blocks.set_opacity(0.28)
        chain_blocks.scale_to_fit_width(8.5)
        chain_blocks.to_edge(DOWN, buff=0.25)
        self.add(chain_blocks)

        intro_text = Text(
            "Now let's bring this together",
            font_size=46,
            weight="BOLD",
            color=WHITE,
        )
        intro_text.move_to(ORIGIN)
        self.play(Write(intro_text), run_time=max(0.05, 1.16))
        self.wait(max(0.05, 0.30))

        # ------------------------------------------------------------------
        # Gap 1.46–2.30
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------------
        # Beat 2: 2.30–6.04 — comparison table, row labels brighten by name
        # ------------------------------------------------------------------
        headers = ["Detection principle", "Location", "Invasiveness", "Signal quality"]
        row_labels_texts = ["EEG electrodes", "ECoG grids", "MEG sensors"]

        col_widths = [2.3, 1.9, 1.7, 2.5]
        row_label_width = 2.4
        cell_height = 0.55

        header_texts = []
        header_cells = []
        corner_spacer = Rectangle(
            width=row_label_width,
            height=cell_height,
            fill_opacity=0.0,
            stroke_opacity=0.0,
        )

        for c, header in enumerate(headers):
            rect = Rectangle(
                width=col_widths[c],
                height=cell_height,
                fill_opacity=0.0,
                stroke_opacity=0.0,
            )
            txt = Text(header, font_size=18, weight="BOLD", color=WHITE)
            txt.scale_to_fit_width(col_widths[c] - 0.25)
            txt.move_to(rect)
            header_texts.append(txt)
            header_cells.append(VGroup(rect, txt))

        header_row = VGroup(corner_spacer, *header_cells).arrange(RIGHT, buff=0.20)

        row_rect_groups = []
        cell_rects = [[None for _ in range(4)] for _ in range(3)]
        for r in range(3):
            label_rect = Rectangle(
                width=row_label_width,
                height=cell_height,
                fill_opacity=0.0,
                stroke_opacity=0.0,
            )
            rects = []
            for c in range(4):
                rect = Rectangle(
                    width=col_widths[c],
                    height=cell_height,
                    fill_color=GREY_B,
                    fill_opacity=0.08,
                    stroke_color=GREY_B,
                    stroke_width=1.5,
                )
                rects.append(rect)
                cell_rects[r][c] = rect
            row_group = VGroup(label_rect, *rects).arrange(RIGHT, buff=0.20)
            row_rect_groups.append(row_group)

        table_base = VGroup(header_row, *row_rect_groups).arrange(DOWN, buff=0.20)
        table_base.move_to(np.array([0, 0.6, 0]))

        row_label_mobs = []
        for r, label_text in enumerate(row_labels_texts):
            label_rect = row_rect_groups[r][0]
            txt = Text(label_text, font_size=20, weight="BOLD", color=GREY_B)
            txt.scale_to_fit_width(row_label_width - 0.35)
            txt.move_to(label_rect)
            txt.set_z_index(4)
            row_label_mobs.append(txt)

        cell_values = [
            ["Electrical voltage", "Scalp", "Non-invasive", "Lower signal quality"],
            ["Electrical voltage", "Cortical surface", "Invasive", "Higher signal quality"],
            ["Magnetic fields", "Just outside head", "Non-invasive", "Intermediate signal quality"],
        ]
        cell_texts = [[None for _ in range(4)] for _ in range(3)]
        for r in range(3):
            for c in range(4):
                txt = Text(cell_values[r][c], font_size=15, color=WHITE)
                txt.scale_to_fit_width(col_widths[c] - 0.35)
                txt.move_to(cell_rects[r][c])
                txt.set_z_index(2)
                cell_texts[r][c] = txt

        self.play(FadeOut(intro_text), FadeIn(table_base), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.05))

        for label in row_label_mobs:
            self.play(FadeIn(label), run_time=max(0.05, 0.13))
        self.wait(max(0.05, 0.01))

        self.play(row_label_mobs[0].animate.set_color(YELLOW), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.86))

        self.play(row_label_mobs[1].animate.set_color(YELLOW), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.36))

        self.play(row_label_mobs[2].animate.set_color(YELLOW), run_time=max(0.05, 0.52))

        # ------------------------------------------------------------------
        # Beat 3: 6.20–8.34 — "same fundamental job" bracket
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.16))

        same_job_bracket = SurroundingRectangle(
            VGroup(*row_label_mobs),
            color=TEAL,
            buff=0.12,
            corner_radius=0.08,
        )
        same_job_bracket.set_fill(TEAL, opacity=0.12)
        same_job_bracket.set_stroke(TEAL, width=3)
        same_job_bracket.set_z_index(1)

        same_job_caption = Text(
            "same fundamental job",
            font_size=26,
            weight="BOLD",
            color=YELLOW,
        )
        same_job_caption.next_to(table_base, DOWN, buff=0.35)

        self.play(
            Create(same_job_bracket),
            FadeIn(same_job_caption),
            run_time=max(0.05, 0.70),
        )
        self.play(
            Wiggle(same_job_bracket, scale_value=1.04),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.18))
        self.play(
            FadeOut(same_job_caption),
            FadeOut(same_job_bracket),
            run_time=max(0.05, 0.40),
        )

        # ------------------------------------------------------------------
        # Beat 4: 8.80–12.50 — fill first two cells row by row
        # ------------------------------------------------------------------
        for r in range(3):
            for c in range(2):
                self.play(FadeIn(cell_texts[r][c]), run_time=max(0.05, 0.52))

        chain_arrow = Arrow(
            start=table_base.get_bottom() + DOWN * 0.2,
            end=first_chain_block.get_top() + UP * 0.1,
            color=GREEN,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(
            chain_blocks.animate.set_opacity(1.0),
            Create(chain_arrow),
            run_time=max(0.05, 0.58),
        )

        # ------------------------------------------------------------------
        # Gap 12.50–13.10
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.30))
        self.play(FadeOut(chain_arrow), run_time=max(0.05, 0.30))

        # ------------------------------------------------------------------
        # Beat 5: 13.10–19.04 — invasiveness + signal quality columns
        # ------------------------------------------------------------------
        loc_inv_highlight = SurroundingRectangle(
            VGroup(header_texts[1], header_texts[2]),
            color=GREEN,
            buff=0.12,
            corner_radius=0.05,
        )
        loc_inv_highlight.set_fill(GREEN, opacity=0.06)
        loc_inv_highlight.set_stroke(GREEN, width=3)
        loc_inv_highlight.set_z_index(3)

        self.play(FadeIn(loc_inv_highlight), run_time=max(0.05, 0.60))

        for r in range(3):
            self.play(FadeIn(cell_texts[r][2]), run_time=max(0.05, 0.90))

        quality_highlight = SurroundingRectangle(
            header_texts[3],
            color=ORANGE,
            buff=0.12,
            corner_radius=0.05,
        )
        quality_highlight.set_fill(ORANGE, opacity=0.06)
        quality_highlight.set_stroke(ORANGE, width=3)
        quality_highlight.set_z_index(3)

        self.play(
            FadeOut(loc_inv_highlight),
            FadeIn(quality_highlight),
            run_time=max(0.05, 0.60),
        )

        for r in range(3):
            self.play(FadeIn(cell_texts[r][3]), run_time=max(0.05, 0.68))

        # ------------------------------------------------------------------
        # Gap 19.04–19.90
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.16))
        self.play(
            FadeOut(quality_highlight),
            FadeOut(chain_blocks),
            run_time=max(0.05, 0.24),
        )
        self.wait(max(0.05, 0.46))

        # ------------------------------------------------------------------
        # Beat 6: 19.90–23.72 — table shifts up, balance beam appears
        # ------------------------------------------------------------------
        all_table = VGroup(
            table_base,
            *row_label_mobs,
            *[cell_texts[r][c] for r in range(3) for c in range(4)],
        )

        beam_center = np.array([0, -1.4, 0])
        beam = Rectangle(
            width=6.4,
            height=0.22,
            fill_color=GREY_B,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        beam.move_to(beam_center)

        fulcrum_apex = beam.get_bottom()
        fulcrum = Polygon(
            fulcrum_apex + DOWN * 0.55 + LEFT * 0.45,
            fulcrum_apex + DOWN * 0.55 + RIGHT * 0.45,
            fulcrum_apex,
            fill_color=ORANGE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5,
        )

        left_beam_end = beam.get_left()
        right_beam_end = beam.get_right()
        left_pan_center = np.array([left_beam_end[0], -2.55, 0])
        right_pan_center = np.array([right_beam_end[0], -2.55, 0])

        left_pan = Rectangle(
            width=2.4,
            height=0.16,
            fill_color=GREY_B,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).move_to(left_pan_center)
        right_pan = Rectangle(
            width=2.4,
            height=0.16,
            fill_color=GREY_B,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=1.5,
        ).move_to(right_pan_center)

        left_string1 = Line(left_beam_end, left_pan.get_left() + UP * 0.08, color=WHITE, stroke_width=2)
        left_string2 = Line(left_beam_end, left_pan.get_right() + UP * 0.08, color=WHITE, stroke_width=2)
        right_string1 = Line(right_beam_end, right_pan.get_left() + UP * 0.08, color=WHITE, stroke_width=2)
        right_string2 = Line(right_beam_end, right_pan.get_right() + UP * 0.08, color=WHITE, stroke_width=2)

        balance_assembly = VGroup(
            beam,
            left_string1,
            left_string2,
            right_string1,
            right_string2,
            left_pan,
            right_pan,
        )

        left_weight_pos1 = left_pan_center + UP * 0.42 + LEFT * 0.60
        left_weight_pos2 = left_pan_center + UP * 0.42 + RIGHT * 0.60
        right_weight_pos1 = right_pan_center + UP * 0.42 + RIGHT * 0.60
        right_weight_pos2 = right_pan_center + UP * 0.42 + LEFT * 0.60

        def make_weight(label, position, color):
            block = Rectangle(
                width=0.95,
                height=0.50,
                fill_color=color,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            block.move_to(position)
            label_text = Text(label, font_size=14, weight="BOLD", color=BLACK, line_spacing=0.6)
            label_text.scale_to_fit_width(0.80)
            label_text.move_to(block)
            return VGroup(block, label_text).move_to(position)

        self.play(
            all_table.animate.scale(0.75).move_to(np.array([0, 2.0, 0])),
            FadeIn(fulcrum),
            FadeIn(balance_assembly),
            run_time=max(0.05, 0.60),
        )

        lw1 = make_weight("signal\nquality", left_weight_pos1, YELLOW)
        lw1.set_opacity(0)
        balance_assembly.add(lw1)
        self.play(
            lw1.animate.set_opacity(1),
            balance_assembly.animate.rotate(0.12, about_point=fulcrum_apex),
            run_time=max(0.05, 0.80),
        )

        rw1 = make_weight("spatial\nresolution", right_weight_pos1, TEAL)
        rw1.set_opacity(0)
        balance_assembly.add(rw1)
        self.play(
            rw1.animate.set_opacity(1),
            balance_assembly.animate.rotate(-0.24, about_point=fulcrum_apex),
            run_time=max(0.05, 0.90),
        )

        self.play(
            balance_assembly.animate.rotate(-0.03, about_point=fulcrum_apex),
            rate_func=there_and_back,
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------------
        # Gap 23.72–24.10
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.38))

        # ------------------------------------------------------------------
        # Beat 7: 24.10–28.26 — second weights, beam tips right
        # ------------------------------------------------------------------
        lw2 = make_weight("patient\nsafety", left_weight_pos2, GREEN)
        lw2.set_opacity(0)
        balance_assembly.add(lw2)
        self.play(
            all_table.animate.set_opacity(0.25),
            lw2.animate.set_opacity(1),
            balance_assembly.animate.rotate(0.20, about_point=fulcrum_apex),
            run_time=max(0.05, 0.60),
        )

        rw2 = make_weight("invasiveness", right_weight_pos2, RED)
        rw2.set_opacity(0)
        balance_assembly.add(rw2)
        self.play(
            rw2.animate.set_opacity(1),
            balance_assembly.animate.rotate(-0.36, about_point=fulcrum_apex),
            run_time=max(0.05, 0.90),
        )

        left_arrow = Arrow(
            start=beam.get_left() + UP * 0.20 + LEFT * 0.25,
            end=beam.get_left() + UP * 0.85 + LEFT * 0.25,
            color=YELLOW,
            stroke_width=4,
            buff=0.05,
            max_tip_length_to_length_ratio=0.28,
        )
        right_arrow = Arrow(
            start=beam.get_right() + DOWN * 0.20 + RIGHT * 0.25,
            end=beam.get_right() + DOWN * 0.85 + RIGHT * 0.25,
            color=YELLOW,
            stroke_width=4,
            buff=0.05,
            max_tip_length_to_length_ratio=0.28,
        )
        motion_arrows = VGroup(left_arrow, right_arrow)
        self.play(FadeIn(motion_arrows), run_time=max(0.05, 0.60))
        self.play(
            Wiggle(motion_arrows, scale_value=1.15),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 1.26))

        # ------------------------------------------------------------------
        # Beat 8: 28.26–29.05 — hold final layout
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.79))