from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SyncStatus(str, Enum):
    PENDING = "PENDING"
    SYNCED = "SYNCED"
    FAILED = "FAILED"


class GameSessionEvent(BaseModel):
    """
    Immutable, client-generated cognitive game session event.
    Every offline session is uniquely identified by client_uuid.
    """

    client_uuid: str = Field(
        ..., description="Unique UUIDv4 generated on-device before offline storage"
    )
    patient_id: str = Field(..., description="Anonymized patient identifier")
    game_id: str = Field(..., description="Identifier of the cognitive activity played")
    difficulty_level: int = Field(
        ..., ge=1, le=5, description="Difficulty level during the session"
    )
    accuracy: float = Field(
        ..., ge=0.0, le=1.0, description="Task accuracy percentage (0.0 to 1.0)"
    )
    duration_seconds: float = Field(
        ..., ge=0.0, description="Duration in seconds taken to complete activity"
    )
    hints_used: int = Field(
        default=0, ge=0, description="Number of hints requested by user"
    )
    completed_at: datetime = Field(
        ..., description="Timestamp when the activity was completed on-device"
    )
    metadata: dict[str, Any] | None = Field(
        default_factory=dict, description="Game-specific event telemetry"
    )


class SyncEventBatch(BaseModel):
    """Batch of offline session events submitted to /sync/upload."""

    device_id: str = Field(..., description="Paired hardware/app device token")
    events: list[GameSessionEvent] = Field(..., min_length=1, max_length=100)


class SyncUploadResponse(BaseModel):
    """Result of processing a sync batch."""

    accepted_uuids: list[str]
    rejected_uuids: list[dict[str, str]]
    duplicate_uuids: list[str]
    total_processed: int
