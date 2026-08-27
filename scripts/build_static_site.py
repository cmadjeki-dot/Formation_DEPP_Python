import html
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data" / "interim" / "etude_lecture_6e_clean.csv"
FIGURES = ROOT / "outputs" / "figures"
TABLES = ROOT / "outputs" / "tables"
REPORTS = ROOT / "outputs" / "reports"
SITE = ROOT / "site"

for directory in (FIGURES, TABLES, REPORTS, SITE):
    directory.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA)
by_pcs = df.groupby("pcs", as_index=False).agg(score_moyen=("score_lecture", "mean"), effectif=("id_eleve", "count"))
by_sexe = df.groupby("sexe", as_index=False).agg(score_moyen=("score_lecture", "mean"), effectif=("id_eleve", "count"))
by_retard = df.groupby("retard", as_index=False).agg(score_moyen=("score_lecture", "mean"), effectif=("id_eleve", "count"))

tables = {"scores_par_pcs": by_pcs, "scores_par_sexe": by_sexe, "scores_par_retard": by_retard}
for name, table in tables.items():
    table.to_html(TABLES / f"{name}.html", index=False, classes="data-table", border=0)

(REPORTS / "rapport_synthese.html").write_text(
    """<!doctype html><html lang="fr"><meta charset="utf-8"><title>Rapport DEPP</title>
<h1>Rapport de synthèse DEPP</h1><p>Étude simulée sur les performances en lecture des élèves de 6e.</p>
<p>Les résultats descriptifs montrent des écarts selon la PCS et le retard scolaire. Les notebooks documentent la méthodologie complète.</p>
<p><a href="../../docs/rapport_final.md">Rapport méthodologique Markdown</a></p>""",
    encoding="utf-8",
)

cards = [
    ("score_par_pcs_hd.png", "Score moyen par PCS", "Les écarts de score sont présentés par catégorie socioprofessionnelle."),
    ("distribution_score_lecture_hd.png", "Distribution des scores", "La distribution décrit la dispersion des performances observées."),
    ("boxplot_score_by_pcs_hd.png", "Dispersion par PCS", "Le boxplot compare médianes et dispersion entre PCS."),
    ("scatter_score_vs_ressources_hd.png", "Score et ressources numériques", "Relation descriptive entre ressources numériques et score."),
    ("correlation_heatmap_hd.png", "Matrice de corrélation", "Corrélations entre variables numériques de la base."),
]
cards_html = "\n".join(
    f'<article><h3>{html.escape(title)}</h3><img src="figures/{filename}" alt="{html.escape(title)}"><p>{html.escape(description)}</p></article>'
    for filename, title, description in cards
)
links = "\n".join(f'<li><a href="tables/{name}.html">{name.replace("_", " ").title()}</a></li>' for name in tables)
index = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Formation DEPP — Restitution</title><style>
body{{font-family:system-ui,Arial;margin:0;background:#f5f7fb;color:#172033}}main{{max-width:1180px;margin:auto;padding:32px}}
header{{background:#123b63;color:white;padding:36px;border-radius:12px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}}
article,.panel{{background:white;padding:18px;border-radius:10px;box-shadow:0 2px 8px #0001}}img{{width:100%;height:220px;object-fit:contain}}
a{{color:#075ca8}}.kpi{{font-size:1.5rem;font-weight:bold}}
</style></head><body><main><header><h1>Formation DEPP Python</h1>
<p>Mini-site de restitution de l'étude sur la lecture en 6e.</p>
<p><a href="https://github.com/cmadjeki-dot/Formation_DEPP_Python" style="color:white">Voir le dépôt GitHub</a>
 · <a href="https://streamlit.io/cloud" style="color:white">Déployer le dashboard Streamlit</a></p></header>
<section class="panel"><h2>Indicateurs principaux</h2><div class="grid">
<div><div class="kpi">{len(df):,}</div>élèves</div><div><div class="kpi">{df.score_lecture.mean():.2f}</div>score moyen</div>
<div><div class="kpi">{df.retard.mean()*100:.1f}%</div>avec retard</div></div></section>
<h2>Galerie des graphiques</h2><section class="grid">{cards_html}</section>
<section class="panel"><h2>Tableaux principaux</h2><ul>{links}</ul>
<p><a href="reports/rapport_synthese.html">Lire le rapport de synthèse</a> · <a href="https://github.com/cmadjeki-dot/Formation_DEPP_Python/tree/main/notebooks">Consulter les notebooks</a></p></section>
<footer><p>Projet pédagogique — données simulées — génération reproductible par <code>scripts/build_static_site.py</code>.</p></footer>
</main></body></html>"""
(SITE / "index.html").write_text(index, encoding="utf-8")
print(f"Static site generated in {SITE}")
