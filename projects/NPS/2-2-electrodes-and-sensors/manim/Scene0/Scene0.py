ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *

class Scene0(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Build the five-block acquisition chain from the previous scene
        block_names = ["Electrode / Sensor", "Amplifier", "Filter",
                       "Digitizer", "Recording System"]
        block_colors = [BLUE, TEAL, GREEN, ORANGE, PURPLE]
        block_w = 2.2
        block_h = 1.0
        gap = 0.45

        blocks = []
        rects = []
        for name, color in zip(block_names, block_colors):
            rect = Rectangle(
                width=block_w,
                height=block_h,
                fill_color=color,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=2
            )
            label = Text(name, font_size=18, weight="BOLD", color=WHITE)
            label.move_to(rect.get_center())
            block = VGroup(rect, label)
            blocks.append(block)
            rects.append(rect)

        start_x = -(len(blocks) - 1) * (block_w + gap) / 2
        for i, block in enumerate(blocks):
            block.move_to(RIGHT * (start_x + i * (block_w + gap)))

        chain_arrows = []
        for i in range(len(blocks) - 1):
            chain_arrows.append(
                Arrow(
                    blocks[i].get_right(),
                    blocks[i + 1].get_left(),
                    buff=0.10,
                    color=WHITE,
                    stroke_width=4
                )
            )

        chain = VGroup(*blocks, *chain_arrows)
        self.add(chain)

        # 0.00 - 5.80: recall the common acquisition chain
        self.wait(max(0.05, 5.80))

        first_block = blocks[0]
        first_rect = rects[0]
        downstream_blocks = VGroup(*blocks[1:])

        # 5.80 - 6.58 gap
        self.wait(max(0.05, 0.78))

        # 6.58 - 9.86: spotlight the electrode/sensor block
        glow_rect = SurroundingRectangle(
            first_block,
            color=YELLOW,
            buff=0.15,
            stroke_width=8,
            fill_opacity=0
        )
        self.play(
            GrowFromCenter(glow_rect),
            first_rect.animate.set_stroke(YELLOW, width=4),
            downstream_blocks.animate.set_opacity(0.3),
            run_time=max(0.05, 0.70
        ))
        # One subtle border pulse when the electrode is named
        self.play(
            glow_rect.animate.scale(1.08).set_stroke(width=12),
            run_time=max(0.05, 0.35
        ))
        self.play(
            glow_rect.animate.scale(1 / 1.08).set_stroke(width=8),
            run_time=max(0.05, 0.35
        ))
        self.wait(max(0.05, 1.88))

        # 9.86 - 11.50 gap
        self.wait(max(0.05, 1.64))

        # Build four recording-method labels above the first block
        method_names = ["EEG", "EMG", "ECoG", "MEG"]
        method_dxs = [-0.9, -0.3, 0.3, 0.9]
        method_labels = []
        method_arrows = []
        for name, dx in zip(method_names, method_dxs):
            lab = Text(name, font_size=20, weight="BOLD", color=YELLOW)
            lab.move_to(first_rect.get_top() + RIGHT * dx + UP * 0.9)
            arrow = Arrow(
                lab.get_bottom(),
                first_rect.get_top() + RIGHT * dx,
                buff=0.08,
                color=WHITE,
                stroke_width=2
            )
            method_labels.append(lab)
            method_arrows.append(arrow)

        method_group = VGroup(*method_labels, *method_arrows)

        # 11.50 - 15.04: labels appear one at a time
        self.play(
            FadeIn(method_labels[0]), Create(method_arrows[0]),
            glow_rect.animate.set_stroke(width=9),
            first_rect.animate.set_stroke(YELLOW, width=5),
            run_time=max(0.05, 0.50
        ))
        self.wait(max(0.05, 1.06))

        self.play(
            FadeIn(method_labels[1]), Create(method_arrows[1]),
            glow_rect.animate.set_stroke(width=10),
            first_rect.animate.set_stroke(YELLOW, width=6),
            run_time=max(0.05, 0.50
        ))
        self.wait(max(0.05, 0.34))

        self.play(
            FadeIn(method_labels[2]), Create(method_arrows[2]),
            glow_rect.animate.set_stroke(width=11),
            first_rect.animate.set_stroke(YELLOW, width=7),
            run_time=max(0.05, 0.40
        ))
        self.wait(max(0.05, 0.48))

        self.play(
            FadeIn(method_labels[3]), Create(method_arrows[3]),
            glow_rect.animate.set_stroke(width=12),
            first_rect.animate.set_stroke(YELLOW, width=8),
            run_time=max(0.05, 0.26
        ))

        # 15.04 - 15.52 gap
        self.wait(max(0.05, 0.48))

        # 15.52 - 19.92: pulses travel down each arrow into the first block
        for arrow in method_arrows:
            pulse = Dot(
                point=arrow.get_start(),
                radius=0.06,
                color=YELLOW,
                fill_opacity=1
            )
            self.add(pulse)
            self.play(pulse.animate.move_to(arrow.get_end()), run_time=max(0.05, 0.65))
            self.play(FadeOut(pulse), run_time=max(0.05, 0.20))
            self.wait(max(0.05, 0.25))

        # 19.92 - 20.76 gap
        self.wait(max(0.05, 0.84))

        # 20.76 - 25.00: downstream blocks briefly recover,
        # then the electrode/sensor block flashes once more
        self.play(downstream_blocks.animate.set_opacity(1), run_time=max(0.05, 0.70))
        self.wait(max(0.05, 0.64))

        self.play(
            first_rect.animate.set_fill(YELLOW, opacity=1).set_stroke(YELLOW, width=10),
            glow_rect.animate.set_stroke(width=14),
            run_time=max(0.05, 0.35
        ))
        self.play(
            first_rect.animate.set_fill(BLUE, opacity=1).set_stroke(YELLOW, width=8),
            glow_rect.animate.set_stroke(width=12),
            run_time=max(0.05, 0.35
        ))
        self.wait(max(0.05, 2.20))

        # 25.00 - 25.62 gap
        self.wait(max(0.05, 0.62))

        # 25.62 - 30.60: subtle zoom out to hold the full diagram
        self.play(self.camera.frame.animate.scale(1.18), run_time=max(0.05, 1.20))
        self.wait(max(0.05, 3.78))

        # 30.60 - 31.54 gap
        self.wait(max(0.05, 0.94))

        # 31.54 - 38.28: final electrode/sensor emphasis and faint label pulse
        self.play(
            first_rect.animate.set_fill(YELLOW, opacity=1).set_stroke(YELLOW, width=10),
            glow_rect.animate.set_stroke(width=14),
            downstream_blocks.animate.set_opacity(0.5),
            method_group.animate.set_opacity(0.55),
            run_time=max(0.05, 0.60
        ))
        self.play(method_group.animate.set_opacity(1), run_time=max(0.05, 0.40))
        self.wait(max(0.05, 5.74))

        # Hold through the end of narration
        self.wait(max(0.05, 0.97))