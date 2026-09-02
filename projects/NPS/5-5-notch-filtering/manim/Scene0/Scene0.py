ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def freq_to_x(f):
            return -6 + (f / 100.0) * 12

        # --- frequency axis ---
        axis_line = Line(
            np.array([-6.5, 0, 0]),
            np.array([6.5, 0, 0]),
            color=GREY,
            stroke_width=4,
        )
        ticks = VGroup()
        tick_labels = VGroup()
        tick_50 = None

        for f in range(0, 101, 10):
            x = freq_to_x(f)
            tick = Line(
                np.array([x, 0, 0]),
                np.array([x, 0.2, 0]),
                color=GREY,
                stroke_width=3,
            )
            ticks.add(tick)
            if f == 50:
                tick_50 = tick

            label = Text(str(f), font_size=24, color=GREY)
            label.move_to(np.array([x, -0.5, 0]))
            tick_labels.add(label)

        axis_group = VGroup(axis_line, ticks, tick_labels)

        # --- generic PSD curve ---
        def psd_func(x):
            return (
                1.6 * np.exp(-((x + 4) / 1.3) ** 2)
                + 1.4 * np.exp(-((x - 4) / 1.5) ** 2)
                + 0.4 * np.exp(-((x + 1.5) / 0.5) ** 2)
                + 0.4 * np.exp(-((x - 1.5) / 0.5) ** 2)
                + 0.05
            )

        psd_curve = FunctionGraph(
            psd_func,
            x_range=[-6, 6, 0.01],
            color=BLUE,
            stroke_width=5,
        )

        # Beat 1: 0.00 - 18.46
        self.play(Write(axis_group), run_time=max(0.05, 2.0))
        self.play(Create(psd_curve), run_time=max(0.05, 4.0))
        self.wait(max(0.05, 18.46 - 2.0 - 4.0))

        # Beat 2: 18.46 - 23.34
        label_50 = Text("50 Hz", font_size=36, color=YELLOW)
        label_50.next_to(tick_50, UP, buff=0.3)

        glow = Circle(
            radius=0.30,
            color=YELLOW,
            fill_opacity=0.0,
            stroke_width=0,
        )
        glow.move_to(np.array([0, 0.125, 0]))

        self.add(glow)
        self.play(
            FadeIn(label_50),
            tick_50.animate.set_color(YELLOW),
            run_time=max(0.05, 2.0),
        )
        self.play(glow.animate.set_fill(opacity=0.25), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 4.88 - 2.0 - 1.5))

        # Beat 3: 23.34 - 24.50  -- band expands
        dim_overlay = Rectangle(
            width=4.8,
            height=2.8,
            fill_color="#0F1116",
            fill_opacity=0.0,
            stroke_width=0,
        )
        dim_overlay.move_to(np.array([0, 1.2, 0]))

        band = Rectangle(
            width=0.05,
            height=2.8,
            fill_color=GREY,
            fill_opacity=0.3,
            stroke_color=GREY_A,
            stroke_width=1,
        )
        band.move_to(np.array([0, 1.2, 0]))

        self.add(dim_overlay)
        self.add(band)
        self.play(band.animate.stretch_to_fit_width(4.8), run_time=max(0.05, 1.16))

        # Beat 4: 24.50 - 27.72  -- dim inside band
        self.play(dim_overlay.animate.set_fill(opacity=0.55), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 3.22 - 1.5))

        # Beat 5: 27.72 - 31.12  -- "Not this" text
        not_this = Text(
            "Not this — too much lost.",
            font_size=32,
            color=ORANGE,
        )
        not_this.scale_to_fit_width(10)
        not_this.move_to(np.array([0, 3.1, 0]))

        self.play(FadeIn(not_this), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 3.40 - 2.0))

        # Beat 6: 31.12 - 33.84  -- text fades, band contracts
        self.play(
            FadeOut(not_this),
            band.animate.stretch_to_fit_width(0.05),
            run_time=max(0.05, 2.72),
        )

        # Beat 7: 33.84 - 38.88  -- outside brightens
        self.play(dim_overlay.animate.set_fill(opacity=0.0), run_time=max(0.05, 5.04))

        # Beat 8: 38.88 - 39.64  -- only thin sliver remains dark
        self.wait(max(0.05, 0.76))

        # Beat 9: 39.64 - 40.72  -- sliver fades
        self.play(FadeOut(band), run_time=max(0.05, 1.08))

        # Beat 10: 40.72 - 42.05  -- notch filter explanation remains
        notch_text = Text(
            "Notch filter — remove only the narrow band.",
            font_size=32,
            color=WHITE,
            t2c={"Notch filter": YELLOW},
        )
        notch_text.move_to(np.array([0, -2.3, 0]))
        self.play(FadeIn(notch_text), run_time=max(0.05, 1.33))