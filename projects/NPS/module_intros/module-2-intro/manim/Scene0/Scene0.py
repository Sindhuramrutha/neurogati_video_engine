ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 0.00-0.54
        title = Text("MODULE 2", font_size=72, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        subtitle = Text("The Neural Signal Acquisition Chain", font_size=42, color=WHITE)
        subtitle.scale_to_fit_width(12)
        subtitle.next_to(title, DOWN, buff=0.4)
        title_final = title.get_center().copy()
        title.move_to(title_final + UP*5)
        self.play(title.animate.move_to(title_final), run_time=max(0.05, 0.54), rate_func=rate_functions.ease_out_cubic)

        # 0.54-2.98
        self.play(AddTextLetterByLetter(subtitle), run_time=max(0.05, 2.44))
        self.wait(max(0.05, 0.84))

        chain_parts = []

        # 3.82-4.42 electrode
        shaft = Rectangle(width=0.28, height=1.2, fill_color=BLUE, fill_opacity=1, stroke_width=0)
        shaft.move_to(np.array([-5, 0.25, 0]))
        tip = Polygon([-5.14, -0.35, 0], [-4.86, -0.35, 0], [-5, -0.85, 0],
                      fill_color=BLUE, fill_opacity=1, stroke_width=0)
        electrode_shape = VGroup(shaft, tip)
        electrode_label = Text("Electrode", font_size=26, color=GREY_B).move_to(np.array([-5, -1.8, 0]))
        electrode_display = VGroup(electrode_shape, electrode_label)
        tip_apex = np.array([-5, -0.85, 0])
        self.play(GrowFromPoint(electrode_display, point=tip_apex), run_time=max(0.05, 0.60))
        chain_parts.append(electrode_display)

        # 4.42-5.86 ripples from electrode tip
        for _ in range(3):
            ripple = Circle(radius=0.25, color=TEAL, stroke_width=3)
            ripple.move_to(tip_apex)
            self.add(ripple)
            self.play(ripple.animate.scale(2.5).set_opacity(0), rate_func=linear, run_time=max(0.05, 0.48))
            self.remove(ripple)
        self.wait(max(0.05, 0.52))

        # 6.38-7.72 amplifier/filter + arrow
        amp_tri = Polygon([-0.9, 0.55, 0], [-0.9, -0.55, 0], [0.9, 0, 0],
                          fill_color=ORANGE, fill_opacity=1, stroke_width=0)
        amp_plus = Text("+", font_size=30, color=WHITE).move_to(np.array([-0.55, -0.25, 0]))
        amp_minus = Text("-", font_size=30, color=WHITE).move_to(np.array([-0.55, 0.25, 0]))
        amp_icon = VGroup(amp_tri, amp_plus, amp_minus)
        amp_icon.move_to(np.array([-2.2, -4, 0]))
        amp_label = Text("Amplifier / Filter", font_size=26, color=GREY_B).move_to(np.array([-2.2, -1.8, 0]))
        self.play(
            amp_icon.animate.move_to(np.array([-2.2, 0, 0])),
            FadeIn(amp_label),
            run_time=max(0.05, 0.80),
            rate_func=rate_functions.ease_out_cubic
        )
        amp_display = VGroup(amp_icon, amp_label)
        chain_parts.append(amp_display)

        arrow1 = Arrow(start=np.array([-4.8, 0, 0]), end=np.array([-3.15, 0, 0]),
                       buff=0.05, color=WHITE, stroke_width=4)
        self.play(Create(arrow1), run_time=max(0.05, 0.54))
        chain_parts.append(arrow1)

        # 7.72-8.56 condition them
        noise_wave = FunctionGraph(lambda x: 0.2*np.sin(15*x) + 0.08*np.sin(29*x),
                                   x_range=[-0.8, 0.8], color=TEAL, stroke_width=3)
        noise_wave.move_to(np.array([-3.9, 0.8, 0]))
        clean_wave = FunctionGraph(lambda x: 0.25*np.sin(2*np.pi*x/1.2),
                                   x_range=[0, 2.4], color=GREEN, stroke_width=3)
        clean_wave.move_to(np.array([-0.2, 0.8, 0]))
        self.play(Create(noise_wave), run_time=max(0.05, 0.28))
        self.play(ReplacementTransform(noise_wave, clean_wave), run_time=max(0.05, 0.56))
        chain_parts.append(clean_wave)
        self.wait(max(0.05, 0.52))

        # 9.08-9.64 ADC + arrow
        adc_segments = VGroup()
        pts = [
            (-0.8, 0), (-0.5, 0), (-0.5, 0.5), (-0.2, 0.5),
            (-0.2, -0.2), (0.1, -0.2), (0.1, 0.3), (0.6, 0.3)
        ]
        for p, q in zip(pts[:-1], pts[1:]):
            adc_segments.add(Line(np.array([p[0], p[1], 0]),
                                  np.array([q[0], q[1], 0]),
                                  color=PURPLE, stroke_width=6))
        adc_icon = adc_segments
        adc_icon.move_to(np.array([1.4, 0, 0]))
        adc_label = Text("ADC", font_size=26, color=GREY_B).move_to(np.array([1.4, -1.8, 0]))
        adc_display = VGroup(adc_icon, adc_label)
        self.play(LaggedStart(*[Create(seg) for seg in adc_segments], lag_ratio=0.15), run_time=max(0.05, 0.36))

        arrow2 = Arrow(start=np.array([-1.25, 0, 0]), end=np.array([0.5, 0, 0]),
                       buff=0.05, color=WHITE, stroke_width=4)
        self.play(Create(arrow2), run_time=max(0.05, 0.20))
        chain_parts.append(adc_display)
        chain_parts.append(arrow2)

        # 9.64-11.26 digital output
        bar_xs = [2.9, 3.4, 3.9, 4.4, 4.9]
        heights = [0.35, 0.65, 0.25, 0.55, 0.45]
        digital_bars = VGroup()
        for x, h in zip(bar_xs, heights):
            bar = Rectangle(width=0.25, height=h, fill_color=GREEN, fill_opacity=1, stroke_width=0)
            bar.move_to(np.array([x, 0, 0]))
            digital_bars.add(bar)
        digital_label = Text("Digital data", font_size=26, color=GREY_B).move_to(np.array([3.9, -1.8, 0]))
        digital_group = VGroup(digital_bars, digital_label)
        self.play(
            LaggedStart(*[GrowFromCenter(bar) for bar in digital_bars], lag_ratio=0.25),
            FadeIn(digital_label),
            run_time=max(0.05, 0.90
        ))
        self.play(digital_group.animate.shift(RIGHT*1.3), run_time=max(0.05, 0.72), rate_func=linear)
        chain_parts.append(digital_group)

        # 11.26-12.62 traveling pulse
        pulse_dot = Dot(radius=0.08, color=YELLOW, fill_opacity=1).move_to(np.array([-4.7, 0, 0]))
        pulse_glow = Circle(radius=0.22, color=YELLOW, stroke_width=3).move_to(pulse_dot.get_center())
        pulse = VGroup(pulse_glow, pulse_dot)
        pulse_path = Line(start=np.array([-4.7, 0, 0]), end=np.array([6.0, 0, 0]),
                          color=WHITE, stroke_opacity=0)
        self.add(pulse_path)
        self.add(pulse)
        self.play(MoveAlongPath(pulse, pulse_path), run_time=max(0.05, 1.36), rate_func=linear)
        chain_parts.append(pulse)
        self.wait(max(0.05, 1.06))

        # 13.68-14.34 clear chain + burst phrase
        self.play(*[FadeOut(p) for p in chain_parts], run_time=max(0.05, 0.25))

        lets_go = Text("Let's get started!", font_size=100, color=YELLOW, weight=BOLD)
        lets_go.scale_to_fit_width(11)
        lets_go.move_to(ORIGIN)
        lets_go.scale(0.2).set_opacity(0)

        flash_rect = Rectangle(width=14, height=8, fill_color=YELLOW, fill_opacity=0.35, stroke_width=0)
        flash_rect.move_to(ORIGIN)

        self.add(lets_go)
        self.play(
            lets_go.animate.scale(5).set_opacity(1),
            FadeIn(flash_rect),
            run_time=max(0.05, 0.30),
            rate_func=rate_functions.ease_out_back
        )
        self.play(FadeOut(flash_rect), run_time=max(0.05, 0.11))

        # 14.34-15.10 hold with slight settle/pulse
        self.play(lets_go.animate.scale(1.03), run_time=max(0.05, 0.38))
        self.play(lets_go.animate.scale(1/1.03), run_time=max(0.05, 0.38))