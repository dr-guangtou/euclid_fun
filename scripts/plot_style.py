"""Shared publication-quality matplotlib style (LaTeX fonts) for the figures in figures/."""

import matplotlib as mpl

figure_width_single = 3.5  # inches, one A&A column
figure_width_double = 7.2  # inches, full A&A page width


def use_publication_style(use_tex: bool = True) -> None:
    mpl.rcParams.update(
        {
            "text.usetex": use_tex,
            "font.family": "serif",
            "font.serif": ["Computer Modern Roman"],
            "text.latex.preamble": r"\usepackage{amsmath}\usepackage{amssymb}",
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 9,
            "legend.fontsize": 7.5,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "xtick.minor.visible": True,
            "ytick.minor.visible": True,
            "xtick.major.size": 4,
            "ytick.major.size": 4,
            "xtick.minor.size": 2,
            "ytick.minor.size": 2,
            "axes.linewidth": 0.7,
            "axes.grid": False,  # the user's ~/.matplotlib/matplotlibrc turns grids on
            "lines.linewidth": 1.1,
            "legend.frameon": False,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.03,
            "image.origin": "lower",
            "image.interpolation": "nearest",
        }
    )
