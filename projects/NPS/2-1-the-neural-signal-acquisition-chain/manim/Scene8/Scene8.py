ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Camera setup: show the full acquisition chain comfortably.
        # ------------------------------------------------------------
        self.camera.frame.scale(1.15)
        self.camera.frame.move_to(np.array([0.5, -0.4, 0.0]))
        self.camera.frame.set_stroke(width=0)

        # ------------------------------------------------------------
        # Constants matching the previous scene's final state.
        # ------------------------------------------------------------
        AXIS_Y = -1.4
        VALUE_SCALE = 2.0
        FINAL_SAMPLE_XS = np.array([-5.5, -4.6, -3.7, -2.8, -1.9, -1.0])
        SAMPLE_VALUES = np.array([0.2, 0.5, 0.8, 0.6, 0.9, 0.4])
        DIG_XS = np.array([2.0, 2.6, 3.2, 3.8, 4.4, 5.0])

        # ------------------------------------------------------------
        # Catmull-Rom interpolation for the smooth analog waveform.
        # ------------------------------------------------------------
        def catmull_rom(points, n_per_seg=90):
            pts = []
            p = [np.array(pt, dtype=float) for pt in points]
            for i in range(len(p) - 1):
                p0 = p[max(i - 1, 0)]
                p1 = p[i]
                p2 = p[i + 1]
                p3 = p[min(i + 2, len(p) - 1)]
                for j in range(n_per_seg):
                    t = j / n_per_seg
                    t2 = t * t
                    t3 = t2 * t
                    pt = 0.5 * (
                        (2.0 * p1)
                        + (-p0 + p2) * t
                        + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2
                        + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3
                    )
                    pts.append(pt)
            pts.append(p[-1])
            return pts

        # ------------------------------------------------------------
        # Analog waveform and sample dots from the previous scene.
        # ------------------------------------------------------------
        initial_sample_points = [
            np.array([x, AXIS_Y + VALUE_SCALE * v, 0.0])
            for x, v in zip(FINAL_SAMPLE_XS, SAMPLE_VALUES)
        ]
        analog_points = catmull_rom(initial_sample_points, n_per_seg=90)
        analog_wave = VMobject().set_points_as_corners(analog_points)
        analog_wave.set_stroke(color=ORANGE, width=6)
        analog_wave.set_fill(opacity=0)

        analog_axis = Line(
            start=np.array([FINAL_SAMPLE_XS[0] - 0.6, AXIS_Y, 0.0]),
            end=np.array([FINAL_SAMPLE_XS[-1] + 0.6, AXIS_Y, 0.0]),
            color=GREY_B,
            stroke_width=3,
        )

        analog_label = Text("analog signal", font_size=28, color=YELLOW)
        analog_label.next_to(analog_wave, UP, buff=0.25)

        sample_dots = VGroup()
        sample_labels = VGroup()
        for x, v in zip(FINAL_SAMPLE_XS, SAMPLE_VALUES):
            y_wave = AXIS_Y + VALUE_SCALE * v
            dot = Dot(point=np.array([x, y_wave, 0.0]), radius=0.08, color=YELLOW)
            sample_dots.add(dot)
            label = Text(str(round(v, 1)), font_size=20, color=YELLOW)
            label.next_to(dot, UP, buff=0.16)
            sample_labels.add(label)

        # ------------------------------------------------------------
        # ADC block.
        # ------------------------------------------------------------
        adc_box = Rectangle(
            width=2.4,
            height=1.6,
            stroke_color=TEAL,
            stroke_width=4,
            fill_color=TEAL,
            fill_opacity=0.90,
        )
        adc_box.move_to(np.array([0.6, 0.4, 0.0]))
        adc_abbr = Text("ADC", font_size=40, color=YELLOW)
        adc_full = Text("Analog-to-Digital Converter", font_size=14, color=WHITE)
        adc_full.scale_to_fit_width(2.05)
        adc_text = VGroup(adc_abbr, adc_full).arrange(DOWN, buff=0.15)
        adc_text.move_to(adc_box.get_center())

        # ------------------------------------------------------------
        # Digital staircase representation.
        # ------------------------------------------------------------
        stair_ys = AXIS_Y + VALUE_SCALE * SAMPLE_VALUES

        stair_axis = Line(
            start=np.array([DIG_XS[0], AXIS_Y, 0.0]),
            end=np.array([DIG_XS[-1], AXIS_Y, 0.0]),
            color=GREY_B,
            stroke_width=3,
        )

        stair_pts = [np.array([DIG_XS[0], stair_ys[0], 0.0])]
        for i in range(len(DIG_XS) - 1):
            stair_pts.append(np.array([DIG_XS[i + 1], stair_ys[i], 0.0]))
            stair_pts.append(np.array([DIG_XS[i + 1], stair_ys[i + 1], 0.0]))

        stair_path = VMobject().set_points_as_corners(stair_pts)
        stair_path.set_stroke(color=GREEN, width=6)
        stair_path.set_fill(opacity=0)

        digital_label = Text("digital representation", font_size=24, color=GREEN)
        digital_label.next_to(stair_axis, DOWN, buff=0.25)

        # Everything that was already on screen when this scene starts.
        initial_chain = VGroup(
            analog_wave,
            analog_axis,
            analog_label,
            sample_dots,
            sample_labels,
            adc_box,
            adc_text,
            stair_axis,
            stair_path,
            digital_label,
        )
        self.add(initial_chain)

        # ------------------------------------------------------------
        # Computer box at the far right.
        # ------------------------------------------------------------
        computer_box = Rectangle(
            width=2.0,
            height=2.2,
            stroke_color=BLUE,
            stroke_width=4,
            fill_color=BLUE,
            fill_opacity=0.20,
        )
        computer_box.move_to(np.array([6.1, 1.1, 0.0]))

        computer_label = Text("Computer", font_size=30, color=WHITE)
        computer_label.next_to(computer_box, UP, buff=0.12)

        # Monitor inside the Computer box, currently blank/dim.
        monitor_rect = Rectangle(
            width=1.45,
            height=0.95,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.6,
        )
        monitor_rect.move_to(computer_box.get_center() + UP * 0.12)

        monitor_screen = Rectangle(
            width=1.25,
            height=0.75,
            stroke_color=WHITE,
            stroke_width=1.5,
            fill_color=BLACK,
            fill_opacity=0.8,
        )
        monitor_screen.move_to(monitor_rect.get_center())

        # Arrow from the digital staircase output into the Computer box.
        digital_to_computer_arrow = Arrow(
            start=np.array([DIG_XS[-1], stair_ys[-1], 0.0]),
            end=computer_box.get_left() + DOWN * 1.1,
            color=TEAL,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
            buff=0.05,
        )

        # ------------------------------------------------------------
        # Clean staircase waveform inside the monitor screen.
        # ------------------------------------------------------------
        screen_l = monitor_screen.get_left()[0] + 0.08
        screen_r = monitor_screen.get_right()[0] - 0.08
        screen_b = monitor_screen.get_bottom()[1] + 0.08
        screen_t = monitor_screen.get_top()[1] - 0.08
        screen_xs = np.linspace(screen_l, screen_r, len(SAMPLE_VALUES))
        screen_ys = screen_b + (SAMPLE_VALUES - SAMPLE_VALUES.min()) / (
            SAMPLE_VALUES.max() - SAMPLE_VALUES.min()
        ) * (screen_t - screen_b)

        screen_stair_pts = [np.array([screen_xs[0], screen_ys[0], 0.0])]
        for i in range(len(screen_xs) - 1):
            screen_stair_pts.append(np.array([screen_xs[i + 1], screen_ys[i], 0.0]))
            screen_stair_pts.append(np.array([screen_xs[i + 1], screen_ys[i + 1], 0.0]))

        screen_wave = VMobject().set_points_as_corners(screen_stair_pts)
        screen_wave.set_stroke(color=GREEN, width=3)
        screen_wave.set_fill(opacity=0)

        # ------------------------------------------------------------
        # Icons around the monitor / below the Computer box.
        # ------------------------------------------------------------
        def make_display_icon():
            scr = Rectangle(
                width=0.5,
                height=0.36,
                stroke_color=BLUE,
                stroke_width=2,
                fill_color=BLUE,
                fill_opacity=0.9,
            )
            stand = Line(
                scr.get_bottom(),
                scr.get_bottom() + DOWN * 0.12,
                color=BLUE,
                stroke_width=2,
            )
            base = Line(
                stand.get_end() + LEFT * 0.14,
                stand.get_end() + RIGHT * 0.14,
                color=BLUE,
                stroke_width=2,
            )
            return VGroup(scr, stand, base).scale_to_fit_height(0.4)

        def make_icon_group(label_text, icon, color=WHITE):
            lab = Text(label_text, font_size=15, color=color)
            return VGroup(icon, lab).arrange(DOWN, buff=0.07)

        display_icon_group = make_icon_group("Display", make_display_icon())

        store_icon = SVGMobject(
            ASSET_PATHS["table"],
            height=0.35,
            fill_color=TEAL,
            fill_opacity=1,
            stroke_width=0,
        )
        store_icon_group = make_icon_group("Store", store_icon)

        process_icon = SVGMobject(
            ASSET_PATHS["cpu"],
            height=0.35,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_width=0,
        )
        process_icon_group = make_icon_group("Process", process_icon)

        analyze_icon = SVGMobject(
            ASSET_PATHS["graph_trend"],
            height=0.35,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        )
        analyze_icon_group = make_icon_group("Analyze", analyze_icon)

        icon_groups = [
            display_icon_group,
            store_icon_group,
            process_icon_group,
            analyze_icon_group,
        ]
        icon_row = VGroup(*icon_groups).arrange(RIGHT, buff=0.22)
        icon_row.scale_to_fit_width(3.4)
        icon_row.next_to(computer_box, DOWN, buff=0.22)

        # Thin lines from each icon up to the Computer box.
        icon_connectors = VGroup()
        for ig in icon_groups:
            top_point = ig.get_top()
            bottom_target = np.array(
                [top_point[0], computer_box.get_bottom()[1], 0.0]
            )
            line = Line(
                start=top_point,
                end=bottom_target,
                color=GREY_B,
                stroke_width=2,
            )
            icon_connectors.add(line)

        recorded_data_caption = Text("recorded data", font_size=24, color=YELLOW)
        recorded_data_caption.next_to(icon_row, DOWN, buff=0.25)

        # ------------------------------------------------------------
        # Downstream boxes and their connections back to the chain.
        # ------------------------------------------------------------
        spine_x = 5.3
        spine = Line(
            start=np.array([spine_x, -1.8, 0.0]),
            end=np.array([spine_x, -4.0, 0.0]),
            color=GREY_B,
            stroke_width=2,
        )

        downstream_defs = [
            ("Filtering", PURPLE),
            ("Feature Extraction", PINK),
            ("Spectral Analysis", ORANGE),
            ("Classification", GREEN),
        ]
        ds_pos_y = [-2.0, -2.65, -3.3, -3.95]
        ds_boxes = []
        ds_connections = VGroup()

        for (label, color), y in zip(downstream_defs, ds_pos_y):
            box = Rectangle(
                width=2.1,
                height=0.56,
                stroke_color=color,
                stroke_width=3,
                fill_color=color,
                fill_opacity=0.15,
            )
            box.move_to(np.array([6.9, y, 0.0]))
            lab = Text(label, font_size=15, color=WHITE).scale_to_fit_width(1.85)
            lab.move_to(box.get_center())
            box_group = VGroup(box, lab)
            ds_boxes.append(box_group)

            conn = Arrow(
                start=box.get_left(),
                end=np.array([spine_x, y, 0.0]),
                color=GREY_B,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
                buff=0.05,
            )
            ds_connections.add(conn)

        downstream_boxes_group = VGroup(*ds_boxes)

        # ------------------------------------------------------------
        # Beat 11 highlight / quality label.
        # ------------------------------------------------------------
        acq_highlight = SurroundingRectangle(
            VGroup(analog_wave, adc_box, computer_box),
            color=YELLOW,
            buff=0.15,
            stroke_width=3,
            corner_radius=0.1,
        )
        acq_quality_label = Text("acquired signal quality", font_size=24, color=GREEN)
        acq_quality_label.next_to(acq_highlight, DOWN, buff=0.28)

        work_caption = Text(
            "The computer can only work with what it's been given.",
            font_size=22,
            color=YELLOW,
        )
        work_caption.scale_to_fit_width(5.5)
        work_caption.next_to(computer_label, UP, buff=0.20)

        trace_dot = Dot(
            point=computer_box.get_center(), radius=0.06, color=YELLOW
        )

        # ============================================================
        # Beat 1: 0.00 - 3.66
        # Computer box fades in, connected from the staircase output.
        # ============================================================
        self.play(
            FadeIn(computer_box),
            FadeIn(monitor_rect),
            FadeIn(monitor_screen),
            Write(computer_label),
            Create(digital_to_computer_arrow),
            run_time=max(0.05, 1.40),
        )
        self.play(
            Indicate(computer_box, scale_factor=1.03, color=TEAL),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 1.56))

        # Gap to 4.42
        self.wait(max(0.05, 0.76))

        # ============================================================
        # Beat 2: 4.42 - 6.28
        # Monitor displays a crisp digital waveform; Display icon pulses.
        # ============================================================
        self.play(
            Create(screen_wave),
            GrowFromCenter(display_icon_group),
            run_time=max(0.05, 1.10),
        )
        self.play(
            Indicate(display_icon_group, scale_factor=1.12, color=YELLOW),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.26))

        # Gap to 6.40
        self.wait(max(0.05, 0.12))

        # ============================================================
        # Beat 3: 6.40 - 7.00
        # Store icon appears and pulses.
        # ============================================================
        self.play(
            GrowFromCenter(store_icon_group),
            run_time=max(0.05, 0.45),
        )
        self.play(
            Indicate(store_icon_group, scale_factor=1.10, color=YELLOW),
            run_time=max(0.05, 0.15),
        )

        # ============================================================
        # Beat 4: 7.00 - 7.84
        # Process icon appears and pulses.
        # ============================================================
        self.play(
            GrowFromCenter(process_icon_group),
            run_time=max(0.05, 0.45),
        )
        self.play(
            Indicate(process_icon_group, scale_factor=1.10, color=YELLOW),
            run_time=max(0.05, 0.35),
        )
        self.wait(max(0.05, 0.04))

        # ============================================================
        # Beat 5: 7.84 - 9.30
        # Analyze icon, connector lines, and recorded-data caption.
        # ============================================================
        self.play(
            GrowFromCenter(analyze_icon_group),
            run_time=max(0.05, 0.40),
        )
        self.play(
            Indicate(analyze_icon_group, scale_factor=1.10, color=YELLOW),
            run_time=max(0.05, 0.30),
        )
        self.play(
            LaggedStart(
                *[Create(line) for line in icon_connectors],
                lag_ratio=0.10,
            ),
            Write(recorded_data_caption),
            run_time=max(0.05, 0.76),
        )

        # Gap to 10.16
        self.wait(max(0.05, 0.86))

        # ============================================================
        # Beat 6: 10.16 - 11.22
        # "Computer" label pulses to draw the eye.
        # ============================================================
        self.play(
            computer_label.animate.set_color(YELLOW),
            computer_box.animate.set_stroke(width=6),
            run_time=max(0.05, 0.40),
        )
        self.play(
            computer_label.animate.set_color(WHITE),
            computer_box.animate.set_stroke(width=4),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.26))

        # Gap to 11.84
        self.wait(max(0.05, 0.62))

        # ============================================================
        # Beat 7: 11.84 - 13.50
        # First downstream box: Filtering.
        # ============================================================
        self.play(
            Create(spine),
            FadeIn(ds_boxes[0]),
            Create(ds_connections[0]),
            run_time=max(0.05, 0.80),
        )
        self.play(
            Indicate(ds_boxes[0], scale_factor=1.04, color=YELLOW),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 0.46))

        # Gap to 14.68
        self.wait(max(0.05, 1.18))

        # ============================================================
        # Beat 8: 14.68 - 15.32
        # Second downstream box: Feature Extraction.
        # ============================================================
        self.play(
            FadeIn(ds_boxes[1]),
            Create(ds_connections[1]),
            run_time=max(0.05, 0.64),
        )

        # Gap to 15.86
        self.wait(max(0.05, 0.54))

        # ============================================================
        # Beat 9: 15.86 - 16.48
        # Third downstream box: Spectral Analysis.
        # ============================================================
        self.play(
            FadeIn(ds_boxes[2]),
            Create(ds_connections[2]),
            run_time=max(0.05, 0.62),
        )

        # Gap to 17.60
        self.wait(max(0.05, 1.12))

        # ============================================================
        # Beat 10: 17.60 - 18.28
        # Fourth downstream box: Classification.
        # ============================================================
        self.play(
            FadeIn(ds_boxes[3]),
            Create(ds_connections[3]),
            run_time=max(0.05, 0.68),
        )

        # Gap to 18.36
        self.wait(max(0.05, 0.08))

        # ============================================================
        # Beat 11: 18.36 - 20.68
        # Expand view slightly; connections pulse; acquisition bracket.
        # ============================================================
        self.play(
            self.camera.frame.animate.scale(1.2),
            run_time=max(0.05, 0.70),
        )
        self.play(
            icon_connectors.animate.set_stroke(color=YELLOW, width=4),
            ds_connections.animate.set_stroke(color=YELLOW, width=4),
            spine.animate.set_stroke(color=YELLOW, width=4),
            run_time=max(0.05, 0.35),
        )
        self.play(
            icon_connectors.animate.set_stroke(color=WHITE, width=3),
            ds_connections.animate.set_stroke(color=WHITE, width=3),
            spine.animate.set_stroke(color=GREY_B, width=2),
            run_time=max(0.05, 0.35),
        )
        self.play(
            Write(acq_highlight),
            Write(acq_quality_label),
            run_time=max(0.05, 0.92),
        )

        # Gap to 22.12
        self.wait(max(0.05, 1.44))

        # ============================================================
        # Beat 12: 22.12 - 24.78
        # Dim downstream, brighten Computer, caption, glow trace.
        # ============================================================
        self.play(
            downstream_boxes_group.animate.set_opacity(0.3),
            ds_connections.animate.set_opacity(0.3),
            spine.animate.set_opacity(0.3),
            run_time=max(0.05, 0.40),
        )
        self.play(
            computer_box.animate.set_stroke(width=7, color=TEAL),
            monitor_rect.animate.set_stroke(width=4),
            monitor_screen.animate.set_fill(opacity=0.95),
            run_time=max(0.05, 0.40),
        )
        self.play(
            Write(work_caption),
            run_time=max(0.05, 0.50),
        )

        # Subtle glow traces from Computer back toward ADC and analog signal.
        self.add(trace_dot)
        self.play(
            trace_dot.animate.move_to(adc_box.get_center()),
            run_time=max(0.05, 0.42),
        )
        self.play(
            trace_dot.animate.move_to(analog_wave.get_center()),
            run_time=max(0.05, 0.42),
        )
        self.play(
            FadeOut(trace_dot),
            run_time=max(0.05, 0.36),
        )
        self.wait(max(0.05, 0.16))

        # ============================================================
        # Beat 13: 24.78 - 25.77
        # Final hold on the complete frame.
        # ============================================================
        self.wait(max(0.05, 0.99))