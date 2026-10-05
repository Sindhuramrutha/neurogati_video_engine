# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///
"""A worked example: a headline that rises in, an accent bar that grows, and the
on-screen words arriving one line at a time. Drawn with scenekit and Pillow."""

from scenekit import VideoWriter, between, canvas, font, load_brief, wrap

brief = load_brief()
look = brief.look
margin = int(brief.width * 0.08)
headline_font = font(brief, 88, bold=True)
body_font = font(brief, 46)

with VideoWriter(brief) as video:
    for n in range(brief.frames):
        t = n / max(1, brief.frames - 1)
        image, draw = canvas(brief)

        # The headline rises into place over the first tenth of the scene.
        rise = between(t, 0.0, 0.10)
        y = int(brief.height * 0.22 + (1 - rise) * 60)
        lines = wrap(draw, brief.headline, headline_font, brief.width - 2 * margin)
        for index, line in enumerate(lines[:2]):
            draw.text((margin, y + index * 104), line, font=headline_font, fill=look["text"])

        # The accent bar grows under it.
        grow = between(t, 0.05, 0.18)
        bar_top = y + len(lines[:2]) * 104 + 24
        draw.rectangle([margin, bar_top, margin + int(420 * grow), bar_top + 12],
                       fill=look["accent"])

        # The on-screen words arrive a line at a time, spread across the scene.
        points = [p.strip() for p in brief.on_screen.split(".") if p.strip()][:3]
        for index, point in enumerate(points):
            appear = between(t, 0.20 + index * 0.22, 0.30 + index * 0.22)
            if appear <= 0:
                continue
            row = bar_top + 80 + index * 92
            shown = wrap(draw, point, body_font, brief.width - 2 * margin)[0]
            draw.text((margin + int((1 - appear) * 40), row), shown, font=body_font,
                      fill=look["text"] if appear >= 1 else look["dim"])
        video.write(image)
