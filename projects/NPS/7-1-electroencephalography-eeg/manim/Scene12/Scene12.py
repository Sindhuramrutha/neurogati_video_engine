ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene12(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        wave_time = ValueTracker(0)
        alpha_amp = ValueTracker(0.0)
        slow_amp = ValueTracker(0.0)
        light_bg_cycles = ValueTracker(8.0)

        def advance(duration, *anims):
            if duration <= 0:
                return
            safe = max(0.05, float(duration))
            all_anims = list(anims)
            all_anims.append(wave_time.animate.increment_value(safe))
            self.play(*all_anims, run_time=max(0.05, safe), rate_func=linear)

        # ------------------------------------------------------------------
        # Previous scene's composition (definition box + stage cards + arrows)
        # ------------------------------------------------------------------
        prev_def_text = Text(
            "Sleep staging = process of identifying different stages of sleep\nby analysing physiological signals, particularly EEG",
            font_size=20,
            color=WHITE,
        )
        prev_def_box = RoundedRectangle(
            corner_radius=0.15,
            width=prev_def_text.width + 0.6,
            height=prev_def_text.height + 0.4,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        prev_def_text.move_to(prev_def_box.get_center())
        prev_def = VGroup(prev_def_box, prev_def_text)
        prev_def.move_to(np.array([0, 1.7, 0]))

        prev_cards = VGroup()
        stage_info = [
            ("Wakefulness", TEAL),
            ("Light Sleep", BLUE),
            ("Deep Sleep", PURPLE),
            ("REM", PINK),
        ]
        for idx, (name, color) in enumerate(stage_info):
            ww = Rectangle(
                width=1.1,
                height=0.42,
                stroke_color=GREY_B,
                stroke_width=1.0,
                fill_color=BLACK,
                fill_opacity=0.4,
            )
            wave = VMobject()
            wave.set_stroke(color=YELLOW, width=1.5, opacity=0.9)
            u = np.linspace(0, 1, 40)
            x_left = ww.get_left()[0] + 0.07
            x_right = ww.get_right()[0] - 0.07
            xs = np.linspace(x_left, x_right, 40)
            cy = ww.get_center()[1]
            y = 0.11 * np.sin(2 * np.pi * 3 * u + idx * 1.2)
            wave.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )
            block = RoundedRectangle(
                corner_radius=0.08,
                width=1.25,
                height=0.6,
                fill_color=color,
                fill_opacity=0.30,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            label = Text(name, font_size=13, color=WHITE)
            block.next_to(ww, DOWN, buff=0.08)
            label.next_to(block, DOWN, buff=0.05)
            prev_cards.add(VGroup(ww, wave, block, label))

        prev_cards.arrange(RIGHT, buff=0.35)
        prev_cards.next_to(prev_def, DOWN, buff=0.5)

        prev_arrows = VGroup()
        for i in range(3):
            arrow = Arrow(
                prev_cards[i].get_right() + RIGHT * 0.06,
                prev_cards[i + 1].get_left() + LEFT * 0.06,
                color=GREY_B,
                stroke_width=2,
                buff=0.06,
            )
            prev_arrows.add(arrow)

        prev_composition = VGroup(prev_def, prev_cards, prev_arrows)
        prev_composition.scale_to_fit_width(11.5)
        prev_composition.move_to(np.array([0, 0.2, 0]))

        self.add(prev_composition)

        # ------------------------------------------------------------------
        # New sleep branching diagram
        # ------------------------------------------------------------------
        sleep_title = Text("Sleep", font_size=52, color=GOLD, weight="BOLD")
        sleep_title.move_to(np.array([0, 3.15, 0]))

        # NREM box
        nrem_box = RoundedRectangle(
            corner_radius=0.18,
            width=3.3,
            height=1.3,
            fill_color=BLUE,
            fill_opacity=0.30,
            stroke_color=WHITE,
            stroke_width=2,
        )
        nrem_full = Text("Non-Rapid Eye Movement", font_size=14, color=WHITE)
        nrem_short = Text("NREM sleep", font_size=22, color=WHITE, weight="BOLD")
        nrem_texts = VGroup(nrem_full, nrem_short).arrange(DOWN, buff=0.08)
        nrem_group = VGroup(nrem_box, nrem_texts)
        nrem_group.move_to(np.array([-3.5, 1.9, 0]))
        nrem_texts.move_to(nrem_box.get_center())

        # REM box
        rem_box = RoundedRectangle(
            corner_radius=0.18,
            width=3.1,
            height=1.3,
            fill_color=PINK,
            fill_opacity=0.30,
            stroke_color=WHITE,
            stroke_width=2,
        )
        rem_full = Text("Rapid Eye Movement", font_size=14, color=WHITE)
        rem_short = Text("REM sleep", font_size=22, color=WHITE, weight="BOLD")
        rem_texts = VGroup(rem_full, rem_short).arrange(DOWN, buff=0.08)
        rem_group = VGroup(rem_box, rem_texts)
        rem_group.move_to(np.array([3.5, 1.9, 0]))
        rem_texts.move_to(rem_box.get_center())

        sleep_bottom = sleep_title.get_bottom()
        left_branch_initial = np.array([-2.6, 2.15, 0])
        right_branch_initial = np.array([2.6, 2.15, 0])

        left_branch = Line(sleep_bottom, left_branch_initial,
                           color=GREY_B, stroke_width=3.0)
        right_branch = Line(sleep_bottom, right_branch_initial,
                            color=GREY_B, stroke_width=3.0)
        left_completion = Line(left_branch_initial, nrem_box.get_top(),
                               color=GREY_B, stroke_width=3.0)
        right_completion = Line(right_branch_initial, rem_box.get_top(),
                                color=GREY_B, stroke_width=3.0)

        # NREM stage boxes below NREM, progressively darker
        stage_centers_y = [0.55, -0.30, -1.15]
        stage_fills = [0.25, 0.45, 0.70]
        stage_labels = ["Stage 1", "Stage 2", "Stage 3"]
        stage_boxes = []
        for label, fill, y in zip(stage_labels, stage_fills, stage_centers_y):
            box = RoundedRectangle(
                corner_radius=0.12,
                width=1.9,
                height=0.6,
                fill_color=BLUE,
                fill_opacity=fill,
                stroke_color=WHITE,
                stroke_width=1.6,
            )
            txt = Text(label, font_size=18, color=WHITE)
            grp = VGroup(box, txt)
            grp.move_to(np.array([-3.5, y, 0]))
            txt.move_to(box.get_center())
            stage_boxes.append(grp)

        stage_lines = [
            Line(nrem_box.get_bottom(), stage_boxes[0].get_top(),
                 color=GREY_B, stroke_width=2.4),
            Line(stage_boxes[0].get_bottom(), stage_boxes[1].get_top(),
                 color=GREY_B, stroke_width=2.4),
            Line(stage_boxes[1].get_bottom(), stage_boxes[2].get_top(),
                 color=GREY_B, stroke_width=2.4),
        ]

        # Small waveform thumbnails for each stage and REM
        def make_thumb(cycles, amp, burst=False):
            rect = RoundedRectangle(
                corner_radius=0.06,
                width=0.95,
                height=0.45,
                fill_color=BLACK,
                fill_opacity=0.4,
                stroke_color=GREY_B,
                stroke_width=1.0,
            )
            u = np.linspace(0, 1, 90)
            if burst:
                y = (
                    0.10 * np.sin(2 * np.pi * 2.5 * u)
                    + 0.18 * np.exp(-((u - 0.30) / 0.10) ** 2)
                    * np.sin(2 * np.pi * 9 * u)
                    + 0.18 * np.exp(-((u - 0.70) / 0.10) ** 2)
                    * np.sin(2 * np.pi * 10 * u - 0.8)
                )
            else:
                y = amp * np.sin(2 * np.pi * cycles * u) + 0.04 * np.sin(
                    2 * np.pi * (cycles + 2) * u + 0.9
                )
            wave = VMobject()
            wave.set_stroke(color=GREY_B, width=1.6, opacity=0.75)
            left = rect.get_left()[0] + 0.06
            right = rect.get_right()[0] - 0.06
            xs = np.linspace(left, right, 90)
            cy = rect.get_center()[1]
            wave.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )
            return VGroup(rect, wave)

        stage1_thumb = make_thumb(4, 0.16)
        stage2_thumb = make_thumb(2.4, 0.12, burst=True)
        stage3_thumb = make_thumb(1, 0.30)
        rem_thumb = make_thumb(7, 0.09)

        stage1_thumb.next_to(stage_boxes[0], RIGHT, buff=0.55)
        stage2_thumb.next_to(stage_boxes[1], RIGHT, buff=0.55)
        stage3_thumb.next_to(stage_boxes[2], RIGHT, buff=0.55)
        rem_thumb.next_to(rem_group, RIGHT, buff=0.55)

        # ------------------------------------------------------------------
        # Bottom waveform panels
        # ------------------------------------------------------------------
        wake_panel_bg = RoundedRectangle(
            corner_radius=0.15,
            width=12.0,
            height=1.0,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_color=TEAL,
            stroke_width=1.5,
        )
        wake_panel_bg.move_to(np.array([0, -2.1, 0]))

        wake_label = Text("Wakefulness", font_size=22, color=TEAL, weight="BOLD")
        wake_label.move_to(
            np.array([
                wake_panel_bg.get_left()[0] + wake_label.width / 2 + 0.6,
                wake_panel_bg.get_top()[1] + 0.18,
                0,
            ])
        )

        wake_fast_wave = VMobject()
        wake_fast_wave.set_stroke(color=GREY_B, width=1.8, opacity=0.0)
        wake_alpha_wave = VMobject()
        wake_alpha_wave.set_stroke(color=ORANGE, width=3.0, opacity=0.0)

        def update_wake_fast(mob):
            left = wake_panel_bg.get_left()[0] + 0.2
            right = wake_panel_bg.get_right()[0] - 0.2
            cy = wake_panel_bg.get_center()[1]
            t = wave_time.get_value()
            u = np.linspace(0, 1, 160)
            xs = left + u * (right - left)
            y = 0.045 * np.sin(2 * np.pi * 22 * u - 9 * t) + 0.025 * np.sin(
                2 * np.pi * 37 * u - 15 * t + 1.3
            )
            mob.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )

        def update_wake_alpha(mob):
            left = wake_panel_bg.get_left()[0] + 0.2
            right = wake_panel_bg.get_right()[0] - 0.2
            cy = wake_panel_bg.get_center()[1]
            t = wave_time.get_value()
            u = np.linspace(0, 1, 160)
            xs = left + u * (right - left)
            amp = alpha_amp.get_value()
            y = amp * np.sin(2 * np.pi * 9 * u - 1.5 * t)
            mob.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )

        alpha_caption = Text("alpha rhythm (~10 Hz)", font_size=20, color=ORANGE)
        alpha_caption.move_to(
            np.array([
                wake_panel_bg.get_right()[0] - alpha_caption.width / 2 - 0.6,
                wake_panel_bg.get_top()[1] + 0.18,
                0,
            ])
        )

        light_panel_bg = RoundedRectangle(
            corner_radius=0.15,
            width=12.0,
            height=0.9,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_color=BLUE,
            stroke_width=1.5,
        )
        light_panel_bg.move_to(np.array([0, -3.4, 0]))

        light_label = Text("Light sleep (Stage 1)", font_size=20, color=BLUE, weight="BOLD")
        light_label.move_to(
            np.array([
                light_panel_bg.get_left()[0] + light_label.width / 2 + 0.6,
                light_panel_bg.get_top()[1] + 0.16,
                0,
            ])
        )

        light_bg_wave = VMobject()
        light_bg_wave.set_stroke(color=GREY_B, width=1.4, opacity=0.0)
        light_slow_wave = VMobject()
        light_slow_wave.set_stroke(color=GREEN, width=2.8, opacity=0.0)

        def update_light_bg(mob):
            left = light_panel_bg.get_left()[0] + 0.2
            right = light_panel_bg.get_right()[0] - 0.2
            cy = light_panel_bg.get_center()[1]
            t = wave_time.get_value()
            u = np.linspace(0, 1, 150)
            xs = left + u * (right - left)
            cyc = light_bg_cycles.get_value()
            y = 0.04 * np.sin(2 * np.pi * cyc * u - 2.0 * t) + 0.02 * np.sin(
                2 * np.pi * (cyc + 3) * u - 4 * t
            )
            mob.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )

        def update_light_slow(mob):
            left = light_panel_bg.get_left()[0] + 0.2
            right = light_panel_bg.get_right()[0] - 0.2
            cy = light_panel_bg.get_center()[1]
            t = wave_time.get_value()
            u = np.linspace(0, 1, 150)
            xs = left + u * (right - left)
            amp = slow_amp.get_value()
            y = amp * np.sin(2 * np.pi * 3 * u - 0.8 * t)
            mob.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )

        wake_fast_wave.add_updater(update_wake_fast)
        wake_alpha_wave.add_updater(update_wake_alpha)
        light_bg_wave.add_updater(update_light_bg)
        light_slow_wave.add_updater(update_light_slow)

        # Add waves to scene now so updaters run throughout; hidden until needed.
        self.add(wake_fast_wave, wake_alpha_wave, light_bg_wave, light_slow_wave)

        # ------------------------------------------------------------------
        # Timed beats
        # ------------------------------------------------------------------
        # Beat 1: 0.00–2.72 — fade previous composition, show Sleep, draw initial branches
        advance(0.30, FadeOut(prev_composition), FadeIn(sleep_title))
        advance(2.42, Create(left_branch), Create(right_branch))

        # Gap to 3.44
        advance(0.72)

        # Beat 2: 3.44–6.08 — left branch completes, NREM box appears
        advance(1.00, Create(left_completion))
        advance(1.64, GrowFromCenter(nrem_group))

        # Gap to 6.54
        advance(0.46)

        # Beat 3: 6.54–8.86 — right branch completes, REM box appears
        advance(0.90, Create(right_completion))
        advance(1.42, GrowFromCenter(rem_group))

        # Gap to 9.48
        advance(0.62)

        # Beat 4: 9.48–14.68 — three NREM stage boxes appear in sequence
        per_stage = 5.20 / 3
        for line, box in zip(stage_lines, stage_boxes):
            advance(per_stage * 0.35, Create(line))
            advance(per_stage * 0.65, GrowFromCenter(box))

        # Gap to 15.44
        advance(0.76)

        # Beat 5: 15.44–18.68 — small waveform thumbnails beside stages and REM
        thumbs = [stage1_thumb, stage2_thumb, stage3_thumb, rem_thumb]
        per_thumb = 3.24 / 4
        for thumb in thumbs:
            advance(per_thumb * 0.75, GrowFromCenter(thumb))
            advance(per_thumb * 0.25)

        # Gap to 19.46
        advance(0.78)

        # Beat 6: 19.46–23.66 — full-width Wakefulness panel, fast scrolling wave
        advance(0.80, FadeIn(wake_panel_bg), FadeIn(wake_label))
        advance(3.40, FadeIn(wake_fast_wave))

        # Gap to 24.44
        advance(0.78)

        # Beat 7: 24.44–28.90 — alpha rhythm overlay, prominent against faster background
        advance(1.20, alpha_amp.animate.set_value(0.27),
                wake_alpha_wave.animate.set_opacity(1))
        advance(0.80, FadeIn(alpha_caption))
        advance(2.46)

        # Gap to 29.90
        advance(1.00)

        # Beat 8: 29.90–36.77 — light sleep panel appears, transition to slower rhythm
        advance(0.90, FadeIn(light_panel_bg), FadeIn(light_label),
                FadeIn(light_bg_wave))
        advance(4.00,
                alpha_amp.animate.set_value(0.02),
                slow_amp.animate.set_value(0.38),
                light_slow_wave.animate.set_opacity(1),
                light_bg_cycles.animate.set_value(6.0))
        advance(1.97)