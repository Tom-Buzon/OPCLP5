import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from .db import init_db, engine, Base, SessionLocal
from .models import Employee, Prediction

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """
    Initialise la base avant les tests ou skip si DB inaccessible
    """
    try:
        Base.metadata.drop_all(bind=engine)
        init_db()
    except OperationalError:
        pytest.skip("PostgreSQL server inaccessible - skipping DB tests", allow_module_level=True)
    yield
    Base.metadata.drop_all(bind=engine)


def test_tables_created():
    """Vérifie que les tables existent bien"""
    insp = inspect(engine)
    tables = insp.get_table_names()
    assert "employees" in tables
    assert "predictions" in tables


def test_session_and_crud():
    """Test CRUD basique via SQLAlchemy session"""
    session = SessionLocal()
    # Création d'un employee
    emp = Employee(
        heure_supplementaires="0",
        genre="Test",
        poste="Test",
        niveau_hierarchique_poste="Test",
        domaine_etude="Test",
        departement="Test",
        augementation_salaire_precedente="0 %",
        frequence_deplacement="Aucun",
        statut_marital="Célibataire",
        satisfaction_employee_environnement=1,
        note_evaluation_precedente=1,
        satisfaction_employee_nature_travail=1,
        satisfaction_employee_equipe=1,
        satisfaction_employee_equilibre_pro_perso=1,
        niveau_education=1,
        nb_formations_suivies=0,
        revenu_mensuel=100,
        nombre_experiences_precedentes=0,
        annee_experience_totale=0,
        annees_dans_l_entreprise=0,
        annees_dans_le_poste_actuel=0,
        distance_domicile_travail=0,
        annees_depuis_la_derniere_promotion=0,
        nombre_participation_pee=0,
        age=20,
    )
    session.add(emp)
    session.commit()
    assert emp.id is not None

    # Création d'une prédiction liée
    pred = Prediction(employee_id=emp.id, probability=0.5)
    session.add(pred)
    session.commit()
    assert pred.id is not None and pred.employee_id == emp.id

    # Lecture
    e = session.get(Employee, emp.id)
    assert e and e.poste == "Test"
    p = session.get(Prediction, pred.id)
    assert p and p.probability == 0.5

    # Suppression
    session.delete(p)
    session.delete(e)
    session.commit()
    assert session.get(Prediction, pred.id) is None
    assert session.get(Employee, emp.id) is None

    session.close()
