# /// script
# dependencies = ["scipy>=1.13,<2", "matplotlib>=3.8,<4"]
# ///
"""Rebuild the figures with uv run analysis/neon-rl-fried/figures.py."""
from math import sqrt
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MaxNLocator
from scipy.stats import t

OUT = Path(__file__).resolve().parents[2] / "content/blog/neon-rl-fried"
# MongoDB snapshot through 2026-11-28T06:24:10.166Z. Only submitted choices.
# Each row contains (Neon picked, opponent picked).
matchups = {"Astra": (75, 39), "Opus": (6, 11)}
neon, opponent = map(sum, zip(*matchups.values()))
n = neon + opponent
share = neon / n

# Intercept-only, two-way cluster-robust variance for a vote share.
# For each dimension, sum the squared within-cluster sums of (vote - share).
def variance_component(groups, squared_scores):
    return groups / (groups - 1) * squared_scores / n**2

visitor_groups, battle_groups = 53, 38
se = sqrt(variance_component(visitor_groups, 34.12295320785501)
          + variance_component(battle_groups, 38.943534759046685)
          - variance_component(131, 30.91603053435107))
df = min(visitor_groups, battle_groups) - 1
margin = t.ppf(.975, df) * se
p_value = t.sf((share - .5) / se, df)
print(f"Neon {neon}/{n} = {share:.4f}, 95% CI {share-margin:.4f} to {share+margin:.4f}, one-sided p={p_value:.5f}")

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.fonttype": "none"})
colors = ["#155e54", "#61567e"]
labels = ["Gemini 4 Neon", "Opponent"]
positions = [1, 0]

def frame(title, xlabel):
    fig, ax = plt.subplots(figsize=(7.2, 2.8), layout="constrained")
    ax.set_title(title, loc="left", fontweight="bold", fontsize=15, pad=15)
    ax.set_yticks(positions, labels)
    ax.set_ylim(-.55, 1.55)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", color="#e2e4e4")
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", length=0, pad=7)
    ax.spines[:].set_visible(False)
    return fig, ax

def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=190, facecolor="white")
    plt.close(fig)

fig, ax = frame("Which response felt more RL fried?", "Votes")
ax.barh(positions, [neon, opponent], height=.45, color=colors)
for y, value in zip(positions, [neon, opponent]):
    ax.text(value + 1.3, y, str(value), va="center", fontweight="bold")
ax.set_xlim(0, max(neon, opponent) * 1.14)
ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=6))
save(fig, "votes")

fig, ax = frame("Share picked as more RL fried", "Share of votes · 95% confidence intervals")
ax.axvline(.5, color="#575e61", ls="--", lw=1)
for y, value, color in zip(positions, [share, 1-share], colors):
    ax.errorbar(value, y, xerr=margin, fmt="o", color=color, capsize=5, lw=2, ms=8)
    ax.text(value, y+.22, f"{value:.1%}  ({value-margin:.1%}–{value+margin:.1%})",
            ha="center", va="center", color=color, fontsize=10)
ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
save(fig, "vote-share")
