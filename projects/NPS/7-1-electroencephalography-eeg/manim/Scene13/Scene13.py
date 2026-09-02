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


class Scene13(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        wave_time = ValueTracker(0)
        delta_amp = ValueTracker(0.45)

        def advance(duration, *anims):
            if duration <= 0:
                return
            safe = max(0.05, float(duration))
            all_anims = list(anims)
            all_anims.append(wave_time.animate.increment_value(safe))
            self.play(*all_anims, run_time=max(0.05, safe), rate_func=linear)

        # ------------------------------------------------------------------
        # Helper builders
        # ------------------------------------------------------------------
        def make_muscle(color=MAROON):
            body = RoundedRectangle(
                corner_radius=0.3,
                width=1.4,
                height=0.75,
                fill_color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=2,
            )
            lines = VGroup(*[
                Line(
                    body.get_top() + UP * 0.01 + RIGHT * dx,
                    body.get_bottom() + DOWN * 0.01 + RIGHT * dx,
                    color=WHITE,
                    stroke_width=1.5,
                )
                for dx in [-0.25, 0, 0.25]
            ])
            tendon_l = Rectangle(
                width=0.28, height=0.4,
                fill_color=GREY, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1,
            ).next_to(body, LEFT, buff=0)
            tendon_r = Rectangle(
                width=0.28, height=0.4,
                fill_color=GREY, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1,
            ).next_to(body, RIGHT, buff=0)
            return VGroup(tendon_l, body, tendon_r, lines)

        def make_muscle_with_x():
            muscle = make_muscle()
            left = muscle.get_left()
            right = muscle.get_right()
            cross1 = Line(left + UP * 0.35, right + DOWN * 0.35,
                          color=RED, stroke_width=6)
            cross2 = Line(left + DOWN * 0.35, right + UP * 0.35,
                          color=RED, stroke_width=6)
            group = VGroup(muscle, cross1, cross2)
            group.scale_to_fit_width(1.8)
            return group

        def make_eye_base():
            sclera = Ellipse(
                width=0.9, height=0.5,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=1,
            )
            iris = Circle(
                radius=0.13,
                fill_color=BLUE, fill_opacity=1,
                stroke_color=BLACK, stroke_width=0.8,
            )
            return VGroup(sclera, iris)

        def make_cloud_icon():
            c1 = Circle(radius=0.35, fill_color=WHITE, fill_opacity=1,
                        stroke_color=WHITE, stroke_width=1)
            c2 = Circle(radius=0.42, fill_color=WHITE, fill_opacity=1,
                        stroke_color=WHITE, stroke_width=1).shift(LEFT * 0.4 + UP * 0.12)
            c3 = Circle(radius=0.38, fill_color=WHITE, fill_opacity=1,
                        stroke_color=WHITE, stroke_width=1).shift(RIGHT * 0.42 + UP * 0.1)
            base = RoundedRectangle(
                corner_radius=0.45, width=1.4, height=0.5,
                fill_color=WHITE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=0,
            ).shift(DOWN * 0.25)
            return VGroup(base, c1, c2, c3)

        # ------------------------------------------------------------------
        # Previous scene's composition (simplified reconstruction for fade-out)
        # ------------------------------------------------------------------
        prev_title = Text("Sleep", font_size=52, color=GOLD, weight="BOLD").move_to(np.array([0, 3.1, 0]))

        prev_nrem_box = RoundedRectangle(
            corner_radius=0.15, width=3.2, height=1.0,
            fill_color=BLUE, fill_opacity=0.3,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(np.array([-3.3, 1.7, 0]))
        prev_nrem_text = Text("NREM sleep", font_size=20, color=WHITE).move_to(prev_nrem_box)

        prev_rem_box = RoundedRectangle(
            corner_radius=0.15, width=3.2, height=1.0,
            fill_color=PINK, fill_opacity=0.3,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(np.array([3.3, 1.7, 0]))
        prev_rem_text = Text("REM sleep", font_size=20, color=WHITE).move_to(prev_rem_box)

        prev_stage1 = RoundedRectangle(
            corner_radius=0.1, width=1.6, height=0.55,
            fill_color=BLUE, fill_opacity=0.35,
            stroke_color=WHITE, stroke_width=1.2,
        ).move_to(np.array([-3.3, 0.25, 0]))
        prev_stage1_txt = Text("Stage 1", font_size=14, color=WHITE).move_to(prev_stage1)

        prev_stage2 = RoundedRectangle(
            corner_radius=0.1, width=1.6, height=0.55,
            fill_color=BLUE, fill_opacity=0.55,
            stroke_color=WHITE, stroke_width=1.2,
        ).move_to(np.array([-3.3, -0.55, 0]))
        prev_stage2_txt = Text("Stage 2", font_size=14, color=WHITE).move_to(prev_stage2)

        prev_stage3 = RoundedRectangle(
            corner_radius=0.1, width=1.6, height=0.55,
            fill_color=BLUE, fill_opacity=0.75,
            stroke_color=WHITE, stroke_width=1.2,
        ).move_to(np.array([-3.3, -1.35, 0]))
        prev_stage3_txt = Text("Stage 3", font_size=14, color=WHITE).move_to(prev_stage3)

        prev_wake_panel = RoundedRectangle(
            corner_radius=0.15, width=12, height=0.8,
            fill_color=BLACK, fill_opacity=0.55,
            stroke_color=TEAL, stroke_width=1.5,
        ).move_to(np.array([0, -2.3, 0]))

        prev_light_panel = RoundedRectangle(
            corner_radius=0.15, width=12, height=0.8,
            fill_color=BLACK, fill_opacity=0.55,
            stroke_color=BLUE, stroke_width=1.5,
        ).move_to(np.array([0, -3.3, 0]))

        prev_comp = VGroup(
            prev_title,
            prev_nrem_box, prev_nrem_text,
            prev_rem_box, prev_rem_text,
            prev_stage1, prev_stage1_txt,
            prev_stage2, prev_stage2_txt,
            prev_stage3, prev_stage3_txt,
            prev_wake_panel, prev_light_panel,
        )
        prev_comp.scale_to_fit_width(11.5)
        self.add(prev_comp)

        # ------------------------------------------------------------------
        # Deep sleep primary mobjects
        # ------------------------------------------------------------------
        deep_label = Text("Deep sleep", font_size=48, color=WHITE, weight="BOLD")
        deep_label.move_to(np.array([0, 3.15, 0]))

        deep_panel_bg = RoundedRectangle(
            corner_radius=0.15,
            width=12.0,
            height=1.8,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_color=PURPLE,
            stroke_width=1.5,
        )
        deep_panel_bg.move_to(np.array([0, 1.4, 0]))

        deep_caption = Text("delta waves (~1–2 Hz)", font_size=22, color=YELLOW)
        deep_caption.next_to(deep_panel_bg, DOWN, buff=0.15)

        delta_wave = VMobject()
        delta_wave.set_stroke(color=YELLOW, width=4, opacity=0)

        def update_delta_wave(mob):
            left = deep_panel_bg.get_left()[0] + 0.2
            right = deep_panel_bg.get_right()[0] - 0.2
            cy = deep_panel_bg.get_center()[1]
            t = wave_time.get_value()
            u = np.linspace(0, 1, 220)
            xs = left + u * (right - left)
            amp = delta_amp.get_value()
            y = amp * np.sin(2 * np.pi * 1.5 * u - 0.8 * t) + 0.07 * np.sin(2 * np.pi * 3.0 * u - 1.4 * t)
            mob.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )

        delta_wave.add_updater(update_delta_wave)

        # REM mobjects (hidden until Beat 4)
        rem_label = Text("REM sleep", font_size=48, color=PINK, weight="BOLD")
        rem_label.move_to(np.array([0, -0.35, 0]))

        rem_panel_bg = RoundedRectangle(
            corner_radius=0.15,
            width=12.0,
            height=1.0,
            fill_color=BLACK,
            fill_opacity=0.55,
            stroke_color=PINK,
            stroke_width=1.5,
        )
        rem_panel_bg.move_to(np.array([0, -1.7, 0]))

        rem_caption = Text("irregular, fast activity", font_size=22, color=GREY)
        rem_caption.next_to(rem_panel_bg, DOWN, buff=0.15)

        rem_wave = VMobject()
        rem_wave.set_stroke(color=TEAL, width=2.5, opacity=0)

        def update_rem_wave(mob):
            left = rem_panel_bg.get_left()[0] + 0.2
            right = rem_panel_bg.get_right()[0] - 0.2
            cy = rem_panel_bg.get_center()[1]
            t = wave_time.get_value()
            u = np.linspace(0, 1, 200)
            xs = left + u * (right - left)
            y = 0.10 * (
                0.7 * np.sin(2 * np.pi * 13.3 * u - 9.0 * t)
                + 0.35 * np.sin(2 * np.pi * 21.7 * u - 15.0 * t + 1.8)
                + 0.2 * np.sin(2 * np.pi * 37.1 * u - 29.0 * t + 0.6)
            )
            mob.set_points_as_corners(
                np.array([xs, np.full_like(xs, cy) + y, np.zeros_like(xs)]).T
            )

        rem_wave.add_updater(update_rem_wave)

        # Add hidden waves to scene so updaters run throughout
        self.add(delta_wave, rem_wave)

        # ------------------------------------------------------------------
        # Beat 1: 0.00–2.20 fade previous composition, introduce Deep sleep
        # ------------------------------------------------------------------
        advance(1.6, FadeOut(prev_comp), FadeIn(deep_label), FadeIn(deep_panel_bg))
        advance(0.6)

        # ------------------------------------------------------------------
        # Beat 2: 2.20–6.18 delta wave scrolling, amplitude becomes dominant
        # ------------------------------------------------------------------
        advance(0.8, FadeIn(delta_wave), FadeIn(deep_caption))
        advance(3.18, delta_amp.animate.set_value(0.62))

        # Gap 6.18–7.00
        advance(0.82)

        # ------------------------------------------------------------------
        # Beat 3: 7.00–10.94 physical recovery icon
        # ------------------------------------------------------------------
        recovery_heart = SVGMobject(
            ASSET_PATHS["heart"],
            fill_color=RED, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1,
            height=0.7,
        )
        recovery_icons = VGroup(make_muscle(MAROON), recovery_heart).arrange(RIGHT, buff=0.3)
        recovery_label = Text("Physical recovery / restorative processes", font_size=17, color=WHITE)
        recovery_group = VGroup(recovery_icons, recovery_label).arrange(DOWN, buff=0.08)
        recovery_group.scale_to_fit_width(3.4)
        recovery_group.move_to(np.array([4.2, 3.15, 0]))

        advance(1.4, FadeIn(recovery_group))
        advance(2.54)

        # Gap 10.94–11.92
        advance(0.98)

        # ------------------------------------------------------------------
        # Beat 4: 11.92–17.52 introduce REM sleep and irregular waveform
        # ------------------------------------------------------------------
        advance(
            1.2,
            deep_label.animate.scale(0.85).move_to(np.array([0, 3.55, 0])),
            deep_panel_bg.animate.scale(0.85).move_to(np.array([0, 1.9, 0])),
            deep_caption.animate.scale(0.85).move_to(np.array([0, 0.8, 0])),
            recovery_group.animate.scale(0.85).move_to(np.array([4.2, 3.55, 0])),
            FadeIn(rem_label),
        )
        advance(1.4, FadeIn(rem_panel_bg), rem_wave.animate.set_opacity(1))
        advance(1.0, FadeIn(rem_caption))
        advance(2.0)

        # Gap 17.52–18.32
        advance(0.80)

        # ------------------------------------------------------------------
        # Beat 5: 18.32–23.76 eye icon + muscle with X
        # ------------------------------------------------------------------
        eye_base = make_eye_base()
        eye_base.move_to(np.array([4.2, -0.35, 0]))

        eye_center = eye_base.get_center()
        left = eye_base.get_left()
        right = eye_base.get_right()
        left_arrow = Arrow(
            left + LEFT * 0.1, left + LEFT * 0.7,
            color=YELLOW, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.25,
        )
        right_arrow = Arrow(
            right + RIGHT * 0.4, right + RIGHT * 0.95,
            color=YELLOW, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.25,
        )
        left_arrow2 = Arrow(
            left + LEFT * 0.22 + UP * 0.1, left + LEFT * 0.78 + UP * 0.22,
            color=YELLOW, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.25,
        )
        eye_arrows = VGroup(left_arrow, right_arrow, left_arrow2)

        muscle_x_group = make_muscle_with_x()
        muscle_x_group.move_to(np.array([4.2, -0.7, 0]))
        muscle_caption = Text("voluntary skeletal muscles inactive", font_size=16, color=WHITE)
        muscle_caption.move_to(np.array([4.2, -1.0, 0]))

        advance(0.6, FadeIn(eye_base))
        for arrow in eye_arrows:
            advance(0.25, Create(arrow))
        advance(1.0, FadeIn(muscle_x_group), FadeIn(muscle_caption))
        advance(3.09)

        # Gap 23.76–24.72
        advance(0.96)

        # ------------------------------------------------------------------
        # Beat 6: 24.72–29.95 dream cloud + memory consolidation icons
        # ------------------------------------------------------------------
        cloud_icon = make_cloud_icon()
        dream_caption = Text("vivid dreaming", font_size=16, color=WHITE)
        dream_group = VGroup(cloud_icon, dream_caption).arrange(DOWN, buff=0.08)
        dream_group.scale_to_fit_width(2.8)
        dream_group.move_to(np.array([-4.2, -0.15, 0]))

        brain = SVGMobject(
            ASSET_PATHS["brain"],
            fill_color=PURPLE, fill_opacity=1,
            stroke_color=WHITE, stroke_width=0,
            height=0.8,
        )
        plus_v = Line(UP * 0.15, DOWN * 0.15, color=YELLOW, stroke_width=5)
        plus_h = Line(LEFT * 0.15, RIGHT * 0.15, color=YELLOW, stroke_width=5)
        plus = VGroup(plus_v, plus_h).scale(0.6)
        plus.next_to(brain, UR, buff=0.05)
        memory_icon = VGroup(brain, plus)
        memory_caption = Text("memory consolidation", font_size=16, color=WHITE)
        memory_group = VGroup(memory_icon, memory_caption).arrange(DOWN, buff=0.08)
        memory_group.scale_to_fit_width(2.8)
        memory_group.move_to(np.array([-4.2, -0.75, 0]))

        advance(1.2, FadeIn(dream_group))
        advance(1.2, FadeIn(memory_group))
        advance(2.83)