ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene16(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_trace(signal, width=6.0, height=0.8, color=YELLOW, stroke_width=3.0, num_points=500):
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            u = np.linspace(-1, 1, num_points)
            x = u * width / 2.0
            y = signal(u) * height / 2.0
            y = np.clip(y, -height, height)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        def sleep_signal(u):
            slow = 0.55 * np.sin(2 * np.pi * 0.8 * u)
            spindle1 = 0.28 * np.sin(2 * np.pi * 12 * u) * np.exp(-((u + 0.45) / 0.12) ** 2)
            spindle2 = 0.28 * np.sin(2 * np.pi * 12 * u) * np.exp(-((u - 0.5) / 0.12) ** 2)
            return slow + spindle1 + spindle2

        def wake_signal(u):
            return 0.16 * np.sin(2 * np.pi * 18 * u) + 0.08 * np.sin(2 * np.pi * 25 * u)

        def n1_signal(u):
            return 0.35 * np.sin(2 * np.pi * 4.5 * u + 1.2 * np.sin(2 * np.pi * 1.5 * u)) + 0.15 * np.sin(2 * np.pi * 9 * u)

        def n2_signal(u):
            y = 0.28 * np.sin(2 * np.pi * 13 * u) * np.exp(-((u + 0.35) / 0.08) ** 2)
            y += 0.28 * np.sin(2 * np.pi * 13 * u) * np.exp(-((u - 0.35) / 0.08) ** 2)
            y += 0.45 * np.exp(-((u + 0.55) / 0.25) ** 2) * np.sin(2 * np.pi * 1.2 * (u + 0.55))
            return y

        def n3_signal(u):
            return 0.8 * np.sin(2 * np.pi * 0.8 * u)

        def rem_signal(u):
            saw = 2 * ((u * 3) - np.floor(u * 3 + 0.5))
            return 0.3 * saw + 0.15 * np.sin(2 * np.pi * 16 * u)

        def spike_signal(u):
            y = 0.22 * np.sin(2 * np.pi * 2.0 * u) + 0.08 * np.sin(2 * np.pi * 7.0 * u)
            for u0, amp, w in [(-0.55, 2.1, 0.03), (0.05, 2.4, 0.025), (0.65, 2.0, 0.035)]:
                y += amp * np.exp(-((u - u0) / w) ** 2)
                y += 0.25 * np.sin(2 * np.pi * 35 * u) * np.exp(-((u - u0) / 0.1) ** 2)
            return y

        def make_prev_composition():
            panel_positions = [
                LEFT * 3.1 + UP * 1.6,
                RIGHT * 3.1 + UP * 1.6,
                LEFT * 3.1 + DOWN * 0.9,
                RIGHT * 3.1 + DOWN * 0.9,
            ]
            panels = VGroup(*[
                RoundedRectangle(
                    width=2.6, height=1.4, corner_radius=0.12,
                    fill_color=BLACK, fill_opacity=0.5,
                    stroke_color=BLUE, stroke_width=1
                ).move_to(pos)
                for pos in panel_positions
            ])
            trace = make_trace(sleep_signal, width=6.0, height=0.45, color=YELLOW, stroke_width=2).move_to(ORIGIN).shift(DOWN * 1.2)
            bars = VGroup(*[
                Rectangle(
                    width=0.18, height=h,
                    fill_color=color, fill_opacity=0.8, stroke_width=0
                ).move_to(np.array([x, -2.6 + h / 2.0, 0]))
                for x, h, color in [
                    (-2.0, 0.8, BLUE), (-1.2, 1.3, PURPLE), (-0.4, 1.0, TEAL),
                    (0.4, 0.7, GREEN), (1.2, 0.5, ORANGE)
                ]
            ])
            return VGroup(panels, trace, bars)

        # dark backdrop for the later tone shift
        bg_rect = Rectangle(
            width=16, height=9,
            fill_color="#0A0C10", fill_opacity=0.0,
            stroke_width=0
        ).move_to(ORIGIN)
        bg_rect.set_z_index(-5)
        self.add(bg_rect)

        # ---------- beat 1: previous scene fades out ----------
        prev_comp = make_prev_composition()
        self.add(prev_comp)
        self.play(FadeOut(prev_comp), run_time=max(0.05, 1.2))

        # ---------- beat 2: sleep staging waveform ----------
        sleep_wave = make_trace(sleep_signal, width=8.0, height=0.75, color=YELLOW, stroke_width=3).move_to(ORIGIN)
        sleep_label = Text("Sleep Staging", font_size=34, color=WHITE, weight="BOLD")
        sleep_hl = SurroundingRectangle(
            sleep_label, color=BLUE, buff=0.18, stroke_width=2,
            fill_color=BLUE, fill_opacity=0.15
        )
        sleep_label_group = VGroup(sleep_hl, sleep_label).move_to(DOWN * 1.9)

        self.play(FadeIn(sleep_wave), run_time=max(0.05, 1.0))
        self.play(GrowFromCenter(sleep_label_group), run_time=max(0.05, 0.8))
        self.play(sleep_wave.animate.shift(LEFT * 0.9), run_time=max(0.05, 2.88), rate_func=linear)

        self.wait(max(0.05, 0.76))  # 5.88 -> 6.64

        # ---------- beat 3: sleep stages reference set ----------
        self.play(
            sleep_wave.animate.scale(0.6).move_to(UP * 2.35),
            sleep_label_group.animate.scale(0.7).move_to(UP * 1.55),
            run_time=max(0.05, 1.4
        ))

        stage_names = ["Wake", "N1", "N2", "N3", "REM"]
        stage_signals = [wake_signal, n1_signal, n2_signal, n3_signal, rem_signal]
        mini_groups_list = []
        for name, sig in zip(stage_names, stage_signals):
            trace = make_trace(sig, width=1.6, height=0.55, color=YELLOW, stroke_width=2.5)
            label = Text(name, font_size=18, color=WHITE)
            mini = VGroup(trace, label).arrange(DOWN, buff=0.12)
            mini_groups_list.append(mini)

        mini_group = VGroup(*mini_groups_list).arrange(RIGHT, buff=0.5)
        mini_group.scale_to_fit_width(12.5)
        mini_group.move_to(DOWN * 0.2)

        per_item3 = 5.34 / 5.0
        for mini in mini_groups_list:
            self.play(FadeIn(mini), run_time=max(0.05, per_item3 * 0.55))
            self.wait(max(0.05, per_item3 * 0.45))

        # ---------- beat 4: signal processing blocks ----------
        def build_filter_icon():
            rect = Rectangle(
                width=1.4, height=0.65,
                color=GREY_B, fill_color=GREY_B, fill_opacity=0.3,
                stroke_color=WHITE, stroke_width=1
            )
            noise_lines = VGroup(*[
                Line(
                    rect.get_bottom() + np.array([x, 0.05, 0]),
                    rect.get_top() + np.array([x, -0.05, 0]),
                    color=GREY, stroke_width=1.5
                )
                for x in [-0.55, -0.27, 0.0, 0.27, 0.55]
            ])
            diag = Line(
                rect.get_corner(DL) + LEFT * 0.1 + UP * 0.1,
                rect.get_corner(UR) + RIGHT * 0.1 + DOWN * 0.1,
                color=YELLOW, stroke_width=5
            )
            return VGroup(rect, noise_lines, diag)

        def build_spectrum_icon():
            axis = Line(LEFT * 0.7, RIGHT * 0.7, color=WHITE, stroke_width=2)
            bars = VGroup(*[
                Rectangle(
                    width=0.14, height=h,
                    fill_color=color, fill_opacity=1, stroke_width=0
                ).move_to(axis.get_start() + np.array([x, h / 2.0, 0]))
                for x, h, color in [
                    (-0.5, 0.4, BLUE), (-0.25, 0.7, PURPLE),
                    (0.0, 0.5, TEAL), (0.25, 0.65, GREEN), (0.5, 0.45, ORANGE)
                ]
            ])
            return VGroup(axis, bars)

        def build_spectrogram_icon():
            rows, cols = 4, 6
            cells = VGroup(*[
                Square(side_length=0.18, fill_color=BLACK, fill_opacity=1, stroke_width=0.5)
                for _ in range(rows * cols)
            ])
            cells.arrange_in_grid(rows=rows, cols=cols, buff=0.02)
            for r in range(rows):
                for c in range(cols):
                    val = 0.3 + 0.7 * (c / (cols - 1)) * (1 - r / rows)
                    if val < 0.3:
                        col = BLACK
                    elif val < 0.5:
                        col = MAROON
                    elif val < 0.7:
                        col = RED
                    else:
                        col = YELLOW
                    cells[r * cols + c].set_fill(col, opacity=1)
            xlabel = Text("t →", font_size=12, color=GREY).next_to(cells, DOWN, buff=0.05)
            ylabel = Text("f ↑", font_size=12, color=GREY).next_to(cells, LEFT, buff=0.05).rotate(PI / 2)
            return VGroup(cells, xlabel, ylabel)

        def make_signal_block(icon, label_text, width=3.2, height=1.35):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.15,
                fill_color=BLUE, fill_opacity=0.25,
                stroke_color=BLUE, stroke_width=1
            )
            icon.scale_to_fit_height(0.55)
            txt = Text(label_text, font_size=15, color=WHITE, weight="BOLD")
            content = VGroup(icon, txt).arrange(DOWN, buff=0.1).move_to(rect)
            return VGroup(rect, content)

        block_filter = make_signal_block(build_filter_icon(), "Filtering")
        block_spectrum = make_signal_block(build_spectrum_icon(), "Spectral Analysis")
        block_spectrogram = make_signal_block(build_spectrogram_icon(), "Spectrogram Analysis")
        blocks = [block_filter, block_spectrum, block_spectrogram]
        blocks_group = VGroup(*blocks).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.4)
        blocks_group.scale_to_fit_width(12.2)

        per_block = 6.44 / 3.0
        for block in blocks:
            self.play(GrowFromCenter(block), run_time=max(0.05, per_block * 0.35))
            self.play(block.animate.scale(1.08), run_time=max(0.05, per_block * 0.15))
            self.play(block.animate.scale(1 / 1.08), run_time=max(0.05, per_block * 0.15))
            self.wait(max(0.05, per_block * 0.35))

        # ---------- beat 5: identified pipeline ----------
        mini_labels = [mc[1] for mc in mini_groups_list]
        self.play(mini_group.animate.scale(1.08), run_time=max(0.05, 0.8))
        for lab in mini_labels:
            self.play(Indicate(lab, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.35))

        caption = Text(
            "Identified stages → sleep quality → diagnosis",
            font_size=24, color=WHITE, weight="BOLD"
        )
        check_circle = Circle(
            radius=0.22, fill_color=GREEN, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1
        )
        check_text = Text("✓", font_size=18, color=WHITE).move_to(check_circle.get_center())
        check_mark = VGroup(check_circle, check_text)
        caption_group = VGroup(caption, check_mark).arrange(RIGHT, buff=0.35).move_to(DOWN * 3.12)

        self.play(Write(caption), run_time=max(0.05, 1.0))
        self.play(FadeIn(check_mark), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.97))

        self.wait(max(0.05, 1.0))  # 26.84 -> 27.84

        # ---------- beat 6: sleep staging as normal function ----------
        sleep_comp = VGroup(sleep_wave, sleep_label_group, mini_group, blocks_group, caption_group)
        self.play(sleep_comp.animate.scale(0.65).shift(UP * 1.5).set_opacity(0.55), run_time=max(0.05, 1.8))

        normal_glow = SurroundingRectangle(
            mini_group, color=GREEN, buff=0.22, stroke_width=5,
            fill_color=GREEN, fill_opacity=0.05
        )
        self.play(FadeIn(normal_glow), run_time=max(0.05, 0.4))
        self.play(
            normal_glow.animate.set_stroke(width=8, opacity=0.9).set_fill(GREEN, opacity=0.12),
            run_time=max(0.05, 0.7
        ))
        self.play(
            normal_glow.animate.set_stroke(width=3, opacity=0.5).set_fill(GREEN, opacity=0.04),
            run_time=max(0.05, 0.7
        ))
        self.wait(max(0.05, 0.82))

        self.wait(max(0.05, 0.66))  # 32.26 -> 32.92

        # ---------- beat 7: however -> epilepsy transition ----------
        however = Text("However", font_size=56, color=WHITE, weight="BOLD").move_to(ORIGIN)
        self.play(FadeIn(however), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.4))
        self.play(FadeOut(however), run_time=max(0.05, 0.3))

        self.play(
            sleep_comp.animate.shift(UP * 5).set_opacity(0.05),
            bg_rect.animate.set_fill("#0A0C10", opacity=0.55),
            run_time=max(0.05, 1.47
        ))

        smooth_epilepsy_trace = make_trace(
            sleep_signal, width=7.5, height=0.75,
            color=YELLOW, stroke_width=3
        ).move_to(ORIGIN)
        self.play(FadeIn(smooth_epilepsy_trace), run_time=max(0.05, 1.85))

        self.wait(max(0.05, 0.92))  # 37.24 -> 38.16

        # ---------- beat 8: epilepsy title and anticipation ----------
        epilepsy_title = Text("Epilepsy", font_size=54, weight="BOLD", color=RED).move_to(UP * 2.25)

        def build_lightning_bolt(color=YELLOW):
            pts = [
                np.array([0.0, 0.55, 0.0]),
                np.array([0.08, 0.18, 0.0]),
                np.array([0.30, 0.22, 0.0]),
                np.array([0.02, -0.08, 0.0]),
                np.array([0.18, -0.35, 0.0]),
                np.array([-0.12, -0.08, 0.0]),
                np.array([-0.25, 0.10, 0.0]),
                np.array([-0.10, 0.28, 0.0]),
            ]
            return Polygon(*pts).set_fill(color, opacity=1).set_stroke(WHITE, width=2)

        bolt = build_lightning_bolt(YELLOW).scale_to_fit_height(0.9)
        bolt.move_to(epilepsy_title.get_top() + UP * 0.5)

        self.play(
            GrowFromCenter(bolt),
            FadeIn(epilepsy_title),
            smooth_epilepsy_trace.animate.shift(LEFT * 0.3),
            run_time=max(0.05, 1.0
        ))
        self.play(Indicate(bolt, scale_factor=1.45, color=WHITE), run_time=max(0.05, 0.8))
        self.play(smooth_epilepsy_trace.animate.shift(LEFT * 0.3), run_time=max(0.05, 3.12), rate_func=linear)

        self.wait(max(0.05, 0.64))  # 43.08 -> 43.72

        # ---------- beat 9: abnormal discharge ----------
        center = smooth_epilepsy_trace.get_center()
        jagged_epilepsy_trace = make_trace(
            spike_signal, width=7.5, height=1.0,
            color=YELLOW, stroke_width=3
        ).move_to(center)
        self.play(Transform(smooth_epilepsy_trace, jagged_epilepsy_trace), run_time=max(0.05, 0.8))

        spike_u_positions = [-0.5, 0.05, 0.6]
        spike_peak_positions = []
        for u_peak in spike_u_positions:
            pos = center + np.array([u_peak * 7.5 / 2.0, 0.85, 0.0])
            spike_peak_positions.append(pos)

        glows = VGroup(*[
            Dot(point=pos, radius=0.13, color=RED, fill_opacity=0.7, stroke_width=0).set_opacity(0.0)
            for pos in spike_peak_positions
        ])
        self.add(glows)

        for _ in range(3):
            self.play(
                glows.animate.set_opacity(0.9),
                bolt.animate.set_fill(WHITE).scale(1.25),
                run_time=max(0.05, 0.25
            ))
            self.play(
                glows.animate.set_opacity(0.1),
                bolt.animate.set_fill(YELLOW).scale(1 / 1.25),
                run_time=max(0.05, 0.25
            ))

        caption_ab = Text("Abnormal electrical discharge", font_size=28, color=RED, weight="BOLD")
        caption_ab.move_to(DOWN * 2.0).shift(LEFT * 0.6)
        self.play(Write(caption_ab), run_time=max(0.05, 0.6))

        arrow_to_spike = Arrow(
            caption_ab.get_top() + UP * 0.15,
            spike_peak_positions[1],
            color=RED, buff=0.15, stroke_width=4
        )
        self.play(Create(arrow_to_spike), run_time=max(0.05, 0.4))

        def make_eval_block(label_text):
            rect = RoundedRectangle(
                width=2.9, height=0.85, corner_radius=0.15,
                fill_color=MAROON, fill_opacity=0.3,
                stroke_color=WHITE, stroke_width=1
            )
            txt = Text(label_text, font_size=17, color=WHITE)
            txt.move_to(rect)
            return VGroup(rect, txt)

        block_eval = make_eval_block("Patient evaluation").move_to(np.array([4.6, -2.2, 0]))
        block_treat = make_eval_block("Treatment planning").move_to(np.array([4.8, -3.1, 0]))
        line_to_eval = Line(block_eval.get_left(), spike_peak_positions[1], color=GREY, stroke_width=2)
        line_to_treat = Line(block_treat.get_left(), spike_peak_positions[-1], color=GREY, stroke_width=2)

        self.play(
            FadeIn(block_eval), FadeIn(block_treat),
            Create(line_to_eval), Create(line_to_treat),
            run_time=max(0.05, 1.4
        ))
        self.wait(max(0.05, 1.48))

        # ---------- beat 10: diagnosis and monitoring ----------
        last_highlight = Circle(
            radius=0.24, color=RED, stroke_width=5,
            fill_color=RED, fill_opacity=0.25
        )
        last_highlight.move_to(spike_peak_positions[-1])
        self.play(GrowFromCenter(last_highlight), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.1))

        diag_label = Text("Diagnosis", font_size=22, color=WHITE).move_to(np.array([-1.8, -3.0, 0]))
        mon_label = Text("Monitoring", font_size=22, color=WHITE).move_to(np.array([0.5, -3.0, 0]))
        diag_line = Line(diag_label.get_top() + UP * 0.08, spike_peak_positions[1], color=GREY, stroke_width=2)
        mon_line = Line(mon_label.get_top() + UP * 0.08, spike_peak_positions[-1], color=GREY, stroke_width=2)

        self.play(
            FadeIn(diag_label), FadeIn(mon_label),
            Create(diag_line), Create(mon_line),
            run_time=max(0.05, 0.7
        ))
        self.wait(max(0.05, 0.7))
        self.play(
            FadeOut(diag_label), FadeOut(mon_label),
            FadeOut(diag_line), FadeOut(mon_line),
            run_time=max(0.05, 0.7
        ))
        self.wait(max(0.05, 3.7))