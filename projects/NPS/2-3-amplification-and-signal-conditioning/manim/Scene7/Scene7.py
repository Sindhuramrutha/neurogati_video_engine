ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --------------------------------------------------------------
        # helpers
        # --------------------------------------------------------------
        def make_block(label, color, width, height):
            rect = Rectangle(
                width=width, height=height,
                fill_color=color, fill_opacity=0.35,
                stroke_color=color, stroke_width=2,
            )
            text = Text(label, font_size=18, color=WHITE, weight="BOLD",
                        line_spacing=0.8)
            if text.width > width - 0.2:
                text.scale_to_fit_width(width - 0.2)
            text.move_to(rect.get_center())
            return VGroup(rect, text)

        def make_bullet(text, max_width=10.2):
            b = Text("•  " + text, font_size=21, color=WHITE)
            if b.width > max_width:
                b.scale_to_fit_width(max_width)
            return b

        def make_glow(block, color=YELLOW, stroke_width=5,
                      fill_opacity=0.06, buff=0.12):
            glow = SurroundingRectangle(
                block, color=color, buff=buff, stroke_width=stroke_width,
            )
            glow.set_fill(color, opacity=fill_opacity)
            return glow

        # --------------------------------------------------------------
        # title + lower summary panel
        # --------------------------------------------------------------
        title = Text(
            "Section Summary", font_size=58, weight="BOLD", color=WHITE,
            t2c={"Summary": YELLOW},
        )
        title.to_edge(UP, buff=0.35)

        panel_rect = Rectangle(
            width=11.2, height=2.4,
            fill_color=GREY, fill_opacity=0.16,
            stroke_color=GREY_B, stroke_width=2,
        )
        panel_rect.move_to(np.array([0, -2.2, 0]))

        line1 = Line(
            start=panel_rect.get_left() + RIGHT * 0.2,
            end=panel_rect.get_right() + LEFT * 0.2,
            color=GREY_B, stroke_width=1.4,
        ).move_to(np.array([0, -1.8, 0]))
        line2 = Line(
            start=panel_rect.get_left() + RIGHT * 0.2,
            end=panel_rect.get_right() + LEFT * 0.2,
            color=GREY_B, stroke_width=1.4,
        ).move_to(np.array([0, -2.6, 0]))

        summary_panel = VGroup(panel_rect, line1, line2)

        # bullets for the three panel slots
        bullet1 = make_bullet(
            "Neural signals are extremely weak and require amplification before further processing."
        )
        bullet2 = make_bullet(
            "Signal conditioning prepares the amplified signal for digitisation by reducing unwanted interference."
        )
        bullet3 = make_bullet(
            "Together, amplification and signal conditioning improve recording reliability."
        )

        slot_centers = [
            np.array([0, -1.4, 0]),
            np.array([0, -2.2, 0]),
            np.array([0, -3.0, 0]),
        ]
        bullet1.move_to(slot_centers[0])
        bullet2.move_to(slot_centers[1])
        bullet3.move_to(slot_centers[2])

        # --------------------------------------------------------------
        # acquisition chain diagram
        # --------------------------------------------------------------
        block_electrode = make_block("Electrode", BLUE, 1.5, 0.95)
        block_amp = make_block("Amplifier", ORANGE, 1.6, 0.95)
        block_cond = make_block("Signal\nConditioning", TEAL, 1.8, 1.1)
        block_adc = make_block("ADC", PURPLE, 1.2, 0.95)
        block_digital = make_block("Digital\nOutput", GREEN, 1.7, 1.1)

        chain_blocks = VGroup(
            block_electrode, block_amp, block_cond, block_adc, block_digital,
        )
        chain_blocks.arrange(RIGHT, buff=0.7)
        chain_blocks.scale_to_fit_width(11.5)
        chain_blocks.move_to(np.array([0, 0.8, 0]))

        chain_arrows = VGroup(
            Arrow(
                chain_blocks[0].get_right(), chain_blocks[1].get_left(),
                buff=0.15, color=GREY, stroke_width=2.5,
            ),
            Arrow(
                chain_blocks[1].get_right(), chain_blocks[2].get_left(),
                buff=0.15, color=GREY, stroke_width=2.5,
            ),
            Arrow(
                chain_blocks[2].get_right(), chain_blocks[3].get_left(),
                buff=0.15, color=GREY, stroke_width=2.5,
            ),
            Arrow(
                chain_blocks[3].get_right(), chain_blocks[4].get_left(),
                buff=0.15, color=GREY, stroke_width=2.5,
            ),
        )

        # highlights
        amp_glow = make_glow(block_amp, YELLOW, 5, 0.06)
        cond_glow = make_glow(block_cond, YELLOW, 5, 0.06)
        adc_glow_soft = make_glow(block_adc, YELLOW, 3, 0.04)
        adc_glow_soft.set_stroke(YELLOW, width=3, opacity=0.7)

        triple_amp = make_glow(block_amp, YELLOW, 3, 0.04, buff=0.10)
        triple_cond = make_glow(block_cond, YELLOW, 3, 0.04, buff=0.10)
        triple_adc = make_glow(block_adc, YELLOW, 3, 0.04, buff=0.10)
        triple_glow = VGroup(triple_amp, triple_cond, triple_adc)
        triple_glow.set_opacity(0)

        # analog-to-digital waveform that will draw through the chain
        x0 = block_cond.get_right()[0] + 0.08
        x_adc_right = block_adc.get_right()[0]
        x_dig_right = block_digital.get_right()[0] - 0.08
        y0 = block_cond.get_center()[1]

        wave_points = []
        n_analog = 120
        for i in range(n_analog):
            t = i / (n_analog - 1)
            x = x0 + t * (x_adc_right - x0)
            y = y0 + 0.22 * np.sin(2 * np.pi * 1.8 * t)
            wave_points.append(np.array([x, y, 0]))

        n_steps = 9
        for i in range(n_steps):
            t_sample = 0.75 + 0.25 * (i / (n_steps - 1))
            y_sample = y0 + 0.18 * np.sin(2 * np.pi * 1.5 * t_sample)
            xa = x_adc_right + (i / n_steps) * (x_dig_right - x_adc_right)
            xb = x_adc_right + ((i + 1) / n_steps) * (x_dig_right - x_adc_right)
            wave_points.append(np.array([xa, y_sample, 0]))
            wave_points.append(np.array([xb, y_sample, 0]))

        wave_path = VMobject()
        wave_path.set_points_as_corners(wave_points)
        wave_path.set_color(YELLOW)
        wave_path.set_stroke(width=4)

        # the rest of the chain that dims when amplifier is highlighted
        non_amp_chain = VGroup(
            block_electrode, block_cond, block_adc, block_digital, chain_arrows,
        )

        # --------------------------------------------------------------
        # 1. 0.00-1.34  title + empty panel
        # --------------------------------------------------------------
        self.play(FadeIn(title), FadeIn(summary_panel), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 0.14))

        # --------------------------------------------------------------
        # 2. 1.34-6.36  full acquisition chain fades in
        # --------------------------------------------------------------
        self.play(FadeIn(chain_blocks), FadeIn(chain_arrows), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 3.02))

        # gap 6.36-7.32
        self.wait(max(0.05, 0.96))

        # --------------------------------------------------------------
        # 3. 7.32-13.04  first bullet + amplifier highlight
        # --------------------------------------------------------------
        self.play(
            FadeIn(bullet1),
            FadeIn(amp_glow),
            non_amp_chain.animate.set_opacity(0.3),
            run_time=max(0.05, 2.0),
        )
        self.play(
            amp_glow.animate.set_fill(YELLOW, opacity=0.12).set_stroke(YELLOW, width=8),
            run_time=max(0.05, 0.6),
        )
        self.play(
            amp_glow.animate.set_fill(YELLOW, opacity=0.06).set_stroke(YELLOW, width=5),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 2.52))

        # gap 13.04-13.96
        self.wait(max(0.05, 0.92))

        # --------------------------------------------------------------
        # 4. 13.96-24.96  second bullet + conditioning highlight, then ADC
        # --------------------------------------------------------------
        self.play(
            FadeIn(bullet2),
            FadeOut(amp_glow),
            FadeIn(cond_glow),
            block_cond.animate.set_opacity(1),
            block_amp.animate.set_opacity(0.3),
            run_time=max(0.05, 2.4),
        )
        self.play(
            cond_glow.animate.set_fill(YELLOW, opacity=0.12).set_stroke(YELLOW, width=8),
            run_time=max(0.05, 0.4),
        )
        self.play(
            cond_glow.animate.set_fill(YELLOW, opacity=0.06).set_stroke(YELLOW, width=5),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 3.68))

        # 20.84-24.96  ADC gains a softer highlight
        self.play(
            FadeIn(adc_glow_soft),
            block_adc.animate.set_opacity(0.7),
            run_time=max(0.05, 1.4),
        )
        self.wait(max(0.05, 2.72))

        # --------------------------------------------------------------
        # 5. 24.96-25.94  analog-to-digital waveform draws through chain
        # --------------------------------------------------------------
        self.play(Create(wave_path), run_time=max(0.05, 0.98))

        # --------------------------------------------------------------
        # 6. 25.94-34.24  third bullet + unified analog front-end glow
        # --------------------------------------------------------------
        self.play(
            FadeIn(bullet3),
            FadeOut(cond_glow),
            FadeOut(adc_glow_soft),
            triple_glow.animate.set_opacity(0.7),
            block_amp.animate.set_opacity(1),
            block_cond.animate.set_opacity(1),
            block_adc.animate.set_opacity(1),
            wave_path.animate.set_opacity(0.45),
            run_time=max(0.05, 2.2),
        )

        # soft breathing glow 28.14-33.16
        for _ in range(2):
            self.play(triple_glow.animate.set_opacity(0.8), run_time=max(0.05, 1.255))
            self.play(triple_glow.animate.set_opacity(0.4), run_time=max(0.05, 1.255))

        # --------------------------------------------------------------
        # 7. 33.16-35.10  digitized waveform pulse once, then fade out
        # --------------------------------------------------------------
        self.play(
            Indicate(wave_path, color=YELLOW, scale_factor=1.06),
            run_time=max(0.05, 0.94),
        )

        final_group = VGroup(
            title, summary_panel, chain_blocks, chain_arrows,
            bullet1, bullet2, bullet3, triple_glow, wave_path,
        )
        self.play(FadeOut(final_group), run_time=max(0.05, 1.0))