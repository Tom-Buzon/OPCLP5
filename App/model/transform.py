import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import KFold
import category_encoders as ce

def add_custom_features(df):
    df = df.copy()
    df["ratio_appartenance"] = df["annees_dans_l_entreprise"] / df["annee_experience_totale"].replace(0, np.nan)
    df["interet_long_terme"] = df["nombre_participation_pee"] / df["annees_dans_l_entreprise"].replace(0, np.nan)
    df["ratio_poste"] = df["annees_dans_le_poste_actuel"] / df["annees_dans_l_entreprise"].replace(0, np.nan)
    df["valeur_formation"] = df["revenu_mensuel"] / df["niveau_education"].replace(0, np.nan)
    return df.fillna(0)

 
def transform_df_encoder(x, y_target='a_quitte_l_entreprise'):    #### OBSOLETE  => DIRECTEMENT DANS LE PIPE JOBLIB
    df = x.copy()

    # Gestion présence ou non de y
    has_y = y_target in df.columns
    y = df[y_target].map({"Oui": 0, "Non": 1}) if has_y else None
    if has_y:
        df = df.drop(columns=[y_target])

    # Séparer les blocs
    df_num = df.select_dtypes(include='number').copy()
    df_cat = df.select_dtypes(exclude='number').copy()

    # Colonnes par type
    ohe_cols = ['heure_supplementaires', 'genre', 'domaine_etude', 'departement']
    ord_cols = ['augementation_salaire_precedente', 'frequence_deplacement', 'statut_marital']
    ord_num_cols = [
        'satisfaction_employee_environnement',
        'note_evaluation_precedente',
        'satisfaction_employee_nature_travail',
        'satisfaction_employee_equipe',
        'satisfaction_employee_equilibre_pro_perso',
        'niveau_education',
        'nb_formations_suivies'
    ]
    target_cols = ['poste', 'niveau_hierarchique_poste']

    # One-Hot Encoding
    ohe = OneHotEncoder(drop='if_binary', sparse_output=False)
    ohe_encoded = ohe.fit_transform(df_cat[ohe_cols])
    ohe_df = pd.DataFrame(ohe_encoded, columns=ohe.get_feature_names_out(ohe_cols), index=df_cat.index)

    # Ordinal Encoding
    order_salary = [f"{i} %" for i in range(11, 26)]
    df_cat['augementation_salaire_precedente'] = pd.Categorical(
        df_cat['augementation_salaire_precedente'], categories=order_salary, ordered=True)
    df_cat['statut_marital'] = df_cat['statut_marital'].map({'Célibataire': 3, 'Marié(e)': 2, 'Divorcé(e)': 1})
    df_cat['frequence_deplacement'] = df_cat['frequence_deplacement'].map({'Frequent': 3, 'Occasionnel': 2, 'Aucun': 1})
    ord_df = df_cat[ord_cols].copy()
    ord_df['augementation_salaire_precedente'] = df_cat['augementation_salaire_precedente'].cat.codes

    # Target Encoding (avec fallback safe)
    te_df = pd.DataFrame(index=df.index)
    if has_y:
        import category_encoders as ce
        from sklearn.model_selection import KFold
        te = ce.TargetEncoder(cols=target_cols)
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        te_folds = []

        for train_idx, valid_idx in kf.split(df):
            te.fit(df.iloc[train_idx][target_cols], y.iloc[train_idx])
            temp = te.transform(df.iloc[valid_idx][target_cols])
            temp.index = valid_idx
            te_folds.append(temp)

        te_df = pd.concat(te_folds).sort_index().add_suffix('_te')
    else:
        # En prod : charger les encodages appris (optionnel ici, à personnaliser)
        for col in target_cols:
            te_df[col + '_te'] = 0  # valeur par défaut si encodage non dispo

    # Numériques
    df_num_clean = df_num.drop(columns=ord_num_cols).copy()
    bins = [-0.1, 2500, 5000, 14000, np.inf]
    df_num_clean['revenu_mensuel'] = pd.cut(df_num['revenu_mensuel'], bins=bins)
    df_num_clean['revenu_mensuel_log'] = np.log1p(df_num['revenu_mensuel'])
    df_num_clean.drop(['revenu_mensuel'], axis=1, inplace=True)

    for col in ['nombre_experiences_precedentes', 'annee_experience_totale',
                'annees_dans_l_entreprise', 'annees_dans_le_poste_actuel',
                'distance_domicile_travail']:
        df_num_clean[col] = np.log1p(df_num_clean[col])

    df_num_clean.drop(['annee_experience_totale', 'annees_dans_l_entreprise'], axis=1, inplace=True)

    # Join all
    df_all = pd.concat([ohe_df, ord_df, df_num_clean, df[ord_num_cols], te_df], axis=1)

    # Features custom
    df_all['ratio_appartenance'] = df['annees_dans_l_entreprise'] / df['annee_experience_totale'].replace(0, np.nan)
    df_all['interet_long_terme'] = df['nombre_participation_pee'] / df['annees_dans_l_entreprise'].replace(0, np.nan)
    df_all['ratio_poste'] = df['annees_dans_le_poste_actuel'] / df['annees_dans_l_entreprise'].replace(0, np.nan)
    df_all['valeur_formation'] = df['revenu_mensuel'] / df['niveau_education'].replace(0, np.nan)
    df_all['flag_cluster_inertie_2'] = (
        (df_all['revenu_mensuel_log'] > df_all['revenu_mensuel_log'].median()) &
        (df_all.get('heure_supplementaires_Oui', 0) == 0)
    ).astype(int)

    # Clean
    df_all.fillna(0, inplace=True)
    df_all.drop(columns=[
        'niveau_hierarchique_poste_te', 'niveau_hierarchique_poste',
        'departement_Ressources Humaines', 'domaine_etude_Marketing',
        'note_evaluation_actuelle', 'domaine_etude_Autre',
        'domaine_etude_Ressources Humaines', 'annes_sous_responsable_actuel'
    ], errors='ignore', inplace=True)

    return (df_all, y) if has_y else df_all
