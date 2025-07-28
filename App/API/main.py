from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .schemas import EmployeeInput, PredictionResult
from .predictor import load_model, predict_quit
from .db import init_db, SessionLocal
from .models import Employee, Prediction
import json

# Initialisation de la base de données
init_db()

app = FastAPI(title="API de Prédiction de Départ")

# Stockage du modèle en variable globale
model = None

@app.on_event("startup")
def load_ml_model():
    global model
    model = load_model()

# Dependency pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API opérationnelle 🚀"}

@app.post("/predict", response_model=PredictionResult)
def predict(input_data: EmployeeInput, db: Session = Depends(get_db)):
    try:
        # Exécution de la prédiction
        proba = predict_quit(input_data, model)

        # Enregistrement en base
        # Crée ou récupère l'employé (à simplifier selon votre logique)
        emp_dict = input_data.dict()
        emp = Employee(**emp_dict)
        db.add(emp)
        db.commit()
        db.refresh(emp)

        # Enregistre la prédiction
        pred = Prediction(employee_id=emp.id, probability=proba)
        db.add(pred)
        db.commit()
        db.refresh(pred)

        return {"probability": proba}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/employees/{employee_id}")
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.get(Employee, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Retourne l'employee et ses prédictions
    return {
        "employee": emp_dict if (emp_dict := emp.__dict__) else {},
        "predictions": [{"id": p.id, "probability": p.probability, "timestamp": p.timestamp} for p in emp.predictions]
    }

@app.get("/predictions/{prediction_id}")
def read_prediction(prediction_id: int, db: Session = Depends(get_db)):
    pred = db.get(Prediction, prediction_id)
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"id": pred.id, "employee_id": pred.employee_id, "probability": pred.probability, "timestamp": pred.timestamp}

@app.get("/employees")
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emps = db.query(Employee).offset(skip).limit(limit).all()
    return [emp.__dict__ for emp in emps]

@app.get("/predictions")
def list_predictions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    preds = db.query(Prediction).offset(skip).limit(limit).all()
    return [{"id": p.id, "employee_id": p.employee_id, "probability": p.probability, "timestamp": p.timestamp} for p in preds]
