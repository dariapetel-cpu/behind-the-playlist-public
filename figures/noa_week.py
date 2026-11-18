"""Chapter 2 figure: Noa's fictional week, plays vs. skips by hour of day.

FICTIONAL DATA. Reads figures/data/noa_week.csv and writes book/figures/noa_week.pdf
(vector) plus a printed summary used to brief the Writer.

Hebrew labels: matplotlib >= 3.11 lays out RTL text itself. Hebrew strings are passed in
natural (logical) order. Do NOT apply python-bidi's get_display(): it reverses the letters
a second time (verified 2026-11-14 at glyph level, see docs/prompts.md, Prompt 10).
Run:  .venv/bin/python figures/noa_week.py
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "figures" / "data" / "noa_week.csv"
OUT = ROOT / "book" / "figures" / "noa_week.pdf"

# Book palette (Prompt 13; same hex values as book/style.sty). Green/pink are used only for
# bar fills (non-text graphics); all text is charcoal or muted grey (>= 6.7:1 on the page colour).
GREEN, PINK, CHARCOAL, MUTED, GRID, PAGE = "#1ED760", "#FF2E88", "#121212", "#555555", "#D4D4D4", "#F2F2F2"

for f in ("/System/Library/Fonts/Supplemental/Arial.ttf",
          "/System/Library/Fonts/Supplemental/Arial Bold.ttf"):
    font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Arial", "font.size": 9, "pdf.fonttype": 42,
                     "axes.edgecolor": MUTED, "xtick.color": CHARCOAL, "ytick.color": CHARCOAL,
                     "figure.facecolor": PAGE, "axes.facecolor": PAGE, "savefig.facecolor": PAGE,
                     "hatch.color": CHARCOAL, "hatch.linewidth": 0.6, "text.color": CHARCOAL})

def he(s: str) -> str:
    """Identity: kept as one hook in case a matplotlib without RTL layout is used."""
    assert int(matplotlib.__version__.split(".")[0]) >= 3 and int(matplotlib.__version__.split(".")[1]) >= 11, \
        "matplotlib < 3.11 does not lay out RTL text; use python-bidi get_display here"
    return s

def load():
    rows = [r for r in csv.reader(l for l in DATA.open(encoding="utf-8") if not l.startswith("#"))]
    head, body = rows[0], rows[1:]
    assert head == ["hour", "plays", "skips"]
    return [int(r[0]) for r in body], [int(r[1]) for r in body], [int(r[2]) for r in body]

def main():
    hours, plays, skips = load()
    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    w = 0.78
    ax.bar(hours, plays, w, color=GREEN, label=he("השמעות (האזנה של יותר מ־30 שניות)"),
           edgecolor=PAGE, linewidth=0.8, zorder=2)
    ax.bar(hours, skips, w, bottom=plays, color=PINK, label=he("דילוגים"),
           edgecolor=PAGE, linewidth=0.8, hatch="////", zorder=2)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], fontsize=7.5)
    ax.set_xlim(-0.7, 23.7)
    ax.set_xlabel(he("שעה ביום"), color=CHARCOAL)
    ax.set_ylabel(he("מספר שירים בשבוע"), color=CHARCOAL)
    ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    # Direct labels on the three moments the chapter talks about
    notes = {8: "אוטובוס", 18: "חדר כושר", 22: "לימודים"}
    for h, txt in notes.items():
        ax.annotate(he(txt), (h, plays[h] + skips[h]), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=8, color=CHARCOAL, fontweight="bold")
    ax.set_ylim(0, max(p + s for p, s in zip(plays, skips)) * 1.18)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    ax.text(0.995, 0.98, he("נתונים בדיוניים"), transform=ax.transAxes, ha="right", va="top",
            fontsize=7.5, color=MUTED, bbox=dict(boxstyle="round,pad=0.25", fc=PAGE, ec=MUTED, lw=0.6, ls="--"))
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)

    tp, ts = sum(plays), sum(skips)
    def share(hs): return sum(skips[h] for h in hs), sum(plays[h] + skips[h] for h in hs)
    print(f"total plays={tp} skips={ts} songs={tp+ts} skip_share={ts/(tp+ts):.1%}")
    for name, hs in {"bus 07-09": [7, 8], "gym 17-19": [17, 18], "study 22-24": [22, 23]}.items():
        s, n = share(hs)
        print(f"{name}: skips {s} of {n} songs = {s/n:.0%}")
    print(f"wrote {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
