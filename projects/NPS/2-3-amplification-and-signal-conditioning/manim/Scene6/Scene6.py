ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --------------------------------------------------------------
        # helpers
        # --------------------------------------------------------------
        def make_panel(center_x, center_y, w, h):
            rect = Rectangle(
                width=w, height=h,
                fill_color=GREY, fill_opacity=0.16,
                stroke_color=GREY_B, stroke_width=2,
            ).move_to(np.array([center_x, center_y, 0]))
            axis = Line(
                start=rect.get_left() + RIGHT * 0.18,
                end=rect.get_right() + LEFT * 0.18,
                color=GREY_B, stroke_width=1.6, stroke_opacity=0.8,
            )
            return VGroup(rect, axis), rect

        def make_wave(panel, amp=0.5, noise_level=0.0, clip=False,
                      color=GREEN, stroke_width=2.5, deform=False, seed=7):
            left_x = panel.get_left()[0] + 0.22
            right_x = panel.get_right()[0] - 0.22
            n = 200
            xs = np.linspace(left_x, right_x, n)
            x_norm = (xs - left_x) / (right_x - left_x)
            center_y = panel.get_center()[1]

            if deform:
                ys = amp * np.sin(2 * PI * 1.5 * x_norm)
                mask = (x_norm > 0.35) & (x_norm < 0.65)
                idx = np.where(mask)[0]
                if len(idx) > 2:
                    i0, i1 = idx[0], idx[-1]
                    ys[i0:i1 + 1] = np.interp(
                        x_norm[i0:i1 + 1],
                        [x_norm[i0], x_norm[i1]],
                        [ys[i0], ys[i1]],
                    )
            else:
                ys = amp * np.sin(2 * PI * 1.2 * x_norm)
                if noise_level:
                    rng = np.random.RandomState(seed)
                    jagged = (
                        0.55 * noise_level * np.sin(2 * PI * 12 * x_norm)
                        + 0.25 * noise_level * np.sin(2 * PI * 23 * x_norm)
                        + 0.20 * noise_level * rng.randn(n)
                    )
                    ys = ys + jagged

            if clip:
                half_h = panel.get_height() / 2
                top = center_y + half_h - 0.06
                bottom = center_y - half_h + 0.06
                ys = np.clip(ys, bottom, top)

            wave = VMobject()
            wave.set_points_as_corners(
                [np.array([x, y, 0]) for x, y in zip(xs, ys)]
            )
            wave.set_stroke(color=color, width=stroke_width)
            return wave

        # --------------------------------------------------------------
        # 1. 0.00-5.80  title + three empty waveform panels
        # --------------------------------------------------------------
        title = Text("Amplification and Signal Conditioning", font_size=40,
                     color=WHITE, weight="BOLD")
        title.scale_to_fit_width(12.5)
        title.to_edge(UP, buff=0.35)

        panel_w = 3.2
        panel_h = 1.8
        panel_gap = 0.8
        panel_y = 0.7
        old_centers = np.array([-4.0, 0.0, 4.0])

        old_panels = []
        for cx in old_centers:
            panel, _ = make_panel(cx, panel_y, panel_w, panel_h)
            old_panels.append(panel)
        panel_left, panel_center, panel_right = old_panels
        panels_group = VGroup(*old_panels)

        self.wait(max(0.05, 0.4))
        self.play(FadeIn(title), run_time=max(0.05, 1.0))
        self.play(FadeIn(panels_group), run_time=max(0.05, 1.2))
        self.play(panels_group.animate.scale(1.015, about_point=panels_group.get_center()),
                  run_time=max(0.05, 0.5))
        self.play(panels_group.animate.scale(1 / 1.015, about_point=panels_group.get_center()),
                  run_time=max(0.05, 0.5))
        self.wait(max(0.05, 2.2))

        # 5.80-6.80 gap
        self.wait(max(0.05, 1.0))

        # --------------------------------------------------------------
        # 2. 6.80-10.20  too little amplification -> tiny wave left
        # --------------------------------------------------------------
        wave_left = make_wave(panel_left, amp=0.11, noise_level=0.0,
                              color=BLUE, stroke_width=2.5)
        label_left = Text("too little amplification: difficult to analyse",
                          font_size=16, color=BLUE)
        label_left.scale_to_fit_width(panel_w + 0.6)
        label_left.next_to(panel_left, DOWN, buff=0.22)

        self.play(Create(wave_left), run_time=max(0.05, 2.0))
        self.play(FadeIn(label_left), run_time=max(0.05, 0.8))
        self.play(wave_left.animate.scale(1.04, about_point=wave_left.get_center()),
                  run_time=max(0.05, 0.3))
        self.play(wave_left.animate.scale(1 / 1.04, about_point=wave_left.get_center()),
                  run_time=max(0.05, 0.3))

        # 10.20-11.08 gap
        self.wait(max(0.05, 0.88))

        # --------------------------------------------------------------
        # 3. 11.08-17.44  excessive amplification -> clipped, noisy right
        # --------------------------------------------------------------
        wave_right = make_wave(panel_right, amp=1.7, noise_level=0.30,
                               clip=True, color=RED, stroke_width=2.8, seed=9)
        label_right = Text("excessive amplification: noise amplified, saturation",
                           font_size=16, color=RED)
        label_right.scale_to_fit_width(panel_w + 0.6)
        label_right.next_to(panel_right, DOWN, buff=0.22)

        self.play(Create(wave_right), run_time=max(0.05, 3.0))
        self.play(FadeIn(label_right), run_time=max(0.05, 0.8))
        self.play(Indicate(panel_right, color=RED, scale_factor=1.07), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.96))

        # --------------------------------------------------------------
        # 4. 17.44-18.22  correct amplification -> clean center wave
        # --------------------------------------------------------------
        wave_center = make_wave(panel_center, amp=0.55, noise_level=0.0,
                                color=GREEN, stroke_width=2.6)
        label_center = Text("correct amplification: processable",
                            font_size=16, color=GREEN)
        label_center.scale_to_fit_width(panel_w + 0.6)
        label_center.next_to(panel_center, DOWN, buff=0.22)

        self.play(FadeIn(VGroup(wave_center, label_center)), run_time=max(0.05, 0.78))

        # --------------------------------------------------------------
        # 5. 18.22-26.62  poor conditioning comparison
        # --------------------------------------------------------------
        old_all = VGroup(
            panel_left, panel_center, panel_right,
            wave_left, wave_right, wave_center,
            label_left, label_right, label_center,
        )

        new_panel_w = 3.8
        new_left_panel, _ = make_panel(-2.8, panel_y, new_panel_w, panel_h)
        new_right_panel, _ = make_panel(2.8, panel_y, new_panel_w, panel_h)
        new_panels = VGroup(new_left_panel, new_right_panel)

        self.play(FadeOut(old_all), FadeIn(new_panels), run_time=max(0.05, 1.0))

        wave_new_left = make_wave(new_left_panel, amp=0.55, deform=True,
                                  color=PURPLE, stroke_width=2.6)
        label_new_left = Text("poor conditioning: useful information removed",
                              font_size=16, color=PURPLE)
        label_new_left.scale_to_fit_width(new_panel_w + 0.8)
        label_new_left.next_to(new_left_panel, DOWN, buff=0.22)

        self.play(Create(wave_new_left), run_time=max(0.05, 2.4))
        self.play(FadeIn(label_new_left), run_time=max(0.05, 0.8))

        wave_new_right = make_wave(new_right_panel, amp=0.55, noise_level=0.18,
                                   color=ORANGE, stroke_width=2.6, seed=11)
        label_new_right = Text("poor conditioning: unwanted interference remains",
                               font_size=16, color=ORANGE)
        label_new_right.scale_to_fit_width(new_panel_w + 0.8)
        label_new_right.next_to(new_right_panel, DOWN, buff=0.22)

        self.play(Create(wave_new_right), run_time=max(0.05, 2.4))
        self.play(FadeIn(label_new_right), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.0))

        # --------------------------------------------------------------
        # 6. 26.62-35.38  critical-stage statement and fade-out
        # --------------------------------------------------------------
        new_all = VGroup(
            new_left_panel, new_right_panel,
            wave_new_left, wave_new_right,
            label_new_left, label_new_right,
        )
        self.play(FadeOut(new_all), run_time=max(0.05, 1.0))

        statement = Text(
            "Amplification and signal conditioning are critical stages.",
            font_size=46, weight="BOLD", color=WHITE,
            t2c={"critical stages": YELLOW},
        )
        statement.scale_to_fit_width(11)
        statement.move_to(ORIGIN)

        self.play(GrowFromCenter(statement), run_time=max(0.05, 0.8))
        self.play(statement.animate.scale(1.03), run_time=max(0.05, 0.25))
        self.play(statement.animate.scale(1 / 1.03), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 5.46))

        self.play(FadeOut(VGroup(title, statement)), run_time=max(0.05, 1.0))