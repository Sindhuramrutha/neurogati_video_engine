ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\ruler.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}


class Scene27(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- tiny reusable helpers ----------
        def make_headset(head, color=YELLOW):
            hs = VGroup()
            arc = Arc(radius=0.11, start_angle=0, angle=PI,
                      color=color, stroke_width=2.5)
            arc.move_to(head.get_center() + UP * 0.02)
            d1 = Dot(head.get_center() + LEFT * 0.09 + UP * 0.02,
                     radius=0.025, color=color)
            d2 = Dot(head.get_center() + RIGHT * 0.09 + UP * 0.02,
                     radius=0.025, color=color)
            hs.add(arc, d1, d2)
            return hs

        def make_seated_user_with_wheelchair(headset_color=YELLOW):
            user = VGroup()
            head = Circle(radius=0.1, color=WHITE, fill_opacity=1,
                          stroke_width=0).move_to(UP * 0.40)
            torso = Polygon(
                np.array([-0.11, 0.14, 0]),
                np.array([0.11, 0.14, 0]),
                np.array([0.10, -0.02, 0]),
                np.array([-0.12, -0.02, 0]),
                fill_color=WHITE, fill_opacity=1, stroke_width=0,
            )
            thigh = Rectangle(width=0.38, height=0.07,
                              fill_color=WHITE, fill_opacity=1,
                              stroke_width=0).move_to(RIGHT * 0.10 + DOWN * 0.21)
            shin = Rectangle(width=0.07, height=0.26,
                             fill_color=WHITE, fill_opacity=1,
                             stroke_width=0).move_to(RIGHT * 0.30 + DOWN * 0.41)
            arm = Rectangle(width=0.06, height=0.22,
                            fill_color=WHITE, fill_opacity=1,
                            stroke_width=0).move_to(LEFT * 0.01 + DOWN * 0.04)
            user.add(head, torso, thigh, shin, arm)

            wheel_rear = Circle(radius=0.18, fill_color=BLACK, fill_opacity=1,
                                stroke_color=WHITE,
                                stroke_width=2).move_to(LEFT * 0.20 + DOWN * 0.28)
            wheel_front = Circle(radius=0.09, fill_color=BLACK, fill_opacity=1,
                                 stroke_color=WHITE,
                                 stroke_width=2).move_to(RIGHT * 0.32 + DOWN * 0.39)
            seat = Rectangle(width=0.46, height=0.08, fill_color=BLUE,
                             fill_opacity=1, stroke_width=0).move_to(DOWN * 0.13)
            backrest = Rectangle(width=0.06, height=0.34, fill_color=BLUE,
                                 fill_opacity=1, stroke_width=0).move_to(
                LEFT * 0.20 + UP * 0.04)
            wheelchair = VGroup(wheel_rear, wheel_front, seat, backrest)

            headset = make_headset(head, headset_color)
            group = VGroup(user, wheelchair, headset)
            return group, {
                "head": head,
                "wheel_rear": wheel_rear,
                "wheel_front": wheel_front,
                "wheelchair": wheelchair,
                "user": user,
                "headset": headset,
            }

        def make_computer_monitor():
            body = Rectangle(width=0.66, height=0.48,
                             fill_color=GREY_B, fill_opacity=0.85,
                             stroke_color=WHITE, stroke_width=2)
            screen = Rectangle(width=0.54, height=0.36,
                               fill_color=BLACK, fill_opacity=1,
                               stroke_color=GREY_B, stroke_width=1)
            screen.move_to(body)
            stand = Rectangle(width=0.07, height=0.20,
                              fill_color=GREY_B, fill_opacity=0.85,
                              stroke_width=0).move_to(
                body.get_bottom() + DOWN * 0.10)
            base = Rectangle(width=0.38, height=0.06,
                             fill_color=GREY_B, fill_opacity=0.85,
                             stroke_width=0).move_to(
                stand.get_bottom() + DOWN * 0.03)
            return VGroup(body, screen, stand, base), screen

        def make_robot_arm():
            base = Rectangle(width=0.5, height=0.15,
                             fill_color=GREY_B, fill_opacity=0.9,
                             stroke_width=0).move_to(DOWN * 0.05)
            shoulder = Circle(radius=0.09, color=TEAL, fill_opacity=1,
                              stroke_color=WHITE,
                              stroke_width=2).move_to(UP * 0.12)

            upper = Rectangle(width=0.16, height=0.72,
                              fill_color=BLUE, fill_opacity=1,
                              stroke_color=WHITE, stroke_width=2)
            upper.move_to(shoulder.get_center() + UP * 0.36)
            upper.rotate(PI / 5, about_point=shoulder.get_center())

            elbow = Circle(radius=0.06, color=TEAL, fill_opacity=1,
                           stroke_color=WHITE,
                           stroke_width=2).move_to(upper.get_top())
            upper_group = VGroup(upper, elbow)

            forearm = Rectangle(width=0.14, height=0.58,
                                fill_color=PURPLE, fill_opacity=1,
                                stroke_color=WHITE, stroke_width=2)
            forearm.move_to(elbow.get_center() + UP * 0.29)
            forearm.rotate(-PI / 7, about_point=elbow.get_center())

            wrist = Circle(radius=0.045, color=TEAL, fill_opacity=1,
                           stroke_color=WHITE,
                           stroke_width=2).move_to(forearm.get_top())
            gripper_left = Polygon(
                UP * 0.05 + LEFT * 0.02,
                UP * 0.12 + LEFT * 0.08,
                DOWN * 0.02 + LEFT * 0.02,
                fill_color=GREEN, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ).move_to(wrist.get_center() + UP * 0.04 + LEFT * 0.05)
            gripper_right = Polygon(
                UP * 0.05 + RIGHT * 0.02,
                UP * 0.12 + RIGHT * 0.08,
                DOWN * 0.02 + RIGHT * 0.02,
                fill_color=GREEN, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1.5,
            ).move_to(wrist.get_center() + UP * 0.04 + RIGHT * 0.05)

            forearm_group = VGroup(forearm, wrist,
                                   gripper_left, gripper_right)
            arm_group = VGroup(base, shoulder, upper_group, forearm_group)
            return (arm_group, shoulder, upper_group, elbow,
                    forearm_group, gripper_left, gripper_right)

        # ---------- helper scenes ----------
        def make_panel1_scene():
            scene = VGroup()
            user_group, refs = make_seated_user_with_wheelchair()
            user_group.move_to(LEFT * 0.60 + DOWN * 0.08)
            computer, screen = make_computer_monitor()
            computer.move_to(RIGHT * 0.40 + UP * 0.08)
            scene.add(user_group, computer)

            head_top = refs["head"].get_center() + UP * 0.10 + RIGHT * 0.02
            screen_pt = screen.get_left() + np.array([0.02, 0.06, 0])
            signal_path = Line(head_top, screen_pt,
                               color=YELLOW, stroke_width=2.2, path_arc=-0.7)
            scene.add(signal_path)
            return scene, {"screen": screen, "signal_path": signal_path}

        def make_panel2_scene():
            scene = VGroup()
            user_group, refs = make_seated_user_with_wheelchair()
            user_group.move_to(LEFT * 0.60 + DOWN * 0.08)

            motor = Rectangle(width=0.18, height=0.14,
                              fill_color=ORANGE, fill_opacity=1,
                              stroke_color=WHITE, stroke_width=1)
            motor.move_to(refs["wheelchair"].get_center()
                          + RIGHT * 0.15 + DOWN * 0.18)
            user_group.add(motor)

            head_center = refs["head"].get_center()
            signal_path = Line(
                head_center + UP * 0.08,
                motor.get_center() + UP * 0.12,
                color=YELLOW, stroke_width=2.2,
            )
            moving_group = VGroup(user_group, signal_path)
            scene.add(moving_group)
            return scene, {
                "moving_group": moving_group,
                "wheel_rear": refs["wheel_rear"],
                "wheel_front": refs["wheel_front"],
                "signal_path": signal_path,
                "head": refs["head"],
                "motor": motor,
            }

        def make_panel3_scene():
            scene = VGroup()
            table = Rectangle(width=1.6, height=0.10,
                              fill_color=GREY_B, fill_opacity=0.85,
                              stroke_width=0).move_to(DOWN * 0.40)
            scene.add(table)

            person_group, person_refs = make_seated_user_with_wheelchair()
            person_group.move_to(LEFT * 0.75 + DOWN * 0.10)
            scene.add(person_group)

            (arm_group, shoulder, upper_group, elbow,
             forearm_group, g_left, g_right) = make_robot_arm()
            arm_group.move_to(RIGHT * 0.30 + DOWN * 0.32)
            scene.add(arm_group)

            target_obj = Circle(radius=0.07, color=ORANGE, fill_opacity=1,
                                stroke_color=WHITE,
                                stroke_width=1.5).move_to(
                g_right.get_center() + RIGHT * 0.14 + DOWN * 0.02)
            scene.add(target_obj)

            signal_path = Line(
                person_refs["head"].get_center() + UP * 0.08,
                shoulder.get_center() + UP * 0.12,
                color=YELLOW, stroke_width=2.2, path_arc=-0.5,
            )
            scene.add(signal_path)
            return scene, {
                "shoulder": shoulder,
                "upper_group": upper_group,
                "elbow": elbow,
                "forearm_group": forearm_group,
                "g_left": g_left,
                "g_right": g_right,
                "target_obj": target_obj,
                "signal_path": signal_path,
            }

        def make_panel4_scene():
            scene = VGroup()
            bed = Rectangle(width=1.6, height=0.16,
                            fill_color=GREY_B, fill_opacity=0.8,
                            stroke_color=WHITE,
                            stroke_width=1).move_to(DOWN * 0.15)
            scene.add(bed)

            head = Circle(radius=0.11, color=WHITE, fill_opacity=1,
                          stroke_width=0).move_to(LEFT * 0.55 + UP * 0.30)
            body = Rectangle(width=0.85, height=0.22,
                             fill_color=WHITE, fill_opacity=1,
                             stroke_width=0).move_to(RIGHT * 0.05 + UP * 0.30)
            patient_arm = Rectangle(width=0.45, height=0.08,
                                    fill_color=WHITE, fill_opacity=1,
                                    stroke_width=0).move_to(
                RIGHT * 0.42 + UP * 0.34)
            headset = make_headset(head)
            patient = VGroup(head, body, patient_arm, headset)
            scene.add(patient)

            display, display_screen = make_computer_monitor()
            display.move_to(RIGHT * 0.55 + UP * 0.10)
            scene.add(display)

            feedback_bar = Rectangle(width=0.10, height=0.15,
                                     fill_color=YELLOW, fill_opacity=1,
                                     stroke_width=0).move_to(
                display_screen.get_center() + LEFT * 0.15)
            scene.add(feedback_bar)

            signal_line = Line(
                head.get_center() + UP * 0.08,
                display_screen.get_left() + UP * 0.05,
                color=YELLOW, stroke_width=2.2, path_arc=-0.5,
            )
            scene.add(signal_line)
            return scene, {
                "patient_arm": patient_arm,
                "display_screen": display_screen,
                "feedback_bar": feedback_bar,
                "signal_line": signal_line,
                "head": head,
            }

        def make_panel5_scene():
            scene = VGroup()
            head = Circle(radius=0.12, color=WHITE, fill_opacity=1,
                          stroke_width=0).move_to(UP * 0.55)
            body = RoundedRectangle(width=0.24, height=0.5, corner_radius=0.08,
                                    fill_color=WHITE, fill_opacity=1,
                                    stroke_width=0).move_to(UP * 0.15)
            leg1 = Rectangle(width=0.07, height=0.30,
                             fill_color=WHITE, fill_opacity=1,
                             stroke_width=0).move_to(LEFT * 0.05 + DOWN * 0.36)
            leg2 = Rectangle(width=0.07, height=0.30,
                             fill_color=WHITE, fill_opacity=1,
                             stroke_width=0).move_to(RIGHT * 0.08 + DOWN * 0.36)
            headset = make_headset(head)
            person = VGroup(head, body, leg1, leg2, headset)
            person.move_to(LEFT * 0.55)
            scene.add(person)

            computer, screen = make_computer_monitor()
            computer.move_to(RIGHT * 0.40 + UP * 0.10)
            scene.add(computer)

            two_way_arrow = DoubleArrow(
                head.get_center() + RIGHT * 0.14,
                screen.get_left() + LEFT * 0.08,
                color=YELLOW, stroke_width=4, buff=0.08,
                max_tip_length_to_length_ratio=0.20,
            )
            scene.add(two_way_arrow)
            return scene, {
                "head": head,
                "screen": screen,
                "two_way_arrow": two_way_arrow,
            }

        # ---------- Beat 1: five empty panels fade in sequentially ----------
        panel_labels = [
            "Assistive Communication",
            "Wheelchair Control",
            "Prosthetic Device Control",
            "Neurorehabilitation",
            "Research and HCI",
        ]
        panel_colors = [BLUE, TEAL, PURPLE, ORANGE, PINK]
        xs = [-5.3, -2.65, 0.0, 2.65, 5.3]

        panel_rects = []
        panel_texts = []
        panel_groups = []
        for i, label in enumerate(panel_labels):
            rect = Rectangle(
                width=2.35, height=3.0,
                fill_color=GREY_B, fill_opacity=0.06,
                stroke_color=GREY_B, stroke_width=2.5,
            )
            rect.move_to(np.array([xs[i], 0.4, 0]))
            lab = Text(label, font_size=15, weight="BOLD", color=GREY_B)
            lab.scale_to_fit_width(2.25)
            lab.next_to(rect, DOWN, buff=0.12)
            group = VGroup(rect, lab)
            panel_rects.append(rect)
            panel_texts.append(lab)
            panel_groups.append(group)

        per_item = 4.06 / len(panel_groups)
        for group in panel_groups:
            self.play(FadeIn(group), run_time=max(0.05, per_item * 0.8))
            self.wait(max(0.05, per_item * 0.2))

        # ---------- Gap before Beat 2 ----------
        self.wait(max(0.05, 0.90))

        # ---------- Beat 2: Assistive Communication panel ----------
        p1_scene, p1_refs = make_panel1_scene()
        p1_scene.scale_to_fit_width(1.9)
        p1_scene.scale_to_fit_height(2.3)
        p1_scene.scale(1.05)
        p1_scene.move_to(panel_rects[0].get_center())

        self.play(
            FadeIn(p1_scene),
            panel_rects[0].animate.set_stroke(BLUE, width=4)
                           .set_fill(BLUE, opacity=0.22)
                           .scale(1.05),
            panel_texts[0].animate.set_color(WHITE),
            run_time=max(0.05, 0.68),
        )

        # ---------- Gap before Beat 3 ----------
        self.wait(max(0.05, 1.16))

        # ---------- Beat 3: spelled-out communication ----------
        screen_center = p1_refs["screen"].get_center()
        signal_path = p1_refs["signal_path"]
        letters = "HELLO"
        per_letter = 5.26 / len(letters)

        for i, letter in enumerate(letters):
            char = Text(letter, font_size=12, color=GREEN, weight="BOLD")
            char.move_to(screen_center + np.array([-0.16 + i * 0.08, 0, 0]))
            self.play(Write(char),
                      run_time=max(0.05, per_letter * 0.45))
            self.play(signal_path.animate.set_stroke(YELLOW, width=5),
                      run_time=max(0.05, per_letter * 0.25))
            self.play(signal_path.animate.set_stroke(WHITE, width=2.2),
                      run_time=max(0.05, per_letter * 0.15))
            self.wait(max(0.05, per_letter * 0.15))

        # ---------- Gap before Beat 4 ----------
        self.wait(max(0.05, 0.96))

        # ---------- Beat 4: Wheelchair Control panel ----------
        p2_scene, p2_refs = make_panel2_scene()
        p2_scene.scale_to_fit_width(1.9)
        p2_scene.scale_to_fit_height(2.3)
        p2_scene.scale(1.05)
        p2_scene.move_to(panel_rects[1].get_center())

        self.play(
            FadeIn(p2_scene),
            panel_rects[1].animate.set_stroke(TEAL, width=4)
                           .set_fill(TEAL, opacity=0.22)
                           .scale(1.05),
            panel_texts[1].animate.set_color(WHITE),
            run_time=max(0.05, 0.52),
        )

        # ---------- Gap before Beat 5 ----------
        self.wait(max(0.05, 0.76))

        # ---------- Beat 5: wheelchair movement and command ----------
        moving_group = p2_refs["moving_group"]
        wheel_rear = p2_refs["wheel_rear"]
        wheel_front = p2_refs["wheel_front"]
        p2_signal = p2_refs["signal_path"]
        p2_head = p2_refs["head"]
        p2_motor = p2_refs["motor"]

        self.play(p2_signal.animate.set_stroke(YELLOW, width=5), run_time=max(0.05, 0.25))
        self.play(p2_signal.animate.set_stroke(WHITE, width=2.2), run_time=max(0.05, 0.25))

        self.play(
            moving_group.animate.shift(RIGHT * 0.72),
            wheel_rear.animate.rotate(-2.4,
                                      about_point=wheel_rear.get_center()),
            wheel_front.animate.rotate(-2.4,
                                       about_point=wheel_front.get_center()),
            run_time=max(0.05, 1.7),
        )

        command_arrow = Arrow(
            p2_head.get_center() + DOWN * 0.10,
            p2_motor.get_center() + UP * 0.05,
            color=YELLOW, stroke_width=3, buff=0.05,
        )
        self.play(Create(command_arrow), run_time=max(0.05, 0.5))
        self.play(Indicate(command_arrow, color=YELLOW), run_time=max(0.05, 0.44))
        self.wait(max(0.05, 0.40))

        # ---------- Gap before Beat 6 ----------
        self.wait(max(0.05, 0.96))

        # ---------- Beat 6: Prosthetic Device Control panel ----------
        p3_scene, p3_refs = make_panel3_scene()
        p3_scene.scale_to_fit_width(1.9)
        p3_scene.scale_to_fit_height(2.3)
        p3_scene.scale(1.05)
        p3_scene.move_to(panel_rects[2].get_center())

        self.play(
            FadeIn(p3_scene),
            panel_rects[2].animate.set_stroke(PURPLE, width=4)
                           .set_fill(PURPLE, opacity=0.22)
                           .scale(1.05),
            panel_texts[2].animate.set_color(WHITE),
            run_time=max(0.05, 1.08),
        )

        # ---------- Gap before Beat 7 ----------
        self.wait(max(0.05, 0.62))

        # ---------- Beat 7: robotic arm movement ----------
        shoulder = p3_refs["shoulder"]
        upper_group = p3_refs["upper_group"]
        elbow = p3_refs["elbow"]
        forearm_group = p3_refs["forearm_group"]
        g_left = p3_refs["g_left"]
        g_right = p3_refs["g_right"]
        target_obj = p3_refs["target_obj"]
        p3_signal = p3_refs["signal_path"]

        self.play(
            upper_group.animate.rotate(-0.55,
                                       about_point=shoulder.get_center()),
            run_time=max(0.05, 1.1),
        )
        self.play(
            forearm_group.animate.rotate(0.8,
                                         about_point=elbow.get_center()),
            run_time=max(0.05, 0.7),
        )
        self.play(p3_signal.animate.set_stroke(YELLOW, width=5), run_time=max(0.05, 0.3))
        self.play(p3_signal.animate.set_stroke(WHITE, width=2.2), run_time=max(0.05, 0.3))

        self.play(g_left.animate.shift(LEFT * 0.06),
                  g_right.animate.shift(RIGHT * 0.06), run_time=max(0.05, 0.5))
        self.play(
            g_left.animate.shift(RIGHT * 0.06),
            g_right.animate.shift(LEFT * 0.06),
            target_obj.animate.move_to(g_right.get_center()
                                       + RIGHT * 0.03 + DOWN * 0.02),
            run_time=max(0.05, 0.7),
        )
        self.wait(max(0.05, 0.48))

        # ---------- Gap before Beat 8 ----------
        self.wait(max(0.05, 1.32))

        # ---------- Beat 8: Neurorehabilitation panel ----------
        p4_scene, p4_refs = make_panel4_scene()
        p4_scene.scale_to_fit_width(1.9)
        p4_scene.scale_to_fit_height(2.3)
        p4_scene.scale(1.05)
        p4_scene.move_to(panel_rects[3].get_center())

        self.play(
            FadeIn(p4_scene),
            panel_rects[3].animate.set_stroke(ORANGE, width=4)
                           .set_fill(ORANGE, opacity=0.22)
                           .scale(1.05),
            panel_texts[3].animate.set_color(WHITE),
            run_time=max(0.05, 0.50),
        )

        # ---------- Gap before Beat 9 ----------
        self.wait(max(0.05, 1.00))

        # ---------- Beat 9: closed-loop rehabilitation feedback ----------
        patient_arm = p4_refs["patient_arm"]
        display_screen = p4_refs["display_screen"]
        feedback_bar = p4_refs["feedback_bar"]
        p4_signal = p4_refs["signal_line"]

        per_cycle = 6.50 / 3
        for _ in range(3):
            self.play(
                feedback_bar.animate.stretch(1.35, dim=1),
                display_screen.animate.set_fill(BLUE, opacity=0.5),
                run_time=max(0.05, per_cycle * 0.22),
            )
            self.play(
                feedback_bar.animate.stretch(1 / 1.35, dim=1),
                display_screen.animate.set_fill(BLACK, opacity=1),
                run_time=max(0.05, per_cycle * 0.18),
            )
            self.play(
                patient_arm.animate.rotate(PI / 14,
                                           about_point=patient_arm.get_left()),
                run_time=max(0.05, per_cycle * 0.18),
            )
            self.play(
                patient_arm.animate.rotate(-PI / 14,
                                           about_point=patient_arm.get_left()),
                run_time=max(0.05, per_cycle * 0.18),
            )
            self.play(p4_signal.animate.set_stroke(YELLOW, width=5),
                      run_time=max(0.05, per_cycle * 0.12))
            self.play(p4_signal.animate.set_stroke(WHITE, width=2.2),
                      run_time=max(0.05, per_cycle * 0.12))

        # ---------- Gap before Beat 10 ----------
        self.wait(max(0.05, 0.70))

        # ---------- Beat 10: Research and HCI panel ----------
        p5_scene, p5_refs = make_panel5_scene()
        p5_scene.scale_to_fit_width(1.9)
        p5_scene.scale_to_fit_height(2.3)
        p5_scene.scale(1.05)
        p5_scene.move_to(panel_rects[4].get_center())

        self.play(
            FadeIn(p5_scene),
            panel_rects[4].animate.set_stroke(PINK, width=4)
                           .set_fill(PINK, opacity=0.22)
                           .scale(1.05),
            panel_texts[4].animate.set_color(WHITE),
            run_time=max(0.05, 2.14),
        )

        # ---------- Gap before Beat 11 ----------
        self.wait(max(0.05, 0.68))

        # ---------- Beat 11: cognition shapes and interaction network ----------
        screen = p5_refs["screen"]
        head = p5_refs["head"]
        two_way_arrow = p5_refs["two_way_arrow"]

        self.play(Indicate(two_way_arrow, color=YELLOW, scale_factor=1.15),
                  run_time=max(0.05, 0.6))

        brain_icon = SVGMobject(ASSET_PATHS["brain"]).set_color(WHITE)
        brain_icon.scale_to_fit_height(0.24)
        brain_icon.move_to(screen.get_center() + UP * 0.08)

        square = Square(side_length=0.10, fill_color=GREEN, fill_opacity=1,
                        stroke_width=0)
        square.move_to(screen.get_center() + LEFT * 0.15 + DOWN * 0.08)
        circle = Circle(radius=0.05, color=BLUE, fill_opacity=1,
                        stroke_width=0)
        circle.move_to(screen.get_center() + RIGHT * 0.16 + DOWN * 0.06)
        triangle = Polygon(
            UP * 0.06, LEFT * 0.06 + DOWN * 0.05, RIGHT * 0.06 + DOWN * 0.05,
            fill_color=ORANGE, fill_opacity=1, stroke_width=0,
        )
        triangle.move_to(screen.get_center() + RIGHT * 0.08 + UP * 0.10)
        geometric_shapes = VGroup(square, circle, triangle)

        self.play(FadeIn(brain_icon), run_time=max(0.05, 0.6))
        self.play(FadeIn(geometric_shapes), run_time=max(0.05, 0.6))

        self.play(FadeOut(two_way_arrow), run_time=max(0.05, 0.30))

        screen_points = [
            screen.get_left() + UP * 0.16,
            screen.get_left() + DOWN * 0.10,
            screen.get_left() + UP * 0.03,
            screen.get_left() + DOWN * 0.18,
            screen.get_left() + UP * 0.28,
            screen.get_left() + DOWN * 0.24,
            screen.get_left() + UP * 0.10,
        ]
        head_anchor = head.get_center() + RIGHT * 0.12 + UP * 0.05
        network_lines = VGroup(*[
            Line(head_anchor, pt, color=WHITE, stroke_width=1.2)
            for pt in screen_points
        ])
        network_nodes = VGroup(*[
            Dot(line.get_center(), radius=0.025, color=YELLOW)
            for line in network_lines
        ])

        for line, node in zip(network_lines, network_nodes):
            self.play(Create(line), run_time=max(0.05, 0.5))
            self.play(FadeIn(node), run_time=max(0.05, 0.2))
            self.wait(max(0.05, 0.14))

        # ---------- Final hold through 46.30 ----------
        self.wait(max(0.05, 0.90))