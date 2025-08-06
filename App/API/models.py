# models.py

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    heure_supplementaires           = Column(String,  nullable=False)
    genre                           = Column(String,  nullable=False)
    poste                           = Column(String,  nullable=False)
    niveau_hierarchique_poste = Column(Integer, nullable=False)
    domaine_etude                   = Column(String,  nullable=False)
    departement                     = Column(String,  nullable=False)
    augementation_salaire_precedente= Column(String,  nullable=False)
    frequence_deplacement           = Column(String,  nullable=False)
    statut_marital                  = Column(String,  nullable=False)
    satisfaction_employee_environnement    = Column(Integer, nullable=False)
    note_evaluation_precedente             = Column(Integer, nullable=False)
    satisfaction_employee_nature_travail   = Column(Integer, nullable=False)
    satisfaction_employee_equipe            = Column(Integer, nullable=False)
    satisfaction_employee_equilibre_pro_perso = Column(Integer, nullable=False)
    niveau_education                = Column(Integer, nullable=False)
    nb_formations_suivies           = Column(Integer, nullable=False)
    revenu_mensuel                  = Column(Integer, nullable=False)
    nombre_experiences_precedentes = Column(Integer, nullable=False)
    annee_experience_totale         = Column(Integer, nullable=False)
    annees_dans_l_entreprise        = Column(Integer, nullable=False)
    annees_dans_le_poste_actuel     = Column(Integer, nullable=False)
    distance_domicile_travail       = Column(Integer, nullable=False)
    annees_depuis_la_derniere_promotion = Column(Integer, nullable=False)
    nombre_participation_pee        = Column(Integer, nullable=False)
    age                             = Column(Integer, nullable=False)

    # relation vers les prédictions
    predictions = relationship("Prediction", back_populates="employee")


class Prediction(Base):
    __tablename__ = "predictions"

    id           = Column(Integer, primary_key=True, index=True)
    employee_id  = Column(Integer, ForeignKey("employees.id"), nullable=False)
    timestamp    = Column(DateTime, default=datetime.utcnow, nullable=False)
    probability  = Column(Float, nullable=False)
    # si vous préférez stocker tout l'input JSON directement :
    # input_data = Column(JSON, nullable=False)

    employee = relationship("Employee", back_populates="predictions")