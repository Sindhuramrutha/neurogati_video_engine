ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene9(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ── Generate representative signals for each modality ──
        n_pts = 200
        t = np.linspace(0, 1, n_pts)
        np.random.seed(99)

        # EEG: low-frequency oscillations
        eeg = 0.5 * np.sin(2 * np.pi * 8 * t) + 0.3 * np.sin(2 * np.pi * 20 * t) + 0.1 * np.random.randn(n_pts)

        # EMG: high-frequency bursty noise
        emg_noise = np.random.randn(n_pts)
        envelope = np.sin(2 * np.pi * t * 3) ** 2
        emg = envelope * emg_noise * 0.8 + 0.1 * np.random.randn(n_pts)

        # LFP: slower oscillations
        lfp = 0.6 * np.sin(2 * np.pi * 0.5 * t) + 0.3 * np.sin(2 * np.pi * 2 * t + 1) + 0.15 * np.random.randn(n_pts)

        # Single-unit: baseline with occasional sharp spikes
        unit = 0.05 * np.random.randn(n_pts)
        spike_idx = [15, 45, 75, 110, 140, 170]
        for i in spike_idx:
            unit[i] += 1.8

        # ── Helper to create a waveform VMobject ──
        def make_waveform(signal, color, width=2.2, height=1.0):
            n = len(signal)
            x = np.linspace(-width / 2, width / 2, n)
            y = signal - np.mean(signal)
            y = y / (np.max(np.abs(y)) * 1.1) * height / 2
            points = [np.array([x[i], y[i], 0]) for i in range(n)]
            trace = VMobject(stroke_color=color, stroke_width=2.8, fill_opacity=0)
            trace.set_points_as_corners(points)
            return trace

        # ── Title ──
        title = Text(
            "Selecting Filters for Common Neural Signals",
            font_size=34,
            color=YELLOW,
            weight=BOLD,
        )
        title.scale_to_fit_width(12)
        title.to_edge(UP, buff=0.3)

        # ── Build four modality columns ──
        modalities = [
            ("EEG", "EEG", eeg, BLUE, "0.5\u201340 Hz"),          # en dash
            ("EMG", "EMG", emg, ORANGE, "10\u2013500 Hz"),
            ("LFP", "LFP", lfp, TEAL, "0.5\u2013200 Hz"),
            ("SU", "Single-unit", unit, PINK, "300\u20133000 Hz"),
        ]

        containers = []
        waveforms = []
        freq_texts = []

        for abbr, full, sig, col, frange in modalities:
            # Icon circle with abbreviation
            circle = Circle(radius=0.4, fill_color=col, fill_opacity=1, stroke_width=0)
            icon_text = Text(abbr, font_size=22, color=WHITE, weight=BOLD)
            icon_text.move_to(circle.get_center())
            icon = VGroup(circle, icon_text)

            # Modality label
            label = Text(full, font_size=20, color=col)
            label.next_to(icon, DOWN, buff=0.1)

            # Bounding box for waveform
            box = Rectangle(
                width=2.5, height=1.2,
                stroke_color=GREY, stroke_width=1.5,
                fill_opacity=0,
            )
            box.next_to(label, DOWN, buff=0.2)

            # Waveform trace
            wave = make_waveform(sig, col, width=2.2, height=1.0)
            wave.move_to(box.get_center())

            # Frequency range label
            freq = Text(frange, font_size=16, color=GREY_B)
            freq.next_to(box, DOWN, buff=0.15)

            # Container without waveform and freq_text (so we can reveal them later)
            container = VGroup(icon, label, box)
            containers.append(container)
            waveforms.append(wave)
            freq_texts.append(freq)

        # Arrange all four columns side by side
        x_centers = np.linspace(-5.5, 5.5, 4)
        for i, cont in enumerate(containers):
            cont.move_to(np.array([x_centers[i], 0, 0]))
        columns_group = VGroup(*containers)
        columns_group.next_to(title, DOWN, buff=0.6)

        # Also group waveforms and freq_texts for later fadeouts
        waveforms_group = VGroup(*waveforms)
        freq_group = VGroup(*freq_texts)
        # They are already positioned inside each column's container; just need to be added later

        # ── Timing definition ──
        # Beat 1: 0.00–1.50   Title
        self.play(Write(title), run_time=max(0.05, 1.5))

        # Beat 2: 1.50–2.70   Columns appear
        self.play(FadeIn(columns_group, shift=UP * 0.5), run_time=max(0.05, 1.2))

        # Beat 3: 2.70–4.20   Waveforms drawn
        for wave in waveforms:
            self.play(Create(wave), run_time=max(0.05, 0.375))   # 4 * 0.375 = 1.5 s

        # Beat 4: 4.20–6.70   Frequency ranges appear
        for freq in freq_texts:
            self.play(FadeIn(freq), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.5))   # total 2.0 + 0.5 = 2.5 s

        # Beat 5: 6.70–9.70   Summary diagram (funnel + text)
        funnel = SVGMobject(
            ASSET_PATHS["funnel"],
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
            height=1.2,
        )
        funnel.move_to(ORIGIN + DOWN * 2.5)
        summary_text = Text(
            "Objective-driven filter selection",
            font_size=28,
            color=YELLOW,
            weight=BOLD,
        )
        summary_text.next_to(funnel, UP, buff=0.3)

        self.play(FadeIn(funnel), Write(summary_text), run_time=max(0.05, 2.0))
        self.wait(max(0.05, 1.0))

        # Beat 6: 9.70–13.70   Transition to takeaway
        takeaway = Text(
            "Filter choice depends on\nsignal characteristics & analysis goals",
            font_size=32,
            color=TEAL,
            weight=BOLD,
            line_spacing=1.1,
        )
        takeaway.move_to(ORIGIN)

        self.play(
            FadeOut(columns_group),
            FadeOut(waveforms_group),
            FadeOut(freq_group),
            FadeOut(title),
            FadeOut(funnel),
            FadeOut(summary_text),
            run_time=max(0.05, 1.5),
        )
        self.play(Write(takeaway), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.5))   # total 4.0 s

        # Beat 7: 13.70–17.70   Hold takeaway with gentle pulse
        # (A slow pulse via scale oscillation, using ValueTracker)
        pulse = ValueTracker(1)
        takeaway.add_updater(lambda mo: mo.set_opacity(np.interp(np.sin(pulse.get_value() * 3), [-1, 1], [0.8, 1.0])))
        self.play(pulse.animate.set_value(4 * np.pi), run_time=max(0.05, 4.0), rate_func=linear)
        takeaway.clear_updaters()

        # Beat 8: 17.70–19.98   Fade out
        self.play(FadeOut(takeaway), run_time=max(0.05, 1.0))
        self.wait(max(0.05, 1.28))