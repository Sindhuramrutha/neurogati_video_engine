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

import numpy as np
from manim import *


def make_tile_segment(amplitude=0.4, cycles=4, width=8.0, color=TEAL):
    xs = np.linspace(0, width, 120)
    ys = amplitude * np.sin(2 * PI * cycles * xs / width)
    pts = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
    tile = VMobject()
    tile.set_points_as_corners(pts)
    tile.set_stroke(color, width=2)
    tile.set_fill(opacity=0)
    return tile


def make_wavy_connector(start, end, color, amp=0.25, cycles=4):
    start = np.array(start)
    end = np.array(end)
    d = end - start
    length = np.linalg.norm(d)
    if length < 1e-9:
        length = 1e-9
    unit = d / length
    perp = np.array([-unit[1], unit[0], 0])

    n = 60
    ts = np.linspace(0, 1, n)
    taper = np.sin(PI * ts)
    offsets = amp * taper * np.sin(2 * PI * cycles * ts)

    pts = []
    for i in range(n):
        pts.append(start + unit * (ts[i] * length) + perp * offsets[i])

    conn = VMobject()
    conn.set_points_as_corners(pts)
    conn.set_stroke(color, width=2)
    conn.set_fill(opacity=0)
    return conn


def make_card(label, color):
    rect = Rectangle(width=3.6, height=1.4, stroke_color=color, stroke_width=2.5)
    rect.set_fill(color, opacity=0.0)
    txt = Text(label, font_size=24, color=WHITE, weight="SEMIBOLD")
    txt.scale_to_fit_width(rect.width - 0.35)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt), rect


def make_chart_icon():
    axes = VGroup(
        Line(LEFT * 0.6 + DOWN * 0.15, RIGHT * 0.6 + DOWN * 0.15, color=WHITE, stroke_width=2),
        Line(LEFT * 0.6 + DOWN * 0.15, LEFT * 0.6 + UP * 0.55, color=WHITE, stroke_width=2),
    )
    xs = np.linspace(-0.5, 0.5, 40)
    ys = 0.25 * np.sin(2 * PI * 2 * xs)
    wave = VMobject()
    wave.set_points_as_corners([np.array([x, y - 0.1, 0]) for x, y in zip(xs, ys)])
    wave.set_stroke(TEAL, width=2)
    wave.set_fill(opacity=0)
    return VGroup(axes, wave)


def make_clip_icon():
    panel = Rectangle(width=1.2, height=0.9, fill_color=DARK_GREY, fill_opacity=0.9,
                      stroke_color=WHITE, stroke_width=1.5)
    pulse_pts = [
        np.array([-0.40, -0.22, 0]),
        np.array([-0.15, -0.22, 0]),
        np.array([-0.05, 0.30, 0]),
        np.array([0.05, 0.30, 0]),
        np.array([0.20, -0.22, 0]),
        np.array([0.40, 0.18, 0]),
    ]
    pulse = VMobject()
    pulse.set_points_as_corners(pulse_pts)
    pulse.set_stroke(TEAL, width=2)
    pulse.set_fill(opacity=0)
    pulse.move_to(panel.get_center())
    return VGroup(panel, pulse)


def make_bci_figure():
    head = Circle(radius=0.15, stroke_color=WHITE, stroke_width=2, fill_opacity=0)
    head.move_to(ORIGIN + UP * 0.25)
    body = Line(ORIGIN + UP * 0.10, ORIGIN + DOWN * 0.30, color=WHITE, stroke_width=2)
    arms = Line(LEFT * 0.25, RIGHT * 0.25, color=WHITE, stroke_width=2).shift(DOWN * 0.05)
    left_leg = Line(ORIGIN + DOWN * 0.30, LEFT * 0.20 + DOWN * 0.60, color=WHITE, stroke_width=2)
    right_leg = Line(ORIGIN + DOWN * 0.30, RIGHT * 0.20 + DOWN * 0.60, color=WHITE, stroke_width=2)
    person = VGroup(head, body, arms, left_leg, right_leg)
    cursor = Arrow(
        start=head.get_right() + RIGHT * 0.15 + UP * 0.10,
        end=head.get_right() + RIGHT * 0.50 + UP * 0.25,
        buff=0,
        color=YELLOW,
        stroke_width=2,
        max_tip_length_to_length_ratio=0.3,
    )
    return VGroup(person, cursor)


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Beat durations
        b1 = 2.74
        b2 = 2.88
        b3 = 3.00
        b4 = 5.20
        b5 = 3.74
        b6 = 3.76
        b7 = 4.92
        b8 = 6.52
        b9 = 4.10
        b10 = 5.54
        b11 = 4.52
        b12 = 7.24
        b13 = 4.58
        b14 = 6.44
        b15 = 3.90
        b16 = 7.62

        card_labels = {
            "brain_states": "Brain States",
            "sleep": "Sleep Staging",
            "epilepsy": "Epilepsy",
            "bci": "Brain-Computer Interfaces",
        }
        card_colors = {
            "brain_states": BLUE,
            "sleep": PURPLE,
            "epilepsy": ORANGE,
            "bci": TEAL,
        }
        card_order = ["brain_states", "sleep", "epilepsy", "bci"]

        final_centers = {
            "brain_states": np.array([-4.0, 1.55, 0]),
            "sleep": np.array([4.0, 1.55, 0]),
            "epilepsy": np.array([-4.0, -1.55, 0]),
            "bci": np.array([4.0, -1.55, 0]),
        }
        initial_centers = {name: center * 1.10 for name, center in final_centers.items()}

        # Continuous background EEG waveform
        tile_width = 8.0
        base_tile = make_tile_segment(amplitude=0.38, cycles=4, width=tile_width, color=TEAL)
        wave = VGroup(base_tile.copy(), base_tile.copy())
        wave.arrange(RIGHT, buff=0)
        wave.move_to(ORIGIN)
        wave.set_stroke(TEAL, width=2)
        wave.set_fill(opacity=0)
        wave.set_opacity(0)
        wave.set_z_index(-10)

        wave_speed = ValueTracker(1.50)

        def update_wave(g, dt):
            step = wave_speed.get_value() * dt
            g.shift(LEFT * step)
            if g.get_center()[0] < -tile_width:
                g.shift(RIGHT * tile_width)

        wave.add_updater(update_wave)

        # Brain icon with electrode dots
        brain_icon = SVGMobject(ASSET_PATHS["brain"])
        brain_icon.set_color(WHITE)
        brain_icon.set_fill(opacity=0)
        brain_icon.set_stroke(WHITE, width=2)
        brain_icon.scale_to_fit_height(2.3)
        brain_icon.move_to(ORIGIN)

        top_y = brain_icon.get_top()[1]
        dot_xs = [-0.75, -0.38, 0.0, 0.38, 0.75]
        dot_ys = [top_y - 0.55, top_y - 0.22, top_y - 0.15, top_y - 0.22, top_y - 0.55]
        electrode_dots = VGroup(
            *[Dot(np.array([x, y, 0]), radius=0.045, color=GOLD) for x, y in zip(dot_xs, dot_ys)]
        )
        brain_group = VGroup(brain_icon, electrode_dots)

        brain_halo = Circle(radius=1.75, fill_color=PURPLE, fill_opacity=0.08, stroke_width=0)
        brain_halo.move_to(brain_icon.get_center())
        brain_halo.set_z_index(-1)

        title = Text("Applications of EEG", font_size=56, color=WHITE, t2c={"EEG": YELLOW})
        title.scale_to_fit_width(8.2)
        title.move_to(np.array([0, -2.55, 0]))

        # Cards
        card_groups = {}
        card_rects = {}
        for name in card_order:
            group, rect = make_card(card_labels[name], card_colors[name])
            group.move_to(initial_centers[name])
            card_groups[name] = group
            card_rects[name] = rect

        cards_vgroup = VGroup(*[card_groups[name] for name in card_order])

        # Beat 1: title screen fade-in with brain and scrolling waveform
        self.add(brain_halo, wave)
        self.play(
            wave.animate.set_opacity(0.45),
            Write(brain_group),
            run_time=max(0.05, b1),
        )

        # Beat 2: waveform slows to a steady pace
        self.play(wave_speed.animate.set_value(1.0), run_time=max(0.05, b2))

        # Beat 3: title fades in beneath brain
        self.play(Write(title), run_time=max(0.05, b3))

        # Beat 4: title moves up and first card appears
        self.play(title.animate.to_edge(UP, buff=0.35), run_time=max(0.05, 1.2))
        self.play(GrowFromCenter(card_groups["brain_states"]), run_time=max(0.05, 1.6))
        self.wait(max(0.05, b4 - 2.8))

        # Beat 5: remaining cards fade in one at a time
        per_card_5 = b5 / 3
        anim_5 = max(0.05, 0.8)
        wait_5 = max(0.05, per_card_5 - anim_5)
        for name in ["sleep", "epilepsy", "bci"]:
            self.play(FadeIn(card_groups[name]), run_time=max(0.05, anim_5))
            self.wait(max(0.05, wait_5))

        # Beat 6: cards settle, wave connectors appear
        self.play(
            *[card_groups[name].animate.move_to(final_centers[name]) for name in card_order],
            run_time=max(0.05, 1.6),
        )

        connectors = []
        for name in card_order:
            center = card_groups[name].get_center()
            direction = center - brain_group.get_center()
            direction /= np.linalg.norm(direction)
            start = brain_group.get_center() + direction * 1.45
            end = center - direction * 2.05
            connectors.append(make_wavy_connector(start, end, card_colors[name], amp=0.22, cycles=4))

        connectors_group = VGroup(*connectors)
        connectors_group.set_z_index(0)
        self.play(Create(connectors_group), run_time=max(0.05, b6 - 1.6))

        main_comp = VGroup(
            brain_halo,
            brain_group,
            title,
            cards_vgroup,
            connectors_group,
        )

        # Beat 7: brain pulse once, then waveform lines brighten in sequence
        self.play(
            brain_halo.animate.scale(1.15).set_fill(PURPLE, 0.28),
            brain_group.animate.scale(1.04),
            run_time=max(0.05, 1.0),
        )
        self.play(
            brain_halo.animate.scale(1 / 1.15).set_fill(PURPLE, 0.08),
            brain_group.animate.scale(1 / 1.04),
            run_time=max(0.05, 1.0),
        )

        per_connector_7 = (b7 - 2.0) / 4
        half_7 = max(0.05, per_connector_7 / 2)
        for i, conn in enumerate(connectors):
            self.play(conn.animate.set_stroke(WHITE, width=5), run_time=max(0.05, half_7))
            self.play(conn.animate.set_stroke(card_colors[card_order[i]], width=2), run_time=max(0.05, half_7))

        # Beat 8: zoom-in panel on waveform plus inset brain with highlighted cortex
        zoom_panel = Rectangle(width=6.4, height=2.7, fill_color=DARK_GREY, fill_opacity=0.95,
                               stroke_color=WHITE, stroke_width=1.5)
        zoom_panel.move_to(np.array([0, 0.9, 0]))

        xs_zoom = np.linspace(-2.8, 2.8, 150)
        ys_zoom = 0.38 * np.sin(2 * PI * 6 * xs_zoom / 5.6) + 0.14 * np.sin(2 * PI * 14 * xs_zoom / 5.6)
        zoom_wave = VMobject()
        zoom_wave.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs_zoom, ys_zoom)])
        zoom_wave.set_stroke(YELLOW, width=3)
        zoom_wave.set_fill(opacity=0)
        zoom_wave.move_to(zoom_panel.get_center())

        inset_panel = Rectangle(width=1.5, height=1.1, fill_color=DARK_GREY, fill_opacity=0.95,
                                stroke_color=WHITE, stroke_width=1)
        inset_panel.move_to(np.array([3.6, -1.4, 0]))

        inset_brain = brain_icon.copy()
        inset_brain.set_fill(opacity=0)
        inset_brain.set_stroke(WHITE, width=1.2)
        inset_brain.scale(0.32)
        inset_brain.move_to(inset_panel.get_center() + LEFT * 0.05)

        inset_highlight = Ellipse(width=0.34, height=0.50, fill_color=PINK, fill_opacity=0.35,
                                  stroke_color=PINK, stroke_width=1)
        inset_highlight.move_to(inset_brain.get_top() + DOWN * 0.15)

        inset_brain_group = VGroup(inset_panel, inset_brain, inset_highlight)

        zoom_panel_group = VGroup(zoom_panel, zoom_wave)

        self.play(main_comp.animate.set_opacity(0.12), run_time=max(0.05, 1.5))
        self.play(FadeIn(zoom_panel_group), run_time=max(0.05, 1.2))
        self.play(FadeIn(inset_brain_group), run_time=max(0.05, 1.0))
        self.wait(max(0.05, b8 - 3.7))

        # Beat 9: return to main composition, cortex highlight fades, dynamic activity continues
        self.play(
            main_comp.animate.set_opacity(1.0),
            FadeOut(zoom_panel_group),
            FadeOut(inset_brain_group),
            run_time=max(0.05, 2.0),
        )
        self.play(brain_halo.animate.set_fill(PURPLE, 0.35), run_time=max(0.05, 0.7))
        self.play(brain_halo.animate.set_fill(PURPLE, 0.08), run_time=max(0.05, 0.8))
        self.wait(max(0.05, b9 - 3.5))

        # Beat 10: Brain States card pulses, connection brightens, other cards dim
        self.play(
            card_groups["brain_states"].animate.scale(1.06),
            card_rects["brain_states"].animate.set_stroke(YELLOW, width=4),
            run_time=max(0.05, 0.8),
        )
        self.play(
            card_groups["brain_states"].animate.scale(1 / 1.06),
            card_rects["brain_states"].animate.set_stroke(card_colors["brain_states"], width=2.5),
            run_time=max(0.05, 0.8),
        )
        self.play(
            connectors[0].animate.set_stroke(YELLOW, width=4),
            card_groups["sleep"].animate.set_opacity(0.30),
            card_groups["epilepsy"].animate.set_opacity(0.30),
            card_groups["bci"].animate.set_opacity(0.30),
            run_time=max(0.05, 1.2),
        )
        self.wait(max(0.05, b10 - 2.8))

        # Beat 11: two visual lanes with chart and clinical clip icons
        chart_icon = make_chart_icon().scale_to_fit_width(1.0)
        chart_icon.move_to(card_groups["brain_states"].get_top() + UP * 0.25)

        clip_icon = make_clip_icon().scale_to_fit_width(1.0)
        clip_icon.move_to(card_groups["epilepsy"].get_top() + UP * 0.25)

        divider = Line(UP * 3.2, DOWN * 3.2, color=GREY_B, stroke_width=1, stroke_opacity=0.5)

        self.play(
            FadeIn(divider),
            FadeIn(chart_icon),
            FadeIn(clip_icon),
            card_groups["sleep"].animate.set_opacity(0.15),
            card_groups["bci"].animate.set_opacity(0.15),
            card_groups["epilepsy"].animate.set_opacity(1.0),
            run_time=max(0.05, 2.0),
        )
        self.wait(max(0.05, b11 - 2.0))

        # Beat 12: merge back; BCI helper figure appears
        bci_figure = make_bci_figure().scale_to_fit_height(0.7)
        bci_figure.next_to(card_groups["bci"], UP, buff=0.12)

        self.play(
            FadeOut(divider),
            FadeOut(chart_icon),
            FadeOut(clip_icon),
            card_groups["sleep"].animate.set_opacity(1.0),
            card_groups["bci"].animate.set_opacity(1.0),
            run_time=max(0.05, 2.0),
        )
        self.play(FadeIn(bci_figure), run_time=max(0.05, 1.0))
        self.wait(max(0.05, b12 - 3.0))

        # Beat 13: cards lift and brighten; label appears and fades
        self.play(
            main_comp.animate.shift(UP * 0.12),
            *[card_rects[name].animate.set_stroke(card_colors[name], width=4) for name in card_order],
            run_time=max(0.05, 1.2),
        )
        self.play(*[conn.animate.set_stroke(WHITE, width=5) for conn in connectors], run_time=max(0.05, 0.5))
        self.play(*[conn.animate.set_stroke(card_colors[name], width=2)
                    for name, conn in zip(card_order, connectors)], run_time=max(0.05, 0.5))

        four_areas_label = Text("four major application areas", font_size=28, color=GOLD)
        four_areas_label.move_to(np.array([0, -3.1, 0]))
        self.play(FadeIn(four_areas_label), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.6))
        self.play(FadeOut(four_areas_label), run_time=max(0.05, 0.98))

        # Beat 14: focus moves card by card
        focus_rect = Rectangle(width=3.8, height=1.6, stroke_color=YELLOW, stroke_width=4)
        focus_rect.move_to(card_groups[card_order[0]].get_center())
        self.add(focus_rect)

        per_card_14 = b14 / 4
        anim_14 = max(0.05, 0.8)
        wait_14 = max(0.05, per_card_14 - anim_14)
        for name in card_order:
            others = [o for o in card_order if o != name]
            self.play(
                focus_rect.animate.move_to(card_groups[name].get_center()),
                card_groups[name].animate.set_opacity(1.0),
                *[card_groups[o].animate.set_opacity(0.25) for o in others],
                run_time=max(0.05, anim_14),
            )
            self.wait(max(0.05, wait_14))

        # Beat 15: all cards equal; connectors straighten and pulse in common rhythm
        straight_connectors = []
        for name in card_order:
            center = card_groups[name].get_center()
            direction = center - brain_group.get_center()
            direction /= np.linalg.norm(direction)
            start = brain_group.get_center() + direction * 1.45
            end = center - direction * 2.05
            straight_connectors.append(Line(start, end).set_stroke(card_colors[name], width=3))

        self.play(
            FadeOut(focus_rect),
            *[card_groups[name].animate.set_opacity(1.0) for name in card_order],
            *[Transform(conn, straight) for conn, straight in zip(connectors, straight_connectors)],
            run_time=max(0.05, 2.2),
        )
        self.play(*[conn.animate.set_stroke(WHITE, width=5) for conn in connectors], run_time=max(0.05, 0.6))
        self.play(*[conn.animate.set_stroke(card_colors[name], width=3)
                    for name, conn in zip(card_order, connectors)], run_time=max(0.05, 0.6))
        self.wait(max(0.05, b15 - 3.4))

        # Beat 16: final loop, brain glow, title returns at bottom, hold
        for i, conn in enumerate(connectors):
            self.play(conn.animate.set_stroke(WHITE, width=6), run_time=max(0.05, 0.3))
            self.play(conn.animate.set_stroke(card_colors[card_order[i]], width=3), run_time=max(0.05, 0.3))

        self.play(brain_halo.animate.set_fill(PURPLE, 0.30), run_time=max(0.05, 0.7))
        self.play(brain_halo.animate.set_fill(PURPLE, 0.08), run_time=max(0.05, 0.8))

        title.scale_to_fit_width(6.0)
        title.move_to(np.array([0, -3.1, 0]))
        self.play(title.animate.set_opacity(1.0), run_time=max(0.05, 0.9))
        self.wait(max(0.05, b16 - 4.8))