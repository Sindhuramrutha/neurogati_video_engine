ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene13(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        S = lambda t: max(0.05, t)

        # ------------------------------------------------------------
        # Raw trace / top signal
        # ------------------------------------------------------------
        raw_trace = FunctionGraph(
            lambda x: 0.20 * np.sin(3.0 * x)
            + 0.13 * np.sin(7.3 * x + 1.2)
            + 0.08 * np.sin(13.5 * x + 0.4)
            + 0.04 * np.sin(19.0 * x + 2.0),
            x_range=[-4.2, 4.2, 0.02],
            color=WHITE,
            stroke_width=3,
        ).move_to([0, 2.5, 0])

        raw_label = Text("Raw extracellular signal", font_size=21,
                         color=WHITE, weight=BOLD)
        raw_label.next_to(raw_trace, UP, buff=0.15)

        raw_trace_group = VGroup(raw_trace, raw_label)
        raw_box = SurroundingRectangle(raw_trace_group, buff=0.12,
                                       color=WHITE, stroke_width=2)

        fast_layer = FunctionGraph(
            lambda x: 0.18 * np.sin(12.0 * x) + 0.08 * np.sin(19.0 * x + 1.1),
            x_range=[-4.2, 4.2, 0.02],
            color=BLUE,
            stroke_width=2,
        ).move_to([0, 2.5, 0])

        slow_layer = FunctionGraph(
            lambda x: 0.38 * np.sin(1.7 * x + 0.5),
            x_range=[-4.2, 4.2, 0.02],
            color=ORANGE,
            stroke_width=5,
        ).move_to([0, 2.5, 0])

        mixture_label = Text("mixture of components", font_size=20,
                             color=YELLOW)
        mixture_label.next_to(raw_box, DOWN, buff=0.20)

        sig_proc_caption = Text("signal processing is essential",
                                font_size=28, color=WHITE, weight=BOLD)
        sig_proc_caption.move_to([0, 0.7, 0])

        raw_highlight = SurroundingRectangle(raw_trace, buff=0.08,
                                             color=YELLOW, stroke_width=4)
        raw_label_underline = Line(
            raw_label.get_left() + DOWN * 0.14,
            raw_label.get_right() + DOWN * 0.14,
            color=YELLOW,
            stroke_width=4,
        )

        raw_measurement_overlay = Text("raw electrical measurement",
                                       font_size=18, color=YELLOW,
                                       weight=BOLD)
        raw_measurement_overlay.move_to(raw_trace.get_bottom() + DOWN * 0.25)

        # warning note next to raw trace box
        not_yet = Text("not yet", font_size=17, color=WHITE)
        final_info = Text("final information", font_size=17, color=WHITE)
        warning_note = VGroup(not_yet, final_info)
        warning_note.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        warning_note.next_to(raw_box, RIGHT, buff=0.20)

        # ------------------------------------------------------------
        # helper builders
        # ------------------------------------------------------------
        def make_box(text, center, width=2.4, height=0.7,
                     font_size=16, stroke_color=WHITE):
            rect = Rectangle(
                width=width, height=height,
                fill_color=GREY, fill_opacity=0.25,
                stroke_color=stroke_color, stroke_width=2,
            ).move_to(center)
            label = Text(text, font_size=font_size, color=WHITE)
            label.scale_to_fit_width(width - 0.3)
            label.move_to(rect.get_center())
            return VGroup(rect, label), rect, label

        def make_branch_box(text, center, icon_type, stroke_color=WHITE):
            rect = Rectangle(
                width=3.0, height=0.95,
                fill_color=GREY, fill_opacity=0.25,
                stroke_color=stroke_color, stroke_width=2,
            ).move_to(center)
            label = Text(text, font_size=14, color=WHITE)
            label.scale_to_fit_width(2.4)
            label.move_to(rect.get_center() + UP * 0.13)
            if icon_type == "spike":
                icon = FunctionGraph(
                    lambda x: 0.09 * np.sin(14.0 * x),
                    x_range=[-0.35, 0.35, 0.01],
                    color=BLUE,
                    stroke_width=2.5,
                ).move_to(rect.get_bottom() + UP * 0.28)
            else:
                icon = FunctionGraph(
                    lambda x: 0.13 * np.sin(3.5 * x),
                    x_range=[-0.35, 0.35, 0.01],
                    color=ORANGE,
                    stroke_width=3,
                ).move_to(rect.get_bottom() + UP * 0.28)
            group = VGroup(rect, label)
            return group, rect, label, icon

        # ------------------------------------------------------------
        # Main pipeline boxes
        # ------------------------------------------------------------
        filtering_box, filtering_rect, filtering_label = make_box(
            "Filtering", np.array([0, 1.35, 0]), width=2.4, height=0.7,
            font_size=18)

        left_branch_box, left_branch_rect, left_branch_label, left_spike_icon = (
            make_branch_box("High-frequency\nspike component",
                            np.array([-2.7, 0.0, 0]), "spike"))
        right_branch_box, right_branch_rect, right_branch_label, right_lfp_icon = (
            make_branch_box("Lower-frequency\nLFP component",
                            np.array([2.7, 0.0, 0]), "lfp"))

        feature_box, feature_rect, feature_label = make_box(
            "Feature extraction", np.array([0, -1.0, 0]),
            width=2.5, height=0.65, font_size=16)

        neural_rect = Rectangle(
            width=3.6, height=0.7,
            fill_color=GREY, fill_opacity=0.25,
            stroke_color=WHITE, stroke_width=2,
        ).move_to([0, -2.0, 0])
        neural_part1 = Text("Neural interpretation", font_size=16, color=WHITE)
        neural_slash = Text("/", font_size=16, color=WHITE)
        neural_part3 = Text("decoding", font_size=16, color=WHITE)
        neural_label_text = VGroup(neural_part1, neural_slash, neural_part3)
        neural_label_text.arrange(RIGHT, buff=0.12)
        neural_label_text.move_to(neural_rect.get_center())
        neural_box_group = VGroup(neural_rect, neural_label_text)

        # ------------------------------------------------------------
        # Arrows
        # ------------------------------------------------------------
        down_arrow = Arrow(
            raw_box.get_bottom() + DOWN * 0.05,
            filtering_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=4, buff=0.05,
        )

        left_branch_arrow = Arrow(
            filtering_rect.get_bottom() + DOWN * 0.05,
            left_branch_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=4, buff=0.05,
        )
        right_branch_arrow = Arrow(
            filtering_rect.get_bottom() + DOWN * 0.05,
            right_branch_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=4, buff=0.05,
        )

        left_converge_arrow = Arrow(
            left_branch_rect.get_bottom() + DOWN * 0.05,
            feature_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=4, buff=0.05,
        )
        right_converge_arrow = Arrow(
            right_branch_rect.get_bottom() + DOWN * 0.05,
            feature_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=4, buff=0.05,
        )

        final_down_arrow = Arrow(
            feature_rect.get_bottom() + DOWN * 0.05,
            neural_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=4, buff=0.05,
        )

        pipeline_bg = VGroup(
            raw_trace, raw_label, raw_box, fast_layer, slow_layer,
            filtering_box, left_branch_box, right_branch_box,
            left_spike_icon, right_lfp_icon,
            left_branch_arrow, right_branch_arrow,
            left_converge_arrow, right_converge_arrow,
            feature_box, final_down_arrow, neural_box_group,
        )

        # ------------------------------------------------------------
        # Foreground chains for spike / LFP details
        # ------------------------------------------------------------
        left_fg_branch, lfgb_rect, lfgb_label, lfgb_icon = make_branch_box(
            "High-frequency\nspike component", np.array([-4.9, 1.2, 0]),
            "spike", stroke_color=BLUE)
        left_fg_branch.add(lfgb_icon)
        for_spikes_label = Text("For spikes", font_size=22, color=WHITE,
                                weight=BOLD)
        for_spikes_label.next_to(left_fg_branch, UP, buff=0.15)

        highpass_box, highpass_rect, highpass_label = make_box(
            "High-pass filtering", np.array([-4.9, 0.0, 0]),
            width=2.6, height=0.7, font_size=14)
        spike_detect_box, sd_rect, sd_label = make_box(
            "Spike detection", np.array([-4.9, -1.05, 0]),
            width=2.6, height=0.7, font_size=14)
        spike_sort_box, ss_rect, ss_label = make_box(
            "Spike sorting", np.array([-4.9, -2.1, 0]),
            width=2.6, height=0.7, font_size=14)

        l_arrow1 = Arrow(
            left_fg_branch.get_bottom() + DOWN * 0.05,
            highpass_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=3, buff=0.05,
        )
        l_arrow2 = Arrow(
            highpass_rect.get_bottom() + DOWN * 0.05,
            sd_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=3, buff=0.05,
        )
        l_arrow3 = Arrow(
            sd_rect.get_bottom() + DOWN * 0.05,
            ss_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=3, buff=0.05,
        )
        left_fg_chain = VGroup(
            left_fg_branch, for_spikes_label, l_arrow1, highpass_box,
            l_arrow2, spike_detect_box, l_arrow3, spike_sort_box,
        )

        right_fg_branch, rfgb_rect, rfgb_label, rfgb_icon = make_branch_box(
            "Lower-frequency\nLFP component", np.array([4.9, 1.2, 0]),
            "lfp", stroke_color=ORANGE)
        right_fg_branch.add(rfgb_icon)
        for_lfps_label = Text("For LFPs", font_size=22, color=WHITE,
                              weight=BOLD)
        for_lfps_label.next_to(right_fg_branch, UP, buff=0.15)

        low_freq_box, lf_rect, lf_label = make_box(
            "Low-frequency filtering", np.array([4.9, 0.0, 0]),
            width=2.6, height=0.7, font_size=14)
        spectral_box, spectral_rect, spectral_label = make_box(
            "Spectral analysis", np.array([4.9, -1.05, 0]),
            width=2.6, height=0.7, font_size=14)
        time_freq_box, tf_rect, tf_label = make_box(
            "Time-frequency analysis", np.array([4.9, -2.1, 0]),
            width=2.6, height=0.7, font_size=14)

        r_arrow1 = Arrow(
            right_fg_branch.get_bottom() + DOWN * 0.05,
            lf_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=3, buff=0.05,
        )
        r_arrow2 = Arrow(
            lf_rect.get_bottom() + DOWN * 0.05,
            spectral_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=3, buff=0.05,
        )
        r_arrow3 = Arrow(
            spectral_rect.get_bottom() + DOWN * 0.05,
            tf_rect.get_top() + UP * 0.05,
            color=WHITE, stroke_width=3, buff=0.05,
        )
        right_fg_chain = VGroup(
            right_fg_branch, for_lfps_label, r_arrow1, low_freq_box,
            r_arrow2, spectral_box, r_arrow3, time_freq_box,
        )

        bottom_caption = Text("meaningful neural features",
                              font_size=26, color=YELLOW, weight=BOLD)
        bottom_caption.to_edge(DOWN, buff=0.30)

        # ============================================================
        # BEAT 1  [0.00 - 4.58]
        # ============================================================
        self.play(Create(raw_trace), run_time=max(0.05, S(0.80)))
        self.wait(max(0.05, S(1.32)))  # 0.80 -> 2.12
        self.play(FadeIn(sig_proc_caption), run_time=max(0.05, S(0.60)))
        self.wait(max(0.05, S(0.56)))  # 2.72 -> 3.28
        self.play(
            sig_proc_caption.animate.set_color(YELLOW),
            raw_trace.animate.set_stroke(YELLOW, width=5),
            run_time=max(0.05, S(0.50)),
        )
        self.play(
            sig_proc_caption.animate.set_color(WHITE),
            raw_trace.animate.set_stroke(WHITE, width=3),
            run_time=max(0.05, S(0.40)),
        )
        self.wait(max(0.05, S(0.40)))  # 4.18 -> 4.58
        self.play(FadeOut(sig_proc_caption), run_time=max(0.05, S(0.20)))
        self.wait(max(0.05, S(0.88)))  # 4.78 -> 5.66

        # ============================================================
        # BEAT 2  [5.66 - 8.78]
        # ============================================================
        self.play(
            raw_trace.animate.set_stroke(WHITE, width=3).set_color(WHITE),
            FadeIn(raw_label),
            run_time=max(0.05, S(0.20)),
        )
        self.wait(max(0.05, S(0.68)))  # 5.86 -> 6.54
        self.play(FadeIn(raw_box), run_time=max(0.05, S(0.50)))  # 6.54 -> 7.04
        self.play(Indicate(raw_box, color=YELLOW), run_time=max(0.05, S(0.78)))
        self.play(
            FadeIn(fast_layer),
            FadeIn(slow_layer),
            raw_trace.animate.set_opacity(0.55),
            run_time=max(0.05, S(0.44)),
        )
        self.play(
            fast_layer.animate.shift(UP * 0.12),
            slow_layer.animate.shift(DOWN * 0.12),
            run_time=max(0.05, S(0.12)),
        )
        self.play(
            fast_layer.animate.shift(DOWN * 0.12),
            slow_layer.animate.shift(UP * 0.12),
            run_time=max(0.05, S(0.12)),
        )
        self.play(FadeIn(mixture_label), run_time=max(0.05, S(0.28)))
        self.play(FadeOut(mixture_label), run_time=max(0.05, S(0.15)))
        self.wait(max(0.05, S(0.81)))  # 8.93 -> 9.74

        # ============================================================
        # BEAT 3  [9.74 - 13.22]
        # ============================================================
        self.play(Create(down_arrow), run_time=max(0.05, S(0.16)))  # 9.74 -> 9.90
        self.play(down_arrow.animate.set_opacity(0.7), run_time=max(0.05, S(0.10)))
        self.wait(max(0.05, S(0.44)))  # 10.00 -> 10.44
        self.play(
            FadeOut(down_arrow),
            FadeIn(left_branch_arrow),
            FadeIn(right_branch_arrow),
            run_time=max(0.05, S(0.62)),
        )
        self.wait(max(0.05, S(0.28)))  # 11.06 -> 11.34
        self.play(
            raw_box.animate.set_opacity(0.4),
            raw_trace.animate.set_opacity(0.4),
            fast_layer.animate.set_opacity(0.4),
            slow_layer.animate.set_opacity(0.4),
            raw_label.animate.set_opacity(0.7),
            run_time=max(0.05, S(0.66)),
        )
        self.wait(max(0.05, S(0.74)))  # 12.00 -> 12.74
        self.play(Indicate(raw_label, color=YELLOW), run_time=max(0.05, S(0.40)))
        self.wait(max(0.05, S(0.48)))  # 13.14 -> 13.62

        # ============================================================
        # BEAT 4  [13.62 - 18.02]
        # ============================================================
        self.play(FadeIn(filtering_box), run_time=max(0.05, S(0.10)))
        self.play(Indicate(filtering_box, color=YELLOW), run_time=max(0.05, S(0.30)))
        self.wait(max(0.05, S(0.60)))  # 14.02 -> 14.62
        self.play(Indicate(left_branch_arrow, color=YELLOW),
                  run_time=max(0.05, S(0.08)))
        self.play(FadeIn(left_branch_box), run_time=max(0.05, S(0.14)))
        self.wait(max(0.05, S(0.30)))  # 14.84 -> 15.14
        self.play(GrowFromCenter(left_spike_icon), run_time=max(0.05, S(0.38)))
        self.play(Indicate(left_branch_box, color=YELLOW),
                  run_time=max(0.05, S(0.78)))
        self.play(Indicate(right_branch_arrow, color=YELLOW),
                  run_time=max(0.05, S(0.10)))
        self.play(FadeIn(right_branch_box), run_time=max(0.05, S(0.22)))
        self.wait(max(0.05, S(0.42)))  # 16.62 -> 17.04
        self.play(GrowFromCenter(right_lfp_icon), run_time=max(0.05, S(0.54)))
        self.play(Indicate(right_branch_box, color=YELLOW),
                  run_time=max(0.05, S(0.44)))
        self.wait(max(0.05, S(0.46)))  # 18.02 -> 18.48

        # ============================================================
        # BEAT 5  [18.48 - 22.20]
        # ============================================================
        self.play(
            Create(left_converge_arrow),
            Create(right_converge_arrow),
            run_time=max(0.05, S(0.30)),
        )
        self.play(FadeIn(feature_box), run_time=max(0.05, S(0.26)))
        self.play(Indicate(feature_box, color=YELLOW), run_time=max(0.05, S(0.56)))
        self.wait(max(0.05, S(0.50)))  # 19.60 -> 20.10
        self.play(Create(final_down_arrow), run_time=max(0.05, S(0.54)))
        self.play(FadeIn(neural_rect), run_time=max(0.05, S(0.26)))
        self.play(Write(neural_label_text), run_time=max(0.05, S(0.66)))
        self.play(neural_slash.animate.set_opacity(0), run_time=max(0.05, S(0.10)))
        self.play(neural_slash.animate.set_opacity(1), run_time=max(0.05, S(0.10)))
        self.wait(max(0.05, S(0.30)))  # 21.76 -> 22.06
        self.play(Indicate(neural_box_group, color=YELLOW),
                  run_time=max(0.05, S(0.14)))
        self.wait(max(0.05, S(1.10)))  # 22.20 -> 23.30

        # ============================================================
        # BEAT 6  [23.30 - 28.24]
        # ============================================================
        self.play(
            pipeline_bg.animate.set_opacity(0.25).shift(UP * 0.5),
            FadeIn(left_fg_branch),
            run_time=max(0.05, S(0.06)),
        )
        self.play(FadeIn(for_spikes_label), run_time=max(0.05, S(0.60)))
        self.wait(max(0.05, S(0.10)))  # 23.96 -> 24.06
        self.play(Create(l_arrow1), run_time=max(0.05, S(0.84)))
        self.play(FadeIn(highpass_box), run_time=max(0.05, S(0.32)))
        self.wait(max(0.05, S(0.26)))  # 25.22 -> 25.48
        self.play(Indicate(highpass_box, color=YELLOW), run_time=max(0.05, S(0.20)))
        self.play(Create(l_arrow2), run_time=max(0.05, S(0.98)))
        self.play(FadeIn(spike_detect_box), run_time=max(0.05, S(0.14)))
        self.play(Indicate(spike_detect_box, color=YELLOW),
                  run_time=max(0.05, S(0.20)))
        self.wait(max(0.05, S(0.78)))  # 27.00 -> 27.78
        self.play(Create(l_arrow3), run_time=max(0.05, S(0.20)))
        self.play(FadeIn(spike_sort_box), run_time=max(0.05, S(0.26)))
        self.wait(max(0.05, S(0.76)))  # 28.24 -> 29.00

        # ============================================================
        # BEAT 7  [29.00 - 36.22]
        # ============================================================
        self.play(
            left_fg_chain.animate.set_opacity(0.30).shift(LEFT * 0.6),
            FadeIn(right_fg_branch),
            run_time=max(0.05, S(0.40)),
        )
        self.play(FadeIn(for_lfps_label), run_time=max(0.05, S(0.56)))
        self.wait(max(0.05, S(0.50)))  # 29.96 -> 30.46
        self.play(Create(r_arrow1), run_time=max(0.05, S(0.42)))
        self.wait(max(0.05, S(0.40)))  # 30.88 -> 31.28
        self.play(FadeIn(low_freq_box), run_time=max(0.05, S(0.30)))
        self.wait(max(0.05, S(0.40)))  # 31.58 -> 31.98
        self.play(Indicate(low_freq_box, color=YELLOW), run_time=max(0.05, S(0.36)))
        self.play(Create(r_arrow2), run_time=max(0.05, S(1.30)))
        self.play(FadeIn(spectral_box), run_time=max(0.05, S(0.22)))
        self.play(Indicate(spectral_box, color=YELLOW), run_time=max(0.05, S(0.20)))
        self.wait(max(0.05, S(1.06)))  # 34.06 -> 35.12
        self.play(Create(r_arrow3), run_time=max(0.05, S(0.06)))
        self.play(FadeIn(time_freq_box), run_time=max(0.05, S(0.22)))
        self.wait(max(0.05, S(0.30)))  # 35.40 -> 35.70
        self.play(Indicate(time_freq_box, color=YELLOW), run_time=max(0.05, S(0.34)))
        self.wait(max(0.05, S(0.18)))  # 36.04 -> 36.22
        self.wait(max(0.05, S(1.14)))  # 36.22 -> 37.36

        # ============================================================
        # BEAT 8  [37.36 - 41.58]
        # ============================================================
        self.play(
            FadeOut(left_fg_chain),
            FadeOut(right_fg_chain),
            pipeline_bg.animate.set_opacity(1).shift(DOWN * 0.5),
            FadeIn(raw_highlight),
            run_time=max(0.05, S(0.30)),
        )
        self.wait(max(0.05, S(0.50)))  # 37.66 -> 38.16
        self.play(Create(raw_label_underline), run_time=max(0.05, S(0.24)))
        self.wait(max(0.05, S(0.20)))  # 38.40 -> 38.60
        self.play(FadeOut(raw_highlight), run_time=max(0.05, S(0.10)))
        self.wait(max(0.05, S(0.04)))  # 38.70 -> 38.74
        self.play(raw_trace.animate.set_opacity(0.65), run_time=max(0.05, S(0.28)))
        self.play(Indicate(raw_box, color=YELLOW), run_time=max(0.05, S(0.50)))
        self.play(FadeIn(not_yet), run_time=max(0.05, S(0.46)))
        self.play(not_yet.animate.set_color(ORANGE), run_time=max(0.05, S(0.22)))
        self.play(Indicate(not_yet, color=ORANGE), run_time=max(0.05, S(0.26)))
        self.play(FadeIn(final_info), run_time=max(0.05, S(0.40)))
        self.play(
            not_yet.animate.set_color(GREY),
            final_info.animate.set_color(GREY),
            run_time=max(0.05, S(0.72)),
        )
        self.play(FadeOut(not_yet, final_info), run_time=max(0.05, S(0.30)))
        self.wait(max(0.05, S(0.46)))  # 41.88 -> 42.34

        # ============================================================
        # BEAT 9  [42.34 - 47.78]
        # ============================================================
        self.play(
            raw_trace.animate.set_opacity(1).set_stroke(WHITE, width=3),
            run_time=max(0.05, S(0.24)),
        )
        self.play(
            filtering_rect.animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, S(0.52)),
        )

        common_path = VMobject().set_points_as_corners([
            raw_trace.get_bottom(), filtering_rect.get_top(),
        ])
        left_path = VMobject().set_points_as_corners([
            filtering_rect.get_bottom(), left_branch_rect.get_top(),
            left_branch_rect.get_bottom(), feature_rect.get_top(),
        ])
        right_path = VMobject().set_points_as_corners([
            filtering_rect.get_bottom(), right_branch_rect.get_top(),
            right_branch_rect.get_bottom(), feature_rect.get_top(),
        ])

        dot_common = Dot(raw_trace.get_bottom(), radius=0.06,
                         color=YELLOW, fill_opacity=1)
        self.add(dot_common)
        self.play(MoveAlongPath(dot_common, common_path), run_time=max(0.05, S(0.30)))
        self.remove(dot_common)

        dot_left = Dot(filtering_rect.get_bottom(), radius=0.055,
                       color=YELLOW, fill_opacity=1)
        dot_right = Dot(filtering_rect.get_bottom(), radius=0.055,
                        color=YELLOW, fill_opacity=1)
        self.add(dot_left, dot_right)
        self.play(
            MoveAlongPath(dot_left, left_path),
            MoveAlongPath(dot_right, right_path),
            run_time=max(0.05, S(0.52)),
        )
        self.remove(dot_left, dot_right)

        # colored layers flow into the two branch boxes
        flow_fast = fast_layer.copy().set_color(BLUE)
        flow_slow = slow_layer.copy().set_color(ORANGE)
        flow_fast_path = VMobject().set_points_as_corners([
            raw_trace.get_center(), left_branch_rect.get_center(),
        ])
        flow_slow_path = VMobject().set_points_as_corners([
            raw_trace.get_center(), right_branch_rect.get_center(),
        ])
        self.add(flow_fast, flow_slow)
        self.play(
            MoveAlongPath(flow_fast, flow_fast_path),
            MoveAlongPath(flow_slow, flow_slow_path),
            run_time=max(0.05, S(0.88)),
        )
        self.remove(flow_fast, flow_slow)

        self.play(raw_trace.animate.set_opacity(0.4), run_time=max(0.05, S(0.18)))
        self.play(Indicate(raw_label, color=YELLOW), run_time=max(0.05, S(0.52)))
        self.play(FadeIn(raw_measurement_overlay), run_time=max(0.05, S(0.34)))
        self.wait(max(0.05, S(0.74)))  # 45.84 -> 46.58

        self.play(Indicate(feature_box, color=YELLOW), run_time=max(0.05, S(0.40)))
        self.play(
            neural_rect.animate.set_stroke(YELLOW, width=4),
            neural_label_text.animate.set_color(YELLOW),
            run_time=max(0.05, S(0.36)),
        )

        caption_path = VMobject().set_points_as_corners([
            feature_rect.get_bottom(), neural_rect.get_top(),
            neural_rect.get_bottom(), bottom_caption.get_top(),
        ])
        caption_dot = Dot(feature_rect.get_bottom(), radius=0.05,
                          color=YELLOW, fill_opacity=1)
        self.add(caption_dot)
        self.play(
            FadeIn(bottom_caption),
            MoveAlongPath(caption_dot, caption_path),
            run_time=max(0.05, S(0.44)),
        )
        self.remove(caption_dot)

        # ============================================================
        # BEAT 10  [47.78 - 48.60]
        # ============================================================
        self.play(
            pipeline_bg.animate.scale(1.015),
            bottom_caption.animate.scale(1.03),
            run_time=max(0.05, S(0.30)),
        )
        self.play(
            pipeline_bg.animate.scale(1 / 1.015),
            bottom_caption.animate.scale(1 / 1.03),
            run_time=max(0.05, S(0.30)),
        )
        self.wait(max(0.05, S(0.22)))  # 48.38 -> 48.60