ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


def make_filter_icon():
    xs_jag = np.linspace(-0.34, -0.02, 50)
    jag_phase = (xs_jag - xs_jag[0]) / (xs_jag[-1] - xs_jag[0])
    ys_jag = 0.10 * np.sin(2 * PI * 5 * jag_phase) + 0.12 * np.sin(2 * PI * 11 * jag_phase + 0.5)
    jag = VMobject()
    jag.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs_jag, ys_jag)])
    jag.set_stroke(ORANGE, width=2)
    jag.set_fill(opacity=0)

    xs_sm = np.linspace(0.02, 0.34, 60)
    sm_phase = (xs_sm - xs_sm[0]) / (xs_sm[-1] - xs_sm[0])
    ys_sm = 0.16 * np.sin(2 * PI * 2 * sm_phase)
    smooth = VMobject()
    smooth.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs_sm, ys_sm)])
    smooth.set_stroke(TEAL, width=2)
    smooth.set_fill(opacity=0)

    return VGroup(jag, smooth)


def make_filter_sparks():
    sparks = VGroup()
    positions = [(-0.26, 0.16), (-0.20, -0.12), (-0.12, 0.10), (-0.06, -0.13)]
    for x, y in positions:
        l1 = Line(
            np.array([x - 0.03, y - 0.02, 0]),
            np.array([x + 0.03, y + 0.03, 0]),
            color=RED,
            stroke_width=2.5,
        )
        l2 = Line(
            np.array([x + 0.03, y + 0.03, 0]),
            np.array([x + 0.01, y - 0.03, 0]),
            color=RED,
            stroke_width=2.5,
        )
        sparks.add(VGroup(l1, l2))
    return sparks


def make_spectral_icon():
    axis = Line(np.array([-0.34, 0, 0]), np.array([0.34, 0, 0]), color=WHITE, stroke_width=2)
    bars = VGroup()
    heights = [0.10, 0.20, 0.38, 0.46, 0.32, 0.18, 0.10]
    colors = [BLUE, BLUE, PURPLE, PURPLE, PURPLE, BLUE, BLUE]
    xs = np.linspace(-0.30, 0.30, len(heights))
    for x, h, c in zip(xs, heights, colors):
        rect = Rectangle(width=0.07, height=h, fill_color=c, fill_opacity=1, stroke_width=0)
        rect.move_to(np.array([x, h / 2 + 0.015, 0]))
        bars.add(rect)
    return VGroup(axis, bars), bars


def make_spectrogram_icon():
    bands = VGroup()
    band_y = [-0.18, -0.09, 0.0, 0.09, 0.18]
    band_colors = [TEAL, BLUE, PURPLE, ORANGE, GREEN]
    band_opacity = [0.55, 0.75, 0.95, 0.70, 0.45]
    for y, c, op in zip(band_y, band_colors, band_opacity):
        rect = Rectangle(width=0.68, height=0.055, fill_color=c, fill_opacity=op, stroke_width=0)
        rect.move_to(np.array([0, y, 0]))
        bands.add(rect)
    t_label = Text("t →", font_size=16, color=WHITE)
    t_label.next_to(bands, DOWN, buff=0.04)
    return VGroup(bands, t_label), bands


def make_wavelet_icon():
    xs = np.linspace(-0.36, 0.36, 120)
    sigma = 0.11
    ys = 0.26 * np.sin(2 * PI * 4 * xs) * np.exp(-(xs ** 2) / (2 * sigma ** 2))
    curve = VMobject()
    curve.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
    curve.set_stroke(PURPLE, width=3)
    curve.set_fill(opacity=0)
    return curve


def make_erp_icon():
    x_axis = Line(np.array([-0.34, 0, 0]), np.array([0.34, 0, 0]), color=WHITE, stroke_width=1.5)
    y_axis = Line(np.array([-0.34, -0.18, 0]), np.array([-0.34, 0.18, 0]), color=WHITE, stroke_width=1.5)
    dashed = DashedLine(
        np.array([0.02, -0.19, 0]),
        np.array([0.02, 0.19, 0]),
        color=GREY_B,
        dash_length=0.03,
    )

    traces = VGroup()
    xs = np.linspace(-0.30, 0.30, 90)
    for shift, phase in zip([-0.06, -0.02, 0.02, 0.06], [0.2, 0.7, 1.1, 0.5]):
        ys = 0.14 * np.exp(-((xs - 0.01) ** 2) / 0.012) + 0.04 * np.sin(2 * PI * 1.5 * xs + phase) + shift * 0.08
        trace = VMobject()
        trace.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
        trace.set_stroke(GREY_B, width=1.5)
        trace.set_opacity(0.45)
        traces.add(trace)

    avg_ys = 0.18 * np.exp(-((xs - 0.01) ** 2) / 0.012) + 0.03 * np.sin(2 * PI * 1.5 * xs + 0.6)
    avg_trace = VMobject()
    avg_trace.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, avg_ys)])
    avg_trace.set_stroke(WHITE, width=2)
    avg_trace.set_opacity(0.45)

    return VGroup(x_axis, y_axis, dashed, traces, avg_trace), avg_trace


def make_clean_wave():
    xs = np.linspace(4.75, 6.15, 120)
    ys = 0.38 * np.sin(2 * PI * 2.5 * (xs - xs[0]) / (xs[-1] - xs[0])) + 0.2
    wave = VMobject()
    wave.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
    wave.set_stroke(TEAL, width=3)
    wave.set_fill(opacity=0)
    return wave


class Scene2(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------------------------- Beat 1: 0.00–2.06 ----------------------------
        raw_x = np.linspace(-5.9, -2.3, 220)
        raw_phase = ValueTracker(0)

        def raw_y(x, ph):
            period = 2.4
            z = (x - ph) / period
            return (
                0.30 * np.sin(2 * PI * 1.7 * z)
                + 0.20 * np.sin(2 * PI * 4.3 * z + 1.1)
                + 0.12 * np.sin(2 * PI * 8.5 * z + 0.5)
                + 0.07 * np.sin(2 * PI * 14 * z + 2.2)
            )

        raw_wave = VMobject()

        def update_raw_wave(m):
            pts = [np.array([x, raw_y(x, raw_phase.get_value()) + 0.2, 0]) for x in raw_x]
            m.set_points_as_corners(pts)

        raw_wave.add_updater(update_raw_wave)
        update_raw_wave(raw_wave)
        raw_wave.set_stroke(TEAL, width=2)
        raw_wave.set_fill(opacity=0)

        self.play(FadeIn(raw_wave), raw_phase.animate.set_value(2.4), run_time=max(0.05, 2.06))

        # ---------------------------- Beat 2: 2.06–5.48 ----------------------------
        raw_label = Text("Raw EEG waveform", font_size=26, color=WHITE)
        raw_label.move_to(np.array([-4.5, -0.65, 0]))

        cross_center = np.array([-1.85, 0.4, 0])
        cross = VGroup(
            Line(
                cross_center + LEFT * 0.35 + UP * 0.35,
                cross_center + RIGHT * 0.35 + DOWN * 0.35,
                color=RED,
                stroke_width=10,
            ),
            Line(
                cross_center + LEFT * 0.35 + DOWN * 0.35,
                cross_center + RIGHT * 0.35 + UP * 0.35,
                color=RED,
                stroke_width=10,
            ),
        )

        self.play(FadeIn(raw_label), run_time=max(0.05, 0.7))
        self.play(
            raw_wave.animate.set_color(GREY_B).set_opacity(0.65),
            FadeIn(cross),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.5))
        self.play(FadeOut(cross), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.82))

        # ---------------------------- Beat 3: 5.48–7.88 ----------------------------
        input_arrow = Arrow(
            np.array([-2.18, 0.2, 0]),
            np.array([-1.48, 0.2, 0]),
            buff=0.02,
            color=WHITE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.35,
        )
        signal_processing_text = Text("Signal Processing", font_size=24, color=WHITE, weight="MEDIUM")
        signal_processing_text.next_to(input_arrow, UP, buff=0.18)

        self.play(FadeIn(input_arrow), run_time=max(0.05, 0.9))
        self.play(FadeIn(signal_processing_text), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.7))

        # ---------------------------- Build processing blocks ----------------------------
        labels = ["Filtering", "Spectral Analysis", "Spectrogram", "Wavelet Analysis", "ERP Analysis"]
        block_centers = [
            np.array([-1.0, 0.2, 0]),
            np.array([0.18, 0.2, 0]),
            np.array([1.36, 0.2, 0]),
            np.array([2.54, 0.2, 0]),
            np.array([3.72, 0.2, 0]),
        ]
        placeholder_colors = [BLUE, PURPLE, TEAL, ORANGE, GREEN]

        block_rects = []
        placeholders = []
        icon_positions = []
        block_visuals = []

        for i, center in enumerate(block_centers):
            rect = RoundedRectangle(
                corner_radius=0.14,
                width=0.95,
                height=0.95,
                stroke_color=WHITE,
                stroke_width=2,
                fill_color=BLACK,
                fill_opacity=0.0,
            )
            rect.move_to(center)

            icon_pos = center + UP * 0.10
            placeholder = Circle(
                radius=0.07,
                fill_color=placeholder_colors[i],
                fill_opacity=1,
                stroke_width=0,
            )
            placeholder.move_to(icon_pos)

            label = Text(labels[i], font_size=14, color=WHITE)
            label.scale_to_fit_width(0.82)
            label.move_to(center + DOWN * 0.24)

            block_rects.append(rect)
            placeholders.append(placeholder)
            icon_positions.append(icon_pos)
            block_visuals.append(VGroup(rect, placeholder, label))

        connector_arrows = VGroup()
        for i in range(4):
            arrow = Arrow(
                block_rects[i].get_right(),
                block_rects[i + 1].get_left(),
                buff=0.03,
                color=GREY_B,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.5,
            )
            connector_arrows.add(arrow)

        # ---------------------------- Beat 4: 7.88–12.20 ----------------------------
        for visual in block_visuals:
            self.play(FadeIn(visual), run_time=max(0.05, 0.7))
        self.play(FadeIn(connector_arrows), run_time=max(0.05, 0.82))

        # ---------------------------- Beat 5: 12.20–15.78 ----------------------------
        filter_icon = make_filter_icon()
        filter_icon.scale_to_fit_height(0.46)
        filter_icon.move_to(icon_positions[0])

        filter_sparks = make_filter_sparks()
        filter_sparks.scale_to_fit_width(0.38)
        filter_sparks.move_to(icon_positions[0] + LEFT * 0.04)

        rect0 = block_rects[0]
        self.play(
            rect0.animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).scale(1.12),
            FadeOut(placeholders[0]),
            FadeIn(filter_icon),
            run_time=max(0.05, 0.8),
        )
        self.play(FadeIn(filter_sparks), run_time=max(0.05, 0.5))
        self.play(FadeOut(filter_sparks), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 1.73))

        # ---------------------------- Beat 6: 15.78–19.50 ----------------------------
        spectral_icon, spectral_bars = make_spectral_icon()
        spectral_icon.scale_to_fit_height(0.46)
        spectral_icon.move_to(icon_positions[1])

        rect1 = block_rects[1]
        tall_bars = VGroup(spectral_bars[2], spectral_bars[3])
        self.play(
            rect0.animate.set_stroke(WHITE, 2).set_fill(BLACK, 0).scale(1 / 1.12),
            rect1.animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).scale(1.12),
            FadeOut(placeholders[1]),
            FadeIn(spectral_icon),
            run_time=max(0.05, 0.75),
        )
        self.play(tall_bars.animate.set_fill(YELLOW).scale(1.15), run_time=max(0.05, 0.4))
        self.play(tall_bars.animate.set_fill(PURPLE).scale(1 / 1.15), run_time=max(0.05, 0.4))
        self.play(
            rect1.animate.set_stroke(WHITE, 2).set_fill(BLACK, 0).scale(1 / 1.12),
            run_time=max(0.05, 0.45),
        )
        self.wait(max(0.05, 1.72))

        # ---------------------------- Beat 7: 19.50–23.48 ----------------------------
        spectrogram_icon, spectrogram_bands = make_spectrogram_icon()
        spectrogram_icon.scale_to_fit_height(0.46)
        spectrogram_icon.move_to(icon_positions[2])

        rect2 = block_rects[2]
        self.play(
            rect2.animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).scale(1.12),
            FadeOut(placeholders[2]),
            FadeIn(spectrogram_icon),
            run_time=max(0.05, 0.8),
        )
        self.play(spectrogram_bands.animate.shift(RIGHT * 0.07), run_time=max(0.05, 0.55))
        self.play(spectrogram_bands.animate.shift(LEFT * 0.07), run_time=max(0.05, 0.55))
        self.play(
            rect2.animate.set_stroke(WHITE, 2).set_fill(BLACK, 0).scale(1 / 1.12),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 1.68))

        # ---------------------------- Beat 8: 23.48–26.68 ----------------------------
        wavelet_icon = make_wavelet_icon()
        wavelet_icon.scale_to_fit_height(0.46)
        wavelet_icon.move_to(icon_positions[3])

        rect3 = block_rects[3]
        self.play(
            rect3.animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).scale(1.12),
            FadeOut(placeholders[3]),
            FadeIn(wavelet_icon),
            run_time=max(0.05, 0.75),
        )
        pulse_dot = Dot(color=YELLOW, radius=0.05)
        self.play(FadeIn(pulse_dot), run_time=max(0.05, 0.2))
        self.play(MoveAlongPath(pulse_dot, wavelet_icon), run_time=max(0.05, 0.9))
        self.play(FadeOut(pulse_dot), run_time=max(0.05, 0.2))
        self.play(
            rect3.animate.set_stroke(WHITE, 2).set_fill(BLACK, 0).scale(1 / 1.12),
            run_time=max(0.05, 0.4),
        )
        self.wait(max(0.05, 0.75))

        # ---------------------------- Beat 9: 26.68–32.02 ----------------------------
        erp_icon, avg_trace = make_erp_icon()
        erp_icon.scale_to_fit_height(0.52)
        erp_icon.move_to(icon_positions[4])

        rect4 = block_rects[4]
        self.play(
            rect4.animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).scale(1.12),
            FadeOut(placeholders[4]),
            FadeIn(erp_icon),
            run_time=max(0.05, 0.9),
        )
        self.play(avg_trace.animate.set_stroke(YELLOW, 4).set_opacity(1), run_time=max(0.05, 1.3))
        self.wait(max(0.05, 1.2))
        self.play(
            rect4.animate.set_stroke(WHITE, 2).set_fill(BLACK, 0).scale(1 / 1.12),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 1.44))

        # ---------------------------- Beat 10: 32.02–36.30 ----------------------------
        self.play(rect4.animate.set_stroke(WHITE, 2).set_fill(BLACK, 0), run_time=max(0.05, 0.4))

        clean_wave = make_clean_wave()
        final_arrow = Arrow(
            rect4.get_right(),
            clean_wave.get_left(),
            buff=0.05,
            color=WHITE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.35,
        )

        self.play(FadeIn(final_arrow), run_time=max(0.05, 0.6))
        self.play(Write(clean_wave), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 1.88))

        # ---------------------------- Beat 11: 36.30–40.48 ----------------------------
        clean_label = Text("Extracted information", font_size=24, color=WHITE)
        clean_label.next_to(clean_wave, DOWN, buff=0.25)
        self.play(FadeIn(clean_label), run_time=max(0.05, 0.7))

        for rect in block_rects:
            self.play(
                rect.animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.15).scale(1.05),
                run_time=max(0.05, 0.18),
            )
            self.play(
                rect.animate.set_stroke(WHITE, 2).set_fill(BLACK, 0).scale(1 / 1.05),
                run_time=max(0.05, 0.18),
            )

        bracket = Line(
            np.array([block_rects[0].get_left()[0], 1.05, 0]),
            np.array([block_rects[-1].get_right()[0], 1.05, 0]),
            color=GREY_B,
            stroke_width=2,
        )
        concepts_text = Text("Concepts from earlier modules", font_size=18, color=GREY_B)
        concepts_text.next_to(bracket, UP, buff=0.10)

        self.play(FadeIn(bracket), FadeIn(concepts_text), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.98))