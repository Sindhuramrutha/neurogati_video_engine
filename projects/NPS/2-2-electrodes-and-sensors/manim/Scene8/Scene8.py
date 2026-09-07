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
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'
}

class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Beat 1 (0.00-4.02): head outline + EEG electrodes
        # ------------------------------------------------------------------
        head_points = [
            np.array([3.4, 2.8, 0]),
            np.array([5.2, 1.2, 0]),
            np.array([5.0, -1.7, 0]),
            np.array([3.4, -2.6, 0]),
            np.array([2.2, -1.8, 0]),
            np.array([2.2, -1.0, 0]),
            np.array([1.0, -0.3, 0]),
            np.array([1.2, 1.0, 0]),
            np.array([1.9, 2.0, 0]),
            np.array([2.6, 2.6, 0]),
        ]

        head_outline = VMobject(
            stroke_color=GREY_B,
            stroke_width=2.5,
            fill_color=WHITE,
            fill_opacity=0.0
        )
        head_outline.set_points_smoothly(head_points + [head_points[0]])

        # Electrode grid over scalp region
        electrodes = VGroup()
        for row in range(3):
            for col in range(5):
                pos = np.array([2.8 + col * 0.55, 1.6 + row * 0.45, 0])
                disc = Circle(
                    radius=0.08,
                    fill_color=YELLOW,
                    fill_opacity=0.4,
                    stroke_color=WHITE,
                    stroke_width=1.0
                )
                disc.move_to(pos)
                electrodes.add(disc)

        eeg_label = Text("EEG", font_size=30, weight="BOLD", color=YELLOW)
        eeg_label.move_to(np.array([1.2, 2.5, 0]))

        head_visual_group = VGroup(head_outline, electrodes)
        head_group = VGroup(head_outline, electrodes, eeg_label)

        self.play(FadeIn(head_outline), run_time=max(0.05, 1.40))
        self.play(FadeIn(electrodes), run_time=max(0.05, 1.40))
        self.play(
            electrodes.animate.set_opacity(1).set_color(YELLOW),
            FadeIn(eeg_label),
            run_time=max(0.05, 1.22
        ))

        # ------------------------------------------------------------------
        # Beat 2 (5.00-11.10): cross-sectional view + 10-20 label + legend
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.98))

        scalp = Circle(
            radius=1.85,
            fill_color=ORANGE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5
        )
        skull = Circle(
            radius=1.55,
            fill_color=GREY_B,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5
        )
        meninges = Circle(
            radius=1.25,
            fill_color=TEAL,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5
        )
        brain_cross = Circle(
            radius=0.9,
            fill_color=PURPLE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5
        )

        cross_section = VGroup(scalp, skull, meninges, brain_cross)
        cross_section.move_to(np.array([-3.2, 0, 0]))

        meninges_label = Text("meninges", font_size=18, color=WHITE)
        meninges_label.move_to(np.array([-1.45, 1.05, 0]))
        skull_label = Text("skull", font_size=18, color=WHITE)
        skull_label.move_to(np.array([-1.20, 0.10, 0]))
        scalp_label = Text("scalp", font_size=18, color=WHITE)
        scalp_label.move_to(np.array([-0.85, -0.55, 0]))

        cross_section_group = VGroup(
            cross_section,
            meninges_label,
            skull_label,
            scalp_label
        )

        system_label = Text(
            "International 10\u201320 System",
            font_size=26,
            color=WHITE,
            t2c={"10\u201320": YELLOW}
        )
        system_label.next_to(head_outline, UP, buff=0.30)

        legend_items = VGroup(
            Text("10\u201320", font_size=20, color=YELLOW),
            Text("standardized placement", font_size=18, color=WHITE)
        ).arrange(DOWN, buff=0.08)

        legend_box = VGroup(
            Rectangle(
                width=2.6,
                height=1.0,
                fill_color="#0F1116",
                fill_opacity=0.8,
                stroke_color=GREY_B,
                stroke_width=1.5
            ),
            legend_items
        )
        legend_items.move_to(legend_box.get_center())
        legend_box.next_to(head_outline, DOWN, buff=0.25)

        head_group.add(system_label, legend_box)

        self.play(FadeIn(cross_section_group), run_time=max(0.05, 2.00))
        self.play(FadeIn(system_label), run_time=max(0.05, 1.20))
        self.play(FadeIn(legend_box), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 1.70))

        # ------------------------------------------------------------------
        # Beat 3 (11.82-14.14): cross-section focus + meninges glow + spark
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.72))

        cross_scale = 1.5

        self.play(
            cross_section_group.animate.move_to(ORIGIN).scale(cross_scale),
            head_group.animate.set_opacity(0.25),
            run_time=max(0.05, 1.00
        ))

        meninges_highlight = Circle(
            radius=1.25 * cross_scale,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_color=YELLOW,
            fill_opacity=0.10
        )
        meninges_highlight.move_to(ORIGIN)
        cross_section_group.add(meninges_highlight)

        spark = Dot(radius=0.08, color=YELLOW, z_index=20)
        spark.move_to(ORIGIN)

        self.play(FadeIn(meninges_highlight), run_time=max(0.05, 0.70))
        self.play(GrowFromCenter(spark), run_time=max(0.05, 0.25))
        self.play(spark.animate.move_to(np.array([0, 1.0, 0])), run_time=max(0.05, 0.37))

        # ------------------------------------------------------------------
        # Beat 4 (14.90-15.52): skull then scalp highlight + impulse travels
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.76))

        skull_highlight = Circle(
            radius=1.55 * cross_scale,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_color=YELLOW,
            fill_opacity=0.10
        )
        skull_highlight.move_to(ORIGIN)
        cross_section_group.add(skull_highlight)

        scalp_highlight = Circle(
            radius=1.85 * cross_scale,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_color=YELLOW,
            fill_opacity=0.10
        )
        scalp_highlight.move_to(ORIGIN)
        cross_section_group.add(scalp_highlight)

        self.play(
            FadeIn(skull_highlight),
            spark.animate.move_to(np.array([0, 1.55 * cross_scale, 0])),
            run_time=max(0.05, 0.31
        ))
        self.play(
            FadeIn(scalp_highlight),
            spark.animate.move_to(np.array([0, 1.85 * cross_scale - 0.08, 0])),
            run_time=max(0.05, 0.31
        ))

        # ------------------------------------------------------------------
        # Beat 5 (15.98-19.24): signal reaches scalp electrode + weak waveform
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.46))

        scalp_electrode = Circle(
            radius=0.15,
            fill_color=YELLOW,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=2.0
        )
        scalp_electrode.move_to(np.array([0, 1.85 * cross_scale, 0]))
        cross_section_group.add(scalp_electrode)

        wave_pts = [
            np.array([
                x,
                1.85 * cross_scale + 0.18 * np.sin(2 * np.pi * (x - 0.35) / 1.2),
                0
            ])
            for x in np.linspace(0.35, 1.90, 40)
        ]
        waveform = VMobject()
        waveform.set_stroke(color=TEAL, width=2, opacity=0.7)
        waveform.set_points_smoothly(wave_pts)

        wave_label = Text("small in amplitude", font_size=20, color=GREY_B)
        wave_label.move_to(np.array([1.60, 1.85 * cross_scale - 0.45, 0]))

        self.play(GrowFromCenter(scalp_electrode), run_time=max(0.05, 0.50))
        self.play(
            spark.animate.move_to(scalp_electrode.get_center()),
            run_time=max(0.05, 0.60
        ))
        self.play(FadeIn(waveform), FadeIn(wave_label), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 1.36))

        # ------------------------------------------------------------------
        # Beat 6 (20.20-24.82): close-up of electrode-scalp interface
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.96))

        self.play(FadeOut(waveform), FadeOut(wave_label), run_time=max(0.05, 0.40))
        self.play(cross_section_group.animate.set_opacity(0.30), run_time=max(0.05, 0.50))

        inset_bg = Rectangle(
            width=5.0,
            height=3.0,
            fill_color="#0F1116",
            fill_opacity=0.95,
            stroke_color=GREY_B,
            stroke_width=2.0
        )
        inset_bg.move_to(np.array([0, 0.5, 0]))

        scalp_surface = Rectangle(
            width=3.0,
            height=0.35,
            fill_color=ORANGE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.0
        )
        scalp_surface.move_to(np.array([0, 0.30, 0]))

        electrode_pad = Rectangle(
            width=1.2,
            height=0.45,
            fill_color=YELLOW,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5
        )
        electrode_pad.move_to(np.array([0, 0.75, 0]))

        gap_line = DashedLine(
            np.array([-0.6, 0.50, 0]),
            np.array([0.6, 0.50, 0]),
            color=WHITE,
            dash_length=0.06,
            stroke_width=2.0
        )

        contact_ellipse = Ellipse(
            width=0.8,
            height=0.20,
            fill_color=RED,
            fill_opacity=0.20,
            stroke_color=RED,
            stroke_width=1.5
        )
        contact_ellipse.move_to(np.array([0, 0.50, 0]))

        close_up_group = VGroup(
            inset_bg,
            scalp_surface,
            electrode_pad,
            gap_line,
            contact_ellipse
        )

        interface_glow = Ellipse(
            width=1.8,
            height=0.40,
            fill_color=YELLOW,
            fill_opacity=0.25,
            stroke_color=YELLOW,
            stroke_width=2.0
        )
        interface_glow.move_to(np.array([0, 0.50, 0]))

        low_imp_label = Text("low impedance", font_size=22, color=GREEN)
        low_imp_label.move_to(np.array([-1.70, 0.90, 0]))

        good_contact_label = Text("good contact", font_size=22, color=GREEN)
        good_contact_label.move_to(np.array([1.70, 0.90, 0]))

        self.play(FadeIn(close_up_group), run_time=max(0.05, 0.90))
        self.play(FadeIn(low_imp_label), run_time=max(0.05, 0.80))
        self.play(FadeIn(good_contact_label), run_time=max(0.05, 0.80))
        self.play(
            interface_glow.animate.scale(1.15).set_opacity(0.50),
            rate_func=there_and_back,
            run_time=max(0.05, 0.60
        ))
        self.wait(max(0.05, 0.62))

        # ------------------------------------------------------------------
        # Beat 7 (25.42-28.18): return to head outline + quality indicator
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.60))

        self.play(
            FadeOut(close_up_group),
            FadeOut(low_imp_label),
            FadeOut(good_contact_label),
            FadeOut(interface_glow),
            run_time=max(0.05, 0.40
        ))
        self.play(
            FadeOut(cross_section_group),
            FadeOut(spark),
            run_time=max(0.05, 0.40
        ))
        self.play(head_group.animate.set_opacity(1), run_time=max(0.05, 0.50))

        quality_tag = Text(
            "high-quality EEG recordings",
            font_size=24,
            color=WHITE
        )
        quality_tag.move_to(np.array([1.30, 1.40, 0]))

        check_icon = SVGMobject(
            ASSET_PATHS["check_circle"],
            height=0.55
        )
        check_icon.set_color(GREEN)
        check_icon.set_fill(GREEN, opacity=1.0)
        check_icon.set_stroke(WHITE, width=0.5)
        check_icon.next_to(quality_tag, LEFT, buff=0.20)

        self.play(
            FadeIn(quality_tag),
            FadeIn(check_icon),
            run_time=max(0.05, 0.70
        ))
        self.play(
            head_visual_group.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=max(0.05, 0.76
        ))

        # ------------------------------------------------------------------
        # Beat 8 (28.18-31.48): forward-looking 10-20 system + applications tag
        # ------------------------------------------------------------------
        self.play(
            FadeOut(head_group),
            FadeOut(quality_tag),
            FadeOut(check_icon),
            run_time=max(0.05, 0.40
        ))

        simple_head_outline = Circle(
            radius=2.2,
            stroke_color=GREY_B,
            stroke_width=2.0,
            fill_color=WHITE,
            fill_opacity=0.0
        )

        simple_grid = VGroup()
        for r in range(4):
            for c in range(5):
                x = -1.2 + c * 0.6
                y = -0.9 + r * 0.6
                dot = Dot(
                    point=np.array([x, y, 0]),
                    radius=0.07,
                    color=YELLOW
                )
                dot.set_fill(YELLOW, opacity=0.7)
                simple_grid.add(dot)

        simple_head_diagram = VGroup(simple_head_outline, simple_grid)
        simple_head_diagram.scale_to_fit_width(5)
        simple_head_diagram.move_to(ORIGIN)
        simple_head_diagram.set_opacity(0.45)

        phrase_text = Text(
            "10\u201320 system",
            font_size=44,
            weight="BOLD",
            color=WHITE,
            t2c={"10\u201320": YELLOW}
        )
        phrase_text.move_to(ORIGIN)

        badge_rect = Rectangle(
            width=2.8,
            height=0.8,
            fill_color=ORANGE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5
        )
        badge_text = Text("Applications module", font_size=20, color=WHITE)
        badge_text.move_to(badge_rect.get_center())
        badge = VGroup(badge_rect, badge_text)
        badge.move_to(np.array([0, -2.6, 0]))

        forward_arrow = Arrow(
            start=np.array([1.8, -2.6, 0]),
            end=np.array([5.8, -2.6, 0]),
            color=YELLOW,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.3
        )

        self.play(FadeIn(simple_head_diagram), run_time=max(0.05, 0.80))
        self.play(FadeIn(phrase_text), run_time=max(0.05, 0.70))
        self.play(
            FadeIn(badge),
            FadeIn(forward_arrow),
            run_time=max(0.05, 0.70
        ))
        self.wait(max(0.05, 0.70))

        # ------------------------------------------------------------------
        # Beat 9 (31.48-36.77): hold + timeline marker at bottom
        # ------------------------------------------------------------------
        timeline_bar = Line(
            np.array([-5.5, -3.5, 0]),
            np.array([5.5, -3.5, 0]),
            color=GREY_B,
            stroke_width=4
        )
        timeline_dot = Dot(
            point=np.array([-5.5, -3.5, 0]),
            radius=0.12,
            color=YELLOW
        )

        self.play(
            Create(timeline_bar),
            FadeIn(timeline_dot),
            run_time=max(0.05, 1.00
        ))
        self.wait(max(0.05, 4.29))