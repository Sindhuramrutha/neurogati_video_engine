ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *
from manim import rate_functions

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # 1. MODULE 5 flies in from left
        module_label = Text("MODULE 5", font_size=54, color=GOLD, weight="BOLD")
        module_label.move_to(UP * 3.2)
        module_label.shift(LEFT * 10)
        self.play(
            module_label.animate.move_to(UP * 3.2),
            run_time=max(0.05, 0.52),
            rate_func=rate_functions.ease_out_elastic,
        )

        # 2. Hold module label
        self.wait(max(0.05, 0.42))
        self.wait(max(0.05, 0.58))

        # 3-5. Title words appear letter by letter
        word1 = Text("Filtering", font_size=36, color=WHITE)
        word2 = Text("Neural", font_size=36, color=WHITE)
        word3 = Text("Signals.", font_size=36, color=WHITE)
        VGroup(word1, word2, word3).arrange(RIGHT, buff=0.3).next_to(module_label, DOWN, buff=0.45)

        self.play(AddTextLetterByLetter(word1), run_time=max(0.05, 0.24))
        self.play(AddTextLetterByLetter(word2), run_time=max(0.05, 0.28))
        self.play(AddTextLetterByLetter(word3), run_time=max(0.05, 0.58))

        # Hold title before waveform
        self.wait(max(0.05, 0.78))

        # 6-7. Noisy jagged waveform draws left to right
        n_points = 600
        x = np.linspace(-6.2, 6.2, n_points)
        rng = np.random.default_rng(42)

        noisy_y = -0.2 + 0.55 * np.sin(0.9 * x) + 0.18 * np.sin(6.0 * x + 1.2)
        noisy_y += rng.normal(0, 0.22, x.size)
        spike_idx = rng.choice(x.size, size=10, replace=False)
        noisy_y[spike_idx] += rng.choice([-0.8, 0.8], size=10)

        noisy_pts = np.c_[x, noisy_y, np.zeros_like(x)]
        noisy_wave = VMobject(stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
        noisy_wave.set_points_as_corners(noisy_pts)

        # Smooth target waveform
        smooth_y = -0.2 + 0.75 * np.sin(0.9 * x)
        smooth_pts = np.c_[x, smooth_y, np.zeros_like(x)]
        smooth_wave = VMobject(stroke_color=GREEN, stroke_width=4, fill_opacity=0)
        smooth_wave.set_points_as_corners(smooth_pts)

        self.play(Create(noisy_wave), run_time=max(0.05, 1.36))

        # Wait before empty slots
        self.wait(max(0.05, 0.48))

        # 8. Four empty slots fade in
        slot_width = 1.6
        slot_height = 0.8
        slot_rects = VGroup(*[
            Rectangle(
                width=slot_width,
                height=slot_height,
                stroke_color=GREY_B,
                stroke_width=3,
                fill_color=BLACK,
                fill_opacity=0.4,
            )
            for _ in range(4)
        ])
        slot_rects.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=1.1)
        self.play(FadeIn(slot_rects), run_time=max(0.05, 0.24))

        # Card helper
        def make_filter_card(label, color):
            rect = Rectangle(
                width=slot_width,
                height=slot_height,
                fill_color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=2,
            )
            txt = Text(label, font_size=22, color=WHITE)
            return VGroup(rect, txt)

        # 9. Low-Pass card
        low_card = make_filter_card("Low-Pass", BLUE)
        low_card.move_to(slot_rects[0].get_center())
        self.play(GrowFromCenter(low_card), run_time=max(0.05, 0.30))
        self.play(
            Flash(low_card, color=YELLOW, line_length=0.2, num_lines=12, flash_radius=1.1),
            run_time=max(0.05, 0.14),
        )

        # Wait before High-Pass
        self.wait(max(0.05, 0.40))

        # 10. High-Pass card, low-pass dims
        high_card = make_filter_card("High-Pass", GREEN)
        high_card.move_to(slot_rects[1].get_center())
        self.play(GrowFromCenter(high_card), run_time=max(0.05, 0.20))
        self.play(
            Flash(high_card, color=YELLOW, line_length=0.2, num_lines=12, flash_radius=1.1),
            low_card.animate.set_opacity(0.65),
            run_time=max(0.05, 0.12),
        )

        # Wait before Band-Pass
        self.wait(max(0.05, 0.32))

        # 11. Band-Pass card, high-pass dims
        band_card = make_filter_card("Band-Pass", ORANGE)
        band_card.move_to(slot_rects[2].get_center())
        self.play(GrowFromCenter(band_card), run_time=max(0.05, 0.22))
        self.play(
            Flash(band_card, color=YELLOW, line_length=0.2, num_lines=12, flash_radius=1.1),
            high_card.animate.set_opacity(0.65),
            run_time=max(0.05, 0.14),
        )

        # Wait before Notch
        self.wait(max(0.05, 0.30))

        # 12. Notch card, band-pass dims
        notch_card = make_filter_card("Notch", PURPLE)
        notch_card.move_to(slot_rects[3].get_center())
        self.play(GrowFromCenter(notch_card), run_time=max(0.05, 0.14))
        self.play(
            Flash(notch_card, color=YELLOW, line_length=0.2, num_lines=12, flash_radius=1.1),
            band_card.animate.set_opacity(0.65),
            run_time=max(0.05, 0.10),
        )

        # 13. Hold all four dimmed cards and noisy waveform
        self.wait(max(0.05, 0.34))
        self.wait(max(0.05, 0.44))

        # 14-16. Morph noisy waveform into clean smooth wave
        self.play(
            Transform(noisy_wave, smooth_wave),
            run_time=max(0.05, 2.20),
            rate_func=rate_functions.smooth,
        )

        # 17. Hold waveform and cards
        self.wait(max(0.05, 1.06))

        # Brief hold before clear
        self.wait(max(0.05, 0.14))

        # 18. Clear waveform, cards, and title
        self.play(
            FadeOut(module_label),
            FadeOut(word1),
            FadeOut(word2),
            FadeOut(word3),
            FadeOut(noisy_wave),
            FadeOut(slot_rects),
            FadeOut(low_card),
            FadeOut(high_card),
            FadeOut(band_card),
            FadeOut(notch_card),
            run_time=max(0.05, 0.26),
        )

        # 19. "Let's get started!" bursts in
        lets_go = Text("Let's get started!", font_size=72, color=YELLOW, weight="BOLD")
        lets_go.move_to(ORIGIN)
        lets_go.scale(0.2)
        lets_go.set_opacity(0)

        self.play(lets_go.animate.scale(5).set_opacity(1), run_time=max(0.05, 0.30))
        self.play(
            Flash(lets_go, color=WHITE, line_length=0.3, num_lines=16, flash_radius=1.8),
            run_time=max(0.05, 0.14),
        )

        # 20. Hold to end
        self.wait(max(0.05, 0.73))