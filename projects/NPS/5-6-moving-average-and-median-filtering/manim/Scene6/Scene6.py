ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Data: five neighbouring samples from the narration
        # ------------------------------------------------------------------
        values = [5, 6, 7, 35, 8]
        y_max = 40.0
        chart_height = 2.8
        baseline_y = -1.8
        x_positions = np.array([-4.0, -2.0, 0.0, 2.0, 4.0])
        bar_width = 0.85

        # ------------------------------------------------------------------
        # Title and baseline
        # ------------------------------------------------------------------
        title = Text(
            "Median Filter: Numerical Example",
            font_size=48,
            color=WHITE,
            weight="BOLD",
            t2c={"Median Filter": YELLOW},
        )
        title.to_edge(UP, buff=0.25)

        baseline_line = Line(
            start=np.array([-5.2, baseline_y, 0]),
            end=np.array([5.2, baseline_y, 0]),
            color=GREY,
            stroke_width=2,
        )

        # ------------------------------------------------------------------
        # Build the five sample bars
        # ------------------------------------------------------------------
        bar_rects = []
        bar_labels = []
        bars = []
        bar_group = VGroup()

        for val, x in zip(values, x_positions):
            height = (val / y_max) * chart_height
            rect = Rectangle(
                width=bar_width,
                height=height,
                fill_color=BLUE,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            rect.move_to(np.array([x, baseline_y + height / 2, 0]))
            label = Text(str(val), font_size=24, color=WHITE, weight="BOLD")
            label.next_to(rect, UP, buff=0.12)
            bar = VGroup(rect, label)
            bars.append(bar)
            bar_rects.append(rect)
            bar_labels.append(label)
            bar_group.add(bar)

        spike_rect = bar_rects[3]
        spike_label = bar_labels[3]
        spike_bar = bars[3]

        unwanted = Text("unwanted spike", font_size=22, color=RED, weight="BOLD")
        unwanted.next_to(spike_label, UP, buff=0.18)
        bars[3].add(unwanted)

        # ==================================================================
        # BEAT 1  [0.00 - 2.00]  Title, baseline, and sample bars
        # ==================================================================
        self.play(Write(title), run_time=max(0.05, 0.80))
        self.play(
            Create(baseline_line),
            LaggedStart(
                *[GrowFromCenter(rect) for rect in bar_rects],
                lag_ratio=0.15,
            ),
            *[Write(label) for label in bar_labels],
            run_time=max(0.05, 1.20),
        )

        # ==================================================================
        # BEAT 2  [2.00 - 6.00]  Mark the 35 as an unwanted spike
        # ==================================================================
        self.play(
            Indicate(spike_rect, color=RED, scale_factor=1.08),
            run_time=max(0.05, 1.00),
        )
        self.play(
            spike_rect.animate.set_fill(RED, opacity=1).set_color(RED),
            spike_label.animate.set_color(RED),
            FadeIn(unwanted),
            run_time=max(0.05, 1.40),
        )
        self.wait(max(0.05, 1.60))

        # ==================================================================
        # BEAT 3  [6.00 - 11.00]  Moving average is pulled upward
        # ==================================================================
        mean_val = (5 + 6 + 7 + 35 + 8) / 5  # 12.2
        mean_y = baseline_y + (mean_val / y_max) * chart_height

        mean_line = DashedLine(
            start=np.array([-5.0, mean_y, 0]),
            end=np.array([5.0, mean_y, 0]),
            color=ORANGE,
            stroke_width=3,
            dash_length=0.18,
        )
        mean_label = Text("mean 12.2", font_size=20, color=ORANGE, weight="BOLD")
        mean_label.next_to(mean_line.get_end(), RIGHT, buff=0.20)

        self.play(Create(mean_line), run_time=max(0.05, 1.40))
        self.play(FadeIn(mean_label), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 1.00))
        self.play(
            mean_line.animate.set_stroke(width=5),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 1.20))

        # ==================================================================
        # BEAT 4  [11.00 - 16.00]  Sort, highlight median 7
        # ==================================================================
        median_y = baseline_y + (7.0 / y_max) * chart_height
        median_line = DashedLine(
            start=np.array([-5.0, median_y, 0]),
            end=np.array([5.0, median_y, 0]),
            color=GREEN,
            stroke_width=3,
            dash_length=0.18,
        )
        median_label = Text("median 7", font_size=20, color=GREEN, weight="BOLD")
        median_label.next_to(median_line.get_end(), RIGHT, buff=0.20)

        self.play(FadeOut(mean_line), FadeOut(mean_label), run_time=max(0.05, 0.60))
        self.play(
            bars[3].animate.shift(RIGHT * 2),
            bars[4].animate.shift(LEFT * 2),
            run_time=max(0.05, 1.20),
        )
        self.play(
            Create(median_line),
            FadeIn(median_label),
            run_time=max(0.05, 1.00),
        )
        self.play(
            bars[2][0].animate.set_fill(GREEN, opacity=1).set_color(GREEN),
            bars[2][1].animate.set_color(YELLOW),
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 1.40))

        # ==================================================================
        # BEAT 5  [16.00 - 21.00]  Show the output: 7
        # ==================================================================
        output_text = Text("Output = 7", font_size=60, color=GREEN, weight="BOLD")
        output_text.next_to(baseline_line, DOWN, buff=0.55)

        surround_rect = SurroundingRectangle(
            bars[2],
            color=YELLOW,
            buff=0.12,
            corner_radius=0.10,
        )

        self.play(
            GrowFromCenter(output_text),
            Create(surround_rect),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 1.00))
        self.play(output_text.animate.scale(1.06), run_time=max(0.05, 0.80))
        self.play(output_text.animate.scale(1 / 1.06), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 1.20))

        # ==================================================================
        # BEAT 6  [21.00 - 25.00]  Small waveform: impulsive noise cleaned
        # ==================================================================
        chart_group = VGroup(
            baseline_line,
            bar_group,
            median_line,
            median_label,
            output_text,
            surround_rect,
        )
        self.play(FadeOut(chart_group), run_time=max(0.05, 0.50))

        mini_axes = Axes(
            x_range=[0, 20, 1],
            y_range=[0, 11, 1],
            x_length=6.0,
            y_length=2.4,
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
                "stroke_color": GREY,
                "stroke_width": 2,
            },
            tips=False,
        ).move_to(ORIGIN)

        n_trace = 61
        x_trace = np.linspace(0, 20, n_trace)
        smooth = 5 + 0.8 * np.sin(0.55 * x_trace) + 0.5 * np.sin(1.35 * x_trace)
        orig_y = smooth.copy()
        orig_y[30] = 10.5
        clean_y = smooth.copy()

        orig_trace = VMobject(
            stroke_color=RED, stroke_width=3, fill_opacity=0
        ).set_points_as_corners(
            [mini_axes.c2p(x_trace[i], orig_y[i]) for i in range(n_trace)]
        )

        clean_trace = VMobject(
            stroke_color=GREEN, stroke_width=3, fill_opacity=0
        ).set_points_as_corners(
            [mini_axes.c2p(x_trace[i], clean_y[i]) for i in range(n_trace)]
        )

        self.play(
            FadeIn(mini_axes),
            FadeIn(orig_trace),
            run_time=max(0.05, 0.60),
        )
        self.play(Transform(orig_trace, clean_trace), run_time=max(0.05, 1.40))

        clean_label = Text("spike removed", font_size=26, color=GREEN, weight="BOLD")
        clean_label.next_to(mini_axes, DOWN, buff=0.30)
        self.play(FadeIn(clean_label), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.00))

        # ==================================================================
        # BEAT 7  [25.00 - 29.30]  Final takeaway
        # ==================================================================
        final_text = Text(
            "Median filter removes the spike\nand preserves the surrounding waveform",
            font_size=30,
            color=WHITE,
            line_spacing=0.8,
            t2c={"removes the spike": GREEN},
        )
        final_text.scale_to_fit_width(9.5)
        final_text.next_to(mini_axes, DOWN, buff=0.40)

        self.play(
            FadeOut(clean_label),
            FadeIn(final_text),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 1.50))
        self.play(
            Indicate(orig_trace, color=GREEN, scale_factor=1.03),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.60))