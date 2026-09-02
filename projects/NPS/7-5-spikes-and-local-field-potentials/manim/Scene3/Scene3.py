ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

TAU = 2 * np.pi

class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        rt = lambda t: max(0.05, t)

        # shared spike-event parameters
        spike_centers = [0.13, 0.27, 0.43, 0.61, 0.80]
        spike_amps = [0.55, 0.70, 0.45, 0.65, 0.55]
        spike_w = [0.008, 0.007, 0.008, 0.008, 0.008]

        def raw_signal(u):
            baseline = 0.16 * np.sin(TAU * 0.7 * u + 0.7) + 0.08 * np.sin(TAU * 1.4 * u + 1.9)
            hf_noise = (
                0.06 * np.sin(TAU * 9.5 * u + 0.3)
                + 0.05 * np.sin(TAU * 16.0 * u + 2.2)
                + 0.03 * np.sin(TAU * 27.0 * u + 1.1)
            )
            s = baseline + hf_noise
            for c, a, w in zip(spike_centers, spike_amps, spike_w):
                s += -a * np.exp(-((u - c) ** 2) / (2 * w ** 2))
            return s

        def clean_signal(u):
            s = 0.0
            for c, a, w in zip(spike_centers, spike_amps, spike_w):
                s += -a * np.exp(-((u - c) ** 2) / (2 * w ** 2))
            return s

        def slow_component(u):
            return (
                0.16 * np.sin(TAU * 0.7 * u + 0.7)
                + 0.08 * np.sin(TAU * 1.4 * u + 1.9)
                + 0.05 * np.sin(TAU * 1.1 * u + 1.0)
            )

        # ---------- Beat 1: full-width messy raw trace ----------
        raw_panel_full = Rectangle(
            width=12.8,
            height=5.0,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=GREY_E,
            fill_opacity=0.12,
        ).move_to(ORIGIN)

        raw_l = raw_panel_full.get_left()[0] + 0.35
        raw_r = raw_panel_full.get_right()[0] - 0.35
        raw_y = raw_panel_full.get_center()[1]
        raw_amp = raw_panel_full.height * 0.38

        def raw_point(u):
            x = raw_l + u * (raw_r - raw_l)
            y = raw_y + raw_signal(u) * raw_amp
            return np.array([x, y, 0])

        raw_trace_full = ParametricFunction(
            raw_point,
            t_range=[0, 1, 0.001],
            color=WHITE,
            stroke_width=3,
        )

        self.play(FadeIn(raw_panel_full), run_time=max(0.05, rt(0.8)))
        self.play(Create(raw_trace_full), run_time=max(0.05, rt(3.0)), rate_func=linear)
        self.wait(max(0.05, rt(0.34)))

        # gap to first label
        self.wait(max(0.05, rt(0.84)))

        label_groups = []

        def make_component_label(text, u, offset, color):
            pt = raw_point(u)
            label = Text(text, font_size=22, color=color, fill_opacity=0.5)
            label.move_to(pt + offset)
            line = Line(label.get_center(), pt, color=color, stroke_width=1.5, stroke_opacity=0.4)
            group = VGroup(label, line)
            label_groups.append(group)
            return label, line, group

        # ---------- Beat 2: neural spikes ----------
        spike_label, spike_line, spike_group = make_component_label(
            "neural spikes", 0.13, UP * 1.9 + LEFT * 0.2, YELLOW
        )
        self.play(FadeIn(spike_group), run_time=max(0.05, rt(0.9)))
        self.play(
            spike_label.animate.set_opacity(1.0),
            spike_line.animate.set_stroke(opacity=0.8),
            run_time=max(0.05, rt(0.6)),
        )
        self.play(
            spike_label.animate.set_opacity(0.55),
            spike_line.animate.set_stroke(opacity=0.4),
            run_time=max(0.05, rt(0.5)),
        )
        self.wait(max(0.05, rt(0.5)))

        # ---------- Beat 3: background neural activity ----------
        self.wait(max(0.05, rt(0.52)))
        bg_label, bg_line, bg_group = make_component_label(
            "background neural activity", 0.25, DOWN * 1.9 + LEFT * 0.1, BLUE
        )
        self.play(FadeIn(bg_group), run_time=max(0.05, rt(0.5)))
        self.play(
            bg_label.animate.set_opacity(1.0),
            bg_line.animate.set_stroke(opacity=0.8),
            run_time=max(0.05, rt(0.31)),
        )
        self.play(
            bg_label.animate.set_opacity(0.55),
            bg_line.animate.set_stroke(opacity=0.4),
            run_time=max(0.05, rt(0.31)),
        )

        # ---------- Beat 4: electronic noise ----------
        self.wait(max(0.05, rt(0.48)))
        en_label, en_line, en_group = make_component_label(
            "electronic noise", 0.50, UP * 2.0, ORANGE
        )
        self.play(FadeIn(en_group), run_time=max(0.05, rt(0.4)))
        self.play(
            en_label.animate.set_opacity(1.0),
            en_line.animate.set_stroke(opacity=0.8),
            run_time=max(0.05, rt(0.22)),
        )
        self.play(
            en_label.animate.set_opacity(0.55),
            en_line.animate.set_stroke(opacity=0.4),
            run_time=max(0.05, rt(0.22)),
        )

        # ---------- Beat 5: thermal noise ----------
        self.wait(max(0.05, rt(0.44)))
        tn_label, tn_line, tn_group = make_component_label(
            "thermal noise", 0.68, DOWN * 1.9, PINK
        )
        self.play(FadeIn(tn_group), run_time=max(0.05, rt(0.26)))
        self.play(
            tn_label.animate.set_opacity(1.0),
            tn_line.animate.set_stroke(opacity=0.8),
            run_time=max(0.05, rt(0.13)),
        )
        self.play(
            tn_label.animate.set_opacity(0.55),
            tn_line.animate.set_stroke(opacity=0.4),
            run_time=max(0.05, rt(0.13)),
        )

        # ---------- Beat 6: other physiological signals ----------
        self.wait(max(0.05, rt(0.38)))
        op_label, op_line, op_group = make_component_label(
            "other physiological signals", 0.83, UP * 1.9 + RIGHT * 0.2, GREEN
        )
        self.play(FadeIn(op_group), run_time=max(0.05, rt(0.5)))
        self.play(
            op_label.animate.set_opacity(1.0),
            op_line.animate.set_stroke(opacity=0.8),
            run_time=max(0.05, rt(0.42)),
        )
        self.play(
            op_label.animate.set_opacity(0.55),
            op_line.animate.set_stroke(opacity=0.4),
            run_time=max(0.05, rt(0.42)),
        )

        # ---------- Beat 7: filter block appears ----------
        self.wait(max(0.05, rt(0.82)))

        filter_block = Rectangle(
            width=1.6,
            height=2.6,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.15,
        ).move_to(np.array([1.3, 0.2, 0]))

        filter_label_top = Text("High-pass filter", font_size=18, color=WHITE)
        filter_label_hz = Text("300 Hz", font_size=25, color=YELLOW)
        filter_label_group = VGroup(filter_label_top, filter_label_hz).arrange(DOWN, buff=0.12)
        filter_label_group.scale_to_fit_width(filter_block.width + 0.6)
        filter_label_group.next_to(filter_block, UP, buff=0.2)

        fib_l = filter_block.get_left()[0] + 0.18
        fib_r = filter_block.get_right()[0] - 0.18
        fib_y = filter_block.get_center()[1]
        fib_amp = (filter_block.height - 0.6) * 0.4

        def make_fib_point(sig_func):
            def coords(u):
                x = fib_l + u * (fib_r - fib_l)
                y = fib_y + sig_func(u) * fib_amp
                return np.array([x, y, 0])
            return coords

        inside_low_part = ParametricFunction(
            make_fib_point(slow_component),
            t_range=[0, 1, 0.001],
            color=GREEN,
            stroke_width=2.5,
        ).set_opacity(0.0)

        inside_spikes = ParametricFunction(
            make_fib_point(clean_signal),
            t_range=[0, 1, 0.001],
            color=YELLOW,
            stroke_width=2.5,
        ).set_opacity(0.0)

        lfp_label = Text("LFP component", font_size=18, color=GREEN).next_to(
            filter_block, DOWN, buff=0.2
        ).set_opacity(0.0)

        output_panel = Rectangle(
            width=4.4,
            height=2.4,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=GREY_E,
            fill_opacity=0.1,
        ).move_to(np.array([4.5, 0.2, 0])).set_opacity(0.0)

        out_l = output_panel.get_left()[0] + 0.3
        out_r = output_panel.get_right()[0] - 0.3
        out_y = output_panel.get_center()[1]
        out_amp = output_panel.height * 0.38

        def out_coords(u):
            x = out_l + u * (out_r - out_l)
            y = out_y + clean_signal(u) * out_amp
            return np.array([x, y, 0])

        clean_output = ParametricFunction(
            out_coords,
            t_range=[0, 1, 0.001],
            color=YELLOW,
            stroke_width=4,
        ).set_opacity(0.0)

        trace_copy = raw_trace_full.copy().scale_to_fit_width(1.1).set_opacity(0.0).move_to(ORIGIN)

        self.play(*[FadeOut(g) for g in label_groups], run_time=max(0.05, rt(0.6)))
        self.play(
            raw_panel_full.animate.scale(0.5).move_to(np.array([-3.4, 0.2, 0])),
            raw_trace_full.animate.scale(0.5).move_to(np.array([-3.4, 0.2, 0])),
            run_time=max(0.05, rt(1.3)),
        )
        self.play(GrowFromCenter(filter_block), FadeIn(filter_label_group), run_time=max(0.05, rt(0.8)))
        self.play(
            trace_copy.animate.move_to(
                np.array([filter_block.get_left()[0] - 0.55, 0.2, 0])
            ).set_opacity(0.5),
            run_time=max(0.05, rt(1.4)),
        )
        self.wait(max(0.05, rt(0.44)))

        # gap to Beat 8
        self.wait(max(0.05, rt(0.74)))

        # ---------- Beat 8: filtering animation ----------
        inside_low_part.set_opacity(1.0)
        inside_spikes.set_opacity(1.0)
        output_panel.set_opacity(1.0)
        lfp_label.set_opacity(1.0)

        self.play(
            trace_copy.animate.move_to(filter_block.get_center()).set_opacity(0.25),
            FadeIn(inside_low_part, inside_spikes),
            FadeIn(output_panel),
            run_time=max(0.05, rt(2.0)),
        )
        self.play(
            FadeIn(lfp_label),
            FadeOut(trace_copy),
            run_time=max(0.05, rt(0.6)),
        )

        clean_output.set_opacity(1.0)
        self.play(
            FadeOut(inside_low_part),
            FadeOut(lfp_label),
            Create(clean_output),
            run_time=max(0.05, rt(2.6)),
            rate_func=linear,
        )
        self.play(
            Indicate(filter_label_hz, color=YELLOW, scale_factor=1.25),
            run_time=max(0.05, rt(0.9)),
        )
        self.wait(max(0.05, rt(1.8)))

        # ---------- Beat 9: leave only isolated spike activity ----------
        self.play(
            FadeOut(raw_panel_full, raw_trace_full),
            FadeOut(filter_block),
            FadeOut(filter_label_group),
            FadeOut(inside_spikes),
            output_panel.animate.scale(1.55).move_to(ORIGIN),
            clean_output.animate.scale(1.55).move_to(ORIGIN),
            run_time=max(0.05, rt(1.6)),
        )

        output_group = VGroup(output_panel, clean_output)
        isolated_label = Text(
            "isolated spike activity", font_size=30, color=YELLOW
        ).next_to(output_group, UP, buff=0.35)

        self.play(FadeIn(isolated_label), run_time=max(0.05, rt(0.6)))
        self.wait(max(0.05, rt(0.84)))

        # ---------- Beat 10: mark individual spikes ----------
        time_axis = Line(
            np.array([
                output_group.get_left()[0] + 0.15,
                output_group.get_bottom()[1] - 0.5,
                0,
            ]),
            np.array([
                output_group.get_right()[0] - 0.15,
                output_group.get_bottom()[1] - 0.5,
                0,
            ]),
            color=WHITE,
            stroke_width=2,
        )
        self.play(Create(time_axis), run_time=max(0.05, rt(0.4)))

        axis_y = time_axis.get_start()[1]

        # 5 markers, sequential, within the remaining 2.86 s
        dot_time = 0.22
        line_time = 0.22
        wait_time = 0.132

        for c in spike_centers:
            pt = clean_output.point_from_proportion(c)
            dot = Dot(pt, radius=0.07, color=YELLOW, fill_opacity=1)
            vertical = Line(
                pt,
                np.array([pt[0], axis_y, 0]),
                color=WHITE,
                stroke_width=2,
            )
            self.play(GrowFromCenter(dot), run_time=max(0.05, rt(dot_time)))
            self.play(Create(vertical), run_time=max(0.05, rt(line_time)))
            self.wait(max(0.05, rt(wait_time)))