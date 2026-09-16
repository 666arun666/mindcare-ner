import uuid
from datetime import UTC, datetime

from backend.src.models.session import GameSession


def test_offline_sync_lifecycle_and_idempotency(client, test_patient, db_session):
    """
    Simulates:
    1. Offline session created with unique client_uuid
    2. Network connects, uploaded to server -> Accepted
    3. Network timeout / disconnect simulated
    4. Client retries with EXACT same client_uuid
    5. Server suppresses duplicate, returns success, exactly ONE record persists.
    """
    fixed_client_uuid = str(uuid.uuid4())
    completed_time = datetime.now(UTC).isoformat()

    payload = {
        "device_id": "device-tablet-01",
        "events": [
            {
                "client_uuid": fixed_client_uuid,
                "patient_id": test_patient.id,
                "game_id": "memory_match",
                "difficulty_level": 2,
                "accuracy": 0.85,
                "duration_seconds": 45.0,
                "hints_used": 1,
                "completed_at": completed_time,
                "metadata": {"theme": "assam_tea_gardens"},
            }
        ],
    }

    # Step 1: Initial upload
    response_1 = client.post("/api/v1/sync/upload", json=payload)
    assert response_1.status_code == 200
    data_1 = response_1.json()
    assert fixed_client_uuid in data_1["accepted_uuids"]
    assert len(data_1["duplicate_uuids"]) == 0

    # Verify session is persisted in DB
    records_after_first = (
        db_session.query(GameSession).filter(GameSession.client_uuid == fixed_client_uuid).all()
    )
    assert len(records_after_first) == 1

    # Step 2: Retry scenario (identical client_uuid sent again due to presumed network retry)
    response_2 = client.post("/api/v1/sync/upload", json=payload)
    assert response_2.status_code == 200
    data_2 = response_2.json()

    # Step 3: Verify server recognized duplicate and DID NOT insert a second row
    assert fixed_client_uuid in data_2["duplicate_uuids"]
    assert fixed_client_uuid not in data_2["accepted_uuids"]

    records_after_retry = (
        db_session.query(GameSession).filter(GameSession.client_uuid == fixed_client_uuid).all()
    )
    # Critical property: Total rows in database must still be exactly 1
    assert len(records_after_retry) == 1


def test_batch_sync_with_partial_duplicates_and_failures(client, test_patient, db_session):
    """
    Tests a mixed batch:
    - Event 1: New valid session
    - Event 2: Pre-existing duplicate UUID
    - Event 3: Unknown patient ID (rejected)
    """
    existing_uuid = str(uuid.uuid4())
    new_uuid = str(uuid.uuid4())
    completed_time = datetime.now(UTC).isoformat()

    # Pre-seed one session
    seed_session = GameSession(
        client_uuid=existing_uuid,
        patient_id=test_patient.id,
        game_id="sequence_recall",
        difficulty_level=1,
        accuracy=0.9,
        duration_seconds=30.0,
        hints_used=0,
        completed_at=datetime.now(UTC),
    )
    db_session.add(seed_session)
    db_session.commit()

    batch_payload = {
        "device_id": "device-tablet-01",
        "events": [
            {
                "client_uuid": new_uuid,
                "patient_id": test_patient.id,
                "game_id": "pattern_match",
                "difficulty_level": 3,
                "accuracy": 0.75,
                "duration_seconds": 60.0,
                "hints_used": 2,
                "completed_at": completed_time,
            },
            {
                "client_uuid": existing_uuid,
                "patient_id": test_patient.id,
                "game_id": "sequence_recall",
                "difficulty_level": 1,
                "accuracy": 0.9,
                "duration_seconds": 30.0,
                "hints_used": 0,
                "completed_at": completed_time,
            },
            {
                "client_uuid": str(uuid.uuid4()),
                "patient_id": "nonexistent-patient-id",
                "game_id": "memory_match",
                "difficulty_level": 1,
                "accuracy": 0.5,
                "duration_seconds": 50.0,
                "hints_used": 1,
                "completed_at": completed_time,
            },
        ],
    }

    res = client.post("/api/v1/sync/upload", json=batch_payload)
    assert res.status_code == 200
    body = res.json()

    assert new_uuid in body["accepted_uuids"]
    assert existing_uuid in body["duplicate_uuids"]
    assert len(body["rejected_uuids"]) == 1
    assert "Unknown patient_id" in body["rejected_uuids"][0]["reason"]
