import joblib
import pandas as pd
from App.model.transform import transform_df_encoder

# Charger le modèle une seule fois (optimisé)
model = joblib.load("App/model/model.joblib")

def predict_with_model(input_data: dict):
    """
    Fonction de prédiction appelée depuis FastAPI.
    - input_data : dictionnaire avec les features attendues par transform_df_encoder
    - retourne : prédiction de probabilité
    """

    # Conversion de l'entrée (Pydantic → dict) en DataFrame
    df_input = pd.DataFrame([input_data])

    # Appliquer la transformation custom (sans y)
    df_transformed = transform_df_encoder(df_input)

    # Faire une prédiction (probabilité de classe 1)
    y_proba = model.predict_proba(df_transformed)[0][1]

    # Retourner la proba + seuils en bande optionnelle
    return {
        "proba_quitte": round(y_proba, 4),
        "classe": "Haut" if y_proba >= 0.8 else
                  "Moyen" if y_proba >= 0.6 else
                  "Bas" if y_proba >= 0.372 else
                  "Non détecté"
    }
