ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- Beat 1: head + EEG electrode ----------
        head_outline = Ellipse(
            width=3.0, height=4.0,
            stroke_color=WHITE, stroke_width=4,
            fill_opacity=0
        ).move_to(ORIGIN)

        electrode_eeg = Dot(
            point=head_outline.get_top(),
            radius=0.1,
            color=GREY_B,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1
        )

        self.play(FadeIn(head_outline), run_time=max(0.05, 1.5))
        self.play(GrowFromCenter(electrode_eeg), run_time=max(0.05, 0.5))

        # ---------- Beat 2: EEG wave + label ----------
        label_eeg = Text(
            "EEG: large-scale activity",
            font_size=28,
            color=GOLD
        ).next_to(electrode_eeg, RIGHT, buff=0.5)

        eeg_phase = ValueTracker(0)

        def make_eeg_waves(phase):
            waves = VGroup()
            for y_off in [-1.2, -0.75, -0.3, 0.15, 0.6, 1.05, 1.35]:
                wave = ParametricFunction(
                    lambda t, off=y_off: np.array([
                        -1.4 + 2.8 * t,
                        off + 0.25 * np.sin(2 * PI * 2 * t + phase),
                        0
                    ]),
                    t_range=[0, 1, 0.01],
                    stroke_color=TEAL,
                    stroke_width=2.5
                )
                waves.add(wave)
            return waves

        eeg_wave = always_redraw(lambda: make_eeg_waves(eeg_phase.get_value()))
        self.add(eeg_wave)

        self.play(
            eeg_phase.animate.set_value(4 * PI),
            FadeIn(label_eeg),
            run_time=max(0.05, 3.5
        ))

        head_group = VGroup(head_outline, electrode_eeg, label_eeg)

        # ---------- Beat 3: zoom toward electrode ----------
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(electrode_eeg.get_center()),
            label_eeg.animate.set_opacity(0).shift(RIGHT * 2),
            run_time=max(0.05, 1.5
        ))

        # ---------- Tissue cross-section ----------
        positions = [
            (0.0, 0.1), (-0.55, 0.45), (0.6, 0.35), (-0.25, -0.65),
            (0.7, -0.6), (-0.9, -0.2), (0.95, 0.8), (-0.85, 0.8),
            (0.2, 0.95), (-0.5, 0.95), (1.35, -0.1), (-1.45, 0.15),
            (1.1, -1.0), (-1.2, -1.0), (1.4, 1.2), (-1.4, 1.25),
            (0.05, -1.35), (1.7, 0.5), (-1.7, -0.4), (0.0, -1.1)
        ]

        def make_neuron(pos, color):
            pos = np.array([pos[0], pos[1], 0])
            soma = Circle(
                radius=0.13,
                color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1
            ).move_to(pos)

            dendrites = VGroup()
            for ang in [0, 2 * PI / 3, 4 * PI / 3]:
                direction = np.array([np.cos(ang), np.sin(ang), 0])
                start = pos + direction * 0.11
                end = pos + direction * 0.32
                dendrites.add(
                    Line(start, end, color=color, stroke_width=1.5)
                )
            return VGroup(soma, dendrites)

        neuron_colors = [TEAL, GREEN, ORANGE, PURPLE, PINK, BLUE, TEAL, GREEN]
        neuron_groups = []
        neuron_positions = []
        for i, pos in enumerate(positions):
            color = neuron_colors[i % len(neuron_colors)]
            neuron = make_neuron(pos, color)
            neuron_groups.append(neuron)
            neuron_positions.append(np.array([pos[0], pos[1], 0]))

        tissue_background = Rectangle(
            width=5.0, height=4.6,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLUE_E, fill_opacity=0.12
        ).move_to(ORIGIN)

        tissue_group = VGroup(tissue_background, *neuron_groups)

        # ---------- Beat 4: cross-fade to tissue ----------
        eeg_wave.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(2.5).move_to(ORIGIN),
            FadeOut(head_group),
            FadeOut(eeg_wave),
            FadeIn(tissue_group),
            run_time=max(0.05, 4.2
        ))

        # ---------- Beat 5: brightness pulse sweeps tissue ----------
        pulse = Rectangle(
            width=0.5,
            height=tissue_background.height,
            fill_color=YELLOW,
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(tissue_background.get_left())

        self.add(pulse)
        self.play(
            pulse.animate.move_to(tissue_background.get_right()).set_opacity(0),
            run_time=max(0.05, 3.0
        ))
        self.remove(pulse)
        self.wait(max(0.05, 0.3))

        # ---------- Beat 6: sharp electrode descends ----------
        probe = Polygon(
            [-0.08, 4.0, 0],
            [0.08, 4.0, 0],
            [0.03, 0.2, 0],
            [0, 0, 0],
            [-0.03, 0.2, 0],
        ).set_fill(GREY_B, opacity=1).set_stroke(WHITE, width=1)
        probe_height = probe.height

        tip_end = np.array([0, -0.2, 0])
        tip_start = np.array([
            tissue_group.get_center()[0],
            tissue_background.get_top()[1] + 2.8,
            0
        ])
        probe.move_to(tip_start + UP * (probe_height / 2))

        self.play(
            probe.animate.move_to(tip_end + UP * (probe_height / 2)),
            run_time=max(0.05, 3.7
        ))

        # ---------- Beat 7: blank trace panel appears ----------
        top_rect = Rectangle(
            width=3.2, height=1.4,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLUE_E, fill_opacity=0.10
        )
        bottom_rect = Rectangle(
            width=3.2, height=1.4,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLUE_E, fill_opacity=0.10
        )
        panel_group = VGroup(top_rect, bottom_rect).arrange(DOWN, buff=0.3)
        panel_group.next_to(tissue_group, RIGHT, buff=0.7)

        self.play(FadeIn(panel_group), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 2.0))

        # ---------- Beat 8: spike/LFP labels ----------
        spike_label = Text("Spike", font_size=26, color=GOLD).move_to(
            np.array([top_rect.get_left()[0] + 0.7, top_rect.get_center()[1], 0])
        )
        lfp_label = Text("LFP", font_size=26, color=TEAL).move_to(
            np.array([bottom_rect.get_left()[0] + 0.55, bottom_rect.get_center()[1], 0])
        )

        self.play(FadeIn(spike_label, lfp_label), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 1.6))

        trace_system_group = VGroup(panel_group, spike_label, lfp_label)

        # ---------- Trace waveform utilities ----------
        spike_progress = ValueTracker(0)
        lfp_progress = ValueTracker(0)
        spike_phase = ValueTracker(0)
        lfp_phase = ValueTracker(0)

        def make_spike_trace(progress, phase):
            left = top_rect.get_left()[0] + 0.85
            right = top_rect.get_right()[0] - 0.1
            width = right - left
            y0 = top_rect.get_center()[1]
            amp = top_rect.height * 0.32

            def tri(ph):
                return (2 / np.pi) * np.arcsin(np.sin(ph))

            return ParametricFunction(
                lambda t: np.array([
                    left + width * t * progress,
                    y0 + amp * tri(2 * PI * 9 * t * progress - phase),
                    0
                ]),
                t_range=[0, 1, 0.01],
                stroke_color=YELLOW,
                stroke_width=3
            )

        def make_lfp_trace(progress, phase):
            left = bottom_rect.get_left()[0] + 0.85
            right = bottom_rect.get_right()[0] - 0.1
            width = right - left
            y0 = bottom_rect.get_center()[1]
            amp = bottom_rect.height * 0.30

            return ParametricFunction(
                lambda t: np.array([
                    left + width * t * progress,
                    y0 + amp * np.sin(2 * PI * 1.4 * t * progress - phase),
                    0
                ]),
                t_range=[0, 1, 0.01],
                stroke_color=TEAL,
                stroke_width=3
            )

        spike_trace = always_redraw(
            lambda: make_spike_trace(spike_progress.get_value(), spike_phase.get_value())
        )
        lfp_trace = always_redraw(
            lambda: make_lfp_trace(lfp_progress.get_value(), lfp_phase.get_value())
        )

        # ---------- Beat 9: both traces begin drawing ----------
        self.add(spike_trace, lfp_trace)
        self.play(
            spike_progress.animate.set_value(1),
            lfp_progress.animate.set_value(1),
            run_time=max(0.05, 3.8),
            rate_func=linear
        )

        # ---------- Beat 10: traces continue, labels dim ----------
        self.play(
            spike_phase.animate.increment_value(8 * PI),
            lfp_phase.animate.increment_value(2.5 * PI),
            spike_label.animate.set_opacity(0.55),
            lfp_label.animate.set_opacity(0.55),
            run_time=max(0.05, 4.3
        ))

        # ---------- Beat 11: highlight single neuron ----------
        tip_position = tip_end
        idx = min(
            range(len(neuron_positions)),
            key=lambda i: np.linalg.norm(neuron_positions[i] - tip_position)
        )
        selected_neuron = neuron_groups[idx]

        selected_center = selected_neuron.get_center()
        vec = tip_position - selected_center
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        single_highlight = VGroup(
            Circle(
                radius=0.28,
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.20,
                stroke_width=3
            ).move_to(selected_center),
            Dot(
                point=selected_center + vec * 0.13,
                radius=0.06,
                color=YELLOW,
                fill_opacity=1
            )
        )

        self.play(FadeIn(single_highlight), run_time=max(0.05, 0.5))
        self.play(spike_phase.animate.increment_value(6 * PI), run_time=max(0.05, 2.2))
        self.play(
            Indicate(single_highlight, scale_factor=1.2, color=YELLOW),
            run_time=max(0.05, 0.6
        ))
        self.play(spike_phase.animate.increment_value(6 * PI), run_time=max(0.05, 0.8))

        # ---------- Beat 12: population glow ----------
        self.play(FadeOut(single_highlight), run_time=max(0.05, 0.8))

        def make_population_glow(center, radius, neuron_list):
            group = VGroup()
            for r, op in [(radius, 0.06), (radius * 0.6, 0.12), (radius * 0.3, 0.20)]:
                group.add(
                    Circle(
                        radius=r,
                        color=BLUE,
                        fill_color=BLUE,
                        fill_opacity=op,
                        stroke_width=0
                    ).move_to(center)
                )
            for neuron in neuron_list:
                group.add(
                    Circle(
                        radius=0.16,
                        color=BLUE,
                        fill_color=BLUE,
                        fill_opacity=0.15,
                        stroke_width=0
                    ).move_to(neuron.get_center())
                )
            return group

        pop_indices = [
            i for i, pos in enumerate(neuron_positions)
            if np.linalg.norm(np.array(pos) - tip_position) <= 1.2
        ]
        population_glow = make_population_glow(
            tip_position,
            1.2,
            [neuron_groups[i] for i in pop_indices]
        )

        pop_pulse = ValueTracker(0)
        self.play(FadeIn(population_glow), run_time=max(0.05, 0.5))
        population_glow.add_updater(
            lambda m: m.set_opacity(0.5 + 0.35 * np.sin(pop_pulse.get_value()))
        )
        self.play(
            pop_pulse.animate.set_value(4 * PI),
            lfp_phase.animate.increment_value(3 * PI),
            run_time=max(0.05, 6.0
        ))
        self.wait(max(0.05, 0.4))

        # ---------- Beat 13: shrink left, traces right, alternate ----------
        population_glow.clear_updaters()
        self.play(FadeOut(population_glow), run_time=max(0.05, 0.4))

        new_tissue_center = np.array([-3.2, 0, 0])
        new_tip = new_tissue_center + DOWN * 0.13
        new_probe_center = new_tip + UP * (probe_height / 2)

        self.play(
            tissue_group.animate.scale(0.65).move_to(new_tissue_center),
            probe.animate.move_to(new_probe_center),
            trace_system_group.animate.scale(0.85).move_to(RIGHT * 3.2),
            spike_phase.animate.increment_value(4 * PI),
            lfp_phase.animate.increment_value(2 * PI),
            run_time=max(0.05, 2.0
        ))

        tip_current = np.array([
            probe.get_center()[0],
            probe.get_bottom()[1],
            0
        ])
        selected_center2 = selected_neuron.get_center()
        vec2 = tip_current - selected_center2
        norm2 = np.linalg.norm(vec2)
        if norm2 > 0:
            vec2 = vec2 / norm2

        single_highlight2 = VGroup(
            Circle(
                radius=0.24,
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.25,
                stroke_width=3
            ).move_to(selected_center2),
            Dot(
                point=selected_center2 + vec2 * 0.13,
                radius=0.05,
                color=YELLOW,
                fill_opacity=1
            )
        )

        self.play(FadeIn(single_highlight2), run_time=max(0.05, 0.5))
        self.play(
            Indicate(single_highlight2, scale_factor=1.2, color=YELLOW),
            spike_phase.animate.increment_value(6 * PI),
            run_time=max(0.05, 1.0
        ))
        self.play(FadeOut(single_highlight2), run_time=max(0.05, 0.3))

        pop_indices2 = [
            i for i, neuron in enumerate(neuron_groups)
            if np.linalg.norm(neuron.get_center() - tip_current) <= 1.2 * 0.65
        ]
        population_glow2 = make_population_glow(
            tip_current,
            1.2 * 0.65,
            [neuron_groups[i] for i in pop_indices2]
        )

        self.play(
            FadeIn(population_glow2),
            lfp_phase.animate.increment_value(PI),
            run_time=max(0.05, 0.7
        ))
        self.play(
            population_glow2.animate.set_opacity(0.8).scale(1.15),
            lfp_phase.animate.increment_value(2 * PI),
            run_time=max(0.05, 0.6
        ))
        self.play(
            population_glow2.animate.set_opacity(0.4).scale(0.87),
            run_time=max(0.05, 0.6
        ))
        self.play(FadeOut(population_glow2), run_time=max(0.05, 0.6))

        # ---------- Beat 14: final composition ----------
        caption = Text(
            "Complementary views",
            font_size=32,
            color=WHITE
        ).to_edge(DOWN, buff=0.4)

        self.play(
            spike_phase.animate.increment_value(2 * PI),
            lfp_phase.animate.increment_value(1.2 * PI),
            spike_label.animate.set_opacity(1),
            lfp_label.animate.set_opacity(1),
            FadeIn(caption),
            run_time=max(0.05, 4.97
        ))