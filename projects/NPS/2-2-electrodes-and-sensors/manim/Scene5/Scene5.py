ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene5(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- previous two-column layout placeholder (from Scene 4) ---
        prev_left_header = Text("Advantages", font_size=34, weight="BOLD", color=WHITE)
        prev_left_header.move_to(np.array([-3.3, 2.5, 0]))
        prev_right_header = Text("Limitations", font_size=34, weight="BOLD", color=WHITE)
        prev_right_header.move_to(np.array([3.3, 2.5, 0]))

        prev_left_cards = VGroup(*[
            Rectangle(width=4.8, height=0.6, fill_color=GREY, fill_opacity=0.25,
                      stroke_color=GREY_B, stroke_width=2)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.28).move_to(np.array([-3.3, 0.4, 0]))

        prev_right_cards = VGroup(*[
            Rectangle(width=4.8, height=0.6, fill_color=GREY, fill_opacity=0.25,
                      stroke_color=GREY_B, stroke_width=2)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.28).move_to(np.array([3.3, 0.4, 0]))

        prev_layout = VGroup(prev_left_header, prev_right_header, prev_left_cards, prev_right_cards)

        # --- anatomical cross-section: skin band, muscle tissue, fibers ---
        skin_band = Rectangle(width=12, height=0.34, fill_color=PINK, fill_opacity=0.9,
                              stroke_color=WHITE, stroke_width=2)
        skin_band.move_to(np.array([0, 0.85, 0]))

        muscle_region = Rectangle(width=12, height=4.0, fill_color=MAROON, fill_opacity=0.9,
                                  stroke_color=WHITE, stroke_width=2)
        muscle_region.move_to(np.array([0, -1.32, 0]))

        skin_label = Text("skin", font_size=22, color=WHITE)
        skin_label.next_to(skin_band, UP, buff=0.12).shift(LEFT * 4.5)

        muscle_label = Text("muscle", font_size=22, color=WHITE)
        muscle_label.move_to(np.array([3.6, -2.8, 0]))

        fiber_lines = VGroup()
        for i in range(14):
            y = 0.5 - i * 0.26
            fiber_lines.add(
                Line(LEFT * 5.8 + UP * y, RIGHT * 5.8 + UP * y,
                     color=WHITE, stroke_width=2, stroke_opacity=0.28)
            )

        cross_section = VGroup(muscle_region, fiber_lines, skin_band, skin_label, muscle_label)

        self.add(prev_layout)
        self.play(
            FadeOut(prev_layout),
            FadeIn(cross_section),
            run_time=max(0.05, 0.58
        ))

        # --- beat 2: needle descends through skin into muscle ---
        tip_bottom_initial = 3.0
        tip_top_initial = tip_bottom_initial + 0.2
        shaft_center_initial_y = tip_top_initial + 1.1  # shaft height 2.2

        needle_shaft = Rectangle(width=0.12, height=2.2,
                                 fill_color=GREY_B, fill_opacity=1,
                                 stroke_color=WHITE, stroke_width=1.5)
        needle_shaft.move_to(np.array([0, shaft_center_initial_y, 0]))

        needle_tip = Polygon(
            [-0.06, tip_top_initial, 0],
            [0.06, tip_top_initial, 0],
            [0, tip_bottom_initial, 0],
            fill_color=GREY_B, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1.5
        )

        needle = VGroup(needle_shaft, needle_tip).set_z_index(6)

        tip_final_point = np.array([0, -0.8, 0])
        insertion_distance = tip_bottom_initial - tip_final_point[1]

        self.add(needle)
        self.play(needle.animate.shift(DOWN * insertion_distance), run_time=max(0.05, 1.06))
        self.wait(max(0.05, 1.00))  # gap to 2.64

        # --- beat 3: tip rests among muscle fibers ---
        tip_ring = Circle(radius=0.15, color=YELLOW, fill_opacity=0,
                          stroke_width=3).move_to(tip_final_point)
        self.play(FadeIn(tip_ring), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.56))
        self.wait(max(0.05, 0.80))  # gap to 4.40

        # --- beat 4: faded surface electrode and distance indicator ---
        skin_top_y = skin_band.get_top()[1]

        surface_electrode = Ellipse(width=0.85, height=0.24,
                                    fill_color=GREY, fill_opacity=0.45,
                                    stroke_color=WHITE, stroke_width=2.5)
        surface_electrode.move_to(np.array([-2.8, skin_top_y + 0.12, 0]))
        surface_electrode.set_opacity(0.55)

        distance_line = DashedLine(surface_electrode.get_center(), tip_final_point,
                                   color=YELLOW, stroke_width=3, dash_length=0.12)
        distance_line.set_opacity(0.65)

        self.play(
            FadeIn(surface_electrode),
            FadeIn(distance_line),
            run_time=max(0.05, 1.20
        ))
        self.wait(max(0.05, 0.74))  # gap to 6.34

        # --- beat 5: sparks at tip plus pulses travelling up the wire ---
        spark_offsets = [
            np.array([0.18, 0.12, 0]),
            np.array([-0.18, 0.12, 0]),
            np.array([0, 0.22, 0]),
            np.array([0.22, -0.12, 0]),
            np.array([-0.22, -0.12, 0]),
            np.array([0, -0.22, 0])
        ]
        spark_group = VGroup(*[
            Dot(point=tip_final_point + offset, radius=0.035, color=YELLOW, fill_opacity=1)
            for offset in spark_offsets
        ])
        spark_group.set_z_index(8)

        shaft_top_final_y = shaft_center_initial_y + 1.1 - insertion_distance
        wire_end = np.array([0, shaft_top_final_y, 0])
        wire = Line(tip_final_point, wire_end,
                    color=YELLOW, stroke_width=3, stroke_opacity=0.9).set_z_index(7)

        signal_source_label = Text("signal source", font_size=22, color=YELLOW)
        signal_source_label.next_to(tip_final_point, RIGHT, buff=0.25)

        self.play(
            FadeIn(spark_group),
            FadeIn(wire),
            Write(signal_source_label),
            run_time=max(0.05, 0.40
        ))

        for _ in range(3):
            pulse = Dot(point=tip_final_point, radius=0.06, color=YELLOW, fill_opacity=1)
            pulse.set_z_index(9)
            self.add(pulse)
            self.play(pulse.animate.move_to(wire_end), run_time=max(0.05, 0.50))
            self.remove(pulse)
            self.wait(max(0.05, 0.20))
        self.wait(max(0.05, 0.20))
        self.wait(max(0.05, 0.90))  # gap to 9.94

        # --- beat 6: clinical EMG label + highlighted individual muscle fiber ---
        clinical_label = Text("Clinical EMG", font_size=30, weight="BOLD", color=WHITE)
        clinical_label.to_corner(UP + LEFT, buff=0.5)

        highlight_fiber = Line(LEFT * 5.5 + UP * tip_final_point[1],
                               RIGHT * 5.5 + UP * tip_final_point[1],
                               color=YELLOW, stroke_width=7, stroke_opacity=0.9)
        highlight_fiber.set_z_index(2)

        self.play(FadeIn(clinical_label), run_time=max(0.05, 0.60))
        self.play(Create(highlight_fiber), run_time=max(0.05, 0.80))
        self.play(Indicate(spark_group, scale_factor=1.3, color=YELLOW), run_time=max(0.05, 0.50))

        pulse = Dot(point=tip_final_point, radius=0.06, color=YELLOW, fill_opacity=1)
        pulse.set_z_index(9)
        self.add(pulse)
        self.play(pulse.animate.move_to(wire_end), run_time=max(0.05, 0.50))
        self.remove(pulse)
        self.wait(max(0.05, 0.14))
        self.wait(max(0.05, 1.42))  # gap to 13.90

        # --- beat 7: fiber's own faint electrical activity, synchronized pulses ---
        fiber_activity = FunctionGraph(
            lambda x: 0.10 * np.sin(8 * x),
            x_range=[-5.5, 5.5, 0.05],
            color=YELLOW, stroke_width=2, stroke_opacity=0.7
        ).scale_to_fit_width(10.5).move_to(np.array([0, tip_final_point[1], 0]))
        fiber_activity.set_z_index(3)

        self.play(Create(fiber_activity), run_time=max(0.05, 0.70))
        self.play(
            fiber_activity.animate.set_opacity(0.35),
            spark_group.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=max(0.05, 0.50
        ))

        pulse = Dot(point=tip_final_point, radius=0.06, color=YELLOW, fill_opacity=1)
        pulse.set_z_index(9)
        self.add(pulse)
        self.play(pulse.animate.move_to(wire_end), run_time=max(0.05, 0.50))
        self.remove(pulse)
        self.wait(max(0.05, 0.40))
        self.wait(max(0.05, 1.34))  # gap to 17.34

        # --- beat 8: slight zoom toward needle tip inside muscle ---
        zoom_factor = 0.85
        self.play(
            self.camera.frame.animate.scale(zoom_factor).move_to(tip_final_point),
            run_time=max(0.05, 1.00
        ))
        self.play(Indicate(muscle_label, scale_factor=1.1, color=WHITE), run_time=max(0.05, 0.48))
        self.play(
            self.camera.frame.animate.scale(1 / zoom_factor).move_to(ORIGIN),
            run_time=max(0.05, 0.56
        ))

        # --- beat 9: waveform comparison panel ---
        wave_panel_rect = Rectangle(width=6.4, height=3.2,
                                    fill_color=GREY, fill_opacity=0.9,
                                    stroke_color=WHITE, stroke_width=2)
        wave_panel_rect.move_to(np.array([3.0, 0.5, 0]))
        wave_panel_rect.set_z_index(5)

        needle_wave = FunctionGraph(
            lambda x: 1.1 * np.sin(4 * x),
            x_range=[-1.8, 1.8, 0.01],
            color=TEAL, stroke_width=4
        ).scale_to_fit_width(2.6)

        surface_wave = FunctionGraph(
            lambda x: 0.35 * np.sin(4 * x) + 0.15 * np.sin(17 * x),
            x_range=[-1.8, 1.8, 0.01],
            color=PURPLE, stroke_width=2.5
        ).scale_to_fit_width(2.6)

        needle_label = Text("needle electrode", font_size=22, color=TEAL)
        surface_label = Text("surface electrode", font_size=22, color=GREY_B)

        left_wave_group = VGroup(needle_wave, needle_label).arrange(DOWN, buff=0.2)
        right_wave_group = VGroup(surface_wave, surface_label).arrange(DOWN, buff=0.2)
        wave_content = VGroup(left_wave_group, right_wave_group).arrange(RIGHT, buff=0.7)
        wave_content.move_to(wave_panel_rect.get_center())
        wave_content.set_z_index(6)

        arrow_to_surface = Arrow(
            surface_electrode.get_right() + RIGHT * 0.1,
            surface_wave.get_left() + LEFT * 0.1,
            buff=0.2,
            color=WHITE,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.08
        )
        arrow_to_surface.set_opacity(0.8)
        arrow_to_surface.set_z_index(6)

        wave_all = VGroup(wave_panel_rect, wave_content, arrow_to_surface)

        self.play(FadeIn(wave_panel_rect), run_time=max(0.05, 0.50))
        self.play(FadeIn(left_wave_group), run_time=max(0.05, 0.50))
        self.play(FadeIn(right_wave_group), run_time=max(0.05, 0.50))
        self.play(surface_electrode.animate.set_opacity(0.25), run_time=max(0.05, 0.40))
        self.play(FadeIn(arrow_to_surface), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 1.04))
        self.wait(max(0.05, 0.98))  # gap to 23.90

        # --- beat 10: red warning tint/glow + "invasive" label ---
        self.play(FadeOut(wave_all), run_time=max(0.05, 0.50))

        puncture_point = np.array([0, skin_top_y, 0])

        puncture_glow = Circle(radius=0.24, color=RED,
                               fill_color=RED, fill_opacity=0.18,
                               stroke_color=RED, stroke_width=3)
        puncture_glow.move_to(puncture_point)
        puncture_glow.set_z_index(8)

        invasive_label = Text("invasive", font_size=24, color=RED)
        invasive_label.next_to(puncture_glow, RIGHT, buff=0.25)

        self.play(
            FadeIn(puncture_glow),
            Write(invasive_label),
            run_time=max(0.05, 0.50
        ))
        self.play(
            puncture_glow.animate.scale(1.2).set_opacity(0.7),
            rate_func=there_and_back,
            run_time=max(0.05, 0.40
        ))
        self.wait(max(0.05, 0.72))  # gap to 26.02

        # --- beat 11: discomfort marks + slight muscle fiber quiver ---
        discomfort_lines = VGroup()
        for ang_deg in [30, 90, 150, 210, 270, 330]:
            direction = np.array([
                np.cos(np.deg2rad(ang_deg)),
                np.sin(np.deg2rad(ang_deg)),
                0
            ])
            discomfort_lines.add(
                Line(puncture_point, puncture_point + direction * 0.35,
                     color=RED, stroke_width=2, stroke_opacity=0.6)
            )
        discomfort_lines.set_z_index(9)

        self.play(FadeIn(discomfort_lines), run_time=max(0.05, 0.40))
        self.play(
            fiber_lines.animate.shift(UP * 0.03),
            rate_func=there_and_back,
            run_time=max(0.05, 0.42
        ))

        # --- beat 12: final calm hold ---
        self.wait(max(0.05, 0.84))