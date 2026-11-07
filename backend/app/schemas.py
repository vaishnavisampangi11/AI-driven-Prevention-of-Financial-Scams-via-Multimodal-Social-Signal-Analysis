from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisCreate(BaseModel):
    input_type: str
    input_content: str
    source_type: Optional[str] = None


class AnalysisResult(BaseModel):
    analysis_id: Optional[int] = None
    risk_score: float
    risk_level: str
    classification: str
    evidence: List[str]
    explanation: str
    recommendation: str
    decision: str
    probability: Optional[float] = None
    detector_type: Optional[str] = None
    details: Optional[dict[str, Any]] = None


class AlertResponse(BaseModel):
    id: int
    severity: str
    message: str
    is_read: bool
    created_at: datetime
    analysis_id: Optional[int]

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    total: int
    safe: int
    suspicious: int
    high_risk: int
    critical: int
    recent_analyses: List[dict]
    recent_alerts: List[dict]


class HistoryItem(BaseModel):
    id: int
    input_type: str
    classification: str
    risk_score: float
    risk_level: str
    created_at: datetime
    recommendation: str

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
