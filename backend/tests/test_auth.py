def test_auth_login_success(client, test_caregiver):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test_caregiver", "password": "CaregiverSecret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "caregiver"
    assert data["username"] == "test_caregiver"


def test_auth_login_invalid_credentials(client, test_caregiver):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "test_caregiver", "password": "WrongPassword"},
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


def test_protected_route_without_token(client):
    response = client.get("/api/v1/patients")
    assert response.status_code == 401
    assert "Authentication token missing" in response.json()["detail"]
