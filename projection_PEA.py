import streamlit as st
import matplotlib.pyplot as plt

def projeter_pea(montant_initial, versement_mensuel, taux_rendement, annees):
    """
    Projette l'évolution d'un PEA sur une période donnée.
    """
    montant = montant_initial
    evolution = [montant]

    for annee in range(1, annees + 1):
        montant += versement_mensuel * 12
        montant *= (1 + taux_rendement)
        evolution.append(montant)

    return evolution

# Titre de l'application
st.title("Projection de ton PEA Fortunéo 📈")

# Paramètres utilisateur
montant_initial = st.number_input("Montant initial (€)", min_value=0, value=10000)
versement_mensuel = st.number_input("Versement mensuel (€)", min_value=0, value=200)
taux_rendement = st.number_input("Taux de rendement annuel (%)", min_value=0.0, value=5.0) / 100.0

# Calcul des projections
projection_1an = projeter_pea(montant_initial, versement_mensuel, taux_rendement, 1)
projection_5ans = projeter_pea(montant_initial, versement_mensuel, taux_rendement, 5)
projection_10ans = projeter_pea(montant_initial, versement_mensuel, taux_rendement, 10)

# Affichage des résultats
st.subheader("Résultats")
st.write(f"- **Dans 1 an** : {projection_1an[-1]:.2f} €")
st.write(f"- **Dans 5 ans** : {projection_5ans[-1]:.2f} €")
st.write(f"- **Dans 10 ans** : {projection_10ans[-1]:.2f} €")

# Graphique de l'évolution
st.subheader("Évolution du capital")
annees = list(range(0, 11))
evolution_10ans = projeter_pea(montant_initial, versement_mensuel, taux_rendement, 10)
fig, ax = plt.subplots()
ax.plot(annees, evolution_10ans, marker='o')
ax.set_xlabel("Années")
ax.set_ylabel("Capital (€)")
ax.set_title("Projection sur 10 ans")
st.pyplot(fig)
