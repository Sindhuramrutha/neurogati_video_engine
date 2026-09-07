ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *

class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        def wave_y(t):
            return 2.0 + 0.18 * np.sin(12 * t) + 0.07 * np.sin(35 * t)

        # ------------------------------------------------------------
        # Beat 1: continuous EEG timeline + dense waveform (0.00 - 2.76)
        # ------------------------------------------------------------
        timeline_line = Line([-6.5, 2.0, 0], [6.5, 2.0, 0], color=WHITE, stroke_width=2)

        wave = VMobject(color=TEAL, stroke_width=2.5)
        wave.set_points_smoothly([
            np.array([x, wave_y(x), 0])
            for x in np.linspace(-6.5, 6.5, 500)
        ])

        outside_group = VGroup(timeline_line, wave)

        self.play(FadeIn(timeline_line), run_time=max(0.05, 0.8))
        self.play(Create(wave), run_time=max(0.05, 1.4))
        self.wait(max(0.05, 2.76 - 0.8 - 1.4))  # 0.56

        # ------------------------------------------------------------
        # Beat 2: STFT label (2.76 - 4.82)
        # ------------------------------------------------------------
        stft_label = Text("Short-Time Fourier Transform", font_size=28, color=GOLD)
        stft_label.move_to([0, 3.3, 0])
        stft_label.scale_to_fit_width(6)

        self.play(FadeIn(stft_label), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 1.36))
        self.play(FadeOut(stft_label), run_time=max(0.05, 0.3))

        # ------------------------------------------------------------
        # Beat 3: Spectrograms / Wavelet analysis (4.82 - 6.48)
        # ------------------------------------------------------------
        spect_label = Text("Spectrograms", font_size=28, color=GOLD).move_to([0, 3.3, 0])
        wavelet_label = Text("Wavelet analysis", font_size=28, color=GOLD).move_to([0, 3.3, 0])

        self.play(FadeIn(spect_label), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.38))
        self.play(FadeOut(spect_label), run_time=max(0.05, 0.20))

        self.play(FadeIn(wavelet_label), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.38))
        self.play(FadeOut(wavelet_label), run_time=max(0.05, 0.20))

        # Gap: 6.48 -> 11.36
        self.wait(max(0.05, 4.88))

        # ------------------------------------------------------------
        # Beat 4: Continuous neural activity (11.36 - 12.30)
        # ------------------------------------------------------------
        cont_text = Text("Continuous neural activity", font_size=30, color=WHITE).move_to([0, 1.0, 0])
        cont_underline = Line(
            cont_text.get_left() + DOWN * 0.18,
            cont_text.get_right() + DOWN * 0.18,
            color=YELLOW,
            stroke_width=3,
        )
        cont_group = VGroup(cont_text, cont_underline)

        self.play(Write(cont_text), run_time=max(0.05, 0.3))
        self.play(Create(cont_underline), run_time=max(0.05, 0.2))
        self.play(wave.animate.set_color(GOLD).set_stroke(width=4), run_time=max(0.05, 0.44))

        # Gap: 12.30 -> 15.32
        self.wait(max(0.05, 3.02))

        # ------------------------------------------------------------
        # Beat 5: specific events + vertical dashed marker (15.32 - 18.66)
        # ------------------------------------------------------------
        x_event = -1.0

        dashed_event = DashedLine(
            start=[x_event, 3.4, 0],
            end=[x_event, 1.0, 0],
            color=GREY,
            stroke_width=3,
        ).shift(UP * 1.2)
        outside_group.add(dashed_event)

        specific_text = Text("specific events", font_size=30, color=GOLD).move_to([0, 1.0, 0])

        self.play(FadeOut(cont_group), run_time=max(0.05, 0.2))
        self.play(wave.animate.set_opacity(0.55), run_time=max(0.05, 0.4))
        self.play(dashed_event.animate.shift(DOWN * 1.2), run_time=max(0.05, 0.8))
        self.play(FadeIn(specific_text), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 1.34))
        self.play(FadeOut(specific_text), run_time=max(0.05, 0.3))

        # Gap: 18.66 -> 19.40
        self.wait(max(0.05, 0.74))

        # ------------------------------------------------------------
        # Beat 6: speaker icon + expanding sound ring (19.40 - 21.96)
        # ------------------------------------------------------------
        x_speaker = -3.3
        y_icon = 3.5

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
            width=0.14,
            height=0.40,
            fill_color=BLUE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to([-0.12, 0, 0])
        speaker = VGroup(speaker_cone, speaker_box)
        speaker.scale_to_fit_height(0.6)
        speaker.move_to([x_speaker, y_icon, 0])
        outside_group.add(speaker)

        self.play(GrowFromCenter(speaker), run_time=max(0.05, 0.4))

        ring = Circle(radius=0.55, color=BLUE, stroke_width=3).move_to(speaker.get_center())
        self.play(GrowFromCenter(ring), run_time=max(0.05, 0.35))
        self.play(ring.animate.scale(2.5).set_opacity(0), run_time=max(0.05, 0.55))

        sound_label = Text("Sound", font_size=24, color=WHITE).move_to([x_speaker, 2.8, 0])
        self.play(FadeIn(sound_label), run_time=max(0.05, 0.3))
        self.wait(max(0.05, 0.46))
        self.play(FadeOut(sound_label), run_time=max(0.05, 0.3))
        self.remove(ring)
        self.wait(max(0.05, 0.2))

        # Gap: 21.96 -> 22.40
        self.wait(max(0.05, 0.44))

        # ------------------------------------------------------------
        # Beat 7: eye/image icon (22.40 - 23.00)
        # ------------------------------------------------------------
        x_eye = x_event

        eye_white = Ellipse(width=0.8, height=0.5, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        eye_pupil = Circle(radius=0.14, fill_color=BLUE, fill_opacity=1, stroke_width=0)
        eye = VGroup(eye_white, eye_pupil).move_to([x_eye, y_icon, 0])
        outside_group.add(eye)

        self.play(GrowFromCenter(eye), run_time=max(0.05, 0.25))

        image_label = Text("Image", font_size=24, color=WHITE).move_to([x_eye + 0.6, 2.8, 0])
        self.play(FadeIn(image_label), run_time=max(0.05, 0.15))
        self.wait(max(0.05, 0.05))
        self.play(FadeOut(image_label), run_time=max(0.05, 0.15))

        # Gap: 23.00 -> 23.42
        self.wait(max(0.05, 0.42))

        # ------------------------------------------------------------
        # Beat 8: tactile hand icon (23.42 - 24.52)
        # ------------------------------------------------------------
        x_hand = 1.5

        hand = SVGMobject(ASSET_PATHS["hand"])
        hand.set_color(ORANGE)
        hand.set_fill(ORANGE, opacity=1)
        hand.set_stroke(width=0)
        hand.scale_to_fit_height(0.7)
        hand.move_to([x_hand, y_icon, 0])
        outside_group.add(hand)

        self.play(SpinInFromNothing(hand), run_time=max(0.05, 0.35))

        tactile_label = Text("Tactile stimulus", font_size=22, color=WHITE).move_to([x_hand, 2.8, 0])
        self.play(FadeIn(tactile_label), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 0.35))
        self.play(FadeOut(tactile_label), run_time=max(0.05, 0.2))

        # Gap: 24.52 -> 25.10
        self.wait(max(0.05, 0.58))

        # ------------------------------------------------------------
        # Beat 9: button press icon (25.10 - 27.18)
        # ------------------------------------------------------------
        x_button = 3.8

        button_base = RoundedRectangle(
            width=0.85,
            height=0.55,
            corner_radius=0.15,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=0,
        )
        button_top = RoundedRectangle(
            width=0.55,
            height=0.18,
            corner_radius=0.08,
            fill_color=TEAL,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(button_base.get_top() + DOWN * 0.10)
        button = VGroup(button_base, button_top).move_to([x_button, y_icon, 0])
        outside_group.add(button)

        self.play(GrowFromCenter(button), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.3))
        self.play(button.animate.scale(0.85).shift(DOWN * 0.08), run_time=max(0.05, 0.25))
        self.play(button.animate.scale(1 / 0.85).shift(UP * 0.08), run_time=max(0.05, 0.25))

        button_label = Text("Button press", font_size=24, color=WHITE).move_to([x_button, 2.8, 0])
        self.play(FadeIn(button_label), run_time=max(0.05, 0.2))
        self.wait(max(0.05, 0.53))
        self.play(FadeOut(button_label), run_time=max(0.05, 0.2))

        # Gap: 27.18 -> 27.94
        self.wait(max(0.05, 0.76))

        # ------------------------------------------------------------
        # Beat 10: connect icons, highlight post-event segments (27.94 - 33.64)
        # ------------------------------------------------------------
        connectors = VGroup()
        highlight_segments = VGroup()

        event_icons = [
            (speaker, x_speaker),
            (eye, x_eye),
            (hand, x_hand),
            (button, x_button),
        ]
        per_item = 5.70 / len(event_icons)

        for icon, x in event_icons:
            connector = Line(
                start=np.array([x, icon.get_bottom()[1] - 0.05, 0]),
                end=np.array([x, 2.2, 0]),
                color=GREY,
                stroke_width=1.5,
            )

            seg = VMobject(color=YELLOW, stroke_width=4, stroke_opacity=0.7)
            seg_pts = [np.array([t, wave_y(t), 0]) for t in np.linspace(x, x + 1.0, 80)]
            seg.set_points_smoothly(seg_pts)

            pulse = Dot(point=seg.get_start(), radius=0.06, color=ORANGE)

            self.play(Create(connector), run_time=max(0.05, 0.35))
            self.play(Create(seg), run_time=max(0.05, 0.25))
            self.add(pulse)
            self.play(MoveAlongPath(pulse, seg), run_time=max(0.05, 0.55))
            self.play(FadeOut(pulse), run_time=max(0.05, 0.15))
            self.remove(pulse)

            self.wait(max(0.05, per_item - (0.35 + 0.25 + 0.55 + 0.15)))

            connectors.add(connector)
            highlight_segments.add(seg)

        outside_group.add(connectors, highlight_segments)

        # Gap: 33.64 -> 34.50
        self.wait(max(0.05, 0.86))

        # ------------------------------------------------------------
        # Beat 11: zoom window around eye event (34.50 - 37.48)
        # ------------------------------------------------------------
        zoom_window = Rectangle(
            width=3.2,
            height=2.2,
            color=YELLOW,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.1,
        ).move_to([x_event, 2.6, 0])

        zoomed_wave = VMobject(color=GOLD, stroke_width=4)
        zoom_pts = [
            np.array([
                x_event + (t - x_event) * 2.8,
                2.6 + (wave_y(t) - 2.0) * 3.0,
                0,
            ])
            for t in np.linspace(x_event - 0.45, x_event + 0.45, 150)
        ]
        zoomed_wave.set_points_smoothly(zoom_pts)

        zoom_vline = DashedLine(
            start=[x_event, 1.7, 0],
            end=[x_event, 3.5, 0],
            color=RED,
            stroke_width=2,
        )

        zoom_group = VGroup(zoom_window, zoomed_wave, zoom_vline)

        dim_targets = [
            timeline_line,
            wave,
            dashed_event,
            speaker,
            hand,
            button,
            connectors,
            highlight_segments,
        ]

        self.play(*[m.animate.set_opacity(0.25) for m in dim_targets], run_time=max(0.05, 0.7))
        self.play(GrowFromCenter(zoom_window), run_time=max(0.05, 0.55))
        self.play(Create(zoomed_wave), run_time=max(0.05, 0.75))
        self.play(Create(zoom_vline), run_time=max(0.05, 0.35))
        self.wait(max(0.05, 0.63))

        # Gap: 37.48 -> 37.98
        self.wait(max(0.05, 0.50))

        # ------------------------------------------------------------
        # Beat 12: expand window around each event (37.98 - 41.34)
        # ------------------------------------------------------------
        around_text = Text("around each event", font_size=30, color=WHITE).move_to([0, -0.35, 0])

        self.play(zoom_group.animate.scale(1.35).move_to([0, 1.6, 0]), run_time=max(0.05, 1.3))
        self.play(FadeIn(around_text), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 1.46))

        # Gap: 41.34 -> 42.14
        self.wait(max(0.05, 0.80))

        # ------------------------------------------------------------
        # Beat 13: sharpened zoomed ERP waveform + phrase (42.14 - 47.06)
        # ------------------------------------------------------------
        self.play(
            *[FadeOut(mob) for mob in outside_group],
            FadeOut(around_text),
            run_time=max(0.05, 0.8),
        )

        self.play(
            zoomed_wave.animate.set_stroke(width=5).set_color(YELLOW).set_opacity(1),
            zoom_window.animate.set_stroke(width=4),
            run_time=max(0.05, 0.8),
        )

        erp_word1 = Text("Event-Related", font_size=50, color=WHITE)
        erp_word2 = Text("Potential", font_size=50, color=WHITE)
        phrase_group = VGroup(erp_word1, erp_word2).arrange(RIGHT, buff=0.2)
        phrase_group.move_to([0, -0.75, 0])

        self.play(AddTextLetterByLetter(erp_word1), run_time=max(0.05, 1.2))
        self.play(AddTextLetterByLetter(erp_word2), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.12))

        # Gap: 47.06 -> 47.68
        self.wait(max(0.05, 0.62))

        # ------------------------------------------------------------
        # Beat 14: ERP letters + shrinking phrase + inset waveform (47.68 - 49.48)
        # ------------------------------------------------------------
        erp_text = Text("ERP", font_size=130, weight=BOLD, color=YELLOW)
        erp_text.move_to([0, -0.3, 0])

        self.play(GrowFromCenter(erp_text), run_time=max(0.05, 0.6))
        self.play(
            phrase_group.animate.scale(0.45).move_to([0, 1.0, 0]),
            zoom_group.animate.scale(0.35).move_to([0, 2.7, 0]),
            run_time=max(0.05, 1.2),
        )

        # ------------------------------------------------------------
        # Beat 15: hold final frame (49.48 - 50.23)
        # ------------------------------------------------------------
        self.wait(max(0.05, 0.75))