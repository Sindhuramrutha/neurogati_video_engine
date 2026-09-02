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
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        wave = self.make_smooth_wave()
        gate = self.make_filter_gate()
        previous_visual = VGroup(wave, gate)

        previous_caption = Text(
            "Neural Signal Processing", font_size=28, color=YELLOW
        ).to_edge(DOWN, buff=0.4)

        self.add(previous_visual, previous_caption)

        title = Text("Learning Objectives", font_size=44, color=WHITE)
        title.to_edge(UP, buff=0.55)

        self.play(
            previous_visual.animate.set_opacity(0.35),
            previous_caption.animate.set_opacity(0.35),
            FadeIn(title),
            run_time=max(0.05, 1.22),
        )
        self.wait(max(0.05, 0.56))

        badge_texts = [
            "Define a low-pass filter",
            "Explain its operating principle.",
            "Describe the cutoff frequency.",
            "Identify situations where low-pass filtering is useful.",
            "Understand both its advantages and its limitations.",
        ]

        y_positions = [1.7, 0.82, -0.06, -0.94, -1.82]
        badges = []

        badge1 = self.make_badge(badge_texts[0])
        badge1.move_to(np.array([-9, y_positions[0], 0])).set_opacity(0)
        self.play(
            FadeOut(previous_visual),
            FadeOut(previous_caption),
            badge1.animate.set_opacity(1).move_to(np.array([0, y_positions[0], 0])),
            run_time=max(0.05, 1.96),
        )
        badges.append(badge1)
        self.wait(max(0.05, 0.72))

        badge2 = self.make_badge(badge_texts[1])
        badge2.move_to(np.array([-9, y_positions[1], 0])).set_opacity(0)
        self.play(
            badge2.animate.set_opacity(1).move_to(np.array([0, y_positions[1], 0])),
            run_time=max(0.05, 1.66),
        )
        badges.append(badge2)
        self.wait(max(0.05, 0.46))

        badge3 = self.make_badge(badge_texts[2])
        badge3.move_to(np.array([-9, y_positions[2], 0])).set_opacity(0)
        self.play(
            badge3.animate.set_opacity(1).move_to(np.array([0, y_positions[2], 0])),
            run_time=max(0.05, 1.32),
        )
        badges.append(badge3)
        self.wait(max(0.05, 0.86))

        badge4 = self.make_badge(badge_texts[3])
        badge4.move_to(np.array([-9, y_positions[3], 0])).set_opacity(0)
        self.play(
            badge4.animate.set_opacity(1).move_to(np.array([0, y_positions[3], 0])),
            run_time=max(0.05, 2.76),
        )
        badges.append(badge4)
        self.wait(max(0.05, 0.90))

        badge5 = self.make_badge(badge_texts[4])
        badge5.move_to(np.array([-9, y_positions[4], 0])).set_opacity(0)
        self.play(
            badge5.animate.set_opacity(1).move_to(np.array([0, y_positions[4], 0])),
            run_time=max(0.05, 2.32),
        )
        badges.append(badge5)

        sweep_rect = RoundedRectangle(
            width=badges[0][0].width + 0.12,
            height=badges[0][0].height + 0.12,
            corner_radius=0.22,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.12,
        )
        sweep_rect.move_to(badges[0].get_center())
        sweep_rect.set_opacity(0)
        self.add(sweep_rect)

        self.play(
            sweep_rect.animate.set_opacity(1).move_to(badges[1].get_center()),
            run_time=max(0.05, 0.28),
        )
        self.play(
            sweep_rect.animate.move_to(badges[4].get_center()),
            run_time=max(0.05, 1.0),
        )
        self.play(FadeOut(sweep_rect), run_time=max(0.05, 0.13))

    def make_badge(self, text_str):
        rect = RoundedRectangle(
            width=7.8,
            height=0.8,
            corner_radius=0.2,
            fill_color=BLUE,
            fill_opacity=0.17,
            stroke_color=BLUE,
            stroke_width=2,
        )

        check = SVGMobject(
            ASSET_PATHS["check_circle"],
            height=0.42,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=0,
        )
        check.set_color(GREEN)

        label = Text(text_str, font_size=28, color=WHITE)
        label.scale_to_fit_width(6.2)

        content = VGroup(check, label).arrange(RIGHT, buff=0.22)
        content.next_to(rect.get_left(), RIGHT, buff=0.35)

        return VGroup(rect, content)

    def make_smooth_wave(self):
        xs = np.linspace(-6.2, 6.2, 220)
        ys = 0.55 * np.sin(0.6 * xs) + 0.10 * np.sin(0.3 * xs - 0.7) - 1.15
        zs = np.zeros_like(xs)
        points = np.column_stack((xs, ys, zs))

        wave = VMobject(stroke_color=TEAL, stroke_width=5, fill_opacity=0)
        wave.set_points_as_corners(points)
        return wave

    def make_filter_gate(self):
        top = Line(
            LEFT * 1.1 + UP * 1.3,
            RIGHT * 1.1 + UP * 1.3,
            color=BLUE,
            stroke_width=8,
        )
        left = Line(
            LEFT * 1.1 + DOWN * 1.3,
            LEFT * 1.1 + UP * 1.3,
            color=BLUE,
            stroke_width=8,
        )
        right = Line(
            RIGHT * 1.1 + DOWN * 1.3,
            RIGHT * 1.1 + UP * 1.3,
            color=BLUE,
            stroke_width=8,
        )

        slats = VGroup(
            *[
                Line(
                    LEFT * 0.95 + UP * y,
                    RIGHT * 0.95 + UP * y,
                    color=BLUE,
                    stroke_width=5,
                )
                for y in [-0.8, -0.4, 0.0, 0.4, 0.8, 1.1]
            ]
        )

        return VGroup(top, left, right, slats).move_to(np.array([0, 0.9, 0]))