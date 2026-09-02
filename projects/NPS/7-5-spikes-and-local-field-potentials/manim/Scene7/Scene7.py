ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----- helpers -----
        def v2(x, y):
            return np.array([x, y, 0.0])

        def make_neuron(center, radius=0.30, fill_color=GREY, fill_opacity=0.7):
            soma = Circle(
                radius=radius,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_color=GREY_B,
                stroke_width=2.5,
            ).move_to(center)
            dirs = [
                v2(1.0, 0.8), v2(0.2, -1.0), v2(-0.9, 0.4),
                v2(-0.4, -0.8), v2(0.7, -0.5), v2(-0.7, 0.7)
            ]
            dendrites = VGroup()
            for d in dirs:
                d = d / np.linalg.norm(d)
                dendrites.add(
                    Line(center + d * radius, center + d * (radius + 0.25),
                         color=GREY_B, stroke_width=2.0)
                )
            return VGroup(soma, dendrites)

        # ----- 1. [0.00-4.82] fade in neuron, ticks, title -----
        title = Text("Neural Coding", font_size=55, color=WHITE).to_edge(UP, buff=0.3)
        neuron = make_neuron(v2(0, 1.6))
        time_axis = VGroup()
        axis_line = Line(v2(-5.0, -0.5), v2(5.0, -0.5), color=GREY_B, stroke_width=2.5)
        time_axis.add(axis_line)
        for x in np.linspace(-4.5, 4.5, 11):
            time_axis.add(Line(v2(x, -0.5), v2(x, -0.35), color=GREY_B, stroke_width=1.8))
        time_axis.set_opacity(0.7)

        self.play(FadeIn(neuron), run_time=max(0.05, 1.5))
        self.play(Create(time_axis), run_time=max(0.05, 1.0))
        self.play(FadeIn(title), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 4.82 - (1.5 + 1.0 + 1.0)))

        # ----- 2. [4.82-8.00] neuron pulse + caption -----
        pulse_clock = ValueTracker(0)

        def update_neuron(mob):
            t = pulse_clock.get_value()
            val = 0.5 + 0.4 * np.sin(2 * np.pi * t / 1.2)
            mob.set_opacity(max(0.2, min(0.9, val)))

        neuron.add_updater(update_neuron)
        caption_on_off = Text("not simply on / off", font_size=28, color=YELLOW)
        caption_on_off.next_to(neuron, DOWN, buff=0.6)

        self.play(FadeIn(caption_on_off), pulse_clock.animate.set_value(0.25), run_time=max(0.05, 0.25))
        self.play(pulse_clock.animate.set_value(1.45), run_time=max(0.05, 1.20))
        self.play(FadeOut(caption_on_off), pulse_clock.animate.set_value(1.70), run_time=max(0.05, 0.25))
        self.play(pulse_clock.animate.set_value(3.18), run_time=max(0.05, 1.48))
        neuron.clear_updaters()
        neuron.set_opacity(0.7)

        # ----- 3-6. heading + four characteristic icons -----
        heading = Text("Information represented by:", font_size=32, color=WHITE).move_to(v2(0, 0.3))

        def make_freq_icon():
            line = Line(LEFT * 0.6, RIGHT * 0.6, color=GREY_B, stroke_width=2)
            ticks = VGroup()
            xs = [-0.45, -0.25, -0.05, 0.15, 0.35, 0.5]
            hs = [0.15, 0.25, 0.18, 0.3, 0.22, 0.35]
            for x, h in zip(xs, hs):
                ticks.add(Line(v2(x, 0), v2(x, h), color=GREY_B, stroke_width=2))
            return VGroup(line, ticks)

        def make_timing_icon():
            line = Line(LEFT * 0.5, RIGHT * 0.5, color=GREY_B, stroke_width=2)
            t1 = Line(v2(-0.2, 0), v2(-0.2, 0.3), color=GREY_B, stroke_width=2)
            t2 = Line(v2(0.2, 0), v2(0.2, 0.3), color=GREY_B, stroke_width=2)
            return VGroup(line, t1, t2)

        def make_patterns_icon():
            line = Line(LEFT * 0.8, RIGHT * 0.8, color=GREY_B, stroke_width=2)
            ticks = VGroup()
            xs = [-0.42, -0.36, -0.30, 0.18, 0.24, 0.30]
            for x in xs:
                ticks.add(Line(v2(x, 0), v2(x, 0.3), color=GREY_B, stroke_width=2))
            return VGroup(line, ticks)

        def make_population_icon():
            dots = VGroup()
            lit = {(0, 0), (0, 2), (1, 1), (2, 1), (2, 3)}
            for r in range(3):
                for c in range(4):
                    is_lit = (r, c) in lit
                    dot = Dot(radius=0.06, color=BLUE if is_lit else GREY)
                    dot.set_fill(BLUE if is_lit else GREY, opacity=1 if is_lit else 0.3)
                    dots.add(dot)
            dots.arrange_in_grid(rows=3, cols=4, buff=0.08)
            return dots

        x_slots = [-4.1, -1.5, 1.5, 4.1]
        y_icons = -1.6
        icon_groups = {}

        self.wait(max(0.05, 0.48))  # 8.00 -> 8.48
        self.play(FadeIn(heading), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 11.78 - (8.48 + 0.6)))  # 9.08 -> 11.78

        freq_icon = make_freq_icon()
        freq_label = Text("frequency", font_size=20, color=YELLOW)
        freq_group = VGroup(freq_icon, freq_label).arrange(DOWN, buff=0.1)
        freq_group.move_to(v2(x_slots[0], y_icons))
        self.play(FadeIn(freq_group), run_time=max(0.05, 0.6))
        icon_groups["freq"] = freq_group
        self.wait(max(0.05, 13.98 - (11.78 + 0.6)))  # 12.38 -> 13.98

        timing_icon = make_timing_icon()
        timing_label = Text("spike timing", font_size=20, color=YELLOW)
        timing_group = VGroup(timing_icon, timing_label).arrange(DOWN, buff=0.1)
        timing_group.move_to(v2(x_slots[1], y_icons))
        timing_rect = SurroundingRectangle(timing_group, color=WHITE, buff=0.12, stroke_width=3)
        self.play(FadeIn(timing_group), FadeIn(timing_rect), run_time=max(0.05, 0.30))
        icon_groups["timing"] = timing_group
        self.play(timing_rect.animate.scale(1.15), run_time=max(0.05, 0.35))
        self.play(timing_rect.animate.scale(1 / 1.15), run_time=max(0.05, 0.35))
        self.play(FadeOut(timing_rect), run_time=max(0.05, 0.20))  # 15.18

        patterns_icon = make_patterns_icon()
        patterns_label = Text("spike patterns", font_size=20, color=YELLOW)
        patterns_group = VGroup(patterns_icon, patterns_label).arrange(DOWN, buff=0.1)
        patterns_group.move_to(v2(x_slots[2], y_icons))
        patterns_rect = SurroundingRectangle(patterns_group, color=WHITE, buff=0.12, stroke_width=3)
        self.play(FadeIn(patterns_group), FadeIn(patterns_rect), run_time=max(0.05, 0.30))  # 16.00
        icon_groups["patterns"] = patterns_group
        self.play(patterns_rect.animate.scale(1.15), run_time=max(0.05, 0.50))
        self.play(patterns_rect.animate.scale(1 / 1.15), run_time=max(0.05, 0.48))
        self.play(FadeOut(patterns_rect), run_time=max(0.05, 0.20))  # ~17.18

        population_icon = make_population_icon()
        population_label = Text("population activity", font_size=20, color=YELLOW)
        population_group = VGroup(population_icon, population_label).arrange(DOWN, buff=0.1)
        population_group.move_to(v2(x_slots[3], y_icons))
        population_rect = SurroundingRectangle(population_group, color=WHITE, buff=0.12, stroke_width=3)
        self.play(FadeIn(population_group), FadeIn(population_rect), run_time=max(0.05, 0.30))  # 18.08
        icon_groups["population"] = population_group
        self.play(population_rect.animate.scale(1.15), run_time=max(0.05, 0.65))
        self.play(population_rect.animate.scale(1 / 1.15), run_time=max(0.05, 0.61))
        self.play(FadeOut(population_rect), run_time=max(0.05, 0.40))  # ~19.74

        self.wait(max(0.05, 20.64 - 19.74))  # 0.90

        # ----- 7. [20.64-24.34] expand frequency icon to firing rate panel -----
        self.play(FadeOut(icon_groups["timing"]), FadeOut(icon_groups["patterns"]),
                  FadeOut(icon_groups["population"]), run_time=max(0.05, 0.5))
        self.play(FadeOut(icon_groups["freq"]), run_time=max(0.05, 0.3))  # 21.14

        panel_title = Text("Firing Rate", font_size=36, color=WHITE).move_to(v2(0, 1.8))
        time_axis_line = Line(v2(-4.5, 0.4), v2(4.5, 0.4), color=WHITE, stroke_width=2)

        region_A = Rectangle(width=2.3, height=0.8, fill_color=BLUE, fill_opacity=0.15,
                             stroke_color=BLUE, stroke_width=2).move_to(v2(-1.7, -0.15))
        region_B = Rectangle(width=2.3, height=0.8, fill_color=ORANGE, fill_opacity=0.15,
                             stroke_color=ORANGE, stroke_width=2).move_to(v2(1.7, -0.15))
        cond_A_label = Text("Condition A", font_size=20, color=BLUE).move_to(v2(-1.7, 0.85))
        cond_B_label = Text("Condition B", font_size=20, color=ORANGE).move_to(v2(1.7, 0.85))

        condA_spikes = VGroup()
        for x in [-2.8, -2.0, -1.2]:
            condA_spikes.add(Line(v2(x, -0.45), v2(x, 0.35), color=BLUE, stroke_width=3))

        condB_spikes = VGroup()
        for x in np.linspace(1.1, 3.3, 12):
            condB_spikes.add(Line(v2(x, -0.45), v2(x, 0.35), color=ORANGE, stroke_width=3))

        caption_more = Text("more spikes = higher firing rate", font_size=24, color=YELLOW)
        caption_more.next_to(VGroup(region_A, region_B), DOWN, buff=0.35)

        self.play(FadeIn(panel_title), FadeIn(time_axis_line), run_time=max(0.05, 0.4))
        self.play(FadeIn(region_A), FadeIn(region_B), FadeIn(cond_A_label), FadeIn(cond_B_label), run_time=max(0.05, 0.6))
        self.play(FadeIn(condA_spikes), FadeIn(condB_spikes), run_time=max(0.05, 0.6))
        self.play(FadeIn(caption_more), run_time=max(0.05, 0.6))

        # total used after icon fade: 0.4+0.6+0.6+0.6 = 2.2, plus 0.3 (freq fade) = 2.5, plus 0.5 (first fade out) = 3.0, starting at 20.64 -> 23.64
        # remaining until 24.34: 0.70
        self.wait(max(0.05, 24.34 - (20.64 + 0.5 + 0.3 + 0.4 + 0.6 + 0.6 + 0.6)))

        # ----- 8. condition highlights + three small contextual icons -----
        # 24.34 -> 25.10 wait, then at 25.40 highlight A
        self.wait(max(0.05, 0.30))  # 24.34 -> 24.64? Wait I computed event at 25.40, not 25.10.
        # Actually beat8 says [25.10-31.70] but the first event is at 25.40. We'll wait until 25.40.
        # From 24.34 to 25.40 is 1.06 seconds.
        self.wait(max(0.05, 25.40 - 24.34))  # 1.06

        # Condition A highlight (25.40-27.74 = 2.34s)
        condA_overlay = Rectangle(width=2.3, height=0.8, fill_color=BLUE, fill_opacity=0.35,
                                  stroke_width=0).move_to(region_A)
        self.play(FadeIn(condA_overlay), run_time=max(0.05, 0.3))
        # pulse spikes A three times, each pulse 0.78s: scale up 0.39, scale down 0.39
        spike_A_copy = condA_spikes.copy()
        for _ in range(3):
            self.play(spike_A_copy.animate.scale(1.15).set_color(YELLOW), run_time=max(0.05, 0.39))
            self.play(spike_A_copy.animate.scale(1 / 1.15).set_color(BLUE), run_time=max(0.05, 0.39))
        self.play(FadeOut(condA_overlay), run_time=max(0.05, 0.2))  # ends ~27.74

        # Condition B highlight (27.74-28.94 = 1.20s)
        condB_overlay = Rectangle(width=2.3, height=0.8, fill_color=ORANGE, fill_opacity=0.35,
                                  stroke_width=0).move_to(region_B)
        self.play(FadeIn(condB_overlay), run_time=max(0.05, 0.2))
        spike_B_copy = condB_spikes.copy()
        self.play(spike_B_copy.animate.scale(1.15).set_color(YELLOW), run_time=max(0.05, 0.4))
        self.play(spike_B_copy.animate.scale(1 / 1.15).set_color(ORANGE), run_time=max(0.05, 0.4))
        self.play(FadeOut(condB_overlay), run_time=max(0.05, 0.2))  # ends ~28.94

        # wait until 29.70 for difference bracket
        self.wait(max(0.05, 29.70 - 28.94))

        bracket = VGroup(
            Line(v2(-1.7, -0.8), v2(-1.7, -1.3), color=WHITE, stroke_width=2),
            Line(v2(1.7, -0.8), v2(1.7, -1.3), color=WHITE, stroke_width=2),
            Line(v2(-1.7, -1.3), v2(1.7, -1.3), color=WHITE, stroke_width=2)
        )
        bracket_label = Text("difference in firing rate", font_size=22, color=YELLOW)
        bracket_label.next_to(bracket, DOWN, buff=0.15)
        self.play(FadeIn(bracket), FadeIn(bracket_label), run_time=max(0.05, 0.6))

        # wait until 32.88
        self.wait(max(0.05, 32.88 - (29.70 + 0.6)))

        # stimulus checkerboard near Condition A
        checker = VGroup()
        for i in range(2):
            for j in range(2):
                sq = Square(side_length=0.12, fill_color=GREY if (i + j) % 2 == 0 else GREY_B,
                            fill_opacity=1, stroke_width=0)
                sq.shift(v2((j - 0.5) * 0.25, (i - 0.5) * 0.25))
                checker.add(sq)
        checker.move_to(region_A.get_bottom() + v2(0, -0.5))
        self.play(FadeIn(checker), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 0.3))
        self.play(FadeOut(checker), run_time=max(0.05, 0.2))

        # wait until 33.72
        self.wait(max(0.05, 33.72 - (32.88 + 0.2 + 0.3 + 0.2)))

        # movement arrow
        movement_arrow = Arrow(LEFT, RIGHT, color=GREY, stroke_width=3, buff=0)
        movement_arrow.scale_to_fit_width(0.6)
        movement_arrow.next_to(region_A, DOWN, buff=0.55)
        self.play(FadeIn(movement_arrow), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 0.3))
        self.play(FadeOut(movement_arrow), run_time=max(0.05, 0.2))

        # wait until 35.04
        self.wait(max(0.05, 35.04 - (33.72 + 0.2 + 0.3 + 0.2)))

        # cloud icon (behavioral state)
        cloud = VGroup(
            Circle(radius=0.12, color=GREY, fill_color=GREY, fill_opacity=1, stroke_width=0).shift(v2(-0.1, 0)),
            Circle(radius=0.15, color=GREY, fill_color=GREY, fill_opacity=1, stroke_width=0).shift(v2(0.05, 0.05)),
            Circle(radius=0.12, color=GREY, fill_color=GREY, fill_opacity=1, stroke_width=0).shift(v2(0.2, 0))
        )
        cloud.next_to(region_A, DOWN, buff=1.0)
        self.play(FadeIn(cloud), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 0.3))
        self.play(FadeOut(cloud), run_time=max(0.05, 0.2))

        # wait until 36.32 (start beat9)
        self.wait(max(0.05, 36.32 - (35.04 + 0.2 + 0.3 + 0.2)))

        # ----- 9. [36.32-42.84] bar chart -----
        # fade out firing rate panel elements (except maybe keep title? let's fade all relevant)
        old_firing_elements = VGroup(panel_title, time_axis_line, region_A, region_B,
                                     cond_A_label, cond_B_label, condA_spikes, condB_spikes,
                                     caption_more, bracket, bracket_label)
        self.play(FadeOut(old_firing_elements), run_time=max(0.05, 0.6))

        # bar chart
        bar_axis = Line(v2(-2.5, -0.8), v2(2.5, -0.8), color=GREY_B, stroke_width=2)
        bar_left = Rectangle(width=0.8, height=0.8, fill_color=BLUE, fill_opacity=0.8,
                             stroke_color=BLUE, stroke_width=2)
        bar_left.move_to(v2(-1.2, -0.8 + 0.4))  # bottom at -0.8
        bar_right = Rectangle(width=0.8, height=2.4, fill_color=ORANGE, fill_opacity=0.8,
                              stroke_color=ORANGE, stroke_width=2)
        bar_right.move_to(v2(1.2, -0.8 + 1.2))

        label_left = Text("Condition A — 3 spikes", font_size=20, color=BLUE)
        label_left.next_to(bar_left, DOWN, buff=0.15)
        label_right = Text("Condition B — 12 spikes", font_size=20, color=ORANGE)
        label_right.next_to(bar_right, DOWN, buff=0.15)

        brace = Brace(VGroup(bar_left, bar_right), direction=UP)
        brace_label = Text("compare firing rates across conditions", font_size=22, color=YELLOW)
        brace_label.next_to(brace, UP, buff=0.1)

        time_window_arrow = Arrow(v2(-2.5, -1.6), v2(2.5, -1.6), color=GREY, stroke_width=2, buff=0.0)
        time_window_label = Text("defined time window", font_size=20, color=GREY)
        time_window_label.next_to(time_window_arrow, DOWN, buff=0.1)

        self.play(FadeIn(bar_axis), run_time=max(0.05, 0.3))
        self.play(GrowFromEdge(bar_left, DOWN), FadeIn(label_left), run_time=max(0.05, 0.5))
        self.play(GrowFromEdge(bar_right, DOWN), FadeIn(label_right), run_time=max(0.05, 0.5))
        self.play(FadeIn(brace), FadeIn(brace_label), run_time=max(0.05, 0.6))
        self.play(FadeIn(time_window_arrow), FadeIn(time_window_label), run_time=max(0.05, 0.5))

        # hold until 42.84
        self.wait(max(0.05, 42.84 - (36.32 + 0.6 + 0.3 + 0.5 + 0.5 + 0.6 + 0.5)))

        # ----- 10. [43.58-49.30] same rate, different timing -----
        # fade out bar chart
        bar_group = VGroup(bar_axis, bar_left, bar_right, label_left, label_right,
                           brace, brace_label, time_window_arrow, time_window_label)
        self.play(FadeOut(bar_group), run_time=max(0.05, 0.5))

        # same-rate panel
        same_title = Text("Same rate, different timing", font_size=36, color=WHITE)
        same_title.move_to(v2(0, 2.2))

        top_axis = Line(v2(-3, 0.5), v2(3, 0.5), color=WHITE, stroke_width=2)
        bottom_axis = Line(v2(-3, -1.0), v2(3, -1.0), color=WHITE, stroke_width=2)

        # top train: 5 evenly spaced ticks
        top_ticks = VGroup()
        for x in [-2.5, -1.25, 0, 1.25, 2.5]:
            top_ticks.add(Line(v2(x, 0.1), v2(x, 0.8), color=BLUE, stroke_width=3))
        top_label = Text("5 spikes", font_size=20, color=BLUE)
        top_label.next_to(top_axis, UP, buff=0.15)

        # bottom train: clustered 3 + 2, with dimmed gap between
        bottom_ticks = VGroup()
        for x in [-2.8, -2.6, -2.4, 1.9, 2.1]:
            bottom_ticks.add(Line(v2(x, -1.4), v2(x, -0.7), color=ORANGE, stroke_width=3))
        bottom_label = Text("5 spikes", font_size=20, color=ORANGE)
        bottom_label.next_to(bottom_axis, DOWN, buff=0.15)

        gap_zone = Rectangle(width=3.2, height=0.35, fill_color=GREY, fill_opacity=0.3,
                             stroke_width=0).move_to(v2(0.2, -1.05))

        self.play(FadeIn(same_title), run_time=max(0.05, 0.4))
        self.play(FadeIn(top_axis), FadeIn(bottom_axis), run_time=max(0.05, 0.4))
        self.play(FadeIn(top_ticks), FadeIn(top_label), run_time=max(0.05, 0.8))
        self.play(FadeIn(bottom_ticks), FadeIn(bottom_label), FadeIn(gap_zone), run_time=max(0.05, 0.8))

        # wait until 47.92
        self.wait(max(0.05, 47.92 - (43.58 + 0.5 + 0.4 + 0.4 + 0.8 + 0.8)))

        # count badge flash
        badge_5_top = Text("5", font_size=26, color=YELLOW).next_to(top_axis, RIGHT, buff=0.2)
        badge_5_bottom = Text("5", font_size=26, color=YELLOW).next_to(bottom_axis, RIGHT, buff=0.2)
        self.play(FadeIn(badge_5_top), FadeIn(badge_5_bottom), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.5))
        self.play(FadeOut(badge_5_top), FadeOut(badge_5_bottom), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 49.30 - (47.92 + 0.3 + 0.5 + 0.3)))

        # ----- 11. [50.24-54.66] similar rates + spacing highlights -----
        # wait until 50.42
        self.wait(max(0.05, 50.42 - 49.30))

        similar_caption = Text("similar firing rates  =", font_size=28, color=WHITE)
        similar_caption.move_to(v2(0, -0.25))
        self.play(FadeIn(similar_caption), run_time=max(0.05, 0.4))

        # wait until 53.04
        self.wait(max(0.05, 53.04 - (50.42 + 0.4)))

        # top evenly spaced arrows
        arrow_top = VGroup()
        for x1, x2 in [(-2.5, -1.25), (-1.25, 0), (0, 1.25), (1.25, 2.5)]:
            a = Arrow(v2(x1 + 0.05, 0.7), v2(x2 - 0.05, 0.7), color=BLUE, stroke_width=2,
                      max_tip_length_to_length_ratio=0.3, buff=0.0)
            arrow_top.add(a)
        label_even = Text("evenly spaced", font_size=20, color=BLUE)
        label_even.next_to(arrow_top, UP, buff=0.1)

        # bottom clusters dotted rings and labels
        ring1 = VGroup(
            DashedVMobject(Circle(radius=0.18, color=ORANGE, stroke_width=2)).move_to(v2(-2.6, -1.05)),
            DashedVMobject(Circle(radius=0.18, color=ORANGE, stroke_width=2)).move_to(v2(-2.4, -1.05))
        )
        ring2 = VGroup(
            DashedVMobject(Circle(radius=0.18, color=ORANGE, stroke_width=2)).move_to(v2(1.9, -1.05)),
            DashedVMobject(Circle(radius=0.18, color=ORANGE, stroke_width=2)).move_to(v2(2.1, -1.05))
        )
        label_bursts = Text("bursts", font_size=20, color=ORANGE).next_to(ring1, DOWN, buff=0.1)
        label_pauses = Text("pauses", font_size=20, color=ORANGE).next_to(gap_zone, DOWN, buff=0.1)

        self.play(FadeIn(arrow_top), FadeIn(label_even), run_time=max(0.05, 0.6))
        self.play(FadeIn(ring1), FadeIn(ring2), FadeIn(label_bursts), FadeIn(label_pauses), run_time=max(0.05, 0.6))
        # final caption
        final_caption = Text("same rate, different timing", font_size=26, color=YELLOW)
        final_caption.next_to(VGroup(top_axis, bottom_axis), DOWN, buff=0.4)
        self.play(FadeIn(final_caption), run_time=max(0.05, 0.36))  # ends ~54.66

        # ----- 12. [54.66-61.88] summary panel -----
        old_same_group = VGroup(same_title, top_axis, bottom_axis, top_ticks, top_label,
                                bottom_ticks, bottom_label, gap_zone, similar_caption,
                                arrow_top, label_even, ring1, ring2, label_bursts,
                                label_pauses, final_caption)
        self.play(FadeOut(old_same_group), run_time=max(0.05, 0.8))

        summary_panel = Rectangle(width=11, height=4.2, fill_color=GREY, fill_opacity=0.1,
                                  stroke_color=GREY_B, stroke_width=2).move_to(v2(0, 0.2))
        self.play(FadeIn(summary_panel), run_time=max(0.05, 0.6))

        # left mini bar chart
        left_mini_axis = Line(v2(-4.5, -0.6), v2(-1.5, -0.6), color=GREY_B, stroke_width=2)
        left_bar1 = Rectangle(width=0.4, height=0.4, fill_color=BLUE, fill_opacity=0.9).move_to(v2(-3.7, -0.4))
        left_bar2 = Rectangle(width=0.4, height=1.6, fill_color=ORANGE, fill_opacity=0.9).move_to(v2(-2.8, -0.2))
        left_label = Text("firing rate coding", font_size=22, color=BLUE).move_to(v2(-3.0, -1.2))

        # right mini spike trains
        right_axis_top = Line(v2(1.5, 0.5), v2(4.5, 0.5), color=WHITE, stroke_width=2)
        right_axis_bottom = Line(v2(1.5, -0.2), v2(4.5, -0.2), color=WHITE, stroke_width=2)
        right_top_ticks = VGroup()
        for x in [1.8, 2.2, 2.6, 3.0, 3.4]:
            right_top_ticks.add(Line(v2(x, 0.2), v2(x, 0.7), color=BLUE, stroke_width=2))
        right_bottom_ticks = VGroup()
        for x in [1.8, 2.0, 2.2, 3.6, 3.8]:
            right_bottom_ticks.add(Line(v2(x, -0.5), v2(x, -0.1), color=ORANGE, stroke_width=2))
        right_label = Text("temporal coding — spike timing", font_size=22, color=ORANGE).move_to(v2(3.0, -1.2))

        self.play(FadeIn(left_mini_axis), FadeIn(left_bar1), FadeIn(left_bar2), FadeIn(left_label),
                  run_time=max(0.05, 0.8))
        self.play(FadeIn(right_axis_top), FadeIn(right_axis_bottom), FadeIn(right_top_ticks),
                  FadeIn(right_bottom_ticks), FadeIn(right_label), run_time=max(0.05, 0.8))

        # wait until 57.30 left pulse
        self.wait(max(0.05, 57.30 - (54.66 + 0.8 + 0.6 + 0.8 + 0.8)))

        left_group_pulse = VGroup(left_mini_axis, left_bar1, left_bar2, left_label)
        self.play(left_group_pulse.animate.scale(1.08), run_time=max(0.05, 0.5))
        self.play(left_group_pulse.animate.scale(1 / 1.08), run_time=max(0.05, 0.5))

        # wait until 58.52 right pulse
        self.wait(max(0.05, 58.52 - (57.30 + 0.5 + 0.5)))

        right_group_pulse = VGroup(right_axis_top, right_axis_bottom, right_top_ticks,
                                   right_bottom_ticks, right_label)
        self.play(right_group_pulse.animate.scale(1.08), run_time=max(0.05, 0.5))
        self.play(right_group_pulse.animate.scale(1 / 1.08), run_time=max(0.05, 0.5))

        # wait until 59.78 convergence
        self.wait(max(0.05, 59.78 - (58.52 + 0.5 + 0.5)))

        # central glowing neuron symbol
        central_neuron = Circle(radius=0.25, fill_color=YELLOW, fill_opacity=1,
                                stroke_width=0).move_to(v2(0, 0.2))
        central_neuron.add(
            Line(v2(0, 0.2), v2(0.3, 0.4), color=YELLOW, stroke_width=2),
            Line(v2(0, 0.2), v2(-0.3, 0.4), color=YELLOW, stroke_width=2),
            Line(v2(0, 0.2), v2(0.3, -0.1), color=YELLOW, stroke_width=2),
            Line(v2(0, 0.2), v2(-0.3, -0.1), color=YELLOW, stroke_width=2)
        )
        convergence_line_left = Line(v2(-3.0, -0.2), v2(-0.3, 0.2), color=WHITE, stroke_width=2)
        convergence_line_right = Line(v2(3.0, -0.2), v2(0.3, 0.2), color=WHITE, stroke_width=2)
        caption_richer = Text("richer understanding of neural coding", font_size=28, color=YELLOW)
        caption_richer.move_to(v2(0, -1.8))

        self.play(
            FadeIn(central_neuron),
            Create(convergence_line_left), Create(convergence_line_right),
            FadeIn(caption_richer),
            run_time=max(0.05, 0.8
        ))

        # hold until 61.88 (beat12 ends)
        self.wait(max(0.05, 61.88 - (59.78 + 0.8)))

        # ----- 13. [61.88-62.60] fade out -----
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=max(0.05, 0.72))
        self.wait(max(0.05, 62.60 - 61.88 - 0.72))