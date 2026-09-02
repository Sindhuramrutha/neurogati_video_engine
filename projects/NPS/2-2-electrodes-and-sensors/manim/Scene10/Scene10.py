ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene10(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # Coordinates / reusable positions
        # ------------------------------------------------------------------
        head_center = np.array([0, 0.2, 0])
        active_center = head_center + np.array([0.55, 0.1, 0])

        # ------------------------------------------------------------------
        # Beat 1 opening: brief previous-scene warning, then head + helmet
        # ------------------------------------------------------------------
        warn_tri = Polygon(
            np.array([-0.35, 0.25, 0]),
            np.array([0.35, 0.25, 0]),
            np.array([0, -0.35, 0]),
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
        )
        warn_exclaim = Text("!", font_size=28, weight="BOLD", color=BLACK)
        warn_exclaim.move_to(warn_tri.get_center() + DOWN * 0.02)
        prev_warning = VGroup(warn_tri, warn_exclaim).scale(0.55)
        prev_warning.move_to(ORIGIN)
        self.add(prev_warning)
        self.play(FadeOut(prev_warning), run_time=max(0.05, 0.66))

        # Main head / brain / helmet
        head = Ellipse(
            width=2.5,
            height=3.0,
            fill_color=GREY_B,
            fill_opacity=0.22,
            stroke_color=GREY_B,
            stroke_width=2.0,
        )
        head.move_to(head_center)

        brain_outline = Ellipse(
            width=1.8,
            height=2.3,
            fill_color=PURPLE,
            fill_opacity=0.0,
            stroke_color=PURPLE,
            stroke_width=2.0,
            stroke_opacity=0.55,
        )
        brain_outline.move_to(head_center)

        helmet_ring = Ellipse(
            width=3.8,
            height=4.2,
            stroke_color=GREY_B,
            stroke_width=1.5,
            fill_opacity=0.0,
        )
        helmet_ring.set_opacity(0.22)
        helmet_ring.move_to(head_center)

        title_meg = Text("MEG", font_size=54, weight="BOLD", color=YELLOW)
        title_sub = Text("Magnetoencephalography", font_size=20, color=WHITE)
        title_group = VGroup(title_meg, title_sub).arrange(DOWN, buff=0.10)
        title_group.move_to(np.array([0, 3.0, 0]))

        # Sensor coils as a VGroup of small rectangles around upper scalp
        coils = VGroup()
        for theta in np.linspace(0, PI, 16):
            point = head_center + np.array(
                [1.85 * np.cos(theta), 2.05 * np.sin(theta), 0]
            )
            coil = Rectangle(
                width=0.30,
                height=0.16,
                fill_color=BLUE,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=1.0,
            )
            coil.move_to(point)
            coils.add(coil)

        self.play(
            GrowFromCenter(head),
            FadeIn(brain_outline),
            FadeIn(helmet_ring),
            LaggedStart(*[FadeIn(c) for c in coils], lag_ratio=0.04),
            FadeIn(title_group),
            run_time=max(0.05, 2.20),
        )

        # ------------------------------------------------------------------
        # Gap 2.86-3.70
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.84))

        # ------------------------------------------------------------------
        # Beat 2: active neural population + first field lines +
        #          crossed-out "voltage"
        # ------------------------------------------------------------------
        self.play(coils.animate.set_opacity(0.30), run_time=max(0.05, 0.30))

        active_region = Circle(
            radius=0.13,
            fill_color=YELLOW,
            fill_opacity=1.0,
            stroke_width=0,
        )
        active_region.move_to(active_center)

        active_glow = Circle(
            radius=0.30,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=0,
        )
        active_glow.move_to(active_center)

        # Choose top coils for first few field lines
        yvals = [c.get_center()[1] for c in coils]
        basic_indices = sorted(range(len(coils)), key=lambda i: -yvals[i])[:4]

        def field_arrow(target):
            return Arrow(
                start=active_center,
                end=target.get_center(),
                path_arc=0.6,
                color=YELLOW,
                stroke_width=1.4,
                buff=0.05,
                max_tip_length_to_length_ratio=0.12,
            )

        basic_lines = VGroup(*[field_arrow(coils[i]) for i in basic_indices])

        self.play(
            FadeIn(active_region),
            FadeIn(active_glow),
            LaggedStart(*[Create(line) for line in basic_lines], lag_ratio=0.18),
            run_time=max(0.05, 0.70),
        )

        voltage_label = Text("voltage", font_size=30, color=WHITE)
        voltage_label.move_to(np.array([-4.8, 2.5, 0]))
        voltage_cross = Line(
            start=voltage_label.get_left() + LEFT * 0.08 + UP * 0.18,
            end=voltage_label.get_right() + RIGHT * 0.08 + DOWN * 0.18,
            color=RED,
            stroke_width=5,
        )
        voltage_group = VGroup(voltage_label, voltage_cross)

        self.play(
            FadeIn(voltage_label),
            Create(voltage_cross),
            run_time=max(0.05, 0.42),
        )

        self.play(
            active_region.animate.scale(1.12),
            active_glow.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=max(0.05, 0.30),
        )

        # ------------------------------------------------------------------
        # Gap 5.42-6.02: clean up crossed-out voltage
        # ------------------------------------------------------------------
        self.play(FadeOut(*voltage_group), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.20))

        # ------------------------------------------------------------------
        # Beat 3: brighter active region, more field lines, descriptor labels
        # ------------------------------------------------------------------
        self.play(
            active_region.animate.scale(1.15),
            active_glow.animate.scale(1.25).set_opacity(0.30),
            run_time=max(0.05, 0.40),
        )

        many_indices = sorted(range(len(coils)), key=lambda i: -yvals[i])[4:12]
        many_lines = VGroup(*[field_arrow(coils[i]) for i in many_indices])
        per_line = max(0.05, 1.00 / len(many_lines))
        for line, idx in zip(many_lines, many_indices):
            self.play(
                Create(line),
                coils[idx].animate.set_color(YELLOW).set_opacity(0.95),
                run_time=max(0.05, per_line),
            )

        all_field_lines = VGroup(*basic_lines, *many_lines)

        small_label = Text("extremely small", font_size=24, color=WHITE)
        small_label.move_to(np.array([4.9, 1.8, 0]))
        self.play(FadeIn(small_label), run_time=max(0.05, 0.30))
        self.play(Indicate(small_label, color=YELLOW, scale_factor=1.08), run_time=max(0.05, 0.40))

        magnetic_fields_label = Text("magnetic fields", font_size=24, color=WHITE)
        magnetic_fields_label.move_to(np.array([-4.9, 1.8, 0]))
        self.play(FadeIn(magnetic_fields_label), run_time=max(0.05, 0.30))
        self.play(
            Indicate(magnetic_fields_label, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.40),
        )

        neuronal_label = Text("neuronal activity", font_size=24, color=WHITE)
        neuronal_label.move_to(np.array([4.6, -0.9, 0]))
        self.play(FadeIn(neuronal_label), run_time=max(0.05, 0.30))
        self.play(
            Indicate(neuronal_label, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.40),
        )

        self.play(
            active_region.animate.scale(1.06),
            active_glow.animate.scale(1.08),
            rate_func=there_and_back,
            run_time=max(0.05, 0.74),
        )

        # ------------------------------------------------------------------
        # Gap 10.26-11.16
        # ------------------------------------------------------------------
        self.play(
            FadeOut(small_label),
            FadeOut(magnetic_fields_label),
            FadeOut(neuronal_label),
            run_time=max(0.05, 0.50),
        )
        self.wait(max(0.05, 0.40))

        # ------------------------------------------------------------------
        # Beat 4: EEG electrode crossed out, no-electrodes text
        # ------------------------------------------------------------------
        self.play(coils.animate.set_opacity(0.25), run_time=max(0.05, 0.45))

        eeg_electrode = Circle(
            radius=0.14,
            fill_color=YELLOW,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        eeg_electrode.move_to(head_center + UP * 1.30)
        self.play(FadeIn(eeg_electrode), run_time=max(0.05, 0.25))

        ee_cross = Line(
            start=eeg_electrode.get_center() + LEFT * 0.16 + UP * 0.16,
            end=eeg_electrode.get_center() + RIGHT * 0.16 + DOWN * 0.16,
            color=RED,
            stroke_width=5,
        )
        self.play(Create(ee_cross), run_time=max(0.05, 0.35))

        no_electrodes_text = Text(
            "does not use electrodes",
            font_size=30,
            weight="BOLD",
            color=YELLOW,
        )
        no_electrodes_text.move_to(np.array([0, -2.3, 0]))

        self.play(
            FadeOut(eeg_electrode),
            FadeOut(ee_cross),
            FadeIn(no_electrodes_text),
            run_time=max(0.05, 0.50),
        )

        self.play(coils.animate.set_opacity(1.0), run_time=max(0.05, 0.47))

        # ------------------------------------------------------------------
        # Gap 13.18-14.82
        # ------------------------------------------------------------------
        self.play(FadeOut(no_electrodes_text), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 1.24))

        # ------------------------------------------------------------------
        # Beat 5: bright helmet array with sensitivity halos + pointer label
        # ------------------------------------------------------------------
        halos = VGroup()
        for c in coils:
            halo = Circle(
                radius=0.30,
                fill_color=YELLOW,
                fill_opacity=0.08,
                stroke_color=YELLOW,
                stroke_width=1.0,
                stroke_opacity=0.7,
            )
            halo.move_to(c.get_center())
            halos.add(halo)

        self.play(
            coils.animate.set_color(BLUE).set_opacity(1.0),
            LaggedStart(*[FadeIn(h) for h in halos], lag_ratio=0.04),
            run_time=max(0.05, 1.20),
        )

        self.play(
            all_field_lines.animate.set_color(YELLOW).set_opacity(1.0),
            active_glow.animate.set_opacity(0.35),
            run_time=max(0.05, 0.80),
        )

        sensor_target = coils[basic_indices[1]]
        sensor_label = Text("magnetic sensor", font_size=20, color=YELLOW)
        sensor_label.next_to(sensor_target, RIGHT, buff=1.2)
        sensor_arrow = Arrow(
            start=sensor_label.get_left() + LEFT * 0.08,
            end=sensor_target.get_right() + RIGHT * 0.05,
            color=YELLOW,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.18,
        )
        self.play(
            FadeIn(sensor_label),
            Create(sensor_arrow),
            run_time=max(0.05, 1.00),
        )

        self.play(
            halos.animate.set_opacity(0.25),
            rate_func=there_and_back,
            run_time=max(0.05, 0.73),
        )
        self.play(
            halos.animate.set_opacity(0.25),
            rate_func=there_and_back,
            run_time=max(0.05, 0.73),
        )

        # ------------------------------------------------------------------
        # Gap 19.28-20.04
        # ------------------------------------------------------------------
        self.play(FadeOut(sensor_label), FadeOut(sensor_arrow), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.36))

        # ------------------------------------------------------------------
        # Beat 6: sensing technology differs split-panel
        # ------------------------------------------------------------------
        left_icon_group = VGroup(
            Circle(
                radius=0.12,
                fill_color=YELLOW,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=1.5,
            ),
            Text("EEG electrode", font_size=16, color=WHITE),
        ).arrange(DOWN, buff=0.08)

        right_icon_group = VGroup(
            Rectangle(
                width=0.30,
                height=0.18,
                fill_color=BLUE,
                fill_opacity=1.0,
                stroke_color=WHITE,
                stroke_width=1.5,
            ),
            Text("MEG sensor", font_size=16, color=WHITE),
        ).arrange(DOWN, buff=0.08)

        icons_row = VGroup(left_icon_group, right_icon_group).arrange(RIGHT, buff=1.0)

        callout_text = Text(
            "sensing technology differs",
            font_size=26,
            weight="BOLD",
            color=YELLOW,
        )
        callout_group = VGroup(callout_text, icons_row).arrange(DOWN, buff=0.22)
        callout_group.move_to(np.array([0, -2.0, 0]))

        self.play(
            coils.animate.set_opacity(0.25),
            all_field_lines.animate.set_opacity(0.25),
            halos.animate.set_opacity(0.15),
            run_time=max(0.05, 0.40),
        )
        self.play(FadeIn(callout_group), run_time=max(0.05, 0.62))
        self.play(
            Indicate(callout_text, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.62),
        )

        # ------------------------------------------------------------------
        # Gap 21.68-22.16
        # ------------------------------------------------------------------
        self.wait(max(0.05, 0.48))

        # ------------------------------------------------------------------
        # Beat 7: same purpose, convergent arrows
        # ------------------------------------------------------------------
        self.play(FadeOut(callout_group), run_time=max(0.05, 0.30))

        purpose_text = Text(
            "purpose remains the same",
            font_size=26,
            weight="BOLD",
            color=YELLOW,
        )
        purpose_text.move_to(np.array([0, -1.5, 0]))

        left_circle = Circle(
            radius=0.11,
            fill_color=YELLOW,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        left_cross = Line(
            start=left_circle.get_center() + LEFT * 0.10 + UP * 0.10,
            end=left_circle.get_center() + RIGHT * 0.10 + DOWN * 0.10,
            color=RED,
            stroke_width=3,
        )
        left_icon = VGroup(left_circle, left_cross)
        left_icon.move_to(np.array([-3.8, -2.3, 0]))

        right_icon_rect = Rectangle(
            width=0.28,
            height=0.16,
            fill_color=BLUE,
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        right_icon_rect.move_to(np.array([3.8, -2.3, 0]))

        converge_target = Dot(
            point=np.array([0, -3.0, 0]),
            radius=0.08,
            color=GREEN,
        )

        arr_left = Arrow(
            start=left_icon.get_right(),
            end=converge_target.get_left(),
            color=GREEN,
            stroke_width=3,
            buff=0.1,
        )
        arr_right = Arrow(
            start=right_icon_rect.get_left(),
            end=converge_target.get_right() + RIGHT * 0.05,
            color=GREEN,
            stroke_width=3,
            buff=0.1,
        )

        self.play(
            coils.animate.set_opacity(1.0),
            all_field_lines.animate.set_opacity(1.0),
            halos.animate.set_opacity(1.0),
            FadeIn(purpose_text),
            run_time=max(0.05, 0.36),
        )
        self.play(
            FadeIn(left_icon),
            FadeIn(right_icon_rect),
            Create(arr_left),
            Create(arr_right),
            FadeIn(converge_target),
            run_time=max(0.05, 0.60),
        )
        self.play(
            Indicate(converge_target, color=GREEN, scale_factor=1.15),
            run_time=max(0.05, 0.30),
        )

        purpose_group = VGroup(
            purpose_text,
            left_icon,
            right_icon_rect,
            converge_target,
            arr_left,
            arr_right,
        )

        # ------------------------------------------------------------------
        # Gap 23.72-24.26: clear purpose layout
        # ------------------------------------------------------------------
        self.play(FadeOut(*purpose_group), run_time=max(0.05, 0.54))

        # ------------------------------------------------------------------
        # Beat 8: bottom acquisition chain
        # ------------------------------------------------------------------
        block_names = [
            "MEG sensors",
            "amplification",
            "filtering",
            "digitization",
            "recording",
        ]
        chain_blocks = []
        for name in block_names:
            rect = Rectangle(
                width=2.0,
                height=0.65,
                fill_color=BLUE,
                fill_opacity=0.25,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            label = Text(name, font_size=16, color=WHITE).scale_to_fit_width(1.7)
            block = VGroup(rect, label)
            chain_blocks.append(block)

        first_rect = chain_blocks[0][0]
        first_label = chain_blocks[0][1]
        first_rect.set_fill(YELLOW, opacity=0.9)
        first_rect.set_stroke(YELLOW, width=4)
        first_label.set_color(BLACK)

        blocks_row = VGroup(*chain_blocks).arrange(RIGHT, buff=0.45)
        chain_arrows = VGroup()
        for i in range(len(chain_blocks) - 1):
            arrow = Arrow(
                start=chain_blocks[i].get_right(),
                end=chain_blocks[i + 1].get_left(),
                color=GREY_B,
                stroke_width=3,
                buff=0.05,
            )
            chain_arrows.add(arrow)

        chain_group = VGroup(blocks_row, chain_arrows)
        chain_group.move_to(np.array([0, -2.8, 0]))

        connector = Arrow(
            start=np.array([0, -1.4, 0]),
            end=chain_blocks[0].get_top() + UP * 0.1,
            color=YELLOW,
            stroke_width=3,
            buff=0.1,
        )
        chain_link_label = Text("sensor output", font_size=16, color=YELLOW)
        chain_link_label.next_to(connector, RIGHT, buff=0.12)

        final_indices = sorted(range(len(coils)), key=lambda i: yvals[i])[:3]
        final_lines = VGroup(*[field_arrow(coils[i]) for i in final_indices])

        self.play(FadeIn(chain_group), run_time=max(0.05, 0.90))
        self.play(
            Create(connector),
            FadeIn(chain_link_label),
            run_time=max(0.05, 0.60),
        )
        self.play(
            LaggedStart(*[Create(line) for line in final_lines], lag_ratio=0.20),
            first_rect.animate.set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=1.0),
            run_time=max(0.05, 0.90),
        )
        self.play(
            Indicate(chain_blocks[0], color=YELLOW, scale_factor=1.07),
            run_time=max(0.05, 0.70),
        )
        self.play(
            active_region.animate.scale(1.06),
            active_glow.animate.scale(1.08),
            rate_func=there_and_back,
            run_time=max(0.05, 1.12),
        )
        self.wait(max(0.05, 0.05))