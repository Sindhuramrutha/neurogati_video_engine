ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Beat 1 (0.00-1.76): cross-section of head, layers, open skull, cortex
        # ------------------------------------------------------------------
        scalp = Ellipse(
            width=3.2,
            height=4.6,
            fill_color=ORANGE,
            fill_opacity=1.0,
            stroke_color=GREY_B,
            stroke_width=2.0,
        )
        skull = Ellipse(
            width=2.7,
            height=3.9,
            fill_color=GREY_B,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.0,
        )
        brain = Ellipse(
            width=2.1,
            height=3.2,
            fill_color=PURPLE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.0,
        )

        # Top portion cut away to expose cortex
        mask_top = Rectangle(
            width=4.6,
            height=2.6,
            fill_color="#0F1116",
            fill_opacity=1.0,
            stroke_width=0,
        )
        mask_top.move_to(np.array([0, 1.7, 0]))

        cut_edge = DashedLine(
            start=np.array([-1.95, 0.4, 0]),
            end=np.array([1.95, 0.4, 0]),
            color=WHITE,
            stroke_width=2.0,
            dash_length=0.08,
        )

        def wavy_cortex_line(y_offset, color, width):
            pts = []
            for x in np.linspace(-1.6, 1.6, 40):
                y = y_offset + 0.10 * np.sin(3.2 * PI * (x + 1.6) / 3.2)
                pts.append(np.array([x, y, 0]))
            line = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
            line.set_points_smoothly(pts)
            return line

        cortex_folds = VGroup(
            wavy_cortex_line(0.05, TEAL, 5),
            wavy_cortex_line(-0.12, GREEN, 3),
            wavy_cortex_line(-0.24, TEAL, 2),
        )

        cross_section = VGroup(scalp, skull, brain, mask_top, cut_edge, cortex_folds)

        self.play(FadeIn(cross_section), run_time=max(0.05, 1.76))

        # ------------------------------------------------------------------
        # Beat 2 (1.76-4.48): ECoG label + pointer + cortex glow
        # ------------------------------------------------------------------
        ecog_label = Text("ECoG", font_size=80, weight="BOLD", color=YELLOW)
        ecog_label.move_to(np.array([3.0, 1.2, 0]))
        ecog_full = Text("Electrocorticography", font_size=30, color=WHITE)
        ecog_full.next_to(ecog_label, DOWN, buff=0.15)

        ecog_pointer = Arrow(
            start=ecog_label.get_left() + LEFT * 0.15,
            end=np.array([1.6, 0.0, 0]),
            color=YELLOW,
            stroke_width=5,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        cortex_glow = cortex_folds[0].copy()
        cortex_glow.set_stroke(YELLOW, width=18, opacity=0.35)

        self.play(
            FadeIn(ecog_label),
            FadeIn(ecog_full),
            Create(ecog_pointer),
            FadeIn(cortex_glow),
            run_time=max(0.05, 2.72),
        )

        # ------------------------------------------------------------------
        # Beat 3 (4.48-7.04): zoom toward cortex + cortical trace label
        # ------------------------------------------------------------------
        self.play(
            FadeOut(ecog_pointer),
            FadeOut(cortex_glow),
            cross_section.animate.scale(1.22, about_point=ORIGIN),
            run_time=max(0.05, 1.00),
        )

        trace = cortex_folds[0].copy()
        trace.set_stroke(YELLOW, width=8, opacity=1.0)

        cortex_label = Text("cerebral cortex", font_size=28, color=GREEN)
        cortex_label.move_to(np.array([1.9, -0.55, 0]))

        # Use a point from the first cortex fold's points array to avoid
        # get_point_from_proportion (which caused a TypeError in this environment)
        cortex_points = cortex_folds[0].get_points()
        mid_index = len(cortex_points) // 2
        cortex_endpoint = cortex_points[mid_index]

        cortex_arrow = Arrow(
            start=cortex_label.get_left(),
            end=cortex_endpoint,
            color=GREEN,
            stroke_width=4,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        self.play(
            Create(trace),
            FadeIn(cortex_label),
            Create(cortex_arrow),
            run_time=max(0.05, 1.56),
        )

        # ------------------------------------------------------------------
        # Gap 7.04-7.98
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.94))

        # ------------------------------------------------------------------
        # Beat 4 (7.98-11.10): old scalp EEG discs crossed out
        # ------------------------------------------------------------------
        scalp_discs = VGroup()

        scalp_disc_positions = [
            np.array([-1.90, -0.3, 0]),
            np.array([-1.95, -1.0, 0]),
            np.array([-1.85, -1.8, 0]),
            np.array([1.90, -0.2, 0]),
            np.array([1.92, -1.0, 0]),
        ]
        for pos in scalp_disc_positions:
            disc = Circle(
                radius=0.08,
                fill_color=YELLOW,
                fill_opacity=0.4,
                stroke_color=GREY_B,
                stroke_width=1.0,
            )
            disc.move_to(pos)
            scalp_discs.add(disc)

        crossout_line = Line(
            start=np.array([-2.45, 0.3, 0]),
            end=np.array([-1.25, -2.2, 0]),
            color=RED,
            stroke_width=3.5,
        )

        self.play(FadeIn(scalp_discs), run_time=max(0.05, 1.00))
        self.play(
            Create(crossout_line),
            scalp_discs.animate.set_opacity(0.15),
            run_time=max(0.05, 2.12),
        )

        # ------------------------------------------------------------------
        # Beat 5 (11.10-15.38): flexible ECoG grid + strip + surgical tag
        # ------------------------------------------------------------------
        grid_base_y = -0.12
        grid_x_vals = np.linspace(-0.9, 0.9, 5)

        def grid_mid_y(x):
            return grid_base_y + 0.12 * np.sin(PI * (x + 0.9) / 1.8)

        grid_contacts = VGroup()
        for c in range(5):
            x = grid_x_vals[c]
            for offset in [-0.16, 0.16]:
                dot = Circle(
                    radius=0.055,
                    fill_color=YELLOW,
                    fill_opacity=0.9,
                    stroke_color=WHITE,
                    stroke_width=1.0,
                )
                dot.move_to(np.array([x, grid_mid_y(x) + offset, 0]))
                grid_contacts.add(dot)

        grid_upper = [
            np.array([x, grid_mid_y(x) + 0.33, 0]) for x in grid_x_vals
        ]
        grid_lower = [
            np.array([x, grid_mid_y(x) - 0.33, 0]) for x in grid_x_vals
        ]
        grid_backing = VMobject(
            fill_color=TEAL,
            fill_opacity=0.35,
            stroke_color=YELLOW,
            stroke_width=1.5,
            close_new_points=True,
        )
        grid_backing.set_points_as_corners(grid_upper + grid_lower[::-1])

        strip_x_vals = np.linspace(-1.35, -0.45, 5)
        strip_base_y = -0.65

        def strip_mid_y(x):
            return strip_base_y + 0.10 * np.sin(PI * (x + 1.35) / 0.9)

        strip_contacts = VGroup()
        for x in strip_x_vals:
            dot = Circle(
                radius=0.045,
                fill_color=YELLOW,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=1.0,
            )
            dot.move_to(np.array([x, strip_mid_y(x), 0]))
            strip_contacts.add(dot)

        strip_upper = [
            np.array([x, strip_mid_y(x) + 0.16, 0]) for x in strip_x_vals
        ]
        strip_lower = [
            np.array([x, strip_mid_y(x) - 0.16, 0]) for x in strip_x_vals
        ]
        strip_backing = VMobject(
            fill_color=PURPLE,
            fill_opacity=0.30,
            stroke_color=YELLOW,
            stroke_width=1.5,
            close_new_points=True,
        )
        strip_backing.set_points_as_corners(strip_upper + strip_lower[::-1])

        grid_label = Text("flexible electrode grid", font_size=18, color=WHITE)
        grid_label.next_to(grid_backing, DOWN, buff=0.20).shift(LEFT * 0.5)

        strip_label = Text("electrode strip", font_size=18, color=WHITE)
        strip_label.next_to(strip_backing, DOWN, buff=0.15).shift(LEFT * 0.4)

        scalpel_handle = Line(start=ORIGIN, end=RIGHT * 0.5, color=GREY_B, stroke_width=4)
        scalpel_blade = Polygon(
            np.array([0, 0, 0]),
            np.array([0.18, 0.10, 0]),
            np.array([0.18, -0.10, 0]),
            fill_color=GREY_B,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.0,
        )
        scalpel = VGroup(scalpel_handle, scalpel_blade).scale(0.35).rotate(-30 * DEGREES)
        surg_text = Text("surgically placed", font_size=18, color=ORANGE)
        surg_tag = VGroup(scalpel, surg_text).arrange(RIGHT, buff=0.12)
        surg_tag.next_to(grid_backing, RIGHT, buff=0.25).shift(DOWN * 0.25)

        self.play(
            FadeIn(grid_backing),
            FadeIn(grid_contacts),
            run_time=max(0.05, 1.60),
        )
        self.play(
            FadeIn(strip_backing),
            FadeIn(strip_contacts),
            run_time=max(0.05, 1.30),
        )
        self.play(
            FadeIn(grid_label),
            FadeIn(strip_label),
            FadeIn(surg_tag),
            run_time=max(0.05, 1.38),
        )

        # ------------------------------------------------------------------
        # Gap 15.38-16.36
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.98))

        # Fade out all scene-9-specific single-view content before side-by-side
        previous_scene_group = VGroup(
            cross_section,
            ecog_label,
            ecog_full,
            trace,
            cortex_label,
            cortex_arrow,
            scalp_discs,
            crossout_line,
            grid_backing,
            grid_contacts,
            strip_backing,
            strip_contacts,
            grid_label,
            strip_label,
            surg_tag,
        )

        # ------------------------------------------------------------------
        # Beat 6 (16.36-19.30): side-by-side EEG vs ECoG comparison panel
        # ------------------------------------------------------------------
        left_x = -3.4
        right_x = 3.4
        head_cy = 1.5

        left_head = Circle(
            radius=1.0,
            fill_color=ORANGE,
            fill_opacity=0.12,
            stroke_color=GREY_B,
            stroke_width=2.0,
        )
        left_head.move_to(np.array([left_x, head_cy, 0]))

        left_electrode = Circle(
            radius=0.12,
            fill_color=YELLOW,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        left_electrode.move_to(np.array([left_x, head_cy + 1.0, 0]))

        left_wave_x = np.linspace(left_x - 2.0, left_x + 2.0, 70)
        rng = np.random.RandomState(42)
        left_wave_y = (
            -0.9
            + 0.16 * np.sin(3 * 2 * PI * (left_wave_x - left_x) / 4.0)
            + 0.08 * rng.normal(size=len(left_wave_x))
        )
        left_waveform = VMobject(stroke_color=TEAL, stroke_width=1.5)
        left_waveform.set_points_as_corners(
            [np.array([x, y, 0]) for x, y in zip(left_wave_x, left_wave_y)]
        )

        left_wave_label = Text("EEG (scalp)", font_size=22, color=WHITE)
        left_wave_label.next_to(left_waveform, DOWN, buff=0.18)

        left_source = Dot(
            point=np.array([left_x, head_cy - 0.1, 0]),
            radius=0.08,
            color=RED,
        )
        left_dist_line = DashedLine(
            start=left_source.get_center(),
            end=left_electrode.get_center(),
            color=GREY_B,
            stroke_width=2.0,
        )
        left_dist_label = Text("distance", font_size=16, color=GREY_B)
        left_dist_label.next_to(left_dist_line, LEFT, buff=0.12)

        left_panel = VGroup(
            left_head,
            left_electrode,
            left_waveform,
            left_wave_label,
            left_source,
            left_dist_line,
            left_dist_label,
        )

        right_head = Circle(
            radius=1.0,
            fill_color=PURPLE,
            fill_opacity=0.25,
            stroke_color=GREY_B,
            stroke_width=2.0,
        )
        right_head.move_to(np.array([right_x, head_cy, 0]))

        right_cut_line = DashedLine(
            start=np.array([right_x - 0.7, head_cy + 0.85, 0]),
            end=np.array([right_x + 0.7, head_cy + 0.85, 0]),
            color=WHITE,
            stroke_width=2.0,
            dash_length=0.07,
        )

        cortex_x = np.linspace(right_x - 0.55, right_x + 0.55, 30)
        cortex_y = head_cy + 0.55 + 0.08 * np.sin(
            2 * 2 * PI * (cortex_x - (right_x - 0.55)) / 1.1
        )
        right_cortex_line = VMobject(stroke_color=GREEN, stroke_width=4)
        right_cortex_line.set_points_smoothly(
            [np.array([x, y, 0]) for x, y in zip(cortex_x, cortex_y)]
        )

        right_grid_contacts = VGroup()
        for c in range(6):
            x = right_x - 0.55 + c * 0.22
            y = head_cy + 0.52 + 0.08 * np.sin(
                2 * 2 * PI * (x - (right_x - 0.55)) / 1.1
            )
            dot = Circle(
                radius=0.05,
                fill_color=GREY_B,
                fill_opacity=0.5,
                stroke_color=GREY_B,
                stroke_width=1.0,
            )
            dot.move_to(np.array([x, y, 0]))
            right_grid_contacts.add(dot)

        right_grid = VGroup(right_cortex_line, right_grid_contacts)

        right_wave_x = np.linspace(right_x - 2.0, right_x + 2.0, 70)
        right_wave_y = -0.9 + 0.65 * np.sin(
            2 * 2 * PI * (right_wave_x - right_x) / 4.0
        )
        right_waveform = VMobject(stroke_color=GREEN, stroke_width=2.0)
        right_waveform.set_points_smoothly(
            [np.array([x, y, 0]) for x, y in zip(right_wave_x, right_wave_y)]
        )

        rng2 = np.random.RandomState(7)
        right_noise_y = right_wave_y + 0.12 * rng2.normal(size=len(right_wave_x))
        right_noise_overlay = VMobject(
            stroke_color=GREY_B,
            stroke_width=1.2,
            stroke_opacity=0.5,
        )
        right_noise_overlay.set_points_as_corners(
            [np.array([x, y, 0]) for x, y in zip(right_wave_x, right_noise_y)]
        )

        right_wave_label = Text("ECoG (cortex)", font_size=22, color=WHITE)
        right_wave_label.next_to(right_waveform, DOWN, buff=0.18)

        right_source = Dot(
            point=np.array([right_x, head_cy - 0.1, 0]),
            radius=0.08,
            color=RED,
        )
        right_dist_line = DashedLine(
            start=right_source.get_center(),
            end=right_grid_contacts[1].get_center() + UP * 0.05,
            color=GREY_B,
            stroke_width=2.0,
        )
        right_dist_label = Text("shorter distance", font_size=16, color=GREEN)
        right_dist_label.next_to(right_dist_line, RIGHT, buff=0.15)

        right_panel = VGroup(
            right_head,
            right_cut_line,
            right_cortex_line,
            right_grid_contacts,
            right_waveform,
            right_noise_overlay,
            right_wave_label,
            right_source,
            right_dist_line,
            right_dist_label,
        )

        panel_group = VGroup(left_panel, right_panel)

        self.play(FadeOut(previous_scene_group), run_time=max(0.05, 0.50))
        self.play(FadeIn(left_panel), run_time=max(0.05, 1.40))
        self.play(FadeIn(right_panel), run_time=max(0.05, 1.04))

        # ------------------------------------------------------------------
        # Beat 7 (19.30-27.82): three advantages reinforced
        # ------------------------------------------------------------------
        adv1 = Text("higher signal amplitude", font_size=24, color=GREY_B)
        adv2 = Text("better spatial resolution", font_size=24, color=GREY_B)
        adv3 = Text(
            "improved signal-to-noise ratio",
            font_size=24,
            color=GREY_B,
        )
        adv_group = VGroup(adv1, adv2, adv3).arrange(DOWN, buff=0.18)
        adv_group.move_to(np.array([0, -2.5, 0]))

        # phase 1: higher signal amplitude (1.70s)
        self.play(FadeIn(adv_group), run_time=max(0.05, 0.50))
        self.play(
            right_waveform.animate.stretch(1.5, 1),
            adv1.animate.set_color(YELLOW),
            run_time=max(0.05, 1.20),
        )

        # phase 2: better spatial resolution (2.40s)
        self.play(adv2.animate.set_color(YELLOW), run_time=max(0.05, 0.30))
        per_contact_time = (2.40 - 0.30) / len(right_grid_contacts)
        for contact in right_grid_contacts:
            self.play(
                contact.animate.set_color(YELLOW),
                run_time=max(0.05, per_contact_time),
            )

        # phase 3: improved SNR (2.40s)
        self.play(adv3.animate.set_color(YELLOW), run_time=max(0.05, 0.30))
        self.play(FadeOut(right_noise_overlay), run_time=max(0.05, 2.10))

        # phase 4: brief emphasis + hold (2.02s)
        self.play(
            Indicate(right_grid, color=YELLOW, scale_factor=1.06),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------------
        # Beat 8 (27.82-32.46): neurosurgery warning
        # ------------------------------------------------------------------
        warning_triangle = Polygon(
            np.array([-0.35, 0.25, 0]),
            np.array([0.35, 0.25, 0]),
            np.array([0, -0.35, 0]),
            fill_color=YELLOW,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.0,
        )
        exclaim = Text("!", font_size=28, weight="BOLD", color=BLACK)
        exclaim.move_to(warning_triangle.get_center() + DOWN * 0.02)
        warning_icon = VGroup(warning_triangle, exclaim).scale(0.5)

        warning_text = Text(
            "requires neurosurgery",
            font_size=24,
            weight="BOLD",
            color=YELLOW,
        )
        warning_group = VGroup(warning_icon, warning_text).arrange(RIGHT, buff=0.18)
        warning_group.move_to(np.array([right_x, 3.0, 0]))

        grid_highlight = SurroundingRectangle(
            right_grid,
            color=YELLOW,
            buff=0.08,
            stroke_width=4.0,
        )

        cut_glow = DashedLine(
            start=np.array([right_x - 0.7, head_cy + 0.85, 0]),
            end=np.array([right_x + 0.7, head_cy + 0.85, 0]),
            color=YELLOW,
            stroke_width=4.0,
            dash_length=0.09,
        )

        self.play(
            panel_group.animate.set_opacity(0.35),
            run_time=max(0.05, 0.80),
        )
        self.play(FadeIn(warning_group), run_time=max(0.05, 1.00))
        self.play(
            Create(grid_highlight),
            FadeIn(cut_glow),
            run_time=max(0.05, 1.00),
        )
        self.play(
            Indicate(right_grid, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 1.00),
        )
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------------
        # Beat 9 (32.46-36.30): invasive label + red tint + final hold
        # ------------------------------------------------------------------
        invasive_text = Text(
            "invasive",
            font_size=30,
            weight="BOLD",
            color=RED,
        )
        invasive_text.next_to(right_wave_label, DOWN, buff=0.20)

        red_tint_overlay = SurroundingRectangle(
            right_grid,
            color=RED,
            buff=0.15,
            fill_color=RED,
            fill_opacity=0.15,
            stroke_width=2.0,
        )

        self.play(
            FadeIn(invasive_text),
            FadeIn(red_tint_overlay),
            run_time=max(0.05, 1.20),
        )
        self.play(
            red_tint_overlay.animate.set_opacity(0.08),
            rate_func=there_and_back,
            run_time=max(0.05, 1.44),
        )
        self.wait(max(0.05, 1.20))