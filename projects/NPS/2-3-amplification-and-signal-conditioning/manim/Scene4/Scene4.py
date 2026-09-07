ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # helpers
        # ------------------------------------------------------------------
        def make_signal(noise=True, color=BLUE, stroke_width=4):
            width = 3.8
            n = 190
            xs = np.linspace(-width / 2, width / 2, n)
            base = 1.3 * np.sin(2 * PI * 1.25 * xs / width) + \
                   0.35 * np.sin(2 * PI * 0.5 * xs / width + 1.0)
            if noise:
                rng = np.random.RandomState(42)
                noise_vals = 0.42 * rng.randn(n)
                drift = 0.28 * (xs / width)
                ys = base + noise_vals + drift
            else:
                ys = base
            wave = VMobject()
            wave.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
            wave.set_stroke(color=color, width=stroke_width)
            wave.set_fill(opacity=0)
            return wave

        def make_noise_overlay(color=ORANGE, stroke_width=7):
            width = 3.8
            n = 190
            xs = np.linspace(-width / 2, width / 2, n)
            rng = np.random.RandomState(99)
            ys = 0.5 * rng.randn(n)
            overlay = VMobject()
            overlay.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
            overlay.set_stroke(color=color, width=stroke_width)
            overlay.set_fill(opacity=0)
            return overlay

        def make_dashed_arrow(start, end, color=GREY_B, stroke_width=3):
            body = DashedLine(start, end, dash_length=0.12,
                              color=color, stroke_width=stroke_width)
            direction = (end - start) / np.linalg.norm(end - start)
            perp = np.array([-direction[1], direction[0], 0])
            head = Polygon(
                end,
                end - direction * 0.12 + perp * 0.07,
                end - direction * 0.12 - perp * 0.07,
            )
            head.set_fill(color, opacity=1).set_stroke(color, width=0)
            return VGroup(body, head)

        def make_bullet(text, y):
            dot = Dot(radius=0.07, color=TEAL)
            label = Text(text, font_size=18, color=WHITE)
            group = VGroup(dot, label).arrange(RIGHT, buff=0.15)
            group.move_to(np.array([panel.get_left()[0] + 0.45, y, 0]),
                          aligned_edge=LEFT)
            return group

        # ------------------------------------------------------------------
        # previous-scene holdover: amplifier symbol + callout box
        # ------------------------------------------------------------------
        prev_amp = Polygon(
            [-0.8, 0.55, 0], [-0.8, -0.55, 0], [0.9, 0, 0],
        )
        prev_amp.set_fill(TEAL, opacity=0.6).set_stroke(TEAL, width=3)

        prev_callout = RoundedRectangle(
            width=5.0, height=1.2, corner_radius=0.15,
            stroke_color=YELLOW, fill_color=BLACK, fill_opacity=0.65,
            stroke_width=2,
        )
        prev_text = Text("Amplification: increase signal level",
                         font_size=22, color=WHITE).move_to(prev_callout.get_center())
        prev_group = VGroup(prev_amp, prev_callout, prev_text).arrange(RIGHT, buff=0.5)
        prev_group.move_to(ORIGIN)

        ghost_amp = prev_amp.copy().set_opacity(0.25)
        ghost_amp.move_to(LEFT * 4.8 + UP * 0.2)

        self.add(prev_group, ghost_amp)

        # tall, amplified noisy waveform
        noisy_wave = make_signal(noise=True, color=BLUE)
        noisy_wave.move_to(ORIGIN)

        # ------------------------------------------------------------------
        # 0.00-1.78 : transition into the noisy amplified waveform
        # ------------------------------------------------------------------
        self.play(FadeOut(prev_group), FadeIn(noisy_wave), run_time=max(0.05, 1.2))
        self.play(FadeOut(ghost_amp), run_time=max(0.05, 0.58))

        # ------------------------------------------------------------------
        # 1.78-4.84 : blocked path arrow + red X
        # ------------------------------------------------------------------
        self.play(noisy_wave.animate.scale(1.06, about_point=noisy_wave.get_center()),
                  run_time=max(0.05, 0.5))
        self.play(noisy_wave.animate.scale(1 / 1.06, about_point=noisy_wave.get_center()),
                  run_time=max(0.05, 0.5))

        red_x = VGroup(
            Line(np.array([-0.18, 0.18, 0]), np.array([0.18, -0.18, 0]),
                 color=RED, stroke_width=8),
            Line(np.array([-0.18, -0.18, 0]), np.array([0.18, 0.18, 0]),
                 color=RED, stroke_width=8),
        ).move_to(RIGHT * 4.4)

        blocked_arrow = make_dashed_arrow(
            noisy_wave.get_right() + RIGHT * 0.2,
            red_x.get_left() + LEFT * 0.15,
            color=GREY_B, stroke_width=3,
        )
        blocked_label = Text("cannot be sent directly to computer.",
                             font_size=24, color=RED).next_to(red_x, DOWN, buff=0.3)
        blocked_label.scale_to_fit_width(4.8)

        self.play(Create(blocked_arrow), run_time=max(0.05, 1.0))
        self.play(FadeIn(red_x), FadeIn(blocked_label), run_time=max(0.05, 1.06))

        # ------------------------------------------------------------------
        # 5.68-9.66 : brief gap, then zoom in on noise + baseline drift
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.84))

        noise_overlay = make_noise_overlay().move_to(noisy_wave.get_center())
        interference_label = Text("electrical interference",
                                  font_size=20, color=ORANGE).next_to(noise_overlay, UP, buff=0.2)

        self.play(self.camera.frame.animate.scale(0.8).move_to(noisy_wave.get_center()),
                  run_time=max(0.05, 0.7))
        self.play(FadeIn(noise_overlay), FadeIn(interference_label), run_time=max(0.05, 0.6))
        self.play(noise_overlay.animate.scale(1.08, about_point=noise_overlay.get_center()),
                  run_time=max(0.05, 0.4))
        self.play(noise_overlay.animate.scale(1 / 1.08, about_point=noise_overlay.get_center()),
                  run_time=max(0.05, 0.4))

        baseline_line = DashedLine(
            start=noisy_wave.get_left() + DOWN * 1.25 + RIGHT * 0.1,
            end=noisy_wave.get_right() + DOWN * 1.75 + LEFT * 0.1,
            dash_length=0.1, color=GREY_A, stroke_width=3,
        )
        baseline_label = Text("baseline drift", font_size=20, color=YELLOW)
        baseline_label.next_to(baseline_line, DOWN, buff=0.3)
        baseline_curved_arrow = CurvedArrow(
            start_point=baseline_label.get_top() + UP * 0.1,
            end_point=baseline_line.get_center() + DOWN * 0.2,
            color=YELLOW, stroke_width=3,
        )

        self.play(FadeIn(baseline_line), run_time=max(0.05, 0.5))
        self.play(Create(baseline_curved_arrow), FadeIn(baseline_label), run_time=max(0.05, 0.5))
        self.play(baseline_line.animate.shift(UP * 0.2), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.38))

        # ------------------------------------------------------------------
        # 10.30-12.68 : artifacts, degraded-quality red tint
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.64))

        artifact_dots = VGroup(*[
            Dot(noisy_wave.get_center() + np.array([x, y, 0]), radius=0.035, color=GREY_A)
            for x, y in [(-1.1, 0.9), (0.2, -1.0), (1.2, 0.6), (-0.3, 1.1)]
        ])

        red_tint = noisy_wave.copy().set_stroke(RED, width=8).set_opacity(0.2)
        red_tint.scale(1.05, about_point=noisy_wave.get_center())
        degraded_label = Text("reduced recording quality",
                              font_size=20, color=RED).next_to(noisy_wave, DOWN, buff=0.5)

        self.play(FadeIn(artifact_dots), run_time=max(0.05, 0.35))
        self.play(FadeOut(artifact_dots), run_time=max(0.05, 0.35))
        self.play(noisy_wave.animate.set_opacity(0.55),
                  FadeIn(red_tint), FadeIn(degraded_label), run_time=max(0.05, 0.65))
        self.wait(max(0.05, 0.39))

        # ------------------------------------------------------------------
        # 13.52-18.64 : zoom out, place block to the right, arrow from wave
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.84))

        beat34_extra_group = VGroup(
            noise_overlay, interference_label, baseline_line,
            baseline_curved_arrow, baseline_label, red_tint, degraded_label,
        )

        sc_block = Rectangle(
            width=2.8, height=2.2,
            color=TEAL, fill_color=TEAL, fill_opacity=0.15, stroke_width=3,
        ).move_to(RIGHT * 3.0)
        sc_title = Text("Signal Conditioning", font_size=20,
                        color=TEAL, weight="BOLD").move_to(sc_block.get_center())
        sc_label = Text("Signal Conditioning", font_size=24,
                        color=YELLOW).next_to(sc_block, DOWN, buff=0.25)

        self.play(
            self.camera.frame.animate.scale(1 / 0.8).move_to(ORIGIN),
            noisy_wave.animate.set_opacity(1).move_to(LEFT * 3.2),
            FadeOut(beat34_extra_group),
            run_time=max(0.05, 0.9),
        )
        self.play(FadeIn(sc_block), FadeIn(sc_title), run_time=max(0.05, 0.6))

        sc_arrow = Arrow(
            noisy_wave.get_right() + RIGHT * 0.2,
            sc_block.get_left() + LEFT * 0.1,
            color=TEAL, buff=0.05, stroke_width=3,
        )
        self.play(Create(sc_arrow), run_time=max(0.05, 0.5))
        self.play(FadeIn(sc_label), run_time=max(0.05, 0.4))
        self.play(Indicate(sc_label, color=YELLOW, scale_factor=1.06), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.22))

        # ------------------------------------------------------------------
        # 19.64-26.48 : wave passes through conditioning block and exits clean
        # ------------------------------------------------------------------
        self.wait(max(0.05, 1.0))

        noisy_ref = noisy_wave.copy()
        noisy_ref.set_opacity(0)

        self.play(FadeOut(sc_arrow), run_time=max(0.05, 0.35))
        self.play(noisy_wave.animate.move_to(sc_block.get_center()), run_time=max(0.05, 1.3))

        clean_wave = make_signal(noise=False, color=GREEN)
        clean_wave.scale_to_fit_width(2.4).move_to(sc_block.get_center())

        self.play(ReplacementTransform(noisy_wave, clean_wave), run_time=max(0.05, 1.1))
        self.play(clean_wave.animate.move_to(RIGHT * 5.4), run_time=max(0.05, 1.0))

        accurate_label = Text("accurate digital conversion",
                              font_size=22, color=GREEN).next_to(clean_wave, DOWN, buff=0.35)
        self.play(FadeIn(accurate_label), run_time=max(0.05, 0.6))
        self.play(Indicate(clean_wave, color=GREEN, scale_factor=1.04), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.99))

        # ------------------------------------------------------------------
        # 27.42-31.00 : empty panel below the block
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.94))
        self.play(FadeOut(sc_label), run_time=max(0.05, 0.2))

        panel = RoundedRectangle(
            width=4.6, height=2.0, corner_radius=0.2,
            fill_color=WHITE, fill_opacity=0.12,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(np.array([3.0, -2.15, 0]))
        self.play(FadeIn(panel), run_time=max(0.05, 0.8))
        self.play(Indicate(panel, color=WHITE, scale_factor=1.02), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.28))

        # ------------------------------------------------------------------
        # 31.00-32.60 : first bullet - Initial filtering
        # ------------------------------------------------------------------
        bullet_list = VGroup()
        bullet_y = panel.get_top()[1] - 0.45

        b1 = make_bullet("Initial filtering", bullet_y)
        bullet_y -= 0.34
        bullet_list.add(b1)

        self.play(FadeIn(b1), run_time=max(0.05, 0.6))
        self.play(Indicate(b1[1], color=YELLOW, scale_factor=1.05), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.5))

        # ------------------------------------------------------------------
        # 32.84-33.56 : second bullet + noisy flicker + clean pulse
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.24))

        b2 = make_bullet("Noise reduction", bullet_y)
        bullet_y -= 0.34
        bullet_list.add(b2)

        noisy_ref.scale_to_fit_width(1.2)
        noisy_ref.move_to(panel.get_left() + LEFT * 1.2 + UP * 0.35)

        self.play(FadeIn(b2), run_time=max(0.05, 0.28))
        self.add(noisy_ref)
        self.play(noisy_ref.animate.set_opacity(1), run_time=max(0.05, 0.2))
        self.play(FadeOut(noisy_ref), Indicate(clean_wave, color=GREEN, scale_factor=1.05),
                  run_time=max(0.05, 0.24))

        # ------------------------------------------------------------------
        # 34.14-34.98 : third bullet - Baseline stabilisation
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.58))

        b3 = make_bullet("Baseline stabilisation", bullet_y)
        bullet_y -= 0.34
        bullet_list.add(b3)

        drift_start = b3.get_right() + RIGHT * 0.55 + UP * 0.15
        drift_end_sloped = b3.get_right() + RIGHT * 0.55 + DOWN * 0.25
        drift_end_flat = b3.get_right() + RIGHT * 0.55 + UP * 0.15
        drift_line_small = DashedLine(
            drift_start, drift_end_sloped,
            dash_length=0.08, color=GREY_A, stroke_width=3,
        )

        self.play(FadeIn(b3), FadeIn(drift_line_small), run_time=max(0.05, 0.34))
        self.play(drift_line_small.animate.put_start_and_end_on(drift_start, drift_end_flat),
                  run_time=max(0.05, 0.25))
        self.play(FadeOut(drift_line_small), run_time=max(0.05, 0.25))

        # ------------------------------------------------------------------
        # 35.88-36.58 : fourth bullet - Impedance matching
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.90))

        b4 = make_bullet("Impedance matching", bullet_y)
        bullet_y -= 0.34
        bullet_list.add(b4)

        conn_h = RoundedRectangle(
            width=0.35, height=0.16, corner_radius=0.05,
            fill_color=TEAL, fill_opacity=1, stroke_color=TEAL, stroke_width=0,
        )
        conn_v = RoundedRectangle(
            width=0.16, height=0.35, corner_radius=0.05,
            fill_color=TEAL, fill_opacity=1, stroke_color=TEAL, stroke_width=0,
        ).move_to(conn_h)
        connector = VGroup(conn_h, conn_v).scale(0.8).next_to(b4, RIGHT, buff=0.35)

        self.play(FadeIn(b4), FadeIn(connector), run_time=max(0.05, 0.35))
        self.play(FadeOut(connector), run_time=max(0.05, 0.35))

        # ------------------------------------------------------------------
        # 37.20-37.78 : fifth bullet - Signal isolation + panel pulse
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.62))

        b5 = make_bullet("Signal isolation", bullet_y)
        bullet_list.add(b5)

        self.play(FadeIn(b5), run_time=max(0.05, 0.28))
        self.play(Indicate(panel, color=TEAL, scale_factor=1.03), run_time=max(0.05, 0.30))

        # ------------------------------------------------------------------
        # 39.06-44.60 : dependency blocks and dashed arrows
        # ------------------------------------------------------------------
        self.wait(max(0.05, 1.28))

        modality_block = RoundedRectangle(
            width=2.2, height=0.68, corner_radius=0.12,
            fill_color=BLUE, fill_opacity=0.25,
            stroke_color=BLUE, stroke_width=2,
        )
        modality_label_text = Text("Recording modality", font_size=18, color=BLUE)
        modality_label_text.move_to(modality_block.get_center())
        modality_group = VGroup(modality_block, modality_label_text)
        modality_group.move_to(panel.get_left() + LEFT * 1.8 + UP * 0.65)

        acq_block = RoundedRectangle(
            width=2.2, height=0.68, corner_radius=0.12,
            fill_color=BLUE, fill_opacity=0.25,
            stroke_color=BLUE, stroke_width=2,
        )
        acq_label_text = Text("Acquisition system design", font_size=17, color=BLUE)
        acq_label_text.move_to(acq_block.get_center())
        acq_group = VGroup(acq_block, acq_label_text)
        acq_group.move_to(panel.get_left() + LEFT * 1.8 + DOWN * 0.65)

        mod_arrow = make_dashed_arrow(
            modality_group.get_right() + RIGHT * 0.1,
            panel.get_left() + LEFT * 0.1,
            color=BLUE, stroke_width=2,
        )
        acq_arrow = make_dashed_arrow(
            acq_group.get_right() + RIGHT * 0.1,
            panel.get_left() + LEFT * 0.1,
            color=BLUE, stroke_width=2,
        )

        self.play(panel.animate.set_opacity(0.35),
                  bullet_list.animate.set_opacity(0.4), run_time=max(0.05, 0.6))
        self.play(FadeIn(modality_group), FadeIn(acq_group), run_time=max(0.05, 0.7))
        self.play(Create(mod_arrow), Create(acq_arrow), run_time=max(0.05, 0.8))
        self.play(Indicate(mod_arrow, color=BLUE, scale_factor=1.08),
                  Indicate(acq_arrow, color=BLUE, scale_factor=1.08),
                  run_time=max(0.05, 0.7))
        self.wait(max(0.05, 2.74))

        # ------------------------------------------------------------------
        # 45.38-46.48 : fade panel, dim clean content, blank definition box
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.78))

        def_box = RoundedRectangle(
            width=10.0, height=3.6, corner_radius=0.2,
            stroke_color=YELLOW, fill_color=BLACK, fill_opacity=0.8,
            stroke_width=3,
        ).move_to(ORIGIN)

        self.play(
            self.camera.frame.animate.scale(1.12).move_to(ORIGIN),
            FadeOut(panel), FadeOut(bullet_list),
            FadeOut(modality_group), FadeOut(acq_group),
            FadeOut(mod_arrow), FadeOut(acq_arrow),
            clean_wave.animate.set_opacity(0.25),
            sc_block.animate.set_opacity(0.25),
            sc_title.animate.set_opacity(0.25),
            accurate_label.animate.set_opacity(0.25),
            run_time=max(0.05, 0.65),
        )
        self.play(FadeIn(def_box), run_time=max(0.05, 0.45))

        # ------------------------------------------------------------------
        # 47.58-55.48 : definition text, final hold, fade out
        # ------------------------------------------------------------------
        self.wait(max(0.05, 1.10))

        def_left = Text("Signal conditioning", font_size=30,
                        color=YELLOW, weight="BOLD")
        def_eq = Text("=", font_size=36, color=WHITE)
        def_line1 = Text("all operations performed on a biological signal",
                         font_size=20, color=WHITE)
        def_line2 = Text("to prepare it for accurate digitisation",
                         font_size=20, color=WHITE)
        def_line3 = Text("and analysis.", font_size=20, color=WHITE)
        def_right = VGroup(def_line1, def_line2, def_line3).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT
        )
        def_group = VGroup(def_left, def_eq, def_right).arrange(
            RIGHT, buff=0.25, aligned_edge=UP
        )
        def_group.scale_to_fit_width(def_box.width - 1.2)
        def_group.move_to(def_box.get_center())

        self.play(FadeIn(def_left), FadeIn(def_eq), run_time=max(0.05, 1.22))
        self.play(FadeIn(def_line1), run_time=max(0.05, 2.0))
        self.play(FadeIn(def_line2), run_time=max(0.05, 1.8))
        self.play(FadeIn(def_line3), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 0.48))

        final_visible = VGroup(
            def_box, def_group,
            clean_wave, sc_block, sc_title, accurate_label,
        )
        self.play(FadeOut(final_visible), run_time=max(0.05, 1.0))