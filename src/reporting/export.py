"""Export de résultats et tableaux."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_csv(data: pd.DataFrame, path: str | Path) -> None:
    """Exporte un DataFrame en CSV."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)
