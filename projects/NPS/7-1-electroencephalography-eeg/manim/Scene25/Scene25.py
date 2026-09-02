ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene25(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_wave(func, x_min, x_max, color=YELLOW, stroke_width=2.5, num_points=120):
            vm = VMobject()
            vm.set_stroke(color=color, width=stroke_width, opacity=1)
            x = np.linspace(x_min, x_max, num_points)
            y = func(x)
            vm.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return vm

        def make_block_rect(label, color, x, y, width=1.5, height=0.9):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.1,
                fill_color=GREY_B, fill_opacity=0.25,
                stroke_color=GREY_B, stroke_width=2.5,
            )
            rect.move_to(np.array([x, y, 0]))
            lab = Text(label, font_size=12, weight="BOLD", color=GREY_B)
            lab.scale_to_fit_width(width * 0.85)
            lab.move_to(rect.get_center())
            return rect, lab

        def make_head_drawing():
            a, b = 0.25, 0.32
            head_ellipse = Ellipse(
                width=2 * a, height=2 * b,
                stroke_color=WHITE, stroke_width=2.5,
                fill_color=GREY_B, fill_opacity=0.2,
            )
            dots = VGroup()
            leads = VGroup()
            xs = [-0.16, -0.06, 0.06, 0.16]
            for x in xs:
                y = b * np.sqrt(max(0, 1 - (x / a) ** 2))
                pt = head_ellipse.get_center() + np.array([x, y, 0])
                dot = Circle(radius=0.04, fill_color=ORANGE, fill_opacity=1,
                             stroke_color=WHITE, stroke_width=1.2)
                dot.move_to(pt)
                lead = Line(
                    pt,
                    head_ellipse.get_center() + np.array([x, -b * 0.6, 0]),
                    color=GREY_B, stroke_width=1.2,
                )
                dots.add(dot)
                leads.add(lead)
            head_group = VGroup(head_ellipse, leads, dots)
            head_group.scale_to_fit_height(0.62)
            head_group.scale_to_fit_width(0.62)
            return head_group, head_ellipse, dots, leads

        def make_filter_icon():
            hline = Line(LEFT * 0.25, RIGHT * 0.25, color=WHITE, stroke_width=2)
            wave = make_wave(lambda x: 0.04 * np.sin(2 * np.pi * 5 * x), -0.25, 0.25,
                             color=YELLOW, stroke_width=2)
            wave.scale_to_fit_width(0.45)
            icon = VGroup(hline, wave).arrange(DOWN, buff=0.05)
            label = Text("Filter", font_size=9, color=WHITE).scale_to_fit_width(0.75)
            return VGroup(icon, label).arrange(DOWN, buff=0.06)

        def make_artifact_icon():
            jagged = VMobject()
            jagged.set_stroke(color=ORANGE, width=2, opacity=1)
            pts = [
                [-0.3, 0, 0], [-0.1, 0.18, 0], [0.0, 0, 0],
                [0.1, 0.18, 0], [0.2, 0, 0]
            ]
            jagged.set_points_as_corners(np.array(pts))
            jagged.scale_to_fit_width(0.6)
            x1 = Line(jagged.get_left() + LEFT * 0.05 + UP * 0.08,
                      jagged.get_right() + RIGHT * 0.05 + DOWN * 0.08,
                      color=WHITE, stroke_width=2)
            x2 = Line(jagged.get_left() + LEFT * 0.05 + DOWN * 0.08,
                      jagged.get_right() + RIGHT * 0.05 + UP * 0.08,
                      color=WHITE, stroke_width=2)
            icon = VGroup(jagged, x1, x2)
            label = Text("Artifact Removal", font_size=9, color=WHITE).scale_to_fit_width(0.8)
            return VGroup(icon, label).arrange(DOWN, buff=0.06)

        def make_bar_chart_icon():
            base = Line(LEFT * 0.3, RIGHT * 0.3, color=WHITE, stroke_width=2)
            b1 = Rectangle(width=0.08, height=0.2, fill_color=BLUE, fill_opacity=1,
                           stroke_width=0).move_to(base.get_left() + RIGHT * 0.1 + UP * 0.1)
            b2 = Rectangle(width=0.08, height=0.3, fill_color=GREEN, fill_opacity=1,
                           stroke_width=0).move_to(base.get_center() + UP * 0.15)
            b3 = Rectangle(width=0.08, height=0.15, fill_color=ORANGE, fill_opacity=1,
                           stroke_width=0).move_to(base.get_right() + LEFT * 0.1 + UP * 0.075)
            icon = VGroup(base, b1, b2, b3)
            label = Text("Frequency-Band Power", font_size=9, color=WHITE).scale_to_fit_width(0.75)
            return VGroup(icon, label).arrange(DOWN, buff=0.06)

        def make_p300_wave():
            vm = VMobject()
            vm.set_stroke(color=YELLOW, width=2.5, opacity=1)
            x = np.linspace(-0.4, 0.4, 100)
            y = 0.02 * np.sin(2 * np.pi * 3 * x) + 0.25 * np.exp(-((x - 0.1) / 0.07) ** 2)
            vm.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            vm.scale_to_fit_width(0.5)
            label = Text("P300", font_size=10, color=WHITE)
            return VGroup(vm, label).arrange(DOWN, buff=0.06)

        def make_tf_icon():
            outer = Rectangle(width=0.45, height=0.35, stroke_color=WHITE, stroke_width=2)
            patches = VGroup(*[
                Rectangle(width=0.08, height=0.06, fill_color=ORANGE, fill_opacity=0.9,
                          stroke_width=0)
                for _ in range(4)
            ]).arrange_in_grid(rows=2, cols=2, buff=0.04).move_to(outer.get_center())
            label = Text("Time-Frequency Features", font_size=9, color=WHITE).scale_to_fit_width(0.8)
            return VGroup(outer, patches, label).arrange(DOWN, buff=0.06)

        def make_topo_icon():
            head = Ellipse(width=0.4, height=0.5, fill_color=GREY_B, fill_opacity=0.2,
                           stroke_color=WHITE, stroke_width=2)
            region1 = Ellipse(width=0.15, height=0.2, fill_color=PINK, fill_opacity=0.7,
                              stroke_width=0).move_to(head.get_center() + LEFT * 0.07 + UP * 0.05)
            region2 = Ellipse(width=0.1, height=0.15, fill_color=ORANGE, fill_opacity=0.8,
                              stroke_width=0).move_to(head.get_center() + RIGHT * 0.08 + DOWN * 0.03)
            icon = VGroup(head, region1, region2)
            label = Text("Spatial Features", font_size=9, color=WHITE).scale_to_fit_width(0.75)
            return VGroup(icon, label).arrange(DOWN, buff=0.06)

        def make_decision_tree_icon():
            root = Circle(radius=0.05, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            root.move_to(UP * 0.3)
            split_pt = DOWN * 0.05
            trunk = Line(root.get_bottom(), split_pt, color=WHITE, stroke_width=2)
            branches = VGroup()
            endpoints = [
                LEFT * 0.22 + DOWN * 0.35,
                LEFT * 0.07 + DOWN * 0.35,
                RIGHT * 0.07 + DOWN * 0.35,
                RIGHT * 0.22 + DOWN * 0.35,
            ]
            for ep in endpoints:
                branch = Line(split_pt, ep, color=WHITE, stroke_width=1.5)
                leaf = Circle(radius=0.04, fill_color=GREEN, fill_opacity=1,
                              stroke_width=0).move_to(ep)
                branches.add(branch, leaf)
            group = VGroup(root, trunk, branches)
            group.scale_to_fit_width(0.55)
            return group

        # ---------- pipeline construction ----------
        labels_text = [
            "Signal Acquisition",
            "Preprocessing",
            "Feature Extraction",
            "Classification",
            "Device Control",
        ]
        block_colors = [BLUE, TEAL, GREEN, PURPLE, ORANGE]
        xs = [-4.0, -2.0, 0.0, 2.0, 4.0]
        row_y = -0.4

        rects = []
        block_labels = []
        for i, label in enumerate(labels_text):
            rect, lab = make_block_rect(label, block_colors[i], xs[i], row_y)
            rects.append(rect)
            block_labels.append(lab)

        # static initial arrows for fade-in
        initial_arrows = VGroup(*[
            Arrow(
                rects[i].get_right() + RIGHT * 0.03,
                rects[i + 1].get_left() + LEFT * 0.03,
                color=GREY_B, stroke_width=3, buff=0.05,
                max_tip_length_to_length_ratio=0.45,
            )
            for i in range(4)
        ])
        title = Text("EEG-Based BCI Processing Stages", font_size=30, weight="BOLD", color=YELLOW)
        title.scale_to_fit_width(10.0)
        title.move_to(UP * 3.0)

        self.class_arrow_active = False
        self.command_arrow_active = False

        def get_arrows():
            arrows = []
            for i in range(4):
                color = GREY_B
                sw = 3
                if i == 3:
                    if self.command_arrow_active:
                        color = ORANGE
                        sw = 10
                    elif self.class_arrow_active:
                        color = YELLOW
                        sw = 7
                arr = Arrow(
                    rects[i].get_right() + RIGHT * 0.03,
                    rects[i + 1].get_left() + LEFT * 0.03,
                    color=color, stroke_width=sw, buff=0.05,
                    max_tip_length_to_length_ratio=0.45,
                )
                arrows.append(arr)
            return VGroup(*arrows)

        connection_arrows = always_redraw(get_arrows)

        # class label following the third inter-block arrow
        class_label = Text("Class Label", font_size=10, color=YELLOW)
        class_label.set_opacity(0)
        class_label.add_updater(lambda m: m.move_to(
            (rects[3].get_right() + rects[4].get_left()) / 2 + DOWN * 0.15
        ))
        self.add(class_label)

        # ---------- beat 1: 0.00-4.52 ----------
        self.play(
            FadeIn(title),
            FadeIn(VGroup(*rects, *block_labels, initial_arrows)),
            run_time=max(0.05, 4.52),
        )
        self.remove(initial_arrows)
        self.add(connection_arrows)

        # ---------- beat 2: 4.52-6.90 ----------
        self.play(
            rects[0].animate.set_stroke(BLUE, width=4).set_fill(BLUE, opacity=0.4).scale(1.12),
            block_labels[0].animate.set_color(WHITE),
            run_time=max(0.05, 0.9),
        )
        head_group, head_ellipse, electrode_dots, electrode_leads = make_head_drawing()
        head_group.move_to(rects[0].get_center() + DOWN * 0.15)
        self.play(
            block_labels[0].animate.move_to(rects[0].get_top() + DOWN * 0.22),
            Create(head_group),
            run_time=max(0.05, 1.48),
        )

        # ---------- beat 3: 6.90-10.18 ----------
        trace_group = VGroup()
        for dot in electrode_dots:
            trace = VMobject()
            trace.set_stroke(color=YELLOW, width=2, opacity=0.8)
            x = np.linspace(-0.1, 0.1, 30)
            y = 0.03 * np.sin(2 * np.pi * 8 * x) * np.exp(-((x) / 0.06) ** 2)
            trace.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            trace.move_to(dot.get_center() + UP * 0.12)
            trace_group.add(trace)

        pulse_group = VGroup(*electrode_dots, *trace_group)
        pulse_t = ValueTracker(0)

        def update_pulse(mob):
            val = pulse_t.get_value()
            op = 0.65 + 0.3 * np.sin(2 * np.pi * 1.5 * val)
            mob.set_opacity(max(0.2, op))

        pulse_group.add_updater(update_pulse)

        self.play(
            head_ellipse.animate.set_stroke(YELLOW, width=5),
            Create(trace_group),
            run_time=max(0.05, 1.1),
        )
        self.play(pulse_t.animate.set_value(2.0), run_time=max(0.05, 2.18))
        pulse_group.clear_updaters()
        pulse_group.set_opacity(1)

        # gap 10.18-11.00
        self.wait(max(0.05, 0.82))

        # ---------- beat 4: 11.00-13.12 ----------
        self.play(
            rects[0].animate.scale(1 / 1.12),
            rects[1].animate.set_stroke(TEAL, width=4).set_fill(TEAL, opacity=0.4).scale(1.12),
            block_labels[1].animate.set_color(WHITE),
            run_time=max(0.05, 2.12),
        )

        # ---------- beat 5: 13.12-17.60 ----------
        filter_icon = make_filter_icon()
        artifact_icon = make_artifact_icon()
        preproc_icons = VGroup(filter_icon, artifact_icon).arrange(RIGHT, buff=0.3)
        preproc_icons.scale_to_fit_width(1.3)
        preproc_icons.move_to(rects[1].get_center() + DOWN * 0.18)

        wave_y = rects[1].get_bottom()[1] + 0.2
        noisy_wave = make_wave(
            lambda x: 0.08 * np.sin(2 * np.pi * 4 * x) + 0.06 * np.sin(2 * np.pi * 11 * x) +
                      0.05 * np.sin(2 * np.pi * 19 * x),
            -0.7, 0.7, color=GREY_B, stroke_width=2.2,
        )
        noisy_wave.scale_to_fit_width(1.3)
        noisy_wave.move_to(np.array([rects[1].get_left()[0] - 0.25, wave_y, 0]))

        clean_wave = make_wave(
            lambda x: 0.09 * np.sin(2 * np.pi * 1.8 * x),
            -0.7, 0.7, color=GREEN, stroke_width=2.8,
        )
        clean_wave.scale_to_fit_width(1.3)
        clean_wave.move_to(np.array([rects[1].get_center()[0], wave_y, 0]))

        self.play(
            block_labels[1].animate.move_to(rects[1].get_top() + DOWN * 0.22),
            FadeIn(preproc_icons),
            run_time=max(0.05, 0.8),
        )
        self.play(Create(noisy_wave), run_time=max(0.05, 0.6))
        self.play(noisy_wave.animate.move_to(rects[1].get_center()), run_time=max(0.05, 1.2))
        self.play(Transform(noisy_wave, clean_wave), run_time=max(0.05, 0.8))
        self.play(
            noisy_wave.animate.move_to(
                np.array([rects[1].get_right()[0] + 0.25, wave_y, 0])
            ),
            run_time=max(0.05, 1.08),
        )

        # gap 17.60-18.38
        self.wait(max(0.05, 0.78))

        # ---------- beat 6: 18.38-20.86 ----------
        self.play(
            rects[1].animate.scale(1 / 1.12),
            rects[2].animate.set_stroke(GREEN, width=4).set_fill(GREEN, opacity=0.4).scale(1.12),
            block_labels[2].animate.set_color(WHITE),
            run_time=max(0.05, 2.48),
        )

        # ---------- beat 7: 20.86-23.98 ----------
        self.play(
            block_labels[2].animate.move_to(rects[2].get_top() + DOWN * 0.22),
            noisy_wave.animate.move_to(rects[2].get_left() + RIGHT * 0.15),
            run_time=max(0.05, 0.8),
        )

        marker_shapes = [
            Circle(radius=0.05, fill_color=YELLOW, fill_opacity=1,
                   stroke_color=WHITE, stroke_width=1.5),
            Triangle(fill_color=ORANGE, fill_opacity=1,
                     stroke_color=WHITE, stroke_width=1.5).scale(0.22),
            Rectangle(width=0.08, height=0.14, fill_color=TEAL, fill_opacity=1,
                      stroke_color=WHITE, stroke_width=1.5),
            Circle(radius=0.04, fill_color=PINK, fill_opacity=1,
                   stroke_color=WHITE, stroke_width=1.5),
            Triangle(fill_color=PURPLE, fill_opacity=1,
                     stroke_color=WHITE, stroke_width=1.5).scale(0.18),
        ]
        feature_markers = VGroup(*marker_shapes)
        wave_points = [
            noisy_wave.point_from_proportion(p) for p in [0.2, 0.4, 0.6, 0.8, 0.5]
        ]
        for marker, pt in zip(feature_markers, wave_points):
            marker.move_to(pt)

        self.play(FadeIn(feature_markers), run_time=max(0.05, 0.4))
        self.play(
            feature_markers.animate.arrange(RIGHT, buff=0.12).move_to(
                rects[2].get_bottom() + UP * 0.2
            ),
            run_time=max(0.05, 1.92),
        )

        # gap 23.98-25.02
        self.wait(max(0.05, 1.04))

        # ---------- beat 8: 25.02-32.96 ----------
        mini_bar = make_bar_chart_icon()
        mini_p300 = make_p300_wave()
        mini_tf = make_tf_icon()
        mini_topo = make_topo_icon()
        mini_icons = [mini_bar, mini_p300, mini_tf, mini_topo]
        mini_grid = VGroup(*mini_icons).arrange_in_grid(rows=2, cols=2, buff=0.14)
        mini_grid.scale_to_fit_width(1.5)
        mini_grid.scale_to_fit_height(0.68)
        mini_grid.move_to(rects[2].get_center() + DOWN * 0.12)
        for icon in mini_icons:
            icon.set_opacity(0)
        self.add(mini_grid)

        self.play(FadeOut(feature_markers), run_time=max(0.05, 0.84))  # 25.02-25.86

        self.play(FadeIn(mini_icons[0]), run_time=max(0.05, 0.35))
        self.play(Indicate(mini_icons[0]), run_time=max(0.05, 0.35))  # ends 26.56
        self.wait(max(0.05, 1.08))  # to 27.64

        self.play(FadeIn(mini_icons[1]), run_time=max(0.05, 0.35))
        self.play(Indicate(mini_icons[1]), run_time=max(0.05, 0.35))  # ends 28.34
        self.wait(max(0.05, 1.50))  # to 29.84

        self.play(FadeIn(mini_icons[2]), run_time=max(0.05, 0.35))
        self.play(Indicate(mini_icons[2]), run_time=max(0.05, 0.35))  # ends 30.54
        self.wait(max(0.05, 1.50))  # to 32.04

        self.play(FadeIn(mini_icons[3]), run_time=max(0.05, 0.35))
        self.play(Indicate(mini_icons[3]), run_time=max(0.05, 0.35))  # ends 32.74
        self.wait(max(0.05, 0.22))  # to 32.96

        # gap 32.96-33.66
        self.wait(max(0.05, 0.70))

        # ---------- beat 9: 33.66-36.10 ----------
        self.play(
            rects[2].animate.scale(1 / 1.12),
            rects[3].animate.set_stroke(PURPLE, width=4).set_fill(PURPLE, opacity=0.4).scale(1.12),
            block_labels[3].animate.set_color(WHITE),
            run_time=max(0.05, 2.44),
        )

        # ---------- beat 10: 36.10-41.32 ----------
        decision_tree = make_decision_tree_icon()
        decision_tree.move_to(rects[3].get_center() + DOWN * 0.15)

        flow_shapes = [
            Circle(radius=0.05, fill_color=YELLOW, fill_opacity=1,
                   stroke_color=WHITE, stroke_width=1),
            Triangle(fill_color=ORANGE, fill_opacity=1,
                     stroke_color=WHITE, stroke_width=1).scale(0.22),
            Rectangle(width=0.1, height=0.12, fill_color=TEAL, fill_opacity=1,
                      stroke_color=WHITE, stroke_width=1),
            Circle(radius=0.05, fill_color=PINK, fill_opacity=1,
                   stroke_color=WHITE, stroke_width=1),
            Triangle(fill_color=PURPLE, fill_opacity=1,
                     stroke_color=WHITE, stroke_width=1).scale(0.2),
        ]
        flow_markers = VGroup(*flow_shapes).arrange(RIGHT, buff=0.1)
        flow_markers.scale_to_fit_width(1.0)
        flow_markers.move_to(rects[2].get_right() + RIGHT * 0.2)

        self.play(
            block_labels[3].animate.move_to(rects[3].get_top() + DOWN * 0.22),
            FadeIn(decision_tree),
            run_time=max(0.05, 0.7),
        )
        self.play(Create(flow_markers), run_time=max(0.05, 0.5))
        self.play(flow_markers.animate.move_to(rects[3].get_center() + DOWN * 0.25), run_time=max(0.05, 1.1))

        self.class_arrow_active = True
        self.play(
            flow_markers.animate.move_to(rects[3].get_right() + LEFT * 0.1).set_opacity(0),
            class_label.animate.set_opacity(1),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 1.42))  # to 41.32

        # gap 41.32-42.24
        self.wait(max(0.05, 0.92))

        # ---------- beat 11: 42.24-44.76 ----------
        self.play(
            rects[3].animate.scale(1 / 1.12),
            rects[4].animate.set_stroke(ORANGE, width=4).set_fill(ORANGE, opacity=0.4).scale(1.12),
            block_labels[4].animate.set_color(WHITE),
            run_time=max(0.05, 2.52),
        )

        # ---------- beat 12: 44.76-49.67 ----------
        screen = RoundedRectangle(
            width=0.5, height=0.3, corner_radius=0.04,
            fill_color=BLUE, fill_opacity=0.95,
            stroke_color=WHITE, stroke_width=1.5,
        )
        buttons = VGroup(*[
            Circle(radius=0.04, fill_color=WHITE, fill_opacity=0.7, stroke_width=0)
            for _ in range(2)
        ]).arrange(RIGHT, buff=0.1).next_to(screen, DOWN, buff=0.08)
        device_icon = VGroup(screen, buttons)
        device_icon.scale_to_fit_width(0.55)
        device_label = Text("External Device", font_size=10, color=WHITE)
        device_group = VGroup(device_icon, device_label).arrange(DOWN, buff=0.05)
        device_group.move_to(rects[4].get_bottom() + UP * 0.4)

        self.play(
            block_labels[4].animate.move_to(rects[4].get_top() + DOWN * 0.22),
            run_time=max(0.05, 0.5),
        )
        self.play(FadeIn(device_group), run_time=max(0.05, 0.7))

        self.command_arrow_active = True
        self.play(class_label.animate.set_color(ORANGE), run_time=max(0.05, 0.5))

        for _ in range(3):
            self.play(device_icon.animate.scale(1.15), run_time=max(0.05, 0.6))
            self.play(device_icon.animate.scale(1 / 1.15), run_time=max(0.05, 0.4))

        self.wait(max(0.05, 0.21))  # hold full pipeline to end