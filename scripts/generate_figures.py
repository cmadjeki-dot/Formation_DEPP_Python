import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.loader import data_path, load_csv

fig_dir = ROOT / 'outputs' / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)

# Load cleaned data
clean_path = data_path('data', 'interim', 'etude_lecture_6e_clean.csv')
if not Path(clean_path).exists():
    # fallback to raw
    clean_path = data_path('src', 'data', 'raw', 'etude_lecture_6e.csv')

df = load_csv(clean_path)

# 1. Mean score by PCS
if 'pcs' in df.columns and 'score_lecture' in df.columns:
    mean_by_pcs = df.groupby('pcs')['score_lecture'].mean().sort_values(ascending=False)
    ax = mean_by_pcs.plot(kind='bar', figsize=(10, 6), color='steelblue')
    ax.set_title('Score moyen en lecture par PCS')
    ax.set_xlabel('PCS')
    ax.set_ylabel('Score moyen')
    plt.tight_layout()
    plt.savefig(fig_dir / 'score_par_pcs.png')
    plt.close()

# 2. Distribution of score_lecture
if 'score_lecture' in df.columns:
    plt.figure(figsize=(10, 6))
    plt.hist(df['score_lecture'].dropna(), bins=30, color='darkorange', edgecolor='black')
    plt.title('Distribution du score de lecture')
    plt.xlabel('Score lecture')
    plt.ylabel('Fréquence')
    plt.tight_layout()
    plt.savefig(fig_dir / 'distribution_score_lecture.png')
    plt.close()

# 3. Boxplot by sexe
if 'sexe' in df.columns and 'score_lecture' in df.columns:
    plt.figure(figsize=(8,6))
    df.boxplot(column='score_lecture', by='sexe')
    plt.title('Score lecture par sexe')
    plt.suptitle('')
    plt.xlabel('Sexe')
    plt.ylabel('Score lecture')
    plt.tight_layout()
    plt.savefig(fig_dir / 'boxplot_score_by_sexe.png')
    plt.close()

print('Figures saved to', fig_dir)
