ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene13(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helper
        # ------------------------------------------------------------
        def rot_vec(vec, angle):
            x, y = vec[0], vec[1]
            return np.array([
                x * np.cos(angle) - y * np.sin(angle),
                x * np.sin(angle) + y * np.cos(angle),
                0.0,
            ])

        # ------------------------------------------------------------
        # Title and three empty card slots
        # ------------------------------------------------------------
        title = Text("Short-Time Fourier Transform", font_size=42, color=YELLOW, weight=BOLD)
        title.scale_to_fit_width(11)
        title.to_edge(UP, buff=0.35)

        card_w, card_h = 3.8, 2.7
        card1 = Rectangle(
            width=card_w, height=card_h,
            stroke_color=GREY_B, stroke_width=2.5,
            fill_color=GREY_B, fill_opacity=0.06,
        )
        card2 = card1.copy()
        card3 = card1.copy()
        cards = VGroup(card1, card2, card3).arrange(RIGHT, buff=0.8).move_to(np.array([0, 0.55, 0]))
        card1, card2, card3 = cards

        # ------------------------------------------------------------
        # Card 1: small window over continuous waveform
        # ------------------------------------------------------------
        card1_ax = Axes(
            x_range=[0, 10, 2.5],
            y_range=[-1.1, 1.1, 0.5],
            x_length=3.1,
            y_length=1.5,
            axis_config={"color": GREY_B, "stroke_width": 2},
            x_axis_config={"include_numbers": False, "include_ticks": False},
            y_axis_config={"include_numbers": False, "include_ticks": False},
        ).move_to(card1.get_center() + UP * 0.05)

        def card1_wave_func(x):
            return 0.85 * np.sin(2 * PI * 0.45 * x + 0.7) * np.sin(2 * PI * 0.13 * x + 0.3) + 0.2 * np.sin(2 * PI * 1.1 * x)

        wave_pts = [
            card1_ax.coords_to_point(x, card1_wave_func(x))
            for x in np.linspace(0.3, 9.7, 320)
        ]
        wave = VMobject(stroke_color=TEAL, stroke_width=3)
        wave.set_points_as_corners(wave_pts)

        win_left_x = 3.5
        win_right_x = 5.0
        win_center_x = (win_left_x + win_right_x) / 2
        win_width = card1_ax.c2p(win_right_x, 0)[0] - card1_ax.c2p(win_left_x, 0)[0]
        window = Rectangle(
            width=win_width,
            height=1.5,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.28,
        ).move_to(card1_ax.c2p(win_center_x, 0))
        card1_diagram = VGroup(card1_ax, wave, window)

        label1 = Text("STFT", font_size=28, color=WHITE, weight=BOLD).next_to(card1, DOWN, buff=0.35)

        # ------------------------------------------------------------
        # Card 2: three small frequency spectra
        # ------------------------------------------------------------
        mini_axes = []
        for _ in range(3):
            ax = Axes(
                x_range=[0, 10, 5],
                y_range=[0, 1.2, 0.5],
                x_length=0.9,
                y_length=1.2,
                axis_config={"color": GREY_B, "stroke_width": 2},
                x_axis_config={"include_numbers": False, "include_ticks": False},
                y_axis_config={"include_numbers": False, "include_ticks": False},
            )
            mini_axes.append(ax)
        spectra_axes_group = VGroup(*mini_axes).arrange(RIGHT, buff=0.22).move_to(card2.get_center() + UP * 0.1)

        peak_specs = [
            {"center": 2.6, "height": 0.9, "color": TEAL},
            {"center": 4.8, "height": 1.05, "color": GREEN},
            {"center": 7.0, "height": 0.75, "color": ORANGE},
        ]
        peak_curves = []
        for ax, spec in zip(mini_axes, peak_specs):
            xs = np.linspace(0.5, 9.5, 160)
            ys = spec["height"] * np.exp(-((xs - spec["center"]) ** 2) / (2 * 0.8 ** 2))
            curve = VMobject(stroke_color=spec["color"], stroke_width=4)
            curve.set_points_as_corners([ax.c2p(xs[i], ys[i]) for i in range(len(xs))])
            peak_curves.append(curve)

        label2 = Text(
            "Frequency content over time", font_size=24, color=WHITE
        ).scale_to_fit_width(3.4).next_to(card2, DOWN, buff=0.35)

        time_axis_line = Line(
            start=spectra_axes_group.get_left() + DOWN * 0.55,
            end=spectra_axes_group.get_right() + DOWN * 0.55,
            color=GREY_B,
            stroke_width=2,
            stroke_opacity=0.8,
        )
        time_label = Text("time", font_size=22, color=GREY_B).next_to(time_axis_line, DOWN, buff=0.08)
        arrow_time = Arrow(
            start=spectra_axes_group.get_bottom() + DOWN * 0.1,
            end=time_axis_line.get_top(),
            buff=0.08,
            color=GREY_B,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
            stroke_opacity=0.8,
        )

        # ------------------------------------------------------------
        # Card 3: tilted balance scale with narrow vs wide window icons
        # ------------------------------------------------------------
        apex = card3.get_center() + UP * 0.18
        beam_angle = -0.08
        left_top = apex + rot_vec(LEFT * 1.4, beam_angle)
        right_top = apex + rot_vec(RIGHT * 1.4, beam_angle)
        left_pan_top = left_top + DOWN * 0.55
        right_pan_top = right_top + DOWN * 0.55

        beam_line = Line(left_top, right_top, color=WHITE, stroke_width=5)
        left_string = Line(left_top, left_pan_top, color=WHITE, stroke_width=2)
        right_string = Line(right_top, right_pan_top, color=WHITE, stroke_width=2)

        left_pan = Polygon(
            left_pan_top + LEFT * 0.3,
            left_pan_top + RIGHT * 0.3,
            left_pan_top + DOWN * 0.2,
        ).set_fill(GREY_B, opacity=0.4).set_stroke(WHITE, width=2)

        right_pan = Polygon(
            right_pan_top + LEFT * 0.3,
            right_pan_top + RIGHT * 0.3,
            right_pan_top + DOWN * 0.2,
        ).set_fill(GREY_B, opacity=0.4).set_stroke(WHITE, width=2)

        left_win_icon = Rectangle(
            width=0.35, height=0.45,
            fill_color=TEAL, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(left_pan_top + DOWN * 0.02)

        right_win_icon = Rectangle(
            width=0.85, height=0.45,
            fill_color=ORANGE, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(right_pan_top + DOWN * 0.02)

        fulcrum = Polygon(
            apex,
            apex + LEFT * 0.2 + DOWN * 0.45,
            apex + RIGHT * 0.2 + DOWN * 0.45,
        ).set_fill(GREY_B, opacity=0.8).set_stroke(WHITE, width=2)

        balance_rig = VGroup(
            beam_line, left_string, right_string,
            left_pan, right_pan,
            left_win_icon, right_win_icon,
        )

        time_res_label = Text("Time resolution", font_size=18, color=YELLOW).scale_to_fit_width(1.4)
        freq_res_label = Text("Frequency resolution", font_size=18, color=YELLOW).scale_to_fit_width(1.4)
        time_res_label.next_to(left_win_icon, DOWN, buff=0.25)
        freq_res_label.next_to(right_win_icon, DOWN, buff=0.25)
        time_res_label.set_opacity(0)
        freq_res_label.set_opacity(0)
        balance_rig.add(time_res_label, freq_res_label)

        balance_label = Text(
            "Fixed analysis window", font_size=24, color=WHITE
        ).scale_to_fit_width(3.4).next_to(card3, DOWN, buff=0.35)

        # ------------------------------------------------------------
        # BEAT 1: 0.00 - 1.20 — layout fades in
        # ------------------------------------------------------------
        self.play(FadeIn(title), FadeIn(cards), run_time=max(0.05, 1.2))

        # ------------------------------------------------------------
        # BEAT 2: 1.20 - 3.30 — first card diagram + STFT label
        # ------------------------------------------------------------
        self.play(FadeIn(card1_diagram), run_time=max(0.05, 1.4))
        self.play(FadeIn(label1), run_time=max(0.05, 0.7))

        # gap 3.30 - 4.22
        self.wait(max(0.05, 0.92))

        # ------------------------------------------------------------
        # BEAT 3: 4.22 - 5.32 — second card blank spectra + label
        # ------------------------------------------------------------
        self.play(FadeIn(spectra_axes_group), run_time=max(0.05, 0.6))
        self.play(FadeIn(label2), run_time=max(0.05, 0.5))

        # ------------------------------------------------------------
        # BEAT 4: 5.32 - 9.88 — first card highlight, window pulse,
        # explanatory text
        # ------------------------------------------------------------
        self.play(card1.animate.set_stroke(color=YELLOW, width=5), run_time=max(0.05, 0.6))
        self.play(Indicate(window, scale_factor=1.08, color=YELLOW), run_time=max(0.05, 0.8))

        explain1 = Text(
            "Analyses short segments instead of the entire recording",
            font_size=22, color=WHITE,
        ).scale_to_fit_width(4.2).next_to(label1, DOWN, buff=0.3)

        self.play(FadeIn(explain1), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.16))

        # ------------------------------------------------------------
        # BEAT 5: 9.88 - 13.48 — window slides, rest dimmed
        # ------------------------------------------------------------
        self.play(
            wave.animate.set_stroke(color=GREY_B, width=3),
            window.animate.set_fill(color=YELLOW, opacity=0.25),
            run_time=max(0.05, 0.4),
        )

        window_centers = [4.25, 5.6, 6.95, 8.3]
        for x_center in window_centers:
            self.play(window.animate.move_to(card1_ax.c2p(x_center, 0)), run_time=max(0.05, 0.55))
            self.wait(max(0.05, 0.25))

        # gap 13.48 - 14.28
        self.wait(max(0.05, 0.8))

        # ------------------------------------------------------------
        # BEAT 6: 14.28 - 18.80 — second card highlighted, peaks appear
        # ------------------------------------------------------------
        self.play(card2.animate.set_stroke(color=YELLOW, width=5), run_time=max(0.05, 0.5))

        for curve in peak_curves:
            self.play(FadeIn(curve), run_time=max(0.05, 0.55))
            self.wait(max(0.05, 0.2))

        self.play(
            FadeIn(time_axis_line),
            FadeIn(arrow_time),
            FadeIn(time_label),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.97))

        # gap 18.80 - 19.56
        self.wait(max(0.05, 0.76))

        # ------------------------------------------------------------
        # BEAT 7: 19.56 - 23.72 — third card balance scale fades in
        # ------------------------------------------------------------
        self.play(FadeIn(fulcrum), FadeIn(balance_rig), run_time=max(0.05, 1.4))
        self.play(FadeIn(balance_label), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.26))

        # ------------------------------------------------------------
        # BEAT 8: 23.72 - 25.60 — enlarge, label pans, tilt further/back
        # ------------------------------------------------------------
        self.play(
            balance_rig.animate.scale(1.08, about_point=apex),
            fulcrum.animate.scale(1.08, about_point=apex),
            run_time=max(0.05, 0.3),
        )
        self.play(
            time_res_label.animate.set_opacity(1),
            freq_res_label.animate.set_opacity(1),
            run_time=max(0.05, 0.4),
        )
        self.play(balance_rig.animate.rotate(-0.07, about_point=apex), run_time=max(0.05, 0.6))
        self.play(balance_rig.animate.rotate(0.06, about_point=apex), run_time=max(0.05, 0.48))
        self.wait(max(0.05, 0.10))

        # ------------------------------------------------------------
        # BEAT 9: 25.60 - 28.95 — settle tilted, hold full layout
        # ------------------------------------------------------------
        self.play(balance_rig.animate.rotate(-0.04, about_point=apex), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 2.45))