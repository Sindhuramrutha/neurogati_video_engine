ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))

        x_min, x_max = -6.0, 6.0
        num_points = 300
        xs = np.linspace(x_min, x_max, num_points)

        def base_y(t):
            return 0.5*np.sin(2*PI*0.45*xs + 0.8*t) + 0.2*np.sin(2*PI*0.7*xs - 0.6*t)

        def noise1_y(t):
            return 0.18*np.sin(2*PI*8*xs + 20*t) + 0.08*np.sin(2*PI*13*xs - 30*t)

        def noise2_y(t):
            spikes = np.abs(np.sin(2*PI*1.2*xs + 0.7*t))**9 + np.abs(np.sin(2*PI*1.8*xs - 1.0*t))**9
            return 0.4 * spikes

        def noise3_y(t):
            return (0.1*np.sin(2*PI*12*xs + 35*t)
                    + 0.1*np.sin(2*PI*18*xs - 45*t)
                    + 0.05*np.sin(2*PI*27*xs + 60*t))

        def noise4_y(t):
            return 0.45*np.sin(2*PI*0.16*xs + 0.3*t) + 0.25*np.sin(2*PI*0.09*xs - 0.2*t)

        def noise5_y(t):
            return 0.22*np.sin(2*PI*9*xs + 80*t) + 0.1*np.sin(2*PI*5*xs + 120*t)

        def wave1_y(t): return base_y(t) + noise1_y(t)
        def wave2_y(t): return base_y(t) + noise2_y(t)
        def wave3_y(t): return base_y(t) + noise3_y(t)
        def wave4_y(t): return base_y(t) + noise4_y(t)
        def wave5_y(t): return base_y(t) + noise5_y(t)
        def combined_y(t): return base_y(t)+noise1_y(t)+noise2_y(t)+noise3_y(t)+noise4_y(t)+noise5_y(t)

        def make_points(y_func, t=0.0):
            y = y_func(t)
            return np.stack([xs, y, np.zeros_like(xs)], axis=1)

        def make_wave(y_func, color=WHITE, width=3, opacity=1):
            mob = VMobject()
            mob.set_points_as_corners(make_points(y_func, 0))
            mob.set_stroke(color, width=width, opacity=opacity)
            mob.set_fill(opacity=0)
            mob.add_updater(lambda m: m.set_points_as_corners(make_points(y_func, time_tracker.get_value())))
            return mob

        clean_trace = make_wave(base_y, color=GREEN, width=3, opacity=0)
        noise_trace1 = make_wave(wave1_y, color=BLUE, width=2.2, opacity=0)
        noise_trace2 = make_wave(wave2_y, color=ORANGE, width=2.2, opacity=0)
        noise_trace3 = make_wave(wave3_y, color=PURPLE, width=2.2, opacity=0)
        noise_trace4 = make_wave(wave4_y, color=YELLOW, width=2.2, opacity=0)
        noise_trace5 = make_wave(wave5_y, color=TEAL, width=2.2, opacity=0)
        chaotic_trace = make_wave(combined_y, color=WHITE, width=6, opacity=0)
        trace_group = VGroup(clean_trace, noise_trace1, noise_trace2, noise_trace3, noise_trace4, noise_trace5, chaotic_trace)

        phys_label = Text("physiological signal", color=GREEN, font_size=36).next_to(clean_trace, UP, buff=0.8)

        ctx_labels = []
        ctx_texts = ["EEG", "EMG", "ECoG", "microelectrode"]
        for i, s in enumerate(ctx_texts):
            lab = Text(s, color=WHITE, font_size=28)
            lab.scale_to_fit_width(2.2)
            lab.move_to(np.array([-3.6 + i*2.4, 2.8, 0]))
            ctx_labels.append(lab)

        noise_label_defs = [
            ("electrical equipment", BLUE),
            ("movement of subject", ORANGE),
            ("muscle activity", PURPLE),
            ("poor electrode contact", YELLOW),
            ("surrounding environment", TEAL),
        ]
        noise_label_positions = [
            np.array([-4.5, -1.7, 0]),
            np.array([-0.5, -1.7, 0]),
            np.array([3.5, -1.7, 0]),
            np.array([-3.0, -2.45, 0]),
            np.array([3.0, -2.45, 0]),
        ]
        noise_labels = []
        for (s, color), pos in zip(noise_label_defs, noise_label_positions):
            lab = Text(s, color=color, font_size=26)
            lab.scale_to_fit_width(3.6)
            lab.move_to(pos)
            noise_labels.append(lab)

        # Beat 1
        self.add(clean_trace)
        self.play(clean_trace.animate.set_stroke(opacity=1), run_time=max(0.05, 1.5))

        # Beat 2
        self.play(FadeIn(phys_label, shift=UP*0.2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 3.34))

        self.wait(max(0.05, 0.74))  # gap to beat 3

        # Beat 3
        self.play(Indicate(clean_trace, color=GREEN, scale_factor=1.05), run_time=max(0.05, 0.8))
        self.play(clean_trace.animate.set_stroke(opacity=0.45), run_time=max(0.05, 0.4))
        self.play(clean_trace.animate.set_stroke(opacity=1.0), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.54))

        self.wait(max(0.05, 0.66))  # gap to beat 4

        # Beat 4
        self.play(FadeOut(phys_label), run_time=max(0.05, 0.35))
        for lab in ctx_labels:
            self.play(FadeIn(lab, shift=UP*0.2), run_time=max(0.05, 1.10))
        self.wait(max(0.05, 0.35))

        self.wait(max(0.05, 0.66))  # gap to beat 5

        # Beat 5
        contamination_arrows = VGroup(
            Arrow(np.array([-5, 1.6, 0]), np.array([-2.5, 0.4, 0]), color=GREY_B, stroke_opacity=0.35, max_tip_length_to_length_ratio=0.2),
            Arrow(np.array([5, 1.6, 0]), np.array([2.5, 0.4, 0]), color=GREY_B, stroke_opacity=0.35, max_tip_length_to_length_ratio=0.2),
            Arrow(np.array([-1.0, -1.2, 0]), np.array([-0.3, -0.2, 0]), color=GREY_B, stroke_opacity=0.35, max_tip_length_to_length_ratio=0.2),
            Arrow(np.array([1.0, -1.2, 0]), np.array([0.3, -0.2, 0]), color=GREY_B, stroke_opacity=0.35, max_tip_length_to_length_ratio=0.2),
        )
        self.play(clean_trace.animate.set_stroke(width=5), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 2.2))
        self.play(FadeIn(contamination_arrows), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 3.44))

        # gap before beat 6, fade out faint arrows
        self.wait(max(0.05, 0.3))
        self.play(FadeOut(contamination_arrows), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.1))

        # Beat 6
        self.add(noise_trace1)
        self.play(
            noise_trace1.animate.set_stroke(opacity=1),
            FadeIn(noise_labels[0], shift=UP*0.2),
            run_time=max(0.05, 1.8),
        )
        self.wait(max(0.05, 1.38))

        # Beat 7
        self.add(noise_trace2)
        self.play(
            noise_trace2.animate.set_stroke(opacity=1),
            FadeIn(noise_labels[1], shift=UP*0.2),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.74))

        self.wait(max(0.05, 0.42))  # gap to beat 8

        # Beat 8
        self.add(noise_trace3)
        self.play(
            noise_trace3.animate.set_stroke(opacity=1),
            FadeIn(noise_labels[2], shift=UP*0.2),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.28))

        self.wait(max(0.05, 0.62))  # gap to beat 9

        # Beat 9
        self.add(noise_trace4)
        self.play(
            noise_trace4.animate.set_stroke(opacity=1),
            FadeIn(noise_labels[3], shift=UP*0.2),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.46))

        self.wait(max(0.05, 0.50))  # gap to beat 10

        # Beat 10
        self.add(noise_trace5)
        self.play(
            noise_trace5.animate.set_stroke(opacity=1),
            FadeIn(noise_labels[4], shift=UP*0.2),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.60))

        self.wait(max(0.05, 1.00))  # gap to beat 11

        # Beat 11
        self.add(chaotic_trace)
        self.play(
            chaotic_trace.animate.set_stroke(opacity=1),
            clean_trace.animate.set_stroke(opacity=0.35, width=5),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 4.56))

        self.wait(max(0.05, 1.14))  # gap to beat 12

        # Beat 12
        highlight_rect = SurroundingRectangle(trace_group, color=YELLOW, buff=0.3, corner_radius=0.15)
        message = Text("Filtering removes what we don't want.", color=YELLOW, font_size=38)
        message.scale_to_fit_width(11)
        message.move_to(DOWN*3.15)
        self.play(
            FadeIn(message, shift=UP*0.2),
            Create(highlight_rect),
            run_time=max(0.05, 2.9),
        )

        # Beat 13
        self.wait(max(0.05, 1.97))