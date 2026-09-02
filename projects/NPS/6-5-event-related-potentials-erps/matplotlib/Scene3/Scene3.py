import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import Normalize
import numpy as np
import textwrap

fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
fig.patch.set_facecolor("#0F1116")

ax = fig.add_subplot(111)
ax.set_facecolor("#0F1116")
fig.subplots_adjust(left=0.07, right=0.97, top=0.92, bottom=0.18)

xticks = [-400, -300, -200, -100, 0, 100, 200, 300, 400]
yticks = [-2, -1, 0, 1, 2]

ax.set_xlim(-430, 430)
ax.set_ylim(-2.4, 2.8)
ax.set_xticks(xticks)
ax.set_yticks(yticks)
ax.set_xticklabels([""] * len(xticks))
ax.set_yticklabels([])
ax.tick_params(axis="both", colors="white", length=4, width=1, labelsize=11)

ax.grid(True, color="white", alpha=0.10, linewidth=0.5)
ax.set_axisbelow(True)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
for spine in ["bottom", "left"]:
    ax.spines[spine].set_color("white")
    ax.spines[spine].set_linewidth(1.2)

spine_tick_artists = [ax.spines["bottom"], ax.spines["left"]]
spine_tick_artists += list(ax.get_xticklines())
spine_tick_artists += list(ax.get_yticklines())
grid_artists = list(ax.get_xgridlines()) + list(ax.get_ygridlines())

for artist in spine_tick_artists:
    artist.set_alpha(0.0)
for gl in grid_artists:
    gl.set_alpha(0.0)

vline = ax.axvline(0.0, color="white", linestyle="--", linewidth=1.5, alpha=0.0)

zero_label = ax.text(
    0.0, -2.28, "0", color="white", fontsize=12,
    ha="center", va="top", alpha=0.0, zorder=7
)

ms_label = ax.text(
    410, -2.25, "ms", color="grey", fontsize=10,
    ha="right", va="top", alpha=0.0, zorder=7
)

bottom_text = fig.text(
    0.5, 0.045, "", fontsize=14, color="white",
    ha="center", va="center", zorder=20
)

def erp_wave(x):
    y = 0.48 * np.exp(-((x - 100.0) ** 2) / (2 * 11.0 ** 2))
    y += -0.72 * np.exp(-((x - 115.0) ** 2) / (2 * 14.0 ** 2))
    y += 1.38 * np.exp(-((x - 300.0) ** 2) / (2 * 58.0 ** 2))
    y += 0.07 * np.exp(-((x - 30.0) ** 2) / (2 * 20.0 ** 2))
    return y

xP = 100.0
yP = erp_wave(xP)
xN = 115.0
yN = erp_wave(xN)
xP300 = 300.0
yP300 = erp_wave(xP300)

xs_full = np.linspace(-430, 430, 1600)
ys_full = erp_wave(xs_full)
points = np.array([xs_full, ys_full]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
midpoints = (xs_full[:-1] + xs_full[1:]) / 2.0
cmap = plt.cm.turbo
norm = Normalize(-430, 430)

wave_lc = LineCollection([], cmap=cmap, norm=norm, linewidths=2.5, zorder=3)
ax.add_collection(wave_lc)

sweep_pos_line, = ax.plot([], [], color="white", lw=7, alpha=0.0,
                           solid_capstyle="round", zorder=4)
sweep_neg_line, = ax.plot([], [], color="white", lw=7, alpha=0.0,
                           solid_capstyle="round", zorder=4)

x_sweep_pos = np.linspace(60, 125, 160)
y_sweep_pos = erp_wave(x_sweep_pos)
x_sweep_neg = np.linspace(100, 160, 160)
y_sweep_neg = erp_wave(x_sweep_neg)

x_pos_fill = np.linspace(60, 125, 160)
y_pos_fill = erp_wave(x_pos_fill)
x_neg_fill = np.linspace(95, 155, 160)
y_neg_fill = erp_wave(x_neg_fill)
x_large_fill = np.linspace(180, 430, 180)
y_large_fill = erp_wave(x_large_fill)

pos_fill = ax.fill_between(
    x_pos_fill, 0, y_pos_fill, where=(y_pos_fill > 0),
    color="#2ecc71", alpha=0.0, zorder=2
)
neg_fill = ax.fill_between(
    x_neg_fill, 0, y_neg_fill, where=(y_neg_fill < 0),
    color="#5dade2", alpha=0.0, zorder=2
)
large_fill = ax.fill_between(
    x_large_fill, 0, y_large_fill, where=(y_large_fill > 0),
    color="#2ecc71", alpha=0.0, zorder=2
)

P_n_label = ax.text(
    120, 2.30, "P", color="#2ecc71", fontsize=13,
    ha="center", va="center", alpha=0.0, zorder=6
)
N_n_label = ax.text(
    220, 2.30, "N", color="#5dade2", fontsize=13,
    ha="center", va="center", alpha=0.0, zorder=6
)
P_n_arrow = FancyArrowPatch(
    posA=(120, 2.30), posB=(xP, yP), arrowstyle="-|>",
    mutation_scale=8, color="#2ecc71", lw=1.2, alpha=0.0, zorder=5
)
N_n_arrow = FancyArrowPatch(
    posA=(220, 2.30), posB=(xN, yN), arrowstyle="-|>",
    mutation_scale=8, color="#5dade2", lw=1.2, alpha=0.0, zorder=5
)
ax.add_patch(P_n_arrow)
ax.add_patch(N_n_arrow)

P100_label = ax.text(
    xP, 2.15, "P100", color="#2ecc71", fontsize=12,
    ha="center", va="center", alpha=0.0, zorder=6
)
P100_arrow = FancyArrowPatch(
    posA=(xP, 2.15), posB=(xP, yP), arrowstyle="-|>",
    mutation_scale=7, color="#2ecc71", lw=1.2, alpha=0.0, zorder=5
)
ax.add_patch(P100_arrow)

N100_label = ax.text(
    xN, 1.70, "N100", color="#5dade2", fontsize=12,
    ha="center", va="center", alpha=0.0, zorder=6
)
N100_arrow = FancyArrowPatch(
    posA=(xN, 1.70), posB=(xN, yN), arrowstyle="-|>",
    mutation_scale=7, color="#5dade2", lw=1.2, alpha=0.0, zorder=5
)
ax.add_patch(N100_arrow)

P300_label = ax.text(
    xP300, 2.50, "P300", color="#2ecc71", fontsize=15,
    ha="center", va="center", alpha=0.0, zorder=6
)
P300_arrow = FancyArrowPatch(
    posA=(xP300, 2.50), posB=(xP300, yP300), arrowstyle="-|>",
    mutation_scale=8, color="#2ecc71", lw=1.3, alpha=0.0, zorder=5
)
ax.add_patch(P300_arrow)

def smoothstep(t, t0, t1):
    if t <= t0:
        return 0.0
    if t >= t1:
        return 1.0
    x = (t - t0) / (t1 - t0)
    return x * x * (3.0 - 2.0 * x)

def pulse(t, t0, t1, peak=1.0):
    if t <= t0 or t >= t1:
        return 0.0
    progress = (t - t0) / (t1 - t0)
    return peak * np.sin(np.pi * progress) ** 2

def flash_intensity(t, center, width=0.30):
    if abs(t - center) >= width:
        return 0.0
    return np.cos((t - center) / width * (np.pi / 2.0)) ** 2

def clip_alpha(values, max_alpha=0.70):
    return float(np.clip(np.sum(values), 0.0, max_alpha))

text_events = [
    (4.75, 5.70, "An ERP waveform consists of a series of positive and negative voltage deflections"),
    (5.70, 9.18, "These deflections are referred to as ERP components"),
    (9.18, 11.98, "They are usually named according to their polarity"),
    (11.98, 14.36, "P for positive, N for negative"),
    (14.36, 17.62, "and their approximate latency after the stimulus"),
    (17.62, 25.32, "For example, P100 is a positive peak occurring approximately 100 milliseconds after stimulus onset"),
    (25.32, 32.26, "N100 is a negative peak occurring approximately 100 milliseconds after stimulus onset"),
    (32.26, 39.46, "P300 is a positive peak occurring approximately 300 milliseconds after stimulus onset"),
    (39.46, 46.83, "Different ERP components are associated with different stages of sensory, perceptual, or cognitive processing"),
]

def get_text_alpha(t, start, end, fade=0.45):
    if t < start - fade or t > end + fade:
        return 0.0
    if t < start:
        return smoothstep(start - fade, start, t)
    if t > end:
        return 1.0 - smoothstep(end, end + fade, t)
    return 1.0

fps = 30
total_duration = 46.83
total_frames = int(round(total_duration * fps))

x_tick_texts = ax.get_xticklabels()
for txt in x_tick_texts:
    txt.set_fontsize(11)

def update(frame):
    t = frame / fps

    axes_alpha = smoothstep(0.0, 0.8, t)
    spine_alpha = 0.85 * axes_alpha
    grid_alpha = 0.10 * axes_alpha

    for artist in spine_tick_artists:
        artist.set_alpha(spine_alpha)
    for gl in grid_artists:
        gl.set_alpha(grid_alpha)

    vline.set_alpha(0.80 * axes_alpha)

    reveal = smoothstep(0.6, 4.4, t)
    n_wave = int(len(segments) * reveal)
    wave_lc.set_segments(segments[:n_wave])
    if n_wave > 0:
        wave_lc.set_array(midpoints[:n_wave])
    else:
        wave_lc.set_array(np.empty(0))

    x_label_alpha = smoothstep(14.36, 15.8, t)
    for idx, val in enumerate(xticks):
        if val >= 0 and x_label_alpha > 0.0:
            x_tick_texts[idx].set_text(str(val))
            x_tick_texts[idx].set_color("white")
            x_tick_texts[idx].set_alpha(x_label_alpha)
        else:
            x_tick_texts[idx].set_text("")
            x_tick_texts[idx].set_alpha(0.0)

    flash_100_1 = flash_intensity(t, 20.0, 0.30)
    flash_100_2 = flash_intensity(t, 28.0, 0.30)
    flash_300 = flash_intensity(t, 35.0, 0.30)

    for idx, val in enumerate(xticks):
        if val == 100:
            f = max(flash_100_1, flash_100_2)
            if f > 1e-3:
                x_tick_texts[idx].set_color("#ffd966")
                x_tick_texts[idx].set_alpha(min(1.0, x_label_alpha + 0.85 * f))
        elif val == 300 and flash_300 > 1e-3:
            x_tick_texts[idx].set_color("#ffd966")
            x_tick_texts[idx].set_alpha(min(1.0, x_label_alpha + 0.85 * flash_300))

    zero_label.set_alpha(0.80 * axes_alpha * (1.0 - x_label_alpha))
    ms_label.set_alpha(0.80 * x_label_alpha)

    sweep_alpha = 0.45 * smoothstep(5.7, 6.0, t) * (1.0 - smoothstep(7.8, 8.4, t))
    sweep_pos_reveal = smoothstep(5.7, 6.2, t)
    sweep_neg_reveal = smoothstep(6.7, 7.2, t)

    m_pos = int(len(x_sweep_pos) * sweep_pos_reveal)
    if m_pos > 0:
        sweep_pos_line.set_data(x_sweep_pos[:m_pos], y_sweep_pos[:m_pos])
    else:
        sweep_pos_line.set_data([], [])

    m_neg = int(len(x_sweep_neg) * sweep_neg_reveal)
    if m_neg > 0:
        sweep_neg_line.set_data(x_sweep_neg[:m_neg], y_sweep_neg[:m_neg])
    else:
        sweep_neg_line.set_data([], [])

    sweep_pos_line.set_alpha(sweep_alpha)
    sweep_neg_line.set_alpha(sweep_alpha)

    pos_glow = pulse(t, 9.18, 10.4, 0.35)
    neg_glow = pulse(t, 10.4, 11.42, 0.40)

    pos_highlight = 0.35 * smoothstep(17.62, 18.2, t) * (1.0 - smoothstep(24.0, 24.36, t))
    neg_highlight = 0.35 * smoothstep(25.32, 25.9, t) * (1.0 - smoothstep(30.9, 31.32, t))
    large_highlight = 0.35 * smoothstep(32.26, 32.9, t) * (1.0 - smoothstep(38.0, 38.52, t))

    p100_seq = pulse(t, 40.0, 41.8, 0.50)
    n100_seq = pulse(t, 42.0, 43.8, 0.50)
    p300_seq = pulse(t, 44.0, 45.8, 0.55)

    pos_fill.set_alpha(clip_alpha([pos_glow, pos_highlight, p100_seq]))
    neg_fill.set_alpha(clip_alpha([neg_glow, neg_highlight, n100_seq]))
    large_fill.set_alpha(clip_alpha([large_highlight, p300_seq]))

    u_pn = smoothstep(11.98, 12.8, t)
    pn_alpha = smoothstep(11.98, 12.5, t) * (1.0 - smoothstep(16.4, 17.2, t))

    P_n_x = 120.0 + (100.0 - 120.0) * u_pn
    P_n_y = 2.30 + (1.45 - 2.30) * u_pn
    N_n_x = 220.0 + (145.0 - 220.0) * u_pn
    N_n_y = 2.30 + (1.50 - 2.30) * u_pn

    P_n_label.set_position((P_n_x, P_n_y))
    N_n_label.set_position((N_n_x, N_n_y))
    P_n_arrow.set_positions((P_n_x, P_n_y), (xP, yP))
    N_n_arrow.set_positions((N_n_x, N_n_y), (xN, yN))

    P_n_label.set_alpha(pn_alpha)
    N_n_label.set_alpha(pn_alpha)
    P_n_arrow.set_alpha(0.9 * pn_alpha)
    N_n_arrow.set_alpha(0.9 * pn_alpha)

    appear_p100 = smoothstep(17.62, 18.2, t)
    P100_y = 2.15 - 0.30 * appear_p100
    P100_label.set_position((xP, P100_y))
    P100_arrow.set_positions((xP, P100_y), (xP, yP))
    P100_label.set_alpha(appear_p100)
    P100_arrow.set_alpha(0.9 * appear_p100)

    appear_n100 = smoothstep(25.32, 25.9, t)
    N100_y = 1.70 - 0.25 * appear_n100
    N100_label.set_position((xN, N100_y))
    N100_arrow.set_positions((xN, N100_y), (xN, yN))
    N100_label.set_alpha(appear_n100)
    N100_arrow.set_alpha(0.9 * appear_n100)

    appear_p300 = smoothstep(32.26, 32.9, t)
    P300_y = 2.50 - 0.30 * appear_p300
    P300_label.set_position((xP300, P300_y))
    P300_arrow.set_positions((xP300, P300_y), (xP300, yP300))
    P300_label.set_alpha(appear_p300)
    P300_arrow.set_alpha(0.9 * appear_p300)

    best_text = ""
    best_alpha = 0.0
    for start, end, txt in text_events:
        alpha = get_text_alpha(t, start, end)
        if alpha > best_alpha:
            best_alpha = alpha
            best_text = txt

    if best_alpha > 0.0 and best_text:
        wrapped = "\n".join(textwrap.wrap(best_text, 70))
        bottom_text.set_text(wrapped)
        bottom_text.set_alpha(best_alpha)
    else:
        bottom_text.set_text("")
        bottom_text.set_alpha(0.0)

    return []

ani = animation.FuncAnimation(
    fig, update, frames=total_frames,
    interval=1000 / fps, blit=False
)

ani.save("output.mp4", writer="ffmpeg", fps=30)