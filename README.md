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
