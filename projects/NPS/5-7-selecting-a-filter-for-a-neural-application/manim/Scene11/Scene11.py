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

class Scene11(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ----- helper functions -----
        def make_wave(sig, color, width=3.0, height=1.0, stroke_width=3):
            n = len(sig)
            x = np.linspace(-width / 2, width / 2, n)
            y = sig - np.mean(sig)
            y = y / (np.max(np.abs(y)) * 1.1 + 1e-12) * height / 2
            points = [np.array([x[i], y[i], 0]) for i in range(n)]
            trace = VMobject(stroke_color=color, stroke_width=stroke_width, fill_opacity=0)
            trace.set_points_as_corners(points)
            return trace

        def make_check(color=GREEN, height=0.7):
            return SVGMobject(
                ASSET_PATHS["check_circle"],
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
                height=height,
            )

        # ----- BEAT 1: banner already on screen -----
        banner_bg = Rectangle(
            width=11.0, height=1.4,
            fill_color=GREEN, fill_opacity=0.18,
            stroke_color=GREEN, stroke_width=2,
        )
        banner_text = Text(
            "Goal: preserve physiological information, not just smoothness",
            font_size=30, color=WHITE, weight=BOLD,
        )
        banner_text.scale_to_fit_width(8.6)
        banner_check = make_check(GREEN, 0.75)

        banner_group = VGroup(banner_check, banner_text).arrange(RIGHT, buff=0.3)
        banner_group.move_to(banner_bg.get_center())
        banner = VGroup(banner_bg, banner_group)
        banner.move_to(np.array([0, -2.8, 0]))
        self.add(banner)
        self.wait(max(0.05, 0.48))   # 0.00 → 0.48

        # ----- build the four icons -----
        # 1) brain + waveform inside
        brain_svg = SVGMobject(ASSET_PATHS["brain"], fill_color=WHITE, fill_opacity=1,
                               stroke_width=0, height=1.3)
        t_wave = np.linspace(0, 2 * np.pi, 80)
        sig_wave = 0.3 * np.sin(t_wave)
        wave_mob = make_wave(sig_wave, YELLOW, width=1.2, height=0.4, stroke_width=3)
        wave_mob.move_to(brain_svg.get_center())
        brain_icon = VGroup(brain_svg, wave_mob)

        # 2) jagged noise
        noise_seed = np.random.RandomState(42)
        noise_sig = noise_seed.randn(200).cumsum() * 0.15
        noise_icon = make_wave(noise_sig, ORANGE, width=2.0, height=1.2, stroke_width=3)

        # 3) bar‑chart‑like spectrum icon
        spec_icon = SVGMobject(ASSET_PATHS["bar_chart"], fill_color=TEAL, fill_opacity=1,
                               stroke_width=0, height=1.5)

        # 4) dartboard with arrow in bullseye
        def create_dartboard(height=1.5):
            radii = [0.75, 0.6, 0.45, 0.3, 0.15]
            colors = [RED, WHITE, RED, WHITE, RED]
            circles_group = VGroup()
            for r, c in zip(radii, colors):
                circle = Circle(radius=r, fill_color=c, fill_opacity=1,
                                stroke_width=1.5, stroke_color=WHITE)
                circles_group.add(circle)
            arrow = Arrow(start=ORIGIN + LEFT * 0.9, end=ORIGIN,
                          color=YELLOW, stroke_width=4,
                          max_tip_length_to_length_ratio=0.25, buff=0)
            board = VGroup(circles_group, arrow)
            board.scale_to_fit_height(height)
            return board

        dart_icon = create_dartboard(height=1.4)

        icons = [brain_icon, noise_icon, spec_icon, dart_icon]

        # initial loose orbital placement
        center = np.array([0.0, 0.0, 0.0])
        radius = 3.0
        phases = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
        np.random.seed(11)
        offsets = [np.array([np.random.uniform(-0.4, 0.4),
                              np.random.uniform(-0.4, 0.4), 0]) for _ in range(4)]
        for i, icon in enumerate(icons):
            pos = center + radius * np.array([np.cos(phases[i]), np.sin(phases[i]), 0]) + offsets[i]
            icon.move_to(pos)

        icons_group = VGroup(*icons)

        # ----- BEAT 2: banner fades, icons appear -----
        self.play(FadeOut(banner), FadeIn(icons_group), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 1.62 - 0.48 - 0.5))   # 0.48 → 1.62

        # ----- BEAT 3: slow circular orbit -----
        orbit_angle = ValueTracker(0)

        def update_icon(icon, phase):
            def updater(mob):
                ang = orbit_angle.get_value()
                pos = center + radius * np.array([np.cos(ang + phase),
                                                  np.sin(ang + phase), 0])
                mob.move_to(pos)
            return updater

        for i, icon in enumerate(icons):
            icon.add_updater(update_icon(icon, phases[i]))

        self.play(orbit_angle.animate.set_value(2 * PI),
                  run_time=max(0.05, 1.86))   # 1.62 → 3.48

        # stop orbit
        for icon in icons:
            icon.clear_updaters()

        # ----- BEAT 4: tighten to horizontal row -----
        row_x = [-4.5, -1.5, 1.5, 4.5]
        row_y = 0.0
        row_targets = [np.array([x, row_y, 0]) for x in row_x]

        anims_to_row = [icon.animate.move_to(target)
                        for icon, target in zip(icons, row_targets)]
        self.play(AnimationGroup(*anims_to_row, lag_ratio=0.1),
                  run_time=max(0.05, 2.50))   # 3.48 → 5.98

        # labels that will appear in beats 5‑8
        labels_text = ["Signal", "Interference", "Frequency range", "Analysis objective"]
        label_colors = [YELLOW, ORANGE, TEAL, PURPLE]
        labels = []
        for txt, col in zip(labels_text, label_colors):
            label = Text(txt, font_size=24, color=col, weight=BOLD)
            labels.append(label)

        # ----- BEAT 5: brain → "Signal" -----
        signal_label = labels[0]
        signal_label.next_to(icons[0], DOWN, buff=0.2)
        self.play(
            icons[0].animate.scale(1.25),
            FadeIn(signal_label),
            run_time=max(0.05, 1.70),   # 5.98 → 7.68
        )

        # ----- BEAT 6: noise → "Interference" -----
        interference_label = labels[1]
        interference_label.next_to(icons[1], DOWN, buff=0.2)
        self.play(
            icons[1].animate.scale(1.25),
            FadeIn(interference_label),
            run_time=max(0.05, 2.78),   # 7.68 → 10.46
        )

        # ----- BEAT 7: spectrum → "Frequency range" -----
        freq_label = labels[2]
        freq_label.next_to(icons[2], DOWN, buff=0.2)
        self.play(
            icons[2].animate.scale(1.25),
            FadeIn(freq_label),
            run_time=max(0.05, 3.04),   # 10.46 → 13.50
        )

        # ----- BEAT 8: dartboard → "Analysis objective" -----
        analysis_label = labels[3]
        analysis_label.next_to(icons[3], DOWN, buff=0.2)
        self.play(
            icons[3].animate.scale(1.25),
            FadeIn(analysis_label),
            run_time=max(0.05, 1.96),   # 13.50 → 15.46
        )

        # group each icon with its label for later convenience
        icon_with_labels = [VGroup(icon, lbl) for icon, lbl in zip(icons, labels)]
        icons_top_group = VGroup(*icon_with_labels)

        # ----- BEAT 9: hold, gentle pulse -----
        self.play(
            icons_top_group.animate.scale(1.05),
            run_time=max(0.05, 2.24),
            rate_func=there_and_back,
        )   # 15.46 → 17.70
        self.wait(max(0.05, 2.24))   # 17.70 → 19.94

        # ----- BEAT 10: shrink to bottom, filter graphic appears -----
        bottom_targets = [np.array([x, -2.5, 0]) for x in row_x]
        anims_bottom = [
            grp.animate.move_to(target).scale(0.65)
            for grp, target in zip(icon_with_labels, bottom_targets)
        ]
        self.play(*anims_bottom, run_time=max(0.05, 1.5))   # 19.94 → 21.44

        # ---- build the filter graphic ----
        # central block
        central_rect = Rectangle(
            width=3.5, height=2.0,
            fill_color=BLUE, fill_opacity=0.8,
            stroke_color=WHITE, stroke_width=2,
        )
        filter_text = Text("Filter", font_size=36, color=WHITE, weight=BOLD)
        filter_text.move_to(central_rect)

        # multiple input arrows from left
        input_arrows = VGroup()
        for y_shift in [0.5, 0, -0.5]:
            start_pt = central_rect.get_left() + LEFT * 1.0 + UP * y_shift
            end_pt = central_rect.get_left() + UP * y_shift
            arr = Arrow(start=start_pt, end=end_pt, color=WHITE, stroke_width=3,
                        buff=0, max_tip_length_to_length_ratio=0.2)
            input_arrows.add(arr)

        # one selected output arrow on right
        output_arrow = Arrow(
            start=central_rect.get_right(), end=central_rect.get_right() + RIGHT * 1.2,
            color=GREEN, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.2,
        )

        central_block = VGroup(central_rect, filter_text, input_arrows, output_arrow)
        central_block.move_to(np.array([0, 1.5, 0]))

        # small filter blocks around it
        block_size = (1.4, 0.7)
        block_labels = ["Low-pass", "High-pass", "Notch", "Band-pass"]
        block_positions = [
            np.array([0, 2.8, 0]),    # top
            np.array([2.9, 1.5, 0]),  # right
            np.array([0, 0.2, 0]),    # bottom
            np.array([-2.9, 1.5, 0]), # left
        ]
        small_blocks = []
        for pos, blabel in zip(block_positions, block_labels):
            rect = RoundedRectangle(
                width=block_size[0], height=block_size[1],
                fill_color=BLUE, fill_opacity=0.4,
                stroke_color=WHITE, stroke_width=1,
                corner_radius=0.1,
            )
            txt = Text(blabel, font_size=14, color=WHITE, weight=BOLD).move_to(rect)
            block = VGroup(rect, txt)
            block.move_to(pos)
            small_blocks.append(block)

        # dim all except Low‑pass (index 0)
        for i, blk in enumerate(small_blocks):
            if i != 0:
                blk.set_opacity(0.3)
            else:
                blk[0].set_fill(BLUE, opacity=0.9)
                blk.set_opacity(1)

        highlight = SurroundingRectangle(small_blocks[0], color=YELLOW, stroke_width=3)

        filter_system = VGroup(central_block, *small_blocks, highlight)
        self.play(FadeIn(filter_system, shift=UP * 0.2),
                  run_time=max(0.05, 1.74))   # 21.44 → 23.18

        # ----- BEAT 11: cycle filter highlight, flash icons -----
        signal_icon = icon_with_labels[0][0]
        noise_icon  = icon_with_labels[1][0]
        spec_icon   = icon_with_labels[2][0]
        analysis_icon = icon_with_labels[3][0]

        band_pass_block = small_blocks[3]   # left block
        low_pass_block  = small_blocks[0]   # top block

        # move to Band‑pass, indicate first two icons
        self.play(
            highlight.animate.move_to(band_pass_block.get_center()),
            Indicate(signal_icon, scale_factor=1.08, color=YELLOW),
            Indicate(noise_icon, scale_factor=1.08, color=ORANGE),
            run_time=max(0.05, 0.5),
        )
        # move back to Low‑pass, indicate remaining two icons
        self.play(
            highlight.animate.move_to(low_pass_block.get_center()),
            Indicate(spec_icon, scale_factor=1.08, color=TEAL),
            Indicate(analysis_icon, scale_factor=1.08, color=PURPLE),
            run_time=max(0.05, 0.5),
        )
        self.wait(max(0.05, 0.84))   # 23.18 → 25.02

        # ----- BEAT 12: hold until end -----
        self.wait(max(0.05, 0.83))   # 25.02 → 25.85