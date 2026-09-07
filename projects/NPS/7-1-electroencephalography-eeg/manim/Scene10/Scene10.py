ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene10(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- time trackers ---
        scroll_time = ValueTracker(0)
        breath_time = ValueTracker(0)
        freq_tracker = ValueTracker(1.0)   # initial slow, high-amplitude EEG
        amp_tracker = ValueTracker(0.30)

        # --- night sky ---
        rows_n = 20
        sky_rects = VGroup(*[
            Rectangle(
                width=14.4, height=8.4 / rows_n,
                fill_color=interpolate_color(BLUE, BLACK, 0.22 + 0.78 * i / (rows_n - 1)),
                fill_opacity=1, stroke_width=0
            ).move_to([0, 4.2 - (i + 0.5) * 8.4 / rows_n, 0])
            for i in range(rows_n)
        ])

        rng = np.random.default_rng(42)
        star_positions = [np.array([rng.uniform(-6.2, 6.2), rng.uniform(-3.0, 3.4), 0]) for _ in range(26)]
        stars = VGroup(*[
            Dot(point=pos, radius=float(rng.uniform(0.015, 0.035)),
                color=WHITE, fill_opacity=rng.uniform(0.5, 0.95), stroke_width=0)
            for pos in star_positions
        ])

        moon_main = Circle(radius=0.36, fill_color=WHITE, fill_opacity=0.92,
                           stroke_width=0).move_to([5.3, 2.8, 0])
        moon_cut = Circle(radius=0.28, fill_color=interpolate_color(BLUE, BLACK, 0.22),
                          fill_opacity=1, stroke_width=0).move_to(
            moon_main.get_center() + RIGHT * 0.16 + DOWN * 0.05)
        moon = VGroup(moon_main, moon_cut)

        # --- title ---
        title = Text("Sleep Staging", font_size=40, color=WHITE, weight="BOLD")
        title.to_edge(UP, buff=0.30).set_opacity(0.35)

        # --- EEG wave mobject ---
        base_eeg_y = 0.55
        eeg_xs = np.linspace(-5.2, 5.2, 360)
        eeg_u = np.linspace(0, 1, 360)

        def update_eeg(wave):
            t = scroll_time.get_value()
            f = freq_tracker.get_value()
            a = amp_tracker.get_value()
            pts = [np.array([
                x,
                base_eeg_y + a * (
                    0.75 * np.sin(2 * np.pi * f * u - 0.7 * t) +
                    0.25 * np.sin(2 * np.pi * 2.3 * f * u - 1.2 * t + 0.6)
                ),
                0.0
            ]) for x, u in zip(eeg_xs, eeg_u)]
            wave.set_points_as_corners(pts)

        eeg_wave = VMobject()
        eeg_wave.set_points_as_corners([np.array([x, base_eeg_y, 0]) for x in eeg_xs])
        eeg_wave.set_stroke(GREEN, width=2.5)
        eeg_wave.set_fill(opacity=0)
        eeg_wave.add_updater(update_eeg)

        # colored glow band that follows the wave
        band_wave = eeg_wave.copy()
        band_wave.clear_updaters()
        band_wave.set_stroke(color=BLUE, width=10, opacity=0.0)

        def update_band(band):
            band.set_points_as_corners(eeg_wave.get_points())

        band_wave.add_updater(update_band)

        # --- full-screen dim overlay ---
        dim_overlay = Rectangle(width=14.4, height=8.4,
                                fill_color=BLACK, fill_opacity=0,
                                stroke_width=0).move_to(ORIGIN)

        # --- head and sleeping person ---
        head_pts = [
            [-0.75, 0.95, 0], [-0.10, 1.15, 0], [0.45, 0.85, 0], [0.75, 0.45, 0],
            [0.55, 0.00, 0], [0.85, -0.35, 0], [0.55, -0.75, 0], [0.05, -1.00, 0],
            [-0.65, -1.00, 0], [-0.80, -0.60, 0], [-0.85, 0.00, 0], [-0.75, 0.60, 0]
        ]
        old_head = Polygon(*head_pts, fill_color=BLACK, fill_opacity=1,
                           stroke_color=GREY_B, stroke_width=2.2)
        old_head.scale_to_fit_height(2.6).move_to([0, 0.0, 0])

        new_head = old_head.copy().scale_to_fit_height(0.55).move_to([-2.2, -0.65, 0])

        mattress = RoundedRectangle(corner_radius=0.10, width=7.4, height=0.45,
                                    fill_color=GREY_D, fill_opacity=1,
                                    stroke_color=GREY_B, stroke_width=1.5).move_to([0, -1.55, 0])
        leg1 = Rectangle(width=0.15, height=0.35, fill_color=GREY_D,
                         fill_opacity=1, stroke_width=0).move_to([-2.9, -1.9, 0])
        leg2 = Rectangle(width=0.15, height=0.35, fill_color=GREY_D,
                         fill_opacity=1, stroke_width=0).move_to([2.9, -1.9, 0])
        pillow = RoundedRectangle(corner_radius=0.08, width=1.0, height=0.24,
                                  fill_color=WHITE, fill_opacity=0.9,
                                  stroke_color=GREY_B, stroke_width=1.0).move_to([-2.2, -1.15, 0])
        blanket = RoundedRectangle(corner_radius=0.20, width=5.0, height=0.55,
                                   fill_color=PURPLE, fill_opacity=1,
                                   stroke_color=GREY_B, stroke_width=1.5).move_to([0.3, -1.18, 0])

        chest_base_y = -0.88
        chest = Ellipse(width=0.75, height=0.16, fill_color=PURPLE,
                        fill_opacity=1, stroke_width=0).move_to([0.0, chest_base_y, 0])

        def update_chest(chest_mob):
            b = 0.9 * breath_time.get_value()
            chest_mob.set_height(0.16 + 0.04 * np.sin(b))
            chest_mob.move_to([0.0, chest_base_y + 0.02 * np.sin(b), 0])

        chest.add_updater(update_chest)

        bed_base = VGroup(mattress, leg1, leg2, pillow, blanket, chest).set_opacity(0)

        # soft glow inside head region
        head_glow = Circle(radius=0.45, fill_color=YELLOW, fill_opacity=0,
                           stroke_width=0).move_to([-2.2, -0.55, 0])

        # --- segment highlight box (for pause beat) ---
        segment_highlight = RoundedRectangle(
            corner_radius=0.08, width=1.6, height=0.8,
            color=YELLOW, stroke_width=2.5,
            fill_color=YELLOW, fill_opacity=0.08
        ).move_to([0.2, base_eeg_y, 0]).set_opacity(0)

        # --- stage markers ---
        stage_labels = VGroup(*[
            Text(f"Stage {i+1}", font_size=18, color=WHITE)
            for i in range(3)
        ]).arrange(RIGHT, buff=1.0).move_to([0, -2.55, 0]).set_opacity(0)

        # --- bottom clinical/research/disorder items ---
        def make_cross_icon(h=0.30):
            sq = RoundedRectangle(corner_radius=0.06, width=h, height=h,
                                  fill_color=GREY_D, fill_opacity=0.95,
                                  stroke_color=WHITE, stroke_width=1.5)
            vertical = Line(sq.get_center() + UP * 0.12, sq.get_center() + DOWN * 0.12,
                            color=WHITE, stroke_width=3)
            horizontal = Line(sq.get_center() + LEFT * 0.12, sq.get_center() + RIGHT * 0.12,
                              color=WHITE, stroke_width=3)
            return VGroup(sq, vertical, horizontal).scale_to_fit_height(h)

        def make_book_icon(h=0.30):
            doc = Rectangle(width=0.45, height=0.32, fill_color=WHITE,
                            fill_opacity=0.9, stroke_color=GREY_B, stroke_width=1.2)
            l1 = Line(doc.get_left() + RIGHT * 0.08 + DOWN * 0.04,
                      doc.get_right() + LEFT * 0.08 + DOWN * 0.04,
                      color=GREY_B, stroke_width=1.2)
            l2 = Line(doc.get_left() + RIGHT * 0.08, doc.get_right() + LEFT * 0.08,
                      color=GREY_B, stroke_width=1.2)
            l3 = Line(doc.get_left() + RIGHT * 0.08 + UP * 0.04,
                      doc.get_right() + LEFT * 0.08 + UP * 0.04,
                      color=GREY_B, stroke_width=1.2)
            return VGroup(doc, l1, l2, l3).scale_to_fit_height(h)

        def make_warning_icon(h=0.30):
            tri = Polygon(UP * 0.16, LEFT * 0.18 + DOWN * 0.12, RIGHT * 0.18 + DOWN * 0.12,
                          fill_color=YELLOW, fill_opacity=0.9,
                          stroke_color=WHITE, stroke_width=1.5)
            mark = Text("!", font_size=14, color=BLACK, weight="BOLD").move_to(
                tri.get_center() + DOWN * 0.02)
            return VGroup(tri, mark).scale_to_fit_height(h)

        clinical_item = VGroup(
            make_cross_icon(0.30),
            Text("EEG Clinical Applications", font_size=13, color=WHITE)
        ).arrange(DOWN, buff=0.08)

        research_item = VGroup(
            make_book_icon(0.30),
            Text("Sleep research", font_size=13, color=WHITE)
        ).arrange(DOWN, buff=0.08)

        disorder_item = VGroup(
            make_warning_icon(0.30),
            Text("Sleep disorders", font_size=13, color=WHITE)
        ).arrange(DOWN, buff=0.08)

        bottom_row = VGroup(clinical_item, research_item, disorder_item).arrange(
            RIGHT, buff=0.6
        ).scale_to_fit_width(5.6).move_to([-3.2, -3.35, 0])

        clinical_item.set_opacity(0)
        research_item.set_opacity(0)
        disorder_item.set_opacity(0)

        # --- add all mobjects ---
        self.add(sky_rects, stars, moon)
        self.add(dim_overlay)
        self.add(head_glow)
        self.add(bed_base)
        self.add(old_head)
        self.add(eeg_wave)
        self.add(band_wave)
        self.add(segment_highlight)
        self.add(stage_labels)
        self.add(bottom_row)
        self.add(title)

        # --- helper: animate content and keep scroll + breathing active ---
        def play_scene(duration, *anims, scroll=True, breathe=True):
            if duration <= 0:
                return
            anims = list(anims)
            if scroll:
                anims.append(scroll_time.animate.increment_value(duration))
            if breathe:
                anims.append(breath_time.animate.increment_value(duration))
            self.play(*anims, run_time=max(0.05, duration), rate_func=linear)

        # Beat 1: 0.00-4.02
        play_scene(4.02,
                   Transform(old_head, new_head),
                   bed_base.animate.set_opacity(1),
                   title.animate.set_opacity(0.75))

        # gap: 4.02-4.64
        play_scene(0.62)

        # Beat 2: 4.64-8.48 — brain remains active
        play_scene(3.84,
                   dim_overlay.animate.set_fill(opacity=0.30),
                   head_glow.animate.set_fill(opacity=0.50),
                   eeg_wave.animate.set_stroke(color=YELLOW, width=3.0),
                   freq_tracker.animate.set_value(2.0),
                   amp_tracker.animate.set_value(0.22))

        # gap: 8.48-9.10
        play_scene(0.62)

        # Beat 3: 9.10-12.38 — waveform gradually changes shape
        play_scene(1.10,
                   freq_tracker.animate.set_value(2.8),
                   amp_tracker.animate.set_value(0.18))
        play_scene(1.10,
                   freq_tracker.animate.set_value(1.5),
                   amp_tracker.animate.set_value(0.28))
        play_scene(1.08,
                   freq_tracker.animate.set_value(0.7),
                   amp_tracker.animate.set_value(0.34))

        # gap: 12.38-13.12
        play_scene(0.74)

        # Beat 4: 13.12-15.46 — colored band shifts hue/intensity
        play_scene(0.60,
                   band_wave.animate.set_stroke(color=BLUE, opacity=0.16))
        play_scene(0.90,
                   band_wave.animate.set_stroke(color=PURPLE, opacity=0.25))
        play_scene(0.84,
                   band_wave.animate.set_stroke(color=PINK, opacity=0.35))

        # gap: 15.46-16.06
        play_scene(0.60)

        # Beat 5: 16.06-18.68 — pause, highlight a segment, resume
        play_scene(0.60)
        self.play(
            segment_highlight.animate.set_opacity(1).scale(1.06),
            breath_time.animate.increment_value(0.70),
            run_time=max(0.05, 0.70), rate_func=linear
        )
        self.play(
            segment_highlight.animate.scale(1 / 1.06),
            breath_time.animate.increment_value(0.72),
            run_time=max(0.05, 0.72), rate_func=linear
        )
        play_scene(0.60,
                   segment_highlight.animate.set_opacity(0))

        # gap: 18.68-19.38
        play_scene(0.70)

        # Beat 6: 19.38-24.96 — stage markers appear with matching patterns
        stage_targets = [(2.4, 0.18), (1.2, 0.28), (0.6, 0.36)]
        per_stage_first = 1.26
        per_stage_second = 0.60

        for i in range(3):
            play_scene(per_stage_first,
                       stage_labels[i].animate.set_opacity(1).set_color(YELLOW),
                       freq_tracker.animate.set_value(stage_targets[i][0]),
                       amp_tracker.animate.set_value(stage_targets[i][1]))

            extras = [Indicate(stage_labels[i], scale_factor=1.08, color=YELLOW)]
            if i > 0:
                extras.append(stage_labels[i - 1].animate.set_color(WHITE))
            play_scene(per_stage_second, *extras)

        # gap: 24.96-25.60
        play_scene(0.64)

        # Beat 7: 25.60-27.60 — title becomes main focus, connector to wave
        connector_line = Line(
            title.get_center() + DOWN * 0.9,
            [0, base_eeg_y + 0.4, 0],
            color=GREY_B, stroke_width=2.0, stroke_opacity=0.8
        )
        play_scene(2.00,
                   title.animate.set_opacity(1).scale(1.18),
                   stage_labels.animate.set_opacity(0.4).scale(0.9),
                   Create(connector_line))

        # Beat 8: 27.60-33.26 — clinical item fades in
        play_scene(0.90,
                   clinical_item.animate.set_opacity(1))
        play_scene(4.76)

        # Beat 9: 33.26-37.72 — research and disorder items appear
        play_scene(0.90,
                   research_item.animate.set_opacity(1))
        play_scene(0.90,
                   disorder_item.animate.set_opacity(1))
        play_scene(2.66)

        # final hold: 37.72-38.55
        play_scene(0.83)