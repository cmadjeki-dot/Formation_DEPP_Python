"""Helpers de visualisation."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_distribution(series: pd.Series, title: str = "Distribution") -> None:
    """Affiche l'histogramme d'une série."""
    plt.figure(figsize=(8, 5))
    series.plot(kind="hist", title=title)
    plt.tight_layout()
    plt.show()
