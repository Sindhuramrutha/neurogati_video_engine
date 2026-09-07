ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- small helpers ----------
        def make_wave_mobject(
            freq=3.0,
            amp=0.12,
            width=1.0,
            height=0.4,
            color=WHITE,
            stroke_width=1.5,
            phase=0.0,
            n=140,
        ):
            xs = np.linspace(-width / 2.0, width / 2.0, n)
            t = np.linspace(0, 1, n)
            y = amp * np.sin(2 * np.pi * freq * t + phase)
            wave = VMobject()
            wave.set_points_as_corners([np.array([x, yy, 0.0]) for x, yy in zip(xs, y)])
            wave.set_stroke(color, width=stroke_width)
            wave.set_fill(opacity=0)
            return wave

        def make_burst_wave(width=0.7, height=0.3, color=PURPLE):
            xs = np.linspace(-width / 2.0, width / 2.0, 220)
            t = np.linspace(0, 1, 220)
            y = np.zeros_like(t)
            bursts = [(0.08, 0.16), (0.42, 0.52), (0.76, 0.84)]
            for a, b in bursts:
                mask = (t >= a) & (t <= b)
                idxs = np.where(mask)[0]
                if len(idxs) > 4:
                    inner = np.linspace(0, 4 * np.pi, len(idxs))
                    y[idxs] = height * 0.42 * np.sin(inner) * np.exp(-np.linspace(0, 1.8, len(idxs)))
            y += 0.025 * height * np.sin(2 * np.pi * 40 * t)
            wave = VMobject()
            wave.set_points_as_corners([np.array([x, yy, 0.0]) for x, yy in zip(xs, y)])
            wave.set_stroke(color, width=1.6)
            wave.set_fill(opacity=0)
            return wave

        def make_mixed_wave(width=0.7, height=0.3, color=ORANGE, seed=7):
            np.random.seed(seed)
            xs = np.linspace(-width / 2.0, width / 2.0, 220)
            t = np.linspace(0, 1, 220)
            y = (
                0.16 * np.sin(2 * np.pi * 9.0 * t)
                + 0.10 * np.sin(2 * np.pi * 3.0 * t + 1.2)
                + 0.08 * np.sin(2 * np.pi * 16.0 * t + 0.4)
                + 0.05 * np.random.randn(len(t))
            )
            y = y / (np.max(np.abs(y)) + 1e-6) * (height * 0.45)
            wave = VMobject()
            wave.set_points_as_corners([np.array([x, yy, 0.0]) for x, yy in zip(xs, y)])
            wave.set_stroke(color, width=1.6)
            wave.set_fill(opacity=0)
            return wave

        def make_check_icon(height=0.32):
            circle = Circle(radius=height / 2.0, fill_color=GREEN, fill_opacity=1, stroke_width=0)
            c = circle.get_center()
            line1 = Line(
                c + LEFT * 0.10 + DOWN * 0.03,
                c + LEFT * 0.01 + UP * 0.09,
                color=WHITE,
                stroke_width=3.5,
            )
            line2 = Line(
                c + LEFT * 0.01 + UP * 0.09,
                c + RIGHT * 0.12 + DOWN * 0.08,
                color=WHITE,
                stroke_width=3.5,
            )
            return VGroup(circle, line1, line2)

        def fit_content(content, panel, pad_w=0.38, pad_h=0.30):
            content.scale_to_fit_width(panel.get_width() - pad_w)
            content.scale_to_fit_height(panel.get_height() - pad_h)
            content.move_to(panel.get_center())
            return content

        # ---------- previous scene ending composition ----------
        prev_comp = VGroup()
        prev_labels = ["Raw EEG", "Filter", "Spectral", "Wavelet"]
        for i, lab in enumerate(prev_labels):
            r = RoundedRectangle(
                corner_radius=0.10,
                width=1.8,
                height=1.1,
                stroke_color=GREY_B,
                stroke_width=1.5,
                fill_color="#1A1D26",
                fill_opacity=0.95,
            )
            r.move_to(np.array([-3.9 + i * 2.6, -0.4, 0.0]))
            t = Text(lab, font_size=16, color=GREY_B)
            t.next_to(r, DOWN, buff=0.12)
            prev_comp.add(r, t)
        prev_wave = VMobject()
        prev_xs = np.linspace(-5.8, 5.8, 400)
        prev_wave.set_points_as_corners(
            [np.array([x, 0.7 + 0.18 * np.sin(2 * np.pi * 4 * (x + 5.8) / 11.6), 0.0]) for x in prev_xs]
        )
        prev_wave.set_stroke(GREY_B, width=2)
        prev_comp.add(prev_wave)

        # ---------- title and EEG anchor bar ----------
        main_title = Text("Applications of EEG", font_size=44, color=WHITE, weight="BOLD")
        main_title.to_edge(UP, buff=0.25)

        anchor_rect = RoundedRectangle(
            corner_radius=0.18,
            width=11.6,
            height=0.85,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.95,
        )
        anchor_rect.move_to(UP * 2.5)
        eeg_label = Text("EEG", font_size=24, color=YELLOW, weight="BOLD")
        eeg_label.move_to(anchor_rect.get_left() + RIGHT * 0.75)

        phase_state = {"p": 0.0}

        anchor_wave_xs = np.linspace(
            anchor_rect.get_left()[0] + 1.25,
            anchor_rect.get_right()[0] - 0.40,
            420,
        )

        def update_anchor_wave(wave, dt=0.016):
            phase_state["p"] += dt * 0.8
            t = (anchor_wave_xs - anchor_wave_xs[0]) / (anchor_wave_xs[-1] - anchor_wave_xs[0])
            y = (
                0.08 * np.sin(2 * np.pi * 1.5 * t + phase_state["p"])
                + 0.06 * np.sin(2 * np.pi * 6.0 * t + 1.4 * phase_state["p"])
                + 0.04 * np.sin(2 * np.pi * 12.0 * t + 2.1 * phase_state["p"])
            )
            pts = [
                np.array([x, anchor_rect.get_center()[1] + yy, 0.0])
                for x, yy in zip(anchor_wave_xs, y)
            ]
            wave.set_points_as_corners(pts)

        anchor_wave = VMobject()
        anchor_wave.set_stroke(WHITE, width=2)
        anchor_wave.set_fill(opacity=0)
        anchor_wave.add_updater(update_anchor_wave)
        update_anchor_wave(anchor_wave)

        anchor_group = VGroup(anchor_rect, eeg_label, anchor_wave)

        # ---------- application grid ----------
        panel_width = 2.75
        panel_height = 1.65
        panel_centers = [
            np.array([-1.7, 0.45, 0.0]),
            np.array([1.7, 0.45, 0.0]),
            np.array([-1.7, -1.65, 0.0]),
            np.array([1.7, -1.65, 0.0]),
        ]
        panel_rects = []
        for p in panel_centers:
            panel = RoundedRectangle(
                corner_radius=0.12,
                width=panel_width,
                height=panel_height,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_color="#1A1D26",
                fill_opacity=0.95,
            )
            panel.move_to(p)
            panel_rects.append(panel)
        grid_group = VGroup(*panel_rects)

        faint_brain = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=WHITE,
            fill_opacity=0.3,
            stroke_color=WHITE,
            stroke_width=1.2,
            height=0.95,
        ).move_to(panel_rects[0].get_center())

        gauge_placeholder = VGroup(
            Arc(radius=0.42, start_angle=PI / 2, angle=PI, color=WHITE, stroke_width=2),
            Line(ORIGIN, UP * 0.38 + RIGHT * 0.18, color=WHITE, stroke_width=1.8),
        )
        gauge_placeholder.move_to(panel_rects[1].get_center())
        gauge_placeholder.set_opacity(0.3)

        spectrum_placeholder = VGroup()
        spec_heights = [0.15, 0.28, 0.42, 0.30, 0.50]
        for i, h in enumerate(spec_heights):
            bar = Rectangle(
                width=0.13,
                height=h,
                fill_color=WHITE,
                fill_opacity=0.35,
                stroke_width=0,
            )
            bar.shift(RIGHT * (i - 2) * 0.19)
            spectrum_placeholder.add(bar)
        spectrum_placeholder.move_to(panel_rects[2].get_center())
        spectrum_placeholder.set_opacity(0.3)

        loop_placeholder = SVGMobject(
            ASSET_PATHS["arrow_repeat"],
            fill_color=WHITE,
            fill_opacity=0.3,
            stroke_color=WHITE,
            stroke_width=1.2,
            height=0.95,
        ).move_to(panel_rects[3].get_center())

        place_icons = [faint_brain, gauge_placeholder, spectrum_placeholder, loop_placeholder]

        # ---------- Beat 1: clear previous composition, show title + EEG anchor ----------
        self.add(prev_comp)
        self.wait(max(0.05, 0.30))
        self.play(
            FadeOut(prev_comp),
            FadeIn(main_title),
            FadeIn(anchor_group),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.70))

        # ---------- Beat 2: 2x2 empty panels with faint icons ----------
        self.play(FadeIn(grid_group), run_time=max(0.05, 0.80))
        for icon in place_icons:
            self.play(GrowFromCenter(icon), run_time=max(0.05, 0.45))
        practice_caption = Text(
            "Neuroscience and clinical practice", font_size=22, color=GREY_B
        )
        practice_caption.next_to(grid_group, DOWN, buff=0.35)
        self.play(FadeIn(practice_caption), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.48))
        self.play(FadeOut(practice_caption), run_time=max(0.05, 0.50))

        self.wait(max(0.05, 1.02))  # gap 6.28-7.30

        # ---------- Beat 3: cognitive neuroscience panel active ----------
        self.play(
            place_icons[0].animate.set_opacity(1.0).set_stroke(width=2).set_color(WHITE),
            *[icon.animate.set_opacity(0.20) for icon in place_icons[1:]],
            panel_rects[0].animate.set_stroke(color=YELLOW, width=3),
            run_time=max(0.05, 0.50),
        )

        brain_center = panel_rects[0].get_center() + DOWN * 0.10

        # task icons
        eye_icon = VGroup(
            Ellipse(width=0.40, height=0.20, fill_color=WHITE, fill_opacity=0.95, stroke_color=WHITE, stroke_width=1.2),
            Circle(radius=0.07, fill_color=BLUE, fill_opacity=1, stroke_width=0),
        )
        eye_icon.scale_to_fit_height(0.38)

        thought_icon = VGroup(
            Circle(radius=0.13, fill_color=WHITE, fill_opacity=0.95, stroke_width=0),
            Circle(radius=0.07, fill_color=WHITE, fill_opacity=0.95, stroke_width=0).move_to(LEFT * 0.11 + DOWN * 0.09),
            Polygon(
                ORIGIN + LEFT * 0.02,
                ORIGIN + LEFT * 0.12 + DOWN * 0.10,
                ORIGIN + RIGHT * 0.02 + DOWN * 0.04,
                fill_color=WHITE,
                fill_opacity=0.95,
                stroke_width=0,
            ),
        )
        thought_icon.scale_to_fit_height(0.38)

        speech_icon = VGroup(
            RoundedRectangle(corner_radius=0.08, width=0.42, height=0.24, fill_color=WHITE, fill_opacity=0.95, stroke_width=0),
            Polygon(
                ORIGIN + LEFT * 0.06,
                ORIGIN + LEFT * 0.14 + DOWN * 0.10,
                ORIGIN + LEFT * 0.02 + DOWN * 0.04,
                fill_color=WHITE,
                fill_opacity=0.95,
                stroke_width=0,
            ),
        )
        speech_icon.scale_to_fit_height(0.38)

        branch_icon = VGroup(
            Arrow(ORIGIN, UP * 0.26 + RIGHT * 0.04, color=WHITE, stroke_width=2, buff=0.02, max_tip_length_to_length_ratio=0.35),
            Arrow(ORIGIN, RIGHT * 0.26, color=WHITE, stroke_width=2, buff=0.02, max_tip_length_to_length_ratio=0.35),
            Arrow(ORIGIN, DOWN * 0.26 + RIGHT * 0.04, color=WHITE, stroke_width=2, buff=0.02, max_tip_length_to_length_ratio=0.35),
        )
        branch_icon.scale_to_fit_height(0.38)

        def make_task_marker(icon, label_text):
            label = Text(label_text, font_size=9, color=WHITE)
            marker = VGroup(icon, label)
            marker.arrange(DOWN, buff=0.05)
            marker.scale_to_fit_width(0.62)
            return marker

        eye_mark = make_task_marker(eye_icon, "Attention")
        thought_mark = make_task_marker(thought_icon, "Memory")
        speech_mark = make_task_marker(speech_icon, "Language")
        branch_mark = make_task_marker(branch_icon, "Decision-making")

        eye_mark.move_to(brain_center + LEFT * 0.72 + UP * 0.52)
        thought_mark.move_to(brain_center + RIGHT * 0.72 + UP * 0.52)
        speech_mark.move_to(brain_center + LEFT * 0.72 + DOWN * 0.52)
        branch_mark.move_to(brain_center + RIGHT * 0.72 + DOWN * 0.52)

        task_markers = [eye_mark, thought_mark, speech_mark, branch_mark]
        task_icons = [eye_icon, thought_icon, speech_icon, branch_icon]

        for mark in task_markers:
            self.play(GrowFromCenter(mark), run_time=max(0.05, 0.38))
            self.wait(max(0.05, 0.08))

        cognitive_label = Text("Cognitive Neuroscience", font_size=15, color=WHITE)
        cognitive_label.next_to(panel_rects[0], DOWN, buff=0.14)
        self.play(FadeIn(cognitive_label), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.48))

        # ---------- Beat 4: task icon pulses + mini EEG inside cognitive panel ----------
        cog_wave_strip = make_wave_mobject(
            freq=5.0, amp=0.06, width=panel_width - 0.50, height=0.22, color=GREY_B, stroke_width=1.6
        )
        cog_wave_strip.move_to(panel_rects[0].get_top() + DOWN * 0.28)
        self.play(FadeIn(cog_wave_strip), run_time=max(0.05, 0.50))

        per_pulse_dur = (6.04 - 0.50) / 4.0  # total beat 6.04
        for icon in task_icons:
            self.play(Indicate(icon, color=YELLOW, scale_factor=1.25), run_time=max(0.05, 0.70))
            self.play(
                cog_wave_strip.animate.set_stroke(color=YELLOW, width=3).set_opacity(1),
                run_time=max(0.05, 0.20),
            )
            self.play(
                cog_wave_strip.animate.set_stroke(color=GREY_B, width=1.6).set_opacity(0.7),
                run_time=max(0.05, 0.20),
            )
            self.wait(max(0.05, per_pulse_dur - 1.10))

        self.wait(max(0.05, 0.44))  # gap 17.18-17.62

        # ---------- Beat 5: two mini EEG segments compared ----------
        self.play(
            FadeOut(cog_wave_strip),
            FadeOut(place_icons[0]),
            *[FadeOut(m) for m in task_markers],
            run_time=max(0.05, 0.40),
        )

        task_a_wave = make_wave_mobject(freq=7.0, amp=0.09, width=0.85, height=0.24, color=TEAL)
        task_b_wave = make_wave_mobject(freq=3.0, amp=0.15, width=0.85, height=0.24, color=ORANGE)

        def make_task_wave_card(icon, label_text, wave):
            lab = Text(label_text, font_size=9, color=WHITE)
            icon_copy = icon.copy()
            icon_copy.scale_to_fit_height(0.20)
            card = VGroup(icon_copy, lab, wave)
            card.arrange(DOWN, buff=0.07)
            card.scale_to_fit_width(0.92)
            return card

        card_a = make_task_wave_card(eye_icon, "Task A", task_a_wave)
        card_b = make_task_wave_card(branch_icon, "Task B", task_b_wave)
        card_a.move_to(panel_rects[0].get_center() + LEFT * 0.48)
        card_b.move_to(panel_rects[0].get_center() + RIGHT * 0.48)

        compare_arrow = Arrow(
            card_a.get_right() + RIGHT * 0.07,
            card_b.get_left() + LEFT * 0.07,
            color=YELLOW,
            stroke_width=2.5,
            buff=0.04,
            max_tip_length_to_length_ratio=0.35,
        )

        comparison_group = VGroup(card_a, card_b)
        self.play(GrowFromCenter(comparison_group), run_time=max(0.05, 0.70))
        self.play(Create(compare_arrow), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 2.15))

        self.wait(max(0.05, 0.96))  # gap 21.22-22.18

        # ---------- Beat 6: mental workload panel active ----------
        panel_mw = panel_rects[1]
        mw_center = panel_mw.get_center()
        mw_left_x = mw_center[0] - 0.82
        mw_track_bottom = mw_center[1] - 0.42
        mw_track_top = mw_center[1] + 0.42
        mw_track = Line(
            np.array([mw_left_x, mw_track_bottom, 0.0]),
            np.array([mw_left_x, mw_track_top, 0.0]),
            color=WHITE,
            stroke_width=3,
        )
        mw_pivot = np.array([mw_left_x, mw_track_bottom + 0.05, 0.0])
        mw_needle = Line(mw_pivot, mw_pivot + UP * 0.58, color=RED, stroke_width=2.5)
        mw_needle.rotate(-0.9, about_point=mw_pivot)

        mw_ticks = VGroup()
        for frac in [-0.8, 0.0, 0.8]:
            tick_y = mw_center[1] + frac * 0.38
            mw_ticks.add(
                Line(
                    np.array([mw_left_x - 0.10, tick_y, 0.0]),
                    np.array([mw_left_x + 0.10, tick_y, 0.0]),
                    color=GREY_B,
                    stroke_width=1.5,
                )
            )

        mw_wave = make_wave_mobject(freq=3, amp=0.13, width=1.20, height=0.34, color=GREY_B, stroke_width=1.6)
        mw_wave.move_to(np.array([mw_center[0] + 0.62, mw_center[1], 0.0]))

        mental_content = VGroup(mw_track, mw_ticks, mw_needle, mw_wave)
        mental_label = Text("Mental Workload", font_size=15, color=WHITE)
        mental_label.next_to(panel_mw, DOWN, buff=0.14)

        self.play(
            comparison_group.animate.set_opacity(0.45),
            cognitive_label.animate.set_opacity(0.45),
            FadeOut(gauge_placeholder),
            GrowFromCenter(mental_content),
            FadeIn(mental_label),
            run_time=max(0.05, 0.88),
        )
        self.wait(max(0.05, 0.20))

        self.wait(max(0.05, 0.48))  # gap 23.26-23.74

        # ---------- Beat 7: mental effort then fatigue ----------
        effort_wave = make_wave_mobject(freq=8, amp=0.07, width=1.20, height=0.34, color=YELLOW, stroke_width=1.7)
        effort_wave.move_to(mw_wave.get_center())
        fatigue_wave = make_wave_mobject(freq=3, amp=0.14, width=1.20, height=0.34, color=ORANGE, stroke_width=1.7)
        fatigue_wave.move_to(mw_wave.get_center())

        self.play(
            mw_needle.animate.rotate(1.2, about_point=mw_pivot),
            Transform(mw_wave, effort_wave),
            run_time=max(0.05, 2.20),
        )
        self.play(
            mw_needle.animate.rotate(-0.4, about_point=mw_pivot),
            Transform(mw_wave, fatigue_wave),
            run_time=max(0.05, 1.30),
        )
        self.wait(max(0.05, 0.80))

        self.wait(max(0.05, 0.38))  # gap 28.04-28.42

        # ---------- Beat 8: sustained attention + gauge markers ----------
        focused_wave = make_wave_mobject(freq=6, amp=0.08, width=1.20, height=0.34, color=GREEN, stroke_width=1.7)
        focused_wave.move_to(mw_wave.get_center())

        self.play(
            mw_needle.animate.rotate(0.6, about_point=mw_pivot),
            Transform(mw_wave, focused_wave),
            run_time=max(0.05, 1.40),
        )

        mw_glow = SurroundingRectangle(
            panel_mw,
            color=YELLOW,
            stroke_width=3.5,
            buff=0.08,
            corner_radius=0.10,
        )
        self.play(Create(mw_glow), run_time=max(0.05, 0.35))

        mw_label_effort = Text("Effort", font_size=8, color=YELLOW).move_to(
            np.array([mw_left_x - 0.38, mw_center[1] + 0.28, 0.0])
        )
        mw_label_fatigue = Text("Fatigue", font_size=8, color=ORANGE).move_to(
            np.array([mw_left_x - 0.38, mw_center[1] - 0.22, 0.0])
        )
        mw_label_sustained = Text("Sustained\nattention", font_size=7, color=GREEN, line_spacing=0.6).move_to(
            np.array([mw_left_x - 0.34, mw_center[1] + 0.05, 0.0])
        )
        mw_markers = VGroup(mw_label_effort, mw_label_fatigue, mw_label_sustained)
        self.play(FadeIn(mw_markers), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.98))

        self.wait(max(0.05, 1.08))  # gap 31.60-32.68

        # ---------- Beat 9: consciousness research panel active ----------
        panel_c = panel_rects[2]
        c_center = panel_c.get_center()
        c_left_x = panel_c.get_left()[0] + 0.24
        c_right_x = panel_c.get_right()[0] - 0.24
        c_line_y = c_center[1] - 0.28
        c_line = Line(
            np.array([c_left_x, c_line_y, 0.0]),
            np.array([c_right_x, c_line_y, 0.0]),
            color=WHITE,
            stroke_width=3,
        )

        def state_x(frac):
            return c_left_x + frac * (c_right_x - c_left_x)

        state_positions = [state_x(0.0), state_x(0.35), state_x(0.66), state_x(1.0)]
        state_names = ["Wakefulness", "Sleep", "Anaesthesia", "Altered states"]
        c_state_labels = VGroup()
        for pos, name in zip(state_positions, state_names):
            lab = Text(name, font_size=7, color=GREY_B, line_spacing=0.6)
            lab.scale_to_fit_width(0.78)
            lab.move_to(np.array([pos, c_line_y - 0.18, 0.0]))
            c_state_labels.add(lab)

        c_wave_pos = np.array([c_center[0], c_line_y + 0.34, 0.0])
        c_awake_wave = make_wave_mobject(freq=10, amp=0.06, width=0.75, height=0.30, color=GREEN, stroke_width=1.6)
        c_awake_wave.move_to(c_wave_pos)
        c_sleep_wave = make_wave_mobject(freq=2, amp=0.16, width=0.75, height=0.30, color=BLUE, stroke_width=1.6)
        c_sleep_wave.move_to(c_wave_pos)
        c_anesthesia_wave = make_burst_wave(width=0.75, height=0.30, color=PURPLE)
        c_anesthesia_wave.move_to(c_wave_pos)
        c_altered_wave = make_mixed_wave(width=0.75, height=0.30, color=ORANGE, seed=11)
        c_altered_wave.move_to(c_wave_pos)

        c_playhead = Dot(radius=0.055, color=YELLOW)
        c_playhead.move_to(np.array([state_positions[0], c_line_y, 0.0]))

        c_wave = c_awake_wave.copy()
        conscious_content = VGroup(c_line, c_state_labels, c_wave, c_playhead)
        conscious_label = Text("Consciousness Research", font_size=15, color=WHITE)
        conscious_label.next_to(panel_c, DOWN, buff=0.14)

        self.play(
            mental_content.animate.set_opacity(0.45),
            mental_label.animate.set_opacity(0.45),
            mw_glow.animate.set_opacity(0.30),
            FadeOut(spectrum_placeholder),
            GrowFromCenter(conscious_content),
            FadeIn(conscious_label),
            run_time=max(0.05, 0.82),
        )

        self.wait(max(0.05, 0.82))  # gap 33.50-34.32

        # ---------- Beat 10: consciousness states along spectrum ----------
        state_wave_sequence = [
            (state_positions[0], c_awake_wave),
            (state_positions[1], c_sleep_wave),
            (state_positions[2], c_anesthesia_wave),
            (state_positions[3], c_altered_wave),
        ]
        state_anim_dur = 1.05
        state_hold_dur = 0.76
        for pos, target_wave in state_wave_sequence:
            self.play(
                c_playhead.animate.move_to(pos),
                Transform(c_wave, target_wave),
                run_time=max(0.05, state_anim_dur),
            )
            self.wait(max(0.05, state_hold_dur))

        self.wait(max(0.05, 0.96))  # gap 41.56-42.52

        # ---------- Beat 11: neurofeedback panel active ----------
        panel_n = panel_rects[3]
        n_center = panel_n.get_center()

        n_brain = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
            height=0.55,
        )
        n_monitor = RoundedRectangle(
            corner_radius=0.07,
            width=0.72,
            height=0.60,
            stroke_color=WHITE,
            stroke_width=1.6,
            fill_color="#1A1D26",
            fill_opacity=1,
        )
        n_screen = Rectangle(
            width=0.62,
            height=0.42,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=1,
        ).move_to(n_monitor.get_center())
        n_monitor_wave = make_wave_mobject(freq=5, amp=0.04, width=0.56, height=0.14, color=GREEN, stroke_width=1.2)
        n_monitor_wave.move_to(n_screen.get_center())

        n_brain.move_to(panel_n.get_left() + RIGHT * 0.52)
        n_monitor.move_to(panel_n.get_right() + LEFT * 0.56)

        n_forward = Arrow(
            np.array([n_brain.get_center()[0] + 0.06, n_brain.get_top()[1] + 0.14, 0.0]),
            np.array([n_monitor.get_center()[0] - 0.06, n_monitor.get_top()[1] + 0.14, 0.0]),
            color=YELLOW,
            stroke_width=2.2,
            buff=0.04,
            max_tip_length_to_length_ratio=0.22,
        )
        n_return = Arrow(
            np.array([n_monitor.get_center()[0] - 0.06, n_monitor.get_bottom()[1] - 0.14, 0.0]),
            np.array([n_brain.get_center()[0] + 0.06, n_brain.get_bottom()[1] - 0.14, 0.0]),
            color=YELLOW,
            stroke_width=2.2,
            buff=0.04,
            max_tip_length_to_length_ratio=0.22,
        )

        neuro_content = VGroup(n_brain, n_monitor, n_monitor_wave, n_forward, n_return)
        neuro_content.scale_to_fit_width(panel_width - 0.40)
        neuro_content.scale_to_fit_height(panel_height - 0.32)
        neuro_content.move_to(panel_n.get_center())

        neuro_label = Text("Neurofeedback", font_size=15, color=WHITE)
        neuro_label.next_to(panel_n, DOWN, buff=0.14)

        self.play(
            conscious_content.animate.set_opacity(0.45),
            conscious_label.animate.set_opacity(0.45),
            FadeOut(loop_placeholder),
            GrowFromCenter(neuro_content),
            FadeIn(neuro_label),
            run_time=max(0.05, 0.90),
        )

        self.wait(max(0.05, 0.34))  # gap 43.42-43.76

        # ---------- Beat 12: neurofeedback loop cycles ----------
        real_time_label = Text("Real-time", font_size=10, color=YELLOW)
        real_time_label.next_to(n_monitor, UP, buff=0.10)
        self.play(FadeIn(real_time_label), run_time=max(0.05, 0.40))

        signal_dot = Dot(radius=0.045, color=YELLOW)
        signal_dot.move_to(n_forward.get_start())

        cycle_forward_dur = 0.90
        cycle_update_dur = 0.35
        cycle_highlight_dur = 0.25
        cycle_return_dur = 0.90
        pulse_dur = 0.25

        for cycle in range(3):
            signal_dot.move_to(n_forward.get_start())
            self.play(signal_dot.animate.move_to(n_forward.get_end()), run_time=max(0.05, cycle_forward_dur))

            new_monitor_wave = make_wave_mobject(
                freq=4 + cycle * 2,
                amp=0.04,
                width=0.56,
                height=0.14,
                color=GREEN,
                stroke_width=1.2,
            )
            new_monitor_wave.move_to(n_screen.get_center())
            self.play(Transform(n_monitor_wave, new_monitor_wave), run_time=max(0.05, cycle_update_dur))
            self.play(
                n_monitor_wave.animate.set_stroke(color=YELLOW, width=2.0),
                run_time=max(0.05, cycle_highlight_dur),
            )

            signal_dot.move_to(n_return.get_start())
            self.play(signal_dot.animate.move_to(n_return.get_end()), run_time=max(0.05, cycle_return_dur))

            self.play(n_brain.animate.scale(1.10), run_time=max(0.05, pulse_dur))
            self.play(n_brain.animate.scale(1 / 1.10), run_time=max(0.05, pulse_dur))

        self.wait(max(0.05, 0.22))

        self.wait(max(0.05, 1.00))  # gap 53.08-54.08

        # ---------- Beat 13: shrink app grid, create advantages panel ----------
        application_group = VGroup(
            *panel_rects,
            cognitive_label,
            comparison_group,
            compare_arrow,
            mental_content,
            mental_label,
            mw_glow,
            mw_markers,
            conscious_content,
            conscious_label,
            neuro_content,
            neuro_label,
            real_time_label,
        )

        adv_panel = RoundedRectangle(
            corner_radius=0.15,
            width=5.8,
            height=6.4,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.97,
        )
        adv_panel.move_to(np.array([3.5, -0.35, 0.0]))
        adv_title = Text("Advantages of EEG", font_size=30, color=WHITE, weight="BOLD")
        adv_title.move_to(adv_panel.get_top() + DOWN * 0.60)

        self.play(
            application_group.animate.scale(0.55).move_to(LEFT * 4.25).set_opacity(0.38),
            FadeOut(main_title),
            FadeOut(anchor_group),
            run_time=max(0.05, 2.20),
        )
        self.play(FadeIn(adv_panel), Write(adv_title), run_time=max(0.05, 1.04))

        self.wait(max(0.05, 0.40))  # gap 57.32-57.72

        # ---------- checklist panel layout ----------
        adv_inner_left = 1.05
        adv_inner_right = 6.00
        row_ys = [1.35, 0.55, -0.25, -1.05, -1.85]

        def make_adv_item(text, graphic, row_y):
            check = make_check_icon(height=0.34)
            check.move_to(np.array([adv_inner_left, row_y, 0.0]))
            label = Text(text, font_size=19, color=WHITE)
            if label.width > 3.10:
                label.scale_to_fit_width(3.10)
            label.next_to(check, RIGHT, buff=0.16)
            graphic.scale_to_fit_height(0.50)
            graphic.move_to(np.array([adv_inner_right, row_y, 0.0]))
            item = VGroup(check, label, graphic)
            return item

        # graphics used in checklist items
        g_stopwatch = SVGMobject(
            ASSET_PATHS["stopwatch"],
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
            height=0.55,
        )

        g_head_sensor = VGroup(
            Circle(radius=0.24, stroke_color=WHITE, stroke_width=2, fill_color=None),
            Dot(point=RIGHT * 0.40, radius=0.055, color=YELLOW),
            Line(RIGHT * 0.20, RIGHT * 0.34, color=GREY_B, stroke_width=1.5),
        )
        g_head_sensor.scale_to_fit_height(0.52)

        g_trace = make_wave_mobject(freq=6, amp=0.10, width=0.85, height=0.30, color=GREEN, stroke_width=2)
        g_trace.scale_to_fit_height(0.44)

        g_clock_line = VGroup(
            Circle(radius=0.22, stroke_color=WHITE, stroke_width=2, fill_color=None),
            Arrow(
                RIGHT * 0.02,
                RIGHT * 0.46,
                color=BLUE,
                stroke_width=2,
                buff=0.04,
                max_tip_length_to_length_ratio=0.35,
            ),
        )
        g_clock_line.scale_to_fit_height(0.52)

        g_processing = VGroup(
            make_wave_mobject(freq=5, amp=0.07, width=0.40, height=0.16, color=GREEN, stroke_width=1.4),
            Arrow(LEFT * 0.10, LEFT * 0.01, color=WHITE, stroke_width=1.5, buff=0.02),
            RoundedRectangle(
                corner_radius=0.04,
                width=0.36,
                height=0.30,
                fill_color=ORANGE,
                fill_opacity=1,
                stroke_width=0,
            ),
            Arrow(RIGHT * 0.01, RIGHT * 0.10, color=WHITE, stroke_width=1.5, buff=0.02),
            make_wave_mobject(freq=8, amp=0.06, width=0.40, height=0.16, color=GREEN, stroke_width=1.4),
        )
        g_processing.arrange(RIGHT, buff=0.05)
        g_processing.scale_to_fit_height(0.45)

        checklist_items = []
        checklist_texts = [
            "Excellent temporal resolution",
            "Non-invasive recording",
            "Continuous monitoring",
            "Long-duration recordings",
            "Real-time signal processing",
        ]
        checklist_graphics = [g_stopwatch, g_head_sensor, g_trace, g_clock_line, g_processing]

        # ---------- Beat 14: item 1 ----------
        item1 = make_adv_item(checklist_texts[0], checklist_graphics[0], row_ys[0])
        checklist_items.append(item1)
        self.play(GrowFromCenter(item1[0]), Write(item1[1]), FadeIn(item1[2]), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.52))

        self.wait(max(0.05, 0.48))  # gap 59.24-59.72

        # ---------- Beat 15: item 2 ----------
        item2 = make_adv_item(checklist_texts[1], checklist_graphics[1], row_ys[1])
        checklist_items.append(item2)
        self.play(GrowFromCenter(item2[0]), Write(item2[1]), FadeIn(item2[2]), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.46))

        self.wait(max(0.05, 0.54))  # gap 60.88-61.42

        # ---------- Beat 16: item 3 ----------
        item3 = make_adv_item(checklist_texts[2], checklist_graphics[2], row_ys[2])
        checklist_items.append(item3)
        self.play(GrowFromCenter(item3[0]), Write(item3[1]), FadeIn(item3[2]), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.84))

        self.wait(max(0.05, 0.56))  # gap 63.26-63.82

        # ---------- Beat 17: item 4 ----------
        item4 = make_adv_item(checklist_texts[3], checklist_graphics[3], row_ys[3])
        checklist_items.append(item4)
        self.play(GrowFromCenter(item4[0]), Write(item4[1]), FadeIn(item4[2]), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.82))

        self.wait(max(0.05, 0.60))  # gap 65.64-66.24

        # ---------- Beat 18: item 5 ----------
        item5 = make_adv_item(checklist_texts[4], checklist_graphics[4], row_ys[4])
        checklist_items.append(item5)
        self.play(GrowFromCenter(item5[0]), Write(item5[1]), FadeIn(item5[2]), run_time=max(0.05, 1.40))
        self.wait(max(0.05, 0.74))

        self.wait(max(0.05, 1.00))  # gap 68.38-69.38

        # ---------- Beat 19: full checklist, sweep highlight, caption ----------
        self.play(application_group.animate.set_opacity(0.50), run_time=max(0.05, 0.50))
        self.play(application_group.animate.set_opacity(0.38), run_time=max(0.05, 0.50))

        sweep_rect = SurroundingRectangle(
            checklist_items[0],
            color=YELLOW,
            stroke_width=3,
            buff=0.10,
            corner_radius=0.08,
        )
        self.play(Create(sweep_rect), run_time=max(0.05, 0.40))
        for row in checklist_items[1:]:
            self.play(sweep_rect.animate.move_to(row.get_center()), run_time=max(0.05, 0.45))
        self.play(FadeOut(sweep_rect), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.35))

        advantage_caption = Text(
            "Most widely used tool for dynamic brain function",
            font_size=20,
            color=YELLOW,
        )
        advantage_caption.next_to(adv_panel, DOWN, buff=0.26)
        self.play(FadeIn(advantage_caption), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.00))
        self.play(FadeOut(advantage_caption), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.98))

        self.wait(max(0.05, 0.78))  # gap 76.16-76.94

        # ---------- Beat 20: single sample is insufficient ----------
        adv_group = VGroup(adv_panel, adv_title, *checklist_items)

        sample_box = RoundedRectangle(
            corner_radius=0.10,
            width=2.2,
            height=1.2,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=1,
        )
        sample_wave = make_wave_mobject(freq=4, amp=0.15, width=1.6, height=0.48, color=BLUE, stroke_width=1.6)
        sample_wave.move_to(sample_box.get_center())
        sample_label = Text("Single sample", font_size=18, color=GREY_B)
        sample_label.next_to(sample_box, DOWN, buff=0.18)
        single_sample_group = VGroup(sample_box, sample_wave, sample_label)
        single_sample_group.move_to(ORIGIN)

        red_x = SVGMobject(
            ASSET_PATHS["x_circle"],
            fill_color=RED,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
            height=0.65,
        )
        red_x.move_to(sample_box.get_top() + RIGHT * 1.05)

        self.play(
            adv_group.animate.set_opacity(0.18),
            application_group.animate.set_opacity(0.14).scale(0.90),
            run_time=max(0.05, 1.20),
        )
        self.play(FadeIn(single_sample_group), run_time=max(0.05, 0.90))
        self.play(GrowFromCenter(red_x), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.82))

        self.wait(max(0.05, 0.88))  # gap 80.26-81.14

        # ---------- Beat 21: analysis over time, moving window ----------
        sample_left_pos = np.array([-5.95, 1.80, 0.0])

        long_xs = np.linspace(-5.0, 5.0, 900)
        long_t = np.linspace(0, 1, 900)
        long_y = (
            0.22 * np.sin(2 * np.pi * 1.2 * long_t)
            + 0.18 * np.sin(2 * np.pi * 3.5 * long_t + 1.0)
            + 0.13 * np.sin(2 * np.pi * 8.0 * long_t + 2.0)
            + 0.07 * np.sin(2 * np.pi * 16.0 * long_t + 3.0)
        )
        long_y = long_y / (np.max(np.abs(long_y)) + 1e-6) * 0.58
        long_wave = VMobject()
        long_wave.set_points_as_corners([np.array([x, y, 0.0]) for x, y in zip(long_xs, long_y)])
        long_wave.set_stroke(WHITE, width=2)
        long_wave.set_fill(opacity=0)
        long_wave.move_to(np.array([0.4, 2.05, 0.0]))

        long_label = Text("Analysis over time", font_size=22, color=WHITE)
        long_label.next_to(long_wave, DOWN, buff=0.20)
        long_group = VGroup(long_wave, long_label)

        window_rect = Rectangle(
            width=1.30,
            height=1.05,
            fill_color=YELLOW,
            fill_opacity=0.18,
            stroke_color=YELLOW,
            stroke_width=2,
        )
        window_rect.move_to(np.array([long_wave.get_left()[0] + 0.70, long_wave.get_center()[1], 0.0]))

        self.play(
            single_sample_group.animate.scale(0.55).move_to(sample_left_pos),
            run_time=max(0.05, 1.00),
        )
        self.play(GrowFromCenter(long_group), run_time=max(0.05, 1.20))
        self.play(FadeIn(window_rect), run_time=max(0.05, 0.30))
        self.play(
            window_rect.animate.move_to(
                np.array([long_wave.get_right()[0] - 0.70, long_wave.get_center()[1], 0.0])
            ),
            run_time=max(0.05, 2.20),
            rate_func=linear,
        )
        self.wait(max(0.05, 0.62))

        # ---------- Beat 22: three signal-processing panels ----------
        sig_panel_centers = [-3.35, 0.40, 4.15]
        sig_panel_y = -0.30
        sig_panel_w = 2.80
        sig_panel_h = 2.20

        sig_panels = []
        sig_labels = []
        sig_arrows = []

        panel_spec_plot = RoundedRectangle(
            corner_radius=0.10,
            width=sig_panel_w,
            height=sig_panel_h,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.98,
        )
        panel_spec_plot.move_to(np.array([sig_panel_centers[0], sig_panel_y, 0.0]))
        # simple power spectrum
        sp = panel_spec_plot
        ax_left = sp.get_left()[0] + 0.30
        ax_right = sp.get_right()[0] - 0.26
        ax_bottom = sp.get_bottom()[1] + 0.28
        ax_top = sp.get_top()[1] - 0.42
        ax_x = Line(np.array([ax_left, ax_bottom, 0]), np.array([ax_right, ax_bottom, 0]), color=GREY_B, stroke_width=2)
        ax_y = Line(np.array([ax_left, ax_bottom, 0]), np.array([ax_left, ax_top, 0]), color=GREY_B, stroke_width=2)
        freqs = np.linspace(0, 30, 90)
        pow_vals = np.exp(-((freqs - 9.0) / 2.8) ** 2) + 0.18 * np.exp(-((freqs - 18.0) / 4.0) ** 2)
        pow_vals = pow_vals / np.max(pow_vals)
        curve_pts = [
            np.array([
                ax_left + (f / 30.0) * (ax_right - ax_left),
                ax_bottom + p * (ax_top - ax_bottom) * 0.78,
                0.0,
            ])
            for f, p in zip(freqs, pow_vals)
        ]
        pow_curve = VMobject()
        pow_curve.set_points_as_corners(curve_pts)
        pow_curve.set_stroke(GREEN, width=2)
        pow_curve.set_fill(opacity=0)
        spec_content_plot = VGroup(ax_x, ax_y, pow_curve)
        spec_content_plot.scale_to_fit_width(sig_panel_w - 0.44)
        spec_content_plot.scale_to_fit_height(sig_panel_h - 0.44)
        spec_content_plot.move_to(sp.get_center())

        panel_spectrogram = RoundedRectangle(
            corner_radius=0.10,
            width=sig_panel_w,
            height=sig_panel_h,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.98,
        )
        panel_spectrogram.move_to(np.array([sig_panel_centers[1], sig_panel_y, 0.0]))
        sg = panel_spectrogram
        left_sg = sg.get_left()[0] + 0.22
        right_sg = sg.get_right()[0] - 0.22
        bottom_sg = sg.get_bottom()[1] + 0.26
        top_sg = sg.get_top()[1] - 0.42
        cell_w = (right_sg - left_sg) / 10.0
        cell_h = (top_sg - bottom_sg) / 5.0
        warm_colors = [ORANGE, YELLOW, GREEN, TEAL, BLUE]
        heat_cells = VGroup()
        for r in range(5):
            for c in range(10):
                cell = Rectangle(
                    width=cell_w * 0.92,
                    height=cell_h * 0.92,
                    fill_color=warm_colors[r],
                    fill_opacity=0.45 + 0.08 * c,
                    stroke_color=GREY_B,
                    stroke_width=0.6,
                )
                cell.move_to(np.array([left_sg + (c + 0.5) * cell_w, bottom_sg + (r + 0.5) * cell_h, 0.0]))
                heat_cells.add(cell)
        spec_content_sg = VGroup(heat_cells)
        spec_content_sg.scale_to_fit_width(sig_panel_w - 0.40)
        spec_content_sg.scale_to_fit_height(sig_panel_h - 0.40)
        spec_content_sg.move_to(sg.get_center())

        panel_timefreq = RoundedRectangle(
            corner_radius=0.10,
            width=sig_panel_w,
            height=sig_panel_h,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.98,
        )
        panel_timefreq.move_to(np.array([sig_panel_centers[2], sig_panel_y, 0.0]))
        tf = panel_timefreq
        left_tf = tf.get_left()[0] + 0.24
        right_tf = tf.get_right()[0] - 0.24
        bottom_tf = tf.get_bottom()[1] + 0.26
        top_tf = tf.get_top()[1] - 0.42
        tf_cell_w = (right_tf - left_tf) / 16.0
        tf_cell_h = (top_tf - bottom_tf) / 7.0
        tf_colors = [PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, TEAL]
        tf_cells = VGroup()
        for r in range(7):
            for c in range(16):
                cell = Rectangle(
                    width=tf_cell_w * 0.90,
                    height=tf_cell_h * 0.90,
                    fill_color=tf_colors[r],
                    fill_opacity=0.45 + 0.40 * np.exp(-((c - 8) ** 2) / 12.0),
                    stroke_color=GREY_B,
                    stroke_width=0.5,
                )
                cell.move_to(np.array([left_tf + (c + 0.5) * tf_cell_w, bottom_tf + (r + 0.5) * tf_cell_h, 0.0]))
                tf_cells.add(cell)
        spec_content_tf = VGroup(tf_cells)
        spec_content_tf.scale_to_fit_width(sig_panel_w - 0.40)
        spec_content_tf.scale_to_fit_height(sig_panel_h - 0.40)
        spec_content_tf.move_to(tf.get_center())

        sig_panel_groups = [
            VGroup(panel_spec_plot, spec_content_plot),
            VGroup(panel_spectrogram, spec_content_sg),
            VGroup(panel_timefreq, spec_content_tf),
        ]
        sig_label_texts = ["Spectral analysis", "Spectrogram", "Time-frequency analysis"]

        for i, (panel_group, lab_text) in enumerate(zip(sig_panel_groups, sig_label_texts)):
            panel_group.move_to(np.array([sig_panel_centers[i], sig_panel_y, 0.0]))
            lab = Text(lab_text, font_size=14, color=WHITE)
            lab.next_to(panel_group, DOWN, buff=0.16)
            arrow = Arrow(
                start=np.array([panel_group.get_center()[0], long_wave.get_bottom()[1] - 0.10, 0.0]),
                end=panel_group.get_top() + UP * 0.08,
                color=YELLOW,
                stroke_width=2,
                buff=0.05,
                max_tip_length_to_length_ratio=0.22,
            )
            sig_panels.append(panel_group)
            sig_labels.append(lab)
            sig_arrows.append(arrow)

        self.play(FadeIn(sig_panels[0]), FadeIn(sig_labels[0]), Create(sig_arrows[0]), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.20))
        self.play(FadeIn(sig_panels[1]), FadeIn(sig_labels[1]), Create(sig_arrows[1]), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.20))
        self.play(FadeIn(sig_panels[2]), FadeIn(sig_labels[2]), Create(sig_arrows[2]), run_time=max(0.05, 1.00))
        self.wait(max(0.05, 0.20))
        self.wait(max(0.05, 2.92))

        # ---------- Beat 23: final hold ----------
        self.wait(max(0.05, 0.85))