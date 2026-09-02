ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helper builders ----------
        def make_sine_wave(x_min, x_max, y_center, n_cycles=3, amplitude=0.35, color=WHITE):
            pts = []
            N = 121
            for i in range(N):
                t = i / (N - 1)
                x = x_min + (x_max - x_min) * t
                y = y_center + amplitude * np.sin(2 * PI * n_cycles * t)
                pts.append(np.array([x, y, 0.0]))
            wave = VMobject()
            wave.set_points_as_corners(pts)
            wave.set_stroke(color=color, width=4)
            wave.set_fill(opacity=0)
            return wave

        def make_noisy_wave(x_min, x_max, y_center, color=ORANGE, seed=42):
            rng = np.random.default_rng(seed)
            pts = []
            N = 170
            for i in range(N):
                t = i / (N - 1)
                x = x_min + (x_max - x_min) * t
                freq = 5 + 12 * (0.5 + 0.5 * np.sin(2 * PI * 1.7 * t))
                noise = rng.normal(0, 0.3)
                y = y_center + 0.32 * np.sin(2 * PI * freq * t + noise)
                pts.append(np.array([x, y, 0.0]))
            wave = VMobject()
            wave.set_points_as_corners(pts)
            wave.set_stroke(color=color, width=4)
            wave.set_fill(opacity=0)
            return wave

        def build_balance_visual(center):
            grp = VGroup()
            fulcrum = Polygon(
                center + np.array([-0.22, -0.3, 0]),
                center + np.array([0.22, -0.3, 0]),
                center + np.array([0.0, 0.12, 0]),
                color=GREY,
                fill_color=GREY,
                fill_opacity=1,
                stroke_width=0,
            )
            beam = Line(
                center + np.array([-1.0, 0.04, 0]),
                center + np.array([1.0, 0.04, 0]),
                color=GREY,
                stroke_width=4,
            )
            left_string = Line(
                center + np.array([-0.7, 0.04, 0]),
                center + np.array([-0.7, -0.18, 0]),
                color=ORANGE,
                stroke_width=3,
            )
            right_string = Line(
                center + np.array([0.7, 0.04, 0]),
                center + np.array([0.7, -0.18, 0]),
                color=TEAL,
                stroke_width=3,
            )
            left_pan = Rectangle(width=0.55, height=0.12, fill_color=ORANGE, fill_opacity=1, stroke_width=0)
            left_pan.move_to(center + np.array([-0.7, -0.27, 0]))
            right_pan = Rectangle(width=0.55, height=0.12, fill_color=TEAL, fill_opacity=1, stroke_width=0)
            right_pan.move_to(center + np.array([0.7, -0.27, 0]))
            left_label = Text("time", font_size=16, color=ORANGE).next_to(left_pan, DOWN, buff=0.07)
            right_label = Text("frequency", font_size=14, color=TEAL).next_to(right_pan, DOWN, buff=0.07)
            grp.add(fulcrum, beam, left_string, right_string, left_pan, right_pan, left_label, right_label)
            return grp

        # ---------- Beat 1: 0.00-2.56 ----------
        problem_label = Text("The Problem", font_size=72, color=WHITE)
        problem_label.move_to(ORIGIN)
        self.play(FadeIn(problem_label), run_time=max(0.05, 2.56))

        # ---------- Beat 2: 2.56-4.66 ----------
        timeline_line = Line(LEFT * 4.5, RIGHT * 4.5, color=GREY_B, stroke_width=6)
        timeline_line.move_to(ORIGIN)

        tick_positions = [-4.5, -1.5, 1.5, 4.5]
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i, x in enumerate(tick_positions):
            tick = Line(x * RIGHT + UP * 0.15, x * RIGHT + DOWN * 0.15, color=WHITE, stroke_width=3)
            tick_marks.add(tick)
            label = Text(f"{i * 10} s", font_size=24, color=GREY_B)
            label.move_to(np.array([x, -0.65, 0]))
            tick_labels.add(label)

        marker = Polygon(
            np.array([-4.5 - 0.15, 0.25, 0]),
            np.array([-4.5 + 0.15, 0.25, 0]),
            np.array([-4.5, 0.48, 0]),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
        )

        timeline_group = VGroup(timeline_line, tick_marks, tick_labels, marker)
        self.play(
            problem_label.animate.move_to(UP * 2.5),
            FadeIn(timeline_group),
            run_time=max(0.05, 2.10),
        )

        # ---------- Beat 3: 4.66-5.96 ----------
        thirty_label = Text("30 seconds", font_size=32, color=YELLOW)
        thirty_label.move_to(np.array([0, -1.7, 0]))
        self.play(
            timeline_line.animate.set_color(YELLOW),
            FadeIn(thirty_label),
            run_time=max(0.05, 1.30),
        )

        # ---------- Beat 4: 5.96-8.16 ----------
        region1_rect = Rectangle(
            width=3, height=0.8,
            color=BLUE, fill_color=BLUE, fill_opacity=0.25, stroke_width=0,
        )
        region1_rect.move_to(np.array([-3, 0, 0]))

        alpha_wave = make_sine_wave(-4.6, -1.4, 1.4, n_cycles=3, color=BLUE)
        alpha_wave_label = Text("alpha", font_size=24, color=BLUE).move_to(np.array([-4.4, 1.85, 0]))
        alpha_dom_label = Text("alpha dominant", font_size=22, color=BLUE).move_to(np.array([-3, -1.15, 0]))

        timeline_group.add(region1_rect, alpha_wave, alpha_wave_label, alpha_dom_label)
        self.play(
            FadeIn(region1_rect),
            Create(alpha_wave),
            FadeIn(alpha_wave_label),
            FadeIn(alpha_dom_label),
            run_time=max(0.05, 2.20),
        )

        # ---------- Beat 5: 8.16-9.58 ----------
        self.play(alpha_wave.animate.shift(RIGHT * 0.15), run_time=max(0.05, 0.71))
        self.play(alpha_wave.animate.shift(LEFT * 0.15), run_time=max(0.05, 0.71))

        # ---------- Beat 6: 9.58-11.12 ----------
        region2_rect = Rectangle(
            width=3, height=0.8,
            color=ORANGE, fill_color=ORANGE, fill_opacity=0.25, stroke_width=0,
        )
        region2_rect.move_to(np.array([0, 0, 0]))

        beta_wave = make_sine_wave(-1.6, 1.6, 1.4, n_cycles=5, color=ORANGE)
        beta_wave_label = Text("beta", font_size=24, color=ORANGE).move_to(np.array([-1.4, 1.9, 0]))
        beta_dom_label = Text("beta dominant", font_size=22, color=ORANGE).move_to(np.array([0, -1.15, 0]))

        timeline_group.add(region2_rect, beta_wave, beta_wave_label, beta_dom_label)
        self.play(
            FadeIn(region2_rect),
            Create(beta_wave),
            FadeIn(beta_wave_label),
            FadeIn(beta_dom_label),
            run_time=max(0.05, 1.54),
        )

        # ---------- Beat 7: 11.12-13.54 ----------
        self.play(
            Wiggle(beta_wave, scale_value=0.2),
            alpha_wave.animate.set_opacity(0.35),
            run_time=max(0.05, 2.42),
        )

        # ---------- Beat 8: 13.54-16.14 ----------
        region3_rect = Rectangle(
            width=3, height=0.8,
            color=GREEN, fill_color=GREEN, fill_opacity=0.25, stroke_width=0,
        )
        region3_rect.move_to(np.array([3, 0, 0]))

        gamma_wave = make_sine_wave(1.4, 4.6, 1.4, n_cycles=7, color=GREEN)
        gamma_wave_label = Text("gamma", font_size=24, color=GREEN).move_to(np.array([1.6, 1.9, 0]))
        gamma_dom_label = Text("gamma brief", font_size=22, color=GREEN).move_to(np.array([3, -1.15, 0]))

        timeline_group.add(region3_rect, gamma_wave, gamma_wave_label, gamma_dom_label)
        self.play(
            FadeIn(region3_rect),
            Create(gamma_wave),
            FadeIn(gamma_wave_label),
            FadeIn(gamma_dom_label),
            run_time=max(0.05, 2.60),
        )

        # ---------- Beat 9: 16.14-18.28 ----------
        self.play(Wiggle(gamma_wave, scale_value=0.2), run_time=max(0.05, 0.9))
        self.play(FadeOut(gamma_wave), run_time=max(0.05, 1.24))

        # ---------- Beat 10: 18.28-21.64 ----------
        self.play(
            timeline_group.animate.scale(0.6).move_to(UP * 2.6),
            FadeOut(thirty_label),
            FadeOut(problem_label),
            run_time=max(0.05, 2.0),
        )

        span_brace = Brace(timeline_group, DOWN, color=WHITE)
        span_label = Text("entire 30-second recording", font_size=24, color=WHITE).next_to(span_brace, DOWN, buff=0.1)
        self.play(FadeIn(span_brace), FadeIn(span_label), run_time=max(0.05, 1.36))

        # ---------- Beat 11: 21.64-25.20 ----------
        x_axis = Line(np.array([-3.5, -0.4, 0]), np.array([3.5, -0.4, 0]), color=GREY_B, stroke_width=4)
        y_axis = Line(np.array([-3.5, -1.0, 0]), np.array([-3.5, 1.4, 0]), color=GREY_B, stroke_width=4)

        freq_axis_label = Text("frequency", font_size=20, color=GREY_B).move_to(np.array([0, -1.2, 0]))
        mag_axis_label = Text("magnitude", font_size=20, color=GREY_B).rotate(PI / 2).move_to(np.array([-4.3, 0.4, 0]))

        alpha_peak = Rectangle(
            width=0.6, height=1.8,
            fill_color=BLUE, fill_opacity=0.9, stroke_width=0,
        )
        alpha_peak.move_to(np.array([-2.5, -0.4 + 0.9, 0]))

        beta_peak = Rectangle(
            width=0.6, height=1.5,
            fill_color=ORANGE, fill_opacity=0.9, stroke_width=0,
        )
        beta_peak.move_to(np.array([0, -0.4 + 0.75, 0]))

        gamma_peak = Rectangle(
            width=0.6, height=1.2,
            fill_color=GREEN, fill_opacity=0.9, stroke_width=0,
        )
        gamma_peak.move_to(np.array([2.5, -0.4 + 0.6, 0]))

        alpha_peak_label = Text("alpha", font_size=24, color=BLUE).move_to(np.array([-2.5, -0.9, 0]))
        beta_peak_label = Text("beta", font_size=24, color=ORANGE).move_to(np.array([0, -0.9, 0]))
        gamma_peak_label = Text("gamma", font_size=24, color=GREEN).move_to(np.array([2.5, -0.9, 0]))

        spectrum_title = Text("Single Frequency Spectrum", font_size=28, color=WHITE).move_to(np.array([0, -2.4, 0]))

        spectrum_group = VGroup(
            x_axis, y_axis,
            alpha_peak, beta_peak, gamma_peak,
            alpha_peak_label, beta_peak_label, gamma_peak_label,
            freq_axis_label, mag_axis_label,
            spectrum_title,
        )
        self.play(FadeIn(spectrum_group), run_time=max(0.05, 3.56))

        # ---------- Beat 12: 25.20-27.68 ----------
        connect_arrow = Arrow(
            np.array([0, 1.65, 0]),
            np.array([0, 1.35, 0]),
            color=GREY_B,
            stroke_width=3,
            buff=0,
        ).set_opacity(0.5)
        self.add(connect_arrow)

        pulse_dur = 0.41
        for peak in [alpha_peak, beta_peak, gamma_peak]:
            self.play(peak.animate.scale(1.2), run_time=max(0.05, pulse_dur))
            self.play(peak.animate.scale(1 / 1.2), run_time=max(0.05, pulse_dur))
        self.wait(max(0.05, 2.48 - 6 * pulse_dur))

        # ---------- Beat 13: 27.68-31.62 ----------
        freq_present = Text("frequencies are present", font_size=28, color=WHITE).move_to(np.array([0, -3.0, 0]))
        self.play(
            FadeIn(freq_present),
            alpha_peak.animate.set_fill(BLUE, opacity=1),
            beta_peak.animate.set_fill(ORANGE, opacity=1),
            gamma_peak.animate.set_fill(GREEN, opacity=1),
            run_time=max(0.05, 0.9),
        )
        self.play(Indicate(alpha_peak, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 1.0))
        self.play(Indicate(beta_peak, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 1.0))
        self.play(Indicate(gamma_peak, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.04))

        # ---------- Beat 14: 31.62-34.92 ----------
        clock_center = np.array([0.0, 0.4, 0.0])
        clock_radius = 0.7

        clock_face = Circle(
            radius=clock_radius,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.15,
            stroke_color=WHITE,
            stroke_width=3,
        )
        clock_face.move_to(clock_center)

        clock_ticks = VGroup()
        for k in range(12):
            angle = k * TAU / 12
            start_point = clock_center + clock_radius * 0.8 * np.array([np.cos(angle), np.sin(angle), 0])
            end_point = clock_center + clock_radius * 0.9 * np.array([np.cos(angle), np.sin(angle), 0])
            clock_ticks.add(Line(start_point, end_point, color=WHITE, stroke_width=2))

        minute_hand = Line(
            clock_center,
            clock_center + clock_radius * 0.6 * np.array([0, 1, 0]),
            color=WHITE,
            stroke_width=5,
        )
        hour_hand = Line(
            clock_center,
            clock_center + clock_radius * 0.4 * np.array([1, 0, 0]),
            color=WHITE,
            stroke_width=5,
        )
        clock_group = VGroup(clock_face, clock_ticks, hour_hand, minute_hand)

        qmark = Text("?", font_size=80, color=YELLOW, weight="BOLD").move_to(clock_center + RIGHT * 1.2)

        self.play(
            FadeIn(clock_group),
            FadeIn(qmark),
            FadeOut(freq_present),
            run_time=max(0.05, 0.6),
        )
        self.play(
            Rotate(minute_hand, angle=-3 * TAU, about_point=clock_center),
            Rotate(hour_hand, angle=-PI, about_point=clock_center),
            FadeOut(timeline_group),
            FadeOut(span_brace),
            FadeOut(span_label),
            FadeOut(connect_arrow),
            run_time=max(0.05, 2.7),
        )

        # ---------- Beat 15: 34.92-37.02 ----------
        no_timing_label = Text("No timing information", font_size=36, color=YELLOW).move_to(np.array([0, -3.1, 0]))
        self.play(FadeIn(no_timing_label), run_time=max(0.05, 2.10))

        # ---------- Beat 16: 37.02-40.12 ----------
        limitation_box = SurroundingRectangle(
            VGroup(spectrum_group, clock_group, qmark),
            color=RED,
            buff=0.2,
            stroke_width=6,
        )
        sig_lim_label = Text("significant limitation", font_size=34, color=RED, weight="BOLD")
        sig_lim_label.next_to(limitation_box, UP, buff=0.2)

        shake_group = VGroup(spectrum_group, clock_group, qmark, no_timing_label)

        self.play(
            Create(limitation_box),
            FadeIn(sig_lim_label),
            alpha_peak.animate.set_fill(BLUE, opacity=0.35),
            beta_peak.animate.set_fill(ORANGE, opacity=0.35),
            gamma_peak.animate.set_fill(GREEN, opacity=0.35),
            run_time=max(0.05, 1.6),
        )
        for _ in range(4):
            self.play(shake_group.animate.shift(RIGHT * 0.03), run_time=max(0.05, 0.12))
            self.play(shake_group.animate.shift(LEFT * 0.03), run_time=max(0.05, 0.12))
        self.wait(max(0.05, 0.54))

        limitation_group = VGroup(
            spectrum_group, clock_group, qmark,
            no_timing_label, limitation_box, sig_lim_label,
        )

        # ---------- Beat 17: 40.12-44.32 ----------
        panel_rect = Rectangle(
            width=3.6, height=2.6,
            color=PURPLE, fill_color=PURPLE, fill_opacity=0.30,
            stroke_color=PURPLE, stroke_width=4,
        )
        panel_rect.move_to(np.array([4.6, -2.1, 0]))

        dynamic_wave = make_noisy_wave(3.1, 6.0, -1.8, color=ORANGE)
        dynamic_label = Text("neural activity is dynamic", font_size=22, color=ORANGE)
        dynamic_label.move_to(np.array([4.6, -0.5, 0]))

        dynamic_panel_group = VGroup(panel_rect, dynamic_wave, dynamic_label)
        self.play(
            FadeIn(panel_rect),
            Create(dynamic_wave),
            FadeIn(dynamic_label),
            run_time=max(0.05, 4.20),
        )

        # ---------- Beat 18: 44.32-49.14 ----------
        self.play(dynamic_panel_group.animate.scale(1.1), run_time=max(0.05, 1.2))
        self.play(Wiggle(dynamic_wave, scale_value=0.2), run_time=max(0.05, 1.2))

        freq_label = Text("frequency", font_size=26, color=YELLOW).move_to(np.array([3.3, -0.55, 0]))
        time_label = Text("time", font_size=26, color=YELLOW).move_to(np.array([5.2, -0.55, 0]))
        self.play(FadeIn(freq_label), FadeIn(time_label), run_time=max(0.05, 1.0))

        balance_vis = build_balance_visual(center=np.array([4.6, -3.1, 0]))
        self.play(FadeIn(balance_vis), run_time=max(0.05, 1.42))

        # ---------- Beat 19: 49.14-51.52 ----------
        q1 = Text("which frequencies are present?", font_size=27, color=WHITE)
        q1.move_to(np.array([-2.5, 2.8, 0]))
        q2 = Text("at what time do they occur?", font_size=27, color=WHITE)
        q2.move_to(np.array([-2.5, 2.2, 0]))

        self.play(FadeIn(q1), FadeIn(q2), run_time=max(0.05, 1.0))
        self.play(q1.animate.scale(1.1), q2.animate.scale(1.1), run_time=max(0.05, 0.69))
        self.play(q1.animate.scale(1 / 1.1), q2.animate.scale(1 / 1.1), run_time=max(0.05, 0.69))

        # ---------- Beat 20: 51.52-56.00 ----------
        self.play(
            limitation_group.animate.scale(0.55).move_to(RIGHT * 4.5 + UP * 1.5),
            dynamic_panel_group.animate.scale(0.9).move_to(LEFT * 4.5 + DOWN * 0.5),
            FadeOut(q1),
            FadeOut(q2),
            FadeOut(freq_label),
            FadeOut(time_label),
            FadeOut(balance_vis),
            run_time=max(0.05, 2.6),
        )

        stft_text = Text("Short-Time Fourier Transform", font_size=48, color=WHITE)
        stft_text.move_to(ORIGIN)
        forward_arrow = Arrow(LEFT * 1.2, RIGHT * 1.2, color=YELLOW, stroke_width=6, buff=0)
        forward_arrow.next_to(stft_text, DOWN, buff=0.4)
        self.play(FadeIn(stft_text), FadeIn(forward_arrow), run_time=max(0.05, 1.88))

        # ---------- Beat 21: 56.00-56.70 ----------
        self.wait(max(0.05, 0.70))