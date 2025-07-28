# App/API/db.py

import logging
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupérer les paramètres de connexion
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "OPCLP5")

# Déclarative base SQLAlchemy
Base = declarative_base()

# Importer vos modèles pour qu'ils s'y enregistrent
from . import models  # noqa: F401

# Construire l'URL de connexion dynamiquement
DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Créer l'engine et la factory de sessions
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Initialisation de logging (optionnel)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """
    Vérifie l'existence des tables 'employees' et 'predictions'.
    Si elles n'existent pas, les crée via Base.metadata.create_all().
    """
    inspector = inspect(engine)
    needs_create = not (
        inspector.has_table("employees")
        and inspector.has_table("predictions")
    )

    if needs_create:
        Base.metadata.create_all(bind=engine)
        logger.info(
            "Tables 'employees' et 'predictions' créées. "
            "Connection à la DB établie avec succès."
        )
    else:
        logger.info("Connection à la DB établie avec succès.")


if __name__ == "__main__":
    init_db()
