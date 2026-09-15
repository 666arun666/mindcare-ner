import uuid

from backend.src.core.database import Base
from backend.src.models.base import TimestampMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(64), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(32), default="caregiver", nullable=False)  # caregiver, admin
    full_name = Column(String(128), nullable=False)


class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    caregiver_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    anonymized_code = Column(String(64), unique=True, index=True, nullable=False)
    preferred_language = Column(String(32), default="Assamese", nullable=False)
    age = Column(Integer, nullable=True)
    device_token = Column(String(128), unique=True, nullable=True)

    sessions = relationship("GameSession", backref="patient", lazy="dynamic")
