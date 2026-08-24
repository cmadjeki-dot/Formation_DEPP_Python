"""Contrôle qualité des données."""

from __future__ import annotations

import pandas as pd


def missing_values_report(data: pd.DataFrame) -> pd.Series:
    """Renvoie le nombre de valeurs manquantes par colonne."""
    return data.isna().sum()


def duplicate_count(data: pd.DataFrame) -> int:
    """Compte le nombre de lignes dupliquées."""
    return int(data.duplicated().sum())


def outlier_mask(series: pd.Series, lower: float | None = None, upper: float | None = None) -> pd.Series:
    """Retourne le masque des valeurs hors intervalle."""
    if lower is None:
        lower = series.min()
    if upper is None:
        upper = series.max()
    return (series < lower) | (series > upper)


def summarize_quality(data: pd.DataFrame) -> pd.DataFrame:
    """Produit un résumé rapide pour le contrôle qualité."""
    summary = []
    for column in data.columns:
        s = data[column]
        summary.append(
            {
                "variable": column,
                "n_missing": int(s.isna().sum()),
                "pct_missing": round(float(s.isna().mean() * 100), 2),
                "n_unique": int(s.nunique()),
                "dtype": str(s.dtype),
            }
        )
    return pd.DataFrame(summary)
