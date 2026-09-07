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


def double_arrow(start, end, color=WHITE, stroke_width=3.0):
    return VGroup(
        Arrow(start, end, color=color, stroke_width=stroke_width, buff=0),
        Arrow(end, start, color=color, stroke_width=stroke_width, buff=0),
    )


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Reconstruct the previous completed checklist ---
        prev_title = Text("ERP ANALYSIS", font_size=28, color=WHITE, weight="BOLD")
        prev_sub = Text("provides several important advantages", font_size=20, color=GREY_B)
        prev_rows = VGroup()
        for _ in range(4):
            box = Square(side_length=0.22, color=GREEN, stroke_width=2, fill_opacity=0)
            line = Line(LEFT * 1.4, RIGHT * 1.4, color=GREY_B, stroke_width=2)
            row = VGroup(box, line).arrange(RIGHT, buff=0.3)
            center = box.get_center()
            check = VGroup(
                Line(center + LEFT * 0.09 + DOWN * 0.02, center + UP * 0.03, color=GREEN, stroke_width=4),
                Line(center + UP * 0.03, center + RIGHT * 0.11 + DOWN * 0.07, color=GREEN, stroke_width=4),
            )
            row.add(check)
            prev_rows.add(row)
        prev_rows.arrange(DOWN, buff=0.35)
        prev_group = VGroup(prev_title, prev_sub, prev_rows).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        self.add(prev_group)

        # --- 1. Slide checklist away and bring up single EEG trace ---
        single_x_min, single_x_max = -5.5, 5.5
        single_xs, single_ys = make_background_points(101, single_x_min, single_x_max,
                                                      n=300, base_amp=0.8)
        single_bg = make_trace_from_points(single_xs, single_ys, color=WHITE, stroke_width=3)
        tick_x = -4.2
        tick_y = np.interp(tick_x, single_xs, single_ys)
        tick = Line(UP * 0.22, DOWN * 0.22, color=PINK, stroke_width=4)
        tick.move_to(np.array([tick_x, tick_y, 0.0]))
        single_trace_vis = VGroup(single_bg, tick)
        single_label = Text("Single EEG recording", font_size=22, color=GREY_B)
        single_label.next_to(single_trace_vis, DOWN, buff=0.5)

        self.play(
            prev_group.animate.shift(LEFT * 7).set_opacity(0),
            FadeIn(single_bg),
            GrowFromCenter(tick),
            FadeIn(single_label),
            run_time=max(0.05, 2.78),
        )

        # --- 2. Add small event-related deflection and highlight ---
        bump_x = tick_x + 1.3
        y_bump_base = np.interp(bump_x, single_xs, single_ys)
        bump_span = 0.5
        bump_width = 0.25
        bump_amp = 0.13
        bump_xs = np.linspace(bump_x - bump_span, bump_x + bump_span, 60)
        bump_ys = y_bump_base + bump_amp * np.exp(-0.5 * ((bump_xs - bump_x) / bump_width) ** 2)
        single_bump = make_trace_from_points(bump_xs, bump_ys, color=YELLOW, stroke_width=4)
        single_highlight = SurroundingRectangle(single_bump, color=YELLOW,
                                                stroke_width=2.5, fill_opacity=0, buff=0.1)
        resp_label = Text("Event-related response", font_size=20, color=YELLOW)
        resp_label.next_to(single_label, DOWN, buff=0.4)
        resp_arrow = Arrow(resp_label.get_top() + UP * 0.1,
                           single_bump.get_bottom() + DOWN * 0.1,
                           color=YELLOW, stroke_width=2.5, buff=0.1)

        self.play(
            Create(single_bump),
            Create(single_highlight),
            FadeIn(resp_label),
            Create(resp_arrow),
            run_time=max(0.05, 1.86),
        )

        # --- 3. Zoom/expand vertically, add size-contrast arrows ---
        scale_y_factor = 2.1
        def zoom_func(p):
            return np.array([p[0], (p[1] - y_bump_base) * scale_y_factor + y_bump_base, p[2]])

        tall_arrow = double_arrow(np.array([5.4, -1.7, 0]), np.array([5.4, 1.7, 0]),
                                  color=BLUE, stroke_width=5)
        short_arrow = double_arrow(np.array([6.1, -0.13, 0]), np.array([6.1, 0.13, 0]),
                                   color=YELLOW, stroke_width=4)
        bg_arrow_label = Text("Background EEG activity", font_size=16, color=BLUE)
        bg_arrow_label.scale_to_fit_width(2.7)
        bg_arrow_label.next_to(tall_arrow, UP, buff=0.1)
        erp_arrow_label = Text("ERP", font_size=22, color=YELLOW)
        erp_arrow_label.next_to(short_arrow, UP, buff=0.1)

        self.play(
            single_bg.animate.apply_function(zoom_func),
            Create(tall_arrow),
            Create(short_arrow),
            FadeIn(bg_arrow_label),
            FadeIn(erp_arrow_label),
            run_time=max(0.05, 2.10),
        )

        # --- 4. Hold zoomed view with size-contrast message ---
        bottom_label = Text("Response is much smaller than ongoing EEG activity.",
                            font_size=26, color=WHITE)
        bottom_label.to_edge(DOWN, buff=0.5)

        self.play(
            FadeOut(single_label),
            FadeOut(resp_label),
            FadeOut(resp_arrow),
            FadeIn(bottom_label),
            run_time=max(0.05, 1.0),
        )
        self.play(Indicate(single_highlight, scale_factor=1.07, color=YELLOW,
                           run_time=max(0.05, 1.2)))
        self.wait(max(0.05, 2.86))

        # --- 5. Single trace shrinks and moves left; right side empty ---
        single_trace_vis = VGroup(single_bg, tick, single_bump, single_highlight)
        left_panel_center = np.array([-4.1, 0.0, 0.0])

        self.play(
            FadeOut(tall_arrow),
            FadeOut(short_arrow),
            FadeOut(bg_arrow_label),
            FadeOut(erp_arrow_label),
            FadeOut(bottom_label),
            single_trace_vis.animate.scale(0.55).move_to(left_panel_center),
            run_time=max(0.05, 1.54),
        )

        # --- 6. Right side: aligned-latency stack appears one by one ---
        align_x_min, align_x_max = -2.5, 2.5
        align_init_x = 2.9
        align_stack_y = 0.75
        align_tick_x = -1.7
        align_resp_x = -0.7
        align_n = 7
        align_step = 0.55

        aligned_items = []
        for i in range(align_n):
            y = 1.65 - i * align_step
            tr, tk = make_trace_with_tick(
                seed=210 + i,
                x_min=align_x_min,
                x_max=align_x_max,
                base_amp=0.32,
                tick_x=align_tick_x,
                bump_center=align_resp_x,
                bump_amp=0.07,
                bump_width=0.18,
                color=WHITE,
                stroke_width=1.8,
            )
            item = VGroup(tr, tk).move_to(np.array([align_init_x, align_stack_y + y, 0.0]))
            aligned_items.append(item)

        align_top_y = align_stack_y + 1.65 + 0.2
        align_bottom_y = align_stack_y - (align_n - 1) * align_step - 0.2

        onset_line_aligned = DashedLine(
            start=np.array([align_init_x + align_tick_x, align_top_y, 0]),
            end=np.array([align_init_x + align_tick_x, align_bottom_y, 0]),
            color=PINK, stroke_width=2, stroke_opacity=0.4,
        )
        response_line_aligned = DashedLine(
            start=np.array([align_init_x + align_resp_x, align_top_y, 0]),
            end=np.array([align_init_x + align_resp_x, align_bottom_y, 0]),
            color=YELLOW, stroke_width=2.5, dash_length=0.15,
        )
        aligned_stack_group = VGroup(*aligned_items)
        aligned_stack_label = Text("Consistent latency", font_size=20, color=YELLOW)
        aligned_stack_label.next_to(aligned_stack_group, DOWN, buff=0.2)

        aligned_objs = list(aligned_items)
        aligned_objs.extend([onset_line_aligned, response_line_aligned, aligned_stack_label])

        per_align = 3.6 / align_n
        for item in aligned_items:
            self.play(Create(item[0]), FadeIn(item[1]),
                      run_time=max(0.05, per_align * 0.85))
            self.wait(max(0.01, per_align * 0.15))
        self.play(
            Create(onset_line_aligned),
            Create(response_line_aligned),
            FadeIn(aligned_stack_label),
            run_time=max(0.05, 1.24),
        )

        # --- 7. Aligned average below stack ---
        aligned_avg_trace, _, _ = make_smooth_trace(
            seed=301,
            x_min=align_x_min,
            x_max=align_x_max,
            base_amp=0.12,
            color=GOLD,
            bump_center=align_resp_x,
            bump_amp=0.36,
            bump_width=0.18,
            stroke_width=4,
        )
        aligned_avg_group = VGroup(aligned_avg_trace)
        aligned_avg_group.move_to(np.array([align_init_x, align_stack_y - 2.4, 0.0]))
        clear_peak_rect = SurroundingRectangle(aligned_avg_group, color=GOLD,
                                               stroke_width=2, fill_opacity=0, buff=0.08)
        aligned_avg_label = Text("Averaged waveform — clear ERP peak.",
                                 font_size=18, color=GOLD)
        aligned_avg_label.next_to(aligned_avg_group, DOWN, buff=0.15)

        aligned_objs.extend([aligned_avg_group, clear_peak_rect, aligned_avg_label])

        self.play(FadeOut(aligned_stack_label), run_time=max(0.05, 0.2))
        self.play(
            Create(aligned_avg_trace),
            Create(clear_peak_rect),
            FadeIn(aligned_avg_label),
            run_time=max(0.05, 2.0),
        )
        self.play(Indicate(clear_peak_rect, scale_factor=1.06, color=GOLD,
                           run_time=max(0.05, 1.08)))

        # --- 8. Shift aligned panel left, build variable-latency stack on right ---
        var_x_min, var_x_max = -1.4, 1.4
        var_center_x = 5.0
        var_stack_y = 0.75
        var_tick_x = -0.9
        var_latencies = [0.0, 0.65, 0.2, 1.0, 0.45, 1.3]
        var_n = len(var_latencies)
        var_step = 0.55
        var_items = []
        for i, lat in enumerate(var_latencies):
            bump_c = var_tick_x + lat
            tr, tk = make_trace_with_tick(
                seed=310 + i,
                x_min=var_x_min,
                x_max=var_x_max,
                base_amp=0.3,
                tick_x=var_tick_x,
                bump_center=bump_c,
                bump_amp=0.07,
                bump_width=0.18,
                color=WHITE,
                stroke_width=1.7,
            )
            y = 1.35 - i * var_step
            item = VGroup(tr, tk).move_to(np.array([var_center_x, var_stack_y + y, 0.0]))
            var_items.append(item)

        var_top_y = var_stack_y + 1.35 + 0.2
        var_bottom_y = var_stack_y - (var_n - 1) * var_step - 0.2
        var_attempt_x = var_tick_x + np.mean(var_latencies)

        onset_line_var = DashedLine(
            start=np.array([var_center_x + var_tick_x, var_top_y, 0]),
            end=np.array([var_center_x + var_tick_x, var_bottom_y, 0]),
            color=PINK, stroke_width=2, stroke_opacity=0.4,
        )
        response_attempt_line = DashedLine(
            start=np.array([var_center_x + var_attempt_x, var_top_y, 0]),
            end=np.array([var_center_x + var_attempt_x, var_bottom_y, 0]),
            color=GREY_B, stroke_width=2.5, stroke_opacity=0.55,
        )
        var_stack_group = VGroup(*var_items)
        var_stack_label = Text("Response latency varies across trials.",
                               font_size=18, color=ORANGE)
        var_stack_label.scale_to_fit_width(4.6)
        var_stack_label.next_to(var_stack_group, DOWN, buff=0.3)

        shift_align = LEFT * 1.9
        self.play(
            FadeOut(single_trace_vis),
            *[obj.animate.shift(shift_align) for obj in aligned_objs],
            run_time=max(0.05, 1.0),
        )

        per_var = 3.0 / var_n
        for item in var_items:
            self.play(Create(item[0]), FadeIn(item[1]),
                      run_time=max(0.05, per_var * 0.8))
            self.wait(max(0.01, per_var * 0.2))
        self.play(
            Create(onset_line_var),
            Create(response_attempt_line),
            FadeIn(var_stack_label),
            run_time=max(0.05, 1.86),
        )

        # --- 9. Variable-latency average appears smeared ---
        var_avg_trace, _, _ = make_smooth_trace(
            seed=402,
            x_min=var_x_min,
            x_max=var_x_max,
            base_amp=0.10,
            color=ORANGE,
            bump_center=var_attempt_x,
            bump_amp=0.22,
            bump_width=0.5,
            stroke_width=4,
        )
        var_avg_group = VGroup(var_avg_trace)
        var_avg_group.move_to(np.array([var_center_x, var_stack_y - 2.4, 0.0]))
        var_avg_highlight = SurroundingRectangle(var_avg_group, color=ORANGE,
                                                 stroke_width=2.5, fill_opacity=0, buff=0.08)
        variable_avg_label = Text("Smeared averaged response", font_size=18, color=ORANGE)
        variable_avg_label.next_to(var_avg_group, DOWN, buff=0.15)

        self.play(FadeOut(var_stack_label), run_time=max(0.05, 0.2))
        self.play(
            Create(var_avg_trace),
            Create(var_avg_highlight),
            FadeIn(variable_avg_label),
            run_time=max(0.05, 3.0),
        )
        self.wait(max(0.05, 0.96))

        # --- 10. Side-by-side comparison labels ---
        clear_peak_label = Text("Clear peak", font_size=22, color=GREEN, weight="BOLD")
        clear_peak_label.next_to(aligned_avg_group, DOWN, buff=0.15)
        reduced_peak_label = Text("Reduced peak", font_size=22, color=ORANGE, weight="BOLD")
        reduced_peak_label.next_to(var_avg_group, DOWN, buff=0.15)

        self.play(
            FadeOut(aligned_avg_label),
            FadeOut(variable_avg_label),
            run_time=max(0.05, 0.6),
        )
        self.play(
            FadeIn(clear_peak_label),
            FadeIn(reduced_peak_label),
            run_time=max(0.05, 0.8),
        )
        self.play(
            Indicate(clear_peak_rect, scale_factor=1.08, color=GREEN, run_time=max(0.05, 0.8)),
            Indicate(var_avg_highlight, scale_factor=1.08, color=ORANGE, run_time=max(0.05, 0.8)),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.88))

        # --- 11. Fade comparison, show crossed-out single recording ---
        current_objs = [
            *aligned_objs,
            clear_peak_label,
            reduced_peak_label,
            *var_items,
            onset_line_var,
            response_attempt_line,
            var_avg_group,
            var_avg_highlight,
        ]
        self.play(FadeOut(*current_objs), run_time=max(0.05, 1.2))

        fresh_t, fresh_tk = make_trace_with_tick(
            seed=510,
            x_min=-5.5,
            x_max=5.5,
            base_amp=0.75,
            tick_x=-4.2,
            bump_center=-2.9,
            bump_amp=0.12,
            bump_width=0.25,
            color=WHITE,
            stroke_width=3,
        )
        fresh_group = VGroup(fresh_t, fresh_tk).move_to(ORIGIN)
        red_x = VGroup(
            Line(LEFT * 3.2 + UP * 2.0, RIGHT * 3.2 + DOWN * 2.0,
                 color=RED, stroke_width=10, stroke_opacity=0.9),
            Line(LEFT * 3.2 + DOWN * 2.0, RIGHT * 3.2 + UP * 2.0,
                 color=RED, stroke_width=10, stroke_opacity=0.9),
        ).move_to(fresh_group.get_center())
        not_text = Text("An ERP is NOT obtained from a single EEG recording.",
                        font_size=26, color=WHITE, t2c={"NOT": RED})
        not_text.scale_to_fit_width(12)
        not_text.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(fresh_group), Create(red_x), Write(not_text),
                  run_time=max(0.05, 3.0))
        self.wait(max(0.05, 1.04))

        # --- 12. Crossed single trace replaced by many aligned epochs plus average ---
        self.play(FadeOut(fresh_group), FadeOut(red_x), FadeOut(not_text),
                  run_time=max(0.05, 0.8))

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
        final_stack_label = Text("Many aligned EEG epochs", font_size=24, color=WHITE)
        final_stack_label.next_to(final_stack_group, UP, buff=0.2)

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
        final_avg_label = Text("Averaged ERP waveform", font_size=22, color=GOLD)
        final_avg_label.next_to(final_avg_group, DOWN, buff=0.2)
        final_arrow = Arrow(final_stack_group.get_bottom() + DOWN * 0.1,
                            final_avg_group.get_top() + UP * 0.15,
                            color=GOLD, stroke_width=4, buff=0.1)

        per_final = 2.8 / final_n
        for item in final_items:
            self.play(Create(item[0]), FadeIn(item[1]),
                      run_time=max(0.05, 0.2))
            self.wait(max(0.01, 0.08))
        self.play(
            Create(final_avg_trace),
            Create(final_arrow),
            FadeIn(final_stack_label),
            FadeIn(final_avg_label),
            run_time=max(0.05, 2.66),
        )

        # --- 13. Averaging formula and highlighted peak ---
        final_stack_top_guide = final_stack_top_y + 0.15
        final_stack_bottom_guide = final_stack_top_y - (final_n - 1) * final_step - 0.15
        final_response_line = DashedLine(
            start=np.array([final_bump_x, final_stack_top_guide, 0]),
            end=np.array([final_bump_x, final_stack_bottom_guide, 0]),
            color=YELLOW, stroke_width=2.5, dash_length=0.14,
        )
        final_peak_rect = SurroundingRectangle(final_avg_group, color=GOLD,
                                               stroke_width=3, fill_opacity=0, buff=0.08)
        equation_text = Text("ERP = average of many aligned EEG epochs",
                             font_size=30, color=YELLOW, weight="BOLD")
        equation_text.scale_to_fit_width(11)
        equation_text.to_edge(DOWN, buff=0.3)

        self.play(
            Create(final_response_line),
            Create(final_peak_rect),
            FadeIn(equation_text),
            run_time=max(0.05, 4.0),
        )
        self.play(Indicate(final_peak_rect, scale_factor=1.06, color=GOLD,
                           run_time=max(0.05, 1.2)))
        self.wait(max(0.05, 1.1))

        # --- 14. Final hold with a gentle peak pulse ---
        self.play(Indicate(final_peak_rect, scale_factor=1.08, color=GOLD,
                           run_time=max(0.05, 1.2)))
        self.wait(max(0.05, 1.74))