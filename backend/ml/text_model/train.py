import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

DATASET = [
    {"text": "Your electricity bill is ready. View your bill in the official application.", "label": "legitimate"},
    {"text": "Your account statement is ready in the official online banking portal.", "label": "legitimate"},
    {"text": "We have updated your profile. Please log in to confirm your account details.", "label": "legitimate"},
    {"text": "URGENT! Your bank account will be blocked today. Send OTP immediately.", "label": "scam"},
    {"text": "Congratulations! You won a prize. Pay ₹500 to claim your reward now.", "label": "scam"},
    {"text": "Action needed: verify your identity and transfer money to unlock access.", "label": "scam"},
    {"text": "Your package is delayed. Please confirm delivery details through the secure link.", "label": "scam"},
]


def train_model():
    texts = [item["text"] for item in DATASET]
    labels = [1 if item["label"] == "scam" else 0 for item in DATASET]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X = vectorizer.fit_transform(texts)
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.25, random_state=42, stratify=labels)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print("Demo dataset metrics:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1: {f1:.4f}")

    output_dir = Path(__file__).resolve().parent / "model"
    output_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, output_dir / "vectorizer.joblib")
    joblib.dump(model, output_dir / "model.joblib")
    metadata = {
        "type": "TF-IDF + Logistic Regression",
        "description": "Demo/sample dataset only for academic project demonstration.",
        "label_map": {"0": "legitimate", "1": "scam"},
    }
    with open(output_dir / "metadata.json", "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    print(f"Saved model and vectorizer to {output_dir}")


if __name__ == "__main__":
    train_model()
