import os
import pandas as pd
import logging
from sqlalchemy import inspect
from App.API.db import SessionLocal, engine, init_db
from App.API.models import Employee

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_columns(table_name: str) -> set:
    """Retourne la liste des colonnes réellement présentes dans la base."""
    inspector = inspect(engine)
    columns = {col["name"] for col in inspector.get_columns(table_name)}
    return columns

def table_exists(table_name: str) -> bool:
    """Vérifie si la table existe physiquement en base."""
    inspector = inspect(engine)
    return inspector.has_table(table_name)

def table_is_empty(session, model) -> bool:
    """Vérifie si la table contient déjà des données."""
    return session.query(model).first() is None

def load_employees_from_csv(session, csv_path: str):
    """Charge les données depuis le CSV, filtre les colonnes inutiles, insère dans la DB."""
    try:
        df = pd.read_csv(csv_path)
        df = df.where(pd.notnull(df), None)  # Nettoie les NaN → None

        # Colonnes du CSV
        csv_columns = set(df.columns)

        # Colonnes réellement présentes dans la table
        db_columns = get_db_columns("employees")

        # Comparaison
        extra_columns = csv_columns - db_columns
        missing_columns = db_columns - csv_columns

        logger.info(f"✅ Colonnes de la table 'employees' (PostgreSQL) : {sorted(db_columns)}")
        logger.info(f"📄 Colonnes du fichier CSV : {sorted(csv_columns)}")

        if extra_columns:
            logger.warning(f"🟡 Colonnes en trop dans le CSV : {sorted(extra_columns)} (elles seront ignorées)")
        if missing_columns:
            logger.warning(f"🔴 Colonnes manquantes dans le CSV : {sorted(missing_columns)} (valeurs par défaut utilisées ou erreur possible)")

        # Filtrage automatique du DataFrame
        filtered_df = df[[col for col in df.columns if col in db_columns]]
        logger.info(f"📤 {len(filtered_df)} lignes prêtes à l’insertion avec {len(filtered_df.columns)} colonnes valides.")

        # Création des objets Employee
        employees = [Employee(**row) for row in filtered_df.to_dict(orient="records")]
        session.add_all(employees)
        session.commit()
        logger.info(f"✅ {len(employees)} employés insérés avec succès.")
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement du CSV : {e}")
        session.rollback()
        raise

def main():
    logger.info("🔄 Initialisation de la base de données...")
    init_db()

    session = SessionLocal()
    try:
        if not table_exists("employees"):
            logger.info("📋 Table 'employees' absente. Création en cours...")
            init_db()

        if table_is_empty(session, Employee):
            logger.info("📥 Table 'employees' vide. Insertion des données depuis le CSV...")
            csv_path = os.path.abspath("df_merged_export.csv")
            load_employees_from_csv(session, csv_path)
        else:
            logger.info("✅ La table 'employees' contient déjà des données. Aucun chargement effectué.")
    finally:
        session.close()
        logger.info("🔚 Connexion à la base fermée.")

if __name__ == "__main__":
    main()