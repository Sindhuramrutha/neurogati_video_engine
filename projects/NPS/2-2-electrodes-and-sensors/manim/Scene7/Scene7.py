ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene7(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        X_MIN, X_MAX = -5.6, 5.6

        def signal_y(x):
            return 0.0 + 2.2 * (np.tanh((x - 0.2) / 2.0) + 1) / 2

        def invasiveness_y(x):
            return -0.2 + 1.9 * (np.tanh((x - 0.0) / 2.0) + 1) / 2

        def make_curve(func, color, width=3.5, opacity=0.85):
            pts = [np.array([x, func(x), 0]) for x in np.linspace(X_MIN, X_MAX, 80)]
            curve = VMobject()
            curve.set_points_smoothly(pts)
            curve.set_stroke(color=color, width=width, opacity=opacity)
            return curve

        # Beat 1: labeled horizontal axis
        axis = Line(np.array([X_MIN, -0.8, 0]), np.array([X_MAX, -0.8, 0]),
                    color=WHITE, stroke_width=3)
        distance_label = Text("Distance from source", font_size=24, color=WHITE)
        distance_label.next_to(axis.get_left(), UP, buff=0.25, aligned_edge=LEFT)
        position_label = Text("Electrode position", font_size=24, color=WHITE)
        position_label.next_to(axis.get_center(), UP, buff=0.25)

        self.play(FadeIn(axis), FadeIn(distance_label), FadeIn(position_label),
                  run_time=max(0.05, 1.36))

        # Beat 2: electrode icons
        surface_rect = Rectangle(width=1.4, height=0.4,
                                 fill_color=BLUE, fill_opacity=1,
                                 stroke_color=WHITE, stroke_width=1.5)
        surface_rect.move_to(np.array([-5.0, -0.6, 0]))
        needle_rect = Rectangle(width=0.28, height=1.2,
                                fill_color=GREEN, fill_opacity=1,
                                stroke_color=WHITE, stroke_width=1.5)
        needle_rect.move_to(np.array([2.0, -0.2, 0]))
        micro_rect = Rectangle(width=0.07, height=1.0,
                               fill_color=PURPLE, fill_opacity=1,
                               stroke_color=WHITE, stroke_width=1)
        micro_rect.move_to(np.array([5.3, -0.3, 0]))

        surface_label = Text("Surface", font_size=22, color=WHITE)
        surface_label.next_to(surface_rect, DOWN, buff=0.3)
        needle_label = Text("Needle", font_size=22, color=WHITE)
        needle_label.next_to(needle_rect, DOWN, buff=0.3)
        micro_label = Text("Micro", font_size=22, color=WHITE)
        micro_label.next_to(micro_rect, DOWN, buff=0.5)

        micro_rect.set_z_index(15)
        micro_label.set_z_index(15)
        surface_rect.set_z_index(12)
        needle_rect.set_z_index(12)

        electrode_group = VGroup(surface_rect, surface_label,
                                 needle_rect, needle_label,
                                 micro_rect, micro_label)
        dim_group = VGroup(surface_rect, surface_label,
                           needle_rect, needle_label)

        self.play(FadeIn(electrode_group), run_time=max(0.05, 1.62))

        # Beat 3: highlight microelectrode, mark source direction
        micro_glow = Circle(radius=0.75,
                            fill_color=YELLOW, fill_opacity=0.25,
                            stroke_color=YELLOW, stroke_width=2,
                            stroke_opacity=0.6)
        micro_glow.move_to(micro_rect.get_center())
        micro_glow.set_z_index(7)

        axis_marker = Arrow(start=np.array([5.3, -1.0, 0]),
                            end=np.array([5.3, -0.8, 0]),
                            color=YELLOW, buff=0, stroke_width=4,
                            max_tip_length_to_length_ratio=0.6)

        source_arrow = Arrow(start=axis.get_right() + LEFT * 0.7,
                             end=axis.get_right() + RIGHT * 0.02,
                             color=YELLOW, buff=0, stroke_width=5,
                             max_tip_length_to_length_ratio=0.5)
        source_label = Text("source", font_size=22, color=YELLOW)
        source_label.next_to(source_arrow, UP, buff=0.12)

        self.play(dim_group.animate.set_opacity(0.35),
                  FadeIn(micro_glow), run_time=max(0.05, 0.9))
        self.play(FadeIn(axis_marker), run_time=max(0.05, 0.6))
        self.play(FadeIn(source_arrow), FadeIn(source_label), run_time=max(0.05, 0.98))

        # Curves
        signal_curve = make_curve(signal_y, TEAL, width=3.5, opacity=0.8)
        invasiveness_curve = make_curve(invasiveness_y, ORANGE, width=3.5, opacity=0.8)

        signal_label = Text("Signal quality", font_size=24, color=TEAL)
        signal_label.move_to(np.array([3.4, signal_y(3.4) + 0.45, 0]))
        invasiveness_label = Text("Invasiveness", font_size=24, color=ORANGE)
        invasiveness_label.move_to(np.array([3.4, invasiveness_y(3.4) - 0.45, 0]))

        # Beat 4: signal quality curve + moving dot
        signal_dot = Dot(radius=0.08, color=YELLOW, z_index=20)
        signal_dot.move_to(signal_curve.point_from_proportion(0))

        self.play(FadeIn(signal_curve), FadeIn(signal_label), run_time=max(0.05, 0.9))
        self.play(GrowFromCenter(signal_dot), run_time=max(0.05, 0.2))
        self.play(signal_curve.animate.set_stroke(width=6, opacity=1.0),
                  MoveAlongPath(signal_dot, signal_curve),
                  run_time=max(0.05, 1.08))

        # Beat 5: invasiveness curve, labels, legend chips
        legend_signal = Rectangle(width=0.3, height=0.3,
                                  fill_color=TEAL, fill_opacity=1,
                                  stroke_color=TEAL, stroke_width=1)
        legend_signal.next_to(signal_label, LEFT, buff=0.12)
        legend_invasiveness = Rectangle(width=0.3, height=0.3,
                                        fill_color=ORANGE, fill_opacity=1,
                                        stroke_color=ORANGE, stroke_width=1)
        legend_invasiveness.next_to(invasiveness_label, LEFT, buff=0.12)

        self.play(FadeOut(signal_dot), run_time=max(0.05, 0.2))
        self.play(FadeIn(invasiveness_curve), run_time=max(0.05, 2.4))
        self.play(FadeIn(invasiveness_label),
                  FadeIn(legend_signal),
                  FadeIn(legend_invasiveness),
                  run_time=max(0.05, 0.8))
        self.wait(max(0.05, 0.36))

        # Beat 6: paired dots climb both curves
        dot_sig2 = Dot(radius=0.08, color=YELLOW, z_index=20)
        dot_sig2.move_to(signal_curve.point_from_proportion(0))
        dot_inv2 = Dot(radius=0.08, color=YELLOW, z_index=20)
        dot_inv2.move_to(invasiveness_curve.point_from_proportion(0))

        self.play(FadeIn(dot_sig2), FadeIn(dot_inv2), run_time=max(0.05, 0.2))
        self.play(invasiveness_curve.animate.set_stroke(width=6, opacity=1.0),
                  MoveAlongPath(dot_sig2, signal_curve),
                  MoveAlongPath(dot_inv2, invasiveness_curve),
                  run_time=max(0.05, 1.3))

        # Beat 7: dashed vertical drop lines
        drop_lines = VGroup()
        for x, top_y in [(-5.0, -0.4), (2.0, 0.4), (5.3, 0.2)]:
            drop_lines.add(
                DashedLine(np.array([x, signal_y(x), 0]),
                           np.array([x, top_y, 0]),
                           color=WHITE, dash_length=0.08,
                           stroke_width=2)
            )
        drop_lines.set_stroke(width=1.6, opacity=0.7)
        drop_lines.set_z_index(4)

        self.play(FadeOut(dot_sig2, dot_inv2), run_time=max(0.05, 0.2))
        self.play(Create(drop_lines), run_time=max(0.05, 1.6))
        self.wait(max(0.05, 0.66))

        # Beat 8: the closing trade-off label
        tradeoff_label = Text("The fundamental trade-off",
                              font_size=36, weight="BOLD", color=YELLOW)
        tradeoff_label.move_to(np.array([0, 3.2, 0]))

        self.play(FadeIn(tradeoff_label), run_time=max(0.05, 0.52))
        self.play(tradeoff_label.animate.scale(1.08).set_opacity(0.8),
                  rate_func=there_and_back, run_time=max(0.05, 0.52))
        self.wait(max(0.05, 0.48))