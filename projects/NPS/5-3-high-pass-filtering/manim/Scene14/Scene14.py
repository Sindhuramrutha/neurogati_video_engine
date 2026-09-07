ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

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

from manim import *
import numpy as np


class Scene14(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Helper to build a filter box with label and arrow
        def make_filter_box(label_text, arrow_dir, fill_col, name_size=24):
            rect = Rectangle(width=3.5, height=1.8,
                             fill_color=fill_col, fill_opacity=0.2,
                             stroke_color=WHITE, stroke_width=2)
            label = Text(label_text, font_size=name_size, color=WHITE)
            # arrow icon: direction "up" or "down"
            if arrow_dir == "up":
                arrow = Arrow(start=ORIGIN + DOWN * 0.25,
                              end=ORIGIN + UP * 0.25,
                              color=WHITE, stroke_width=4,
                              max_tip_length_to_length_ratio=0.3)
            else:
                arrow = Arrow(start=ORIGIN + UP * 0.25,
                              end=ORIGIN + DOWN * 0.25,
                              color=WHITE, stroke_width=4,
                              max_tip_length_to_length_ratio=0.3)
            arrow.scale(0.7)
            content = VGroup(label, arrow).arrange(DOWN, buff=0.15)
            content.move_to(rect.get_center())
            box = VGroup(rect, content)
            return box, rect, label

        low_box, low_rect, low_label = make_filter_box(
            "Low-pass filter", "up", BLUE
        )
        high_box, high_rect, high_label = make_filter_box(
            "High-pass filter", "down", ORANGE
        )

        low_box.move_to(LEFT * 3 + UP * 2.5)
        high_box.move_to(RIGHT * 3 + UP * 2.5)

        # ------------------------------------------------------------
        # Beat 1: 0.00–1.30
        self.play(FadeIn(low_box, high_box), run_time=max(0.05, 1.30))
        self.wait(max(0.05, 3.54 - 1.30))  # 2.24

        # ------------------------------------------------------------
        # Beat 2: 3.54–5.48  (Low-pass brightens and pulses gently)
        self.play(
            low_rect.animate.set_fill(opacity=0.6),
            low_label.animate.set_color(YELLOW),
            run_time=max(0.05, 0.5)
        )
        self.play(low_box.animate.scale(1.05), run_time=max(0.05, 0.3))
        self.play(low_box.animate.scale(1 / 1.05), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 5.48 - 3.54 - 0.5 - 0.3 - 0.3))  # 0.84

        # ------------------------------------------------------------
        # Gap before beat 3
        self.wait(max(0.05, 6.14 - 5.48))  # 0.66

        # Beat 3: 6.14–8.22  (High-pass brightens, low-pass dims)
        self.play(
            low_rect.animate.set_fill(opacity=0.2),
            low_label.animate.set_color(WHITE),
            high_rect.animate.set_fill(opacity=0.6),
            high_label.animate.set_color(YELLOW),
            run_time=max(0.05, 0.5)
        )
        self.play(high_box.animate.scale(1.05), run_time=max(0.05, 0.3))
        self.play(high_box.animate.scale(1 / 1.05), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 8.22 - 6.14 - 0.5 - 0.3 - 0.3))  # 0.98

        # ------------------------------------------------------------
        # Gap before beat 4
        self.wait(max(0.05, 9.12 - 8.22))  # 0.90

        # Beat 4: 9.12–12.60  (Frequency spectrum appears)
        axis = Line(LEFT * 5, RIGHT * 5, color=WHITE, stroke_width=2)
        freq_label = Text("Frequency", font_size=24, color=WHITE)
        freq_label.next_to(axis, DOWN, buff=0.2)
        band_rect = Rectangle(
            width=10, height=1.0,
            fill_color=GREY_B, fill_opacity=0.5, stroke_width=0
        )
        band_rect.move_to(axis.get_center())
        spectrum_group = VGroup(axis, band_rect, freq_label)
        spectrum_group.move_to(DOWN * 0.5)  # below boxes

        self.play(FadeIn(spectrum_group), run_time=max(0.05, 3.48))

        # Prepare gray overlays (invisible, width 0)
        left_gray = Rectangle(
            width=0, height=1.2,
            fill_color=GREY, fill_opacity=0.6, stroke_width=0
        )
        left_gray.align_to(band_rect, LEFT)
        left_gray.set_y(band_rect.get_center()[1])
        right_gray = Rectangle(
            width=0, height=1.2,
            fill_color=GREY, fill_opacity=0.6, stroke_width=0
        )
        right_gray.align_to(band_rect, RIGHT)
        right_gray.set_y(band_rect.get_center()[1])
        self.add(left_gray, right_gray)

        # Gap to beat 5 (hold steady) + gap to beat 6
        self.wait(max(0.05, 14.96 - 12.60))  # 2.36

        # ------------------------------------------------------------
        # Beat 6: 14.96–18.10  (Gray overlays invade from edges)
        self.play(
            left_gray.animate.stretch_to_fit_width(3.5, about_edge=LEFT),
            right_gray.animate.stretch_to_fit_width(3.5, about_edge=RIGHT),
            run_time=max(0.05, 3.14)
        )

        # Gap before beat 7
        self.wait(max(0.05, 18.68 - 18.10))  # 0.58

        # ------------------------------------------------------------
        # Beat 7: 18.68–20.70  (Central band becomes bold and pulses)
        central_highlight = Rectangle(
            width=3, height=1.0,
            fill_color=TEAL, fill_opacity=1.0, stroke_width=0
        )
        central_highlight.move_to(band_rect.get_center())
        self.play(FadeIn(central_highlight), run_time=max(0.05, 0.4))
        # Gentle periodic glow: 2 cycles of scaling and opacity
        pulse_cycles = 2
        for _ in range(pulse_cycles):
            self.play(
                central_highlight.animate.scale(1.1).set_opacity(0.7),
                run_time=max(0.05, 0.4)
            )
            self.play(
                central_highlight.animate.scale(1 / 1.1).set_opacity(1.0),
                run_time=max(0.05, 0.4)
            )
        self.wait(max(0.05, 20.70 - 18.68 - 0.4 - 0.8 * pulse_cycles))

        # ------------------------------------------------------------
        # Gap before beat 8
        self.wait(max(0.05, 21.68 - 20.70))  # 0.98

        # Beat 8: 21.68–23.66  (Band-pass box appears, old boxes dim)
        band_rect_box = Rectangle(
            width=4.5, height=2.2,
            fill_color=TEAL, fill_opacity=0.3,
            stroke_color=WHITE, stroke_width=2
        )
        band_label = Text("Band-pass filter", font_size=32, color=WHITE)
        up_arrow = Arrow(
            start=ORIGIN + DOWN * 0.3, end=ORIGIN + UP * 0.3,
            color=WHITE, stroke_width=5, max_tip_length_to_length_ratio=0.3
        )
        down_arrow = Arrow(
            start=ORIGIN + UP * 0.3, end=ORIGIN + DOWN * 0.3,
            color=WHITE, stroke_width=5, max_tip_length_to_length_ratio=0.3
        )
        double_arrow = VGroup(up_arrow, down_arrow).arrange(RIGHT, buff=0.2).scale(0.7)
        band_content = VGroup(band_label, double_arrow).arrange(DOWN, buff=0.2)
        band_content.move_to(band_rect_box)
        band_pass_box = VGroup(band_rect_box, band_content)
        band_pass_box.move_to(DOWN * 2.5)  # below spectrum

        self.play(
            FadeIn(band_pass_box),
            low_box.animate.set_opacity(0.3),
            high_box.animate.set_opacity(0.3),
            run_time=max(0.05, 1.98)
        )

        # ------------------------------------------------------------
        # Gap before beat 9
        self.wait(max(0.05, 23.98 - 23.66))  # 0.32

        # Beat 9: 23.98–25.74  (Dim everything except band-pass)
        bg_group = VGroup(
            low_box, high_box, spectrum_group,
            left_gray, right_gray, central_highlight
        )
        self.play(
            bg_group.animate.set_opacity(0.2),
            band_pass_box.animate.scale(1.05).set_opacity(1.0),
            run_time=max(0.05, 1.76)
        )

        # ------------------------------------------------------------
        # Beat 10: 25.74–26.88  (Arrow + text, then fade out)
        transition_arrow = Arrow(
            LEFT * 2, RIGHT * 2, color=YELLOW,
            stroke_width=6, max_tip_length_to_length_ratio=0.3
        )
        transition_arrow.scale(0.9)
        transition_arrow.move_to(LEFT * 7.5 + band_pass_box.get_center() * 0)
        transition_arrow.set_y(band_pass_box.get_center()[1])
        self.add(transition_arrow)

        self.play(
            transition_arrow.animate.move_to(RIGHT * 7.5),
            run_time=max(0.05, 0.5)
        )  # 25.74 -> 26.24

        next_text = Text("Next: Section 5.4", font_size=28, color=WHITE)
        next_text.next_to(transition_arrow, DOWN, buff=0.4)
        self.play(FadeIn(next_text), run_time=max(0.05, 0.14))  # 26.38

        # Fade out everything smoothly over final 0.5 s
        self.play(FadeOut(*self.mobjects), run_time=max(0.05, 0.5))