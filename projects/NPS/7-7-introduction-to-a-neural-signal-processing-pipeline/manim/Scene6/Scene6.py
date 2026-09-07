ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Color palette
        C_SLEEP = BLUE
        C_EPILEPSY = TEAL
        C_MOVEMENT = GREEN
        C_BCI = ORANGE

        def make_application_card(label, accent_color):
            rect = RoundedRectangle(
                width=2.5,
                height=0.9,
                corner_radius=0.15,
                fill_color=WHITE,
                fill_opacity=1,
                stroke_color=accent_color,
                stroke_width=4,
            )
            text = Text(label, font_size=22, color=BLACK, weight="BOLD")
            text.scale_to_fit_width(rect.width - 0.4)
            text.move_to(rect.get_center())
            return VGroup(rect, text)

        # Beat 1: blank screen 0.00–3.54
        self.wait(max(0.05, 3.54))

        # Gap to 4.16
        self.wait(max(0.05, 0.62))

        # Beat 2: application cards 4.16–5.26
        labels = [
            "Sleep staging",
            "Epilepsy detection",
            "Movement analysis",
            "Brain-computer interface",
        ]
        colors = [C_SLEEP, C_EPILEPSY, C_MOVEMENT, C_BCI]
        cards = [
            make_application_card(lab, col)
            for lab, col in zip(labels, colors)
        ]
        cards_group = VGroup(*cards).arrange(RIGHT, buff=0.4)
        cards_group.to_edge(UP, buff=0.75)

        self.play(FadeIn(cards_group, shift=UP * 0.1), run_time=max(0.05, 1.10))

        card1, card2, card3, card4 = cards
        other_cards = VGroup(card2, card3, card4)

        def pulse_card(card, accent, run_time):
            self.play(
                card[0].animate.set_stroke(color=accent, width=10),
                card.animate.scale(1.06),
                run_time=max(0.05, run_time),
            )
            self.play(
                card[0].animate.set_stroke(color=accent, width=4),
                card.animate.scale(1 / 1.06),
                run_time=max(0.05, run_time),
            )

        # Beat 3: pulses 6.04–11.00
        self.wait(max(0.05, 0.78))  # 5.26 -> 6.04
        pulse_card(card1, C_SLEEP, 0.35)
        self.wait(max(0.05, 0.34))  # -> 7.08
        pulse_card(card2, C_EPILEPSY, 0.35)
        self.wait(max(0.05, 0.72))  # -> 8.50
        pulse_card(card3, C_MOVEMENT, 0.35)
        self.wait(max(0.05, 0.60))  # -> 9.80
        pulse_card(card4, C_BCI, 0.35)
        self.wait(max(0.05, 0.50))  # -> 11.00

        # Beat 4: downward arrow hint 11.72–13.70
        self.wait(max(0.05, 0.72))
        arrow_hint = Arrow(
            start=card1.get_bottom() + DOWN * 0.05,
            end=card1.get_bottom() + DOWN * 0.65,
            color=GREY_B,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(Create(arrow_hint), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 0.78))

        # Beat 5: sleep staging card expands, others cluster 14.88–16.20
        self.wait(max(0.05, 1.18))
        self.play(
            card1[0].animate.set_stroke(color=C_SLEEP, width=6),
            card1.animate.scale(1.2).move_to(np.array([0, 2.8, 0])),
            other_cards.animate.scale(0.6).set_opacity(0.45).to_corner(UR, buff=0.45),
            FadeOut(arrow_hint),
            run_time=max(0.05, 0.80),
        )

        end_y = card1.get_bottom()[1]
        connector_to_raw = Arrow(
            start=card1.get_bottom() + DOWN * 0.05,
            end=np.array([0, end_y - 0.5, 0]),
            color=GREY_B,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )
        self.play(Create(connector_to_raw), run_time=max(0.05, 0.52))

        pipeline_mobs = [connector_to_raw]

        # Beat 6: raw EEG trace 16.90–17.80
        self.wait(max(0.05, 0.70))

        rng = np.random.RandomState(42)
        xs = np.linspace(-1.6, 1.6, 60)
        ys = (
            0.28 * np.sin(2.5 * xs)
            + 0.18 * np.sin(7 * xs)
            + 0.12 * np.sin(17 * xs)
            + 0.04 * rng.randn(len(xs))
        )
        points = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
        trace_segments = VGroup(
            *[
                Line(points[i], points[i + 1], color=C_SLEEP, stroke_width=2.0)
                for i in range(len(points) - 1)
            ]
        )
        baseline = Line(
            start=LEFT * 1.6,
            end=RIGHT * 1.6,
            color=GREY_B,
            stroke_width=1.2,
        )
        raw_label = Text("Raw EEG", font_size=20, color=C_SLEEP, weight="BOLD")
        raw_label.next_to(baseline, DOWN, buff=0.20)

        raw_eeg_group = VGroup(baseline, trace_segments, raw_label)
        raw_eeg_group.move_to(
            np.array([0, connector_to_raw.get_end()[1] - 0.4, 0])
        )

        self.play(FadeIn(raw_eeg_group, shift=UP * 0.1), run_time=max(0.05, 0.90))
        pipeline_mobs.append(raw_eeg_group)

        # Beat 7: preprocessing box 18.54–21.54
        self.wait(max(0.05, 0.74))

        pre_box = RoundedRectangle(
            width=3.4,
            height=1.0,
            corner_radius=0.1,
            fill_color=TEAL,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=2,
        )
        pre_box.move_to(np.array([0, 0.1, 0]))
        pre_label = Text("Preprocessing", font_size=24, color=WHITE, weight="BOLD")
        pre_label.move_to(pre_box.get_top() + DOWN * 0.25)
        pre_sub1 = Text("Remove artifacts", font_size=17, color=WHITE)
        pre_sub1.next_to(pre_label, DOWN, buff=0.12).shift(RIGHT * 0.25)
        pre_sub2 = Text("Apply appropriate filtering", font_size=17, color=WHITE)
        pre_sub2.next_to(pre_sub1, DOWN, buff=0.10).shift(RIGHT * 0.25)
        pre_sub2.scale_to_fit_width(2.8)
        pre_sub1.set_opacity(0)
        pre_sub2.set_opacity(0)

        arrow_raw_pre = Arrow(
            start=raw_eeg_group.get_bottom() + DOWN * 0.05,
            end=pre_box.get_top() + UP * 0.05,
            color=WHITE,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            Create(arrow_raw_pre),
            FadeIn(pre_box),
            FadeIn(pre_label),
            run_time=max(0.05, 0.88),
        )
        self.play(FadeIn(pre_sub1), run_time=max(0.05, 0.56))
        self.wait(max(0.05, 0.56))
        self.play(FadeIn(pre_sub2), run_time=max(0.05, 1.00))

        pipeline_mobs.extend([arrow_raw_pre, pre_box, pre_label, pre_sub1, pre_sub2])

        # Beat 8: feature extraction box 22.22–25.06
        self.wait(max(0.05, 0.68))

        feature_box = RoundedRectangle(
            width=3.4,
            height=0.8,
            corner_radius=0.1,
            fill_color=GREEN,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=2,
        )
        feature_box.move_to(np.array([0, -0.9, 0]))
        feature_label = Text("Feature Extraction", font_size=22, color=WHITE, weight="BOLD")
        feature_label.move_to(feature_box.get_top() + DOWN * 0.28)
        feature_sub = Text("Calculate frequency-band power", font_size=16, color=WHITE)
        feature_sub.next_to(feature_label, DOWN, buff=0.12).shift(RIGHT * 0.25)
        feature_sub.scale_to_fit_width(3.0)
        feature_sub.set_opacity(0)

        arrow_pre_feat = Arrow(
            start=pre_box.get_bottom() + DOWN * 0.05,
            end=feature_box.get_top() + UP * 0.05,
            color=WHITE,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            Create(arrow_pre_feat),
            FadeIn(feature_box),
            FadeIn(feature_label),
            run_time=max(0.05, 1.34),
        )
        self.play(FadeIn(feature_sub), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.70))

        pipeline_mobs.extend([arrow_pre_feat, feature_box, feature_label, feature_sub])

        # Beat 9: classification box 25.46–28.46
        self.wait(max(0.05, 0.40))

        class_box = RoundedRectangle(
            width=3.4,
            height=0.8,
            corner_radius=0.1,
            fill_color=ORANGE,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=2,
        )
        class_box.move_to(np.array([0, -1.85, 0]))
        class_label = Text("Classification", font_size=22, color=WHITE, weight="BOLD")
        class_label.move_to(class_box.get_top() + DOWN * 0.28)
        class_sub = Text("Classify into sleep stage", font_size=16, color=WHITE)
        class_sub.next_to(class_label, DOWN, buff=0.12).shift(RIGHT * 0.25)
        class_sub.scale_to_fit_width(3.0)
        class_sub.set_opacity(0)

        arrow_feat_class = Arrow(
            start=feature_box.get_bottom() + DOWN * 0.05,
            end=class_box.get_top() + UP * 0.05,
            color=WHITE,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            Create(arrow_feat_class),
            FadeIn(class_box),
            FadeIn(class_label),
            run_time=max(0.05, 1.22),
        )
        self.play(FadeIn(class_sub), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.98))

        pipeline_mobs.extend([arrow_feat_class, class_box, class_label, class_sub])

        # Beat 10: output box 28.94–31.94
        self.wait(max(0.05, 0.48))

        output_box = RoundedRectangle(
            width=3.6,
            height=0.65,
            corner_radius=0.1,
            fill_color=WHITE,
            fill_opacity=0.95,
            stroke_color=GOLD,
            stroke_width=2,
        )
        output_box.move_to(np.array([0, -2.65, 0]))
        output_label = Text("Output", font_size=20, color=BLACK, weight="BOLD")
        output_label.move_to(output_box.get_top() + DOWN * 0.18)

        wake_label = Text("Wake", font_size=18, color=GOLD, weight="BOLD")
        nrem_label = Text("NREM", font_size=18, color=PURPLE, weight="BOLD")
        rem_label = Text("REM", font_size=18, color=PINK, weight="BOLD")
        output_labels = VGroup(wake_label, nrem_label, rem_label).arrange(
            RIGHT, buff=0.25
        )
        output_labels.move_to(output_box.get_bottom() + UP * 0.28)
        wake_label.set_opacity(0)
        nrem_label.set_opacity(0)
        rem_label.set_opacity(0)

        arrow_class_out = Arrow(
            start=class_box.get_bottom() + DOWN * 0.05,
            end=output_box.get_top() + UP * 0.05,
            color=WHITE,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            Create(arrow_class_out),
            FadeIn(output_box),
            FadeIn(output_label),
            run_time=max(0.05, 0.44),
        )
        self.play(FadeIn(wake_label), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.04))
        self.play(FadeIn(nrem_label), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.34))
        self.play(FadeIn(rem_label), run_time=max(0.05, 0.18))

        pipeline_mobs.extend(
            [
                arrow_class_out,
                output_box,
                output_label,
                wake_label,
                nrem_label,
                rem_label,
            ]
        )

        # Beat 11: gentle whole-pipeline pulse 32.72–36.54
        self.wait(max(0.05, 0.78))
        pipeline_group = VGroup(*pipeline_mobs)
        self.play(pipeline_group.animate.scale(1.02), run_time=max(0.05, 0.70))
        self.play(pipeline_group.animate.scale(1 / 1.02), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 2.42))

        # Beat 12: goal text and hold 37.40–43.02
        self.wait(max(0.05, 0.86))
        goal_text = Text(
            "Goal: understand why each stage is necessary\nand how the stages connect together",
            font_size=26,
            color=WHITE,
            weight="SEMIBOLD",
            line_spacing=0.8,
        )
        goal_text.scale_to_fit_width(11)
        goal_text.move_to(np.array([0, -3.3, 0]))
        self.play(FadeIn(goal_text, shift=UP * 0.1), run_time=max(0.05, 1.50))
        self.wait(max(0.05, 3.34))
        self.wait(max(0.05, 0.78))