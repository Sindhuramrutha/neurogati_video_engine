ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        centers = [
            np.array([-4.4, 0, 0]),
            np.array([0, 0, 0]),
            np.array([4.4, 0, 0]),
        ]
        active_shift = np.array([0, 0.32, 0])
        step_shift = np.array([0, -0.20, 0])

        card_width = 3.8
        card_height = 3.4

        # Three blank card outlines, initially invisible so they can fade to faint.
        rects = []
        for center in centers:
            rect = Rectangle(
                width=card_width,
                height=card_height,
                stroke_color=GREY_B,
                stroke_width=3,
                fill_color=GREY_B,
                fill_opacity=0.35,
            )
            rect.move_to(center)
            rect.set_opacity(0)
            rects.append(rect)

        rect1, rect2, rect3 = rects
        card_rects = VGroup(rect1, rect2, rect3)

        # Icon 1: circled question mark.
        q_circle = Circle(radius=0.55, color=YELLOW, stroke_width=5)
        q_mark = Text("?", font_size=48, color=YELLOW)
        icon1 = VGroup(q_circle, q_mark)

        label1 = Text(
            "Why filtering\nis necessary.",
            font_size=30,
            color=WHITE,
            line_spacing=0.8,
            t2c={"necessary": YELLOW},
        )
        label1.scale_to_fit_width(3.3)
        label1.next_to(icon1, DOWN, buff=0.2)
        content1 = VGroup(icon1, label1)
        content1.move_to(centers[0] + active_shift)

        # Icon 2: smooth wave overlaid with jagged noise.
        smooth = VMobject()
        xs_s = np.linspace(-1.1, 1.1, 100)
        ys_s = 0.35 * np.sin(2 * PI * 1.2 * xs_s)
        smooth.set_points_as_corners(
            np.stack([xs_s, ys_s, np.zeros_like(xs_s)], axis=1)
        )
        smooth.set_stroke(GREEN, width=5)

        jagged = VMobject()
        jagged_pts = [
            np.array([-1.1, 0.18, 0]),
            np.array([-0.8, -0.30, 0]),
            np.array([-0.45, 0.22, 0]),
            np.array([-0.1, -0.28, 0]),
            np.array([0.2, 0.32, 0]),
            np.array([0.5, -0.22, 0]),
            np.array([0.75, 0.36, 0]),
            np.array([1.1, -0.12, 0]),
        ]
        jagged.set_points_as_corners(jagged_pts)
        jagged.set_stroke(ORANGE, width=4)

        icon2 = VGroup(smooth, jagged)
        label2 = Text(
            "Signal vs. noise.",
            font_size=30,
            color=WHITE,
            t2c={"noise": ORANGE},
        )
        label2.scale_to_fit_width(3.3)
        label2.next_to(icon2, DOWN, buff=0.2)
        content2 = VGroup(icon2, label2)
        content2.move_to(centers[1] + active_shift)

        # Icon 3: waveform passing through a filter/funnel symbol.
        funnel = Polygon(
            np.array([-0.95, 0.95, 0]),
            np.array([0.95, 0.95, 0]),
            np.array([0.32, -0.95, 0]),
            np.array([-0.32, -0.95, 0]),
            stroke_color=TEAL,
            stroke_width=5,
            fill_color=TEAL,
            fill_opacity=0.25,
        )
        xs_f = np.linspace(-0.75, 0.75, 80)
        ys_f = 0.22 * np.sin(2 * PI * 1.6 * xs_f)
        wave = VMobject()
        wave.set_points_as_corners(
            np.stack([xs_f, ys_f, np.zeros_like(xs_f)], axis=1)
        )
        wave.set_stroke(YELLOW, width=4)

        icon3 = VGroup(funnel, wave)
        label3 = Text(
            "Purpose of filtering\nin neural processing.",
            font_size=30,
            color=WHITE,
            line_spacing=0.8,
        )
        label3.scale_to_fit_width(3.3)
        label3.next_to(icon3, DOWN, buff=0.2)
        content3 = VGroup(icon3, label3)
        content3.move_to(centers[2] + active_shift)

        # Beat 1: three faint, blank cards.
        self.add(card_rects)
        self.play(card_rects.animate.set_opacity(0.38), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 0.36))  # to 1.26
        self.wait(max(0.05, 0.56))  # to 1.82

        # Beat 2: first card brightens and gains icon + label.
        self.play(
            rect1.animate.set_opacity(1).move_to(centers[0] + active_shift),
            run_time=max(0.05, 0.60),
        )
        self.play(FadeIn(content1, shift=UP * 0.15), run_time=max(0.05, 0.54))

        # Beat 3: emphasize "necessary".
        self.wait(max(0.05, 0.40))  # to 3.36
        self.play(Indicate(label1, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.48))  # to 4.84

        # Beat 4: second card brightens, first steps back.
        self.wait(max(0.05, 0.56))  # to 5.40
        self.play(
            rect1.animate.set_opacity(0.55).move_to(centers[0] + step_shift),
            content1.animate.set_opacity(0.55).move_to(centers[0] + step_shift),
            rect2.animate.set_opacity(1).move_to(centers[1] + active_shift),
            run_time=max(0.05, 0.98),
        )
        self.play(FadeIn(content2, shift=UP * 0.15), run_time=max(0.05, 1.00))

        # Beat 5: emphasize unwanted noise.
        self.wait(max(0.05, 0.46))  # to 7.84
        self.play(Indicate(jagged, color=ORANGE, scale_factor=1.2), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.28))  # to 8.72

        # Beat 6: third card brightens, first two step back.
        self.wait(max(0.05, 0.52))  # to 9.24
        self.play(
            rect1.animate.set_opacity(0.45).move_to(centers[0] + step_shift),
            content1.animate.set_opacity(0.45).move_to(centers[0] + step_shift),
            rect2.animate.set_opacity(0.45).move_to(centers[1] + step_shift),
            content2.animate.set_opacity(0.45).move_to(centers[1] + step_shift),
            rect3.animate.set_opacity(1).move_to(centers[2] + active_shift),
            run_time=max(0.05, 0.80),
        )
        self.play(FadeIn(content3, shift=UP * 0.15), run_time=max(0.05, 0.70))

        # Beat 7: all three cards aligned, fully visible.
        self.wait(max(0.05, 0.42))  # to 11.16
        self.play(
            rect1.animate.set_opacity(1).move_to(centers[0]),
            content1.animate.set_opacity(1).move_to(centers[0]),
            rect2.animate.set_opacity(1).move_to(centers[1]),
            content2.animate.set_opacity(1).move_to(centers[1]),
            rect3.animate.set_opacity(1).move_to(centers[2]),
            content3.animate.set_opacity(1).move_to(centers[2]),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.40))  # to 12.76

        # Beat 8: smooth fade out.
        self.play(
            FadeOut(card_rects, content1, content2, content3),
            run_time=max(0.05, 0.84),
        )