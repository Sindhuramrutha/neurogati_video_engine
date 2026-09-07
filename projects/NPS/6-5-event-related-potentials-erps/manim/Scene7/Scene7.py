ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


def make_background_points(seed, x_min, x_max, n=220, base_amp=0.4):
    rng = np.random.RandomState(seed)
    xs = np.linspace(x_min, x_max, n)
    y = np.zeros(n)
    for k in range(1, 6):
        freq = rng.uniform(0.7, 3.0)
        phase = rng.uniform(0, TAU)
        amp = base_amp / (k ** 0.85)
        y += amp * np.sin(TAU * freq * (xs - x_min) / (x_max - x_min) + phase)
    y += rng.normal(0, 0.08 * base_amp, n)
    if np.max(np.abs(y)) > 0:
        y = y / np.max(np.abs(y)) * base_amp
    return xs, y


def add_gaussian_bump(xs, y, center, amp, width):
    return y + amp * np.exp(-0.5 * ((xs - center) / width) ** 2)


def make_trace_from_points(xs, ys, color=WHITE, stroke_width=2.0):
    points = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
    trace = VMobject(fill_opacity=0)
    trace.set_stroke(color=color, width=stroke_width, opacity=1)
    trace.set_points_as_corners(points)
    return trace


def make_trace(seed, x_min, x_max, base_amp=0.4, color=WHITE,
               stroke_width=2.0, bump_center=None, bump_amp=0.1,
               bump_width=0.18, n=220):
    xs, ys = make_background_points(seed, x_min, x_max, n=n, base_amp=base_amp)
    if bump_center is not None:
        ys = add_gaussian_bump(xs, ys, bump_center, bump_amp, bump_width)
    return make_trace_from_points(xs, ys, color=color, stroke_width=stroke_width)


def make_trace_with_tick(seed, x_min, x_max, base_amp=0.4, tick_x=0.0,
                         bump_center=None, bump_amp=0.08, bump_width=0.18,
                         color=WHITE, stroke_width=1.8, n=220):
    xs, ys = make_background_points(seed, x_min, x_max, n=n, base_amp=base_amp)
    if bump_center is not None:
        ys = add_gaussian_bump(xs, ys, bump_center, bump_amp, bump_width)
    trace = make_trace_from_points(xs, ys, color=color, stroke_width=stroke_width)
    y_tick = np.interp(tick_x, xs, ys)
    tick = Line(UP * 0.14, DOWN * 0.14, color=PINK, stroke_width=2.5)
    tick.move_to(np.array([tick_x, y_tick, 0.0]))
    return trace, tick


def make_smooth_trace(seed, x_min, x_max, base_amp=0.12, color=GOLD,
                      bump_center=0.0, bump_amp=0.35, bump_width=0.18,
                      stroke_width=4.0, n=260):
    rng = np.random.RandomState(seed)
    xs = np.linspace(x_min, x_max, n)
    y = np.zeros(n)
    y += base_amp * np.sin(TAU * 0.35 * (xs - x_min) / (x_max - x_min) + rng.uniform(0, TAU))
    y += 0.5 * base_amp * np.sin(TAU * 0.7 * (xs - x_min) / (x_max - x_min) + rng.uniform(0, TAU))
    y += rng.normal(0, 0.03 * base_amp, n)
    if bump_amp is not None:
        y += bump_amp * np.exp(-0.5 * ((xs - bump_center) / bump_width) ** 2)
    trace = make_trace_from_points(xs, y, color=color, stroke_width=stroke_width)
    return trace, xs, y


def make_oscillatory_burst(seed, x_min, x_max, tick_x, color=WHITE,
                           stroke_width=2.5, n=260, cycles=4.5, amp=0.3,
                           envelope_center=1.5, envelope_width=1.1):
    rng = np.random.RandomState(seed)
    xs = np.linspace(x_min, x_max, n)
    y = 0.08 * np.sin(TAU * 0.35 * (xs - x_min) / (x_max - x_min) + rng.uniform(0, TAU))
    y += rng.normal(0, 0.03, n)
    x_after = xs - tick_x
    envelope = np.exp(-0.5 * ((x_after - envelope_center) / envelope_width) ** 2)
    y += amp * envelope * np.sin(TAU * cycles * x_after / (x_max - tick_x))
    return make_trace_from_points(xs, y, color=color, stroke_width=stroke_width)


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Background tint overlay used later for a subtle lighting shift.
        tint_overlay = Rectangle(
            width=14, height=8,
            color=BLUE, fill_color=BLUE,
            fill_opacity=0.0, stroke_width=0,
        ).move_to(ORIGIN).set_z_index(-10)
        self.add(tint_overlay)

        # --- Previous scene composition (recreated for continuity) ---
        prev_comp = self.build_previous_composition()
        self.add(prev_comp)

        # --- Recap icon ---
        recap_icon, mini_traces, recap_arrow, clean_wave = self.build_recap_icon()

        # Beat 1: 0.00-3.52 — fade out previous composition, fade in recap icon.
        self.play(FadeOut(prev_comp), run_time=max(0.05, 1.6))
        self.play(FadeIn(recap_icon), run_time=max(0.05, 1.92))

        # Beat 2: 3.52-6.94 — recap icon holds with subtle motion.
        selected_trace = mini_traces[2]
        self.play(selected_trace.animate.set_color(WHITE), run_time=max(0.05, 0.8))
        self.play(Indicate(recap_arrow, scale_factor=1.15, color=GOLD), run_time=max(0.05, 0.9))
        self.play(Indicate(clean_wave, scale_factor=1.08, color=GOLD), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.72))

        # Beat 3: 6.94-9.38 — recap icon out, vertical divider in.
        divider = Line(UP * 3.7, DOWN * 3.7, color=GREY_B, stroke_width=2.5)
        self.play(FadeOut(recap_icon), run_time=max(0.05, 1.2))
        self.play(Create(divider), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.44))

        # --- Build left time-locked trace ---
        left_x_min, left_x_max = -2.8, 2.8
        left_tick_x = -2.2
        left_deflection_x = -0.8
        left_tick_screen_x = -5.2

        left_trace, left_tick = make_trace_with_tick(
            seed=501,
            x_min=left_x_min,
            x_max=left_x_max,
            base_amp=0.12,
            tick_x=left_tick_x,
            bump_center=left_deflection_x,
            bump_amp=0.36,
            bump_width=0.18,
            color=WHITE,
            stroke_width=2.5,
            n=260,
        )
        left_trace_group = VGroup(left_trace, left_tick)
        shift_x_left = left_tick_screen_x - left_tick.get_center()[0]
        left_trace_group.shift(np.array([shift_x_left, 0.6, 0]))

        left_deflection_screen_x = left_tick_screen_x + (left_deflection_x - left_tick_x)
        left_prop = (left_deflection_x - left_x_min) / (left_x_max - left_x_min)
        left_deflection_y = left_trace.point_from_proportion(left_prop)[1]
        left_highlight = RoundedRectangle(
            height=0.9, width=0.85,
            color=GOLD, fill_color=GOLD,
            fill_opacity=0.12, stroke_width=3,
            corner_radius=0.1,
        ).move_to(np.array([left_deflection_screen_x, left_deflection_y, 0]))

        left_stim_label = Text("Stimulus", font_size=18, color=GREY_B).next_to(
            left_tick, DOWN, buff=0.12
        )
        left_tl_label = Text("Time-locked", font_size=26, color=WHITE, weight="BOLD").next_to(
            left_trace_group, DOWN, buff=1.0
        )
        left_panel_group = VGroup(left_trace_group, left_highlight, left_stim_label, left_tl_label)

        # Beat 4: 9.38-14.46 — left stimulus marker and time-locked trace.
        self.play(
            Create(left_trace),
            FadeIn(left_tick),
            FadeIn(left_stim_label),
            FadeIn(left_highlight),
            run_time=max(0.05, 5.08),
        )

        # --- Build right induced trace ---
        right_x_min, right_x_max = -2.8, 2.8
        right_tick_x = -2.2
        right_tick_screen_x = 0.7

        right_trace = make_oscillatory_burst(
            seed=777,
            x_min=right_x_min,
            x_max=right_x_max,
            tick_x=right_tick_x,
            color=TEAL,
            stroke_width=2.5,
            cycles=5,
            amp=0.3,
            envelope_center=1.5,
            envelope_width=1.1,
        )
        right_tick_prop = (right_tick_x - right_x_min) / (right_x_max - right_x_min)
        right_tick_y = right_trace.point_from_proportion(right_tick_prop)[1]
        right_tick = Line(UP * 0.14, DOWN * 0.14, color=PINK, stroke_width=2.5)
        right_tick.move_to(np.array([right_tick_x, right_tick_y, 0]))

        right_trace_group = VGroup(right_trace, right_tick)
        shift_x_right = right_tick_screen_x - right_tick.get_center()[0]
        right_trace_group.shift(np.array([shift_x_right, 0.6, 0]))

        right_stim_label = Text("Stimulus", font_size=18, color=GREY_B).next_to(
            right_tick, DOWN, buff=0.12
        )
        right_ind_label = Text("Induced", font_size=26, color=WHITE, weight="BOLD").next_to(
            right_trace_group, DOWN, buff=1.0
        )
        right_panel_group = VGroup(right_trace_group, right_stim_label, right_ind_label)

        # Beat 5: 14.46-21.08 — right stimulus marker, induced trace, both labels.
        self.play(
            Create(right_trace),
            FadeIn(right_tick),
            FadeIn(right_stim_label),
            FadeIn(left_tl_label),
            FadeIn(right_ind_label),
            run_time=max(0.05, 6.62),
        )

        # Beat 6: 21.08-27.74 — left deflection pulses once; right phase shifts subtly.
        self.play(Indicate(left_highlight, scale_factor=1.08, color=GOLD), run_time=max(0.05, 1.4))
        self.play(right_trace.animate.shift(LEFT * 0.12), run_time=max(0.05, 1.2))
        self.play(right_trace.animate.shift(RIGHT * 0.24), run_time=max(0.05, 1.2))
        self.play(right_trace.animate.shift(LEFT * 0.12), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.66))

        # Beat 7: 27.74-33.50 — ghosted phase-shifted copies of right trace fade in.
        ghost_shifts = [-0.28, -0.12, 0.22, 0.06]
        ghosts = VGroup(*[
            right_trace.copy().set_opacity(0.28).shift(RIGHT * s)
            for s in ghost_shifts
        ])
        ghosts.set_z_index(0)
        right_trace.set_z_index(1)
        self.play(FadeIn(ghosts), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 3.76))

        # Beat 8: 33.50-41.18 — ghosts out, annotation appears on right.
        bracket_top = np.array([right_trace.get_center()[0], right_trace.get_top()[1] + 0.15, 0])
        bracket_bottom = np.array([right_trace.get_center()[0], right_trace.get_bottom()[1] - 0.15, 0])
        no_deflection_bracket = DashedLine(
            bracket_top, bracket_bottom,
            color=ORANGE, stroke_width=2.5, dash_length=0.12,
        )
        no_deflection_text = Text("No consistent deflection", font_size=20, color=ORANGE, weight="BOLD")
        no_deflection_text.scale_to_fit_width(3.0)
        no_deflection_text.next_to(no_deflection_bracket, RIGHT, buff=0.6).shift(UP * 0.35)
        no_deflection_arrow = Arrow(
            no_deflection_text.get_bottom() + DOWN * 0.1,
            right_trace.get_center() + RIGHT * 0.35,
            color=ORANGE, stroke_width=3, buff=0.1,
        )
        annotation_group = VGroup(no_deflection_bracket, no_deflection_text, no_deflection_arrow)

        self.play(FadeOut(ghosts), run_time=max(0.05, 1.2))
        self.play(
            FadeIn(no_deflection_text),
            Create(no_deflection_arrow),
            Create(no_deflection_bracket),
            run_time=max(0.05, 3.0),
        )
        self.wait(max(0.05, 3.48))

        # Beat 9: 41.18-44.54 — annotation out, subtle background tint shift.
        self.play(
            FadeOut(annotation_group),
            tint_overlay.animate.set_fill(opacity=0.07),
            run_time=max(0.05, 3.36),
        )

        # Beat 10: 44.54-49.10 — left side brightens, deflection pulses, then eases.
        self.play(
            left_trace.animate.set_stroke(width=4),
            left_tl_label.animate.set_color(YELLOW),
            left_highlight.animate.set_stroke(width=5),
            run_time=max(0.05, 1.2),
        )
        self.play(Indicate(left_highlight, scale_factor=1.12, color=GOLD), run_time=max(0.05, 1.2))
        self.play(
            left_trace.animate.set_stroke(width=2.5),
            left_highlight.animate.set_stroke(width=3),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.96))

        # Beat 11: 49.10-56.42 — right side brightens, oscillatory burst animates more visibly.
        self.play(
            right_trace.animate.set_stroke(color=TEAL, width=4),
            right_ind_label.animate.set_color(YELLOW),
            left_panel_group.animate.set_opacity(0.55),
            run_time=max(0.05, 1.6),
        )
        self.play(right_trace.animate.shift(LEFT * 0.2), run_time=max(0.05, 1.2))
        self.play(right_trace.animate.shift(RIGHT * 0.4), run_time=max(0.05, 1.2))
        self.play(right_trace.animate.shift(LEFT * 0.2), run_time=max(0.05, 1.2))
        self.play(Indicate(right_ind_label, scale_factor=1.08, color=YELLOW), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.92))

        # Beat 12: 56.42-63.42 — equal brightness, stable side-by-side comparison.
        self.play(
            left_panel_group.animate.set_opacity(1),
            left_tl_label.animate.set_color(WHITE),
            right_trace.animate.set_stroke(color=TEAL, width=2.5),
            right_ind_label.animate.set_color(WHITE),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 5.0))

        # Beat 13: 63.42-70.40 — labels pulse softly, left then right.
        self.play(Indicate(left_tl_label, scale_factor=1.08, color=YELLOW), run_time=max(0.05, 1.8))
        self.play(Indicate(right_ind_label, scale_factor=1.08, color=YELLOW), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 3.38))

        # Beat 14: 70.40-71.78 — final hold with Section 6.6.
        section_text = Text("Section 6.6", font_size=30, color=YELLOW, weight="BOLD")
        section_text.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(section_text), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.38))

    def build_previous_composition(self):
        final_x_min, final_x_max = -4.8, 4.8
        final_tick_x = -3.3
        final_bump_x = -1.4
        final_n = 10
        final_step = 0.34
        final_stack_top_y = 1.7

        final_items = []
        for i in range(final_n):
            tr, tk = make_trace_with_tick(
                seed=610 + i,
                x_min=final_x_min,
                x_max=final_x_max,
                base_amp=0.26,
                tick_x=final_tick_x,
                bump_center=final_bump_x,
                bump_amp=0.06,
                bump_width=0.2,
                color=WHITE,
                stroke_width=1.3,
            )
            y = final_stack_top_y - i * final_step
            item = VGroup(tr, tk).move_to(np.array([0.0, y, 0.0]))
            final_items.append(item)

        final_stack_group = VGroup(*final_items)

        final_avg_trace, _, _ = make_smooth_trace(
            seed=710,
            x_min=final_x_min,
            x_max=final_x_max,
            base_amp=0.08,
            color=GOLD,
            bump_center=final_bump_x,
            bump_amp=0.4,
            bump_width=0.18,
            stroke_width=5,
        )
        final_avg_group = VGroup(final_avg_trace).move_to(np.array([0.0, -2.2, 0.0]))

        final_peak_rect = SurroundingRectangle(
            final_avg_group, color=GOLD, stroke_width=3, fill_opacity=0, buff=0.08
        )

        final_stack_top_guide = final_stack_top_y + 0.15
        final_stack_bottom_guide = final_stack_top_y - (final_n - 1) * final_step - 0.15
        final_response_line = DashedLine(
            start=np.array([final_bump_x, final_stack_top_guide, 0]),
            end=np.array([final_bump_x, final_stack_bottom_guide, 0]),
            color=YELLOW, stroke_width=2.5, dash_length=0.14,
        )

        equation_text = Text(
            "ERP = average of many aligned EEG epochs",
            font_size=30, color=YELLOW, weight="BOLD",
        )
        equation_text.scale_to_fit_width(11)
        equation_text.to_edge(DOWN, buff=0.3)

        return VGroup(
            final_stack_group,
            final_avg_group,
            final_peak_rect,
            final_response_line,
            equation_text,
        )

    def build_recap_icon(self):
        mini_traces = VGroup()
        for i in range(5):
            xs, ys = make_background_points(40 + i, -1.6, 1.6, n=80, base_amp=0.08)
            trace = make_trace_from_points(xs, ys, color=GREY_B, stroke_width=1.4)
            mini_traces.add(trace)

        mini_traces.arrange(DOWN, buff=0.12)
        mini_traces.scale_to_fit_width(2.6)
        mini_traces.move_to(UP * 0.7)

        clean_wave, _, _ = make_smooth_trace(
            seed=99,
            x_min=-1.6,
            x_max=1.6,
            base_amp=0.04,
            color=GOLD,
            bump_center=0.0,
            bump_amp=0.3,
            bump_width=0.22,
            stroke_width=3,
        )
        clean_wave.scale_to_fit_width(2.9)
        clean_wave.next_to(mini_traces, DOWN, buff=0.75)

        arrow = Arrow(
            mini_traces.get_bottom() + DOWN * 0.1,
            clean_wave.get_top() + UP * 0.12,
            color=GOLD, stroke_width=5, buff=0,
        )

        icon_content = VGroup(mini_traces, arrow, clean_wave)
        rounded_rect = SurroundingRectangle(
            icon_content,
            color=GREY_B, fill_color=BLUE, fill_opacity=0.08,
            stroke_width=1.5, buff=0.35, corner_radius=0.25,
        )
        icon = VGroup(icon_content, rounded_rect)
        return icon, mini_traces, arrow, clean_wave