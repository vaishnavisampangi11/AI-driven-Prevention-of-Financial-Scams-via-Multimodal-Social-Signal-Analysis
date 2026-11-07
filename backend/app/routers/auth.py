from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.database import get_db
from app.models import User
from app.schemas import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    new_user = User(name=user.name.strip(), email=user.email.lower(), password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "data": {"message": "Registration successful", "user_id": new_user.id}}


@router.post("/login", response_model=dict)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    token = create_access_token(subject=user.email)
    return {"success": True, "data": {"token": token, "user": {"id": user.id, "name": user.name, "email": user.email}}}


@router.get("/me", response_model=dict)
def me(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role, "created_at": current_user.created_at.isoformat()}}
