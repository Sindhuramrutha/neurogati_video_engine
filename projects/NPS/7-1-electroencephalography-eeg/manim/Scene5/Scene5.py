ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    "brain": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\brain_test.svg",
}


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Beat 1: 0.00-0.94  Opening composition, fade out
        # ------------------------------------------------------------
        opening_title = Text("Brain States", font_size=48, color=WHITE, weight="BOLD")
        opening_title.move_to(UP * 3.0)

        brain_svg = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=PURPLE,
            fill_opacity=0.35,
            stroke_color=WHITE,
            stroke_width=2,
            stroke_opacity=0.9,
        )
        brain_svg.scale_to_fit_height(4.2)
        brain_svg.move_to(LEFT * 3.3 + DOWN * 0.2)

        opening_dots = VGroup()
        rng_open = np.random.default_rng(11)
        for _ in range(22):
            theta = rng_open.uniform(0, 2 * np.pi)
            r = np.sqrt(rng_open.uniform(0.05, 1.0))
            offset = np.array([1.1 * r * np.cos(theta), 1.0 * r * np.sin(theta), 0])
            dot = Dot(
                brain_svg.get_center() + offset,
                radius=0.028,
                color=YELLOW,
                fill_opacity=0.8,
                stroke_width=0,
            )
            opening_dots.add(dot)

        # small right-side panels from previous scene's closing composition
        small_panels = VGroup()
        small_states = [
            ("Awake", TEAL),
            ("Relaxed", BLUE),
            ("Sleeping", PURPLE),
        ]
        for i, (label_txt, color) in enumerate(small_states):
            rect = RoundedRectangle(
                corner_radius=0.12,
                width=2.7,
                height=0.72,
                stroke_color=color,
                stroke_width=2,
                fill_color="#1A1D26",
                fill_opacity=0.95,
            )
            rect.move_to(RIGHT * 3.6 + UP * (1.6 - 1.6 * i))
            lab = Text(label_txt, font_size=18, color=WHITE)
            lab.move_to(rect.get_center())
            small_panels.add(rect, lab)

        opening_group = VGroup(opening_title, brain_svg, opening_dots, small_panels)
        self.add(opening_group)
        self.play(FadeOut(opening_group), run_time=max(0.05, 0.94))

        # ------------------------------------------------------------
        # Beat 2: 0.94-2.06  Empty definition box fades in
        # ------------------------------------------------------------
        def_box = RoundedRectangle(
            corner_radius=0.32,
            width=12.5,
            height=3.7,
            stroke_color=TEAL,
            stroke_width=2.5,
            fill_color="#1A1D26",
            fill_opacity=0.93,
        )
        def_box.move_to(ORIGIN)
        self.play(FadeIn(def_box), run_time=max(0.05, 1.12))

        # ------------------------------------------------------------
        # Beat 3: 2.06-8.34  Definition text phrase by phrase
        # ------------------------------------------------------------
        label_text = Text("Brain state =", font_size=34, color=YELLOW, weight="BOLD")
        phrase1 = Text("overall pattern of neural activity", font_size=28, color=WHITE)
        phrase2 = Text("associated with a particular", font_size=28, color=WHITE)
        phrase3 = Text("behavioural,", font_size=28, color=WHITE)
        phrase4 = Text("cognitive,", font_size=28, color=WHITE)
        phrase5 = Text("or physiological condition.", font_size=28, color=WHITE)

        # lay out three left-aligned lines inside the box
        line1 = VGroup(label_text, phrase1).arrange(RIGHT, buff=0.32)
        line2 = VGroup(phrase2)
        line3 = VGroup(phrase3, phrase4, phrase5).arrange(RIGHT, buff=0.22)

        left_x = def_box.get_left()[0] + 0.55
        top_y = def_box.get_top()[1] - 0.85
        line1.move_to(np.array([left_x + line1.get_width() / 2, top_y, 0]))
        line2.move_to(np.array([left_x + line2.get_width() / 2, top_y - 0.95, 0]))
        line3.move_to(np.array([left_x + line3.get_width() / 2, top_y - 1.85, 0]))

        for line in (line1, line2, line3):
            if line.get_width() > 11.2:
                line.scale_to_fit_width(11.2)

        # 2.06-3.52
        self.play(Write(label_text), run_time=max(0.05, 0.5))
        self.play(Write(phrase1), run_time=max(0.05, 0.96))

        # 3.52-5.24
        self.play(Write(phrase2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.72))

        # 5.24-6.30
        self.play(Write(phrase3), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.56))

        # 6.30-7.22
        self.play(Write(phrase4), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.42))

        # 7.22-8.34
        self.play(Write(phrase5), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.42))

        # definition group for later movement/dimming
        def_group = VGroup(def_box, label_text, phrase1, phrase2, phrase3, phrase4, phrase5)

        # ------------------------------------------------------------
        # Beat 4: 8.34-9.20  Brief pause
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.86))

        # ------------------------------------------------------------
        # Beat 5: 9.20-12.26  Timeline + continuous waveform
        # ------------------------------------------------------------
        timeline_line = Line(LEFT * 6 + DOWN * 1.5, RIGHT * 6 + DOWN * 1.5, color=GREY_B, stroke_width=2)

        xs = np.linspace(-6, 6, 420)
        ys = np.zeros_like(xs)
        for i, x in enumerate(xs):
            u = (x + 6) / 12
            if u < 0.18:
                amp, freq, phase = 0.52, 1.5, 0.0
            elif u < 0.38:
                amp, freq, phase = 0.26, 4.2, 2.0
            elif u < 0.60:
                amp, freq, phase = 0.66, 1.9, 4.0
            elif u < 0.82:
                amp, freq, phase = 0.32, 5.4, 1.2
            else:
                amp, freq, phase = 0.72, 1.2, 3.0
            ys[i] = amp * np.sin(2 * np.pi * freq * u + phase)
        continuous_wave = VMobject()
        continuous_wave.set_points_as_corners(
            [np.array([x, -1.5 + y, 0]) for x, y in zip(xs, ys)]
        )
        continuous_wave.set_stroke(TEAL, width=3)
        continuous_wave.set_fill(opacity=0)

        self.play(
            def_group.animate.scale(0.7).move_to(UP * 2.4),
            FadeIn(timeline_line),
            run_time=max(0.05, 0.9),
        )
        self.play(Create(continuous_wave), run_time=max(0.05, 2.16))

        # ------------------------------------------------------------
        # Beat 6: 12.26-12.96  Hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.70))

        # ------------------------------------------------------------
        # Beat 7: 12.96-16.72  Four activity snapshot panels
        # ------------------------------------------------------------
        def make_state_wave(state, rect, color):
            x0 = rect.get_left()[0] + 0.22
            x1 = rect.get_right()[0] - 0.22
            xs_local = np.linspace(x0, x1, 110)
            ys_local = np.zeros_like(xs_local)
            for i, x in enumerate(xs_local):
                u = (x - x0) / (x1 - x0)
                if state == "relaxed":
                    ys_local[i] = 0.22 * np.sin(2 * np.pi * 1.5 * u) + 0.05 * np.sin(2 * np.pi * 2.4 * u + 0.5)
                elif state == "attentive":
                    ys_local[i] = (
                        0.08 * np.sin(2 * np.pi * 6.5 * u)
                        + 0.05 * np.sin(2 * np.pi * 12.0 * u + 1.0)
                        + 0.04 * np.sin(2 * np.pi * 17.0 * u + 3.0)
                    )
                elif state == "problem":
                    base = 0.20 * np.sin(2 * np.pi * 4.0 * u)
                    burst1 = 0.28 * np.exp(-((u - 0.42) / 0.09) ** 2) * np.sin(2 * np.pi * 9.0 * u)
                    burst2 = 0.22 * np.exp(-((u - 0.74) / 0.08) ** 2) * np.sin(2 * np.pi * 11.0 * u + 1.5)
                    ys_local[i] = base + burst1 + burst2
                else:  # sleeping
                    ys_local[i] = 0.34 * np.sin(2 * np.pi * 0.8 * u + 0.4) + 0.10 * np.sin(2 * np.pi * 1.6 * u)
            wave = VMobject()
            wave.set_points_as_corners(
                [np.array([x, rect.get_center()[1] + y, 0]) for x, y in zip(xs_local, ys_local)]
            )
            wave.set_stroke(color, width=2.5)
            wave.set_fill(opacity=0)
            return wave

        def make_panel_dots(rect, state, seed):
            rng_d = np.random.default_rng(seed)
            dots = VGroup()
            n = {"relaxed": 8, "attentive": 12, "problem": 10, "sleeping": 6}[state]
            for _ in range(n):
                dx = rng_d.uniform(-0.75, 0.75)
                dy = rng_d.uniform(-0.30, 0.30)
                dot = Dot(
                    rect.get_center() + np.array([dx, dy, 0]),
                    radius=0.033,
                    color=YELLOW,
                    fill_opacity=0.5,
                    stroke_width=0,
                )
                dot.set_z_index(1)
                dots.add(dot)
            return dots

        states_data = [
            ("relaxed", TEAL, "Relaxed", 101),
            ("attentive", BLUE, "Attentive", 202),
            ("problem", ORANGE, "Problem-solving", 303),
            ("sleeping", PURPLE, "Sleeping", 404),
        ]
        x_centers = [-4.5, -1.5, 1.5, 4.5]

        panel_rects = []
        panel_waves = []
        panel_labels = []
        panel_dots = []
        panel_color_list = []

        for i, (state, color, label, seed) in enumerate(states_data):
            rect = RoundedRectangle(
                corner_radius=0.10,
                width=2.55,
                height=0.95,
                stroke_color=color,
                stroke_width=2,
                fill_color="#1A1D26",
                fill_opacity=0.95,
            )
            rect.move_to(np.array([x_centers[i], -1.7, 0]))
            rect.set_z_index(0)

            wave = make_state_wave(state, rect, color)
            wave.set_z_index(2)

            lab = Text(label, font_size=20, color=WHITE)
            lab.next_to(rect, DOWN, buff=0.16)
            lab.set_z_index(3)

            dots = make_panel_dots(rect, state, seed)

            panel_rects.append(rect)
            panel_waves.append(wave)
            panel_labels.append(lab)
            panel_dots.append(dots)
            panel_color_list.append(color)

        # fade out timeline and continuous waveform
        self.play(
            FadeOut(timeline_line),
            FadeOut(continuous_wave),
            run_time=max(0.05, 0.32),
        )

        # panel 1: relaxed
        panel1 = VGroup(panel_rects[0], panel_waves[0], panel_labels[0])
        self.play(FadeIn(panel1), run_time=max(0.05, 0.36))

        # wait to panel 2
        self.wait(max(0.05, 0.82))

        # panel 2: attentive
        panel2 = VGroup(panel_rects[1], panel_waves[1], panel_labels[1])
        self.play(FadeIn(panel2), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.08))

        # panel 3: problem-solving
        panel3 = VGroup(panel_rects[2], panel_waves[2], panel_labels[2])
        self.play(FadeIn(panel3), run_time=max(0.05, 0.68))
        self.wait(max(0.05, 0.70))

        # panel 4: sleeping
        panel4 = VGroup(panel_rects[3], panel_waves[3], panel_labels[3])
        self.play(FadeIn(panel4), run_time=max(0.05, 0.30))

        # ------------------------------------------------------------
        # Beat 8: 16.72-19.14  Sequential highlight + neuron markers
        # ------------------------------------------------------------
        per_panel = 2.42 / 4
        for wave, dots, orig_color in zip(panel_waves, panel_dots, panel_color_list):
            self.play(
                wave.animate.set_stroke(YELLOW, width=4),
                FadeIn(dots),
                run_time=max(0.05, per_panel * 0.55),
            )
            self.play(
                wave.animate.set_stroke(orig_color, width=2.5),
                run_time=max(0.05, per_panel * 0.45),
            )

        # ------------------------------------------------------------
        # Beat 9: 19.14-20.00  Hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.86))

        # ------------------------------------------------------------
        # Beat 10: 20.00-24.34  Real-time EEG tracing
        # ------------------------------------------------------------
        static_wave_points = [np.array(w.get_points()) for w in panel_waves]

        # hide static waves
        self.play(*[FadeOut(w) for w in panel_waves], run_time=max(0.05, 0.25))

        dynamic_groups = []
        progress_trackers = []

        def make_trace_updater(wave, dot, tracker, points):
            pts = [np.array(p) for p in points]
            def updater(m):
                p = tracker.get_value()
                n = len(pts)
                idx = int(p * (n - 1))
                idx = max(1, min(idx, n - 1))
                wave.set_points_as_corners(pts[: max(2, idx + 1)])
                dot.move_to(pts[idx])
            return updater

        for i, pts in enumerate(static_wave_points):
            tracker = ValueTracker(0)
            wave = VMobject()
            wave.set_stroke(panel_color_list[i], width=2.5)
            wave.set_fill(opacity=0)
            wave.set_z_index(2)
            dot = Dot(radius=0.045, color=YELLOW)
            dot.set_z_index(4)
            grp = VGroup(wave, dot)
            grp.add_updater(make_trace_updater(wave, dot, tracker, pts))
            dynamic_groups.append(grp)
            progress_trackers.append(tracker)

        self.add(*dynamic_groups)

        # different speeds per state
        trace_targets = [0.75, 1.0, 0.65, 0.45]
        self.play(
            *[tracker.animate.set_value(target) for tracker, target in zip(progress_trackers, trace_targets)],
            run_time=max(0.05, 4.09),
        )

        # ------------------------------------------------------------
        # Beat 11: 24.34-25.82  Hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.48))

        # ------------------------------------------------------------
        # Beat 12: 25.82-30.82  Large synchronized neuron population
        # ------------------------------------------------------------
        # fade out panels
        panel_mobjects_to_fade = []
        for rect in panel_rects:
            panel_mobjects_to_fade.append(rect)
        for lab in panel_labels:
            panel_mobjects_to_fade.append(lab)
        for dots in panel_dots:
            panel_mobjects_to_fade.append(dots)
        for grp in dynamic_groups:
            panel_mobjects_to_fade.append(grp)

        self.play(*[FadeOut(m) for m in panel_mobjects_to_fade], run_time=max(0.05, 0.6))

        # population of dots
        n_pop = 240
        rng_pop = np.random.default_rng(27)
        pop_dot_list = []
        for _ in range(n_pop):
            theta = rng_pop.uniform(0, 2 * np.pi)
            r = np.sqrt(rng_pop.uniform(0.02, 1.0))
            point = np.array([4.8 * r * np.cos(theta), 2.5 * r * np.sin(theta) - 0.5, 0])
            dot = Dot(point, radius=0.028, color=YELLOW, fill_opacity=0.15, stroke_width=0)
            dot.set_z_index(0)
            pop_dot_list.append(dot)

        population_dots = VGroup(*pop_dot_list)
        random_freqs = rng_pop.uniform(1.8, 5.5, n_pop)
        random_phases = rng_pop.uniform(0, 2 * np.pi, n_pop)
        active_mask = rng_pop.random(n_pop) < 0.40

        sync_tracker = ValueTracker(0)
        complexity_tracker = ValueTracker(0)
        pop_start_time = 0.0

        def update_population(dots):
            s = sync_tracker.get_value()
            c = complexity_tracker.get_value()
            t = self.time - pop_start_time
            for i, dot in enumerate(dots):
                x = dot.get_x()
                y = dot.get_y()
                if active_mask[i]:
                    random_term = 0.5 + 0.5 * np.sin(2 * np.pi * random_freqs[i] * t + random_phases[i])
                else:
                    random_term = 0.0
                simple = 0.5 + 0.5 * np.sin(2 * np.pi * 0.95 * t - 2 * np.pi * x / 5.5 + random_phases[i] * 0.1)
                multi = 0.5 + 0.5 * (
                    0.5 * np.sin(2 * np.pi * 0.70 * t - 2 * np.pi * x / 4.5 + random_phases[i] * 0.15)
                    + 0.5 * np.sin(2 * np.pi * 1.90 * t + 2 * np.pi * y / 3.8 + random_phases[i] * 0.08)
                )
                coherent = (1 - c) * simple + c * multi
                brightness = 0.10 + 0.90 * (s * coherent + (1 - s) * random_term)
                brightness = float(np.clip(brightness, 0.03, 1.0))
                dot.set_opacity(brightness)

        self.add(population_dots)
        self.play(FadeIn(population_dots), run_time=max(0.05, 0.8))

        pop_start_time = self.time
        population_dots.add_updater(update_population)

        self.play(
            sync_tracker.animate.set_value(1.0),
            run_time=max(0.05, 3.6),
        )

        # ------------------------------------------------------------
        # Beat 13: 30.82-33.20  Millisecond time-scale marker
        # ------------------------------------------------------------
        tick_marks = VGroup()
        for x_tick in np.arange(-6.0, 6.001, 0.5):
            tick = Line(
                np.array([x_tick, -3.15, 0]),
                np.array([x_tick, -2.85, 0]),
                color=GREY_B,
                stroke_width=1.2,
            )
            tick_marks.add(tick)

        label0 = Text("0 ms", font_size=14, color=GREY_B).move_to(np.array([-5.0, -3.42, 0]))
        label20 = Text("20 ms", font_size=14, color=GREY_B).move_to(np.array([0.0, -3.42, 0]))
        label40 = Text("40 ms", font_size=14, color=GREY_B).move_to(np.array([5.0, -3.42, 0]))
        ticks_group = VGroup(tick_marks, label0, label20, label40)
        ticks_group.set_z_index(5)

        self.play(FadeIn(ticks_group), run_time=max(0.05, 0.8))

        sweep_pop = Rectangle(
            width=0.10,
            height=population_dots.get_height() + 0.5,
            fill_color=YELLOW,
            fill_opacity=0.7,
            stroke_width=0,
        )
        sweep_pop.set_z_index(6)
        start_x = population_dots.get_left()[0] + 0.2
        end_x = population_dots.get_right()[0] - 0.2
        pop_y = population_dots.get_y()
        sweep_pop.move_to(np.array([start_x, pop_y, 0]))
        self.add(sweep_pop)
        self.play(sweep_pop.animate.move_to(np.array([end_x, pop_y, 0])), run_time=max(0.05, 0.5))
        self.play(FadeOut(sweep_pop), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 0.88))

        # ------------------------------------------------------------
        # Beat 14: 33.20-38.64  Dynamics continue, definition dims
        # ------------------------------------------------------------
        self.play(
            def_group.animate.set_opacity(0.45),
            complexity_tracker.animate.set_value(1.0),
            run_time=max(0.05, 5.44),
        )

        # ------------------------------------------------------------
        # Beat 15: 38.64-39.64  Hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 1.0))

        # ------------------------------------------------------------
        # Beat 16: 39.64-42.36  Single neuron inset
        # ------------------------------------------------------------
        source_dot = min(pop_dot_list, key=lambda d: d.get_x())
        source_ring = Circle(radius=0.18, color=YELLOW, stroke_width=2)
        source_ring.move_to(source_dot)
        source_ring.set_z_index(7)

        inset_circle = Circle(
            radius=1.0,
            fill_color="#1A1D26",
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=2,
        )
        inset_circle.move_to(np.array([4.8, -2.2, 0]))
        inset_circle.set_z_index(8)

        inset_dot = Dot(inset_circle.get_center(), radius=0.12, color=YELLOW)
        inset_dot.set_z_index(9)

        trace_points = [
            np.array([-0.75, -0.45, 0]),
            np.array([-0.50, -0.45, 0]),
            np.array([-0.40, 0.15, 0]),
            np.array([-0.30, -0.45, 0]),
            np.array([-0.10, 0.25, 0]),
            np.array([0.00, -0.45, 0]),
            np.array([0.30, 0.10, 0]),
            np.array([0.50, -0.45, 0]),
            np.array([0.75, -0.45, 0]),
        ]
        inset_trace = VMobject()
        inset_trace.set_points_as_corners([inset_circle.get_center() + p for p in trace_points])
        inset_trace.set_stroke(YELLOW, width=2)
        inset_trace.set_z_index(9)

        inset_label = Text("Single neuron", font_size=12, color=GREY_B)
        inset_label.move_to(inset_circle.get_bottom() + DOWN * 0.18)
        inset_label.set_z_index(10)

        self.play(FadeIn(source_ring), run_time=max(0.05, 0.5))
        self.play(
            GrowFromCenter(inset_circle),
            FadeIn(inset_dot),
            FadeIn(inset_trace),
            FadeIn(inset_label),
            run_time=max(0.05, 1.4),
        )
        self.play(Indicate(inset_dot, color=YELLOW, scale_factor=1.4), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.22))

        # ------------------------------------------------------------
        # Beat 17: 42.36-46.60  Global view + overlay sweep
        # ------------------------------------------------------------
        self.play(
            FadeOut(source_ring),
            FadeOut(inset_circle),
            FadeOut(inset_dot),
            FadeOut(inset_trace),
            FadeOut(inset_label),
            run_time=max(0.05, 0.5),
        )

        global_sweep = Rectangle(
            width=3.2,
            height=population_dots.get_height() + 0.6,
            fill_color=TEAL,
            fill_opacity=0.22,
            stroke_width=0,
        )
        global_sweep.set_z_index(6)
        global_sweep.move_to(np.array([start_x, pop_y, 0]))
        self.play(FadeIn(global_sweep), run_time=max(0.05, 0.3))
        self.play(
            global_sweep.animate.move_to(np.array([end_x, pop_y, 0])),
            run_time=max(0.05, 2.6),
        )
        self.play(FadeOut(global_sweep), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.44))

        # ------------------------------------------------------------
        # Beat 18: 46.60-47.35  Final hold
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.75))