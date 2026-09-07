ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {}

class Scene12(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        self.main_scene = VGroup()

        def add_to_main(*mobjects):
            self.main_scene.add(*mobjects)

        # --------------------------------------------------------------
        # helper builders
        # --------------------------------------------------------------
        def build_person():
            head = Ellipse(
                width=0.75, height=0.90,
                fill_color=GREY_B, fill_opacity=1,
                stroke_color=BLUE, stroke_width=3,
            ).move_to([-5.3, 0.75, 0])

            nose = Polygon(
                head.get_right() + RIGHT * 0.08 + UP * 0.08,
                head.get_right() + RIGHT * 0.24 + DOWN * 0.00,
                head.get_right() + RIGHT * 0.05 + DOWN * 0.16,
                fill_color=GREY_B, fill_opacity=1,
                stroke_color=BLUE, stroke_width=2,
            )

            body = RoundedRectangle(
                width=1.8, height=1.6, corner_radius=0.35,
                fill_color=GREY_B, fill_opacity=1,
                stroke_color=BLUE, stroke_width=3,
            ).move_to([-5.35, -1.35, 0])

            chair_seat = Line([-6.0, -1.85, 0], [-4.55, -1.85, 0],
                              color=WHITE, stroke_width=3)
            chair_back = Line([-5.75, -1.95, 0], [-5.75, -0.75, 0],
                              color=WHITE, stroke_width=3)
            chair = VGroup(chair_seat, chair_back)

            person = VGroup(head, nose, body, chair)
            return person, head, nose, body

        def build_device_on_scalp(head):
            device = VGroup(
                RoundedRectangle(
                    width=0.30, height=0.20, corner_radius=0.06,
                    fill_color=GREY_B, fill_opacity=1,
                    stroke_color=WHITE, stroke_width=1.8,
                ),
                Dot(radius=0.045, color=GREEN, fill_opacity=1),
            ).move_to(head.get_top() + UP * 0.08)
            return device

        def build_thought_bubble(center):
            bubble = Ellipse(
                width=1.55, height=1.00,
                stroke_color=WHITE, stroke_width=2,
            ).move_to(center)

            tail1 = Circle(radius=0.05, color=WHITE, stroke_width=1)
            tail1.move_to(center + DOWN * 0.42 + LEFT * 0.05)
            tail2 = Circle(radius=0.04, color=WHITE, stroke_width=1)
            tail2.move_to(center + DOWN * 0.56 + LEFT * 0.18)

            shoulder = center + LEFT * 0.50 + DOWN * 0.28
            elbow = shoulder + RIGHT * 0.34 + UP * 0.06
            hand = elbow + RIGHT * 0.40 + DOWN * 0.16

            upper_arm = Line(shoulder, elbow, color=WHITE, stroke_width=3)
            forearm_line = Line(elbow, hand, color=WHITE, stroke_width=3)
            hand_dot = Dot(hand, radius=0.055, color=ORANGE, fill_opacity=1)
            forearm_group = VGroup(forearm_line, hand_dot)
            arm_in_bubble = VGroup(upper_arm, forearm_group)

            thought_bubble = VGroup(bubble, tail1, tail2, arm_in_bubble)
            return thought_bubble, arm_in_bubble, forearm_group, elbow

        def build_robotic_arm():
            base = RoundedRectangle(
                width=0.85, height=0.28, corner_radius=0.08,
                fill_color=GREY_B, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.8,
            ).move_to([5.0, -1.5, 0])

            base_top = base.get_top()
            arm_link = Line(
                base_top,
                base_top + RIGHT * 0.5 + UP * 0.4,
                color=GREY_B,
                stroke_width=5,
            )
            effector = Dot(arm_link.get_end(), radius=0.07,
                           color=YELLOW, fill_opacity=1)

            arm_group = VGroup(arm_link, effector)
            robotic_arm = VGroup(base, arm_group)
            return robotic_arm, arm_group, base, base_top, effector

        def build_feature_cards():
            # spike counts bar chart
            card1_bg = RoundedRectangle(
                width=1.15, height=0.80, corner_radius=0.08,
                fill_color=GREY, fill_opacity=0.20,
                stroke_color=WHITE, stroke_width=1.2,
            )
            bars = VGroup()
            heights = [0.09, 0.17, 0.12, 0.20, 0.14]
            for i, h in enumerate(heights):
                bar = Rectangle(
                    width=0.10, height=h,
                    fill_color=ORANGE, fill_opacity=1, stroke_width=0,
                )
                bar.move_to(
                    card1_bg.get_center() + LEFT * 0.30
                    + RIGHT * 0.15 * i + DOWN * 0.06
                )
                bars.add(bar)
            label1 = Text("spike counts", font_size=8, color=WHITE)
            label1.next_to(card1_bg, DOWN, buff=0.05)
            card1 = VGroup(card1_bg, bars, label1)

            # firing rates line graph
            card2_bg = RoundedRectangle(
                width=1.15, height=0.80, corner_radius=0.08,
                fill_color=GREY, fill_opacity=0.20,
                stroke_color=WHITE, stroke_width=1.2,
            )
            line2 = FunctionGraph(
                lambda x: 0.18 * np.sin(2.4 * x),
                x_range=[-0.38, 0.38, 0.02],
                color=TEAL,
                stroke_width=2.5,
            ).move_to(card2_bg.get_center())
            label2 = Text("firing rates", font_size=8, color=WHITE)
            label2.next_to(card2_bg, DOWN, buff=0.05)
            card2 = VGroup(card2_bg, line2, label2)

            # frequency-specific power spectrum
            card3_bg = RoundedRectangle(
                width=1.15, height=0.80, corner_radius=0.08,
                fill_color=GREY, fill_opacity=0.20,
                stroke_color=WHITE, stroke_width=1.2,
            )
            spectrum = FunctionGraph(
                lambda x: 0.22 * np.exp(-((x - 0.05) / 0.13) ** 2),
                x_range=[-0.42, 0.42, 0.02],
                color=PURPLE,
                stroke_width=2.5,
            ).move_to(card3_bg.get_center())
            label3 = Text("frequency-specific power", font_size=8, color=WHITE)
            label3.next_to(card3_bg, DOWN, buff=0.05)
            card3 = VGroup(card3_bg, spectrum, label3)

            # multiple neurons small grid
            card4_bg = RoundedRectangle(
                width=1.15, height=0.80, corner_radius=0.08,
                fill_color=GREY, fill_opacity=0.20,
                stroke_color=WHITE, stroke_width=1.2,
            )
            neurons = VGroup()
            for dx in [-0.22, -0.07, 0.08, 0.23]:
                neuron = Circle(
                    radius=0.045, fill_color=GREY_B, fill_opacity=1,
                    stroke_color=WHITE, stroke_width=1,
                ).move_to(card4_bg.get_center() + [dx, -0.07, 0])
                spike = Line(
                    neuron.get_top() + UP * 0.01,
                    neuron.get_top() + UP * 0.15,
                    color=YELLOW, stroke_width=1.6,
                )
                neurons.add(VGroup(neuron, spike))
            label4 = Text("multiple neurons", font_size=8, color=WHITE)
            label4.next_to(card4_bg, DOWN, buff=0.05)
            card4 = VGroup(card4_bg, neurons, label4)

            cards = VGroup(card1, card2, card3, card4)
            cards.arrange_in_grid(rows=2, cols=2, buff=0.20)
            cards.move_to([0.5, -1.3, 0])
            return cards

        def build_network_model(center):
            input_nodes = VGroup(
                Dot(center + LEFT * 0.9 + UP * 0.35, radius=0.07,
                    color=YELLOW, fill_opacity=1),
                Dot(center + LEFT * 0.9 + DOWN * 0.35, radius=0.07,
                    color=YELLOW, fill_opacity=1),
            )
            hidden_nodes = VGroup(
                Dot(center + UP * 0.55, radius=0.07,
                    color=ORANGE, fill_opacity=1),
                Dot(center + ORIGIN, radius=0.07,
                    color=ORANGE, fill_opacity=1),
                Dot(center + DOWN * 0.55, radius=0.07,
                    color=ORANGE, fill_opacity=1),
            )
            output_nodes = VGroup(
                Dot(center + RIGHT * 0.9 + UP * 0.35, radius=0.07,
                    color=TEAL, fill_opacity=1),
                Dot(center + RIGHT * 0.9 + DOWN * 0.35, radius=0.07,
                    color=TEAL, fill_opacity=1),
            )

            connections = VGroup()
            for inp in input_nodes:
                for hid in hidden_nodes:
                    connections.add(
                        Line(inp.get_center(), hid.get_center(),
                             color=GREY_B, stroke_width=1.1)
                    )
            for hid in hidden_nodes:
                for out in output_nodes:
                    connections.add(
                        Line(hid.get_center(), out.get_center(),
                             color=GREY_B, stroke_width=1.1)
                    )

            weight_label = Text("weights", font_size=10, color=GREY_B)
            weight_label.next_to(connections[0], LEFT, buff=0.04)

            network = VGroup(
                connections, input_nodes, hidden_nodes,
                output_nodes, weight_label,
            )
            network.move_to(center)
            return network, input_nodes, hidden_nodes, output_nodes

        # --------------------------------------------------------------
        # Build all permanent objects, but only add to main_scene when they
        # become part of the persistent composition.
        # --------------------------------------------------------------
        person_group, head, nose, body = build_person()
        device = build_device_on_scalp(head)
        cable = Line(
            device.get_center() + LEFT * 0.20,
            np.array([-6.5, device.get_center()[1], 0]),
            color=GREY_B,
            stroke_width=3,
        )

        bubble_center = head.get_top() + UP * 0.82 + RIGHT * 0.25
        thought_bubble_group, arm_in_bubble, forearm_group, elbow = (
            build_thought_bubble(bubble_center)
        )

        robotic_arm, arm_group, robot_base, base_top, effector = (
            build_robotic_arm()
        )

        # add persistent core (they exist from the start and remain)
        add_to_main(person_group, device, cable)
        add_to_main(thought_bubble_group)
        add_to_main(robotic_arm)

        # --------------------------------------------------------------
        # Beat 1: 0.00 - 2.82
        # --------------------------------------------------------------
        # previous scene dim visual
        prev_visual = VGroup(
            RoundedRectangle(
                width=5.0, height=1.2, corner_radius=0.12,
                fill_color=GREY_B, fill_opacity=0.25,
                stroke_color=GREY_B, stroke_width=2,
            ),
            Text("neural prosthesis pipeline", font_size=25, color=WHITE),
        ).move_to(ORIGIN).set_opacity(0.45)
        self.add(prev_visual)

        self.play(
            FadeOut(prev_visual),
            FadeIn(person_group, device, cable),
            run_time=max(0.05, 0.74),
        )
        self.play(
            Indicate(person_group, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.68),
        )
        self.play(
            FadeIn(thought_bubble_group),
            run_time=max(0.05, 0.68),
        )
        self.play(
            FadeIn(robotic_arm),
            run_time=max(0.05, 0.26),
        )
        self.play(
            forearm_group.animate.rotate(0.28, about_point=elbow),
            run_time=max(0.05, 0.46),
        )

        # gap 2.82 -> 3.60
        self.wait(max(0.05, 0.78))

        # --------------------------------------------------------------
        # Beat 2: 3.60 - 5.32
        # --------------------------------------------------------------
        self.wait(max(0.05, 0.04))  # 3.60 -> 3.64

        system_rect = DashedVMobject(
            Rectangle(width=12.8, height=6.6),
            num_dashes=60,
        ).move_to([0, -0.1, 0]).set_stroke(WHITE, width=2)
        self.play(Create(system_rect), run_time=max(0.05, 0.50))  # 3.64 -> 4.14
        add_to_main(system_rect)

        cable_start = device.get_center() + LEFT * 0.20
        cable_end = cable.get_end()

        # 4.14 pulse
        pulse = Dot(cable_start, radius=0.05, color=YELLOW, fill_opacity=1)
        self.add(pulse)
        self.play(pulse.animate.move_to(cable_end), run_time=max(0.05, 0.28))  # 4.14 -> 4.42
        self.remove(pulse)

        # 4.42 device brightens
        self.play(
            Indicate(device, color=YELLOW, scale_factor=1.35),
            run_time=max(0.05, 0.32),  # 4.42 -> 4.74
        )

        # 4.74 live waveform panel
        wave_panel_bg = Rectangle(
            width=2.4, height=1.8,
            fill_color=BLACK, fill_opacity=0.75,
            stroke_color=GREY_B, stroke_width=2,
        ).move_to([-3.0, 1.2, 0])
        live_wave = FunctionGraph(
            lambda x: 0.24 * np.sin(3.2 * x),
            x_range=[-1.0, 1.0, 0.03],
            color=YELLOW,
            stroke_width=2.5,
        ).move_to(wave_panel_bg.get_center())

        self.play(
            FadeIn(wave_panel_bg),
            Create(live_wave),
            run_time=max(0.05, 0.58),  # 4.74 -> 5.32
        )

        # --------------------------------------------------------------
        # gap 5.32 -> 5.82
        self.wait(max(0.05, 0.50))

        # --------------------------------------------------------------
        # Beat 3: 5.82 - 8.20
        # --------------------------------------------------------------
        top_panel = Rectangle(
            width=2.4, height=1.0,
            fill_color=BLACK, fill_opacity=0.80,
            stroke_color=GREY_B, stroke_width=2,
        ).move_to([-3.0, 1.7, 0])
        bottom_panel = Rectangle(
            width=2.4, height=1.0,
            fill_color=BLACK, fill_opacity=0.80,
            stroke_color=GREY_B, stroke_width=2,
        ).move_to([-3.0, 0.7, 0])

        top_label = Text("Spikes", font_size=14, color=WHITE, weight=BOLD)
        top_label.next_to(top_panel, UP, buff=0.08)
        bottom_label = Text("LFP", font_size=14, color=WHITE, weight=BOLD)
        bottom_label.next_to(bottom_panel, UP, buff=0.08)

        self.play(
            FadeOut(wave_panel_bg, live_wave),
            FadeIn(top_panel, bottom_panel, top_label, bottom_label),
            run_time=max(0.05, 0.16),  # 5.82 -> 5.98
        )

        # 5.98 spike ticks
        spike_ticks = VGroup()
        tick_xs = [-0.85, -0.58, -0.32, -0.02, 0.22, 0.48, 0.70, 0.92]
        for x in tick_xs:
            spike_ticks.add(
                Line(
                    top_panel.get_bottom() + [x, 0.10, 0],
                    top_panel.get_bottom() + [x, 0.38, 0],
                    color=YELLOW, stroke_width=2.2,
                )
            )
        self.play(
            LaggedStart(*[Create(tick) for tick in spike_ticks],
                        lag_ratio=0.40),
            run_time=max(0.05, 0.92),  # 5.98 -> 6.90
        )

        # 6.90 LFP bold wave, bottom brightens
        lfp_wave = FunctionGraph(
            lambda x: 0.20 * np.sin(3.8 * x),
            x_range=[-0.95, 0.95, 0.03],
            color=PURPLE,
            stroke_width=4,
        ).move_to(bottom_panel.get_center())
        self.play(
            bottom_panel.animate.set_stroke(PURPLE, width=3),
            Create(lfp_wave),
            run_time=max(0.05, 0.42),  # 6.90 -> 7.32
        )

        # 7.32 LFP pulse softly (opacity dip and return)
        self.play(lfp_wave.animate.set_opacity(0.5), run_time=max(0.05, 0.44))  # 7.32 -> 7.76
        self.play(lfp_wave.animate.set_opacity(1.0), run_time=max(0.05, 0.44))  # 7.76 -> 8.20

        waveform_subpanels = VGroup(
            top_panel, bottom_panel,
            top_label, bottom_label,
            spike_ticks, lfp_wave,
        )
        add_to_main(waveform_subpanels)

        # --------------------------------------------------------------
        # gap 8.20 -> 8.52
        self.wait(max(0.05, 0.32))

        # --------------------------------------------------------------
        # Beat 4: 8.52 - 10.12
        # --------------------------------------------------------------
        feature_cards = build_feature_cards()
        add_to_main(feature_cards)

        self.play(
            waveform_subpanels.animate.scale(0.65).move_to([-3.8, 1.95, 0]),
            FadeIn(feature_cards),
            run_time=max(0.05, 0.34),  # 8.52 -> 8.86
        )

        feature_highlight = DashedVMobject(
            SurroundingRectangle(feature_cards, buff=0.14),
            num_dashes=32,
        ).set_stroke(YELLOW, width=2)
        self.play(Create(feature_highlight), run_time=max(0.05, 0.84))  # 8.86 -> 9.70
        add_to_main(feature_highlight)

        self.play(
            Indicate(feature_cards, color=YELLOW, scale_factor=1.12),
            run_time=max(0.05, 0.42),  # 9.70 -> 10.12
        )

        # --------------------------------------------------------------
        # gap 10.12 -> 10.84
        self.wait(max(0.05, 0.72))

        # --------------------------------------------------------------
        # Beat 5: 10.84 - 13.70
        # --------------------------------------------------------------
        self.play(
            feature_cards.animate.set_opacity(0.50),
            run_time=max(0.05, 0.20),  # 10.84 -> 11.04
        )

        model_center = np.array([1.8, 0.9, 0])
        network_model, input_nodes, hidden_nodes, output_nodes = (
            build_network_model(model_center)
        )
        self.play(FadeIn(network_model), run_time=max(0.05, 0.28))  # 11.04 -> 11.32
        add_to_main(network_model)

        self.play(
            Indicate(network_model, color=YELLOW, scale_factor=1.06),
            run_time=max(0.05, 0.94),  # 11.32 -> 12.26
        )

        packet_start_a = feature_cards.get_center() + LEFT * 0.8 + UP * 0.35
        packet_start_b = feature_cards.get_center() + RIGHT * 0.8 + UP * 0.35
        packet_a = Dot(packet_start_a, radius=0.05, color=TEAL, fill_opacity=1)
        packet_b = Dot(packet_start_b, radius=0.05, color=GREEN, fill_opacity=1)
        self.add(packet_a, packet_b)
        self.play(
            packet_a.animate.move_to(input_nodes[0].get_center()),
            packet_b.animate.move_to(input_nodes[1].get_center()),
            run_time=max(0.05, 0.64),  # 12.26 -> 12.90
        )
        self.remove(packet_a, packet_b)

        self.play(
            Indicate(arm_in_bubble, color=ORANGE, scale_factor=1.12),
            run_time=max(0.05, 0.18),  # 12.90 -> 13.08
        )

        output_center = output_nodes.get_center()
        trajectory_line = DashedLine(
            output_center + RIGHT * 0.35,
            output_center + RIGHT * 1.9,
            color=GREY_B,
            dash_length=0.09,
            stroke_width=3,
        )
        self.play(Create(trajectory_line), run_time=max(0.05, 0.62))  # 13.08 -> 13.70

        # --------------------------------------------------------------
        # gap 13.70 -> 14.38
        self.wait(max(0.05, 0.68))

        # --------------------------------------------------------------
        # Beat 6: 14.38 - 16.38
        # --------------------------------------------------------------
        final_trajectory = DashedLine(
            output_center + RIGHT * 0.35,
            robot_base.get_left() + LEFT * 0.12,
            color=GREY_B,
            dash_length=0.09,
            stroke_width=3,
        )
        self.play(
            Transform(trajectory_line, final_trajectory),
            run_time=max(0.05, 0.44),  # 14.38 -> 14.82
        )

        thought_arm_overlay = arm_in_bubble.copy()
        thought_arm_overlay.set_color(ORANGE).set_opacity(0.95)
        traj_center = trajectory_line.get_center()
        self.play(
            FadeIn(thought_arm_overlay),
            thought_arm_overlay.animate.move_to(traj_center).rotate(PI / 8),
            run_time=max(0.05, 0.78),  # 14.82 -> 15.60
        )

        control_arrow = Arrow(
            output_center + RIGHT * 0.35,
            robot_base.get_left() + LEFT * 0.08,
            color=YELLOW,
            stroke_width=5,
            buff=0.10,
            max_tip_length_to_length_ratio=0.18,
        )
        control_label = Text("control command", font_size=16,
                             color=YELLOW, weight=BOLD)
        control_label.next_to(control_arrow, UP, buff=0.10)
        self.play(
            ReplacementTransform(trajectory_line, control_arrow),
            FadeIn(control_label),
            run_time=max(0.05, 0.34),  # 15.60 -> 15.94
        )
        add_to_main(control_arrow)  # note: we add the arrow, not the label yet
        # keep control_label separate for now; we will fade it out in Beat 9

        self.play(
            Indicate(control_arrow, color=YELLOW, scale_factor=1.08),
            run_time=max(0.05, 0.44),  # 15.94 -> 16.38
        )

        # --------------------------------------------------------------
        # gap 16.38 -> 16.90
        self.wait(max(0.05, 0.52))

        # --------------------------------------------------------------
        # Beat 7: 16.90 - 18.32
        # --------------------------------------------------------------
        self.play(
            Indicate(robotic_arm, color=YELLOW, scale_factor=1.10),
            run_time=max(0.05, 0.20),  # 16.90 -> 17.10
        )

        self.play(
            control_arrow.animate.put_start_and_end_on(
                control_arrow.get_start(),
                robot_base.get_left(),
            ),
            arm_group.animate.rotate(0.18, about_point=base_top),
            run_time=max(0.05, 0.46),  # 17.10 -> 17.56
        )

        target_obj = Circle(
            radius=0.16,
            fill_color=PURPLE, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        ).move_to([5.65, -0.85, 0])
        self.play(
            FadeIn(target_obj),
            arm_group.animate.rotate(0.17, about_point=base_top),
            run_time=max(0.05, 0.76),  # 17.56 -> 18.32
        )
        add_to_main(target_obj)

        # --------------------------------------------------------------
        # gap 18.32 -> 19.34
        self.wait(max(0.05, 1.02))

        # --------------------------------------------------------------
        # Beat 8: 19.34 - 26.36
        # --------------------------------------------------------------
        self.wait(max(0.05, 1.00))  # 19.34 -> 20.34

        caption = Text("neural signal processing", font_size=24,
                       color=WHITE, weight=BOLD)
        caption.move_to([0, -3.45, 0])
        self.play(FadeIn(caption), run_time=max(0.05, 1.00))  # 20.34 -> 21.34
        add_to_main(caption)

        self.wait(max(0.05, 0.78))  # 21.34 -> 22.12

        # light wave travels through the pipeline
        path_points = [
            device.get_center(),
            cable.get_end(),
            waveform_subpanels.get_center(),
            input_nodes[0].get_center(),
            output_nodes[0].get_center(),
            control_arrow.get_start(),
            robot_base.get_center(),
        ]
        travel_path = VMobject().set_points_as_corners(path_points)
        wave_packet = Dot(path_points[0], radius=0.055,
                          color=YELLOW, fill_opacity=1)
        self.add(wave_packet)
        self.play(MoveAlongPath(wave_packet, travel_path), run_time=max(0.05, 1.54))  # 22.12 -> 23.66
        self.remove(wave_packet)

        nervous_highlight = VGroup(head, device)
        self.play(
            Indicate(nervous_highlight, color=YELLOW, scale_factor=1.15),
            run_time=max(0.05, 1.96),  # 23.66 -> 25.62
        )

        external_highlight = VGroup(robotic_arm, target_obj)
        self.play(
            Indicate(external_highlight, color=YELLOW, scale_factor=1.10),
            arm_group.animate.rotate(0.07, about_point=base_top),
            run_time=max(0.05, 0.74),  # 25.62 -> 26.36
        )

        # --------------------------------------------------------------
        # Beat 9: 26.36 - 27.18
        # --------------------------------------------------------------
        # 26.36 -> 26.46: fade out old control label
        self.play(FadeOut(control_label), run_time=max(0.05, 0.10))

        # create final labels
        label_recording = Text("recording", font_size=12, color=YELLOW)
        label_recording.next_to(head, LEFT, buff=0.12)

        label_spike_lfp = Text("spike or LFP analysis", font_size=12,
                               color=YELLOW)
        label_spike_lfp.next_to(waveform_subpanels, RIGHT, buff=0.12)
        label_spike_lfp.scale_to_fit_width(2.2)

        label_feature_extraction = Text("feature extraction",
                                        font_size=12, color=YELLOW)
        label_feature_extraction.next_to(feature_cards, UP, buff=0.12)

        label_movement_estimation = Text("movement estimation",
                                         font_size=12, color=YELLOW)
        label_movement_estimation.next_to(network_model, UP, buff=0.12)

        label_control = Text("control command", font_size=12, color=YELLOW)
        label_control.next_to(control_arrow, UP, buff=0.10)

        label_device_movement = Text("device movement", font_size=12,
                                     color=YELLOW)
        label_device_movement.next_to(robotic_arm, RIGHT, buff=0.12)

        labels_to_add = [
            label_recording,
            label_spike_lfp,
            label_feature_extraction,
            label_movement_estimation,
            label_control,
            label_device_movement,
        ]
        for lab in labels_to_add:
            add_to_main(lab)

        self.play(
            LaggedStart(*[FadeIn(lab) for lab in labels_to_add],
                        lag_ratio=0.8),
            run_time=max(0.05, 0.40),  # 26.46 -> 26.86
        )

        self.play(
            Indicate(self.main_scene, color=YELLOW, scale_factor=1.01),
            run_time=max(0.05, 0.18),  # 26.86 -> 27.04
        )

        self.play(FadeOut(self.main_scene), run_time=max(0.05, 0.14))  # 27.04 -> 27.18