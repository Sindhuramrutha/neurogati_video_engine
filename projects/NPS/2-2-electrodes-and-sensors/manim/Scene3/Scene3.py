ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene3(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ------------------------------------------------------------
        # Beat 1: 0.00–3.24  skin cross-section
        # ------------------------------------------------------------
        self.skin_cross = self.build_skin_cross()
        self.label_skin = Text("skin surface", font_size=22, color=WHITE)
        self.label_skin.next_to(self.skin_cross, RIGHT, buff=0.3, aligned_edge=UP)
        self.play(FadeIn(self.skin_cross), FadeIn(self.label_skin), run_time=max(0.05, 1.2))
        self.wait(max(0.05, 3.24 - 1.2))

        # ------------------------------------------------------------
        # Beat 2: 3.24–5.32  electrode descends
        # ------------------------------------------------------------
        skin_top_y = self.skin_cross.get_top()[1]
        disc_height = 0.35
        final_center_y = skin_top_y - disc_height / 2.0
        self.electrode, self.disc, self.wire = self.build_electrode()
        start_y = final_center_y + 3.0
        self.electrode.move_to(np.array([0, start_y, 0]))
        self.play(
            self.electrode.animate.move_to(np.array([0, final_center_y, 0])),
            run_time=max(0.05, 1.2
        ))
        # Contact highlight
        contact_line_half_width = 0.8
        self.contact_line = Line(
            start=np.array([-contact_line_half_width, skin_top_y, 0]),
            end=np.array([contact_line_half_width, skin_top_y, 0]),
            color=WHITE,
            stroke_width=3,
            stroke_opacity=0.9
        )
        self.play(FadeIn(self.contact_line), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 5.32 - (3.24 + 1.2 + 0.5)))  # 0.38

        # ------------------------------------------------------------
        # Beat 3: 5.32–10.70  non-invasive labels
        # ------------------------------------------------------------
        self.red_x = self.build_red_x()
        self.red_x.move_to(np.array([0, -0.7, 0]))
        self.label_no_surgery = Text(
            "no surgery / no needle insertion",
            font_size=22,
            color=RED,
            weight="BOLD"
        )
        self.label_no_surgery.next_to(self.red_x, RIGHT, buff=0.4)
        self.label_non_invasive = Text("non-invasive", font_size=20, color=GOLD, weight="BOLD")
        self.label_non_invasive.next_to(self.electrode, UP, buff=0.3).shift(RIGHT * 0.4)

        self.play(
            FadeIn(self.red_x),
            FadeIn(self.label_no_surgery),
            run_time=max(0.05, 0.8
        ))
        self.play(FadeIn(self.label_non_invasive), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 1.2))
        self.play(
            FadeOut(self.red_x),
            FadeOut(self.label_no_surgery),
            FadeOut(self.label_non_invasive),
            run_time=max(0.05, 0.8
        ))
        self.wait(max(0.05, 10.70 - 5.32 - (0.8 + 0.8 + 1.2 + 0.8)))  # 1.78

        # ------------------------------------------------------------
        # Gap 10.70–11.26
        # ------------------------------------------------------------
        self.wait(max(0.05, 11.26 - 10.70))

        # ------------------------------------------------------------
        # Beat 4: 11.26–16.18  scale/move cross-section, show list
        # ------------------------------------------------------------
        # Group skin, electrode, contact line for scaling/moving
        self.assembly = VGroup(self.skin_cross, self.electrode, self.contact_line)
        self.play(
            self.assembly.animate.scale(0.8).move_to(np.array([0, 1.1, 0])),
            run_time=max(0.05, 0.8
        ))

        # List items
        list_items = [
            ("EEG — cortical recording", BLUE),
            ("sEMG — muscle recording", ORANGE),
            ("ECG — cardiac recording", GREEN)
        ]
        self.list_group = VGroup()
        for text, color in list_items:
            accent = Rectangle(
                width=0.08,
                height=0.25,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            )
            label = Text(text, font_size=24, weight="BOLD", color=WHITE)
            item = VGroup(accent, label).arrange(RIGHT, buff=0.2)
            self.list_group.add(item)
        self.list_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        self.list_group.next_to(self.assembly, DOWN, buff=0.5)

        # Sequential fade-ins with exact per-item duration
        per_item_duration = (16.18 - 11.26 - 0.8) / 3.0  # 1.3733333
        for item in self.list_group:
            self.play(FadeIn(item), run_time=max(0.05, 1.0))
            self.wait(max(0.05, per_item_duration - 1.0))

        # ------------------------------------------------------------
        # Gap 16.18–16.92
        # ------------------------------------------------------------
        self.wait(max(0.05, 16.92 - 16.18))

        # ------------------------------------------------------------
        # Beat 5: 16.92–21.28  pulses per application
        # ------------------------------------------------------------
        pulse_per_item = (21.28 - 16.92) / 3.0  # 1.4533333

        # EEG: blue pulse on wire
        self.play(
            Indicate(self.wire, color=BLUE, scale_factor=1.2),
            run_time=max(0.05, 1.0
        ))
        self.wait(max(0.05, pulse_per_item - 1.0))

        # sEMG: amber accent on disc
        self.play(
            Indicate(self.disc, color=ORANGE, scale_factor=1.15),
            run_time=max(0.05, 1.0
        ))
        self.wait(max(0.05, pulse_per_item - 1.0))

        # ECG: green pulse travels up wire
        ecg_dot = Dot(radius=0.06, color=GREEN, fill_opacity=1)
        ecg_dot.move_to(self.disc.get_top())
        self.play(
            ecg_dot.animate.move_to(self.wire.get_end()),
            run_time=max(0.05, 0.8
        ))
        self.play(FadeOut(ecg_dot), run_time=max(0.05, 0.2))
        self.wait(max(0.05, pulse_per_item - 1.0))

        # ------------------------------------------------------------
        # Beat 6: 21.28–25.44  safe/inexpensive/easy line + checkmarks
        # ------------------------------------------------------------
        self.play(FadeOut(self.list_group), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 0.1))

        word_safe = Text("safe", font_size=26, color=WHITE)
        dash1 = Text("—", font_size=26, color=GREY)
        word_inexpensive = Text("inexpensive", font_size=26, color=WHITE)
        dash2 = Text("—", font_size=26, color=GREY)
        word_easy = Text("easy to apply", font_size=26, color=WHITE)
        self.descriptor_group = VGroup(word_safe, dash1, word_inexpensive, dash2, word_easy)
        self.descriptor_group.arrange(RIGHT, buff=0.2)
        self.descriptor_group.next_to(self.assembly, DOWN, buff=0.7)
        self.play(FadeIn(self.descriptor_group), run_time=max(0.05, 0.6))

        # Checkmarks next to each descriptor
        self.checkmarks = VGroup()
        for word in [word_safe, word_inexpensive, word_easy]:
            check = Text("✓", font_size=28, color=GREEN)
            check.next_to(word, LEFT, buff=0.1)
            self.checkmarks.add(check)

        check_duration = (25.44 - 21.28 - 0.6 - 0.1 - 0.6) / 3.0  # 1.4
        for check in self.checkmarks:
            self.play(FadeIn(check), run_time=max(0.05, 0.9))
            self.wait(max(0.05, check_duration - 0.9))

        # ------------------------------------------------------------
        # Gap 25.44–26.22
        # ------------------------------------------------------------
        self.wait(max(0.05, 26.22 - 25.44))

        # ------------------------------------------------------------
        # Beat 7: 26.22–31.88  electrode lifts, gel appears
        # ------------------------------------------------------------
        lift_amount = 0.45
        self.play(self.electrode.animate.shift(UP * lift_amount), run_time=max(0.05, 0.8))

        # Gel between disc and skin
        skin_top_after = self.skin_cross.get_top()[1]
        disc_bottom_after = self.disc.get_bottom()[1]
        gel_height = disc_bottom_after - skin_top_after
        self.gel = Rectangle(
            width=1.3,
            height=gel_height,
            fill_color=BLUE,
            fill_opacity=0.35,
            stroke_color=BLUE,
            stroke_width=2
        )
        self.gel.move_to(np.array([0, (skin_top_after + disc_bottom_after) / 2.0, 0]))
        self.play(FadeIn(self.gel), run_time=max(0.05, 0.6))

        # Glisten / moist highlight on skin top under gel
        glisten_line = Line(
            start=self.gel.get_bottom() + LEFT * 0.5,
            end=self.gel.get_bottom() + RIGHT * 0.5,
            color=WHITE,
            stroke_width=2,
            stroke_opacity=0.7
        )
        self.play(FadeIn(glisten_line), run_time=max(0.05, 0.4))

        # Label conductive gel with arrow
        self.label_gel = Text("conductive gel", font_size=22, color=BLUE)
        self.label_gel.next_to(self.gel, RIGHT, buff=0.3)
        arrow_gel = Arrow(
            start=self.label_gel.get_left(),
            end=self.gel.get_right(),
            color=BLUE,
            stroke_width=3,
            buff=0.1
        )
        self.play(FadeIn(self.label_gel), FadeIn(arrow_gel), run_time=max(0.05, 0.6))

        # Label surface electrode near top of disc
        self.label_surface = Text("surface electrode", font_size=22, color=WHITE)
        self.label_surface.next_to(self.disc, UP, buff=0.2).shift(RIGHT * 0.5)
        self.play(FadeIn(self.label_surface), run_time=max(0.05, 0.5))

        remaining_beat7 = 31.88 - 26.22 - (0.8 + 0.6 + 0.4 + 0.6 + 0.5)
        self.wait(max(0.05, remaining_beat7))

        # ------------------------------------------------------------
        # Gap 31.88–32.72
        # ------------------------------------------------------------
        self.wait(max(0.05, 32.72 - 31.88))

        # ------------------------------------------------------------
        # Beat 8: 32.72–38.46  arrows / reduced contact resistance
        # ------------------------------------------------------------
        arrows_group = VGroup()
        dashed_lines = VGroup()
        for x_offset in [-0.45, 0.0, 0.45]:
            start = np.array([self.gel.get_center()[0] + x_offset, self.gel.get_bottom()[1], 0])
            end = np.array([self.gel.get_center()[0] + x_offset, self.gel.get_top()[1], 0])
            arrow = Arrow(start, end, color=BLUE, stroke_width=3, buff=0)
            dashed = DashedLine(start, end, color=BLUE, stroke_width=2, dash_length=0.08)
            arrows_group.add(arrow)
            dashed_lines.add(dashed)
        self.play(
            Create(arrows_group),
            FadeIn(dashed_lines),
            run_time=max(0.05, 0.8
        ))

        self.label_reduced = Text("reduced contact resistance", font_size=22, color=WHITE)
        self.label_reduced.next_to(arrows_group, DOWN, buff=0.4)
        self.play(FadeIn(self.label_reduced), run_time=max(0.05, 0.5))

        # Brighten gel-skin interface and gel-disc outline
        bright_line = Line(
            start=self.gel.get_bottom() + LEFT * 0.5,
            end=self.gel.get_bottom() + RIGHT * 0.5,
            color=WHITE,
            stroke_width=3,
            stroke_opacity=1.0
        )
        outline = SurroundingRectangle(
            self.gel,
            color=WHITE,
            buff=0.05,
            stroke_width=2
        )
        self.play(
            FadeIn(bright_line),
            Create(outline),
            run_time=max(0.05, 0.8
        ))
        remaining_beat8 = 38.46 - 32.72 - (0.8 + 0.5 + 0.8)
        self.wait(max(0.05, remaining_beat8))

        # ------------------------------------------------------------
        # Beat 9: 38.46–41.25  cleaner recordings + pulse
        # ------------------------------------------------------------
        self.label_clean = Text("cleaner recordings", font_size=24, color=GREEN, weight="BOLD")
        self.label_clean.to_edge(DOWN, buff=0.5)
        self.play(
            FadeOut(self.label_reduced),
            FadeIn(self.label_clean),
            run_time=max(0.05, 0.4
        ))

        # Pulse dot looping from skin through gel to disc to wire
        path_points = [
            self.gel.get_bottom(),
            self.gel.get_top(),
            self.disc.get_center(),
            self.wire.get_end()
        ]
        pulse_path = VMobject(stroke_width=0, fill_opacity=0)
        pulse_path.set_points_as_corners(path_points)
        pulse_dot = Dot(radius=0.06, color=GREEN, fill_opacity=1)
        pulse_dot.move_to(path_points[0])

        pulse_tracker = ValueTracker(0)
        pulse_tracker.add_updater(lambda m, dt: m.increment_value(dt * 0.7))
        pulse_dot.add_updater(
            lambda d: d.move_to(pulse_path.point_from_proportion(pulse_tracker.get_value() % 1.0))
        )
        self.add(pulse_dot, pulse_tracker)

        remaining_beat9 = 41.25 - 38.46 - 0.4
        self.wait(max(0.05, remaining_beat9))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def build_skin_cross(self):
        # Top irregular band (epidermis)
        vertices = [np.array([-3, -0.225, 0]), np.array([3, -0.225, 0])]
        top_x = np.linspace(-3, 3, 60)
        for x in top_x:
            y = 0.225 + 0.05 * np.sin(2 * np.pi * x * 0.8)
            vertices.append(np.array([x, y, 0]))
        vertices.append(np.array([-3, 0.225, 0]))
        top_band = Polygon(
            *vertices,
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1
        )

        # Deep dermis region
        dermis = Rectangle(
            width=6,
            height=2.6,
            fill_color=PINK,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1
        )
        dermis.move_to(np.array([0, -0.225 - 1.3, 0]))

        # Texture dots in dermis
        texture = VGroup()
        np.random.seed(42)
        for _ in range(18):
            x = np.random.uniform(-2.6, 2.6)
            y = np.random.uniform(-2.6, -0.35)
            dot = Ellipse(width=0.15, height=0.08, fill_color=ORANGE, fill_opacity=0.5, stroke_width=0)
            dot.move_to(np.array([x, y, 0]))
            texture.add(dot)

        # Clean top surface line
        top_surface_line = Line(
            start=np.array([-3, 0, 0]),
            end=np.array([3, 0, 0]),
            color=WHITE,
            stroke_width=3
        )

        skin_group = VGroup(top_band, dermis, texture, top_surface_line)
        # Shift so top is at y=1.5
        current_top = skin_group.get_top()[1]
        skin_group.shift(UP * (1.5 - current_top))
        return skin_group

    def build_electrode(self):
        disc = Ellipse(
            width=1.5,
            height=0.35,
            fill_color=GREY,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2
        )
        disc.move_to(ORIGIN)
        wire = Line(
            start=disc.get_top(),
            end=disc.get_top() + UP * 1.5,
            color=GREY_B,
            stroke_width=3
        )
        group = VGroup(disc, wire)
        return group, disc, wire

    def build_red_x(self, size=0.5):
        line1 = Line(
            [-size, -size, 0], [size, size, 0],
            color=RED,
            stroke_width=8
        )
        line2 = Line(
            [-size, size, 0], [size, -size, 0],
            color=RED,
            stroke_width=8
        )
        return VGroup(line1, line2)