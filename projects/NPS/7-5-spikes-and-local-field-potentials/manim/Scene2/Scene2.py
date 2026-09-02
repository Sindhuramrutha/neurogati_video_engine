ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        rt = lambda t: max(0.05, t)

        # ---------- Beat 1: neuron appears ----------
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
        axon = Line(soma.get_bottom(), axon_end, path_arc=-0.5, color=WHITE, stroke_width=3)
        terminal = VGroup(
            Line(axon_end, axon_end + DOWN * 0.3 + LEFT * 0.25, color=WHITE, stroke_width=2),
            Line(axon_end, axon_end + DOWN * 0.3 + RIGHT * 0.25, color=WHITE, stroke_width=2),
        )

        neuron = VGroup(soma, dendrites, axon, terminal)
        self.play(Write(neuron), run_time=max(0.05, rt(2.6)))
        self.wait(max(0.05, rt(0.64)))

        # ---------- Beat 2: factor list ----------
        factors = [
            "type of neuron",
            "location of recording electrode",
            "distance between neuron and electrode",
            "geometry of the neuron",
            "properties of the electrode",
        ]
        factor_rows = VGroup()
        for i, item in enumerate(factors):
            dot = Dot(radius=0.06, color=GOLD if i == 0 else GREY_B)
            label = Text(item, font_size=22, color=GOLD if i == 0 else WHITE)
            row = VGroup(dot, label).arrange(RIGHT, buff=0.18)
            factor_rows.add(row)
        factor_rows.arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        factor_rows.move_to(np.array([3.2, 0.1, 0]))

        self.play(FadeIn(factor_rows), run_time=max(0.05, rt(1.42)))

        # ---------- Beat 3: sequential highlighting ----------
        rows = list(factor_rows)
        self.play(
            rows[0].animate.set_color(WHITE),
            rows[1].animate.set_color(GOLD),
            run_time=max(0.05, rt(0.52)),
        )
        self.wait(max(0.05, rt(2.14)))
        self.play(
            rows[1].animate.set_color(WHITE),
            rows[2].animate.set_color(GOLD),
            run_time=max(0.05, rt(0.5)),
        )
        self.wait(max(0.05, rt(1.96)))
        self.play(
            rows[2].animate.set_color(WHITE),
            rows[3].animate.set_color(GOLD),
            run_time=max(0.05, rt(0.5)),
        )
        self.wait(max(0.05, rt(1.18)))
        self.play(
            rows[3].animate.set_color(WHITE),
            rows[4].animate.set_color(GOLD),
            run_time=max(0.05, rt(0.5)),
        )
        self.wait(max(0.05, rt(0.56)))

        # ---------- Beat 4: electrode descends, soma trace ----------
        self.wait(max(0.05, rt(0.86)))

        final_soma_tip_x = -1.8 + 0.6 + 0.6  # left-shifted soma + soma radius + one width
        final_soma_tip_y = 0.0
        electrode = Polygon(
            [final_soma_tip_x - 0.08, final_soma_tip_y + 4.0, 0],
            [final_soma_tip_x + 0.08, final_soma_tip_y + 4.0, 0],
            [final_soma_tip_x + 0.025, final_soma_tip_y, 0],
            [final_soma_tip_x, final_soma_tip_y - 0.09, 0],
            [final_soma_tip_x - 0.025, final_soma_tip_y, 0],
        ).set_fill(GREY_B, opacity=1).set_stroke(WHITE, width=1)
        electrode.shift(UP * 4.0)
        self.add(electrode)

        soma_panel = Rectangle(
            width=2.8,
            height=1.8,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.10,
        ).move_to(np.array([2.8, -0.2, 0]))

        soma_label = Text("soma recording", font_size=20, color=GOLD).next_to(soma_panel, UP, buff=0.15)

        panel_left = soma_panel.get_left()[0] + 0.15
        panel_right = soma_panel.get_right()[0] - 0.15
        panel_center_y = soma_panel.get_center()[1]

        def soma_v(t):
            v = 0.0
            if 0.12 < t < 0.32:
                v += 0.18 * np.sin(np.pi * (t - 0.12) / 0.20)
            v += -0.85 * np.exp(-((t - 0.5) ** 2) / (2 * 0.055 ** 2))
            if 0.68 < t < 0.88:
                v += 0.18 * np.sin(np.pi * (t - 0.68) / 0.20)
            return v

        def soma_coords(t):
            x = panel_left + t * (panel_right - panel_left)
            y = panel_center_y + soma_v(t) * 0.38 * soma_panel.height
            return np.array([x, y, 0])

        soma_wave = ParametricFunction(
            soma_coords,
            t_range=[0, 1, 0.005],
            color=YELLOW,
            stroke_width=4,
        )

        self.play(
            FadeOut(factor_rows),
            neuron.animate.shift(LEFT * 1.8),
            run_time=max(0.05, rt(0.8)),
        )
        self.play(electrode.animate.shift(DOWN * 4.0), run_time=max(0.05, rt(1.2)))
        self.play(FadeIn(soma_panel, soma_label), run_time=max(0.05, rt(0.7)))
        self.play(Create(soma_wave), run_time=max(0.05, rt(1.48)))

        # ---------- Beat 5: move electrode to dendrite, dendrite trace ----------
        self.wait(max(0.05, rt(0.52)))

        dendrite_tip = np.array([-0.4, 2.6, 0])  # upper-right branch after neuron shift
        initial_dendrite_tip = dendrite_tip + RIGHT * 0.5
        self.play(
            electrode.animate.shift(np.array([0.7, 2.6, 0])),
            run_time=max(0.05, rt(1.0)),
        )

        dendrite_label = Text("dendrite recording", font_size=20, color=TEAL).move_to(soma_label)

        def dend_v(t):
            v = 0.0
            if 0.15 < t < 0.35:
                v += 0.30 * np.sin(np.pi * (t - 0.15) / 0.20)
            v += -0.40 * np.exp(-((t - 0.5) ** 2) / (2 * 0.06 ** 2))
            if 0.65 < t < 0.85:
                v += 0.35 * np.sin(np.pi * (t - 0.65) / 0.20)
            return v

        def dend_coords(t):
            x = panel_left + t * (panel_right - panel_left)
            y = panel_center_y + dend_v(t) * 0.38 * soma_panel.height
            return np.array([x, y, 0])

        dend_wave = ParametricFunction(
            dend_coords,
            t_range=[0, 1, 0.005],
            color=TEAL,
            stroke_width=4,
        )

        self.play(
            FadeOut(soma_label),
            FadeIn(dendrite_label),
            FadeOut(soma_wave),
            run_time=max(0.05, rt(0.4)),
        )
        self.play(Create(dend_wave), run_time=max(0.05, rt(2.2)))

        # ---------- Beat 6: side-by-side waveform comparison ----------
        comp_soma_panel = Rectangle(
            width=2.6,
            height=1.8,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.10,
        ).move_to(np.array([-1.8, 0.1, 0]))

        comp_dend_panel = Rectangle(
            width=2.6,
            height=1.8,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=TEAL,
            fill_opacity=0.08,
        ).move_to(np.array([1.8, 0.1, 0]))

        def make_wave_in_panel(panel, value_func, color):
            left = panel.get_left()[0] + 0.15
            right = panel.get_right()[0] - 0.15
            center_y = panel.get_center()[1]
            h = panel.height

            def coords(t):
                x = left + t * (right - left)
                y = center_y + value_func(t) * 0.38 * h
                return np.array([x, y, 0])

            return ParametricFunction(coords, t_range=[0, 1, 0.005], color=color, stroke_width=4)

        comp_soma_wave = make_wave_in_panel(comp_soma_panel, soma_v, YELLOW)
        comp_dend_wave = make_wave_in_panel(comp_dend_panel, dend_v, TEAL)

        self.play(
            FadeOut(soma_panel, dendrite_label, dend_wave, electrode),
            neuron.animate.shift(LEFT * 2.2).set_opacity(0.35),
            run_time=max(0.05, rt(0.8)),
        )
        self.play(FadeIn(comp_soma_panel, comp_dend_panel), run_time=max(0.05, rt(0.7)))
        self.play(Create(comp_soma_wave), Create(comp_dend_wave), run_time=max(0.05, rt(1.4)))
        self.play(Indicate(comp_soma_wave, color=GOLD, scale_factor=1.08), run_time=max(0.05, rt(1.2)))
        self.wait(max(0.05, rt(0.2)))
        self.play(Indicate(comp_dend_wave, color=TEAL, scale_factor=1.08), run_time=max(0.05, rt(1.2)))
        self.wait(max(0.05, rt(0.72)))

        # ---------- Beat 7: shrink to small extracellular trace ----------
        self.wait(max(0.05, rt(1.10)))

        extra_panel = Rectangle(
            width=4.2,
            height=1.5,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=TEAL,
            fill_opacity=0.08,
        ).move_to(np.array([2.5, -2.2, 0]))

        extra_left = extra_panel.get_left()[0] + 0.20
        extra_right = extra_panel.get_right()[0] - 0.20
        extra_center_y = extra_panel.get_center()[1]

        def extra_v(t):
            v = 0.0
            if 0.15 < t < 0.35:
                v += 0.15 * np.sin(np.pi * (t - 0.15) / 0.20)
            v += -0.80 * np.exp(-((t - 0.5) ** 2) / (2 * 0.06 ** 2))
            if 0.65 < t < 0.85:
                v += 0.15 * np.sin(np.pi * (t - 0.65) / 0.20)
            return v

        def extra_coords(t):
            x = extra_left + t * (extra_right - extra_left)
            y = extra_center_y + extra_v(t) * 0.45 * extra_panel.height
            return np.array([x, y, 0])

        extra_wave = ParametricFunction(
            extra_coords,
            t_range=[0, 1, 0.005],
            color=TEAL,
            stroke_width=3,
        )

        extra_scale_label_small = Text("100 µV", font_size=15, color=YELLOW).next_to(
            extra_panel, LEFT, buff=0.35
        )

        self.play(
            FadeOut(comp_soma_panel, comp_dend_panel, comp_soma_wave, comp_dend_wave),
            neuron.animate.move_to(np.array([-1.8, 0, 0])).set_opacity(1),
            FadeIn(electrode),
            run_time=max(0.05, rt(0.9)),
        )
        self.play(FadeIn(extra_panel, extra_wave), run_time=max(0.05, rt(0.5)))
        self.play(
            extra_wave.animate.scale(0.3),
            FadeIn(extra_scale_label_small),
            run_time=max(0.05, rt(0.9)),
        )

        # ---------- Beat 8: intracellular AP trace ----------
        self.wait(max(0.05, rt(0.70)))

        intra_panel = Rectangle(
            width=3.0,
            height=2.2,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.10,
        ).move_to(np.array([2.5, -0.2, 0]))

        intra_label = Text("intracellular recording", font_size=18, color=GOLD).scale_to_fit_width(
            intra_panel.width - 0.3
        ).next_to(intra_panel, UP, buff=0.12)

        intra_scale_line = Line(
            intra_panel.get_left() + LEFT * 0.45,
            intra_panel.get_left() + LEFT * 0.45 + UP * 1.7,
            color=WHITE,
            stroke_width=2,
        )
        intra_scale_label = Text("100 mV", font_size=14, color=WHITE).next_to(
            intra_scale_line, UP, buff=0.08
        )
        intra_scale_bar_group = VGroup(intra_scale_line, intra_scale_label)

        int_left = intra_panel.get_left()[0] + 0.18
        int_right = intra_panel.get_right()[0] - 0.18
        int_bottom = intra_panel.get_bottom()[1] + 0.25
        int_top = intra_panel.get_top()[1] - 0.25
        usable_h = int_top - int_bottom
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
            x = int_left + t * (int_right - int_left)
            v = ap_mv(t)
            y = int_bottom + ((v - vmin) / (vmax - vmin)) * usable_h
            return np.array([x, y, 0])

        intra_wave = ParametricFunction(
            intra_coords,
            t_range=[0, 1, 0.005],
            color=YELLOW,
            stroke_width=4,
        )

        self.play(FadeIn(intra_panel, intra_label), run_time=max(0.05, rt(0.6)))
        self.play(FadeIn(intra_scale_bar_group), run_time=max(0.05, rt(0.4)))
        self.play(Create(intra_wave), run_time=max(0.05, rt(2.74)), rate_func=linear)

        # ---------- Beat 9: scales, bracket, units ----------
        self.wait(max(0.05, rt(0.42)))

        extra_scale_line = Line(
            extra_panel.get_left() + LEFT * 0.4,
            extra_panel.get_left() + LEFT * 0.4 + UP * 0.35,
            color=YELLOW,
            stroke_width=2,
        )

        intra_unit_label = Text("millivolts", font_size=18, color=GOLD).next_to(
            intra_panel, DOWN, buff=0.15
        )
        extra_unit_label = Text("microvolts", font_size=18, color=TEAL).next_to(
            extra_panel, DOWN, buff=0.15
        )

        bracket_x = extra_panel.get_right()[0] + 0.35
        amplitude_bracket = DoubleArrow(
            start=np.array([bracket_x, extra_wave.get_bottom()[1], 0]),
            end=np.array([bracket_x, intra_wave.get_top()[1], 0]),
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(FadeIn(extra_scale_line), run_time=max(0.05, rt(0.8)))
        self.play(FadeIn(intra_unit_label, extra_unit_label), run_time=max(0.05, rt(0.5)))
        self.play(Create(amplitude_bracket), run_time=max(0.05, rt(1.0)))
        self.wait(max(0.05, rt(2.6)))

        # ---------- Beat 10: electrode moves away, waveform shrinks ----------
        self.wait(max(0.05, rt(0.88)))

        distance_line = Line(
            dendrite_tip,
            electrode.get_bottom(),
            color=YELLOW,
            stroke_width=2,
        )
        distance_line.add_updater(
            lambda m: m.put_start_and_end_on(dendrite_tip, electrode.get_bottom())
        )

        final_dendrite_tip = dendrite_tip + RIGHT * 1.0

        self.play(
            FadeOut(
                intra_panel,
                intra_label,
                intra_scale_bar_group,
                intra_wave,
                intra_unit_label,
                amplitude_bracket,
            ),
            run_time=max(0.05, rt(0.8)),
        )
        self.play(FadeIn(distance_line), run_time=max(0.05, rt(0.3)))
        self.play(
            electrode.animate.shift(np.array([0.5, 0, 0])),
            extra_wave.animate.scale(0.35),
            run_time=max(0.05, rt(3.0)),
        )
        self.wait(max(0.05, rt(0.74)))

        # ---------- Beat 11: zoom into extracellular panel ----------
        self.wait(max(0.05, rt(0.98)))
        distance_line.clear_updaters()

        axis_y = extra_panel.get_center()[1]
        time_axis = Line(
            extra_panel.get_left() + RIGHT * 0.15,
            extra_panel.get_right() + LEFT * 0.15,
            color=GREY_B,
            stroke_width=3,
        ).shift(UP * 0.0)

        def soma_zoom_v(t):
            v = 0.0
            if 0.15 < t < 0.35:
                v += 0.15 * np.sin(np.pi * (t - 0.15) / 0.20)
            v += -0.85 * np.exp(-((t - 0.625) ** 2) / (2 * 0.055 ** 2))
            if 0.65 < t < 0.85:
                v += 0.15 * np.sin(np.pi * (t - 0.65) / 0.20)
            return v

        def zoom_soma_coords(t):
            x = extra_left + t * (extra_right - extra_left)
            y = extra_center_y + soma_zoom_v(t) * 0.55 * extra_panel.height
            return np.array([x, y, 0])

        zoomed_soma_wave = ParametricFunction(
            zoom_soma_coords,
            t_range=[0, 1, 0.005],
            color=YELLOW,
            stroke_width=5,
        )

        self.play(
            FadeOut(neuron, electrode, distance_line),
            run_time=max(0.05, rt(0.5)),
        )
        self.play(
            self.camera.frame.animate.scale(0.3),
            self.camera.frame.animate.move_to(extra_panel.get_center()),
            run_time=max(0.05, rt(0.5)),
        )
        self.play(
            FadeOut(extra_wave, extra_scale_label_small),
            FadeIn(time_axis),
            Create(zoomed_soma_wave),
            run_time=max(0.05, rt(0.38)),
        )

        # ---------- Beat 12: time axis, ticks, 2-3 ms region ----------
        self.wait(max(0.05, rt(0.76)))

        axis_left_x = time_axis.get_start()[0]
        axis_right_x = time_axis.get_end()[0]
        axis_y = time_axis.get_start()[1]

        tick_group = VGroup()
        for frac, tick_label_text in [(0, "0 ms"), (0.25, "1 ms"), (0.5, "2 ms"), (0.75, "3 ms")]:
            x = axis_left_x + frac * (axis_right_x - axis_left_x)
            tick = Line(
                np.array([x, axis_y - 0.06, 0]),
                np.array([x, axis_y + 0.06, 0]),
                color=WHITE,
                stroke_width=2,
            )
            tick_label = Text(tick_label_text, font_size=12, color=WHITE).next_to(
                tick, DOWN, buff=0.05
            )
            tick_group.add(VGroup(tick, tick_label))

        dur_left = axis_left_x + 0.5 * (axis_right_x - axis_left_x)
        dur_right = axis_left_x + 0.75 * (axis_right_x - axis_left_x)
        duration_region = Rectangle(
            width=dur_right - dur_left,
            height=0.35,
            stroke_color=GOLD,
            stroke_width=2,
            fill_color=GOLD,
            fill_opacity=0.30,
        ).move_to(np.array([(dur_left + dur_right) / 2, axis_y - 0.35, 0]))
        duration_label = Text("2–3 ms", font_size=14, color=GOLD).move_to(
            duration_region.get_bottom() + DOWN * 0.18
        )

        self.play(
            time_axis.animate.set_stroke(YELLOW, width=4),
            FadeIn(tick_group),
            FadeIn(duration_region, duration_label),
            run_time=max(0.05, rt(1.2)),
        )
        self.play(self.camera.frame.animate.scale(0.55), run_time=max(0.05, rt(1.76)))
        self.wait(max(0.05, rt(1.0)))

        # ---------- Beat 13: frequency content panel ----------
        freq_panel = Rectangle(
            width=extra_panel.width,
            height=0.9,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=PURPLE,
            fill_opacity=0.08,
        ).next_to(extra_panel, DOWN, buff=0.3)

        freq_label = Text("frequency content", font_size=16, color=GOLD).scale_to_fit_width(
            freq_panel.width - 0.3
        ).next_to(freq_panel, UP, buff=0.12)

        freq_left = freq_panel.get_left()[0] + 0.15
        freq_right = freq_panel.get_right()[0] - 0.15
        freq_bottom = freq_panel.get_bottom()[1] + 0.10
        freq_top = freq_panel.get_top()[1] - 0.10

        def spectrum_val(u):
            if u < 0.05:
                return 0.10
            elif u < 0.25:
                return 0.10 + 0.90 * (u - 0.05) / 0.20
            elif u < 0.80:
                return 1.0
            else:
                return max(0.0, 1.0 - (u - 0.80) / 0.20)

        n_pts = 80
        spec_points = []
        for i in range(n_pts + 1):
            u = i / n_pts
            x = freq_left + u * (freq_right - freq_left)
            y = freq_bottom + spectrum_val(u) * (freq_top - freq_bottom)
            spec_points.append(np.array([x, y, 0]))
        for i in range(n_pts, -1, -1):
            u = i / n_pts
            x = freq_left + u * (freq_right - freq_left)
            spec_points.append(np.array([x, freq_bottom, 0]))

        spectrum_area = Polygon(
            *spec_points,
            color=PURPLE,
            fill_opacity=0.30,
            stroke_color=PURPLE,
            stroke_width=2,
        )

        self.play(
            self.camera.frame.animate.scale(2.2),
            self.camera.frame.animate.move_to(np.array([extra_panel.get_center()[0], -2.9, 0])),
            run_time=max(0.05, rt(1.0)),
        )
        self.play(FadeIn(freq_panel, freq_label), run_time=max(0.05, rt(0.5)))
        self.play(Create(spectrum_area), run_time=max(0.05, rt(1.72)))

        # ---------- Beat 14: frequency band 300 Hz - several kHz ----------
        self.wait(max(0.05, rt(0.88)))

        freq_axis_line = Line(
            np.array([freq_left, freq_bottom, 0]),
            np.array([freq_right, freq_bottom, 0]),
            color=GREY_B,
            stroke_width=2,
        )

        freq_tick_group = VGroup()
        for freq_hz, label in [(300, "300"), (1000, "1k"), (3000, "3k"), (5000, "5k")]:
            frac = freq_hz / 6000.0
            x = freq_left + frac * (freq_right - freq_left)
            tick = Line(
                np.array([x, freq_bottom - 0.05, 0]),
                np.array([x, freq_bottom + 0.05, 0]),
                color=WHITE,
                stroke_width=2,
            )
            tick_label = Text(label, font_size=12, color=WHITE).next_to(tick, DOWN, buff=0.04)
            freq_tick_group.add(VGroup(tick, tick_label))

        band_left_x = freq_left + (300 / 6000) * (freq_right - freq_left)
        band_right_x = freq_left + (5000 / 6000) * (freq_right - freq_left)
        freq_band = Rectangle(
            width=band_right_x - band_left_x,
            height=freq_panel.height * 0.92,
            stroke_color=ORANGE,
            stroke_width=2,
            fill_color=ORANGE,
            fill_opacity=0.22,
        ).move_to(np.array([(band_left_x + band_right_x) / 2, freq_panel.get_center()[1], 0]))
        band_label = Text("300 Hz – several kHz", font_size=13, color=WHITE).move_to(
            freq_band.get_center()
        )

        self.play(
            FadeIn(freq_band, band_label),
            FadeIn(freq_axis_line),
            FadeIn(freq_tick_group),
            run_time=max(0.05, rt(1.0)),
        )
        self.play(freq_band.animate.set_fill(opacity=0.45), run_time=max(0.05, rt(1.0)))
        self.play(freq_band.animate.set_fill(opacity=0.20), run_time=max(0.05, rt(1.0)))
        self.play(freq_band.animate.set_fill(opacity=0.45), run_time=max(0.05, rt(1.0)))
        self.play(freq_band.animate.set_fill(opacity=0.20), run_time=max(0.05, rt(1.0)))
        self.wait(max(0.05, rt(0.74)))

        # ---------- Beat 15: hold with subtle framing pulse ----------
        self.wait(max(0.05, rt(0.90)))
        self.play(self.camera.frame.animate.scale(1.03), run_time=max(0.05, rt(1.0)))
        self.play(self.camera.frame.animate.scale(1 / 1.03), run_time=max(0.05, rt(1.0)))
        self.wait(max(0.05, rt(3.12)))