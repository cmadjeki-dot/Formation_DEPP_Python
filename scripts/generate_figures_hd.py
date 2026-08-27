import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.loader import data_path, load_csv

fig_dir = ROOT / 'outputs' / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)

# Load cleaned data
clean_path = data_path('data', 'interim', 'etude_lecture_6e_clean.csv')
if not Path(clean_path).exists():
    clean_path = data_path('data', 'raw', 'etude_lecture_6e.csv')

df = load_csv(clean_path)

# Ensure numeric columns
if 'score_lecture' in df.columns:
    df['score_lecture'] = pd.to_numeric(df['score_lecture'], errors='coerce')
if 'ressources_num' in df.columns:
    df['ressources_num'] = pd.to_numeric(df['ressources_num'], errors='coerce')

# Helper to save in png (300dpi) and pdf
def save_fig(fig, name):
    png_path = fig_dir / f"{name}.png"
    pdf_path = fig_dir / f"{name}.pdf"
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(pdf_path, bbox_inches='tight')
    plt.close(fig)
    print('Saved', png_path, pdf_path)

# 1. High-res bar: mean score by PCS
if 'pcs' in df.columns and 'score_lecture' in df.columns:
    mean_by_pcs = df.groupby('pcs')['score_lecture'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(x=mean_by_pcs.values, y=mean_by_pcs.index, palette='Blues_r', ax=ax)
    ax.set_title('Score moyen en lecture par PCS (HD)')
    ax.set_xlabel('Score moyen')
    ax.set_ylabel('PCS')
    save_fig(fig, 'score_par_pcs_hd')

# 2. High-res distribution with KDE
if 'score_lecture' in df.columns:
    fig, ax = plt.subplots(figsize=(12,8))
    sns.histplot(df['score_lecture'].dropna(), bins=40, kde=True, color='darkorange', ax=ax)
    ax.set_title('Distribution du score de lecture (HD)')
    ax.set_xlabel('Score lecture')
    ax.set_ylabel('Fréquence')
    save_fig(fig, 'distribution_score_lecture_hd')

# 3. Boxplot by PCS (if not too many categories)
if 'pcs' in df.columns and df['pcs'].nunique() <= 12:
    fig, ax = plt.subplots(figsize=(14,8))
    order = df.groupby('pcs')['score_lecture'].median().sort_values(ascending=False).index
    sns.boxplot(x='score_lecture', y='pcs', data=df, order=order, palette='pastel', ax=ax)
    ax.set_title('Boxplot score lecture par PCS (HD)')
    save_fig(fig, 'boxplot_score_by_pcs_hd')

# 4. Scatter score vs ressources_num with regression line
if 'score_lecture' in df.columns and 'ressources_num' in df.columns:
    fig, ax = plt.subplots(figsize=(10,8))
    sns.regplot(x='ressources_num', y='score_lecture', data=df.sample(min(len(df), 5000), random_state=1), scatter_kws={'s':10, 'alpha':0.3}, line_kws={'color':'red'}, ax=ax)
    ax.set_title('Score lecture vs ressources numériques (HD)')
    ax.set_xlabel('Ressources numériques (normalisé)')
    ax.set_ylabel('Score lecture')
    save_fig(fig, 'scatter_score_vs_ressources_hd')

# 5. Correlation heatmap of numeric variables
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(num_cols) >= 2:
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    ax.set_title('Matrice de corrélation (HD)')
    save_fig(fig, 'correlation_heatmap_hd')

print('All high-res figures generated in', fig_dir)
