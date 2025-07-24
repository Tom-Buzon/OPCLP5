from pydantic import BaseModel

class EmployeeInput(BaseModel):
    heure_supplementaires: str
    genre: str
    poste: str
    niveau_hierarchique_poste: str
    domaine_etude: str
    departement: str
    augementation_salaire_precedente: str
    frequence_deplacement: str
    statut_marital: str
    satisfaction_employee_environnement: int
    note_evaluation_precedente: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    niveau_education: int
    nb_formations_suivies: int
    revenu_mensuel: int
    nombre_experiences_precedentes: int
    annee_experience_totale: int
    annees_dans_l_entreprise: int
    annees_dans_le_poste_actuel: int
    distance_domicile_travail: int
    annees_depuis_la_derniere_promotion: int
    nombre_participation_pee: int
    age: int

class PredictionResult(BaseModel):
    probability: float
