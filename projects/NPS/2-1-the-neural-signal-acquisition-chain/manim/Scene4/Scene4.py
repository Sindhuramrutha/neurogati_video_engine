ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def make_head_profile(color=WHITE, fill_opacity=0.3, stroke_width=3):
            head = Ellipse(
                width=1.4, height=1.1,
                stroke_color=color, stroke_width=stroke_width,
                fill_color=color, fill_opacity=fill_opacity,
            )
            nose = Polygon(
                np.array([-0.72, 0.15, 0]),
                np.array([-1.08, 0.0, 0]),
                np.array([-0.72, -0.15, 0]),
                stroke_color=color, stroke_width=stroke_width,
                fill_color=color, fill_opacity=fill_opacity,
            )
            return VGroup(head, nose)

        # Previous scene placeholder
        prev_head = make_head_profile(color=GREY, fill_opacity=0.0).scale(1.15).move_to(UP * 0.4)
        prev_caption = Text("no activity = no signal", font_size=28, color=GREY).next_to(prev_head, DOWN, buff=0.35)
        self.add(prev_head, prev_caption)

        # Four empty panels in 2x2 grid
        panel_w, panel_h = 5.0, 1.7
        p1 = Rectangle(width=panel_w, height=panel_h, stroke_color=GREY_B, stroke_width=2.5,
                       fill_color=BLACK, fill_opacity=0).move_to(np.array([-2.8, 1.25, 0]))
        p2 = Rectangle(width=panel_w, height=panel_h, stroke_color=GREY_B, stroke_width=2.5,
                       fill_color=BLACK, fill_opacity=0).move_to(np.array([2.8, 1.25, 0]))
        p3 = Rectangle(width=panel_w, height=panel_h, stroke_color=GREY_B, stroke_width=2.5,
                       fill_color=BLACK, fill_opacity=0).move_to(np.array([-2.8, -1.25, 0]))
        p4 = Rectangle(width=panel_w, height=panel_h, stroke_color=GREY_B, stroke_width=2.5,
                       fill_color=BLACK, fill_opacity=0).move_to(np.array([2.8, -1.25, 0]))
        panels = VGroup(p1, p2, p3, p4)

        # Beat 1: fade previous scene, bring in empty panels
        self.play(FadeOut(prev_head, prev_caption), FadeIn(panels), run_time=max(0.05, 1.86))
        self.wait(max(0.05, 0.88))

        # Build all future content, hidden until used
        # EEG: head profile with scalp electrodes
        eeg_head = make_head_profile(fill_opacity=0.35)
        eeg_dots = VGroup()
        for deg in [35, 70, 105, 140]:
            th = np.deg2rad(deg)
            dot = Dot(point=np.array([0.7 * np.cos(th), 0.55 * np.sin(th), 0]),
                      radius=0.055, color=YELLOW, fill_opacity=1)
            eeg_dots.add(dot)
        eeg_content = VGroup(eeg_head, eeg_dots)
        eeg_content.scale_to_fit_height(1.2).scale_to_fit_width(4.0).move_to(p1.get_center())
        label_eeg = Text("EEG: scalp electrodes", font_size=24, color=WHITE)
        label_eeg.scale_to_fit_width(4.6).next_to(p1, DOWN, buff=0.12)

        # EMG: arm cross-section with surface pad and needle
        arm_ellipse = Ellipse(width=2.6, height=1.5, fill_color=PINK, fill_opacity=0.9,
                              stroke_color=WHITE, stroke_width=2).move_to(ORIGIN)
        surface_pad = Rectangle(width=0.3, height=0.14, fill_color=YELLOW, fill_opacity=1,
                                stroke_width=0).move_to(np.array([0, 0.75, 0]))
        needle = Line(start=np.array([0, 0.62, 0]), end=np.array([0.35, -0.45, 0]),
                      color=YELLOW, stroke_width=3)
        emg_content = VGroup(arm_ellipse, surface_pad, needle)
        emg_content.scale_to_fit_height(1.25).scale_to_fit_width(4.2).move_to(p2.get_center())
        label_emg = Text("EMG: surface or needle electrodes", font_size=24, color=WHITE)
        label_emg.scale_to_fit_width(4.6).next_to(p2, DOWN, buff=0.12)

        # ECoG: filled cortical surface with rectangular contact grid
        t_vals = np.linspace(-1.6, 1.6, 60)
        upper_points = [np.array([t, 0.25 * np.sin(3 * t) + 0.25, 0]) for t in t_vals]
        lower_points = [np.array([t, -0.35, 0]) for t in reversed(t_vals)]
        cortical_surface = Polygon(*upper_points, *lower_points,
                                   stroke_color=WHITE, stroke_width=2)
        cortical_surface.set_fill(PURPLE, opacity=0.6)
        ecog_grid = VGroup()
        for row_off, row_idx in zip([0.0, 0.16], range(2)):
            for cx in np.linspace(-1.3, 1.3, 4):
                cy = 0.25 * np.sin(3 * cx) + 0.30 + row_off
                rect = Rectangle(width=0.36, height=0.10, fill_color=YELLOW, fill_opacity=1,
                                 stroke_color=GREEN, stroke_width=1).move_to(np.array([cx, cy, 0]))
                ecog_grid.add(rect)
        ecog_content = VGroup(cortical_surface, ecog_grid)
        ecog_content.scale_to_fit_height(1.2).scale_to_fit_width(4.2).move_to(p3.get_center())
        label_ecog = Text("ECoG: cortical grid", font_size=24, color=WHITE)
        label_ecog.scale_to_fit_width(4.6).next_to(p3, DOWN, buff=0.12)

        # MEG: head with helmet and loop-shaped magnetic sensors
        meg_head = make_head_profile(fill_opacity=0.35).move_to(ORIGIN)
        helmet = Arc(radius=0.78, start_angle=0, angle=PI, color=WHITE, stroke_width=5)
        meg_sensors = VGroup()
        for deg in [30, 65, 100, 135]:
            th = np.deg2rad(deg)
            r = 0.62
            pos = np.array([r * np.cos(th), r * np.sin(th), 0])
            loop = Circle(radius=0.075, color=YELLOW, stroke_width=2.5).move_to(pos)
            loop.set_fill(YELLOW, opacity=0.45)
            meg_sensors.add(loop)
        meg_content = VGroup(meg_head, helmet, meg_sensors)
        meg_content.scale_to_fit_height(1.3).scale_to_fit_width(4.0).move_to(p4.get_center())
        label_meg = Text("MEG: magnetic sensors", font_size=24, color=WHITE)
        label_meg.scale_to_fit_width(4.6).next_to(p4, DOWN, buff=0.12)

        # Beat 2: generic sensor with wire pulse
        pad = Rectangle(width=0.65, height=0.30, fill_color=ORANGE, fill_opacity=1,
                        stroke_width=0).move_to(np.array([-1.6, 2.9, 0]))
        wire_end = np.array([1.6, 2.9, 0])
        wire = Line(start=pad.get_right(), end=wire_end, color=GREY_B, stroke_width=4)
        terminal = Dot(wire_end, radius=0.06, color=GREEN)
        sensor_group = VGroup(pad, wire, terminal)
        sensor_label = Text("Electrode / Sensor", font_size=30, color=YELLOW)
        sensor_label.next_to(sensor_group, DOWN, buff=0.20)
        caption_sensor = Text(
            "Detects the biological signal and transfers it to the recording system.",
            font_size=22, color=GREY_B,
        ).scale_to_fit_width(13).to_edge(DOWN, buff=0.30)

        self.play(GrowFromCenter(sensor_group), Write(sensor_label),
                  FadeIn(caption_sensor), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 0.15))

        pulse_start = np.array([-1.25, 2.9, 0])
        pulse_end = np.array([1.55, 2.9, 0])
        for _ in range(4):
            pulse = Dot(pulse_start, radius=0.06, color=YELLOW, fill_opacity=1)
            self.play(FadeIn(pulse, scale=0.4), run_time=max(0.05, 0.12))
            self.play(pulse.animate.move_to(pulse_end), run_time=max(0.05, 0.50))
            self.play(FadeOut(pulse), run_time=max(0.05, 0.08))
            self.wait(max(0.05, 0.15))
        self.wait(max(0.05, 0.17))
        self.wait(max(0.05, 0.64))

        # Beat 3: clear sensor, brighten panel outlines sequentially
        self.play(FadeOut(sensor_group), FadeOut(sensor_label),
                  FadeOut(caption_sensor), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.10))
        for i, panel in enumerate(panels):
            self.play(
                panel.animate.set_stroke(color=WHITE, width=4).set_fill(WHITE, opacity=0.07),
                run_time=max(0.05, 0.25),
            )
            if i < 3:
                self.wait(max(0.05, 0.10))
        self.wait(max(0.05, 0.07))
        self.wait(max(0.05, 0.92))

        # Beat 4: EEG panel
        self.play(
            p1.animate.set_fill(BLUE, opacity=0.22).set_stroke(BLUE, width=4),
            GrowFromCenter(eeg_content),
            FadeIn(label_eeg),
            run_time=max(0.05, 1.60),
        )
        self.wait(max(0.05, 1.84))
        self.wait(max(0.05, 0.74))

        # Beat 5: dim EEG, show EMG
        self.play(
            p1.animate.set_fill(GREY_B, opacity=0.08).set_stroke(GREY_B, width=2),
            eeg_content.animate.set_opacity(0.30),
            label_eeg.animate.set_opacity(0.30),
            run_time=max(0.05, 0.75),
        )
        self.wait(max(0.05, 0.10))
        self.play(
            p2.animate.set_fill(TEAL, opacity=0.22).set_stroke(TEAL, width=4),
            GrowFromCenter(emg_content),
            FadeIn(label_emg),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 0.23))
        self.wait(max(0.05, 0.94))

        # Beat 6: dim EMG, show ECoG
        self.play(
            p2.animate.set_fill(GREY_B, opacity=0.08).set_stroke(GREY_B, width=2),
            emg_content.animate.set_opacity(0.30),
            label_emg.animate.set_opacity(0.30),
            run_time=max(0.05, 0.75),
        )
        self.wait(max(0.05, 0.10))
        self.play(
            p3.animate.set_fill(GREEN, opacity=0.22).set_stroke(GREEN, width=4),
            GrowFromCenter(ecog_content),
            FadeIn(label_ecog),
            run_time=max(0.05, 1.40),
        )
        self.wait(max(0.05, 1.49))
        self.wait(max(0.05, 0.84))

        # Beat 7: dim ECoG, show MEG
        self.play(
            p3.animate.set_fill(GREY_B, opacity=0.08).set_stroke(GREY_B, width=2),
            ecog_content.animate.set_opacity(0.30),
            label_ecog.animate.set_opacity(0.30),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.10))
        self.play(
            p4.animate.set_fill(PURPLE, opacity=0.22).set_stroke(PURPLE, width=4),
            GrowFromCenter(meg_content),
            FadeIn(label_meg),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 0.22))
        self.wait(max(0.05, 0.94))

        # Beat 8: all four fully visible side by side
        self.play(
            p1.animate.set_fill(BLUE, opacity=0.25).set_stroke(BLUE, width=4),
            p2.animate.set_fill(TEAL, opacity=0.25).set_stroke(TEAL, width=4),
            p3.animate.set_fill(GREEN, opacity=0.25).set_stroke(GREEN, width=4),
            p4.animate.set_fill(PURPLE, opacity=0.25).set_stroke(PURPLE, width=4),
            eeg_content.animate.set_opacity(1.0),
            emg_content.animate.set_opacity(1.0),
            ecog_content.animate.set_opacity(1.0),
            meg_content.animate.set_opacity(1.0),
            label_eeg.animate.set_opacity(1.0),
            label_emg.animate.set_opacity(1.0),
            label_ecog.animate.set_opacity(1.0),
            label_meg.animate.set_opacity(1.0),
            run_time=max(0.05, 1.40),
        )
        self.wait(max(0.05, 0.54))
        self.wait(max(0.05, 0.62))

        # Beat 9: unify with arrow and common label
        arrow = Arrow(
            start=np.array([-4.8, -2.7, 0]),
            end=np.array([4.8, -2.7, 0]),
            stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.08,
            color=YELLOW,
        )
        unified_label = Text("detect physiological activity", font_size=30, color=YELLOW)
        unified_label.scale_to_fit_width(4.5).next_to(arrow, DOWN, buff=0.15)
        self.play(Create(arrow), Write(unified_label), run_time=max(0.05, 1.60))
        self.wait(max(0.05, 0.78))
        self.wait(max(0.05, 0.76))

        # Beat 10: brighten label, pulse arrow, final caption
        final_caption = Text("detecting physiological activity", font_size=22, color=YELLOW)
        final_caption.scale_to_fit_width(4.2).next_to(unified_label, DOWN, buff=0.10)

        self.play(unified_label.animate.set_color(GOLD).scale(1.08), run_time=max(0.05, 0.35))
        bright_pulse = Dot(arrow.get_start(), radius=0.08, color=WHITE, fill_opacity=1)
        self.play(FadeIn(bright_pulse, scale=0.4), run_time=max(0.05, 0.15))
        self.play(bright_pulse.animate.move_to(arrow.get_end()), run_time=max(0.05, 0.55))
        self.play(FadeOut(bright_pulse), FadeIn(final_caption), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.33))

        # Beat 11: hold static to end
        self.wait(max(0.05, 0.89))