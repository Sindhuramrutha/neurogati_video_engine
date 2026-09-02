ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene15(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------------- helper: EEG-like waveform ----------------
        def make_wave(signal, width=3.0, height=0.55, color=YELLOW, stroke_width=2.0, num_points=180):
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            u = np.linspace(-1, 1, num_points)
            x = u * width / 2.0
            y = signal(u) * height / 2.0
            y = np.clip(y, -height, height)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        # ----- waveform patterns used in top-left and central stack -----
        def sig_irregular(u):
            y = np.zeros_like(u)
            y += 0.9 * np.exp(-((u + 0.55) / 0.12) ** 2) * np.sin(2 * np.pi * 3.2 * (u + 0.55))
            y += 0.7 * np.exp(-((u + 0.08) / 0.10) ** 2) * np.sin(2 * np.pi * 5.1 * (u + 0.08))
            y += 0.8 * np.exp(-((u + 0.72) / 0.09) ** 2) * np.sin(2 * np.pi * 4.0 * (u + 0.72))
            return y

        def sig_fragmented(u):
            y = np.zeros_like(u)
            y += 0.55 * np.exp(-((u + 0.65) / 0.16) ** 2) * np.sin(2 * np.pi * 6.0 * (u + 0.65))
            y += 0.45 * np.exp(-((u + 0.20) / 0.13) ** 2) * np.sin(2 * np.pi * 8.0 * (u + 0.20))
            y += 0.6 * np.exp(-((u - 0.25) / 0.14) ** 2) * np.sin(2 * np.pi * 5.5 * (u - 0.25))
            y += 0.45 * np.exp(-((u - 0.70) / 0.12) ** 2) * np.sin(2 * np.pi * 7.0 * (u - 0.70))
            return y

        def sig_narcolepsy(u):
            slow = 0.85 * np.sin(2 * np.pi * 1.4 * u) * (u < 0.10)
            fast = 0.25 * np.sin(2 * np.pi * 13.0 * u) * (u >= 0.10)
            return slow + fast

        def sig_variant1(u):
            return np.where(
                np.abs(u + 0.4) < 0.08,
                0.9 * np.sin(2 * np.pi * 9 * (u + 0.4)),
                0.1 * np.sin(2 * np.pi * 2 * u),
            )

        def sig_variant2(u):
            return 0.65 * np.sin(2 * np.pi * 12 * u) * np.exp(-np.abs(u - 0.0) / 0.4) + 0.15 * np.sin(2 * np.pi * 3 * u)

        def sig_variant3(u):
            return 0.8 * np.sin(2 * np.pi * 2.5 * u) * (u < -0.1) + 0.25 * np.sin(2 * np.pi * 15 * u) * (u >= -0.1)

        def sig_slow_regular(u):
            return 0.8 * np.sin(2 * np.pi * 1.3 * u)

        def sig_age45(u):
            return 0.6 * np.sin(2 * np.pi * 1.15 * u) + 0.12 * np.sin(2 * np.pi * 5.0 * u)

        def sig_age70(u):
            return 0.45 * np.sin(2 * np.pi * 0.95 * u) + 0.22 * np.sin(2 * np.pi * 7.0 * u)

        def sig_disease(u):
            return 0.7 * np.sin(2 * np.pi * 4.2 * u + 1.5 * np.sin(2 * np.pi * 0.8 * u))

        def sig_medication(u):
            return 0.28 * np.sin(2 * np.pi * 0.7 * u) + 0.05 * np.sin(2 * np.pi * 10.0 * u)

        def make_previous_composition():
            left_panel = RoundedRectangle(
                width=3.2, height=1.8, fill_color=BLACK, fill_opacity=0.5,
                stroke_color=BLUE, stroke_width=1
            ).move_to(LEFT * 4 + UP * 0.6)
            trace = make_wave(sig_irregular, width=2.8, height=0.5, color=YELLOW).move_to(left_panel.get_center())
            block1 = RoundedRectangle(
                width=1.5, height=0.8, fill_color=ORANGE, fill_opacity=0.3,
                stroke_color=YELLOW, stroke_width=1
            ).move_to(ORIGIN)
            block2 = RoundedRectangle(
                width=1.5, height=0.8, fill_color=PURPLE, fill_opacity=0.3,
                stroke_color=YELLOW, stroke_width=1
            ).move_to(RIGHT * 2.2 + DOWN * 0.6)
            plot = Rectangle(
                width=1.6, height=1.2, fill_color=BLACK, fill_opacity=0.5,
                stroke_color=TEAL, stroke_width=1
            ).move_to(RIGHT * 2 + UP * 1.2)
            stage_labels = VGroup(*[
                Text(s, font_size=14, color=WHITE) for s in ["Wake", "N1", "N2", "N3", "REM"]
            ]).arrange(RIGHT, buff=0.25).move_to(RIGHT * 2 + DOWN * 2.0)
            return VGroup(left_panel, trace, block1, block2, plot, stage_labels)

        # ---------------- beat 1: previous scene composition fades out ----------------
        prev_comp = make_previous_composition()
        self.add(prev_comp)

        # ----- icons drawn from primitives -----
        def build_stethoscope(color=BLUE):
            chest = Circle(radius=0.18, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            ear_l = Circle(radius=0.08, fill_color=color, fill_opacity=1, stroke_width=0).move_to(LEFT * 0.35 + UP * 0.4)
            ear_r = Circle(radius=0.08, fill_color=color, fill_opacity=1, stroke_width=0).move_to(RIGHT * 0.35 + UP * 0.4)
            tube_l = Line(ear_l.get_bottom(), chest.get_top(), color=color, stroke_width=3)
            tube_r = Line(ear_r.get_bottom(), chest.get_top(), color=color, stroke_width=3)
            return VGroup(chest, ear_l, ear_r, tube_l, tube_r)

        def build_moon():
            moon = Text("☾", font_size=30, color=WHITE)
            star1 = Dot(radius=0.05, color=GOLD, fill_opacity=1).move_to(RIGHT * 0.45 + UP * 0.3)
            star2 = Dot(radius=0.04, color=WHITE, fill_opacity=1).move_to(LEFT * 0.45 + UP * 0.5)
            return VGroup(moon, star1, star2)

        def build_smartwatch(color=TEAL):
            face = RoundedRectangle(
                width=0.5, height=0.65, corner_radius=0.1,
                fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=1
            )
            screen = Rectangle(
                width=0.34, height=0.43, fill_color=BLACK, fill_opacity=1, stroke_width=0
            ).move_to(face)
            top_strap = Line(face.get_top(), face.get_top() + UP * 0.3, color=GREY_B, stroke_width=3)
            bottom_strap = Line(face.get_bottom(), face.get_bottom() + DOWN * 0.3, color=GREY_B, stroke_width=3)
            return VGroup(top_strap, face, screen, bottom_strap)

        # ----- blank 2x2 panel grid -----
        def make_panel(icon_mob):
            rect = RoundedRectangle(
                width=5.8, height=3.4, corner_radius=0.22,
                fill_color=BLACK, fill_opacity=0.45,
                stroke_color=WHITE, stroke_width=1.5
            )
            underline = Line(LEFT * 1.7, RIGHT * 1.7, color=GREY, stroke_width=2).move_to(DOWN * 0.25)
            icon_mob.scale_to_fit_height(0.55)
            icon_mob.move_to(UP * 0.7)
            panel = VGroup(rect, icon_mob, underline)
            return panel, rect, icon_mob, underline

        stethoscope_icon = build_stethoscope()
        moon_icon = build_moon()
        brain_icon_top = SVGMobject(
            ASSET_PATHS["brain"], height=0.7,
            fill_color=PURPLE, fill_opacity=1, stroke_color=WHITE, stroke_width=1
        )
        watch_icon = build_smartwatch()

        panel_tl, rect_tl, icon_tl, underline_tl = make_panel(stethoscope_icon)
        panel_tr, rect_tr, icon_tr, underline_tr = make_panel(moon_icon)
        panel_bl, rect_bl, icon_bl, underline_bl = make_panel(brain_icon_top)
        panel_br, rect_br, icon_br, underline_br = make_panel(watch_icon)

        panels = VGroup(panel_tl, panel_tr, panel_bl, panel_br).arrange_in_grid(rows=2, cols=2, buff=0.55)
        panels.move_to(ORIGIN)

        self.play(FadeOut(prev_comp), run_time=max(0.05, 1.3))
        self.play(GrowFromCenter(panels), run_time=max(0.05, 2.4))
        self.wait(max(0.05, 1.28))

        # ---------------- beat 2: sleep disorder diagnosis panel (top-left) ----------------
        label_tl = Text("Sleep Disorder Diagnosis", font_size=19, color=WHITE, weight="BOLD")
        label_tl.scale_to_fit_width(3.9)
        label_tl.move_to(rect_tl.get_center() + UP * 0.15)
        label_tl.set_opacity(0)
        panel_tl.add(label_tl)

        insomnia_word = Text("Insomnia", font_size=14, color=GREY_B)
        sep1 = Text(" · ", font_size=14, color=GREY)
        narcolepsy_word = Text("Narcolepsy", font_size=14, color=GREY_B)
        sep2 = Text(" · ", font_size=14, color=GREY)
        other_word = Text("Other sleep disorders", font_size=14, color=GREY_B)
        sub_tl = VGroup(insomnia_word, sep1, narcolepsy_word, sep2, other_word).arrange(RIGHT, buff=0.1)
        sub_tl.scale_to_fit_width(4.6)
        sub_tl.move_to(rect_tl.get_center() + DOWN * 0.45)
        sub_tl.set_opacity(0)
        panel_tl.add(sub_tl)

        alarm_accent = VGroup(
            Circle(radius=0.09, fill_color=GOLD, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            .move_to(icon_tl.get_center() + RIGHT * 0.55 + DOWN * 0.35)
        )
        alarm_accent.set_opacity(0)
        panel_tl.add(alarm_accent)

        self.play(FadeIn(label_tl), FadeIn(sub_tl), FadeIn(alarm_accent), run_time=max(0.05, 1.52))

        # ---------------- beat 3: abnormal waveform + insomnia pulse ----------------
        self.wait(max(0.05, 0.36))

        main_wave_pos = rect_tl.get_center() + DOWN * 0.95
        wave_tl_initial = make_wave(sig_irregular, width=3.5, height=0.55, color=TEAL, stroke_width=2.0)
        wave_tl_initial.move_to(main_wave_pos)
        wave_tl_initial.set_opacity(0)
        panel_tl.add(wave_tl_initial)

        wave_tl_fragmented = make_wave(sig_fragmented, width=3.5, height=0.55, color=TEAL, stroke_width=2.0)
        wave_tl_fragmented.move_to(wave_tl_initial.get_center())

        self.play(FadeIn(wave_tl_initial), run_time=max(0.05, 0.7))
        self.play(Indicate(insomnia_word, scale_factor=1.25, color=YELLOW), run_time=max(0.05, 0.5))
        self.play(Transform(wave_tl_initial, wave_tl_fragmented), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.98))

        # ---------------- beat 4: narcolepsy pulse + small variant waves ----------------
        self.wait(max(0.05, 0.60))

        wave_tl_narcolepsy = make_wave(sig_narcolepsy, width=3.5, height=0.55, color=TEAL, stroke_width=2.0)
        wave_tl_narcolepsy.move_to(wave_tl_initial.get_center())

        self.play(Indicate(narcolepsy_word, scale_factor=1.25, color=YELLOW), run_time=max(0.05, 0.5))
        self.play(Transform(wave_tl_initial, wave_tl_narcolepsy), run_time=max(0.05, 0.9))

        variant_signals = [sig_variant1, sig_variant2, sig_variant3]
        variant_waves = []
        variant_xs = [-1.7, 0, 1.7]
        base_y = rect_tl.get_center()[1] - 1.35
        per_variant = 2.34 / 3.0

        for idx, sig in enumerate(variant_signals):
            v = make_wave(sig, width=1.05, height=0.22, color=MAROON, stroke_width=1.8)
            v.move_to(np.array([rect_tl.get_center()[0] + variant_xs[idx], base_y, 0]))
            v.set_opacity(0)
            panel_tl.add(v)
            variant_waves.append(v)

        for v in variant_waves:
            self.play(FadeIn(v), run_time=max(0.05, per_variant * 0.3))
            self.wait(max(0.05, per_variant * 0.4))
            self.play(FadeOut(v), run_time=max(0.05, per_variant * 0.3))

        # ---------------- beat 5: sleep quality assessment panel (top-right) ----------------
        self.wait(max(0.05, 1.14))

        label_tr = Text("Sleep Quality Assessment", font_size=19, color=WHITE, weight="BOLD")
        label_tr.scale_to_fit_width(3.9)
        label_tr.move_to(rect_tr.get_center() + UP * 0.15)
        label_tr.set_opacity(0)
        panel_tr.add(label_tr)

        scale_bar_center = rect_tr.get_center() + DOWN * 0.55
        bar_line = Line(LEFT * 1.6, RIGHT * 1.6, color=WHITE, stroke_width=3).move_to(scale_bar_center)
        ticks = VGroup()
        tick_heights = [0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14]
        for i, tick_h in enumerate(tick_heights):
            x = bar_line.get_start()[0] + (i / (len(tick_heights) - 1)) * bar_line.get_width()
            tick = Line(
                np.array([x, scale_bar_center[1] - tick_h, 0]),
                np.array([x, scale_bar_center[1] + tick_h, 0]),
                color=WHITE, stroke_width=2
            )
            ticks.add(tick)
        scale_bar = VGroup(bar_line, ticks)
        scale_bar.set_opacity(0)
        panel_tr.add(scale_bar)

        self.play(FadeIn(label_tr), icon_tr.animate.set_color(GOLD), run_time=max(0.05, 0.7))
        self.play(FadeIn(scale_bar), run_time=max(0.05, 0.78))

        # ---------------- beat 6: age/disease/medication waveform strips ----------------
        self.wait(max(0.05, 0.52))

        def make_strip(strip_label, signal, color):
            lab = Text(strip_label, font_size=11, color=WHITE)
            wv = make_wave(signal, width=3.0, height=0.18, color=color, stroke_width=1.5)
            strip = VGroup(lab, wv).arrange(DOWN, buff=0.03)
            return strip

        strip_data = []
        strip_specs = [
            ("Age 20", sig_slow_regular, YELLOW),
            ("Age 45", sig_age45, TEAL),
            ("Age 70", sig_age70, ORANGE),
            ("Disease", sig_disease, RED),
            ("Medication", sig_medication, PURPLE),
        ]
        for strip_label, signal, color in strip_specs:
            strip_data.append({"strip": make_strip(strip_label, signal, color)})

        strips_group = VGroup(*[d["strip"] for d in strip_data]).arrange(DOWN, buff=0.1)
        strips_group.scale_to_fit_height(1.45)
        strips_group.move_to(rect_tr.get_center() + DOWN * 0.8)
        for d in strip_data[3:]:
            d["strip"].set_opacity(0)
        panel_tr.add(strips_group)

        self.play(*[FadeIn(d["strip"]) for d in strip_data[:3]], run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.5))
        self.play(Indicate(strip_data[0]["strip"], scale_factor=1.05, color=YELLOW), run_time=max(0.05, 0.6))
        self.play(Indicate(strip_data[1]["strip"], scale_factor=1.05, color=TEAL), run_time=max(0.05, 0.6))
        self.play(Indicate(strip_data[2]["strip"], scale_factor=1.05, color=ORANGE), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.7))
        self.play(FadeIn(strip_data[3]["strip"]), run_time=max(0.05, 1.0))
        self.play(FadeIn(strip_data[4]["strip"]), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.28))

        # ---------------- beat 7: neuroscience research panel (bottom-left) ----------------
        self.wait(max(0.05, 1.80))

        label_bl = Text("Neuroscience Research", font_size=19, color=WHITE, weight="BOLD")
        label_bl.scale_to_fit_width(3.9)
        label_bl.move_to(rect_bl.get_center() + UP * 0.15)
        label_bl.set_opacity(0)
        panel_bl.add(label_bl)

        brain_schematic = SVGMobject(
            ASSET_PATHS["brain"], height=1.3,
            fill_color=PURPLE, fill_opacity=1, stroke_color=WHITE, stroke_width=1
        ).move_to(rect_bl.get_center() + DOWN * 0.55)

        node_positions = [
            LEFT * 0.45 + UP * 0.20,
            RIGHT * 0.40 + UP * 0.15,
            LEFT * 0.55 + DOWN * 0.20,
            RIGHT * 0.50 + DOWN * 0.10,
        ]
        node_colors = [PURPLE, BLUE, TEAL, ORANGE]
        node_dots = VGroup()
        for pos, color in zip(node_positions, node_colors):
            dot = Dot(radius=0.08, color=color, fill_opacity=1, stroke_width=0)
            dot.move_to(brain_schematic.get_center() + pos)
            node_dots.add(dot)

        brain_schematic_group = VGroup(brain_schematic, node_dots)
        brain_schematic_group.set_opacity(0)
        panel_bl.add(brain_schematic_group)

        self.play(FadeIn(label_bl), icon_bl.animate.set_color(PURPLE), run_time=max(0.05, 0.8))
        self.play(FadeIn(brain_schematic_group), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.82))

        # ---------------- beat 8: four research sub-icons around brain schematic ----------------
        self.wait(max(0.05, 1.00))

        memory_icon = SVGMobject(
            ASSET_PATHS["arrow_repeat"], height=0.35,
            fill_color=YELLOW, fill_opacity=1, stroke_color=WHITE, stroke_width=1
        )

        def build_book_icon(color=GREEN):
            left_page = Rectangle(width=0.22, height=0.35, fill_color=color, fill_opacity=1,
                                  stroke_color=WHITE, stroke_width=1).move_to(LEFT * 0.12)
            right_page = Rectangle(width=0.22, height=0.35, fill_color=color, fill_opacity=1,
                                   stroke_color=WHITE, stroke_width=1).move_to(RIGHT * 0.12)
            spine = Line(left_page.get_top(), left_page.get_bottom(), color=WHITE, stroke_width=2)
            return VGroup(left_page, right_page, spine)

        def build_branch_icon(color=ORANGE):
            trunk = Line(DOWN * 0.3, UP * 0.1, color=color, stroke_width=3)
            b1 = Line(trunk.get_top(), LEFT * 0.25 + UP * 0.35, color=color, stroke_width=2)
            b2 = Line(trunk.get_top(), RIGHT * 0.25 + UP * 0.35, color=color, stroke_width=2)
            dots = VGroup(*[
                Dot(radius=0.04, color=color, fill_opacity=1, stroke_width=0).move_to(p)
                for p in [LEFT * 0.25 + UP * 0.35, RIGHT * 0.25 + UP * 0.35, UP * 0.1]
            ])
            return VGroup(trunk, b1, b2, dots)

        learning_icon = build_book_icon()
        development_icon = build_branch_icon()
        cognitive_icon = SVGMobject(
            ASSET_PATHS["gear"], height=0.35,
            fill_color=BLUE, fill_opacity=1, stroke_color=WHITE, stroke_width=1
        )

        annotation_infos = [
            (memory_icon, "Memory consolidation", brain_schematic.get_corner(UL) + UP * 0.25 + LEFT * 0.4, node_dots[0]),
            (learning_icon, "Learning", brain_schematic.get_corner(UR) + UP * 0.25 + RIGHT * 0.4, node_dots[1]),
            (development_icon, "Brain development", brain_schematic.get_corner(DL) + DOWN * 0.25 + LEFT * 0.4, node_dots[2]),
            (cognitive_icon, "Cognitive function", brain_schematic.get_corner(DR) + DOWN * 0.25 + RIGHT * 0.4, node_dots[3]),
        ]

        annotation_groups = []
        for icon, text, pos, node in annotation_infos:
            icon_text = VGroup(icon, Text(text, font_size=10, color=WHITE)).arrange(DOWN, buff=0.05)
            icon_text.scale_to_fit_width(1.05)
            icon_text.move_to(pos)
            icon_text.set_opacity(0)
            line = Line(node.get_center(), icon_text.get_left(), color=GREY, stroke_width=1.5)
            line.set_opacity(0)
            panel_bl.add(icon_text, line)
            annotation_groups.append((icon_text, line))

        per_annotation = 5.46 / 4.0
        for icon_text, line in annotation_groups:
            self.play(FadeIn(icon_text), Create(line), run_time=max(0.05, per_annotation * 0.62))
            self.wait(max(0.05, per_annotation * 0.38))

        # ---------------- beat 9: automated sleep monitoring panel (bottom-right) ----------------
        self.wait(max(0.05, 0.80))

        label_br = Text("Automated Sleep Monitoring", font_size=17, color=WHITE, weight="BOLD")
        label_br.scale_to_fit_width(3.9)
        label_br.move_to(rect_br.get_center() + UP * 0.15)
        label_br.set_opacity(0)
        panel_br.add(label_br)

        left_device = build_smartwatch(color=TEAL).scale_to_fit_height(0.65)
        left_device.move_to(rect_br.get_center() + LEFT * 1.6 + DOWN * 0.6)
        left_device.set_opacity(0)
        panel_br.add(left_device)

        def build_headbox():
            box = Rectangle(width=0.75, height=0.55, fill_color=ORANGE, fill_opacity=0.9,
                            stroke_color=WHITE, stroke_width=1)
            ports = VGroup(*[
                Circle(radius=0.05, fill_color=WHITE, fill_opacity=1, stroke_width=0)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.08).move_to(box.get_center())
            leads = VGroup(*[
                Line(port.get_center() + LEFT * 0.15, port.get_center() + LEFT * 0.4, color=GREY_B, stroke_width=1)
                for port in ports
            ])
            return VGroup(box, ports, leads)

        headbox = build_headbox().scale_to_fit_height(0.65)
        headbox.move_to(rect_br.get_center() + RIGHT * 1.6 + DOWN * 0.6)
        headbox.set_opacity(0)
        panel_br.add(headbox)

        flow_wave = make_wave(lambda u: 0.5 * np.sin(2 * np.pi * 6 * u), width=1.0, height=0.25,
                              color=YELLOW, stroke_width=2)
        flow_wave.move_to(rect_br.get_center() + UP * 0.3)
        flow_wave.set_opacity(0)
        panel_br.add(flow_wave)

        flow_block = RoundedRectangle(
            width=1.8, height=1.1, corner_radius=0.12,
            fill_color=BLUE, fill_opacity=0.4, stroke_color=YELLOW, stroke_width=1.5
        ).move_to(rect_br.get_center() + DOWN * 0.6)

        def build_small_node_graph():
            root = Circle(radius=0.07, fill_color=BLUE, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            root.move_to(UP * 0.18)
            left_child = Circle(radius=0.07, fill_color=TEAL, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            left_child.move_to(DOWN * 0.12 + LEFT * 0.22)
            right_child = Circle(radius=0.07, fill_color=GREEN, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            right_child.move_to(DOWN * 0.12 + RIGHT * 0.22)
            e1 = Line(root.get_bottom(), left_child.get_top(), color=WHITE, stroke_width=1.5)
            e2 = Line(root.get_bottom(), right_child.get_top(), color=WHITE, stroke_width=1.5)
            return VGroup(root, left_child, right_child, e1, e2)

        flow_block_content = VGroup(
            Text("Signal Processing", font_size=10, color=WHITE),
            build_small_node_graph()
        ).arrange(DOWN, buff=0.1).move_to(flow_block)
        flow_block_group = VGroup(flow_block, flow_block_content)
        flow_arrow = Line(flow_wave.get_bottom(), flow_block.get_top(), color=WHITE, stroke_width=2)
        flow_block_group.set_opacity(0)
        flow_arrow.set_opacity(0)
        panel_br.add(flow_block_group, flow_arrow)

        stage_names = ["Wake", "N1", "N2", "N3", "REM"]
        stage_labels_group = VGroup(*[
            Text(name, font_size=11, color=GREY) for name in stage_names
        ]).arrange(RIGHT, buff=0.2)
        stage_labels_group.scale_to_fit_width(3.4)
        stage_labels_group.move_to(flow_block.get_bottom() + DOWN * 0.45)
        stage_labels_group.set_opacity(0)
        panel_br.add(stage_labels_group)

        self.play(FadeIn(label_br), icon_br.animate.set_color(TEAL), run_time=max(0.05, 0.8))
        self.play(FadeIn(left_device), FadeIn(headbox), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.2))
        self.play(FadeIn(flow_block_group), FadeIn(flow_wave), FadeIn(flow_arrow), run_time=max(0.05, 2.5))
        self.wait(max(0.05, 0.2))
        self.play(stage_labels_group.animate.set_opacity(0.4), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.2))

        per_stage = 3.70 / 5.0
        for i in range(5):
            anims = [stage_labels_group[i].animate.set_color(YELLOW).scale(1.2)]
            if i > 0:
                anims.append(stage_labels_group[i - 1].animate.set_color(GREY).scale(1 / 1.2))
            self.play(*anims, run_time=max(0.05, per_stage * 0.6))
            self.wait(max(0.05, per_stage * 0.4))

        # ---------------- beat 10: grid shifts up, advantages checklist begins ----------------
        self.wait(max(0.05, 1.52))

        self.play(panels.animate.scale(0.72).move_to(UP * 0.9), run_time=max(0.05, 1.1))

        checklist_title = Text("EEG Advantages for Sleep Analysis", font_size=18, color=WHITE, weight="BOLD")

        def make_check_row(*text_parts):
            check = Text("✓", font_size=22, color=GREEN)
            text_group = VGroup(*text_parts).arrange(RIGHT, buff=0.08)
            row = VGroup(check, text_group).arrange(RIGHT, buff=0.18, aligned_edge=LEFT)
            return row, text_group

        row1, _ = make_check_row(Text("Directly measures brain activity", font_size=13, color=WHITE))
        row2, _ = make_check_row(Text("Excellent temporal resolution", font_size=13, color=WHITE))
        row3, _ = make_check_row(Text("Clearly distinguishes sleep stages", font_size=13, color=WHITE))
        row4, _ = make_check_row(Text("Supports manual and automated scoring", font_size=13, color=WHITE))

        eog_word = Text("EOG", font_size=13, color=WHITE)
        emg_word = Text("EMG", font_size=13, color=WHITE)
        row5, row5_text_group = make_check_row(
            Text("Combines with ", font_size=13, color=WHITE),
            eog_word,
            Text(" and ", font_size=13, color=WHITE),
            emg_word,
            Text(" in polysomnography.", font_size=13, color=WHITE),
        )

        checklist_rows = VGroup(checklist_title, row1, row2, row3, row4, row5)
        checklist_rows.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        checklist_rows.move_to(np.array([-3.4, -2.35, 0]))

        checklist_title.set_opacity(0)
        for row in [row1, row2, row3, row4, row5]:
            row.set_opacity(0)
        self.add(checklist_rows)

        self.play(FadeIn(checklist_title), run_time=max(0.05, 0.6))
        self.play(FadeIn(row1), run_time=max(0.05, 1.4))
        self.play(FadeIn(row2), run_time=max(0.05, 1.4))
        self.play(FadeIn(row3), run_time=max(0.05, 1.4))

        # ---------------- beat 11: remaining checklist rows + EOG/EMG highlight ----------------
        self.wait(max(0.05, 5.08))

        self.play(FadeIn(row4), run_time=max(0.05, 1.2))
        self.play(FadeIn(row5), run_time=max(0.05, 1.2))
        self.play(Indicate(eog_word, scale_factor=1.2, color=YELLOW), run_time=max(0.05, 1.0))
        self.play(Indicate(emg_word, scale_factor=1.2, color=YELLOW), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 3.66))

        # ---------------- beat 12: polysomnography diagram ----------------
        def build_psg_diagram():
            bed = RoundedRectangle(
                width=3.0, height=0.5, corner_radius=0.1,
                fill_color=GREY_B, fill_opacity=0.7, stroke_color=WHITE, stroke_width=1
            ).shift(DOWN * 0.6)
            body = Rectangle(
                width=2.6, height=0.65, fill_color=BLUE, fill_opacity=0.4,
                stroke_color=WHITE, stroke_width=1
            ).shift(DOWN * 0.15)
            head = Circle(radius=0.25, fill_color=PINK, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            head.shift(LEFT * 1.0 + UP * 0.1)

            eeg_dot1 = Dot(point=head.get_center() + UP * 0.25 + LEFT * 0.1, radius=0.05, color=YELLOW)
            eeg_dot2 = Dot(point=head.get_center() + UP * 0.1 + RIGHT * 0.20, radius=0.05, color=YELLOW)
            eog_dot_left = Dot(point=head.get_center() + RIGHT * 0.28 + UP * 0.05, radius=0.05, color=TEAL)
            eog_dot_right = Dot(point=head.get_center() + RIGHT * 0.38 + UP * 0.0, radius=0.05, color=TEAL)
            emg_dot = Dot(point=body.get_center() + DOWN * 0.2 + RIGHT * 0.5, radius=0.05, color=PURPLE)

            eeg_label = Text("EEG", font_size=10, color=YELLOW).next_to(eeg_dot1, UP, buff=0.08)
            eog_label = Text("EOG", font_size=10, color=TEAL).next_to(eog_dot_left, UP, buff=0.08)
            emg_label = Text("EMG", font_size=10, color=PURPLE).next_to(emg_dot, DOWN, buff=0.08)

            rec_box = RoundedRectangle(
                width=1.4, height=1.0, corner_radius=0.12,
                fill_color=GREY_B, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1
            ).shift(RIGHT * 1.6 + UP * 0.0)
            monitor = Rectangle(
                width=1.1, height=0.65,
                fill_color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=1
            ).move_to(rec_box)

            trace_eeg_psg = make_wave(lambda u: 0.5 * np.sin(2 * np.pi * 1.5 * u),
                                      width=1.0, height=0.15, color=YELLOW, stroke_width=1.8)
            trace_eeg_psg.move_to(monitor.get_top() + DOWN * 0.22)
            trace_eog_psg = make_wave(sig_variant2, width=1.0, height=0.15, color=TEAL, stroke_width=1.8)
            trace_eog_psg.move_to(monitor.get_top() + DOWN * 0.42)
            trace_emg_psg = make_wave(lambda u: 0.35 * np.sin(2 * np.pi * 10 * u),
                                      width=1.0, height=0.15, color=PURPLE, stroke_width=1.8)
            trace_emg_psg.move_to(monitor.get_top() + DOWN * 0.62)

            trace_labels = VGroup(
                Text("EEG", font_size=9, color=YELLOW).next_to(trace_eeg_psg, RIGHT, buff=0.05),
                Text("EOG", font_size=9, color=TEAL).next_to(trace_eog_psg, RIGHT, buff=0.05),
                Text("EMG", font_size=9, color=PURPLE).next_to(trace_emg_psg, RIGHT, buff=0.05),
            )

            lead_lines = VGroup(
                Line(eeg_dot1.get_center(), rec_box.get_left(), color=GREY, stroke_width=1),
                Line(eog_dot_left.get_center(), rec_box.get_left(), color=GREY, stroke_width=1),
                Line(emg_dot.get_center(), rec_box.get_left(), color=GREY, stroke_width=1),
            )

            return VGroup(
                bed, body, head,
                eeg_dot1, eeg_dot2, eog_dot_left, eog_dot_right, emg_dot,
                eeg_label, eog_label, emg_label,
                rec_box, monitor,
                trace_eeg_psg, trace_eog_psg, trace_emg_psg,
                trace_labels, lead_lines
            ), trace_eeg_psg

        psg_diagram, trace_eeg_psg = build_psg_diagram()
        psg_diagram.scale_to_fit_width(4.2)
        psg_diagram.move_to(np.array([3.6, -2.2, 0]))
        psg_diagram.set_opacity(0)
        self.add(psg_diagram)

        self.play(FadeIn(psg_diagram), run_time=max(0.05, 1.4))

        # ---------------- beat 13: EEG trace enlarges, ghost traces fragment and fade ----------------
        self.wait(max(0.05, 0.90))

        enlarged_eeg = trace_eeg_psg.copy()
        enlarged_eeg.move_to(ORIGIN)
        enlarged_eeg.scale(2.0)
        enlarged_eeg.set_opacity(1)

        self.play(FadeIn(enlarged_eeg), psg_diagram.animate.set_opacity(0.2), run_time=max(0.05, 1.2))

        ghost_dirs = [UL * 0.9, UR * 0.9, DL * 1.0, DR * 0.8]
        ghosts = [enlarged_eeg.copy().set_opacity(0.55) for _ in ghost_dirs]
        self.add(*ghosts)
        self.play(*[ghost.animate.shift(direction) for ghost, direction in zip(ghosts, ghost_dirs)],
                  run_time=max(0.05, 0.8))

        fade_group = ghosts + [enlarged_eeg]
        per_fade = 1.36 / len(fade_group)
        for mob in fade_group:
            self.play(FadeOut(mob), run_time=max(0.05, per_fade))

        # ---------------- beat 14: central layered stack ----------------
        self.wait(max(0.05, 0.76))

        background_group = VGroup(panels, checklist_rows, psg_diagram)
        self.play(background_group.animate.set_opacity(0.3), run_time=max(0.05, 1.0))

        central_eeg_trace = make_wave(
            lambda u: 0.6 * np.sin(2 * np.pi * 1.5 * u) + 0.15 * np.sin(2 * np.pi * 6 * u),
            width=4.6, height=0.7, color=YELLOW, stroke_width=3
        )
        central_eeg_group = VGroup(
            Text("EEG", font_size=14, color=YELLOW),
            central_eeg_trace
        ).arrange(RIGHT, buff=0.15)
        central_eeg_group.scale_to_fit_width(5.2)

        def make_spectrum_group():
            axis = Line(LEFT * 2.4, RIGHT * 2.4, color=WHITE, stroke_width=2)
            positions = [-1.8, -0.9, 0.0, 0.6, 1.5]
            heights = [1.4, 0.8, 0.7, 0.5, 0.35]
            colors = [PURPLE, BLUE, TEAL, GREEN, ORANGE]
            names = [
                ("delta", "0.5–4 Hz"),
                ("theta", "4–8 Hz"),
                ("alpha", "8–12 Hz"),
                ("sigma", "12–15 Hz"),
                ("beta", "15–30 Hz"),
            ]
            group = VGroup(axis)
            for pos, h, color, (name, freq_range) in zip(positions, heights, colors, names):
                bar = Rectangle(width=0.3, height=h, fill_color=color, fill_opacity=0.85,
                                stroke_color=WHITE, stroke_width=1)
                bar.move_to(np.array([pos, h / 2.0, 0]))
                name_label = Text(name, font_size=10, color=WHITE).move_to(np.array([pos, h + 0.22, 0]))
                range_label = Text(freq_range, font_size=8, color=GREY_B).move_to(np.array([pos, -0.28, 0]))
                group.add(bar, name_label, range_label)
            x_axis_label = Text("Frequency (Hz)", font_size=11, color=WHITE).move_to(DOWN * 0.75)
            group.add(x_axis_label)
            return group

        spectrum_group = make_spectrum_group()

        def make_spectrogram_group():
            rows, cols = 5, 12
            cells = VGroup(*[
                Square(side_length=0.3, fill_color=BLACK, fill_opacity=1, stroke_width=0.5)
                for _ in range(rows * cols)
            ])
            cells.arrange_in_grid(rows=rows, cols=cols, buff=0.03)
            for r in range(rows):
                for c in range(cols):
                    power = 0.35 * np.exp(-((c - 2) / 4.0) ** 2) * (1 - r / rows) + \
                            0.35 * np.exp(-((c - 8) / 3.0) ** 2) * (r / rows)
                    if power < 0.12:
                        color = BLACK
                    elif power < 0.25:
                        color = MAROON
                    elif power < 0.4:
                        color = RED
                    elif power < 0.6:
                        color = ORANGE
                    else:
                        color = YELLOW
                    cells[r * cols + c].set_fill(color, opacity=1)
            freq_label = Text("Frequency →", font_size=10, color=GREY).rotate(PI / 2)
            freq_label.next_to(cells, LEFT, buff=0.1)
            time_label = Text("Time →", font_size=10, color=GREY).next_to(cells, DOWN, buff=0.1)
            return VGroup(cells, freq_label, time_label)

        spectrogram_group = make_spectrogram_group()

        eog_trace = make_wave(
            lambda u: 0.25 * np.sin(2 * np.pi * 1.2 * u)
                      + 0.9 * np.exp(-((u + 0.4) / 0.04) ** 2)
                      + 0.9 * np.exp(-((u - 0.3) / 0.04) ** 2),
            width=4.0, height=0.45, color=TEAL, stroke_width=2.5
        )
        emg_trace = make_wave(
            lambda u: 0.25 * np.sin(2 * np.pi * 10 * u) + 0.10 * np.sin(2 * np.pi * 23 * u),
            width=4.0, height=0.45, color=PURPLE, stroke_width=2.5
        )
        eog_row = VGroup(Text("EOG", font_size=13, color=TEAL), eog_trace).arrange(RIGHT, buff=0.15)
        emg_row = VGroup(Text("EMG", font_size=13, color=PURPLE), emg_trace).arrange(RIGHT, buff=0.15)
        eog_emg_group = VGroup(eog_row, emg_row).arrange(DOWN, buff=0.2)
        eog_emg_group.scale_to_fit_width(5.8)

        central_eeg_group.set_opacity(0)
        spectrum_group.set_opacity(0)
        spectrogram_group.set_opacity(0)
        eog_emg_group.set_opacity(0)

        central_stack = VGroup(
            central_eeg_group,
            spectrum_group,
            spectrogram_group,
            eog_emg_group,
        ).arrange(DOWN, buff=0.2)
        central_stack.scale_to_fit_height(5.8)
        central_stack.move_to(ORIGIN)
        self.add(central_stack)

        self.play(FadeIn(central_eeg_group), FadeIn(spectrum_group), run_time=max(0.05, 1.8))
        self.play(FadeIn(spectrogram_group), run_time=max(0.05, 1.8))
        self.play(FadeIn(eog_emg_group), run_time=max(0.05, 2.3))

        self.wait(max(0.05, 0.76))
        self.play(central_stack.animate.scale(1.02), run_time=max(0.05, 1.0))
        self.play(central_stack.animate.scale(1 / 1.02), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 4.0))