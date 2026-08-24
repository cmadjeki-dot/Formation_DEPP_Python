"""Simulation d'une base DEPP sur les performances en lecture."""

from __future__ import annotations

import numpy as np
import pandas as pd


ACADEMIES = [
    "Paris", "Lyon", "Marseille", "Toulouse", "Nancy", "Bordeaux", "Nantes", "Lille"
]
PCS_LEVELS = ["Ouvrier", "Employe", "Cadre", "Professions_intermediaires", "Agriculteur", "Retraite"]
SEXE_VALUES = ["F", "M"]
TYPE_ETAB = ["Public", "Prive"]


def generate_student_dataset(n_students: int = 15000, seed: int = 42) -> pd.DataFrame:
    """Génère une base simulée de 15 000 élèves de 6e.

    Les variables sont inspirées du protocole statistique décrit dans le projet DEPP.
    """
    rng = np.random.default_rng(seed)

    n = int(n_students)
    data = pd.DataFrame(
        {
            "id_eleve": np.arange(1, n + 1),
            "sexe": rng.choice(SEXE_VALUES, size=n),
            "pcs": rng.choice(PCS_LEVELS, size=n),
            "retard": rng.binomial(1, 0.18, size=n),
            "academie": rng.choice(ACADEMIES, size=n),
            "type_etab": rng.choice(TYPE_ETAB, size=n),
            "ressources_num": rng.normal(0.5, 0.2, size=n),
            "age": rng.integers(10, 14, size=n),
            "score_lecture": np.zeros(n, dtype=float),
        }
    )

    pcs_score = {
        "Ouvrier": -12,
        "Employe": -5,
        "Professions_intermediaires": 2,
        "Cadre": 12,
        "Agriculteur": -4,
        "Retraite": -8,
    }

    data["score_lecture"] = (
        55
        + data["ressources_num"] * 22
        + data["retard"].map({0: 6, 1: -14})
        + data["sexe"].map({"F": 1.5, "M": 0})
        + data["pcs"].map(pcs_score)
        + rng.normal(0, 9, size=n)
    )

    data["score_lecture"] = data["score_lecture"].clip(0, 100)
    data["score_lecture"] = data["score_lecture"].round(2)
    return data


def inject_quality_issues(data: pd.DataFrame, missing_rate: float = 0.03) -> pd.DataFrame:
    """Ajoute des anomalies réalistes : valeurs manquantes, doublons et outliers."""
    result = data.copy()
    rng = np.random.default_rng(123)

    missing_mask = rng.random(result.shape[0]) < missing_rate
    result.loc[missing_mask, "score_lecture"] = np.nan

    duplicate_indices = rng.choice(result.index, size=max(1, len(result) // 1000), replace=False)
    result = pd.concat([result, result.loc[duplicate_indices]], ignore_index=True)

    outlier_index = rng.integers(0, len(result), size=max(1, len(result) // 200))
    result.loc[outlier_index, "score_lecture"] = 150 + rng.normal(0, 5, size=len(outlier_index))

    return result


def export_dataset(path: str, data: pd.DataFrame) -> None:
    """Exporte la base simulée en CSV."""
    data.to_csv(path, index=False)
