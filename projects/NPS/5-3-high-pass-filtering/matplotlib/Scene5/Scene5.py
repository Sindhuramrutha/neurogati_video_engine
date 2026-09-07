import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator
import numpy as np

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
fig = plt.figure(figsize=(12, 7))
fig.patch.set_facecolor("#0F1116")
ax = fig.add_subplot(1, 1, 1)
ax.set_facecolor("#0F1116")

ax.set_xlim(0, 4)
ax.set_ylim(0, 1.05)
ax.xaxis.set_major_locator(MaxNLocator(6))
ax.yaxis.set_major_locator(MaxNLocator(6))

ax.set_xlabel("Frequency (Hz)", color="white", fontsize=18)
ax.set_ylabel("Amplitude Response", color="white", fontsize=18)
ax.tick_params(colors="white", labelsize=12)
ax.grid(True, color="white", alpha=0.15, linestyle="--", linewidth=0.6)

for spine in ax.spines.values():
    spine.set_color("white")
    spine.set_alpha(0.75)

# ----------------------------------------------------------------------
# Data: high-pass S-curve, cutoff at 1 Hz
# ----------------------------------------------------------------------
k = 5.0
x0 = 1.0
x_full = np.linspace(0, 4, 1000)
y_full = 1.0 / (1.0 + np.exp(-k * (x_full - x0)))

n_segments = len(x_full) - 1
segments_full = [
    ((x_full[i], y_full[i]), (x_full[i + 1], y_full[i + 1]))
    for i in range(n_segments)
]

# Main colored curve, colored by frequency position.
lc_main = LineCollection(
    segments_full,
    cmap="plasma",
    norm=mcolors.Normalize(0, 4),
    linewidth=2.5,
    alpha=0,
    zorder=3,
)
lc_main.set_array(x_full[:-1])
ax.add_collection(lc_main)

# Left/right static glow overlays.
mask_left = x_full <= x0
mask_right = x_full >= x0
left_glow, = ax.plot(
    x_full[mask_left], y_full[mask_left],
    color="red", linewidth=5, alpha=0, zorder=4,
)
right_glow, = ax.plot(
    x_full[mask_right], y_full[mask_right],
    color="green", linewidth=5, alpha=0, zorder=4,
)

# White flowing glow trace, drawn left to right near the end.
glow_lc = LineCollection(
    segments_full,
    colors="white",
    linewidth=6,
    alpha=0,
    zorder=4,
)
ax.add_collection(glow_lc)

# ----------------------------------------------------------------------
# Persistent graphical elements
# ----------------------------------------------------------------------
vline = ax.axvline(x0, color="white", linestyle="--", linewidth=2, alpha=0, zorder=2)

cutoff_label = ax.text(
    x0, -0.08, "cutoff frequency (1 Hz)",
    transform=ax.transData,
    ha="center", va="top", fontsize=11, color="white",
    alpha=0, clip_on=False, zorder=5,
)

stopband_span = ax.axvspan(0, x0, color="red", alpha=0, zorder=1)
passband_span = ax.axvspan(x0, 4, color="green", alpha=0, zorder=1)

stopband_label = ax.text(
    0.5, 0.55, "stopband",
    transform=ax.transData, ha="center", va="center",
    fontsize=14, color="white", alpha=0, zorder=2,
)
passband_label = ax.text(
    2.5, 0.55, "passband",
    transform=ax.transData, ha="center", va="center",
    fontsize=14, color="white", alpha=0, zorder=2,
)

# Markers on the curve.
marker_x1 = 0.98
marker_y1 = 1.0 / (1.0 + np.exp(-k * (marker_x1 - x0)))
marker1, = ax.plot(
    [marker_x1], [marker_y1], "o",
    color="white", markersize=8, alpha=0, zorder=6,
)

marker_x2 = 0.02
marker_y2 = 1.0 / (1.0 + np.exp(-k * (marker_x2 - x0)))
marker2, = ax.plot(
    [marker_x2], [marker_y2], "o",
    color="white", markersize=8, alpha=0, zorder=6,
)

# Annotations with arrows.
annot1 = ax.annotate(
    "close to cutoff: partially attenuated",
    xy=(marker_x1, marker_y1),
    xytext=(0.78, 0.58),
    arrowprops=dict(arrowstyle="->", color="white", lw=1.5),
    fontsize=11, color="white", ha="center", alpha=0, zorder=10,
)

annot2 = ax.annotate(
    "well below cutoff: strongly attenuated",
    xy=(marker_x2, marker_y2),
    xytext=(0.04, 0.03),
    arrowprops=dict(arrowstyle="->", color="white", lw=1.5),
    fontsize=11, color="white", ha="center", alpha=0, zorder=10,
)

# White glow span around transition.
white_glow_span = ax.axvspan(0.85, 1.15, color="white", alpha=0, zorder=2)

# Text overlays, all pre-created.
text_hp = ax.text(
    0.5, 1.06, "high-pass filter",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=20, color="white", alpha=0, clip_on=False, zorder=8,
)
text_cutoff_word = ax.text(
    0.5, 1.06, "cutoff frequency",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=20, color="white", alpha=0, clip_on=False, zorder=8,
)
text_title = ax.text(
    0.5, 1.06, "High-Pass Filter",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=22, color="white", alpha=0, clip_on=False, zorder=8,
)
text_subtitle = ax.text(
    0.5, 0.98, "Cutoff Frequency: 1 Hz",
    transform=ax.transAxes, ha="center", va="top",
    fontsize=16, color="white", alpha=0, clip_on=False, zorder=8,
)
text_lowpass_note = ax.text(
    0.5, 1.06, "As with the low-pass filter",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=20, color="white", alpha=0, clip_on=False, zorder=8,
)
text_not_abrupt = ax.text(
    0.5, 0.05, "not abrupt",
    transform=ax.transAxes, ha="center", va="bottom",
    fontsize=14, color="white", alpha=0, clip_on=False, zorder=8,
)

# Additional labels near the curve.
largely_preserved_text = ax.text(
    1.28, 0.82, "largely preserved",
    fontsize=12, color="#99ff99", ha="center", va="center",
    alpha=0, zorder=7,
)
progressively_att_text = ax.text(
    0.68, 0.22, "progressively attenuated",
    fontsize=12, color="#ff9999", ha="center", va="center",
    alpha=0, zorder=7,
)

# Previous-scene definition-card cover.
cover = ax.add_patch(
    plt.Rectangle(
        (0, 0), 1, 1,
        transform=ax.transAxes,
        facecolor="#0F1116", edgecolor="none",
        zorder=100,
    )
)
card_text = ax.text(
    0.5, 0.5,
    "High-Pass Filter\nA filter that preserves high-frequency components\nwhile attenuating low-frequency components below a selected cutoff frequency",
    transform=ax.transAxes,
    ha="center", va="center",
    fontsize=18, color="white",
    zorder=101, linespacing=1.5,
)

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def clip01(x):
    return float(np.clip(x, 0.0, 1.0))

def smoothstep(t, t0, t1):
    if t <= t0:
        return 0.0
    if t >= t1:
        return 1.0
    x = (t - t0) / (t1 - t0)
    return x * x * (3 - 2 * x)

def fade_in(t, t0, t1):
    if t <= t0:
        return 0.0
    if t >= t1:
        return 1.0
    return (t - t0) / (t1 - t0)

def fade_out(t, t0, t1):
    if t <= t0:
        return 1.0
    if t >= t1:
        return 0.0
    return 1.0 - (t - t0) / (t1 - t0)

def fade_in_out(t, t_in0, t_in1, t_out0, t_out1):
    if t < t_in0:
        return 0.0
    elif t < t_in1:
        return (t - t_in0) / (t_in1 - t_in0)
    elif t < t_out0:
        return 1.0
    elif t < t_out1:
        return 1.0 - (t - t_out0) / (t_out1 - t_out0)
    else:
        return 0.0

def pulse_val(t, t0, t1):
    if t < t0 or t > t1:
        return 0.0
    return np.sin(np.pi * (t - t0) / (t1 - t0)) ** 2

# Axis-limit keyframes.
lim_times = [0, 10.88, 11.66, 27.96, 28.96, 32.18, 32.72, 35.88, 37.48]
xlim_keys = [
    (0, 4), (0, 4), (0.5, 1.5), (0.5, 1.5),
    (0.75, 1.05), (0.75, 1.05), (0, 0.1), (0, 0.1), (0, 4),
]
ylim_keys = [
    (0, 1.05), (0, 1.05), (0, 1.0), (0, 1.0),
    (0.35, 0.65), (0.35, 0.65), (0, 0.05), (0, 0.05), (0, 1.05),
]

def interpolate_lims(t, times, vals):
    if t <= times[0]:
        return vals[0]
    if t >= times[-1]:
        return vals[-1]
    for i in range(len(times) - 1):
        if times[i] <= t <= times[i + 1]:
            s = smoothstep(t, times[i], times[i + 1])
            return (
                (1 - s) * vals[i][0] + s * vals[i + 1][0],
                (1 - s) * vals[i][1] + s * vals[i + 1][1],
            )
    return vals[-1]

# ----------------------------------------------------------------------
# Animation update
# ----------------------------------------------------------------------
fps = 30
duration = 37.48
n_frames = int(duration * fps) + 1

def animate(i):
    t = i / fps

    # Beat 1: card fades out, revealing plot skeleton.
    card_alpha = 1.0 if t <= 0 else max(0.0, 1.0 - t / 0.44)
    cover.set_alpha(card_alpha)
    card_text.set_alpha(card_alpha)

    # Axis limits (zooms and pans).
    xlim = interpolate_lims(t, lim_times, xlim_keys)
    ylim = interpolate_lims(t, lim_times, ylim_keys)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # Beat 2: horizontal axis label pulse.
    pulse_x = pulse_val(t, 0.64, 1.10)
    ax.xaxis.label.set_alpha(clip01(1.0 - 0.4 * pulse_x))

    # Beat 3: vertical axis label pulse.
    pulse_y = pulse_val(t, 1.10, 1.40)
    ax.yaxis.label.set_alpha(clip01(1.0 - 0.4 * pulse_y))

    # Beat 4: "high-pass filter" text above plot.
    text_hp.set_alpha(fade_in_out(t, 1.88, 2.00, 2.20, 2.36))

    # Beat 5: "cutoff frequency" text fades into dashed line.
    text_cutoff_word.set_alpha(fade_in_out(t, 2.62, 2.85, 3.20, 3.54))

    # Dashed line and label appear.
    vline_base = fade_in(t, 3.25, 3.54)
    vline.set_alpha(vline_base)
    cutoff_label.set_alpha(vline_base)

    # Beat 6: dashed cutoff line pulses and label glows.
    pulse_6 = pulse_val(t, 3.62, 4.20)
    pulse_13 = pulse_val(t, 13.46, 14.00)
    vline.set_linewidth(2 + 3 * (pulse_6 + pulse_13))

    if pulse_6 > 0.1 or pulse_13 > 0.1:
        cutoff_label.set_color("#FFD966")
    else:
        cutoff_label.set_color("white")

    # Beat 7: shaded stopband/passband regions and labels.
    region_base = fade_in(t, 5.12, 5.80)
    stopband_span.set_alpha(0.20 * region_base)
    passband_span.set_alpha(0.20 * region_base)
    stopband_label.set_alpha(region_base)
    passband_label.set_alpha(region_base)

    # Beat 8: draw S-curve from left to right.
    draw_s = smoothstep(t, 6.72, 8.38)
    n_show = int(n_segments * draw_s)
    if n_show <= 0:
        lc_main.set_segments([])
        lc_main.set_array(np.array([]))
        lc_main.set_alpha(0)
    else:
        lc_main.set_segments(segments_full[:n_show])
        lc_main.set_array(x_full[:-1][:n_show])
        lc_main.set_alpha(1)

    # Beat 9 + 17: left-of-cutoff red glow. Base glow persists; beat 17 pulses.
    left_glow_alpha = 0.5 * fade_in(t, 8.76, 9.20) + 0.3 * pulse_val(t, 20.80, 22.30)
    left_glow.set_alpha(clip01(left_glow_alpha))

    # Beat 12 & 13: title overlay.
    title_fade_out_factor = 1.0 - fade_in(t, 16.12, 17.06)
    text_title.set_alpha(clip01(fade_in(t, 12.14, 13.14) * title_fade_out_factor))
    text_subtitle.set_alpha(clip01(fade_in(t, 13.46, 15.30) * title_fade_out_factor))

    # Beat 14: passband pulses and title/subtitle fades out.
    passband_pulse = pulse_val(t, 16.12, 17.06)
    passband_span.set_alpha(clip01(0.20 * region_base + 0.18 * passband_pulse))

    # Beat 15: right-of-cutoff green glow and "largely preserved" label.
    right_glow_alpha = 0.55 * fade_in(t, 17.36, 17.80) * (1.0 - fade_in(t, 19.72, 20.20))
    right_glow.set_alpha(clip01(right_glow_alpha))
    largely_preserved_text.set_alpha(
        clip01(fade_in(t, 17.36, 18.00) * (1.0 - fade_in(t, 19.72, 20.20)))
    )

    # Beat 16: stopband pulses.
    stopband_pulse = pulse_val(t, 19.72, 20.58)
    stopband_span.set_alpha(clip01(0.20 * region_base + 0.18 * stopband_pulse))

    # Beat 17: "progressively attenuated" label.
    progressively_att_text.set_alpha(fade_in(t, 20.80, 21.20))

    # Beat 18: "As with the low-pass filter" note.
    text_lowpass_note.set_alpha(fade_in_out(t, 23.04, 23.32, 24.20, 24.48))

    # Beat 19: white flowing glow trace left to right.
    glow_progress = smoothstep(t, 24.86, 26.08)
    n_glow = int(n_segments * glow_progress)
    if n_glow <= 0:
        glow_lc.set_segments([])
    else:
        glow_lc.set_segments(segments_full[:n_glow])

    # Beat 20: glow intensifies briefly, then settles.
    glow_pulse = pulse_val(t, 26.70, 27.12)
    glow_alpha = 0.25 * fade_in(t, 24.86, 26.08) + 0.45 * glow_pulse
    # Beat 26: gentle final glow.
    glow_alpha += 0.10 * pulse_val(t, 35.88, 37.48)
    glow_lc.set_alpha(clip01(glow_alpha))

    # White transition glow around the cutoff.
    white_span_alpha = (
        0.25 * fade_in(t, 24.86, 25.20)
        + 0.35 * glow_pulse
        + 0.20 * pulse_val(t, 35.88, 37.48)
    )
    white_glow_span.set_alpha(clip01(white_span_alpha))

    # Beat 20: "not abrupt" caption.
    text_not_abrupt.set_alpha(fade_in(t, 26.70, 27.12))

    # Beat 21: marker1 appears close to cutoff.
    marker1.set_alpha(fade_in(t, 27.96, 28.96))
    if t < 30.04:
        annot1.set_alpha(0)
        annot1.arrow_patch.set_alpha(0)
    else:
        a1 = fade_in(t, 30.04, 30.60)
        annot1.set_alpha(a1)
        annot1.arrow_patch.set_alpha(a1)

    # Beat 24: marker2 appears far left.
    marker2.set_alpha(fade_in(t, 33.34, 34.00))
    if t < 34.84:
        annot2.set_alpha(0)
        annot2.arrow_patch.set_alpha(0)
    else:
        a2 = fade_in(t, 34.84, 35.50)
        annot2.set_alpha(a2)
        annot2.arrow_patch.set_alpha(a2)

    # Beat 26: main curve gently glows by slightly increasing linewidth.
    final_glow_pulse = pulse_val(t, 35.88, 37.48)
    lc_main.set_linewidth(2.5 + 0.6 * final_glow_pulse)

# ----------------------------------------------------------------------
# Save
# ----------------------------------------------------------------------
anim = animation.FuncAnimation(
    fig, animate, frames=n_frames, interval=1000 / fps, blit=False
)
anim.save("output.mp4", writer="ffmpeg", fps=30)