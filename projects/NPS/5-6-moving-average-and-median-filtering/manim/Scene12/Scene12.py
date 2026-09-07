ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene12(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # BEAT 1 (0.00 - 1.16): question mark + "Which filter?" fade in
        # ------------------------------------------------------------------
        question_mark = Text("?", font_size=200, color=YELLOW, weight="BOLD")
        question_text = Text("Which filter?", font_size=64, color=WHITE)

        question_core = VGroup(question_mark, question_text)
        question_core.arrange(DOWN, buff=0.4)
        question_core.move_to(ORIGIN)

        pulse_circle = Circle(
            radius=1.5,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_opacity=0,
        )
        pulse_circle.move_to(question_mark.get_center())
        pulse_circle.set_opacity(0)

        self.play(FadeIn(question_core), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.56))  # 0.60 -> 1.16

        # ------------------------------------------------------------------
        # BEAT 2 (1.16 - 3.16): slow upward float + soft pulse
        # ------------------------------------------------------------------
        self.add(pulse_circle)
        self.play(
            question_core.animate.shift(UP * 0.4),
            pulse_circle.animate.shift(UP * 0.4).set_opacity(0.4).scale(1.8),
            run_time=max(0.05, 2.0),
        )

        # ------------------------------------------------------------------
        # BEAT 3 (3.16 - 4.48): dim and fade out question display
        # ------------------------------------------------------------------
        self.play(
            FadeOut(question_core),
            FadeOut(pulse_circle),
            run_time=max(0.05, 0.9),
        )
        self.wait(max(0.05, 0.42))  # 4.06 -> 4.48

        # ------------------------------------------------------------------
        # BEAT 4 (4.48 - 5.72): section title fades in
        # ------------------------------------------------------------------
        section_label = Text(
            "Section 5.7:",
            font_size=36,
            color="#B0B5BC",
            weight="BOLD",
        )
        selecting_word = Text(
            "Selecting",
            font_size=48,
            color=WHITE,
            weight="BOLD",
        )
        filters_words = Text(
            "Filters for Neural Applications",
            font_size=48,
            color=WHITE,
            weight="BOLD",
        )

        title_main = VGroup(selecting_word, filters_words)
        title_main.arrange(RIGHT, buff=0.12)

        title_display = VGroup(section_label, title_main)
        title_display.arrange(DOWN, buff=0.25)
        title_display.move_to(ORIGIN)

        self.play(FadeIn(title_display), run_time=max(0.05, 1.24))
        self.wait(max(0.05, 0.56))  # 5.72 -> 6.28

        # ------------------------------------------------------------------
        # BEAT 5 (6.28 - 7.92): faint ghost question pulse behind title
        # ------------------------------------------------------------------
        ghost_q_mark = Text(
            "?",
            font_size=120,
            color=YELLOW,
            weight="BOLD",
        )
        ghost_q_mark.move_to(title_display.get_center())
        ghost_q_mark.set_opacity(0)

        ghost_glow = Circle(
            radius=1.2,
            stroke_color=YELLOW,
            stroke_width=4,
            fill_opacity=0,
        )
        ghost_glow.move_to(ghost_q_mark.get_center())
        ghost_glow.set_opacity(0)

        self.add(ghost_q_mark, ghost_glow)
        self.bring_to_back(ghost_q_mark)
        self.bring_to_back(ghost_glow)

        self.play(
            ghost_q_mark.animate.set_opacity(0.15),
            ghost_glow.animate.set_opacity(0.4),
            run_time=max(0.05, 0.35),
        )
        self.play(
            ghost_glow.animate.scale(1.5).set_opacity(0),
            run_time=max(0.05, 0.7),
        )
        self.play(
            FadeOut(ghost_q_mark),
            FadeOut(ghost_glow),
            run_time=max(0.05, 0.35),
        )
        self.wait(max(0.05, 0.24))  # 7.68 -> 7.92

        # ------------------------------------------------------------------
        # BEAT 6 (7.92 - 9.38): subtle outline around "Selecting"
        # ------------------------------------------------------------------
        select_rect = SurroundingRectangle(
            selecting_word,
            color=YELLOW,
            buff=0.1,
            stroke_width=2,
            fill_opacity=0,
        )

        self.play(Create(select_rect), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.2))  # 8.52 -> 8.72
        self.play(FadeOut(select_rect), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.16))  # 9.22 -> 9.38

        # ------------------------------------------------------------------
        # BEAT 7 (9.38 - 11.30): faint neural waveform behind title
        # ------------------------------------------------------------------
        wave_x = np.linspace(-2.5, 2.5, 200)
        wave_y = 0.4 * np.sin(2 * np.pi * 1.5 * wave_x) * np.exp(-0.3 * np.abs(wave_x))
        wave_points = [np.array([x, y, 0]) for x, y in zip(wave_x, wave_y)]

        waveform = VMobject(
            stroke_color=TEAL,
            stroke_width=5,
            fill_opacity=0,
            stroke_opacity=0.25,
        )
        waveform.set_points_as_corners(wave_points)
        waveform.scale_to_fit_width(title_display.width + 2.0)
        waveform.move_to(title_display.get_center())

        self.add(waveform)
        self.bring_to_back(waveform)

        self.play(
            waveform.animate.set_stroke(opacity=0.5),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 0.7))  # 9.98 -> 10.68
        self.play(
            waveform.animate.set_stroke(opacity=0.0),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.12))  # 11.18 -> 11.30

        # ------------------------------------------------------------------
        # BEAT 8 (11.30 - 13.04): title settles lower + underline
        # ------------------------------------------------------------------
        self.play(
            title_display.animate.shift(DOWN * 0.4),
            run_time=max(0.05, 0.6),
        )
        self.wait(max(0.05, 0.1))  # 11.90 -> 12.00

        underline = Line(
            LEFT * title_main.width / 2,
            RIGHT * title_main.width / 2,
            color=GREY,
            stroke_width=3,
        )
        underline.next_to(title_main, DOWN, buff=0.2)

        self.play(Create(underline), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.54))  # 12.50 -> 13.04

        # ------------------------------------------------------------------
        # BEAT 9 (13.04 - 14.90): three filter chips fade in one by one
        # ------------------------------------------------------------------
        chip_texts = ["low-pass", "high-pass", "band-pass"]
        chips = VGroup()

        for txt in chip_texts:
            chip_rect = Rectangle(
                width=1.6,
                height=0.6,
                stroke_color=WHITE,
                stroke_width=2,
                fill_color=BLUE,
                fill_opacity=0.2,
            )
            chip_label = Text(txt, font_size=22, color=WHITE)
            chip_label.move_to(chip_rect.get_center())
            single_chip = VGroup(chip_rect, chip_label)
            chips.add(single_chip)

        chips.arrange(RIGHT, buff=0.3)
        chips.next_to(underline, DOWN, buff=0.3)

        self.play(FadeIn(chips[0]), run_time=max(0.05, 0.3))
        self.play(FadeIn(chips[1]), run_time=max(0.05, 0.3))
        self.play(FadeIn(chips[2]), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.96))  # 13.94 -> 14.90

        # ------------------------------------------------------------------
        # BEAT 10 (14.90 - 15.56): chips and underline fade out
        # ------------------------------------------------------------------
        self.play(
            FadeOut(chips),
            FadeOut(underline),
            run_time=max(0.05, 0.66),
        )

        # ------------------------------------------------------------------
        # BEAT 11 (15.56 - 16.80): soft transition, scale down, soft vignette
        # ------------------------------------------------------------------
        overlay = Rectangle(
            width=14,
            height=8,
            fill_color=BLACK,
            fill_opacity=0,
            stroke_width=0,
        )
        overlay.move_to(ORIGIN)
        self.add(overlay)

        self.play(
            title_display.animate.scale(0.95).set_opacity(0.8),
            overlay.animate.set_fill(opacity=0.4),
            run_time=max(0.05, 1.24),
        )

        # ------------------------------------------------------------------
        # BEAT 12 (16.80 - 17.75): transition deepens, title low intensity
        # ------------------------------------------------------------------
        self.play(
            title_display.animate.set_opacity(0.15),
            overlay.animate.set_fill(opacity=0.85),
            run_time=max(0.05, 0.95),
        )