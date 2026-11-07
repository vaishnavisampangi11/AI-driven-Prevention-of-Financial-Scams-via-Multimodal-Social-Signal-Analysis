from sqlalchemy.orm import Session

from app.models import Alert


def create_alert(db: Session, user_id: int, analysis_id: int, severity: str, message: str):
    alert = Alert(user_id=user_id, analysis_id=analysis_id, severity=severity, message=message)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
