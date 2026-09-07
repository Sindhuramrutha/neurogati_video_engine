ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        CYCLES = 1

        def make_wave(center, length, amplitude, color, stroke_width=5, cycles=CYCLES, n=120):
            pts = []
            x0 = center[0] - length / 2
            for i in range(n + 1):
                x = x0 + length * i / n
                y = center[1] + amplitude * np.sin(2 * PI * cycles * (i / n))
                pts.append(np.array([x, y, 0]))
            wave = VMobject()
            wave.set_points_as_corners(pts)
            wave.set_stroke(color=color, width=stroke_width)
            wave.set_fill(opacity=0)
            return wave, pts

        # Input side
        input_baseline = Line(
            start=np.array([-6.25, 1.2, 0]),
            end=np.array([-2.95, 1.2, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        input_wave, input_points = make_wave(
            center=np.array([-4.6, 1.2, 0]),
            length=3.3,
            amplitude=0.20,
            color=TEAL,
            stroke_width=5,
        )
        label_microvolts = Text("a few microvolts", font_size=26, color=YELLOW)
        label_microvolts.next_to(input_wave, DOWN, buff=0.30)

        # Amplifier triangle, empty at first
        amp_triangle = Polygon(
            np.array([-1.0, 1.9, 0]),
            np.array([-1.0, 0.5, 0]),
            np.array([1.0, 1.2, 0]),
            stroke_color=GREY_B,
            stroke_width=5,
            fill_color=BLACK,
            fill_opacity=0,
        )

        # Weak initial flow
        weak_start = input_baseline.get_end()
        weak_end = weak_start + RIGHT * 0.55
        weak_arrow = Arrow(
            start=weak_start,
            end=weak_end,
            buff=0,
            stroke_width=3,
            color=GREY_B,
            max_tip_length_to_length_ratio=0.20,
        )

        # Caption for the too-weak beat
        caption_too_weak = Text(
            "too weak to process reliably",
            font_size=22,
            color=ORANGE,
        )
        caption_too_weak.scale_to_fit_width(4.6).next_to(input_wave, UP, buff=0.25)

        # Strong full flow
        full_flow = Arrow(
            start=weak_start,
            end=amp_triangle.get_left(),
            buff=0,
            stroke_width=5,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.15,
        )

        # Output side
        out_flow_end = np.array([2.7, 1.2, 0])
        out_flow_line = Arrow(
            start=amp_triangle.get_right(),
            end=out_flow_end,
            buff=0,
            stroke_width=5,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.15,
        )
        output_baseline = Line(
            start=out_flow_end,
            end=np.array([6.4, 1.2, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        output_wave, output_points = make_wave(
            center=np.array([4.55, 1.2, 0]),
            length=3.7,
            amplitude=1.0,
            color=ORANGE,
            stroke_width=6,
        )
        label_amplified = Text("amplified signal", font_size=26, color=WHITE)
        label_amplified.next_to(output_wave, DOWN, buff=0.30)

        # Comparison inset
        comp_frame = Rectangle(
            width=6.2,
            height=2.2,
            stroke_color=GREY_B,
            stroke_width=2.5,
            fill_color=BLACK,
            fill_opacity=0.3,
        )
        comp_axis = Line(
            start=np.array([-2.7, 0, 0]),
            end=np.array([2.7, 0, 0]),
            color=GREY_B,
            stroke_width=3,
        )
        comp_guides = VGroup()
        for x in [-2.7, -1.35, 0, 1.35, 2.7]:
            guide = DashedLine(
                start=np.array([x, -1.1, 0]),
                end=np.array([x, 1.1, 0]),
                color=GREY,
                stroke_width=1.5,
            )
            guide.set_stroke(opacity=0.35)
            comp_guides.add(guide)

        small_comp, _ = make_wave(
            center=ORIGIN,
            length=5.4,
            amplitude=0.20,
            color=TEAL,
            stroke_width=5,
        )
        large_comp, _ = make_wave(
            center=ORIGIN,
            length=5.4,
            amplitude=0.95,
            color=ORANGE,
            stroke_width=5,
        )

        comp_group = VGroup(comp_frame, comp_axis, comp_guides, small_comp, large_comp)
        comp_group.move_to(np.array([0, -2.15, 0]))

        caption_same_shape = Text("same shape, bigger", font_size=28, color=YELLOW)
        caption_same_shape.next_to(comp_group, UP, buff=0.20)

        # Beat 1: baseline, tiny waveform, microvolt label
        self.play(Create(input_baseline), run_time=max(0.05, 0.35))
        self.play(Create(input_wave), Write(label_microvolts), run_time=max(0.05, 0.63))

        # Gap before Beat 2
        self.wait(max(0.05, 0.94))

        # Beat 2: weak flow arrow and empty amplifier
        self.play(GrowFromCenter(amp_triangle), Create(weak_arrow), run_time=max(0.05, 1.50))
        self.wait(max(0.05, 2.18))

        # Gap before Beat 3
        self.wait(max(0.05, 0.30))

        # Beat 3: brighten the microvolt label once
        self.play(label_microvolts.animate.set_color(GOLD).scale(1.18), run_time=max(0.05, 0.40))
        self.play(label_microvolts.animate.set_color(YELLOW).scale(1 / 1.18), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 1.06))

        # Gap before Beat 4
        self.wait(max(0.05, 0.38))

        # Beat 4: too weak to process reliably
        self.play(
            Write(caption_too_weak),
            input_baseline.animate.set_stroke(opacity=0.4),
            input_wave.animate.set_stroke(opacity=0.30),
            weak_arrow.animate.set_opacity(0.25),
            label_microvolts.animate.set_opacity(0.4),
            run_time=max(0.05, 1.80),
        )
        self.wait(max(0.05, 1.32))

        # Gap before Beat 5
        self.wait(max(0.05, 0.92))

        # Beat 5: full flow into amplifier, amplifier lights up
        self.play(
            FadeOut(weak_arrow),
            FadeOut(caption_too_weak),
            Create(full_flow),
            input_baseline.animate.set_stroke(opacity=1),
            input_wave.animate.set_stroke(opacity=1),
            label_microvolts.animate.set_opacity(1),
            amp_triangle.animate.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW, width=5),
            run_time=max(0.05, 1.50),
        )
        self.wait(max(0.05, 0.30))

        # Gap before Beat 6
        self.wait(max(0.05, 0.96))

        # Beat 6: output flow and large amplified waveform
        self.play(Create(out_flow_line), run_time=max(0.05, 0.40))
        self.play(
            Create(output_baseline),
            Create(output_wave),
            Write(label_amplified),
            run_time=max(0.05, 1.40),
        )
        self.wait(max(0.05, 0.40))

        # Gap before Beat 7
        self.wait(max(0.05, 0.74))

        # Beat 7: pulse traces along the output waveform
        pulse_dot_out = Dot(
            point=output_points[0],
            radius=0.08,
            color=WHITE,
            fill_opacity=1,
        )
        self.add(pulse_dot_out)

        def update_pulse_out(mob, alpha):
            idx = int(alpha * (len(output_points) - 1))
            mob.move_to(output_points[idx])

        self.play(
            UpdateFromAlphaFunc(pulse_dot_out, update_pulse_out),
            run_time=max(0.05, 3.20),
        )
        self.play(FadeOut(pulse_dot_out), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.24))

        # Gap before Beat 8
        self.wait(max(0.05, 0.66))

        # Beat 8: comparison inset
        self.play(GrowFromCenter(comp_group), run_time=max(0.05, 1.30))
        self.wait(max(0.05, 0.74))

        # Gap before Beat 9
        self.wait(max(0.05, 0.38))

        # Beat 9: large output in the comparison pulses, final caption
        self.play(
            large_comp.animate.set_stroke(color=WHITE, width=7),
            FadeIn(caption_same_shape),
            run_time=max(0.05, 0.40),
        )
        self.play(
            large_comp.animate.set_stroke(color=ORANGE, width=5),
            run_time=max(0.05, 0.25),
        )
        self.wait(max(0.05, 0.35))

        # Beat 10: hold static to end
        self.wait(max(0.05, 0.75))