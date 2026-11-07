from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, Analysis, User
from app.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total = db.query(Analysis).filter(Analysis.user_id == current_user.id).count()
    safe = db.query(Analysis).filter(Analysis.user_id == current_user.id, Analysis.risk_level == "SAFE").count()
    suspicious = db.query(Analysis).filter(Analysis.user_id == current_user.id, Analysis.risk_level == "SUSPICIOUS").count()
    high_risk = db.query(Analysis).filter(Analysis.user_id == current_user.id, Analysis.risk_level == "HIGH RISK").count()
    critical = db.query(Analysis).filter(Analysis.user_id == current_user.id, Analysis.risk_level == "CRITICAL").count()

    recent_analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).limit(5).all()
    recent_alerts = db.query(Alert).filter(Alert.user_id == current_user.id).order_by(Alert.created_at.desc()).limit(5).all()

    return {
        "success": True,
        "data": {
            "total": total,
            "safe": safe,
            "suspicious": suspicious,
            "high_risk": high_risk,
            "critical": critical,
            "recent_analyses": [
                {
                    "id": a.id,
                    "input_type": a.input_type,
                    "classification": a.classification,
                    "risk_score": a.risk_score,
                    "risk_level": a.risk_level,
                    "created_at": a.created_at.isoformat(),
                }
                for a in recent_analyses
            ],
            "recent_alerts": [
                {"id": a.id, "severity": a.severity, "message": a.message, "created_at": a.created_at.isoformat()}
                for a in recent_alerts
            ],
        },
    }
