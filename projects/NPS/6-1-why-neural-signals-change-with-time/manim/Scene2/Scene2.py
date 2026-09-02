ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 1. Heading and definition box
        heading = Text("Stationary Signal", font_size=52, weight="BOLD", color=WHITE)
        heading.to_edge(UP, buff=0.6)

        def_parts = [
            Text("Stationary: ", font_size=30, color=WHITE),
            Text("statistical", font_size=30, color=WHITE),
            Text(" and ", font_size=30, color=WHITE),
            Text("spectral", font_size=30, color=WHITE),
            Text(" characteristics ", font_size=30, color=WHITE),
            Text("essentially constant", font_size=30, color=WHITE),
            Text(" over time", font_size=30, color=WHITE),
        ]
        def_text = VGroup(*def_parts).arrange(RIGHT, buff=0.0)
        if def_text.width > 10.5:
            def_text.scale_to_fit_width(10.5)

        def_box = SurroundingRectangle(
            def_text,
            color=BLUE,
            buff=0.35,
            corner_radius=0.18,
            fill_color=BLUE,
            fill_opacity=0.10,
            stroke_width=2,
        )
        definition_group = VGroup(def_box, def_text)
        definition_group.to_edge(DOWN, buff=0.55)

        # 0.00 - 1.50
        self.play(FadeIn(heading), FadeIn(definition_group), run_time=max(0.05, 1.50))

        # 1.50 - 2.48 pause
        self.wait(max(0.05, 0.98))

        # 2.48 - 9.34 pulse once, then highlight key phrases in sequence
        self.play(
            def_box.animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=0.18),
            run_time=max(0.05, 0.50),
        )
        self.play(
            def_box.animate.set_stroke(BLUE, width=2).set_fill(BLUE, opacity=0.10),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.20))

        # "statistical"
        self.play(def_parts[1].animate.set_color(YELLOW), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 1.10))
        self.play(def_parts[1].animate.set_color(WHITE), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.15))

        # "spectral"
        self.play(def_parts[3].animate.set_color(YELLOW), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.95))
        self.play(def_parts[3].animate.set_color(WHITE), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.15))

        # "essentially constant"
        self.play(def_parts[5].animate.set_color(YELLOW), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.90))
        self.play(def_parts[5].animate.set_color(WHITE), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.11))

        # 9.34 - 10.06 pause
        self.wait(max(0.05, 0.72))

        # 10.06 - 15.20 generator with constant vibration
        body_rect = Rectangle(
            width=2.2,
            height=0.9,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=GOLD,
            stroke_width=2,
        )
        left_cap = Circle(
            radius=0.45,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=GOLD,
            stroke_width=2,
        )
        right_cap = Circle(
            radius=0.45,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=GOLD,
            stroke_width=2,
        )
        left_cap.move_to(body_rect.get_left())
        right_cap.move_to(body_rect.get_right())
        body_capsule = VGroup(left_cap, body_rect, right_cap)

        turb_center = right_cap.get_right() + RIGHT * 0.12
        turbine_circle = Circle(
            radius=0.38,
            color=TEAL,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        turbine_circle.move_to(turb_center)
        turbine = VGroup(turbine_circle)
        for angle in [0, 2 * PI / 3, 4 * PI / 3]:
            blade = Line(turb_center, turb_center + RIGHT * 0.33)
            blade.rotate(angle, about_point=turb_center)
            blade.set_stroke(WHITE, width=2)
            turbine.add(blade)

        generator_group = VGroup(body_capsule, turbine).move_to(np.array([-4.5, 1.7, 0.0]))

        self.play(GrowFromCenter(generator_group), run_time=max(0.05, 1.20))

        base_gen_center = generator_group.get_center()
        gen_phase = 0.0

        def vibrate(mob, dt):
            nonlocal gen_phase
            gen_phase += dt * 25.0
            mob.move_to(base_gen_center + UP * 0.03 * np.sin(gen_phase))

        generator_group.add_updater(vibrate)
        self.wait(max(0.05, 3.94))

        # 15.20 - 17.28 steady scrolling waveform below generator
        WAVE_AMP = 0.55
        WAVE_WAVELENGTH = 3.2
        SCROLL_SPEED = 0.25

        wave_x = np.linspace(-10.0, 18.0, 500)
        wave_y = WAVE_AMP * np.sin(2 * PI * wave_x / WAVE_WAVELENGTH)
        wave_line = VMobject(stroke_color=GREEN, stroke_width=4)
        wave_line.set_points_as_corners(
            [np.array([x, y, 0.0]) for x, y in zip(wave_x, wave_y)]
        )

        axis_line = Line(LEFT * 7.2, RIGHT * 7.2, color=GREY_B, stroke_width=2).shift(DOWN * 0.5)
        wave_line.shift(DOWN * 0.5)

        connection_line = Line(
            generator_group.get_bottom(),
            axis_line.get_left(),
            color=YELLOW,
            stroke_opacity=0.22,
            stroke_width=2,
        )
        waveform_group = VGroup(axis_line, wave_line, connection_line)

        def scroll_wave(mob, dt):
            mob.shift(LEFT * SCROLL_SPEED * dt)

        wave_line.add_updater(scroll_wave)

        self.play(
            Create(wave_line),
            FadeIn(axis_line),
            FadeIn(connection_line),
            run_time=max(0.05, 2.08),
        )

        # 17.28 - 20.54 three time-window markers
        marker_data = [(-4.5, "1 s"), (0.0, "5 s"), (4.5, "1 min")]
        markers = []
        for x_pos, label in marker_data:
            tick = Line(UP * 0.12, DOWN * 0.12, color=WHITE, stroke_width=3)
            label_text = Text(label, font_size=24, weight="BOLD", color=WHITE)
            marker = VGroup(tick, label_text).arrange(DOWN, buff=0.10)
            marker.move_to(np.array([x_pos, 0.35, 0.0]))
            markers.append(marker)
        markers_group = VGroup(*markers)

        per_marker_time = 3.26 / 3
        for marker in markers:
            self.play(FadeIn(marker), run_time=max(0.05, 0.65))
            self.wait(max(0.05, per_marker_time - 0.65))

        # 20.54 - 23.80 highlight 1 s marker, inset appears
        self.play(markers[0].animate.set_color(YELLOW).scale(1.15), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.25))

        inset_box = Rectangle(
            width=3.8,
            height=2.0,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.12,
            stroke_width=2,
        )
        inset_box.move_to(np.array([4.8, 2.5, 0.0]))
        inset_tag = Text("1 s", font_size=24, weight="BOLD", color=YELLOW)
        inset_tag.move_to(inset_box.get_top() + DOWN * 0.4)

        inset_x = np.linspace(-1.6, 1.6, 200)
        inset_y = WAVE_AMP * np.sin(2 * PI * inset_x / WAVE_WAVELENGTH)
        inset_wave = VMobject(stroke_color=GREEN, stroke_width=3)
        inset_wave.set_points_as_corners(
            [np.array([x, y, 0.0]) for x, y in zip(inset_x, inset_y)]
        )
        inset_axis = Line(LEFT * 1.6, RIGHT * 1.6, color=GREY_B, stroke_width=2)
        inset_plot = VGroup(inset_axis, inset_wave).move_to(
            inset_box.get_center() + DOWN * 0.15
        )
        inset_group = VGroup(inset_box, inset_plot, inset_tag)

        self.play(GrowFromCenter(inset_group), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 1.66))

        # 23.80 - 27.00 5 s marker highlights, 1 s dims, inset label updates
        self.play(
            markers[1].animate.set_color(YELLOW).scale(1.15),
            markers[0].animate.set_color(WHITE).scale(1 / 1.15),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.15))
        new_label = Text("5 s", font_size=24, weight="BOLD", color=YELLOW)
        new_label.move_to(inset_tag.get_center())
        self.play(Transform(inset_tag, new_label), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 1.90))

        # 27.00 - 29.44 1 min marker highlights, 5 s dims
        self.play(
            markers[2].animate.set_color(YELLOW).scale(1.15),
            markers[1].animate.set_color(WHITE).scale(1 / 1.15),
            run_time=max(0.05, 0.65),
        )
        self.wait(max(0.05, 0.15))
        new_label = Text("1 min", font_size=24, weight="BOLD", color=YELLOW)
        new_label.move_to(inset_tag.get_center())
        self.play(Transform(inset_tag, new_label), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 1.19))

        # 29.44 - 32.88 markers dim, inset fades, definition box highlights briefly
        self.play(
            markers[2].animate.set_color(WHITE).scale(1 / 1.15),
            run_time=max(0.05, 0.50),
        )
        self.play(
            inset_group.animate.scale(0.6).set_opacity(0),
            run_time=max(0.05, 0.70),
        )
        self.remove(inset_group)

        self.play(
            def_box.animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=0.18),
            run_time=max(0.05, 0.70),
            rate_func=there_and_back,
        )
        self.wait(max(0.05, 1.54))

        # 32.88 - 39.40 definition box pulses on "Stationary", generator and wave continue
        self.play(
            def_parts[0].animate.set_color(YELLOW),
            def_box.animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=0.18),
            run_time=max(0.05, 0.65),
        )
        self.wait(max(0.05, 0.60))
        self.play(
            def_parts[0].animate.set_color(WHITE),
            def_box.animate.set_stroke(BLUE, width=2).set_fill(BLUE, opacity=0.10),
            run_time=max(0.05, 0.65),
        )
        self.wait(max(0.05, 4.62))

        # 39.40 - 44.62 generator and waveform fade out, faint waveform backdrop appears
        generator_group.clear_updaters()
        wave_line.clear_updaters()
        self.play(
            FadeOut(generator_group, waveform_group, markers_group),
            run_time=max(0.05, 1.30),
        )

        glyph_group = VGroup()
        center_y = definition_group.get_center()[1]
        for x_center in [-5.0, -2.5, 0.0, 2.5, 5.0]:
            gx = np.linspace(-0.5, 0.5, 40)
            small_wave = VMobject(stroke_color=GREY_B, stroke_width=2)
            small_wave.set_points_as_corners(
                [
                    np.array([x, 0.12 * np.sin(2 * PI * x / 1.8), 0.0])
                    for x in gx
                ]
            )
            small_wave.move_to(np.array([x_center, center_y, 0.0]))
            glyph_group.add(small_wave)

        glyph_group.set_opacity(0.18)
        glyph_group.set_z_index(0)
        definition_group.set_z_index(1)
        heading.set_z_index(1)

        self.play(FadeIn(glyph_group), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 2.72))

        # 44.62 - 45.48 final hold, then fade out
        self.wait(max(0.05, 0.60))
        self.play(FadeOut(heading, definition_group, glyph_group), run_time=max(0.05, 0.26))