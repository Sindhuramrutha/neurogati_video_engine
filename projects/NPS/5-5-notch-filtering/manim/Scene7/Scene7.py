ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- helpers ----------
        def make_signal_trace(width=4.0, height=1.2, noise_level=0.15, n_points=120, seed=42):
            np.random.seed(seed)
            x_vals = np.linspace(-width / 2, width / 2, n_points)
            base = 0.3 * np.sin(2 * np.pi * 0.8 * x_vals) + 0.15 * np.sin(2 * np.pi * 2.1 * x_vals + 1.2)
            noise = noise_level * np.random.randn(n_points)
            y_vals = base + noise
            y_vals = y_vals / np.max(np.abs(y_vals)) * (height / 2)
            points = [np.array([x, y, 0]) for x, y in zip(x_vals, y_vals)]
            trace = VMobject(fill_color=None, stroke_color=WHITE, stroke_width=2)
            trace.set_points_smoothly(points)
            return trace

        def make_monitor(width=4.8, height=3.2, label_text=""):
            outer = Rectangle(width=width, height=height, stroke_color=GREY, stroke_width=3,
                              fill_color="#1A1C23", fill_opacity=1)
            screen = Rectangle(width=width * 0.85, height=height * 0.75,
                               fill_color="#0A0C12", fill_opacity=1, stroke_color=GREY, stroke_width=1)
            screen.move_to(outer.get_center() + UP * (height * 0.08))
            stand = Line(outer.get_bottom(), outer.get_bottom() + DOWN * (height * 0.25),
                         stroke_color=GREY, stroke_width=4)
            base = Line(stand.get_end() + LEFT * (width * 0.3),
                        stand.get_end() + RIGHT * (width * 0.3),
                        stroke_color=GREY, stroke_width=5)
            label = Text(label_text, font_size=22, color=GREY)
            label.next_to(outer, DOWN, buff=0.15)
            return VGroup(outer, screen, stand, base, label)

        def make_notch_icon(size=1.0, color=RED, opacity=1.0, stroke_w=3):
            circle = Circle(radius=size * 0.5, stroke_color=color, stroke_width=stroke_w,
                            fill_color=color, fill_opacity=0.15)
            nf_text = Text("NF", font_size=size * 20, color=color, weight="BOLD")
            nf_text.scale_to_fit_width(size * 0.5)
            nf_text.move_to(circle.get_center())
            sine_path = VMobject(stroke_color=color, stroke_width=stroke_w)
            n_pts = 30
            pts = [np.array([-size*0.3 + t*size*0.6, size*0.15*np.sin(t*4*np.pi), 0])
                   for t in [i/(n_pts-1) for i in range(n_pts)]]
            sine_path.set_points_smoothly(pts)
            sine_path.next_to(circle, DOWN, buff=size * 0.15)
            slash = Line(circle.get_corner(DL) + DL*size*0.05,
                         circle.get_corner(UR) + UR*size*0.05,
                         stroke_color=color, stroke_width=stroke_w * 0.8)
            result = VGroup(circle, nf_text, sine_path, slash)
            result.set_opacity(opacity)
            return result

        # ---------- left pane ----------
        left_bg = Rectangle(width=6.5, height=7.2, fill_color="#1C1E26", fill_opacity=1,
                            stroke_color=GREY, stroke_width=1.5)
        left_header = Text("❌ Poor Recording Setup", font_size=30, color=RED, weight="BOLD")
        left_header.next_to(left_bg, UP, buff=0.15)

        # electrode dangling
        electrode_body = Rectangle(width=0.35, height=1.4, fill_color=GREY, fill_opacity=1,
                                   stroke_color=WHITE, stroke_width=1)
        electrode_disk = Circle(radius=0.22, fill_color=GREY_B, fill_opacity=1,
                                stroke_color=WHITE, stroke_width=1)
        electrode_disk.next_to(electrode_body, DOWN, buff=0)
        electrode_wire = Line(electrode_body.get_top(), electrode_body.get_top() + UP * 1.5,
                              stroke_color=GREY, stroke_width=2)
        dangling = VGroup(electrode_body, electrode_disk, electrode_wire)
        dangling.move_to(left_bg.get_center() + LEFT * 1.3 + UP * 1.0)

        # disconnected ground
        ground_clip = Polygon(np.array([-0.15, 0, 0]), np.array([0.15, 0, 0]),
                              np.array([0.1, -0.35, 0]), np.array([-0.1, -0.35, 0]),
                              fill_color=GREY, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
        ground_wire = Line(ground_clip.get_top(), ground_clip.get_top() + UP * 1.2,
                           stroke_color=GREY, stroke_width=2)
        ground_label = Text("GND", font_size=18, color=GREY_B)
        ground_label.next_to(ground_wire, LEFT, buff=0.1)
        disc_ground = VGroup(ground_clip, ground_wire, ground_label)
        disc_ground.move_to(left_bg.get_center() + RIGHT * 1.6 + UP * 1.6)

        # warning icon (static)
        warning = Text("⚠", font_size=48, color=RED, weight="BOLD")
        warning.next_to(dangling, RIGHT, buff=0.3)

        # left monitor with noisy signal
        left_mon = make_monitor(width=4.8, height=3.2, label_text="Recording Signal")
        left_mon.move_to(left_bg.get_center() + DOWN * 1.4)
        left_trace = make_signal_trace(width=3.8, height=1.0, noise_level=0.4, seed=123)
        left_trace.move_to(left_mon[1].get_center())
        left_mon.add(left_trace)

        # large red notch filter on left monitor
        left_notch = make_notch_icon(size=1.2, color=RED, opacity=1.0, stroke_w=4)
        left_notch.move_to(left_mon[1].get_center())

        # red X stamp (using asset)
        left_xstamp = SVGMobject(ASSET_PATHS["x_circle"])
        left_xstamp.set_color(RED).set_opacity(0.7).scale_to_fit_height(4.5)
        left_xstamp.move_to(left_bg.get_center())

        left_content = VGroup(dangling, disc_ground, warning, left_mon, left_notch)
        all_left = VGroup(left_bg, left_header, left_content)

        # ---------- right pane ----------
        right_bg = Rectangle(width=6.5, height=7.2, fill_color="#1C1E26", fill_opacity=1,
                             stroke_color=GREY, stroke_width=1.5)
        right_header = Text("✅ Well-Prepared Setup", font_size=30, color=GREEN, weight="BOLD")
        right_header.next_to(right_bg, UP, buff=0.15)

        skin_patch = Rectangle(width=1.0, height=0.4, fill_color="#D4A574", fill_opacity=1,
                               stroke_color=WHITE, stroke_width=1)
        skin_patch.move_to(right_bg.get_center() + LEFT * 1.0 + UP * 1.8)

        r_electrode_body = Rectangle(width=0.35, height=1.0, fill_color=GREY, fill_opacity=1,
                                     stroke_color=WHITE, stroke_width=1)
        r_electrode_disk = Circle(radius=0.22, fill_color=GREY_B, fill_opacity=1,
                                  stroke_color=WHITE, stroke_width=1)
        r_electrode_disk.move_to(r_electrode_body.get_bottom() + DOWN * 0.05)
        r_electrode_wire = Line(r_electrode_body.get_top(), r_electrode_body.get_top() + UP * 0.8,
                                stroke_color=GREY, stroke_width=2)
        right_electrode = VGroup(r_electrode_body, r_electrode_disk, r_electrode_wire)
        right_electrode.move_to(skin_patch.get_top() + UP * r_electrode_body.height / 2)

        cable_sheath = Rectangle(width=2.5, height=0.2, fill_color="#555555", fill_opacity=1,
                                 stroke_color=WHITE, stroke_width=1)
        cable_sheath.next_to(r_electrode_wire.get_top(), RIGHT, buff=0).shift(UP * 0.8)
        shield_label = Text("Shielded Cable", font_size=16, color=BLUE)
        shield_label.next_to(cable_sheath, UP, buff=0.1)

        gnd_line = Line(cable_sheath.get_left() + DOWN * 0.15,
                        cable_sheath.get_left() + DOWN * 0.8,
                        stroke_color=GREEN, stroke_width=3)
        gnd_dot = Dot(gnd_line.get_end(), radius=0.1, color=GREEN, fill_opacity=1)

        right_mon = make_monitor(width=4.8, height=3.2, label_text="Recording Signal")
        right_mon.move_to(right_bg.get_center() + DOWN * 1.4)
        right_trace = make_signal_trace(width=3.8, height=1.0, noise_level=0.07, seed=456)
        right_trace.move_to(right_mon[1].get_center())
        right_mon.add(right_trace)

        right_notch_faint = make_notch_icon(size=0.55, color="#4477AA", opacity=0.3, stroke_w=2)
        right_notch_faint.move_to(right_mon[1].get_center() + RIGHT * 1.3 + DOWN * 0.8)

        right_content = VGroup(skin_patch, right_electrode, cable_sheath, shield_label,
                               gnd_line, gnd_dot, right_mon, right_notch_faint)
        all_right = VGroup(right_bg, right_header, right_content)

        # ---------- scale and position ----------
        split = VGroup(all_left, all_right)
        split.arrange(RIGHT, buff=0.8).move_to(ORIGIN)
        split.scale_to_fit_height(7.0)
        split.shift(UP * 0.3)  # room for bottom text

        # ---------- beat 1: fade in (0.00-2.62) ----------
        self.play(FadeIn(split, shift=UP * 0.3), run_time=max(0.05, 2.62))

        # ---------- beat 2: red X stamp at 2.62 ----------
        self.play(Write(left_xstamp), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 7.48))  # until 10.60

        # ---------- beat 3: good electrode contact (10.60-12.34) ----------
        pulse_box = SurroundingRectangle(VGroup(skin_patch, r_electrode_disk),
                                         color=GREEN, buff=0.15, stroke_width=3)
        check1 = SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN)
        check1.scale_to_fit_height(0.6)
        lbl1 = Text("Good Contact", font_size=22, color=GREEN)
        lbl1.next_to(check1, RIGHT, buff=0.15)
        check1_group = VGroup(check1, lbl1)
        check1_group.next_to(pulse_box, RIGHT, buff=0.4)

        self.play(Flash(pulse_box, color=GREEN, flash_radius=0.4, line_length=0.6, line_stroke_width=8),
                  run_time=max(0.05, 0.8))
        self.play(GrowFromCenter(check1_group), run_time=max(0.05, 0.94))
        pulse_box.set_stroke(opacity=0.4, width=2)
        self.add(pulse_box)

        # ---------- beat 4: proper grounding (12.34-13.58) ----------
        cable_box = SurroundingRectangle(VGroup(cable_sheath, gnd_line, gnd_dot),
                                         color=BLUE, buff=0.15, stroke_width=3)
        check2 = SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN)
        check2.scale_to_fit_height(0.6)
        lbl2 = Text("Proper Grounding", font_size=22, color=GREEN)
        lbl2.next_to(check2, RIGHT, buff=0.15)
        check2_group = VGroup(check2, lbl2)
        check2_group.next_to(cable_box, LEFT, buff=0.4)

        self.play(Flash(cable_box, color=BLUE, flash_radius=0.4, line_length=0.6, line_stroke_width=8),
                  run_time=max(0.05, 0.74))
        self.play(GrowFromCenter(check2_group), run_time=max(0.05, 0.5))
        cable_box.set_stroke(opacity=0.4, width=2)
        self.add(cable_box)

        # ---------- beat 5: appropriate shielding (13.58-14.98) ----------
        shield_box = SurroundingRectangle(cable_sheath, color=PURPLE, buff=0.12, stroke_width=3)
        check3 = SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN)
        check3.scale_to_fit_height(0.6)
        lbl3 = Text("Appropriate Shielding", font_size=22, color=GREEN)
        lbl3.next_to(check3, RIGHT, buff=0.15)
        check3_group = VGroup(check3, lbl3)
        check3_group.next_to(shield_box, LEFT, buff=0.2)

        self.play(Flash(shield_box, color=PURPLE, flash_radius=0.4, line_length=0.6, line_stroke_width=8),
                  run_time=max(0.05, 0.8))
        self.play(GrowFromCenter(check3_group), run_time=max(0.05, 0.6))
        shield_box.set_stroke(opacity=0.4, width=2)
        self.add(shield_box)

        # ---------- beat 6: correct equipment setup (14.98-16.98) ----------
        setup_glow = SurroundingRectangle(right_bg, color=GREEN, buff=0.05,
                                          stroke_width=5, stroke_opacity=0.4)
        check4 = SVGMobject(ASSET_PATHS["check_circle"]).set_color(GREEN)
        check4.scale_to_fit_height(0.6)
        lbl4 = Text("Correct Setup", font_size=22, color=GREEN)
        lbl4.next_to(check4, RIGHT, buff=0.15)
        check4_group = VGroup(check4, lbl4)
        check4_group.next_to(right_bg, DOWN, buff=0.4)

        self.play(GrowFromCenter(setup_glow),
                  GrowFromCenter(check4_group),
                  run_time=max(0.05, 2.0))

        # ---------- beat 7: residual filtering (16.98-19.10) ----------
        # left notch pulse
        self.play(left_notch.animate.set_color("#FF3333").scale(1.15), run_time=max(0.05, 0.5))
        self.play(left_notch.animate.set_color(RED).scale(1 / 1.15), run_time=max(0.05, 0.5))

        right_notch_bright = make_notch_icon(size=0.8, color=BLUE, opacity=1.0, stroke_w=3)
        right_notch_bright.move_to(right_notch_faint.get_center())
        right_notch_label = Text("Residual Filtering", font_size=18, color=BLUE, weight="BOLD")
        right_notch_label.next_to(right_notch_bright, DOWN, buff=0.2)

        self.play(FadeOut(right_notch_faint),
                  FadeIn(right_notch_bright),
                  FadeIn(right_notch_label),
                  run_time=max(0.05, 1.12))

        # ---------- beat 8: bottom text (19.10-23.00) ----------
        bottom_text = Text(
            "Filter residual interference, not poor practices.",
            font_size=32, color=WHITE, weight="BOLD",
            stroke_color="#0F1116", stroke_width=3,
        )
        bottom_text.to_edge(DOWN, buff=0.4)
        self.play(Write(bottom_text), run_time=max(0.05, 1.5))
        self.wait(max(0.05, 2.4))

        # ---------- beat 9: hold until 23.88 ----------
        self.wait(max(0.05, 0.88))