ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import math
import numpy as np


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- 1-2. MODULE 6 title ----------
        module = Text("MODULE", font_size=80, weight=BOLD, color=WHITE)
        six = Text("6", font_size=80, weight=BOLD, color=GOLD)
        title = VGroup(module, six).arrange(RIGHT, buff=0.3).move_to(UP * 2.8)

        module_target = module.get_center()
        six_target = six.get_center()

        module.move_to(LEFT * 9 + UP * 1.8)
        self.play(
            module.animate.move_to(module_target),
            run_time=max(0.05, 0.48),
            rate_func=rate_functions.ease_out_sine,
        )

        six.move_to(RIGHT * 9 + UP * 2.8)
        self.play(
            six.animate.move_to(six_target),
            run_time=max(0.05, 0.30),
            rate_func=rate_functions.ease_in_out_sine,
        )

        # settle bounce
        self.play(
            module.animate.shift(DOWN * 0.06),
            six.animate.shift(DOWN * 0.06),
            run_time=max(0.05, 0.04),
            rate_func=rate_functions.ease_out_sine,
        )
        self.play(
            module.animate.shift(UP * 0.06),
            six.animate.shift(UP * 0.06),
            run_time=max(0.05, 0.04),
            rate_func=rate_functions.ease_in_out_sine,
        )

        self.wait(max(0.05, 0.70))  # 0.86 -> 1.56

        # ---------- 3. Subtitle, letter by letter ----------
        sub_text = "Time-Frequency Analysis"
        sub_letters = VGroup(*[Text(ch, font_size=36, color=GREY_B) for ch in sub_text])
        sub_letters.arrange(RIGHT, buff=0.03)
        sub_letters.next_to(title, DOWN, buff=0.6)

        for ch in sub_letters:
            ch.scale(1.4).set_opacity(0)

        per_char = max(0.02, 0.82 / len(sub_letters))
        for ch in sub_letters:
            self.play(
                ch.animate.scale(1 / 1.4).set_opacity(1),
                run_time=max(0.05, per_char),
            )

        self.wait(max(0.05, 1.18))  # 2.38 -> 3.56

        # ---------- 4-5. Wavy time-domain signal ----------
        wave_xs = np.linspace(-6.3, -0.6, 300)

        def wave_y(x, t):
            amp1 = 0.55 * (1 + 0.30 * math.sin(0.8 * t))
            amp2 = 0.35 * (1 - 0.25 * math.sin(0.7 * t + 0.8))
            amp3 = 0.28 * (1 + 0.30 * math.sin(0.9 * t + 1.5))

            y = (
                amp1 * math.sin(0.9 * x + 0.6)
                + amp2 * math.sin(1.7 * x + 2.2)
                + amp3 * math.sin(2.6 * x + 4.0)
            )
            y += 0.07 * math.sin(2.0 * x - 1.2 * t) * math.sin(1.1 * t)
            return y - 0.5

        points = [np.array([x, wave_y(x, 0.0), 0.0]) for x in wave_xs]
        wave = VMobject(stroke_color=BLUE, stroke_width=4).set_points_as_corners(points)

        self.play(
            Create(wave),
            run_time=max(0.05, 0.96),
            rate_func=rate_functions.linear,
        )

        # continuous wiggle state
        wave_time = ValueTracker(0)
        self.add(wave_time)
        wave_time.add_updater(lambda m, dt: m.increment_value(dt))

        wave_opacity = ValueTracker(1)
        self.add(wave_opacity)

        peak_x = -3.1
        peak_state = {"marker": None, "afterglow": None}

        def update_wave(mob):
            t = wave_time.get_value()
            pts = [np.array([x, wave_y(x, t), 0.0]) for x in wave_xs]
            mob.set_points_as_corners(pts)
            mob.set_stroke(opacity=wave_opacity.get_value())

            marker = peak_state.get("marker")
            if marker is not None:
                marker.move_to(np.array([peak_x, wave_y(peak_x, t), 0.0]))

            afterglow = peak_state.get("afterglow")
            if afterglow is not None:
                afterglow.move_to(np.array([peak_x, wave_y(peak_x, t), 0.0]))

        wave.add_updater(update_wave)

        self.wait(max(0.05, 1.18))  # 4.52 -> 5.70
        self.wait(max(0.05, 0.42))  # 5.70 -> 6.12

        # ---------- 6-8. Spectrogram heatmap ----------
        n_rows = 10
        n_cols = 16
        cell_w = 0.23
        cell_h = 0.17

        row_colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, RED], n_rows + 1)

        rows = []
        for r in range(n_rows):
            row = VGroup()
            for c in range(n_cols):
                mix = 0.5 + 0.5 * math.sin(2 * math.pi * c / n_cols)
                color = interpolate_color(row_colors[r], row_colors[r + 1], mix)
                rect = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_width=0,
                    stroke_opacity=0,
                )
                row.add(rect)
            row.arrange(RIGHT, buff=0)
            rows.append(row)

        spec_group = VGroup(*rows).arrange(UP, buff=0).move_to(RIGHT * 3.6 + DOWN * 0.6)

        spec_time = ValueTracker(0)
        self.add(spec_time)
        spec_time.add_updater(lambda m, dt: m.increment_value(dt))

        def make_spec_updater(r_idx):
            def updater(row_mob):
                t = spec_time.get_value()
                for c, cell in enumerate(row_mob):
                    mix = 0.5 + 0.5 * math.sin(
                        2 * math.pi * c / n_cols - t * 2.0
                    )
                    cell.set_fill(
                        interpolate_color(
                            row_colors[r_idx], row_colors[r_idx + 1], mix
                        )
                    )

            return updater

        # first half of rows, bottom-up
        per_row = 0.86 / 5
        for r in range(5):
            self.play(FadeIn(rows[r]), run_time=max(0.05, per_row))
            rows[r].add_updater(make_spec_updater(r))

        # remaining rows + transform arrow
        arrow_start = np.array([-0.9, -0.8, 0.0])
        arrow_end = np.array([1.55, -0.8, 0.0])
        shaft = Line(arrow_start, arrow_end, color=YELLOW, stroke_width=4)
        tip = Polygon(
            arrow_end,
            arrow_end + LEFT * 0.22 + UP * 0.10,
            arrow_end + LEFT * 0.22 + DOWN * 0.10,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
        )

        remaining_rows = rows[5:]
        self.play(
            LaggedStart(
                *[FadeIn(row) for row in remaining_rows],
                lag_ratio=0.25,
                run_time=max(0.05, 0.60),
            ),
            Create(shaft, run_time=max(0.05, 0.60)),
        )
        self.play(GrowFromCenter(tip), run_time=max(0.05, 0.12))

        for r in range(5, n_rows):
            rows[r].add_updater(make_spec_updater(r))

        # completed living heatmap holds
        self.wait(max(0.05, 0.84))  # 7.70 -> 8.54
        self.wait(max(0.05, 0.58))  # 8.54 -> 9.12

        # ---------- 9. Highlight one peak, pulse twice ----------
        current_peak_y = wave_y(peak_x, wave_time.get_value())
        marker = Dot(
            point=np.array([peak_x, current_peak_y, 0.0]),
            radius=0.12,
            color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
        )
        marker.set_opacity(0.8)
        peak_state["marker"] = marker

        self.play(
            wave_opacity.animate.set_value(0.35),
            GrowFromCenter(marker),
            run_time=max(0.05, 0.12),
        )

        self.play(marker.animate.scale(1.5).set_opacity(1), run_time=max(0.05, 0.12))
        self.play(marker.animate.scale(1 / 1.5).set_opacity(0.7), run_time=max(0.05, 0.12))
        self.play(marker.animate.scale(1.5).set_opacity(1), run_time=max(0.05, 0.12))
        self.play(marker.animate.scale(1 / 1.5).set_opacity(0.7), run_time=max(0.05, 0.12))
        self.wait(max(0.05, 0.28))  # total 0.88

        # ---------- 10. One more pulse, then highlight fades ----------
        self.play(marker.animate.scale(1.5).set_opacity(1), run_time=max(0.05, 0.12))
        self.play(marker.animate.scale(1 / 1.5).set_opacity(0.7), run_time=max(0.05, 0.12))
        self.play(
            FadeOut(marker),
            wave_opacity.animate.set_value(1),
            run_time=max(0.05, 0.52),
        )
        peak_state["marker"] = None

        # ---------- 11. Faint afterglow, then return ----------
        afterglow_y = wave_y(peak_x, wave_time.get_value())
        afterglow = Circle(
            radius=0.18,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=0,
        )
        afterglow.move_to(np.array([peak_x, afterglow_y, 0.0]))
        afterglow.set_opacity(0)
        peak_state["afterglow"] = afterglow

        self.play(afterglow.animate.set_opacity(0.25), run_time=max(0.05, 0.16))
        self.play(afterglow.animate.set_opacity(0), run_time=max(0.05, 0.40))
        peak_state["afterglow"] = None
        self.wait(max(0.05, 0.50))  # total 1.06

        # hold everything steady
        self.wait(max(0.05, 0.94))  # 11.82 -> 12.76

        # ---------- 12. Clear diagram ----------
        self.play(
            wave_opacity.animate.set_value(0),
            shaft.animate.scale(0.7).set_opacity(0),
            tip.animate.scale(0.7).set_opacity(0),
            *[row.animate.scale(0.7).set_opacity(0) for row in rows],
            FadeOut(module),
            FadeOut(six),
            *[FadeOut(ch) for ch in sub_letters],
            run_time=max(0.05, 0.26),
            rate_func=rate_functions.ease_in_sine,
        )

        # ---------- 13-14. Closing phrase ----------
        phrase = Text("Let's get started!", font_size=72, weight=BOLD, color=WHITE)
        phrase.scale(0.2).set_opacity(0)

        self.play(
            phrase.animate.scale(5).set_opacity(1),
            run_time=max(0.05, 0.30),
            rate_func=rate_functions.ease_out_sine,
        )
        self.play(
            Flash(
                phrase.get_center(),
                color=YELLOW,
                line_length=0.5,
                num_lines=12,
                flash_radius=0.6,
            ),
            run_time=max(0.05, 0.14),
        )

        # subtle settle pulse during hold
        self.play(
            phrase.animate.scale(1.04),
            run_time=max(0.05, 0.37),
            rate_func=rate_functions.there_and_back,
        )
        self.wait(max(0.05, 0.37))  # 13.46 + 0.74 -> 14.20