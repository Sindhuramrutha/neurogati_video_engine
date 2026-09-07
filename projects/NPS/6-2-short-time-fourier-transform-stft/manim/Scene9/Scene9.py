ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # BALANCE SCALE
        # ------------------------------------------------------------
        beam = Rectangle(
            width=7.0,
            height=0.14,
            fill_color=WHITE,
            fill_opacity=0.9,
            stroke_width=0,
        )
        beam.move_to(np.array([0, 0.25, 0]))

        pivot = Polygon(
            np.array([-0.4, -0.55, 0]),
            np.array([0.4, -0.55, 0]),
            np.array([0, 0.18, 0]),
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        )

        left_string = Line(
            np.array([-3.4, 0.18, 0]),
            np.array([-3.4, -0.72, 0]),
            color=GREY_B,
            stroke_width=4,
        )
        right_string = Line(
            np.array([3.4, 0.18, 0]),
            np.array([3.4, -0.72, 0]),
            color=GREY_B,
            stroke_width=4,
        )

        left_pan = Rectangle(
            width=1.9,
            height=0.22,
            fill_color=GREY_A,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        left_pan.move_to(np.array([-3.4, -0.85, 0]))

        right_pan = Rectangle(
            width=1.9,
            height=0.22,
            fill_color=GREY_A,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        right_pan.move_to(np.array([3.4, -0.85, 0]))

        small_window_icon = Rectangle(
            width=0.7,
            height=0.42,
            fill_color=YELLOW,
            fill_opacity=0.25,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        small_window_icon.move_to(np.array([-3.4, -0.52, 0]))

        large_window_icon = Rectangle(
            width=1.5,
            height=0.8,
            fill_color=YELLOW,
            fill_opacity=0.25,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        large_window_icon.move_to(np.array([3.4, -0.35, 0]))

        scale_group = VGroup(
            beam,
            pivot,
            left_string,
            right_string,
            left_pan,
            right_pan,
            small_window_icon,
            large_window_icon,
        )
        scale_group.shift(np.array([0, 0.6, 0]))

        initial_pivot = np.array([0, 0.78, 0])

        # Labels under each side of the scale
        left_label = Text(
            "Better time resolution",
            font_size=30,
            weight="BOLD",
            color=WHITE,
            t2c={"time": YELLOW},
        )
        left_label.scale_to_fit_width(4.2)
        left_label.next_to(left_pan, DOWN, buff=0.5)

        right_label = Text(
            "Better frequency resolution",
            font_size=30,
            weight="BOLD",
            color=WHITE,
            t2c={"frequency": YELLOW},
        )
        right_label.scale_to_fit_width(4.2)
        right_label.next_to(right_pan, DOWN, buff=0.5)

        tradeoff_text = Text(
            "One fixed window cannot optimize both",
            font_size=34,
            weight="BOLD",
            color=YELLOW,
        )
        tradeoff_text.scale_to_fit_width(7.5)
        tradeoff_text.next_to(scale_group, DOWN, buff=0.8)

        # ------------------------------------------------------------
        # CLOSE-UP SIGNAL
        # ------------------------------------------------------------
        close_left = -5.8
        close_right = -0.6
        close_center_x = (close_left + close_right) / 2
        signal_y0 = 0.7
        signal_scale = 1.2
        window_width = 1.5

        def close_signal_y(x):
            local_x = x - close_center_x
            low = 0.13 * np.sin(2 * np.pi * 0.75 * local_x)
            burst = (
                0.52
                * np.sin(2 * np.pi * 3.0 * local_x)
                * np.exp(-((local_x) / 0.28) ** 2)
            )
            return signal_y0 + signal_scale * (low + burst)

        close_panel = Rectangle(
            width=6.4,
            height=3.4,
            fill_color=GREY,
            fill_opacity=0.10,
            stroke_color=GREY_B,
            stroke_width=2,
        )
        close_panel.move_to(np.array([close_center_x, 0.7, 0]))

        close_signal = FunctionGraph(
            close_signal_y,
            x_range=[close_left, close_right],
        )
        close_signal.set_stroke(color=TEAL, width=3)

        close_window = Rectangle(
            width=window_width,
            height=2.2,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=4,
        )

        start_window_x = close_left + 0.3 + window_width / 2
        close_window.move_to(np.array([start_window_x, signal_y0, 0]))

        close_label = Text(
            "STFT uses a fixed window size",
            font_size=30,
            weight="BOLD",
            color=WHITE,
            t2c={"fixed window size": YELLOW},
        )
        close_label.scale_to_fit_width(5.2)
        close_label.next_to(close_panel, DOWN, buff=0.2)

        dash_y_bottom = 1.45
        dash_y_top = 2.25
        dash_y_center = (dash_y_bottom + dash_y_top) / 2

        dash_left = DashedLine(
            np.array([start_window_x - window_width / 2, dash_y_bottom, 0]),
            np.array([start_window_x - window_width / 2, dash_y_top, 0]),
            dash_length=0.12,
            color=YELLOW,
            stroke_width=3,
        )
        dash_right = DashedLine(
            np.array([start_window_x + window_width / 2, dash_y_bottom, 0]),
            np.array([start_window_x + window_width / 2, dash_y_top, 0]),
            dash_length=0.12,
            color=YELLOW,
            stroke_width=3,
        )
        dash_group = VGroup(dash_left, dash_right)
        dash_group.move_to(np.array([start_window_x, dash_y_center, 0]))

        limitation_text = Text(
            "Fixed-window approach: a major limitation of STFT",
            font_size=30,
            weight="BOLD",
            color=WHITE,
            t2c={"major limitation": YELLOW},
        )
        limitation_text.scale_to_fit_width(9.5)
        limitation_text.to_edge(DOWN, buff=0.45)

        # ------------------------------------------------------------
        # BEAT 1: 0.00 - 1.96
        # ------------------------------------------------------------
        self.play(FadeIn(scale_group), run_time=max(0.05, 1.96))
        self.wait(max(0.05, 0.64))

        # ------------------------------------------------------------
        # BEAT 2: 2.60 - 5.08
        # ------------------------------------------------------------
        self.play(
            scale_group.animate.rotate(-0.16, about_point=initial_pivot),
            run_time=max(0.05, 1.50),
        )
        self.play(
            FadeIn(left_label),
            small_window_icon.animate.set_fill(color=YELLOW, opacity=0.75).set_stroke(
                color=WHITE, width=5
            ),
            run_time=max(0.05, 0.98),
        )
        self.wait(max(0.05, 0.86))

        # ------------------------------------------------------------
        # BEAT 3: 5.94 - 9.04
        # ------------------------------------------------------------
        self.play(
            scale_group.animate.rotate(0.32, about_point=initial_pivot),
            run_time=max(0.05, 1.80),
        )
        self.play(
            FadeIn(right_label),
            large_window_icon.animate.set_fill(color=YELLOW, opacity=0.75).set_stroke(
                color=WHITE, width=5
            ),
            run_time=max(0.05, 1.30),
        )
        self.wait(max(0.05, 0.92))

        # ------------------------------------------------------------
        # BEAT 4: 9.96 - 13.92
        # ------------------------------------------------------------
        self.play(
            scale_group.animate.rotate(-0.26, about_point=initial_pivot),
            run_time=max(0.05, 0.80),
        )
        self.play(
            scale_group.animate.rotate(0.23, about_point=initial_pivot),
            run_time=max(0.05, 0.80),
        )
        self.play(
            scale_group.animate.rotate(-0.17, about_point=initial_pivot),
            FadeIn(tradeoff_text),
            run_time=max(0.05, 0.80),
        )
        self.play(
            scale_group.animate.rotate(0.10, about_point=initial_pivot),
            run_time=max(0.05, 0.60),
        )
        self.play(
            scale_group.animate.rotate(-0.08, about_point=initial_pivot),
            run_time=max(0.05, 0.60),
        )
        self.wait(max(0.05, 0.36))
        self.wait(max(0.05, 1.12))

        # ------------------------------------------------------------
        # BEAT 5: 15.04 - 17.18
        # ------------------------------------------------------------
        old_scale_center = scale_group.get_center()
        target_scale_center = np.array([3.2, 1.8, 0])
        scale_factor = 0.55

        old_left_pan_center = left_pan.get_center()
        old_right_pan_center = right_pan.get_center()

        target_left_label = (
            target_scale_center
            + (old_left_pan_center - old_scale_center) * scale_factor
            + np.array([0, -0.5, 0])
        )
        target_right_label = (
            target_scale_center
            + (old_right_pan_center - old_scale_center) * scale_factor
            + np.array([0, -0.5, 0])
        )

        self.play(
            scale_group.animate.scale(scale_factor).move_to(target_scale_center),
            left_label.animate.scale(0.70).move_to(target_left_label),
            right_label.animate.scale(0.70).move_to(target_right_label),
            tradeoff_text.animate.scale(0.75).move_to(np.array([-3.4, 3.2, 0])),
            FadeIn(close_panel, close_signal, close_window, close_label),
            run_time=max(0.05, 2.14),
        )
        self.wait(max(0.05, 0.60))

        # ------------------------------------------------------------
        # BEAT 6: 17.78 - 21.14
        # ------------------------------------------------------------
        burst_center_x = close_center_x

        self.play(FadeIn(dash_group), run_time=max(0.05, 0.50))
        self.play(
            close_window.animate.move_to(np.array([burst_center_x, signal_y0, 0])),
            dash_group.animate.move_to(np.array([burst_center_x, dash_y_center, 0])),
            run_time=max(0.05, 2.86),
        )
        self.wait(max(0.05, 0.34))

        # ------------------------------------------------------------
        # BEAT 7: 21.48 - 24.62
        # ------------------------------------------------------------
        right_end_center_x = close_right - 0.3 - window_width / 2

        self.play(
            close_window.animate.move_to(np.array([right_end_center_x, signal_y0, 0])),
            dash_group.animate.move_to(np.array([right_end_center_x, dash_y_center, 0])),
            run_time=max(0.05, 3.14),
        )
        self.wait(max(0.05, 0.66))

        # ------------------------------------------------------------
        # BEAT 8: 25.28 - 31.10
        # ------------------------------------------------------------
        self.play(
            tradeoff_text.animate.set_opacity(0.55),
            FadeIn(limitation_text),
            run_time=max(0.05, 1.60),
        )

        self.play(
            close_window.animate.set_stroke(color=WHITE, width=7).set_fill(opacity=0.25),
            run_time=max(0.05, 0.50),
        )
        self.play(
            close_window.animate.set_stroke(color=YELLOW, width=4).set_fill(opacity=0.12),
            run_time=max(0.05, 0.50),
        )

        self.wait(max(0.05, 3.22))

        # ------------------------------------------------------------
        # BEAT 9: 31.10 - 31.85
        # ------------------------------------------------------------
        self.play(
            Indicate(limitation_text, scale_factor=1.06, color=YELLOW),
            run_time=max(0.05, 0.75),
        )