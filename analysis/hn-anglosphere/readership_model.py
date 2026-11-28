"""Charts for "Science, startups and beer drinking predict ... HN readership".

Inputs (this folder): goatcounter-locations.csv, worldbank-population-2024.json, country-features.csv
(see country-features-sources.md). Charts have titles only (no subtitles or source footers).

Run:  uv run --with matplotlib --with pandas --with statsmodels --with scipy --with adjustText python analysis/hn-anglosphere/readership_model.py
Writes into content/blog/hn-readership-model/.
"""

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import statsmodels.api as sm

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, NullFormatter

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "content/blog/hn-readership-model"
OUT.mkdir(parents=True, exist_ok=True)

ink, muted, green, green_light, accent, gray, rule = (
    "#172b3a", "#607485", "#087f8c", "#5fb3bb", "#c2410c", "#9eabb6", "#e7edf1")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": ink,
                     "axes.labelcolor": ink, "xtick.color": muted, "ytick.color": muted,
                     "svg.fonttype": "none"})
GROUPS = [("anglosphere", "Anglosphere", green), ("europe", "Rest of Europe", accent), ("rest", "Rest of world", gray)]
MIN_VISITS = 30
TAIWAN_POP = 23_400_000
Y_LABEL = "Share of visits ÷ share of world population"
xfmt = FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:g}")
yfmt = FuncFormatter(lambda v, _: f"{v:g}x")


def save(fig, name, dpi=220):
    for ext in ["png", "svg"]:
        fig.savefig(OUT / f"{name}.{ext}", dpi=dpi, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def style(ax):
    ax.grid(color=rule, lw=0.8, which="major")
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(gray)


def table(name, title, header, rows, widths=None):
    """A ranked list rendered as an image (same layout as plot_charts.py, no subtitle or footer).
    The last column is bold."""
    widths = widths or [0.42, 0.14, 0.16, 0.16, 0.12]
    row_h, top_pad, bottom_pad = 0.36, 1.05, 0.25
    height = top_pad + row_h * (len(rows) + 1) + bottom_pad
    fig = plt.figure(figsize=(9, height), facecolor="white")
    y_in = lambda inches: 1 - inches / height
    fig.text(0.04, y_in(0.45), title, fontsize=17, weight="bold", va="center")
    xs = 0.04 + np.concatenate([[0], np.cumsum(widths[:-1])]) * 0.92
    right = 0.04 + np.cumsum(widths) * 0.92
    for i, (h, x, r) in enumerate(zip(header, xs, right)):
        fig.text(x if i == 0 else r, y_in(top_pad), h, fontsize=10, color=muted,
                 ha="left" if i == 0 else "right", va="center")
    for j, row in enumerate(rows, start=1):
        yc = y_in(top_pad + j * row_h)
        line = y_in(top_pad + (j - 0.5) * row_h)
        fig.add_artist(Line2D([0.04, 0.96], [line, line], color=rule if j > 1 else gray, lw=0.8))
        for i, (cell, x, r) in enumerate(zip(row, xs, right)):
            fig.text(x if i == 0 else r, yc, cell, fontsize=12, color=ink, va="center",
                     ha="left" if i == 0 else "right", weight="bold" if i == len(row) - 1 else "normal")
    save(fig, name)


pct = lambda x: f"{x:.3%}" if x < 0.001 else f"{x:.1%}" if x >= 0.01 else f"{x:.2%}"

# --- Tables: top 5 by visits, top 5 by visits per person ---------------------------------
visits = pd.read_csv(HERE / "goatcounter-locations.csv", keep_default_na=False)
TOTAL = visits["visits"].sum()
known = visits[visits["country"] != "(unknown)"].copy()
pop = {r["countryiso3code"]: r["value"] for r in json.loads((HERE / "worldbank-population-2024.json").read_text())[1]
       if r["value"]}
WORLD = pop["WLD"]
pop["TWN"] = TAIWAN_POP
known["share"] = known["visits"] / TOTAL
known["pop_share"] = known["iso3"].map(pop) / WORLD
known["ratio"] = known["share"] / known["pop_share"]

top = known.nlargest(5, "visits")
table("top-5-countries", "Top 5 countries by visits", ["Country", "Visits", "Share of visits"],
      [[c, f"{v:,}", pct(s)] for c, v, s in zip(top.country, top.visits, top.share)],
      widths=[0.6, 0.2, 0.2])
per = known[known["visits"] >= MIN_VISITS].nlargest(5, "ratio")
table("top-5-per-person", "Top 5 countries by visits per person",
      ["Country", "Visits", "Visit share", "Population share", "Ratio"],
      [[c, f"{v:,}", pct(s), pct(p), f"{r:.1f}x"]
       for c, v, s, p, r in zip(per.country, per.visits, per.share, per.pop_share, per.ratio)])

# --- Feature table and the variables shown in the grid ------------------------------------
f = pd.read_csv(HERE / "country-features.csv")
assert len(f) == 50 and not f.isna().any().any()
y = f["visit_ratio"].to_numpy()
popm = f["population"].to_numpy() / 1e6


def per_million(col):
    n = f[col].to_numpy()
    return np.maximum(n, 0.5) / popm, list(f.country[n == 0])


yc_x, yc_none = per_million("yc_companies")
nord_x, nord_none = per_million("nordvpn_servers")
none_note = lambda z: f" ({', '.join(z)}: none)" if z else ""
# key: (values, panel title, x label, log x?, countries left out of the fit)
VARS = {
    "papers": (f["papers_per_million"].to_numpy(), "Scientific papers", "Journal articles per million people", True, []),
    "yc": (yc_x, "YC startups", "Startups per million people" + none_note(yc_none), True, yc_none),
    "beer": (f["beer_litres"].to_numpy(), "Beer drinking", "Litres of pure alcohol from beer per adult per year", False, []),
    "nordvpn": (nord_x, "NordVPN servers", "Servers per million people" + none_note(nord_none), True, nord_none),
    "gdp": (f["gdp_per_capita"].to_numpy() / 1000, "GDP per capita", "US$ thousands, 2024", True, []),
    "english": (f["english_pct"].to_numpy(), "English speakers", "% of population", False, []),
    "broadband": (f["broadband_per_100"].to_numpy(), "Home broadband", "Fixed subscriptions per 100 people", False, []),
    "hours": (f["working_hours"].to_numpy(), "Working hours", "Hours per worker per year", False, []),
    "population": (popm, "Population", "Millions of people", True, []),
    "happiness": (f["happiness"].to_numpy(), "Happiness", "Life satisfaction, 0–10", False, []),
    "social": (f["social_media_min_per_day"].to_numpy(), "Social media time", "Minutes per day", False, []),
    "age": (f["median_age"].to_numpy(), "Median age", "Years", False, []),
    "vpnuse": (f["vpn_downloads_per_100"].to_numpy(), "VPN app downloads", "Downloads per 100 people, 2024", True, []),
    "alcohol": (f["total_alcohol_litres"].to_numpy(), "All alcohol", "Litres of pure alcohol per adult per year", False, []),
    "freelance": (f["freelancers_vs_world"].to_numpy(), "Freelancers", "Online freelancers per person, × world average", True, []),
    "obesity": (f["obesity_pct"].to_numpy(), "Obesity", "% of adults", False, []),
}
IN_TITLE = {"papers", "yc", "beer"}


def simple_fit(key):
    x, _, _, logx, skip = VARS[key]
    use = ~f.country.isin(skip).to_numpy()
    lx = np.log10(x) if logx else x
    return sm.OLS(np.log10(y[use]), sm.add_constant(lx[use])).fit(), lx, use


fits = {k: simple_fit(k)[0] for k in VARS}
order = sorted(VARS, key=lambda k: -fits[k].rsquared)

# --- 4 x 4 grid of every variable against visits per person -------------------------------
fig, axes = plt.subplots(4, 4, figsize=(16, 16.5), facecolor="white")
fig.text(0.015, 0.995, "Sixteen country traits against HN visits per person", fontsize=21, weight="bold", va="top")
for i, (ax, key) in enumerate(zip(axes.flat, order)):
    x, title, xlabel, logx, skip = VARS[key]
    fit, lx, use = simple_fit(key)
    grid = np.linspace(lx[use].min(), lx[use].max(), 100)
    pr = fit.get_prediction(sm.add_constant(grid)).summary_frame(alpha=0.05)
    gx = 10 ** grid if logx else grid
    ax.fill_between(gx, 10 ** pr["mean_ci_lower"], 10 ** pr["mean_ci_upper"], color=rule, alpha=0.9, lw=0, zorder=1)
    ax.plot(gx, 10 ** pr["mean"], color=ink, lw=1.1, ls=(0, (4, 3)), zorder=2)
    for gk, gl, c in GROUPS:
        m = (f["group"] == gk).to_numpy()
        ax.scatter(x[m], y[m], s=24, color=c, edgecolor="white", linewidth=0.6, zorder=3, label=gl)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(yfmt)
    if logx:
        ax.set_xscale("log")
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_minor_formatter(NullFormatter())
    style(ax)
    slope = np.asarray(fit.params)[1]
    ax.set_title(f"{title}   R² {fit.rsquared:.2f}{'' if slope > 0 else ', negative'}", loc="left", fontsize=13,
                 weight="bold", color=green if key in IN_TITLE else ink)
    ax.set_xlabel(xlabel, fontsize=9.5)
    if i % 4 == 0:
        ax.set_ylabel("Visits ÷ population share", fontsize=10)
    ax.tick_params(labelsize=9)
axes.flat[0].legend(loc="lower right", frameon=False, fontsize=9)
fig.tight_layout(rect=(0, 0, 1, 0.975), h_pad=2.4, w_pad=1.6)
save(fig, "sixteen-traits-vs-visits", dpi=160)

# --- Three-variable model and the model without beer --------------------------------------
X = pd.DataFrame({"papers": np.log10(f["papers_per_million"]),
                  "yc": np.log10((f["yc_companies"] + 0.5) / f["population"] * 1e6),  # +0.5 so zero is defined
                  "beer": f["beer_litres"]})
ly = np.log10(y)
three = sm.OLS(ly, sm.add_constant(X)).fit()
no_beer = sm.OLS(ly, sm.add_constant(X[["papers", "yc"]])).fit()
resid = ly - no_beer.fittedvalues
print(f"papers + YC + beer: R2 {three.rsquared:.3f} (adj {three.rsquared_adj:.3f}); p = "
      + ", ".join(f"{k} {v:.4f}" for k, v in three.pvalues.drop('const').items()))
print(f"papers + YC only:   R2 {no_beer.rsquared:.3f}; corr(beer, residual) = {np.corrcoef(f['beer_litres'], resid)[0, 1]:+.2f}")

LABEL = {"United States": "US", "United Kingdom": "UK"}

# Predicted vs actual for the three-variable model, with a 95% prediction band around actual = predicted.
from matplotlib.patches import Patch
from scipy import stats

p3 = 10 ** three.fittedvalues.to_numpy()
band = 10 ** (stats.t.ppf(0.975, three.df_resid) * np.sqrt(three.scale))
print(f"95% prediction band: ÷/× {band:.2f}; outside: {list(f.country[np.abs(three.resid) > np.log10(band)])}")
fig = plt.figure(figsize=(9, 8.4), facecolor="white")
fig.text(0.04, 0.965, "Scientific papers + startups + beer", fontsize=17, weight="bold")
ax = fig.add_axes([0.11, 0.07, 0.85, 0.86])
lo, hi = min(p3.min(), y.min()) / 1.5, max(p3.max(), y.max()) * 1.5
ax.fill_between([lo, hi], [lo / band, hi / band], [lo * band, hi * band], color=rule, alpha=0.8, lw=0, zorder=1)
ax.plot([lo, hi], [lo, hi], color=ink, lw=1.2, ls=(0, (4, 3)), zorder=2)
ax.scatter(p3, y, s=46, color=green, edgecolor="white", linewidth=1.2, zorder=3)
texts = [ax.text(a, b, LABEL.get(n, n), fontsize=8.5, color=ink, zorder=4) for a, b, n in zip(p3, y, f.country)]
ax.set(xscale="log", yscale="log", xlim=(lo, hi), ylim=(lo, hi), aspect="equal",
       xlabel="Predicted by scientific papers, YC startups and beer", ylabel="Actual: " + Y_LABEL.lower())
ax.xaxis.set_major_formatter(yfmt)
ax.yaxis.set_major_formatter(yfmt)
style(ax)
ax.legend(handles=[Patch(color=rule, label="95% prediction band")], loc="lower right", frameon=False, fontsize=10)
adjust_text(texts, x=p3, y=y, ax=ax, expand=(1.3, 1.6), arrowprops={"arrowstyle": "-", "color": gray, "lw": 0.6})
save(fig, "model-predicted-vs-actual")

pred, actual, beer = 10 ** no_beer.fittedvalues.to_numpy(), y, f["beer_litres"].to_numpy()
size = lambda litres: 18 + 70 * litres
fig = plt.figure(figsize=(9, 8.4), facecolor="white")
fig.text(0.04, 0.965, "Scientific papers + startups", fontsize=17, weight="bold")
ax = fig.add_axes([0.11, 0.07, 0.85, 0.86])
lo, hi = min(pred.min(), actual.min()) / 1.5, max(pred.max(), actual.max()) * 1.5
ax.plot([lo, hi], [lo, hi], color=ink, lw=1.2, ls=(0, (4, 3)), zorder=2)
ax.scatter(pred, actual, s=size(beer), color=green, alpha=0.75, edgecolor="white", linewidth=1, zorder=3)
texts = [ax.text(a, b, {"United States": "US", "United Kingdom": "UK"}.get(n, n), fontsize=8.5, color=ink, zorder=4)
         for a, b, n in zip(pred, actual, f.country)]
ax.text(0.015, 0.97, "Above the dashed line: more visits than the model predicts", transform=ax.transAxes,
        fontsize=10, color=ink, va="top")
ax.set(xscale="log", yscale="log", xlim=(lo, hi), ylim=(lo, hi), aspect="equal",
       xlabel="Predicted by scientific papers and YC startups", ylabel="Actual: " + Y_LABEL.lower())
ax.xaxis.set_major_formatter(yfmt)
ax.yaxis.set_major_formatter(yfmt)
style(ax)
sizes = [plt.scatter([], [], s=size(v), color=green, alpha=0.75, edgecolor="white", label=f"{v} litre{'' if v == 1 else 's'} of beer")
         for v in (1, 3, 6)]
ax.legend(handles=sizes, loc="lower right", frameon=False, fontsize=9.5, labelspacing=1.1, borderpad=1)
adjust_text(texts, x=pred, y=actual, ax=ax, expand=(1.3, 1.6),
            arrowprops={"arrowstyle": "-", "color": gray, "lw": 0.6})
save(fig, "model-without-beer")
