ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Core layout values
        width_full = 12.4
        center_y_raw = 0.25
        left_width = 4.4
        right_width = 4.4
        left_center = np.array([-4.2, center_y_raw, 0])
        right_center = np.array([4.2, center_y_raw, 0])
        filter_center = np.array([0, center_y_raw, 0])

        # ----- Beat 1: 0.00 - 2.62 -----
        prev_visual = self.make_prev_visual()
        self.add(prev_visual)

        main_wave = self.make_wave(
            width_full,
            lambda x: 1.0,
            color=WHITE,
            stroke_width=5,
        ).move_to(UP * center_y_raw)

        eeg_label = Text("EEG Recording", font_size=36, color=WHITE)
        eeg_label.move_to(DOWN * 2.2)

        self.play(
            FadeOut(prev_visual),
            FadeIn(main_wave),
            Write(eeg_label),
            run_time=max(0.05, 2.62),
        )

        # ----- Beat 2: 2.62 - 4.48 -----
        slow_glow = self.make_smooth_wave(width_full, TEAL, 12).set_opacity(0.25)
        slow_glow.move_to(UP * center_y_raw)

        slow_curve = self.make_smooth_wave(width_full, TEAL, 5).move_to(UP * center_y_raw)
        noise_spikes = self.make_noise_spikes(width_full, main_wave)

        y_center = main_wave.get_center()[1]
        slow_text = Text("Useful Brain Activity", font_size=24, color=TEAL)
        slow_text.move_to(UP * 2.1 + LEFT * 3.9)

        slow_target_x = -2.5
        slow_target_y = self.slow_val(slow_target_x, width_full) + y_center
        slow_arrow = Arrow(
            start=slow_text.get_bottom() + DOWN * 0.05,
            end=np.array([slow_target_x, slow_target_y, 0]),
            color=TEAL,
            stroke_width=3,
            buff=0.08,
        )

        noise_text = Text("High-Frequency Noise", font_size=24, color=ORANGE)
        noise_text.move_to(UP * 2.1 + RIGHT * 3.9)

        noise_target_x = 2.5
        noise_target_y = self.wave_val(noise_target_x, width_full) + y_center
        noise_arrow = Arrow(
            start=noise_text.get_bottom() + DOWN * 0.05,
            end=np.array([noise_target_x, noise_target_y, 0]),
            color=ORANGE,
            stroke_width=3,
            buff=0.08,
        )

        full_callouts = VGroup(slow_text, slow_arrow, noise_text, noise_arrow)

        self.play(
            FadeIn(slow_glow),
            FadeIn(slow_curve),
            FadeIn(noise_spikes),
            FadeIn(full_callouts),
            run_time=max(0.05, 1.86),
        )
        self.bring_to_back(slow_glow)
        self.bring_to_front(noise_spikes)

        # ----- Beat 3: 4.48 - 8.68 -----
        highlight_tracker = ValueTracker(-4.0)
        highlight_dot = always_redraw(
            lambda: Dot(
                self.point_on_wave(highlight_tracker.get_value(), main_wave, width_full),
                radius=0.07,
                color=YELLOW,
            )
        )
        highlight_ring = always_redraw(
            lambda: Circle(
                radius=0.25,
                color=YELLOW,
                stroke_width=2,
                fill_color=YELLOW,
                fill_opacity=0.06,
            ).move_to(self.point_on_wave(highlight_tracker.get_value(), main_wave, width_full))
        )

        self.add(highlight_dot, highlight_ring)
        self.play(highlight_tracker.animate.set_value(2.0), run_time=max(0.05, 4.20))

        # Gap 8.68 - 9.26
        self.remove(highlight_dot, highlight_ring)
        self.wait(max(0.05, 0.58))

        # ----- Beat 4: 9.26 - 11.76 -----
        left_noisy = self.make_wave(
            left_width,
            lambda x: 1.0,
            color=WHITE,
            stroke_width=5,
        ).move_to(left_center)

        filter_block = Rectangle(
            width=2.0,
            height=2.0,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.22,
            stroke_width=4,
        )
        filter_block.move_to(filter_center)

        filter_label = Text("Low-Pass\nFilter", font_size=20, color=WHITE)
        filter_label.move_to(filter_center)
        filter_label.scale_to_fit_width(1.6)

        filter_arrow = Arrow(
            start=np.array([-1.85, center_y_raw, 0]),
            end=np.array([-1.15, center_y_raw, 0]),
            color=YELLOW,
            stroke_width=4,
            buff=0.05,
        )

        self.play(
            FadeOut(full_callouts),
            FadeOut(slow_glow),
            FadeOut(slow_curve),
            FadeOut(noise_spikes),
            FadeOut(eeg_label),
            Transform(main_wave, left_noisy),
            FadeIn(filter_block),
            FadeIn(filter_label),
            Create(filter_arrow),
            run_time=max(0.05, 2.50),
        )

        left_wave = main_wave

        # ----- Beat 5: 11.76 - 16.78 -----
        left_label = Text("Before Filtering", font_size=22, color=WHITE)
        left_label.move_to(np.array([-4.2, -1.45, 0]))

        right_sweep_tracker = ValueTracker(-2.6)
        right_wave = always_redraw(
            lambda: self.make_wave(
                right_width,
                lambda x: self.right_noise_factor(x, right_sweep_tracker.get_value()),
                color=WHITE,
                stroke_width=5,
            ).move_to(right_center)
        )

        right_sweep_band = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=2.6,
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.12,
                stroke_width=0,
            ).move_to(np.array([4.2 + right_sweep_tracker.get_value(), center_y_raw, 0]))
        )

        right_label = Text("After Low-Pass Filtering", font_size=20, color=WHITE)
        right_label.move_to(np.array([4.2, -1.45, 0]))
        right_label.scale_to_fit_width(3.8)

        self.add(right_wave, right_sweep_band)
        self.play(FadeIn(left_label), FadeIn(right_label), run_time=max(0.05, 1.00))
        self.play(right_sweep_tracker.animate.set_value(2.6), run_time=max(0.05, 4.02))

        # Gap 16.78 - 17.64
        self.wait(max(0.05, 0.86))

        # ----- Beat 6: 17.64 - 21.12 -----
        self.remove(right_wave, right_sweep_band)

        right_static = self.make_wave(
            right_width,
            lambda x: 0.0,
            color=WHITE,
            stroke_width=5,
        ).move_to(right_center)
        right_wave = right_static

        self.play(FadeIn(right_wave), run_time=max(0.05, 0.98))

        for _ in range(5):
            self.play(
                left_wave.animate.shift(UP * 0.025),
                rate_func=there_and_back,
                run_time=max(0.05, 0.25),
            )
            self.play(
                left_wave.animate.shift(DOWN * 0.025),
                rate_func=there_and_back,
                run_time=max(0.05, 0.25),
            )

        # Gap 21.12 - 21.96
        self.wait(max(0.05, 0.84))

        # ----- Beat 7: 21.96 - 28.12 -----
        right_glow = self.make_smooth_wave(right_width, TEAL, 10).move_to(right_center).set_opacity(0.28)

        preserve_text = Text("Physiological Signal Preserved", font_size=18, color=GREEN)
        preserve_text.move_to(np.array([5.2, 2.15, 0]))
        preserve_text.scale_to_fit_width(3.0)
        preserve_arrow = Arrow(
            start=preserve_text.get_bottom() + DOWN * 0.05,
            end=np.array([3.5, 0.66, 0]),
            color=GREEN,
            stroke_width=2,
            buff=0.08,
        )

        suppress_text = Text("High-Frequency Components Suppressed", font_size=16, color=ORANGE)
        suppress_text.move_to(np.array([5.2, -2.0, 0]))
        suppress_text.scale_to_fit_width(3.2)
        suppress_arrow = Arrow(
            start=suppress_text.get_top() + UP * 0.05,
            end=np.array([3.5, -0.15, 0]),
            color=ORANGE,
            stroke_width=2,
            buff=0.08,
        )

        annotation_group = VGroup(preserve_text, preserve_arrow, suppress_text, suppress_arrow)

        ghost_noise = self.make_noise_only_wave(right_width, ORANGE, 2).move_to(right_center).set_opacity(0.35)

        self.play(FadeIn(right_glow), FadeIn(annotation_group), run_time=max(0.05, 1.00))
        self.bring_to_back(right_glow)

        self.play(FadeIn(ghost_noise), run_time=max(0.05, 0.80))
        self.play(FadeOut(ghost_noise), run_time=max(0.05, 0.80))
        self.play(
            right_glow.animate.set_stroke(width=14),
            rate_func=there_and_back,
            run_time=max(0.05, 3.56),
        )

        # Gap 28.12 - 29.03
        self.wait(max(0.05, 0.91))

        # ----- Beat 8: 29.03 - 34.36 -----
        warn_triangle = Polygon(
            np.array([-0.4, 0.35, 0]),
            np.array([0.4, 0.35, 0]),
            np.array([0, -0.35, 0]),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
        )
        warn_line = Line(
            np.array([0, 0.15, 0]),
            np.array([0, -0.05, 0]),
            color=BLACK,
            stroke_width=5,
        )
        warn_dot = Dot(np.array([0, -0.2, 0]), radius=0.05, color=BLACK)
        warn_icon = VGroup(warn_triangle, warn_line, warn_dot).scale(0.8)

        warn_text = Text("All frequencies above cutoff are removed", font_size=22, color=YELLOW)
        warn_text.next_to(warn_icon, RIGHT, buff=0.6)

        warning_group = VGroup(warn_icon, warn_text)
        warning_group.move_to(UP * 2.85)

        self.play(SpinInFromNothing(warn_icon), Write(warn_text), run_time=max(0.05, 1.20))
        self.play(
            right_wave.animate.set_opacity(0.55),
            right_glow.animate.set_opacity(0.18),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 3.13))

        # Gap 34.36 - 34.84
        self.wait(max(0.05, 0.48))

        # ----- Beat 9: 34.84 - 39.30 -----
        self.play(
            FadeOut(preserve_text),
            FadeOut(preserve_arrow),
            FadeOut(suppress_text),
            FadeOut(suppress_arrow),
            run_time=max(0.05, 0.80),
        )

        useful_text = Text("Useful high-frequency info also removed", font_size=18, color=ORANGE)
        useful_text.move_to(np.array([5.0, -2.5, 0]))
        useful_text.scale_to_fit_width(3.6)

        useful_arrow = Arrow(
            start=useful_text.get_top() + UP * 0.05,
            end=np.array([3.4, -0.1, 0]),
            color=ORANGE,
            stroke_width=2,
            buff=0.08,
        )

        ghost_useful = self.make_noise_only_wave(right_width, ORANGE, 2).move_to(right_center).set_opacity(0.35)

        self.play(
            FadeIn(useful_text),
            FadeIn(useful_arrow),
            FadeIn(ghost_useful),
            left_wave.animate.shift(UP * 0.025),
            rate_func=there_and_back,
            run_time=max(0.05, 1.00),
        )

        self.play(FadeOut(ghost_useful), run_time=max(0.05, 0.80))
        self.play(
            warn_icon.animate.scale(1.08),
            rate_func=there_and_back,
            run_time=max(0.05, 0.80),
        )

        for _ in range(4):
            self.play(
                left_wave.animate.shift(UP * 0.025),
                rate_func=there_and_back,
                run_time=max(0.05, 0.13),
            )
            self.play(
                left_wave.animate.shift(DOWN * 0.025),
                rate_func=there_and_back,
                run_time=max(0.05, 0.13),
            )
        self.wait(max(0.05, 0.02))

        # Gap 39.30 - 40.08
        self.wait(max(0.05, 0.78))

        # ----- Beat 10: 40.08 - 44.10 -----
        self.play(
            warn_icon.animate.scale(1.06),
            rate_func=there_and_back,
            run_time=max(0.05, 2.00),
        )
        self.play(
            warn_icon.animate.scale(1.04),
            rate_func=there_and_back,
            run_time=max(0.05, 2.00),
        )
        self.wait(max(0.05, 0.02))

    # ------------------------------------------------------------------
    # Helper: previous scene continuity visual
    # ------------------------------------------------------------------
    def make_prev_visual(self):
        ax = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 1.4, 0.2],
            x_length=8,
            y_length=2.8,
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 2.5,
                "include_numbers": False,
            },
            tips=False,
        )
        ax.move_to(ORIGIN + DOWN * 0.3)

        flat = ax.plot(lambda f: 1.0, x_range=[0, 40], color=BLUE, stroke_width=6)
        roll = ax.plot(
            lambda f: self.gain_func(f),
            x_range=[40, 100],
            color=BLUE,
            stroke_width=6,
        )
        cutoff_line = DashedLine(
            ax.c2p(40, 0),
            ax.c2p(40, 1.0),
            color=YELLOW,
            stroke_width=3,
        )
        cutoff_label = Text("Cutoff Frequency (40 Hz)", font_size=20, color=YELLOW)
        cutoff_label.move_to(ax.c2p(53, 1.12))

        pass_shade = Polygon(
            ax.c2p(0, 0),
            ax.c2p(40, 0),
            ax.c2p(40, 1.0),
            ax.c2p(0, 1.0),
            fill_color=GREEN,
            fill_opacity=0.15,
            stroke_width=0,
        )

        return VGroup(ax, flat, roll, cutoff_line, cutoff_label, pass_shade)

    def gain_func(self, f):
        if f <= 40:
            return 1.0
        d = (f - 40) / 16.0
        return 1.0 / np.sqrt(1.0 + d * d)

    # ------------------------------------------------------------------
    # Waveform helpers
    # ------------------------------------------------------------------
    def slow_array(self, xs, width):
        return 0.45 * np.sin(2 * np.pi * 1.25 * (xs / width) + 0.5)

    def noise_array(self, xs, width):
        return 0.16 * (
            np.sin(2 * np.pi * 22.0 * (xs / width))
            + 0.4 * np.sin(2 * np.pi * 39.0 * (xs / width))
        )

    def slow_val(self, x, width):
        return 0.45 * np.sin(2 * np.pi * 1.25 * (x / width) + 0.5)

    def noise_val(self, x, width):
        return 0.16 * (
            np.sin(2 * np.pi * 22.0 * (x / width))
            + 0.4 * np.sin(2 * np.pi * 39.0 * (x / width))
        )

    def wave_val(self, x, width):
        return self.slow_val(x, width) + self.noise_val(x, width)

    def make_wave(self, width, noise_factor_func, color=WHITE, stroke_width=4, num_points=700):
        xs = np.linspace(-width / 2.0, width / 2.0, num_points)
        factors = np.array([noise_factor_func(float(x)) for x in xs])
        ys = self.slow_array(xs, width) + factors * self.noise_array(xs, width)
        wave = VMobject(
            stroke_color=color,
            stroke_width=stroke_width,
            fill_opacity=0,
        )
        wave.set_points_as_corners(np.column_stack([xs, ys, np.zeros_like(xs)]))
        return wave

    def make_smooth_wave(self, width, color=TEAL, stroke_width=4):
        return self.make_wave(
            width,
            lambda x: 0.0,
            color=color,
            stroke_width=stroke_width,
        )

    def make_noise_only_wave(self, width, color=ORANGE, stroke_width=2):
        xs = np.linspace(-width / 2.0, width / 2.0, 600)
        ys = self.noise_array(xs, width)
        vm = VMobject(
            stroke_color=color,
            stroke_width=stroke_width,
            fill_opacity=0,
        )
        vm.set_points_as_corners(np.column_stack([xs, ys, np.zeros_like(xs)]))
        return vm

    def make_noise_spikes(self, width, wave_mobject, num_spikes=100):
        cy = wave_mobject.get_center()[1]
        xs = np.linspace(-width / 2.0 + 0.25, width / 2.0 - 0.25, num_spikes)
        spikes = []
        for x in xs:
            y_slow = self.slow_val(x, width) + cy
            y_full = self.wave_val(x, width) + cy
            spikes.append(
                Line(
                    np.array([x, y_slow, 0]),
                    np.array([x, y_full, 0]),
                    color=ORANGE,
                    stroke_width=2,
                )
            )
        return VGroup(*spikes)

    def point_on_wave(self, x, wave_mobject, width):
        cy = wave_mobject.get_center()[1]
        y = self.wave_val(x, width) + cy
        return np.array([x, y, 0])

    def right_noise_factor(self, x, sweep_pos):
        if x < sweep_pos - 0.35:
            return 0.0
        elif x < sweep_pos + 0.35:
            return (x - (sweep_pos - 0.35)) / 0.70
        else:
            return 1.0