import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "src" / "data" / "interim" / "etude_lecture_6e_clean.csv"
RAW_PATH = ROOT / "src" / "data" / "raw" / "etude_lecture_6e.csv"

st.set_page_config(page_title="DEPP — Restitution", page_icon="📊", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    path = DATA_PATH if DATA_PATH.exists() else RAW_PATH
    if not path.exists():
        raise FileNotFoundError(f"Donnée introuvable : {path}")
    data = pd.read_csv(path)
    data["score_lecture"] = pd.to_numeric(data["score_lecture"], errors="coerce")
    data["ressources_num"] = pd.to_numeric(data["ressources_num"], errors="coerce")
    return data


def download_csv(data: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    data.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


try:
    df = load_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

st.title("Dashboard DEPP — Lecture en 6e")
st.caption("Restitution interactive de la base simulée et des analyses du projet.")

with st.sidebar:
    st.header("Navigation")
    section = st.radio(
        "Choisir une vue",
        [
            "Vue d'ensemble",
            "Qualité des données",
            "Analyse descriptive",
            "Résultats par PCS",
            "Résultats selon le sexe",
            "Retard scolaire",
            "Psychométrie",
            "Modélisation",
            "Analyse longitudinale",
            "Analyse causale",
            "Indicateurs décisionnels",
            "Restitution ministérielle",
        ],
    )
    st.divider()
    selected_pcs = st.multiselect("PCS", sorted(df["pcs"].dropna().unique()), default=sorted(df["pcs"].dropna().unique()))
    selected_academies = st.multiselect(
        "Académies", sorted(df["academie"].dropna().unique()), default=sorted(df["academie"].dropna().unique())
    )

filtered = df[df["pcs"].isin(selected_pcs) & df["academie"].isin(selected_academies)].copy()


def show_kpis(data: pd.DataFrame) -> None:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Élèves", f"{len(data):,}".replace(",", " "))
    k2.metric("Score moyen", f"{data['score_lecture'].mean():.2f}")
    k3.metric("Retard scolaire", f"{data['retard'].mean() * 100:.1f} %")
    k4.metric("Académies", data["academie"].nunique())


if section == "Vue d'ensemble":
    show_kpis(filtered)
    st.subheader("Message clé")
    st.info("Les écarts de score sont associés à la PCS, au retard scolaire et au contexte territorial. Cette base est simulée.")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.histogram(filtered, x="score_lecture", nbins=35, title="Distribution des scores"), width="stretch")
    with col2:
        by_academy = filtered.groupby("academie", as_index=False)["score_lecture"].mean().sort_values("score_lecture", ascending=False)
        st.plotly_chart(px.bar(by_academy, x="academie", y="score_lecture", title="Score moyen par académie"), width="stretch")
    st.download_button("Télécharger les données filtrées", download_csv(filtered), "donnees_filtrees.csv", "text/csv")

elif section == "Qualité des données":
    st.subheader("Contrôle qualité")
    quality = pd.DataFrame(
        {
            "variable": df.columns,
            "valeurs_manquantes": [int(df[column].isna().sum()) for column in df.columns],
            "valeurs_uniques": [int(df[column].nunique()) for column in df.columns],
            "type": [str(df[column].dtype) for column in df.columns],
        }
    )
    show_kpis(filtered)
    st.metric("Doublons exacts", int(df.duplicated().sum()))
    st.dataframe(quality, width="stretch", hide_index=True)
    st.download_button("Télécharger le contrôle qualité", download_csv(quality), "controle_qualite.csv", "text/csv")

elif section == "Analyse descriptive":
    show_kpis(filtered)
    summary = filtered.describe(include="all").transpose().reset_index(names="variable")
    st.dataframe(summary, width="stretch", hide_index=True)
    st.plotly_chart(px.box(filtered, x="sexe", y="score_lecture", color="sexe", title="Scores selon le sexe"), width="stretch")

elif section == "Résultats par PCS":
    result = filtered.groupby("pcs", as_index=False).agg(score_moyen=("score_lecture", "mean"), effectif=("id_eleve", "count"))
    result = result.sort_values("score_moyen", ascending=False)
    st.plotly_chart(px.bar(result, x="pcs", y="score_moyen", text_auto=".2f", title="Score moyen par PCS"), width="stretch")
    st.dataframe(result, width="stretch", hide_index=True)

elif section == "Résultats selon le sexe":
    result = filtered.groupby("sexe", as_index=False).agg(score_moyen=("score_lecture", "mean"), effectif=("id_eleve", "count"))
    st.plotly_chart(px.bar(result, x="sexe", y="score_moyen", text_auto=".2f", title="Score moyen selon le sexe"), width="stretch")
    st.dataframe(result, width="stretch", hide_index=True)

elif section == "Retard scolaire":
    result = filtered.groupby("retard", as_index=False).agg(score_moyen=("score_lecture", "mean"), effectif=("id_eleve", "count"))
    result["statut"] = result["retard"].map({0: "Sans retard", 1: "Avec retard"})
    st.plotly_chart(px.bar(result, x="statut", y="score_moyen", text_auto=".2f", title="Score selon le retard scolaire"), width="stretch")
    st.dataframe(result[["statut", "score_moyen", "effectif"]], width="stretch", hide_index=True)

elif section == "Psychométrie":
    st.subheader("Psychométrie")
    st.info("Le notebook 07 calcule les corrélations entre items. La base élève disponible ne contient pas d'items psychométriques persistés.")
    numeric = filtered.select_dtypes("number")
    st.dataframe(numeric.corr().round(3), width="stretch")

elif section == "Modélisation":
    st.subheader("Régression linéaire")
    st.info("Les coefficients affichés proviennent du pipeline reproductible du notebook 12.")
    model = pd.DataFrame(
        {
            "variable": ["sexe", "retard", "pcs_Cadre", "pcs_Employe", "pcs_Ouvrier", "pcs_Professions_intermediaires", "pcs_Retraite"],
            "coefficient": [-1.5506, -19.5888, 15.3084, -0.7557, -7.4144, 6.1154, -3.7064],
        }
    )
    st.dataframe(model, width="stretch", hide_index=True)

elif section == "Analyse longitudinale":
    longitudinal = pd.DataFrame({"annee": [2022, 2023, 2024, 2025], "score_moyen": [56, 58, 61, 64]})
    st.plotly_chart(px.line(longitudinal, x="annee", y="score_moyen", markers=True, title="Évolution du score moyen"), width="stretch")
    st.dataframe(longitudinal, width="stretch", hide_index=True)

elif section == "Analyse causale":
    st.subheader("Analyse causale")
    st.warning("Le notebook 09 présente une démonstration pédagogique sur données jouet ; elle ne constitue pas une estimation causale sur la base élève.")
    st.markdown("Consulter le notebook **09 — Analyse causale** pour le protocole, le traitement et l'effet moyen illustratif.")

elif section == "Indicateurs décisionnels":
    show_kpis(filtered)
    decision = pd.DataFrame(
        {
            "indicateur": ["Score moyen observé", "Écart PCS max-min", "Écart retard/sans retard"],
            "valeur": [
                filtered["score_lecture"].mean(),
                filtered.groupby("pcs")["score_lecture"].mean().max() - filtered.groupby("pcs")["score_lecture"].mean().min(),
                filtered.loc[filtered["retard"] == 1, "score_lecture"].mean() - filtered.loc[filtered["retard"] == 0, "score_lecture"].mean(),
            ],
        }
    )
    st.dataframe(decision.round(2), width="stretch", hide_index=True)

else:
    st.subheader("Restitution ministérielle")
    st.success("Le contexte socio-économique et le retard scolaire sont les principaux leviers de lecture à surveiller.")
    st.markdown(
        "- cibler l'accompagnement des élèves en retard ;\n"
        "- suivre les écarts entre groupes sociaux et territoires ;\n"
        "- renforcer le suivi longitudinal et l'accès aux ressources numériques."
    )
    st.download_button("Télécharger la synthèse", "Synthèse DEPP\n\n" + st.session_state.get("summary", "Restitution décisionnelle."), "synthese_depp.txt")
