ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {}

class Scene9(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Shared waveform parameters
        # ------------------------------------------------------------
        x_wave = np.linspace(-2.2, 2.2, 520)

        def make_signal(low_scale=1.0, high_scale=0.8, phase=0.0):
            t = 2.5 * x_wave + 5.0 + phase

            # Broad slow LFP waves
            slow = (
                0.45 * np.sin(0.55 * t)
                + 0.22 * np.sin(1.05 * t + 1.2)
                + 0.15 * np.sin(1.6 * t + 2.3)
            )

            # Sharp narrow action-potential spikes
            spike_centers = [-1.6, -0.55, 0.7, 1.5]
            spike_widths  = [0.15, 0.16, 0.14, 0.15]
            spike_freqs   = [28.0, 30.0, 26.0, 29.0]
            spike_amps    = [0.60, 0.68, 0.55, 0.62]

            high = np.zeros_like(x_wave)
            for cx, w, f, a in zip(spike_centers, spike_widths, spike_freqs, spike_amps):
                high += a * np.exp(-((x_wave - cx) ** 2) / (2 * w * w)) * np.sin(f * x_wave + 0.8)

            total = 0.85 * (low_scale * slow + high_scale * high)
            return np.column_stack([x_wave, total, np.zeros_like(x_wave)])

        def make_wave_mobject(points, color=WHITE, stroke_width=2.5):
            wave = VMobject()
            wave.set_points_as_corners(points)
            wave.set_stroke(color=color, width=stroke_width)
            wave.set_fill(opacity=0)
            return wave

        # ------------------------------------------------------------
        # Screen / chart display (right side)
        # ------------------------------------------------------------
        screen = RoundedRectangle(
            width=5.0,
            height=2.8,
            corner_radius=0.10,
            fill_color="#181C24",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to(np.array([3.5, 0.0, 0]))

        # Grid lines inside screen
        grid_lines = VGroup()
        for y_off in np.linspace(-1.2, 1.2, 7):
            grid_line = DashedLine(
                screen.get_left() + RIGHT * 0.12,
                screen.get_right() + LEFT * 0.12,
                color=GREY_B,
                dash_length=0.06,
                stroke_width=0.9,
            )
            grid_line.move_to(np.array([screen.get_center()[0], y_off, 0]))
            grid_line.set_opacity(0.12)
            grid_lines.add(grid_line)

        for x_rel in np.linspace(-2.0, 2.0, 9):
            grid_line = DashedLine(
                np.array([x_rel + screen.get_center()[0], screen.get_bottom()[1] + 0.12, 0]),
                np.array([x_rel + screen.get_center()[0], screen.get_top()[1] - 0.12, 0]),
                color=GREY_B,
                dash_length=0.06,
                stroke_width=0.9,
            )
            grid_line.set_opacity(0.12)
            grid_lines.add(grid_line)

        center_line_disp = DashedLine(
            screen.get_left() + RIGHT * 0.12,
            screen.get_right() + LEFT * 0.12,
            color=GREY_B,
            dash_length=0.08,
            stroke_width=1.2,
        ).move_to(screen.get_center())
        center_line_disp.set_opacity(0.18)

        display_group = VGroup(screen, grid_lines, center_line_disp)

        # Label above display
        extracellular_label = Text("extracellular recording", font_size=28, color=WHITE)
        extracellular_label.next_to(screen, UP, buff=0.22)

        # ------------------------------------------------------------
        # Microelectrode (left side)
        # ------------------------------------------------------------
        # Tapered needle shaft, tip pointing toward neurons
        needle_tip  = np.array([-4.7, -1.5, 0])
        needle_base_l = np.array([-5.5, 0.2, 0])
        needle_base_r = np.array([-4.9, 0.2, 0])
        needle_mid_l  = np.array([-5.3, -0.3, 0])
        needle_mid_r  = np.array([-4.8, -0.5, 0])

        needle = Polygon(
            needle_tip,
            needle_mid_l,
            needle_base_l,
            needle_base_r,
            needle_mid_r,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        )

        # Neurons: three cell bodies with short dendrites
        neuron_colors = [TEAL, PURPLE, ORANGE]
        neuron_centers = [
            np.array([-5.2, -1.8, 0]),
            np.array([-4.6, -2.0, 0]),
            np.array([-5.0, -1.4, 0]),
        ]

        neurons = VGroup()
        for center, col in zip(neuron_centers, neuron_colors):
            soma = Circle(
                radius=0.18,
                fill_color=col,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1.5,
            ).move_to(center)

            dendrites = VGroup()
            for angle in np.linspace(0, 2 * np.pi, 6, endpoint=False):
                branch = Line(
                    soma.get_center(),
                    soma.get_center() + 0.45 * np.array([np.cos(angle), np.sin(angle), 0]),
                    color=col,
                    stroke_width=2.5,
                )
                dendrites.add(branch)

            neuron = VGroup(soma, dendrites)
            neurons.add(neuron)

        # ------------------------------------------------------------
        # Wiring (initially direct, later split through filter)
        # ------------------------------------------------------------
        wire_start = np.array([-5.2, 0.2, 0])   # needle base
        wire_end   = screen.get_left()          # left edge of screen center

        initial_wire = Line(wire_start, wire_end, color=GREY_B, stroke_width=2.5)

        # High-pass filter box (appears in beat 3 dim, activates in beat 5)
        filter_center = np.array([-2.1, 0.1, 0])
        filter_rect = RoundedRectangle(
            width=2.2,
            height=0.9,
            corner_radius=0.18,
            fill_color="#181C24",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        )
        filter_text = Text("High-pass filter", font_size=20, color=GREY_B)
        filter_text.scale_to_fit_width(filter_rect.width - 0.5)
        filter_text.move_to(filter_rect.get_center())
        dim_filter_group = VGroup(filter_rect, filter_text).move_to(filter_center)

        # Split wires when filter is present
        split_wire_left  = Line(wire_start, filter_rect.get_left(), color=GREY_B, stroke_width=2.5)
        split_wire_right = Line(filter_rect.get_right(), wire_end, color=GREY_B, stroke_width=2.5)
        split_wires = VGroup(split_wire_left, split_wire_right)

        # Bright/active filter version
        bright_filter_rect = RoundedRectangle(
            width=2.2,
            height=0.9,
            corner_radius=0.18,
            fill_color="#1B2B3A",
            fill_opacity=1,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        bright_filter_text = Text("High-pass filter", font_size=20, color=WHITE)
        bright_filter_text.scale_to_fit_width(bright_filter_rect.width - 0.5)
        bright_filter_text.move_to(bright_filter_rect.get_center())
        bright_filter_group = VGroup(bright_filter_rect, bright_filter_text).move_to(filter_center)

        # ------------------------------------------------------------
        # Callouts
        # ------------------------------------------------------------
        # LFP callout (low-frequency)
        lfp_label = Text("LFP: low-frequency", font_size=24, color=YELLOW)
        lfp_label.move_to(np.array([-0.8, -1.9, 0]))  # outside bottom-left of screen
        lfp_arrow = Arrow(
            start=lfp_label.get_top() + UP * 0.1,
            end=np.array([1.6, -0.7, 0]),
            color=YELLOW,
            buff=0.05,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.2,
        )
        lfp_group = VGroup(lfp_label, lfp_arrow)

        # Spike callout (high-frequency)
        spike_label = Text("spikes: high-frequency", font_size=24, color=YELLOW)
        spike_label.move_to(np.array([5.2, 2.0, 0]))  # outside top-right of screen
        spike_arrow = Arrow(
            start=spike_label.get_bottom() + DOWN * 0.1,
            end=np.array([3.05, 0.55, 0]),  # near a spike
            color=YELLOW,
            buff=0.05,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.2,
        )
        spike_group = VGroup(spike_label, spike_arrow)

        # Bottom label after filtering
        after_filter_label = Text("spike recording after filtering", font_size=26, color=WHITE)
        after_filter_label.next_to(screen, DOWN, buff=0.25)

        # ------------------------------------------------------------
        # Pre-computed waveforms
        # ------------------------------------------------------------
        # Mixed states
        wave_full_0  = make_wave_mobject(make_signal(1.0, 0.8, 0.0)).move_to(screen.get_center())
        wave_full_30 = make_wave_mobject(make_signal(1.0, 0.8, 0.5)).move_to(screen.get_center())
        wave_mid_06  = make_wave_mobject(make_signal(0.6, 0.85, 1.0)).move_to(screen.get_center())
        wave_mid_03  = make_wave_mobject(make_signal(0.3, 0.9, 1.5)).move_to(screen.get_center())
        wave_pure_0  = make_wave_mobject(make_signal(0.0, 1.0, 2.0)).move_to(screen.get_center())
        wave_pure_30 = make_wave_mobject(make_signal(0.0, 1.0, 2.5)).move_to(screen.get_center())
        wave_pure_60 = make_wave_mobject(make_signal(0.0, 1.0, 3.0)).move_to(screen.get_center())

        current_wave = wave_full_0

        # ------------------------------------------------------------
        # BEAT 1: 0.00–2.78  (setup appears)
        # ------------------------------------------------------------
        self.play(
            FadeIn(needle),
            FadeIn(neurons),
            FadeIn(display_group),
            FadeIn(initial_wire),
            FadeIn(extracellular_label),
            run_time=max(0.05, 2.78),
        )

        # ------------------------------------------------------------
        # BEAT 2: 2.78–4.38  (live trace begins: mixed signal)
        # ------------------------------------------------------------
        self.play(Create(current_wave), run_time=max(0.05, 1.60))

        # ------------------------------------------------------------
        # BEAT 3: 4.38–6.62  (high-pass filter box appears, dim)
        # ------------------------------------------------------------
        # Fade out direct wire, fade in split wires and dim filter
        self.play(
            FadeOut(initial_wire),
            FadeIn(dim_filter_group),
            FadeIn(split_wires),
            run_time=max(0.05, 0.8),
        )
        # Continue live trace with slight phase shift
        self.play(
            Transform(current_wave, wave_full_30),
            run_time=max(0.05, 1.44),
        )
        current_wave = wave_full_30

        # ------------------------------------------------------------
        # BEAT 4: 6.62–8.84  (LFP and spike callouts appear)
        # ------------------------------------------------------------
        self.play(
            FadeIn(lfp_group),
            FadeIn(spike_group),
            run_time=max(0.05, 2.22),
        )

        # ------------------------------------------------------------
        # GAP: 8.84–9.42  (hold)
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.58))

        # ------------------------------------------------------------
        # BEAT 5: 9.42–12.48  (filter activates, slow waves fade)
        # ------------------------------------------------------------
        # Quick flash/click on filter box
        self.play(Indicate(dim_filter_group, color=YELLOW, scale_factor=1.1), run_time=max(0.05, 0.5))

        # Switch filter box to bright/active
        self.play(ReplacementTransform(dim_filter_group, bright_filter_group), run_time=max(0.05, 0.4))
        dim_filter_group = bright_filter_group  # now refer to active box

        # Gradually reduce low-frequency amplitude
        self.play(Transform(current_wave, wave_mid_06), run_time=max(0.05, 0.6))
        current_wave = wave_mid_06

        self.play(Transform(current_wave, wave_mid_03), run_time=max(0.05, 0.6))
        current_wave = wave_mid_03

        # Last step: pure spikes, and fade out LFP callout
        self.play(
            Transform(current_wave, wave_pure_0),
            FadeOut(lfp_group),
            run_time=max(0.05, 0.6),
        )
        current_wave = wave_pure_0

        # Small hold to fill exact beat duration (3.06 - 2.7 = 0.36)
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------
        # BEAT 6: 13.20–14.84  (clean spikes only, bottom label)
        # ------------------------------------------------------------
        self.play(Write(after_filter_label), run_time=max(0.05, 1.64))

        # ------------------------------------------------------------
        # BEAT 7: 14.84–17.22  (clean spikes continue)
        # ------------------------------------------------------------
        self.play(Transform(current_wave, wave_pure_30), run_time=max(0.05, 0.8))
        current_wave = wave_pure_30
        self.wait(max(0.05, 0.78))

        self.play(Transform(current_wave, wave_pure_60), run_time=max(0.05, 0.8))
        current_wave = wave_pure_60

        # ------------------------------------------------------------
        # BEAT 8: 17.22–18.10  (hold, then fade out)
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.38))
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=max(0.05, 0.5))