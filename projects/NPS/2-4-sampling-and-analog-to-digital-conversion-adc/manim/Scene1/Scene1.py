ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Title
        # ------------------------------------------------------------------
        title = Text("Learning Objectives", color=WHITE, font_size=40)
        title.to_edge(UP, buff=0.55)

        # ------------------------------------------------------------------
        # Icon builders
        # ------------------------------------------------------------------
        def make_wave_icon():
            smooth = VMobject()
            smooth.set_points_as_corners([
                [x, 0.30 * np.sin(3.0 * x), 0.0]
                for x in np.linspace(-0.60, 0.60, 80)
            ])
            smooth.set_stroke(BLUE, width=4)

            stair = VMobject()
            stair.set_points_as_corners([
                [-0.60, -0.25, 0.0],
                [-0.20, -0.25, 0.0],
                [-0.20,  0.20, 0.0],
                [ 0.20,  0.20, 0.0],
                [ 0.20, -0.10, 0.0],
                [ 0.60, -0.10, 0.0],
            ])
            stair.set_stroke(ORANGE, width=4)

            icon = VGroup(smooth, stair).arrange(RIGHT, buff=0.15)
            icon.scale_to_fit_height(0.55)
            return icon

        def make_dotgrid_icon():
            dots = VGroup(*[
                Dot(radius=0.055, color=YELLOW, fill_opacity=1.0)
                for _ in range(9)
            ])
            dots.arrange_in_grid(rows=3, cols=3, buff=0.22)
            dots.scale_to_fit_height(0.60)
            return dots

        def make_frequency_icon():
            axis = Line(
                np.array([-0.6, 0.0, 0.0]),
                np.array([0.6, 0.0, 0.0]),
                color=WHITE,
                stroke_width=3,
            )
            ticks = VGroup()
            for x in np.linspace(-0.6, 0.6, 5):
                ticks.add(Line(
                    np.array([x, 0.0, 0.0]),
                    np.array([x, 0.30, 0.0]),
                    color=TEAL,
                    stroke_width=3,
                ))
            icon = VGroup(axis, ticks)
            icon.scale_to_fit_height(0.55)
            return icon

        def make_chip_icon():
            body = Rectangle(
                width=0.75,
                height=0.60,
                fill_color=BLACK,
                fill_opacity=1.0,
                stroke_color=BLUE,
                stroke_width=2,
            )
            pins = VGroup()
            for y in np.linspace(-0.20, 0.20, 4):
                left_x = body.get_left()[0]
                right_x = body.get_right()[0]
                pins.add(Line(
                    np.array([left_x - 0.20, y, 0.0]),
                    np.array([left_x, y, 0.0]),
                    color=GOLD,
                    stroke_width=2,
                ))
                pins.add(Line(
                    np.array([right_x, y, 0.0]),
                    np.array([right_x + 0.20, y, 0.0]),
                    color=GOLD,
                    stroke_width=2,
                ))
            icon = VGroup(body, pins)
            icon.scale_to_fit_height(0.55)
            return icon

        def make_check_icon():
            line1 = Line(
                np.array([-0.35, 0.00, 0.0]),
                np.array([-0.05, 0.30, 0.0]),
                color=GREEN,
                stroke_width=5,
            )
            line2 = Line(
                np.array([-0.05, 0.30, 0.0]),
                np.array([0.40, -0.25, 0.0]),
                color=GREEN,
                stroke_width=5,
            )
            icon = VGroup(line1, line2)
            icon.scale_to_fit_height(0.55)
            return icon

        # ------------------------------------------------------------------
        # Bullet rows
        # ------------------------------------------------------------------
        def make_bullet_text(txt):
            t = Text(txt, color=WHITE, font_size=28)
            if t.width > 10.8:
                t.scale_to_fit_width(10.8)
            return t

        def make_bullet(icon, txt):
            t = make_bullet_text(txt)
            row = VGroup(icon, t).arrange(RIGHT, buff=0.35)
            return row

        bullet1 = make_bullet(
            make_wave_icon(),
            "differentiate between analog and digital signals"
        )
        bullet2 = make_bullet(
            make_dotgrid_icon(),
            "explain the concept of sampling"
        )
        bullet3 = make_bullet(
            make_frequency_icon(),
            "define sampling frequency"
        )
        bullet4 = make_bullet(
            make_chip_icon(),
            "describe the role of an analog-to-digital converter"
        )
        bullet5 = make_bullet(
            make_check_icon(),
            "understand why proper sampling is important for accurate neural signal recording"
        )

        bullets = VGroup(bullet1, bullet2, bullet3, bullet4, bullet5)
        bullets.arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        bullets.next_to(title, DOWN, buff=0.65)

        # ------------------------------------------------------------------
        # Beat 1: title
        # ------------------------------------------------------------------
        self.play(FadeIn(title), run_time=max(0.05, 1.30))
        self.wait(max(0.05, 0.54))

        # ------------------------------------------------------------------
        # Beat 2: first bullet
        # ------------------------------------------------------------------
        self.play(FadeIn(bullet1), run_time=max(0.05, 1.20))
        self.play(bullet1[0].animate.scale(1.08), run_time=max(0.05, 0.40))
        self.play(bullet1[0].animate.scale(1 / 1.08), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 2.54))

        # ------------------------------------------------------------------
        # Beat 3: second bullet
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.34))
        self.play(FadeIn(bullet2), run_time=max(0.05, 0.90))
        self.play(bullet2[0].animate.scale(1.08), run_time=max(0.05, 0.25))
        self.play(bullet2[0].animate.scale(1 / 1.08), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.24))

        # ------------------------------------------------------------------
        # Beat 4: third bullet
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.62))
        self.play(FadeIn(bullet3), run_time=max(0.05, 0.70))
        self.play(bullet3[0].animate.scale(1.08), run_time=max(0.05, 0.20))
        self.play(bullet3[0].animate.scale(1 / 1.08), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.12))

        # ------------------------------------------------------------------
        # Beat 5: fourth bullet
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.80))
        self.play(FadeIn(bullet4), run_time=max(0.05, 1.00))
        self.play(bullet4[0].animate.scale(1.08), run_time=max(0.05, 0.30))
        self.play(bullet4[0].animate.scale(1 / 1.08), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.88))

        # ------------------------------------------------------------------
        # Beat 6: fifth bullet
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.88))
        self.play(FadeIn(bullet5), run_time=max(0.05, 1.00))
        self.play(bullet5[0].animate.scale(1.08), run_time=max(0.05, 0.40))
        self.play(bullet5[0].animate.scale(1 / 1.08), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 2.66))

        # ------------------------------------------------------------------
        # Beat 7: hold final composition
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.80))