ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

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

from manim import *
import numpy as np


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Heading
        heading = Text("Sensory Stimulation", font_size=50, weight="BOLD", color=WHITE)
        heading.to_edge(UP, buff=0.45)

        # Icon geometry
        icon_x = [-4.2, 0.0, 4.2]
        icon_y = 1.05
        glow_colors = [BLUE, ORANGE, GREEN]
        trace_colors = [BLUE, ORANGE, GREEN]
        labels = ["Visual", "Auditory", "Tactile"]

        # -------------------------
        # Build icons and glows
        # -------------------------

        # Visual: eye
        eye_outer = Ellipse(
            width=1.25, height=0.55,
            stroke_color=WHITE, stroke_width=4,
            fill_color=WHITE, fill_opacity=0.08,
        )
        iris = Circle(radius=0.21, fill_color=BLUE, fill_opacity=0.75, stroke_width=0)
        visual_icon = VGroup(eye_outer, iris)
        visual_icon.scale_to_fit_height(1.0)
        visual_icon.move_to(np.array([icon_x[0], icon_y, 0.0]))

        # Auditory: ear (stylized outer ellipse + inner curve)
        ear_outer = Ellipse(
            width=0.82, height=1.15,
            stroke_color=WHITE, stroke_width=4,
            fill_color=WHITE, fill_opacity=0.08,
        )
        ear_outer.move_to(np.array([icon_x[1], icon_y, 0.0]))
        ear_inner = ArcBetweenPoints(
            ear_outer.get_left() + UP * 0.22 + RIGHT * 0.12,
            ear_outer.get_left() + DOWN * 0.22 + RIGHT * 0.12,
            angle=PI / 2,
            color=WHITE,
            stroke_width=3,
        )
        auditory_icon = VGroup(ear_outer, ear_inner)

        # Tactile: hand asset
        tactile_icon = SVGMobject(ASSET_PATHS["hand"])
        tactile_icon.set_color(WHITE)
        tactile_icon.scale_to_fit_height(1.0)
        tactile_icon.move_to(np.array([icon_x[2], icon_y, 0.0]))

        icons = [visual_icon, auditory_icon, tactile_icon]

        # Icon glows (created for highlighting pulses)
        glows = VGroup()
        for center_x, color in zip(icon_x, glow_colors):
            glow = Circle(
                radius=0.95,
                fill_color=color,
                fill_opacity=0.0,
                stroke_width=0,
            )
            glow.move_to(np.array([center_x, icon_y, 0.0]))
            glow.set_z_index(-1)
            glows.add(glow)

        visual_glow = glows[0]
        auditory_glow = glows[1]
        tactile_glow = glows[2]

        # Labels
        visual_label = Text(labels[0], font_size=25, color=WHITE).next_to(visual_icon, DOWN, buff=0.22)
        auditory_label = Text(labels[1], font_size=25, color=WHITE).next_to(auditory_icon, DOWN, buff=0.22)
        tactile_label = Text(labels[2], font_size=25, color=WHITE).next_to(tactile_icon, DOWN, buff=0.22)
        icon_labels = [visual_label, auditory_label, tactile_label]

        # -------------------------
        # Scrolling waveform traces
        # -------------------------
        trace_center_y = -0.65
        trace_width = 3.2
        trace_num_points = 260
        spike_sigma = 0.06
        spike_height = 0.55
        baseline_amp = 0.16

        scroll_tracker = ValueTracker(0.0)
        scroll_speed = 0.4  # cycles-ish per second; horizontal scroll speed

        visual_amp_t = ValueTracker(0.0)
        visual_pos_t = ValueTracker(-1.5)
        auditory_amp_t = ValueTracker(0.0)
        auditory_pos_t = ValueTracker(-1.5)
        tactile_amp_t = ValueTracker(0.0)
        tactile_pos_t = ValueTracker(-1.5)

        amp_trackers = [visual_amp_t, auditory_amp_t, tactile_amp_t]
        pos_trackers = [visual_pos_t, auditory_pos_t, tactile_pos_t]

        def make_trace_mobject(center_x, amp_t, pos_t, color):
            def get_trace():
                phase = scroll_tracker.get_value()
                xs = np.linspace(-trace_width / 2, trace_width / 2, trace_num_points)
                baseline = baseline_amp * np.sin(2 * PI * 0.9 * (xs + phase))
                amp = amp_t.get_value()
                pos = pos_t.get_value()
                spike = amp * spike_height * np.exp(-((xs - pos) ** 2) / (2 * spike_sigma ** 2))
                ys = baseline + spike
                points = [
                    np.array([center_x + x, trace_center_y + y, 0.0])
                    for x, y in zip(xs, ys)
                ]
                trace = VMobject(stroke_color=color, stroke_width=3)
                trace.set_points_as_corners(points)
                return trace
            return always_redraw(get_trace)

        visual_trace = make_trace_mobject(icon_x[0], visual_amp_t, visual_pos_t, trace_colors[0])
        auditory_trace = make_trace_mobject(icon_x[1], auditory_amp_t, auditory_pos_t, trace_colors[1])
        tactile_trace = make_trace_mobject(icon_x[2], tactile_amp_t, tactile_pos_t, trace_colors[2])

        scroll_tracker.add_updater(lambda m, dt: m.increment_value(scroll_speed * dt))
        self.add(scroll_tracker)

        # Bottom note
        note_text = Text(
            "transient responses — short periods of time",
            font_size=25,
            color=WHITE,
            t2c={
                "transient responses": YELLOW,
                "short periods of time": YELLOW,
            },
        )
        if note_text.width > 12.0:
            note_text.scale_to_fit_width(12.0)
        note_box = SurroundingRectangle(
            note_text,
            color=YELLOW,
            buff=0.22,
            corner_radius=0.14,
            fill_color=YELLOW,
            fill_opacity=0.12,
            stroke_width=3,
        )
        note_group = VGroup(note_box, note_text).to_edge(DOWN, buff=0.45)

        # =================== TIMED SEQUENCE ===================
        # 0.00-1.48: heading fades in
        self.play(FadeIn(heading), run_time=max(0.05, 1.48))

        # 1.48-2.22: pause
        self.wait(max(0.05, 0.74))

        # 2.22-3.52: pause
        self.wait(max(0.05, 1.30))

        # 3.52-3.88: first icon + label fade in (visual)
        self.play(FadeIn(visual_icon, visual_label), run_time=max(0.05, 0.36))

        # 3.88-4.78: visual highlight briefly, then dim
        self.play(
            visual_glow.animate.set_opacity(0.55).scale(1.15),
            run_time=max(0.05, 0.45),
        )
        self.play(
            visual_glow.animate.set_opacity(0.0).scale(1 / 1.15),
            run_time=max(0.05, 0.45),
        )

        # 4.78-5.10: auditory + tactile icons/labels appear; ear then hand highlight
        self.play(FadeIn(auditory_icon, auditory_label, tactile_icon, tactile_label), run_time=max(0.05, 0.14))
        self.play(auditory_glow.animate.set_opacity(0.55).scale(1.15), run_time=max(0.05, 0.08))
        self.play(
            auditory_glow.animate.set_opacity(0.0).scale(1 / 1.15),
            tactile_glow.animate.set_opacity(0.55).scale(1.15),
            run_time=max(0.05, 0.05),
        )
        self.play(tactile_glow.animate.set_opacity(0.0).scale(1 / 1.15), run_time=max(0.05, 0.05))

        # 5.10-5.72: all three icons pulse softly in unison
        self.play(
            visual_glow.animate.set_opacity(0.45).scale(1.2),
            auditory_glow.animate.set_opacity(0.45).scale(1.2),
            tactile_glow.animate.set_opacity(0.45).scale(1.2),
            rate_func=there_and_back,
            run_time=max(0.05, 0.62),
        )

        # 5.72-6.32: baseline traces fade in
        self.play(FadeIn(visual_trace, auditory_trace, tactile_trace), run_time=max(0.05, 0.60))

        # 6.32-7.70: visual highlight + visual transient spike
        self.play(visual_glow.animate.set_opacity(0.65).scale(1.25), run_time=max(0.05, 0.18))
        self.play(visual_amp_t.animate.set_value(1.0), run_time=max(0.05, 0.15))
        self.play(visual_pos_t.animate.set_value(1.5), run_time=max(0.05, 0.68), rate_func=linear)
        self.play(
            visual_amp_t.animate.set_value(0.0),
            visual_glow.animate.set_opacity(0.0).scale(1 / 1.25),
            run_time=max(0.05, 0.37),
        )

        # 7.70-8.68: pause; visual highlight dims, baselines scroll
        self.wait(max(0.05, 0.98))

        # 8.68-9.20: hold; no new element
        self.wait(max(0.05, 0.52))

        # 9.20-10.26: auditory highlight + auditory transient
        self.play(auditory_glow.animate.set_opacity(0.65).scale(1.25), run_time=max(0.05, 0.16))
        self.play(auditory_amp_t.animate.set_value(1.0), run_time=max(0.05, 0.14))
        self.play(auditory_pos_t.animate.set_value(1.5), run_time=max(0.05, 0.58), rate_func=linear)
        self.play(
            auditory_amp_t.animate.set_value(0.0),
            auditory_glow.animate.set_opacity(0.0).scale(1 / 1.25),
            run_time=max(0.05, 0.18),
        )

        # 10.26-10.48: tactile highlight + very brief tactile transient
        self.play(
            tactile_glow.animate.set_opacity(0.6).scale(1.2),
            auditory_glow.animate.set_opacity(0.0).scale(1 / 1.2),
            run_time=max(0.05, 0.07),
        )
        self.play(tactile_amp_t.animate.set_value(1.0), run_time=max(0.05, 0.05))
        self.play(tactile_pos_t.animate.set_value(0.8), run_time=max(0.05, 0.05), rate_func=linear)
        self.play(
            tactile_amp_t.animate.set_value(0.0),
            tactile_glow.animate.set_opacity(0.0).scale(1 / 1.2),
            run_time=max(0.05, 0.05),
        )

        # 10.48-11.68: three distinct brief transients -- visual, auditory, tactile
        for amp_t, pos_t in zip(amp_trackers, pos_trackers):
            pos_t.set_value(-1.5)
            amp_t.set_value(0.0)
        for amp_t, pos_t in zip(amp_trackers, pos_trackers):
            self.play(amp_t.animate.set_value(1.0), run_time=max(0.05, 0.10))
            self.play(pos_t.animate.set_value(1.2), run_time=max(0.05, 0.22), rate_func=linear)
            self.play(amp_t.animate.set_value(0.0), run_time=max(0.05, 0.08))

        # 11.68-12.52: hold steady while traces scroll
        self.wait(max(0.05, 0.84))

        # 12.52-14.46: more frequent transient spikes; icons pulse softly again
        self.play(
            visual_glow.animate.set_opacity(0.45).scale(1.2),
            auditory_glow.animate.set_opacity(0.45).scale(1.2),
            tactile_glow.animate.set_opacity(0.45).scale(1.2),
            rate_func=there_and_back,
            run_time=max(0.05, 0.50),
        )
        transient_order = [
            (visual_amp_t, visual_pos_t),
            (auditory_amp_t, auditory_pos_t),
            (tactile_amp_t, tactile_pos_t),
            (visual_amp_t, visual_pos_t),
            (auditory_amp_t, auditory_pos_t),
            (tactile_amp_t, tactile_pos_t),
        ]
        for amp_t, pos_t in transient_order:
            pos_t.set_value(-1.5)
            amp_t.set_value(0.0)
            self.play(amp_t.animate.set_value(1.0), run_time=max(0.05, 0.05))
            self.play(pos_t.animate.set_value(1.2), run_time=max(0.05, 0.14), rate_func=linear)
            self.play(amp_t.animate.set_value(0.0), run_time=max(0.05, 0.05))

        # 14.46-15.20: highlighted note fades in near bottom
        self.play(FadeIn(note_group), run_time=max(0.05, 0.74))

        # 15.20-16.05: final hold
        self.wait(max(0.05, 0.85))