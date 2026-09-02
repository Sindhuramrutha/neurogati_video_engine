ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- Beat 1: Frequency axis (0.00 – 6.38) ----------
        axis = Arrow(
            start=LEFT * 6.5,
            end=RIGHT * 6.5,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.05,
            buff=0,
        )
        freq_label = Text("Frequency", font_size=36, color=WHITE)
        freq_label.next_to(axis.get_end(), RIGHT, buff=0.2)

        t1 = 0.0
        self.play(Create(axis), Write(freq_label), run_time=max(0.05, 3.0))
        # keep alive with small pulse
        self.play(freq_label.animate.scale(1.15), run_time=max(0.05, 0.5))
        self.play(freq_label.animate.scale(1 / 1.15), run_time=max(0.05, 0.5))
        remain = 6.38 - (3.0 + 0.5 + 0.5)
        self.wait(max(0.05, remain))

        # ---------- Beat 2: Low‑pass curve (6.38 – 11.04) ----------
        f_L = 1.5   # cutoff for low‑pass (upper band‑pass edge)
        sigma = 0.4

        lowpass_fn = lambda x: 3 / (1 + np.exp((x - f_L) / sigma))
        low_pass_graph = FunctionGraph(
            lowpass_fn, x_range=[-6.5, 6.5], color=BLUE, stroke_width=4
        )

        # Arrow and label for f_L
        low_arrow_y = lowpass_fn(f_L)  # = 1.5
        arrow_fL = Arrow(
            start=np.array([f_L, 0, 0]),
            end=np.array([f_L, low_arrow_y, 0]),
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        label_fL = Text("f_L", font_size=30, color=GOLD)
        label_fL.next_to(arrow_fL.get_end(), UP, buff=0.1)
        fL_group = VGroup(arrow_fL, label_fL)

        t2 = 6.38
        anim_time = 3.0
        self.play(Create(low_pass_graph), Create(fL_group), run_time=max(0.05, anim_time))
        used = anim_time
        # soft brightening
        self.play(low_pass_graph.animate.set_stroke(width=6), run_time=max(0.05, 0.5))
        self.play(low_pass_graph.animate.set_stroke(width=4), run_time=max(0.05, 0.5))
        used += 1.0
        wait_time = (11.04 - t2) - used
        self.wait(max(0.05, wait_time))

        # ---------- Beat 3: High‑pass curve (11.04 – 14.36) ----------
        f_H = -1.5   # cutoff for high‑pass (lower band‑pass edge)
        highpass_fn = lambda x: 3 / (1 + np.exp(-(x - f_H) / sigma))
        high_pass_graph = FunctionGraph(
            highpass_fn, x_range=[-6.5, 6.5], color=RED, stroke_width=4
        )

        high_arrow_y = highpass_fn(f_H)  # = 1.5
        arrow_fH = Arrow(
            start=np.array([f_H, 0, 0]),
            end=np.array([f_H, high_arrow_y, 0]),
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        label_fH = Text("f_H", font_size=30, color=GOLD)
        label_fH.next_to(arrow_fH.get_end(), UP, buff=0.1)
        fH_group = VGroup(arrow_fH, label_fH)

        t3 = 11.04
        anim_time = 2.2
        self.play(Create(high_pass_graph), Create(fH_group), run_time=max(0.05, anim_time))
        used = anim_time
        self.play(high_pass_graph.animate.set_stroke(width=6), run_time=max(0.05, 0.4))
        self.play(high_pass_graph.animate.set_stroke(width=4), run_time=max(0.05, 0.4))
        used += 0.8
        wait_time = (14.36 - t3) - used
        self.wait(max(0.05, wait_time))

        # ---------- Beat 4: Band‑pass curve emerges (14.36 – 24.98) ----------
        # Fade low‑ and high‑pass to semi‑transparent
        self.play(
            low_pass_graph.animate.set_opacity(0.3),
            high_pass_graph.animate.set_opacity(0.3),
            run_time=max(0.05, 1.2),
        )
        t4 = 14.36
        used = 1.2

        # Band‑pass function = product of the two
        bandpass_fn = lambda x: lowpass_fn(x) * highpass_fn(x) / 3.0  # normalise back to [0,3]
        band_pass_graph = FunctionGraph(
            bandpass_fn, x_range=[-6.5, 6.5], color=GREEN, stroke_width=5
        )

        self.play(Create(band_pass_graph), run_time=max(0.05, 3.0))
        used += 3.0
        # gentle emphasis pulses on band‑pass
        self.play(band_pass_graph.animate.set_stroke(width=7), run_time=max(0.05, 0.8))
        self.play(band_pass_graph.animate.set_stroke(width=5), run_time=max(0.05, 0.8))
        used += 1.6
        self.play(band_pass_graph.animate.set_stroke(width=8), run_time=max(0.05, 0.6))
        self.play(band_pass_graph.animate.set_stroke(width=5), run_time=max(0.05, 0.6))
        used += 1.2
        wait_time = (24.98 - t4) - used
        self.wait(max(0.05, wait_time))

        # ---------- Beat 5: Highlight “High‑pass component” (24.98 – 30.44) ----------
        high_label = Text(
            "High‑pass component", font_size=28, color=RED, weight="BOLD"
        )
        # attach near the curve at x = 2.0 (where curve is high)
        anchor_x = 2.0
        anchor_y = highpass_fn(anchor_x)  # ≈ 3.0
        high_label.move_to(np.array([anchor_x, anchor_y + 1.0, 0]))
        high_arrow = Arrow(
            start=high_label.get_bottom(),
            end=np.array([anchor_x, anchor_y, 0]),
            color=RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        t5 = 24.98
        self.play(FadeIn(high_label), Create(high_arrow), run_time=max(0.05, 2.0))
        used = 2.0
        self.play(high_pass_graph.animate.set_opacity(1).set_stroke(width=7), run_time=max(0.05, 1.0))
        self.play(high_pass_graph.animate.set_opacity(0.3).set_stroke(width=4), run_time=max(0.05, 1.0))
        used += 2.0
        wait_time = (30.44 - t5) - used
        self.wait(max(0.05, wait_time))

        # ---------- Beat 6: Highlight “Low‑pass component” (30.44 – 34.84) ----------
        low_label = Text(
            "Low‑pass component", font_size=28, color=BLUE, weight="BOLD"
        )
        anchor_x = -3.0
        anchor_y = lowpass_fn(anchor_x)  # ≈ 3.0
        low_label.move_to(np.array([anchor_x, anchor_y + 1.0, 0]))
        low_arrow = Arrow(
            start=low_label.get_bottom(),
            end=np.array([anchor_x, anchor_y, 0]),
            color=BLUE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        t6 = 30.44
        self.play(FadeIn(low_label), Create(low_arrow), run_time=max(0.05, 1.8))
        used = 1.8
        self.play(low_pass_graph.animate.set_opacity(1).set_stroke(width=7), run_time=max(0.05, 1.0))
        self.play(low_pass_graph.animate.set_opacity(0.3).set_stroke(width=4), run_time=max(0.05, 1.0))
        used += 2.0
        wait_time = (34.84 - t6) - used
        self.wait(max(0.05, wait_time))

        # ---------- Beat 7: Highlight “Band‑pass output” (34.84 – 39.60) ----------
        band_label = Text(
            "Band‑pass output", font_size=28, color=GREEN, weight="BOLD"
        )
        anchor_x = 0.0
        anchor_y = bandpass_fn(anchor_x)  # ≈ 3.0
        band_label.move_to(np.array([anchor_x, anchor_y + 1.0, 0]))
        band_arrow = Arrow(
            start=band_label.get_bottom(),
            end=np.array([anchor_x, anchor_y, 0]),
            color=GREEN,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        t7 = 34.84
        self.play(FadeIn(band_label), Create(band_arrow), run_time=max(0.05, 1.8))
        used = 1.8
        self.play(band_pass_graph.animate.set_stroke(width=10), run_time=max(0.05, 1.0))
        self.play(band_pass_graph.animate.set_stroke(width=6), run_time=max(0.05, 1.0))
        used += 2.0
        wait_time = (39.60 - t7) - used
        self.wait(max(0.05, wait_time))

        # ---------- Beat 8: Definition box slides in (39.60 – 48.88) ----------
        box = Rectangle(
            width=12, height=1.6,
            fill_color="#2B2B2B", fill_opacity=1,
            stroke_color=WHITE, stroke_width=1,
        )
        def_text = Text(
            "Band‑Pass Filter: preserves frequencies within a\n"
            "specified range, attenuates frequencies outside that range.",
            font_size=26, color=WHITE, line_spacing=0.6,
        )
        def_box = VGroup(box, def_text)
        def_text.move_to(box.get_center())

        # start off‑screen at bottom
        def_box.move_to(DOWN * 5)
        t8 = 39.60
        self.play(def_box.animate.to_edge(DOWN, buff=0.4), run_time=max(0.05, 1.2))
        wait_to_end = 48.88 - (t8 + 1.2)
        self.wait(max(0.05, wait_to_end))