ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def make_nonstationary_trace(amp=0.75, y_center=-0.8):
            x = np.linspace(-6, 6, 1200)
            dx = x[1] - x[0]
            freq = 2.0 + 2.5*np.sin(np.pi*x/3) + 0.9*np.sin(2.7*np.pi*x/2.5)
            phase = 2*np.pi*np.cumsum(freq)*dx
            y = y_center + amp*np.sin(phase) + 0.12*np.sin(2.3*phase)
            points = [np.array([xi, yi, 0]) for xi, yi in zip(x, y)]
            vm = VMobject(stroke_color=TEAL, stroke_width=4)
            vm.set_points_smoothly(points)
            return vm

        def make_exaggerated_trace():
            x = np.linspace(-6, 6, 1200)
            dx = x[1] - x[0]
            freq = 2.0 + 4.0*np.sin(np.pi*x/2.5) + 1.4*np.sin(3*np.pi*x/2)
            phase = 2*np.pi*np.cumsum(freq)*dx
            y = -0.8 + 1.1*np.sin(phase) + 0.2*np.sin(2.5*phase)
            points = [np.array([xi, yi, 0]) for xi, yi in zip(x, y)]
            vm = VMobject(stroke_color=TEAL, stroke_width=4)
            vm.set_points_smoothly(points)
            return vm

        def make_short_signal():
            x = np.linspace(-1.5, 1.5, 400)
            y = 0.3 + 0.5*np.sin(3*np.pi*x) + 0.15*np.sin(9*np.pi*x)
            points = [np.array([xi, yi, 0]) for xi, yi in zip(x, y)]
            vm = VMobject(stroke_color=TEAL, stroke_width=4)
            vm.set_points_smoothly(points)
            return vm

        def make_eeg_trace(left_x, right_x, y_center, seed, amp=0.35):
            x = np.linspace(left_x, right_x, 500)
            np.random.seed(seed)
            base = (
                0.25*np.sin(7*np.pi*(x-left_x)/(right_x-left_x))
                + 0.15*np.sin(20*np.pi*(x-left_x)/(right_x-left_x))
                + 0.08*np.random.randn(len(x))
            )
            y = y_center + base
            points = [np.array([xi, yi, 0]) for xi, yi in zip(x, y)]
            vm = VMobject(stroke_color=GREY_B, stroke_width=3)
            vm.set_points_smoothly(points)
            return vm

        def make_alpha_trace(left_x, right_x, y_center, amp=0.45):
            x = np.linspace(left_x, right_x, 600)
            y = y_center + amp*np.sin(2*np.pi*10*(x-left_x)/(right_x-left_x))
            points = [np.array([xi, yi, 0]) for xi, yi in zip(x, y)]
            vm = VMobject(stroke_color=TEAL, stroke_width=5)
            vm.set_points_smoothly(points)
            return vm

        def make_bracket(left_x, right_x, y, label_text, color):
            hline = Line(np.array([left_x, y, 0]), np.array([right_x, y, 0]), color=color, stroke_width=3)
            l_tick = Line(np.array([left_x, y-0.15, 0]), np.array([left_x, y+0.15, 0]), color=color, stroke_width=3)
            r_tick = Line(np.array([right_x, y-0.15, 0]), np.array([right_x, y+0.15, 0]), color=color, stroke_width=3)
            label = Text(label_text, font_size=26, color=color).next_to(hline, UP, buff=0.1)
            return VGroup(hline, l_tick, r_tick, label)

        # Beat 1: title
        title = Text("Nonstationary Signals", font_size=72, color=WHITE, weight=BOLD).move_to(ORIGIN)
        self.play(FadeIn(title, scale=1.03), run_time=max(0.05, 1.06))
        self.wait(max(0.05, 0.62))

        # Beat 2: signal trace draws
        signal_trace = make_nonstationary_trace()
        self.play(FadeOut(title), Create(signal_trace), run_time=max(0.05, 1.10))

        # Beat 3: label above, more exaggerated oscillations
        freq_label = Text("Frequency changes over time", font_size=36, color=YELLOW).next_to(signal_trace, UP, buff=0.4)
        exaggerated_trace = make_exaggerated_trace()
        self.play(FadeIn(freq_label, shift=UP*0.2), Transform(signal_trace, exaggerated_trace), run_time=max(0.05, 1.82))
        self.wait(max(0.05, 0.56))

        # Beat 4: time shaded region
        time_band = Rectangle(width=12, height=0.5, fill_color=BLUE, fill_opacity=0.25, stroke_color=BLUE, stroke_width=2)
        time_band.move_to(DOWN*2.2)
        time_label = Text("Time", font_size=28, color=GREY).move_to(time_band.get_center())
        self.play(FadeOut(freq_label), GrowFromCenter(time_band), FadeIn(time_label), run_time=max(0.05, 2.34))

        # Beat 5: time tick travels along axis
        tick_line = Line(UP*0.35, DOWN*0.35, color=ORANGE, stroke_width=5).move_to(np.array([-6, -2.2, 0]))
        tick_label = Text("time", font_size=24, color=ORANGE).next_to(tick_line, DOWN, buff=0.1)
        tick_group = VGroup(tick_line, tick_label)
        self.play(FadeIn(tick_group, shift=UP*0.2), run_time=max(0.05, 0.4))
        self.play(tick_group.animate.shift(RIGHT*11.8), run_time=max(0.05, 2.32))
        self.wait(max(0.05, 0.74))

        # Beat 6: Fourier Transform text
        diagram_group = VGroup(signal_trace, time_band, time_label, tick_group)
        ft_title = Text("Fourier Transform", font_size=64, color=WHITE, weight=BOLD).move_to(LEFT*3 + UP*0.6)
        ft_subtitle = Text("Which frequencies?", font_size=40, color=YELLOW).next_to(ft_title, DOWN, buff=0.35)
        ft_group = VGroup(ft_title, ft_subtitle)
        self.play(FadeOut(diagram_group), FadeIn(ft_group), run_time=max(0.05, 3.84))
        self.wait(max(0.05, 0.84))

        # Beat 7: split visual with spectrum + ? + clock
        left_signal = make_short_signal().move_to(LEFT*3.4 + UP*0.2)

        bar_heights = [0.6, 1.3, 2.0, 1.3, 0.6]
        bar_colors = [BLUE, TEAL, GREEN, ORANGE, PURPLE]
        spectrum_bars_list = []
        for h, c in zip(bar_heights, bar_colors):
            bar = Rectangle(width=0.6, height=h, fill_color=c, fill_opacity=1, stroke_width=0)
            spectrum_bars_list.append(bar)
        bars_group = VGroup(*spectrum_bars_list).arrange(RIGHT, buff=0.4)
        baseline = Line(LEFT*2.6, RIGHT*2.6, color=WHITE, stroke_width=3)
        bars_group.next_to(baseline, UP, buff=0)
        spectrum_group = VGroup(bars_group, baseline).move_to(RIGHT*3.4 + UP*0.4)

        question_symbol = Text("?", font_size=96, color=RED, weight=BOLD).next_to(spectrum_group, UP, buff=0.35)
        clock_icon = SVGMobject(
            ASSET_PATHS["stopwatch"],
            height=0.9,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).next_to(question_symbol, RIGHT, buff=0.5)

        self.play(FadeOut(ft_group), Create(left_signal), FadeIn(baseline), run_time=max(0.05, 1.0))
        self.play(*[GrowFromEdge(bar, DOWN) for bar in spectrum_bars_list], run_time=max(0.05, 1.5))
        self.play(FadeIn(question_symbol, shift=UP*0.2), FadeIn(clock_icon, shift=RIGHT*0.2), run_time=max(0.05, 0.9))
        self.play(clock_icon.animate.set_color(GREY).set_opacity(0.6), run_time=max(0.05, 1.78))
        self.wait(max(0.05, 0.70))

        # Beat 8: When?, ROI, timing essential
        when_text = Text("When?", font_size=64, color=ORANGE, weight=BOLD).next_to(spectrum_group, DOWN, buff=0.7)
        roi_box = Rectangle(width=1.5, height=1.4, color=ORANGE, fill_color=ORANGE, fill_opacity=0.18, stroke_width=3)
        roi_box.move_to(left_signal.get_center() + RIGHT*0.1 + UP*0.1)
        roi_q = Text("?", font_size=36, color=ORANGE).next_to(roi_box, RIGHT, buff=0.15)
        timing_label = Text("Timing is essential", font_size=36, color=YELLOW).to_edge(DOWN, buff=0.6)

        self.play(
            FadeIn(when_text, shift=UP*0.1),
            FadeIn(roi_box),
            FadeIn(roi_q),
            FadeIn(timing_label),
            run_time=max(0.05, 2.0),
        )
        self.play(when_text.animate.scale(1.25), run_time=max(0.05, 0.7))
        self.play(when_text.animate.scale(0.8), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.56))
        self.wait(max(0.05, 0.80))

        # Beat 9: EEG view
        split_group = VGroup(
            left_signal,
            spectrum_group,
            question_symbol,
            clock_icon,
            when_text,
            roi_box,
            roi_q,
            timing_label,
        )

        timeline = Line(LEFT*6 + DOWN*1.0, RIGHT*6 + DOWN*1.0, color=WHITE, stroke_width=3)
        ticks = VGroup(*[
            Line(np.array([i, -1.0, 0]) + DOWN*0.08, np.array([i, -1.0, 0]) - DOWN*0.08, color=GREY_B, stroke_width=2)
            for i in range(-6, 7)
        ])
        eeg_timeline = VGroup(timeline, ticks)
        brain = SVGMobject(
            ASSET_PATHS["brain"],
            height=1.4,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(np.array([0, 1.8, 0]))
        open_trace = make_eeg_trace(-5.2, 0.2, 0.5, seed=1)
        closed_base = make_eeg_trace(0.8, 5.2, 0.5, seed=2)
        eeg_group = VGroup(eeg_timeline, brain, open_trace, closed_base)

        self.play(FadeOut(split_group), FadeIn(eeg_group), run_time=max(0.05, 1.5))
        self.play(brain.animate.scale(1.08), run_time=max(0.05, 1.0))
        self.play(brain.animate.scale(1/1.08), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.48))
        self.wait(max(0.05, 0.74))

        # Beat 10: eyes open/closed brackets and alpha oscillation
        eyes_open_bracket = make_bracket(-5.2, 0.2, 1.1, "Eyes open", BLUE)
        eyes_closed_bracket = make_bracket(0.8, 5.2, 1.1, "Eyes closed", PURPLE)
        alpha_trace = make_alpha_trace(0.8, 5.2, 0.5)

        self.play(FadeIn(eyes_open_bracket, shift=UP*0.2), run_time=max(0.05, 1.0))
        self.play(FadeIn(eyes_closed_bracket, shift=UP*0.2), run_time=max(0.05, 1.0))
        self.play(Create(alpha_trace), closed_base.animate.set_opacity(0.5), run_time=max(0.05, 2.18))
        self.wait(max(0.05, 0.80))

        # Beat 11: Why frequencies? alpha highlight
        which_freq_caption = Text("Which frequencies?", font_size=44, color=YELLOW).to_edge(UP, buff=0.5)
        alpha_overlay = Rectangle(width=4.4, height=1.1, fill_color=TEAL, fill_opacity=0.2, stroke_color=TEAL, stroke_width=0)
        alpha_overlay.move_to(np.array([3.0, 0.5, 0]))

        self.play(FadeIn(which_freq_caption), FadeIn(alpha_overlay), run_time=max(0.05, 2.0))
        self.play(alpha_overlay.animate.set_opacity(0.5), run_time=max(0.05, 1.0))
        self.play(alpha_overlay.animate.set_opacity(0.2), run_time=max(0.05, 1.36))
        self.wait(max(0.05, 0.64))

        # Beat 12: But when? onset pulse
        but_when_caption = Text("But when?", font_size=44, color=ORANGE).to_edge(UP, buff=0.5)
        onset_point = np.array([0.8, 0.5, 0])
        onset_dot = Dot(onset_point, radius=0.08, color=RED)
        onset_ring = Circle(radius=0.35, color=RED, stroke_width=4).move_to(onset_point)

        self.play(
            FadeOut(which_freq_caption),
            FadeIn(but_when_caption),
            FadeIn(onset_dot),
            FadeIn(onset_ring),
            run_time=max(0.05, 1.0),
        )
        self.play(onset_ring.animate.scale(2.5).set_opacity(0), run_time=max(0.05, 0.7))
        onset_ring.set_opacity(1)
        onset_ring.scale(1/2.5)
        self.play(onset_ring.animate.scale(2.5).set_opacity(0), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.64))
        self.wait(max(0.05, 0.80))

        # Beat 13: method needed text and repeated pulse
        method_text = Text("Method needed: time and frequency simultaneously.", font_size=36, color=WHITE)
        method_text.to_edge(DOWN, buff=0.7)

        self.play(FadeIn(method_text, shift=UP*0.2), run_time=max(0.05, 1.2))
        self.play(alpha_overlay.animate.set_opacity(0.5), run_time=max(0.05, 0.6))
        self.play(alpha_overlay.animate.set_opacity(0.2), run_time=max(0.05, 0.6))
        onset_ring.set_opacity(1)
        onset_ring.scale(1/2.5)
        self.play(onset_ring.animate.scale(2.5).set_opacity(0), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 2.08))
        self.wait(max(0.05, 1.04))

        # Beat 14: Short-Time Fourier Transform title
        eeg_view_all = VGroup(
            eeg_group,
            eyes_open_bracket,
            eyes_closed_bracket,
            alpha_trace,
            alpha_overlay,
            but_when_caption,
            method_text,
            onset_dot,
            onset_ring,
        )
        stft_full = Text("Short-Time Fourier Transform", font_size=68, color=WHITE, weight=BOLD).move_to(ORIGIN)
        stft_box = SurroundingRectangle(stft_full, color=YELLOW, buff=0.25, stroke_width=3)

        self.play(
            eeg_view_all.animate.set_opacity(0.15),
            FadeIn(stft_full, shift=UP*0.2),
            FadeIn(stft_box),
            run_time=max(0.05, 3.80),
        )

        # Beat 15: anticipating abbreviation
        hint_text = Text("commonly abbreviated as", font_size=30, color=GREY).next_to(stft_full, DOWN, buff=0.45)
        self.play(FadeIn(hint_text, shift=UP*0.1), run_time=max(0.05, 1.52))
        self.wait(max(0.05, 0.70))

        # Beat 16: STFT abbreviation
        stft_abbr = Text("STFT", font_size=110, color=YELLOW, weight=BOLD).move_to(ORIGIN)
        self.play(FadeOut(stft_full, stft_box, hint_text), FadeIn(stft_abbr, shift=UP*0.2), run_time=max(0.05, 1.2))
        self.play(stft_abbr.animate.scale(1.08), run_time=max(0.05, 0.7))
        self.play(stft_abbr.animate.scale(0.9259), run_time=max(0.05, 0.87))