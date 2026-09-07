ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- layout constants ----------
        axis_left = -6.5
        axis_right = 6.5
        freq_max = 50.0           # right edge of axis corresponds to 50 Hz
        x_scale = (axis_right - axis_left) / freq_max   # 13/50 = 0.26

        x_L = axis_left + 1 * x_scale   # 1 Hz
        x_H = axis_left + 40 * x_scale  # 40 Hz

        # ---------- frequency axis (kept from previous scene) ----------
        axis = Arrow(
            start=LEFT * axis_right,
            end=RIGHT * axis_right,
            color=WHITE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.05,
            buff=0,
        )
        freq_label = Text("Frequency", font_size=36, color=WHITE)
        freq_label.next_to(axis.get_end(), RIGHT, buff=0.2)
        axis.set_z_index(3)
        freq_label.set_z_index(3)

        # ---------- re-create all elements from the end of Scene 2 ----------
        sigma_old = 0.4

        # old green band‑pass curve (cutoffs at -1.5 and 1.5)
        lowpass_old = lambda x: 3 / (1 + np.exp((x - 1.5) / sigma_old))
        highpass_old = lambda x: 3 / (1 + np.exp(-(x + 1.5) / sigma_old))
        bandpass_old_fn = lambda x: lowpass_old(x) * highpass_old(x) / 3.0
        old_band_pass = FunctionGraph(
            bandpass_old_fn,
            x_range=[axis_left, axis_right],
            color=GREEN,
            stroke_width=5,
        )
        old_band_pass.set_z_index(2)

        # old high‑pass and low‑pass curves (semi‑transparent)
        old_high_pass = FunctionGraph(
            lambda x: 3 / (1 + np.exp(-(x + 1.5) / sigma_old)),
            x_range=[axis_left, axis_right],
            color=RED,
            stroke_width=4,
        ).set_opacity(0.3)

        old_low_pass = FunctionGraph(
            lambda x: 3 / (1 + np.exp((x - 1.5) / sigma_old)),
            x_range=[axis_left, axis_right],
            color=BLUE,
            stroke_width=4,
        ).set_opacity(0.3)

        # old cut‑off arrows (f_L = 1.5, f_H = -1.5)
        f_L_old = 1.5
        f_H_old = -1.5
        arrow_old_fL = Arrow(
            start=np.array([f_L_old, 0, 0]),
            end=np.array([f_L_old, 1.5, 0]),
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        label_old_fL = Text("f_L", font_size=30, color=GOLD).next_to(
            arrow_old_fL.get_end(), UP, buff=0.1
        )
        arrow_old_fH = Arrow(
            start=np.array([f_H_old, 0, 0]),
            end=np.array([f_H_old, 1.5, 0]),
            color=GOLD,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        label_old_fH = Text("f_H", font_size=30, color=GOLD).next_to(
            arrow_old_fH.get_end(), UP, buff=0.1
        )

        # component labels
        high_label = Text(
            "High‑pass component", font_size=28, color=RED, weight="BOLD"
        ).move_to(np.array([2.0, highpass_old(2.0) + 1.0, 0]))
        high_arrow_comp = Arrow(
            start=high_label.get_bottom(),
            end=np.array([2.0, highpass_old(2.0), 0]),
            color=RED,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        low_label = Text(
            "Low‑pass component", font_size=28, color=BLUE, weight="BOLD"
        ).move_to(np.array([-3.0, lowpass_old(-3.0) + 1.0, 0]))
        low_arrow_comp = Arrow(
            start=low_label.get_bottom(),
            end=np.array([-3.0, lowpass_old(-3.0), 0]),
            color=BLUE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )
        band_label = Text(
            "Band‑pass output", font_size=28, color=GREEN, weight="BOLD"
        ).move_to(np.array([0.0, bandpass_old_fn(0.0) + 1.0, 0]))
        band_arrow_comp = Arrow(
            start=band_label.get_bottom(),
            end=np.array([0.0, bandpass_old_fn(0.0), 0]),
            color=GREEN,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
            buff=0,
        )

        # definition box
        box = Rectangle(
            width=12,
            height=1.6,
            fill_color="#2B2B2B",
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
        )
        def_text = Text(
            (
                "Band‑Pass Filter: preserves frequencies within a\n"
                "specified range, attenuates frequencies outside that range."
            ),
            font_size=26,
            color=WHITE,
            line_spacing=0.6,
        )
        def_box = VGroup(box, def_text)
        def_text.move_to(box.get_center())
        def_box.to_edge(DOWN, buff=0.4)

        # ---------- new green band‑pass curve (vertical drops at 1 Hz & 40 Hz) ----------
        sigma_new = 0.05
        def new_bandpass(x):
            freq = (x - axis_left) / x_scale
            return (
                3
                * (1 / (1 + np.exp(-(freq - 1) / sigma_new)))
                * (1 / (1 + np.exp((freq - 40) / sigma_new)))
            )
        new_band_pass = FunctionGraph(
            new_bandpass,
            x_range=[axis_left, axis_right],
            color=GREEN,
            stroke_width=5,
        ).set_z_index(2)

        # ---------- bring everything on screen ----------
        self.add(
            axis,
            freq_label,
            old_band_pass,
            old_high_pass,
            old_low_pass,
            arrow_old_fL,
            label_old_fL,
            arrow_old_fH,
            label_old_fH,
            high_label,
            high_arrow_comp,
            low_label,
            low_arrow_comp,
            band_label,
            band_arrow_comp,
            def_box,
        )

        # ========== BEAT 1: fade out old components, morph green curve (0.00‑0.50) ==========
        to_fade = [
            old_high_pass,
            old_low_pass,
            arrow_old_fL,
            label_old_fL,
            arrow_old_fH,
            label_old_fH,
            high_label,
            high_arrow_comp,
            low_label,
            low_arrow_comp,
            band_label,
            band_arrow_comp,
            def_box,
        ]
        self.play(
            FadeOut(*to_fade),
            Transform(old_band_pass, new_band_pass),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 2.16))   # gap to 2.66

        # ========== BEAT 2: two vertical dashed lines + labels (2.66‑4.46) ==========
        dashed_L = DashedLine(
            start=np.array([x_L, 0, 0]),
            end=np.array([x_L, 3.5, 0]),
            color=WHITE,
            dash_length=0.2,
            stroke_width=2,
        ).set_z_index(1)
        dashed_H = DashedLine(
            start=np.array([x_H, 0, 0]),
            end=np.array([x_H, 3.5, 0]),
            color=WHITE,
            dash_length=0.2,
            stroke_width=2,
        ).set_z_index(1)

        label_L = Text("f_L", font_size=30, color=WHITE).next_to(
            dashed_L.get_end(), UP, buff=0.1
        )
        label_H = Text("f_H", font_size=30, color=WHITE).next_to(
            dashed_H.get_end(), UP, buff=0.1
        )

        self.play(
            Create(dashed_L),
            Create(dashed_H),
            Write(label_L),
            Write(label_H),
            run_time=max(0.05, 1.8),
        )

        # ========== BEAT 3: brighten f_L, left red band (4.46‑9.62) ==========
        self.play(
            dashed_L.animate.set_stroke(color=GOLD, width=4),
            label_L.animate.set_color(GOLD),
            run_time=max(0.05, 1.0),
        )

        left_red_band = Rectangle(
            width=x_L - axis_left,
            height=3.5,
            fill_color=RED,
            fill_opacity=0.3,
            stroke_width=0,
        ).move_to(np.array([axis_left, 1.75, 0]), aligned_edge=LEFT)
        left_red_band.set_z_index(0)

        self.play(FadeIn(left_red_band), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 3.16))   # remainder of 5.16 s

        # ========== BEAT 4: flash left red band (9.62‑12.90) ==========
        self.play(left_red_band.animate.set_opacity(0.6), run_time=max(0.05, 0.3))
        self.play(left_red_band.animate.set_opacity(0.3), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 3.28 - 0.6))

        # ========== BEAT 5: brighten f_H, right red & green bands (12.90‑18.68) ==========
        self.play(
            dashed_H.animate.set_stroke(color=GOLD, width=4),
            label_H.animate.set_color(GOLD),
            run_time=max(0.05, 1.0),
        )

        right_red_band = Rectangle(
            width=axis_right - x_H,
            height=3.5,
            fill_color=RED,
            fill_opacity=0.3,
            stroke_width=0,
        ).move_to(np.array([axis_right, 1.75, 0]), aligned_edge=RIGHT)
        right_red_band.set_z_index(0)

        green_band = Rectangle(
            width=x_H - x_L,
            height=3.5,
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_width=0,
        ).move_to(np.array([(x_L + x_H) / 2, 1.75, 0]))
        green_band.set_z_index(0)

        self.play(
            FadeIn(right_red_band),
            FadeIn(green_band),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 3.28))   # remainder of 5.78 s

        # ========== BEAT 6: flash right red band (18.68‑21.98) ==========
        self.play(right_red_band.animate.set_opacity(0.6), run_time=max(0.05, 0.3))
        self.play(right_red_band.animate.set_opacity(0.3), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 3.3 - 0.6))

        # ========== BEAT 7: change labels to "f_L = 1 Hz" / "f_H = 40 Hz" (21.98‑27.04) ==========
        new_label_L = Text("f_L = 1 Hz", font_size=30, color=GOLD).move_to(
            label_L.get_center()
        )
        new_label_H = Text("f_H = 40 Hz", font_size=30, color=GOLD).move_to(
            label_H.get_center()
        )
        self.play(
            Transform(label_L, new_label_L),
            Transform(label_H, new_label_H),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, 3.06))   # remainder of 5.06 s

        # ========== BEAT 8: emphasize left red band, "Attenuated" (27.04‑30.92) ==========
        self.play(left_red_band.animate.set_opacity(0.6), run_time=max(0.05, 0.5))

        left_band_width = x_L - axis_left
        left_attenuated = (
            Text("Attenuated", font_size=24, color=WHITE)
            .scale_to_fit_width(left_band_width * 0.8)
            .move_to(np.array([(axis_left + x_L) / 2, 1.75, 0]))
        )
        left_attenuated.set_z_index(1)
        self.play(FadeIn(left_attenuated), run_time=max(0.05, 0.5))
        self.play(left_red_band.animate.set_opacity(0.3), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 3.88 - 1.3))   # 0.5+0.5+0.3 = 1.3 used

        # ========== BEAT 9: emphasize green band, "Preserved" (30.92‑33.88) ==========
        self.play(green_band.animate.set_opacity(0.6), run_time=max(0.05, 0.5))
        preserved = Text("Preserved", font_size=28, color=WHITE).move_to(
            np.array([(x_L + x_H) / 2, 1.75, 0])
        )
        preserved.set_z_index(1)
        self.play(FadeIn(preserved), run_time=max(0.05, 0.5))
        self.play(green_band.animate.set_opacity(0.3), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 2.96 - 1.3))

        # ========== BEAT 10: emphasize right red band, "Attenuated" (33.88‑37.14) ==========
        self.play(right_red_band.animate.set_opacity(0.6), run_time=max(0.05, 0.5))
        right_attenuated = Text("Attenuated", font_size=28, color=WHITE).move_to(
            np.array([(x_H + axis_right) / 2, 1.75, 0])
        )
        right_attenuated.set_z_index(1)
        self.play(FadeIn(right_attenuated), run_time=max(0.05, 0.5))
        self.play(right_red_band.animate.set_opacity(0.3), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 3.26 - 1.3))

        # ========== BEAT 11: dim red bands, keep green band bright (37.14‑41.04) ==========
        self.play(
            left_red_band.animate.set_opacity(0.15),
            right_red_band.animate.set_opacity(0.15),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 3.9 - 1.5))

        # ========== BEAT 12: hold static (41.04‑42.20) ==========
        self.wait(max(0.05, 1.16))