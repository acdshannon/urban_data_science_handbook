"""Shared matplotlib style for the Urban Data Science Handbook.

Figures print on paper as well as they glow on screen: light ground,
navy ink, the book's gold/teal accents. Chapters call set_style() once,
in their setup cell.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

# The book's palette (see styles/theme-*.scss)
NAVY = "#192738"
GOLD = "#b07d20"
TEAL = "#1d8a8d"
BRICK = "#a84b3c"
SLATE = "#6b7a8f"
PLUM = "#7d5d86"
CREAM = "#fffdf7"
INK = "#1f2d3d"
FAINT = "#9aa3ad"

PALETTE = [NAVY, GOLD, TEAL, BRICK, SLATE, PLUM]

# Sequential ramp for choropleths and heatmaps: cream -> teal -> navy
CMAP_SEQ = mpl.colors.LinearSegmentedColormap.from_list(
    "book_seq", [CREAM, "#cfe3e0", TEAL, "#14545c", NAVY]
)
# Diverging ramp: brick -> cream -> teal
CMAP_DIV = mpl.colors.LinearSegmentedColormap.from_list(
    "book_div", [BRICK, "#e9c1b3", CREAM, "#bcd9d6", TEAL]
)
mpl.colormaps.register(CMAP_SEQ, name="book_seq", force=True)
mpl.colormaps.register(CMAP_DIV, name="book_div", force=True)


def set_style():
    plt.rcParams.update(
        {
            "figure.figsize": (8, 4.5),
            "figure.dpi": 110,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
            "font.family": "serif",
            "font.serif": [
                "Palatino Linotype",
                "Palatino",
                "P052",
                "URW Palladio L",
                "Georgia",
                "DejaVu Serif",
            ],
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 12,
            "axes.labelsize": 11,
            "axes.labelcolor": INK,
            "axes.edgecolor": FAINT,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#e4e1d8",
            "grid.linewidth": 0.6,
            "axes.axisbelow": True,
            "axes.prop_cycle": cycler(color=PALETTE),
            "xtick.color": INK,
            "ytick.color": INK,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.frameon": False,
            "legend.fontsize": 10,
            "text.color": INK,
            "lines.linewidth": 1.8,
        }
    )


def note(ax, text, xy, xytext, color=INK):
    """Direct annotation with a quiet connector — the book labels lines and
    events on the figure itself rather than in legends where it can."""
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        fontsize=9.5,
        fontstyle="italic",
        color=color,
        arrowprops={"arrowstyle": "-", "color": FAINT, "lw": 0.8, "shrinkB": 3},
    )
