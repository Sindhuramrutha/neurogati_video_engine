ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- black overlay for fade-in from black ---
        black_overlay = Rectangle(
            width=14, height=8,
            fill_color=BLACK, fill_opacity=1,
            stroke_width=0
        )
        black_overlay.move_to(ORIGIN)

        # --- left panel (Before Notch Filter) ---
        left_box = Rectangle(
            width=5.0, height=2.8,
            color=WHITE, stroke_width=2.5,
            fill_opacity=0
        )
        left_box.move_to(LEFT * 3.7 + UP * 1.0)

        left_label = Text(
            "Before Notch Filter",
            font_size=28, color=WHITE, weight="BOLD"
        )
        left_label.next_to(left_box, UP, buff=0.25)

        # --- right panel (After Notch Filter) — dashed rectangle ---
        right_box_start = LEFT * 3.7 + RIGHT * 7.4 + UP * 1.0  # mirror of left_box
        right_box = Rectangle(
            width=5.0, height=2.8,
            color=WHITE, stroke_width=2.5,
            fill_opacity=0
        )
        # Create dashed effect manually (no dash style param in Rectangle)
        right_box_dash = DashedVMobject(right_box, num_dashes=30, dashed_ratio=0.5)
        right_box_dash.move_to(right_box_start)

        right_label = Text(
            "After Notch Filter",
            font_size=28, color=WHITE, weight="BOLD"
        )
        right_label.next_to(right_box_dash, UP, buff=0.25)

        # --- contaminated EEG wave (left) ---
        x_min, x_max = 0, 2.5
        def contaminated_wave(x):
            return np.sin(2 * np.pi * 1.5 * x) + 0.22 * np.sin(2 * np.pi * 50 * x + 0.3)

        left_wave = FunctionGraph(
            contaminated_wave,
            x_range=[x_min, x_max],
            color=WHITE, stroke_width=2.5
        )
        left_wave.set_width(left_box.get_width() * 0.88)
        left_wave.move_to(left_box.get_center())

        # --- clean EEG wave (right) ---
        def clean_wave_func(x):
            return np.sin(2 * np.pi * 1.5 * x)

        right_wave_clean = FunctionGraph(
            clean_wave_func,
            x_range=[x_min, x_max],
            color=WHITE, stroke_width=2.5
        )
        right_wave_clean.set_width(right_box_dash.get_width() * 0.88)
        right_wave_clean.move_to(right_box_dash.get_center())
        right_wave_clean.set_opacity(0)  # hidden until beat 4

        # --- frequency spectrum helper ---
        def make_spectrum():
            axes = Axes(
                x_range=[0, 100, 10],
                y_range=[0, 1.2, 0.2],
                x_length=4.0,
                y_length=2.4,
                axis_config={"color": GREY, "stroke_width": 1.5},
                tips=False,
            )
            bg_curve = axes.plot(
                lambda x: 0.18 + 0.04 * np.sin(0.2 * x) + 0.05 * np.cos(0.15 * x),
                x_range=[0, 100],
                color=GREY_B, stroke_width=2.5
            )
            baseline_50 = 0.18 + 0.04 * np.sin(0.2 * 50) + 0.05 * np.cos(0.15 * 50)
            peak_line = Line(
                axes.c2p(50, baseline_50),
                axes.c2p(50, 1.05),
                color=RED, stroke_width=7
            )
            freq_label = Text("Frequency (Hz)", font_size=22, color=GREY)
            freq_label.next_to(axes.x_axis, DOWN, buff=0.15)
            return axes, bg_curve, peak_line, freq_label

        # left spectrum
        left_axes, left_bg, left_peak, left_freq_label = make_spectrum()
        left_spec_group = VGroup(left_axes, left_bg, left_peak, left_freq_label)
        left_spec_group.next_to(left_box, DOWN, buff=0.35)
        # small 50 Hz label under the peak
        left_peak_label_50 = Text("50 Hz", font_size=20, color=RED, weight="BOLD")
        left_peak_label_50.next_to(left_peak, DOWN, buff=0.05)

        # right spectrum (identical, hidden until beat 4)
        right_axes, right_bg, right_peak, right_freq_label = make_spectrum()
        right_spec_group = VGroup(right_axes, right_bg, right_peak, right_freq_label)
        right_spec_group.next_to(right_box_dash, DOWN, buff=0.35)
        right_spec_group.set_opacity(0)
        right_peak_label_50 = Text("50 Hz", font_size=20, color=RED, weight="BOLD")
        right_peak_label_50.next_to(right_peak, DOWN, buff=0.05)
        right_peak_label_50.set_opacity(0)

        # --- notch filter icon ---
        notch_line = VMobject(color=YELLOW, stroke_width=5, fill_opacity=0)
        # Build a horizontal line with V-shaped notch
        notch_p1 = np.array([-0.6, 0, 0])
        notch_p2 = np.array([-0.08, 0, 0])
        notch_p3 = np.array([0, -0.25, 0])
        notch_p4 = np.array([0.08, 0, 0])
        notch_p5 = np.array([0.6, 0, 0])
        notch_line.set_points_as_corners([notch_p1, notch_p2, notch_p3, notch_p4, notch_p5])
        notch_icon = VGroup(notch_line)
        notch_icon.scale_to_fit_width(1.4)

        # start position: vertical dividing line between panels
        dividing_x = (left_box.get_right()[0] + right_box_dash.get_left()[0]) / 2
        notch_icon.move_to(np.array([dividing_x, left_box.get_center()[1], 0]))
        notch_icon.set_opacity(0)

        # ============================================================
        # BEAT 1: 0.00–1.20 – fade from black, all elements visible
        # ============================================================
        initial_scene = VGroup(
            left_box, left_label, left_wave,
            left_spec_group, left_peak_label_50,
            right_box_dash, right_label,
        )
        self.add(initial_scene, black_overlay)
        self.play(FadeOut(black_overlay), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.20 - self.renderer.time))

        # ============================================================
        # BEAT 2: 3.18–7.80 – highlight 50 Hz ripple, pulse spike, label
        # ============================================================
        self.wait(max(0.05, 3.18 - self.renderer.time))

        # red semi-transparent overlay on left wave
        red_overlay = left_wave.copy()
        red_overlay.set_color(RED)
        red_overlay.set_opacity(0.45)
        red_overlay.set_stroke(width=8)
        self.play(GrowFromCenter(red_overlay), run_time=max(0.05, 0.8))

        # pulse the 50 Hz spike twice
        for _ in range(2):
            self.play(Indicate(left_peak, color=YELLOW, scale_factor=1.3), run_time=max(0.05, 0.5))
            self.wait(max(0.05, 0.2))

        # label "50 Hz power line noise"
        noise_label = Text(
            "50 Hz power line noise",
            font_size=24, color=YELLOW, weight="BOLD"
        )
        noise_label.next_to(left_peak.get_top(), UP, buff=0.25)
        self.play(Write(noise_label), run_time=max(0.05, 0.8))
        # keep label visible as per brief (annotations remain visible)
        self.wait(max(0.05, 7.80 - self.renderer.time))

        # ============================================================
        # BEAT 3: 7.80–13.84 – trace slow wave (blue) and ripple (red)
        #          outlines + labels with connectors
        # ============================================================
        beat3_duration = 13.84 - 7.80  # 6.04 s
        per_step = beat3_duration / 6  # ~1.0 s each for 6 sub-steps

        # blue outline of slow component
        slow_func = lambda x: np.sin(2 * np.pi * 1.5 * x)
        slow_trace = FunctionGraph(
            slow_func,
            x_range=[x_min, x_max],
            color=BLUE, stroke_width=5
        )
        slow_trace.set_width(left_wave.get_width())
        slow_trace.move_to(left_box.get_center())
        self.play(Write(slow_trace), run_time=max(0.05, per_step * 1.2))

        # label "Neural signal" + blue connector
        neural_label = Text(
            "Neural signal",
            font_size=26, color=BLUE, weight="BOLD"
        )
        neural_label.next_to(left_box, UP, buff=0.15).align_to(left_box, LEFT).shift(UP * 0.3)
        connector_neural = Arrow(
            neural_label.get_bottom() + DOWN * 0.1,
            slow_trace.point_from_proportion(0.25),
            color=BLUE, stroke_width=3, buff=0.1
        )
        self.play(Write(neural_label), GrowArrow(connector_neural), run_time=max(0.05, per_step * 1.2))

        # red outline of 50 Hz ripple (replace overlay)
        self.play(FadeOut(red_overlay), run_time=max(0.05, per_step * 0.6))
        ripple_func = lambda x: 0.22 * np.sin(2 * np.pi * 50 * x + 0.3)
        ripple_trace = FunctionGraph(
            ripple_func,
            x_range=[x_min, x_max],
            color=RED, stroke_width=5
        )
        ripple_trace.set_width(left_wave.get_width())
        ripple_trace.move_to(left_box.get_center())
        self.play(Write(ripple_trace), run_time=max(0.05, per_step * 1.2))

        # label "50 Hz electrical component" + red connector
        electrical_label = Text(
            "50 Hz electrical component",
            font_size=22, color=RED, weight="BOLD"
        )
        electrical_label.next_to(ripple_trace, DOWN, buff=0.5)
        connector_elec = Arrow(
            electrical_label.get_top() + UP * 0.1,
            ripple_trace.point_from_proportion(0.7),
            color=RED, stroke_width=3, buff=0.1
        )
        self.play(Write(electrical_label), GrowArrow(connector_elec), run_time=max(0.05, per_step * 1.2))

        self.wait(max(0.05, 13.84 - self.renderer.time))

        # ============================================================
        # BEAT 4: 13.84–16.86 – notch icon slides right, right panel
        #          fills with clean waveform and spectrum, spike collapses
        # ============================================================
        # Fade in notch icon at dividing line
        self.play(FadeIn(notch_icon), run_time=max(0.05, 0.3))

        # Show right clean wave and spectrum
        right_wave_clean.set_opacity(1)
        right_spec_group.set_opacity(1)
        right_peak_label_50.set_opacity(1)

        # notch target: slide to right edge by ~16.0
        notch_target = np.array([right_box_dash.get_right()[0] + 0.5, notch_icon.get_center()[1], 0])

        # collapse right peak to baseline
        baseline_50_right_y = 0.18 + 0.04 * np.sin(0.2 * 50) + 0.05 * np.cos(0.15 * 50)
        baseline_50_right = right_axes.c2p(50, baseline_50_right_y)
        collapsed_line = Line(baseline_50_right, baseline_50_right, color=RED, stroke_width=0)

        # Animate notch slide + right contents appear + peak collapse
        self.play(
            notch_icon.animate.move_to(notch_target),
            FadeIn(right_wave_clean, shift=DOWN * 0.2),
            FadeIn(right_spec_group, shift=UP * 0.2),
            FadeIn(right_peak_label_50, shift=UP * 0.2),
            run_time=max(0.05, 2.2)
        )
        # Collapse spike
        self.play(Transform(right_peak, collapsed_line), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 16.86 - self.renderer.time))

        # ============================================================
        # BEAT 5: 16.86–20.76 – narrow attenuated band on right spectrum
        # ============================================================
        beat5_duration = 20.76 - 16.86

        # semi-transparent vertical band straddling 50 Hz
        left_band_coord = right_axes.c2p(48, 0)[0]
        right_band_coord = right_axes.c2p(52, 0)[0]
        band_width = right_band_coord - left_band_coord
        band_height = right_axes.get_height()
        band_center_y = right_axes.get_center()[1]
        band_rect = Rectangle(
            width=band_width, height=band_height,
            fill_color=YELLOW, fill_opacity=0.2, stroke_width=0
        )
        band_rect.move_to(np.array([(left_band_coord + right_band_coord) / 2, band_center_y, 0]))

        self.play(FadeIn(band_rect), run_time=max(0.05, beat5_duration * 0.3))

        # label "Attenuated 50 Hz band"
        atten_label = Text(
            "Attenuated 50 Hz band",
            font_size=20, color=YELLOW, weight="BOLD"
        )
        atten_label.next_to(band_rect, DOWN, buff=0.25)
        self.play(FadeIn(atten_label), run_time=max(0.05, beat5_duration * 0.3))

        # brighten band briefly
        self.play(
            band_rect.animate.set_fill(opacity=0.5),
            run_time=max(0.05, beat5_duration * 0.2)
        )
        self.play(
            band_rect.animate.set_fill(opacity=0.2),
            run_time=max(0.05, beat5_duration * 0.2)
        )
        self.wait(max(0.05, 20.76 - self.renderer.time))

        # ============================================================
        # BEAT 6: 20.76–25.10 – highlight unchanged frequencies outside band
        # ============================================================
        beat6_duration = 25.10 - 20.76

        # left unchanged region 0–45 Hz
        left_uch_width = right_axes.c2p(45, 0)[0] - right_axes.c2p(0, 0)[0]
        left_unchanged = Rectangle(
            width=left_uch_width, height=band_height,
            fill_color=YELLOW, fill_opacity=0.18, stroke_width=0
        )
        left_unchanged.move_to(np.array([right_axes.c2p(22.5, 0)[0], band_center_y, 0]))

        # right unchanged region 55–100 Hz
        right_uch_width = right_axes.c2p(100, 0)[0] - right_axes.c2p(55, 0)[0]
        right_unchanged = Rectangle(
            width=right_uch_width, height=band_height,
            fill_color=YELLOW, fill_opacity=0.18, stroke_width=0
        )
        rt_center_x = (right_axes.c2p(55, 0)[0] + right_axes.c2p(100, 0)[0]) / 2
        right_unchanged.move_to(np.array([rt_center_x, band_center_y, 0]))

        self.play(
            FadeIn(left_unchanged), FadeIn(right_unchanged),
            run_time=max(0.05, beat6_duration * 0.15)
        )

        # label "Unchanged frequencies"
        unchange_label = Text(
            "Unchanged frequencies",
            font_size=22, color=YELLOW, weight="BOLD"
        )
        unchange_label.next_to(right_unchanged, UP, buff=0.15)
        self.play(FadeIn(unchange_label), run_time=max(0.05, beat6_duration * 0.15))
        # fade after 2 seconds
        self.wait(max(0.05, beat6_duration * 0.45))
        self.play(FadeOut(unchange_label), run_time=max(0.05, beat6_duration * 0.15))
        self.wait(max(0.05, 25.10 - self.renderer.time))

        # ============================================================
        # BEAT 7: 25.10–32.20 – remove red ripple overlay (already gone),
        #          right clean wave gets blue outline, green checkmark
        # ============================================================
        beat7_duration = 32.20 - 25.10

        # The red ripple trace (ripple_trace) still visible from beat 3 — pulse and remove it
        self.play(Indicate(ripple_trace, color=RED, scale_factor=1.2), run_time=max(0.05, beat7_duration * 0.1))
        self.play(
            FadeOut(ripple_trace),
            FadeOut(electrical_label),
            FadeOut(connector_elec),
            run_time=max(0.05, beat7_duration * 0.15)
        )

        # blue outline on right clean wave
        blue_right_trace = FunctionGraph(
            clean_wave_func,
            x_range=[x_min, x_max],
            color=BLUE, stroke_width=5
        )
        blue_right_trace.set_width(right_wave_clean.get_width())
        blue_right_trace.move_to(right_box_dash.get_center())
        self.play(Write(blue_right_trace), run_time=max(0.05, beat7_duration * 0.15))

        # green checkmark near "After Notch Filter" label
        check_icon = SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN)
        check_icon.scale_to_fit_height(0.6)
        check_icon.next_to(right_label, RIGHT, buff=0.3)
        check_text = Text(
            "Clear neural signal",
            font_size=22, color=GREEN, weight="BOLD"
        )
        check_text.next_to(check_icon, DOWN, buff=0.1)
        self.play(
            SpinInFromNothing(check_icon, angle=PI / 2),
            Write(check_text),
            run_time=max(0.05, beat7_duration * 0.2)
        )

        self.wait(max(0.05, 32.20 - self.renderer.time))

        # ============================================================
        # BEAT 8: 32.20–36.38 – zoom into right spectrum 40–65 Hz,
        #          text box appears
        # ============================================================
        # target center: 52.5 Hz on right_axes
        target_x = right_axes.c2p(52.5, 0)[0]
        target_y = right_axes.get_center()[1]
        target_center = np.array([target_x, target_y, 0])

        # frame 25 Hz width (40–65) tightly — 25/100 of 4.0 → 1.0 units; scale ~0.35
        self.play(
            self.camera.frame.animate.scale(0.35).move_to(target_center),
            run_time=max(0.05, 3.0)
        )

        # text box after zoom settles
        outside_text = Text(
            "Frequencies outside\nrejected band unchanged",
            font_size=24, color=WHITE, weight="NORMAL",
            line_spacing=0.8,
        )
        outside_text.to_corner(UR, buff=0.5)
        box_bg = SurroundingRectangle(
            outside_text, color=YELLOW, buff=0.15,
            fill_opacity=0.15, stroke_width=2
        )
        text_box = VGroup(box_bg, outside_text)
        self.play(FadeIn(text_box), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 36.38 - self.renderer.time))

        # ============================================================
        # BEAT 9: 36.38–37.58 – hold steady, then fade to black
        # ============================================================
        self.wait(max(0.05, 37.38 - self.renderer.time))

        # final fade to black
        black_out = Rectangle(
            width=20, height=12,
            fill_color=BLACK, fill_opacity=1,
            stroke_width=0
        )
        black_out.move_to(self.camera.frame.get_center())
        self.play(FadeIn(black_out), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 37.58 - self.renderer.time))