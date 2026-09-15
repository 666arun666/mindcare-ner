from backend.src.models.patient import Patient
from backend.src.models.session import GameSession
from shared.schemas.sync_event import SyncEventBatch, SyncUploadResponse
from sqlalchemy.orm import Session


class SyncService:
    @staticmethod
    def process_batch(db: Session, batch: SyncEventBatch) -> SyncUploadResponse:
        accepted: list[str] = []
        rejected: list[dict] = []
        duplicates: list[str] = []

        for event in batch.events:
            # 1. Verify patient exists (or create a stub if in paired testing mode)
            patient = db.query(Patient).filter(Patient.id == event.patient_id).first()
            if not patient:
                # To maintain resilience for offline registered patients, check if patient exists or reject
                # If patient is completely unknown, we record reason
                rejected.append(
                    {
                        "uuid": event.client_uuid,
                        "reason": f"Unknown patient_id '{event.patient_id}'",
                    }
                )
                continue

            # 2. Idempotency Check: Check if client_uuid has already been ingested
            existing = (
                db.query(GameSession).filter(GameSession.client_uuid == event.client_uuid).first()
            )
            if existing:
                # Idempotent success: already recorded, suppress duplicate insertion
                duplicates.append(event.client_uuid)
                continue

            # 3. Insert new session event
            new_session = GameSession(
                client_uuid=event.client_uuid,
                patient_id=event.patient_id,
                game_id=event.game_id,
                difficulty_level=event.difficulty_level,
                accuracy=event.accuracy,
                duration_seconds=event.duration_seconds,
                hints_used=event.hints_used,
                completed_at=event.completed_at,
                session_metadata=event.metadata or {},
            )
            db.add(new_session)
            accepted.append(event.client_uuid)

        db.commit()

        return SyncUploadResponse(
            accepted_uuids=accepted,
            rejected_uuids=rejected,
            duplicate_uuids=duplicates,
            total_processed=len(batch.events),
        )
