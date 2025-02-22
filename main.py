from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel
from io import BytesIO
import boto3
import joblib
from huggingface_hub import hf_hub_download, login
import os
HF_TOKEN = os.getenv("HF_ACCESS_TOKEN")  # Securely fetch from environment

def load_model():
    model_path = hf_hub_download(repo_id="Shashankhmg/citybike-demnd-prediction", filename="RF.joblib")
    return joblib.load(model_path)

model = load_model()

# Define input data structure
class InputData(BaseModel):
    start_station_id: int
    hour_of_day: int
    day_of_week: int
    weekend: int
    month: int
    rush_hour: int
    avg_rolling_7days: float
    avg_rolling_30days: float
    start_lat: float
    start_lng: float

@app.post("/predict")
def predict(data: InputData):
    features = np.array([[data.start_station_id, data.hour_of_day, data.day_of_week, data.weekend, data.month, data.rush,
                        data.avg_rolling_7days, data.avg_rolling_30days, data.start_lat, data.start_lng]])
    prediction = model.predict(features)
    return {"predicted_demand": prediction.tolist()}
