ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

import numpy as np
from manim import *


class Scene0(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # --- Geometry constants ---
        x_left = -6.3
        x_right = 6.3
        t0_x = -2.5
        partial_end = x_left + 0.7 * (x_right - x_left)  # 70 % of the timeline
        upper_onset_x = 0.0
        lower_onsets = [-1.8, 0.3, 2.4]
        upper_row_ys = [0.85, 1.45, 2.05]
        lower_row_ys = [-0.85, -1.45, -2.05]

        upper_color = TEAL
        lower_color = ORANGE

        # --- Burst waveform helper ---
        def make_burst(onset_x, row_y, color):
            amp = 0.35
            sigma = 0.65
            freq = 1.0
            center_offset = 1.6
            x_span = 3.8

            def func(x):
                shifted = x - onset_x
                env = np.where(
                    shifted < 0,
                    0.0,
                    np.exp(-0.5 * ((shifted - center_offset) / sigma) ** 2),
                )
                return row_y + amp * env * np.sin(
                    2 * PI * freq * (shifted - center_offset)
                )

            graph = FunctionGraph(
                func,
                x_range=[onset_x, onset_x + x_span, 0.03],
                color=color,
            )
            graph.set_stroke(color=color, width=3, opacity=0.9)
            return graph

        # --- Beat 1: faint partial timeline ---
        partial_line = Line(
            [x_left, 0, 0],
            [partial_end, 0, 0],
            stroke_color=GREY_B,
            stroke_width=4,
            stroke_opacity=0.45,
        )
        remaining_line = Line(
            [partial_end, 0, 0],
            [x_right, 0, 0],
            stroke_color=WHITE,
            stroke_width=4,
            stroke_opacity=1.0,
        )

        self.wait(max(0.05, 0.20))
        self.play(Create(partial_line), run_time=max(0.05, 0.92))
        self.wait(max(0.05, 0.54))  # gap to 1.66

        # --- Beat 2: full solid timeline, t=0 tick, Stimulus label ---
        self.play(
            Create(remaining_line),
            partial_line.animate.set_color(WHITE).set_stroke(width=4, opacity=1),
            run_time=max(0.05, 1.20),
        )

        tick = Line(
            [t0_x, -0.20, 0],
            [t0_x, 0.20, 0],
            stroke_color=YELLOW,
            stroke_width=5,
            stroke_opacity=1.0,
        )
        stimulus_label = Text(
            "Stimulus", font_size=30, color=YELLOW, weight="BOLD"
        ).next_to(tick, DOWN, buff=0.15)

        self.play(Create(tick), FadeIn(stimulus_label), run_time=max(0.05, 0.60))
        self.wait(max(0.05, 1.36))  # beat total 1.20+0.60+1.36 = 3.16
        self.wait(max(0.05, 0.40))  # gap to 5.22

        # --- Beat 3: upper time-locked bursts ---
        upper_bursts = [
            make_burst(upper_onset_x, row_y, upper_color) for row_y in upper_row_ys
        ]
        upper_group = VGroup(*upper_bursts)

        for i, burst in enumerate(upper_bursts):
            self.play(Create(burst), run_time=max(0.05, 1.20))
            if i < 2:
                self.wait(max(0.05, 0.20))
        self.wait(max(0.05, 1.16))  # beat total 5.16
        self.wait(max(0.05, 1.34))  # gap to 11.72

        # --- Beat 4: guide line slides and upper group pulses in unison ---
        guide_line = Line(
            [t0_x, -1.20, 0],
            [t0_x, 2.90, 0],
            stroke_color=WHITE,
            stroke_width=2,
            stroke_opacity=0.35,
        )
        self.play(
            guide_line.animate.shift(RIGHT * (upper_onset_x - t0_x)),
            run_time=max(0.05, 2.00),
        )

        for _ in range(3):
            self.play(
                upper_group.animate.set_stroke(width=5, opacity=1),
                run_time=max(0.05, 0.70),
            )
            self.play(
                upper_group.animate.set_stroke(width=3, opacity=0.9),
                run_time=max(0.05, 0.70),
            )

        self.play(FadeOut(guide_line), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.92))  # beat total 2.00+4.20+0.40+0.92 = 7.52
        self.wait(max(0.05, 1.56))  # gap to 20.80

        # --- Beat 5: Time-Locked label ---
        time_locked_label = Text(
            "Time-Locked", font_size=40, color=YELLOW, weight="BOLD"
        ).next_to(upper_group, UP, buff=0.35)
        self.play(FadeIn(time_locked_label), run_time=max(0.05, 1.40))
        self.wait(max(0.05, 3.00))  # beat total 4.40

        # --- Beat 6: lower induced bursts ---
        lower_bursts = [
            make_burst(onset_x, row_y, lower_color)
            for onset_x, row_y in zip(lower_onsets, lower_row_ys)
        ]
        lower_group = VGroup(*lower_bursts)

        play_t = 1.50
        wait_t = (6.88 - 3 * play_t) / 3
        for burst in lower_bursts:
            self.play(Create(burst), run_time=max(0.05, play_t))
            self.wait(max(0.05, wait_t))

        self.wait(max(0.05, 0.72))  # gap to 32.80

        # --- Beat 7: sequential lower pulses, dim upper group ---
        self.play(
            upper_group.animate.set_opacity(0.45),
            lower_group.animate.set_opacity(1.0),
            run_time=max(0.05, 0.80),
        )

        delays = [0.10, 0.40, 0.70]
        for delay, burst in zip(delays, lower_bursts):
            self.wait(max(0.05, delay))
            self.play(
                burst.animate.set_stroke(width=5, opacity=1),
                run_time=max(0.05, 0.50),
            )
            self.play(
                burst.animate.set_stroke(width=3, opacity=1),
                run_time=max(0.05, 0.50),
            )

        self.play(lower_group.animate.set_opacity(1.0), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 0.46))  # beat total 0.80+1.20+3.00+0.40+0.46 = 5.86
        self.wait(max(0.05, 0.76))  # gap to 39.42

        # --- Beat 8: Induced label ---
        induced_label = Text(
            "Induced", font_size=40, color=YELLOW, weight="BOLD"
        ).next_to(lower_group, DOWN, buff=0.35)
        self.play(FadeIn(induced_label), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 1.82))  # beat total 3.02

        # --- Beat 9: highlight both concepts in turn ---
        self.play(
            Indicate(
                time_locked_label,
                scale_factor=1.15,
                color=YELLOW,
                run_time=max(0.05, 1.40),
            ),
            upper_group.animate.set_opacity(1.0).set_stroke(width=5, opacity=1.0),
            run_time=max(0.05, 1.40),
        )
        self.play(
            upper_group.animate.set_stroke(width=3, opacity=0.9),
            run_time=max(0.05, 0.40),
        )

        self.play(
            Indicate(
                induced_label,
                scale_factor=1.15,
                color=YELLOW,
                run_time=max(0.05, 1.40),
            ),
            lower_group.animate.set_stroke(width=5, opacity=1.0),
            run_time=max(0.05, 1.40),
        )
        self.play(
            lower_group.animate.set_stroke(width=3, opacity=0.9),
            run_time=max(0.05, 0.40),
        )
        self.wait(max(0.05, 2.20))  # beat total 5.80
        self.wait(max(0.05, 0.91))  # gap to 49.15

        # --- Beat 10: final static comparison ---
        self.wait(max(0.05, 10.30))