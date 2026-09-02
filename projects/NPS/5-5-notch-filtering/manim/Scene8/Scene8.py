ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def build_prev_frame():
            left_pane = Rectangle(width=6.0, height=6.8, fill_color="#1C1E26", fill_opacity=1,
                                  stroke_color=GREY, stroke_width=1.5).shift(LEFT * 3.4)
            red_x = SVGMobject(ASSET_PATHS["x_circle"]).set_color(RED).scale_to_fit_height(3.0)
            red_x.move_to(left_pane)
            poor_text = Text("Poor Practices", font_size=24, color=RED, weight="BOLD")
            poor_text.next_to(red_x, DOWN, buff=0.2)
            left_group = VGroup(left_pane, red_x, poor_text)

            right_pane = Rectangle(width=6.0, height=6.8, fill_color="#1C1E26", fill_opacity=1,
                                   stroke_color=GREY, stroke_width=1.5).shift(RIGHT * 3.4)
            checks = VGroup(
                SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN).scale_to_fit_height(0.9),
                SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN).scale_to_fit_height(0.9),
                SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN).scale_to_fit_height(0.9),
            )
            checks.arrange(DOWN, buff=0.5).move_to(right_pane.get_center() + UP * 0.3)
            good_text = Text("Good Setup", font_size=24, color=GREEN, weight="BOLD")
            good_text.next_to(checks, DOWN, buff=0.4)
            right_group = VGroup(right_pane, checks, good_text)

            bottom_text = Text(
                "Filter residual interference, not poor practices.",
                font_size=28, color=WHITE, weight="BOLD"
            ).to_edge(DOWN, buff=0.35)

            return VGroup(left_group, right_group, bottom_text)

        def build_freq_plot():
            # plot dimensions
            plot_w = 9.5
            plot_h = 3.8
            x_min, x_max = 0, 100
            y_min, y_max = 0, 1.0

            def to_plot(x, y):
                px = (x - x_min) / (x_max - x_min) * plot_w - plot_w / 2
                py = (y - y_min) / (y_max - y_min) * plot_h - plot_h / 2
                return np.array([px, py, 0])

            # axes lines
            x_axis = Line(to_plot(x_min, 0), to_plot(x_max, 0), stroke_color=WHITE, stroke_width=2)
            y_axis = Line(to_plot(0, y_min), to_plot(0, y_max), stroke_color=WHITE, stroke_width=2)

            # axis labels
            x_label = Text("Frequency (Hz)", font_size=26, color=WHITE)
            x_label.next_to(x_axis, DOWN, buff=0.3)
            y_label = Text("Magnitude", font_size=26, color=WHITE).rotate(PI / 2)
            y_label.next_to(y_axis, LEFT, buff=0.3)

            # ticks
            x_ticks = [0, 50, 100]
            y_ticks = [0, 0.5, 1.0]
            tick_group = VGroup()
            for xt in x_ticks:
                tick = Line(to_plot(xt, -0.02), to_plot(xt, 0.02), stroke_color=WHITE, stroke_width=2)
                lbl = Text(str(xt), font_size=20, color=WHITE)
                lbl.next_to(tick, DOWN, buff=0.05)
                tick_group.add(VGroup(tick, lbl))
            for yt in y_ticks:
                tick = Line(to_plot(-0.02, yt), to_plot(0.02, yt), stroke_color=WHITE, stroke_width=2)
                lbl = Text(str(yt), font_size=20, color=WHITE)
                lbl.next_to(tick, LEFT, buff=0.05)
                tick_group.add(VGroup(tick, lbl))

            # curve
            def curve_y(x):
                return 0.65 + 0.22 * np.sin(x / 8.0) + 0.08 * np.cos(x / 2.0)

            left_x = np.linspace(x_min, 49.2, 160)
            right_x = np.linspace(50.8, x_max, 160)

            left_curve = VMobject(stroke_color=BLUE, stroke_width=4)
            left_curve.set_points_smoothly([to_plot(x, curve_y(x)) for x in left_x])
            right_curve = VMobject(stroke_color=BLUE, stroke_width=4)
            right_curve.set_points_smoothly([to_plot(x, curve_y(x)) for x in right_x])

            # gap center
            gap_y = (curve_y(49.2) + curve_y(50.8)) / 2
            gap_plot_pos = to_plot(50, gap_y)

            return VGroup(x_axis, y_axis, x_label, y_label, tick_group, left_curve, right_curve), gap_plot_pos

        def build_time_panel():
            # Time waveform panel
            tw = 5.2
            th = 2.6
            t_min, t_max = 0, 10
            v_min, v_max = -2, 2

            def to_panel(t, v):
                px = (t - t_min) / (t_max - t_min) * tw - tw / 2
                py = (v - v_min) / (v_max - v_min) * th - th / 2
                return np.array([px, py, 0])

            x_ax_line = Line(to_panel(0, 0), to_panel(10, 0), stroke_color=WHITE, stroke_width=2)
            y_ax_line = Line(to_panel(0, -2), to_panel(0, 2), stroke_color=WHITE, stroke_width=2)
            x_lab = Text("Time", font_size=18, color=WHITE).next_to(x_ax_line, DOWN, buff=0.2)
            y_lab = Text("Amplitude", font_size=18, color=WHITE).rotate(PI/2).next_to(y_ax_line, LEFT, buff=0.2)

            # ticks
            ticks = VGroup()
            for tv in range(0, 11, 5):
                tick = Line(to_panel(tv, -0.1), to_panel(tv, 0.1), stroke_color=WHITE, stroke_width=1.5)
                lbl = Text(str(tv), font_size=14, color=WHITE).next_to(tick, DOWN, buff=0.05)
                ticks.add(VGroup(tick, lbl))
            for vv in [-2, 0, 2]:
                tick = Line(to_panel(-0.1, vv), to_panel(0.1, vv), stroke_color=WHITE, stroke_width=1.5)
                lbl = Text(str(vv), font_size=14, color=WHITE).next_to(tick, LEFT, buff=0.05)
                ticks.add(VGroup(tick, lbl))

            # noisy signal
            np.random.seed(12)
            t_vals = np.linspace(0, 10, 300)
            base = 0.5 * np.sin(2 * np.pi * 0.6 * t_vals) + 0.25 * np.sin(2 * np.pi * 1.7 * t_vals + 1)
            noise = 0.35 * np.random.randn(300)
            y_vals = np.clip(base + noise, -1.8, 1.8)
            spike_idx = int(np.argmin(np.abs(t_vals - 5)))
            y_vals[spike_idx] = 1.8

            curve = VMobject(stroke_color=TEAL, stroke_width=3)
            curve.set_points_smoothly([to_panel(ti, yi) for ti, yi in zip(t_vals, y_vals)])

            panel = VGroup(x_ax_line, y_ax_line, x_lab, y_lab, ticks, curve)
            return panel

        def make_filter_card(title, desc, color):
            rect = RoundedRectangle(
                corner_radius=0.15,
                width=3.6,
                height=2.2,
                fill_color="#1A1C23",
                fill_opacity=1,
                stroke_color=color,
                stroke_width=3,
            )
            t = Text(title, font_size=24, color=color, weight="BOLD")
            t.move_to(rect.get_top() + DOWN * 0.45)
            d = Text(desc, font_size=16, color=GREY)
            d.move_to(rect.get_bottom() + UP * 0.45)
            dot = Dot(radius=0.08, color=color).move_to(rect.get_left() + RIGHT * 0.15 + UP * 0.35)
            return VGroup(rect, t, d, dot)

        # ---------- Build visuals ----------
        prev = build_prev_frame()
        freq_plot, gap_center = build_freq_plot()
        freq_plot.center()  # center the whole plot

        # gap pulse marker (circle at gap center)
        gap_pulse = Circle(radius=0.22, stroke_color=YELLOW, stroke_width=4,
                           fill_color=YELLOW, fill_opacity=0.25)
        gap_pulse.move_to(gap_center)

        # removed band
        gap_left_x = (49.2 / 100) * 9.5 - 9.5/2  # from mapping
        gap_right_x = (50.8 / 100) * 9.5 - 9.5/2
        band_width = (gap_right_x - gap_left_x) * 1.2
        band = Rectangle(width=band_width, height=3.8,
                         fill_color=RED, fill_opacity=0.35,
                         stroke_color=RED, stroke_width=2)
        band.move_to(np.array([(gap_left_x + gap_right_x)/2, 0, 0]))
        band_label = Text("removed band", font_size=20, color=RED, weight="BOLD")
        band_label.next_to(band, UP, buff=0.1)

        # dashed vertical line
        drop_line = DashedLine(
            start=np.array([(gap_left_x + gap_right_x)/2, 1.9, 0]),
            end=np.array([(gap_left_x + gap_right_x)/2, -1.9, 0]),
            dash_length=0.15, stroke_width=3, color=YELLOW
        )
        notch_freq_label = Text("50 Hz", font_size=22, color=YELLOW, weight="BOLD")
        notch_freq_label.next_to(drop_line, RIGHT, buff=0.15).shift(DOWN * 0.4)

        preserve_note = Text("Preserves other frequencies", font_size=20, color=GREEN, weight="BOLD")
        preserve_note.next_to(freq_plot, LEFT, buff=0.6).shift(UP * 0.5)
        power_note = Text("Power line: 50 / 60 Hz", font_size=20, color=YELLOW, weight="BOLD")
        power_note.next_to(freq_plot, RIGHT, buff=0.6).shift(UP * 0.5)

        # summary checkpoints
        summary_rows = VGroup(
            VGroup(
                SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN).scale_to_fit_height(0.6),
                Text("Removes a narrow frequency band", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN).scale_to_fit_height(0.6),
                Text("Targets 50 / 60 Hz power line interference", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN).scale_to_fit_height(0.6),
                Text("Preserves the rest of the signal", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        # time panel
        time_panel = build_time_panel()
        time_panel.to_edge(RIGHT, buff=0.8).shift(UP * 1.2)

        # # filter cards
        moving_card = make_filter_card("Moving Average", "Smooths random fluctuations", TEAL)
        median_card = make_filter_card("Median Filter", "Removes impulsive spikes", PURPLE)
        cards = VGroup(moving_card, median_card).arrange(RIGHT, buff=1.5).move_to(ORIGIN).shift(DOWN * 0.2)

        # ---------- timeline ----------
        # 0.00-1.56 crossfade
        self.add(prev)
        self.play(FadeOut(prev, shift=UP*0.3), FadeIn(freq_plot), run_time=max(0.05, 1.56))
        # add gap pulse after plot is visible
        self.add(gap_pulse)  # already centered
        self.wait(max(0.05, 0.0))  # no extra wait

        # 1.56-2.64 gap pulse (two pulses, each 0.54s)
        for _ in range(2):
            self.play(gap_pulse.animate.scale(1.4).set_opacity(0.5), run_time=max(0.05, 0.54))
            self.play(gap_pulse.animate.scale(1/1.4).set_opacity(1.0), run_time=max(0.05, 0.54))
        # (1.56 + 1.08 = 2.64) now gap_pulse still visible, we'll remove it next

        # 2.64-4.46: removed band with label (1.82s)
        self.play(FadeOut(gap_pulse), GrowFromCenter(band), Write(band_label), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.32))

        # 4.46-6.64: dashed line and notes (2.18s)
        self.play(Create(drop_line), FadeIn(notch_freq_label),
                  FadeIn(preserve_note), FadeIn(power_note), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.18))

        # 6.64-10.00: summary points (3.36s)
        summary_rows.next_to(freq_plot, DOWN, buff=0.6)
        self.play(Write(summary_rows), run_time=max(0.05, 2.5))
        self.wait(max(0.05, 0.86))

        # 10.00-13.00: transition to time domain (3.0s)
        freq_group = VGroup(freq_plot, band, band_label, drop_line, notch_freq_label,
                            preserve_note, power_note)
        self.play(FadeOut(summary_rows),
                  freq_group.animate.scale(0.65).move_to(LEFT * 3.5 + UP * 1.5),
                  FadeIn(time_panel), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 1.0))

        # 13.00-20.00: noisy waveform focus (7.0s)
        noise_label = Text("Random Fluctuations", font_size=18, color=YELLOW, weight="BOLD")
        impulse_label = Text("Impulsive Noise", font_size=18, color=RED, weight="BOLD")
        # find spike position on time panel
        # time panel curve at t=5, v=1.8, we approximate
        spike_point = time_panel[5][-1].get_points()[np.argmax([p[1] for p in time_panel[5][-1].get_points()])]
        # simpler: we know the peak is near t=5, v=1.8, so we compute manually: plot coords: tw=5.2, center shift?
        # We can use the same to_panel function. But we don't have direct access. We'll estimate: panel center is at (right edge, UP). Hard.
        # Instead, we'll just place impulse_label near the curve's top right.
        impulse_label.next_to(time_panel, UR, buff=0.2).shift(DOWN*0.3)
        arrow = Arrow(start=impulse_label.get_bottom(), end=impulse_label.get_bottom() + DOWN*0.5 + LEFT*0.5,
                      buff=0.1, stroke_width=2, color=RED)
        self.play(FadeIn(noise_label), FadeIn(impulse_label), FadeIn(arrow), run_time=max(0.05, 2.0))
        self.play(Indicate(time_panel[5][-1], color=YELLOW, scale_factor=1.05), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 3.0))

        # 20.00-27.00: introduce two filters (7.0s)
        self.play(FadeOut(freq_group), FadeOut(time_panel), FadeOut(noise_label),
                  FadeOut(impulse_label), FadeOut(arrow), run_time=max(0.05, 1.0))
        header = Text("Next: Time-Domain Filters", font_size=30, color=WHITE, weight="BOLD")
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header), run_time=max(0.05, 1.0))
        self.play(GrowFromCenter(moving_card), GrowFromCenter(median_card), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 3.5))

        # 27.00-34.00: moving average highlight (7.0s)
        moving_detail = Text("Averages neighboring samples to smooth noise",
                             font_size=18, color=TEAL)
        moving_detail.next_to(moving_card, DOWN, buff=0.25)
        self.play(Indicate(moving_card, color=TEAL, scale_factor=1.08), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.5))
        self.play(FadeIn(moving_detail), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 2.0))

        # 34.00-41.00: median highlight (7.0s)
        median_detail = Text("Replaces samples with the median to remove spikes",
                             font_size=18, color=PURPLE)
        median_detail.next_to(median_card, DOWN, buff=0.25)
        self.play(Indicate(median_card, color=PURPLE, scale_factor=1.08), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.5))
        self.play(FadeIn(median_detail), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 2.0))

        # 41.00-46.00: closing (5.0s)
        self.play(FadeOut(moving_detail), FadeOut(median_detail), run_time=max(0.05, 1.0))
        closing = Text("Time-domain filters for cleaner recordings", font_size=24, color=GREY)
        closing.next_to(cards, DOWN, buff=0.8)
        self.play(FadeIn(closing), run_time=max(0.05, 1.5))
        self.play(Wiggle(moving_card, scale_value=1.03),
                  Wiggle(median_card, scale_value=1.03), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.0))

        # 46.00-49.50: hold (3.5s)
        self.wait(max(0.05, 3.5))