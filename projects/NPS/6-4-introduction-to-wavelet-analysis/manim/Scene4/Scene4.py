ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Helper functions -- same waveform/wavelet style as previous scene.
        # ----------------------------------------------------------------
        SIGNAL_LEFT_X = -5.8
        SIGNAL_RIGHT_X = -0.2
        SIGNAL_CY = 0.0
        SIGNAL_AMP = 0.55
        SIGNAL_WIDTH = SIGNAL_RIGHT_X - SIGNAL_LEFT_X
        SLOW_T = 0.22
        SPIKE_T = 0.82

        def signal_y(t):
            slow_env = 1 / (1 + np.exp((t - 0.55) * 15))
            slow = 0.85 * np.sin(2 * np.pi * 1.5 * t) * slow_env
            spike = 1.15 * np.exp(-(((t - 0.82) / 0.015) ** 2))
            return slow + spike

        def make_signal_waveform(x_left, x_right, center_y=SIGNAL_CY, amp=SIGNAL_AMP):
            width = x_right - x_left

            def func(t):
                x = x_left + width * t
                y = center_y + amp * signal_y(t)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                func,
                t_range=[0, 1, 0.002],
                color=WHITE,
                stroke_width=2.5,
            )

        def make_wavelet(center_x, center_y, x_scale=1.0, color=WHITE,
                         stroke_width=3.5, amp=0.65):
            base_half_extent = 1.05
            cycles = 2.8

            def func(t):
                x = center_x + t * x_scale * base_half_extent
                env = np.exp(-(t ** 2) / (2 * 0.34 ** 2))
                y = center_y + amp * env * np.sin(2 * np.pi * cycles * t)
                return np.array([x, y, 0.0])

            return ParametricFunction(
                func,
                t_range=[-1, 1, 0.004],
                color=color,
                stroke_width=stroke_width,
            )

        # ----------------------------------------------------------------
        # Initial split-screen state carried over from Scene 3.
        # ----------------------------------------------------------------
        left_signal = make_signal_waveform(-5.8, -0.2)
        right_signal = make_signal_waveform(0.2, 5.8)

        left_window2 = Rectangle(
            width=1.3, height=1.7,
            stroke_color=GOLD, stroke_width=3, fill_opacity=0,
        ).move_to([-1.8, SIGNAL_CY, 0])

        right_wavelets = VGroup(
            make_wavelet(0.9, SIGNAL_CY, x_scale=1.0, color=ORANGE),
            make_wavelet(2.2, SIGNAL_CY, x_scale=0.85, color=ORANGE),
            make_wavelet(3.1, SIGNAL_CY, x_scale=0.55, color=TEAL),
            make_wavelet(4.4, SIGNAL_CY, x_scale=0.20, color=YELLOW),
            make_wavelet(5.5, SIGNAL_CY, x_scale=0.16, color=YELLOW),
        )

        left_half = VGroup(left_signal, left_window2)
        right_half = VGroup(right_signal, right_wavelets)

        vert_line = Line([0, -3.0, 0], [0, 3.0, 0],
                         color=GREY, stroke_width=2)

        header = Text("Direct Comparison", font_size=36, color=GOLD)
        header.move_to([0, 3.0, 0])

        self.add(left_half, right_half, vert_line, header)

        # ----------------------------------------------------------------
        # Beat 1: 0.00-3.40 -- slide halves apart, table fades in, header changes.
        # ----------------------------------------------------------------
        self.play(
            left_half.animate.shift(LEFT * 1.0 + UP * 0.5),
            right_half.animate.shift(RIGHT * 1.0 + UP * 0.5),
            FadeOut(vert_line),
            run_time=max(0.05, 1.20),
        )

        # Build empty comparison table.
        left_col = Rectangle(
            width=0.95, height=3.0,
            stroke_color=GREY_B, stroke_width=1.5,
            fill_color=BLACK, fill_opacity=0.65,
        )
        right_col = Rectangle(
            width=0.95, height=3.0,
            stroke_color=GREY_B, stroke_width=1.5,
            fill_color=BLACK, fill_opacity=0.65,
        )
        table_rects = VGroup(left_col, right_col).arrange(RIGHT, buff=0.2)
        table_rects.move_to([0, 0.85, 0])

        left_header_text = Text("STFT", font_size=20, color=WHITE)
        right_header_text = Text("Wavelet Analysis", font_size=15, color=WHITE)
        right_header_text.scale_to_fit_width(0.75)

        left_header_text.move_to(left_col.get_top() + DOWN * 0.35)
        right_header_text.move_to(right_col.get_top() + DOWN * 0.35)

        table = VGroup(left_col, right_col, left_header_text, right_header_text)
        self.play(FadeIn(table), run_time=max(0.05, 0.90))

        summary_text = Text("Summary", font_size=22, color=GOLD)
        summary_text.move_to([0, -1.05, 0])
        self.play(Transform(header, summary_text), run_time=max(0.05, 1.0))

        self.wait(max(0.05, 0.30))

        # ----------------------------------------------------------------
        # Beat 2: 4.22-5.98 -- fixed rectangle in left column + labels.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.82))

        mini_rect = Rectangle(
            width=0.30, height=0.42,
            stroke_color=GOLD, stroke_width=2, fill_opacity=0,
        )
        mini_rect.move_to(left_col.get_center() + UP * 0.45)

        fixed_window_text = Text("fixed window", font_size=14, color=WHITE)
        uniform_res_text = Text("uniform resolution", font_size=14, color=WHITE)
        left_text_group = VGroup(fixed_window_text, uniform_res_text).arrange(DOWN, buff=0.10)
        left_text_group.scale_to_fit_width(0.80)
        left_text_group.move_to(left_col.get_center() + DOWN * 0.30)

        self.play(FadeIn(mini_rect), FadeIn(left_text_group), run_time=max(0.05, 1.00))
        self.play(left_col.animate.set_stroke(color=GOLD, width=3.0),
                  run_time=max(0.05, 0.76))

        # ----------------------------------------------------------------
        # Beat 3: 6.62-10.68 -- multiple wavelets in right column + sentence.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.64))

        right_col_cx = right_col.get_center()[0]
        row_centers = [1.60, 1.10, 0.60, 0.10, -0.35]

        right_wavelet_group = VGroup(
            make_wavelet(right_col_cx, row_centers[0], x_scale=0.42, color=ORANGE, stroke_width=2.0, amp=0.25),
            make_wavelet(right_col_cx, row_centers[1], x_scale=0.38, color=ORANGE, stroke_width=2.0, amp=0.25),
            make_wavelet(right_col_cx, row_centers[2], x_scale=0.28, color=TEAL, stroke_width=2.0, amp=0.25),
            make_wavelet(right_col_cx, row_centers[3], x_scale=0.17, color=YELLOW, stroke_width=2.0, amp=0.25),
            make_wavelet(right_col_cx, row_centers[4], x_scale=0.12, color=YELLOW, stroke_width=2.0, amp=0.25),
        )

        variable_window_text = Text("variable window sizes", font_size=14, color=WHITE)
        multi_res_text = Text("multi-resolution", font_size=14, color=WHITE)
        right_text_group = VGroup(variable_window_text, multi_res_text).arrange(DOWN, buff=0.10)
        right_text_group.scale_to_fit_width(0.80)
        right_text_group.move_to([right_col_cx, -0.75, 0])

        self.play(FadeIn(right_wavelet_group), run_time=max(0.05, 1.20))
        self.play(FadeIn(right_text_group), run_time=max(0.05, 0.70))
        self.play(right_col.animate.set_stroke(color=GOLD, width=3.0),
                  run_time=max(0.05, 0.60))

        # Sentence below table: "Wavelet analysis extends the STFT"
        sentence_left = Text("Wavelet analysis", font_size=20, color=WHITE)
        extends_word = Text("extends", font_size=20, color=YELLOW)
        sentence_right = Text(" the STFT", font_size=20, color=WHITE)
        sentence_group = VGroup(sentence_left, extends_word, sentence_right).arrange(RIGHT, buff=0.12)
        sentence_group.move_to([0, -1.55, 0])

        self.play(FadeIn(sentence_group), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.76))

        # ----------------------------------------------------------------
        # Beat 4: 11.80-18.16 -- pulse extends, equal signs, both remain valuable.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 1.12))

        # Pulse extends softly.
        for _ in range(2):
            self.play(extends_word.animate.scale(1.08, about_point=extends_word.get_center()),
                      run_time=max(0.05, 0.30))
            self.play(extends_word.animate.scale(1 / 1.08, about_point=extends_word.get_center()),
                      run_time=max(0.05, 0.30))

        # Equal-sign groups with checkmarks.
        check1 = Text("✓", font_size=22, color=GREEN)
        eq1_group = VGroup(
            Text("=", font_size=28, color=WHITE),
            Text("STFT", font_size=16, color=WHITE),
            check1,
        ).arrange(RIGHT, buff=0.12)

        check2 = Text("✓", font_size=22, color=GREEN)
        eq2_group = VGroup(
            Text("=", font_size=28, color=WHITE),
            Text("Wavelet Analysis", font_size=15, color=WHITE),
            check2,
        ).arrange(RIGHT, buff=0.12)

        equal_signs_row = VGroup(eq1_group, eq2_group).arrange(RIGHT, buff=0.8)
        equal_signs_row.scale_to_fit_width(5.5)
        equal_signs_row.move_to([0, -2.5, 0])

        self.play(FadeIn(equal_signs_row), run_time=max(0.05, 1.00))

        both_valuable_label = Text("Both remain valuable", font_size=16, color=WHITE)
        both_valuable_label.move_to([0, -2.95, 0])
        self.play(FadeIn(both_valuable_label), run_time=max(0.05, 0.70))

        # Pulse checkmarks gently while "valuable" is said.
        checkmarks = VGroup(check1, check2)
        for _ in range(2):
            self.play(checkmarks.animate.scale(1.2, about_point=checkmarks.get_center()),
                      run_time=max(0.05, 0.30))
            self.play(checkmarks.animate.scale(1 / 1.2, about_point=checkmarks.get_center()),
                      run_time=max(0.05, 0.30))

        choice_line1 = Text(
            "Choice depends on data characteristics and study objectives",
            font_size=16, color=WHITE
        )
        choice_line1.scale_to_fit_width(6.5)
        choice_line1.move_to([0, -3.35, 0])
        self.play(FadeIn(choice_line1), run_time=max(0.05, 1.00))

        self.wait(max(0.05, 1.26))

        # ----------------------------------------------------------------
        # Beat 5: 18.88-23.68 -- dims/brightens extends, ghost "replaces", caption.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.72))

        # Dim extends temporarily.
        self.play(extends_word.animate.set_color(GREY), run_time=max(0.05, 0.40))

        # Ghosted 'replaces' with strike-through above extends.
        ghost_word = Text("replaces", font_size=16, color=RED, fill_opacity=0.4)
        ghost_word.move_to(np.array([
            extends_word.get_center()[0],
            extends_word.get_top()[1] + 0.25,
            0.0,
        ]))
        strike_line = Line(
            ghost_word.get_left() + DOWN * 0.05,
            ghost_word.get_right() + DOWN * 0.05,
            color=RED, stroke_width=2.5,
        )
        ghost_group = VGroup(ghost_word, strike_line)

        self.play(FadeIn(ghost_group), run_time=max(0.05, 0.80))
        self.play(FadeOut(ghost_group), run_time=max(0.05, 0.40))

        # Brighten extends back.
        self.play(extends_word.animate.set_color(YELLOW), run_time=max(0.05, 0.40))

        # Caption below first sentence.
        caption_before = Text("Wavelet analysis is ", font_size=16, color=WHITE)
        notsimply_word = Text("not simply", font_size=16, color=GREY)
        caption_after = Text(" a better version of the STFT", font_size=16, color=WHITE)
        caption_group = VGroup(caption_before, notsimply_word, caption_after).arrange(RIGHT, buff=0.1)
        caption_group.scale_to_fit_width(6.5)
        caption_group.move_to([0, -2.1, 0])

        self.play(FadeIn(caption_group), run_time=max(0.05, 1.00))

        # Brighten "not simply".
        self.play(notsimply_word.animate.set_color(YELLOW), run_time=max(0.05, 0.80))

        self.wait(max(0.05, 1.00))

        # ----------------------------------------------------------------
        # Beat 6: 24.28-31.90 -- column highlights, final line, brighten, hold.
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.60))

        # Left column highlight.
        self.play(left_col.animate.set_stroke(color=YELLOW, width=3.5),
                  run_time=max(0.05, 1.00))
        self.play(left_col.animate.set_stroke(color=GREY_B, width=1.5),
                  run_time=max(0.05, 0.80))

        # Right column highlight.
        self.play(right_col.animate.set_stroke(color=YELLOW, width=3.5),
                  run_time=max(0.05, 1.00))
        self.play(right_col.animate.set_stroke(color=GREY_B, width=1.5),
                  run_time=max(0.05, 0.80))

        # Settle both at equal brightness.
        self.play(
            left_col.animate.set_stroke(color=GREY_B, width=2.0),
            right_col.animate.set_stroke(color=GREY_B, width=2.0),
            run_time=max(0.05, 0.60),
        )

        # Final line replaces earlier choice line.
        choice_final_before = Text(
            "Choice depends on the neural signal and the ",
            font_size=16, color=WHITE,
        )
        sci_quest_word = Text("scientific question", font_size=16, color=GREY)
        choice_final_group = VGroup(choice_final_before, sci_quest_word).arrange(RIGHT, buff=0.0)
        choice_final_group.scale_to_fit_width(6.5)
        choice_final_group.move_to([0, -3.35, 0])

        self.play(FadeOut(choice_line1), FadeIn(choice_final_group), run_time=max(0.05, 1.00))

        # Brighten "scientific question".
        self.play(sci_quest_word.animate.set_color(YELLOW), run_time=max(0.05, 0.80))

        self.wait(max(0.05, 1.62))

        # Final hold to 32.62.
        self.wait(max(0.05, 0.72))