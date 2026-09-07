ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --------------------------------------------------------------
        # helpers
        # --------------------------------------------------------------
        def make_block(label, color, width, height, dimmed=False):
            if dimmed:
                rect = Rectangle(
                    width=width, height=height,
                    fill_color=color, fill_opacity=0.08,
                    stroke_color=GREY_B, stroke_width=2,
                )
                text = Text(label, font_size=18, color=GREY, weight="BOLD",
                            line_spacing=0.8)
            else:
                rect = Rectangle(
                    width=width, height=height,
                    fill_color=color, fill_opacity=0.45,
                    stroke_color=color, stroke_width=2,
                )
                text = Text(label, font_size=18, color=WHITE, weight="BOLD",
                            line_spacing=0.8)

            if text.width > width - 0.2:
                text.scale_to_fit_width(width - 0.2)
            text.move_to(rect.get_center())
            group = VGroup(rect, text)
            group.rect = rect
            group.text = text
            return group

        def make_glow(block, color, stroke_width=4, fill_opacity=0.08, buff=0.12):
            glow = SurroundingRectangle(
                block, color=color, buff=buff,
                stroke_width=stroke_width,
            )
            glow.set_fill(color, opacity=fill_opacity)
            return glow

        # --------------------------------------------------------------
        # acquisition chain
        # --------------------------------------------------------------
        block_electrode = make_block("Electrode", BLUE, 1.4, 0.95)
        block_amp = make_block("Amplifier", ORANGE, 1.5, 0.95)
        block_cond = make_block("Signal\nConditioning", TEAL, 1.7, 1.1)
        block_adc = make_block("ADC", PURPLE, 1.2, 0.95, dimmed=True)
        block_digital = make_block("Digital\nOutput", GREEN, 1.6, 1.1, dimmed=True)

        chain_blocks = VGroup(
            block_electrode, block_amp, block_cond, block_adc, block_digital,
        )
        chain_blocks.arrange(RIGHT, buff=1.6)
        chain_blocks.scale_to_fit_width(12.6)
        chain_blocks.move_to(np.array([0, 1.2, 0]))

        # Stored rect references for pulse / brightness animation
        electrode_rect = block_electrode.rect
        amp_rect = block_amp.rect
        cond_rect = block_cond.rect
        adc_rect = block_adc.rect
        digital_rect = block_digital.rect
        adc_text = block_adc.text
        digital_text = block_digital.text

        # Glows
        electrode_glow = make_glow(block_electrode, YELLOW, stroke_width=4, fill_opacity=0.08)
        amp_glow = make_glow(block_amp, YELLOW, stroke_width=4, fill_opacity=0.08)
        cond_glow = make_glow(block_cond, YELLOW, stroke_width=4, fill_opacity=0.08)
        adc_glow_soft = make_glow(block_adc, YELLOW, stroke_width=3, fill_opacity=0.04)
        digital_glow = make_glow(block_digital, YELLOW, stroke_width=4, fill_opacity=0.08)

        # Arrows between blocks
        arrow_e_amp = Arrow(
            block_electrode.get_right(), block_amp.get_left(),
            buff=0.12, color=GREY, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.16,
        )
        arrow_amp_cond = Arrow(
            block_amp.get_right(), block_cond.get_left(),
            buff=0.12, color=GREY, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.16,
        )
        arrow_cond_adc = Arrow(
            block_cond.get_right(), block_adc.get_left(),
            buff=0.12, color=GREY, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.16,
        )
        arrow_adc_digital = Arrow(
            block_adc.get_right(), block_digital.get_left(),
            buff=0.12, color=GREY, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.16,
        )
        chain_arrows = VGroup(
            arrow_e_amp, arrow_amp_cond, arrow_cond_adc, arrow_adc_digital,
        )

        # --------------------------------------------------------------
        # analog waveform geometry
        # --------------------------------------------------------------
        x_wave_start = block_cond.rect.get_right()[0] + 0.12
        x_wave_end = block_adc.rect.get_left()[0] - 0.5
        y_wave = block_cond.rect.get_center()[1]

        n_wave_points = 200

        def make_wave_points(phase):
            pts = []
            for i in range(n_wave_points):
                t = i / (n_wave_points - 1)
                x = x_wave_start + (x_wave_end - x_wave_start) * t
                y = y_wave + 0.28 * np.sin(2 * np.pi * 2.2 * t - phase)
                pts.append(np.array([x, y, 0]))
            return pts

        analog_wave = VMobject()
        analog_wave.set_color(YELLOW).set_stroke(width=4)
        analog_wave.set_points_as_corners(make_wave_points(0))

        analog_label = Text("analogue signal", font_size=21, color=WHITE)
        analog_label.next_to(analog_wave, DOWN, buff=0.28)

        wave_phase = ValueTracker(0)

        def update_wave(mob):
            mob.set_points_as_corners(make_wave_points(wave_phase.get_value()))

        # Arrow from wave tip to ADC
        tip_y = y_wave + 0.28 * np.sin(2 * np.pi * 2.2)
        arrow_analog = Arrow(
            start=np.array([x_wave_end, tip_y, 0]),
            end=np.array([block_adc.rect.get_left()[0] + 0.06, y_wave + 0.05, 0]),
            buff=0.06,
            color=WHITE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.24,
        )

        # --------------------------------------------------------------
        # discrete samples inside / after ADC
        # --------------------------------------------------------------
        n_samples = 8
        adc_left = block_adc.rect.get_left()[0]
        adc_right = block_adc.rect.get_right()[0]
        y_base = block_adc.rect.get_bottom()[1] + 0.12

        sample_groups = VGroup()
        sample_points_pos = []
        for i in range(n_samples):
            x = adc_left + 0.18 + i * (adc_right - adc_left - 0.36) / (n_samples - 1)
            t_cont = (x - x_wave_start) / (x_wave_end - x_wave_start)
            y = y_wave + 0.28 * np.sin(2 * np.pi * 2.2 * t_cont)
            point = np.array([x, y, 0])
            base = np.array([x, y_base, 0])
            stem = Line(base, point, color=PURPLE, stroke_width=4)
            dot = Dot(point, radius=0.06, color=YELLOW)
            sample_group = VGroup(stem, dot)
            sample_groups.add(sample_group)
            sample_points_pos.append(point)

        # --------------------------------------------------------------
        # binary stream snippets
        # --------------------------------------------------------------
        bits_sequence = ["01", "10", "11", "00", "01", "10", "11", "00"]
        binary_labels = VGroup()
        stream_final_positions = []
        for i in range(n_samples):
            label = Text(bits_sequence[i], font_size=13, color=GREEN)
            label.move_to(sample_points_pos[i] + UP * 0.25)
            binary_labels.add(label)

            # final positions stacked at the digital-output input
            fx = block_digital.rect.get_left()[0] + 0.12
            fy = block_digital.rect.get_center()[1] + (0.30 - 0.08 * i)
            stream_final_positions.append(np.array([fx, fy, 0]))

        stream_group = binary_labels

        # --------------------------------------------------------------
        # bottom next-section text
        # --------------------------------------------------------------
        next_text = Text(
            "Next: Section 2.4 — Sampling and Analog-to-Digital Conversion",
            font_size=22,
            color=WHITE,
            t2c={"Next:": YELLOW},
        )
        next_text.scale_to_fit_width(12.5)
        next_text.to_edge(DOWN, buff=0.4)

        # --------------------------------------------------------------
        # 1. 0.00-0.84  chain fades in
        # --------------------------------------------------------------
        self.play(
            FadeIn(chain_blocks),
            FadeIn(chain_arrows),
            FadeIn(electrode_glow),
            FadeIn(amp_glow),
            FadeIn(cond_glow),
            run_time=max(0.05, 0.84),
        )

        # --------------------------------------------------------------
        # 2. 0.84-2.48  electrode pulse
        # --------------------------------------------------------------
        self.play(
            electrode_glow.animate.set_stroke(YELLOW, width=8).set_fill(YELLOW, opacity=0.19),
            electrode_rect.animate.set_fill(BLUE, opacity=0.8),
            run_time=max(0.05, 0.55),
        )
        self.play(
            electrode_glow.animate.set_stroke(YELLOW, width=4).set_fill(YELLOW, opacity=0.08),
            electrode_rect.animate.set_fill(BLUE, opacity=0.45),
            run_time=max(0.05, 0.55),
        )
        self.wait(max(0.05, 0.54))

        # --------------------------------------------------------------
        # 3. 3.06-4.28  amplifier then conditioning pulse
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.58))

        self.play(
            amp_glow.animate.set_stroke(YELLOW, width=8).set_fill(YELLOW, opacity=0.19),
            amp_rect.animate.set_fill(ORANGE, opacity=0.8),
            run_time=max(0.05, 0.24),
        )
        self.play(
            amp_glow.animate.set_stroke(YELLOW, width=4).set_fill(YELLOW, opacity=0.08),
            amp_rect.animate.set_fill(ORANGE, opacity=0.45),
            run_time=max(0.05, 0.19),
        )
        self.play(
            cond_glow.animate.set_stroke(YELLOW, width=8).set_fill(YELLOW, opacity=0.19),
            cond_rect.animate.set_fill(TEAL, opacity=0.8),
            run_time=max(0.05, 0.24),
        )
        self.play(
            cond_glow.animate.set_stroke(YELLOW, width=4).set_fill(YELLOW, opacity=0.08),
            cond_rect.animate.set_fill(TEAL, opacity=0.45),
            run_time=max(0.05, 0.19),
        )
        self.wait(max(0.05, 0.36))

        # --------------------------------------------------------------
        # 4. 5.24-7.22  waveform emerges
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.96))

        self.play(
            FadeOut(arrow_cond_adc),
            Create(analog_wave),
            FadeIn(analog_label),
            run_time=max(0.05, 1.98),
        )

        # --------------------------------------------------------------
        # 5. 7.84-10.26  waveform continuous motion
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.62))

        analog_wave.add_updater(update_wave)
        self.play(
            wave_phase.animate.set_value(6 * PI),
            run_time=max(0.05, 2.42),
        )

        # --------------------------------------------------------------
        # 6. 10.98-14.08  arrow to ADC and soft ADC brighten
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.72))

        self.play(Create(arrow_analog), run_time=max(0.05, 1.9))
        self.play(
            adc_rect.animate.set_fill(PURPLE, opacity=0.35),
            adc_text.animate.set_color(WHITE),
            FadeIn(adc_glow_soft),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.5))

        # --------------------------------------------------------------
        # 7. 14.64-16.30  continuous wave becomes points and bars
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.56))

        per_sample_create = max(0.05, 1.66 / n_samples)
        for sample in sample_groups:
            self.play(
                Create(sample[0]),
                GrowFromCenter(sample[1]),
                run_time=max(0.05, per_sample_create),
            )

        # --------------------------------------------------------------
        # 8. 16.90-21.04  samples to binary stream flowing toward digital
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.60))

        self.play(
            analog_wave.animate.set_opacity(0.4),
            arrow_analog.animate.set_opacity(0.4),
            run_time=max(0.05, 0.35),
        )

        per_sample_binary = max(0.05, 0.10)
        for i in range(n_samples):
            self.play(
                FadeOut(sample_groups[i]),
                GrowFromCenter(binary_labels[i]),
                run_time=max(0.05, per_sample_binary),
            )

        self.play(FadeOut(arrow_adc_digital), run_time=max(0.05, 0.45))

        per_stream_move = max(0.05, 0.18)
        for i in range(n_samples):
            self.play(
                binary_labels[i].animate.move_to(stream_final_positions[i]),
                run_time=max(0.05, per_stream_move),
            )

        self.wait(max(0.05, 1.10))

        # --------------------------------------------------------------
        # 9. 21.74-22.36  ADC pulse and label
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.70))

        adc_badge = Text("ADC", font_size=24, color=YELLOW, weight="BOLD")
        adc_badge.next_to(block_adc, UP, buff=0.2)

        self.play(
            Indicate(block_adc, color=YELLOW, scale_factor=1.06),
            FadeIn(adc_badge),
            run_time=max(0.05, 0.62),
        )

        # --------------------------------------------------------------
        # 10-11. 23.44-28.82  digital output brightens, stream continues,
        # then next-section text fades in and scene holds
        # --------------------------------------------------------------
        self.wait(max(0.05, 1.08))

        self.play(
            digital_rect.animate.set_fill(GREEN, opacity=0.55),
            digital_text.animate.set_color(WHITE),
            FadeIn(digital_glow),
            run_time=max(0.05, 0.80),
        )

        # gentle stream motion before next-section text
        shift_step = 0.04
        for _ in range(2):
            self.play(stream_group.animate.shift(UP * shift_step), run_time=max(0.05, 0.5))
            self.play(stream_group.animate.shift(DOWN * shift_step), run_time=max(0.05, 0.5))

        self.wait(max(0.05, 0.94))

        self.play(FadeIn(next_text), run_time=max(0.05, 0.7))

        # final gentle motion while next-section text is visible
        tail_step = 0.03
        self.play(stream_group.animate.shift(UP * tail_step), run_time=max(0.05, 0.47))
        self.play(stream_group.animate.shift(DOWN * tail_step), run_time=max(0.05, 0.47))

        self.wait(max(0.05, 0.0))