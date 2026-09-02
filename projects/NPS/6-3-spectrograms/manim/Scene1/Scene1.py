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


class Scene1(Scene):
    def build_spectrogram(self):
        n_cols = 36
        n_bins = 20
        col_width = 0.15
        row_height = 3.0 / n_bins
        img = VGroup()
        for i in range(n_cols):
            t_val = i / (n_cols - 1)
            center_freq = 2.0 + 2.5 * t_val + 1.8 * np.sin(2 * np.pi * (t_val - 0.2))
            column = VGroup()
            for j in range(n_bins):
                freq = 1.0 + (8.0 - 1.0) * j / (n_bins - 1)
                intensity = np.exp(-((freq - center_freq) ** 2) / (2 * 0.65 ** 2))
                intensity2 = 0.55 * np.exp(
                    -((freq - (center_freq + 5 * np.exp(-((t_val - 0.7) / 0.2) ** 2))) ** 2)
                    / (2 * 0.5 ** 2)
                )
                intensity = max(intensity, intensity2)
                color_idx = int(min(1.0, intensity) * 6)
                color = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED][color_idx]
                rect = Rectangle(
                    width=col_width,
                    height=row_height,
                    fill_color=color,
                    fill_opacity=intensity,
                    stroke_width=0,
                )
                rect.move_to(np.array([0, -1.5 + row_height * (j + 0.5), 0]))
                column.add(rect)
            column.move_to(np.array([-(n_cols - 1) * col_width / 2 + i * col_width, 0, 0]))
            img.add(column)
        return img

    def make_spectra_cluster(self):
        colors = [BLUE, TEAL, GREEN, YELLOW, GOLD, ORANGE, RED]
        cluster = VGroup()
        width = 0.30
        height = 1.4
        for color in colors:
            rect = Rectangle(
                width=width,
                height=height,
                fill_color=color,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=0.5,
            )
            line = Line(UP * height * 0.3, DOWN * height * 0.3, color=WHITE, stroke_width=1.5)
            graph = VGroup(rect, line)
            cluster.add(graph)
        cluster.arrange(RIGHT, buff=0.08)
        return cluster

    def construct(self):
        self.camera.background_color = "#0F1116"

        # -- Build the spectrogram already on screen (carried over from previous scene) --
        spec_image = self.build_spectrogram()
        spec_image.move_to(np.array([0, 0.6, 0]))

        spec_left = spec_image.get_left()[0]
        spec_right = spec_image.get_right()[0]
        spec_top = spec_image.get_top()[1]
        spec_bottom = spec_image.get_bottom()[1]

        x_axis_line = Line(
            np.array([spec_left - 0.2, spec_bottom - 0.15, 0]),
            np.array([spec_right + 0.2, spec_bottom - 0.15, 0]),
            color=WHITE,
            stroke_width=2,
        )
        y_axis_line = Line(
            np.array([spec_left - 0.15, spec_bottom - 0.2, 0]),
            np.array([spec_left - 0.15, spec_top + 0.2, 0]),
            color=WHITE,
            stroke_width=2,
        )

        time_label = Text("Time", font_size=24, color=WHITE).next_to(x_axis_line, DOWN, buff=0.08)
        freq_label = Text("Frequency", font_size=24, color=WHITE)
        freq_label.rotate(PI / 2)
        freq_label.next_to(y_axis_line, LEFT, buff=0.10)

        gradient_colors = [BLUE, BLUE, TEAL, TEAL, GREEN, GREEN, YELLOW, YELLOW, GOLD, GOLD, ORANGE, RED]
        colorbar = VGroup(
            *[
                Rectangle(
                    width=0.22,
                    height=3.2 / len(gradient_colors),
                    fill_color=c,
                    fill_opacity=1,
                    stroke_width=0,
                )
                for c in gradient_colors
            ]
        )
        colorbar.arrange(DOWN, buff=0)
        colorbar.next_to(spec_image, RIGHT, buff=0.35)
        weak_label = Text("weak", font_size=15, color=GREY_B).next_to(colorbar, DOWN, buff=0.05)
        strong_label = Text("strong", font_size=15, color=WHITE).next_to(colorbar, UP, buff=0.05)
        magnitude_label = Text("magnitude", font_size=16, color=WHITE)
        magnitude_label.rotate(PI / 2)
        magnitude_label.next_to(colorbar, RIGHT, buff=0.12)

        self.add(
            spec_image,
            x_axis_line,
            y_axis_line,
            time_label,
            freq_label,
            colorbar,
            weak_label,
            strong_label,
            magnitude_label,
        )

        # Soft bright patches inside the spectrogram, used for "shifting energy" animations.
        patch_centers = [
            np.array([spec_left + 0.8, spec_bottom + 0.7, 0]),
            np.array([spec_image.get_center()[0], spec_bottom + 1.7, 0]),
            np.array([spec_right - 0.9, spec_bottom + 1.0, 0]),
        ]
        patch_colors = [YELLOW, GOLD, ORANGE]
        bright_patches = VGroup()
        for center, color in zip(patch_centers, patch_colors):
            patch = Ellipse(width=0.9, height=0.55, fill_color=color, fill_opacity=0.55, stroke_width=0)
            patch.move_to(center)
            bright_patches.add(patch)
        self.add(bright_patches)

        # -- 1. 0.00-1.68 — bright patches shift up/down across the image --
        self.play(
            bright_patches[0].animate.shift(UP * 0.7),
            bright_patches[1].animate.shift(DOWN * 0.6),
            bright_patches[2].animate.shift(UP * 0.8),
            run_time=max(0.05, 0.84),
        )
        self.play(
            bright_patches[0].animate.shift(DOWN * 0.5),
            bright_patches[1].animate.shift(UP * 0.7),
            bright_patches[2].animate.shift(DOWN * 0.6),
            run_time=max(0.05, 0.84),
        )

        # -- 2. 1.68-4.34 — soft rounded highlight pulses once, then settles --
        spec_highlight = SurroundingRectangle(
            spec_image,
            color=WHITE,
            buff=0.12,
            corner_radius=0.2,
            stroke_width=3,
        )
        self.play(Create(spec_highlight), run_time=max(0.05, 0.66))
        self.play(spec_highlight.animate.scale(1.03), run_time=max(0.05, 0.75))
        self.play(spec_highlight.animate.scale(1 / 1.03), run_time=max(0.05, 0.65))
        self.wait(max(0.05, 0.60))

        # -- 3. 4.34-7.90 — label fades in; axes glow; bright patches shift --
        graph_label = Text("graphical representation", font_size=30, color=WHITE)
        graph_label.next_to(time_label, DOWN, buff=0.45)
        self.play(FadeIn(graph_label), run_time=max(0.05, 0.80))
        self.play(Indicate(freq_label, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.50))
        self.play(Indicate(time_label, color=YELLOW, scale_factor=1.2), run_time=max(0.05, 0.50))
        self.play(
            bright_patches[0].animate.shift(UP * 0.4 + RIGHT * 0.15),
            bright_patches[1].animate.shift(UP * 0.3 + LEFT * 0.1),
            bright_patches[2].animate.shift(DOWN * 0.35),
            run_time=max(0.05, 1.76),
        )

        # -- gap 7.90-8.66 --
        self.wait(max(0.05, 0.76))

        # -- 4. 8.66-13.70 — border fades, vertical window grid fades in --
        self.play(FadeOut(spec_highlight), run_time=max(0.05, 0.80))

        n_strips = 16
        strip_boundaries = np.linspace(spec_left, spec_right, n_strips + 1)
        vertical_lines = VGroup()
        tick_marks = VGroup()
        for x in strip_boundaries:
            v_line = Line(
                np.array([x, spec_bottom, 0]),
                np.array([x, spec_top, 0]),
                color=WHITE,
                stroke_width=1.5,
                stroke_opacity=0.35,
            )
            vertical_lines.add(v_line)
            tick = Line(
                np.array([x, x_axis_line.get_bottom()[1], 0]),
                np.array([x, x_axis_line.get_bottom()[1] - 0.1, 0]),
                color=GREY_B,
                stroke_width=2,
            )
            tick_marks.add(tick)

        self.play(
            LaggedStart(*[FadeIn(line) for line in vertical_lines], lag_ratio=0.06),
            LaggedStart(*[FadeIn(tick) for tick in tick_marks], lag_ratio=0.06),
            run_time=max(0.05, 2.00),
        )
        self.wait(max(0.05, 2.24))

        # -- 5. 13.70-16.66 — vertical lines remain; horizontal wipe moves left to right --
        strip_centers = (strip_boundaries[:-1] + strip_boundaries[1:]) / 2
        strip_width = float(strip_centers[1] - strip_centers[0])

        dim_overlays = VGroup()
        strip_overlay_list = []
        for cx in strip_centers:
            overlay = Rectangle(
                width=strip_width,
                height=spec_image.height,
                fill_color=BLACK,
                fill_opacity=0.0,
                stroke_width=0,
            )
            overlay.move_to(np.array([cx, spec_image.get_center()[1], 0]))
            dim_overlays.add(overlay)
            strip_overlay_list.append(overlay)

        wipe_tracker = ValueTracker(strip_centers[0])
        wipe_band = Rectangle(
            width=strip_width,
            height=spec_image.height,
            fill_color=WHITE,
            fill_opacity=0.12,
            stroke_color=WHITE,
            stroke_width=1.5,
            stroke_opacity=0.4,
        )
        wipe_band.move_to(np.array([strip_centers[0], spec_image.get_center()[1], 0]))
        wipe_band.add_updater(lambda m: m.set_x(wipe_tracker.get_value()))

        def make_overlay_updater(cx):
            def updater(ov):
                wipe_x = wipe_tracker.get_value()
                if abs(cx - wipe_x) < strip_width * 0.5:
                    ov.set_fill(opacity=0.0)
                else:
                    ov.set_fill(opacity=0.62)
            return updater

        for ov, cx in zip(strip_overlay_list, strip_centers):
            ov.add_updater(make_overlay_updater(cx))

        # Keep grid lines visible above dim layers.
        vertical_lines.set_z_index(5)
        tick_marks.set_z_index(5)
        dim_overlays.set_z_index(2)
        wipe_band.set_z_index(3)

        self.add(dim_overlays)
        self.play(FadeIn(wipe_band), run_time=max(0.05, 0.25))
        self.play(wipe_tracker.animate.set_value(strip_centers[-1]), run_time=max(0.05, 2.41))
        self.wait(max(0.05, 0.30))

        # -- 6. 16.66-22.16 — grid fades, strips merge, image brightens slightly --
        wipe_band.clear_updaters()
        for ov in strip_overlay_list:
            ov.clear_updaters()

        brighten_overlay = Rectangle(
            width=spec_image.width,
            height=spec_image.height,
            fill_color=WHITE,
            fill_opacity=0.0,
            stroke_width=0,
        ).move_to(spec_image.get_center())
        self.add(brighten_overlay)

        self.play(
            FadeOut(dim_overlays),
            FadeOut(wipe_band),
            FadeOut(vertical_lines),
            FadeOut(tick_marks),
            run_time=max(0.05, 2.00),
        )
        self.play(brighten_overlay.animate.set_fill(opacity=0.10), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 2.70))

        # -- 7. 22.16-28.32 — two labels appear sequentially, then slow shifting animation --
        self.play(FadeOut(graph_label), run_time=max(0.05, 0.56))
        label1 = Text("Time–frequency representation", font_size=28, color=WHITE)
        label1.next_to(time_label, DOWN, buff=0.4)
        label2 = Text("Frequency content over time", font_size=28, color=WHITE)
        label2.next_to(time_label, DOWN, buff=0.4)

        self.play(FadeIn(label1), run_time=max(0.05, 0.90))
        self.wait(max(0.05, 0.30))
        self.play(FadeOut(label1), run_time=max(0.05, 0.80))
        self.play(FadeIn(label2), run_time=max(0.05, 0.80))

        self.play(
            bright_patches[0].animate.shift(RIGHT * 0.8 + UP * 0.2).set_fill(opacity=0.75),
            bright_patches[1].animate.shift(LEFT * 0.4 + DOWN * 0.5).set_fill(opacity=0.45),
            bright_patches[2].animate.shift(DOWN * 0.7).set_fill(opacity=0.7),
            run_time=max(0.05, 2.80),
        )

        # -- gap 28.32-29.06 --
        self.wait(max(0.05, 0.74))

        # -- 8. 29.06-36.62 — cluster of spectra flows into the spectrogram --
        self.play(FadeOut(label2), run_time=max(0.05, 0.60))

        spectra_cluster = self.make_spectra_cluster()
        spectra_cluster.move_to(np.array([spec_left - 1.8, spec_image.get_center()[1], 0]))
        self.play(GrowFromCenter(spectra_cluster), run_time=max(0.05, 1.20))
        self.play(spectra_cluster.animate.scale(1.06), run_time=max(0.05, 0.40))
        self.play(spectra_cluster.animate.scale(1 / 1.06), run_time=max(0.05, 0.40))

        self.play(
            spectra_cluster.animate.scale(0.35).move_to(spec_image.get_center()).set_opacity(0.2),
            FadeOut(bright_patches),
            brighten_overlay.animate.set_fill(opacity=0.13),
            run_time=max(0.05, 3.00),
        )
        self.play(FadeOut(spectra_cluster), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.46))

        # -- gap 36.62-37.70 --
        self.wait(max(0.05, 1.08))

        # -- 9. 37.70-44.18 — three application icons appear in turn with linking lines --
        icon_specs = [
            ("soundwave", "Speech processing", BLUE),
            ("activity", "Biomedical engineering", GOLD),
            ("brain", "Neuroscience", PURPLE),
        ]
        icon_xs = [-4.8, 0.0, 4.8]

        icon_items = []
        for (asset_key, label_text, color), x in zip(icon_specs, icon_xs):
            if asset_key == "soundwave":
                icon = SVGMobject(ASSET_PATHS["soundwave"])
            elif asset_key == "activity":
                icon = SVGMobject(ASSET_PATHS["activity"])
            else:
                icon = SVGMobject(ASSET_PATHS["brain"])

            icon.scale_to_fit_height(0.75)
            icon.set_color(color)
            icon.set_stroke(color, width=1.5)
            label = Text(label_text, font_size=18, color=WHITE).next_to(icon, DOWN, buff=0.15)
            group = VGroup(icon, label)
            group.move_to(np.array([x, -3.05, 0]))
            line = Line(
                np.array([x, group.get_top()[1], 0]),
                np.array([x, spec_bottom, 0]),
                color=WHITE,
                stroke_width=1.5,
                stroke_opacity=0.45,
            )
            icon_items.append((group, line))

        for group, line in icon_items:
            self.play(FadeIn(group), Create(line), run_time=max(0.05, 0.80))
            self.wait(max(0.05, 0.50))
            self.play(FadeOut(line), run_time=max(0.05, 0.50))
            self.wait(max(0.05, 0.36))

        app_icons_group = VGroup(*[item[0] for item in icon_items])

        # -- 10. 44.18-45.17 — icons fade out, definition box fades in --
        self.play(FadeOut(app_icons_group), run_time=max(0.05, 0.35))

        def_text = Text(
            "Spectrogram: A time–frequency representation\nshowing how the frequency content of a signal changes over time",
            font_size=21,
            color=WHITE,
            line_spacing=0.8,
        )
        def_text.scale_to_fit_width(9.0)
        def_box = RoundedRectangle(
            width=def_text.width + 0.7,
            height=def_text.height + 0.35,
            corner_radius=0.25,
            fill_color=WHITE,
            fill_opacity=0.08,
            stroke_color=WHITE,
            stroke_width=2,
        )
        def_text.move_to(def_box.get_center())
        definition_group = VGroup(def_box, def_text)
        definition_group.next_to(time_label, DOWN, buff=0.4)

        self.play(FadeIn(definition_group), run_time=max(0.05, 0.64))