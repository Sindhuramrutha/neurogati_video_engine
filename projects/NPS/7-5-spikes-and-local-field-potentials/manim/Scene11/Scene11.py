ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {
    'heart': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\test_heart.svg',
    'brain': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\brain_test.svg',
    'stopwatch': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\stopwatch.svg',
    'activity': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\activity.svg',
    'soundwave': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\soundwave.svg',
    'grid_matrix': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\grid-3x3-gap-fill.svg',
    'bar_chart': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\bar-chart.svg',
    'graph_trend': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\graph-up-arrow.svg',
    'cpu': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\cpu.svg',
    'funnel': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\funnel.svg',
    'table': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\table.svg',
    'hospital': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\hospital.svg',
    'capsule': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\capsule.svg',
    'clipboard_pulse': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\clipboard2-pulse.svg',
    'hand': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\hand-index-thumb.svg',
    'broadcast': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\broadcast-pin.svg',
    'gear': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\gear.svg',
    'arrow_repeat': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\arrow-repeat.svg',
    'lightbulb': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\lightbulb.svg',
    'bell': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\bell.svg',
    'check_circle': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\check-circle.svg',
    'x_circle': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\x-circle.svg',
    'rulers': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\rulers.svg',
    'puzzle': r'C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\puzzle.svg',
}


class Scene11(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------------
        # helpers
        # ------------------------------------------------------------------
        def rotated_rect_group(label, icon, color, icon_h=0.55):
            icon = icon.set_color(color).scale_to_fit_height(icon_h)
            txt = Text(label, font_size=16, color=WHITE)
            txt.next_to(icon, DOWN, buff=0.08)
            return VGroup(icon, txt)

        def faint_trace(center, amp=0.18, n=2.4, color=YELLOW, x_span=2.4,
                        stroke_width=2, opacity=1.0):
            return FunctionGraph(
                lambda x: amp * np.sin(2 * np.pi * n * x / x_span),
                x_range=[-x_span / 2, x_span / 2, 0.03],
                color=color,
                stroke_width=stroke_width,
            ).move_to(center).set_opacity(opacity)

        # ------------------------------------------------------------------
        # previous scene dim thumbnail, then new scene fades in
        # ------------------------------------------------------------------
        prev_panels = VGroup()
        for k, xc in enumerate([-4.2, 0.0, 4.2]):
            rect = Rectangle(
                width=3.0, height=2.1,
                fill_color=GREY_B, fill_opacity=0.20,
                stroke_color=GREY_B, stroke_width=2,
            ).move_to([xc, 0, 0])
            trace = FunctionGraph(
                lambda x: 0.18 * np.sin(2 * x + 1.2 * k),
                x_range=[xc - 0.8, xc + 0.8, 0.03],
                color=GREY_B,
                stroke_width=2,
            ).move_to([xc, 0, 0])
            prev_panels.add(VGroup(rect, trace))
        prev_panels.scale_to_fit_width(11.5).set_opacity(0.45)
        self.add(prev_panels)

        # human figure, profile facing right, dark gray-blue tones
        head = Ellipse(
            width=0.58, height=0.78,
            fill_color=GREY_B, fill_opacity=1,
            stroke_color=BLUE, stroke_width=3,
        ).move_to([-3.55, 0.45, 0])
        nose = Polygon(
            head.get_right(),
            head.get_right() + RIGHT * 0.16 + DOWN * 0.04,
            head.get_right() + RIGHT * 0.16 + UP * 0.08,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_color=BLUE,
            stroke_width=2,
        )
        body = RoundedRectangle(
            width=1.7, height=1.6, corner_radius=0.28,
            fill_color=GREY_B, fill_opacity=1,
            stroke_color=BLUE, stroke_width=3,
        ).move_to([-3.65, -0.85, 0])
        person_group = VGroup(head, nose, body)

        device = VGroup(
            RoundedRectangle(
                width=0.26, height=0.20, corner_radius=0.05,
                fill_color=GREY_B, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ),
            Dot(radius=0.035, color=GREEN, fill_opacity=1),
        ).move_to(head.get_top() + UP * 0.07)

        cable = Line(
            device.get_left(),
            np.array([-6.8, device.get_center()[1], 0]),
            color=GREY_B,
            stroke_width=2.5,
        )

        title = Text("neural prosthesis", font_size=40, color=WHITE,
                     weight=BOLD).move_to([0, 2.65, 0])
        underline = Line(
            title.get_left() + DOWN * 0.16,
            title.get_right() + DOWN * 0.16,
            color=YELLOW,
            stroke_width=3,
        )
        title_group = VGroup(title, underline)

        # beat 1
        self.play(FadeOut(prev_panels), run_time=max(0.05, 0.20))
        self.play(FadeIn(person_group, device, cable), run_time=max(0.05, 0.16))
        self.play(device.animate.set_color(YELLOW).set_stroke(YELLOW, width=2),
                  run_time=max(0.05, 0.44))
        self.wait(max(0.05, 0.30))
        self.play(FadeIn(title_group), run_time=max(0.05, 0.34))

        # beat 2
        system_rect = DashedVMobject(
            Rectangle(width=11.2, height=5.7),
            num_dashes=52,
        )
        system_rect.set_stroke(WHITE, width=2)
        system_rect.move_to([0.25, 0.0, 0])

        self.wait(max(0.05, 0.10))
        self.play(Create(system_rect), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.16))

        cable_start = device.get_left()
        cable_end = cable.get_end()

        # 2.10-2.36 low frequency pulse
        pulse = Dot(cable_start, radius=0.045, color=YELLOW, fill_opacity=1)
        self.add(pulse)
        self.play(pulse.animate.move_to(cable_end), run_time=max(0.05, 0.26))
        self.remove(pulse)

        # 2.36 high frequency pulses
        for _ in range(2):
            p = Dot(cable_start, radius=0.045, color=YELLOW, fill_opacity=1)
            self.add(p)
            self.play(p.animate.move_to(cable_end), run_time=max(0.05, 0.13))
            self.remove(p)

        signal_label = Text("neural signals", font_size=17, color=WHITE)
        wave_icon = SVGMobject(ASSET_PATHS["activity"]).set_color(YELLOW)
        wave_icon.scale_to_fit_height(0.34)
        signal_label_group = VGroup(wave_icon, signal_label).arrange(RIGHT, buff=0.10)
        signal_label_group.next_to(cable, UP, buff=0.14).shift(RIGHT * 1.2)

        self.play(FadeIn(signal_label_group), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.10))

        # beat 3: restore / replace / assist icons
        restore_icon = rotated_rect_group(
            "restore",
            SVGMobject(ASSET_PATHS["arrow_repeat"]),
            YELLOW,
        )
        replace_icon = VGroup(
            Rectangle(width=0.16, height=0.35, fill_color=TEAL, fill_opacity=0.9,
                      stroke_color=WHITE, stroke_width=1.5).move_to(LEFT * 0.14),
            Rectangle(width=0.16, height=0.35, fill_color=BLUE, fill_opacity=0.8,
                      stroke_color=WHITE, stroke_width=1.5).move_to(RIGHT * 0.14),
            Arrow(LEFT * 0.35, RIGHT * 0.35, color=YELLOW, stroke_width=3.5,
                  buff=0.04, max_tip_length_to_length_ratio=0.3),
        )
        replace_label = Text("replace", font_size=16, color=WHITE)
        replace_label.next_to(replace_icon, DOWN, buff=0.08)
        replace_icon = VGroup(replace_icon, replace_label)

        assist_icon = VGroup(
            SVGMobject(ASSET_PATHS["hand"]).set_color(YELLOW).scale_to_fit_height(0.62),
            Text("assist", font_size=16, color=WHITE).next_to(
                SVGMobject(ASSET_PATHS["hand"]).set_color(YELLOW).scale_to_fit_height(0.62),
                DOWN, buff=0.08,
            ),
        )
        assist_icon = VGroup(
            SVGMobject(ASSET_PATHS["hand"]).set_color(YELLOW).scale_to_fit_height(0.62),
            Text("assist", font_size=16, color=WHITE),
        )
        assist_icon.arrange(DOWN, buff=0.08)

        icons_group = VGroup(restore_icon, replace_icon, assist_icon)
        icons_group.arrange(RIGHT, buff=0.55)
        icons_group.move_to([-3.2, 1.95, 0])

        self.wait(max(0.05, 0.40))  # to 3.42
        self.play(SpinInFromNothing(restore_icon, angle=PI / 2, run_time=max(0.05, 0.70)))
        self.play(FadeIn(replace_icon), run_time=max(0.05, 0.88))
        self.play(FadeIn(assist_icon), run_time=max(0.05, 0.44))

        # pulse once in unison at 5.44
        self.play(
            *[Indicate(icon, scale_factor=1.18, color=YELLOW) for icon in icons_group],
            run_time=max(0.05, 0.88),
        )

        # dim at 6.32
        self.play(icons_group.animate.set_opacity(0.50), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.40))

        # 7.02 caption
        caption_phrase = Text(
            "restore, replace, or assist lost function",
            font_size=27,
            color=WHITE,
            weight=BOLD,
        )
        caption_phrase.scale_to_fit_width(10.5)
        caption_phrase.move_to([0, 1.55, 0])

        self.play(FadeOut(icons_group), FadeIn(caption_phrase), run_time=max(0.05, 0.28))
        self.wait(max(0.05, 0.88))

        # beat 4: caption out, person brightens, panel, waveforms, cluster, bubble
        self.play(FadeOut(caption_phrase), person_group.animate.set_stroke(BLUE, width=5),
                  device.animate.set_color(YELLOW), run_time=max(0.05, 0.20))

        for _ in range(2):
            p = Dot(cable_start, radius=0.05, color=YELLOW, fill_opacity=1)
            self.add(p)
            self.play(p.animate.move_to(cable_end), run_time=max(0.05, 0.43))
            self.remove(p)

        # right analysis panel
        panel_bg = Rectangle(
            width=4.6, height=3.2,
            fill_color=BLACK, fill_opacity=0.75,
            stroke_color=GREY_B, stroke_width=2,
        )
        panel_center = np.array([3.95, -0.2, 0])
        panel_bg.move_to(panel_center)
        grid_lines = VGroup()
        for dx in np.linspace(-2.0, 2.0, 9):
            grid_lines.add(
                Line(panel_center + [dx, -1.45, 0],
                     panel_center + [dx, 1.45, 0],
                     color=GREY_B, stroke_width=0.8, stroke_opacity=0.35)
            )
        for dy in np.linspace(-1.3, 1.3, 7):
            grid_lines.add(
                Line(panel_center + [-2.1, dy, 0],
                     panel_center + [2.1, dy, 0],
                     color=GREY_B, stroke_width=0.8, stroke_opacity=0.35)
            )
        panel_group = VGroup(panel_bg, grid_lines)

        self.play(FadeIn(panel_group), run_time=max(0.05, 0.28))

        waveform_centers = [
            panel_center + UP * 0.55,
            panel_center,
            panel_center + DOWN * 0.55,
        ]
        waveforms_group = VGroup()
        for c in waveform_centers:
            waveforms_group.add(
                FunctionGraph(
                    lambda x: 0.22 * np.sin(3.2 * x + 0.4),
                    x_range=[-1.4, 1.4, 0.03],
                    color=YELLOW,
                    stroke_width=2.5,
                ).move_to(c)
            )
        for wf in waveforms_group:
            self.play(Create(wf), run_time=max(0.05, 0.30))

        cluster_a = VGroup(
            Dot(panel_center + LEFT * 0.8 + UP * 0.5, radius=0.045, color=YELLOW),
            Arrow(LEFT * 0.10, RIGHT * 0.10, color=GREY_B, stroke_width=2,
                  buff=0.02, max_tip_length_to_length_ratio=0.35).move_to(
                panel_center + LEFT * 0.8 + UP * 0.5),
        )
        cluster_b = VGroup(
            Dot(panel_center + RIGHT * 0.9 + DOWN * 0.4, radius=0.045, color=YELLOW),
            Arrow(LEFT * 0.10, RIGHT * 0.10, color=GREY_B, stroke_width=2,
                  buff=0.02, max_tip_length_to_length_ratio=0.35).move_to(
                panel_center + RIGHT * 0.9 + DOWN * 0.4),
        )
        cluster_c = VGroup(
            Dot(panel_center + LEFT * 0.4 + DOWN * 0.6, radius=0.045, color=YELLOW),
            Arrow(LEFT * 0.10, RIGHT * 0.10, color=GREY_B, stroke_width=2,
                  buff=0.02, max_tip_length_to_length_ratio=0.35).move_to(
                panel_center + LEFT * 0.4 + DOWN * 0.6),
        )
        cluster_group = VGroup(cluster_a, cluster_b, cluster_c)

        self.play(FadeOut(waveforms_group), FadeIn(cluster_group), run_time=max(0.05, 0.06))

        self.play(Indicate(person_group, scale_factor=1.05, color=YELLOW),
                  run_time=max(0.05, 0.56))

        head_to_panel_arrow = DashedLine(
            head.get_right() + RIGHT * 0.25,
            panel_bg.get_left() + LEFT * 0.25,
            color=YELLOW,
            dash_length=0.08,
            stroke_width=3,
        )
        head_to_panel_arrow.add_tip(at_start=False)
        self.play(Create(head_to_panel_arrow), run_time=max(0.05, 0.26))

        # thought bubble with stick figure arm
        bubble_outline = VGroup(
            Ellipse(width=1.5, height=0.95, color=WHITE, stroke_width=2),
            Circle(radius=0.05, color=WHITE, stroke_width=1).move_to(
                head.get_top() + UP * 0.10),
            Circle(radius=0.04, color=WHITE, stroke_width=1).move_to(
                head.get_top() + UP * 0.30 + LEFT * 0.12),
        )
        bubble_center = head.get_top() + UP * 0.85
        bubble_outline[0].move_to(bubble_center)

        shoulder = bubble_center + LEFT * 0.45 + DOWN * 0.25
        elbow = shoulder + RIGHT * 0.35 + UP * 0.12
        hand_pos = elbow + RIGHT * 0.38 + DOWN * 0.18
        upper_arm = Line(shoulder, elbow, color=WHITE, stroke_width=3)
        forearm_line = Line(elbow, hand_pos, color=WHITE, stroke_width=3)
        hand_dot = Dot(hand_pos, radius=0.05, color=ORANGE, fill_opacity=1)
        forearm_group = VGroup(forearm_line, hand_dot)
        arm_in_bubble = VGroup(upper_arm, forearm_line, hand_dot)
        thought_bubble_group = VGroup(bubble_outline, arm_in_bubble)

        self.play(FadeIn(thought_bubble_group), run_time=max(0.05, 0.38))

        # beat 5: inset panel, spikes, connection, arm highlight/motion, playback
        self.wait(max(0.05, 0.92))

        inset_panel = Rectangle(
            width=2.3, height=1.4,
            fill_color=BLACK, fill_opacity=0.8,
            stroke_color=GREY_B, stroke_width=2,
        ).move_to([-4.85, -2.35, 0])
        inset_center = inset_panel.get_center()
        self.wait(max(0.05, 0.36))
        self.play(FadeIn(inset_panel), run_time=max(0.05, 0.36))

        spike_ticks = VGroup()
        for x in np.linspace(-0.85, 0.85, 7):
            spike_ticks.add(
                Line(inset_center + [x, -0.45, 0],
                     inset_center + [x, -0.10, 0],
                     color=YELLOW, stroke_width=2.5)
            )
        self.play(
            LaggedStart(*[Create(tick) for tick in spike_ticks],
                        lag_ratio=0.25),
            run_time=max(0.05, 0.26),
        )

        extra_ticks = VGroup()
        for x in np.linspace(-0.7, 0.7, 5):
            extra_ticks.add(
                Line(inset_center + [x + 0.09, -0.55, 0],
                     inset_center + [x + 0.09, -0.20, 0],
                     color=YELLOW, stroke_width=2)
            )
        self.play(Create(extra_ticks), run_time=max(0.05, 0.52))

        connect_line_a = Line(
            inset_panel.get_top() + LEFT * 0.3,
            bubble_outline[0].get_bottom() + LEFT * 0.3,
            color=GREY_B,
            stroke_width=1.5,
        )
        connect_line_b = Line(
            inset_panel.get_top() + RIGHT * 0.3,
            bubble_outline[0].get_bottom() + RIGHT * 0.3,
            color=GREY_B,
            stroke_width=1.5,
        )
        connecting_lines = VGroup(connect_line_a, connect_line_b)
        self.play(Create(connecting_lines), run_time=max(0.05, 0.44))

        self.play(connecting_lines.animate.set_color(YELLOW).set_stroke(width=3.5),
                  run_time=max(0.05, 0.62))

        self.play(Indicate(hand_dot, scale_factor=1.8, color=ORANGE), run_time=max(0.05, 0.66))
        self.play(Indicate(arm_in_bubble, scale_factor=1.12, color=ORANGE),
                  run_time=max(0.05, 0.34))

        elbow_pos = elbow
        self.play(Rotate(forearm_group, angle=0.48, about_point=elbow_pos),
                  run_time=max(0.05, 0.56))
        self.play(Rotate(forearm_group, angle=-0.48, about_point=elbow_pos),
                  run_time=max(0.05, 0.50))

        playback_lines = DashedVMobject(
            Rectangle(width=2.55, height=1.65),
            num_dashes=28,
        ).move_to(inset_panel).set_stroke(YELLOW, width=2)
        repeat_ticks = spike_ticks.copy().set_opacity(0.45).shift(RIGHT * 0.18)

        self.play(FadeIn(playback_lines), FadeIn(repeat_ticks), run_time=max(0.05, 0.64))

        mag_circle = Circle(radius=0.30, color=WHITE, stroke_width=2,
                            fill_opacity=0)
        mag_handle = Line(RIGHT * 0.18, RIGHT * 0.48 + DOWN * 0.12,
                          color=WHITE, stroke_width=3)
        mag_glass = VGroup(mag_circle, mag_handle)
        mag_glass.move_to(inset_panel.get_left() + RIGHT * 0.2 + UP * 0.3)
        scan_rect = Rectangle(
            width=0.10, height=1.0,
            fill_color=YELLOW, fill_opacity=0.35, stroke_width=0,
        ).move_to(inset_panel.get_left() + RIGHT * 0.2)
        self.add(mag_glass, scan_rect)
        self.play(
            mag_glass.animate.move_to(inset_panel.get_right() + LEFT * 0.2 + UP * 0.3),
            scan_rect.animate.move_to(inset_panel.get_right() + LEFT * 0.2),
            run_time=max(0.05, 0.32),
        )
        self.remove(mag_glass, scan_rect)

        # beat 6: fade inset/bubble, build pipeline
        old_vis = VGroup(
            panel_group,
            cluster_group,
            head_to_panel_arrow,
            thought_bubble_group,
            inset_panel,
            spike_ticks,
            extra_ticks,
            connecting_lines,
            playback_lines,
            repeat_ticks,
        )
        self.wait(max(0.05, 1.02 - 0.32))  # end of beat5 already at 18.18
        # (previous action ended at 18.18; now wait to 19.20)
        self.wait(max(0.05, 1.02))

        self.play(FadeOut(old_vis), run_time=max(0.05, 0.10))

        block_colors = [ORANGE, TEAL, GREEN, BLUE, PURPLE]
        block_label_texts = [
            "Neural recording",
            "Preprocessing",
            "Feature extraction",
            "Decoding",
            "Device control",
        ]

        block_groups = []
        block_rects = []
        block_labels = []
        for lab, col in zip(block_label_texts, block_colors):
            rect = RoundedRectangle(
                width=1.05, height=0.95, corner_radius=0.12,
                fill_color=GREY, fill_opacity=0.08,
                stroke_color=GREY_B, stroke_width=2,
            )
            try:
                rect.corner_radius = 0.12
            except AttributeError:
                pass
            lbl = Text(lab, font_size=12, color=GREY_B, weight=BOLD)
            lbl.scale_to_fit_width(0.95)
            lbl.move_to(rect.get_center())
            lbl.set_opacity(0.55)
            block_groups.append(VGroup(rect, lbl))
            block_rects.append(rect)
            block_labels.append(lbl)

        pipeline_blocks = VGroup(*block_groups)
        pipeline_blocks.arrange(RIGHT, buff=0.65)
        pipeline_blocks.move_to([1.5, -0.6, 0])

        pipeline_arrows = VGroup()
        for i in range(4):
            arrow = Arrow(
                block_rects[i].get_right(),
                block_rects[i + 1].get_left(),
                color=GREY_B,
                stroke_width=3,
                buff=0.10,
                max_tip_length_to_length_ratio=0.30,
                max_stroke_width_to_length_ratio=5,
            )
            pipeline_arrows.add(arrow)

        pipeline_caption = Text(
            "simplified neural prosthesis pipeline",
            font_size=24,
            color=WHITE,
            weight=BOLD,
        )
        pipeline_caption.next_to(pipeline_blocks, UP, buff=0.25)

        self.play(FadeIn(pipeline_blocks), FadeIn(pipeline_arrows), run_time=max(0.05, 0.28))
        self.play(block_labels[0].animate.set_color(WHITE).set_opacity(1),
                  run_time=max(0.05, 0.05))
        self.play(FadeIn(pipeline_caption), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 1.51))

        # first block brightens
        self.play(
            block_rects[0].animate.set_fill(ORANGE, opacity=0.35).set_stroke(ORANGE, width=3),
            run_time=max(0.05, 0.76),
        )
        self.wait(max(0.05, 0.00))  # placeholder clarity; replaced by next exact wait below

        electrode_icon = VGroup(
            Line(UP * 0.20, DOWN * 0.20, color=WHITE, stroke_width=2),
            Dot(DOWN * 0.28, radius=0.04, color=YELLOW, fill_opacity=1),
        ).move_to(block_rects[0].get_bottom() + UP * 0.30)
        self.play(FadeIn(electrode_icon), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.84))

        self.play(
            block_rects[1].animate.set_fill(TEAL, opacity=0.35).set_stroke(TEAL, width=3),
            block_labels[1].animate.set_color(WHITE).set_opacity(1),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 0.90))

        self.play(
            block_rects[2].animate.set_fill(GREEN, opacity=0.25).set_stroke(GREEN, width=3),
            block_labels[2].animate.set_color(WHITE).set_opacity(1),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 1.26))

        self.play(
            block_rects[3].animate.set_fill(BLUE, opacity=0.25).set_stroke(BLUE, width=3),
            block_labels[3].animate.set_color(WHITE).set_opacity(1),
            run_time=max(0.05, 0.30),
        )
        self.wait(max(0.05, 0.76))

        self.play(
            block_rects[4].animate.set_fill(PURPLE, opacity=0.30).set_stroke(PURPLE, width=3),
            block_labels[4].animate.set_color(WHITE).set_opacity(1),
            run_time=max(0.05, 0.30),
        )
        self.play(
            LaggedStart(*[Indicate(a, color=YELLOW, scale_factor=1.06)
                           for a in pipeline_arrows],
                        lag_ratio=0.20),
            run_time=max(0.05, 0.36),
        )

        # beat 7: signal flows into first block then preprocessing
        self.play(Indicate(person_group, scale_factor=1.06, color=YELLOW),
                  run_time=max(0.05, 1.06))

        stream_path = Line(
            device.get_center(),
            block_rects[0].get_left() + LEFT * 0.15,
            path_arc=-0.80,
            color=YELLOW,
            stroke_width=2.5,
        )
        self.play(Create(stream_path), run_time=max(0.05, 0.50))

        waveform_block0 = FunctionGraph(
            lambda x: 0.24 * np.sin(6.0 * x),
            x_range=[-0.80, 0.80, 0.02],
            color=YELLOW,
            stroke_width=2.5,
        ).move_to(block_rects[0])
        self.play(Create(waveform_block0), run_time=max(0.05, 0.22))
        self.play(waveform_block0.animate.set_stroke(color=WHITE, width=4),
                  run_time=max(0.05, 0.40))

        self.play(pipeline_arrows[0].animate.set_color(YELLOW).set_stroke(width=5),
                  run_time=max(0.05, 0.42))

        flow_dot = Dot(block_rects[0].get_right(), radius=0.06, color=YELLOW,
                       fill_opacity=1)
        self.add(flow_dot)
        self.play(flow_dot.animate.move_to(block_rects[1].get_left()),
                  run_time=max(0.05, 0.66))
        self.remove(flow_dot)

        noisy_wave = FunctionGraph(
            lambda x: 0.18 * np.sin(7.0 * x) + 0.09 * np.sin(23.0 * x),
            x_range=[-0.75, 0.75, 0.02],
            color=WHITE,
            stroke_width=2,
        ).move_to(block_rects[1])
        clean_wave = FunctionGraph(
            lambda x: 0.28 * np.sin(5.0 * x),
            x_range=[-0.75, 0.75, 0.02],
            color=TEAL,
            stroke_width=3,
        ).move_to(block_rects[1])
        filter_sweep = Line(
            block_rects[1].get_left() + RIGHT * 0.05 + UP * 0.35,
            block_rects[1].get_left() + RIGHT * 0.05 + DOWN * 0.35,
            color=YELLOW,
            stroke_width=3,
        )

        self.play(Create(noisy_wave), run_time=max(0.05, 0.10))
        self.play(
            Transform(noisy_wave, clean_wave),
            filter_sweep.animate.move_to(block_rects[1].get_right() + LEFT * 0.05),
            run_time=max(0.05, 0.54),
        )
        self.remove(filter_sweep)

        filtered_label = Text("filtered", font_size=11, color=YELLOW)
        aligned_label = Text("aligned", font_size=11, color=TEAL)
        filtered_label.next_to(clean_wave, UP, buff=0.06)
        aligned_label.next_to(clean_wave, DOWN, buff=0.06)
        self.play(FadeIn(filtered_label, aligned_label), run_time=max(0.05, 0.19))
        self.play(FadeOut(filtered_label, aligned_label), run_time=max(0.05, 0.19))

        # beat 8: feature extraction expansion and spike-based mini-cards
        self.wait(max(0.05, 0.74))
        self.play(pipeline_arrows[1].animate.set_color(YELLOW).set_stroke(width=5),
                  run_time=max(0.05, 0.30))

        feature_rect = block_rects[2]
        feature_label = block_labels[2]
        feature_center = feature_rect.get_center()
        expanded_feature = RoundedRectangle(
            width=2.8, height=2.8, corner_radius=0.18,
            fill_color=GREEN, fill_opacity=0.14,
            stroke_color=GREEN, stroke_width=3,
        ).move_to(feature_center)

        top_panel = Rectangle(
            width=2.5, height=1.6,
            fill_color=BLACK, fill_opacity=0.55,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(feature_center + UP * 0.45)
        bottom_panel = Rectangle(
            width=2.5, height=0.9,
            fill_color=BLACK, fill_opacity=0.55,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(feature_center + DOWN * 0.95)

        top_label = Text("Spike-based", font_size=15, color=WHITE, weight=BOLD)
        top_label.move_to(top_panel.get_top() + DOWN * 0.18)
        bottom_label = Text("LFP-based", font_size=15, color=WHITE, weight=BOLD)
        bottom_label.move_to(bottom_panel.get_top() + DOWN * 0.16)

        subpanels_group = VGroup(top_panel, bottom_panel, top_label, bottom_label)

        self.play(
            Transform(feature_rect, expanded_feature),
            feature_label.animate.move_to(feature_center + UP * 1.12).set_color(YELLOW),
            run_time=max(0.05, 0.30),
        )
        self.play(FadeIn(subpanels_group), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.72))

        # clean signal enters and splits
        signal_dot = Dot(block_rects[1].get_right(), radius=0.055, color=TEAL,
                         fill_opacity=1)
        self.add(signal_dot)
        self.play(signal_dot.animate.move_to(feature_center), run_time=max(0.05, 0.30))
        self.play(signal_dot.animate.move_to(top_panel.get_center()), run_time=max(0.05, 0.20))
        self.remove(signal_dot)
        self.wait(max(0.05, 0.78))

        # spike-train illustration at top
        spike_train = VGroup()
        for x in np.linspace(-0.9, 0.9, 7):
            spike_train.add(
                Line(top_panel.get_top() + [x, -0.45, 0],
                     top_panel.get_top() + [x, -0.20, 0],
                     color=YELLOW, stroke_width=2)
            )
        self.play(Create(spike_train), run_time=max(0.05, 0.55))
        self.wait(max(0.05, 1.03))

        self.play(Indicate(top_panel, scale_factor=1.05, color=YELLOW),
                  run_time=max(0.05, 0.36))

        card_area_outline = DashedVMobject(
            Rectangle(width=2.3, height=1.25),
            num_dashes=24,
        ).move_to(top_panel.get_center()).set_stroke(YELLOW, width=2)
        self.play(FadeIn(card_area_outline), run_time=max(0.05, 0.58))

        # four mini-cards
        def make_card(illustration, label):
            card_bg = RoundedRectangle(
                width=0.95, height=0.52, corner_radius=0.05,
                fill_color=GREY, fill_opacity=0.18,
                stroke_color=WHITE, stroke_width=1,
            )
            illustration.scale_to_fit_width(0.80)
            illustration.scale_to_fit_height(0.30)
            illustration.move_to(card_bg.get_center() + UP * 0.04)
            txt = Text(label, font_size=7, color=WHITE)
            txt.next_to(card_bg, DOWN, buff=0.04)
            return VGroup(card_bg, illustration, txt)

        # spike counts card
        card1_bars = VGroup()
        card1_counts = VGroup()
        card1_center = ORIGIN
        bar_heights = [0.07, 0.13, 0.10, 0.17, 0.12]
        for i, h in enumerate(bar_heights):
            bar = Rectangle(width=0.08, height=h, fill_color=ORANGE,
                            fill_opacity=1, stroke_width=0)
            bar.move_to(card1_center + LEFT * 0.16 + RIGHT * 0.08 * i + DOWN * 0.05)
            card1_bars.add(bar)
            c = Text(str(i + 2), font_size=5.5, color=WHITE)
            c.next_to(bar, UP, buff=0.01)
            card1_counts.add(c)
        card1_ill = VGroup(card1_bars, card1_counts)
        card1 = make_card(card1_ill, "spike counts")

        # firing rates card
        card2_line = FunctionGraph(
            lambda x: 0.12 * np.sin(2.2 * x),
            x_range=[-0.45, 0.45, 0.02],
            color=TEAL,
            stroke_width=2,
        ).move_to(ORIGIN)
        card2_ill = VGroup(card2_line)
        card2 = make_card(card2_ill, "firing rates")

        # spike timing card
        card3_dots = VGroup(*[
            Dot([-0.30 + 0.20 * i, -0.03, 0], radius=0.028, color=YELLOW,
                fill_opacity=1)
            for i in range(4)
        ])
        card3_ill = VGroup(card3_dots)
        card3 = make_card(card3_ill, "spike timing")

        # multiple neurons card
        card4_neurons = VGroup()
        for x in [-0.30, -0.10, 0.10, 0.30]:
            neuron = Circle(radius=0.04, fill_color=GREY_B, fill_opacity=1,
                            stroke_width=0).move_to([x, -0.04, 0])
            spike = Line([x, 0.03, 0], [x, 0.14, 0], color=YELLOW, stroke_width=1.5)
            card4_neurons.add(VGroup(neuron, spike))
        card4_ill = VGroup(card4_neurons)
        card4 = make_card(card4_ill, "multiple neurons")

        cards = [card1, card2, card3, card4]
        card_positions = [
            top_panel.get_center() + [dx, dy, 0]
            for dy in [0.28, -0.32]
            for dx in [-0.65, 0.65]
        ]
        for card, pos in zip(cards, card_positions):
            card.move_to(pos)

        self.play(FadeIn(card1), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.85))
        self.play(FadeIn(card2), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.93))
        self.play(FadeIn(card3), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.71))
        self.play(FadeIn(card4), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.67))

        cards_group = VGroup(*cards)
        self.play(Indicate(cards_group, scale_factor=1.10, color=YELLOW),
                  run_time=max(0.05, 0.32))

        # beat 9: LFP features
        self.wait(max(0.05, 1.08))
        self.play(bottom_panel.animate.set_stroke(PURPLE, width=3),
                  run_time=max(0.05, 0.54))

        lfp_card1_bg = RoundedRectangle(
            width=1.05, height=0.65, corner_radius=0.06,
            fill_color=GREY, fill_opacity=0.15,
            stroke_color=WHITE, stroke_width=1,
        ).move_to(bottom_panel.get_center() + LEFT * 0.55)
        lfp_card2_bg = RoundedRectangle(
            width=1.05, height=0.65, corner_radius=0.06,
            fill_color=GREY, fill_opacity=0.15,
            stroke_color=WHITE, stroke_width=1,
        ).move_to(bottom_panel.get_center() + RIGHT * 0.55)
        lfp_card1_label = Text("population activity", font_size=7, color=WHITE)
        lfp_card1_label.next_to(lfp_card1_bg, DOWN, buff=0.04)
        lfp_card2_label = Text("frequency-specific power", font_size=7, color=WHITE)
        lfp_card2_label.next_to(lfp_card2_bg, DOWN, buff=0.04)
        lfp_card1 = VGroup(lfp_card1_bg, lfp_card1_label)
        lfp_card2 = VGroup(lfp_card2_bg, lfp_card2_label)

        self.play(FadeIn(lfp_card1, lfp_card2), run_time=max(0.05, 0.30))
        self.wait(max(0.05, 0.80))

        lfp_card1_center = lfp_card1_bg.get_center()
        faint_traces = VGroup()
        for ph in np.linspace(0, 3.0, 8):
            faint_traces.add(
                FunctionGraph(
                    lambda x, ph=ph: 0.07 * np.sin(2.8 * x + ph),
                    x_range=[-0.42, 0.42, 0.03],
                    color=TEAL,
                    stroke_width=1,
                    stroke_opacity=0.35,
                ).move_to(lfp_card1_center)
            )
        bold_envelope = FunctionGraph(
            lambda x: 0.15 * np.sin(2.8 * x),
            x_range=[-0.42, 0.42, 0.03],
            color=TEAL,
            stroke_width=3,
        ).move_to(lfp_card1_center)
        first_lfp_content = VGroup(faint_traces, bold_envelope)
        self.play(FadeIn(first_lfp_content), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 1.48))

        divider = Line(UP * 0.28, DOWN * 0.28, color=WHITE, stroke_width=2)
        divider.move_to(bottom_panel.get_center())
        self.play(Create(divider), run_time=max(0.05, 0.70))

        lfp_card2_center = lfp_card2_bg.get_center()
        spectrum_curve = FunctionGraph(
            lambda x: 0.24 * np.exp(-((x - 0.08) / 0.12) ** 2),
            x_range=[-0.45, 0.45, 0.02],
            color=WHITE,
            stroke_width=2,
        ).move_to(lfp_card2_center)
        shaded_band = Rectangle(
            width=0.22, height=0.30,
            fill_color=PURPLE, fill_opacity=0.45, stroke_width=0,
        ).move_to(lfp_card2_center + RIGHT * 0.06 + UP * 0.05)
        second_lfp_content = VGroup(spectrum_curve, shaded_band)
        self.play(FadeIn(second_lfp_content), run_time=max(0.05, 0.86))
        self.play(Indicate(shaded_band, scale_factor=1.2, color=PURPLE),
                  run_time=max(0.05, 0.40))

        # beat 10 + beat 11 combined timeline from 49.22 to 55.45
        self.play(pipeline_arrows[2].animate.set_color(YELLOW).set_stroke(width=5)
                  .set_z_index(10), run_time=max(0.05, 0.96))

        dec_rect = block_rects[3]
        dec_label = block_labels[3]
        dec_center = dec_rect.get_center()
        expanded_dec = RoundedRectangle(
            width=2.6, height=2.6, corner_radius=0.18,
            fill_color=BLUE, fill_opacity=0.12,
            stroke_color=BLUE, stroke_width=3,
        ).move_to(dec_center)

        input_nodes = VGroup(
            Dot(dec_center + LEFT * 0.9 + UP * 0.35, radius=0.07, color=YELLOW),
            Dot(dec_center + LEFT * 0.9 + DOWN * 0.35, radius=0.07, color=YELLOW),
        )
        hidden_nodes = VGroup(
            Dot(dec_center + UP * 0.55, radius=0.07, color=ORANGE),
            Dot(dec_center + ORIGIN, radius=0.07, color=ORANGE),
            Dot(dec_center + DOWN * 0.55, radius=0.07, color=ORANGE),
        )
        output_nodes = VGroup(
            Dot(dec_center + RIGHT * 0.9 + UP * 0.35, radius=0.07, color=TEAL),
            Dot(dec_center + RIGHT * 0.9 + DOWN * 0.35, radius=0.07, color=TEAL),
        )
        connections = VGroup()
        for inp in input_nodes:
            for hid in hidden_nodes:
                connections.add(
                    Line(inp.get_center(), hid.get_center(),
                         color=GREY_B, stroke_width=1.2)
                )
        for hid in hidden_nodes:
            for out in output_nodes:
                connections.add(
                    Line(hid.get_center(), out.get_center(),
                         color=GREY_B, stroke_width=1.2)
                )
        weight_label = Text("weights", font_size=10, color=GREY_B)
        weight_label.next_to(connections[0], LEFT, buff=0.04)
        network_diagram = VGroup(
            connections, input_nodes, hidden_nodes, output_nodes, weight_label,
        )

        self.play(
            Transform(dec_rect, expanded_dec),
            dec_label.animate.move_to(dec_center + UP * 1.10).set_color(YELLOW),
            run_time=max(0.05, 0.40),
        )
        self.play(FadeIn(network_diagram), run_time=max(0.05, 0.30))

        # selected features flow into decoding block
        packet_start = np.array([feature_center[0] + 0.8, feature_center[1] + 0.3, 0])
        packet1 = Dot(packet_start, radius=0.045, color=TEAL, fill_opacity=1)
        packet2 = Dot(packet_start + DOWN * 0.35, radius=0.045, color=GREEN,
                      fill_opacity=1)
        self.add(packet1, packet2)
        self.play(
            packet1.animate.move_to(input_nodes[0].get_center()),
            packet2.animate.move_to(input_nodes[1].get_center()),
            run_time=max(0.05, 0.58),
        )
        self.remove(packet1, packet2)

        self.play(Indicate(input_nodes, scale_factor=1.25, color=YELLOW),
                  run_time=max(0.05, 0.34))
        self.play(
            LaggedStart(*[Indicate(n, scale_factor=1.25, color=ORANGE)
                           for n in hidden_nodes],
                        lag_ratio=0.35),
            run_time=max(0.05, 0.32),
        )
        self.play(Indicate(output_nodes, scale_factor=1.25, color=TEAL),
                  run_time=max(0.05, 0.64))

        pred_path = DashedLine(
            output_nodes.get_center() + RIGHT * 0.5,
            block_rects[4].get_left() + LEFT * 0.2,
            color=YELLOW,
            dash_length=0.08,
            stroke_width=3,
        )
        pred_path.add_tip(at_start=False)
        self.play(Create(pred_path), run_time=max(0.05, 0.70))

        # thought-bubble arm reappears and overlays trajectory
        thought_arm_overlay = arm_in_bubble.copy()
        thought_arm_overlay.move_to(pred_path.get_center() + UP * 0.25)
        self.play(
            Indicate(person_group, scale_factor=1.06, color=YELLOW),
            FadeIn(thought_arm_overlay),
            run_time=max(0.05, 0.48),
        )
        self.play(thought_arm_overlay.animate.move_to(pred_path.get_center()),
                  run_time=max(0.05, 0.18))

        moving_path_group = VGroup(pred_path, thought_arm_overlay)
        self.play(
            moving_path_group.animate.move_to(block_rects[4].get_center() + LEFT * 0.4),
            run_time=max(0.05, 0.60),
        )

        # robotic arm fades in far right, connected to device control
        robot_base = RoundedRectangle(
            width=0.75, height=0.28, corner_radius=0.08,
            fill_color=GREY_B, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to([5.85, -1.30, 0])
        robot_seg1 = Line(
            robot_base.get_top(),
            robot_base.get_top() + UP * 0.55 + RIGHT * 0.20,
            color=GREY_B,
            stroke_width=4,
        )
        robot_seg2 = Line(
            robot_seg1.get_end(),
            robot_seg1.get_end() + RIGHT * 0.55 + DOWN * 0.25,
            color=GREY_B,
            stroke_width=3,
        )
        robot_effector = Dot(robot_seg2.get_end(), radius=0.08, color=YELLOW,
                             fill_opacity=1)
        robotic_arm = VGroup(robot_base, robot_seg1, robot_seg2, robot_effector)
        robot_connect = Line(
            block_rects[4].get_right(),
            robot_base.get_left(),
            color=YELLOW,
            stroke_width=2,
        )

        self.play(FadeIn(robotic_arm, robot_connect), run_time=max(0.05, 0.28))

        # settle, checkmark, final pulse
        check_icon = SVGMobject(ASSET_PATHS["check_circle"])
        check_icon.set_color(GREEN).scale_to_fit_height(0.55)
        check_icon.next_to(block_rects[4], UP, buff=0.10)

        self.play(FadeIn(check_icon), robot_effector.animate.set_color(GREEN),
                  run_time=max(0.05, 0.15))
        self.play(
            LaggedStart(*[Indicate(a, color=YELLOW, scale_factor=1.08)
                           for a in pipeline_arrows],
                        lag_ratio=0.18),
            run_time=max(0.05, 0.25),
        )
        self.wait(max(0.05, 0.05))