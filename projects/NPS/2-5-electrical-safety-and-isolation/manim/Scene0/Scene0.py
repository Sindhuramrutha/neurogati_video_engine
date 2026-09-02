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


class Scene0(MovingCameraScene):
    def make_wave(self, color=YELLOW, width=1.2, height=0.3, stroke_width=5):
        wave = VMobject()
        wave.set_stroke(color=color, width=stroke_width, opacity=1)
        pts = []
        n = 50
        for i in range(n + 1):
            x = -width / 2 + width * i / n
            y = height * np.sin(4 * PI * (x + width / 2) / width)
            pts.append(np.array([x, y, 0]))
        wave.set_points_as_corners(pts)
        return wave

    def make_lightning(self, color=YELLOW, scale=1.0):
        bolt = Polygon(
            np.array([0.08, 0.22, 0]) * scale,
            np.array([-0.20, -0.06, 0]) * scale,
            np.array([0.00, -0.06, 0]) * scale,
            np.array([-0.08, -0.28, 0]) * scale,
            np.array([0.24, 0.08, 0]) * scale,
            np.array([0.04, 0.08, 0]) * scale,
            stroke_width=2,
            fill_color=color,
            fill_opacity=1,
            stroke_color=color,
        )
        return bolt

    def make_shield(self, color):
        shield = Polygon(
            np.array([-0.4, 0.35, 0]),
            np.array([0.4, 0.35, 0]),
            np.array([0.4, -0.15, 0]),
            np.array([0.25, -0.15, 0]),
            np.array([0, -0.65, 0]),
            np.array([-0.25, -0.15, 0]),
            np.array([-0.4, -0.15, 0]),
            stroke_width=3,
            fill_color=color,
            fill_opacity=1,
            stroke_color=WHITE,
        )
        return shield

    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- Human figure ----------
        head = Circle(
            radius=0.35,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=3,
        )
        head.move_to(np.array([0, 1.45, 0]))
        torso = Line(np.array([0, 1.05, 0]), np.array([0, -1.0, 0]), color=WHITE, stroke_width=6)
        left_arm = Line(np.array([0, 0.70, 0]), np.array([-0.8, 0.0, 0]), color=WHITE, stroke_width=5)
        right_arm = Line(np.array([0, 0.70, 0]), np.array([0.8, -0.1, 0]), color=WHITE, stroke_width=5)
        left_leg = Line(np.array([0, -1.0, 0]), np.array([-0.5, -2.2, 0]), color=WHITE, stroke_width=6)
        right_leg = Line(np.array([0, -1.0, 0]), np.array([0.5, -2.2, 0]), color=WHITE, stroke_width=6)
        human = VGroup(head, torso, left_arm, right_arm, left_leg, right_leg)
        human.move_to(np.array([-5.2, 0, 0]))

        head_conn = head.get_right() + np.array([0.05, 0, 0])
        arm_point = right_arm.get_center() + np.array([0.2, -0.15, 0])

        # ---------- Amplifier ----------
        amp_box = Rectangle(
            width=1.4,
            height=0.9,
            fill_color=PURPLE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        amp_text = Text("amp", font_size=26, color=WHITE)
        amp_text.move_to(amp_box.get_center())
        amp = VGroup(amp_box, amp_text)
        amp.move_to(np.array([-0.6, 1.5, 0]))

        # ---------- Computer ----------
        monitor_frame = Rectangle(
            width=1.8,
            height=1.2,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        screen = Rectangle(
            width=1.5,
            height=0.85,
            fill_color=TEAL,
            fill_opacity=0.35,
            stroke_color=WHITE,
            stroke_width=1,
        )
        screen.move_to(monitor_frame.get_center())
        monitor = VGroup(monitor_frame, screen)
        monitor.move_to(np.array([4.0, 1.55, 0]))
        tower = Rectangle(
            width=0.8,
            height=1.4,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2,
        )
        tower.move_to(np.array([4.0, 0.1, 0]))
        computer = VGroup(monitor, tower)

        comp_left = monitor_frame.get_left()
        amp_left = amp_box.get_left()
        amp_right = amp_box.get_right()

        # ---------- Cable ----------
        cable_left = Line(head_conn, amp_left, color=GREY, stroke_width=5)
        cable_right = Line(amp_right, comp_left, color=GREY, stroke_width=5)
        cable_group = VGroup(cable_left, cable_right)

        wave_path = Line(head_conn, comp_left, stroke_width=0, stroke_opacity=0)

        # ---------- Bit grid on computer screen ----------
        bit_grid = VGroup()
        for i in range(5):
            for j in range(3):
                dot = Dot(radius=0.05, color=GREEN, fill_opacity=1)
                dot.move_to(screen.get_center() + np.array([(i - 2) * 0.22, (j - 1) * 0.22, 0]))
                bit_grid.add(dot)
        bit_grid.set_opacity(0)
        self.add(bit_grid)

        # ---------- Electrodes / sensors ----------
        head_electrode = Dot(head_conn, radius=0.09, color=GOLD)
        arm_electrode = Dot(arm_point, radius=0.09, color=GOLD)
        wire_head = Line(head_conn + RIGHT * 0.05, head_conn + RIGHT * 0.22, color=PINK, stroke_width=2)
        wire_arm = Line(arm_point, np.array([-4.30, 1.52, 0]), color=PINK, stroke_width=2)
        electrodes = VGroup(head_electrode, arm_electrode, wire_head, wire_arm)

        # ---------- Cross-section illustration ----------
        cross_out = Ellipse(
            width=1.8,
            height=1.4,
            fill_color=MAROON,
            fill_opacity=0.45,
            stroke_color=WHITE,
            stroke_width=2,
        )
        cross_in = Ellipse(
            width=1.25,
            height=0.9,
            fill_color=PINK,
            fill_opacity=0.35,
            stroke_color=GREY,
            stroke_width=1,
        )
        needle = Line(np.array([0, 0.45, 0]), np.array([0, 0.08, 0]), color=YELLOW, stroke_width=3)
        tip = Dot(np.array([0, 0.08, 0]), radius=0.05, color=YELLOW)
        cross_out.move_to(ORIGIN)
        cross_in.move_to(ORIGIN)
        cross_section = VGroup(cross_out, cross_in, needle, tip)
        cross_section.move_to(torso.get_center())

        # ---------- Titles / labels ----------
        title_acq = Text("Neural Signal Acquisition", font_size=40, color=WHITE)
        title_acq.to_edge(UP, buff=0.7)

        # ---------- Beat 1 (0.00-1.10): draw acquisition chain ----------
        self.play(
            Write(human),
            Write(amp),
            Write(computer),
            Write(cable_group),
            run_time=max(0.05, 1.10),
        )
        self.wait(max(0.05, 0.30))

        # ---------- Beat 2 (1.40-2.36): title + brightened cable ----------
        self.play(
            FadeIn(title_acq),
            cable_group.animate.set_color(WHITE),
            run_time=max(0.05, 0.96),
        )
        self.wait(max(0.05, 0.56))

        # ---------- Beat 3 (2.92-4.00): waveform starts moving ----------
        wave = self.make_wave(color=YELLOW, width=1.2, height=0.30, stroke_width=5)
        wave.move_to(wave_path.point_from_proportion(0))
        self.add(wave)
        self.play(
            wave.animate.move_to(wave_path.point_from_proportion(0.40)),
            run_time=max(0.05, 1.08),
        )
        self.wait(max(0.05, 0.56))

        # ---------- Beat 4 (4.56-5.62): detecting label at head ----------
        origin_pulse = Dot(head_conn, radius=0.12, color=YELLOW)
        self.add(origin_pulse)
        detect_label = Text("detecting", font_size=24, color=YELLOW)
        detect_label.next_to(head_conn, UP, buff=0.35)
        self.play(
            wave.animate.move_to(wave_path.point_from_proportion(0.47)),
            origin_pulse.animate.scale(1.5),
            FadeIn(detect_label),
            run_time=max(0.05, 0.53),
        )
        self.play(
            origin_pulse.animate.scale(1 / 1.5),
            FadeOut(detect_label),
            run_time=max(0.05, 0.53),
        )
        self.wait(max(0.05, 0.36))

        # ---------- Beat 5 (5.98-6.84): amplifier pulse + larger amplitude ----------
        amp_label = Text("amplifying", font_size=24, color=YELLOW)
        amp_label.next_to(amp, UP, buff=0.25)
        self.play(
            wave.animate.move_to(wave_path.point_from_proportion(0.48)),
            amp.animate.scale(1.08),
            FadeIn(amp_label),
            run_time=max(0.05, 0.30),
        )
        self.play(
            amp.animate.scale(1 / 1.08),
            FadeOut(amp_label),
            wave.animate.scale(1.5),
            run_time=max(0.05, 0.56),
        )
        self.wait(max(0.05, 0.34))

        # ---------- Beat 6 (7.18-7.90): conditioning, cleaner waveform ----------
        cond_label = Text("conditioning", font_size=24, color=YELLOW)
        cond_label.move_to((amp_right + comp_left) / 2 + UP * 0.7)
        clean_wave = self.make_wave(color=TEAL, width=1.2, height=0.28, stroke_width=5)
        clean_wave.move_to(wave.get_center())
        self.play(
            Transform(wave, clean_wave),
            FadeIn(cond_label),
            run_time=max(0.05, 0.36),
        )
        self.play(
            wave.animate.move_to(wave_path.point_from_proportion(0.88)),
            run_time=max(0.05, 0.36),
        )
        self.wait(max(0.05, 0.24))

        # ---------- Beat 7 (8.14-9.78): arrival at computer, digital data flash ----------
        digital_label = Text("digital data", font_size=24, color=GREEN)
        digital_label.next_to(monitor_frame, UP, buff=0.30)
        self.play(
            wave.animate.move_to(comp_left),
            bit_grid.animate.set_opacity(1),
            FadeIn(digital_label),
            run_time=max(0.05, 0.94),
        )
        self.play(
            FadeOut(wave),
            bit_grid.animate.set_opacity(0.25),
            FadeOut(digital_label),
            run_time=max(0.05, 0.70),
        )
        self.wait(max(0.05, 0.92))

        # ---------- Beat 8 (10.70-15.04): dim chain, electrical safety warning ----------
        acquisition_chain = VGroup(human, amp, computer, cable_group)
        self.play(acquisition_chain.animate.set_opacity(0.55), run_time=max(0.05, 0.70))

        tri_w = 0.9
        warning_tri = Polygon(
            np.array([-tri_w * 0.45, -tri_w * 0.35, 0]),
            np.array([tri_w * 0.45, -tri_w * 0.35, 0]),
            np.array([0, tri_w * 0.5, 0]),
            stroke_width=3,
            stroke_color=GREY,
            fill_color=YELLOW,
            fill_opacity=1,
        )
        warning_bolt = self.make_lightning(color=GREY, scale=0.5)
        warning_bolt.move_to(warning_tri.get_center())
        warning_icon = VGroup(warning_tri, warning_bolt)
        warning_label = Text("Electrical Safety", font_size=24, color=YELLOW)
        warning_label.next_to(warning_icon, RIGHT, buff=0.25)
        warning_group = VGroup(warning_icon, warning_label)
        warning_group.move_to(head_conn + UP * 1.4 + RIGHT * 0.7)

        self.play(GrowFromCenter(warning_icon), FadeIn(warning_label), run_time=max(0.05, 1.30))
        self.play(warning_icon.animate.scale(1.2), rate_func=there_and_back, run_time=max(0.05, 1.20))
        self.wait(max(0.05, 1.14))

        # Gap from beat 8 (15.04) to beat 9 (15.96)
        self.wait(max(0.05, 0.92))

        # ---------- Beat 9 (15.96-20.40): warning moves up, electrodes appear ----------
        self.play(
            warning_group.animate.scale(0.7).move_to(np.array([-5.3, 3.1, 0])),
            human.animate.set_opacity(1.0),
            FadeIn(electrodes),
            run_time=max(0.05, 2.44),
        )
        self.play(
            head_electrode.animate.scale(1.3),
            arm_electrode.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 1.20))

        # Gap from beat 9 (20.40) to beat 10 (20.98)
        self.wait(max(0.05, 0.58))

        # ---------- Beat 10 (20.98-22.22): zoom to skin electrode ----------
        skin_label = Text("on the skin", font_size=24, color=YELLOW)
        skin_label.next_to(arm_electrode, UP, buff=0.4)
        self.play(
            self.camera.frame.animate.scale(0.55).move_to(arm_electrode.get_center()),
            run_time=max(0.05, 0.50),
        )
        self.play(
            FadeIn(skin_label),
            arm_electrode.animate.scale(1.6).set_color(WHITE),
            rate_func=there_and_back,
            run_time=max(0.05, 0.44),
        )
        self.wait(max(0.05, 0.30))

        # Gap from beat 10 (22.22) to beat 11 (23.14)
        self.wait(max(0.05, 0.92))

        # ---------- Beat 11 (23.14-25.80): inside-the-body illustration ----------
        inside_label = Text("inside the body", font_size=24, color=WHITE)
        inside_label.next_to(cross_section, UP, buff=0.20)
        surgery_tag = Text("surgery", font_size=24, color=ORANGE)
        surgery_tag.next_to(cross_section, RIGHT, buff=0.20)

        self.play(
            self.camera.frame.animate.move_to(cross_section.get_center()),
            FadeIn(cross_section),
            run_time=max(0.05, 0.60),
        )
        self.play(FadeIn(inside_label), run_time=max(0.05, 0.50))
        self.play(FadeIn(surgery_tag), run_time=max(0.05, 0.36))
        self.play(FadeOut(surgery_tag), run_time=max(0.05, 0.36))
        self.wait(max(0.05, 0.84))

        # Gap from beat 11 (25.80) to beat 12 (26.76)
        self.wait(max(0.05, 0.96))

        # ---------- Beat 12 (26.76-30.34): return to full chain, direct connection ----------
        self.play(
            FadeOut(skin_label),
            FadeOut(inside_label),
            FadeOut(cross_section),
            run_time=max(0.05, 0.55),
        )
        self.play(
            self.camera.frame.animate.scale(1 / 0.55).move_to(ORIGIN),
            run_time=max(0.05, 1.20),
        )
        self.play(
            cable_group.animate.set_color(WHITE).set_opacity(1.0),
            amp.animate.set_opacity(1.0),
            computer.animate.set_opacity(1.0),
            run_time=max(0.05, 0.55),
        )
        direct_line = DashedLine(head_conn, comp_left, color=YELLOW, dash_length=0.18, stroke_width=3)
        direct_label = Text("directly connected", font_size=26, color=YELLOW)
        direct_label.next_to(direct_line, UP, buff=0.5)
        self.play(Write(direct_line), FadeIn(direct_label), run_time=max(0.05, 0.78))
        self.wait(max(0.05, 0.50))

        # Gap from beat 12 (30.34) to beat 13 (30.96)
        self.wait(max(0.05, 0.62))

        # ---------- Beat 13 (30.96-35.94): shields + blocked hazard ----------
        shield_human = self.make_shield(GREEN)
        shield_human.move_to(np.array([-5.2, 0.6, 0]))
        shield_comp = self.make_shield(BLUE)
        shield_comp.move_to(np.array([4.0, 0.9, 0]))
        protected_human = Text("protected", font_size=20, color=GREEN)
        protected_human.next_to(shield_human, DOWN, buff=0.25)
        protected_comp = Text("protected", font_size=20, color=BLUE)
        protected_comp.next_to(shield_comp, DOWN, buff=0.25)

        hazard_bolt = self.make_lightning(color=ORANGE, scale=1.25)
        hazard_bolt.move_to(np.array([-2.75, 1.52, 0]))
        hazard_cross_1 = Line(
            hazard_bolt.get_left() + UP * 0.15,
            hazard_bolt.get_right() + DOWN * 0.15,
            color=RED,
            stroke_width=8,
        )
        hazard_cross_2 = Line(
            hazard_bolt.get_left() + DOWN * 0.15,
            hazard_bolt.get_right() + UP * 0.15,
            color=RED,
            stroke_width=8,
        )
        hazard_cross = VGroup(hazard_cross_1, hazard_cross_2)
        hazard_group = VGroup(hazard_bolt, hazard_cross)

        self.play(FadeOut(direct_line), FadeOut(direct_label), run_time=max(0.05, 0.40))
        self.play(GrowFromCenter(shield_human), GrowFromCenter(shield_comp), run_time=max(0.05, 0.60))
        self.play(FadeIn(protected_human), FadeIn(protected_comp), run_time=max(0.05, 0.50))
        self.play(FadeIn(hazard_bolt), run_time=max(0.05, 0.55))
        self.play(Create(hazard_cross), run_time=max(0.05, 0.55))
        self.play(
            shield_human.animate.scale(1.1),
            shield_comp.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=max(0.05, 0.55),
        )
        self.wait(max(0.05, 1.83))

        # Gap from beat 13 (35.94) to beat 14 (37.02)
        self.wait(max(0.05, 1.08))

        # ---------- Beat 14 (37.02-40.20): focus shifts to electrical safety ----------
        main_title = Text("Why electrical safety matters", font_size=38, color=YELLOW)
        main_title.move_to(title_acq.get_center())
        main_title.scale_to_fit_width(12)

        self.play(FadeOut(hazard_group), run_time=max(0.05, 0.40))
        self.play(warning_icon.animate.scale(1.15), rate_func=there_and_back, run_time=max(0.05, 0.60))
        self.play(FadeOut(title_acq), FadeIn(main_title), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 1.38))

        # Gap from beat 14 (40.20) to beat 15 (40.86)
        self.wait(max(0.05, 0.66))

        # ---------- Beat 15 (40.86-46.12): electrical isolation gap + signal crossing ----------
        iso_label = Text("Electrical Isolation", font_size=30, color=BLUE)
        iso_label.next_to(main_title, DOWN, buff=0.45)

        gap_left_x = -3.5
        gap_right_x = -2.9
        gap_cable_1 = Line(head_conn, np.array([gap_left_x, 1.48, 0]), color=WHITE, stroke_width=5)
        gap_cable_2 = Line(np.array([gap_right_x, 1.50, 0]), amp_left, color=WHITE, stroke_width=5)
        barrier_line_1 = Line(
            np.array([gap_left_x, 1.24, 0]),
            np.array([gap_left_x, 1.72, 0]),
            color=YELLOW,
            stroke_width=6,
        )
        barrier_line_2 = Line(
            np.array([gap_right_x, 1.24, 0]),
            np.array([gap_right_x, 1.72, 0]),
            color=YELLOW,
            stroke_width=6,
        )
        isolation_barrier = VGroup(barrier_line_1, barrier_line_2)

        self.play(
            FadeOut(cable_left),
            FadeIn(gap_cable_1),
            FadeIn(gap_cable_2),
            FadeIn(isolation_barrier),
            run_time=max(0.05, 0.80),
        )
        self.play(
            shield_human.animate.shift(LEFT * 0.3),
            shield_comp.animate.shift(RIGHT * 0.3),
            FadeIn(iso_label),
            run_time=max(0.05, 0.70),
        )

        sig_progress = ValueTracker(0)
        wave2 = self.make_wave(color=GREEN, width=1.2, height=0.28, stroke_width=5)
        wave2.move_to(wave_path.point_from_proportion(0))
        wave2.add_updater(lambda m: m.move_to(wave_path.point_from_proportion(sig_progress.get_value())))
        self.add(wave2)
        self.play(sig_progress.animate.set_value(1), run_time=max(0.05, 3.76))

        # ---------- Beat 16 (46.12-46.92): final held frame, gently pulsing gap ----------
        self.play(isolation_barrier.animate.set_opacity(0.70), rate_func=there_and_back, run_time=max(0.05, 0.80))