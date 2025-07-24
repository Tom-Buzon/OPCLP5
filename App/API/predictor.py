import pandas as pd
import joblib
import numpy as np

from sklearn.preprocessing import FunctionTransformer




# === Nécessaire pour joblib
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

def load_model():
    return joblib.load("App/model/model.joblib")

def predict_quit(input_data, model):
    df_input = pd.DataFrame([input_data.dict()])
    df_input = add_custom_features(df_input)
    proba = model.predict_proba(df_input)[0][0]
    return proba


import __main__
__main__.map_ordinals = map_ordinals
__main__.add_custom_features = add_custom_features
__main__.TargetEncoderWrapper = TargetEncoderWrapper
__main__.NamedPassthrough = NamedPassthrough
__main__.apply_frozen_target_encoding = apply_frozen_target_encoding 