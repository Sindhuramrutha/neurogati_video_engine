ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helper functions
        # ------------------------------------------------------------
        def make_previous_plot():
            ax = Axes(
                x_range=[0, 4, 1],
                y_range=[0, 1.05, 0.5],
                x_length=7,
                y_length=3.5,
                axis_config={"color": GREY, "include_tip": False},
            )
            curve = ax.plot(
                lambda x: 1.0 / (1.0 + np.exp(-5.0 * (x - 1.0))),
                color=GREEN,
                stroke_width=3,
            )
            return VGroup(ax, curve).move_to(ORIGIN)

        def build_panel(title, label_opacity=1.0):
            rect = Rectangle(
                width=5.0,
                height=3.6,
                color=GREY_B,
                stroke_width=1.5,
                fill_color="#181C24",
                fill_opacity=0.8,
            )
            grid_lines = VGroup(*[
                Line(LEFT * 2.35, RIGHT * 2.35, color=GREY, stroke_width=1.0)
                .set_opacity(0.2)
                .shift(UP * y)
                for y in [-1.2, -0.6, 0.0, 0.6, 1.2]
            ])
            label = Text(title, font_size=20, color=WHITE, fill_opacity=label_opacity)
            label.shift(UP * 1.3)
            group = VGroup(rect, grid_lines, label)
            return group, rect, label

        def make_wave_points(drift_scale=1.0, rapid_scale=1.0, residual_drift=False, n=360):
            x = np.linspace(-2.3, 2.3, n)
            t = np.linspace(0, 8 * np.pi, n)
            drift = (
                0.60 * np.sin(0.6 * t)
                + 0.45 * np.sin(1.4 * t + 1.3)
                + 0.30 * np.sin(2.4 * t + 2.8)
            )
            rapid = (
                0.15 * np.sin(14 * t)
                + 0.10 * np.sin(21 * t + 0.7)
                + 0.06 * np.sin(37 * t + 1.5)
            )
            if residual_drift:
                env = np.linspace(0.3, 0.0, n)
                y = rapid_scale * rapid + drift_scale * drift * env
            else:
                y = rapid_scale * rapid + drift_scale * drift
            return np.column_stack([x, y, np.zeros(n)])

        def make_wave_mobject(points, color=WHITE, stroke_width=2.5, stroke_opacity=1.0):
            wave = VMobject()
            wave.set_points_as_corners(points)
            wave.set_stroke(color=color, width=stroke_width, opacity=stroke_opacity)
            wave.set_fill(opacity=0)
            return wave

        def make_dashed_circle(radius=0.62, color=RED, stroke_width=3, segments=36):
            segs = VGroup()
            for i in range(segments):
                a1 = 2 * PI * i / segments
                a2 = a1 + PI / segments
                p1 = radius * np.array([np.cos(a1), np.sin(a1), 0])
                p2 = radius * np.array([np.cos(a2), np.sin(a2), 0])
                segs.add(Line(p1, p2, color=color, stroke_width=stroke_width))
            return segs

        # ------------------------------------------------------------
        # Initial transition from the previous scene's frequency plot
        # ------------------------------------------------------------
        freq_plot = make_previous_plot()
        self.add(freq_plot)

        left_center = np.array([-3.8, 0.7, 0])
        right_center = np.array([3.8, 0.7, 0])

        left_panel_group, left_rect, left_label = build_panel(
            "Before high-pass filtering", label_opacity=1.0
        )
        right_panel_group, right_rect, right_label = build_panel(
            "After high-pass filtering", label_opacity=0.35
        )
        left_panel_group.move_to(left_center)
        right_panel_group.move_to(right_center)
        layout = VGroup(left_panel_group, right_panel_group)

        # Hidden wave layers
        left_raw = make_wave_mobject(make_wave_points(1.0, 1.0), WHITE, 2.5, 1.0)
        left_raw.move_to(left_center)

        left_drift = make_wave_mobject(make_wave_points(1.0, 0.0), YELLOW, 9, 0.65)
        left_drift.move_to(left_center)

        left_rapid_glow = left_raw.copy()
        left_rapid_glow.set_stroke(color=WHITE, width=14, opacity=0.0)
        left_rapid_glow.move_to(left_center)

        left_baseline = DashedLine(
            LEFT * 2.35, RIGHT * 2.35, color=GREY_B, stroke_width=1.5, dash_length=0.08
        ).move_to(left_center)
        left_baseline_label = Text("ideal baseline", font_size=13, color=GREY_B).move_to(
            left_center + LEFT * 0.6 + UP * 0.25
        )
        left_baseline_group = VGroup(left_baseline, left_baseline_label).set_opacity(0)

        right_baseline = DashedLine(
            LEFT * 2.35, RIGHT * 2.35, color=GREY_B, stroke_width=1.5, dash_length=0.08
        ).move_to(right_center)
        right_baseline_label = Text("ideal baseline", font_size=13, color=GREY_B).move_to(
            right_center + RIGHT * 0.6 + UP * 0.25
        )
        right_baseline_group = VGroup(right_baseline, right_baseline_label).set_opacity(0)

        right_wave_partial = make_wave_mobject(
            make_wave_points(drift_scale=1.0, rapid_scale=1.0, residual_drift=True),
            WHITE,
            2.5,
            1.0,
        ).move_to(right_center)
        right_wave_flat = make_wave_mobject(
            make_wave_points(drift_scale=0.0, rapid_scale=1.0, residual_drift=False),
            WHITE,
            2.5,
            1.0,
        ).move_to(right_center)

        # ------------------------------------------------------------
        # Beat 1: previous plot fades out, two-panel layout fades in
        # ------------------------------------------------------------
        self.play(FadeOut(freq_plot), FadeIn(layout), run_time=max(0.05, 1.36))
        right_label.set_opacity(0.35)

        # ------------------------------------------------------------
        # Beat 2: raw EEG-like waveform draws in left panel
        # ------------------------------------------------------------
        self.play(Create(left_raw), run_time=max(0.05, 0.94))

        # ------------------------------------------------------------
        # Beat 3: yellow drift curve + ideal baseline in left panel
        # ------------------------------------------------------------
        self.add(left_baseline_group)
        self.play(
            Create(left_drift),
            left_baseline_group.animate.set_opacity(1),
            run_time=max(0.05, 1.18),
        )

        # ------------------------------------------------------------
        # Beat 4: yellow drift curve glows gently
        # ------------------------------------------------------------
        self.play(left_drift.animate.set_stroke(width=14, opacity=0.9), run_time=max(0.05, 0.8))
        self.play(left_drift.animate.set_stroke(width=8, opacity=0.65), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.04))

        # ------------------------------------------------------------
        # Beat 5: electrode contact annotation
        # ------------------------------------------------------------
        contact_point = Circle(
            radius=0.1,
            color=GREY,
            fill_color=GREY,
            fill_opacity=1,
            stroke_width=1,
        ).move_to(DOWN * 0.5)
        wire = Line(UP * 0.3, DOWN * 0.4, color=GREY_B, stroke_width=3)
        electrode_icon = VGroup(wire, contact_point)
        electrode_text = Text("electrode contact", font_size=18, color=WHITE)
        annotation = VGroup(electrode_icon, electrode_text).arrange(RIGHT, buff=0.2)
        annotation.move_to(left_center + DOWN * 2.3)

        annotation_arrow = Arrow(
            annotation.get_top() + UP * 0.15,
            left_drift.point_from_proportion(0.25),
            color=GREY_B,
            buff=0.05,
            stroke_width=3,
        )
        annotation_group = VGroup(annotation, annotation_arrow)

        self.play(FadeIn(annotation_group), run_time=max(0.05, 0.6))
        self.play(contact_point.animate.scale(1.3), run_time=max(0.05, 0.27))
        self.play(contact_point.animate.scale(1 / 1.3), run_time=max(0.05, 0.27))

        # Gap: 6.26 -> 7.08
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------
        # Beat 6: white glow on fast oscillation component
        # ------------------------------------------------------------
        self.add(left_rapid_glow)
        self.play(
            left_rapid_glow.animate.set_stroke(opacity=0.5, width=18),
            run_time=max(0.05, 0.65),
        )
        self.play(
            left_rapid_glow.animate.set_stroke(opacity=0.2, width=12),
            run_time=max(0.05, 0.65),
        )

        # ------------------------------------------------------------
        # Beat 7: white glow fades, yellow drift glows once
        # ------------------------------------------------------------
        self.play(
            left_rapid_glow.animate.set_stroke(opacity=0.0),
            left_drift.animate.set_stroke(width=16, opacity=0.9),
            run_time=max(0.05, 0.34),
        )
        self.play(
            left_drift.animate.set_stroke(width=8, opacity=0.65),
            run_time=max(0.05, 0.34),
        )

        # Gap: 9.06 -> 9.56
        self.wait(max(0.05, 0.50))

        # ------------------------------------------------------------
        # Beat 8: red border pulses, Hard to interpret caption
        # ------------------------------------------------------------
        left_border = SurroundingRectangle(
            left_rect, color=RED, buff=0.08, stroke_width=3, fill_opacity=0
        ).set_opacity(0)
        self.add(left_border)
        hard_caption = Text("Hard to interpret", font_size=22, color=WHITE).move_to(
            left_center + DOWN * 2.5
        )

        self.play(FadeOut(annotation_group), run_time=max(0.05, 0.4))
        self.play(left_border.animate.set_opacity(0.9), run_time=max(0.05, 0.5))
        self.play(left_border.animate.set_opacity(0.25), run_time=max(0.05, 0.5))
        self.play(FadeIn(hard_caption), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.4))

        # Gap: 12.86 -> 13.56
        self.wait(max(0.05, 0.70))

        # ------------------------------------------------------------
        # Beat 9: filter icon appears between panels
        # ------------------------------------------------------------
        filter_rect = RoundedRectangle(
            corner_radius=0.15,
            width=1.9,
            height=0.9,
            color=BLUE,
            fill_color="#1B2B3A",
            fill_opacity=1,
            stroke_width=2,
        )
        filter_label = Text("High-pass filter", font_size=18, color=WHITE)
        filter_icon = VGroup(filter_rect, filter_label).move_to(np.array([0, 0.7, 0]))
        filter_arrow = Arrow(
            filter_icon.get_right() + RIGHT * 0.1,
            right_rect.get_left() + LEFT * 0.1,
            color=GREEN,
            buff=0.1,
            stroke_width=4,
        )

        self.play(
            GrowFromCenter(filter_icon),
            GrowArrow(filter_arrow),
            right_label.animate.set_opacity(1),
            run_time=max(0.05, 1.62),
        )

        # Gap: 15.18 -> 15.82
        self.wait(max(0.05, 0.64))

        # ------------------------------------------------------------
        # Beat 10: filter icon pulses once, arrow glows
        # ------------------------------------------------------------
        self.play(
            Indicate(filter_icon, color=YELLOW, scale_factor=1.05),
            Indicate(filter_arrow, color=YELLOW, scale_factor=1.0),
            run_time=max(0.05, 0.84),
        )

        # Gap: 16.66 -> 17.28
        self.wait(max(0.05, 0.62))

        # ------------------------------------------------------------
        # Beat 11: left drift partially fades, right waveform draws
        # ------------------------------------------------------------
        self.play(
            left_drift.animate.set_opacity(0.3),
            Create(right_wave_partial),
            run_time=max(0.05, 1.12),
        )

        # Gap: 18.40 -> 19.62
        self.wait(max(0.05, 1.22))

        # ------------------------------------------------------------
        # Beat 12: right waveform flattens, right ideal baseline brightens
        # ------------------------------------------------------------
        self.add(right_baseline_group)
        self.play(
            Transform(right_wave_partial, right_wave_flat),
            right_baseline_group.animate.set_opacity(1),
            run_time=max(0.05, 1.5),
        )

        # Gap: 21.12 -> 21.70
        self.wait(max(0.05, 0.58))

        # ------------------------------------------------------------
        # Beat 13: bright white glow on right-panel fast oscillations
        # ------------------------------------------------------------
        right_glow = right_wave_partial.copy()
        right_glow.set_stroke(color=WHITE, width=16, opacity=0.0)
        self.add(right_glow)

        easier_caption = Text("Easier to observe", font_size=22, color=WHITE).move_to(
            right_center + DOWN * 2.5
        )

        self.play(right_glow.animate.set_stroke(opacity=0.55, width=18), run_time=max(0.05, 0.7))
        self.play(right_glow.animate.set_stroke(opacity=0.25, width=12), run_time=max(0.05, 0.7))
        self.play(FadeIn(easier_caption), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.08))

        # Gap: 24.68 -> 25.55
        self.wait(max(0.05, 0.87))

        # ------------------------------------------------------------
        # Beat 14: left yellow drift gone, improved visibility overlay
        # ------------------------------------------------------------
        improved_text = Text(
            "Improved visibility", font_size=28, color=YELLOW, weight=BOLD
        ).move_to(UP * 3.25)

        self.play(FadeOut(left_drift), Write(improved_text), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 1.59))

        # ------------------------------------------------------------
        # Beat 15: red overlay along removed drift path
        # ------------------------------------------------------------
        left_removed_overlay = left_drift.copy()
        left_removed_overlay.set_stroke(color=RED, width=12, opacity=0.0)
        self.add(left_removed_overlay)

        removed_label = Text("removed", font_size=18, color=RED).move_to(
            left_drift.point_from_proportion(0.7) + UP * 0.4
        )

        self.play(
            left_removed_overlay.animate.set_stroke(opacity=0.35),
            Write(removed_label),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 1.52))

        # Gap: 31.96 -> 32.84
        self.wait(max(0.05, 0.88))

        # ------------------------------------------------------------
        # Beat 16: right panel dims, Be careful heading appears
        # ------------------------------------------------------------
        be_careful_text = Text(
            "Be careful", font_size=28, color=RED, weight=BOLD
        ).move_to(DOWN * 3.0)

        self.play(
            FadeOut(improved_text),
            FadeOut(hard_caption),
            FadeOut(easier_caption),
            FadeOut(removed_label),
            run_time=max(0.05, 0.4),
        )
        self.play(
            right_panel_group.animate.set_opacity(0.6),
            right_wave_partial.animate.set_opacity(0.6),
            right_glow.animate.set_opacity(0.25),
            right_baseline_group.animate.set_opacity(0.5),
            run_time=max(0.05, 0.6),
        )
        self.play(FadeIn(be_careful_text), run_time=max(0.05, 0.46))

        # Gap: 34.30 -> 35.08
        self.wait(max(0.05, 0.78))

        # ------------------------------------------------------------
        # Beat 17: filter glows red, red dashed circle around slow oscillation
        # ------------------------------------------------------------
        red_dashed_circle = make_dashed_circle(radius=0.62, color=RED, stroke_width=3)
        t_slow = np.linspace(0, 2 * np.pi, 120)
        x_slow = np.linspace(-0.42, 0.42, 120)
        y_slow = 0.28 * np.sin(0.9 * t_slow + 0.6) + 0.10 * np.sin(1.8 * t_slow + 1.2)
        slow_phys_points = np.column_stack([x_slow, y_slow, np.zeros(len(x_slow))])
        slow_phys_wave = make_wave_mobject(slow_phys_points, RED, 3.5, 0.95)
        red_circle_group = VGroup(red_dashed_circle, slow_phys_wave).move_to(
            left_center + LEFT * 0.2 + UP * 0.4
        )

        self.play(FadeOut(left_removed_overlay), run_time=max(0.05, 0.4))
        self.play(
            filter_icon.animate.set_color(RED),
            filter_arrow.animate.set_color(RED),
            run_time=max(0.05, 0.5),
        )
        self.play(Indicate(filter_icon, color=RED, scale_factor=1.05), run_time=max(0.05, 0.8))
        self.play(Create(red_circle_group), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 1.46))

        # Gap: 39.44 -> 40.42
        self.wait(max(0.05, 0.98))

        # ------------------------------------------------------------
        # Beat 18: slow oscillation fades, red caution caption appears
        # ------------------------------------------------------------
        removed_phys_caption = Text(
            "Physiological activity below the cutoff is also removed.",
            font_size=20,
            color=RED,
        ).move_to(DOWN * 3.0)
        removed_phys_caption.scale_to_fit_width(11)

        self.play(slow_phys_wave.animate.set_opacity(0), run_time=max(0.05, 3.0))
        self.play(
            FadeOut(be_careful_text),
            FadeIn(removed_phys_caption),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 1.82))

        # Gap: 46.24 -> 46.92
        self.wait(max(0.05, 0.68))

        # ------------------------------------------------------------
        # Beat 19: selected carefully emphasized
        # ------------------------------------------------------------
        cutoff_part1 = Text(
            "Cutoff frequency must always be ", font_size=22, color=WHITE
        )
        cutoff_part2 = Text("selected carefully", font_size=22, color=RED, weight=BOLD)
        cutoff_text = VGroup(cutoff_part1, cutoff_part2).arrange(RIGHT, buff=0.12)
        cutoff_text.move_to(UP * 3.25)
        cutoff_text.scale_to_fit_width(12)

        self.play(FadeIn(cutoff_text), run_time=max(0.05, 1.0))
        self.play(Indicate(cutoff_part2, color=RED, scale_factor=1.03), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.34))

        # ------------------------------------------------------------
        # Beat 20: final hold and gentle fade out
        # ------------------------------------------------------------
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=max(0.05, 0.91))