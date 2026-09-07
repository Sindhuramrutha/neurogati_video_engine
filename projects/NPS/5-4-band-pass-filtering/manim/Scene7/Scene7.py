ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np
from manim.utils import rate_functions


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def get_filter_poly(
            low_cut,
            high_cut,
            axis_y,
            gain=0.5,
            slope_width=0.5,
            x_min=-3.0,
            x_max=3.0,
        ):
            points = [
                np.array([x_min, axis_y, 0]),
                np.array([low_cut - slope_width, axis_y, 0]),
                np.array([low_cut, axis_y + gain, 0]),
                np.array([high_cut, axis_y + gain, 0]),
                np.array([high_cut + slope_width, axis_y, 0]),
                np.array([x_max, axis_y, 0]),
            ]
            return Polygon(
                *points,
                fill_color=TEAL,
                fill_opacity=0.7,
                stroke_color=WHITE,
                stroke_width=1.5,
            )

        def make_waveform(signal_func, x_range, y_center, color=WHITE, stroke_width=1.5):
            return ParametricFunction(
                lambda t: np.array(
                    [
                        x_range[0] + t * (x_range[1] - x_range[0]),
                        y_center + signal_func(t),
                        0,
                    ]
                ),
                t_range=[0, 1],
                dt=0.01,
                color=color,
                stroke_width=stroke_width,
                stroke_opacity=1,
            )

        def make_small_axis():
            axis = Line(LEFT * 3, RIGHT * 3, color=GREY, stroke_width=2)
            ticks = VGroup(
                *[
                    Line(UP * 0.15, DOWN * 0.15, color=GREY).move_to(
                        np.array([x, 0, 0])
                    )
                    for x in [-3, -2, -1, 0, 1, 2, 3]
                ]
            )
            label = Text("Frequency (Hz)", font_size=20, color=WHITE).next_to(
                axis, DOWN, buff=0.3
            )
            return VGroup(axis, ticks, label)

        # ---------- Beat 1: frequency axis + narrow band-pass ----------
        axis_line = Line(LEFT * 4.5, RIGHT * 4.5, color=GREY, stroke_width=2)
        axis_line.move_to(UP * 1.0)

        main_ticks = VGroup(
            *[
                Line(UP * 0.2, DOWN * 0.2, color=GREY).move_to(
                    np.array([x, 1.0, 0])
                )
                for x in [-4, -3, -2, -1, 0, 1, 2, 3, 4]
            ]
        )

        main_label = Text("Frequency (Hz)", font_size=28, color=WHITE).next_to(
            axis_line, DOWN, buff=0.5
        )

        main_filter = get_filter_poly(
            low_cut=-0.5,
            high_cut=0.5,
            axis_y=1.0,
            gain=0.5,
            slope_width=0.8,
            x_min=-4.5,
            x_max=4.5,
        )

        self.play(
            Create(axis_line),
            Write(main_ticks),
            Write(main_label),
            DrawBorderThenFill(main_filter),
            run_time=max(0.05, 2.4),
        )
        self.wait(max(0.05, 3.06 - 2.4))

        # ---------- Beat 2: overly smooth waveform + critical label ----------
        narrow_wave = make_waveform(
            signal_func=lambda t: 0.4 * np.sin(2 * np.pi * 2 * t),
            x_range=(-4.5, 4.5),
            y_center=-0.8,
        )

        critical_label = Text(
            "Cutoff choice is critical", font_size=30, color=YELLOW
        ).next_to(main_filter, UP, buff=0.5)

        self.play(
            Create(narrow_wave),
            FadeIn(critical_label),
            run_time=max(0.05, 1.6),
        )
        self.wait(max(0.05, 5.80 - 3.06 - 1.6))

        # ---------- Beat 3: widen passband, waveform gains detail + noise ----------
        np.random.seed(42)
        t_vals = np.linspace(0, 1, 200)
        noise_arr = np.random.randn(200) * 0.05

        wide_filter = get_filter_poly(
            low_cut=-2.0,
            high_cut=2.0,
            axis_y=1.0,
            gain=0.5,
            slope_width=0.8,
            x_min=-4.5,
            x_max=4.5,
        )

        wide_wave = make_waveform(
            signal_func=lambda t: 0.3 * np.sin(2 * np.pi * 8 * t)
            + 0.2 * np.sin(2 * np.pi * 15 * t)
            + np.interp(t, t_vals, noise_arr),
            x_range=(-4.5, 4.5),
            y_center=-0.8,
        )

        self.play(
            Transform(main_filter, wide_filter),
            Transform(narrow_wave, wide_wave),
            run_time=max(0.05, 3.0),
        )
        self.wait(max(0.05, 11.34 - 5.80 - 3.0))

        # Everything on the main screen, for the upcoming split fade-out.
        scene_group = VGroup(
            axis_line, main_ticks, main_label, main_filter, narrow_wave, critical_label
        )

        # ---------- Beat 4: split into two panels ----------
        # Left panel: ideal passband
        left_static = make_small_axis()
        left_filter = get_filter_poly(
            low_cut=-1.0,
            high_cut=1.0,
            axis_y=0.0,
            gain=0.5,
            slope_width=0.6,
            x_min=-3.0,
            x_max=3.0,
        )
        left_ideal_wave = make_waveform(
            signal_func=lambda t: 0.3 * np.sin(2 * np.pi * 3 * t)
            + 0.2 * np.sin(2 * np.pi * 7 * t)
            + 0.15 * np.sin(2 * np.pi * 12 * t),
            x_range=(-3.0, 3.0),
            y_center=-1.3,
        )
        left_label = Text("Ideal passband", font_size=22, color=GREEN).next_to(
            left_static, UP, buff=0.5
        )
        left_panel = VGroup(left_static, left_filter, left_ideal_wave, left_label)
        left_panel.move_to(np.array([-3.5, 1.0, 0]))

        # Right panel: too narrow / too wide
        right_static = make_small_axis()
        right_label = Text(
            "Too narrow or too wide", font_size=20, color=ORANGE
        ).next_to(right_static, UP, buff=0.5)

        right_filter_narrow = get_filter_poly(
            low_cut=-0.4,
            high_cut=0.4,
            axis_y=0.0,
            gain=0.5,
            slope_width=0.4,
            x_min=-3.0,
            x_max=3.0,
        )
        right_wave_narrow = make_waveform(
            signal_func=lambda t: 0.4 * np.sin(2 * np.pi * 1.5 * t),
            x_range=(-3.0, 3.0),
            y_center=-1.3,
        )

        right_filter_wide = get_filter_poly(
            low_cut=-2.0,
            high_cut=2.0,
            axis_y=0.0,
            gain=0.5,
            slope_width=0.5,
            x_min=-3.0,
            x_max=3.0,
        )
        right_wave_wide = make_waveform(
            signal_func=lambda t: 0.3 * np.sin(2 * np.pi * 7 * t)
            + 0.2 * np.sin(2 * np.pi * 14 * t)
            + np.interp(t, t_vals, noise_arr * 0.6),
            x_range=(-3.0, 3.0),
            y_center=-1.3,
        )

        right_panel = VGroup(
            right_static, right_filter_narrow, right_wave_narrow, right_label
        )
        right_panel.move_to(np.array([3.5, 1.0, 0]))

        self.play(FadeOut(scene_group), run_time=max(0.05, 0.6))
        self.play(
            FadeIn(left_panel),
            FadeIn(right_panel),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.7))

        right_filter_wide.move_to(right_filter_narrow.get_center())
        right_wave_wide.move_to(right_wave_narrow.get_center())
        self.play(
            Transform(right_filter_narrow, right_filter_wide),
            Transform(right_wave_narrow, right_wave_wide),
            run_time=max(0.05, 1.6),
        )
        self.wait(max(0.05, 16.08 - 11.34 - 0.6 - 1.2 - 0.7 - 1.6))

        # ---------- Beat 5: dashed box + warning message ----------
        dashed_box = DashedVMobject(
            SurroundingRectangle(right_panel, color=RED, stroke_width=2, buff=0.3),
            num_dashes=24,
        )

        warning_rect = Rectangle(
            width=10,
            height=1.2,
            fill_color=MAROON,
            fill_opacity=0.9,
            stroke_color=RED,
            stroke_width=2,
        )
        warning_text = Text(
            "Incorrect cutoff frequencies may remove\nuseful information or preserve unwanted interference",
            font_size=24,
            color=WHITE,
            line_spacing=0.8,
        )
        warning_box = VGroup(warning_rect, warning_text)
        warning_box.move_to(DOWN * 2.8)

        self.play(Create(dashed_box), run_time=max(0.05, 1.2))
        self.play(FadeIn(warning_box), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 23.74 - 16.08 - 1.2 - 1.2))

        # ---------- Beat 6: hold, narration only ----------
        self.wait(max(0.05, 36.38 - 23.74))

        # ---------- Beat 7: subtle warning-box pulse ----------
        self.play(
            warning_box.animate.scale(1.05),
            run_time=max(0.05, 0.7),
            rate_func=rate_functions.there_and_back,
        )
        self.wait(max(0.05, 43.45 - 36.38 - 0.7))