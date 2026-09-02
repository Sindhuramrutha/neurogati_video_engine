ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {
    'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg',
    'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg',
    'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg',
    'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg',
    'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg',
    'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg',
    'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg',
    'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg',
    'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg',
    'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg',
    'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg',
    'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg',
    'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg',
    'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg',
    'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg',
    'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg',
    'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg',
    'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg',
    'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg',
    'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg',
    'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg',
    'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg',
    'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg',
    'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg',
    'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png',
    'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png',
    'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png',
}

from manim import *
import numpy as np


def make_static_raw_wave():
    xs = np.linspace(-5.9, -2.3, 180)
    z = xs / 2.4
    ys = (
        0.25 * np.sin(2 * PI * 1.7 * z)
        + 0.16 * np.sin(2 * PI * 4.3 * z + 1.1)
        + 0.08 * np.sin(2 * PI * 8.2 * z + 0.5)
    )
    raw = VMobject()
    raw.set_points_as_corners([np.array([x, y + 0.2, 0]) for x, y in zip(xs, ys)])
    raw.set_stroke(TEAL, width=2)
    raw.set_fill(opacity=0)
    return raw


def make_processing_chain():
    labels = ["Filtering", "Spectral", "Spectrogram", "Wavelet", "ERP"]
    centers = [
        np.array([-1.0, 0.2, 0]),
        np.array([0.18, 0.2, 0]),
        np.array([1.36, 0.2, 0]),
        np.array([2.54, 0.2, 0]),
        np.array([3.72, 0.2, 0]),
    ]
    chain = VGroup()
    for label, center in zip(labels, centers):
        rect = RoundedRectangle(
            corner_radius=0.12,
            width=0.95,
            height=0.95,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.3,
        )
        rect.move_to(center)
        text = Text(label, font_size=12, color=WHITE)
        text.scale_to_fit_width(0.8)
        text.move_to(center + DOWN * 0.32)
        chain.add(VGroup(rect, text))
    return chain


def make_clean_label():
    return Text("Extracted information", font_size=24, color=WHITE)


def make_abnormal_eeg_icon():
    xs = np.linspace(-1.2, 1.2, 220)
    ys = 0.07 * np.sin(2 * PI * 1.6 * xs)
    ys += 0.45 * np.exp(-((xs + 0.48) ** 2) / 0.006)
    ys -= 0.38 * np.exp(-((xs - 0.22) ** 2) / 0.006)
    trace = VMobject()
    trace.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
    trace.set_stroke(RED, width=3)
    trace.set_fill(opacity=0)
    trace.scale_to_fit_width(1.45)
    trace.scale_to_fit_height(0.9)
    return trace


def make_mini_segment(cycles=2, width=1.5, height=0.22, color=TEAL):
    xs = np.linspace(-width / 2, width / 2, 120)
    ys = (height / 2) * np.sin(2 * PI * cycles * (xs - xs[0]) / (xs[-1] - xs[0]))
    wave = VMobject()
    wave.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, ys)])
    wave.set_stroke(color, width=3)
    wave.set_fill(opacity=0)
    return wave


def make_brain_icon():
    brain_svg = SVGMobject(
        ASSET_PATHS["brain"],
        fill_color=PURPLE,
        fill_opacity=1,
        stroke_color=WHITE,
        stroke_width=0.5,
    )
    brain_svg.scale_to_fit_height(0.9)
    frontal = Circle(radius=0.14, fill_color=ORANGE, fill_opacity=1, stroke_width=0)
    frontal.move_to(brain_svg.get_center() + LEFT * 0.32 + UP * 0.08)
    group = VGroup(brain_svg, frontal)
    group.scale_to_fit_height(0.95)
    group.scale_to_fit_width(1.3)
    return group


def make_heart_wave_icon():
    heart = SVGMobject(
        ASSET_PATHS["heart"],
        fill_color=PINK,
        fill_opacity=1,
        stroke_color=WHITE,
        stroke_width=0.5,
    )
    heart.scale_to_fit_height(0.7)
    seg = make_mini_segment(cycles=2, width=1.1, height=0.3, color=TEAL)
    group = VGroup(heart, seg).arrange(RIGHT, buff=0.2)
    group.scale_to_fit_width(1.4)
    group.scale_to_fit_height(0.85)
    return group


def make_hand_device_icon():
    hand = SVGMobject(
        ASSET_PATHS["hand"],
        fill_color=WHITE,
        fill_opacity=1,
        stroke_color=WHITE,
        stroke_width=0.5,
    )
    hand.scale_to_fit_height(0.75)
    device = RoundedRectangle(
        corner_radius=0.1,
        width=0.8,
        height=0.6,
        stroke_color=BLUE,
        stroke_width=2,
        fill_color=BLUE,
        fill_opacity=0.25,
    )
    pair = VGroup(hand, device).arrange(RIGHT, buff=0.45)
    line = Line(hand.get_right(), device.get_left(), color=GREY_B, stroke_width=2)
    group = VGroup(pair, line)
    group.scale_to_fit_width(1.45)
    group.scale_to_fit_height(0.85)
    return group


class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Continuous flowing waveform trackers
        wave_x_center = ValueTracker(5.45)
        wave_y_center = ValueTracker(0.2)
        wave_amp = ValueTracker(0.38)
        wave_freq = ValueTracker(5.0)
        wave_width = ValueTracker(1.4)

        # Static clean waveform from the previous scene's closing composition
        clean_xs = np.linspace(4.75, 6.15, 120)
        clean_phase = (clean_xs - clean_xs[0]) / (clean_xs[-1] - clean_xs[0])
        clean_ys = 0.38 * np.sin(2 * PI * 2.5 * clean_phase) + 0.2
        wave = VMobject()
        wave.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(clean_xs, clean_ys)])
        wave.set_stroke(TEAL, width=3)
        wave.set_fill(opacity=0)

        # Opening composition that fades away
        raw_wave = make_static_raw_wave()
        processing_chain = make_processing_chain()
        clean_label = make_clean_label()
        clean_label.next_to(wave, DOWN, buff=0.25)
        opening_extra = VGroup(raw_wave, processing_chain, clean_label)

        # ---------------------------- Beat 1: 0.00–2.44 ----------------------------
        self.add(wave, opening_extra)
        self.play(FadeOut(opening_extra), run_time=max(0.05, 1.0))

        def update_wave(m, dt=None):
            t = self.time
            cx = wave_x_center.get_value()
            cy = wave_y_center.get_value()
            w = wave_width.get_value()
            x0, x1 = cx - w / 2, cx + w / 2
            xs = np.linspace(x0, x1, 160)
            f = wave_freq.get_value()
            amp = wave_amp.get_value()
            cycles = max(0.35, f)
            ys = amp * np.sin(2 * PI * f * t - 2 * PI * cycles * (xs - x0) / w)
            m.set_points_as_corners([np.array([x, cy + y, 0]) for x, y in zip(xs, ys)])

        wave.add_updater(update_wave)
        self.play(
            wave_x_center.animate.set_value(-3.5),
            wave_y_center.animate.set_value(0.0),
            wave_width.animate.set_value(6.2),
            run_time=max(0.05, 1.44),
            rate_func=smooth,
        )

        # ---------------------------- Beat 2: 2.44–4.44 ----------------------------
        panel_center = np.array([3.0, -0.15, 0])
        panel = RoundedRectangle(
            corner_radius=0.35,
            width=6.5,
            height=5.7,
            stroke_color=GREY_B,
            stroke_width=2,
            fill_color="#1A1D26",
            fill_opacity=0.95,
        )
        panel.move_to(panel_center)

        slot_positions = [
            np.array([1.5, 0.5, 0]),
            np.array([4.5, 0.5, 0]),
            np.array([1.5, -1.4, 0]),
            np.array([4.5, -1.4, 0]),
        ]
        slots = VGroup()
        for pos in slot_positions:
            slot = RoundedRectangle(
                corner_radius=0.15,
                width=2.0,
                height=1.5,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_color=BLACK,
                fill_opacity=0.2,
            )
            slot.move_to(pos)
            slots.add(slot)

        # Stylized scalp outline + three electrode markers + descending lines
        scalp_arc = Arc(
            radius=0.7,
            start_angle=0,
            angle=PI,
            arc_center=np.array([3.0, 1.75, 0]),
            color=GREY_B,
            stroke_width=4,
        )
        electrode_positions = [scalp_arc.point_from_proportion(p) for p in (0.18, 0.5, 0.82)]
        electrode_dots = VGroup()
        for pos in electrode_positions:
            dot = Dot(pos, radius=0.07, color=YELLOW)
            electrode_dots.add(dot)

        wave_target_points = [
            np.array([-0.9, 0.4, 0]),
            np.array([-0.6, 0.0, 0]),
            np.array([-1.0, -0.35, 0]),
        ]
        electrode_lines = VGroup()
        for start, end in zip(electrode_positions, wave_target_points):
            electrode_lines.add(Line(start, end, color=GREY_B, stroke_width=1.5))
        electrodes = VGroup(electrode_dots, electrode_lines)

        self.play(FadeIn(panel), run_time=max(0.05, 0.6))
        self.play(FadeIn(slots), run_time=max(0.05, 0.5))
        self.play(FadeIn(scalp_arc), FadeIn(electrodes), run_time=max(0.05, 0.4))
        self.play(electrodes.animate.scale(1.15).set_fill(WHITE), run_time=max(0.05, 0.25))
        self.play(FadeOut(electrodes), run_time=max(0.05, 0.25))

        # ---------------------------- Beat 3: 4.44–5.28 ----------------------------
        self.play(
            slots.animate.set_stroke(YELLOW, width=3).set_fill(YELLOW, opacity=0.08),
            run_time=max(0.05, 0.42),
        )
        self.play(
            slots.animate.set_stroke(GREY_B, width=2).set_fill(BLACK, opacity=0.2),
            run_time=max(0.05, 0.42),
        )

        # ---------------------------- Beat 4–5: 5.28–16.10 ----------------------------
        # Icons appear left-to-right, top-to-bottom, on spoken phrases.
        brain_icon = make_brain_icon().move_to(slot_positions[0])
        eeg_icon = make_abnormal_eeg_icon().move_to(slot_positions[1])
        heart_icon = make_heart_wave_icon().move_to(slot_positions[2])
        hand_icon = make_hand_device_icon().move_to(slot_positions[3])

        self.wait(max(0.05, 1.72))  # 7.0
        self.play(FadeIn(brain_icon), run_time=max(0.05, 0.6))

        self.wait(max(0.05, 2.9))  # 10.5
        self.play(FadeIn(eeg_icon), run_time=max(0.05, 0.6))

        self.wait(max(0.05, 1.9))  # 13.0
        self.play(FadeIn(heart_icon), run_time=max(0.05, 0.6))

        self.wait(max(0.05, 1.4))  # 15.0
        self.play(FadeIn(hand_icon), run_time=max(0.05, 0.6))
        self.play(Indicate(hand_icon, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 0.5))

        # ---------------------------- Beat 6: 16.10–17.34 ----------------------------
        self.wait(max(0.05, 1.24))

        # ---------------------------- Beat 7: 17.34–26.36 ----------------------------
        right_area = VGroup(
            panel,
            slots,
            scalp_arc,
            brain_icon,
            eeg_icon,
            heart_icon,
            hand_icon,
        )
        self.play(FadeOut(right_area), run_time=max(0.05, 1.0))

        title_four = Text(
            "4 Applications",
            font_size=52,
            color=WHITE,
            t2c={"4": YELLOW},
        )
        title_four.move_to(np.array([3.2, 2.7, 0]))
        self.play(FadeIn(title_four), run_time=max(0.05, 0.8))

        self.wait(max(0.05, 0.86))
        self.play(wave.animate.set_stroke(GREEN, width=5), run_time=max(0.05, 0.6))

        self.wait(max(0.05, 2.7))  # 23.3
        neural_label = Text("Neural signal processing", font_size=24, color=WHITE)
        neural_label.next_to(wave, DOWN, buff=0.4)
        up_arrow = Arrow(
            start=wave.get_center() + UP * 0.4,
            end=title_four.get_bottom() + DOWN * 0.15,
            buff=0.05,
            color=GREY_B,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.3,
        )
        self.play(FadeIn(neural_label), FadeIn(up_arrow), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.5))
        self.play(FadeOut(neural_label), FadeOut(up_arrow), run_time=max(0.05, 0.7))
        self.wait(max(0.05, 0.06))

        # ---------------------------- Beat 8: 26.36–31.62 ----------------------------
        self.wait(max(0.05, 0.84))  # 27.2
        self.play(
            wave_freq.animate.set_value(2.5),
            wave.animate.set_stroke(WHITE, width=5),
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 2.6))  # 30.6

        brain_title = Text(
            "Brain States",
            font_size=52,
            color=WHITE,
            weight="BOLD",
        )
        brain_title.move_to(np.array([3.2, 2.7, 0]))
        self.play(FadeOut(title_four), FadeIn(brain_title), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 0.02))

        # ---------------------------- Beat 9: 31.62–39.80 ----------------------------
        self.wait(max(0.05, 5.18))  # strong pause through the list setup

        # awake: fast dense oscillation
        self.play(
            wave_freq.animate.set_value(5.0),
            wave_amp.animate.set_value(0.38),
            run_time=max(0.05, 0.7),
            rate_func=smooth,
        )
        # relaxed: transition to slower, broader waves
        self.play(
            wave_freq.animate.set_value(2.5),
            wave_amp.animate.set_value(0.38),
            run_time=max(0.05, 1.2),
            rate_func=smooth,
        )
        # concentrating: briefly sharpens to faster rhythmic activity
        self.play(
            wave_freq.animate.set_value(4.6),
            wave_amp.animate.set_value(0.38),
            run_time=max(0.05, 0.5),
            rate_func=smooth,
        )
        # asleep: very slow, high-amplitude, widely spaced waves
        self.play(
            wave_freq.animate.set_value(0.75),
            wave_amp.animate.set_value(0.95),
            run_time=max(0.05, 0.6),
            rate_func=smooth,
        )

        # ---------------------------- Beat 10: 39.80–47.42 ----------------------------
        self.wait(max(0.05, 0.2))

        label_awake = VGroup(
            make_mini_segment(cycles=5, width=1.5, height=0.22, color=TEAL),
            Text("Awake", font_size=22, color=WHITE),
        )
        label_awake.arrange(DOWN, buff=0.08)

        label_relaxed = VGroup(
            make_mini_segment(cycles=2, width=1.5, height=0.22, color=TEAL),
            Text("Relaxed", font_size=22, color=WHITE),
        )
        label_relaxed.arrange(DOWN, buff=0.08)

        label_asleep = VGroup(
            make_mini_segment(cycles=1, width=1.5, height=0.22, color=TEAL),
            Text("Asleep", font_size=22, color=WHITE),
        )
        label_asleep.arrange(DOWN, buff=0.08)

        for label, x in [(label_awake, -5.0), (label_relaxed, -3.5), (label_asleep, -2.0)]:
            label.move_to(np.array([x, -1.6, 0]))

        labels_group = VGroup(label_awake, label_relaxed, label_asleep)
        self.play(FadeIn(labels_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.9))  # 43.9

        self.play(FadeOut(labels_group), run_time=max(0.05, 0.4))

        note = Text("Normal brain function & behavior", font_size=24, color=WHITE)
        note.next_to(wave, DOWN, buff=0.5)

        self.play(
            FadeIn(note),
            wave_freq.animate.set_value(5.0),
            wave_amp.animate.set_value(0.38),
            run_time=max(0.05, 0.8),
            rate_func=smooth,
        )
        self.play(
            wave_freq.animate.set_value(0.75),
            wave_amp.animate.set_value(0.9),
            run_time=max(0.05, 0.8),
            rate_func=smooth,
        )
        self.play(
            wave_freq.animate.set_value(2.5),
            wave_amp.animate.set_value(0.38),
            run_time=max(0.05, 0.8),
            rate_func=smooth,
        )
        self.play(FadeOut(note), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 0.32))

        # ---------------------------- Beat 11: 47.42–52.83 ----------------------------
        self.play(
            brain_title.animate.scale(1.1).move_to(np.array([0, 2.4, 0])),
            wave_x_center.animate.set_value(0.0),
            wave_y_center.animate.set_value(-0.5),
            wave_width.animate.set_value(5.4),
            run_time=max(0.05, 1.4),
            rate_func=smooth,
        )
        self.wait(max(0.05, 0.8))

        final_arrow = Arrow(
            start=wave.get_top() + UP * 0.15,
            end=brain_title.get_bottom() + DOWN * 0.1,
            buff=0.05,
            color=GREY_B,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.3,
        )
        next_section = Text("Next section", font_size=24, color=WHITE)
        next_section.to_corner(DR, buff=0.5)

        self.play(FadeIn(final_arrow), FadeIn(next_section), run_time=max(0.05, 0.8))
        self.play(wave.animate.set_stroke(WHITE, width=6), run_time=max(0.05, 0.4))
        self.play(wave.animate.set_stroke(TEAL, width=4), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 1.61))