ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {"brain": "C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg"}

from manim import *
import numpy as np


def make_panel_wave(cycles=4, width=2.5, height=0.2, color=TEAL):
    xs = np.linspace(-width / 2, width / 2, 140)
    phase = (xs - xs[0]) / (xs[-1] - xs[0])
    ys = (height / 2) * np.sin(2 * PI * cycles * phase)
    wave = VMobject()
    wave.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
    wave.set_stroke(color, width=3)
    wave.set_fill(opacity=0)
    return wave


def make_stick_figure(open_eye=True, lying=False, color=WHITE):
    if not lying:
        head = Circle(radius=0.13, color=color, stroke_width=2)
        head.set_fill(opacity=0)
        head.move_to(UP * 0.65)

        body = Line(UP * 0.5, DOWN * 0.28, color=color, stroke_width=2)
        arms = Line(UP * 0.22 + LEFT * 0.2, UP * 0.22 + RIGHT * 0.2, color=color, stroke_width=2)
        legs = VGroup(
            Line(DOWN * 0.28, DOWN * 0.75 + LEFT * 0.2, color=color, stroke_width=2),
            Line(DOWN * 0.28, DOWN * 0.75 + RIGHT * 0.2, color=color, stroke_width=2),
        )
        figure = VGroup(head, body, arms, legs)

        if open_eye:
            eye = Dot(head.get_center() + RIGHT * 0.04 + UP * 0.02, radius=0.03, color=YELLOW)
            figure.add(eye)
        else:
            closed = Line(
                head.get_center() + LEFT * 0.055 + UP * 0.03,
                head.get_center() + RIGHT * 0.055 + UP * 0.03,
                color=color,
                stroke_width=2,
            )
            figure.add(closed)
    else:
        head = Circle(radius=0.11, color=color, stroke_width=2)
        head.set_fill(opacity=0)
        head.move_to(LEFT * 0.5)

        body = Line(LEFT * 0.36, RIGHT * 0.5, color=color, stroke_width=2)
        arm = Line(LEFT * 0.15, LEFT * 0.15 + UP * 0.16, color=color, stroke_width=2)
        legs = VGroup(
            Line(RIGHT * 0.5, RIGHT * 0.66 + DOWN * 0.18, color=color, stroke_width=2),
            Line(RIGHT * 0.5, RIGHT * 0.66 + UP * 0.18, color=color, stroke_width=2),
        )
        figure = VGroup(head, body, arm, legs)

        closed = Line(
            head.get_center() + LEFT * 0.04 + UP * 0.03,
            head.get_center() + RIGHT * 0.04 + UP * 0.03,
            color=color,
            stroke_width=2,
        )
        figure.add(closed)

    figure.scale(0.55)
    return figure


def generate_dots(n, x_radius, y_radius, y_center=0.05, seed=0):
    rng = np.random.default_rng(seed)
    colors = [YELLOW, ORANGE, TEAL, PINK]
    dots = VGroup()
    for _ in range(n):
        while True:
            x = rng.uniform(-x_radius, x_radius)
            y = rng.uniform(-y_radius, y_radius)
            if (x / x_radius) ** 2 + (y / y_radius) ** 2 <= 0.96:
                break
        dot = Dot(
            point=np.array([x, y + y_center, 0]),
            radius=0.028,
            color=colors[int(rng.integers(0, 4))],
            stroke_width=0,
        )
        dot.phase = rng.uniform(0, TAU)
        if x < -0.45:
            dot.region = 0
        elif x > 0.45:
            dot.region = 2
        else:
            dot.region = 1
        dots.add(dot)
    return dots


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- Closing composition from previous scene ---------------------
        prev_title = Text("Brain States", font_size=52, color=WHITE, weight="BOLD")
        prev_title.move_to(UP * 2.4)

        prev_wave_xs = np.linspace(-2.7, 2.7, 140)
        prev_wave_phase = (prev_wave_xs - prev_wave_xs[0]) / (prev_wave_xs[-1] - prev_wave_xs[0])
        prev_wave_ys = 0.42 * np.sin(2 * PI * 2.2 * prev_wave_phase)
        prev_wave = VMobject()
        prev_wave.set_points_as_corners(
            [np.array([x, -0.5 + y, 0]) for x, y in zip(prev_wave_xs, prev_wave_ys)]
        )
        prev_wave.set_stroke(TEAL, width=4)
        prev_wave.set_fill(opacity=0)

        next_section = Text("Next section", font_size=24, color=WHITE)
        next_section.to_corner(DR, buff=0.5)

        prev_group = VGroup(prev_title, prev_wave, next_section)

        # ---- Main brain and halo ----------------------------------------
        brain = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=PURPLE,
            fill_opacity=0.3,
            stroke_color=WHITE,
            stroke_width=2,
            stroke_opacity=0.9,
        )
        brain.scale_to_fit_height(5.8)
        brain.move_to(np.array([0, 0.1, 0]))
        brain.set_z_index(1)

        brain_halo = brain.copy()
        brain_halo.set_fill(opacity=0)
        brain_halo.set_stroke(WHITE, width=10, opacity=0)
        brain_halo.scale(1.02)
        brain_halo.set_z_index(0)

        # ---- Beat 1: 0.00-2.42 ------------------------------------------
        self.add(prev_group)
        self.play(FadeOut(prev_group), run_time=max(0.05, 1.0))
        self.play(FadeIn(brain), run_time=max(0.05, 1.42))
        self.add(brain_halo)

        # ---- Beat 2: 2.42-3.28 ------------------------------------------
        self.wait(max(0.05, 0.86))

        # ---- Beat 3: 3.28-6.10 ------------------------------------------
        self.play(
            brain_halo.animate.set_stroke(WHITE, width=12, opacity=0.4),
            run_time=max(0.05, 1.0),
        )
        self.play(
            brain_halo.animate.set_stroke(WHITE, width=6, opacity=0.0),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.82))

        # ---- Neuron trackers and updater ---------------------------------
        bright_left = ValueTracker(1.0)
        bright_center = ValueTracker(1.0)
        bright_right = ValueTracker(1.0)

        def update_dot_group(group, dt=None):
            t = self.time
            bl = bright_left.get_value()
            bc = bright_center.get_value()
            br = bright_right.get_value()
            for dot in group:
                brightness = bl if dot.region == 0 else (bc if dot.region == 1 else br)
                flash = max(0.0, np.sin(2 * PI * 2.1 * t + dot.phase)) ** 1.5
                opacity = 0.15 + 0.85 * flash * brightness
                dot.set_fill(opacity=opacity)

        dots_first = generate_dots(8, 0.35, 0.4, seed=11)
        dots_dozens = generate_dots(35, 0.9, 1.15, seed=22)
        dots_many = generate_dots(110, 1.45, 2.05, seed=33)

        # ---- Waveform trackers -------------------------------------------
        wave_amp = ValueTracker(0.12)
        wave_freq = ValueTracker(2.0)
        wave_xs = np.linspace(-5.5, 5.5, 220)

        def get_wave_points(t):
            amp = wave_amp.get_value()
            f = wave_freq.get_value()
            u = (wave_xs - wave_xs[0]) / (wave_xs[-1] - wave_xs[0])
            ys = amp * (
                0.7 * np.sin(2 * PI * f * t - 2 * PI * f * 1.1 * u)
                + 0.3 * np.sin(2 * PI * 2.3 * f * t - 2 * PI * 1.7 * f * u + 1.7)
                + 0.2 * np.sin(2 * PI * 3.8 * t - 2 * PI * 2.5 * u + 0.5)
            )
            return [np.array([x, -3.15 + y, 0]) for x, y in zip(wave_xs, ys)]

        wave_path = VMobject()
        wave_path.set_points_as_corners(get_wave_points(self.time))
        wave_path.set_stroke(TEAL, width=3)
        wave_path.set_fill(opacity=0)

        def update_wave(wave, dt=None):
            wave.set_points_as_corners(get_wave_points(self.time))

        # ---- Beat 4: 6.10-11.10 -----------------------------------------
        self.play(FadeIn(dots_first), run_time=max(0.05, 0.6))
        dots_first.add_updater(update_dot_group)

        self.play(FadeIn(dots_dozens), run_time=max(0.05, 0.8))
        dots_dozens.add_updater(update_dot_group)

        self.play(FadeIn(dots_many), run_time=max(0.05, 0.8))
        dots_many.add_updater(update_dot_group)

        self.wait(max(0.05, 0.6))

        self.play(Create(wave_path), run_time=max(0.05, 1.2))
        wave_path.add_updater(update_wave)

        self.wait(max(0.05, 1.0))

        # ---- Beat 5: 11.10-12.58 ----------------------------------------
        self.wait(max(0.05, 1.48))

        # ---- Beat 6: 12.58-14.98 ----------------------------------------
        self.play(
            wave_amp.animate.set_value(0.45),
            wave_freq.animate.set_value(4.0),
            bright_left.animate.set_value(0.4),
            bright_center.animate.set_value(1.0),
            bright_right.animate.set_value(0.55),
            run_time=max(0.05, 0.8),
        )
        self.play(
            wave_amp.animate.set_value(0.18),
            wave_freq.animate.set_value(1.6),
            bright_left.animate.set_value(1.0),
            bright_center.animate.set_value(0.45),
            bright_right.animate.set_value(0.8),
            run_time=max(0.05, 0.6),
        )
        self.play(
            wave_amp.animate.set_value(0.55),
            wave_freq.animate.set_value(5.5),
            bright_left.animate.set_value(0.7),
            bright_center.animate.set_value(1.0),
            bright_right.animate.set_value(0.3),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.3))

        # ---- Beat 7: 14.98-19.18 ----------------------------------------
        self.play(
            wave_amp.animate.set_value(0.28),
            wave_freq.animate.set_value(2.6),
            bright_left.animate.set_value(0.7),
            bright_center.animate.set_value(0.65),
            bright_right.animate.set_value(0.9),
            run_time=max(0.05, 1.0),
        )
        self.play(
            wave_amp.animate.set_value(0.5),
            wave_freq.animate.set_value(4.2),
            bright_left.animate.set_value(1.0),
            bright_center.animate.set_value(0.4),
            bright_right.animate.set_value(0.7),
            run_time=max(0.05, 1.0),
        )
        self.play(
            wave_amp.animate.set_value(0.3),
            wave_freq.animate.set_value(3.0),
            bright_left.animate.set_value(0.55),
            bright_center.animate.set_value(0.85),
            bright_right.animate.set_value(1.0),
            run_time=max(0.05, 1.1),
        )
        self.play(
            wave_amp.animate.set_value(0.47),
            wave_freq.animate.set_value(5.2),
            bright_left.animate.set_value(0.8),
            bright_center.animate.set_value(0.6),
            bright_right.animate.set_value(0.45),
            run_time=max(0.05, 1.1),
        )

        # ---- Beat 8: 19.18-25.74 ----------------------------------------
        wave_path.clear_updaters()
        self.play(FadeOut(wave_path), run_time=max(0.05, 0.8))

        brain_target = np.array([-4.2, 0.1, 0])
        self.play(
            brain.animate.scale(0.55).move_to(brain_target),
            brain_halo.animate.scale(0.55).move_to(brain_target),
            dots_first.animate.scale(0.55).move_to(brain_target),
            dots_dozens.animate.scale(0.55).move_to(brain_target),
            dots_many.animate.scale(0.55).move_to(brain_target),
            run_time=max(0.05, 2.0),
        )

        # Three inset panels on the right
        panel_titles = [
            "Awake — solving a problem",
            "Relaxed — eyes closed",
            "Sleeping",
        ]

        def make_panel(title):
            rect = RoundedRectangle(
                corner_radius=0.18,
                width=3.0,
                height=1.9,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_color="#1A1D26",
                fill_opacity=0.95,
            )
            label = Text(title, font_size=18, color=WHITE)
            label.scale_to_fit_width(2.5)
            label.move_to(rect.get_top() + DOWN * 0.38)
            return VGroup(rect, label)

        top_panel = make_panel(panel_titles[0])
        mid_panel = make_panel(panel_titles[1])
        bot_panel = make_panel(panel_titles[2])

        panels_group = VGroup(top_panel, mid_panel, bot_panel)
        panels_group.arrange(DOWN, buff=0.35)
        panels_group.move_to(RIGHT * 4.0 + DOWN * 0.05)

        top_rect = top_panel[0]
        mid_rect = mid_panel[0]
        bot_rect = bot_panel[0]

        # Top panel content: awake
        awake_wave = make_panel_wave(cycles=6, width=2.5, height=0.18, color=TEAL)
        awake_figure = make_stick_figure(open_eye=True)
        awake_equation = Text("7×8=?", font_size=20, color=YELLOW)
        awake_top_row = VGroup(awake_figure, awake_equation).arrange(RIGHT, buff=0.25)
        top_content = VGroup(awake_top_row, awake_wave).arrange(DOWN, buff=0.1)
        top_content.scale_to_fit_height(0.95)
        top_content.scale_to_fit_width(2.6)
        top_content.move_to(top_rect.get_center() + DOWN * 0.25)

        # Middle panel content: relaxed
        relaxed_wave = make_panel_wave(cycles=3, width=2.5, height=0.3, color=BLUE)
        relaxed_figure = make_stick_figure(open_eye=False)
        mid_content = VGroup(relaxed_figure, relaxed_wave).arrange(DOWN, buff=0.1)
        mid_content.scale_to_fit_height(0.9)
        mid_content.scale_to_fit_width(2.5)
        mid_content.move_to(mid_rect.get_center() + DOWN * 0.2)

        # Bottom panel content: sleeping
        sleep_wave = make_panel_wave(cycles=1.5, width=2.5, height=0.34, color=PURPLE)
        sleep_figure = make_stick_figure(lying=True)
        bot_content = VGroup(sleep_figure, sleep_wave).arrange(DOWN, buff=0.1)
        bot_content.scale_to_fit_height(0.9)
        bot_content.scale_to_fit_width(2.5)
        bot_content.move_to(bot_rect.get_center() + DOWN * 0.2)

        self.play(FadeIn(panels_group), run_time=max(0.05, 1.0))
        self.play(FadeIn(top_content), run_time=max(0.05, 1.0))
        self.play(Indicate(top_panel, color=YELLOW, scale_factor=1.04), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.96))

        # ---- Beat 9: 25.74-31.70 ----------------------------------------
        self.wait(max(0.05, 1.46))
        self.play(FadeIn(mid_content), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 2.5))
        self.play(FadeIn(bot_content), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.2))

        # ---- Beat 10: 31.70-36.38 ----------------------------------------
        brain_states_title = Text("Brain States", font_size=46, color=WHITE, weight="BOLD")
        title_x = panels_group.get_center()[0]
        title_y = panels_group.get_top()[1] + 0.4
        brain_states_title.move_to(np.array([title_x, title_y, 0]))
        brain_states_title.scale_to_fit_width(4.5)

        connector_lines = VGroup()
        for panel in (top_panel, mid_panel, bot_panel):
            connector_lines.add(
                Line(
                    brain_states_title.get_bottom() + DOWN * 0.08,
                    panel[0].get_top() + UP * 0.05,
                    color=GREY_B,
                    stroke_width=1.5,
                )
            )

        self.play(FadeIn(brain_states_title), run_time=max(0.05, 0.8))
        self.play(Create(connector_lines), run_time=max(0.05, 1.2))
        self.play(brain_states_title.animate.set_color(YELLOW).scale(1.04), run_time=max(0.05, 0.7))
        self.play(brain_states_title.animate.set_color(WHITE).scale(1 / 1.04), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.28))

        # ---- Beat 11: 36.38-43.17 ----------------------------------------
        wave_highlight = VGroup(
            *[SurroundingRectangle(w, color=YELLOW, buff=0.08, stroke_width=2) for w in (awake_wave, relaxed_wave, sleep_wave)]
        )

        self.wait(max(0.05, 2.82))
        self.play(FadeIn(wave_highlight), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.7))
        self.play(
            wave_highlight.animate.set_stroke(YELLOW, width=5).set_opacity(1.0),
            run_time=max(0.05, 0.5),
        )
        self.play(
            wave_highlight.animate.set_stroke(YELLOW, width=2).set_opacity(0.9),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 0.2))
        self.play(brain_states_title.animate.set_color(YELLOW).scale(1.05), run_time=max(0.05, 0.5))
        self.play(brain_states_title.animate.set_color(WHITE).scale(1 / 1.05), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.47))