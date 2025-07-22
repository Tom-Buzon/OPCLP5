from fastapi import FastAPI
from App.API.schemas import InputData
from App.API.predictor import predict_with_model

app = FastAPI()

@app.post("/predict")
def predict(data: InputData):
    return predict_with_model(data)
