ASSET_PATHS = {'heart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\test_heart.svg', 'brain': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\brain_test.svg', 'stopwatch': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\stopwatch.svg', 'activity': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\activity.svg', 'soundwave': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\soundwave.svg', 'grid_matrix': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\grid-3x3-gap-fill.svg', 'bar_chart': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bar-chart.svg', 'graph_trend': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\graph-up-arrow.svg', 'cpu': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\cpu.svg', 'funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\funnel.svg', 'table': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\table.svg', 'hospital': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hospital.svg', 'capsule': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\capsule.svg', 'clipboard_pulse': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\clipboard2-pulse.svg', 'hand': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\hand-index-thumb.svg', 'broadcast': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\broadcast-pin.svg', 'gear': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\gear.svg', 'arrow_repeat': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\arrow-repeat.svg', 'lightbulb': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\lightbulb.svg', 'bell': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\bell.svg', 'check_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\check-circle.svg', 'x_circle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\x-circle.svg', 'rulers': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\rulers.svg', 'puzzle': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\puzzle.svg', 'fig_measurement_funnel': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_measurement_funnel.png', 'fig_mindmap_three_pillars': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_three_pillars.png', 'fig_mindmap_full': 'C:\\Users\\DELL\\Desktop\\neurogati_video_engine\\assets\\image\\fig_mindmap_full.png'}

from manim import *

class Scene1(Scene):
    def construct(self):
        self.camera.background_color = "#0F1116"

        # Initial fade-in from black to dark background
        black_cover = Rectangle(
            width=20, height=12,
            fill_color=BLACK, fill_opacity=1,
            stroke_width=0
        )
        black_cover.move_to(ORIGIN)
        self.add(black_cover)
        self.play(FadeOut(black_cover, run_time=max(0.05, 1.76)))

        # Bullet 1
        marker1 = Dot(radius=0.08, color=WHITE, fill_opacity=1, stroke_width=0)
        text1 = Text("Explain moving-average filter", font_size=38, color=WHITE)
        bullet1 = VGroup(marker1, text1).arrange(RIGHT, buff=0.25)
        bullet1.move_to(UP * 1.0)
        self.play(FadeIn(bullet1, run_time=max(0.05, 1.0)))
        self.wait(max(0.05, 1.26))  # until 4.02

        # Brighten bullet1
        self.play(text1.animate.set_color(YELLOW), run_time=max(0.05, 0.25))
        self.play(text1.animate.set_color(WHITE), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.64))  # until 5.16

        # Bullet 2
        marker2 = Dot(radius=0.08, color=WHITE, fill_opacity=1, stroke_width=0)
        text2 = Text("Explain median filter", font_size=38, color=WHITE)
        bullet2 = VGroup(marker2, text2).arrange(RIGHT, buff=0.25)
        bullet2.next_to(bullet1, DOWN, buff=0.5)
        self.play(FadeIn(bullet2, run_time=max(0.05, 0.5)))
        self.play(text2.animate.set_color(YELLOW), run_time=max(0.05, 0.25))
        self.play(text2.animate.set_color(WHITE), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.48))  # until 6.64

        # Bullet 3
        marker3 = Dot(radius=0.08, color=WHITE, fill_opacity=1, stroke_width=0)
        text3 = Text("Compare both filters", font_size=38, color=WHITE)
        bullet3 = VGroup(marker3, text3).arrange(RIGHT, buff=0.25)
        bullet3.next_to(bullet2, DOWN, buff=0.5)
        self.play(FadeIn(bullet3, run_time=max(0.05, 0.5)))
        self.play(text3.animate.set_color(YELLOW), run_time=max(0.05, 0.25))
        self.play(text3.animate.set_color(WHITE), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 0.58))  # until 8.22

        # Bullet 4
        marker4 = Dot(radius=0.08, color=WHITE, fill_opacity=1, stroke_width=0)
        text4 = Text("Identify appropriate applications", font_size=38, color=WHITE)
        bullet4 = VGroup(marker4, text4).arrange(RIGHT, buff=0.25)
        bullet4.next_to(bullet3, DOWN, buff=0.5)
        self.play(FadeIn(bullet4, run_time=max(0.05, 0.5)))
        self.play(text4.animate.set_color(YELLOW), run_time=max(0.05, 0.25))
        self.play(text4.animate.set_color(WHITE), run_time=max(0.05, 0.25))
        self.wait(max(0.05, 2.78))  # until 12.00

        # Final line (no bullet, slightly smaller and dimmer)
        final_text = Text(
            "You'll also understand their advantages and limitations.",
            font_size=28,
            color=GREY
        )
        final_text.next_to(bullet4, DOWN, buff=0.7)
        self.play(FadeIn(final_text, run_time=max(0.05, 0.8)))
        self.wait(max(0.05, 1.6))  # until 14.40

        # Fade the whole list and background to black
        fade_to_black = Rectangle(
            width=20, height=12,
            fill_color=BLACK, fill_opacity=0,
            stroke_width=0
        )
        fade_to_black.move_to(ORIGIN)
        self.add(fade_to_black)
        self.play(fade_to_black.animate.set_fill(opacity=1), run_time=max(0.05, 1.13))