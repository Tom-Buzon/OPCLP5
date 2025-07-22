import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import KFold
import category_encoders as ce

def transform_df_encoder(x): #, y_target='a_quitte_l_entreprise'):
    df = x.copy()

    #y = df['a_quitte_l_entreprise']

    ##
    ## Séparer les blocs
    ##

    df_num = df.select_dtypes(include='number').copy()
    df_cat = df.select_dtypes(exclude='number').copy()

    ##
    ## Définir variables par type
    ##

    # Nominales ➜ OneHotEncoder
    ohe_cols = ['heure_supplementaires', 'genre', 'domaine_etude', 'departement']  

    # Ordinales ➜ OrdinalEncoder
    ord_cols = [
        'augementation_salaire_precedente',
        'frequence_deplacement',
        'statut_marital'
    ]

    ord_num_cols = [
        'satisfaction_employee_environnement',
        'note_evaluation_precedente',
        'satisfaction_employee_nature_travail',
        'satisfaction_employee_equipe',
        'satisfaction_employee_equilibre_pro_perso',
        #'nombre_participation_pee',
        'niveau_education',
        'nb_formations_suivies'
    ]



    

    # TargetEncoder ➜ poste par exemple
    target_cols = ['poste', 'niveau_hierarchique_poste' ]

    ##
    ## Encodage One-Hot
    ##

    ohe = OneHotEncoder(drop='if_binary', sparse_output=False)
    ohe_encoded = ohe.fit_transform(df_cat[ohe_cols])
    ohe_df = pd.DataFrame(ohe_encoded,
                          columns=ohe.get_feature_names_out(ohe_cols),
                          index=df_cat.index)

    ##
    ## Encodage Ordinal   = pour les ord col num il n'y a pas de modif mais pour celles ci il faut les remettre danbs l'ordre logique avant d'encoder
    ##

    # Pour augementation_salaire_precedente : fixer ordre
    order_salary = [
        '11 %', '12 %', '13 %', '14 %', '15 %', '16 %',
        '17 %', '18 %', '19 %', '20 %', '21 %', '22 %',
        '23 %', '24 %', '25 %'
    ]
    df_cat['augementation_salaire_precedente'] = pd.Categorical(
        df_cat['augementation_salaire_precedente'],
        categories=order_salary,
        ordered=True
    )

    # Mapper manuel pour statut_marital
    map_sm = {
        'Célibataire': 3,
        'Marié(e)': 2,
        'Divorcé(e)': 1
    }
    df_cat['statut_marital'] = df_cat['statut_marital'].map(map_sm)

    # Mapper manuel pour frequence_deplacement
    map_freq = {
        'Frequent': 3,
        'Occasionnel': 2,
        'Aucun': 1
    }
    df_cat['frequence_deplacement'] = df_cat['frequence_deplacement'].map(map_freq)

    ord_df = df_cat[ord_cols].copy()
    ord_df['augementation_salaire_precedente'] = df_cat['augementation_salaire_precedente'].cat.codes

    ##
    ## TargetEncoder K-Fold
    ##

    y = df[y_target]
    te = ce.TargetEncoder(cols=target_cols)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Collecte tous les folds dans une liste
    te_folds = []

    for train_idx, valid_idx in kf.split(df):
        te.fit(df.iloc[train_idx][target_cols], y.iloc[train_idx])
        te_transformed = te.transform(df.iloc[valid_idx][target_cols])
        te_transformed.index = valid_idx  # Garder l'index correct
        te_folds.append(te_transformed)

    # Recolle tous les morceaux encodés
    te_df = pd.concat(te_folds).sort_index().add_suffix('_te')

    ##
    ## Continues ➜ transformation log, binning, etc.
    ##

    df_num_clean = df_num.copy()
    df_num_clean = df_num.drop(columns=ord_num_cols).copy()
    

    bins = [-0.1, 2500, 5000, 14000, np.inf]
    df_num_clean['revenu_mensuel'] = pd.cut(df_num['revenu_mensuel'], bins=bins)
    df_num_clean['revenu_mensuel_log'] = np.log1p(df_num['revenu_mensuel'])
    df_num_clean.drop(['revenu_mensuel'], axis=1, inplace=True)

    df_num_clean['nombre_experiences_precedentes'] = np.log1p(df_num_clean['nombre_experiences_precedentes'])
    df_num_clean['annee_experience_totale'] = np.log1p(df_num_clean['annee_experience_totale'])
    df_num_clean['annees_dans_l_entreprise'] = np.log1p(df_num_clean['annees_dans_l_entreprise'])
    df_num_clean['annees_dans_le_poste_actuel'] = np.log1p(df_num_clean['annees_dans_le_poste_actuel'])
    df_num_clean['distance_domicile_travail'] = np.log1p(df_num_clean['distance_domicile_travail'])

    # Retirer colonnes corrélées si besoin
    df_num_clean.drop(['annee_experience_totale', 'annees_dans_l_entreprise'], axis=1, inplace=True)

    ##
    ## Joindre blocs
    ##

    df_all = pd.concat([ohe_df, ord_df, df_num_clean, df[ord_num_cols], te_df], axis=1)

    ##
    ## Feature Engineering custom
    ##

    df_all['ratio_appartenance'] = df['annees_dans_l_entreprise'] / df['annee_experience_totale']
    df_all['interet_long_terme'] = df['nombre_participation_pee'] / df['annees_dans_l_entreprise'].replace(0, np.nan)
    df_all['ratio_poste'] = df['annees_dans_le_poste_actuel'] / df['annees_dans_l_entreprise'].replace(0, np.nan)
    df_all['valeur_formation'] = df['revenu_mensuel'] / df['niveau_education'].replace(0, np.nan)

    df_all['flag_cluster_inertie_2'] = (
        (df_all['revenu_mensuel_log'] > df_all['revenu_mensuel_log'].median()) &
        (df_all['heure_supplementaires_Oui'] == 0)
    ).astype(int)

    df_all.fillna(0, inplace=True)


    df_all.drop(['niveau_hierarchique_poste_te', 'niveau_hierarchique_poste'], axis=1, inplace=True) #bad pearson
    df_all.drop(['departement_Ressources Humaines', 'domaine_etude_Marketing', 'note_evaluation_actuelle', 'domaine_etude_Autre', 'domaine_etude_Ressources Humaines'], axis=1, inplace=True) #bad feature global
    df_all.drop(['annes_sous_responsable_actuel'], axis=1, inplace=True) #bad : analyse finale : produit plus de FN que tout le reste
    
    

    return df_all#, y