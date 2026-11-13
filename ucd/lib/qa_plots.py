"""Shared figure helpers for the QA plots (publication style, LaTeX fonts, PNG)."""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ucd.lib.run_state import repository_root  # noqa: E402

sys.path.insert(0, str(repository_root / "scripts"))
import plot_style  # noqa: E402

plot_style.use_publication_style()
single_width = plot_style.figure_width_single
double_width = plot_style.figure_width_double

colors = {
    "all": "0.6",
    "star": "#4477AA",
    "selected": "#EE7733",
    "known": "#CC3311",
    "candidate": "#009988",
    "control": "#AA4499",
    "galaxy": "#BBBB44",
}


def save(figure, folder: Path, name: str) -> Path:
    path = Path(folder) / f"{name}.png"
    figure.savefig(path)
    plt.close(figure)
    print(f"  figure: {path}")
    return path
