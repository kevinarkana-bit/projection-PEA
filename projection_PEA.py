import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io

# Données ETF (ton portefeuille réel)
etf_data = {
    "ETF": [
        "AMUNDI PEA MONDE (MSCI World)",
        "AMUNDI PEA US Tech ESG",
        "Amundi CAC 40 UCITS ETF",
        "Amundi MSCI USA Daily (2x)",
        "Amundi PEA Emergent (MSCI EM)",
        "Amundi PEA Nasdaq-100",
        "Amundi PEA SP 500 UCITS ETF",
        "iShares MSCI World Swap"
    ],
    "Valorisation (€)": [4967.08, 695.60, 40.92, 105.04, 228.06, 181.60, 1640.02, 1579.71],
    "Poids (%)": [52.6, 7.4, 0.4, 1.1, 2.4, 1.9, 17.4, 16.7],
    "Rendement (%)": [5.5, 8.0, 4.0, 12.0, 6.0, 9.0, 7.5, 5.0]
}
etf_df = pd.DataFrame(etf_data)

def projeter_pea(montant_initial, versement_mensuel, taux_rendement, annees):
    montant = montant_initial
    evolution = [montant]
    for annee in range(1, annees + 1):
        montant += versement_mensuel * 12
        montant *= (1 + taux_rendement)
        evolution.append(montant)
    return evolution

# Titre et introduction
st.title("📈 Projection PEA Fortunéo (avec TES ETF)")
st.markdown("*" + " ".join([""] * 10))

# Section ETF
st.subheader("📊 Ton portefeuille d'ETF")
col1, col2 = st.columns([1, 2])
with col1:
    st.dataframe(etf_df, hide_index=True)
with col2:
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(etf_df["Poids (%)"], labels=etf_df["ETF"], autopct='%1.1f%%', startangle=90)
    ax_pie.set_title("Répartition de ton PEA")
    st.pyplot(fig_pie)

# Calcul du taux moyen pondéré
taux_moyen = sum(etf_df["Poids (%)"] * etf_df["Rendement (%)"]) / 100
st.info(f"Taux de rendement moyen pondéré : **{taux_moyen:.2f} %** (basé sur tes ETF et leurs rendements historiques)")

# Paramètres de projection
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    montant_initial = st.number_input("Montant initial (€)", min_value=0, value=int(etf_df["Valorisation (€)"].sum()))
with col2:
    versement_mensuel = st.number_input("Versement mensuel (€)", min_value=0, value=200)

# Scénarios
st.subheader("🔮 Scénarios de projection")
taux_optimiste = st.slider("Taux optimiste (%)", 0.0, 15.0, 8.0, 0.1)
taux_realiste = st.slider("Taux réaliste (%)", 0.0, 15.0, taux_moyen, 0.1)
taux_pessimiste = st.slider("Taux pessimiste (%)", 0.0, 15.0, 3.0, 0.1)

# Calcul des projections
annees = list(range(0, 11))
evolution_optimiste = projeter_pea(montant_initial, versement_mensuel, taux_optimiste/100, 10)
evolution_realiste = projeter_pea(montant_initial, versement_mensuel, taux_realiste/100, 10)
evolution_pessimiste = projeter_pea(montant_initial, versement_mensuel, taux_pessimiste/100, 10)

# Résultats
st.subheader("💰 Résultats (brut et net après PFU 30%)")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Optimiste (10 ans)", f"{evolution_optimiste[-1]:.2f} €", f"{evolution_optimiste[-1]*0.7:.2f} € net")
with col_b:
    st.metric("Réaliste (10 ans)", f"{evolution_realiste[-1]:.2f} €", f"{evolution_realiste[-1]*0.7:.2f} € net")
with col_c:
    st.metric("Pessimiste (10 ans)", f"{evolution_pessimiste[-1]:.2f} €", f"{evolution_pessimiste[-1]*0.7:.2f} € net")

# Graphique d'évolution
st.subheader("📈 Évolution du capital")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(annees, evolution_pessimiste, marker='o', color='orange', label=f"Pessimiste ({taux_pessimiste} %)")
ax.plot(annees, evolution_realiste, marker='o', color='green', label=f"Réaliste ({taux_realiste:.2f} %)")
ax.plot(annees, evolution_optimiste, marker='o', color='blue', label=f"Optimiste ({taux_optimiste} %)")
ax.set_xlabel("Années")
ax.set_ylabel("Capital (€)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Export CSV
st.subheader("📥 Exporter les données")
data = {
    "Année": annees,
    "Pessimiste (brut)": evolution_pessimiste,
    "Réaliste (brut)": evolution_realiste,
    "Optimiste (brut)": evolution_optimiste,
}
df_export = pd.DataFrame(data)
csv = df_export.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Télécharger en CSV",
    data=csv,
    file_name='projection_pea_etf_reels.csv',
    mime='text/csv',
)
