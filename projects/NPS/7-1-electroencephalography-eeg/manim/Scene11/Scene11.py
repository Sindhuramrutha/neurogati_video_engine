ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene11(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        wave_time = ValueTracker(0)
        rng = np.random.default_rng(11)
        waves_created = False

        def advance(duration, *anims):
            nonlocal waves_created
            if duration <= 0:
                return
            safe = max(0.05, float(duration))
            all_anims = list(anims)
            if waves_created:
                all_anims.append(wave_time.animate.increment_value(safe))
            if all_anims:
                self.play(*all_anims, run_time=max(0.05, safe), rate_func=linear)
            else:
                self.wait(max(0.05, safe))

        # ------------------------------------------------------------------
        # Previous scene's night-sleep composition, kept minimal and fast
        # ------------------------------------------------------------------
        moon = Circle(radius=0.35, fill_color=WHITE, fill_opacity=0.92,
                      stroke_width=0).move_to([5.2, 2.7, 0])
        stars = VGroup(*[
            Dot(point=[rng.uniform(-6.2, 6.2), rng.uniform(-2.8, 3.2), 0],
                radius=0.02, color=WHITE,
                fill_opacity=rng.uniform(0.5, 0.9), stroke_width=0)
            for _ in range(10)
        ])
        head = Circle(radius=0.22, fill_color=BLACK, fill_opacity=1,
                      stroke_color=GREY_B, stroke_width=1.5).move_to([-2.0, -0.5, 0])
        body = RoundedRectangle(corner_radius=0.25, width=0.85, height=0.6,
                                fill_color=BLACK, fill_opacity=1,
                                stroke_color=GREY_B, stroke_width=1.5).move_to([-2.0, -1.05, 0])
        person = VGroup(head, body)

        stage_markers = VGroup(*[
            Text(f"Stage {i+1}", font_size=18, color=WHITE).set_opacity(0.6)
            for i in range(3)
        ]).arrange(RIGHT, buff=0.7).move_to([0, -2.6, 0])

        def tiny_icon(label):
            rect = RoundedRectangle(corner_radius=0.08, width=0.4, height=0.4,
                                    fill_color=GREY_D, fill_opacity=0.95,
                                    stroke_color=WHITE, stroke_width=1.2)
            line = Line(rect.get_left() + RIGHT * 0.08 + UP * 0.05,
                        rect.get_right() + LEFT * 0.08 + DOWN * 0.05,
                        color=WHITE, stroke_width=1.2)
            txt = Text(label, font_size=13, color=WHITE)
            return VGroup(rect, line, txt).arrange(DOWN, buff=0.06)

        bottom_icons = VGroup(
            tiny_icon("Clinical"),
            tiny_icon("Research"),
            tiny_icon("Disorders"),
        ).arrange(RIGHT, buff=0.5).move_to([-3.2, -3.35, 0])

        old_scene = VGroup(moon, stars, person, stage_markers, bottom_icons)
        self.add(old_scene)

        # ------------------------------------------------------------------
        # Definition box, top center, exact phrase-by-phrase text
        # ------------------------------------------------------------------
        p1 = Text("Sleep staging =", color=YELLOW, font_size=30, weight="BOLD").set_opacity(0)
        p2 = Text("process of identifying different stages of sleep",
                  color=WHITE, font_size=26).set_opacity(0)
        p3 = Text("by analysing physiological signals,",
                  color=WHITE, font_size=26).set_opacity(0)
        p4 = Text("particularly EEG", color=WHITE, font_size=26).set_opacity(0)

        # Use a temporary VGroup only to arrange positions, but animate each part separately
        def_text_parts = VGroup(p1, p2, p3, p4).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT
        ).move_to([0, 2.5, 0])
        definition_box = RoundedRectangle(
            corner_radius=0.2,
            width=def_text_parts.width + 0.7,
            height=def_text_parts.height + 0.5,
            fill_color=BLACK, fill_opacity=0.7,
            stroke_color=YELLOW, stroke_width=2
        )
        definition_box.move_to([0, 2.5, 0])
        def_text_parts.move_to(definition_box.get_center())
        # Remove temp group so phrases are independent mobjects on scene
        self.remove(def_text_parts)
        self.add(p1, p2, p3, p4)

        # Beat 1: 0.00-0.80, definition box appears phrase by phrase
        advance(0.30, FadeOut(old_scene), FadeIn(definition_box))
        advance(0.08, p1.animate.set_opacity(1))
        advance(0.08, p2.animate.set_opacity(1))
        advance(0.08, p3.animate.set_opacity(1))
        advance(0.08, p4.animate.set_opacity(1))
        advance(0.18)

        # gap: 0.80 - 3.80
        advance(3.00)

        # ------------------------------------------------------------------
        # Four sleep-stage cards with distinct waveforms above each block
        # ------------------------------------------------------------------
        stage_infos = [
            {"name": "Wakefulness", "color": TEAL,   "freq": 4.0, "amp": 0.08, "speed": 2.0, "burst": False},
            {"name": "Light Sleep", "color": BLUE,   "freq": 2.0, "amp": 0.14, "speed": 1.2, "burst": False},
            {"name": "Deep Sleep",  "color": PURPLE, "freq": 0.7, "amp": 0.28, "speed": 0.5, "burst": False},
            {"name": "REM",         "color": PINK,   "freq": 3.5, "amp": 0.10, "speed": 1.8, "burst": True},
        ]
        num_points = 60
        local_xs = np.linspace(-0.85, 0.85, num_points)

        def update_wave(mob, info, wave_window):
            t = wave_time.get_value()
            xs = local_xs
            if info["burst"]:
                burst_env = 0.5 + 0.5 * np.sin(2 * np.pi * (t * 0.8 - 0.25))
                y = info["amp"] * (
                    np.sin(2 * np.pi * info["freq"] * xs - info["speed"] * t) +
                    0.6 * burst_env * np.sin(2 * np.pi * 6 * xs - 2.5 * t)
                )
            else:
                y = info["amp"] * (
                    np.sin(2 * np.pi * info["freq"] * xs - info["speed"] * t) +
                    0.25 * np.sin(2 * np.pi * 2.0 * info["freq"] * xs - 0.8 * info["speed"] * t + 0.6)
                )
            center = wave_window.get_center()
            pts = np.vstack([center[0] + xs, center[1] + y, np.zeros_like(xs)]).T
            mob.set_points_as_corners(pts)

        cards = []
        blocks = []
        labels = []
        waves = []
        wave_windows = []

        for info in stage_infos:
            ww = Rectangle(
                width=1.8, height=0.7,
                color=GREY_B, stroke_width=1.2,
                fill_color=BLACK, fill_opacity=0.4
            )
            block = RoundedRectangle(
                corner_radius=0.15, width=1.9, height=1.0,
                fill_color=info["color"], fill_opacity=0.30,
                stroke_color=WHITE, stroke_width=2.0
            )
            label = Text(info["name"], font_size=20, color=WHITE)

            block.next_to(ww, DOWN, buff=0.14)
            label.next_to(block, DOWN, buff=0.10)

            wave = VMobject()
            wave.set_stroke(color=YELLOW, width=2.0)
            wave.set_fill(opacity=0)
            # set initial points once
            xs = local_xs
            if info["burst"]:
                y = info["amp"] * (
                    np.sin(2 * np.pi * info["freq"] * xs) +
                    0.3 * np.sin(2 * np.pi * 6 * xs)
                )
            else:
                y = info["amp"] * (
                    np.sin(2 * np.pi * info["freq"] * xs) +
                    0.25 * np.sin(2 * np.pi * 2.0 * info["freq"] * xs + 0.6)
                )
            ww_center = ww.get_center()
            wave.set_points_as_corners(
                np.vstack([ww_center[0] + xs, ww_center[1] + y, np.zeros_like(xs)]).T
            )

            card = VGroup(ww, wave, block, label)
            cards.append(card)
            blocks.append(block)
            labels.append(label)
            waves.append(wave)
            wave_windows.append(ww)

        stage_group = VGroup(*cards).arrange(RIGHT, buff=0.55).move_to([0, -0.3, 0])

        # Add updaters after final layout
        for info, wave, ww in zip(stage_infos, waves, wave_windows):
            wave.add_updater(lambda m, info=info, ww=ww: update_wave(m, info, ww))
        waves_created = True

        # Soft highlights around each waveform region, created after layout
        wave_highlights = []
        for ww in wave_windows:
            sr = SurroundingRectangle(
                ww, color=YELLOW, buff=0.06, corner_radius=0.1,
                stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.10
            )
            sr.set_opacity(0)
            wave_highlights.append(sr)
        self.add(*wave_highlights)

        # Transition arrows between adjacent stage blocks
        arrows = []
        for i in range(3):
            start = blocks[i].get_right() + RIGHT * 0.1
            end = blocks[i + 1].get_left() + LEFT * 0.1
            arrow = Arrow(start, end, color=GREY_B, stroke_width=2.0, buff=0.1)
            arrows.append(arrow)

        # Beat 2: 3.80-5.60, four stage blocks fade in along center
        advance(1.80, *[FadeIn(card) for card in cards])

        # gap: 5.60-8.14
        advance(2.54)

        # Beat 3: 8.14-10.32, pulse through each stage quickly
        per_pulse = 2.18 / 4
        for i in range(4):
            advance(per_pulse * 0.55,
                    Indicate(blocks[i], scale_factor=1.10, color=YELLOW),
                    waves[i].animate.set_stroke(color=WHITE, width=2.8))
            advance(per_pulse * 0.45,
                    Indicate(wave_windows[i], scale_factor=1.05, color=YELLOW))

        # gap: 10.32-10.88
        advance(0.56)

        # Beat 4: 10.88-13.26, transition arrows draw in sequence
        per_arrow_time = 2.38 / 3
        for arrow in arrows:
            advance(per_arrow_time, Create(arrow))

        # gap: 13.26-13.80
        advance(0.54)

        # Beat 5: 13.80-16.68, each waveform brightens with soft highlight
        per_wave_highlight = 2.88 / 4
        for i in range(4):
            advance(
                per_wave_highlight,
                waves[i].animate.set_stroke(color=WHITE, width=3.2, opacity=1),
                wave_highlights[i].animate.set_opacity(0.7)
            )

        # gap: 16.68-17.66
        advance(0.98)

        # Beat 6: 17.66-20.20, progression Wakefulness -> Light -> Deep
        per_trace = 2.54 / 3
        for i in range(3):
            advance(
                per_trace * 0.55,
                Indicate(blocks[i], scale_factor=1.12, color=YELLOW),
                waves[i].animate.set_stroke(color=YELLOW, width=3.2)
            )
            advance(
                per_trace * 0.45,
                arrows[i].animate.set_color(YELLOW)
            )

        # gap: 20.20-20.60
        advance(0.40)

        # Beat 7: 20.60-23.68, REM highlighted and pulsed
        advance(
            0.90,
            Indicate(blocks[3], scale_factor=1.15, color=YELLOW),
            labels[3].animate.set_color(YELLOW)
        )
        advance(
            0.70,
            Indicate(wave_windows[3], scale_factor=1.10, color=YELLOW),
            waves[3].animate.set_stroke(color=WHITE, width=3.5, opacity=1)
        )
        advance(0.60, labels[3].animate.scale(1.15))
        advance(0.88)

        # gap: 23.68-24.14
        advance(0.46)

        # Beat 8: 24.14-28.24, continuous scrolling + flowing arrows
        flow_dot = Dot(radius=0.06, color=YELLOW, fill_opacity=0.9)
        flow_dot.move_to(blocks[0].get_left() + LEFT * 0.1)
        self.add(flow_dot)
        advance(3.40, flow_dot.animate.move_to(blocks[3].get_right() + RIGHT * 0.1))
        advance(0.70, FadeOut(flow_dot))

        # gap: 28.24-28.87
        advance(0.63)

        # Beat 9: 28.87-34.54, clinician monitor reads stages
        monitor_screen = RoundedRectangle(
            corner_radius=0.12, width=1.4, height=0.8,
            fill_color=BLACK, fill_opacity=0.7,
            stroke_color=GREEN, stroke_width=2
        )
        # simple static pulse waveform inside monitor
        monitor_pts = np.array([
            [-0.55, -0.18, 0], [-0.35, -0.18, 0], [-0.25, -0.18, 0],
            [-0.15, 0.15, 0], [-0.05, -0.25, 0], [0.05, 0.20, 0],
            [0.15, -0.18, 0], [0.35, -0.18, 0], [0.55, -0.18, 0]
        ])
        monitor_wave = VMobject().set_points_as_corners(monitor_pts)
        monitor_wave.set_stroke(GREEN, width=2.0)
        monitor_wave.move_to(monitor_screen.get_center())
        monitor_stand = Line(
            monitor_screen.get_bottom(),
            monitor_screen.get_bottom() + DOWN * 0.2,
            color=GREY_B, stroke_width=2
        )
        monitor_group = VGroup(monitor_screen, monitor_wave, monitor_stand)
        monitor_group.scale_to_fit_height(1.0).move_to([5.0, -2.0, 0])

        advance(0.80, FadeIn(monitor_group))

        per_read = 4.87 / 4
        for i in range(4):
            advance(
                per_read,
                Indicate(wave_windows[i], scale_factor=1.12, color=YELLOW),
                waves[i].animate.set_stroke(color=WHITE, width=3.5, opacity=1)
            )

        # gap: 34.54-35.58
        advance(1.04)

        # Beat 10: 35.58-44.58, brain schematic + connections + caption
        brain_ellipse = Ellipse(
            width=1.4, height=0.95,
            stroke_color=PINK, stroke_width=2.0,
            fill_color=PINK, fill_opacity=0.15
        )
        gyrus1 = Line(
            brain_ellipse.get_left() + RIGHT * 0.2 + UP * 0.18,
            brain_ellipse.get_right() + LEFT * 0.2 + UP * 0.18,
            color=PINK, stroke_width=1.0
        )
        gyrus2 = Line(
            brain_ellipse.get_left() + RIGHT * 0.2 + DOWN * 0.18,
            brain_ellipse.get_right() + LEFT * 0.2 + DOWN * 0.18,
            color=PINK, stroke_width=1.0
        )
        brain = VGroup(brain_ellipse, gyrus1, gyrus2)
        brain.scale_to_fit_height(1.2).move_to([-5.2, 1.1, 0])

        connections = VGroup()
        for ww in wave_windows:
            line = Line(
                brain.get_right() + RIGHT * 0.1,
                ww.get_top() + UP * 0.2,
                color=YELLOW, stroke_width=1.5, stroke_opacity=0.5
            )
            connections.add(line)

        caption = Text("high temporal resolution",
                       font_size=28, color=YELLOW, weight="BOLD")
        caption.move_to([0, -2.0, 0])

        advance(0.80, FadeIn(brain))
        advance(1.20, *[Create(line) for line in connections])
        advance(0.70, FadeIn(caption))

        per_brain_wave = 4.80 / 4
        for i in range(4):
            advance(
                per_brain_wave,
                Indicate(wave_windows[i], scale_factor=1.15, color=YELLOW),
                waves[i].animate.set_stroke(color=WHITE, width=3.5, opacity=1)
            )

        # hold within beat 10 to reach its full duration
        advance(1.50)

        # final hold: 44.58-45.50
        advance(0.92)