ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene8(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        TOTAL = 54.17
        elapsed = 0.0

        # ---------- Beat 1: title + summary band-pass diagram ----------
        title = Text("Band-Pass Filter — Summary", font_size=52, color=WHITE).to_edge(
            UP, buff=0.3
        )
        subtitle = Text(
            "Keeps a selected band; attenuates everything else",
            font_size=26,
            color=GREY,
        ).next_to(title, DOWN, buff=0.18)

        left_rect = Rectangle(
            width=2.3,
            height=1.8,
            fill_color=RED,
            fill_opacity=0.45,
            stroke_color=RED,
            stroke_width=2,
        )
        mid_rect = Rectangle(
            width=4.2,
            height=2.25,
            fill_color=GREEN,
            fill_opacity=0.8,
            stroke_color=GREEN,
            stroke_width=2,
        )
        right_rect = Rectangle(
            width=4.2,
            height=1.8,
            fill_color=RED,
            fill_opacity=0.45,
            stroke_color=RED,
            stroke_width=2,
        )
        regions = VGroup(left_rect, mid_rect, right_rect).arrange(RIGHT, buff=0)
        left_rect.align_to(mid_rect, DOWN)
        right_rect.align_to(mid_rect, DOWN)

        left_in = Text("< 1 Hz", font_size=26, color=WHITE).move_to(left_rect)
        mid_in = VGroup(
            Text("1 – 40 Hz", font_size=32, color=WHITE),
            Text("preserved", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.12)
        mid_in.move_to(mid_rect)
        right_in = Text("> 40 Hz", font_size=26, color=WHITE).move_to(right_rect)

        under_left = Text("attenuated", font_size=20, color=RED).next_to(
            left_rect, DOWN, buff=0.15
        )
        under_mid = Text("passband", font_size=22, color=GREEN).next_to(
            mid_rect, DOWN, buff=0.15
        )
        under_right = Text("attenuated", font_size=20, color=RED).next_to(
            right_rect, DOWN, buff=0.15
        )

        main_diagram = VGroup(
            regions,
            VGroup(left_in, mid_in, right_in),
            VGroup(under_left, under_mid, under_right),
        )
        main_diagram.scale_to_fit_width(11)
        main_diagram.move_to(ORIGIN)

        self.play(Write(title), FadeIn(subtitle), run_time=max(0.05, 1.0))
        elapsed += 1.0
        self.play(GrowFromCenter(main_diagram), run_time=max(0.05, 2.0))
        elapsed += 2.0
        self.wait(max(0.05, 3.0))
        elapsed += 3.0

        # ---------- Beat 2: applications row ----------
        apps_title = Text(
            "Common preprocessing in neural signal processing",
            font_size=24,
            color=GREY,
        )

        def make_app_badge(abbrev, label, color):
            circle = Circle(radius=0.45, fill_color=color, fill_opacity=0.9,
                            stroke_color=WHITE, stroke_width=1.5)
            abbrev_text = Text(abbrev, font_size=20, color=WHITE).move_to(circle)
            label_text = Text(label, font_size=20, color=WHITE)
            return VGroup(circle, abbrev_text, label_text).arrange(DOWN, buff=0.15)

        app_items = [
            make_app_badge("EEG", "EEG", BLUE),
            make_app_badge("EMG", "EMG", ORANGE),
            make_app_badge("LFP", "LFP", TEAL),
            make_app_badge("BCI", "BCI", PURPLE),
        ]
        apps_row = VGroup(*app_items).arrange(RIGHT, buff=0.9)
        apps_row.scale_to_fit_width(9.6)
        apps_group = VGroup(apps_title, apps_row).arrange(DOWN, buff=0.25)
        apps_group.next_to(main_diagram, DOWN, buff=0.45)

        self.play(FadeIn(apps_group, shift=UP * 0.4), run_time=max(0.05, 2.5))
        elapsed += 2.5
        self.wait(max(0.05, 5.5))
        elapsed += 5.5

        # ---------- Beat 3: recap + passband pulse ----------
        recap = Text(
            "Only the selected middle band is preserved",
            font_size=28,
            color=YELLOW,
        )
        recap.next_to(main_diagram, UP, buff=0.35)

        self.play(FadeIn(recap), run_time=max(0.05, 1.5))
        elapsed += 1.5
        self.play(Indicate(mid_rect, scale_factor=1.05, color=GREEN), run_time=max(0.05, 1.2))
        elapsed += 1.2
        self.wait(max(0.05, 3.3))
        elapsed += 3.3

        # ---------- Beat 4: transition to one specific frequency ----------
        self.play(FadeOut(apps_group, recap), run_time=max(0.05, 1.0))
        elapsed += 1.0
        self.play(FadeOut(main_diagram, title, subtitle), run_time=max(0.05, 1.2))
        elapsed += 1.2

        trans_title = Text(
            "Sometimes interference is one exact frequency",
            font_size=42,
            color=YELLOW,
        ).to_edge(UP, buff=0.45)
        trans_title.scale_to_fit_width(11.5)
        trans_sub = Text(
            "Power-line interference at 50 or 60 Hz",
            font_size=26,
            color=GREY,
        ).next_to(trans_title, DOWN, buff=0.2)

        spike_axis = Line(LEFT * 5.2, RIGHT * 5.2, color=GREY, stroke_width=2)
        spike_axis.move_to(DOWN * 0.4)
        axis_y = spike_axis.get_center()[1]

        spike = Line(
            np.array([0, axis_y, 0]),
            np.array([0, axis_y + 1.7, 0]),
            color=RED,
            stroke_width=8,
        )
        spike_label = Text("50/60 Hz\ninterference", font_size=24, color=RED).next_to(
            spike, UP, buff=0.2
        )

        zero_text = Text("0 Hz", font_size=20, color=WHITE).next_to(
            spike_axis.get_left(), DOWN, buff=0.2
        )
        center_text = Text("50/60 Hz", font_size=24, color=RED).next_to(
            spike_axis, DOWN, buff=0.4
        )
        axis_label = Text("Frequency (Hz)", font_size=22, color=WHITE).next_to(
            spike_axis, DOWN, buff=0.95
        )

        self.play(
            FadeIn(
                trans_title,
                trans_sub,
                spike_axis,
                spike,
                spike_label,
                zero_text,
                center_text,
                axis_label,
            ),
            run_time=max(0.05, 2.5),
        )
        elapsed += 2.5
        self.wait(max(0.05, 5.3))
        elapsed += 5.3

        # ---------- Beat 5: notch filter diagram ----------
        notch_title = Text(
            "A notch filter removes only one frequency",
            font_size=42,
            color=GREEN,
        ).to_edge(UP, buff=0.45)
        notch_title.scale_to_fit_width(11.5)

        small_spike = Line(
            np.array([0, axis_y, 0]),
            np.array([0, axis_y + 0.45, 0]),
            color=RED,
            stroke_width=8,
        )

        self.play(
            FadeOut(trans_title, trans_sub, spike_label),
            Transform(spike, small_spike),
            FadeIn(notch_title),
            run_time=max(0.05, 1.5),
        )
        elapsed += 1.5

        x0 = 0.0
        baseline = 1.25
        xs = np.linspace(-5.2, 5.2, 240)

        def notch_gain(x):
            return 1 - 0.95 * np.exp(-0.5 * ((x - x0) / 0.25) ** 2)

        ys = baseline * np.array([notch_gain(x) for x in xs])
        notch_points = [np.array([xs[0], axis_y, 0])]
        for x, yval in zip(xs, ys):
            notch_points.append(np.array([x, axis_y + yval, 0]))
        notch_points.append(np.array([xs[-1], axis_y, 0]))

        notch_poly = Polygon(
            *notch_points,
            fill_color=TEAL,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=1.5,
        )

        self.play(Create(notch_poly), run_time=max(0.05, 3.0))
        elapsed += 3.0

        preserved_left = Text("Preserved", font_size=24, color=GREEN).move_to(
            np.array([-3.6, 1.7, 0])
        )
        preserved_right = Text("Preserved", font_size=24, color=GREEN).move_to(
            np.array([3.6, 1.7, 0])
        )
        removed_label = Text("Removed at 50/60 Hz", font_size=24, color=RED).move_to(
            np.array([0, 1.9, 0])
        )

        self.play(
            FadeIn(preserved_left, preserved_right, removed_label), run_time=max(0.05, 1.5
        ))
        elapsed += 1.5
        self.wait(max(0.05, 5.0))
        elapsed += 5.0

        # ---------- Beat 6: pulse the notch ----------
        self.play(
            Indicate(notch_poly, scale_factor=1.03, color=GREEN), run_time=max(0.05, 1.2
        ))
        elapsed += 1.2
        self.wait(max(0.05, 6.8))
        elapsed += 6.8

        # ---------- Beat 7: next-section badge ----------
        next_rect = Rectangle(
            width=5.6,
            height=1.0,
            fill_color=BLUE,
            fill_opacity=0.85,
            stroke_color=BLUE,
            stroke_width=2,
        )
        next_text = Text("Next: Notch Filter", font_size=30, color=WHITE)
        next_badge = VGroup(next_rect, next_text)
        next_badge.move_to(DOWN * 2.9)

        self.play(FadeIn(next_badge, shift=UP * 0.3), run_time=max(0.05, 1.0))
        elapsed += 1.0

        self.wait(max(0.05, TOTAL - elapsed))