import uuid

from backend.src.core.database import Base
from backend.src.models.base import TimestampMixin
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String


class GameSession(Base, TimestampMixin):
    """
    Durable record of a cognitive game session synced from an offline device.
    client_uuid is unique and provided by the client device.
    """

    __tablename__ = "game_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_uuid = Column(String(36), unique=True, index=True, nullable=False)
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    game_id = Column(String(64), nullable=False, index=True)
    difficulty_level = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)
    duration_seconds = Column(Float, nullable=False)
    hints_used = Column(Integer, default=0, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=False)
    session_metadata = Column(JSON, default=dict, nullable=False)
