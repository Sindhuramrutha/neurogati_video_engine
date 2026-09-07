ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene6(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---- helpers -------------------------------------------------
        def make_microelectrode():
            shaft = Rectangle(width=0.04, height=2.2,
                              fill_color=GREY_B, fill_opacity=1,
                              stroke_color=WHITE, stroke_width=0.8)
            shaft.move_to(np.array([0, 0.22 + 1.1, 0]))
            tip = Polygon([-0.025, 0.22, 0], [0.025, 0.22, 0], [0, 0, 0],
                          fill_color=GREY_B, fill_opacity=1,
                          stroke_color=WHITE, stroke_width=0.8)
            return VGroup(shaft, tip).set_z_index(12)

        def make_action_potential():
            vm = VMobject()
            pts = [
                np.array([-1.0, 0, 0]),
                np.array([0, 0, 0]),
                np.array([0.08, 1.6, 0]),
                np.array([0.12, 1.6, 0]),
                np.array([0.5, -0.35, 0]),
                np.array([0.9, 0, 0]),
                np.array([1.2, 0, 0]),
            ]
            vm.set_points_as_corners(pts)
            vm.set_stroke(color=TEAL, width=3)
            vm.set_fill(opacity=0)
            vm.scale(0.65)
            return vm

        def make_zoom_lens():
            radius = 0.55
            lens_bg = Circle(radius=radius, fill_color=BLACK, fill_opacity=0.35,
                             stroke_color=WHITE, stroke_width=2)
            membrane_line = Line(LEFT * 0.28, RIGHT * 0.28,
                                 color=GOLD, stroke_width=4).shift(UP * 0.10)
            tip_line = Line(LEFT * 0.12, RIGHT * 0.12,
                            color=GREY_B, stroke_width=3).shift(DOWN * 0.20)
            gap_line = DashedLine([-0.06, 0.10, 0], [-0.06, -0.20, 0],
                                  color=YELLOW, stroke_width=1.5)
            close_up = VGroup(membrane_line, tip_line, gap_line)
            return VGroup(lens_bg, close_up)

        def make_grid_overlay(center, width=2.2, height=2.2, spacing=0.18):
            grid = VGroup()
            half_w = width / 2
            half_h = height / 2
            cx, cy = center[0], center[1]
            nx = int(width / spacing) + 1
            ny = int(height / spacing) + 1
            for i in range(-nx // 2, nx // 2 + 1):
                x = cx + i * spacing
                grid.add(Line([x, cy - half_h, 0], [x, cy + half_h, 0],
                              color=WHITE, stroke_width=0.7, stroke_opacity=0.5))
            for j in range(-ny // 2, ny // 2 + 1):
                y = cy + j * spacing
                grid.add(Line([cx - half_w, y, 0], [cx + half_w, y, 0],
                              color=WHITE, stroke_width=0.7, stroke_opacity=0.5))
            grid.set_opacity(0)
            grid.set_z_index(1)
            return grid

        def create_old_tissue():
            tissue = VGroup()
            neurons_list = []
            colors = [TEAL, GREEN, BLUE, PURPLE, PINK]

            prominent = Circle(radius=0.62, fill_color=GOLD, fill_opacity=0.45,
                               stroke_color=YELLOW, stroke_width=3)
            prominent.move_to(np.array([1.5, 0.0, 0]))
            tissue.add(prominent)

            for ang in [20, 80, 150, 210, 300, 340]:
                direction = np.array([np.cos(np.deg2rad(ang)),
                                      np.sin(np.deg2rad(ang)), 0])
                tissue.add(Line(prominent.get_center(),
                                prominent.get_center() + direction * (0.62 + 0.35),
                                color=YELLOW, stroke_width=1.4, stroke_opacity=0.40))

            neighbor_specs = [(2.5, 0.5, 0.30), (2.1, -0.7, 0.28), (0.7, 0.5, 0.32)]
            for i, (x, y, r) in enumerate(neighbor_specs):
                color = colors[i % len(colors)]
                c = Circle(radius=r, fill_color=color, fill_opacity=0.30,
                           stroke_color=WHITE, stroke_width=1.5, stroke_opacity=0.6)
                c.move_to(np.array([x, y, 0]))
                tissue.add(c)
                neurons_list.append(c)
                for ang in [30, 120, 220, 310]:
                    direction = np.array([np.cos(np.deg2rad(ang)),
                                          np.sin(np.deg2rad(ang)), 0])
                    tissue.add(Line(c.get_center(),
                                    c.get_center() + direction * (r + 0.30),
                                    color=color, stroke_width=1.0, stroke_opacity=0.30))

            other_positions = [
                (3.8, 1.4), (4.5, -1.0), (0.1, 1.1), (-0.5, -1.3),
                (4.0, -2.0), (5.1, 0.6), (3.0, 2.0), (0.9, -1.9),
                (5.4, -1.7), (-0.6, 0.0), (4.8, 2.0), (1.2, 1.5)
            ]
            rng = np.random.default_rng(10)
            for x, y in other_positions:
                r = float(rng.uniform(0.25, 0.45))
                color = colors[int(rng.integers(0, len(colors)))]
                c = Circle(radius=r, fill_color=color, fill_opacity=0.25,
                           stroke_color=WHITE, stroke_width=1.5, stroke_opacity=0.55)
                c.move_to(np.array([x, y, 0]))
                tissue.add(c)
                for ang in [30, 110, 210, 320]:
                    direction = np.array([np.cos(np.deg2rad(ang)),
                                          np.sin(np.deg2rad(ang)), 0])
                    tissue.add(Line(c.get_center(),
                                    c.get_center() + direction * (r + 0.35),
                                    color=color, stroke_width=1.0, stroke_opacity=0.28))

            return tissue, prominent, neurons_list

        def make_surgical_tissue():
            outer = Rectangle(width=6.4, height=3.8,
                              fill_color=PURPLE, fill_opacity=0.7,
                              stroke_color=WHITE, stroke_width=2)
            outer.move_to(np.array([2.8, -0.3, 0]))
            surface = Rectangle(width=6.4, height=0.24,
                                fill_color=PINK, fill_opacity=0.9,
                                stroke_color=WHITE, stroke_width=2)
            surface.move_to(np.array([2.8, 1.48, 0]))

            neuron_big = Circle(radius=0.55, fill_color=TEAL, fill_opacity=0.55,
                                stroke_color=WHITE, stroke_width=2)
            neuron_big.move_to(np.array([2.8, -0.4, 0]))
            neuron_small_l = Circle(radius=0.30, fill_color=GREEN, fill_opacity=0.40,
                                    stroke_color=WHITE, stroke_width=1.5)
            neuron_small_l.move_to(np.array([1.6, 0.2, 0]))
            neuron_small_r = Circle(radius=0.30, fill_color=BLUE, fill_opacity=0.40,
                                    stroke_color=WHITE, stroke_width=1.5)
            neuron_small_r.move_to(np.array([4.0, 0.1, 0]))

            group = VGroup(outer, surface, neuron_big, neuron_small_l, neuron_small_r)
            surface_top_y = surface.get_top()[1]
            return group, surface_top_y

        # ---- previous anatomical cross-section placeholder (opening) ----
        prev_skin = Rectangle(width=12, height=0.34, fill_color=PINK, fill_opacity=0.9,
                              stroke_color=WHITE, stroke_width=2)
        prev_skin.move_to(np.array([0, 0.85, 0]))
        prev_muscle = Rectangle(width=12, height=4.0, fill_color=MAROON, fill_opacity=0.9,
                                stroke_color=WHITE, stroke_width=2)
        prev_muscle.move_to(np.array([0, -1.32, 0]))
        prev_fibers = VGroup()
        for i in range(9):
            y = 0.55 - i * 0.28
            prev_fibers.add(Line(LEFT * 5.8 + UP * y, RIGHT * 5.8 + UP * y,
                                 color=WHITE, stroke_width=2, stroke_opacity=0.25))
        prev_cross_section = VGroup(prev_muscle, prev_fibers, prev_skin)

        old_tissue, prominent_neuron, neighbor_neurons = create_old_tissue()

        micro = make_microelectrode()
        micro_tip_to_center = micro.get_center() - micro.get_bottom()

        # ---- beat 1: cross-section opens into neural tissue, micro enters ----
        self.add(prev_cross_section)
        self.play(FadeOut(prev_cross_section), FadeIn(old_tissue), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 0.20))

        micro_enter_tip = np.array([-1.2, 1.4, 0])
        self.add(micro)
        self.play(micro.animate.move_to(micro_enter_tip + micro_tip_to_center),
                  run_time=max(0.05, 0.64))

        # ---- beat 2: slow descent, approaching but not touching ----
        approach_tip = np.array([1.5, 0.98, 0])
        self.play(micro.animate.move_to(approach_tip + micro_tip_to_center),
                  run_time=max(0.05, 1.52))
        self.wait(max(0.05, 0.20))

        # ---- beat 3: settles into near-contact, pulsing highlight ----
        final_tip = np.array([1.5, 0.82, 0])
        self.play(micro.animate.move_to(final_tip + micro_tip_to_center),
                  run_time=max(0.05, 0.70))

        tip_ring = Circle(radius=0.40, color=YELLOW,
                          fill_color=YELLOW, fill_opacity=0.10,
                          stroke_color=YELLOW, stroke_width=3)
        tip_ring.move_to(final_tip + DOWN * 0.06)
        self.play(GrowFromCenter(tip_ring), run_time=max(0.05, 0.40))

        cellular_label = Text("cellular level", font_size=24, color=WHITE)
        cellular_label.next_to(tip_ring, LEFT, buff=0.25)
        self.play(FadeIn(cellular_label), run_time=max(0.05, 0.30))

        self.play(tip_ring.animate.scale(1.2).set_opacity(0.6),
                  rate_func=there_and_back, run_time=max(0.05, 0.56))
        self.wait(max(0.05, 0.10))

        # gap to beat 4
        self.wait(max(0.05, 0.66))

        # ---- beat 4: neuron fires, action potential trace appears ----
        action_wave = make_action_potential()
        action_wave.move_to(np.array([3.6, -0.4, 0]))
        lead_line = Line(final_tip,
                         action_wave.get_left() + RIGHT * 0.15 + UP * 0.10,
                         color=TEAL, stroke_width=1.5, stroke_opacity=0.8)

        self.play(FadeIn(lead_line), run_time=max(0.05, 0.30))
        self.play(Create(action_wave), run_time=max(0.05, 0.90))
        self.play(Indicate(action_wave, scale_factor=1.05, color=YELLOW),
                  run_time=max(0.05, 0.52))
        self.wait(max(0.05, 0.40))

        # ---- beat 5: single neuron vs small group ----
        prominent_highlight = Circle(radius=0.75, color=YELLOW,
                                     stroke_width=3, fill_opacity=0)
        prominent_highlight.move_to(prominent_neuron.get_center())
        self.play(FadeIn(prominent_highlight), run_time=max(0.05, 0.50))

        cluster_highlight = VGroup()
        for n in neighbor_neurons:
            ring = Circle(radius=n.radius + 0.10, color=PINK,
                          stroke_width=3, fill_opacity=0)
            ring.move_to(n.get_center())
            cluster_highlight.add(ring)
        self.play(FadeIn(cluster_highlight), run_time=max(0.05, 0.60))

        small_wave = action_wave.copy().scale(0.55)
        small_wave.set_color(PINK).set_stroke(width=2.5)
        small_wave.move_to(cluster_highlight.get_center() + LEFT * 2.3 + UP * 0.8)
        self.play(FadeIn(small_wave), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.64))

        # gap to beat 6
        self.wait(max(0.05, 0.50))

        # ---- beat 6: comparison fades, zoom circle appears ----
        self.play(FadeOut(VGroup(cluster_highlight, small_wave)), run_time=max(0.05, 0.40))

        zoom_lens = make_zoom_lens()
        zoom_lens.move_to(np.array([0.9, 1.6, 0]))
        self.play(GrowFromCenter(zoom_lens), run_time=max(0.05, 0.50))
        self.wait(max(0.05, 0.22))

        # ---- beat 7: clean view, first label ----
        self.play(FadeOut(action_wave), FadeOut(lead_line),
                  FadeOut(zoom_lens), FadeOut(tip_ring),
                  FadeOut(cellular_label), run_time=max(0.05, 0.60))

        label_research = Text("neuroscience research", font_size=30,
                              weight="BOLD", color=WHITE)
        label_research.move_to(np.array([-3.9, 2.7, 0]))
        self.play(FadeIn(label_research), run_time=max(0.05, 0.50))
        self.play(label_research.animate.set_color(YELLOW),
                  rate_func=there_and_back, run_time=max(0.05, 0.60))
        self.wait(max(0.05, 1.14))

        # gap to beat 8
        self.wait(max(0.05, 0.60))

        # ---- beat 8: stack labels ----
        label_neurophys = Text("neurophysiology", font_size=28, color=WHITE)
        label_neurophys.next_to(label_research, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(label_neurophys), run_time=max(0.05, 0.42))

        label_bci = Text("BCI studies", font_size=28, color=WHITE)
        label_bci.next_to(label_neurophys, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(label_bci), run_time=max(0.05, 0.42))
        self.wait(max(0.05, 0.48))

        # gap to beat 9
        self.wait(max(0.05, 0.68))

        # ---- beat 9: slight zoom + fine resolution grid ----
        grid_overlay = make_grid_overlay(final_tip, width=2.4, height=2.4, spacing=0.18)

        self.play(self.camera.frame.animate.scale(0.88).move_to(np.array([1.8, 0.0, 0])),
                  run_time=max(0.05, 1.20))
        self.play(grid_overlay.animate.set_opacity(0.20), run_time=max(0.05, 0.60))
        self.play(grid_overlay.animate.set_opacity(0.50), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.84))

        # gap to beat 10
        self.wait(max(0.05, 1.22))

        # ---- beat 10: shift to surgical implantation view ----
        surgical_tissue, surface_top_y = make_surgical_tissue()
        entry_point = np.array([2.8, surface_top_y, 0])
        insert_start_tip = entry_point + UP * 0.3
        surgical_target_tip = np.array([2.8, 0.25, 0])
        insertion_line = DashedLine(entry_point, surgical_target_tip,
                                    color=WHITE, stroke_width=2,
                                    dash_length=0.08, stroke_opacity=0.6)

        self.play(FadeOut(VGroup(label_research, label_neurophys, label_bci)),
                  FadeOut(grid_overlay),
                  self.camera.frame.animate.scale(1 / 0.88).move_to(ORIGIN),
                  run_time=max(0.05, 0.40))

        self.play(FadeOut(old_tissue), FadeOut(prominent_highlight),
                  FadeIn(surgical_tissue), run_time=max(0.05, 0.55))

        self.play(micro.animate.move_to(insert_start_tip + micro_tip_to_center),
                  Create(insertion_line), run_time=max(0.05, 0.40))
        self.play(micro.animate.move_to(surgical_target_tip + micro_tip_to_center),
                  run_time=max(0.05, 0.47))
        self.wait(max(0.05, 0.30))

        # gap to beat 11
        self.wait(max(0.05, 0.60))

        # ---- beat 11: procedural surgical marks ----
        guide_h = Line(entry_point + LEFT * 0.42, entry_point + RIGHT * 0.42,
                       color=TEAL, stroke_width=2)
        guide_v = Line(entry_point + DOWN * 0.42, entry_point + UP * 0.42,
                       color=TEAL, stroke_width=2)
        sterile_ring = Circle(radius=0.50, color=TEAL, stroke_width=2,
                              fill_opacity=0).move_to(entry_point)
        procedural_marks = VGroup(guide_h, guide_v, sterile_ring)

        self.play(FadeIn(procedural_marks), run_time=max(0.05, 0.80))
        self.wait(max(0.05, 0.94))

        # ---- beat 12: invasive warning ----
        red_glow = Circle(radius=0.28, color=RED,
                          fill_color=RED, fill_opacity=0.20,
                          stroke_color=RED, stroke_width=3)
        red_glow.move_to(entry_point)
        self.play(FadeIn(red_glow), run_time=max(0.05, 0.40))

        invasive_label = Text("highly invasive", font_size=24, color=RED)
        invasive_label.next_to(red_glow, RIGHT, buff=0.30)
        self.play(FadeIn(invasive_label), run_time=max(0.05, 0.40))

        self.play(red_glow.animate.scale(1.25).set_opacity(0.65),
                  rate_func=there_and_back, run_time=max(0.05, 0.60))
        self.wait(max(0.05, 0.40))

        # ---- beat 13: calm hold to end ----
        self.wait(max(0.05, 0.88))