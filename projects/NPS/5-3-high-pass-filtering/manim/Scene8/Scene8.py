ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Shared x-axis for the monitor trace
        x_wave = np.linspace(-2.3, 2.3, 560)

        def make_wave_points(low_scale=1.0, high_scale=0.0, phase_shift=0.0):
            x = x_wave
            t = 2.6 * x + 6.0 + phase_shift

            # Broad, rolling low-frequency waves
            slow = (
                0.50 * np.sin(0.50 * t)
                + 0.28 * np.sin(0.95 * t + 1.4)
                + 0.16 * np.sin(1.70 * t + 2.0)
            )

            # Tight, separated high-frequency bursts
            centers = [-1.7, -0.35, 0.95]
            widths = [0.30, 0.34, 0.28]
            freqs = [22.0, 26.0, 20.0]
            amps = [0.85, 1.0, 0.8]

            high = np.zeros_like(x)
            for cx, w, f, a in zip(centers, widths, freqs, amps):
                high += (
                    a
                    * np.exp(-((x - cx) ** 2) / (2 * w * w))
                    * np.sin(f * x + 1.2)
                )

            y = 0.8 * (low_scale * slow + high_scale * high)
            return np.column_stack([x, y, np.zeros_like(x)])

        def make_wave_mobject(points, color=WHITE, stroke_width=2.5):
            wave = VMobject()
            wave.set_points_as_corners(points)
            wave.set_stroke(color=color, width=stroke_width)
            wave.set_fill(opacity=0)
            return wave

        # ------------------------------------------------------------
        # Bicep and electrodes
        # ------------------------------------------------------------
        arm_main = RoundedRectangle(
            width=1.05,
            height=3.0,
            corner_radius=0.5,
            fill_color=PINK,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(np.array([-4.8, 0.0, 0]))

        arm_bulge = Ellipse(
            width=1.75,
            height=1.95,
            fill_color=PINK,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(arm_main.get_center() + LEFT * 0.25 + DOWN * 0.1)

        e1 = Dot(
            point=np.array([
                arm_bulge.get_right()[0] - 0.02,
                arm_bulge.get_center()[1] + 0.45,
                0,
            ]),
            radius=0.09,
            color=ORANGE,
            fill_opacity=1,
            stroke_width=0,
        )
        e2 = Dot(
            point=np.array([
                arm_bulge.get_right()[0] - 0.02,
                arm_bulge.get_center()[1] - 0.45,
                0,
            ]),
            radius=0.09,
            color=TEAL,
            fill_opacity=1,
            stroke_width=0,
        )

        arm_group = VGroup(arm_main, arm_bulge, e1, e2)

        # ------------------------------------------------------------
        # Monitor
        # ------------------------------------------------------------
        screen = RoundedRectangle(
            width=5.2,
            height=3.0,
            corner_radius=0.12,
            fill_color="#181C24",
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).move_to(np.array([3.8, 0.0, 0]))

        center_line = DashedLine(
            screen.get_left() + RIGHT * 0.18,
            screen.get_right() + LEFT * 0.18,
            color=GREY_B,
            dash_length=0.10,
            stroke_width=1.4,
        ).move_to(screen.get_center())
        center_line.set_opacity(0.20)

        monitor_group = VGroup(screen, center_line)

        # ------------------------------------------------------------
        # EMG title
        # ------------------------------------------------------------
        emg_label = Text("EMG", font_size=80, color=WHITE, weight=BOLD)
        emg_label.to_edge(UP, buff=0.45)

        # ------------------------------------------------------------
        # High-pass filter box (created now, faded in at beat 5)
        # ------------------------------------------------------------
        filter_rect = RoundedRectangle(
            width=2.7,
            height=1.4,
            corner_radius=0.2,
            fill_color="#1B2B3A",
            fill_opacity=1,
            stroke_color=YELLOW,
            stroke_width=3,
        )
        filter_label = Text("High-pass filter", font_size=22, color=WHITE)
        filter_label.scale_to_fit_width(filter_rect.width - 0.5)
        filter_label.move_to(filter_rect.get_center())
        filter_box = VGroup(filter_rect, filter_label)

        filter_glow = SurroundingRectangle(
            filter_box,
            color=YELLOW,
            buff=0.12,
            stroke_width=5,
            fill_opacity=0,
        ).set_opacity(0.7)

        filter_group = VGroup(filter_glow, filter_box)
        filter_group.move_to(np.array([-0.9, 0.0, 0]))

        # ------------------------------------------------------------
        # Wires that continuously attach electrodes -> filter/screen
        # ------------------------------------------------------------
        filter_active = False

        def build_wires():
            wire_color = GREY_B
            stroke_w = 2
            if not filter_active:
                return VGroup(
                    Line(
                        e1.get_center(),
                        screen.get_left() + UP * 0.4,
                        color=wire_color,
                        stroke_width=stroke_w,
                    ),
                    Line(
                        e2.get_center(),
                        screen.get_left() + DOWN * 0.4,
                        color=wire_color,
                        stroke_width=stroke_w,
                    ),
                )
            else:
                fl = filter_rect.get_left()
                fr = filter_rect.get_right()
                sl = screen.get_left()
                return VGroup(
                    Line(
                        e1.get_center(),
                        fl + UP * 0.30,
                        color=wire_color,
                        stroke_width=stroke_w,
                    ),
                    Line(
                        fr + UP * 0.30,
                        sl + UP * 0.4,
                        color=wire_color,
                        stroke_width=stroke_w,
                    ),
                    Line(
                        e2.get_center(),
                        fl + DOWN * 0.30,
                        color=wire_color,
                        stroke_width=stroke_w,
                    ),
                    Line(
                        fr + DOWN * 0.30,
                        sl + DOWN * 0.4,
                        color=wire_color,
                        stroke_width=stroke_w,
                    ),
                )

        self.wire_system = always_redraw(build_wires)

        # ------------------------------------------------------------
        # Setup with everything visible at scene start
        # ------------------------------------------------------------
        setup_group = VGroup(
            arm_group,
            monitor_group,
            emg_label,
            self.wire_system,
        )

        # ------------------------------------------------------------
        # Pre-build waveform targets
        # ------------------------------------------------------------
        wave_slow = make_wave_mobject(
            make_wave_points(low_scale=1.0, high_scale=0.0)
        ).move_to(screen.get_center())
        wave_artifact = make_wave_mobject(
            make_wave_points(low_scale=1.0, high_scale=0.45)
        ).move_to(screen.get_center())
        wave_artifact_b = make_wave_mobject(
            make_wave_points(low_scale=1.0, high_scale=0.45, phase_shift=0.4)
        ).move_to(screen.get_center())
        wave_artifact_c = make_wave_mobject(
            make_wave_points(low_scale=1.0, high_scale=0.45, phase_shift=0.9)
        ).move_to(screen.get_center())
        wave_flatten = make_wave_mobject(
            make_wave_points(low_scale=0.35, high_scale=0.7)
        ).move_to(screen.get_center())
        wave_high = make_wave_mobject(
            make_wave_points(low_scale=0.0, high_scale=1.15)
        ).move_to(screen.get_center())

        # ------------------------------------------------------------
        # Beat 1: 0.00-1.46 -- fade in EMG setup, monitor dark
        # ------------------------------------------------------------
        self.play(FadeIn(setup_group), run_time=max(0.05, 1.46))

        # ------------------------------------------------------------
        # Beat 2: 1.46-2.78 -- slow waveform draws across monitor
        # ------------------------------------------------------------
        wave_mobject = wave_slow.copy()
        self.play(Create(wave_mobject), run_time=max(0.05, 1.32))

        # ------------------------------------------------------------
        # Beat 3: 2.78-4.52 -- slow waves + partially buried spikes
        # ------------------------------------------------------------
        artifact_points = make_wave_points(low_scale=1.0, high_scale=0.45)
        idx_artifact = np.argmin(np.abs(x_wave - (-1.1)))
        artifact_target = screen.get_center() + artifact_points[idx_artifact]

        artifact_label = Text("motion artifact", font_size=22, color=YELLOW)
        artifact_label.next_to(screen, UP, buff=0.25).shift(LEFT * 1.55)

        artifact_arrow = Arrow(
            artifact_label.get_bottom() + DOWN * 0.12,
            artifact_target,
            color=YELLOW,
            stroke_width=1.8,
            buff=0.05,
            max_tip_length_to_length_ratio=0.18,
        )
        artifact_group = VGroup(artifact_label, artifact_arrow)

        self.play(
            Transform(wave_mobject, wave_artifact),
            FadeIn(artifact_group, run_time=max(0.05, 0.9)),
            run_time=max(0.05, 1.74),
        )

        # ------------------------------------------------------------
        # Beat 4: 4.52-6.08 -- slow waves drift, bicep wobbles subtly
        # ------------------------------------------------------------
        self.play(
            Transform(wave_mobject, wave_artifact_b),
            arm_group.animate.shift(LEFT * 0.05 + UP * 0.04),
            run_time=max(0.05, 0.78),
        )
        self.play(
            Transform(wave_mobject, wave_artifact_c),
            arm_group.animate.shift(RIGHT * 0.07 + DOWN * 0.05),
            run_time=max(0.05, 0.78),
        )

        # ------------------------------------------------------------
        # Gap: 6.08-6.96 -- hold while narration pauses
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.88))

        # ------------------------------------------------------------
        # Beat 5: 6.96-8.32 -- high-pass filter box appears in wire path
        # ------------------------------------------------------------
        filter_active = True
        self.play(FadeIn(filter_group), run_time=max(0.05, 1.36))

        # ------------------------------------------------------------
        # Beat 6: 8.32-10.30 -- slow waves flatten, artifact label fades
        # ------------------------------------------------------------
        self.play(
            Transform(wave_mobject, wave_flatten),
            FadeOut(artifact_group, run_time=max(0.05, 0.9)),
            run_time=max(0.05, 0.99),
        )
        self.play(Transform(wave_mobject, wave_high), run_time=max(0.05, 0.99))

        # ------------------------------------------------------------
        # Beat 7: 10.30-12.20 -- sharp high-frequency bursts become clear
        # ------------------------------------------------------------
        high_points = make_wave_points(low_scale=0.0, high_scale=1.15)
        idx_muscle = np.argmin(np.abs(x_wave - (-0.35)))
        muscle_target = screen.get_center() + high_points[idx_muscle]

        muscle_label = Text("muscle activity", font_size=22, color=YELLOW)
        muscle_label.next_to(screen, UP, buff=0.25).shift(RIGHT * 0.4)

        muscle_arrow = Arrow(
            muscle_label.get_bottom() + DOWN * 0.12,
            muscle_target,
            color=YELLOW,
            stroke_width=1.8,
            buff=0.05,
            max_tip_length_to_length_ratio=0.18,
        )
        muscle_group = VGroup(muscle_label, muscle_arrow)

        self.play(FadeIn(muscle_group), run_time=max(0.05, 1.1))
        self.play(
            Indicate(wave_mobject, color=WHITE, scale_factor=1.04),
            run_time=max(0.05, 0.8),
        )

        # ------------------------------------------------------------
        # Gap: 12.20-12.48 -- brief hold before final emphasis
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.28))

        # ------------------------------------------------------------
        # Beat 8: 12.48-14.68 -- clean activity, filter pulse, EMG brightens
        # ------------------------------------------------------------
        self.play(
            Indicate(filter_box, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.9),
        )
        self.play(
            emg_label.animate.set_color(YELLOW),
            wave_mobject.animate.set_stroke(width=3.2, color=WHITE),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.6))

        # ------------------------------------------------------------
        # Beat 9: 14.68-15.55 -- final hold, then gentle fade out
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.37))
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=max(0.05, 0.5))