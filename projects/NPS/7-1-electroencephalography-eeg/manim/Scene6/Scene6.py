ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Beat 1: 0.00-0.98 continuity fade-out
        continuity_group = self.make_continuity_group()
        self.add(continuity_group)
        self.play(FadeOut(continuity_group), run_time=max(0.05, 0.98))

        # ------------------------------------------------------------
        # Beat 2: 0.98-5.92 frequency axis + five band bars
        # ------------------------------------------------------------
        AXIS_LEFT_X = -4.5
        AXIS_RIGHT_X = 5.5
        AXIS_Y = -2.6

        def fx(f):
            return AXIS_LEFT_X + (f / 50.0) * (AXIS_RIGHT_X - AXIS_LEFT_X)

        axis_line = Line(
            np.array([AXIS_LEFT_X, AXIS_Y, 0]),
            np.array([AXIS_RIGHT_X, AXIS_Y, 0]),
            color=GREY_B,
            stroke_width=2,
        )

        tick_marks = VGroup()
        tick_labels = VGroup()
        for val in [0, 4, 8, 13, 30, 50]:
            x = fx(val)
            tick_marks.add(
                Line(
                    np.array([x, AXIS_Y - 0.08, 0]),
                    np.array([x, AXIS_Y + 0.08, 0]),
                    color=GREY_B,
                    stroke_width=1.5,
                )
            )
            tick_labels.add(
                Text(str(val), font_size=14, color=GREY_B).move_to(
                    np.array([x, AXIS_Y - 0.32, 0])
                )
            )

        axis_title = Text("Frequency (Hz)", font_size=16, color=GREY_B).move_to(
            np.array([0.0, AXIS_Y - 0.80, 0])
        )

        bands = [
            {
                "name": "delta",
                "color": BLUE,
                "range_start": 0.5,
                "range_end": 4,
                "range_text": "0.5–4 Hz",
                "sample_title": "Delta — deep sleep",
                "description": "Delta activity is commonly observed during deep sleep",
            },
            {
                "name": "theta",
                "color": TEAL,
                "range_start": 4,
                "range_end": 8,
                "range_text": "4–8 Hz",
                "sample_title": "Theta — drowsiness, memory",
                "description": "Theta activity is often associated with drowsiness and certain memory-related processes",
            },
            {
                "name": "alpha",
                "color": GREEN,
                "range_start": 8,
                "range_end": 13,
                "range_text": "8–13 Hz",
                "sample_title": "Alpha — awake, relaxed, eyes closed",
                "description": "Alpha activity becomes prominent when a person is awake, relaxed, and has their eyes closed",
            },
            {
                "name": "beta",
                "color": ORANGE,
                "range_start": 13,
                "range_end": 30,
                "range_text": "13–30 Hz",
                "sample_title": "Beta — active thinking, focused attention",
                "description": "Beta activity is generally stronger during active thinking and focused attention",
            },
            {
                "name": "gamma",
                "color": RED,
                "range_start": 30,
                "range_end": 50,
                "range_text": "30+ Hz",
                "sample_title": "Gamma — higher cognitive processing",
                "description": "Gamma activity has been associated with higher cognitive processing and information integration",
            },
        ]

        band_bars = []
        band_bar_labels = []
        bar_y_positions = [-2.25, -1.75, -1.25, -0.75, -0.25]

        for i, band in enumerate(bands):
            x_left = fx(band["range_start"])
            x_right = fx(band["range_end"])
            width = x_right - x_left
            bar = Rectangle(
                width=width,
                height=0.40,
                fill_color=band["color"],
                fill_opacity=0.50,
                stroke_width=0,
            )
            bar.move_to(np.array([(x_left + x_right) / 2, bar_y_positions[i], 0]))

            label = VGroup(
                Text(band["name"], font_size=18, color=band["color"], weight="BOLD"),
                Text(band["range_text"], font_size=14, color=GREY_B),
            ).arrange(DOWN, buff=0.08)
            label.next_to(bar, LEFT, buff=0.12)

            band_bars.append(bar)
            band_bar_labels.append(label)

        self.play(
            Create(axis_line),
            FadeIn(tick_marks, tick_labels, axis_title),
            run_time=max(0.05, 1.0),
        )

        for bar, label in zip(band_bars, band_bar_labels):
            self.play(
                GrowFromCenter(bar),
                FadeIn(label),
                run_time=max(0.05, 0.75),
            )

        self.wait(max(0.05, 0.19))  # to 5.92
        self.wait(max(0.05, 0.64))  # to 6.56

        # ------------------------------------------------------------
        # Beat 3: 6.56-12.18 sequential subtle pulses
        # ------------------------------------------------------------
        per_pulse = 5.62 / 5
        for bar in band_bars:
            self.play(
                bar.animate.set_fill(opacity=1.0),
                run_time=max(0.05, per_pulse * 0.42),
            )
            self.play(
                bar.animate.set_fill(opacity=0.45),
                run_time=max(0.05, per_pulse * 0.58),
            )

        self.wait(max(0.05, 0.74))  # to 12.92

        # ------------------------------------------------------------
        # Beat 4: 12.92-13.30 dim + brief "Example:"
        # ------------------------------------------------------------
        self.play(
            *[bar.animate.set_fill(opacity=0.30) for bar in band_bars],
            run_time=max(0.05, 0.20),
        )

        example_text = (
            Text("Example:", font_size=22, color=YELLOW, weight="BOLD")
            .to_corner(UL, buff=0.35)
            .shift(DOWN * 0.25)
        )
        self.play(FadeIn(example_text), run_time=max(0.05, 0.09))
        self.play(FadeOut(example_text), run_time=max(0.05, 0.09))
        self.wait(max(0.05, 0.56))  # to 13.86

        ENLARGE = 1.08

        # ------------------------------------------------------------
        # Beat 5: 13.86-16.80 delta sample
        # ------------------------------------------------------------
        delta_bar = band_bars[0]
        self.play(
            delta_bar.animate.set_fill(opacity=1.0).scale(ENLARGE),
            run_time=max(0.05, 0.50),
        )

        panel_d, wave_d, title_d, desc_d, icon_d = self.build_sample_group(
            bands[0], self.make_sleep_icon()
        )
        delta_sample_group = VGroup(panel_d, wave_d, title_d, desc_d, icon_d)

        self.play(
            FadeIn(panel_d),
            Write(title_d),
            GrowFromCenter(icon_d),
            run_time=max(0.05, 0.70),
        )
        self.play(Create(wave_d), run_time=max(0.05, 1.24))
        self.play(FadeIn(desc_d), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.72))  # to 17.52

        # ------------------------------------------------------------
        # Beat 6: 17.52-22.34 theta sample
        # ------------------------------------------------------------
        theta_bar = band_bars[1]
        self.play(
            delta_bar.animate.set_fill(opacity=0.30).scale(1 / ENLARGE),
            FadeOut(delta_sample_group),
            run_time=max(0.05, 0.50),
        )
        self.play(
            theta_bar.animate.set_fill(opacity=1.0).scale(ENLARGE),
            run_time=max(0.05, 0.50),
        )

        panel_t, wave_t, title_t, desc_t, icon_t = self.build_sample_group(
            bands[1], self.make_drowsy_icon()
        )
        theta_sample_group = VGroup(panel_t, wave_t, title_t, desc_t, icon_t)

        self.play(
            FadeIn(panel_t),
            Write(title_t),
            GrowFromCenter(icon_t),
            run_time=max(0.05, 0.70),
        )
        self.play(Create(wave_t), run_time=max(0.05, 2.00))
        self.play(FadeIn(desc_t), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.32))  # hold inside beat
        self.wait(max(0.05, 0.86))  # to 23.20

        # ------------------------------------------------------------
        # Beat 7: 23.20-28.46 alpha sample + closing eyes
        # ------------------------------------------------------------
        alpha_bar = band_bars[2]
        self.play(
            theta_bar.animate.set_fill(opacity=0.30).scale(1 / ENLARGE),
            FadeOut(theta_sample_group),
            run_time=max(0.05, 0.50),
        )
        self.play(
            alpha_bar.animate.set_fill(opacity=1.0).scale(ENLARGE),
            run_time=max(0.05, 0.50),
        )

        alpha_icon_group, alpha_eyelids = self.make_eyes_icon()
        panel_a, wave_a, title_a, desc_a, icon_a = self.build_sample_group(
            bands[2], alpha_icon_group
        )
        alpha_sample_group = VGroup(panel_a, wave_a, title_a, desc_a, icon_a)

        self.play(
            FadeIn(panel_a),
            Write(title_a),
            GrowFromCenter(icon_a),
            run_time=max(0.05, 0.60),
        )
        self.play(Create(wave_a), run_time=max(0.05, 2.00))
        self.play(FadeIn(desc_a), run_time=max(0.05, 0.70))
        self.play(
            alpha_eyelids.animate.shift(DOWN * 0.20),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.46))  # hold inside beat
        self.wait(max(0.05, 0.80))  # to 29.26

        # ------------------------------------------------------------
        # Beat 8: 29.26-34.08 beta sample
        # ------------------------------------------------------------
        beta_bar = band_bars[3]
        self.play(
            alpha_bar.animate.set_fill(opacity=0.30).scale(1 / ENLARGE),
            FadeOut(alpha_sample_group),
            run_time=max(0.05, 0.50),
        )
        self.play(
            beta_bar.animate.set_fill(opacity=1.0).scale(ENLARGE),
            run_time=max(0.05, 0.50),
        )

        panel_b, wave_b, title_b, desc_b, icon_b = self.build_sample_group(
            bands[3], self.make_focused_icon()
        )
        beta_sample_group = VGroup(panel_b, wave_b, title_b, desc_b, icon_b)

        self.play(
            FadeIn(panel_b),
            Write(title_b),
            GrowFromCenter(icon_b),
            run_time=max(0.05, 0.60),
        )
        self.play(Create(wave_b), run_time=max(0.05, 2.00))
        self.play(FadeIn(desc_b), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.42))  # hold inside beat
        self.wait(max(0.05, 0.66))  # to 34.74

        # ------------------------------------------------------------
        # Beat 9: 34.74-40.06 gamma sample
        # ------------------------------------------------------------
        gamma_bar = band_bars[4]
        self.play(
            beta_bar.animate.set_fill(opacity=0.30).scale(1 / ENLARGE),
            FadeOut(beta_sample_group),
            run_time=max(0.05, 0.50),
        )
        self.play(
            gamma_bar.animate.set_fill(opacity=1.0).scale(ENLARGE),
            run_time=max(0.05, 0.50),
        )

        panel_g, wave_g, title_g, desc_g, icon_g = self.build_sample_group(
            bands[4], self.make_gamma_network_icon()
        )
        gamma_sample_group = VGroup(panel_g, wave_g, title_g, desc_g, icon_g)

        self.play(
            FadeIn(panel_g),
            Write(title_g),
            GrowFromCenter(icon_g),
            run_time=max(0.05, 0.60),
        )
        self.play(Create(wave_g), run_time=max(0.05, 2.20))
        self.play(FadeIn(desc_g), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 0.62))  # ends exactly at 40.06

        # ------------------------------------------------------------
        # Beat 10: 40.06-40.90 all bars normal, gamma sample fades
        # ------------------------------------------------------------
        self.play(
            gamma_bar.animate.set_fill(opacity=0.50).scale(1 / ENLARGE),
            *[
                bar.animate.set_fill(opacity=0.50)
                for bar in band_bars
                if bar is not gamma_bar
            ],
            FadeOut(gamma_sample_group),
            run_time=max(0.05, 0.84),
        )

        # ------------------------------------------------------------
        # Beat 11: 40.90-46.44 continuous morphing EEG waveform
        # ------------------------------------------------------------
        morph_tracker = ValueTracker(0)
        wave_y = 1.0
        wave_points_x = np.linspace(-6.0, 6.0, 600)

        morph_keys = [
            (0.00, 1.5, 0.55),
            (0.14, 5.5, 0.38),
            (0.29, 10.0, 0.28),
            (0.44, 21.0, 0.15),
            (0.60, 45.0, 0.06),
            (0.76, 21.0, 0.15),
            (0.86, 10.0, 0.28),
            (0.93, 5.5, 0.38),
            (0.97, 1.5, 0.55),
            (1.00, 10.0, 0.28),  # final hold settles in alpha
        ]
        band_centers = {
            "delta": 2.25,
            "theta": 6.0,
            "alpha": 10.5,
            "beta": 21.5,
            "gamma": 40.0,
        }
        band_sigmas = {
            "delta": 2.0,
            "theta": 1.8,
            "alpha": 2.0,
            "beta": 4.0,
            "gamma": 6.0,
        }

        def get_freq_amp(p):
            p = max(0.0, min(1.0, p))
            for i in range(len(morph_keys) - 1):
                p0, f0, a0 = morph_keys[i]
                p1, f1, a1 = morph_keys[i + 1]
                if p0 <= p <= p1:
                    if p1 == p0:
                        return f1, a1
                    t = (p - p0) / (p1 - p0)
                    t = t * t * (3 - 2 * t)
                    return f0 + (f1 - f0) * t, a0 + (a1 - a0) * t
            return morph_keys[-1][1], morph_keys[-1][2]

        def update_wave_and_bars(wave):
            p = morph_tracker.get_value()
            freq, amp = get_freq_amp(p)
            u = (wave_points_x + 6.0) / 12.0
            ys = amp * np.sin(2 * np.pi * freq * u) + 0.18 * amp * np.sin(
                2 * np.pi * 1.8 * freq * u + 1.2
            )
            pts = [
                np.array([x, wave_y + y, 0])
                for x, y in zip(wave_points_x, ys)
            ]
            wave.set_points_as_corners(pts)

            for band, bar in zip(bands, band_bars):
                center = band_centers[band["name"]]
                sigma = band_sigmas[band["name"]]
                weight = np.exp(-((freq - center) ** 2) / (2 * sigma ** 2))
                bar.set_fill(opacity=0.25 + 0.75 * float(weight))

        continuous_wave = VMobject()
        continuous_wave.set_stroke(WHITE, width=2.5)
        continuous_wave.set_fill(opacity=0)
        continuous_wave.add_updater(update_wave_and_bars)

        update_wave_and_bars(continuous_wave)
        self.add(continuous_wave)

        self.play(
            morph_tracker.animate.set_value(1.0),
            run_time=max(0.05, 5.54),
        )

        # ------------------------------------------------------------
        # Beat 12: 46.44-47.38 final hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.94))

    # ------------------------------------------------------------
    # Helper builders
    # ------------------------------------------------------------
    def make_continuity_group(self):
        def_box = RoundedRectangle(
            corner_radius=0.25,
            width=8.0,
            height=1.9,
            stroke_color=TEAL,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.85,
        )
        def_box.move_to(UP * 2.5)

        def_title = Text(
            "Brain state = overall pattern of neural activity",
            font_size=22,
            color=WHITE,
        )
        def_title.move_to(def_box.get_center())
        def_title.scale_to_fit_width(7.2)

        rng = np.random.default_rng(5)
        dots = VGroup()
        for _ in range(80):
            theta = rng.uniform(0, 2 * np.pi)
            r = np.sqrt(rng.uniform(0.0, 1.0))
            point = np.array([4.8 * r * np.cos(theta), 2.0 * r * np.sin(theta) - 0.8, 0])
            dot = Dot(
                point,
                radius=0.028,
                color=YELLOW,
                fill_opacity=0.30,
                stroke_width=0,
            )
            dots.add(dot)

        waves = VGroup()
        xs = np.linspace(-5.5, 5.5, 200)
        for i, color in enumerate([TEAL, BLUE, PURPLE]):
            ys = 0.15 * np.sin(2 * np.pi * (1.2 + 0.5 * i) * (xs + 5.5) / 11.0 + i)
            wave = VMobject()
            wave.set_points_as_corners(
                [np.array([x, -1.6 + y + 0.3 * i, 0]) for x, y in zip(xs, ys)]
            )
            wave.set_stroke(color, width=2)
            wave.set_fill(opacity=0)
            waves.add(wave)

        return VGroup(def_box, def_title, dots, waves)

    def make_band_wave(self, name, panel, color):
        x0 = panel.get_left()[0] + 0.22
        x1 = panel.get_right()[0] - 0.22
        xs = np.linspace(x0, x1, 260)
        ys = np.zeros_like(xs)

        for i, x in enumerate(xs):
            u = (x - x0) / (x1 - x0)
            if name == "delta":
                y = 0.52 * np.sin(2 * np.pi * 1.2 * u) + 0.10 * np.sin(
                    2 * np.pi * 2.4 * u
                )
            elif name == "theta":
                y = 0.34 * np.sin(2 * np.pi * 2.2 * u + 0.4) + 0.08 * np.sin(
                    2 * np.pi * 4.4 * u
                )
            elif name == "alpha":
                y = 0.24 * np.sin(2 * np.pi * 3.0 * u) + 0.06 * np.sin(
                    2 * np.pi * 6.0 * u + 0.7
                )
            elif name == "beta":
                y = (
                    0.10 * np.sin(2 * np.pi * 5.0 * u)
                    + 0.07 * np.sin(2 * np.pi * 11.0 * u + 1.0)
                    + 0.05 * np.sin(2 * np.pi * 17.0 * u + 2.5)
                )
            elif name == "gamma":
                y = (
                    0.025 * np.sin(2 * np.pi * 20.0 * u)
                    + 0.020 * np.sin(2 * np.pi * 30.0 * u + 0.7)
                    + 0.015 * np.sin(2 * np.pi * 42.0 * u + 1.3)
                    + 0.012 * np.sin(2 * np.pi * 48.0 * u + 2.1)
                )
            else:
                y = 0.0
            ys[i] = y

        wave = VMobject()
        wave.set_points_as_corners(
            [np.array([x, panel.get_center()[1] + y, 0]) for x, y in zip(xs, ys)]
        )
        wave.set_stroke(color, width=2.5)
        wave.set_fill(opacity=0)
        return wave

    def build_sample_group(self, band, icon):
        color = band["color"]
        panel = RoundedRectangle(
            corner_radius=0.12,
            width=3.4,
            height=1.0,
            stroke_color=color,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.95,
        )
        panel.move_to(np.array([3.0, 1.8, 0]))

        wave = self.make_band_wave(band["name"], panel, color)
        title = Text(
            band["sample_title"], font_size=18, color=WHITE, weight="BOLD"
        ).next_to(panel, UP, buff=0.12)

        desc = Text(band["description"], font_size=16, color=WHITE)
        desc.next_to(panel, DOWN, buff=0.18)
        if desc.get_width() > 6.0:
            desc.scale_to_fit_width(6.0)

        icon.scale_to_fit_height(0.7)
        icon.next_to(panel, RIGHT, buff=0.30)

        return panel, wave, title, desc, icon

    def make_sleep_icon(self):
        face = Circle(
            radius=0.34,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(UP * 0.12)

        pillow = RoundedRectangle(
            corner_radius=0.12,
            width=0.95,
            height=0.25,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(DOWN * 0.35)

        eye_l = Line(
            LEFT * 0.20 + UP * 0.16,
            LEFT * 0.08 + UP * 0.16,
            color=WHITE,
            stroke_width=3,
        )
        eye_r = Line(
            RIGHT * 0.08 + UP * 0.16,
            RIGHT * 0.20 + UP * 0.16,
            color=WHITE,
            stroke_width=3,
        )
        mouth = Line(
            LEFT * 0.08 + DOWN * 0.12,
            RIGHT * 0.08 + DOWN * 0.12,
            color=WHITE,
            stroke_width=2,
        )
        return VGroup(face, pillow, eye_l, eye_r, mouth)

    def make_drowsy_icon(self):
        face = Circle(
            radius=0.34,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(ORIGIN)

        eye_l = Ellipse(
            width=0.18,
            height=0.10,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(LEFT * 0.12 + UP * 0.08)
        eye_r = Ellipse(
            width=0.18,
            height=0.10,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(RIGHT * 0.12 + UP * 0.08)

        lid_l = Rectangle(
            width=0.22,
            height=0.08,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(LEFT * 0.12 + UP * 0.11)
        lid_r = Rectangle(
            width=0.22,
            height=0.08,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(RIGHT * 0.12 + UP * 0.11)

        mouth = Line(
            LEFT * 0.08 + DOWN * 0.15,
            RIGHT * 0.08 + DOWN * 0.15,
            color=WHITE,
            stroke_width=2,
        )
        return VGroup(face, eye_l, eye_r, lid_l, lid_r, mouth)

    def make_eyes_icon(self):
        face = Circle(
            radius=0.34,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(ORIGIN)

        eye_l = Ellipse(
            width=0.18,
            height=0.11,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(LEFT * 0.12 + UP * 0.08)
        eye_r = Ellipse(
            width=0.18,
            height=0.11,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(RIGHT * 0.12 + UP * 0.08)

        lid_l = Rectangle(
            width=0.22,
            height=0.12,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(eye_l.get_center() + UP * 0.17)
        lid_r = Rectangle(
            width=0.22,
            height=0.12,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(eye_r.get_center() + UP * 0.17)

        mouth = Line(
            LEFT * 0.08 + DOWN * 0.16,
            RIGHT * 0.08 + DOWN * 0.16,
            color=WHITE,
            stroke_width=2,
        )

        icon = VGroup(face, eye_l, eye_r, lid_l, lid_r, mouth)
        eyelids = VGroup(lid_l, lid_r)
        return icon, eyelids

    def make_focused_icon(self):
        face = Circle(
            radius=0.34,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(ORIGIN)

        eye_l = Ellipse(
            width=0.14,
            height=0.09,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(LEFT * 0.13 + UP * 0.06)
        eye_r = Ellipse(
            width=0.14,
            height=0.09,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(RIGHT * 0.13 + UP * 0.06)

        pupil_l = Dot(eye_l.get_center(), radius=0.035, color=BLACK, fill_opacity=1)
        pupil_r = Dot(eye_r.get_center(), radius=0.035, color=BLACK, fill_opacity=1)

        brow_l = Line(
            LEFT * 0.25 + UP * 0.20,
            LEFT * 0.05 + UP * 0.13,
            color=WHITE,
            stroke_width=2,
        )
        brow_r = Line(
            RIGHT * 0.25 + UP * 0.20,
            RIGHT * 0.05 + UP * 0.13,
            color=WHITE,
            stroke_width=2,
        )
        mouth = Line(
            LEFT * 0.06 + DOWN * 0.16,
            RIGHT * 0.06 + DOWN * 0.16,
            color=WHITE,
            stroke_width=2,
        )

        return VGroup(face, eye_l, eye_r, pupil_l, pupil_r, brow_l, brow_r, mouth)

    def make_gamma_network_icon(self):
        node_positions = [
            LEFT * 0.35 + UP * 0.20,
            RIGHT * 0.35 + UP * 0.20,
            LEFT * 0.35 + DOWN * 0.20,
            RIGHT * 0.35 + DOWN * 0.20,
        ]
        node_colors = [YELLOW, TEAL, PURPLE, ORANGE]

        nodes = VGroup(
            *[
                Dot(pos, radius=0.10, color=color, fill_opacity=1, stroke_width=0)
                for pos, color in zip(node_positions, node_colors)
            ]
        )

        lines = VGroup()
        for i in range(len(node_positions)):
            for j in range(i + 1, len(node_positions)):
                lines.add(
                    Line(
                        node_positions[i],
                        node_positions[j],
                        color=GREY_B,
                        stroke_width=1.5,
                    )
                )

        return VGroup(lines, nodes)