ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np
from manim.utils.color import interpolate_color

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}


class Scene14(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_neuron(color=PINK, scale_factor=1.0):
            soma = Circle(
                radius=0.20 * scale_factor,
                fill_color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            dendrites = VGroup(*[
                Line(ORIGIN, d * 0.34 * scale_factor, color=color, stroke_width=2)
                for d in (UP, DOWN, LEFT, RIGHT)
            ])
            axon = Line(ORIGIN, RIGHT * 0.44 * scale_factor, color=color, stroke_width=2)
            neuron = VGroup(dendrites, axon, soma)
            neuron.move_to(ORIGIN)
            return neuron

        def make_bolt(loc, scale=0.35):
            bolt = VMobject().set_points_as_corners([
                np.array([0, 0, 0]),
                np.array([0.12, 0.25, 0]),
                np.array([-0.04, 0.18, 0]),
                np.array([0.18, 0.55, 0]),
            ])
            bolt.set_stroke(YELLOW, width=3)
            bolt.scale(scale)
            bolt.move_to(loc)
            return bolt

        # ---------- BEAT 1 [0.00-1.54] ----------
        prev_pipeline = VGroup()
        for i, txt in enumerate([
            "Raw extracellular signal",
            "Filtering",
            "Spike / LFP components",
            "Feature extraction",
            "Neural interpretation / decoding",
        ]):
            box = Rectangle(
                width=3.0, height=0.55,
                fill_color=GREY, fill_opacity=0.85,
                stroke_color=WHITE, stroke_width=2,
            )
            label = Text(txt, font_size=13, color=WHITE)
            label.scale_to_fit_width(2.6)
            box.move_to([0, -i * 0.9, 0])
            label.move_to(box.get_center())
            prev_pipeline.add(VGroup(box, label))
        prev_pipeline.arrange(DOWN, buff=0.30)
        prev_pipeline.scale_to_fit_height(6.2)
        prev_pipeline.move_to(ORIGIN)
        self.add(prev_pipeline)

        recap_title = Text("Recap", font_size=76, color=WHITE, weight=BOLD)
        recap_title.move_to([0, 2.9, 0])
        divider_line = Line(
            recap_title.get_left() + DOWN * 0.45,
            recap_title.get_right() + DOWN * 0.45,
            color=GREY, stroke_width=5,
        ).set_opacity(0)

        self.play(
            prev_pipeline.animate.set_opacity(0.15).scale(0.75).move_to([0, 0.5, 0]),
            run_time=max(0.05, 0.54),
        )
        self.play(FadeIn(recap_title), run_time=max(0.05, 0.24))
        self.play(divider_line.animate.set_opacity(1), run_time=max(0.05, 0.34))
        self.play(prev_pipeline.animate.set_opacity(0.10), run_time=max(0.05, 0.20))
        self.play(recap_title.animate.set_color(YELLOW), run_time=max(0.05, 0.22))
        self.wait(max(0.05, 0.72))  # gap to 2.26

        # ---------- BEAT 2 [2.26-6.78] ----------
        spiky = lambda x: 0.28 * (np.sin(np.pi * x)) ** 40 - 0.12 * (np.sin(np.pi * (x - 0.35))) ** 40
        smooth = lambda x: 0.35 * np.sin(1.4 * x)

        spike_trace = FunctionGraph(
            spiky, x_range=[-4.2, 4.2, 0.02],
            color=BLUE, stroke_width=2.5,
        ).move_to([-2.8, 0.5, 0])
        lfp_trace = FunctionGraph(
            smooth, x_range=[-4.2, 4.2, 0.02],
            color=ORANGE, stroke_width=5,
        ).move_to([2.8, 0.5, 0])

        spike_label = Text("Spikes", font_size=24, color=BLUE, weight=BOLD)
        spike_label.next_to(spike_trace, DOWN, buff=0.25)
        lfp_label = Text("LFPs", font_size=24, color=ORANGE, weight=BOLD)
        lfp_label.next_to(lfp_trace, DOWN, buff=0.25)

        complement_caption = Text(
            "Two complementary views of neural activity",
            font_size=24, color=WHITE,
        ).move_to([0, 1.9, 0])

        self.play(
            FadeOut(recap_title, divider_line),
            FadeIn(spike_trace), FadeIn(spike_label),
            run_time=max(0.05, 0.30),
        )
        self.play(FadeIn(lfp_trace), FadeIn(lfp_label), run_time=max(0.05, 0.28))
        self.wait(max(0.05, 0.16))
        self.play(FadeIn(complement_caption), run_time=max(0.05, 0.36))
        self.play(Indicate(lfp_trace, color=ORANGE, scale_factor=1.08), run_time=max(0.05, 0.76))
        self.play(
            spike_trace.animate.set_stroke(BLUE, width=3.5, opacity=1),
            lfp_trace.animate.set_stroke(ORANGE, width=6, opacity=1),
            run_time=max(0.05, 0.24),
        )
        self.play(
            spike_trace.animate.shift(LEFT * 0.7),
            spike_label.animate.shift(LEFT * 0.7),
            lfp_trace.animate.shift(RIGHT * 0.7),
            lfp_label.animate.shift(RIGHT * 0.7),
            run_time=max(0.05, 0.42),
        )

        left_edge = spike_trace.get_right()
        right_edge = lfp_trace.get_left()
        gradient_bridge = VGroup()
        n_steps = 20
        for i in range(n_steps + 1):
            alpha = i / n_steps
            color = interpolate_color(BLUE, ORANGE, alpha)
            vline = Line(ORIGIN, UP * 1.0, color=color, stroke_width=12)
            x = left_edge[0] + (right_edge[0] - left_edge[0]) * alpha
            vline.move_to([x, 0.5, 0])
            vline.set_opacity(0.55)
            gradient_bridge.add(vline)
        self.play(FadeIn(gradient_bridge), run_time=max(0.05, 0.52))

        self.wait(max(0.05, 0.54))

        neuron_bg = make_neuron(PURPLE).scale(2.2).move_to([0, 0.5, 0])
        neuron_bg.set_opacity(0.2)
        self.play(FadeIn(neuron_bg), run_time=max(0.05, 0.30))
        self.play(neuron_bg.animate.set_opacity(0.50), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.44))
        self.wait(max(0.05, 0.88))  # gap to 7.66

        # ---------- BEAT 3 [7.66-12.78] ----------
        self.play(
            FadeOut(gradient_bridge), FadeOut(neuron_bg), FadeOut(complement_caption),
            lfp_trace.animate.set_opacity(0.25).shift(LEFT * 2.0),
            lfp_label.animate.shift(LEFT * 2.0).set_opacity(0.6),
            spike_trace.animate.move_to([0, 0.2, 0]),
            spike_label.animate.move_to([0, -0.8, 0]),
            run_time=max(0.05, 0.24),
        )
        self.play(spike_trace.animate.scale(1.1), run_time=max(0.05, 0.36))

        spike_caption = Text(
            "Brief, high-frequency electrical events",
            font_size=28, color=YELLOW,
        )
        spike_caption.next_to(spike_trace, UP, buff=0.45)
        self.play(FadeIn(spike_caption), run_time=max(0.05, 0.30))
        self.play(Indicate(spike_trace, color=BLUE, scale_factor=1.08), run_time=max(0.05, 0.64))
        self.play(spike_trace.animate.stretch(1.25, 1), run_time=max(0.05, 0.26))
        self.play(spike_trace.animate.shift(UP * 0.05), run_time=max(0.05, 0.12))
        self.play(spike_trace.animate.shift(DOWN * 0.10), run_time=max(0.05, 0.12))
        self.play(spike_trace.animate.shift(UP * 0.05), run_time=max(0.05, 0.12))

        lightning_ticks = VGroup()
        trace_center = spike_trace.get_center()
        for dx in [-2.2, -1.0, 0.4, 1.6, 2.6]:
            bolt = make_bolt([trace_center[0] + dx, trace_center[1] + 0.55, 0])
            lightning_ticks.add(bolt)
        self.play(FadeIn(lightning_ticks), run_time=max(0.05, 0.40))
        self.play(Indicate(spike_trace, color=BLUE, scale_factor=1.06), run_time=max(0.05, 0.66))

        neuron_icon_small = make_neuron(PINK).scale(0.85)
        neuron_icon_small.move_to([spike_trace.get_right()[0] + 0.8, 0.0, 0])
        self.play(GrowFromCenter(neuron_icon_small), run_time=max(0.05, 0.60))

        neuron_link = Line(
            neuron_icon_small.get_left(), spike_trace.get_right(),
            color=GREY, stroke_width=2,
        )
        self.play(Create(neuron_link), run_time=max(0.05, 0.58))

        flash_dot = Dot(neuron_icon_small.get_center(), radius=0.06, color=YELLOW, fill_opacity=1)
        self.add(flash_dot)
        self.play(MoveAlongPath(flash_dot, neuron_link), run_time=max(0.05, 0.22))
        self.remove(flash_dot)

        self.play(
            Indicate(spike_trace, color=BLUE),
            Indicate(neuron_icon_small, color=YELLOW),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.80))  # gap to 13.58

        # ---------- BEAT 4 [13.58-19.04] ----------
        self.play(
            FadeOut(spike_caption), FadeOut(lightning_ticks),
            FadeOut(neuron_icon_small), FadeOut(neuron_link),
            spike_trace.animate.move_to([-1.6, 1.5, 0]),
            spike_label.animate.move_to([-1.6, 0.7, 0]),
            run_time=max(0.05, 0.16),
        )
        self.play(spike_trace.animate.scale(0.90), run_time=max(0.05, 0.18))

        scale_bar = Rectangle(
            height=3.0, width=0.4,
            fill_color=GREY, fill_opacity=0.85,
            stroke_color=WHITE, stroke_width=2,
        ).move_to([3.2, 1.5, 0])
        scale_bar_label = Text("100 mV", font_size=20, color=YELLOW)
        scale_bar_label.next_to(scale_bar, UP, buff=0.15)
        scale_bar_group = VGroup(scale_bar, scale_bar_label)
        self.play(FadeIn(scale_bar_group), run_time=max(0.05, 0.12))
        self.play(spike_trace.animate.scale(0.88), run_time=max(0.05, 0.30))

        temporal_highlight = SurroundingRectangle(
            spike_trace, color=YELLOW, buff=0.08,
            corner_radius=0.05, stroke_width=3,
        )
        self.play(Create(temporal_highlight), run_time=max(0.05, 0.44))

        duration_bracket = VGroup(
            Line([-2.2, 0.5, 0], [-2.2, 1.0, 0], color=YELLOW, stroke_width=3),
            Line([-1.0, 0.5, 0], [-1.0, 1.0, 0], color=YELLOW, stroke_width=3),
        )
        self.play(FadeIn(duration_bracket), run_time=max(0.05, 0.28))

        time_axis = Line([-4.8, -0.4, 0], [4.8, -0.4, 0], color=GREY, stroke_width=3)
        time_label = Text("time", font_size=18, color=GREY)
        time_label.next_to(time_axis, RIGHT, buff=0.10)
        time_axis_group = VGroup(time_axis, time_label)
        self.play(FadeIn(time_axis_group), run_time=max(0.05, 0.22))

        sliver_highlight = Rectangle(
            width=0.55, height=0.25,
            fill_color=BLUE, fill_opacity=0.6,
            stroke_color=BLUE, stroke_width=2,
        ).move_to(time_axis.get_center() + LEFT * 1.8)
        self.play(FadeIn(sliver_highlight), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.72))

        self.play(Indicate(spike_trace, color=BLUE), run_time=max(0.05, 0.10))

        warn_tri = Polygon(
            [0, 0.4, 0], [0.35, -0.3, 0], [-0.35, -0.3, 0],
            fill_color=YELLOW, fill_opacity=0.9,
            stroke_color=YELLOW, stroke_width=1,
        )
        warn_mark = Text("!", font_size=28, color=BLACK)
        warn_mark.move_to(warn_tri.get_center() + DOWN * 0.08)
        warning_icon = VGroup(warn_tri, warn_mark).move_to([3.2, 0.4, 0])
        self.play(FadeIn(warning_icon), run_time=max(0.05, 0.30))
        self.play(Indicate(warning_icon, color=ORANGE), run_time=max(0.05, 0.56))

        filter_icon = FunctionGraph(
            lambda x: 0.32 * np.sin(8 * x),
            x_range=[-0.5, 0.5, 0.02],
            color=BLUE, stroke_width=3,
        )
        highpass_label = Text("High-pass filtering", font_size=22, color=WHITE)
        highpass_group = VGroup(filter_icon, highpass_label).arrange(RIGHT, buff=0.3)
        highpass_group.move_to([-3.4, -2.3, 0])
        self.play(FadeIn(highpass_group), run_time=max(0.05, 0.50))

        detect_icon = FunctionGraph(
            lambda x: 0.25 * np.sin(14 * x),
            x_range=[-0.4, 0.4, 0.02],
            color=BLUE, stroke_width=3,
        )
        detection_label = Text("Spike detection", font_size=22, color=WHITE)
        detection_group = VGroup(detect_icon, detection_label).arrange(RIGHT, buff=0.3)
        detection_group.move_to([3.4, -2.3, 0])
        self.play(FadeIn(detection_group), run_time=max(0.05, 0.52))
        self.wait(max(0.05, 0.26))
        self.play(
            Indicate(VGroup(highpass_group, detection_group), color=YELLOW),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.86))  # gap to 19.90

        # ---------- BEAT 5 [19.90-22.84] ----------
        self.play(
            highpass_group.animate.set_opacity(0.35),
            detection_group.animate.set_opacity(0.35),
            FadeOut(scale_bar_group),
            FadeOut(time_axis_group),
            FadeOut(duration_bracket),
            FadeOut(temporal_highlight),
            FadeOut(sliver_highlight),
            FadeOut(warning_icon),
            run_time=max(0.05, 0.16),
        )

        sorting_label = Text("Spike sorting", font_size=22, color=YELLOW, weight=BOLD)
        sorting_label.move_to([0, -2.75, 0])
        self.play(FadeIn(sorting_label), run_time=max(0.05, 0.32))

        spike_trace_solid = spike_trace.copy()
        spike_trace_solid.set_color(BLUE).move_to([0, 1.2, 0])
        spike_trace_dashed = DashedVMobject(spike_trace.copy(), num_dashes=30).set_color(TEAL)
        spike_trace_dashed.move_to([0, 1.2, 0])
        self.play(FadeIn(spike_trace_solid), FadeIn(spike_trace_dashed), run_time=max(0.05, 0.44))

        self.play(
            spike_trace_solid.animate.shift(LEFT * 0.25),
            spike_trace_dashed.animate.shift(RIGHT * 0.25),
            run_time=max(0.05, 0.20),
        )
        self.play(
            spike_trace_solid.animate.set_color(BLUE).move_to([-1.2, 1.2, 0]),
            spike_trace_dashed.animate.set_color(TEAL).move_to([1.4, 1.2, 0]),
            run_time=max(0.05, 0.46),
        )
        self.play(Indicate(spike_trace_solid, color=BLUE), run_time=max(0.05, 0.20))
        self.play(Indicate(spike_trace_dashed, color=TEAL), run_time=max(0.05, 0.20))

        divider_line_sort = Line([0, 0.0, 0], [0, 2.2, 0], color=GREY, stroke_width=2)
        self.play(FadeIn(divider_line_sort), run_time=max(0.05, 0.42))
        self.wait(max(0.05, 0.26))

        neuron_left2 = make_neuron(BLUE).scale(0.6)
        neuron_left2.move_to(spike_trace_solid.get_left() + LEFT * 0.7)
        neuron_right2 = make_neuron(TEAL).scale(0.6)
        neuron_right2.move_to(spike_trace_dashed.get_right() + RIGHT * 0.7)
        link_left2 = Line(neuron_left2.get_right(), spike_trace_solid.get_left(), color=BLUE, stroke_width=2)
        link_right2 = Line(neuron_right2.get_left(), spike_trace_dashed.get_right(), color=TEAL, stroke_width=2)
        self.play(
            FadeIn(neuron_left2), FadeIn(neuron_right2),
            FadeIn(link_left2), FadeIn(link_right2),
            run_time=max(0.05, 0.28),
        )

        spike_sorting_group = VGroup(
            spike_trace_solid, spike_trace_dashed,
            highpass_group, detection_group, sorting_label,
            divider_line_sort, neuron_left2, neuron_right2,
            link_left2, link_right2,
        )
        self.wait(max(0.05, 0.92))  # gap to 23.76

        # ---------- BEAT 6 [23.76-30.88] ----------
        self.play(
            spike_sorting_group.animate.set_opacity(0.25).shift(LEFT * 3.0),
            lfp_trace.animate.set_opacity(1).move_to([0, -0.2, 0]),
            lfp_label.animate.set_opacity(1).move_to([0, -0.55, 0]),
            run_time=max(0.05, 0.46),
        )
        self.play(lfp_trace.animate.scale(1.25), run_time=max(0.05, 0.30))

        lfp_label_main = Text("LFPs", font_size=28, color=ORANGE, weight=BOLD)
        lfp_label_main.next_to(lfp_trace, UP, buff=0.25)
        self.play(FadeIn(lfp_label_main), FadeOut(lfp_label), run_time=max(0.05, 0.76))

        lfp_caption = Text("Slower electrical activity", font_size=26, color=YELLOW)
        lfp_caption.next_to(lfp_trace, DOWN, buff=0.4)
        self.play(FadeIn(lfp_caption), run_time=max(0.05, 0.22))

        lfp_slower = FunctionGraph(
            lambda x: 0.33 * np.sin(0.7 * x),
            x_range=[-4.5, 4.5, 0.01],
            color=ORANGE, stroke_width=5,
        ).move_to(lfp_trace.get_center())
        self.play(ReplacementTransform(lfp_trace, lfp_slower), run_time=max(0.05, 0.58))
        lfp_main = lfp_slower

        lfp_glow = lfp_main.copy().set_stroke(ORANGE, width=12).set_opacity(0.25)
        self.play(FadeIn(lfp_glow), run_time=max(0.05, 0.34))
        self.play(Indicate(lfp_main, color=ORANGE), run_time=max(0.05, 0.66))

        lfp_neuron_cluster = VGroup()
        for i in range(7):
            ang = i * 2 * np.pi / 7
            r = 1.4
            lfp_neuron_cluster.add(
                make_neuron(PINK).scale(0.45).move_to([r * np.cos(ang), r * np.sin(ang) - 0.2, 0])
            )
        self.play(FadeIn(lfp_neuron_cluster), run_time=max(0.05, 0.92))

        cluster_links = VGroup()
        for neuron in lfp_neuron_cluster:
            cluster_links.add(Line(neuron.get_center(), lfp_main.get_center(), color=GREY, stroke_width=1.5))
        self.play(FadeIn(cluster_links), run_time=max(0.05, 0.22))

        self.play(
            lfp_neuron_cluster.animate.scale(1.4),
            cluster_links.animate.scale(1.4),
            run_time=max(0.05, 0.44),
        )

        extra_neurons = VGroup()
        for i in range(8):
            ang = i * np.pi / 4 + 0.3
            r = 2.2
            extra_neurons.add(
                make_neuron(PURPLE).scale(0.35).move_to([r * np.cos(ang), r * np.sin(ang) - 0.2, 0])
            )
        self.play(FadeIn(extra_neurons), run_time=max(0.05, 0.42))
        self.wait(max(0.05, 0.26))

        electrode_icon = VGroup(
            Rectangle(
                width=0.22, height=0.8,
                fill_color=YELLOW, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ),
            Line(ORIGIN, DOWN * 0.2, color=YELLOW, stroke_width=2),
        )
        electrode_icon.move_to([0, -0.2, 0])
        self.play(FadeIn(electrode_icon), run_time=max(0.05, 0.66))
        self.play(Indicate(electrode_icon, color=YELLOW), run_time=max(0.05, 0.14))

        electrode_label = Text("recording electrode", font_size=20, color=YELLOW)
        electrode_label.next_to(electrode_icon, DOWN, buff=0.15)
        self.play(FadeIn(electrode_label), run_time=max(0.05, 0.30))
        self.play(
            Indicate(electrode_icon, color=YELLOW),
            Indicate(lfp_main, color=ORANGE),
            run_time=max(0.05, 0.44),
        )
        self.wait(max(0.05, 0.92))  # gap to 31.80

        # ---------- BEAT 7 [31.80-36.08] ----------
        self.play(lfp_main.animate.set_stroke(ORANGE, width=6, opacity=1), run_time=max(0.05, 0.12))

        info_caption = Text(
            "Information about local population activity and neural oscillations",
            font_size=24, color=WHITE,
        ).move_to([0, 2.8, 0])
        self.play(FadeIn(info_caption), run_time=max(0.05, 0.62))
        self.play(Indicate(lfp_neuron_cluster, color=YELLOW), run_time=max(0.05, 0.52))
        self.play(Indicate(lfp_neuron_cluster, color=PINK), run_time=max(0.05, 0.22))
        self.play(Indicate(lfp_main, color=ORANGE), run_time=max(0.05, 0.56))
        self.wait(max(0.05, 0.52))

        osc_trace = FunctionGraph(
            lambda x: 0.30 * np.sin(2.5 * x),
            x_range=[-4.5, 4.5, 0.01],
            color=PURPLE, stroke_width=4,
        ).move_to(lfp_main.get_center())
        self.play(FadeIn(osc_trace), run_time=max(0.05, 0.62))
        osc_label = Text("neural oscillations", font_size=22, color=PURPLE, weight=BOLD)
        osc_label.next_to(osc_trace, DOWN, buff=0.30)
        self.play(FadeIn(osc_label), run_time=max(0.05, 0.26))
        self.play(Indicate(osc_trace, color=PURPLE), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.22))
        self.play(Indicate(osc_trace, color=PURPLE), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.22))
        self.wait(max(0.05, 0.48))  # gap to 36.56

        # ---------- BEAT 8 [36.56-40.62] ----------
        self.play(
            FadeOut(info_caption), FadeOut(osc_trace), FadeOut(osc_label),
            FadeOut(lfp_neuron_cluster), FadeOut(extra_neurons), FadeOut(cluster_links),
            FadeOut(electrode_icon), FadeOut(electrode_label), FadeOut(lfp_glow),
            FadeOut(lfp_label_main), FadeOut(lfp_caption),
            run_time=max(0.05, 0.20),
        )

        spiky2 = lambda x: 0.20 * (np.sin(np.pi * x)) ** 30 - 0.08 * (np.sin(np.pi * (x - 0.4))) ** 30
        smooth2 = lambda x: 0.25 * np.sin(1.5 * x)

        spike_eq = FunctionGraph(spiky2, x_range=[-3.6, 3.6, 0.02], color=BLUE, stroke_width=3)
        lfp_eq = FunctionGraph(smooth2, x_range=[-3.6, 3.6, 0.02], color=ORANGE, stroke_width=5)
        spike_eq.move_to([-1.8, 1.2, 0])
        lfp_eq.move_to([1.8, 1.2, 0])
        spike_label_eq = Text("Spikes", font_size=24, color=BLUE, weight=BOLD)
        spike_label_eq.next_to(spike_eq, DOWN, buff=0.25)
        lfp_label_eq = Text("LFPs", font_size=24, color=ORANGE, weight=BOLD)
        lfp_label_eq.next_to(lfp_eq, DOWN, buff=0.25)

        self.play(
            FadeIn(spike_eq), FadeIn(lfp_eq),
            FadeIn(spike_label_eq), FadeIn(lfp_label_eq),
            run_time=max(0.05, 0.84),
        )
        self.play(
            spike_eq.animate.set_stroke(BLUE, width=4, opacity=1),
            lfp_eq.animate.set_stroke(ORANGE, width=7, opacity=1),
            run_time=max(0.05, 0.22),
        )
        connect_line = Line(spike_eq.get_right(), lfp_eq.get_left(), color=GREY, stroke_width=2)
        self.play(Create(connect_line), run_time=max(0.05, 0.36))

        down_arrow = Arrow([0, 0.5, 0], [0, -0.5, 0], color=WHITE, stroke_width=5)
        self.play(FadeIn(down_arrow), run_time=max(0.05, 0.42))
        self.play(down_arrow.animate.shift(DOWN * 0.5), run_time=max(0.05, 0.22))

        col_width = 3.4
        col_height = 3.0
        col_bottom = -3.0
        col_centers = [-4.2, 0, 4.2]
        columns = VGroup()
        for cx in col_centers:
            rect = Rectangle(width=col_width, height=col_height, fill_color=GREY, fill_opacity=0.1,
                              stroke_color=WHITE, stroke_width=2)
            rect.move_to([cx, col_bottom + col_height/2, 0])
            columns.add(rect)
        self.play(FadeIn(columns), run_time=max(0.05, 0.22))

        col_labels = VGroup()
        col_names = ["Neural coding", "Circuit analysis", "Neural prostheses"]
        for i, name in enumerate(col_names):
            lab = Text(name, font_size=22, color=WHITE, weight=BOLD)
            lab.next_to(columns[i], UP, buff=0.15)
            col_labels.add(lab)
            self.play(FadeIn(lab), run_time=max(0.05, 0.16))
        self.wait(max(0.05, 0.02))  # total labels 3*0.16=0.48, need 0.50 for 38.84-39.34
        self.play(col_labels[0].animate.set_color(YELLOW), run_time=max(0.05, 0.34))

        neuron_coding = make_neuron(PINK).scale(0.7)
        neuron_coding.move_to(columns[0].get_center() + UP * 0.6)
        self.play(GrowFromCenter(neuron_coding), run_time=max(0.05, 0.94))

        # ---------- BEAT 9 [40.62-43.04] ----------
        encoding_caption = Text("How information is represented", font_size=18, color=WHITE)
        encoding_caption.scale_to_fit_width(col_width - 1.0)
        encoding_caption.move_to(columns[0].get_bottom() + UP * 0.8)
        self.play(FadeIn(encoding_caption), run_time=max(0.05, 0.48))
        self.play(Indicate(neuron_coding, color=YELLOW), run_time=max(0.05, 0.52))

        encoding_dots = VGroup()
        for i in range(4):
            dot = Dot(radius=0.06, color=BLUE, fill_opacity=1)
            dot.move_to(columns[0].get_center() + UP * 0.2 + RIGHT * (i * 0.4 - 0.6))
            encoding_dots.add(dot)
        self.play(FadeIn(encoding_dots), run_time=max(0.05, 0.44))
        self.play(Indicate(encoding_dots, color=BLUE), run_time=max(0.05, 0.32))

        coding_link = Line(neuron_coding.get_bottom(), encoding_dots.get_top(), color=GREY, stroke_width=1.5)
        self.play(Create(coding_link), run_time=max(0.05, 0.24))
        self.play(Indicate(columns[0], color=YELLOW), run_time=max(0.05, 0.42))

        self.wait(max(0.05, 0.86))  # gap to 43.90

        # ---------- BEAT 10 [43.90-47.10] ----------
        self.play(col_labels[1].animate.set_color(YELLOW), run_time=max(0.05, 0.32))

        net_neurons = VGroup()
        positions = [
            columns[1].get_center() + UP * 0.7 + LEFT * 0.9,
            columns[1].get_center() + UP * 0.7 + RIGHT * 0.9,
            columns[1].get_center() + DOWN * 0.5 + LEFT * 1.0,
            columns[1].get_center() + DOWN * 0.5 + RIGHT * 1.0,
        ]
        for pos in positions:
            n = make_neuron(TEAL).scale(0.45)
            n.move_to(pos)
            net_neurons.add(n)
        self.play(FadeIn(net_neurons), run_time=max(0.05, 0.70))

        net_arrows = VGroup()
        for i in range(len(net_neurons)-1):
            for j in range(i+1, len(net_neurons)):
                if np.linalg.norm(net_neurons[i].get_center() - net_neurons[j].get_center()) < 2.5:
                    arrow = Arrow(net_neurons[i].get_center(), net_neurons[j].get_center(), color=GREY, stroke_width=2, buff=0.15)
                    net_arrows.add(arrow)
        self.play(FadeIn(net_arrows), run_time=max(0.05, 0.40))

        circuit_caption = Text("How different neural populations interact", font_size=18, color=WHITE)
        circuit_caption.scale_to_fit_width(col_width - 0.8)
        circuit_caption.move_to(columns[1].get_bottom() + UP * 0.8)
        self.play(FadeIn(circuit_caption), run_time=max(0.05, 0.20))

        group1 = VGroup(net_neurons[0], net_neurons[2])
        group2 = VGroup(net_neurons[1], net_neurons[3])
        self.play(
            group1.animate.set_color(BLUE),
            group2.animate.set_color(ORANGE),
            run_time=max(0.05, 0.28),
        )
        self.play(Indicate(net_neurons, color=YELLOW), run_time=max(0.05, 0.22))
        self.wait(max(0.05, 0.60))
        for arrow in net_arrows:
            self.play(Indicate(arrow, color=YELLOW), run_time=max(0.05, 0.24))
        self.wait(max(0.05, 0.48))
        self.wait(max(0.05, 0.76))  # gap to 47.86

        # ---------- BEAT 11 [47.86-52.70] ----------
        self.play(col_labels[2].animate.set_color(YELLOW), run_time=max(0.05, 0.14))

        arm_base = Rectangle(width=0.8, height=0.2, fill_color=GREY, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
        arm_base.move_to(columns[2].get_bottom() + UP * 0.6)
        arm_link1 = Line(arm_base.get_top(), arm_base.get_top() + UP * 0.7, color=GREY, stroke_width=6)
        arm_joint = Circle(radius=0.08, fill_color=GREY, fill_opacity=1, stroke_color=WHITE, stroke_width=1).move_to(arm_link1.get_end())
        arm_gripper = VGroup(
            Rectangle(width=0.1, height=0.35, fill_color=GREY, fill_opacity=1, stroke_color=WHITE, stroke_width=0.5).rotate(PI/4).move_to(arm_joint.get_center()+RIGHT*0.25+UP*0.2),
            Rectangle(width=0.1, height=0.35, fill_color=GREY, fill_opacity=1, stroke_color=WHITE, stroke_width=0.5).rotate(-PI/4).move_to(arm_joint.get_center()+RIGHT*0.25+DOWN*0.2),
        )
        prosthetic_arm = VGroup(arm_base, arm_link1, arm_joint, arm_gripper).move_to(columns[2].get_center() + UP * 0.7)
        self.play(FadeIn(prosthetic_arm), run_time=max(0.05, 0.26))
        self.wait(max(0.05, 1.10))

        prost_caption = Text("How neural activity can be decoded to control external devices", font_size=18, color=WHITE)
        prost_caption.scale_to_fit_width(col_width - 0.8)
        prost_caption.move_to(columns[2].get_bottom() + UP * 0.8)
        self.play(FadeIn(prost_caption), run_time=max(0.05, 0.20))

        brain_icon_small = SVGMobject(ASSET_PATHS["brain"], fill_color=PINK, fill_opacity=1, stroke_color=WHITE, stroke_width=1).scale(0.7)
        brain_icon_small.move_to(columns[2].get_left() + RIGHT * 0.8 + UP * 0.6)
        self.play(FadeIn(brain_icon_small), run_time=max(0.05, 0.24))
        self.play(Indicate(brain_icon_small, color=PINK), run_time=max(0.05, 0.46))

        dashed_link = DashedLine(brain_icon_small.get_right(), prosthetic_arm.get_left(), color=GREY, dash_length=0.1)
        self.play(FadeIn(dashed_link), run_time=max(0.05, 0.42))
        solid_link = Line(brain_icon_small.get_right(), prosthetic_arm.get_left(), color=WHITE, stroke_width=2)
        self.play(ReplacementTransform(dashed_link, solid_link), run_time=max(0.05, 0.12))
        self.play(
            Indicate(brain_icon_small, color=PINK),
            prosthetic_arm.animate.shift(RIGHT * 0.2),
            run_time=max(0.05, 0.44),
        )
        self.play(solid_link.animate.set_color(YELLOW), run_time=max(0.05, 0.22))
        self.play(
            prosthetic_arm.animate.shift(LEFT * 0.1).rotate(PI/6, about_point=arm_joint.get_center()),
            run_time=max(0.05, 0.36),
        )
        external_label = Text("external device", font_size=20, color=YELLOW, weight=BOLD)
        external_label.next_to(prosthetic_arm, DOWN, buff=0.2)
        self.play(FadeIn(external_label), run_time=max(0.05, 0.40))
        self.play(prosthetic_arm.animate.shift(RIGHT * 0.2), run_time=max(0.05, 0.24))
        self.play(prosthetic_arm.animate.shift(LEFT * 0.2), run_time=max(0.05, 0.24))

        # ---------- BEAT 12 [52.70-59.40] ----------
        layout_group = VGroup(columns, col_labels, neuron_coding, encoding_dots, coding_link,
                              net_neurons, net_arrows, circuit_caption,
                              prosthetic_arm, brain_icon_small, solid_link, external_label)
        self.play(
            layout_group.animate.set_opacity(0.25).shift(UP * 0.5).scale(0.85),
            FadeOut(down_arrow),
            FadeOut(connect_line),
            spike_eq.animate.set_opacity(0.4),
            lfp_eq.animate.set_opacity(0.4),
            spike_label_eq.animate.set_opacity(0.5),
            lfp_label_eq.animate.set_opacity(0.5),
            run_time=max(0.05, 1.46),
        )

        center_dot = Dot(ORIGIN, radius=0.1, color=WHITE, fill_opacity=1)
        self.play(FadeIn(center_dot), run_time=max(0.05, 0.16))

        tissue_view = VGroup()
        for i in range(5):
            pos = np.array([-4 + i*2.5, 3 - i*0.6, 0])
            n = make_neuron(PINK, scale_factor=0.5).move_to(pos)
            tissue_view.add(n)
        for i in range(3):
            pos = np.array([-3 + i*3, -1.5, 0])
            cluster = VGroup(*[make_neuron(PURPLE, scale_factor=0.3).move_to(pos + np.array([r*np.cos(a), r*np.sin(a), 0])) for r, a in [(0.25,0),(0.25,2*np.pi/3),(0.25,4*np.pi/3)]])
            tissue_view.add(cluster)
        tissue_view.scale_to_fit_width(10)
        tissue_view.move_to(ORIGIN)
        self.play(FadeOut(center_dot), FadeIn(tissue_view), run_time=max(0.05, 0.36))
        self.play(Indicate(tissue_view, color=YELLOW), run_time=max(0.05, 0.24))

        overlay_spike = spike_eq.copy().set_opacity(0.5).move_to([0,1.5,0])
        overlay_lfp = lfp_eq.copy().set_opacity(0.5).move_to([0,-1.5,0])
        self.play(FadeIn(overlay_spike), FadeIn(overlay_lfp), run_time=max(0.05, 0.40))
        overlay_link1 = Line(overlay_spike.get_bottom(), tissue_view.get_top(), color=GREY, stroke_width=1)
        overlay_link2 = Line(overlay_lfp.get_top(), tissue_view.get_top(), color=GREY, stroke_width=1)
        self.play(Create(overlay_link1), Create(overlay_link2), run_time=max(0.05, 0.44))

        small_neurons = VGroup(*[make_neuron(BLUE, scale_factor=0.3).move_to(tissue_view[n].get_center() + RIGHT*0.3) for n in [0,2,4]])
        self.play(FadeIn(small_neurons), run_time=max(0.05, 0.46))
        self.play(Indicate(small_neurons[0], color=YELLOW), run_time=max(0.05, 0.48))
        self.play(Indicate(small_neurons[0], color=BLUE), run_time=max(0.05, 0.38))
        self.play(Indicate(tissue_view[1], color=PURPLE), run_time=max(0.05, 0.72))

        local_label = Text("local populations", font_size=22, color=PURPLE, weight=BOLD)
        local_label.next_to(tissue_view[1], DOWN, buff=0.15)
        self.play(FadeIn(local_label), run_time=max(0.05, 0.20))
        self.play(Indicate(tissue_view[1], color=PURPLE), run_time=max(0.05, 0.72))
        self.play(tissue_view.animate.scale(0.7).move_to([0, -0.2, 0]), run_time=max(0.05, 0.68))

        # ---------- BEAT 13 [59.40-64.56] ----------
        brain_icon_large = SVGMobject(ASSET_PATHS["brain"], fill_color=PINK, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1).scale(2.4)
        brain_icon_large.move_to([0, -0.2, 0])
        self.play(
            FadeOut(tissue_view), FadeOut(overlay_spike), FadeOut(overlay_lfp),
            FadeOut(overlay_link1), FadeOut(overlay_link2), FadeOut(small_neurons),
            FadeOut(local_label),
            FadeIn(brain_icon_large),
            run_time=max(0.05, 0.74),
        )
        self.play(brain_icon_large.animate.set_fill(PINK, opacity=1), run_time=max(0.05, 0.38))
        self.wait(max(0.05, 0.50))
        self.play(brain_icon_large.animate.rotate(PI/8), run_time=max(0.05, 0.56))

        head_outline = Circle(radius=2.2, fill_color=GREY, fill_opacity=0.08, stroke_color=GREY, stroke_width=4)
        head_outline.move_to(brain_icon_large.get_center())
        self.play(FadeIn(head_outline), run_time=max(0.05, 0.66))
        self.play(head_outline.animate.set_stroke(WHITE, width=5), run_time=max(0.05, 0.28))
        self.play(Indicate(brain_icon_large, color=YELLOW), run_time=max(0.05, 0.30))

        field_lines = VGroup()
        angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
        for ang in angles:
            start = brain_icon_large.get_center() + np.array([np.cos(ang)*1.3, np.sin(ang)*1.3, 0])
            end = head_outline.get_center() + np.array([np.cos(ang)*2.4, np.sin(ang)*2.4, 0])
            line = Line(start, end, color=TEAL, stroke_width=2)
            field_lines.add(line)
        self.play(FadeIn(field_lines), run_time=max(0.05, 0.52))

        meg_sensors = VGroup()
        sensor_positions = [
            head_outline.get_center() + UP*2.4,
            head_outline.get_center() + DOWN*2.4,
            head_outline.get_center() + LEFT*2.4,
            head_outline.get_center() + RIGHT*2.4,
            head_outline.get_center() + UP*1.8 + RIGHT*1.2,
            head_outline.get_center() + UP*1.8 + LEFT*1.2,
            head_outline.get_center() + DOWN*1.8 + RIGHT*1.2,
            head_outline.get_center() + DOWN*1.8 + LEFT*1.2,
        ]
        for pos in sensor_positions:
            sensor = Rectangle(width=0.4, height=0.8, fill_color=GREY, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1).move_to(pos)
            meg_sensors.add(sensor)
        meg_helmet = VGroup(head_outline.copy(), meg_sensors)
        self.play(FadeIn(meg_helmet), run_time=max(0.05, 0.44))
        self.play(meg_helmet.animate.set_opacity(0.85), run_time=max(0.05, 0.26))
        self.play(meg_helmet.animate.set_opacity(1), run_time=max(0.05, 0.34))

        meg_label = Text("MEG", font_size=48, color=YELLOW, weight=BOLD)
        meg_label.next_to(meg_helmet, UP, buff=0.5)
        self.play(FadeIn(meg_label), run_time=max(0.05, 0.18))
        self.wait(max(0.05, 0.80))  # gap to 65.36

        # ---------- BEAT 14 [65.36-68.52] ----------
        self.play(Indicate(meg_label, color=YELLOW), run_time=max(0.05, 0.22))
        self.wait(max(0.05, 0.10))
        self.play(
            VGroup(brain_icon_large, head_outline, field_lines, meg_helmet, meg_label).animate.scale(0.9).move_to([0, 0.6, 0]),
            run_time=max(0.05, 0.16),
        )
        self.play(meg_helmet.animate.set_stroke(YELLOW, width=4), run_time=max(0.05, 0.90))

        question_mark = Text("?", font_size=56, color=WHITE, weight=BOLD)
        question_mark.move_to([0, -2.8, 0])
        self.play(FadeIn(question_mark), run_time=max(0.05, 0.22))

        meg_full_text1 = Text("Magnetoencephalography", font_size=30, color=YELLOW, weight=BOLD)
        meg_full_text1.move_to([0, -2.8, 0])
        self.play(FadeOut(question_mark), FadeIn(meg_full_text1), run_time=max(0.05, 0.30))

        meg_full_text2 = Text("(MEG)", font_size=30, color=YELLOW, weight=BOLD)
        meg_full_text2.next_to(meg_full_text1, RIGHT, buff=0.4)
        self.play(FadeIn(meg_full_text2), run_time=max(0.05, 0.72))

        meg_title = VGroup(meg_full_text1, meg_full_text2).move_to([0, -2.8, 0])
        self.play(meg_title.animate.scale(1.05), run_time=max(0.05, 0.12))
        self.play(Indicate(meg_title, color=YELLOW), run_time=max(0.05, 0.42))
        self.wait(max(0.05, 0.46))  # gap to 68.98

        # ---------- BEAT 15 [68.98-79.08] ----------
        self.play(Indicate(meg_full_text2, color=YELLOW), run_time=max(0.05, 0.18))
        self.play(Indicate(meg_helmet, color=YELLOW), run_time=max(0.05, 0.84))
        self.play(field_lines.animate.set_color(TEAL).set_stroke(TEAL, width=4), run_time=max(0.05, 0.20))
        self.play(Indicate(field_lines, color=TEAL), run_time=max(0.05, 0.18))

        mag_caption = Text("Magnetic fields generated by neural activity", font_size=24, color=WHITE)
        mag_caption.to_edge(UP, buff=0.4)
        self.play(FadeIn(mag_caption), run_time=max(0.05, 0.22))
        self.play(field_lines.animate.set_stroke(TEAL, width=5), run_time=max(0.05, 0.28))
        self.play(field_lines.animate.set_stroke(TEAL, width=7), run_time=max(0.05, 0.46))
        self.play(Indicate(brain_icon_large, color=YELLOW), run_time=max(0.05, 0.46))
        self.play(field_lines.animate.set_stroke(TEAL, width=5), run_time=max(0.05, 0.50))
        self.play(Indicate(brain_icon_large, color=YELLOW), run_time=max(0.05, 0.24))
        self.play(Indicate(field_lines, color=TEAL), run_time=max(0.05, 0.50))

        func_caption = Text("Functional brain mapping and timing of neural processes", font_size=22, color=WHITE)
        func_caption.to_edge(UP, buff=1.2)
        self.play(FadeIn(func_caption), run_time=max(0.05, 0.70))
        self.play(func_caption.animate.set_opacity(0.6), run_time=max(0.05, 0.14))
        self.play(func_caption.animate.set_opacity(1), run_time=max(0.05, 0.28))

        brain_map_overlay = VGroup(
            Ellipse(width=1.8, height=1.2, fill_color=PINK, fill_opacity=0.25, stroke_color=WHITE, stroke_width=1).move_to([-0.8, 0.8, 0]),
            Ellipse(width=1.4, height=0.9, fill_color=BLUE, fill_opacity=0.25, stroke_color=WHITE, stroke_width=1).move_to([0.8, -0.4, 0]),
            Ellipse(width=1.0, height=0.7, fill_color=GREEN, fill_opacity=0.25, stroke_color=WHITE, stroke_width=1).move_to([0.1, 0.9, 0]),
        )
        self.play(FadeIn(brain_map_overlay), run_time=max(0.05, 0.26))
        self.play(brain_map_overlay.animate.set_fill(opacity=0.5), run_time=max(0.05, 0.40))
        self.play(Indicate(brain_map_overlay, color=YELLOW), run_time=max(0.05, 0.32))
        self.wait(max(0.05, 0.44))

        stopwatch_icon = SVGMobject(ASSET_PATHS["stopwatch"], fill_color=WHITE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1).scale(0.8)
        stopwatch_icon.move_to([4.5, -1.2, 0])
        self.play(FadeIn(stopwatch_icon), run_time=max(0.05, 0.66))
        self.play(Indicate(stopwatch_icon, color=YELLOW), run_time=max(0.05, 0.38))

        timing_label = Text("timing", font_size=22, color=YELLOW, weight=BOLD)
        timing_label.next_to(stopwatch_icon, DOWN, buff=0.2)
        self.play(FadeIn(timing_label), run_time=max(0.05, 0.24))
        self.play(timing_label.animate.set_color(WHITE), run_time=max(0.05, 0.28))

        timeline_link = Line(stopwatch_icon.get_left(), brain_map_overlay.get_right(), color=GREY, stroke_width=2)
        self.play(Create(timeline_link), run_time=max(0.05, 0.24))
        self.play(Indicate(brain_icon_large, color=PINK), run_time=max(0.05, 0.24))
        self.play(
            Indicate(stopwatch_icon, color=YELLOW),
            Indicate(brain_map_overlay, color=YELLOW),
            run_time=max(0.05, 0.52),
        )

        # final fade to black at 79.08
        self.play(FadeOut(*self.mobjects), run_time=max(0.05, 0.94))