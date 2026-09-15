from backend.src.core.database import get_db
from backend.src.services.sync_service import SyncService
from fastapi import APIRouter, Depends, status
from shared.schemas.sync_event import SyncEventBatch, SyncUploadResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/upload", response_model=SyncUploadResponse, status_code=status.HTTP_200_OK)
def upload_sync_batch(batch: SyncEventBatch, db: Session = Depends(get_db)):
    """
    Idempotent batch upload endpoint for offline-generated game sessions.
    Identified by client_uuid. Duplicate submissions are safely ignored.
    """
    return SyncService.process_batch(db, batch)
