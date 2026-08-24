"""Analyse descriptive de base."""

from __future__ import annotations

import pandas as pd


def summary_by_group(data: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    """Retourne les statistiques descriptives par groupe."""
    return data.groupby(group_col)[value_col].describe().reset_index()
