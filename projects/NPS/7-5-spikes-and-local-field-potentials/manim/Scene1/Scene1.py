ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        rt = lambda t: max(0.05, t)

        # ---------- Beat 1: single neuron ----------
        soma = Circle(
            radius=0.6,
            color=WHITE,
            stroke_width=3,
            fill_color=BLUE_E,
            fill_opacity=0.18,
        ).move_to(ORIGIN)

        dendrites = VGroup(
            Line([0, 0.6, 0], [0, 1.3, 0], color=WHITE, stroke_width=3),
            Line([0, 1.3, 0], [-0.9, 2.0, 0], color=WHITE, stroke_width=3),
            Line([0, 1.3, 0], [0.9, 2.0, 0], color=WHITE, stroke_width=3),
            Line([-0.9, 2.0, 0], [-1.4, 2.6, 0], color=WHITE, stroke_width=2),
            Line([-0.9, 2.0, 0], [-0.5, 2.7, 0], color=WHITE, stroke_width=2),
            Line([0.9, 2.0, 0], [1.4, 2.6, 0], color=WHITE, stroke_width=2),
            Line([0.9, 2.0, 0], [0.5, 2.7, 0], color=WHITE, stroke_width=2),
            Line([-0.3, 0.8, 0], [-1.3, 1.5, 0], color=WHITE, stroke_width=2),
            Line([0.3, 0.8, 0], [1.3, 1.5, 0], color=WHITE, stroke_width=2),
        )

        axon_end = soma.get_bottom() + DOWN * 2.6 + RIGHT * 0.9
        axon = Line(
            soma.get_bottom(),
            axon_end,
            path_arc=-0.5,
            color=WHITE,
            stroke_width=3,
        )
        terminal = VGroup(
            Line(axon_end, axon_end + DOWN * 0.3 + LEFT * 0.25, color=WHITE, stroke_width=2),
            Line(axon_end, axon_end + DOWN * 0.3 + RIGHT * 0.25, color=WHITE, stroke_width=2),
        )

        neuron = VGroup(soma, dendrites, axon, terminal)

        self.play(Write(neuron), run_time=max(0.05, rt(2.2)))
        self.wait(max(0.05, rt(0.24)))

        # ---------- Beat 2: neural spike badge ----------
        badge_disc = Circle(
            radius=0.78,
            color=PURPLE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        badge_text = (
            Text("neural spike", font_size=20, color=WHITE)
            .scale_to_fit_width(1.25)
            .move_to(badge_disc)
        )
        badge_group = VGroup(badge_disc, badge_text).move_to(np.array([3.4, 2.1, 0]))

        brief_label = Text(
            "brief electrical signal",
            font_size=24,
            color=GOLD,
        ).move_to(badge_group.get_bottom() + DOWN * 0.45)

        self.play(GrowFromCenter(badge_group), run_time=max(0.05, rt(0.6)))
        self.play(FadeIn(brief_label), run_time=max(0.05, rt(0.7)))
        self.play(badge_disc.animate.scale(1.12), run_time=max(0.05, rt(0.4)))
        self.play(badge_disc.animate.scale(1 / 1.12), run_time=max(0.05, rt(0.4)))
        self.wait(max(0.05, rt(2.92)))

        # ---------- Beat 3: firing flash ----------
        soma_glow = VGroup(
            Circle(radius=0.85, color=BLUE, fill_color=BLUE, fill_opacity=0.12, stroke_width=0).move_to(soma),
            Circle(radius=1.1, color=BLUE, fill_color=BLUE, fill_opacity=0.08, stroke_width=0).move_to(soma),
        )
        fire_label = Text(
            "firing of a neuron",
            font_size=24,
            color=GOLD,
        ).move_to(brief_label.get_center())

        flash = axon.copy().set_stroke(YELLOW, width=8).set_opacity(1)

        self.play(
            FadeIn(soma_glow),
            FadeOut(brief_label),
            FadeIn(fire_label),
            run_time=max(0.05, rt(0.8)),
        )
        self.play(Create(flash), run_time=max(0.05, rt(1.5)), rate_func=linear)
        self.play(FadeOut(flash), run_time=max(0.05, rt(0.3)))
        self.play(FadeOut(soma_glow), run_time=max(0.05, rt(0.5)))
        self.wait(max(0.05, rt(0.94)))

        # ---------- Beat 4: incoming excitatory input ----------
        input_group = VGroup()
        target_positions = [
            np.array([-0.9, 1.9, 0]),
            np.array([-1.3, 1.4, 0]),
            np.array([-0.4, 2.5, 0]),
            np.array([-1.7, 2.5, 0]),
        ]
        start_positions = [
            np.array([-4.0, 3.0, 0]),
            np.array([-3.4, 3.4, 0]),
            np.array([-4.2, 3.2, 0]),
            np.array([-3.2, 3.6, 0]),
        ]

        for i in range(4):
            v1 = Line(LEFT * 0.14 + UP * 0.16, ORIGIN, color=ORANGE, stroke_width=3)
            v2 = Line(RIGHT * 0.14 + UP * 0.16, ORIGIN, color=ORANGE, stroke_width=3)
            glow = Circle(radius=0.16, fill_color=ORANGE, fill_opacity=0.25, stroke_width=0)
            mark = VGroup(glow, VGroup(v1, v2)).move_to(start_positions[i]).set_opacity(0.85)
            input_group.add(mark)

        self.add(input_group)
        self.play(
            *[
                mark.animate.move_to(target_positions[i])
                for i, mark in enumerate(input_group)
            ],
            run_time=max(0.05, rt(2.5)),
        )
        self.wait(max(0.05, rt(0.4)))

        # ---------- Beat 5: threshold + membrane potential meter ----------
        threshold_y = 0.4
        threshold_line = DashedLine(
            start=np.array([soma.get_left()[0] - 0.4, threshold_y, 0]),
            end=np.array([soma.get_right()[0] + 0.4, threshold_y, 0]),
            color=GOLD,
            stroke_width=2.5,
            dash_length=0.15,
            dashed_ratio=0.6,
        )
        threshold_label = (
            Text("firing threshold", font_size=20, color=GOLD)
            .next_to(threshold_line, LEFT, buff=0.25)
        )

        meter_bar = Rectangle(
            width=0.35,
            height=3.4,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.25,
        ).move_to(np.array([3.7, 0.0, 0]))

        meter_value = ValueTracker(0)
        meter_indicator = Line(
            meter_bar.get_left() + LEFT * 0.12,
            meter_bar.get_right() + RIGHT * 0.12,
            color=YELLOW,
            stroke_width=4,
        )
        meter_indicator.move_to(np.array([meter_bar.get_center()[0], meter_bar.get_bottom()[1], 0]))
        meter_indicator.add_updater(
            lambda m: m.move_to(
                np.array([
                    meter_bar.get_center()[0],
                    meter_bar.get_bottom()[1] + meter_value.get_value() * meter_bar.height,
                    0,
                ])
            )
        )

        self.play(
            Create(threshold_line),
            FadeIn(threshold_label),
            FadeIn(meter_bar),
            input_group.animate.shift(LEFT * 0.06 + UP * 0.04),
            run_time=max(0.05, rt(0.8)),
        )
        self.add(meter_indicator)
        self.play(
            meter_value.animate.set_value(1),
            input_group.animate.shift(LEFT * 0.06 + UP * 0.04).set_opacity(0.6),
            run_time=max(0.05, rt(4.6)),
            rate_func=linear,
        )
        self.wait(max(0.05, rt(0.4)))

        # ---------- Beat 6: caption, clean transition ----------
        meter_indicator.clear_updaters()
        caption = Text(
            "measuring an action potential",
            font_size=30,
            color=WHITE,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeOut(threshold_line, threshold_label, meter_bar, meter_indicator, input_group),
            FadeIn(caption),
            run_time=max(0.05, rt(1.2)),
        )
        self.wait(max(0.05, rt(2.18)))

        # ---------- Beat 7: intracellular electrode ----------
        outer_membrane = Circle(
            radius=soma.radius + 0.08,
            stroke_color=TEAL,
            stroke_width=1.5,
            fill_opacity=0,
        ).move_to(soma.get_center())

        electrode = Polygon(
            [-0.07, 4.0, 0],
            [0.07, 4.0, 0],
            [0.02, 0.0, 0],
            [0, -0.08, 0],
            [-0.02, 0.0, 0],
        ).set_fill(GREY_B, opacity=1).set_stroke(WHITE, width=1)
        electrode.shift(UP * 4.0)

        self.play(FadeIn(outer_membrane), run_time=max(0.05, rt(0.35)))
        self.play(electrode.animate.shift(DOWN * 4.0), run_time=max(0.05, rt(1.9)), rate_func=linear)
        self.wait(max(0.05, rt(0.11)))

        # ---------- Beat 8: intracellular trace panel + AP waveform ----------
        self.play(
            FadeOut(badge_group, fire_label, caption),
            neuron.animate.shift(LEFT * 3),
            electrode.animate.shift(LEFT * 3),
            outer_membrane.animate.shift(LEFT * 3),
            run_time=max(0.05, rt(0.9)),
        )

        intra_panel_rect = Rectangle(
            width=3.0,
            height=2.2,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.10,
        ).move_to(np.array([1.4, 0.2, 0]))

        intra_label = (
            Text("intracellular recording", font_size=20, color=GOLD)
            .scale_to_fit_width(intra_panel_rect.width - 0.3)
            .next_to(intra_panel_rect, UP, buff=0.15)
        )

        scale_bar_vertical = Line(
            intra_panel_rect.get_left() + LEFT * 0.35,
            intra_panel_rect.get_left() + LEFT * 0.35 + UP * 1.2,
            color=WHITE,
            stroke_width=2,
        )
        scale_bar_label = (
            Text("100 mV", font_size=16, color=WHITE)
            .next_to(scale_bar_vertical, UP, buff=0.08)
            .scale_to_fit_width(1.0)
        )
        scale_bar_group = VGroup(scale_bar_vertical, scale_bar_label)

        panel_left = intra_panel_rect.get_left()[0] + 0.15
        panel_right = intra_panel_rect.get_right()[0] - 0.15
        panel_bottom = intra_panel_rect.get_bottom()[1] + 0.3
        panel_top = intra_panel_rect.get_top()[1] - 0.3
        usable_height = panel_top - panel_bottom
        vmin, vmax = -85.0, 40.0

        def ap_mv(t):
            if t < 0.15:
                return -70.0
            elif t < 0.25:
                return -70.0 + 100.0 * (t - 0.15) / 0.10
            elif t < 0.45:
                return 30.0 - 110.0 * (t - 0.25) / 0.20
            elif t < 0.60:
                return -80.0 + 10.0 * (t - 0.45) / 0.15
            else:
                return -70.0

        def intra_coords(t):
            x = panel_left + t * (panel_right - panel_left)
            v = ap_mv(t)
            y = panel_bottom + ((v - vmin) / (vmax - vmin)) * usable_height
            return np.array([x, y, 0])

        intra_wave = ParametricFunction(
            intra_coords,
            t_range=[0, 1, 0.005],
            color=YELLOW,
            stroke_width=4,
        )

        intra_trace_group = VGroup(
            intra_panel_rect,
            intra_label,
            scale_bar_group,
            intra_wave,
        )

        self.play(FadeIn(intra_panel_rect, intra_label), run_time=max(0.05, rt(0.7)))
        self.play(FadeIn(scale_bar_group), run_time=max(0.05, rt(0.3)))
        self.play(Create(intra_wave), run_time=max(0.05, rt(4.0)), rate_func=linear)
        self.wait(max(0.05, rt(0.46)))

        # ---------- Beat 9: retract electrode, dim/shift intracellular trace ----------
        self.play(
            electrode.animate.shift(UP * 4.0).set_opacity(0),
            intra_trace_group.animate.set_opacity(0.45).shift(RIGHT * 0.3),
            run_time=max(0.05, rt(1.4)),
        )
        self.remove(electrode)
        self.wait(max(0.05, rt(0.96)))

        # ---------- Beat 10: extracellular electrode ----------
        final_tip_x = soma.get_center()[0] + soma.radius + 1.2
        final_tip_y = soma.get_center()[1]

        extra_electrode = Polygon(
            [final_tip_x - 0.07, 4.0, 0],
            [final_tip_x + 0.07, 4.0, 0],
            [final_tip_x + 0.02, final_tip_y, 0],
            [final_tip_x, final_tip_y - 0.08, 0],
            [final_tip_x - 0.02, final_tip_y, 0],
        ).set_fill(TEAL, opacity=1).set_stroke(WHITE, width=1)
        extra_electrode.shift(UP * 4.0)

        self.play(
            outer_membrane.animate.set_stroke(TEAL, width=2.5).set_opacity(1),
            run_time=max(0.05, rt(0.5)),
        )
        self.play(extra_electrode.animate.shift(DOWN * 4.0), run_time=max(0.05, rt(2.2)), rate_func=linear)
        self.wait(max(0.05, rt(0.66)))

        # ---------- Beat 11: firing + electric field halo ----------
        flash2 = axon.copy().set_stroke(YELLOW, width=9).set_opacity(1)
        soma_center = soma.get_center()
        halo_rings = VGroup(
            Circle(radius=0.9, color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.07).move_to(soma_center),
            Circle(radius=1.4, color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.05).move_to(soma_center),
            Circle(radius=1.9, color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.03).move_to(soma_center),
        )

        self.add(halo_rings)
        self.play(
            Create(flash2),
            halo_rings.animate.scale(1.8).set_opacity(0),
            run_time=max(0.05, rt(1.8)),
            rate_func=linear,
        )
        self.play(FadeOut(flash2), run_time=max(0.05, rt(0.2)))
        self.remove(halo_rings)
        self.wait(max(0.05, rt(1.92)))

        # ---------- Beat 12: extracellular trace panel ----------
        extra_panel_rect = Rectangle(
            width=3.0,
            height=2.2,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=TEAL,
            fill_opacity=0.08,
        ).move_to(np.array([4.8, 0.2, 0]))

        extra_label = (
            Text("extracellular recording", font_size=20, color=TEAL)
            .scale_to_fit_width(extra_panel_rect.width - 0.3)
            .next_to(extra_panel_rect, UP, buff=0.15)
        )

        extra_left = extra_panel_rect.get_left()[0] + 0.15
        extra_right = extra_panel_rect.get_right()[0] - 0.15
        extra_center_y = extra_panel_rect.get_center()[1]

        def ext_mv(t):
            if t < 0.2:
                return 0
            elif t < 0.35:
                return -8 * (t - 0.2) / 0.15
            elif t < 0.5:
                return -8 + 10 * (t - 0.35) / 0.15
            elif t < 0.65:
                return 2 - 2 * (t - 0.5) / 0.15
            else:
                return 0

        def ext_coords(t):
            x = extra_left + t * (extra_right - extra_left)
            v = ext_mv(t)
            y = extra_center_y + (v / 10.0) * 0.35 * extra_panel_rect.height
            return np.array([x, y, 0])

        extra_wave = ParametricFunction(
            ext_coords,
            t_range=[0, 1, 0.005],
            color=TEAL,
            stroke_width=3,
        )
        spike_label = Text("spike", font_size=18, color=GOLD).next_to(extra_wave, RIGHT, buff=0.1)

        extra_trace_group = VGroup(extra_panel_rect, extra_label, extra_wave)

        self.play(FadeIn(extra_panel_rect, extra_label), run_time=max(0.05, rt(0.4)))
        self.play(Create(extra_wave), run_time=max(0.05, rt(1.0)), rate_func=linear)
        self.play(FadeIn(spike_label), run_time=max(0.05, rt(0.3)))
        self.wait(max(0.05, rt(0.84)))

        # ---------- Beat 13: side-by-side comparison ----------
        self.play(
            intra_trace_group.animate.set_opacity(1).shift(LEFT * 0.2),
            extra_trace_group.animate.set_opacity(1),
            run_time=max(0.05, rt(0.9)),
        )

        intra_peak_y = intra_wave.point_from_proportion(0.25)[1]
        extra_peak_y = extra_wave.point_from_proportion(0.5)[1]
        arrow_x = (intra_panel_rect.get_right()[0] + extra_panel_rect.get_left()[0]) / 2

        amplitude_arrow = Arrow(
            start=np.array([arrow_x, extra_peak_y, 0]),
            end=np.array([arrow_x, intra_peak_y, 0]),
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.25,
        )

        self.play(Create(amplitude_arrow), run_time=max(0.05, rt(0.6)))
        self.play(spike_label.animate.scale(1.3), run_time=max(0.05, rt(0.4)))
        self.play(spike_label.animate.scale(1 / 1.3), run_time=max(0.05, rt(0.4)))
        self.wait(max(0.05, rt(0.16)))

        # ---------- Beat 14: soft final spike pulse ----------
        self.play(
            spike_label.animate.scale(1.12).set_opacity(0.85),
            run_time=max(0.05, rt(0.38)),
        )
        self.play(
            spike_label.animate.scale(1 / 1.12).set_opacity(1),
            run_time=max(0.05, rt(0.38)),
        )