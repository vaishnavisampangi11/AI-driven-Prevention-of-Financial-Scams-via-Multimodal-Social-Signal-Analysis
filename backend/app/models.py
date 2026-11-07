from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    input_type = Column(String, nullable=False)
    input_content = Column(Text, nullable=False)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="SAFE")
    classification = Column(String, default="LEGITIMATE")
    recommendation = Column(Text, default="")
    decision = Column(String, default="ALLOW")
    created_at = Column(DateTime, default=datetime.utcnow)


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    detector_type = Column(String, nullable=False)
    probability = Column(Float, default=0.0)
    classification = Column(String, default="UNKNOWN")
    evidence = Column(Text, default="")
    feature_data = Column(Text, default="")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    severity = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScamCase(Base):
    __tablename__ = "scam_cases"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    status = Column(String, default="open")
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
