import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.explanation_engine import build_explanation
from app.models import Analysis, DetectionResult, User

router = APIRouter(prefix="/api/analyses", tags=["history"])


@router.get("/history")
def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "success": True,
        "data": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "items": [
                {
                    "id": analysis.id,
                    "input_type": analysis.input_type,
                    "classification": analysis.classification,
                    "risk_score": analysis.risk_score,
                    "risk_level": analysis.risk_level,
                    "recommendation": analysis.recommendation,
                    "created_at": analysis.created_at.isoformat(),
                }
                for analysis in items
            ],
        },
    }


@router.get("/{analysis_id}")
def get_analysis_by_id(analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    detection = db.query(DetectionResult).filter(DetectionResult.analysis_id == analysis.id).order_by(DetectionResult.id.desc()).first()
    try:
        evidence = json.loads(detection.evidence) if detection and detection.evidence else []
    except (TypeError, json.JSONDecodeError):
        evidence = []
    try:
        features = json.loads(detection.feature_data) if detection and detection.feature_data else {}
    except (TypeError, json.JSONDecodeError):
        features = {}
    detector_type = analysis.input_type.lower() if analysis.input_type.lower() in {"text", "url"} else "qr"
    explanation = build_explanation(detector_type, {"features": features, "keywords": features.get("keywords", []), "url_risk": analysis.risk_score / 100})["summary"]
    return {"success": True, "data": {"id": analysis.id, "input_type": analysis.input_type, "input_content": analysis.input_content, "risk_score": analysis.risk_score, "risk_level": analysis.risk_level, "classification": analysis.classification, "recommendation": analysis.recommendation, "decision": analysis.decision, "evidence": evidence, "features": features, "explanation": explanation, "created_at": analysis.created_at.isoformat()}}
