ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --------------------------------------------------------------
        # Title
        # --------------------------------------------------------------
        title = Text("Sampling", font_size=56, color=WHITE, weight="BOLD")
        title.to_edge(UP, buff=0.3)

        # Beat 1: brief hold, then clean title (0.00 - 1.66)
        self.wait(max(0.05, 0.66))
        self.play(Write(title), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.66))  # gap to beat 2

        # --------------------------------------------------------------
        # Main lower waveform panel
        # --------------------------------------------------------------
        main_panel = Rectangle(
            width=7.8,
            height=2.5,
            color=WHITE,
            stroke_width=2.0,
        ).move_to(np.array([-0.8, -1.55, 0.0]))

        axis_y = main_panel.get_bottom()[1] + 0.45  # -2.35
        amplitude_x = main_panel.get_left()[0] + 0.35
        time_axis_start = np.array([amplitude_x, axis_y, 0.0])
        time_axis_end = np.array([main_panel.get_right()[0] - 0.35, axis_y, 0.0])
        amplitude_axis_start = np.array([amplitude_x, axis_y, 0.0])
        amplitude_axis_end = np.array([amplitude_x, main_panel.get_top()[1] - 0.25, 0.0])

        time_axis = Line(time_axis_start, time_axis_end, color=GREY_B, stroke_width=3)
        amplitude_axis = Line(amplitude_axis_start, amplitude_axis_end, color=GREY_B, stroke_width=3)

        analogue_label = Text("analogue signal", font_size=20, color=WHITE)
        analogue_label.scale_to_fit_width(2.0)
        analogue_label.next_to(main_panel, LEFT, buff=0.3)

        # Waveform geometry
        curve_x_start = amplitude_x + 0.4
        curve_x_end = main_panel.get_right()[0] - 0.55
        curve_center_y = axis_y + 0.55
        cycles = 2.3

        amp_tracker = ValueTracker(0.65)
        phase_state = [0.0]
        wiggle_speed_tracker = ValueTracker(0.8)

        def wave_y_at_x(x):
            frac = (x - curve_x_start) / (curve_x_end - curve_x_start)
            return curve_center_y + amp_tracker.get_value() * np.sin(
                TAU * cycles * frac + phase_state[0]
            )

        def wave_points():
            xs = np.linspace(curve_x_start, curve_x_end, 200)
            return [np.array([x, wave_y_at_x(x), 0.0]) for x in xs]

        waveform = VMobject()
        waveform.set_stroke(BLUE, width=4)
        waveform.set_points_as_corners(wave_points())
        waveform.set_z_index(1)

        wave_glow = VMobject()
        wave_glow.set_stroke(GOLD, width=10, opacity=0.25)
        wave_glow.set_points_as_corners(wave_points())
        wave_glow.set_z_index(0)

        # Beat 2: coordinate plane + waveform (2.32 - 4.78)
        self.play(
            FadeIn(main_panel, time_axis, amplitude_axis, analogue_label),
            run_time=max(0.05, 0.6),
        )
        self.add(wave_glow)
        self.play(Write(waveform), run_time=max(0.05, 1.86))
        self.wait(max(0.05, 0.72))  # gap to beat 3

        # --------------------------------------------------------------
        # Equal-interval dashed lines
        # --------------------------------------------------------------
        n_samples = 8
        sample_xs = np.linspace(curve_x_start + 0.4, curve_x_end - 0.4, n_samples)

        dash_lines = VGroup()
        for x in sample_xs:
            line = DashedLine(
                start=np.array([x, axis_y, 0.0]),
                end=np.array([x, main_panel.get_top()[1] - 0.2, 0.0]),
                color=GREY,
                dash_length=0.1,
                stroke_width=2.0,
            )
            dash_lines.add(line)

        regular_label = Text("regular intervals", font_size=22, color=WHITE)
        regular_label.next_to(time_axis, DOWN, buff=0.12)

        # Beat 3: draw dashed lines left-to-right (4.78 - 7.74)
        per_line = 1.5 / len(dash_lines)
        for line in dash_lines:
            self.play(Create(line), run_time=max(0.05, per_line))

        self.play(FadeIn(regular_label), run_time=max(0.05, 0.96))
        self.wait(max(0.05, 0.5))
        self.wait(max(0.05, 0.72))  # gap to beat 4

        # --------------------------------------------------------------
        # Initial sample dots
        # --------------------------------------------------------------
        initial_sample_dots = VGroup()
        for x in sample_xs:
            dot = Dot(
                point=np.array([x, wave_y_at_x(x), 0.0]),
                radius=0.06,
                color=ORANGE,
                fill_opacity=1.0,
            )
            initial_sample_dots.add(dot)

        sample_label = Text("sample", font_size=22, color=WHITE)
        sample_label.next_to(initial_sample_dots[3], UP + RIGHT, buff=0.12)

        # Beat 4: dots at intersections + sample label (8.46 - 10.08)
        per_dot = 0.9 / len(initial_sample_dots)
        for dot in initial_sample_dots:
            self.play(GrowFromCenter(dot), run_time=max(0.05, per_dot))

        self.play(FadeIn(sample_label), run_time=max(0.05, 0.35))
        self.play(
            Indicate(initial_sample_dots, color=YELLOW, scale_factor=1.3),
            run_time=max(0.05, 0.37),
        )
        self.wait(max(0.05, 0.62))  # gap to beat 5

        # --------------------------------------------------------------
        # Upper bouncing-ball panel
        # --------------------------------------------------------------
        upper_panel = Rectangle(
            width=7.8,
            height=2.3,
            color=WHITE,
            stroke_width=2.0,
        ).move_to(np.array([0.0, 1.15, 0.0]))

        ground_y = upper_panel.get_bottom()[1] + 0.35
        ground_line = Line(
            start=np.array([upper_panel.get_left()[0] + 0.35, ground_y, 0.0]),
            end=np.array([upper_panel.get_right()[0] - 0.35, ground_y, 0.0]),
            color=GREY,
            stroke_width=3,
        )

        ball = Circle(
            radius=0.16,
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=1.0,
            stroke_width=0,
        )
        ball.move_to(np.array([upper_panel.get_left()[0] + 0.8, ground_y + 0.16, 0.0]))

        bounce_state = [0.0]
        bounce_speed_tracker = ValueTracker(1.0)
        ball_left_x = upper_panel.get_left()[0] + 0.8
        ball_right_x = upper_panel.get_right()[0] - 0.8
        bounce_width = ball_right_x - ball_left_x
        bounce_height = 0.75

        def update_ball(mob, dt):
            bounce_state[0] += dt * bounce_speed_tracker.get_value()
            t = bounce_state[0]
            phase = t % 1.0
            x = ball_left_x + phase * bounce_width
            y = ground_y + 4.0 * bounce_height * phase * (1.0 - phase)
            mob.move_to(np.array([x, y, 0.0]))

        ball.add_updater(update_ball)

        # Beat 5: bouncing ball loops continuously (10.70 - 13.68)
        self.play(FadeIn(upper_panel, ground_line), run_time=max(0.05, 0.4))
        self.play(GrowFromCenter(ball), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.08))
        self.wait(max(0.05, 1.12))  # gap to beat 6

        # --------------------------------------------------------------
        # Photograph-style snapshots
        # --------------------------------------------------------------
        flash_rect = Rectangle(
            width=upper_panel.width,
            height=upper_panel.height,
            fill_color=WHITE,
            fill_opacity=0.0,
            stroke_width=0,
        ).move_to(upper_panel.get_center())

        snapshot_data = [0.15, 0.85, 0.45, 0.9, 0.2, 0.75, 0.5]
        snapshot_frames = VGroup()
        for frac in snapshot_data:
            frame = Rectangle(
                width=0.45,
                height=0.45,
                color=WHITE,
                stroke_width=1.5,
                fill_color=BLACK,
                fill_opacity=0.9,
            )
            mini_ball = Dot(
                point=frame.get_center() + np.array([0.0, -0.15 + frac * 0.30, 0.0]),
                radius=0.05,
                color=TEAL,
                fill_opacity=1.0,
            )
            snap = VGroup(frame, mini_ball)
            snapshot_frames.add(snap)

        snapshot_frames.arrange(RIGHT, buff=0.12)
        snapshot_frames.move_to(np.array([upper_panel.get_center()[0], 0.25, 0.0]))

        self.add(flash_rect)

        # Beat 6: flash + first three stills (14.80 - 17.76)
        flash_wait = 0.6067
        for i in range(3):
            self.play(
                flash_rect.animate.set_fill(opacity=0.85),
                run_time=max(0.05, 0.08),
            )
            self.play(
                flash_rect.animate.set_fill(opacity=0.0),
                run_time=max(0.05, 0.12),
            )
            self.play(FadeIn(snapshot_frames[i]), run_time=max(0.05, 0.18))
            self.wait(max(0.05, flash_wait))

        # Beat 7: complete snapshot row + label (17.76 - 19.94)
        remaining_snapshots = snapshot_frames[3:]
        per_snap = 1.2 / len(remaining_snapshots)
        for snap in remaining_snapshots:
            self.play(FadeIn(snap), run_time=max(0.05, per_snap))

        series_label = Text(
            "a series of individual images",
            font_size=18,
            color=WHITE,
        )
        series_label.next_to(snapshot_frames, DOWN, buff=0.2)
        self.play(FadeIn(series_label), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.38))
        self.wait(max(0.05, 0.76))  # gap to beat 8

        # --------------------------------------------------------------
        # Dim upper panel + pulse dashed lines left to right
        # --------------------------------------------------------------
        upper_group = VGroup(
            upper_panel,
            ground_line,
            ball,
            snapshot_frames,
            series_label,
        )

        # Beat 8: focus lower panel again (20.70 - 23.24)
        self.play(upper_group.animate.set_opacity(0.35), run_time=max(0.05, 0.5))

        pulse_per_line = 2.04 / len(dash_lines)
        for line in dash_lines:
            self.play(
                line.animate.set_stroke(color=YELLOW, width=3.0),
                run_time=max(0.05, pulse_per_line * 0.45),
            )
            self.play(
                line.animate.set_stroke(color=GREY, width=2.0),
                run_time=max(0.05, pulse_per_line * 0.55),
            )

        # --------------------------------------------------------------
        # Animate waveform changing with soft glow
        # --------------------------------------------------------------
        def update_waveform(mob, dt):
            phase_state[0] += dt * wiggle_speed_tracker.get_value()
            mob.set_points_as_corners(wave_points())

        def update_wave_glow(mob, dt):
            mob.set_points_as_corners(wave_points())

        # Beat 9: changing waveform (23.24 - 27.14)
        self.play(FadeOut(initial_sample_dots), run_time=max(0.05, 0.35))
        waveform.add_updater(update_waveform)
        wave_glow.add_updater(update_wave_glow)
        self.play(
            wave_glow.animate.set_stroke(opacity=0.65, width=12),
            run_time=max(0.05, 0.45),
        )
        self.play(
            wiggle_speed_tracker.animate.set_value(2.0),
            amp_tracker.animate.set_value(1.0),
            run_time=max(0.05, 1.55),
        )
        self.play(amp_tracker.animate.set_value(0.65), run_time=max(0.05, 1.55))
        self.wait(max(0.05, 0.66))  # gap to beat 10

        # --------------------------------------------------------------
        # Fresh scan dots on the changing waveform
        # --------------------------------------------------------------
        fresh_dots = VGroup()
        for i, x in enumerate(sample_xs):
            dot = Dot(
                point=np.array([x, wave_y_at_x(x), 0.0]),
                radius=0.055,
                color=ORANGE,
                fill_opacity=1.0,
            )
            dot.add_updater(
                lambda mob, dt, idx=i: mob.move_to(
                    np.array([sample_xs[idx], wave_y_at_x(sample_xs[idx]), 0.0])
                )
            )
            fresh_dots.add(dot)

        # Beat 10: scan left-to-right (27.80 - 30.38)
        fresh_per_dot = 2.58 / len(fresh_dots)
        for dot in fresh_dots:
            self.play(GrowFromCenter(dot), run_time=max(0.05, fresh_per_dot))
        self.wait(max(0.05, 0.88))  # gap to beat 11

        # --------------------------------------------------------------
        # Highlight one measurement, then all dots
        # --------------------------------------------------------------
        rep_dot = fresh_dots[3]

        # Beat 11: hold dots and pulse (31.26 - 34.06)
        self.play(wiggle_speed_tracker.animate.set_value(0.0), run_time=max(0.05, 0.3))

        highlight_ring = Circle(
            radius=0.16,
            color=GOLD,
            stroke_width=3,
        ).move_to(rep_dot.get_center())
        self.play(GrowFromCenter(highlight_ring), run_time=max(0.05, 0.35))

        measure_label = Text(
            "measurement at that instant",
            font_size=18,
            color=WHITE,
        )
        measure_label.next_to(rep_dot, UP, buff=0.15)
        self.play(FadeIn(measure_label), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.4))
        self.play(FadeOut(measure_label, highlight_ring), run_time=max(0.05, 0.4))
        self.play(
            Indicate(fresh_dots, color=YELLOW, scale_factor=1.3),
            run_time=max(0.05, 0.85),
        )
        self.wait(max(0.05, 0.80))  # gap to beat 12

        # --------------------------------------------------------------
        # Counter-style display below time axis
        # --------------------------------------------------------------
        counter_box = Rectangle(
            width=1.8,
            height=0.55,
            color=GREY,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.9,
        ).move_to(np.array([main_panel.get_center()[0], -3.1, 0.0]))

        counter_text = Text("0", font_size=28, color=WHITE)
        counter_text.move_to(counter_box.get_center())
        counter_text_center = counter_text.get_center()
        counter_state = [0.0]
        counter_speed_tracker = ValueTracker(80.0)
        counter_highlight_state = [False]

        def update_counter_text(mob, dt):
            counter_state[0] += counter_speed_tracker.get_value() * dt
            color = GOLD if counter_highlight_state[0] else WHITE
            mob.become(
                Text(
                    str(int(counter_state[0])),
                    font_size=28,
                    color=color,
                ).move_to(counter_text_center)
            )

        # Beat 12: counter begins ticking (34.86 - 37.40)
        self.play(FadeIn(counter_box, counter_text), run_time=max(0.05, 0.5))
        counter_text.add_updater(update_counter_text)
        self.wait(max(0.05, 2.04))
        self.wait(max(0.05, 0.48))  # gap to beat 13

        # --------------------------------------------------------------
        # Mini digital-representation panel
        # --------------------------------------------------------------
        mini_panel = Rectangle(
            width=2.6,
            height=1.6,
            color=WHITE,
            stroke_width=2,
        ).move_to(np.array([4.8, -1.55, 0.0]))

        mini_left = mini_panel.get_left()[0] + 0.25
        mini_right = mini_panel.get_right()[0] - 0.25
        mini_bottom = mini_panel.get_bottom()[1] + 0.30
        mini_top = mini_panel.get_top()[1] - 0.30

        current_ys = [wave_y_at_x(x) for x in sample_xs]
        y_min = min(current_ys)
        y_max = max(current_ys)

        mini_dot_positions = []
        for x, y in zip(sample_xs, current_ys):
            mini_x = mini_left + (x - sample_xs[0]) / (sample_xs[-1] - sample_xs[0]) * (mini_right - mini_left)
            mini_y = mini_bottom + (y - y_min) / (y_max - y_min) * (mini_top - mini_bottom)
            mini_dot_positions.append(np.array([mini_x, mini_y, 0.0]))

        mini_dots = VGroup()
        for pos in mini_dot_positions:
            mini_dots.add(
                Dot(point=pos, radius=0.05, color=ORANGE, fill_opacity=1.0)
            )

        mini_line = VMobject()
        mini_line.set_stroke(WHITE, width=2)
        mini_line_xs = np.linspace(mini_dot_positions[0][0], mini_dot_positions[-1][0], 200)
        mini_line_points = []
        for x in mini_line_xs:
            interp_y = np.interp(
                x,
                [p[0] for p in mini_dot_positions],
                [p[1] for p in mini_dot_positions],
            )
            mini_line_points.append(np.array([x, interp_y, 0.0]))
        mini_line.set_points_as_corners(mini_line_points)

        digital_repr_label = Text(
            "digital representation",
            font_size=20,
            color=GOLD,
            weight="BOLD",
        )
        digital_repr_label.next_to(mini_panel, DOWN, buff=0.2)

        mini_group = VGroup(mini_panel, mini_dots, mini_line, digital_repr_label)

        # Beat 13: dots-only reconstruction mini panel (37.88 - 41.94)
        self.play(
            waveform.animate.set_opacity(0.15),
            dash_lines.animate.set_opacity(0.15),
            wave_glow.animate.set_opacity(0.1),
            run_time=max(0.05, 1.0),
        )
        self.play(FadeIn(mini_panel), run_time=max(0.05, 0.5))
        self.play(Write(mini_line), run_time=max(0.05, 1.0))
        self.play(FadeIn(mini_dots), run_time=max(0.05, 0.5))
        self.play(FadeIn(digital_repr_label), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.56))
        self.wait(max(0.05, 0.62))  # gap to beat 14

        # --------------------------------------------------------------
        # Restore main panel + EEG recording system label
        # --------------------------------------------------------------
        eeg_label = Text("EEG recording system", font_size=18, color=WHITE)
        eeg_label.move_to(np.array([main_panel.get_center()[0] - 2.0, main_panel.get_bottom()[1] - 0.3, 0.0]))

        # Beat 14: back to main waveform (42.56 - 45.84)
        self.play(
            waveform.animate.set_opacity(1.0),
            dash_lines.animate.set_opacity(1.0),
            wave_glow.animate.set_opacity(0.35),
            run_time=max(0.05, 1.0),
        )
        self.play(mini_group.animate.set_opacity(0.35), run_time=max(0.05, 0.3))
        self.play(FadeIn(eeg_label), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 1.28))

        # --------------------------------------------------------------
        # 1000 samples per second + counter acceleration
        # --------------------------------------------------------------
        samples_per_second_label = Text(
            "1000 samples per second",
            font_size=26,
            color=YELLOW,
            weight="BOLD",
        )
        samples_per_second_label.move_to(
            np.array([main_panel.get_center()[0], main_panel.get_top()[1] - 0.45, 0.0])
        )

        # Beat 15: sampling-frequency label (45.84 - 49.22)
        self.play(Write(samples_per_second_label), run_time=max(0.05, 0.6))
        self.play(counter_speed_tracker.animate.set_value(1000.0), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 1.18))
        self.wait(max(0.05, 0.44))  # gap to beat 16

        # --------------------------------------------------------------
        # Progress arc that pulses every 1000 counts
        # --------------------------------------------------------------
        progress_ring = Circle(
            radius=0.26,
            color=GREY,
            stroke_width=2,
        ).move_to(np.array([counter_box.get_right()[0] + 0.65, counter_box.get_center()[1], 0.0]))

        progress_arc_center = progress_ring.get_center()

        progress_arc = Arc(
            radius=0.22,
            start_angle=PI / 2,
            angle=0.05,
            color=GOLD,
            stroke_width=4,
        ).move_to(progress_arc_center)

        def update_progress_arc(mob):
            frac = (counter_state[0] % 1000.0) / 1000.0
            angle = max(0.05, TAU * frac)
            new_arc = Arc(
                radius=0.22,
                start_angle=PI / 2,
                angle=angle,
                color=GOLD,
                stroke_width=4,
            ).move_to(progress_arc_center)
            mob.become(new_arc)

        progress_arc.add_updater(update_progress_arc)

        count_1000_label = Text("1000", font_size=22, color=WHITE)
        count_1000_label.next_to(progress_ring, LEFT, buff=0.2)

        # Beat 16: count marker cycles (49.66 - 55.10)
        self.play(
            FadeIn(progress_ring, progress_arc, count_1000_label),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 4.64))
        self.wait(max(0.05, 1.76))  # gap to beat 17

        # --------------------------------------------------------------
        # Final comparison + highlighted 1000
        # --------------------------------------------------------------
        recon_arrow = Arrow(
            start=main_panel.get_right(),
            end=mini_panel.get_left(),
            color=WHITE,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.25,
        )

        connect_label = Text(
            "EEG waveform in digital form",
            font_size=22,
            color=WHITE,
            weight="BOLD",
        )
        connect_label.next_to(recon_arrow, DOWN, buff=0.2)

        final_1000_label = Text("1000", font_size=24, color=YELLOW, weight="BOLD")
        final_1000_label.next_to(counter_box, RIGHT, buff=0.25)
        final_1000_ring = SurroundingRectangle(final_1000_label, color=GOLD, buff=0.1)
        final_1000_group = VGroup(final_1000_label, final_1000_ring)

        # Beat 17: full comparison and final highlighted 1000 (56.86 - 61.04)
        self.play(counter_speed_tracker.animate.set_value(0.0), run_time=max(0.05, 0.35))
        counter_state[0] = 1000.0
        counter_highlight_state[0] = True

        self.play(mini_group.animate.set_opacity(1.0), run_time=max(0.05, 0.55))
        self.play(Create(recon_arrow), run_time=max(0.05, 0.7))
        self.play(FadeIn(connect_label), run_time=max(0.05, 0.6))
        self.play(FadeIn(final_1000_group), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.48))

        # Beat 18: final hold (61.04 - 61.73)
        self.wait(max(0.05, 0.69))