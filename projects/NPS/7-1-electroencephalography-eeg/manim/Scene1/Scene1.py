ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

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


def make_tile_segment(amplitude=0.4, cycles=4, width=8.0, color=TEAL):
    xs = np.linspace(0, width, 120)
    ys = amplitude * np.sin(2 * PI * cycles * xs / width)
    pts = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
    tile = VMobject()
    tile.set_points_as_corners(pts)
    tile.set_stroke(color, width=2)
    tile.set_fill(opacity=0)
    return tile


def make_scroll_wave(center, tile_width, amplitude, cycles, color, speed):
    tile = make_tile_segment(amplitude=amplitude, cycles=cycles, width=tile_width, color=color)
    group = VGroup(tile.copy(), tile.copy())
    group.arrange(RIGHT, buff=0)
    group.move_to(center)
    center_x = center[0]

    def updater(g, dt):
        g.shift(LEFT * speed * dt)
        if g.get_center()[0] < center_x - tile_width:
            g.shift(RIGHT * tile_width)

    group.add_updater(updater)
    return group


def make_headset():
    band = Arc(radius=0.42, start_angle=0, angle=PI, color=WHITE, stroke_width=3)
    band.shift(UP * 0.15)
    electrodes = VGroup(*[
        Dot(np.array([x, y, 0]), radius=0.04, color=GOLD)
        for x, y in [(-0.30, 0.38), (-0.12, 0.48), (0.10, 0.44), (0.28, 0.34)]
    ])
    box_rect = Rectangle(width=0.55, height=0.25, fill_color=BLUE, fill_opacity=1,
                         stroke_color=WHITE, stroke_width=1)
    box_rect.shift(DOWN * 0.35 + RIGHT * 0.10)
    wire = Line(band.get_end(), box_rect.get_top(), color=GREY_B, stroke_width=1)
    return VGroup(band, electrodes, box_rect, wire), box_rect


def make_house_icon():
    base = Rectangle(width=0.55, height=0.40, fill_color=ORANGE, fill_opacity=1,
                     stroke_color=WHITE, stroke_width=1)
    base.move_to(ORIGIN)
    roof = Polygon(
        base.get_corner(UL) + UP * 0.05,
        base.get_corner(UR) + UP * 0.05,
        base.get_top() + UP * 0.28,
        fill_color=ORANGE, fill_opacity=1, stroke_color=WHITE, stroke_width=1,
    )
    return VGroup(base, roof)


def make_lab_icon():
    building = Rectangle(width=0.55, height=0.42, fill_color=PURPLE, fill_opacity=1,
                         stroke_color=WHITE, stroke_width=1)
    building.move_to(ORIGIN + DOWN * 0.06)
    neck = Line(UP * 0.30, UP * 0.46, color=WHITE, stroke_width=1.5)
    bulb = Ellipse(width=0.24, height=0.30, fill_color=GREEN, fill_opacity=1,
                   stroke_color=WHITE, stroke_width=1)
    bulb.move_to(UP * 0.20)
    return VGroup(building, neck, bulb)


def make_magnifier():
    circle = Circle(radius=0.32, stroke_color=WHITE, stroke_width=4,
                    fill_color=BLUE, fill_opacity=0.20)
    handle = Line(
        circle.get_center() + RIGHT * 0.20 + DOWN * 0.20,
        circle.get_center() + RIGHT * 0.52 + DOWN * 0.52,
        color=WHITE, stroke_width=4,
    )
    return VGroup(circle, handle)


def make_event_marker():
    line = Line(DOWN * 0.45, UP * 0.50, color=RED, stroke_width=3)
    flag = Polygon(
        UP * 0.50,
        UP * 0.50 + RIGHT * 0.18,
        UP * 0.35 + RIGHT * 0.12,
        fill_color=RED, fill_opacity=1, stroke_width=0,
    )
    return VGroup(line, flag)


def make_burst_annotation():
    angles = np.linspace(0, TAU, 9, endpoint=False)
    lines = VGroup(*[
        Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * 0.16, color=YELLOW, stroke_width=2)
        for a in angles
    ])
    label = Text("milliseconds", font_size=14, color=GOLD)
    label.next_to(lines, RIGHT, buff=0.05)
    return VGroup(lines, label)


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        slot_centers = [
            np.array([-4.95, 0.35, 0]),
            np.array([-1.65, 0.35, 0]),
            np.array([1.65, 0.35, 0]),
            np.array([4.95, 0.35, 0]),
        ]

        # Title
        title_why = Text("Why EEG?", font_size=52, color=WHITE, t2c={"EEG": YELLOW})
        title_why.scale_to_fit_width(7)
        title_why.move_to(np.array([0, 3.0, 0]))

        # Four faint rounded icon slots
        slot_rects = []
        for center in slot_centers:
            rect = RoundedRectangle(
                corner_radius=0.18,
                width=2.8,
                height=2.6,
                stroke_color=GREY_B,
                stroke_width=2,
                fill_color=BLACK,
                fill_opacity=0.0,
            )
            rect.move_to(center)
            slot_rects.append(rect)
        slots_group = VGroup(*slot_rects)

        # Initial soft scrolling EEG waveform
        wave1 = make_scroll_wave(
            center=np.array([0, 0.1, 0]),
            tile_width=8.0,
            amplitude=0.4,
            cycles=4,
            color=TEAL,
            speed=1.2,
        )
        wave1.set_opacity(0.45)

        # Beat 1: scrolling waveform and title fade-in (0.00-3.90)
        self.add(wave1)
        self.wait(max(0.05, 0.6))
        self.play(FadeIn(title_why), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 1.9))

        # Beat 2: waveform fades out, slots fade in (3.90-5.50)
        self.play(FadeOut(wave1), FadeIn(slots_group), run_time=max(0.05, 1.6))
        wave1.clear_updaters()

        # Slot 1 content: head with electrode dots
        head_circle = Circle(radius=0.5, stroke_color=WHITE, stroke_width=2, fill_opacity=0)
        head_circle.move_to(slot_centers[0])
        electrode_dots = VGroup(*[
            Dot(head_circle.point_at_angle(angle), radius=0.04, color=GOLD)
            for angle in np.linspace(PI / 4, 3 * PI / 4, 7)
        ])
        head_group = VGroup(head_circle, electrode_dots)

        # Beat 3: first slot brightens, head appears (5.50-7.58)
        self.play(
            slot_rects[0].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.08),
            GrowFromCenter(head_group),
            run_time=max(0.05, 2.08),
        )

        # Beat 4: prohibited symbol and scalpel (7.58-11.82)
        red_circle = Circle(radius=0.42, stroke_color=RED, stroke_width=5,
                            fill_color=RED, fill_opacity=0.10)
        slash = Line(
            red_circle.point_at_angle(3 * PI / 4),
            red_circle.point_at_angle(-PI / 4),
            color=RED, stroke_width=5,
        )
        prohibit_group = VGroup(red_circle, slash)
        prohibit_group.move_to(np.array([slot_centers[0][0] + 0.65, slot_centers[0][1] + 0.10, 0]))

        scalpel_handle = Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12,
                              color=WHITE, stroke_width=3)
        scalpel_blade = Polygon(
            RIGHT * 0.12 + UP * 0.12,
            RIGHT * 0.23 + UP * 0.07,
            RIGHT * 0.08 + UP * 0.23,
            fill_color=WHITE, fill_opacity=1, stroke_color=WHITE, stroke_width=0.5,
        )
        scalpel = VGroup(scalpel_handle, scalpel_blade).scale_to_fit_height(0.30)
        scalpel.move_to(red_circle.get_center())

        self.play(GrowFromCenter(prohibit_group), FadeIn(scalpel), run_time=max(0.05, 1.5))
        self.play(FadeOut(scalpel), run_time=max(0.05, 0.7))
        self.play(prohibit_group.animate.scale(1.12), run_time=max(0.05, 0.4))
        self.play(prohibit_group.animate.scale(1 / 1.12).set_color(GREY_B), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.14))

        # Beat 5: first slot dims slightly (11.82-12.74)
        self.play(
            slot_rects[0].animate.set_stroke(GREY_B, 2).set_fill(BLACK, 0),
            head_group.animate.set_opacity(0.85),
            run_time=max(0.05, 0.92),
        )

        # Slot 2: timeline and temporal resolution
        axis_line = Line(LEFT * 0.95, RIGHT * 0.95, color=WHITE, stroke_width=2)
        tick_xs = np.linspace(-0.95, 0.95, 7)
        ticks = VGroup(*[
            Line(np.array([x, -0.04, 0]), np.array([x, 0.04, 0]),
                 color=WHITE, stroke_width=2)
            for x in tick_xs
        ])
        timeline_group = VGroup(axis_line, ticks)
        timeline_group.move_to(slot_centers[1] + DOWN * 0.15)

        temporal_label = Text("temporal resolution", font_size=20, color=WHITE)
        temporal_label.scale_to_fit_width(2.0)
        temporal_label.next_to(slot_rects[1], DOWN, buff=0.15)

        # Beat 6: second slot brightens, timeline appears (12.74-14.46)
        self.play(
            slot_rects[1].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.08),
            FadeIn(timeline_group),
            FadeIn(temporal_label),
            run_time=max(0.05, 1.72),
        )

        # Beat 7: tick flashing and ms label (14.46-16.06)
        ms_label = Text("ms", font_size=20, color=GOLD)
        ms_label.next_to(timeline_group, LEFT, buff=0.15)

        self.play(FadeIn(ms_label), run_time=max(0.05, 0.2))
        flash_durations = [0.22, 0.20, 0.18, 0.16, 0.14, 0.12, 0.10]
        for tick, dur in zip(ticks, flash_durations):
            self.play(tick.animate.set_stroke(YELLOW, width=4), run_time=max(0.05, dur / 2))
            self.play(tick.animate.set_stroke(WHITE, width=2), run_time=max(0.05, dur / 2))
        self.wait(max(0.05, 0.28))

        # Beat 8: magnifier sweep and burst annotation (16.06-19.74)
        magnifier = make_magnifier()
        magnifier.move_to(slot_centers[1] + LEFT * 1.9 + UP * 0.30)
        target_pos = timeline_group.get_center() + RIGHT * 0.05 + UP * 0.25
        burst_ann = make_burst_annotation()
        burst_ann.move_to(np.array([target_pos[0], target_pos[1] - 0.25, 0]))

        self.add(magnifier)
        self.play(magnifier.animate.move_to(target_pos), run_time=max(0.05, 1.4))
        self.play(ticks[3].animate.scale(1.5), ticks[4].animate.scale(1.5), run_time=max(0.05, 0.8))
        self.play(FadeIn(burst_ann), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.98))

        # Slot 2: waveform plus brain icon
        wave2_xs = np.linspace(-1.0, 1.0, 160)
        phase_tracker = ValueTracker(0)

        def wave2_points(phase):
            return [
                np.array([x, 0.19 * np.sin(2 * PI * 9 * x / 2.0 + phase), 0])
                for x in wave2_xs
            ]

        wave2 = VMobject()
        wave2.set_points_as_corners(wave2_points(0))
        wave2.set_stroke(TEAL, width=2.5)
        wave2.set_fill(opacity=0)
        wave2.move_to(np.array([slot_centers[1][0], slot_centers[1][1] - 0.25, 0]))
        wave2.add_updater(lambda m: m.set_points_as_corners(wave2_points(phase_tracker.get_value())))

        brain_icon = SVGMobject(ASSET_PATHS["brain"])
        brain_icon.set_color(PURPLE)
        brain_icon.set_fill(PURPLE, opacity=0.9)
        brain_icon.set_stroke(WHITE, width=1)
        brain_icon.scale_to_fit_height(0.60)
        brain_icon.move_to(np.array([slot_centers[1][0], slot_centers[1][1] + 0.55, 0]))
        brain_base_height = 0.60
        brain_icon.add_updater(
            lambda m: m.scale_to_fit_height(brain_base_height * (1 + 0.12 * np.sin(phase_tracker.get_value())))
        )

        # Beat 9: timeline shifts to waveform, brain pulses, second slot dims (19.74-24.86)
        self.play(FadeOut(magnifier), FadeOut(burst_ann), run_time=max(0.05, 0.6))
        self.play(FadeOut(timeline_group), FadeOut(ms_label), FadeIn(wave2), run_time=max(0.05, 0.8))
        self.play(FadeIn(brain_icon), run_time=max(0.05, 0.5))
        self.play(phase_tracker.animate.set_value(4 * PI), run_time=max(0.05, 2.4))
        self.wait(max(0.05, 0.32))
        self.play(slot_rects[1].animate.set_stroke(GREY_B, 2).set_fill(BLACK, 0), run_time=max(0.05, 0.5))

        # Beat 10: hold second slot (24.86-25.84)
        self.wait(max(0.05, 0.98))

        # Slot 3: affordability and portability
        dollar = Text("$", font_size=64, color=GREEN)
        dollar.move_to(np.array([slot_centers[2][0], slot_centers[2][1] + 0.70, 0]))
        affordable_text = Text("relatively affordable", font_size=18, color=WHITE)
        affordable_text.scale_to_fit_width(2.2)
        affordable_text.next_to(dollar, DOWN, buff=0.10)

        # Beat 11: third slot brightens, dollar sign appears (25.84-28.02)
        self.play(
            slot_rects[2].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.08),
            FadeIn(dollar),
            run_time=max(0.05, 0.9),
        )
        self.play(FadeIn(affordable_text), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.2))
        self.play(FadeOut(affordable_text), run_time=max(0.05, 0.58))

        headset_group, recording_box = make_headset()
        headset_group.scale_to_fit_width(1.05)
        headset_group.move_to(np.array([slot_centers[2][0] + 0.65, slot_centers[2][1] + 0.35, 0]))

        stopwatch_icon = SVGMobject(ASSET_PATHS["stopwatch"])
        stopwatch_icon.set_color(WHITE)
        stopwatch_icon.scale_to_fit_height(0.55)
        arrow_repeat_icon = SVGMobject(ASSET_PATHS["arrow_repeat"])
        arrow_repeat_icon.set_color(ORANGE)
        arrow_repeat_icon.scale_to_fit_height(0.38)
        arrow_repeat_icon.next_to(stopwatch_icon, RIGHT, buff=0.08)
        clock_group = VGroup(stopwatch_icon, arrow_repeat_icon)
        clock_group.move_to(np.array([slot_centers[2][0] + 0.85, slot_centers[2][1] - 0.15, 0]))

        # Beat 12: headset, clock, and duration arrow (28.02-31.24)
        self.play(dollar.animate.shift(LEFT * 0.7), run_time=max(0.05, 0.8))
        self.play(FadeIn(headset_group), run_time=max(0.05, 0.8))
        self.play(FadeIn(clock_group), run_time=max(0.05, 0.6))
        self.play(
            arrow_repeat_icon.animate.rotate(TAU, about_point=arrow_repeat_icon.get_center()),
            run_time=max(0.05, 1.02),
        )

        house_icon = make_house_icon()
        house_icon.scale_to_fit_width(0.55)
        house_icon.move_to(np.array([slot_centers[2][0] + 0.65, slot_centers[2][1] - 0.95, 0]))
        box_to_house_line = Line(recording_box.get_bottom(), house_icon.get_top(),
                                 color=GREY_B, stroke_width=1)
        portable_text = Text("portable", font_size=16, color=GOLD)
        portable_text.next_to(headset_group, DOWN, buff=0.10)
        long_duration_text = Text("long-duration", font_size=16, color=GOLD)
        long_duration_text.move_to(clock_group.get_center() + DOWN * 0.12)

        # Beat 13: house icon, home-use connection, short labels (31.24-34.62)
        self.play(FadeOut(clock_group), run_time=max(0.05, 0.6))
        self.play(FadeIn(house_icon), FadeIn(box_to_house_line), run_time=max(0.05, 0.8))
        self.play(FadeIn(portable_text), run_time=max(0.05, 0.45))
        self.play(FadeIn(long_duration_text), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.40))
        self.play(FadeOut(portable_text), FadeOut(long_duration_text), run_time=max(0.05, 0.68))

        hospital_icon = SVGMobject(ASSET_PATHS["hospital"])
        hospital_icon.set_color(BLUE)
        hospital_icon.scale_to_fit_height(0.60)
        hospital_icon.move_to(np.array([slot_centers[2][0] - 0.65, slot_centers[2][1] - 0.95, 0]))
        lab_icon = make_lab_icon()
        lab_icon.scale_to_fit_width(0.55)
        lab_icon.move_to(np.array([slot_centers[2][0], slot_centers[2][1] - 0.95, 0]))

        # Beat 14: three building icons and glow sequence (34.62-38.00)
        self.play(FadeIn(hospital_icon), FadeIn(lab_icon), run_time=max(0.05, 0.7))
        self.play(Indicate(hospital_icon, color=YELLOW), run_time=max(0.05, 0.55))
        self.play(Indicate(lab_icon, color=YELLOW), run_time=max(0.05, 0.55))
        self.play(Indicate(house_icon, color=YELLOW), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 0.48))
        self.play(slot_rects[2].animate.set_stroke(GREY_B, 2).set_fill(BLACK, 0), run_time=max(0.05, 0.55))

        # Beat 15: hold third slot (38.00-39.00)
        self.wait(max(0.05, 1.0))

        # Slot 4: continuous recording
        wave4_group = make_scroll_wave(
            center=np.array([slot_centers[3][0], slot_centers[3][1] - 0.15, 0]),
            tile_width=1.4,
            amplitude=0.22,
            cycles=3,
            color=TEAL,
            speed=0.8,
        )
        continuous_label = Text("continuous recording", font_size=20, color=WHITE)
        continuous_label.scale_to_fit_width(2.4)
        continuous_label.next_to(slot_rects[3], DOWN, buff=0.15)

        # Beat 16: fourth slot brightens, continuous waveform appears (39.00-43.72)
        self.play(
            slot_rects[3].animate.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.08),
            FadeIn(wave4_group),
            FadeIn(continuous_label),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, 3.52))

        marker1 = make_event_marker()
        marker1.move_to(np.array([slot_centers[3][0] - 0.7, slot_centers[3][1] + 0.05, 0]))
        marker2 = make_event_marker()
        marker2.move_to(np.array([slot_centers[3][0] + 0.7, slot_centers[3][1] + 0.05, 0]))
        spontaneous_label = Text("spontaneous", font_size=16, color=GOLD)
        spontaneous_label.next_to(marker1, UP, buff=0.06)
        event_label = Text("event-related", font_size=16, color=GOLD)
        event_label.next_to(marker2, UP, buff=0.06)

        # Beat 17: event markers and spontaneous/event-related labels (43.72-50.10)
        self.play(FadeIn(marker1), run_time=max(0.05, 0.55))
        self.play(FadeIn(spontaneous_label), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.55))
        self.play(FadeOut(spontaneous_label), run_time=max(0.05, 0.40))
        self.play(FadeOut(marker1), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 1.28))
        self.play(FadeIn(marker2), run_time=max(0.05, 0.55))
        self.play(FadeIn(event_label), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.65))
        self.play(FadeOut(event_label), run_time=max(0.05, 0.40))
        self.play(FadeOut(marker2), run_time=max(0.05, 0.45))
        self.wait(max(0.05, 0.20))

        # Beat 18: all slots brighten, lift, title changes (50.10-53.04)
        title_adv = Text("Advantages of EEG", font_size=52, color=WHITE, weight="BOLD", t2c={"EEG": YELLOW})
        title_adv.scale_to_fit_width(8)
        title_adv.move_to(title_why.get_center())

        lift_group = VGroup(
            slots_group,
            head_group,
            wave2,
            brain_icon,
            temporal_label,
            headset_group,
            dollar,
            hospital_icon,
            lab_icon,
            house_icon,
            wave4_group,
            continuous_label,
        )

        self.play(
            FadeOut(title_why),
            FadeIn(title_adv),
            lift_group.animate.shift(UP * 0.30),
            run_time=max(0.05, 1.2),
        )
        self.play(
            *[rect.animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.10) for rect in slot_rects],
            run_time=max(0.05, 0.8),
        )
        self.wait(max(0.05, 0.94))

        # Beat 19: subtitle fades in, four icons pulse left to right (53.04-58.16)
        techniques_text = Text("most commonly used neural recording techniques", font_size=28, color=WHITE)
        techniques_text.scale_to_fit_width(10)
        techniques_text.move_to(np.array([0, -2.55, 0]))

        self.play(FadeIn(techniques_text), run_time=max(0.05, 0.8))

        slot1_visual = head_group
        slot2_visual = VGroup(wave2, brain_icon)
        slot3_visual = VGroup(dollar, headset_group, hospital_icon, lab_icon, house_icon)
        slot4_visual = wave4_group
        slot_visuals = [slot1_visual, slot2_visual, slot3_visual, slot4_visual]

        for visual in slot_visuals:
            self.play(visual.animate.scale(1.08), run_time=max(0.05, 0.3))
            self.play(visual.animate.scale(1 / 1.08), run_time=max(0.05, 0.3))

        self.wait(max(0.05, 1.92))

        # Beat 20: small bottom waveform scrolls, hold final composition (58.16-61.75)
        bottom_wave = make_scroll_wave(
            center=np.array([0, -3.15, 0]),
            tile_width=8.0,
            amplitude=0.25,
            cycles=6,
            color=TEAL,
            speed=1.1,
        )

        self.play(FadeIn(bottom_wave), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 2.59))