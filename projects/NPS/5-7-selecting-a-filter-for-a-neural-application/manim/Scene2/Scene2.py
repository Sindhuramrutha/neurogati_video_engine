ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Beat 1: Recording setup + trace (0 - 12.84) ---
        # stylized microelectrode tip
        tip_body = Polygon(
            [-0.2, 0.4, 0], [0.2, 0.4, 0], [0, 1.2, 0],
            fill_color=GREY, fill_opacity=1, stroke_width=1, stroke_color=WHITE
        )
        tip_shaft = Rectangle(height=2.5, width=0.08, fill_color=GREY, fill_opacity=1, stroke_width=0)
        tip_shaft.next_to(tip_body, UP, buff=0)
        electrode_tip = VGroup(tip_shaft, tip_body).move_to(np.array([-5.5, 2.5, 0]))

        # stylized neuron
        neuron_body = Circle(radius=0.6, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
        neuron_body.next_to(electrode_tip, RIGHT, buff=0.8)
        dendrites = VGroup(*[
            Line(
                neuron_body.get_edge_center(UP + LEFT * 0.8),
                neuron_body.get_edge_center(UP + LEFT * 0.8) + normalize(UP + LEFT) * 0.5,
                stroke_color=PURPLE, stroke_width=3
            ) for _ in range(3)
        ])
        axon = Line(
            neuron_body.get_edge_center(DOWN * 0.9 + RIGHT * 0.4),
            neuron_body.get_edge_center(DOWN * 0.9 + RIGHT * 0.4) + DOWN * 1.2,
            stroke_color=PURPLE, stroke_width=4
        )
        neuron = VGroup(neuron_body, dendrites, axon)
        recording_setup = VGroup(electrode_tip, neuron).move_to(np.array([-5.5, 2.2, 0]))

        # raw noisy voltage trace data
        n_pts = 600
        t = np.linspace(0, 10 * np.pi, n_pts)
        slow_wave = 1.2 * np.sin(t * 0.8)          # neural waveform
        fast_noise = 0.5 * np.sin(t * 9.0) + 0.3 * np.sin(t * 17.0)  # high-frequency noise
        raw_signal = slow_wave + fast_noise

        x_scale = 14.0 / (n_pts - 1)
        y_scale = 1.0
        trace_points = [
            np.array([-7.0 + i * x_scale, raw_signal[i] * y_scale - 1.8, 0])
            for i in range(n_pts)
        ]
        trace = VMobject(stroke_color=WHITE, stroke_width=2).set_points_as_corners(trace_points)

        self.play(FadeIn(recording_setup), run_time=max(0.05, 1.0))
        self.play(Write(trace), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 12.84 - 1.0 - 1.5))  # 10.34

        # --- Beat 2: "What signal?" + cyan glow on slow waveform (12.84 - 14.68) ---
        q_signal = Text("What signal?", font_size=36, color=WHITE)
        q_signal.next_to(recording_setup, UP, buff=0.6)
        q_signal.to_edge(UP, buff=0.4)

        self.play(Write(q_signal), run_time=max(0.05, 0.4))

        # cyan outline for underlying slow wave (use TEAL as cyan substitute)
        slow_trace = VMobject(stroke_color=TEAL, stroke_width=6, stroke_opacity=0.9)
        slow_pts = [
            np.array([-7.0 + i * x_scale, slow_wave[i] * y_scale - 1.8, 0])
            for i in range(n_pts)
        ]
        slow_trace.set_points_as_corners(slow_pts)

        self.play(FadeIn(slow_trace), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.7))  # brief glow
        self.play(FadeOut(slow_trace), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 1.84 - 0.4 - 0.3 - 0.7 - 0.3))  # 0.14

        # --- Beat 3: "What noise?" + red tint on high-frequency noise (14.68 - 17.16) ---
        q_noise = Text("What noise?", font_size=36, color=WHITE)
        q_noise.next_to(q_signal, DOWN, buff=0.35)

        self.play(Write(q_noise), run_time=max(0.05, 0.5))

        # semi-transparent red overlay for fast noise component
        noise_trace = VMobject(stroke_color=RED, stroke_width=3, stroke_opacity=0.5)
        noise_pts = [
            np.array([-7.0 + i * x_scale, fast_noise[i] * y_scale - 1.8, 0])
            for i in range(n_pts)
        ]
        noise_trace.set_points_as_corners(noise_pts)

        self.play(FadeIn(noise_trace), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.48 - 0.5 - 0.5))  # 1.48

        # --- Beat 4: "Which frequencies are useful?" + spectrum (17.16 - 21.02) ---
        q_freqs = Text("Which frequencies are useful?", font_size=36, color=WHITE)
        q_freqs.next_to(q_noise, DOWN, buff=0.35)

        self.play(Write(q_freqs), run_time=max(0.05, 0.5))

        # build frequency spectrum (magnitude vs frequency)
        spectrum_ax = Line([-3.5, -3, 0], [3.5, -3, 0], stroke_color=GREY, stroke_width=2)
        spectrum_ay = Line([-3.5, -3, 0], [-3.5, -1, 0], stroke_color=GREY, stroke_width=2)
        spectrum_group = VGroup(spectrum_ax, spectrum_ay)

        freq_pts = np.linspace(0, 200, 200)
        mag = np.exp(-0.03 * freq_pts) * 1.5 + 0.15
        mag[40:] *= 0.7  # drop after ~100 Hz
        curve_pts = [
            np.array([-3.5 + (f / 200) * 7.0, -3.0 + mag[i] * 2.0, 0])
            for i, f in enumerate(freq_pts)
        ]
        mag_curve = VMobject(stroke_color=BLUE, stroke_width=3).set_points_as_corners(curve_pts)

        # frequency band 0.5 Hz to 100 Hz
        x_left = -3.5 + (0.5 / 200) * 7.0
        x_right = -3.5 + (100 / 200) * 7.0
        band_rect = Rectangle(
            width=x_right - x_left, height=2.0,
            fill_color=GREEN, fill_opacity=0.18, stroke_width=0
        )
        band_rect.move_to(np.array([(x_left + x_right) / 2, -3.0 + 1.0, 0]))
        band_label = Text("physiological information", font_size=20, color=GREEN)
        band_label.next_to(band_rect, DOWN, buff=0.15)

        # prepare red strike for >100 Hz (hidden initially)
        strike_line = Line(
            [0.2, -1.8, 0], [2.0, -0.5, 0],
            stroke_color=RED, stroke_width=5, stroke_opacity=0
        )

        # assemble spectrum and position beside trace
        spectrum_full = VGroup(spectrum_group, mag_curve, band_rect, band_label, strike_line)
        spectrum_full.move_to(np.array([3.5, -0.2, 0]))

        self.play(FadeIn(spectrum_group), FadeIn(mag_curve), run_time=max(0.05, 0.8))
        self.play(FadeIn(band_rect), Write(band_label), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 3.86 - 0.5 - 0.8 - 0.8))  # 1.76

        # --- Beat 5: "Which frequencies to remove?" + red strike (21.02 - 29.80) ---
        q_remove = Text("Which frequencies to remove?", font_size=36, color=WHITE)
        q_remove.next_to(q_freqs, DOWN, buff=0.35)

        self.play(Write(q_remove), run_time=max(0.05, 0.5))

        # reveal the diagonal red strike line
        self.play(strike_line.animate.set_stroke(opacity=1), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 8.78 - 0.5 - 0.5))  # 7.78

        # --- Beat 6: Fade out, key phrase + green check (29.80 - 33.75) ---
        everything_else = VGroup(
            recording_setup, trace, noise_trace, spectrum_full,
            q_signal, q_noise, q_freqs, q_remove
        )
        self.play(FadeOut(everything_else), run_time=max(0.05, 0.8))

        # key phrase and green check icon
        key_phrase = Text(
            "Choose the filter based on the signal,\nnot on the software",
            font_size=42, color=WHITE, line_spacing=1.2
        )
        check_icon = SVGMobject(ASSET_PATHS["check_circle"], fill_color=GREEN, fill_opacity=1, stroke_width=0)
        check_icon.scale(0.8)
        check_icon.next_to(key_phrase, RIGHT, buff=0.6)
        full_phrase = VGroup(check_icon, key_phrase)

        # start small and off-center, then enlarge and move to center
        full_phrase.scale(0.6)
        full_phrase.move_to(UP * 2 + RIGHT * 2)
        self.play(
            FadeIn(full_phrase, shift=DOWN * 0.3),
            full_phrase.animate.scale(1 / 0.6).move_to(ORIGIN),
            run_time=max(0.05, 1.2
        ))
        self.wait(max(0.05, 3.95 - 0.8 - 1.2))  # 1.95