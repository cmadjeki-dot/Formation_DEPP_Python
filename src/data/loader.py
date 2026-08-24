"""Fonctions de chargement et sauvegarde des données."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_csv(path: str | Path) -> pd.DataFrame:
    """Charge un fichier CSV dans un DataFrame."""
    return pd.read_csv(path)


def save_csv(data: pd.DataFrame, path: str | Path) -> Path:
    """Sauvegarde un DataFrame au format CSV."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)
    return output_path


def data_path(*parts: str) -> Path:
    """Construit un chemin absolu depuis la racine du projet."""
    return PROJECT_ROOT.joinpath(*parts)
