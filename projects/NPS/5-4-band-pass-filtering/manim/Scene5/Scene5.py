ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


def make_trace(signal, center, width, height, color, stroke_width=2):
    scaled = signal / max(np.max(np.abs(signal)), 1e-9) * (height / 2) * 0.85
    xs = np.linspace(center[0] - width / 2, center[0] + width / 2, len(signal))
    pts = [np.array([xs[i], center[1] + scaled[i], 0]) for i in range(len(signal))]
    trace = VMobject(stroke_color=color, stroke_width=stroke_width)
    trace.set_points_as_corners(pts)
    return trace


def build_eeg_graphic():
    np.random.seed(123)
    t = np.linspace(0, 1, 500)
    drift = 0.7 * np.sin(2 * np.pi * 0.4 * t)
    brain = 1.0 * np.sin(2 * np.pi * 8 * t) + 0.4 * np.sin(2 * np.pi * 16 * t)
    noise = 0.25 * np.random.randn(500)
    raw = drift + brain + noise
    filt = 0.9 * brain

    raw_trace = make_trace(raw, np.array([2.5, 0.7, 0]), 4.8, 1.0, GREY)
    filt_trace = make_trace(filt, np.array([2.5, -1.0, 0]), 4.8, 1.0, TEAL)
    raw_label = Text("Raw EEG", font_size=18, color=GREY).move_to(np.array([2.5, 1.35, 0]))
    filt_label = Text("Filtered EEG (1–40 Hz)", font_size=18, color=TEAL).move_to(np.array([2.5, -1.85, 0]))
    arrow = Arrow(
        start=np.array([2.2, 0.15, 0]),
        end=np.array([2.2, -0.35, 0]),
        color=TEAL,
        stroke_width=4,
        buff=0,
    )
    arrow_label = Text("band-pass", font_size=16, color=TEAL).next_to(arrow, RIGHT, buff=0.12).scale_to_fit_width(1.2)
    return VGroup(raw_trace, filt_trace, raw_label, filt_label, arrow, arrow_label)


def build_emg_graphic():
    np.random.seed(7)
    t = np.linspace(0, 1, 600)
    slow = 0.55 * np.sin(2 * np.pi * 0.35 * t) + 0.30 * np.sin(2 * np.pi * 1.2 * t)
    envelope = np.exp(-((t - 0.45) ** 2) / 0.015) + np.exp(-((t - 0.75) ** 2) / 0.008)
    muscle = 0.85 * envelope * np.random.randn(600)
    raw = slow + muscle
    filt = 0.85 * envelope * np.random.randn(600)

    raw_trace = make_trace(raw, np.array([2.5, 0.7, 0]), 4.8, 1.0, GREY)
    filt_trace = make_trace(filt, np.array([2.5, -1.0, 0]), 4.8, 1.0, ORANGE)
    raw_label = Text("Raw EMG", font_size=18, color=GREY).move_to(np.array([2.5, 1.35, 0]))
    filt_label = Text("Filtered EMG", font_size=18, color=ORANGE).move_to(np.array([2.5, -1.85, 0]))
    arrow = Arrow(
        start=np.array([2.2, 0.15, 0]),
        end=np.array([2.2, -0.35, 0]),
        color=ORANGE,
        stroke_width=4,
        buff=0,
    )
    arrow_label = Text("remove motion + noise", font_size=14, color=ORANGE).next_to(arrow, RIGHT, buff=0.12).scale_to_fit_width(1.6)
    return VGroup(raw_trace, filt_trace, raw_label, filt_label, arrow, arrow_label)


def build_lfp_graphic():
    t = np.linspace(0, 1, 600)
    raw = 0.8 * np.sin(2 * np.pi * 3 * t) + 1.0 * np.sin(2 * np.pi * 10 * t) + 0.4 * np.sin(2 * np.pi * 25 * t)
    filt = 1.0 * np.sin(2 * np.pi * 10 * t)

    raw_trace = make_trace(raw, np.array([2.5, 0.7, 0]), 4.8, 1.0, GREY)
    filt_trace = make_trace(filt, np.array([2.5, -1.0, 0]), 4.8, 1.0, TEAL)
    raw_label = Text("Raw LFP", font_size=18, color=GREY).move_to(np.array([2.5, 1.35, 0]))
    filt_label = Text("Filtered LFP (θ band)", font_size=18, color=TEAL).move_to(np.array([2.5, -1.85, 0]))
    arrow = Arrow(
        start=np.array([2.2, 0.15, 0]),
        end=np.array([2.2, -0.35, 0]),
        color=TEAL,
        stroke_width=4,
        buff=0,
    )
    arrow_label = Text("isolate θ", font_size=16, color=TEAL).next_to(arrow, RIGHT, buff=0.12).scale_to_fit_width(1.1)
    return VGroup(raw_trace, filt_trace, raw_label, filt_label, arrow, arrow_label)


def build_bci_graphic():
    box1 = Rectangle(width=1.4, height=0.7, fill_color="#1A1D24", fill_opacity=1, stroke_color=WHITE, stroke_width=1)
    t1 = Text("Raw signal", font_size=16, color=WHITE).scale_to_fit_width(1.1)
    t1.move_to(box1.get_center())
    box1_group = VGroup(box1, t1).move_to(np.array([2.5 - 1.9, -0.2, 0]))

    box2 = Rectangle(width=1.3, height=0.7, fill_color=BLUE, fill_opacity=0.35, stroke_color=BLUE, stroke_width=2)
    t2 = Text("Band-pass", font_size=16, color=WHITE).scale_to_fit_width(1.0)
    t2.move_to(box2.get_center())
    box2_group = VGroup(box2, t2).move_to(np.array([2.5, -0.2, 0]))

    box3 = Rectangle(width=1.7, height=0.7, fill_color=GREEN, fill_opacity=0.35, stroke_color=GREEN, stroke_width=2)
    t3 = Text("Features → Classify", font_size=15, color=WHITE).scale_to_fit_width(1.3)
    t3.move_to(box3.get_center())
    box3_group = VGroup(box3, t3).move_to(np.array([2.5 + 1.9, -0.2, 0]))

    arrow1 = Arrow(
        start=box1_group.get_right() + RIGHT * 0.12,
        end=box2_group.get_left() + LEFT * 0.12,
        color=PURPLE,
        stroke_width=3,
        buff=0,
    )
    arrow2 = Arrow(
        start=box2_group.get_right() + RIGHT * 0.12,
        end=box3_group.get_left() + LEFT * 0.12,
        color=PURPLE,
        stroke_width=3,
        buff=0,
    )
    return VGroup(box1_group, box2_group, box3_group, arrow1, arrow2)


class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        time_elapsed = 0.0
        def play_rt(*args, run_time=max(0.05, 1.0), **kwargs):
            nonlocal time_elapsed
            self.play(*args, run_time=max(0.05, run_time), **kwargs)
            time_elapsed += run_time
        def wait_rt(duration):
            nonlocal time_elapsed
            if duration > 0:
                self.wait(max(0.05, duration))
                time_elapsed += duration

        # ---------- Title ----------
        title = Text("Applications in Neural Signal Processing", font_size=40, color=WHITE, weight="BOLD")
        subtitle = Text("Band-pass filtering in practice", font_size=24, color=GREY)
        title.to_edge(UP, buff=0.35)
        subtitle.next_to(title, DOWN, buff=0.15)

        play_rt(FadeIn(title), run_time=max(0.05, 0.8))
        play_rt(Write(subtitle), run_time=max(0.05, 0.7))
        wait_rt(0.5)

        # ---------- Preview icons ----------
        preview_icons = VGroup(
            SVGMobject(ASSET_PATHS["brain"], fill_color=BLUE, fill_opacity=1, stroke_color=BLUE, stroke_width=0).scale_to_fit_height(0.9),
            SVGMobject(ASSET_PATHS["hand"], fill_color=ORANGE, fill_opacity=1, stroke_color=ORANGE, stroke_width=0).scale_to_fit_height(0.9),
            SVGMobject(ASSET_PATHS["clipboard_pulse"], fill_color=TEAL, fill_opacity=1, stroke_color=TEAL, stroke_width=0).scale_to_fit_height(0.9),
            SVGMobject(ASSET_PATHS["cpu"], fill_color=PURPLE, fill_opacity=1, stroke_color=PURPLE, stroke_width=0).scale_to_fit_height(0.9),
        ).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.1)

        play_rt(FadeIn(preview_icons), run_time=max(0.05, 1.2))
        wait_rt(1.3)

        # ---------- Application loop ----------
        # Data for each modality
        modalities = [
            {
                "name": "EEG",
                "color": BLUE,
                "caption": "Keeps 1–40 Hz activity\nremoves drift + noise",
                "build_graphic": build_eeg_graphic,
            },
            {
                "name": "EMG",
                "color": ORANGE,
                "caption": "Preserves muscle bursts\nremoves motion artefact",
                "build_graphic": build_emg_graphic,
            },
            {
                "name": "LFP",
                "color": TEAL,
                "caption": "Isolates specific\noscillatory bands",
                "build_graphic": build_lfp_graphic,
            },
            {
                "name": "BCI",
                "color": PURPLE,
                "caption": "Preprocessing before\nfeature extraction",
                "build_graphic": build_bci_graphic,
            },
        ]

        # Fade out preview icons
        play_rt(FadeOut(preview_icons), run_time=max(0.05, 0.4))
        t_app_start = time_elapsed
        total_app_duration = 37.7 - t_app_start   # ~32.8 s
        each_app_duration = total_app_duration / 4

        current_panel = None
        for i, mod in enumerate(modalities):
            # Build panel
            panel_bg = Rectangle(
                width=12.6,
                height=4.4,
                fill_color="#1A1D24",
                fill_opacity=1,
                stroke_color=GREY,
                stroke_width=1,
            ).move_to(np.array([0, -0.2, 0]))

            # Load icon explicitly with literal key
            if i == 0:
                icon = SVGMobject(ASSET_PATHS["brain"], fill_color=mod["color"], fill_opacity=1,
                                  stroke_color=mod["color"], stroke_width=0).scale_to_fit_height(1.3)
            elif i == 1:
                icon = SVGMobject(ASSET_PATHS["hand"], fill_color=mod["color"], fill_opacity=1,
                                  stroke_color=mod["color"], stroke_width=0).scale_to_fit_height(1.3)
            elif i == 2:
                icon = SVGMobject(ASSET_PATHS["clipboard_pulse"], fill_color=mod["color"], fill_opacity=1,
                                  stroke_color=mod["color"], stroke_width=0).scale_to_fit_height(1.3)
            else:
                icon = SVGMobject(ASSET_PATHS["cpu"], fill_color=mod["color"], fill_opacity=1,
                                  stroke_color=mod["color"], stroke_width=0).scale_to_fit_height(1.3)
            icon.move_to(np.array([-4.4, -0.2, 0]))

            title_text = Text(mod["name"], font_size=48, color=mod["color"], weight="BOLD")
            caption_text = Text(mod["caption"], font_size=20, color=GREY).scale_to_fit_width(3.8)
            text_group = VGroup(title_text, caption_text).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            text_group.move_to(np.array([-2.2, -0.2, 0]))

            graphic = mod["build_graphic"]()
            graphic.move_to(np.array([2.6, -0.2, 0]))

            panel_group = VGroup(panel_bg, icon, text_group, graphic)

            # Transition
            if current_panel is not None:
                play_rt(FadeOut(current_panel), run_time=max(0.05, 0.5))
            play_rt(FadeIn(panel_group), run_time=max(0.05, 0.7))
            play_rt(Wiggle(graphic, scale_value=1.05), run_time=max(0.05, 1.0))
            play_rt(Indicate(graphic, color=mod["color"]), run_time=max(0.05, 0.8))
            play_rt(Wiggle(graphic, scale_value=1.03), run_time=max(0.05, 0.8))

            current_panel = panel_group

            # Wait until the end of this app's slot
            target_end = t_app_start + (i + 1) * each_app_duration
            wait_rt(max(0.05, target_end - time_elapsed))

        # ---------- Closing recap ----------
        play_rt(FadeOut(current_panel), run_time=max(0.05, 0.5))

        closing_icons = VGroup(
            VGroup(
                SVGMobject(ASSET_PATHS["brain"], fill_color=BLUE, fill_opacity=1, stroke_color=BLUE, stroke_width=0).scale_to_fit_height(1.0),
                Text("EEG", font_size=22, color=BLUE)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                SVGMobject(ASSET_PATHS["hand"], fill_color=ORANGE, fill_opacity=1, stroke_color=ORANGE, stroke_width=0).scale_to_fit_height(1.0),
                Text("EMG", font_size=22, color=ORANGE)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                SVGMobject(ASSET_PATHS["clipboard_pulse"], fill_color=TEAL, fill_opacity=1, stroke_color=TEAL, stroke_width=0).scale_to_fit_height(1.0),
                Text("LFP", font_size=22, color=TEAL)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                SVGMobject(ASSET_PATHS["cpu"], fill_color=PURPLE, fill_opacity=1, stroke_color=PURPLE, stroke_width=0).scale_to_fit_height(1.0),
                Text("BCI", font_size=22, color=PURPLE)
            ).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.3)

        play_rt(FadeIn(closing_icons), run_time=max(0.05, 1.0))
        play_rt(Wiggle(closing_icons, scale_value=1.1), run_time=max(0.05, 1.0))
        play_rt(Indicate(closing_icons, color=WHITE), run_time=max(0.05, 0.8))

        # Fill remaining time
        if time_elapsed < 44.92:
            wait_rt(max(0.05, 44.92 - time_elapsed))