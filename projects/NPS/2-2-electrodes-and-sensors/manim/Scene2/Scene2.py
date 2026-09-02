ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Global clock for continuous animations
        self.time_tracker = ValueTracker(0)
        self.add(self.time_tracker)
        self.time_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        # Build and place body at start (static for beat 1)
        self.body = self.build_body()
        self.body.move_to(np.array([-3.2, -0.2, 0]))
        self.add(self.body)

        # Thermometer
        self.thermo, self.thermo_fluid, self.thermo_ticks, self.thermo_bulb = self.build_thermometer()
        self.thermo.move_to(np.array([0.9, 0.6, 0]))

        # Beat 1: 0.00-2.04 thermometer fades in
        self.play(FadeIn(self.thermo), run_time=max(0.05, 2.04))

        # Positions and heat state
        self.heat_speed = ValueTracker(1.0)
        self.heat_group = None
        self.heat_lines = VGroup()
        self.heat_heads = VGroup()
        self.heat_funcs = []
        self.heat_base_arrows = []
        self.shoulder_point = np.array([-2.65, 1.55, 0])
        self.bulb_point = np.array([-2.25, 2.10, 0])

        # Beat 2: 2.04-4.50 thermometer slides closer, heat arrows rise, fill rises
        thermo_target = np.array([-2.1, 2.30, 0])
        self.play(
            self.thermo.animate.move_to(thermo_target),
            self.thermo_fluid.animate.stretch(1.25, 1, about_edge=DOWN),
            run_time=max(0.05, 1.2
        ))
        self.create_heat_arrows(self.shoulder_point, self.bulb_point)
        self.play(FadeIn(self.heat_group), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.46))

        # Electrode side state
        self.pulse_speed = ValueTracker(1.0)
        self.pulse_start = np.array([-2.85, 0.40, 0])
        self.pulse_end = np.array([4.0, 0.40, 0])
        self.pulse_dots_group = VGroup()

        # Beat 3: 4.50-8.44 shift left, pad appears and moves to chest, wire, pulses
        shift_vec = LEFT * 0.35
        self.play(
            self.body.animate.shift(shift_vec),
            self.thermo.animate.shift(shift_vec),
            self.heat_group.animate.shift(shift_vec),
            run_time=max(0.05, 0.7
        ))
        self.shoulder_point += shift_vec
        self.bulb_point += shift_vec
        self.pulse_start += shift_vec
        self.pulse_end += shift_vec

        # Electrode pad
        pad_start = np.array([4.5, 2.2, 0])
        pad_target = np.array([-2.85, 0.40, 0])
        self.pad = self.build_pad()
        self.pad.move_to(pad_start)
        self.play(FadeIn(self.pad), run_time=max(0.05, 0.35))
        self.play(self.pad.animate.move_to(pad_target), run_time=max(0.05, 0.95))

        # Wire already drawn from pad to box end
        self.box_left = np.array([4.0, 0.40, 0])
        wire_left = pad_target + RIGHT * 0.35
        self.wire = Line(
            start=wire_left,
            end=self.box_left,
            color=GREY_B,
            stroke_width=3
        )
        self.play(FadeIn(self.wire), run_time=max(0.05, 0.35))

        # Continuous pulse dots
        self.create_pulses()
        self.play(FadeIn(self.pulse_dots_group), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.09))

        # Beat 4: 8.44-9.20 recording box fades in, indicator blinks
        self.box = self.build_recording_box()
        self.box.move_to(np.array([5.0, 0.40, 0]))
        self.box_left = self.box.get_left()
        self.pulse_end = self.box.get_left()
        self.play(FadeIn(self.box), run_time=max(0.05, 0.76))
        self.start_indicator_blink()

        # Beat 5: 9.20-11.46 red X over body/thermo side, heat arrows stop and turn gray
        self.red_x = self.build_red_x()
        self.red_x.move_to(np.array([-2.6, 1.75, 0]))
        self.label_no_gen = Text(
            "does NOT generate signals",
            font_size=24,
            weight="BOLD",
            color=RED
        )
        self.label_no_gen.next_to(self.red_x, DOWN, buff=0.3)
        self.play(
            FadeIn(self.red_x),
            FadeIn(self.label_no_gen),
            run_time=max(0.05, 0.5
        ))
        self.play(
            self.heat_speed.animate.set_value(0.0),
            self.heat_lines.animate.set_color(GREY),
            self.heat_heads.animate.set_fill(GREY),
            run_time=max(0.05, 1.76
        ))

        # Gap 11.46-13.14 hold after beat 5
        self.wait(max(0.05, 1.68))

        # Beat 6: 13.14-16.20 red X/label fade, brighten electrode side, dashed circle at contact
        self.play(
            FadeOut(self.red_x),
            FadeOut(self.label_no_gen),
            run_time=max(0.05, 0.5
        ))
        self.play(
            self.body.animate.set_opacity(1.0),
            self.pad.animate.set_opacity(1.0),
            self.wire.animate.set_opacity(1.0),
            self.box.animate.set_opacity(1.0),
            run_time=max(0.05, 0.6
        ))
        dashed_circle = DashedVMobject(
            Circle(radius=0.35, color=YELLOW, stroke_width=4),
            num_dashes=24
        )
        dashed_circle.move_to(self.pad.get_center() + LEFT * 0.35)
        self.play(Create(dashed_circle), run_time=max(0.05, 0.7))
        self.dashed_circle = dashed_circle
        self.wait(max(0.05, 1.26))

        # Gap 16.20-20.78 clear left side except body (remove thermo and heat)
        self.play(
            FadeOut(self.thermo),
            FadeOut(self.heat_group),
            run_time=max(0.05, 1.2
        ))
        self.wait(max(0.05, 3.38))

        # Beat 7: 20.78-24.38 thermometer reappears, heat arrows orange, fill rises
        self.play(FadeIn(self.thermo), run_time=max(0.05, 0.6))
        self.heat_speed.set_value(1.0)
        self.heat_lines.set_color(ORANGE)
        self.heat_heads.set_fill(ORANGE)
        self.play(FadeIn(self.heat_group), run_time=max(0.05, 0.8))
        self.play(
            self.thermo_fluid.animate.stretch(1.2, 1, about_edge=DOWN),
            run_time=max(0.05, 0.7
        ))
        self.wait(max(0.05, 1.5))

        # Beat 8: 24.38-27.80 red X over thermometer, arrows freeze gray, label
        self.red_x2 = self.build_red_x()
        self.red_x2.move_to(np.array([-2.1, 1.95, 0]))
        self.label_no_heat = Text(
            "does NOT produce heat",
            font_size=24,
            weight="BOLD",
            color=RED
        )
        self.label_no_heat.next_to(self.red_x2, DOWN, buff=0.3)
        self.play(
            FadeIn(self.red_x2),
            FadeIn(self.label_no_heat),
            run_time=max(0.05, 0.5
        ))
        self.play(
            self.heat_speed.animate.set_value(0.0),
            self.heat_lines.animate.set_color(GREY),
            self.heat_heads.animate.set_fill(GREY),
            run_time=max(0.05, 2.92
        ))

        # Gap 27.80-28.18
        self.wait(max(0.05, 0.38))

        # Beat 9: 28.18-29.18 red X/label fade, arrows resume, fill rises
        self.play(
            FadeOut(self.red_x2),
            FadeOut(self.label_no_heat),
            run_time=max(0.05, 0.4
        ))
        self.play(
            self.heat_speed.animate.set_value(1.0),
            self.heat_lines.animate.set_color(ORANGE),
            self.heat_heads.animate.set_fill(ORANGE),
            self.thermo_fluid.animate.stretch(1.15, 1, about_edge=DOWN),
            run_time=max(0.05, 0.6
        ))

        # Gap 29.18-30.28
        self.wait(max(0.05, 1.10))

        # Beat 10: 30.28-32.30 thermo/arrows fade, electrode brightens, echo on pad
        self.play(
            FadeOut(self.thermo),
            FadeOut(self.heat_group),
            run_time=max(0.05, 0.6
        ))
        self.play(
            self.pad.animate.set_stroke(ORANGE, width=4),
            run_time=max(0.05, 0.3
        ))
        self.play(Indicate(self.pad, color=ORANGE, scale_factor=1.25), run_time=max(0.05, 0.35))
        self.play(Indicate(self.pad, color=ORANGE, scale_factor=1.25), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.42))

        # Gap 32.30-32.94
        self.wait(max(0.05, 0.64))

        # Beat 11: 32.94-38.18 pulses slow/brighten, source points flash, labels
        self.play(
            self.pulse_speed.animate.set_value(0.65),
            run_time=max(0.05, 0.5
        ))
        self.play(
            self.pulse_dots_group.animate.set_opacity(1.0),
            run_time=max(0.05, 0.3
        ))

        source_positions = [
            (np.array([-3.55, 2.55, 0]), "neurons"),
            (np.array([-3.55, -0.05, 0]), "muscles"),
            (np.array([-3.55, 1.20, 0]), "other tissues")
        ]
        self.source_points = VGroup()
        self.source_labels = VGroup()
        for pt, word in source_positions:
            dot = Dot(pt, radius=0.08, color=YELLOW, fill_opacity=1)
            self.source_points.add(dot)
            lab = Text(word, font_size=20, color=WHITE)
            if word == "neurons":
                lab.next_to(dot, LEFT, buff=0.15)
            elif word == "muscles":
                lab.next_to(dot, LEFT, buff=0.15)
            else:
                lab.next_to(dot, LEFT, buff=0.15)
            self.source_labels.add(lab)
        self.play(
            FadeIn(self.source_points),
            FadeIn(self.source_labels),
            run_time=max(0.05, 0.5
        ))

        self.flash_sources_cycle(duration_per_source=0.8)
        self.wait(max(0.05, 1.54))

        # Beat 12: 38.18-42.42 continue flashing, label acquisition system
        label_acq = Text(
            "acquisition system",
            font_size=22,
            color=WHITE
        )
        label_acq.next_to(self.box, DOWN, buff=0.3)
        self.play(FadeIn(label_acq), run_time=max(0.05, 0.4))
        self.flash_sources_cycle(duration_per_source=0.8)
        self.wait(max(0.05, 1.44))

        # Gap 42.42-46.42
        self.wait(max(0.05, 4.0))

        # Beat 13: 46.42-50.36 labels fade, points stop, glowing outline, clean pulse
        self.play(
            FadeOut(self.source_labels),
            FadeOut(self.source_points),
            run_time=max(0.05, 0.5
        ))
        self.glow = SurroundingRectangle(
            self.pad,
            color=YELLOW,
            buff=0.12,
            corner_radius=0.05
        )
        self.glow.set_stroke(width=5)
        self.play(Create(self.glow), run_time=max(0.05, 0.6))
        self.play(
            self.pulse_speed.animate.set_value(1.0),
            self.pulse_dots_group.animate.set_color(BLUE).set_opacity(0.9),
            run_time=max(0.05, 0.5
        ))
        self.wait(max(0.05, 2.34))

        # Gap 50.36-51.55
        self.wait(max(0.05, 1.19))

        # Beat 14: 51.55-55.74 glow dim gray, pad pulls away, pulses jagged/noisy, poor contact
        self.play(
            self.glow.animate.set_color(GREY).set_opacity(0.5),
            run_time=max(0.05, 0.4
        ))
        gap_shift = RIGHT * 0.4
        self.play(
            self.pad.animate.shift(gap_shift),
            run_time=max(0.05, 0.5
        ))
        # Update pulse start and wire start to new pad position
        self.pulse_start = self.pad.get_center()
        new_wire_left = self.pad.get_center() + RIGHT * 0.35
        self.wire.put_start_and_end_on(new_wire_left, self.box.get_left())

        self.create_noise_speckles()
        self.play(FadeIn(self.noise_speckles), run_time=max(0.05, 0.5))
        self.play(
            self.pulse_speed.animate.set_value(0.45),
            self.pulse_dots_group.animate.set_opacity(0.35),
            run_time=max(0.05, 0.5
        ))
        self.label_poor = Text(
            "poor contact",
            font_size=22,
            weight="BOLD",
            color=RED
        )
        self.label_poor.next_to(self.pad, DOWN, buff=0.3)
        self.play(FadeIn(self.label_poor), run_time=max(0.05, 0.4))
        self.play(
            self.indicator.animate.set_color(RED),
            run_time=max(0.05, 0.3
        ))
        self.wait(max(0.05, 1.59))

        # Beat 15: 55.74-58.48 static intensifies, screen waveform degrades, label reduced quality
        self.play(
            self.noise_speckles.animate.set_opacity(1.0),
            run_time=max(0.05, 0.3
        ))
        clean_wave = self.build_clean_waveform().move_to(self.screen.get_center())
        noisy_wave = self.build_noisy_waveform().move_to(self.screen.get_center())
        self.add(clean_wave)
        self.play(Transform(clean_wave, noisy_wave), run_time=max(0.05, 1.0))
        self.play(FadeOut(clean_wave), run_time=max(0.05, 0.0)) if False else None  # no-op never reached
        # Actually keep transformed noisy wave; remove clean after transform
        # Transform replaces clean with noisy; clean object now equals noisy
        label_signal = Text(
            "reduced signal quality / unreliable analysis",
            font_size=20,
            color=RED
        )
        label_signal.next_to(self.box, DOWN, buff=0.7)
        self.play(FadeIn(label_signal), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.94))

        # Beat 16: 58.48-59.17 panel slides in from right with definition
        panel = RoundedRectangle(
            width=4.5,
            height=2.8,
            corner_radius=0.15,
            fill_color="#1A1C22",
            fill_opacity=0.95,
            stroke_color=YELLOW,
            stroke_width=2
        )
        definition = Text(
            "Electrode: A conductive interface\n"
            "that detects biological electrical\n"
            "activity and transfers it to\n"
            "the recording system.",
            font_size=22,
            color=WHITE,
            line_spacing=0.8
        )
        definition.scale_to_fit_width(3.9)
        definition.move_to(panel.get_center())
        panel_group = VGroup(panel, definition)
        panel_group.move_to(np.array([9.5, 0.0, 0]))
        self.play(
            panel_group.animate.move_to(np.array([4.7, 0.0, 0])),
            run_time=max(0.05, 0.69
        ))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def build_body(self):
        head = Circle(radius=0.42, color=GREY_B, fill_opacity=1, stroke_width=0)
        head.move_to(np.array([0, 2.35, 0]))
        torso = Polygon(
            [-0.48, 1.35, 0], [0.48, 1.35, 0],
            [0.38, -1.0, 0], [-0.32, -1.0, 0],
            fill_color=GREY_B, fill_opacity=1, stroke_width=0
        )
        left_arm = Line(
            [-0.48, 1.15, 0], [-0.98, -0.05, 0],
            stroke_color=GREY_B, stroke_width=13
        )
        right_arm = Line(
            [0.48, 1.15, 0], [0.98, -0.05, 0],
            stroke_color=GREY_B, stroke_width=13
        )
        left_leg = Line(
            [-0.25, -1.0, 0], [-0.42, -2.75, 0],
            stroke_color=GREY_B, stroke_width=13
        )
        right_leg = Line(
            [0.2, -1.0, 0], [0.32, -2.75, 0],
            stroke_color=GREY_B, stroke_width=13
        )
        group = VGroup(head, torso, left_arm, right_arm, left_leg, right_leg)
        group.scale_to_fit_height(6.0)
        return group

    def build_thermometer(self):
        outer = Rectangle(
            width=0.34,
            height=1.5,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=BLUE_E,
            fill_opacity=0.08
        )
        outer.move_to(np.array([0, 0.15, 0]))
        bulb = Circle(
            radius=0.26,
            fill_color=RED,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        )
        bulb.move_to(np.array([0, -0.72, 0]))
        fluid = Rectangle(
            width=0.2,
            height=0.45,
            fill_color=RED,
            fill_opacity=1,
            stroke_width=0
        )
        fluid.move_to(np.array([0, -0.5, 0]))
        ticks = VGroup()
        for py in [-0.55, -0.25, 0.05, 0.35]:
            tick = Line(
                [-0.22, py, 0], [0.22, py, 0],
                color=WHITE,
                stroke_width=1.5
            )
            ticks.add(tick)
        group = VGroup(outer, bulb, fluid, ticks)
        group.scale_to_fit_height(2.7)
        return group, fluid, ticks, bulb

    def create_heat_arrows(self, start, end):
        # Static wavy paths + moving arrowheads
        self.heat_lines = VGroup()
        self.heat_heads = VGroup()
        self.heat_funcs = []
        self.heat_base_arrows = []
        for i in range(3):
            amp = 0.12 + i * 0.05
            phase = i * 0.35
            func = self.make_heat_func(start, end, amp, phase)
            path = ParametricFunction(
                func,
                t_range=[0, 1],
                color=ORANGE,
                stroke_width=4,
                stroke_opacity=0.5
            )
            self.heat_lines.add(path)
            arrow = Polygon(
                [0.12, 0, 0],
                [-0.08, 0.07, 0],
                [-0.08, -0.07, 0],
                fill_color=ORANGE,
                fill_opacity=1,
                stroke_width=0
            )
            self.heat_heads.add(arrow)
            self.heat_base_arrows.append(arrow.copy())
            self.heat_funcs.append(func)

        self.heat_heads.add_updater(self.make_heat_heads_updater())
        self.heat_group = VGroup(self.heat_lines, self.heat_heads)

    def make_heat_func(self, start, end, amp, phase):
        def func(t):
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t + amp * np.sin(
                2 * np.pi * (t * 1.6 + phase)
            )
            return np.array([x, y, 0])
        return func

    def make_heat_heads_updater(self):
        def updater(m, dt):
            speed = self.heat_speed.get_value()
            t_base = self.time_tracker.get_value() * speed * 0.45
            for i, head in enumerate(self.heat_heads):
                t = (t_base + i * 0.33) % 1
                p = self.heat_funcs[i](t)
                p2 = self.heat_funcs[i](t + 0.001)
                angle = np.arctan2(p2[1] - p[1], p2[0] - p[0])
                head.become(
                    self.heat_base_arrows[i].copy().rotate(angle).move_to(p)
                )
        return updater

    def build_pad(self):
        pad = RoundedRectangle(
            width=0.75,
            height=0.5,
            corner_radius=0.12,
            fill_color=GREY,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2
        )
        wire_dot = Circle(
            radius=0.07,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
        wire_dot.move_to(pad.get_center())
        return VGroup(pad, wire_dot)

    def create_pulses(self):
        self.pulse_dots_group = VGroup()
        for _ in range(3):
            dot = Dot(radius=0.055, color=BLUE, fill_opacity=1)
            self.pulse_dots_group.add(dot)
        self.pulse_dots_group.add_updater(self.make_pulses_updater())
        self.add(self.pulse_dots_group)

    def make_pulses_updater(self):
        def updater(m, dt):
            speed = self.pulse_speed.get_value()
            t_base = self.time_tracker.get_value() * speed * 0.55
            for i, dot in enumerate(self.pulse_dots_group):
                t = (t_base + i * 0.33) % 1
                point = self.pulse_start + (self.pulse_end - self.pulse_start) * t
                dot.move_to(point)
                if t < 0.05 or t > 0.95:
                    dot.set_opacity(0.2)
                else:
                    dot.set_opacity(0.9)
        return updater

    def build_recording_box(self):
        box = Rectangle(
            width=2.0,
            height=1.3,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_C,
            stroke_width=2
        )
        label = Text("Recording System", font_size=18, color=WHITE)
        label.move_to(box.get_center() + DOWN * 0.4)
        self.indicator = Circle(
            radius=0.07,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=0
        )
        self.indicator.move_to(box.get_top() + LEFT * 0.5)
        self.screen = Rectangle(
            width=0.85,
            height=0.45,
            fill_color="#0B0C10",
            fill_opacity=1,
            stroke_color=GREY,
            stroke_width=1
        )
        self.screen.move_to(box.get_center() + UP * 0.35)
        return VGroup(box, label, self.indicator, self.screen)

    def start_indicator_blink(self):
        self.indicator.add_updater(self.make_indicator_updater())

    def make_indicator_updater(self):
        def updater(m, dt):
            speed = self.pulse_speed.get_value()
            val = np.sin(2 * np.pi * self.time_tracker.get_value() * speed * 0.55)
            m.set_opacity(max(0.0, val))
        return updater

    def build_red_x(self):
        line1 = Line(
            [-0.25, -0.25, 0], [0.25, 0.25, 0],
            color=RED,
            stroke_width=8
        )
        line2 = Line(
            [-0.25, 0.25, 0], [0.25, -0.25, 0],
            color=RED,
            stroke_width=8
        )
        return VGroup(line1, line2)

    def create_noise_speckles(self):
        self.noise_speckles = VGroup()
        y_wire = 0.40
        for _ in range(20):
            x = np.random.uniform(
                self.pad.get_center()[0] + 0.1,
                self.box.get_left()[0] - 0.1
            )
            y = y_wire + np.random.uniform(-0.15, 0.15)
            dot = Dot(
                point=np.array([x, y, 0]),
                radius=0.025,
                color=GREY,
                fill_opacity=0.7
            )
            self.noise_speckles.add(dot)
        self.add(self.noise_speckles)

    def build_clean_waveform(self):
        pts = []
        x_vals = np.linspace(-0.35, 0.35, 20)
        for x in x_vals:
            y = 0.15 * np.sin(2 * np.pi * x * 3)
            pts.append(np.array([x, y, 0]))
        wave = VMobject(stroke_color=GREEN, stroke_width=3)
        wave.set_points_as_corners(pts)
        return wave

    def build_noisy_waveform(self):
        pts = []
        x_vals = np.linspace(-0.35, 0.35, 20)
        np.random.seed(42)
        for x in x_vals:
            y = 0.12 * np.sin(2 * np.pi * x * 1.5) + np.random.uniform(-0.12, 0.12)
            pts.append(np.array([x, y, 0]))
        wave = VMobject(stroke_color=RED, stroke_width=3)
        wave.set_points_as_corners(pts)
        return wave

    def flash_sources_cycle(self, duration_per_source):
        for dot in self.source_points:
            self.play(
                Indicate(dot, color=YELLOW, scale_factor=1.3),
                run_time=max(0.05, duration_per_source * 0.4
            ))
            temp_pulse = Dot(
                dot.get_center(),
                radius=0.06,
                color=YELLOW,
                fill_opacity=1
            )
            self.add(temp_pulse)
            self.play(
                temp_pulse.animate.move_to(self.pad.get_center()).set_opacity(0),
                run_time=max(0.05, duration_per_source * 0.6),
                rate_func=linear
            )
            self.remove(temp_pulse)