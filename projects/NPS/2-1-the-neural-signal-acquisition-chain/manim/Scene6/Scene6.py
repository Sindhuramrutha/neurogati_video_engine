ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Helper: make a sine-wave VMobject from points
        def make_wave_points(center, length, amplitude, cycles=1, n=160):
            pts = []
            x0 = center[0] - length / 2
            for i in range(n + 1):
                x = x0 + length * i / n
                y = center[1] + amplitude * np.sin(2 * PI * cycles * i / n)
                pts.append(np.array([x, y, 0]))
            return pts

        def make_wave(pts, color, width):
            wave = VMobject()
            wave.set_points_as_corners(pts)
            wave.set_stroke(color=color, width=width)
            wave.set_fill(opacity=0)
            return wave

        # Layout
        input_center = np.array([-4.7, 1.2, 0])
        input_length = 3.5
        amp = 1.0
        input_right = np.array([input_center[0] + input_length / 2, 1.2, 0])  # -2.95

        filter_cx = 0.8
        box_w = 2.6
        box_h = 1.7
        filter_left = np.array([filter_cx - box_w / 2, 1.2, 0])    # -0.5
        filter_right = np.array([filter_cx + box_w / 2, 1.2, 0])   # 2.1

        output_center = np.array([4.9, 1.2, 0])
        output_length = 2.9
        output_left = np.array([output_center[0] - output_length / 2, 1.2, 0])  # 3.45

        # The clean amplified waveform that continues from Scene 5
        input_pts = make_wave_points(input_center, input_length, amp)
        input_clean = make_wave(input_pts, ORANGE, 6)

        # Noise trace: same shape plus sharp random vertical jitter
        np.random.seed(7)
        jitter = np.random.uniform(-0.14, 0.14, size=len(input_pts))
        noise_pts = [input_pts[i] + np.array([0, jitter[i], 0]) for i in range(len(input_pts))]
        noise_trace = make_wave(noise_pts, RED, 3)

        # Labels for the noisy input
        label_noisy = Text("amplified signal + interference", font_size=24, color=WHITE)
        label_noisy.next_to(noise_trace, DOWN, buff=0.25)

        label_interference = Text("unwanted electrical interference", font_size=24, color=RED)
        label_interference.next_to(noise_trace, DOWN, buff=0.25)

        # Flow line into the future filter box
        flow_in = Arrow(
            start=input_right,
            end=filter_left,
            buff=0,
            stroke_width=5,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.12,
        )

        # Filter box and label
        filter_box = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=BLUE,
            stroke_width=4,
            fill_color=BLUE,
            fill_opacity=0.15,
        )
        filter_box.move_to(np.array([filter_cx, 1.2, 0]))
        filter_label = Text("Filter", font_size=32, color=WHITE)
        filter_label.move_to(filter_box.get_center())

        # Output side: clean wave and flow out
        output_pts = make_wave_points(output_center, output_length, amp)
        output_clean = make_wave(output_pts, ORANGE, 6)

        flow_out = Arrow(
            start=filter_right,
            end=output_left,
            buff=0,
            stroke_width=5,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.12,
        )

        caption_signal = Text("signal of interest", font_size=24, color=YELLOW)
        caption_signal.next_to(output_clean, DOWN, buff=0.25)

        # Frequency spectrum panels
        def make_spectrum(center, low_heights=None, high_heights=None, include_high=True):
            axis = Line(
                start=center + LEFT * 2.9,
                end=center + RIGHT * 2.9,
                color=GREY_B,
                stroke_width=3,
            )
            low_xs = [-2.55, -2.10, -1.65, -1.20, -0.75, -0.30]
            if low_heights is None:
                low_heights = [0.65, 0.85, 0.75, 0.95, 0.70, 0.85]
            low_bars = VGroup()
            for x, h in zip(low_xs, low_heights):
                bar = Rectangle(
                    width=0.20,
                    height=h,
                    fill_color=GREEN,
                    fill_opacity=1,
                    stroke_width=0,
                )
                bar.move_to(center + np.array([x, h / 2, 0]))
                low_bars.add(bar)

            high_bars = VGroup()
            if include_high:
                high_xs = [0.30, 0.65, 1.00, 1.35, 1.70, 2.05, 2.40]
                if high_heights is None:
                    high_heights = [0.30, 0.18, 0.38, 0.22, 0.34, 0.20, 0.28]
                for x, h in zip(high_xs, high_heights):
                    bar = Rectangle(
                        width=0.14,
                        height=h,
                        fill_color=RED,
                        fill_opacity=1,
                        stroke_width=0,
                    )
                    bar.move_to(center + np.array([x, h / 2, 0]))
                    high_bars.add(bar)

            signal_label = Text("signal", font_size=18, color=GREEN)
            signal_label.next_to(low_bars, UP, buff=0.12)

            freq_label = Text("frequency", font_size=18, color=GREY_B)
            freq_label.next_to(axis, DOWN, buff=0.20)

            interference_label = None
            if include_high:
                interference_label = Text("interference", font_size=18, color=RED)
                interference_label.next_to(high_bars, UP, buff=0.12)

            group = VGroup(axis, low_bars, signal_label)
            if include_high:
                group.add(high_bars)
                group.add(interference_label)
            group.add(freq_label)

            return group, low_bars, high_bars, axis, signal_label, interference_label, freq_label

        panel1_center = np.array([0, -1.65, 0])
        panel2_center = np.array([0, -3.05, 0])

        panel1, low_bars1, high_bars1, axis1, sig_lab1, interf_lab1, freq_lab1 = make_spectrum(
            panel1_center, include_high=True
        )
        panel2, low_bars2, high_bars2, axis2, sig_lab2, _, _ = make_spectrum(
            panel2_center, include_high=False
        )

        before_label = Text("before filtering", font_size=20, color=GREY_B)
        before_label.next_to(panel1, LEFT, buff=0.7)
        after_label = Text("after filtering", font_size=20, color=GREY_B)
        after_label.next_to(panel2, LEFT, buff=0.7)

        all_bars1 = VGroup(*low_bars1, *high_bars1)

        # Flow dot path from noisy input through the filter to clean output
        flow_path_points = [input_right, filter_left, filter_right, output_left]
        flow_dot = Dot(input_right, radius=0.07, color=WHITE)
        flow_dot.set_z_index(0)
        filter_box.set_z_index(2)

        def update_flow_dot(mob, alpha):
            seg = alpha * (len(flow_path_points) - 1)
            i = min(int(seg), len(flow_path_points) - 2)
            frac = seg - i
            p1 = flow_path_points[i]
            p2 = flow_path_points[i + 1]
            mob.move_to(p1 * (1 - frac) + p2 * frac)

        # Beat 1 (0.00-0.50): amplified waveform is already visible, noise appears.
        self.add(input_clean)
        self.play(FadeIn(noise_trace), run_time=max(0.05, 0.50))

        # Beat 2 (0.50-1.36): hold noisy waveform and label it.
        self.play(Write(label_noisy), run_time=max(0.05, 0.86))

        # Gap to 2.10
        self.wait(max(0.05, 0.74))

        # Beat 3 (2.10-3.16): flow line toward the right / future filter.
        self.play(Create(flow_in), run_time=max(0.05, 1.06))

        # Gap to 3.64
        self.wait(max(0.05, 0.48))

        # Beat 4 (3.64-5.18): noise pulses once, interference label replaces initial label.
        self.play(
            noise_trace.animate.set_stroke(color=WHITE, width=6),
            run_time=max(0.05, 0.50),
        )
        self.play(
            noise_trace.animate.set_stroke(color=RED, width=3),
            FadeOut(label_noisy),
            Write(label_interference),
            run_time=max(0.05, 1.04),
        )

        # Gap to 6.18
        self.wait(max(0.05, 1.00))

        # Beat 5 (6.18-7.64): filter box draws around the flow line.
        self.play(Create(filter_box), Write(filter_label), run_time=max(0.05, 1.46))

        # Gap to 8.50
        self.wait(max(0.05, 0.86))

        # Beat 6 (8.50-10.80): clean output emerges from the right side of the filter.
        self.play(Create(flow_out), run_time=max(0.05, 0.45))
        self.play(Create(output_clean), run_time=max(0.05, 1.85))

        # Gap to 11.38
        self.wait(max(0.05, 0.58))

        # Beat 7 (11.38-12.92): output wave pulses, flow dot moves, caption appears.
        self.add(flow_dot)
        self.play(
            output_clean.animate.set_stroke(color=WHITE, width=8),
            Write(caption_signal),
            run_time=max(0.05, 0.50),
        )
        self.play(
            output_clean.animate.set_stroke(color=ORANGE, width=6),
            run_time=max(0.05, 0.24),
        )
        self.play(UpdateFromAlphaFunc(flow_dot, update_flow_dot), run_time=max(0.05, 0.80))
        self.remove(flow_dot)

        # Gap to 13.78
        self.wait(max(0.05, 0.86))

        # Beat 8 (13.78-16.66): frequency spectrum panel appears.
        self.play(Create(axis1), run_time=max(0.05, 0.40))
        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in all_bars1], lag_ratio=0.06),
            run_time=max(0.05, 1.50),
        )
        self.play(
            Write(sig_lab1),
            Write(interf_lab1),
            Write(freq_lab1),
            run_time=max(0.05, 0.98),
        )

        # Gap to 17.62
        self.wait(max(0.05, 0.96))

        # Beat 9 (17.62-20.88): subtle overlay around filter box, hold.
        overlay = SurroundingRectangle(
            filter_box,
            color=GREY,
            buff=0.28,
            stroke_width=1.5,
        )
        overlay.set_stroke(opacity=0.40)
        self.play(FadeIn(overlay), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 2.46))

        # Gap to 21.26
        self.wait(max(0.05, 0.38))

        # Beat 10 (21.26-22.62): "remember" near the filter box.
        remember_text = Text("remember", font_size=30, color=YELLOW)
        remember_text.next_to(filter_box, UP, buff=0.45)
        self.play(Write(remember_text), run_time=max(0.05, 1.36))

        # Gap to 23.34
        self.wait(max(0.05, 0.72))

        # Beat 11 (23.34-24.70): second spectrum panel appears, with before/after labels.
        self.play(Create(axis2), run_time=max(0.05, 0.30))
        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in low_bars2], lag_ratio=0.08),
            run_time=max(0.05, 0.50),
        )
        self.play(
            Write(before_label),
            Write(after_label),
            Write(sig_lab2),
            run_time=max(0.05, 0.56),
        )

        # Gap to 25.14
        self.wait(max(0.05, 0.44))

        # Beat 12 (25.14-26.56): high-frequency interference bars fade one by one.
        per_bar = 0.18
        for bar in high_bars1:
            self.play(FadeOut(bar), run_time=max(0.05, per_bar))
        self.play(output_clean.animate.set_stroke(color=WHITE, width=9), run_time=max(0.05, 0.08))
        self.play(output_clean.animate.set_stroke(color=ORANGE, width=6), run_time=max(0.05, 0.08))

        # Beat 13 (26.56-27.57): hold full scene.
        self.wait(max(0.05, 1.01))