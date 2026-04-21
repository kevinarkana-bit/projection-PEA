import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
    "Rendement (%)": [5.5, 8.0, 4.0, 12.0, 6.0, 9.0, 7.5, 5.0]  # Rendements annuels (dividendes réinvestis inclus)
}
etf_df = pd.DataFrame(etf_data)

def projeter_pea(montant_initial, versement_mensuel, taux_rendement, annees_max):
    """
    Projette l'évolution du PEA en réinvestissant automatiquement les gains (dividendes inclus).
    """
    montant = montant_initial
    evolution = [montant]
    plus_values_annuelles = [0]  # Plus-value la première année = 0
    versements_cumules = [0]     # Versements cumulés

    for annee in range(1, annees_max + 1):
        # Ajout des versements mensuels (12 mois)
        versement_annuel = versement_mensuel * 12
        versements_cumules.append(versements_cumules[-1] + versement_annuel)
        # Calcul de la plus-value annuelle (inclut les dividendes réinvestis)
        plus_value = (montant + versement_annuel) * taux_rendement
        plus_values_annuelles.append(plus_value)
        # Mise à jour du montant total (capital + versements + dividendes réinvestis)
        montant = (montant + versement_annuel) * (1 + taux_rendement)
        evolution.append(montant)

    return evolution, plus_values_annuelles, versements_cumules

# Titre et sélecteur d'âge du PEA
st.title("📈 Projection PEA Fortunéo (20 ans + Dividendes Réinvestis)")
st.markdown("""
*Tous tes ETF sont **capitalisants** : les dividendes sont automatiquement réinvestis et inclus dans les rendements annuels affichés.*
""")

age_pea = st.radio(
    "🕒 Âge de ton PEA :",
    ["Plus de 5 ans (17,2 % prélèvements sociaux)", "Moins de 5 ans (PFU 30 %)"],
    help="Sélectionne l'âge de ton PEA pour ajuster la fiscalité."
)
prelevements_sociaux = 0.172 if "5 ans" in age_pea else 0.30

# Section ETF
st.subheader("📊 Ton portefeuille d'ETF (capitalisants)")
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
st.info(f"""
**Taux de rendement moyen pondéré : {taux_moyen:.2f} %**
*(Ce taux inclut déjà le réinvestissement des dividendes, car tes ETF sont capitalisants.)*
""")

# Paramètres de projection
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    montant_initial = st.number_input("Montant initial (€)", min_value=0, value=int(etf_df["Valorisation (€)"].sum()))
with col2:
    versement_mensuel = st.number_input("Versement mensuel (€)", min_value=0, value=200)

# Durée de projection
annees_max = st.slider("📅 Durée de projection (années)", 1, 30, 20, help="Jusqu'à 30 ans pour voir l'effet des intérêts composés.")

# Scénarios
st.subheader("🔮 Scénarios de projection")
taux_optimiste = st.slider("Taux optimiste (%)", 0.0, 15.0, 8.0, 0.1, help="Rendement annuel (dividendes réinvestis inclus).")
taux_realiste = st.slider("Taux réaliste (%)", 0.0, 15.0, taux_moyen, 0.1, help="Basé sur ton portefeuille actuel.")
taux_pessimiste = st.slider("Taux pessimiste (%)", 0.0, 15.0, 3.0, 0.1)

# Calcul des projections
evolution_optimiste, pv_optimiste, versements_optimiste = projeter_pea(montant_initial, versement_mensuel, taux_optimiste/100, annees_max)
evolution_realiste, pv_realiste, versements_realiste = projeter_pea(montant_initial, versement_mensuel, taux_realiste/100, annees_max)
evolution_pessimiste, pv_pessimiste, versements_pessimiste = projeter_pea(montant_initial, versement_mensuel, taux_pessimiste/100, annees_max)

# Résultats finaux
st.subheader(f"💰 Résultats après {annees_max} ans (brut et net)")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Optimiste", f"{evolution_optimiste[-1]:.2f} €", f"{evolution_optimiste[-1]*(1-prelevements_sociaux):.2f} € net")
with col_b:
    st.metric("Réaliste", f"{evolution_realiste[-1]:.2f} €", f"{evolution_realiste[-1]*(1-prelevements_sociaux):.2f} € net")
with col_c:
    st.metric("Pessimiste", f"{evolution_pessimiste[-1]:.2f} €", f"{evolution_pessimiste[-1]*(1-prelevements_sociaux):.2f} € net")

# Note fiscale et dividendes
st.caption(f"""
⚠️ Fiscalité appliquée : {age_pea}.
💡 **Dividendes** : Tous tes ETF sont capitalisants → les dividendes sont réinvestis automatiquement et **inclus dans les rendements annuels**.
""")

# Graphique 1 : Évolution du capital (brut)
st.subheader("📈 Évolution du capital (brut)")
annees = list(range(0, annees_max + 1))
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(annees, evolution_pessimiste, marker='o', color='orange', label=f"Pessimiste ({taux_pessimiste} %)")
ax1.plot(annees, evolution_realiste, marker='o', color='green', label=f"Réaliste ({taux_realiste:.2f} %)")
ax1.plot(annees, evolution_optimiste, marker='o', color='blue', label=f"Optimiste ({taux_optimiste} %)")
ax1.set_xlabel("Années")
ax1.set_ylabel("Capital (€)")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# Graphique 2 : Effet des intérêts composés (scénario réaliste)
st.subheader("🧮 Effet des intérêts composés (Réaliste)")
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(annees, versements_realiste, label="Versements cumulés", color='lightblue')
ax2.plot(annees, [e - v for e, v in zip(evolution_realiste, versements_realiste)], label="Plus-values + dividendes réinvestis", color='lightgreen')
ax2.set_xlabel("Années")
ax2.set_ylabel("Capital (€)")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# Graphique 3 : Plus-values annuelles (réaliste)
st.subheader("📊 Plus-values annuelles (Réaliste)")
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(range(1, annees_max + 1), pv_realiste[1:], color='green', alpha=0.7)
ax3.set_xlabel("Années")
ax3.set_ylabel("Plus-value annuelle (€)")
ax3.grid(True)
st.pyplot(fig3)

# Tableau récapitulatif annuel (scénario réaliste)
st.subheader("📝 Détail annuel (scénario réaliste)")
detail_annuel = pd.DataFrame({
    "Année": annees,
    "Capital (€)": [f"{x:.2f}" for x in evolution_realiste],
    "Plus-value annuelle (€)": [f"{x:.2f}" for x in pv_realiste],
    "Plus-value cumulée (€)": [f"{sum(pv_realiste[:i+1]):.2f}" for i in range(len(pv_realiste))],
    "Versements cumulés (€)": [f"{x:.2f}" for x in versements_realiste],
    "Part des dividendes réinvestis": [f"{((e - v) / e * 100 if e > 0 else 0):.1f}%" for e, v in zip(evolution_realiste, versements_realiste)]
})
st.dataframe(detail_annuel)

# Export CSV
st.subheader("📥 Exporter les données")
data_export = {
    "Année": annees,
    "Optimiste (brut)": evolution_optimiste,
    "Réaliste (brut)": evolution_realiste,
    "Pessimiste (brut)": evolution_pessimiste,
    "Optimiste (net)": [x*(1-prelevements_sociaux) for x in evolution_optimiste],
    "Réaliste (net)": [x*(1-prelevements_sociaux) for x in evolution_realiste],
    "Pessimiste (net)": [x*(1-prelevements_sociaux) for x in evolution_pessimiste],
    "Plus-value annuelle (réaliste)": pv_realiste,
    "Plus-value cumulée (réaliste)": np.cumsum(pv_realiste),
    "Versements cumulés (réaliste)": versements_realiste
}
df_export = pd.DataFrame(data_export)
csv = df_export.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Télécharger en CSV",
    data=csv,
    file_name=f'projection_pea_{annees_max}ans_dividendes.csv',
    mime='text/csv',
)

# Explication sur les dividendes
st.markdown("""
---
### 💡 Pourquoi les dividendes sont-ils déjà inclus ?
Tous tes ETF sont **capitalisants** :
- Les dividendes sont **automatiquement réinvestis** dans l’ETF.
- Ils **augmentent la valeur liquidative** de l’ETF (et donc ton capital).
- **Résultat** : Le rendement annuel affiché (ex. 5,5 % pour le MSCI World) **inclut déjà cet effet**.
- **Avantage** : Pas besoin de calcul supplémentaire → tout est pris en compte dans les projections !

*Exemple : Si un ETF a un rendement de 5 %/an, cela inclut à la fois la plus-value et les dividendes réinvestis.*
""")
