ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Helper: build waveform points in local monitor coordinates
        def make_wave_points(drift_scale=1.0, rapid_scale=1.0, n=320):
            x = np.linspace(-2.2, 2.2, n)
            t = np.linspace(0, 7 * np.pi, n)
            drift = (
                0.60 * np.sin(0.70 * t)
                + 0.35 * np.sin(1.30 * t + 1.2)
                + 0.20 * np.sin(2.40 * t + 2.5)
            )
            rapid = (
                0.14 * np.sin(14 * t)
                + 0.08 * np.sin(23 * t + 0.5)
                + 0.05 * np.sin(37 * t + 1.2)
            )
            y = drift_scale * drift + rapid_scale * rapid
            return np.column_stack([x, y, np.zeros(n)])

        def make_wave_mobject(points, color=WHITE, stroke_width=2.5):
            wave = VMobject()
            wave.set_points_as_corners(points)
            wave.set_stroke(color=color, width=stroke_width)
            wave.set_fill(opacity=0)
            return wave

        # ------------------------------------------------------------
        # Previous scene's two-panel layout (simplified continuity)
        # ------------------------------------------------------------
        prev_left_rect = Rectangle(
            width=5.0, height=3.2, fill_color="#181C24", fill_opacity=0.9,
            stroke_color=GREY_B, stroke_width=1.5
        ).move_to(LEFT * 3.8 + UP * 0.2)
        prev_right_rect = Rectangle(
            width=5.0, height=3.2, fill_color="#181C24", fill_opacity=0.9,
            stroke_color=GREY_B, stroke_width=1.5
        ).move_to(RIGHT * 3.8 + UP * 0.2)
        prev_left_wave = make_wave_mobject(
            make_wave_points(1.0, 1.0), color=WHITE, stroke_width=2
        ).scale(0.75).move_to(prev_left_rect.get_center())
        prev_right_wave = make_wave_mobject(
            make_wave_points(0.0, 1.0), color=WHITE, stroke_width=2
        ).scale(0.75).move_to(prev_right_rect.get_center())
        previous_layout = VGroup(
            prev_left_rect, prev_right_rect, prev_left_wave, prev_right_wave
        )
        self.add(previous_layout)

        # ------------------------------------------------------------
        # New EEG recording setup
        # ------------------------------------------------------------
        eeg_label = Text("EEG", font_size=80, color=WHITE, weight=BOLD)
        eeg_label.to_edge(UP, buff=0.45)

        # Head silhouette
        head_shape = Circle(
            radius=1.4,
            color=WHITE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.85,
        ).move_to(np.array([-5.0, -0.5, 0]))
        neck = Rectangle(
            width=1.0, height=0.8,
            fill_color=BLUE, fill_opacity=0.85,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(head_shape.get_bottom() + DOWN * 0.20)
        head_group = VGroup(head_shape, neck)

        # Electrodes on the scalp
        head_center = head_shape.get_center()
        e1 = Dot(
            point=head_center + np.array([0.70, 0.95, 0]),
            radius=0.11, color=ORANGE, fill_opacity=1, stroke_width=0,
        )
        e2 = Dot(
            point=head_center + np.array([0.45, -0.55, 0]),
            radius=0.11, color=TEAL, fill_opacity=1, stroke_width=0,
        )
        e3 = Dot(
            point=head_center + np.array([-0.30, -1.05, 0]),
            radius=0.11, color=PURPLE, fill_opacity=1, stroke_width=0,
        )
        electrode_group = VGroup(e1, e2, e3)

        # Monitor screen
        screen = RoundedRectangle(
            width=4.8, height=3.0, corner_radius=0.12,
            fill_color="#181C24", fill_opacity=1,
            stroke_color=GREY_B, stroke_width=2,
        ).move_to(np.array([3.8, -0.4, 0]))
        stand_neck = Rectangle(
            width=0.30, height=0.55,
            fill_color=GREY_D, fill_opacity=1, stroke_width=0,
        ).move_to(screen.get_bottom() + DOWN * 0.28)
        stand_base = Rectangle(
            width=1.20, height=0.16,
            fill_color=GREY_D, fill_opacity=1, stroke_width=0,
        ).next_to(stand_neck, DOWN, buff=0)
        dashed_center = DashedLine(
            screen.get_left() + RIGHT * 0.15,
            screen.get_right() + LEFT * 0.15,
            color=GREY_B, dash_length=0.12, stroke_width=1.5,
        ).move_to(screen.get_center())
        dashed_center.set_opacity(0.25)
        monitor_group = VGroup(screen, stand_neck, stand_base, dashed_center)

        # Wires from electrodes to monitor
        wire1 = Line(e1.get_center(), screen.get_left() + UP * 0.90, color=GREY_B, stroke_width=2)
        wire2 = Line(e2.get_center(), screen.get_left() + UP * 0.10, color=GREY_B, stroke_width=2)
        wire3 = Line(e3.get_center(), screen.get_left() + DOWN * 0.50, color=GREY_B, stroke_width=2)
        wires_group = VGroup(wire1, wire2, wire3)

        new_setup = VGroup(eeg_label, head_group, electrode_group, wires_group, monitor_group)

        # ------------------------------------------------------------
        # Beat 1: fade from previous layout into EEG setup (0.00-1.92)
        # ------------------------------------------------------------
        self.play(
            FadeOut(previous_layout),
            FadeIn(new_setup),
            run_time=max(0.05, 1.92),
        )

        # ------------------------------------------------------------
        # Beat 2: ECG-like jagged waveform draws on monitor (1.92-3.78)
        # ------------------------------------------------------------
        wave_mobject = make_wave_mobject(
            make_wave_points(1.0, 1.0), color=WHITE, stroke_width=2.5
        ).move_to(screen.get_center())
        self.play(Create(wave_mobject), run_time=max(0.05, 1.86))

        # Gap 3.78 -> 4.54
        self.wait(max(0.05, 0.76))

        # ------------------------------------------------------------
        # Beat 3: high-pass filter box appears (4.54-7.88)
        # ------------------------------------------------------------
        filter_rect = RoundedRectangle(
            width=2.6, height=1.2, corner_radius=0.2,
            fill_color="#1B2B3A", fill_opacity=1,
            stroke_color=BLUE, stroke_width=2,
        ).move_to(np.array([-0.4, -0.4, 0]))
        filter_label = Text("High-pass filter", font_size=20, color=WHITE)
        filter_label.move_to(filter_rect.get_center())
        filter_label.scale_to_fit_width(filter_rect.width - 0.4)
        filter_box = VGroup(filter_rect, filter_label)
        filter_glow = SurroundingRectangle(
            filter_box, color=YELLOW, buff=0.10,
            stroke_width=4, fill_opacity=0,
        ).set_opacity(0.60)
        filter_group = VGroup(filter_glow, filter_box)

        self.play(GrowFromCenter(filter_group), run_time=max(0.05, 1.30))
        self.play(filter_glow.animate.set_stroke(width=8, opacity=0.95), run_time=max(0.05, 0.50))
        self.play(filter_glow.animate.set_stroke(width=4, opacity=0.60), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.04))

        # Gap 7.88 -> 9.16
        self.wait(max(0.05, 1.28))

        # ------------------------------------------------------------
        # Beat 4: EEG label pulses (9.16-11.34)
        # ------------------------------------------------------------
        self.play(
            Indicate(eeg_label, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 1.20),
        )
        self.wait(max(0.05, 0.98))

        # Gap 11.34 -> 11.68
        self.wait(max(0.05, 0.34))

        # ------------------------------------------------------------
        # Beat 5: slow baseline wander starts to diminish (11.68-13.74)
        # ------------------------------------------------------------
        wave_partial = make_wave_mobject(
            make_wave_points(0.25, 1.0), color=WHITE, stroke_width=2.5
        ).move_to(screen.get_center())
        self.play(Transform(wave_mobject, wave_partial), run_time=max(0.05, 2.06))

        # Gap 13.74 -> 14.10
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------
        # Beat 6: electrode movement caption + wobble (14.10-14.92)
        # ------------------------------------------------------------
        caption1_text = Text("electrode movement", font_size=18, color=WHITE)
        caption1_text.next_to(e1, RIGHT, buff=0.35).shift(UP * 0.15)
        caption1_arrow = Arrow(
            caption1_text.get_left(), e1.get_center(),
            color=GREY_B, buff=0.05, stroke_width=2,
            max_tip_length_to_length_ratio=0.18,
        )
        caption1_group = VGroup(caption1_text, caption1_arrow)

        self.play(FadeIn(caption1_group), run_time=max(0.05, 0.35))
        self.play(e1.animate.shift(UP * 0.05 + RIGHT * 0.03), run_time=max(0.05, 0.20))
        self.play(e1.animate.shift(DOWN * 0.05 + LEFT * 0.03), run_time=max(0.05, 0.20))
        self.wait(max(0.05, 0.07))

        # ------------------------------------------------------------
        # Beat 7: impedance change caption + electrode pulse (14.92-16.96)
        # ------------------------------------------------------------
        caption2_text = Text("impedance change", font_size=18, color=WHITE)
        caption2_text.next_to(e2, RIGHT, buff=0.35).shift(UP * 0.15)
        caption2_arrow = Arrow(
            caption2_text.get_left(), e2.get_center(),
            color=GREY_B, buff=0.05, stroke_width=2,
            max_tip_length_to_length_ratio=0.18,
        )
        caption2_group = VGroup(caption2_text, caption2_arrow)

        self.play(FadeOut(caption1_group), run_time=max(0.05, 0.40))
        self.play(FadeIn(caption2_group), run_time=max(0.05, 0.40))
        self.play(e2.animate.set_fill(RED, opacity=1), run_time=max(0.05, 0.35))
        self.play(e2.animate.set_fill(TEAL, opacity=1), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.54))

        # Gap 16.96 -> 17.54
        self.wait(max(0.05, 0.58))

        # ------------------------------------------------------------
        # Beat 8: filter pulses, baseline stabilizes (17.54-19.30)
        # ------------------------------------------------------------
        wave_flat = make_wave_mobject(
            make_wave_points(0.0, 1.0), color=WHITE, stroke_width=2.5
        ).move_to(screen.get_center())

        self.play(
            FadeOut(caption2_group),
            Indicate(filter_box, color=YELLOW, scale_factor=1.06),
            run_time=max(0.05, 0.80),
        )
        self.play(
            Transform(wave_mobject, wave_flat),
            dashed_center.animate.set_opacity(1).set_stroke(width=3, color=WHITE),
            run_time=max(0.05, 0.96),
        )

        # ------------------------------------------------------------
        # Beat 9: final stable-for-analysis label and fade out (19.30-20.88)
        # ------------------------------------------------------------
        stable_label = Text(
            "stable for analysis", font_size=26, color=GREEN, weight=BOLD
        ).next_to(monitor_group, DOWN, buff=0.35)

        self.play(FadeIn(stable_label), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.28))
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=max(0.05, 0.50))