from backend.src.core.security import create_access_token


def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "MINDCARE NER Backend"


def test_patient_listing_authorized(client, test_caregiver, test_patient):
    token = create_access_token(
        {"sub": test_caregiver.id, "username": test_caregiver.username, "role": "caregiver"}
    )
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/patients", headers=headers)
    assert response.status_code == 200
    patients = response.json()
    assert len(patients) >= 1
    assert any(p["anonymized_code"] == "NER-PAT-001" for p in patients)


def test_patient_creation_conflict(client, test_caregiver, test_patient):
    token = create_access_token(
        {"sub": test_caregiver.id, "username": test_caregiver.username, "role": "caregiver"}
    )
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to create duplicate anonymized code
    response = client.post(
        "/api/v1/patients",
        headers=headers,
        json={"anonymized_code": "NER-PAT-001", "preferred_language": "Bodo"},
    )
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]
