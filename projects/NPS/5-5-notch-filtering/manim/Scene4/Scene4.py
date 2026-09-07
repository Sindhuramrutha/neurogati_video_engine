ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Colours ---
        OFF_WHITE = "#F0EAD6"
        GOLD = "#FFD700"
        HEAD_FILL = OFF_WHITE
        HEAD_STROKE = WHITE
        RED = "#FF4444"
        MONITOR_BEZEL = "#3A3A3A"

        # --- Helper: head outline ---
        head = Circle(radius=1.4, fill_color=HEAD_FILL, fill_opacity=1,
                      stroke_color=HEAD_STROKE, stroke_width=2)
        # Nose/face bump
        nose = Polygon(
            head.get_right() + UP * 0.3,
            head.get_right() + RIGHT * 0.35 + UP * 0.1,
            head.get_right() + RIGHT * 0.35 + DOWN * 0.1,
            head.get_right() + DOWN * 0.3,
            fill_color=HEAD_FILL, fill_opacity=1,
            stroke_color=HEAD_STROKE, stroke_width=2
        )
        head_outline = VGroup(head, nose)
        head_outline.move_to(LEFT * 3.5 + UP * 0.5)

        # --- Electrodes at Fz, Cz, Pz, O1, T3 ---
        electrode_positions = {
            "Fz": head_outline.get_top() + DOWN * 0.5,
            "Cz": head_outline.get_center(),
            "Pz": head_outline.get_bottom() + UP * 0.5,
            "O1": head_outline.get_bottom() + LEFT * 0.4 + UP * 0.2,
            "T3": head_outline.get_left() + RIGHT * 0.20 + UP * 0.1,
        }
        electrodes = VGroup()
        for pos in electrode_positions.values():
            dot = Dot(point=pos, radius=0.18, color=GOLD, stroke_width=2, fill_opacity=1)
            electrodes.add(dot)

        # --- Power socket (right of head) ---
        socket = VGroup()
        socket_body = Rectangle(width=0.8, height=1.0,
                                fill_color="#4A4A4A", fill_opacity=1,
                                stroke_color=WHITE, stroke_width=2)
        slot1 = Line(UP * 0.2, DOWN * 0.05, color="#2A2A2A", stroke_width=4)
        slot2 = Line(UP * 0.2, DOWN * 0.05, color="#2A2A2A", stroke_width=4)
        slot1.shift(LEFT * 0.15)
        slot2.shift(RIGHT * 0.15)
        socket_group = VGroup(socket_body, slot1, slot2)
        socket_group.move_to(RIGHT * 1.5 + UP * 0.5)

        # --- Interference wavy lines ---
        def make_interference():
            wave = VMobject(stroke_color=RED, stroke_width=2.5, fill_opacity=0)
            # Sine-like curve
            points = []
            for t in np.linspace(0, 4 * PI, 150):
                points.append(np.array([t * 0.5, 0.2 * np.sin(t), 0]))
            wave.set_points_as_corners(points)
            wave.set_opacity(0.35)
            return wave

        interference1 = make_interference()
        interference1.move_to(socket_group.get_left() + LEFT * 1.5)
        interference1.shift(DOWN * 0.1)

        interference2 = make_interference()
        interference2.move_to(socket_group.get_left() + LEFT * 2.2)
        interference2.shift(UP * 0.1)

        interference3 = make_interference()
        interference3.move_to(socket_group.get_left() + LEFT * 0.8)
        interference3.shift(DOWN * 0.4)

        interference_group = VGroup(interference1, interference2, interference3)
        # Drift leftward loop
        interference_group.add_updater(lambda m, dt: m.shift(LEFT * dt * 0.3))

        # --- Monitor ---
        monitor_outer = RoundedRectangle(width=2.4, height=1.8, corner_radius=0.2,
                                         fill_color=MONITOR_BEZEL, fill_opacity=1,
                                         stroke_color=WHITE, stroke_width=2)
        monitor_screen = Rectangle(width=2.0, height=1.45,
                                   fill_color="#0A0A1A", fill_opacity=1,
                                   stroke_color=WHITE, stroke_width=1.5)
        monitor_screen.move_to(monitor_outer.get_center())
        monitor_stand = Line(monitor_outer.get_bottom() + DOWN * 0.1,
                             monitor_outer.get_bottom() + DOWN * 0.65,
                             color=WHITE, stroke_width=4)
        monitor_base = Rectangle(width=1.2, height=0.1,
                                 fill_color=WHITE, fill_opacity=1,
                                 stroke_width=0)
        monitor_base.move_to(monitor_stand.get_end() + DOWN * 0.05)
        monitor_group = VGroup(monitor_outer, monitor_screen, monitor_stand, monitor_base)
        monitor_group.move_to(RIGHT * 5.8 + UP * 0.3)

        # --- EEG trace inside monitor ---
        def make_eeg_trace(clean=True, noise_amp=0.0):
            eeg = VMobject(stroke_color="#00FF88", stroke_width=2.5, fill_opacity=0)
            x_min, x_max = -1.0, 1.0
            dx = 0.025
            pts = []
            for i, x in enumerate(np.arange(x_min, x_max + dx, dx)):
                y = 0.5 * np.sin(2 * np.pi * 2.0 * x)  # ~2 Hz
                if noise_amp > 0:
                    y += noise_amp * np.sin(2 * np.pi * 50 * x + 0.3)  # ~50 Hz ripple
                pts.append(np.array([x, y, 0]))
            eeg.set_points_smoothly(pts)
            eeg.stretch_to_fit_width(1.85)
            eeg.stretch_to_fit_height(1.2)
            eeg.move_to(monitor_screen.get_center())
            eeg.set_opacity(0)
            return eeg

        clean_eeg = make_eeg_trace(clean=True)
        noisy_eeg = make_eeg_trace(noise_amp=0.1)

        # --- Frequency spectrum (inside monitor, lower-right) ---
        def make_spectrum():
            spec = VGroup()
            axes = Axes(
                x_range=[0, 100, 20],
                y_range=[0, 1.2, 0.4],
                x_length=1.5,
                y_length=0.8,
                axis_config={"color": GREY, "stroke_width": 1, "include_numbers": False},
                tips=False,
            )
            bg = axes.plot(lambda x: 0.1 + 0.02 * np.sin(0.15 * x),
                           x_range=[0, 100], color=GREY, stroke_width=1.5)
            spike50 = Line(
                axes.c2p(50, 0.1),
                axes.c2p(50, 0.95),
                color=RED, stroke_width=4
            )
            spike60 = Line(
                axes.c2p(60, 0.1),
                axes.c2p(60, 0.45),
                color=RED, stroke_width=4
            )
            spec.add(axes, bg, spike50, spike60)
            return spec

        spectrum = make_spectrum()
        spectrum.move_to(monitor_screen.get_right() + DOWN * 0.3)
        spectrum.shift(LEFT * 0.5 + DOWN * 0.15)
        spectrum.set_opacity(0)

        # --- Notch filter symbols ---
        notch_symbols = VGroup()
        for pos in electrode_positions.values():
            symbol = VGroup()
            circle = Circle(radius=0.15, color=WHITE, stroke_width=2, fill_opacity=0)
            slash = Line(
                circle.get_corner(DL),
                circle.get_corner(UR),
                color=RED, stroke_width=3
            )
            symbol.add(circle, slash)
            symbol.move_to(pos + RIGHT * 0.35)
            symbol.set_opacity(0)
            notch_symbols.add(symbol)

        # --- Labels ---
        filtered_label = Text("Filtered EEG", font_size=22, color=WHITE, weight="BOLD")
        filtered_label.next_to(monitor_group, DOWN, buff=0.2)
        filtered_label.set_opacity(0)

        hum_label = Text("Hum", font_size=14, color=RED, weight="BOLD")
        hum_label.next_to(spectrum[2].get_top(), UP, buff=0.1)
        hum_label.set_opacity(0)

        hum60_label = Text("Hum", font_size=14, color=RED, weight="BOLD")
        hum60_label.next_to(spectrum[3].get_top(), UP, buff=0.1)
        hum60_label.set_opacity(0)

        hum_removed_label = Text("50/60 Hz hum removed", font_size=18, color=GREEN, weight="BOLD")
        hum_removed_label.next_to(spectrum, DOWN, buff=0.15)
        hum_removed_label.set_opacity(0)

        # =====================================================================
        # BEAT 1: 0.00 – 1.00  Fade in from black, all main elements visible
        # =====================================================================
        black_overlay = Rectangle(width=14, height=8,
                                  fill_color=BLACK, fill_opacity=1,
                                  stroke_width=0)
        black_overlay.move_to(ORIGIN)
        self.add(black_overlay)

        self.play(FadeOut(black_overlay), run_time=max(0.05, 0.5))
        self.add(head_outline, electrodes, socket_group, monitor_group,
                 interference_group)
        self.wait(max(0.05, 0.5))  # fully visible by 1.0 s

        # =====================================================================
        # BEAT 2: 2.30 – 3.52  Notch symbols appear one-by-one, interference starts to fade
        # =====================================================================
        self.wait(max(0.05, 2.30 - self.renderer.time))

        notch_duration = 0.5  # 2.62 - 2.30 = 0.32, but 0.5 as per brief
        for i, sym in enumerate(notch_symbols):
            sym.set_opacity(1)
            self.play(
                FadeIn(sym, scale=0.9),
                run_time=max(0.05, notch_duration / len(notch_symbols))
            )

        # Pulsing softly after all appear
        def pulse_notch(m, dt):
            if not hasattr(pulse_notch, "time"):
                pulse_notch.time = 0
            pulse_notch.time += dt
            for s in notch_symbols:
                scale = 1 + 0.05 * np.sin(pulse_notch.time * 4)
                s.set_stroke(width=2 * scale)

        notch_symbols.add_updater(pulse_notch)
        interference_group.set_opacity(0.7)
        self.play(interference_group.animate.set_opacity(0.3),
                  run_time=max(0.05, 3.52 - 2.62))
        self.wait(max(0.05, 3.52 - self.renderer.time))

        # =====================================================================
        # BEAT 3: 3.52 – 6.22  Interference vanishes, monitor illuminates
        # =====================================================================
        interference_group.clear_updaters()
        self.play(
            interference_group.animate.set_opacity(0),
            run_time=max(0.05, 5.46 - 3.52)
        )

        # Monitor shows clean EEG
        clean_eeg.set_opacity(1)
        self.play(FadeIn(clean_eeg), FadeIn(filtered_label),
                  run_time=max(0.05, 0.8))
        self.wait(max(0.05, 6.22 - self.renderer.time))

        # =====================================================================
        # BEAT 4: 6.22 – 9.30  Glow on head, spectrum appears, spikes, collapse
        # =====================================================================
        # Soft glow on head outline
        glow = head_outline.copy().set_color(YELLOW).set_stroke(width=12).set_opacity(0)
        self.add(glow)
        self.play(glow.animate.set_opacity(0.5), run_time=max(0.05, 0.4))
        self.play(glow.animate.set_opacity(0), run_time=max(0.05, 0.4))

        # Spectrum fades in
        spectrum.set_opacity(1)
        hum_label.set_opacity(1)
        hum60_label.set_opacity(1)
        self.play(FadeIn(spectrum), FadeIn(hum_label), FadeIn(hum60_label),
                  run_time=max(0.05, 1.0))

        # Spikes present (already drawn), then collapse at 7.46–9.08
        self.wait(max(0.05, 7.46 - self.renderer.time))

        # Collapse spikes
        target_spike50 = Line(
            spectrum[0].c2p(50, 0.1),
            spectrum[0].c2p(50, 0.1),
            color=RED, stroke_width=4
        )
        target_spike60 = Line(
            spectrum[0].c2p(60, 0.1),
            spectrum[0].c2p(60, 0.1),
            color=RED, stroke_width=4
        )

        # Add V-shaped notch visually: new spectrum curve with dips
        def notched_curve(x):
            base = 0.1 + 0.02 * np.sin(0.15 * x)
            if 48 < x < 52:
                base -= 0.6 * np.exp(-((x - 50) / 2) ** 2)
            if 58 < x < 62:
                base -= 0.4 * np.exp(-((x - 60) / 2) ** 2)
            return max(0.0, base)

        notched_bg = spectrum[0].plot(
            notched_curve,
            x_range=[0, 100],
            color=GREY, stroke_width=2.5
        )

        self.play(
            Transform(spectrum[2], target_spike50),
            Transform(spectrum[3], target_spike60),
            Transform(spectrum[1], notched_bg),
            FadeOut(hum_label),
            FadeOut(hum60_label),
            FadeIn(hum_removed_label),
            run_time=max(0.05, 9.08 - 7.46)
        )

        # Pulse notch symbols in unison
        for sym in notch_symbols:
            self.play(sym.animate.scale(1.15), run_time=max(0.05, 0.25))
            self.play(sym.animate.scale(1 / 1.15), run_time=max(0.05, 0.25))

        self.wait(max(0.05, 9.30 - self.renderer.time))

        # =====================================================================
        # BEAT 5: 9.30 – 12.30  Highlight notch zone with yellow circle
        # =====================================================================
        yellow_highlight = Circle(
            radius=0.25, color=YELLOW, stroke_width=3, fill_opacity=0.2
        )
        yellow_highlight.move_to(spectrum[0].c2p(50, 0.3))

        yellow_highlight2 = yellow_highlight.copy()
        yellow_highlight2.move_to(spectrum[0].c2p(60, 0.2))

        self.play(FadeIn(yellow_highlight), FadeIn(yellow_highlight2),
                  run_time=max(0.05, 0.5))
        # Hold while narrator speaks
        self.wait(max(0.05, 12.30 - self.renderer.time))

        self.play(FadeOut(yellow_highlight), FadeOut(yellow_highlight2),
                  run_time=max(0.05, 0.5))

        # =====================================================================
        # BEAT 6: 12.30 – 15.18  Spectrum fades, label appears on electrode, then fades
        # =====================================================================
        self.play(FadeOut(spectrum), FadeOut(hum_removed_label),
                  run_time=max(0.05, 1.5))

        self.wait(max(0.05, 12.64 - self.renderer.time))
        scalp_label = Text("Scalp recording", font_size=18, color=WHITE, weight="BOLD")
        scalp_label.next_to(electrode_positions["Cz"], UP * 0.5)
        arrow_to_electrode = Arrow(
            scalp_label.get_bottom() + DOWN * 0.05,
            electrode_positions["Cz"],
            color=WHITE, stroke_width=2, buff=0.1
        )
        self.play(FadeIn(scalp_label), GrowArrow(arrow_to_electrode), run_time=max(0.05, 0.6))
        self.wait(max(0.05, 13.96 - self.renderer.time))
        self.play(FadeOut(scalp_label), FadeOut(arrow_to_electrode), run_time=max(0.05, 0.4))
        self.wait(max(0.05, 15.18 - self.renderer.time))

        # =====================================================================
        # BEAT 7: 15.18 – 17.50  Zoom into Cz electrode
        # =====================================================================
        cz_electrode_pos = electrode_positions["Cz"]
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.25).move_to(cz_electrode_pos),
            run_time=max(0.05, 2.3)
        )

        voltage_text = Text("~10 µV", font_size=28, color=GREEN, weight="BOLD")
        voltage_text.next_to(electrodes[1], RIGHT, buff=0.5)
        voltage_text.set_opacity(0)

        # Faint, clean neural waveform near electrode
        neural_waveform = VMobject(stroke_color=GREEN, stroke_width=2, fill_opacity=0)
        wpts = []
        for t in np.linspace(0, 2 * PI, 100):
            wpts.append(np.array([t * 0.3, 0.2 * np.sin(t * 2.5), 0]))
        neural_waveform.set_points_as_corners(wpts)
        neural_waveform.move_to(electrodes[1].get_center() + RIGHT * 1.0)
        neural_waveform.set_opacity(0)

        self.play(
            FadeIn(voltage_text),
            FadeIn(neural_waveform),
            run_time=max(0.05, 0.8
        ))
        self.wait(max(0.05, 17.50 - self.renderer.time))

        # =====================================================================
        # BEAT 8: 17.50 – 20.20  Interference re-extends, distorts waveform
        # =====================================================================
        # Re-insert interference lines from socket
        interference_group.set_opacity(0.2)
        self.play(interference_group.animate.set_opacity(0.5), run_time=max(0.05, 0.8))

        # Waveform gets noisy overlay
        noisy_overlay = neural_waveform.copy().set_color(RED).set_stroke(width=4)
        self.play(FadeIn(noisy_overlay), run_time=max(0.05, 0.5))

        # Voltage flickers to noisy
        voltage_noisy = Text("~12 µV (noisy)", font_size=28, color=RED, weight="BOLD")
        voltage_noisy.move_to(voltage_text.get_center())
        self.play(ReplacementTransform(voltage_text, voltage_noisy), run_time=max(0.05, 0.5))

        # Annotation bottom of frame
        annot_text = Text("Electromagnetic noise from the room",
                          font_size=22, color=YELLOW, weight="BOLD")
        annot_text.to_edge(DOWN, buff=0.8)
        annot_arrow = Arrow(
            annot_text.get_top(),
            interference_group.get_bottom(),
            color=YELLOW, stroke_width=2
        )
        self.play(FadeIn(annot_text), GrowArrow(annot_arrow), run_time=max(0.05, 0.8))
        self.wait(max(0.05, 20.20 - self.renderer.time))

        # =====================================================================
        # BEAT 9: 20.20 – 22.44  Interference fades, voltage stabilises, zoom out
        # =====================================================================
        # Pulse interference brighter once
        self.play(interference_group.animate.set_opacity(0.7), run_time=max(0.05, 0.2))
        self.play(interference_group.animate.set_opacity(0.1), run_time=max(0.05, 0.3))

        # Voltage stabilises
        voltage_stable = Text("~10.1 µV", font_size=28, color=GREEN, weight="BOLD")
        voltage_stable.move_to(voltage_noisy.get_center())
        self.play(ReplacementTransform(voltage_noisy, voltage_stable), run_time=max(0.05, 0.5))

        # Dim annotation
        self.play(annot_text.animate.set_opacity(0.4),
                  annot_arrow.animate.set_opacity(0.4), run_time=max(0.05, 0.5))

        # Clean waveform back
        self.play(FadeOut(noisy_overlay), run_time=max(0.05, 0.3))

        # Zoom out to full scene
        self.play(
            self.camera.frame.animate.restore(),
            run_time=max(0.05, 22.44 - self.renderer.time)
        )

        # =====================================================================
        # BEAT 10: 22.44 – 23.15 Hold full scene
        # =====================================================================
        self.wait(max(0.05, 23.15 - self.renderer.time))