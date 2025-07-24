import streamlit as st
import requests
import pandas as pd

st.title("🧠 Prédiction de départ d'un employé")
st.write("Veuillez remplir les informations ci-dessous pour obtenir une prédiction.")

# === Champs pré-remplis ===
input_data = {
    "heure_supplementaires": st.selectbox("Heures supplémentaires", ["Oui", "Non"], index=1),
    "genre": st.selectbox("Genre", ["M", "F"], index=0),
    "poste": st.selectbox("Poste", [
        'Cadre Commercial', 'Assistant de Direction', 'Consultant',
        'Tech Lead', 'Manager', 'Senior Manager',
        'Représentant Commercial', 'Directeur Technique', 'Ressources Humaines'
    ], index=0),
    "niveau_hierarchique_poste": st.selectbox("Niveau hiérarchique", ["Débutant", "Intermédiaire", "Avancé"], index=1),
    "domaine_etude": st.selectbox("Domaine d'étude", ["Entrepreunariat", "Infra & Cloud", "Transformation Digitale", "Autre"], index=2),
    "departement": st.selectbox("Département", ["Commercial", "Consulting", "R&D"], index=1),
    "augementation_salaire_precedente": st.selectbox("Dernière augmentation", [f"{i} %" for i in range(11, 26)], index=0),
    "frequence_deplacement": st.selectbox("Fréquence de déplacement", ['Aucun', 'Occasionnel', 'Frequent'], index=0),
    "statut_marital": st.selectbox("Statut marital", ['Divorcé(e)', 'Marié(e)', 'Célibataire'], index=2),
    "satisfaction_employee_environnement": st.slider("Satisfaction environnement", 1, 5, 3),
    "note_evaluation_precedente": st.slider("Note d'évaluation", 1, 5, 4),
    "satisfaction_employee_nature_travail": st.slider("Satisfaction nature du travail", 1, 5, 4),
    "satisfaction_employee_equipe": st.slider("Satisfaction équipe", 1, 5, 3),
    "satisfaction_employee_equilibre_pro_perso": st.slider("Équilibre pro/perso", 1, 5, 3),
    "niveau_education": st.slider("Niveau d'éducation", 1, 5, 3),
    "nb_formations_suivies": st.slider("Nombre de formations suivies", 0, 10, 2),
    "revenu_mensuel": st.slider("Revenu mensuel", 1000, 20000, 3000, step=100),
    "nombre_experiences_precedentes": st.slider("Expériences précédentes", 0, 10, 2),
    "annee_experience_totale": st.slider("Expérience totale (années)", 0, 40, 10),
    "annees_dans_l_entreprise": st.slider("Années dans l'entreprise", 0, 30, 5),
    "annees_dans_le_poste_actuel": st.slider("Années dans le poste actuel", 0, 30, 3),
    "distance_domicile_travail": st.slider("Distance domicile-travail (km)", 0, 100, 10),
    "annees_depuis_la_derniere_promotion": st.slider("Années depuis dernière promotion", 0, 20, 2),
    "nombre_participation_pee": st.slider("Participation PEE", 0, 10, 1),
    "age": st.slider("Âge", 18, 65, 35)
}

if st.button("Prédire"):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        if response.status_code == 200:
            proba = response.json()["probability"]
            st.success(f"Probabilité de départ : {round(proba * 100, 2)} %")

            if proba >= 0.8:
                st.error("⚠️ Risque ÉLEVÉ de départ")
            elif proba >= 0.6:
                st.warning("⚠️ Risque MODÉRÉ")
            elif proba >= 0.372:
                st.info("Risque FAIBLE détecté")
            else:
                st.success("✅ Aucun risque détecté")
        else:
            st.error(f"Erreur {response.status_code} : {response.json()['detail']}")
    except Exception as e:
        st.exception(f"Une erreur est survenue : {e}")
