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


class Scene19(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helper: draw an EEG-like trace ----------
        def make_trace(signal, width=2.0, height=0.8, color=YELLOW, stroke_width=3.0, num_points=600):
            mob = VMobject()
            mob.set_stroke(color=color, width=stroke_width, opacity=1)
            u = np.linspace(-1, 1, num_points)
            x = u * width / 2.0
            y = signal(u) * height / 2.0
            y = np.clip(y, -height / 2.0, height / 2.0)
            mob.set_points_as_corners(np.array([x, y, np.zeros_like(x)]).T)
            return mob

        # signals from previous scene / for panels
        def spike_wave_signal(u):
            y = 0.12 * np.sin(2 * np.pi * 1.5 * u)
            y += 1.4 * np.exp(-((u + 0.4) / 0.06) ** 2)
            y += 1.5 * np.exp(-((u - 0.4) / 0.06) ** 2)
            y += 0.35 * np.sin(2 * np.pi * 3.0 * (u - 0.5)) * np.exp(-((u - 0.5) / 0.25) ** 2)
            y += 0.35 * np.sin(2 * np.pi * 3.0 * (u + 0.5)) * np.exp(-((u + 0.5) / 0.25) ** 2)
            return y

        def epileptic_spike_signal(u):
            y = np.zeros_like(u)
            y += -1.8 * np.exp(-((u + 0.10) / 0.04) ** 2)
            y += 2.4 * np.exp(-((u - 0.12) / 0.035) ** 2)
            return y

        def sharp_wave_signal(u):
            y = np.zeros_like(u)
            y += 2.0 * np.exp(-(u / 0.07) ** 2)
            return y

        def spike_and_wave_complex_signal(u):
            y = 0.15 * np.sin(2 * np.pi * 1.8 * u)
            y += 2.6 * np.exp(-((u + 0.25) / 0.03) ** 2)
            y += -1.3 * np.exp(-((u - 0.05) / 0.12) ** 2)
            return y

        def rhythmic_seizure_signal(u):
            y = 0.30 * np.sin(2 * np.pi * 4 * u)
            centers = np.arange(-0.85, 0.86, 0.28)
            for c in centers:
                y += 1.1 * np.exp(-((u - c) / 0.025) ** 2)
            y += 0.25 * np.sin(2 * np.pi * 17 * u) * np.exp(-(u ** 2) / 0.8)
            return y

        # ---------- previous scene's final composition ----------
        # left: EEG trace with annotations, shifted/shrunk from previous scene
        old_eeg = make_trace(spike_wave_signal, width=9.0, height=1.5, color=YELLOW, stroke_width=4)
        peak_left = Circle(radius=0.14, fill_color=RED, fill_opacity=0.9, stroke_width=0)
        peak_left.move_to(old_eeg.get_center() + LEFT * 2.4 + UP * 0.6)
        peak_right = Circle(radius=0.14, fill_color=RED, fill_opacity=0.9, stroke_width=0)
        peak_right.move_to(old_eeg.get_center() + RIGHT * 2.4 + UP * 0.6)

        marker_spike = Text("Sharp spike", font_size=18, color=YELLOW)
        marker_spike.next_to(old_eeg.get_center() + LEFT * 2.4 + UP * 1.1, UP, buff=0.1)
        marker_slow = Text("Slow wave", font_size=18, color=YELLOW)
        marker_slow.next_to(old_eeg.get_center() + LEFT * 0.5 + DOWN * 1.0, DOWN, buff=0.1)
        marker_after = Text("After-discharge", font_size=18, color=ORANGE)
        marker_after.next_to(old_eeg.get_center() + RIGHT * 1.8 + DOWN * 1.15, DOWN, buff=0.1)

        annotation_sweep = Line(old_eeg.get_bottom(), old_eeg.get_top(), color=WHITE, stroke_width=2)
        annotation_sweep.move_to(old_eeg.get_left())

        old_eeg_group = VGroup(old_eeg, peak_left, peak_right, marker_spike, marker_slow, marker_after, annotation_sweep)
        old_eeg_group.scale(0.75).move_to(LEFT * 3.5 + UP * 0.1)

        # right: structural brain image + caption
        structural_brain = SVGMobject(ASSET_PATHS["brain"])
        structural_brain.set_color(GREY_B).set_fill(opacity=0)
        structural_brain.scale_to_fit_height(3.0)
        structural_brain.move_to(RIGHT * 4.2 + UP * 0.2)

        structural_label = Text("Structural imaging", font_size=20, color=GREY_B)
        structural_label.next_to(structural_brain, DOWN, buff=0.25)

        structural_caption = Text(
            "Structural imaging alone cannot provide this information.",
            font_size=20,
            color=GREY_B,
        )
        structural_caption.to_edge(DOWN, buff=0.4)

        self.add(old_eeg_group, structural_brain, structural_label, structural_caption)

        # ---------- beat 1: 0.00 - 1.64 ----------
        heading = Text("Abnormal EEG Findings in Epilepsy", font_size=33, color=WHITE, weight="BOLD")
        heading.scale_to_fit_width(11)
        heading.to_edge(UP, buff=0.4)

        self.play(
            FadeOut(structural_brain),
            FadeOut(structural_label),
            FadeOut(structural_caption),
            old_eeg_group.animate.scale(0.45).move_to(UP * 2.0).set_opacity(0.14),
            Write(heading),
            run_time=max(0.05, 1.64),
        )

        # ---------- panel outlines ----------
        panel_rects = []
        panel_label_slots = []
        panel_groups = []

        for _ in range(4):
            rect = Rectangle(
                width=2.7,
                height=1.5,
                fill_color=BLACK,
                fill_opacity=0.55,
                stroke_color=GREY_B,
                stroke_width=1.5,
            )
            slot = Text(" ", font_size=14, color=WHITE)
            slot.next_to(rect, DOWN, buff=0.12)
            panel = VGroup(rect, slot)
            panel_rects.append(rect)
            panel_label_slots.append(slot)
            panel_groups.append(panel)

        panel_row = VGroup(*panel_groups).arrange(RIGHT, buff=0.55).move_to(UP * 0.3)

        # waveform colors, in panel order
        panel_colors = [YELLOW, ORANGE, PURPLE, RED]

        # ---------- beat 2: 1.64 - 4.06 ----------
        self.play(
            old_eeg_group.animate.set_opacity(0.07),
            FadeIn(panel_row),
            run_time=max(0.05, 1.42),
        )
        self.wait(max(0.05, 1.00))

        # preview traces for each panel, drawn later
        wave1 = make_trace(epileptic_spike_signal, width=2.25, height=0.9, color=panel_colors[0], stroke_width=3.0)
        wave1.move_to(panel_rects[0].get_center())
        label1 = Text("Epileptic Spike", font_size=14, color=WHITE)
        label1.scale_to_fit_width(2.4)
        label1.move_to(panel_label_slots[0].get_center())

        # ---------- beat 3: 4.06 - 6.00 ----------
        self.play(Create(wave1), run_time=max(0.05, 1.24))
        self.play(FadeIn(label1), run_time=max(0.05, 0.70))

        # ---------- beat 4: 6.00 - 6.80 ----------
        self.wait(max(0.05, 0.80))

        # gap 6.80 - 8.12
        self.wait(max(0.05, 1.32))

        wave2 = make_trace(sharp_wave_signal, width=2.25, height=0.9, color=panel_colors[1], stroke_width=3.0)
        wave2.move_to(panel_rects[1].get_center())
        label2 = Text("Sharp Wave", font_size=14, color=WHITE)
        label2.scale_to_fit_width(2.4)
        label2.move_to(panel_label_slots[1].get_center())

        # ---------- beat 5: 8.12 - 9.76 ----------
        self.play(Create(wave2), run_time=max(0.05, 0.94))
        self.play(FadeIn(label2), run_time=max(0.05, 0.70))

        # ---------- beat 6: 9.76 - 11.68 ----------
        self.play(
            wave1.animate.set_stroke(color=WHITE, width=4.5, opacity=1),
            label1.animate.set_color(YELLOW),
            run_time=max(0.05, 0.70),
        )
        self.play(
            wave1.animate.set_stroke(color=panel_colors[0], width=3.0, opacity=1),
            label1.animate.set_color(WHITE),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.52))

        # ---------- beat 7: 11.68 - 12.86 ----------
        self.play(
            wave2.animate.set_stroke(color=WHITE, width=4.5, opacity=1),
            label2.animate.set_color(YELLOW),
            run_time=max(0.05, 0.44),
        )
        self.play(
            wave2.animate.set_stroke(color=panel_colors[1], width=3.0, opacity=1),
            label2.animate.set_color(WHITE),
            run_time=max(0.05, 0.44),
        )
        self.wait(max(0.05, 0.30))

        # gap 12.86 - 13.46
        self.wait(max(0.05, 0.60))

        wave3 = make_trace(spike_and_wave_complex_signal, width=2.25, height=0.9, color=panel_colors[2], stroke_width=3.0)
        wave3.move_to(panel_rects[2].get_center())
        label3 = Text("Spike-and-Wave Complex", font_size=14, color=WHITE)
        label3.scale_to_fit_width(2.4)
        label3.move_to(panel_label_slots[2].get_center())

        # ---------- beat 8: 13.46 - 14.58 ----------
        self.play(Create(wave3), run_time=max(0.05, 0.62))
        self.play(FadeIn(label3), run_time=max(0.05, 0.50))

        # gap 14.58 - 15.30
        self.wait(max(0.05, 0.72))

        wave4 = make_trace(rhythmic_seizure_signal, width=2.25, height=0.9, color=panel_colors[3], stroke_width=3.0)
        wave4.move_to(panel_rects[3].get_center())
        label4 = Text("Rhythmic Seizure Activity", font_size=14, color=WHITE)
        label4.scale_to_fit_width(2.4)
        label4.move_to(panel_label_slots[3].get_center())

        # ---------- beat 9: 15.30 - 16.50 ----------
        self.play(Create(wave4), run_time=max(0.05, 0.65))
        self.play(FadeIn(label4), run_time=max(0.05, 0.55))

        # ---------- beat 10: 16.50 - 17.54 ----------
        self.wait(max(0.05, 1.04))

        waveform_list = [wave1, wave2, wave3, wave4]
        label_list = [label1, label2, label3, label4]

        # ---------- beat 11: 17.54 - 19.28 ----------
        caption = Text("Important evidence.", font_size=20, color=YELLOW)
        caption.next_to(panel_row, DOWN, buff=1.2)

        self.play(
            *[r.animate.set_stroke(color=YELLOW, width=3, opacity=0.85) for r in panel_rects],
            *[w.animate.set_stroke(width=4, opacity=1) for w in waveform_list],
            run_time=max(0.05, 0.84),
        )
        self.play(FadeIn(caption), run_time=max(0.05, 0.90))

        current_caption = caption

        # ---------- beat 12: 19.28 - 20.44 ----------
        caption2 = Text("Helps clinicians evaluate.", font_size=20, color=YELLOW)
        caption2.move_to(current_caption.get_center())

        self.play(FadeOut(current_caption), FadeIn(caption2), run_time=max(0.05, 0.36))
        current_caption = caption2

        for i in range(4):
            self.play(
                panel_rects[i].animate.set_stroke(color=WHITE, width=4, opacity=1),
                waveform_list[i].animate.set_stroke(color=WHITE, width=5, opacity=1),
                label_list[i].animate.set_color(YELLOW),
                run_time=max(0.05, 0.10),
            )
            self.play(
                panel_rects[i].animate.set_stroke(color=YELLOW, width=3, opacity=0.85),
                waveform_list[i].animate.set_stroke(color=panel_colors[i], width=4, opacity=1),
                label_list[i].animate.set_color(WHITE),
                run_time=max(0.05, 0.10),
            )

        # ---------- beat 13: 20.44 - 22.80 ----------
        caption3 = Text("Evaluate and classify epileptic disorders.", font_size=20, color=YELLOW)
        caption3.move_to(current_caption.get_center())

        self.play(FadeOut(current_caption), FadeIn(caption3), run_time=max(0.05, 0.40))
        current_caption = caption3

        # classification line below the row, with a branch pointing up to each panel
        class_line_y = caption3.get_top()[1] + 0.35
        x_left = panel_rects[0].get_left()[0] - 0.30
        x_right = panel_rects[-1].get_right()[0] + 0.30
        class_line = Line(
            np.array([x_left, class_line_y, 0.0]),
            np.array([x_right, class_line_y, 0.0]),
            color=YELLOW,
            stroke_width=2,
        )

        branch_arrows = VGroup()
        for i, rect in enumerate(panel_rects):
            x = rect.get_center()[0]
            end_y = panel_groups[i].get_bottom()[1] + 0.08
            arrow = Arrow(
                start=np.array([x, class_line_y, 0.0]),
                end=np.array([x, end_y, 0.0]),
                color=YELLOW,
                stroke_width=2,
                buff=0.06,
                max_tip_length_to_length_ratio=0.25,
            )
            branch_arrows.add(arrow)

        classification_group = VGroup(class_line, branch_arrows)

        self.play(Create(classification_group), run_time=max(0.05, 0.80))

        # panels continue to be highlighted one after another
        for i in range(4):
            self.play(
                panel_rects[i].animate.set_stroke(color=WHITE, width=4, opacity=1),
                waveform_list[i].animate.set_stroke(color=WHITE, width=5, opacity=1),
                label_list[i].animate.set_color(YELLOW),
                run_time=max(0.05, 0.12),
            )
            self.play(
                panel_rects[i].animate.set_stroke(color=YELLOW, width=3, opacity=0.85),
                waveform_list[i].animate.set_stroke(color=panel_colors[i], width=4, opacity=1),
                label_list[i].animate.set_color(WHITE),
                run_time=max(0.05, 0.12),
            )
        self.wait(max(0.05, 0.20))

        # ---------- beat 14: 22.80 - 24.02 ----------
        self.wait(max(0.05, 1.22))