from sklearn.preprocessing import FunctionTransformer
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# === Pour que joblib décode NamedPassthrough
class NamedPassthrough(FunctionTransformer):
    def get_feature_names_out(self, input_features=None):
        return input_features

class TargetEncoderWrapper:
    def __init__(self, cols, encoding_maps=None):
        self.cols = cols
        self.encoding_maps = encoding_maps or {}

    def fit(self, X, y):
        df = X.copy()
        df[y.name] = y
        self.encoding_maps = {
            col: df.groupby(col)[y.name].mean().to_dict() for col in self.cols
        }
        return self

    def transform(self, X):
        X_copy = X.copy()
        for col in self.cols:
            X_copy[col + "_te"] = X_copy[col].map(self.encoding_maps[col]).fillna(0)
            X_copy.drop(columns=[col], inplace=True)
        return X_copy

    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X)

def map_ordinals(X):
    ordinal_map = {
        "augementation_salaire_precedente": [f"{i} %" for i in range(11, 26)],
        "frequence_deplacement": ['Aucun', 'Occasionnel', 'Frequent'],
        "statut_marital": ['Divorcé(e)', 'Marié(e)', 'Célibataire']
    }
    X_copy = X.copy()
    for col, categories in ordinal_map.items():
        X_copy[col] = pd.Categorical(X_copy[col], categories=categories, ordered=True).codes
    return X_copy

def add_custom_features(df):
    df = df.copy()
    df["ratio_appartenance"] = df["annees_dans_l_entreprise"] / df["annee_experience_totale"].replace(0, np.nan)
    df["interet_long_terme"] = df["nombre_participation_pee"] / df["annees_dans_l_entreprise"].replace(0, np.nan)
    df["ratio_poste"] = df["annees_dans_le_poste_actuel"] / df["annees_dans_l_entreprise"].replace(0, np.nan)
    df["valeur_formation"] = df["revenu_mensuel"] / df["niveau_education"].replace(0, np.nan)
    return df.fillna(0)

def apply_frozen_target_encoding(X):
    te = joblib.load("App/model/te_encoder.joblib")
    return te.transform(X) 

# === Chargement du modèle complet pipeline + classifier
model = joblib.load("App/model/model.joblib")

# === UI
st.title("🧠 Prédiction de départ d'un employé")
st.write("Veuillez remplir les informations ci-dessous pour obtenir une prédiction.")

# === Champs utilisateur
input_data = {
    "heure_supplementaires": st.selectbox("Heures supplémentaires", ["Oui", "Non"]),
    "genre": st.selectbox("Genre", ["M", "F"]),
    "poste": st.selectbox("Poste", [
        'Cadre Commercial', 'Assistant de Direction', 'Consultant',
        'Tech Lead', 'Manager', 'Senior Manager',
        'Représentant Commercial', 'Directeur Technique', 'Ressources Humaines'
    ]),
    "niveau_hierarchique_poste": st.selectbox("Niveau hiérarchique", ["Débutant", "Intermédiaire", "Avancé"]),
    "domaine_etude": st.selectbox("Domaine d'étude", ["Entrepreunariat", "Infra & Cloud", "Transformation Digitale", "Autre"]),
    "departement": st.selectbox("Département", ["Commercial", "Consulting", "R&D"]),
    "augementation_salaire_precedente": st.selectbox("Dernière augmentation", [f"{i} %" for i in range(11, 26)]),
    "frequence_deplacement": st.selectbox("Fréquence de déplacement", ['Aucun', 'Occasionnel', 'Frequent']),
    "statut_marital": st.selectbox("Statut marital", ['Divorcé(e)', 'Marié(e)', 'Célibataire']),
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

# === Prédiction
if st.button("Prédire"):
    df_input = pd.DataFrame([input_data])
    df_input = add_custom_features(df_input)

    try:
        proba_quit = model.predict_proba(df_input)[0][0]

        st.success(f"Probabilité de départ : {round(proba_quit * 100, 2)} %")

        if proba_quit >= 0.8:
            st.error("⚠️ Risque ÉLEVÉ de départ")
        elif proba_quit >= 0.6:
            st.warning("⚠️ Risque MODÉRÉ")
        elif proba_quit >= 0.372:
            st.info("Risque FAIBLE détecté")
        else:
            st.success("✅ Aucun risque détecté")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction : {e}")
