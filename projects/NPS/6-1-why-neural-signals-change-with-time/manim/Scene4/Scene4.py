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


def make_wave_vmobject(amp, freq, mix, color=TEAL, width=4.0, num=240):
    xs = np.linspace(-width / 2, width / 2, num)
    ys = amp * np.sin(2 * PI * freq * xs) + mix * np.sin(2 * PI * freq * 2.3 * xs + 1.1)
    wave = VMobject(stroke_color=color, stroke_width=3)
    wave.set_points_as_corners([np.array([x, y, 0.0]) for x, y in zip(xs, ys)])
    return wave


def make_resting_icon():
    chair = VGroup(
        Line(LEFT * 0.30 + DOWN * 0.30, RIGHT * 0.30 + DOWN * 0.30, color=GREY_B, stroke_width=3),
        Line(LEFT * 0.22 + DOWN * 0.30, LEFT * 0.22 + UP * 0.20, color=GREY_B, stroke_width=3),
    )
    head = Circle(radius=0.10, color=WHITE, fill_opacity=1, stroke_width=0).move_to(UP * 0.46)
    body = Line(UP * 0.34, ORIGIN, color=WHITE, stroke_width=3)
    arms = VGroup(
        Line(UP * 0.24, LEFT * 0.18, color=WHITE, stroke_width=3),
        Line(UP * 0.24, RIGHT * 0.18, color=WHITE, stroke_width=3),
    )
    legs = VGroup(
        Line(ORIGIN, LEFT * 0.24 + DOWN * 0.28, color=WHITE, stroke_width=3),
        Line(LEFT * 0.24 + DOWN * 0.28, LEFT * 0.38 + DOWN * 0.48, color=WHITE, stroke_width=3),
        Line(ORIGIN, RIGHT * 0.24 + DOWN * 0.28, color=WHITE, stroke_width=3),
        Line(RIGHT * 0.24 + DOWN * 0.28, RIGHT * 0.38 + DOWN * 0.48, color=WHITE, stroke_width=3),
    )
    return VGroup(chair, head, body, arms, legs)


def make_walking_icon():
    head = Circle(radius=0.10, color=WHITE, fill_opacity=1, stroke_width=0).move_to(UP * 0.48)
    body = Line(UP * 0.36, DOWN * 0.02, color=WHITE, stroke_width=3)
    arms = VGroup(
        Line(UP * 0.28, RIGHT * 0.34 + UP * 0.04, color=WHITE, stroke_width=3),
        Line(UP * 0.28, LEFT * 0.32 + UP * 0.08, color=WHITE, stroke_width=3),
    )
    legs = VGroup(
        Line(DOWN * 0.02, LEFT * 0.30 + DOWN * 0.30, color=WHITE, stroke_width=3),
        Line(LEFT * 0.30 + DOWN * 0.30, LEFT * 0.46 + DOWN * 0.48, color=WHITE, stroke_width=3),
        Line(DOWN * 0.02, RIGHT * 0.30 + DOWN * 0.30, color=WHITE, stroke_width=3),
        Line(RIGHT * 0.30 + DOWN * 0.30, RIGHT * 0.46 + DOWN * 0.48, color=WHITE, stroke_width=3),
    )
    return VGroup(head, body, arms, legs)


def make_speaking_icon():
    head = Circle(radius=0.10, color=WHITE, fill_opacity=1, stroke_width=0).move_to(UP * 0.44)
    body = Line(UP * 0.33, DOWN * 0.12, color=WHITE, stroke_width=3)
    arms = VGroup(
        Line(UP * 0.22, LEFT * 0.22 + DOWN * 0.10, color=WHITE, stroke_width=3),
        Line(UP * 0.22, RIGHT * 0.22 + DOWN * 0.10, color=WHITE, stroke_width=3),
    )
    legs = VGroup(
        Line(DOWN * 0.12, LEFT * 0.18 + DOWN * 0.42, color=WHITE, stroke_width=3),
        Line(DOWN * 0.12, RIGHT * 0.18 + DOWN * 0.42, color=WHITE, stroke_width=3),
    )
    speech = VGroup(
        Arc(radius=0.13, start_angle=0.2, angle=1.6, color=WHITE, stroke_width=2),
        Arc(radius=0.20, start_angle=0.2, angle=1.6, color=WHITE, stroke_width=2),
        Arc(radius=0.27, start_angle=0.2, angle=1.6, color=WHITE, stroke_width=2),
    ).move_to(RIGHT * 0.42 + UP * 0.42)
    return VGroup(head, body, arms, legs, speech)


def make_task_icon():
    desk = Line(LEFT * 0.45 + DOWN * 0.02, RIGHT * 0.45 + DOWN * 0.02, color=GREY_B, stroke_width=4)
    obj = Rectangle(width=0.16, height=0.12, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
    obj.move_to(RIGHT * 0.18 + DOWN * 0.04)
    head = Circle(radius=0.10, color=WHITE, fill_opacity=1, stroke_width=0).move_to(UP * 0.48)
    body = Line(UP * 0.36, DOWN * 0.04, color=WHITE, stroke_width=3)
    arms = VGroup(
        Line(UP * 0.26, LEFT * 0.24 + DOWN * 0.04, color=WHITE, stroke_width=3),
        Line(UP * 0.26, RIGHT * 0.12 + DOWN * 0.02, color=WHITE, stroke_width=3),
    )
    legs = VGroup(
        Line(DOWN * 0.04, LEFT * 0.22 + DOWN * 0.42, color=WHITE, stroke_width=3),
        Line(DOWN * 0.04, RIGHT * 0.22 + DOWN * 0.42, color=WHITE, stroke_width=3),
    )
    return VGroup(desk, obj, head, body, arms, legs)


def place_slot_icon(slot, icon):
    icon.scale_to_fit_height(0.85)
    if icon.width > 1.25:
        icon.scale_to_fit_width(1.25)
    return icon.move_to(slot.get_center() + LEFT * 0.55 + UP * 0.15)


def place_slot_label(slot, text):
    label = Text(text, font_size=16, color=WHITE)
    if label.width > 2.5:
        label.scale_to_fit_width(2.5)
    return label.move_to(slot.get_bottom() + UP * 0.30)


def place_slot_wave(slot, wave):
    wave.scale_to_fit_width(1.2)
    return wave.move_to(slot.get_center() + RIGHT * 0.62 + UP * 0.15)


class Scene4(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Previous scene carry-over (heading + definition box)
        prev_heading = Text("Nonstationary Signal", font_size=52, weight="BOLD", color=WHITE)
        prev_heading.to_edge(UP, buff=0.6)
        prev_def_text = Text(
            "Nonstationary: statistical or spectral characteristics change over time",
            font_size=30,
            color=WHITE,
            t2c={"statistical": YELLOW, "spectral": YELLOW, "change": YELLOW},
        )
        if prev_def_text.width > 10.5:
            prev_def_text.scale_to_fit_width(10.5)
        prev_def_box = SurroundingRectangle(
            prev_def_text,
            color=YELLOW,
            buff=0.35,
            corner_radius=0.18,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=3,
        )
        prev_def_group = VGroup(prev_def_box, prev_def_text).to_edge(DOWN, buff=0.55)
        self.add(prev_heading, prev_def_group)

        # New heading
        heading = Text("Changes in Behaviour", font_size=46, weight="BOLD", color=WHITE)
        heading.to_edge(UP, buff=0.45)

        # Brain outline + glow
        brain_asset = SVGMobject(ASSET_PATHS["brain"])
        brain_asset.set(height=2.2)
        brain_asset.move_to(np.array([-3.0, 1.45, 0.0]))
        brain_asset.set_fill(BLUE, opacity=0.14).set_stroke(BLUE, width=2)

        brain_label = Text("ongoing physiological activity", font_size=22, color=WHITE)
        brain_label.next_to(brain_asset, DOWN, buff=0.25)

        brain_glow = Circle(
            radius=1.35,
            stroke_width=0,
            fill_color=BLUE,
            fill_opacity=0.12,
        ).move_to(brain_asset.get_center())
        brain_glow.set_z_index(-1)

        # Main waveform beside brain (morphing variants)
        brain_wave_default = make_wave_vmobject(0.38, 1.8, 0.12, TEAL, width=4.0)
        brain_wave_fast = make_wave_vmobject(0.28, 2.8, 0.35, TEAL, width=4.0)
        brain_wave_slow = make_wave_vmobject(0.45, 1.4, 0.15, TEAL, width=4.0)
        brain_wave_natural = make_wave_vmobject(0.30, 2.2, 0.45, TEAL, width=4.0)
        for w in [brain_wave_default, brain_wave_fast, brain_wave_slow, brain_wave_natural]:
            w.move_to(np.array([3.1, 1.45, 0.0]))
        brain_wave = brain_wave_default.copy()

        # Four empty behaviour slots
        slot_rects = VGroup(*[
            Rectangle(
                width=2.75,
                height=2.15,
                color=GREY_B,
                stroke_width=1.5,
                fill_color=GREY_B,
                fill_opacity=0.08,
            )
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.4).move_to(np.array([0.0, -2.05, 0.0]))

        # Build icons, labels, and small waveforms
        resting_icon = place_slot_icon(slot_rects[0], make_resting_icon())
        resting_label = place_slot_label(slot_rects[0], "Resting")
        walking_icon = place_slot_icon(slot_rects[1], make_walking_icon())
        walking_label = place_slot_label(slot_rects[1], "Walking")
        speaking_icon = place_slot_icon(slot_rects[2], make_speaking_icon())
        speaking_label = place_slot_label(slot_rects[2], "Speaking")
        task_icon = place_slot_icon(slot_rects[3], make_task_icon())
        task_label = place_slot_label(slot_rects[3], "Performing a task")

        resting_wave = place_slot_wave(slot_rects[0], make_wave_vmobject(0.32, 1.0, 0.0, GREEN, width=1.3, num=130))
        walking_wave = place_slot_wave(slot_rects[1], make_wave_vmobject(0.20, 2.2, 0.0, TEAL, width=1.3, num=130))
        speaking_wave = place_slot_wave(slot_rects[2], make_wave_vmobject(0.10, 4.2, 0.0, ORANGE, width=1.3, num=130))
        task_wave = place_slot_wave(slot_rects[3], make_wave_vmobject(0.08, 2.8, 0.12, PURPLE, width=1.3, num=160))

        # --- 0.00-2.26: fade old, bring in new heading, brain, label ---
        self.play(FadeOut(prev_heading, prev_def_group), run_time=max(0.05, 0.70))
        self.play(FadeIn(heading), run_time=max(0.05, 0.60))
        self.play(FadeIn(brain_asset, brain_label, brain_glow), run_time=max(0.05, 0.96))

        # --- 2.26-2.80: pulse subtle glow ---
        self.play(
            brain_glow.animate.scale(1.15).set_opacity(0.22),
            rate_func=there_and_back,
            run_time=max(0.05, 0.54),
        )

        # --- 2.80-6.88: label highlight, brain pulse, main wave fades in ---
        self.play(
            brain_label.animate.set_color(YELLOW).scale(1.15),
            run_time=max(0.05, 0.50),
        )
        self.play(
            brain_label.animate.set_color(WHITE).scale(1 / 1.15),
            FadeIn(brain_wave),
            run_time=max(0.05, 0.50),
        )
        self.play(
            brain_glow.animate.scale(1.28).set_opacity(0.32),
            rate_func=there_and_back,
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 2.38))

        # --- 6.88-7.54: brief pulse ---
        self.play(
            brain_glow.animate.scale(1.18).set_opacity(0.25),
            rate_func=there_and_back,
            run_time=max(0.05, 0.66),
        )

        # --- 7.54-12.16: waveform variability + faster/slower brain pulse ---
        self.play(
            Transform(brain_wave, brain_wave_fast),
            brain_glow.animate.scale(1.25).set_opacity(0.32),
            run_time=max(0.05, 1.54),
        )
        self.play(
            Transform(brain_wave, brain_wave_slow),
            brain_glow.animate.scale(1.15).set_opacity(0.22),
            run_time=max(0.05, 1.54),
        )
        self.play(
            Transform(brain_wave, brain_wave_fast),
            brain_glow.animate.scale(1.25).set_opacity(0.32),
            run_time=max(0.05, 1.54),
        )

        # --- 12.16-12.58: pause with established variability ---
        self.wait(max(0.05, 0.42))

        # --- 12.58-15.18: recurring irregularity settles in ---
        self.play(
            Transform(brain_wave, brain_wave_natural),
            run_time=max(0.05, 1.10),
        )
        self.play(
            brain_glow.animate.scale(1.20).set_opacity(0.28),
            rate_func=there_and_back,
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.80))

        # --- 15.18-16.02: hold current composition ---
        self.wait(max(0.05, 0.84))

        # --- 16.02-18.08: four empty slots fade in ---
        self.play(FadeIn(slot_rects), run_time=max(0.05, 2.06))

        # --- 18.08-18.94: brief pause ---
        self.wait(max(0.05, 0.86))

        # --- 18.94-19.76: first slot fills: Resting ---
        self.play(FadeIn(resting_icon, resting_label), run_time=max(0.05, 0.50))
        self.play(
            Indicate(VGroup(resting_icon, resting_label), scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.32),
        )

        # --- 19.76-20.34: pause after Resting ---
        self.wait(max(0.05, 0.58))

        # --- 20.34-21.34: brain pulse continues, anticipation ---
        self.play(
            brain_glow.animate.scale(1.22).set_opacity(0.28),
            rate_func=there_and_back,
            run_time=max(0.05, 1.00),
        )

        # --- 21.34-22.30: second slot fills: Walking ---
        self.play(FadeIn(walking_icon, walking_label), run_time=max(0.05, 0.50))
        self.play(
            Indicate(VGroup(walking_icon, walking_label), scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.46),
        )

        # --- 22.30-23.36: third slot fills: Speaking ---
        self.play(FadeIn(speaking_icon, speaking_label), run_time=max(0.05, 0.50))
        self.play(
            Indicate(VGroup(speaking_icon, speaking_label), scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.56),
        )

        # --- 23.36-23.92: all three icons visible, fourth empty ---
        self.wait(max(0.05, 0.56))

        # --- 23.92-24.18: Resting highlight + slow large waveform ---
        self.play(
            FadeIn(resting_wave),
            Indicate(resting_icon, scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.26),
        )

        # --- 24.18-24.72: pause while resting waveform remains ---
        self.wait(max(0.05, 0.54))

        # --- 24.72-24.98: Walking highlight + moderate waveform ---
        self.play(
            FadeIn(walking_wave),
            Indicate(walking_icon, scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.26),
        )

        # --- 24.98-25.52: Speaking highlight + fine rapid waveform ---
        self.play(
            FadeIn(speaking_wave),
            Indicate(speaking_icon, scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.54),
        )

        # --- 25.52-25.86: all three waveform segments visible ---
        self.wait(max(0.05, 0.34))

        # --- 25.86-26.30: fourth slot fills: Performing a task ---
        self.play(FadeIn(task_icon, task_label), run_time=max(0.05, 0.22))
        self.play(
            Indicate(VGroup(task_icon, task_label), scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.22),
        )

        # --- 26.30-26.76: task waveform appears ---
        self.play(
            FadeIn(task_wave),
            Indicate(task_icon, scale_factor=1.15, color=YELLOW),
            run_time=max(0.05, 0.46),
        )

        # --- 26.76-27.22: all four icons + waveforms visible ---
        self.wait(max(0.05, 0.46))

        # --- 27.22-28.46: arrow from brain to behaviours appears ---
        causal_arrow = Arrow(
            start=brain_asset.get_bottom() + DOWN * 0.18,
            end=slot_rects.get_top() + UP * 0.10,
            path_arc=0.35,
            color=ORANGE,
            stroke_width=5,
            buff=0.05,
        )
        self.play(FadeIn(causal_arrow), run_time=max(0.05, 0.70))
        self.play(
            causal_arrow.animate.set_stroke(YELLOW, width=7),
            rate_func=there_and_back,
            run_time=max(0.05, 0.54),
        )

        # --- 28.46-29.36: sequential waveform highlights ---
        wave_list = [resting_wave, walking_wave, speaking_wave, task_wave]
        color_list = [GREEN, TEAL, ORANGE, PURPLE]
        per = max(0.05, 0.90 / 4.0)
        for wave, color in zip(wave_list, color_list):
            self.play(
                wave.animate.set_color(YELLOW).set_stroke(width=5),
                run_time=max(0.05, per * 0.5),
            )
            self.play(
                wave.animate.set_color(color).set_stroke(width=3),
                run_time=max(0.05, per * 0.5),
            )

        # --- 29.36-29.86: arrow holds steady, wave highlights return ---
        self.wait(max(0.05, 0.50))

        # --- 29.86-30.62: label re-highlights, pulse synchronises ---
        self.play(
            brain_label.animate.set_color(YELLOW).scale(1.15),
            brain_glow.animate.scale(1.18).set_opacity(0.28),
            run_time=max(0.05, 0.38),
        )
        self.play(
            brain_label.animate.set_color(WHITE).scale(1 / 1.15),
            brain_glow.animate.scale(1.0).set_opacity(0.15),
            run_time=max(0.05, 0.38),
        )

        # --- 30.62-31.50: final sequential wave brighten ---
        per_final = max(0.05, 0.88 / 4.0)
        for wave, color in zip(wave_list, color_list):
            self.play(
                wave.animate.set_color(WHITE).set_stroke(width=6),
                run_time=max(0.05, per_final * 0.5),
            )
            self.play(
                wave.animate.set_color(color).set_stroke(width=3),
                run_time=max(0.05, per_final * 0.5),
            )

        # --- 31.50-32.23: final hold ---
        self.wait(max(0.05, 0.73))