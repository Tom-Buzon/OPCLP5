import streamlit as st
import requests
import pandas as pd

st.title("🧠 Prédiction de départ d'un employé")
st.write("Remplissez les informations ou sélectionnez un employé existant.")

# === 1. Chargement des employés ===
employee = None
predictions = []
selected_id = None

try:
    id_response = requests.get("http://127.0.0.1:8000/employees/ids")
    employee_ids = id_response.json() if id_response.status_code == 200 else []

    employee_options = ["— Aucun —"] + employee_ids
    selected_option = st.selectbox("👤 Sélectionnez un employé", options=employee_options)
    selected_id = selected_option if selected_option != "— Aucun —" else None

    if selected_id:
        emp_response = requests.get(f"http://127.0.0.1:8000/employees/{selected_id}")
        if emp_response.status_code == 200:
            data = emp_response.json()
            employee = data["employee"]
            predictions = data["predictions"]

            st.subheader("📋 Données de l'employé")
            df_employee = pd.DataFrame([employee]).T
            df_employee.columns = ["Valeur"]
            df_employee.index.name = "Champ"
            df_employee = df_employee.astype(str)
            st.dataframe(df_employee)

            st.subheader("📊 Prédictions précédentes")
            if predictions:
                df_pred = pd.DataFrame(predictions)
                df_pred["timestamp"] = pd.to_datetime(df_pred["timestamp"])
                st.dataframe(df_pred)
            else:
                st.info("Aucune prédiction enregistrée pour cet employé.")
        else:
            st.warning("Impossible de charger les informations de l'employé.")
except Exception as e:
    st.error(f"Erreur lors du chargement des employés : {e}")

# === 2. Formulaire ===
def get_value(field, default):
    return employee.get(field, default) if employee else default

poste_options = [
    'Cadre Commercial', 'Assistant de Direction', 'Consultant',
    'Tech Lead', 'Manager', 'Senior Manager',
    'Représentant Commercial', 'Directeur Technique', 'Ressources Humaines'
]

input_data = {
    "heure_supplementaires": st.selectbox("Heures supplémentaires", ["Oui", "Non"],
                                          index=["Oui", "Non"].index(get_value("heure_supplementaires", "Non"))),
    "genre": st.selectbox("Genre", ["M", "F"], index=["M", "F"].index(get_value("genre", "M"))),
    "poste": st.selectbox("Poste", poste_options,
                          index=poste_options.index(get_value("poste", "Cadre Commercial")) if get_value("poste", "Cadre Commercial") in poste_options else 0),
    "niveau_hierarchique_poste": st.slider("Niveau hiérarchique (1-5)", 1, 5, int(get_value("niveau_hierarchique_poste", 3))),
    "domaine_etude": st.selectbox("Domaine d'étude", ["Entrepreunariat", "Infra & Cloud", "Transformation Digitale", "Autre"],
                                  index=["Entrepreunariat", "Infra & Cloud", "Transformation Digitale", "Autre"].index(get_value("domaine_etude", "Autre"))),
    "departement": st.selectbox("Département", ["Commercial", "Consulting", "R&D"],
                                index=["Commercial", "Consulting", "R&D"].index(get_value("departement", "Consulting"))),
    "augementation_salaire_precedente": st.selectbox("Dernière augmentation", [f"{i} %" for i in range(11, 26)],
                                                     index=[f"{i} %" for i in range(11, 26)].index(get_value("augementation_salaire_precedente", "11 %"))),
    "frequence_deplacement": st.selectbox("Fréquence de déplacement", ['Aucun', 'Occasionnel', 'Frequent'],
                                          index=['Aucun', 'Occasionnel', 'Frequent'].index(get_value("frequence_deplacement", "Aucun"))),
    "statut_marital": st.selectbox("Statut marital", ['Divorcé(e)', 'Marié(e)', 'Célibataire'],
                                   index=['Divorcé(e)', 'Marié(e)', 'Célibataire'].index(get_value("statut_marital", 'Célibataire'))),
    "satisfaction_employee_environnement": st.slider("Satisfaction environnement", 1, 5, get_value("satisfaction_employee_environnement", 3)),
    "note_evaluation_precedente": st.slider("Note d'évaluation", 1, 5, get_value("note_evaluation_precedente", 3)),
    "satisfaction_employee_nature_travail": st.slider("Satisfaction nature du travail", 1, 5, get_value("satisfaction_employee_nature_travail", 3)),
    "satisfaction_employee_equipe": st.slider("Satisfaction équipe", 1, 5, get_value("satisfaction_employee_equipe", 3)),
    "satisfaction_employee_equilibre_pro_perso": st.slider("Équilibre pro/perso", 1, 5, get_value("satisfaction_employee_equilibre_pro_perso", 3)),
    "niveau_education": st.slider("Niveau d'éducation", 1, 5, get_value("niveau_education", 3)),
    "nb_formations_suivies": st.slider("Nombre de formations suivies", 0, 10, get_value("nb_formations_suivies", 2)),
    "revenu_mensuel": st.slider("Revenu mensuel", 1000, 20000, get_value("revenu_mensuel", 3000), step=100),
    "nombre_experiences_precedentes": st.slider("Expériences précédentes", 0, 10, get_value("nombre_experiences_precedentes", 2)),
    "annee_experience_totale": st.slider("Expérience totale (années)", 0, 40, get_value("annee_experience_totale", 5)),
    "annees_dans_l_entreprise": st.slider("Années dans l'entreprise", 0, 30, get_value("annees_dans_l_entreprise", 3)),
    "annees_dans_le_poste_actuel": st.slider("Années dans le poste actuel", 0, 30, get_value("annees_dans_le_poste_actuel", 2)),
    "distance_domicile_travail": st.slider("Distance domicile-travail (km)", 0, 100, get_value("distance_domicile_travail", 10)),
    "annees_depuis_la_derniere_promotion": st.slider("Années depuis dernière promotion", 0, 20, get_value("annees_depuis_la_derniere_promotion", 1)),
    "nombre_participation_pee": st.slider("Participation PEE", 0, 10, get_value("nombre_participation_pee", 1)),
    "age": st.slider("Âge", 18, 65, get_value("age", 30))
}

# Ajout de l’ID si existant
if selected_id:
    input_data["employee_id"] = selected_id

# === 3. Bouton de prédiction ===
if st.button("🔮 Prédire"):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        if response.status_code == 200:
            proba = response.json()["probability"]
            st.success(f"✅ Probabilité de départ : {round(proba * 100, 2)} %")

            if proba >= 0.8:
                st.error("⚠️ Risque ÉLEVÉ de départ")
            elif proba >= 0.6:
                st.warning("⚠️ Risque MODÉRÉ")
            elif proba >= 0.372:
                st.info("Risque FAIBLE détecté")
            else:
                st.success("✅ Aucun risque détecté")
        else:
            st.error(f"Erreur {response.status_code} : {response.json().get('detail', 'Erreur inconnue')}")
    except Exception as e:
        st.exception(f"❌ Une erreur est survenue : {e}")
