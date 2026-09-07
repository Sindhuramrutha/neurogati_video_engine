ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np

ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

class Scene5(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # ---------- palette ----------
        panel_fill = "#162A3A"
        skin = "#E8C39E"
        pink = "#E8A0BF"
        gold = "#FFD700"
        screen_bg = "#0A0A1A"
        trace_colors = {"emg": GREEN, "ecog": TEAL, "lfp": PURPLE}

        # ---------- helpers ----------
        def make_screen(w=2.8, h=0.7):
            return Rectangle(width=w, height=h, fill_color=screen_bg, fill_opacity=1,
                             stroke_color=WHITE, stroke_width=1)

        def make_trace(kind, color, width=2.8, height=0.6):
            trace = VMobject(stroke_color=color, stroke_width=2, fill_opacity=0)
            x = np.linspace(-1.2, 1.2, 400)
            if kind == "emg":
                y = 0.05 * np.sin(2*np.pi*3*x)
                bursts = [(-0.95, -0.75, 0.35, 18),
                          (-0.30, -0.05, 0.45, 22),
                          (0.40, 0.70, 0.30, 20)]
                for x0, x1, amp, freq in bursts:
                    mask = (x >= x0) & (x <= x1)
                    t = (x[mask] - x0) / (x1 - x0)
                    y[mask] += amp * np.sin(2*np.pi*freq*t) * np.sin(np.pi*t)
            elif kind == "ecog":
                y = 0.30*np.sin(2*np.pi*10*x) + 0.10*np.sin(2*np.pi*20*x)
            elif kind == "lfp":
                y = 0.40*np.sin(2*np.pi*4*x) + 0.10*np.sin(2*np.pi*8*x)
            max_abs = max(0.001, np.max(np.abs(y)))
            y = y / max_abs * 0.22
            pts = np.column_stack([x, y, np.zeros_like(x)])
            trace.set_points_smoothly(pts)
            trace.stretch_to_fit_width(width)
            trace.stretch_to_fit_height(height)
            return trace

        def make_ripple(width=2.8, height=0.6, amp=0.12):
            x = np.linspace(-1.2, 1.2, 400)
            y = amp * np.sin(2*np.pi*50*x + 0.5)
            ripple = VMobject(stroke_color=RED, stroke_width=2, fill_opacity=0)
            ripple.set_points_smoothly(np.column_stack([x, y, np.zeros_like(x)]))
            ripple.stretch_to_fit_width(width)
            ripple.stretch_to_fit_height(height)
            ripple.set_opacity(0)
            return ripple

        def make_wavelet():
            w = VMobject(stroke_color=RED, stroke_width=2, fill_opacity=0)
            x = np.linspace(0, 1.0, 70)
            y = 0.25 * np.sin(2*np.pi*2.2*x)
            w.set_points_as_corners(np.column_stack([x, y, np.zeros_like(x)]))
            w.set_opacity(0)
            return w

        def make_notch_symbol():
            circle = Circle(radius=0.18, color=WHITE, stroke_width=2, fill_opacity=0)
            slash = Line(circle.get_corner(DL), circle.get_corner(UR), color=RED, stroke_width=3)
            symbol = VGroup(circle, slash)
            symbol.set_opacity(0)
            return symbol

        def make_pipeline():
            labels = ["Raw", "Notch filter", "Clean"]
            fills = [BLUE, YELLOW, GREEN]
            blocks = VGroup()
            for lab, fill in zip(labels, fills):
                rect = RoundedRectangle(width=1.0, height=0.4, corner_radius=0.08,
                                        fill_color=fill, fill_opacity=0.7 if lab == "Notch filter" else 0.3,
                                        stroke_color=WHITE, stroke_width=1)
                text = Text(lab, font_size=14, color=WHITE, weight="BOLD").move_to(rect.get_center())
                block = VGroup(rect, text)
                blocks.add(block)
            blocks.arrange(RIGHT, buff=0.12)
            return blocks

        # ---------- panel skeletons ----------
        def make_panel_bg(width=3.4, height=4.2):
            return RoundedRectangle(width=width, height=height, corner_radius=0.1,
                                    fill_color=panel_fill, fill_opacity=1,
                                    stroke_color=WHITE, stroke_width=1.5)

        # EMG panel
        emg_rect = make_panel_bg()
        emg_title = Text("Surface EMG", font_size=20, color=WHITE, weight="BOLD")
        arm = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.45,
                               fill_color=skin, fill_opacity=1,
                               stroke_color=WHITE, stroke_width=1.5)
        emg_electrodes = VGroup()
        for dx in [-0.5, 0, 0.5]:
            dot = Dot(point=arm.get_top() + DOWN*0.15 + RIGHT*dx,
                      radius=0.06, color=gold, fill_opacity=1)
            emg_electrodes.add(dot)
        emg_screen = make_screen()
        emg_panel = VGroup(emg_rect, arm, emg_electrodes, emg_screen)

        # ECoG panel
        ecog_rect = make_panel_bg()
        ecog_title = Text("ECoG", font_size=20, color=WHITE, weight="BOLD")
        brain = SVGMobject(ASSET_PATHS["brain"]).set_fill(pink, opacity=1).set_stroke(WHITE, width=1.5)
        brain.scale_to_fit_width(2.2)
        brain.scale_to_fit_height(1.4)
        ecog_grid = VGroup()
        for i in range(3):
            for j in range(2):
                sq = Square(side_length=0.08, fill_color=gold, fill_opacity=1, stroke_width=0.5)
                ecog_grid.add(sq)
        ecog_screen = make_screen()
        ecog_panel = VGroup(ecog_rect, brain, ecog_grid, ecog_screen)

        # LFP panel
        lfp_rect = make_panel_bg()
        lfp_title = Text("Local Field Potential", font_size=20, color=WHITE, weight="BOLD")
        probe = Rectangle(width=0.08, height=1.2, fill_color=GREY_B, fill_opacity=1,
                          stroke_color=WHITE, stroke_width=1)
        tip = Dot(radius=0.05, color=gold, fill_opacity=1).move_to(probe.get_bottom())
        lfp_electrode = VGroup(probe, tip)
        lfp_screen = make_screen()
        lfp_panel = VGroup(lfp_rect, lfp_electrode, lfp_screen)

        # ---------- position panels ----------
        emg_panel.move_to(LEFT*4.2 + UP*0.2)
        ecog_panel.move_to(UP*0.2)
        lfp_panel.move_to(RIGHT*4.2 + UP*0.2)

        # position internals relative to their panels
        arm.move_to(emg_rect.get_center() + UP*0.9)
        emg_electrodes.move_to(arm.get_top() + DOWN*0.15)
        emg_screen.next_to(arm, DOWN, buff=0.45)
        emg_title.next_to(emg_rect, UP, buff=0.15)

        brain.move_to(ecog_rect.get_center() + UP*0.9)
        # grid on brain surface, lower-right area
        grid_center = brain.get_center() + RIGHT*0.5 + DOWN*0.25
        for i in range(3):
            for j in range(2):
                ecog_grid.add(Square(side_length=0.08, fill_color=gold, fill_opacity=1, stroke_width=0.5)
                              .move_to(grid_center + RIGHT*(i-1)*0.25 + DOWN*(j-0.5)*0.2))
        ecog_screen.next_to(brain, DOWN, buff=0.45)
        ecog_title.next_to(ecog_rect, UP, buff=0.15)

        lfp_electrode.move_to(lfp_rect.get_center() + UP*0.9)
        lfp_screen.next_to(lfp_electrode, RIGHT, buff=0.4)
        lfp_title.next_to(lfp_rect, UP, buff=0.15)

        # ---------- traces, wavelets, notch symbols (created after panels positioned) ----------
        emg_clean = make_trace("emg", trace_colors["emg"]).move_to(emg_screen)
        emg_noise = make_ripple().move_to(emg_screen)
        emg_wavelet = make_wavelet().move_to(emg_screen.get_left() + RIGHT*0.3)
        emg_notch = make_notch_symbol().next_to(emg_screen, UP, buff=0.12)

        ecog_clean = make_trace("ecog", trace_colors["ecog"]).move_to(ecog_screen)
        ecog_noise = make_ripple().move_to(ecog_screen)
        ecog_wavelet = make_wavelet().move_to(ecog_screen.get_left() + RIGHT*0.3)
        ecog_notch = make_notch_symbol().next_to(ecog_screen, UP, buff=0.12)

        lfp_clean = make_trace("lfp", trace_colors["lfp"]).move_to(lfp_screen)
        lfp_noise = make_ripple().move_to(lfp_screen)
        lfp_wavelet = make_wavelet().move_to(lfp_screen.get_left() + RIGHT*0.3)
        lfp_notch = make_notch_symbol().next_to(lfp_screen, UP, buff=0.12)

        traces_clean = [emg_clean, ecog_clean, lfp_clean]
        traces_noise = [emg_noise, ecog_noise, lfp_noise]
        notches = [emg_notch, ecog_notch, lfp_notch]
        wavelets = [emg_wavelet, ecog_wavelet, lfp_wavelet]

        # ---------- pipelines, highlights, end glow ----------
        emg_pipeline = make_pipeline().next_to(emg_rect, DOWN, buff=0.25)
        ecog_pipeline = make_pipeline().next_to(ecog_rect, DOWN, buff=0.25)
        lfp_pipeline = make_pipeline().next_to(lfp_rect, DOWN, buff=0.25)
        pipelines = [emg_pipeline, ecog_pipeline, lfp_pipeline]
        for p in pipelines:
            p.set_opacity(0)

        center_highlight = SurroundingRectangle(ecog_rect, color=YELLOW, stroke_width=4, buff=0.12)
        right_highlight = SurroundingRectangle(lfp_rect, color=BLUE, stroke_width=2, buff=0.10)
        center_highlight.set_opacity(0)
        right_highlight.set_opacity(0)

        clean_glows = VGroup()
        for p in pipelines:
            clean_block = p[2]
            glow = SurroundingRectangle(clean_block, color=YELLOW, stroke_width=3, buff=0.08)
            glow.set_opacity(0)
            clean_glows.add(glow)

        # ---------- fade from black + panel sequence ----------
        black_overlay = Rectangle(width=14, height=8, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        black_overlay.move_to(ORIGIN)
        self.add(black_overlay)

        # left panel appears while fading from black
        self.play(FadeOut(black_overlay), FadeIn(emg_panel), FadeIn(emg_title),
                  run_time=max(0.05, 0.48))
        self.play(FadeIn(ecog_panel), FadeIn(ecog_title), run_time=max(0.05, 0.48))
        self.play(FadeIn(lfp_panel), FadeIn(lfp_title), run_time=max(0.05, 0.48))

        # ---------- beat 2: traces draw (1.44-2.64) ----------
        self.play(
            LaggedStart(
                Create(emg_clean), FadeIn(emg_noise),
                Create(ecog_clean), FadeIn(ecog_noise),
                Create(lfp_clean), FadeIn(lfp_noise),
                lag_ratio=0.4
            ),
            run_time=max(0.05, 1.2
        ))

        # ---------- beat 3: ripple pulse + interference wash (2.64-4.84) ----------
        self.play(
            emg_noise.animate.set_stroke(width=3),
            ecog_noise.animate.set_stroke(width=3),
            lfp_noise.animate.set_stroke(width=3),
            run_time=max(0.05, 0.1
        ))
        self.play(
            emg_noise.animate.set_stroke(width=2),
            ecog_noise.animate.set_stroke(width=2),
            lfp_noise.animate.set_stroke(width=2),
            run_time=max(0.05, 0.1
        ))

        self.play(
            emg_wavelet.animate.set_opacity(0.8).shift(RIGHT*2.8),
            ecog_wavelet.animate.set_opacity(0.8).shift(RIGHT*2.8),
            lfp_wavelet.animate.set_opacity(0.8).shift(RIGHT*2.8),
            emg_clean.animate.set_opacity(0.45),
            ecog_clean.animate.set_opacity(0.45),
            lfp_clean.animate.set_opacity(0.45),
            run_time=max(0.05, 1.0
        ))
        self.play(FadeOut(emg_wavelet), FadeOut(ecog_wavelet), FadeOut(lfp_wavelet),
                  run_time=max(0.05, 0.5))
        self.wait(max(0.05, 0.5))

        # ---------- gap before notch symbols ----------
        self.wait(max(0.05, 0.8))

        # ---------- beat 4: notch symbols appear (5.64-6.14) ----------
        self.play(
            FadeIn(emg_notch), Rotate(emg_notch, angle=2*PI, about_point=emg_notch.get_center()),
            FadeIn(ecog_notch), Rotate(ecog_notch, angle=2*PI, about_point=ecog_notch.get_center()),
            FadeIn(lfp_notch), Rotate(lfp_notch, angle=2*PI, about_point=lfp_notch.get_center()),
            run_time=max(0.05, 0.5
        ))

        # ---------- beat 5: pulse + attenuation (6.14-9.90) ----------
        self.play(
            emg_notch.animate.scale(1.2),
            ecog_notch.animate.scale(1.2),
            lfp_notch.animate.scale(1.2),
            run_time=max(0.05, 0.2
        ))
        self.play(
            emg_notch.animate.scale(1/1.2),
            ecog_notch.animate.scale(1/1.2),
            lfp_notch.animate.scale(1/1.2),
            run_time=max(0.05, 0.2
        ))

        # ripple fades, clean signals return
        self.play(
            emg_noise.animate.set_opacity(0),
            ecog_noise.animate.set_opacity(0),
            lfp_noise.animate.set_opacity(0),
            emg_clean.animate.set_opacity(1),
            ecog_clean.animate.set_opacity(1),
            lfp_clean.animate.set_opacity(1),
            run_time=max(0.05, 3.36
        ))

        # ---------- beat 6: notch pulse + settle glow (9.90-11.92) ----------
        self.play(
            emg_notch.animate.scale(1.15),
            ecog_notch.animate.scale(1.15),
            lfp_notch.animate.scale(1.15),
            run_time=max(0.05, 0.2
        ))
        self.play(
            emg_notch.animate.scale(1/1.15),
            ecog_notch.animate.scale(1/1.15),
            lfp_notch.animate.scale(1/1.15),
            run_time=max(0.05, 0.2
        ))
        self.play(
            emg_notch.animate.set_stroke(width=4, color=YELLOW),
            ecog_notch.animate.set_stroke(width=4, color=YELLOW),
            lfp_notch.animate.set_stroke(width=4, color=YELLOW),
            run_time=max(0.05, 0.3
        ))
        for sym in notches:
            sym[0].set_fill(YELLOW, opacity=0.15)
        self.wait(max(0.05, 1.32))

        # ---------- beat 7: highlight ECoG and LFP (11.92-15.82) ----------
        self.play(FadeIn(center_highlight), FadeIn(right_highlight), run_time=max(0.05, 0.5))
        self.wait(max(0.05, 3.4))

        # ---------- beat 8: better signal quality + enlarged traces (16.10-18.98) ----------
        better_text = Text("Better signal quality", font_size=20, color=WHITE, weight="BOLD")
        better_text.to_edge(DOWN, buff=0.9)
        arrow_ecog = Arrow(better_text.get_top() + RIGHT*0.5,
                           ecog_rect.get_bottom() + DOWN*0.05,
                           color=WHITE, stroke_width=2, buff=0.1)
        arrow_lfp = Arrow(better_text.get_top() + LEFT*0.5,
                          lfp_rect.get_bottom() + DOWN*0.05,
                          color=WHITE, stroke_width=2, buff=0.1)
        better_text.set_opacity(0)
        arrow_ecog.set_opacity(0)
        arrow_lfp.set_opacity(0)

        self.play(
            ecog_clean.animate.scale(1.15),
            lfp_clean.animate.scale(1.15),
            FadeIn(better_text),
            FadeIn(arrow_ecog),
            FadeIn(arrow_lfp),
            run_time=max(0.05, 0.5
        ))
        self.wait(max(0.05, 0.5))
        self.play(
            ecog_clean.animate.scale(1/1.15),
            lfp_clean.animate.scale(1/1.15),
            run_time=max(0.05, 0.5
        ))
        self.wait(max(0.05, 1.38))

        # ---------- beat 9: interference returns in ECoG/LFP, text fades (18.98-20.80) ----------
        ecog_wavelet.move_to(ecog_screen.get_left() + RIGHT*0.3).set_opacity(0)
        lfp_wavelet.move_to(lfp_screen.get_left() + RIGHT*0.3).set_opacity(0)

        self.play(
            ecog_wavelet.animate.set_opacity(0.8).shift(RIGHT*2.8),
            lfp_wavelet.animate.set_opacity(0.8).shift(RIGHT*2.8),
            ecog_noise.animate.set_opacity(0.8),
            lfp_noise.animate.set_opacity(0.8),
            ecog_clean.animate.set_opacity(0.7),
            lfp_clean.animate.set_opacity(0.7),
            better_text.animate.set_opacity(0.3),
            arrow_ecog.animate.set_opacity(0.3),
            arrow_lfp.animate.set_opacity(0.3),
            run_time=max(0.05, 1.0
        ))
        self.play(FadeOut(ecog_wavelet), FadeOut(lfp_wavelet), run_time=max(0.05, 0.5))
        self.play(FadeOut(better_text), FadeOut(arrow_ecog), FadeOut(arrow_lfp),
                  run_time=max(0.05, 0.32))

        # ---------- wait before final sweep ----------
        self.wait(max(0.05, 1.18))

        # ---------- beat 10: final notch pulse + white sweep (21.98-23.70) ----------
        self.play(
            emg_notch.animate.scale(1.15),
            ecog_notch.animate.scale(1.15),
            lfp_notch.animate.scale(1.15),
            run_time=max(0.05, 0.12
        ))
        self.play(
            emg_notch.animate.scale(1/1.15),
            ecog_notch.animate.scale(1/1.15),
            lfp_notch.animate.scale(1/1.15),
            run_time=max(0.05, 0.12
        ))

        white_wave = Rectangle(width=0.12, height=3.2, fill_color=WHITE, fill_opacity=0.9, stroke_width=0)
        white_wave.move_to(emg_panel.get_left() + LEFT*0.5)
        white_wave.set_z_index(5)
        self.play(
            white_wave.animate.move_to(lfp_panel.get_right() + RIGHT*0.5),
            ecog_noise.animate.set_opacity(0),
            lfp_noise.animate.set_opacity(0),
            ecog_clean.animate.set_opacity(1),
            lfp_clean.animate.set_opacity(1),
            run_time=max(0.05, 1.48
        ))
        self.remove(white_wave)

        # ---------- wait then pipelines (23.70-27.34) ----------
        self.wait(max(0.05, 0.38))
        self.play(
            FadeIn(emg_pipeline),
            FadeIn(ecog_pipeline),
            FadeIn(lfp_pipeline),
            run_time=max(0.05, 1.0
        ))
        self.wait(max(0.05, 2.26))

        # ---------- beat 12: final brighten + clean glow (27.34-28.52) ----------
        self.play(
            emg_clean.animate.set_stroke(width=4, color=WHITE),
            ecog_clean.animate.set_stroke(width=4, color=WHITE),
            lfp_clean.animate.set_stroke(width=4, color=WHITE),
            FadeIn(clean_glows),
            run_time=max(0.05, 0.6
        ))
        self.wait(max(0.05, 0.58))