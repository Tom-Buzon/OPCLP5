from fastapi import FastAPI, HTTPException
from App.Api.schemas import EmployeeInput, PredictionResult
from App.Api.predictor import load_model, predict_quit

app = FastAPI(title="API de Prédiction de Départ")

# Mettre le modèle en variable globale (initialement None)
model = None

@app.on_event("startup")
def load_ml_model():
    global model
    model = load_model()

@app.get("/")
def root():
    return {"message": "API opérationnelle 🚀"}

@app.post("/predict", response_model=PredictionResult)
def predict(input_data: EmployeeInput):
    try:
        proba = predict_quit(input_data, model)
        return {"probability": proba}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
