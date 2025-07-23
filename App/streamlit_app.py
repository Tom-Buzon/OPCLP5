from sklearn.preprocessing import FunctionTransformer

# ✅ Définir AVANT le joblib.load
class NamedPassthrough(FunctionTransformer):
    def get_feature_names_out(self, input_features=None):
        return input_features

# Ensuite, import et chargement du modèle
import streamlit as st
import pandas as pd
import joblib
from model.transform import transform_df_encoder

# ✅ OK maintenant
model = joblib.load("App/model/model.joblib")




# Formulaire d'entrée utilisateur
st.title("Prédiction de départ d'employé")
st.write("Remplissez les informations pour obtenir une prédiction.")

# Exemple minimal : ajoute les autres champs ensuite
genre = st.selectbox("Genre", ["M", "F"])
poste = st.text_input("Poste")
domaine_etude = st.selectbox("Domaine d'étude", [
    "Entrepreunariat", "Infra & Cloud", "Transformation Digitale", "Autre"
])
departement = st.selectbox("Département", ["Commercial", "Consulting", "R&D"])

# ➕ ajoute ici les autres champs comme heure_supplementaires, age, etc.
age = st.slider("Âge", 18, 65, 35)
revenu_mensuel = st.number_input("Revenu mensuel", min_value=1000, max_value=20000, step=100)

if st.button("Prédire"):
    # Construire un DataFrame avec les colonnes attendues
    input_data = {
        "genre": genre,
        "poste": poste,
        "domaine_etude": domaine_etude,
        "departement": departement,
        "heure_supplementaires": "Non",  # à récupérer depuis l'UI aussi
        "augementation_salaire_precedente": "20 %",
        "frequence_deplacement": "Occasionnel",
        "statut_marital": "Célibataire",
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 4,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "niveau_education": 3,
        "nb_formations_suivies": 2,
        "revenu_mensuel": revenu_mensuel,
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 10,
        "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 3,
        "distance_domicile_travail": 10,
        "annees_depuis_la_derniere_promotion": 2,
        "nombre_participation_pee": 1,
        "niveau_hierarchique_poste": "Intermédiaire",
        "age": age
    }

    df_input = pd.DataFrame([input_data])
    df_transformed = transform_df_encoder(df_input)
    prob = model.predict_proba(df_transformed)[0][1]

    st.success(f"Probabilité de départ : {round(prob * 100, 2)} %")
    if prob >= 0.8:
        st.error("⚠️ Risque élevé de départ (Haut)")
    elif prob >= 0.6:
        st.warning("⚠️ Risque moyen de départ")
    elif prob >= 0.372:
        st.info("Risque faible détecté")
    else:
        st.success("Pas de risque détecté")
