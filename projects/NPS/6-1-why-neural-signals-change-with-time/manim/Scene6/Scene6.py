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


class Scene6(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Heading, carried over from previous scene
        heading = Text("Cognitive Processes", font_size=50, weight="BOLD", color=WHITE)
        heading.to_edge(UP, buff=0.28)
        self.add(heading)

        # Stylized brain outline, empty inside
        brain_outline = SVGMobject(ASSET_PATHS["brain"])
        brain_outline.set_fill(opacity=0)
        brain_outline.set_stroke(WHITE, width=3)
        brain_outline.set_color(WHITE)
        brain_outline.scale_to_fit_height(2.9)
        if brain_outline.width > 4.2:
            brain_outline.scale_to_fit_width(4.2)
        brain_outline.move_to(np.array([0, 0.75, 0]))
        brain_outline.set_z_index(5)

        # 0.00-0.36: brain outline fades in
        self.play(FadeIn(brain_outline), run_time=max(0.05, 0.36))

        # 0.36-1.00: subtle soft emphasis pulse over the brain outline
        self.play(
            brain_outline.animate.set_stroke(color=YELLOW, width=4.5, opacity=0.9),
            rate_func=there_and_back,
            run_time=max(0.05, 0.64),
        )

        # 1.00-1.64: hold
        self.wait(max(0.05, 0.64))

        # Nodes inside brain outline
        n_nodes = 24
        brain_center = brain_outline.get_center()
        brain_w = brain_outline.width
        brain_h = brain_outline.height
        a = brain_w / 2 * 0.88
        b = brain_h / 2 * 0.82

        rng = np.random.RandomState(7)
        positions = []
        while len(positions) < n_nodes:
            x = rng.uniform(-a, a)
            y = rng.uniform(-b, b)
            if (x / a) ** 2 + (y / b) ** 2 <= 0.82:
                positions.append(np.array([brain_center[0] + x, brain_center[1] + y, 0.0]))

        nodes = VGroup(*[
            Dot(pos, radius=0.055, color=TEAL, fill_opacity=1.0)
            for pos in positions
        ])
        nodes.set_z_index(2)

        # Candidate edges: nearest-neighbor style network
        all_dists = []
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                d = np.linalg.norm(positions[i][:2] - positions[j][:2])
                all_dists.append((d, i, j))
        all_dists.sort(key=lambda item: item[0])

        desired_candidates = 55
        candidate_pairs = [(i, j) for _, i, j in all_dists[:desired_candidates]]

        trackers_by_pair = {}
        edge_lines = VGroup()
        for pair in candidate_pairs:
            i, j = pair
            tr = ValueTracker(0.0)
            trackers_by_pair[pair] = tr
            line = Line(
                positions[i],
                positions[j],
                stroke_color=GREY_B,
                stroke_width=2,
                stroke_opacity=0.0,
            )
            line.add_updater(
                lambda m, tr=tr: m.set_stroke(color=GREY_B, width=2, opacity=tr.get_value())
            )
            edge_lines.add(line)
        edge_lines.set_z_index(1)

        config_size = min(30, len(candidate_pairs))

        def generate_config():
            idx = rng.choice(len(candidate_pairs), size=config_size, replace=False)
            return set(int(i) for i in idx)

        def crossfade_anims(remove_idx, add_idx):
            anims = []
            for idx in remove_idx:
                pair = candidate_pairs[idx]
                anims.append(trackers_by_pair[pair].animate.set_value(0.0))
            for idx in add_idx:
                pair = candidate_pairs[idx]
                anims.append(trackers_by_pair[pair].animate.set_value(1.0))
            return anims

        def swap_edges(current_idx, n_remove, n_add):
            removable = list(current_idx)
            remove = set()
            if removable and n_remove > 0:
                k = min(n_remove, len(removable))
                remove = set(rng.choice(removable, size=k, replace=False))

            inactive = [
                i for i in range(len(candidate_pairs))
                if i not in current_idx and i not in remove
            ]
            add = set()
            if inactive and n_add > 0:
                k = min(n_add, len(inactive))
                add = set(int(i) for i in rng.choice(inactive, size=k, replace=False))
            return remove, add

        current_indices = set()

        def run_roll(total_time, rounds, n_remove=5, n_add=5, extra_first=None):
            nonlocal current_indices
            per = total_time / rounds
            for k in range(rounds):
                remove, add = swap_edges(current_indices, n_remove, n_add)
                anims = crossfade_anims(remove, add)
                if k == 0 and extra_first:
                    anims.extend(extra_first)
                self.play(*anims, run_time=max(0.05, per))
                current_indices.difference_update(remove)
                current_indices.update(add)

        initial_edges = generate_config()

        # 1.64-2.22: nodes and initial arbitrary network fade in
        self.add(edge_lines)
        self.play(
            FadeIn(nodes),
            *[trackers_by_pair[candidate_pairs[i]].animate.set_value(1.0) for i in initial_edges],
            run_time=max(0.05, 0.58),
        )
        current_indices = set(initial_edges)

        # 2.22-3.18: network holds
        self.wait(max(0.05, 0.96))

        # Labels around the brain
        att_label = Text("Attention", font_size=27, color=BLUE)
        mem_label = Text("Memory", font_size=27, color=PINK)
        dec_label = Text("Decision-making", font_size=27, color=ORANGE)
        learn_label = Text("Learning", font_size=27, color=GREEN)

        bl = brain_outline.get_left()
        br = brain_outline.get_right()
        bt = brain_outline.get_top()
        bb = brain_outline.get_bottom()

        att_label.move_to(np.array([bl[0] - 0.9, bt[1] + 0.45, 0]))
        mem_label.move_to(np.array([br[0] + 0.9, bt[1] + 0.45, 0]))
        dec_label.move_to(np.array([bl[0] - 0.9, bb[1] - 0.4, 0]))
        learn_label.move_to(np.array([br[0] + 0.9, bb[1] - 0.4, 0]))

        labels = VGroup(att_label, mem_label, dec_label, learn_label)

        # 3.18-3.44: Attention label + first reconfiguration
        att_config = generate_config()
        remove = current_indices - att_config
        add = att_config - current_indices
        self.play(
            FadeIn(att_label),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 0.26),
        )
        current_indices = set(att_config)

        # 3.44-4.04: settle
        self.wait(max(0.05, 0.60))

        # 4.04-4.24: Memory label + second reconfiguration
        mem_config = generate_config()
        remove = current_indices - mem_config
        add = mem_config - current_indices
        self.play(
            FadeIn(mem_label),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 0.20),
        )
        current_indices = set(mem_config)

        # 4.24-4.76: settle
        self.wait(max(0.05, 0.52))

        # 4.76-5.34: Decision-making label + third reconfiguration
        dec_config = generate_config()
        remove = current_indices - dec_config
        add = dec_config - current_indices
        self.play(
            FadeIn(dec_label),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 0.58),
        )
        current_indices = set(dec_config)

        # 5.34-5.78: settle
        self.wait(max(0.05, 0.44))

        # 5.78-6.04: Learning label + fourth reconfiguration
        learn_config = generate_config()
        remove = current_indices - learn_config
        add = learn_config - current_indices
        self.play(
            FadeIn(learn_label),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 0.26),
        )
        current_indices = set(learn_config)

        # 6.04-7.00: four labels pulse softly in unison
        self.play(
            *[lab.animate.set_color(YELLOW) for lab in labels],
            rate_func=there_and_back,
            run_time=max(0.05, 0.96),
        )

        # Waveform trackers, created now but not yet visible
        wave_phase = ValueTracker(0.0)
        wave_amp = ValueTracker(0.5)
        wave_emphasis = ValueTracker(0.0)
        wave_phase.add_updater(lambda m, dt: m.increment_value(0.85 * dt))
        self.add(wave_phase, wave_amp, wave_emphasis)

        # Connection beam and moving glow pulse
        beam_line = Line(
            np.array([0, bb[1] - 0.15, 0]),
            np.array([0, -1.5, 0]),
            stroke_color=YELLOW,
            stroke_width=10,
            stroke_opacity=0.0,
        )
        pulse_dot = Dot(radius=0.075, color=YELLOW, fill_opacity=0.0)
        pulse_dot.move_to(np.array([0, bb[1] - 0.15, 0]))
        self.add(beam_line, pulse_dot)

        wave = VMobject(stroke_color=TEAL, stroke_width=3, stroke_opacity=0.0)
        wave.set_z_index(0)

        def update_wave_path(mob):
            xs = np.linspace(-6.2, 6.2, 320)
            phase = wave_phase.get_value()
            amp = wave_amp.get_value()
            emph = wave_emphasis.get_value()
            color = YELLOW if emph > 0.5 else TEAL
            width = 5 if emph > 0.5 else 3

            y = amp * (
                0.6 * np.sin(2 * PI * 0.42 * (xs - phase * 0.7))
                + 0.25 * np.sin(2 * PI * 0.8 * (xs + phase * 0.5))
                + 0.15 * np.sin(2 * PI * 1.3 * (xs - phase * 1.1))
            )
            y += amp * 0.2 * np.sin(2 * PI * 2.0 * (xs + phase * 0.4)) * np.exp(
                -0.15 * (xs - phase * 0.5) ** 2
            )

            points = [np.array([x, -1.95 + yv, 0]) for x, yv in zip(xs, y)]
            mob.set_points_as_corners(points)
            mob.set_stroke(color=color, width=width)

        wave.add_updater(update_wave_path)
        self.add(wave)

        # 7.00-8.14: continuous rolling reconfiguration
        run_roll(1.14, 3, 5, 5)

        # 8.14-9.16: waveform fades in, synchronized with network movement
        remove, add = swap_edges(current_indices, 5, 5)
        self.play(
            wave.animate.set_stroke(opacity=1.0),
            wave_amp.animate.set_value(0.7),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 1.02),
        )
        current_indices.difference_update(remove)
        current_indices.update(add)

        # 9.16-10.20: complete composition holds while network keeps moving
        run_roll(1.04, 3, 5, 5)

        # 10.20-11.40: evolution becomes more pronounced
        run_roll(
            1.20,
            3,
            7,
            7,
            extra_first=[wave_amp.animate.set_value(0.9)],
        )

        # 11.40-12.48: smooth uninterrupted rolling reconfiguration
        run_roll(1.08, 3, 5, 5)

        # 12.48-13.72: soft influence glow travels down to the waveform
        remove, add = swap_edges(current_indices, 5, 5)
        self.play(
            beam_line.animate.set_stroke(opacity=0.4),
            pulse_dot.animate.move_to(np.array([0, -1.5, 0])).set_fill(opacity=0.9),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 0.62),
        )
        current_indices.difference_update(remove)
        current_indices.update(add)

        remove, add = swap_edges(current_indices, 5, 5)
        self.play(
            beam_line.animate.set_stroke(opacity=0.05),
            pulse_dot.animate.set_fill(opacity=0.0),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 0.62),
        )
        current_indices.difference_update(remove)
        current_indices.update(add)

        # 13.72-14.74: recorded signal becomes focal point
        remove, add = swap_edges(current_indices, 6, 6)
        self.play(
            wave_emphasis.animate.set_value(1.0),
            wave_amp.animate.set_value(0.95),
            *crossfade_anims(remove, add),
            run_time=max(0.05, 1.02),
        )
        current_indices.difference_update(remove)
        current_indices.update(add)

        # 14.74-15.50: final hold with continuous gentle motion
        run_roll(0.76, 2, 5, 5)