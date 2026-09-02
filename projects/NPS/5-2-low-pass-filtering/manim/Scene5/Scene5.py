ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Waveform helpers use this common width inside the panels
        self.wave_width = 2.9

        # ------------------------------------------------------------------
        # Beat 1: 0.00 - 3.74 -- three empty panel outlines + title
        # ------------------------------------------------------------------
        panel_width = 3.6
        panel_height = 2.6
        panel_y = 0.7

        panel1 = Rectangle(
            width=panel_width,
            height=panel_height,
            color=GREY_B,
            stroke_width=1.5,
            fill_opacity=0,
        )
        panel2 = Rectangle(
            width=panel_width,
            height=panel_height,
            color=GREY_B,
            stroke_width=1.5,
            fill_opacity=0,
        )
        panel3 = Rectangle(
            width=panel_width,
            height=panel_height,
            color=GREY_B,
            stroke_width=1.5,
            fill_opacity=0,
        )
        panels_group = VGroup(panel1, panel2, panel3).arrange(RIGHT, buff=0.6)
        panels_group.move_to(UP * panel_y)

        p1_center = panel1.get_center()
        p2_center = panel2.get_center()
        p3_center = panel3.get_center()

        title = Text(
            "Low-Pass Filters in Neuroscience",
            font_size=34,
            color=WHITE,
        )
        title.move_to(UP * 3.42)

        self.play(
            Create(panels_group),
            FadeIn(title),
            run_time=max(0.05, 3.74),
        )

        # ------------------------------------------------------------------
        # Beat 2: 3.74 - 8.76 -- soft low-frequency wave in first panel
        # ------------------------------------------------------------------
        p1_soft_glow = self.make_wave_mobject(
            self.p1_slow_arr,
            p1_center,
            color=TEAL,
            stroke_width=12,
        ).set_opacity(0.25)
        p1_soft_wave = self.make_wave_mobject(
            self.p1_slow_arr,
            p1_center,
            color=TEAL,
            stroke_width=4,
        )

        low_freq_text = Text("Low Frequencies", font_size=24, color=TEAL)
        low_freq_text.move_to(p1_center + DOWN * 1.9)

        self.play(FadeIn(p1_soft_glow), FadeIn(p1_soft_wave), run_time=max(0.05, 1.20))
        self.play(
            p1_soft_wave.animate.set_stroke(width=8),
            p1_soft_glow.animate.set_stroke(width=16),
            rate_func=there_and_back,
            run_time=max(0.05, 1.50),
        )
        self.play(Write(low_freq_text), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.60))
        self.play(FadeOut(low_freq_text), run_time=max(0.05, 0.92))

        # Gap 8.76 - 9.80
        self.wait(max(0.05, 1.04))

        # ------------------------------------------------------------------
        # Beat 3: 9.80 - 11.00 -- jagged EEG in first panel
        # ------------------------------------------------------------------
        p1_sweep = ValueTracker(-1.8)
        p1_wave = always_redraw(
            lambda: self.make_p1_wave(p1_center, p1_sweep.get_value())
        )

        p1_focus = SurroundingRectangle(
            panel1,
            color=YELLOW,
            stroke_width=3,
            buff=0.08,
        )
        eeg_label = Text("EEG", font_size=28, color=WHITE)
        eeg_label.move_to(p1_center + UP * 1.65)

        self.add(p1_wave)
        self.play(
            FadeOut(p1_soft_wave),
            FadeOut(p1_soft_glow),
            FadeIn(p1_focus),
            Write(eeg_label),
            panel2.animate.set_opacity(0.35),
            panel3.animate.set_opacity(0.35),
            run_time=max(0.05, 1.20),
        )

        # ------------------------------------------------------------------
        # Beat 4: 11.00 - 15.24 -- sweep low-pass filter across EEG
        # ------------------------------------------------------------------
        p1_sweep_band = always_redraw(
            lambda: Rectangle(
                width=0.35,
                height=2.2,
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.10,
                stroke_width=0,
            ).move_to(
                np.array([
                    p1_center[0] + p1_sweep.get_value(),
                    p1_center[1],
                    0,
                ])
            )
        )
        filter_p1 = self.make_filter_block(p1_center)

        self.add(p1_sweep_band)
        self.play(
            FadeIn(filter_p1),
            FadeOut(p1_focus),
            run_time=max(0.05, 0.50),
        )
        self.play(p1_sweep.animate.set_value(1.8), run_time=max(0.05, 3.00))
        self.remove(p1_sweep_band)
        self.play(FadeOut(filter_p1), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.24))

        # ------------------------------------------------------------------
        # Beat 5: 15.24 - 19.22 -- clean EEG + preserved-frequencies label
        # ------------------------------------------------------------------
        p1_result_text = Text(
            "Noise Reduced — Relevant EEG Frequencies Preserved",
            font_size=18,
            color=GREEN,
        )
        p1_result_text.scale_to_fit_width(2.9)
        p1_result_text.move_to(p1_center + DOWN * 1.9)

        self.play(Write(p1_result_text), run_time=max(0.05, 1.50))
        self.wait(max(0.05, 2.48))

        # Gap 19.22 - 20.34
        self.wait(max(0.05, 1.12))

        # ------------------------------------------------------------------
        # Beat 6: 20.34 - 23.30 -- LFP waveform + spikes in second panel
        # ------------------------------------------------------------------
        p2_lfp_wave = self.make_wave_mobject(
            self.lfp_slow_arr,
            p2_center,
            color=TEAL,
            stroke_width=4,
        )
        p2_spikes = self.make_lfp_spikes(p2_center)

        p2_focus = SurroundingRectangle(
            panel2,
            color=YELLOW,
            stroke_width=3,
            buff=0.08,
        )
        lfp_label = Text("LFP", font_size=28, color=WHITE)
        lfp_label.move_to(p2_center + UP * 1.65)

        self.play(
            FadeOut(p1_result_text),
            FadeIn(p2_focus),
            FadeIn(p2_lfp_wave),
            FadeIn(p2_spikes),
            Write(lfp_label),
            panel1.animate.set_opacity(0.35),
            panel3.animate.set_opacity(0.35),
            panel2.animate.set_opacity(1.0),
            run_time=max(0.05, 2.96),
        )
        self.bring_to_front(p2_spikes)

        # ------------------------------------------------------------------
        # Beat 7: 23.30 - 26.12 -- highlight smooth LFP, dim spikes, annotate
        # ------------------------------------------------------------------
        p2_lfp_glow = self.make_wave_mobject(
            self.lfp_slow_arr,
            p2_center,
            color=TEAL,
            stroke_width=12,
        ).set_opacity(0.0)

        lower_lfp_text = Text(
            "Lower-Frequency LFP Activity",
            font_size=18,
            color=TEAL,
        )
        lower_lfp_text.scale_to_fit_width(2.2)
        lower_lfp_text.move_to(
            np.array([p2_center[0] - 1.45, p2_center[1] - 2.10, 0])
        )

        lower_lfp_target = np.array([
            p2_center[0] - 0.6,
            p2_center[1] + self.lfp_slow_val(-0.6),
            0,
        ])
        lower_lfp_arrow = Arrow(
            start=lower_lfp_text.get_top() + UP * 0.05,
            end=lower_lfp_target,
            color=TEAL,
            stroke_width=2,
            buff=0.06,
        )

        higher_spike_text = Text(
            "Higher-Frequency Spike Activity",
            font_size=18,
            color=ORANGE,
        )
        higher_spike_text.scale_to_fit_width(2.2)
        higher_spike_text.move_to(
            np.array([p2_center[0] + 1.45, p2_center[1] - 2.10, 0])
        )
        higher_spike_target = np.array([
            p2_center[0] + 0.4,
            p2_center[1] + 0.72,
            0,
        ])
        higher_spike_arrow = Arrow(
            start=higher_spike_text.get_top() + UP * 0.05,
            end=higher_spike_target,
            color=ORANGE,
            stroke_width=2,
            buff=0.06,
        )

        p2_annotations = VGroup(
            lower_lfp_text,
            lower_lfp_arrow,
            higher_spike_text,
            higher_spike_arrow,
        )

        self.add(p2_lfp_glow)
        self.bring_to_back(p2_lfp_glow)
        self.bring_to_front(p2_lfp_wave)
        self.bring_to_front(p2_spikes)

        self.play(
            p2_lfp_glow.animate.set_opacity(0.25),
            p2_spikes.animate.set_opacity(0.35),
            FadeIn(p2_annotations),
            run_time=max(0.05, 2.82),
        )

        # ------------------------------------------------------------------
        # Beat 8: 26.12 - 31.94 -- remove LFP spikes one by one
        # ------------------------------------------------------------------
        filter_p2 = self.make_filter_block(p2_center)
        spike_list = list(p2_spikes.submobjects)
        n_spikes = len(spike_list)
        per_spike = max(0.05, 4.20 / n_spikes)

        self.play(
            FadeIn(filter_p2),
            FadeOut(p2_focus),
            p2_spikes.animate.set_opacity(1.0),
            run_time=max(0.05, 0.60),
        )

        for spike in spike_list:
            self.play(
                spike.animate.scale(
                    0.001,
                    about_point=spike.get_center(),
                ).set_opacity(0),
                run_time=max(0.05, per_spike),
            )

        self.play(FadeOut(filter_p2), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.52))

        # Gap 31.94 - 32.98
        self.wait(max(0.05, 1.04))

        # ------------------------------------------------------------------
        # Beat 9: 32.98 - 35.16 -- raw EMG in third panel
        # ------------------------------------------------------------------
        p3_rectify = ValueTracker(0.0)
        p3_sweep = ValueTracker(-1.8)
        p3_wave = always_redraw(
            lambda: self.make_p3_wave(
                p3_center,
                p3_rectify.get_value(),
                p3_sweep.get_value(),
            )
        )

        p3_focus = SurroundingRectangle(
            panel3,
            color=YELLOW,
            stroke_width=3,
            buff=0.08,
        )
        emg_label = Text("EMG", font_size=28, color=WHITE)
        emg_label.move_to(p3_center + UP * 1.65)

        self.add(p3_wave)
        self.bring_to_front(p3_wave)
        self.play(
            FadeOut(p2_annotations),
            FadeOut(p2_lfp_glow),
            FadeIn(p3_focus),
            Write(emg_label),
            panel1.animate.set_opacity(0.35),
            panel2.animate.set_opacity(0.35),
            panel3.animate.set_opacity(1.0),
            run_time=max(0.05, 2.18),
        )

        # ------------------------------------------------------------------
        # Beat 10: 35.16 - 37.64 -- rectify EMG
        # ------------------------------------------------------------------
        emg_rectified_label = Text("EMG — Rectified", font_size=28, color=WHITE)
        emg_rectified_label.move_to(p3_center + UP * 1.65)

        self.play(
            p3_rectify.animate.set_value(1.0),
            Transform(emg_label, emg_rectified_label),
            run_time=max(0.05, 2.48),
        )

        # ------------------------------------------------------------------
        # Beat 11: 37.64 - 41.60 -- smooth rectified EMG into envelope
        # ------------------------------------------------------------------
        filter_p3 = self.make_filter_block(p3_center)
        p3_sweep_band = always_redraw(
            lambda: Rectangle(
                width=0.35,
                height=2.2,
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.10,
                stroke_width=0,
            ).move_to(
                np.array([
                    p3_center[0] + p3_sweep.get_value(),
                    p3_center[1],
                    0,
                ])
            )
        )

        self.add(p3_sweep_band)
        self.play(FadeIn(filter_p3), run_time=max(0.05, 0.50))
        self.play(p3_sweep.animate.set_value(1.8), run_time=max(0.05, 2.50))
        self.remove(p3_sweep_band)
        self.play(FadeOut(filter_p3), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.46))

        # ------------------------------------------------------------------
        # Beat 12: 41.60 - 44.76 -- highlight EMG envelope + annotate
        # ------------------------------------------------------------------
        p3_envelope_glow = self.make_wave_mobject(
            self.p3_envelope_arr,
            p3_center,
            color=PINK,
            stroke_width=12,
        ).set_opacity(0.0)

        emg_envelope_label = Text("EMG Envelope", font_size=28, color=WHITE)
        emg_envelope_label.move_to(p3_center + UP * 1.65)

        envelope_text = Text(
            "Overall Level of Muscle Activation",
            font_size=18,
            color=PINK,
        )
        envelope_text.scale_to_fit_width(2.6)
        envelope_text.move_to(p3_center + DOWN * 2.0)

        envelope_target = np.array([
            p3_center[0] - 0.7,
            p3_center[1] + self.p3_envelope_val(-0.7),
            0,
        ])
        envelope_arrow = Arrow(
            start=envelope_text.get_top() + UP * 0.05,
            end=envelope_target,
            color=PINK,
            stroke_width=2,
            buff=0.06,
        )
        envelope_annotation = VGroup(envelope_text, envelope_arrow)

        self.add(p3_envelope_glow)
        self.bring_to_back(p3_envelope_glow)
        self.bring_to_front(p3_wave)

        self.play(
            Transform(emg_label, emg_envelope_label),
            p3_envelope_glow.animate.set_opacity(0.30),
            FadeIn(envelope_annotation),
            run_time=max(0.05, 1.50),
        )
        self.play(
            p3_envelope_glow.animate.set_stroke(width=16),
            rate_func=there_and_back,
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.66))

        # ------------------------------------------------------------------
        # Beat 13: 44.76 - 45.83 -- all three panels shown together
        # ------------------------------------------------------------------
        self.play(
            panel1.animate.set_opacity(1.0),
            panel2.animate.set_opacity(1.0),
            panel3.animate.set_opacity(1.0),
            FadeOut(p3_focus),
            run_time=max(0.05, 1.07),
        )

    # ------------------------------------------------------------------
    # Waveform generators
    # ------------------------------------------------------------------
    def make_wave_mobject(
        self,
        arr_func,
        center,
        color=WHITE,
        stroke_width=4,
        num_points=600,
    ):
        xs = np.linspace(-self.wave_width / 2, self.wave_width / 2, num_points)
        ys = arr_func(xs)
        pts = np.column_stack([
            xs + center[0],
            ys + center[1],
            np.zeros(num_points),
        ])
        wave = VMobject(
            stroke_color=color,
            stroke_width=stroke_width,
            fill_opacity=0,
        )
        wave.set_points_as_corners(pts)
        return wave

    def make_filter_block(self, panel_center):
        rect = Rectangle(
            width=1.7,
            height=0.5,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.15,
            stroke_width=2,
        )
        label = Text("Low-Pass Filter", font_size=15, color=YELLOW)
        label.scale_to_fit_width(1.5)
        group = VGroup(rect, label)
        group.move_to(panel_center + UP * 0.95)
        return group

    def sweep_factor(self, x, sweep_pos, band=0.30):
        if x < sweep_pos - band:
            return 0.0
        elif x < sweep_pos + band:
            return (x - (sweep_pos - band)) / (2.0 * band)
        else:
            return 1.0

    # -- Panel 1: EEG -------------------------------------------------
    def p1_slow_arr(self, xs):
        return 0.62 * np.sin(2 * np.pi * 1.4 * (xs / self.wave_width) + 0.4)

    def p1_noise_arr(self, xs):
        return 0.14 * (
            np.sin(2 * np.pi * 25.0 * (xs / self.wave_width))
            + 0.5 * np.sin(2 * np.pi * 37.0 * (xs / self.wave_width))
        )

    def make_p1_wave(self, center, sweep_pos):
        def combined(xs):
            factor = np.array([self.sweep_factor(x, sweep_pos) for x in xs])
            return self.p1_slow_arr(xs) + factor * self.p1_noise_arr(xs)

        return self.make_wave_mobject(
            combined,
            center,
            color=WHITE,
            stroke_width=4,
        )

    # -- Panel 2: LFP -------------------------------------------------
    def lfp_slow_arr(self, xs):
        return 0.60 * np.sin(2 * np.pi * 1.3 * (xs / self.wave_width) + 0.5)

    def lfp_slow_val(self, x):
        return 0.60 * np.sin(2 * np.pi * 1.3 * (x / self.wave_width) + 0.5)

    def make_lfp_spikes(self, center):
        x_positions = [-1.20, -0.72, -0.24, 0.24, 0.72, 1.20]
        spikes = VGroup()
        for x in x_positions:
            y0 = self.lfp_slow_val(x)
            top = y0 + 0.75
            bottom = y0 - 0.55
            spike = Line(
                start=np.array([center[0] + x, center[1] + bottom, 0]),
                end=np.array([center[0] + x, center[1] + top, 0]),
                color=ORANGE,
                stroke_width=2.5,
            )
            spikes.add(spike)
        return spikes

    # -- Panel 3: EMG ------------------------------------------------
    def p3_raw_arr(self, xs):
        return (
            0.42 * np.sin(2 * np.pi * 10.0 * (xs / self.wave_width))
            + 0.30 * np.sin(2 * np.pi * 17.0 * (xs / self.wave_width))
        )

    def p3_rect_arr(self, xs):
        return np.abs(self.p3_raw_arr(xs))

    def p3_envelope_arr(self, xs):
        return 0.38 + 0.22 * np.sin(
            2 * np.pi * 1.6 * (xs / self.wave_width) + 0.7
        )

    def p3_envelope_val(self, x):
        return 0.38 + 0.22 * np.sin(
            2 * np.pi * 1.6 * (x / self.wave_width) + 0.7
        )

    def make_p3_wave(self, center, rectify_amount, sweep_pos):
        def combined(xs):
            raw = self.p3_raw_arr(xs)
            rectified = (1.0 - rectify_amount) * raw + rectify_amount * np.abs(raw)
            factor = np.array([
                self.sweep_factor(x, sweep_pos) for x in xs
            ])
            envelope = self.p3_envelope_arr(xs)
            return envelope + factor * (rectified - envelope)

        return self.make_wave_mobject(
            combined,
            center,
            color=PINK,
            stroke_width=4,
        )