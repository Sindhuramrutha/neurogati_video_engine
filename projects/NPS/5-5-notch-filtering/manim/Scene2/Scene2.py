ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- build left-side diagram: stick figure + electrode ---
        def build_stick_figure():
            head = Circle(radius=0.28, color=WHITE, stroke_width=3, fill_opacity=0)
            head.move_to(np.array([0, 1.25, 0]))
            torso = Line(np.array([0, 0.9, 0]), np.array([0, -0.25, 0]), color=WHITE, stroke_width=4)
            arm = Line(np.array([-0.75, 0.4, 0]), np.array([0.8, 0.15, 0]), color=WHITE, stroke_width=4)
            leg1 = Line(np.array([0, -0.25, 0]), np.array([-0.4, -1.1, 0]), color=WHITE, stroke_width=4)
            leg2 = Line(np.array([0, -0.25, 0]), np.array([0.4, -1.1, 0]), color=WHITE, stroke_width=4)
            electrode = Dot(radius=0.12, color=RED, fill_opacity=1)
            electrode.move_to(np.array([0.8, 0.15, 0]))
            wire = Line(np.array([0.8, 0.15, 0]), np.array([0.8, -1.6, 0]), color=GREY, stroke_width=2)
            return VGroup(head, torso, arm, leg1, leg2, electrode, wire)

        stick = build_stick_figure()
        stick.move_to(np.array([-4.2, 0.2, 0]))

        # --- wall power outlet ---
        def build_outlet():
            plate = Rectangle(
                height=1.1,
                width=0.8,
                fill_color=WHITE,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=3,
            )
            hole1 = Rectangle(
                height=0.25,
                width=0.13,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )
            hole1.move_to(np.array([-0.15, 0.1, 0]))
            hole2 = Rectangle(
                height=0.25,
                width=0.13,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )
            hole2.move_to(np.array([0.15, -0.1, 0]))
            return VGroup(plate, hole1, hole2)

        outlet = build_outlet()
        outlet.move_to(np.array([-0.9, 0.5, 0]))

        # --- faint wavy electromagnetic field lines ---
        def build_wavy_line(start, end, amp=0.1, cycles=5, phase=0.0):
            start = np.array(start)
            end = np.array(end)
            direction = end - start
            length = np.linalg.norm(direction)
            unit = direction / length
            normal = np.array([-unit[1], unit[0], 0])
            points = []
            for t in np.linspace(0, 1, 200):
                pt = start + unit * (t * length) + normal * amp * np.sin(cycles * 2 * PI * t + phase)
                points.append(pt)
            wave = VMobject(color=YELLOW, stroke_width=2, fill_opacity=0)
            wave.set_points_as_corners(points)
            return wave

        start_field = np.array([-0.5, 0.55, 0])
        end_field = np.array([-3.35, 0.35, 0])
        field_lines = VGroup(
            build_wavy_line(start_field, end_field, amp=0.08, cycles=4, phase=0.0),
            build_wavy_line(start_field + np.array([0, 0.08, 0]), end_field + np.array([0, -0.06, 0]), amp=0.12, cycles=6, phase=1.0),
            build_wavy_line(start_field + np.array([0, -0.08, 0]), end_field + np.array([0, 0.06, 0]), amp=0.10, cycles=5, phase=2.0),
            build_wavy_line(start_field + np.array([0, 0.16, 0]), end_field + np.array([0, -0.12, 0]), amp=0.15, cycles=7, phase=3.0),
            build_wavy_line(start_field + np.array([0, -0.16, 0]), end_field + np.array([0, 0.12, 0]), amp=0.09, cycles=3, phase=4.0),
        )
        field_lines.set_opacity(0.25)

        # --- frequency spectrum ---
        axes = Axes(
            x_range=[0, 100, 10],
            y_range=[0, 1.2, 0.2],
            x_length=6.0,
            y_length=3.4,
            axis_config={"color": GREY, "stroke_width": 2},
            tips=False,
        )

        x_label = Text("Frequency (Hz)", font_size=28, color=GREY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.25)
        y_label = Text("Magnitude", font_size=28, color=GREY).rotate(PI / 2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.25)

        bg_curve = axes.plot(
            lambda x: 0.15 + 0.05 * np.sin(0.18 * x) + 0.04 * np.cos(0.11 * x),
            x_range=[0, 100],
            color=GREY,
            stroke_width=3,
        )

        bg_y_at_50 = 0.15 + 0.05 * np.sin(0.18 * 50) + 0.04 * np.cos(0.11 * 50)
        peak_line = Line(
            axes.c2p(50, bg_y_at_50),
            axes.c2p(50, 1.05),
            color=RED,
            stroke_width=12,
        )

        peak_label_50 = Text("50 Hz", font_size=26, color=RED, weight="BOLD")
        peak_label_50.move_to(axes.c2p(50, -0.35))

        # extra narrow-band tick labels, useful after camera zoom
        extra_ticks = VGroup()
        for val in (45, 50, 55):
            tick = Text(str(val), font_size=18, color=GREY)
            tick.move_to(axes.c2p(val, -0.12))
            extra_ticks.add(tick)

        spectrum_group = VGroup(
            axes,
            x_label,
            y_label,
            bg_curve,
            peak_line,
            peak_label_50,
            extra_ticks,
        )
        spectrum_group.move_to(np.array([3.0, 0.2, 0]))

        # ========================
        # BEAT 1: 0.00 - 3.58
        # Fade in the left diagram and faint field lines.
        # ========================
        self.play(FadeIn(stick, outlet, field_lines), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.58))

        # ========================
        # BEAT 2: 3.58 - 5.60
        # Label + highlight above outlet, then spectrum fades in.
        # ========================
        supply_label = Text("Electrical Power Supply", font_size=26, color=YELLOW, weight="BOLD")
        supply_label.next_to(outlet, UP, buff=0.25)
        supply_highlight = SurroundingRectangle(
            supply_label,
            color=YELLOW,
            buff=0.15,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.18,
        )

        self.play(Write(supply_label), FadeIn(supply_highlight), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.6))
        self.play(FadeOut(supply_highlight), FadeIn(spectrum_group), run_time=max(0.05, 0.82))

        # gap 5.60 - 6.24
        self.wait(max(0.05, 0.64))

        # ========================
        # BEAT 3: 6.24 - 11.18
        # Equipment / Lights / Cables labels, then field-line pulse.
        # ========================
        equipment_label = Text("Equipment", font_size=24, color=YELLOW, weight="BOLD")
        equipment_label.next_to(outlet, LEFT, buff=0.3)
        lights_label = Text("Lights", font_size=24, color=YELLOW, weight="BOLD")
        lights_label.next_to(outlet, DOWN, buff=0.28)
        cables_label = Text("Cables", font_size=24, color=YELLOW, weight="BOLD")
        cables_label.next_to(outlet, RIGHT, buff=0.25)

        for label in (equipment_label, lights_label, cables_label):
            self.play(Write(label), run_time=max(0.05, 0.4))
            self.play(Indicate(label, color=YELLOW, scale_factor=1.15), run_time=max(0.05, 0.5))
            self.wait(max(0.05, 0.2))

        # fields become pronounced, then brighter and fuller
        self.play(field_lines.animate.set_opacity(0.7).set_stroke(width=4), run_time=max(0.05, 0.8))
        self.play(field_lines.animate.set_opacity(1.0).set_stroke(width=5), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.04))

        # gap 11.18 - 12.00
        self.wait(max(0.05, 0.82))

        # ========================
        # BEAT 4: 12.00 - 17.12
        # Fields wrap electrode, spark flash, then 50 Hz peak pulses and label appears.
        # ========================
        electrode_center = np.array([-3.35, 0.35, 0])

        def build_wrap_arc(center, radius=0.4, start_angle=-PI * 0.55, end_angle=PI * 0.55):
            arc_pts = []
            for theta in np.linspace(start_angle, end_angle, 80):
                arc_pts.append(center + radius * np.array([np.cos(theta), np.sin(theta), 0]))
            arc = VMobject(color=YELLOW, stroke_width=4, fill_opacity=0)
            arc.set_points_as_corners(arc_pts)
            return arc

        wrap_arc = build_wrap_arc(electrode_center)

        def build_sparks(center, count=8, radius=0.3):
            spark_lines = VGroup()
            for k in range(count):
                angle = k * TAU / count + PI / 8
                end = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
                spark_lines.add(Line(center, end, color=YELLOW, stroke_width=3))
            return spark_lines

        spark_group = build_sparks(electrode_center)
        spark_group.set_opacity(0)

        self.play(FadeIn(wrap_arc), run_time=max(0.05, 0.5))
        self.play(spark_group.animate.set_opacity(1).scale(1.3), run_time=max(0.05, 0.4))
        self.play(spark_group.animate.set_opacity(0).scale(0.4), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 1.3))

        interference_label = Text("Power Line Interference", font_size=28, color=RED, weight="BOLD")
        interference_label.next_to(peak_line.get_top(), UP, buff=0.2)
        pointer_arrow = Arrow(
            interference_label.get_bottom() + DOWN * 0.1,
            peak_line.get_top(),
            color=GOLD,
            stroke_width=4,
            buff=0.15,
        )

        self.play(FadeIn(interference_label, pointer_arrow), run_time=max(0.05, 0.7))
        for _ in range(2):
            self.play(Indicate(peak_line, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.41))

        self.play(FadeOut(interference_label, pointer_arrow), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.7))

        # ========================
        # BEAT 5: 17.12 - 23.02
        # Grid Frequency label, 50 Hz peak brighten + big annotation,
        # then a second 60 Hz peak appears and fades.
        # ========================
        grid_freq_label = Text("Grid Frequency", font_size=30, color=YELLOW, weight="BOLD")
        grid_freq_label.next_to(spectrum_group, UP, buff=0.3)
        grid_freq_label.shift(RIGHT * 1.0)

        self.play(Write(grid_freq_label), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.82))

        big_50_label = Text("50 Hz", font_size=40, color=RED, weight="BOLD")
        big_50_label.next_to(peak_line.get_top(), UP, buff=0.3)

        self.play(
            peak_line.animate.set_stroke(width=16).set_color(RED),
            big_50_label.animate.scale(1.4),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.5))

        bg_y_at_60 = 0.15 + 0.05 * np.sin(0.18 * 60) + 0.04 * np.cos(0.11 * 60)
        peak_60_line = Line(
            axes.c2p(60, bg_y_at_60),
            axes.c2p(60, 0.65),
            color=RED,
            stroke_width=7,
        )
        peak_label_60 = Text("60 Hz", font_size=24, color=RED, weight="BOLD")
        peak_label_60.move_to(axes.c2p(60, -0.35))
        peak_60_group = VGroup(peak_60_line, peak_label_60)

        self.play(FadeIn(peak_60_group), run_time=max(0.05, 0.5))
        self.play(FadeOut(peak_60_group), run_time=max(0.05, 0.46))
        self.wait(max(0.05, 0.92))

        # ========================
        # BEAT 6: 23.02 - 27.34
        # Zoom into the 50 Hz peak.
        # ========================
        peak_center = peak_line.get_center()
        self.play(
            self.camera.frame.animate.scale(0.12).move_to(peak_center),
            run_time=max(0.05, 3.62),
        )
        self.wait(max(0.05, 0.7))

        # ========================
        # BEAT 7: 27.34 - 32.46
        # Notch band descends, peak collapses.
        # ========================
        def build_notch_band(center):
            cx, cy = center[0], center[1]
            half_w = 0.16
            band_half_h = 0.22
            top_y = cy + band_half_h
            bottom_y = cy - band_half_h
            points = [
                np.array([cx - half_w, top_y, 0]),
                np.array([cx + half_w, top_y, 0]),
                np.array([cx + half_w * 0.45, bottom_y, 0]),
                np.array([cx, bottom_y + 0.08, 0]),
                np.array([cx - half_w * 0.45, bottom_y, 0]),
            ]
            band = Polygon(
                *points,
                color=PURPLE,
                fill_color=PURPLE,
                fill_opacity=0.35,
                stroke_width=3,
                stroke_opacity=0.6,
            )
            return band

        notch_band = build_notch_band(peak_center)
        notch_start = peak_center + UP * 1.0
        notch_band.move_to(notch_start)

        self.add(notch_band)
        self.play(notch_band.animate.move_to(peak_center), run_time=max(0.05, 1.2))

        self.wait(max(0.05, 1.16))

        collapsed_peak = Line(peak_line.get_start(), peak_line.get_start(), color=RED, stroke_width=0)
        self.play(Transform(peak_line, collapsed_peak), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.56))

        # ========================
        # BEAT 8: 32.46 - 37.72
        # Broad ghost band contracts, notch band glows, narrow label fades in.
        # ========================
        ghost_band = Rectangle(
            width=notch_band.get_width() * 2.8,
            height=notch_band.get_height() * 1.2,
            fill_color=GREY,
            fill_opacity=0.35,
            stroke_color=GREY,
            stroke_width=0,
        )
        ghost_band.move_to(notch_band.get_center())

        broad_label = Text("Broad", font_size=24, color=GREY_B, weight="BOLD")
        broad_label.next_to(ghost_band, RIGHT, buff=0.2)

        self.play(FadeIn(ghost_band, broad_label), run_time=max(0.05, 0.4))
        self.play(Indicate(broad_label, color=GREY, scale_factor=1.3), run_time=max(0.05, 0.4))
        self.play(FadeOut(broad_label), run_time=max(0.05, 0.2))
        self.play(
            ghost_band.animate.scale(0.3).move_to(notch_band.get_center()).set_opacity(0),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.66))

        narrow_label = Text("Narrow notch band", font_size=18, color=YELLOW, weight="BOLD")
        narrow_label.next_to(notch_band, DOWN, buff=0.1)

        self.play(
            notch_band.animate.set_stroke(color=YELLOW, width=5, opacity=1),
            FadeIn(narrow_label),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 1.9))

        # ========================
        # BEAT 9: 38.24 - 39.00
        # Hold, then fade to black.
        # ========================
        self.wait(max(0.05, 0.52))  # 37.72 -> 38.24
        self.wait(max(0.05, 0.56))  # final hold until 38.80
        self.play(FadeOut(*self.mobjects), run_time=max(0.05, 0.2))