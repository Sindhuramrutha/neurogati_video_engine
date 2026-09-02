ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'
}


class Scene29(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        BACKGROUND = "#0F1116"

        # ---------- helpers ----------
        def make_wave_from_points(xs, ys, color=WHITE, stroke_width=2.5):
            wave = VMobject()
            wave.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
            wave.set_stroke(color, width=stroke_width)
            return wave

        def brain_asset(h=0.5, color=WHITE):
            b = SVGMobject(ASSET_PATHS["brain"])
            b.set_color(color)
            b.scale_to_fit_height(h)
            b.set_stroke(color, width=1.2)
            b.set_fill(color, opacity=0.25)
            return b

        def tiny_wave(width=1.0, freq=2.0, amp=0.08, color=WHITE, n=40):
            xs = np.linspace(-width / 2, width / 2, n)
            ys = amp * np.sin(freq * xs / width * 2 * np.pi)
            return make_wave_from_points(xs, ys, color=color, stroke_width=2)

        def make_device(height=0.55):
            screen = RoundedRectangle(width=0.75, height=0.5, corner_radius=0.05,
                                     fill_color=GREY_E, fill_opacity=0.8,
                                     stroke_color=WHITE, stroke_width=2)
            stand = Line(screen.get_bottom(), screen.get_bottom() + DOWN * 0.18,
                         color=WHITE, stroke_width=2)
            base = Line(stand.get_end() + LEFT * 0.18, stand.get_end() + RIGHT * 0.18,
                        color=WHITE, stroke_width=2)
            cursor = Polygon(
                [0.06, 0.0, 0], [0.0, -0.06, 0], [0.12, -0.06, 0],
                [0.12, 0.12, 0], fill_color=WHITE, fill_opacity=1, stroke_width=0,
            ).move_to(screen.get_center())
            return VGroup(screen, stand, base, cursor)

        def make_double_arrow(length=0.9):
            arr1 = Arrow(LEFT * length, RIGHT * length, color=GOLD, stroke_width=4,
                         buff=0.08, max_tip_length_to_length_ratio=0.25)
            arr2 = Arrow(RIGHT * length, LEFT * length, color=GOLD, stroke_width=4,
                         buff=0.08, max_tip_length_to_length_ratio=0.25)
            line = Line(LEFT * length, RIGHT * length, color=GOLD, stroke_width=1.5)
            return VGroup(arr1, arr2, line)

        def make_thought_bubble_icon():
            bubble_main = Ellipse(width=0.5, height=0.4, fill_color=WHITE,
                                  fill_opacity=0.3, stroke_color=WHITE, stroke_width=2)
            tail1 = Circle(radius=0.04, fill_color=WHITE, fill_opacity=0.4,
                           stroke_width=0).shift(DOWN * 0.25 + LEFT * 0.05)
            tail2 = Circle(radius=0.05, fill_color=WHITE, fill_opacity=0.4,
                           stroke_width=0).shift(DOWN * 0.35 + LEFT * 0.1)
            return VGroup(bubble_main, tail1, tail2).scale_to_fit_height(0.55)

        def make_speech_bubble_icon():
            bubble = Ellipse(width=0.52, height=0.34, fill_color=WHITE,
                             fill_opacity=0.35, stroke_color=WHITE, stroke_width=2)
            tail = Polygon([-0.08, -0.16, 0], [-0.22, -0.3, 0], [-0.06, -0.28, 0],
                           fill_color=WHITE, fill_opacity=0.35, stroke_width=0)
            return VGroup(bubble, tail).scale_to_fit_height(0.45)

        def make_walking_icon():
            head = Circle(radius=0.06, fill_color=WHITE, fill_opacity=0.9,
                          stroke_width=0).move_to(UP * 0.16)
            body = Line(UP * 0.04, ORIGIN, color=WHITE, stroke_width=2)
            leg1 = Line(ORIGIN, LEFT * 0.12 + DOWN * 0.2, color=WHITE, stroke_width=2)
            leg2 = Line(ORIGIN, RIGHT * 0.12 + DOWN * 0.2, color=WHITE, stroke_width=2)
            arm1 = Line(UP * 0.02, LEFT * 0.15 + DOWN * 0.04, color=WHITE, stroke_width=2)
            arm2 = Line(UP * 0.02, RIGHT * 0.15 + DOWN * 0.04, color=WHITE, stroke_width=2)
            return VGroup(head, body, leg1, leg2, arm1, arm2).scale_to_fit_height(0.45)

        def make_prosthetic_icon():
            hand = SVGMobject(ASSET_PATHS["hand"]).set_color(WHITE)
            hand.scale_to_fit_height(0.45)
            hand.set_stroke(WHITE, width=1.2)
            return hand

        def make_flask_icon():
            neck = Rectangle(width=0.12, height=0.15, stroke_color=WHITE,
                             stroke_width=2, fill_color=TEAL, fill_opacity=0.2).move_to(UP * 0.16)
            body = Polygon([-0.2, -0.12, 0], [0.2, -0.12, 0],
                           [0.08, 0.06, 0], [-0.08, 0.06, 0],
                           fill_color=TEAL, fill_opacity=0.35,
                           stroke_color=WHITE, stroke_width=2)
            liquid = Polygon([-0.17, -0.03, 0], [0.17, -0.03, 0],
                             [0.08, 0.06, 0], [-0.08, 0.06, 0],
                             fill_color=TEAL, fill_opacity=0.9, stroke_width=0)
            return VGroup(body, liquid, neck).scale_to_fit_height(0.45)

        def make_panel_content(idx):
            panel_titles = ["Brain States", "Sleep Staging", "Epilepsy", "BCI"]
            panel_colors = [BLUE, PURPLE, RED, TEAL]
            title = Text(panel_titles[idx], font_size=18, weight="BOLD", color=WHITE)

            if idx == 0:
                brain = brain_asset(0.30, WHITE)
                w1 = tiny_wave(width=0.75, freq=2, amp=0.05, color=ORANGE)
                w2 = tiny_wave(width=0.75, freq=5, amp=0.05, color=TEAL)
                w3 = tiny_wave(width=0.75, freq=1, amp=0.05, color=PURPLE)
                waves = VGroup(w1, w2, w3).arrange(DOWN, buff=0.04)
                icon = VGroup(brain, waves).arrange(DOWN, buff=0.05)
                xs = np.linspace(-2.2, 2.2, 180)
                ys = 0.13 * np.sin(3.2 * xs) * (1 + 0.25 * xs)
                bottom_wave = make_wave_from_points(xs, ys, color=BLUE, stroke_width=2.5)
            elif idx == 1:
                moon = VGroup(
                    Circle(radius=0.17, fill_color=YELLOW, fill_opacity=1, stroke_width=0),
                    Circle(radius=0.18, fill_color=BACKGROUND, fill_opacity=1, stroke_width=0).shift(RIGHT * 0.08 + UP * 0.04),
                )
                face = VGroup(
                    Circle(radius=0.11, fill_color=WHITE, fill_opacity=0.35, stroke_color=WHITE, stroke_width=1.5),
                    Line(LEFT * 0.03 + UP * 0.04, RIGHT * 0.03 + UP * 0.04, color=WHITE, stroke_width=1.5),
                    Line(LEFT * 0.03 + DOWN * 0.04, RIGHT * 0.03 + DOWN * 0.04, color=WHITE, stroke_width=1.5),
                )
                icon = VGroup(moon, face).arrange(RIGHT, buff=0.15)
                x1 = np.linspace(-2.2, -0.4, 80)
                y1 = 0.19 * np.sin(1.0 * x1)
                x2 = np.linspace(-0.4, 0.4, 40)
                y2 = 0.28 * np.exp(-10 * (x2 - 0.05) ** 2) * np.sin(14 * x2)
                x3 = np.linspace(0.4, 2.2, 80)
                y3 = 0.10 * np.sin(1.0 * x3)
                xs = np.concatenate([x1, x2, x3])
                ys = np.concatenate([y1, y2, y3])
                bottom_wave = make_wave_from_points(xs, ys, color=PURPLE, stroke_width=2.5)
            elif idx == 2:
                brain = brain_asset(0.28, WHITE)
                bolt = Polygon(
                    [-0.05, 0.22, 0], [0.08, 0.02, 0], [0.0, 0.02, 0],
                    [0.18, -0.22, 0], [0.0, -0.06, 0], [-0.14, -0.06, 0],
                    [-0.02, 0.06, 0], [-0.05, 0.22, 0],
                    fill_color=YELLOW, fill_opacity=1, stroke_width=0,
                )
                icon = VGroup(brain, bolt).arrange(DOWN, buff=0.06)
                xs = np.linspace(-2.2, 2.2, 240)
                ys = 0.12 * np.sin(3 * xs)
                ys += 0.9 * np.exp(-25 * (xs - 0.1) ** 2)
                ys += -0.5 * np.exp(-4 * (xs - 0.3) ** 2)
                bottom_wave = make_wave_from_points(xs, ys, color=RED, stroke_width=2.5)
            else:
                brain = brain_asset(0.32, WHITE)
                screen = RoundedRectangle(width=0.45, height=0.3, corner_radius=0.04,
                                         fill_color=GREY_E, fill_opacity=0.8,
                                         stroke_color=WHITE, stroke_width=2)
                cursor = Polygon(
                    [0.05, 0.0, 0], [0.0, -0.04, 0], [0.1, -0.04, 0],
                    [0.1, 0.1, 0], fill_color=WHITE, fill_opacity=1, stroke_width=0,
                ).move_to(screen.get_center())
                device = VGroup(screen, cursor)
                arr = Arrow(LEFT, RIGHT, color=GREEN, stroke_width=3, buff=0.06,
                            max_tip_length_to_length_ratio=0.4)
                icon = VGroup(brain, arr, device).arrange(RIGHT, buff=0.12)
                xs = np.linspace(-2.2, 2.2, 240)
                ys = np.where(xs < 0, 0.18 * np.sin(5 * xs),
                              0.2 * np.sign(np.sin(7 * np.pi * (xs - 0.2))))
                bottom_wave = make_wave_from_points(xs, ys, color=TEAL, stroke_width=2.5)

            group = VGroup(title, icon, bottom_wave).arrange(DOWN, buff=0.06)
            max_h = 1.15
            max_w = 4.6
            scale_factor = min(max_h / group.height, max_w / group.width)
            group.scale(scale_factor)
            return group, panel_colors[idx]

        # ---------- initial previous-scene group ----------
        prev_labels = ["Signal Acquisition", "Signal Processing",
                       "Feature Extraction", "Classification"]
        prev_colors = [BLUE, TEAL, ORANGE, PURPLE]
        prev_blocks = VGroup()
        for lab, col in zip(prev_labels, prev_colors):
            rect = RoundedRectangle(width=2.0, height=0.65, corner_radius=0.08,
                                    fill_color=col, fill_opacity=0.25,
                                    stroke_color=col, stroke_width=2)
            txt = Text(lab, font_size=14, weight="BOLD", color=WHITE).scale_to_fit_width(1.7)
            txt.move_to(rect)
            prev_blocks.add(VGroup(rect, txt))
        prev_blocks.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.3)
        pattern_icon = SVGMobject(ASSET_PATHS["activity"]).set_color(YELLOW)
        pattern_icon.scale_to_fit_height(0.8)
        pattern_icon.next_to(prev_blocks, UP, buff=0.4)
        prev_group = VGroup(pattern_icon, prev_blocks)
        self.add(prev_group)

        # ---------- Beat 1 (0.00–2.44) ----------
        title_bar = RoundedRectangle(width=7.6, height=0.95, corner_radius=0.12,
                                     fill_color=GOLD, fill_opacity=0.12,
                                     stroke_color=GOLD, stroke_width=2).move_to(UP * 3.0)
        bci_group = VGroup(title_bar)
        self.play(FadeOut(prev_group), FadeIn(title_bar), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.44))

        # ---------- Beat 2 (2.44–5.88) ----------
        title_text = Text("Brain-Computer Interfaces", font_size=40, weight="BOLD", color=WHITE)
        title_text.scale_to_fit_width(title_bar.width - 0.5)
        title_text.move_to(title_bar)
        bci_group.add(title_text)

        thought_icon = make_thought_bubble_icon()
        device_small = RoundedRectangle(width=0.42, height=0.3, corner_radius=0.04,
                                        fill_color=BLUE, fill_opacity=0.8,
                                        stroke_color=WHITE, stroke_width=2)
        thought_arrow = Arrow(LEFT * 0.25, RIGHT * 0.25, color=ORANGE, stroke_width=2.5,
                              buff=0.04, max_tip_length_to_length_ratio=0.5)
        icon_thought_to_device = VGroup(thought_icon, thought_arrow, device_small).arrange(RIGHT, buff=0.12)
        icon_brain = brain_asset(0.55, WHITE)
        icon_hand = SVGMobject(ASSET_PATHS["hand"]).set_color(WHITE).scale_to_fit_height(0.55)
        icons_row = VGroup(icon_thought_to_device, icon_brain, icon_hand).arrange(RIGHT, buff=0.7)
        icons_row.move_to(DOWN * 1.4)

        eeg_wave_top = tiny_wave(width=2.4, freq=4, amp=0.12, color=TEAL, n=80)
        eeg_wave_top.next_to(icons_row, DOWN, buff=0.35)
        bci_group.add(icons_row, eeg_wave_top)

        self.play(Write(title_text), title_bar.animate.set_fill(GOLD, 0.28), run_time=max(0.05, 0.8))
        self.play(FadeIn(icons_row), run_time=max(0.05, 0.7))
        self.play(Create(eeg_wave_top), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.44))

        # gap (5.88 -> 6.64)
        self.wait(max(0.05, 0.76))

        # ---------- Beat 3 (6.64–10.82) ----------
        brain_left = brain_asset(0.85, WHITE)
        device_right = make_device()
        double_arrow = make_double_arrow()
        path_group = VGroup(brain_left, double_arrow, device_right).arrange(RIGHT, buff=0.5)
        path_group.move_to(DOWN * 0.35)
        bci_group.add(path_group)

        self.play(FadeIn(path_group), run_time=max(0.05, 0.9))
        for _ in range(3):
            self.play(double_arrow.animate.scale(1.14), run_time=max(0.05, 0.5))
            self.play(double_arrow.animate.scale(1 / 1.14), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.28))

        # ---------- Beat 4 (10.82–13.36) ----------
        label_brain = Text("Brain", font_size=16, weight="BOLD", color=WHITE)
        label_brain.next_to(brain_left, DOWN, buff=0.2)
        label_path = Text("Direct Communication Pathway", font_size=15, weight="BOLD", color=YELLOW)
        label_path.next_to(double_arrow, DOWN, buff=0.3)
        label_device = Text("External Device", font_size=16, weight="BOLD", color=WHITE)
        label_device.next_to(device_right, DOWN, buff=0.2)
        path_labels = VGroup(label_brain, label_path, label_device)
        bci_group.add(path_labels)

        self.play(Write(label_brain), run_time=max(0.05, 0.6))
        self.play(Write(label_path), run_time=max(0.05, 0.6))
        self.play(Write(label_device), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.74))

        # ---------- Beat 5 (13.36–18.50) ----------
        block_labels = ["Neural Signal Acquisition", "Signal Processing",
                        "Feature Extraction", "Machine Learning"]
        block_colors = [BLUE, TEAL, ORANGE, PURPLE]
        blocks = []
        for lab, col in zip(block_labels, block_colors):
            rect = RoundedRectangle(width=2.2, height=0.55, corner_radius=0.08,
                                    fill_color=col, fill_opacity=0.18,
                                    stroke_color=col, stroke_width=2)
            txt = Text(lab, font_size=13, weight="BOLD", color=WHITE).scale_to_fit_width(1.9)
            txt.move_to(rect)
            blocks.append(VGroup(rect, txt))
        block_group = VGroup(*blocks).arrange(RIGHT, buff=0.5)
        block_group.scale_to_fit_width(11.5)
        block_group.next_to(path_labels, DOWN, buff=0.4)
        block_arrows = []
        for i in range(3):
            arr = Arrow(blocks[i].get_right(), blocks[i + 1].get_left(),
                        color=GREY_B, stroke_width=2, buff=0.12,
                        max_tip_length_to_length_ratio=0.35)
            block_arrows.append(arr)
        flow_group = VGroup(block_group, *block_arrows)
        bci_group.add(flow_group)

        per_block = 5.14 / 4
        for i in range(4):
            self.play(FadeIn(blocks[i]), run_time=max(0.05, 0.36))
            self.play(Indicate(blocks[i], color=block_colors[i], scale_factor=1.08),
                      run_time=max(0.05, 0.26))
            if i < 3:
                self.play(Create(block_arrows[i]), run_time=max(0.05, 0.26))
                self.wait(max(0.05, 0.405))
            else:
                self.wait(max(0.05, 0.665))

        # gap (18.50 -> 19.32)
        self.wait(max(0.05, 0.82))

        # ---------- Beat 6 (19.32–26.66) ----------
        main_bci_group = VGroup(path_group, path_labels, flow_group)
        self.play(main_bci_group.animate.shift(UP * 0.5), run_time=max(0.05, 0.7))

        tag_data = [
            ("Assistive Communication", BLUE, make_speech_bubble_icon()),
            ("Rehabilitation", TEAL, make_walking_icon()),
            ("Prosthetic Control", ORANGE, make_prosthetic_icon()),
            ("Neuroscience Research", PINK, make_flask_icon()),
        ]
        tag_group = VGroup()
        for text_str, col, icon in tag_data:
            rect = RoundedRectangle(width=3.0, height=0.8, corner_radius=0.12,
                                    fill_color=col, fill_opacity=0.18,
                                    stroke_color=col, stroke_width=2)
            txt = Text(text_str, font_size=14, weight="BOLD", color=WHITE).scale_to_fit_width(1.75)
            content = VGroup(icon, txt).arrange(RIGHT, buff=0.1)
            content.move_to(rect)
            tag = VGroup(rect, content)
            tag_group.add(tag)
        tag_group.arrange(RIGHT, buff=0.35)
        tag_group.scale_to_fit_width(12.4)
        tag_group.next_to(flow_group, DOWN, buff=0.35)
        bci_group.add(tag_group)

        per_tag = (7.34 - 0.7) / 4
        for tag in tag_group:
            self.play(GrowFromCenter(tag), run_time=max(0.05, 0.46))
            self.play(tag.animate.scale(1.07), run_time=max(0.05, 0.20))
            self.play(tag.animate.scale(1 / 1.07), run_time=max(0.05, 0.20))
            self.wait(max(0.05, 0.80))

        # gap (26.66 -> 27.50)
        self.wait(max(0.05, 0.84))

        # ---------- Beat 7 (27.50–29.30) ----------
        grid_rect = Rectangle(width=12.4, height=4.0, color=GREY_B, stroke_width=1.5)
        vline = Line(UP * 2.0, DOWN * 2.0, color=GREY_B, stroke_width=1.5, stroke_opacity=0.7)
        hline = Line(LEFT * 6.2, RIGHT * 6.2, color=GREY_B, stroke_width=1.5, stroke_opacity=0.7)
        grid_outer = VGroup(grid_rect, vline, hline)
        grid_outer.move_to(ORIGIN)

        self.play(FadeOut(bci_group), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.2))
        self.play(FadeIn(grid_outer), run_time=max(0.05, 0.4))

        # gap (29.30 -> 30.30)
        self.wait(max(0.05, 1.00))

        # ---------- Beat 8 (30.30–34.94) ----------
        panel_w = 5.4
        panel_h = 1.5
        panel_centers = [(-3.0, 0.85, 0), (3.0, 0.85, 0), (-3.0, -0.85, 0), (3.0, -0.85, 0)]
        panel_frames = []
        for cen in panel_centers:
            fr = RoundedRectangle(width=panel_w, height=panel_h, corner_radius=0.08,
                                  stroke_color=GREY_B, stroke_width=1.5,
                                  fill_color=GREY_E, fill_opacity=0.03)
            fr.move_to(cen)
            panel_frames.append(fr)
        panel_frame_group = VGroup(*panel_frames)

        self.play(FadeIn(panel_frame_group), run_time=max(0.05, 0.5))
        recap_header = Text("Four Major Applications", font_size=28, weight="BOLD", color=WHITE)
        recap_header.move_to(UP * 2.8)
        self.play(Write(recap_header), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 3.14))

        # gap (34.94 -> 35.80)
        self.wait(max(0.05, 0.86))

        # ---------- Beats 9–12: fill panels ----------
        panel_durations = [4.36, 5.72, 6.28, 5.93]
        panel_colors_final = [BLUE, PURPLE, RED, TEAL]
        gaps_between = [0.50, 0.54, 0.65]

        for i, dur in enumerate(panel_durations):
            if i > 0:
                self.wait(max(0.05, gaps_between[i - 1]))

            content, col = make_panel_content(i)
            content.move_to(panel_frames[i].get_center())
            self.play(
                FadeIn(content),
                panel_frames[i].animate.set_stroke(col, width=3),
                panel_frames[i].animate.set_fill(col, 0.12),
                run_time=max(0.05, dur * 0.5)
            )
            self.play(Indicate(panel_frames[i], color=col, scale_factor=1.03),
                      run_time=max(0.05, dur * 0.15))
            self.wait(max(0.05, dur * 0.35))

        # gap (59.78 -> 60.92)
        self.wait(max(0.05, 1.14))

        # ---------- Beat 13 (60.92–63.32) ----------
        dividing_lines = VGroup(vline, hline)
        self.play(dividing_lines.animate.set_stroke(YELLOW, width=3), run_time=max(0.05, 0.6))
        self.play(dividing_lines.animate.set_stroke(GREY_B, width=1.5), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.2))

        # gap (63.32 -> 63.82)
        self.wait(max(0.05, 0.50))

        # ---------- Beat 14 (63.82–68.78) ----------
        band_rect = Rectangle(width=12.2, height=1.4, fill_color="#1C1F26", fill_opacity=0.5,
                              stroke_color=GREY_B, stroke_width=1).move_to(DOWN * 2.8)
        slot_rects = []
        for _ in range(5):
            slot = RoundedRectangle(width=2.0, height=0.85, corner_radius=0.08,
                                    stroke_color=GREY_B, stroke_width=1.5,
                                    fill_color=GREY_E, fill_opacity=0.1)
            slot_rects.append(slot)
        slot_group = VGroup(*slot_rects).arrange(RIGHT, buff=0.3)
        slot_group.move_to(band_rect.get_center())

        tech_labels = ["Filtering", "Spectral Analysis", "Time-Frequency Analysis",
                       "Feature Extraction", "Classification"]
        tech_fills = []

        def make_tech_icon(idx):
            if idx == 0:
                noisy = tiny_wave(width=0.6, freq=9, amp=0.08, color=ORANGE, n=40).shift(LEFT * 0.45)
                funnel = VGroup(
                    Polygon([-0.18, 0.24, 0], [0.18, 0.24, 0],
                            [0.07, -0.2, 0], [-0.07, -0.2, 0],
                            fill_color=GREY_B, fill_opacity=0.8,
                            stroke_color=WHITE, stroke_width=1.5),
                    Rectangle(width=0.14, height=0.18, fill_color=GREY_B,
                              fill_opacity=0.8, stroke_color=WHITE, stroke_width=1.5).move_to(DOWN * 0.27)
                )
                smooth = tiny_wave(width=0.6, freq=1.5, amp=0.06, color=GREEN, n=40).shift(RIGHT * 0.45)
                group = VGroup(noisy, funnel, smooth).arrange(RIGHT, buff=0.05)
                group.scale_to_fit_height(0.4)
                return group
            elif idx == 1:
                wave = tiny_wave(width=1.0, freq=3.0, amp=0.06, color=WHITE, n=40)
                bars = VGroup()
                heights = [0.32, 0.55, 0.2, 0.45, 0.25]
                colors = [TEAL, ORANGE, PURPLE, PINK, BLUE]
                for h, c in zip(heights, colors):
                    b = Rectangle(width=0.1, height=h, fill_color=c, fill_opacity=0.9,
                                  stroke_width=0)
                    bars.add(b)
                bars.arrange(RIGHT, buff=0.06)
                group = VGroup(wave, bars).arrange(DOWN, buff=0.05)
                group.scale_to_fit_height(0.4)
                return group
            elif idx == 2:
                cells = VGroup()
                for r in range(4):
                    row = VGroup()
                    for c in range(5):
                        t = (r + c) / 8.0
                        color = interpolate_color(TEAL, PURPLE, t)
                        sq = Square(side_length=0.14, fill_color=color, fill_opacity=0.9,
                                    stroke_width=0.4, stroke_color=WHITE)
                        row.add(sq)
                    row.arrange(RIGHT, buff=0.04)
                    cells.add(row)
                cells.arrange(DOWN, buff=0.04)
                cells.scale_to_fit_height(0.4)
                freq_label = Text("f", font_size=10, color=WHITE).scale_to_fit_height(0.12)
                time_label = Text("t", font_size=10, color=WHITE).scale_to_fit_height(0.12)
                freq_label.next_to(cells, LEFT, buff=0.08)
                time_label.next_to(cells, DOWN, buff=0.08)
                return VGroup(cells, freq_label, time_label)
            elif idx == 3:
                xs = np.linspace(-0.8, 0.0, 60)
                ys = 0.08 * np.sin(8 * xs)
                wave = make_wave_from_points(xs, ys, color=WHITE, stroke_width=2)
                pts = [np.array([-0.6, 0.04, 0]), np.array([-0.4, -0.05, 0]), np.array([-0.2, 0.06, 0])]
                dots = VGroup(*[Dot(p, radius=0.03, color=YELLOW) for p in pts])
                brackets = VGroup(*[
                    SurroundingRectangle(d, color=YELLOW, buff=0.04, corner_radius=0.02).scale(0.7)
                    for d in dots
                ])
                list_rect = RoundedRectangle(width=0.2, height=0.32, corner_radius=0.04,
                                            fill_color=GREY_E, fill_opacity=0.8,
                                            stroke_color=WHITE, stroke_width=1.5).shift(RIGHT * 0.45)
                lines = VGroup(*[
                    Line(LEFT * 0.06, RIGHT * 0.06, color=WHITE, stroke_width=1.5)
                    for _ in range(3)
                ]).arrange(DOWN, buff=0.08).move_to(list_rect)
                arrow = Arrow(LEFT * 0.1, RIGHT * 0.1, color=ORANGE, stroke_width=2,
                              buff=0.03, max_tip_length_to_length_ratio=0.4).next_to(list_rect, LEFT, buff=0.08)
                group = VGroup(wave, dots, brackets, arrow, list_rect, lines)
                group.scale_to_fit_height(0.4)
                return group
            else:
                in_dots = VGroup(*[Dot(np.array([-0.6, y, 0]), radius=0.04, color=TEAL)
                                   for y in [-0.15, 0.0, 0.15]])
                mid1 = Dot(np.array([-0.2, 0.2, 0]), radius=0.05, color=ORANGE)
                mid2 = Dot(np.array([-0.2, -0.2, 0]), radius=0.05, color=ORANGE)
                out = RoundedRectangle(width=0.3, height=0.22, corner_radius=0.04,
                                      fill_color=GREEN, fill_opacity=0.8,
                                      stroke_color=WHITE, stroke_width=1.5).shift(RIGHT * 0.4)
                out_label = Text("C", font_size=10, weight="BOLD", color=WHITE).move_to(out)
                paths = VGroup()
                paths.add(Line(in_dots[0].get_center(), mid1.get_center(), color=GREY_B, stroke_width=1.5))
                paths.add(Line(in_dots[1].get_center(), mid1.get_center(), color=GREY_B, stroke_width=1.5))
                paths.add(Line(in_dots[2].get_center(), mid2.get_center(), color=GREY_B, stroke_width=1.5))
                paths.add(Line(mid1.get_center(), out.get_left(), color=GREY_B, stroke_width=1.5))
                paths.add(Line(mid2.get_center(), out.get_left(), color=GREY_B, stroke_width=1.5))
                group = VGroup(in_dots, mid1, mid2, paths, VGroup(out, out_label))
                group.scale_to_fit_height(0.4)
                return group

        self.play(FadeIn(band_rect), FadeIn(slot_group), run_time=max(0.05, 1.2))

        # pre-create invisible slot fills
        for i, (slot, lab) in enumerate(zip(slot_rects, tech_labels)):
            icon = make_tech_icon(i)
            icon.scale_to_fit_height(0.28)
            label = Text(lab, font_size=11, weight="BOLD", color=WHITE)
            label.scale_to_fit_width(slot.width - 0.25)
            fill_content = VGroup(icon, label).arrange(DOWN, buff=0.06)
            fill_content.move_to(slot)
            fill_content.set_opacity(0)
            tech_fills.append(fill_content)
            self.add(fill_content)

        self.wait(max(0.05, 3.76))

        # gap (68.78 -> 69.34)
        self.wait(max(0.05, 0.56))

        # ---------- Beats 15–19: fill technique slots ----------
        fill_durations = [0.98, 0.80, 0.94, 0.32, 0.48]
        fill_gaps_before = [0.0, 0.46, 0.88, 0.98, 0.82]

        for i, dur in enumerate(fill_durations):
            if i > 0:
                self.wait(max(0.05, fill_gaps_before[i]))
            self.play(tech_fills[i].animate.set_opacity(1),
                      run_time=max(0.05, dur * 0.6))
            self.wait(max(0.05, dur * 0.4))

        # ---------- Beat 20 (76.00–77.05) ----------
        connectors = VGroup()
        for slot in slot_rects:
            start_point = slot.get_top() + UP * 0.05
            for fr in panel_frames:
                end_point = fr.get_bottom()
                line = Line(start_point, end_point, color=GREY_B, stroke_width=1.1,
                            stroke_opacity=0.35)
                connectors.add(line)
        self.play(Create(connectors), run_time=max(0.05, 1.05))