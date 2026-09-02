ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene10(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_blob(center=ORIGIN, rx=1.5, ry=1.0, seed=11,
                     stroke_color=WHITE, stroke_width=2,
                     fill_color=BLUE, fill_opacity=0.18):
            pts = []
            n = 40
            for i in range(n):
                theta = 2 * np.pi * i / n
                rf = (1 + 0.07 * np.sin(3 * theta + 0.4)
                      + 0.05 * np.cos(5 * theta + 1.2)
                      + 0.03 * np.sin(2 * theta + 2.0))
                pts.append(center + np.array([
                    rx * rf * np.cos(theta),
                    ry * rf * np.sin(theta),
                    0,
                ]))
            return Polygon(
                *pts,
                color=stroke_color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_width=stroke_width,
            )

        def make_electrode(center, label=None, label_dir=DOWN):
            shank = Line(
                center + UP * 0.7,
                center + DOWN * 0.7,
                color=WHITE,
                stroke_width=3,
            )
            tip = Dot(center + DOWN * 0.75, radius=0.07, color=YELLOW, fill_opacity=1)
            parts = [shank, tip]
            lbl = None
            if label is not None:
                lbl = Text(label, font_size=13, color=WHITE).next_to(
                    center + DOWN * 0.75, label_dir, buff=0.10
                )
                parts.append(lbl)
            return {"group": VGroup(*parts), "shank": shank, "tip": tip, "label": lbl}

        def make_region(center, region_text=None, elec_text=None, seed=11):
            blob = make_blob(center, rx=1.4, ry=1.0, seed=seed)
            shank = Line(center + UP * 0.7, center + DOWN * 0.7,
                         color=WHITE, stroke_width=3)
            tip = Dot(center + DOWN * 0.75, radius=0.07,
                      color=YELLOW, fill_opacity=1)
            parts = [blob, shank, tip]
            rlabel = None
            elabel = None
            if region_text is not None:
                rlabel = Text(region_text, font_size=18, color=WHITE).move_to(
                    center + UP * 0.55
                )
                parts.append(rlabel)
            if elec_text is not None:
                elabel = Text(elec_text, font_size=13, color=WHITE).next_to(
                    center + DOWN * 0.75, DOWN, buff=0.10
                )
                parts.append(elabel)
            return {
                "group": VGroup(*parts),
                "blob": blob,
                "shank": shank,
                "tip": tip,
                "region_label": rlabel,
                "electrode_label": elabel,
            }

        def make_small_region(center, region_text=None, seed=31):
            blob = make_blob(center, rx=1.05, ry=0.65, seed=seed,
                             fill_opacity=0.22)
            shank = Line(center + UP * 0.5, center + DOWN * 0.5,
                         color=WHITE, stroke_width=2.5)
            tip = Dot(center + DOWN * 0.55, radius=0.06,
                      color=YELLOW, fill_opacity=1)
            parts = [blob, shank, tip]
            rlabel = None
            if region_text is not None:
                rlabel = Text(region_text, font_size=13, color=WHITE).move_to(
                    center + UP * 0.38
                )
                parts.append(rlabel)
            return {
                "group": VGroup(*parts),
                "blob": blob,
                "tip": tip,
                "region_label": rlabel,
            }

        def make_trace(center_y, phase=0.0, x_left=-4.8, x_right=4.8,
                       amp=0.28, n_cycles=3, color=WHITE, stroke_width=3):
            return FunctionGraph(
                lambda x: center_y + amp * np.sin(
                    2 * np.pi * n_cycles * (x - x_left) / (x_right - x_left)
                    + phase
                ),
                x_range=[x_left, x_right, 0.02],
                color=color,
                stroke_width=stroke_width,
            )

        def make_neuron(pos):
            soma = Circle(radius=0.07, fill_color=GREY_B,
                          fill_opacity=1, stroke_width=0).move_to(pos)
            dendrites = VGroup(*[
                Line(pos, pos + np.array([
                    0.18 * np.cos(a), 0.18 * np.sin(a), 0,
                ]), color=GREY_B, stroke_width=1.2)
                for a in [0, np.pi / 2, np.pi, 3 * np.pi / 2]
            ])
            return VGroup(soma, dendrites)

        def make_row(center, phase_shift, row_label_text=None):
            left_center = center + np.array([-2.7, 0.6, 0])
            right_center = center + np.array([2.7, 0.6, 0])
            left_region = make_region(left_center, region_text="region 1", seed=21)
            right_region = make_region(right_center, region_text="region 2", seed=22)
            trace1 = make_trace(center[1] - 0.6, phase=0.0, amp=0.25)
            trace2 = make_trace(center[1] - 1.5, phase=phase_shift, amp=0.25)
            row_label = None
            group = VGroup(left_region["group"], right_region["group"], trace1, trace2)
            if row_label_text is not None:
                row_label = Text(row_label_text, font_size=20, color=WHITE,
                                 weight=BOLD).move_to(center + UP * 1.5)
                group.add(row_label)
            return {
                "group": group,
                "left_region": left_region,
                "right_region": right_region,
                "trace1": trace1,
                "trace2": trace2,
                "label": row_label,
            }

        # ---------- previous-scene final composed thumbnail ----------
        prev_tissue = make_blob(LEFT * 1.0, rx=3.0, ry=1.8, seed=7,
                                fill_opacity=0.20)
        prev_neurons = VGroup(*[
            Dot(np.array([x, y, 0]), radius=0.05, color=GREY_B)
            for x, y in [(-2.6, 0.6), (-1.8, 1.3), (-0.4, 0.9),
                         (0.6, -0.4), (1.4, 0.5), (2.1, -0.2)]
        ])
        prev_halo_a = Ellipse(width=2.0, height=1.0, color=ORANGE,
                              fill_color=ORANGE, fill_opacity=0.20).move_to([-2.2, 0.8, 0])
        prev_halo_b = Ellipse(width=1.8, height=0.9, color=TEAL,
                              fill_color=TEAL, fill_opacity=0.20).move_to([0.2, -0.7, 0])
        prev_strip = Rectangle(width=0.9, height=3.0, stroke_color=GREY_B,
                               stroke_width=1.5, fill_color=GREY,
                               fill_opacity=0.10).move_to([3.1, 0.1, 0])
        prev_shanks = VGroup()
        prev_contacts = VGroup()
        for i, yy in enumerate([-1.1, -0.4, 0.3, 1.0]):
            shank = Line([2.9, yy, 0], [3.3, yy, 0], color=WHITE, stroke_width=2)
            dot = Dot([3.1, yy, 0], radius=0.05, color=YELLOW, fill_opacity=1)
            prev_shanks.add(shank)
            prev_contacts.add(dot)
        prev_panel = Rectangle(width=1.5, height=2.2, stroke_color=GREY_B,
                               stroke_width=1.5, fill_color=GREY,
                               fill_opacity=0.08).move_to([4.4, 0.1, 0])
        prev_spike_ticks = VGroup(*[
            Line([4.05 + dx, 0.55, 0], [4.05 + dx, 0.85, 0],
                 color=WHITE, stroke_width=2)
            for dx in [-0.25, 0.0, 0.22, 0.38]
        ])
        prev_lfp = make_trace(-0.6, phase=0.0, x_left=3.7, x_right=5.1,
                              amp=0.20, n_cycles=2, stroke_width=2.5)
        prev_caption = Text("network-level phenomena", font_size=26,
                            color=YELLOW, weight=BOLD).move_to([0, 3.25, 0])
        previous_final = VGroup(
            prev_tissue, prev_neurons, prev_halo_a, prev_halo_b,
            prev_strip, prev_shanks, prev_contacts, prev_panel,
            prev_spike_ticks, prev_lfp, prev_caption,
        )
        previous_final.scale_to_fit_width(11.5).move_to(ORIGIN)

        # ---------- beat 1: 0.00-5.36 ----------
        self.play(FadeIn(previous_final), run_time=max(0.05, 0.70))
        self.play(
            previous_final.animate.scale(0.28).to_corner(UL, buff=0.25).set_opacity(0.35),
            run_time=max(0.05, 1.50),
        )
        self.wait(max(0.05, 0.20))

        main_region1 = make_region(LEFT * 2.2 + UP * 1.2,
                                   region_text="region 1", elec_text="electrode 1",
                                   seed=101)
        main_region2 = make_region(RIGHT * 2.2 + UP * 1.2,
                                   region_text="region 2", elec_text="electrode 2",
                                   seed=102)

        main_trace1 = make_trace(-1.2, phase=0.0, x_left=-5, x_right=5,
                                 amp=0.40, n_cycles=3)
        main_trace2_offset = make_trace(-2.6, phase=1.4, x_left=-5, x_right=5,
                                        amp=0.40, n_cycles=3)
        main_trace2_aligned = make_trace(-2.6, phase=0.0, x_left=-5, x_right=5,
                                         amp=0.40, n_cycles=3)

        sync_text = Text("synchronized", font_size=28, color=YELLOW,
                         weight=BOLD).move_to([0, -3.45, 0])
        main_guide_lines = VGroup(
            DashedLine([-0.833, -0.80, 0], [-0.833, -3.00, 0],
                       color=WHITE, dash_length=0.08),
            DashedLine([2.500, -0.80, 0], [2.500, -3.00, 0],
                       color=WHITE, dash_length=0.08),
        )

        tick_axis = Line([-5, -3.05, 0], [5, -3.05, 0],
                         color=GREY_B, stroke_width=2)
        tick_marks = VGroup(*[
            Line([x, -3.05, 0], [x, -2.85, 0], color=WHITE, stroke_width=3)
            for x in [-4.167, -0.833, 2.500]
        ])
        tick_group = VGroup(tick_axis, tick_marks)

        freq_arrow = Line([-4.167, -0.55, 0], [2.500, -0.55, 0],
                          color=YELLOW, stroke_width=4)
        freq_arrow.add_tip(at_start=True)
        freq_arrow.add_tip(at_start=False)
        freq_text = Text("same frequency", font_size=24,
                         color=YELLOW).move_to([(-4.167 + 2.5) / 2, -0.25, 0])
        freq_annotation = VGroup(freq_text, freq_arrow)

        self.play(
            FadeIn(main_region1["group"]),
            FadeIn(main_region2["group"]),
            run_time=max(0.05, 1.60),
        )
        self.wait(max(0.05, 1.36))

        main_view_group = VGroup(
            main_region1["group"], main_region2["group"],
            main_trace1, main_trace2_offset, sync_text, main_guide_lines,
            tick_group, freq_annotation,
        )

        # ---------- beat 2: 5.36-7.20 ----------
        self.play(
            Create(main_trace1),
            Create(main_trace2_offset),
            run_time=max(0.05, 0.54),
        )
        self.play(
            Transform(main_trace2_offset, main_trace2_aligned),
            Create(main_guide_lines),
            FadeIn(sync_text),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.80))

        # ---------- beat 3: 7.20-11.28 ----------
        self.wait(max(0.05, 0.28))
        self.play(
            main_region1["region_label"].animate.set_color(YELLOW),
            main_region2["region_label"].animate.set_color(YELLOW),
            run_time=max(0.05, 0.52),
        )
        self.wait(max(0.05, 0.22))
        self.play(
            main_region1["blob"].animate.scale(
                1.05, about_point=main_region1["blob"].get_center()
            ).set_stroke(width=4),
            main_region2["blob"].animate.scale(
                1.05, about_point=main_region2["blob"].get_center()
            ).set_stroke(width=4),
            run_time=max(0.05, 0.20),
        )
        self.play(
            main_region1["blob"].animate.scale(
                1 / 1.05, about_point=main_region1["blob"].get_center()
            ).set_stroke(width=3),
            main_region2["blob"].animate.scale(
                1 / 1.05, about_point=main_region2["blob"].get_center()
            ).set_stroke(width=3),
            run_time=max(0.05, 0.20),
        )
        self.wait(max(0.05, 0.72))
        self.play(
            main_trace1.animate.set_stroke(color=YELLOW, width=5),
            main_trace2_offset.animate.set_stroke(color=YELLOW, width=5),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.74))
        self.play(Create(tick_group), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.05))
        self.play(FadeIn(freq_annotation), run_time=max(0.05, 0.25))

        # ---------- beat 4: 11.28-15.10 ----------
        self.wait(max(0.05, 0.84))

        top_row = make_row(np.array([0, 2.0, 0]), phase_shift=0.0,
                           row_label_text="phase-aligned")
        bottom_row = make_row(np.array([0, -2.0, 0]), phase_shift=np.pi)

        bottom_phase_guide = VGroup(
            DashedLine([-0.8, -2.35, 0], [-0.8, -3.25, 0],
                       color=YELLOW, dash_length=0.07),
            DashedLine([0.8, -2.35, 0], [0.8, -3.25, 0],
                       color=YELLOW, dash_length=0.07),
            Line([-0.8, -1.45, 0], [0.8, -1.45, 0],
                 color=YELLOW, stroke_width=3).add_tip(at_start=True).add_tip(at_start=False),
            Text("phase shift", font_size=20, color=YELLOW).move_to([0, -1.15, 0]),
        )
        contrast_guides = VGroup(
            DashedLine([-0.8, 1.65, 0], [-0.8, 0.75, 0],
                       color=GREY_B, dash_length=0.08, stroke_width=1),
            DashedLine([-0.8, -2.35, 0], [-0.8, -3.25, 0],
                       color=GREY_B, dash_length=0.08, stroke_width=1),
        )

        self.play(
            FadeOut(main_view_group),
            FadeIn(top_row["group"]),
            FadeIn(bottom_row["group"]),
            run_time=max(0.05, 0.80),
        )
        self.play(Create(bottom_phase_guide), run_time=max(0.05, 0.58))
        self.wait(max(0.05, 0.70))

        self.play(
            Indicate(top_row["trace1"], scale_factor=1.04, color=YELLOW),
            Indicate(top_row["trace2"], scale_factor=1.04, color=YELLOW),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 0.28))
        self.play(FadeIn(contrast_guides), run_time=max(0.05, 0.32))

        # ---------- beat 5: 15.10-19.10 ----------
        self.wait(max(0.05, 0.76))
        self.play(
            top_row["group"].animate.set_stroke(width=3),
            bottom_row["group"].animate.set_opacity(0.40),
            run_time=max(0.05, 0.46),
        )

        functional_label = Text("functional relationship", font_size=30,
                                weight=BOLD, color=YELLOW).move_to([0, 2.6, 0])
        functional_arrow_from_label = Arrow(
            top_row["label"].get_bottom(),
            functional_label.get_top() + UP * 0.05,
            color=WHITE, buff=0.05,
        )
        self.play(
            Create(functional_arrow_from_label),
            FadeIn(functional_label),
            run_time=max(0.05, 0.90),
        )
        self.play(
            Indicate(functional_label, scale_factor=1.06, color=YELLOW),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.38))

        top_relationship_arrow = Line(
            top_row["left_region"]["blob"].get_right(),
            top_row["right_region"]["blob"].get_left(),
            color=YELLOW, stroke_width=5,
        )
        top_relationship_arrow.add_tip(at_start=True)
        top_relationship_arrow.add_tip(at_start=False)
        self.play(Create(top_relationship_arrow), run_time=max(0.05, 0.35))
        start_pulse = top_row["left_region"]["blob"].get_right()
        end_pulse = top_row["right_region"]["blob"].get_left()
        p1 = Dot(start_pulse, radius=0.05, color=YELLOW)
        p2 = Dot(end_pulse, radius=0.05, color=YELLOW)
        self.add(p1, p2)
        self.play(
            p1.animate.move_to(end_pulse),
            p2.animate.move_to(start_pulse),
            run_time=max(0.05, 0.25),
        )
        self.remove(p1, p2)

        top_region_highlights = VGroup(
            SurroundingRectangle(top_row["left_region"]["blob"],
                                 color=WHITE, buff=0.08, stroke_width=2),
            SurroundingRectangle(top_row["right_region"]["blob"],
                                 color=WHITE, buff=0.08, stroke_width=2),
        )
        self.play(FadeIn(top_region_highlights), run_time=max(0.05, 0.30))
        self.play(
            Indicate(functional_label, scale_factor=1.05),
            Indicate(top_relationship_arrow, scale_factor=1.03, color=YELLOW),
            run_time=max(0.05, 0.10),
        )

        rows_comparison_group = VGroup(
            top_row["group"], bottom_row["group"], bottom_phase_guide,
            contrast_guides, functional_label, functional_arrow_from_label,
            top_relationship_arrow, top_region_highlights,
        )

        # ---------- beat 6: 19.10-24.04 ----------
        self.wait(max(0.05, 0.76))

        single_panel_bg = Rectangle(width=4.2, height=3.0,
                                    stroke_color=GREY_B, stroke_width=1.5,
                                    fill_color=GREY, fill_opacity=0.05).move_to([0, 0.4, 0])
        single_region = make_region(UP * 1.2, seed=51)
        local_activity_label = Text("local activity", font_size=24,
                                    color=WHITE, weight=BOLD).move_to([0, -1.0, 0])
        single_panel_group = VGroup(single_panel_bg, single_region["group"],
                                    local_activity_label)
        single_trace = make_trace(-0.5, phase=0.0, x_left=-4.5, x_right=4.5,
                                  amp=0.25, n_cycles=2.5)
        single_caption = Text("local neural activity", font_size=22,
                              color=WHITE).move_to([0, -1.5, 0])

        self.play(
            rows_comparison_group.animate.scale(0.55).to_edge(UP, buff=0.5).set_opacity(0.30),
            FadeIn(single_panel_group),
            run_time=max(0.05, 0.50),
        )
        self.play(
            Create(single_trace),
            FadeIn(single_caption),
            run_time=max(0.05, 0.50),
        )

        red_x1 = Line(single_panel_group.get_center() + LEFT * 0.6 + UP * 0.6,
                      single_panel_group.get_center() + RIGHT * 0.6 + DOWN * 0.6,
                      color=RED, stroke_width=10)
        red_x2 = Line(single_panel_group.get_center() + LEFT * 0.6 + DOWN * 0.6,
                      single_panel_group.get_center() + RIGHT * 0.6 + UP * 0.6,
                      color=RED, stroke_width=10)
        red_x = VGroup(red_x1, red_x2)
        cannot_text = Text("cannot be obtained from a single recording contact",
                           font_size=22, color=RED).move_to([0, -2.1, 0])
        self.play(FadeIn(red_x), FadeIn(cannot_text), run_time=max(0.05, 0.60))

        self.wait(max(0.05, 1.12))

        ghost_region = make_region(RIGHT * 2.8 + UP * 1.2, seed=52)
        ghost_region["group"].set_opacity(0.30)
        self.play(
            single_panel_group.animate.set_opacity(0.35).shift(UP * 0.1),
            FadeIn(ghost_region["group"]),
            run_time=max(0.05, 0.62),
        )
        self.wait(max(0.05, 0.20))
        self.play(
            single_panel_group.animate.scale(0.55).move_to(
                LEFT * 5.0 + UP * 2.8
            ).set_opacity(0.40),
            run_time=max(0.05, 0.54),
        )
        self.wait(max(0.05, 0.10))

        remnants_before_panels = VGroup(
            single_panel_group, single_trace, single_caption,
            red_x, cannot_text, ghost_region["group"],
        )

        # ---------- build three-panel progression ----------
        def build_left_panel(center):
            bg = Rectangle(width=3.6, height=3.4,
                           stroke_color=GREY_B, stroke_width=1.5,
                           fill_color=GREY, fill_opacity=0.05).move_to(center)
            region = make_small_region(center + UP * 0.75)
            trace = make_trace(center[1] - 0.35, phase=0.0,
                               x_left=center[0] - 1.3, x_right=center[0] + 1.3,
                               amp=0.15, n_cycles=2.5)
            label = Text("local activity", font_size=20, color=WHITE,
                         weight=BOLD).next_to(bg, DOWN, buff=0.15)
            return {"group": VGroup(bg, region["group"], trace, label),
                    "trace": trace, "tip": region["tip"], "label": label}

        def build_middle_panel(center):
            bg = Rectangle(width=3.6, height=3.4,
                           stroke_color=GREY_B, stroke_width=1.5,
                           fill_color=GREY, fill_opacity=0.05).move_to(center)
            left = make_small_region(center + LEFT * 1.1 + UP * 0.75,
                                     region_text="region 1", seed=32)
            right = make_small_region(center + RIGHT * 1.1 + UP * 0.75,
                                      region_text="region 2", seed=33)
            left_trace = make_trace(center[1] - 0.35, phase=0.0,
                                    x_left=center[0] - 1.5, x_right=center[0] + 1.5,
                                    amp=0.13, n_cycles=2.0)
            right_trace_offset = make_trace(center[1] - 1.0, phase=1.2,
                                            x_left=center[0] - 1.5, x_right=center[0] + 1.5,
                                            amp=0.13, n_cycles=2.0)
            right_trace_aligned = make_trace(center[1] - 1.0, phase=0.0,
                                             x_left=center[0] - 1.5, x_right=center[0] + 1.5,
                                             amp=0.13, n_cycles=2.0)
            arrow = Line(left["blob"].get_right(), right["blob"].get_left(),
                         color=WHITE, stroke_width=3)
            arrow.add_tip(at_start=True)
            arrow.add_tip(at_start=False)
            label = Text("relationships between populations", font_size=16,
                         color=WHITE, weight=BOLD)
            label.scale_to_fit_width(3.4).next_to(bg, DOWN, buff=0.18)
            group = VGroup(bg, left["group"], right["group"], left_trace,
                           right_trace_offset, arrow, label)
            return {
                "group": group,
                "left_trace": left_trace,
                "right_trace_offset": right_trace_offset,
                "right_trace_aligned": right_trace_aligned,
                "left_region": left,
                "right_region": right,
                "arrow": arrow,
                "label": label,
            }

        def build_right_panel(center):
            bg = Rectangle(width=3.6, height=3.4,
                           stroke_color=GREY_B, stroke_width=1.5,
                           fill_color=GREY, fill_opacity=0.05).move_to(center)
            cluster_a = Ellipse(width=1.5, height=1.0, color=ORANGE,
                                fill_color=ORANGE, fill_opacity=0.20).move_to(
                center + LEFT * 0.7 + UP * 0.5)
            cluster_b = Ellipse(width=1.5, height=1.0, color=TEAL,
                                fill_color=TEAL, fill_opacity=0.20).move_to(
                center + RIGHT * 0.7 + UP * 0.5)
            pos_a = [center + LEFT * 0.7 + UP * 0.5 + np.array([dx, dy, 0])
                     for dx, dy in [(-0.4, 0.2), (0.0, 0.3), (0.4, -0.2)]]
            pos_b = [center + RIGHT * 0.7 + UP * 0.5 + np.array([dx, dy, 0])
                     for dx, dy in [(-0.4, 0.2), (0.0, 0.3), (0.4, -0.2)]]
            neurons = VGroup(*[make_neuron(p) for p in pos_a + pos_b])
            connections = VGroup(
                Line(pos_a[0], pos_a[1], color=GREY_B, stroke_width=1),
                Line(pos_a[1], pos_a[2], color=GREY_B, stroke_width=1),
                Line(pos_b[0], pos_b[1], color=GREY_B, stroke_width=1),
                Line(pos_b[1], pos_b[2], color=GREY_B, stroke_width=1),
                Line(pos_a[1], pos_b[1], color=GREY_B, stroke_width=1),
            )
            network = VGroup(cluster_a, cluster_b, neurons, connections)
            label = Text("neural circuit analysis", font_size=18,
                         color=WHITE, weight=BOLD).next_to(bg, DOWN, buff=0.15)
            group = VGroup(bg, network, label)
            return {"group": group, "network": network,
                    "connections": connections, "neurons": neurons,
                    "label": label}

        left_panel = build_left_panel(np.array([-4.2, -0.1, 0]))
        middle_panel = build_middle_panel(np.array([0, -0.1, 0]))
        right_panel = build_right_panel(np.array([4.2, -0.1, 0]))
        three_panel_group = VGroup(left_panel["group"], middle_panel["group"],
                                   right_panel["group"])

        # ---------- beat 7: 24.04-29.14 ----------
        self.play(
            FadeOut(remnants_before_panels),
            FadeOut(rows_comparison_group),
            FadeIn(three_panel_group),
            run_time=max(0.05, 0.90),
        )
        self.wait(max(0.05, 0.80))

        mid_dashed_outline = SurroundingRectangle(
            middle_panel["group"], color=WHITE, stroke_width=1.5, buff=0.08
        )
        right_dashed_outline = SurroundingRectangle(
            right_panel["group"], color=WHITE, stroke_width=1.5, buff=0.08
        )
        self.play(
            FadeIn(mid_dashed_outline),
            FadeIn(right_dashed_outline),
            run_time=max(0.05, 0.30),
        )

        mid_tips = VGroup(middle_panel["left_region"]["tip"],
                          middle_panel["right_region"]["tip"])
        self.play(
            left_panel["tip"].animate.scale(1.25).set_color(YELLOW),
            mid_tips.animate.scale(1.25).set_color(YELLOW),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 2.80))

        # ---------- beat 8: 29.14-33.40 ----------
        self.play(
            Indicate(left_panel["trace"], scale_factor=1.05, color=YELLOW),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.36))

        self.play(
            middle_panel["arrow"].animate.set_color(YELLOW).set_stroke(width=6),
            run_time=max(0.05, 0.35),
        )
        mid_arrow_start = middle_panel["left_region"]["blob"].get_right()
        mid_arrow_end = middle_panel["right_region"]["blob"].get_left()
        mp1 = Dot(mid_arrow_start, radius=0.04, color=YELLOW)
        mp2 = Dot(mid_arrow_end, radius=0.04, color=YELLOW)
        self.add(mp1, mp2)
        self.play(
            mp1.animate.move_to(mid_arrow_end),
            mp2.animate.move_to(mid_arrow_start),
            run_time=max(0.05, 0.35),
        )
        self.remove(mp1, mp2)
        self.play(
            middle_panel["arrow"].animate.set_color(YELLOW).set_stroke(width=6),
            run_time=max(0.05, 0.10),
        )
        self.wait(max(0.05, 0.28))

        middle_panel_y_lo = -0.30
        middle_panel_y_hi = -1.10
        mid_guide_lines = VGroup(
            DashedLine([0.375, middle_panel_y_lo, 0], [0.375, middle_panel_y_hi, 0],
                       color=WHITE, dash_length=0.06),
            DashedLine([1.875, middle_panel_y_lo, 0], [1.875, middle_panel_y_hi, 0],
                       color=WHITE, dash_length=0.06),
        )
        self.play(
            Transform(middle_panel["right_trace_offset"],
                      middle_panel["right_trace_aligned"]),
            Create(mid_guide_lines),
            run_time=max(0.05, 0.58),
        )

        mid_halo1 = Ellipse(width=0.9, height=0.4, color=ORANGE,
                            fill_color=ORANGE, fill_opacity=0.55,
                            stroke_width=0).move_to(
            middle_panel["left_region"]["region_label"].get_center())
        mid_halo2 = Ellipse(width=0.9, height=0.4, color=TEAL,
                            fill_color=TEAL, fill_opacity=0.55,
                            stroke_width=0).move_to(
            middle_panel["right_region"]["region_label"].get_center())
        self.play(FadeIn(mid_halo1), FadeIn(mid_halo2), run_time=max(0.05, 0.58))

        self.wait(max(0.05, 0.20))

        self.play(
            right_panel["network"].animate.set_stroke(color=WHITE, width=2),
            run_time=max(0.05, 0.22),
        )

        pulse_connections = right_panel["connections"][:3]
        network_pulses = VGroup(*[
            Dot(line.get_start(), radius=0.04, color=YELLOW)
            for line in pulse_connections
        ])
        self.add(network_pulses)
        for dot, line in zip(network_pulses, pulse_connections):
            dot.move_to(line.get_start())
        self.play(
            *[dot.animate.move_to(line.get_end())
              for dot, line in zip(network_pulses, pulse_connections)],
            run_time=max(0.05, 0.34),
        )
        self.remove(network_pulses)

        unifying_highlight = SurroundingRectangle(
            three_panel_group, color=YELLOW, stroke_width=2, buff=0.20,
            corner_radius=0.1,
        )
        self.play(
            right_panel["label"].animate.set_color(YELLOW).scale(1.1),
            FadeIn(unifying_highlight),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 0.10))

        # ---------- beat 9: 33.40-34.33 ----------
        top_caption = Text("multiple electrodes enable circuit analysis",
                           font_size=22, color=WHITE, weight=BOLD)
        top_caption.to_edge(UP, buff=0.25)
        self.play(FadeIn(top_caption), run_time=max(0.05, 0.10))

        final_visible = VGroup(
            three_panel_group,
            unifying_highlight,
            mid_guide_lines,
            mid_halo1,
            mid_halo2,
            top_caption,
            previous_final,
        )
        self.play(FadeOut(final_visible), run_time=max(0.05, 0.83))