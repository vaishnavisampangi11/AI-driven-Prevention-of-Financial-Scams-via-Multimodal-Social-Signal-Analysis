from pathlib import Path

import joblib

from ml.url_model.features import extract_url_features


def analyze_url(url: str):
    features = extract_url_features(url)
    model_path = Path(__file__).resolve().parents[2] / "ml" / "url_model" / "model" / "url_model.joblib"
    if model_path.exists():
        model = joblib.load(model_path)
        probability = float(model.predict_proba([[
            features.get("url_length", 0),
            features.get("hostname_length", 0),
            features.get("dots_count", 0),
            features.get("subdomain_count", 0),
            features.get("special_char_count", 0),
            features.get("digits_count", 0),
            features.get("hyphen_count", 0),
            1 if features.get("has_https") else 0,
            1 if features.get("is_ip_host") else 0,
            1 if features.get("has_at_symbol") else 0,
            1 if features.get("has_encoded_chars") else 0,
            features.get("path_length", 0),
            features.get("query_length", 0),
        ]])[0][1])
    else:
        probability = 0.5
        if features.get("subdomain_count", 0) >= 2:
            probability += 0.12
        if not features.get("has_https"):
            probability += 0.15
        if features.get("is_ip_host"):
            probability += 0.18
        if features.get("path_length", 0) > 35:
            probability += 0.1
        if features.get("url_length", 0) > 60:
            probability += 0.1
        probability = min(0.96, probability)

    classification = "phishing" if probability >= 0.55 else "safe"
    evidence = []
    if features.get("url_length", 0) > 75:
        evidence.append("Very long URL")
    if features.get("subdomain_count", 0) >= 2:
        evidence.append("Multiple subdomains")
    if not features.get("has_https"):
        evidence.append("Missing HTTPS")
    if features.get("is_ip_host"):
        evidence.append("IP-based hostname")
    if features.get("suspicious_keywords"):
        evidence.append("Suspicious keyword in hostname or path")
    if not evidence:
        evidence.append("No major phishing indicators were detected")

    return {
        "probability": round(probability, 4),
        "classification": classification,
        "features": features,
        "evidence": evidence,
    }
