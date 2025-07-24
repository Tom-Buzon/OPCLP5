import pandas as pd
import numpy as np
from App.Api.transformations import add_custom_features, map_ordinals

def test_add_custom_features():
    data = {
        "annees_dans_l_entreprise": [5],
        "annee_experience_totale": [10],
        "nombre_participation_pee": [2],
        "annees_dans_le_poste_actuel": [3],
        "revenu_mensuel": [3000],
        "niveau_education": [3],
    }
    df = pd.DataFrame(data)
    df_out = add_custom_features(df)

    assert "ratio_appartenance" in df_out.columns
    assert "valeur_formation" in df_out.columns
    assert not df_out.isna().any().any()

def test_map_ordinals():
    df = pd.DataFrame({
        "augementation_salaire_precedente": ["12 %"],
        "frequence_deplacement": ["Occasionnel"],
        "statut_marital": ["Marié(e)"]
    })

    df_mapped = map_ordinals(df)

    assert df_mapped["augementation_salaire_precedente"].iloc[0] == 1
    assert df_mapped["frequence_deplacement"].iloc[0] == 1
    assert df_mapped["statut_marital"].iloc[0] == 1
