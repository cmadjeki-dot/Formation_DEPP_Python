# Projet DEPP Python

Projet pédagogique de production statistique publique appliquée à l’évaluation éducative.

## Objectif

Étudier l’impact du contexte socio-économique sur les performances en lecture des élèves de 6e, en reproduisant une logique de travail proche de la DEPP.

## Structure du projet

- `dashboard/` : application Streamlit de restitution
- `src/data/raw/` : données brutes simulées
- `src/data/interim/` : données nettoyées intermédiaires
- `data/processed/` : emplacement réservé aux données prêtes à l’analyse
- `docs/` : documentation et rapport final
- `notebooks/` : séquence d’analyse complète
- `src/` : code réutilisable Python
- `tests/` : tests automatisés
- `outputs/` : figures, modèles et rapports

## Architecture cible finale

L'organisation cible du projet est la suivante :

```text
Formation_DEPP_Python
│
├── dashboard
│   └── app.py
│
├── data
│   ├── external
│   ├── raw
│   ├── interim
│   └── processed
│
├── docs
│   └── rapport_final.md
│
├── notebooks
│   ├── 00_cadrage_du_projet.ipynb
│   ├── 01_generation_ou_acquisition_des_donnees.ipynb
│   ├── 02_importation_et_description.ipynb
│   ├── 03_controle_qualite.ipynb
│   ├── 04_nettoyage_et_valeurs_manquantes.ipynb
│   ├── 05_analyse_descriptive.ipynb
│   ├── 06_modelisation.ipynb
│   ├── 07_analyse_specialisee.ipynb
│   ├── 08_analyse_longitudinale.ipynb
│   ├── 09_analyse_causale.ipynb
│   ├── 10_indicateurs_decisionnels.ipynb
│   ├── 11_restitution_decisionnelle.ipynb
│   ├── 12_pipeline_complet.ipynb
│   └── 13_presentation_orale_finale.ipynb
│
├── outputs
│   ├── figures
│   ├── logs
│   ├── models
│   ├── reports
│   └── tables
│
├── src
│   ├── analysis
│   ├── data
│   ├── modeling
│   ├── quality
│   ├── reporting
│   ├── utils
│   └── visualization
│
├── tests
│
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

Cette arborescence décrit la séparation entre les données, les analyses,
la modélisation, la qualité, la visualisation et les restitutions.

## Environnement

Le projet utilise un environnement virtuel local dans :

- `C:\Users\admin\Desktop\Formation_DEPP_Python\.venv\Scripts\python.exe`

## Démarrage

1. Ouvrir VS Code.
2. Sélectionner l’interpréteur `.venv\Scripts\python.exe`.
3. Ouvrir un notebook dans `notebooks/`.
4. Choisir le kernel `Python (Formation DEPP)`.
5. Lancer le notebook `12_pipeline_complet.ipynb` pour exécuter la chaîne complète.

## Chaîne de travail

- 00 : cadrage du projet
- 01 : génération des données
- 02 : importation et description
- 03 : contrôle qualité
- 04 : traitement des valeurs manquantes
- 05 : analyse descriptive
- 06 : régression linéaire
- 07 : psychométrie
- 08 : analyse longitudinale
- 09 : analyse causale
- 10 : indicateurs décisionnels
- 11 : restitution ministérielle
- 12 : pipeline complet

## Documentation

- [docs/rapport_final.md](docs/rapport_final.md)

## Consulter les résultats

- **Dashboard interactif** : lancer `.venv\Scripts\python.exe -m streamlit run dashboard\app.py`, puis ouvrir <http://localhost:8501>.
- **Galerie statique** : ouvrir [site/index.html](site/index.html) localement ou le site GitHub Pages après activation de la publication.
- **Tableaux HTML** : voir [outputs/tables](outputs/tables).
- **Rapport de synthèse** : voir [outputs/reports/rapport_synthese.html](outputs/reports/rapport_synthese.html).
- **Notebooks** : voir [notebooks](notebooks).
- **Méthodologie** : voir [docs/rapport_final.md](docs/rapport_final.md).

## Validation

Les tests du module de simulation de données passent avec succès.
