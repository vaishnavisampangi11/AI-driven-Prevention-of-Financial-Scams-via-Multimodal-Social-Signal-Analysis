from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user, hash_password, verify_password
from app.database import get_db
from app.models import Alert, Analysis, DetectionResult, ScamCase, User

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("")
def get_profile(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role, "created_at": current_user.created_at.isoformat()}}


@router.put("")
def update_profile(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if "name" in payload and payload["name"]:
        current_user.name = payload["name"]
    if "email" in payload and payload["email"]:
        current_user.email = payload["email"].lower()
    db.commit()
    return {"success": True, "data": {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role}}


@router.put("/password")
def update_password(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_password = payload.get("current_password", "")
    new_password = payload.get("new_password", "")
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect.")
    if len(new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 8 characters long.")
    current_user.password_hash = hash_password(new_password)
    db.commit()
    return {"success": True, "data": {"message": "Password updated successfully."}}


@router.delete("")
def delete_account(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not verify_password(payload.get("password", ""), current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect.")

    analysis_ids = db.query(Analysis.id).filter(Analysis.user_id == current_user.id).subquery()
    db.query(DetectionResult).filter(DetectionResult.analysis_id.in_(analysis_ids)).delete(synchronize_session=False)
    db.query(ScamCase).filter(ScamCase.analysis_id.in_(analysis_ids)).delete(synchronize_session=False)
    db.query(Alert).filter(Alert.user_id == current_user.id).delete(synchronize_session=False)
    db.query(Analysis).filter(Analysis.user_id == current_user.id).delete(synchronize_session=False)
    db.delete(current_user)
    db.commit()
    return {"success": True, "data": {"message": "Account deleted successfully."}}
