import json
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from ml.url_model.features import extract_url_features

DATASET = [
    {"url": "https://bankofamerica.com/security/verify", "label": "legitimate"},
    {"url": "https://www.example.com/account/login", "label": "legitimate"},
    {"url": "https://docs.company.com/portal", "label": "legitimate"},
    {"url": "http://secure-bank-login-update.com/verify?token=123", "label": "phishing"},
    {"url": "https://bit.ly/claim-prize-otp-verify", "label": "phishing"},
    {"url": "http://34.198.56.12/secure/payment/confirm", "label": "phishing"},
    {"url": "https://account-update-verify-login-official.net/confirm", "label": "phishing"},
]


def build_feature_vector(url: str):
    features = extract_url_features(url)
    return [
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


def train_model():
    items = [build_feature_vector(entry["url"]) for entry in DATASET]
    labels = [1 if entry["label"] == "phishing" else 0 for entry in DATASET]

    X_train, X_test, y_train, y_test = train_test_split(items, labels, test_size=0.25, random_state=42, stratify=labels)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("Demo URL dataset metrics:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"F1: {f1_score(y_test, y_pred, zero_division=0):.4f}")

    output_dir = Path(__file__).resolve().parent / "model"
    output_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_dir / "url_model.joblib")
    metadata = {
        "type": "Random Forest on URL lexical features",
        "description": "Demo/sample URL dataset only for academic project demonstration.",
        "label_map": {"0": "safe", "1": "phishing"},
    }
    with open(output_dir / "metadata.json", "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)
    print(f"Saved URL model to {output_dir}")


if __name__ == "__main__":
    train_model()
