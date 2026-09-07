ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *

class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Title ---
        title = Text("Moving-Average Filter", font_size=48, color=WHITE, weight="BOLD")
        subtitle = Text("Definition and Principle", font_size=32, color=GREY)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP, buff=0.8)

        # Slide title in from left
        title_group.move_to(LEFT * 8 + title_group.get_center()[1] * UP)
        self.play(title_group.animate.move_to(UP * 2.5), run_time=max(0.05, 1.5))

        # --- Signal display area ---
        # We'll build a horizontal array of sample points as little rectangles/bars
        n_samples = 17  # odd so there's a clear center for a 5-sample window demo
        sample_values = [2, 3, 4, 3, 2, 3, 5, 4, 3, 4, 6, 5, 4, 5, 7, 6, 5]
        bar_width = 0.5
        max_val = 8
        bar_height_factor = 0.4  # each unit of value = 0.4 units tall

        bars = VGroup()
        for i, val in enumerate(sample_values):
            bar = Rectangle(
                width=bar_width,
                height=val * bar_height_factor,
                fill_color=BLUE,
                fill_opacity=0.9,
                stroke_width=0
            )
            bar.move_to(np.array([(i - n_samples//2) * (bar_width + 0.1), -0.5, 0]), aligned_edge=DOWN)
            bars.add(bar)

        # Axis line under bars
        axis = Line(
            start=bars[0].get_bottom() + LEFT * 0.3,
            end=bars[-1].get_bottom() + RIGHT * 0.3,
            color=GREY, stroke_width=2
        )
        axis_label = Text("signal samples", font_size=22, color=GREY)
        axis_label.next_to(axis, DOWN, buff=0.2)

        # Appear signal display
        self.play(
            FadeIn(bars),
            FadeIn(axis),
            FadeIn(axis_label),
            run_time=max(0.05, 1.5)
        )
        self.wait(max(0.05, 2.0))  # settle

        # --- Highlight a 5-sample window (center sample index 8) ---
        # The window covers indices 6,7,8,9,10
        window_indices = [6, 7, 8, 9, 10]
        window_rect = SurroundingRectangle(
            VGroup(*[bars[i] for i in window_indices]),
            color=YELLOW,
            buff=0.15,
            stroke_width=3
        )

        # Slide window in from the left over the bars
        window_start_rect = SurroundingRectangle(
            VGroup(*[bars[i] for i in range(5)]),
            color=YELLOW,
            buff=0.15,
            stroke_width=3
        )
        window_start_rect.set_opacity(0)
        self.add(window_start_rect)

        # Show the concept of sliding window - animate across
        self.play(
            Transform(window_start_rect, window_rect),
            run_time=max(0.05, 2.0)
        )
        self.remove(window_start_rect)
        self.add(window_rect)

        # --- "Average" label and computation ---
        avg_val = sum(sample_values[i] for i in window_indices) / 5
        avg_text = Text(
            f"Average = {avg_val:.1f}",
            font_size=30,
            color=ORANGE
        )
        avg_text.next_to(window_rect, UP, buff=0.4)

        # Show the replacement bar growing from the original
        center_bar = bars[8]
        new_height = avg_val * bar_height_factor
        avg_bar = Rectangle(
            width=bar_width,
            height=new_height,
            fill_color=ORANGE,
            fill_opacity=0.95,
            stroke_width=0
        )
        avg_bar.move_to(center_bar.get_bottom(), aligned_edge=DOWN)

        self.play(
            Write(avg_text),
            FadeIn(avg_bar),
            run_time=max(0.05, 2.0)
        )
        self.wait(max(0.05, 1.0))

        # --- Show the entire signal after applying moving average ---
        # Compute a 5-point moving average for the whole signal
        def moving_avg(vals, window=5):
            half = window // 2
            result = []
            for i in range(len(vals)):
                start = max(0, i - half)
                end = min(len(vals), i + half + 1)
                # pad with edge values for simplicity
                segment = vals[max(0,i-half): min(len(vals),i+half+1)]
                result.append(sum(segment) / len(segment))
            return result

        smoothed = moving_avg(sample_values, window=5)

        smoothed_bars = VGroup()
        for i, val in enumerate(smoothed):
            bar = Rectangle(
                width=bar_width,
                height=val * bar_height_factor,
                fill_color=TEAL,
                fill_opacity=0.9,
                stroke_width=0
            )
            bar.move_to(np.array([(i - n_samples//2) * (bar_width + 0.1), -0.5, 0]), aligned_edge=DOWN)
            smoothed_bars.add(bar)

        smoothed_bars.set_opacity(0)
        self.add(smoothed_bars)

        # Fade out the average overlay, fade in smoothed bars
        self.play(
            FadeOut(window_rect),
            FadeOut(avg_text),
            FadeOut(avg_bar),
            smoothed_bars.animate.set_opacity(1),
            bars.animate.set_opacity(0.25),
            run_time=max(0.05, 2.5)
        )
        self.wait(max(0.05, 1.0))

        # Label "smoothed signal"
        smoothed_label = Text("smoothed", font_size=28, color=TEAL)
        smoothed_label.next_to(axis_label, DOWN, buff=0.3)

        self.play(Write(smoothed_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.0))

        # --- Key insight text ---
        insight1 = Text(
            "Rapid fluctuations → averaged out",
            font_size=28,
            color=WHITE
        )
        insight2 = Text(
            "Slow trends → preserved",
            font_size=28,
            color=WHITE
        )
        insight_group = VGroup(insight1, insight2).arrange(DOWN, buff=0.3)
        insight_group.next_to(smoothed_label, DOWN, buff=0.7)

        self.play(
            FadeIn(insight1, shift=UP * 0.3, run_time=max(0.05, 1.5)),
        )
        self.play(
            FadeIn(insight2, shift=UP * 0.3, run_time=max(0.05, 1.5)),
        )
        self.wait(max(0.05, 2.0))

        # --- Window size note ---
        window_note = Text(
            "Window size matters: wider = more smoothing",
            font_size=26,
            color=GREY_B
        )
        window_note.next_to(insight_group, DOWN, buff=0.6)

        self.play(FadeIn(window_note, run_time=max(0.05, 1.5)))
        self.wait(max(0.05, 2.0))

        # --- Operation repeats note ---
        repeat_note = Text(
            "This operation repeats for every sample",
            font_size=26,
            color=GREY_B
        )
        repeat_note.next_to(window_note, DOWN, buff=0.4)

        self.play(FadeIn(repeat_note, run_time=max(0.05, 1.5)))
        self.wait(max(0.05, 1.5))

        # --- Fade to black at the end ---
        black_rect = Rectangle(
            width=14, height=8,
            fill_color=BLACK, fill_opacity=0,
            stroke_width=0
        )
        black_rect.to_edge(UP, buff=0).to_edge(LEFT, buff=0)
        self.add(black_rect)

        # Final fade duration computed from total budget
        total_elapsed = 1.5 + 1.5 + 2.0 + 2.0 + 2.0 + 1.0 + 2.5 + 1.0 + 1.0 + 1.0 + 1.5 + 1.5 + 2.0 + 1.5 + 2.0 + 1.5 + 1.5
        # compute remaining time
        remaining = max(0.05, 28.32 - total_elapsed)
        self.play(
            black_rect.animate.set_opacity(1),
            run_time=max(0.05, remaining
        ))
        self.wait(max(0.05, 0))