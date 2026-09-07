ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Title and placeholder row layout
        title = Text("Advantages of Low-Pass Filtering", font_size=36, color=WHITE)
        title.scale_to_fit_width(8.5)

        self.row_circles = []
        self.row_lines = []
        rows_group = VGroup()

        for _ in range(4):
            circle = Circle(radius=0.18, stroke_width=2, fill_opacity=0)
            circle.set_stroke(color=GREY_B, width=2, opacity=0.55)

            line = Line(LEFT * 2.25, RIGHT * 2.25, color=GREY_B, stroke_width=2)
            line.set_opacity(0.35)
            line.next_to(circle, RIGHT, buff=0.4)

            row = VGroup(circle, line)
            rows_group.add(row)
            self.row_circles.append(circle)
            self.row_lines.append(line)

        rows_group.arrange(DOWN, buff=0.65)
        rows_group.move_to(LEFT * 1.8 + DOWN * 0.3)
        title.next_to(rows_group, UP, buff=0.8)

        self.item_groups = {}
        self.list_group = VGroup(title, rows_group)

        # Beat 1: 0.00 - 3.10
        self.play(FadeIn(rows_group), run_time=max(0.05, 1.70))
        self.play(FadeIn(title), run_time=max(0.05, 1.40))

        # Gap to 4.14
        self.wait(max(0.05, 1.04))

        # Beat 2: 4.14 - 6.38
        item1 = self.intro_item(
            0,
            "Reduces high-frequency noise",
            run_time=max(0.05, 1.44),
        )
        self.pulse_item_check(item1, 0.80)

        # Gap to 7.18
        self.wait(max(0.05, 0.80))

        # Beat 3: 7.18 - 8.66
        self.intro_item(
            1,
            "Produces smoother waveforms",
            run_time=max(0.05, 1.48),
            dim_items=[self.item_groups[0]],
        )

        # Gap to 9.40
        self.wait(max(0.05, 0.74))

        # Beat 4: 9.40 - 10.98
        self.intro_item(
            2,
            "Improves signal readability",
            run_time=max(0.05, 1.58),
            dim_items=[self.item_groups[0], self.item_groups[1]],
        )

        # Gap to 11.74
        self.wait(max(0.05, 0.76))

        # Beat 5: 11.74 - 15.70
        item4 = self.intro_item(
            3,
            "Preprocessing before feature extraction",
            run_time=max(0.05, 1.50),
            restore_items=[self.item_groups[0], self.item_groups[1]],
        )
        self.play(
            item4[0].animate.set_stroke(width=8),
            rate_func=there_and_back,
            run_time=max(0.05, 0.80),
        )
        self.wait(max(0.05, 1.66))

        # Beat 6: 15.70 - 16.55, gentle full-prominence hold
        ambient = SurroundingRectangle(
            self.list_group,
            color=YELLOW,
            buff=0.35,
            fill_color=YELLOW,
            fill_opacity=0.0,
            stroke_width=0,
            corner_radius=0.1,
        )
        self.add(ambient)
        self.bring_to_back(ambient)
        self.play(
            ambient.animate.set_fill(opacity=0.08),
            run_time=max(0.05, 0.85),
        )

    def make_checkmark(self, center):
        p1 = center + LEFT * 0.10 + DOWN * 0.03
        p2 = center + LEFT * 0.02 + UP * 0.06
        p3 = center + RIGHT * 0.11 + DOWN * 0.09
        line1 = Line(start=p1, end=p2, color=GREEN, stroke_width=7)
        line2 = Line(start=p2, end=p3, color=GREEN, stroke_width=7)
        return VGroup(line1, line2)

    def intro_item(self, idx, text, run_time, dim_items=None, restore_items=None):
        circle = self.row_circles[idx]
        checkmark = self.make_checkmark(circle.get_center())

        label = Text(text, font_size=28, color=WHITE)
        if label.width > 4.2:
            label.scale_to_fit_width(4.2)
        label.next_to(circle, RIGHT, buff=0.4)
        label.shift(LEFT * 4)
        label.set_opacity(0)

        anims = [
            label.animate.set_opacity(1).shift(RIGHT * 4),
            Create(checkmark),
            FadeOut(self.row_lines[idx]),
        ]

        if dim_items:
            for group in dim_items:
                anims.append(group.animate.set_opacity(0.45))

        if restore_items:
            for group in restore_items:
                anims.append(group.animate.set_opacity(1.0))

        self.play(*anims, run_time=max(0.05, run_time))

        item_group = VGroup(checkmark, label)
        self.item_groups[idx] = item_group
        self.list_group.add(item_group)

        return item_group

    def pulse_item_check(self, item_group, run_time):
        checkmark_group = item_group[0]
        center = checkmark_group.get_center()

        glow = Circle(
            radius=0.25,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.0,
            stroke_width=0,
        )
        glow.move_to(center)
        glow.set_opacity(0)

        self.add(glow)
        self.bring_to_back(glow)

        self.play(
            glow.animate.scale(1.8).set_opacity(0.35),
            rate_func=there_and_back,
            run_time=max(0.05, run_time),
        )

        self.remove(glow)