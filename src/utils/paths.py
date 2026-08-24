"""Utilitaires de gestion des chemins."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def ensure_dir(path: str | Path) -> Path:
    """Crée un dossier s'il n'existe pas."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory
