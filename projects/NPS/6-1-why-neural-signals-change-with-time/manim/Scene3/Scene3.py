ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Heading
        heading = Text("Nonstationary Signal", font_size=52, weight="BOLD", color=WHITE)
        heading.to_edge(UP, buff=0.6)

        # Definition box at bottom
        def_text = Text(
            "Nonstationary: statistical or spectral characteristics change over time",
            font_size=30,
            color=WHITE,
            t2c={"statistical": YELLOW, "spectral": YELLOW, "change": YELLOW},
        )
        if def_text.width > 10.5:
            def_text.scale_to_fit_width(10.5)

        def_box = SurroundingRectangle(
            def_text,
            color=YELLOW,
            buff=0.35,
            corner_radius=0.18,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=3,
        )
        definition_group = VGroup(def_box, def_text)
        definition_group.to_edge(DOWN, buff=0.55)

        # -- 0.00-1.68: heading fades in, clean screen --
        self.play(FadeIn(heading), run_time=max(0.05, 1.68))

        # -- 1.68-2.40: brief pause --
        self.wait(max(0.05, 0.72))

        # -- 2.40-7.26: definition box fades in, pulses once --
        self.play(FadeIn(definition_group), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 0.40))
        self.play(
            def_box.animate.set_stroke(WHITE, width=7).set_fill(YELLOW, opacity=0.25),
            rate_func=there_and_back,
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 2.26))

        # -- 7.26-7.80: definition steadies --
        self.wait(max(0.05, 0.54))

        # -- Build EEG waveform segments --
        wave_y_center = 0.7

        # Segment 1: eyes closed, slow large-alpha rhythm
        xs1 = np.linspace(-6.0, -2.0, 400)
        ys1 = 0.65 * np.sin(2 * PI * (xs1 + 6.0) / 2.0)
        seg1 = VMobject(stroke_color=TEAL, stroke_width=4)
        seg1.set_points_as_corners([np.array([x, wave_y_center + y, 0.0]) for x, y in zip(xs1, ys1)])

        # Segment 2: eyes open, smaller amplitude higher frequency
        xs2 = np.linspace(-2.0, 0.8, 320)
        ys2 = 0.22 * np.sin(2 * PI * (xs2 + 2.0) / 0.5)
        seg2 = VMobject(stroke_color=TEAL, stroke_width=4)
        seg2.set_points_as_corners([np.array([x, wave_y_center + y, 0.0]) for x, y in zip(xs2, ys2)])

        # Segment 3: visual stimulus transient bump
        xs3 = np.linspace(0.8, 1.4, 100)
        ys3 = 0.22 * np.sin(2 * PI * (xs3 + 2.0) / 0.5) + 0.8 * np.exp(-((xs3 - 1.1) / 0.12) ** 2)
        stim_seg = VMobject(stroke_color=TEAL, stroke_width=4)
        stim_seg.set_points_as_corners([np.array([x, wave_y_center + y, 0.0]) for x, y in zip(xs3, ys3)])

        # Segment 4: memory task, irregular mixed frequencies, moderate amplitude
        xs4 = np.linspace(1.4, 6.0, 450)
        ys4 = 0.35 * np.sin(2 * PI * (xs4 - 1.4) / 0.9 + 0.377) + 0.15 * np.sin(
            2 * PI * (xs4 - 1.4) / 0.28
        )
        memory_seg = VMobject(stroke_color=TEAL, stroke_width=4)
        memory_seg.set_points_as_corners([np.array([x, wave_y_center + y, 0.0]) for x, y in zip(xs4, ys4)])

        wave_segments = VGroup(seg1, seg2, stim_seg, memory_seg)

        # -- 7.80-11.76: first segment draws from left to right --
        self.play(Create(seg1), run_time=max(0.05, 3.96))

        # -- 11.76-12.38: pause with first segment on screen --
        self.wait(max(0.05, 0.62))

        # -- 12.38-16.00: "Eyes closed" label appears over first segment --
        label_eyes_closed = Text("Eyes closed", font_size=20, weight="BOLD", color=WHITE)
        label_eyes_closed.move_to(np.array([-4.0, 1.85, 0.0]))
        labels_group = VGroup(label_eyes_closed)
        self.play(FadeIn(label_eyes_closed), run_time=max(0.05, 0.55))
        self.play(label_eyes_closed.animate.set_color(YELLOW).scale(1.15), run_time=max(0.05, 0.50))
        self.play(label_eyes_closed.animate.set_color(WHITE).scale(1 / 1.15), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 2.07))

        # -- 16.00-16.84: transition to smaller, faster waves --
        self.play(Create(seg2), run_time=max(0.05, 0.84))

        # -- 16.84-18.66: "Eyes open" label appears above middle segment --
        label_eyes_open = Text("Eyes open", font_size=20, weight="BOLD", color=WHITE)
        label_eyes_open.move_to(np.array([-0.9, 1.85, 0.0]))
        labels_group.add(label_eyes_open)
        self.play(FadeIn(label_eyes_open), run_time=max(0.05, 0.50))
        self.play(label_eyes_open.animate.set_color(YELLOW).scale(1.15), run_time=max(0.05, 0.50))
        self.play(label_eyes_open.animate.set_color(WHITE).scale(1 / 1.15), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.32))

        # -- 18.66-19.34: smaller-amplitude state continues --
        self.wait(max(0.05, 0.68))

        # -- 19.34-21.62: transient visual stimulus bump + label --
        self.play(Create(stim_seg), run_time=max(0.05, 0.80))
        label_visual = Text("Visual stimulus", font_size=20, weight="BOLD", color=WHITE)
        label_visual.move_to(np.array([1.15, 1.85, 0.0]))
        labels_group.add(label_visual)
        self.play(FadeIn(label_visual), run_time=max(0.05, 0.50))
        self.play(label_visual.animate.set_color(YELLOW).scale(1.15), run_time=max(0.05, 0.35))
        self.play(label_visual.animate.set_color(WHITE).scale(1 / 1.15), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.28))

        # -- 21.62-22.76: memory task irregular segment draws --
        self.play(Create(memory_seg), run_time=max(0.05, 1.14))

        # -- 22.76-24.48: "Memory task" label appears --
        label_memory = Text("Memory task", font_size=20, weight="BOLD", color=WHITE)
        label_memory.move_to(np.array([3.9, 1.85, 0.0]))
        labels_group.add(label_memory)
        self.play(FadeIn(label_memory), run_time=max(0.05, 0.50))
        self.play(label_memory.animate.set_color(YELLOW).scale(1.15), run_time=max(0.05, 0.50))
        self.play(label_memory.animate.set_color(WHITE).scale(1 / 1.15), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.22))

        # -- 24.48-25.20: full waveform with all four labels --
        self.wait(max(0.05, 0.72))

        # -- 25.20-28.12: waveform continues scrolling, labels stay --
        self.wait(max(0.05, 2.92))

        # -- 28.12-28.96: brief pause before frequency comparison --
        self.wait(max(0.05, 0.84))

        # -- Build two frequency-domain inset plots --
        plot_left_center = np.array([-3.05, -0.95, 0.0])
        plot_right_center = np.array([2.35, -0.95, 0.0])

        # Fixed: removed corner_radius from Rectangle.
        left_box = Rectangle(
            width=2.9,
            height=1.35,
            color=BLUE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.10,
        ).move_to(plot_left_center)

        right_box = Rectangle(
            width=2.9,
            height=1.35,
            color=BLUE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.10,
        ).move_to(plot_right_center)

        title_left = Text("Beginning", font_size=20, weight="BOLD", color=WHITE)
        title_left.move_to(left_box.get_top() + UP * 0.18)

        title_right = Text("Later", font_size=20, weight="BOLD", color=WHITE)
        title_right.move_to(right_box.get_top() + UP * 0.18)

        left_axis_line = Line(LEFT * 1.15, RIGHT * 1.15, color=GREY_B, stroke_width=2)
        left_axis_line.move_to(np.array([plot_left_center[0], plot_left_center[1] - 0.40, 0.0]))

        right_axis_line = Line(LEFT * 1.15, RIGHT * 1.15, color=GREY_B, stroke_width=2)
        right_axis_line.move_to(np.array([plot_right_center[0], plot_right_center[1] - 0.40, 0.0]))

        plot_left_infra = VGroup(left_box, left_axis_line, title_left)
        plot_right_infra = VGroup(right_box, right_axis_line, title_right)

        left_base_y = plot_left_center[1] - 0.40
        right_base_y = plot_right_center[1] - 0.40

        def make_bar(center_x, base_y, height, color):
            bar = Rectangle(
                width=0.28,
                height=height,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            bar.move_to(np.array([center_x, base_y + height / 2, 0.0]))
            return bar

        beg_low_bar = make_bar(plot_left_center[0] - 0.55, left_base_y, 0.85, GREEN)
        beg_mid_bar = make_bar(plot_left_center[0] + 0.45, left_base_y, 0.30, TEAL)

        later_low_bar = make_bar(plot_right_center[0] - 0.55, right_base_y, 0.85, GREEN)
        later_high1_bar = make_bar(plot_right_center[0] + 0.45, right_base_y, 0.55, TEAL)
        later_new_bar = make_bar(plot_right_center[0] + 1.00, right_base_y, 0.65, ORANGE)

        arrow_spec = Arrow(
            start=left_box.get_right() + RIGHT * 0.20,
            end=right_box.get_left() + LEFT * 0.20,
            color=YELLOW,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.18,
        )

        inset_dim_group = VGroup(
            plot_left_infra,
            plot_right_infra,
            arrow_spec,
            beg_low_bar,
            beg_mid_bar,
            later_high1_bar,
            later_new_bar,
        )

        # -- 28.96-32.50: inset plots fade in, bars rise / low-frequency bar shrinks --
        self.play(FadeIn(plot_left_infra, plot_right_infra, arrow_spec, later_low_bar), run_time=max(0.05, 0.90))
        self.play(
            GrowFromEdge(beg_low_bar, DOWN),
            GrowFromEdge(beg_mid_bar, DOWN),
            GrowFromEdge(later_high1_bar, DOWN),
            later_low_bar.animate.scale(0.35, about_edge=DOWN),
            run_time=max(0.05, 1.50),
        )
        self.wait(max(0.05, 1.14))

        # -- 32.50-33.30: inset plots remain visible --
        self.wait(max(0.05, 0.80))

        # -- 33.30-36.76: new high-frequency bar appears; original low bar fades in Later --
        self.play(FadeIn(later_new_bar), later_low_bar.animate.set_opacity(0.20), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 2.26))

        # -- 36.76-37.64: brief pause --
        self.wait(max(0.05, 0.88))

        # -- 37.64-41.66: Beginning/Later plots highlight alternately, arrow pulses --
        self.play(left_box.animate.set_stroke(YELLOW, width=5), run_time=max(0.05, 0.70))
        self.play(
            left_box.animate.set_stroke(BLUE, width=2),
            right_box.animate.set_stroke(YELLOW, width=5),
            run_time=max(0.05, 0.70),
        )
        self.play(
            arrow_spec.animate.set_color(ORANGE).scale(1.15, about_point=arrow_spec.get_center()),
            rate_func=there_and_back,
            run_time=max(0.05, 0.80),
        )
        self.play(right_box.animate.set_stroke(BLUE, width=2), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.32))

        # -- 41.66-42.36: inset plots dim, definition box begins to highlight --
        self.play(
            inset_dim_group.animate.set_opacity(0.55),
            later_low_bar.animate.set_opacity(0.12),
            def_box.animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=0.20),
            run_time=max(0.05, 0.70),
        )

        # -- 42.36-47.30: definition box pulses and glows --
        self.play(
            def_box.animate.set_stroke(ORANGE, width=7).set_fill(YELLOW, opacity=0.30),
            rate_func=there_and_back,
            run_time=max(0.05, 0.90),
        )
        self.wait(max(0.05, 0.80))
        self.play(
            def_box.animate.set_stroke(ORANGE, width=7).set_fill(YELLOW, opacity=0.30),
            rate_func=there_and_back,
            run_time=max(0.05, 0.90),
        )
        self.wait(max(0.05, 2.34))

        # -- 47.30-48.08: steady highlighted definition, brief pause --
        self.wait(max(0.05, 0.78))

        # -- 48.08-56.04: EEG and insets fade, faint generic spectrum appears and fades --
        faint_curve_xs = np.linspace(-1.1, 1.1, 120)
        faint_curve_ys = 0.35 * np.exp(-((faint_curve_xs / 0.40) ** 2))
        faint_curve = VMobject(stroke_color=GREY_B, stroke_width=2)
        faint_curve.set_points_as_corners(
            [np.array([x, y, 0.0]) for x, y in zip(faint_curve_xs, faint_curve_ys)]
        )

        faint_spectrum = VGroup(
            Line(LEFT * 1.5, RIGHT * 1.5, color=GREY_B, stroke_width=1.5),
            Line(UP * 0.5, DOWN * 0.5, color=GREY_B, stroke_width=1.5),
            faint_curve,
        )
        faint_spectrum.set_opacity(0.22)
        faint_spectrum.move_to(definition_group.get_center() + DOWN * 0.10)
        faint_spectrum.set_z_index(0)
        definition_group.set_z_index(1)
        heading.set_z_index(1)

        self.play(FadeOut(wave_segments, labels_group, inset_dim_group, later_low_bar), run_time=max(0.05, 1.40))
        self.wait(max(0.05, 0.80))
        self.play(FadeIn(faint_spectrum), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.70))
        self.play(FadeOut(faint_spectrum), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 3.46))

        # -- 56.04-56.90: final hold --
        self.wait(max(0.05, 0.86))