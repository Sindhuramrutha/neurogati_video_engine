ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        clock = 0.0

        def P(dur, *anims, **kwargs):
            nonlocal clock
            if dur <= 0.001:
                return
            self.play(*anims, run_time=max(0.05, dur), **kwargs)
            clock += dur

        def W(dur):
            nonlocal clock
            if dur <= 0.001:
                return
            self.wait(max(0.05, dur))
            clock += dur

        def wait_until(t):
            nonlocal clock
            gap = t - clock
            if gap > 0.001:
                W(gap)

        # ------------------------------------------------------------
        # waveform helpers
        # ------------------------------------------------------------
        def noise_y(x, seed_val=0):
            y = 0.0
            freqs = [2.3, 3.9, 5.8, 8.2, 11.4]
            amps = [0.42, 0.28, 0.17, 0.10, 0.06]
            for k, (f, a) in enumerate(zip(freqs, amps)):
                phase = (seed_val * 1.71 + k * 2.27) % (2 * np.pi)
                y += a * np.sin(f * x + phase)
                y += 0.06 * np.sin((f + 2.0) * x + 2.0 * phase)
            return 0.62 * y

        def erp_bump_shape(x):
            return np.exp(-((x - 0.35) ** 2) / 0.045) - 0.55 * np.exp(
                -((x - 0.62) ** 2) / 0.055
            )

        def avg_component_y(x):
            return 0.55 * np.exp(-((x - 0.30) ** 2) / 0.07) - 0.38 * np.exp(
                -((x - 0.60) ** 2) / 0.09
            )

        # ------------------------------------------------------------
        # Beat 1: single noisy EEG trace + title
        # ------------------------------------------------------------
        xs = np.linspace(-6.4, 6.4, 160)
        trace = VMobject(color=TEAL, stroke_width=3.0)
        trace.set_points_smoothly(
            np.array([[x, noise_y(x, seed_val=10), 0] for x in xs])
        )

        title = Text("Why do we need averaging?", font_size=42, color=GOLD)
        title.to_edge(UP, buff=0.35)

        P(0.70, Create(trace))
        P(0.32, Write(title))
        wait_until(1.74)

        # ------------------------------------------------------------
        # Beat 2: glow travels, faint wavelets appear
        # ------------------------------------------------------------
        text2 = Text(
            "A single EEG recording contains a mixture of many different neural processes",
            font_size=26,
            color=WHITE,
        )
        text2.scale_to_fit_width(12)
        text2.move_to([0, -2.8, 0])

        glow_dot = VGroup(
            Circle(radius=0.22, color=GOLD, fill_opacity=0.30, stroke_width=0),
            Circle(radius=0.10, color=YELLOW, fill_opacity=0.90, stroke_width=0),
        )
        glow_dot.move_to(trace.get_start())

        wavelet_group = VGroup()
        wavelet_colors = [PINK, ORANGE, PURPLE]
        for i, col in enumerate(wavelet_colors):
            w = VMobject(
                color=col,
                stroke_width=1.4,
                stroke_opacity=0.30,
                fill_opacity=0,
            )
            w.set_points_smoothly(
                np.array(
                    [[x, 0.20 * noise_y(x, seed_val=100 + i), 0] for x in np.linspace(-6.2, 6.2, 120)]
                )
            )
            wavelet_group.add(w)

        P(0.70, FadeIn(text2), FadeIn(glow_dot))
        P(2.30, MoveAlongPath(glow_dot, trace), rate_func=linear)
        P(0.55, FadeOut(glow_dot), FadeIn(wavelet_group))
        W(0.29)
        wait_until(6.42)

        # ------------------------------------------------------------
        # Beat 3: ticking clock + continuous activity text
        # ------------------------------------------------------------
        P(0.50, FadeOut(text2), FadeOut(wavelet_group))

        clock_center = np.array([5.2, 1.4, 0])
        clock_face = Circle(
            radius=0.48,
            color=WHITE,
            fill_color=BLUE,
            fill_opacity=0.9,
            stroke_width=3,
        ).move_to(clock_center)

        clock_ticks = VGroup()
        for k in range(12):
            ang = k * 2 * np.pi / 12
            start = clock_center + 0.34 * np.array([np.cos(ang), np.sin(ang), 0])
            end = clock_center + 0.45 * np.array([np.cos(ang), np.sin(ang), 0])
            clock_ticks.add(Line(start, end, color=WHITE, stroke_width=2))

        clock_hand = Line(
            clock_center,
            clock_center + np.array([0, 0.30, 0]),
            color=YELLOW,
            stroke_width=4,
        )
        clock_hand.add_updater(
            lambda mob, dt: mob.rotate(dt * 2.2, about_point=clock_center)
        )
        clock_icon = VGroup(clock_face, clock_ticks, clock_hand)

        text3 = Text(
            "The brain is continuously active, even when no experimental task is being performed",
            font_size=26,
            color=WHITE,
        )
        text3.scale_to_fit_width(12)
        text3.move_to([0, -2.8, 0])

        P(0.80, FadeIn(clock_icon), FadeIn(text3))
        W(3.40)
        wait_until(12.10)

        # ------------------------------------------------------------
        # Beat 4: stimulus marker + tiny event-related bump
        # ------------------------------------------------------------
        P(0.50, FadeOut(text3), FadeOut(clock_icon))
        clock_hand.clear_updaters()

        marker = DashedLine(
            start=np.array([0, -1.8, 0]),
            end=np.array([0, 1.8, 0]),
            color=YELLOW,
            stroke_width=3,
            dash_length=0.15,
        )

        stim_label = Text("stimulus onset", font_size=22, color=YELLOW)
        stim_label.move_to([0, 1.95, 0])

        bump_wave = VMobject(color=TEAL, stroke_width=3.5)
        bump_wave.set_points_smoothly(
            np.array(
                [
                    [x, noise_y(x, seed_val=10) + 0.13 * erp_bump_shape(x), 0]
                    for x in np.linspace(0.05, 1.25, 90)
                ]
            )
        )

        text4 = Text(
            "The response to a single stimulus is often very small compared with the ongoing background EEG",
            font_size=26,
            color=WHITE,
        )
        text4.scale_to_fit_width(12)
        text4.move_to([0, -2.8, 0])

        P(0.70, Create(marker), FadeIn(stim_label))
        P(1.30, Create(bump_wave))
        P(1.00, FadeIn(text4))
        W(2.74)
        wait_until(19.12)

        # ------------------------------------------------------------
        # Beat 5: slight zoom + circled tiny bump
        # ------------------------------------------------------------
        x_bump = 0.35
        y_bump = noise_y(x_bump, seed_val=10) + 0.13 * erp_bump_shape(x_bump)
        bump_circle = Circle(radius=0.42, color=YELLOW, stroke_width=3)
        bump_circle.move_to([x_bump, y_bump, 0])

        text5 = Text(
            "If we examine only one trial, the event-related response may be difficult to distinguish from the surrounding neural activity",
            font_size=24,
            color=WHITE,
        )
        text5.scale_to_fit_width(12)
        text5.move_to([0, -3.0, 0])

        P(
            1.00,
            self.camera.frame.animate.scale(0.82).move_to([0.35, 0, 0]),
            FadeOut(text4),
            FadeOut(stim_label),
        )
        P(0.80, Create(bump_circle))
        P(0.90, FadeIn(text5))
        W(4.10)
        wait_until(26.82)

        # ------------------------------------------------------------
        # Beat 6: fade trace out, repeated stimulus markers
        # ------------------------------------------------------------
        P(
            0.90,
            self.camera.frame.animate.scale(1 / 0.82).move_to([0, 0, 0]),
            FadeOut(trace),
            FadeOut(marker),
            FadeOut(bump_wave),
            FadeOut(bump_circle),
            FadeOut(text5),
            FadeOut(title),
        )

        marker_positions = [-4, -2, 0, 2, 4]
        marker_row = VGroup()
        for mx in marker_positions:
            marker_row.add(
                DashedLine(
                    start=np.array([mx, -0.4, 0]),
                    end=np.array([mx, 0.4, 0]),
                    color=YELLOW,
                    stroke_width=5,
                    dash_length=0.12,
                )
            )

        text6 = Text(
            "To improve the visibility of the response, the same stimulus is presented repeatedly",
            font_size=26,
            color=WHITE,
        )
        text6.scale_to_fit_width(12)
        text6.move_to([0, 3.0, 0])

        P(1.10, FadeIn(marker_row), FadeIn(text6))
        W(2.34)
        wait_until(32.10)

        # ------------------------------------------------------------
        # Beat 7: stacked epochs aligned to central stimulus line
        # ------------------------------------------------------------
        central_tall = DashedLine(
            start=np.array([0, -2.8, 0]),
            end=np.array([0, 2.8, 0]),
            color=YELLOW,
            stroke_width=3,
            dash_length=0.15,
        )

        P(0.60, FadeOut(text6), FadeOut(marker_row), FadeIn(central_tall))

        epoch_traces = VGroup()
        xs_epoch = np.linspace(-4.6, 4.6, 140)
        epoch_y_positions = [-1.8, -0.9, 0.0, 0.9, 1.8]
        for i, yb in enumerate(epoch_y_positions):
            ep = VMobject(color=TEAL, stroke_width=2.2)
            ep.set_points_smoothly(
                np.array(
                    [
                        [x, yb + noise_y(x, seed_val=30 + i) + 0.14 * erp_bump_shape(x), 0]
                        for x in xs_epoch
                    ]
                )
            )
            epoch_traces.add(ep)

        text7 = Text(
            "For each presentation, a short EEG segment is extracted around the event",
            font_size=24,
            color=WHITE,
        )
        text7.scale_to_fit_width(12)
        text7.move_to([0, -3.0, 0])

        P(1.50, FadeIn(epoch_traces))
        P(0.80, FadeIn(text7))
        W(1.28)
        wait_until(37.00)

        # ------------------------------------------------------------
        # Beat 8: highlight epochs + arrows to average
        # ------------------------------------------------------------
        epoch_rect = SurroundingRectangle(
            epoch_traces,
            color=YELLOW,
            buff=0.10,
            stroke_width=3,
        )

        target_dot = Dot([0, -2.95, 0], radius=0.10, color=GOLD)
        arrows_group = VGroup()
        for ep in epoch_traces:
            start = np.array([4.3, ep.get_center()[1], 0])
            arrow = Arrow(
                start=start,
                end=target_dot.get_center(),
                buff=0.1,
                color=WHITE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.08,
            )
            arrows_group.add(arrow)

        text8 = Text(
            "These segments are then averaged together",
            font_size=26,
            color=WHITE,
        )
        text8.scale_to_fit_width(12)
        text8.move_to([0, -3.45, 0])

        P(
            0.68,
            FadeIn(epoch_rect),
            epoch_traces.animate.set_stroke(color=YELLOW, width=4),
            FadeOut(text7),
        )
        P(0.60, FadeIn(target_dot), Create(arrows_group))
        P(0.30, FadeIn(text8))
        W(0.10)
        wait_until(39.24)

        # ------------------------------------------------------------
        # Beat 9: collapse epochs to smooth average waveform
        # ------------------------------------------------------------
        avg_y_base = -1.35
        xs_avg = np.linspace(-2.2, 2.2, 140)
        avg_wave = VMobject(color=YELLOW, stroke_width=4.0)
        avg_wave.set_points_smoothly(
            np.array(
                [
                    [x, avg_y_base + 0.75 * avg_component_y(x), 0]
                    for x in xs_avg
                ]
            )
        )

        P(
            1.10,
            *[ep.animate.move_to([0, avg_y_base, 0]) for ep in epoch_traces],
            FadeOut(epoch_rect),
        )
        P(
            0.90,
            FadeOut(epoch_traces),
            FadeOut(target_dot),
            FadeOut(arrows_group),
            FadeOut(text8),
        )
        P(1.10, Create(avg_wave))

        text9 = Text(
            "Because the event-related response occurs at approximately the same time in every trial, it is reinforced during averaging",
            font_size=24,
            color=WHITE,
        )
        text9.scale_to_fit_width(12)
        text9.move_to([0, -3.1, 0])

        P(0.90, FadeIn(text9))
        W(2.44)
        wait_until(46.68)

        # ------------------------------------------------------------
        # Beat 10: ghosted individual traces flicker, cancel out
        # ------------------------------------------------------------
        text10 = Text(
            "Much of the unrelated background EEG varies randomly from trial to trial and therefore tends to cancel out",
            font_size=24,
            color=WHITE,
        )
        text10.scale_to_fit_width(12)
        text10.move_to([0, 3.2, 0])

        ghost_traces = VGroup()
        xs_ghost = np.linspace(-4.0, 4.0, 100)
        ghost_y_positions = [-1.4, -0.7, 0.0, 0.7, 1.4]
        for gi, yg in enumerate(ghost_y_positions):
            ghost = VMobject(
                color=GREY_B,
                stroke_width=2.0,
                stroke_opacity=0.35,
                fill_opacity=0,
            )
            ghost.set_points_smoothly(
                np.array(
                    [
                        [x, yg + noise_y(x, seed_val=50 + gi) + 0.10 * erp_bump_shape(x), 0]
                        for x in xs_ghost
                    ]
                )
            )
            ghost_traces.add(ghost)

        P(0.90, FadeIn(ghost_traces), FadeIn(text10))
        P(7.00, ghost_traces.animate.shift(UP * 0.06), rate_func=wiggle)
        wait_until(54.58)

        # ------------------------------------------------------------
        # Beat 11: clean average + final clear representation
        # ------------------------------------------------------------
        P(1.00, FadeOut(ghost_traces), FadeOut(text10), FadeOut(text9))

        text11 = Text(
            "The result is a much clearer representation of the brain's response to the stimulus",
            font_size=30,
            color=YELLOW,
        )
        text11.scale_to_fit_width(12)
        text11.move_to([0, -3.1, 0])

        P(0.80, FadeIn(text11))
        P(0.40, avg_wave.animate.set_stroke(width=6, color=GOLD))
        P(0.40, avg_wave.animate.set_stroke(width=4, color=YELLOW))
        W(3.44)
        wait_until(60.62)