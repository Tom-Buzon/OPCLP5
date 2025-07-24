from App.Api.predictor import predict_quit, load_model
from App.Api.schemas import EmployeeInput

#Sdef test_prediction():
#S    model = load_model()
#S    sample_input = EmployeeInput(
#S        heure_supplementaires=\"Oui\",
#S        genre=\"F\",
#S        poste=\"Manager\",
#S        niveau_hierarchique_poste=\"Avancé\",
#S        domaine_etude=\"Entrepreunariat\",
#S        departement=\"R&D\",
#S        augementation_salaire_precedente=\"15 %\",
#S        frequence_deplacement=\"Occasionnel\",
#S        statut_marital=\"Célibataire\",
#S        satisfaction_employee_environnement=3,
#S        note_evaluation_precedente=4,
#S        satisfaction_employee_nature_travail=4,
#S        satisfaction_employee_equipe=3,
#S        satisfaction_employee_equilibre_pro_perso=3,
#S        niveau_education=3,
#S        nb_formations_suivies=2,
#S        revenu_mensuel=3000,
#S        nombre_experiences_precedentes=2,
#S        annee_experience_totale=10,
#S        annees_dans_l_entreprise=5,
#S        annees_dans_le_poste_actuel=3,
#S        distance_domicile_travail=10,
#S        annees_depuis_la_derniere_promotion=2,
#S        nombre_participation_pee=1,
#S        age=35
#S    )
#S
#S    result = predict_quit(sample_input, model)
#S    assert isinstance(result, float)
#S    assert 0.0 <= result <= 1.0