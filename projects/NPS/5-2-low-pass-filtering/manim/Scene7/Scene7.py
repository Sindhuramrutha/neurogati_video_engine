ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------------- signal parameters ----------------
        length = 300
        peak_index = 150
        peak_height = 3.0
        osc_amplitude = 0.2
        num_osc = 6

        moderate_window = 5
        heavy_window = 30

        top_y_center = 1.8
        top_y_range = 1.6
        bottom_y_center = -1.5
        bottom_y_range = 1.2

        cutoff_high_y = 2.6
        cutoff_low_y = 0.6

        # ---------------- raw signal ----------------
        t = np.linspace(0, 4 * np.pi, length)
        y_raw = (
            osc_amplitude * np.sin(num_osc * t)
            + peak_height * np.exp(-((np.arange(length) - peak_index) ** 2) / (2 * 5 ** 2))
        )

        # ---------------- trackers ----------------
        smoothness_tracker = ValueTracker(0)   # drives only the top waveform
        cutoff_tracker = ValueTracker(0)       # drives the dashed cutoff line

        # ---------------- helper functions ----------------
        def get_filtered(smoothness):
            window = int(moderate_window + (heavy_window - moderate_window) * smoothness)
            window = max(1, min(window, length - 1))
            window_arr = np.ones(window) / window
            return np.convolve(y_raw, window_arr, mode="same")

        def get_top_points(smoothness):
            y_filt = get_filtered(smoothness)
            scale_factor = top_y_range / max(np.max(np.abs(y_filt)), 1e-6)
            y_scaled = y_filt * scale_factor + top_y_center
            x_mapped = np.interp(t, (t[0], t[-1]), (-6.5, 6.5))
            return np.column_stack([x_mapped, y_scaled, np.zeros(length)])

        def get_bottom_points():
            window = heavy_window
            window_arr = np.ones(window) / window
            y_heavy = np.convolve(y_raw, window_arr, mode="same")
            scale_factor = bottom_y_range / max(np.max(np.abs(y_heavy)), 1e-6)
            y_scaled = y_heavy * scale_factor + bottom_y_center
            x_mapped = np.interp(t, (t[0], t[-1]), (-6.5, 6.5))
            return np.column_stack([x_mapped, y_scaled, np.zeros(length)])

        def get_cutoff_y(smooth):
            return cutoff_high_y - (cutoff_high_y - cutoff_low_y) * smooth

        # ---------------- top waveform ----------------
        top_wave = VMobject(color=BLUE, stroke_width=3)
        top_wave.set_points_as_corners(get_top_points(0))
        top_wave.add_updater(
            lambda mob: mob.set_points_as_corners(
                get_top_points(smoothness_tracker.get_value())
            )
        )

        # ---------------- bottom waveform ----------------
        bottom_wave_points = get_bottom_points()
        bottom_wave = VMobject(color=TEAL, stroke_width=3)
        bottom_wave.set_points_as_corners(bottom_wave_points)

        # ---------------- labels ----------------
        moderate_label = Text("Moderate filtering", font_size=22, color=BLUE)
        moderate_label.move_to(np.array([-5.3, 3.3, 0]))

        bottom_label = Text("Excessive filtering", font_size=22, color=TEAL)
        bottom_label.move_to(np.array([-5.3, 0.0, 0]))

        # ---------------- peak highlights ----------------
        raw_max = np.max(np.abs(y_raw))
        peak_x_mid = np.interp(t[peak_index], (t[0], t[-1]), (-6.5, 6.5))
        peak_y_max = y_raw[peak_index] * (top_y_range / raw_max) + top_y_center

        peak_circle = Circle(radius=0.25, color=YELLOW, stroke_width=3, fill_opacity=0)
        peak_circle.move_to(np.array([peak_x_mid, peak_y_max, 0]))

        highlight_ring = Circle(radius=0.35, color=YELLOW, stroke_width=5, fill_opacity=0)
        highlight_ring.move_to(np.array([peak_x_mid, peak_y_max, 0]))

        # ============================================================
        # BEAT 1: 0.00 - 2.50
        # ============================================================
        self.play(Write(moderate_label), run_time=max(0.05, 0.5))
        self.play(Create(top_wave), run_time=max(0.05, 1.0))
        self.play(
            peak_circle.animate.scale(1.5).set_stroke(width=6),
            rate_func=there_and_back,
            run_time=max(0.05, 1.0),
        )
        self.remove(peak_circle)

        # gap 0.46
        self.wait(max(0.05, 0.46))

        # ============================================================
        # BEAT 2: 2.96 - 4.00
        # ============================================================
        apply_label = Text("Apply carefully", font_size=28, color=YELLOW)
        apply_label.to_edge(UP, buff=0.3)
        self.play(Write(apply_label), run_time=max(0.05, 0.5))
        self.play(top_wave.animate.set_stroke(width=6), run_time=max(0.05, 0.54))

        # gap 0.96
        self.wait(max(0.05, 0.96))

        # ============================================================
        # BEAT 3: 4.96 - 7.04
        # ============================================================
        cutoff_line = DashedLine(
            LEFT * 6.5 + UP * cutoff_high_y,
            RIGHT * 6.5 + UP * cutoff_high_y,
            color=ORANGE,
            dash_length=0.15,
            stroke_width=3,
        )
        cutoff_line.add_updater(
            lambda mob: mob.put_start_and_end_on(
                np.array([-6.5, get_cutoff_y(cutoff_tracker.get_value()), 0]),
                np.array([6.5, get_cutoff_y(cutoff_tracker.get_value()), 0]),
            )
        )

        # Label and arrow placed above-left of the line so they remain visible.
        cutoff_label = Text("Cutoff frequency", font_size=20, color=ORANGE)
        cutoff_label.move_to(np.array([-5.0, cutoff_high_y + 0.6, 0]))
        cutoff_arrow = Arrow(
            start=np.array([-5.0, cutoff_high_y + 0.35, 0]),
            end=np.array([-5.2, cutoff_high_y + 0.05, 0]),
            color=ORANGE,
            buff=0.05,
        )

        def update_cutoff_label(mob):
            y = get_cutoff_y(cutoff_tracker.get_value())
            mob.move_to(np.array([-5.0, y + 0.6, 0]))

        def update_cutoff_arrow(mob):
            y = get_cutoff_y(cutoff_tracker.get_value())
            mob.put_start_and_end_on(
                np.array([-5.0, y + 0.32, 0]),
                np.array([-5.2, y + 0.05, 0]),
            )

        cutoff_label.add_updater(update_cutoff_label)
        cutoff_arrow.add_updater(update_cutoff_arrow)

        self.play(
            Write(cutoff_line),
            Write(cutoff_label),
            GrowArrow(cutoff_arrow),
            run_time=max(0.05, 0.5),
        )
        self.play(
            smoothness_tracker.animate.set_value(1),
            cutoff_tracker.animate.set_value(1),
            run_time=max(0.05, 1.58),
        )

        # gap 0.28
        self.wait(max(0.05, 0.28))

        # ============================================================
        # BEAT 4: 7.32 - 9.98
        # ============================================================
        red_overlay = Rectangle(
            width=13,
            height=0.5,
            fill_color=RED,
            fill_opacity=0.25,
            stroke_width=0,
        )
        red_overlay.move_to(np.array([0, top_y_center + top_y_range * 0.8, 0]))
        lost_label = Text("Physiological information lost", font_size=20, color=RED)
        lost_label.next_to(red_overlay, UP, buff=0.1)

        self.play(
            smoothness_tracker.animate.set_value(2),
            cutoff_tracker.animate.set_value(2),
            FadeIn(red_overlay, shift=UP * 0.2),
            Write(lost_label),
            run_time=max(0.05, 2.66),
        )

        # --------------- restore after beat 4 ---------------
        self.play(
            smoothness_tracker.animate.set_value(0),
            cutoff_tracker.animate.set_value(0),
            FadeOut(red_overlay),
            FadeOut(lost_label),
            FadeOut(apply_label),
            run_time=max(0.05, 0.88),
        )

        # ============================================================
        # BEAT 5: 10.86 - 14.08
        # ============================================================
        arrow_down = Arrow(
            start=np.array([5.5, top_y_center - top_y_range, 0]),
            end=np.array([5.5, bottom_y_center + bottom_y_range, 0]),
            color=WHITE,
            stroke_width=3,
            buff=0.1,
        )

        self.play(Write(bottom_wave), run_time=max(0.05, 1.0))
        self.play(Write(bottom_label), run_time=max(0.05, 0.8))
        self.play(GrowArrow(arrow_down), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.62))

        # fade out the generic contrast arrow before the specific red arrow
        self.play(FadeOut(arrow_down), run_time=max(0.05, 0.48))

        # ============================================================
        # BEAT 6: 14.56 - 16.86
        # ============================================================
        red_arrow_down = Arrow(
            start=highlight_ring.get_bottom(),
            end=np.array([peak_x_mid, bottom_y_center, 0]),
            color=RED,
            stroke_width=4,
            buff=0.1,
        )
        x_mark = Text("✗", font_size=32, color=RED)
        x_mark.next_to(red_arrow_down.get_end(), DOWN, buff=0.1)

        self.play(
            Create(highlight_ring),
            GrowArrow(red_arrow_down),
            Write(x_mark),
            run_time=max(0.05, 1.5),
        )
        self.wait(max(0.05, 0.8))

        # gap 0.82
        self.wait(max(0.05, 0.82))

        # ============================================================
        # BEAT 7: 17.68 - 23.06
        # ============================================================
        loop_length = 100
        loop_t = np.linspace(0, 4 * np.pi, loop_length)
        loop_y_raw = (
            osc_amplitude * np.sin(num_osc * loop_t)
            + peak_height * np.exp(-((np.arange(loop_length) - 50) ** 2) / (2 * 5 ** 2))
        )

        def loop_filtered(smooth):
            w = int(moderate_window + (heavy_window - moderate_window) * smooth)
            w = max(1, min(w, loop_length - 1))
            w_arr = np.ones(w) / w
            return np.convolve(loop_y_raw, w_arr, mode="same")

        def loop_points(smooth):
            y_rec = loop_filtered(smooth)
            scale = 0.8 / max(np.max(np.abs(y_rec)), 1e-6)
            y_scaled = y_rec * scale
            x_mapped = np.interp(loop_t, (loop_t[0], loop_t[-1]), (-1.3, 1.3))
            return np.column_stack([x_mapped, y_scaled, np.zeros(loop_length)])

        loop_box = Rectangle(
            width=3,
            height=2,
            color=WHITE,
            stroke_width=1,
            fill_opacity=0.1,
            fill_color=BLACK,
        )
        loop_box.to_corner(DL, buff=0.5)
        loop_center = loop_box.get_center()

        def loop_points_abs(smooth):
            return loop_points(smooth) + loop_center

        loop_smoothness = ValueTracker(1)
        loop_wave = VMobject(color=YELLOW, stroke_width=2)
        loop_wave.set_points_as_corners(loop_points_abs(1))
        loop_wave.add_updater(
            lambda mob: mob.set_points_as_corners(
                loop_points_abs(loop_smoothness.get_value())
            )
        )

        loop_cutoff_text = Text("Cutoff ↑", font_size=18, color=YELLOW)
        loop_cutoff_text.next_to(loop_box, UP, buff=0.1)

        choose_text = Text(
            "Choose based on signal characteristics.", font_size=22, color=WHITE
        )
        choose_text.next_to(loop_box, RIGHT, buff=0.5)

        self.play(FadeIn(loop_box), Write(loop_wave), run_time=max(0.05, 1.0))
        self.play(
            loop_smoothness.animate.set_value(0),
            Write(loop_cutoff_text),
            run_time=max(0.05, 2.0),
        )
        self.play(Write(choose_text), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.38))

        # remove the loop before the warning note arrives
        self.play(
            FadeOut(loop_box),
            FadeOut(loop_wave),
            FadeOut(loop_cutoff_text),
            FadeOut(choose_text),
            run_time=max(0.05, 0.96),
        )

        # ============================================================
        # BEAT 8: 24.02 - 27.32
        # ============================================================
        warning_triangle = Polygon(
            [-0.5, -0.4, 0],
            [0.5, -0.4, 0],
            [0, 0.5, 0],
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
        )
        warning_excla = Text("!", font_size=28, color=BLACK, weight=BOLD)
        warning_excla.move_to(warning_triangle.get_center() + UP * 0.05)
        warning_icon = VGroup(warning_triangle, warning_excla)
        warning_icon.to_corner(UR, buff=0.5)

        warning_text1 = Text(
            "Removes high-frequency components,", font_size=22, color=WHITE
        )
        warning_text2 = Text("not necessarily noise", font_size=22, color=ORANGE)
        warning_group = VGroup(warning_text1, warning_text2).arrange(
            DOWN, aligned_edge=LEFT
        )
        warning_group.next_to(warning_icon, DOWN, buff=0.3)

        self.play(
            FadeIn(warning_icon, scale=0.5),
            Write(warning_text1),
            run_time=max(0.05, 1.5),
        )
        self.play(Write(warning_text2), run_time=max(0.05, 1.0))
        self.play(cutoff_line.animate.set_stroke(width=5), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.4))

        # gap 0.56
        self.wait(max(0.05, 0.56))

        # ============================================================
        # BEAT 9: 27.88 - 29.04
        # ============================================================
        self.play(
            warning_text2.animate.shift(UP * 0.1),
            rate_func=there_and_back,
            run_time=max(0.05, 0.3),
        )
        self.play(
            warning_text2.animate.shift(DOWN * 0.1),
            rate_func=there_and_back,
            run_time=max(0.05, 0.3),
        )

        cutoff_tag = Text("Cutoff", font_size=18, color=ORANGE)
        cutoff_tag.move_to(
            np.array([0, get_cutoff_y(cutoff_tracker.get_value()) + 0.25, 0])
        )

        def update_cutoff_tag(mob):
            mob.move_to(
                np.array([0, get_cutoff_y(cutoff_tracker.get_value()) + 0.25, 0])
            )

        cutoff_tag.add_updater(update_cutoff_tag)
        self.play(Write(cutoff_tag), run_time=max(0.05, 0.56))

        # gap 0.96
        self.wait(max(0.05, 0.96))

        # ============================================================
        # BEAT 10: 30.00 - 34.74
        # ============================================================
        self.play(
            highlight_ring.animate.scale(1.2).set_stroke(width=8),
            rate_func=there_and_back,
            run_time=max(0.05, 1.0),
        )

        cutoff_y_now = get_cutoff_y(cutoff_tracker.get_value())
        red_band = Rectangle(
            width=13,
            height=0.1,
            fill_color=RED,
            fill_opacity=0.3,
            stroke_width=0,
        )
        red_band.move_to(np.array([0, cutoff_y_now + red_band.height / 2, 0]))

        above_cutoff_label = Text("Above cutoff", font_size=20, color=RED)
        above_cutoff_label.next_to(red_band, UP, buff=0.1)
        above_cutoff_label.add_updater(
            lambda mob: mob.next_to(red_band, UP, buff=0.1)
        )

        self.play(FadeIn(red_band), Write(above_cutoff_label), run_time=max(0.05, 1.0))
        target_band_height = top_y_center + top_y_range - cutoff_y_now + 0.2
        self.play(
            red_band.animate.stretch_to_fit_height(
                target_band_height,
                about_edge=DOWN,
            ),
            run_time=max(0.05, 2.5),
        )
        self.wait(max(0.05, 0.24))

        # gap 0.72
        self.wait(max(0.05, 0.72))

        # ============================================================
        # BEAT 11: 35.46 - 37.72
        # ============================================================
        self.play(
            red_band.animate.set_opacity(0.15),
            highlight_ring.animate.set_opacity(0.3),
            run_time=max(0.05, 0.5),
        )
        self.play(smoothness_tracker.animate.set_value(0.8), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 0.26))

        # gap 0.80
        self.wait(max(0.05, 0.80))

        # ============================================================
        # BEAT 12: 38.52 - 45.16
        # ============================================================
        self.play(smoothness_tracker.animate.set_value(0), run_time=max(0.05, 1.5))
        self.play(
            FadeOut(red_band),
            FadeOut(above_cutoff_label),
            run_time=max(0.05, 0.5),
        )

        final_text = Text(
            "Filter selection guided by signal characteristics, not convenience.",
            font_size=26,
            color=WHITE,
            t2c={"signal characteristics": GREEN, "convenience": RED},
        )
        final_text.scale_to_fit_width(10)
        final_text.to_edge(DOWN, buff=0.5)
        self.play(Write(final_text), run_time=max(0.05, 2.0))

        self.play(
            highlight_ring.animate.scale(1.3).set_stroke(width=8),
            rate_func=there_and_back,
            run_time=max(0.05, 1.0),
        )

        self.wait(max(0.05, 1.64))

        # final hold to 45.98
        self.wait(max(0.05, 0.82))