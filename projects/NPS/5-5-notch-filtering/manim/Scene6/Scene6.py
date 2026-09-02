ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helper: build a filled balance pan ----------
        def make_pan(width_top=1.7, height=0.65, width_bottom=1.0, color=GREY_B):
            vertices = [
                np.array([-width_top / 2, height / 2, 0]),
                np.array([width_top / 2, height / 2, 0]),
                np.array([width_bottom / 2, -height / 2, 0]),
                np.array([-width_bottom / 2, -height / 2, 0]),
            ]
            return Polygon(
                *vertices,
                fill_color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1.5,
            )

        # ---------- scale geometry ----------
        beam_y = 2.0
        beam_half = 3.0
        pan_top_y = -0.3

        base = Line(
            LEFT * 1.2 + DOWN * 2.8,
            RIGHT * 1.2 + DOWN * 2.8,
            color=GREY_B,
            stroke_width=8,
        )
        pivot = Line(
            DOWN * 2.8,
            UP * beam_y,
            color=GREY_B,
            stroke_width=8,
        )
        beam = Line(
            LEFT * beam_half + UP * beam_y,
            RIGHT * beam_half + UP * beam_y,
            color=GREY_B,
            stroke_width=10,
        )
        pivot_dot = Dot(UP * beam_y, radius=0.12, color=YELLOW, fill_opacity=1)

        left_pan = make_pan(color=GREY_B)
        left_pan.shift(np.array([-beam_half, pan_top_y, 0]) - left_pan.get_top())
        right_pan = make_pan(color=GREY_B)
        right_pan.shift(np.array([beam_half, pan_top_y, 0]) - right_pan.get_top())

        left_chain1 = Line(beam.get_left(), left_pan.get_corner(UL), color=GREY, stroke_width=2)
        left_chain2 = Line(beam.get_left(), left_pan.get_corner(UR), color=GREY, stroke_width=2)
        right_chain1 = Line(beam.get_right(), right_pan.get_corner(UL), color=GREY, stroke_width=2)
        right_chain2 = Line(beam.get_right(), right_pan.get_corner(UR), color=GREY, stroke_width=2)

        left_label = Text("Advantages", font_size=30, color=GREEN, weight="BOLD")
        left_label.next_to(left_pan, DOWN, buff=0.3)
        right_label = Text("Limitations", font_size=30, color=RED, weight="BOLD")
        right_label.next_to(right_pan, DOWN, buff=0.3)

        scale_group = VGroup(
            base,
            pivot,
            beam,
            pivot_dot,
            left_chain1,
            left_chain2,
            right_chain1,
            right_chain2,
            left_pan,
            right_pan,
            left_label,
            right_label,
        )
        scale_group.move_to(ORIGIN)

        # ---------- 0.00 - 1.98: balance scale fades in ----------
        self.play(FadeIn(scale_group), run_time=max(0.05, 1.98))

        # ---------- gap to 2.78 ----------
        self.wait(max(0.05, 0.8))

        # ---------- spectral icon on left pan ----------
        axis_line = Line(LEFT * 0.7, RIGHT * 0.7, color=WHITE, stroke_width=2)
        spike = Polygon(
            np.array([-0.12, 0, 0]),
            np.array([0.12, 0, 0]),
            np.array([0, 0.6, 0]),
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
        )
        f0_label = Text("f₀", font_size=22, color=YELLOW)
        f0_label.next_to(axis_line.get_center(), DOWN, buff=0.15)

        spectral_icon = VGroup(axis_line, spike, f0_label)
        spectral_icon.scale_to_fit_width(1.4)
        spectral_icon.next_to(left_pan, UP, buff=0.15)

        # ---------- 2.78 - 4.20: spectral icon appears ----------
        self.play(Write(spectral_icon), run_time=max(0.05, 1.42))

        # ---------- 4.20 - 5.14: shaded notch band drops over spike ----------
        notch_band = Rectangle(
            width=0.5,
            height=0.85,
            fill_color=RED,
            fill_opacity=0.55,
            stroke_color=RED,
            stroke_width=2,
        )
        notch_band.move_to(spike.get_center() + UP * 1.2)

        self.play(notch_band.animate.move_to(spike.get_center()), run_time=max(0.05, 0.94))

        # ---------- hold the visual with gentle motion for the remaining narration ----------
        remaining = 39.40 - self.renderer.time
        cycle = 4.0
        cycles = int(remaining // cycle)
        rest = remaining - cycles * cycle

        for _ in range(cycles):
            self.play(notch_band.animate.set_opacity(0.25), run_time=max(0.05, 2.0))
            self.play(notch_band.animate.set_opacity(0.55), run_time=max(0.05, 2.0))

        if rest > 0.05:
            self.wait(max(0.05, rest))