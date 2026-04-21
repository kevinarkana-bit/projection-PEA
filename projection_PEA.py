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
st.subheader("📊 Ton portefeuille d
