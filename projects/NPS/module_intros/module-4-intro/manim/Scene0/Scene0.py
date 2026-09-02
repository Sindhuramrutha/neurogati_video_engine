ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----- Title: MODULE 4 -----
        module_text = Text("MODULE", font_size=84, weight=BOLD, color=WHITE)
        four_text = Text("4", font_size=96, weight=BOLD, color=GOLD)

        title_group = VGroup(module_text, four_text).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.4)
        module_final = module_text.get_center()
        four_final = four_text.get_center()

        # Fly MODULE in from upper-left
        module_text.move_to(np.array([-9, 3.2, 0]))
        self.play(
            module_text.animate.move_to(module_final),
            run_time=max(0.05, 0.52),
            rate_func=rate_functions.ease_out_elastic
        )

        # Fly 4 in from upper-right
        four_text.move_to(np.array([9, 3.2, 0]))
        self.play(
            four_text.animate.move_to(four_final),
            run_time=max(0.05, 0.36),
            rate_func=rate_functions.ease_out_elastic
        )

        self.wait(max(0.05, 0.40))  # 0.88 -> 1.28

        # ----- Subtitle -----
        subtitle = Text("Time and Frequency Domains", font_size=52, color=WHITE)
        subtitle.next_to(title_group, DOWN, buff=0.45)
        self.play(AddTextLetterByLetter(subtitle), run_time=max(0.05, 1.32))
        self.wait(max(0.05, 1.08))  # 2.60 -> 3.68

        # ----- Layout constants -----
        x_min, x_max = -6.2, -1.0
        base_y = 0.2
        a1, a2, a3 = 0.7, 0.5, 0.35
        f1, f2, f3 = 2.0, 3.5, 5.5

        def sig_point(t):
            x = x_min + (x_max - x_min) * t
            y = (
                base_y
                + a1 * np.sin(2 * PI * f1 * t)
                + a2 * np.sin(2 * PI * f2 * t + 0.8)
                + a3 * np.sin(2 * PI * f3 * t + 1.5)
            )
            return np.array([x, y, 0])

        # ----- Time-domain waveform -----
        signal = ParametricFunction(
            sig_point,
            t_range=[0, 1],
            color=TEAL,
            stroke_width=5
        )
        time_axis = DashedLine(
            np.array([-6.5, base_y, 0]),
            np.array([-0.5, base_y, 0]),
            color=GREY_B,
            stroke_width=2
        )
        self.play(Create(signal), FadeIn(time_axis), run_time=max(0.05, 1.84), rate_func=linear)
        self.wait(max(0.05, 0.56))  # 5.52 -> 6.08

        # ----- Decompose into three sine waves -----
        comp1 = ParametricFunction(
            lambda t: np.array([
                x_min + (x_max - x_min) * t,
                -1.7 + a1 * np.sin(2 * PI * f1 * t),
                0
            ]),
            t_range=[0, 1],
            color=BLUE,
            stroke_width=4
        )
        comp2 = ParametricFunction(
            lambda t: np.array([
                x_min + (x_max - x_min) * t,
                -2.4 + a2 * np.sin(2 * PI * f2 * t + 0.8),
                0
            ]),
            t_range=[0, 1],
            color=GREEN,
            stroke_width=4
        )
        comp3 = ParametricFunction(
            lambda t: np.array([
                x_min + (x_max - x_min) * t,
                -3.0 + a3 * np.sin(2 * PI * f3 * t + 1.5),
                0
            ]),
            t_range=[0, 1],
            color=ORANGE,
            stroke_width=4
        )
        self.play(
            LaggedStart(
                TransformFromCopy(signal, comp1),
                TransformFromCopy(signal, comp2),
                TransformFromCopy(signal, comp3),
                lag_ratio=0.4,
                run_time=max(0.05, 1.36
            ))
        )
        self.wait(max(0.05, 0.68))  # 7.44 -> 8.12

        # ----- Power spectrum bars -----
        spectrum_baseline = DashedLine(
            np.array([1.2, -2.4, 0]),
            np.array([6.0, -2.4, 0]),
            color=GREY_B,
            stroke_width=2
        )
        bar_xs = [2.2, 3.9, 5.6]
        bar_heights = [2.0, 1.43, 1.0]
        bar_colors = [BLUE, GREEN, ORANGE]
        bars = VGroup()
        for x, h, c in zip(bar_xs, bar_heights, bar_colors):
            bar = Rectangle(
                width=0.55,
                height=h,
                fill_color=c,
                fill_opacity=1,
                stroke_width=0
            )
            bar.move_to(np.array([x, -2.4 + h / 2, 0]))
            bars.add(bar)

        self.play(
            FadeIn(spectrum_baseline),
            *[GrowFromEdge(bar, DOWN) for bar in bars],
            run_time=max(0.05, 1.02
        ))
        self.wait(max(0.05, 0.64))  # 9.14 -> 9.78

        # ----- Sample dots along the original waveform -----
        dot_positions = []
        n_dots = 7
        for i in range(n_dots):
            t = i / (n_dots - 1)
            dot_positions.append(sig_point(t))
        dots = VGroup(*[
            Dot(pos, radius=0.07, color=PINK, fill_opacity=1)
            for pos in dot_positions
        ])
        self.play(
            LaggedStart(
                *[GrowFromCenter(dot) for dot in dots],
                lag_ratio=0.5,
                run_time=max(0.05, 0.26
            ))
        )
        self.wait(max(0.05, 0.54))  # 10.04 -> 10.58

        # ----- Neural frequency bands -----
        band_colors = [BLUE, GREEN, ORANGE]
        band_names = ["Delta", "Theta", "Alpha"]
        bands = VGroup()
        for color, name in zip(band_colors, band_names):
            strip = Rectangle(
                width=1.3,
                height=0.35,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            )
            label = Text(name, font_size=26, color=WHITE)
            band = VGroup(strip, label).arrange(RIGHT, buff=0.18)
            bands.add(band)

        bands.arrange(RIGHT, buff=0.7)
        bands.next_to(spectrum_baseline, DOWN, buff=0.55)

        self.play(
            LaggedStart(
                *[FadeIn(band, shift=DOWN * 0.4) for band in bands],
                lag_ratio=0.35,
                run_time=max(0.05, 0.75
            ))
        )
        self.play(bands.animate.set_opacity(0.8), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.11))  # 10.58 -> 11.74

        # ----- Pulse highlights -----
        self.play(Indicate(bars, color=WHITE, scale_factor=1.15), run_time=max(0.05, 0.60))
        self.play(Indicate(dots, color=YELLOW, scale_factor=1.30), run_time=max(0.05, 0.60))
        self.play(Indicate(bands, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.62))
        self.wait(max(0.05, 0.20))  # 11.74 -> 13.76

        self.wait(max(0.05, 0.84))  # 13.76 -> 14.60

        # ----- Clear and closing burst -----
        all_visuals = VGroup(
            title_group,
            subtitle,
            signal,
            time_axis,
            comp1,
            comp2,
            comp3,
            spectrum_baseline,
            bars,
            dots,
            bands
        )
        self.play(FadeOut(all_visuals), run_time=max(0.05, 0.30))

        final_text = Text("Let's get started!", font_size=72, weight=BOLD, color=WHITE)
        final_text.move_to(ORIGIN).scale(0.25).set_opacity(0)

        self.play(
            final_text.animate.scale(4).set_opacity(1),
            run_time=max(0.05, 0.45),
            rate_func=rate_functions.ease_out_back
        )
        self.play(Flash(final_text, color=WHITE, flash_radius=0.7, line_length=0.4), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.47))  # 14.60 -> 16.07