ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def make_shield_icon(self, color=GREEN, height=0.45):
        shield = Polygon(
            np.array([-0.45, 0.32, 0]),
            np.array([0.45, 0.32, 0]),
            np.array([0.45, -0.12, 0]),
            np.array([0.28, -0.12, 0]),
            np.array([0.00, -0.60, 0]),
            np.array([-0.28, -0.12, 0]),
            np.array([-0.45, -0.12, 0]),
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=3,
        )
        shield.scale_to_fit_height(height)
        return shield

    def make_magnifier_icon(self, height=0.45):
        cable = VMobject().set_stroke(color=GREY_B, width=4)
        pts = []
        for i in range(15):
            x = -0.55 + 0.15 * i
            y = 0.10 * np.sin(2 * PI * 2.0 * i / 14)
            pts.append(np.array([x, y, 0]))
        cable.set_points_as_corners(pts)

        lens = Circle(
            radius=0.22,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.25,
        )
        handle = Line(
            lens.get_edge_center(RIGHT) + RIGHT * 0.02,
            lens.get_edge_center(RIGHT) + RIGHT * 0.28 + UP * 0.14,
            color=WHITE,
            stroke_width=4,
        )
        glass = VGroup(lens, handle)
        glass.move_to(np.array([0.25, 0.06, 0]))

        icon = VGroup(cable, glass)
        icon.scale_to_fit_height(height)
        return icon

    def make_ground_icon(self, height=0.45):
        vertical = Line(ORIGIN, DOWN * 0.35, color=WHITE, stroke_width=3)
        h1 = Line(LEFT * 0.30 + DOWN * 0.35, RIGHT * 0.30 + DOWN * 0.35, color=WHITE, stroke_width=3)
        h2 = Line(LEFT * 0.18 + DOWN * 0.48, RIGHT * 0.18 + DOWN * 0.48, color=WHITE, stroke_width=3)
        h3 = Line(LEFT * 0.08 + DOWN * 0.61, RIGHT * 0.08 + DOWN * 0.61, color=WHITE, stroke_width=3)
        icon = VGroup(vertical, h1, h2, h3)
        icon.scale_to_fit_height(height)
        return icon

    def make_cross_icon(self, height=0.45):
        v = RoundedRectangle(
            corner_radius=0.04,
            width=0.16,
            height=0.50,
            fill_color=RED,
            fill_opacity=1,
            stroke_width=0,
        )
        h = RoundedRectangle(
            corner_radius=0.04,
            width=0.50,
            height=0.16,
            fill_color=RED,
            fill_opacity=1,
            stroke_width=0,
        )
        icon = VGroup(v, h)
        icon.scale_to_fit_height(height)
        return icon

    def make_clipboard_icon(self, height=0.45):
        board = RoundedRectangle(
            corner_radius=0.08,
            width=0.45,
            height=0.55,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        clip = Rectangle(
            width=0.18,
            height=0.10,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        clip.move_to(board.get_top() + DOWN * 0.08)

        line1 = Line(
            board.get_left() + RIGHT * 0.10,
            board.get_right() + LEFT * 0.10,
            color=WHITE,
            stroke_width=1.5,
        )
        line1.move_to(board.get_center() + UP * 0.04)
        line2 = Line(
            board.get_left() + RIGHT * 0.10,
            board.get_right() + LEFT * 0.10,
            color=WHITE,
            stroke_width=1.5,
        )
        line2.move_to(board.get_center() + DOWN * 0.13)

        icon = VGroup(board, clip, line1, line2)
        icon.scale_to_fit_height(height)
        return icon

    def make_checkmark(self, color=GREEN, height=0.30):
        check1 = Line(LEFT * 0.10 + DOWN * 0.02, ORIGIN + UP * 0.04, color=color, stroke_width=5)
        check2 = Line(ORIGIN + UP * 0.04, RIGHT * 0.16 + DOWN * 0.10, color=color, stroke_width=5)
        check = VGroup(check1, check2)
        check.scale_to_fit_height(height)
        return check

    def build_row(self, icon, text_str, target_y):
        text = Text(text_str, font_size=20, color=WHITE)
        if text.width > 4.6:
            text.scale_to_fit_width(4.6)

        group = VGroup(icon, text).arrange(RIGHT, buff=0.35)
        group.move_to(np.array([0, target_y, 0]))
        final_pos = group.get_center()
        group.shift(LEFT * 8)
        return group, final_pos, text

    def build_chain(self):
        labels = ["Participant", "Electrodes", "Isolation", "Acquisition", "Computer"]
        colors = [TEAL, TEAL, GOLD, PURPLE, PURPLE]

        box_groups = []
        for label, fill in zip(labels, colors):
            box = RoundedRectangle(
                corner_radius=0.08,
                width=1.50,
                height=0.55,
                fill_color=fill,
                fill_opacity=0.15,
                stroke_color=fill,
                stroke_width=1.5,
            )
            txt = Text(label, font_size=14, color=WHITE)
            txt.scale_to_fit_width(box.width - 0.25)
            txt.move_to(box.get_center())
            box_groups.append(VGroup(box, txt))

        chain_boxes = VGroup(*box_groups).arrange(RIGHT, buff=0.30)
        chain_arrows = VGroup()
        for i in range(len(chain_boxes) - 1):
            left = chain_boxes[i]
            right = chain_boxes[i + 1]
            arrow = Arrow(
                left.get_right() + RIGHT * 0.05,
                right.get_left() + LEFT * 0.05,
                stroke_width=3,
                color=GREY,
                max_tip_length_to_length_ratio=0.25,
                buff=0.05,
            )
            chain_arrows.add(arrow)

        chain = VGroup(chain_boxes, chain_arrows)
        chain.scale_to_fit_width(8.0)
        return chain

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Beat 1: 0.00-4.30 ----
        panel = RoundedRectangle(
            corner_radius=0.18,
            width=8.6,
            height=6.6,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_color=GREY_B,
            stroke_width=2,
        )
        panel.move_to(UP * 0.1)

        header = Text("Safety Practices", font_size=34, color=GREY_B)
        header.move_to(panel.get_top() + DOWN * 0.55)

        row_y = [1.25, 0.35, -0.55, -1.45, -2.35]

        blank_line = Line(
            panel.get_left() + RIGHT * 0.5,
            panel.get_right() + LEFT * 0.5,
            color=GREY,
            stroke_width=3,
            stroke_opacity=0.5,
        )
        blank_line.move_to(np.array([0, row_y[0], 0]))

        self.play(FadeIn(panel), run_time=max(0.05, 1.0))
        self.play(Write(header), run_time=max(0.05, 1.2))
        self.play(FadeIn(blank_line), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.3))  # Beat 1 total 4.30

        # ---- Beat 2: 4.30-8.36 ----
        subtitle = Text("throughout the entire acquisition chain", font_size=24, color=WHITE)
        subtitle.next_to(header, DOWN, buff=0.35)

        chain = self.build_chain()
        chain.move_to(np.array([0, -3.15, 0]))
        chain.set_opacity(0.35)

        self.play(header.animate.set_color(WHITE), run_time=max(0.05, 0.7))
        self.play(FadeIn(subtitle), run_time=max(0.05, 0.6))
        self.play(FadeIn(chain), run_time=max(0.05, 1.0))
        self.play(chain.animate.set_opacity(0.15), run_time=max(0.05, 0.76))
        self.wait(max(0.05, 1.0))  # Beat 2 total 4.06

        # Gap before Beat 3
        self.wait(max(0.05, 0.94))

        # ---- Rows: Beats 3-7 ----
        row_texts = [
            "Electrically isolated recording equipment",
            "Inspect electrodes and connecting cables before every use",
            "Ensure proper grounding of the recording system",
            "Equipment designed for biomedical applications",
            "Follow established laboratory or clinical safety procedures",
        ]
        icon_builders = [
            self.make_shield_icon,
            self.make_magnifier_icon,
            self.make_ground_icon,
            self.make_cross_icon,
            self.make_clipboard_icon,
        ]
        durations = [4.42, 3.28, 3.08, 3.24, 3.34]
        slide_times = [1.2, 0.8, 0.7, 0.7, 0.7]
        create_times = [1.0, 1.0, 1.0, 1.0, 1.0]
        gaps_between = [0.56, 0.60, 0.84, 0.84]

        row_groups = []
        check_marks = []
        first_row_icon = None

        for i in range(5):
            icon = icon_builders[i](height=0.45)
            row_group, final_pos, text = self.build_row(icon, row_texts[i], row_y[i])

            if i == 0:
                first_row_icon = icon

            self.add(row_group)

            if i == 0:
                self.play(FadeOut(blank_line), row_group.animate.move_to(final_pos), run_time=max(0.05, slide_times[i]))
            else:
                self.play(row_group.animate.move_to(final_pos), run_time=max(0.05, slide_times[i]))

            check = self.make_checkmark(GREEN, 0.32)
            check.move_to(np.array([text.get_right()[0] + 0.32, text.get_center()[1], 0]))

            self.play(Create(check), run_time=max(0.05, create_times[i]))
            row_group.add(check)

            row_groups.append(row_group)
            check_marks.append(check)

            self.play(check.animate.scale(1.2), run_time=max(0.05, 0.15))
            self.play(check.animate.scale(1 / 1.2), run_time=max(0.05, 0.15))

            wait_time = durations[i] - (slide_times[i] + create_times[i] + 0.30)
            self.wait(max(0.05, wait_time))

            if i < 4:
                self.wait(max(0.05, gaps_between[i]))

        # Gap before Beat 8
        self.wait(max(0.05, 0.88))

        rows_grp = VGroup(*row_groups)

        # ---- Beat 8: 30.38-37.22 ----
        caption1 = Text("reduces electrical hazards", font_size=18, color=GREEN)
        caption2 = Text("supports reliable signal acquisition", font_size=18, color=GREEN)
        captions = VGroup(caption1, caption2).arrange(DOWN, buff=0.18).scale_to_fit_width(1.9)
        captions.next_to(panel, RIGHT, buff=0.35)

        for row in row_groups:
            self.play(Indicate(row, color=YELLOW, scale_factor=1.05), run_time=max(0.05, 0.65))

        self.play(FadeIn(captions), run_time=max(0.05, 0.8))
        self.play(*[check.animate.scale(1.15) for check in check_marks], run_time=max(0.05, 0.4))
        self.play(*[check.animate.scale(1 / 1.15) for check in check_marks], run_time=max(0.05, 0.4))
        self.wait(max(0.05, 1.99))  # Beat 8 total 6.84

        # ---- Beat 9: 38.30-43.98 ----
        large_title = Text("High-quality recordings", font_size=38, color=WHITE)
        large_title.move_to(np.array([0, 2.40, 0]))

        warning_phrase = Text("at the expense of participant safety", font_size=24, color=RED)
        warning_phrase.next_to(large_title, DOWN, buff=0.35)

        slash = Line(
            warning_phrase.get_left() + UP * 0.15 + LEFT * 0.10,
            warning_phrase.get_right() + DOWN * 0.15 + RIGHT * 0.10,
            color=RED,
            stroke_width=6,
        )
        warning_group = VGroup(large_title, warning_phrase, slash)

        self.play(
            FadeOut(captions),
            panel.animate.set_opacity(0.20),
            header.animate.set_opacity(0.35),
            subtitle.animate.set_opacity(0.25),
            chain.animate.set_opacity(0.08),
            rows_grp.animate.set_opacity(0.30),
            run_time=max(0.05, 0.75),
        )
        self.play(Write(large_title), run_time=max(0.05, 0.70))
        self.play(FadeIn(warning_phrase), Create(slash), run_time=max(0.05, 0.80))
        self.play(
            first_row_icon.animate.set_fill(YELLOW, opacity=1).set_stroke(WHITE, width=4),
            run_time=max(0.05, 0.40),
        )
        self.play(first_row_icon.animate.scale(1.25), run_time=max(0.05, 0.30))
        self.play(first_row_icon.animate.scale(1 / 1.25), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 2.43))  # Beat 9 total 5.68

        # ---- Beat 10: 44.78-50.83 ----
        banner_bg = Rectangle(
            width=14,
            height=1.7,
            fill_color=GOLD,
            fill_opacity=0.96,
            stroke_width=0,
        )
        banner_text = Text("Participant safety is the first priority.", font_size=31, color=BLACK)
        banner_shield = self.make_shield_icon(GREEN, height=0.8)
        banner_shield.set_fill(GREEN, opacity=1)
        banner_shield.set_stroke(BLACK, width=2)

        banner_content = VGroup(banner_shield, banner_text).arrange(RIGHT, buff=0.5)
        banner_bg.move_to(np.array([0, -2.40, 0]))
        banner_content.move_to(banner_bg.get_center())

        banner = VGroup(banner_bg, banner_content)
        banner.move_to(np.array([0, -2.40, 0]))
        banner.shift(DOWN * 8)
        self.add(banner)

        self.play(FadeOut(warning_group), run_time=max(0.05, 0.5))
        self.play(
            rows_grp.animate.set_opacity(0.22),
            panel.animate.set_opacity(0.15),
            header.animate.set_opacity(0.20),
            subtitle.animate.set_opacity(0.18),
            chain.animate.set_opacity(0.04),
            run_time=max(0.05, 0.5),
        )
        self.play(banner.animate.shift(UP * 8), run_time=max(0.05, 0.8))

        self.play(banner_shield.animate.scale(1.25), run_time=max(0.05, 0.35))
        self.play(banner_shield.animate.scale(1 / 1.25), run_time=max(0.05, 0.35))
        self.play(banner_shield.animate.set_fill(WHITE, opacity=0.9), run_time=max(0.05, 0.5))
        self.play(banner_shield.animate.set_fill(GREEN, opacity=1), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.05))  # Beat 10 total 6.05