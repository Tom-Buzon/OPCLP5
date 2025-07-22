from pydantic import BaseModel

class InputData(BaseModel):
    genre: str
    poste: str
    domaine_etude: str
    departement: str
    heure_supplementaires: str
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
    revenu_mensuel: float
    nombre_experiences_precedentes: float
    annee_experience_totale: float
    annees_dans_l_entreprise: float
    annees_dans_le_poste_actuel: float
    distance_domicile_travail: float
    annees_depuis_la_derniere_promotion: float
    nombre_participation_pee: float
    niveau_hierarchique_poste: str
    age: int  
