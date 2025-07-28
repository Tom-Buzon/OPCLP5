#from App.API.predictor import predict_quit, load_model
#from App.API.schemas import EmployeeInput

import os
import joblib
import pandas as pd
import numpy as np
import importlib.machinery
import importlib.util
import pytest
from types import SimpleNamespace

# Charger dynamiquement predictor.js (contenant du code Python)
HERE = os.path.dirname(__file__)
loader = importlib.machinery.SourceFileLoader(
    'predictor', os.path.join(HERE, 'predictor.py')
)
spec = importlib.util.spec_from_loader(loader.name, loader)
predictor = importlib.util.module_from_spec(spec)
loader.exec_module(predictor)

def test_map_ordinals():
    df = pd.DataFrame({
        "augementation_salaire_precedente": ["11 %", "15 %", "25 %"],
        "frequence_deplacement": ['Aucun', 'Frequent', 'Occasionnel'],
        "statut_marital": ['Marié(e)', 'Célibataire', 'Divorcé(e)']
    })
    out = predictor.map_ordinals(df)
    # vérifie que les codes sont dans les bons intervalles
    assert set(out["augementation_salaire_precedente"].unique()) <= set(range(0, 15))
    assert set(out["frequence_deplacement"].unique()) == {0, 1, 2}
    assert set(out["statut_marital"].unique()) == {0, 1, 2}


def test_add_custom_features():
    df = pd.DataFrame([{
        "annees_dans_l_entreprise": 5,
        "annee_experience_totale": 10,
        "nombre_participation_pee": 2,
        "annees_dans_le_poste_actuel": 3,
        "revenu_mensuel": 2000,
        "niveau_education": 2
    }])
    out = predictor.add_custom_features(df)
    # vérifie les ratios attendus
    assert np.isclose(out.loc[0, "ratio_appartenance"], 5/10)
    assert np.isclose(out.loc[0, "interet_long_terme"], 2/5)
    assert np.isclose(out.loc[0, "ratio_poste"], 3/5)
    assert np.isclose(out.loc[0, "valeur_formation"], 2000/2)


def test_TargetEncoderWrapper_fit_transform():
    # jeu de données toy
    X = pd.DataFrame({"col": ["a", "b", "a", "c"]})
    y = pd.Series([1, 2, 3, 4], name="target")
    te = predictor.TargetEncoderWrapper(cols=["col"])
    Xt = te.fit_transform(X, y)
    # Vérifie qu'on a créé "col_te" et supprimé "col"
    assert "col_te" in Xt.columns and "col" not in Xt.columns
    # moyenne par groupe : a -> (1+3)/2 = 2, b -> 2, c -> 4
    expected = {"a": 2.0, "b": 2.0, "c": 4.0}
    # reconstruction du mapping interne
    assert te.encoding_maps["col"] == expected
    # et valeurs codées conformes
    assert list(Xt["col_te"]) == [2.0, 2.0, 2.0, 4.0]


def test_NamedPassthrough_get_feature_names_out():
    nt = predictor.NamedPassthrough()
    inp = ["f1", "f2", "f3"]
    assert nt.get_feature_names_out(inp) == inp


def test_load_model_and_te_encoder(monkeypatch, tmp_path):
    # on remplace download_from_url pour ne pas télécharger
    calls = []
    def fake_download(url, path):
        calls.append((url, path))
        # crée un fichier vide
        open(path, "wb").close()
    monkeypatch.setattr(predictor, "download_from_url", fake_download)
    # et joblib.load pour renvoyer un objet sentinel
    sentinel_model = object()
    monkeypatch.setattr(joblib, "load", lambda p: sentinel_model)
    m = predictor.load_model()
    assert m is sentinel_model
    assert calls and calls[-1][0].endswith("model.joblib")
    calls.clear()
    sentinel_te = object()
    monkeypatch.setattr(joblib, "load", lambda p: sentinel_te)
    te = predictor.load_te_encoder()
    assert te is sentinel_te
    assert calls and "te_encoder.joblib" in calls[-1][1]


def test_apply_frozen_target_encoding(monkeypatch):
    # stub de l'encodeur
    class DummyTE:
        def transform(self, X):
            return X.assign(dummy=1)
    monkeypatch.setattr(predictor, "load_te_encoder", lambda: DummyTE())
    df = pd.DataFrame({"a":[1,2]})
    out = predictor.apply_frozen_target_encoding(df)
    assert "dummy" in out.columns and all(out["dummy"] == 1)


def test_predict_quit(monkeypatch):
    # stub modèle avec predict_proba
    class DummyModel:
        def predict_proba(self, df):
            # retourne [[0.7, 0.3]]
            return np.array([[0.7, 0.3]])
    dummy = SimpleNamespace(dict=lambda: {
        "annees_dans_l_entreprise":5,
        "annee_experience_totale":10,
        "nombre_participation_pee":2,
        "annees_dans_le_poste_actuel":3,
        "revenu_mensuel":2000,
        "niveau_education":2,
        "augementation_salaire_precedente":"11 %",
        "frequence_deplacement":"Aucun",
        "statut_marital":"Divorcé(e)"
    })
    prob = predictor.predict_quit(dummy, DummyModel())
    assert pytest.approx(prob, rel=1e-3) == 0.7