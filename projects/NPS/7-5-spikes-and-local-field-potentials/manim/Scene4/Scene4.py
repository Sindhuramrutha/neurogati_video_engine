ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *
import numpy as np


class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"
        rt = lambda t: max(0.05, t)

        SHARED_Y = 2.0
        ELECTRODE_TIP = np.array([-4.8, SHARED_Y, 0])

        # ---------- Electrode tip ----------
        shaft = Line(
            np.array([-7.0, SHARED_Y, 0]),
            ELECTRODE_TIP,
            color=GREY_B,
            stroke_width=6,
        )
        tip = Polygon(
            ELECTRODE_TIP + LEFT * 0.08 + UP * 0.08,
            ELECTRODE_TIP + LEFT * 0.08 + DOWN * 0.08,
            ELECTRODE_TIP + RIGHT * 0.30,
            color=GREY_B,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0,
        )
        electrode_group = VGroup(shaft, tip)

        def make_neuron(center, color):
            soma = Circle(
                radius=0.28,
                fill_color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=2,
            ).move_to(center)

            dendrites = VGroup()
            directions = [
                UP + RIGHT,
                RIGHT + DOWN * 0.6,
                DOWN + LEFT * 0.3,
                LEFT + UP * 0.5,
            ]
            for d in directions:
                d = np.array(d)
                d = d / np.linalg.norm(d)
                dendrites.add(
                    Line(
                        soma.get_center() + d * 0.28,
                        soma.get_center() + d * 0.55,
                        color=color,
                        stroke_width=3,
                    )
                )
            return VGroup(soma, dendrites)

        red_neuron = make_neuron(np.array([-3.9, SHARED_Y + 0.9, 0]), RED)
        blue_neuron = make_neuron(np.array([-3.7, SHARED_Y + 0.1, 0]), BLUE)
        green_neuron = make_neuron(np.array([-3.9, SHARED_Y - 0.7, 0]), GREEN)
        neuron_groups = [red_neuron, blue_neuron, green_neuron]

        # 0.00 - 3.80
        self.play(Create(electrode_group), run_time=max(0.05, rt(1.4)))
        self.play(
            LaggedStart(
                GrowFromCenter(red_neuron),
                GrowFromCenter(blue_neuron),
                GrowFromCenter(green_neuron),
                lag_ratio=0.35,
            ),
            run_time=max(0.05, rt(2.0)),
        )
        self.wait(max(0.05, rt(0.4)))

        # gap 3.80 - 4.60
        self.wait(max(0.05, rt(0.80)))

        # ---------- Shared recorded trace ----------
        trace_panel = Rectangle(
            width=10.8,
            height=1.6,
            stroke_color=GREY,
            fill_color=GREY_E,
            fill_opacity=0.12,
        ).move_to(np.array([0.35, SHARED_Y, 0]))

        trace_base = Line(
            np.array([-4.8, SHARED_Y, 0]),
            np.array([5.6, SHARED_Y, 0]),
            color=GREY_A,
            stroke_width=2.5,
        )

        recorded_label = Text("recorded signal", font_size=22, color=WHITE)
        recorded_label.set_opacity(0.5)
        recorded_label.move_to(np.array([-0.5, SHARED_Y + 0.55, 0]))

        self.play(FadeIn(trace_panel), Create(trace_base), run_time=max(0.05, rt(0.85)))
        self.play(FadeIn(recorded_label), run_time=max(0.05, rt(0.43)))

        # ---------- Spike waveforms ----------
        def make_spike_path(center_x, width, amp, color, biphasic=False, y=SHARED_Y):
            total_width = width * 2.2

            def point(t):
                s = t * 2 - 1
                x = center_x + s * total_width * 0.5
                if biphasic:
                    v = -amp * np.exp(-((s / 0.55) ** 2)) * np.cos(2.4 * s)
                else:
                    v = -amp * np.exp(-((s / 0.5) ** 2))
                return np.array([x, y + v, 0])

            p = ParametricFunction(
                point,
                t_range=[0, 1, 0.01],
                color=color,
                stroke_width=4,
            )
            p.set_opacity(0)
            return p

        spike_data = {
            "red": {
                "centers": [-1.6, 0.9, 3.2],
                "width": 0.30,
                "amp": 0.58,
                "biphasic": False,
                "color": RED,
            },
            "blue": {
                "centers": [-0.5, 2.4, 4.5],
                "width": 0.50,
                "amp": 0.48,
                "biphasic": True,
                "color": BLUE,
            },
            "green": {
                "centers": [0.4, 3.0, 5.0],
                "width": 0.60,
                "amp": 0.30,
                "biphasic": False,
                "color": GREEN,
            },
        }

        shared_spikes = {}
        all_spike_paths = []
        for key, spec in spike_data.items():
            paths = []
            for cx in spec["centers"]:
                p = make_spike_path(
                    cx,
                    spec["width"],
                    spec["amp"],
                    spec["color"],
                    spec["biphasic"],
                    SHARED_Y,
                )
                paths.append(p)
                all_spike_paths.append(p)
            shared_spikes[key] = paths

        self.add(*all_spike_paths)
        trace_mobjects = [trace_panel, trace_base, *all_spike_paths]

        def fire_neuron(neuron_group, spike_path, color, total):
            pulse = Dot(
                neuron_group.get_center(),
                radius=0.07,
                color=YELLOW,
                fill_opacity=1,
            )
            target = neuron_group.get_center() + (
                ELECTRODE_TIP - neuron_group.get_center()
            ) * 0.72

            t1 = total * 0.22
            t2 = total * 0.68
            t3 = total * 0.10

            self.play(
                Indicate(neuron_group, color=YELLOW, scale_factor=1.2),
                FadeIn(pulse),
                run_time=max(0.05, rt(t1)),
            )
            self.play(
                pulse.animate.move_to(target),
                spike_path.animate.set_opacity(1),
                run_time=max(0.05, rt(t2)),
            )
            self.play(FadeOut(pulse), run_time=max(0.05, rt(t3)))

        # gap 5.88 - 6.14
        self.wait(max(0.05, rt(0.26)))

        # 6.14 - 8.12: red then blue fire
        fire_neuron(red_neuron, shared_spikes["red"][0], RED, 0.65)
        self.wait(max(0.05, rt(0.33)))
        fire_neuron(blue_neuron, shared_spikes["blue"][0], BLUE, 0.65)
        self.wait(max(0.05, rt(0.35)))

        # 8.12 - 9.00: green fires and the trace becomes a messy mixture
        fire_neuron(green_neuron, shared_spikes["green"][0], GREEN, 0.50)

        extra_spikes = VGroup(
            *shared_spikes["red"][1:],
            *shared_spikes["blue"][1:],
            *shared_spikes["green"][1:],
        )
        self.play(extra_spikes.animate.set_opacity(1), run_time=max(0.05, rt(0.38)))

        # gap 9.00 - 9.84
        self.wait(max(0.05, rt(0.84)))

        # 9.84 - 12.22: title
        title = Text("spike sorting", font_size=58, color=YELLOW)
        title.to_edge(UP, buff=0.25)
        self.play(AddTextLetterByLetter(title), run_time=max(0.05, rt(1.5)))
        self.wait(max(0.05, rt(0.88)))

        # ---------- Detection threshold ----------
        threshold_y = SHARED_Y - 0.25
        threshold_line = DashedLine(
            np.array([-4.7, threshold_y, 0]),
            np.array([5.6, threshold_y, 0]),
            color=GREY_B,
            dash_length=0.15,
            stroke_width=3,
        )

        # ---------- Three sorted rows below ----------
        row_y_positions = [0.15, -0.75, -1.65]
        row_x_min = -1.2
        row_x_max = 6.0
        row_width = 7.2
        row_height = 0.85
        slot_xs = [1.3, 2.8, 4.3]

        rows = []
        for i, key in enumerate(["red", "blue", "green"]):
            color = spike_data[key]["color"]
            y = row_y_positions[i]

            panel = Rectangle(
                width=row_width,
                height=row_height,
                stroke_color=GREY,
                fill_color=color,
                fill_opacity=0.10,
            ).move_to(np.array([(row_x_min + row_x_max) / 2, y, 0]))

            baseline = Line(
                np.array([row_x_min + 0.25, y, 0]),
                np.array([row_x_max - 0.25, y, 0]),
                color=GREY,
                stroke_width=1.5,
            )

            template = make_spike_path(
                -0.2,
                spike_data[key]["width"],
                spike_data[key]["amp"],
                color,
                spike_data[key]["biphasic"],
                y=y,
            ).set_opacity(1)

            markers = []
            for sx in slot_xs:
                marker = Line(
                    np.array([sx, y - 0.18, 0]),
                    np.array([sx, y + 0.18, 0]),
                    color=color,
                    stroke_width=5,
                )
                marker.set_opacity(0)
                markers.append(marker)

            row_group = VGroup(panel, baseline, template)
            rows.append(
                {
                    "group": row_group,
                    "panel": panel,
                    "markers": markers,
                    "row_y": y,
                    "color": color,
                    "key": key,
                }
            )

        rows_vgroup = VGroup(*[r["group"] for r in rows])
        self.add(*(m for row in rows for m in row["markers"]))

        # 12.22 - 15.80: threshold appears, trace scrolls, rows separate
        self.play(
            Create(threshold_line),
            *[m.animate.shift(LEFT * 0.45) for m in trace_mobjects],
            run_time=max(0.05, rt(0.9)),
        )
        self.play(
            *[m.animate.shift(RIGHT * 0.45) for m in trace_mobjects],
            run_time=max(0.05, rt(0.9)),
        )
        self.play(FadeIn(rows_vgroup), run_time=max(0.05, rt(1.2)))
        self.play(
            Indicate(rows[0]["group"], color=RED, scale_factor=1.04),
            Indicate(rows[1]["group"], color=BLUE, scale_factor=1.04),
            Indicate(rows[2]["group"], color=GREEN, scale_factor=1.04),
            run_time=max(0.05, rt(0.58)),
        )

        # ---------- Assignment animation ----------
        def assign_spike(key, idx, marker, total):
            color = spike_data[key]["color"]
            cx = spike_data[key]["centers"][idx]
            orig_path = shared_spikes[key][idx]

            start = np.array([cx, SHARED_Y, 0])
            end = marker.get_center()
            dot = Dot(start, radius=0.06, color=color, fill_opacity=1)

            t1 = total * 0.25
            t2 = total * 0.75
            self.play(
                Indicate(orig_path, color=YELLOW, scale_factor=1.25),
                FadeIn(dot),
                run_time=max(0.05, rt(t1)),
            )
            self.play(
                dot.animate.move_to(end),
                marker.animate.set_opacity(1),
                run_time=max(0.05, rt(t2)),
            )

        # 15.80 - 18.32: first assignment for each neuron
        beat7_per = 2.52 / 3
        for i, key in enumerate(["red", "blue", "green"]):
            assign_spike(key, 0, rows[i]["markers"][0], beat7_per)

        # gap 18.32 - 18.90
        self.wait(max(0.05, rt(0.58)))

        # row labels
        neuron_labels = []
        label_names = ["neuron 1", "neuron 2", "neuron 3"]
        for i, row in enumerate(rows):
            label = Text(label_names[i], font_size=26, color=row["color"])
            label.next_to(row["panel"], LEFT, buff=0.30)
            neuron_labels.append(label)

        self.play(*[FadeIn(lbl) for lbl in neuron_labels], run_time=max(0.05, rt(0.5)))

        # 18.90 - 22.60: complete remaining assignments
        beat8_per = 3.20 / 6
        for i, key in enumerate(["red", "blue", "green"]):
            for idx in [1, 2]:
                assign_spike(key, idx, rows[i]["markers"][idx], beat8_per)

        # gap 22.60 - 23.66
        self.wait(max(0.05, rt(1.06)))

        # ---------- Processing pipeline ----------
        start_y = trace_panel.get_bottom()[1] - 0.12
        end_y = rows_vgroup.get_top()[1] + 0.10
        processing_arrow = Arrow(
            np.array([0.8, start_y, 0]),
            np.array([0.8, end_y, 0]),
            color=BLUE,
            stroke_width=5,
            buff=0.0,
            max_tip_length_to_length_ratio=0.20,
        )
        signal_processing_label = Text(
            "signal processing", font_size=30, color=BLUE
        ).next_to(processing_arrow, UP, buff=0.12)

        self.play(GrowArrow(processing_arrow), run_time=max(0.05, rt(0.9)))
        self.play(Write(signal_processing_label), run_time=max(0.05, rt(0.8)))

        pipeline_center = np.array([0.9, 0.7, 0])
        self.play(
            self.camera.frame.animate.scale(1.12).move_to(pipeline_center),
            run_time=max(0.05, rt(1.4)),
        )
        self.wait(max(0.05, rt(0.86)))

        # gap 27.62 - 27.92
        self.wait(max(0.05, rt(0.30)))

        # ---------- Interpretable information ----------
        interpretable_label = Text(
            "interpretable information", font_size=32, color=TEAL
        ).next_to(rows_vgroup, DOWN, buff=0.45)

        self.play(FadeIn(interpretable_label), run_time=max(0.05, rt(0.6)))
        self.play(
            Indicate(rows[0]["group"], color=RED, scale_factor=1.05),
            Indicate(rows[1]["group"], color=BLUE, scale_factor=1.05),
            Indicate(rows[2]["group"], color=GREEN, scale_factor=1.05),
            run_time=max(0.05, rt(1.5)),
        )
        self.wait(max(0.05, rt(0.96)))

        # 30.98 - 31.85: final hold and fade out
        self.wait(max(0.05, rt(0.27)))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=max(0.05, rt(0.60)))