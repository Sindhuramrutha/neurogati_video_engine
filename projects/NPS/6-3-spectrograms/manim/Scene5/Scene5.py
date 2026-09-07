ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene5(Scene):
    def make_bg_wave(self, phase):
        waves = VGroup()
        x_min, x_max = -9, 9
        specs = [
            (BLUE, -3.3, 0.20, 0.9),
            (TEAL, -1.9, 0.26, 1.15),
            (PURPLE, -0.5, 0.30, 1.4),
            (BLUE, 0.9, 0.28, 1.65),
            (TEAL, 2.3, 0.24, 1.9),
            (PURPLE, 3.7, 0.20, 2.15),
        ]
        for color, y, amp, freq in specs:
            def func(t, y=y, amp=amp, freq=freq, phase=phase):
                x = x_min + (x_max - x_min) * t
                yy = y + amp * np.sin(2 * np.pi * freq * t + phase)
                return np.array([x, yy, 0])
            wave = ParametricFunction(
                func,
                t_range=[0, 1],
                color=color,
                stroke_width=1.4,
                stroke_opacity=0.14,
            )
            wave.set_z_index(0)
            waves.add(wave)
        return waves

    def make_spec_area(self, panel):
        spec_w = panel.width - 0.9
        spec_h = 1.5
        spec_rect = Rectangle(
            width=spec_w,
            height=spec_h,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=1.0,
        )
        spec_rect.move_to(panel.get_center() + DOWN * 0.02)
        spec_rect.set_z_index(3)

        left_x = spec_rect.get_left()[0] + 0.14
        right_x = spec_rect.get_right()[0] - 0.05
        bottom_y = spec_rect.get_bottom()[1] + 0.12
        top_y = spec_rect.get_top()[1] - 0.10

        v_axis = Line(
            np.array([left_x, bottom_y, 0]),
            np.array([left_x, top_y, 0]),
            color=GREY_B,
            stroke_width=1.0,
            stroke_opacity=0.65,
        )
        h_axis = Line(
            np.array([left_x, bottom_y, 0]),
            np.array([right_x, bottom_y, 0]),
            color=GREY_B,
            stroke_width=1.0,
            stroke_opacity=0.65,
        )
        time_label = Text("Time", font_size=14, color=GREY_B)
        time_label.next_to(h_axis, DOWN, buff=0.06)

        for mob in [v_axis, h_axis, time_label]:
            mob.set_z_index(5)

        group = VGroup(spec_rect, v_axis, h_axis, time_label)
        bounds = {
            "x0": left_x + 0.02,
            "x1": right_x - 0.02,
            "y0": bottom_y + 0.04,
            "y1": top_y - 0.02,
        }
        return group, spec_rect, bounds

    def make_horizontal_band_group(self, bounds, f_start, f_end, colors, opacities):
        x0, x1 = bounds["x0"], bounds["x1"]
        y0, y1 = bounds["y0"], bounds["y1"]
        n = len(colors)
        ys = np.linspace(y0 + f_start * (y1 - y0), y0 + f_end * (y1 - y0), n + 1)
        group = VGroup()
        for i, color in enumerate(colors):
            rect = Rectangle(
                width=x1 - x0,
                height=ys[i + 1] - ys[i],
                fill_color=color,
                fill_opacity=opacities[i],
                stroke_width=0,
            )
            rect.move_to(np.array([(x0 + x1) / 2, (ys[i] + ys[i + 1]) / 2, 0]))
            rect.set_z_index(4)
            group.add(rect)
        return group

    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Build the 2x2 empty panel grid ---
        panel_w, panel_h = 5.6, 2.8
        gap_x, gap_y = 0.8, 0.8
        positions = {
            "eeg": np.array([-(panel_w + gap_x) / 2, (panel_h + gap_y) / 2, 0]),
            "emg": np.array([(panel_w + gap_x) / 2, (panel_h + gap_y) / 2, 0]),
            "bci": np.array([-(panel_w + gap_x) / 2, -(panel_h + gap_y) / 2, 0]),
            "er": np.array([(panel_w + gap_x) / 2, -(panel_h + gap_y) / 2, 0]),
        }

        panels = {}
        for key, center in positions.items():
            panel = RoundedRectangle(
                width=panel_w,
                height=panel_h,
                corner_radius=0.14,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_color=GREY_B,
                stroke_width=1.5,
            )
            panel.move_to(center)
            panel.set_z_index(1)
            panels[key] = panel

        grid = VGroup(*panels.values())

        # Labels, placed later per panel
        labels = {}
        for key, text in [
            ("eeg", "EEG Analysis"),
            ("emg", "EMG Analysis"),
            ("bci", "Brain–Computer Interfaces"),
            ("er", "Event-Related Studies"),
        ]:
            label = Text(text, font_size=20, color=WHITE, weight=BOLD)
            label.scale_to_fit_width(panels[key].width - 0.6)
            label.move_to(panels[key].get_top() + DOWN * 0.32)
            labels[key] = label

        # Spectrogram areas
        spec_groups, spec_rects, bounds = {}, {}, {}
        for key in positions:
            sg, sr, bd = self.make_spec_area(panels[key])
            spec_groups[key] = sg
            spec_rects[key] = sr
            bounds[key] = bd

        # --- Prebuild panel contents ---
        eeg_band_group = self.make_horizontal_band_group(
            bounds["eeg"], 0.05, 0.36, [MAROON, ORANGE, GOLD], [0.25, 0.35, 0.35]
        )

        emg_b = bounds["emg"]
        emg_base = Rectangle(
            width=emg_b["x1"] - emg_b["x0"],
            height=emg_b["y1"] - emg_b["y0"],
            fill_color=TEAL,
            fill_opacity=0.06,
            stroke_width=0,
        )
        emg_base.move_to(
            np.array([(emg_b["x0"] + emg_b["x1"]) / 2, (emg_b["y0"] + emg_b["y1"]) / 2, 0])
        )
        emg_base.set_z_index(4)

        emg_band_top = emg_b["y1"] - 0.03
        emg_band = Rectangle(
            width=emg_b["x1"] - emg_b["x0"],
            height=0.09,
            fill_color=TEAL,
            fill_opacity=0.30,
            stroke_width=0,
        )
        emg_band.move_to(
            np.array([(emg_b["x0"] + emg_b["x1"]) / 2, emg_band_top - 0.045, 0])
        )
        emg_band.set_z_index(4)

        bci_b = bounds["bci"]
        bci_band = Rectangle(
            width=bci_b["x1"] - bci_b["x0"],
            height=0.07 * (bci_b["y1"] - bci_b["y0"]),
            fill_color=GOLD,
            fill_opacity=0.80,
            stroke_width=0,
        )
        bci_band.move_to(
            np.array([
                (bci_b["x0"] + bci_b["x1"]) / 2,
                bci_b["y0"] + 0.55 * (bci_b["y1"] - bci_b["y0"]),
                0,
            ])
        )
        bci_band.set_z_index(4)

        er_b = bounds["er"]
        er_baseline = Rectangle(
            width=er_b["x1"] - er_b["x0"],
            height=er_b["y1"] - er_b["y0"],
            fill_color=PURPLE,
            fill_opacity=0.06,
            stroke_width=0,
        )
        er_baseline.move_to(
            np.array([(er_b["x0"] + er_b["x1"]) / 2, (er_b["y0"] + er_b["y1"]) / 2, 0])
        )
        er_baseline.set_z_index(4)

        stim_x = er_b["x0"] + 0.24 * (er_b["x1"] - er_b["x0"])
        stim_line = Line(
            np.array([stim_x, er_b["y0"] + 0.06, 0]),
            np.array([stim_x, er_b["y1"] - 0.14, 0]),
            color=YELLOW,
            stroke_width=2.0,
        )
        stim_line.set_z_index(6)
        stim_label = Text("Stimulus", font_size=13, color=YELLOW)
        stim_label.next_to(np.array([stim_x, er_b["y1"] - 0.14, 0]), UP, buff=0.04)

        burst_x0 = stim_x + 0.06 * (er_b["x1"] - er_b["x0"])
        burst_x1 = stim_x + 0.36 * (er_b["x1"] - er_b["x0"])
        burst_f0, burst_f1 = 0.28, 0.68
        burst_colors = [PINK, PURPLE, ORANGE]
        burst_ys = np.linspace(
            er_b["y0"] + burst_f0 * (er_b["y1"] - er_b["y0"]),
            er_b["y0"] + burst_f1 * (er_b["y1"] - er_b["y0"]),
            len(burst_colors) + 1,
        )
        er_burst = VGroup()
        for i, color in enumerate(burst_colors):
            rect = Rectangle(
                width=burst_x1 - burst_x0,
                height=burst_ys[i + 1] - burst_ys[i],
                fill_color=color,
                fill_opacity=0.75,
                stroke_width=0,
            )
            rect.move_to(
                np.array([
                    (burst_x0 + burst_x1) / 2,
                    (burst_ys[i] + burst_ys[i + 1]) / 2,
                    0,
                ])
            )
            rect.set_z_index(4)
            er_burst.add(rect)

        # Background wave tracker
        phase_tracker = ValueTracker(0)
        bg_waves = always_redraw(lambda: self.make_bg_wave(phase_tracker.get_value()))

        # --- Beat 1: 0.00 - 3.24 ---
        self.wait(max(0.05, 0.40))
        self.play(FadeIn(grid), run_time=max(0.05, 2.84))

        # --- Beat 2: 3.24 - 6.92 ---
        self.add(bg_waves)
        self.play(phase_tracker.animate.set_value(2 * PI), run_time=max(0.05, 3.68))

        # Gap 6.92 - 7.68
        self.wait(max(0.05, 0.76))

        # --- Beat 3: 7.68 - 10.28 (Top-left EEG panel) ---
        eeg_panel = panels["eeg"]
        self.play(
            eeg_panel.animate.set_stroke(WHITE, width=2.5).set_fill(BLUE, opacity=0.07),
            run_time=max(0.05, 0.5),
        )
        self.play(FadeIn(labels["eeg"]), run_time=max(0.05, 0.8))
        self.play(FadeIn(spec_groups["eeg"]), run_time=max(0.05, 1.3))

        # Gap 10.28 - 11.04
        self.wait(max(0.05, 0.76))

        # --- Beat 4: 11.04 - 14.62 (EEG slow rhythmic bands) ---
        self.play(FadeIn(eeg_band_group), run_time=max(0.05, 0.58))
        for _ in range(3):
            self.play(eeg_band_group.animate.set_opacity(0.55), run_time=max(0.05, 0.5))
            self.play(eeg_band_group.animate.set_opacity(0.28), run_time=max(0.05, 0.5))

        # Gap 14.62 - 14.88
        self.wait(max(0.05, 0.26))

        # --- Beat 5: 14.88 - 16.68 (EEG cognitive tasks / sleep) ---
        self.play(
            eeg_band_group.animate.shift(UP * 0.12),
            eeg_band_group.animate.set_opacity(0.65),
            run_time=max(0.05, 0.45),
        )
        self.play(eeg_band_group.animate.set_opacity(0.35), run_time=max(0.05, 0.45))
        self.play(
            eeg_band_group.animate.shift(DOWN * 0.22),
            eeg_band_group.animate.set_opacity(0.15),
            run_time=max(0.05, 0.9),
        )

        # Gap 16.68 - 17.26
        self.wait(max(0.05, 0.58))

        # --- Beat 6: 17.26 - 18.12 (EEG sensory stimulation) ---
        self.play(eeg_band_group.animate.set_opacity(0.95), run_time=max(0.05, 0.43))
        self.play(eeg_band_group.animate.set_opacity(0.20), run_time=max(0.05, 0.43))

        # Gap 18.12 - 19.18
        self.wait(max(0.05, 1.06))

        # --- Beat 7: 19.18 - 21.28 (Top-right EMG panel) ---
        emg_panel = panels["emg"]
        self.play(
            emg_panel.animate.set_stroke(WHITE, width=2.5).set_fill(BLUE, opacity=0.07),
            run_time=max(0.05, 0.4),
        )
        self.play(FadeIn(labels["emg"]), run_time=max(0.05, 0.7))
        self.play(FadeIn(spec_groups["emg"]), FadeIn(emg_base), run_time=max(0.05, 1.0))

        # Gap 21.28 - 21.98
        self.wait(max(0.05, 0.70))

        # --- Beat 8: 21.98 - 24.66 (EMG broadband high-frequency energy) ---
        self.play(FadeIn(emg_band), run_time=max(0.05, 0.3))
        self.play(
            emg_band.animate.stretch_to_fit_height(
                0.50 * (emg_b["y1"] - emg_b["y0"]), about_edge=UP
            ),
            emg_band.animate.set_opacity(0.62),
            run_time=max(0.05, 2.38),
        )

        # --- Beat 9: 24.66 - 26.12 (EMG movement, then fatigue) ---
        self.play(
            emg_band.animate.stretch_to_fit_height(
                0.92 * (emg_b["y1"] - emg_b["y0"]), about_edge=UP
            ),
            emg_band.animate.set_opacity(0.90),
            run_time=max(0.05, 0.73),
        )
        self.play(emg_band.animate.set_opacity(0.35), run_time=max(0.05, 0.25))
        self.play(emg_band.animate.set_opacity(0.55), run_time=max(0.05, 0.15))
        self.play(emg_band.animate.set_opacity(0.30), run_time=max(0.05, 0.15))
        self.play(emg_band.animate.set_opacity(0.45), run_time=max(0.05, 0.18))

        # Gap 26.12 - 26.90
        self.wait(max(0.05, 0.78))

        # --- Beat 10: 26.90 - 28.80 (Bottom-left BCI panel) ---
        bci_panel = panels["bci"]
        self.play(
            bci_panel.animate.set_stroke(WHITE, width=2.5).set_fill(BLUE, opacity=0.07),
            run_time=max(0.05, 0.4),
        )
        self.play(FadeIn(labels["bci"]), run_time=max(0.05, 0.7))
        self.play(FadeIn(spec_groups["bci"]), run_time=max(0.05, 0.8))

        # Gap 28.80 - 29.42
        self.wait(max(0.05, 0.62))

        # --- Beat 11: 29.42 - 32.68 (BCI narrow band pulses) ---
        self.play(FadeIn(bci_band), run_time=max(0.05, 0.26))
        for _ in range(3):
            self.play(bci_band.animate.set_opacity(0.85), run_time=max(0.05, 0.5))
            self.play(bci_band.animate.set_opacity(0.45), run_time=max(0.05, 0.5))

        # --- Beat 12: 32.68 - 35.48 (BCI highlight + feature label) ---
        bci_highlight = SurroundingRectangle(
            bci_band, color=YELLOW, buff=0.10, stroke_width=2
        )
        bci_arrow = Arrow(
            start=bci_band.get_right() + RIGHT * 0.45,
            end=bci_band.get_right() + RIGHT * 0.05,
            color=YELLOW,
            stroke_width=2,
            buff=0.05,
        )
        features_label = Text("Features", font_size=16, color=YELLOW)
        features_label.next_to(bci_arrow, UP, buff=0.10)

        self.play(Create(bci_highlight), run_time=max(0.05, 0.6))
        self.play(FadeIn(bci_arrow), FadeIn(features_label), run_time=max(0.05, 0.5))
        self.play(bci_band.animate.set_opacity(0.95), run_time=max(0.05, 0.4))
        self.play(bci_band.animate.set_opacity(0.60), run_time=max(0.05, 0.35))
        self.play(bci_band.animate.set_opacity(0.85), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.60))

        # Gap 35.48 - 36.62
        self.wait(max(0.05, 1.14))

        # --- Beat 13: 36.62 - 38.00 (Bottom-right Event-Related panel) ---
        er_panel = panels["er"]
        self.play(
            er_panel.animate.set_stroke(WHITE, width=2.5).set_fill(BLUE, opacity=0.07),
            run_time=max(0.05, 0.35),
        )
        self.play(FadeIn(labels["er"]), run_time=max(0.05, 0.5))
        self.play(FadeIn(spec_groups["er"]), run_time=max(0.05, 0.53))

        # Gap 38.00 - 38.40
        self.wait(max(0.05, 0.40))

        # --- Beat 14: 38.40 - 41.42 (Stimulus line on quiet baseline) ---
        self.play(FadeIn(er_baseline), run_time=max(0.05, 1.0))
        self.play(Create(stim_line), run_time=max(0.05, 1.0))
        self.play(FadeIn(stim_label), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.52))

        # --- Beat 15: 41.42 - 44.06 (Post-stimulus burst) ---
        self.play(FadeIn(er_burst), run_time=max(0.05, 0.5))
        self.play(er_burst.animate.set_opacity(0.10), run_time=max(0.05, 2.14))

        # --- Beat 16: 44.06 - 45.58 (Grid holds, sequential pulses) ---
        pulse_order = ["eeg", "emg", "bci", "er"]
        for key in pulse_order:
            self.play(spec_rects[key].animate.set_stroke(YELLOW, width=3), run_time=max(0.05, 0.19))
            self.play(spec_rects[key].animate.set_stroke(GREY_B, width=1.0), run_time=max(0.05, 0.19))