ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene12(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # -------------------------------
        # Build the six sensor icons
        # -------------------------------
        def make_surface():
            disc = Circle(radius=0.3, color=BLUE, stroke_width=4)
            wire = Line(disc.get_right(), disc.get_right() + RIGHT * 0.9, color=GREY_B, stroke_width=3)
            return VGroup(disc, wire).move_to(ORIGIN)

        def make_needle():
            shaft = Line(UP * 0.3, DOWN * 0.7, color=PURPLE, stroke_width=4)
            bevel = Line(DOWN * 0.7, DOWN * 0.85 + LEFT * 0.12, color=PURPLE, stroke_width=4)
            hub = Rectangle(width=0.5, height=0.2, color=PURPLE, stroke_width=4).move_to(UP * 0.3)
            return VGroup(shaft, bevel, hub).move_to(ORIGIN)

        def make_micro():
            tip = Line(DOWN * 0.9, DOWN * 1.15, color=PINK, stroke_width=2)
            shaft = Line(UP * 0.4, DOWN * 0.9, color=PINK, stroke_width=4)
            hub = Line(LEFT * 0.15, RIGHT * 0.15, color=PINK, stroke_width=4).move_to(UP * 0.4)
            return VGroup(tip, shaft, hub).move_to(ORIGIN)

        def make_eeg_cap():
            head = Arc(radius=0.5, start_angle=0, angle=PI, color=TEAL, stroke_width=4)
            base = Line(LEFT * 0.5, RIGHT * 0.5, color=TEAL, stroke_width=4)
            dots = VGroup(*[
                Dot(radius=0.05, color=TEAL, fill_opacity=1).move_to(head.point_from_proportion(p))
                for p in [0.3, 0.5, 0.7]
            ])
            return VGroup(head, base, dots).move_to(ORIGIN)

        def make_ecog_grid():
            rect = Rectangle(width=0.9, height=0.6, color=GREEN, stroke_width=4)
            grid_dots = VGroup(*[
                Dot(radius=0.05, color=GREEN, fill_opacity=1)
                for _ in range(6)
            ]).arrange_in_grid(rows=2, cols=3, buff=0.16).move_to(rect.get_center())
            wire_tail = Line(rect.get_top(), rect.get_top() + UP * 0.7, color=GREY_B, stroke_width=3)
            return VGroup(rect, grid_dots, wire_tail).move_to(ORIGIN)

        def make_meg_helmet():
            helmet = Arc(radius=0.6, start_angle=0, angle=PI, color=ORANGE, stroke_width=4)
            inner = Arc(radius=0.45, start_angle=0, angle=PI, color=GREY_B, stroke_width=3).shift(DOWN * 0.1)
            sensors = VGroup(*[
                Square(side_length=0.12, color=ORANGE, stroke_width=2).move_to(
                    helmet.point_from_proportion(p) + UP * 0.07
                )
                for p in [0.1, 0.25, 0.4, 0.6, 0.75, 0.9]
            ])
            return VGroup(helmet, inner, sensors).move_to(ORIGIN)

        icon_data = [
            (make_surface(), "Surface\nelectrode"),
            (make_needle(), "Needle\nelectrode"),
            (make_micro(), "Micro\nelectrode"),
            (make_eeg_cap(), "EEG\ncap"),
            (make_ecog_grid(), "ECoG\ngrid"),
            (make_meg_helmet(), "MEG\nhelmet"),
        ]

        icon_items = VGroup()
        for drawing, label_text in icon_data:
            label = Text(label_text, font_size=17, color=WHITE).next_to(drawing, DOWN, buff=0.12)
            icon_items.add(VGroup(drawing, label))

        icon_items.arrange(RIGHT, buff=0.45)
        icon_items.scale_to_fit_width(12.5)
        icon_items.move_to(ORIGIN)

        icon_drawings = VGroup(*[icon_items[i][0] for i in range(len(icon_items))])

        # -------------------------------
        # Acquisition chain
        # -------------------------------
        block_defs = [
            ("Sensor", BLUE),
            ("Amplifier", GREEN),
            ("Conditioning", ORANGE),
            ("Processing", PURPLE),
        ]

        chain_blocks = VGroup()
        for label, col in block_defs:
            rect = Rectangle(
                width=1.4,
                height=0.9,
                fill_color=col,
                fill_opacity=0.22,
                stroke_color=col,
                stroke_width=4,
            )
            text = Text(label, font_size=20, color=WHITE)
            text.scale_to_fit_width(1.2)
            text.move_to(rect.get_center())
            chain_blocks.add(VGroup(rect, text))

        chain_blocks.arrange(RIGHT, buff=0.35)
        chain_blocks.move_to(np.array([2.6, 1.2, 0]))

        sensor_rect = chain_blocks[0][0]
        amp_group = chain_blocks[1]
        amp_rect = chain_blocks[1][0]

        sensor_highlight = SurroundingRectangle(sensor_rect, color=YELLOW, buff=0.08, stroke_width=4)

        # Tiny waveform and scale bar
        wave = FunctionGraph(
            lambda x: 0.10 * np.sin(6 * x),
            x_range=[0, 1.2],
            color=YELLOW,
            stroke_width=5,
        ).move_to(np.array([-1.8, 0.0, 0]))

        scale_bar_line = Line(UP * 0.12, DOWN * 0.12, color=GREY_B, stroke_width=4)
        top_tick = Line(
            scale_bar_line.get_top() + LEFT * 0.08,
            scale_bar_line.get_top() + RIGHT * 0.08,
            color=GREY_B,
            stroke_width=3,
        )
        bottom_tick = Line(
            scale_bar_line.get_bottom() + LEFT * 0.08,
            scale_bar_line.get_bottom() + RIGHT * 0.08,
            color=GREY_B,
            stroke_width=3,
        )
        scale_bar = VGroup(scale_bar_line, top_tick, bottom_tick).move_to(np.array([-2.9, 0.0, 0]))
        scale_label = Text("µV", font_size=20, color=GREY).next_to(scale_bar, LEFT, buff=0.1)

        wave_scale_group = VGroup(wave, scale_bar, scale_label)
        wave_original_center = wave_scale_group.get_center()

        arrow_to_sensor = Arrow(
            start=wave.get_right() + RIGHT * 0.1,
            end=sensor_rect.get_left() + LEFT * 0.05,
            color=YELLOW,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        question_mark = Text("?", font_size=72, color=YELLOW, weight=BOLD).move_to(
            wave.get_center() + UP * 0.5
        )

        # -------------------------------
        # Balance beam
        # -------------------------------
        def make_weight(label, color):
            rect = Rectangle(
                width=1.0,
                height=0.32,
                fill_color=color,
                fill_opacity=0.85,
                stroke_color=WHITE,
                stroke_width=2,
            )
            txt = Text(label, font_size=16, color=WHITE).move_to(rect.get_center())
            txt.scale_to_fit_width(0.82)
            return VGroup(rect, txt)

        fulcrum_pos = np.array([1.5, -2.0, 0])
        beam_line = Rectangle(
            width=5.6,
            height=0.08,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(fulcrum_pos + UP * 0.06)
        fulcrum = Triangle(color=GREY, fill_color=GREY_B, fill_opacity=1).scale(0.5).move_to(fulcrum_pos)

        beam_y = fulcrum_pos[1] + 0.06
        left_top = np.array([fulcrum_pos[0] - 2.8, beam_y, 0])
        right_top = np.array([fulcrum_pos[0] + 2.8, beam_y, 0])

        left_str1 = Line(left_top + LEFT * 0.15, left_top + LEFT * 0.15 + DOWN * 0.7, color=GREY, stroke_width=3)
        left_str2 = Line(left_top + RIGHT * 0.15, left_top + RIGHT * 0.15 + DOWN * 0.7, color=GREY, stroke_width=3)
        left_platform = Rectangle(
            width=0.9,
            height=0.08,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(left_top + DOWN * 0.7)

        right_str1 = Line(right_top + LEFT * 0.15, right_top + LEFT * 0.15 + DOWN * 0.7, color=GREY, stroke_width=3)
        right_str2 = Line(right_top + RIGHT * 0.15, right_top + RIGHT * 0.15 + DOWN * 0.7, color=GREY, stroke_width=3)
        right_platform = Rectangle(
            width=0.9,
            height=0.08,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(right_top + DOWN * 0.7)

        left_pan = VGroup(left_str1, left_str2, left_platform)
        right_pan = VGroup(right_str1, right_str2, right_platform)
        beam_system = VGroup(fulcrum, beam_line, left_pan, right_pan)

        left_center = left_platform.get_center() + UP * 0.18
        right_center = right_platform.get_center() + UP * 0.18

        weight1 = make_weight("signal quality", BLUE).move_to(left_center)
        weight2 = make_weight("spatial resolution", ORANGE).move_to(right_center)
        weight3 = make_weight("patient safety", TEAL).move_to(left_center + UP * 0.38)
        weight4 = make_weight("invasiveness", RED).move_to(right_center + UP * 0.38)

        # ===============================
        # TIMED ANIMATION
        # ===============================

        # 1.20 - 5.70  |  Recap row of six icons
        self.wait(max(0.05, 1.20))
        self.play(FadeIn(icon_items), run_time=max(0.05, 1.5))
        self.play(icon_drawings.animate.scale(1.15), run_time=max(0.05, 0.75))
        self.play(icon_drawings.animate.set_stroke(YELLOW, width=6), run_time=max(0.05, 0.75))
        self.play(icon_drawings.animate.scale(1 / 1.15), run_time=max(0.05, 0.75))
        self.play(icon_drawings.animate.set_stroke(WHITE, width=3), run_time=max(0.05, 0.75))

        # 6.72 - 17.52  |  Icons shrink left, acquisition chain appears
        self.wait(max(0.05, 1.02))
        self.play(
            icon_items.animate.scale(0.28).move_to(LEFT * 4.7),
            FadeIn(chain_blocks),
            run_time=max(0.05, 3.8),
        )
        self.wait(max(0.05, 0.2))
        self.play(Create(sensor_highlight), sensor_rect.animate.set_stroke(YELLOW, width=6), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.3))
        self.play(
            Create(wave),
            Create(scale_bar),
            Write(scale_label),
            Create(arrow_to_sensor),
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 2.8))

        # 18.36 - 26.34  |  Balance beam with four weights
        self.wait(max(0.05, 0.84))
        self.play(FadeIn(beam_system), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.3))

        self.play(GrowFromCenter(weight1), run_time=max(0.05, 0.8))
        beam_system.add(weight1)
        self.wait(max(0.05, 0.4))

        self.play(GrowFromCenter(weight2), run_time=max(0.05, 0.8))
        beam_system.add(weight2)
        self.wait(max(0.05, 0.4))

        self.play(GrowFromCenter(weight3), run_time=max(0.05, 0.8))
        beam_system.add(weight3)
        self.wait(max(0.05, 0.4))

        self.play(GrowFromCenter(weight4), run_time=max(0.05, 0.5))
        beam_system.add(weight4)
        self.play(beam_system.animate.rotate(-0.08, about_point=fulcrum_pos), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.88))

        # 27.17 - 32.66  |  Beam fades, amplifier flashes, question appears
        self.wait(max(0.05, 0.83))
        self.play(FadeOut(beam_system), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.3))
        self.play(amp_group.animate.scale(1.12), run_time=max(0.05, 0.8))
        self.play(amp_group.animate.scale(1 / 1.12), run_time=max(0.05, 0.8))
        self.play(GrowFromCenter(question_mark), run_time=max(0.05, 0.7))
        self.play(Indicate(wave, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.09))

        # 33.60 - 38.08  |  Close-up of tiny waveform
        self.wait(max(0.05, 0.94))
        self.play(FadeOut(arrow_to_sensor), FadeOut(question_mark), run_time=max(0.05, 0.5))
        self.play(
            wave_scale_group.animate.scale(2.8).move_to(DOWN * 0.7),
            amp_group.animate.set_opacity(0.3),
            run_time=max(0.05, 2.0),
        )
        few_uv_label = Text(
            "a few microvolts",
            font_size=36,
            color=YELLOW,
            weight=BOLD,
        ).next_to(wave_scale_group, DOWN, buff=0.4)
        self.play(Write(few_uv_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.98))

        # 38.84 - 40.86  |  Weak-signal warning
        self.wait(max(0.05, 0.76))
        weak_label = Text("weak signal", font_size=44, color=RED, weight=BOLD).next_to(
            wave_scale_group, UP, buff=0.4
        )
        exclaim_mark = Text("!", font_size=70, color=RED, weight=BOLD).next_to(
            weak_label, RIGHT, buff=0.2
        )
        cannot_label = Text(
            "cannot be processed directly",
            font_size=24,
            color=GREY,
        ).next_to(amp_group, DOWN, buff=0.3)

        self.play(Write(weak_label), GrowFromCenter(exclaim_mark), run_time=max(0.05, 1.0))
        self.play(Write(cannot_label), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.32))

        # 41.78 - 50.75  |  Amplifier becomes focus
        self.wait(max(0.05, 0.92))
        warnings = VGroup(weak_label, exclaim_mark, cannot_label)
        self.play(FadeOut(warnings), run_time=max(0.05, 0.6))

        self.play(
            wave_scale_group.animate.scale(1 / 2.8).move_to(wave_original_center),
            amp_group.animate.scale(1.3),
            run_time=max(0.05, 1.4),
        )
        self.play(amp_group.animate.set_opacity(1), run_time=max(0.05, 0.4))
        self.play(amp_rect.animate.set_fill(GREEN, opacity=0.7), run_time=max(0.05, 0.4))
        self.play(amp_rect.animate.set_stroke(YELLOW, width=6), run_time=max(0.05, 0.4))

        amplification_label = Text(
            "Amplification",
            font_size=32,
            color=GREEN,
            weight=BOLD,
        ).next_to(amp_group, DOWN, buff=0.15)
        self.play(Write(amplification_label), run_time=max(0.05, 0.7))

        signal_cond_label = Text(
            "Signal conditioning",
            font_size=28,
            color=ORANGE,
            weight=BOLD,
        ).next_to(chain_blocks[2], DOWN, buff=0.15)
        self.play(FadeIn(signal_cond_label), run_time=max(0.05, 0.7))

        arrow_amp_to_wave = Arrow(
            start=wave.get_right() + RIGHT * 0.1,
            end=amp_rect.get_left() + LEFT * 0.1,
            color=YELLOW,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(Create(arrow_amp_to_wave), run_time=max(0.05, 0.8))

        self.wait(max(0.05, 3.57))