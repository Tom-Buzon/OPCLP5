import pytest
from pydantic import ValidationError
from .schemas import EmployeeInput, PredictionResult

@pytest.fixture
def valid_employee_data():
    return {
        "heure_supplementaires": "5",
        "genre": "Homme",
        "poste": "Ingénieur",
        "niveau_hierarchique_poste": "Senior",
        "domaine_etude": "Informatique",
        "departement": "R&D",
        "augementation_salaire_precedente": "10 %",
        "frequence_deplacement": "Occasionnel",
        "statut_marital": "Marié(e)",
        "satisfaction_employee_environnement": 4,
        "note_evaluation_precedente": 3,
        "satisfaction_employee_nature_travail": 5,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "niveau_education": 3,
        "nb_formations_suivies": 2,
        "revenu_mensuel": 2500,
        "nombre_experiences_precedentes": 1,
        "annee_experience_totale": 6,
        "annees_dans_l_entreprise": 4,
        "annees_dans_le_poste_actuel": 2,
        "distance_domicile_travail": 15,
        "annees_depuis_la_derniere_promotion": 1,
        "nombre_participation_pee": 0,
        "age": 30,
    }


def test_employee_input_valid(valid_employee_data):
    emp = EmployeeInput(**valid_employee_data)
    for key, val in valid_employee_data.items():
        assert getattr(emp, key) == val


def test_employee_input_missing_field(valid_employee_data):
    d = valid_employee_data.copy()
    d.pop("poste")
    with pytest.raises(ValidationError) as exc:
        EmployeeInput(**d)
    assert "poste" in str(exc.value)


def test_employee_input_invalid_type(valid_employee_data):
    d = valid_employee_data.copy()
    d["age"] = "trente"
    with pytest.raises(ValidationError) as exc:
        EmployeeInput(**d)
    msg = str(exc.value)
    assert "age" in msg
    assert "unable to parse string as an integer" in msg

@pytest.fixture
def valid_prediction_data():
    return {"probability": 0.42}


def test_prediction_result_valid(valid_prediction_data):
    pr = PredictionResult(**valid_prediction_data)
    assert isinstance(pr.probability, float)
    assert pr.probability == pytest.approx(0.42)


def test_prediction_result_missing_field():
    with pytest.raises(ValidationError) as exc:
        PredictionResult()
    assert "probability" in str(exc.value)


def test_prediction_result_invalid_type():
    with pytest.raises(ValidationError) as exc:
        PredictionResult(probability="high")
    msg = str(exc.value)
    assert "probability" in msg
    assert "unable to parse string as a number" in msg
