import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import settings
from app.database import get_db
from app.decision_engine import decide_action
from app.explanation_engine import build_explanation
from app.models import Alert, Analysis, DetectionResult, User
from app.risk_engine import calculate_risk_score, risk_level
from app.services.alert_service import create_alert
from app.services.qr_detector import decode_qr_image
from app.services.text_detector import analyze_text
from app.services.url_detector import analyze_url
from app.utils.security import validate_upload_file
from app.utils.validators import clean_input, is_valid_url, safe_text_length

router = APIRouter(prefix="/api", tags=["analysis"])


def _persist_analysis(db: Session, user: User, input_type: str, input_content: str, result: dict, detector_type: str):
    classification = result["classification"].upper() if isinstance(result.get("classification"), str) else "LEGITIMATE"
    score = float(result.get("risk_score", 0))
    level = result.get("risk_level", "SAFE")
    recommendation = result.get("recommendation", "")
    decision = result.get("decision", "ALLOW")
    analysis = Analysis(
        user_id=user.id,
        input_type=input_type,
        input_content=input_content,
        risk_score=score,
        risk_level=level,
        classification=classification,
        recommendation=recommendation,
        decision=decision,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    db.add(
        DetectionResult(
            analysis_id=analysis.id,
            detector_type=detector_type,
            probability=float(result.get("probability", 0.0)),
            classification=classification,
            evidence=json.dumps(result.get("evidence", [])),
            feature_data=json.dumps(result.get("features", {})),
        )
    )
    db.commit()

    if level in {"SUSPICIOUS", "HIGH RISK", "CRITICAL"}:
        severity = "HIGH" if level == "HIGH RISK" else "CRITICAL" if level == "CRITICAL" else "MEDIUM"
        create_alert(db, user.id, analysis.id, severity, f"{level} scam alert detected for {input_type} analysis.")
    return analysis


@router.post("/analyses/text")
def analyze_text_endpoint(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    text = clean_input(payload.get("input_text") or payload.get("text") or "")
    if not text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text input is required.")
    if not safe_text_length(text):
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Text exceeds the 4000-character limit.")

    detector = analyze_text(text, source_type=payload.get("source_type", "Other"))
    probability = float(detector["probability"])
    risk_score = round(probability * 100, 2)
    level = risk_level(risk_score)
    explanation = build_explanation("text", {"keywords": detector.get("keywords", []), "financial_request": "payment" in text.lower()})
    decision = decide_action(risk_score)
    result = {
        "risk_score": risk_score,
        "risk_level": level,
        "classification": "SCAM" if probability >= 0.55 else "LEGITIMATE",
        "evidence": detector["evidence"],
        "probability": probability,
        "features": {"keywords": detector.get("keywords", []), "source_type": payload.get("source_type", "Other")},
        "explanation": explanation["summary"],
        "recommendation": decision["action"],
        "decision": decision["decision"],
    }
    analysis = _persist_analysis(db, current_user, "TEXT", text, result, "text")
    result["analysis_id"] = analysis.id
    return {"success": True, "data": result}


@router.post("/analyses/url")
def analyze_url_endpoint(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    url = (payload.get("url") or "").strip()
    if not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is required.")
    if not is_valid_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL is invalid or malformed.")

    detector = analyze_url(url)
    risk_score = round(detector["probability"] * 100, 2)
    level = risk_level(risk_score)
    explanation = build_explanation("url", {"features": detector["features"]})
    decision = decide_action(risk_score)
    result = {
        "risk_score": risk_score,
        "risk_level": level,
        "classification": detector["classification"].upper(),
        "evidence": detector["evidence"],
        "probability": detector["probability"],
        "features": detector["features"],
        "explanation": explanation["summary"],
        "recommendation": decision["action"],
        "decision": decision["decision"],
    }
    analysis = _persist_analysis(db, current_user, "URL", url, result, "url")
    result["analysis_id"] = analysis.id
    return {"success": True, "data": result}


@router.post("/analyses/qr")
def analyze_qr_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    upload_path = validate_upload_file(file, settings.UPLOAD_DIR)
    temp_path = str(upload_path)
    try:
        with open(temp_path, "wb") as out:
            content = file.file.read()
            out.write(content)
        decoded = decode_qr_image(temp_path)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"QR processing failed: {str(exc)}")

    content_value = decoded["decoded_content"]
    url = content_value if decoded["is_url"] else None
    detector_result = {
        "risk_score": 10,
        "risk_level": "SAFE",
        "classification": "LEGITIMATE",
        "evidence": ["QR data was successfully decoded."],
        "probability": 0.1,
        "features": {"decoded_content": content_value, "is_url": decoded["is_url"]},
        "explanation": "The QR code was decoded and checked for embedded content.",
        "recommendation": "Proceed with caution.",
        "decision": "ALLOW",
    }

    if url:
        url_result = analyze_url(url)
        detector_result = {
            "risk_score": round(url_result["probability"] * 100, 2),
            "risk_level": risk_level(round(url_result["probability"] * 100, 2)),
            "classification": url_result["classification"].upper(),
            "evidence": url_result["evidence"],
            "probability": url_result["probability"],
            "features": url_result["features"],
            "explanation": build_explanation("qr", {"url_risk": url_result["probability"]})["summary"],
            "recommendation": decide_action(round(url_result["probability"] * 100, 2))["action"],
            "decision": decide_action(round(url_result["probability"] * 100, 2))["decision"],
        }
    else:
        text_result = analyze_text(content_value, "Other")
        detector_result = {
            "risk_score": round(text_result["probability"] * 100, 2),
            "risk_level": risk_level(round(text_result["probability"] * 100, 2)),
            "classification": text_result["classification"].upper(),
            "evidence": text_result["evidence"],
            "probability": text_result["probability"],
            "features": {"decoded_content": content_value},
            "explanation": build_explanation("text", {"keywords": text_result.get("keywords", [])})["summary"],
            "recommendation": decide_action(round(text_result["probability"] * 100, 2))["action"],
            "decision": decide_action(round(text_result["probability"] * 100, 2))["decision"],
        }

    analysis = _persist_analysis(db, current_user, "QR", content_value, detector_result, "qr")
    detector_result["analysis_id"] = analysis.id
    detector_result["decoded_content"] = content_value
    detector_result["detected_url"] = url
    return {"success": True, "data": detector_result}
