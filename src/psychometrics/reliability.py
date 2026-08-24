"""Fonctions psychométriques simples."""

from __future__ import annotations

import pandas as pd


def item_corr_matrix(data: pd.DataFrame) -> pd.DataFrame:
    """Calcule la matrice des corrélations entre items."""
    return data.corr()
