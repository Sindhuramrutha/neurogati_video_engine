ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *


class Scene10(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Card panel with soft drop shadow
        # ------------------------------------------------------------
        card = RoundedRectangle(
            width=11.5,
            height=5.8,
            corner_radius=0.25,
            fill_color="#ECECEC",
            fill_opacity=1,
            stroke_color="#CCCCCC",
            stroke_width=1.5,
        )
        shadow = card.copy().set_fill(BLACK, opacity=0.35).set_stroke(width=0)
        shadow.shift(RIGHT * 0.08 + DOWN * 0.10)
        card_group = VGroup(shadow, card).move_to(np.array([0, 1.2, 0]))

        title = Text(
            "Advantages of high-pass filtering",
            font_size=38,
            color="#1A1A1A",
            weight="BOLD",
        )
        title.move_to(card.get_top() + DOWN * 0.7)

        # ------------------------------------------------------------
        # Helper: small solid green chevron icon
        # ------------------------------------------------------------
        def make_chevron():
            chev = Polygon(
                [0.22, 0, 0],
                [-0.10, 0.20, 0],
                [-0.02, 0.20, 0],
                [-0.02, -0.20, 0],
                [-0.10, -0.20, 0],
                fill_color=GREEN,
                fill_opacity=1,
                stroke_width=0,
            )
            chev.scale_to_fit_height(0.42)
            chev.scale_to_fit_width(0.50)
            return chev

        def build_row(text_str, y, max_text_width=8.6, font_size=26):
            icon = make_chevron().move_to(np.array([icon_x, y, 0]))
            txt = Text(text_str, font_size=font_size, color="#333333")
            if txt.width > max_text_width:
                txt.scale_to_fit_width(max_text_width)
            txt.next_to(icon, RIGHT, buff=0.3, aligned_edge=LEFT)
            return VGroup(icon, txt)

        icon_x = card.get_left()[0] + 0.7

        row1_y = 2.05
        row2_y = 1.35
        row3_y = 0.65
        row4_y = -0.05
        row5_y = -0.75

        row1 = build_row("Reduces baseline drift", row1_y, font_size=26)
        row2 = build_row("Suppresses slow movement artefacts", row2_y, font_size=26)
        row3 = build_row("Improves baseline stability", row3_y, font_size=26)
        row4 = build_row(
            "Enhances the visibility of rapid physiological events",
            row4_y,
            font_size=24,
        )

        # Row 5 is special: first part slides in alone, second part appears later.
        icon5 = make_chevron().move_to(np.array([icon_x, row5_y, 0]))
        first5 = Text(
            "Serves as an important preprocessing step",
            font_size=24,
            color="#333333",
        )
        if first5.width > 8.0:
            first5.scale_to_fit_width(8.0)
        first5.next_to(icon5, RIGHT, buff=0.3, aligned_edge=LEFT)
        row5 = VGroup(icon5, first5)

        second5 = Text(
            "before spike detection and EMG analysis",
            font_size=24,
            color="#333333",
        )
        if second5.width > 8.0:
            second5.scale_to_fit_width(8.0)
        second5.next_to(first5, DOWN, buff=0.12, aligned_edge=LEFT)

        # ------------------------------------------------------------
        # Beat 1: 0.00–3.06 — card + title appear
        # ------------------------------------------------------------
        self.play(
            FadeIn(card_group),
            Write(title),
            run_time=max(0.05, 1.0),
        )
        self.wait(max(0.05, 2.06))

        # Gap before beat 2
        self.wait(max(0.05, 0.90))

        # ------------------------------------------------------------
        # Beat 2: 3.96–5.28 — row 1 slides in, chevron pulses
        # ------------------------------------------------------------
        row1_final = row1.get_center()
        row1.shift(LEFT * 8.0)
        self.play(
            row1.animate.move_to(row1_final),
            rate_func=rate_functions.ease_out_elastic,
            run_time=max(0.05, 0.9),
        )
        self.play(Indicate(row1[0], scale_factor=1.2, color=GREEN), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.12))

        # Gap before beat 3
        self.wait(max(0.05, 0.82))

        # ------------------------------------------------------------
        # Beat 3: 6.10–7.76 — row 2 slides in
        # ------------------------------------------------------------
        row2_final = row2.get_center()
        row2.shift(LEFT * 8.0)
        self.play(
            row2.animate.move_to(row2_final),
            rate_func=rate_functions.ease_out_elastic,
            run_time=max(0.05, 0.9),
        )
        self.play(Indicate(row2[0], scale_factor=1.2, color=GREEN), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.46))

        # Gap before beat 4
        self.wait(max(0.05, 0.92))

        # ------------------------------------------------------------
        # Beat 4: 8.68–10.02 — row 3 slides in
        # ------------------------------------------------------------
        row3_final = row3.get_center()
        row3.shift(LEFT * 8.0)
        self.play(
            row3.animate.move_to(row3_final),
            rate_func=rate_functions.ease_out_elastic,
            run_time=max(0.05, 0.9),
        )
        self.play(Indicate(row3[0], scale_factor=1.2, color=GREEN), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.14))

        # Gap before beat 5
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------
        # Beat 5: 10.86–13.90 — row 4 slides in (longer text, slightly smaller)
        # ------------------------------------------------------------
        row4_final = row4.get_center()
        row4.shift(LEFT * 8.0)
        self.play(
            row4.animate.move_to(row4_final),
            rate_func=rate_functions.ease_out_elastic,
            run_time=max(0.05, 0.9),
        )
        self.play(Indicate(row4[0], scale_factor=1.2, color=GREEN), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 1.84))

        # Gap before beat 6
        self.wait(max(0.05, 0.80))

        # ------------------------------------------------------------
        # Beat 6: 14.70–16.28 — row 5 slides in with first part only
        # ------------------------------------------------------------
        row5_final = row5.get_center()
        row5.shift(LEFT * 8.0)
        self.play(
            row5.animate.move_to(row5_final),
            rate_func=rate_functions.ease_out_elastic,
            run_time=max(0.05, 0.9),
        )
        self.play(Indicate(row5[0], scale_factor=1.2, color=GREEN), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.38))

        # ------------------------------------------------------------
        # Beat 7: 16.28–20.10 — completed phrase fades/writes in
        # ------------------------------------------------------------
        self.play(AddTextLetterByLetter(second5), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 2.32))

        # ------------------------------------------------------------
        # Beat 8: 20.10–21.07 — hold, then gentle fade out last half second
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.47))
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=max(0.05, 0.5),
        )