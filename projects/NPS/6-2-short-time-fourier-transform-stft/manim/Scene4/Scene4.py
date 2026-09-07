ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def wave_func(x):
            return 0.8 * np.sin(2.5 * x) * np.cos(0.35 * x) + 0.3 * np.sin(5.0 * x) + 0.15 * np.sin(1.2 * x)

        wave_min_x = -6.5
        wave_max_x = 6.5
        n_segments = 10
        seg_w = (wave_max_x - wave_min_x) / n_segments
        lefts = [wave_min_x + i * seg_w for i in range(n_segments)]

        def make_bright_seg(idx):
            left = lefts[idx]
            right = left + seg_w
            seg = FunctionGraph(wave_func, x_range=[left, right])
            seg.set_stroke(GOLD, width=12)
            return seg

        def make_spectrum(center_x):
            bars = VGroup()
            heights = [0.25, 0.55, 0.9, 0.7, 0.5, 0.35]
            bar_w = 0.16
            base_y = -2.0
            for k, h in enumerate(heights):
                bar = Rectangle(width=bar_w, height=h, fill_color=TEAL, fill_opacity=1, stroke_width=0)
                bar.move_to(np.array([center_x - 0.5 + k * bar_w * 1.35, base_y + h / 2, 0]))
                bars.add(bar)
            base = Line(
                start=np.array([center_x - 0.7, base_y, 0]),
                end=np.array([center_x + 0.7, base_y, 0]),
            ).set_stroke(color=GREY_B, width=2)
            return VGroup(base, bars)

        # 1. Full waveform
        wave = FunctionGraph(wave_func, x_range=[wave_min_x, wave_max_x])
        wave.set_stroke(WHITE, width=4)
        self.play(Create(wave), run_time=max(0.05, 1.8))
        self.wait(max(0.05, 0.82))

        # 2. First window and bright segment
        window_rect = Rectangle(width=seg_w, height=2.6, color=YELLOW, stroke_width=5)
        window_rect.move_to(np.array([lefts[0] + seg_w / 2, 0, 0]))
        seg1 = make_bright_seg(0)
        self.play(
            Create(window_rect),
            FadeIn(seg1),
            wave.animate.set_color(GREY).set_stroke(width=2),
            run_time=max(0.05, 1.8),
        )
        self.wait(max(0.05, 0.08))

        # 3. STFT label
        stft_label = Text("STFT", font_size=42, color=YELLOW).to_edge(UP, buff=0.4)
        self.play(Write(stft_label), run_time=max(0.05, 2.2))
        self.wait(max(0.05, 0.58))

        # 4. Full-wave flicker, then window divider
        self.play(wave.animate.set_color(WHITE).set_stroke(width=5), run_time=max(0.05, 0.5))
        self.play(wave.animate.set_color(GREY).set_stroke(width=2), run_time=max(0.05, 0.5))
        divider = Line(
            start=np.array([lefts[0], -1.3, 0]),
            end=np.array([lefts[0], 1.3, 0]),
        ).set_stroke(color=YELLOW, width=3, opacity=0.8)
        self.play(Create(divider), run_time=max(0.05, 1.06))
        self.wait(max(0.05, 0.42))

        # 5. First Fourier indicator
        spectrum1 = make_spectrum(lefts[0] + seg_w / 2)
        self.play(GrowFromCenter(spectrum1), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 0.76))
        self.wait(max(0.05, 1.02))

        # 6. Slight zoom out / whole signal neutral, window stays on first segment
        self.play(
            self.camera.frame.animate.scale(1.08),
            wave.animate.set_color(GREY).set_stroke(width=2),
            run_time=max(0.05, 2.28),
        )
        self.wait(max(0.05, 0.42))

        # 7. Refocus first windowed segment
        self.play(
            window_rect.animate.set_stroke(width=7, color=YELLOW, opacity=1),
            seg1.animate.set_stroke(width=14, color=GOLD),
            run_time=max(0.05, 1.5),
        )
        self.play(Indicate(seg1, scale_factor=1.1, color=YELLOW), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.48))
        self.wait(max(0.05, 0.64))

        # 8. Even more prominent first window
        self.play(
            window_rect.animate.set_stroke(width=12, color=WHITE, opacity=1),
            seg1.animate.set_stroke(width=16, color=GOLD),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 1.12))
        self.wait(max(0.05, 0.64))

        # 9. Interior pulse
        highlight_rect = Rectangle(
            width=window_rect.width,
            height=window_rect.height,
            fill_color=YELLOW,
            fill_opacity=0,
            stroke_width=0,
        )
        highlight_rect.move_to(window_rect.get_center())
        self.add(highlight_rect)
        self.play(highlight_rect.animate.set_fill(opacity=0.5), run_time=max(0.05, 0.9))
        self.play(highlight_rect.animate.set_fill(opacity=0.0), run_time=max(0.05, 0.9))
        self.wait(max(0.05, 0.5))
        self.remove(highlight_rect)
        self.wait(max(0.05, 0.96))

        # 10. Slide window right by one segment
        seg2 = make_bright_seg(1)
        self.play(
            window_rect.animate.shift(RIGHT * seg_w),
            divider.animate.shift(RIGHT * seg_w),
            FadeOut(seg1),
            FadeIn(seg2),
            FadeOut(spectrum1),
            run_time=max(0.05, 1.7),
        )
        self.wait(max(0.05, 0.62))
        self.remove(seg1)
        self.remove(spectrum1)
        current_bright = seg2
        current_index = 1
        self.wait(max(0.05, 0.58))

        # 11. Pulse new window, second Fourier indicator briefly
        spectrum2 = make_spectrum(lefts[current_index] + seg_w / 2)
        self.play(Indicate(window_rect, color=YELLOW, scale_factor=1.1), run_time=max(0.05, 0.45))
        self.play(GrowFromCenter(spectrum2), run_time=max(0.05, 0.55))
        self.play(FadeOut(spectrum2), run_time=max(0.05, 0.30))
        self.remove(spectrum2)
        self.wait(max(0.05, 0.86))

        # 12. Step window rightward to the far end
        n_moves = 8
        normal_t = 0.42
        final_t = 3.66 - normal_t * (n_moves - 1)

        for move_num in range(n_moves):
            target_idx = current_index + 1
            target_bright = make_bright_seg(target_idx)

            if move_num < n_moves - 1:
                slide_t = 0.20
                pulse_t = 0.12
                end_wait = normal_t - slide_t - pulse_t

                self.play(
                    window_rect.animate.shift(RIGHT * seg_w),
                    divider.animate.shift(RIGHT * seg_w),
                    FadeOut(current_bright),
                    FadeIn(target_bright),
                    run_time=max(0.05, slide_t),
                )
                self.play(Indicate(window_rect, color=YELLOW, scale_factor=1.08), run_time=max(0.05, pulse_t))
                self.wait(max(0.05, end_wait))
                self.remove(current_bright)
                current_bright = target_bright
                current_index = target_idx
            else:
                slide_t = 0.28
                pulse_t = 0.12
                dim_t = 0.12
                fade_t = 0.20

                self.play(
                    window_rect.animate.shift(RIGHT * seg_w),
                    divider.animate.shift(RIGHT * seg_w),
                    FadeOut(current_bright),
                    FadeIn(target_bright),
                    run_time=max(0.05, slide_t),
                )
                self.play(Indicate(window_rect, color=YELLOW, scale_factor=1.08), run_time=max(0.05, pulse_t))
                self.play(
                    wave.animate.set_color(GREY).set_stroke(width=1.5),
                    target_bright.animate.set_stroke(width=16, color=WHITE),
                    run_time=max(0.05, dim_t),
                )
                self.play(
                    FadeOut(window_rect),
                    FadeOut(divider),
                    FadeOut(target_bright),
                    run_time=max(0.05, fade_t),
                )
                self.remove(current_bright)
                current_bright = target_bright
                current_index = target_idx

        # 13. Restore full uniform waveform, fade STFT label
        self.play(
            wave.animate.set_color(WHITE).set_stroke(width=4),
            FadeOut(stft_label),
            run_time=max(0.05, 0.77),
        )