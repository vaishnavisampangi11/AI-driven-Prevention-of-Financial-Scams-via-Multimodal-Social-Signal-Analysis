import json
from pathlib import Path

import joblib

MODEL_DIR = Path(__file__).resolve().parent / "model"


def predict_text(message: str):
    vectorizer = joblib.load(MODEL_DIR / "vectorizer.joblib")
    model = joblib.load(MODEL_DIR / "model.joblib")
    vector = vectorizer.transform([message])
    probability = float(model.predict_proba(vector)[0][1])
    return {"probability": probability, "classification": "scam" if probability >= 0.5 else "legitimate"}
