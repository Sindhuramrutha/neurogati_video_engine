ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def make_wave(xs, ys, color=WHITE, width=2.0):
            w = VMobject()
            w.set_points_as_corners([np.array([x, y, 0.0]) for x, y in zip(xs, ys)])
            w.set_stroke(color, width=width)
            w.set_fill(opacity=0)
            return w

        def check_icon(height=0.30):
            c = Circle(radius=height / 2, fill_color=GREEN, fill_opacity=0.85,
                       stroke_color=WHITE, stroke_width=2)
            l1 = Line(c.get_center() + LEFT * 0.13 + DOWN * 0.02,
                      c.get_center() + LEFT * 0.01 + UP * 0.12,
                      color=WHITE, stroke_width=4)
            l2 = Line(c.get_center() + LEFT * 0.01 + UP * 0.12,
                      c.get_center() + RIGHT * 0.15 + DOWN * 0.10,
                      color=WHITE, stroke_width=4)
            return VGroup(c, l1, l2).scale_to_fit_height(height)

        # Beat 1: 0.00-5.82
        title = Text("EEG and Brain States", font_size=44, color=WHITE, weight="BOLD").to_edge(UP, buff=0.30)
        base_xs = np.linspace(-4.6, 4.6, 320)
        base_u = np.linspace(0, 1, 320)
        base_y = 1.1

        wave_a = make_wave(base_xs, base_y + 0.26 * np.sin(2 * np.pi * 13 * base_u)
                           + 0.05 * np.sin(2 * np.pi * 25 * base_u), color=GREEN, width=2.2)
        label_a = Text("State A", font_size=22, color=YELLOW).next_to(wave_a, DOWN, buff=0.25)

        self.play(FadeIn(title), run_time=max(0.05, 0.55))
        self.play(Create(wave_a), run_time=max(0.05, 0.8))
        self.play(FadeIn(label_a), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.4))

        wave_b = make_wave(base_xs, base_y + 0.30 * np.sin(2 * np.pi * 9 * base_u)
                           + 0.04 * np.sin(2 * np.pi * 19 * base_u + 1.2), color=TEAL, width=2.2)
        label_b = Text("State B", font_size=22, color=YELLOW).next_to(wave_a, DOWN, buff=0.25)
        self.play(Transform(wave_a, wave_b), run_time=max(0.05, 1.0))
        self.play(FadeOut(label_a), FadeIn(label_b), run_time=max(0.05, 0.5))

        wave_c = make_wave(base_xs, base_y + 0.38 * np.sin(2 * np.pi * 5 * base_u)
                           + 0.06 * np.sin(2 * np.pi * 12 * base_u + 2.0), color=PURPLE, width=2.2)
        label_c = Text("State C", font_size=22, color=YELLOW).next_to(wave_a, DOWN, buff=0.25)
        self.play(Transform(wave_a, wave_c), run_time=max(0.05, 1.0))
        self.play(FadeOut(label_b), FadeIn(label_c), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.62))

        # Gap to beat 2
        self.wait(max(0.05, 0.86))

        # Beat 2: 6.68-17.30
        self.play(FadeOut(label_c), FadeOut(wave_a), run_time=max(0.05, 0.4))

        row_xs = np.linspace(-5.2, -0.6, 240)
        row_u = np.linspace(0, 1, 240)
        row_ys = [1.7, 0.5, -0.7]
        row_freqs = [5.0, 15.0, 8.0]
        row_amps = [0.30, 0.20, 0.25]
        row_colors = [GREEN, BLUE, ORANGE]
        row_names = ["Rest", "Attention", "Memory"]
        row_groups = []

        for y, freq, amp, col, name in zip(row_ys, row_freqs, row_amps, row_colors, row_names):
            wave = make_wave(row_xs, y + amp * np.sin(2 * np.pi * freq * row_u), color=col, width=2.2)
            lab = Text(name, font_size=16, color=WHITE).next_to(wave, LEFT, buff=0.15)
            row_groups.append(VGroup(wave, lab))

        rows_group = VGroup(*row_groups)
        self.play(LaggedStart(*[FadeIn(g) for g in row_groups], lag_ratio=0.25), run_time=max(0.05, 1.2))

        # Right panels
        spec_panel = RoundedRectangle(corner_radius=0.08, width=3.4, height=2.0,
                                      fill_color="#1A1D26", fill_opacity=0.95,
                                      stroke_color=GREY_B, stroke_width=1.5).move_to([3.5, 1.3, 0])
        ax_h = Line(spec_panel.get_left() + RIGHT * 0.30 + UP * 0.15,
                    spec_panel.get_right() + LEFT * 0.20 + UP * 0.15,
                    color=GREY_B, stroke_width=1.5)
        ax_v = Line(spec_panel.get_left() + RIGHT * 0.30 + UP * 0.15,
                    spec_panel.get_left() + RIGHT * 0.30 + UP * 1.25,
                    color=GREY_B, stroke_width=1.5)
        power_lab = Text("Power", font_size=11, color=GREY_B).rotate(PI / 2).next_to(ax_v, LEFT, buff=0.08)
        freq_lab = Text("Frequency (Hz)", font_size=10, color=GREY_B).move_to(ax_h.get_center() + DOWN * 0.20)

        curve_xs = np.linspace(ax_h.get_left()[0], ax_h.get_right()[0], 150)
        curve_u = np.linspace(0, 1, 150)
        curve_centers = [0.20, 0.65, 0.42]
        curve_colors = row_colors
        curve_mobjects = []
        curve_peaks = []

        for col, center in zip(curve_colors, curve_centers):
            p = np.exp(-0.5 * ((curve_u - center) / 0.09) ** 2) + \
                0.15 * np.exp(-0.5 * ((curve_u - (center + 0.30)) / 0.15) ** 2)
            y_vals = ax_h.get_left()[1] + p * 1.0
            pts = [np.array([x, yy, 0.0]) for x, yy in zip(curve_xs, y_vals)]
            curve = VMobject()
            curve.set_points_as_corners(pts)
            curve.set_stroke(col, width=2.2)
            curve.set_fill(opacity=0)
            curve_mobjects.append(curve)
            curve_peaks.append(pts[int(np.argmax(p))])

        spec_group = VGroup(spec_panel, ax_h, ax_v, power_lab, freq_lab, *curve_mobjects)

        specgram_panel = RoundedRectangle(corner_radius=0.08, width=3.4, height=2.0,
                                          fill_color="#1A1D26", fill_opacity=0.95,
                                          stroke_color=GREY_B, stroke_width=1.5).move_to([3.5, -1.2, 0])
        left = specgram_panel.get_left()[0] + 0.25
        right = specgram_panel.get_right()[0] - 0.18
        bottom = specgram_panel.get_bottom()[1] + 0.28
        top = specgram_panel.get_top()[1] - 0.35
        cols, rows = 8, 5
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                t = c / (cols - 1)
                rf = r / (rows - 1)
                cell_col = interpolate_color(GREEN, PURPLE, 0.30 + 0.50 * t)
                cell = Rectangle(width=(right - left) / cols * 0.92,
                                 height=(top - bottom) / rows * 0.92,
                                 fill_color=cell_col, fill_opacity=0.30 + 0.45 * rf,
                                 stroke_color=GREY_B, stroke_width=0.5)
                cell.move_to([left + (c + 0.5) * (right - left) / cols,
                              bottom + (r + 0.5) * (top - bottom) / rows, 0])
                cells.add(cell)

        time_lab = Text("Time", font_size=10, color=GREY_B).move_to([specgram_panel.get_center()[0], bottom - 0.18, 0])
        freq_lab_specgram = Text("Frequency", font_size=10, color=GREY_B).rotate(PI / 2).move_to(
            [left - 0.25, specgram_panel.get_center()[1], 0])
        specgram_group = VGroup(specgram_panel, cells, time_lab, freq_lab_specgram)

        connectors = VGroup()
        for row_group, peak, col in zip(row_groups, curve_peaks, row_colors):
            start = row_group[0].get_end()
            connector = Line(start, np.array(peak), color=col, stroke_width=1.5, stroke_opacity=0.75)
            connectors.add(connector)

        self.play(FadeIn(spec_group), FadeIn(specgram_group), run_time=max(0.05, 0.8))
        self.play(LaggedStart(*[Create(cl) for cl in connectors], lag_ratio=0.25), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 10.62 - (0.4 + 1.2 + 0.8 + 0.8)))

        # Gap to beat 3
        self.wait(max(0.05, 0.76))

        # Beat 3: 18.06-27.74
        summary_view_group = VGroup(title, rows_group, spec_group, specgram_group, connectors)
        self.play(summary_view_group.animate.set_opacity(0.18).scale(0.75).shift(UP * 0.4), run_time=max(0.05, 0.6))

        strip_rect = RoundedRectangle(corner_radius=0.10, width=7.2, height=0.9,
                                      fill_color="#1A1D26", fill_opacity=0.95,
                                      stroke_color=GREY_B, stroke_width=1.5).move_to([0, 2.35, 0])
        strip_xs = np.linspace(strip_rect.get_left()[0] + 0.55, strip_rect.get_right()[0] - 0.55, 280)
        strip_u = np.linspace(0, 1, 280)
        strip_wave = make_wave(strip_xs, strip_rect.get_center()[1] + 0.20 * np.sin(2 * np.pi * 10 * strip_u),
                               color=GREEN, width=2)
        strip_group = VGroup(strip_rect, strip_wave)
        self.play(FadeIn(strip_group), run_time=max(0.05, 0.9))

        check_labels = ["Excellent temporal resolution", "Non-invasive recording", "Dynamic brain function"]
        check_items = []
        for lab_text in check_labels:
            icon = check_icon(height=0.32)
            lab = Text(lab_text, font_size=19, color=WHITE)
            item = VGroup(icon, lab).arrange(RIGHT, buff=0.22)
            item.scale_to_fit_width(3.5)
            check_items.append(item)

        check_row = VGroup(*check_items).arrange(RIGHT, buff=0.55).move_to([0, 0.7, 0])
        check_row.scale_to_fit_width(11.8)

        for item in check_items:
            self.play(FadeIn(item), run_time=max(0.05, 0.55))
            self.wait(max(0.05, 0.12))

        self.play(check_items[0].animate.set_color(YELLOW), run_time=max(0.05, 0.45))
        self.play(check_items[1].animate.set_color(YELLOW), run_time=max(0.05, 0.45))
        self.play(check_items[2].animate.set_color(YELLOW), run_time=max(0.05, 0.5))
        self.play(check_row.animate.scale(1.04), run_time=max(0.05, 0.4))
        self.play(check_row.animate.scale(1 / 1.04), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 9.68 - (0.6 + 0.9 + 3 * 0.67 + 0.45 + 0.45 + 0.5 + 0.4 + 0.4)))

        # Gap to beat 4
        self.wait(max(0.05, 0.81))

        # Beat 4: 28.55-32.72
        self.play(FadeOut(summary_view_group), FadeOut(strip_group), FadeOut(check_row), run_time=max(0.05, 0.45))

        rows_n = 40
        sky_rects = VGroup(*[
            Rectangle(width=14.2, height=8.2 / rows_n,
                      fill_color=interpolate_color(BLUE, BLACK, 0.22 + 0.78 * i / (rows_n - 1)),
                      fill_opacity=1, stroke_width=0).move_to(
                [0, 4.1 - (i + 0.5) * 8.2 / rows_n, 0])
            for i in range(rows_n)
        ])

        rng = np.random.default_rng(42)
        star_positions = [np.array([rng.uniform(-6.2, 6.2), rng.uniform(-2.8, 3.4), 0]) for _ in range(26)]
        stars = VGroup(*[
            Dot(point=pos, radius=float(rng.uniform(0.015, 0.035)),
                color=WHITE, fill_opacity=rng.uniform(0.5, 0.95), stroke_width=0)
            for pos in star_positions
        ])

        moon_main = Circle(radius=0.36, fill_color=WHITE, fill_opacity=0.92,
                           stroke_width=0).move_to([5.1, 2.75, 0])
        moon_cut = Circle(radius=0.28, fill_color=interpolate_color(BLUE, BLACK, 0.22),
                          fill_opacity=1, stroke_width=0).move_to(moon_main.get_center() + RIGHT * 0.16 + DOWN * 0.05)
        moon = VGroup(moon_main, moon_cut)

        head_pts = [
            [-0.75, 0.95, 0], [-0.1, 1.15, 0], [0.45, 0.85, 0], [0.75, 0.45, 0],
            [0.55, 0.0, 0], [0.85, -0.35, 0], [0.55, -0.75, 0], [0.05, -1.0, 0],
            [-0.65, -1.0, 0], [-0.8, -0.6, 0], [-0.85, 0.0, 0], [-0.75, 0.6, 0]
        ]
        head_profile = Polygon(*head_pts, fill_color=BLACK, fill_opacity=1,
                               stroke_color=GREY_B, stroke_width=2.2)
        head_profile.scale_to_fit_height(2.8)
        head_profile.move_to([0, 0.2, 0])
        neck = Rectangle(width=0.7, height=0.55, fill_color=BLACK, fill_opacity=1,
                         stroke_color=GREY_B, stroke_width=1.5)
        neck.move_to(head_profile.get_bottom() + LEFT * 0.15 + DOWN * 0.25)
        head_silhouette = VGroup(head_profile, neck)

        stage_tracker = ValueTracker(0)
        inner_xs = np.linspace(-0.85, 0.65, 150)
        inner_u = np.linspace(0, 1, 150)
        inner_y = 0.85
        inner_eeg = make_wave(inner_xs, inner_y + 0.06 * np.sin(2 * np.pi * 8.5 * inner_u),
                              color=GREEN, width=2.0)

        sleep_word = Text("Sleep", font_size=44, color=WHITE).move_to([0, -2.0, 0])
        sleep_word.set_opacity(0.92)

        self.play(FadeIn(sky_rects), run_time=max(0.05, 0.7))
        self.play(FadeIn(stars), FadeIn(moon), run_time=max(0.05, 0.55))
        self.play(FadeIn(head_silhouette), run_time=max(0.05, 0.55))
        self.play(Create(inner_eeg), run_time=max(0.05, 0.7))
        self.play(FadeIn(sleep_word), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 4.17 - (0.45 + 0.7 + 0.55 + 0.55 + 0.7 + 0.45)))

        # Gap to beat 5
        self.wait(max(0.05, 0.74))

        # Beat 5: 33.46-39.16
        def update_inner_eeg(wave):
            stage = stage_tracker.get_value()
            u = (inner_xs - inner_xs[0]) / (inner_xs[-1] - inner_xs[0])
            freq = 8.5 - 1.6 * stage
            amp = 0.05 + 0.055 * stage
            pts = [np.array([x, inner_y + amp * np.sin(2 * np.pi * freq * uu + 0.5 * stage), 0])
                   for x, uu in zip(inner_xs, u)]
            wave.set_points_as_corners(pts)

        inner_eeg.add_updater(update_inner_eeg)

        stage_labels = VGroup(*[
            Text(f"Stage {i + 1}", font_size=20, color=GREY_B) for i in range(3)
        ]).arrange(RIGHT, buff=0.5).move_to([0, -2.85, 0])

        self.play(FadeIn(stage_labels), run_time=max(0.05, 0.5))
        for i in range(3):
            self.play(stage_tracker.animate.set_value(i + 1),
                      stage_labels[i].animate.set_color(YELLOW).scale(1.1),
                      run_time=max(0.05, 1.4))
            self.play(stage_labels[i].animate.scale(1 / 1.1), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 5.70 - (0.5 + 3 * 1.6)))

        # Gap to beat 6
        self.wait(max(0.05, 0.66))

        # Beat 6: 39.82-47.02
        for marker in stage_labels:
            self.play(marker.animate.set_color(WHITE).scale(1.12), run_time=max(0.05, 0.3))
            self.play(marker.animate.set_color(YELLOW).scale(1 / 1.12), run_time=max(0.05, 0.2))

        mag_glass = VGroup(
            Circle(radius=0.16, color=WHITE, stroke_width=2.2, fill_color=WHITE, fill_opacity=0.10),
            Line(ORIGIN + 0.10 * UR, ORIGIN + 0.26 * UR, color=WHITE, stroke_width=2.5)
        ).scale_to_fit_height(0.42)
        mag_glass.next_to(sleep_word, RIGHT, buff=0.45)
        self.play(FadeIn(mag_glass), run_time=max(0.05, 0.35))
        self.play(mag_glass.animate.move_to(sleep_word.get_right() + RIGHT * 0.45 + UP * 0.05), run_time=max(0.05, 0.28))
        self.play(mag_glass.animate.move_to(sleep_word.get_right() + RIGHT * 0.45), run_time=max(0.05, 0.28))
        self.play(FadeOut(mag_glass), run_time=max(0.05, 0.35))

        quality_group = VGroup(check_icon(height=0.28),
                               Text("Sleep quality", font_size=18, color=WHITE)).arrange(RIGHT, buff=0.2)
        quality_group.move_to([-4.6, -2.15, 0])
        quality_group.set_opacity(0.9)

        alert_triangle = Polygon(UP * 0.14, LEFT * 0.16 + DOWN * 0.10, RIGHT * 0.16 + DOWN * 0.10,
                                 fill_color=YELLOW, fill_opacity=0.9,
                                 stroke_color=WHITE, stroke_width=1.5)
        alert_mark = Text("!", font_size=14, color=BLACK, weight="BOLD").move_to(
            alert_triangle.get_center() + DOWN * 0.02)
        alert_icon = VGroup(alert_triangle, alert_mark).scale_to_fit_height(0.32)
        disorder_group = VGroup(alert_icon,
                                Text("Sleep disorders", font_size=18, color=WHITE)).arrange(RIGHT, buff=0.2)
        disorder_group.next_to(quality_group, RIGHT, buff=0.8)
        disorder_group.set_opacity(0.9)

        self.play(FadeIn(quality_group), run_time=max(0.05, 0.6))
        self.play(FadeIn(disorder_group), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 7.20 - (1.5 + 1.26 + 0.6 + 0.6)))

        # Gap to beat 7
        self.wait(max(0.05, 1.08))

        # Beat 7: 48.10-52.98
        self.play(self.camera.frame.animate.scale(0.62).move_to(head_profile.get_center() + UP * 0.25),
                  run_time=max(0.05, 1.35))

        rising = VMobject()
        rising.set_points_as_corners([np.array(p) for p in inner_eeg.get_points()])
        rising.set_stroke(WHITE, width=2.5)
        rising.set_fill(opacity=0)
        self.play(rising.animate.move_to([0, 1.5, 0]).scale(2.0).set_stroke(width=3), run_time=max(0.05, 1.0))

        self.play(head_silhouette.animate.set_opacity(0.4), run_time=max(0.05, 0.3))

        title_main = Text("Sleep Staging", font_size=58, color=WHITE, weight="BOLD").move_to([0, 1.5, 0])
        under1_xs = np.linspace(-2.6, 2.6, 120)
        under1 = make_wave(under1_xs, 1.02 + 0.05 * np.sin(2 * np.pi * 1.5 * np.linspace(0, 1, 120)),
                           color=GREY_B, width=1.5)
        under2_xs = np.linspace(-1.9, 1.9, 120)
        under2 = make_wave(under2_xs, 0.78 + 0.04 * np.sin(2 * np.pi * 2.1 * np.linspace(0, 1, 120)),
                           color=GREY_B, width=1.5)
        title_group = VGroup(title_main, under1, under2)

        self.play(FadeIn(title_group), run_time=max(0.05, 0.8))
        self.play(FadeOut(rising), run_time=max(0.05, 0.4))
        self.play(title_group.animate.scale(1.04), run_time=max(0.05, 0.45))
        self.play(title_group.animate.scale(1 / 1.04), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.13))