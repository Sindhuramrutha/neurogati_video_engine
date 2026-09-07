ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- Helper to build a static waveform ----------
        def make_wave(amp, width=1.5, freq=8, color=WHITE, noise=0.0, seed=0, stroke_width=2.5):
            rng = np.random.default_rng(seed)
            xs = np.linspace(-width/2, width/2, 36)
            ys = amp * np.sin(freq * xs)
            if noise > 0:
                ys = ys + noise * rng.normal(size=xs.shape)
            pts = np.c_[xs, ys, np.zeros_like(xs)]
            wave = VMobject()
            wave.set_points_as_corners(pts)
            wave.set_stroke(color=color, width=stroke_width)
            return wave

        def make_jagged_trace(x_min, x_max, baseline, amp, color=ORANGE, seed=0, n=40):
            rng = np.random.default_rng(seed)
            xs = np.linspace(x_min, x_max, n)
            ys = baseline + amp * rng.normal(size=n)
            pts = np.c_[xs, ys, np.zeros_like(xs)]
            trace = VMobject()
            trace.set_points_as_corners(pts)
            trace.set_stroke(color=color, width=3)
            return trace

        # ---------- Layout constants ----------
        HEAD_C = np.array([-5.2, 0.3, 0])
        ELECTRODE_C = np.array([-3.4, 0.4, 0])
        CONTACT = np.array([-3.55, 0.4, 0])
        COMPUTER_C = np.array([5.0, 0.4, 0])
        WIRE_Y = 0.4
        PATH_CENTER = np.array([0.5, 0.4, 0])
        COMPARE_Y = 0.95           # comparison waveforms sit above wire
        MICRO_COMPARE_POS = np.array([0.1, COMPARE_Y, 0])
        TALL_COMPARE_POS = np.array([2.7, COMPARE_Y, 0])
        BLOCK_C = np.array([1.6, WIRE_Y, 0])

        # ---------- Head / electrode / computer ----------
        head_ellipse = Ellipse(width=2.4, height=3.0).move_to(HEAD_C)
        head_ellipse.set_fill(BLUE, opacity=0.28)
        head_ellipse.set_stroke(WHITE, width=3)
        nose = Circle(radius=0.16).move_to(HEAD_C + RIGHT*1.25 + UP*0.15)
        nose.set_fill(BLUE, opacity=0.28).set_stroke(WHITE, width=3)
        neck = Rectangle(width=0.7, height=1.0).move_to(HEAD_C + RIGHT*0.2 + DOWN*2.1)
        neck.set_fill(BLUE, opacity=0.28).set_stroke(WHITE, width=3)
        eye = Dot(point=HEAD_C + RIGHT*0.7 + UP*0.7, radius=0.04, color=WHITE)
        head_group = VGroup(neck, head_ellipse, nose, eye)

        pad = Rectangle(width=0.5, height=0.7).move_to(ELECTRODE_C)
        pad.set_fill(TEAL, opacity=1.0).set_stroke(WHITE, width=2)
        electrode_label = Text("electrode", font_size=20, color=GOLD).next_to(pad, DOWN, buff=0.12)
        contact_dot = Dot(CONTACT, radius=0.09, color=YELLOW)

        monitor = Rectangle(width=1.5, height=1.0).move_to(COMPUTER_C)
        monitor.set_fill(BLUE, opacity=0.9).set_stroke(WHITE, width=2)
        screen = Rectangle(width=1.2, height=0.65).move_to(COMPUTER_C)
        screen.set_fill(TEAL, opacity=0.9).set_stroke(WHITE, width=1)
        stand = Polygon(
            COMPUTER_C + LEFT*0.25 + DOWN*0.65,
            COMPUTER_C + RIGHT*0.25 + DOWN*0.65,
            COMPUTER_C + DOWN*1.3,
            fill_color=GREY, fill_opacity=1.0, stroke_color=WHITE, stroke_width=2
        )
        computer_group = VGroup(stand, monitor, screen)
        computer_label = Text("computer", font_size=20, color=GOLD).next_to(computer_group, DOWN, buff=0.15)
        computer_left_x = monitor.get_left()[0]

        wire_to_computer = Line(
            pad.get_right(),
            np.array([computer_left_x, WIRE_Y, 0]),
            color=GREY, stroke_width=2
        )

        # ---------- Step 1 marker ----------
        step_rect = Rectangle(width=2.2, height=0.7, fill_color=BLUE, fill_opacity=0.9,
                              stroke_color=WHITE, stroke_width=2)
        step_text = Text("Step 1: Detect", font_size=24, color=WHITE)
        step_marker = VGroup(step_rect, step_text).move_to(np.array([-1.2, 1.15, 0]))

        # ---------- Tiny EEG waveform (initial above electrode) ----------
        micro_wave = make_wave(amp=0.08, width=1.8, freq=10, color=WHITE, stroke_width=3)
        micro_wave.move_to(np.array([-3.0, 1.9, 0]))
        micro_label = Text("EEG signal: microvolts", font_size=24, color=WHITE).next_to(micro_wave, UP, buff=0.15)
        micro_scale_line = Line(UP*0.15, DOWN*0.15, color=WHITE, stroke_width=3)
        micro_scale_text = Text("µV", font_size=18, color=WHITE).next_to(micro_scale_line, DOWN, buff=0.08)
        micro_scale_group = VGroup(micro_scale_line, micro_scale_text).next_to(micro_wave, LEFT, buff=0.35)

        # ---------- Tall device voltage waveform ----------
        tall_wave = make_wave(amp=0.75, width=1.6, freq=6, color=ORANGE, stroke_width=3)
        tall_wave.move_to(TALL_COMPARE_POS)
        tall_scale_line = Line(UP*0.65, DOWN*0.65, color=ORANGE, stroke_width=4)
        tall_scale_text = Text("V", font_size=20, color=ORANGE).next_to(tall_scale_line, DOWN, buff=0.08)
        tall_scale_group = VGroup(tall_scale_line, tall_scale_text).move_to(TALL_COMPARE_POS + LEFT*0.9)
        tall_label = Text("typical electronic device voltage: volts", font_size=20, color=WHITE)
        if tall_label.width > 3.5:
            tall_label.scale_to_fit_width(3.5)
        tall_label.next_to(tall_wave, UP, buff=0.1)
        tall_group = VGroup(tall_wave, tall_scale_group, tall_label)

        annotation = Text("~1,000,000x smaller", font_size=24, color=GOLD).move_to(np.array([1.4, 0.25, 0]))

        # ---------- Noise group ----------
        noise_group = VGroup(
            make_jagged_trace(0.5, 4.0, WIRE_Y, 0.75, color=ORANGE, seed=1),
            make_jagged_trace(0.8, 3.8, WIRE_Y+0.5, 0.50, color=ORANGE, seed=2),
            make_jagged_trace(0.8, 3.8, WIRE_Y-0.5, 0.50, color=ORANGE, seed=3),
        )

        # ---------- Computer alert (crossed out) ----------
        computer_alert = VGroup(
            Line(UP*0.3 + LEFT*0.3, DOWN*0.3 + RIGHT*0.3, color=RED, stroke_width=6),
            Line(UP*0.3 + RIGHT*0.3, DOWN*0.3 + LEFT*0.3, color=RED, stroke_width=6),
        ).move_to(monitor.get_center())

        # ---------- Amplification & conditioning block ----------
        block_rect = Rectangle(width=3.0, height=0.9, fill_color=PURPLE, fill_opacity=0.9,
                               stroke_color=WHITE, stroke_width=2).move_to(BLOCK_C)
        block_main_label = Text("Amplification & Signal Conditioning", font_size=22, color=WHITE)
        block_main_label.scale_to_fit_width(2.8).move_to(BLOCK_C)
        block_glow = SurroundingRectangle(block_rect, color=YELLOW, buff=0.1, stroke_width=2, fill_opacity=0)
        block_group = VGroup(block_rect, block_main_label, block_glow)

        block_left_x = block_rect.get_left()[0]
        pre_noise = make_jagged_trace(-3.0, block_left_x, WIRE_Y, amp=0.35, color=ORANGE, seed=7)
        post_clean = Line(
            block_rect.get_right(),
            np.array([computer_left_x, WIRE_Y, 0]),
            color=WHITE, stroke_width=3
        )

        # ---------- Sub-labels ----------
        amp_sub = Text("Amplification", font_size=24, color=GREY_B)
        cond_sub = Text("Signal Conditioning", font_size=24, color=GREY_B)
        sub_labels = VGroup(amp_sub, cond_sub).arrange(RIGHT, buff=0.6).next_to(block_rect, DOWN, buff=0.5)

        # ---------- Amplifier symbol inside block ----------
        input_wave_inside = make_wave(amp=0.06, width=0.6, freq=6, color=GREEN).move_to(block_rect.get_left() + RIGHT*0.45)
        amp_tri = Polygon(
            [-0.25, -0.2, 0], [0.3, 0.0, 0], [-0.25, 0.2, 0],
            fill_color=PURPLE, fill_opacity=1.0, stroke_color=WHITE, stroke_width=2
        ).move_to(block_rect.get_center() + LEFT*0.3)
        amp_text = Text("amplifier", font_size=14, color=WHITE).next_to(amp_tri, DOWN, buff=0.05)
        output_wave_inside = make_wave(amp=0.12, width=0.7, freq=6, color=GREEN).move_to(block_rect.get_right() + LEFT*0.45)
        amp_symbol_group = VGroup(input_wave_inside, amp_tri, amp_text, output_wave_inside)

        # ---------- Before/after waveform pair ----------
        before_wave = make_wave(amp=0.18, width=1.0, freq=8, color=ORANGE, noise=0.15, seed=3)
        before_label = Text("noisy / small", font_size=18, color=ORANGE).next_to(before_wave, DOWN, buff=0.08)
        before_group = VGroup(before_wave, before_label).arrange(DOWN, buff=0.1)

        after_wave = make_wave(amp=0.42, width=1.0, freq=8, color=GREEN)
        after_label = Text("clean / strong", font_size=18, color=GREEN).next_to(after_wave, DOWN, buff=0.08)
        after_group = VGroup(after_wave, after_label).arrange(DOWN, buff=0.1)

        before_after_pair = VGroup(before_group, after_group).arrange(RIGHT, buff=0.9).next_to(block_rect, DOWN, buff=1.6)

        # ---------- Generic conditioning chain ----------
        chain_rects = VGroup(*[
            Rectangle(width=0.8, height=0.55, fill_color=TEAL, fill_opacity=1.0,
                      stroke_color=WHITE, stroke_width=2) for _ in range(3)
        ])
        chain_rects.arrange(RIGHT, buff=0.25).next_to(block_rect, DOWN, buff=1.6)
        squiggle = make_wave(amp=0.1, width=0.5, freq=6, color=WHITE).move_to(chain_rects[0])
        bar = Rectangle(width=0.3, height=0.06, fill_color=YELLOW, fill_opacity=1.0, stroke_width=0).move_to(chain_rects[1])
        arrow = Arrow(
            start=chain_rects[2].get_left() + RIGHT*0.1,
            end=chain_rects[2].get_right() + LEFT*0.1,
            buff=0.1, color=WHITE, stroke_width=2
        )
        conditioning_chain = VGroup(chain_rects, squiggle, bar, arrow)

        # ======================== TIMELINE ========================
        # 0.00–1.14  --- static scene with pulsing dot
        self.add(head_group, pad, electrode_label, contact_dot, wire_to_computer,
                 computer_group, computer_label)
        self.play(contact_dot.animate.set_opacity(0.25), run_time=max(0.05, 0.57))
        self.play(contact_dot.animate.set_opacity(1.0), run_time=max(0.05, 0.57))

        # 1.14–1.66  --- gap before detection pulse
        self.wait(max(0.05, 0.52))

        # 1.66–4.98  --- detection pulse outward + subtitle (3.32 s)
        ripple = Circle(radius=0.12, stroke_color=YELLOW, stroke_width=3,
                        fill_color=YELLOW, fill_opacity=0.35).move_to(CONTACT)
        detect_label = Text("detecting biological signals", font_size=26, color=GOLD).next_to(
            electrode_label, DOWN, buff=0.2)
        self.play(FadeIn(detect_label), ripple.animate.scale(4.5).set_opacity(0), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.82))

        # 4.98–5.46  --- gap
        self.wait(max(0.05, 0.48))

        # 5.46–8.08  --- step marker, dim head/electrode (2.62 s)
        self.play(head_group.animate.set_opacity(0.3),
                  pad.animate.set_opacity(0.3),
                  electrode_label.animate.set_opacity(0.3), run_time=max(0.05, 0.8))
        self.play(GrowFromCenter(step_marker), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.82))

        # 8.08–8.78  --- gap
        self.wait(max(0.05, 0.70))

        # 8.78–12.76 --- tiny EEG waveform appears + gir gentle wiggle (3.98 s)
        self.play(FadeIn(micro_wave), run_time=max(0.05, 0.6))
        self.play(FadeIn(micro_label), run_time=max(0.05, 0.4))
        self.play(Wiggle(micro_wave, scale_value=0.02), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.78))

        # 12.76–13.42 --- gap
        self.wait(max(0.05, 0.66))

        # 13.42–17.44 --- micro wave brightens, scale bar appears (4.02 s)
        self.play(micro_wave.animate.set_opacity(1.0), run_time=max(0.05, 0.8))
        self.play(Write(micro_scale_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.22))

        # 17.44–18.00 --- gap
        self.wait(max(0.05, 0.56))

        # 18.00–22.40 --- comparison: tall waveform, scale, label, annotation (4.40 s)
        self.play(FadeOut(step_marker), run_time=max(0.05, 0.3))
        self.play(
            micro_wave.animate.move_to(MICRO_COMPARE_POS),
            micro_label.animate.move_to(MICRO_COMPARE_POS + UP*0.55),
            micro_scale_group.animate.move_to(MICRO_COMPARE_POS + LEFT*1.3),
            FadeIn(tall_group),
            run_time=max(0.05, 1.7
        ))
        self.play(FadeIn(annotation), run_time=max(0.05, 0.5))
        # both waveforms wiggle during comparison
        self.play(Wiggle(micro_wave, scale_value=0.02), Wiggle(tall_wave, scale_value=0.03), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.7))

        # 22.40–23.32 --- gap
        self.wait(max(0.05, 0.92))

        # 23.32–26.32 --- camera zooms out, tall fades, micro wave travels (3.0 s)
        self.play(self.camera.frame.animate.scale(1.12).move_to(PATH_CENTER),
                  FadeOut(tall_group),
                  FadeOut(micro_label),
                  FadeOut(micro_scale_group),
                  run_time=max(0.05, 1.0))
        self.play(micro_wave.animate.move_to(np.array([2.8, WIRE_Y, 0])).set_opacity(0.2),
                  run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.5))

        # 26.32–31.36 --- noise overwhelms signal, computer alert (5.04 s)
        self.play(FadeOut(micro_wave), FadeIn(noise_group), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.5))
        self.play(noise_group.animate.set_color(RED), run_time=max(0.05, 0.5))
        self.play(noise_group.animate.set_color(ORANGE), run_time=max(0.05, 0.4))
        self.play(Indicate(noise_group, color=ORANGE), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.6))
        self.play(FadeIn(computer_alert), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.44))
        self.play(FadeOut(computer_alert), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.4))

        # 31.36–32.44 --- gap
        self.wait(max(0.05, 1.08))

        # 32.44–38.72 --- amplification & conditioning block inserted (6.28 s)
        self.play(FadeOut(noise_group),
                  FadeIn(block_group),
                  FadeIn(pre_noise),
                  FadeIn(post_clean),
                  run_time=max(0.05, 1.5))
        # gentle pulse of block during narration
        self.play(Indicate(block_group, scale_factor=1.03, color=YELLOW), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 3.98))

        # 38.72–39.74 --- gap
        self.wait(max(0.05, 1.02))

        # 39.74–43.24 --- settle on block, sub-labels, Amplification brightens (3.5 s)
        self.play(self.camera.frame.animate.scale(1.25).move_to(block_rect.get_center()), run_time=max(0.05, 0.8))
        self.play(FadeIn(amp_sub, cond_sub), run_time=max(0.05, 0.5))
        self.play(amp_sub.animate.set_color(YELLOW), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.7))

        # 43.24–44.02 --- gap
        self.wait(max(0.05, 0.78))

        # 44.02–46.10 --- amplifier symbol + before/after pair (2.08 s)
        self.play(FadeOut(block_main_label),
                  FadeIn(amp_symbol_group),
                  FadeIn(before_after_pair),
                  run_time=max(0.05, 0.8))
        self.play(Indicate(amp_sub, color=YELLOW), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.78))

        # 46.10–46.50 --- gap
        self.wait(max(0.05, 0.40))

        # 46.50–49.17 --- signal conditioning chain + final settle (2.67 s)
        self.play(cond_sub.animate.set_color(YELLOW), run_time=max(0.05, 0.5))
        self.play(FadeOut(amp_symbol_group), FadeOut(before_after_pair),
                  FadeIn(conditioning_chain), run_time=max(0.05, 0.8))
        self.play(Indicate(block_group, color=YELLOW), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.87))