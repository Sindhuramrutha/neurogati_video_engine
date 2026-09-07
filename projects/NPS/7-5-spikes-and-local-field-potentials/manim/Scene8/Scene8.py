ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helper for sinusoid waves ----------
        def make_wave(y_center, amp, n_cycles, color, stroke_width=4, opacity=1.0):
            x_left, x_right = -4.3, 3.5
            graph = FunctionGraph(
                lambda x: y_center + amp * np.sin(
                    2 * np.pi * n_cycles * (x - x_left) / (x_right - x_left)
                ),
                x_range=[x_left, x_right, 0.02],
                color=color,
                stroke_width=stroke_width,
            )
            graph.set_opacity(opacity)
            return graph

        # ---------- previous-scene remnant ----------
        rem_neuron = Circle(radius=0.25, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
        rem_neuron.move_to(ORIGIN)
        rem_dendrites = VGroup(
            Line(ORIGIN, RIGHT * 0.35 + UP * 0.25, color=YELLOW, stroke_width=2),
            Line(ORIGIN, LEFT * 0.35 + UP * 0.25, color=YELLOW, stroke_width=2),
            Line(ORIGIN, RIGHT * 0.35 + DOWN * 0.15, color=YELLOW, stroke_width=2),
            Line(ORIGIN, LEFT * 0.35 + DOWN * 0.15, color=YELLOW, stroke_width=2),
        )
        rem_left = Text("firing rate coding", font_size=24, color=BLUE).move_to(LEFT * 3.1 + UP * 0.2)
        rem_right = Text("temporal coding", font_size=24, color=ORANGE).move_to(RIGHT * 3.1 + UP * 0.2)
        remnant = VGroup(rem_neuron, rem_dendrites, rem_left, rem_right)

        caption = Text(
            "LFPs provide another perspective on neural coding",
            font_size=30,
            color=GREY_B,
            t2c={"LFPs": WHITE},
            t2w={"LFPs": BOLD},
        ).to_edge(UP, buff=0.25)

        # ---------- spike train panel ----------
        raw_tick_xs = [12, 18, 25, 40, 55, 70, 82]
        tick_xs = [-4.3 + (x / 90) * 7.8 for x in raw_tick_xs]  # map to [-4.3, 3.5]
        spike_axis = Line([-4.3, 1.2, 0], [3.5, 1.2, 0], color=WHITE, stroke_width=2.5)
        spike_ticks = VGroup(*[
            Line([x, 1.2, 0], [x, 1.75, 0], color=WHITE, stroke_width=3)
            for x in tick_xs
        ])
        spike_group = VGroup(spike_axis, spike_ticks)
        label_individual = Text(
            "individual-neuron level",
            font_size=24,
            color=WHITE,
            t2c={"individual": YELLOW},
            t2w={"individual": BOLD},
        ).next_to(spike_group, UP, buff=0.25)
        upper_panel = VGroup(spike_group, label_individual)
        upper_highlight = SurroundingRectangle(upper_panel, color=WHITE, buff=0.12, stroke_width=3)

        # ---------- LFP panel ----------
        lfp_axis = Line([-4.3, -0.75, 0], [3.5, -0.75, 0], color=GREY_B, stroke_width=2)
        lfp_wave_normal = make_wave(-0.4, 0.35, 1.4, WHITE, stroke_width=4, opacity=0.3)
        lfp_wave_large = make_wave(-0.4, 0.55, 1.4, WHITE, stroke_width=4, opacity=1.0)
        lfp_wave = lfp_wave_normal.copy()  # start dimmed
        lower_panel = VGroup(lfp_axis, lfp_wave)
        label_pop = Text("population level", font_size=24, color=WHITE).move_to([-4.7, 0.05, 0])

        # ---------- decomposition components ----------
        low_comp = make_wave(-1.35, 0.17, 0.8, ORANGE, stroke_width=3.5)
        theta_comp = make_wave(-1.95, 0.16, 1.6, TEAL, stroke_width=3.5)
        gamma_comp = make_wave(-2.55, 0.13, 4.5, PURPLE, stroke_width=3.2)
        low_label = Text("slow oscillation ~4 Hz", font_size=18, color=ORANGE).next_to(low_comp, UP, buff=0.1)
        theta_label = Text("theta ~8 Hz", font_size=18, color=TEAL).next_to(theta_comp, UP, buff=0.1)
        gamma_label = Text("gamma ~30 Hz", font_size=18, color=PURPLE).next_to(gamma_comp, UP, buff=0.1)
        comp_group = VGroup(low_comp, theta_comp, gamma_comp)

        connector_lines = VGroup()
        for x, comp_y in [(2.4, -1.35), (2.8, -1.95), (3.2, -2.55)]:
            connector_lines.add(
                DashedLine(
                    [x, -0.7, 0], [x, comp_y, 0],
                    color=GREY, stroke_width=2.5, dash_length=0.08,
                )
            )

        # ---------- spectral mini-panel ----------
        spectral_axis = Line([4.6, -0.8, 0], [6.3, -0.8, 0], color=GREY_B, stroke_width=2)
        peak4 = Polygon(
            [4.67, -0.8, 0], [4.8, -0.4, 0], [4.93, -0.8, 0],
            fill_color=ORANGE, fill_opacity=0.85, stroke_width=0,
        )
        peak8 = Polygon(
            [5.12, -0.8, 0], [5.28, -0.22, 0], [5.44, -0.8, 0],
            fill_color=TEAL, fill_opacity=0.85, stroke_width=0,
        )
        peak30 = Polygon(
            [5.57, -0.8, 0], [5.7, -0.48, 0], [5.83, -0.8, 0],
            fill_color=PURPLE, fill_opacity=0.85, stroke_width=0,
        )
        val4 = Text("4", font_size=14, color=ORANGE).move_to([4.8, -1.05, 0])
        val8 = Text("8", font_size=14, color=TEAL).move_to([5.28, -1.05, 0])
        val30 = Text("30", font_size=14, color=PURPLE).move_to([5.7, -1.05, 0])
        freq_label = Text("frequency", font_size=16, color=GREY_B).move_to([5.47, -1.35, 0])
        spectral_panel = VGroup(spectral_axis, peak4, peak8, peak30, val4, val8, val30, freq_label)

        # ---------- later highlights and connectors ----------
        upper_glow = SurroundingRectangle(upper_panel, color=WHITE, buff=0.1, stroke_width=2.5)
        lower_glow = SurroundingRectangle(
            VGroup(lower_panel, label_pop), color=WHITE, buff=0.12, stroke_width=2.5
        )
        link_lines = VGroup(*[
            DashedLine(
                [x, -0.6, 0], [x, 1.15, 0],
                color=GREY, stroke_width=2, dash_length=0.08,
            )
            for x in [-2.13, 0.47, 2.81]
        ])

        unified_panel = Rectangle(
            width=9.8, height=5.2,
            stroke_color=GREY_B, stroke_width=3,
            fill_color=GREY, fill_opacity=0.06,
        ).move_to([-0.35, -0.15, 0])
        combined_caption = Text(
            "combined spike and LFP analysis",
            font_size=28, color=WHITE, weight=BOLD,
        ).next_to(unified_panel, DOWN, buff=0.3)

        # ---------- Beat 1: 0.00-2.96 ----------
        self.add(remnant)
        self.play(FadeIn(caption), run_time=max(0.05, 0.5))
        self.play(FadeOut(remnant), run_time=max(0.05, 0.8))
        self.play(
            Create(spike_group),
            FadeIn(label_individual),
            Create(lfp_axis),
            FadeIn(lfp_wave),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 2.96 - (0.5 + 0.8 + 0.7)))

        # ---------- Beat 2: 2.96-5.76 ----------
        self.play(FadeIn(upper_highlight), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 5.02 - (2.96 + 0.4)))  # 1.66
        self.play(Indicate(spike_ticks, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 5.76 - 5.47))  # 0.29

        # ---------- Beat 3: 6.64-8.50 ----------
        self.wait(max(0.05, 6.64 - 5.76))  # 0.88
        self.play(
            FadeOut(upper_highlight),
            FadeIn(label_pop),
            lfp_wave.animate.set_opacity(1),
            run_time=max(0.05, 0.4),
        )
        # amplitude swell once using Transform to the large waveform and back
        self.play(Transform(lfp_wave, lfp_wave_large), run_time=max(0.05, 0.3))
        self.play(Transform(lfp_wave, lfp_wave_normal), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 8.24 - (6.64 + 0.4 + 0.3 + 0.3)))  # 0.6
        self.play(
            lfp_wave.animate.set_stroke(width=8).set_color(YELLOW),
            run_time=max(0.05, 0.26),
        )

        # ---------- Beat 4: 8.50-12.72 ----------
        self.play(Create(low_comp), FadeIn(low_label), run_time=max(0.05, 0.7))  # 8.50->9.20
        self.wait(max(0.05, 9.52 - (8.50 + 0.7)))  # 0.32
        self.play(Create(theta_comp), FadeIn(theta_label), run_time=max(0.05, 0.5))  # 9.52->10.02
        self.wait(max(0.05, 10.08 - (9.52 + 0.5)))  # 0.06
        self.play(Create(gamma_comp), FadeIn(gamma_label), run_time=max(0.05, 0.46))  # 10.08->10.54
        # brief oscillation pulse for all components (using scale instead of scale_y)
        self.play(comp_group.animate.scale(1.12, about_point=comp_group.get_center()), run_time=max(0.05, 0.35))
        self.play(comp_group.animate.scale(1/1.12, about_point=comp_group.get_center()), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 11.70 - (10.54 + 0.35 + 0.35)))  # 0.46
        self.wait(max(0.05, 12.14 - 11.70))  # 0.44
        self.play(Create(connector_lines), FadeIn(spectral_panel), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 12.72 - (12.14 + 0.55)))  # 0.03

        # ---------- Beat 5: 13.90-16.26 ----------
        self.wait(max(0.05, 13.90 - 12.72))  # 1.18
        self.wait(max(0.05, 14.44 - 13.90))  # 0.54
        self.play(FadeIn(upper_glow), FadeIn(lower_glow), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 14.90 - (14.44 + 0.4)))  # 0.06
        self.play(Indicate(upper_panel, color=WHITE, scale_factor=1.05), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 15.30 - (14.90 + 0.25)))  # 0.15
        self.play(Indicate(lower_panel, color=WHITE, scale_factor=1.05), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 16.26 - (15.30 + 0.25)))  # 0.71
        self.play(Create(link_lines), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 16.76 - (16.26 + 0.45)))  # 0.05

        # ---------- Beat 6: 16.76-20.88 ----------
        self.play(
            FadeIn(unified_panel),
            FadeIn(combined_caption),
            FadeOut(upper_glow),
            FadeOut(lower_glow),
            FadeOut(link_lines),
            FadeOut(spectral_panel),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 17.48 - (16.76 + 0.6)))  # 0.12

        eye_icon = VGroup(
            Ellipse(width=0.8, height=0.4, color=WHITE, stroke_width=2),
            Circle(radius=0.12, fill_color=BLUE, fill_opacity=1, stroke_width=0),
            Circle(radius=0.2, color=WHITE, stroke_width=1),
        ).to_corner(UR, buff=0.45)
        self.play(FadeIn(eye_icon), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.16))
        self.play(FadeOut(eye_icon), run_time=max(0.05, 0.20))

        ripple_dot_spike = Dot(radius=0.05, color=WHITE, fill_opacity=1).move_to([-4.3, 1.45, 0])
        ripple_dot_lfp = Dot(radius=0.05, color=WHITE, fill_opacity=1).move_to([-4.3, -0.4, 0])
        self.add(ripple_dot_spike, ripple_dot_lfp)
        self.play(
            ripple_dot_spike.animate.move_to([3.5, 1.45, 0]),
            ripple_dot_lfp.animate.move_to([3.5, -0.4, 0]),
            run_time=max(0.05, 0.55),
        )
        self.remove(ripple_dot_spike, ripple_dot_lfp)
        ripple_dot_spike.move_to([-4.3, 1.45, 0])
        ripple_dot_lfp.move_to([-4.3, -0.4, 0])
        self.add(ripple_dot_spike, ripple_dot_lfp)
        self.play(
            ripple_dot_spike.animate.move_to([3.5, 1.45, 0]),
            ripple_dot_lfp.animate.move_to([3.5, -0.4, 0]),
            run_time=max(0.05, 0.55),
        )
        self.remove(ripple_dot_spike, ripple_dot_lfp)
        self.wait(max(0.05, 19.28 - (17.48 + 0.20 + 0.16 + 0.20 + 0.55 + 0.55)))  # fill to 19.28
        self.wait(max(0.05, 19.72 - 19.28))  # 0.44

        # split labels for "at both"
        split_ind = Text(
            "individual-neuron level",
            font_size=28,
            color=WHITE,
            t2c={"individual": YELLOW},
            t2w={"individual": BOLD},
        ).move_to([-2.0, 2.85, 0])
        split_pop = Text("population level", font_size=28, color=WHITE).move_to([-2.0, -2.95, 0])
        self.play(
            FadeIn(split_ind),
            FadeIn(split_pop),
            FadeOut(label_individual),
            FadeOut(label_pop),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 20.46 - (19.72 + 0.4)))  # 0.34

        # ---------- Beat 7: 20.46-23.24 ----------
        strong_upper_highlight = SurroundingRectangle(
            VGroup(spike_group, label_individual), color=WHITE, buff=0.12, stroke_width=5
        )
        self.play(
            FadeOut(split_ind),
            FadeOut(split_pop),
            FadeIn(label_individual),
            FadeIn(strong_upper_highlight),
            lfp_wave.animate.set_opacity(0.3),
            run_time=max(0.05, 0.3),
        )
        self.wait(max(0.05, 20.88 - (20.46 + 0.3)))  # 0.12

        # replay the 7 spike positions quickly
        for tick in spike_ticks:
            self.play(tick.animate.set_color(YELLOW), run_time=max(0.05, 0.06))
            self.play(tick.animate.set_color(WHITE), run_time=max(0.05, 0.04))

        lower_strong_rect = SurroundingRectangle(
            VGroup(lower_panel, label_pop), color=WHITE, buff=0.12, stroke_width=5
        )
        self.play(
            FadeOut(strong_upper_highlight),
            FadeIn(lower_strong_rect),
            FadeIn(label_pop),
            lfp_wave.animate.set_opacity(1),
            upper_panel.animate.set_opacity(0.5),
            run_time=max(0.05, 0.55),
        )
        self.wait(max(0.05, 22.22 - (20.88 + 7 * 0.10 + 0.55)))  # compute after retrace

        for comp, col in [(low_comp, ORANGE), (theta_comp, TEAL), (gamma_comp, PURPLE)]:
            self.play(Indicate(comp, color=col, scale_factor=1.2), run_time=max(0.05, 0.14))
        self.wait(max(0.05, 22.68 - (22.22 + 3 * 0.14)))  # 0.04

        # components converge back into the single LFP wave
        self.play(
            FadeOut(lower_strong_rect),
            upper_panel.animate.set_opacity(1),
            comp_group.animate.shift(UP * 0.45).set_opacity(0.45),
            lfp_wave.animate.set_opacity(1),
            run_time=max(0.05, 0.25),
        )
        self.play(
            comp_group.animate.shift(DOWN * 0.45).set_opacity(1),
            run_time=max(0.05, 0.25),
        )
        self.wait(max(0.05, 23.24 - (22.68 + 0.25 + 0.25)))  # 0.06

        # ---------- Beat 8: 23.24-23.90 ----------
        final_group = VGroup(
            caption,
            upper_panel,
            lower_panel,
            label_pop,
            low_comp,
            low_label,
            theta_comp,
            theta_label,
            gamma_comp,
            gamma_label,
            connector_lines,
            unified_panel,
            combined_caption,
        )
        self.wait(max(0.05, 0.30))
        self.play(FadeOut(final_group), run_time=max(0.05, 0.36))
        self.wait(max(0.05, 23.90 - (23.24 + 0.30 + 0.36)))  # usually 0.00, skip if <=0