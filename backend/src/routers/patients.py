from backend.src.core.database import get_db
from backend.src.core.security import require_role
from backend.src.models.patient import Patient
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

router = APIRouter(prefix="/patients", tags=["patients"])


class PatientResponse(BaseModel):
    id: str
    anonymized_code: str
    preferred_language: str
    age: int | None = None

    model_config = ConfigDict(from_attributes=True)


class CreatePatientRequest(BaseModel):
    anonymized_code: str
    preferred_language: str = "Assamese"
    age: int | None = None


@router.get("", response_model=list[PatientResponse])
def list_patients(
    db: Session = Depends(get_db),
    user: dict = Depends(require_role("caregiver")),
):
    caregiver_id = user["sub"]
    return db.query(Patient).filter(Patient.caregiver_id == caregiver_id).all()


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    req: CreatePatientRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_role("caregiver")),
):
    existing = db.query(Patient).filter(Patient.anonymized_code == req.anonymized_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Patient with code '{req.anonymized_code}' already registered",
        )
    patient = Patient(
        caregiver_id=user["sub"],
        anonymized_code=req.anonymized_code,
        preferred_language=req.preferred_language,
        age=req.age,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
