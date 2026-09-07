ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene7(Scene):
    def make_signal_wave(self):
        return ParametricFunction(
            lambda t: np.array([
                t,
                0.22 * np.sin(4 * t) + 0.12 * np.sin(9 * t + 0.8) + 0.05 * np.sin(15 * t + 2.2),
                0,
            ]),
            t_range=[-1.2, 1.2, 0.03],
            color=TEAL,
            stroke_width=3,
        )

    def make_window_curve(self):
        return ParametricFunction(
            lambda t: np.array([t, np.exp(-(t * 1.5) ** 2), 0]),
            t_range=[-1.5, 1.5, 0.03],
            color=ORANGE,
            stroke_width=3,
        )

    def make_ft_curve(self):
        gauss = lambda t, mu, sig, amp: amp * np.exp(-0.5 * ((t - mu) / sig) ** 2)
        return ParametricFunction(
            lambda t: np.array([
                t,
                0.75 * gauss(t, 0.0, 0.12, 0.9)
                + 0.55 * gauss(t, 0.35, 0.15, 0.55)
                + 0.4 * gauss(t, -0.5, 0.1, 0.45),
                0,
            ]),
            t_range=[-0.9, 0.9, 0.02],
            color=BLUE,
            stroke_width=3,
        )

    def make_spectra_visual(self):
        group = VGroup()
        colors = [TEAL, ORANGE, PURPLE, GOLD, PINK]
        heights = [0.22, 0.42, 0.2, 0.52, 0.3]
        for i in range(5):
            base_x = i * 0.34 - 0.68
            for j, h in enumerate(heights):
                rect = Rectangle(
                    width=0.2,
                    height=h,
                    fill_color=colors[i],
                    fill_opacity=0.7 + 0.07 * j,
                    stroke_width=0,
                )
                rect.move_to([base_x, (j - 2) * 0.13, 0])
                group.add(rect)
        return group

    def make_node(self, label, color, visual):
        box = RoundedRectangle(
            width=2.6,
            height=1.4,
            corner_radius=0.15,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_color=color,
            stroke_width=1.8,
        )
        label_mob = Text(label, font_size=16, color=WHITE, weight=BOLD)
        label_mob.scale_to_fit_width(2.2)
        label_mob.move_to(box.get_top() + DOWN * 0.24)

        visual.scale_to_fit_width(2.1)
        if visual.get_height() > 0.55:
            visual.scale_to_fit_height(0.55)
        visual.move_to(box.get_center() + DOWN * 0.14)

        return VGroup(box, label_mob, visual)

    def make_heatmap(self, center, width=2.8, height=2.2, seed=0):
        rng = np.random.default_rng(seed)
        n_cols, n_rows = 10, 8
        cell_w = width / n_cols
        cell_h = height / n_rows
        x_left = center[0] - width / 2
        y_bottom = center[1] - height / 2

        group = VGroup()
        border = Rectangle(
            width=width,
            height=height,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_color=GREY_B,
            stroke_width=1.2,
        )
        border.move_to(center)
        group.add(border)

        warm_colors = [RED, ORANGE, YELLOW, GOLD]
        for col in range(n_cols):
            center_row = 3 + 2.5 * np.sin(col / 3 + seed)
            strength = rng.uniform(0, 1)
            for row in range(n_rows):
                dist = np.abs(row - center_row)
                op = np.exp(-0.5 * (dist / 1.5) ** 2) * (0.7 + 0.3 * strength) + 0.05
                op = float(np.clip(op, 0.05, 0.95))
                rect = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    fill_color=warm_colors[(col + row + seed) % 4],
                    fill_opacity=op,
                    stroke_width=0,
                )
                rect.move_to([x_left + col * cell_w + cell_w / 2,
                              y_bottom + row * cell_h + cell_h / 2, 0])
                group.add(rect)
        return group

    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Simplified previous scene end-state, to be faded out ---
        prev_left = RoundedRectangle(
            width=2.6, height=2.2, corner_radius=0.15,
            fill_color=BLACK, fill_opacity=1, stroke_color=GREY_B, stroke_width=1.5,
        ).move_to([-1.5, -0.1, 0])
        prev_right = RoundedRectangle(
            width=2.6, height=2.2, corner_radius=0.15,
            fill_color=BLACK, fill_opacity=1, stroke_color=GREY_B, stroke_width=1.5,
        ).move_to([1.5, -0.1, 0])
        prev_text = Text(
            "Every spectrogram reflects a time–frequency trade-off",
            font_size=24,
            color=WHITE,
            weight=BOLD,
        ).scale_to_fit_width(11.0).to_edge(DOWN, buff=0.55)
        prev_group = VGroup(prev_left, prev_right, prev_text)
        self.add(prev_group)

        # --- Build block-diagram nodes (not yet shown) ---
        signal_visual = self.make_signal_wave()
        window_visual = self.make_window_curve()
        ft_visual = self.make_ft_curve()
        spectra_visual = self.make_spectra_visual()

        node_signal = self.make_node("Signal", TEAL, signal_visual)
        node_window = self.make_node("Windowing", ORANGE, window_visual)
        node_ft = self.make_node("Fourier Transform", BLUE, ft_visual)
        node_spectra = self.make_node("Spectra", PURPLE, spectra_visual)

        nodes = [node_signal, node_window, node_ft, node_spectra]
        x_positions = [-4.5, -1.5, 1.5, 4.5]
        for node, x in zip(nodes, x_positions):
            node.move_to([x, 2.3, 0])

        arrows_between = []
        for i in range(3):
            arr = Arrow(
                start=nodes[i].get_right() + RIGHT * 0.08,
                end=nodes[i + 1].get_left() + LEFT * 0.08,
                stroke_width=2,
                color=GREY_B,
                buff=0.1,
                max_tip_length_to_length_ratio=0.2,
            )
            arrows_between.append(arr)

        block_diagram = VGroup(*nodes, *arrows_between)

        # --- Spectrogram image, downward arrow, and label ---
        spec_img = self.make_heatmap(center=np.array([4.5, -0.5, 0]), seed=0)

        down_arrow_start = nodes[-1].get_bottom() + DOWN * 0.06
        down_arrow_end = spec_img.get_top() + UP * 0.06
        down_arrow = Arrow(
            start=down_arrow_start,
            end=down_arrow_end,
            stroke_width=2,
            color=GREY_B,
            buff=0.05,
        )

        spec_label = Text(
            "Spectrogram = visual representation of STFT",
            font_size=19,
            color=WHITE,
        )
        spec_label.scale_to_fit_width(4.5)
        spec_label.next_to(down_arrow, LEFT, buff=0.35)

        # --- Beat 1: 0.00–4.04 ---
        self.play(FadeOut(prev_group), run_time=max(0.05, 1.3))
        self.play(FadeIn(node_signal), run_time=max(0.05, 0.6))
        self.play(FadeIn(arrows_between[0]), FadeIn(node_window), run_time=max(0.05, 0.6))
        self.play(FadeIn(arrows_between[1]), FadeIn(node_ft), run_time=max(0.05, 0.6))
        self.play(FadeIn(arrows_between[2]), FadeIn(node_spectra), run_time=max(0.05, 0.54))
        self.wait(max(0.05, 0.4))

        # Gap to 4.78
        self.wait(max(0.05, 0.74))

        # --- Beat 2: 4.78–8.36 ---
        self.play(FadeIn(down_arrow), run_time=max(0.05, 0.6))
        self.play(FadeIn(spec_img), run_time=max(0.05, 1.0))
        self.play(FadeIn(spec_label), run_time=max(0.05, 0.8))
        self.play(down_arrow.animate.set_stroke(YELLOW, width=4.5).set_opacity(1), run_time=max(0.05, 0.4))
        self.play(down_arrow.animate.set_stroke(YELLOW, width=2.2).set_opacity(0.85), run_time=max(0.05, 0.58))
        self.wait(max(0.05, 0.2))

        # Gap to 9.24
        self.wait(max(0.05, 0.88))

        # --- Beat 3: 9.24–11.12 ---
        self.play(
            block_diagram.animate.shift(UP * 0.45).set_opacity(0.88),
            spec_img.animate.shift(UP * 0.45).set_opacity(0.88),
            spec_label.animate.shift(UP * 0.45).set_opacity(0.88),
            down_arrow.animate.shift(UP * 0.45),
            run_time=max(0.05, 1.3),
        )
        self.wait(max(0.05, 0.58))

        # Gap to 11.74
        self.wait(max(0.05, 0.62))

        # Build updated spectrogram image at current position for Beat 4
        spec_img_updated = self.make_heatmap(
            center=spec_img.get_center(),
            width=spec_img.width,
            height=spec_img.height,
            seed=1,
        )
        ripple_dot = Dot(radius=0.06, color=YELLOW).move_to(node_ft.get_center())
        ft_box = node_ft[0]

        # --- Beat 4: 11.74–16.74 ---
        self.play(
            ft_box.animate.set_stroke(YELLOW, width=4.0),
            FadeIn(ripple_dot, scale=0.5),
            run_time=max(0.05, 0.6),
        )
        self.play(ripple_dot.animate.move_to(node_spectra.get_center()), run_time=max(0.05, 0.9))
        self.play(ripple_dot.animate.move_to(spec_img.get_top() + DOWN * 0.15), run_time=max(0.05, 0.8))
        self.play(
            FadeOut(ripple_dot),
            Transform(spec_img, spec_img_updated),
            run_time=max(0.05, 1.2),
        )
        self.play(down_arrow.animate.set_stroke(YELLOW, width=4.5).set_opacity(1), run_time=max(0.05, 0.5))
        self.play(
            down_arrow.animate.set_stroke(YELLOW, width=2.2).set_opacity(0.85),
            ft_box.animate.set_stroke(BLUE, width=1.8),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.3))

        # Gap to 17.32
        self.wait(max(0.05, 0.58))

        # --- Summary panel and bullets ---
        summary_panel = RoundedRectangle(
            width=12.4,
            height=2.2,
            corner_radius=0.2,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        summary_panel.move_to(np.array([0, -2.3, 0]))

        bullet_texts = [
            "One of the most widely used visualisation tools in time–frequency analysis",
            "Generated from the Short-Time Fourier Transform",
            "Provides a graphical representation of how the frequency content of a signal changes over time",
            "Displays time, frequency, and signal intensity in a single figure",
        ]
        bullet_mobs = []
        for text in bullet_texts:
            b = Text("• " + text, font_size=19, color=WHITE)
            b.scale_to_fit_width(11.2)
            bullet_mobs.append(b)

        sub_bullet = Text(
            "• Visualises non-stationary neural signals more effectively than a conventional frequency spectrum",
            font_size=19,
            color=YELLOW,
        )
        sub_bullet.scale_to_fit_width(11.0)
        sub_bullet.shift(RIGHT * 0.25)

        bullets_group = VGroup(*bullet_mobs, sub_bullet)
        bullets_group.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        bullets_group.move_to(summary_panel.get_center())
        bullets_group.align_to(summary_panel.get_left() + RIGHT * 0.45, LEFT)

        b1, b2, b3, b4 = bullet_mobs

        # --- Beat 5: 17.32–24.66 ---
        self.play(FadeIn(summary_panel), run_time=max(0.05, 1.2))
        self.play(FadeIn(b1), run_time=max(0.05, 1.4))
        self.play(b1.animate.set_color(YELLOW), run_time=max(0.05, 0.5))
        self.play(b1.animate.set_color(WHITE), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 3.74))

        # Gap to 25.48
        self.wait(max(0.05, 0.82))

        # --- Beat 6: 25.48–29.66 ---
        self.play(FadeIn(b2), run_time=max(0.05, 1.0))
        self.play(ft_box.animate.set_stroke(YELLOW, width=4.0), run_time=max(0.05, 0.4))
        self.play(ft_box.animate.set_stroke(BLUE, width=1.8), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 2.38))

        # Gap to 30.48
        self.wait(max(0.05, 0.82))

        # --- Beat 7: 30.48–35.84 ---
        self.play(FadeIn(b3), run_time=max(0.05, 1.2))
        self.play(down_arrow.animate.set_stroke(YELLOW, width=4.5).set_opacity(1), run_time=max(0.05, 0.4))
        self.play(down_arrow.animate.set_stroke(YELLOW, width=2.2).set_opacity(0.85), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 3.36))

        # Gap to 36.56
        self.wait(max(0.05, 0.72))

        # --- Highlight elements for Beat 8 ---
        v_line_x = spec_img.get_left()[0] + 0.35 * spec_img.width
        v_line_time = Line(
            start=np.array([v_line_x, spec_img.get_bottom()[1], 0]),
            end=np.array([v_line_x, spec_img.get_top()[1], 0]),
            color=YELLOW,
            stroke_width=2.5,
        )

        h_line_y = spec_img.get_bottom()[1] + 0.6 * spec_img.height
        h_line_freq = Line(
            start=np.array([spec_img.get_left()[0], h_line_y, 0]),
            end=np.array([spec_img.get_right()[0], h_line_y, 0]),
            color=YELLOW,
            stroke_width=2.5,
        )

        intensity_region = Rectangle(
            width=spec_img.width - 0.2,
            height=0.45,
            fill_color=ORANGE,
            fill_opacity=0.35,
            stroke_color=YELLOW,
            stroke_width=1,
            stroke_opacity=0.6,
        )
        intensity_region.move_to(spec_img.get_center() + UP * 0.2)

        # --- Beat 8: 36.56–46.62 ---
        self.play(FadeIn(b4), run_time=max(0.05, 1.0))
        self.play(Create(v_line_time), run_time=max(0.05, 0.8))
        self.play(Create(h_line_freq), run_time=max(0.05, 0.8))
        self.play(FadeIn(intensity_region), run_time=max(0.05, 0.8))
        self.play(FadeIn(sub_bullet), run_time=max(0.05, 1.2))
        self.play(intensity_region.animate.set_opacity(0.6), run_time=max(0.05, 0.5))
        self.play(intensity_region.animate.set_opacity(0.9), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 4.46))

        # Gap to 47.02
        self.wait(max(0.05, 0.4))

        # --- Beat 9: 47.02–49.73 ---
        self.play(spec_img.animate.set_opacity(0.7), run_time=max(0.05, 0.8))
        self.play(spec_img.animate.set_opacity(1.0), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.11))