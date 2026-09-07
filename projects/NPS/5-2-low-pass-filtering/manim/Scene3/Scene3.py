ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----- Helper: small continuity visual from previous scene -----
        prev_visual = self.make_prev_visual()
        self.add(prev_visual)

        # ----- Axes / plot construction -----
        ax = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 1.4, 0.2],
            x_length=10,
            y_length=3.2,
            axis_config={
                "include_numbers": False,
                "stroke_color": WHITE,
                "stroke_width": 2.5,
                "tip_width": 0.18,
                "tip_height": 0.18,
            },
            tips=False,
        )
        ax.move_to(ORIGIN + DOWN * 0.2)
        self.ax = ax

        # X tick labels
        x_tick_vals = [0, 20, 40, 60, 80, 100]
        x_tick_labels = VGroup()
        for f in x_tick_vals:
            t = Text(str(f), font_size=17, color=GREY_B)
            t.move_to(ax.c2p(f, 0) + DOWN * 0.32)
            x_tick_labels.add(t)

        # Y tick labels
        y_tick_vals = [0, 0.5, 1.0, 1.4]
        y_tick_labels = VGroup()
        for g in y_tick_vals:
            if abs(g - 1.0) < 0.01:
                s = "1"
            elif abs(g - 1.4) < 0.01:
                s = "1.4"
            elif abs(g - 0.5) < 0.01:
                s = "0.5"
            else:
                s = "0"
            t = Text(s, font_size=16, color=GREY_B)
            t.move_to(ax.c2p(0, g) + LEFT * 0.38)
            y_tick_labels.add(t)

        x_axis_label = Text("Frequency (Hz)", font_size=24, color=WHITE)
        x_axis_label.next_to(ax.x_axis, DOWN, buff=0.95)

        y_axis_label = Text("Gain (Amplitude)", font_size=20, color=WHITE).rotate(PI / 2)
        y_axis_label.next_to(ax.y_axis, LEFT, buff=0.65)

        plot_group = VGroup(ax, x_tick_labels, y_tick_labels, x_axis_label, y_axis_label)

        flat_curve = ax.plot(
            lambda f: 1.0,
            x_range=[0, 40],
            color=BLUE,
            stroke_width=7,
        )
        roll_curve = ax.plot(
            lambda f: self.gain_func(f),
            x_range=[40, 100],
            color=BLUE,
            stroke_width=7,
        )

        # ----- Beat 1: 0.00 - 2.70 -----
        self.play(
            FadeOut(prev_visual),
            FadeIn(plot_group),
            Create(flat_curve),
            run_time=max(0.05, 2.70),
        )

        # ----- gap 2.70 - 5.60 -----
        self.play(flat_curve.animate.set_stroke(width=8), run_time=max(0.05, 0.80))
        self.play(flat_curve.animate.set_stroke(width=7), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 1.30))

        # ----- Beat 2: 5.60 - 9.52 -----
        cutoff_dot = Dot(ax.c2p(40, 0), radius=0.08, color=YELLOW)
        vline = DashedLine(
            ax.c2p(40, 0),
            ax.c2p(40, 1.05),
            color=YELLOW,
            stroke_width=3,
            dash_length=0.12,
        )
        cutoff_label = Text("Cutoff Frequency", font_size=28, color=YELLOW)
        cutoff_label.move_to(cutoff_dot.get_center() + DOWN * 0.62)

        self.play(
            FadeIn(cutoff_dot),
            FadeIn(vline),
            FadeIn(cutoff_label),
            run_time=max(0.05, 3.92),
        )

        # ----- gap 9.52 - 10.54 -----
        self.play(vline.animate.set_stroke(width=4), run_time=max(0.05, 0.35))
        self.play(vline.animate.set_stroke(width=3), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.32))

        # ----- Beat 3: 10.54 - 15.96 -----
        roll_tracker = ValueTracker(40)
        roll_dot = always_redraw(
            lambda: Dot(
                ax.c2p(roll_tracker.get_value(), self.gain_func(roll_tracker.get_value())),
                radius=0.07,
                color=YELLOW,
            )
        )

        self.play(
            Create(roll_curve),
            vline.animate.set_stroke(width=5, color=WHITE),
            run_time=max(0.05, 2.50),
        )
        self.add(roll_dot)
        self.play(roll_tracker.animate.set_value(100), run_time=max(0.05, 2.92))

        # ----- gap 15.96 - 16.64 -----
        self.wait(max(0.05, 0.68))

        # ----- Beat 4: 16.64 - 20.74 -----
        freq_label_40 = Text("40 Hz", font_size=28, color=YELLOW)
        freq_label_40.move_to(cutoff_label.get_center())

        arrow_40 = Arrow(
            start=freq_label_40.get_top() + UP * 0.08,
            end=cutoff_dot.get_center() + DOWN * 0.20,
            color=YELLOW,
            stroke_width=3,
            buff=0.10,
        )

        cutoff_full_label = Text("Cutoff Frequency (40 Hz)", font_size=26, color=YELLOW)
        cutoff_full_label.move_to(ax.c2p(44, 1.06))

        self.play(
            ReplacementTransform(cutoff_label, freq_label_40),
            FadeIn(arrow_40),
            FadeIn(cutoff_full_label),
            run_time=max(0.05, 4.10),
        )

        # ----- gap 20.74 - 20.98 -----
        self.wait(max(0.05, 0.24))

        # ----- Beat 5: 20.98 - 26.48 -----
        passband_shade = Polygon(
            ax.c2p(0, 0),
            ax.c2p(40, 0),
            ax.c2p(40, 1.0),
            ax.c2p(0, 1.0),
            fill_color=GREEN,
            fill_opacity=0.0,
            stroke_width=0,
        )
        self.add(passband_shade)
        self.bring_to_back(passband_shade)

        passband_label = Text("Passband", font_size=30, color=GREEN)
        passband_label.move_to(ax.c2p(20, 1.22))

        self.play(
            passband_shade.animate.set_fill(opacity=0.15),
            FadeIn(passband_label),
            run_time=max(0.05, 5.50),
        )

        # ----- gap 26.48 - 27.22 -----
        self.play(FadeOut(roll_dot), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.44))

        # ----- Beat 6: 27.22 - 34.52 -----
        atten_tracker = ValueTracker(40)
        atten_dot = always_redraw(
            lambda: Dot(
                ax.c2p(atten_tracker.get_value(), self.gain_func(atten_tracker.get_value())),
                radius=0.07,
                color=ORANGE,
            )
        )

        atten_shade_tracker = ValueTracker(40)
        atten_shade = always_redraw(
            lambda: self.make_atten_shade(atten_shade_tracker.get_value())
        )
        self.add(atten_shade)
        self.bring_to_back(atten_shade)

        atten_label = Text("Attenuation Region", font_size=26, color=ORANGE)
        atten_label.move_to(ax.c2p(67, 0.95))

        self.add(atten_dot)
        self.play(
            atten_tracker.animate.set_value(100),
            atten_shade_tracker.animate.set_value(70),
            FadeIn(atten_label),
            run_time=max(0.05, 7.30),
        )

        # ----- gap 34.52 - 35.44 -----
        self.play(FadeOut(atten_dot), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.52))

        # ----- Beat 7: 35.44 - 40.78 -----
        self.camera.frame.save_state()

        bend_tracker = ValueTracker(30)
        bend_dot = always_redraw(
            lambda: Dot(
                ax.c2p(bend_tracker.get_value(), self.gain_func(bend_tracker.get_value())),
                radius=0.11,
                color=YELLOW,
            )
        )
        not_abrupt_text = Text("not an abrupt boundary", font_size=30, color=YELLOW)
        not_abrupt_text.move_to(ax.c2p(58, 1.15))

        self.add(bend_dot)
        self.play(
            self.camera.frame.animate.scale(0.55).move_to(ax.c2p(40, 0.8)),
            FadeIn(not_abrupt_text),
            run_time=max(0.05, 2.00),
        )
        self.play(bend_tracker.animate.set_value(55), run_time=max(0.05, 3.34))

        # ----- gap 40.78 - 41.96 -----
        self.play(
            FadeOut(bend_dot),
            FadeOut(not_abrupt_text),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.68))

        # ----- Beat 8: 41.96 - 46.02 -----
        self.play(
            Restore(self.camera.frame),
            atten_shade_tracker.animate.set_value(100),
            run_time=max(0.05, 3.00),
        )
        self.wait(max(0.05, 1.06))

    # -------------------------------------------------------------------
    def make_prev_visual(self):
        gate = VGroup(
            Line(LEFT * 0.7 + DOWN * 0.2, RIGHT * 0.5 + DOWN * 0.2, color=GREY_B, stroke_width=5),
            Line(DOWN * 0.9, UP * 0.4, color=GREY_B, stroke_width=5),
            Dot(UP * 0.4, radius=0.06, color=YELLOW),
            Line(UP * 0.4, RIGHT * 0.6 + UP * 0.6, color=RED, stroke_width=4),
        ).move_to(LEFT * 3.5 + UP * 0.9)

        low_wave = self.make_static_wave(
            amplitude=0.25,
            wave_number=1.5,
            y_center=-0.2,
            color=TEAL,
        ).move_to(RIGHT * 2.5 + UP * 1.0)

        high_wave = self.make_static_wave(
            amplitude=0.18,
            wave_number=4.0,
            y_center=0.1,
            color=ORANGE,
        ).move_to(RIGHT * 2.5 + UP * 0.8)

        return VGroup(gate, low_wave, high_wave).set_opacity(0.60)

    def make_static_wave(self, amplitude, wave_number, y_center, color):
        xs = np.linspace(-1.0, 1.0, 120)
        ys = y_center + amplitude * np.sin(wave_number * xs)
        zs = np.zeros_like(xs)
        wave = VMobject(
            stroke_color=color,
            stroke_width=4,
            fill_opacity=0,
        )
        wave.set_points_as_corners(np.column_stack([xs, ys, zs]))
        return wave

    # -------------------------------------------------------------------
    def gain_func(self, f):
        if f <= 40:
            return 1.0
        d = (f - 40) / 16.0
        return 1.0 / np.sqrt(1.0 + d * d)

    def make_atten_shade(self, max_freq):
        fs = np.linspace(40, max_freq, max(2, int((max_freq - 40) * 2)))
        pts_top = [self.ax.c2p(f, self.gain_func(f)) for f in fs]
        pts_bot = [self.ax.c2p(f, 0) for f in fs[::-1]]
        pts = pts_top + pts_bot
        return Polygon(
            *pts,
            fill_color=ORANGE,
            fill_opacity=0.16,
            stroke_width=0,
        )