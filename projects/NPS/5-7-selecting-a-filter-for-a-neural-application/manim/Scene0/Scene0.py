ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- Beat 1: noisy trace + orbiting filter icons ----------
        trace_group = self.make_noisy_trace()
        trace_group.set_z_index(0)

        icons, icon_group = self.make_filter_icons()

        self.play(FadeIn(trace_group), run_time=max(0.05, 0.8))
        self.play(FadeIn(icon_group), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 1.74))  # total beat 1 = 3.44

        # ---------- Beats 2-7: pulse each icon ----------
        durations = [0.84, 0.62, 0.74, 0.38, 0.90, 4.10]
        for icon, dur in zip(icons, durations):
            self.pulse_icon(icon, dur)

        # ---------- Beat 8: icons leave, big ? appears over trace ----------
        question = Text("?", font_size=230, weight="BOLD", color=YELLOW)
        question.move_to(ORIGIN)
        question.set_z_index(2)

        self.play(
            FadeOut(icon_group, run_time=max(0.05, 0.5)),
            FadeIn(question, run_time=max(0.05, 0.5)),
        )
        self.wait(max(0.05, 6.82))  # beat 8 total = 7.32

        # ---------- Beat 9: ? becomes header; trace fades ----------
        header_text = Text(
            "Choose filter based on signal & analysis objective",
            font_size=32,
            weight="BOLD",
            color=WHITE,
        )
        header_text.scale_to_fit_width(11.5)
        header_text.move_to(ORIGIN)
        header_text.set_z_index(2)

        self.play(ReplacementTransform(question, header_text), run_time=max(0.05, 1.0))
        self.play(
            header_text.animate.to_edge(UP, buff=0.5),
            FadeOut(trace_group),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 10.78))  # beat 9 total = 12.78

        # ---------- Beat 10: split view ----------
        left_group, left_icon = self.make_clean_signal_icon()
        right_group, right_icon = self.make_noise_icon()
        filter_node = self.make_filter_node()

        left_group.move_to(LEFT * 4.4 + DOWN * 0.9)
        right_group.move_to(RIGHT * 4.4 + DOWN * 0.9)
        filter_node.move_to(DOWN * 0.9)

        arrow_left = Arrow(
            left_icon.get_right() + RIGHT * 0.1,
            filter_node.get_left() + LEFT * 0.1,
            buff=0.1,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.16,
        )
        arrow_right = Arrow(
            right_icon.get_left() + LEFT * 0.1,
            filter_node.get_right() + RIGHT * 0.1,
            buff=0.1,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.16,
        )

        self.play(
            FadeIn(left_group),
            FadeIn(right_group),
            FadeIn(filter_node),
            Create(arrow_left),
            Create(arrow_right),
            run_time=max(0.05, 1.0),
        )

        self.wait(max(0.05, 7.52))  # beat 10 total = 8.52
        self.wait(max(0.05, 0.78))  # beat 11: static to end

    # ------------------------------------------------------------------
    def make_noisy_trace(self):
        rng = np.random.default_rng(5)
        n = 260
        x = np.linspace(-3.0, 3.0, n)

        # Slow random fluctuation + faster oscillatory texture = raw neural-ish trace
        noise = rng.normal(0.0, 0.11, n)
        for i in range(1, n):
            noise[i] = noise[i - 1] * 0.62 + noise[i] * 0.38

        y = 0.16 * np.sin(2 * PI * 1.7 * x) + noise
        y -= np.mean(y)
        y = y / np.max(np.abs(y)) * 0.9

        points = np.array([x, y, np.zeros(n)]).T
        trace = VMobject().set_points_as_corners(points)
        trace.set_stroke(TEAL, width=2.5)

        baseline = Line(
            LEFT * 3.2, RIGHT * 3.2,
            color=GREY,
            stroke_width=1.0,
            stroke_opacity=0.35,
        )

        return VGroup(baseline, trace)

    def regular_polygon(self, n, radius, color, start_angle=PI / 2):
        vertices = []
        for k in range(n):
            ang = start_angle + k * 2 * PI / n
            vertices.append(np.array([radius * np.cos(ang), radius * np.sin(ang), 0.0]))
        shape = Polygon(*vertices)
        shape.set_fill(color, opacity=1.0)
        shape.set_stroke(WHITE, width=2.0, opacity=1.0)
        return shape

    def make_filter_icons(self):
        center = ORIGIN
        radius = 2.4
        names = ["Low-pass", "High-pass", "Band-pass", "Notch", "Moving-Average", "Median"]
        colors = [BLUE, GREEN, ORANGE, PINK, TEAL, RED]

        shapes = [
            Circle(
                radius=0.62,
                fill_color=colors[0],
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=2.0,
            ),
            Square(
                side_length=1.12,
                fill_color=colors[1],
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=2.0,
            ),
            self.regular_polygon(4, 0.65, colors[2], start_angle=PI / 4),  # diamond
            self.regular_polygon(3, 0.70, colors[3]),
            self.regular_polygon(5, 0.65, colors[4]),
            self.regular_polygon(6, 0.65, colors[5]),
        ]

        icons = []
        for i, (name, shape) in enumerate(zip(names, shapes)):
            label = Text(name, font_size=16, color=WHITE)
            icon = VGroup(shape, label).arrange(DOWN, buff=0.08)
            icon.set_opacity(0.4)
            icon.orbit_angle = i * 2 * PI / len(names) - PI / 2
            icon.move_to(
                center
                + radius
                * np.array([np.cos(icon.orbit_angle), np.sin(icon.orbit_angle), 0.0])
            )
            icon.set_z_index(1)

            def orbiter(m, dt, icon=icon):
                icon.orbit_angle += dt * 0.35
                icon.move_to(
                    center
                    + radius
                    * np.array([np.cos(icon.orbit_angle), np.sin(icon.orbit_angle), 0.0])
                )

            icon.add_updater(orbiter)
            icons.append(icon)

        return icons, VGroup(*icons)

    def pulse_icon(self, icon, total_duration):
        if total_duration >= 0.5:
            up_time = 0.25
            down_time = 0.25
            wait_time = total_duration - up_time - down_time
        else:
            up_time = down_time = max(0.05, total_duration / 2.0)
            wait_time = 0.0

        self.play(
            icon.animate.scale(1.3).set_opacity(1.0),
            run_time=max(0.05, up_time),
            rate_func=smooth,
        )
        self.play(
            icon.animate.scale(1.0 / 1.3).set_opacity(0.4),
            run_time=max(0.05, down_time),
            rate_func=smooth,
        )
        if wait_time > 0.001:
            self.wait(max(0.05, wait_time))

    def make_clean_signal_icon(self):
        brain = (
            SVGMobject(ASSET_PATHS["brain"])
            .set_color(PURPLE)
            .set_stroke(PURPLE, width=0.0)
            .set_fill(PURPLE, opacity=0.9)
        )
        brain.scale_to_fit_height(1.5)

        wave_x = np.linspace(-0.95, 0.95, 150)
        wave_y = 0.32 * np.sin(2 * PI * 2.2 * wave_x)
        wave_points = np.array([wave_x, wave_y, np.zeros_like(wave_x)]).T
        wave = VMobject().set_points_as_corners(wave_points)
        wave.set_stroke(GREEN, width=4.0)
        wave.move_to(brain.get_center())

        icon = VGroup(brain, wave)
        label = Text("Physiological Signal", font_size=26, color=WHITE)
        group = VGroup(icon, label).arrange(DOWN, buff=0.15)
        return group, icon

    def make_noise_icon(self):
        panel = Rectangle(
            width=2.6,
            height=1.7,
            fill_color=MAROON,
            fill_opacity=0.35,
            stroke_color=RED,
            stroke_width=2.0,
        ).round_corners(0.1)

        rng = np.random.default_rng(12)
        spike_lines = VGroup()
        y_offsets = [-0.45, 0.0, 0.45]
        line_colors = [RED, PINK, ORANGE]

        for idx, y_off in enumerate(y_offsets):
            n_pts = 42
            xs = np.linspace(-1.05, 1.05, n_pts)
            ys = (
                y_off
                + 0.10 * np.sin(18.0 * xs + idx * 1.2)
                + rng.normal(0.0, 0.05, n_pts)
            )
            line_pts = np.array([xs, ys, np.zeros(n_pts)]).T
            line = VMobject().set_points_as_corners(line_pts)
            line.set_stroke(line_colors[idx], width=2.2)
            spike_lines.add(line)

        static = VGroup()
        for _ in range(10):
            dot = Dot(
                point=np.array([rng.uniform(-1.1, 1.1), rng.uniform(-0.7, 0.7), 0.0]),
                radius=0.018,
                color=RED,
            )
            static.add(dot)

        icon = VGroup(panel, spike_lines, static)
        label = Text("Noise / Interference", font_size=26, color=WHITE)
        group = VGroup(icon, label).arrange(DOWN, buff=0.15)
        return group, icon

    def make_filter_node(self):
        rect = Rectangle(
            width=2.8,
            height=1.5,
            fill_color=BLUE,
            fill_opacity=0.85,
            stroke_color=WHITE,
            stroke_width=2.0,
        ).round_corners(0.12)

        funnel = SVGMobject(ASSET_PATHS["funnel"]).set_color(WHITE)
        funnel.scale_to_fit_height(0.55)
        label = Text("Filter Selection", font_size=20, color=WHITE)

        content = VGroup(funnel, label).arrange(DOWN, buff=0.08)
        content.move_to(rect.get_center())

        return VGroup(rect, content)