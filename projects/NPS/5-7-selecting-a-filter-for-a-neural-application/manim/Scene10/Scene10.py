ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene10(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        np.random.seed(7)

        def make_x(color=RED, height=0.7):
            return SVGMobject(
                ASSET_PATHS["x_circle"],
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
                height=height,
            )

        def make_check(color=GREEN, height=0.7):
            return SVGMobject(
                ASSET_PATHS["check_circle"],
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
                height=height,
            )

        def make_wave(sig, color, width=3.0, height=1.0, stroke_width=3):
            n = len(sig)
            x = np.linspace(-width / 2, width / 2, n)
            y = sig - np.mean(sig)
            y = y / (np.max(np.abs(y)) * 1.1 + 1e-12) * height / 2
            points = [np.array([x[i], y[i], 0]) for i in range(n)]
            trace = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
            trace.set_points_as_corners(points)
            return trace

        def make_spectrum(amp, color, width=4.6, height=1.5, stroke_width=3):
            n = len(amp)
            x = np.linspace(-width / 2, width / 2, n)
            y = amp - np.min(amp)
            y = y / (np.max(y) * 1.1 + 1e-12) * height
            y = y - height / 2
            points = [np.array([x[i], y[i], 0]) for i in range(n)]
            trace = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
            trace.set_points_as_corners(points)
            return trace

        # Beat 1: clean sinusoid
        n_pts = 400
        t_vis = np.linspace(0, 2, n_pts)
        clean_sig = 0.9 * np.sin(2 * np.pi * 2 * t_vis)
        noisy_sig = clean_sig + 0.55 * np.random.randn(n_pts)

        clean_wave = make_wave(clean_sig, BLUE, width=5.5, height=2.2, stroke_width=4)
        noisy_wave = make_wave(noisy_sig, ORANGE, width=5.5, height=2.2, stroke_width=4)
        large_cross = make_x(RED, 1.4).move_to(ORIGIN)

        self.add(clean_wave)
        self.wait(max(0.05, 1.64))

        # Beat 2: distort + red cross
        self.play(Transform(clean_wave, noisy_wave), FadeIn(large_cross), run_time=max(0.05, 0.76))

        # Beat 3: fade out distorted wave and cross
        self.play(FadeOut(clean_wave), FadeOut(large_cross), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.12))

        # Beat 4: title + bullet placeholders
        title_icon = make_x(RED, 0.65)
        title_text = Text("Common mistakes:", font_size=38, color=WHITE, weight=BOLD)
        title_group = VGroup(title_icon, title_text).arrange(RIGHT, buff=0.2)
        title_group.to_corner(UL, buff=0.4)

        mistakes = [
            "applying filters without first identifying the noise source",
            "choosing cutoff frequencies that accidentally remove useful physiological information",
            "over-filtering to the point of distorting waveforms",
            "using a notch filter when there's no power-line interference present",
            "assuming one filter is suitable for every recording",
        ]

        rows = []
        for mistake in mistakes:
            bullet_icon = make_x(RED, 0.34)
            mistake_text = Text(mistake, font_size=19, color=WHITE)
            if mistake_text.width > 4.6:
                mistake_text.scale_to_fit_width(4.6)
            mistake_text.next_to(bullet_icon, RIGHT, buff=0.15)
            mistake_text.set_opacity(0)
            rows.append(VGroup(bullet_icon, mistake_text))

        list_group = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        list_group.next_to(title_group, DOWN, aligned_edge=LEFT, buff=0.4)

        self.play(FadeIn(title_group, shift=UP * 0.2), run_time=max(0.05, 0.4))
        self.play(FadeIn(list_group, shift=UP * 0.2), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.12))

        # Right-side panel background
        panel_bg = Rectangle(
            width=6.4,
            height=4.4,
            stroke_color=GREY,
            stroke_width=2,
            fill_color=GREY,
            fill_opacity=0.15,
        ).move_to(np.array([3.0, 0.2, 0]))

        # Beat 5: mistake 1 — wrong filter, 60 Hz noise
        raw1 = (
            0.4 * np.sin(2 * np.pi * 2 * t_vis)
            + 0.9 * np.sin(2 * np.pi * 60 * t_vis)
            + 0.08 * np.random.randn(n_pts)
        )
        bad1 = (
            0.4 * np.sin(2 * np.pi * 2 * t_vis)
            + 0.7 * np.sin(2 * np.pi * 60 * t_vis)
            + 0.5 * np.random.randn(n_pts)
        )

        left_box1 = Rectangle(width=2.7, height=1.8, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.1)
        left_box1.move_to(panel_bg.get_center() + LEFT * 1.5 + DOWN * 0.2)
        right_box1 = Rectangle(width=2.7, height=1.8, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.1)
        right_box1.move_to(panel_bg.get_center() + RIGHT * 1.5 + DOWN * 0.2)

        raw_label1 = Text("Raw: 60 Hz noise", font_size=16, color=WHITE).next_to(left_box1, DOWN, buff=0.1)
        bad_label1 = Text("After wrong filter", font_size=16, color=RED).next_to(right_box1, DOWN, buff=0.1)

        left_wave1 = make_wave(raw1, BLUE, width=2.5, height=1.4).move_to(left_box1)
        right_wave1 = make_wave(bad1, ORANGE, width=2.5, height=1.4).move_to(right_box1)
        bad_cross1 = make_x(RED, 0.7).next_to(right_box1, UP, buff=0.1)

        panel_structure1 = VGroup(left_box1, raw_label1, right_box1, bad_label1)
        panel_waves1 = VGroup(left_wave1, right_wave1, bad_cross1)
        current_panel_content = VGroup(panel_structure1, panel_waves1)

        first_text = rows[0][1]
        first_text.shift(LEFT * 2.5)
        self.play(
            first_text.animate.shift(RIGHT * 2.5).set_opacity(1),
            FadeIn(panel_bg),
            FadeIn(panel_structure1),
            run_time=max(0.05, 1.0),
        )
        self.play(Create(left_wave1), Create(right_wave1), FadeIn(bad_cross1), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 1.58))

        # Beat 6: mistake 2 — cutoff removes physiological information
        spike_raw = 0.05 * np.random.randn(n_pts)
        for c in [0.4, 0.8, 1.2, 1.6]:
            spike_raw += 1.8 * np.exp(-((t_vis - c) / 0.008) ** 2)
        spike_bad = np.convolve(spike_raw, np.ones(55) / 55, mode="same")
        spike_good = np.convolve(spike_raw, np.ones(3) / 3, mode="same")

        box2 = Rectangle(width=4.8, height=2.0, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.1)
        box2.move_to(panel_bg.get_center() + UP * 0.3)

        raw_label2 = Text("Raw: spike train", font_size=16, color=WHITE).next_to(box2, DOWN, buff=0.15)
        raw_spk_wave = make_wave(spike_raw, BLUE, width=4.4, height=1.5).move_to(box2)
        bad_spk_wave = make_wave(spike_bad, RED, width=4.4, height=1.5).move_to(box2)
        good_spk_wave = make_wave(spike_good, GREEN, width=4.4, height=1.5).move_to(box2)

        bad_label2 = Text("Low-pass filtered (peaks lost)", font_size=16, color=RED).move_to(raw_label2)
        good_label2 = Text("Correctly filtered (peaks preserved)", font_size=16, color=GREEN).move_to(raw_label2)
        bad_cross2 = make_x(RED, 0.7).next_to(box2, UP, buff=0.1)
        good_check2 = make_check(GREEN, 0.7).next_to(box2, UP, buff=0.1)

        second_text = rows[1][1]
        second_text.shift(LEFT * 2.5)
        self.play(
            second_text.animate.shift(RIGHT * 2.5).set_opacity(1),
            FadeOut(current_panel_content),
            run_time=max(0.05, 1.0),
        )

        self.play(FadeIn(box2), FadeIn(raw_label2), Create(raw_spk_wave), run_time=max(0.05, 1.0))
        self.play(
            Transform(raw_spk_wave, bad_spk_wave),
            FadeOut(raw_label2),
            FadeIn(bad_label2),
            FadeIn(bad_cross2),
            run_time=max(0.05, 1.4),
        )
        self.play(
            Transform(raw_spk_wave, good_spk_wave),
            FadeOut(bad_label2),
            FadeIn(good_label2),
            FadeOut(bad_cross2),
            FadeIn(good_check2),
            run_time=max(0.05, 1.4),
        )
        self.wait(max(0.05, 0.34))
        current_panel_content = VGroup(box2, raw_spk_wave, good_label2, good_check2)

        # Beat 7: mistake 3 — over-filtering distortion
        ecg_clean = 0.08 * np.sin(2 * np.pi * 0.8 * t_vis)
        for c in [0.5, 1.5]:
            ecg_clean += 1.4 * np.exp(-((t_vis - c) / 0.015) ** 2)
            ecg_clean += 0.3 * np.exp(-((t_vis - (c + 0.25)) / 0.04) ** 2)
            ecg_clean += 0.18 * np.exp(-((t_vis - (c - 0.25)) / 0.04) ** 2)
        ecg_raw = ecg_clean + 0.08 * np.random.randn(n_pts)
        ecg_bad = np.convolve(ecg_raw, np.ones(80) / 80, mode="same")
        ecg_good = ecg_clean

        box3 = Rectangle(width=4.8, height=2.0, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.1)
        box3.move_to(panel_bg.get_center() + UP * 0.3)

        raw_label3 = Text("Raw ECG", font_size=16, color=WHITE).next_to(box3, DOWN, buff=0.15)
        raw_ecg_wave = make_wave(ecg_raw, BLUE, width=4.4, height=1.5).move_to(box3)
        bad_ecg_wave = make_wave(ecg_bad, RED, width=4.4, height=1.5).move_to(box3)
        good_ecg_wave = make_wave(ecg_good, GREEN, width=4.4, height=1.5).move_to(box3)

        bad_label3 = Text("Over-smoothed (distorted)", font_size=16, color=RED).move_to(raw_label3)
        good_label3 = Text("Correctly filtered (natural shape)", font_size=16, color=GREEN).move_to(raw_label3)
        bad_cross3 = make_x(RED, 0.7).next_to(box3, UP, buff=0.1)
        good_check3 = make_check(GREEN, 0.7).next_to(box3, UP, buff=0.1)

        third_text = rows[2][1]
        third_text.shift(LEFT * 2.5)
        self.play(
            third_text.animate.shift(RIGHT * 2.5).set_opacity(1),
            FadeOut(current_panel_content),
            run_time=max(0.05, 0.8),
        )

        self.play(FadeIn(box3), FadeIn(raw_label3), Create(raw_ecg_wave), run_time=max(0.05, 0.6))
        self.play(
            Transform(raw_ecg_wave, bad_ecg_wave),
            FadeOut(raw_label3),
            FadeIn(bad_label3),
            FadeIn(bad_cross3),
            run_time=max(0.05, 0.7),
        )
        self.play(
            Transform(raw_ecg_wave, good_ecg_wave),
            FadeOut(bad_label3),
            FadeIn(good_label3),
            FadeOut(bad_cross3),
            FadeIn(good_check3),
            run_time=max(0.05, 0.68),
        )
        current_panel_content = VGroup(box3, raw_ecg_wave, good_label3, good_check3)

        # Beat 8: mistake 4 — unnecessary notch filter
        freq_axis = np.linspace(0, 100, 500)
        bio_amp = 0.15 + 0.0 * freq_axis
        for center in [10, 22, 38, 65]:
            bio_amp += 0.9 * np.exp(-((freq_axis - center) / 2.5) ** 2)
        notch_amp = bio_amp * (1 - 0.92 * np.exp(-((freq_axis - 50) / 2.0) ** 2))

        box4 = Rectangle(width=4.8, height=2.0, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.1)
        box4.move_to(panel_bg.get_center() + UP * 0.3)

        raw_label4 = Text("Biological spectrum", font_size=16, color=WHITE).next_to(box4, DOWN, buff=0.15)
        raw_spec_wave = make_spectrum(bio_amp, BLUE, width=4.6, height=1.6).move_to(box4)
        bad_spec_wave = make_spectrum(notch_amp, RED, width=4.6, height=1.6).move_to(box4)

        bad_label4 = Text("Notch applied at 50 Hz (gap)", font_size=16, color=RED).move_to(raw_label4)
        bad_cross4 = make_x(RED, 0.7).next_to(box4, UP, buff=0.1)

        fourth_text = rows[3][1]
        fourth_text.shift(LEFT * 2.5)
        self.play(
            fourth_text.animate.shift(RIGHT * 2.5).set_opacity(1),
            FadeOut(current_panel_content),
            run_time=max(0.05, 0.8),
        )

        self.play(FadeIn(box4), FadeIn(raw_label4), Create(raw_spec_wave), run_time=max(0.05, 1.2))
        self.play(
            Transform(raw_spec_wave, bad_spec_wave),
            FadeOut(raw_label4),
            FadeIn(bad_label4),
            FadeIn(bad_cross4),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 0.82))
        current_panel_content = VGroup(box4, raw_spec_wave, bad_label4, bad_cross4)

        # Beat 9: mistake 5 — one filter for every recording
        raw_hf = 0.7 * np.sin(2 * np.pi * 35 * t_vis) + 0.25 * np.random.randn(n_pts)
        raw_lf = 0.7 * np.sin(2 * np.pi * 0.6 * t_vis) + 0.3 * np.sin(2 * np.pi * 0.2 * t_vis) + 0.05 * np.random.randn(n_pts)
        filt_hf = raw_hf + 0.15 * np.random.randn(n_pts)
        filt_lf = 0.25 * np.sin(2 * np.pi * 2 * t_vis) + 0.03 * np.random.randn(n_pts)

        left_box5 = Rectangle(width=2.7, height=1.8, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.1)
        left_box5.move_to(panel_bg.get_center() + LEFT * 1.5 + DOWN * 0.1)
        right_box5 = Rectangle(width=2.7, height=1.8, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.1)
        right_box5.move_to(panel_bg.get_center() + RIGHT * 1.5 + DOWN * 0.1)

        raw_left_label5 = Text("High-freq noise", font_size=15, color=WHITE).next_to(left_box5, DOWN, buff=0.1)
        raw_right_label5 = Text("Low-freq drift", font_size=15, color=WHITE).next_to(right_box5, DOWN, buff=0.1)

        raw_hf_wave = make_wave(raw_hf, ORANGE, width=2.5, height=1.4).move_to(left_box5)
        raw_lf_wave = make_wave(raw_lf, TEAL, width=2.5, height=1.4).move_to(right_box5)
        filt_hf_wave = make_wave(filt_hf, ORANGE, width=2.5, height=1.4).move_to(left_box5)
        filt_lf_wave = make_wave(filt_lf, GREEN, width=2.5, height=1.4).move_to(right_box5)

        poor_label5 = Text("Still noisy", font_size=15, color=RED).move_to(raw_left_label5)
        good_label5 = Text("Acceptable", font_size=15, color=GREEN).move_to(raw_right_label5)
        bad_cross5 = make_x(RED, 0.7).next_to(left_box5, UP, buff=0.1)

        fifth_text = rows[4][1]
        fifth_text.shift(LEFT * 2.5)
        self.play(
            fifth_text.animate.shift(RIGHT * 2.5).set_opacity(1),
            FadeOut(current_panel_content),
            run_time=max(0.05, 0.8),
        )

        self.play(
            FadeIn(left_box5),
            FadeIn(right_box5),
            FadeIn(raw_left_label5),
            FadeIn(raw_right_label5),
            Create(raw_hf_wave),
            Create(raw_lf_wave),
            run_time=max(0.05, 0.7),
        )
        self.play(
            Transform(raw_hf_wave, filt_hf_wave),
            Transform(raw_lf_wave, filt_lf_wave),
            FadeOut(raw_left_label5),
            FadeOut(raw_right_label5),
            FadeIn(poor_label5),
            FadeIn(good_label5),
            FadeIn(bad_cross5),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.58))
        current_panel_content = VGroup(
            left_box5,
            right_box5,
            raw_hf_wave,
            raw_lf_wave,
            poor_label5,
            good_label5,
            bad_cross5,
        )

        # Beat 10: fade out all mistakes and panels
        self.play(
            FadeOut(title_group),
            FadeOut(list_group),
            FadeOut(panel_bg),
            FadeOut(current_panel_content),
            run_time=max(0.05, 0.26),
        )

        # Beat 11–13: scrolling goal banner
        banner_bg = Rectangle(
            width=11.0,
            height=1.4,
            fill_color=GREEN,
            fill_opacity=0.18,
            stroke_color=GREEN,
            stroke_width=2,
        )
        banner_text = Text(
            "Goal: preserve physiological information, not just smoothness",
            font_size=30,
            color=WHITE,
            weight=BOLD,
        )
        banner_text.scale_to_fit_width(8.6)
        banner_check = make_check(GREEN, 0.75)
        banner_group = VGroup(banner_check, banner_text).arrange(RIGHT, buff=0.3)
        banner_group.move_to(banner_bg.get_center())
        banner = VGroup(banner_bg, banner_group)
        banner.scale_to_fit_width(12.5)
        banner.move_to(np.array([15, -2.8, 0]))

        self.play(
            banner.animate.move_to(np.array([0, -2.8, 0])),
            run_time=max(0.05, 3.62),
            rate_func=smooth,
        )
        self.wait(max(0.05, 10.58))