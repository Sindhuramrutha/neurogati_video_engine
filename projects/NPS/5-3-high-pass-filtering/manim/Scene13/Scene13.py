ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene13(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Beat 1: 0.00–0.80  (duration 0.80)
        heading = Text("Summary: High-Pass Filter", font_size=56, weight="BOLD", color=WHITE)
        heading.move_to(UP * 3.0)
        divider = Line(LEFT * 6, RIGHT * 6, color=GREY_B, stroke_width=2)
        divider.next_to(heading, DOWN, buff=0.25)

        self.play(FadeIn(heading), run_time=max(0.05, 0.5))
        self.play(Create(divider), run_time=max(0.05, 0.3))
        # Gap to 1.36
        self.wait(max(0.05, 1.36 - 0.80))  # 0.56

        # ------------------------------------------------------------
        # Beat 2: 1.36–5.20  (duration 3.84)
        waveform_icon = self._make_fast_wave_icon(color=TEAL)
        waveform_icon.scale(0.55)

        bullet1_text = Text(
            "Preserves high-frequency components while reducing\n"
            "frequencies below a selected cutoff frequency.",
            font_size=28,
            color=WHITE,
            line_spacing=0.6,
        )

        bullet1 = VGroup(waveform_icon, bullet1_text)
        bullet1.arrange(RIGHT, buff=0.4, aligned_edge=UP)
        bullet1.move_to(UP * 1.5)
        bullet1.scale_to_fit_width(12)

        self.play(FadeIn(bullet1), run_time=max(0.05, 1.0))
        # Wait until 5.20
        self.wait(max(0.05, 5.20 - 1.36 - 1.0))  # 2.84

        # ------------------------------------------------------------
        # Beat 3: 6.06–12.02  (duration 5.96)
        # Gap before beat 3
        self.wait(max(0.05, 6.06 - 5.20))  # 0.86

        # Highlight phrase 1: "Preserves high-frequency components"
        self.play(
            bullet1_text.animate.set_color_by_t2c(
                {"Preserves high-frequency components": YELLOW}
            ),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.5))
        # Highlight phrase 2: "reducing frequencies below a selected cutoff frequency"
        self.play(
            bullet1_text.animate.set_color(WHITE).set_color_by_t2c(
                {"reducing frequencies below a selected cutoff frequency": YELLOW}
            ),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 0.5))
        self.play(bullet1_text.animate.set_color(WHITE), run_time=max(0.05, 0.5))
        # Wait until 12.02
        self.wait(max(0.05, 12.02 - 6.06 - (1.0 + 0.5 + 1.0 + 0.5 + 0.5)))  # 2.46

        # ------------------------------------------------------------
        # Beat 4: 13.04–15.20  (duration 2.16)
        self.wait(max(0.05, 13.04 - 12.02))  # 1.02

        arrow_down_icon = self._make_arrow_down_icon(color=ORANGE)
        arrow_down_icon.scale(0.55)

        bullet2_text = Text("Reduces baseline drift.", font_size=28, color=WHITE)
        bullet2 = VGroup(arrow_down_icon, bullet2_text)
        bullet2.arrange(RIGHT, buff=0.4, aligned_edge=UP)
        bullet2.next_to(bullet1, DOWN, buff=0.5, aligned_edge=LEFT)
        bullet2.scale_to_fit_width(12)

        self.play(
            FadeIn(bullet2),
            arrow_down_icon.animate.shift(DOWN * 0.15),
            run_time=max(0.05, 1.2),
        )
        self.play(arrow_down_icon.animate.shift(UP * 0.15), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 15.20 - 13.04 - 1.2 - 0.3))  # 0.66

        # ------------------------------------------------------------
        # Beat 5: 15.78–17.08  (duration 1.30)
        self.wait(max(0.05, 15.78 - 15.20))  # 0.58

        motion_wave_icon = self._make_slow_wave_icon(color=PURPLE)
        motion_wave_icon.scale(0.55)

        bullet3_text = Text("Suppresses slow movement artefacts.", font_size=28, color=WHITE)
        bullet3 = VGroup(motion_wave_icon, bullet3_text)
        bullet3.arrange(RIGHT, buff=0.4, aligned_edge=UP)
        bullet3.next_to(bullet2, DOWN, buff=0.5, aligned_edge=LEFT)
        bullet3.scale_to_fit_width(12)

        self.play(FadeIn(bullet3), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 17.08 - 15.78 - 0.8))  # 0.50

        # ------------------------------------------------------------
        # Beat 6: 17.84–20.90  (duration 3.06)
        self.wait(max(0.05, 17.84 - 17.08))  # 0.76

        square_wave_icon = self._make_square_wave_icon(color=GREEN)
        square_wave_icon.scale(0.55)

        bullet4_text = Text(
            "Improves visibility of rapidly changing neural activity.",
            font_size=28,
            color=WHITE,
        )
        bullet4 = VGroup(square_wave_icon, bullet4_text)
        bullet4.arrange(RIGHT, buff=0.4, aligned_edge=UP)
        bullet4.next_to(bullet3, DOWN, buff=0.5, aligned_edge=LEFT)
        bullet4.scale_to_fit_width(12)

        self.play(FadeIn(bullet4), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 20.90 - 17.84 - 1.0))  # 2.06

        # ------------------------------------------------------------
        # Beat 7: 21.82–26.98  (duration 5.16)
        self.wait(max(0.05, 21.82 - 20.90))  # 0.92

        warning_tri = Polygon(
            np.array([0, 0.45, 0]),
            np.array([-0.5, -0.35, 0]),
            np.array([0.5, -0.35, 0]),
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        warning_ex = Text("!", font_size=24, color="#0F1116", weight="BOLD")
        warning_ex.move_to(warning_tri.get_center() + DOWN * 0.06)
        warning_icon = VGroup(warning_tri, warning_ex)
        warning_icon.scale(0.55)

        bullet5_text = Text(
            "Must be configured carefully to avoid removing\n"
            "useful physiological information.",
            font_size=28,
            color=WHITE,
            line_spacing=0.6,
        )
        bullet5 = VGroup(warning_icon, bullet5_text)
        bullet5.arrange(RIGHT, buff=0.4, aligned_edge=UP)
        bullet5.next_to(bullet4, DOWN, buff=0.5, aligned_edge=LEFT)
        bullet5.scale_to_fit_width(12)

        self.play(FadeIn(bullet5), run_time=max(0.05, 1.0))

        # Gentle pulse on warning triangle (4 cycles, ~1.04s each)
        for _ in range(4):
            self.play(
                warning_icon.animate.scale(1.15).set_opacity(0.85),
                run_time=max(0.05, 0.25),
            )
            self.play(
                warning_icon.animate.scale(1 / 1.15).set_opacity(1),
                run_time=max(0.05, 0.25),
            )
            self.wait(max(0.05, 0.54))

        # ------------------------------------------------------------
        # Beat 8: 26.98–28.55  (duration 1.57)
        # No gap needed (beat 7 ends exactly at 26.98)
        self.wait(max(0.05, 1.07))  # 28.05
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=max(0.05, 0.5))  # 28.55

    # ------------------------------------------------------------------
    # Icon helpers
    def _make_fast_wave_icon(self, color):
        points = []
        n = 60
        for i in range(n + 1):
            t = i / n
            x = -0.5 + t
            y = 0.3 * np.sin(4 * 2 * np.pi * t)
            points.append(np.array([x, y, 0]))
        wave = VMobject(color=color, stroke_width=4)
        wave.set_points_as_corners(points)
        wave.set_stroke(color=color, width=3)
        return wave

    def _make_slow_wave_icon(self, color):
        points = []
        n = 60
        for i in range(n + 1):
            t = i / n
            x = -0.5 + t
            y = 0.3 * np.sin(1.0 * 2 * np.pi * t)
            points.append(np.array([x, y, 0]))
        wave = VMobject(color=color, stroke_width=4)
        wave.set_points_as_corners(points)
        wave.set_stroke(color=color, width=3)
        return wave

    def _make_square_wave_icon(self, color):
        n = 5
        verts = [np.array([-0.5, 0, 0])]
        period = 1.0 / n
        for i in range(n):
            x0 = -0.5 + i * period
            verts.append(np.array([x0 + period * 0.1, 0.3, 0]))
            verts.append(np.array([x0 + period * 0.6, 0.3, 0]))
            verts.append(np.array([x0 + period * 0.6, -0.3, 0]))
            verts.append(np.array([x0 + period, -0.3, 0]))
        sq = VMobject(color=color, stroke_width=4)
        sq.set_points_as_corners(verts)
        sq.set_stroke(color=color, width=3)
        return sq

    def _make_arrow_down_icon(self, color):
        arrow = Arrow(
            start=UP * 0.3,
            end=DOWN * 0.3,
            color=color,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.4,
            buff=0,
        )
        return arrow