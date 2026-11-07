import re
from pathlib import Path

import joblib


def _keywords(text):
    lower = text.lower()
    urgent = [word for word in ["urgent", "immediately", "today", "now", "asap"] if word in lower]
    financial = [word for word in ["otp", "bank", "card", "payment", "verify", "transfer", "atm"] if word in lower]
    suspicious = [word for word in ["won", "prize", "claim", "click", "link", "blocked", "suspended"] if word in lower]
    return urgent, financial, suspicious


def analyze_text(text: str, source_type: str = "Other"):
    text = (text or "").strip()
    urgent, financial, suspicious = _keywords(text)
    heuristic_score = 0.35
    if urgent:
        heuristic_score += 0.2
    if financial:
        heuristic_score += 0.2
    if suspicious:
        heuristic_score += 0.2
    heuristic_score = min(0.95, heuristic_score)

    model_path = Path(__file__).resolve().parents[2] / "ml" / "text_model" / "model" / "model.joblib"
    vectorizer_path = Path(__file__).resolve().parents[2] / "ml" / "text_model" / "model" / "vectorizer.joblib"
    if model_path.exists() and vectorizer_path.exists():
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        features = vectorizer.transform([text])
        probability = float(model.predict_proba(features)[0][1])
    else:
        probability = heuristic_score

    classification = "scam" if probability >= 0.52 else "legitimate"
    evidence = []
    if urgent:
        evidence.append("Urgency language detected")
    if financial:
        evidence.append("Financial request detected")
    if suspicious:
        evidence.append("Suspicious instruction detected")
    if not evidence:
        evidence.append("No strong scam cue detected by the model")

    explanation = (
        f"This message was analyzed with a TF-IDF + logistic model and suspicious linguistic signals. "
        f"Source type: {source_type}."
    )
    return {
        "probability": round(probability, 4),
        "classification": classification,
        "evidence": evidence,
        "keywords": urgent + financial + suspicious,
        "explanation": explanation,
    }
