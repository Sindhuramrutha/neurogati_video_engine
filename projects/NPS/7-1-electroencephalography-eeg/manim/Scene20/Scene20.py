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


class Scene20(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_trace(signal, x_min, x_max, y_scale=0.45, color=YELLOW, stroke_width=3.0, num_points=1000):
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            x = np.linspace(x_min, x_max, num_points)
            y = np.clip(signal(x) * y_scale, -y_scale, y_scale)
            pts = np.array([x, y, np.zeros_like(x)]).T
            mob.set_points_as_corners(pts)
            return mob

        def make_hump(center_x, center_y, width=1.8, height=0.45, sign=1, color=PURPLE, stroke_width=3.0):
            n = 320
            x = np.linspace(center_x - width / 2, center_x + width / 2, n)
            envelope = np.exp(-((x - center_x) / (width / 4)) ** 2)
            y = center_y + sign * height * envelope
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        def make_jagged(center_x, center_y, width=1.4, height=0.14, color=ORANGE,
                        freq1=7, freq2=13, stroke_width=2.0):
            n = 420
            x = np.linspace(center_x - width / 2, center_x + width / 2, n)
            envelope = np.exp(-((x - center_x) / (width / 4)) ** 2)
            small = (
                np.sin(2 * np.pi * freq1 * (x - center_x))
                + 0.7 * np.sin(2 * np.pi * freq2 * (x - center_x) + 1.3)
                + 0.5 * np.sin(2 * np.pi * (freq2 * 1.7) * (x - center_x) + 0.4)
            )
            y = center_y + small * height * envelope
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        def make_jump(center_x, center_y, step=0.18, color=ORANGE, stroke_width=2.5):
            x = [center_x - 0.25, center_x, center_x + 0.04, center_x + 0.30]
            y = [center_y, center_y, center_y + step, center_y + step]
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        # signals
        def noisy_base_func(x):
            return (
                0.16 * np.sin(2 * np.pi * 0.7 * x + 0.4)
                + 0.11 * np.sin(2 * np.pi * 0.23 * x + 1.1)
                + 0.09 * np.sin(2 * np.pi * 1.8 * x + 0.3)
                + 0.07 * np.sin(2 * np.pi * 3.4 * x + 1.9)
                + 0.04 * np.sin(2 * np.pi * 5.7 * x + 0.9)
                + 0.03 * np.sin(2 * np.pi * 9.2 * x + 2.4)
            )

        def clean_base_func(x):
            return 0.15 * np.sin(2 * np.pi * 0.8 * x + 0.3) + 0.04 * np.sin(2 * np.pi * 1.6 * x + 1.2)

        def clean_right_func(x):
            return clean_base_func(x) + 1.25 * np.exp(-((x) / 0.07) ** 2)

        def td_func(x):
            y = 0.10 * np.sin(2 * np.pi * 1.2 * x)
            y += 1.8 * np.exp(-((x + 0.7) / 0.045) ** 2)
            y += 0.9 * np.exp(-((x - 0.5) / 0.25) ** 2)
            return y

        # ---------- previous scene composition to fade out ----------
        prev_comp = VGroup(*[
            Rectangle(width=1.7, height=1.0, fill_color=BLACK, fill_opacity=0.7,
                      stroke_color=GREY_B, stroke_width=1.5)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.25).move_to(DOWN * 1.2)

        heading = Text("Signal Processing in EEG", font_size=36, weight="BOLD", color=WHITE)
        heading.scale_to_fit_width(10)
        heading.to_edge(UP, buff=0.35)

        raw_wave = make_trace(noisy_base_func, -14, 14, y_scale=0.4, color=YELLOW, stroke_width=3.0)
        raw_wave.move_to(UP * 0.5)
        noisy_group = VGroup(raw_wave)

        overlay_list = []

        # ---------- beat 1: 0.00 - 1.64 ----------
        self.play(
            FadeOut(prev_comp),
            Write(heading),
            FadeIn(raw_wave),
            run_time=max(0.05, 1.64),
        )

        # ---------- beat 2: 1.64 - 2.94 ----------
        self.play(noisy_group.animate.shift(LEFT * 0.55), run_time=max(0.05, 0.65))

        p = raw_wave.point_from_proportion(0.42)
        fuzz1 = make_jagged(p[0], p[1], width=1.4, height=0.14, color=ORANGE, freq1=7, freq2=13)
        noisy_group.add(fuzz1)
        overlay_list.append(fuzz1)
        self.play(FadeIn(fuzz1), run_time=max(0.05, 0.65))

        # ---------- beat 3: 2.94 - 4.38 ----------
        self.play(noisy_group.animate.shift(LEFT * 0.30), run_time=max(0.05, 0.36))
        p = raw_wave.point_from_proportion(0.30)
        hump1 = make_hump(p[0], p[1], width=1.8, height=0.45, sign=1, color=PURPLE)
        noisy_group.add(hump1)
        overlay_list.append(hump1)
        self.play(FadeIn(hump1), run_time=max(0.05, 0.36))

        self.play(noisy_group.animate.shift(LEFT * 0.30), run_time=max(0.05, 0.36))
        p = raw_wave.point_from_proportion(0.55)
        hump2 = make_hump(p[0], p[1], width=1.8, height=0.45, sign=-1, color=PURPLE)
        noisy_group.add(hump2)
        overlay_list.append(hump2)
        self.play(FadeIn(hump2), run_time=max(0.05, 0.36))

        # ---------- beat 4: 4.38 - 5.80 ----------
        self.play(noisy_group.animate.shift(LEFT * 0.30), run_time=max(0.05, 0.35))
        p = raw_wave.point_from_proportion(0.35)
        burst1 = make_jagged(p[0], p[1], width=1.2, height=0.10, color=RED, freq1=12, freq2=19)
        noisy_group.add(burst1)
        overlay_list.append(burst1)
        self.play(FadeIn(burst1), run_time=max(0.05, 0.36))

        self.play(noisy_group.animate.shift(LEFT * 0.30), run_time=max(0.05, 0.35))
        p = raw_wave.point_from_proportion(0.65)
        burst2 = make_jagged(p[0], p[1], width=1.2, height=0.10, color=RED, freq1=12, freq2=19)
        noisy_group.add(burst2)
        overlay_list.append(burst2)
        self.play(FadeIn(burst2), run_time=max(0.05, 0.36))

        # ---------- beat 5: 5.80 - 7.88 ----------
        self.play(noisy_group.animate.shift(LEFT * 0.15), run_time=max(0.05, 0.20))

        p = raw_wave.point_from_proportion(0.48)
        wiggle = make_jagged(p[0], p[1], width=0.7, height=0.08, color=ORANGE, freq1=9, freq2=15)
        jump = make_jump(p[0] + 0.55, p[1] - 0.05, step=0.18, color=ORANGE)
        noisy_group.add(wiggle, jump)
        overlay_list.extend([wiggle, jump])

        self.play(FadeIn(wiggle), FadeIn(jump), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 1.43))

        # ---------- beat 6: 7.88 - 10.10 ----------
        filter_block = RoundedRectangle(
            width=1.9, height=1.2, corner_radius=0.15,
            fill_color=BLUE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2
        )
        filter_label = Text("Filtering", font_size=22, color=WHITE)
        filter_group = VGroup(filter_block, filter_label).move_to(RIGHT * 1.2 + UP * 1.6)
        filter_label.move_to(filter_block.get_center())

        self.play(
            noisy_group.animate.scale(0.48).move_to(LEFT * 5.6 + UP * 1.6),
            FadeIn(filter_group),
            run_time=max(0.05, 1.42),
        )

        arrow_in = Arrow(
            noisy_group.get_right() + RIGHT * 0.08,
            filter_block.get_left() + LEFT * 0.05,
            color=GREY_B, stroke_width=2, buff=0.05,
        )
        self.play(Create(arrow_in), run_time=max(0.05, 0.80))

        # ---------- beat 7: 10.10 - 14.28 ----------
        clean_wave = make_trace(clean_right_func, -1.5, 1.5, y_scale=0.35, color=GREEN, stroke_width=3.0)
        clean_wave.move_to(RIGHT * 4.6 + UP * 1.6)
        clean_label = Text("Clean EEG", font_size=18, color=GREEN).next_to(clean_wave, DOWN, buff=0.2)

        arrow_out = Arrow(
            filter_block.get_right() + RIGHT * 0.05,
            clean_wave.get_left(),
            color=GREY_B, stroke_width=2, buff=0.05,
        )

        self.play(
            Create(arrow_out),
            FadeIn(clean_wave),
            FadeIn(clean_label),
            noisy_group.animate.set_opacity(0.85),
            run_time=max(0.05, 2.00),
        )
        self.wait(max(0.05, 2.18))

        # ---------- beat 8: 14.28 - 16.34 ----------
        self.wait(max(0.05, 2.06))

        # ---------- beat 9: 16.34 - 19.60 ----------
        self.play(filter_group.animate.scale(1.08), run_time=max(0.05, 0.60))
        self.play(filter_group.animate.scale(1 / 1.08), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 2.06))

        # ---------- beat 10: 19.60 - 25.50 ----------
        clean_left_wave = make_trace(clean_base_func, -14, 14, y_scale=0.4, color=TEAL, stroke_width=3.5)
        clean_left_wave.scale(0.48).move_to(noisy_group.get_center()).set_opacity(0)
        self.add(clean_left_wave)

        self.play(noisy_group.animate.set_opacity(0.55), run_time=max(0.05, 0.70))
        for ov in overlay_list:
            self.play(FadeOut(ov), run_time=max(0.05, 0.36))
        self.play(
            FadeOut(raw_wave),
            FadeIn(clean_left_wave),
            clean_wave.animate.set_opacity(1),
            run_time=max(0.05, 1.30),
        )
        self.wait(max(0.05, 1.38))

        # ---------- beat 11: 25.50 - 30.20 ----------
        td_panel_bg = Rectangle(
            width=4.4, height=1.5, fill_color=BLACK, fill_opacity=0.55,
            stroke_color=TEAL, stroke_width=2
        ).move_to(LEFT * 2.4 + DOWN * 0.5)

        td_label = Text("Time-Domain Analysis", font_size=17, color=WHITE)
        td_label.move_to(td_panel_bg.get_top() + DOWN * 0.3)

        td_trace = make_trace(td_func, -2.0, 2.0, y_scale=0.35, color=YELLOW, stroke_width=3.0)
        td_trace.move_to(td_panel_bg.get_center() + DOWN * 0.12)

        spike_pos = np.array([td_trace.get_center()[0] - 0.8, td_trace.get_center()[1], 0])
        sharp_pos = np.array([td_trace.get_center()[0] + 0.45, td_trace.get_center()[1], 0])
        highlight_box = Rectangle(width=2.3, height=1.0, color=YELLOW, stroke_width=2, fill_opacity=0)
        highlight_box.move_to(spike_pos)

        self.play(
            FadeIn(td_panel_bg), FadeIn(td_label),
            Create(td_trace), Create(highlight_box),
            run_time=max(0.05, 2.20),
        )
        self.play(Indicate(highlight_box, scale_factor=1.08, color=YELLOW), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 1.30))

        # ---------- beat 12: 30.20 - 34.62 ----------
        self.play(
            highlight_box.animate.move_to(spike_pos),
            td_panel_bg.animate.set_stroke(color=YELLOW, width=4),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 0.30))
        self.play(
            highlight_box.animate.move_to(sharp_pos),
            td_panel_bg.animate.set_stroke(color=TEAL, width=2),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 0.30))
        self.play(
            highlight_box.animate.move_to(spike_pos),
            td_panel_bg.animate.set_stroke(color=YELLOW, width=4),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 0.52))

        # ---------- beat 13: 34.62 - 36.54 ----------
        n_rows, n_cols = 6, 10
        cell_size = 0.260
        spec_cells = []
        for _r in range(n_rows):
            row = []
            for _c in range(n_cols):
                sq = Square(
                    side_length=cell_size, fill_color=BLUE, fill_opacity=0.18,
                    stroke_color=GREY_B, stroke_width=1.0
                )
                row.append(sq)
            spec_cells.append(row)

        all_spec_cells = VGroup(*[spec_cells[r][c] for r in range(n_rows) for c in range(n_cols)])
        all_spec_cells.arrange_in_grid(rows=n_rows, cols=n_cols, buff=0.045)

        spec_panel_bg = Rectangle(
            width=4.4, height=2.1, fill_color=BLACK, fill_opacity=0.55,
            stroke_color=BLUE, stroke_width=2
        ).move_to(LEFT * 2.4 + DOWN * 2.25)

        spec_label = Text("Time-Frequency Analysis", font_size=16, color=WHITE)
        spec_label.move_to(spec_panel_bg.get_top() + DOWN * 0.28)

        all_spec_cells.move_to(spec_panel_bg.get_center() + DOWN * 0.25)

        freq_axis = Text("Freq ↑", font_size=11, color=GREY_B).rotate(PI / 2)
        freq_axis.next_to(all_spec_cells, LEFT, buff=0.12)
        time_axis = Text("Time →", font_size=11, color=GREY_B)
        time_axis.next_to(all_spec_cells, DOWN, buff=0.08)

        spectro_group = VGroup(spec_panel_bg, spec_label, all_spec_cells, freq_axis, time_axis)

        self.play(
            td_panel_bg.animate.set_opacity(0.7),
            td_label.animate.set_opacity(0.7),
            td_trace.animate.set_opacity(0.7),
            highlight_box.animate.set_opacity(0.7),
            FadeIn(spectro_group),
            run_time=max(0.05, 1.92),
        )

        # ---------- beat 14: 36.54 - 44.28 ----------
        low_cells = [spec_cells[r][c] for r in [0, 1] for c in range(n_cols)]
        mid_cells = [spec_cells[r][c] for r in [2, 3, 4] for c in range(n_cols)]
        high_cells = [spec_cells[r][c] for r in [5] for c in range(n_cols)]

        self.play(*[cell.animate.set_fill(color=TEAL, opacity=0.75) for cell in low_cells], run_time=max(0.05, 2.24))
        self.play(*[cell.animate.set_fill(color=GREEN, opacity=0.8) for cell in mid_cells], run_time=max(0.05, 2.80))
        self.play(*[cell.animate.set_fill(color=YELLOW, opacity=0.95) for cell in low_cells], run_time=max(0.05, 1.20))
        self.play(*[cell.animate.set_fill(color=GREEN, opacity=0.55) for cell in high_cells], run_time=max(0.05, 1.50))

        # ---------- beat 15: 44.28 - 47.24 ----------
        intensity = np.exp(-((np.arange(n_cols) - 4.5) ** 2) / (2 * 1.7 ** 2))
        mountain_anims = []
        for r in range(n_rows):
            for c in range(n_cols):
                val = intensity[c]
                if val > 0.7:
                    col, op = YELLOW, 0.95
                elif val > 0.4:
                    col, op = GREEN, 0.8
                elif val > 0.2:
                    col, op = TEAL, 0.6
                else:
                    col, op = BLUE, 0.2
                mountain_anims.append(spec_cells[r][c].animate.set_fill(color=col, opacity=op))
        self.play(*mountain_anims, run_time=max(0.05, 2.96))

        # ---------- beat 16: 47.24 - 52.46 ----------
        mountain_cells = VGroup(*[
            spec_cells[r][c]
            for r in range(n_rows)
            for c in range(n_cols)
            if intensity[c] > 0.4
        ])

        seizure_label = Text("Seizure", font_size=16, color=RED)
        seizure_label.next_to(all_spec_cells, UP, buff=0.15).shift(RIGHT * 0.7)

        self.play(FadeIn(seizure_label), run_time=max(0.05, 0.50))
        for _ in range(5):
            self.play(mountain_cells.animate.set_fill(color=YELLOW, opacity=1.0), run_time=max(0.05, 0.47))
            self.play(mountain_cells.animate.set_fill(color=ORANGE, opacity=0.9), run_time=max(0.05, 0.47))
        self.wait(max(0.05, 0.02))

        # ---------- beat 17: 52.46 - 54.90 ----------
        auto_block = RoundedRectangle(
            width=2.9, height=2.4, corner_radius=0.12,
            fill_color=BLACK, fill_opacity=0.75, stroke_color=PURPLE, stroke_width=2
        ).move_to(RIGHT * 5.0 + DOWN * 0.75)

        auto_label = Text("Automated Detection", font_size=15, color=WHITE)
        auto_label.move_to(auto_block.get_top() + DOWN * 0.3)

        input_sq = Square(side_length=0.5, fill_color=BLUE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
        proc_sq = Square(side_length=0.5, fill_color=ORANGE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
        output_sq = Square(side_length=0.5, fill_color=GREEN, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)

        flow_squares = VGroup(input_sq, proc_sq, output_sq).arrange(RIGHT, buff=0.22).move_to(
            auto_block.get_center() + DOWN * 0.15
        )

        flow_arrow1 = Arrow(
            input_sq.get_right() + RIGHT * 0.05,
            proc_sq.get_left() + LEFT * 0.05,
            color=GREY_B, stroke_width=1.5, buff=0.04,
            max_tip_length_to_length_ratio=0.3,
        )
        flow_arrow2 = Arrow(
            proc_sq.get_right() + RIGHT * 0.05,
            output_sq.get_left() + LEFT * 0.05,
            color=GREY_B, stroke_width=1.5, buff=0.04,
            max_tip_length_to_length_ratio=0.3,
        )

        ml_label = Text("ML Algorithm", font_size=12, color=YELLOW).next_to(proc_sq, DOWN, buff=0.10)
        indicator_dot = Dot(radius=0.06, color=RED, fill_opacity=1).move_to(
            proc_sq.get_top() + RIGHT * 0.06 + UP * 0.08
        )
        auto_group = VGroup(
            auto_block, auto_label, flow_squares, flow_arrow1, flow_arrow2, ml_label, indicator_dot
        )

        arrow_td = Arrow(
            td_panel_bg.get_right() + RIGHT * 0.2,
            auto_block.get_left() + UP * 0.25,
            color=GREY_B, stroke_width=2, buff=0.08,
        )
        arrow_spec = Arrow(
            spec_panel_bg.get_right() + RIGHT * 0.2,
            auto_block.get_left() + DOWN * 0.25,
            color=GREY_B, stroke_width=2, buff=0.08,
        )

        self.play(
            spectro_group.animate.set_opacity(0.65),
            td_panel_bg.animate.set_opacity(0.5),
            td_label.animate.set_opacity(0.5),
            td_trace.animate.set_opacity(0.5),
            highlight_box.animate.set_opacity(0.5),
            FadeIn(auto_group),
            Create(arrow_td),
            Create(arrow_spec),
            run_time=max(0.05, 2.44),
        )

        # ---------- beat 18: 54.90 - 64.24 ----------
        self.play(indicator_dot.animate.scale(2.0), run_time=max(0.05, 0.5))
        self.play(indicator_dot.animate.scale(0.5), run_time=max(0.05, 0.5))
        self.play(indicator_dot.animate.scale(2.0), run_time=max(0.05, 0.5))
        self.play(indicator_dot.animate.scale(0.5), run_time=max(0.05, 0.5))

        alert_bg = RoundedRectangle(
            width=2.5, height=0.5, corner_radius=0.10,
            fill_color=ORANGE, fill_opacity=0.9, stroke_color=YELLOW, stroke_width=2
        )
        alert_text = Text("Automatic Detection Alert", font_size=12, color=BLACK)
        alert_notification = VGroup(alert_bg, alert_text).next_to(clean_wave, UP, buff=0.7)

        self.play(FadeIn(alert_notification), run_time=max(0.05, 1.2))
        self.play(alert_notification.animate.scale(1.05), run_time=max(0.05, 0.6))
        self.play(alert_notification.animate.scale(1 / 1.05), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 4.94))

        # ---------- beat 19: 64.24 - 68.50 ----------
        note_bg = RoundedRectangle(
            width=2.9, height=0.45, corner_radius=0.08,
            fill_color=BLACK, fill_opacity=0.6, stroke_color=GREEN, stroke_width=1.5
        )
        note_text = Text("Complements expert interpretation", font_size=12, color=WHITE)
        note_tag = VGroup(note_bg, note_text).next_to(alert_notification, DOWN, buff=0.15)

        self.play(
            alert_notification.animate.set_opacity(0.75),
            FadeIn(note_tag),
            run_time=max(0.05, 2.00),
        )
        self.wait(max(0.05, 2.26))

        # ---------- beat 20: 68.50 - 72.53 ----------
        self.play(note_tag.animate.set_opacity(1), run_time=max(0.05, 0.40))
        self.play(note_tag.animate.scale(1.04), run_time=max(0.05, 0.60))
        self.play(note_tag.animate.scale(1 / 1.04), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 2.43))