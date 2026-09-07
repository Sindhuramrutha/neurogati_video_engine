ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --------------------------------------------------------------
        # helper: small oscillating waveform (optionally noisy/drifty)
        # --------------------------------------------------------------
        def make_wave(width=0.78, amp=0.22, noise=False, drift=False,
                      color=BLUE, stroke_width=2.5):
            n = 60
            xs = np.linspace(-width / 2, width / 2, n)
            base = amp * np.sin(2 * PI * 1.2 * xs / width)
            ys = base.copy()
            if noise:
                rng = np.random.RandomState(7)
                ys += 0.13 * rng.randn(n)
            if drift:
                ys += 0.10 * (xs / width)
            wave = VMobject()
            wave.set_points_as_corners(
                [np.array([x, y, 0]) for x, y in zip(xs, ys)]
            )
            wave.set_stroke(color=color, width=stroke_width)
            return wave

        # --------------------------------------------------------------
        # build the six-block acquisition chain
        # --------------------------------------------------------------
        colors = [PINK, BLUE, TEAL, GREEN, ORANGE, PURPLE]
        label_texts = [
            "Biological\nSource",
            "Electrode",
            "Amplifier",
            "Signal\nConditioning",
            "ADC",
            "Computer",
        ]
        block_groups = []
        block_rects = []
        block_labels = []

        chain_y = 1.1
        block_w = 1.5
        block_h = 1.5
        gap = 0.85
        total_w = 6 * block_w + 5 * gap
        x0 = -total_w / 2 + block_w / 2

        for i in range(6):
            x = x0 + i * (block_w + gap)
            rect = Rectangle(
                width=block_w, height=block_h,
                fill_color=colors[i], fill_opacity=0.16,
                stroke_color=GREY_B, stroke_width=2,
            ).move_to(np.array([x, chain_y, 0]))
            label = Text(label_texts[i], font_size=16, color=WHITE, weight="BOLD")
            if label.width > rect.width - 0.28:
                label.scale_to_fit_width(rect.width - 0.28)
            label.move_to(rect.get_center())
            label.set_opacity(0)
            group = VGroup(rect, label)
            block_groups.append(group)
            block_rects.append(rect)
            block_labels.append(label)

        arrows = []
        arrow_centers = []
        for i in range(5):
            left_rect = block_rects[i]
            right_rect = block_rects[i + 1]
            arrow = Arrow(
                left_rect.get_right() + RIGHT * 0.03,
                right_rect.get_left() + LEFT * 0.03,
                buff=0,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.3,
                max_stroke_width_to_length_ratio=3,
            )
            arrow.set_stroke(color=GREY_B, width=2, opacity=0.4)
            arrows.append(arrow)
            arrow_centers.append((arrow.get_start() + arrow.get_end()) / 2)

        arrows_vgroup = VGroup(*arrows)

        # --------------------------------------------------------------
        # 0.00-3.24  fade the chain in left to right, dim and unlabeled
        # --------------------------------------------------------------
        chain_parts = []
        for i in range(6):
            chain_parts.append(block_groups[i])
            if i < 5:
                chain_parts.append(arrows[i])

        per_item = 3.24 / len(chain_parts)
        for part in chain_parts:
            self.play(FadeIn(part), run_time=max(0.05, per_item))

        # --------------------------------------------------------------
        # 3.24-9.35  light each block in sequence, add labels
        # --------------------------------------------------------------
        per_block = 6.11 / 6
        for i in range(6):
            plays = [
                block_rects[i].animate.set_fill(color=colors[i], opacity=0.50)
                             .set_stroke(color=colors[i], width=4, opacity=1),
                block_labels[i].animate.set_opacity(1),
            ]
            if i == 5:
                plays.append(arrows_vgroup.animate.set_color(WHITE).set_opacity(1))
            self.play(*plays, run_time=max(0.05, per_block * 0.6))
            self.wait(max(0.05, per_block * 0.4))

        # --------------------------------------------------------------
        # 9.80-14.32  tiny bio signal, then amplified taller signal
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.45))  # 9.35 -> 9.80

        small_wave = make_wave(width=0.72, amp=0.18, noise=False, color=BLUE)
        small_wave.move_to(arrow_centers[1])

        tall_wave = make_wave(width=0.72, amp=0.46, noise=True, drift=True, color=TEAL)
        tall_wave.move_to(arrow_centers[2])

        self.play(FadeIn(small_wave), run_time=max(0.05, 0.55))
        self.play(small_wave.animate.scale(1.25, about_point=small_wave.get_center()),
                  run_time=max(0.05, 0.35))
        self.play(small_wave.animate.scale(0.8, about_point=small_wave.get_center()),
                  run_time=max(0.05, 0.35))

        self.play(FadeIn(tall_wave), run_time=max(0.05, 0.7))
        self.play(tall_wave.animate.scale(1.15, about_point=tall_wave.get_center()),
                  run_time=max(0.05, 0.35))
        self.play(tall_wave.animate.scale(1 / 1.15, about_point=tall_wave.get_center()),
                  run_time=max(0.05, 0.25))

        self.play(
            Indicate(block_rects[1], color=BLUE, scale_factor=1.12),
            Indicate(block_rects[2], color=TEAL, scale_factor=1.12),
            run_time=max(0.05, 0.9),
        )
        self.wait(max(0.05, 1.07))

        # --------------------------------------------------------------
        # 15.14-18.48  tall noisy wave -> clean wave with flat baseline
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.82))  # 14.32 -> 15.14

        clean_wave = make_wave(width=0.72, amp=0.46, noise=False, color=GREEN)
        flat_baseline = Line(
            start=clean_wave.get_left() + DOWN * 0.22,
            end=clean_wave.get_right() + DOWN * 0.22,
            color=GREY_B, stroke_width=2,
        )
        clean_signal = VGroup(clean_wave, flat_baseline)
        clean_signal.move_to(arrow_centers[3])

        self.play(ReplacementTransform(tall_wave, clean_signal), run_time=max(0.05, 1.3))
        self.play(Indicate(block_rects[3], color=GREEN, scale_factor=1.08), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.24))

        # --------------------------------------------------------------
        # 19.30-25.56  continuous signal enters ADC, digital samples emerge
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.82))  # 18.48 -> 19.30

        adc_block = block_rects[4]
        computer_block = block_rects[5]
        adc_target = adc_block.get_left() + RIGHT * 0.20

        self.play(clean_signal.animate.move_to(adc_target), run_time=max(0.05, 1.1))
        self.play(Indicate(adc_block, color=ORANGE, scale_factor=1.1), run_time=max(0.05, 0.7))

        sample_xs = np.linspace(
            adc_block.get_right()[0] + 0.12,
            computer_block.get_left()[0] - 0.12,
            7,
        )
        sample_marker_mobs = []
        for x in sample_xs:
            marker_line = Line(
                start=np.array([x, chain_y - 0.17, 0]),
                end=np.array([x, chain_y + 0.17, 0]),
                color=ORANGE, stroke_width=3,
            )
            marker_dot = Dot(
                point=np.array([x, chain_y + 0.17, 0]),
                radius=0.035, color=YELLOW,
            )
            sample_marker_mobs.append(VGroup(marker_line, marker_dot))
        sample_markers = VGroup(*sample_marker_mobs)

        n_samples = len(sample_marker_mobs)
        per_marker = 1.76 / n_samples
        for marker in sample_marker_mobs:
            self.play(FadeIn(marker), run_time=max(0.05, per_marker))

        self.play(FadeOut(clean_signal), run_time=max(0.05, 0.5))

        travel_dot = Dot(
            point=adc_block.get_right() + RIGHT * 0.08,
            radius=0.06, color=YELLOW,
        )
        self.add(travel_dot)
        self.play(
            travel_dot.animate.move_to(computer_block.get_left() + LEFT * 0.08),
            run_time=max(0.05, 1.0),
        )
        self.play(Indicate(computer_block, color=PURPLE, scale_factor=1.1), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.8))

        # --------------------------------------------------------------
        # 26.34-36.58  focus on Amplifier + Signal Conditioning, caption
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.78))  # 25.56 -> 26.34

        non_focus_blocks = VGroup(
            block_groups[0], block_groups[1],
            block_groups[4], block_groups[5],
        )
        attention_group = VGroup(small_wave, sample_markers, travel_dot)

        self.play(
            block_groups[2].animate.set_opacity(1),
            block_groups[3].animate.set_opacity(1),
            block_rects[2].animate.set_fill(color=TEAL, opacity=0.60)
                           .set_stroke(color=TEAL, width=5, opacity=1),
            block_rects[3].animate.set_fill(color=GREEN, opacity=0.60)
                           .set_stroke(color=GREEN, width=5, opacity=1),
            non_focus_blocks.animate.set_opacity(0.30),
            arrows_vgroup.animate.set_opacity(0.35),
            attention_group.animate.set_opacity(0.30),
            run_time=max(0.05, 1.2),
        )

        x_mid = (block_rects[2].get_center()[0] + block_rects[3].get_center()[0]) / 2
        bottom_y = block_rects[2].get_bottom()[1]
        bottom_mid = np.array([x_mid, bottom_y, 0])

        caption = Text(
            "later stages depend on the quality\nof the amplified and conditioned signal",
            font_size=20, color=WHITE,
        )
        caption.scale_to_fit_width(8.2)
        caption.next_to(bottom_mid, DOWN, buff=0.5)

        self.play(
            FadeIn(caption),
            block_groups[2].animate.scale(1.04, about_point=block_groups[2].get_center()),
            block_groups[3].animate.scale(1.04, about_point=block_groups[3].get_center()),
            run_time=max(0.05, 1.4),
        )
        self.play(
            block_groups[2].animate.scale(1 / 1.04, about_point=block_groups[2].get_center()),
            block_groups[3].animate.scale(1 / 1.04, about_point=block_groups[3].get_center()),
            run_time=max(0.05, 0.5),
        )
        self.play(
            block_groups[2].animate.scale(1.04, about_point=block_groups[2].get_center()),
            block_groups[3].animate.scale(1.04, about_point=block_groups[3].get_center()),
            run_time=max(0.05, 0.5),
        )
        self.play(
            block_groups[2].animate.scale(1 / 1.04, about_point=block_groups[2].get_center()),
            block_groups[3].animate.scale(1 / 1.04, about_point=block_groups[3].get_center()),
            run_time=max(0.05, 0.5),
        )

        self.wait(max(0.05, 5.14))

        # final fade-out
        all_visible = VGroup(
            *block_groups,
            *arrows,
            small_wave,
            sample_markers,
            travel_dot,
            caption,
        )
        self.play(FadeOut(all_visible), run_time=max(0.05, 1.0))