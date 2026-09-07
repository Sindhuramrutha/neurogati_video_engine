ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----------------------------------------------------------------
        # Helper waveform builders -- low sample counts for fast render.
        # ----------------------------------------------------------------
        def make_ns_wave(phase=0.0, x_left=-4.2, x_right=4.2, center_y=-1.5,
                         color=ORANGE, stroke_width=2.5):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                freq = 1.5 + 2.0 * abs(np.sin(phase * 0.8))
                amp = 0.35 + 0.20 * np.sin(2 * np.pi * (0.6 * t + phase))
                y = center_y + amp * np.sin(2 * np.pi * freq * t + 2.0 * phase)
                return np.array([x, y, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.03],
                                      color=color, stroke_width=stroke_width)

        def make_eeg_t1_trace(x_left, x_right, center_y=0.0, color=WHITE,
                              stroke_width=2.5):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                base = (0.33 * np.sin(2 * np.pi * 1.2 * t + 0.4)
                        + 0.18 * np.sin(2 * np.pi * 2.4 * t + 1.0))
                burst = 0.85 * np.exp(-(((t - 0.38) / 0.035) ** 2)) * np.sin(2 * np.pi * 12 * t)
                chirp = 0.0
                if 0.58 < t < 0.92:
                    ct = (t - 0.58) / 0.34
                    chirp = 0.38 * np.sin(2 * np.pi * (1.3 + 6.0 * ct) * ct)
                return np.array([x, center_y + base + burst + chirp, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.01],
                                      color=color, stroke_width=stroke_width)

        def make_burst_segment(x_left, x_right, center_y=0.0, color=ORANGE,
                               stroke_width=5):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                burst = 0.85 * np.exp(-(((t - 0.38) / 0.035) ** 2)) * np.sin(2 * np.pi * 12 * t)
                return np.array([x, center_y + burst, 0.0])

            return ParametricFunction(f, t_range=[0.34, 0.42, 0.005],
                                      color=color, stroke_width=stroke_width)

        def make_chirp_wave(center_x, center_y, wave_width=2.2, color=TEAL,
                            stroke_width=3.2):
            def f(t):
                x = center_x - wave_width / 2 + wave_width * t
                freq = 1.1 + 3.2 * t
                y = center_y + 0.30 * np.sin(2 * np.pi * freq * t)
                return np.array([x, y, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.03],
                                      color=color, stroke_width=stroke_width)

        def make_spike_trace(x_left, x_right, center_y=0.0, color=WHITE,
                             stroke_width=2.8):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                base = 0.38 * np.sin(2 * np.pi * 1.0 * t)
                spike = 1.75 * np.exp(-(((t - 0.5) / 0.012) ** 2)) * np.sin(2 * np.pi * 18 * t)
                return np.array([x, center_y + base + spike, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.01],
                                      color=color, stroke_width=stroke_width)

        def make_spike_highlight(x_left, x_right, center_y=0.0, color=RED,
                                 stroke_width=6):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                spike = 1.75 * np.exp(-(((t - 0.5) / 0.012) ** 2)) * np.sin(2 * np.pi * 18 * t)
                return np.array([x, center_y + spike, 0.0])

            return ParametricFunction(f, t_range=[0.47, 0.53, 0.005],
                                      color=color, stroke_width=stroke_width)

        def make_erp_wave(x_left, x_right, center_y=0.0, color=WHITE,
                          stroke_width=2.5):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                baseline = 0.15 * np.sin(2 * np.pi * 0.8 * t)
                response = 1.1 * np.exp(-(((t - 0.5) / 0.04) ** 2)) * np.sin(2 * np.pi * 1.2 * (t - 0.5))
                return np.array([x, center_y + baseline + response, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.01],
                                      color=color, stroke_width=stroke_width)

        def make_bci_wave(phase=0.0, x_left=-4.3, x_right=-2.1, center_y=0.0,
                          color=WHITE, stroke_width=2.2):
            width = x_right - x_left

            def f(t):
                x = x_left + width * t
                amp = 0.28 + 0.22 * np.sin(2 * np.pi * 0.6 * t + phase)
                freq = 1.2 + 1.8 * (0.5 + 0.5 * np.sin(phase + 1.2 * t))
                y = center_y + amp * np.sin(2 * np.pi * freq * t)
                return np.array([x, y, 0.0])

            return ParametricFunction(f, t_range=[0, 1, 0.03],
                                      color=color, stroke_width=stroke_width)

        # ----------------------------------------------------------------
        # Beat 1: 0.00-3.92
        # ----------------------------------------------------------------
        title_txt = Text("Wavelet analysis", font_size=44, color=WHITE)
        title_txt.move_to([0, 2.8, 0])
        self.play(Write(title_txt), run_time=max(0.05, 0.45))

        wave_icon = SVGMobject(ASSET_PATHS["soundwave"], height=0.8,
                               color=WHITE, fill_color=WHITE)
        wave_icon.move_to([0, 1.7, 0])
        base_icon_width = wave_icon.width
        self.play(FadeIn(wave_icon), run_time=max(0.05, 0.30))

        words = ["Wavelet", "analysis", "has", "become", "an", "important",
                 "tool", "in", "modern", "neuroscience"]
        word_mobs = [Text(w, font_size=26, color=WHITE) for w in words]
        sentence_group = VGroup(*word_mobs).arrange(RIGHT, buff=0.14)
        sentence_group.scale_to_fit_width(11)
        sentence_group.move_to([0, 0.2, 0])

        icon_factors = [1.0, 1.18, 1.35, 1.18, 1.0, 0.86, 0.72, 0.86, 1.0, 1.18]
        icon_widths = [base_icon_width * f for f in icon_factors]

        per_word = 0.264
        for i, word in enumerate(word_mobs):
            if i == 5:
                self.play(FadeIn(word),
                          wave_icon.animate.stretch_to_fit_width(icon_widths[i]),
                          run_time=max(0.05, per_word * 0.5))
                self.play(word.animate.set_color(YELLOW),
                          run_time=max(0.05, per_word * 0.5))
            else:
                self.play(FadeIn(word),
                          wave_icon.animate.stretch_to_fit_width(icon_widths[i]),
                          run_time=max(0.05, per_word))

        self.wait(max(0.05, 0.53))  # 3.39 -> 3.92

        # ----------------------------------------------------------------
        # Beat 2: 3.92-7.54
        # ----------------------------------------------------------------
        ns_wave = make_ns_wave()
        ns_label = Text("nonstationary", font_size=26, color=YELLOW)
        ns_label.move_to([0, -2.7, 0])

        self.play(FadeIn(ns_wave), run_time=max(0.05, 0.40))
        self.play(FadeIn(ns_label), run_time=max(0.05, 0.50))
        self.play(ns_wave.animate.stretch_to_fit_width(7.8), run_time=max(0.05, 0.55))
        self.play(ns_wave.animate.stretch_to_fit_width(5.2), run_time=max(0.05, 0.55))
        self.play(ns_wave.animate.stretch_to_fit_height(1.45), run_time=max(0.05, 0.55))
        self.play(ns_wave.animate.stretch_to_fit_height(0.95), run_time=max(0.05, 0.55))
        self.play(ns_wave.animate.stretch_to_fit_width(4.0), run_time=max(0.05, 0.52))

        # ----------------------------------------------------------------
        # Beat 3: 8.18-10.66
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.64))  # gap 7.54 -> 8.18

        top_group = VGroup(title_txt, wave_icon, sentence_group, ns_wave, ns_label)
        top_group.generate_target()
        top_group.target.scale(0.55)
        top_group.target.to_edge(UP, buff=0.35)
        self.play(MoveToTarget(top_group), run_time=max(0.05, 1.0))

        heading = Text("Some common applications include:", font_size=28, color=WHITE)
        heading.next_to(top_group, DOWN, buff=0.35)
        self.play(FadeIn(heading), run_time=max(0.05, 0.60))

        panel_rects = [Rectangle(width=3.1, height=1.8,
                                 stroke_color=GREY_B, stroke_width=2,
                                 fill_color=BLACK, fill_opacity=0.55)
                       for _ in range(4)]
        panel_grid = VGroup(*panel_rects).arrange_in_grid(rows=2, cols=2, buff=0.35)
        panel_grid.scale_to_fit_width(7.8)
        panel_grid.next_to(heading, DOWN, buff=0.55)
        self.play(FadeIn(panel_grid), run_time=max(0.05, 0.88))

        slot_rects = [rect.copy() for rect in panel_rects]

        # ----------------------------------------------------------------
        # Beat 4: 10.66-14.18 -- EEG panel
        # ----------------------------------------------------------------
        exp_rect1 = Rectangle(width=9.0, height=5.0,
                              stroke_color=WHITE, stroke_width=3,
                              fill_color=BLACK, fill_opacity=0.55).move_to(ORIGIN)
        self.play(Transform(panel_rects[0], exp_rect1), run_time=max(0.05, 0.60))

        trace1_left = panel_rects[0].get_left()[0] + 0.6
        trace1_right = panel_rects[0].get_right()[0] - 0.6
        trace1_cy = panel_rects[0].get_center()[1]

        eeg_trace1 = make_eeg_t1_trace(trace1_left, trace1_right, trace1_cy,
                                       color=WHITE)
        label1 = Text("EEG analysis", font_size=28, color=WHITE)
        label1.next_to(panel_rects[0], UP, buff=0.3)
        self.play(Create(eeg_trace1), FadeIn(label1), run_time=max(0.05, 0.80))

        burst_highlight = make_burst_segment(trace1_left, trace1_right, trace1_cy,
                                             color=ORANGE, stroke_width=5)
        self.play(Create(burst_highlight), run_time=max(0.05, 0.50))

        for _ in range(2):
            self.play(burst_highlight.animate.set_stroke(width=9), run_time=max(0.05, 0.22))
            self.play(burst_highlight.animate.set_stroke(width=5), run_time=max(0.05, 0.22))

        self.wait(max(0.05, 0.74))  # fill to 14.18

        # ----------------------------------------------------------------
        # Beat 5: 14.46-18.04 -- rapidly changing rhythm in same panel
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.28))  # gap 14.18 -> 14.46

        self.play(burst_highlight.animate.set_stroke(width=5, opacity=0.55),
                  run_time=max(0.05, 0.45))

        chirp_x_center = trace1_left + (trace1_right - trace1_left) * 0.75
        chirp_rect = Rectangle(width=2.5, height=1.9,
                               stroke_color=TEAL, stroke_width=3, fill_opacity=0)
        chirp_rect.move_to([chirp_x_center, trace1_cy, 0])
        chirp_wave = make_chirp_wave(chirp_x_center, trace1_cy,
                                     wave_width=2.2, color=TEAL, stroke_width=3.2)

        self.play(Create(chirp_rect), FadeIn(chirp_wave), run_time=max(0.05, 0.50))

        for _ in range(2):
            self.play(chirp_wave.animate.stretch_to_fit_width(2.7), run_time=max(0.05, 0.45))
            self.play(chirp_wave.animate.stretch_to_fit_width(1.8), run_time=max(0.05, 0.45))

        self.wait(max(0.05, 0.83))  # fill to 18.04

        # ----------------------------------------------------------------
        # Beat 6: 18.86-20.22 -- shrink panel 1, expand panel 2
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.82))  # gap 18.04 -> 18.86

        panel1_content = VGroup(eeg_trace1, burst_highlight, chirp_rect, chirp_wave)
        slot1_left = slot_rects[0].get_left()[0]
        slot1_right = slot_rects[0].get_right()[0]
        slot1_cy = slot_rects[0].get_center()[1]
        cond1_trace = make_eeg_t1_trace(slot1_left + 0.25, slot1_right - 0.25,
                                        center_y=slot1_cy + 0.25,
                                        color=WHITE, stroke_width=1.2)
        cond1_label = Text("EEG analysis", font_size=11, color=WHITE)
        cond1_label.scale_to_fit_width(slot_rects[0].width * 0.85)
        cond1_label.move_to([slot_rects[0].get_center()[0],
                             slot_rects[0].get_bottom()[1] + 0.15, 0])
        cond1_group = VGroup(cond1_trace, cond1_label)

        self.play(FadeOut(panel1_content), FadeOut(label1),
                  FadeIn(cond1_group), Transform(panel_rects[0], slot_rects[0]),
                  run_time=max(0.05, 0.55))

        exp_rect2 = Rectangle(width=9.0, height=5.0,
                              stroke_color=WHITE, stroke_width=3,
                              fill_color=BLACK, fill_opacity=0.55).move_to(ORIGIN)
        self.play(Transform(panel_rects[1], exp_rect2), run_time=max(0.05, 0.45))

        rect2_left = panel_rects[1].get_left()[0]
        rect2_right = panel_rects[1].get_right()[0]
        rect2_top = panel_rects[1].get_top()[1]
        rect2_bottom = panel_rects[1].get_bottom()[1]
        rect2_cy = panel_rects[1].get_center()[1]

        marker_x = 0.0
        marker_line = Line([marker_x, rect2_top + 0.8, 0],
                           [marker_x, rect2_bottom - 0.8, 0],
                           color=YELLOW, stroke_width=3)
        bell_icon = SVGMobject(ASSET_PATHS["bell"], height=0.55,
                               color=WHITE, fill_color=WHITE)
        bell_icon.next_to(marker_line.get_top(), DOWN, buff=0.1)

        label2 = Text("Event-related brain activity", font_size=24, color=WHITE)
        label2.next_to(panel_rects[1], UP, buff=0.3)

        self.play(FadeIn(marker_line), FadeIn(bell_icon), FadeIn(label2),
                  run_time=max(0.05, 0.36))

        # ----------------------------------------------------------------
        # Beat 7: 20.96-25.78 -- ERP waveform + before/after windows
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.74))  # gap 20.22 -> 20.96

        erp_left = rect2_left + 0.7
        erp_right = rect2_right - 0.7
        erp_wave = make_erp_wave(erp_left, erp_right, rect2_cy, color=WHITE)
        self.play(Create(erp_wave), run_time=max(0.05, 0.70))

        before_right = marker_x - 0.35
        after_left = marker_x + 0.35
        shade_height = 2.2

        before_shade = Rectangle(width=before_right - erp_left, height=shade_height,
                                 stroke_opacity=0, fill_color=BLUE, fill_opacity=0.22)
        before_shade.move_to([(erp_left + before_right) / 2, rect2_cy, 0])
        after_shade = Rectangle(width=erp_right - after_left, height=shade_height,
                                stroke_opacity=0, fill_color=BLUE, fill_opacity=0.22)
        after_shade.move_to([(after_left + erp_right) / 2, rect2_cy, 0])
        shades = VGroup(before_shade, after_shade)

        self.play(FadeIn(shades), run_time=max(0.05, 0.60))
        self.play(shades.animate.set_opacity(0.42), run_time=max(0.05, 0.25))
        self.play(shades.animate.set_opacity(0.25), run_time=max(0.05, 0.25))

        deflection_highlight = make_erp_wave(erp_left, erp_right, rect2_cy,
                                             color=YELLOW, stroke_width=5)
        self.play(Create(deflection_highlight), run_time=max(0.05, 0.50))

        for _ in range(2):
            self.play(shades.animate.set_opacity(0.40),
                      deflection_highlight.animate.set_stroke(width=7),
                      run_time=max(0.05, 0.35))
            self.play(shades.animate.set_opacity(0.22),
                      deflection_highlight.animate.set_stroke(width=4),
                      run_time=max(0.05, 0.35))

        self.wait(max(0.05, 1.12))  # fill to 25.78

        # ----------------------------------------------------------------
        # Beat 8: 26.78-28.36 -- shrink panel 2, expand epilepsy panel
        # ----------------------------------------------------------------
        self.wait(max(0.05, 1.00))  # gap 25.78 -> 26.78

        panel2_content = VGroup(marker_line, bell_icon, erp_wave,
                                before_shade, after_shade, deflection_highlight)
        slot2_left = slot_rects[1].get_left()[0]
        slot2_right = slot_rects[1].get_right()[0]
        slot2_cy = slot_rects[1].get_center()[1]
        cond2_trace = make_erp_wave(slot2_left + 0.2, slot2_right - 0.2,
                                    center_y=slot2_cy + 0.25,
                                    color=WHITE, stroke_width=1.0)
        cond2_label = Text("Event-related brain activity", font_size=10, color=WHITE)
        cond2_label.scale_to_fit_width(slot_rects[1].width * 0.95)
        cond2_label.move_to([slot_rects[1].get_center()[0],
                             slot_rects[1].get_bottom()[1] + 0.15, 0])
        cond2_group = VGroup(cond2_trace, cond2_label)

        self.play(FadeOut(panel2_content), FadeOut(label2),
                  FadeIn(cond2_group), Transform(panel_rects[1], slot_rects[1]),
                  run_time=max(0.05, 0.45))

        exp_rect3 = Rectangle(width=9.0, height=5.0,
                              stroke_color=WHITE, stroke_width=3,
                              fill_color=BLACK, fill_opacity=0.55).move_to(ORIGIN)
        self.play(Transform(panel_rects[2], exp_rect3), run_time=max(0.05, 0.45))

        trace3_left = panel_rects[2].get_left()[0] + 0.6
        trace3_right = panel_rects[2].get_right()[0] - 0.6
        trace3_cy = panel_rects[2].get_center()[1]

        spike_trace = make_spike_trace(trace3_left, trace3_right, trace3_cy,
                                       color=WHITE)
        spike_highlight = make_spike_highlight(trace3_left, trace3_right, trace3_cy,
                                               color=RED, stroke_width=6)
        label3 = Text("Epilepsy research", font_size=28, color=WHITE)
        label3.next_to(panel_rects[2], UP, buff=0.3)

        self.play(Create(spike_trace), Create(spike_highlight), FadeIn(label3),
                  run_time=max(0.05, 0.68))

        # ----------------------------------------------------------------
        # Beat 9: 28.70-31.62 -- spike pulse + short-duration callout
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.34))  # gap 28.36 -> 28.70

        self.play(spike_highlight.animate.set_stroke(width=10), run_time=max(0.05, 0.20))
        self.play(spike_highlight.animate.set_stroke(width=6), run_time=max(0.05, 0.20))

        spike_x_center = trace3_left + (trace3_right - trace3_left) * 0.5
        duration_line = Line([spike_x_center - 0.35, trace3_cy + 1.4, 0],
                             [spike_x_center + 0.35, trace3_cy + 1.4, 0],
                             color=YELLOW, stroke_width=3)
        duration_label = Text("short duration", font_size=15, color=YELLOW)
        duration_label.next_to(duration_line, UP, buff=0.08)
        callout_group = VGroup(duration_line, duration_label)

        self.play(FadeIn(callout_group), run_time=max(0.05, 0.55))
        self.play(spike_highlight.animate.set_stroke(width=9), run_time=max(0.05, 0.45))
        self.play(spike_highlight.animate.set_stroke(width=5), run_time=max(0.05, 0.35))
        self.play(spike_highlight.animate.set_stroke(width=7), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.82))  # fill to 31.62

        # ----------------------------------------------------------------
        # Beat 10: 31.80-35.32 -- fixed-window comparison ghost
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.18))  # gap 31.62 -> 31.80

        orig_group = VGroup(spike_trace, spike_highlight, callout_group)
        self.play(orig_group.animate.scale(0.62).shift(LEFT * 2.3),
                  run_time=max(0.05, 0.60))

        ghost_left = 1.3
        ghost_right = 4.3
        ghost_cy = trace3_cy
        ghost_trace = make_spike_trace(ghost_left, ghost_right, ghost_cy,
                                       color=GREY, stroke_width=2.0)
        ghost_trace.set_opacity(0.8)

        fixed_window = Rectangle(width=0.9, height=1.6,
                                 stroke_color=GREY, stroke_width=2,
                                 fill_color=GREY, fill_opacity=0.45)
        fixed_window.move_to([(ghost_left + ghost_right) / 2, ghost_cy, 0])
        ghost_group = VGroup(ghost_trace, fixed_window).set_opacity(0.85)

        self.play(FadeIn(ghost_group), run_time=max(0.05, 0.70))

        conventional_label = Text("conventional frequency analysis",
                                  font_size=16, color=WHITE)
        conventional_label.next_to(ghost_group, DOWN, buff=0.4)
        self.play(FadeIn(conventional_label), run_time=max(0.05, 0.60))

        self.play(ghost_group.animate.set_opacity(0.35),
                  spike_highlight.animate.set_stroke(width=9),
                  run_time=max(0.05, 0.70))

        self.wait(max(0.05, 0.92))  # fill to 35.32

        # ----------------------------------------------------------------
        # Beat 11: 36.34-37.98 -- shrink panel 3, expand BCI panel
        # ----------------------------------------------------------------
        self.wait(max(0.05, 1.02))  # gap 35.32 -> 36.34

        panel3_content = VGroup(orig_group, ghost_group, conventional_label)
        slot3_left = slot_rects[2].get_left()[0]
        slot3_right = slot_rects[2].get_right()[0]
        slot3_cy = slot_rects[2].get_center()[1]
        cond3_trace = make_spike_trace(slot3_left + 0.3, slot3_right - 0.3,
                                       center_y=slot3_cy + 0.25,
                                       color=WHITE, stroke_width=1.0)
        cond3_label = Text("Epilepsy research", font_size=10, color=WHITE)
        cond3_label.scale_to_fit_width(slot_rects[2].width * 0.9)
        cond3_label.move_to([slot_rects[2].get_center()[0],
                             slot_rects[2].get_bottom()[1] + 0.15, 0])
        cond3_group = VGroup(cond3_trace, cond3_label)

        self.play(FadeOut(panel3_content), FadeOut(label3),
                  FadeIn(cond3_group), Transform(panel_rects[2], slot_rects[2]),
                  run_time=max(0.05, 0.45))

        exp_rect4 = Rectangle(width=9.0, height=5.0,
                              stroke_color=WHITE, stroke_width=3,
                              fill_color=BLACK, fill_opacity=0.55).move_to(ORIGIN)
        self.play(Transform(panel_rects[3], exp_rect4), run_time=max(0.05, 0.45))

        bci_left_x = -4.3
        bci_right_x = -2.1
        bci_y = panel_rects[3].get_center()[1]
        bci_wave = make_bci_wave(0.0, bci_left_x, bci_right_x, bci_y,
                                 color=WHITE, stroke_width=2.2)

        bci_arrow = Arrow(start=[bci_right_x + 0.15, bci_y, 0],
                          end=[bci_right_x + 0.85, bci_y, 0],
                          color=BLUE, buff=0.1, stroke_width=5)

        computer_center = [0.0, bci_y, 0.0]
        computer = VGroup(
            Rectangle(width=1.4, height=1.0, fill_color=BLUE, fill_opacity=0.6,
                      stroke_color=WHITE, stroke_width=2).move_to(computer_center),
            Rectangle(width=0.95, height=0.55, fill_color=BLACK,
                      fill_opacity=0.7, stroke_color=WHITE,
                      stroke_width=1.5).move_to(computer_center),
        )

        bar_specs = [("left hand", 0.75, BLUE),
                     ("right hand", 1.0, TEAL),
                     ("rest", 0.55, GREEN)]
        bar_items = VGroup()
        bar_rects = []
        for label_txt, val, col in bar_specs:
            bar_rect = Rectangle(width=val, height=0.26,
                                 fill_color=col, fill_opacity=0.55,
                                 stroke_color=WHITE, stroke_width=1.5)
            bar_text = Text(label_txt, font_size=14, color=WHITE)
            bar_text.next_to(bar_rect, LEFT, buff=0.12)
            item = VGroup(bar_rect, bar_text).scale_to_fit_width(3.0)
            bar_items.add(item)
            bar_rects.append(bar_rect)

        bar_items.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        bar_items.move_to([2.8, bci_y, 0])

        classification_title = Text("Classification", font_size=15, color=GREY)
        classification_title.next_to(bar_items, UP, buff=0.2)
        output_panel = VGroup(classification_title, bar_items)
        output_panel.scale_to_fit_width(3.8)
        output_panel.move_to([2.9, bci_y, 0])

        label4 = Text("Brain–computer interfaces", font_size=24, color=WHITE)
        label4.next_to(panel_rects[3], UP, buff=0.3)

        self.play(FadeIn(VGroup(bci_wave, bci_arrow, computer, output_panel)),
                  FadeIn(label4), run_time=max(0.05, 0.74))

        # ----------------------------------------------------------------
        # Beat 12: 38.78-41.86 -- time-varying features + bar updates
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.80))  # gap 37.98 -> 38.78

        time_feature_text = Text("time-varying features", font_size=20, color=WHITE)
        time_feature_text.next_to(bci_wave, DOWN, buff=0.4)

        self.play(FadeIn(time_feature_text), run_time=max(0.05, 0.35))
        self.play(time_feature_text.animate.set_color(YELLOW),
                  Indicate(bci_arrow, color=BLUE), run_time=max(0.05, 0.42))

        self.play(bar_rects[0].animate.set_fill(YELLOW, opacity=0.85),
                  bar_rects[0].animate.set_stroke(YELLOW, width=3),
                  run_time=max(0.05, 0.35))

        self.play(bar_rects[0].animate.set_fill(GREY, opacity=0.35),
                  bar_rects[0].animate.set_stroke(GREY, width=1.5),
                  bar_rects[1].animate.set_fill(YELLOW, opacity=0.85),
                  bar_rects[1].animate.set_stroke(YELLOW, width=3),
                  bci_wave.animate.stretch_to_fit_height(0.9),
                  run_time=max(0.05, 0.65))

        self.play(bar_rects[1].animate.set_fill(GREY, opacity=0.35),
                  bar_rects[1].animate.set_stroke(GREY, width=1.5),
                  bar_rects[2].animate.set_fill(YELLOW, opacity=0.85),
                  bar_rects[2].animate.set_stroke(YELLOW, width=3),
                  bci_wave.animate.stretch_to_fit_height(1.25).stretch_to_fit_width(3.0),
                  Indicate(bci_arrow, color=BLUE),
                  run_time=max(0.05, 0.65))

        self.wait(max(0.05, 0.66))  # fill to 41.86

        # ----------------------------------------------------------------
        # Beat 13: 42.34-44.26 -- classification and control applications
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.48))  # gap 41.86 -> 42.34

        class_word = Text("classification", font_size=21, color=WHITE)
        control_word = Text("control applications", font_size=21, color=WHITE)
        word_pair = VGroup(class_word, control_word).arrange(RIGHT, buff=0.28)
        word_pair.scale_to_fit_width(6.5)
        word_pair.next_to(output_panel, DOWN, buff=0.45)

        self.play(FadeIn(class_word), run_time=max(0.05, 0.35))
        self.play(class_word.animate.set_color(YELLOW), run_time=max(0.05, 0.30))

        cursor_arrow = Arrow(start=output_panel.get_right() + RIGHT * 0.2,
                             end=output_panel.get_right() + RIGHT * 0.8,
                             color=YELLOW, stroke_width=5)
        self.play(FadeIn(control_word),
                  cursor_arrow.animate.shift(LEFT * 0.5),
                  run_time=max(0.05, 0.40))
        self.play(control_word.animate.set_color(YELLOW),
                  cursor_arrow.animate.shift(RIGHT * 0.5),
                  run_time=max(0.05, 0.47))

        self.wait(max(0.05, 0.40))  # fill to 44.26

        # ----------------------------------------------------------------
        # Beat 14: 44.26-45.25 -- shrink panel 4, hold final grid
        # ----------------------------------------------------------------
        self.wait(max(0.05, 0.20))

        panel4_content = VGroup(bci_wave, bci_arrow, computer, output_panel,
                                time_feature_text, class_word, control_word,
                                cursor_arrow)

        slot4_left = slot_rects[3].get_left()[0]
        slot4_right = slot_rects[3].get_right()[0]
        slot4_cy = slot_rects[3].get_center()[1]

        cond4_wave = make_bci_wave(0.0,
                                   slot4_left + 0.25,
                                   slot_rects[3].get_center()[0] - 0.25,
                                   center_y=slot4_cy + 0.25,
                                   color=WHITE, stroke_width=1.2)
        cond4_arrow = Arrow(start=[slot_rects[3].get_center()[0] - 0.30,
                                   slot4_cy + 0.25, 0],
                            end=[slot_rects[3].get_center()[0] + 0.05,
                                 slot4_cy + 0.25, 0],
                            color=BLUE, buff=0.05, stroke_width=2)
        cond4_comp = Rectangle(width=0.32, height=0.26,
                               fill_color=BLUE, fill_opacity=0.7,
                               stroke_color=WHITE, stroke_width=1)
        cond4_comp.move_to([slot_rects[3].get_center()[0] + 0.45,
                            slot4_cy + 0.25, 0])

        cond4_bars = VGroup(*[Rectangle(width=0.16, height=0.08,
                                        fill_color=GREY, fill_opacity=0.7,
                                        stroke_color=WHITE, stroke_width=0.5)
                              for _ in range(3)]).arrange(DOWN, buff=0.08)
        cond4_bars.move_to([slot_rects[3].get_center()[0] + 0.95,
                            slot4_cy + 0.25, 0])

        cond4_label = Text("Brain–computer interfaces", font_size=9, color=WHITE)
        cond4_label.scale_to_fit_width(slot_rects[3].width * 0.9)
        cond4_label.move_to([slot_rects[3].get_center()[0],
                             slot_rects[3].get_bottom()[1] + 0.15, 0])

        cond4_group = VGroup(cond4_wave, cond4_arrow, cond4_comp,
                             cond4_bars, cond4_label)

        self.play(FadeOut(panel4_content), FadeOut(label4),
                  FadeIn(cond4_group),
                  Transform(panel_rects[3], slot_rects[3]),
                  run_time=max(0.05, 0.79))