import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.src.core.database import Base, get_db
from backend.src.core.security import hash_password
from backend.src.models.patient import User, Patient
from backend.src.main import app

# In-memory SQLite engine for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_caregiver(db_session):
    user = User(
        id="caregiver-test-id",
        username="test_caregiver",
        hashed_password=hash_password("CaregiverSecret123"),
        role="caregiver",
        full_name="Caregiver Anita",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_patient(db_session, test_caregiver):
    patient = Patient(
        id="patient-test-id",
        caregiver_id=test_caregiver.id,
        anonymized_code="NER-PAT-001",
        preferred_language="Assamese",
        age=72,
    )
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    return patient
