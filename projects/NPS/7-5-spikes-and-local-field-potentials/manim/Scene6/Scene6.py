ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}


from manim import *
import numpy as np


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def v2(x, y):
            return np.array([x, y, 0.0])

        def x_of_t(t):
            return -6.0 + t * 12.0

        def make_neuron(center, color=BLUE, radius=0.18, fill_opacity=0.6,
                        stroke_color=GREY_B):
            soma = Circle(
                radius=radius,
                fill_color=color,
                fill_opacity=fill_opacity,
                stroke_color=stroke_color,
                stroke_width=1.5,
            ).move_to(center)

            dirs = [
                v2(1.0, 0.8),
                v2(0.2, -1.0),
                v2(-0.9, 0.4),
                v2(-0.4, -0.8),
            ]
            dendrites = VGroup()
            for d in dirs:
                d = d / np.linalg.norm(d)
                dendrites.add(
                    Line(
                        center + d * radius,
                        center + d * (radius + 0.18),
                        color=stroke_color,
                        stroke_width=2.0,
                    )
                )
            return VGroup(soma, dendrites)

        # ---------- shared waveform components ----------
        def slow_variation(t):
            return 0.35 * np.sin(2 * np.pi * 1.05 * t) + 0.10 * np.sin(
                2 * np.pi * 2.4 * t + 0.5
            )

        def fast_variation(t):
            centers_fast = [0.23, 0.40, 0.57, 0.74, 0.90]
            val = 0.0
            for c in centers_fast:
                val += 0.34 * np.exp(-((t - c) ** 2) / (2 * 0.012 ** 2))
            return val

        def raw_mixed_y(t, base=-2.0):
            return base + slow_variation(t) + fast_variation(t)

        # ---------- previous scene ghost panels ----------
        prev_left_panel = Rectangle(
            width=4.6,
            height=3.8,
            stroke_color=RED,
            stroke_width=3,
            fill_color=RED,
            fill_opacity=0.12,
        ).move_to(LEFT * 3.0)
        prev_right_panel = Rectangle(
            width=4.6,
            height=3.8,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.12,
        ).move_to(RIGHT * 3.0)
        self.add(prev_left_panel, prev_right_panel)

        # ---------- soft tissue background ----------
        tissue_glow = VGroup()
        for r, op in [(1.4, 0.07), (2.0, 0.05), (2.4, 0.03)]:
            tissue_glow.add(
                Circle(
                    radius=r,
                    fill_color=BLUE,
                    fill_opacity=op,
                    stroke_width=0,
                ).move_to(v2(0, 0.8))
            )

        # ---------- electrode tip ----------
        electrode_center = v2(0.0, 1.2)
        shaft = Line(
            electrode_center + LEFT * 0.8,
            electrode_center + LEFT * 0.25,
            color=GREY_B,
            stroke_width=5,
        )
        tip_triangle = Polygon(
            electrode_center + UP * 0.11,
            electrode_center + DOWN * 0.11,
            electrode_center + RIGHT * 0.30,
            color=GREY_B,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        )
        electrode_group = VGroup(shaft, tip_triangle)

        # ---------- surrounding neuron cluster ----------
        neuron_list = []
        angles = np.linspace(0, 2 * np.pi, 14, endpoint=False) + 0.3
        for i, a in enumerate(angles):
            radius = 1.25 + 0.40 * ((i % 4) - 1)
            pos = electrode_center + v2(radius * np.cos(a), radius * np.sin(a))
            neuron_list.append(
                make_neuron(
                    pos,
                    color=BLUE,
                    radius=0.17,
                    fill_opacity=0.45,
                    stroke_color=GREY_B,
                )
            )
        neuron_cluster = VGroup(*neuron_list)

        # ---------- raw signal at bottom ----------
        raw_wave = ParametricFunction(
            lambda t: np.array([x_of_t(t), raw_mixed_y(t, base=-2.0), 0.0]),
            t_range=[0, 1, 0.005],
            color=GREY_B,
            stroke_width=2.5,
            stroke_opacity=0.65,
        )
        raw_label = Text("raw recording", font_size=20, color=GREY_B)
        raw_label.next_to(raw_wave, DOWN, buff=0.12)

        # ---------- 1. [0.00-2.14] ----------
        self.play(
            FadeOut(prev_left_panel, prev_right_panel),
            FadeIn(electrode_group),
            run_time=max(0.05, 0.50),
        )
        self.remove(prev_left_panel, prev_right_panel)

        self.play(
            FadeIn(tissue_glow),
            LaggedStart(*[GrowFromCenter(n) for n in neuron_list], lag_ratio=0.08),
            run_time=max(0.05, 1.35),
        )
        self.play(Create(raw_wave), FadeIn(raw_label), run_time=max(0.05, 0.29))

        # ---------- 2. [2.14-4.02] ----------
        raw_slow_tint = ParametricFunction(
            lambda t: np.array([x_of_t(t), -2.0 + slow_variation(t), 0.0]),
            t_range=[0, 1, 0.005],
            color=BLUE,
            stroke_width=2.0,
            stroke_opacity=0,
        )
        raw_spike_highlights = ParametricFunction(
            lambda t: np.array([x_of_t(t), -2.0 + fast_variation(t), 0.0]),
            t_range=[0, 1, 0.005],
            color=RED,
            stroke_width=2.0,
            stroke_opacity=0,
        )
        self.add(raw_slow_tint, raw_spike_highlights)

        self.play(
            raw_spike_highlights.animate.set_stroke(opacity=0.85),
            raw_slow_tint.animate.set_stroke(opacity=0.70),
            Indicate(electrode_group, scale_factor=1.10, color=BLUE),
            run_time=max(0.05, 0.50),
        )
        self.play(
            raw_spike_highlights.animate.set_stroke(opacity=0.30),
            raw_slow_tint.animate.set_stroke(opacity=0.30),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.14))

        scale_label = Text(
            "scale of neural activity", font_size=38, color=WHITE
        ).to_edge(UP, buff=0.25)
        self.play(FadeIn(scale_label), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.24))

        # ---------- 3. [4.02-7.14] ----------
        top_spike_wave = ParametricFunction(
            lambda t: np.array(
                [
                    x_of_t(t),
                    -1.1
                    + 0.55 * np.exp(-((t - 0.15) ** 2) / (2 * 0.012 ** 2))
                    + 0.55 * np.exp(-((t - 0.35) ** 2) / (2 * 0.012 ** 2))
                    + 0.55 * np.exp(-((t - 0.55) ** 2) / (2 * 0.012 ** 2))
                    + 0.55 * np.exp(-((t - 0.75) ** 2) / (2 * 0.012 ** 2))
                    + 0.55 * np.exp(-((t - 0.92) ** 2) / (2 * 0.012 ** 2)),
                    0.0,
                ]
            ),
            t_range=[0, 1, 0.005],
            color=RED,
            stroke_width=2.5,
        )
        bottom_lfp_wave = ParametricFunction(
            lambda t: np.array(
                [
                    x_of_t(t),
                    -2.7
                    + 0.50 * np.sin(2 * np.pi * 0.9 * t)
                    + 0.15 * np.sin(2 * np.pi * 2.2 * t + 0.7),
                    0.0,
                ]
            ),
            t_range=[0, 1, 0.005],
            color=BLUE,
            stroke_width=2.5,
        )

        raw_copy_top = raw_wave.copy()

        self.play(
            Transform(raw_copy_top, top_spike_wave),
            Transform(raw_wave, bottom_lfp_wave),
            FadeOut(raw_spike_highlights),
            FadeOut(raw_slow_tint),
            FadeOut(raw_label),
            FadeOut(scale_label),
            FadeOut(neuron_cluster),
            FadeOut(tissue_glow),
            run_time=max(0.05, 1.16),
        )

        branch_top = raw_copy_top
        branch_bottom = raw_wave

        divider = Line(v2(-6.0, -1.8), v2(6.0, -1.8), color=GREY_B, stroke_width=2)
        self.play(Create(divider), run_time=max(0.05, 0.30))

        measured_caption = Text(
            "measured at different scales", font_size=32, color=YELLOW
        ).next_to(electrode_group, DOWN, buff=0.55)
        self.play(FadeIn(measured_caption), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.40))
        self.play(FadeOut(measured_caption), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.36))

        # ---------- 4. [8.10-9.96] ----------
        self.wait(max(0.05, 0.96))

        not_competing_caption = Text(
            "NOT competing measurements", font_size=34, color=WHITE
        ).to_edge(UP, buff=0.30)
        self.play(FadeIn(not_competing_caption), run_time=max(0.05, 0.50))
        self.play(
            branch_top.animate.set_stroke(opacity=0.65),
            branch_bottom.animate.set_stroke(opacity=0.65),
            run_time=max(0.05, 0.45),
        )
        self.play(
            branch_top.animate.set_stroke(opacity=0.95),
            branch_bottom.animate.set_stroke(opacity=0.95),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 0.46))

        # ---------- 5. [10.90-13.78] ----------
        self.wait(max(0.05, 0.94))

        raw_recombined = ParametricFunction(
            lambda t: np.array([x_of_t(t), raw_mixed_y(t, base=-0.4), 0.0]),
            t_range=[0, 1, 0.005],
            color=GREY_B,
            stroke_width=2.5,
            stroke_opacity=0.85,
        )
        top_copy = branch_top.copy()
        bottom_copy = branch_bottom.copy()

        self.play(
            FadeIn(raw_recombined),
            top_copy.animate.move_to(v2(0, -0.4)),
            bottom_copy.animate.move_to(v2(0, -0.4)),
            branch_top.animate.set_opacity(0),
            branch_bottom.animate.set_opacity(0),
            FadeOut(divider),
            FadeOut(not_competing_caption),
            run_time=max(0.05, 1.16),
        )
        self.play(FadeOut(top_copy), FadeOut(bottom_copy), run_time=max(0.05, 0.24))
        self.wait(max(0.05, 0.10))

        same_caption = Text(
            "different views of the same underlying neural system",
            font_size=32,
            color=YELLOW,
        ).to_edge(UP, buff=0.30)
        self.play(FadeIn(same_caption), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.88))

        # ---------- 6. [14.98-17.42] ----------
        self.wait(max(0.05, 1.20))

        fast_label = Text(
            "spikes — individual neuron level",
            font_size=22,
            color=RED,
        ).scale_to_fit_width(4.2).move_to(v2(4.0, -0.1))
        slow_label = Text(
            "LFP — population level",
            font_size=24,
            color=BLUE,
        ).scale_to_fit_width(4.2).move_to(v2(4.0, -0.9))

        self.play(FadeIn(fast_label), FadeIn(slow_label), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.76))

        both_labels = VGroup(fast_label, slow_label)
        self.play(both_labels.animate.scale(1.08), run_time=max(0.05, 0.50))
        self.play(both_labels.animate.scale(1 / 1.08), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.08))

        # ---------- 7. [17.42-19.58] ----------
        old_group = VGroup(
            raw_recombined,
            fast_label,
            slow_label,
            same_caption,
            electrode_group,
        )
        self.play(FadeOut(old_group), run_time=max(0.05, 0.40))

        common_display = Rectangle(
            width=11.4,
            height=0.8,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color=GREY,
            fill_opacity=0.2,
        ).move_to(v2(0, 2.75))
        left_panel = Rectangle(
            width=5.2,
            height=3.6,
            stroke_color=RED,
            stroke_width=3,
            fill_color=GREY,
            fill_opacity=0.12,
        ).move_to(v2(-3.1, 0.15))
        right_panel = Rectangle(
            width=5.2,
            height=3.6,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=GREY,
            fill_opacity=0.12,
        ).move_to(v2(3.1, 0.15))

        raw_display_wave = ParametricFunction(
            lambda t: np.array(
                [
                    -4.8 + t * 9.6,
                    2.75
                    + 0.14 * np.sin(2 * np.pi * 2.2 * t)
                    + 0.10 * np.sin(2 * np.pi * 5.0 * t),
                    0.0,
                ]
            ),
            t_range=[0, 1, 0.005],
            color=GREY_B,
            stroke_width=1.6,
            stroke_opacity=0.70,
        )

        split_arrow_left = Arrow(
            v2(-3.1, 2.35),
            v2(-3.1, 1.95),
            color=GREY_B,
            stroke_width=2,
            buff=0.0,
            max_tip_length_to_length_ratio=0.25,
        )
        split_arrow_right = Arrow(
            v2(3.1, 2.35),
            v2(3.1, 1.95),
            color=GREY_B,
            stroke_width=2,
            buff=0.0,
            max_tip_length_to_length_ratio=0.25,
        )

        self.play(
            FadeIn(common_display),
            FadeIn(left_panel),
            FadeIn(right_panel),
            FadeIn(raw_display_wave),
            FadeIn(split_arrow_left),
            FadeIn(split_arrow_right),
            run_time=max(0.05, 0.55),
        )

        left_neuron_center = left_panel.get_center() + UP * 0.80
        left_neuron = make_neuron(
            left_neuron_center,
            color=RED,
            radius=0.28,
            fill_opacity=1.0,
            stroke_color=WHITE,
        )

        mini_offsets = [
            (-1.6, 0.7), (0.0, 1.0), (1.6, 0.7),
            (-1.8, 0.05), (0.0, 0.2), (1.8, 0.05),
            (-1.1, -0.6), (1.1, -0.6),
        ]
        right_cluster = VGroup()
        for dx, dy in mini_offsets:
            pos = right_panel.get_center() + v2(dx, dy)
            right_cluster.add(
                make_neuron(
                    pos,
                    color=BLUE,
                    radius=0.14,
                    fill_opacity=0.80,
                    stroke_color=GREY_B,
                )
            )

        left_wave_x_left = left_panel.get_left()[0] + 0.55
        left_wave_x_right = left_panel.get_right()[0] - 0.55
        left_base_y = left_panel.get_bottom()[1] + 0.90

        right_wave_x_left = right_panel.get_left()[0] + 0.55
        right_wave_x_right = right_panel.get_right()[0] - 0.55
        right_base_y = right_panel.get_bottom()[1] + 0.90

        spike_centers = [0.14, 0.32, 0.50, 0.68, 0.86]

        def new_spike_component(t, centers, amp=0.70, sigma=0.012):
            val = 0.0
            for c in centers:
                val += amp * np.exp(-((t - c) ** 2) / (2 * sigma ** 2))
            return val

        def new_lfp_component(t, centers, amp=0.55, sigma=0.065):
            val = 0.0
            for c in centers:
                val += amp * np.exp(-((t - c) ** 2) / (2 * sigma ** 2))
            val += 0.22 * np.sin(2 * np.pi * 1.4 * t)
            return val

        left_spike_wave = ParametricFunction(
            lambda t: np.array(
                [
                    left_wave_x_left + t * (left_wave_x_right - left_wave_x_left),
                    left_base_y + new_spike_component(t, spike_centers),
                    0.0,
                ]
            ),
            t_range=[0, 1, 0.005],
            color=RED,
            stroke_width=3,
        )
        right_lfp_wave = ParametricFunction(
            lambda t: np.array(
                [
                    right_wave_x_left + t * (right_wave_x_right - right_wave_x_left),
                    right_base_y + new_lfp_component(t, spike_centers),
                    0.0,
                ]
            ),
            t_range=[0, 1, 0.005],
            color=BLUE,
            stroke_width=3,
        )

        left_col_label = Text(
            "individual neuronal firing", font_size=22, color=RED
        ).scale_to_fit_width(5.0).next_to(left_panel, DOWN, buff=0.15)
        right_col_label = Text(
            "population activity", font_size=24, color=BLUE
        ).scale_to_fit_width(5.0).next_to(right_panel, DOWN, buff=0.15)

        self.play(
            FadeIn(left_neuron),
            FadeIn(left_spike_wave),
            FadeIn(right_cluster),
            FadeIn(right_lfp_wave),
            FadeIn(left_col_label),
            FadeIn(right_col_label),
            run_time=max(0.05, 0.65),
        )
        self.wait(max(0.05, 0.56))

        # ---------- 8. [19.58-22.12] ----------
        sync_lines = VGroup()
        sync_endpoints = VGroup()
        for c in spike_centers:
            lx = left_wave_x_left + c * (left_wave_x_right - left_wave_x_left)
            ly = left_base_y + new_spike_component(c, spike_centers)
            rx = right_wave_x_left + c * (right_wave_x_right - right_wave_x_left)
            ry = right_base_y + new_lfp_component(c, spike_centers)

            line = DashedLine(
                v2(lx, ly),
                v2(rx, ry),
                color=YELLOW,
                stroke_width=1.5,
                dash_length=0.10,
                stroke_opacity=0.65,
            )
            dot_l = Dot(v2(lx, ly), radius=0.05, color=YELLOW)
            dot_r = Dot(v2(rx, ry), radius=0.05, color=YELLOW)
            sync_lines.add(line)
            sync_endpoints.add(VGroup(dot_l, dot_r))

        per_item = 2.54 / len(spike_centers)
        for i in range(len(spike_centers)):
            self.play(
                FadeIn(sync_lines[i]),
                GrowFromCenter(sync_endpoints[i][0]),
                GrowFromCenter(sync_endpoints[i][1]),
                run_time=max(0.05, per_item * 0.55),
            )
            self.wait(max(0.05, per_item * 0.45))

        # ---------- 9. [22.12-23.85] ----------
        interdependent_label = Text(
            "interdependent", font_size=22, color=YELLOW
        ).scale_to_fit_width(2.6).move_to(v2(0, 0.05))
        complementary_views_label = Text(
            "complementary views", font_size=22, color=TEAL
        ).scale_to_fit_width(2.6).move_to(v2(0, -0.90))

        self.play(
            FadeIn(interdependent_label),
            FadeIn(complementary_views_label),
            run_time=max(0.05, 0.44),
        )

        final_caption = Text(
            "individual firing ↔ population activity",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(final_caption), run_time=max(0.05, 0.50))

        cycle_left_dot = Dot(
            v2(left_wave_x_left, left_base_y + new_spike_component(0, spike_centers)),
            radius=0.06,
            color=YELLOW,
        )
        cycle_right_dot = Dot(
            v2(right_wave_x_left, right_base_y + new_lfp_component(0, spike_centers)),
            radius=0.06,
            color=YELLOW,
        )
        self.add(cycle_left_dot, cycle_right_dot)
        self.play(
            MoveAlongPath(cycle_left_dot, left_spike_wave),
            MoveAlongPath(cycle_right_dot, right_lfp_wave),
            run_time=max(0.05, 0.44),
        )

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=max(0.05, 0.35))