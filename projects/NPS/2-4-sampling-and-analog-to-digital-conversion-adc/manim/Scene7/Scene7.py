ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Helpers for the six inline icons
        # ------------------------------------------------------------------
        def make_sine_icon():
            width = 0.9
            height = 0.45
            n = 80
            pts = []
            for x in np.linspace(-width / 2, width / 2, n):
                y = height / 2 * np.sin(2 * PI * (x + width / 2) / width * 2.0)
                pts.append([x, y, 0.0])
            icon = VMobject()
            icon.set_stroke(BLUE, width=2.5)
            icon.set_points_as_corners(pts)
            return icon

        def make_digital_icon():
            r1 = Text("1 0 1 0", font_size=17, color=GREEN)
            r2 = Text("0 1 0 1", font_size=17, color=GREEN)
            icon = VGroup(r1, r2).arrange(DOWN, buff=0.05)
            return icon

        def make_monitor_icon():
            screen = Rectangle(
                width=0.65,
                height=0.42,
                fill_color=BLUE,
                fill_opacity=0.25,
                stroke_color=BLUE,
                stroke_width=2,
            )
            stand = Line(
                screen.get_bottom() + DOWN * 0.03,
                screen.get_bottom() + DOWN * 0.16,
                color=BLUE,
                stroke_width=2,
            )
            base = Line(
                stand.get_end() + LEFT * 0.12,
                stand.get_end() + RIGHT * 0.12,
                color=BLUE,
                stroke_width=2,
            )
            return VGroup(screen, stand, base)

        def make_dots_icon():
            line = Line(LEFT * 0.4, RIGHT * 0.4, color=GREY_B, stroke_width=2)
            dots = VGroup(*[
                Dot(point=np.array([x, 0.0, 0.0]), radius=0.05, color=TEAL, fill_opacity=1)
                for x in np.linspace(-0.3, 0.3, 5)
            ])
            return VGroup(line, dots), dots

        def make_hz_icon():
            sq = VMobject()
            sq.set_stroke(PURPLE, width=2.5)
            sq.set_points_as_corners([
                [-0.35, 0.0, 0.0],
                [-0.22, 0.12, 0.0],
                [-0.08, -0.12, 0.0],
                [0.06, 0.12, 0.0],
                [0.20, -0.12, 0.0],
                [0.33, 0.0, 0.0],
            ])
            hz = Text("Hz", font_size=18, color=PURPLE, weight="BOLD")
            return VGroup(sq, hz).arrange(RIGHT, buff=0.10), hz

        def make_adc_icon():
            chip = Rectangle(
                width=0.70,
                height=0.45,
                fill_color=ORANGE,
                fill_opacity=0.25,
                stroke_color=ORANGE,
                stroke_width=2,
            )
            ys = [-0.10, 0.0, 0.10]
            left_pins = VGroup(*[
                Line(
                    start=chip.get_left() + UP * y,
                    end=chip.get_left() + LEFT * 0.18 + UP * y,
                    color=ORANGE,
                    stroke_width=1.5,
                )
                for y in ys
            ])
            right_pins = VGroup(*[
                Line(
                    start=chip.get_right() + UP * y,
                    end=chip.get_right() + RIGHT * 0.18 + UP * y,
                    color=ORANGE,
                    stroke_width=1.5,
                )
                for y in ys
            ])
            return VGroup(left_pins, right_pins, chip)

        # ------------------------------------------------------------------
        # Title and recap list setup
        # ------------------------------------------------------------------
        title = Text("Summary of Key Concepts", font_size=36, color=WHITE, weight="BOLD")
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=max(0.05, 1.6))

        icon1 = make_sine_icon()
        icon2 = make_digital_icon()
        icon3 = make_monitor_icon()
        icon4, dots_group4 = make_dots_icon()
        icon5, hz_text = make_hz_icon()
        icon6 = make_adc_icon()

        texts = [
            "Analogue neural signals are converted into digital data",
            "Neural signals are naturally analogue",
            "Computers require digital data for processing",
            "Sampling measures the analogue signal at regular time intervals",
            "Sampling frequency specifies how many samples are collected each second",
            "The analog-to-digital converter performs the conversion from analogue signals to digital numbers",
        ]
        icons = [icon1, icon2, icon3, icon4, icon5, icon6]

        rows = []
        for txt, ic in zip(texts, icons):
            label = Text(txt, font_size=18, color=WHITE)
            row = VGroup(ic, label).arrange(RIGHT, buff=0.18)
            rows.append(row)

        list_group = VGroup(*rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        list_group.next_to(title, DOWN, buff=0.50)

        row1, row2, row3, row4, row5, row6 = rows

        # Connector line and label (added later)
        chain_line_y = list_group.get_bottom()[1] - 0.22
        chain_line = Line(
            start=np.array([-5.0, chain_line_y, 0.0]),
            end=np.array([5.0, chain_line_y, 0.0]),
            color=GREY,
            stroke_width=1.5,
        )
        chain_label = Text("Signal Acquisition Chain", font_size=15, color=GREY)
        chain_label.next_to(chain_line, DOWN, buff=0.08)

        # Checkmark item and downstream stages
        check_icon = VGroup(
            Circle(
                radius=0.22,
                color=GREEN,
                stroke_width=2,
                fill_color=GREEN,
                fill_opacity=0.15,
            ),
            Text("✓", font_size=20, color=GREEN, weight="BOLD"),
        )
        check_text = Text("Accurate sampling is essential", font_size=18, color=WHITE)
        check_item = VGroup(check_icon, check_text).arrange(RIGHT, buff=0.15)
        check_item.next_to(chain_label, DOWN, buff=0.28)

        downstream_boxes = []
        for name in ["Filtering", "Spectral Analysis", "Feature Extraction"]:
            box = Rectangle(
                width=0.95,
                height=0.36,
                fill_color=GREY,
                fill_opacity=0.15,
                stroke_color=GREY,
                stroke_width=1,
            )
            t = Text(name, font_size=13, color=GREY)
            t.scale_to_fit_width(0.85)
            t.move_to(box)
            downstream_boxes.append(VGroup(box, t))

        downstream_group = VGroup(*downstream_boxes).arrange(RIGHT, buff=0.30)
        downstream_group.scale_to_fit_width(4.8)
        downstream_group.next_to(check_item, DOWN, buff=0.35)

        arr1 = Arrow(
            start=downstream_boxes[0].get_right() + RIGHT * 0.08,
            end=downstream_boxes[1].get_left() + LEFT * 0.08,
            color=GREY,
            stroke_width=1.5,
            buff=0.03,
        )
        arr2 = Arrow(
            start=downstream_boxes[1].get_right() + RIGHT * 0.08,
            end=downstream_boxes[2].get_left() + LEFT * 0.08,
            color=GREY,
            stroke_width=1.5,
            buff=0.03,
        )
        downstream_group.add(arr1, arr2)
        downstream_group.set_opacity(0.25)

        dep_arrow = Arrow(
            start=check_item.get_bottom() + DOWN * 0.08,
            end=downstream_group.get_top() + UP * 0.08,
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
        )

        # Question mark transition content
        question_mark = Text("?", font_size=48, color=YELLOW, weight="BOLD")
        question_text = Text("One more essential aspect", font_size=22, color=WHITE, weight="BOLD")
        question_group = VGroup(question_mark, question_text).arrange(RIGHT, buff=0.20)
        question_group.move_to(np.array([0.0, -2.9, 0.0]))

        # ------------------------------------------------------------------
        # 1.60 - 6.54: First item + pulse the waveform icon
        # ------------------------------------------------------------------
        self.play(FadeIn(row1), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 1.0))
        self.play(icon1.animate.scale(1.25), run_time=max(0.05, 0.4))
        self.play(icon1.animate.scale(0.8), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 1.64))

        # ------------------------------------------------------------------
        # 6.54 - 8.92: Second item
        # ------------------------------------------------------------------
        self.play(FadeIn(row2), run_time=max(0.05, 2.38))

        # ------------------------------------------------------------------
        # 8.92 - 11.96: Third item + highlight the first three items
        # ------------------------------------------------------------------
        self.play(FadeIn(row3), run_time=max(0.05, 1.44))
        self.wait(max(0.05, 0.6))
        self.play(Indicate(VGroup(row1, row2, row3), color=YELLOW, scale_factor=1.03), run_time=max(0.05, 1.0))

        # ------------------------------------------------------------------
        # 11.96 - 16.02: Fourth item + brighten evenly spaced dots
        # ------------------------------------------------------------------
        self.play(FadeIn(row4), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 0.7))
        self.play(Indicate(dots_group4, color=YELLOW, scale_factor=1.3), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.96))

        # ------------------------------------------------------------------
        # 16.02 - 21.02: Fifth item + pulse Hz label
        # ------------------------------------------------------------------
        self.play(FadeIn(row5), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 1.0))
        self.play(hz_text.animate.scale(1.25), run_time=max(0.05, 0.4))
        self.play(hz_text.animate.scale(0.8), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 1.6))

        # ------------------------------------------------------------------
        # 21.02 - 26.88: Sixth item + highlight ADC chip
        # ------------------------------------------------------------------
        self.play(FadeIn(row6), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 1.2))
        self.play(Indicate(icon6, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 2.06))

        # ------------------------------------------------------------------
        # 26.88 - 36.26: Accurate sampling + downstream dependency arrow
        # ------------------------------------------------------------------
        self.play(FadeIn(check_item), run_time=max(0.05, 1.8))
        self.play(FadeIn(downstream_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.7))
        self.play(Create(dep_arrow), run_time=max(0.05, 2.0))
        self.play(Indicate(dep_arrow, color=YELLOW, scale_factor=1.0), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.88))

        # ------------------------------------------------------------------
        # 36.26 - 45.12: Signal Acquisition Chain connector + left/right pulses
        # ------------------------------------------------------------------
        self.play(Create(chain_line), run_time=max(0.05, 2.0))
        self.play(FadeIn(chain_label), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.5))
        self.play(Indicate(icon1, color=BLUE, scale_factor=1.2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.4))
        self.play(Indicate(icon6, color=ORANGE, scale_factor=1.2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.96))

        # ------------------------------------------------------------------
        # 45.12 - 48.78: Dim recap + question mark transition
        # ------------------------------------------------------------------
        recap_all = VGroup(*rows, check_item, chain_line, chain_label)
        self.play(
            recap_all.animate.set_opacity(0.6),
            FadeOut(downstream_group),
            FadeOut(dep_arrow),
            run_time=max(0.05, 1.0),
        )
        self.play(FadeIn(question_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.66))

        # ------------------------------------------------------------------
        # 48.78 - 60.20: Transition to person + recording equipment graphic
        # ------------------------------------------------------------------
        self.play(FadeOut(recap_all), FadeOut(question_group), run_time=max(0.05, 1.0))

        person_center = np.array([-4.5, -0.5, 0.0])
        head = Circle(radius=0.18, color=WHITE, fill_opacity=1, stroke_width=0)
        head.move_to(person_center + UP * 0.75)
        body = Line(
            start=person_center + UP * 0.45,
            end=person_center + DOWN * 0.15,
            color=WHITE,
            stroke_width=3,
        )
        arm_right = Line(
            start=person_center + UP * 0.05,
            end=person_center + RIGHT * 0.6 + DOWN * 0.05,
            color=WHITE,
            stroke_width=3,
        )
        arm_left = Line(
            start=person_center + UP * 0.05,
            end=person_center + LEFT * 0.35 + DOWN * 0.05,
            color=WHITE,
            stroke_width=3,
        )
        leg_left = Line(
            start=person_center + DOWN * 0.15,
            end=person_center + LEFT * 0.25 + DOWN * 0.85,
            color=WHITE,
            stroke_width=3,
        )
        leg_right = Line(
            start=person_center + DOWN * 0.15,
            end=person_center + RIGHT * 0.25 + DOWN * 0.85,
            color=WHITE,
            stroke_width=3,
        )
        person = VGroup(head, body, arm_left, arm_right, leg_left, leg_right)

        equipment_box = Rectangle(
            width=1.8,
            height=1.2,
            fill_color=BLUE,
            fill_opacity=0.25,
            stroke_color=BLUE,
            stroke_width=2,
        )
        equipment_label = Text("Recording Equipment", font_size=16, color=WHITE, weight="BOLD")
        equipment_label.scale_to_fit_width(1.5)
        equipment_label.move_to(equipment_box.get_center())
        input_port = Dot(
            point=equipment_box.get_left() + LEFT * 0.06,
            radius=0.07,
            color=TEAL,
            fill_opacity=1,
        )
        equipment_group = VGroup(equipment_box, equipment_label, input_port)
        equipment_group.move_to(np.array([4.5, -0.5, 0.0]))

        cable = Line(
            start=arm_right.get_end(),
            end=input_port.get_center(),
            color=TEAL,
            stroke_width=2.5,
        )

        # Electrical safety symbol: yellow triangle with black lightning bolt
        w, h = 0.70, 0.60
        tri = Polygon(
            np.array([0.0, h / 2, 0.0]),
            np.array([-w / 2, -h / 2, 0.0]),
            np.array([w / 2, -h / 2, 0.0]),
            color=YELLOW,
            fill_opacity=1,
            stroke_color=BLACK,
            stroke_width=2,
        )
        bolt = Polygon(
            np.array([-0.06, 0.20, 0.0]),
            np.array([0.10, 0.20, 0.0]),
            np.array([0.16, -0.02, 0.0]),
            np.array([0.02, -0.02, 0.0]),
            np.array([0.16, -0.22, 0.0]),
            np.array([-0.08, -0.06, 0.0]),
            color=BLACK,
            fill_opacity=1,
            stroke_width=1,
        )
        safety_symbol = VGroup(tri, bolt)
        safety_symbol.move_to(cable.get_center() + UP * 0.75)

        self.play(FadeIn(person), FadeIn(equipment_group), run_time=max(0.05, 1.2))
        self.play(Create(cable), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.3))
        self.play(FadeIn(safety_symbol), run_time=max(0.05, 0.6))

        # Flashing safety symbol
        for _ in range(4):
            self.play(safety_symbol.animate.scale(1.25), run_time=max(0.05, 0.35))
            self.play(safety_symbol.animate.scale(0.8), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 2.52))

        # ------------------------------------------------------------------
        # 60.20 - 64.50: Electrical Safety and Isolation label + final pulse
        # ------------------------------------------------------------------
        safety_label = Text(
            "Electrical Safety and Isolation",
            font_size=24,
            color=WHITE,
            weight="BOLD",
        )
        safety_label.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(safety_label), run_time=max(0.05, 1.0))
        self.play(safety_label.animate.set_color(YELLOW), run_time=max(0.05, 0.8))
        self.play(Indicate(safety_symbol, color=YELLOW, scale_factor=1.3), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.7))

        # ------------------------------------------------------------------
        # 64.50 - 69.28: Final composition with "Next: Electrical Safety and Isolation"
        # ------------------------------------------------------------------
        next_label = Text(
            "Next: Electrical Safety and Isolation",
            font_size=24,
            color=YELLOW,
            weight="BOLD",
        )
        next_label.move_to(safety_label.get_center())
        glow = Circle(
            radius=0.55,
            color=YELLOW,
            fill_opacity=0.15,
            stroke_width=0,
        )
        glow.move_to(safety_symbol)

        self.play(Transform(safety_label, next_label), run_time=max(0.05, 1.0))
        self.play(FadeIn(glow), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 2.98))