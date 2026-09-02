ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

ASSET_PATHS = {
    "heart": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\test_heart.svg",
    "brain": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\brain_test.svg",
    "stopwatch": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\stopwatch.svg",
    "activity": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\activity.svg",
    "soundwave": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\soundwave.svg",
    "grid_matrix": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\grid-3x3-gap-fill.svg",
    "bar_chart": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\bar-chart.svg",
    "graph_trend": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\graph-up-arrow.svg",
    "cpu": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\cpu.svg",
    "funnel": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\funnel.svg",
    "table": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\table.svg",
    "hospital": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\hospital.svg",
    "capsule": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\capsule.svg",
    "clipboard_pulse": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\clipboard2-pulse.svg",
    "hand": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\hand-index-thumb.svg",
    "broadcast": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\broadcast-pin.svg",
    "gear": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\gear.svg",
    "arrow_repeat": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\arrow-repeat.svg",
    "lightbulb": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\lightbulb.svg",
    "bell": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\bell.svg",
    "check_circle": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\check-circle.svg",
    "x_circle": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\x-circle.svg",
    "rulers": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\rulers.svg",
    "puzzle": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\puzzle.svg",
    "fig_measurement_funnel": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\fig_measurement_funnel.png",
    "fig_mindmap_three_pillars": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\fig_mindmap_three_pillars.png",
    "fig_mindmap_full": r"C:\Users\DELL\Desktop\neurogati_video_engine\assets\image\fig_mindmap_full.png",
}


class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        x_event = 0.0

        def wave_y(t):
            return (
                0.45 * np.sin(4.5 * t)
                + 0.22 * np.sin(11.0 * t)
                + 0.13 * np.sin(23.0 * t)
                + 0.07 * np.sin(41.0 * t)
            )

        def avg_y(x):
            return (
                0.55 * np.exp(-((x - 0.15) ** 2) / 0.30)
                - 0.30 * np.exp(-((x - 0.45) ** 2) / 0.18)
                + 0.18 * np.exp(-((x - 0.80) ** 2) / 0.40)
            )

        clock = 0.0

        def P(dur, *anims):
            nonlocal clock
            if dur <= 0:
                return
            self.play(*anims, run_time=max(0.05, dur))
            clock += dur

        def W(dur):
            nonlocal clock
            if dur <= 0:
                return
            self.wait(max(0.05, dur))
            clock += dur

        # --------------------------------
        # Beat 1: single continuous EEG trace
        # --------------------------------
        trace = VMobject(color=TEAL, stroke_width=2.5)
        trace.set_points_smoothly(
            [np.array([x, wave_y(x), 0]) for x in np.linspace(-6.6, 6.6, 600)]
        )

        P(0.94, FadeIn(trace))

        # --------------------------------
        # Beat 2: event marker drops on trace
        # --------------------------------
        event_vline = DashedLine(
            start=np.array([x_event, 1.6, 0]),
            end=np.array([x_event, -1.6, 0]),
            color=GREY_B,
            stroke_width=3,
        ).shift(UP * 2)

        event_label = Text("event", font_size=28, color=WHITE)
        event_label.move_to([x_event + 0.6, 2.1, 0])

        P(0.60, event_vline.animate.shift(DOWN * 2))
        P(0.30, FadeIn(event_label))
        W(0.28)
        P(0.30, FadeOut(event_label))

        # --------------------------------
        # Beat 3: glowing band around event window
        # --------------------------------
        band = Rectangle(
            width=4.2,
            height=1.8,
            color=YELLOW,
            stroke_width=2,
            fill_color=YELLOW,
            fill_opacity=0.12,
        ).move_to([x_event, 0, 0])
        band.stretch_to_fit_width(0.08)

        electrical_resp_label = Text("electrical response", font_size=30, color=YELLOW)
        electrical_resp_label.move_to([x_event, -1.5, 0])

        P(0.90, band.animate.stretch_to_fit_width(4.2), trace.animate.set_opacity(0.45))
        P(0.35, FadeIn(electrical_resp_label))
        W(0.57)

        # --------------------------------
        # Beat 4: brighten / time-locked
        # --------------------------------
        inner_line = Line(
            start=[x_event, -0.7, 0],
            end=[x_event, 0.7, 0],
            color=GOLD,
            stroke_width=3,
        )
        time_locked_label = Text("time-locked", font_size=30, color=GOLD)
        time_locked_label.move_to([x_event + 0.6, 1.2, 0])

        P(
            0.50,
            band.animate.set_fill(opacity=0.28).set_stroke(width=3),
            trace.animate.set_opacity(0.40),
            FadeIn(inner_line),
        )
        P(0.30, FadeIn(time_locked_label))
        W(0.36)
        P(0.30, FadeOut(time_locked_label))

        # --------------------------------
        # Beat 5: event-type icons + specific-event text
        # --------------------------------
        eye_white = Ellipse(
            width=0.80, height=0.50, fill_color=WHITE, fill_opacity=1, stroke_width=0
        )
        eye_pupil = Circle(radius=0.14, fill_color=BLUE, fill_opacity=1, stroke_width=0)
        eye_icon = VGroup(eye_white, eye_pupil)
        eye_icon.scale_to_fit_height(0.55)

        speaker_cone = Polygon(
            [-0.25, 0.15, 0],
            [0.05, 0.20, 0],
            [0.20, 0.45, 0],
            [0.20, -0.45, 0],
            [0.05, -0.20, 0],
            [-0.25, -0.15, 0],
            fill_color=BLUE,
            fill_opacity=1,
            stroke_width=0,
        )
        speaker_box = Rectangle(
            width=0.14, height=0.40, fill_color=BLUE, fill_opacity=1, stroke_width=0
        ).move_to([-0.12, 0, 0])
        speaker_icon = VGroup(speaker_cone, speaker_box)
        speaker_icon.scale_to_fit_height(0.55)

        hand_icon = SVGMobject(ASSET_PATHS["hand"])
        hand_icon.set_fill(ORANGE, opacity=1)
        hand_icon.set_stroke(width=0)
        hand_icon.scale_to_fit_height(0.55)

        figure_head = Circle(
            radius=0.11, fill_color=PINK, fill_opacity=1, stroke_width=0
        ).move_to([0, 0.28, 0])
        figure_body = Polygon(
            [-0.13, 0.0, 0],
            [0.13, 0.0, 0],
            [0.07, -0.38, 0],
            [-0.07, -0.38, 0],
            fill_color=PINK,
            fill_opacity=1,
            stroke_width=0,
        )
        figure_arm_left = Rectangle(
            width=0.06, height=0.22, fill_color=PINK, fill_opacity=1, stroke_width=0
        ).move_to([-0.22, -0.12, 0]).rotate(0.8)
        figure_arm_right = Rectangle(
            width=0.06, height=0.22, fill_color=PINK, fill_opacity=1, stroke_width=0
        ).move_to([0.22, -0.12, 0]).rotate(-0.8)
        figure_leg_left = Rectangle(
            width=0.06, height=0.28, fill_color=PINK, fill_opacity=1, stroke_width=0
        ).move_to([-0.06, -0.50, 0]).rotate(0.2)
        figure_leg_right = Rectangle(
            width=0.06, height=0.28, fill_color=PINK, fill_opacity=1, stroke_width=0
        ).move_to([0.06, -0.50, 0]).rotate(-0.2)
        figure_icon = VGroup(
            figure_head,
            figure_body,
            figure_arm_left,
            figure_arm_right,
            figure_leg_left,
            figure_leg_right,
        )
        figure_icon.scale_to_fit_height(0.55)

        specific_event_text = Text(
            "specific sensory, cognitive, or motor event",
            font_size=26,
            color=WHITE,
        )
        specific_event_text.scale_to_fit_width(12)
        specific_event_text.move_to([0, 1.0, 0])

        P(0.25, FadeIn(specific_event_text))

        for icon in [eye_icon, speaker_icon, hand_icon, figure_icon]:
            icon.move_to([x_event, 2.5, 0])
            P(0.12, FadeIn(icon))
            W(0.07)
            P(0.10, FadeOut(icon))
            W(0.02)

        P(0.12, FadeOut(specific_event_text))
        W(0.11)

        # Gap to beat 6
        W(0.86)

        # --------------------------------
        # Beat 6: dim outside trace / pulse highlight
        # --------------------------------
        focus_text = Text(
            "focuses on neural activity immediately before and after",
            font_size=28,
            color=WHITE,
        )
        focus_text.scale_to_fit_width(12)
        focus_text.move_to([0, -3.0, 0])

        P(
            0.80,
            trace.animate.set_opacity(0.20),
            band.animate.set_fill(opacity=0.32).set_stroke(width=4),
            FadeOut(electrical_resp_label),
        )
        P(0.50, FadeIn(focus_text))

        P(0.50, band.animate.set_fill(opacity=0.42).set_stroke(width=5))
        P(0.50, band.animate.set_fill(opacity=0.25).set_stroke(width=4))
        P(0.50, band.animate.set_fill(opacity=0.42).set_stroke(width=5))
        P(0.50, band.animate.set_fill(opacity=0.25).set_stroke(width=4))
        W(0.82)

        # --------------------------------
        # Beat 7: brighter window, glowing marker, before/after
        # --------------------------------
        before_text = Text("before", font_size=30, color=WHITE)
        before_text.move_to([x_event - 1.5, -1.5, 0])

        after_text = Text("after", font_size=30, color=WHITE)
        after_text.move_to([x_event + 1.5, -1.5, 0])

        particular_text = Text("a particular event", font_size=26, color=WHITE)
        particular_text.scale_to_fit_width(7)
        particular_text.move_to([0, -2.05, 0])

        P(
            0.70,
            trace.animate.set_opacity(0.10),
            band.animate.set_fill(opacity=0.45).set_stroke(width=5),
            FadeOut(focus_text),
        )
        P(0.50, event_vline.animate.set_color(GOLD).set_stroke(width=6, opacity=1))
        P(0.40, event_vline.animate.set_color(GREY_B).set_stroke(width=3))
        P(0.40, FadeIn(before_text), FadeIn(after_text))
        P(0.40, FadeIn(particular_text))
        W(1.78)

        # Gap to beat 8
        W(0.72)

        # --------------------------------
        # Beat 8: icons with labels, in succession
        # --------------------------------
        visual_cap = Text("visual image", font_size=22, color=WHITE)
        visual_cap.move_to([x_event, 1.85, 0])

        auditory_cap = Text("auditory tone", font_size=22, color=WHITE)
        auditory_cap.move_to([x_event, 1.85, 0])

        tactile_cap = Text("tactile stimulus", font_size=22, color=WHITE)
        tactile_cap.move_to([x_event, 1.85, 0])

        movement_cap = Text("movement", font_size=22, color=WHITE)
        movement_cap.move_to([x_event, 1.85, 0])

        beat8_items = [
            (eye_icon, visual_cap),
            (speaker_icon, auditory_cap),
            (hand_icon, tactile_cap),
            (figure_icon, movement_cap),
        ]

        for icon, cap in beat8_items:
            icon.move_to([x_event, 2.5, 0])

        for icon, cap in beat8_items:
            P(0.20, FadeIn(icon), FadeIn(cap))
            W(0.15)
            P(0.15, FadeOut(icon), FadeOut(cap))
            W(0.10)

        W(0.14)

        # Gap to beat 9
        W(0.66)

        # --------------------------------
        # Beat 9: auditory tone + small sinusoidal event
        # --------------------------------
        auditory_wave = VMobject(color=BLUE, stroke_width=2.5)
        auditory_wave.set_points_smoothly(
            [np.array([x, 0.25 * np.sin(10 * x), 0]) for x in np.linspace(-1.2, 1.2, 120)]
        )

        speaker_icon.move_to([x_event, 2.5, 0])
        auditory_cap.move_to([x_event, 1.85, 0])

        P(0.25, FadeIn(speaker_icon), FadeIn(auditory_cap))
        P(0.80, Create(auditory_wave))
        W(0.51)

        # --------------------------------
        # Beat 10: hand, figure, eye appear; speaker then fades
        # --------------------------------
        sp_x = -2.3
        hand_x = -0.8
        fig_x = 0.8
        eye_x = 2.3

        hand_icon.move_to([hand_x, 2.5, 0])
        figure_icon.move_to([fig_x, 2.5, 0])
        eye_icon.move_to([eye_x, 2.5, 0])

        tactile_cap.move_to([hand_x, 1.85, 0])
        movement_cap.move_to([fig_x, 1.85, 0])
        visual_cap.move_to([eye_x, 1.85, 0])

        P(
            0.30,
            speaker_icon.animate.move_to([sp_x, 2.5, 0]),
            auditory_cap.animate.move_to([sp_x, 1.85, 0]),
        )
        P(0.45, FadeIn(hand_icon), FadeIn(tactile_cap))
        W(0.25)
        P(0.45, FadeIn(figure_icon), FadeIn(movement_cap))
        W(0.25)
        P(0.45, FadeIn(eye_icon), FadeIn(visual_cap))
        W(0.25)
        P(0.30, FadeOut(speaker_icon), FadeOut(auditory_cap))
        W(0.62)

        # Gap to beat 11
        W(0.52)

        # --------------------------------
        # Beat 11: brain icon / cognitive decision
        # --------------------------------
        brain_icon = SVGMobject(ASSET_PATHS["brain"])
        brain_icon.set_fill(PURPLE, opacity=1)
        brain_icon.set_stroke(width=0)
        brain_icon.scale_to_fit_height(0.55)
        brain_icon.move_to([0, 2.5, 0])

        brain_label = Text("cognitive decision", font_size=22, color=WHITE)
        brain_label.move_to([0, 1.85, 0])

        P(0.40, FadeIn(brain_icon), FadeIn(brain_label))
        W(0.30)
        P(
            0.48,
            FadeOut(hand_icon),
            FadeOut(figure_icon),
            FadeOut(eye_icon),
            FadeOut(tactile_cap),
            FadeOut(movement_cap),
            FadeOut(visual_cap),
            FadeOut(brain_icon),
            FadeOut(brain_label),
            FadeOut(auditory_wave),
        )

        # Gap to beat 12
        W(0.82)

        # --------------------------------
        # Beat 12: focus only on highlighted window
        # --------------------------------
        respond_text = Text(
            "how the brain responds to that specific event",
            font_size=28,
            color=WHITE,
        )
        respond_text.scale_to_fit_width(12)
        respond_text.move_to([0, -3.0, 0])

        respond_arrow = Arrow(
            start=respond_text.get_top() + UP * 0.15,
            end=np.array([x_event, band.get_bottom()[1] - 0.10, 0]),
            color=WHITE,
            stroke_width=3,
        )

        P(
            0.80,
            trace.animate.set_opacity(0),
            band.animate.set_fill(opacity=0.50).set_stroke(width=5),
            FadeOut(before_text),
            FadeOut(after_text),
            FadeOut(particular_text),
        )
        P(0.60, FadeIn(respond_text), Create(respond_arrow))
        W(2.76)

        # Gap to beat 13
        W(0.68)

        # --------------------------------
        # Beat 13: full-width "entire recording" rectangle + crosshatch
        # --------------------------------
        full_rec = Rectangle(
            width=13.0,
            height=2.2,
            color=GREY,
            stroke_width=2,
            fill_color=GREY,
            fill_opacity=0.08,
        ).move_to([0, 0, 0])

        entire_rec_label = Text("entire recording", font_size=24, color=GREY_B)
        entire_rec_label.move_to([-4.2, 0.75, 0])

        hatch = VGroup()
        for x0 in np.arange(-6.4, -2.0, 0.45):
            hatch.add(
                Line(
                    [x0, -1.0, 0],
                    [x0 + 0.5, 1.0, 0],
                    color=GREY_B,
                    stroke_width=1,
                    stroke_opacity=0.40,
                )
            )
            hatch.add(
                Line(
                    [x0, 1.0, 0],
                    [x0 + 0.5, -1.0, 0],
                    color=GREY_B,
                    stroke_width=1,
                    stroke_opacity=0.25,
                )
            )
        for x0 in np.arange(2.0, 6.4, 0.45):
            hatch.add(
                Line(
                    [x0, -1.0, 0],
                    [x0 + 0.5, 1.0, 0],
                    color=GREY_B,
                    stroke_width=1,
                    stroke_opacity=0.40,
                )
            )
            hatch.add(
                Line(
                    [x0, 1.0, 0],
                    [x0 + 0.5, -1.0, 0],
                    color=GREY_B,
                    stroke_width=1,
                    stroke_opacity=0.25,
                )
            )

        P(
            0.80,
            FadeIn(full_rec),
            FadeIn(entire_rec_label),
            trace.animate.set_opacity(0.18),
            FadeIn(hatch),
        )
        P(0.40, band.animate.set_fill(opacity=0.45).set_stroke(width=5))
        W(1.00)

        # Gap to beat 14
        W(0.46)

        # --------------------------------
        # Beat 14: zoom-in extraction of the event window
        # --------------------------------
        extracted_panel = Rectangle(
            width=4.0,
            height=1.3,
            color=GOLD,
            stroke_width=3,
            fill_color=BLACK,
            fill_opacity=0.25,
        ).move_to([x_event, 2.4, 0])

        extracted_segment = VMobject(color=YELLOW, stroke_width=3)
        extracted_segment.set_points_smoothly(
            [
                np.array([x * 1.05, 2.4 + wave_y(x) * 0.55, 0])
                for x in np.linspace(-1.8, 1.8, 160)
            ]
        )

        segments_label = Text("segments", font_size=30, color=YELLOW)
        segments_label.move_to([0, 1.25, 0])

        P(0.80, FadeOut(band), FadeOut(inner_line))
        P(2.20, GrowFromCenter(extracted_panel), Create(extracted_segment))
        P(0.50, FadeIn(segments_label))
        W(1.96)

        # Gap to beat 15
        W(0.92)

        # --------------------------------
        # Beat 15: duplicate the extracted segment
        # --------------------------------
        copy_group = VGroup()
        for cx in [-4.2, -1.4, 1.4, 4.2]:
            seg_copy = extracted_segment.copy().scale(0.65).move_to([cx, 2.4, 0])
            copy_group.add(seg_copy)

        key_def_label = Text("key definition", font_size=34, color=GOLD)
        key_def_label.scale_to_fit_width(5)
        key_def_label.move_to([0, 3.35, 0])

        P(0.50, FadeOut(extracted_panel), FadeIn(copy_group))
        P(0.40, FadeIn(key_def_label))
        W(0.54)

        # Gap to beat 16
        W(0.58)

        # --------------------------------
        # Beat 16: duplicated segments become averaged waveform
        # --------------------------------
        all_segment_copies = VGroup(extracted_segment, copy_group)

        avg_wave = VMobject(color=YELLOW, stroke_width=4)
        avg_wave.set_points_smoothly(
            [
                np.array([x, 1.0 + avg_y(x) * 0.65, 0])
                for x in np.linspace(-2.0, 2.0, 200)
            ]
        )

        avg_response_label = Text(
            "averaged electrical response", font_size=30, color=WHITE
        )
        avg_response_label.scale_to_fit_width(12)
        avg_response_label.move_to([0, -0.7, 0])

        P(
            0.80,
            FadeOut(all_segment_copies),
            FadeOut(key_def_label),
            FadeOut(segments_label),
            FadeOut(full_rec),
            FadeOut(entire_rec_label),
            FadeOut(hatch),
            FadeOut(respond_text),
            FadeOut(respond_arrow),
            FadeOut(trace),
        )
        P(1.20, Create(avg_wave))
        P(0.40, FadeIn(avg_response_label))
        W(0.92)

        # --------------------------------
        # Beat 17: final Event-Related Potential definition
        # --------------------------------
        erp_title = Text("Event-Related Potential", font_size=44, color=GOLD)
        erp_title.scale_to_fit_width(11)
        erp_title.move_to([0, -1.4, 0])

        erp_subtitle = Text(
            "time-locked to a specific event", font_size=26, color=WHITE
        )
        erp_subtitle.scale_to_fit_width(10)
        erp_subtitle.move_to([0, -2.1, 0])

        P(0.50, FadeOut(avg_response_label))
        P(0.80, FadeIn(erp_title))
        P(0.60, FadeIn(erp_subtitle))
        P(0.50, avg_wave.animate.set_stroke(width=6).set_color(GOLD))
        P(0.50, avg_wave.animate.set_stroke(width=4).set_color(YELLOW))
        W(max(0.05, 51.05 - clock))