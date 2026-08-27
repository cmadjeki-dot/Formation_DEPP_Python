import streamlit as st

from src.data.loader import data_path, load_csv

st.set_page_config(page_title="DEPP Dashboard", page_icon="📊")
st.title("Dashboard DEPP — Lecture 6e")

try:
    df = load_csv(data_path('data', 'interim', 'etude_lecture_6e_clean.csv'))
    st.success("Base chargée avec succès.")
    st.subheader("Aperçu des données")
    st.dataframe(df.head())

    st.subheader("Score moyen par PCS")
    by_pcs = df.groupby('pcs')['score_lecture'].mean().sort_values(ascending=False)
    st.bar_chart(by_pcs)
except FileNotFoundError:
    st.warning("La base nettoyée n'est pas encore disponible. Génère la base dans le notebook 01 puis le notebook 04.")
