from pathlib import Path

import joblib

from ml.url_model.features import extract_url_features

MODEL_DIR = Path(__file__).resolve().parent / "model"


def predict_url(url: str):
    model = joblib.load(MODEL_DIR / "url_model.joblib")
    features = extract_url_features(url)
    vector = [
        features["url_length"],
        features["hostname_length"],
        features["dots_count"],
        features["subdomain_count"],
        features["special_char_count"],
        features["digits_count"],
        features["hyphen_count"],
        1 if features["has_https"] else 0,
        1 if features["is_ip_host"] else 0,
        1 if features["has_at_symbol"] else 0,
        1 if features["has_encoded_chars"] else 0,
        features["path_length"],
        features["query_length"],
    ]
    probability = float(model.predict_proba([vector])[0][1])
    return {"probability": probability, "classification": "phishing" if probability >= 0.5 else "safe"}
